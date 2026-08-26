#!/usr/bin/env python3
"""修 decomposable_note：非日耳曼来源的词不该写「日耳曼核心词」。

    python scripts/fix_decomposable_notes.py --dry-run
    python scripts/fix_decomposable_notes.py

【问题】entries_from_draft.py 只要 root_ids 为空就无条件套用默认文案
「日耳曼核心词，本身即词根，无拉丁词缀可拆」。但「不挂词根」的真实原因有两种：
  a) 确实是日耳曼核心词（古英语 ceosan 那类）
  b) 是拉丁/法语/希腊借词，只是拆开也推不出可学联系，或该族凑不到 3 个成员
b 类同样落到默认文案上，于是 abandon（古法语）、absorb（拉丁语）、absurd
（拉丁语）在库里都写着「日耳曼核心词」。实测 1610 条用默认文案的词条里，
578 条的 origin 明写非日耳曼来源。

由 chunk56 的子代理指出（它写的 alter/mount/nice 五条全属 b 类），核查后发现
是全库范围的既有问题，不止那五条。

【只改文案，不改归属】这些词确实不该挂根——归属是对的，错的是理由。
按 origin 里的语源线索改写成中性表述，不臆断具体来源。origin 里没有任何语源
线索的（83 条）一概不动，那要逐条查证，不能猜。
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DEFAULT = "日耳曼核心词，本身即词根，无拉丁词缀可拆"

# origin 里的语源线索 → 改写后的文案。顺序有意义：先匹配到的胜出，
# 所以「古英语」要排在「拉丁」之前——古英语词条的 origin 常顺带提到拉丁同源词。
GERMANIC = ("古英语", "原始日耳曼", "中古英语", "古诺斯", "古高地德", "古撒克逊",
            "原始西日耳曼")
# 措辞只说「本项目未为它建词根」这个事实，不说「没有词缀」——很多词的 origin
# 明写着词缀（abound 写「ab-（自）+ unda（波浪）」、absorb 写「ab- + sorbere」），
# 断言无词缀等于用一个新的错陈述换掉旧的。真实原因是该词族在 5299 词表里凑不到
# 3 个成员、或拆开推不出可学联系，两者都不该由脚本替人断定，故只陈述事实。
FOREIGN = {
    "法语": "经法语入英语的借词，本项目未为其词族建根，按整体记",
    "拉丁": "拉丁借词，本项目未为其词族建根，按整体记",
    "希腊": "希腊借词，本项目未为其词族建根，按整体记",
    "意大利": "借自意大利语，本项目未为其词族建根，按整体记",
    "西班牙": "借自西班牙语，本项目未为其词族建根，按整体记",
    "荷兰": "借自荷兰语，本项目未为其词族建根，按整体记",
    "阿拉伯": "借自阿拉伯语，本项目未为其词族建根，按整体记",
    "梵语": "借自梵语，本项目未为其词族建根，按整体记",
    "俄语": "借自俄语，本项目未为其词族建根，按整体记",
    "日语": "借自日语，本项目未为其词族建根，按整体记",
}


EARLY_LOAN = "早期借词，经古英语或中古英语阶段传入，词形已归化，无可拆的词缀"


def classify(origin):
    o = origin or ""
    for k in GERMANIC:
        if k in o:
            # 第三档：经古英语/中古英语传入的早期借词。origin 形如
            # 「古英语 ancor ← 拉丁语 ancora」——日耳曼词形只是传入路径，箭头
            # 指向的才是终极来源，这类不是日耳曼核心词。上一版把它们一律留在
            # 默认文案里（理由是「古英语那层在前」），那个判断是错的：belt ←
            # balteus、cheese ← caseus、candle ← candela 都不是日耳曼词。
            # 由 chunk76 的子代理写 turn 时指出。
            for f in FOREIGN:
                if re.search(r"←[^←]{0,14}" + f, o):
                    return EARLY_LOAN
            return None                    # 真日耳曼词，文案本来就对
    for k, note in FOREIGN.items():
        if k in o:
            return note
    return None                            # 无线索，不猜


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="只改前 N 条，用于抽验")
    a = ap.parse_args()

    p = DATA / "words.json"
    db = json.loads(p.read_text(encoding="utf-8"))
    changed = []
    for w in db["words"]:
        if w.get("root_ids"):
            continue
        if w.get("decomposable_note") != DEFAULT:
            continue                        # 已被人工写过的不动
        note = classify(w.get("origin"))
        if not note:
            continue
        if a.limit and len(changed) >= a.limit:
            break
        changed.append((w["id"], (w.get("origin") or "")[:60], note))
        w["decomposable_note"] = note

    import collections
    by = collections.Counter(n for _, _, n in changed)
    print(f"待改 {len(changed)} 条，按新文案分：")
    for note, n in by.most_common():
        print(f"  {n:4}  {note}")
    print("\n样本 8 条：")
    for wid, o, note in changed[:8]:
        print(f"  {wid:14} origin: {o}")
        print(f"  {'':14} → {note}")

    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    p.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    print(f"\n已写入 {len(changed)} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
