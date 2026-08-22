#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch49.

english_reference.json（5299 词形）未收但确为通用英语的近/反义词：
  名词：affluence, deliberation, lecturer, stockpile, thoughtfulness, warehousing
  形容词：periodic, seasonal, sizeable, thriving, fourth
  副词：currently
  动词：reinstate
全为单词词元，不含短语、不含复数形、不含生造词。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "affluence", "currently", "deliberation", "fourth", "lecturer",
    "periodic", "reinstate", "seasonal", "sizeable", "stockpile",
    "thoughtfulness", "thriving", "warehousing",
    # disregard 两边都不在：既不在 english_reference，也不在 lexicon。
    # validate.py 的 Q8 只认 word_ids | lexicon 两个来源，reference 词能过
    # 是因为 review.py merge 会把它们自动登记进 lexicon，故此词须手工补。
    "disregard",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
