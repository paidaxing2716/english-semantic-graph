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
TEMPLATE_NATIVE_2 = "relating to the meaning described by the word"
# 两代批量生成器各用过一个固定画面串。只留一个会让另一代恒不报——08-28 的报告
# 就因为常量还是第一代的串，89 条第二代模板画面一条没报出来。
TEMPLATE_IMAGES = (
    "一张卡片放在桌面中央，旁边摆着几件相关物品，窗光从左侧照来",
    "木桌上摆着一件物品，旁边留着一条空白路径，窗光从左侧照来",
)
TEMPLATE_CONCEPT_SUB = "clear scene connected with"
TEMPLATE_CONCEPT_2 = "a clear situation associated with the word – 与词义相连的清晰场景"
TEMPLATE_SEM_SUB = "从核心场景引出的常用义"
ASCII_WORD = re.compile(r"^[a-zA-Z][a-zA-Z\s'-]*$")
# 英语 IPA 里不会出现的正字法特征。用来区分「拼写冒充音标」与碰巧同形的真音标
# （/net/ /help/ /bed/ 都是合法 IPA，不能因为等于拼写就判假）。
NON_IPA_SPELLING = re.compile(r"[cqxy]|sh|ch|th|ph|wh|ck|oo|ee|ea|ou|ay|ai|oa|igh|ss|ll|tt|pp|mm|nn|gg|ff|dd|bb|rr")


def is_template_native(value):
    v = (value or "").strip()
    return bool(TEMPLATE_NATIVE.match(v)) or v == TEMPLATE_NATIVE_2


def is_template_concept(value):
    v = (value or "").strip()
    return TEMPLATE_CONCEPT_SUB in v or v == TEMPLATE_CONCEPT_2


def is_stub(w):
    """批量生成器留下的占位词条：模板例句与模板释义同时命中才算。

    只命中一项不算——真实词条可能撞上通用释义，也可能例句偶然同形。两项同时
    命中是 build_g_chunk* 那个生成器的签名，实测 1134 条，与手工核对一致。
    """
    ex = [str(x) for x in (w.get("examples") or [])]
    return bool(ex) and bool(TEMPLATE_EX.match("|".join(ex))) and is_template_native(w.get("native_definition"))

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
        if is_template_native(w.get("native_definition")):
            add(suspicious, wid, "native_definition", "疑似通用模板释义")
        if image in TEMPLATE_IMAGES:
            add(suspicious, wid, "core_image", "疑似通用模板画面")
        if is_template_concept(w.get("core_concept")):
            add(suspicious, wid, "core_concept", "疑似通用模板概念")
        se = [str(x) for x in (w.get("semantic_expansions") or [])]
        if se and all(TEMPLATE_SEM_SUB in x for x in se):
            add(suspicious, wid, "semantic_expansions", "疑似通用模板语义展开")
        # 假音标：生成器写的是 '/ˈ'+word+'/'。分两级——精确签名零假阳性；无重音符的
        # /word/ 变体要靠正字法排除，因为 /net/ /help/ /bed/ 这类是合法 IPA。
        ph = str(w.get("phonetic") or "").strip()
        bare = ph.strip("/")
        if ph == "/ˈ" + wid + "/":
            # 这条判据不是零假阳性：self 的真 IPA 恰好就是 /ˈself/，与生成器格式撞车。
            # 单音节且拼写等于音位串的词都有这个风险（net/bed/help 那类因无重音符躲过）。
            # 报出来仍是对的——无法从值本身区分，人核一眼即可。
            add(suspicious, wid, "phonetic", "音标是拼写套斜杠（生成器签名）", ph)
        elif bare == wid and NON_IPA_SPELLING.search(wid):
            add(suspicious, wid, "phonetic", "音标含 IPA 不可能的正字法，疑似拼写冒充", ph)
        # 中文义项全是 ASCII 词：生成器 zh.get(w, w) 的静默回退，等于没有中文释义。
        if zh and all(ASCII_WORD.match(x) for x in zh):
            add(suspicious, wid, "chinese", "中文义项是英文词，疑似生成器回退", "/".join(zh)[:60])
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
    # 占位词条单独成表，不进 risk_rank——它们每条稳定命中六七项模板判据，混进来会把
    # 5248 词里的 5174 词都染成「有风险」，排序就丧失筛选力（08-28 报告即如此）。
    # 它们缺什么是已知的，要的是逐词补内容，不是再排一次序。
    stub_ids = {w["id"] for w in words if is_stub(w)}
    critical_keys = {(x[0], x[1], x[2], x[3]) for x in critical}
    risk = collections.Counter()
    for word, field, claim, detail in critical + suspicious + dup:
        if word in stub_ids:
            continue
        risk[word] += 10 if (word, field, claim, detail) in critical_keys else 3
    # 加权只在「已有报警」的词之间分次序。此前对全库无条件加权，于是有词根或多义的
    # 词凭静态属性就得 1-2 分进榜，3516 条报警栏全空——榜单等于把库抄了一遍。
    for w in words:
        if w["id"] in stub_ids or not risk[w["id"]]:
            continue
        score = risk[w["id"]]
        if w.get("root_ids"): score += 1
        if len(w.get("chinese") or []) > 1: score += 1
        if any(x in (w.get("pos") or "") for x in ("adverb", "preposition", "conjunction")): score += 2
        risk[w["id"]] = score
    detail_by_word = collections.defaultdict(list)
    for x, f, c, d in critical + suspicious + dup:
        detail_by_word[x].append(f"{f}:{c}")
    # 只保留真实词条 id：dup 的键是 "a|b|c" 复合串，混进排序会虚增风险词数。
    # score > 0 是必须的：Counter 读取会把键建出来并置 0，否则那些词会跟着进榜。
    rank = [(wid, score, "; ".join(detail_by_word[wid])[:500])
            for wid, score in risk.most_common() if wid in word_ids and score > 0]
    stub_rows = [(w["id"], w.get("pos") or "", "占位词条：模板例句＋模板释义",
                  "画面已补" if (w.get("core_image") or "").strip() not in TEMPLATE_IMAGES else "画面仍为模板")
                 for w in words if w["id"] in stub_ids]

    tsv(out / "critical.tsv", critical)
    tsv(out / "suspicious.tsv", suspicious)
    tsv(out / "duplicates.tsv", dup)
    tsv(out / "risk_rank.tsv", rank)
    tsv(out / "stubs.tsv", stub_rows)
    usable = len(words) - len(stub_ids)
    summary = {"words": len(words), "usable": usable, "stubs": len(stub_ids),
               "roots": len(roots), "concepts": len(concepts), "relations": len(relations),
               "critical": len(critical), "suspicious": len(suspicious), "duplicates": len(dup),
               "risk_words": len(rank)}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if critical else 0

if __name__ == "__main__":
    raise SystemExit(main())
