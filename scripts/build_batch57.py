#!/usr/bin/env python3
"""Generate batch57: 12 个新词根、46 词——词根型批次的第二部分。

来路：子代理起草日耳曼批次时按词源筛出的词（见 screen_draft_etymology.py）。
这些词的拉丁/希腊词根在考研词表里各有 3 个以上成员，值得建根——
一个 carrus 根一次带出 7 词，比逐个写孤立词条划算，且它们在图谱上成簇。

  carrus（四轮货车）    car / carry / carriage / carrier / cargo / career / charge
  tradere（交付出去）   betray / tradition / traitor / treason
  bainein（走、踏）     base / basic / basis / basement / baseball
  charta（纸叶）        card / chart / charter / cartoon
  campus-field（原野）  camp / campus / campaign / champion
  circulus（小环）      circle / circular / circus / circuit
  bulla（铅封、圆泡）   bulletin / bullet / bowling
  battuere（打）        battle / combat / debate
  canalis（管、芦管）   canal / channel / cannon
  caput（头）           chief / chef / cattle
  citare（召唤）        cite / excite / recite
  klinein（倾斜）       climate / climax / clinic

【词根 id 避自环】
basis 与 campus 本身就是本批要收的单词，拿它们作词根 id 会产生自环边
（form/port/flu/press 已踩过四次），故改用别的词形：
  basis  → bainein（希腊语 bainein 走、踏，basis 由此出）
  campus → campus-field（照 edere-publish、ter-comparative 的加后缀先例）

【本批剔除的同形异源词】
  bull（公牛）← 古英语 bula ← 原始日耳曼语 *bulô，日耳曼源。
       只有「教皇诏书」那一义才出拉丁 bulla（铅封），常用义不属此族
  trade ← 中古低地德语 trade（足迹、路径），与 tread（踩）同源，
       与拉丁 tradere（交付）无关，只是拼写近
两词已退回日耳曼池。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch57.json"


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

# ---------- carrus（四轮货车）----------
families.append({
    "root": {
        "id": "carrus", "root": "carrus", "variants": ["car", "carri", "charg", "cargo"],
        "origin": "拉丁语 carrus（四轮货车），借自高卢语；经古北法语 carre、"
                  "西班牙语 cargar（装车）等分支入英语",
        "core_concept": "a wheeled cart and what it takes on / 一辆载货的车，以及装上去的东西",
        "core_image": "一辆四轮车停在场上，货一件件往车板上码",
        "english_definition": "wheeled cart, to convey by cart",
    },
    "concept": {
        "id": "concept-carrus-cart", "concept": "a wheeled cart and the load it takes on",
        "chinese": "载货的车", "core_image": "四轮车停在场上，货一件件往车板上码",
        "root_ids": ["carrus"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("car", "carrus", "noun", "/kɑː(r)/",
          "carrus（四轮货车）→ 带轮子载人载物的那种车",
          "古北法语 carre ← 拉丁语 carrus（四轮货车）",
          "a road vehicle with an engine and four wheels",
          "the wheeled box one gets into and is taken along in – 坐进去、被它带着走的那个带轮子的箱",
          "四个轮子撑着一个铁壳，人坐进去合上门",
          ["汽车", "车厢"],
          ["She parked the car outside.", "The train has eight cars."],
          ["vehicle", "automobile"], [],
          ["carry", "carriage"],
          ["汽车：带轮载人的那种车", "车厢：列车上同样带轮的一节"],
          "carrus（四轮货车）→ 带轮子载人载物的车"),
        W("carry", "carrus", "verb", "/ˈkæri/",
          "carrus（货车）→ carriare（用车运）→ 把东西带着走",
          "盎格鲁法语 carier（用车运）← 通俗拉丁语 carricare ← carrus（货车）",
          "to hold something and take it with you",
          "taking a load along instead of leaving it where it lay – 把货带着走，而不是留在原地",
          "他把箱子抱起来，一路没放下过",
          ["搬运", "携带", "载运"],
          ["She carried the box upstairs.", "This bus carries fifty people."],
          ["bear", "convey"], ["drop"],
          ["car", "cargo"],
          ["搬运/携带：把东西带着走", "载运：车船同样把货带着走"],
          "carrus（货车）→ carriare（用车运）→ 带着走"),
        W("carriage", "carrus", "noun", "/ˈkærɪdʒ/",
          "carry（用车运）+ -age → 供载运的那辆车，及载运这件事",
          "盎格鲁法语 cariage ← carier ← 通俗拉丁语 carricare ← carrus",
          "a vehicle pulled by horses; a railway coach; the act of carrying",
          "the box on wheels made to be pulled – 造出来专供人拉着走的那个带轮的厢",
          "两匹马在前头，后面那个厢一晃一晃跟着",
          ["马车", "车厢", "运输"],
          ["A horse-drawn carriage waited outside.", "Goods carriage costs extra."],
          ["coach", "transport"], [],
          ["car", "carry"],
          ["马车/车厢：供载运的那个带轮的厢", "运输：把货带着走这件事本身"],
          "carry（用车运）+ -age → 供载运的车及其事"),
        W("carrier", "carrus", "noun", "/ˈkæriə(r)/",
          "carry（带着走）+ -er → 负责把东西带着走的人或物",
          "英语 carrier，来自 carry ← 通俗拉丁语 carricare ← carrus",
          "a person or thing that transports something; one who spreads a disease",
          "whatever the load is handed to for the journey – 把货交给它、由它带走的那个",
          "包裹交到那人手上，第二天出现在另一座城",
          ["运送者", "承运人", "带菌者"],
          ["The carrier delivered it by noon.", "Mosquitoes are carriers of malaria."],
          ["transporter", "bearer"], [],
          ["carry", "cargo"],
          ["运送者/承运人：受托把货带走的那方", "带菌者：同样是被病带着走的那个载体"],
          "carry（带着走）+ -er → 负责带走的那个"),
        W("cargo", "carrus", "noun", "/ˈkɑːɡəʊ/",
          "carrus（货车）→ 西班牙语 cargar（装车）→ 装在车船上的那批货",
          "西班牙语 cargo（装载物）← cargar（装车）← 通俗拉丁语 carricare ← carrus",
          "the goods carried by a ship, plane, or truck",
          "what fills the hold once the loading is done – 装完之后填满舱里的那批东西",
          "舱盖掀开，底下一层层码到顶都是箱子",
          ["货物", "载货"],
          ["The ship carried a cargo of grain.", "Cargo planes fly overnight."],
          ["freight", "load"], [],
          ["carry", "carrier"],
          ["货物/载货：装在车船上被带走的那批东西"],
          "carrus（货车）→ cargar（装车）→ 装上去的货"),
        W("career", "carrus", "noun", "/kəˈrɪə(r)/",
          "carrus（车）→ carraria（车道）→ 跑道 → 一个人走过的那条职业道",
          "法语 carrière（跑马道）← 意大利语 carriera ← 通俗拉丁语 carraria（车道）← carrus",
          "the series of jobs a person has over their working life",
          "the track laid for wheels, and by extension the course one runs – 给车轮铺出的那条道，引申为人一路跑下来的路线",
          "车辙压出两道印子，后来的车都顺着这两道走",
          ["职业", "生涯", "事业"],
          ["She had a long career in law.", "He changed careers at forty."],
          ["profession", "vocation"], [],
          ["car", "carriage"],
          ["职业/事业：一个人顺着走下来的那条道", "生涯：这条道从头到尾的整段"],
          "carrus（车）→ carraria（车道）→ 人走的职业道"),
        W("charge", "carrus", "verb", "/tʃɑːdʒ/",
          "carrus（货车）→ carricare（装车）→ 把担子压上去 → 收费、指控、充电",
          "古法语 chargier（装载）← 通俗拉丁语 carricare（装车）← carrus（货车）",
          "to ask a price; to accuse formally; to put electricity into",
          "loading a weight onto someone or something – 把一份分量压到人或物身上",
          "货往车上一压，车轴吃住了那个重量",
          ["收费", "指控", "充电", "冲锋"],
          ["They charge ten pounds for entry.", "He was charged with theft."],
          ["bill", "accuse"], ["discharge"],
          ["cargo", "carry"],
          ["收费：把价钱这份分量压给顾客", "指控：把罪名压到人身上", "充电：把电这份量压进电池", "冲锋：把整个人的势压向前"],
          "carrus（货车）→ carricare（装车）→ 把分量压上去"),
    ],
})

# ---------- tradere（交付出去）----------
families.append({
    "root": {
        "id": "tradere", "root": "tradere", "variants": ["trad", "trait", "treas"],
        "origin": "拉丁语 tradere（交付、移交），由 trans（越过）＋dare（给）构成；"
                  "交出去的东西是好是坏，分出「传承」与「背卖」两支",
        "core_concept": "handing a thing across into other hands / 把东西越过界交到别人手里",
        "core_image": "一样东西从这只手越过去，落进对面那只手",
        "english_definition": "to hand over, deliver up",
    },
    "concept": {
        "id": "concept-tradere-hand-over", "concept": "handing a thing across into other hands",
        "chinese": "交付出去", "core_image": "东西从这只手越过去，落进对面那只手",
        "root_ids": ["tradere"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("tradition", "tradere", "noun", "/trəˈdɪʃn/",
          "trad（交付）+ -ition → 一代代交下来的那套 → 传统",
          "拉丁语 traditio（交付、口传）← tradere（交付）← trans＋dare",
          "a custom or belief passed down over generations",
          "what each generation puts into the next pair of hands – 每一代交到下一双手里的那份",
          "老人把那套做法一样样交给儿子，儿子照着又教给孙子",
          ["传统", "惯例", "传承"],
          ["It is a family tradition.", "The town keeps its old traditions."],
          ["custom", "heritage"], [],
          ["traitor", "treason"],
          ["传统/惯例：一代代交下来、照着做的那套", "传承：交这个动作本身"],
          "trad（交付）+ -ition → 一代代交下来的那套"),
        W("traitor", "tradere", "noun", "/ˈtreɪtə(r)/",
          "trait（交付）+ -or（人）→ 把自己一方交出去的那个人",
          "古法语 traitre ← 拉丁语 traditor（交付者、叛卖者）← tradere",
          "a person who betrays their country or friends",
          "the one who hands his own side over to the other – 把自己这边交到对面手里的那个",
          "他把名册递了出去，第二天册上的人一个个被带走",
          ["叛徒", "卖国者"],
          ["He was executed as a traitor.", "They called her a traitor."],
          ["betrayer", "defector"], ["patriot", "loyalist"],
          ["treason", "betray"],
          ["叛徒/卖国者：把自己一方交到对面手里的那个人"],
          "trait（交付）+ -or（人）→ 把自己一方交出去的人"),
        W("treason", "tradere", "noun", "/ˈtriːzn/",
          "treas（交付）+ -on → 把国家交出去这桩罪",
          "盎格鲁法语 treisoun ← 拉丁语 traditio（交付、叛卖）← tradere",
          "the crime of betraying one's own country",
          "the act of handing one's own country across – 把自己的国交出去这个行为",
          "图纸从抽屉里取出，越过边境线递到了对面",
          ["叛国罪", "背叛"],
          ["He was tried for treason.", "Such an act amounts to treason."],
          ["betrayal", "sedition"], ["loyalty"],
          ["traitor", "tradition"],
          ["叛国罪：把自己的国交出去这桩罪", "背叛：同一个交出去的动作，泛用"],
          "treas（交付）+ -on → 把国交出去这桩罪"),
        W("betray", "tradere", "verb", "/bɪˈtreɪ/",
          "be-（加强）+ tray（交付）→ 把托付之物交给外人 → 背叛；引申为无意露出",
          "中古英语 betrayen，由 be-＋古法语 trair ← 拉丁语 tradere（交付）",
          "to be disloyal to someone; to reveal something unintentionally",
          "handing over what was entrusted to you – 把托付给自己的东西交了出去",
          "钥匙本是托他保管，他却把它递到了外人手上",
          ["背叛", "泄露", "流露"],
          ["He betrayed his closest friend.", "Her face betrayed her fear."],
          ["deceive", "reveal"], ["protect"],
          ["traitor", "treason"],
          ["背叛：把托付之物交给外人", "泄露：把不该交的消息交了出去", "流露：神情不自觉把心里的事交了出来"],
          "be-（加强）+ tray（交付）→ 把托付之物交出去"),
    ],
})

# ---------- bainein（走、踏）----------
families.append({
    "root": {
        "id": "bainein", "root": "bainein", "variants": ["bas", "base", "basi"],
        "origin": "希腊语 bainein（走、踏），其名词 basis 本义「踏脚处、立足点」，"
                  "经拉丁语 basis 入英语；词根 id 用动词形 bainein，"
                  "因 basis 本身是本批要收的单词，作 id 会产生自环边",
        "core_concept": "the spot the foot comes down on, what everything above rests on / 脚落下的那一处，上面全靠它撑",
        "core_image": "脚踩实了那块石头，整个人的重量才敢压上去",
        "english_definition": "to step, a footing",
    },
    "concept": {
        "id": "concept-bainein-footing", "concept": "the spot the foot comes down on",
        "chinese": "立足之处", "core_image": "脚踩实那块石头，整个人的重量才敢压上去",
        "root_ids": ["bainein"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("base", "bainein", "noun", "/beɪs/",
          "basis（踏脚处）→ 底下承重的那一处 → 底座、基地",
          "古法语 bas ← 拉丁语 basis ← 希腊语 basis（踏脚处）← bainein（踏）",
          "the lowest part that supports something; a centre of operations",
          "the part everything above puts its weight on – 上面所有重量都压在它身上的那一层",
          "柱子底下那块方石承着整根柱，抽掉它上面就塌",
          ["底部", "基础", "基地"],
          ["The base of the lamp is heavy.", "They returned to base at dusk."],
          ["bottom", "foundation"], ["top"],
          ["basic", "basement"],
          ["底部/基础：上面重量全压在它身上的那一层", "基地：一切行动的落脚与出发之处"],
          "basis（踏脚处）→ 底下承重的那一层"),
        W("basis", "bainein", "noun", "/ˈbeɪsɪs/",
          "basis（踏脚处）→ 论证或安排所立足的那一点",
          "拉丁语 basis ← 希腊语 basis（踏脚处）← bainein（踏）",
          "the facts or ideas from which something is developed",
          "the footing an argument stands on – 一番道理踩着立住的那一点",
          "他先把那个前提摆稳，后面的话才踩得住",
          ["基础", "根据", "依据"],
          ["What is the basis of your claim?", "We meet on a weekly basis."],
          ["foundation", "grounds"], [],
          ["base", "basic"],
          ["基础：整套说法立足的那一点", "根据/依据：拿它当立足点来论证"],
          "basis（踏脚处）→ 论证立足的那一点"),
        W("basic", "bainein", "adjective", "/ˈbeɪsɪk/",
          "base（底层）+ -ic → 属于最底那一层的 → 基本的",
          "英语 basic，来自 base ← 希腊语 basis（踏脚处）",
          "forming the simplest and most necessary part of something",
          "the layer nothing else can be put under – 底下再没有别的一层了",
          "把上面几层都揭掉，剩下这层再往下就没有了",
          ["基本的", "初级的", "必需的"],
          ["Learn the basic rules first.", "The room has only basic furniture."],
          ["fundamental", "elementary"], ["advanced", "complex"],
          ["base", "basis"],
          ["基本的/必需的：底下再没有一层可揭的", "初级的：从最底那层学起的"],
          "base（底层）+ -ic → 属于最底那一层"),
        W("basement", "bainein", "noun", "/ˈbeɪsmənt/",
          "base（底部）+ -ment → 房子最底下那一层",
          "英语 basement，来自 base ← 希腊语 basis（踏脚处）",
          "the floor of a building that is below ground level",
          "the storey the whole house stands on, dug into the ground – 整栋房子踩着的那一层，埋在地里",
          "顺楼梯往下走到底，头顶就是一楼的地板",
          ["地下室", "底层"],
          ["They store boxes in the basement.", "The basement floods every spring."],
          ["cellar", "vault"], ["attic"],
          ["base", "basic"],
          ["地下室/底层：整栋房子踩着的、埋在地里那一层"],
          "base（底部）+ -ment → 房子最底那一层"),
        W("baseball", "bainein", "noun", "/ˈbeɪsbɔːl/",
          "base（垒、踏脚处）+ ball（球）→ 绕垒跑的那种球赛",
          "英语复合词 base＋ball；base ← 希腊语 basis（踏脚处）",
          "a game in which players hit a ball and run round four bases",
          "the game named after the spots the runner must step on – 以跑者必须踩到的那几处得名的球赛",
          "打完那一棒他就跑，脚一个个点过场上那四块垫子",
          ["棒球"],
          ["They played baseball all afternoon.", "He collects baseball cards."],
          ["ballgame", "sport"], [],
          ["base", "basic"],
          ["棒球：以跑者要踩的那几处（垒）得名的球赛"],
          "base（垒）+ ball（球）→ 绕垒跑的球赛"),
    ],
})
