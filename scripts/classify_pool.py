#!/usr/bin/env python3
"""把未处理的词按「该走词根批还是日耳曼批」粗分，并用库内已标注词条自评精度。

【为什么要分】
子代理拿到混着两类的片子时，判定成本比写词条本身还高：日耳曼片里混进拉丁词，
它得查族、判成员数、写进 skipped_chunkNN.txt，这一轮白写。实测按字母段的
跳过率极不均匀——a 段 0–10%，c 段 50%，e 段 53%（诺曼法语借词聚在那儿）。
先分一遍能把跳过率压下来。

【为什么可以用启发式，不必让代理逐词判词源】
分错是自纠的：日耳曼片的规格本来就要求「属于真词族的词跳过并列进
skipped_chunkNN.txt」，反之词根片凑不足 3 个成员的也会按日耳曼型写。
所以这里不需要判对，只需要把跳过率压到可接受——故用启发式，别花代理的钱。

【为什么先自评】
库里 2584 条已有 decomposable 标注（root / germanic），正是本脚本要预测的那
两类。所以可以直接量精度，不必猜。跑 --eval 看分数。
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 古典（拉丁/希腊）前缀。只收「后面还剩得下词干」的，避免 in- 吃掉 industry。
CLASSICAL_PREFIX = (
    "ab", "abs", "ad", "ante", "anti", "bene", "bi", "circum", "com", "con", "col",
    "cor", "contra", "counter", "de", "dis", "dif", "equi", "ex", "extra", "in", "im",
    "il", "ir", "inter", "intra", "intro", "male", "multi", "ob", "oc", "of", "op",
    "per", "peri", "post", "pre", "pro", "re", "retro", "se", "semi", "sub", "suc",
    "suf", "sug", "sup", "sur", "sus", "super", "trans", "tri", "ultra", "vice",
    # 希腊。注意不收 a-／an-：希腊否定前缀 a- 只在 atypical 这类里成立，
    # 拿来当规则会把所有 a 开头的普通词吃掉——实测 96 命中只有 33.3% 判对，
    # 是全部规则里最差的一条。
    "amphi", "ana", "apo", "auto", "cata", "dia", "dys", "endo",
    "epi", "eu", "exo", "hemi", "hyper", "hypo", "meta", "mono", "para", "poly",
    "syn", "sym", "syl", "tele", "thermo",
)

# 古典后缀。这类是最强信号——日耳曼核心词几乎不带。
CLASSICAL_SUFFIX = (
    "ation", "ition", "ution", "tion", "sion", "ssion", "ance", "ence", "ancy",
    "ency", "ant", "ent", "ate", "ite", "ude", "tude", "ity", "ety", "ify", "fy",
    "ive", "ous", "eous", "ious", "ose", "ial", "ual", "ary", "ory", "ric",
    "ism", "ist", "ize", "ise", "able", "ible", "ment", "ure", "esce", "escent",
    "cide", "fer", "form", "gram", "graph", "logy", "meter", "metry", "nomy",
    "pathy", "phone", "phobia", "scope", "sophy", "tomy", "vore",
)

# 日耳曼构词法后缀，与上面对立。
GERMANIC_SUFFIX = ("ness", "ship", "hood", "dom", "ful", "less", "some", "ward",
                   "wards", "wise", "like", "th", "en", "ling", "kin")

# 只出现在古典借词里的字母组合。逐个量过精度后保留的（--eval 可复现）：
#   ct 96.7%（122 命中，最强）· pt 85.3% · xt 84.6% · sc+元音 81.2%
#   qu 75.8% · ph 75.0% · gn+元音 75.0%
# 剔掉的：ps / chr（各 1-2 命中，全判错）· mn 40% · 裸 x 70.3%（撞 box/tax/six）
CLASSICAL_CLUSTER = re.compile(r"(ct|pt|xt|sc[aeiou]|qu|ph|rh|gn[aeiou])")

# 只出现在日耳曼本土词里的组合。
GERMANIC_CLUSTER = re.compile(r"(^kn|^wr|^wh|^sw|^tw|^sh|^th|ght|ck|dge|tch|^y[aeiou])")


def load_root_variants():
    """收集已建模词根的变体，用于反查。noisy_variants 跳过（低区分度）。

    最短取 3。量过 2 的情形：词首命中 440→462（+22），精度 91.6%→87.9%。
    22 个新命中里只 3 个真，换来 3.7 个百分点的精度损失，不值。
    2 字母变体全表是 ag / fy / gn / ig / it / li / ly / re / vi——除 ag 外
    都太泛，撞什么都算命中。代价是 agent（ag 族）这类会落进日耳曼批，
    由 skipped 机制兜住。
    """
    p = ROOT / "data" / "roots.json"
    if not p.exists():
        return {}
    out = {}
    for r in json.loads(p.read_text(encoding="utf-8"))["roots"]:
        noisy = {v.lower() for v in (r.get("noisy_variants") or [])}
        for v in [r["id"]] + (r.get("variants") or []):
            v = v.lower()
            if len(v) >= 3 and v not in noisy:
                out.setdefault(v, r["id"])
    return out


_VARIANTS = None


def classify(w):
    """返回 (类别, 依据)。类别 ∈ {latin, germanic, uncertain, phrase}"""
    global _VARIANTS
    if _VARIANTS is None:
        _VARIANTS = load_root_variants()

    s = w.lower()
    if " " in s or "-" in s:
        return "phrase", "多词/连字符"

    for suf in sorted(CLASSICAL_SUFFIX, key=len, reverse=True):
        if s.endswith(suf) and len(s) - len(suf) >= 3:
            return "latin", f"-{suf}"

    # 反查已建模词根的变体，且只认词首命中。
    # 这一条专治长度规则看不见的那类：admit / state / part / sign / place / pass
    # 全是 5 字母以内的拉丁词——诺曼法语把拉丁词形缩短了，所以短，但词根都在库里。
    # 只认词首是因为词中命中噪声最大（find_root_members.py 同一结论）。
    # 变体最短取 3 而不是 4：cap（caput）、cas（cadere）、cur（currere）都是 3 字母，
    # 卡 4 就把 cap / cape / case / curve 这批全漏了。长度从来不是这里的正确筛子
    # （cip 3 字母很准，lat 3 字母 17% 准），区分度由 noisy_variants 显式标注。
    # 余部限 3 字母以内：防 cat- 吃掉 catalog 这类。
    for v, rid in sorted(_VARIANTS.items(), key=lambda x: -len(x[0])):
        if len(v) >= 3 and s.startswith(v) and len(s) - len(v) <= 3:
            return "latin", f"词首={v}（{rid}）"

    for suf in GERMANIC_SUFFIX:
        if s.endswith(suf) and len(s) - len(suf) >= 3:
            return "germanic", f"-{suf}（日耳曼构词）"

    if GERMANIC_CLUSTER.search(s):
        return "germanic", "本土字母组合"

    if CLASSICAL_CLUSTER.search(s):
        return "latin", "古典字母组合"

    for p in sorted(CLASSICAL_PREFIX, key=len, reverse=True):
        if s.startswith(p) and len(s) - len(p) >= 4:
            return "latin", f"{p}-"

    # 兜底看长度。阈值不是猜的——库内 2583 条已标注词按长度统计：
    #   ≤5 字母   真 latin 占 6–26%   → 判 germanic
    #   6–8 字母  真 latin 占 43–63%  → 掷硬币，判了就是 20% 错误率的来源，故弃权
    #   ≥9 字母   真 latin 占 100%（397/397，无一例外）→ 判 latin
    if len(s) >= 9:
        return "latin", "≥9 字母"
    if len(s) <= 5:
        return "germanic", "≤5 字母"
    return "uncertain", "6-8 字母无标记"


def evaluate():
    """用库内 decomposable 标注量精度。root ↔ latin，germanic ↔ germanic。"""
    words = json.loads((ROOT / "data" / "words.json").read_text(encoding="utf-8"))["words"]
    truth = {}
    for w in words:
        d = w.get("decomposable")
        if d == "root":
            truth[w["id"]] = "latin"
        elif d == "germanic":
            truth[w["id"]] = "germanic"

    stat = {}
    conf = {("latin", "latin"): 0, ("latin", "germanic"): 0,
            ("germanic", "latin"): 0, ("germanic", "germanic"): 0}
    unc = 0
    for wid, t in truth.items():
        p, why = classify(wid)
        if p in ("uncertain", "phrase"):
            unc += 1
            continue
        conf[(p, t)] = conf.get((p, t), 0) + 1
        k = (p, why)
        stat.setdefault(k, [0, 0])
        stat[k][0] += 1
        stat[k][1] += (p == t)

    n = sum(conf.values())
    acc = (conf[("latin", "latin")] + conf[("germanic", "germanic")]) / n
    print(f"自评：库内已标注 {len(truth)} 词，判定出 {n} 词（{unc} 词无标记）")
    print(f"总体准确率 {acc*100:.1f}%\n")
    print("             真 latin  真 germanic")
    print(f"  判 latin      {conf[('latin','latin')]:>6}    {conf[('latin','germanic')]:>8}")
    print(f"  判 germanic   {conf[('germanic','latin')]:>6}    {conf[('germanic','germanic')]:>8}")
    pl = conf[("latin", "latin")] / max(1, conf[("latin", "latin")] + conf[("latin", "germanic")])
    pg = conf[("germanic", "germanic")] / max(1, conf[("germanic", "germanic")] + conf[("germanic", "latin")])
    print(f"\n  判 latin 的精度    {pl*100:.1f}%")
    print(f"  判 germanic 的精度 {pg*100:.1f}%")

    print("\n各依据的表现（命中数 / 其中判对）：")
    for (p, why), (tot, hit) in sorted(stat.items(), key=lambda x: -x[1][0])[:18]:
        print(f"  {p:<9} {why:<22} {tot:>5}  {hit/tot*100:>5.1f}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", action="store_true", help="用库内标注自评精度")
    ap.add_argument("-i", "--infile", help="待分类词表，一行一词")
    ap.add_argument("--outdir", default="drafts", help="输出目录")
    a = ap.parse_args()

    if a.eval:
        evaluate()
        return 0

    if not a.infile:
        ap.error("需要 -i 词表，或用 --eval")

    words = [l.strip() for l in Path(a.infile).read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    buckets = {}
    for w in words:
        c, why = classify(w)
        buckets.setdefault(c, []).append((w, why))

    outdir = Path(a.outdir)
    for c, items in sorted(buckets.items()):
        p = outdir / f"cls_{c}.txt"
        p.write_text("\n".join(w for w, _ in items) + "\n", encoding="utf-8")
        print(f"  {c:<10} {len(items):>5}  → {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
