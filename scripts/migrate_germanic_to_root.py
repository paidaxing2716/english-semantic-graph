#!/usr/bin/env python3
"""把误标为 germanic 的词迁到它们真正的词根下。

用法：
    python scripts/migrate_germanic_to_root.py --dry-run
    python scripts/migrate_germanic_to_root.py

【问题来源】
日耳曼型批次的定义是「没有可迁移的拉丁/希腊词族」。起草时若某词的词根
在词表里凑不满 3 个成员，就按 germanic 收入——这本身是对的。
但后续批次可能把那个词根建起来（族成员在别的分片里陆续出现），
先前收的词就成了本该入族却孤立在外的浮点。

本轮由 chunk19 的子代理点出这个盲区（它发现 cage/cave 已作 germanic 入库，
而两者 origin 都写着 cavus）。据此反向扫全部 763 个 germanic 词条，
拿它们的 origin 去比对现有 218 个词根的拉丁词元，命中 14 个，
逐条核后 10 个确为错挂、4 个是子串假阳性：
    choose   → origin 的「gustare」含子串 stare，与 sta 无关
    canvas   → cannabis 与 canna 是两个拉丁词
    colonel  → columna（柱）与 colere（耕作）无关
    autonomy → 与 oikonomia 只共有 nomos 一半，本身是 autos＋nomos

【本脚本做什么】
对下面 10 词：decomposable 由 germanic 改 root、写入 root_ids 与 root_logic、
在 relations 里补一条「词根 → 单词」的边、把词加进该根与该概念的 word_ids。
即 review.py merge 对词根型词条所做的那一套。
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# 单词 -> (词根 id, root_logic)
MOVE = {
    "augment":  ("augere-auctor", "aug（增长）+ -ment → 使之变大 → 增加"),
    "august":   ("augere-auctor", "augustus（尊崇的）← augere（增益）→ 分量增到令人仰视"),
    "account":  ("putare", "ac-（ad- 朝）+ count（算）→ 算给某处的那笔 → 账目、说明"),
    "achieve":  ("caput", "a-（到）+ chieve（caput 头）→ 做到头 → 达成"),
    "acrobat":  ("bainein", "akros（高处）+ bat（bainein 走）→ 在高处走的人"),
    "across":   ("crux", "a-（在）+ cross（十字、横过）→ 横过那一边"),
    "affair":   ("fac", "af-（ad- 去）+ fair（facere 做）→ 要去做的那件事"),
    "agitate":  ("ag", "ag（驱动）+ -itate（反复）→ 不停地驱动 → 搅动、鼓动"),
    "avenue":   ("venire-invent", "a-（ad- 朝）+ venue（venire 来）→ 走得近的那条路"),
    "bill":     ("bulla", "bulla（盖印文书）→ 开出来的那纸单据"),
    # 第二轮：第六十四批建了 haerere 与 jungere 之后重扫，又冒出这两个。
    # 这正是本脚本设计成可重复跑的原因——每建一批新根就该重扫一遍。
    "adhere":   ("haerere", "ad-（朝）+ here（黏住）→ 贴上去黏牢 → 附着、遵守"),
    "adjoin":   ("jungere", "ad-（朝）+ join（接合）→ 接到一处、彼此相连 → 毗连"),
    # 第三轮：第六十五批建了 gnoscere 之后重扫。它的 origin 早就写着
    # 「← 拉丁语 ad- + cognoscere」，却挂着「日耳曼核心词，本身即词根」的说明——
    # 自相矛盾在库里躺了很久，只是此前没有 gnoscere 这个根可挂。
    "acquaint": ("gnoscere", "ac-（ad- 朝）+ quaint（cognoscere 认识）→ 让人认下来 → 使相识"),
}


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def as_list(o, k):
    return o if isinstance(o, list) else o.get(k, [])


def scan(words, roots):
    """扫全部 germanic 词条，找 origin 指向某个已建模词根的——即本该入族的浮点。

    此前本脚本**没有扫描环节**，只套用上面那份手写的 MOVE 字典。那些早已应用完，
    所以 --dry-run 输出「共 0 词」而 docstring 却说「重扫大约 5/6 是子串噪声」——
    那次「反向扫 763 个 germanic 词条」是当初某个代理临时写代码手扫的，从未沉淀
    进脚本。照 docs/NEXT.md 的指引跑它，会看到 0 词 + 自检全绿，以为这轮没有孤词，
    而一次扫描都没发生。本函数补上它。

    只输出候选，不自动改：实测约 5/6 是子串噪声，必须逐个核词源再往 MOVE 里加。
    """
    # 每个根可用来匹配的拉丁/希腊词形：id、root、variants，加 origin 的首个词元。
    # 不整段抓 origin——那是散文，会正当地提到别的拉丁词作对比（dare-give 的
    # origin 写着「trans＋dare 交付」），整段抓会让 trans 变成它的键。
    # 【只能用拉丁/希腊词形做键，不能用 variants】variants 存的是**英语**词干：
    # lacere 的 variants 含 'light'、linum 含 'line'、foris 含 'fore'、rotula 含
    # 'round'。拿它们匹配英语 origin 文本，任何含 light/line 的复合词都会撞上——
    # 实测 laser、daylight、airline、headline、forward 全是这么误报的。
    # 键只取：根 id（本就是拉丁原形）+ origin 里的拉丁词元。
    forms = {}
    for r in roots:
        cand = {r["id"]}
        # origin 开头那一串才是该根的拉丁词元（「拉丁语 densus（稠的）」→ densus），
        # 整段抓会把散文里作对比的别的拉丁词也收进来。
        for m in re.finditer(r"[A-Za-zÀ-ɏ]{4,}", r.get("origin", "")[:40]):
            cand.add(m.group(0))
        cand -= set(r.get("noisy_variants") or [])
        # 英语词形不作键：与该根任一 variant 完全相同的短英语词剔掉
        eng = {v.lower() for v in (r.get("variants") or []) if v.isascii()}
        # 拉丁/希腊前缀不承载词根语义。legere-intel 的 origin 写「intelligere：
        # inter- + legere」，抽 inter 做键会让任何 inter- 词撞上它。
        PREFIX = {"inter", "trans", "circum", "contra", "intro", "super",
                  "supra", "subter", "ante", "post", "prae", "retro", "extra",
                  "infra", "intra", "juxta", "quasi", "ultra", "semi", "multi",
                  "omni", "bene", "male", "vice", "amphi", "anti", "cata",
                  "meta", "para", "peri", "hyper", "hypo", "endo", "exo"}
        forms[r["id"]] = {c.lower() for c in cand
                          if c and len(c) >= 5 and c.lower() not in eng
                          and c.lower() not in PREFIX}

    # origin 里「与 X 不同源」这类排除措辞附近的词形不算命中——写明不同源反而
    # 被当成证据，是同一个坑的第三次（screen_draft_etymology 与 regroup 都栽过）。
    CONTRAST = ("不同根", "不同源", "不计入", "不合并", "非同", "不属", "而不",
                "无关", "勿混", "另有分别", "并非同源", "不是同", "两个不同")

    out = []
    for w in words:
        if w.get("root_ids"):
            continue                          # 已挂根
        origin = (w.get("origin") or "").lower()
        if not origin:
            continue
        for rid, cands in forms.items():
            hit = next((c for c in cands
                        if re.search(r"(?<![a-z])" + re.escape(c) + r"(?![a-z])",
                                     origin)), None)
            if not hit:
                continue
            m = re.search(r"(?<![a-z])" + re.escape(hit) + r"(?![a-z])", origin)
            win = origin[max(0, m.start() - 60):m.end() + 60]
            if any(x in win for x in CONTRAST):
                continue
            out.append((w["id"], rid, hit, w.get("origin", "")))
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--scan", action="store_true",
                    help="扫 germanic 词条找本该入族的浮点，只报候选不改数据")
    a = ap.parse_args()

    wf = load("words.json")
    words = as_list(wf, "words")
    rootf = load("roots.json")
    roots = as_list(rootf, "roots")
    cf = load("concepts.json")
    concepts = as_list(cf, "concepts")
    rf = load("relations.json")
    rels = as_list(rf, "relations")

    if a.scan:
        hits = scan(words, roots)
        n_g = sum(1 for w in words if not w.get("root_ids"))
        print(f"扫 {n_g} 个 germanic 词条，{len(hits)} 个 origin 指向已建模词根：\n")
        for wid, rid, form, origin in hits:
            print(f"  {wid:16} → {rid:16} （origin 里的 {form!r}）")
            print(f"      {origin[:96]}")
        print(f"\n共 {len(hits)} 个候选。**约 5/6 是子串噪声**，逐个核词源，"
              f"真命中的往 MOVE 字典里加一条（累积记录，脚本幂等），再跑一次不带 "
              f"--scan 的本脚本。")
        return 0

    rids = {r["id"] for r in roots}
    bad = [rid for _, (rid, _) in MOVE.items() if rid not in rids]
    if bad:
        print(f"[FAIL] 这些目标词根不存在：{sorted(set(bad))}")
        return 1

    wmap = {w["id"]: w for w in words}
    missing = [k for k in MOVE if k not in wmap]
    if missing:
        print(f"[FAIL] 这些词不在库中：{missing}")
        return 1

    done = []
    for wid, (rid, logic) in MOVE.items():
        w = wmap[wid]
        if w.get("decomposable") == "root" and rid in (w.get("root_ids") or []):
            continue                      # 已迁移过，幂等
        done.append(f"{wid}: germanic → root（{rid}）")
        if a.dry_run:
            continue
        w["decomposable"] = "root"
        w.pop("decomposable_note", None)  # root 型不写这个字段
        w["root_ids"] = [rid]
        w["root_logic"] = logic
        # 根与概念的 word_ids
        for r in roots:
            if r["id"] == rid and wid not in (r.get("word_ids") or []):
                r.setdefault("word_ids", []).append(wid)
                r["word_ids"].sort()
        for c in concepts:
            if rid in (c.get("root_ids") or []) and wid not in (c.get("word_ids") or []):
                c.setdefault("word_ids", []).append(wid)
                c["word_ids"].sort()
        # 词根 → 单词 的边
        if not any(r.get("from") == rid and r.get("to") == wid for r in rels):
            rels.append({"from": rid, "to": wid, "type": "root", "note": logic[:60]})

    for d in done:
        print("  ", d)
    print(f"\n{'（dry-run，未写入）' if a.dry_run else '已写入'} 共 {len(done)} 词")
    if a.dry_run or not done:
        return 0

    save("words.json", wf)
    save("roots.json", rootf)
    save("concepts.json", cf)
    save("relations.json", rf)

    # 自检
    words = as_list(load("words.json"), "words")
    roots = as_list(load("roots.json"), "roots")
    rids = {r["id"] for r in roots}
    wmap = {w["id"]: w for w in words}
    for wid, (rid, _) in MOVE.items():
        w = wmap[wid]
        assert w["decomposable"] == "root", f"{wid} 未改为 root 型"
        assert w["root_ids"] == [rid], f"{wid} 的 root_ids 不对：{w['root_ids']}"
        assert w.get("root_logic"), f"{wid} 缺 root_logic"
        assert "decomposable_note" not in w, f"{wid} 仍留着 decomposable_note"
    dang = {x for w in words for x in (w.get("root_ids") or []) if x not in rids}
    assert not dang, f"root_ids 悬空：{sorted(dang)}"
    loops = [r for r in as_list(load("relations.json"), "relations")
             if r.get("from") == r.get("to")]
    assert not loops, f"relations 自环：{[r['from'] for r in loops]}"
    print("   自检通过：均已改 root 型、无悬空 root_ids、无自环")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
