# -*- coding: utf-8 -*-
"""按列表 join 生成 drafts/g_chunk108.tsv —— 不用 Write，尾列制表符才留得住。

R 行 10 列，W 行 15 列，落盘前跑内容自检（image 字数与义项泄露、例句词数、
列数、root_ids/root_logic 配对、与词库及词根 id 撞名）。
本片新建 1 个根：imperare（号令统辖），本批成员 imperial / imperative，
库中孤立词条 empire / emperor 可另走 attach_orphans_to_new_roots.py 挂进来。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "drafts" / "g_chunk108.tsv"

R = []
W = []


def r(rid, variants, origin, cc, image, edef, slug, czh, dom):
    R.append(["R", rid, variants, origin, cc, image, edef, slug, czh, dom])


def w(word, pos, ph, rids, logic, origin, native, image, zh, ex, concept,
      exps, hint="", colloc=""):
    W.append(["W", word, pos, ph, rids, logic, origin, native, image, zh, ex,
              concept, exps, hint, colloc])


# ---------------- R 行：新建词根 ----------------
r("imperare", "imperi/imperat",
  "拉丁语 imperare（下令、统辖）：名词 imperium 是号令之权，imperator 是发号令的统帅；"
  "它虽由「朝着」与「张罗备置」两截构成，但拉丁语里承义的一直是下令这一支",
  "to give orders and hold sway / 发号令、统辖",
  "一个人抬手说了一句，底下几千人跟着动，声音传到最远的边镇",
  "to command, to rule over", "command", "发号施令", "domain-force")

# ---------------- A 档 ----------------
w("homogeneous", "adjective", "/ˌhɒməˈdʒiːniəs/", "gen",
  "homo-（希腊语 homos 相同）+ gen（gen 生出的那一类）+ -eous → 通体出自同一类，随处取一点都一样",
  "希腊语 homogenes（同一类的），由 homos（相同）与 genos（种、类）构成，经晚期拉丁语 homogeneus 入英语",
  "made up of parts that are all of the same kind",
  "一桶漆搅到底，随便舀一勺出来，颜色都跟别处一个样",
  "同类的/成分均匀的/同质的",
  "The class is a homogeneous group of beginners.|Stir it until the mixture looks homogeneous.",
  "all of one and the same kind – 通体是同一类东西",
  "同类的：一群东西同出一类，彼此没有分别|成分均匀的：混过之后处处一个样，不分层|同质的：说人群、社会也用它，指内部差别小")

w("imperial", "adjective", "/ɪmˈpɪəriəl/", "imperare",
  "imperi（imperare 下令统辖）+ -al（…的）→ 属于那一道号令所及的整片地方",
  "古法语 imperial ← 拉丁语 imperialis ← imperium（号令之权）← imperare（下令、统辖）",
  "belonging to an empire or to the ruler of an empire",
  "地图上一大片涂成同一个颜色，京城发出的一句话，半年后传到最远的边镇",
  "帝国的/皇帝的/宏伟的",
  "The imperial army marched into the city.|They built an imperial palace of stone.",
  "under one ruler's command – 归同一道号令管着的",
  "帝国的：那道号令铺得到的整片地方|皇帝的：发这道号令的那个人自己的|宏伟的：气派大得像那套排场，多说建筑与做派")

w("implicit", "adjective", "/ɪmˈplɪsɪt/", "plic",
  "im-（in- 在里面）+ plic（plic 折）→ 意思折在里面没摊开，看的人自己去展",
  "拉丁语 implicitus ← implicare（缠进、卷进去）← in-（进）+ plicare（折叠）",
  "suggested without being said directly, or complete and unquestioning",
  "合同上没写这一条，可两边都照它办事，谁也没提过",
  "含而不露的/暗含的/绝对的",
  "There was an implicit threat in his tone.|She has implicit trust in her sister.",
  "folded in rather than spread out – 折在里头没摊开",
  "含而不露的：话里折着一层，没说出口|暗含的：前提与条件也这样折着，不另写明|绝对的：信任折得严实到不留缝，即毫无保留")

w("ingenious", "adjective", "/ɪnˈdʒiːniəs/", "gen",
  "in-（生来就在里头）+ gen（gen 生出）+ -ious → 一落生就带着的那份心思，别人学不来",
  "拉丁语 ingeniosus ← ingenium（天生的才具）← in-（在内）+ gignere（生出）",
  "very clever at inventing things or at finding new ways to solve problems",
  "他拿一根弯铁丝和一段皮筋做出了开锁的家伙，旁人只会干瞪眼",
  "有巧思的/精巧的/善于发明的",
  "She found an ingenious way to fix it.|The lock has an ingenious design.",
  "born with a turn of mind others lack – 生来带着别人没有的那份巧劲",
  "有巧思的：脑子里生来带着这份灵活|精巧的：这份心思做出来的东西也这么叫|善于发明的：专把这份劲使在造新东西上")

w("injure", "verb", "/ˈɪndʒə/", "jus",
  "in-（不）+ jur（jus 法、准）→ 不照那把准来对待人 → 落到他身上的实际损伤",
  "中古英语 injurien ← 古法语 injurier ← 拉丁语 injuria（不法加于人的事）← in-（不）+ jus（属格 juris：法、权利）",
  "to cause physical harm to a person or damage to something",
  "工地上钢管砸下来，他左腿一软跪倒，裤子那块渗出血",
  "伤害/损害/使受伤",
  "Two workers were injured in the blast.|Smoking injures your lungs slowly.",
  "harm done to someone against what is right – 不按准来待人，落下的那份损伤",
  "使受伤：身上真被弄伤了|伤害：名誉、感情也这样被弄坏|损害：不限于人，利益与器物受损也用它")

w("injury", "noun", "/ˈɪndʒəri/", "jus",
  "in-（不）+ jur（jus 法、准）+ -y → 不照那把准来对待人，落在身上的那处结果",
  "中古英语 injurie ← 古法语 injurie ← 拉丁语 injuria（不法加于人的事）← in-（不）+ jus（属格 juris：法、权利）",
  "physical harm done to a person, or damage done to something",
  "手腕缠着白纱吊在胸前，医生纸上写着三周内不许用力",
  "伤/损伤/伤害",
  "He missed the season with a knee injury.|The crash caused injury to five people.",
  "the harm left on someone by a wrong – 不按准来待人之后留下的那处",
  "伤：身上那一处实在的破口或断处|损伤：程度轻重不论，身上或物上留下的坏处|伤害：名誉、感情上留下的那种，看不见但在")

w("instance", "noun", "/ˈɪnstəns/", "sta",
  "in-（就在近处）+ stance（sta 站立）→ 就站在眼前的那一个，随手举得出来",
  "古法语 instance ← 拉丁语 instantia（迫近、当前的事）← instare（立于其上、逼近）",
  "a single case of something happening, used as an example",
  "他随手一指桌上那张罚单，说规矩就是这么定的，满屋子人立刻不吭声了",
  "例子/实例/场合",
  "This is a clear instance of bad design.|In most instances the drug works well.",
  "the one standing right in front of you – 就立在眼前那一个",
  "例子：说事时顺手举出来的那一个|实例：真发生过的那一件，不是设想|场合：某一次具体的情形，多用复数",
  "", "for instance —— 例如，句中插入用来引出一个例子|in this instance —— 就这一次而言，指眼下这个具体情形")

w("intact", "adjective", "/ɪnˈtækt/", "tangere",
  "in-（不）+ tact（tangere 触碰）→ 一根手指也没碰过，所以一处不缺",
  "拉丁语 intactus（未经碰触的）← in-（不）+ tactus（碰过的，tangere 的过去分词）",
  "not damaged and with no part missing",
  "包裹在雨里泡了一夜，封条还压得严实，里头瓷杯连一道细纹都没有",
  "完好无损的/未受损的/原封的",
  "The vase arrived intact after the long trip.|His reputation remained intact after the trial.",
  "never touched, so nothing is missing – 没被碰过，所以一处不缺",
  "完好无损的：整件东西一处没坏|未受损的：名誉、体系受了冲击仍旧没坏|原封的：封着没动过，里头一样不少")

w("invalid", "adjective", "/ɪnˈvælɪd/", "valere",
  "in-（不）+ val（valere 有力、有效）→ 没有那股顶得住的劲 → 拿出去不管用",
  "拉丁语 invalidus（不强健的、无力的）← in-（不）+ validus（强健的）← valere（强壮、有效力）",
  "not legally or officially acceptable, or not based on sound reasoning",
  "票面日期是上个月的，闸口刷了三遍都红灯，人被拦在外面",
  "无效的/作废的/站不住的",
  "Your ticket is invalid after that date.|His argument rests on an invalid claim.",
  "having no force to hold up – 没有撑得住的那股劲",
  "无效的：拿出去不管用，机器和规矩都不认|作废的：本来管用，过期或撤销后不作数了|站不住的：说推理与论据，一推就塌")

w("invaluable", "adjective", "/ɪnˈvæljuəbl/", "valere",
  "in-（不能）+ valu（valere 估值）+ -able（可…的）→ 估不出价来，不是不值，而是贵得没法标价",
  "英语 valuable 加否定前缀 in- 构成；value ← 古法语 value ← 拉丁语 valere（有力、值）",
  "extremely useful or precious, beyond any price you could put on it",
  "老木匠留下的那本手记，几代人照着它做活，出多少钱他都不撒手",
  "极宝贵的/无价的",
  "Her advice was invaluable to the team.|The old maps are invaluable to historians.",
  "worth more than any price set on it – 值到没法给它标一个价",
  "极宝贵的：用处大得离不了|无价的：贵到标不出价，注意不是不值钱")

# ---------------- B 档 ----------------
w("hierarchy", "noun", "/ˈhaɪərɑːki/", "", "",
  "古法语 ierarchie ← 中世纪拉丁语 hierarchia ← 希腊语 hierarkhia（司祭的统辖），由 hieros（神圣的）与 arkhein（统辖）构成",
  "a system in which people or things are ranked one above another",
  "一张纸上画着树，最上头一个框，往下分两层，每个框只对上头一个人负责",
  "等级制度/层级/统治集团",
  "She rose quickly in the company hierarchy.|The files are stored in a strict hierarchy.",
  "ranks set one above another – 一层压一层地排定名次",
  "等级制度：人按高低排定，上管下的那套做法|层级：不指人，指结构上的一层层，如文件夹|统治集团：处在最上那几层的那些人")

w("horizon", "noun", "/həˈraɪzn/", "", "",
  "古法语 orizon ← 拉丁语 horizon ← 希腊语 horizōn（划界的那道圈），出自 horizein（划界）、horos（界）",
  "the line at which the earth and the sky appear to meet",
  "船一直往外开，最后只剩桅尖露在那条直线上，再看一眼就没了",
  "地平线/眼界/范围",
  "The sun sank below the horizon at seven.|Travel broadens a young person's horizons.",
  "the line that marks how far you can see – 划出你能看到多远的那道界",
  "地平线：天和地相接的那道界|眼界：见识也有这么一道界，多用复数|范围：谈论与打算所及的那一圈")

w("horizontal", "adjective", "/ˌhɒrɪˈzɒntl/", "", "",
  "法语 horizontal ← 拉丁语 horizon（划界的圈）← 希腊语 horizōn（划界的那道圈），出自 horizein（划界）",
  "flat and going from side to side, at a right angle to a vertical line",
  "水泥地上弹了一道墨线，小球放上去停着不动，两头一样高",
  "水平的/横的",
  "Draw a horizontal line across the page.|The bars are horizontal, not upright.",
  "lying flat along the line where earth meets sky – 顺着天地相接那道线躺平",
  "水平的：与那道界平行，不倾斜|横的：方向上左右走，与竖着相对")

w("hurricane", "noun", "/ˈhʌrɪkən/", "", "",
  "西班牙语 huracán ← 加勒比泰诺语 hurakán（风暴之神）",
  "a violent storm with very strong circling winds, especially in the Atlantic",
  "屋顶铁皮整张揭起来飞走，船被浪推上街，风声像有人拖着钢板过路",
  "飓风/暴风",
  "The hurricane destroyed hundreds of homes.|They boarded the windows before the hurricane.",
  "a whirling storm that tears things loose – 打着旋、把东西都撕下来的风暴",
  "飓风：大西洋上那种成旋的强风，有等级|暴风：泛指来势极凶的大风，不限地域")

w("illustration", "noun", "/ˌɪləˈstreɪʃn/", "", "",
  "拉丁语 illustratio（照明、显示）← illustrare（照亮、使显明）← in-（在上）+ lustrare（照）",
  "a picture in a book, or an example that makes something clear",
  "书页上配着一张剖开的图，箭头标到每一处，文字讲不清的地方一看就明白",
  "插图/说明/例证",
  "The book has fifty colour illustrations.|This case is a good illustration of the rule.",
  "light thrown on a thing so it can be seen – 打上一道光，让人看清那样东西",
  "插图：印在书里的那张图|说明：把道理照亮的那番讲解|例证：拿一件具体事去照亮抽象的道理")

w("imperative", "adjective / noun", "/ɪmˈperətɪv/", "imperare",
  "imperat（imperare 下令）+ -ive（带…性质的）→ 带着号令的性质，不容商量",
  "拉丁语 imperativus（命令式的）← imperare（下令、统辖）",
  "extremely urgent and necessary, or the verb form used to give orders",
  "他把话说得极短，没有一句留出回话的空，听的人只能照做",
  "紧急必需的/命令式的/必要之事",
  "It is imperative that we leave at once.|Use the imperative to give instructions.",
  "carrying the force of an order – 带着号令的那股不容商量",
  "紧急必需的：非做不可，语气近乎命令|命令式的：语法上专用来下令的那个式|必要之事：作名词，摆在面前不得不办的那一桩")

w("incorporate", "verb", "/ɪnˈkɔːpəreɪt/", "", "",
  "晚期拉丁语 incorporare（并成一体）← in-（进入）+ corpus（属格 corporis：身体）；本项目未为该族建根",
  "to include something as part of a larger whole",
  "改稿时把别人提的三条意见揉进正文，读下来看不出是后加的",
  "并入/纳入/包含",
  "We incorporated his ideas into the plan.|The new law incorporates several old rules.",
  "taken into one body – 收进同一个身子里",
  "并入：把外面的东西收进这个整体|纳入：条款、意见被收进来成为其中一条|包含：结果上就成了它的一部分，看不出接缝")

w("ingredient", "noun", "/ɪnˈɡriːdiənt/", "gradus",
  "in-（进去）+ gredi（gradus 走）+ -ent（…的东西）→ 一样样走进锅里的东西",
  "拉丁语 ingrediens（走进去的）← ingredi（走进去）← in-（进）+ gradi（走）",
  "any of the things that are combined to make a mixture or a dish",
  "台面上摊着面粉、糖、蛋和一小碟盐，一样样往盆里加",
  "成分/原料/要素",
  "Mix all the dry ingredients in a bowl.|Patience is a key ingredient of success.",
  "what walks into the mixture – 走进这一锅里的那一样",
  "原料：做菜做东西时投进去的那一样|成分：成品里含着的那一样，可以拆着说|要素：抽象的事也这样凑成，如成功的要素")

w("intimate", "adjective", "/ˈɪntɪmət/", "", "",
  "拉丁语 intimus（最里面的），intus（在内）的最高级；晚期拉丁语 intimare 表「使深知」，与 timidus（胆怯）那一支无关",
  "very close in friendship, or private and personal",
  "两人坐在灯下压着声音说话，讲的是没跟别人提过的那些事",
  "亲密的/私密的/详尽的",
  "They have been intimate friends for years.|He shared his most intimate thoughts.",
  "as far in as one can get – 一直到最里面那一层",
  "亲密的：交情深到进得了最里面那一层|私密的：只在最里头，不给外人看|详尽的：知道得到了里层，细处都清楚")

w("intimidate", "verb", "/ɪnˈtɪmɪdeɪt/", "", "",
  "中世纪拉丁语 intimidare（使胆怯）← in-（使）+ timidus（胆怯的）← timere（怕）；与 intimate 所本的 intimus（最里面的）不同源",
  "to frighten someone, especially in order to make them do what you want",
  "他一句话不说，只把椅子拖近半步，站着俯下身来看着对方",
  "恐吓/威胁/使胆怯",
  "They tried to intimidate the witness.|His size intimidates people at first.",
  "making someone go timid – 把人逼到发怯",
  "恐吓：明着来，要人怕|威胁：带着后果的压迫，逼人照办|使胆怯：不必开口，气势就让人退了半步")

w("intuition", "noun", "/ˌɪntjuˈɪʃn/", "", "",
  "晚期拉丁语 intuitio（凝视、直观）← intueri（往里看）← in-（向内）+ tueri（看、守望）",
  "the ability to know something without being told and without reasoning it out",
  "面试才聊两句，她心里已经定了不要这个人，讲不出是哪句话让她这么想",
  "直觉/直观",
  "She trusted her intuition and said no.|Good doctors rely partly on intuition.",
  "seeing a thing inwardly all at once – 不经中间步骤，往里一看就见着了",
  "直觉：没有推导就有的那个判断|直观：不借中间步骤地直接看见，多用于说方法")

# ---------------- C 档 ----------------
w("harassment", "noun", "/ˈhærəsmənt/", "", "",
  "法语 harassement ← harasser（骚扰、使疲于奔命）← 古法语 harer（放狗驱赶），更早词源不明",
  "repeated behaviour meant to trouble, threaten or annoy someone",
  "电话一天来七通，下楼买菜也有人跟着，事情不大但没一天清静",
  "骚扰/烦扰/侵扰",
  "She reported the harassment to her manager.|New rules aim to stop online harassment.",
  "being driven at again and again – 一遍遍地被撵着不放",
  "骚扰：一次次找上来，让人不得安宁|烦扰：程度轻些，搅得人心烦|侵扰：带上侵犯的意味，如性骚扰")

w("have", "verb", "/hæv/", "", "",
  "古英语 habban（持有、拿住）← 原始日耳曼语 *habjaną",
  "to own or hold something, to experience something, or to make something happen",
  "钥匙攥在他手里，口袋里还多一串，门开不开由他一句话",
  "有/持有/经历/使",
  "They have three children and a dog.|We had a long talk about it.",
  "the thing is in your hands – 那样东西就在你手上",
  "有：东西归你，在你手上|持有：正拿着、正掌着，强调握在手里|经历：一段事也这样落在你身上|使：安排别人去做，事情由你手里发出",
  "",
  "have sth done —— 让别人把某事做了，重点在结果不在谁做|have to do sth —— 不得不做，压力来自外部|have sb do sth —— 使唤某人做某事，主使者是你|have been doing sth —— 一直在做，动作从过去接到现在")

w("horsepower", "noun", "/ˈhɔːspaʊə/", "posse",
  "horse（马）+ power（posse 能成事的那股劲）→ 一匹马拉得动的那份力气，拿它做机器出力的尺子",
  "英语复合词 horse（古英语 hors，马）+ power；power ← 通俗拉丁语 potere ← 拉丁语 posse（能够）",
  "a unit for measuring the power of an engine",
  "说明书上标着一个数，意思是这台机器出的劲相当于多少匹畜生一起拉",
  "马力/功率",
  "This engine develops 200 horsepower.|The tractor has plenty of horsepower.",
  "as much pull as one horse can give – 一匹马能出的那份劲",
  "马力：量发动机出力的那个单位|功率：泛指出力的大小，口语里这么说")

w("household", "noun / adjective", "/ˈhaʊshəʊld/", "", "",
  "中古英语 houshold，由 hous（古英语 hūs，房子）与 hold（古英语 healdan 持守 → 掌管的那一摊）复合",
  "all the people living together in one house, or relating to the home",
  "一个屋顶下五口人，一口锅一本账，水电柴米都从这一份里出",
  "家庭/一家人/家用的",
  "The average household spends more on food.|She buys household goods in bulk.",
  "all that is held together under one roof – 一个屋顶下掌在一处的那一摊",
  "家庭：住在一起、账算在一处的这一户|一家人：这户里的那些人本身|家用的：作形容词，归这一摊日常用的")

w("how", "adverb", "/haʊ/", "", "",
  "古英语 hū（以何方式）← 原始日耳曼语 *hwō，与 who、what 同出一个疑问词干",
  "in what way, by what means, or to what degree",
  "他把螺丝拆下来举到灯下，问的是它当初怎么装上去的",
  "怎样/多么/如何",
  "Show me how you opened the locked door.|I forgot how cold it gets here.",
  "asking in what way or to what degree – 问的是走哪条路、到哪个份上",
  "怎样：问方式与路数，最常用|多么：接形容词表程度，多在感叹句里|如何：问情况与状态，语气偏正式",
  "",
  "how + adj/adv —— 多么…，问程度或作感叹，后面接主谓|how about doing sth —— …怎么样，用来提议或征询|how come + 主谓 —— 怎么会，口语里问原因，不倒装|know how to do sth —— 懂得怎么做，指方法上的会")

w("hunger", "noun / verb", "/ˈhʌŋɡə/", "", "",
  "古英语 hungor ← 原始日耳曼语 *hungruz",
  "the uncomfortable feeling caused by lack of food, or a strong wish for something",
  "下午三点还没吃上饭，胃里空得发紧，闻见楼下油烟就走不动路",
  "饥饿/渴望/渴求",
  "Many children still die of hunger.|He hungered for a word of praise.",
  "an empty place pulling to be filled – 空着的那处一直在拉扯",
  "饥饿：肚子空着的那种难受|渴望：名声、爱也这样空着拉扯人|渴求：作动词，为那样东西一直空着等着")

w("illustrate", "verb", "/ˈɪləstreɪt/", "", "",
  "拉丁语 illustrare（照亮、使显明）← in-（在上）+ lustrare（照）",
  "to make something clear by giving examples, or to add pictures to a book",
  "他在白板上画了三个圈两条线，绕了半天的道理一下就看清了",
  "说明/举例说明/为…配图",
  "Let me illustrate this with an example.|She illustrates children's books for a living.",
  "throwing light on a thing so it shows – 打一道光过去，让它显出来",
  "举例说明：拿具体的事去照亮抽象的话|说明：泛指把事情讲得让人看清|为…配图：给书页配上图，也是照亮文字")

w("interesting", "adjective", "/ˈɪntrəstɪŋ/", "praeesse",
  "inter-（在两者之间）+ est（esse 在）+ -ing → 这事横在我这边、与我有牵连，所以我上心",
  "英语 interest 加 -ing 构成；interest ← 古法语 interest ← 拉丁语 interest（interesse：夹在中间、有关系）",
  "holding your attention because it seems worth knowing about",
  "他讲的那段旧事，屋里人本来各干各的，后来都停下手看着他",
  "有趣的/引人注意的/耐人寻味的",
  "That was an interesting talk on birds.|She made an interesting point about cost.",
  "having a hold on you, so you attend to it – 与你搭上了牵连，你便上心",
  "有趣的：跟我搭上了关系，愿意听下去|引人注意的：把旁人的注意力拉过来|耐人寻味的：说法、现象值得多想一层")

w("internet", "noun", "/ˈɪntənet/", "", "",
  "二十世纪新造词，由 international（国际的）与 network（网络）缩合而成，1974 年起用于指互联的计算机网络",
  "the worldwide system of connected computer networks",
  "一根线插进墙上的口子，屏幕上就调得出地球另一头的一间图书馆",
  "互联网/因特网",
  "She looks everything up on the internet.|The internet was down all morning.",
  "networks of the whole world joined into one – 各国的网连成同一张",
  "互联网：连成一张的那整套网|因特网：同一样东西的音译叫法，偏正式")

# ---------------- 落盘前自检 ----------------
CJK = re.compile(r"[一-鿿]")
errs = []
roots = json.loads((ROOT / "data" / "roots.json").read_text(encoding="utf-8"))["roots"]
rids = {x["id"] for x in roots}
libwords = {x["word"] for x in
            json.loads((ROOT / "data" / "words.json").read_text(encoding="utf-8"))["words"]}
new_rids = {x[1] for x in R}
all_rids = rids | new_rids

src = (ROOT / "drafts" / "g_chunk108.txt").read_text(encoding="utf-8")
expected = [l.split("\t")[0].strip() for l in src.splitlines()
            if l.strip() and not l.startswith("#")]
got = [x[1] for x in W]
if expected != got:
    errs.append("词表不匹配 缺=%s 多=%s" % (sorted(set(expected) - set(got)),
                                            sorted(set(got) - set(expected))))

for x in R:
    if len(x) != 10:
        errs.append("R %s: %d 列" % (x[1], len(x)))
        continue
    if x[1] in rids:
        errs.append("R %s: 词根已存在" % x[1])
    if x[1] in libwords or x[1] in got:
        errs.append("R %s: 与单词同名" % x[1])
    if "/" not in x[4]:
        errs.append("R %s: core_concept 缺斜杠" % x[1])
    if not x[7].replace("-", "").isalpha() or x[7] != x[7].lower():
        errs.append("R %s: concept_slug 非小写英文" % x[1])
    for v in [y for y in x[2].split("/") if y]:
        for other in roots:
            if v in (other.get("variants") or []):
                errs.append("R %s: variant %s 与根 %s 撞" % (x[1], v, other["id"]))

for x in W:
    if len(x) != 15:
        errs.append("%s: %d 列" % (x[1], len(x)))
        continue
    (word, pos, ph, rid, logic, origin, native, image, zh, ex, concept,
     exps, hint, colloc) = x[1:]
    n = len(CJK.findall(image))
    if not (15 <= n <= 35):
        errs.append("%s: image %d 字，须 15-35" % (word, n))
    zl = [y.strip() for y in zh.split("/") if y.strip()]
    if not (1 <= len(zl) <= 4):
        errs.append("%s: 义项 %d 个" % (word, len(zl)))
    for y in zl:
        if len(y) >= 2 and y in image:
            errs.append("%s: image 含义项 %s" % (word, y))
    exl = [y.strip() for y in ex.split("|") if y.strip()]
    if len(exl) != 2:
        errs.append("%s: 例句 %d 条" % (word, len(exl)))
    for e in exl:
        c = len(e.split())
        if not (5 <= c <= 12):
            errs.append("%s: 例句 %d 词 -> %s" % (word, c, e))
        if not e.endswith("."):
            errs.append("%s: 例句无句号 -> %s" % (word, e))
    if len(zl) >= 2 and not exps:
        errs.append("%s: %d 义项无 expansions" % (word, len(zl)))
    if len(zl) >= 2 and len([y for y in exps.split("|") if y.strip()]) < len(zl):
        errs.append("%s: expansions 条数少于义项数" % word)
    if bool(rid) != bool(logic):
        errs.append("%s: root_ids 与 root_logic 不配对" % word)
    for y in [z.strip() for z in rid.split("/") if z.strip()]:
        if y not in all_rids:
            errs.append("%s: 根 %s 不存在" % (word, y))
    if rid:
        blanks = sum(logic.count(y) for y in zl if len(y) >= 2)
        if blanks >= 3 and not hint:
            errs.append("%s: root_logic 含 %d 处义项，须填 hint" % (word, blanks))
    if not (ph.startswith("/") and ph.endswith("/")):
        errs.append("%s: 音标 %s" % (word, ph))
    if "–" not in concept:
        errs.append("%s: concept 缺短破折号" % word)
    if word in libwords:
        errs.append("%s: 已在词库" % word)
    if word in all_rids:
        errs.append("%s: 与词根 id 同名" % word)
    if colloc and "——" not in colloc:
        errs.append("%s: colloc 缺分隔" % word)
    if any("\t" in c or "\n" in c for c in x):
        errs.append("%s: 字段内含制表符或换行" % word)

if errs:
    print("[BUILD-FAIL]")
    for e in errs:
        print("   ", e)
    raise SystemExit(1)

lines = ["\t".join(x) for x in R] + ["\t".join(x) for x in W]
OUT.write_text("\n".join(lines) + "\n", newline="\n", encoding="utf-8")
nr = sum(1 for x in W if x[4])
print("[BUILD-OK] R %d 行，W %d 行（词根型 %d，孤立/日耳曼型 %d）"
      % (len(R), len(W), nr, len(W) - nr))
