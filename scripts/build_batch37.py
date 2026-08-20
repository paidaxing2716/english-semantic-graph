#!/usr/bin/env python3
"""Generate batch37: four new families.

- auctoritas（权威/作者）新根：author / authentic / authority
- clarus（明亮清晰）新根：clarify / clarity / declare
- crescere（生长）新根：increase / decrease / increasingly
- gerere（携带/进行）新根：gesture / suggest / digest

共 12 词。教训沿用 batch36：domain_add 同域累积、core_image 不点中文义项、
related 只指库内词。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch37.json"


def W(wid, rid, pos, ph, logic, origin, native, concept, image, zh, ex, syn, ant, rel, exp, hint):
    return {
        "id": wid, "word": wid, "pos": pos, "phonetic": ph,
        "decomposable": "root", "root_ids": [rid],
        "root_logic": logic, "origin": origin,
        "native_definition": native, "core_concept": concept,
        "core_image": image, "chinese": zh, "examples": ex,
        "synonyms": syn, "antonyms": ant, "related": rel,
        "semantic_expansions": exp, "recall_hint": hint,
    }


families = [
    # ---------- auctoritas（权威/作者）----------
    {
        "root": {
            "id": "augere-auctor", "root": "auctor", "variants": ["auth", "auct"],
            "origin": "拉丁语 auctor（创造者、发起者），来自 augere（增长、使兴旺）——能令事物产生并发展的人",
            "core_concept": "the one who brings something into being, the source of authority / 使事物产生的人，权威的来源",
            "core_image": "工匠亲手打造出第一件器物，后来者都来仿照它",
            "english_definition": "originator, authority, growth",
        },
        "concept": {
            "id": "concept-augere-author", "concept": "one who originates, the growing source of authority",
            "chinese": "作者权威", "core_image": "工匠打成第一件器物，众人以它为准则",
            "root_ids": ["augere-auctor"], "word_ids": [],
        },
        "domain": "domain-make",
        "words": [
            W("author", "augere-auctor", "noun", "/ˈɔːθə(r)/",
              "auth（使产生）+ -or（人）→ 使作品产生的人 → 作者",
              "拉丁语 auctor（创造者、发起者），经古法语 autor 入英语",
              "a person who writes a book or article, or creates something",
              "the one who brings a work into being – 使一部作品得以产生的人",
              "书桌上摊开的稿纸旁，执笔人刚刚落下最后一个句号",
              ["作者", "著者", "创始人"],
              ["The author signed copies of her novel.", "He is the author of the plan."],
              ["writer", "creator"], [],
              ["authority", "authentic"],
              ["作者/著者：使作品产生的人","创始人：使某种做法或机构产生的人"],
              "auth（使产生）+ -or → 使作品产生的人"),
            W("authentic", "augere-auctor", "adjective", "/ɔːˈθentɪk/",
              "auth（源头可靠）→ 出自可信源头的、非伪造的",
              "希腊语 authentikos（原始的、可信的），经拉丁语 authenticus 入英语",
              "real, genuine, and not a copy or fake",
              "traceable to the true origin, not an imitation – 能追溯到真实源头、非仿制",
              "博物馆里那幅画经鉴定出自画家本人之手，笔触与署名都对得上",
              ["真实的", "可信的", "正宗的"],
              ["The museum displayed an authentic painting.", "The dish uses authentic spices."],
              ["genuine", "real"], ["fake", "counterfeit"],
              ["author", "authority"],
              ["真实的/正宗的：可追溯到真实源头、非伪造"],
              "auth（源头）→ 追得到可靠源头 → 真实可信"),
            W("authority", "augere-auctor", "noun", "/ɔːˈθɒrəti/",
              "auth（使产生）+ -ority → 使事物产生并定夺的那份力量",
              "拉丁语 auctoritas（权威、影响力），来自 auctor（创造者）",
              "the power to make decisions or give orders; a reliable source of information",
              "the originating power that settles things – 能定夺事物、源头可靠的那份力量",
              "裁判手中的哨子一响，场上争执即刻平息",
              ["权威", "权力", "当局"],
              ["The police have authority to enforce the law.", "She is an authority on ancient art."],
              ["power", "jurisdiction"], [],
              ["author", "authentic"],
              ["权威/权力：能定夺事物、让人信服的源头力量","当局：行使权力的一方机构"],
              "auth（使产生）+ -ority → 能定夺的源头力量 → 权威"),
        ],
    },
    # ---------- clarus（明亮清晰）----------
    {
        "root": {
            "id": "clarus", "root": "clarus", "variants": ["clar", "clear"],
            "origin": "拉丁语 clarus（明亮、清晰、响亮），与古英语 clear 同源",
            "core_concept": "bright and clear, easy to see or hear / 明亮清晰、一望即明",
            "core_image": "雨后天晴，远山的轮廓在明净空气里一线分明",
            "english_definition": "clear, bright, distinct",
        },
        "concept": {
            "id": "concept-clarus-clear", "concept": "bright and clear, plainly visible",
            "chinese": "明亮清晰", "core_image": "雨后初晴，远山轮廓在明净空气中一线分明",
            "root_ids": ["clarus"], "word_ids": [],
        },
        "domain": "domain-perceive",
        "words": [
            W("clarify", "clarus", "verb", "/ˈklærɪfaɪ/",
              "clar（清晰）+ -ify（使）→ 使思绪或说法变得清楚明白",
              "拉丁语 clarificare（使明亮），来自 clarus（清晰的）",
              "to make something easier to understand, or to make a liquid clear",
              "making murkiness bright until it is plainly seen – 把浑浊之处照亮直到看得分明",
              "浑浊的水静置后慢慢变清，杯底杂质沉下去",
              ["澄清", "阐明", "使清晰"],
              ["Could you clarify what you meant?", "The liquid clarified overnight."],
              ["explain", "elucidate"], ["confuse", "obscure"],
              ["clarity", "declare"],
              ["澄清/阐明：把含混之处说清楚"],
              "clar（清晰）+ -ify（使）→ 使变得清楚"),
            W("clarity", "clarus", "noun", "/ˈklærəti/",
              "clar（清晰）+ -ity（名词）→ 清楚明白的状态",
              "拉丁语 claritas（明亮），来自 clarus（清晰的）",
              "the quality of being clear and easy to understand or see",
              "the bright state of being plainly seen – 一眼看明的明亮状态",
              "晨光下的湖面映出岸边每棵树的倒影，根根分明",
              ["清晰", "清楚", "清澈"],
              ["The report was praised for its clarity.", "Water clarity improved after the rain."],
              ["lucidity", "clearness"], ["vagueness", "confusion"],
              ["clarify", "declare"],
              ["清晰/清澈：一目了然的明亮状态"],
              "clar（清晰）+ -ity → 清楚明白的状态"),
            W("declare", "clarus", "verb", "/dɪˈkleə(r)/",
              "de-（完全）+ clar（清晰）→ 把话说得完全清楚 → 公开宣布",
              "拉丁语 declarare（使完全清晰），来自 de＋clarus",
              "to announce something officially or publicly",
              "speaking a matter fully clear before all – 当着众人把话说到完全明白",
              "主持人走到台前，把最终结果一字一句念给全场",
              ["宣布", "声明", "申报"],
              ["The government declared a state of emergency.", "You must declare any gifts at customs."],
              ["announce", "proclaim"], ["conceal"],
              ["clarity", "clarify"],
              ["宣布/声明：公开把话说清楚","申报：向官方明确报告"],
              "de-（完全）+ clar（清晰）→ 说得全然明白 → 宣布"),
        ],
    },
    # ---------- crescere（生长）----------
    {
        "root": {
            "id": "crescere", "root": "crescere", "variants": ["creas", "crease", "cresc"],
            "origin": "拉丁语 crescere（生长、增多、壮大）",
            "core_concept": "to grow, to swell in size or number / 生长、增多、壮大",
            "core_image": "幼苗在雨后一节节拔高，从土里冒出新叶",
            "english_definition": "to grow, increase, spring up",
        },
        "concept": {
            "id": "concept-crescere-grow", "concept": "to grow larger in size or number",
            "chinese": "生长增长", "core_image": "雨后幼苗一节节拔高、抽出新叶",
            "root_ids": ["crescere"], "word_ids": [],
        },
        "domain": "domain-make",
        "words": [
            W("increase", "crescere", "verb / noun", "/ɪnˈkriːs/",
              "in-（向内）+ crease（生长）→ 向内积聚地生长 → 增多",
              "拉丁语 increscere（生长其中），来自 in＋crescere",
              "to become or make greater in size, number, or degree",
              "growing inward and upward until there is more – 生长累积直到数量变大",
              "雪球从山顶滚下，越滚越大、越滚越快",
              ["增加", "增长", "提高"],
              ["The price of oil increased sharply.", "Sales show an increase this quarter."],
              ["grow", "rise"], ["decrease", "reduce"],
              ["decrease", "increasingly"],
              ["增加/增长：数量或程度生长变大"],
              "in-（向内）+ crease（生长）→ 向内生长变多"),
            W("decrease", "crescere", "verb / noun", "/dɪˈkriːs/",
              "de-（向下）+ crease（生长）→ 生长势头向下走 → 减少",
              "拉丁语 decrescere（减少），来自 de＋crescere",
              "to become or make smaller in size, number, or degree",
              "growing in the downward direction, lessening – 朝下生长的方向收缩变小",
              "退潮时水位一寸寸落下去，露出更多滩涂",
              ["减少", "降低", "下降"],
              ["The number of visitors decreased last year.", "There was a decrease in accidents."],
              ["decline", "diminish"], ["increase", "rise"],
              ["increase", "increasingly"],
              ["减少/下降：生长的势头向下收缩"],
              "de-（向下）+ crease（生长）→ 生长朝下走 → 减少"),
            W("increasingly", "crescere", "adverb", "/ɪnˈkriːsɪŋli/",
              "increase（增多）+ -ingly（副词）→ 以日益增多的方式",
              "increase 的副词形式",
              "more and more; to an ever greater degree",
              "growing all the while, more with each step – 一直生长、一步比一步更多",
              "天色渐暗，路灯一盏接一盏亮起，街上人流愈密",
              ["越来越", "日益"],
              ["Life there is becoming increasingly expensive.", "She increasingly prefers quiet evenings."],
              ["progressively", "ever more"], [],
              ["increase", "decrease"],
              ["越来越/日益：程度随生长不断加大"],
              "increase（增多）+ -ingly → 越来越多地"),
        ],
    },
    # ---------- gerere（携带/进行）----------
    {
        "root": {
            "id": "gerere", "root": "gerere", "variants": ["gest", "ger"],
            "origin": "拉丁语 gerere（携带、承载、进行）",
            "core_concept": "to carry, to bear and convey / 携带、承载并把某物传递过去",
            "core_image": "信使把一封沉甸甸的信揣在怀里，从一处送到另一处",
            "english_definition": "to carry, bear, conduct",
        },
        "concept": {
            "id": "concept-gerere-carry", "concept": "to carry and convey, bearing meaning along",
            "chinese": "携带传递", "core_image": "信使把信揣在怀里从一处送到另一处",
            "root_ids": ["gerere"], "word_ids": [],
        },
        "domain": "domain-transfer",
        "words": [
            W("gesture", "gerere", "noun / verb", "/ˈdʒestʃə(r)/",
              "gest（携带）+ -ure → 用手臂'携带'意思的动作",
              "拉丁语 gestura（举止、姿态），来自 gerere（携带、做）",
              "a movement of the body that expresses meaning",
              "carrying meaning with one's body instead of words – 不用言语、用身体把意思带出去",
              "老人竖起大拇指，无需开口，赞许便送到了对方眼前",
              ["手势", "姿态", "表示"],
              ["She made a gesture of welcome.", "Thumbs up is a universal gesture."],
              ["signal", "sign"], [],
              ["suggest", "digest"],
              ["手势/姿态：用身体携带并传递意思的动作"],
              "gest（携带）+ -ure → 用手势把意思带出去"),
            W("suggest", "gerere", "verb", "/səˈdʒest/",
              "sug-（sub- 从下）+ gest（携带）→ 从底层悄悄带上来的意思 → 暗示",
              "拉丁语 suggerere（从下面带上、提示），来自 sub＋gerere",
              "to put forward an idea for consideration, or imply something indirectly",
              "carrying an idea up from below, softly offering it – 从下方悄悄把想法带上来给人看",
              "桌下轻轻踢了一脚，话不必说出口意思已经到了",
              ["建议", "暗示", "表明"],
              ["I suggest we leave early.", "His tone suggested doubt."],
              ["propose", "imply"], [],
              ["gesture", "digest"],
              ["建议：把想法带上台面供人考虑","暗示：不直说而把意思带出来"],
              "sug-（从下）+ gest（携带）→ 悄悄带上来的意思 → 暗示"),
            W("digest", "gerere", "verb / noun", "/daɪˈdʒest/",
              "di-（dis- 分开）+ gest（携带）→ 把食物分开携带走 → 消化",
              "拉丁语 digerere（分开、分配），来自 dis＋gerere",
              "to break down food in the body, or absorb information",
              "carrying food apart and away into the body – 把食物拆开并分别带走、吸收利用",
              "胃里像一座小磨坊，把吃下的东西慢慢磨碎化开",
              ["消化", "领会", "文摘"],
              ["The body digests food slowly.", "It takes time to digest the news."],
              ["absorb", "assimilate"], [],
              ["gesture", "suggest"],
              ["消化：把食物拆开带走为身体所用","领会：把信息慢慢吸收理解","文摘：把大量内容压缩携带的读物"],
              "di-（分开）+ gest（携带）→ 把食物分开带走 → 消化"),
        ],
    },
]

roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
# 同域累积追加（batch36 教训：dict 覆盖会丢词根）
domain_add = {}
for f in families:
    domain_add.setdefault(f["domain"], []).append(f["root"]["id"])

words = []
for fam in families:
    words.extend(fam["words"])

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words, {len(roots)} new roots")