#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch44.

english_reference.json（5299 词形）未收但确为通用英语的近义词：
  commentary（评论）、influenza（流感全称，flu 的来源词）、
  screenplay（电影剧本）、version（版本）、weaken（削弱）
全为单词词元，不含短语、不含复数形、不含生造词。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {"commentary", "influenza", "screenplay", "version", "weaken"}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
