#!/usr/bin/env python3
"""Generate batch43: 6 new Latin root families (18 词) + 4 additions (4 词).

新族（词源清楚、画面好写的大族）:
  serere（编连）      assert / desert / insert
  habere（持有）      exhibit / inhibit / prohibit
  manus（手）         manage / manner / manual
  structus（垒砌）    construction / destruction / instruction
  spatium（间距）     space / spaceship / spacious
  stringere（拉紧）   constrain / restrain / strain

补词（4 词，挂已建模词根；forma/portus 由上一步迁移刚解锁）:
  forma  ← form / former / performance
  portus ← port

注：desert（抛弃/沙漠）来自 deserere（解开编连而弃置），与 dessert（甜品，
法语 desservir 清桌）无关——HANDOFF 风险族 1.1 特别点名，勿混。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch43.json"


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


families = []

# ---------- serere（编连）----------
families.append({
    "root": {
        "id": "serere", "root": "serere", "variants": ["sert", "ser"],
        "origin": "拉丁语 serere（把东西一个接一个编连起来，如串珠、编篱），"
                  "过去分词 sertus；series（系列）同根",
        "core_concept": "to join things one after another in a line / 一个接一个串连成列",
        "core_image": "一根线把珠子一颗接一颗串起来，中间断一颗整串就散",
        "english_definition": "to join, link in a row",
    },
    "concept": {
        "id": "concept-serere-link", "concept": "to join things one after another in a line",
        "chinese": "串连成列", "core_image": "线上珠子一颗接一颗，抽掉一颗整串就散",
        "root_ids": ["serere"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("assert", "serere", "verb", "/əˈsɜːt/",
          "as-（ad- 靠向）+ sert（串连）→ 把话一句扣一句地接稳 → 断言",
          "拉丁语 asserere（宣称、主张），来自 ad＋serere（连上）",
          "to state something firmly as true; to make others recognize a right",
          "linking one's words tight to a claim and standing on it – 把话紧扣在主张上，站定不退",
          "他把三条依据一条接一条摆上桌，语气不留退路",
          ["断言", "声称", "维护"],
          ["She asserted that the data was sound.", "He asserted his right to speak."],
          ["declare", "maintain"], ["deny"],
          ["insert", "desert"],
          ["断言/声称：把话紧扣在主张上说定", "维护：把自己的权利扣住不放"],
          "as-（靠向）+ sert（串连）→ 把话扣紧在主张上"),
        W("desert", "serere", "verb", "/dɪˈzɜːt/",
          "de-（脱开）+ sert（串连）→ 把串连解开、撇下不管 → 抛弃",
          "拉丁语 deserere（解开连结、弃置），来自 de＋serere；"
          "与甜品 dessert（法语 desservir 清桌）无关，勿混",
          "to abandon someone or something, especially a duty or post",
          "unhooking oneself from the row and walking off – 把自己从串上解开走掉",
          "队伍还在原地，他半夜把装备一扔就走了",
          ["抛弃", "遗弃", "擅离"],
          ["He deserted his post before dawn.", "She felt deserted by her closest friends."],
          ["abandon", "forsake"], ["support"],
          ["assert", "insert"],
          ["抛弃/遗弃：把自己从串连中解开、撇下不管", "擅离：擅自脱开本该守住的那一环"],
          "de-（脱开）+ sert（串连）→ 从串上解开走掉"),
        W("insert", "serere", "verb", "/ɪnˈsɜːt/",
          "in-（进入）+ sert（串连）→ 把一物插进串里、接进队列",
          "拉丁语 inserere（插入、嵌进），来自 in＋serere",
          "to put something into something else, or between other things",
          "opening the row to let one more link take its place – 把串挑开，让一枚补进那一环",
          "把新的一颗珠子挑进线上，两边一收又是整串",
          ["插入", "嵌入", "刊登"],
          ["Insert the card into the slot.", "They inserted a clause into the contract."],
          ["introduce", "embed"], ["remove", "extract"],
          ["assert", "desert"],
          ["插入/嵌入：把一物接进串里的那一环", "刊登：把文字插进版面里"],
          "in-（进入）+ sert（串连）→ 插进串里补上一环"),
    ],
})

# ---------- habere（持有）----------
families.append({
    "root": {
        "id": "habere", "root": "habere", "variants": ["hibit", "hab"],
        "origin": "拉丁语 habere（持有、拿住、保持某状态）；复合词里元音弱化成 -hibēre，"
                  "故拼作 -hibit（habit/inhabit 亦同源，已另立 habitare 族）",
        "core_concept": "to hold a thing and decide whether it is let out / 手里拿住，并决定放不放出去",
        "core_image": "一只手把东西攥着：张开给人看，或收拢不许动",
        "english_definition": "to hold, keep, have",
    },
    "concept": {
        "id": "concept-habere-hold", "concept": "to hold a thing and decide whether to let it out",
        "chinese": "攥住取舍", "core_image": "手攥着一物，张开是给人看，收拢是不许动",
        "root_ids": ["habere"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("exhibit", "habere", "verb", "/ɪɡˈzɪbɪt/",
          "ex-（向外）+ hibit（持有）→ 把手里的东西拿出来给人看",
          "拉丁语 exhibere（拿出、呈现），来自 ex＋habere",
          "to show something publicly, or to display a quality",
          "holding a thing out where others may see it – 把攥住的东西伸出去让人看",
          "他摊开掌心，把那枚旧币举到灯下让众人看",
          ["展出", "展示", "表现出"],
          ["The museum will exhibit her early work.", "He exhibited no sign of fear."],
          ["display", "show"], ["conceal", "hide"],
          ["inhibit", "prohibit"],
          ["展出/展示：把持有之物拿出来给人看", "表现出：把内里的性质显露到外面"],
          "ex-（向外）+ hibit（持有）→ 把手里的拿出来给人看"),
        W("inhibit", "habere", "verb", "/ɪnˈhɪbɪt/",
          "in-（向内）+ hibit（持有）→ 往回攥住不放 → 抑制",
          "拉丁语 inhibere（拉住、制止），来自 in＋habere",
          "to hold back a process or feeling; to make someone self-conscious",
          "keeping the hand closed so the thing cannot come out – 手往回收，使之出不来",
          "话到嘴边又被咽了回去，掌心攥得更紧",
          ["抑制", "阻碍", "使拘束"],
          ["The drug inhibits the growth of bacteria.", "Fear of failure inhibited her."],
          ["restrain", "hinder"], ["encourage", "release"],
          ["exhibit", "prohibit"],
          ["抑制/阻碍：往回攥住、使发不出来", "使拘束：人被这股回收之力箝住"],
          "in-（向内）+ hibit（持有）→ 往回攥住不放"),
        W("prohibit", "habere", "verb", "/prəˈhɪbɪt/",
          "pro-（在前）+ hibit（持有）→ 伸手拦在前面不许过 → 禁止",
          "拉丁语 prohibere（拦住、禁止），来自 pro＋habere",
          "to forbid something formally, especially by law",
          "an arm held out in front so none may pass – 一臂横在前头，谁也过不去",
          "门口那只手一横，牌子上写着不许带火进去",
          ["禁止", "阻止"],
          ["The law prohibits smoking indoors.", "Signs prohibit entry after dark."],
          ["forbid", "ban"], ["permit", "allow"],
          ["exhibit", "inhibit"],
          ["禁止/阻止：伸手拦在前面不许通行"],
          "pro-（在前）+ hibit（持有）→ 伸手横拦在前"),
    ],
})

# ---------- manus（手）----------
families.append({
    "root": {
        "id": "manus", "root": "manus", "variants": ["man", "manu", "main"],
        "origin": "拉丁语 manus（手）；manuālis（手上的）、manuārius 及意大利语 maneggiare"
                  "（驯马、经手打理）都由此出",
        "core_concept": "the hand that takes hold and works a thing / 一双上手打理事物的手",
        "core_image": "一双手把缰绳收在掌里，一收一放都由这双手定",
        "english_definition": "hand, by hand",
    },
    "concept": {
        "id": "concept-manus-hand", "concept": "the hand that takes hold and works a thing",
        "chinese": "上手打理", "core_image": "缰绳收在掌里，一收一放都由这双手定",
        "root_ids": ["manus"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("manage", "manus", "verb", "/ˈmænɪdʒ/",
          "man（手）+ -age → 亲手把事牵住打理 → 经营、设法办成",
          "意大利语 maneggiare（用手驯马、经手打理），来自拉丁语 manus（手）",
          "to be in charge of something; to succeed in doing something difficult",
          "keeping the reins in hand so the thing goes where one wants – 把缰绳握在手里，使其听使唤",
          "缰绳一紧一松，性子最烈的马也顺着走了",
          ["管理", "设法完成", "勉力应付"],
          ["She manages a team of twelve.", "He managed to finish before the deadline."],
          ["handle", "administer"], ["neglect"],
          ["manner", "manual"],
          ["管理：把事牵在手里打理", "设法完成/勉力应付：手上使力，硬把难事牵成"],
          "man（手）+ -age → 把缰绳握在手里打理"),
        W("manner", "manus", "noun", "/ˈmænə(r)/",
          "man（手）+ -er → 上手做一件事的手法 → 方式；复数指待人的举止",
          "盎格鲁法语 manere，来自拉丁语 manuarius（手上的）← manus",
          "the way in which something is done; a person's way of behaving",
          "the particular way the hand goes about a thing – 那双手上手时的特定手法",
          "同一道菜，他下刀的手法和别人明显不同",
          ["方式", "举止", "礼貌"],
          ["He answered in a friendly manner.", "It is bad manners to interrupt."],
          ["way", "behaviour"], [],
          ["manage", "manual"],
          ["方式：上手做事的那套手法", "举止/礼貌：待人时手上与身上的分寸"],
          "man（手）+ -er → 上手做事的那套手法"),
        W("manual", "manus", "adjective", "/ˈmænjuəl/",
          "manu（手）+ -al（…的）→ 靠手做的；名词指握在手里的那本册子",
          "拉丁语 manualis（手上的、便于手持的），来自 manus",
          "done with the hands rather than by machine; a book of instructions",
          "what is worked by hand, and the book held in one – 靠手来做的，以及手上拿的那本册子",
          "机器停了，几个人挽起袖子一件件搬；旁边摊着一本翻旧的册子",
          ["手工的", "体力的", "手册"],
          ["This is manual work, not automated.", "Check the manual before you start."],
          ["handmade", "handbook"], ["automatic"],
          ["manage", "manner"],
          ["手工的/体力的：靠一双手来做的", "手册：可握在手里翻的那本说明"],
          "manu（手）+ -al → 靠手做的，及手持的那本册子"),
    ],
})

# ---------- structus（垒砌）----------
families.append({
    "root": {
        "id": "structus", "root": "structus", "variants": ["struct", "stru"],
        "origin": "拉丁语 struere（一层层垒起来）的过去分词 structus；"
                  "instruere 本义是「把材料备齐垒上」，引申为教导",
        "core_concept": "to pile layer on layer into a standing whole / 一层层垒起来，成为立得住的整体",
        "core_image": "砖一层压一层垒上去，垒到最后自己立得稳",
        "english_definition": "to pile up, build",
    },
    "concept": {
        "id": "concept-structus-build", "concept": "to pile layer on layer into a standing whole",
        "chinese": "层层垒起", "core_image": "砖一层压一层垒上去，垒稳了自己立得住",
        "root_ids": ["structus"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("construction", "structus", "noun", "/kənˈstrʌkʃn/",
          "con-（一起）+ struct（垒）+ -ion → 把材料一并垒起来这件事，及垒成之物",
          "拉丁语 constructio（构筑），来自 construere（垒建）← con＋struere",
          "the act of building something, or the thing built",
          "the piling of parts together until it stands – 各部分一并垒起、直到立住",
          "脚手架一层层往上升，砖也一层层压上去",
          ["建造", "建筑物", "结构"],
          ["The bridge is still under construction.", "It is a steel construction."],
          ["building", "assembly"], ["destruction"],
          ["destruction", "instruction"],
          ["建造：把材料一并垒起的过程", "建筑物/结构：垒起来立住的那个整体"],
          "con-（一起）+ struct（垒）+ -ion → 一并垒起、立成整体"),
        W("destruction", "structus", "noun", "/dɪˈstrʌkʃn/",
          "de-（向下）+ struct（垒）+ -ion → 把垒起来的一层层拆掉推倒",
          "拉丁语 destructio（拆毁），来自 destruere（拆垒）← de＋struere",
          "the act of ruining something completely",
          "the pile taken back down until nothing stands – 把垒起的一层层卸到什么都不剩",
          "墙体一层层往下塌，最后只余一地碎砖",
          ["破坏", "摧毁", "毁灭"],
          ["The storm caused widespread destruction.", "War brought the destruction of the old town."],
          ["ruin", "demolition"], ["construction", "creation"],
          ["construction", "instruction"],
          ["破坏/摧毁：把垒起之物一层层卸掉推倒", "毁灭：卸到什么也不剩"],
          "de-（向下）+ struct（垒）+ -ion → 把垒起的拆到不剩"),
        W("instruction", "structus", "noun", "/ɪnˈstrʌkʃn/",
          "in-（向内）+ struct（垒）+ -ion → 往人心里一层层垒进去 → 教导、指示",
          "拉丁语 instructio（备置、教导），来自 instruere（备齐垒上）← in＋struere",
          "teaching, or a statement telling someone what to do",
          "laying knowledge in course by course inside someone – 往人里头一层层垒进去",
          "师傅一步一步讲，学徒心里的底子一层层垒实",
          ["指示", "说明", "教导"],
          ["Follow the instructions on the label.", "She received instruction in music."],
          ["direction", "teaching"], [],
          ["construction", "destruction"],
          ["指示/说明：把该怎么做一层层交代进去", "教导：把学问往人心里垒实"],
          "in-（向内）+ struct（垒）+ -ion → 往人心里一层层垒进去"),
    ],
})

# ---------- spatium（间距）----------
families.append({
    "root": {
        "id": "spatium", "root": "spatium", "variants": ["spac", "spat"],
        "origin": "拉丁语 spatium（跨开的距离、场地、一段时间），原与「迈步跨开」相关",
        "core_concept": "the gap opened up between things / 物与物之间撑开的那段距离",
        "core_image": "两手向左右撑开，中间空出一段谁也不占的距离",
        "english_definition": "distance, room, extent",
    },
    "concept": {
        "id": "concept-spatium-gap", "concept": "the gap opened up between things",
        "chinese": "撑开的距离", "core_image": "两手左右撑开，中间空出一段谁也不占的地方",
        "root_ids": ["spatium"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("space", "spatium", "noun", "/speɪs/",
          "spatium（跨开的距离）→ 物之间空出的地方；引申为大气之外那片空阔",
          "古法语 espace，来自拉丁语 spatium（距离、场地）",
          "an empty area available for use; the region beyond the earth's air",
          "the emptiness left open between things – 物与物之间留着的那段空",
          "两本书之间空着一指宽，正好再塞一本进去",
          ["空间", "地方", "太空"],
          ["There is space for one more chair.", "The rocket vanished into space."],
          ["room", "gap"], [],
          ["spacious", "spaceship"],
          ["空间/地方：物之间空出可用的那段", "太空：大气之外那片空阔无物之处"],
          "spatium（跨开的距离）→ 物之间空出的那段"),
        W("spaceship", "spatium", "noun", "/ˈspeɪsʃɪp/",
          "space（太空）+ ship（船）→ 在那片空阔里航行的船",
          "英语复合词 space＋ship，20 世纪初随航天想象出现",
          "a vehicle used for travelling beyond the earth's air",
          "a vessel that sails the open emptiness – 在那片空阔里航行的船",
          "舷窗外一片漆黑，船身静静滑过没有风的地方",
          ["宇宙飞船", "太空船"],
          ["The spaceship docked with the station.", "Children drew a spaceship on the wall."],
          ["spacecraft", "rocket"], [],
          ["space", "spacious"],
          ["宇宙飞船/太空船：在那片空阔里航行的船"],
          "space（那片空阔）+ ship（船）→ 在其中航行的船"),
        W("spacious", "spatium", "adjective", "/ˈspeɪʃəs/",
          "spac（距离）+ -ious（多…的）→ 空出的距离足够多的",
          "拉丁语 spatiosus（宽阔的），来自 spatium",
          "having plenty of room inside",
          "holding a wide gap within, nothing pressing – 内里撑得开，四下不挤",
          "推门进去，四壁离得老远，脚步声都有回响",
          ["宽敞的", "广阔的"],
          ["The flat is bright and spacious.", "They crossed a spacious hall."],
          ["roomy", "vast"], ["cramped", "narrow"],
          ["space", "spaceship"],
          ["宽敞的/广阔的：内里撑开的距离足够多"],
          "spac（距离）+ -ious（多…的）→ 内里撑得开、不挤"),
    ],
})

# ---------- stringere（拉紧）----------
families.append({
    "root": {
        "id": "stringere", "root": "stringere", "variants": ["strain", "strict", "string"],
        "origin": "拉丁语 stringere（拉紧、束紧），过去分词 strictus；"
                  "strict（严格）、string（弦）同根",
        "core_concept": "to draw a cord tight so movement is checked / 把绳收紧，使动弹不得",
        "core_image": "绳子越收越紧，勒在物上，想动也动不了多少",
        "english_definition": "to draw tight, bind",
    },
    "concept": {
        "id": "concept-stringere-tighten", "concept": "to draw a cord tight so movement is checked",
        "chinese": "收紧勒住", "core_image": "绳子越收越紧勒在物上，想动也动不了多少",
        "root_ids": ["stringere"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("constrain", "stringere", "verb", "/kənˈstreɪn/",
          "con-（加强）+ strain（拉紧）→ 四面收紧，把人限在窄处",
          "古法语 constraindre，来自拉丁语 constringere（束紧）← con＋stringere",
          "to limit someone's freedom of action; to force a course",
          "cords drawn tight on every side so only one way is left – 四面收紧，只剩一条路可走",
          "四根绳同时收紧，能挪的余地只剩一寸",
          ["限制", "约束", "强迫"],
          ["Tight budgets constrain our choices.", "He felt constrained to agree."],
          ["restrict", "compel"], ["free", "release"],
          ["restrain", "strain"],
          ["限制/约束：四面收紧、余地被勒小", "强迫：紧到只剩一条路可走"],
          "con-（加强）+ strain（拉紧）→ 四面收紧、只剩一条路"),
        W("restrain", "stringere", "verb", "/rɪˈstreɪn/",
          "re-（往回）+ strain（拉紧）→ 往回一拽收住 → 拦住、克制",
          "古法语 restraindre，来自拉丁语 restringere（拉回束住）← re＋stringere",
          "to hold someone or something back; to keep a feeling in check",
          "pulling the cord back to check something mid-motion – 往回一拽，把正要动的收住",
          "他刚要冲上去，绳子似的一只手把他往后一带",
          ["制止", "拦住", "克制"],
          ["Two officers restrained the man.", "She restrained her anger."],
          ["hold back", "curb"], ["release", "provoke"],
          ["constrain", "strain"],
          ["制止/拦住：往回一拽把正动的收住", "克制：把自己的情绪往回收紧"],
          "re-（往回）+ strain（拉紧）→ 往回拽住收停"),
        W("strain", "stringere", "noun / verb", "/streɪn/",
          "strain（拉紧）→ 被拉紧时承的那股劲，及拉过头造成的伤",
          "古法语 estreindre，来自拉丁语 stringere（拉紧）",
          "force pulling on something; pressure on a person; to injure by overstretching",
          "the pull borne by a cord stretched near its limit – 绷到将断时那根绳承着的劲",
          "绳子绷得笔直，纤维吱吱作响，眼看要断",
          ["拉力", "压力", "拉伤"],
          ["The rope broke under the strain.", "He strained a muscle while lifting."],
          ["tension", "pressure"], ["relaxation"],
          ["constrain", "restrain"],
          ["拉力/压力：被拉紧时承着的那股劲", "拉伤：拉过了头、绷出来的伤"],
          "strain（拉紧）→ 绷紧时承的劲，绷过头即伤"),
    ],
})

# ================= 补词：挂已建模词根 =================
# forma / portus 两根刚由 scripts/migrate_root_ids_latin.py 从 form / port 改名，
# 自环边限制解除，这四个词才得以入库。
additions = [
    W("form", "forma", "noun / verb", "/fɔːm/",
      "forma（形状、模子）→ 物体的外廓；引申为定下来的规范式样，及使之成形",
      "古法语 forme，来自拉丁语 forma（形状、模子）",
      "the shape of something; a printed sheet with blanks to fill; to bring into shape",
      "the outline a thing settles into – 事物定下来的那个外廓",
      "泥坯在轮盘上转，手一收，边缘就定住了",
      ["形状", "形式", "表格"],
      ["The lake has the form of a crescent.", "Please fill in this form and sign it."],
      ["shape", "structure"], [],
      ["formal", "perform"],
      ["形状/形式：事物定下来的那个外廓", "表格：把要填之项定成规范式样的那张纸"],
      "forma（形状、模子）→ 定下来的外廓与式样"),
    W("former", "forma", "adjective", "/ˈfɔːmə(r)/",
      "forma（最先的）+ -er（比较）→ 两者之中在先的那个",
      "中古英语 formere，来自古英语 forma（最先的）；与 forma（形状）同形，"
      "此处取「最先」一支",
      "of an earlier time; the first of two things mentioned",
      "the one standing earlier in the line of two – 两者并列时在先的那个",
      "两个名字并排写着，手指点住上面那个",
      ["以前的", "前者的"],
      ["Her former employer wrote the reference.", "Of the two routes, the former is shorter."],
      ["previous", "earlier"], ["latter"],
      ["form", "formal"],
      ["以前的/前者的：两者并列时处在先的那个"],
      "forma（最先的）+ -er → 两者中在先的那个"),
    W("performance", "forma", "noun", "/pəˈfɔːməns/",
      "per-（彻底）+ form（成形）+ -ance → 把一件事彻底做成形 → 当众做完的一场，及成效",
      "盎格鲁法语 parfourmance，来自 parfournir（彻底完成）← per＋fournir，"
      "后受 form 影响改拼",
      "an act of presenting a play or music before an audience; how well someone does something",
      "carrying a thing through until it stands fully formed – 把一件事一路做到彻底成形",
      "幕布拉开，她把整支曲子一气走完",
      ["表演", "演出", "表现"],
      ["The evening performance starts at eight.", "His performance at work has improved."],
      ["show", "achievement"], [],
      ["perform", "form"],
      ["表演/演出：当众把一件事彻底做成形的那一场", "表现：把事做到什么成形程度，即成效"],
      "per-（彻底）+ form（成形）→ 彻底做成形的一场与其成效"),
    W("port", "portus", "noun", "/pɔːt/",
      "portus（港、门道）与 portare（运送）同族 → 货物由船转陆的那个口",
      "拉丁语 portus（港口、门道），与 portare（运送）同族",
      "a town or place where ships load and unload",
      "the mouth where goods pass between ship and shore – 货物在船与岸之间过渡的那个口",
      "吊臂起落，成箱货物从船舷转到岸上",
      ["港口", "口岸"],
      ["The ship reached port before dawn.", "Grain is shipped through this port."],
      ["harbour", "dock"], ["inland"],
      ["import", "export"],
      ["港口/口岸：货物在船与岸之间过渡的那个口"],
      "portus（港、门道）→ 货物由船转陆的那个口"),
]

# ================= 组装 =================
words = []
for fam in families:
    words.extend(fam["words"])
words.extend(additions)

roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
# 同域多根必须累积追加（dict 直接赋值会丢根，第三十六批踩过）
domain_add = {}
for f in families:
    domain_add.setdefault(f["domain"], []).append(f["root"]["id"])

# ---- 生成期自检：review.py check 不查 Q12，合并后 validate.py 才查 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"

assert len(words) == 22, len(words)
assert len(roots) == 6, len(roots)
assert len({r["id"] for r in roots}) == 6, "新词根 id 有重复"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words "
      f"({len(words) - len(additions)} family + {len(additions)} additions), "
      f"{len(roots)} new roots")
