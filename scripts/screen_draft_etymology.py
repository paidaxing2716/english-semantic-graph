#!/usr/bin/env python3
"""筛出草稿里其实属于已建模词根的词——它们不该走日耳曼型。

用法：
    python scripts/screen_draft_etymology.py drafts/g_chunk1.tsv drafts/g_chunk2.tsv ...

【为什么需要这一步】
drafts/germanic_pool.txt 是按「拼写不含任何已建模词根的变体」筛出来的。
但拼写看不出词源关系，这个筛法必漏：
    able / ability  ← 拉丁 habilis ← habere（拿住）。habere 的变体是
                      ['hibit','hab']，able 一个都不含，于是漏进日耳曼池
    ally / alliance ← 拉丁 alligare ← ligare（绑）。ligare 有变体 'ly'，
                      但只有 2 字母，被建池时 len>=3 的阈值滤掉了
    avail           ← 拉丁 valere（有力、值）
这与 find_root_members.py 的召回缺口同源：同一个词根在英语里的拼写变体
往往面目全非（receive 与 capable 同出 capere，拼写毫无交集）。

【解法】
子代理写的 origin 字段本身就是信号——它已经把拉丁/希腊源头写出来了。
本脚本扫 origin，凡提到某个已建模词根的拉丁词形，就报出来，
交人工判断该词是否应改走词根型（补进那个根，而非单独立成孤立词条）。

漏掉这一步的后果：本该并入词族的词被做成孤立浮点，图谱结构被切碎——
这正是项目要消除的东西（structus 重复 stru 那次已经犯过一回）。
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(n):
    o = json.loads((ROOT / "data" / n).read_text(encoding="utf-8"))
    return o


def as_list(o, k):
    return o if isinstance(o, list) else o.get(k, [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", nargs="+")
    ap.add_argument("--min-len", type=int, default=5,
                    help="词根拉丁词形至少这么长才拿去匹配 origin，默认 5（短的噪声大）")
    a = ap.parse_args()

    roots = as_list(load("roots.json"), "roots")
    words = as_list(load("words.json"), "words")

    # 每个词根可用来在 origin 里匹配的拉丁/希腊词形。
    #
    # 【为什么不能只用 root id 与 variants】
    # 194 个词根里有 43 个的拉丁词形短于 5 字母（fac / sta / ced / pars / fin / ag …），
    # 占两成有余。拿它们直接去匹配必须设长度下限，否则 'ag' 之类会命中一大片；
    # 但设了下限，这 43 个根就成了盲区——benign ← bene+genus 属 gen 根，
    # 'gen' 只 3 字母，旧实现整个漏掉。
    #
    # 【解法】改从词根自己的 origin 里抽拉丁/希腊词元。那里写的是完整词形
    # （sta 的 origin 写 stare、fac 写 facere、gen 写 genus / generare），
    # 长度足够、辨识度高，既覆盖短 id 的根，又不必放宽长度下限。
    lemma_pat = re.compile(r"\b([a-z][a-z]{3,})\b")
    # 这些是 origin 里的中文说明夹带的英文，不是拉丁词元
    STOP = {"vetted", "note", "pie", "root", "variants"}
    forms = {}
    for r in roots:
        cand = {r.get("root", "")} | set(r.get("variants") or [])
        cand |= set(lemma_pat.findall(r.get("origin", "")))
        cand = {c for c in cand
                if c and len(c) >= a.min_len and c.isalpha() and c not in STOP}
        if cand:
            forms[r["id"]] = cand

    members = {}
    for w in words:
        for rid in w.get("root_ids") or []:
            members.setdefault(rid, []).append(w["id"])

    hits = []
    for f in a.tsv:
        for row in csv.reader(Path(f).read_text(encoding="utf-8").splitlines(),
                              delimiter="\t"):
            if not row or len(row) < 4:
                continue
            word, origin = row[0], row[3]
            for rid, cands in forms.items():
                for c in cands:
                    if c.lower() in origin.lower():
                        hits.append((Path(f).name, word, rid, c, origin))
                        break
                else:
                    continue
                break

    if not hits:
        print("[OK] 草稿里没有词的 origin 提到已建模词根，全部可按日耳曼型入库")
        return 0

    print(f"[REVIEW] {len(hits)} 个词的 origin 提到了已建模词根，"
          f"应考虑改走词根型而非孤立词条：\n")
    for fn, word, rid, form, origin in hits:
        print(f"  {word:12s} → 词根 {rid}（origin 里出现 {form!r}）")
        print(f"      origin: {origin}")
        print(f"      该根现有成员: {members.get(rid, [])}")
        print()
    print("处理办法：把这些行从 TSV 里删掉，另做一批词根型词条补进对应词根。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
