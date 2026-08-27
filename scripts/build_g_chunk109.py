# -*- coding: utf-8 -*-
"""按列表 join 生成 drafts/g_chunk109.tsv —— 不用 Write，尾列制表符才留得住。

本片 0 新根，5 个补词（judicial/judgement→jus、lesson→legere、letter→littera、
liability→ligare），其余 25 词按孤立/日耳曼型写。

A 档六个可疑的全部核不成立（level←libra 非 liber、litter←lectus 非 littera、
lantern←lampein 非 cernere、latent←latere 非 tendere、leg←古诺尔斯 leggr、
light←古英语 lēoht/līht）。另加一个 prompt 未点出的：library/librarian ← liber
「书」，而库中 liber 根的 origin 与 5 员全是「自由」那一支，属近形异源，不挂。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "drafts" / "g_chunk109.tsv"

R = []
W = []


def r(rid, variants, origin, cc, image, edef, slug, czh, dom):
    R.append(["R", rid, variants, origin, cc, image, edef, slug, czh, dom])


def w(word, pos, ph, rids, logic, origin, native, image, zh, ex, concept,
      exps, hint="", colloc=""):
    W.append(["W", word, pos, ph, rids, logic, origin, native, image, zh, ex,
              concept, exps, hint, colloc])


# ================= A 档 =================

w("judicial", "adjective", "/dʒuːˈdɪʃl/", "jus",
  "judic（jus 法、准 → judex 宣法的人）+ -ial（属…的）→ 归那套宣法程序管着的",
  "古法语 judicial ← 拉丁语 judicialis（法庭的、审断的）← judicium（审断）"
  "← judex（法官）← jus（属格 juris：法、权利）",
  "relating to courts of law, to judges, or to the process of judging",
  "穿黑袍的人坐在高台后，敲一下木槌，底下两边立刻停止争辩",
  "司法的/法院的/审判的",
  "The judicial system needs urgent reform.|The case went through a judicial review.",
  "belonging to the courts that judge – 归那套依准断案的机构所有",
  "司法的：整套依法断案的机构与程序都这么叫|法院的：出自法院、由法院做出的|审判的：专指断案那个过程本身，如审判权")

w("lantern", "noun", "/ˈlæntən/", "", "",
  "古法语 lanterne ← 拉丁语 lanterna ← 希腊语 lampter（灯、火把）← lampein（发光）；"
  "与 cernere（筛分、辨别）无关，形近而已",
  "a lamp with a case around it so it can be carried and used outdoors",
  "一圈薄纸罩着里头那点火苗，风大也不灭，手提着走夜路脚边亮一小块",
  "灯笼/提灯",
  "He carried a lantern down the path.|Red lanterns hung along the street.",
  "a small flame housed so wind cannot reach it – 把火苗关在罩里，风吹不着",
  "灯笼：纸或绸糊的罩子，节日里挂起来|提灯：金属玻璃做的那种，能拎着照路")

w("latent", "adjective", "/ˈleɪtnt/", "", "",
  "拉丁语 latens（潜伏着的），是 latere（躺着不露、藏起来）的现在分词；"
  "与 tendere（伸展）无关",
  "present but not yet active or visible",
  "种子在冻土里躺了整个冬天，地面上什么也看不出，开春一夜冒出芽",
  "潜在的/潜伏的",
  "The virus can stay latent for years.|She has a latent talent for music.",
  "lying hidden, not yet showing – 躺着藏起来，还没露头",
  "潜在的：本事、可能性都在，只是还没使出来|潜伏的：病与危险这样藏着，到时候才发作")

w("leg", "noun", "/leɡ/", "", "",
  "中古英语 leg ← 古诺尔斯语 leggr（腿、骨的空腔），取代了古英语的 sceanca；"
  "与拉丁语 legere（读、拣选）同形而无关",
  "one of the limbs an animal or person stands and walks on",
  "一条从髋垂到脚踝的支撑，人站着靠它，桌子靠四根木杆同理",
  "腿/支腿/赛段",
  "He broke his left leg while skiing.|The last leg of the trip was long.",
  "the upright that carries the weight – 承着重量的那根直撑",
  "腿：身上那两条，用来站与走|支腿：桌椅底下那几根木杆或铁杆，同一个道理|赛段：一整段路程或比赛的其中一截，一段接一段往前")

w("lesson", "noun", "/ˈlesn/", "legere",
  "less（legere 的读义，经 lectio 一段诵读）+ -on → 一次念下来、听进去的那一段",
  "古法语 leçon ← 拉丁语 lectio（诵读、朗读的那一段）← legere（拾取、挑选、读）",
  "a period of teaching, or something learned from experience",
  "老师在黑板上写完最后一行，铃响了，本子上多出三页字",
  "课/一节课/教训",
  "We have three piano lessons each week.|His failure taught him a hard lesson.",
  "one stretch read out and taken in – 一次念下来、听进去的那一段",
  "课：学校里按科目分的那一门|一节课：按钟点算的那一段时间|教训：吃过亏之后学到的那一条，不在课堂上")

w("letter", "noun", "/ˈletə/", "littera",
  "lett（littera 字母、文字）+ -er → 一个个写下来的记号；攒成一整张寄出去的也叫它",
  "古法语 letre ← 拉丁语 littera（字母、文字），复数 litterae 指书信",
  "a written sign standing for a sound, or a written message sent to someone",
  "信封上一个个手写的符号排成人名，贴上票，投进街角那只铁箱",
  "字母/信/信件",
  "Write your name in capital letters.|She posted the letter this morning.",
  "a written mark, and a sheet made of them – 写下来的那个记号，攒成一张",
  "字母：拼写用的那一个个记号|信：写满了这些记号、封起来寄给人的那一张|信件：同一样东西的正式说法，多用于统称")

w("level", "noun / adjective", "/ˈlevl/", "", "",
  "古法语 livel ← 通俗拉丁语 *libellus ← 拉丁语 libella（小水准器），是 libra（天平、秤）"
  "的指小形；与 liber（自由的）不同源",
  "a height or standard reached, or flat with no part higher than another",
  "一根管里的气泡走到正中两道刻线之间，木板两头才算一样高",
  "水平/水准/级别/平的",
  "The water rose to a dangerous level.|Put the box on level ground.",
  "measured true against a balance – 拿秤那样比出来的一条准线",
  "水平：拿准线量出来的那个高度|水准：本事与质量也这样量，如英语水准|级别：一层层比出来的那一档|平的：两头一样高，看不出倾斜")

w("liability", "noun", "/ˌlaɪəˈbɪləti/", "ligare",
  "li（ligare 捆住）+ -able（能…的）+ -ity（名词）→ 被绳系在某事上脱不开的那个状态",
  "英语 liable 加 -ity 构成；liable ← 盎格鲁法语 liable ← 古法语 lier（捆、系）"
  "← 拉丁语 ligare（捆、绑住）",
  "legal responsibility for something, or a person or thing that causes trouble",
  "签完字那一刻，后果就一头系在他手腕上，甩不掉也转不出去",
  "责任/债务/累赘",
  "The company denies liability for the damage.|His temper is a liability to the team.",
  "tied to a thing you cannot slip out of – 被系在一件事上，抽不出手",
  "责任：法律上系在你身上、必须担的那一份|债务：欠出去的钱也这样系着，多用复数|累赘：人或事拖着你走不快，反过来成了负担")

w("library", "noun", "/ˈlaɪbrəri/", "", "",
  "古法语 librairie（书摊、藏书处）← 拉丁语 librarium（放书的箱柜）← liber（书，本义树的"
  "内皮）；与库中「自由」那一支的 liber 同形而不同源，不属该族",
  "a building or room where books are kept for people to read or borrow",
  "一排排高到顶的架子，书脊上贴着编号，翻页的声音是屋里最大的动静",
  "图书馆/藏书/库",
  "She borrowed three novels from the library.|He has a fine library of old maps.",
  "a chest for books grown into a building – 装书的箱柜大成了一整座屋子",
  "图书馆：供人借阅的那个地方|藏书：某人手里收着的那一批书本身|库：程序里现成可调用的那一套，也借这个说法")

w("light", "noun / adjective / verb", "/laɪt/", "", "",
  "「明亮」义出自古英语 lēoht ← 原始日耳曼语 *leuhtam；「不重」义出自古英语 līht "
  "← 原始日耳曼语 *līhtaz（不沉的）；两支都非拉丁借入",
  "the brightness that lets us see, not heavy in weight, or to set something burning",
  "拉开窗帘，屋里一下能看清桌上的东西；手边那盒泡沫一只手就掀起来了",
  "光/轻的/明亮的/点燃",
  "The light from the window was weak.|This bag is very light to carry.",
  "what lets you see, and what weighs almost nothing – 让人看得见的那样东西，和几乎不压手的那种",
  "光：让人看得见的那样东西|明亮的：那样东西多的时候，屋子就这样|轻的：另一支来源，手一提就起来，不压手|点燃：作动词，给它添上那样东西")

w("litter", "noun / verb", "/ˈlɪtə/", "", "",
  "盎格鲁法语 litere（卧铺、担架）← 古法语 litiere ← 中世纪拉丁语 lectaria ← 拉丁语 "
  "lectus（床、卧榻）；与 littera（字母）无关，同片的 letter 才属那一支",
  "small pieces of rubbish left lying about, or all the young born at one time",
  "棚里地上铺着一层干草，草窝里挤着刚生下的几只小东西，窝边还散着人丢的碎纸",
  "垃圾/一窝幼崽/乱丢",
  "Please do not drop litter in the park.|The cat had a litter of five.",
  "straw strewn on the ground to lie on – 摊在地上供躺卧的那一层草",
  "一窝幼崽：睡在同一处草窝里的那一批|垃圾：地上散摊着的那些碎纸杂物，同样是摊开的|乱丢：作动词，把那些东西摊满一地")

# ================= B 档 =================

w("investigate", "verb", "/ɪnˈvestɪɡeɪt/", "", "",
  "拉丁语 investigare（循着脚印追查）：in-（朝着）+ vestigium（脚印、足迹）；"
  "与 vestis（衣服）那一支不同源",
  "to try to find out the truth about something by examining it carefully",
  "雪地上一行脚印往林子里去，两个人跟着一步步走，走到印子断掉的地方蹲下来",
  "调查/侦查/研究",
  "Police are investigating the cause of the fire.|Scientists investigate how memory works.",
  "following the footprints back to the source – 顺着脚印一路追到源头",
  "调查：一步步查明一件事的经过|侦查：警方查案时那样追下去|研究：学问上也这么追，顺着线索往回找")

w("invitation", "noun", "/ˌɪnvɪˈteɪʃn/", "", "",
  "拉丁语 invitatio（请人前来）← invitare（邀请）；invitare 更早词源不明，"
  "与 venire（来）并非同源",
  "a spoken or written request asking someone to come somewhere or do something",
  "信箱里躺着一张烫金边的硬卡片，上头写着日子和地点，末尾一行小字请你回话",
  "邀请/请帖/招致",
  "She sent out fifty wedding invitations.|He came at my invitation.",
  "a request held out for someone to accept – 递到人面前、等他接的那一份请求",
  "邀请：请人来的这个举动本身|请帖：写着日子地点的那张卡片|招致：把不好的东西也这样请了来，如招致批评")

w("jacket", "noun", "/ˈdʒækɪt/", "", "",
  "古法语 jaquet（短外衣），是 jaque（农人穿的短上衣）的指小形，更早词源不明；"
  "与 jacere（投、扔）无关",
  "a short coat that reaches to the waist or hips",
  "挂在椅背上的那件短外衣，袖口磨白了，胸前一排扣子只扣着中间两颗",
  "夹克/短外套",
  "He hung his jacket on the chair.|She wore a leather jacket to work.",
  "a coat cut short at the waist – 齐腰剪断的那件外衣",
  "夹克：收口在腰上的那种短外衣|短外套：泛指长度到腰胯的外面那一层")

w("latitude", "noun", "/ˈlætɪtjuːd/", "", "",
  "拉丁语 latitudo（宽度）← latus（宽的）；与 lateral 所本的 latus（侧边）"
  "以及 referre 那支的 latus（被带走的）不同源",
  "the distance of a place north or south of the equator, or freedom to act",
  "地球仪上一圈圈平行的横线，越往上越短，指头按住哪一圈就报得出数",
  "纬度/自由度/回旋余地",
  "The city lies at forty degrees latitude.|Teachers have some latitude in this.",
  "how broad a band you stand in – 你落在哪一条横带上，那条带子有多宽",
  "纬度：南北方向上量出来的那个数|自由度：可动的范围也这样论宽窄|回旋余地：办事时留给你的那点宽松")

w("linguistic", "adjective", "/lɪŋˈɡwɪstɪk/", "", "",
  "法语 linguistique ← 拉丁语 lingua（舌头，引申为所说的话）；库中 language 同出这一支",
  "relating to language or to the study of language",
  "两个人各说各的一套，中间那个把每个音都记下来，对着看哪一处对得上",
  "语言的/语言学的",
  "She has great linguistic ability.|The book covers linguistic change over time.",
  "having to do with the tongue and what it says – 与舌头和它说出的话有关",
  "语言的：与说的话本身有关|语言学的：把话当作对象来研究的那门学问")

# ================= C 档 =================

w("investment", "noun", "/ɪnˈvestmənt/", "", "",
  "英语 invest 加 -ment 构成；invest ← 拉丁语 investire（给…穿上衣服）："
  "in-（进）+ vestire（穿衣）← vestis（衣服），后转指把钱披到生意上",
  "money put into something in the hope of earning more, or effort put in",
  "他把攒下的钱换成一叠纸凭证锁进抽屉，指望几年后那叠纸值得更多",
  "投资/投入/投资额",
  "They made a large investment in solar power.|Learning a language needs real investment.",
  "money laid onto a business as a garment – 把钱像衣服一样披到生意身上",
  "投资：为求回报而投出去的那笔钱|投入：时间与精力也这样投出去|投资额：投出去的那个数目本身")

w("inward", "adjective / adverb", "/ˈɪnwəd/", "", "",
  "古英语 inneweard（朝里的）← inne（在内）+ -weard（朝向）← 原始日耳曼语",
  "turned or moving towards the inside, or existing in the mind",
  "门被推着朝屋子那一边转开，人跟着走进去；心里那点想法也是朝那个方向的",
  "向内的/内心的",
  "The door swings inward when you push.|He kept his inward doubts to himself.",
  "facing towards the inside – 面朝里头的那一边",
  "向内的：方向上冲着里面，与朝外相对|内心的：不露在外，只在心里那一层",
  "",
  "inward + n —— 向内的…，作定语说方向或心里那一层|turn inward —— 转向内里，指人变得内省或不再对外|inward investment —— 外来投资流入本国，经济报道里的固定说法")

w("judgement", "noun", "/ˈdʒʌdʒmənt/", "jus",
  "judge（jus 法、准 → judex 宣法的人）+ -ment（名词）→ 依那把准比过之后落下的那句话",
  "古法语 jugement ← jugier（审断）← 拉丁语 judicare ← judex（法官）"
  "← jus（属格 juris：法、权利）",
  "the ability to make good decisions, or a decision made by a court",
  "两边都说完了，他停了几秒，把手里的纸一合，说出那句定下来的话",
  "判断力/判决/看法",
  "She showed good judgement under pressure.|The court delivered its judgement today.",
  "the call made after weighing against the standard – 拿那把准比过之后落下的那句话",
  "判断力：看得准、决断得好的那份本事|判决：法院正式落下的那一句|看法：个人比过之后得出的那个结论")

w("landlord", "noun", "/ˈlændlɔːd/", "", "",
  "中古英语 landlord，由 land（古英语 land 地）与 lord（古英语 hlaford 家主）复合",
  "a person or company that owns a house or land and lets others use it for rent",
  "每月头几天他来敲一次门，收走一个信封，水管坏了也得等他点头才修",
  "房东/地主",
  "Our landlord raised the rent again.|The landlord owns twelve flats here.",
  "the one who holds the ground others live on – 别人住着的这块地归他手里",
  "房东：把房子租给人住、收租的那个人|地主：把田地租给人种的那种，多说旧时")

w("last", "adjective / verb / adverb", "/lɑːst/", "", "",
  "「最后的」出自古英语 latost（最迟的），是 læt（迟）的最高级；「持续」出自古英语 "
  "læstan（跟得住、支撑住）← 原始日耳曼语 *laistijan",
  "coming after all the others, most recent, or to go on for a length of time",
  "他冲过终点线时后面已经没人了；那罐漆刷完三面墙还剩小半罐",
  "最后的/上一个的/持续",
  "He was the last one to leave.|The meeting lasted three hours.",
  "nothing comes after it, and it keeps going – 后面再没有别的了，而且还撑得下去",
  "最后的：排在末位，后面没有了|上一个的：时间上刚过去的那一个，如上周|持续：另一支来源，撑住一段时间不断",
  "",
  "at last —— 终于，等了很久之后才发生|last but not least —— 最后但同样重要，列举收尾时用|the last person to do sth —— 最不可能做某事的人，反说|last for + 时段 —— 持续多久，说时间长度")

w("lately", "adverb", "/ˈleɪtli/", "", "",
  "英语 late 加 -ly 构成；late ← 古英语 læt（迟的）← 原始日耳曼语 *lataz（松懈、迟缓）",
  "in the period of time just before now",
  "这几个礼拜他老是熬到半夜才睡，白天说话都比从前慢半拍",
  "最近/近来",
  "I have not seen him lately.|She has been working late lately.",
  "in the stretch just gone by – 刚过去的那一段里",
  "最近：离现在不远的那一段时间里|近来：同一个意思，语气偏书面",
  "",
  "have/has + 过去分词 + lately —— 与完成时连用，说刚过去这段里的事|not ... lately —— 近来没有，最常见的否定型式|lately + 现在完成进行 —— 强调这段时间一直如此")

w("lateral", "adjective", "/ˈlætərəl/", "", "",
  "拉丁语 lateralis（侧边的）← latus（属格 lateris：身侧、旁边）；与 latitude 所本的 "
  "latus（宽的）不同源",
  "relating to the side, or moving sideways rather than forwards",
  "他不往前走，脚一横朝旁边挪了两步，正好躲开对面伸来的手",
  "侧面的/横向的",
  "The plant has lateral roots near the surface.|He made a lateral move to another team.",
  "on or towards the flank – 在身侧那一边，或朝那一边去",
  "侧面的：位置在旁边，不在正前正后|横向的：动作与调动都往旁边走，如平级调动")

w("latter", "adjective", "/ˈlætə/", "", "",
  "古英语 lætra（更迟的），是 læt（迟的）的比较级 ← 原始日耳曼语 *lataz",
  "the second of two people or things just mentioned, or nearer the end",
  "两样东西摆在桌上说了一遍，他手一指后头提到的那一样",
  "后者的/后一半的",
  "Of tea and coffee, I prefer the latter.|Prices rose in the latter half of the year.",
  "the one that came later of the two – 两个里头后说到的那一个",
  "后者的：两者对举时指后提到的那个|后一半的：一段时间的靠后那一截，如下半年",
  "",
  "the former ... the latter —— 前者…后者…，成对出现，指代刚提的两样|the latter half of sth —— 某段时间的后一半|the latter part of sth —— 某事的后段，多说时期或过程")

w("layman", "noun", "/ˈleɪmən/", "", "",
  "中古英语 layman，由 lay（非教职的、属俗众的）与 man 复合；lay ← 古法语 lai "
  "← 晚期拉丁语 laicus ← 希腊语 laikos（属民众的）",
  "a person without special training or knowledge in a particular subject",
  "满桌子人讲的全是行话，只有他一个听得皱眉，问的问题旁人都笑",
  "外行/非专业人士",
  "Explain it in terms a layman can grasp.|To a layman the two look identical.",
  "one of the ordinary crowd, not of the trained few – 是众人里的一个，不在那批受过训的人之列",
  "外行：这门里没受过训、不懂门道的人|非专业人士：说法正式些，与专家相对")

w("librarian", "noun", "/laɪˈbreəriən/", "", "",
  "英语 library 加 -an（做这份差事的人）构成；library ← 拉丁语 librarium（放书的箱柜）"
  "← liber（书，本义树的内皮），与「自由」那支的 liber 同形不同源",
  "a person who works in a library and looks after the books",
  "柜台后头那个人把还回来的书按编号一本本插回架上，顺手在卡片上画一道",
  "图书馆员/管理员",
  "The librarian helped me find the map.|She trained as a librarian after college.",
  "the one who keeps the books in order – 把那一架子书管得有条理的人",
  "图书馆员：在那个地方上班、管书的人|管理员：泛指管着这一摊事的人，语气随意些")

w("linger", "verb", "/ˈlɪŋɡə/", "", "",
  "中古英语 lengeren，是古英语 lengan（拖长、延缓）的反复形 ← 原始日耳曼语 *langjan（使变长）",
  "to stay somewhere longer than expected, or to fade away slowly",
  "客人都走了，他还站在门口摸着帽檐说话，一句接一句不肯下台阶",
  "逗留/徘徊/久留不去",
  "A few guests lingered after midnight.|The smell of smoke lingered for days.",
  "stretching out the staying – 把待着这件事拖长",
  "逗留：该走了还不走，多待一阵|徘徊：在一处来回走动不离开|久留不去：气味、疑虑这样迟迟不散")

w("little", "adjective / adverb", "/ˈlɪtl/", "", "",
  "古英语 lȳtel（小的、少的）← 原始日耳曼语 *lūtilaz",
  "small in size, or not much of something",
  "一颗豆子大的东西搁在掌心几乎看不出，杯底那点水晃一晃就没了",
  "小的/少的/几乎没有",
  "She lives in a little house by the river.|There is little hope of a change.",
  "not much of it, and not much to it – 分量少，个头也小",
  "小的：个头不大，说东西也说人|少的：不可数的东西分量不多|几乎没有：不加冠词时偏否定，等于说不够",
  "",
  "a little + 不可数 —— 有一点，肯定意味，说还有一些|little + 不可数 —— 几乎没有，否定意味，与 a little 相反|little by little —— 一点一点地，说渐变过程|a little + adj —— 稍微，程度上轻轻一点")

w("lock", "noun / verb", "/lɒk/", "", "",
  "古英语 loc（门闩、闭合处）← 原始日耳曼语 *lukaz；与拉丁语 locus（地点）无关",
  "a device for fastening something shut with a key, or to fasten it that way",
  "钥匙转半圈，里头几片铁舌一齐弹进槽里，门再推也不动了",
  "锁/锁上/闸室",
  "He turned the key in the lock.|Remember to lock the back door.",
  "the bolt that drops into place – 落进槽里、卡住不放的那根舌头",
  "锁：装在门上、要钥匙才开的那个件|锁上：作动词，把它转到卡住的位置|闸室：运河上两道闸门围起的一段，同样是关起来")

w("locker", "noun", "/ˈlɒkə/", "", "",
  "英语 lock（锁）加 -er（存放处）构成；lock ← 古英语 loc（门闩）← 原始日耳曼语 *lukaz",
  "a small cupboard with a lock, used for keeping personal things in a public place",
  "更衣室墙上一排窄铁柜，各挂一把小锁，运动服和鞋都塞在自己那一格里",
  "寄物柜/储物柜",
  "He left his bag in the locker.|Each student gets a locker key.",
  "a small box you can lock – 能上锁的那一小格柜子",
  "寄物柜：车站商场里临时存东西的那种|储物柜：学校健身房里长期归你用的那一格")

# ---------------- 落盘前自检 ----------------
CJK = re.compile(r"[一-鿿]")
errs = []
roots = json.loads((ROOT / "data" / "roots.json").read_text(encoding="utf-8"))["roots"]
rids = {x["id"] for x in roots}
libwords = {x["word"] for x in
            json.loads((ROOT / "data" / "words.json").read_text(encoding="utf-8"))["words"]}
new_rids = {x[1] for x in R}
all_rids = rids | new_rids

src = (ROOT / "drafts" / "g_chunk109.txt").read_text(encoding="utf-8")
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
