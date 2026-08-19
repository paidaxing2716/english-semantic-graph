#!/usr/bin/env python3
"""English Semantic Graph — 数据校验脚本

校验 data/*.json 的完整性：
- JSON 可解析
- id 唯一性
- 外键引用存在（root_ids / word_ids）
- 关系类型合法
- 必填字段非空
- Q7：related 指向词库内已存在词条（防死链）
- Q8：synonyms/antonyms 为词库词或白名单已核验真词（防 AI 造词）
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

VALID_RELATION_TYPES = {
    "root", "derived", "semantic_extension", "synonym", "antonym", "context"
}

REQUIRED_WORD_FIELDS = ["id", "word", "pos", "phonetic", "root_ids", "root_logic", "origin", "native_definition", "core_concept", "core_image", "chinese", "examples"]
REQUIRED_ROOT_FIELDS = ["id", "root", "origin", "core_concept", "core_image", "word_ids"]
REQUIRED_CONCEPT_FIELDS = ["id", "concept", "chinese", "core_image", "root_ids", "word_ids"]
REQUIRED_CLUSTER_FIELDS = ["id", "type", "concept", "chinese", "core_image", "word_ids"]


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
            if f not in w or w[f] in (None, ""):
                print(f"[FAIL] words 缺少必填字段 {f}: {w.get('id', '?')}")
                ok = False
            elif f == "root_ids" and not isinstance(w[f], list):
                print(f"[FAIL] words.{w['id']}.root_ids 必须是数组")
                ok = False
            elif f == "examples" and not isinstance(w[f], list):
                print(f"[FAIL] words.{w['id']}.examples 必须是数组")
                ok = False
            elif f == "phonetic" and not w[f].strip().startswith("/"):
                print(f"[FAIL] words.{w['id']}.phonetic 必须以 / 开头（IPA 格式）")
                ok = False
    for r in roots:
        for f in REQUIRED_ROOT_FIELDS:
            if f not in r or r[f] in (None, "", []):
                print(f"[FAIL] roots 缺少必填字段 {f}: {r.get('id', '?')}")
                ok = False
    for c in concepts:
        if c.get("type") == "cluster":
            for f in REQUIRED_CLUSTER_FIELDS:
                if f not in c or c[f] in (None, "", []):
                    print(f"[FAIL] cluster 概念缺少必填字段 {f}: {c.get('id', '?')}")
                    ok = False
            if not c.get("word_ids"):
                print(f"[FAIL] cluster 概念必须有组成员 (word_ids): {c.get('id', '?')}")
                ok = False
        else:
            for f in REQUIRED_CONCEPT_FIELDS:
                if f not in c or c[f] in (None, "", []):
                    print(f"[FAIL] concepts 缺少必填字段 {f}: {c.get('id', '?')}")
                    ok = False

    # --- synonym_group 引用校验（近义词组必须引用存在的 cluster 概念）---
    cluster_ids = {c["id"] for c in concepts if c.get("type") == "cluster"}
    for w in words:
        sg = w.get("synonym_group")
        if sg:
            if sg not in cluster_ids:
                print(f"[FAIL] words.{w['id']}.synonym_group 引用不存在的 cluster 概念: {sg}")
                ok = False
            # 反向：该 cluster 的 word_ids 应包含这个词
            cluster = next((c for c in concepts if c["id"] == sg), None)
            if cluster and w["id"] not in cluster.get("word_ids", []):
                print(f"[WARN] words.{w['id']} 声明 synonym_group={sg} 但 cluster 未收录它")
        # 反向检查：cluster 里的词应声明 synonym_group
        for c in concepts:
            if c.get("type") == "cluster" and w["id"] in c.get("word_ids", []) and not sg:
                print(f"[WARN] cluster {c['id']} 收录了 {w['id']} 但该词未声明 synonym_group")

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

    # --- Q7：related 必须指向词库内已存在的词条 ---
    # related 是图谱的边：指向不存在的词条会让详情面板出现点不开的死链。
    word_id_set = set(word_ids)
    dangling = []
    for w in words:
        for t in w.get("related") or []:
            if t not in word_id_set:
                dangling.append(f"{w['id']}.related -> {t}")
        if w["id"] in (w.get("related") or []):
            print(f"[FAIL] words.{w['id']}.related 自引用")
            ok = False
    if dangling:
        print(f"[FAIL] related 悬空引用 (Q7)，必须指向已存在词条: {len(dangling)} 条")
        for d in dangling:
            print(f"        {d}")
        ok = False
    else:
        print("[INFO] Q7 related 引用完整")

    # --- Q8：synonyms/antonyms 必须是词库内词条或白名单已核验的真词 ---
    # 防 AI 造词（如 configure 的反义写成不存在的 disconfigure）。
    lexicon = load("lexicon.json").get("external_words") or []
    allowed = word_id_set | set(lexicon)
    unvetted = []
    for w in words:
        for f in ("synonyms", "antonyms"):
            for t in w.get(f) or []:
                if t not in allowed:
                    unvetted.append(f"{w['id']}.{f} -> {t}")
    if unvetted:
        print(f"[FAIL] synonyms/antonyms 含未核验词 (Q8): {len(unvetted)} 条")
        for u in unvetted:
            print(f"        {u}")
        print("        → 人工确认该词真实存在后，加入 data/lexicon.json 的 external_words")
        ok = False
    else:
        print(f"[INFO] Q8 近/反义词全部已核验（白名单 {len(lexicon)} 词）")

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

    # --- 质量门 Q1：多义词解释覆盖 ---
    # 规则：
    # 1) 硬门槛：多义词（chinese ≥ 2）必须至少有 1 条 semantic_expansions，
    #    防止"只列义项不解释"的空心词条。
    # 2) 真实多义词（词义分叉，见 TRUE_POLYSEMY 名单）必须提供足够解释（≥ 2 条），
    #    确保"方面/感染/快递"这类独立引申义被解释。
    TRUE_POLYSEMY = {
        "figure", "express", "contract", "respect", "import",
        "mission", "prospect", "transcript", "produce", "transport",
        "subscribe", "expose", "position", "commit", "conduct",
    }
    no_exp = []
    weak_poly = []
    for w in words:
        n_meanings = len(w["chinese"])
        n_exps = len(w.get("semantic_expansions") or [])
        if n_meanings >= 2 and n_exps < 1:
            no_exp.append(w["word"])
        elif w["word"] in TRUE_POLYSEMY and n_exps < 2:
            weak_poly.append(w["word"])
    if no_exp:
        print(f"[FAIL] 多义词缺少语义解释 (Q1): {', '.join(no_exp)}")
        ok = False
    if weak_poly:
        print(f"[FAIL] 真实多义词解释不足 (Q1): {', '.join(weak_poly)}")
        ok = False
    if not no_exp and not weak_poly:
        print("[INFO] Q1 多义词覆盖通过")

    # --- 质量门 Q2：词源诚实性抽查 ---
    # root_logic 不得包含想当然的"XX 就是 XX"句式（简单化推导警示）
    suspicious = []
    for w in words:
        logic = w.get("root_logic") or ""
        if "就是" in logic and "间接" not in logic and "独立" not in logic:
            suspicious.append(w["word"])
    if suspicious:
        print(f"[WARN] root_logic 含'就是'式简单推导，请人工复核 (Q2): {', '.join(suspicious)}")
    else:
        print("[INFO] Q2 词源抽查通过")

    # --- 质量门 Q4：core_image 有效性 ---
    weak_images = []
    for w in words:
        img = w.get("core_image") or ""
        # 画面过短或纯概念复述判为弱
        if len(img) < 8 or img == w.get("core_concept", "")[:10]:
            weak_images.append(w["word"])
    if weak_images:
        print(f"[WARN] core_image 可能过弱 (Q4): {', '.join(weak_images)}")

    # --- 汇总 ---
    print(f"\n词根: {len(roots)} | 概念: {len(concepts)} | 单词: {len(words)} | 关系: {len(relations)} | 例句: {len(examples)}")
    if ok:
        print("\n[PASS] 全部校验通过 ✅")
        return 0
    print("\n[FAIL] 存在错误 ❌")
    return 1


if __name__ == "__main__":
    sys.exit(main())