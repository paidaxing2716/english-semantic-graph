#!/usr/bin/env python3
"""Generate batch36: one existing-root addition (fac) + four new families.

- fac（做）补词：fact / factor / factory —— 拉丁语 factum（已做成的事）
- habit（居住）新根：habit / inhabit / inhabitant
- point（尖端/点）新根：point / appoint / appointment
- limes（边界）新根：limit / limitation / limited
- gubernare（掌舵）新根：govern / government / governor

共 15 词：3 补词 + 12 新族词。所有词条全字段含 phonetic / recall_hint /
semantic_expansions，可直接合并入库。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch36.json"


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
    # ---------- habit（居住）----------
    {
        "root": {
            "id": "habitare", "root": "habitare", "variants": ["habit", "hibit"],
            "origin": "拉丁语 habitare（居住、常驻），是 habere（持有）的反复体：反复持有某地 → 住下",
            "core_concept": "to dwell, to hold a place as one's own / 长期驻留某处、把某处据为己居",
            "core_image": "鸟在同一个巢里年复一年回来住下",
            "english_definition": "to dwell, inhabit, keep",
        },
        "concept": {
            "id": "concept-habitare-dwell", "concept": "to dwell in a place, to keep returning to it",
            "chinese": "居住栖居", "core_image": "同一只鸟年复一年回到同一个巢里住下",
            "root_ids": ["habitare"], "word_ids": [],
        },
        "domain": "domain-hold",
        "words": [
            W("habit", "habitare", "noun", "/ˈhæbɪt/",
              "habit（居住/反复持有）→ 反复做的动作像反复住同一个地方一样固定下来",
              "拉丁语 habitus（状态、习惯），来自 habere（持有）的反复体 habitare（居住）",
              "a settled regular practice, especially one hard to give up",
              "a practice one returns to as steadily as returning home – 像反复回到老住处一样稳定反复的做法",
              "同一条路每天清晨都走一遍，脚自己就知道往哪拐",
              ["习惯", "习性"],
              ["He has a habit of reading before bed.", "Smoking is a hard habit to break."],
              ["custom", "routine"], ["impulse"],
              ["inhabit"],
              ["习惯/习性：反复做、像常驻一样稳定的行为方式"],
              "habit（居住）→ 反复回到同一处住下 → 反复做的动作固定成习惯"),
            W("inhabit", "habitare", "verb", "/ɪnˈhæbɪt/",
              "in-（在内）+ habit（居住）→ 在某个地方里边住着",
              "拉丁语 inhabitare（居住于），来自 in＋habitare",
              "to live or dwell in a place",
              "dwelling inside a place as its resident – 作为居者住在某地之内",
              "一家人搬进山谷里的小屋，从此长期住下",
              ["居住于", "栖息于"],
              ["These birds inhabit the coastal cliffs.", "Thousands of species inhabit the reef."],
              ["dwell", "occupy"], ["vacate"],
              ["habit"],
              ["居住于/栖息于：作为居民长期住在某处"],
              "in-（在内）+ habit（居住）→ 住在某处里面"),
            W("inhabitant", "habitare", "noun", "/ɪnˈhæbɪtənt/",
              "in-（在内）+ habit（居住）+ -ant（人）→ 住在里面的人",
              "拉丁语 inhabitans（居住的），来自 inhabitare（居住于）",
              "a person or animal that lives in a particular place",
              "one who dwells inside a place – 住在某地之内的人或生物",
              "山谷小屋的窗户里透出灯光，屋主一家常年住在那里",
              ["居民", "住户", "栖居者"],
              ["The island's inhabitants rely on fishing.", "Ancient inhabitants left stone circles here."],
              ["resident", "dweller"], ["visitor"],
              ["habit", "inhabit"],
              ["居民/住户：长期居住在某地的成员"],
              "in-（在内）+ habit（居住）+ -ant（人）→ 住在此地的人"),
        ],
    },
    # ---------- point（尖端/点）----------
    {
        "root": {
            "id": "punktum", "root": "punktum", "variants": ["point", "punct"],
            "origin": "拉丁语 punctum（刺出的点、小孔），来自 pungere（刺）的过去分词 punctus",
            "core_concept": "a sharp point, a single marked spot / 一个尖锐的顶端或一个单独标记的点",
            "core_image": "针尖在纸上刺出一个小孔——又尖又小、位置精确",
            "english_definition": "point, prick, spot",
        },
        "concept": {
            "id": "concept-punktum-point", "concept": "a sharp point or a single precise spot",
            "chinese": "尖端点", "core_image": "针尖刺纸留下一个精准的小孔",
            "root_ids": ["punktum"], "word_ids": [],
        },
        "domain": "domain-shape",
        "words": [
            W("point", "punktum", "noun / verb", "/pɔɪnt/",
              "point（刺出的点）→ 尖端、要点；动词指把注意力指向某一点",
              "古法语 point（点），来自拉丁语 punctum（刺出的点）",
              "a sharp end, a particular spot, or the main idea; to direct attention to something",
              "the exact spot marked by a prick, sharp and precise – 被刺出的那个精准位置，尖而确定",
              "箭头的尖稳稳扎在靶心那一个点上",
              ["点", "要点", "尖端", "指向"],
              ["The pencil has a sharp point.", "Good point—let me reconsider.", "She pointed at the map."],
              ["spot", "gist"], [],
              ["appoint"],
              ["点/尖端：刺出的尖锐位置","要点：众多话里被'点'出的核心一处","指向：把注意力引到某个点上"],
              "point（刺出的点）→ 靶尖那样精确的一处；话里的'点'即被指出要点"),
            W("appoint", "punktum", "verb", "/əˈpɔɪnt/",
              "ap-（ad- 靠向）+ point（点）→ 把某人'点'定到某个职位上",
              "古法语 apointier（安排到位），来自拉丁语 ad＋punctum（点到）",
              "to choose someone for a position, or fix a time for something",
              "marking someone out to a post, or fixing a moment – 把某人点定为职位人选，或把时间定于某刻",
              "校长在名单上点出一个名字，指定他担任组长",
              ["任命", "指派", "约定"],
              ["They appointed her to lead the team.", "The meeting was appointed for Monday."],
              ["assign", "designate"], ["dismiss"],
              ["point", "appointment"],
              ["任命/指派：把人点定到某个职位","约定：把时间点定为某刻"],
              "ap-（靠向）+ point（点）→ 把人点到某个职位上"),
            W("appointment", "punktum", "noun", "/əˈpɔɪntmənt/",
              "appoint（任命/约定）+ -ment（名词）→ 任命这件事，或约好的相会时刻",
              "古法语 apointement（安排），来自 apointier（安排到位）",
              "an arrangement to meet at a set time, or the act of choosing someone for a post",
              "a fixed meeting moment, or the assigned post itself – 定好的相会时刻，或已被点定的职位",
              "日历上画着圈的那格时间，就是和牙医约好的就诊时刻",
              ["预约", "约会", "任命"],
              ["I have a dentist appointment at three.", "Her appointment as director was announced."],
              ["booking", "date"], ["cancellation"],
              ["appoint", "point"],
              ["预约/约定：定好的会面时刻","任命：被点定担任的职位"],
              "appoint（点定）+ -ment → 点定的时刻或职位"),
        ],
    },
    # ---------- limes（边界）----------
    {
        "root": {
            "id": "limes", "root": "limes", "variants": ["limit"],
            "origin": "拉丁语 limes（边界、田界），limitis 的属格 → 英语 limit",
            "core_concept": "a boundary line, the edge beyond which something may not go / 一条边界线，越线即被禁止",
            "core_image": "田地尽头的一道界桩，牛走到那儿就停下不再往前",
            "english_definition": "boundary, border, limit",
        },
        "concept": {
            "id": "concept-limes-boundary", "concept": "the boundary edge beyond which one may not pass",
            "chinese": "边界界限", "core_image": "田边的界桩挡住牛不再往前走",
            "root_ids": ["limes"], "word_ids": [],
        },
        "domain": "domain-hold",
        "words": [
            W("limit", "limes", "noun / verb", "/ˈlɪmɪt/",
              "limit（边界）→ 不许越过的边界；动词是给某物划下边界",
              "拉丁语 limes（边界），经古法语 limite 入英语",
              "a point or line beyond which something does not or may not extend; to set such a line",
              "the boundary line one may not cross – 不允许越过的那条边界线",
              "跑道上画着终点线，冲过那根线比赛就结束",
              ["限度", "限制", "界限"],
              ["There is a limit to what we can do.", "Please limit your speech to five minutes."],
              ["bound", "cap"], ["unlimited"],
              ["limited", "limitation"],
              ["限度/界限：不许越过的那条边界","限制：为事物划下边界"],
              "limit（边界）→ 不许越过的线；划线即限制"),
            W("limitation", "limes", "noun", "/ˌlɪmɪˈteɪʃn/",
              "limit（边界）+ -ation（名词）→ 边界的存在本身，即受限制的状态",
              "拉丁语 limitatio（划定边界），来自 limitare（划界）",
              "a restriction, or a weakness that restricts what someone can do",
              "the state of having a boundary drawn around one – 被划在边界内、无法越出的状态",
              "笼子再大也有边框，飞禽的活动范围到此为止",
              ["限制", "局限", "缺陷"],
              ["The main limitation is the budget.", "He knows his own limitations."],
              ["restriction", "drawback"], ["advantage"],
              ["limit", "limited"],
              ["限制/局限：被边界框住的状态","缺陷：能力被边界框住的部分"],
              "limit（边界）+ -ation → 被边界框住的状态"),
            W("limited", "limes", "adjective", "/ˈlɪmɪtɪd/",
              "limit（边界）+ -ed（已…的）→ 已被划下边界、范围不大的",
              "limit 的过去分词形式",
              "restricted in size, amount, or extent; not very large",
              "having a boundary drawn around it, small in reach – 被边界圈住、伸展余地不大",
              "一小块圈起来的实验田，只种得下几种作物",
              ["有限的", "受限的"],
              ["The offer is available for a limited time.", "His knowledge of the subject is limited."],
              ["restricted", "finite"], ["unlimited", "boundless"],
              ["limit", "limitation"],
              ["有限的：被边界圈住、范围不大"],
              "limit（边界）+ -ed → 被边界圈定的、范围有限"),
        ],
    },
    # ---------- gubernare（掌舵）----------
    {
        "root": {
            "id": "gubernare", "root": "gubernare", "variants": ["govern"],
            "origin": "希腊语 kybernan（掌舵）经拉丁语 gubernare（驾驶、指挥）传入，控制论的 cybernetics 同源",
            "core_concept": "to steer a ship, to direct and control / 掌舵引航、把握方向实施掌控",
            "core_image": "舵手站在船尾把住舵轮，船按他定的方向前行",
            "english_definition": "to steer, direct, rule",
        },
        "concept": {
            "id": "concept-gubernare-steer", "concept": "to steer and direct, holding the course",
            "chinese": "掌舵治理", "core_image": "舵手把住舵轮，让船按定好的方向走",
            "root_ids": ["gubernare"], "word_ids": [],
        },
        "domain": "domain-hold",
        "words": [
            W("govern", "gubernare", "verb", "/ˈɡʌvən/",
              "govern（掌舵）→ 像舵手把握方向一样管理众人事务",
              "古法语 governer，来自拉丁语 gubernare（驾驶、指挥）",
              "to control and direct a country, group, or activity",
              "steering a vessel of people along a chosen course – 像把舵一样引导众人沿既定方向行进",
              "船长端坐驾驶台，轮船按他给出的航线破浪前行",
              ["统治", "治理", "支配"],
              ["The council governs the town.", "Prices are governed by supply and demand."],
              ["rule", "administer"], ["obey"],
              ["government", "governor"],
              ["统治/治理：像掌舵一样把握方向管理事务","支配：规律像舵一样主导结果"],
              "govern（掌舵）→ 把握方向 → 治理一方事务"),
            W("government", "gubernare", "noun", "/ˈɡʌvənmənt/",
              "govern（治理）+ -ment（名词）→ 治理一国的机构整体",
              "古法语 governement（管理），来自 governer（治理）",
              "the group of people who rule a country or state",
              "the steering apparatus of a whole nation – 为整个国家把舵的那套机构",
              "议会大楼里的人们开会定策，相当于给国家掌舵的那套装置",
              ["政府", "政体", "治理"],
              ["The government announced new policies.", "She works for the local government."],
              ["administration", "regime"], [],
              ["govern", "governor"],
              ["政府/政体：治理一国的机构整体"],
              "govern（治理）+ -ment → 治理国家的机构"),
            W("governor", "gubernare", "noun", "/ˈɡʌvənə(r)/",
              "govern（治理）+ -or（人）→ 掌舵的人 → 一方之长",
              "古法语 gouvreneur，来自拉丁语 gubernator（舵手、指挥者）",
              "the head of a state, region, or institution",
              "the person at the helm of a region or body – 为某地区或机构把舵的人",
              "楼顶旗帜猎猎，坐在主位的那人统筹着全州大小事务",
              ["州长", "总督", "主管"],
              ["The governor signed the new law.", "He was elected governor last year."],
              ["administrator", "chief"], [],
              ["govern", "government"],
              ["州长/总督：为一方把舵的首脑"],
              "govern（治理）+ -or（人）→ 为一方掌舵的人"),
        ],
    },
]

# fac（做）补词：fact / factor / factory
fac_additions = [
    W("fact", "fac", "noun", "/fækt/",
      "fact（做→已做成）→ 已经做成、不会改变的事 → 事实",
      "拉丁语 factum（已做成的事），facere（做）的过去分词中性形式",
      "something known to be true, especially something that can be proved",
      "a thing already done and fixed, standing firm – 已经做成、定型不变之物",
      "石碑上刻下的那行字，任谁来看都是不动的实情",
      ["事实", "真相"],
      ["The fact is that we were late.", "Facts speak louder than words."],
      ["reality", "truth"], ["fiction"],
      ["factor", "factory", "actual"],
      ["事实：已成定局、不再改变的事","（法律）既成事实 → 真相"],
      "fac（做）+ 过去分词 → 已经做成的、定型之事 → 事实"),
    W("factor", "fac", "noun / verb", "/ˈfæktə(r)/",
      "fact（已做成的）+ -or（做…者）→ 参与做成某事的一个成分",
      "拉丁语 factor（制造者），来自 facere（做）",
      "one of the things that helps produce a result; a number that divides another exactly",
      "one of the doers that together make a result – 合力造成某一结果的各个成分之一",
      "烹调的几味调料缺一不可，缺一味味道就变",
      ["因素", "要素", "因子"],
      ["Cost is a major factor in the decision.", "Two and three are factors of six."],
      ["element", "component"], [],
      ["fact", "factory"],
      ["因素/要素：共同造成结果的一个成分","因子：把某数'做成'其整数倍的成分"],
      "fact（做）+ -or（者）→ 参与做成结果的成分"),
    W("factory", "fac", "noun", "/ˈfæktəri/",
      "fact（做）+ -ory（场所）→ 专门做东西的场所",
      "拉丁语 factoria（工场），来自 factor（制造者）",
      "a building where goods are made in large quantities",
      "a place where making happens at scale – 大批量'做'东西的场所",
      "厂房里流水线不停转动，商品一件件被做出来",
      ["工厂", "制造厂"],
      ["The factory employs five hundred workers.", "Cars roll off the factory line daily."],
      ["plant", "mill"], [],
      ["fact", "factor"],
      ["工厂：专门大批量制造物品的场所"],
      "fact（做）+ -ory（场所）→ 做东西的地方"),
]

words = []
for fam in families:
    words.extend(fam["words"])
words.extend(fac_additions)

# 输出 batch：新根 + 概念 + 域归属 + 全部词条
roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
# 注意：多个族可能归入同一个语义域，必须累积追加而非 dict 覆盖
domain_add = {}
for f in families:
    domain_add.setdefault(f["domain"], []).append(f["root"]["id"])

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words, {len(roots)} new roots")