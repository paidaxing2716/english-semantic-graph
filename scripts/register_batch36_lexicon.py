#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch36.

batch36 的近/反义词涉及的外来词，经人工确认为真实英语词后登记。
unlimited 虽形似 un+limited 的组合，但确为词典收录词，一并登记。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "dwell", "vacate", "dweller", "visitor", "gist", "cancellation",
    "unlimited", "restriction", "restricted", "administrator",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")