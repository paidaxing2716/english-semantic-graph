#!/usr/bin/env python3
"""测量：能否用 Wiktionary 词源数据自动判定「词属于哪个词根」。

不改任何数据，只测量。标注集用库里 1283 个已有 root_ids 的词——那是项目自己
写的标准答案，所以准确率是算出来的，不是肉眼判的。

    python scripts/probe_etymology_coverage.py            # 跑标注集
    python scripts/probe_etymology_coverage.py --pool     # 加测日耳曼池

wikitext 缓存在 drafts/.etym_cache/（gitignored），可反复跑不重复请求。
"""
import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE = ROOT / "drafts" / ".etym_cache"
API = "https://en.wiktionary.org/w/api.php"
UA = "english-semantic-graph-probe/0.1 (etymology coverage measurement)"

# 表示「继承／借入」的模板 = 真正的祖先链。cog（同源词）和 doublet 不是祖先，
# 必须排除：cognate 只说明平行关系，拿它当来源会把 sibling 误判成父代。
ANCESTRY = {"der", "inh", "bor", "lbor", "slbor", "obor", "uder", "calque",
            "cal", "clq", "learned borrowing", "semi-learned borrowing",
            "orthographic borrowing", "inherited", "derived", "borrowed"}
# 老式写法 {{etyl|la|en}} 之后紧跟 {{m|la|lemma}}，m 单独出现时算弱证据
MENTION = {"m", "mention", "l", "link"}
INTEREST = {"la", "grc", "la-med", "ML.", "LL."}   # 拉丁 / 古希腊
# 罗曼语中间站：figurative ← 中古法语 figuratif，词源段里根本没有拉丁模板，
# 但罗曼词形保留了拉丁词干，够用来定根，算弱证据
ROMANCE = {"fro", "frm", "xno", "fr", "it", "es", "pt", "ca", "oc", "roa-opt"}

# 拉丁前缀（含同化变体 ad→ac/af/ag…）。拉丁复合词是 前缀+词基，
# propono 里没有 ponere 的字样，必须先剥前缀再比词干，否则永远匹配不上。
LAT_PREFIX = sorted({
    "trans", "circum", "contra", "inter", "intro", "super", "supra", "subter",
    "sub", "suf", "sup", "sus", "ante", "post", "prae", "pre", "pro", "per",
    "retro", "re", "se", "de", "dis", "di", "ex", "ec", "in", "im", "il",
    "ir", "ob", "oc", "of", "op", "ad", "ac", "af", "ag", "al", "ap", "ar",
    "as", "at", "abs", "ab", "com", "con", "col", "cor", "co", "ne", "non",
    "bene", "male", "multi", "omni", "semi", "uni", "bi", "tri", "quasi",
    "ultra", "infra", "intra", "juxta", "cis", "extra", "sine", "vice",
    "amphi", "ana", "anti", "apo", "cata", "dia", "dys", "en", "endo", "epi",
    "eu", "exo", "hyper", "hypo", "meta", "para", "peri", "pros", "syn", "sym",
}, key=len, reverse=True)
# 单字符前缀（e-、a-）剥出来的多是垃圾：expres 去掉 e 变 xpres，白送一堆假匹配

# 词尾（长的先试），剥到只剩 >=3 字符为止。pendere→pend、forma→form、positio→posit
# 'sus'/'tus' 不能剥：expressus 会变 expres（丢了 press）、positus 变 pos（丢了 posit），
# 词基反而被切掉。只剥 'us'，让 express/posit 完整留下。
ENDINGS = ["issimus", "ationem", "ionem", "ation", "atus", "itus", "etus",
           "ator", "atio", "ion", "are", "ere", "ire", "ori", "ari", "tum",
           "ium", "ius", "eus", "if", "io", "is", "us", "um", "em", "er",
           "or", "on", "o", "a", "e"]
# 英语内部派生：figurative = figure + -ative，词源段里没有拉丁模板，
# 但基词往往已在库里挂好根，直接继承即可
AFFIX = {"af", "affix", "suffix", "prefix", "com", "compound", "confix", "sur"}
TREE = {"ety", "etymon"}            # 新版树状词源模板，整条链在一个模板里

# 拉丁前缀／介词会作为独立模板出现（{{der|en|la|pro-}}），它们不是词根线索。
# 不排掉的话 pro- 会把 propose 判给 proprius、ob- 把 oppose 判给 prob——
# 首轮实测 4 个不一致里 4 个都是这一类。
STOP = {
    "ab", "abs", "ad", "ante", "anti", "bi", "bene", "circum", "cis", "com",
    "con", "contra", "cum", "de", "di", "dis", "e", "ex", "extra", "in", "infra",
    "inter", "intra", "intro", "juxta", "male", "multi", "ne", "non", "ob",
    "omni", "per", "post", "prae", "pre", "preter", "pro", "quasi", "re",
    "retro", "se", "semi", "sine", "sub", "subter", "super", "supra", "trans",
    "tri", "ultra", "un", "uni-", "vice",
    # 希腊侧
    "a", "an", "amphi", "ana", "anti-", "apo", "cata", "dia", "dys", "ec",
    "en", "endo", "epi", "eu", "exo", "hyper", "hypo", "meta", "para", "peri",
    "pros", "syn", "sym",
}


def norm(s):
    """去变音符、去重建星号、小写。expendēre → expendere"""
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip().lstrip("*").strip().lower()


def fetch(titles):
    """批量取 wikitext，50 个一批，带缓存。"""
    out, need = {}, []
    for t in titles:
        f = CACHE / (urllib.parse.quote(t, safe="") + ".txt")
        if f.exists():
            out[t] = f.read_text(encoding="utf-8")
        else:
            need.append(t)
    CACHE.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(need), 50):
        batch = need[i:i + 50]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "revisions",
            "rvprop": "content", "rvslots": "main", "maxlag": "5",
            "titles": "|".join(batch)})
        req = urllib.request.Request(API + "?" + q, headers={"User-Agent": UA})
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=45).read())
        except Exception as e:                      # 网络抖动不该丢掉整轮测量
            print(f"  [warn] 批 {i//50} 失败：{e}", file=sys.stderr)
            time.sleep(2)
            continue
        for p in d.get("query", {}).get("pages", {}).values():
            title = p["title"]
            try:
                txt = p["revisions"][0]["slots"]["main"]["*"]
            except (KeyError, IndexError):
                txt = ""                            # 词条不存在
            (CACHE / (urllib.parse.quote(title, safe="") + ".txt")).write_text(
                txt, encoding="utf-8")
            out[title] = txt
        sys.stderr.write(f"\r  取回 {min(i+50, len(need))}/{len(need)}")
        time.sleep(0.2)
    if need:
        sys.stderr.write("\n")
    return out


def english_etymology(wikitext):
    """切出 ==English== 下的 ===Etymology=== 正文（可能有 Etymology 1/2）。"""
    m = re.search(r"^==\s*English\s*==\s*$", wikitext, re.M)
    if not m:
        return ""
    rest = wikitext[m.end():]
    nxt = re.search(r"^==[^=]", rest, re.M)         # 下一个 L2 语言标题
    rest = rest[:nxt.start()] if nxt else rest
    parts = []
    for em in re.finditer(r"^===+\s*Etymology[^=]*===+\s*$", rest, re.M):
        tail = rest[em.end():]
        nh = re.search(r"^===", tail, re.M)
        parts.append(tail[:nh.start()] if nh else tail)
    return "\n".join(parts)


def base_words(ety):
    """英语内部派生的基词：{{af|en|figure|-ative}} → figure
    新版语法 {{ety|en|:af|propose|-al<id:nominal>|tree=1}} 同样要接。"""
    out = []
    for tm in re.finditer(r"\{\{([^{}]*)\}\}", ety):
        parts = [p.strip() for p in tm.group(1).split("|")]
        if not parts:
            continue
        name = parts[0].lower()
        if name in AFFIX and len(parts) >= 3 and parts[1] == "en":
            rest = parts[2:]
        elif name in TREE and any(p.startswith(":af") for p in parts):
            i = next(i for i, p in enumerate(parts) if p.startswith(":af"))
            rest = parts[i + 1:]
        else:
            continue
        for p in rest:
            p = p.split("<")[0].strip()
            if p and not p.startswith("-") and not p.endswith("-") \
                    and "=" not in p and re.fullmatch(r"[a-zA-Z]{3,}", p):
                out.append(p.lower())
    return out


def lemmas(ety):
    """从词源正文里抽拉丁/希腊词元。返回 [(lemma, 强证据?)]"""
    found = []
    for tm in re.finditer(r"\{\{([^{}]*)\}\}", ety):
        parts = [p.strip() for p in tm.group(1).split("|")]
        if not parts:
            continue
        name = parts[0].lower()
        if name in ANCESTRY and len(parts) >= 4:
            # {{der|en|la|expendere||to weigh out}} → parts[2]=la parts[3]=lemma
            if parts[2] in INTEREST and parts[3]:
                found.append((norm(parts[3]), True))
            elif parts[2] in ROMANCE and parts[3]:
                found.append((norm(parts[3]), False))
        elif name in MENTION and len(parts) >= 3:
            if parts[1] in INTEREST | ROMANCE and parts[2]:
                found.append((norm(parts[2]), False))
        elif name in TREE:
            # 新版树状语法把整条链塞进一个模板，用 <> 嵌套：
            #   {{ety|en|:inh|enm:dependen<ety:der<fro:dependre<ety:der<la:dependeō>>>>}}
            # la:dependeō 藏在嵌套里，按竖线分段永远取不到，得整体扫。
            body = tm.group(1)
            if "cog" in body:      # {{ncog}}/{{cog}} 是同源词，不是祖先
                body = re.sub(r"n?cog[^<>|]*", "", body)
            for lang, lm in re.findall(
                    r"\b(la|grc|la-med|fro|frm|fr|xno|it|es|pt|ca)"
                    r":([A-Za-zÀ-ɏ*][A-Za-zÀ-ɏ'-]{2,})", body):
                found.append((norm(lm), lang in INTEREST))
    seen, out = set(), []
    for lm, strong in found:
        lm = lm.rstrip("-")
        if lm and lm not in seen and lm not in STOP and len(lm) >= 4:
            seen.add(lm)
            out.append((lm, strong))
    return out


def stem(x):
    """剥词尾到词干。pendere→pend，forma→form，propono→propon（>=3 字符）"""
    x = norm(x)
    for e in ENDINGS:
        if x.endswith(e) and len(x) - len(e) >= 3:
            return x[:-len(e)]
    return x


def variants_of(lemma):
    """拉丁词元的可比形式：整体词干，以及剥掉各前缀后的词干。
    propono → {propon, pon}（pro-）；transformo → {transform, form}（trans-）"""
    s = stem(lemma)
    out = {s}
    for p in LAT_PREFIX:
        if s.startswith(p) and len(s) - len(p) >= 3:
            out.add(stem(s[len(p):]))
    return out


def root_keys(roots):
    """根 -> 可匹配的词干键。

    只取 id / root / variants，加 origin 的**首个**拉丁词元。origin 是散文，
    会正当地提到别的拉丁词作对比（dare-give 的 origin 写着「trans＋dare 交付」），
    整段抓 ASCII 会让 trans、publish、portio 变成键——首轮 transform/propose
    判错就是这么来的。
    """
    keys = {}
    for r in roots:
        raw = {r["id"], r.get("root", "")} | set(r.get("variants") or [])
        head = re.search(r"[A-Za-zÀ-ɏ]{3,}", r.get("origin", ""))
        if head:
            raw.add(head.group(0))
        raw -= set(r.get("noisy_variants") or [])
        ks = set()
        for v in raw:
            for piece in re.split(r"[^A-Za-zÀ-ɏ]+", v or ""):
                if len(piece) >= 3:
                    ks.add(stem(piece))
                    ks.add(norm(piece))
        keys[r["id"]] = {k for k in ks if len(k) >= 3 and k not in STOP}
    return keys


def match(word_lemmas, keys, sizes):
    """词元 -> 候选根。按「对齐方式 → 证据强弱 → 重叠长度」排序。

    对齐方式压过证据强弱：manuscriptus 是强证据，但 manus 只能前缀对齐，
    而弱证据的 scribere 能精确对齐到 script——库里判的正是后者（复合词取词尾
    那个语义中心）。反过来排会把一批复合词判给修饰成分。
    """
    KIND = {"exact": 0, "suffix": 1, "prefix": 2, "inside": 3}
    cand = {}
    for lemma, strong in word_lemmas:
        for form in variants_of(lemma):
            for rid, ks in keys.items():
                best = None
                for k in ks:
                    # 精确对齐 3 字符即可（pon、pos 是真词干）；部分对齐要 4 字符，
                    # 否则 ire 的 'iti' 会从尾部咬住 positi
                    if k == form:
                        kind = "exact"
                    elif len(k) < 4:
                        continue
                    elif form.endswith(k):      # 拉丁复合词的词基在末尾
                        kind = "suffix"
                    elif form.startswith(k):    # 派生词的词基在开头（figur+at）
                        kind = "prefix"
                    elif k in form:
                        kind = "inside"
                    else:
                        continue
                    s = (KIND[kind], 0 if strong else 1, -len(k))
                    if best is None or s < best[0]:
                        best = (s, kind, k)
                if best is None:
                    continue
                if rid not in cand or best[0] < cand[rid][0]:
                    cand[rid] = (best[0], best[1])
    return [(r, t) for r, (_, t) in
            sorted(cand.items(), key=lambda kv: (kv[1][0], -sizes.get(kv[0], 0)))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", action="store_true", help="加测日耳曼池的词")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    words = json.loads((DATA / "words.json").read_text(encoding="utf-8"))["words"]
    roots = json.loads((DATA / "roots.json").read_text(encoding="utf-8"))["roots"]
    keys = root_keys(roots)
    sizes = {r["id"]: len(r.get("word_ids") or []) for r in roots}

    labeled = [(w["id"], w["root_ids"][0]) for w in words if w.get("root_ids")]
    if a.limit:
        labeled = labeled[:a.limit]
    targets = [w for w, _ in labeled]

    pool = []
    if a.pool:
        ids = {w["id"] for w in words}
        for line in (ROOT / "drafts" / "germanic_remaining.txt").read_text(
                encoding="utf-8").splitlines():
            s = line.split("#")[0].strip().split("\t")[0].strip().lower()
            if s and s not in ids:
                pool.append(s)
        if a.limit:
            pool = pool[:a.limit]
        targets += pool

    print(f"取 wikitext：{len(targets)} 词（缓存在 {CACHE.relative_to(ROOT)}）")
    text = fetch(targets)

    # ---- 第二轮：英语内部派生的词回溯基词（figurative → figure）----
    lib_root = {w["id"]: (w.get("root_ids") or [None])[0] for w in words}
    need_base = {}
    for t in targets:
        ety = english_etymology(text.get(t, ""))
        if not lemmas(ety):
            for b in base_words(ety):
                if b != t:
                    need_base.setdefault(t, []).append(b)
    extra = sorted({b for bs in need_base.values() for b in bs
                    if b not in text})
    if extra:
        print(f"回溯基词：{len(need_base)} 词无拉丁模板，取其 {len(extra)} 个基词")
        text.update(fetch(extra))

    def resolve(wid):
        """返回 (词元表, 来源)。自身没有拉丁模板时退回基词。"""
        lms = lemmas(english_etymology(text.get(wid, "")))
        if lms:
            return lms, "self"
        for b in need_base.get(wid, []):
            if lib_root.get(b):            # 基词已在库里挂好根 → 直接继承
                return [], f"inherit:{b}"
            bl = lemmas(english_etymology(text.get(b, "")))
            if bl:
                return bl, f"base:{b}"
        return [], "none"

    # ---- 标注集上算准确率 ----
    stat = defaultdict(int)
    disagree, nolemma = [], []
    for wid, truth in labeled:
        lms, src = resolve(wid)
        if src.startswith("inherit:"):
            base = src.split(":", 1)[1]
            stat["经基词继承"] += 1
            if lib_root.get(base) == truth:
                stat["top1 命中（inherit）"] += 1
            else:
                disagree.append((wid, truth, [(lib_root[base], src)], "继承不符"))
            continue
        if not lms:
            stat["无拉丁希腊词元"] += 1
            nolemma.append(wid)
            continue
        stat["有词元"] += 1
        cands = match(lms, keys, sizes)
        if not cands:
            stat["有词元但匹配不到已有根"] += 1
            continue
        top, tier = cands[0]
        if top == truth:
            stat[f"top1 命中（{tier}）"] += 1
        elif truth in [c for c, _ in cands]:
            stat["真根在候选里但不是 top1"] += 1
            disagree.append((wid, truth, cands[:3], "非top1"))
        else:
            stat["与库不一致"] += 1
            disagree.append((wid, truth, cands[:3], "不一致"))

    n = len(labeled)
    print(f"\n===== 标注集 {n} 词 =====")
    for k in sorted(stat, key=lambda k: -stat[k]):
        print(f"  {stat[k]:5}  {stat[k]/n:5.1%}  {k}")
    hit = sum(v for k, v in stat.items() if k.startswith("top1"))
    print(f"\n  top1 与库一致合计：{hit}/{n} = {hit/n:.1%}")
    got = stat["有词元"]
    if got:
        print(f"  在有词元的 {got} 词里，top1 一致率：{hit/got:.1%}")

    print(f"\n--- 不一致样本（前 25，共 {len(disagree)}）---")
    for wid, truth, cands, why in disagree[:25]:
        c = ", ".join(f"{r}({t})" for r, t in cands)
        print(f"  {wid:16} 库={truth:14} 查={c}  [{why}]")

    print(f"\n--- 查不到拉丁/希腊词元的（前 20，共 {len(nolemma)}）---")
    print("   " + ", ".join(nolemma[:20]))

    # ---- 池子：能自动定根的比例 ----
    if pool:
        print(f"\n===== 日耳曼池 {len(pool)} 词 =====")
        got = []
        for w in pool:
            lms, src = resolve(w)
            if not lms:
                continue
            cands = match(lms, keys, sizes)
            if cands:
                got.append((w, lms[0][0], cands[0]))
        print(f"  能挂到已有根上的：{len(got)}/{len(pool)} = {len(got)/len(pool):.1%}")
        print("  （这些本会被写成无根孤词）前 40：")
        for w, lm, (r, t) in got[:40]:
            print(f"    {w:18} ← {lm:16} → 根 {r:14} [{t}]")


if __name__ == "__main__":
    main()
