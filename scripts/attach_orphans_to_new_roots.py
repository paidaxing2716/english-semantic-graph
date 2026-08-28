#!/usr/bin/env python3
"""把库中已有的无根孤立词条挂进新建的词根，四处同步。

    python scripts/attach_orphans_to_new_roots.py --dry-run
    python scripts/attach_orphans_to_new_roots.py

【为什么要单独一步】这些词已在库中（多为日耳曼型孤立词条），走不了
entries_from_draft——那条管道遇到已入库的词会报「已在词库中，勿重复入库」。
而新根是由批次的 R 行建的，所以顺序必然是：先建根写新词 → 再把老词挂进去。

ATTACH 是累积记录，脚本幂等：已挂好的词会被跳过，可反复跑。
每条都写明 root_logic——挂根就必填，留空会被 review.py 挡下。
"""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

# 单词 -> (词根 id, root_logic)
ATTACH = {
    # ---- 第七十七批建的 5 个根 ----
    "apparatus": ("parare",
                  "ap-（ad- 朝）+ par（parare 备好）+ -atus → 为一件事摆出来的那一整套家伙"),
    "ascend": ("scandere", "a-（ad- 向）+ scend（scandere 攀）→ 顺着梯子一级级往上挪"),
    "descent": ("scandere", "de-（往下）+ scent（scandere 攀）→ 顺原路一级级退下来；也指血脉往下传的那条线"),
    "descendant": ("scandere", "de-（往下）+ scend（scandere 攀）+ -ant（人）→ 顺着这道梯子往下传的那一支"),
    "dessert": ("servire", "des-（撤去）+ sert（servire 伺候、上菜）→ 正餐撤下桌后才端上的那一道"),
    "deserve": ("servire", "de-（彻底）+ serve（servire 伺候）→ 伺候得够本，换来该得的那份"),
    "command": ("mandare", "com-（合力）+ mand（mandare 交托）→ 把差事连话一并压到手上，责令照办"),
    "commend": ("mandare", "com-（郑重）+ mend（mandare 交托）→ 把人或物郑重交到对方手上并担保"),
    "accompany": ("panis", "ac-（ad- 朝）+ company（← panis 面包）→ 与分饼的那伙人一道上路"),
    # ---- 第七十八批（chunk86）建的 5 个根，合并后再启用 ----
    "division": ("dividere", "di-（分开）+ vis（dividere 分）+ -ion → 分出来的那一份或那道界"),
    "device": ("dividere", "de-（从）+ vice（dividere 分）→ 分着琢磨出来的那个巧法子，落成实物即器械"),
    "devise": ("dividere", "de-（从）+ vise（dividere 分）→ 把事情拆开来琢磨，想出个法子"),
    "distinct": ("stinguere", "di-（分开）+ stinct（stinguere 戳）→ 戳出记号所以彼此分得清"),
    "distinction": ("stinguere", "di-（分开）+ stinct（stinguere 戳）+ -ion → 戳出来的那道分别"),
    "distinguish": ("stinguere", "di-（分开）+ stingu（stinguere 戳）→ 拿尖头戳出记号，把两样分开"),
    "eminent": ("minere", "e-（ex- 向外）+ min（minere 凸出）→ 从一片人里鼓出来，高过四周"),
    "mountain": ("minere", "mount（← minere 凸出的那块地）+ -ain → 从平地鼓起来的那一大块"),
    "mount": ("minere", "minere（凸出）→ 鼓起来的那块地；登上它即为登、骑"),
    "architect": ("tekton", "archi-（为首）+ tect（tekton 匠人）→ 一群匠人里领头拿主张的那个"),
    "architecture": ("tekton", "archi-（为首）+ tect（tekton 匠人）+ -ure → 领头匠人立起来的那套法式"),
    "epidemic": ("demos", "epi-（落在上头）+ dem（demos 民众）→ 落到一方百姓身上并铺开的那场病"),
    # ---- 第八十一批（chunk91）建的 2 个根 ----
    "applaud": ("plaudere", "ap-（ad- 朝）+ plaud（plaudere 拍手）→ 朝着台上把两掌拍响"),
    "applause": ("plaudere", "ap-（ad- 朝）+ plaus（plaudere 拍手）+ -e → 朝台上拍出来的那一片响"),
    "atmosphere": ("sphaira", "atmo-（气）+ sphere（← sphaira 球）→ 罩在这颗球外头那层气"),
    # ---- 三处小挂接：根已建好，但这几个词先入库成了孤立词条 ----
    # empire/emperor 自己的 origin 写着「承义的是下令统辖这一支，不是备置，故未挂
    # parare」——那句等于说这一支该有自己的根（imperare），现在有了。
    "empire": ("imperare", "emp（← imperium 号令之权）-ire → 号令所能统辖的那一整片"),
    "emperor": ("imperare", "emper（← imperator 发号令的统帅）+ -or（人）→ 发号令的那个人"),
    # exemplify ← exemplum（从整批里取出的一件）← eximere ← emere（取）；
    # 根的 origin 已明写这条链和 exemplum 这一支。
    "exemplify": ("emere", "exempl（← exemplum 从整批取出的那一件）+ -ify（使）→ 把取出的那一件摆出来替整批说话"),
    # similis 的 origin 明写「ad-＋similis 一支出 assimilare」。
    "assimilate": ("similis", "as-（ad- 朝着）+ simil（similis 相像）+ -ate → 朝着周围变得同一样"),
    # migrare 根建好后回收先前入库的孤立词；origin 本身已写明 in-/ex- + migrare。
    "immigrant": ("migrare", "im-（in- 进入）+ migr（migrare 迁移）+ -ant → 迁进来的人"),
    "emigrate": ("migrare", "e-（ex- 离开）+ migr（migrare 迁移）+ -ate → 从原处迁出去"),
    "pet": ("pet-seek", "pet（petere 追求）→ 主动向某人讨取关注或抚爱"),
}


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
    concepts, rels = load("concepts.json"), load("relations.json")
    wmap = {w["id"]: w for w in words["words"]}
    rmap = {r["id"]: r for r in roots["roots"]}

    done, skip, wait = [], [], []
    for wid, (rid, logic) in ATTACH.items():
        if rid not in rmap:
            wait.append(f"{wid} → {rid}（根尚未建，等那批合并后再跑）")
            continue
        w = wmap.get(wid)
        if w is None:
            skip.append(f"{wid} 不在库中")
            continue
        if w.get("root_ids"):
            skip.append(f"{wid} 已挂 {w['root_ids']}")
            continue
        w["root_ids"] = [rid]
        w["root_logic"] = logic
        w["decomposable"] = "root"
        w.pop("decomposable_note", None)
        r = rmap[rid]
        if wid not in (r.get("word_ids") or []):
            r.setdefault("word_ids", []).append(wid)
            r["word_ids"].sort()
        for c in concepts["concepts"]:
            if rid in (c.get("root_ids") or []) \
                    and wid not in (c.get("word_ids") or []):
                c.setdefault("word_ids", []).append(wid)
                c["word_ids"].sort()
        if not any(x.get("to") == wid and x.get("type") == "root"
                   for x in rels["relations"]):
            rels["relations"].append({"from": rid, "to": wid,
                                      "type": "root", "note": logic})
        done.append(f"{wid}: 孤立词条 → {rid}")

    for d in done:
        print("  " + d)
    if skip:
        print(f"\n  跳过 {len(skip)}：" + "；".join(skip[:6]))
    if wait:
        print(f"\n  等待 {len(wait)}：")
        for x in wait:
            print("    " + x)
    if a.dry_run:
        print("\n（dry-run，未写入）")
        return 0
    for n, o in (("words.json", words), ("roots.json", roots),
                 ("concepts.json", concepts), ("relations.json", rels)):
        save(n, o)
    print(f"\n已写入 4 个文件，挂上 {len(done)} 词")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
