#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch45.

english_reference.json（5299 词形）未收但确为通用英语的近/反义词：
  规则否定式：illegal, improper, disqualify
  法律/宗教语域常用词：lawful, bequest, inheritance, creed, devout, secular
  其它通用词：commitment, entrust, scrupulous, temperate
全为单词词元，不含短语、不含复数形、不含生造词。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "bequest", "commitment", "creed", "devout", "disqualify", "entrust",
    "illegal", "improper", "inheritance", "lawful", "scrupulous",
    "secular", "temperate",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
