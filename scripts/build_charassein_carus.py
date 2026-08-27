#!/usr/bin/env python3
"""建 charassein / carus 两根，把 6 个已入库的孤立词条挂进去。

    python scripts/build_charassein_carus.py --dry-run
    python scripts/build_charassein_carus.py

【为什么不走 entries_from_draft】两族的 6 个词已全部入库（现为无根孤立词条），
那条管道遇到已入库的词会报「已在词库中」。而 0 词的 R 行也走不通它——word_ids
字段不会被创建，merge 后 validate 报「roots 缺少必填字段」（本会话实测栽过一次，
见 split_humor_humus.py 的注释）。所以两根都在此直接建，成员从一开始就写进 word_ids。

两族的词源在各词的 origin 里已写对，画面也已写好，本脚本只补根与挂接。
carus 各词的 origin 里那句「本项目未为 carus 族建根」现在不成立了，一并改掉。

【近邻】库中已有 carrus（拉丁 carrus 四轮货车，借自高卢语，8 员 car/carry/charge…），
与 carus（亲爱的）**不同源**——cherish 曾被匹配器误判到那边。两根的 origin 互相
写明界线，措辞落在第二道门 CONTRAST 的窗口内。
"""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

ROOTS = [
    {
        "id": "charassein",
        "root": "charassein",
        "variants": ["charact", "charakt", "charass"],
        "origin": ("希腊语 kharassein（刻、划）→ kharakter（刻下的印记、烙印）；"
                   "kharax（尖桩）更早词源不明。刻痕一旦嵌进去便改不动，"
                   "故由「印记」转出「性格、特征」"),
        "core_concept": "a mark cut in, too deep to rub out / 刻进去的那道痕，擦不掉也改不动",
        "core_image": "刀尖在木板上划下几道，木屑翻起，痕嵌进纹理里，谁看都认得出是哪一块",
        "english_definition": "to engrave, to cut a mark; hence a distinctive stamp",
        "word_ids": ["character", "characteristic", "characterize"],
        "domain": "domain-perceive",
        "concept_id": "concept-charassein-engrave",
        "concept_zh": "刻下的印记",
    },
    {
        "id": "carus",
        "root": "carus",
        "variants": ["char", "cher", "cares"],
        "origin": ("拉丁语 carus（亲爱的、贵重的）→ caritas（珍视之情）；"
                   "经古法语 chier / cherir 与意大利语 caro / carezza 入英语。"
                   "与库中 carrus（四轮货车，借自高卢语）**不同源**，勿混"),
        "core_concept": "holding something dear enough to handle it gently / 看得贵重，于是手上就轻",
        "core_image": "一件旧物拿在手里，指头不敢用力，放下时还垫了一层软布",
        "english_definition": "dear, precious; costly",
        "word_ids": ["caress", "charity", "cherish"],
        "domain": "domain-hold",
        "concept_id": "concept-carus-dear",
        "concept_zh": "看得贵重",
    },
]

LOGIC = {
    "character": "charact（charassein 刻）+ -er → 刻下来的那个印记 → 一个人身上改不动的那些",
    "characteristic": "charact（charassein 刻）+ -istic → 属于那个刻痕的 → 一眼认得出的特点",
    "characterize": "charact（charassein 刻）+ -ize → 拿刻痕把它标出来 → 描述其特征",
    "charity": "char（carus 亲爱、贵重）+ -ity → 把别人看得贵重这份心 → 施予、慈善",
    "cherish": "cher（← chier ← carus 亲爱）+ -ish → 当贵重东西那样对待 → 珍爱",
    "caress": "cares（← carezza ← carus 亲爱）→ 把人当贵重物件那样碰 → 轻抚",
}
# carus 各词 origin 里这句现在不成立了。**前置标点两种都有**——charity 用分号、
# caress 用逗号，只匹配一种会漏掉一条（实测漏过 caress）。
STALE = "本项目未为 carus 族建根"


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    words, roots = load("words.json"), load("roots.json")
    concepts, rels, doms = load("concepts.json"), load("relations.json"), load("domains.json")
    wmap = {w["id"]: w for w in words["words"]}
    rids = {r["id"] for r in roots["roots"]}
    done = []

    for spec in ROOTS:
        rid = spec["id"]
        # 撞名红线：两个方向都查
        if rid in wmap:
            print(f"[FAIL] 根 id {rid} 与单词同名")
            return 1
        for w in spec["word_ids"]:
            if w not in wmap:
                print(f"[FAIL] {w} 不在库中")
                return 1
            if wmap[w].get("root_ids"):
                print(f"[FAIL] {w} 已挂 {wmap[w]['root_ids']}，本脚本只处理孤立词条")
                return 1
        if rid in rids:
            done.append(f"{rid}: 根已存在，跳过建根")
        else:
            roots["roots"].append({k: v for k, v in spec.items()
                                   if k not in ("domain", "concept_id", "concept_zh")})
            done.append(f"roots: 新建 {rid}（{len(spec['word_ids'])} 员）")
            for d in (doms["domains"] if isinstance(doms, dict) else doms):
                if d["id"] == spec["domain"] and rid not in d["root_ids"]:
                    d["root_ids"].append(rid)
                    d["root_ids"].sort()
                    done.append(f"domains: {rid} 归入 {spec['domain']}")
            if not any(c["id"] == spec["concept_id"] for c in concepts["concepts"]):
                concepts["concepts"].append({
                    "id": spec["concept_id"],
                    "concept": spec["core_concept"].split(" / ")[0],
                    "chinese": spec["concept_zh"],
                    "core_image": spec["core_image"],
                    "root_ids": [rid],
                    "word_ids": sorted(spec["word_ids"]),
                })
                done.append(f"concepts: 新建 {spec['concept_id']}")

        for w in spec["word_ids"]:
            e = wmap[w]
            e["root_ids"] = [rid]
            e["root_logic"] = LOGIC[w]
            e["decomposable"] = "root"
            e.pop("decomposable_note", None)
            if STALE in (e.get("origin") or ""):
                o = e["origin"]
                i = o.find(STALE)
                # 连同它前面那个标点一起去掉，别留下孤立的「；」或「，」
                cut = i - 1 if i > 0 and o[i - 1] in "；，;," else i
                e["origin"] = o[:cut] + o[i + len(STALE):]
                done.append(f"  {w}: origin 去掉「未为 carus 族建根」那句")
            if not any(x.get("to") == w and x.get("type") == "root"
                       for x in rels["relations"]):
                rels["relations"].append({"from": rid, "to": w,
                                          "type": "root", "note": LOGIC[w]})
            done.append(f"  {w}: 孤立词条 → {rid}")

    for d in done:
        print("  " + d)
    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    for n, o in (("words.json", words), ("roots.json", roots),
                 ("concepts.json", concepts), ("relations.json", rels),
                 ("domains.json", doms)):
        save(n, o)
    print(f"\n已写入 5 个文件，{len(done)} 处改动")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
