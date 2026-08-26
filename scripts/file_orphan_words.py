#!/usr/bin/env python3
"""把从未进过任何池子的考研词归池。

    python scripts/file_orphan_words.py --dry-run
    python scripts/file_orphan_words.py

【问题】考研词表 5299 词形里，有一批既不在库、也不在 germanic_remaining /
latin_remaining 任何池子里——按现有流程**永远派不到**。这与早先发现的
root_backlog_from_67.txt 那 111 词是同一类：排池方式本身在漏词。

【怎么分档】按 Wiktionary 词元与现有 273 个根的匹配结果分三档：
  root  —— 词元匹配到某个现有根，走词根批（族头标「疑」，必须逐词核）
  germ  —— 查不到拉丁/希腊词元，或词元零散凑不到 3 个成员，走日耳曼批
  hold  —— 多词短语与连字符词，规格未定体例，先扣下

**root 档的匹配噪声很高**（实测 cash→cep、cup→cep、command→manus、artery→
ter-comparative 都是假的），所以只写成「疑」，不写成「确」。派发时必须让代理
逐词核词源，别照单全收。

核心功能词（a / and / be / he / it / in / not …）不归池：它们没有画面也没有词族，
按项目规则本就不建词条。名单见 FUNC。
"""
import argparse
import collections
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "drafts"
sys.path.insert(0, str(ROOT / "scripts"))
import probe_etymology_coverage as P  # noqa: E402

FUNC = set(
    "a all and any at be being both but by can do each few for have he her here "
    "him his how in it its me more most no not of on only or other our own same "
    "she so some such than that the their them then there these they this those "
    "to too us very was we were what when where which who whom whose why will "
    "with you your i my am is are been does did had has just should now if as yes"
    .split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    W = json.loads((ROOT / "data/words.json").read_text(encoding="utf-8"))["words"]
    R = json.loads((ROOT / "data/roots.json").read_text(encoding="utf-8"))["roots"]
    ids = {w["id"] for w in W}
    ref = {(w if isinstance(w, str) else (w.get("word") or w.get("lemma"))).lower()
           for w in json.loads((ROOT / "data/english_reference.json")
                               .read_text(encoding="utf-8"))["words"]}

    pool = {}
    for f in ("germanic_remaining", "latin_remaining"):
        for line in (D / f"{f}.txt").read_text(encoding="utf-8").splitlines():
            t = line.split("#")[0].strip().split("\t")[0].strip().lower()
            if t:
                pool[t] = f

    orphan = sorted(w for w in ref
                    if w and w not in ids and w not in pool and w not in FUNC)
    if not orphan:
        print("没有漏网词，池子是完整的")
        return 0

    keys = P.root_keys(R)
    sizes = {r["id"]: len(r.get("word_ids") or []) for r in R}
    root_hits, by_lemma, germ, hold = {}, collections.defaultdict(list), [], []
    for w in orphan:
        if " " in w or "-" in w:
            hold.append(w)
            continue
        f = P.CACHE / (urllib.parse.quote(w, safe="") + ".txt")
        lms = P.lemmas(P.english_etymology(f.read_text(encoding="utf-8"))) \
            if f.exists() else []
        if not lms:
            germ.append(w)
            continue
        m = P.match(lms, keys, sizes)
        if m:
            root_hits[w] = m[0][0]
        else:
            by_lemma[lms[0][0]].append(w)

    # 词元族凑不到 3 个成员的，按项目规则不值得开根 → 归日耳曼批
    for lm, ws in by_lemma.items():
        if len(ws) >= 3:
            for w in ws:
                root_hits[w] = f"NEW:{lm}"
        else:
            germ.extend(ws)
    germ.sort()

    print(f"漏网 {len(orphan)} 词（已剔 {len(FUNC & ref)} 个核心功能词）：")
    print(f"  root 档 {len(root_hits)} 词 → drafts/orphan_root.txt（族头标「疑」）")
    print(f"  germ 档 {len(germ)} 词 → 并入 germanic_remaining.txt")
    print(f"  hold 档 {len(hold)} 词 → drafts/orphan_hold.txt：{', '.join(hold)}")

    byroot = collections.defaultdict(list)
    for w, rid in root_hits.items():
        byroot[rid].append(w)
    lines = ["# 本文件的归属全部是「疑」——匹配噪声高（实测 cash→cep、cup→cep、",
             "# command→manus、artery→ter-comparative 都是假的），派发时必须逐词核词源。",
             "# 由 scripts/file_orphan_words.py 生成；这些词此前不在任何池子里。"]
    for rid, ws in sorted(byroot.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        cur = sizes.get(rid, 0)
        tag = (f"疑新根（词元 {rid[4:]}）" if rid.startswith("NEW:")
               else f"疑补词——同名根已存在（{rid}），现有 {cur} 词")
        lines.append(f"# {rid}\t{len(ws)} 词\t{tag}")
        lines.extend(sorted(ws))

    if a.dry_run:
        print("\n（dry-run，未写入）前 12 行预览：")
        for x in lines[:12]:
            print("   " + x)
        return 0

    (D / "orphan_root.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (D / "orphan_hold.txt").write_text(
        "# 多词短语与连字符词：规格未定体例，先扣下\n" + "\n".join(hold) + "\n",
        encoding="utf-8")
    gp = D / "germanic_remaining.txt"
    old = gp.read_text(encoding="utf-8").rstrip("\n").splitlines()
    have = {x.split("#")[0].strip().split("\t")[0].strip().lower() for x in old}
    add = [w for w in germ if w not in have]
    gp.write_text("\n".join(old + add) + "\n", encoding="utf-8")
    print(f"\n已写入：orphan_root.txt（{len(root_hits)} 词）、"
          f"orphan_hold.txt（{len(hold)} 词）、"
          f"germanic_remaining.txt 追加 {len(add)} 词")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
