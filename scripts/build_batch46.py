#!/usr/bin/env python3
"""Generate batch46: 6 new roots (18 词) + 3 additions to ponere.

新族:
  cadere（落下）    incidence / incident / incidentally
  kyklos（轮转）    bicycle / cycle / recycle
  largus（充裕）    enlarge / large / largely
  maior（更大）     majesty / major / majority
  numerus（数目）   innumerable / numerical / numerous
  logos（言说条理） apologise / apology / biology
      vetted 族名作 olog，那是自动词干提取切出来的假词根：
      apology ← apo（离开）＋logos（说辞），biology ← bios（生命）＋logos（条理），
      三词真正共用的是 logos，故词根立 logos 而非 olog。

补词（并入已建模 ponere 根）:
  post / postage / posture —— 均出拉丁 ponere（放置）的 positum 一支：
      驿站是「置马之处」→ 邮政；被安置的位子 → 职位；身体摆放的样子 → 姿势。
      注：门柱义的 post 来自拉丁 postis，与此不同源，故本词条不收该义。

词根 id 一律用拉丁/希腊词形：large、post 等本身是单词，用族名作 id 会造自环边
（form/port/flu/press 已踩过三次）。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch46.json"


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

# ---------- cadere（落下）----------
families.append({
    "root": {
        "id": "cadere", "root": "cadere", "variants": ["cid", "cad", "cas"],
        "origin": "拉丁语 cadere（落下、掉下来），过去分词 casus；"
                  "incidere（in＋cadere）本义是「落到某处上头」，引申为事情落下来发生",
        "core_concept": "to fall upon, to come down on something / 落到某处上头",
        "core_image": "一颗东西从高处掉下来，正砸在路当中",
        "english_definition": "to fall, drop",
    },
    "concept": {
        "id": "concept-cadere-fall", "concept": "to fall upon, to come down on something",
        "chinese": "落到头上", "core_image": "东西自高处掉下，正砸在路当中",
        "root_ids": ["cadere"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("incident", "cadere", "noun", "/ˈɪnsɪdənt/",
          "in-（落到…上）+ cid（落下）+ -ent → 落到日常里头的那一桩",
          "拉丁语 incidens（落在上头的），来自 incidere ← in＋cadere（落下）",
          "an event, especially an unpleasant or unusual one",
          "the one thing that came down into an otherwise plain day – 落进平常日子里的那一桩",
          "路当中忽然砸下一样东西，行人全停下来看",
          ["事件", "事变"],
          ["The incident was reported to the police.", "No one was hurt in the incident."],
          ["event", "occurrence"], [],
          ["incidence", "incidentally"],
          ["事件/事变：落进平常日子里的那一桩"],
          "in-（落到上）+ cid（落下）→ 落进日子里的那一桩"),
        W("incidence", "cadere", "noun", "/ˈɪnsɪdəns/",
          "incident（落下之事）+ -ence → 落下来的频密程度 → 发生的多寡",
          "拉丁语 incidentia，来自 incidere（落到上头）",
          "the rate at which something happens, especially something unwanted",
          "how thickly such fallings come down over a stretch – 一段里头落下多密",
          "雨点打在窗台上，一阵密一阵疏，数得出快慢",
          ["发生率", "发生频率"],
          ["The incidence of the disease has fallen.", "There is a high incidence of theft here."],
          ["rate", "frequency"], [],
          ["incident", "incidentally"],
          ["发生率/发生频率：这类事落下来的密度"],
          "incident（落下之事）+ -ence → 落下来有多密"),
        W("incidentally", "cadere", "adverb", "/ˌɪnsɪˈdentli/",
          "incidental（顺带落下的）+ -ly → 顺着话头落下来一句 → 顺便说",
          "英语 incidentally，来自 incidental ← incident",
          "used to add a remark not connected to the main point",
          "a word that drops in alongside, not the thing one came to say – 顺着旁边落下来的一句，不是正题",
          "话说到一半，他顺口带出一句不相干的",
          ["顺便说", "偶然地"],
          ["Incidentally, I saw her yesterday.", "The two met quite incidentally."],
          ["casually"], ["deliberately"],
          ["incident", "incidence"],
          ["顺便说：顺着话头旁落下来的一句", "偶然地：不是安排好、恰巧落下的"],
          "incidental（顺带落下）+ -ly → 顺着旁边落下一句"),
    ],
})

# ---------- kyklos（轮转）----------
families.append({
    "root": {
        "id": "kyklos", "root": "kyklos", "variants": ["cycl", "cycle"],
        "origin": "希腊语 kyklos（圆圈、轮子）经拉丁语 cyclus 入英语；"
                  "轮子转一整圈回到原处，是这一族的共同意象",
        "core_concept": "a wheel coming round to where it began / 转一圈又回到起点的轮",
        "core_image": "轮子滚过一整圈，气门嘴又回到贴地那一点",
        "english_definition": "circle, wheel",
    },
    "concept": {
        "id": "concept-kyklos-wheel", "concept": "a wheel coming round to where it began",
        "chinese": "轮转一圈", "core_image": "轮子滚满一圈，气门嘴又回到贴地那一点",
        "root_ids": ["kyklos"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("cycle", "kyklos", "noun / verb", "/ˈsaɪkl/",
          "kyklos（圆圈）→ 转回原处的一整圈 → 周期；也指骑那两个轮子",
          "拉丁语 cyclus，来自希腊语 kyklos（圆圈、轮）",
          "a set of events repeating in the same order; to ride a bicycle",
          "one full turn that ends where it started – 转满一圈、终点又是起点",
          "四季走一遍，又回到落第一场雪的那几天",
          ["周期", "循环", "骑车"],
          ["The washing machine has a short cycle.", "She cycles to work every day."],
          ["round", "sequence"], [],
          ["bicycle", "recycle"],
          ["周期/循环：转满一圈又回到起点", "骑车：踩着轮子转圈前行"],
          "kyklos（圆圈）→ 转回原处的一整圈"),
        W("bicycle", "kyklos", "noun", "/ˈbaɪsɪkl/",
          "bi-（二）+ cycl（轮）+ -e → 两个轮子的车",
          "法语 bicycle，由拉丁 bi-（二）＋希腊 kyklos（轮）合成，19 世纪造词",
          "a vehicle with two wheels that one pedals",
          "the frame that rides on two turning circles – 架在两个转圈之物上的车",
          "前后两个圈一齐转起来，人就跟着往前走",
          ["自行车", "脚踏车"],
          ["He rode his bicycle to school.", "Her bicycle has a broken chain."],
          ["bike", "cycle"], [],
          ["cycle", "recycle"],
          ["自行车/脚踏车：架在两个转圈之物上的车"],
          "bi-（二）+ cycl（轮）→ 两个轮子的车"),
        W("recycle", "kyklos", "verb", "/riːˈsaɪkl/",
          "re-（再）+ cycl（转一圈）+ -e → 让它再转一圈回来 → 回收再用",
          "英语 recycle，由 re-＋cycle 合成，20 世纪随环保用语普及",
          "to treat used material so it can be used again",
          "sending a thing round the loop once more instead of dropping it – 让用过之物再走一圈回来，而不是丢掉",
          "旧瓶子送回炉里，出来时又是一只能用的",
          ["回收", "再利用"],
          ["We recycle paper and glass at home.", "These bottles can be recycled."],
          ["reuse", "reclaim"], ["discard"],
          ["cycle", "bicycle"],
          ["回收/再利用：让用过之物再转一圈回来"],
          "re-（再）+ cycl（转圈）→ 让它再走一圈回来"),
    ],
})

# ---------- largus（充裕）----------
families.append({
    "root": {
        "id": "largus", "root": "largus", "variants": ["larg", "large"],
        "origin": "拉丁语 largus（丰足的、宽绰的），本义偏「给得出、有余裕」，"
                  "英语 large 早期也表「宽绰」，后才专指体量",
        "core_concept": "having room and to spare / 宽绰有余、装得下还有空",
        "core_image": "一只箱子装完东西还空着半截，盖子轻轻就合上",
        "english_definition": "abundant, ample, roomy",
    },
    "concept": {
        "id": "concept-largus-ample", "concept": "having room and to spare",
        "chinese": "宽绰有余", "core_image": "箱子装完还空着半截，盖子轻轻就合上",
        "root_ids": ["largus"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("large", "largus", "adjective", "/lɑːdʒ/",
          "largus（宽绰有余）→ 体量占得开、不局促",
          "古法语 large，来自拉丁语 largus（丰足的、宽绰的）",
          "of considerable size or extent",
          "taking up room with margin left over – 占得开、周围还留着余地",
          "两臂张开也抱不住那截树身",
          ["大的", "大量的"],
          ["They live in a large house.", "A large number of people came."],
          ["big", "considerable"], ["small", "tiny"],
          ["enlarge", "largely"],
          ["大的/大量的：占得开、有余裕而不局促"],
          "largus（宽绰有余）→ 占得开、不局促"),
        W("enlarge", "largus", "verb", "/ɪnˈlɑːdʒ/",
          "en-（使…）+ large（宽绰）→ 使它占得更开 → 扩大、放大",
          "古法语 enlargier（放宽），由 en-＋large ← 拉丁语 largus",
          "to make something bigger, or to become bigger",
          "pushing the edges out so there is more room within – 把边往外推，里头就更宽绰",
          "照片一角被拉到满幅，原先看不清的纹路露了出来",
          ["扩大", "放大", "增大"],
          ["They plan to enlarge the kitchen.", "Please enlarge this photograph."],
          ["expand", "extend"], ["reduce", "shrink"],
          ["large", "largely"],
          ["扩大/放大/增大：把边往外推、使更宽绰"],
          "en-（使）+ large（宽绰）→ 把边往外推"),
        W("largely", "largus", "adverb", "/ˈlɑːdʒli/",
          "large（大部分）+ -ly → 占着大头地 → 主要、多半",
          "英语 largely，来自 large 加副词后缀 -ly",
          "mostly; to a great extent",
          "the side that takes up most of the whole – 占了整体大头的那一边",
          "天平一头压得低低的，另一头只剩一点",
          ["主要地", "大部分", "多半"],
          ["The project was largely successful.", "His account is largely accurate."],
          ["mainly", "mostly"], ["slightly"],
          ["large", "enlarge"],
          ["主要地/大部分/多半：占着整体大头的那一边"],
          "large（大部分）+ -ly → 占着大头地"),
    ],
})

# ---------- maior（更大）----------
families.append({
    "root": {
        "id": "maior", "root": "maior", "variants": ["maj", "major"],
        "origin": "拉丁语 maior（更大的，magnus 的比较级）；maiestas（尊大、威仪）由此出，"
                  "英语 major/majority/majesty 同循此路",
        "core_concept": "the greater of what is compared / 相比之下更大的那一方",
        "core_image": "一棵树上最粗那根枝，别的枝都从它分出去",
        "english_definition": "greater, larger",
    },
    "concept": {
        "id": "concept-maior-greater", "concept": "the greater of what is compared",
        "chinese": "更大一方", "core_image": "树上最粗那根枝，别的枝都由它分出",
        "root_ids": ["maior"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("major", "maior", "adjective", "/ˈmeɪdʒə(r)/",
          "maior（更大的）→ 相比之下更要紧的；名词指主修的那一门",
          "拉丁语 maior（更大的），magnus（大）的比较级",
          "greater in size or importance; a student's main subject",
          "the thicker branch the others hang off – 别的枝都挂在它上头的那一根",
          "顺着树身往上看，最粗那根撑住了大半个树冠",
          ["主要的", "重大的", "专业"],
          ["This is a major problem for us.", "She chose history as her major."],
          ["principal", "chief"], ["minor"],
          ["majority", "majesty"],
          ["主要的/重大的：相比之下更大更要紧的那一方", "专业：所修各门里作主干的那一门"],
          "maior（更大的）→ 别的都挂在它上头的那一根"),
        W("majority", "maior", "noun", "/məˈdʒɒrəti/",
          "major（更大的）+ -ity → 更大的那一部分 → 多数",
          "法语 majorité，来自中世纪拉丁语 maioritas ← maior",
          "the greater number or part of a group",
          "the side that has the greater count – 数下来更多的那一边",
          "举手一数，一边的手明显比另一边密",
          ["大多数", "多数"],
          ["The majority voted in favour.", "A majority of students agreed."],
          ["most", "bulk"], ["minority"],
          ["major", "majesty"],
          ["大多数/多数：数下来更多的那一边"],
          "major（更大的）+ -ity → 数下来更多那一边"),
        W("majesty", "maior", "noun", "/ˈmædʒəsti/",
          "maior（更大）→ maiestas（尊大）→ 令人仰视的气派；亦作君主尊称",
          "古法语 majeste，来自拉丁语 maiestas（威严、尊大）← maior",
          "impressive dignity or grandeur; a title for a king or queen",
          "the bearing of one seated higher than all present – 坐得比在场所有人都高的那份气派",
          "台阶尽头那个座位高出一截，底下的人都得抬头看",
          ["威严", "壮丽", "陛下"],
          ["The mountains rose in silent majesty.", "Her Majesty will arrive at noon."],
          ["grandeur", "dignity"], [],
          ["major", "majority"],
          ["威严/壮丽：令人须仰视的那份气派", "陛下：以此气派作君主的尊称"],
          "maior（更大）→ maiestas（尊大）→ 令人仰视的气派"),
    ],
})

# ---------- numerus（数目）----------
families.append({
    "root": {
        "id": "numerus", "root": "numerus", "variants": ["numer", "num"],
        "origin": "拉丁语 numerus（数目、数），numerare（计数）由此出；"
                  "英语 number 同源，本族收 -numer- 一支的派生词",
        "core_concept": "the count that can be told off one by one / 能一个一个点数出来的数目",
        "core_image": "手指点着东西一件件数过去，嘴里跟着报数",
        "english_definition": "number, count",
    },
    "concept": {
        "id": "concept-numerus-count", "concept": "the count that can be told off one by one",
        "chinese": "逐一点数", "core_image": "手指点着一件件数过去，嘴里跟着报数",
        "root_ids": ["numerus"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("numerous", "numerus", "adjective", "/ˈnjuːmərəs/",
          "numer（数目）+ -ous（多…的）→ 数目多的",
          "拉丁语 numerosus（数目多的），来自 numerus（数目）",
          "existing in great numbers; many",
          "so many that the counting runs long – 点起来要数好一阵",
          "屋檐下的燕子一排接一排，数到后头就乱了",
          ["许多的", "众多的"],
          ["She has numerous friends abroad.", "We met on numerous occasions."],
          ["many", "abundant"], ["few"],
          ["numerical", "innumerable"],
          ["许多的/众多的：数目多、点起来要数好一阵"],
          "numer（数目）+ -ous（多…的）→ 数目多的"),
        W("numerical", "numerus", "adjective", "/njuːˈmerɪkl/",
          "numer（数目）+ -ical（…的）→ 用数目表示的、按数计的",
          "英语 numerical，来自中世纪拉丁语 numericus ← numerus",
          "expressed in numbers; relating to numbers",
          "set down as counts rather than words – 记成数目而非文字",
          "表格里每一栏都换成了阿拉伯记号，一列列排下去",
          ["数字的", "数值的"],
          ["Put the files in numerical order.", "The numerical results agree with theory."],
          ["quantitative", "arithmetical"], [],
          ["numerous", "innumerable"],
          ["数字的/数值的：以数目记下、按数计的"],
          "numer（数目）+ -ical → 以数目记下的"),
        W("innumerable", "numerus", "adjective", "/ɪˈnjuːmərəbl/",
          "in-（不）+ numer（数）+ -able（可…的）→ 数不过来的",
          "拉丁语 innumerabilis（数不清的），来自 in-＋numerare（计数）← numerus",
          "too many to be counted",
          "more than the fingers can keep up with – 手指跟不上、点不完",
          "沙从指缝里漏下去，颗数根本跟不上",
          ["数不清的", "无数的"],
          ["He made innumerable attempts.", "Innumerable stars filled the sky."],
          ["countless", "myriad"], ["few"],
          ["numerous", "numerical"],
          ["数不清的/无数的：多到点不过来"],
          "in-（不）+ numer（数）+ -able → 数不过来的"),
    ],
})

# ---------- logos（言说条理）----------
families.append({
    "root": {
        "id": "logos", "root": "logos", "variants": ["log", "logy", "logue"],
        "origin": "希腊语 logos（话语、道理、条理），legein（说）的名词形；"
                  "-logy 作学科后缀即「关于某物的条理」。"
                  "vetted 族名作 olog，那是词干提取切出的假词根：真正共用的是 logos",
        "core_concept": "words that give an account of something / 把一件事说出条理来",
        "core_image": "一个人开口把事情从头理到尾，听的人跟得上",
        "english_definition": "word, speech, reasoned account",
    },
    "concept": {
        "id": "concept-logos-account", "concept": "words that give an account of something",
        "chinese": "说出条理", "core_image": "开口把事情从头理到尾，听的人跟得上",
        "root_ids": ["logos"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("apology", "logos", "noun", "/əˈpɒlədʒi/",
          "apo-（离开、退开）+ log（说辞）→ 退一步把话说开 → 认过的说辞",
          "希腊语 apologia（辩解、答辩），来自 apo（离）＋logos（话语）",
          "a statement saying one is sorry for a fault",
          "stepping back and putting the fault into words – 退一步，把自己的不是说出口",
          "他往后退了半步，把话头接过来，承认是自己没办好",
          ["道歉", "歉意", "辩解"],
          ["He offered a sincere apology.", "She made no apology for her view."],
          ["regret", "excuse"], [],
          ["apologise", "biology"],
          ["道歉/歉意：退一步把自己的不是说出口", "辩解：同样是把话说开，为自己申说"],
          "apo-（退开）+ log（说辞）→ 退一步把话说开"),
        W("apologise", "logos", "verb", "/əˈpɒlədʒaɪz/",
          "apology（认过的说辞）+ -ise（使、行）→ 把那番话说出来",
          "希腊语 apologizesthai（申说），来自 apologia ← apo＋logos",
          "to say that one is sorry for a fault",
          "putting the stepping-back into actual words – 把那退一步的意思真说出口",
          "他站起来，当着众人把那句话讲了出来",
          ["道歉", "认错"],
          ["He apologised for being late.", "She refused to apologise."],
          ["regret", "atone"], [],
          ["apology", "biology"],
          ["道歉/认错：把退一步认过的话说出口"],
          "apology（认过说辞）+ -ise → 把那番话说出口"),
        W("biology", "logos", "noun", "/baɪˈɒlədʒi/",
          "bio-（生命）+ -logy（条理、学科）→ 讲清生命之理的那门学问",
          "希腊语 bios（生命）＋logos（条理）合成，19 世纪造词",
          "the scientific study of living things",
          "the account given of how living things work – 把活物的道理说清的那一套",
          "从一片叶脉讲到血液怎么走，条理一路排下来",
          ["生物学"],
          ["She teaches biology at the college.", "Marine biology is his field."],
          [], [],
          ["apology", "apologise"],
          ["生物学：把活物的道理说出条理的那门学问"],
          "bio-（生命）+ -logy（条理）→ 讲清生命之理的学问"),
    ],
})

# ================= 补词：并入已建模 ponere 根 =================
# post/postage/posture 均出拉丁 ponere（放置）的 positum 一支。
# 门柱义的 post 来自拉丁 postis，与 ponere 不同源，故不收该义。
additions = [
    W("post", "ponere", "noun", "/pəʊst/",
      "positum（被放置的）→ 沿路安置的驿站 → 邮政；被安置的位子 → 职位",
      "古法语 poste，来自意大利语 posta ← 拉丁语 posita/ponere（放置）；"
      "驿站本义是「沿途置马之处」。门柱义的 post 另出拉丁 postis，不在此族",
      "the system that carries letters; a job or official position",
      "a station set along the way, and by extension a place one is set in – 沿途安置的那一站，引申为人被安在的位子",
      "沿路每隔一程设一处，换马换人，信件一路递下去",
      ["邮政", "邮件", "职位"],
      ["Send it by post, not by email.", "She applied for a teaching post."],
      ["mail", "position"], [],
      ["position", "postage"],
      ["邮政/邮件：靠沿途置站接力递送的那套", "职位：人被安置进去的那个位子"],
      "positum（被放置的）→ 沿途置站 → 邮政；被安的位子 → 职位"),
    W("postage", "ponere", "noun", "/ˈpəʊstɪdʒ/",
      "post（驿站接力）+ -age（费用）→ 走这套接力所付的钱",
      "英语 postage，由 post ← 拉丁语 ponere（放置）加 -age 构成",
      "the money charged for sending something by post",
      "what one pays for the relay of stations to carry it – 为那套接力递送付的钱",
      "柜台上称过重量，贴上几枚小纸片才收下",
      ["邮费", "邮资"],
      ["Postage costs have gone up again.", "The price includes postage."],
      ["fee", "charge"], [],
      ["post", "position"],
      ["邮费/邮资：为沿途接力递送所付的钱"],
      "post（驿站接力）+ -age（费用）→ 走这套递送付的钱"),
    W("posture", "ponere", "noun", "/ˈpɒstʃə(r)/",
      "positura（放置的样子）→ 身体摆放的姿态",
      "法语 posture，来自意大利语 postura ← 拉丁语 positura（安放、位置）← ponere",
      "the way a person holds their body; an attitude taken up",
      "how the body is set and held in place – 身体被摆放、端住的那个样子",
      "他把背挺直、肩往后收，整个人的架子就稳住了",
      ["姿势", "体态", "姿态"],
      ["Good posture prevents back pain.", "The country took a defensive posture."],
      ["stance", "bearing"], [],
      ["position", "post"],
      ["姿势/体态：身体摆放端住的那个样子", "姿态：对外摆出的那副架势"],
      "positura（放置的样子）→ 身体摆放端住的样子"),
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
