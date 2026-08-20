#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch32."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))
confirmed = {
    "specifics", "overview", "selling", "wholesale", "dressmaker",
    "leader", "chairperson", "occupant", "recount", "disconnect",
    "separation", "estrangement", "useful", "impractical", "virtually",
    "realistically", "rehearse", "bodily", "clinician", "mechanics",
    "outdo", "momentous", "landmark", "insignificant", "documented",
    "powered", "charged", "installer", "thrifty",
}
obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} manually confirmed words; total {len(obj['external_words'])}")
