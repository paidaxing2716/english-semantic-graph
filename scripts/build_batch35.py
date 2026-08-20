#!/usr/bin/env python3
"""Generate batch35: four new families plus existing-root additions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch35.json"

families = [
    {
        "root": {"id":"firmare","root":"firmare","variants":["firm"],"origin":"拉丁语 firmare（使坚固、使稳固），来自 firmus（坚固的）","core_concept":"to make steady and dependable / 把东西弄到稳固可靠、不会动摇","core_image":"一根立柱被夯实进土里，无论怎么推它都纹丝不动","english_definition":"to make firm, strengthen"},
        "concept": {"id":"concept-firmare-steady","concept":"to make firm and dependable","chinese":"使坚固稳固","core_image":"立柱被夯进土里，受推仍纹丝不动","root_ids":["firmare"],"word_ids":[]},
        "domain":"domain-hold",
        "words":[
            ["firm","adjective","/fɜːm/","firm（坚固）→ 牢固不移、确定的","拉丁语 firmus（坚固的、结实的）","steady, resolute, and not easily moved or changed","set so solidly it will not strain or shift – 安放得结实坚固、不松动不移位","一根桩子被深深钉进地面，推上去只是更稳",["坚固的","坚决的","公司的"],["She kept a firm hold on the rope.","The manager gave a firm answer."],["solid","steady"],["unstable"],["affirm","confirm"],["坚固的：质地坚实不松动","坚决的：立场笃定不打折扣","公司：英文重新借回 firm 作营业实体"]],
            ["affirm","verb","/əˈfɜːm/","af-（ad- 靠向）+ firm（坚固）→ 把话坚定地确认下来","拉丁语 affirmare（使确定），来自 ad＋firmare","to state positively that something is true","pressing a claim until it stands solid – 把一句话说到坚硬稳固、坐实为真","某人的表态被重重按下，像盖章一样坐实",["断言","确认","肯定"],["The witness affirmed the account.","She affirmed her support for the plan."],["assert","confirm"],["deny"],["firm","confirm"],["断言/确认：把说法坚定地说到坐实为真"]],
            ["confirm","verb","/kənˈfɜːm/","con-（完全）+ firm（坚固）→ 使原先的话头被完全坐实","拉丁语 confirmare（加强确认），来自 con＋firmare","to show that something is true, certain, or definite","settling a suspicion into a fixed fact – 把尚不确定的事坐实为定局","机票座位号得到第二处核对，原先的犹豫落了地",["证实","确认","批准"],["The test confirmed the diagnosis.","Please confirm your attendance by Friday."],["verify","validate"],["doubt"],["firm","affirm"],["证实/确认：使不确定之事坐实为确定事实"]]
        ]
    },
    {
        "root": {"id":"nuntiare","root":"nuntiare","variants":["nounce","nunti"],"origin":"拉丁语 nuntiare（通告、报信），来自 nuntius（信使、消息）","core_concept":"to carry word / 把消息送达人前、让众人都听到","core_image":"一名信使跑到广场中央，把一则消息高声喊给所有人","english_definition":"to announce, report"},
        "concept": {"id":"concept-nuntiare-word","concept":"to carry and publish a message","chinese":"通告报信","core_image":"信使把消息送到广场中央对众人高声宣告","root_ids":["nuntiare"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ["announce","verb","/əˈnaʊns/","an-（ad- 靠向）+ nounce（通告）→ 把消息正式说到众人面前","拉丁语 annuntiare（宣告），来自 ad＋nuntiare","to make something known publicly and formally","bringing a piece of news to the crowd's attention – 把一则消息正式送达众人面前","主持人上台，向全场公开念出那条新消息",["宣布","宣告","公布"],["The company announced a new product.","They announced the winner last night."],["declare","proclaim"],["conceal"],["denounce","pronounce"],["宣布/公布：把消息正式公开告知众人"]],
            ["denounce","verb","/dɪˈnaʊns/","de-（向下、出）+ nounce（通告）→ 当众公开谴责、斥责","拉丁语 denuntiare（正式告知、谴责）","to publicly condemn or strongly criticize","speaking a public farewell of blame against someone – 当众发布对某人的公开谴责","发言人站在人前，把某种丑行当众指认出来",["谴责","告发","公开指责"],["The mayor denounced the violence.","Critics denounced the new policy."],["condemn","criticize"],["praise"],["announce","pronounce"],["谴责/公开指责：当众批判某种言行"]],
            ["pronounce","verb","/prəˈnaʊns/","pro-（向前）+ nounce（通告）→ 把音从往前送出来正式说清","拉丁语 pronuntiare（宣读出、说出）","to speak a word with its proper sound, or declare officially","pushing a sound out to the front so it is clearly heard – 把音节向前送出、让人听清","舌尖把每个音节推到前面，清清楚楚念出来",["发音","宣布","宣判"],["How do you pronounce this word?","The judge pronounced the sentence."],["enunciate","declare"],["mumble"],["announce","denounce"],["发音：把语音正确地念出来","宣判/宣布：正式说出具有效力的结论"]]
        ]
    },
    {
        "root": {"id":"cors","root":"cors","variants":["cour","cord"],"origin":"拉丁语 cor/cordis（心，也指胸、膛），法语借入时变 cour/courage","core_concept":"the heart and chest as the seat of inner strength / 心与胸膛，内里勇气与热忱的所在","core_image":"胸腔里一团搏动的心，支撑人迎着压力把力量放出去","english_definition":"heart, core, courage"},
        "concept": {"id":"concept-cors-heart","concept":"the heart as the seat of courage","chinese":"心与勇气","core_image":"胸腔中搏动的心支撑人迎着压力发力","root_ids":["cors"],"word_ids":[]},
        "domain":"domain-force",
        "words":[
            ["courage","noun","/ˈkʌrɪdʒ/","cour（心）+ -age → 把心放进胸膛去面对凶险的一种力量","法语 courage，来自 cœur（心）","the ability to face danger or difficulty without giving in","the strength one draws from the heart when pressure mounts – 压力压顶时从心里提出的那股劲","一个人在威胁面前按住心跳，仍朝前迈出一步",["勇气","胆量"],["It took great courage to speak up.","Soldiers fought with courage."],["bravery","nerve"],["timidity"],["encourage","discourage"],["勇气/胆量：面对凶险时内心撑起的力量"]],
            ["encourage","verb","/ɪnˈkʌrɪdʒ/","en-（使进入）+ courage（勇气）→ 使勇气注入人心中","法语 encourager，来自 en＋courage","to give someone confidence or support to do something","pouring courage into another's heart so they dare – 把勇气注进对方心里让他敢去行动","一只手搭上肩，对方心里便多了迈步的底气",["鼓励","激励","支持"],["The coach encouraged the players.","She encouraged me to apply."],["motivate","inspire"],["discourage"],["courage","discourage"],["鼓励/激励：把信心和勇气送入他人心中"]],
            ["discourage","verb","/dɪsˈkʌrɪdʒ/","dis-（除去）+ courage（勇气）→ 把勇气从人心里抽走","法语 décourager，来自 dis＋courage","to make someone lose confidence or willingness","pulling the heart's courage away so one no longer dares – 把心中勇气抽走、让人不敢再试","一连串打击让原本高涨的心气一点点泄掉",["使气馁","阻止","使灰心"],["Don't let failure discourage you.","The price discouraged most buyers."],["dishearten","deter"],["encourage"],["courage","encourage"],["使气馁/使灰心：抽走人行动的勇气"]],
            ["cordial","adjective","/ˈkɔːdiəl/","cord（心）+ -ial → 从心里发出、热诚真挚的","中世纪拉丁语 cordialis（与心有关的），来自 cor","warm and friendly in manner","coming straight from the heart, unguarded and warm – 由心直接流出、真挚热诚","主人握住的双手带有发自内心的热乎劲",["热诚的","亲切的","由衷的"],["The two leaders had a cordial meeting.","He gave us a cordial welcome."],["warm","friendly"],["hostile"],["courage","encourage"],["热诚的/由衷的：从心里直接流出、真挚亲切"]]
        ]
    },
    {
        "root": {"id":"pati","root":"pati","variants":["pat","pass"],"origin":"拉丁语 pati（承受、忍耐），过去分词 passus","core_concept":"to bear, to undergo, to endure / 承受外来作用而不被压垮","core_image":"人背着压到身上的重量，原地稳住、慢慢承受","english_definition":"to suffer, bear, endure"},
        "concept": {"id":"concept-pati-endure","concept":"to bear and endure without breaking","chinese":"承受忍耐","core_image":"人背负压下的重量原地稳住慢慢承受","root_ids":["pati"],"word_ids":[]},
        "domain":"domain-hold",
        "words":[
            ["patient","noun","/ˈpeɪʃnt/","pati（承受）→ 愿意稳稳承受病情或等待而不急躁","拉丁语 patiens（忍耐的、承受的），来自 pati","a person receiving medical care, or someone able to wait calmly","one who bears an affliction steadily without complaint – 愿意稳稳承受病痛或等待而不急躁","病床上的人静静躺着，接受照护、不怨不躁",["病人","有耐心的"],["The nurse checked on each patient.","Be patient with the slow process."],["invalid","tolerant"],["impatient"],["patience","impatient"],["病人：正在承受、接受治疗的人","有耐心的：能稳住等待不焦躁"]],
            ["patience","noun","/ˈpeɪʃns/","pati（承受）+ -ence → 稳稳承受等待与麻烦的能力","拉丁语 patientia（忍耐），来自 pati","the capacity to accept delay or trouble without annoyance","the steady bearing of waiting and hardship without snapping – 面对等待与麻烦仍稳稳不放、不崩裂","一个人排队等了很久，仍平静如初不抱怨",["耐心","忍耐"],["The task requires great patience.","She waited with patience for the news."],["forbearance","perseverance"],["impatience"],["patient","impatient"],["耐心/忍耐：承受等待与麻烦而不急躁崩裂的能力"]],
            ["impatient","adjective","/ɪmˈpeɪʃnt/","im-（不）+ patient（忍耐）→ 不能安心等待、急不可耐","拉丁语 impatientia（不耐烦），来自 in＋pati","unable to wait calmly, or eager to have something happen soon","unwilling to bear delay, wanting it now – 不愿承受片刻等待、立时要到","排队者来回数着步子，恨不能立刻轮到自己",["不耐烦的","急切的"],["He grew impatient with the delays.","Children are impatient for the holiday."],["restless","anxious"],["patient"],["patient","patience"],["不耐烦的/急切的：不能安心等待、急于成事"]],
            ["passion","noun","/ˈpæʃn/","pass（承受）+ -ion → 强烈到使人几乎被卷挟过去的情感","拉丁语 passio（受苦、激烈情感），来自 pati","a very strong feeling, especially love or enthusiasm","an emotion so strong one feels swept or carried by it – 强烈到像被裹挟着走的情感","一个人谈起所爱之事时，眼里近乎着了火",["激情","热情","酷爱"],["She has a passion for music.","The argument was fought with passion."],["enthusiasm","ardor"],["apathy"],["passive","compassion"],["激情/热情：强烈到几乎把人卷走的情感","酷爱：对某事近乎难以自抑的热衷"]],
            ["passive","adjective","/ˈpæsɪv/","pass（承受）+ -ive → 处于承受、被作用一方的","拉丁语 passivus（被动的），来自 pati","showing no active resistance; receiving action","on the receiving end of action without doing – 处于被作用而自身不主动的一方","一个人只是静静承受外力，不去推、不去挡",["消极的","被动的","顺从的"],["He took a passive role in the debate.","The patient remained passive during treatment."],["inactive","submissive"],["active"],["passion","compassion"],["被动的/消极的：处于被作用而不主动推动"]],
            ["compassion","noun","/kəmˈpæʃn/","com-（共同）+ passion（承受）→ 与他人共同承受其苦","法语 compassion，来自拉丁语 com＋pati","sympathetic concern for the suffering of others","bearing another's pain alongside them as if shared – 与他人一同承受对方的苦楚","老人跌倒时，旁人心里也像跟着疼了一下",["同情","怜悯"],["She showed great compassion for the refugees.","Compassion moved the doctor to volunteer."],["sympathy","mercy"],["indifference"],["passion","passive"],["同情/怜悯：与他人的苦难一同承受而产生的关怀"]]
        ]
    }
]

additions = {
    "ced": [
        ["concede","verb","/kənˈsiːd/","con-（完全）+ ced（让出）→ 完全让出、承认对方有理","拉丁语 concedere（让与），来自 con＋cedere","to admit something is true, or give up a claim","stepping fully aside to let the other side pass – 完全退让、把位置让给对方","争执中一方慢慢退后，把原来的立场交出去",["承认","让步","让出"],["She conceded that she was wrong.","The team conceded two goals."],["admit","yield"],["deny"],["process","proceed","precede"],["承认/让步：让出立场、承认对方有理"],"ced（让出）走到完全退让那一步，不再争持"],
        ["precede","verb","/prɪˈsiːd/","pre-（在前）+ ced（行走）→ 走在他人之前","拉丁语 praecedere（走在前面），来自 prae＋cedere","to come before someone or something in time or order","walking out ahead so others follow in sequence – 走在队伍最前面、他人随后","开幕的号角声在前，正戏紧随其后上演",["在…之前","先于"],["A brief speech preceded the ceremony.","The storm was preceded by dark clouds."],["antecede","forerun"],["follow"],["process","proceed","precedent"],["在…之前：时间或次序上先行一步"]],
        ["recede","verb","/rɪˈsiːd/","re-（向后）+ ced（行走）→ 向后退去、退远","拉丁语 recedere（后退），来自 re＋cedere","to move back or appear to move away","walking backward, drawing away from the front – 朝后退行、远离当前","退潮时水面一点点斜着往回缩",["退去","后移","减退"],["The floods slowly receded.","The coastline receded into mist."],["retreat","ebb"],["approach"],["process","proceed","concede"],["退去/减退：向后退行、声势逐渐减弱"]],
        ["precedent","noun","/ˈpresɪdənt/","pre-（在前）+ ced（行走）+ -ent → 走在前、可作先例再对照","拉丁语 praecedens（在先的），来自 praecedere","an earlier event or ruling used as an example for later ones","the earlier case that walks ahead and guides later ones – 走在前头、供后来者参照的先例","存档的旧卷宗摆在前，后来的案子便照着走",["先例","判例"],["The ruling set a legal precedent.","There is no precedent for this decision."],["example","antecedent"],["novelty"],["precede","process","successor"],["先例/判例：走在前、供后来者参照的既有之例"]]
    ],
    "sta": [
        ["constant","adjective","/ˈkɒnstənt/","con-（完全）+ stant（站立）→ 始终站定、不变化的","拉丁语 constans（不变的），来自 con＋stare","not changing; happening all the time","standing always in one fixed position unchanged – 一直站在原处、始终不变","桌上的钟摆按同一节奏不停摆动，从不停歇",["恒定的","持续的","不变的"],["The clock keeps a constant speed.","She lives under constant pressure."],["steady","continuous"],["variable"],["state","stable","instant"],["恒定的/持续的：一直站定不变、不间断"]],
        ["instant","noun","/ˈɪnstənt/","in-（在上）+ stant（站立）→ 紧贴着眼前的当下、正立在当处","拉丁语 instans（正在进行的），来自 instare（立于其上）","a very short moment of time; happening immediately","the point that stands right up against the now – 紧贴在当下这一点上","电光火石间那一瞬，几乎来不及眨眼",["片刻","瞬间","立刻"],["He paused for an instant.","The message reached me in an instant."],["moment","flash"],["eternity"],["constant","instantaneous"],["片刻/瞬间：紧贴现在的极短一瞬","立刻：就在当下发生"]],
        ["instantaneous","adjective","/ˌɪnstənˈteɪniəs/","instant（瞬间）+ -aneous → 发生在转眼之间、同时即至","英语 instantaneous，来自 instant","happening immediately, without delay","taking but the blink of an instant – 眨眼之间即发生、毫不拖延","按下的按钮与亮起的光几乎同时完成",["瞬间的","即时的"],["The site gave instantaneous feedback.","Death was instantaneous."],["immediate","split-second"],["gradual"],["instant","constant"],["瞬间的/即时的：在眨眼之间即发生"]],
        ["stable","adjective","/ˈsteɪbl/","st（站立）+ -able → 能稳稳站住、不会倒下","拉丁语 stabilis（稳固的），来自 stare（站立）","steady and not likely to change or collapse","able to stand steadily without falling – 能安稳站立、不易倾倒","一栋楼的地基打得深，风吹只晃不动",["稳定的","牢固的"],["The patient's condition is stable.","They built on stable ground."],["steady","secure"],["unstable"],["state","constant","establish"],["稳定的/牢固的：能稳立不倒、不易改变"]],
        ["establish","verb","/ɪˈstæblɪʃ/","est-（站）+ -abl- + -ish → 使某物立起来并稳稳站住","拉丁语 stabilire（使稳固），来自 stare","to set up something durable, or prove something as fact","raising something onto solid footing where it stands firm – 把事物立起来使其稳固站定","一块碑被深深埋住竖好，从此站在那里不再倒",["建立","设立","确立"],["They established a new school.","The theory was established by evidence."],["found","form"],["dismantle"],["state","stable","constitution"],["建立/确立：把事物立稳、使其长久站定"]]
    ],
    "fac": [
        ["manufacture","verb","/ˌmænjuˈfæktʃə/","manu-（手）+ fact（做）+ -ure → 原指用手做出，后指量产制造","拉丁语 manufactura（手工制造），来自 manus＋facere","to produce goods in large quantities","making things by hand or machine at scale – 通过手或机器大批产出成品","流水线上工位相接，一件件成品被造出来",["制造","生产"],["The plant manufactures car parts.","They manufacture goods for export."],["produce","fabricate"],["consume"],["efficient","effect","sufficient"],["制造/生产：用手或机器成批做出物品"]],
        ["beneficial","adjective","/ˌbenɪˈfɪʃl/","bene-（好）+ fic（做出）+ -ial → 造出好处的、有利的","拉丁语 beneficialis（有益的），来自 beneficium（恩惠）","producing good or helpful results","making good come forth for someone – 为某人造出好处","一场及时雨洒下，田地因此长势更好",["有益的","有利的"],["Regular exercise is beneficial to health.","The new law is beneficial to farmers."],["advantageous","helpful"],["harmful"],["efficient","effect","sufficient"],["有益的/有利的：能为人带来好处与助益"]]
    ],
    "fin": [
        ["confine","verb","/kənˈfaɪn/","con-（共同）+ fin（界限）→ 把范围限制在共同划定的边界内","拉丁语 confinare（限定边界），来自 con＋finis","to keep within set limits, or restrict a person","holding something inside a fixed boundary line – 把事物限制在划定的界线之内","乱跑的小动物被围栏圈回，出不了那道边",["限制","禁闭","局限于"],["The fire was confined to one room.","Please confine your remarks to the topic."],["restrict","limit"],["release"],["final","finish","define"],["限制/局限于：把范围关在既定边界之内"]],
        ["define","verb","/dɪˈfaɪn/","de-（下、定）+ fin（界限）→ 为事物的边界下定义","拉丁语 definire（定界限），来自 de＋finire","to state the exact meaning or limits of something","setting down the boundary so a thing is clearly delimited – 划下界线把含义确定下来","词典编者用一句话圈出那个词的确切边界",["定义","界定","明确"],["Please define the key terms.","The rules define what is allowed."],["demarcate","specify"],["obscure"],["definite","definition","refine"],["定义/界定：划定精确边界以确定含义"]],
        ["refine","verb","/rɪˈfaɪn/","re-（再次）+ fin（末端、纯净）→ 反复提纯、去除杂质","拉丁语 raffinare（提纯），来自 re＋fin","to purify, or improve by removing unwanted parts","re-passing something to its clean end state, stripping impurity – 反复过一遍把杂质滤净","粗矿在炉中一再炼制，杂质一层层被剔除",["精炼","提纯","改进"],["The company refines crude oil.","They refined the design over months."],["purify","polish"],["corrupt"],["define","definite","final"],["精炼/提纯：反复处理以滤除杂质","改进：去掉粗糙处使其更完善"]]
    ],
    "ferre": [
        ["offer","verb","/ˈɒfə(r)/","of-（ob- 迎面）+ fer（带来）→ 把东西带到面前供人取舍","拉丁语 offerre（呈上），来自 ob＋ferre","to present something for acceptance or rejection, or a deal","bringing a thing up to someone's face to take or refuse – 把物件呈到人前供其接或拒","托盘被端到宾客面前，任他取用或推回",["提供","提出","给予"],["She offered him a cup of tea.","He offered to help with the move."],["present","propose"],["withdraw"],["prefer","refer","transfer"],["提供/提出：把事物呈到面前供人选择"]],
        ["refer","verb","/rɪˈfɜː(r)/","re-（回）+ fer（携带）→ 把目光或话题带回某处","拉丁语 referre（带回、提及），来自 re＋ferre","to direct attention to, or mention as a source","carrying attention back to a source or named thing – 把注意力带回所指之处","读者顺着页码把问题带回那一段原文",["提到","参考","查阅"],["She referred to the report.","The doctor referred him to a specialist."],["cite","mention"],["ignore"],["prefer","infer","transfer"],["提到/参考：把注意力引回某一来源或对象"]],
        ["confer","verb","/kənˈfɜː(r)/","con-（共同）+ fer（携带）→ 共同带着意见来商谈，或把好处授予人","拉丁语 conferre（带到一起、授予）","to award or grant, or to discuss with others","bringing views together around a table, or bestowing worth on someone – 把众人意见带到一起商谈，或把一项荣誉带给人","委员会围坐一处商议，最终把奖项授出",["授予","商讨","给予"],["The board conferred an honorary degree.","They conferred before deciding."],["grant","consult"],["withhold"],["prefer","refer","transfer"],["授予/给予：把荣誉或权利交到人手上","商讨：把众人意见带到一处合计"]],
        ["infer","verb","/ɪnˈfɜː(r)/","in-（入内）+ fer（携带）→ 从材料中把结论带出来","拉丁语 inferre（带入、推断），来自 in＋ferre","to conclude by reasoning from evidence","carrying a conclusion out from the given facts – 从已有材料中推出结论","侦探从一串脚印里推出刚才发生的事",["推断","推论","暗示"],["We can infer the outcome from the data.","I inferred from his tone that he was angry."],["deduce","surmise"],["guess"],["prefer","refer","confer"],["推断/推论：从已有事实中推出结论"]]
    ]
}

roots=[]; concepts=[]; domain_add={}; words=[]
for fam in families:
    root=dict(fam["root"]); root["word_ids"]=[]; roots.append(root)
    concepts.append(fam["concept"])
    domain_add.setdefault(fam["domain"],[]).append(root["id"])
    for item in fam["words"]:
        wid,pos,phon,logic,origin,native,core,image,chinese,examples,syn,ant,related,exp,*rh=item
        w={"id":wid,"word":wid,"pos":pos,"phonetic":phon,"decomposable":"root","root_ids":[root["id"]],"root_logic":logic,"origin":origin,"native_definition":native,"core_concept":core,"core_image":image,"chinese":chinese,"examples":examples,"synonyms":syn,"antonyms":ant,"related":related,"semantic_expansions":exp}
        if rh: w["recall_hint"]=rh[0]
        words.append(w)
for root_id, entries in additions.items():
    for item in entries:
        wid,pos,phon,logic,origin,native,core,image,chinese,examples,syn,ant,related,exp,*rh=item
        w={"id":wid,"word":wid,"pos":pos,"phonetic":phon,"decomposable":"root","root_ids":[root_id],"root_logic":logic,"origin":origin,"native_definition":native,"core_concept":core,"core_image":image,"chinese":chinese,"examples":examples,"synonyms":syn,"antonyms":ant,"related":related,"semantic_expansions":exp}
        if rh: w["recall_hint"]=rh[0]
        words.append(w)

# 4 families: 3+3+4+6 = 16 new-family words + 18 additions = 34
assert len(words)==34, len(words)
assert len(roots)==4
OUT.write_text(json.dumps({"roots":roots,"concepts":concepts,"domain_add":domain_add,"words":words},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"wrote {OUT} with {len(words)} words, {len(roots)} roots")