#!/usr/bin/env python3
"""量门二的精度与召回，两组对照都用库内已挂根的词当标注集。

    python scripts/measure_gate2.py                    # 量当前工作树版本
    python scripts/measure_gate2.py --script _screen_head.py   # 量指定版本

【为什么要有这个脚本】
改门二时我凭手跑的零散命令报过一批数字，其中有的根本没跑出来。把测量固化成
脚本，谁都能复现，也就没有「我记得是 22 条」这种东西。

【两组对照，缺一不可】
  伪报组 declared.tsv —— 把已挂对根的词按补词行写出（第 5 列填真实根）。
      门二会跳过词自己声明的那个根，所以**任何** REVIEW 都是伪报。
      这一组量的是精度。
  召回组 stripped.tsv —— 同一批词，第 5、6 列留空，伪装成孤立词条。
      门二必须报出来，而且必须报**对**根。这一组量的是召回。
只看伪报组会把门改哑（键删干净了自然一条不报）；只看召回组会放任噪声。

【为什么还要跑真实批次】
控制样本全是词根型词，而真实批次里孤立词占多数——古英语词形与拉丁词干同形
（leg/loc/man/stan 那类）只在后者身上撞。只按控制样本调参数会调错方向。
"""
import argparse
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = Path(os.environ.get("TEMP", "/tmp"))


def load(n, k):
    return json.loads((ROOT / "data" / n).read_text(encoding="utf-8"))[k]


def row(w, declare):
    """拼一个 15 列 W 行。declare=False 时第 5、6 列留空（伪装孤立词条）。"""
    ex = (w.get("examples") or ["a b c d e.", "f g h i j."])[:2]
    while len(ex) < 2:
        ex.append("a b c d e.")
    return "\t".join([
        "W", w["id"], w.get("pos") or "noun", w.get("phonetic") or "/x/",
        "/".join(w["root_ids"]) if declare else "",
        (w.get("root_logic") or "x") if declare else "",
        w.get("origin") or "", w.get("native_definition") or "x",
        w.get("core_image") or "画面", "/".join(w.get("chinese") or ["x"]),
        " | ".join(ex), w.get("core_concept") or "x – y",
        " | ".join(w.get("semantic_expansions") or []), "", ""])


def build_controls(n):
    words = load("words.json", "words")
    pool = [w for w in words if w.get("root_ids") and w.get("origin")]
    random.seed(42)
    sample = random.sample(pool, min(n, len(pool)))
    truth = {w["id"]: list(w["root_ids"]) for w in sample}
    for name, dec in (("declared", True), ("stripped", False)):
        p = TMP / f"g2_{name}.tsv"
        p.write_text("".join(row(w, dec) + "\n" for w in sample),
                     encoding="utf-8", newline="")
    return truth


def run(script, tsv):
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / script),
                          str(tsv)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    hits = {}
    for line in (out.stdout or "").splitlines():
        m = re.search(r"^\s+(\S+)\s+→ 词根 (\S+)（origin 里出现 '([^']+)'）", line)
        if m:
            hits[m.group(1)] = (m.group(2), m.group(3))
    return hits, out.stdout or "", out.stderr or ""


def blind_roots(script):
    """哪些根一个匹配键都没有——门二对它们结构上不可能报出漏挂。
    直接把脚本的 forms 构造逻辑跑一遍太绕，改用它的 [info] 反推不可靠，
    所以这里独立实现一遍，与脚本里的常量保持同步（改脚本时这里也要改）。"""
    src = (ROOT / "scripts" / script).read_text(encoding="utf-8")
    floor = 4 if "len(c) >= 4" in src else 5
    stop = set(re.findall(r'"([a-z]{2,})"',
                          src.split("STOP = {")[1].split("}")[0]))
    pat = re.compile(r"\b([a-z][a-z]{3,})\b")
    out = []
    for r in load("roots.json", "roots"):
        dec = {c for c in ({r["id"], r.get("root", "")}
                           | set(r.get("variants") or []))
               if c and len(c) >= floor and c.isalpha() and c not in stop}
        dec -= set(r.get("noisy_variants") or [])
        har = {c for c in pat.findall(r.get("origin") or "")
               if len(c) >= 5 and c not in stop}
        if not (dec | har):
            out.append((r["id"], len(r.get("word_ids") or [])))
    return sorted(out, key=lambda x: -x[1]), floor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default="screen_draft_etymology.py")
    ap.add_argument("-n", type=int, default=400, help="控制样本词数")
    ap.add_argument("--chunks", nargs="*",
                    default=["g_chunk106.tsv", "g_chunk107.tsv",
                             "g_chunk108.tsv", "g_chunk109.tsv"])
    a = ap.parse_args()

    truth = build_controls(a.n)
    print(f"# 被测脚本 {a.script}，控制样本 {len(truth)} 词\n")

    spur, _, err = run(a.script, TMP / "g2_declared.tsv")
    if err.strip():
        print("[stderr]", err.strip()[:300])
    print(f"精度（伪报组：已挂对根，任何 REVIEW 都是伪报）")
    print(f"    伪报 {len(spur)} 条 / {len(truth)} 词")
    for w, (rid, key) in sorted(spur.items()):
        print(f"      {w:14} → {rid:18} 键 {key!r}  真实 {truth[w]}")

    rec, _, _ = run(a.script, TMP / "g2_stripped.tsv")
    ok = sum(1 for w, (rid, _) in rec.items() if rid in truth.get(w, []))
    wrong = {w: (rid, truth[w]) for w, (rid, _) in rec.items()
             if rid not in truth.get(w, [])}
    print(f"\n召回（召回组：剥掉 root_ids，须报出且报对根）")
    print(f"    报出 {len(rec)} / {len(truth)}，其中报对根 {ok}，报错根 {len(wrong)}")
    if rec:
        print(f"    报出的里面报对的占 {ok/len(rec)*100:.1f}%")
    for w, (got, real) in sorted(wrong.items())[:10]:
        print(f"      报错 {w:14} → {got}（真实 {real[0]}）")

    print(f"\n真实批次（孤立词占多数，短词干撞名主要在这里）")
    for c in a.chunks:
        p = ROOT / "drafts" / c
        if not p.exists():
            print(f"    {c:18} 不存在，跳过")
            continue
        h, _, _ = run(a.script, p)
        detail = "，".join(f"{w}→{r}" for w, (r, _) in sorted(h.items()))
        print(f"    {c:18} {len(h)} 条" + (f"：{detail}" if h else ""))

    b, floor = blind_roots(a.script)
    tot = sum(n for _, n in b)
    print(f"\n失明的根（一个匹配键都没有，下限={floor}）：{len(b)} 个，"
          f"共辖 {tot} 词")
    for rid, n in b:
        print(f"      {rid:22} {n} 员")
    return 0


if __name__ == "__main__":
    sys.exit(main())
