#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch48.

english_reference.json（5299 词形）未收但确为通用英语的近/反义词：
  规则否定/反义式：apolitical, disfavor, unfavorable, inexperience, disliked
  名词：artwork, buyer, clarification, decorator, legislator, seller,
        statecraft, vegetation
  形容词：civic, governmental, preferred, proven
  动词：graft, relocate
  英式拼写：colour
全为单词词元。favorite 的反义原写作短语 least liked，已在词条里改成 disliked。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "apolitical", "artwork", "buyer", "civic", "clarification", "colour",
    "decorator", "disfavor", "disliked", "governmental", "graft",
    "inexperience", "legislator", "preferred", "proven", "relocate",
    "seller", "statecraft", "unfavorable", "vegetation",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
