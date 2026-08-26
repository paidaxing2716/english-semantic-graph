#!/usr/bin/env python3
"""整理两份清单，engra × Wiktionary 双源交叉验证。

    python scripts/build_root_gaps.py

输出（都在 drafts/，gitignored，不动 data/）：
    drafts/root_gaps_existing.txt   现有根缺的考研词
    drafts/root_candidates_new.txt  该开的新根候选

判定分三档：
    双源一致  engra 的根 == Wiktionary 词元映射到的根 —— 可直接派
    仅 engra  Wiktionary 查到拉丁/希腊词元但映射不到该根 —— 要核
    非词源    Wiktionary 根本查不到拉丁/希腊来源 —— engra 是按语素/拼写聚的，剔除

第三档是关键：它把 self/day/gl/like/head/way 这类英语语素分组自动筛掉，
不必人肉判断——判据是「有没有拉丁希腊祖先」，不是「看着像不像词根」。
"""
import collections
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_etymology_coverage as P                      # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
D = ROOT / "drafts"


def load_engra():
    p = Path(os.environ["TEMP"]) / "engra_words.csv"
    if not p.exists():
        sys.exit(f"缺 {p}，先下载 eslsoft/engra 的 dict/words.csv")
    out = {}
    with open(p, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = (row["name"] or "").strip().lower()
            r = (row.get("roots") or "").strip()
            if n and r:
                out[n] = r
    return out


def fetch_all(words):
    """分批取全，撞 429 就退避重试——上一版静默丢批，只取到 1/4 就当查不到。"""
    todo = [w for w in words
            if not (P.CACHE / (urllib.parse.quote(w, safe="") + ".txt")).exists()]
    for attempt in range(6):
        if not todo:
            break
        print(f"  取 wikitext 第 {attempt + 1} 轮：{len(todo)} 词")
        P.fetch(todo)
        todo = [w for w in todo
                if not (P.CACHE / (urllib.parse.quote(w, safe="") + ".txt")).exists()]
        if todo:
            time.sleep(5 * (attempt + 1))
    if todo:
        print(f"  [warn] {len(todo)} 词始终没取到，按「无词源」处理：{todo[:8]}")


def wiki_roots(word, keys, sizes):
    """Wiktionary 侧：返回 (候选根列表, 拉丁/希腊词元列表)"""
    f = P.CACHE / (urllib.parse.quote(word, safe="") + ".txt")
    if not f.exists():
        return [], []
    ety = P.english_etymology(f.read_text(encoding="utf-8"))
    lms = P.lemmas(ety)
    if not lms:
        for b in P.base_words(ety):                      # 英语内部派生回溯基词
            bf = P.CACHE / (urllib.parse.quote(b, safe="") + ".txt")
            if bf.exists():
                lms = P.lemmas(P.english_etymology(bf.read_text(encoding="utf-8")))
                if lms:
                    break
    if not lms:
        return [], []
    return [r for r, _ in P.match(lms, keys, sizes)], [l for l, _ in lms]


def main():
    E = load_engra()
    words = json.loads((DATA / "words.json").read_text(encoding="utf-8"))["words"]
    roots = json.loads((DATA / "roots.json").read_text(encoding="utf-8"))["roots"]
    ref = {(w if isinstance(w, str) else (w.get("word") or w.get("lemma"))).lower()
           for w in json.loads((DATA / "english_reference.json").read_text(
               encoding="utf-8"))["words"]}
    ref = {w for w in ref if w}
    libroot = {w["id"]: (w.get("root_ids") or [None])[0] for w in words}
    keys = P.root_keys(roots)
    sizes = {r["id"]: len(r.get("word_ids") or []) for r in roots}
    cur = {r["id"]: sorted(r.get("word_ids") or []) for r in roots}

    byl = collections.defaultdict(list)
    for w, l in E.items():
        byl[l].append(w)

    # engra 标签 -> 库中根：靠该标签下已入库成员的 root_ids 投票，绕开命名差异
    mapped, cand = {}, {}
    for l, ws in byl.items():
        inlib = [w for w in ws if w in libroot]
        votes = collections.Counter(libroot[w] for w in inlib if libroot[w])
        if votes:
            strong = [r for r, c in votes.items() if c >= 2]
            if len(strong) < 2:
                mapped[l] = votes.most_common(1)[0]
        else:
            cand[l] = ws

    gaps = collections.defaultdict(list)
    for l, (rid, _) in mapped.items():
        for w in byl[l]:
            if w not in libroot and w in ref:
                gaps[rid].append(w)
    news = {l: [w for w in ws if w in ref] for l, ws in cand.items()
            if len([w for w in ws if w in ref]) >= 3}

    need = sorted({w for v in gaps.values() for w in v} |
                  {w for v in news.values() for w in v})
    print(f"需核验 {len(need)} 词")
    fetch_all(need)

    # ---- 一、现有根缺的词 ----
    tier = collections.Counter()
    lines = ["# 现有根缺失的考研词 —— engra × Wiktionary 双源交叉验证",
             "# 档位：AGREE=两源一致可直接派 / ENGRA_ONLY=需核 / NO_ETYM=非词源分组，建议剔除",
             "# 格式：根id <TAB> 档位 <TAB> 词 <TAB> Wiktionary 词元", ""]
    for rid in sorted(gaps, key=lambda r: -len(gaps[r])):
        ws = sorted(set(gaps[rid]))
        body = []
        for w in ws:
            cands, lms = wiki_roots(w, keys, sizes)
            if not lms:
                t = "NO_ETYM"
            elif rid in cands[:3]:
                t = "AGREE"
            else:
                t = "ENGRA_ONLY"
            tier[t] += 1
            body.append(f"{rid}\t{t}\t{w}\t{'/'.join(lms[:3])}")
        lines.append(f"# {rid}\t现有 {len(cur.get(rid, []))} 词\t缺 {len(ws)} 词")
        lines += body
        lines.append("")
    (D / "root_gaps_existing.txt").write_text("\n".join(lines), encoding="utf-8")

    # ---- 二、新根候选 ----
    out = ["# 新根候选 —— 该 engra 标签下无任何已入库成员，且考研词 >=3",
           "# 只保留「多数成员查得到拉丁/希腊祖先」的标签；其余是按语素/拼写聚的，已剔除",
           "# 格式：# engra标签 <TAB> 考研词数 <TAB> 最常见词元  然后逐词列出", ""]
    keep, drop = [], []
    for l, ws in sorted(news.items(), key=lambda kv: -len(kv[1])):
        rows, lem = [], collections.Counter()
        for w in sorted(ws):
            cands, lms = wiki_roots(w, keys, sizes)
            rows.append((w, lms, cands))
            for x in lms[:1]:
                lem[x] += 1
        have = sum(1 for _, lms, _ in rows if lms)
        if have * 2 < len(rows):                 # 过半查不到祖先 = 不是词源族
            drop.append((l, len(ws), have))
            continue
        keep.append((l, ws, lem, rows))
    out.append(f"# 保留 {len(keep)} 个标签，剔除 {len(drop)} 个非词源标签")
    out.append("")
    for l, ws, lem, rows in keep:
        top = "/".join(x for x, _ in lem.most_common(3))
        out.append(f"# {l}\t{len(ws)} 考研词\t{top}")
        for w, lms, cands in rows:
            hint = f"\t（Wiktionary 映射到已有根 {cands[0]}，可能不必新建）" if cands else ""
            out.append(f"{w}\t{'/'.join(lms[:3])}{hint}")
        out.append("")
    out.append("# ---- 剔除的非词源标签（过半成员查不到拉丁/希腊祖先）----")
    for l, n, have in sorted(drop, key=lambda x: -x[1]):
        out.append(f"# {l}\t{n} 词\t仅 {have} 个有词源")
    (D / "root_candidates_new.txt").write_text("\n".join(out), encoding="utf-8")

    print()
    print("=== 一、现有根缺失词 ===")
    print(f"  {len(gaps)} 个根 / {sum(len(set(v)) for v in gaps.values())} 个考研词")
    for t in ("AGREE", "ENGRA_ONLY", "NO_ETYM"):
        print(f"    {t:12} {tier[t]}")
    print("=== 二、新根候选 ===")
    print(f"  保留 {len(keep)} 个标签 / {sum(len(x[1]) for x in keep)} 词，"
          f"剔除 {len(drop)} 个非词源标签 / {sum(x[1] for x in drop)} 词")
    print()
    print("写出：drafts/root_gaps_existing.txt、drafts/root_candidates_new.txt")


if __name__ == "__main__":
    main()
