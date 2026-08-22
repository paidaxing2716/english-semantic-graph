#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch46.

english_reference.json（5299 词形）未收但确为通用英语的近/反义词：
  副词：casually, deliberately, mainly, slightly
  形容词：arithmetical, countless, myriad
  名词：grandeur, stance, bike
  动词：atone, reuse
全为单词词元。biology 的 life science / bioscience 与 incidentally 的
by the way 已在词条里去掉——短语和生僻词不进白名单。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "arithmetical", "atone", "bike", "casually", "countless", "deliberately",
    "grandeur", "mainly", "myriad", "reuse", "slightly", "stance",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
