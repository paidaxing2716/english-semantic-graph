#!/usr/bin/env python3
"""Generate batch47: 6 new roots (18 词) + 3 additions to placere.

新族:
  friskaz（新鲜）    fresh / refresh / refreshment   —— 日耳曼源，非拉丁
  wardon（看守）     regard / regarding / regardless —— 法兰克源经古法语
  regula（准尺）     regular / regulate / regulation
  heros（英豪）      hero / heroic / heroine
  diurnus（一日）    journal / journalist / journey
  metron（量度）     metre / metric / symmetry

补词（并入已建模 placere 根，该根现有 place/replace/displace）:
  pleasant / please / pleasure

关于日耳曼源词族的处理：项目已有 hum-onomatopoeia（拟声）先例，词根不限拉丁/希腊，
故 fresh 与 regard 两族照样立词根、标 decomposable="root"。
裸 germanic 标记（root_ids 留空）只给「查无可建模词根」的词，如已有的 choose/pick/miss。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch47.json"


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

# ---------- friskaz（新鲜）----------
families.append({
    "root": {
        "id": "friskaz", "root": "friskaz", "variants": ["fresh", "fresch"],
        "origin": "原始日耳曼语 *friskaz（不咸的、未腐的），古英语作 fersc；"
                  "同一支经法兰克语入古法语成 fresche，英语 refresh 即从这一路借回，"
                  "故本族是日耳曼源而非拉丁源",
        "core_concept": "still as it was when new, not gone stale / 还是刚来时那样，没走味",
        "core_image": "刚摘下的果子掰开，切面水亮，凑近有股清气",
        "english_definition": "new, unspoiled, not salt",
    },
    "concept": {
        "id": "concept-friskaz-unspoiled", "concept": "still as it was when new, not gone stale",
        "chinese": "未走味", "core_image": "刚摘的果子掰开，切面水亮，凑近有股清气",
        "root_ids": ["friskaz"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("fresh", "friskaz", "adjective", "/freʃ/",
          "friskaz（未腐、不咸）→ 还保着刚来时那副样子",
          "古英语 fersc（不咸的、未腐的），来自原始日耳曼语 *friskaz",
          "newly made or obtained; not stale; not salty",
          "keeping the state it had at the very start – 还守着刚出来时那个状态",
          "刚出炉的那一块掰开，热气往上冒",
          ["新鲜的", "清新的", "淡水的"],
          ["Buy fresh bread every morning.", "She went out for some fresh air."],
          ["new", "crisp"], ["stale"],
          ["refresh", "refreshment"],
          ["新鲜的：还是刚出来时那个样子", "清新的：气息不闷不浊", "淡水的：不带盐味的那种水"],
          "friskaz（未腐、不咸）→ 还守着刚来时的状态"),
        W("refresh", "friskaz", "verb", "/rɪˈfreʃ/",
          "re-（重新）+ fresh（未走味）→ 把那副刚来时的样子找回来",
          "古法语 refreschier（使变凉爽），由 re-＋fresche ← 法兰克语，同出 *friskaz",
          "to make someone feel less tired; to update something",
          "bringing a thing back to the state it started in – 把它拉回刚出来时那个状态",
          "洗过脸再坐下，人像换了一个",
          ["使恢复精神", "刷新"],
          ["A cold drink will refresh you.", "Refresh the page to see the change."],
          ["revive", "renew"], ["tire", "exhaust"],
          ["fresh", "refreshment"],
          ["使恢复精神：把人拉回刚开始时那股劲", "刷新：把画面拉回最新那一版"],
          "re-（重新）+ fresh（未走味）→ 拉回刚来时的状态"),
        W("refreshment", "friskaz", "noun", "/rɪˈfreʃmənt/",
          "refresh（使恢复）+ -ment → 使人回过劲来的那份东西",
          "古法语 refreschissement，来自 refreschier ← 同出 *friskaz",
          "a light snack or drink; the act of making one feel less tired",
          "the small thing taken to get one's edge back – 拿来把劲头找回来的那一点东西",
          "半路歇脚，喝下那一杯，脚步又轻了",
          ["点心", "饮料", "恢复精神"],
          ["Refreshments will be served at noon.", "He paused for refreshment."],
          ["snack", "revival"], [],
          ["fresh", "refresh"],
          ["点心/饮料：拿来把劲头找回的那点东西", "恢复精神：找回劲头这件事本身"],
          "refresh（使恢复）+ -ment → 把劲头找回的那份东西"),
    ],
})

# ---------- wardon（看守）----------
families.append({
    "root": {
        "id": "wardon", "root": "wardon", "variants": ["gard", "guard", "ward"],
        "origin": "法兰克语 *wardon（守望、看顾）入古法语成 guarder/garder（看守），"
                  "regarder 即 re-＋garder（再看一眼）；英语 guard、ward 同出此支，"
                  "故本族为日耳曼源经法语，而非拉丁源",
        "core_concept": "to turn the eyes onto something and keep them there / 把目光投过去并守住",
        "core_image": "守夜人举灯朝那个方向照过去，眼睛一直盯着不移开",
        "english_definition": "to watch over, keep in view",
    },
    "concept": {
        "id": "concept-wardon-watch", "concept": "to turn the eyes onto something and keep them there",
        "chinese": "投目看守", "core_image": "守夜人举灯朝一处照去，眼睛盯住不移开",
        "root_ids": ["wardon"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("regard", "wardon", "verb", "/rɪˈɡɑːd/",
          "re-（再）+ gard（看守）→ 再把目光投过去 → 看待；引申为敬重、问候",
          "古法语 regarder（注视），由 re-＋garder（看守）← 法兰克语 *wardon",
          "to think of someone in a particular way; respect; greetings",
          "turning the eyes back onto a thing and holding a view of it – 把目光再投回去，并就此存下一个看法",
          "他把灯又转回那一处，端端地照了好一会儿",
          ["看待", "认为", "尊重", "问候"],
          ["She is regarded as an expert.", "Give my regards to your parents."],
          ["consider", "esteem"], ["ignore", "despise"],
          ["regarding", "regardless"],
          ["看待/认为：把目光投过去并存下一个看法", "尊重：目光里带着分量", "问候：把这份目光托人带过去"],
          "re-（再）+ gard（看守）→ 再把目光投过去"),
        W("regarding", "wardon", "preposition", "/rɪˈɡɑːdɪŋ/",
          "regard（投目看待）的分词转介词 → 目光所对着的那件事",
          "英语 regarding，regard 的现在分词转作介词",
          "about; concerning a particular matter",
          "pointing at the very thing the eyes are turned on – 直指目光正对着的那一桩",
          "灯光圈住的就是要谈的那一处，旁的都在暗里",
          ["关于", "至于"],
          ["I wrote to him regarding the delay.", "Regarding costs, we need more data."],
          ["about", "concerning"], [],
          ["regard", "regardless"],
          ["关于/至于：目光正对着的那一桩事"],
          "regard（投目）+ -ing → 目光所对着的那件事"),
        W("regardless", "wardon", "adverb", "/rɪˈɡɑːdləs/",
          "regard（投目留意）+ -less（无…）→ 不往那边看 → 不顾、照样做",
          "英语 regardless，由 regard＋-less（缺乏）构成",
          "without paying attention to something; anyway",
          "walking on without turning the eyes to what stands there – 眼睛不往那边转，照样往前走",
          "旁边有人喊他，他连头都没偏，脚步没停",
          ["不顾", "不管", "无论如何"],
          ["He went ahead regardless of the risk.", "We must finish it regardless."],
          ["anyway", "nevertheless"], [],
          ["regard", "regarding"],
          ["不顾/不管：目光不往那边转", "无论如何：不管那边有什么，照样进行"],
          "regard（投目留意）+ -less（无）→ 不往那边看，照样走"),
    ],
})

# ---------- regula（准尺）----------
families.append({
    "root": {
        "id": "regula", "root": "regula", "variants": ["regul", "rul"],
        "origin": "拉丁语 regula（笔直的木尺、准绳），来自 regere（导正）；"
                  "英语 rule 同出此支。与已建模的 rect（regere 的分词 rectus 一支：correct/direct）"
                  "同源而分支不同，本族收 regula 名词一路",
        "core_concept": "a straight rod things are lined up against / 一根直尺，凡物都靠它比齐",
        "core_image": "一把直尺压在纸上，笔沿着它走，线才不歪",
        "english_definition": "straight rod, rule, standard",
    },
    "concept": {
        "id": "concept-regula-straightedge", "concept": "a straight rod things are lined up against",
        "chinese": "准绳直尺", "core_image": "直尺压在纸上，笔沿着它走，线才不歪",
        "root_ids": ["regula"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("regular", "regula", "adjective", "/ˈreɡjələ(r)/",
          "regul（直尺）+ -ar（…的）→ 合着尺子来的 → 匀齐、按时",
          "拉丁语 regularis（合于准尺的），来自 regula（直尺）",
          "happening at even intervals; usual; evenly shaped",
          "coming out even because each was laid to the same rod – 每一个都照同一把尺来，故彼此齐整",
          "砖缝一道道对齐，间距都照同一把尺量过",
          ["规则的", "定期的", "经常的"],
          ["He is a regular customer here.", "Take regular breaks while working."],
          ["steady", "routine"], ["irregular", "occasional"],
          ["regulate", "regulation"],
          ["规则的：处处合着同一把尺、匀齐", "定期的/经常的：时间上也按尺子等距排开"],
          "regul（直尺）+ -ar → 合着同一把尺、故齐整"),
        W("regulate", "regula", "verb", "/ˈreɡjuleɪt/",
          "regul（直尺）+ -ate（使…）→ 拿尺子把它校到位 → 调节、管束",
          "晚期拉丁语 regulare（按准尺处理），来自 regula",
          "to control the rate or level of something; to govern by rules",
          "holding a thing to the rod and trimming it to fit – 拿尺子比着，把它修到合线",
          "旋钮往回拧半圈，指针就落回刻线上",
          ["调节", "管理", "控制"],
          ["A thermostat regulates the temperature.", "New laws regulate online sales."],
          ["control", "adjust"], [],
          ["regular", "regulation"],
          ["调节/控制：拿尺子比着把它校到合线", "管理：用成套准绳去管束"],
          "regul（直尺）+ -ate → 拿尺子把它校到位"),
        W("regulation", "regula", "noun", "/ˌreɡjuˈleɪʃn/",
          "regulate（按尺校准）+ -ion → 立成条款的那把尺，及校准这件事",
          "晚期拉丁语 regulatio，来自 regulare ← regula",
          "an official rule; the act of controlling something",
          "the rod written down so all must be laid against it – 把那把尺写成条款，人人都得比着它",
          "墙上钉着一张表，每条都写明该照哪道线来",
          ["规章", "条例", "调节"],
          ["Safety regulations must be followed.", "The regulation of prices is disputed."],
          ["rule", "control"], [],
          ["regular", "regulate"],
          ["规章/条例：写成条款、人人须比着的那把尺", "调节：按尺校准这件事本身"],
          "regulate（按尺校准）+ -ion → 写成条款的那把尺"),
    ],
})

# ---------- heros（英豪）----------
families.append({
    "root": {
        "id": "heros", "root": "heros", "variants": ["hero", "heroin"],
        "origin": "希腊语 hērōs（半神的勇士、受尊崇的死者）经拉丁语 heros 入英语；"
                  "阴性作 hērōinē，英语 heroine 由此",
        "core_concept": "the one the story is told about for daring / 因胆识而被传颂的那个人",
        "core_image": "众人围坐火边，一遍遍讲同一个人闯过的那一关",
        "english_definition": "hero, demigod, champion",
    },
    "concept": {
        "id": "concept-heros-champion", "concept": "the one the story is told about for daring",
        "chinese": "被传颂者", "core_image": "众人围坐火边，一遍遍讲同一个人闯过的那一关",
        "root_ids": ["heros"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("hero", "heros", "noun", "/ˈhɪərəʊ/",
          "hērōs（受尊崇的勇士）→ 因胆识受人传颂的人；也指故事里的主角",
          "拉丁语 heros，来自希腊语 hērōs（半神的勇士）",
          "a person admired for courage; the chief character in a story",
          "the one whose deed the others keep retelling – 事迹被旁人一再讲起的那个人",
          "火堆边的人又提起他，那一关闯得众人服气",
          ["英雄", "男主角"],
          ["He was hailed as a hero.", "The hero of the novel is a doctor."],
          ["champion", "protagonist"], ["coward", "villain"],
          ["heroic", "heroine"],
          ["英雄：因胆识被一再传颂的人", "男主角：故事里被讲述的那个中心人物"],
          "hērōs（受尊崇的勇士）→ 事迹被一再讲起的人"),
        W("heroic", "heros", "adjective", "/hɪˈrəʊɪk/",
          "hero（被传颂者）+ -ic（…的）→ 够得上被传颂的那种",
          "希腊语 hērōikos（属于勇士的），来自 hērōs",
          "very brave; showing great courage",
          "of the kind that gets retold afterwards – 属于事后会被人讲起的那一种",
          "他冲进去那一下，后来被人反复说起",
          ["英勇的", "英雄的"],
          ["She made a heroic effort to save him.", "It was a heroic act of defiance."],
          ["brave", "valiant"], ["cowardly"],
          ["hero", "heroine"],
          ["英勇的/英雄的：够得上事后被人传颂的那种"],
          "hero（被传颂者）+ -ic → 够得上被传颂的那种"),
        W("heroine", "heros", "noun", "/ˈherəʊɪn/",
          "hero（被传颂者）+ -ine（阴性）→ 女性的那一位；也指故事女主角",
          "希腊语 hērōinē（女勇士），hērōs 的阴性形",
          "a woman admired for courage; the chief female character in a story",
          "the woman whose deed the others keep retelling – 事迹被旁人一再讲起的那位女性",
          "那家人至今说起她夜里背人出来的事",
          ["女英雄", "女主角"],
          ["She became a national heroine.", "The heroine escapes in the last act."],
          ["champion", "protagonist"], ["villain"],
          ["hero", "heroic"],
          ["女英雄：因胆识被传颂的女性", "女主角：故事里被讲述的那位女性中心人物"],
          "hero（被传颂者）+ -ine（阴性）→ 女性的那一位"),
    ],
})

# ---------- diurnus（一日）----------
families.append({
    "root": {
        "id": "diurnus", "root": "diurnus", "variants": ["journ", "jour", "diurn"],
        "origin": "拉丁语 diurnus（一日的），来自 dies（日）；经古法语 jour（日）派出 "
                  "jornal（每日的记事）与 jornee（一天的路程），英语 journal/journey 分别由此",
        "core_concept": "the span of one day, and what fills it / 一天这段光景，及这一天里的事",
        "core_image": "天亮出门天黑歇脚，这一天走了多远、记下什么，都装在这一段里",
        "english_definition": "of the day, daily",
    },
    "concept": {
        "id": "concept-diurnus-day", "concept": "the span of one day, and what fills it",
        "chinese": "一日之程", "core_image": "天亮出门天黑歇脚，一天里走的路、记的事都在这段里",
        "root_ids": ["diurnus"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("journal", "diurnus", "noun", "/ˈdʒɜːnl/",
          "jour（日）+ -nal → 按日记下的册子 → 日志；引申为定期出的刊物",
          "古法语 jornal（每日的记事），来自拉丁语 diurnalis ← diurnus（一日的）",
          "a daily record of events; a magazine on a special subject",
          "the book that takes one entry per day – 一天记一笔的那本册子",
          "每晚睡前写一行，一年下来那本厚了一截",
          ["日志", "日记", "期刊"],
          ["She keeps a journal of her travels.", "The paper appeared in a medical journal."],
          ["diary", "periodical"], [],
          ["journalist", "journey"],
          ["日志/日记：按日记下的那本册子", "期刊：同样按期出的那类刊物"],
          "jour（日）+ -nal → 一天记一笔的那本册子"),
        W("journalist", "diurnus", "noun", "/ˈdʒɜːnəlɪst/",
          "journal（按日的刊）+ -ist（司此业者）→ 替这类刊物采写的人",
          "法语 journaliste，来自 journal ← 拉丁语 diurnus",
          "a person who writes news for papers, radio, or television",
          "the one who fills the daily pages – 把那按日出的版面填起来的人",
          "他赶在天黑前把稿子发回去，好赶上明早那一版",
          ["记者", "新闻工作者"],
          ["The journalist interviewed both sides.", "She trained as a journalist."],
          ["reporter", "correspondent"], [],
          ["journal", "journey"],
          ["记者/新闻工作者：替按日出的刊物采写的人"],
          "journal（按日的刊）+ -ist → 替它采写的人"),
        W("journey", "diurnus", "noun", "/ˈdʒɜːni/",
          "jour（日）+ -ney → 本指一天能走完的路程，后泛指整趟行程",
          "古法语 jornee（一天的路程、一天的活），来自 jour（日）← 拉丁语 diurnus",
          "an act of travelling from one place to another",
          "as far as one gets between sunup and dark, extended to the whole trip – 天亮到天黑能走的那一段，后指整趟",
          "清早动身，日头落时到了下一个镇子",
          ["旅程", "行程", "旅行"],
          ["The journey takes about three hours.", "They set out on a long journey."],
          ["trip", "voyage"], [],
          ["journal", "journalist"],
          ["旅程/行程：本指一天走完的路，后指整趟路途", "旅行：走这段路这件事"],
          "jour（日）+ -ney → 一天能走完的路，引申为整趟"),
    ],
})

# ---------- metron（量度）----------
families.append({
    "root": {
        "id": "metron", "root": "metron", "variants": ["metr", "meter", "metri"],
        "origin": "希腊语 metron（量具、尺度、诗的音步）经拉丁语 metrum、法语 mètre 入英语；"
                  "symmetry 是 syn（一同）＋metron（量度）——两边照同一尺量得一样",
        "core_concept": "the measure by which things are gauged / 拿来量东西的那个尺度",
        "core_image": "一根标好刻度的杆横过去，长短照它报数",
        "english_definition": "measure, metre",
    },
    "concept": {
        "id": "concept-metron-measure", "concept": "the measure by which things are gauged",
        "chinese": "量度尺", "core_image": "标好刻度的杆横过去，长短照它报数",
        "root_ids": ["metron"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("metre", "metron", "noun", "/ˈmiːtə(r)/",
          "metron（量度）→ 定作标准的那一段长；诗里指音步的节拍",
          "法语 mètre，来自希腊语 metron（量具、音步）",
          "a unit of length equal to 100 centimetres; the rhythm of verse",
          "the one length agreed on as the yardstick – 公认拿来当准的那一段长",
          "地上那道标线到下一道，正好是定死的一段",
          ["米", "韵律"],
          ["The room is four metres wide.", "The poem is written in strict metre."],
          ["yard", "rhythm"], [],
          ["metric", "symmetry"],
          ["米：公认作准的那一段长", "韵律：诗句里按拍子量出的节奏"],
          "metron（量度）→ 定作标准的那一段长"),
        W("metric", "metron", "adjective", "/ˈmetrɪk/",
          "metr（量度）+ -ic（…的）→ 按这套尺度来的",
          "法语 métrique，来自希腊语 metrikos（关于量度的）← metron",
          "relating to the system based on metres and grams",
          "belonging to the one agreed set of measures – 属于那一套公认尺度的",
          "秤和尺换成同一套标法，各处报出的数才对得上",
          ["公制的", "度量的"],
          ["Britain uses metric units now.", "Convert the figures to metric."],
          ["decimal", "measured"], [],
          ["metre", "symmetry"],
          ["公制的/度量的：按那一套公认尺度来的"],
          "metr（量度）+ -ic → 按这套尺度来的"),
        W("symmetry", "metron", "noun", "/ˈsɪmətri/",
          "sym-（syn- 一同）+ metr（量度）+ -y → 两边照同一尺量得一样 → 对称",
          "希腊语 symmetria（同一尺度、匀称），来自 syn（一同）＋metron（量度）",
          "the quality of having two halves that match exactly",
          "both sides coming out equal when laid to the same measure – 拿同一把尺量两边，数一样",
          "蝴蝶合起翅膀，左右两片严丝合缝地叠在一起",
          ["对称", "匀称"],
          ["The building has perfect symmetry.", "There is a pleasing symmetry to the design."],
          ["balance", "proportion"], ["asymmetry"],
          ["metre", "metric"],
          ["对称/匀称：两边照同一尺量出来一样"],
          "sym-（一同）+ metr（量度）→ 两边量得一样"),
    ],
})

# ================= 补词：并入已建模 placere 根 =================
# placere（使中意）根下现有 place/replace/replacement/displace。
additions = [
    W("please", "placere", "verb", "/pliːz/",
      "placere（使中意）→ 让对方合意；作副词时是「若合你意」的省说，即请",
      "古法语 plaisir（使满意），来自拉丁语 placere（使中意、讨喜）",
      "to make someone glad; used politely to ask for something",
      "bringing a thing round to what the other finds agreeable – 把事情做到对方合意那一步",
      "他把茶端到手边，对方眉头一松",
      ["使高兴", "请", "使满意"],
      ["It pleased her to hear the news.", "Please close the door behind you."],
      ["satisfy", "delight"], ["annoy", "displease"],
      ["pleasant", "pleasure"],
      ["使高兴/使满意：做到对方合意那一步", "请：说话时以「若合你意」相求"],
      "placere（使中意）→ 做到对方合意；「若合你意」即请"),
    W("pleasant", "placere", "adjective", "/ˈpleznt/",
      "please（使合意）+ -ant（正…的）→ 正让人合意的",
      "古法语 plaisant（讨喜的），plaisir 的现在分词 ← 拉丁语 placere",
      "enjoyable; giving a feeling of satisfaction",
      "of the kind that sits well with whoever meets it – 遇上的人都觉得受用的那种",
      "屋里温度刚好，坐下来谁都不想起身",
      ["令人愉快的", "宜人的", "友善的"],
      ["We had a pleasant evening together.", "She has a pleasant manner."],
      ["agreeable", "delightful"], ["unpleasant"],
      ["please", "pleasure"],
      ["令人愉快的/宜人的：正让人合意受用的", "友善的：待人的样子也让人合意"],
      "please（使合意）+ -ant → 正让人合意的"),
    W("pleasure", "placere", "noun", "/ˈpleʒə(r)/",
      "please（使合意）+ -ure（名词）→ 合意时心里那份受用",
      "古法语 plaisir（快乐），本是动词不定式用作名词 ← 拉丁语 placere",
      "a feeling of happy satisfaction; something that gives this",
      "what one feels when a thing lands just right – 事情正合意时心里那份受用",
      "他听完往椅背上一靠，脸上的紧绷散了",
      ["乐趣", "愉快", "荣幸"],
      ["Reading gives him great pleasure.", "It is a pleasure to meet you."],
      ["delight", "enjoyment"], ["pain", "displeasure"],
      ["please", "pleasant"],
      ["乐趣/愉快：正合意时心里那份受用", "荣幸：把此事当作合意之事来说的客气话"],
      "please（使合意）+ -ure → 合意时心里那份受用"),
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

assert len(words) == 21, len(words)
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
