#!/usr/bin/env python3
"""生成 drafts/g_chunk105.tsv。

用列表 join 落盘（不用 Write 工具），尾列留空的行才留得住制表符。
每行落盘前 assert 列数：W=15，R=10。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "drafts" / "g_chunk105.tsv"

R_ROWS = []
W_ROWS = []


def R(rid, variants, origin, cc, image, edef, slug, czh, dom):
    row = ["R", rid, variants, origin, cc, image, edef, slug, czh, dom]
    assert len(row) == 10, f"{rid}: {len(row)} 列"
    R_ROWS.append(row)


def W(word, pos, ph, rids, logic, origin, native, image, zh, ex, concept,
      exps="", hint="", colloc=""):
    row = ["W", word, pos, ph, rids, logic, origin, native, image, zh, ex,
           concept, exps, hint, colloc]
    assert len(row) == 15, f"{word}: {len(row)} 列"
    W_ROWS.append(row)


# ---------------------------------------------------------------- 新建词根 2 个
R("frangere", "frag/fract",
  "拉丁语 frangere（把整块打断、砸碎），过去分词 fractus → fractio（掰断这件事）、"
  "fragilis（一碰就断的）、fragmentum（掰下来的那一块）；库中 fragrant 出自 fragrare"
  "（散出气味），与本根不同源，只是字母相含",
  "to break a whole into pieces / 把整块弄断成几块",
  "一块石板从中间裂开，断口毛糙，碎屑落了一地",
  "to break, to shatter into pieces", "shatter", "掰成碎块", "domain-force")

R("fundus", "fund/found",
  "拉丁语 fundus（底、地基、田产的底子），动词 fundare（给它垫上底、奠基）、"
  "fundamentum（垫在下面的那一层）、profundus（往底下深去的）同出此支；"
  "库中另有一个拼写相近的拉丁词根，义为倒出、浇注，与本根不同源，勿混",
  "the bottom layer a thing rests on / 压在最下面、托住上头的那一层",
  "墙还没砌，先在地上铺一层石头，往下踩不动了才开始往上垒",
  "bottom, base, foundation", "bottom", "垫在底下", "domain-shape")

# ---------------------------------------------------------------- A 档 6 词
W("fit", "adjective / verb", "/fɪt/", "", "",
  "中古英语 fit / fitten（15 世纪，本义排布、使相称），更早词源不明；"
  "或与古诺斯语 fitja（编结）有关，未有定论",
  "right in size, shape, or condition for a purpose",
  "抽屉板往槽里一推，四边正好挨上，推到底不晃也不卡",
  "适合/合身/健康的/安装",
  "These shoes fit me perfectly.|He keeps fit by swimming daily.",
  "sitting into place with no gap left – 放进去正好挨上，不空不挤",
  "适合：用途上正好对得上|合身：尺寸上正好挨着身子|健康的：身体状况正对得上要做的事|"
  "安装：把件东西按进它该在的位置。四义共享「正好落进该在的位置」")

W("fluctuate", "verb", "/ˈflʌktʃueɪt/", "fluere",
  "fluc（fluere 流动）+ -ate → fluctus 是流动堆起的浪 → 面上一处鼓起一处塌下，高低不定",
  "拉丁语 fluctuare（起浪、摇荡）← fluctus（浪）← fluere（流动）",
  "to keep rising and falling in an irregular way",
  "湖面被风推着，这边刚鼓起来，旁边就塌下去，没有一刻是平的",
  "波动/起伏/涨落",
  "Oil prices fluctuate from week to week.|Her mood fluctuated all through the winter.",
  "a surface that rises and sinks without settling – 面上一处起一处落，始终定不下来",
  "波动：数值上下摆，不停在一个数上|起伏：一高一低轮着来|涨落：像潮水那样涨上去又退回来。"
  "三义共享「面上一处起一处落，定不下来」",
  "fluc（流动）+ -ate → 水面被推得一处鼓一处塌，高低轮着换，始终不停在一个数上")

W("formidable", "adjective", "/ˈfɔːmɪdəbl/", "", "",
  "拉丁语 formidabilis ← formidare（畏惧）← formido（恐惧）；"
  "与库中 forma 那一根（形状）不同源，只是拼写头几个字母相含",
  "so strong, large, or difficult that it makes people uneasy",
  "那人一站起来把门框占满了，屋里说话的都停了",
  "可怕的/令人敬畏的/艰巨的",
  "She was a formidable opponent in court.|They face a formidable task this year.",
  "big enough to make one hesitate – 大得让人先怯一下，不敢轻易上前",
  "可怕的：让人怕|令人敬畏的：怕里还带着服气|艰巨的：事情大到让人先怯。"
  "三义共享「大到让人先怯一下」，分别落在人、态度与事上")

W("fountain", "noun", "/ˈfaʊntɪn/", "", "",
  "古法语 fontaine ← 晚期拉丁语 fontana（泉眼）← 拉丁语 fons（泉）；"
  "与库中 tain 那一根（握住）无关，只是词尾拼写相含",
  "a structure that sends water up into the air; also a natural spring",
  "水从池子中央直直冲上去，到了顶散成一片，落回来砸得石沿全是点子",
  "喷泉/泉水/源头",
  "Children ran around the fountain in the square.|The village drinks from a mountain fountain.",
  "water pushed up out of an opening – 水从一个口子被顶出来，往上冒",
  "喷泉：人造的那一处往上冒水|泉水：地里自己冒出来的水|源头：往上追，东西是从这儿冒出来的。"
  "三义共享「从一个口子往上冒出来」，一处说人造，一处说天然，一处转指来处")

W("fundamental", "adjective / noun", "/ˌfʌndəˈmentl/", "fundus",
  "fund（底）+ -mental → fundamentum 是垫在最下面的那一层 → 抽掉一块，上头整片跟着垮",
  "拉丁语 fundamentalis ← fundamentum（垫在下面的那一层）← fundus（底、地基）",
  "forming the base that everything else rests on",
  "把楼扒到只剩底下那层石头，抽走一块，上面整片跟着塌",
  "基本的/根本的/基本原理",
  "Reading is a fundamental skill for children.|Learn the fundamentals before you improvise.",
  "the lowest layer that carries the rest – 压在最下面、托着上头一切的那一层",
  "基本的：位置上最靠底，别的都搭在它上头|根本的：动它一下，上头全跟着变|"
  "基本原理：那一层本身，拿出来单说。三义共享「压在最下面、托着上头的那一层」",
  "fund（底）+ -mental → 垫在最下面那一层，抽掉一块，上头整片跟着垮")

W("genius", "noun", "/ˈdʒiːniəs/", "gen",
  "gen（生出）→ genius 本指随人一同生下来的守护灵 → 一出生就带着、后天补不齐的那一份",
  "拉丁语 genius（伴人一生的守护神灵）← gignere（生出）；与 genus（种、出身）同支",
  "very great natural ability, or a person who has it",
  "谱子第一次翻开，手按下去就是对的，旁边练了十年的还差一截",
  "天才/天赋/天资",
  "Mozart showed his genius as a small child.|She has a genius for solving puzzles.",
  "something one is born carrying – 一出生就带在身上的那一份，不是学来的",
  "天才：带着那一份的人|天赋：那一份东西本身|天资：那一份的高低成色。"
  "三义共享「出生就带着、后天补不齐」，一个说人，两个说那份东西",
  "gen（生出）→ 随人一同生下来的那一份，别人后天再练也补不齐")

# ---------------------------------------------------------------- B 档 10 词
W("filter", "noun / verb", "/ˈfɪltə/", "", "",
  "中世纪拉丁语 filtrum（滤水用的毛毡）← 日耳曼语支表「毡」的词，与英语 felt 同源；"
  "与库中 filum 那一根（线）不同源",
  "a device that lets liquid or air through but holds back solids",
  "漏斗里垫一层毡，水一滴一滴渗下去，渣子全留在毡面上",
  "过滤器/滤除/筛选",
  "Change the water filter every three months.|The app filters out unwanted messages.",
  "a layer that lets one thing through and keeps the rest – 一层拦子，过一样留一样",
  "过滤器：那一层拦子本身|滤除：把不要的留在拦子上|筛选：拿这一层挑出要的。"
  "三义共享「一层拦子，过一样留一样」，一个说物，两个说这个动作")

W("fraction", "noun", "/ˈfrækʃn/", "frangere",
  "fract（frangere 打断）+ -ion → 从整块上断下来的那一小块",
  "古法语 fraccion ← 晚期拉丁语 fractio（掰断）← frangere（打断）的过去分词 fractus",
  "a small part of something whole; also a number written as one part over another",
  "整张饼掰下一角，剩下的还摊在盘里，一眼看得出掰走的少",
  "分数/小部分/一点点",
  "Only a fraction of the crowd stayed.|Add these two fractions together.",
  "one piece broken off a whole – 从整块上断下来的那一块",
  "分数：写成上下两截的那种数，本就是整数掰开来记|小部分：整体里掰下来的一块|"
  "一点点：那一块小到几乎不算。三义共享「从整块上掰下来的一块」，按记法与大小分",
  "fract（打断）+ -ion → 整块掰开，手里剩的那一块比原来小得多")

W("fragile", "adjective", "/ˈfrædʒaɪl/", "frangere",
  "frag（frangere 打断）+ -ile（容易…的）→ 一点力就断",
  "拉丁语 fragilis（一碰就断的）← frangere（打断）",
  "easily broken or damaged; also weak in health",
  "纸箱侧面画着朝上的箭头，工人两手托着底，脚下走得极慢",
  "易碎的/脆弱的/虚弱的",
  "Handle those glasses, they are fragile.|The peace agreement remains fragile.",
  "giving way before the force is even applied – 力还没使上就先断了",
  "易碎的：物件一碰就裂|脆弱的：局面一碰就散|虚弱的：人身子一碰就倒。"
  "三义共享「力还没使上就先断」，分别落在物、局面与人身上",
  "frag（打断）+ -ile（容易）→ 力还没使上就先断，物、局面、人身都一样")

W("frequency", "noun", "/ˈfriːkwənsi/", "", "",
  "拉丁语 frequentia（人多、挤在一处、屡屡）← frequens（挤满的、屡屡的）；"
  "frequens 更早词源不明",
  "how often something happens within a period of time",
  "同一格里的划痕挤成一片，隔壁那格只有零星两三道",
  "频率/频繁/次数",
  "The frequency of storms has risen sharply.|Trains run with great frequency at rush hour.",
  "how densely the same thing repeats in a stretch – 同一件事在一段里挤得多密",
  "频率：单位时间里出现多少回，可以量|频繁：挤得密这个样子|次数：数出来的那个回数。"
  "三义共享「同一件事在一段时间里挤得多密」，说度量、说样子、说数目")

W("frustrate", "verb", "/frʌˈstreɪt/", "", "",
  "拉丁语 frustrari（使落空、骗过）← frustra（白费、徒然）的过去分词 frustratus",
  "to stop someone's plan from succeeding, or to make someone feel helpless",
  "钥匙插进去转了半圈就卡住，来回拧了十几次，锁还是没开",
  "使挫败/使沮丧/阻挠",
  "Bad weather frustrated our travel plans.|It frustrates me when nobody answers.",
  "force spent that comes to nothing – 力气使出去，落了个空",
  "使挫败：事情办不成|使沮丧：办不成之后心里那口闷气|阻挠：从外头动手让别人的事落空。"
  "三义共享「力气使出去落了空」，一个说结果，一个说心里，一个说是谁弄的")

W("genetic", "adjective", "/dʒɪˈnetɪk/", "gen",
  "gen（生出）→ 希腊语 genesis（生成、起头）→ genetikos → 上一代生下一代时带过去的那一份",
  "希腊语 genetikos（关于生成的）← genesis（生成、起源），与拉丁语 genus（种、出身）同支",
  "relating to genes, or passed from parents to children",
  "父子俩眉心那道竖纹长在同一处，隔了三十年一模一样",
  "遗传的/基因的",
  "The disease has a clear genetic cause.|Scientists study genetic changes in rice.",
  "carried over at the moment of being born – 生下来那一刻就带过去的那一份",
  "遗传的：上一代带给下一代|基因的：带过去的那份东西本身。"
  "两义共享「生下来那刻就带着」，一个说这件事，一个说那样东西",
  "gen（生出）→ genesis（生成）→ 上一代生下一代时一并带过去的那一份")

W("genuine", "adjective", "/ˈdʒenjuɪn/", "gen",
  "gen（生出）→ genuinus（天生如此的）→ 生下来就是这个，不是后头装出来的",
  "拉丁语 genuinus（天生的、本来的）← gignere（生出），与 genus（种、出身）同支",
  "really what it appears to be, not fake",
  "银器底上那个戳记是压进去的，指甲刮不掉；仿的一擦就花了",
  "真正的/真诚的/纯正的",
  "This bag is genuine leather.|He showed genuine concern for her.",
  "born as this, not put on afterwards – 生下来就是这个，不是后来添的",
  "真正的：东西本身就是它看着那样|真诚的：人的心思也是本来那样，没装|"
  "纯正的：血统或来处没混过别的。三义共享「生下来就是这个，不是后添的」",
  "gen（生出）→ 生下来就是这个样子，后头装的都刮得掉")

W("germ", "noun", "/dʒɜːm/", "gen",
  "gen（生出）→ 拉丁语 germen（刚冒出的芽）→ 一点点小东西，整株都从它长出来",
  "法语 germe ← 拉丁语 germen（芽、萌出物）；germen 更早词源不明，"
  "一说与 genus（种、生出）同出一支",
  "a very small living thing that can cause disease; also the earliest bud of something",
  "麦粒剖开，尖头上那一点白的，整株都从这一点长出来",
  "细菌/胚芽/萌芽",
  "Wash your hands to kill germs.|That trip was the germ of her novel.",
  "the tiny thing everything grows out of – 一点点小东西，整个都从它长出来",
  "细菌：小到看不见却能长成一片的活物|胚芽：谷粒里往外长的那一点|"
  "萌芽：想法刚起头的那一点。三义共享「小到不起眼，却是整个由它长出来」",
  "gen（生出）→ germen（刚冒出的芽）→ 小到不起眼的那一点，整个都从它长起来")

W("guarantee", "noun / verb", "/ˌɡærənˈtiː/", "", "",
  "古法语 garant（作保人、保状）经西班牙语 garante 改形入英语，与 warrant 是同一支的"
  "两种拼法；库中 wardon 那一根（守望、看顾）出自另一支，不同源，勿混",
  "a firm promise that something will happen or be put right",
  "合同末尾多签一个人的名字，将来出岔子先找他",
  "保证/担保/保修",
  "The shop offers a two-year guarantee.|I guarantee you will enjoy this book.",
  "a second name standing behind a promise – 承诺背后另有一个人担着",
  "保证：把话说死，出事我负责|担保：拿自己的信用替别人顶着|保修：商家许下的那段包修期。"
  "三义共享「承诺背后另有一个人担着」，按担的是话、别人的事还是货")

W("hamper", "verb / noun", "/ˈhæmpə/", "", "",
  "中古英语 hampren（围住、妨碍），词源不明，或出自表大篮子的同形名词；"
  "名词那一支经盎格鲁法语 hanaper ← 古法语 hanepier ← 日耳曼语借词 hanap（高脚杯）",
  "to make it hard for someone or something to move or make progress",
  "泥浆没到膝盖，每抬一步都得先把脚从里头拔出来",
  "妨碍/阻碍/大篮子",
  "Heavy snow hampered the rescue team.|She packed a hamper for the picnic.",
  "something clinging that makes every step cost more – 身上缠着东西，每动一下都更费力",
  "妨碍：使动作变慢变难|阻碍：拦在路上让进展变慢|"
  "大篮子：本义那只带盖的大篮，装满了提着就沉。三义共享「缠着、沉着，动起来更费力」，"
  "两义说使人费力，一义说那只让人费力的容器")

# ---------------------------------------------------------------- C 档 15 词
W("film", "noun / verb", "/fɪlm/", "", "",
  "古英语 filmen（薄皮、膜）← 原始西日耳曼语 *filmīn，与 fell（兽皮）同支",
  "a very thin layer or coating; also a story recorded to be shown on a screen",
  "牛奶放凉，表面结出一层皮，勺子一挑整片提起来",
  "薄膜/电影/胶片",
  "A film of dust covered the shelf.|They filmed the scene at dawn.",
  "one very thin layer lying over a surface – 覆在表面上薄薄的一层",
  "薄膜：本义那薄薄一层|胶片：涂了药的那一层，影像落在上头|"
  "电影：拍在那一层上、放出来的东西。三义共享「薄薄一层」，由物延到记在这层上的影像")

W("finding", "noun", "/ˈfaɪndɪŋ/", "", "",
  "由 find 加 -ing 构成；find ← 古英语 findan（找到、遇上）← 原始日耳曼语 *finþanan",
  "a fact or conclusion reached after research or an official inquiry",
  "翻了三个月的记录，最后在纸上写下一行，底下签名盖章",
  "发现/研究结果/裁定",
  "The findings were published last month.|The court announced its finding today.",
  "what turns up after searching, set down in writing – 找了一场之后落到纸上的那一条",
  "发现：找到的那件事本身|研究结果：一场研究之后写下来的那几条|"
  "裁定：正式查过之后给出的那个判断。三义共享「找过一场，把找到的落成一条」")

W("fireman", "noun", "/ˈfaɪəmən/", "", "",
  "英语复合词 fire（火 ← 古英语 fȳr）+ man（人 ← 古英语 mann）",
  "a person whose job is to put out fires, or to tend a furnace on a ship or train",
  "头盔压到眉毛，抱着水带往冒烟的门里冲，身后水管一路绷直",
  "消防员/司炉",
  "The fireman carried the child down the ladder.|The fireman shovelled coal all night.",
  "the man who deals with the flames – 专管跟火打交道的那个人",
  "消防员：把火扑掉的那个人|司炉：往炉里添火、看着火的那个人。"
  "两义共享「跟火打交道的人」，一个灭火，一个添火")

W("fisherman", "noun", "/ˈfɪʃəmən/", "", "",
  "英语复合词 fisher（捕鱼的人 ← 古英语 fisc 鱼）+ man（人）",
  "a person who catches fish, for work or for pleasure",
  "天没亮网就从船舷放下去，人坐在船尾盯着水面，一动不动",
  "渔民/钓鱼的人",
  "The fisherman mended his nets on the beach.|My uncle is a keen fisherman.",
  "the one who takes fish out of the water – 把鱼从水里弄上来的那个人",
  "渔民：以此为生的那批人|钓鱼的人：为消遣坐在水边的那个人。"
  "两义共享「把鱼从水里弄上来的人」，按是生计还是消遣分")

W("flatter", "verb", "/ˈflætə/", "", "",
  "古法语 flater（抚摸、奉承），出自日耳曼语支，与 flat（平的）同支——"
  "像用平掌顺着毛抚过去",
  "to praise someone too much in order to please them",
  "说话的人手贴着对方袖子一路顺下去，句句都挑对方爱听的说",
  "奉承/讨好/使显得更好看",
  "He flattered the boss at every meeting.|That dress really flatters her.",
  "stroking along the grain so the other feels good – 顺着毛抚过去，让对方受用",
  "奉承：好话说得过了头|讨好：说好话是为了换对方高兴|"
  "使显得更好看：衣物或灯光把人衬得比实际好。三义共享「顺着毛抚过去，让对方受用」")

W("forecast", "noun / verb", "/ˈfɔːkɑːst/", "", "",
  "中古英语 forecasten：fore-（预先 ← 古英语 fore）+ casten（抛、投 ← 古诺斯语 kasta）"
  "——把盘算先往前抛出去，看落在哪儿",
  "a statement of what is likely to happen, especially about the weather",
  "地图上画着几条弧线往东移，旁边标着明天这一片落多少雨",
  "预报/预测",
  "The forecast says rain for the weekend.|Analysts forecast slower growth next year.",
  "throwing the reckoning ahead to see where it lands – 把盘算往前抛出去，看它落在哪儿",
  "预报与预测：都是「把盘算往前抛」，一个偏正式发布出来的那份，一个偏做这件事")

W("forth", "adverb", "/fɔːθ/", "", "",
  "古英语 forð（向前、往外）← 原始日耳曼语 *furth-，与 for、fore 同支",
  "out from a place, or onward in time",
  "门开出一条缝，人从里头走出来，脚步没往回收",
  "向前/往外/此后",
  "He stepped forth from the shadows.|From that day forth she never wrote.",
  "out and onward from where one was – 从原处往外、往前，不回头",
  "向前：位置上朝前去|往外：从里头出到外头|此后：时间上从那一刻往后。"
  "三义共享「从原处往外往前」，两义说地方，一义说时间",
  "back and forth —— 来回、往复，两头之间反复移动|"
  "and so forth —— 等等，列举未尽时收尾，与 and so on 同用|"
  "from that day / time forth —— 从那时起，往后一直如此，书面语|"
  "bring / put forth sth —— 提出、生出，把原本收着的拿到外面来")

W("forty", "noun / adjective", "/ˈfɔːti/", "", "",
  "古英语 fēowertig：fēower（四 ← 原始日耳曼语 *fedwōr）+ -tig（十为一组 ← *tigus）",
  "the number 40",
  "一排排十个一数，数到第四排刚好数完，手指停在那里",
  "四十",
  "She turns forty next month.|Forty people signed the letter.",
  "four tens counted out – 四个「十」一组组数下来")

W("framework", "noun", "/ˈfreɪmwɜːk/", "", "",
  "英语复合词 frame（骨架 ← 古英语 framian 撑出去）+ work（做成的活儿 ← 古英语 weorc）",
  "a supporting structure of bars, or a set of ideas used to organize thinking",
  "钢管一根根接起来立成骨架，墙板还没上，风从缝里穿过去",
  "框架/构架/体系",
  "Workers bolted the steel framework together.|We need a legal framework for this.",
  "the bare bones put up first, everything else hung on later – 先立起来的骨架，"
  "别的往上挂",
  "框架：立起来的那副骨架|构架：搭这副骨架的搭法|"
  "体系：把想法照骨架摆好的那一套。三义共享「先立骨架，别的往上挂」，"
  "两义说实物与搭法，一义转说想法")

W("fuss", "noun / verb", "/fʌs/", "", "",
  "1701 年前后出现的口语词，更早词源不明；或为 force 的变形，或是拟声，"
  "亦有人比之丹麦语 fjas（胡闹），均无定论",
  "unnecessary excitement or complaint about something unimportant",
  "一只杯子放歪了，半屋子人被叫过来围着看，手一直挥个不停",
  "大惊小怪/忙乱/抱怨",
  "Don't make a fuss over a small stain.|She fussed about the seating all evening.",
  "a lot of motion stirred up by very little – 一点小事惹出一大片动静",
  "大惊小怪：小事被说得很大|忙乱：手脚一直动，事没进展|"
  "抱怨：嘴上一直挑小毛病。三义共享「一点小事惹出一大片动静」，说程度、说手脚、说嘴上")

W("gently", "adverb", "/ˈdʒentli/", "gen",
  "gen（生出）→ 拉丁语 gens（族、出身）→ gentilis（同族的、出身好的）→ "
  "gentil（举止不粗）→ gentle + -ly → 出手不带力道",
  "古法语 gentil（出身高贵、举止有教养）← 拉丁语 gentilis ← gens（族、出身）；"
  "库中 generous 走的是同一条路，也由「出身好」转到待人上",
  "in a soft, careful, or mild way, without force",
  "指尖托着蛋壳往窝里放，手指一点点松开，全程没有声音",
  "轻地/温和地/缓缓地",
  "Gently place the eggs in the basket.|The path slopes gently down to the river.",
  "acting with no force put behind it – 出手时不把力道加上去",
  "轻地：手上不使劲|温和地：待人不带火气|缓缓地：坡度或变化不陡。"
  "三义共享「不使力、慢着来」，分别落在手上、态度上与坡度上",
  "gen（生出）→ gens（族、出身）→ 出身好的人举止不粗 → 出手时不把力道加上去")

W("gramme", "noun", "/ɡræm/", "", "",
  "法语 gramme ← 晚期拉丁语 gramma（一小份重量）← 希腊语 gramma（写下的一小笔）；"
  "本词只承下「一小份重量」这一义，与「书写」那一支语义已分，故不并入",
  "a unit of mass equal to one thousandth of a kilogram",
  "天平右盘只搁一枚最小的砝码，指针才刚偏过刻度一格",
  "克",
  "This letter weighs only ten grammes.|Add fifty grammes of butter.",
  "the smallest weight that still tips the beam – 小到只够让天平偏一格的那份重量")

W("greenhouse", "noun", "/ˈɡriːnhaʊs/", "", "",
  "英语复合词 green（绿的 ← 古英语 grēne）+ house（房子 ← 古英语 hūs）",
  "a glass building where plants are grown in warmth",
  "玻璃上挂满水汽，外头一层白霜，里头的苗还在往上抽",
  "温室/暖房",
  "Tomatoes ripen early in the greenhouse.|He built a small greenhouse behind the shed.",
  "a glass room that keeps the warmth in – 一间玻璃屋子，把暖气圈在里头",
  "温室与暖房：都是「玻璃屋子把暖气圈住」，一个偏栽培用途，一个偏屋子本身")

W("guideline", "noun", "/ˈɡaɪdlaɪn/", "", "",
  "英语复合词，由 guide（引路，出自古法语 guider ← 法兰克语 *wītan 示路）"
  "与 line（线）合成——先画一条线，照着它走",
  "a statement that advises how something should be done",
  "地上先弹出一条白线，后面的人踩着线走，脚不越出去",
  "指导方针/准则",
  "The department issued new safety guidelines.|Follow the guidelines when writing the report.",
  "a line drawn first for others to follow – 先画好一条线，让人照着走",
  "指导方针与准则：都是「先画一条线让人照着」，一个偏指方向，一个偏划界限")

W("handicap", "noun / verb", "/ˈhændikæp/", "", "",
  "英语本土词，出自 17 世纪赌局用语 hand in cap（手伸进帽子里抓阄定彩），"
  "后转指为拉平强弱而给占优一方加的负担",
  "something that makes it harder to succeed, or extra weight given to the stronger side",
  "跑得最快的那匹马腰上加了铅块，别的照常起跑，到终点几乎并头",
  "障碍/不利条件/让分",
  "Poor eyesight was a serious handicap for him.|The rules handicap the strongest team.",
  "extra load put on whoever is ahead – 给跑在前头的那一方另加一份负担",
  "障碍：挡在前面让事难成|不利条件：本身带着的那份吃亏|"
  "让分：比赛里为拉平强弱另加的那份负担。三义共享「身上多一份负担，因此更难成」")


def main():
    lines = ["\t".join(r) for r in R_ROWS] + ["\t".join(r) for r in W_ROWS]
    for r in R_ROWS:
        assert len(r) == 10
    for r in W_ROWS:
        assert len(r) == 15
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"写入 {OUT}：R {len(R_ROWS)} 行 / W {len(W_ROWS)} 行")


if __name__ == "__main__":
    main()
