#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch50.

由 scripts/check_lexicon_gap.py 的 [MANUAL] 清单得出——那 6 词既不在
words.json 也不在 english_reference，merge 不会自动登记，须手工确认。

  abstain（弃权、戒除）、contributor（贡献者）、fussy（挑剔的）、
  lenient（宽松的）、separately（分别地）、triviality（琐碎、无关紧要）

另有 6 处原本要往白名单里塞的词已在词条里换掉，不进 lexicon：
  undeceive → enlighten   （undeceive 非通用词，且命中 SUSPECT_PREFIXES）
  asunder   → 删（保留 separately）  （asunder 偏古旧）
  speck     → grain
  observer  → witness
  mathematics → arithmetic
  autograph / hallmark → 留空（signature 的近义词非必需）
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {
    "abstain", "contributor", "fussy", "lenient", "separately", "triviality",
}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
