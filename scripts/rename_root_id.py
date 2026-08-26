#!/usr/bin/env python3
"""给词根改 id，四处同步。用于解决「词根 id 与单词同名」的撞名。

    python scripts/rename_root_id.py minus minus-less --dry-run
    python scripts/rename_root_id.py minus minus-less

【为什么需要】词根 id 与单词 id 共用一个键空间（frontend 的 idMap 装域/根/
概念/单词），同名时单词后插入会把词根节点顶掉，成员词全连到错误类型的节点上。
每道门都绿，只有画面上看得出来。命名先例：dare→dare-give、humor→humor-moist、
ter→ter-comparative。

【只按字段改，不做全文替换】roots.json 的 origin、words.json 的 root_logic 等
散文字段里会正当地提到别的词（dominate/dominant 的文本就含 'minus'），全文
替换会改坏它们。本脚本只动这些位置：
  roots[].id / root / variants   （variants 保持英文词干不变，只在等于旧 id 时改）
  words[].root_ids[]
  concepts[].root_ids[]
  relations[].from / .to  （type == root 的边）
  domains[].root_ids[]    ← 第五处，别漏。漏了 validate.py 会报
                            「domain-shape.root_ids 引用不存在的词根」+ Q10
                            「词根未归入任何语义域」，实测栽过一次。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(
        json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    old, new = a.old, a.new

    words, roots = load("words.json"), load("roots.json")
    concepts, rels = load("concepts.json"), load("relations.json")
    domains = load("domains.json")
    done = []

    rids = {r["id"] for r in roots["roots"]}
    if old not in rids:
        print(f"[FAIL] 词根 {old} 不存在")
        return 1
    if new in rids:
        print(f"[FAIL] 词根 {new} 已存在，会合并两个根")
        return 1
    if new in {w["id"] for w in words["words"]}:
        print(f"[FAIL] 新 id {new} 与单词同名，等于没解决撞名")
        return 1

    for r in roots["roots"]:
        if r["id"] == old:
            r["id"] = new
            done.append(f"roots: id {old} → {new}")
            # root 字段是展示用的拉丁词形，variants 是英文词干，都不该跟着改；
            # 但若其中恰好等于旧 id 才需同步（此处保留原值，仅报告）
            done.append(f"  （root={r.get('root')!r} variants={r.get('variants')} 保持不变）")

    n = 0
    for w in words["words"]:
        ids = w.get("root_ids") or []
        if old in ids:
            w["root_ids"] = [new if x == old else x for x in ids]
            n += 1
    if n:
        done.append(f"words: {n} 个词的 root_ids 改指向")

    n = 0
    for c in concepts["concepts"]:
        ids = c.get("root_ids") or []
        if old in ids:
            c["root_ids"] = [new if x == old else x for x in ids]
            n += 1
    if n:
        done.append(f"concepts: {n} 个概念的 root_ids 改指向")

    n = 0
    for r in rels["relations"]:
        for k in ("from", "to"):
            if r.get(k) == old:
                r[k] = new
                n += 1
    if n:
        done.append(f"relations: {n} 处端点改指向")

    n = 0
    for d in (domains["domains"] if isinstance(domains, dict) else domains):
        ids = d.get("root_ids") or []
        if old in ids:
            d["root_ids"] = [new if x == old else x for x in ids]
            n += 1
    if n:
        done.append(f"domains: {n} 个语义域的 root_ids 改指向")

    for d in done:
        print("  " + d)
    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    for name, o in (("words.json", words), ("roots.json", roots),
                    ("concepts.json", concepts), ("relations.json", rels),
                    ("domains.json", domains)):
        save(name, o)
    print("\n已写入 5 个文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
