#!/usr/bin/env python3
"""Generate batch34: eight new three-to-four-word families plus five existing-root additions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch34.json"

families = [
    {
        "root": {"id":"notare","root":"notare","variants":["not"],"origin":"拉丁语 notare（做记号、标注），来自 nota（记号、符号）","core_concept":"to mark something so it stands out / 给东西做记号让它突出","core_image":"一只手在一件物品上画下记号，使它从同类中被认出来","english_definition":"to mark, note"},
        "concept": {"id":"concept-notare-mark","concept":"to make a mark so something stands out","chinese":"做记号标注","core_image":"物品被画上记号而从同类中被认出","root_ids":["notare"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ["notable","adjective","/ˈnəʊtəbl/","not（做记号）+ -able → 值得被单独做记号记下的","拉丁语 notabilis（值得注意的），来自 notare（做记号）","worthy of attention or being remembered","marked out enough to be worth special notice – 被特别标注出来、值得关注的","人群中一个身影被光标单独圈出，让人记住",["值得注意的","显著的","著名的"],["The meeting produced a notable breakthrough.","She is a notable figure in the field."],["remarkable","prominent"],["ordinary"],["notify","notion","notorious"],["值得注意的/显著的：重要到值得单独做记号","著名的：因突出而被众人记住"]],
            ["notify","verb","/ˈnəʊtɪfaɪ/","not（记号）+ -ify（使）→ 把一个记号/消息送到某人面前让他知道","晚期拉丁语 notificare（使知道），来自 notare＋facere","to formally tell someone about something","bringing a marked message to someone so it becomes known – 把做了记号的信息送到某人眼前","一封盖着红印章、写着明确消息的信被递到收件人手上",["通知","告知"],["Please notify us of any change of address.","The system notifies users of updates."],["inform","alert"],["conceal"],["notable","notion","notorious"],["通知/告知：把信息正式送到某人面前使其知晓"]],
            ["notion","noun","/ˈnəʊʃn/","not（记号）+ -ion → 心中形成的记号，即一个想法或概念","拉丁语 notio（认识、概念），来自 notus（知道的）","an idea, belief, or vague understanding","a mark formed in the mind that stands for an idea – 在脑中成形的、代表某个想法的记号","一个念头像发光的标签在脑海里亮起",["概念","观念","想法"],["She rejected the notion of fate.","I have no notion of what he means."],["idea","belief"],["reality"],["notable","notify","notorious"],["概念/观念：心中代表某种理解而成立的记号","想法：脑中浮现的、尚未成形的认识"]],
            ["notorious","adjective","/nəʊˈtɔːriəs/","not（记号）+ -orious → 被广泛做了记号、名声传开的（多带贬义）","中世纪拉丁语 notorius（尽人皆知的），来自 notus（被知道的）","famous for something bad","marked so widely that everyone knows the name – 被处处标注、名声尽人皆知","一栋建筑的名字反复出现在负面报道的标题上",["臭名昭著的","声名狼藉的"],["The city is notorious for traffic jams.","He is a notorious liar."],["infamous","ill-famed"],["respected"],["notable","notify","notion"],["臭名昭著的：因负面事情名声广为人知"]]
        ]
    },
    {
        "root": {"id":"operari","root":"operari","variants":["oper"],"origin":"拉丁语 operari（劳作、从事工作），来自 opus（工作、作品）","core_concept":"to work, to put effort into function / 让各部分投入运作","core_image":"一双手把部件组合起来并推动，整台系统开始产出结果","english_definition":"to work, function, labor"},
        "concept": {"id":"concept-operari-work","concept":"to work / systems turned to produce a result","chinese":"运作劳作","core_image":"部件被组装并推动，系统开始产出结果","root_ids":["operari"],"word_ids":[]},
        "domain":"domain-make",
        "words":[
            ["operate","verb","/ˈɒpəreɪt/","oper（工作）+ -ate → 让机器或组织进入工作状态","拉丁语 operatus，来自 operari（劳作、工作）","to control a machine, run a system, or be in working condition","bringing parts together so a whole begins producing work – 让各部分配合开始产出结果","驾驶舱里的手推动手柄，整台装置随之启动",["操作","运转","经营"],["She operates the crane safely.","The hospital operates a 24-hour clinic."],["run","control"],["stop"],["operation","operational"],["操作：控制机器使其按规程工作","运转/经营：系统或组织持续发挥功能"]],
            ["operation","noun","/ˌɒpəˈreɪʃn/","oper（工作）+ -ation → 使系统工作的过程、活动或手术","拉丁语 operatio（劳作、活动），来自 operari","the process of working, an organized action, or a medical procedure","getting parts to cooperate and produce, including the body during surgery – 让部件配合产出结果的一次过程","一套流程启动，从投入逐步走到产出",["操作","运作","手术"],["The new line is now in operation.","The patient was prepared for operation."],["procedure","function"],["malfunction"],["operate","operational"],["操作/运作：系统投入工作的过程","手术：医生在病人身体上进行的专门操作"]],
            ["operational","adjective","/ˌɒpəˈreɪʃnəl/","operation（运作）+ -al → 能够执行作业的，或与实际运作有关的","英语 operational，来自 operation","working and ready to be used, or relating to practical functioning","able to be put to work now – 此刻就能投入工作的","指示灯亮起，表示整套系统已就绪可运转",["可操作的","运行中的","作战的"],["The plant is fully operational again.","We need an operational plan for the launch."],["functional","working"],["inoperative"],["operate","operation"],["可操作的/运行中的：系统当前能正常执行任务","实际运作的：与执行层面的具体工作有关"]]
        ]
    },
    {
        "root": {"id":"dignus","root":"dignus","variants":["dign"],"origin":"拉丁语 dignus（值得的、配得上的），dignitas（尊严、地位）","core_concept":"to be worthy of respect / 一件事或一个人够得上尊重","core_image":"一杆天平，一端是一张面孔或一份成就，另一端放着配得上的荣誉","english_definition":"worthy, deserving"},
        "concept": {"id":"concept-dignus-worthy","concept":"worthy of respect","chinese":"配得上尊重","core_image":"天平一端是成就，一端放着配得上的荣誉","root_ids":["dignus"],"word_ids":[]},
        "domain":"domain-force",
        "words":[
            ["dignity","noun","/ˈdɪɡnəti/","dign（值得）+ -ity（状态）→ 值得尊重并把持住的自身价值","拉丁语 dignitas（尊严、地位），来自 dignus（值得的）","the state of being worthy of respect, or calm self-respect","the worth that proves one deserves respect – 经得起检验、配得上尊重的那份价值","一个人挺直站立，肩头托着的重量与所得尊重相称",["尊严","高贵","庄重"],["She faced the crowd with dignity.","Every person deserves to be treated with dignity."],["honor","serenity"],["shame"],["indignant","indignation"],["尊严：证明自己值得被尊重的那份价值","庄重：以稳定姿态撑住这份价值"]],
            ["indignant","adjective","/ɪnˈdɪɡnənt/","in-（不、反对）+ dign（配得上）+ -ant → 因觉得受了不相配的对待而愤怒","拉丁语 indignans（愤愤不平的），来自 indignari（认为不配）","angry because of unjust or unworthy treatment","feeling that something is beneath one and thus wrong – 感到被按不配的身价对待而激起愤怒","一个人自认高出所受待遇，胸口腾起不平之气",["愤慨的","义愤的"],["She was indignant at the false accusation.","Citizens grew indignant over the unfair tax."],["resentful","outraged"],["pleased"],["dignity","indignation"],["愤慨的/义愤的：因遭遇不相配、不公正的对待而愤怒"]],
            ["indignation","noun","/ˌɪndɪɡˈneɪʃn/","indignant（愤慨）+ -ation → 因不公或轻视而产生的愤怒情绪","拉丁语 indignatio（愤懑），来自 indignari","anger caused by unworthy or unjust treatment","the flame kindled when one is treated as beneath one's worth – 被按低劣身价对待时腾起的怒火","被轻视者胸口涌起的怒火几乎可见",["愤慨","义愤"],["The unfair dismissal caused general indignation.","He reported the news with indignation."],["resentment","outrage"],["complacency"],["dignity","indignant"],["愤慨/义愤：因受到不相配的轻视或不公而生的强烈不满"]]
        ]
    },
    {
        "root": {"id":"ordinare","root":"ordinare","variants":["ordin","ord"],"origin":"拉丁语 ordinare（排列成序、安排），来自 ordo（次序、行列）","core_concept":"to lay things out in a sequence / 把事物排成前后有别的次序","core_image":"散乱的物品被一个接一个排成纵列，前后位置分明","english_definition":"to arrange in order, set in a row"},
        "concept": {"id":"concept-ordinare-order","concept":"to arrange into an ordered line","chinese":"排列成序","core_image":"散乱物品被排成前后位置分明的纵列","root_ids":["ordinare"],"word_ids":[]},
        "domain":"domain-shape",
        "words":[
            ["ordinary","adjective","/ˈɔːdnri/","ordin（次序）+ -ary（属于…的）→ 依通常次序而来、不越出常规的","拉丁语 ordinarius（按次序的），来自 ordo（次序）","normal and not special in any way","following the usual rank and line, nothing extra – 顺着常规次序、没有超出","一摞日用品按平常位置摆放，没有任何特别标记",["普通的","平常的","平庸的"],["In an ordinary year we plant in spring.","The film turned an ordinary story into something moving."],["common","typical"],["extraordinary"],["coordinate","subordinate"],["普通的/平常的：顺着通常次序、不特别","平庸的：缺少超出常规的突出点"]],
            ["coordinate","verb","/kəʊˈɔːdɪneɪt/","co-（共同）+ ordin（次序）+ -ate → 让多方按共同次序配合行动","晚期拉丁语 coordinare（共同排列），来自 ordinare","to organize different parts so they work together","putting separate pieces into one shared order so they move as one – 把分散部分排进同一次序协同运作","几个团队接到同一张时间表，动作因此合到同一节奏",["协调","配合","使一致"],["She coordinates the volunteers across three sites.","The rescue teams coordinated their efforts."],["organize","harmonize"],["scatter"],["ordinary","subordinate"],["协调/配合：把不同部分排进共同次序","使一致：让各方步调对齐"]],
            ["subordinate","adjective","/səˈbɔːdɪnət/","sub-（在下）+ ordin（次序）→ 排在主序之下、位居从属","拉丁语 subordinatus，来自 subordinare（置于下位）","lower in rank or position, or a person in such a rank","placed under the main order – 被排在主序列之下","一人站在阶梯较下一级，听命于更高位置者的安排",["从属的","次要的","下级"],["The chief delegate delegated tasks to her subordinates.","Safety is subordinate to the deadline in his logic."],["junior","secondary"],["superior"],["ordinary","coordinate"],["从属的/次要的：排在主序之下","下级：职位处于从属序列的人员"]]
        ]
    },
    {
        "root": {"id":"solidus","root":"solidus","variants":["solid"],"origin":"拉丁语 solidus（坚实、密实的，无空隙的整体）","core_concept":"firm and whole, no hollows / 坚实完整、没有空隙","core_image":"一块厚实的材料，用手按压纹丝不动，内部没有空洞","english_definition":"solid, firm, dense"},
        "concept": {"id":"concept-solidus-whole","concept":"firm and without hollows","chinese":"坚实完整","core_image":"无空洞的厚实材料，按压纹丝不动","root_ids":["solidus"],"word_ids":[]},
        "domain":"domain-hold",
        "words":[
            ["solid","adjective","/ˈsɒlɪd/","solid（坚实）→ 质地密实、无空隙，或可靠","拉丁语 solidus（坚实的）","firm, dense, reliable, and without gaps","a body with no hollow inside that will not yield to pressure – 内部无空隙、受压力不塌陷","一块整木被重物压住仍棱角分明，没有变形",["固体的","坚实的","可靠的"],["The table is made of solid oak.","The proposal rests on solid evidence."],["firm","sturdy"],["hollow"],["solidarity","consolidate"],["固体的/坚实的：质地密实无空隙","可靠的：像实心结构一样经得起压力"]],
            ["consolidate","verb","/kənˈsɒlɪdeɪt/","con-（共同）+ solid（坚实）→ 使分散部分凝成一块坚实整体","拉丁语 consolidare（使牢固）：con- + solidare","to combine into a stronger whole or make more secure","pressing separate pieces until they become one solid mass – 让分散部分挤成无空隙的整体","几处松散的土堆被压成一片结实的路基",["巩固","合并","使坚强"],["The firm consolidated several departments.","Sleep helps consolidate memory."],["merge","strengthen"],["divide"],["solid","solidarity"],["合并：把分散部分合成一个坚实整体","巩固：让结构或成果变得更牢固"]],
            ["solidarity","noun","/ˌsɒlɪˈdærəti/","solid（坚实）+ -arity（状态）→ 众人像一块整体那样彼此支撑","法语 solidarité，来自 solidaire（连带的）","unity of feeling and support within a group","a group standing as one dense body where each supports the rest – 大家合成一块整体彼此担当","许多人并肩站成一面墙，一人受力众人都顶住",["团结","相互支持"],["Workers showed solidarity during the strike.","We stand in solidarity with the community."],["unity","togetherness"],["division"],["solid","consolidate"],["团结/相互支持：众人如一体般彼此坚实支撑"]]
        ]
    },
    {
        "root": {"id":"terrere","root":"terrere","variants":["terr"],"origin":"拉丁语 terrere（使惊惧、吓住）","core_concept":"to fill with a numbing fear / 用巨大的恐惧把人震住","core_image":"黑浪朝人涌来，一瞬间呼吸和动作都被镇住","english_definition":"to frighten, terrify"},
        "concept": {"id":"concept-terrere-fear","concept":"to fill with overpowering fear","chinese":"令人惊惧","core_image":"巨大威胁逼近，人被镇住难以动弹","root_ids":["terrere"],"word_ids":[]},
        "domain":"domain-force",
        "words":[
            ["terrible","adjective","/ˈterəbl/","terr（惊惧）+ -ible（可…的）→ 让人感到惊惧的，或程度极严重","拉丁语 terribilis（可怕的），来自 terrere","extremely bad, harmful, or causing great fear","so bad that it overwhelms and frightens – 坏到把人镇住","一场灾难的场面铺满视野，任何抵抗都显得无力",["可怕的","严重的","糟糕的"],["The storm caused terrible damage.","I had a terrible night's sleep."],["awful","appalling"],["excellent"],["terrify","terror"],["可怕的：引发强烈恐惧","严重/糟糕的：坏到接近令人害怕的程度"]],
            ["terrify","verb","/ˈterɪfaɪ/","terr（惊惧）+ -ify（使）→ 使人充满恐惧","法语 terrifier，来自拉丁语 terrificare","to make someone feel intense fear","pouring fear into someone until they freeze – 让恐惧充满一个人直到僵住","黑影从角落逼近，被看者瞬间屏住呼吸",["使恐惧","使惊吓"],["The loud bang terrified the child.","She was terrified of heights."],["frighten","horrify"],["reassure"],["terrible","terror"],["使恐惧/使惊吓：用巨大威胁让人充满恐惧"]],
            ["terror","noun","/ˈterə/","terr（惊惧）+ -or（名词）→ 极端剧烈的恐惧","拉丁语 terror（惊恐），来自 terrere","extreme fear, or violence meant to spread such fear","the frozen state produced by a force too big to face – 面对无法抵挡之物时被镇住的状态","城市突然笼罩在一种让人无法入睡的惊恐中",["恐怖","惊骇","恐怖行为"],["The crowd fled in terror.","The group used terror to control the town."],["dread","panic"],["calm"],["terrible","terrify"],["恐怖/惊骇：极端剧烈的恐惧","恐怖行为：以制造恐惧为手段的暴力"]]
        ]
    },
    {
        "root": {"id":"rumpere","root":"rumpere","variants":["rupt","rum"],"origin":"拉丁语 rumpere（打断、断裂）及其过去分词 ruptus","core_concept":"to break apart suddenly / 使完整的东西猛然断裂","core_image":"一根绷紧的绳索突然从中间断开，两端弹开","english_definition":"to break, burst apart"},
        "concept": {"id":"concept-rumpere-break","concept":"to break apart suddenly","chinese":"猛然断裂","core_image":"绷紧的绳索从中间突然断开","root_ids":["rumpere"],"word_ids":[]},
        "domain":"domain-force",
        "words":[
            ["disrupt","verb","/dɪsˈrʌpt/","dis-（分开、打散）+ rupt（断裂）→ 打断正常运行","拉丁语 disruptus，来自 disrumpere（裂开、打断）","to interrupt or throw something out of its normal course","breaking the continuity of a running system – 把正运行的过程从中间打断","正在亮起的长串灯忽然断掉几盏，节奏被打乱",["扰乱","打断","中断"],["Flights were disrupted by the storm.","The protest disrupted traffic."],["interrupt","disturb"],["maintain"],["disturbance","abrupt","corrupt"],["扰乱/打断：使正常运行从中间断开","中断：使连续性暂时或永久停止"]],
            ["abrupt","adjective","/əˈbrʌpt/","ab-（离开）+ rupt（断裂）→ 像被硬生生掐断、缺乏过渡","拉丁语 abruptus（断裂的），来自 abrumpere（切断）","sudden, unexpected, and lacking smooth transition","cut off sharply without the usual lead-in – 没有过渡就硬生生断掉","一条平整的山路走到底突然断成悬崖边缘",["突然的","生硬的","陡峭的"],["The meeting came to an abrupt end.","His tone was abrupt and cold."],["sudden","brusque"],["gradual"],["disrupt","corrupt"],["突然的/生硬的：像被硬生生断开、缺少过渡","陡峭的：地形如断裂般骤然下降"]],
            ["corrupt","adjective","/kəˈrʌpt/","cor-（完全）+ rupt（断裂）→ 使原本正直的东西整体腐坏变形","拉丁语 corruptus，来自 corrumpere（败坏）","dishonest or morally decayed, or data that has been damaged","breaking down a sound whole, morally or materially – 把一个完好整体从内部败坏","原本明亮的证书被墨渍和篡改弄得形状歪曲",["腐败的","腐化的","损坏的"],["Corrupt officials were removed from office.","The file was corrupt and could not be opened."],["dishonest","decayed"],["honest"],["disrupt","abrupt"],["腐败的/腐化的：整体从内部败坏","损坏的：数据或物品被破坏到无法正常用"]]
        ]
    },
    {
        "root": {"id":"summa","root":"summa","variants":["sum"],"origin":"拉丁语 summa（顶端、总数），来自 summus（最高的）","core_concept":"the topmost point, then the total that tops up a whole / 最高处，也指汇聚成顶点的总和","core_image":"一枚枚更小的量被叠起来，最高处立着一个代表全部的顶端","english_definition":"top, total, sum"},
        "concept": {"id":"concept-summa-total","concept":"the total at the top of a stack","chinese":"总顶合计","core_image":"众多小量叠起，顶端立着代表全部的总量","root_ids":["summa"],"word_ids":[]},
        "domain":"domain-shape",
        "words":[
            ["sum","noun","/sʌm/","sum（总数）→ 若干部分加在一起得到的总量","拉丁语 summa（总数、顶端）","the total amount from adding parts, or an amount of money","the top result reached when all parts are piled together – 各部分相加后处于顶端的那个总值","一叠小账单被整齐相加，顶端得出一个数字",["总和","金额","算术题"],["The sum of the parts equals the whole.","He paid a large sum for the house."],["total","amount"],["difference"],["summarize","summary"],["总和：各部分组成的总量","金额：一笔具体数额的钱"]],
            ["summarize","verb","/ˈsʌməraɪz/","summary（概要）+ -ize（使）→ 把大量内容收拢成一段简短总说","英语 summarize，来自 summary","to state the main points briefly","gathering a long account into a single top-line statement – 把长内容收拢成顶端的简要概括","成堆文字被压成一行要点，整齐排在顶部",["总结","概括"],["Summarize the key findings in two sentences.","The report summarizes five years of data."],["outline","condense"],["expand"],["sum","summary"],["总结/概括：把大量内容收拢成简短的要点"]],
            ["summary","noun","/ˈsʌməri/","sum（总数）+ -mary → 把内容汇总成简短整体","中世纪拉丁语 summarius（概要的），来自 summa（总数）","a brief statement of the main points","the compact total of a longer account – 长内容汇总出的简短总体","一本书的末页浓缩了全部章节的要点",["摘要","概要"],["Each chapter ends with a summary.","She gave a brief summary of the case."],["abstract","digest"],["expansion"],["sum","summarize"],["摘要/概要：把完整内容浓缩成的简要总体"]]
        ]
    }
]

additions = {
    "fin": [
        ["finance","noun","/ˈfaɪnæns/","fin（终结、结清）+ -ance → 与清偿/资金结算有关的事务","中古法语 finance（结算），来自 finer（终结、清账）","the management of money, or money provided for a purpose","the money side of seeing a matter through to its end – 把事项推进到收尾时的资金支撑","一张建造计划下方垫着一层钱物，支撑它进行到完工",["金融","财政","资金"],["She studied finance at university.","The project needs public finance."],["funding","capital"],["bankruptcy"],["final","finish","infinite"],["金融/财政：围绕资金收付与管理的事务","资金：支撑事项完成所需的款项"]],
    ],
    "pars": [
        ["compartment","noun","/kəmˈpɑːtmənt/","com-（共同）+ part（部分）+ -ment → 大空间被划分出的一个部分","法语 compartiment，来自 compartir（分割）","a separate section, often given a specific use","one divided-out pocket inside a larger whole – 大整体中切分出的一块空位","列车长椅上方被隔板分成一个个独立空间",["隔间","车厢","分隔间"],["The fridge has a separate compartment for vegetables.","Her bag has a hidden compartment."],["section","pocket"],["whole"],["part","depart","impart"],["隔间/车厢：大空间中被划分出的独立部分"]],
        ["counterpart","noun","/ˈkaʊntəpɑːt/","counter-（对应、对照）+ part（部分）→ 与某部分相对称的对应部分","英语 counterpart，来自 counter ＋ part","a person or thing that corresponds to another in position or function","the matching part standing opposite across a shared scheme – 在共同结构中与一方成对的另一半","谈判桌两边各坐一人，职位一一对应",["对应的人/物","地位相当者"],["The US secretary met his British counterpart.","This gear is the counterpart of that one."],["equivalent","match"],["contrast"],["part","impart","department"],["对应的人/物：在共同结构中与另一方地位、功能相对的部分"]],
    ],
    "pet": [
        ["perpetual","adjective","/pəˈpetʃuəl/","per-（贯穿）+ pet（追求）+ -ual → 一直向前追着不停，没有终止","拉丁语 perpetuus（连续的），可能与 per＋petere 相关","continuing forever, or seeming to never end","stretching forward without a breaking point – 一路向前不断开","一条线向前延展到望不见尽头的位置",["永恒的","永久的","不断的"],["The clock is driven by a near-perpetual motion.","He complained about the perpetual noise."],["endless","everlasting"],["temporary"],["competition","petition","repetition"],["永恒的/永久的：向前不断开、没有终止","不断的：持续发生而看上去无尽头"]],
    ],
    "jac": [
        ["adjective","noun","/ˈædʒɪktɪv/","ad-（靠向）+ ject（投掷）→ 原意“加靠到名词旁的词”","拉丁语 adjectivum（附加的词），来自 adjicere（添加）","a word that modifies a noun by adding a quality","a word thrown alongside a noun to add description – 投过去依附在名词旁起修饰作用的词","“blue”被放到“sky”旁边，天空的颜色就此明确",["形容词"],["In English, adjectives usually precede the noun.","The adjective modifies the noun."],[],[],["object","subject","reject"],["形容词：投放到名词旁、为其添加描述的词"]],
    ],
    "rect": [
        ["directory","noun","/dəˈrektəri/","direct（指引）+ -ory（场所）→ 用来指引人找到对象的名册或路径组织","中世纪拉丁语 directorium（指引的书册），来自 dirigere（指引）","a listing of names or files used to find things","an organized place that points one toward the sought item – 帮你指向目标所在的编排","大厅里的名册按姓氏排列，一翻就能指向对应房间",["名录","目录","文件夹"],["Please check the directory for the extension.","Save the file into a new directory."],["index","catalogue"],[],["direct","correct","director"],["名录/目录：按规则编排、指引人找到对象的集合","文件夹：计算机中指向并组织文件的位置"]],
    ],
}

roots=[]; concepts=[]; domain_add={}; words=[]
for fam in families:
    root=dict(fam["root"]); root["word_ids"]=[]; roots.append(root)
    concepts.append(fam["concept"])
    domain_add.setdefault(fam["domain"],[]).append(root["id"])
    for item in fam["words"]:
        wid,pos,phon,logic,origin,native,core,image,chinese,examples,syn,ant,related,exp=item
        words.append({"id":wid,"word":wid,"pos":pos,"phonetic":phon,"decomposable":"root","root_ids":[root["id"]],"root_logic":logic,"origin":origin,"native_definition":native,"core_concept":core,"core_image":image,"chinese":chinese,"examples":examples,"synonyms":syn,"antonyms":ant,"related":related,"semantic_expansions":exp})
for root_id, entries in additions.items():
    for item in entries:
        wid,pos,phon,logic,origin,native,core,image,chinese,examples,syn,ant,related,exp=item
        words.append({"id":wid,"word":wid,"pos":pos,"phonetic":phon,"decomposable":"root","root_ids":[root_id],"root_logic":logic,"origin":origin,"native_definition":native,"core_concept":core,"core_image":image,"chinese":chinese,"examples":examples,"synonyms":syn,"antonyms":ant,"related":related,"semantic_expansions":exp})

# 8 families: 4+3+3+3+3+3+3+3 = 25 new-family words + 6 additions = 31
assert len(words)==31, len(words)
assert len(roots)==8
OUT.write_text(json.dumps({"roots":roots,"concepts":concepts,"domain_add":domain_add,"words":words},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"wrote {OUT} with {len(words)} words, {len(roots)} roots")