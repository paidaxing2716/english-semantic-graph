#!/usr/bin/env python3
"""从已建模词根反查考研词表里尚未入库的同族候选词。

用法：
    python scripts/find_root_members.py                 # 全部词根，出汇总
    python scripts/find_root_members.py cep venire-invent   # 只看指定词根，出明细
    python scripts/find_root_members.py --min-len 4     # 只用长度≥4的变体（噪声更低）

【为什么要这个脚本】
ai_pipeline/classify_wordlist.py 是「从词表聚类」：剥词缀得词干，词干被 ≥3 词
共享才算词族。它按**拼写**匹配，于是同一词根的差异拼写会被判成互不相干的孤立词——
capere 在英语里作 cap-/capt-/cept-/cip-/ceive，`receive` 与 `capable` 拼写毫无交集，
算法只能各判一个孤立词。文档记的「3682 词孤立」因此是高估，自己也标了
「约 35% 成员被误判」。

本脚本反向做：词源判断已由人工完成（194 个词根、含 variants），
拿这些变体去词表里捞成员，召回率远高于拼写聚类。

【必须人工复核，不能自动入库】
短变体（cap / fac / sta / vent）作子串会大量误命中：
    cap  → escape, capital, cape, landscape
    sta  → instant, distance, stable
所以输出是**候选清单**，须逐词核词源后才可写进 build 脚本。
脚本会标出命中位置（词首/词中/词尾）与命中的变体，便于快速筛。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def as_list(obj, key):
    return obj if isinstance(obj, list) else obj.get(key, [])


def hit_position(word, var):
    """命中在词首/词尾/词中——词首命中多为真同族，词中命中噪声最大。"""
    i = word.find(var)
    if i == 0:
        return "词首"
    if i + len(var) == len(word):
        return "词尾"
    return "词中"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="*", help="只查这些词根 id，留空则全查")
    ap.add_argument("--min-len", type=int, default=3,
                    help="变体最短长度，默认 3；调到 4 可显著降噪")
    ap.add_argument("--include-noisy", action="store_true",
                    help="连 roots.json 里标了 noisy_variants 的低区分度变体一起用")
    ap.add_argument("-o", "--out", help="把候选写成 JSON")
    args = ap.parse_args()

    roots = as_list(load("roots.json"), "roots")
    words = as_list(load("words.json"), "words")
    in_db = {x["id"] for x in words}
    ref = as_list(load("english_reference.json"), "words")
    ref_words = {w.lower() for w in ref}

    # vetted 里已排过的词不必再提
    try:
        v = load_vetted = json.loads(
            (ROOT / "ai_pipeline" / "vetted_families.json").read_text(encoding="utf-8"))
        fams = v if isinstance(v, list) else v.get("families", v)
        if isinstance(fams, dict):
            fams = [{"words": val if isinstance(val, list) else val.get("words", [])}
                    for val in fams.values()]
        vetted = {
            (m if isinstance(m, str) else (m.get("word") or m.get("id")))
            for f in fams for m in (f.get("words") or f.get("members") or [])
        }
    except Exception:
        vetted = set()

    targets = [r for r in roots if not args.roots or r["id"] in args.roots]
    if args.roots and not targets:
        print(f"找不到词根：{args.roots}")
        return 1

    results = {}
    for r in targets:
        rid = r["id"]
        variants = sorted(
            {v.lower() for v in ([r.get("root")] + (r.get("variants") or [])) if v},
            key=len, reverse=True,
        )
        variants = [v for v in variants if len(v) >= args.min_len and v.isalpha()]
        # 低区分度变体：是真变体但作子串噪声压倒信号（如 ferre 的 lat，精度 17%）。
        # 长度挡不住这类——cip 只 3 字母却很准，lat 同样 3 字母却没用。
        # 故由 roots.json 的 noisy_variants 显式标注，默认跳过。
        if not args.include_noisy:
            noisy = {v.lower() for v in (r.get("noisy_variants") or [])}
            variants = [v for v in variants if v not in noisy]
        found = {}
        for w in ref_words:
            if w in in_db:          # 已入库
                continue
            for var in variants:
                if var in w:
                    found[w] = (var, hit_position(w, var))
                    break
        if found:
            results[rid] = found

    detail = bool(args.roots)
    total = sum(len(v) for v in results.values())
    print(f"扫描 {len(targets)} 个词根，变体最短长度 {args.min_len}")
    print(f"候选 {total} 词（已排除库中 {len(in_db)} 词）\n")

    for rid, found in sorted(results.items(), key=lambda kv: -len(kv[1])):
        head = [w for w, (v, p) in found.items() if p == "词首"]
        tail = [w for w, (v, p) in found.items() if p == "词尾"]
        mid = [w for w, (v, p) in found.items() if p == "词中"]
        newly = [w for w in found if w not in vetted]
        if detail:
            print(f"=== {rid}（候选 {len(found)}，其中 vetted 未收 {len(newly)}）===")
            for label, group in (("词首", head), ("词尾", tail), ("词中", mid)):
                if group:
                    print(f"  [{label}] " + ", ".join(
                        f"{w}({found[w][0]})" for w in sorted(group)))
            print()
        else:
            print(f"  {rid:22s} 候选 {len(found):3d}  "
                  f"词首 {len(head):3d} 词尾 {len(tail):3d} 词中 {len(mid):3d}  "
                  f"vetted 未收 {len(newly):3d}")

    if not detail:
        print("\n加词根 id 看明细，例：python scripts/find_root_members.py cep")
        print("词首命中多为真同族；词中命中噪声最大，务必逐词核词源。")

    if args.out:
        Path(args.out).write_text(json.dumps(
            {k: {w: list(t) for w, t in v.items()} for k, v in results.items()},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n已写出 {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
