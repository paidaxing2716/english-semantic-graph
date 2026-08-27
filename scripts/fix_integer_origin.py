#!/usr/bin/env python3
"""把 integer 根 origin 里的裸拉丁原形 tangere 换成中文描述。

    python scripts/fix_integer_origin.py [--dry-run]

【为什么要改】
门二从每个根的 origin 里抽首个拉丁词当匹配键（root_keys 的设计）。integer 的
origin 写着「in-（不）+ tangere（触碰）」，于是 tangere 成了 integer 的键，任何
origin 里提到 tangere 的词都会被报成「应该挂 integer」。

第九十八批的 intact 就中了这一枪：它正确挂在 tangere 上，门二却报它该挂 integer。
这不是一次性误报——库里已有 tangere 根（3 员），今后每个走 tangere 的词都会撞。

项目对新词条早有这条规则（draft-spec：origin 里不要写别的词根的拉丁原形，要对比
就用根 id 或中文描述），但**这条规则没有回头适用于已入库的根**。本脚本补这一处。

改法：只动 origin 的表述，不动词源事实——in- + 「触碰」那一支的语义仍然写着，
学习者读到的内容不变，只是不再给门二留一个假键。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "roots.json"

OLD = "拉丁语 integer（完整、未触碰），由 in-（不）+ tangere（触碰）形成"
NEW = ("拉丁语 integer（完整、未触碰），由 in-（不）+「触碰」那一支的过去分词形成；"
       "碰过就有缺口，没碰过才是整的")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    d = json.loads(P.read_text(encoding="utf-8"))
    hit = None
    for r in d["roots"]:
        if r["id"] == "integer":
            hit = r
            break
    if hit is None:
        raise SystemExit("[FAIL] 没找到 integer 根")

    cur = hit.get("origin", "")
    if cur != OLD:
        # 不静默跳过——静默跳过正是这一轮在消灭的缺陷类型
        raise SystemExit(
            f"[FAIL] integer 的 origin 与预期不符，可能已被改过。\n"
            f"  现值：{cur}\n  预期：{OLD}\n"
            f"  先确认再改，别盲目覆盖。")

    print(f"[改] integer.origin\n  旧：{cur}\n  新：{NEW}")
    if a.dry_run:
        print("\n[dry-run] 未写盘")
        return

    hit["origin"] = NEW
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    print("\n[OK] 已写盘")


if __name__ == "__main__":
    main()
