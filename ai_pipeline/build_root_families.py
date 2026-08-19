#!/usr/bin/env python3
"""把自动发现的词族 + 词源审核结论，合成一份可用的词族清单。

输入：
  classify_wordlist.py 的输出（自动发现的词族，含拼写巧合造成的误并）
  etymology_verdicts.json（逐族审词源的结论）

输出：
  vetted_families.json —— 清理后的词族，可直接作为建词条的选题清单

用法：
    python ai_pipeline/build_root_families.py <classified.json> [-o vetted_families.json]
"""

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MIN_KEEP = 3     # 清理后不足这么多词的族，教学价值有限，降级


def load_small_verdicts():
    """小词族的判断按类型分组存放，展开成与大词族相同的结构。"""
    p = HERE / "etymology_verdicts_small.json"
    if not p.exists():
        return {}
    s = json.loads(p.read_text(encoding="utf-8"))
    out = {}

    g = s.get("dissolve_germanic") or {}
    for stem in g.get("stems") or []:
        out[stem] = {"dissolve": g.get("why", "日耳曼语族，不适用本方法")}

    c = s.get("dissolve_coincidence") or {}
    for stem, why in (c.get("stems") or {}).items():
        out[stem] = {"dissolve": why}

    sp = s.get("split") or {}
    for stem, groups in (sp.get("stems") or {}).items():
        out.setdefault(stem, {})["split"] = groups

    dr = s.get("drop") or {}
    for stem, words in (dr.get("words") or {}).items():
        out.setdefault(stem, {}).setdefault("drop", {}).update(words)

    k = s.get("keep") or {}
    for stem in k.get("stems") or []:
        out.setdefault(stem, {})["keep_all"] = k.get("why", "全族同源")

    # 第二轮：修正词干提取 bug 后新出现的词族
    sp2 = s.get("split_second_pass") or {}
    for stem, groups in (sp2.get("stems") or {}).items():
        out.setdefault(stem, {})["split"] = groups

    k2 = s.get("keep_second_pass") or {}
    for stem in k2.get("stems") or []:
        out.setdefault(stem, {})["keep_all"] = k2.get("why", "全族同源")

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("classified")
    ap.add_argument("-o", "--out", default=str(HERE / "vetted_families.json"))
    ap.add_argument("--min-keep", type=int, default=MIN_KEEP)
    a = ap.parse_args()

    auto = json.loads(Path(a.classified).read_text(encoding="utf-8"))["qualified_families"]
    vd = json.loads((HERE / "etymology_verdicts.json").read_text(encoding="utf-8"))["verdicts"]
    vd.update(load_small_verdicts())

    families = {k: sorted(set(v)) for k, v in auto.items()}
    log = {"dropped": [], "split": [], "merged": [], "dissolved": [], "demoted": []}

    # 1) 整族作废（拼写巧合）
    for stem, v in vd.items():
        if "dissolve" in v and stem in families:
            log["dissolved"].append({"stem": stem, "words": families[stem],
                                     "why": v["dissolve"]})
            del families[stem]

    # 2) 先剔除有明确词源判断的混入词。
    # 必须在拆族之前：拆族会把整族取走，之后再剔除就找不到这些词，
    # 理由会被误记成"缺少词源判断"，掩盖掉实际已有的判断依据。
    for stem, v in vd.items():
        for w, why in (v.get("drop") or {}).items():
            for key in [k for k in families if k == stem or k.startswith(stem + "::")]:
                if w in families[key]:
                    families[key].remove(w)
                    log["dropped"].append({"word": w, "from": key, "why": why})

    # 3) 拆族（一个拼写下混了多个词根）
    for stem, v in list(vd.items()):
        if "split" not in v or stem not in families:
            continue
        original = families.pop(stem)
        placed = set()
        for label, words in v["split"].items():
            got = [w for w in words if w in original]
            if not got:
                continue
            key = f"{stem}::{label.split()[0]}"
            families[key] = sorted(got)
            placed.update(got)
        leftover = [w for w in original if w not in placed]
        log["split"].append({"stem": stem, "into": list(v["split"].keys()),
                             "unplaced": leftover})
        # 拆分名单没覆盖到的词：无判断依据，不留在任何族里
        for w in leftover:
            log["dropped"].append({"word": w, "from": stem,
                                   "why": "拆族时未列入任何子族，缺少词源判断"})

    # 4) 合并同源族
    for stem, v in vd.items():
        tgt = v.get("merge_into")
        if not tgt or stem not in families:
            continue
        src = families.pop(stem)
        # 目标族可能已被拆分，合并到主干或新建
        cand = [k for k in families if k == tgt or k.startswith(tgt + "::")]
        key = cand[0] if cand else tgt
        families.setdefault(key, [])
        before = len(families[key])
        families[key] = sorted(set(families[key]) | set(src))
        log["merged"].append({"from": stem, "into": key,
                              "added": len(families[key]) - before,
                              "why": v.get("why", "")})

    # 5) 清理后过小的族降级
    vetted, demoted = {}, {}
    for k, v in families.items():
        if len(v) >= a.min_keep:
            vetted[k] = v
        else:
            demoted[k] = v
            log["demoted"].append({"stem": k, "words": v})

    reviewed = set(vd)
    unreviewed = [k for k in auto if k not in reviewed]

    print(f"自动发现          {len(auto)} 族 / {sum(len(v) for v in auto.values())} 词次")
    print(f"已审词源          {len(reviewed)} 族")
    print(f"未审（3-4 词小族） {len(unreviewed)} 族\n")
    print(f"整族作废（拼写巧合）  {len(log['dissolved'])} 族")
    print(f"拆族（混多个词根）    {len(log['split'])} 族")
    print(f"合并（同根被拆开）    {len(log['merged'])} 族")
    print(f"剔除混入词            {len(log['dropped'])} 词")
    print(f"清理后过小降级        {len(log['demoted'])} 族")
    print(f"\n可用词族              {len(vetted)} 族 / {sum(len(v) for v in vetted.values())} 词次")

    print("\n整族作废的：")
    for d in log["dissolved"]:
        print(f"  {d['stem']:<7} {', '.join(d['words'][:6])}")

    print("\n剔除的混入词（前 20）：")
    for d in log["dropped"][:20]:
        print(f"  {d['word']:<12} 原属 {d['from']:<14} {d['why'][:44]}")

    print("\n清理后最大的词族：")
    for k, v in sorted(vetted.items(), key=lambda kv: -len(kv[1]))[:12]:
        print(f"  {k:<22} {len(v):>2} 词  {', '.join(v[:6])}")

    Path(a.out).write_text(json.dumps({
        "schema_version": "0.1",
        "source": Path(a.classified).name,
        "min_keep": a.min_keep,
        "accuracy_note": (
            "此处词数是下限，不是精确值。词族由启发式词干提取发现，"
            "对已知高产词根抽样校准显示约 35% 的成员被误判为'孤立词'"
            "（如 capere 的 capable/capacity/capture、volvere 的 evolve/involve）。"
            "另有 62 个族清理后只剩 2 词而被降级，但其词根本身高产，"
            "只是在考研词表范围内成员少。因此实际可教词量高于此数。"
        ),
        "stats": {
            "auto_families": len(auto),
            "reviewed_families": len(reviewed),
            "unreviewed_families": len(unreviewed),
            "vetted_families": len(vetted),
            "vetted_words": sum(len(v) for v in vetted.values()),
            "dissolved": len(log["dissolved"]),
            "split": len(log["split"]),
            "merged": len(log["merged"]),
            "dropped_words": len(log["dropped"]),
        },
        "families": vetted,
        "demoted": demoted,
        "unreviewed": {k: auto[k] for k in unreviewed},
        "log": log,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n已写入 {a.out}")


if __name__ == "__main__":
    main()
