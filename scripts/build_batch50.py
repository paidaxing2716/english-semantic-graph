#!/usr/bin/env python3
"""Generate batch50: 反查工具的第一批收获——25 词，全部补进已建模词根，不新建根。

这批词的来路与前 14 批不同：它们全在 classify_wordlist.py 判定的
「3682 个孤立词」里，但逐条核词源后确认属于已建模的词根，只是词干提取
按拼写聚类抓不到（receive 与 capable 拼写毫无交集，却同出 capere）。
候选由 scripts/find_root_members.py 反查得出，再人工核词源筛定。

  cep（capere 抓取）    receive / deceive / conceive / perceive / capture / captive
  pars（partis 份）     participate / participant / particle / particular
                        / apart / apartment
  metron（量度）        diameter / parameter / thermometer / geometry / centimetre
  tract（trahere 拉）   treat / treaty / retreat
  signum（记号）        signature / significance / significant
  stringere（拉紧）     strict / restrict / district

【剔除的同形异源候选，勿再捡回】
  captain / capital ← caput（头），不是 capere
  metropolitan     ← 希腊 mētēr（母）+ polis（城），不是 metron
  cemetery         ← 希腊 koimētērion（安寝处），与 metron 无关
  string           ← 原始日耳曼语 *strangiz，不是 stringere
  standpoint       ← 英语自造复合词，不是 punktum 的拉丁派生
  spicy            ← spice ← species，语义已远，不作 spect 族收
  partner / party  ← 经古法语走形较远，留待专批再审

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch50.json"


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

# ================= cep（capere 抓取）=================
words += [
    W("receive", "cep", "verb", "/rɪˈsiːv/",
      "re-（回）+ ceive（接住）→ 把递来的接到手里",
      "古法语 receivre，来自拉丁语 recipere（收取）← re＋capere（抓取）",
      "to be given or sent something; to take delivery of",
      "closing the hand on what has been sent one's way – 把送到跟前的东西接进手里",
      "门口递进来一个包裹，他伸手接过，签了字",
      ["收到", "接受", "接待"],
      ["She received a letter this morning.", "The hotel receives guests all year."],
      ["accept", "obtain"], ["send", "reject"],
      ["reception", "deceive"],
      ["收到/接受：把送来的接进手里", "接待：把来客接进门"],
      "re-（回）+ ceive（接住）→ 把递来的接到手里"),
    W("deceive", "cep", "verb", "/dɪˈsiːv/",
      "de-（脱开正道）+ ceive（接住）→ 让人接住的是假的 → 欺骗",
      "古法语 deceivre，来自拉丁语 decipere（诱骗）← de＋capere（抓取）",
      "to make someone believe something that is not true",
      "handing over something false for the other to take as real – 递过去一件假的，让对方当真接下",
      "他把掺了水的那壶递过去，对方没尝出来",
      ["欺骗", "蒙骗", "误导"],
      ["He deceived his own family for years.", "Do not let appearances deceive you."],
      ["mislead", "cheat"], ["enlighten"],
      ["receive", "conceive"],
      ["欺骗/蒙骗：递过去假的让人当真接下", "误导：使人接住的判断偏了道"],
      "de-（脱开正道）+ ceive（接住）→ 让人接下假的"),
    W("conceive", "cep", "verb", "/kənˈsiːv/",
      "con-（收进）+ ceive（接住）→ 接进来在里头成形 → 构想；亦指怀胎",
      "古法语 conceivre，来自拉丁语 concipere（收纳、孕育）← con＋capere",
      "to form an idea in the mind; to become pregnant",
      "taking a thing in and letting it take shape inside – 接进来，让它在里头长成形",
      "那个念头一进脑子就慢慢长出了轮廓",
      ["构想", "设想", "怀孕"],
      ["She conceived the plan on the train.", "They could not conceive a child."],
      ["imagine", "devise"], [],
      ["receive", "perceive"],
      ["构想/设想：接进来在心里长成形", "怀孕：同一个「接进来使成形」用在孕育上"],
      "con-（收进）+ ceive（接住）→ 接进来在里头成形"),
    W("perceive", "cep", "verb", "/pəˈsiːv/",
      "per-（彻底）+ ceive（接住）→ 把外来讯息完整接住 → 察觉",
      "古法语 perceivre，来自拉丁语 percipere（察知）← per＋capere",
      "to become aware of something through the senses; to regard in a certain way",
      "catching what comes in fully enough to know it – 把送进来的接得够全，于是知道了",
      "风里那点异味被他一下接住，立刻回头看",
      ["察觉", "感知", "看待"],
      ["She perceived a change in his tone.", "He is perceived as a fair judge."],
      ["notice", "discern"], ["overlook"],
      ["receive", "conceive"],
      ["察觉/感知：把外来讯息接得够全而知晓", "看待：接住之后认定成某个样子"],
      "per-（彻底）+ ceive（接住）→ 把讯息接得够全"),
    W("capture", "cep", "verb", "/ˈkæptʃə(r)/",
      "capt（抓取）+ -ure → 一把抓到手里 → 捕获；引申为把景象留住",
      "法语 capture，来自拉丁语 captura（捕获）← capere（抓取）",
      "to catch a person or animal; to record or preserve something",
      "closing the hand on what was loose – 把在外头的一把抓进手里",
      "网一收，方才还在跳的那条被兜住了",
      ["捕获", "夺取", "捕捉"],
      ["The escaped animal was captured at dawn.", "The photo captured her expression."],
      ["seize", "catch"], ["release", "free"],
      ["captive", "receive"],
      ["捕获/夺取：一把抓到手里", "捕捉：把稍纵即逝的景象留住"],
      "capt（抓取）+ -ure → 一把抓到手里"),
    W("captive", "cep", "noun", "/ˈkæptɪv/",
      "capt（抓取）+ -ive → 已被抓住、脱不了身的那个",
      "拉丁语 captivus（被俘的），来自 captus（capere 的过去分词）",
      "a person kept as a prisoner; held and unable to leave",
      "the one already in the closed hand – 已经落在合起来那只手里的人",
      "绳子系在木桩上，那人整夜没能挪出那个圈",
      ["俘虏", "被囚者"],
      ["The captives were released at last.", "He was held captive for a month."],
      ["prisoner", "hostage"], ["captor"],
      ["capture", "receive"],
      ["俘虏/被囚者：已被抓住、脱不了身的那个"],
      "capt（抓取）+ -ive → 已被抓住脱不了身的"),
]

# ================= pars（partis 份）=================
words += [
    W("participate", "pars", "verb", "/pɑːˈtɪsɪpeɪt/",
      "parti（份）+ cip（取）+ -ate → 领走自己那一份 → 加入其中",
      "拉丁语 participare（分享、参与），来自 pars（份）＋capere（取）",
      "to take part in an activity or event",
      "taking up one's own share of a joint doing – 在共做的事里领走属于自己那一份",
      "几个人各领一段绳，一头一个攥着往上拉",
      ["参加", "参与"],
      ["She participates in every rehearsal.", "Only members may participate."],
      ["join", "engage"], ["abstain"],
      ["participant", "particle"],
      ["参加/参与：在共做之事里领走自己那一份"],
      "parti（份）+ cip（取）→ 领走自己那一份"),
    W("participant", "pars", "noun", "/pɑːˈtɪsɪpənt/",
      "participate（领份加入）+ -ant（人）→ 领了一份、在其中的那个人",
      "拉丁语 participans，participare 的现在分词",
      "a person who takes part in something",
      "the one holding a share of the work – 手里攥着一份活的那个人",
      "名单上每个名字后头都跟着一段分给他的活",
      ["参与者", "参加者"],
      ["Each participant received a badge.", "Twelve participants signed up."],
      ["member", "contributor"], ["witness"],
      ["participate", "particular"],
      ["参与者/参加者：领了一份、身在其中的人"],
      "participate（领份加入）+ -ant → 领了一份的那个人"),
    W("particle", "pars", "noun", "/ˈpɑːtɪkl/",
      "parti（份）+ -cle（小）→ 份里最小的那一点",
      "拉丁语 particula（小部分），pars 的指小形",
      "an extremely small piece of matter",
      "the smallest share a thing can be broken into – 一物能分到的最小那一份",
      "光柱里浮着数不清的细屑，一粒一粒看得见",
      ["微粒", "粒子", "极少量"],
      ["Dust particles hung in the light.", "There is not a particle of truth in it."],
      ["grain", "fragment"], ["mass"],
      ["particular", "participate"],
      ["微粒/粒子：份里最小的那一点", "极少量：小到只剩一点点的那个量"],
      "parti（份）+ -cle（小）→ 份里最小的那一点"),
    W("particular", "pars", "adjective", "/pəˈtɪkjələ(r)/",
      "particul（小份）+ -ar（…的）→ 单指其中那一份的 → 特定的；引申为挑剔",
      "拉丁语 particularis（属于部分的），来自 particula",
      "specific rather than general; hard to please",
      "singling out one share instead of the whole – 从整体里只指定那一份",
      "他从一摞里单挑出那一份，别的都不看",
      ["特定的", "挑剔的", "详情"],
      ["This particular case is different.", "He is particular about his coffee."],
      ["specific", "fussy"], ["general"],
      ["particle", "participant"],
      ["特定的：从整体里只指定那一份", "挑剔的：只肯要合意那一份", "详情：逐份说清的那些条目"],
      "particul（小份）+ -ar → 只指定其中那一份"),
    W("apart", "pars", "adverb", "/əˈpɑːt/",
      "a-（ad- 朝）+ part（份）→ 各归各份 → 分处两边",
      "古法语 a part（各自一边），来自拉丁语 ad partem（朝各份）",
      "separated by a distance; into pieces",
      "each share standing off on its own – 各份各占一边，中间空着",
      "两只箱子摆在屋子两头，中间空出一大片",
      ["分开", "相隔", "除外"],
      ["They stood ten metres apart.", "The old chair fell apart."],
      ["separately"], ["together"],
      ["apartment", "part"],
      ["分开/相隔：各份各占一边", "除外：把那一份单撇出去不算"],
      "a-（朝）+ part（份）→ 各归各份、分处两边"),
    W("apartment", "pars", "noun", "/əˈpɑːtmənt/",
      "apart（各归各份）+ -ment → 整栋被隔出来的那一户",
      "法语 appartement，来自意大利语 appartamento ← a parte（各自一边）",
      "a set of rooms in a building, used as one home",
      "the share a building is divided into – 整栋房子分出来的那一份",
      "一层楼被墙隔成几户，各有各的门",
      ["公寓", "套房"],
      ["They rent an apartment downtown.", "Her apartment is on the third floor."],
      ["flat", "residence"], [],
      ["apart", "part"],
      ["公寓/套房：整栋房子隔出来的那一份"],
      "apart（各归各份）+ -ment → 隔出来的那一户"),
]

# ================= metron（量度）=================
words += [
    W("diameter", "metron", "noun", "/daɪˈæmɪtə(r)/",
      "dia-（穿过）+ meter（量度）→ 穿过圆心量出的那条长",
      "希腊语 diametros（横贯的线），来自 dia（穿过）＋metron（量度）",
      "a straight line passing through the centre of a circle",
      "the length measured straight across through the middle – 从中间穿过去量出的那一段长",
      "一条线从圆边穿过正中，抵到对面那一点",
      ["直径"],
      ["The circle has a diameter of ten centimetres.", "Measure the diameter of the pipe."],
      ["breadth", "width"], ["radius"],
      ["parameter", "centimetre"],
      ["直径：穿过圆心量出的那条长"],
      "dia-（穿过）+ meter（量度）→ 穿过正中量出的长"),
    W("parameter", "metron", "noun", "/pəˈræmɪtə(r)/",
      "para-（旁）+ meter（量度）→ 旁边立起的量尺 → 划定范围的那个量",
      "希腊语 para（旁）＋metron（量度），经近代科学用语入英语",
      "a limit or boundary that defines the scope of something",
      "the rod set alongside to mark how far a thing may go – 旁边立一根尺，定住它能走多远",
      "旋钮定在几个刻度上，机器只在这几档之内动",
      ["参数", "参量", "界限"],
      ["Set the parameters before running the test.", "We must work within these parameters."],
      ["limit", "variable"], [],
      ["diameter", "thermometer"],
      ["参数/参量：旁边立起、用来定量的那个尺度", "界限：这把尺划出的可行范围"],
      "para-（旁）+ meter（量度）→ 旁立一尺定住范围"),
    W("thermometer", "metron", "noun", "/θəˈmɒmɪtə(r)/",
      "thermo-（热）+ meter（量度）→ 量热的那件器具",
      "希腊语 thermos（热）＋metron（量度），17 世纪造词",
      "an instrument for measuring temperature",
      "the tool that puts a number on how hot a thing is – 把冷热读成数字的那件器具",
      "玻璃管里那道细红线随冷热上下爬",
      ["温度计", "体温计"],
      ["The thermometer read thirty degrees.", "Put the thermometer under your arm."],
      ["gauge", "instrument"], [],
      ["parameter", "diameter"],
      ["温度计/体温计：把冷热量成数字的那件器具"],
      "thermo-（热）+ meter（量度）→ 量热的器具"),
    W("geometry", "metron", "noun", "/dʒiˈɒmətri/",
      "geo-（地）+ metr（量度）+ -y → 本是量地之术，后成研究形与空间的学问",
      "希腊语 geōmetria（测地术），来自 gē（地）＋metron（量度）",
      "the branch of mathematics dealing with shapes and space",
      "what began as measuring the ground and grew into the study of shape – 起于量地，后来专研形状与空间",
      "拿绳量地，边长与夹角一一记下",
      ["几何学", "几何结构"],
      ["She teaches geometry to first-years.", "The geometry of the roof is complex."],
      ["arithmetic", "structure"], [],
      ["diameter", "centimetre"],
      ["几何学：起于量地、后专研形状空间的学问", "几何结构：某物在形状上的排布"],
      "geo-（地）+ metr（量度）→ 起于量地的形状之学"),
    W("centimetre", "metron", "noun", "/ˈsentɪmiːtə(r)/",
      "centi-（百分之一）+ metre（米）→ 一米的百分之一",
      "法语 centimètre，由拉丁 centum（百）＋希腊 metron（量度）合成",
      "a unit of length equal to one hundredth of a metre",
      "one of the hundred parts a metre is cut into – 一米均分成百份里的一份",
      "尺子上一米被均分成一百格，取其中一格",
      ["厘米", "公分"],
      ["The line is four centimetres long.", "Cut two centimetres off the end."],
      ["unit", "measure"], [],
      ["metre", "geometry"],
      ["厘米/公分：一米均分成百份后的一份"],
      "centi-（百分之一）+ metre（米）→ 一米的百分之一"),
]

# ================= tract（trahere 拉）=================
words += [
    W("treat", "tract", "verb", "/triːt/",
      "tractare（反复拉扯、处置）→ 把事拉到手上处置 → 对待、医治",
      "古法语 traitier，来自拉丁语 tractare（处理），trahere（拉）的反复体",
      "to behave toward someone in a certain way; to give medical care",
      "drawing a matter to hand and dealing with it – 把事拉到手边，一样样处置",
      "他把那件事拉到手边，一条一条过",
      ["对待", "治疗", "款待"],
      ["They treated her with respect.", "The doctor treated his wound."],
      ["handle", "cure"], ["neglect"],
      ["treaty", "retreat"],
      ["对待：把事或人拉到手边如此处置", "治疗：把病拉到手上处置", "款待：以酒食待客这般处置"],
      "tractare（拉到手上处置）→ 对待、医治"),
    W("treaty", "tract", "noun", "/ˈtriːti/",
      "treat（处置、商议）+ -y → 商议处置之后立下的文书",
      "古法语 traité，来自拉丁语 tractatus（处理、论述）← tractare",
      "a formal agreement between countries",
      "what two sides set down after drawing the matter out together – 两方把事拉到一处议定后写下的那纸",
      "两方被拉到一张桌前，谈定的每条都写进纸里",
      ["条约", "协定"],
      ["The treaty was signed in Vienna.", "Both sides honoured the treaty."],
      ["pact", "accord"], ["dispute"],
      ["treat", "retreat"],
      ["条约/协定：两方议定后写下的那纸文书"],
      "treat（商议处置）+ -y → 议定后立下的文书"),
    W("retreat", "tract", "verb", "/rɪˈtriːt/",
      "re-（往回）+ treat（拉）→ 把自己往回拉 → 撤退；名词亦指退居之所",
      "古法语 retrait（退回），来自拉丁语 retrahere（拉回）← re＋trahere",
      "to move back from a position; a quiet place to withdraw to",
      "drawing oneself back from where one stood – 把自己从原处往回拉",
      "队伍把自己往后拉，一步步离开那道坡",
      ["撤退", "后退", "静居处"],
      ["The army retreated at nightfall.", "She spends August at a mountain retreat."],
      ["withdraw", "refuge"], ["advance"],
      ["treat", "treaty"],
      ["撤退/后退：把自己往回拉离原处", "静居处：退到那里图个清静的地方"],
      "re-（往回）+ treat（拉）→ 把自己往回拉"),
]

# ================= signum（记号）=================
words += [
    W("signature", "signum", "noun", "/ˈsɪɡnətʃə(r)/",
      "sign（记号）+ -ature → 亲手画下、认作己出的那道记号",
      "中世纪拉丁语 signatura（盖印），来自 signare（标记）← signum（记号）",
      "a person's name written by themselves; a distinctive mark",
      "the mark one draws to own a thing as one's own – 亲手画下、用以认领的那道记号",
      "他在末尾落下自己那道熟手的笔迹，认作己出",
      ["签名", "签字", "标志性特征"],
      ["Put your signature at the bottom.", "The dish is the chef's signature."],
      [], [],
      ["significance", "significant"],
      ["签名/签字：亲手画下用以认领的记号", "标志性特征：一眼就认得出是谁的那个标记"],
      "sign（记号）+ -ature → 亲手画下认作己出的记号"),
    W("significance", "signum", "noun", "/sɪɡˈnɪfɪkəns/",
      "signi（记号）+ fic（做）+ -ance → 做下记号的缘由 → 意义、分量",
      "拉丁语 significantia（含意），来自 significare（示意）← signum＋facere",
      "the meaning of something; its importance",
      "why the mark was made there in the first place – 当初为什么在那儿划下记号",
      "那道刻痕反复被人提起，才显出当初为何划它",
      ["意义", "重要性"],
      ["The date has special significance.", "They stressed the significance of the find."],
      ["meaning", "importance"], ["triviality"],
      ["significant", "signature"],
      ["意义：做下这记号的缘由", "重要性：这缘由分量有多重"],
      "signi（记号）+ fic（做）→ 划下记号的缘由"),
    W("significant", "signum", "adjective", "/sɪɡˈnɪfɪkənt/",
      "signi（记号）+ fic（做）+ -ant → 值得划记号的 → 重要、显著",
      "拉丁语 significans，significare 的现在分词",
      "large or important enough to be noticed",
      "worth putting a mark against – 够得上被划一道记号的",
      "满页里只有那一处被划了记号，看的人都停在那儿",
      ["重要的", "显著的", "有意义的"],
      ["There was a significant rise in costs.", "It is a significant step forward."],
      ["notable", "considerable"], ["negligible"],
      ["significance", "signature"],
      ["重要的/显著的：够得上被划一道记号的", "有意义的：这记号背后有缘由可讲"],
      "signi（记号）+ fic（做）→ 值得划下记号的"),
]

# ================= stringere（拉紧）=================
words += [
    W("strict", "stringere", "adjective", "/strɪkt/",
      "strictus（拉紧的）→ 绷到不留余地 → 严格",
      "拉丁语 strictus（拉紧的），stringere（拉紧）的过去分词",
      "demanding exact obedience; allowing no exception",
      "drawn so tight that no slack is left – 绷到一丝松都不留",
      "绳子拉到最紧，连一点回弹的余地都没有",
      ["严格的", "严厉的"],
      ["The school has strict rules.", "He is strict about deadlines."],
      ["rigorous", "stern"], ["lenient"],
      ["restrict", "district"],
      ["严格的/严厉的：绷到不留一丝余地"],
      "strictus（拉紧的）→ 绷到不留余地"),
    W("restrict", "stringere", "verb", "/rɪˈstrɪkt/",
      "re-（往回）+ strict（拉紧）→ 往回收紧 → 把范围缩小",
      "拉丁语 restrictus，restringere（拉回束紧）的过去分词 ← re＋stringere",
      "to keep something within limits; to reduce what is allowed",
      "pulling the cord back so the circle grows smaller – 绳往回收，能动的圈越缩越小",
      "绳往回一收，能走动的那圈跟着小了一半",
      ["限制", "约束"],
      ["They restricted access to the site.", "Her diet restricts salt."],
      ["limit", "confine"], ["expand", "permit"],
      ["strict", "district"],
      ["限制/约束：往回收紧、把可动范围缩小"],
      "re-（往回）+ strict（拉紧）→ 往回收紧范围"),
    W("district", "stringere", "noun", "/ˈdɪstrɪkt/",
      "di-（分开）+ strict（拉紧）→ 用界线圈紧的一块 → 辖区",
      "中世纪拉丁语 districtus（管辖范围），来自 distringere ← dis＋stringere",
      "an area of a town or country, often an official division",
      "the patch a boundary has been drawn tight around – 被界线圈紧的那一块地面",
      "界线一圈拉起来，圈内归一处管",
      ["地区", "行政区"],
      ["She grew up in the old district.", "The school district covers three towns."],
      ["region", "zone"], [],
      ["strict", "restrict"],
      ["地区/行政区：被界线圈紧、归一处管的那块地面"],
      "di-（分开）+ strict（拉紧）→ 界线圈紧的一块"),
]

# ================= 组装 =================
# 本批不新建词根/概念/语义域，全部补进已建模的六个根。
# ---- 生成期自检：review.py check 不查 Q12，合并后 validate.py 才查 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"

assert len(words) == 26, len(words)
assert len({w["id"] for w in words}) == 26, "词条 id 有重复"

OUT.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=2) + "\n",
               encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words，全部补进已建模词根，无新根")
