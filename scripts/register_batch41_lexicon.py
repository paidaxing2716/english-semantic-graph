#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch41."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "succinct", "verbose", "lengthy", "disobey", "violate",
    "unsuitable", "hinder", "settle", "harmonize", "couple", "duo",
    "mend", "prepare", "collect", "assemble", "submission", "disobedience",
    # 以下 8 词为 review 第二轮列出、仍未核验的常用词与规则否定式
    "buzz", "drone", "witty", "earlier", "compliant", "rebellious",
    "disobedient", "incomparable",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")