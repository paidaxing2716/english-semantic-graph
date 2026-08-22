#!/usr/bin/env python3
"""审核候选词条：先查再并。

流程：候选 JSON → 结构与语言检查 → 人工确认 → 合并进 data/
合并后跑 tests/validate.py，不过就拒绝落库。

批次文件可以同时声明新的词根 / 概念 / 语义域，与词条一起原子落地：

    {
      "roots":    [{"id":"tend", "root":"tend", ...}],      // word_ids 自动填
      "concepts": [{"id":"concept-tend-stretch", ...}],     // word_ids 自动填
      "domains":  [{"id":"domain-x", ..., "root_ids":[...]}],
      "domain_add": {"domain-force": ["tend"]},             // 往现有域追加词根
      "words":    [ ... ]
    }

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

REQUIRED = ["id", "word", "pos", "phonetic", "origin",
            "native_definition", "core_concept", "core_image", "chinese", "examples"]
# 只对 root 型必填——日耳曼词、借词没有词根推导可写
ROOT_ONLY = ["root_ids", "root_logic"]
OPTIONAL = ["synonyms", "antonyms", "related", "semantic_expansions",
            "synonym_group", "synonym_note", "collocations", "level",
            "phrasal_verbs", "patterns", "decomposable", "decomposable_note",
            "recall_hint"]
ALLOWED_FIELDS = set(REQUIRED) | set(OPTIONAL) | set(ROOT_ONLY)

VALID_DECOMP = {"root", "root_pending", "germanic", "loanword", "phrasal", "opaque"}
# 与 tests/validate.py 的 Q11 保持一致：只收谈论词源关系的对冲措辞，
# 不收描述词义的词（否则 abduct 的"强行带走"会被误判）
HEDGES = ["词源不同", "并非同源", "不同源", "无直接关系", "非同一词根",
          "此处按", "硬凑", "牵强附会", "严格来说无关"]
# 加 conjunction / pronoun：第五十四批起收日耳曼核心词，其中 although 是连词、
# anybody/anyone 是代词。旧表没有这两项，逼得只能标成最近似的 noun，那是事实错误。
VALID_POS = {"noun", "verb", "adjective", "adverb", "adj", "adv", "preposition",
             "conjunction", "pronoun"}

# AI 造词的典型形态：前缀 + 已有词。命中且不在白名单里就要人工核。
SUSPECT_PREFIXES = ("dis", "un", "de", "in", "im", "non", "anti", "mis", "re", "over", "under")


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def _today():
    from datetime import date
    return date.today().isoformat()


def load_reference():
    """参考词表：词形出现在其中即可自动认定为真实英语词。

    目的是免掉"逐个确认常见词"的重复劳动——每批原本有十几项都是
    enough / result / fault 这类明显真词，只有表外的才值得人工过目。
    文件缺失时退化为全部人工确认，不报错。
    """
    p = DATA / "english_reference.json"
    if not p.exists():
        return set()
    try:
        with open(p, encoding="utf-8") as f:
            return {w.lower() for w in json.load(f).get("words") or []}
    except (json.JSONDecodeError, OSError):
        print("[WARN] english_reference.json 读取失败，本次全部转人工确认")
        return set()


def check(candidates, decl=None):
    """返回 (错误列表, 待人工确认列表)。错误必须修，确认项由人判断。

    decl 是批次里声明的新词根/概念/域；它们尚未入库但本批可以引用。
    """
    decl = decl or {}
    words = load("words.json")["words"]
    roots = load("roots.json")["roots"]
    lexicon = set(load("lexicon.json").get("external_words") or [])
    reference = load_reference()

    existing = {w["id"] for w in words}
    # 本批声明的新词根视为"将存在"，否则每次新建词根都要先手写脚本插进去
    root_ids = {r["id"] for r in roots} | {r["id"] for r in decl.get("roots") or []}
    # 造词检测的比对基准要含本批次：AI 常在同一批里同时产出
    # 一个词和它不存在的反义词（disconfigure 模式）
    existing_words = {w["word"].lower() for w in words}
    existing_words |= {(c.get("word") or "").lower() for c in candidates if c.get("word")}

    errors = []
    review = []
    auto_ok = set()      # 由参考词表自动核验通过的外部词
    seen = set()
    # 候选之间也可能互相引用，一并视为"将存在"
    incoming = {c.get("id") for c in candidates if c.get("id")}
    known = existing | incoming

    for c in candidates:
        wid = c.get("id", "?")

        need = list(REQUIRED)
        # decomposable 缺失时只报缺这个字段，不再连带抱怨缺词根字段——
        # 主错误是没声明可拆性，词根该不该有取决于它
        if c.get("decomposable") == "root":
            need += ROOT_ONLY
        for f in need:
            v = c.get(f)
            if f not in c or v in (None, "", []):
                errors.append(f"{wid}: 缺少必填字段 {f}")

        # 未知字段：模型幻觉出的字段不能静默入库
        for f in c:
            if f not in ALLOWED_FIELDS:
                errors.append(f"{wid}: 出现 schema 未定义的字段 {f!r}")

        if wid in existing:
            errors.append(f"{wid}: 词条已存在，不能重复入库")
        # 词根与词条共用同一 id 命名空间（关系图的端点都从这里取），
        # 同名会让"词根→该词"这条边变成自环。词根应改用拉丁词形。
        if wid in root_ids:
            errors.append(f"{wid}: 与词根同名，会产生自环边——"
                          f"把词根 id 改成拉丁词形（如 part → pars）")
        if wid in seen:
            errors.append(f"{wid}: 候选批次内 id 重复")
        seen.add(wid)

        if c.get("word", "").lower() != wid.lower():
            errors.append(f"{wid}: id 与 word 不一致（word={c.get('word')}）")

        ph = c.get("phonetic", "")
        if ph and not (ph.startswith("/") and ph.endswith("/")):
            errors.append(f"{wid}: phonetic 必须以 / 包裹，当前 {ph!r}")

        # 双词性用斜杠写，如 'noun / verb'——库里早有此约定（noun / verb 26 例、
        # verb / noun 19 例）。旧实现拿整串去平集匹配，认不出斜杠形式，
        # 于是每批刷出几十条假警告，把真问题盖掉。故拆开逐项校验。
        pos = (c.get("pos") or "").lower()
        pos_parts = [p.strip() for p in pos.split("/") if p.strip()]
        if pos and not all(p in VALID_POS for p in pos_parts):
            review.append(f"{wid}: pos={pos!r} 不在常用取值内，确认是否笔误")

        for rid in c.get("root_ids") or []:
            if rid not in root_ids:
                errors.append(f"{wid}: root_ids 引用不存在的词根 {rid}")

        # 可拆性：不可拆的词不得硬编词根（撤掉 seclude 那次就是这个形态）
        dec = c.get("decomposable")
        logic = (c.get("root_logic") or "").strip()
        if dec is None:
            errors.append(f"{wid}: 缺少 decomposable 字段（词源对不上就标 germanic/"
                          f"loanword/opaque，不要硬编词根）")
        elif dec not in VALID_DECOMP:
            errors.append(f"{wid}: decomposable 取值非法 {dec!r}，"
                          f"应为 {'/'.join(sorted(VALID_DECOMP))}")
        elif dec == "root":
            if not c.get("root_ids"):
                errors.append(f"{wid}: 标为 root 型但 root_ids 为空"
                              f"（词根未建模则标 root_pending）")
            hit = [h for h in HEDGES if h in logic]
            if hit:
                errors.append(f"{wid}: root_logic 含承认词源不成立的措辞 {hit}，"
                              f"却仍挂词根——改标 decomposable，不要硬编推导")
        else:
            if c.get("root_ids"):
                errors.append(f"{wid}: 标为 {dec} 型（不可拆）却挂了词根 {c['root_ids']}")
            if logic:
                errors.append(f"{wid}: 标为 {dec} 型（不可拆）却写了 root_logic")

        # related 必须指向已存在或本批次的词条，否则图谱上是死链
        for t in c.get("related") or []:
            if t not in known:
                errors.append(f"{wid}: related 指向词库中不存在的 {t!r}（会产生死链）")

        # synonyms/antonyms：不在词库、白名单、参考词表里的才转人工
        for f in ("synonyms", "antonyms"):
            for t in c.get(f) or []:
                low = t.lower()
                if t in existing or t in incoming or t in lexicon:
                    continue
                fabricated = any(
                    low.startswith(p) and low[len(p):] in existing_words
                    for p in SUSPECT_PREFIXES
                )
                # 参考词表能证明它是真词就自动过；但疑似造词仍要人看，
                # 因为"前缀+真词"也可能恰好撞进词表（如 inform vs *infirm）
                if low in reference and not fabricated:
                    auto_ok.add(t)
                    continue
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

    return errors, review, sorted(auto_ok)


def run_validate():
    r = subprocess.run([sys.executable, str(ROOT / "tests" / "validate.py")],
                       capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def merge(candidates, decl=None):
    """合并进 data/：words + examples + relations + 词根/概念/域的反向引用。

    decl 里声明的新词根、概念、语义域与词条一起落地，word_ids 自动按
    本批词条填好——避免"先建空词根导致校验不过"的中间状态。
    """
    decl = decl or {}
    wf = load("words.json")
    ef = load("examples.json")
    rf = load("relations.json")
    rootf = load("roots.json")
    cf = load("concepts.json")
    dmf = load("domains.json")

    # 本批每个词根收了哪些词
    by_root = {}
    for c in candidates:
        for rid in c.get("root_ids") or []:
            by_root.setdefault(rid, []).append(c["id"])

    # 新词根：创建时即带 word_ids
    have_roots = {r["id"] for r in rootf["roots"]}
    for r in decl.get("roots") or []:
        if r["id"] in have_roots:
            continue
        r = dict(r)
        r["word_ids"] = sorted(set(r.get("word_ids") or []) | set(by_root.get(r["id"], [])))
        rootf["roots"].append(r)

    # 新概念：同样带 word_ids
    have_con = {x["id"] for x in cf["concepts"]}
    for c2 in decl.get("concepts") or []:
        if c2["id"] in have_con:
            continue
        c2 = dict(c2)
        seed = set(c2.get("word_ids") or [])
        for rid in c2.get("root_ids") or []:
            seed |= set(by_root.get(rid, []))
        c2["word_ids"] = sorted(seed)
        cf["concepts"].append(c2)

    # 新语义域
    have_dm = {x["id"] for x in dmf["domains"]}
    for d2 in decl.get("domains") or []:
        if d2["id"] not in have_dm:
            dmf["domains"].append(dict(d2))

    # 往现有语义域追加词根
    for did, rids in (decl.get("domain_add") or {}).items():
        for d2 in dmf["domains"]:
            if d2["id"] == did:
                for rid in rids:
                    if rid not in d2["root_ids"]:
                        d2["root_ids"].append(rid)

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
                      ("concepts.json", cf), ("domains.json", dmf)):
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
    decl = {k: raw.get(k) for k in ("roots", "concepts", "domains", "domain_add")} \
        if isinstance(raw, dict) else {}

    print(f"候选词条 {len(candidates)} 条：{', '.join(c.get('id', '?') for c in candidates)}")
    for key, label in (("roots", "新词根"), ("concepts", "新概念"), ("domains", "新语义域")):
        if decl.get(key):
            print(f"{label} {len(decl[key])} 个："
                  f"{', '.join(x['id'] for x in decl[key])}")
    if decl.get("domain_add"):
        print("追加到现有语义域：" + "; ".join(
            f"{k} += {v}" for k, v in decl["domain_add"].items()))
    print()

    errors, review, auto_ok = check(candidates, decl)

    if errors:
        print(f"[FAIL] 结构错误 {len(errors)} 处，必须修正：")
        for e in errors:
            print(f"        {e}")
    else:
        print("[PASS] 结构检查通过")

    if auto_ok:
        print(f"[AUTO] {len(auto_ok)} 个外部词由参考词表自动核验："
              f"{', '.join(auto_ok[:12])}{' …' if len(auto_ok) > 12 else ''}")

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

    # 记录合并前的状态，便于判断问题是谁引入的。
    # 但不据此阻止合并——新增词根/概念必须与词条同批落地，
    # 中间状态必然"不干净"（词根的 word_ids 指向尚未入库的词）。
    pre_code, _ = run_validate()
    if pre_code != 0:
        print("\n[NOTE] 合并前 data/ 校验未通过。"
              "若本批含新增词根/概念，这是预期的中间状态；"
              "否则说明合并前就已有问题。")

    # 自动核验通过的词要登记进白名单，否则 validate.py 的 Q8 仍会拦下
    if auto_ok:
        lf = load("lexicon.json")
        before = len(lf["external_words"])
        lf["external_words"] = sorted(set(lf["external_words"]) | set(auto_ok))
        lf["reviewed_at"] = _today()
        with open(DATA / "lexicon.json", "w", encoding="utf-8") as f:
            json.dump(lf, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"白名单 {before} → {len(lf['external_words'])}（自动核验部分已登记）")

    merge(candidates, decl)
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
