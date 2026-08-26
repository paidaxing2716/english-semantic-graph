#!/usr/bin/env python3
"""修三条错挂：alternate / international / deliberate。

    python scripts/fix_misrooted_three.py --dry-run
    python scripts/fix_misrooted_three.py

三条都属「origin 自己写明了真实词源，归属却指向另一个同形或近形的根」，与本会话
早先修的 interference 同类。由全库扫描（scripts/audit_trap_pairs.py 思路）找出，
chunk56 的子代理此前已点出前两条。

1. international：ternus → nasci
   origin 写「inter-（之间）+ natio（国族）← nasci（出生）」。承载词义的是 natio，
   不是方位。ternus 是 externus/internus，核心概念「界线的里侧与外侧」，推不出
   「国际」。nasci 根已存在且 nation/national/nationality 都在里面。

2. alternate：ternus → 新根 alter-other
   origin 写「alternare ← alter（两者中的另一个）」，与里外无关。库中 alter /
   alternative / alternate 三词同族，够 3 个成员开根。
   **根 id 不能叫 alter**——会与单词 alter 撞名，前端 idMap 会让单词顶掉词根节点
   （本会话已因 minus 栽过一次）。按 dare-give / minus-less 的先例叫 alter-other。

3. deliberate：liber → 日耳曼型
   同形异源，最严重的一条：origin 明写「librare ← libra（天平）」，而 liber 是
   「自由的」。它的 root_logic 甚至打了补丁「此处取 libra 天平义」——那句话本身
   就是错挂的自白。libra（天平）族库中仅此一词，凑不到 3 个成员，不开根。
"""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

NEW_ROOT = {
    "id": "alter-other",
    "root": "alter",
    "variants": ["alter", "altern"],
    "origin": "拉丁语 alter（两者中的另一个）；alternare 表「在两者间来回换」",
    "core_concept": "the other one of two / 两个当中的那另一个",
    "core_image": "两只碗轮换着用，端起这只就放下那只，手上始终只有一只",
    "english_definition": "the other of two, every second one",
    "word_ids": ["alter", "alternate", "alternative"],
}

MOVE = {
    "international": ("nasci",
                      "inter-（之间）+ nation（← natio 国族，nasci 生出的一支族群）"
                      "→ 在生出来的各族之间往来的 → 国际的"),
    "alternate": ("alter-other",
                  "alter（两者中的另一个）+ -ate → 换到另一个上去，再换回来 → 交替"),
}
TO_GERMANIC = {
    "deliberate": "拉丁借词，本项目未为其词族建根，按整体记"
                  "（libra 天平一支库中仅此一词，且与 liber 自由不同源）",
}


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    words, roots = load("words.json"), load("roots.json")
    concepts, rels = load("concepts.json"), load("relations.json")
    wmap = {w["id"]: w for w in words["words"]}
    rmap = {r["id"]: r for r in roots["roots"]}
    done = []

    # 撞名红线：新根 id 不得与任何单词同名（两个方向都不行）
    if NEW_ROOT["id"] in wmap:
        print(f"[FAIL] 新根 id {NEW_ROOT['id']} 与单词同名")
        return 1
    for w in NEW_ROOT["word_ids"]:
        if w not in wmap:
            print(f"[FAIL] {w} 不在库中，无法作为 {NEW_ROOT['id']} 的成员")
            return 1

    if NEW_ROOT["id"] not in rmap:
        roots["roots"].append(NEW_ROOT)
        rmap[NEW_ROOT["id"]] = NEW_ROOT
        done.append(f"roots: 新建 {NEW_ROOT['id']}（{len(NEW_ROOT['word_ids'])} 成员）")

    for wid, (rid, logic) in MOVE.items():
        w = wmap.get(wid)
        if w is None:
            print(f"[FAIL] {wid} 不在库中")
            return 1
        old = (w.get("root_ids") or [None])[0]
        if old == rid:
            done.append(f"{wid}: 已是 {rid}，跳过")
            continue
        w["root_ids"] = [rid]
        w["root_logic"] = logic
        done.append(f"{wid}: {old} → {rid}")
        for r in roots["roots"]:
            ids = r.get("word_ids") or []
            if r["id"] == old and wid in ids:
                ids.remove(wid)
            if r["id"] == rid and wid not in ids:
                r.setdefault("word_ids", []).append(wid)
                r["word_ids"].sort()
        for c in concepts["concepts"]:
            cr = c.get("root_ids") or []
            ids = c.get("word_ids") or []
            if old in cr and wid in ids:
                ids.remove(wid)
            if rid in cr and wid not in ids:
                c.setdefault("word_ids", []).append(wid)
                c["word_ids"].sort()
        for r in rels["relations"]:
            if r.get("to") == wid and r.get("type") == "root":
                r["from"] = rid
                r["note"] = logic

    for wid, note in TO_GERMANIC.items():
        w = wmap.get(wid)
        old = (w.get("root_ids") or [None])[0]
        if not old:
            done.append(f"{wid}: 已是日耳曼型，跳过")
            continue
        w["root_ids"] = []
        w["root_logic"] = ""
        w["decomposable"] = "germanic"
        w["decomposable_note"] = note
        done.append(f"{wid}: {old} → 日耳曼型")
        for r in roots["roots"]:
            if r["id"] == old and wid in (r.get("word_ids") or []):
                r["word_ids"].remove(wid)
        for c in concepts["concepts"]:
            if wid in (c.get("word_ids") or []):
                c["word_ids"].remove(wid)
        before = len(rels["relations"])
        rels["relations"] = [x for x in rels["relations"]
                             if not (x.get("to") == wid and x.get("type") == "root")]
        if len(rels["relations"]) != before:
            done.append(f"  relations: 删 {before-len(rels['relations'])} 条边")

    # 新根需要一条概念与语义域归属，否则 validate 的 Q10 会挡
    for w in NEW_ROOT["word_ids"]:
        for r in rels["relations"]:
            if r.get("to") == w and r.get("type") == "root":
                r["from"] = NEW_ROOT["id"]
    for w in NEW_ROOT["word_ids"]:
        if not any(x.get("to") == w and x.get("type") == "root"
                   for x in rels["relations"]):
            rels["relations"].append({
                "from": NEW_ROOT["id"], "to": w, "type": "root",
                "note": f"{w} 出自 {NEW_ROOT['root']}"})
            done.append(f"relations: 补 {NEW_ROOT['id']} → {w}")

    for d in done:
        print("  " + d)
    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    for n, o in (("words.json", words), ("roots.json", roots),
                 ("concepts.json", concepts), ("relations.json", rels)):
        save(n, o)
    print(f"\n已写入 4 个文件，{len(done)} 处改动")
    print("提醒：新建了词根，还要给它归语义域（domains.json）与概念，"
          "跑 validate.py 看 Q10 是否通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
