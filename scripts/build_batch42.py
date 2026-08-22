#!/usr/bin/env python3
"""Generate batch42: 8 new Latin/Greek root families (25 词).

  hostis（门外来人）  host / hostage / hostess / hostile   —— hospes 与 hostis 双支
  cernere（筛分辨别）  concern / concerning / discern
  levare（举起）       lever / levy / relevant
  musa（缪斯）         music / musical / musician
  ars（技艺）          art / artist / artistic
  ordo（次序行列）     order / disorder / orderly
  origo（涌出之源）    origin / original / originate
  pangere（钉合缔结）  pact / compact / impact

单词 form / port 本批不收：roots.json 里 `form`、`port` 两个词根 id 正是这两个
英文单词本身，直接入库会产生自环边（项目现有 0 处自环，是硬不变量）。解法是先把
词根改成拉丁词形（forma / portus，照 punktum、limes、gubernare 先例），那是一次
动到 22 个已入库词的迁移，单独一步做，见 scripts/migrate_root_ids_latin.py。

写法：W() 是定参函数，漏字段直接 TypeError，不会像位置元组那样静默错位。
Q12/Q1 自检前移到生成期——review.py check 不查 Q12，只有合并后 validate.py 查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch42.json"


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

# ---------- hostis（门外来人：hospes 与 hostis 双支）----------
families.append({
    "root": {
        "id": "hostis", "root": "hostis", "variants": ["host", "hospit"],
        "origin": "拉丁语 hostis（外来者，引申为敌）与 hospes（主/客）同出原始印欧语 *ghos-ti-（外来人）；"
                  "同一个「门外来人」在善意一支成 hospes（待客），在敌意一支成 hostis（对敌）",
        "core_concept": "the outsider at the door, received or resisted / 门外来人，或迎或拒",
        "core_image": "一扇门前站着外来人：开门递茶是一支，横身挡道是另一支",
        "english_definition": "stranger at the door, guest, enemy",
    },
    "concept": {
        "id": "concept-hostis-outsider", "concept": "the outsider at the door, received or resisted",
        "chinese": "门外来人", "core_image": "门前立着外来人，或请进或挡住，两条路分出两支词",
        "root_ids": ["hostis"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("host", "hostis", "noun", "/həʊst/",
          "hospes（主/客）一支 → 开门接纳来者、张罗招待的那一方",
          "古法语 hoste，来自拉丁语 hospes（主人与客人同词），与 hostis 同源",
          "a person who receives and entertains guests; also a large number of things",
          "the one who takes in whoever arrives and sees to them – 接纳来者并一手张罗的那方",
          "门一开，来者被让进屋，茶已经斟在桌上",
          ["主人", "主持人", "大量"],
          ["The host welcomed every guest at the door.", "A host of problems followed the storm."],
          ["receiver", "presenter"], ["guest"],
          ["hostess", "hostage"],
          ["主人/主持人：接纳来者并张罗招待的一方", "大量：如同一屋子挤满来客，多到成群"],
          "hospes（主/客）→ 开门接纳来者的那一方"),
        W("hostage", "hostis", "noun", "/ˈhɒstɪdʒ/",
          "hoste（客）+ -age → 留在对方手里的「客」，实为被扣下作抵的人",
          "古法语 ostage（寄居、抵押），来自 hoste（客），源头同 hospes/hostis",
          "a person held captive as security until demands are met",
          "a guest turned pledge, kept until terms are met – 由客转为抵押，扣着等对方应条件",
          "旅人被留在营中不得走，成了对方开条件的凭据",
          ["人质"],
          ["The gunmen held three hostages inside.", "He was taken hostage on the border."],
          ["captive", "prisoner"], ["captor"],
          ["host", "hostile"],
          ["人质：被扣下充作抵押的来人"],
          "hoste（客）+ -age → 被扣在对方手里充抵的来人"),
        W("hostess", "hostis", "noun", "/ˈhəʊstəs/",
          "host（主人）+ -ess（阴性）→ 出面招待来客的女性一方",
          "英语 hostess，host 加阴性后缀 -ess",
          "a woman who receives and entertains guests",
          "the woman who takes in arrivals and sees to them – 出面接纳并招待来者的女方",
          "她举杯招呼满屋来客，一张张桌子都照看过来",
          ["女主人", "女主持人"],
          ["The hostess showed us to our seats.", "She works as an air hostess."],
          ["presenter", "receiver"], ["guest"],
          ["host", "hostage"],
          ["女主人/女主持人：出面接纳并招待来者的女方"],
          "host（招待方）+ -ess（阴性）→ 出面招待来者的女方"),
        W("hostile", "hostis", "adjective", "/ˈhɒstaɪl/",
          "hostis（外来者→对头）+ -ile → 摆出对头架势的",
          "拉丁语 hostilis（属于 hostis 的），来自 hostis（外来者、对头）",
          "unfriendly and aggressive; showing strong opposition",
          "wearing the temper of the one barred at the door – 摆出门口横身挡道那种架势",
          "来者脸色不善，话里透着要开仗的意思",
          ["敌意的", "敌对的"],
          ["The crowd turned hostile within minutes.", "They faced hostile questions all evening."],
          ["unfriendly", "aggressive"], ["friendly", "cordial"],
          ["hostage", "host"],
          ["敌意的/敌对的：摆出挡道对峙的那副架势"],
          "hostis（门外对头）+ -ile → 摆出对峙架势的"),
    ],
})

# ---------- cernere（筛分辨别）----------
families.append({
    "root": {
        "id": "cernere", "root": "cernere", "variants": ["cern", "cret"],
        "origin": "拉丁语 cernere（筛、分开、看出分别），本义是拿筛子把杂物分开",
        "core_concept": "to sift things apart until each shows clear / 筛开混杂，直到各自分明",
        "core_image": "手里的筛子一摇，砂石落下，留在网上的粒粒分明",
        "english_definition": "to sift, separate, make out",
    },
    "concept": {
        "id": "concept-cernere-sift", "concept": "to sift apart until each thing shows clear",
        "chinese": "筛开分明", "core_image": "筛子一摇，杂物落尽，留下的粒粒看得分明",
        "root_ids": ["cernere"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("concern", "cernere", "verb / noun", "/kənˈsɜːn/",
          "con-（一并）+ cern（筛分）→ 一并筛进来跟自己有牵连 → 牵动心思",
          "拉丁语 concernere（混在一起筛、相关），来自 con＋cernere",
          "to be about something, or to make someone anxious; such anxiety",
          "being sifted into the same pile as a matter, so it weighs on one – 被筛进同一堆里，事情便挂在心上",
          "消息传来，他一夜没合眼，反复过着那桩事",
          ["关心", "涉及", "担忧"],
          ["This rule concerns everyone in the building.", "Her silence caused real concern."],
          ["involve", "worry"], ["ignore"],
          ["concerning", "discern"],
          ["涉及：被筛进同一堆、与之有牵连", "关心/担忧：牵连到自己，于是挂在心上"],
          "con-（一并）+ cern（筛分）→ 被筛进同一堆 → 有牵连、挂心上"),
        W("concerning", "cernere", "preposition", "/kənˈsɜːnɪŋ/",
          "concern（牵涉）的分词转介词 → 就所牵涉的那件事而言",
          "英语 concerning，concern 的现在分词转作介词",
          "about; with reference to a particular matter",
          "pointing at the very pile a matter was sifted into – 直指某事被归进的那一堆",
          "信里逐条写的，都紧扣那笔款的来龙去脉",
          ["关于", "有关"],
          ["He asked several questions concerning the delay.", "We had no news concerning her whereabouts."],
          ["regarding", "about"], [],
          ["concern", "discern"],
          ["关于/有关：就所牵涉的那一桩而言"],
          "concern（牵涉）+ -ing → 就所牵涉的那桩而言"),
        W("discern", "cernere", "verb", "/dɪˈsɜːn/",
          "dis-（分开）+ cern（筛分）→ 一层层筛开，直到看出分别",
          "拉丁语 discernere（区分开来），来自 dis＋cernere",
          "to recognize or make out something with effort",
          "sifting the layers apart until the thing stands out – 层层筛开，直到那物凸显出来",
          "隔着晨雾眯眼细看，岸上那道影子终于显出轮廓",
          ["辨别", "认出", "洞悉"],
          ["She could just discern a figure in the fog.", "It is hard to discern his true motive."],
          ["distinguish", "perceive"], ["confuse", "overlook"],
          ["concern", "concerning"],
          ["辨别/认出：筛开混杂后把那物分出来", "洞悉：筛到底层、连内里也看出来"],
          "dis-（分开）+ cern（筛分）→ 筛开层层，看出分别"),
    ],
})

# ---------- levare（举起）----------
families.append({
    "root": {
        "id": "levare", "root": "levare", "variants": ["lev", "liev"],
        "origin": "拉丁语 levare（举起、减轻），来自 levis（轻的）：使变轻即托得起来",
        "core_concept": "to raise a load by making it light / 把重物托起、使之变轻",
        "core_image": "一头垫住石块，另一头轻轻下压，沉物就离了地",
        "english_definition": "to lift, raise, lighten",
    },
    "concept": {
        "id": "concept-levare-lift", "concept": "to raise a load by making it light",
        "chinese": "托举变轻", "core_image": "一压一撬，沉甸甸的石头就离了地面",
        "root_ids": ["levare"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("lever", "levare", "noun", "/ˈliːvə(r)/",
          "lev（举起）+ -er（工具）→ 用来把重物撬起来的那根杆",
          "古法语 levier（撬棒），来自 lever（举起）← 拉丁语 levare",
          "a bar used to prise something up; a means of exerting pressure",
          "the bar that raises a weight far heavier than the hand pressing it – 以小力撬起远重于手劲之物的杆",
          "长杆一头垫住石块，另一头轻轻下压，巨石离地",
          ["杠杆", "手段"],
          ["He used an iron bar as a lever.", "Tax breaks became a political lever."],
          ["bar", "crowbar"], [],
          ["levy", "relevant"],
          ["杠杆：以小力撬起重物的那根杆", "手段：像撬杆一样能撬动局面的着力处"],
          "lev（举起）+ -er（工具）→ 撬起重物的那根杆"),
        W("levy", "levare", "verb / noun", "/ˈlevi/",
          "lev（举起）→ 把款项或人手「举」起收拢到官府手里",
          "古法语 levee（收取、征集），来自 lever（举起）← 拉丁语 levare",
          "to impose and collect a tax or troops; the amount so raised",
          "raising a sum or a body of men out of the populace – 从民间把银钱或人手举收上来",
          "官府张榜，按册向各户收取银钱",
          ["征收", "征募", "税款"],
          ["The council levied a new charge on parking.", "A levy was placed on imported goods."],
          ["impose", "collect"], ["refund"],
          ["lever", "relevant"],
          ["征收/税款：从民间举收上来的银钱", "征募：同样手法举收人手入伍"],
          "lev（举起）→ 从民间举收银钱或人手"),
        W("relevant", "levare", "adjective", "/ˈreləvənt/",
          "re-（回）+ lev（举起）+ -ant → 能把话题重新托举起来的 → 搭得上",
          "中世纪拉丁语 relevans（托起、有助于），来自 relevare（再举起）",
          "closely connected with the matter being discussed",
          "able to lift the matter at hand rather than hang off it – 托得起眼下这桩事，而非旁挂",
          "他提的两点正落在会上要议的那桩事上",
          ["相关的", "切题的"],
          ["Please bring any relevant paperwork.", "That remark was hardly relevant here."],
          ["pertinent", "applicable"], ["irrelevant"],
          ["lever", "levy"],
          ["相关的/切题的：托得起眼下这桩事、搭得上"],
          "re-（回）+ lev（举起）→ 把眼下话题托举得起 → 搭得上"),
    ],
})

# ---------- musa（缪斯）----------
families.append({
    "root": {
        "id": "musa", "root": "musa", "variants": ["mus", "muse"],
        "origin": "希腊语 Mousa（缪斯，司文艺的九女神）经拉丁语 musa 入英语；"
                  "mousike techne（缪斯的技艺）本指诗歌与声律合一的技艺",
        "core_concept": "the ordered sound the Muses grant / 缪斯所赐、合于法度的声响技艺",
        "core_image": "琴弦被拨动，一串声响按着法度次第流出",
        "english_definition": "the Muse, ordered sound",
    },
    "concept": {
        "id": "concept-musa-ordered-sound", "concept": "the ordered sound the Muses grant",
        "chinese": "缪斯声律", "core_image": "指尖拨过琴弦，声响依法度次第流出",
        "root_ids": ["musa"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("music", "musa", "noun", "/ˈmjuːzɪk/",
          "mus（缪斯）+ -ic（…的技艺）→ 缪斯所司的声律技艺",
          "希腊语 mousike（缪斯的技艺）经拉丁语 musica、古法语 musique 入英语",
          "sounds arranged in a pleasing or ordered way",
          "sound set in order so the ear follows it – 把声响排布成序，耳朵便跟得上",
          "琴弦一拨，满室的说话声就静了下来",
          ["音乐", "乐曲"],
          ["She has listened to this music all week.", "The music grew louder as we entered."],
          ["melody", "tune"], ["noise"],
          ["musical", "musician"],
          ["音乐/乐曲：排布成序、耳朵跟得上的声响"],
          "mus（缪斯）+ -ic → 缪斯所司的声律技艺"),
        W("musical", "musa", "adjective", "/ˈmjuːzɪkl/",
          "music（声律技艺）+ -al（…的）→ 属于声律的、听着顺耳的",
          "英语 musical，music 加形容词后缀 -al",
          "relating to sound arranged in order; pleasant to hear",
          "belonging to ordered sound, so it falls kindly on the ear – 属于有序声响，故听来顺耳",
          "这孩子开口一唱，调子准得让人侧耳",
          ["音乐的", "悦耳的"],
          ["He comes from a musical family.", "She spoke in a soft, musical voice."],
          ["melodious", "tuneful"], ["tuneless"],
          ["music", "musician"],
          ["音乐的：属于声律技艺的", "悦耳的：合于法度，听来顺耳"],
          "music（声律）+ -al → 属于声律的、听来顺耳"),
        W("musician", "musa", "noun", "/mjuˈzɪʃn/",
          "music（声律技艺）+ -ian（司此业者）→ 以声律技艺为业的人",
          "古法语 musicien，来自拉丁语 musicus（通声律者）",
          "a person who plays or writes music, especially as a job",
          "one whose craft is ordered sound – 以有序声响为业的人",
          "台上几人调好弦，静候指挥落棒",
          ["音乐家", "乐手"],
          ["The musician tuned her violin.", "He became a professional musician at twenty."],
          ["player", "performer"], ["listener"],
          ["music", "musical"],
          ["音乐家/乐手：以声律技艺为业的人"],
          "music（声律）+ -ian（司此业者）→ 以声律为业的人"),
    ],
})

# ---------- ars（技艺）----------
families.append({
    "root": {
        "id": "ars", "root": "ars", "variants": ["art"],
        "origin": "拉丁语 ars（属格 artis：手上练出的本事、门道），与 artus（关节、接合）同源，"
                  "本义偏「把东西接合安排得当的手艺」",
        "core_concept": "skill of the trained hand, arranging things aright / 练出来的手上功夫，把物事安排得当",
        "core_image": "一双练过千遍的手，把零散材料摆布成让人挪不开眼的东西",
        "english_definition": "skill, craft, art",
    },
    "concept": {
        "id": "concept-ars-craft", "concept": "the trained hand's skill in arranging things aright",
        "chinese": "手上功夫", "core_image": "练过千遍的手，把零散材料摆布成挪不开眼的东西",
        "root_ids": ["ars"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("art", "ars", "noun", "/ɑːt/",
          "ars（手上本事）→ 练出来的门道，及其做出的作品",
          "古法语 art，来自拉丁语 ars/artis（手艺、门道）",
          "the making of things meant to be looked at or admired; a learned skill",
          "what the trained hand brings forth, and the knack behind it – 练过的手所成之物，及其中门道",
          "画布上一笔一笔堆出光影，看的人半晌没说话",
          ["艺术", "美术", "技艺"],
          ["She studied art for four years.", "There is an art to asking good questions."],
          ["craft", "skill"], [],
          ["artist", "artistic"],
          ["艺术/美术：练出的手所成、供人观览之物", "技艺：做成此物背后的那套门道"],
          "ars（手上练出的本事）→ 门道，及其做出的作品"),
        W("artist", "ars", "noun", "/ˈɑːtɪst/",
          "art（手艺）+ -ist（司此业者）→ 以这门手上功夫为业的人",
          "法语 artiste，来自中世纪拉丁语 artista（通艺者）← ars",
          "a person who makes paintings, sculpture, or other such works",
          "one whose trade is the trained hand's making – 以练出的手做东西为业的人",
          "他在阁楼里对着画架站了一整天，颜料蹭到袖口",
          ["艺术家", "画家"],
          ["The artist worked in oils and charcoal.", "She is a well-known artist in this city."],
          ["painter", "creator"], ["critic"],
          ["art", "artistic"],
          ["艺术家/画家：以练出的手做东西为业的人"],
          "art（手艺）+ -ist（司此业者）→ 以此手艺为业的人"),
        W("artistic", "ars", "adjective", "/ɑːˈtɪstɪk/",
          "artist（司艺者）+ -ic（…的）→ 见得出手上门道的、有讲究的",
          "英语 artistic，artist 加形容词后缀 -ic",
          "showing skill and taste in making or arranging things",
          "bearing the mark of a trained hand's judgement – 带着练过的手那份分寸",
          "这只陶碗的弧线收得讲究，摆上桌就压住了满桌俗气",
          ["艺术的", "有美感的"],
          ["The room had an artistic arrangement of flowers.", "He has real artistic talent."],
          ["tasteful", "creative"], ["crude"],
          ["art", "artist"],
          ["艺术的/有美感的：带着练过的手那份分寸与讲究"],
          "artist（司艺者）+ -ic → 见得出手上门道的、有讲究的"),
    ],
})

# ---------- ordo（次序行列）----------
families.append({
    "root": {
        "id": "ordo", "root": "ordo", "variants": ["ord", "ordin"],
        "origin": "拉丁语 ordo（属格 ordinis：行列、次序），本指织机上排开的经线，"
                  "引申为凡物各就其位的排布",
        "core_concept": "each thing standing in its own place in a row / 各就各位、排成一列",
        "core_image": "一列物件按高矮排开，谁也不越出自己那格",
        "english_definition": "row, rank, arrangement",
    },
    "concept": {
        "id": "concept-ordo-arrangement", "concept": "each thing standing in its own place in a row",
        "chinese": "各就各位", "core_image": "一列物件按高矮排开，谁也不越出自己那格",
        "root_ids": ["ordo"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("order", "ordo", "noun / verb", "/ˈɔːdə(r)/",
          "ordo（行列）→ 各就其位的排布；由「排定」引申为排定要办之事、要买之货",
          "古法语 ordre，来自拉丁语 ordo/ordinis（行列、次序）",
          "the way things are arranged; an instruction to do something; a request for goods",
          "things standing each in its place, and the word that puts them there – 各就其位的排布，以及使其就位的那句话",
          "书脊按高矮一列排开，谁也不越位；掌事的一句话下来，各人照着做",
          ["顺序", "秩序", "命令", "订单"],
          ["Please put the files back in order.", "The captain ordered them to wait."],
          ["sequence", "command"], ["chaos"],
          ["disorder", "orderly"],
          ["顺序/秩序：各就其位的那个排布", "命令：使各人就位去办的那句话", "订单：把要买之货排定下来"],
          "ordo（行列）→ 各就其位；使之就位便是发话与排定"),
        W("disorder", "ordo", "noun", "/dɪsˈɔːdə(r)/",
          "dis-（离散）+ order（各就其位）→ 位次散了 → 乱；身体位次乱了即病症",
          "法语 désordre（无秩序），dis-＋ordre ← 拉丁语 ordo",
          "a state of confusion; also an illness that upsets normal function",
          "the row broken up, nothing standing where it should – 行列散开，无一物在该在的位上",
          "抽屉被翻得底朝天，东西全不在原处",
          ["混乱", "失调", "疾病"],
          ["The room was left in complete disorder.", "He suffers from a sleep disorder."],
          ["chaos", "confusion"], ["order"],
          ["order", "orderly"],
          ["混乱：行列散开、无物在其位", "失调/疾病：身体各处的位次乱了"],
          "dis-（离散）+ order（就位）→ 位次散乱"),
        W("orderly", "ordo", "adjective", "/ˈɔːdəli/",
          "order（各就其位）+ -ly（…样的）→ 一眼看去各在其位的",
          "英语 orderly，order 加后缀 -ly",
          "neatly arranged; behaving in a controlled way",
          "keeping the row unbroken, each in place – 行列不散，各守其位",
          "队伍一列列排开，间距分毫不差",
          ["整齐的", "有条理的"],
          ["They formed an orderly queue at the gate.", "She keeps an orderly desk."],
          ["tidy", "methodical"], ["chaotic"],
          ["order", "disorder"],
          ["整齐的/有条理的：行列不散、各守其位"],
          "order（就位）+ -ly → 各在其位、看去不散"),
    ],
})

# ---------- origo（涌出之源）----------
families.append({
    "root": {
        "id": "origo", "root": "origo", "variants": ["orig", "ori"],
        "origin": "拉丁语 origo（属格 originis：发端、出处），来自 oriri（升起、涌出），"
                  "与 oriens（东方，日升之处）同根",
        "core_concept": "the point where something first rises up / 事物最初涌出来的那一处",
        "core_image": "顺溪流一路上溯，走到山间那眼往上冒水的泉口",
        "english_definition": "rising, source, beginning",
    },
    "concept": {
        "id": "concept-origo-source", "concept": "the point where something first rises up",
        "chinese": "涌出之源", "core_image": "溯流而上，尽头是那眼往上冒水的泉口",
        "root_ids": ["origo"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("origin", "origo", "noun", "/ˈɒrɪdʒɪn/",
          "origo（涌出之处）→ 事物最初冒出来的那一处，及人的出处",
          "法语 origine，来自拉丁语 origo/originis（发端）← oriri（升起）",
          "the point or cause from which something begins; a person's ancestry",
          "the spot where a thing first rises into being – 那物最初冒出来的那一处",
          "顺着溪流一路上溯，直到山间那眼冒水的泉口",
          ["起源", "出身", "起点"],
          ["The origin of the fire is still unknown.", "She is proud of her humble origins."],
          ["source", "beginning"], ["end", "outcome"],
          ["original", "originate"],
          ["起源/起点：事物最初涌出的那一处", "出身：人所从来的那一处"],
          "origo（涌出之处）→ 最初冒出来的那一点"),
        W("original", "origo", "adjective / noun", "/əˈrɪdʒənl/",
          "origin（发端）+ -al（…的）→ 处在最初那一处的；也指头一份实物",
          "古法语 original，来自拉丁语 originalis（属于发端的）",
          "existing from the start; new and not copied; the first version of a thing",
          "standing at the rising point, before any copy – 立在涌出那一处，尚无摹本",
          "抽屉里那张手稿是头一份，后来的都照着它抄",
          ["最初的", "原创的", "原件"],
          ["The house keeps its original windows.", "Please send me the original, not a copy."],
          ["initial", "authentic"], ["copy", "imitation"],
          ["origin", "originate"],
          ["最初的：立在发端那一处的", "原创的：从自己那处涌出、非摹自他人", "原件：头一份实物，摹本之前的那个"],
          "origin（发端）+ -al → 处在最初那一处、尚无摹本"),
        W("originate", "origo", "verb", "/əˈrɪdʒɪneɪt/",
          "origin（发端）+ -ate（使…）→ 自某处涌出、由某处发端",
          "中世纪拉丁语 originare（发端于），来自 origo",
          "to begin in a particular place or from a particular cause",
          "to come rising out of a given spot – 自某一处冒出来",
          "这条河的水，是从那道石缝里第一次涌出来的",
          ["起源于", "发源", "创始"],
          ["The custom originated in southern Spain.", "The idea originated with her, not him."],
          ["arise", "stem"], ["end", "conclude"],
          ["origin", "original"],
          ["起源于/发源：自某处涌出来", "创始：使某物从自己这处涌出"],
          "origin（发端）+ -ate → 自某处涌出来"),
    ],
})

# ---------- pangere（钉合缔结）----------
families.append({
    "root": {
        "id": "pangere", "root": "pangere", "variants": ["pact", "ping", "pag"],
        "origin": "拉丁语 pangere（钉入、固定、缔结），过去分词 pactus；"
                  "把桩钉牢即定下约，故 pactum 表协议，compingere/impingere 表拼合与撞入",
        "core_concept": "to drive a thing fast in place, hence to fix an agreement / 把物钉牢固定，引申为定下约",
        "core_image": "木桩被一锤锤钉进土里，钉牢了就再也挪不动",
        "english_definition": "to fix, fasten, settle",
    },
    "concept": {
        "id": "concept-pangere-fix", "concept": "to drive a thing fast in place, hence to settle an accord",
        "chinese": "钉牢定约", "core_image": "木桩一锤锤钉进土里，钉牢便再挪不动",
        "root_ids": ["pangere"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("pact", "pangere", "noun", "/pækt/",
          "pactum（已钉牢之事）→ 双方钉定下来的约",
          "拉丁语 pactum（协议），pacisci（缔约）的过去分词，源于 pangere（钉牢）",
          "a formal agreement between two or more sides",
          "the terms driven fast so neither side may shift them – 条款被钉牢，两边都不得再挪",
          "两方在纸上各按一个手印，从此照纸上写的办",
          ["协定", "条约"],
          ["The two nations signed a trade pact.", "They made a pact never to speak of it."],
          ["agreement", "treaty"], ["dispute"],
          ["compact", "impact"],
          ["协定/条约：被钉牢、双方不得再挪的约"],
          "pactum（钉牢之事）→ 双方钉定下来的约"),
        W("compact", "pangere", "adjective", "/kəmˈpækt/",
          "com-（一起）+ pact（钉合）→ 各部分钉合在一起、不占地方的",
          "拉丁语 compactus，compingere（拼合钉牢）的过去分词，来自 com＋pangere",
          "closely packed into a small space; neatly small",
          "parts driven together so no gap is left – 各部分钉合到一处，不留空隙",
          "行李被压得严丝合缝，箱盖一扣还有余地",
          ["紧密的", "小巧的"],
          ["The flat has a compact kitchen.", "Snow was compact underfoot."],
          ["dense", "tight"], ["loose", "bulky"],
          ["pact", "impact"],
          ["紧密的：各部分钉合到一处、不留空隙", "小巧的：因钉合紧密而不占地方"],
          "com-（一起）+ pact（钉合）→ 钉合到一处、不留空隙"),
        W("impact", "pangere", "noun / verb", "/ˈɪmpækt/",
          "im-（in- 向内）+ pact（钉入）→ 直钉进去的那一下 → 撞击及其后果",
          "拉丁语 impactus，impingere（撞入、钉入）的过去分词，来自 in＋pangere",
          "the force of one thing striking another; a marked effect on something",
          "the blow of being driven into a thing, and what it leaves behind – 钉进去那一下，以及留下的后果",
          "石子砸进水面，波纹一圈圈荡到岸边",
          ["撞击", "影响", "冲击"],
          ["The impact shattered the windscreen.", "New rules had a real impact on costs."],
          ["collision", "effect"], [],
          ["pact", "compact"],
          ["撞击：直钉进去那一下", "影响/冲击：那一下过后留在事物上的后果"],
          "im-（向内）+ pact（钉入）→ 钉进去那一下及其后果"),
    ],
})

# ================= 组装 =================
words = []
for fam in families:
    words.extend(fam["words"])

roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
# 同一语义域可能收多个新词根，必须累积追加（dict 直接赋值会丢根，第三十六批踩过）
domain_add = {}
for f in families:
    domain_add.setdefault(f["domain"], []).append(f["root"]["id"])

# ---- 生成前自检：把质量门前移，错了当场炸而不是合并后再回滚 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"

assert len(words) == 25, len(words)
assert len(roots) == 8, len(roots)
assert len({r["id"] for r in roots}) == 8, "新词根 id 有重复"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words, {len(roots)} new roots")
