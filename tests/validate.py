#!/usr/bin/env python3
"""English Semantic Graph — 数据校验脚本

校验 data/*.json 的完整性：
- JSON 可解析
- id 唯一性
- 外键引用存在（root_ids / word_ids）
- 关系类型合法
- 必填字段非空
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

VALID_RELATION_TYPES = {
    "root", "derived", "semantic_extension", "synonym", "antonym", "context"
}

REQUIRED_WORD_FIELDS = ["id", "word", "root_ids", "native_definition", "core_concept"]
REQUIRED_ROOT_FIELDS = ["id", "root", "origin", "core_concept", "core_image", "word_ids"]
REQUIRED_CONCEPT_FIELDS = ["id", "concept", "chinese", "core_image", "root_ids", "word_ids"]


def load(name):
    path = DATA / name
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[FAIL] 找不到文件: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[FAIL] JSON 解析失败 {name}: {e}")
        sys.exit(1)


def check_unique(ids, label):
    dupes = [x for x in set(ids) if ids.count(x) > 1]
    if dupes:
        print(f"[FAIL] {label} 存在重复 id: {dupes}")
        return False
    return True


def main():
    ok = True

    roots = load("roots.json")["roots"]
    concepts = load("concepts.json")["concepts"]
    words = load("words.json")["words"]
    relations = load("relations.json")["relations"]
    examples = load("examples.json")["examples"]

    # --- id 唯一性 ---
    root_ids = [r["id"] for r in roots]
    concept_ids = [c["id"] for c in concepts]
    word_ids = [w["id"] for w in words]

    ok &= check_unique(root_ids, "roots")
    ok &= check_unique(concept_ids, "concepts")
    ok &= check_unique(word_ids, "words")

    all_ids = set(root_ids) | set(concept_ids) | set(word_ids)

    # --- 必填字段 ---
    for w in words:
        for f in REQUIRED_WORD_FIELDS:
            if f not in w or w[f] in (None, "", []):
                print(f"[FAIL] words 缺少必填字段 {f}: {w.get('id', '?')}")
                ok = False
    for r in roots:
        for f in REQUIRED_ROOT_FIELDS:
            if f not in r or r[f] in (None, "", []):
                print(f"[FAIL] roots 缺少必填字段 {f}: {r.get('id', '?')}")
                ok = False
    for c in concepts:
        for f in REQUIRED_CONCEPT_FIELDS:
            if f not in c or c[f] in (None, "", []):
                print(f"[FAIL] concepts 缺少必填字段 {f}: {c.get('id', '?')}")
                ok = False

    # --- 外键引用 ---
    # words.root_ids 引用 roots
    for w in words:
        for rid in w["root_ids"]:
            if rid not in root_ids:
                print(f"[FAIL] words.{w['id']}.root_ids 引用不存在的词根: {rid}")
                ok = False
    # roots.word_ids 引用 words
    for r in roots:
        for wid in r["word_ids"]:
            if wid not in word_ids:
                print(f"[FAIL] roots.{r['id']}.word_ids 引用不存在的单词: {wid}")
                ok = False
    # concepts.root_ids / word_ids
    for c in concepts:
        for rid in c["root_ids"]:
            if rid not in root_ids:
                print(f"[FAIL] concepts.{c['id']}.root_ids 引用不存在的词根: {rid}")
                ok = False
        for wid in c["word_ids"]:
            if wid not in word_ids:
                print(f"[FAIL] concepts.{c['id']}.word_ids 引用不存在的单词: {wid}")
                ok = False

    # --- 关系类型 & 端点 ---
    for rel in relations:
        if rel["type"] not in VALID_RELATION_TYPES:
            print(f"[FAIL] relations 非法类型: {rel.get('from')} -> {rel.get('to')}: {rel['type']}")
            ok = False
        if rel["from"] not in all_ids:
            print(f"[FAIL] relations.from 不存在: {rel['from']}")
            ok = False
        if rel["to"] not in all_ids:
            print(f"[FAIL] relations.to 不存在: {rel['to']}")
            ok = False
        if rel["from"] == rel["to"]:
            print(f"[FAIL] relations 自环: {rel['from']}")
            ok = False

    # --- 例句引用单词 ---
    for ex in examples:
        if ex["word_id"] not in word_ids:
            print(f"[FAIL] examples.{ex['id']}.word_id 引用不存在的单词: {ex['word_id']}")
            ok = False

    # --- 汇总 ---
    print(f"\n词根: {len(roots)} | 概念: {len(concepts)} | 单词: {len(words)} | 关系: {len(relations)} | 例句: {len(examples)}")
    if ok:
        print("\n[PASS] 全部校验通过 ✅")
        return 0
    print("\n[FAIL] 存在错误 ❌")
    return 1


if __name__ == "__main__":
    sys.exit(main())