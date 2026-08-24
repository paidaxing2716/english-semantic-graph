#!/usr/bin/env python3
"""把子代理起草的精简 TSV 转成完整词条 JSON，并在生成期跑完质量门。

用法：
    python scripts/entries_from_draft.py drafts/g01.tsv   -o ai_pipeline/batch54.json
    python scripts/entries_from_draft.py drafts/r65.tsv   -o ai_pipeline/batch65.json

【为什么要这个】
实测：日耳曼批走本脚本，我方成本约 19 字节/词（只付一份派发提示词）；
词根批过去由我手写 build_batchNN.py 的 Python 字面量，1141 字节/词——
同样的内容差 60 倍。词根型只比日耳曼型多三样东西（root_ids、root_logic、
近反义词），没有任何理由手写。本脚本因此同时吃两种行。

固定字段自动填，Q1/Q12 等自检前移到生成期：review.py check 不查 Q12，
只有合并后的 validate.py 才查，不自检就会白跑一轮 merge 再回滚
（pair/hum/suitable 那次就是这么栽的）。

【行格式】每行第一列是标签，决定这行按哪套列规格解析。
标签让列数校验能分型进行——13 列的词根行漏一列，不会被误当成 12 列的
合法行放过；而这正是必须防的：漏中间某列会让后面字段整体错位，
拿 concept 当 expansions，各列都是自由文本，跑得通、看不出。

  R 行 —— 新建词根（10 列）
    1  R
    2  root_id      词根 id，用拉丁语原形，如 jungere。**不得与任何单词同名**
                    （否则 relations 里会出现 forma→forma 自环，已栽过一次）
    3  variants     词形变体，用 / 分隔，如「join/junct/jug」；无则留空
    4  origin       词源，写清本象，如「拉丁语 jungere（把两物套到一处），
                    过去分词 junctus；jugum（牛轭）同根——两头牛套进同一副轭」
    5  core_concept 「英文短语 / 中文」，如「two things set into one yoke / 套进同一副轭」
    6  core_image   词根的核心画面（中文）
    7  english_def  英文定义，动词原形，如「to yoke, join together」
    8  concept_slug 概念 id 的尾巴，小写英文单词，如 yoke
                    → 拼成 concept-jungere-yoke
    9  concept_zh   概念中文名，2-5 字，如「套在一处」
   10  domain       所属语义域 id，如 domain-hold

  W 行 —— 单词（14 列）
    1  W
    2  word         单词
    3  pos          词性；多词性用 / 分隔，如「noun / verb」
    4  phonetic     音标，含斜杠
    5  root_ids     词根 id，多个用 / 分隔；**留空则本词按日耳曼型处理**
    6  root_logic   拆解逻辑，如「di-（分开）+ vorce（vertere 转）→ 各自转开」
                    有 root_ids 时必填；无 root_ids 时必须留空
    7  origin       词源
    8  native       英文释义（一句，小写开头，不加句号）
    9  image        核心画面（中文，一个具体场景；**不得出现任何中文义项**）
   10  zh           中文义项，用 / 分隔
   11  examples     两个英文例句，用 | 分隔
   12  concept      核心概念，格式「英文短语 – 中文解释」
   13  expansions   语义扩展，多条用 | 分隔；单义词可留空
   14  hint         recall_hint，多数情况留空。**当 root_logic 里出现 3 次及以上
                    中文义项时必填**：回想模式会遮掉中文，那时 root_logic 只剩
                    一串方块，得有一条不点名义项的推导兜着。脚本会替你判要不要填。

  兼容：不带标签的 10 列行仍按旧日耳曼规格解析，老草稿不用改。

【硬规则，子代理必须遵守】
  · image 里不能出现 zh 的任何一项（长度≥2 的）。这是 Q12 的红线：
    遮住单词和中文后，画面是唯一的记忆抓手，点名义项等于自泄答案。
  · zh 有 2 项以上时，expansions 必填（Q1）。
  · 例句必须 2 条。
  · 词根行的 root_id 必须是拉丁语原形，且先查 roots.json 的 origin ——
    同一个词根常已用别的拉丁词形建过模（stare=sta、movere=mov、
    magnus⊂maior），报成新根会造重复根。
  · 日耳曼行不写 root_logic、不指派词根。

【自动填】
  word_ids（词根/概念两处的回填）、decomposable、decomposable_note、
  concept 的 core_image（取词根的）、synonyms/antonyms/related 默认空。
  回填自动做的理由：这三处手写最容易漏，漏了 validate 才报，
  而那时已经 merge 进 data/ 了。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NOTE_DEFAULT = "日耳曼核心词，本身即词根，无拉丁词缀可拆"


def split_on(s, sep):
    return [x.strip() for x in s.split(sep) if x.strip()]


def build_root(cols, lineno):
    """R 行 → (root, concept, domain_id)"""
    if len(cols) != 10:
        raise ValueError(
            f"第 {lineno} 行 R 标签有 {len(cols)} 列，规格要求 10 列"
            f"（variants 可为空，但制表符不能省）")
    (_, rid, variants, origin, cc, image, edef, slug, czh, dom) = [c.strip() for c in cols]

    for name, v in (("root_id", rid), ("origin", origin), ("core_concept", cc),
                    ("core_image", image), ("english_def", edef),
                    ("concept_slug", slug), ("concept_zh", czh), ("domain", dom)):
        if not v:
            raise ValueError(f"第 {lineno} 行 R：{name} 不能为空")
    if "/" not in cc:
        raise ValueError(f"{rid}: core_concept 缺「英文 / 中文」分隔符")
    if not slug.replace("-", "").isalpha() or slug != slug.lower():
        raise ValueError(f"{rid}: concept_slug {slug!r} 应为小写英文")

    root = {
        "id": rid, "root": rid,
        "variants": split_on(variants, "/"),
        "origin": origin,
        "core_concept": cc,
        "core_image": image,
        "english_definition": edef,
        "word_ids": [],
    }
    concept = {
        "id": f"concept-{rid}-{slug}",
        "concept": cc.split("/")[0].strip(),
        "chinese": czh,
        "core_image": image,          # 与词根同画面，不让子代理重写一遍
        "root_ids": [rid],
        "word_ids": [],
    }
    return root, concept, dom


def build_word(cols, lineno, legacy=False):
    """W 行（或旧式无标签 10 列行）→ word"""
    if legacy:
        # 旧日耳曼规格：10 列，无标签、无 root_ids/root_logic
        if len(cols) != 10:
            raise ValueError(
                f"第 {lineno} 行有 {len(cols)} 列，旧日耳曼规格要求 10 列"
                f"（单义词第 10 列可为空，但前面的制表符不能省）")
        (word, pos, ph, origin, native, image, zh, ex, concept, exps) = \
            [c.strip() for c in cols]
        rid_s, logic = "", ""
        hint = ""
    else:
        if len(cols) != 14:
            raise ValueError(
                f"第 {lineno} 行 W 标签有 {len(cols)} 列，规格要求 14 列"
                f"（root_ids/root_logic/expansions/hint 可为空，但制表符不能省）")
        (_, word, pos, ph, rid_s, logic, origin, native, image, zh, ex,
         concept, exps, hint) = [c.strip() for c in cols]

    zh_list = split_on(zh, "/")
    ex_list = split_on(ex, "|")
    exp_list = split_on(exps, "|")
    rid_list = split_on(rid_s, "/")

    w = {
        "id": word, "word": word, "pos": pos, "phonetic": ph,
        "decomposable": "root" if rid_list else "germanic",
        "root_ids": rid_list,
        "root_logic": logic,
        "origin": origin,
        "native_definition": native,
        "core_concept": concept,
        "core_image": image,
        "chinese": zh_list,
        "examples": ex_list,
        "synonyms": [], "antonyms": [], "related": [],
        "semantic_expansions": exp_list,
    }
    if hint:
        w["recall_hint"] = hint
    if not rid_list:
        # review.py 只在「标为不可拆」时才允许空 root_logic，且此时
        # decomposable_note 必填——两者是一套，不能只填一半。
        w["decomposable_note"] = NOTE_DEFAULT

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
    if rid_list and not logic:
        raise ValueError(f"{word}: 指派了词根 {rid_list} 却没写 root_logic")
    if not rid_list and logic:
        raise ValueError(
            f"{word}: 没指派词根却写了 root_logic——review.py 会判"
            f"「标为不可拆却写了 root_logic」")
    if rid_list and not hint:
        # 复刻 validate.py 的触发条件（Q12 后半段）：root_logic 里中文义项
        # 出现 ≥3 次时，遮罩后只剩方块，必须有 recall_hint。
        # 在这里挡，是为了不等 merge 之后才发现——那时得回滚 data/。
        blanks = sum(logic.count(x) for x in zh_list if len(x) >= 2)
        if blanks >= 3:
            raise ValueError(
                f"{word}: root_logic 含 {blanks} 处中文义项，遮罩后提示不足，"
                f"第 14 列 hint 必填（写一条不点名义项的推导）")
    return w


def load_db():
    def rd(name, key):
        p = ROOT / "data" / name
        if not p.exists():
            return []
        o = json.loads(p.read_text(encoding="utf-8"))
        return o if isinstance(o, list) else o.get(key, [])
    return (
        {x["id"] for x in rd("words.json", "words")},
        {x["id"] for x in rd("roots.json", "roots")},
        {d["id"] for d in rd("domains.json", "domains")},
        {x["id"] for x in rd("concepts.json", "concepts")},
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", help="子代理起草的 TSV")
    ap.add_argument("-o", "--out", required=True, help="输出 batchNN.json")
    ap.add_argument("--allow-dup", action="store_true",
                    help="允许与词库已有词重复（默认报错）")
    a = ap.parse_args()

    have_w, have_r, have_d, have_c = load_db()

    words, roots, concepts, errs = [], [], [], []
    dom_add = {}
    for i, line in enumerate(Path(a.tsv).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        tag = cols[0].strip()
        try:
            if tag == "R":
                r, c, dom = build_root(cols, i)
                if r["id"] in have_r:
                    errs.append(f"{r['id']}: 词根已存在——先查 roots.json 的 origin，"
                                f"同一个根常已用别的拉丁词形建过模")
                    continue
                if c["id"] in have_c:
                    errs.append(f"{c['id']}: 概念 id 已存在")
                    continue
                if dom not in have_d:
                    errs.append(f"{r['id']}: 语义域 {dom} 不存在，可选 {sorted(have_d)}")
                    continue
                roots.append(r)
                concepts.append(c)
                dom_add.setdefault(dom, []).append(r["id"])
            elif tag == "W":
                words.append(build_word(cols, i))
            else:
                words.append(build_word(cols, i, legacy=True))
        except ValueError as e:
            errs.append(str(e))

    for w in words:
        if w["id"] in have_w and not a.allow_dup:
            errs.append(f"{w['id']}: 已在词库中，勿重复入库")

    seen = {}
    for w in words:
        seen[w["id"]] = seen.get(w["id"], 0) + 1
    errs += [f"{k}: 本批内重复 {n} 次" for k, n in seen.items() if n > 1]

    new_r = {r["id"] for r in roots}
    all_r = have_r | new_r
    batch_w = {w["id"] for w in words}

    # 撞名红线：词根 id 与单词 id 相同有两种后果，第二种更隐蔽。
    #   a) 该词恰好是这个根的成员 → relations 出现 forma→forma 自环（已栽过）
    #   b) 同形异源（英文 dare vs 拉丁 dare）→ 无自环，但 frontend 的 idMap
    #      装域/根/概念/单词用同一个键空间，单词后插入、把词根节点顶掉，
    #      成员词连到错误类型的节点上。每道门都绿，只有画面上看得出来。
    # 所以这里一律挡，不区分是不是成员词。
    for rid in sorted(new_r & (have_w | batch_w)):
        errs.append(f"{rid}: 词根 id 与单词同名——前端 idMap 会让单词顶掉词根节点，"
                    f"换拉丁原形（如 dare-give）")

    for w in words:
        for rid in w["root_ids"]:
            if rid not in all_r:
                errs.append(f"{w['id']}: 词根 {rid} 不存在（本批也没建）")

    if errs:
        print(f"[FAIL] {len(errs)} 条不合格，未输出：")
        for e in errs:
            print("   ", e)
        return 1

    # ---- 回填 word_ids ----
    # 手写最容易漏这一步，而漏了要到 merge 之后 validate 才报。
    by_root = {}
    for w in words:
        for rid in w["root_ids"]:
            by_root.setdefault(rid, []).append(w["id"])
    for r in roots:
        r["word_ids"] = by_root.get(r["id"], [])
    for c in concepts:
        c["word_ids"] = by_root.get(c["root_ids"][0], [])

    out = {}
    if roots:
        out["roots"] = roots
        out["concepts"] = concepts
        out["domain_add"] = dom_add
    out["words"] = words

    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2)
                           + "\n", encoding="utf-8")
    nr = sum(1 for w in words if w["root_ids"])
    print(f"[OK] 写入 {a.out}：{len(words)} 词（词根型 {nr} / 日耳曼型 {len(words)-nr}）"
          f"，新建词根 {len(roots)} 个（全部通过生成期自检）")
    if roots:
        empty = [r["id"] for r in roots if not r["word_ids"]]
        if empty:
            print(f"[注意] 这些新根本批没有成员词：{empty}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
