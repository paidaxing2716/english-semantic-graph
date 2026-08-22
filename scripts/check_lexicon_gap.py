#!/usr/bin/env python3
"""列出某批次里 Q8 会拦下的 synonyms/antonyms，供人工核验后写进 lexicon。

用法：python scripts/check_lexicon_gap.py ai_pipeline/batchNN.json

【为什么要有这个脚本】
tests/validate.py 的 Q8 只认两个来源：
    allowed = words.json 的 id 集合 | lexicon.json 的 external_words
**不含** data/english_reference.json。reference 里的词平时能过，是因为
review.py merge 会把 auto_ok 那批自动登记进 lexicon。

但 auto_ok 有一条容易被忽略的例外（review.py 的 SUSPECT_PREFIXES）：
    若某词形如「可疑前缀 + 词库里已有的词」，即便它在 reference 里，
    也判为「疑似造词」转人工，不进 auto_ok。
    理由是 dis-/un-/re- 之类拼出来的假词可能恰好撞进词表。

第四十九批就栽在这上头：consideration 的反义 disregard 在 reference 里，
本该自动过；但 regard 刚在第四十七批入库，于是 disregard 变成
「dis + 词库已有词」→ 判疑似造词 → 不自动登记 → 合并后 Q8 拦下、白回滚一次。

本脚本完整复刻这条规则，把「会自动登记」与「必须手工登记」分开报。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def as_list(obj, key):
    return obj if isinstance(obj, list) else obj.get(key, [])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    batch = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    words = as_list(load("words.json"), "words")
    db_ids = {x["id"] for x in words}
    lexicon = set(load("lexicon.json").get("external_words") or [])
    ref = load("english_reference.json")
    ref_words = set(as_list(ref, "words"))

    incoming = {x["id"] for x in batch.get("words", [])}
    # Q8 的真实口径：只有词库 id 与 lexicon 算已核验（本批词条合并后也会进词库）
    q8_allowed = db_ids | lexicon | incoming

    # 复刻 review.py 的 SUSPECT_PREFIXES 规则
    SUSPECT_PREFIXES = ("dis", "un", "de", "in", "im", "non", "anti",
                        "mis", "re", "over", "under")
    existing_words = {(x.get("word") or x["id"]).lower() for x in words}

    auto = set()      # 在 reference 且不疑似造词 —— merge 会自动登记
    manual = set()    # 其余 —— 必须手工确认后写进 lexicon
    why = {}
    for x in batch.get("words", []):
        for f in ("synonyms", "antonyms"):
            for t in x.get(f) or []:
                if t in q8_allowed:
                    continue
                low = t.lower()
                fabricated = any(
                    low.startswith(p) and low[len(p):] in existing_words
                    for p in SUSPECT_PREFIXES
                )
                if low in ref_words and not fabricated:
                    auto.add(t)
                else:
                    manual.add(t)
                    if fabricated and low in ref_words:
                        why[t] = "在 reference 里，但形如「前缀+词库已有词」，判疑似造词转人工"

    print(f"[AUTO] {len(auto)} 词在 english_reference 中，merge 会自动登记进 lexicon：")
    print("   ", ", ".join(sorted(auto)) or "（无）")
    print()
    print(f"[MANUAL] {len(manual)} 词不会被自动登记，必须人工确认后写进 lexicon，"
          f"否则合并后 Q8 必挂：")
    print("   ", ", ".join(sorted(manual)) or "（无）")
    for t, reason in sorted(why.items()):
        print(f"      ↳ {t}：{reason}")
    print()
    phrases = sorted(t for t in auto | manual if " " in t)
    if phrases:
        print(f"[注意] 含空格的多词短语 {len(phrases)} 条，优先换成单词词元："
              f"{', '.join(phrases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
