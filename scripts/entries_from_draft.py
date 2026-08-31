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
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NOTE_DEFAULT = "日耳曼核心词，本身即词根，无拉丁词缀可拆"
# 借词用的文案。只陈述「本项目未为它建根」这个事实，不断言「没有词缀」——
# 很多这类词的 origin 明写着词缀（abound 的 origin 就写「ab-（自）+ unda」），
# 断言无词缀是用一个新错陈述换掉旧的。真实原因（族不足 3 员／拆了不助记）
# 不该由脚本替人断定。与 scripts/fix_decomposable_notes.py 的文案保持一致。
NOTE_BORROWED = {
    "法语": "经法语入英语的借词，本项目未为其词族建根，按整体记",
    "拉丁": "拉丁借词，本项目未为其词族建根，按整体记",
    "希腊": "希腊借词，本项目未为其词族建根，按整体记",
    "意大利": "借自意大利语，本项目未为其词族建根，按整体记",
    "西班牙": "借自西班牙语，本项目未为其词族建根，按整体记",
    "荷兰": "借自荷兰语，本项目未为其词族建根，按整体记",
    "阿拉伯": "借自阿拉伯语，本项目未为其词族建根，按整体记",
    "梵语": "借自梵语，本项目未为其词族建根，按整体记",
    "俄语": "借自俄语，本项目未为其词族建根，按整体记",
    "日语": "借自日语，本项目未为其词族建根，按整体记",
    # 凯尔特语支：slogan ← 苏格兰盖尔语 sluagh-ghairm 是这一档的唯一实例，
    # 但没有这个键时它会落回「日耳曼核心词」——盖尔语既不在借源键里，也不含
    # 日耳曼标记，分流器无从判别。
    "盖尔": "借自盖尔语，本项目未为其词族建根，按整体记",
    "爱尔兰": "借自爱尔兰语，本项目未为其词族建根，按整体记",
}
NOTE_EARLY_LOAN = "早期借词，经古英语或中古英语阶段传入，词形已归化，无可拆的词缀"
# 第四档：源头是日耳曼语支、但经罗曼语（多为法语）回流进英语的词。
# 既不是「日耳曼核心词」（那句暗示古英语直接继承），也不是「法语借词」（源头不在
# 罗曼语）。engage / engagement / border / garden 这类都属此列。
NOTE_GERMANIC_VIA_ROMANCE = "源头在日耳曼语支，经法语回流入英语，本项目未为其词族建根"
GERMANIC_MARK = ("古英语", "原始日耳曼", "中古英语", "古诺斯", "古诺尔斯",
                 "古高地德", "古撒克逊", "原始西日耳曼")
# 日耳曼语支但不经古英语直接继承的来源
GERMANIC_OTHER = ("法兰克语", "古法兰克", "哥特语", "古弗里斯兰", "古荷兰",
                  "中古荷兰", "原始北日耳曼")
# 否定措辞：origin 里写「非拉丁」「不是希腊语」时，那个语言名是被排除的对象，
# 不能当来源。此前没防这一条，「日耳曼源，非拉丁」被判成「拉丁借词」——
# 与原文意思正相反（由 chunk103 的子代理指出）。
NEGATE = ("非", "不是", "而非", "无关", "不属", "并非")


def classify_note(origin):
    """按 origin 的语源线索给 decomposable_note 分流。

    三档而非两档。此前只分「有日耳曼词形 → 日耳曼核心词」与「有外语词形 → 借词」，
    漏了第三种：**经古英语传入的早期借词**——origin 形如「古英语 ancor ← 拉丁语
    ancora」，日耳曼标记在前所以被判成「日耳曼核心词，本身即词根」，而它压根不是
    日耳曼词。实测库里 65 条属此类（belt ← balteus、cheese ← caseus、candle ←
    candela、turn ← tornare）。由 chunk76 的子代理写 turn 时指出。
    判据是 `←` 后面紧跟外语名：日耳曼词形是传入路径，箭头指向的才是终极来源。
    """
    o = origin or ""
    # 日耳曼语支但经罗曼语回流的，单独一档（法兰克语那类）
    if any(k in o for k in GERMANIC_OTHER)             and not any(k in o for k in GERMANIC_MARK):
        return NOTE_GERMANIC_VIA_ROMANCE
    if any(k in o for k in GERMANIC_MARK):
        for k in NOTE_BORROWED:
            if re.search(r"←[^←]{0,14}" + k, o):
                return NOTE_EARLY_LOAN
        return NOTE_DEFAULT
    # 取**最后一个 ← 之后**那一跳的语言。三次才改对，记下来：
    #   ① 按字典键序取第一个命中 → 「中世纪拉丁语 X ← 阿拉伯语 Y」判成拉丁（错）
    #   ② 改取全文最右的命中 → 同一条 origin 末尾又写「英语按拉丁式加 -ate」，
    #      「拉丁」位置反而更右，还是判成拉丁（错）
    #   ③ 只看最后一个箭头之后的那一段 —— 那才是词源链的终点
    # 由 chunk90 的子代理指出 assassinate 这一例。
    def earliest(seg):
        """取该段里位置最靠前的语言名——紧跟箭头的那个才是来源。
        尾段常在末尾又提一次别的语言（assassinate 那条写「英语按拉丁式加 -ate」），
        按字典键序取会让「拉丁」压过「阿拉伯」，所以必须按出现位置取。
        被否定措辞紧挨着的语言名跳过（「非拉丁」里的拉丁不是来源）。"""
        h = []
        for k in NOTE_BORROWED:
            i = seg.find(k)
            if i < 0:
                continue
            if any(x in seg[max(0, i - 4):i] for x in NEGATE):
                continue
            h.append((i, k))
        return NOTE_BORROWED[min(h)[1]] if h else None
    if "←" in o:
        note = earliest(o.rsplit("←", 1)[-1])
        if note:
            return note
    return earliest(o) or NOTE_DEFAULT


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
        # 14 列是旧格式，15 列是加了 collocations 的新格式，两者都收。
        # 【为什么这里要格外小心】此前「15 列」正是那个缺陷的特征：expansions 或
        # examples 里的 `|` 被误打成制表符，整行多出一列而两道门都放行，只有
        # awk -F'\t' 'NF!=14' 看得出来——本会话发生过三次（universal、promote、
        # accommodate）。现在 15 列合法了，那个特征就失效了，所以改用内容判别：
        # 真的第 15 列只放搭配（含 `——` 或为空），而错位挤出来的那一列是被截断的
        # 义项说明或例句片段。判反了会让错位重新变成静默失效。
        if len(cols) == 14:
            (_, word, pos, ph, rid_s, logic, origin, native, image, zh, ex,
             concept, exps, hint) = [c.strip() for c in cols]
            colloc = ""
        elif len(cols) == 15:
            (_, word, pos, ph, rid_s, logic, origin, native, image, zh, ex,
             concept, exps, hint, colloc) = [c.strip() for c in cols]
            if colloc and "——" not in colloc:
                raise ValueError(
                    f"第 {lineno} 行第 15 列不像搭配（缺 '——'）："
                    f"{colloc[:40]!r}。若这是 expansions/examples 里的 `|` 被误打成"
                    f"制表符挤出来的，改回 `|`；搭配格式是 `型式 —— 中文说明`")
            # 第 15 列为空也不能免检：错位可能把原本为空的 hint 挤到第 15 位，
            # 于是空的第 15 列「看起来合法」，而义项说明被挤进了 hint 列。
            # hint 是一条不点名义项的推导，绝不会长成「甲：…」这种义项条目式。
            if not colloc and re.match(r"^[^：:]{1,8}[：:]", hint):
                raise ValueError(
                    f"第 {lineno} 行第 14 列（hint）像义项说明而非回想提示："
                    f"{hint[:40]!r}，且第 15 列为空——多半是 expansions 里的 `|` "
                    f"被误打成制表符，整行往后错了一位。改回 `|`")
        else:
            raise ValueError(
                f"第 {lineno} 行 W 标签有 {len(cols)} 列，规格要求 14 或 15 列"
                f"（root_ids/root_logic/expansions/hint/collocations 可为空，"
                f"但制表符不能省）")

    zh_list = split_on(zh, "/")
    ex_list = split_on(ex, "|")
    exp_list = split_on(exps, "|")
    rid_list = split_on(rid_s, "/")
    colloc_list = split_on(colloc, "|")

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
    # 可选字段，只在有内容时写——避免给三千多个实词凭空加一个空数组
    if colloc_list:
        w["collocations"] = colloc_list
    if hint:
        w["recall_hint"] = hint
    if not rid_list:
        # review.py 只在「标为不可拆」时才允许空 root_logic，且此时
        # decomposable_note 必填——两者是一套，不能只填一半。
        #
        # 但「不挂词根」有两种原因，此前一律套用「日耳曼核心词」那句默认文案：
        #   a) 确实是日耳曼核心词（古英语 ceosan 那类）
        #   b) 拉丁/法语/希腊借词，只是拆开推不出可学联系、或该族凑不到 3 个成员
        # b 类被写成 a，实测全库积了 578 条错陈述（abandon 古法语、absorb 拉丁语
        # 都写着「日耳曼核心词」），由 chunk56 的子代理指出。按 origin 的语源线索
        # 分流；origin 无线索时仍用默认句（判不了就别猜）。
        w["decomposable_note"] = classify_note(origin)

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

    # 反方向同样致命，但此前不查：本批新加的**单词**撞已建好的**词根** id。
    # 补词批里 new_r 是空集，上面那道门形同不存在，于是 minus（根，挂着
    # administer/minister/minor 等 6 词）遇上单词 minus 时照样放行——后果与
    # a)b) 完全一样，且更隐蔽，因为它不需要本批建任何新根。
    # 由 chunk64 的子代理发现，它扣下了那个词没写。
    for wid in sorted(batch_w & have_r):
        errs.append(f"{wid}: 单词与已有词根 id 同名——前端 idMap 会让它顶掉词根 "
                    f"{wid}，先按 dare→dare-give 的先例给词根改名再补这个词")

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
