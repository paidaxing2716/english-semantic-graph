#!/usr/bin/env python3
"""把搭配回填进已入库词条的 collocations 字段。

    python scripts/backfill_collocations.py drafts/cl_chunk73.tsv --dry-run
    python scripts/backfill_collocations.py drafts/cl_chunk73.tsv

输入是两列 TSV：`word <TAB> 型式 —— 说明|型式 —— 说明|...`

【为什么不走 entries_from_draft】那条管道是给**新词条**用的，遇到已入库的词会
报「已在词库中，勿重复入库」并拒绝——本任务恰恰只改已入库词条的一个字段。
走这条路也避免重写其余 14 列（回填不该动画面、义项、例句）。

只写 collocations 一个字段，其余一律不动。已有搭配的词条默认跳过（要覆盖用
--overwrite），避免把前一批写好的内容冲掉。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--overwrite", action="store_true",
                    help="连已有搭配的词条一起覆盖（默认跳过）")
    a = ap.parse_args()

    p = DATA / "words.json"
    db = json.loads(p.read_text(encoding="utf-8"))
    idx = {w["id"]: w for w in db["words"]}

    rows, errs = [], []
    for f in a.tsv:
        for lineno, line in enumerate(
                Path(f).read_text(encoding="utf-8").splitlines(), 1):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) != 2:
                errs.append(f"{Path(f).name}:{lineno} 应为 2 列，实为 {len(cols)}")
                continue
            wid, colloc = cols[0].strip(), cols[1].strip()
            if wid not in idx:
                errs.append(f"{Path(f).name}:{lineno} {wid} 不在库中")
                continue
            items = [x.strip() for x in colloc.split("|") if x.strip()]
            if not items:
                errs.append(f"{Path(f).name}:{lineno} {wid} 搭配为空")
                continue
            bad = [x for x in items if "——" not in x]
            if bad:
                errs.append(f"{Path(f).name}:{lineno} {wid} 这些条目缺 '——'："
                            f"{bad[:2]}")
                continue
            # 型式里不该出现中文（型式是英文句法模板，说明才是中文）
            for x in items:
                pat = x.split("——")[0]
                if any("一" <= c <= "鿿" for c in pat) \
                        and not any(k in pat for k in ("从句", "主语", "主句")):
                    errs.append(f"{Path(f).name}:{lineno} {wid} 型式里有中文："
                                f"{pat.strip()!r}")
                    break
            else:
                rows.append((wid, items))

    if errs:
        print(f"[FAIL] {len(errs)} 条不合格，未写入：")
        for e in errs:
            print("   " + e)
        return 1

    changed, skipped = [], []
    for wid, items in rows:
        if idx[wid].get("collocations") and not a.overwrite:
            skipped.append(wid)
            continue
        changed.append((wid, items))

    print(f"待回填 {len(changed)} 词" +
          (f"，跳过已有搭配的 {len(skipped)} 词：{skipped}" if skipped else ""))
    for wid, items in changed[:5]:
        print(f"\n  {wid}")
        for x in items:
            print(f"    {x}")
    if len(changed) > 5:
        print(f"\n  …其余 {len(changed) - 5} 词略")

    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    for wid, items in changed:
        idx[wid]["collocations"] = items
    p.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    print(f"\n已写入 {len(changed)} 词的 collocations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
