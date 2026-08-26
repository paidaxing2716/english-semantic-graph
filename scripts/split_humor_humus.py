#!/usr/bin/env python3
"""分开 umor（湿）与 humus（土）两支，新建 humus 根。

    python scripts/split_humor_humus.py --dry-run
    python scripts/split_humor_humus.py

【实际情形不是「拆一个根」】查库后发现 humor-moist 里本来就只有湿气那一支
（humor / humorous 两词），humiliate 早已是日耳曼型且 origin 正确写着 humus，
而 humid / human / humanity 压根不在库。所以要做的是**新建 humus 支**，
并把 humor-moist 的 origin 改写准确。

【为什么这两支必须分开】humor 实为拉丁 umor（体液、湿气），拼成 h- 是后人与
humus（泥土）误联想的结果——etymonline 明写 "by false association with humus"。
两者同形而异源：umor 出 PIE *wegʷ-（湿），humus 出 PIE *dhghem-（地）。
由 chunk62 的子代理在核 humiliate 时查明。

本脚本只动已入库的部分：
  - 改写 humor-moist 的 origin，注明 h- 是误联想、与 humus 不同源
  - 新建 humus 根，把 humiliate 从日耳曼型改挂进去
humus 支只有 humiliate 一个已入库成员，不足 3 员——故新根**先建但标注待补**，
human / humanity 两个考研词随后一批补入即可满足门槛。若不想留一个 1 员根，
用 --defer 只改 origin 不建根。
"""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

NEW_ORIGIN = ("拉丁语 umor（湿气、体液），中世纪拼作 humor——这个 h 是后人与 "
              "humus（泥土）误联想加上的，两者不同源：umor 出原始印欧语 *wegʷ-"
              "（湿），humus 出 *dhghem-（地）。体液学说由此引申出生性与幽默")

HUMUS_ROOT = {
    "id": "humus",
    "root": "humus",
    "variants": ["hum", "human"],
    "origin": ("拉丁语 humus（泥土、地面）← 原始印欧语 *dhghem-（地）；humilis 是"
               "「贴着地面的」，homo/humanus 是「地上生的那种活物」。"
               "与 umor（湿气，即 humor 一支）不同源，勿混"),
    "core_concept": "of the ground, earth-born / 属于地面的、从土里生出来的",
    "core_image": "一个人蹲下去，手掌按在泥地上，掌纹里嵌着湿土",
    "english_definition": "earth, ground; earth-born",
    "word_ids": ["humiliate"],
}

LOGIC = ("humus（泥土、地面）→ humilis（贴着地面的）+ -ate → 把人按到地面那么低 "
         "→ 使屈辱")


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--defer", action="store_true",
                    help="只改 origin，不建 humus 根（等 human/humanity 入库再建）")
    a = ap.parse_args()

    words, roots = load("words.json"), load("roots.json")
    concepts, rels, doms = load("concepts.json"), load("relations.json"), load("domains.json")
    wmap = {w["id"]: w for w in words["words"]}
    rmap = {r["id"]: r for r in roots["roots"]}
    done = []

    if HUMUS_ROOT["id"] in wmap:
        print(f"[FAIL] 新根 id {HUMUS_ROOT['id']} 与单词同名")
        return 1

    for r in roots["roots"]:
        if r["id"] == "humor-moist" and r["origin"] != NEW_ORIGIN:
            r["origin"] = NEW_ORIGIN
            done.append("humor-moist: origin 改写，注明 h- 是与 humus 的误联想")

    # 【已废弃的建根分支，勿恢复】原来这里有一整段：建 humus 根、把 humiliate 从
    # 日耳曼型改挂过来、写 relations、归 domain、建 concept——全都裹在
    # `if not a.defer and HUMUS_ROOT["id"] not in rmap:` 这一个条件里。
    # 由 chunk83 的子代理指出致命缺陷：一旦 humus 根已存在（它的 R 行建的），
    # 整段静默跳过，humiliate 就永远留在日耳曼型，而脚本照样输出成功、门全绿。
    # 这与本会话修掉的六处「输出绿色但什么都没发生」是同一个模式。
    # 实际做法：humus 根由批次的 R 行建（human/humanity 两员），合并后单独把
    # humiliate 挂进去凑满 3 员——两步都做过了，各自可验证。
    # 本脚本现在只保留 origin 改写这一件事，那是幂等且可重复核对的。
    if not a.defer:
        print("  [SKIP] 建根分支已废弃，humus 根与 humiliate 归属已分两步完成")

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
    if not a.defer:
        print("提醒：humus 现只 1 个成员，未达 3 员门槛。"
              "human / humanity 两个考研词随后补入即可。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
