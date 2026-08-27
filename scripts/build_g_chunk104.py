#!/usr/bin/env python3
"""Build drafts/g_chunk104.tsv by list-join (never Write) so trailing tabs survive.

W rows = 15 cols, R rows = 10 cols, asserted before write.
Also dry-runs the etymology screen's key matching so origins can be fixed here.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "drafts" / "g_chunk104.tsv"

R_ROWS = []
W_ROWS = []

# ---------------------------------------------------------------- new root
R_ROWS.append([
    "R",
    "hodos",
    # variants 留空是刻意的：族里可见的词干是 "od"（episode/method/period），
    # 但它在库中 3813 词里命中 47 个（"ode" 命中 9 个），真成员只 3 个——
    # 比规格里 tangere 把 tain 列进 variants 那次（1 真 : 20 假）更糟。
    # 照那条实测提示，这类该标 noisy 而非当正常变体用；R 行没有 noisy_variants
    # 这一列，故留空，把"三词共享 od"这个事实放在 origin 里保住。
    "",
    "希腊语 hodos（路、走法）；epeisodion 是 epi-（另加）+ eis（进入）+ hodos，"
    "指正戏之外另插进来的一段；methodos（追着走的那条路）、periodos（绕一圈走回来）同出此支",
    "a way along which one travels / 一条走的路",
    "脚下一条路伸出去，顺着它走才到得了，中途插进来的也算一段",
    "a way, a road, a course of travel",
    "way",
    "一条路",
    "domain-transfer",
])


def W(word, pos, ph, rids, logic, origin, native, image, zh, ex, concept,
      exps="", hint="", colloc=""):
    W_ROWS.append(["W", word, pos, ph, rids, logic, origin, native, image, zh,
                   ex, concept, exps, hint, colloc])


# ============================== A 档 ==============================
W("enforce", "verb", "/ɪnˈfɔːs/", "fortis",
  "en-（使成为）+ force（fortis 强力）→ 在规矩背后加上一股力 → 使它落到实处",
  "古法语 enforcier：en-（使）+ force ← 通俗拉丁语 fortia ← 拉丁语 fortis（强壮的、有力的）；"
  "与库中 fortuna（命运）不同支",
  "to make people obey a rule, or to make something happen by force",
  "路口立起一块牌子，旁边站着人，谁想绕过去都被拦下来",
  "执行/强制/加强",
  "Police enforce the speed limit here.|The court will enforce the agreement.",
  "putting force behind a rule – 在规矩背后加上一股力，使它落到实处",
  "执行：让写在纸上的条文真的发生|强制：对方不愿意也得照办，力从外面加上去|"
  "加强：给已有的东西再添一份力。三义共享「背后有力顶着」",
  "en-（使）+ fort/forc（强力）→ 背后加上一股力，纸上的东西才动得起来")

W("faculty", "noun", "/ˈfæklti/", "fac",
  "fac（做）→ facilis（做得来的）→ facultas（做得来的本事）→ 一手拿得出的本事；"
  "校中掌某门本事的那批人",
  "古法语 faculte ← 拉丁语 facultas（做得来的本事）← facilis（容易的）← facere（做）；"
  "拼写里的 cult 与 colere（耕作）无关，只是字母相含",
  "a natural ability, or a department of a university and its teaching staff",
  "同一门手艺的人聚在一栋楼里，各自都有一手拿得出的真本事",
  "能力/院系/全体教员",
  "She has a faculty for languages.|The faculty voted against the proposal.",
  "what one can do, and those who hold that skill – 做得来的那点本事，以及掌着它的那批人",
  "能力：天生就做得来的那一手|院系：一所学校里专掌某门本事的那一块|"
  "全体教员：那一块里的人合起来。三义共享「做得来的本事」，一个说本事本身，两个说掌着它的人",
  "fac（做）→ facilis（做得来的）→ 做得来的那点本事，以及掌着这门本事的那批人")

W("eternal", "adjective", "/ɪˈtɜːnl/", "", "",
  "拉丁语 aeternus（永久的）← aevum（一个时代、极长的时间）；与库中 ternus 那支"
  "（externus / internus 的里外之分）无关，只是拼写相含",
  "lasting for ever, with no end",
  "刻在石头上的字，风吹了几百年还在那儿，一笔没缺",
  "永恒的/永久的/不朽的",
  "They swore eternal friendship that summer.|The city holds an eternal flame.",
  "lasting through age after age – 一个时代接一个时代地存在下去",
  "永恒的：时间上没有尽头|永久的：定下之后不再更改|不朽的：留下的名声不随人消失。"
  "三义共享「一代接一代地留着」")

W("feminine", "adjective", "/ˈfemənɪn/", "", "",
  "古法语 feminin ← 拉丁语 femininus ← femina（女子）；femina 出自原始印欧语 "
  "*dheh₁-（哺乳）一支，与 minus（更小）无关",
  "having qualities traditionally thought of as belonging to women",
  "衣料软软垂下来，线条一路圆过去，没有一处是硬角",
  "女性的/阴性的/柔美的",
  "She has a soft feminine voice.|In French, the noun is feminine.",
  "of the woman's side of things – 归在女子那一边的那些特质",
  "女性的：属于女子这一边|阴性的：语法上归在那一类|柔美的：那一边被认作的样子。"
  "三义共享「归在女子那一边」，一个说人，一个说语法类别，一个说观感")


# ============================== B 档 ==============================
W("energy", "noun", "/ˈenədʒi/", "", "",
  "希腊语 energeia：en-（在其中）+ ergon（干活、功）——里头有活在做；"
  "经晚期拉丁语 energia 入英语",
  "the power to do work, or the liveliness a person has",
  "锅底火苗一直顶着，水在里头翻个不停，一夜没歇",
  "能量/精力/活力",
  "Solar panels turn sunlight into energy.|The children still had energy at midnight.",
  "work going on inside a thing – 一样东西里头有活在做，因此动得起来",
  "能量：物里头做功的那份|精力：人身上能拿去做事的那份|活力：那份显在外头的样子。"
  "三义共享「里头有活在做」")

W("engine", "noun", "/ˈendʒɪn/", "", "",
  "古法语 engin ← 拉丁语 ingenium（天生的巧思）：in-（在内）+ gignere（生出）；"
  "由巧思转指巧妙的器械，再窄到机器，与「生出一类」那支语义已分",
  "a machine that turns fuel or power into movement",
  "铁壳子里活塞上下捣着，油送进去，轮轴就转起来",
  "发动机/引擎/机车",
  "The engine stalled halfway up the hill.|Mechanics rebuilt the old engine last winter.",
  "a contrived thing that turns power into motion – 一台巧做出来的东西，把力变成转动",
  "发动机：把力变成转动的那台东西|引擎：同一台东西的音译说法|机车：整车里以它为核心。"
  "三义共享「巧做出来、把力变成转动的那台东西」")

W("enthusiastic", "adjective", "/ɪnˌθjuːziˈæstɪk/", "", "",
  "希腊语 enthousiastikos ← enthousiazein ← entheos：en-（在其中）+ theos（神）"
  "——像有神进了身",
  "showing strong eagerness and interest",
  "讲到一半人已站起来，手比划得比嘴还快，眼睛发亮",
  "热情的/热烈的/积极的",
  "The crowd gave an enthusiastic welcome.|He is enthusiastic about learning Chinese.",
  "filled as if by something inside – 像有东西进了身，从里头把人推着往前",
  "热情的：人被里头那股劲推着|热烈的：场面上显出来的那股劲|积极的：那股劲落到做事上。"
  "三义共享「里头进了一股劲」，分别说人、场面与行动")

W("episode", "noun", "/ˈepɪsəʊd/", "hodos",
  "epi-（另加）+ eis（进入）+ od（hodos 路）→ 正路之外另插进来的那一段",
  "希腊语 epeisodion：epi-（另加）+ eis（进入）+ hodos（路）——原指古希腊戏剧里"
  "歌队之间插进来的那一段",
  "one part of a series, or a single event within a longer stretch",
  "连着播的片子今晚只放一段，看完停住，下一段要等明天",
  "一集/插曲/事件",
  "The final episode airs on Sunday night.|That episode of his life stayed hidden.",
  "one stretch inserted along a longer way – 长路上单独插进来的那一段",
  "一集：连播的东西里单独一段|插曲：正事之外插进来的一段|事件：一长段经历里单独可讲的一段。"
  "三义共享「长路上单独的一段」",
  "epi-（另加）+ od（路）→ 一条长路上另插进来、可以单独拿出来讲的那一段")

W("escape", "verb / noun", "/ɪˈskeɪp/", "", "",
  "古法语 eschaper ← 通俗拉丁语 excappare：ex-（出）+ cappa（斗篷）——身子从斗篷里"
  "滑出去，斗篷留在追者手上；cappa 更早词源不明，故本词不属 caput 族",
  "to get away from a place or a danger; the act of getting away",
  "外套被人一把抓住，肩膀一缩，人从袖子里滑了出去",
  "逃脱/逃跑/避开",
  "Two prisoners escaped during the night.|She planned her escape for weeks.",
  "slipping out and leaving the hold behind – 身子滑出去，被抓住的那层留在原处",
  "逃脱：从抓着自己的那处滑出来|逃跑：滑出来之后往远处去|避开：不等抓住就先滑开。"
  "三义共享「从箝制里滑出去」，按时机与远近分")

W("establishment", "noun", "/ɪˈstæblɪʃmənt/", "sta",
  "sta（站立）→ stabilis（站得稳的）→ establish（使站稳）+ -ment（结果）"
  "→ 立起来并且站住了的那一摊",
  "古法语 establissement ← establir ← 拉丁语 stabilire（使稳固）← stabilis ← stare（站立）",
  "the act of setting something up, or an organization and the people holding power",
  "牌子钉上墙，门开了，桌椅摆定，从此天天照点开门",
  "建立/机构/权势集团",
  "The establishment of the fund took years.|He works at a small printing establishment.",
  "something set up and made to stand – 立起来并且站住了的那一摊",
  "建立：把它立起来这个动作|机构：立起来之后站住的那一摊|权势集团：站得最稳、动不了的那一批人。"
  "三义共享「立起来站住」，一个说动作，两个说立成的东西",
  "sta（站立）→ stabilis（站得稳）→ 立起来并站住了的那一摊，以及立它的那个动作")

W("evacuate", "verb", "/ɪˈvækjueɪt/", "", "",
  "拉丁语 evacuare：e-（出）+ vacuus（空的）——把里头腾空；vacuus 一族在本词表内"
  "同支的只 void / avoid，且拼写上看不出，本项目未为它建根",
  "to move people out of a place because it is not safe",
  "警报一响，楼里的人一层层往外走，最后只剩空椅子",
  "疏散/撤离/腾空",
  "Police evacuated the building after the alarm.|Residents were told to evacuate immediately.",
  "emptying a place of what is in it – 把一处地方里头的东西腾出去",
  "疏散：组织人往外走|撤离：人自己离开那处|腾空：结果是里头什么都不剩。"
  "三义共享「把里头腾空」，前两个说人怎么动，后一个说腾完的样子")

W("examine", "verb", "/ɪɡˈzæmɪn/", "ag",
  "ex-（出）+ ag（驱动）→ exigere（赶出来、称量）→ examen（天平的指针）"
  "→ 一样样称过，看针停在哪里",
  "古法语 examiner ← 拉丁语 examinare ← examen（天平的指针）← exigere：ex-（出）"
  "+ agere（驱动、称量）",
  "to look at something closely in order to judge it",
  "一件件举到灯下翻过来看，指甲刮一下，再放到另一堆",
  "检查/审查/考核",
  "The doctor examined her injured knee.|Examine the contract before you sign.",
  "weighing item by item until the needle settles – 一样样称过，针停住了才算数",
  "检查：逐样看过有没有毛病|审查：看它合不合规矩，带判定|考核：拿题去称一个人。"
  "三义共享「逐样称过再判」，按被称的是物、事还是人分",
  "ex-（出）+ ag（驱动）→ 把每一样赶到天平上称一遍，针停住了才下判断")

W("excellent", "adjective", "/ˈeksələnt/", "", "",
  "拉丁语 excellens ← excellere：ex-（出）+ cellere（高起、耸出）——比周围高出一头；"
  "cellere 一族在本词表内同支的只 excel，不足以建根",
  "extremely good; of the highest quality",
  "一排苗里有一株高出一头，叶子也比旁边的厚",
  "极好的/优秀的",
  "Her spoken English is excellent.|The hotel served an excellent breakfast.",
  "standing a head above the rest – 比周围那一片高出一头",
  "极好的与优秀的：都是「比周围高出一头」，中文一个偏程度，一个偏评价")

W("exemplify", "verb", "/ɪɡˈzemplɪfaɪ/", "", "",
  "中世纪拉丁语 exemplificare ← 拉丁语 exemplum（从整批里取出的一件）"
  "← eximere：ex-（出）+ emere（取）",
  "to be a typical example of something, or to show something by example",
  "从整筐里挑出一个举到眼前，说剩下的都跟这个一样",
  "例证/举例说明",
  "This case exemplifies the wider problem.|Her work exemplifies careful research.",
  "holding one out of the batch to stand for all – 从整批里取一件出来替其余说话",
  "例证与举例说明：都是「取一件出来替整批说话」，中文一个偏它本身，一个偏这个做法")

W("exercise", "noun / verb", "/ˈeksəsaɪz/", "", "",
  "拉丁语 exercitium ← exercere：ex-（出）+ arcere（关住、圈住）——把圈着的牲口"
  "赶出来遛动；arcere 未在本项目建根",
  "physical activity done to stay healthy; also to use a power or a right",
  "牲口从栏里赶出来，绕着场子一圈圈遛，出了汗才停",
  "锻炼/练习/行使",
  "Daily exercise keeps the heart strong.|She exercised her right to vote.",
  "driving out of the pen and keeping it moving – 从圈里赶出来，让它一直动着",
  "锻炼：让身子动起来|练习：让某项本事反复动起来|行使：让手里的权真的动起来。"
  "三义共享「圈着的东西赶出来动一动」，动的是身体、本事还是权柄")

W("expansion", "noun", "/ɪkˈspænʃn/", "", "",
  "拉丁语 expansio ← expandere：ex-（出）+ pandere（摊开）；本词不属库中 "
  "passare（迈步经过）那一支",
  "the process of becoming larger, or a part added on",
  "折起来的地图在桌上摊开，边缘一直推到桌沿外头",
  "扩张/扩大/扩建部分",
  "The company announced its overseas expansion.|Heat causes expansion of the metal rail.",
  "spreading out from a folded state – 原本收着的东西朝外摊开",
  "扩张：朝外铺开的那个过程|扩大：铺开之后尺寸变了|扩建部分：铺出来多的那一块。"
  "三义共享「原本收着的朝外摊开」，说过程、说结果、说多出来的那块")

W("extreme", "adjective / noun", "/ɪkˈstriːm/", "ternus",
  "ex-（外）+ ter（方位：那一侧）→ extremus（最外那一头）→ 到边到顶，"
  "再往前没有地方了",
  "拉丁语 extremus，是 exterus（外面的）的最高级 ← 方位词根 ter；这一路不属 "
  "ter-comparative 收的 -terior 对照级，故归里外之分这一根",
  "as far as it can go in one direction; the furthest point",
  "站在悬崖最外那道边上，脚尖前面已经没有地了",
  "极端的/极度的/末端",
  "He holds extreme views on taxation.|They survived extreme cold in the mountains.",
  "the furthest point out on one side – 一侧上最外、再往前没有了的那一点",
  "极端的：立场站到最外那一头|极度的：程度顶到边|末端：位置上最外那一点。"
  "三义共享「最外那一头」，分别落在立场、程度与位置",
  "ex-（外）+ ter（那一侧）的最高级 → 一侧上最外那一头，再往前就没有地方了")

W("famine", "noun", "/ˈfæmɪn/", "", "",
  "古法语 famine ← 通俗拉丁语 famina ← 拉丁语 fames（饥饿）；与 fame（名声，"
  "出自 fari 说）不同源，勿混",
  "a severe shortage of food across a whole area",
  "地裂着缝，谷仓底扫得见木板，村口的锅倒扣着",
  "饥荒/饥饿",
  "Drought brought famine to the region.|Aid arrived too late to stop famine.",
  "a whole land run out of food – 一整片地方的粮见了底",
  "饥荒与饥饿：都是「粮见了底」，一个说那片地方的局面，一个说人身上的感觉")

W("fascinate", "verb", "/ˈfæsɪneɪt/", "", "",
  "拉丁语 fascinare（施法定住）← fascinum（咒符、护符）——像被下了咒，眼睛移不开；"
  "fascinum 一族在本词表内只此一词",
  "to hold someone's interest completely",
  "眼睛黏在那件东西上，旁边有人叫也没听见",
  "使着迷/吸引住",
  "Snakes fascinate my younger brother.|The old maps fascinated her for hours.",
  "held in place as if by a spell – 像被下了咒，眼睛挪不开",
  "使着迷与吸引住：都是「像被咒定住」，一个说人里头的状态，一个说那东西的作用")

W("fiction", "noun", "/ˈfɪkʃn/", "figur",
  "fic（捏塑）→ fictio（捏出来的东西）→ 手捏出来的一套，现实里找不到对应",
  "古法语 ficcion ← 拉丁语 fictio（捏造之物）← fingere（塑造、捏造）；"
  "库中 figment 同出这一支，故并入同一根",
  "writing that tells of imagined people and events; something made up",
  "空手在空气里捏出一个人，讲得有鼻子有眼，松手什么都不剩",
  "小说/虚构/编造",
  "She writes fiction set in Victorian London.|That story is pure fiction.",
  "a shape moulded only in words – 只用话捏出来的形状，现实里没有对应",
  "小说：捏出来的那一整套写成书|虚构：捏出来这件事本身|编造：捏的时候还想让人当真。"
  "三义共享「手里捏出个形，松手就没了」",
  "fic（捏塑）+ -tion（结果）→ 捏出来的那个形，讲得再像也找不到对应的实物")


# ============================== C 档 ==============================
W("empirical", "adjective", "/ɪmˈpɪrɪkl/", "experiri",
  "em-（en 在其中）+ piri（peira 试）→ 在亲手试过之中得来的 → 凭实测立论",
  "希腊语 empeirikos ← empeiria（亲身经历）：en-（在其中）+ peira（试）；"
  "与拉丁语 experiri 的 peritus 一支同出原始印欧语 *per-（试、冒险），是同源而非借入",
  "based on what has actually been observed or measured",
  "不查书，先架起仪器读三天的数，纸上记满了才开口",
  "经验主义的/实证的",
  "The claim needs empirical support.|Their method is strictly empirical.",
  "resting on what one has tried oneself – 立在亲手试过、量过的那点东西上",
  "经验主义的与实证的：都是「只认亲手试过的」，一个说这套主张，一个说这个做法",
  "em-（在其中）+ piri（试）→ 只认亲手试过、量过的那点东西，不认书上写着的")

W("equator", "noun", "/ɪˈkweɪtə/", "aequus",
  "aequ（平、相等）+ -ator（做那事的）→ 把昼夜分得一样长的那条线",
  "中世纪拉丁语 aequator（把昼夜均分者）← aequare（使相等）← 拉丁语 aequus（平的、相等的）",
  "the imaginary line around the middle of the earth",
  "地球仪腰上一圈刻线，上下两半正好一样大",
  "赤道", "Singapore lies close to the equator.|Temperatures rise as you near the equator.",
  "the line that halves the globe evenly – 把球身平分成一样两半的那道线", "",
  "aequ（平、相等）+ -ator（做那事的）→ 腰上那道线，把上下分得一样大")

W("especially", "adverb", "/ɪˈspeʃəli/", "spect",
  "spec（看）→ species（一眼看去的种类）→ especial（自成一类的）+ -ly "
  "→ 把这一项单独挑出来说",
  "古法语 especial ← 拉丁语 specialis（单独一类的）← species（种类、样貌）← specere（看）",
  "more than in other cases; above all",
  "一整排里有一格被手指点住，说的就是这一格，别的先放着",
  "尤其/特别",
  "I love fruit, especially ripe mangoes.|The road is dangerous, especially at night.",
  "singling one item out of the row – 从一排里把这一项单独点出来",
  "尤其与特别：都是「从一排里点出这一项」，中文一个偏比较，一个偏程度",
  "spec（看）→ species（种类）→ 从一排里把这一项单独点出来说",
  "especially + n —— 从前面那一类里单独点出这一项，后面多接名词或名词短语|"
  "especially when / if + 从句 —— 在某种情形下更是如此，用来收窄适用场合|"
  "not especially + adj —— 不怎么、不太，把程度往下压，比 not very 缓和|"
  "especially 与 specially —— 前者是从一类里挑出来，后者是为某个目的专门去做")

W("evaluate", "verb", "/ɪˈvæljueɪt/", "valere",
  "e-（出）+ val（valere 有力、值）→ 把它值多少掂出来",
  "法语 évaluer ← 古法语 esvaluer：es-（ex- 出）+ value ← 拉丁语 valere（有力、值）",
  "to judge how good, useful, or valuable something is",
  "东西掂在手里上下颠两下，心里给它记一个数",
  "评估/估价",
  "We must evaluate the risks first.|Teachers evaluate each student twice a year.",
  "working out what a thing is worth – 把一样东西值多少掂出来",
  "评估与估价：都是「掂出它值多少」，一个用在事上，一个用在物与钱数上",
  "e-（出）+ val（值）→ 掂一掂，把它值多少这个数说出来")

W("everything", "pronoun", "/ˈevriθɪŋ/", "", "",
  "中古英语 every thing 两词合成：every ← 古英语 æfre ǣlc（永远每一个），"
  "thing ← 古英语 þing（物、事）",
  "all things; the whole of a situation",
  "桌上摊开的东西一样没少，连纸角上的别针都在里头",
  "一切/每样东西/所有事",
  "He packed everything into one small bag.|Everything depends on tomorrow's weather.",
  "every single thing taken together – 每一样都算进去，一件不落",
  "一切：合起来说的那个总数|每样东西：落到具体物件上|所有事：落到事情上。"
  "三义共享「一件不落地都算进去」", "",
  "everything + 单数动词 —— 作主语时谓语用单数，如 everything is ready|"
  "everything but / except sth —— 除这一项之外全都算上|"
  "do everything possible to do sth —— 尽一切办法，possible 后置修饰|"
  "everything 与 all —— everything 可单独作主语宾语，all 多带 of 或后接从句")

W("exceedingly", "adverb", "/ɪkˈsiːdɪŋli/", "ced",
  "ex-（出、越过）+ ceed（行走）+ -ingly → 走出划定那条线之外的程度",
  "拉丁语 excedere：ex-（出）+ cedere（行走）；英语 exceed 加 -ingly 成副词",
  "to a very great degree",
  "水位早漫过警戒刻度，还在一格一格往上爬",
  "极其/非常",
  "The exam was exceedingly difficult.|She was exceedingly kind to us.",
  "past the marked line by far – 远远走出划定的那条线",
  "极其与非常：都是「远远越过那条线」，中文两种说法对应同一个程度",
  "ex-（越过）+ ced（行走）→ 远远走到划定那条线之外的那个程度",
  "exceedingly + adj —— 极其，程度顶格，书面色彩比 very 重|"
  "exceedingly well / rare —— 修饰副词与偏书面的形容词最自然，口语少用|"
  "exceedingly 与 excessively —— 前者只说程度高，后者带过了头的贬义")

W("extra", "adjective / adverb / noun", "/ˈekstrə/", "ternus",
  "ex-（外）+ ter（方位：那一侧）→ extra（在界线之外）→ 定数之外另添的",
  "拉丁语 extra（在外面），是 exterus（外面的）的夺格 ← 方位词根 ter；本词不属 "
  "ter-comparative 收的 -terior 对照级那一路",
  "more than what is usual or expected; something added on",
  "碗里盛好了又添一勺，勺子是从锅边另拿的",
  "额外的/另外/临时演员",
  "We need an extra chair here.|The hotel charges extra for breakfast.",
  "added from outside the set amount – 定数之外，从外头再添上的",
  "额外的：数目之外多的那份|另外：作副词说另加着算|临时演员：片子里名单之外补上的人。"
  "三义共享「定数之外从外头添进来的」",
  "ex-（外）+ ter（那一侧）→ 原定那个数之外，从外头再添上的那份",
  "an extra + n —— 额外一个，在原定数目之外再加|"
  "extra + adj —— 特别、格外，口语里加强程度，如 extra careful|"
  "charge / pay extra —— 另外加钱，此时 extra 作副词放在动词后|"
  "extras —— 复数指另计费的附加项，也指片中的群众演员")

W("ferry", "noun / verb", "/ˈferi/", "", "",
  "中古英语 ferien ← 古诺斯语 ferja（渡运），与古英语 ferian（运送）同支 "
  "← 原始日耳曼语 *farjan（使渡过）",
  "a boat that carries people across water; to carry across",
  "一条平底船在两岸之间来回，甲板上停着车和人",
  "渡船/摆渡/运送",
  "We took the ferry across the strait.|Buses ferry workers to the site daily.",
  "carrying across from bank to bank – 把人和物从这岸带到那岸",
  "渡船：来回带人的那条船|摆渡：船来回这个动作|运送：不限于水面，一趟趟把人送过去。"
  "三义共享「从这边带到那边」，说船、说动作、说泛化后的来回接送")

W("fight", "verb / noun", "/faɪt/", "", "",
  "古英语 feohtan（搏斗）← 原始西日耳曼语 *fehtan ← 原始日耳曼语 *fehtaną（搏击）",
  "to take part in a violent struggle; a violent struggle",
  "两个人扭在一起，拳头往对方身上落，谁也不肯先松手",
  "打斗/斗争/打架",
  "The two boys fought behind the shed.|She fought hard for equal pay.",
  "two forces set against each other – 两股力顶在一处，谁都不肯退",
  "打斗：身体上互相下手|斗争：为某件事长期顶着，不一定动手|打架：一场具体的动手。"
  "三义共享「两股力顶在一处不肯退」，按是否动手与时间长短分")


# ============================== 落盘 + 自检 ==============================
def main():
    rows = R_ROWS + W_ROWS
    for i, r in enumerate(rows, 1):
        tag = r[0]
        need = 10 if tag == "R" else 15
        assert len(r) == need, f"row {i} ({r[1]}): {len(r)} cols, need {need}"
        for c in r:
            assert "\t" not in c, f"row {i} ({r[1]}): embedded tab"
            assert "\n" not in c, f"row {i} ({r[1]}): embedded newline"

    # image 规则：15-35 字，不含任何长度 >=2 的 zh 义项
    for r in W_ROWS:
        word, image, zh = r[1], r[8], r[9]
        n = len(image)
        assert 15 <= n <= 35, f"{word}: image {n} 字，需 15-35"
        for x in [x.strip() for x in zh.split("/") if x.strip()]:
            assert not (len(x) >= 2 and x in image), f"{word}: image 含义项 {x}"
        # 例句 5-12 词、句末句号
        ex = [e.strip() for e in r[10].split("|") if e.strip()]
        assert len(ex) == 2, f"{word}: {len(ex)} 例句"
        for e in ex:
            assert e.endswith("."), f"{word}: 例句缺句号 {e!r}"
            nw = len(e.rstrip(".").split())
            assert 5 <= nw <= 12, f"{word}: 例句 {nw} 词 {e!r}"
        # zh >=2 项须有 expansions
        zl = [x for x in zh.split("/") if x.strip()]
        if len(zl) >= 2:
            assert r[12].strip(), f"{word}: {len(zl)} 义项却无 expansions"
        # root_ids 与 root_logic 同进同退
        assert bool(r[4].strip()) == bool(r[5].strip()), f"{word}: 第5/6列不配对"
        # hint 门：root_logic 里中文义项出现 >=3 次时必填
        if r[4].strip():
            blanks = sum(r[5].count(x) for x in zl if len(x.strip()) >= 2)
            if blanks >= 3:
                assert r[13].strip(), f"{word}: root_logic 含 {blanks} 处义项，hint 必填"
        # 第 15 列非空须含 ——
        if r[14].strip():
            assert "——" in r[14], f"{word}: 第15列缺 ——"

    OUT.write_text("\n".join("\t".join(r) for r in rows) + "\n", newline="\n",
                   encoding="utf-8")
    nr = sum(1 for r in W_ROWS if r[4].strip())
    print(f"[written] {OUT}  R={len(R_ROWS)} W={len(W_ROWS)}"
          f"（词根型 {nr} / 日耳曼型 {len(W_ROWS)-nr}）")

    # ---- 干跑筛查脚本的匹配键，提前发现结构性假阳性 ----
    roots = json.loads((ROOT / "data" / "roots.json").read_text(encoding="utf-8"))["roots"]
    lemma_pat = re.compile(r"\b([a-z][a-z]{3,})\b")
    STOP = {"vetted", "note", "pie", "root", "variants", "inter", "trans",
            "circum", "contra", "intro", "super", "supra", "subter", "ante",
            "post", "prae", "retro", "extra", "infra", "intra", "juxta",
            "quasi", "ultra", "semi", "multi", "omni", "bene", "male", "vice",
            "amphi", "anti", "cata", "meta", "para", "peri", "hyper", "hypo",
            "endo", "exo"}
    CONTRAST = ("不同根", "不同源", "不计入", "不合并", "非同", "不属", "而不",
                "无关", "勿混", "另有分别", "并非同源", "不是同", "两个不同",
                "已分化", "而分支不同", "不同支", "承义的是", "不是 ", "语义已分",
                "不在此列", "另有分立")
    WIN = 60

    def clause(t, p, e=None):
        return t[max(0, p - WIN):(e or p) + WIN]

    forms = {}
    for rt in roots:
        cand = {rt.get("root", "")} | set(rt.get("variants") or [])
        o = rt.get("origin", "")
        for m in lemma_pat.finditer(o):
            if not any(x in clause(o, m.start(), m.end()) for x in CONTRAST):
                cand.add(m.group(1))
        cand = {c for c in cand if c and len(c) >= 5 and c.isalpha()
                and c not in STOP}
        if cand:
            forms[rt["id"]] = cand

    hits = []
    for r in W_ROWS:
        word, origin = r[1], r[6]
        declared = {x.strip() for x in r[4].split("/") if x.strip()}
        for rid, cands in forms.items():
            if rid in declared:
                continue
            for c in cands:
                m = re.search(r"(?<![a-z])" + re.escape(c.lower()) + r"(?![a-z])",
                              origin.lower())
                if m and not any(x in clause(origin, m.start(), m.end())
                                 for x in CONTRAST):
                    hits.append((word, rid, c))
                    break
    if hits:
        print(f"[dry-run screen] {len(hits)} 处会触发 [REVIEW]:")
        for w, rid, c in hits:
            print(f"    {w} → {rid}（{c}）")
    else:
        print("[dry-run screen] 无触发")


if __name__ == "__main__":
    main()
