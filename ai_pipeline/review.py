#!/usr/bin/env python3
"""审核候选词条：先查再并。

流程：候选 JSON → 结构与语言检查 → 人工确认 → 合并进 data/
合并前后都跑 tests/validate.py，任何一步不过就拒绝落库。

用法：
    python ai_pipeline/review.py check  candidates.json     # 只查不并
    python ai_pipeline/review.py merge  candidates.json     # 查过后合并
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

REQUIRED = ["id", "word", "pos", "phonetic", "root_ids", "root_logic", "origin",
            "native_definition", "core_concept", "core_image", "chinese", "examples"]
OPTIONAL = ["synonyms", "antonyms", "related", "semantic_expansions",
            "synonym_group", "synonym_note", "collocations", "level",
            "phrasal_verbs", "patterns"]
ALLOWED_FIELDS = set(REQUIRED) | set(OPTIONAL)
VALID_POS = {"noun", "verb", "adjective", "adverb", "adj", "adv", "preposition"}

# AI 造词的典型形态：前缀 + 已有词。命中且不在白名单里就要人工核。
SUSPECT_PREFIXES = ("dis", "un", "de", "in", "im", "non", "anti", "mis", "re", "over", "under")


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def check(candidates):
    """返回 (错误列表, 待人工确认列表)。错误必须修，确认项由人判断。"""
    words = load("words.json")["words"]
    roots = load("roots.json")["roots"]
    lexicon = set(load("lexicon.json").get("external_words") or [])

    existing = {w["id"] for w in words}
    root_ids = {r["id"] for r in roots}
    # 造词检测的比对基准要含本批次：AI 常在同一批里同时产出
    # 一个词和它不存在的反义词（disconfigure 模式）
    existing_words = {w["word"].lower() for w in words}
    existing_words |= {(c.get("word") or "").lower() for c in candidates if c.get("word")}

    errors = []
    review = []
    seen = set()
    # 候选之间也可能互相引用，一并视为"将存在"
    incoming = {c.get("id") for c in candidates if c.get("id")}
    known = existing | incoming

    for c in candidates:
        wid = c.get("id", "?")

        for f in REQUIRED:
            v = c.get(f)
            if f not in c or v in (None, "", []):
                errors.append(f"{wid}: 缺少必填字段 {f}")

        # 未知字段：模型幻觉出的字段不能静默入库
        for f in c:
            if f not in ALLOWED_FIELDS:
                errors.append(f"{wid}: 出现 schema 未定义的字段 {f!r}")

        if wid in existing:
            errors.append(f"{wid}: 词条已存在，不能重复入库")
        if wid in seen:
            errors.append(f"{wid}: 候选批次内 id 重复")
        seen.add(wid)

        if c.get("word", "").lower() != wid.lower():
            errors.append(f"{wid}: id 与 word 不一致（word={c.get('word')}）")

        ph = c.get("phonetic", "")
        if ph and not (ph.startswith("/") and ph.endswith("/")):
            errors.append(f"{wid}: phonetic 必须以 / 包裹，当前 {ph!r}")

        pos = (c.get("pos") or "").lower()
        if pos and pos not in VALID_POS:
            review.append(f"{wid}: pos={pos!r} 不在常用取值内，确认是否笔误")

        for rid in c.get("root_ids") or []:
            if rid not in root_ids:
                errors.append(f"{wid}: root_ids 引用不存在的词根 {rid}")

        # related 必须指向已存在或本批次的词条，否则图谱上是死链
        for t in c.get("related") or []:
            if t not in known:
                errors.append(f"{wid}: related 指向词库中不存在的 {t!r}（会产生死链）")

        # synonyms/antonyms：不在词库也不在白名单的一律拦下人工核
        for f in ("synonyms", "antonyms"):
            for t in c.get(f) or []:
                if t in existing or t in incoming or t in lexicon:
                    continue
                low = t.lower()
                fabricated = any(
                    low.startswith(p) and low[len(p):] in existing_words
                    for p in SUSPECT_PREFIXES
                )
                tag = "疑似造词" if fabricated else "未核验"
                review.append(
                    f"{wid}.{f}: {t!r} {tag}——确认是真实英语词后加入 data/lexicon.json"
                )

        # 多义词必须解释义项为何同源，不能只列不解释
        zh = c.get("chinese") or []
        exps = c.get("semantic_expansions") or []
        if len(zh) >= 2 and not exps:
            errors.append(f"{wid}: chinese 有 {len(zh)} 个义项但 semantic_expansions 为空 (Q1)")

        logic = c.get("root_logic") or ""
        if "就是" in logic and "间接" not in logic and "独立" not in logic:
            review.append(f"{wid}: root_logic 含'就是'式同义反复，确认推导是否成立 (Q2)")

        img = c.get("core_image") or ""
        if img and len(img) < 8:
            review.append(f"{wid}: core_image 偏短（{len(img)} 字），确认是否是具体画面")
        if img and img == (c.get("core_concept") or "")[:len(img)]:
            review.append(f"{wid}: core_image 疑似复述 core_concept")

        if not re.search(r"[A-Za-z]", " ".join(c.get("examples") or [])):
            errors.append(f"{wid}: examples 不含英文句子")

    return errors, review


def run_validate():
    r = subprocess.run([sys.executable, str(ROOT / "tests" / "validate.py")],
                       capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def merge(candidates):
    """合并进 data/：words.json + examples.json + relations.json + 词根反向引用。"""
    wf = load("words.json")
    ef = load("examples.json")
    rf = load("relations.json")
    rootf = load("roots.json")
    cf = load("concepts.json")

    for c in candidates:
        wf["words"].append(c)

        for i, text in enumerate(c.get("examples") or [], 1):
            ef["examples"].append({
                "id": f"ex-{c['id']}-{i}",
                "word_id": c["id"],
                "text": text,
                "source": "AI 生成 · 人工审核",
                "scene": c.get("core_image", "")[:40],
            })

        for rid in c.get("root_ids") or []:
            rf["relations"].append({
                "from": rid, "to": c["id"], "type": "root",
                "note": c.get("root_logic", "")[:60],
            })
            for r in rootf["roots"]:
                if r["id"] == rid and c["id"] not in r["word_ids"]:
                    r["word_ids"].append(c["id"])
            # 词根概念的反向引用：漏了新词就不会挂到概念节点下
            for con in cf["concepts"]:
                if con.get("type") == "cluster":
                    continue
                if rid in (con.get("root_ids") or []) and c["id"] not in con["word_ids"]:
                    con["word_ids"].append(c["id"])

    for name, obj in (("words.json", wf), ("examples.json", ef),
                      ("relations.json", rf), ("roots.json", rootf),
                      ("concepts.json", cf)):
        with open(DATA / name, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("check", "merge"):
        print(__doc__)
        return 2
    mode, path = sys.argv[1], Path(sys.argv[2])

    raw = json.loads(path.read_text(encoding="utf-8"))
    candidates = raw["words"] if isinstance(raw, dict) else raw
    print(f"候选词条 {len(candidates)} 条：{', '.join(c.get('id', '?') for c in candidates)}\n")

    errors, review = check(candidates)

    if errors:
        print(f"[FAIL] 结构错误 {len(errors)} 处，必须修正：")
        for e in errors:
            print(f"        {e}")
    else:
        print("[PASS] 结构检查通过")

    if review:
        print(f"\n[REVIEW] {len(review)} 项需人工确认：")
        for r in review:
            print(f"        {r}")
    else:
        print("[PASS] 无待确认项")

    if errors:
        print("\n[ABORT] 存在结构错误，未合并 ❌")
        return 1

    if mode == "check":
        print("\n[OK] 检查完毕（未合并）。确认无误后运行 merge。")
        return 0

    # 合并前先确认现有数据是干净的，否则分不清是谁引入的问题
    code, out = run_validate()
    if code != 0:
        print("\n[ABORT] 合并前 data/ 本身校验不通过，先修好再合并：")
        print(out[-600:])
        return 1

    merge(candidates)
    print(f"\n已合并 {len(candidates)} 条，重新校验：")
    code, out = run_validate()
    print(out[-700:])
    if code != 0:
        print("[FAIL] 合并后校验不通过，请 git checkout data/ 回滚 ❌")
        return 1
    print("[PASS] 合并完成 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
