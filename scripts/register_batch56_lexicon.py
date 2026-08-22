#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch56.

由 scripts/check_lexicon_gap.py 的 [MANUAL] 清单得出，6 词：
  harmless（无害的）、inability（无能力）、kindly（和善的）、
  metropolis（大都市）、mortar（砂浆）、unable（不能的）

其中 inability / unable / harmless 是规则否定式，命中 review.py 的
SUSPECT_PREFIXES 故不自动登记，但都是通用英语词。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {"harmless", "inability", "kindly", "metropolis", "mortar", "unable"}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
