#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch43.

english_reference.json（5299 词形）未收但确为通用英语的近/反义词：
  英式拼写：behaviour, harbour
  常见派生/复合：handmade, roomy, cramped, demolition, relaxation, teaching
  普通词：dock, forsake, vast
  多词短语：hold back —— HANDOFF 提示短语必须显式注册才过 Q8
不含任何生造词。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "behaviour", "cramped", "demolition", "dock", "forsake", "handmade",
    "harbour", "hold back", "relaxation", "roomy", "teaching", "vast",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
