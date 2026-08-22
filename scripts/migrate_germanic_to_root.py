#!/usr/bin/env python3
"""把误标为 germanic 的词迁到它们真正的词根下。

用法：
    python scripts/migrate_germanic_to_root.py --dry-run
    python scripts/migrate_germanic_to_root.py

【问题来源】
日耳曼型批次的定义是「没有可迁移的拉丁/希腊词族」。起草时若某词的词根
在词表里凑不满 3 个成员，就按 germanic 收入——这本身是对的。
但后续批次可能把那个词根建起来（族成员在别的分片里陆续出现），
先前收的词就成了本该入族却孤立在外的浮点。

本轮由 chunk19 的子代理点出这个盲区（它发现 cage/cave 已作 germanic 入库，
而两者 origin 都写着 cavus）。据此反向扫全部 763 个 germanic 词条，
拿它们的 origin 去比对现有 218 个词根的拉丁词元，命中 14 个，
逐条核后 10 个确为错挂、4 个是子串假阳性：
    choose   → origin 的「gustare」含子串 stare，与 sta 无关
    canvas   → cannabis 与 canna 是两个拉丁词
    colonel  → columna（柱）与 colere（耕作）无关
    autonomy → 与 oikonomia 只共有 nomos 一半，本身是 autos＋nomos

【本脚本做什么】
对下面 10 词：decomposable 由 germanic 改 root、写入 root_ids 与 root_logic、
在 relations 里补一条「词根 → 单词」的边、把词加进该根与该概念的 word_ids。
即 review.py merge 对词根型词条所做的那一套。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# 单词 -> (词根 id, root_logic)
MOVE = {
    "augment":  ("augere-auctor", "aug（增长）+ -ment → 使之变大 → 增加"),
    "august":   ("augere-auctor", "augustus（尊崇的）← augere（增益）→ 分量增到令人仰视"),
    "account":  ("putare", "ac-（ad- 朝）+ count（算）→ 算给某处的那笔 → 账目、说明"),
    "achieve":  ("caput", "a-（到）+ chieve（caput 头）→ 做到头 → 达成"),
    "acrobat":  ("bainein", "akros（高处）+ bat（bainein 走）→ 在高处走的人"),
    "across":   ("crux", "a-（在）+ cross（十字、横过）→ 横过那一边"),
    "affair":   ("fac", "af-（ad- 去）+ fair（facere 做）→ 要去做的那件事"),
    "agitate":  ("ag", "ag（驱动）+ -itate（反复）→ 不停地驱动 → 搅动、鼓动"),
    "avenue":   ("venire-invent", "a-（ad- 朝）+ venue（venire 来）→ 走得近的那条路"),
    "bill":     ("bulla", "bulla（盖印文书）→ 开出来的那纸单据"),
    # 第二轮：第六十四批建了 haerere 与 jungere 之后重扫，又冒出这两个。
    # 这正是本脚本设计成可重复跑的原因——每建一批新根就该重扫一遍。
    "adhere":   ("haerere", "ad-（朝）+ here（黏住）→ 贴上去黏牢 → 附着、遵守"),
    "adjoin":   ("jungere", "ad-（朝）+ join（接合）→ 接到一处、彼此相连 → 毗连"),
}


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def as_list(o, k):
    return o if isinstance(o, list) else o.get(k, [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    wf = load("words.json")
    words = as_list(wf, "words")
    rootf = load("roots.json")
    roots = as_list(rootf, "roots")
    cf = load("concepts.json")
    concepts = as_list(cf, "concepts")
    rf = load("relations.json")
    rels = as_list(rf, "relations")

    rids = {r["id"] for r in roots}
    bad = [rid for _, (rid, _) in MOVE.items() if rid not in rids]
    if bad:
        print(f"[FAIL] 这些目标词根不存在：{sorted(set(bad))}")
        return 1

    wmap = {w["id"]: w for w in words}
    missing = [k for k in MOVE if k not in wmap]
    if missing:
        print(f"[FAIL] 这些词不在库中：{missing}")
        return 1

    done = []
    for wid, (rid, logic) in MOVE.items():
        w = wmap[wid]
        if w.get("decomposable") == "root" and rid in (w.get("root_ids") or []):
            continue                      # 已迁移过，幂等
        done.append(f"{wid}: germanic → root（{rid}）")
        if a.dry_run:
            continue
        w["decomposable"] = "root"
        w.pop("decomposable_note", None)  # root 型不写这个字段
        w["root_ids"] = [rid]
        w["root_logic"] = logic
        # 根与概念的 word_ids
        for r in roots:
            if r["id"] == rid and wid not in (r.get("word_ids") or []):
                r.setdefault("word_ids", []).append(wid)
                r["word_ids"].sort()
        for c in concepts:
            if rid in (c.get("root_ids") or []) and wid not in (c.get("word_ids") or []):
                c.setdefault("word_ids", []).append(wid)
                c["word_ids"].sort()
        # 词根 → 单词 的边
        if not any(r.get("from") == rid and r.get("to") == wid for r in rels):
            rels.append({"from": rid, "to": wid, "type": "root", "note": logic[:60]})

    for d in done:
        print("  ", d)
    print(f"\n{'（dry-run，未写入）' if a.dry_run else '已写入'} 共 {len(done)} 词")
    if a.dry_run or not done:
        return 0

    save("words.json", wf)
    save("roots.json", rootf)
    save("concepts.json", cf)
    save("relations.json", rf)

    # 自检
    words = as_list(load("words.json"), "words")
    roots = as_list(load("roots.json"), "roots")
    rids = {r["id"] for r in roots}
    wmap = {w["id"]: w for w in words}
    for wid, (rid, _) in MOVE.items():
        w = wmap[wid]
        assert w["decomposable"] == "root", f"{wid} 未改为 root 型"
        assert w["root_ids"] == [rid], f"{wid} 的 root_ids 不对：{w['root_ids']}"
        assert w.get("root_logic"), f"{wid} 缺 root_logic"
        assert "decomposable_note" not in w, f"{wid} 仍留着 decomposable_note"
    dang = {x for w in words for x in (w.get("root_ids") or []) if x not in rids}
    assert not dang, f"root_ids 悬空：{sorted(dang)}"
    loops = [r for r in as_list(load("relations.json"), "relations")
             if r.get("from") == r.get("to")]
    assert not loops, f"relations 自环：{[r['from'] for r in loops]}"
    print("   自检通过：均已改 root 型、无悬空 root_ids、无自环")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
