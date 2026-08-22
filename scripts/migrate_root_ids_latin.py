#!/usr/bin/env python3
"""把与英文单词同名的词根 id 改成拉丁词形，解除自环边限制。

背景：项目不变量是「词根 id 不得与任何单词 id 相同」，否则图谱出现自环边
（root → word 指向自己）。roots.json 里 `form` 和 `port` 正是英文单词本身，
于是单词 form / port 一直无法入库——vetted_families 里它们始终挂在待办上。

做法（照 punktum/limes/gubernare 已有先例，用拉丁词形）：
    form  → forma   （拉丁语 forma，形状、模子）
    port  → portus  （拉丁语 portus，港口、门道）
    flu   → fluere  （拉丁语 fluere，流动）
    press → premere （拉丁语 premere，压、按）

本脚本累积记录全部改名，幂等：已迁移过的条目再跑是空操作，
故新增一对改名后可直接重跑，不必另写脚本。

需要同步改的引用（已全量核查，无其它引用点）：
    data/roots.json      root.id
    data/words.json      word.root_ids[]
    data/concepts.json   concept.root_ids[]
    data/domains.json    域下的词根清单
    data/relations.json  relation.from

本脚本幂等：已迁移过再跑不会重复改动。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

RENAME = {
    # 第一轮（已提交 d1a29f9）：解锁单词 form / port
    "form": "forma",     # 拉丁语 forma，形状、模子
    "port": "portus",    # 拉丁语 portus，港口、门道
    # 第二轮：解锁单词 flu / press
    "flu": "fluere",     # 拉丁语 fluere，流动
    "press": "premere",  # 拉丁语 premere，压、按
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def as_list(obj, key):
    """data/*.json 有的是裸数组、有的是 {key: [...]}，两种都要支持。"""
    if isinstance(obj, list):
        return obj, None
    return obj.get(key, []), key


def main():
    changes = []

    # 1) roots.json —— 改 id 本身
    obj = load("roots.json")
    roots, key = as_list(obj, "roots")
    for r in roots:
        if r.get("id") in RENAME:
            old = r["id"]
            r["id"] = RENAME[old]
            # root 字段存的是词根书写形式，一并更新为拉丁词形
            if r.get("root") == old:
                r["root"] = RENAME[old]
            # 原英文形保留进 variants，学习者仍能按 form/port 检索
            vs = r.setdefault("variants", [])
            if old not in vs:
                vs.insert(0, old)
            changes.append(f"roots.json: {old} → {r['id']}")
    save("roots.json", obj)

    # 2) words.json —— 改 root_ids
    obj = load("words.json")
    words, _ = as_list(obj, "words")
    n = 0
    for w in words:
        rs = w.get("root_ids") or []
        for i, rid in enumerate(rs):
            if rid in RENAME:
                rs[i] = RENAME[rid]
                n += 1
    save("words.json", obj)
    changes.append(f"words.json: {n} 处 root_ids 改写")

    # 3) concepts.json —— 改 root_ids
    obj = load("concepts.json")
    concepts, _ = as_list(obj, "concepts")
    n = 0
    for c in concepts:
        rs = c.get("root_ids") or []
        for i, rid in enumerate(rs):
            if rid in RENAME:
                rs[i] = RENAME[rid]
                n += 1
    save("concepts.json", obj)
    changes.append(f"concepts.json: {n} 处 root_ids 改写")

    # 4) domains.json —— 改域下词根清单（键名可能是 root_ids 或 roots）
    obj = load("domains.json")
    doms, _ = as_list(obj, "domains")
    n = 0
    for d in doms:
        for field in ("root_ids", "roots"):
            rs = d.get(field)
            if not isinstance(rs, list):
                continue
            for i, rid in enumerate(rs):
                if rid in RENAME:
                    rs[i] = RENAME[rid]
                    n += 1
    save("domains.json", obj)
    changes.append(f"domains.json: {n} 处词根引用改写")

    # 5) relations.json —— 只改词根那一端（from/source）
    #
    # 【坑】不能顺手把 to/target 也改：type=root 的关系是「词根 → 单词」，
    # to 存的是**单词 id**。而单词 form / port / flu / press 本身正好与旧词根
    # 同名，一旦连 to 一起改，forma → form 就会变成 forma → forma 自环——
    # 这正是本迁移要消除的东西。第一次跑没炸，只因当时这些单词还没入库；
    # 第四十三批把 form / port 入库后重跑，立刻炸出两条自环。
    obj = load("relations.json")
    rels, _ = as_list(obj, "relations")
    n = 0
    for r in rels:
        for field in ("from", "source"):
            if r.get(field) in RENAME:
                r[field] = RENAME[r[field]]
                n += 1
    save("relations.json", obj)
    changes.append(f"relations.json: {n} 处词根端改写")

    for c in changes:
        print("  ", c)

    # 迁移后自检：不再有任何词根 id 与单词 id 相同
    roots, _ = as_list(load("roots.json"), "roots")
    words, _ = as_list(load("words.json"), "words")
    rids = {r["id"] for r in roots}
    wids = {w["id"] for w in words}
    clash = rids & wids
    assert not clash, f"仍存在词根/单词同名：{sorted(clash)}"
    assert not (rids & set(RENAME)), "旧词根 id 仍残留"
    # 所有词条的 root_ids 必须都能在 roots 里找到
    dangling = {
        rid for w in words for rid in (w.get("root_ids") or []) if rid not in rids
    }
    assert not dangling, f"root_ids 指向不存在的词根：{sorted(dangling)}"
    # relations 不得出现自环——迁移的全部目的就是消除自环，若反倒造出来则必须当场炸
    rels, _ = as_list(load("relations.json"), "relations")
    loops = [r for r in rels if r.get("from") == r.get("to")]
    assert not loops, f"迁移造出 relations 自环：{[r['from'] for r in loops]}"
    print("   自检通过：无同名、无残留、无悬空 root_ids、无 relations 自环")


if __name__ == "__main__":
    main()
