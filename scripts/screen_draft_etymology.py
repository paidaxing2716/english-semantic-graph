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

【本脚本只出候选，会有子串假阳性，必须人工核】
匹配是按子串做的，两个无关的拉丁词只要拼写相含就会误报。实例：
    canvas 的 origin 写「cannapaceus ← cannabis（大麻）」，其中含 'canna'，
    于是被报成 canalis（芦苇、管道）族。但 cannabis（← 希腊 kannabis 大麻）
    与 canna（← 希腊 kanna 芦苇）是两个不同的拉丁词，canvas 不属该族。
故本脚本的输出是「应考虑」而非「必须改」，逐条核过再动。

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
    # 后半是拉丁/希腊**前缀**：它们在 origin 里作为构词成分出现（legere-intel 的
    # origin 写「intelligere：inter- + legere」），抽成键会让任何 inter-/trans-
    # 开头的词都撞上该根。前缀不承载词根语义，不该做匹配键。
    STOP = {"vetted", "note", "pie", "root", "variants",
            "inter", "trans", "circum", "contra", "intro", "super", "supra",
            "subter", "ante", "post", "prae", "retro", "extra", "infra",
            "intra", "juxta", "quasi", "ultra", "semi", "multi", "omni",
            "bene", "male", "vice", "amphi", "anti", "cata", "meta", "para",
            "peri", "hyper", "hypo", "endo", "exo",
            # 三四字母的古典前缀。原先只挡长前缀，是因为短的本来就被长度下限
            # 顺带挡住了；给根自己声明的词形放宽下限后（见下方 declared），
            # 它们会现形：`per` 是 experiri 的变体，一放宽就命中 perfect /
            # perform / perceive / percent / perspective 五个 per- 开头的词，
            # 而承义的根本不是它。前缀不承载词根语义，一律不做键。
            "per", "par", "pro", "pre", "sub", "sur", "dis", "dif", "con",
            "com", "col", "cor", "obs", "abs", "des", "ses"}

    # 【排除措辞】origin 是散文，会正当地提到**别的**拉丁词来划清界限：
    #   profiteri 的 origin 写「与 profile 的 filum（线）一支毫无关系，勿混」
    #   tangere   的 origin 写「源头与 tenere（握）另有分别」
    #   jus       的 origin 写「judex 是 jus＋dicere（宣法者）」
    # 把这些词形抽成匹配键，等于让「写明不同源」反过来制造误报，且是系统性的：
    # 任何引用 filum / tenere / dicere 的补词都会被报一次。四个子代理各自撞上，
    # 其中一个为了让门变绿把自己 origin 里的 regere/credere 改写成 rego/credo
    # ——门在诱导数据往错的方向弯。
    # 同款过滤 regroup_pools_by_family.py 已有（CONTRAST），这里补 无关/勿混/分别。
    # 「已分化」「承义的是」是子代理实际写出来、而此前不被识别的两种措辞：
    #   par-equal 的 origin 写「parare（使就绪）同 PIE 但拉丁已分化」→ parare 被
    #   抽成 par-equal 的键，apparatus 因此误报（chunk85 指出）
    #   entrepreneur 的 origin 写「承义的是抓住这一支，不是 intrare」→ 裸「不是」
    #   此前不在表里（chunk84 指出，它没为让门变绿去改词源措辞，做得对）
    CONTRAST = ("不同根", "不同源", "不计入", "不合并", "不并入", "非同", "不属", "而不",
                "无关", "勿混", "另有分别", "并非同源", "不是同", "两个不同",
                "已分化", "而分支不同", "不同支", "承义的是", "不是 ", "语义已分",
                # 「异源」补的是**同形异源**这个写法：库中 tense 的 origin 写着
                # 「表『时态』的 tense 另出拉丁语 tempus，同形异源」，处理完全正确，
                # 但「同形异源」里没有「不同源」三字连排，旧表匹配不到，于是一条
                # 写对了的词源说明反而被报成漏挂。
                "异源", "不在此列", "另有分立")

    # 语境用**字数窗口**，不按标点分句。试过分句，更差：这些 origin 的否定词
    # 常与词形隔着逗号或括号（「与 profile 的 filum（线）一支毫无关系」——
    # filum 在括号前、否定在括号后），分句正好把两者切散，报警从 12 涨到 17。
    # 窗口取 ±60 字，覆盖实测最远的一例（miniature 那条 31 字）。
    WIN = 60

    def clause_of(text, pos, end=None):
        return text[max(0, pos - WIN):(end or pos) + WIN]

    def lemmas_from_origin(origin):
        """抽词元，但跳过处在排除措辞附近的——那是在说「不是这个」。"""
        out, dropped = set(), set()
        for m in lemma_pat.finditer(origin):
            c = clause_of(origin, m.start(), m.end())
            (dropped if any(x in c for x in CONTRAST) else out).add(m.group(1))
        return out, dropped - out

    # 【别根的自有标识不做本根的键】
    # 根的 origin 会正当地写出构词成分，而那个成分本身常常就是另一个根：
    #     intelligere 的 origin 写「inter-（之间）+ legere（挑选）」
    #     fortuna     的 origin 写「fortis（强）→ fortuna」
    #     mandare     的 origin 写「manus（手）+ dare」
    # 于是 legere / fortis / manus 成了**前者**的键，任何 origin 提到它们的词都被
    # 报成「应挂前者」。实测全库 23 处这样的泄漏，正是本会话反复出现又被逐条判成
    # 假阳性的那批警告的成因：force → fortuna、fireplace → placere、
    # lesson → intelligere 全部出自此处。
    #
    # 判据：一个拉丁词形若已经是**另一个根的 id 或 root 字段**，它就属于那个根，
    # 不该同时充当「origin 里提到它的根」的键。那个根自己会用它匹配，召回不丢。
    #
    # 只过滤 origin 抽出来的键，**不动 id / root / variants**——全库有 25 个变体
    # 被多个根有意同时声明（`leg` 同属 legere 与 lex-legis 是刻意分立），
    # 那类冲突由 noisy_variants 处理，不该在这里一刀切掉。
    #
    # 「自有标识」除了 id 与 root 字段，还必须算上**本根 origin 里的首个拉丁词元**。
    # 全库约三分之一的根按族里可见的英语词干命名（fac / rect / dict / plic / pend /
    # spect，见 draft-spec 的命名一节），它们的拉丁原形只出现在自己的 origin 里。
    # 不算这一层的话，jus 的 origin 写「judex 是 jus＋dicere」时，dicere 仍会成为
    # jus 的键，而 dicere 真正的归属是 id 为 `dict` 的那个根——condition 正确挂在
    # dict 上，却被报成该挂 jus。取首个而非全部，理由与 probe_etymology_coverage
    # 的 root_keys 相同：origin 是散文，首个之后提到的往往正是别的根。
    owned = set()
    for r in roots:
        marks = [r["id"], r.get("root", "")]
        head = re.search(r"[A-Za-z][A-Za-z]{3,}", r.get("origin", "") or "")
        if head:
            marks.append(head.group(0))
        for x in marks:
            for piece in re.split(r"[^A-Za-z]+", x or ""):
                if len(piece) >= a.min_len:
                    owned.add(piece.lower())

    forms, ignored, borrowed = {}, {}, {}
    for r in roots:
        cand = {r.get("root", "")} | set(r.get("variants") or [])
        keep, drop = lemmas_from_origin(r.get("origin", ""))
        mine = {x.lower() for x in cand if x}
        steal = {c for c in keep if c.lower() in owned and c.lower() not in mine}
        if steal:
            borrowed[r["id"]] = sorted(steal)
        # 长度下限只该管**从 origin 散文里抽出来的**词元——那里噪声大。根**自己
        # 声明的** id / root / variants 不是噪声，是刻意选定的标识，可以放宽，
        # 但**放宽到 4 而不是 3**。这个界是量出来的，不是估的：
        #
        #   下限 3：4 个失明的根全部现形，但 chunk109 的伪报从 0 涨到 4，全是
        #           日耳曼词的古英语词形与拉丁词干同形——leg（古诺尔斯 leggr）撞
        #           legere、loc（古英语 loc 门闩）撞 loc（locus）、man 撞 manus、
        #           stan 撞 sta。真实批次里孤立词占多数，这类撞得最凶。
        #   下限 4：cura（13 员，最大的那个失明根）现形，上面四个 3 字母的撞名
        #           全部避开。res / via（各 5 员）仍失明，改法在数据侧——给它们的
        #           origin 补一个 ≥5 字母的同族词形（curare 那种），不在这里放宽。
        #
        # 只按控制样本调这个数会调错：400 个已挂根的词里短词干撞名很少，
        # 真实批次里到处都是。
        declared = {c for c in ({r["id"], r.get("root", "")}
                                | set(r.get("variants") or []))
                    if c and len(c) >= 4 and c.isalpha() and c not in STOP}
        declared -= {c for c in (r.get("noisy_variants") or [])}
        harvested = {c for c in (keep - steal)
                     if len(c) >= a.min_len and c.isalpha() and c not in STOP}
        cand = declared | harvested
        if cand:
            forms[r["id"]] = cand
        drop = {c for c in drop if len(c) >= a.min_len and c.isalpha()
                and c not in STOP}
        if drop:
            ignored[r["id"]] = sorted(drop)

    members = {}
    for w in words:
        for rid in w.get("root_ids") or []:
            members.setdefault(rid, []).append(w["id"])

    # 列位置随行格式变，必须按标签取，不能写死下标。
    #   旧式无标签 10 列： word=0  origin=3
    #   新式 W 行 14 列：  word=1  origin=6   （3 是 phonetic）
    #   新式 R 行 10 列：  本身就是词根，不参与筛查
    # 写死 row[3] 的后果不是报错而是**静默失效**：它拿拉丁词元去比对 IPA 串，
    # 永远比不中，于是任何带标签的草稿都能拿到一个空洞的 [OK]。
    # 由 chunk34 的子代理发现——它自己按第 7 列重跑了一遍匹配逻辑。
    # 还要取第 5 列 root_ids：本脚本找的是「本该走词根型、却被写成孤立词条」的词，
    # 已经在第 5 列挂好该根的补词不属此列。不看第 5 列的后果是词根批必然全红——
    # 补词的 origin 天然会写出它所属根的拉丁词形（mobile 的 origin 就得写 movere），
    # 于是每个补词都自报一次，而给出的处理办法是「把这些行删掉」，
    # 照做就会删掉正确的成员词。日耳曼批不受影响：那边第 5 列一律为空。
    def pick(row):
        tag = row[0].strip()
        if tag == "R":
            return None
        if tag == "W":
            if len(row) < 7:
                return None
            declared = {x.strip() for x in row[4].split("/") if x.strip()}
            return (row[1], row[6], declared)
        return (row[0], row[3], set()) if len(row) >= 4 else None

    hits = []
    for f in a.tsv:
        for row in csv.reader(Path(f).read_text(encoding="utf-8").splitlines(),
                              delimiter="\t"):
            if not row:
                continue
            got = pick(row)
            if not got:
                continue
            word, origin, declared = got
            for rid, cands in forms.items():
                if rid in declared:      # 已挂在这个根上，不是漏挂
                    continue
                for c in cands:
                    # 按词边界匹配。纯子串的后果：'edere'（ex+dare 交出）会命中
                    # cedere / caedere / sedere —— 那是拉丁第二/三变位的 -edere
                    # 词尾，不是词根。access/excess/necessary 七个词都被这一条
                    # 误报过。同理 'inter' 是前缀而非承义根。
                    m = re.search(r"(?<![a-z])" + re.escape(c.lower())
                                  + r"(?![a-z])", origin.lower())
                    if not m:
                        continue
                    # 草稿自己的 origin 也会有排除措辞：三条真实修正（miniature
                    # 「与 minus 并非同源」、put「与 putare 无关」、portion
                    # 「与 portare 无关」）必须写出那个词才说得清为什么不挂它，
                    # 而写出来就被这道门抓。改对了反而变红，会逼下一个人改回去。
                    if any(x in clause_of(origin, m.start(), m.end())
                           for x in CONTRAST):
                        continue
                    hits.append((Path(f).name, word, rid, c, origin))
                    break
                else:
                    continue
                break

    # 放宽检查的地方必须自己说出来，否则下一个人无法判断 [OK] 有多少含金量。
    if borrowed:
        n = sum(len(v) for v in borrowed.values())
        print(f"[info] {n} 个词形是别根的自有标识，未用作本根的键"
              f"（归属那个根，由它自己匹配），涉及 {len(borrowed)} 个根：")
        for rid, fs in sorted(borrowed.items()):
            print(f"    {rid} 的 origin 提到 {', '.join(fs)}")
        print()
    if ignored:
        n = sum(len(v) for v in ignored.values())
        print(f"[info] {n} 个词形处在排除措辞（{'/'.join(CONTRAST[:4])}…）附近，"
              f"未用作匹配键，涉及 {len(ignored)} 个根：")
        for rid, forms_ in sorted(ignored.items()):
            print(f"    {rid}: {', '.join(forms_)}")
        print()

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
    # 别照这条建议删行：删掉的可能正是该根的正确成员（filum 族的 file 就是
    # 这种），而报警本身可能来自别的根 origin 里的子串。先核词源再决定。
    print("处理办法：逐条核词源。确为漏挂的，把行从 TSV 删掉另做词根型词条；"
          "属子串假阳性的，在回报里说明，别改数据。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
