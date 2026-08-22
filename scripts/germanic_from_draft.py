#!/usr/bin/env python3
"""把子代理起草的精简 TSV 转成完整的日耳曼词条 JSON，并在生成期跑完质量门。

用法：
    python scripts/germanic_from_draft.py drafts/g01.tsv -o ai_pipeline/batch54.json

【为什么要这个】
日耳曼词条共 14 个字段，其中 5 个是固定值（decomposable / root_ids /
root_logic / related），2 个高度套路（origin / decomposable_note 的句式）。
让子代理逐条写全 14 个字段，既慢又容易漏字段、写错格式。
本脚本把子代理的输出压到 7 列，其余自动填，并把 Q1/Q12 自检前移到生成期——
review.py check 不查 Q12，只有合并后的 validate.py 才查，不自检就会白跑一轮
merge 再回滚（disregard 那次就是这么栽的）。

【TSV 列（制表符分隔，7 列）】
    1 word        单词
    2 pos         词性（noun / verb / adjective / adverb...）
    3 phonetic    音标，含斜杠，如 /siːd/
    4 oe_origin   词源，只写古英语/原始日耳曼语那一句，如
                  「古英语 sæd ← 原始日耳曼语 *sēdiz（撒下之物）」
    5 native      英文释义（一句，小写开头，不加句号）
    6 image       核心画面（中文，一个具体场景；**不得出现任何中文义项**）
    7 zh          中文义项，用 / 分隔，如「种子/籽/起因」
    8 examples    两个英文例句，用 | 分隔
    9 concept     核心概念，格式「英文短语 – 中文解释」
   10 expansions  语义扩展，多条用 | 分隔；单义词可留空

【硬规则，子代理必须遵守】
  · image 里不能出现 zh 的任何一项（长度≥2 的）。这是 Q12 的红线：
    遮住单词和中文后，画面是唯一的记忆抓手，点名义项等于自泄答案。
  · zh 有 2 项以上时，expansions 必填（Q1）。
  · 例句必须 2 条。
  · 不写 root_logic、不指派词根——这类词没有可迁移的同族词。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NOTE_DEFAULT = "日耳曼核心词，本身即词根，无拉丁词缀可拆"


def build(row, lineno):
    cols = row.rstrip("\n").split("\t")
    if len(cols) < 9:
        raise ValueError(f"第 {lineno} 行只有 {len(cols)} 列，至少要 9 列")
    (word, pos, ph, origin, native, image, zh, ex, concept) = [c.strip() for c in cols[:9]]
    exps = cols[9].strip() if len(cols) > 9 else ""

    zh_list = [x.strip() for x in zh.split("/") if x.strip()]
    ex_list = [x.strip() for x in ex.split("|") if x.strip()]
    exp_list = [x.strip() for x in exps.split("|") if x.strip()]

    w = {
        "id": word, "word": word, "pos": pos, "phonetic": ph,
        "decomposable": "germanic",
        "decomposable_note": NOTE_DEFAULT,
        "root_ids": [], "root_logic": "",
        "origin": origin,
        "native_definition": native,
        "core_concept": concept,
        "core_image": image,
        "chinese": zh_list,
        "examples": ex_list,
        "synonyms": [], "antonyms": [], "related": [],
        "semantic_expansions": exp_list,
    }

    # ---- 生成期自检 ----
    for x in zh_list:
        if len(x) >= 2 and x in image:
            raise ValueError(
                f"{word}: core_image 点名义项「{x}」——遮罩后就没提示了（Q12 红线）")
    if len(zh_list) >= 2 and not exp_list:
        raise ValueError(f"{word}: 有 {len(zh_list)} 个义项却无 semantic_expansions（Q1）")
    if len(ex_list) < 2:
        raise ValueError(f"{word}: 例句 {len(ex_list)} 条，需 2 条")
    if not ph.startswith("/") or not ph.endswith("/"):
        raise ValueError(f"{word}: 音标 {ph!r} 应以斜杠包裹")
    if "–" not in concept and "-" not in concept:
        raise ValueError(f"{word}: core_concept 缺「英文 – 中文」分隔符")
    return w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", help="子代理起草的 TSV")
    ap.add_argument("-o", "--out", required=True, help="输出 batchNN.json")
    ap.add_argument("--allow-dup", action="store_true",
                    help="允许与词库已有词重复（默认报错）")
    a = ap.parse_args()

    have = set()
    wp = ROOT / "data" / "words.json"
    if wp.exists():
        o = json.loads(wp.read_text(encoding="utf-8"))
        have = {x["id"] for x in (o if isinstance(o, list) else o.get("words", []))}

    words, errs = [], []
    for i, line in enumerate(Path(a.tsv).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            w = build(line, i)
        except ValueError as e:
            errs.append(str(e))
            continue
        if w["id"] in have and not a.allow_dup:
            errs.append(f"{w['id']}: 已在词库中，勿重复入库")
            continue
        words.append(w)

    seen = {}
    for w in words:
        seen.setdefault(w["id"], 0)
        seen[w["id"]] += 1
    for k, n in seen.items():
        if n > 1:
            errs.append(f"{k}: 本批内重复 {n} 次")

    if errs:
        print(f"[FAIL] {len(errs)} 条不合格，未输出：")
        for e in errs:
            print("   ", e)
        return 1

    Path(a.out).write_text(json.dumps({"words": words}, ensure_ascii=False, indent=2)
                           + "\n", encoding="utf-8")
    print(f"[OK] {len(words)} 词写入 {a.out}（全部通过生成期 Q1/Q12 自检）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
