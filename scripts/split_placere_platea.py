#!/usr/bin/env python3
"""拆开被混成一个根的 platea（空地）与 placere（使中意）。

用法：
    python scripts/split_placere_platea.py --dry-run
    python scripts/split_placere_platea.py

【问题】
data/roots.json 里 id=placere 的那个根，origin 自己就写着两条词源：
    「拉丁语 platea（宽街）/ placere（放置、安置）」
而它的 core_concept 是「东西落定的那个位置」、core_image 是「把箱子搁在地上
那块空处」——那是 platea 的意思，与 placere（使中意、讨喜）无关。
名下 7 词实为两族：
    platea（← 希腊 plateia 宽阔的路）：place / replace / replacement / displace
    placere（使中意）                 ：please / pleasant / pleasure
两者在拉丁语本是两个词，到古法语阶段拼写才撞到一起（plaisir 与 place）。

【做法】
既有根的概念与画面本就属 platea，故把它改名 platea 并修正 origin，
please 三词另立新根 placere。这样不必重写概念，改动面最小。
    placere（旧，实为 platea）→ platea，留 place/replace/replacement/displace
    新建 placere              → please/pleasant/pleasure
概念同理：concept-placere-spot → concept-platea-spot（内容不动，只改 id 与 root_ids）
          新建 concept-placere-agreeable

【只改词根那一端】
relations 里 type=root 的关系 to 端存的是**单词 id**，不能跟着改，
否则会造出自环（上一轮迁移已踩过：forma → forma）。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PLATEA_WORDS = ["place", "replace", "replacement", "displace"]
PLACERE_WORDS = ["please", "pleasant", "pleasure"]

NEW_ROOT = {
    "id": "placere", "root": "placere", "variants": ["plais", "pleas", "plac"],
    "origin": "拉丁语 placere（使中意、讨喜），古法语作 plaisir；"
              "与 platea（宽街、空地）本是两个拉丁词，到古法语阶段拼写才撞到一起",
    "core_concept": "to sit well with the one who meets it / 正合对方的意",
    "core_image": "茶端到手边，接的人眉头一松，什么也没说",
    "english_definition": "to please, be agreeable",
    "word_ids": list(PLACERE_WORDS),
}
NEW_CONCEPT = {
    "id": "concept-placere-agreeable", "concept": "to sit well with the one who meets it",
    "chinese": "正合其意", "core_image": "茶端到手边，接的人眉头一松",
    "root_ids": ["placere"], "word_ids": list(PLACERE_WORDS),
}


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def as_list(o, k):
    return o if isinstance(o, list) else o.get(k, [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    log = []

    # 1) roots.json：旧 placere 改名 platea + 修 origin；再插入新的 placere
    o = load("roots.json")
    roots = as_list(o, "roots")
    old = next((r for r in roots if r["id"] == "placere"), None)
    if old is None:
        print("找不到 id=placere 的词根，可能已迁移过")
        return 0
    log.append("roots.json: placere → platea（概念与画面本属 platea，只改 id 与 origin）")
    log.append(f"roots.json: 新建 placere，收 {PLACERE_WORDS}")
    if not a.dry_run:
        old["id"] = "platea"
        old["root"] = "platea"
        old["variants"] = ["place", "plac", "platea"]
        old["origin"] = ("拉丁语 platea（宽街、场地）← 希腊语 plateia（宽阔的路）；"
                         "与 placere（使中意）本是两个拉丁词，"
                         "到古法语阶段拼写才撞到一起")
        old["word_ids"] = list(PLATEA_WORDS)
        roots.append(dict(NEW_ROOT))
        save("roots.json", o)

    # 2) words.json：please 三词改挂新根
    o = load("words.json")
    n = 0
    for w in as_list(o, "words"):
        rs = w.get("root_ids") or []
        if "placere" not in rs:
            continue
        tgt = "placere" if w["id"] in PLACERE_WORDS else "platea"
        new = sorted({tgt if x == "placere" else x for x in rs})
        if new != rs:
            n += 1
            if not a.dry_run:
                w["root_ids"] = new
    log.append(f"words.json: {n} 词 root_ids 改写为 platea"
               f"（please 三词本就挂 placere，无需改动，故不计入）")
    if not a.dry_run:
        save("words.json", o)

    # 3) concepts.json：旧概念改名 platea，另建 placere 概念
    o = load("concepts.json")
    cs = as_list(o, "concepts")
    oldc = next((c for c in cs if c["id"] == "concept-placere-spot"), None)
    if oldc is not None:
        log.append("concepts.json: concept-placere-spot → concept-platea-spot")
        log.append("concepts.json: 新建 concept-placere-agreeable")
        if not a.dry_run:
            oldc["id"] = "concept-platea-spot"
            oldc["root_ids"] = ["platea"]
            oldc["word_ids"] = list(PLATEA_WORDS)
            cs.append(dict(NEW_CONCEPT))
            save("concepts.json", o)

    # 4) domains.json：placere → platea，并把新根也加进同一域
    o = load("domains.json")
    for d in as_list(o, "domains"):
        for f in ("root_ids", "roots"):
            v = d.get(f)
            if isinstance(v, list) and "placere" in v:
                log.append(f"domains.json: {d['id']}.{f} placere → platea + placere")
                if not a.dry_run:
                    d[f] = [("platea" if x == "placere" else x) for x in v]
                    if "placere" not in d[f]:
                        d[f].append("placere")
        cv = d.get("concept_ids")
        if isinstance(cv, list) and "concept-placere-spot" in cv:
            if not a.dry_run:
                d["concept_ids"] = [("concept-platea-spot" if c == "concept-placere-spot" else c)
                                    for c in cv]
                d["concept_ids"].append("concept-placere-agreeable")
    if not a.dry_run:
        save("domains.json", o)

    # 5) relations.json：只改词根那一端；please 三词的边改指新根
    o = load("relations.json")
    n = 0
    for r in as_list(o, "relations"):
        for f in ("from", "source"):
            if r.get(f) == "placere":
                tgt = "placere" if r.get("to") in PLACERE_WORDS else "platea"
                if not a.dry_run:
                    r[f] = tgt
                n += 1
    log.append(f"relations.json: {n} 处词根端按所指单词分流（to 端不动）")
    if not a.dry_run:
        save("relations.json", o)

    for x in log:
        print("  ", x)
    print(f"\n{'（dry-run，未写入）' if a.dry_run else '已写入'}")
    if a.dry_run:
        return 0

    # 自检
    roots = as_list(load("roots.json"), "roots")
    words = as_list(load("words.json"), "words")
    cs = as_list(load("concepts.json"), "concepts")
    rids = {r["id"] for r in roots}
    wids = {w["id"] for w in words}
    assert "platea" in rids and "placere" in rids, "两根须同时存在"
    assert not (rids & wids), f"词根/单词同名：{sorted(rids & wids)}"
    dang = {x for w in words for x in (w.get("root_ids") or []) if x not in rids}
    assert not dang, f"words.root_ids 悬空：{sorted(dang)}"
    dang = {x for c in cs for x in (c.get("root_ids") or []) if x not in rids}
    assert not dang, f"concepts.root_ids 悬空：{sorted(dang)}"
    loops = [r for r in as_list(load("relations.json"), "relations")
             if r.get("from") == r.get("to")]
    assert not loops, f"relations 自环：{[r['from'] for r in loops]}"
    for w in words:
        if w["id"] in PLACERE_WORDS:
            assert w["root_ids"] == ["placere"], f"{w['id']} 未归 placere"
        if w["id"] in PLATEA_WORDS:
            assert w["root_ids"] == ["platea"], f"{w['id']} 未归 platea"
    print("   自检通过：两根分立、无同名、无悬空、无自环、7 词各归其位")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
