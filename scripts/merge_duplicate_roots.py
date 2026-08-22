#!/usr/bin/env python3
"""合并重复词根：structus → stru（两者同出拉丁 struere，是我建族时漏查造成的重复）。

用法：
    python scripts/merge_duplicate_roots.py --dry-run
    python scripts/merge_duplicate_roots.py

【背景】
data/roots.json 里 stru 与 structus 的 origin 都写拉丁语 struere（堆叠、建造）：
    stru      早有 structure/construct/destructive/instruct/instrument/instrumental
    structus  第四十三批新建，挂 construction/destruction/instruction
同一个词源在图谱里裂成两个节点，正是本项目要消除的东西。concept 也重了一份
（concept-stru-build 与 concept-structus-build，画面都是「砖一层层垒起」）。

【只改词根那一端】
relations 里 type=root 的关系是「词根 → 单词」，to 存的是**单词 id**。
上一轮迁移就是因为顺手把 to 也改了，造出 forma → forma 自环。
故此处只改 from/source，并在自检里断言无自环。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# 死根 -> 活根
MERGE = {"structus": "stru"}
# 死概念 -> 活概念
MERGE_CONCEPT = {"concept-structus-build": "concept-stru-build"}


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
    log = []

    # 1) roots.json —— 变体并入活根，删掉死根
    o = load("roots.json")
    roots = as_list(o, "roots")
    idx = {r["id"]: r for r in roots}
    for dead, alive in MERGE.items():
        if dead not in idx or alive not in idx:
            continue
        av = idx[alive].setdefault("variants", [])
        low = {v.lower() for v in av}
        add = [v for v in (idx[dead].get("variants") or []) if v.lower() not in low]
        if add:
            log.append(f"roots.json: {alive}.variants += {add}")
            if not a.dry_run:
                av.extend(add)
        log.append(f"roots.json: 删除重复词根 {dead}")
    if not a.dry_run:
        keep = [r for r in roots if r["id"] not in MERGE]
        if isinstance(o, list):
            o = keep
        else:
            o["roots"] = keep
        save("roots.json", o)

    # 2) words.json —— root_ids 改挂活根
    o = load("words.json")
    n = 0
    for w in as_list(o, "words"):
        rs = w.get("root_ids") or []
        new = [MERGE.get(x, x) for x in rs]
        seen, ded = set(), []
        for x in new:
            if x not in seen:
                seen.add(x)
                ded.append(x)
        if ded != rs:
            n += 1
            if not a.dry_run:
                w["root_ids"] = ded
    log.append(f"words.json: {n} 词改挂")
    if not a.dry_run:
        save("words.json", o)

    # 3) concepts.json —— word_ids 并入活概念，删掉死概念
    o = load("concepts.json")
    cs = as_list(o, "concepts")
    cidx = {c["id"]: c for c in cs}
    for dead, alive in MERGE_CONCEPT.items():
        if dead not in cidx or alive not in cidx:
            continue
        tgt = cidx[alive].setdefault("word_ids", [])
        add = [w for w in (cidx[dead].get("word_ids") or []) if w not in tgt]
        log.append(f"concepts.json: {alive}.word_ids += {add}；删除 {dead}")
        if not a.dry_run:
            tgt.extend(add)
            tgt.sort()
    for c in cs:
        rs = c.get("root_ids") or []
        new = [MERGE.get(x, x) for x in rs]
        if new != rs and not a.dry_run:
            c["root_ids"] = sorted(set(new))
    if not a.dry_run:
        keep = [c for c in cs if c["id"] not in MERGE_CONCEPT]
        if isinstance(o, list):
            o = keep
        else:
            o["concepts"] = keep
        save("concepts.json", o)

    # 4) domains.json —— 去掉死根与死概念
    o = load("domains.json")
    for d in as_list(o, "domains"):
        for f in ("root_ids", "roots"):
            v = d.get(f)
            if isinstance(v, list):
                new = []
                for x in v:
                    x = MERGE.get(x, x)
                    if x not in new:
                        new.append(x)
                if new != v:
                    log.append(f"domains.json: {d['id']}.{f} 去重 {v} → {new}")
                    if not a.dry_run:
                        d[f] = new
        cv = d.get("concept_ids")
        if isinstance(cv, list):
            new = [c for c in cv if c not in MERGE_CONCEPT]
            if new != cv:
                log.append(f"domains.json: {d['id']}.concept_ids 删死概念")
                if not a.dry_run:
                    d["concept_ids"] = new
    if not a.dry_run:
        save("domains.json", o)

    # 5) relations.json —— 只改词根那一端
    o = load("relations.json")
    n = 0
    for r in as_list(o, "relations"):
        for f in ("from", "source"):
            if r.get(f) in MERGE:
                if not a.dry_run:
                    r[f] = MERGE[r[f]]
                n += 1
    log.append(f"relations.json: {n} 处词根端改写（to 端不动，那是单词 id）")
    if not a.dry_run:
        save("relations.json", o)

    for x in log:
        print("  ", x)
    print(f"\n{'（dry-run，未写入）' if a.dry_run else '已写入'}")

    if a.dry_run:
        return 0

    # 自检
    roots = as_list(load("roots.json"), "roots")
    words = as_list(load("words.json"), "words")
    cs = as_list(load("concepts.json"), "concepts")
    rids = {r["id"] for r in roots}
    wids = {w["id"] for w in words}
    assert not (rids & set(MERGE)), "旧词根 id 仍残留"
    assert not (rids & wids), f"词根/单词同名：{sorted(rids & wids)}"
    dang = {x for w in words for x in (w.get("root_ids") or []) if x not in rids}
    assert not dang, f"words.root_ids 悬空：{sorted(dang)}"
    dang = {x for c in cs for x in (c.get("root_ids") or []) if x not in rids}
    assert not dang, f"concepts.root_ids 悬空：{sorted(dang)}"
    loops = [r for r in as_list(load("relations.json"), "relations")
             if r.get("from") == r.get("to")]
    assert not loops, f"relations 自环：{[r['from'] for r in loops]}"
    print("   自检通过：无残留、无同名、无悬空、无自环")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
