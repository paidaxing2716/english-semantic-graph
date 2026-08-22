#!/usr/bin/env python3
"""Generate batch49: 7 new roots (18 词) —— vetted 清单收尾批。

  praeesse（在前主事）  presence / present / presently
  profiteri（当众声明）  profession / professor
  filum（细线）          profile          ← prof 族最后一处分叉，必须与上一根分开
  sperare（盼成）        prosper / prosperity / prosperous
  quartus（第四）        quart / quarter / quarterly
  sidus（星辰）          consider / considerable / consideration
  instaurare（重立）     restore / storage / store

prof 是 HANDOFF 之外我自己查出的第四个分叉族：
  profession / professor ← profiteri（pro＋fateri 当众承认、公开声明）
  profile               ← 意大利语 profilare ← pro＋filum（沿着线描边）
两者只是都以 pro- 起头，词源不同，故拆成 profiteri 与 filum 两根。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch49.json"


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

# ---------- praeesse（在前主事）----------
families.append({
    "root": {
        "id": "praeesse", "root": "praeesse", "variants": ["pres", "present"],
        "origin": "拉丁语 praeesse（在前、主事），由 prae（在前）＋ esse（是、在）构成；"
                  "分词 praesens 表「正在眼前的」，英语 present 由此",
        "core_concept": "being right here in front, not elsewhere / 人就在眼前这儿，不在别处",
        "core_image": "点名点到的人应了一声，抬头就能看见他站在那儿",
        "english_definition": "to be at hand, be in front",
    },
    "concept": {
        "id": "concept-praeesse-at-hand", "concept": "being right here in front, not elsewhere",
        "chinese": "就在眼前", "core_image": "点名点到的人应了一声，抬头就见他站在那儿",
        "root_ids": ["praeesse"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("present", "praeesse", "adjective", "/ˈpreznt/",
          "prae-（在前）+ sent（在）→ 正在眼前的 → 出席的、当下的；引申为送到眼前之物",
          "拉丁语 praesens（在眼前的），praeesse（在前）的现在分词",
          "in this place now; happening now; a gift given to someone",
          "standing here where one can be seen – 就站在这儿、看得见的那个状态",
          "点到名字，那人在后排应了一声抬起手",
          ["出席的", "现在的", "礼物"],
          ["All the students were present.", "She gave him a birthday present."],
          ["current", "gift"], ["absent"],
          ["presence", "presently"],
          ["出席的：人就在眼前这儿", "现在的：时间上正在眼前的这一段", "礼物：拿到人眼前递过去的那件"],
          "prae-（在前）+ sent（在）→ 正在眼前的"),
        W("presence", "praeesse", "noun", "/ˈprezns/",
          "present（在眼前）+ -ence → 人在此处这件事；引申为身上那股压得住场的气派",
          "拉丁语 praesentia（在场），来自 praesens ← praeesse",
          "the state of being in a place; an impressive manner",
          "the fact that one is here rather than away – 人在此而不在别处这个事实",
          "他一进门，满屋的说话声就低了半度",
          ["出席", "存在", "气度"],
          ["Your presence is required at the meeting.", "She has real stage presence."],
          ["attendance", "bearing"], ["absence"],
          ["present", "presently"],
          ["出席/存在：人或物就在此处这件事", "气度：在场时压得住场面的那股劲"],
          "present（在眼前）+ -ence → 人在此处这件事"),
        W("presently", "praeesse", "adverb", "/ˈprezntli/",
          "present（当下）+ -ly → 就眼下而言；也表「过一会儿就」",
          "英语 presently，来自 present ← 拉丁语 praeesse",
          "at the present time; soon, after a short while",
          "at the point one is standing on, or just past it – 就在所站的这一刻，或刚过这一刻",
          "他说了句稍等，转身进屋，没几步又折回来了",
          ["目前", "不久", "很快"],
          ["He is presently working abroad.", "The doctor will see you presently."],
          ["currently", "soon"], [],
          ["present", "presence"],
          ["目前：就眼下这一刻而言", "不久/很快：刚过眼下这一刻就到"],
          "present（当下）+ -ly → 就眼下这一刻，或刚过这一刻"),
    ],
})

# ---------- profiteri（当众声明）----------
families.append({
    "root": {
        "id": "profiteri", "root": "profiteri", "variants": ["profess", "profe"],
        "origin": "拉丁语 profiteri（公开承认、当众声明），由 pro（在众人前）＋ fateri（承认）构成；"
                  "过去分词 professus。与 profile 的 filum（线）一支毫无关系，勿混",
        "core_concept": "to declare one's standing out loud before all / 当众把自己的名分说出口",
        "core_image": "他站到众人面前开口，把自己认下的那门本事讲明",
        "english_definition": "to declare publicly, avow",
    },
    "concept": {
        "id": "concept-profiteri-avow", "concept": "to declare one's standing out loud before all",
        "chinese": "当众声明", "core_image": "站到众人面前开口，把自己认下的本事讲明",
        "root_ids": ["profiteri"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("profession", "profiteri", "noun", "/prəˈfeʃn/",
          "pro-（众人前）+ fess（承认）+ -ion → 当众声明自己所执的那门业 → 职业",
          "拉丁语 professio（公开声明、所执之业），来自 profiteri",
          "a paid job needing special training; an open declaration",
          "the calling one names aloud as one's own – 当众说出「我干这一行」的那门业",
          "他报出自己那一行，众人便知他受过哪套训练",
          ["职业", "专业", "声明"],
          ["She entered the legal profession.", "He made a profession of loyalty."],
          ["occupation", "declaration"], [],
          ["professor", "profile"],
          ["职业/专业：当众声明所执、需专门训练的那一行", "声明：把立场当众说出口这件事"],
          "pro-（众人前）+ fess（承认）→ 当众说出所执的那门业"),
        W("professor", "profiteri", "noun", "/prəˈfesə(r)/",
          "profess（当众讲明）+ -or（人）→ 在讲堂上当众讲学的人",
          "拉丁语 professor（公开讲授者），来自 profiteri",
          "a teacher of the highest rank at a university",
          "the one who stands up and expounds before all – 站到众人前讲说的那个人",
          "他站上讲台，把那套道理从头讲给满堂人听",
          ["教授"],
          ["The professor published a new study.", "She was made professor at forty."],
          ["lecturer", "academic"], ["student"],
          ["profession", "profile"],
          ["教授：在讲堂上当众讲学、位阶最高的教师"],
          "profess（当众讲明）+ -or → 站到众人前讲说的人"),
    ],
})

# ---------- filum（细线）----------
families.append({
    "root": {
        "id": "filum", "root": "filum", "variants": ["fil", "profil"],
        "origin": "拉丁语 filum（线、丝），意大利语 profilare 是 pro（沿着）＋filare（拉线）"
                  "→「沿轮廓描一条线」，英语 profile 由此；filament、file（成列）同出此支。"
                  "与 profiteri（当众声明）只是都带 pro-，词源无关",
        "core_concept": "a thread drawn along an edge / 沿着边缘拉出的一条线",
        "core_image": "笔尖贴着侧脸的边一路描下去，只留一条轮廓线",
        "english_definition": "thread, line",
    },
    "concept": {
        "id": "concept-filum-thread", "concept": "a thread drawn along an edge",
        "chinese": "沿边描线", "core_image": "笔尖贴着侧脸的边描下去，只留一条轮廓线",
        "root_ids": ["filum"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("profile", "filum", "noun", "/ˈprəʊfaɪl/",
          "pro-（沿着）+ fil（线）+ -e → 沿边描出的那条线 → 侧影；引申为人物概况",
          "意大利语 profilo（侧影、轮廓），来自 profilare ← pro＋filum（线）",
          "a side view of someone's face; a short description of a person",
          "the single line left when an edge is traced – 沿着边描一遍后剩下的那条线",
          "灯打在墙上，只剩一条贴着脸缘的黑边",
          ["侧面", "轮廓", "简介"],
          ["He was photographed in profile.", "Her profile appeared in the magazine."],
          ["outline", "summary"], [],
          ["profession", "professor"],
          ["侧面/轮廓：沿边描出的那条线", "简介：把人的要点勾出一条轮廓"],
          "pro-（沿着）+ fil（线）→ 沿边描出的那条线"),
    ],
})

# ---------- sperare（盼成）----------
families.append({
    "root": {
        "id": "sperare", "root": "sperare", "variants": ["sper", "spair"],
        "origin": "拉丁语 sperare（盼望），spes（希望）；prosperus 本义「合所盼的」"
                  "（pro＋spes），故 prosper 表事情顺着所盼往好处走。desperate（绝望）反用此根",
        "core_concept": "things going the way one hoped / 事情顺着所盼的那样走",
        "core_image": "禾苗一天比一天高，秋后果然收成压弯了车",
        "english_definition": "to hope, to fare well",
    },
    "concept": {
        "id": "concept-sperare-thrive", "concept": "things going the way one hoped",
        "chinese": "顺所盼而成", "core_image": "禾苗一天比一天高，秋后收成压弯了车",
        "root_ids": ["sperare"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("prosper", "sperare", "verb", "/ˈprɒspə(r)/",
          "pro-（合乎）+ sper（所盼）→ 事情合着所盼往好处走 → 兴旺",
          "拉丁语 prosperare（使顺利），来自 prosperus（合所盼的）← pro＋spes（希望）",
          "to succeed and do well, especially financially",
          "moving along just as one had hoped it would – 一路照着所盼的样子往前走",
          "铺子头一年只两三个客，第三年桌子摆到了门外",
          ["兴旺", "繁荣", "成功"],
          ["The business prospered under her care.", "Few crops prosper in dry soil."],
          ["thrive", "flourish"], ["fail", "decline"],
          ["prosperity", "prosperous"],
          ["兴旺/繁荣/成功：事情顺着所盼一路往好处走"],
          "pro-（合乎）+ sper（所盼）→ 照所盼的样子走下去"),
        W("prosperity", "sperare", "noun", "/prɒˈsperəti/",
          "prosper（兴旺）+ -ity → 兴旺这个状态 → 繁荣、富足",
          "拉丁语 prosperitas（顺利、昌盛），来自 prosperus",
          "the state of being successful and having plenty of money",
          "the condition of things having gone as hoped – 事情已照所盼走成的那个局面",
          "满仓的粮堆到梁下，院里车马进出不断",
          ["繁荣", "富足", "兴旺"],
          ["The country enjoyed years of prosperity.", "They shared in the town's prosperity."],
          ["wealth", "affluence"], ["poverty"],
          ["prosper", "prosperous"],
          ["繁荣/富足/兴旺：事情已照所盼走成的那个局面"],
          "prosper（兴旺）+ -ity → 已照所盼走成的局面"),
        W("prosperous", "sperare", "adjective", "/ˈprɒspərəs/",
          "prosper（兴旺）+ -ous（…的）→ 正处在兴旺里的",
          "拉丁语 prosperus（顺利的、合所盼的），来自 pro＋spes",
          "successful and having plenty of money",
          "standing in the state that hope aimed at – 正站在所盼的那个局面里",
          "他家门前石阶新换过，仓房也添了一间",
          ["繁荣的", "富裕的", "成功的"],
          ["It is a prosperous farming region.", "He came from a prosperous family."],
          ["wealthy", "thriving"], ["poor"],
          ["prosper", "prosperity"],
          ["繁荣的/富裕的/成功的：正处在所盼那个局面里的"],
          "prosper（兴旺）+ -ous → 正处在所盼局面里的"),
    ],
})

# ---------- quartus（第四）----------
families.append({
    "root": {
        "id": "quartus", "root": "quartus", "variants": ["quart", "quar"],
        "origin": "拉丁语 quartus（第四的），来自 quattuor（四）；"
                  "quarta pars（第四份）即四分之一，英语 quart/quarter 由此",
        "core_concept": "one of four equal parts / 均分成四份里的一份",
        "core_image": "一张饼横竖各切一刀，正好四块，取走其中一块",
        "english_definition": "fourth, a quarter",
    },
    "concept": {
        "id": "concept-quartus-fourth", "concept": "one of four equal parts",
        "chinese": "四分之一", "core_image": "饼横竖各切一刀成四块，取走其中一块",
        "root_ids": ["quartus"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("quarter", "quartus", "noun", "/ˈkwɔːtə(r)/",
          "quart（第四）+ -er → 四份中的一份；引申为一年的四分之一、城中一区",
          "古法语 quartier，来自拉丁语 quartarius（四分之一）← quartus",
          "one of four equal parts; three months of a year; a district of a town",
          "the single piece left when a whole is cut in four – 整体切成四块后取的那一块",
          "横竖各一刀，取走其中一块，手里正好是整张的一份",
          ["四分之一", "季度", "地区"],
          ["Cut the apple into quarters.", "Sales rose in the final quarter."],
          ["fourth", "district"], ["whole"],
          ["quart", "quarterly"],
          ["四分之一：整体分四份后的一份", "季度：一年切成四份后的一份", "地区：城中划出的那一块"],
          "quart（第四）+ -er → 整体切四块后的那一块"),
        W("quart", "quartus", "noun", "/kwɔːt/",
          "quartus（第四）→ 一加仑的四分之一，作容量单位",
          "古法语 quarte，来自拉丁语 quarta（第四份）← quartus",
          "a unit of liquid measure equal to a quarter of a gallon",
          "the measure that is one of four in a gallon – 一加仑分作四份中的一份",
          "壶里的奶倒满四回，正好把大桶灌平",
          ["夸脱"],
          ["Add a quart of milk to the pan.", "The recipe calls for two quarts of water."],
          ["measure", "litre"], [],
          ["quarter", "quarterly"],
          ["夸脱：等于一加仑四分之一的容量单位"],
          "quartus（第四）→ 一加仑的四分之一"),
        W("quarterly", "quartus", "adjective", "/ˈkwɔːtəli/",
          "quarter（季度）+ -ly（每…的）→ 每季一次的",
          "英语 quarterly，来自 quarter ← 拉丁语 quartus",
          "happening or produced once every three months",
          "coming round once in each of the four parts of a year – 一年四份里各来一回",
          "账本一年结四回，每回隔三个月",
          ["季度的", "每季一次的"],
          ["The company files quarterly reports.", "She receives a quarterly payment."],
          ["periodic", "seasonal"], [],
          ["quarter", "quart"],
          ["季度的/每季一次的：一年四份里各来一回"],
          "quarter（季度）+ -ly → 一年四份里各来一回"),
    ],
})

# ---------- sidus（星辰）----------
families.append({
    "root": {
        "id": "sidus", "root": "sidus", "variants": ["sider", "sid"],
        "origin": "拉丁语 sidus（属格 sideris：星、星座）；considerare 本义是「细看星象」"
                  "（con＋sidus），古人观星定吉凶，故引申为反复审量。desire 亦出此支",
        "core_concept": "to study the stars closely before deciding / 定夺之前先把星象细看一遍",
        "core_image": "夜里抬头把星位一颗颗对过，才决定明天动不动身",
        "english_definition": "star, constellation",
    },
    "concept": {
        "id": "concept-sidus-study-stars", "concept": "to study the stars closely before deciding",
        "chinese": "观星审量", "core_image": "夜里把星位一颗颗对过，才决定明天动不动身",
        "root_ids": ["sidus"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("consider", "sidus", "verb", "/kənˈsɪdə(r)/",
          "con-（仔细）+ sider（星象）→ 像看星象那样反复审量 → 考虑；引申为认为",
          "拉丁语 considerare（细察星象、审量），来自 con＋sidus（星）",
          "to think about something carefully; to regard in a certain way",
          "going over the signs one by one before settling – 定夺前把各处一一对过",
          "他抬头把满天的星位挨个对过，才开口说话",
          ["考虑", "认为", "顾及"],
          ["Please consider my proposal.", "She is considered an expert."],
          ["ponder", "regard"], ["ignore"],
          ["considerable", "consideration"],
          ["考虑/顾及：像对星位那样一一审量", "认为：审量之后得出的看法"],
          "con-（仔细）+ sider（星象）→ 像看星象那样反复审量"),
        W("considerable", "sidus", "adjective", "/kənˈsɪdərəbl/",
          "consider（审量）+ -able（值得…的）→ 值得专门审量的 → 相当大的",
          "中世纪拉丁语 considerabilis（值得注意的），来自 considerare",
          "great in amount, extent, or importance",
          "big enough to be worth going over carefully – 大到值得专门拿来审量一遍",
          "报上来的数目不小，掌事的把册子翻了两遍",
          ["相当大的", "可观的", "重要的"],
          ["They spent a considerable sum.", "She has considerable influence here."],
          ["substantial", "sizeable"], ["negligible", "slight"],
          ["consider", "consideration"],
          ["相当大的/可观的：大到值得专门审量一遍", "重要的：因分量重而须审量"],
          "consider（审量）+ -able → 大到值得专门审量"),
        W("consideration", "sidus", "noun", "/kənˌsɪdəˈreɪʃn/",
          "consider（审量）+ -ation → 审量这件事；也指审量时须顾到的那一项、体谅",
          "拉丁语 consideratio（细察、审量），来自 considerare",
          "careful thought; a factor to be taken into account; thoughtfulness",
          "the going-over itself, and each thing weighed in it – 审量这件事本身，及其中每一项须顾到的",
          "他把册子摊在灯下，一条条对过去，末了还问了句家里方便不方便",
          ["考虑", "考虑因素", "体谅"],
          ["The plan is under consideration.", "He showed great consideration for others."],
          ["deliberation", "thoughtfulness"], ["disregard"],
          ["consider", "considerable"],
          ["考虑：审量这件事本身", "考虑因素：审量时须顾到的那一项", "体谅：顾到旁人处境的那份心"],
          "consider（审量）+ -ation → 审量这件事及所顾各项"),
    ],
})

# ---------- instaurare（重立）----------
families.append({
    "root": {
        "id": "instaurare", "root": "instaurare", "variants": ["stor", "staur"],
        "origin": "拉丁语 instaurare（重新立起、复原、备置），经古法语 estorer 入英语；"
                  "restore 是 re-＋staurare（再立起），store 本义是「备置存下的物资」",
        "core_concept": "to set a thing up again and keep it ready / 重新立好，并存着备用",
        "core_image": "倒下的架子重新扶起立稳，东西一件件搬回架上码好",
        "english_definition": "to set up again, renew, lay in store",
    },
    "concept": {
        "id": "concept-instaurare-set-up-again", "concept": "to set a thing up again and keep it ready",
        "chinese": "重立备存", "core_image": "倒下的架子扶起立稳，东西一件件搬回码好",
        "root_ids": ["instaurare"], "word_ids": [],
    },
    "domain": "domain-make",
    "words": [
        W("restore", "instaurare", "verb", "/rɪˈstɔː(r)/",
          "re-（再）+ stor（立起）→ 把倒下的重新立回原样 → 修复、恢复",
          "古法语 restorer，来自拉丁语 restaurare（重新立起）← re＋staurare",
          "to bring something back to its former state; to give back",
          "putting a thing back up as it stood before – 把它照原先那样重新立回去",
          "散架的柜子一块块拼回去，扶正后又能立稳",
          ["修复", "恢复", "归还"],
          ["They restored the old church.", "Power was restored within the hour."],
          ["repair", "reinstate"], ["damage", "destroy"],
          ["store", "storage"],
          ["修复/恢复：把它照原先那样重新立回去", "归还：把原属他人之物放回原处"],
          "re-（再）+ stor（立起）→ 照原样重新立回去"),
        W("store", "instaurare", "noun / verb", "/stɔː(r)/",
          "instaurare（备置）→ 备下存着的物资 → 储备；存放之处即店铺",
          "古法语 estor（储备、供给），来自 instaurare（备置、重立）",
          "a supply kept for future use; a shop; to keep for later",
          "what is laid in and kept standing ready – 备下来、一直搁着待用的那批东西",
          "米袋一层层码到墙根，够撑过整个冬天",
          ["储存", "商店", "储备"],
          ["Store the grain in a dry place.", "She works at a grocery store."],
          ["stock", "shop"], ["discard"],
          ["restore", "storage"],
          ["储存/储备：备下搁着待用的那批东西", "商店：存放货物待售的那个处所"],
          "instaurare（备置）→ 备下待用之物；存物之处即店"),
        W("storage", "instaurare", "noun", "/ˈstɔːrɪdʒ/",
          "store（备存）+ -age → 存放这件事，及存放的地方与费用",
          "英语 storage，来自 store ← 拉丁语 instaurare",
          "the keeping of things until needed; space for this",
          "the keeping-in-readiness, and the room it takes – 备着待用这件事，及所占的地方",
          "阁楼腾出半间，箱子摞起来到房梁",
          ["储存", "存放", "储藏空间"],
          ["We put the boxes into storage.", "The phone has 128GB of storage."],
          ["stockpile", "warehousing"], [],
          ["store", "restore"],
          ["储存/存放：备着待用这件事", "储藏空间：为此腾出的那块地方"],
          "store（备存）+ -age → 备着待用这件事及其处所"),
    ],
})

# ================= 组装 =================
words = []
for fam in families:
    words.extend(fam["words"])

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

assert len(words) == 18, len(words)
assert len(roots) == 7, len(roots)
assert len({r["id"] for r in roots}) == 7, "新词根 id 有重复"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words, {len(roots)} new roots")
