#!/usr/bin/env python3
"""Generate batch52: 反查第三批 30 词，全部补进已建模词根，不新建根。

  stru（垒起）        obstruct / obstruction / infrastructure
  elektron（琥珀）    electron / electronic
  tribuere（分给）    tribute / contribution
  hostis（门外来人）  hospital / hospitality   —— hospes 待客那一支
  consuetudo（惯常）  costume / accustomed
  praeesse（在前）    represent / representative
  tempus（时间/分寸） temperature             —— temperare 调和那一支
  stringere（拉紧）   restraint
  cadere（落下）      accident / accidental    —— 非 identus，见下
  vid（看）           evident                  —— 非 identus，见下
  ordinare（排序）    extraordinary
  punktum（刺点）     punctual / disappoint
  gen（生）           generalize / generator
  sequ（跟随）        persecute / prosecute
  classis（等级）     classmate / classroom
  sumere（取）        assumption / consumption
  solvere（解开）     resolute / resolution
  referre（带回）     relative / relativity
  habitare（居住）    habitat
  modus（分寸尺度）   modern / modernization

【两处纠偏：反查把它们报在 identus 名下，但词源不对】
  accident / accidental ← ad＋cadere（落到…上），与 incident 同族，归 cadere
  evident               ← ex＋videre（看出来），归 vid
  identus 是 idem（同一个）→ identity/identical/identify 那一支，
  这三词只因拼写含 ident 才被命中，与「同一」无关。

【本批剔除的候选，勿再捡回】
  litter / glitter  ← 第五十一批已剔：litiere ← lectus（床）／古诺斯 glitra
  string            ← 第五十批已剔：原始日耳曼语 *strangiz
  standpoint        ← 英语自造复合词，非 punktum 的拉丁派生
  heroin            ← 19 世纪拜耳药名，德语造词，非 hērōs 的词族成员
  plateau           ← 法语 plat（平）一支，归 planus 更妥，不归 platea
  nuclear           ← nucleus（果核），与 clarus（明亮）无关，纯拼写巧合
  exhibition        ← habere 的 -hibit 支（已有 exhibit/inhibit/prohibit），
                      不归 habitare（居住）；本批不收，留待 habere 专批
  according to      ← 多词短语，不能作 word id
  coordinates       ← 复数形，词元是已入库的 coordinate

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch52.json"


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

# ================= stru（垒起）=================
words += [
    W("obstruct", "stru", "verb", "/əbˈstrʌkt/",
      "ob-（挡在前）+ struct（垒）→ 在通路上垒起东西 → 堵住",
      "拉丁语 obstruere（堵塞），来自 ob（对面、挡）＋struere（堆叠）",
      "to block a path or prevent something from happening",
      "piling something up across the way so nothing gets through – 在通路上垒起一堆，谁也过不去",
      "巷口垒起半人高的砖，车马到此只能折返",
      ["阻塞", "阻碍"],
      ["A fallen tree obstructed the road.", "He was charged with obstructing justice."],
      ["block", "hinder"], ["clear", "assist"],
      ["obstruction", "construct"],
      ["阻塞/阻碍：在通路上垒起东西、使过不去"],
      "ob-（挡在前）+ struct（垒）→ 在路上垒起一堆"),
    W("obstruction", "stru", "noun", "/əbˈstrʌkʃn/",
      "obstruct（垒起挡路）+ -ion → 挡路这件事，或挡路的那个东西",
      "拉丁语 obstructio，来自 obstruere ← ob＋struere",
      "something that blocks a way; the act of blocking",
      "the pile that stands across the way, and the placing of it – 横在路上的那一堆，及垒它这件事",
      "清障车开来，把横在道中的那一堆一点点搬开",
      ["障碍物", "阻碍", "妨碍"],
      ["Remove any obstruction from the pipe.", "He was fined for obstruction."],
      ["barrier", "obstacle"], ["clear"],
      ["obstruct", "construct"],
      ["障碍物：横在路上的那一堆", "阻碍/妨碍：垒起它、使人过不去这件事"],
      "obstruct（垒起挡路）+ -ion → 挡路之物与其事"),
    W("infrastructure", "stru", "noun", "/ˈɪnfrəstrʌktʃə(r)/",
      "infra-（在下）+ structure（垒起之物）→ 垒在底下托住上面的那一套",
      "英语 infrastructure，由拉丁 infra（在下）＋structura（构造）← struere 合成",
      "the basic systems such as roads and power that a country needs",
      "what is built underneath to hold everything else up – 垒在底下、托住上面全部的那一层",
      "路面之下埋着管线与地基，上面的楼才立得住",
      ["基础设施", "基础架构"],
      ["The country invested in infrastructure.", "Cloud infrastructure supports the service."],
      ["framework", "foundation"], [],
      ["structure", "obstruct"],
      ["基础设施/基础架构：垒在底下托住上层全部的那一套"],
      "infra-（在下）+ structure（垒起之物）→ 垒在底下托住上面"),
]

# ================= elektron（琥珀）=================
words += [
    W("electron", "elektron", "noun", "/ɪˈlektrɒn/",
      "elektr（琥珀）+ -on（粒）→ 带那种「琥珀之力」的最小粒",
      "英语 electron，1891 年由 electric＋-on 造出；electric ← 希腊语 elektron（琥珀），"
      "琥珀摩擦后能吸引轻物，电现象由此得名",
      "a very small particle carrying a negative charge",
      "the smallest bearer of the force amber showed when rubbed – 琥珀摩擦所显那股力的最小承载者",
      "琥珀在布上擦几下，碎纸屑就往它上头扑",
      ["电子"],
      ["Electrons orbit the nucleus.", "The beam is a stream of electrons."],
      ["particle", "electric"], [],
      ["electronic", "electric"],
      ["电子：带负电、体积极小的那种粒子"],
      "elektr（琥珀）+ -on（粒）→ 带琥珀之力的最小粒"),
    W("electronic", "elektron", "adjective", "/ˌelɪkˈtrɒnɪk/",
      "electron（电子）+ -ic（…的）→ 靠电子工作的",
      "英语 electronic，来自 electron ← 希腊语 elektron（琥珀）",
      "using or relating to devices that work by controlling electrons",
      "working by steering those smallest bearers of charge – 靠驾驭那些最小带电粒来运作",
      "板子上细如发丝的线路一通，屏就亮了",
      ["电子的", "电子化的"],
      ["She reads electronic books.", "All records are now electronic."],
      ["digital", "electric"], ["manual"],
      ["electron", "electric"],
      ["电子的/电子化的：靠驾驭电子来运作的"],
      "electron（电子）+ -ic → 靠电子工作的"),
]

# ================= tribuere（分给）=================
words += [
    W("tribute", "tribuere", "noun", "/ˈtrɪbjuːt/",
      "tribuere（分给、缴纳）→ 按份缴上去的那笔 → 贡赋；引申为致敬之礼",
      "拉丁语 tributum（贡赋），来自 tribuere（分配、缴纳）",
      "something said or given to show respect; a payment made by one state to another",
      "the share handed up in acknowledgement – 按份呈上去、表示认这份情的东西",
      "各家按份把谷物送到城门，一车车登记入册",
      ["贡品", "致敬", "颂词"],
      ["The concert was a tribute to her teacher.", "The city paid tribute to the empire."],
      ["respect", "praise"], ["insult"],
      ["contribution", "distribute"],
      ["贡品：按份呈上去的那笔", "致敬/颂词：把心意按份呈上，同一个「奉上」动作"],
      "tribuere（分给、缴纳）→ 按份呈上去的东西"),
    W("contribution", "tribuere", "noun", "/ˌkɒntrɪˈbjuːʃn/",
      "con-（一同）+ tribut（分给）+ -ion → 各人拿出自己那份凑到一处",
      "拉丁语 contributio，来自 contribuere（共同出资）← con＋tribuere",
      "something given to help achieve something; a payment to a common fund",
      "each hand putting its share into the same pile – 各人把自己那份放进同一堆里",
      "桌上那只匣子，来的人各投一份进去",
      ["贡献", "捐款", "投稿"],
      ["Her contribution was decisive.", "He made a small contribution to the fund."],
      ["gift", "input"], [],
      ["tribute", "distribute"],
      ["贡献：拿出自己那份凑到共同一处", "捐款/投稿：同一动作用在钱或文稿上"],
      "con-（一同）+ tribut（分给）→ 各出一份凑到一处"),
]

# ================= hostis（门外来人：hospes 待客那一支）=================
words += [
    W("hospital", "hostis", "noun", "/ˈhɒspɪtl/",
      "hospit（待客）+ -al → 本指收留旅人之所，后专指收治病人的地方",
      "中世纪拉丁语 hospitale（客舍、济贫院），来自 hospes（主/客）；"
      "hospes 与 hostis 同出原始印欧语 *ghos-ti-，本族收待客那一支",
      "a place where sick or injured people are treated",
      "the house that takes in whoever arrives needing care – 接纳前来求治者的那处屋舍",
      "门开着，抬进来的人一个个被接下、安置到床位上",
      ["医院"],
      ["She was taken to hospital by ambulance.", "He works at the city hospital."],
      ["clinic", "ward"], [],
      ["hospitality", "host"],
      ["医院：本为收留旅人之所，后专指收治病人的地方"],
      "hospit（待客）+ -al → 接纳来者的那处屋舍"),
    W("hospitality", "hostis", "noun", "/ˌhɒspɪˈtæləti/",
      "hospit（待客）+ -ality → 待客这件事、那份周到",
      "拉丁语 hospitalitas（好客），来自 hospes（主/客）← *ghos-ti-",
      "friendly and generous treatment of guests",
      "the care put into receiving whoever comes – 接待来者时使出的那份周到",
      "客人一进门，茶水与坐处都已备下",
      ["好客", "招待", "款待"],
      ["Thank you for your hospitality.", "The hotel is known for its hospitality."],
      ["welcome", "warmth"], ["coldness"],
      ["hospital", "host"],
      ["好客/招待/款待：接待来者时使出的那份周到"],
      "hospit（待客）+ -ality → 待客那份周到"),
]

# ================= consuetudo（惯常）=================
words += [
    W("costume", "consuetudo", "noun", "/ˈkɒstjuːm/",
      "consuetudo（成例、惯常）→ 一地惯常的穿戴 → 服装、戏装",
      "法语 costume，来自意大利语 costume（习俗、装束）← 拉丁语 consuetudo（惯常）；"
      "与 custom 同源，一支走「习俗」义，一支走「装束」义",
      "clothes worn to look like someone else, or typical of a place or period",
      "what a place has long been in the habit of wearing – 一地长年惯常穿戴的那一套",
      "戏班箱子里那几套按老样式裁的衣裳，年年照旧",
      ["服装", "戏装", "民族服装"],
      ["She wore a bear costume.", "The dancers appeared in traditional costume."],
      ["outfit", "dress"], [],
      ["custom", "customary"],
      ["服装/民族服装：一地惯常穿戴的那一套", "戏装：照旧样式备下、供扮演穿的那身"],
      "consuetudo（成例）→ 惯常的穿戴 → 服装"),
    W("accustomed", "consuetudo", "adjective", "/əˈkʌstəmd/",
      "ac-（ad- 朝）+ custom（成例）+ -ed → 已入成例的 → 习惯了的",
      "英语 accustomed，来自 accustom ← 古法语 acostumer ← 拉丁语 consuetudo",
      "familiar with something through long experience; usual",
      "worn into the groove until it feels ordinary – 走顺了那道沟，做起来不觉费力",
      "同一条路走了几十年，脚自己知道往哪拐",
      ["习惯的", "惯常的"],
      ["She is accustomed to early starts.", "He took his accustomed seat."],
      ["usual", "habit"], ["strange"],
      ["custom", "customary"],
      ["习惯的/惯常的：已走顺那道沟、做来不觉费力"],
      "ac-（朝）+ custom（成例）+ -ed → 已入成例的"),
]

# ================= praeesse（在前主事）=================
words += [
    W("represent", "praeesse", "verb", "/ˌreprɪˈzent/",
      "re-（再）+ present（放到眼前）→ 再把它摆到眼前 → 代表、表现",
      "拉丁语 repraesentare（再现、呈现），来自 re＋praesentare ← praesens ← praeesse",
      "to act on behalf of someone; to stand for or depict something",
      "putting a thing before the eyes again in another's stead – 替某方再把它摆到眼前",
      "他替全村上台开口，村里人虽不在场，话却在场",
      ["代表", "表现", "象征"],
      ["She represents her country abroad.", "This graph represents last year's sales."],
      ["show", "depict"], [],
      ["representative", "present"],
      ["代表：替某方把其意再摆到眼前", "表现/象征：把事物再呈到眼前来指代它"],
      "re-（再）+ present（放到眼前）→ 替人再摆到眼前"),
    W("representative", "praeesse", "noun", "/ˌreprɪˈzentətɪv/",
      "represent（代表）+ -ative → 受托来代表的那个人或物",
      "英语 representative，来自 represent ← 拉丁语 repraesentare ← praeesse",
      "a person chosen to act or speak for others; typical of a group",
      "the one sent to stand before others in their stead – 被派去替众人站到台前的那个",
      "各车间推一个人出来，那人往台前一站，说的是全班的意思",
      ["代表", "代理人", "有代表性的"],
      ["Each class elects a representative.", "This sample is representative of the whole."],
      ["agent", "deputy"], [],
      ["represent", "present"],
      ["代表/代理人：受托替众人站到台前的那个", "有代表性的：拿它就能指代整体的"],
      "represent（代表）+ -ative → 受托代表的那个"),
]

# ================= tempus（时间/分寸：temperare 调和那一支）=================
words += [
    W("temperature", "tempus", "noun", "/ˈtemprətʃə(r)/",
      "temper（调和、按分寸）+ -ature → 冷热调到什么分寸 → 温度",
      "拉丁语 temperatura（调和之度），来自 temperare（调和、节制）← tempus；"
      "本族已收 temper/temporary/contemporary，此词走「调和分寸」那一支",
      "how hot or cold something is, measured on a scale",
      "where the hot and cold have been brought into balance – 冷与热调停到的那个位置",
      "壶里兑进一瓢凉水，手伸进去正好不烫",
      ["温度", "气温", "体温"],
      ["The temperature dropped overnight.", "His temperature is back to normal."],
      ["heat", "warmth"], [],
      ["temper", "temporary"],
      ["温度/气温：冷热调停到的那个位置", "体温：人身上那个位置的读数"],
      "temper（调和分寸）+ -ature → 冷热调到的那个度"),
]

# ================= stringere（拉紧）=================
words += [
    W("restraint", "stringere", "noun", "/rɪˈstreɪnt/",
      "re-（往回）+ strain（拉紧）+ -t → 往回收紧这件事 → 克制、约束",
      "古法语 restrainte，来自 restringere（拉回束紧）← re＋stringere（拉紧）",
      "control over one's own behaviour; a limit placed on someone",
      "the cord pulled back to check what was about to move – 往回一拽、把正要动的收住那股力",
      "话到嘴边被自己拽回去，脸上一点没露",
      ["克制", "约束", "限制措施"],
      ["He showed great restraint.", "New restraints were placed on spending."],
      ["control", "curb"], ["luxury"],
      ["restrict", "strict"],
      ["克制：把自己往回拽住那份力", "约束/限制措施：外加的那道收紧"],
      "re-（往回）+ strain（拉紧）→ 往回收住那股力"),
]

# ================= cadere（落下）—— 反查报在 identus 名下，实为此族 =================
words += [
    W("accident", "cadere", "noun", "/ˈæksɪdənt/",
      "ac-（ad- 落到…上）+ cid（落下）+ -ent → 落到人头上的那一桩 → 意外",
      "拉丁语 accidens（偶然发生的），来自 accidere（落到、发生）← ad＋cadere（落下）；"
      "与 incident 同族。拼写含 ident 只是巧合，与 idem（同一个）无关",
      "an unexpected event that causes damage or injury",
      "the thing that came down on one without being asked – 没招呼一声就落到人头上的那一桩",
      "拐角处一声闷响，两辆车谁也没料到会撞上",
      ["事故", "意外", "偶然"],
      ["He was hurt in a car accident.", "They met by accident at the station."],
      ["mishap", "chance"], ["purpose"],
      ["accidental", "incident"],
      ["事故/意外：没打招呼就落到头上的那一桩", "偶然：并非安排、恰好落下的"],
      "ac-（落到上）+ cid（落下）→ 落到人头上的那一桩"),
    W("accidental", "cadere", "adjective", "/ˌæksɪˈdentl/",
      "accident（落下之事）+ -al（…的）→ 属于偶然落下的 → 无意的",
      "英语 accidental，来自 accident ← accidere ← ad＋cadere",
      "happening by chance and not on purpose",
      "of the kind that just came down, not aimed – 属于恰好落下、并非瞄准的那种",
      "手一滑那杯子就掉了，谁也不是有意的",
      ["偶然的", "意外的", "无意的"],
      ["It was an accidental discovery.", "The damage was purely accidental."],
      ["chance", "accidental"], ["deliberate", "planned"],
      ["accident", "incident"],
      ["偶然的/意外的：恰好落下、并非瞄准的", "无意的：落下时本无此心"],
      "accident（落下之事）+ -al → 属于恰好落下的"),
]

# ================= vid（看）—— 反查报在 identus 名下，实为此族 =================
words += [
    W("evident", "vid", "adjective", "/ˈevɪdənt/",
      "e-（ex- 出来）+ vid（看）+ -ent → 明摆在外看得见的 → 显然",
      "拉丁语 evidens（明显的），来自 e＋videre（看）；"
      "拼写含 ident 只是巧合，与 idem（同一个）无关",
      "clear to see or understand; obvious",
      "standing out where the eye cannot miss it – 摆在外头，眼睛想漏也漏不掉",
      "地上那道湿痕一直连到门口，谁进过屋一看便知",
      ["明显的", "显然的"],
      ["It was evident that she was tired.", "His skill is evident in every line."],
      ["obvious", "apparent"], ["obscure", "hidden"],
      ["invisible", "envisage"],
      ["明显的/显然的：明摆在外、眼睛漏不掉的"],
      "e-（出来）+ vid（看）→ 明摆在外看得见的"),
]

# ================= ordinare（排序）=================
words += [
    W("extraordinary", "ordinare", "adjective", "/ɪkˈstrɔːdnri/",
      "extra-（出乎…之外）+ ordinary（常序）→ 跳出常序之外的 → 非凡",
      "拉丁语 extraordinarius（不合常规的），来自 extra ordinem（在常序之外）← ordo",
      "very unusual or remarkable; beyond what is ordinary",
      "the one that falls outside the row everything else stands in – 从众物所立那一列里跳出去的",
      "一排都齐着，只有那一个高出一头，站在队形之外",
      ["非凡的", "特别的", "异常的"],
      ["She has extraordinary talent.", "They took extraordinary measures."],
      ["remarkable", "exceptional"], ["ordinary", "commonplace"],
      ["ordinary", "coordinate"],
      ["非凡的/特别的：跳出常序、不在那一列里", "异常的：同样偏离常规那一档"],
      "extra-（之外）+ ordinary（常序）→ 跳出常序之外"),
]

# ================= punktum（刺点）=================
words += [
    W("punctual", "punktum", "adjective", "/ˈpʌŋktʃuəl/",
      "punct（刺出的点）+ -ual → 正落在那个点上的 → 准时",
      "中世纪拉丁语 punctualis（准于一点的），来自 punctum（刺出的点）",
      "arriving or happening at exactly the right time",
      "landing exactly on the marked spot, not beside it – 正落在标出的那一点上，不偏旁边",
      "针尖落下正压在刻度那一道上，分毫不差",
      ["准时的", "守时的"],
      ["He is always punctual for class.", "Punctual delivery is guaranteed."],
      ["prompt", "timely"], ["late", "slow"],
      ["point", "appoint"],
      ["准时的/守时的：正落在标定那一点上、不偏不错"],
      "punct（刺点）+ -ual → 正落在那一点上"),
    W("disappoint", "punktum", "verb", "/ˌdɪsəˈpɔɪnt/",
      "dis-（取消）+ appoint（点定）→ 把点定好的那件事撤掉 → 使失望",
      "古法语 desapointier（免职、取消约定），由 des-＋apointier ← punctum（点）",
      "to make someone sad by failing to do what they hoped",
      "undoing what had been pinned to a point, leaving it empty – 把钉在那点上的事撤掉，那儿就空了",
      "约好的那一格被划掉，人白等了一下午",
      ["使失望", "使扫兴"],
      ["The result disappointed his parents.", "I hate to disappoint you."],
      ["fail", "dishearten"], ["satisfy", "delight"],
      ["appoint", "point"],
      ["使失望/使扫兴：把点定好的事撤掉，留下空处"],
      "dis-（取消）+ appoint（点定）→ 把定好的撤掉"),
]

# ================= gen（生）=================
words += [
    W("generalize", "gen", "verb", "/ˈdʒenrəlaɪz/",
      "gener（族类）+ -al + -ize → 由个别推到整族 → 概括、一概而论",
      "英语 generalize，来自 general ← 拉丁语 generalis（属于全族的）← genus（族类）",
      "to draw a broad conclusion from particular cases",
      "taking what one case showed and laying it over the whole kin – 把一例所见铺到整族头上",
      "看了三只都是白的，便说这一族都白",
      ["概括", "归纳", "一概而论"],
      ["Do not generalize from one example.", "She generalized the findings."],
      ["conclude", "infer"], ["specify"],
      ["generator", "general"],
      ["概括/归纳：由个别推及整族", "一概而论：铺得过头、不分个别的那种推法"],
      "gener（族类）+ -ize → 由个别推到整族"),
    W("generator", "gen", "noun", "/ˈdʒenəreɪtə(r)/",
      "gener（生出）+ -ator（施为者）→ 使某物生出来的那件机器",
      "拉丁语 generator（生育者、产生者），来自 generare（生出）← genus",
      "a machine that produces electricity or other output",
      "the thing that brings a supply into being – 使某样东西源源生出来的那件器械",
      "机器一响，原本没有的电就源源出来了",
      ["发电机", "发生器"],
      ["The hospital has a backup generator.", "This tool is a code generator."],
      ["engine", "machine"], [],
      ["generalize", "generate"],
      ["发电机/发生器：使某物源源生出来的那件器械"],
      "gener（生出）+ -ator → 使之生出的那件机器"),
]

# ================= sequ（跟随）=================
words += [
    W("prosecute", "sequ", "verb", "/ˈprɒsɪkjuːt/",
      "pro-（往前）+ secut（跟随）→ 一路追到底 → 起诉、依法追究",
      "拉丁语 prosecutus，prosequi（追随到底）的过去分词 ← pro＋sequi（跟随）",
      "to bring a legal case against someone in court",
      "following a matter all the way through to its end – 咬住一桩事一路跟到底",
      "案卷一层层往上递，一路跟到判下来为止",
      ["起诉", "检举", "彻底进行"],
      ["The state decided to prosecute.", "They prosecuted the case for two years."],
      ["accuse", "pursue"], ["defend"],
      ["persecute", "sequence"],
      ["起诉/检举：依法咬住一桩事追到底", "彻底进行：同一个「跟到底」用在做事上"],
      "pro-（往前）+ secut（跟随）→ 一路追到底"),
    W("persecute", "sequ", "verb", "/ˈpɜːsɪkjuːt/",
      "per-（一路、不断）+ secut（跟随）→ 不断追着为难 → 迫害",
      "拉丁语 persecutus，persequi（追逼）的过去分词 ← per＋sequi（跟随）",
      "to treat someone cruelly over time, especially for their beliefs",
      "keeping after a person without ever letting up – 一路追着不放、不给对方喘息",
      "那家人搬到哪儿，后头的人就跟到哪儿，一年没断过",
      ["迫害", "折磨"],
      ["They were persecuted for their faith.", "He felt persecuted by the press."],
      ["oppress", "trouble"], ["protect"],
      ["prosecute", "sequence"],
      ["迫害/折磨：一路追着不放、不给喘息"],
      "per-（不断）+ secut（跟随）→ 追着不放"),
]

# ================= classis（等级）=================
words += [
    W("classmate", "classis", "noun", "/ˈklɑːsmeɪt/",
      "class（同一等第）+ mate（伙伴）→ 被编在同一班的伙伴",
      "英语复合词 class＋mate；class ← 拉丁语 classis（等第、编组）",
      "a person in the same class at school",
      "one sorted into the same bracket as oneself – 与自己被编进同一格的那个人",
      "点名册上两个名字挨着，从开学起就坐一排",
      ["同班同学"],
      ["She met her old classmate downtown.", "My classmates helped me revise."],
      ["peer", "friend"], [],
      ["classroom", "class"],
      ["同班同学：与自己被编进同一格的人"],
      "class（同一等第）+ mate（伙伴）→ 同格的伙伴"),
    W("classroom", "classis", "noun", "/ˈklɑːsruːm/",
      "class（编组）+ room（屋）→ 一编人一起上课的那间屋",
      "英语复合词 class＋room；class ← 拉丁语 classis（等第、编组）",
      "a room in a school where lessons are taught",
      "the room a whole bracket of learners sits in – 同编的一群人共坐的那间屋",
      "推门进去，桌椅一排排冲着黑板",
      ["教室"],
      ["The classroom holds thirty desks.", "She stayed in the classroom after school."],
      ["school", "hall"], [],
      ["classmate", "class"],
      ["教室：同编一群人一起上课的那间屋"],
      "class（编组）+ room（屋）→ 同编者共坐的屋"),
]

# ================= sumere（取）=================
words += [
    W("assumption", "sumere", "noun", "/əˈsʌmpʃn/",
      "as-（ad- 朝）+ sumpt（取）+ -ion → 先取来当真的那一条 → 假定",
      "拉丁语 assumptio（取用、采纳），来自 assumere（取来）← ad＋sumere（取）",
      "something believed true without proof; the act of taking on",
      "the piece one picks up and treats as given before checking – 未及核就先拿来当真的那一条",
      "他没查底册，先拿一条当真，往下全按这条推",
      ["假定", "假设", "承担"],
      ["That assumption proved wrong.", "His assumption of office was swift."],
      ["premise", "guess"], ["proof"],
      ["consumption", "assume"],
      ["假定/假设：未核就先取来当真的那一条", "承担：把职责取到自己身上"],
      "as-（朝）+ sumpt（取）→ 先取来当真的那条"),
    W("consumption", "sumere", "noun", "/kənˈsʌmpʃn/",
      "con-（尽）+ sumpt（取用）+ -ion → 取用到尽 → 消耗、消费",
      "拉丁语 consumptio（耗尽），来自 consumere（用尽）← con＋sumere（取）",
      "the using up of resources; the amount used",
      "taking from the store until it is spent – 一直从堆里取，取到见底",
      "油表的针一路往左掉，箱里那些一趟就见了底",
      ["消耗", "消费", "食用"],
      ["Fuel consumption has risen.", "Limit your sugar consumption."],
      ["use", "expenditure"], ["production"],
      ["assumption", "consume"],
      ["消耗/消费：取用到尽的那个量与过程", "食用：同一个「取入」用在饮食上"],
      "con-（尽）+ sumpt（取用）→ 取用到见底"),
]

# ================= solvere（解开）=================
words += [
    W("resolution", "solvere", "noun", "/ˌrezəˈluːʃn/",
      "re-（彻底）+ solut（解开）+ -ion → 把缠住的彻底解开 → 决心、解决、决议",
      "拉丁语 resolutio（解开、分解），来自 resolvere（解开）← re＋solvere",
      "a firm decision; the solving of a problem; a formal vote of a body",
      "the knot worked loose so the line runs free again – 缠住的那个结被解开，绳又顺了",
      "缠了半天的那个结终于松开，线一抽就顺了",
      ["决心", "解决", "决议"],
      ["She made a New Year resolution.", "The council passed a resolution."],
      ["decision", "solution"], ["doubt"],
      ["resolute", "solve"],
      ["决心：心里犹疑的结被解开、定住", "解决：把缠住的难处解开", "决议：会上表决定下的那一条"],
      "re-（彻底）+ solut（解开）→ 把结彻底解开"),
    W("resolute", "solvere", "adjective", "/ˈrezəluːt/",
      "re-（彻底）+ solut（解开）→ 犹疑已解开、心里定住的 → 坚决",
      "拉丁语 resolutus，resolvere（解开）的过去分词 ← re＋solvere",
      "showing firm determination; not wavering",
      "with the hesitation already untied, nothing left pulling back – 犹疑那道结已解开，再没什么往回拽",
      "他不再来回踱步，抬头说出那句话时脚跟没动",
      ["坚决的", "果断的"],
      ["She was resolute in her refusal.", "He gave a resolute answer."],
      ["firm", "decided"], ["doubtful", "weak"],
      ["resolution", "solve"],
      ["坚决的/果断的：犹疑已解开、心里定住不再摇"],
      "re-（彻底）+ solut（解开）→ 犹疑解开、心已定"),
]

# ================= referre（带回）=================
words += [
    W("relative", "referre", "adjective", "/ˈrelətɪv/",
      "relat（带回、关联）+ -ive → 得带回来比着看的 → 相对的；名词指亲属",
      "拉丁语 relativus（有关联的），来自 relatus（referre 的过去分词）← re＋ferre（带）",
      "considered in comparison with something else; a member of one's family",
      "only meaningful when carried back and set beside another – 非得带回来与另一个并着看才有意义",
      "单说这块高不算数，把它搬到那块旁边一比才知道",
      ["相对的", "相关的", "亲属"],
      ["It is a relative improvement.", "She invited all her relatives."],
      ["comparative", "kin"], ["absolute"],
      ["relativity", "relate"],
      ["相对的：须带回来与他物并比才有意义", "相关的：两者之间有可带回的联系", "亲属：与自己有血缘关联的人"],
      "relat（带回关联）+ -ive → 须并着比才算数"),
    W("relativity", "referre", "noun", "/ˌreləˈtɪvəti/",
      "relative（相对的）+ -ity → 相对这个性质；物理学上专指该理论",
      "英语 relativity，来自 relative ← 拉丁语 relatus ← re＋ferre",
      "the state of being relative; Einstein's theory of space and time",
      "the fact that a measure holds only against some other – 一个量非得对着另一个才立得住",
      "在车里看是静的，站在路边看却在动，得说明对着谁量",
      ["相对性", "相对论"],
      ["The theory of relativity changed physics.", "He wrote on the relativity of morals."],
      ["connection", "theory"], ["absolute"],
      ["relative", "relate"],
      ["相对性：量非得对着另一个才立得住", "相对论：以此为核心的那套物理理论"],
      "relative（相对的）+ -ity → 须对着他物才立得住"),
]

# ================= habitare（居住）=================
words += [
    W("habitat", "habitare", "noun", "/ˈhæbɪtæt/",
      "habitat（它居住）→ 某种生物惯常住的那片地方",
      "拉丁语 habitat（它居住），habitare（居住）的第三人称现在式；"
      "旧时物种志用此词起头标注产地，遂成名词",
      "the natural home of an animal or plant",
      "the place a living thing keeps returning to dwell in – 某种活物一代代回来住下的那片地方",
      "同一片湿地，那群鸟年年回来筑巢",
      ["栖息地", "生境"],
      ["The marsh is a habitat for rare birds.", "Logging destroys their habitat."],
      ["home", "environment"], [],
      ["habit", "inhabit"],
      ["栖息地/生境：某种活物惯常回来住下的那片地方"],
      "habitat（它居住）→ 惯常住下的那片地方"),
]

# ================= modus（分寸尺度）=================
words += [
    W("modern", "modus", "adjective", "/ˈmɒdn/",
      "mod（量度、时式）+ -ern → 合当下这一档时式的 → 现代的",
      "晚期拉丁语 modernus（当今的），来自 modo（just now）← modus（量度、方式）",
      "belonging to the present time; up to date",
      "cut to the measure the present moment uses – 按眼下这一档尺度裁出来的",
      "屋里陈设照当下的样式换过一轮，旧的一件没留",
      ["现代的", "近代的", "新式的"],
      ["This is modern architecture.", "She prefers modern methods."],
      ["contemporary", "current"], ["ancient", "old"],
      ["modernization", "moderate"],
      ["现代的/近代的：按眼下这一档时式裁出来的", "新式的：同一档上属新的那一头"],
      "mod（时式）+ -ern → 合当下这档时式的"),
    W("modernization", "modus", "noun", "/ˌmɒdənaɪˈzeɪʃn/",
      "modern（现代的）+ -ization → 把旧的改到当下这一档 → 现代化",
      "英语 modernization，来自 modernize ← modern ← 拉丁语 modus",
      "the process of making something suit present-day needs",
      "refitting the old thing to the measure now in use – 把旧的一样样改到眼下通行那一档",
      "老厂房一间间翻修，机器照新标准换过",
      ["现代化", "更新"],
      ["The modernization took five years.", "Farm modernization raised yields."],
      ["update", "reform"], [],
      ["modern", "moderate"],
      ["现代化/更新：把旧的改到眼下通行那一档"],
      "modern（现代的）+ -ization → 改到当下这一档"),
]

# ================= 组装 =================
# 本批不新建词根/概念/语义域，全部补进已建模的根。
# ---- 生成期自检：review.py check 不查 Q12，合并后 validate.py 才查 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"

assert len({w["id"] for w in words}) == len(words), "词条 id 有重复"
print(f"共 {len(words)} 词")

OUT.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=2) + "\n",
               encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words，全部补进已建模词根，无新根")
