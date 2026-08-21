#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch38.

batch38 近/反义词涉及的外来词经人工确认（均为常见英语词）。
短语近义词已改为单词（writing materials→paper/pens、data-driven→quantitative）。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "accomplishment", "anticipation", "appealing", "bearer", "broken",
    "ceaseless", "charming", "compliance", "conformity", "consequent",
    "defiance", "disagreement", "improbable", "landmass", "matching",
    "opposition", "prevailing", "quantitative", "repellent", "resulting",
    "unaffected", "paper", "pens",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
