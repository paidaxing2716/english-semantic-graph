#!/usr/bin/env python3
"""Generate batch51: 反查第二批 30 词，全部补进已建模词根，不新建根。

含上一批故意跳过的 planus / polis 两族——它们混了不少同形异源词，单独一批细过。

  planus（平）        plain / explain / aeroplane
  polis（城邦）       police / policeman / policy / metropolitan
  spect（看）         spectacular / spectrum / despise / irrespective
  graphein（刻写）    telegraph / biography / bibliography / geography
  premere（压）       print / blueprint / repression
  ponere（放置）      positive / deposit
  quir（寻求）        question / questionnaire / acquisition
  gradus（步）        progress / progressive / congress
  littera（字母）     literature
  ferre（带）         circumference / conference / interference

【本批剔除的同形异源候选，勿再捡回】
  planet   ← 希腊 planētēs（游走的星），与 planus（平）无关
  complain / complaint ← 拉丁 plangere（拍打、哀号），不是 planus。
           拼写像 plain 纯属巧合，两者中古法语阶段才撞到一起
  polish / polite ← 拉丁 polire（磨光），不是 polis（城邦）
  pound    ← 古英语 pund（重量单位，日耳曼源），不是 ponere
  litter   ← 古法语 litiere（卧铺）← 拉丁 lectus（床），不是 littera（字母）
  glitter  ← 古诺斯语 glitra，日耳曼源
  metropolitan 上一批从 metron（量度）名下剔掉是对的——它是 mētēr（母）+ polis，
           量度那支无关；但它确实含 polis，故本批收进 polis 族

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch51.json"


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


words = []

# ================= planus（平）=================
words += [
    W("plain", "planus", "adjective", "/pleɪn/",
      "planus（平的）→ 表面无起伏 → 不加修饰的、一望便知的；名词指平地",
      "古法语 plain，来自拉丁语 planus（平的）",
      "simple and without decoration; easy to understand; a large flat area",
      "a surface with nothing raised on it to catch the eye – 面上不起花样，一眼扫得到底",
      "一张白桌面从这头看到那头，什么摆件都没有",
      ["朴素的", "清楚的", "平原"],
      ["She wore a plain grey dress.", "It is plain that he was lying."],
      ["simple", "obvious"], ["fancy", "obscure"],
      ["explain", "plan"],
      ["朴素的：面上不加花样", "清楚的：摊得平、一眼看到底", "平原：地面无起伏的那一片"],
      "planus（平的）→ 面上不起花样、一眼见底"),
    W("explain", "planus", "verb", "/ɪkˈspleɪn/",
      "ex-（出来）+ plain（平）→ 把褶皱摊平摊开 → 讲清楚",
      "拉丁语 explanare（摊平、阐明），来自 ex＋planus（平的）",
      "to make something clear by describing it in detail",
      "smoothing the folds out so the whole lies open – 把折起来的一层层摊开，全貌就露出来",
      "他把揉成一团的那张纸一点点抹开，字迹才连得起来",
      ["解释", "说明", "阐明"],
      ["Please explain how it works.", "She explained her reasons at length."],
      ["clarify", "describe"], ["confuse"],
      ["explanation", "plain"],
      ["解释/说明/阐明：把褶皱摊平、使人看清"],
      "ex-（出来）+ plain（平）→ 把褶子摊开讲清"),
    W("aeroplane", "planus", "noun", "/ˈeərəpleɪn/",
      "aero-（空气）+ plane（平面）→ 靠平展翼面浮在空气里的那件东西",
      "法语 aéroplane，由希腊 aēr（空气）＋拉丁 planus（平面）合成",
      "a vehicle with wings and engines that flies through the air",
      "the craft held up by two flat faces pressed against the air – 靠两片平展的面撑住空气而浮起的器械",
      "两侧那两片薄薄的面一斜，整个机身就抬了起来",
      ["飞机"],
      ["The aeroplane took off on time.", "He has never been on an aeroplane."],
      ["aircraft", "plane"], [],
      ["plane", "plain"],
      ["飞机：靠平展翼面撑住空气而飞的器械"],
      "aero-（空气）+ plane（平面）→ 靠平展翼面浮起"),
]

# ================= polis（城邦）=================
words += [
    W("police", "polis", "noun", "/pəˈliːs/",
      "polis（城邦）→ politia（城邦治理）→ 维持城中秩序的那班人",
      "法语 police，来自拉丁语 politia（治理）← 希腊语 politeia ← polis（城邦）",
      "the official force that keeps order and enforces the law",
      "the body charged with keeping the city's order – 受命看住全城秩序的那班人",
      "街口那几个人一站，闹哄哄的人群自己让出条路",
      ["警察", "警方"],
      ["The police arrived within minutes.", "She called the police at once."],
      ["officer", "guard"], [],
      ["policeman", "policy"],
      ["警察/警方：受命维持城中秩序的那班人"],
      "polis（城邦）→ politia（治理）→ 维持城中秩序者"),
    W("policeman", "polis", "noun", "/pəˈliːsmən/",
      "police（维持秩序者）+ man（人）→ 其中一名",
      "英语复合词 police＋man，police ← 拉丁语 politia ← 希腊语 polis",
      "a male member of the police force",
      "one man out of the body that keeps order – 看守秩序那班人里的一名男性",
      "路口那一位抬手一比，车流就停住了",
      ["警察", "男警"],
      ["A policeman directed the traffic.", "The policeman took down her name."],
      ["guard", "police"], [],
      ["police", "policy"],
      ["警察/男警：维持秩序那班人里的一名男性"],
      "police（维持秩序者）+ man → 其中一名"),
    W("policy", "polis", "noun", "/ˈpɒləsi/",
      "polis（城邦）→ politia（治理）→ 治理所定的那套方针",
      "古法语 policie（治理），来自拉丁语 politia ← 希腊语 politeia ← polis",
      "a plan of action agreed by a government or organization",
      "the settled course by which a body is run – 治事者定下来照办的那条路子",
      "议事厅定下一条，往后各处照着这条办",
      ["政策", "方针", "保单"],
      ["The government changed its policy.", "Read your insurance policy carefully."],
      ["strategy", "guideline"], [],
      ["police", "political"],
      ["政策/方针：治事所定、往后照办的那条路子", "保单：把承保条款定死的那纸文书"],
      "polis（城邦）→ politia（治理）→ 所定的方针"),
    W("metropolitan", "polis", "adjective", "/ˌmetrəˈpɒlɪtən/",
      "metro-（mētēr 母）+ polit（城邦）+ -an → 属于母城、大城的",
      "晚期拉丁语 metropolitanus，来自希腊语 mētropolis（母城）← mētēr（母）＋polis（城邦）；"
      "与 metron（量度）无关，上一批从 metron 名下剔除是对的",
      "relating to a large city and the area around it",
      "belonging to the mother-city that other towns grew out of – 属于那座生出周边诸镇的母城",
      "地铁线从那座大城摊开，一路连出去几十个镇子",
      ["大都市的", "大城市的"],
      ["He works for the metropolitan council.", "It is a metropolitan area of ten million."],
      ["city", "civic"], ["rural"],
      ["police", "policy"],
      ["大都市的/大城市的：属于那座生出周边诸镇的母城"],
      "metro-（母）+ polit（城邦）→ 属于母城、大城的"),
]

# ================= spect（看）=================
words += [
    W("spectacular", "spect", "adjective", "/spekˈtækjələ(r)/",
      "spect（看）+ -acular → 值得停下来看的 → 壮观",
      "拉丁语 spectaculum（可观之物），来自 spectare（观看）← specere（看）",
      "very impressive to look at; strikingly great",
      "the sight that stops the eye and holds it – 让眼睛停住、挪不开的那种景象",
      "转过山口，眼前那一片让所有人都收住了脚",
      ["壮观的", "惊人的"],
      ["The view was spectacular.", "She made a spectacular recovery."],
      ["striking", "impressive"], ["dull"],
      ["spectrum", "inspect"],
      ["壮观的/惊人的：让眼睛停住挪不开的那种"],
      "spect（看）+ -acular → 值得停下来看的"),
    W("spectrum", "spect", "noun", "/ˈspektrəm/",
      "spect（看）+ -rum → 呈给眼睛看的那一整条 → 光谱、范围",
      "拉丁语 spectrum（显现、影像），来自 specere（看）",
      "the band of colours light splits into; a full range of related things",
      "the whole band laid out for the eye to run along – 摊开来让眼睛一路扫过去的那一整条",
      "光穿过棱镜，摊出一条从红到紫的带子",
      ["光谱", "范围", "系列"],
      ["Sunlight splits into a spectrum.", "Opinions cover the whole spectrum."],
      ["range", "band"], [],
      ["spectacular", "inspect"],
      ["光谱：光摊开成的那一条色带", "范围/系列：同类事物摊开成的整条幅面"],
      "spect（看）+ -rum → 呈给眼睛的那一整条"),
    W("despise", "spect", "verb", "/dɪˈspaɪz/",
      "de-（往下）+ spise（看）→ 从上往下看 → 鄙视",
      "古法语 despis-，来自拉丁语 despicere（俯视、轻蔑）← de＋specere（看）",
      "to feel a strong dislike and lack of respect for",
      "looking down on a thing from above – 眼光自上往下落在那物上",
      "他下巴一抬，眼光从鼻梁上头扫过去",
      ["鄙视", "轻视"],
      ["He despised their dishonesty.", "She despises gossip of any kind."],
      ["scorn", "disdain"], ["admire", "respect"],
      ["spectacular", "inspect"],
      ["鄙视/轻视：眼光自上往下落在那物上"],
      "de-（往下）+ spise（看）→ 从上往下看"),
    W("irrespective", "spect", "adjective", "/ˌɪrɪˈspektɪv/",
      "ir-（不）+ respect（回看顾及）+ -ive → 不回头看那一头 → 不顾、无论",
      "英语 irrespective，由 ir-＋respective ← 拉丁语 respicere（回看）← re＋specere",
      "not taking something into account; regardless of",
      "walking on without turning the eye back to it – 眼睛不往那边回一下，照旧往前",
      "旁边情形如何他一眼没回，脚步照原样走",
      ["不顾的", "无论的"],
      ["Open to all, irrespective of age.", "It applies irrespective of cost."],
      ["regardless", "notwithstanding"], [],
      ["spectacular", "despise"],
      ["不顾的/无论的：眼睛不回看那一头，照旧进行"],
      "ir-（不）+ respect（回看）→ 不回头看那一头"),
]

# ================= graphein（刻写）=================
words += [
    W("biography", "graphein", "noun", "/baɪˈɒɡrəfi/",
      "bio-（生命）+ graph（写）+ -y → 把一个人一生写下来的那本",
      "希腊语 bios（生命）＋graphein（书写），17 世纪造词",
      "the written story of a person's life",
      "one life set down on paper from start to end – 把一个人从头到尾写在纸上",
      "从出生那页翻到最后一页，全是同一个人的事",
      ["传记"],
      ["She wrote a biography of her father.", "The biography runs to 600 pages."],
      ["account", "writing"], [],
      ["bibliography", "geography"],
      ["传记：把一个人一生写下来的那本"],
      "bio-（生命）+ graph（写）→ 把一生写下来"),
    W("bibliography", "graphein", "noun", "/ˌbɪbliˈɒɡrəfi/",
      "biblio-（书）+ graph（写）+ -y → 把所引各书列写出来的那一份",
      "希腊语 biblion（书）＋graphein（书写）",
      "a list of the books and sources used in a piece of work",
      "the roll of every book one leaned on, written out – 把倚仗过的书一本本写成清单",
      "论文末尾几页，一行一本地列着看过的书",
      ["参考书目", "文献目录"],
      ["Add the sources to your bibliography.", "The bibliography lists forty titles."],
      ["writing", "account"], [],
      ["biography", "geography"],
      ["参考书目/文献目录：把所引各书列写出来的那一份"],
      "biblio-（书）+ graph（写）→ 把所引各书列写出来"),
    W("geography", "graphein", "noun", "/dʒiˈɒɡrəfi/",
      "geo-（地）+ graph（写）+ -y → 把大地描写下来的那门学问",
      "希腊语 geōgraphia（描写大地），来自 gē（地）＋graphein（书写）",
      "the study of the earth's surface, climate, and peoples",
      "putting the face of the land down on paper – 把大地的样貌描到纸上",
      "山川河道一笔笔画进图里，纸上就成了那片地",
      ["地理", "地理学", "地形"],
      ["She teaches geography at the school.", "The geography of the region is rugged."],
      ["land", "map"], [],
      ["biography", "telegraph"],
      ["地理/地理学：把大地样貌描写下来的那门学问", "地形：某地起伏走势的那副样貌"],
      "geo-（地）+ graph（写）→ 把大地描到纸上"),
    W("telegraph", "graphein", "noun", "/ˈtelɪɡrɑːf/",
      "tele-（远）+ graph（写）→ 把字写到远处去的那套装置",
      "法语 télégraphe，由希腊 tēle（远）＋graphein（书写）合成，19 世纪造词",
      "a system for sending messages over distance by electric signal",
      "writing that lands far from the hand that made it – 手在此处落笔，字却出现在远处",
      "这头按下几下长短，那头纸带上就吐出一串记号",
      ["电报", "电报机"],
      ["The news came by telegraph.", "He sent a telegraph from the port."],
      ["cable", "wire"], [],
      ["geography", "biography"],
      ["电报/电报机：把字送到远处去的那套装置"],
      "tele-（远）+ graph（写）→ 把字写到远处去"),
]

# ================= premere（压）=================
words += [
    W("print", "premere", "verb", "/prɪnt/",
      "premere（压）→ preinte（压出的痕）→ 压出字迹 → 印刷",
      "古法语 preinte（压痕），来自 preindre ← 拉丁语 premere（压）",
      "to produce text or pictures by pressing ink onto paper",
      "the mark left where something was pressed down – 压下去之后留在那儿的痕",
      "版子往纸上一压，抬起来时字就留住了",
      ["印刷", "印", "字迹"],
      ["They printed a thousand copies.", "Print your name in capitals."],
      ["publish", "impress"], [],
      ["blueprint", "pressure"],
      ["印刷/印：压下去把字留在纸上", "字迹：压出来的那些痕"],
      "premere（压）→ 压出痕迹 → 印刷"),
    W("blueprint", "premere", "noun", "/ˈbluːprɪnt/",
      "blue（蓝）+ print（压印）→ 蓝底压印出的图 → 蓝图、方案",
      "英语复合词 blue＋print；旧时晒图工艺出蓝底白线，print ← 拉丁语 premere",
      "a technical drawing of a plan; a detailed scheme",
      "the pressed-out drawing everything is built from – 压印出来、照着它造的那张图",
      "摊开那张蓝底的图纸，每根梁的位置都标着",
      ["蓝图", "设计图", "方案"],
      ["The architect showed us the blueprint.", "This is a blueprint for reform."],
      ["plan", "scheme"], [],
      ["print", "pressure"],
      ["蓝图/设计图：压印出来、照着施工的那张图", "方案：同样作依据的那套设想"],
      "blue（蓝）+ print（压印）→ 蓝底压印的图"),
    W("repression", "premere", "noun", "/rɪˈpreʃn/",
      "re-（往回）+ press（压）+ -ion → 往回压住 → 镇压、压抑",
      "拉丁语 repressio，来自 reprimere（压回）← re＋premere（压）",
      "the act of keeping something down by force or by will",
      "pressing a thing back down so it cannot rise – 把往上冒的按回去，不许起来",
      "刚要抬头的那一下被一只手按了回去",
      ["镇压", "压抑", "抑制"],
      ["The repression of protest drew criticism.", "Years of repression left their mark."],
      ["control", "restraint"], ["freedom"],
      ["print", "pressure"],
      ["镇压：用力把动作按回去", "压抑/抑制：把情绪或冲动按住不许冒头"],
      "re-（往回）+ press（压）→ 往回按住不许起"),
]

# ================= ponere（放置）=================
words += [
    W("positive", "ponere", "adjective", "/ˈpɒzətɪv/",
      "posit（放定）+ -ive → 已经放定、不再摇摆的 → 确定的、肯定的",
      "拉丁语 positivus（明定的），来自 positus（ponere 的过去分词）",
      "certain and confident; showing agreement; greater than zero",
      "set down firmly so it no longer wavers – 已经放定，不再来回移动",
      "他把那枚棋子按在格里松手，再没挪动过",
      ["积极的", "肯定的", "确定的"],
      ["She has a positive attitude.", "The test came back positive."],
      ["certain", "sure"], ["negative", "doubt"],
      ["deposit", "position"],
      ["肯定的/确定的：已经放定、不再摇摆", "积极的：心气上同样是定住往前的那一头"],
      "posit（放定）+ -ive → 放定了不再摇摆"),
    W("deposit", "ponere", "verb", "/dɪˈpɒzɪt/",
      "de-（向下）+ posit（放）→ 往下放好搁着 → 存放、押金",
      "拉丁语 depositum（寄存物），来自 deponere（放下）← de＋ponere",
      "to put something somewhere for safe keeping; money paid as security",
      "setting a thing down and leaving it in keeping – 往下放好，就搁在那儿托人看着",
      "他把袋子往柜台里一放，换回一张凭条",
      ["存放", "存款", "押金"],
      ["She deposited the cash at the bank.", "We paid a deposit on the flat."],
      ["store", "saving"], ["withdraw"],
      ["positive", "position"],
      ["存放/存款：往下放好交人看着", "押金：先放下作担保的那笔钱"],
      "de-（向下）+ posit（放）→ 放下搁着托管"),
]

# ================= quir（quaerere 寻求）=================
words += [
    W("question", "quir", "noun", "/ˈkwestʃən/",
      "quest（寻求）+ -ion → 为求答案而发出的那一句",
      "古法语 question，来自拉丁语 quaestio（询问）← quaerere（寻找、探求）",
      "a sentence asked in order to get information; a matter in doubt",
      "the sentence sent out to fetch an answer back – 抛出去、指望换回一个答案的那句话",
      "他抛出一句，屋里几个人都抬头等着谁接",
      ["问题", "疑问", "询问"],
      ["She asked a difficult question.", "There is no question of his honesty."],
      ["query", "inquiry"], ["answer"],
      ["questionnaire", "acquisition"],
      ["问题/询问：为求答案而发出的那一句", "疑问：尚未有着落、悬着的那一处"],
      "quest（寻求）+ -ion → 为求答案发出的那句"),
    W("questionnaire", "quir", "noun", "/ˌkwestʃəˈneə(r)/",
      "question（问）+ -naire（成套）→ 排成一套发出去的问句",
      "法语 questionnaire，来自 question ← 拉丁语 quaerere",
      "a printed list of questions used to gather information",
      "a run of asked sentences set out in order to be answered – 一整串问句排开等人逐条作答",
      "纸上一行一行都留着空格，等着人挨着填",
      ["问卷", "调查表"],
      ["Please fill in the questionnaire.", "We sent questionnaires to 200 people."],
      ["survey", "form"], [],
      ["question", "acquisition"],
      ["问卷/调查表：排成一套、发出去等人逐条作答的问句"],
      "question（问）+ -naire（成套）→ 排成一套的问句"),
    W("acquisition", "quir", "noun", "/ˌækwɪˈzɪʃn/",
      "ac-（ad- 朝）+ quisit（求得）+ -ion → 求而得之 → 获得、所得之物",
      "拉丁语 acquisitio（获得），来自 acquirere（取得）← ad＋quaerere（求）",
      "the act of getting something; a thing obtained",
      "what the seeking finally brings into hand – 一路求下来，终于拿到手的那个",
      "找了半年，终于把那件东西拿到手里",
      ["获得", "收购", "所得物"],
      ["The acquisition took two years.", "The painting is her latest acquisition."],
      ["purchase", "gain"], ["loss"],
      ["question", "require"],
      ["获得：求而终于拿到手", "收购：以此手段把公司或资产求到手", "所得物：求来的那件东西"],
      "ac-（朝）+ quisit（求得）→ 求而得之"),
]

# ================= gradus（步）=================
words += [
    W("progress", "gradus", "noun", "/ˈprəʊɡres/",
      "pro-（往前）+ gress（走）→ 一步步往前 → 进展",
      "拉丁语 progressus（前行），来自 progredi（前进）← pro＋gradi（走）",
      "movement forward or improvement over time",
      "one step set down ahead of the last – 一步落在上一步前头",
      "脚印一个接一个往前排，回头看已走出一段",
      ["进展", "进步", "前进"],
      ["We are making good progress.", "The work progressed slowly."],
      ["advance", "improvement"], ["decline"],
      ["progressive", "congress"],
      ["进展/进步：一步步落在前头、往前推", "前进：脚步实际向前那一动"],
      "pro-（往前）+ gress（走）→ 一步落在前头"),
    W("progressive", "gradus", "adjective", "/prəˈɡresɪv/",
      "progress（前行）+ -ive → 一路往前走的 → 渐进的、主张改革的",
      "英语 progressive，来自 progress ← 拉丁语 progredi",
      "happening gradually; favouring reform and new ideas",
      "keeping the steps coming one after another – 步子一个接一个不停下来",
      "水位一格一格往上抬，每天都比前一天高一点",
      ["渐进的", "进步的", "前进的"],
      ["The disease is progressive.", "She holds progressive views."],
      ["gradual", "steady"], ["conservative"],
      ["progress", "congress"],
      ["渐进的：步子一个接一个不停下来", "进步的：主张往前走、求改革的那一头"],
      "progress（前行）+ -ive → 步子接连不停"),
    W("congress", "gradus", "noun", "/ˈkɒŋɡres/",
      "con-（一同）+ gress（走）→ 各方走到一处 → 集会、国会",
      "拉丁语 congressus（会合），来自 congredi（走到一起）← con＋gradi（走）",
      "a formal meeting; the national law-making body of some countries",
      "steps from many directions ending in one room – 各路脚步走到同一间屋里",
      "各地的人一路赶来，最后都进了同一间厅",
      ["代表大会", "国会", "会议"],
      ["The congress meets every autumn.", "Congress passed the bill."],
      ["assembly", "parliament"], [],
      ["progress", "progressive"],
      ["代表大会/会议：各方走到一处开的会", "国会：由此制度化而成的立法机构"],
      "con-（一同）+ gress（走）→ 各方走到一处"),
]

# ================= littera（字母）=================
words += [
    W("literature", "littera", "noun", "/ˈlɪtrətʃə(r)/",
      "litter（字母、文字）+ -ature → 用文字写成的那一整片 → 文学、文献",
      "拉丁语 litteratura（书写、学问），来自 littera（字母）",
      "written works valued as art; the writings on a subject",
      "the body of what has been set down in letters – 用文字写下来、积成的那一整片",
      "架上一层层排开，全是用字写成的东西",
      ["文学", "文献", "著作"],
      ["She studies French literature.", "Read the literature on the topic first."],
      ["writing", "text"], [],
      ["literary", "literacy"],
      ["文学/著作：用文字写成、可当艺术看的那些作品", "文献：某一题目下写下来的全部材料"],
      "litter（文字）+ -ature → 用文字写成的那一整片"),
]

# ================= ferre（带）=================
words += [
    W("conference", "ferre", "noun", "/ˈkɒnfərəns/",
      "con-（一同）+ fer（带）+ -ence → 各方把话带到一处 → 会议",
      "中世纪拉丁语 conferentia，来自 conferre（聚拢、商议）← con＋ferre（带）",
      "a formal meeting for discussion, often lasting days",
      "everyone carrying their piece to the same table – 各人把自己那份话带到同一张桌上",
      "几十个人从各处赶来，把手里的材料摊到一张桌上",
      ["会议", "会谈", "研讨会"],
      ["The conference lasts three days.", "She spoke at an international conference."],
      ["meeting", "convention"], [],
      ["circumference", "interference"],
      ["会议/会谈：各方把话带到一处商议", "研讨会：以此形式专议某题目的那种会"],
      "con-（一同）+ fer（带）→ 各方把话带到一处"),
    W("circumference", "ferre", "noun", "/səˈkʌmfərəns/",
      "circum-（绕）+ fer（带）+ -ence → 绕一圈带过去的那条线 → 周长",
      "拉丁语 circumferentia（绕行的线），来自 circumferre（环绕）← circum＋ferre",
      "the distance around the edge of a circle",
      "the line carried all the way round back to its start – 绕着边一路带回起点的那条线",
      "笔沿着圆边走一整圈，回到落笔那一点",
      ["圆周", "周长"],
      ["Measure the circumference of the trunk.", "The lake is 5 km in circumference."],
      ["boundary", "edge"], ["diameter"],
      ["conference", "interference"],
      ["圆周/周长：绕边一路带回起点的那条线"],
      "circum-（绕）+ fer（带）→ 绕一圈带回起点"),
    W("interference", "ferre", "noun", "/ˌɪntəˈfɪərəns/",
      "inter-（在中间）+ fer（带）+ -ence → 把自己插到中间去 → 干扰",
      "英语 interference，来自 interfere ← 古法语 s'entreferir（互击）← 拉丁 inter＋ferire",
      "the act of getting involved where one is not wanted; disruption of a signal",
      "something carried in between so the two can no longer meet cleanly – 有东西插进中间，两头就接不干净了",
      "两人正说着，第三个人的声音插进中间，谁也听不清了",
      ["干扰", "干涉", "妨碍"],
      ["He resented her interference.", "Radio interference spoiled the broadcast."],
      ["block", "disruption"], ["assistance"],
      ["conference", "circumference"],
      ["干涉/妨碍：把自己插到中间去搅一脚", "干扰：信号里插进杂物、传不干净"],
      "inter-（在中间）+ fer（带）→ 插到中间搅一脚"),
]

# ================= 组装 =================
# 本批不新建词根/概念/语义域，全部补进已建模的十个根。
# ---- 生成期自检：review.py check 不查 Q12，合并后 validate.py 才查 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"

assert len(words) == 30, len(words)
assert len({w["id"] for w in words}) == 30, "词条 id 有重复"

OUT.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=2) + "\n",
               encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words，全部补进已建模词根，无新根")
