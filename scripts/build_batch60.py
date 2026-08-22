#!/usr/bin/env python3
"""Generate batch60: 6 个新词根 18 词 + 11 个补词，共 29 词。

新根（各族在考研词表内均有 3 个以上成员）：
  colere（耕作、照管）  colony / colonial / culture
  creare（使生出）      create / creative / creature
  crux（十字架）        cross / crucial / cruise
  dare（给出）          data / database / date
  camera（拱顶小室）    camera / chamber / comrade
  damnum（损失）        damage / damn / condemn

补进已建模根：
  sta（stare 站立）  contrast / cost / costly  —— 子代理原报作新根 stare，
                     但 sta 的 origin 就写「拉丁语 stare」，是同一个根
  cep（capere）      cable / deceit
  cadere（落下）     decay
  caput（头）        cabbage
  consulere（商议）  counsel
  crescere（生长）   crew
  habere（持有）     debt
  legere（拣选、读） coil

【dare 与已有两根的关系，在词根条目里写明】
库中已有 edere-publish（ex＋dare 交出、发布）与 tradere（trans＋dare 交付），
两者都是含 dare 的复合动词，各自作根建模在先。本批新建的 dare 是那个被复合的
本体（datum「所给之物」直接由它出），三者同源而分支不同，故并立。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期。
末尾断言词根 id 不得与本批任何单词同名（自环边，已踩过四次）。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch60.json"


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

# ---------- colere（耕作、照管）----------
families.append({
    "root": {
        "id": "colere", "root": "colere", "variants": ["col", "cult", "colon"],
        "origin": "拉丁语 colere（耕作、住下来照管），过去分词 cultus；"
                  "colonus 是「垦地定居的人」，cultura 是「照管出来的东西」",
        "core_concept": "settling on ground and tending it until it yields / 在一处住下、照管到它长出东西",
        "core_image": "一块生地被人年年翻整，几季之后垄上长出成片的苗",
        "english_definition": "to till, tend, dwell",
    },
    "concept": {
        "id": "concept-colere-tend", "concept": "settling on ground and tending it until it yields",
        "chinese": "垦地照管", "core_image": "生地被人年年翻整，几季后垄上长出成片的苗",
        "root_ids": ["colere"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("colony", "colere", "noun", "/ˈkɒləni/",
          "colonus（垦地定居者）+ -y → 一群人迁去垦住的那片地方",
          "拉丁语 colonia（垦殖地）← colonus（垦地定居的人）← colere（耕作、住下）",
          "a country or area controlled by another; a group of the same kind living together",
          "ground a group moved onto and settled, still answering to where they came from – 一群人迁去住下、却仍听原处号令的那片地",
          "船靠岸后那批人就地搭屋开垦，账目还往老家报",
          ["殖民地", "聚居地", "群体"],
          ["The colony gained independence in 1960.", "A colony of ants lives under the step."],
          ["settlement", "territory"], [],
          ["colonial", "culture"],
          ["殖民地：迁去垦住、仍受原处管辖的那片地", "聚居地/群体：同类生物聚在一处住下的那一片"],
          "colonus（垦地定居者）→ 一群人迁去垦住的地方"),
        W("colonial", "colere", "adjective", "/kəˈləʊniəl/",
          "colony（垦殖地）+ -al（…的）→ 属于殖民地那一套的",
          "英语 colonial，来自 colony ← 拉丁语 colonia ← colere",
          "relating to a colony or to the period of colonial rule",
          "belonging to the arrangement where one land is worked for another – 属于「一地被另一地经营」那套安排",
          "旧账本上写着每季运回去多少，签的是本地人的名",
          ["殖民的", "殖民地的"],
          ["The building dates from colonial times.", "They opposed colonial rule."],
          ["imperial", "overseas"], [],
          ["colony", "culture"],
          ["殖民的/殖民地的：属于「一地被另一地经营」那套安排"],
          "colony（垦殖地）+ -al → 属于那套安排的"),
        W("culture", "colere", "noun", "/ˈkʌltʃə(r)/",
          "cult（照管）+ -ure → 照管出来的那一片 → 耕作，引申为世代养出的风习",
          "拉丁语 cultura（耕作、照管）← colere（耕作、住下照管）",
          "the customs and arts of a society; the growing of plants or cells",
          "what long tending finally brings up out of the ground – 长年照管之后，从地里长出来的那一片",
          "同一块地翻了几十年，长出来的东西跟别处就是不一样",
          ["文化", "培养", "栽培"],
          ["Each region has its own culture.", "They grew a culture of bacteria."],
          ["civilization", "custom"], [],
          ["colony", "colonial"],
          ["文化：世代照管养出来的那套风习", "培养/栽培：照管使之长起来这个动作本身"],
          "cult（照管）+ -ure → 长年照管长出来的那一片"),
    ],
})

# ---------- creare（使生出）----------
families.append({
    "root": {
        "id": "creare", "root": "creare", "variants": ["creat", "creas", "cre"],
        "origin": "拉丁语 creare（使生出、造出），与 crescere（生长）同源而分工："
                  "creare 是「使之生出」，crescere 是「自己长大」",
        "core_concept": "bringing into being what was not there / 把原先没有的弄出来",
        "core_image": "空空的台面上，手一撤，那件东西就摆在那儿了",
        "english_definition": "to bring forth, produce",
    },
    "concept": {
        "id": "concept-creare-bring-forth", "concept": "bringing into being what was not there",
        "chinese": "使之生出", "core_image": "空台面上手一撤，那件东西就摆在那儿了",
        "root_ids": ["creare"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("create", "creare", "verb", "/kriˈeɪt/",
          "creare（使生出）→ 把原先没有的做出来",
          "拉丁语 creare（造出、使生出）的过去分词 creatus",
          "to make something exist that did not exist before",
          "the moment a thing first stands where nothing stood – 原先空着的那处，头一回有了东西",
          "纸上本来什么都没有，笔一落，一个形状就在那儿了",
          ["创造", "创作", "造成"],
          ["She created a new design.", "The storm created chaos."],
          ["make", "produce"], ["destroy"],
          ["creative", "creature"],
          ["创造/创作：把原先没有的做出来", "造成：某事使一个局面生出来"],
          "creare（使生出）→ 把原先没有的做出来"),
        W("creative", "creare", "adjective", "/kriˈeɪtɪv/",
          "create（使生出）+ -ive → 能把没有的弄出来的",
          "英语 creative，来自 create ← 拉丁语 creare",
          "able to produce new and original things",
          "of the kind that turns an empty surface into something – 属于「能把空处变出东西」那一类",
          "同样一堆边角料，有人摆着摆着就成了个能用的东西",
          ["有创造力的", "创造性的"],
          ["She has a creative mind.", "It was a creative solution."],
          ["original", "clever"], ["dull"],
          ["create", "creature"],
          ["有创造力的/创造性的：能把原先没有的弄出来的那种"],
          "create（使生出）+ -ive → 能把没有的弄出来"),
        W("creature", "creare", "noun", "/ˈkriːtʃə(r)/",
          "create（使生出）+ -ure → 被造出来的那个 → 生物",
          "古法语 creature ← 晚期拉丁语 creatura（被造之物）← creare（造出）",
          "any living thing that can move, especially an animal",
          "whatever was brought into being and now moves on its own – 被弄出来、如今自己会动的那个",
          "石头下面那个小东西被光一照，八条腿一齐动起来",
          ["生物", "动物", "家伙"],
          ["Strange creatures live in the deep sea.", "The poor creature was shivering."],
          ["animal", "being"], [],
          ["create", "creative"],
          ["生物/动物：被造出来、自己会动的那个", "家伙：带感情色彩地指某个人"],
          "create（使生出）+ -ure → 被造出来的那个"),
    ],
})

# ---------- crux（十字架）----------
families.append({
    "root": {
        "id": "crux", "root": "crux", "variants": ["cruc", "cross", "crus"],
        "origin": "拉丁语 crux（属格 crucis：十字架、交叉的木架）；"
                  "两根木条交叉的那个点，是这一族的共同意象",
        "core_concept": "two lines meeting at one crossing point / 两条线交在一点上",
        "core_image": "两根木条叠成十字，钉在交叉那一点上",
        "english_definition": "cross, crossing point",
    },
    "concept": {
        "id": "concept-crux-crossing", "concept": "two lines meeting at one crossing point",
        "chinese": "交叉之点", "core_image": "两根木条叠成十字，钉在交叉那一点上",
        "root_ids": ["crux"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("cross", "crux", "verb", "/krɒs/",
          "crux（十字）→ 从一边横过到另一边，路线与原线相交",
          "古英语 cros ← 古爱尔兰语 cros ← 拉丁语 crux（十字架）",
          "to go from one side to the other; a mark or shape of two lines",
          "the path that cuts through another instead of running alongside – 不顺着走，而是横切过去的那条线",
          "他从这边人行道横切过去，走线正好压过车道",
          ["穿过", "十字", "交叉"],
          ["Look both ways before you cross.", "Mark your answer with a cross."],
          ["span", "pass"], [],
          ["crucial", "cruise"],
          ["穿过：横切过另一条线", "十字/交叉：两条线相交留下的那个形"],
          "crux（十字）→ 横切过去、与原线相交"),
        W("crucial", "crux", "adjective", "/ˈkruːʃl/",
          "cruc（十字路口）+ -ial → 处在岔路交点上的 → 决定性的",
          "拉丁语 crucialis（十字形的）← crux（十字架）；"
          "十字路口须择一路走，故引申为「决定成败的那一处」",
          "extremely important because it decides what follows",
          "the fork where the road splits and one must be chosen – 路在此分岔，非选一条不可的那一点",
          "路到这儿分成两条，选哪条后头就全不一样了",
          ["决定性的", "关键的", "至关重要的"],
          ["This is a crucial decision.", "Timing was crucial to the plan."],
          ["critical", "decisive"], ["trivial"],
          ["cross", "cruise"],
          ["决定性的/关键的：处在岔路交点、选择定成败的那一处"],
          "cruc（十字路口）+ -ial → 岔路交点、择一定成败"),
        W("cruise", "crux", "verb", "/kruːz/",
          "crux（十字）→ 荷兰语 kruisen（打十字、来回横渡）→ 巡航",
          "荷兰语 kruisen（十字形来回航行）← kruis（十字）← 拉丁语 crux",
          "to sail or drive at a steady pace without hurrying",
          "going back and forth across a stretch rather than straight to one end – 在一片水面上来回横着走，不直奔一头",
          "船不赶路，在同一片海面上来回划着走，速度一直没变",
          ["巡航", "巡游", "缓行"],
          ["The ship cruised along the coast.", "We cruised at sixty miles an hour."],
          ["sail", "glide"], [],
          ["cross", "crucial"],
          ["巡航/巡游：来回横着走而不直奔一头", "缓行：保持一个不赶的速度走"],
          "crux（十字）→ kruisen（来回横渡）→ 巡航"),
    ],
})

# ---------- dare（给出）----------
families.append({
    "root": {
        "id": "dare", "root": "dare", "variants": ["dat", "dos", "don"],
        "origin": "拉丁语 dare（给），过去分词 datus，中性 datum 表「所给之物」。"
                  "库中已有的 edere-publish（ex＋dare 交出）与 tradere（trans＋dare 交付）"
                  "是含 dare 的复合动词，各自建模在先；本根是被复合的本体，三者同源分支不同",
        "core_concept": "putting a thing into another's hands / 把东西交到别人手上",
        "core_image": "手一伸，东西从这边转到那边的手里",
        "english_definition": "to give",
    },
    "concept": {
        "id": "concept-dare-give", "concept": "putting a thing into another's hands",
        "chinese": "交到手上", "core_image": "手一伸，东西从这边转到那边的手里",
        "root_ids": ["dare"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("data", "dare", "noun", "/ˈdeɪtə/",
          "datum（所给之物）的复数 → 摆出来供人处理的那些事实",
          "拉丁语 data（datum 的复数，「所给之物」）← dare（给）",
          "facts and figures collected for reference or analysis",
          "the figures handed over for someone else to work on – 交到手上、让人拿去处理的那些数字",
          "一叠表格递过来，上面全是记好的数字，等着人去算",
          ["数据", "资料"],
          ["The data shows a clear trend.", "We collected data for six months."],
          ["record", "information"], [],
          ["database", "date"],
          ["数据/资料：交到手上供人处理的那些事实与数字"],
          "datum（所给之物）的复数 → 供人处理的事实"),
        W("database", "dare", "noun", "/ˈdeɪtəbeɪs/",
          "data（所给之物）+ base（底座）→ 把数据搁在一处的那个底盘",
          "英语复合词 data＋base；data ← 拉丁语 dare（给）",
          "an organized store of information held in a computer",
          "the one place all the handed-over figures are kept – 把交上来的数字全搁在一处的那个地方",
          "所有表格最后都归到同一个柜里，查哪一份都能翻出来",
          ["数据库"],
          ["The database holds ten million records.", "She queried the customer database."],
          ["store", "record"], [],
          ["data", "date"],
          ["数据库：把交上来的数据统一搁在一处的那个地方"],
          "data（所给之物）+ base（底座）→ 存放数据的底盘"),
        W("date", "dare", "noun", "/deɪt/",
          "datum（所给之物）→ 旧文书末尾写「datum Romae…（给于罗马某日）」→ 日期",
          "古法语 date ← 晚期拉丁语 data（文书上标注的签发日）← dare（给）；"
          "旧时公文末尾以 datum（给于某地某日）起句，遂以此指日期",
          "the day of the month or year; an arrangement to meet",
          "the day written at the foot of a paper to fix when it was handed over – 写在文书末尾、标明何日交出的那一天",
          "信纸最下面一行写着地点和那一天，字迹比正文小些",
          ["日期", "约会", "枣"],
          ["What is the date today?", "They went on a date last night."],
          ["day", "appointment"], [],
          ["data", "database"],
          ["日期：文书上标明何日交出的那一天", "约会：定好在哪一天见面这件事", "枣：另一支借自希腊 daktulos（指头），与本族无关"],
          "datum（给于某日）→ 文书末尾标注的那一天"),
    ],
})

# ---------- camera（拱顶小室）----------
families.append({
    "root": {
        "id": "kamara", "root": "kamara", "variants": ["camera", "camer", "chamb", "camar"],
        "origin": "希腊语 kamara（拱顶）→ 拉丁语 camera（拱顶的小室）；"
                  "词根 id 取希腊词形 kamara，因 camera 本身是本批要收的单词，作 id 会产生自环边；"
                  "暗箱成像的器械因是「暗室」而得名 camera obscura，遂简称 camera",
        "core_concept": "a small closed room, and what happens inside it / 一间关起来的小屋，及屋里发生的事",
        "core_image": "一间没有窗的小屋，门一关，里外就隔断了",
        "english_definition": "vaulted chamber, small room",
    },
    "concept": {
        "id": "concept-kamara-chamber", "concept": "a small closed room, and what happens inside it",
        "chinese": "关起来的小屋", "core_image": "没有窗的小屋，门一关，里外就隔断了",
        "root_ids": ["kamara"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("camera", "kamara", "noun", "/ˈkæmərə/",
          "camera obscura（暗室）截短 → 靠一间暗室成像的那件器械",
          "拉丁语 camera obscura（暗室）的截短形 ← camera（小室）← 希腊语 kamara（拱顶）",
          "a device for taking photographs or filming",
          "the light-tight box that lets in just one narrow beam – 密不透光的那个盒子，只放一束光进去",
          "盒子四面不透光，只前头留一个小孔，光从那儿进来",
          ["照相机", "摄像机"],
          ["He bought a new camera.", "The camera stopped recording."],
          ["lens", "recorder"], [],
          ["chamber", "comrade"],
          ["照相机/摄像机：靠一间密闭暗室成像的那件器械"],
          "camera obscura（暗室）截短 → 成像的暗箱器械"),
        W("chamber", "kamara", "noun", "/ˈtʃeɪmbə(r)/",
          "camera（小室）经古法语 chambre → 一间围起来的屋，也指枪膛、议院",
          "古法语 chambre ← 拉丁语 camera（拱顶小室）",
          "a room, especially a private or official one; an enclosed space",
          "the space walled off so what is inside stays inside – 围起来、使里头的东西留在里头的那块空间",
          "推开厚门是一间不大的屋，声音在里头闷着传不出去",
          ["房间", "议院", "膛室"],
          ["The judge spoke in his chamber.", "The gun has six chambers."],
          ["room", "compartment"], [],
          ["camera", "comrade"],
          ["房间：围起来的一间屋", "议院：议事者聚在其中的那间", "膛室：枪械里围起来装弹的那格"],
          "camera（小室）→ 围起来的一间屋"),
        W("comrade", "kamara", "noun", "/ˈkɒmreɪd/",
          "camara（小室）→ 同住一室的人 → 同伴、战友",
          "法语 camarade ← 西班牙语 camarada（同室者）← 拉丁语 camera（小室）",
          "a friend or fellow member, especially one sharing hardship",
          "the one who slept in the same small room as you – 跟你睡同一间小屋的那个人",
          "两张床挤在同一间屋里，夜里说话不用抬高声音",
          ["同伴", "战友", "同志"],
          ["He lost two comrades in the war.", "She greeted her old comrades."],
          ["companion", "fellow"], [],
          ["camera", "chamber"],
          ["同伴/战友：同住一室、共过患难的那个人", "同志：以此互称的政治用法"],
          "camara（小室）→ 同住一室的人"),
    ],
})

# ---------- damnum（损失）----------
families.append({
    "root": {
        "id": "damnum", "root": "damnum", "variants": ["damn", "damag", "demn"],
        "origin": "拉丁语 damnum（损失、罚金），动词 damnare 表「判罚、使受损」；"
                  "经古法语 damage、damner 分支入英语",
        "core_concept": "loss inflicted, and the judgement that inflicts it / 加在人身上的损失，及判它的那道裁断",
        "core_image": "账上被划掉一笔，那笔就再也回不来了",
        "english_definition": "loss, penalty",
    },
    "concept": {
        "id": "concept-damnum-loss", "concept": "loss inflicted, and the judgement that inflicts it",
        "chinese": "加于人的损失", "core_image": "账上被划掉一笔，那笔再也回不来了",
        "root_ids": ["damnum"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("damage", "damnum", "noun", "/ˈdæmɪdʒ/",
          "damnum（损失）+ -age → 受损这件事，及损到什么程度",
          "古法语 damage（损失）← 拉丁语 damnum（损失）",
          "physical harm that makes something less useful or valuable",
          "what is gone from a thing and will not come back – 从一件东西上少掉、再补不回的那部分",
          "车头凹进去一块，钣金敲平了，那道折痕还留着",
          ["损害", "损坏", "损失"],
          ["The storm caused serious damage.", "Water damaged the floor."],
          ["harm", "injury"], ["repair"],
          ["damn", "condemn"],
          ["损害/损坏：从物上少掉、补不回的那部分", "损失：算总账时少掉的那一笔"],
          "damnum（损失）+ -age → 受损及其程度"),
        W("damn", "damnum", "verb", "/dæm/",
          "damnare（判罚）→ 判某人该受损失 → 谴责、诅咒",
          "古法语 damner ← 拉丁语 damnare（判罚、使受损）← damnum（损失）",
          "to condemn strongly; used as a mild swear word",
          "handing down the verdict that a thing is to be written off – 一句话判定它就此作废",
          "他把那份稿子往桌上一推，一句话就断了它的生路",
          ["谴责", "诅咒", "该死的"],
          ["Critics damned the film.", "He damned his own bad luck."],
          ["condemn", "curse"], ["praise", "bless"],
          ["damage", "condemn"],
          ["谴责：判定其该受损、就此作废", "诅咒/该死的：把这道判词当骂语用"],
          "damnare（判罚）→ 判它该受损、就此作废"),
        W("condemn", "damnum", "verb", "/kənˈdem/",
          "con-（加强）+ demn（判罚）→ 正式判定其有罪或不堪用",
          "拉丁语 condemnare（定罪）← con＋damnare（判罚）← damnum（损失）",
          "to express strong disapproval; to sentence; to declare unfit for use",
          "the formal word that settles a thing's fate against it – 一纸判词把它的去向定死",
          "楼门上钉了一张告示，写明此后不许住人",
          ["谴责", "判罪", "宣告不适用"],
          ["They condemned the attack.", "The building was condemned last year."],
          ["denounce", "sentence"], ["approve"],
          ["damn", "damage"],
          ["谴责：正式表明不认可", "判罪：判定其有罪", "宣告不适用：判定房屋器物不堪再用"],
          "con-（加强）+ demn（判罚）→ 正式判定其不堪"),
    ],
})

# ================= 补进已建模词根 =================
additions = [
    # sta（stare 站立）—— 子代理原报作新根 stare，实为同一个根
    W("cost", "sta", "noun", "/kɒst/",
      "con-（一起）+ sta（立）→ constare（合起来立住、值多少）→ 代价",
      "古法语 coster ← 拉丁语 constare（值、花费）← com＋stare（站立）",
      "the amount of money needed to buy or do something",
      "what has to be put up before a thing will stand – 要它立得住，先得垫上去的那份",
      "柜台上报出一个数，那数付了东西才归你",
      ["费用", "代价", "花费"],
      ["The cost of living keeps rising.", "It cost more than we expected."],
      ["price", "expense"], ["profit"],
      ["costly", "state"],
      ["费用/花费：换取一物须付出的那个数", "代价：不止钱，泛指须付出的那一份"],
      "con-（一起）+ sta（立）→ 要它立住须垫上的那份"),
    W("costly", "sta", "adjective", "/ˈkɒstli/",
      "cost（代价）+ -ly（…样的）→ 代价大的",
      "英语 costly，来自 cost ← 拉丁语 constare ← com＋stare",
      "expensive; causing much loss or harm",
      "the kind that takes a great deal to keep standing – 要撑住它得垫进去很多的那种",
      "那间铺子每月要垫进去的钱越来越多，最后关了门",
      ["昂贵的", "代价高的"],
      ["It was a costly mistake.", "Repairs proved too costly."],
      ["expensive", "dear"], ["cheap"],
      ["cost", "state"],
      ["昂贵的/代价高的：要撑住它得垫进去很多的那种"],
      "cost（代价）+ -ly → 代价大的"),
    W("contrast", "sta", "noun", "/ˈkɒntrɑːst/",
      "contra-（相对）+ sta（立）→ 两者对立而站 → 对比出的差别",
      "法语 contraste ← 意大利语 contrastare（对立）← 拉丁语 contra＋stare（站立）",
      "a clear difference seen when two things are put side by side",
      "two things stood against each other so the gap shows – 两样对着立住，差别就显出来",
      "深浅两块布并排铺开，挨着一看才知道差多少",
      ["对比", "对照", "反差"],
      ["The contrast between them is striking.", "Her mood contrasts with his."],
      ["difference", "comparison"], ["similarity"],
      ["cost", "state"],
      ["对比/对照：两者对立而站、差别显出来", "反差：那道差别本身的大小"],
      "contra-（相对）+ sta（立）→ 对着立住，差别显出"),
    # cep（capere 抓取）
    W("cable", "cep", "noun", "/ˈkeɪbl/",
      "capulum（套索）← capere（抓取）→ 抓得住东西的粗绳 → 缆",
      "古北法语 cable ← 晚期拉丁语 capulum（套索）← 拉丁语 capere（抓取）",
      "a thick strong rope or bundle of wires",
      "the rope thick enough to hold whatever it is put around – 粗到能箍住东西不放的那种绳",
      "手腕粗的一股绞在一起，绕上桩子拽不动",
      ["缆绳", "电缆", "电报"],
      ["The cable snapped under strain.", "They laid a cable under the sea."],
      ["rope", "wire"], [],
      ["capture", "catch"],
      ["缆绳：粗到能箍住东西的那种绳", "电缆：同样成股的导线", "电报：靠海底电缆发的那种讯"],
      "capulum（套索）← capere（抓取）→ 抓得住的粗绳"),
    W("deceit", "cep", "noun", "/dɪˈsiːt/",
      "de-（脱开正道）+ ceit（接住）→ 让人接住假的 → 欺骗",
      "古法语 deceite ← 拉丁语 decipere（诱骗）← de＋capere（抓取）",
      "the act of making someone believe what is not true",
      "handing over the false one so it is taken as real – 递过去一件假的，让人当真接下",
      "他把掺过的那壶推到客人手边，自己那壶另放着",
      ["欺骗", "欺诈", "谎言"],
      ["She was hurt by his deceit.", "The scheme was built on deceit."],
      ["fraud", "lie"], ["honesty"],
      ["deceive", "receive"],
      ["欺骗/欺诈：递假的让人当真接下", "谎言：用来骗人接下的那句话"],
      "de-（脱开正道）+ ceit（接住）→ 让人接住假的"),
    # cadere（落下）
    W("decay", "cadere", "verb", "/dɪˈkeɪ/",
      "de-（往下）+ cay（落）→ 一路往下落 → 衰败、腐烂",
      "古北法语 decair ← 通俗拉丁语 decadere（落下去）← de＋cadere（落下）",
      "to become gradually worse or to rot away",
      "the slow slide downward that nothing stops – 一路往下掉，没什么拦住它",
      "木桩底下一年年发软，用手一掰就掉渣",
      ["腐烂", "衰败", "衰退"],
      ["The wood began to decay.", "The empire slowly decayed."],
      ["rot", "decline"], ["thrive"],
      ["accident", "chance"],
      ["腐烂：一路往下坏到掉渣", "衰败/衰退：局面同样一路往下落"],
      "de-（往下）+ cay（落）→ 一路往下落"),
    # caput（头）
    W("cabbage", "caput", "noun", "/ˈkæbɪdʒ/",
      "caboche（大脑袋）← caput（头）→ 长成一个圆头的那种菜",
      "古北法语 caboche（脑袋）← 拉丁语 caput（头）",
      "a round vegetable with thick green or purple leaves",
      "the vegetable that grows into one tight round head – 长成紧紧一个圆球的那种菜",
      "菜地里一颗颗圆球贴地摆着，叶子层层裹得很紧",
      ["卷心菜", "甘蓝"],
      ["She shredded a whole cabbage.", "Cabbage grows well in cool weather."],
      ["plant", "leaf"], [],
      ["chief", "chef"],
      ["卷心菜/甘蓝：叶子裹成紧紧一个圆头的那种菜"],
      "caboche（大脑袋）← caput（头）→ 长成圆头的菜"),
    # consulere（商议）
    W("counsel", "consulere", "noun", "/ˈkaʊnsl/",
      "consulere（商议、求教）→ 商议后给出的那番话 → 建议",
      "古法语 conseil ← 拉丁语 consilium（商议、议事）← consulere（商议、求教）",
      "advice given after careful thought; a lawyer in a case",
      "what is said back after the matter has been talked through – 事情议过一遍之后回给你的那番话",
      "他把来龙去脉听完，沉了一会儿才开口说该怎么办",
      ["建议", "劝告", "律师"],
      ["She sought legal counsel.", "He counselled patience."],
      ["advice", "guidance"], [],
      ["consult", "consultant"],
      ["建议/劝告：议过之后回给你的那番话", "律师：在案中受聘出这番话的人"],
      "consulere（商议）→ 议过之后回给你的话"),
    # crescere（生长）
    W("crew", "crescere", "noun", "/kruː/",
      "crescere（增多）→ crue（增补的人手）→ 一船一机上的那班人",
      "古法语 crue（增补、增援）← creistre ← 拉丁语 crescere（生长、增多）",
      "the people who work on a ship, plane, or team",
      "the hands added until there are enough to work the vessel – 添到够用为止的那班人手",
      "船要开了还差几个人，码头上又叫来两个才凑齐",
      ["船员", "机组", "全体人员"],
      ["The crew worked through the night.", "A film crew arrived at dawn."],
      ["staff", "team"], [],
      ["increase", "decrease"],
      ["船员/机组：添到够用、操作船机的那班人", "全体人员：同一班人的总称"],
      "crescere（增多）→ crue（增补人手）→ 那班人"),
    # habere（持有）
    W("debt", "habere", "noun", "/det/",
      "de-（脱开）+ bt（habere 持有）→ debere（本该有却不在手上）→ 欠款",
      "古法语 dette ← 拉丁语 debitum（所欠之物）← debere（欠）← de＋habere（持有）",
      "money that one owes to another",
      "what should be in your hands but is not, because it is owed – 本该在手上、却因为欠着而不在的那份",
      "账本上写着数目，钱却还在别人那儿",
      ["债务", "欠款", "人情债"],
      ["He paid off his debts.", "The company is deep in debt."],
      ["liability", "loan"], ["credit"],
      ["able", "ability"],
      ["债务/欠款：本该在手上、因欠着而不在的那份", "人情债：同样欠着、须回报的那一份"],
      "de-（脱开）+ habere（持有）→ 本该有却不在手上"),
    # legere（拣选、读）
    W("coil", "legere", "noun", "/kɔɪl/",
      "col-（一起）+ leg（拣拢）→ colligere（收拢）→ 绕成一圈圈收起来",
      "古法语 coillir（收拢）← 拉丁语 colligere（聚集）← com＋legere（拣选、拢起）",
      "a length of rope or wire wound into rings",
      "the rope gathered in on itself, ring lying on ring – 绳往自己身上收拢，一圈压一圈",
      "绳子一圈压一圈盘在甲板上，中间空出一个洞",
      ["线圈", "盘卷", "卷成圈"],
      ["He hung a coil of rope on the hook.", "The snake coiled around the branch."],
      ["loop", "spiral"], [],
      ["collect", "collective"],
      ["线圈/盘卷：绕成一圈圈收拢起来的那束", "卷成圈：把它绕起来这个动作"],
      "col-（一起）+ leg（拣拢）→ 绕成一圈圈收起"),
]

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
words.extend(additions)

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
wid = {w["id"] for w in words}
clash = [r["id"] for r in roots if r["id"] in wid]
assert not clash, f"词根 id 与本批单词同名，会产生自环边：{clash}"

OUT.write_text(json.dumps({
    "roots": roots, "concepts": concepts,
    "domain_add": domain_add, "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} 词（{len(words)-len(additions)} 族词 + "
      f"{len(additions)} 补词）, {len(roots)} 新词根")
