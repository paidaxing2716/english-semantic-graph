#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch53（日耳曼核心词样品）。

由 scripts/check_lexicon_gap.py 的 [MANUAL] 清单得出，12 词全为通用英语词：
  clog（堵塞）、clown（小丑）、falcon（猎鹰）、fowl（禽）、gullet（食道）、
  kernel（核、仁）、nightfall（黄昏）、raptor（猛禽）、sage（智者）、
  suffocate（窒息）、twilight（暮色）、vow（誓约）
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "clog", "clown", "falcon", "fowl", "gullet", "kernel",
    "nightfall", "raptor", "sage", "suffocate", "twilight", "vow",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
