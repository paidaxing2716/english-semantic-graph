#!/usr/bin/env python3
"""Generate batch32: nine vetted four-word etymological families."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch32.json"

families = [
    {
        "root": {"id":"taillier","root":"taillier","variants":["tail","taille"],"origin":"古法语 taillier（切、裁开），源自晚期拉丁语 taliare","core_concept":"to cut into a measured piece / 按需要切出一块","core_image":"剪刀沿着画好的线落下，把整块布裁成所需的小块","english_definition":"to cut, shape, or portion"},
        "concept": {"id":"concept-taillier-cut","concept":"to cut into a measured piece","chinese":"裁切、分出","core_image":"剪刀沿线把整块材料裁成所需的小块","root_ids":["taillier"],"word_ids":[]},
        "domain":"domain-shape",
        "words":[
            ("detail","noun","/ˈdiːteɪl/","de-（完全）+ taillier（切）→ 从整体中细细切出的部分","古法语 detail：de- + taillier（切开）","a small individual part of a larger whole","a small piece cut out for close attention – 从整体中切出来单独细看的小部分","一幅大图被放大，其中一小角显出细密纹路",["细节","详情","详述"],["The report includes every important detail.","She described the scene in detail."],["particular","specifics"],["overview"],["entail","retail","tailor"],["细节/详情：从整体中切出并单独查看的小部分","详述（动词）：把整体切成小部分逐项说清"]),
            ("entail","verb","/ɪnˈteɪl/","en-（使进入）+ taillier（切、刻）→ 把条件刻进安排里，使其必然随附","古法语 entaillier（刻入）；法律义先指以限定方式安排地产，后泛化为必然包含","to make something necessary or to involve it as a consequence","having a condition cut into an arrangement so it must come with it – 条件被刻进安排，无法单独拿掉","合同边缘刻着一道条件，签下主体也同时带上它",["使必要","牵涉","必然包含"],["The job entails frequent travel.","Repairing the roof will entail considerable expense."],["involve","require"],[],["detail","retail","tailor"],["使必要/必然包含：条件已经刻进安排，接受主体就必须连带接受它","牵涉：某事随主要行动一并被带进来"]),
            ("retail","noun","/ˈriːteɪl/","re-（再次、分回）+ taillier（切）→ 从大宗货物中再切成小份出售","古法语 retaillier（切下一块）；retail 原指零切出售","the sale of goods to the public in small quantities","cutting bulk goods into portions for individual buyers – 把大宗货切成个人能买的小份","一整卷布在柜台上按顾客需要一段段剪下",["零售","零售业","零售的"],["The company sells its products at retail.","Online retail has grown rapidly."],["commerce","selling"],["wholesale"],["detail","entail","tailor"],["零售：把大宗货物分切成面向个人的小份","零售业/零售的：围绕这种分份出售形成的行业或属性"]),
            ("tailor","noun","/ˈteɪlər/","taillier（切、裁）+ 人称后缀 → 按尺寸裁布的人","古法语 tailleur（裁切者），来自 taillier（切）","a person who makes fitted clothes, or to adapt something for a purpose","cutting material to fit one particular body or need – 按特定对象的尺寸裁出合身形状","一双手沿着粉笔线下剪，让布片恰好贴合一个人的尺寸",["裁缝","专门制作","使适合"],["The tailor adjusted the jacket sleeves.","The course is tailored to beginners."],["dressmaker","adapt"],[],["detail","entail","retail"],["裁缝：按人的尺寸裁布者","使适合：像裁衣一样按具体需要改造内容"]),
        ]
    },
    {
        "root":{"id":"sedere","root":"sedere","variants":["sid","sed","sess"],"origin":"拉丁语 sedere（坐）；相关形式 subsidere（坐下、留作后备）","core_concept":"to sit, settle, or remain in position / 坐下并留在一个位置","core_image":"一个人走到指定座位坐下，位置从此稳定下来","english_definition":"to sit, settle, remain"},
        "concept":{"id":"concept-sedere-sit","concept":"to sit and remain in position","chinese":"坐定、驻留","core_image":"人走到指定座位坐下，稳定地留在那里","root_ids":["sedere"],"word_ids":[]},
        "domain":"domain-hold",
        "words":[
            ("president","noun","/ˈprezɪdənt/","pre-（在前）+ sid（坐）+ -ent（人）→ 坐在众人前面主持的人","拉丁语 praesidens，praesidere（坐在前面、主持）的现在分词","the elected head of a republic or the person in charge of an organization","the person seated before a group to preside over it – 坐在众人前面主持事务的人","会议桌前端有一个主位，坐在那里的人主持全场",["总统","主席","会长"],["The president addressed the nation.","She was elected president of the association."],["leader","chairperson"],[],["residence","resident","subsidy"],["总统/主席/会长：都指坐在集体前面主持事务的人，中文按组织层级区分"]),
            ("residence","noun","/ˈrezɪdəns/","re-（留在、回到）+ sid（坐）+ -ence → 稳定坐落并居住的地方","拉丁语 residentia，来自 residere（留下、居住）","the place where someone lives, especially officially","a place where someone settles and remains – 一个人坐定并长期留下的地方","夜里一栋房子的窗户亮起，住户每天都回到这里",["住所","居住","官邸"],["The form asks for your place of residence.","The ambassador returned to the official residence."],["home","dwelling"],[],["president","resident","subsidy"],["住所/官邸：人稳定居住的地点，官邸强调职务身份","居住：在某处坐定并持续留下的状态"]),
            ("resident","noun","/ˈrezɪdənt/","re-（留在）+ sid（坐）+ -ent（人）→ 在一个地方坐定并长期留下的人","拉丁语 residens，residere（留下、居住）的现在分词","a person who lives in a particular place, or staying in a place","someone settled in a particular place – 在某地坐定并长期留下的人","公寓门口的一排信箱写着长期住在这里的人的名字",["居民","住户","居住的"],["Local residents opposed the plan.","She is resident in London."],["inhabitant","occupant"],[],["president","residence","subsidy"],["居民/住户：在某地稳定留下的人","居住的：说明某人或事物固定留在该处"]),
            ("subsidy","noun","/ˈsʌbsədi/","sub-（在后、在下）+ sid（坐）→ 坐在后方待命的后备力量 → 支援款项","拉丁语 subsidium（后备部队、援助），来自 subsidere（坐在后方待命）","money given by a government or organization to support an activity","support kept sitting in reserve behind an activity – 留在后方、需要时托住事情的支援","主力资金快见底时，后方一只储备钱袋被推到桌前",["补贴","津贴","补助金"],["Farmers receive a government subsidy.","The museum depends on public subsidies."],["grant","support"],[],["president","residence","resident"],["补贴/津贴/补助金：都是后方拨出的支援资金，中文按对象和制度区分"]),
        ]
    },
    {
        "root":{"id":"referre","root":"referre","variants":["relat","refer"],"origin":"拉丁语 referre（带回、报告）；过去分词 relatus","core_concept":"to carry something back into connection / 把一件事带回另一件事旁边","core_image":"两张分开的卡片被拿到一起，用一根线连起来比较","english_definition":"to bring back, report, connect"},
        "concept":{"id":"concept-referre-connect","concept":"to bring back into connection","chinese":"带回并关联","core_image":"两张分开的卡片被拿到一起，用线连成一组","root_ids":["referre"],"word_ids":[]},
        "domain":"domain-transfer",
        "words":[
            ("correlate","verb","/ˈkɒrəleɪt/","cor-（共同）+ relate（带入联系）→ 把两项共同带到一条线上比较","现代拉丁语 correlatio：com-（共同）+ relatio（关联）","to show or have a mutual relationship","bringing two changing things onto the same line – 把两个变化项带到一起看它们是否同步","两条数据曲线叠在同一张图上，一起升降",["相关","使相互关联","关联物"],["Income tends to correlate with education.","Researchers correlated the two sets of data."],["associate","connect"],["separate"],["relate","relation","relationship"],["相关/使相互关联：把两项带到同一条线上寻找共同变化","关联物：在这条联系中与另一项对应的事物"]),
            ("relate","verb","/rɪˈleɪt/","re-（带回）+ lat（ferre 的过去分词词干，带）→ 把一件事带回另一件事旁边 → 关联或讲述","拉丁语 relatus，referre（带回、报告）的过去分词","to connect things, tell an account, or understand someone's experience","carrying one thing back beside another – 把一件事带到另一件事旁边形成联系","说话者把过去发生的事一件件带回听众面前",["联系","讲述","理解并认同"],["The study relates diet to health.","She related the whole incident to the police.","Many readers can relate to the character."],["connect","recount"],["disconnect"],["correlate","relation","relationship"],["联系：把两件事带到一起","讲述：把过去的事情带回听者面前","理解并认同：把别人的经历带回自己的经验旁边比较"]),
            ("relation","noun","/rɪˈleɪʃn/","relate（带到一起）+ -ion → 两件事被带到一起后形成的联系","拉丁语 relatio（带回、报告、联系），来自 referre","a connection between people, groups, or things","the connection formed by bringing things together – 事物被带到一起后形成的那条联系","两座分开的岛之间架起一座桥，双方因此相连",["关系","联系","亲属"],["The relation between the two variables is unclear.","Diplomatic relations have improved."],["connection","association"],["separation"],["correlate","relate","relationship"],["关系/联系：事物被带到一起后形成的连接","亲属：由共同血缘把人带到一起的一类关系"]),
            ("relationship","noun","/rɪˈleɪʃnʃɪp/","relation（联系）+ -ship（状态）→ 联系持续存在的状态与方式","英语 relation + -ship，relation 最终来自拉丁语 referre（带回）","the way in which people or things are connected","an ongoing state of connection – 一条联系持续存在并形成固定相处方式","两个人之间的一根线经过长期往来变成稳定的纽带",["关系","人际关系","关联"],["They have a close working relationship.","The chart shows the relationship between cost and quality."],["connection","bond"],["estrangement"],["correlate","relate","relation"],["关系/关联：两方持续相连的方式","人际关系：这种持续连接发生在人与人之间"]),
        ]
    },
    {
        "root":{"id":"prassein","root":"prassein","variants":["pract","prag"],"origin":"希腊语 prassein（做、实行），其形容词 praktikos 表示适合行动的","core_concept":"to do something in actual action / 把想法真正做出来","core_image":"图纸放在一边，双手开始按步骤把零件装成实物","english_definition":"to do, act, put into practice"},
        "concept":{"id":"concept-prassein-do","concept":"to put into actual action","chinese":"实行、实做","core_image":"双手按步骤把图纸上的想法装成实物","root_ids":["prassein"],"word_ids":[]},
        "domain":"domain-make",
        "words":[
            ("practical","adjective","/ˈpræktɪkl/","pract（做）+ -ical（…的）→ 能拿来实际做、能解决现实问题的","希腊语 praktikos（适合行动的），来自 prassein（做）","concerned with real situations and likely to work effectively","suited to being done in the real world – 放到现实中能真正做成的","方案从纸面搬到工作台，工具材料都刚好用得上",["实际的","实用的","实践的"],["We need a practical solution.","The course provides practical experience."],["realistic","useful"],["impractical"],["practically","practise","practitioner"],["实际的/实践的：着眼于真实行动而非纯理论","实用的：放进现实行动后确实能解决问题"]),
            ("practically","adverb","/ˈpræktɪkli/","practical（实际可做的）+ -ly → 从实际操作看；进一步表示几乎已经如此","英语 practical + -ly；practical 最终来自希腊语 prassein（做）","in a realistic way, or almost completely","judged by what happens in actual action – 按真正做起来的结果判断","进度条只剩细细一格，实际看已经等于完成",["实际上","实用地","几乎"],["Practically speaking, the plan is impossible.","The hall was practically empty."],["virtually","realistically"],[],["practical","practise","practitioner"],["实际上/实用地：按现实行动而不是抽象说法判断","几乎：实际效果已经接近完整状态，只差极小一步"]),
            ("practise","verb","/ˈpræktɪs/","pract（做）+ -ise（使、反复进行）→ 反复实际去做以形成能力","中古英语 practisen，来自古法语 practiser，最终源自希腊语 prassein（做）","to do an activity repeatedly to improve, or to work in a profession","doing an action repeatedly until it becomes reliable – 一遍遍实际去做直到熟练","同一段旋律被每天重复弹奏，手指越来越顺",["练习","实行","从事职业"],["She practises the piano every morning.","He practises law in Manchester."],["rehearse","exercise"],["neglect"],["practical","practically","practitioner"],["练习：反复实际去做以提高能力","实行：把原则落实为行动","从事职业：长期实际执行某种专业工作"]),
            ("practitioner","noun","/prækˈtɪʃənər/","practise（实际从事）+ -er（人）→ 长期实际从事某项专业工作的人","英语 practitioner，来自 practise；最终源自希腊语 prassein（做）","a person actively engaged in a profession or skilled practice","a person who regularly carries out a skilled practice – 经常亲手执行专业工作的人","诊室里的人不是只读理论，而是每天亲自处理真实病例",["从业者","执业者","实践者"],["The clinic needs an experienced medical practitioner.","She is a leading practitioner of the method."],["professional","specialist"],[],["practical","practically","practise"],["从业者/执业者：实际执行某种专业工作的人","实践者：把一种方法持续落实为行动的人"]),
        ]
    },
    {
        "root":{"id":"physis","root":"physis","variants":["phys","physic"],"origin":"希腊语 physis（自然、生长出来的本性），来自 phyein（生长）","core_concept":"the nature that grows into being / 自然生长并呈现出的本性","core_image":"种子自己破土长成植株，显出它内在的结构和规律","english_definition":"nature, natural growth, bodily nature"},
        "concept":{"id":"concept-physis-nature","concept":"nature grown into being","chinese":"自然、本性","core_image":"种子破土长成植株，显出内在结构和规律","root_ids":["physis"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ("physical","adjective","/ˈfɪzɪkl/","phys（自然、身体）+ -ical（…的）→ 属于可观察自然或身体实体的","拉丁语 physicalis，来自希腊语 physikos（自然的），源于 physis（自然）","relating to the body, material things, or the laws of nature","belonging to material nature and the body – 属于可触摸的自然实体与身体","手掌碰到石块，能感到它真实的重量和硬度",["身体的","物质的","物理的"],["Regular physical activity improves health.","The device suffered physical damage."],["bodily","material"],["mental"],["physician","physicist","physics"],["身体的：指自然生长的身体实体","物质的：指可触摸和测量的自然实体","物理的：指这些实体遵循的自然规律"]),
            ("physician","noun","/fɪˈzɪʃn/","physic（自然知识、医术）+ -ian（从业者）→ 研究并照料身体自然状态的人","中古英语 fisicien，来自古法语，最终源自希腊语 physis（自然）；中世纪 physic 兼指自然学与医术","a medical doctor, especially one treating illness without surgery","a specialist in the body's natural condition – 诊察身体状态并帮助其恢复的人","医生观察脉搏、呼吸和体温，从身体迹象判断病情",["医师","内科医生"],["The physician examined the patient carefully.","Consult your physician before changing the dose."],["doctor","clinician"],[],["physical","physicist","physics"],["医师：研究并处理身体自然状态的专业人员","内科医生：现代语境中常特指主要用非外科方法治疗的人"]),
            ("physicist","noun","/ˈfɪzɪsɪst/","physics（自然规律之学）+ -ist（研究者）→ 研究物质与能量规律的人","英语 physicist，来自 physics；physics 最终源自希腊语 physis（自然）","a scientist who studies matter, energy, and natural forces","a researcher of the rules governing material nature – 寻找物质世界运行规律的人","实验室里一束光穿过仪器，研究者记录它如何偏转",["物理学家"],["The physicist developed a new model of matter.","Several physicists repeated the experiment."],["scientist","researcher"],[],["physical","physician","physics"],[]),
            ("physics","noun","/ˈfɪzɪks/","phys（自然）+ -ics（学科）→ 研究自然物质、能量与运动规律的学科","希腊语 ta physika（关于自然之事），来自 physis（自然）","the science of matter, energy, motion, and forces","the systematic study of material nature – 系统寻找物质自然如何运行","小球沿斜面滚下，刻度和计时器把运动规律记录下来",["物理学","物理现象"],["She studies physics at university.","The physics of flight is complex."],["science","mechanics"],[],["physical","physician","physicist"],["物理学：系统研究物质与能量的自然规律","物理现象：某件事背后实际运行的那些规律"]),
        ]
    },
    {
        "root":{"id":"passare","root":"passare","variants":["pass","pas"],"origin":"晚期拉丁语 passare（迈步、经过），与拉丁语 passus（步）相关","core_concept":"to take a step and go beyond / 迈步经过并越到另一边","core_image":"一只脚跨过门槛，身体从这一边移动到另一边","english_definition":"to step, pass, go beyond"},
        "concept":{"id":"concept-passare-step","concept":"to step and go beyond","chinese":"迈过、经过","core_image":"一只脚跨过门槛，从这一边移动到另一边","root_ids":["passare"],"word_ids":[]},
        "domain":"domain-transfer",
        "words":[
            ("compass","noun","/ˈkʌmpəs/","com-（共同、环绕）+ pass（步）→ 绕着边界一步步走量 → 圈定范围与定向工具","中古英语 compas，来自古法语 compasser（丈量、绕行），与 passus（步）相关","an instrument showing direction, or the range and limits of something","pacing around a boundary to establish direction and range – 绕着范围走量以确定方向和界限","人在空地绕一圈丈量边界，再用指针确认北方",["指南针","圆规","范围"],["Use a compass to find north.","The issue lies beyond the compass of this study."],["guide","range"],[],["pass","passage","surpass"],["指南针：帮助行路者确定该往哪一步走","圆规：绕中心划定圆形边界","范围：被绕行丈量后圈定的界限"]),
            ("pass","verb","/pæs/","passare（迈步经过）→ 从一边走过界线到另一边","古法语 passer，来自晚期拉丁语 passare（迈步、经过）","to move beyond a point, give something onward, or succeed in a test","moving across a point and onward – 跨过一个位置继续向前","接力棒越过两人之间的界线，被递到下一只手里",["经过","通过","传递"],["We passed the station at noon.","She passed the exam.","Please pass the salt."],["cross","succeed"],["fail"],["compass","passage","surpass"],["经过：身体跨过一个地点","通过：跨过考试设下的标准线","传递：让物品越过人与人之间的界线"]),
            ("passage","noun","/ˈpæsɪdʒ/","pass（经过）+ -age（过程或结果）→ 经过某处的通道、过程或一段文字","古法语 passage，来自 passer（经过）","the act or route of passing, or a section of text","a route or segment through which movement proceeds – 让移动穿过的一段路径","墙中留出一条窄道，人可以从一个房间走到另一个房间",["通道","经过","段落"],["A narrow passage led to the garden.","The passage of time changed the town.","Read the final passage carefully."],["corridor","extract"],[],["compass","pass","surpass"],["通道：供人经过的路径","经过：跨越过程本身","段落：阅读时从头走到尾的一段文字"]),
            ("surpass","verb","/sərˈpæs/","sur-（越过、在上）+ pass（经过）→ 走过对方所在的位置 → 超过","古法语 surpasser：sur-（在上、越过）+ passer（经过）","to do or be better or greater than someone or something","passing beyond another person's level – 跨过对方所处的标线继续向前","两名跑者并排时，其中一人再迈一步越到前面",["超过","胜过","超越"],["Sales surpassed all expectations.","Her latest work surpasses the earlier novel."],["exceed","outdo"],["trail"],["compass","pass","passage"],["超过/超越：跨过原有数量或水平线","胜过：跨过竞争者所在的位置"]),
        ]
    },
    {
        "root":{"id":"historia","root":"historia","variants":["histor","histori"],"origin":"希腊语 historia（调查所得的知识、叙述），来自 histor（知情的见证者）","core_concept":"an inquiry turned into an account / 调查之后形成的叙述记录","core_image":"调查者收集证词和旧物，再按顺序写成一卷记录","english_definition":"inquiry, knowledge from investigation, account"},
        "concept":{"id":"concept-historia-inquiry","concept":"an inquiry turned into an account","chinese":"调查与记述","core_image":"调查者收集证词和旧物，再按顺序写成记录","root_ids":["historia"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ("historian","noun","/hɪˈstɔːriən/","histor(y)（调查记录）+ -ian（从事者）→ 研究并书写过去记录的人","英语 historian，来自 history；最终源自希腊语 historia（调查、叙述）","a person who studies and writes about the past","a person who investigates evidence and builds an account of the past – 查证材料并重建过去叙述的人","书桌上摊着档案、旧信和地图，研究者逐项核对年代",["历史学家","史学工作者"],["The historian examined newly opened archives.","Historians disagree about the cause of the war."],["scholar","researcher"],[],["historic","historical","history"],["历史学家/史学工作者：都指调查证据并组织过去叙述的人，中文按语境正式程度区分"]),
            ("historic","adjective","/hɪˈstɒrɪk/","histor(y)（历史记录）+ -ic → 值得写进历史记录的 → 有历史重大意义的","英语 historic，来自 history；最终源自希腊语 historia","important enough to be remembered in history","important enough to enter the lasting account – 重要到会被写进长期记录","签字笔落下的一刻，大批记者把这一事件记录下来",["有历史意义的","历史性的"],["The leaders signed a historic agreement.","It was a historic victory for the team."],["momentous","landmark"],["insignificant"],["historian","historical","history"],["有历史意义的/历史性的：重要到会被后人持续记述；不是泛指任何过去的事物"]),
            ("historical","adjective","/hɪˈstɒrɪkl/","history（历史记录）+ -ical → 与过去记录或历史研究有关的","英语 historical，来自 history；最终源自希腊语 historia","connected with the study or events of the past","belonging to the evidence and account of the past – 属于过去材料与叙述范围的","博物馆展柜里陈列旧地图，标签注明它来自哪个年代",["历史的","有关历史的","史实的"],["The novel is based on historical events.","We need to examine the historical evidence."],["documented","past"],[],["historian","historic","history"],["历史的/有关历史的：泛指与过去事件或研究有关","史实的：强调叙述能够由历史材料支持；与 historic 的重大意义不同"]),
            ("history","noun","/ˈhɪstri/","historia（调查、叙述）→ 对过去进行调查后形成的记录","希腊语 historia（调查所得的知识、叙述），经拉丁语和古法语进入英语","the study and record of past events, or a person's previous experience","an investigated account of what happened before – 对已经发生之事的查证与记述","一卷时间轴把散落的旧事件按先后顺序连接起来",["历史","历史学","经历"],["She teaches modern European history.","The patient has a history of heart disease."],["past","record"],["future"],["historian","historic","historical"],["历史/历史学：对过去事件的记录与系统研究","经历：某个人或事物过去发生过的事情记录"]),
        ]
    },
    {
        "root":{"id":"elektron","root":"elektron","variants":["electr","electric"],"origin":"希腊语 elektron（琥珀）；琥珀摩擦后能吸引轻物，因而成为电现象名称来源","core_concept":"the attracting force observed in rubbed amber / 摩擦琥珀显出的吸引力","core_image":"一块琥珀在布上摩擦后，把桌面的细小羽毛吸了起来","english_definition":"amber; electric attraction and charge"},
        "concept":{"id":"concept-elektron-charge","concept":"attraction and charge first seen in amber","chinese":"电荷与吸引","core_image":"琥珀在布上摩擦后吸起桌面的细小羽毛","root_ids":["elektron"],"word_ids":[]},
        "domain":"domain-force",
        "words":[
            ("electric","adjective","/ɪˈlektrɪk/","electr（琥珀摩擦产生的电现象）+ -ic → 由电荷驱动或带电的","新拉丁语 electricus（像琥珀一样能吸引），来自希腊语 elektron（琥珀）","using, producing, or charged with electricity","driven by or carrying electric charge – 由电荷推动或自身带有电荷","插头接通后，电流沿导线进入机器让它运转",["电的","电动的","带电的"],["They bought an electric car.","The wire carries an electric current."],["powered","charged"],["manual"],["electrical","electrician","electricity"],["电的/带电的：直接涉及电荷和电流","电动的：以电流作为运转动力"]),
            ("electrical","adjective","/ɪˈlektrɪkl/","electric（电的）+ -al（有关…的）→ 与电力系统、设备或电学有关的","英语 electric + -al；electric 最终来自希腊语 elektron（琥珀）","relating to electricity, especially systems and equipment","connected with systems that carry and use charge – 与传送和使用电流的系统有关","墙内成束导线连接配电箱与各个插座",["电气的","电力的","有关电的"],["The building needs extensive electrical repairs.","She studies electrical engineering."],["electric","technical"],[],["electric","electrician","electricity"],["电气的/电力的：多指完整的供电系统和设备","有关电的：泛指与电现象或电学相关；electric 常直接修饰由电驱动的东西"]),
            ("electrician","noun","/ɪˌlekˈtrɪʃn/","electric（电）+ -ian（专业人员）→ 安装和维修电力线路设备的人","英语 electrician，来自 electric；electric 最终来自希腊语 elektron（琥珀）","a person trained to install and repair electrical systems","a specialist who works directly with systems carrying current – 亲手处理电流线路与设备的人","技术人员打开配电箱，用仪表逐根检查线路",["电工","电气技师"],["Call an electrician to inspect the wiring.","The electrician replaced the damaged cable."],["technician","installer"],[],["electric","electrical","electricity"],["电工/电气技师：都指安装维修电力系统的人，后者更强调专业技术身份"]),
            ("electricity","noun","/ɪˌlekˈtrɪsəti/","electric（电荷作用的）+ -ity（状态）→ 电荷存在、移动所形成的能量和现象","英语 electricity，来自 electric；electricus 原指琥珀摩擦后的吸引性质","a form of energy resulting from charged particles, especially when flowing as current","energy produced by the presence and movement of charge – 电荷存在和移动形成的能量","开关闭合后，电荷沿导线流动，灯丝随即发亮",["电","电力","电学现象"],["The storm cut off the electricity.","Electricity flows through the cable."],["power","current"],[],["electric","electrical","electrician"],["电/电力：可输送并驱动设备的电能","电学现象：电荷静止或移动时表现出的各种作用"]),
        ]
    },
    {
        "root":{"id":"oikonomia","root":"oikonomia","variants":["econom","econ"],"origin":"希腊语 oikonomia：oikos（家、 household）+ nomos（规则、管理）","core_concept":"managing limited resources as a household / 像管一个家一样安排有限资源","core_image":"桌上只有一定的钱粮，管家把它们分配到吃住、工具和储备中","english_definition":"household management; allocation of resources"},
        "concept":{"id":"concept-oikonomia-manage","concept":"to manage limited resources","chinese":"资源管理","core_image":"管家把有限的钱粮分配到日常需要和储备中","root_ids":["oikonomia"],"word_ids":[]},
        "domain":"domain-make",
        "words":[
            ("economic","adjective","/ˌiːkəˈnɒmɪk/","econom（管理资源）+ -ic → 与生产、分配和整体资源体系有关的","法语 économique，来自希腊语 oikonomikos；根源为 oikonomia（家政管理）","relating to the production, distribution, and use of wealth and resources","belonging to the system that organizes resources – 属于整个资源生产和分配体系的","城市地图上，工厂、市场、家庭与资金流被线条连成一个系统",["经济的","经济上的","经济学的"],["The country faces serious economic problems.","Economic growth slowed this year."],["financial","commercial"],[],["economical","economics","economy"],["经济的/经济上的：涉及社会整体资源如何生产和分配","经济学的：涉及研究这套资源体系的学科"]),
            ("economical","adjective","/ˌiːkəˈnɒmɪkl/","econom（管理资源）+ -ical → 会精打细算、不浪费资源的","英语 economical，来自 economic；最终源自希腊语 oikonomia（家政管理）","using money, time, or resources carefully without waste","managing a limited supply with little waste – 把有限资源安排得够用而不浪费","同样一箱燃料，这台机器安排得当，运行时间更长",["节约的","经济实惠的","省耗的"],["This small car is economical to run.","We need a more economical use of water."],["thrifty","efficient"],["wasteful"],["economic","economics","economy"],["节约的/省耗的：管理资源时尽量减少浪费","经济实惠的：花费与所得安排得划算；不同于 economic 的宏观经济含义"]),
            ("economics","noun","/ˌiːkəˈnɒmɪks/","econom（管理资源）+ -ics（学科）→ 研究稀缺资源如何生产、分配和使用的学科","英语 economics，来自 economy；最终源自希腊语 oikonomia（家政管理）","the study of how resources, goods, and services are produced and distributed","the systematic study of allocating limited resources – 系统研究有限资源如何安排","黑板上一边写有限预算，一边画出家庭、企业和政府之间的流动箭头",["经济学","经济状况"],["She studied economics at university.","The economics of the project remain uncertain."],["finance","commerce"],[],["economic","economical","economy"],["经济学：研究资源生产与分配的学科","经济状况（the economics of）：某个项目的成本收益结构"]),
            ("economy","noun","/ɪˈkɒnəmi/","oiko-（家）+ nom-（管理规则）→ 原指管理一个家，后扩大为管理社会资源的整体体系","希腊语 oikonomia（家政管理），由 oikos（家）+ nomos（规则、管理）构成","the system by which a society organizes production and resources, or careful use without waste","an organized household enlarged to society – 把整个社会的资源像一个家一样安排","一个巨大的家庭账本里同时记录生产、交易、收入和支出",["经济","经济体","节约"],["Tourism is vital to the local economy.","We must achieve greater economy in fuel use."],["market","thrift"],["waste"],["economic","economical","economics"],["经济/经济体：社会范围内组织生产和分配资源的整体","节约：回到家政管理本义，谨慎安排有限资源避免浪费"]),
        ]
    },
]

roots=[]; concepts=[]; domain_add={}; words=[]
for fam in families:
    r=dict(fam["root"]); r["word_ids"]=[]; roots.append(r)
    concepts.append(fam["concept"])
    domain_add.setdefault(fam["domain"], []).append(r["id"])
    ids=[x[0] for x in fam["words"]]
    for item in fam["words"]:
        wid,pos,phon,logic,origin,native,core,image,chinese,examples,syn,ant,related,exp=item
        entry = {
            "id":wid,"word":wid,"pos":pos,"phonetic":phon,"decomposable":"root",
            "root_ids":[r["id"]],"root_logic":logic,"origin":origin,
            "native_definition":native,"core_concept":core,"core_image":image,
            "chinese":chinese,"examples":examples,"synonyms":syn,"antonyms":ant,
            "related":related,"semantic_expansions":exp,
        }
        if wid == "passage":
            entry["recall_hint"] = "先抓住 pass 的‘跨过’：它既可以是供移动穿过的一段路径，也可以是时间推进的过程，还可以是阅读时从头走到尾的一段文字。"
        words.append(entry)

assert len(words)==36
OUT.write_text(json.dumps({"roots":roots,"concepts":concepts,"domain_add":domain_add,"words":words}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"wrote {OUT} with {len(words)} words")
