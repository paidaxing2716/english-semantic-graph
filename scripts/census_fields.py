#!/usr/bin/env python3
"""字段普查：不预设查什么，量每个字段的值分布，让异常自己浮出来。

    python scripts/census_fields.py               # 全量报告
    python scripts/census_fields.py --field pos   # 只看某字段

【为什么要这个】
audit_all.py 查的是**已经有人想到要查**的东西。它报 critical 0 只说明「已知的那几类
没命中」，不说明干净。2026-09 一轮里四类缺陷全是撞上的，不是查出来的：

  59 条模板例句     随手看 suspicious.tsv 的分类才发现
  193 条美式音标    去查余下 7 条的判语才发现
  tentative 词性错  写内容时顺眼看到
  stern/till/tire   核画面时才发现画面指向另一个同形异源词

这四类里前两类是**分布异常**——同一个模板串出现 59 次、同一种记法在 114 条上与另一种
记法的 119 条并存。分布异常不需要预先知道「要找什么」就能看见，这就是普查的用处。

【报什么】
每个字段报四样，每一样都是能直接看出异常的形态：

  覆盖    有值 / 空 / 缺字段。空值集中在某一段字母 = 某次生成漏灌
  重复值  同一个值出现 N 次。N 大 = 模板串或复制粘贴
  长度    分位数与两端极值。极短极长都是可疑
  形态    值里出现的字符类别与可疑记法。两种记法数量相当 = 口径不统一

**普查只报数，不判对错。** 判对错要看规格，那是人的事。报出来的东西多数是合法的，
少数不是——这正是它的用法：把 5248 条压成几十行可读的分布，人扫一眼就知道哪儿反常。
"""
import argparse
import collections
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# 报重复值时，出现次数达到这个数才算异常。2 次可能是巧合（近义词共用释义），
# 3 次以上基本是模板或复制粘贴。
DUP_MIN = 3
# 每个字段最多列几条重复值、几条极值
TOP = 6


def flat(v):
    """把字段值压成可比较的字符串。列表按 | 连接——列表型字段的重复要连整个列表一起看，
    只看单个元素会把「两个词共用一句例句」和「整批共用同一对例句」混为一谈。"""
    if v is None:
        return None
    if isinstance(v, list):
        return "|".join(str(x) for x in v)
    return str(v)


def census(words, field):
    vals, empty, missing = [], 0, 0
    for w in words:
        if field not in w:
            missing += 1
            continue
        s = flat(w[field])
        if s is None or not s.strip():
            empty += 1
            continue
        vals.append((w["id"], s))
    return vals, empty, missing


def report_field(words, field):
    vals, empty, missing = census(words, field)
    n = len(words)
    print(f"\n{'─'*74}\n{field}")
    print(f"  覆盖   有值 {len(vals)}  空值 {empty}  无此字段 {missing}  （共 {n}）")
    if not vals:
        return

    # 空值集中在哪几个字母段——某次生成漏灌会在字母上聚堆
    if empty or missing:
        blanks = [w["id"] for w in words
                  if field not in w or not (flat(w.get(field)) or "").strip()]
        head = collections.Counter(x[0] for x in blanks)
        print(f"  空值首字母 {dict(sorted(head.items(), key=lambda kv: -kv[1])[:8])}")

    # 重复值：同一个值出现多次
    c = collections.Counter(s for _, s in vals)
    dups = [(s, k) for s, k in c.items() if k >= DUP_MIN]
    if dups:
        dups.sort(key=lambda x: -x[1])
        tot = sum(k for _, k in dups)
        print(f"  重复值 {len(dups)} 种，覆盖 {tot} 条（阈值 ≥{DUP_MIN} 次）")
        by = collections.defaultdict(list)
        for wid, s in vals:
            by[s].append(wid)
        for s, k in dups[:TOP]:
            print(f"    {k:4}× {s[:58]}")
            print(f"          {' '.join(by[s][:7])}{' …' if k > 7 else ''}")
    else:
        print(f"  重复值 无（阈值 ≥{DUP_MIN} 次）")

    # 长度分布与两端
    L = sorted(len(s) for _, s in vals)
    q = statistics.quantiles(L, n=10) if len(L) > 10 else [L[0], L[-1]]
    print(f"  长度   最短 {L[0]}  十分位 {int(q[0])}  中位 {int(statistics.median(L))}"
          f"  九分位 {int(q[-1])}  最长 {L[-1]}")
    ex = sorted(vals, key=lambda x: len(x[1]))
    print(f"    最短：{'  '.join(f'{w}({len(s)})' for w, s in ex[:4])}")
    print(f"    最长：{'  '.join(f'{w}({len(s)})' for w, s in ex[-4:])}")

    # 形态：字符类别构成
    kinds = collections.Counter()
    for _, s in vals:
        if re.search(r"[一-鿿]", s):
            kinds["含中文"] += 1
        if re.search(r"[A-Za-z]", s):
            kinds["含拉丁字母"] += 1
        if re.search(r"[ɑɒəɜɪʊʌæðŋʃʒθˈˌː]", s):
            kinds["含 IPA 符号"] += 1
        if re.search(r"\d", s):
            kinds["含数字"] += 1
        if "(" in s or "（" in s:
            kinds["含括号"] += 1
    if kinds:
        print(f"  形态   {dict(kinds)}")


def notation_split(words):
    """记法并存检查：同一件事有两种写法且数量相当，说明口径没统一。

    这是普查里唯一带判断的一节，因为「两种写法」得先知道哪两种成对。列表是踩出来的：
    2026-09 查出 (r) 记法 119 条与裸儿化 r 114 条并存——数量相当，靠占比判不出谁对，
    只能回去看规格（文档明写非儿化）。这类对子加进来，下次一眼就看得见。
    """
    print(f"\n{'─'*74}\n记法并存（两种写法数量相当 = 口径未统一，不是「异类 vs 约定」）")
    pairs = [
        ("音标 (r) 连读记法", lambda p: "(r)" in p,
         "音标裸儿化 r", lambda p: bool(re.search(r"r(?=[bdfɡhjklmnpstvwzðŋʃʒθ])|r/$", p)) and "(r)" not in p),
        ("音标含 ɒ", lambda p: "ɒ" in p,
         "音标含 ɑː", lambda p: "ɑː" in p),
        ("音标含 əʊ", lambda p: "əʊ" in p,
         "音标含 oʊ", lambda p: "oʊ" in p),
    ]
    for na, fa, nb, fb in pairs:
        a = [w["id"] for w in words if fa(w.get("phonetic") or "")]
        b = [w["id"] for w in words if fb(w.get("phonetic") or "")]
        if not a and not b:
            continue
        flag = ""
        if a and b:
            r = min(len(a), len(b)) / max(len(a), len(b))
            flag = "  ← 数量相当，需按规格定夺" if r > 0.3 else "  ← 少数派多半是错的"
        print(f"  {na} {len(a)}  ｜  {nb} {len(b)}{flag}")
        if b and len(b) <= 8:
            print(f"      少数派：{' '.join(b)}")

    # pos 写法。只查空格，**不要查顺序**——见下。
    sp = [w["id"] for w in words if " / " in (w.get("pos") or "")]
    ns = [w["id"] for w in words if "/" in (w.get("pos") or "") and " / " not in w["pos"]]
    print(f"  pos「noun / verb」带空格 {len(sp)}  ｜  「noun/verb」无空格 {len(ns)}"
          f"{'  ← 少数派' if ns else ''}")
    if ns and len(ns) <= 8:
        print(f"      少数派：{' '.join(ns)}")
    print("  pos 顺序（noun / verb 520 条 vs verb / noun 240 条）**不是口径不统一**：")
    print("    顺序编码的是哪个词性为主。verb / noun 那批是 reform contract permit")
    print("    conduct import export——主要是动词；noun / verb 那批是 figure position")
    print("    point limit factor——主要是名词。别按「统一格式」批量改，那会毁掉信息。")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--field", action="append", help="只查这些字段，可重复")
    a = ap.parse_args()

    db = json.loads((DATA / "words.json").read_text(encoding="utf-8"))
    words = db["words"]

    # 字段清单从数据里现取，不写死——写死会漏掉后来加的字段，那正是普查该避免的
    seen = collections.Counter()
    for w in words:
        for k in w:
            seen[k] += 1
    fields = a.field or [k for k, _ in seen.most_common()]

    print(f"字段普查：{len(words)} 词条，{len(seen)} 个字段")
    print(f"字段出现次数：{dict(seen.most_common())}")
    for f in fields:
        report_field(words, f)
    if not a.field:
        notation_split(words)


if __name__ == "__main__":
    main()
