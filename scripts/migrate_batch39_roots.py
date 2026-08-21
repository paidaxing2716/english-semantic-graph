#!/usr/bin/env python3
"""Migrate 7 mis-attached words to their correct roots (HANDOFF 二·五).

词源核查确认：
- concept/except/receipt/susceptible/accept ← capere（抓取），
  误挂 fac（facere 做），应改挂 cep
- invisible/advisable ← videre（看），误挂 spect（specere），
  应改挂 vid

修改文件：
- words.json：root_ids 改到新根（root_logic 本就写对了，不动）
- relations.json：删旧边，加新边
- concepts.json：从旧概念 word_ids 移除，加进新概念 word_ids
- 新根 cep/vid 的 word_ids 由 merge 已加过本批新词，这里补充迁移词
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

MOVE = {
    "cep": ["concept", "except", "receipt", "susceptible", "accept"],
    "vid": ["invisible", "advisable"],
}
# 每个迁移词原有的相关词（保持 related 不悬空，不动它们）
FROM_ROOT = {"cep": "fac", "vid": "spect"}

def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)

def save(name, obj):
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

words = load("words.json")
roots = load("roots.json")
concepts = load("concepts.json")
relations = load("relations.json")

# 1) words.json：root_ids 改挂
by_id = {w["id"]: w for w in words["words"]}
for new_root, wid_list in MOVE.items():
    for wid in wid_list:
        w = by_id.get(wid)
        if not w:
            print(f"  [skip] {wid} 不在库")
            continue
        old = w["root_ids"]
        w["root_ids"] = [new_root]
        print(f"  {wid}: roots {old} -> {[new_root]}")

# 2) relations.json：删旧边加新边
rel = relations["relations"]
moved_set = {wid for wids in MOVE.values() for wid in wids}
before = len(rel)
rel = [r for r in rel if not (r["to"] in moved_set and r["type"] == "root")]
for new_root, wid_list in MOVE.items():
    for wid in wid_list:
        if wid in moved_set:
            rel.append({"from": new_root, "to": wid, "type": "root",
                        "note": "词源修正迁移"})
relations["relations"] = rel
print(f"  relations: {before} -> {len(rel)}")

# 3) concepts.json：旧概念移除，新概念补充
for c in concepts["concepts"]:
    if c.get("type") == "cluster":
        continue
    # 从旧概念移除
    for old_root, wid_list in MOVE.items():
        pass
    # 若此概念含迁移词且其 root_ids 含旧根，则移除
    for wid in moved_set:
        if wid in c.get("word_ids", []):
            # 该词现在属于新根，若新根不在本概念 root_ids，则移除
            # 若新根在（理论上 merge 已建），移除旧引用
            c["word_ids"] = [x for x in c["word_ids"] if x != wid]
    # 补充进新根概念
for new_root, wid_list in MOVE.items():
    for c in concepts["concepts"]:
        if c.get("type") == "cluster":
            continue
        if new_root in (c.get("root_ids") or []):
            for wid in wid_list:
                if wid not in c["word_ids"]:
                    c["word_ids"].append(wid)

# 4) roots.json：新根 word_ids 补迁移词；旧根 word_ids 移除迁移词
moved_set2 = {wid for wids in MOVE.values() for wid in wids}
for r in roots["roots"]:
    for new_root, wid_list in MOVE.items():
        if r["id"] == new_root:
            for wid in wid_list:
                if wid not in r["word_ids"]:
                    r["word_ids"].append(wid)
    # 旧根移除（fac/spect 等有残留的分支）
    if r["id"] in FROM_ROOT.values():
        r["word_ids"] = [x for x in r["word_ids"] if x not in moved_set2]

save("words.json", words)
save("relations.json", relations)
save("concepts.json", concepts)
save("roots.json", roots)
print("迁移完成 ✅")
