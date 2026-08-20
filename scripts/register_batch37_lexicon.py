#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch37.

batch37 近/反义词涉及的外来词经人工确认。'ever more' 是短语非单词，
review 里会按 external_words 找不到而提示——短语不进词表，直接忽略提示。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "writer", "creator", "counterfeit", "jurisdiction", "elucidate",
    "lucidity", "clearness", "vagueness", "progressively",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")