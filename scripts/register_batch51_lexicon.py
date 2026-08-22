#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch51.

由 scripts/check_lexicon_gap.py 的 [MANUAL] 清单得出，仅 2 词：
  query（疑问、查询）、saving（储蓄、节省）

原始清单有 22 词，绝大多数已在词条里换成 english_reference 中已核验的词元，
不往白名单硬塞。换掉的几类：
  多词短语 3 条 → life story/reference list → account/writing；
                  down payment → saving
  复数形 officers → officer / guard
  生僻或冷门 → attainment→gain、girth→edge、topography/terrain→land/map、
              perimeter→boundary、intrusion→block、suppression→control、
              regression→decline、reformist→steady、ornate→fancy、
              affirmative→certain、memoir→writing、urban→city、
              constable/constabulary→guard/police、works→text
另修一处死链：literature 的 related 原写 'letter'（不在库），
改为 littera 族已入库成员 literary / literacy。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {"query", "saving"}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
