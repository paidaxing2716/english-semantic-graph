#!/usr/bin/env python3
"""给高产词根补全 variants（英语实际拼写形），提升反查召回率。

用法：
    python scripts/enrich_root_variants.py --dry-run   # 只看会改什么
    python scripts/enrich_root_variants.py             # 实际写入

【背景】
scripts/find_root_members.py 靠 roots.json 的 variants 去词表里捞同族词。
但 variants 原来是建族时顺手写的，只覆盖该批词条用到的拼写，不求全。
例：cep（capere 抓取）只登记了 cep/capt/cept/cap，缺 ceive 与 cip，
于是 receive/deceive/conceive/perceive/recipe/principle 等真成员一个都捞不到。
补这一项，反查的召回率才有意义。

【variants 是「召回线索」，不是「词源断言」】
补进来的拼写只用于把候选词捞出来给人看，不代表凡命中者皆同族。
同形异源照样会混进来，必须人工核：
    cip  → discipline（← discere 学，不是 capere）  ✗
    cap  → captain/capital（← caput 头）            ✗
所以本脚本只扩召回面，判断仍在人工那一关。

【为什么有些变体很短】
fy（facere）、fit（facere）这类只有 2-3 字母，作子串会噪声爆炸。
仍然登记，因为它们确实是该词根在英语里的真实形态；
噪声由 find_root_members.py 的 --min-len 在扫描时控制，两件事分开。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "roots.json"

# 词根 id -> 低区分度变体。这些是**真变体**，但作子串匹配噪声压倒信号，
# 反查时默认跳过（写进 roots.json 的 noisy_variants 字段，供工具读取）。
# 长度不能当过滤标准：cip（3 字母）精度很高，lat（3 字母）只有 17%。
NOISY = {
    # latus 是 ferre 的过去分词，translate/relate 确属此支；
    # 但 -ate 动词里 l 属词干、ate 属后缀（calculate←calculus、
    # circulate←circulus），另有 plate←希腊 platys、chocolate←纳瓦特尔语、
    # late←古英语，全与 ferre 无关。实测真 7 噪 35，精度 17%。
    "ferre": ["lat"],
    # 同理：spec 会命中 special/species 之外大量 -spect 无关词已由 spect 覆盖
    "premere": ["prim"],
}

# 词根 id -> 该删的变体。建族时把前缀误写成了词根变体。
REMOVE = {
    # 'dif' 是前缀（dis- 在 f 前的同化形），不是 ferre 的拼写变体。
    # differ/difference/different/indifferent 都含 'fer'，删掉不损召回；
    # 留着反而把 difficult/difficulty（← dis+facilis，属 fac 族）
    # 和 modify（← modus+facere）误挂到 ferre 名下。
    "ferre": ["dif"],
}

# 词根 id -> 待补的英语拼写形。每条都注明它能捞回哪些真成员。
ADD = {
    # capere（抓取）在英语里的四条拼写线，原表只有 cap/capt/cept
    "cep": [
        "ceive",   # receive, deceive, conceive, perceive
        "cip",     # recipe, principle, principal, municipal, participate
        "cup",     # occupy
    ],
    # stare（立）的重叠形 sistere，拼作 sist
    "sta": [
        "sist",    # assist, consist, insist, persist, resist
        "stan",    # substance, circumstance
    ],
    # claudere（关）的 clos 一线，原表只有 clud/clus/claus
    "clud": [
        "clos",    # close, closet, closure, enclose, disclose
    ],
    # mittere（送）的 mise 一线
    "mit-miss": [
        "mise",    # promise, compromise, premise
    ],
    # specere（看）的 spis 一线
    "spect": [
        "spis",    # despise
        "spise",
    ],
    # facere（做）在英语里的弱化形，短但真实
    "fac": [
        "fit",     # benefit, profit
        "fy",      # satisfy, simplify, justify, notify, identify
        "feit",    # counterfeit
    ],
    # ferre（带）的形容词形 fert
    "ferre": [
        "fert",    # fertile
        "ference", # reference, difference（长变体，噪声低）
    ],
    # tenere（握）与 tendere（伸）各自的补充
    "tain": [
        "tenu",    # tenure（若入表）
        "tent",    # content, retention
    ],
    "tendere": [
        "tens",    # tension, intense
        "tenu",    # tenuous
    ],
    # ponere（放）的 pound 一线（compound/component 走 pon）
    "ponere": [
        "pound",   # compound, expound
    ],
    # premere（压）的 print 一线
    "premere": [
        "print",   # print, imprint（← 古法语 preinte ← premere）
        "prim",    # 仅 imprimatur 类，短且噪声高，靠 min-len 挡
    ],
    # trahere（拉）的 treat 一线
    "tract": [
        "treat",   # treat, treaty, treatment（← tractare）
    ],
    # ducere（引）
    "duc-duct": [
        "duke",    # duke, duchess
    ],
    # cedere（走）的 cease 一线
    "ced": [
        "cease",   # cease, deceased（← cessare ← cedere）
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    obj = json.loads(P.read_text(encoding="utf-8"))
    roots = obj if isinstance(obj, list) else obj.get("roots", [])
    index = {r["id"]: r for r in roots}

    missing_ids = [rid for rid in ADD if rid not in index]
    if missing_ids:
        print(f"[警告] 这些词根 id 不存在，已跳过：{missing_ids}")

    changed = 0

    # 先删误写成变体的前缀
    for rid, drop in REMOVE.items():
        r = index.get(rid)
        if not r:
            continue
        cur = r.get("variants") or []
        keep = [v for v in cur if v.lower() not in {d.lower() for d in drop}]
        if len(keep) != len(cur):
            print(f"  {rid:12s} {cur}")
            print(f"  {'':12s}   - {[v for v in cur if v not in keep]}（前缀，非词根变体）")
            if not args.dry_run:
                r["variants"] = keep
            changed += len(cur) - len(keep)

    # 标注低区分度变体：仍留在 variants 里（它们是真变体），
    # 另存一份 noisy_variants 供 find_root_members.py 默认跳过
    for rid, noisy in NOISY.items():
        r = index.get(rid)
        if not r:
            continue
        have = {v.lower() for v in (r.get("variants") or [])}
        mark = sorted({n.lower() for n in noisy} & have)
        if mark and r.get("noisy_variants") != mark:
            print(f"  {rid:12s} 标记低区分度变体 {mark}（反查默认跳过）")
            if not args.dry_run:
                r["noisy_variants"] = mark
            changed += len(mark)

    for rid, extra in ADD.items():
        r = index.get(rid)
        if not r:
            continue
        cur = r.get("variants") or []
        low = {v.lower() for v in cur}
        new = [v for v in extra if v.lower() not in low]
        if not new:
            continue
        print(f"  {rid:12s} {cur}")
        print(f"  {'':12s}   + {new}")
        if not args.dry_run:
            r["variants"] = cur + new
        changed += len(new)

    print(f"\n{'（dry-run，未写入）' if args.dry_run else '已写入'} "
          f"共改动 {changed} 个变体（补 {len(ADD)} 根 / 清 {len(REMOVE)} 根）")

    if not args.dry_run and changed:
        P.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
