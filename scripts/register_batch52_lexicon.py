#!/usr/bin/env python3
"""Register manually confirmed real English words used by batch52.

由 scripts/check_lexicon_gap.py 的 [MANUAL] 清单得出，仅 3 词：
  coldness（冷淡）、decided（明确的、坚决的）、planned（有计划的）

原始清单有 30 词，绝大多数已在词条里换成 english_reference 中已核验的词元，
不往白名单硬塞。换掉的几类：
  多词短语 2 条：let down → fail；stand for → show
  形近生僻：blockage→obstacle、clearance→clear、dynamo→engine、
           infirmary→ward、schoolfellow→friend、schoolroom→school、
           supposition→guess、absoluteness→absolute、interdependence→connection、
           indecision→doubt、tardy→slow、outdated→old、homage→respect、
           donation→gift、indict→accuse、harass→trouble、indulgence→luxury、
           habituated→habit、unaccustomed→strange、computerized→electric、
           determination→decision、hesitant/wavering→doubtful/weak、
           hostility→coldness、unintended→accidental、intentional→planned
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "lexicon.json"
obj = json.loads(p.read_text(encoding="utf-8"))

confirmed = {"coldness", "decided", "planned"}

obj["external_words"] = sorted(set(obj.get("external_words", [])) | confirmed)
obj["reviewed_at"] = date.today().isoformat()
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered {len(confirmed)} words; total {len(obj['external_words'])}")
