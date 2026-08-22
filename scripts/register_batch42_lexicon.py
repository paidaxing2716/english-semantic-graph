#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch42.

这些词都是 english_reference.json（5299 词形）没收、但确为通用英语词的近/反义词：
  常见派生/否定式：unfriendly, irrelevant, tuneless, chaotic, bulky
  施动者名词：captor, presenter, receiver, listener
  日常实物/性质词：crowbar, melodious, tuneful, pertinent, methodical, tasteful
不含任何生造词。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "bulky", "captor", "chaotic", "crowbar", "irrelevant", "listener",
    "melodious", "methodical", "pertinent", "presenter", "receiver",
    "tasteful", "tuneful", "tuneless", "unfriendly",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
