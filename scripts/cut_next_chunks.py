#!/usr/bin/env python3
"""从「考研表未入库」里切下一批可派的片子，带 engra × Wiktionary 双源档位。

    python scripts/cut_next_chunks.py --start 107 --n 2 --size 30

【为什么要有这个脚本】
前 106 片的输入靠手写档位清单，每次派发前要人肉查 engra + Wiktionary + roots.json。
这个活完全是机械的，且手写时踩过两次坑：派了已入库的词（第六坑），以及同一个词
在两片里被判给不同根（chunk_agree_gaps 里记的 universal 撞车）。本脚本把两件事
都做成程序判据。

【档位是线索不是结论】
实测单源匹配假阳性约 50%、假阴性约 29%（NEXT.md §2b）。所以：
    A 档 = 双源一致指向一个**库内已有**的根 —— 仍要核，只是先验高
    B 档 = 查到拉丁/希腊词元但映射不到库内根 —— 可能是「库里有根但匹配器没找到」
    C 档 = 查不到古典词元 —— 大概率日耳曼/孤立词条，但同样要自己判
档位写进文件头的警告里，派发指令必须原样带上。

【为什么不做拼写聚类】
项目已栽过多次（NEXT.md「别做」）。这里的族信息只来自 Wiktionary 词元，
拼写相似一概不合并。
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_etymology_coverage as P                      # noqa: E402
from build_root_gaps import load_engra                    # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
D = ROOT / "drafts"

HEADER = (
    "# 档位是**线索不是结论**。单源匹配实测假阳性约 50%、假阴性约 30%。两个方向都核。\n"
)


def library():
    """返回 (已占用词形, 根id集, 根变体→根id)。

    变体索引是必须的：regroup_pools_by_family 漏查 variants 那次，
    把已在库的词又派了一遍（NEXT.md 六处缺陷之三）。
    """
    words = json.loads((DATA / "words.json").read_text(encoding="utf-8"))["words"]
    taken = set()
    for w in words:
        taken.add(w["id"].lower())
        for v in (w.get("variants") or []):
            taken.add(v.lower())
    roots = json.loads((DATA / "roots.json").read_text(encoding="utf-8"))["roots"]
    rids = {r["id"] for r in roots}
    var2root = {}
    for r in roots:
        var2root[r["id"].lower()] = r["id"]
        for v in (r.get("variants") or []):
            if v.lower() not in (r.get("noisy_variants") or []):
                var2root.setdefault(v.lower(), r["id"])
    return taken, rids, var2root


def already_dispatched():
    """扫所有已派输入与已出草稿，避免重复派发。"""
    seen = {}
    for pat in ("g_chunk*.txt", "rt_chunk*.txt", "cl_chunk*.txt"):
        for f in sorted(D.glob(pat)):
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("#") or not line.strip():
                    continue
                w = line.split("#")[0].strip().split("\t")[0].strip().lower()
                if w:
                    seen.setdefault(w, f.name)
    for pat in ("g_chunk*.tsv", "r_chunk*.tsv", "batch*.tsv"):
        for f in sorted(D.glob(pat)):
            for line in f.read_text(encoding="utf-8").splitlines():
                p = line.split("\t")
                if len(p) > 1 and p[0] == "W":
                    seen.setdefault(p[1].strip().lower(), f.name)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True, help="片号起点")
    ap.add_argument("--n", type=int, default=2, help="切几片（中转站上限 2 路）")
    ap.add_argument("--size", type=int, default=30, help="每片词数")
    a = ap.parse_args()

    taken, rids, var2root = library()
    dispatched = already_dispatched()

    ref = json.loads((DATA / "english_reference.json").read_text(
        encoding="utf-8"))["words"]
    if isinstance(ref, dict):
        ref = list(ref.keys())

    # 不可结构化的词：冠词、裸代词、基数词、系动词、情态动词。
    # 判据取自 skipped_function_words.txt 自己的结论——「有没有可教的搭配或画面」，
    # 不是「是不是功能词」。about/between/against 有型式，收了；a/the/five 没有。
    # 这份名单是**穷举**而非规则：拿前缀或词长当规则会把 house、hold 一起吃掉。
    UNSTRUCTURABLE = {
        "a", "an", "the", "all", "and", "any", "at", "be", "being", "been",
        "both", "but", "by", "can", "could", "do", "does", "did", "each",
        "few", "for", "he", "her", "here", "him", "his", "i", "if", "in",
        "is", "it", "its", "may", "me", "might", "must", "my", "no", "not",
        "of", "on", "one", "or", "our", "she", "shall", "should", "so",
        "some", "such", "than", "that", "their", "them", "then", "there",
        "these", "they", "this", "those", "to", "us", "very", "was", "we",
        "were", "what", "when", "where", "which", "who", "whom", "whose",
        "will", "with", "would", "you", "your",
        # 基数词与序数词：没有画面，也不成族
        "first", "second", "third", "five", "four", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "twenty", "thirty", "forty",
        "fifty", "hundred", "thousand", "million", "billion", "zero",
    }

    pool = []
    skip_dispatched = skip_unstruct = 0
    for w in ref:
        lw = w.lower()
        if lw in taken:
            continue
        if " " in w or "-" in w:
            continue          # orphan_hold.txt：多词条目还没有规格约定
        if lw in UNSTRUCTURABLE:
            skip_unstruct += 1
            continue
        if lw in dispatched:
            skip_dispatched += 1
            continue
        pool.append(w)

    print(f"待办池 {len(pool)} 词"
          f"（剔除：已入库 / 不可结构化 {skip_unstruct} / 已派未合 {skip_dispatched}"
          f" / 多词条目）")

    need = a.n * a.size
    batch = pool[:need]
    print(f"本轮取前 {len(batch)} 词：{batch[0]} … {batch[-1]}")

    engra = load_engra()
    roots = json.loads((DATA / "roots.json").read_text(encoding="utf-8"))["roots"]
    keys = P.root_keys(roots)
    sizes = {r["id"]: len(r.get("word_ids") or []) for r in roots}

    wiki = P.fetch(batch)
    if len(wiki) < len(batch):
        # 429 那次异常分支静默跳过了整批，算出个假的 3.3%（NEXT.md 记的坑）
        print(f"[warn] 只取回 {len(wiki)}/{len(batch)} 个词条，档位会偏 C；"
              f"重跑本脚本可续取（缓存已落盘）")

    rows = []
    for w in batch:
        lw = w.lower()
        ety = P.english_etymology(wiki.get(w, "") or wiki.get(lw, ""))
        lems = P.lemmas(ety) if ety else []
        lem = lems[0][0] if lems else ""

        # 双源：Wiktionary 词元经 match 映射到库内根，与 engra 直接给的根名
        by_lemma = ""
        if lems:
            cands = P.match(lems, keys, sizes)
            if cands:
                by_lemma = cands[0][0]
        eng = (engra.get(lw) or "").strip().lower()
        by_engra = var2root.get(eng, "") if eng else ""

        if by_lemma and by_engra and by_lemma == by_engra:
            tier, guess = "A", by_lemma
        elif by_lemma or by_engra:
            tier, guess = "A", (by_lemma or by_engra)
        elif lem:
            tier, guess = "B", ""
        else:
            tier, guess = "C", ""
        rows.append((tier, w, lem, guess))

    order = {"A": 0, "B": 1, "C": 2}

    # 族整体不跨片。chunk_agree_gaps 定的规矩：同族词在同一个代理手里，写
    # root_logic 时才看得到全族。首轮切完出过 illustrate（C 档 108）与
    # illustration（B 档 107）分家——同族分给两个代理，且档位还不一致。
    # 族键取「猜到的根」优先，其次词元词干，最后英文前 5 字母兜底
    # （install/installation/installment 靠这一层才聚得起来）。
    # 英文词干比拉丁词元更适合当**路由**键：同族的词元会分叉
    # （imitate←imitor 与 imitation←imitacion 词干不同，illustrate 干脆没取到词元），
    # 而英文派生后缀是规则的。
    #
    # 这不违反「别自动归族」那条——那条说的是别拿拼写**定词根归属**。这里只决定
    # 哪些词进同一个代理的视野：合错了无代价（多看两个词），拆错了代理就看不到全族。
    # 判据不同，所以可以用拼写。
    SUF = ("ational", "ization", "ication", "ation", "ition", "ment", "ance",
           "ence", "ible", "able", "ical", "ious", "ive", "ate", "ant", "ent",
           "ous", "ing", "ion", "ity", "al", "ic", "ly", "ed", "es", "y", "s")

    def estem(w):
        s = w.lower()
        for _ in range(2):                  # installation → installat → install
            for suf in SUF:
                if s.endswith(suf) and len(s) - len(suf) >= 4:
                    s = s[:-len(suf)]
                    break
            else:
                break
        return s.rstrip("aeiou") if len(s) > 5 else s

    def famkey(row):
        tier, w, lem, guess = row
        # 猜到同一个根的必须同片；否则按英文词干
        return f"r:{guess}" if guess else f"e:{estem(w)}"

    fams = collections.defaultdict(list)
    for r in rows:
        fams[famkey(r)].append(r)

    # 后缀剥完仍可能差一个尾辅音（horizon vs horizontal→horizont），再做一轮
    # 前缀并合：短干是长干的前缀且 ≥5 字母就并。5 字母下限是为了不把 inter- 这类
    # 前缀并成一族——interpret 与 interest 互不为前缀，不受影响。
    ekeys = sorted((k for k in fams if k.startswith("e:")), key=len)
    merged = {}
    for i, short in enumerate(ekeys):
        s = short[2:]
        if len(s) < 5 or short in merged:
            continue
        for long in ekeys[i + 1:]:
            if long not in merged and long[2:].startswith(s):
                merged[long] = short
    for long, short in merged.items():
        fams[short].extend(fams.pop(long))
    # 族内按档位排，族之间按「最好档位 → 族大小降序」排，大族先落片
    groups = []
    for k, members in fams.items():
        members.sort(key=lambda r: (order[r[0]], r[1]))
        best = min(order[m[0]] for m in members)
        groups.append((best, -len(members), k, members))
    groups.sort()

    # 贪心装箱：每次投进当前最空的片，档位因此自然摊开到各片
    bins = [[] for _ in range(a.n)]
    for _, _, _, members in groups:
        bins.sort(key=len)
        bins[0].extend(members)

    for i in range(a.n):
        part = sorted(bins[i], key=lambda r: (order[r[0]], r[1]))
        if not part:
            break
        out = D / f"g_chunk{a.start + i}.txt"
        lines = [HEADER]
        cur = None
        for tier, w, lem, guess in part:
            if tier != cur:
                cur = tier
                lines.append({
                    "A": "## A 档：疑可挂现有根 —— 核对成立按补词写；不成立退回 B/C 并说明\n",
                    "B": "## B 档：借词但匹配器没找到根 —— **没找到 ≠ 没有**，自己查 roots.json\n",
                    "C": "## C 档：查不到古典词元 —— 多为孤立/日耳曼型，但仍自己判\n",
                }[tier])
            g = f"疑 → {guess}" if guess else "疑 → "
            lines.append(f"{w}\t# 词元 {lem or '—'}\t{g}\n")
        out.write_text("".join(lines), encoding="utf-8")
        c = collections.Counter(t for t, *_ in part)
        print(f"  {out.name}: {len(part)} 词  A{c['A']} B{c['B']} C{c['C']}")


if __name__ == "__main__":
    main()
