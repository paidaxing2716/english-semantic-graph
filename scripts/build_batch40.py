#!/usr/bin/env python3
"""Generate batch40: five new families.

- fortis（强壮）: comfort / comfortable / effort
- fortuna（运气）: fortunate / fortune / misfortune
- gravis（重）: aggravate / grave / gravity
- tempus（时间·调和）: contemporary / temper / temporary
- temptare（试探）: attempt / contempt / tempt

共 15 词。host 族（hospes/hostis 双源）留待下批单独斟酌。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch40.json"


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
    # ---------- fortis（强壮）----------
    {
        "root": {
            "id": "fortis", "root": "fortis", "variants": ["fort", "forc"],
            "origin": "拉丁语 fortis（强壮的、有力的）",
            "core_concept": "strong, holding firm / 强壮、撑得住",
            "core_image": "一堵厚墙稳稳立着，外面怎么推都推不动",
            "english_definition": "strong, firm, brave",
        },
        "concept": {
            "id": "concept-fortis-strong", "concept": "strong and firm, able to hold up",
            "chinese": "强壮稳固", "core_image": "厚墙立着，怎么推都不动",
            "root_ids": ["fortis"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("comfort", "fortis", "noun / verb", "/ˈkʌmfərt/",
              "com-（加强）+ fort（强）→ 让人重新强起来的那种安稳 → 安慰",
              "拉丁语 confortare（使强壮）：com-（加强）+ fortis（强壮）",
              "a state of ease and calm; to soothe someone",
              "the easing that restores strength – 让人重新有力气的安顿",
              "累了一天后陷进软沙发里，那一下全身放松的感觉",
              ["安慰", "舒适"],
              ["The chair offers great comfort.", "She comforted the crying child."],
              ["consolation", "ease"], ["discomfort"],
              ["comfortable", "effort", "comfortable"],
              ["安慰：让人重新有力量","舒适：身体放松的状态"],
              "com-（加强）+ fort（强）→ 让人重新强壮 → 安慰"),
            W("comfortable", "fortis", "adjective", "/ˈkʌmftəbl/",
              "comfort（舒适）+ -able → 能让人安顿下来的 → 舒适的",
              "comfort 的形容词",
              "giving ease and relaxation; at ease",
              "able to rest and recover strength – 能让人放松休整的",
              "那双旧鞋已经穿出脚形，走一天也不磨脚",
              ["舒适的", "自在的"],
              ["The bed was comfortable.", "She felt comfortable in the group."],
              ["cozy", "relaxing"], ["uncomfortable"],
              ["comfort", "effort", "comfortable"],
              ["舒适：能让人放松的","自在：不别扭、放得开"],
              "comfort（舒适）+ -able → 能安顿的"),
            W("effort", "fortis", "noun", "/ˈefərt/",
              "ef-（ex- 出）+ fort（强）→ 把力量使出来 → 努力",
              "拉丁语 exfortis：ex-（出）+ fortis（强壮）——'使出气力'",
              "physical or mental energy used to do something",
              "strength pushed out toward the task – 朝事情使出去的那股劲",
              "双手抓住箱子两端往上抬，脸都涨红了的那一下",
              ["努力", "气力"],
              ["It took great effort to finish.", "She made every effort to help."],
              ["endeavor", "exertion"], [],
              ["comfort", "comfortable", "comfortable"],
              ["努力：使出去的气力"],
              "ef-（出）+ fort（强）→ 使出力 → 努力"),
        ],
    },
    # ---------- fortuna（运气）----------
    {
        "root": {
            "id": "fortuna", "root": "fortuna", "variants": ["fortun"],
            "origin": "拉丁语 fortuna（命运、运气）——本义'所遭遇的'，与 fortis 相关但不直接",
            "core_concept": "what chance brings one's way / 命运降落到人头上的那份好坏",
            "core_image": "转盘停下，指针落定的那一刻，决定了好坏",
            "english_definition": "fortune, chance, luck",
        },
        "concept": {
            "id": "concept-fortuna-luck", "concept": "what chance brings, one's lot in life",
            "chinese": "命运运气", "core_image": "转盘停下，指针落定",
            "root_ids": ["fortuna"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("fortune", "fortuna", "noun", "/ˈfɔːrtʃən/",
              "fortun（命运）+ -e → 命运降下的那份好坏 → 运气；财富",
              "拉丁语 fortuna（命运）",
              "chance as a force in life; a large amount of money",
              "what fate hands down – 命运递到手上的那份",
              "抽奖箱里摸出一张券，展开一看中了大奖，那一下就是它",
              ["运气", "财富"],
              ["Fortune smiled on them.", "He made a fortune in trade."],
              ["luck", "wealth"], ["misfortune"],
              ["fortunate", "misfortune", "misfortune"],
              ["运气：命运降下的好坏","财富：命运眷顾带来的钱财"],
              "fortun（命运）→ 命运递来的 → 运气"),
            W("fortunate", "fortuna", "adjective", "/ˈfɔːrtʃənət/",
              "fortune（运气）+ -ate → 有好运气的 → 幸运的",
              "fortuna 的形容词",
              "having good luck or a favorable outcome",
              "receiving good from fate – 命运给了好的一份",
              "雨刚停你正好到站，一滴没淋着，运气就是这感觉",
              ["幸运的"],
              ["We were fortunate to escape.", "She is fortunate to have support."],
              ["lucky", "favored"], ["misfortune"],
              ["fortune", "misfortune", "misfortune"],
              ["幸运：命运给了好的一份"],
              "fortune（运气）+ -ate → 有好运的"),
            W("misfortune", "fortuna", "noun", "/ˌmɪsˈfɔːrtʃən/",
              "mis-（坏）+ fortune（运气）→ 坏运气 → 不幸",
              "mis-（否定/坏）+ fortuna（命运）",
              "bad luck; an unfortunate event",
              "fate handing down a bad lot – 命运递来的坏一份",
              "台风过境，家里被水淹了半层，那一片狼藉就是它",
              ["不幸", "厄运"],
              ["The flood was a great misfortune.", "He bore his misfortune bravely."],
              ["mishap", "adversity"], ["fortune"],
              ["fortune", "fortunate"],
              ["不幸：命运递来的坏一份"],
              "mis-（坏）+ fortune（运气）→ 坏运气"),
        ],
    },
    # ---------- gravis（重）----------
    {
        "root": {
            "id": "gravis", "root": "gravis", "variants": ["grav", "griev"],
            "origin": "拉丁语 gravis（重的、沉甸甸的）",
            "core_concept": "heavy, weighty / 重、沉甸甸压着",
            "core_image": "一块铅锭沉在手里，分量压得手往下坠",
            "english_definition": "heavy, weighty, serious",
        },
        "concept": {
            "id": "concept-gravis-heavy", "concept": "heavy, weighing down and serious",
            "chinese": "沉重", "core_image": "铅锭压在手里，分量往下坠",
            "root_ids": ["gravis"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("grave", "gravis", "noun / adjective", "/ɡreɪv/",
              "grav（重）+ -e → 沉重的 → 严重的；坟，埋重的那处",
              "拉丁语 gravis（重）；名词'坟'义来自日耳曼语 gräf（挖），撞音",
              "serious and worrying; a place of burial",
              "heavy with weight or worry – 压得人心沉的",
              "医生的表情一下沉下来，那句诊断还没说出口，气氛已经压住了",
              ["严重的", "沉重的", "坟墓"],
              ["This is a grave mistake.", "The situation is grave."],
              ["serious", "solemn"], ["trivial"],
              ["gravity", "aggravate"],
              ["严重：压得人心沉","坟墓：安放逝者的重地"],
              "grav（重）→ 沉甸甸压着 → 严重"),
            W("gravity", "gravis", "noun", "/ˈɡrævəti/",
              "grav（重）+ -ity → 重的性质 → 重力；严肃",
              "拉丁语 gravitas：gravis（重）",
              "the force that pulls things down; seriousness",
              "the heaviness that pulls things down – 把东西往下拽的那股重",
              "抛向空中的球升到最高点，顿一下，被那股力量拽回地面",
              ["重力", "严肃"],
              ["Gravity pulls objects toward Earth.", "The matter deserves grave consideration."],
              ["gravitation"], [],
              ["grave", "aggravate", "grave"],
              ["重力：往下拽的重","严肃：压着不轻浮的分量"],
              "grav（重）+ -ity → 往下的重 → 重力"),
            W("aggravate", "gravis", "verb", "/ˈæɡrəveɪt/",
              "ag-（ad- 加强）+ grav（重）+ -ate → 使更重 → 加重",
              "拉丁语 aggravare：ad-（加强）+ gravis（重）",
              "to make something worse or more serious",
              "adding more weight to an already heavy load – 往本已沉的上面再压",
              "伤口没好就去搬重物，原来一点小伤被折腾得更厉害了",
              ["加重", "恶化"],
              ["Stress aggravates the condition.", "The delay aggravated the problem."],
              ["worsen", "exacerbate"], ["alleviate"],
              ["grave", "gravity", "grave"],
              ["加重：往重处再压"],
              "ag-（加强）+ grav（重）+ -ate → 更重 → 加重"),
        ],
    },
    # ---------- tempus（时间·调和）----------
    {
        "root": {
            "id": "tempus", "root": "tempus", "variants": ["tempor", "temper"],
            "origin": "拉丁语 tempus（时间）→ tempor-；temperare（调和，'按时得当'引申）",
            "core_concept": "time; the right measure at the right time / 时间，及按时得当的分寸",
            "core_image": "沙漏里的沙缓缓流下，刻度处正好",
            "english_definition": "time, season, due measure",
        },
        "concept": {
            "id": "concept-tempus-time", "concept": "time, and the right measure timed aright",
            "chinese": "时间分寸", "core_image": "沙漏流沙，刻度恰好",
            "root_ids": ["tempus"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("contemporary", "tempus", "adjective", "/kənˈtempəreri/",
              "con-（共同）+ tempor（时间）+ -ary → 同处一个时代的 → 当代的",
              "拉丁语 contemporaneus：com-（共同）+ tempus（时间）",
              "belonging to the present time; of the same period",
              "sharing the same time as now – 与当下同处一个时刻",
              "同一代人的合影里，大家穿的衣服、留的发型都在同一个时代",
              ["当代的", "同时代的"],
              ["Contemporary art challenges tradition.", "They are contemporary writers."],
              ["modern", "current"], ["ancient"],
              ["temporary", "temper", "contemporary"],
              ["当代：与当下同时","同时代：与他人同处一时"],
              "con-（共同）+ tempor（时间）→ 同处一时"),
            W("temporary", "tempus", "adjective", "/ˈtempəreri/",
              "tempor（时间）+ -ary → 只属于一段时间的 → 临时的",
              "拉丁语 temporarius：tempus（时间）",
              "lasting only for a limited time",
              "bound to a stretch of time, not forever – 只占一段时间、不永久",
              "工地旁的蓝色铁皮房，住一段就拆，不是长久之计",
              ["临时的", "暂时的"],
              ["She took a temporary job.", "The road is closed temporarily."],
              ["provisional", "transient"], ["permanent"],
              ["contemporary", "temper", "contemporary"],
              ["临时：只占一段时间"],
              "tempor（时间）+ -ary → 只属一段时间的"),
            W("temper", "tempus", "noun / verb", "/ˈtempər/",
              "temper（调和）→ 按时得当的调配 → 脾气；使缓和",
              "拉丁语 temperare（调和、使适中）——tempus 的'按时得当'引申",
              "a person's mood or nature; to make something less extreme",
              "mixing to the right measure at the right time – 按分寸调配",
              "调酒师把几种酒按比例兑在一起，最后那一下点味",
              ["脾气", "使缓和", "调和"],
              ["She has a calm temper.", "He tempered the criticism with praise."],
              ["mood", "disposition"], [],
              ["temporary", "contemporary"],
              ["脾气：那点分寸失当的样子","使缓和：调回到适中"],
              "temper（调和）→ 按分寸调配 → 脾气"),
        ],
    },
    # ---------- temptare（试探）----------
    {
        "root": {
            "id": "temptare", "root": "temptare", "variants": ["tempt", "tent"],
            "origin": "拉丁语 temptare（试探、考验）——注意与 time 无关",
            "core_concept": "to test, to probe and try / 试探、考验",
            "core_image": "伸出一根手指轻轻碰一下水面，探它冷不冷",
            "english_definition": "to try, to test, to probe",
        },
        "concept": {
            "id": "concept-temptare-test", "concept": "to try and test, probing what comes",
            "chinese": "试探考验", "core_image": "指尖碰水面，探冷暖",
            "root_ids": ["temptare"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("tempt", "temptare", "verb", "/tempt/",
              "tempt（试探）→ 试探一个人的定力 → 引诱",
              "拉丁语 temptare（试探、尝试）",
              "to attract or lure someone to do something, often wrong",
              "probing one's resolve – 试探一个人的定力",
              "橱窗里的甜点摆得诱人，路过时脚就不由自主往那边挪",
              ["引诱", "诱惑"],
              ["The offer tempted him.", "Don't tempt me with chocolate."],
              ["lure", "entice"], [],
              ["attempt", "contempt", "tempt"],
              ["引诱：试探定力","诱惑：把意志动摇"],
              "tempt（试探）→ 试探定力 → 引诱"),
            W("attempt", "temptare", "noun / verb", "/əˈtempt/",
              "at-（ad- 朝向）+ tempt（试探）→ 朝目标试一下 → 尝试",
              "拉丁语 attemptare：ad-（朝向）+ temptare（试探）",
              "to try to do something; an effort to do something",
              "reaching out to test the way – 伸手朝目标探路",
              "第一次滑冰，扶着栏杆小心翼翼地迈出第一步，试了试站不站得稳",
              ["尝试", "企图"],
              ["She attempted the climb.", "His attempt failed."],
              ["try", "endeavor"], [],
              ["tempt", "contempt"],
              ["尝试：朝目标试一下"],
              "at-（朝向）+ tempt（试探）→ 朝目标试 → 尝试"),
            W("contempt", "temptare", "noun", "/kənˈtempt/",
              "con-（完全）+ tempt（试探）→ 看穿之后轻慢地对待 → 蔑视",
              "拉丁语 contemptus：com-（完全）+ temptare（试探）——'看透了'",
              "a strong feeling of disliking and despising",
              "dismissing after probing and finding nothing worthy – 试探后觉得不屑一顾",
              "对那种当面一套背后一套的做法，他只斜眼看了下就不再正眼",
              ["蔑视", "轻视"],
              ["She looked at him with contempt.", "He has contempt for cheats."],
              ["scorn", "disdain"], ["respect"],
              ["tempt", "attempt", "tempt"],
              ["蔑视：试探后觉得不屑"],
              "con-（完全）+ tempt（试探）→ 看透而不屑 → 蔑视"),
        ],
    },
]

roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
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
