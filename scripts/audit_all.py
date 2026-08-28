#!/usr/bin/env python3
"""全库静态质量审计，不修改 data/。

    python scripts/audit_all.py
    python scripts/audit_all.py --out audit

输出 critical.tsv、suspicious.tsv、duplicates.tsv、risk_rank.tsv、summary.json。
硬结构问题尽量复用 validate.py 的判据；内容检查只报线索，不自动改词条。
"""
import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VALID_POS = {"noun", "verb", "adjective", "adverb", "adj", "adv", "preposition", "conjunction", "pronoun", "interjection"}
TEMPLATE_EX = re.compile(r"^The (\w+) changed the situation\.\|Researchers discussed the \1 carefully\.$")
TEMPLATE_NATIVE = re.compile(r"^a thing or action related to \w+$")
TEMPLATE_IMAGE = "一张卡片放在桌面中央，旁边摆着几件相关物品，窗光从左侧照来"

def load(name, key):
    obj = json.loads((DATA / name).read_text(encoding="utf-8"))
    return obj[key] if isinstance(obj, dict) else obj

def tsv(path, rows):
    path.write_text("\n".join("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) for r in rows) + ("\n" if rows else ""), encoding="utf-8", newline="")

def add(bucket, word, field, claim, detail=""):
    bucket.append((word, field, claim, detail))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="audit")
    a = ap.parse_args()
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    words = load("words.json", "words")
    roots = load("roots.json", "roots")
    concepts = load("concepts.json", "concepts")
    relations = load("relations.json", "relations")
    domains = load("domains.json", "domains")
    critical, suspicious, dup = [], [], []
    word_ids = {w.get("id") for w in words}
    root_ids = {r.get("id") for r in roots}
    concept_ids = {c.get("id") for c in concepts}
    all_ids = word_ids | root_ids | concept_ids | {d.get("id") for d in domains}
    root_map = {r.get("id"): r for r in roots}
    word_map = {w.get("id"): w for w in words}
    concept_map = {c.get("id"): c for c in concepts}

    # 词条字段与内容硬检查
    for w in words:
        wid = w.get("id", "")
        if w.get("word") != wid:
            add(critical, wid, "word", "id != word", repr(w.get("word")))
        if not (str(w.get("phonetic", "")).startswith("/") and str(w.get("phonetic", "")).endswith("/")):
            add(suspicious, wid, "phonetic", "音标可能包含多读音或非标准格式", w.get("phonetic", ""))
        pos = [x.strip() for x in (w.get("pos") or "").lower().split("/") if x.strip()]
        if not pos or any(x not in VALID_POS for x in pos):
            add(critical, wid, "pos", "词性不在允许集合", w.get("pos", ""))
        ex = w.get("examples") or []
        if len(ex) < 2:
            add(critical, wid, "examples", "例句少于两条", str(len(ex)))
        elif len(ex) != 2:
            add(suspicious, wid, "examples", "例句不是正好两条（旧数据可能合法）", str(len(ex)))
        for i, sentence in enumerate(ex):
            if not isinstance(sentence, str) or not sentence.rstrip().endswith((".", "!", "?", "。", "！", "？")):
                add(critical, wid, f"examples[{i}]", "例句未以句号结束")
            if isinstance(sentence, str) and not (5 <= len(sentence.rstrip(".").split()) <= 20):
                add(suspicious, wid, f"examples[{i}]", "例句词数异常", str(len(sentence.rstrip(".").split())))
        zh = [x.strip() for x in (w.get("chinese") or []) if x.strip()]
        image = w.get("core_image") or ""
        for x in zh:
            if len(x) >= 2 and x in image:
                add(critical, wid, "core_image", "画面包含中文义项", x)
    # 例句模板不是「含有该词」就算问题；这里只报精确的通用模板。
        if TEMPLATE_EX.match("|".join(ex)):
            add(suspicious, wid, "examples", "疑似通用模板例句")
        if TEMPLATE_NATIVE.match(w.get("native_definition") or ""):
            add(suspicious, wid, "native_definition", "疑似通用模板释义")
        if image == TEMPLATE_IMAGE:
            add(suspicious, wid, "core_image", "疑似通用模板画面")
        if "clear scene connected with" in (w.get("core_concept") or ""):
            add(suspicious, wid, "core_concept", "疑似通用模板概念")
        if w.get("collocations"):
            for c in w["collocations"]:
                if "——" not in c:
                    add(critical, wid, "collocations", "搭配缺少 ——", c)
        if w.get("root_ids") and not (w.get("root_logic") or "").strip():
            add(critical, wid, "root_logic", "有词根但拆解逻辑为空")
        if not w.get("root_ids") and (w.get("root_logic") or "").strip():
            add(critical, wid, "root_logic", "无词根却有拆解逻辑")
        for rid in w.get("root_ids") or []:
            if rid not in root_ids:
                add(critical, wid, "root_ids", "引用不存在的词根", rid)
        if wid in root_ids:
            add(critical, wid, "id", "单词与词根 id 冲突")

    # 重复值：重复画面本身不一定错，统一放 duplicates/suspicious，不硬判错
    for field in ("core_image", "native_definition", "core_concept"):
        groups = collections.defaultdict(list)
        for w in words:
            v = (w.get(field) or "").strip()
            if v:
                groups[v].append(w["id"])
        for value, ids in groups.items():
            if len(ids) > 1:
                add(dup, "|".join(ids[:3]), field, f"重复 {len(ids)} 次", value)
    ex_groups = collections.defaultdict(list)
    for w in words:
        ex_groups["|".join(w.get("examples") or [])].append(w["id"])
    for value, ids in ex_groups.items():
        if value and len(ids) > 1:
            add(dup, "|".join(ids[:3]), "examples", f"整组例句重复 {len(ids)} 次", value)

    # 词根、概念、域、关系四向一致性
    for r in roots:
        rid = r.get("id", "")
        for wid in r.get("word_ids") or []:
            if wid not in word_ids:
                add(critical, rid, "word_ids", "词根引用不存在单词", wid)
            elif rid not in (word_map[wid].get("root_ids") or []):
                add(critical, rid, "word_ids", "词根→单词与单词→词根不一致", wid)
    for c in concepts:
        cid = c.get("id", "")
        for wid in c.get("word_ids") or []:
            if wid not in word_ids:
                add(critical, cid, "word_ids", "概念引用不存在单词", wid)
        for rid in c.get("root_ids") or []:
            if rid not in root_ids:
                add(critical, cid, "root_ids", "概念引用不存在词根", rid)
    rel_seen = set()
    for rel in relations:
        key = (rel.get("from"), rel.get("to"), rel.get("type"))
        if key in rel_seen:
            add(dup, str(key), "relations", "关系重复")
        rel_seen.add(key)
        if rel.get("from") not in all_ids or rel.get("to") not in all_ids:
            add(critical, str(key), "relations", "关系端点不存在")
    for d in domains:
        for rid in d.get("root_ids") or []:
            if rid not in root_ids:
                add(critical, d.get("id", ""), "root_ids", "语义域引用不存在词根", rid)

    # 风险排序：把异常密集、模板命中、词根型、抽象词排在前面。
    risk = collections.Counter()
    for word, field, claim, detail in critical + suspicious + dup:
        risk[word] += 10 if (word, field, claim, detail) in critical else 3
    for w in words:
        score = risk[w["id"]]
        if w.get("root_ids"): score += 1
        if len(w.get("chinese") or []) > 1: score += 1
        if any(x in (w.get("pos") or "") for x in ("adverb", "preposition", "conjunction")): score += 2
        if score:
            risk[w["id"]] = score
    rank = [(wid, score, "; ".join(f"{f}:{c}" for x, f, c, d in critical + suspicious + dup if x == wid)[:500]) for wid, score in risk.most_common()]

    tsv(out / "critical.tsv", critical)
    tsv(out / "suspicious.tsv", suspicious)
    tsv(out / "duplicates.tsv", dup)
    tsv(out / "risk_rank.tsv", rank)
    summary = {"words": len(words), "roots": len(roots), "concepts": len(concepts), "relations": len(relations),
               "critical": len(critical), "suspicious": len(suspicious), "duplicates": len(dup), "risk_words": len(rank)}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if critical else 0

if __name__ == "__main__":
    raise SystemExit(main())
