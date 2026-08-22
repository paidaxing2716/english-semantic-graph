#!/usr/bin/env python3
"""Generate batch48: 7 new roots (21 词).

  consuetudo（惯常）  custom / customary / customer
  favere（示好）      favor / favorable / favorite
  pingere（着色）     paint / painter / painting
  experiri（试过）    experience / experiment / experimental
  planus（平）        plan / plane / explanation
  planta（幼苗）      plant / plantation / transplant
  polis（城邦）       political / politician / politics

词根 id 一律取拉丁/希腊词形：custom、paint、plan、plant 这几个词本批就要入库，
若拿 vetted 族名作 id 立刻产生自环边（form/port/flu/press 已踩过三次）。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch48.json"


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

# ---------- consuetudo（惯常）----------
families.append({
    "root": {
        "id": "consuetudo", "root": "consuetudo", "variants": ["custom", "costum"],
        "origin": "拉丁语 consuetudo（惯常、成例），来自 consuescere（习惯于）；"
                  "经古法语 costume 入英语。旧时按成例缴纳的税费即 customs（关税），"
                  "常来照顾生意的人即 customer",
        "core_concept": "the way long repeated until it counts as the way / 做惯了，于是成了该那么做",
        "core_image": "同一条路走了几十年，草都被踩出一道浅沟",
        "english_definition": "habit, usage, established practice",
    },
    "concept": {
        "id": "concept-consuetudo-usage", "concept": "the way long repeated until it counts as the way",
        "chinese": "做惯成例", "core_image": "同一条路走了几十年，草被踩出一道浅沟",
        "root_ids": ["consuetudo"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("custom", "consuetudo", "noun", "/ˈkʌstəm/",
          "consuetudo（惯常）→ 一地长年照做的成例；按成例缴的税即关税一义",
          "古法语 costume，来自拉丁语 consuetudo（惯常）← consuescere（习惯于）",
          "a way of behaving long established in a place; duties paid on imports",
          "what a place has done so long that it now counts as proper – 一地做久了、如今被认作该那么做的事",
          "每年这天各家都摆一样的供品，谁也说不清是从哪辈起的",
          ["习俗", "惯例", "关税"],
          ["It is a local custom to bring flowers.", "The goods were held at customs."],
          ["tradition", "practice"], [],
          ["customary", "customer"],
          ["习俗/惯例：一地长年照做、被认作该如此的事", "关税：旧时按成例向过境货物征收的那笔"],
          "consuetudo（惯常）→ 做久成例；按例缴的税即关税"),
        W("customary", "consuetudo", "adjective", "/ˈkʌstəməri/",
          "custom（成例）+ -ary（…的）→ 照成例来的、素来如此的",
          "拉丁语 consuetudinarius（依惯例的），来自 consuetudo",
          "according to what is usually done",
          "following the groove already worn in – 顺着早被踩出来的那道沟走",
          "他照素来的做法先斟茶再落座，一步没差",
          ["习惯上的", "惯常的"],
          ["It is customary to tip the driver.", "He took his customary seat by the window."],
          ["usual", "traditional"], ["unusual"],
          ["custom", "customer"],
          ["习惯上的/惯常的：顺着早已踩出的那道沟来"],
          "custom（成例）+ -ary → 顺着旧沟、素来如此"),
        W("customer", "consuetudo", "noun", "/ˈkʌstəmə(r)/",
          "custom（惯常照顾）+ -er（人）→ 惯常上门买东西的那个人",
          "英语 customer，来自 custom（惯常光顾）← 拉丁语 consuetudo",
          "a person who buys goods or services from a shop or business",
          "the one who keeps coming back to the same counter – 一趟趟回到同一个柜台的那个人",
          "掌柜一抬头就知道他要哪一样，来的回数太多了",
          ["顾客", "客户"],
          ["The shop has many regular customers.", "A customer complained about the delay."],
          ["client", "buyer"], ["seller"],
          ["custom", "customary"],
          ["顾客/客户：惯常回到同一处买东西的人"],
          "custom（惯常光顾）+ -er → 一趟趟回来的那个人"),
    ],
})

# ---------- favere（示好）----------
families.append({
    "root": {
        "id": "favere", "root": "favere", "variants": ["fav", "favor"],
        "origin": "拉丁语 favere（善待、偏袒、喝彩），名词 favor（好意、青睐）；"
                  "经古法语 favour 入英语",
        "core_concept": "to lean toward one side and wish it well / 心偏向某一边，盼它好",
        "core_image": "看台上手掌全朝着一边拍，另一边冷冷清清",
        "english_definition": "to be kind to, to favour",
    },
    "concept": {
        "id": "concept-favere-lean-toward", "concept": "to lean toward one side and wish it well",
        "chinese": "心向一边", "core_image": "看台上手掌全朝一边拍，另一边冷清",
        "root_ids": ["favere"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("favor", "favere", "noun", "/ˈfeɪvə(r)/",
          "favere（善待、偏袒）→ 给某一边的好意；也指为人做的那件方便事",
          "古法语 favour，来自拉丁语 favor（好意、青睐）← favere",
          "kind approval or support; a kind act done for someone",
          "the good will turned toward one side – 朝某一边送去的那份好意",
          "他把手一挥，众人的掌声全往那一边去了",
          ["恩惠", "赞成", "偏爱"],
          ["Could you do me a favor?", "The plan found favor with the board."],
          ["kindness", "approval"], ["disfavor"],
          ["favorable", "favorite"],
          ["恩惠：为人做的那件方便事", "赞成/偏爱：心朝某一边送去的好意"],
          "favere（善待偏袒）→ 朝某一边送去的好意"),
        W("favorable", "favere", "adjective", "/ˈfeɪvərəbl/",
          "favor（好意）+ -able（可…的）→ 带着好意的、于我有利的",
          "拉丁语 favorabilis（讨喜的、有利的），来自 favor ← favere",
          "showing approval; helpful and likely to bring advantage",
          "with the wind leaning one's own way – 风向偏在自己这一边",
          "风顺着帆往前推，船比预定快了半日",
          ["有利的", "赞同的", "顺利的"],
          ["The weather was favorable for sailing.", "She gave a favorable reply."],
          ["advantageous", "positive"], ["unfavorable"],
          ["favor", "favorite"],
          ["赞同的：带着好意的", "有利的/顺利的：势头偏在自己这一边"],
          "favor（好意）+ -able → 好意所向、势头偏向自己"),
        W("favorite", "favere", "adjective", "/ˈfeɪvərɪt/",
          "favor（偏爱）+ -ite（受…的）→ 得那份偏爱最多的",
          "意大利语 favorito（受宠者），来自 favorire ← 拉丁语 favere",
          "liked more than all others of the same kind",
          "the one the leaning always settles on – 那份偏心总落在它头上",
          "一柜子的杯子，他伸手拿的永远是同一只",
          ["最喜欢的", "最爱的"],
          ["This is my favorite song.", "Blue is her favorite color."],
          ["preferred", "beloved"], ["disliked"],
          ["favor", "favorable"],
          ["最喜欢的/最爱的：偏心总落在它头上的那一个"],
          "favor（偏爱）+ -ite → 偏心总落在它头上"),
    ],
})

# ---------- pingere（着色）----------
families.append({
    "root": {
        "id": "pingere", "root": "pingere", "variants": ["paint", "pict", "pig"],
        "origin": "拉丁语 pingere（用颜色涂画、绣饰），过去分词 pictus；"
                  "经古法语 peindre 入英语成 paint，picture、pigment 同出此支",
        "core_concept": "to lay colour onto a surface / 把颜色敷到面上去",
        "core_image": "刷子蘸上颜色，在板面上抹开，木纹一点点被盖住",
        "english_definition": "to paint, colour, depict",
    },
    "concept": {
        "id": "concept-pingere-lay-colour", "concept": "to lay colour onto a surface",
        "chinese": "敷色于面", "core_image": "刷子蘸色在板面抹开，木纹一点点被盖住",
        "root_ids": ["pingere"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("paint", "pingere", "noun / verb", "/peɪnt/",
          "pingere（涂色）→ 敷到面上的那种颜色；也指作画这件事",
          "古法语 peint（涂过的），peindre 的过去分词 ← 拉丁语 pingere",
          "coloured liquid put on a surface; to make a picture with colour",
          "the colour laid on, and the laying of it – 敷上去的那层色，以及敷色这件事",
          "刷子在板上来回一趟，后头的木纹就看不见了",
          ["油漆", "颜料", "绘画"],
          ["The door needs a fresh coat of paint.", "She paints in oils."],
          ["colour", "coat"], [],
          ["painter", "painting"],
          ["油漆/颜料：敷到面上的那层色", "绘画：把色敷成图这件事"],
          "pingere（涂色）→ 敷到面上的那层色及敷色之事"),
        W("painter", "pingere", "noun", "/ˈpeɪntə(r)/",
          "paint（敷色）+ -er（人）→ 干敷色这活的人：作画的或刷漆的",
          "英语 painter，来自 paint ← 拉丁语 pingere",
          "a person who paints pictures, or who paints buildings as a job",
          "the one whose work is laying colour on – 以敷色为活计的那个人",
          "他蹲在梯子下调色，桶边一圈干了的痕",
          ["画家", "油漆工"],
          ["The painter finished the portrait.", "We hired a painter for the kitchen."],
          ["artist", "decorator"], [],
          ["paint", "painting"],
          ["画家：以敷色作画为业的人", "油漆工：以敷色刷面为业的人"],
          "paint（敷色）+ -er → 干敷色这活的人"),
        W("painting", "pingere", "noun", "/ˈpeɪntɪŋ/",
          "paint（敷色）+ -ing → 敷色所成之物，及敷色这门事",
          "英语 painting，来自 paint 的动名词 ← 拉丁语 pingere",
          "a picture made with paint; the art or act of painting",
          "what the laid colour has become – 那层色最后成了的样子",
          "框子里那一幅挂上墙，颜色厚得能看出笔痕",
          ["画作", "绘画"],
          ["The painting hangs in the hall.", "She studied painting in Paris."],
          ["picture", "artwork"], [],
          ["paint", "painter"],
          ["画作：敷色所成的那一幅", "绘画：敷色成图这门事本身"],
          "paint（敷色）+ -ing → 敷色所成之物与其事"),
    ],
})

# ---------- experiri（试过）----------
families.append({
    "root": {
        "id": "experiri", "root": "experiri", "variants": ["peri", "per"],
        "origin": "拉丁语 experiri（试一试、亲身尝过），由 ex（出来）＋ peritus（试过的、有经验的）"
                  "一支构成；periculum（危险，本义「试出来的凶险」）同根",
        "core_concept": "knowledge got by trying it oneself / 亲手试过才落下来的那点东西",
        "core_image": "手伸进水里试了一下，凉热心里就有了数",
        "english_definition": "to try, test, undergo",
    },
    "concept": {
        "id": "concept-experiri-try", "concept": "knowledge got by trying it oneself",
        "chinese": "亲试而知", "core_image": "手伸进水里试一下，凉热心里就有了数",
        "root_ids": ["experiri"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("experience", "experiri", "noun", "/ɪkˈspɪəriəns/",
          "ex-（出来）+ peri（试）+ -ence → 亲身试过后留下来的那点本事",
          "拉丁语 experientia（试验所得），来自 experiri（亲身试过）",
          "knowledge or skill gained by doing something; an event one lives through",
          "what stays with one after having tried it – 试过之后留在身上的那点东西",
          "手在水里试过几回，伸进去就知道够不够烫",
          ["经验", "体验", "经历"],
          ["She has years of teaching experience.", "It was a frightening experience."],
          ["knowledge", "encounter"], ["inexperience"],
          ["experiment", "experimental"],
          ["经验：亲身试过后留下的本事", "体验/经历：亲身走过的那一遭"],
          "ex-（出来）+ peri（试）→ 试过后留在身上的东西"),
        W("experiment", "experiri", "noun", "/ɪkˈsperɪmənt/",
          "ex-（出来）+ peri（试）+ -ment → 特意安排的一次试，看会出什么",
          "拉丁语 experimentum（试验、检验），来自 experiri",
          "a scientific test done to find out what happens",
          "a trying set up on purpose to see what comes out – 特意摆开来试一次，看结果怎样",
          "两只杯子只差一样条件，摆在一处等着看分别",
          ["实验", "试验"],
          ["They ran the experiment three times.", "The experiment confirmed her theory."],
          ["test", "trial"], [],
          ["experience", "experimental"],
          ["实验/试验：特意安排的一次试，用来看结果"],
          "ex-（出来）+ peri（试）+ -ment → 特意摆开试一次"),
        W("experimental", "experiri", "adjective", "/ɪkˌsperɪˈmentl/",
          "experiment（试一次）+ -al（…的）→ 尚在试的、拿来试的",
          "英语 experimental，来自 experiment ← 拉丁语 experiri",
          "based on new methods not yet proved; used for testing",
          "still at the trying stage, not yet settled – 还在试的阶段，尚未定下来",
          "那台机器还摆在台上，参数天天改",
          ["实验的", "试验性的"],
          ["The treatment is still experimental.", "They set up an experimental farm."],
          ["trial", "tentative"], ["proven"],
          ["experience", "experiment"],
          ["实验的/试验性的：还在试、尚未定下来的"],
          "experiment（试一次）+ -al → 还在试的阶段"),
    ],
})

# ---------- planus（平）----------
families.append({
    "root": {
        "id": "planus", "root": "planus", "variants": ["plan", "plain", "plane"],
        "origin": "拉丁语 planus（平的、无起伏的）；plan 本指画在平面上的图样，"
                  "explanare（ex＋planus）是「把褶皱摊平」故引申为讲清楚，plain 亦同源",
        "core_concept": "flat with nothing standing in the way / 摊得平平的，没有起伏遮挡",
        "core_image": "一张纸铺开压平，褶子都推到边上去了",
        "english_definition": "flat, level, plain",
    },
    "concept": {
        "id": "concept-planus-flat", "concept": "flat with nothing standing in the way",
        "chinese": "摊得平", "core_image": "纸铺开压平，褶子都被推到边上",
        "root_ids": ["planus"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("plan", "planus", "noun / verb", "/plæn/",
          "planus（平面）→ 画在平面上的图样 → 打算、方案；动词即谋划",
          "法语 plan（平面图），来自拉丁语 planus（平的）",
          "a detailed proposal for doing something; a drawing seen from above",
          "the layout drawn flat before anything is built – 动工之前先摊在平面上画出来的那套",
          "桌上铺开一张图，每一处都先在纸上定好位置",
          ["计划", "方案", "平面图"],
          ["We made a plan for the weekend.", "The architect showed us the floor plan."],
          ["scheme", "design"], [],
          ["plane", "explanation"],
          ["计划/方案：动工前先在平面上定下的那套", "平面图：从上方看、摊平画出的那张图"],
          "planus（平面）→ 先摊平画出来的那套"),
        W("plane", "planus", "noun", "/pleɪn/",
          "planus（平的）→ 平面；机翼是平展的面，故 aeroplane 截短为 plane；刨子是找平的工具",
          "拉丁语 planus（平的）；飞机义来自 aeroplane（aer 空气＋planus 平面）的截短",
          "a flat surface; an aircraft; a tool for smoothing wood",
          "a face with no rise in it, and things named for such a face – 没有起伏的那个面，以及以此得名之物",
          "推子沿着木头走过去，凸起的一层卷成花掉在地上",
          ["平面", "飞机", "刨子"],
          ["Draw two lines on the same plane.", "Our plane landed on time."],
          ["surface", "aircraft"], [],
          ["plan", "explanation"],
          ["平面：没有起伏的那个面", "飞机：因平展机翼得名（aeroplane 截短）", "刨子：把面找平的那件工具"],
          "planus（平的）→ 无起伏的面，及因此得名之物"),
        W("explanation", "planus", "noun", "/ˌekspləˈneɪʃn/",
          "ex-（出来）+ plan（平）+ -ation → 把褶子摊平摊开 → 讲清楚的那番话",
          "拉丁语 explanatio（阐明），来自 explanare（摊平、讲清）← ex＋planus",
          "a statement that makes something clear or gives a reason",
          "smoothing the folds out until the whole thing lies plain – 把褶皱一一摊开，整件事平平摆着",
          "他把揉皱的那张纸一点点抹平，字才认得出来",
          ["解释", "说明", "解释的理由"],
          ["He gave no explanation for the delay.", "Her explanation satisfied everyone."],
          ["clarification", "account"], [],
          ["plan", "plane"],
          ["解释/说明：把褶皱摊平、让人看清那番话", "解释的理由：摊平之后露出来的原委"],
          "ex-（出来）+ plan（平）→ 把褶子摊开讲清"),
    ],
})

# ---------- planta（幼苗）----------
families.append({
    "root": {
        "id": "planta", "root": "planta", "variants": ["plant"],
        "origin": "拉丁语 planta（幼苗、插枝），动词 plantare（栽种）本义是「用脚掌把苗踩进土里」"
                  "（planta 亦指脚掌）；与 planus（平）不同词，勿混",
        "core_concept": "a shoot pressed down into soil to grow / 把幼苗按进土里让它长",
        "core_image": "苗根塞进坑里，脚掌把周围的土踩实",
        "english_definition": "shoot, sprout, to set in soil",
    },
    "concept": {
        "id": "concept-planta-set-in-soil", "concept": "a shoot pressed down into soil to grow",
        "chinese": "栽苗入土", "core_image": "苗根塞进坑里，脚掌把周围的土踩实",
        "root_ids": ["planta"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("plant", "planta", "noun / verb", "/plɑːnt/",
          "planta（幼苗）→ 长在土里的活物；动词是把苗按进土里。厂房义由「设置安放」引申",
          "古英语 plante 借自拉丁语 planta（幼苗），动词 plantare（栽种）",
          "a living thing that grows in soil; a factory; to put in the ground to grow",
          "the shoot set into soil, and by extension anything set in place to work – 按进土里的那株苗，引申为安置到位以运作之物",
          "苗根塞进坑里，土一踩实，叶子第二天就抬起来了",
          ["植物", "种植", "工厂"],
          ["Water the plants every morning.", "They plant rice in early summer."],
          ["vegetation", "factory"], [],
          ["plantation", "transplant"],
          ["植物：按进土里长起来的活物", "种植：把苗按进土里这件事", "工厂：由「安置到位以运作」引申而来的厂房"],
          "planta（幼苗）→ 按进土里的苗；引申为安置到位之物"),
        W("plantation", "planta", "noun", "/plænˈteɪʃn/",
          "plant（栽种）+ -ation → 成片栽种的那块地",
          "拉丁语 plantatio（栽种），来自 plantare ← planta",
          "a large area where crops such as tea or rubber are grown",
          "ground where the setting-in was done row upon row – 一垄接一垄都按进苗去的那片地",
          "一垄接一垄望不到头，每株间距都一样",
          ["种植园", "人造林"],
          ["He works on a tea plantation.", "The plantation covers two hundred acres."],
          ["estate", "farm"], [],
          ["plant", "transplant"],
          ["种植园/人造林：成片按苗栽下的那块地"],
          "plant（栽种）+ -ation → 成片栽下苗的那块地"),
        W("transplant", "planta", "verb", "/trænsˈplɑːnt/",
          "trans-（转移）+ plant（栽）→ 起出来栽到别处 → 移栽；医学上指移植器官",
          "拉丁语 transplantare（移栽），来自 trans＋plantare ← planta",
          "to move a plant to another place; to move an organ into another body",
          "lifting what was set in one spot and setting it into another – 把按在这处的起出来，按到那处去",
          "带着根土整株起出来，挪到新坑里再踩实",
          ["移植", "移栽"],
          ["We transplanted the seedlings today.", "He received a heart transplant."],
          ["relocate", "graft"], [],
          ["plant", "plantation"],
          ["移栽：把苗起出来栽到别处", "移植：同一动作用在器官上"],
          "trans-（转移）+ plant（栽）→ 起出来按到别处"),
    ],
})

# ---------- polis（城邦）----------
families.append({
    "root": {
        "id": "polis", "root": "polis", "variants": ["polit", "polic", "polis"],
        "origin": "希腊语 polis（城邦），politēs（城邦公民）、politikos（关于城邦公共事务的）由此出；"
                  "英语 police、policy 同出此支",
        "core_concept": "the affairs of the city held in common / 城邦里众人共管的那些事",
        "core_image": "广场上一群人围着争执，事关全城谁都要开口",
        "english_definition": "city, city-state, citizenry",
    },
    "concept": {
        "id": "concept-polis-city-affairs", "concept": "the affairs of the city held in common",
        "chinese": "城邦公事", "core_image": "广场上众人围着争执，事关全城谁都要开口",
        "root_ids": ["polis"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("politics", "polis", "noun", "/ˈpɒlətɪks/",
          "polit（城邦公事）+ -ics（…之学/之事）→ 争夺与处置公共事务这一摊",
          "希腊语 politika（城邦事务），来自 politikos ← polis（城邦）",
          "the activities of government and of gaining power in it",
          "the wrangling over what the whole city should do – 围着「全城该怎么办」争出来的那一摊事",
          "广场中央吵成一片，各方都想让自己那套算数",
          ["政治", "政治学", "权术"],
          ["He went into politics at thirty.", "Office politics wore her down."],
          ["government", "statecraft"], [],
          ["political", "politician"],
          ["政治/政治学：处置公共事务这一摊及其学问", "权术：为在其中占上风而使的手段"],
          "polit（城邦公事）+ -ics → 争夺处置公事这一摊"),
        W("political", "polis", "adjective", "/pəˈlɪtɪkl/",
          "polit（城邦公事）+ -ical（…的）→ 与公共事务、权力相关的",
          "希腊语 politikos（关于城邦的），来自 polis",
          "relating to government or public affairs",
          "belonging to what the whole city argues over – 属于全城要争议的那类事",
          "这件事一摆上广场，各方立刻按立场分了边",
          ["政治的", "政党的"],
          ["It became a political issue overnight.", "She has strong political views."],
          ["governmental", "civic"], ["apolitical"],
          ["politics", "politician"],
          ["政治的/政党的：属于城邦公共事务与权力的"],
          "polit（城邦公事）+ -ical → 属于公共事务的"),
        W("politician", "polis", "noun", "/ˌpɒləˈtɪʃn/",
          "politic（城邦公事）+ -ian（司此业者）→ 以处置公共事务为业的人",
          "英语 politician，来自 politic ← 希腊语 polis",
          "a person whose job is in government or seeking elected office",
          "the one who stands in the square and speaks for a side – 站到广场上替一方开口的那个人",
          "他登上台阶开口，底下的人分头喝彩与嘘声",
          ["政治家", "政客"],
          ["The politician avoided the question.", "She is a career politician."],
          ["statesman", "legislator"], [],
          ["politics", "political"],
          ["政治家/政客：以处置公共事务为业、替一方发声的人"],
          "politic（城邦公事）+ -ian → 以处置公事为业的人"),
    ],
})

# ================= 组装 =================
words = []
for fam in families:
    words.extend(fam["words"])

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

assert len(words) == 21, len(words)
assert len(roots) == 7, len(roots)
assert len({r["id"] for r in roots}) == 7, "新词根 id 有重复"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words, {len(roots)} new roots")
