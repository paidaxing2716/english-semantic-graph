#!/usr/bin/env python3
"""把 interference 从 ferre 摘下来，改成孤立词条（日耳曼型）。

    python scripts/fix_interference_root.py --dry-run
    python scripts/fix_interference_root.py

【为什么】库里这条自相矛盾：origin 明写「inter＋ferire」，root_logic 却写
「fer（带）」，挂在 ferre 上。Wiktionary 证实 interfere ← 古法语 entreferir
← 拉丁 ferio（击打），与 ferre（带、拿去）是两个动词。由 chunk61 的子代理
在核 interfere 时点出。

ferire 一支库中仅此一词（interfere 本身尚未入库），按「凑不到 3 个成员不值得
开根」转为孤立词条，不新建 ferire 根。

【四处同步】只改 words.json 会被 Q9 挡下：
  words 的 root_ids/root_logic → 根的 word_ids → 概念的 word_ids → relations 的边
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

WORD = "interference"
FROM_ROOT = "ferre"
NOTE = ("日耳曼核心词处理：ferire（击打）一支库中仅此一词，不足以开根；"
        "与 ferre（带、拿去）不同源，勿混")


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(
        json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    words, roots = load("words.json"), load("roots.json")
    concepts, rels = load("concepts.json"), load("relations.json")
    done = []

    w = next((x for x in words["words"] if x["id"] == WORD), None)
    if w is None:
        print(f"[FAIL] {WORD} 不在库中")
        return 1
    if w.get("root_ids") != [FROM_ROOT]:
        print(f"[SKIP] {WORD} 的 root_ids 是 {w.get('root_ids')}，"
              f"不是 [{FROM_ROOT}]——可能已修过")
        return 0

    # 字段名是 decomposable（不是 type），且 root_logic 必须留空串——
    # 它是必填字段，删掉会被 validate.py 报「words 缺少必填字段」。
    # 判断词条类型看的也是 decomposable，写 type 不生效（Q11 仍判它是 root 型）。
    w["root_ids"] = []
    w["root_logic"] = ""
    w.pop("type", None)                    # 清掉上一版误加的字段
    w["decomposable"] = "germanic"
    w["decomposable_note"] = NOTE
    done.append("words: root_ids 清空、root_logic 置空串、"
                "decomposable=germanic、加 decomposable_note")

    for r in roots["roots"]:
        if r["id"] == FROM_ROOT and WORD in (r.get("word_ids") or []):
            r["word_ids"].remove(WORD)
            done.append(f"roots: 从 {FROM_ROOT}.word_ids 移除"
                        f"（剩 {len(r['word_ids'])} 词）")

    for c in concepts["concepts"]:
        if WORD in (c.get("word_ids") or []):
            c["word_ids"].remove(WORD)
            done.append(f"concepts: 从 {c['id']}.word_ids 移除")

    before = len(rels["relations"])
    rels["relations"] = [r for r in rels["relations"]
                         if not (r.get("to") == WORD and r.get("type") == "root")]
    if len(rels["relations"]) != before:
        done.append(f"relations: 删 {before - len(rels['relations'])} 条 root 边")

    for d in done:
        print("  " + d)
    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    for n, o in (("words.json", words), ("roots.json", roots),
                 ("concepts.json", concepts), ("relations.json", rels)):
        save(n, o)
    print(f"\n已写入 4 个文件，共 {len(done)} 处改动")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
