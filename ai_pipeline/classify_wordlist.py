#!/usr/bin/env python3
"""统计词表中有多少词适合"词根拆解"这套方法。

方法：数据驱动的词族发现，而非比对手写词根表。
手写表永远不够全（试过，62% 落到"未归类"）。真正该问的不是
"这个词含不含某个词根"，而是"这个词根能不能撑起一个词族"——
只出现一次的词根没有教学价值。

做法：
1. 剥掉常见拉丁前缀/后缀，得到候选词干
2. 统计每个词干在词表中被多少个词共享
3. 词干被 >= MIN_FAMILY 个词共享，且该词本身带词缀 → 可拆
   （光有词干说明是词族的根，光有词缀但词干孤立说明拆了也没用）

输出的是数量级，用于回答"图谱密度该按多大规模设计"。

用法：
    python ai_pipeline/classify_wordlist.py <wordlist.txt> [-o report.json]
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

MIN_FAMILY = 3   # 词干至少被这么多词共享，才算能撑起词族

# 拉丁/希腊前缀。长的排前面，剥离时优先匹配。
PREFIXES = sorted([
    "circum", "contra", "counter", "intro", "intra", "inter", "retro", "trans", "ultra",
    "super", "hyper", "hypo", "multi", "mono", "poly", "para", "meta", "peri", "epi",
    "ante", "anti", "post", "pre", "pro", "sub", "suc", "suf", "sug", "sup", "sur",
    "sus", "dis", "dif", "com", "con", "col", "cor", "non", "mal", "mis", "obs", "occ",
    "off", "opp", "per", "syn", "sym", "abs", "ads", "ab", "ad", "af", "ag", "al", "an",
    "ap", "ar", "as", "at", "bi", "co", "de", "di", "ef", "em", "en", "ex", "il", "im",
    "in", "ir", "ob", "oc", "op", "re", "se", "tri", "un", "up",
], key=len, reverse=True)

# 派生后缀。同样长优先。
SUFFIXES = sorted([
    "ableness", "ibleness", "ification", "ationally", "iously", "eously",
    "ization", "isation", "ational", "ability", "ibility", "aneous",
    "ation", "ition", "ution", "ement", "ance", "ence", "ancy", "ency", "ical",
    "ious", "eous", "uous", "able", "ible", "ally", "ancy", "ette", "hood", "ical",
    "ious", "ise", "ish", "ism", "ist", "ite", "ity", "ive", "ize", "less", "like",
    "ment", "ness", "ory", "ous", "ship", "sion", "tion", "ual", "ure", "ward", "wise",
    "acy", "age", "ant", "ary", "ate", "dom", "ent", "ery", "ess", "ful", "ify",
    "ial", "ian", "ing", "ion", "ile", "ine", "ism", "ity", "ive", "ize",
    "al", "ar", "cy", "ed", "en", "er", "es", "ic", "ly", "or", "ty", "y", "s",
], key=len, reverse=True)

GERMANIC_CORE = set("""
get make take give go come put set let keep hold find leave bring stand
hand head heart foot eye ear mouth tooth hair bone blood skin body
water fire earth wind rain snow ice stone wood iron gold silver
house home door window wall floor roof room bed table chair
man woman child boy girl friend life death wife husband
day night year week month morning evening summer winter spring
good bad big small long short high low old new young little
work play walk run jump swim fly sit sleep wake eat drink
speak talk say tell ask answer hear listen see look watch read write
think know learn teach understand remember forget believe hope wish want need
love like hate fear feel laugh cry smile help
buy sell pay cost spend save lose win send
open shut break cut burn build grow fall rise ride drive
warm cold hot cool dry wet clean dirty full empty
back front side top bottom left right near far
king queen lord land field road bridge ship boat
milk bread meat fish egg salt corn apple
dog cat horse cow sheep bird tree grass leaf flower seed
sun moon star sky sea river hill mountain
word name song story book
strong weak quick slow soft hard heavy light deep wide narrow
""".split())

FUNCTION_WORDS = set("""
a an the this that these those i you he she it we they me him her us them
my your his its our their mine yours hers ours theirs
am is are was were be been being do does did done have has had
of to in on at by for with from into onto upon about
and or but nor so yet if then than as because although though while
not no yes very too also just only even still already always never
who whom whose which what when where why how
there here some any all both each every other another such
one two three four five six seven eight nine ten hundred thousand
none most more less least much many few
shall will should would can could may might must ought need dare
""".split())

LOANWORDS = set("""
tea coffee sofa typhoon karaoke tofu sushi kimono safari
bazaar caravan tobacco potato tomato chocolate banana coconut mango
piano opera solo tempo pizza balcony umbrella volcano
robot vodka tundra czar yacht boss cookie skate
alcohol algebra sugar syrup cotton lemon orange
jungle shampoo bungalow thug guru kindergarten waltz
ballet buffet cafe garage genre bureau plateau collage
tsunami origami manga khaki jazz
""".split())

PHRASAL_TAILS = {
    "up", "down", "off", "on", "in", "out", "away", "back", "over", "under",
    "through", "about", "after", "for", "with", "into", "to", "by", "from", "of",
}


def parse_line(line):
    line = line.strip()
    if not line:
        return None
    m = re.match(r"^([A-Za-z][A-Za-z\-' ]*?)\s*[\[/]", line)
    if m:
        return m.group(1).strip()
    m = re.match(r"^([A-Za-z][A-Za-z\-' ]*?)\s{2,}", line)
    return m.group(1).strip() if m else None


def strip_affixes(w):
    """剥前后缀，返回 (词干, 是否剥掉过东西)。"""
    stem = w
    affixed = False

    # 只在第一轮允许剥单字母后缀（s/y）。否则 extensive → extens → "exten"，
    # 词干被啃掉一截，整个词族就归错了。
    for round_i in range(2):
        for s in SUFFIXES:
            if len(s) == 1 and round_i > 0:
                continue
            if stem.endswith(s) and len(stem) - len(s) >= 3:
                stem = stem[: -len(s)]
                affixed = True
                break
        else:
            break

    for p in PREFIXES:
        if stem.startswith(p) and len(stem) - len(p) >= 3:
            stem = stem[len(p):]
            affixed = True
            break

    return stem, affixed


def normalize_stem(s):
    """吸收拼写变体，让同一词根的不同形态归到一起。
    如 ceiv/cept、mit/miss、duc/duct 在派生中互换。"""
    pairs = [
        ("ceiv", "cept"), ("ceipt", "cept"), ("miss", "mit"), ("mitt", "mit"),
        ("duct", "duc"), ("script", "scrib"), ("scrip", "scrib"),
        ("spect", "spec"), ("spic", "spec"), ("vers", "vert"),
        ("vis", "vid"), ("puls", "pel"), ("curs", "cur"), ("curr", "cur"),
        ("pens", "pend"), ("tens", "tend"), ("tent", "tain"), ("ten", "tain"),
        ("sens", "sent"), ("cess", "ced"), ("cid", "cad"), ("cis", "cid"),
        ("clus", "clud"), ("claus", "clud"), ("fect", "fac"), ("fic", "fac"),
        ("fess", "fat"), ("gress", "grad"), ("ject", "jac"), ("junct", "jug"),
        ("lect", "leg"), ("lig", "leg"), ("mot", "mov"), ("nounc", "nunc"),
        ("plic", "ply"), ("pos", "pon"), ("pound", "pon"), ("quis", "quir"),
        ("quest", "quir"), ("rupt", "rump"), ("sect", "sec"), ("secut", "sequ"),
        ("sist", "sta"), ("stit", "sta"), ("stat", "sta"), ("struct", "stru"),
        ("sumpt", "sum"), ("tact", "tang"), ("tract", "trah"), ("trus", "trud"),
        ("vas", "vad"), ("vent", "ven"), ("volut", "volv"), ("solut", "solv"),
        ("sorb", "sorpt"),
    ]
    for a, b in pairs:
        if s == a:
            return b
        if len(s) > len(a) and s.endswith(a):
            return s[: -len(a)] + b
    # 词尾单辅音重复、哑音 e
    s = re.sub(r"([bcdfgklmnprstvz])\1$", r"\1", s)
    s = re.sub(r"e$", "", s) if len(s) > 4 else s
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wordlist")
    ap.add_argument("-o", "--out")
    ap.add_argument("--min-family", type=int, default=MIN_FAMILY)
    a = ap.parse_args()

    raw, skipped = [], 0
    for line in Path(a.wordlist).read_text(encoding="utf-8", errors="replace").splitlines():
        w = parse_line(line)
        if w:
            raw.append(w)
        elif line.strip():
            skipped += 1

    seen, uniq = set(), []
    for w in raw:
        k = w.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(k)

    # 第一遍：建立词干 → 词 的映射
    stem_of, families = {}, defaultdict(set)
    for w in uniq:
        if " " in w or "-" in w or w in FUNCTION_WORDS or w in GERMANIC_CORE or w in LOANWORDS:
            continue
        stem, affixed = strip_affixes(w)
        stem = normalize_stem(stem)
        if len(stem) < 3:
            continue
        stem_of[w] = (stem, affixed)
        families[stem].add(w)

    # 第二遍：定类
    buckets = defaultdict(list)
    for w in uniq:
        if " " in w or "-" in w:
            parts = w.replace("-", " ").split()
            buckets["phrasal" if len(parts) >= 2 and parts[-1] in PHRASAL_TAILS
                    else "compound"].append(w)
            continue
        if w in FUNCTION_WORDS:
            buckets["function"].append(w)
            continue
        if w in GERMANIC_CORE:
            buckets["germanic"].append(w)
            continue
        if w in LOANWORDS:
            buckets["loanword"].append(w)
            continue

        info = stem_of.get(w)
        if not info:
            buckets["opaque"].append(w)
            continue
        stem, affixed = info
        fam = families[stem]
        if len(fam) >= a.min_family and affixed:
            buckets["decomposable"].append(w)
        elif len(fam) >= a.min_family:
            buckets["family_base"].append(w)   # 词族的裸词干，本身是那个"根"
        else:
            buckets["isolated"].append(w)

    total = len(uniq)
    LABEL = {
        "decomposable": "可拆 — 词缀 + 有词族的词根",
        "family_base": "词族基词 — 本身即该族的根",
        "isolated": "孤立词 — 拆了也无同族词可迁移",
        "germanic": "日耳曼核心词 — 本身即词根",
        "function": "功能词 — 不需记忆策略",
        "loanword": "借词/专名 — 拆解无认知价值",
        "phrasal": "短语动词 — 意义在介词隐喻",
        "compound": "复合词/多词条目",
        "opaque": "无法剥出词干",
    }

    print(f"词表：{a.wordlist}")
    print(f"唯一词条 {total} 个（跳过无法解析 {skipped} 行）")
    print(f"词族门槛：词干至少被 {a.min_family} 个词共享\n")
    print(f"{'类别':<30} {'数量':>6} {'占比':>7}")
    print("-" * 48)
    for k, n in Counter({k: len(v) for k, v in buckets.items()}).most_common():
        print(f"{LABEL[k]:<30} {n:>6} {n / total * 100:>6.1f}%")

    dec = len(buckets["decomposable"])
    base = len(buckets["family_base"])
    print("-" * 48)
    print(f"{'适用本方法（可拆 + 基词）':<30} {dec + base:>6} {(dec + base) / total * 100:>6.1f}%")

    # 最高产的词族
    big = sorted(families.items(), key=lambda kv: -len(kv[1]))[:18]
    print(f"\n最高产的词族（共 {sum(1 for f in families.values() if len(f) >= a.min_family)} 个达标词族）：")
    for stem, fam in big:
        print(f"  {stem:<9} {len(fam):>3} 词  {', '.join(sorted(fam)[:7])}")

    print("\n各类抽样：")
    for k in ["decomposable", "family_base", "isolated", "germanic", "opaque", "phrasal"]:
        if buckets[k]:
            print(f"  {k:<13} {', '.join(buckets[k][:8])}")

    if a.out:
        Path(a.out).write_text(json.dumps({
            "total": total,
            "min_family": a.min_family,
            "counts": {k: len(v) for k, v in buckets.items()},
            "applicable": dec + base,
            "applicable_ratio": round((dec + base) / total, 4),
            "qualified_families": {k: sorted(v) for k, v in families.items()
                                   if len(v) >= a.min_family},
            "buckets": {k: v for k, v in buckets.items()},
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n已写入 {a.out}")


if __name__ == "__main__":
    main()
