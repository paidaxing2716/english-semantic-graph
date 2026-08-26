#!/usr/bin/env python3
"""把 root_gaps_existing.txt 的 AGREE 档切成可派的词根批输入。

    python scripts/chunk_agree_gaps.py [--n 5]

AGREE 档 = engra 与 Wiktionary 双源指向同一个已有根，是这批里最干净的部分。
全部是**补词**（根已存在，不写 R 行，W 行第 5 列填根 id），所以族头统一标补词。

输出 drafts/rt_chunk61.txt … （61 起，1-36 与 41-56 已用过）
族整体不跨片——同族词在同一个代理手里，写 root_logic 时能看到全族。
"""
import argparse
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "drafts"
START = 61


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5, help="切几片")
    a = ap.parse_args()

    words = json.loads((ROOT / "data" / "words.json").read_text(
        encoding="utf-8"))["words"]
    ids = {w["id"] for w in words}
    roots = json.loads((ROOT / "data" / "roots.json").read_text(
        encoding="utf-8"))["roots"]
    rids = {r["id"] for r in roots}
    cur = {r["id"]: len(r.get("word_ids") or []) for r in roots}

    # 已在别处待派或已起草的词必须摘掉，否则同一个词会有两份冲突记录。
    # 实测过一次：universal 在 rt_chunk51 被判给 unus、在本批被判给 vert，
    # 两批都合并就是排池文档警告的那种撞车。
    taken = {}
    for f in sorted(D.glob("rt_chunk[1-5]*.txt")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            w = line.split("#")[0].strip().split("\t")[0].strip().lower()
            if w:
                taken[w] = f.name
    for f in sorted(D.glob("r_chunk*.tsv")):
        for line in f.read_text(encoding="utf-8").splitlines():
            p = line.split("\t")
            if len(p) > 1 and p[0] == "W":
                taken[p[1].strip().lower()] = f.name

    fam = collections.defaultdict(list)
    clash = []
    for line in (D / "root_gaps_existing.txt").read_text(
            encoding="utf-8").splitlines():
        if line.startswith("#") or line.count("\t") < 2:
            continue
        parts = line.split("\t")
        rid, tier, word = parts[0], parts[1], parts[2]
        lemma = parts[3].strip() if len(parts) > 3 else ""
        if tier != "AGREE":
            continue
        if word in ids:                    # 已入库的不该出现在缺失清单里
            print(f"  [skip] {word} 已在库")
            continue
        if word in taken:                  # 别处已占
            clash.append((word, rid, taken[word]))
            continue
        if rid not in rids:                # 根必须真存在，否则不是补词
            print(f"  [skip] {word} 的根 {rid} 不在 roots.json")
            continue
        fam[rid].append((word, lemma))
    if clash:
        print(f"  摘掉 {len(clash)} 个已被别处占用的词：")
        for w, rid, where in sorted(clash):
            print(f"    {w:16} 本批想判 {rid:14} 但已在 {where}")

    groups = sorted(fam.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    bins = [[] for _ in range(a.n)]
    sizes = [0] * a.n
    for rid, members in groups:            # 族整体不跨片，按词数装最小的那片
        i = sizes.index(min(sizes))
        bins[i].append((rid, sorted(set(members))))
        sizes[i] += len(members)

    seen, written = set(), []
    for n, chunk in enumerate(bins, start=START):
        lines = []
        for rid, members in sorted(chunk, key=lambda kv: (-len(kv[1]), kv[0])):
            lines.append(f"# {rid}\t{len(members)} 词\t"
                         f"补词——同名根已存在，按补词写，勿新建（{rid}）"
                         f"\t现有 {cur.get(rid, 0)} 词")
            for w, lemma in members:
                assert w not in seen, f"跨片重复：{w}"
                seen.add(w)
                lines.append(f"{w}\t# 词元 {lemma}" if lemma else w)
        f = D / f"rt_chunk{n}.txt"
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append((f.name, sum(len(m) for _, m in chunk), len(chunk)))

    print(f"AGREE 档 {sum(len(v) for v in fam.values())} 词 / {len(groups)} 族，"
          f"切 {a.n} 片")
    for name, nw, nf in written:
        print(f"  {name}: {nw} 词 / {nf} 族")
    print(f"去重校验：写出 {len(seen)} 词，无跨片重复")


if __name__ == "__main__":
    main()
