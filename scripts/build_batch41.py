#!/usr/bin/env python3
"""Generate batch41: C-class split execution (part 1).

按 C 类拆分决策（词源核查版）建 8 个新根 + 吸收到现有根：
- 新根 conciliare（和好）: reconcile
- 新根 par-equal（相等）: comparable / pair / repair
- 新根 compilare（汇编）: compile
- 新根 audire（听）: obedience / obedient
- 新根 valere（强壮）: prevalent
- 新根 via（路）: previous
- 新根 hum-onomatopoeia（拟声）: hum
- 新根 humor-moist（湿·幽默）: humor / humorous
- 归现有根：concession→ced、concise→caedere、comply→plere、
  suit/suitable/suite→sequ、prevent→venire-invent

注意：plere/sequ/venire-invent 需扩展 variants（ply / suit suiv / vent）。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch41.json"


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
    # ---------- conciliare（和好）----------
    {
        "root": {
            "id": "conciliare", "root": "conciliare", "variants": ["concil", "concili"],
            "origin": "拉丁语 conciliare（使结合、和好）← concilium（集会、联盟）",
            "core_concept": "to bring into harmony / 使重新聚拢、和好",
            "core_image": "两个人闹僵后又坐回同一张桌前",
            "english_definition": "to reconcile, unite",
        },
        "concept": {
            "id": "concept-conciliare-harmony", "concept": "to bring parties back together in harmony",
            "chinese": "和好", "core_image": "闹僵后重新坐回一桌",
            "root_ids": ["conciliare"], "word_ids": [],
        },
        "domain": "domain-hold",
        "words": [
            W("reconcile", "conciliare", "verb", "/ˈrekənsaɪl/",
              "re-（再）+ concili（使和好）→ 使重新和好 → 和解；调和",
              "拉丁语 reconciliare：re-（再）+ conciliare（使和好）",
              "to make two things or people compatible again",
              "bringing the estranged back together – 把闹翻的重新拢到一处",
              "兄弟为遗产争了多年，最终坐下来把旧账一笔笔说清，重归于好",
              ["和解", "调和"],
              ["They reconciled after the quarrel.", "It is hard to reconcile the two accounts."],
              ["settle", "harmonize"], [],
              ["accord"],
              ["和解：使重新和好","调和：把矛盾摆平"],
              "re-（再）+ concili（和好）→ 重新和好"),
        ],
    },
    # ---------- par（相等）----------
    {
        "root": {
            "id": "par-equal", "root": "par", "variants": ["par", "pari"],
            "origin": "拉丁语 par（相等的、对等的），PIE *per-；parare（使就绪）同 PIE 但拉丁已分化",
            "core_concept": "equal, on a level / 对等、相等",
            "core_image": "天平两端摆到同一高度，谁也不压谁",
            "english_definition": "equal, matching",
        },
        "concept": {
            "id": "concept-par-equal", "concept": "equal and on a level, matched to another",
            "chinese": "对等", "core_image": "天平两端同高",
            "root_ids": ["par-equal"], "word_ids": [],
        },
        "domain": "domain-shape",
        "words": [
            W("comparable", "par-equal", "adjective", "/ˈkɑːmpərəbl/",
              "com-（共同）+ par（对等）+ -able → 能放到同一天平上比 → 可比较的",
              "拉丁语 comparabilis：com-（共同）+ par（对等）",
              "similar enough to be compared with something",
              "able to be set on the same scale – 能放上同一杆秤",
              "两款手机摆在展台并列，屏幕、价格、厚度都能放一起权衡",
              ["可比较的", "类似的"],
              ["The two products are comparable.", "His salary is comparable to mine."],
              ["similar", "equivalent"], ["incomparable"],
              ["pair", "repair"],
              ["可比较：放得上同一杆秤","类似：同一档次的"],
              "com-（共同）+ par（对等）→ 能同秤比较"),
            W("pair", "par-equal", "noun / verb", "/per/",
              "par（对等）→ 两个对等的东西 → 一对",
              "古法语 paire ← 拉丁语 paria（对等物）← par（相等）",
              "two things of the same kind used together",
              "two matched, equal things – 两个对等相配的东西",
              "抽屉里两只袜子花色相同，摆在一处正好齐整，少了一只就不成样子",
              ["一对", "配成对"],
              ["He bought a pair of shoes.", "The students paired up to practice."],
              ["couple", "duo"], [],
              ["comparable", "repair"],
              ["一对：两个相配的东西"],
              "par（对等）→ 两个对等 → 一对"),
            W("repair", "par-equal", "verb / noun", "/rɪˈper/",
              "re-（再）+ pair（对等/使就绪）→ 重新使恢复到某种状态 → 修理",
              "古法语 reparer ← 拉丁语 reparare：re-（再）+ parare（使就绪）；parare 与 par 同 PIE *per-",
              "to fix something broken or damaged",
              "making it ready again as before – 把它重新弄回原样",
              "自行车链条掉了，蹲下来一节节挂回齿轮，车又能骑了",
              ["修理", "修复"],
              ["He repaired the broken chair.", "The bridge needs repair."],
              ["mend", "fix"], ["break"],
              ["pair", "comparable"],
              ["修理：重新弄回原样"],
              "re-（再）+ pair（使就绪）→ 弄回原样"),
        ],
    },
    # ---------- compilare（汇编）----------
    {
        "root": {
            "id": "compilare", "root": "compilare", "variants": ["compil", "pila"],
            "origin": "拉丁语 compilare（堆在一起）← pila（柱、堆）",
            "core_concept": "to heap together, gather up / 堆拢成册",
            "core_image": "把散落的纸稿按序叠成一摞",
            "english_definition": "to compile, gather",
        },
        "concept": {
            "id": "concept-compilare-gather", "concept": "to gather scattered pieces into one pile",
            "chinese": "汇集", "core_image": "散稿按序叠成一摞",
            "root_ids": ["compilare"], "word_ids": [],
        },
        "domain": "domain-shape",
        "words": [
            W("compile", "compilare", "verb", "/kəmˈpaɪl/",
              "com-（一起）+ pile（堆）→ 把散件堆到一起 → 汇编",
              "拉丁语 compilare：com-（一起）+ pilare（堆垛）",
              "to collect information together to make a report or book",
              "heaping scattered pieces into one pile – 把零散的都拢成堆",
              "把历年数据一行行摘下来，排成整齐的表格编成册",
              ["汇编", "编纂"],
              ["The researchers compiled the data.", "They compiled a list of sources."],
              ["collect", "assemble"], [],
              ["association"],
              ["汇编：把散件堆拢成册"],
              "com-（一起）+ pile（堆）→ 堆到一起 → 汇编"),
        ],
    },
    # ---------- audire（听）----------
    {
        "root": {
            "id": "audire", "root": "audire", "variants": ["aud", "audi", "obed"],
            "origin": "拉丁语 audire（听）",
            "core_concept": "to hear, to listen / 听",
            "core_image": "耳朵侧过去，听清那句话",
            "english_definition": "to hear, to listen",
        },
        "concept": {
            "id": "concept-audire-hear", "concept": "to hear and heed, listening to another",
            "chinese": "听从", "core_image": "侧耳，听清那句话",
            "root_ids": ["audire"], "word_ids": [],
        },
        "domain": "domain-perceive",
        "words": [
            W("obedience", "audire", "noun", "/əˈbiːdiəns/",
              "ob-（朝向）+ edi（听）→ 朝着喊话的方向听 → 服从",
              "拉丁语 oboedientia：ob-（朝向）+ audire（听）——'听着办'",
              "willingness to follow orders or rules",
              "hearing the direction and acting on it – 听清了照着办",
              "老师一声令下，全班齐刷刷坐好，动作整齐一致",
              ["服从", "顺从"],
              ["The dog was trained to obedience.", "Obedience to the law is expected."],
              ["compliance", "submission"], ["disobedience"],
              ["obedient"],
              ["服从：听清了就照办"],
              "ob-（朝向）+ edi（听）→ 听着办 → 服从"),
            W("obedient", "audire", "adjective", "/əˈbiːdiənt/",
              "ob-（朝向）+ edi（听）+ -ent → 愿意听着办的 → 顺从的",
              "oboediens 分词：ob-（朝向）+ audire（听）",
              "willing to do what one is told",
              "one who hears and follows – 听着就办的",
              "训练有素的马儿听到缰绳的轻响就转向，不闹脾气",
              ["顺从的", "听话的"],
              ["The obedient dog stayed by his side.", "She was an obedient student."],
              ["compliant", "submissive"], ["disobedient", "rebellious"],
              ["obedience"],
              ["顺从：听着就照办"],
              "ob-（朝向）+ edi（听）+ -ent → 听着就办"),
        ],
    },
    # ---------- valere（强壮）----------
    {
        "root": {
            "id": "valere", "root": "valere", "variants": ["val", "vale"],
            "origin": "拉丁语 valere（强壮、有力、有效）",
            "core_concept": "strong, in force / 强壮、有效力",
            "core_image": "一株幼苗在石缝里挺直腰杆顶开土块",
            "english_definition": "to be strong, avail, be valid",
        },
        "concept": {
            "id": "concept-valere-strong", "concept": "being strong and in force, prevailing",
            "chinese": "强壮有力", "core_image": "幼苗顶开土块挺直",
            "root_ids": ["valere"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("prevalent", "valere", "adjective", "/ˈprevələnt/",
              "pre-（更）+ val（强）→ 比别处都强、都普及 → 流行的",
              "拉丁语 praevalere：prae-（更）+ valere（强）",
              "existing commonly or widely at a given time",
              "being the strongest presence around – 在四周占优势地存在",
              "这座城到处都立着同一家奶茶店的招牌，走两步就撞见一家",
              ["流行的", "普遍的"],
              ["The habit is prevalent in rural areas.", "Flu is prevalent in winter."],
              ["widespread", "common"], ["rare"],
              ["prevent"],
              ["流行：占优势地到处存在"],
              "pre-（更）+ val（强）→ 到处都强 → 流行"),
        ],
    },
    # ---------- via（路）----------
    {
        "root": {
            "id": "via", "root": "via", "variants": ["via", "vi"],
            "origin": "拉丁语 via（路、途径）",
            "core_concept": "a path, a way / 路、途径",
            "core_image": "一条大路笔直通向远处",
            "english_definition": "way, road, path",
        },
        "concept": {
            "id": "concept-via-way", "concept": "a way leading onward, a path",
            "chinese": "路途", "core_image": "大路笔直通向远处",
            "root_ids": ["via"], "word_ids": [],
        },
        "domain": "domain-transfer",
        "words": [
            W("previous", "via", "adjective", "/ˈpriːviəs/",
              "pre-（在前）+ vi（路）→ 在路前面、先走到的 → 先前的",
              "拉丁语 praevius：prae-（在前）+ via（路）",
              "existing or happening before this one",
              "the one that walked ahead on the road – 在路上先走到的那个",
              "翻回上一所学校的学生证，照片里是更年轻的脸",
              ["先前的", "以前的"],
              ["She had a previous job.", "I met him on a previous visit."],
              ["prior", "earlier"], ["following", "later"],
              ["prevent"],
              ["先前：在路上先走到"],
              "pre-（在前）+ vi（路）→ 先走上路的"),
        ],
    },
    # ---------- hum（拟声）----------
    {
        "root": {
            "id": "hum-onomatopoeia", "root": "hum", "variants": ["hum"],
            "origin": "英语 hum（拟声词，低声哼/嗡响），与拉丁皆无关",
            "core_concept": "a low humming sound / 低沉持续的嗡嗡声",
            "core_image": "机器低鸣，隔墙都能感到震颤",
            "english_definition": "to buzz, hum, drone",
        },
        "concept": {
            "id": "concept-hum-buzz", "concept": "a low steady buzzing sound",
            "chinese": "低鸣", "core_image": "机器低鸣震人",
            "root_ids": ["hum-onomatopoeia"], "word_ids": [],
        },
        "domain": "domain-perceive",
        "words": [
            W("hum", "hum-onomatopoeia", "verb / noun", "/hʌm/",
              "hum（拟声）→ 低沉持续的嗡嗡声",
              "英语拟声词，模仿嗡嗡声；与拉丁 hum（湿）无关",
              "to make a low continuous sound; a low continuous sound",
              "the low steady buzz that fills a quiet room – 充满屋子的低鸣",
              "夏天傍晚风扇低低震着耳朵，关掉反而觉得少了什么",
              ["嗡嗡响", "哼歌"],
              ["The machine hummed all night.", "She hummed a tune."],
              ["buzz", "drone"], [],
              ["humor", "humorous"],
              ["嗡嗡响：低沉持续的鸣声","哼歌：闭着唇哼出的调子"],
              "hum（拟声）→ 嗡嗡声"),
        ],
    },
    # ---------- humor（湿）----------
    {
        "root": {
            "id": "humor-moist", "root": "humor", "variants": ["hum", "humor"],
            "origin": "拉丁语 humor（湿气、体液）——体液学说引申出生性与幽默",
            "core_concept": "the body's moisture and temper / 体液引申出的性情与幽默",
            "core_image": "四杯体液各居其位，平衡了人就开朗",
            "english_definition": "humour, disposition",
        },
        "concept": {
            "id": "concept-humor-temper", "concept": "humours and disposition born of them",
            "chinese": "性情幽默", "core_image": "体液调和，人便开朗",
            "root_ids": ["humor-moist"], "word_ids": [],
        },
        "domain": "domain-hold",
        "words": [
            W("humor", "humor-moist", "noun", "/ˈhjuːmər/",
              "humor（体液）→ 古人认为体液决定性情 → 幽默",
              "拉丁语 humor（湿气、体液）",
              "the quality of being funny; mood",
              "the disposition born of one's humours – 由体液定下的那份性情",
              "台上那人几句话说下来，全场笑声此起彼伏，气氛一下就活了",
              ["幽默", "情绪"],
              ["His humor lightened the room.", "She was in good humor today."],
              ["wit", "comedy"], [],
              ["humorous", "hum", "temper"],
              ["幽默：让人发笑的本事","情绪：当下心气的好坏"],
              "humor（体液）→ 定性情的湿度 → 幽默"),
            W("humorous", "humor-moist", "adjective", "/ˈhjuːmərəs/",
              "humor（幽默）+ -ous → 有幽默感的 → 幽默的",
              "humor 的形容词",
              "funny and entertaining",
              "carrying a humour that makes people smile – 带趣味、逗人笑",
              "饭桌上他讲的那个段子，大家都笑了，连不苟言笑的老爸都弯了嘴角",
              ["幽默的", "滑稽的"],
              ["The book is humorous and warm.", "He made a humorous remark."],
              ["funny", "witty"], ["serious"],
              ["humor", "hum", "temper"],
              ["幽默：逗人发笑的"],
              "humor（幽默）+ -ous → 逗人笑的"),
        ],
    },
]

roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
domain_add = {}
for f in families:
    domain_add.setdefault(f["domain"], []).append(f["root"]["id"])

# 新根族自己的词也要进 words（merge 靠 words 补 concept word_ids）
family_words = []
for fam in families:
    family_words.extend(fam["words"])

# 吸收到现有根（不新建根，只收词，merge 会补 word_ids）
# concession→ced、concise→caedere、comply→plere、suit系→sequ、prevent→venire-invent
# 这些词的 entry 单独放，root_ids 用现根
absorbed = [
    W("concession", "ced", "noun", "/kənˈseʃn/",
      "con-（一起）+ cess（走）→ 一起往后让 → 让步",
      "拉丁语 concessio：con-（一起）+ cedere（退让）",
      "something given up or allowed",
      "yielding ground together – 一起往后退让的那份",
      "谈判桌上，一方把价格往下调了一档，另一方也松了口",
      ["让步", "特许"],
      ["He made a concession on price.", "The store runs a food concession."],
      ["compromise", "allowance"], [],
      ["concede", "precede", "recede"],
      ["让步：退让一份","特许：被让出的经营权"],
      "con-（一起）+ cess（走）→ 一起退让"),
    W("concise", "caedere", "adjective", "/kənˈsaɪs/",
      "con-（完全）+ cis（切）→ 把废话切掉 → 简明的",
      "拉丁语 concisus：con-（完全）+ caedere（切）——'切短的'",
      "short and clear, with no extra words",
      "cut down to essentials – 切掉多余、只剩要点",
      "会议纪要只留三行，废话全删，一眼看完",
      ["简明的", "简洁的"],
      ["The summary was concise and clear.", "Keep your answers concise."],
      ["brief", "succinct"], ["verbose", "lengthy"],
      ["precise", "concede"],
      ["简明：切掉废话只剩要点"],
      "con-（完全）+ cis（切）→ 切短的"),
    W("comply", "plere", "verb", "/kəmˈplaɪ/",
      "com-（完全）+ ply（填满）→ 满足全部要求 → 遵从",
      "拉丁语 complere：com-（完全）+ plere（填满）",
      "to obey a rule or law",
      "filling the requirement completely – 把它填到满足",
      "接到整改通知后，把每一条要求都做到位，检查组来查样样达标",
      ["遵从", "服从"],
      ["All staff must comply with the rules.", "The firm failed to comply."],
      ["obey", "conform"], ["disobey", "violate"],
      ["implement", "supplement"],
      ["遵从：把要求填满到位"],
      "com-（完全）+ ply（填满）→ 填满要求"),
    W("suit", "sequ", "noun / verb", "/suːt/",
      "suit（跟随）→ 跟着身体的形状走 → 合身、适合",
      "古法语 suite/suivre ← 拉丁语 sequi（跟随）",
      "to be right for someone; a set of clothes",
      "following a shape or situation exactly – 贴身跟随、正好合适",
      "那件西装上身，肩线正落肩头，裤长恰好及鞋面，哪哪都服帖",
      ["适合", "套装", "诉讼"],
      ["The color suits her.", "He wore a grey suit."],
      ["fit", "match"], [],
      ["suitable", "suite", "sequence"],
      ["适合：刚好跟上了","套装：成套相配的衣裳","诉讼：跟进的一项程序"],
      "suit（跟随）→ 贴身合适"),
    W("suitable", "sequ", "adjective", "/ˈsuːtəbl/",
      "suit（适合）+ -able → 合适的",
      "suit 的形容词",
      "right for a particular purpose or person",
      "able to follow the need exactly – 正好匹配那份需要",
      "下雨天换上这双防滑鞋，走哪一段路都不打滑",
      ["合适的", "适宜的"],
      ["This is a suitable place for the camp.", "Find a suitable time to call."],
      ["appropriate", "fitting"], ["unsuitable"],
      ["suit", "suite", "sequence"],
      ["合适：正好匹配需要"],
      "suit（适合）+ -able → 合适的"),
    W("suite", "sequ", "noun", "/swiːt/",
      "suite（跟随的一系列）→ 一串相随的东西",
      "法语 suite（随行）← seguir ← sequi（跟随）",
      "a set of connected rooms; a set of musical pieces",
      "a series following one after another – 一串连续相随的",
      "酒店里连着的一套客房，客厅卧室洗手间一溜排开",
      ["套房", "组曲"],
      ["They rented a hotel suite.", "The pianist played a suite."],
      ["set", "series"], [],
      ["suit", "suitable", "sequence"],
      ["套房：一连串相通的房间"],
      "suite（跟随的一系列）→ 相连成套"),
    W("prevent", "venire-invent", "verb", "/prɪˈvent/",
      "pre-（在前）+ vent（来）→ 先一步来到 → 阻止",
      "拉丁语 praevenire：prae-（在前）+ venire（来）",
      "to stop something from happening",
      "coming before it so it can't happen – 抢在它前面赶到",
      "看到前方封路，一脚刹车停住，车没冲进施工区",
      ["阻止", "预防"],
      ["The guard prevented the theft.", "Vaccine prevents the disease."],
      ["stop", "hinder"], ["allow", "permit"],
      ["invent", "invention"],
      ["阻止：抢在前面赶到","预防：事先防住"],
      "pre-（在前）+ vent（来）→ 先一步到 → 阻止"),
]

# ---- 生成前自检：Q12/Q1 前移到生成期，避免合并后才发现再回滚 ----
# review.py check 不查 Q12，只有合并后的 validate.py 查；不自检就会白跑一轮 merge。
for _w in family_words + absorbed:
    for _zh in _w.get("chinese") or []:
        assert not (len(_zh) >= 2 and _zh in _w["core_image"]), \
            f"Q12 泄题：{_w['id']} 的 core_image 点名义项「{_zh}」"
    if len(_w.get("chinese") or []) >= 2:
        assert _w.get("semantic_expansions"), f"Q1：{_w['id']} 多义却无 semantic_expansions"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": family_words + absorbed,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(roots)} new roots, "
      f"{len(family_words)} family words + {len(absorbed)} absorbed words")