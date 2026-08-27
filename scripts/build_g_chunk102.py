#!/usr/bin/env python3
"""生成 drafts/g_chunk102.tsv。按列表 join，避免 Write 工具吃掉行尾制表符。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "drafts" / "g_chunk102.tsv"

# 每行 15 列：W word pos ph root_ids root_logic origin native image zh ex concept exps hint colloc
ROWS = []


def W(word, pos, ph, rid, logic, origin, native, image, zh, ex, concept, exps,
      hint="", colloc=""):
    ROWS.append(["W", word, pos, ph, rid, logic, origin, native, image, zh, ex,
                 concept, exps, hint, colloc])


# ---------- A 档：两个疑挂根都核为假阳性，退回孤立词条 ----------
W("coward", "noun", "/ˈkaʊəd/", "", "",
  "古法语 coart（缩着尾巴的那个）← coe / cue（尾巴）← 拉丁语 cauda，加贬义后缀 -ard；与拉丁语 ars（技艺）无关，同含 -ar- 只是拼写偶合",
  "a person who lacks the courage to face danger or pain",
  "狗见了人夹起尾巴往后退，主人一抬手它先钻到桌子底下",
  "胆小鬼/懦夫",
  "He was called a coward for running away.|Only a coward would hit a child.",
  "one who backs away when danger comes – 危险一来就往后缩的那个人",
  "胆小鬼：遇事就退、不敢往前的那一个|懦夫：该站出来时始终不肯站出来的人")

W("curtain", "noun", "/ˈkɜːtn/", "", "",
  "古法语 cortine ← 晚期拉丁语 cortina（帷幕）；与拉丁语 tenere（握住）、tangere（触）都不同源，拼作 -tain 纯属偶合，更早词源不明",
  "a piece of hanging cloth that covers a window or a stage",
  "一块布沿轨道拉过去，窗外的光一下被挡住，屋里暗下来",
  "窗帘/幕布",
  "She drew the curtains before turning on the light.|The curtain rose and the play began.",
  "hanging cloth that shuts off what is behind – 挂起来把后面遮断的那块布",
  "窗帘：挡在窗户上的那块布，拉上就看不见外头|幕布：戏台前面那块大布，升起来戏才开始")

# ---------- B 档：核出的假阴性，挂库中已有根 ----------
W("compliment", "noun / verb", "/ˈkɒmplɪmənt/", "plere",
  "com-（完全）+ pli（plere 填满）+ -ment（物）→ 把礼数填够的那句话",
  "意大利语 complimento ← 西班牙语 cumplimiento（礼数尽到）← 拉丁语 complere（填满）；与 complement 同出一源，后来分写两形",
  "a remark that expresses praise or admiration",
  "有人夸你今天这身衣服好看，你听着不好意思又高兴",
  "赞美/夸奖/致意",
  "She paid him a compliment on his cooking.|He complimented her on the fine speech.",
  "words that fill out what courtesy asks for – 把礼数填满的那句话",
  "赞美：把好话说到位，听的人受用|夸奖：当面说对方哪里做得好|致意：见面时把该有的客套话补上")

W("conjunction", "noun", "/kənˈdʒʌŋkʃn/", "jungere",
  "con-（一同）+ junct（jungere 套到一处）+ -ion（事）→ 把两边套在同一副轭里的那一处",
  "拉丁语 coniunctio ← coniungere：com-（一同）+ iungere（套到一处），过去分词 iunctus",
  "a word that links two clauses, or the state of things happening together",
  "两个句子中间放一个小词，前后就接成一句话",
  "连词/结合/同时发生",
  "And is the commonest conjunction in English.|The two events happened in conjunction.",
  "the piece that yokes two parts into one – 把两部分套进同一副轭的那一处",
  "连词：夹在两句之间把它们接起来的那个词|结合：两样东西合到一处的状态|同时发生：两件事凑在同一时候一起来")

W("contaminate", "verb", "/kənˈtæmɪneɪt/", "tangere",
  "con-（一同）+ tam（tangere 触）+ -inate（使…）→ 挨上了就跟着变脏",
  "拉丁语 contaminare（弄脏）← contamen（接触、染上）← con-（一同）+ tangere 的词干 tag-（触）",
  "to make something dirty or harmful by adding a bad substance",
  "一滴墨掉进整桶清水，水色立刻发灰，整桶都不能喝了",
  "污染/弄脏/带坏",
  "The leak contaminated the town water supply.|Do not let raw meat contaminate the salad.",
  "spoiling a thing by letting a bad one touch it – 让脏东西挨上，整样就跟着坏",
  "污染：坏东西掺进来，整批都不能用|弄脏：挨上一点就沾了，擦不干净|带坏：人挨着人，坏习气也跟着传过去")

W("convey", "verb", "/kənˈveɪ/", "via",
  "con-（一同）+ vey（via 路）→ 一路陪着送过去",
  "古法语 conveier（护送上路）← 通俗拉丁语 conviare：com-（一同）+ via（路）",
  "to carry something from one place to another, or to make an idea known",
  "传送带把箱子一路送到另一头，也能把一个眼神递到对面",
  "运送/传达/表达",
  "Pipes convey water to the whole village.|Her face conveyed more than her words.",
  "taking a thing along the road to the other end – 顺着路把东西带到那一头",
  "运送：把货物顺路带到目的地|传达：把话或消息一路递到人手里|表达：把心里的意思送到对方那边去")

W("decisive", "adjective", "/dɪˈsaɪsɪv/", "caedere",
  "de-（去掉）+ cis（caedere 切）+ -ive（有…性质的）→ 一刀切下去，再不回头",
  "法语 décisif ← 中世纪拉丁语 decisivus ← 拉丁语 decidere：de-（去掉）+ caedere（切）",
  "settling a question, or able to make choices quickly and firmly",
  "会开到一半有人拍下桌子定了方案，散会后没人再提别的",
  "决定性的/果断的",
  "That goal was decisive in the final.|A good leader must be decisive.",
  "cutting the matter off so it cannot drag on – 一刀切断，事情不再拖",
  "决定性的：这一下切下去，结局就定了|果断的：该切就切，不在两头之间来回")

W("desirable", "adjective", "/dɪˈzaɪərəbl/", "sidus",
  "de-（离开）+ sir（sidus 星）+ -able（可…的）→ 值得抬头去望的那一个",
  "古法语 desirable ← 拉丁语 desiderabilis ← desiderare（渴望）← de- + sidus（星）",
  "worth having or wanting because of its qualities",
  "招聘栏里那个岗位人人都投，工资和地点都挑不出毛病",
  "令人向往的/可取的",
  "A quiet flat is highly desirable here.|Fluent Japanese is desirable for this post.",
  "worth reaching up toward – 值得伸手去要的那一样",
  "令人向往的：一看见就想要，人人都盯着|可取的：条件上站得住，值得选它")

W("destiny", "noun", "/ˈdestɪni/", "sta",
  "de-（彻底）+ stin（sta 立定）+ -y（名词）→ 早就立定在那里、挪不动的那一条",
  "古法语 destinee ← 拉丁语 destinata ← destinare（立定、钉住）← de- + stare（站立）的使动一支",
  "the events that will happen to someone, seen as already fixed",
  "一条路上早钉好了木桩，走到哪一步都绕不开那几个桩子",
  "命运/天命",
  "She believed it was her destiny to teach.|No one can escape his own destiny.",
  "what has been stood firm in advance – 事先立定、不再移动的那一条",
  "命运：一生里绕不开的那条线|天命：被认作上头早已定下、由不得自己的安排")

W("elegant", "adjective", "/ˈelɪɡənt/", "legere",
  "e-（从中）+ leg（legere 挑选）+ -ant（…的）→ 一样样挑出来的，才这么讲究",
  "拉丁语 elegantem ← eligere（挑选出来）：ex-（从中）+ legere（拣选）",
  "pleasingly graceful and simple in style or appearance",
  "一身素色衣服剪裁贴身，只戴一只细表，进屋人人回头看",
  "优雅的/雅致的/简洁的",
  "She wore an elegant black dress.|He found an elegant solution to the problem.",
  "made of picked-out choices, nothing left in by accident – 每一处都是挑过的，没有多余",
  "优雅的：举止和穿着都挑过，看着舒服|雅致的：器物花样不多而处处得当|简洁的：办法或证明里没有一步是多的")

W("eligible", "adjective", "/ˈelɪdʒəbl/", "legere",
  "e-（从中）+ lig（legere 挑选）+ -ible（可…的）→ 可以被从人堆里挑出来的",
  "晚期拉丁语 eligibilis（可选出的）← 拉丁语 eligere：ex-（从中）+ legere（拣选）",
  "having the right qualities or conditions to be chosen or allowed",
  "报名表交上去，工作人员照条件核对一遍，在名字后打了勾",
  "符合条件的/有资格的",
  "Only members are eligible for the discount.|She is eligible to apply this year.",
  "fit to be picked out of the group – 条件够得上，能被挑出来",
  "符合条件的：门槛上的每一条都对得上|有资格的：够格进这个名单，可以来领或来考")

W("emotion", "noun", "/ɪˈməʊʃn/", "mov",
  "e-（向外）+ mot（mov 动）+ -ion（事）→ 心里被搅动起来的那一下",
  "法语 émotion ← 拉丁语 emotio ← emovere：ex-（向外）+ movere（动）",
  "a strong feeling such as joy, anger, or fear",
  "听到那句话，胸口猛地一紧，手抖得握不住杯子",
  "情绪/情感/激动",
  "He spoke with real emotion about his father.|She tried to hide her emotions.",
  "something inside stirred out of its rest – 心里原本静着的东西被搅动起来",
  "情绪：心里一时被搅起的那个状态|情感：长久存着、遇事就动的那一份|激动：动得厉害，身上也跟着显出来")

# ---------- B 档：库中确实无根，按孤立词条写 ----------
W("corporation", "noun", "/ˌkɔːpəˈreɪʃn/", "", "",
  "拉丁语 corporatio ← corporare（结成一个整体）← corpus（属格 corporis：身体）；本项目未为 corpus 一族建根",
  "a large business or group that the law treats as a single body",
  "几千人分散在各地上班，对外只用一个名字签合同",
  "公司/法人团体",
  "He works for a large oil corporation.|The corporation was fined for the spill.",
  "many people counted as one body before the law – 一群人在法律上算作一个身体",
  "公司：合起来做买卖的那个整体|法人团体：法律上当成一个人来对待的那一群")

W("couple", "noun / verb", "/ˈkʌpl/", "", "",
  "古法语 cople ← 拉丁语 copula（把两样系在一起的带子）← co-（一同）+ apere（系住）；本项目未为 copula 一族建根",
  "two people or things taken together, or to join two things",
  "两只手扣在一起，也可以是两节车厢挂上同一个钩",
  "一对/夫妻/连接",
  "A young couple moved in next door.|They coupled the two carriages together.",
  "two things tied so they go as one – 两样被系住，从此一同走",
  "一对：数目上凑成两个的那一组|夫妻：结成一家的那两个人|连接：把两样挂上同一个扣")

W("court", "noun", "/kɔːt/", "", "",
  "古法语 cort ← 拉丁语 cohortem（围起来的院子）：co-（一同）+ hort-（围场，与 hortus 花园同支）；本项目未为 cohors 一族建根",
  "a place where legal cases are heard, or an enclosed area for a ball game",
  "四面围起来的一块空地，中间画着线，边上坐着一排人看着",
  "法庭/球场/宫廷",
  "The case will go to court next month.|They booked a tennis court for Sunday.",
  "an enclosed yard where a fixed business is settled – 围起来的一块地，事情在里面按规矩了断",
  "法庭：围起来的那间屋子，是非在里面判定|球场：围起来画好线的那块地，按规矩打球|宫廷：君主住的那个大院，臣子在里面听差")

W("curve", "noun / verb", "/kɜːv/", "", "",
  "拉丁语 curvus（弯的），名词一支经拉丁语 curva（弯线）入英语；本项目未为 curvus 一族建根",
  "a line or surface that bends smoothly without any sharp angle",
  "公路顺着山脚一路弯过去，没有一个直角",
  "曲线/弯道/弯曲",
  "The road curves sharply to the left.|She drew a smooth curve on the paper.",
  "a line that bends without breaking – 一条不带折角地弯过去的线",
  "曲线：图纸上圆顺地弯着的那条线|弯道：路上转过去的那一段|弯曲：让直的东西弯过来这个动作")

W("demonstrate", "verb", "/ˈdemənstreɪt/", "", "",
  "拉丁语 demonstrare（指明给人看）：de-（彻底）+ monstrare（指示）← monstrum（示警之物）← monere（提醒）；本项目未为 monere 一族建根",
  "to show clearly how something works or that something is true",
  "店员把机器搬到台前，当众按一遍键，让围观的人看清每一步",
  "演示/证明/示威",
  "He demonstrated the machine to the buyers.|The results demonstrate that the method works.",
  "putting a thing where all can see it plainly – 摆到众人眼前，一步步指给人看",
  "演示：当面做一遍给人看清楚|证明：把根据摊开，让人不得不信|示威：一群人走到街上，把主张摆给众人看")

W("dilute", "verb / adjective", "/daɪˈluːt/", "", "",
  "拉丁语 dilutus ← diluere：dis-（分开）+ luere（洗、冲）；luere 与 lavare（洗）同支，本项目未为这一族建根",
  "to make a liquid thinner or weaker by adding water",
  "一勺蜂蜜倒进整壶水里搅开，尝一口几乎没味道了",
  "稀释/冲淡/减弱",
  "Dilute the paint with a little water.|Too many members diluted her influence.",
  "washing a thing out until it is thin – 兑水冲开，浓的变淡",
  "稀释：加水进去，浓度降下来|冲淡：颜色或味道被水带走一部分|减弱：不限液体，力量或影响也能被摊薄")

W("embarrass", "verb", "/ɪmˈbærəs/", "", "",
  "法语 embarrasser（阻住、使为难）← 西班牙语 embarazar ← barra（横杠）；barra 更早词源不明",
  "to make someone feel awkward and self-conscious",
  "当着一屋子人说错了对方名字，脸一下发烫，话接不下去",
  "使窘迫/使难为情",
  "His question embarrassed the whole table.|She was embarrassed by the loud praise.",
  "a bar thrown across so one cannot go on – 前面横上一杠，人卡在那里",
  "使窘迫：让人当场卡住，不知怎么接|使难为情：戳到不好意思的地方，脸上挂不住")

# ---------- C 档 ----------
W("coordinates", "noun", "/kəʊˈɔːdɪnəts/", "ordinare",
  "co-（一同）+ ordin（ordinare 排成序）+ -ate（使…）→ 两把尺排进同一套次序，交出一个位次",
  "拉丁语 co-（一同）+ ordinare（排列成序）← ordo（行列、次序）",
  "a set of numbers that fix the position of a point on a map or graph",
  "地图上横竖两把尺交出一格，报出两个数就找得到那一点",
  "坐标",
  "He gave us the coordinates of the camp.|Enter the coordinates into the ship's computer.",
  "numbers set in one shared order to fix a point – 放进同一套行列里，用来定住一个点",
  "坐标：两条互相垂直的尺各报一个数，点的位置就定下来了")

W("country", "noun", "/ˈkʌntri/", "", "",
  "古法语 contree ← 通俗拉丁语 contrata（terra）（迎面铺开的那片地）← 拉丁语 contra（对面、正对着）；是拉丁借词而非日耳曼词，本项目未为 contra 一族建根",
  "a nation with its own government, or land away from towns",
  "站在坡上往前看，一整片田野铺到天边，远处立着一道界碑",
  "国家/乡下/地区",
  "She has visited over thirty countries.|They moved to the country last spring.",
  "the stretch of land lying out in front of you – 摊在面前的那一整片地",
  "国家：一片地连着住在上面的人和管事的政府|乡下：城外那一片田野和村子|地区：一整片连着的地面，按地势或用途分开说")

W("courtyard", "noun", "/ˈkɔːtjɑːd/", "", "",
  "中古英语 court（← 古法语 cort ← 拉丁语 cohortem 围起来的院子）+ yard（← 古英语 geard 围场）；前半是拉丁借词，后半是日耳曼词，两个同义成分叠在一起",
  "an open space enclosed by the walls of a building",
  "四面墙围出一块露天空地，中间一口井，晾着几件衣服",
  "庭院/天井",
  "Children were playing in the courtyard.|The hotel has a quiet inner courtyard.",
  "open ground fenced in on every side – 四面拦住、中间露天的一块地",
  "庭院：房子围出来的那块空地，自家人在里面走动|天井：屋子中间留出的一小方露天，光从上头下来")

W("cupboard", "noun", "/ˈkʌbəd/", "", "",
  "中古英语 cupborde：cup（← 古英语 cuppe ← 晚期拉丁语 cuppa 杯）+ board（← 古英语 bord 板）；本义是摆杯盘的那层板，前半是经古英语传入的拉丁借词",
  "a piece of furniture with doors and shelves for storing things",
  "厨房墙上一排带门的格子，拉开门里面摞着盘子和罐头",
  "橱柜/壁橱",
  "The plates are in the kitchen cupboard.|She hid the box in a cupboard.",
  "shelf boards shut behind a door – 关在门后的那几层板",
  "橱柜：带门带层板，用来收放东西的家具|壁橱：嵌在墙里的那一种，不占地方")

W("curse", "noun / verb", "/kɜːs/", "", "",
  "古英语 curs（诅咒的话），更早词源不明；与拉丁语 cursus（跑）同形而无关",
  "a word or wish calling harm down on someone, or to swear at someone",
  "有人朝着背影狠狠说了一句狠话，旁边的人听了直摇头",
  "诅咒/咒骂/祸根",
  "He cursed loudly and slammed the door.|She believed the old house was under a curse.",
  "harsh words sent out to bring harm down – 放出一句话，要祸事落到那人头上",
  "诅咒：说出话来盼对方遭祸|咒骂：气头上骂出难听的话|祸根：像被那句话缠上一样，长久跟着的坏运")

W("diagnose", "verb", "/ˈdaɪəɡnəʊz/", "", "",
  "希腊语 diagignoskein（分辨清楚）：dia-（透过、分开）+ gignoskein（认知），经晚期拉丁语 diagnosis 入英语；是希腊借词而非日耳曼词。库中 gnoscere 根收的是拉丁一支，与本词同出印欧语「知」一根而分支不同，照 regula 与 rect 的先例不合并",
  "to find out what illness or fault someone or something has",
  "医生把片子举到灯前看了半分钟，在单子上圈出一处",
  "诊断/判定病因",
  "Doctors diagnosed a rare blood disorder.|The engineer diagnosed the fault in minutes.",
  "telling one thing apart from another until the cause is named – 一样样分开辨，直到认出是哪一种",
  "诊断：看过症状和片子，认定是哪一种病|判定病因：不限人身上，机器毛病出在哪也这么找")

W("downstairs", "adverb / adjective", "/ˌdaʊnˈsteəz/", "", "",
  "中古英语 doun（← 古英语 of dūne 从高处下来）+ stairs（← 古英语 stǣger 台阶）；两半都是日耳曼词，本是短语后写成一词",
  "on or to a lower floor of a building",
  "脚步声顺着台阶一级级往下，最后停在门厅的地板上",
  "楼下/往楼下",
  "She ran downstairs to answer the door.|The downstairs windows were all shut.",
  "down the steps to the floor below – 顺台阶下到底下那一层",
  "楼下：底下那一层，就在台阶下头|往楼下：动作朝下面那一层去")

W("earthquake", "noun", "/ˈɜːθkweɪk/", "", "",
  "中古英语 erthequake：earth（← 古英语 eorþe 土地）+ quake（← 古英语 cwacian 抖动）；两半都是日耳曼词",
  "a sudden violent shaking of the ground",
  "吊灯突然乱晃，杯子从桌沿滑下去，墙上裂开一条缝",
  "地震",
  "The earthquake destroyed hundreds of homes.|A strong earthquake struck the coast at dawn.",
  "the ground itself shaking underfoot – 脚底下那片地自己抖起来",
  "地震：地面自己抖动，上面的东西跟着乱")

W("edible", "adjective", "/ˈedəbl/", "", "",
  "晚期拉丁语 edibilis ← 拉丁语 edere（吃）——与库中 edere-publish 那个同形的 edere（ex＋dare 交出）无关，勿混；是拉丁借词而非日耳曼词，本项目未为「吃」这一支建根",
  "fit or safe to be eaten",
  "野地里两朵相似的菌子，本地人拿起一朵咬了一口，另一朵扔开",
  "可食用的/能吃的",
  "Not every wild berry is edible.|The flowers are edible and slightly sweet.",
  "safe to put in the mouth – 放进嘴里没问题的那一样",
  "可食用的：性质上没毒，人能拿来当食物|能吃的：眼前这一份没坏、下得了口")

W("elsewhere", "adverb", "/ˌelsˈweə(r)/", "", "",
  "古英语 elles（另外地）+ hwær（何处）；两半都是日耳曼词，中古英语时合成一词",
  "in, at, or to some other place",
  "这家店门口贴着告示，要买的那样东西得往下一条街去问",
  "在别处/到别处",
  "The book is not here; look elsewhere.|Many workers went elsewhere for better pay.",
  "at some other place than this one – 不在这儿，在另外的地方",
  "在别处：人或物不在眼下这个地方|到别处：动作朝另一个地方去")

# ---------- 落盘前自检 ----------
POS_OK = {"noun", "verb", "adjective", "adverb", "preposition", "conjunction", "pronoun"}
seen = set()
for r in ROWS:
    assert len(r) == 15, ("列数错", r[1], len(r))
    tag, word, pos, ph, rid, logic, origin, native, image, zh, ex, concept, exps, hint, colloc = r
    assert word not in seen, ("重复词", word)
    seen.add(word)
    assert ph.startswith("/") and ph.endswith("/"), ("音标", word, ph)
    for p in pos.split("/"):
        assert p.strip() in POS_OK, ("词性", word, p)
    zh_list = [x.strip() for x in zh.split("/") if x.strip()]
    assert 1 <= len(zh_list) <= 4, ("义项数", word, zh_list)
    n = len(image)
    assert 15 <= n <= 35, ("image 字数", word, n)
    for x in zh_list:
        assert not (len(x) >= 2 and x in image), ("image 泄题", word, x)
    ex_list = [x.strip() for x in ex.split("|") if x.strip()]
    assert len(ex_list) == 2, ("例句数", word, len(ex_list))
    for s in ex_list:
        assert s.endswith("."), ("例句缺句号", word, s)
        nw = len(s.rstrip(".").split())
        assert 5 <= nw <= 12, ("例句词数", word, nw, s)
    exp_list = [x.strip() for x in exps.split("|") if x.strip()]
    if len(zh_list) >= 2:
        assert exp_list, ("多义项缺 expansions", word)
    assert "–" in concept, ("concept 缺短破折号", word)
    assert bool(rid) == bool(logic), ("root_ids 与 root_logic 须同有同无", word)
    if rid:
        blanks = sum(logic.count(x) for x in zh_list if len(x) >= 2)
        assert blanks < 3 or hint, ("root_logic 含 3 处义项须填 hint", word, blanks)
    if colloc:
        assert "——" in colloc, ("搭配格式", word)
    assert "\t" not in "".join(r), ("字段内含制表符", word)

txt = "\n".join("\t".join(r) for r in ROWS) + "\n"
OUT.write_text(txt, encoding="utf-8", newline="\n")
print("[BUILD] %d 行 -> %s" % (len(ROWS), OUT))
print("  挂根 %d，孤立 %d" % (sum(1 for r in ROWS if r[4]), sum(1 for r in ROWS if not r[4])))
