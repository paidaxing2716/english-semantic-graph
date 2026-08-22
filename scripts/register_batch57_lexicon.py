#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch57.

由 scripts/check_lexicon_gap.py 的 [MANUAL] 清单得出，4 词：
  announcement（公告）、baker（面包师）、loser（败者）、victor（胜者）

原始清单有 35 词，31 个已在词条里换成 english_reference 中已核验的词元，
不往白名单硬塞。换掉的几类：
  复数形：cows → cattle/animal；grounds → yard/field 与 reason
  带连字符（等同短语）：runner-up → loser
  生僻或冷门：automobile→car、transporter→carrier、artillery→weapon、
    dispensary→ward、culmination→top、anticlimax→low、sedition→revolt、
    defector→spy、loyalist→faith、encampment→base、caterer→baker、
    declaim→read、skittles→game、ballgame→sport、waterway→channel、
    strait→route、vault→store、attic→roof、arena→stage、quad→yard、
    cyclic→circular、soothe→quiet、truce→calm、slug→ball、animation→film
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {"announcement", "baker", "loser", "victor"}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
