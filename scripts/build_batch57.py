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
          ["car", "truck"], [],
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
          ["carrier", "ship"], [],
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
          ["load", "goods"], [],
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
          ["rebel", "spy"], ["loyal", "faith"],
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
          ["crime", "revolt"], ["loyalty"],
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
          ["foundation", "reason"], [],
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
          ["cellar", "store"], ["roof"],
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
          ["sport", "play"], [],
          ["base", "basic"],
          ["棒球：以跑者要踩的那几处（垒）得名的球赛"],
          "base（垒）+ ball（球）→ 绕垒跑的球赛"),
    ],
})

# ---------- charta（纸叶）----------
families.append({
    "root": {
        "id": "charta", "root": "charta", "variants": ["chart", "card", "cart"],
        "origin": "拉丁语 charta（纸莎草叶、纸）← 希腊语 khartēs（纸卷）；"
                  "经意大利语 carta、法语 carte 分支入英语",
        "core_concept": "a flat sheet that carries marks / 一张平面，用来承载写画的东西",
        "core_image": "一张硬纸铺开，上面画的线和字一目了然",
        "english_definition": "sheet of papyrus, paper",
    },
    "concept": {
        "id": "concept-charta-sheet", "concept": "a flat sheet that carries marks",
        "chinese": "承载写画的纸", "core_image": "硬纸铺开，上面画的线和字一目了然",
        "root_ids": ["charta"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("card", "charta", "noun", "/kɑːd/",
          "charta（纸）→ 裁成小张的硬纸片",
          "法语 carte ← 意大利语 carta ← 拉丁语 charta（纸）← 希腊语 khartēs",
          "a small piece of stiff paper used for messages, games, or identity",
          "the palm-sized stiff sheet you hand over or hold – 递出去或攥在手里那张巴掌大的硬纸",
          "他从钱包里抽出一张硬硬的小方片，递到柜台上",
          ["卡片", "纸牌", "证件"],
          ["She sent me a birthday card.", "He shuffled the cards twice."],
          ["ticket", "slip"], [],
          ["chart", "charter"],
          ["卡片：裁成小张的硬纸", "纸牌：印了花色供玩的那种小张", "证件：印了身份信息的那一张"],
          "charta（纸）→ 裁成小张的硬纸片"),
        W("chart", "charta", "noun", "/tʃɑːt/",
          "charta（纸）→ 画上线条数据的那张纸 → 图表、海图",
          "法语 charte ← 拉丁语 charta（纸）",
          "a sheet showing information as lines, figures, or a map",
          "the sheet whose marks let you read a whole situation at a glance – 靠纸上的线条一眼看出全局的那张",
          "墙上贴的那张纸画着起落的折线，谁走过都抬头看一眼",
          ["图表", "海图", "排行榜"],
          ["The chart shows monthly sales.", "The captain checked the chart."],
          ["graph", "diagram"], [],
          ["card", "charter"],
          ["图表：把数据画成线条的那张纸", "海图：画着航路水深的那张", "排行榜：把名次排成表的那张"],
          "charta（纸）→ 画上线条数据的那张纸"),
        W("charter", "charta", "noun", "/ˈtʃɑːtə(r)/",
          "chart（纸）+ -er → 写明权利的那份正式文书；动词指按约包租",
          "古法语 chartre ← 拉丁语 chartula（小纸片、文书）← charta（纸）",
          "a formal document stating rights; to hire a vehicle for exclusive use",
          "the sheet whose words bind, once sealed – 一旦盖了印，纸上的字就约束住人",
          "羊皮纸上盖了红印，从此城里的人按那上头写的办",
          ["宪章", "特许证", "包租"],
          ["The city received its charter in 1215.", "They chartered a plane."],
          ["deed", "contract"], [],
          ["card", "chart"],
          ["宪章/特许证：写明权利、盖印生效的那份文书", "包租：照文书约定独家使用车船"],
          "chart（纸）+ -er → 写明权利、盖印生效的文书"),
        W("cartoon", "charta", "noun", "/kɑːˈtuːn/",
          "carta（纸）+ -one（大）→ 大张硬纸上的草图 → 漫画、动画",
          "意大利语 cartone（厚纸板、草图）← carta ← 拉丁语 charta（纸）",
          "a humorous drawing; a film made from drawings",
          "the big sheet a drawing is worked out on before anything else – 别的都还没动，先在大张纸上画出来的那个",
          "一大张厚纸摊在桌上，草稿一格一格画满了",
          ["漫画", "动画片"],
          ["The cartoon made everyone laugh.", "Children watched a cartoon."],
          ["comic", "film"], [],
          ["card", "chart"],
          ["漫画：画在纸上、供人一看就笑的那种图", "动画片：由这类画一格格连成的影片"],
          "carta（纸）+ -one（大）→ 大张纸上的草图"),
    ],
})

# ---------- campus-field（原野）----------
families.append({
    "root": {
        "id": "campus-field", "root": "campus", "variants": ["camp", "champ", "campagn"],
        "origin": "拉丁语 campus（平坦原野、operations 用的场地）；"
                  "词根 id 加 -field 后缀，因 campus 本身是本批要收的单词，"
                  "作 id 会产生自环边（照 edere-publish、ter-comparative 先例）",
        "core_concept": "an open flat ground where things are staged / 一片摊开的平地，事在上头铺排",
        "core_image": "一片空旷平地，帐篷一排排扎开，中间留出走道",
        "english_definition": "open field, level ground",
    },
    "concept": {
        "id": "concept-campus-open-ground", "concept": "an open flat ground where things are staged",
        "chinese": "摊开的平地", "core_image": "空旷平地上帐篷一排排扎开，中间留出走道",
        "root_ids": ["campus-field"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("camp", "campus-field", "noun", "/kæmp/",
          "campus（原野）→ 在野地上扎下的临时住处",
          "法语 camp ← 意大利语 campo ← 拉丁语 campus（原野）",
          "a place with tents or huts where people stay temporarily",
          "cloth and poles set up on open ground, meant to come down again – 在空地上搭起来、还要拆走的那些棚帐",
          "空地上支起十几顶帐篷，绳子一头钉进土里",
          ["营地", "露营", "阵营"],
          ["They set up camp by the river.", "We camped for three nights."],
          ["base", "ground"], [],
          ["campus", "campaign"],
          ["营地/露营：在野地搭起、还要拆走的临时住处", "阵营：同一块地上聚起来的那一伙人"],
          "campus（原野）→ 野地上扎的临时住处"),
        W("campus", "campus-field", "noun", "/ˈkæmpəs/",
          "campus（原野）→ 学校所占的那整片地",
          "拉丁语 campus（原野），18 世纪美国普林斯顿用它指校地，遂成此义",
          "the grounds and buildings of a university or college",
          "the whole stretch of ground a school spreads over – 一所学校摊开来占住的那整片地",
          "从图书馆走到食堂要穿过两片草坪，全在同一圈围墙里",
          ["校园", "校区"],
          ["The campus has three libraries.", "She lives on campus."],
          ["yard", "field"], [],
          ["camp", "campaign"],
          ["校园/校区：一所学校摊开占住的那整片地"],
          "campus（原野）→ 学校占住的那整片地"),
        W("campaign", "campus-field", "noun", "/kæmˈpeɪn/",
          "campagna（旷野）→ 军队开到野地上打的那一仗 → 战役；引申为有组织的行动",
          "法语 campagne ← 意大利语 campagna（旷野）← 拉丁语 campus（原野）",
          "a planned series of actions to achieve a goal, military or public",
          "a run of moves carried out on open ground toward one end – 在开阔地上一步步铺排、朝一个目标去的那串动作",
          "队伍开到野地上驻下，一步步照计划往前推",
          ["战役", "运动", "竞选活动"],
          ["The campaign lasted six months.", "She ran a campaign for clean water."],
          ["operation", "drive"], [],
          ["camp", "campus"],
          ["战役：军队在野地上铺排的那一仗", "运动/竞选活动：同样有组织、朝一个目标推的那串行动"],
          "campagna（旷野）→ 野地上铺排的那一仗"),
        W("champion", "campus-field", "noun", "/ˈtʃæmpiən/",
          "campio（在场上格斗的人）← campus（场地）→ 场上胜出的那个 → 冠军",
          "古法语 champion ← 晚期拉丁语 campio（角斗者）← 拉丁语 campus（场地）",
          "a person who wins a competition; one who fights for a cause",
          "the one left standing on the field when the others are done – 场上比到最后还立着的那个",
          "场地中间只剩一个人站着，四周的人开始鼓掌",
          ["冠军", "拥护者"],
          ["She is the world champion.", "He championed the new law."],
          ["victor", "advocate"], ["loser"],
          ["camp", "campus"],
          ["冠军：场上比到最后立着的那个", "拥护者：同样在场上替某一方出战的人"],
          "campio（场上格斗者）← campus（场地）→ 胜出者"),
    ],
})

# ---------- circulus（小环）----------
families.append({
    "root": {
        "id": "circulus", "root": "circulus", "variants": ["circul", "circ", "circum"],
        "origin": "拉丁语 circulus（小环）是 circus（圆圈）的指小形 ← 希腊语 kirkos（环）；"
                  "circum（绕、环着）本是 circus 的宾格作副词用，故 circuit 一支也归此族",
        "core_concept": "a line that comes round to where it began / 一条线绕回到起点",
        "core_image": "用绳拴住笔一转，笔尖回到落笔那一点，圈就合上了",
        "english_definition": "small ring, circle",
    },
    "concept": {
        "id": "concept-circulus-ring", "concept": "a line that comes round to where it began",
        "chinese": "绕回起点的圈", "core_image": "绳拴笔一转，笔尖回到落笔那点，圈合上了",
        "root_ids": ["circulus"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("circle", "circulus", "noun", "/ˈsɜːkl/",
          "circulus（小环）→ 一圈闭合的线，及圈起来的那片",
          "古法语 cercle ← 拉丁语 circulus（小环）← circus（圆圈）",
          "a round shape whose edge is everywhere the same distance from the centre",
          "the closed line that ends exactly where it started – 终点正落在起点上的那条闭线",
          "笔尖绕一圈回到原处，纸上留下一条合起来的线",
          ["圆", "圈子", "环绕"],
          ["Draw a circle on the board.", "She has a small circle of friends."],
          ["ring", "loop"], [],
          ["circular", "circus"],
          ["圆：终点落回起点的那条闭线", "圈子：像那条线一样围起来的一小群人", "环绕：沿着那条线走一遍"],
          "circulus（小环）→ 终点落回起点的闭线"),
        W("circular", "circulus", "adjective", "/ˈsɜːkjələ(r)/",
          "circul（小环）+ -ar（…的）→ 圆形的；也指绕回原处的（论证）",
          "晚期拉丁语 circularis（属于环的）← circulus",
          "shaped like a circle; moving round; returning to the start",
          "of the form that leads back to where it set out – 属于那种走回原处的形状",
          "跑道绕了一整圈，起跑线和终点线是同一条",
          ["圆形的", "循环的", "通知（传阅件）"],
          ["The table has a circular top.", "That is a circular argument."],
          ["round", "circular"], ["straight"],
          ["circle", "circus"],
          ["圆形的：形如那条闭线", "循环的：绕一圈回到原处", "通知：绕着一圈人依次传阅的那张"],
          "circul（小环）+ -ar → 形如闭线、绕回原处"),
        W("circus", "circulus", "noun", "/ˈsɜːkəs/",
          "circus（圆圈）→ 圆形场地 → 在圆场里演的那种班子",
          "拉丁语 circus（圆圈、圆形竞技场）← 希腊语 kirkos（环）",
          "a travelling show with acrobats and animals, performed in a ring",
          "the round pit the audience sits all the way around – 观众围满一整圈的那个圆场",
          "帐篷中间空出一个圆场，看台把它整整围了一圈",
          ["马戏团", "圆形广场"],
          ["The circus came to town.", "They met at Piccadilly Circus."],
          ["show", "stage"], [],
          ["circle", "circular"],
          ["马戏团：在圆场里演出的那个班子", "圆形广场：几条路绕成一圈的那处场地"],
          "circus（圆圈）→ 圆形场地 → 圆场里的班子"),
        W("circuit", "circulus", "noun", "/ˈsɜːkɪt/",
          "circum（绕，circus 的宾格作副词）+ it（ire 行）→ 绕行一周 → 回路、巡回",
          "古法语 circuit ← 拉丁语 circuitus（绕行）← circum（绕）＋ire（行）；"
          "主根是 ire（行），但 circum 出自 circus，故归此族并在此注明",
          "a closed path, especially one electricity flows round; a regular tour",
          "the way that must close on itself for anything to move along it – 必须首尾接上、才走得通的那条路",
          "线从这头接到那头再绕回来，灯才亮起来",
          ["电路", "环线", "巡回"],
          ["The circuit was broken.", "The judge rides the circuit."],
          ["loop", "route"], [],
          ["circle", "circular"],
          ["电路：首尾接上才通电的那条闭路", "环线/巡回：同样绕一圈回到原处的路线"],
          "circum（绕）+ it（行）→ 绕行一周、首尾接上"),
    ],
})

# ---------- battuere（打）----------
families.append({
    "root": {
        "id": "battuere", "root": "battuere", "variants": ["batt", "bat", "bate"],
        "origin": "拉丁语 battuere（击打、拍击），通俗拉丁语里取代 caedere 成常用词；"
                  "英语 battle、combat、debate 均自此支",
        "core_concept": "blow answering blow between two sides / 两边一下接一下地对打",
        "core_image": "两只手轮着往下砸，一下接一下，谁也不肯先停",
        "english_definition": "to beat, strike",
    },
    "concept": {
        "id": "concept-battuere-strike", "concept": "blow answering blow between two sides",
        "chinese": "对打", "core_image": "两只手轮着往下砸，一下接一下，谁也不肯先停",
        "root_ids": ["battuere"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("battle", "battuere", "noun", "/ˈbætl/",
          "battuere（击打）→ battualia（操练、交手）→ 两军对打的那一场",
          "古法语 bataille ← 晚期拉丁语 battualia（击剑操练）← battuere（击打）",
          "a fight between armed forces; a struggle to achieve something",
          "two sides trading blows until one gives way – 两边对着打，直到一方撑不住",
          "两队人在坡上互相冲了几个来回，谁也没退",
          ["战斗", "战役", "斗争"],
          ["The battle lasted two days.", "She fought a long battle with illness."],
          ["fight", "struggle"], ["peace", "calm"],
          ["combat", "debate"],
          ["战斗/战役：两军对着打的那一场", "斗争：把这场对打用在非武力的事上"],
          "battuere（击打）→ 两边对打的那一场"),
        W("combat", "battuere", "noun", "/ˈkɒmbæt/",
          "com-（相对）+ bat（打）→ 面对面对打",
          "法语 combat ← combattre ← 晚期拉丁语 combattere ← com＋battuere（击打）",
          "fighting between armed forces; to try to stop something bad",
          "the two standing face to face, each blow met by another – 两人面对面站定，一下换一下",
          "两人正面站着，拳头一来一回，没人侧身躲开",
          ["战斗", "搏斗", "对抗"],
          ["He was killed in combat.", "New laws combat pollution."],
          ["fight", "resist"], ["surrender"],
          ["battle", "debate"],
          ["战斗/搏斗：面对面对打", "对抗：把这股对打之力用在抑制某事上"],
          "com-（相对）+ bat（打）→ 面对面对打"),
        W("debate", "battuere", "noun", "/dɪˈbeɪt/",
          "de-（往下）+ bate（打）→ 用话往下打 → 辩论",
          "古法语 debatre（争辩）← de＋batre ← 晚期拉丁语 battuere（击打）",
          "a formal discussion where opposing views are argued",
          "blows traded in words instead of fists – 打的是话，不是拳头",
          "两人隔着讲台一句接一句往回顶，谁也不肯松口",
          ["辩论", "争论", "讨论"],
          ["The debate ran for three hours.", "They debated the new policy."],
          ["argue", "discuss"], ["agree"],
          ["battle", "combat"],
          ["辩论/争论：用话一句接一句地对打", "讨论：同一动作缓和下来，只交换看法"],
          "de-（往下）+ bate（打）→ 用话往下打"),
    ],
})

# ---------- canalis（管、芦管）----------
families.append({
    "root": {
        "id": "canalis", "root": "canalis", "variants": ["canal", "chann", "cann"],
        "origin": "拉丁语 canalis（水槽、管道）← canna（芦苇、管）← 希腊语 kanna；"
                  "芦苇中空成管，故引申为凡中空可通之物",
        "core_concept": "a hollow tube that something runs through / 一根中空的管，东西顺着它走",
        "core_image": "一截芦苇折断，里头是空的，水一倒就顺着流出去",
        "english_definition": "reed, pipe, channel",
    },
    "concept": {
        "id": "concept-canalis-tube", "concept": "a hollow tube that something runs through",
        "chinese": "中空可通之管", "core_image": "芦苇折断，里头是空的，水一倒就顺着流出去",
        "root_ids": ["canalis"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("canal", "canalis", "noun", "/kəˈnæl/",
          "canalis（水槽）→ 人工挖出让水通行的那条道",
          "拉丁语 canalis（水槽、管道）← canna（芦管）",
          "a long channel dug for boats or for carrying water",
          "the trench cut so water has one path and no other – 挖出来只许水走这一条的沟",
          "两岸砌得笔直，水面一路平着延到看不见的地方",
          ["运河", "沟渠", "管道"],
          ["The canal links two rivers.", "Boats pass through the canal daily."],
          ["channel", "path"], [],
          ["channel", "cannon"],
          ["运河/沟渠：挖出让水通行的那条道", "管道：体内同样中空可通的那种道"],
          "canalis（水槽）→ 挖出让水通行的那条道"),
        W("channel", "canalis", "noun", "/ˈtʃænl/",
          "canalis（管道）经古法语 chanel → 水流经过的那条道；引申为传递的路子",
          "古法语 chanel ← 拉丁语 canalis（水槽、管道）",
          "a passage water flows along; a band for broadcasting; a way of doing something",
          "the groove that decides where the flow may go – 决定水往哪儿走的那道槽",
          "石板上凿出一道浅槽，水只能顺着这道往下淌",
          ["海峡", "频道", "途径"],
          ["The Channel separates England and France.", "Change to another channel."],
          ["route", "path"], [],
          ["canal", "cannon"],
          ["海峡：两地之间供水通行的那条道", "频道：信号顺着走的那条道", "途径：办事所走的那条道"],
          "canalis（管道）→ 决定流向的那道槽"),
        W("cannon", "canalis", "noun", "/ˈkænən/",
          "canna（管）+ -one（大）→ 一根大管子 → 火炮",
          "法语 canon ← 意大利语 cannone（大管）← canna（芦管）← 拉丁语",
          "a large heavy gun that fires solid balls",
          "the oversized tube that sends its load out one end – 一根粗大的管，装的东西从一头轰出去",
          "铜管架在木架上，粗到能塞进拳头，一头对着城墙",
          ["大炮", "火炮"],
          ["The cannon fired at dawn.", "Old cannons line the fort wall."],
          ["gun", "weapon"], [],
          ["canal", "channel"],
          ["大炮/火炮：一根粗大的管，装的东西从一头轰出去"],
          "canna（管）+ -one（大）→ 一根大管子"),
    ],
})

# ---------- caput（头）----------
families.append({
    "root": {
        "id": "caput", "root": "caput", "variants": ["chief", "chef", "cap", "cabb"],
        "origin": "拉丁语 caput（头、首要之处）；经古法语 chief 一支入英语，"
                  "又经晚期拉丁语 capitale（首要财产）派出 cattle",
        "core_concept": "the head, hence whatever stands at the top / 头，引申为居首的那一个",
        "core_image": "一群人里那个头往前一伸，别人的目光跟着转过去",
        "english_definition": "head, chief thing",
    },
    "concept": {
        "id": "concept-caput-head", "concept": "the head, hence whatever stands at the top",
        "chinese": "居首之处", "core_image": "一群人里那个头往前一伸，别人的目光跟着转过去",
        "root_ids": ["caput"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("chief", "caput", "noun", "/tʃiːf/",
          "caput（头）经古法语 chief → 一群人里居首的那个",
          "古法语 chief（头、首领）← 拉丁语 caput（头）",
          "the leader of a group; most important",
          "the one the others look to before acting – 别人动手前先看的那一个",
          "帐篷里众人说着话，一齐朝上座那人望过去",
          ["首领", "主要的", "首席的"],
          ["The chief gave the order.", "That is our chief concern."],
          ["leader", "principal"], ["subordinate"],
          ["chef", "cattle"],
          ["首领：一群人里居首的那个", "主要的/首席的：诸事里排在头位的"],
          "caput（头）→ 一群人里居首的那个"),
        W("chef", "caput", "noun", "/ʃef/",
          "chief（首领）的法语后期形 → 厨房里居首的那个 → 主厨",
          "法语 chef（de cuisine，厨房之长）← 古法语 chief ← 拉丁语 caput（头）",
          "a professional cook, especially the one in charge of a kitchen",
          "the one whose word settles what leaves the kitchen – 菜出不出得了门，由他一句话定",
          "灶台后那人一抬手，几个帮手同时停下等着听",
          ["主厨", "厨师长"],
          ["The chef prepared a special menu.", "She trained as a chef in Paris."],
          ["cook", "baker"], [],
          ["chief", "cattle"],
          ["主厨/厨师长：厨房里居首、说话作数的那个"],
          "chief（首领）法语后期形 → 厨房之长"),
        W("cattle", "caput", "noun", "/ˈkætl/",
          "capitale（首要财产）→ 旧时最值钱的家产就是牛 → 牛群",
          "盎格鲁法语 catel（财产）← 晚期拉丁语 capitale（首要财产）← caput（头）；"
          "英语 capital（资本）同出此支，牛作旧时首要家产故得此名",
          "cows and bulls kept on a farm",
          "what used to count as a household's chief wealth, counted by the head – 旧时算作一家首要财产、按头来数的那些",
          "栏里十几头挤在一处，主人清早数一遍才放心",
          ["牛", "牲畜"],
          ["The cattle grazed by the river.", "He keeps forty head of cattle."],
          ["cattle", "animal"], [],
          ["chief", "chef"],
          ["牛/牲畜：旧时算作首要家产、按头计数的那些"],
          "capitale（首要财产）→ 旧时最值钱的家产即牛"),
    ],
})

# ---------- citare（召唤）----------
families.append({
    "root": {
        "id": "citare", "root": "citare", "variants": ["cit", "cite"],
        "origin": "拉丁语 citare（唤来、催动）是 ciere（使动起来）的反复体；"
                  "本义是把人或话「叫到面前来」",
        "core_concept": "calling a thing up so it stands before you / 把某样东西唤到眼前来",
        "core_image": "一声招呼，本来不在场的那个被叫到跟前站着",
        "english_definition": "to summon, set in motion",
    },
    "concept": {
        "id": "concept-citare-summon", "concept": "calling a thing up so it stands before you",
        "chinese": "唤到眼前", "core_image": "一声招呼，本来不在场的那个被叫到跟前站着",
        "root_ids": ["citare"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("cite", "citare", "verb", "/saɪt/",
          "citare（唤来）→ 把别人的话唤到眼前作凭据 → 引用",
          "拉丁语 citare（唤来、传唤）← ciere（使动起来）",
          "to quote a source as evidence; to summon to court",
          "calling another's words up to stand as witness – 把别人说过的话叫到跟前当证人",
          "他翻开书按住那一行，念出来给在座的人听",
          ["引用", "引证", "传唤"],
          ["She cited three studies.", "He was cited to appear in court."],
          ["quote", "summon"], [],
          ["excite", "recite"],
          ["引用/引证：把别人的话唤到眼前作凭据", "传唤：把人唤到庭前"],
          "citare（唤来）→ 把话唤到眼前作凭据"),
        W("excite", "citare", "verb", "/ɪkˈsaɪt/",
          "ex-（出来）+ cite（唤动）→ 把里头的劲唤出来 → 使激动",
          "拉丁语 excitare（唤起、激发）← ex＋citare（唤动）",
          "to make someone feel eager or stirred up",
          "calling out the energy that was sitting still inside – 把本来静着的那股劲唤出来",
          "话音刚落，屋里人一下都坐直了，声音也高了",
          ["使激动", "激起", "刺激"],
          ["The news excited everyone.", "Loud noise excites the dog."],
          ["stir", "arouse"], ["calm", "quiet"],
          ["cite", "recite"],
          ["使激动/激起：把静着的劲唤出来", "刺激：同一动作用在感官或神经上"],
          "ex-（出来）+ cite（唤动）→ 把里头的劲唤出来"),
        W("recite", "citare", "verb", "/rɪˈsaɪt/",
          "re-（再）+ cite（唤来）→ 把记住的话再唤出来 → 背诵",
          "拉丁语 recitare（朗读、背诵）← re＋citare（唤来）",
          "to say aloud something learned by heart",
          "calling the words up again from memory, out loud – 把记下的话再唤出来，说给人听",
          "他闭着眼把整段说完，一个字没停顿",
          ["背诵", "朗诵", "列举"],
          ["She recited the poem from memory.", "He recited the whole list."],
          ["repeat", "read"], [],
          ["cite", "excite"],
          ["背诵/朗诵：把记下的话再唤出来说给人听", "列举：把各项一件件唤出来点过"],
          "re-（再）+ cite（唤来）→ 把记住的话再唤出来"),
    ],
})

# ---------- klinein（倾斜）----------
families.append({
    "root": {
        "id": "klinein", "root": "klinein", "variants": ["clim", "clin"],
        "origin": "希腊语 klinein（使倾斜、斜靠）；klima（地带，本指日照斜角）、"
                  "klimax（梯子，一级级斜上去）、klinē（卧床，斜靠之处）皆由此出",
        "core_concept": "leaning at a slant, and what follows from the tilt / 斜着倾靠，以及这个斜度带来的结果",
        "core_image": "一块板一头垫高，东西顺着那道斜面往下滑",
        "english_definition": "to lean, slant",
    },
    "concept": {
        "id": "concept-klinein-slant", "concept": "leaning at a slant, and what follows from the tilt",
        "chinese": "倾斜之势", "core_image": "板子一头垫高，东西顺着那道斜面往下滑",
        "root_ids": ["klinein"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("climate", "klinein", "noun", "/ˈklaɪmət/",
          "klima（地带）← klinein（倾斜）→ 日照斜角不同分出的地带 → 一地长年的天候",
          "晚期拉丁语 clima（地带）← 希腊语 klima（倾斜、地带）← klinein（倾斜）；"
          "古人按日照入射的斜角划分地带，故此词本指「斜度」",
          "the usual weather conditions of an area over many years",
          "what the sun's slant onto one stretch of ground settles into over years – 日头斜照一地，年复一年定下来的那副样子",
          "同一片地上，年年都是那几个月潮、那几个月干",
          ["气候", "风气"],
          ["The climate here is mild.", "There is a climate of distrust."],
          ["weather", "atmosphere"], [],
          ["climax", "clinic"],
          ["气候：日照斜度定下的、一地长年的天候", "风气：一处长期形成的那种氛围"],
          "klima（斜度、地带）← klinein（倾斜）→ 长年天候"),
        W("climax", "klinein", "noun", "/ˈklaɪmæks/",
          "klimax（梯子）← klinein（斜靠）→ 一级级斜上去的顶端 → 高潮",
          "希腊语 klimax（梯子）← klinein（斜靠、倾斜）",
          "the most intense or important point of something",
          "the last rung of a ladder that leans up and stops – 斜靠上去的梯子，最后那一级",
          "一级一级往上，到最上面那级再没有了，人就停在那儿",
          ["高潮", "顶点"],
          ["The film builds to a climax.", "Her career reached its climax."],
          ["peak", "top"], ["low"],
          ["climate", "clinic"],
          ["高潮/顶点：斜梯一级级上去、最后那一级"],
          "klimax（梯子）← klinein（斜靠）→ 最后那一级"),
        W("clinic", "klinein", "noun", "/ˈklɪnɪk/",
          "klinē（卧床）← klinein（斜靠）→ 在床边诊治 → 诊所",
          "法语 clinique ← 希腊语 klinikē（床边医术）← klinē（卧床）← klinein（斜靠）",
          "a place where people go for medical treatment or advice",
          "the room built around the bed a patient leans back on – 围着病人斜靠的那张床设起来的屋",
          "一排床挨墙摆着，穿白衣的人挨床看过去",
          ["诊所", "门诊"],
          ["The clinic opens at eight.", "She works at a dental clinic."],
          ["surgery", "ward"], [],
          ["climate", "climax"],
          ["诊所/门诊：围着病人斜靠的床设起来的诊治之处"],
          "klinē（卧床）← klinein（斜靠）→ 床边诊治之处"),
    ],
})

# ---------- bulla（铅封、圆泡）----------
families.append({
    "root": {
        "id": "bulla", "root": "bulla", "variants": ["bull", "boul", "bowl"],
        "origin": "拉丁语 bulla（水泡、圆凸的铅封）；封在文书上的铅印是圆的，"
                  "故文书本身也叫 bulla，英语 bulletin 由此；圆球一支经法语 boule 派出 bullet",
        "core_concept": "a small round swelling, and what is sealed or shaped by it / 一个圆凸的小物，及由它封定或成形之物",
        "core_image": "一枚圆铅印按在纸角上，凸起来一小块",
        "english_definition": "bubble, round seal",
    },
    "concept": {
        "id": "concept-bulla-round-seal", "concept": "a small round swelling, and what it seals",
        "chinese": "圆凸小物", "core_image": "一枚圆铅印按在纸角上，凸起来一小块",
        "root_ids": ["bulla"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("bulletin", "bulla", "noun", "/ˈbʊlətɪn/",
          "bulla（铅封文书）→ bullettino（小文书）→ 简短公告",
          "法语 bulletin ← 意大利语 bullettino（小文告）← bulla（盖铅封的文书）← 拉丁语",
          "a short official statement of news",
          "the sealed slip put up so all may read the same words – 盖了印贴出来、让众人读到同一句话的那张",
          "墙上钉着一张短短的纸，底下按了印，路过的人都停下看",
          ["公告", "简报", "新闻快报"],
          ["A bulletin was issued at noon.", "She reads the news bulletin."],
          ["notice", "announcement"], [],
          ["bullet", "bowling"],
          ["公告/简报：盖印贴出、让众人读到的那张短文", "新闻快报：同样简短、随时发出的那种"],
          "bulla（铅封文书）→ 简短公告"),
        W("bullet", "bulla", "noun", "/ˈbʊlɪt/",
          "boule（球）+ -ette（小）→ 小圆球 → 枪弹",
          "法语 boulette（小球）← boule（球）← 拉丁语 bulla（圆泡）",
          "a small piece of metal fired from a gun",
          "the little round slug that leaves the barrel – 从枪管里出去的那颗小圆粒",
          "掌心里几颗黄铜色的小圆粒，一头是尖的",
          ["子弹", "弹丸"],
          ["The bullet missed by inches.", "He loaded six bullets."],
          ["shot", "ball"], [],
          ["bulletin", "bowling"],
          ["子弹/弹丸：从枪管出去的那颗小圆粒"],
          "boule（球）+ -ette（小）→ 小圆球 → 枪弹"),
        W("bowling", "bulla", "noun", "/ˈbəʊlɪŋ/",
          "boule（球）→ bowl（滚球）+ -ing → 滚球撞瓶的那种玩法",
          "英语 bowling，来自 bowl（滚球）← 法语 boule（球）← 拉丁语 bulla（圆泡）",
          "a game in which a heavy ball is rolled to knock down pins",
          "the heavy round thing sent rolling down a lane – 顺着一条道滚出去的那个沉圆物",
          "一个沉沉的圆球贴地滚出去，尽头一排木柱哗啦倒了",
          ["保龄球", "滚球游戏"],
          ["They went bowling on Friday.", "He booked a bowling lane."],
          ["game", "sport"], [],
          ["bullet", "bulletin"],
          ["保龄球/滚球游戏：把沉圆物滚出去撞倒木柱的那种玩法"],
          "boule（球）→ bowl（滚球）→ 滚球撞瓶的玩法"),
    ],
})

# ================= 组装 =================
words = []
roots = []
concepts = []
domain_add = {}
for fam in families:
    r = dict(fam["root"]); r["word_ids"] = []
    roots.append(r)
    concepts.append(fam["concept"])
    domain_add.setdefault(fam["domain"], []).append(r["id"])
    words.extend(fam["words"])

# ---- 生成期自检 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"
assert len({w["id"] for w in words}) == len(words), "词条 id 有重复"
assert len({r["id"] for r in roots}) == len(roots), "词根 id 有重复"
# 词根 id 不得与本批任何单词同名（自环边）
wid = {w["id"] for w in words}
clash = [r["id"] for r in roots if r["id"] in wid]
assert not clash, f"词根 id 与本批单词同名，会产生自环边：{clash}"

OUT.write_text(json.dumps({
    "roots": roots, "concepts": concepts,
    "domain_add": domain_add, "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} 词, {len(roots)} 新词根")
