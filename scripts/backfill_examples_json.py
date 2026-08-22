#!/usr/bin/env python3
"""回填 examples.json 里缺失的条目，使其与 words.json 的内嵌例句对齐。

用法：
    python scripts/backfill_examples_json.py --dry-run
    python scripts/backfill_examples_json.py

【问题】
data/examples.json 3855 条覆盖 1931 词，而 data/words.json 内嵌 3882 条例句
覆盖 1935 词——差 27 条、4 个词。缺口全在早期手工批次：
    完全没有条目：choose / select / pick / state
    条数少于 words.json：figure / impress / express / suppress / perform /
        position / compose / admit / commit 等 21 个
这些词都早于 ai_pipeline/review.py 的 merge 管线。该管线自建立起就会为每个
合并的词写 examples.json（review.py:293-299），故后续批次都是对齐的。

【为什么之前没被发现】
tests/validate.py 只查一个方向（examples.json 的 word_id 是否都存在于
words.json，第 358 行），不查反向。前端读的是 words.json 的内嵌 examples
（graph.js:238、study.js:96），不读 examples.json，所以产品显示一直正常，
只有 validate 报的「例句 N」少报了 27 条。

【做法】
照 review.py 同一套逻辑生成缺失条目，不编造内容：
    id      = f"ex-{word_id}-{序号}"
    scene   = 该词 core_image 的前 40 字
    source  = "回填 · 据 words.json 对齐"（与 AI 生成条目区分开）
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    wf = json.loads((DATA / "words.json").read_text(encoding="utf-8"))
    ef = json.loads((DATA / "examples.json").read_text(encoding="utf-8"))
    words = wf if isinstance(wf, list) else wf["words"]

    have = {}
    for e in ef["examples"]:
        have.setdefault(e["word_id"], set()).add(e["text"])

    added = []
    for w in words:
        got = have.get(w["id"], set())
        for i, text in enumerate(w.get("examples") or [], 1):
            if text in got:
                continue
            added.append({
                "id": f"ex-{w['id']}-{i}",
                "word_id": w["id"],
                "text": text,
                "source": "回填 · 据 words.json 对齐",
                "scene": (w.get("core_image") or "")[:40],
            })

    print(f"examples.json 现有 {len(ef['examples'])} 条")
    print(f"words.json 内嵌 {sum(len(w.get('examples') or []) for w in words)} 条")
    print(f"须回填 {len(added)} 条，涉及 {len({x['word_id'] for x in added})} 个词：")
    for x in added[:8]:
        print(f"   {x['word_id']}: {x['text'][:52]}")
    if len(added) > 8:
        print(f"   …… 另 {len(added)-8} 条")

    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0

    # id 去重：同一词若已有 ex-xxx-1，新条目要避开
    used = {e["id"] for e in ef["examples"]}
    for x in added:
        base = x["id"]
        n = 1
        while x["id"] in used:
            n += 1
            x["id"] = f"{base}-{n}"
        used.add(x["id"])

    ef["examples"].extend(added)
    (DATA / "examples.json").write_text(
        json.dumps(ef, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n已写入，examples.json 现 {len(ef['examples'])} 条")

    # 自检：两边应完全对齐
    have2 = {}
    for e in ef["examples"]:
        have2.setdefault(e["word_id"], set()).add(e["text"])
    gap = [(w["id"], t) for w in words for t in (w.get("examples") or [])
           if t not in have2.get(w["id"], set())]
    assert not gap, f"仍有 {len(gap)} 条未对齐：{gap[:3]}"
    ids = [e["id"] for e in ef["examples"]]
    assert len(ids) == len(set(ids)), "examples.json 出现重复 id"
    print("   自检通过：两边完全对齐、id 无重复")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
