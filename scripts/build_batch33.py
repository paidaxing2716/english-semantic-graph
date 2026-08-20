#!/usr/bin/env python3
"""Generate batch33: ten new three-word families plus nine existing-family additions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch33.json"

families = [
    {
        "root": {"id":"vocare","root":"vocare","variants":["voc","vok"],"origin":"拉丁语 vocare（呼叫、召唤），来自 vox（声音）","core_concept":"to call out with a voice / 发声呼叫","core_image":"一个人向远处喊出声音，听见的人转身回应","english_definition":"to call, name, summon by voice"},
        "concept": {"id":"concept-vocare-call","concept":"to call out with a voice","chinese":"发声召唤","core_image":"声音越过一段距离，使听见的人转身回应","root_ids":["vocare"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ["advocate","noun","/ˈædvəkət/","ad-（到…旁边）+ voc（呼叫）+ -ate → 被叫到身旁替人发声的人","拉丁语 advocatus，来自 advocare（召来作援助）","a person who publicly supports a cause, or to support it publicly","someone called beside another person to speak in support – 被召到身边替某人发声","一人面对人群陈述理由，身旁的人因此不再独自应对",["倡导者","拥护者","提倡"],["She is a strong advocate for equal access.","The report advocates stricter safety rules."],["supporter","campaigner"],["opponent"],["vocal","vocation"],["倡导者/拥护者：站到某人或某事旁边替其发声的人","提倡：公开发声支持一种主张"]],
            ["vocal","adjective","/ˈvəʊkl/","voc（声音）+ -al（有关…的）→ 与声音有关，或把意见明确说出来的","拉丁语 vocalis（有声音的），来自 vox（声音）","relating to the voice, or expressing opinions openly","using the voice so a position can be heard – 让声音清楚传到别人耳中","原本安静的人走到麦克风前，把立场清楚说出",["声音的","直言不讳的","声乐的"],["The song demands strong vocal control.","Residents were vocal in their opposition."],["outspoken","spoken"],["silent"],["advocate","vocation"],["声音的/声乐的：直接涉及人声及其运用","直言不讳的：把意见发声说出而不保持沉默"]],
            ["vocation","noun","/vəʊˈkeɪʃn/","voc（召唤）+ -ation → 内心或职责发出的召唤，进而成为长期投入的职业","拉丁语 vocatio（召唤），来自 vocare（呼叫）","a strong sense of fitness for a particular career, or that career itself","a line of work that seems to call a person toward it – 某项工作像声音一样不断召人前往","一条工作道路从远处亮起，像持续的呼声引人走过去",["使命感","天职","职业"],["Teaching became her vocation.","He felt a vocation to serve the community."],["calling","profession"],["disinterest"],["advocate","vocal"],["使命感/天职：内心听见某项长期职责的召唤","职业：由这种召唤发展成持续从事的工作"]]
        ]
    },
    {
        "root": {"id":"turba","root":"turba","variants":["turb"],"origin":"拉丁语 turba（拥挤的人群、混乱）及相关 turbo（旋转、旋风）","core_concept":"a mass thrown into turbulent motion / 一团东西被搅得混乱旋动","core_image":"平静的人群忽然互相推挤，中央卷起一个旋涡","english_definition":"crowd, turmoil, turbulent turning"},
        "concept": {"id":"concept-turba-turmoil","concept":"a mass in turbulent motion","chinese":"扰乱旋动","core_image":"原本平静的一团东西被推挤成旋涡","root_ids":["turba"],"word_ids":[]},
        "domain":"domain-force",
        "words":[
            ["disturb","verb","/dɪˈstɜːb/","dis-（分开、打乱）+ turb（混乱）→ 把原有秩序搅散","拉丁语 disturbare：dis- + turbare（使混乱），经古法语进入英语","to interrupt calm, order, or concentration","stirring a settled state into disorder – 把平静稳定的状态搅乱","平整水面被突然拨动，波纹向四周扩散",["打扰","扰乱","使不安"],["Please do not disturb the patients.","The news disturbed her deeply."],["interrupt","unsettle"],["calm"],["disturbance","turbine"],["打扰/扰乱：打断原有的安静或秩序","使不安：把内心的稳定状态搅动起来"]],
            ["disturbance","noun","/dɪˈstɜːbəns/","disturb（搅乱）+ -ance（状态或事件）→ 打破平静后出现的混乱或异常","英语 disturbance，来自 disturb","an interruption of peace or normal conditions","the disorder left after calm has been stirred – 平静被搅动后留下的异常状态","原本整齐的队列出现一处推挤，波动传遍全队",["干扰","骚乱","异常"],["The noise caused a serious disturbance.","Scientists detected a disturbance in the field."],["disruption","disorder"],["stability"],["disturb","turbine"],["干扰：正常过程被外力搅动","骚乱：人群秩序被搅散","异常：稳定系统中出现的扰动"]],
            ["turbine","noun","/ˈtɜːbaɪn/","turb（旋动）+ -ine（装置）→ 被流体推动而持续旋转的机器","法语 turbine，来自拉丁语 turbo（旋风、旋转物）","a machine whose blades rotate when driven by a moving fluid","a wheel turned by a controlled stream like a contained whirl – 流体推动叶片形成受控旋转","水流冲向一圈叶片，中心轴随之快速转动",["涡轮机","叶轮机"],["Steam drives the turbine.","The wind turbine generates electricity."],["rotor","engine"],[],["disturb","disturbance"],["涡轮机/叶轮机：利用水、气或蒸汽的流动推动叶片旋转的装置"]]
        ]
    },
    {
        "root": {"id":"tribuere","root":"tribuere","variants":["tribut","tribu"],"origin":"拉丁语 tribuere（分配、给予），与 tribus（部族、分区）相关","core_concept":"to assign a share to each party / 把一份东西分派给某一方","core_image":"桌上的一堆物品被按名单分成几份，分别推到各人面前","english_definition":"to assign, allot, give a share"},
        "concept": {"id":"concept-tribuere-assign","concept":"to assign a share","chinese":"分派份额","core_image":"一堆资源按名单分成几份并交到各方手中","root_ids":["tribuere"],"word_ids":[]},
        "domain":"domain-transfer",
        "words":[
            ["attribute","verb","/əˈtrɪbjuːt/","at-（向）+ tribut（分派）→ 把原因、性质或作品归到某一方名下","拉丁语 attributus，来自 attribuere（分配给、归于）","to regard something as caused or created by a particular source","assigning a result to one named source – 把结果那一份归到特定来源名下","几条原因卡片最终被放到同一个名字下面",["归因于","把…归属","属性"],["She attributes her success to persistence.","The work is attributed to a local artist."],["ascribe","assign"],["detach"],["contribute","distribute"],["归因于/归属：把结果或作品分派到某个来源名下","属性：被归给某一对象的特征"]],
            ["contribute","verb","/kənˈtrɪbjuːt/","con-（共同）+ tribut（分派给予）→ 每个人把自己的一份交进共同之中","拉丁语 contribuere：con- + tribuere（共同给予）","to give money, effort, ideas, or help toward a shared result","giving one's assigned share into a common pool – 把自己的一份投入共同目标","多人各放一块材料，中央逐渐拼成完整结构",["贡献","捐助","促成"],["Many volunteers contributed their time.","Several factors contributed to the decline."],["donate","add"],["withhold"],["attribute","distribute"],["贡献/捐助：把自己的资源份额交给共同目标","促成：某个因素把自己的一份作用加入最终结果"]],
            ["distribute","verb","/dɪˈstrɪbjuːt/","dis-（分开、向各处）+ tribut（分派）→ 把整体拆成份额送到各方","拉丁语 distribuere：dis- + tribuere（分开分配）","to give or spread portions among people or places","dividing a whole into shares and sending each outward – 把整体分成多份向外送出","一摞资料被逐份递到房间里每个人手中",["分发","分配","分布"],["Workers distributed food to the crowd.","The species is widely distributed."],["allocate","circulate"],["collect"],["attribute","contribute"],["分发/分配：把整体按份额交给不同对象","分布：许多份散到不同地点后形成的状态"]]
        ]
    },
    {
        "root": {"id":"torquere","root":"torquere","variants":["tort","torqu"],"origin":"拉丁语 torquere（扭转、拧）及过去分词 tortus","core_concept":"to twist something out of its line / 把东西拧离原来的直线","core_image":"两只手抓住一根直绳向相反方向拧，使它卷曲变形","english_definition":"to twist, turn, wrench"},
        "concept": {"id":"concept-torquere-twist","concept":"to twist out of line","chinese":"扭转变形","core_image":"一根直绳被两手反向拧成卷曲形状","root_ids":["torquere"],"word_ids":[]},
        "domain":"domain-shape",
        "words":[
            ["distort","verb","/dɪˈstɔːt/","dis-（分离、偏离）+ tort（扭）→ 把原形或原意扭离正确位置","拉丁语 distortus，来自 distorquere（扭向一边）","to twist the shape, sound, facts, or meaning away from accuracy","twisting something away from its true line – 把形状或信息拧离真实轨道","一条笔直网格被拉扯后弯曲，图像随之走样",["扭曲","歪曲","使变形"],["The lens distorted the image.","Do not distort what she said."],["twist","misrepresent"],["clarify"],["retort","torture"],["扭曲/使变形：物体被拧离原形","歪曲：事实或原意被拧离真实含义"]],
            ["retort","verb","/rɪˈtɔːt/","re-（向回）+ tort（扭）→ 把对方的话拧转回去，形成尖锐回应","拉丁语 retortus，来自 retorquere（扭回、投回）","to reply quickly and sharply, or a vessel with a curved neck","turning an attack back toward its source – 把来势迅速扭回发出者方向","一支射来的箭被弯曲挡板弹转回去",["反驳","回嘴","曲颈甑"],["She retorted that the claim was unfair.","The liquid was heated in a glass retort."],["reply","counter"],["agree"],["distort","torture"],["反驳/回嘴：把对方的话锋扭转回去","曲颈甑：蒸馏容器的颈部弯转，使蒸气改向"]],
            ["torture","noun","/ˈtɔːtʃə/","tort（扭）+ -ure → 原指扭曲身体施加痛苦，后泛指极端折磨","晚期拉丁语 tortura（扭曲、折磨），来自 torquere（扭）","the deliberate infliction of severe pain, or extreme suffering","pain produced as if the body or mind were being twisted – 身体或内心像被持续拧紧","绳索被一点点收紧，承受者无法摆脱压力",["酷刑","折磨","使受煎熬"],["The treaty prohibits torture.","The long uncertainty was torture for the family."],["torment","agony"],["comfort"],["distort","retort"],["酷刑：通过强力扭压身体制造剧痛","折磨/使受煎熬：痛苦像持续拧紧一样无法停止"]]
        ]
    },
    {
        "root": {"id":"tolerare","root":"tolerare","variants":["toler","tol"],"origin":"拉丁语 tolerare（承受、忍耐）","core_concept":"to carry a burden without breaking / 扛住负担而不崩溃","core_image":"肩上压着重物的人稳住脚步，继续向前","english_definition":"to bear, endure, sustain"},
        "concept": {"id":"concept-tolerare-bear","concept":"to bear without breaking","chinese":"承受容忍","core_image":"肩负重物的人稳住身体继续前进","root_ids":["tolerare"],"word_ids":[]},
        "domain":"domain-hold",
        "words":[
            ["tolerance","noun","/ˈtɒlərəns/","toler（承受）+ -ance（能力或状态）→ 面对差异、压力或剂量仍能承受的范围","拉丁语 tolerantia（忍耐），来自 tolerare","the ability or willingness to accept difference, pain, or adverse conditions","the range of burden that can be borne without failure – 在不崩溃前可以承住的范围","秤盘不断加码，支架仍保持稳定",["容忍","耐受性","公差"],["A healthy society requires tolerance.","The material has a high heat tolerance."],["acceptance","endurance"],["intolerance"],["tolerant","tolerate"],["容忍：承受与自己不同的人或观点","耐受性：身体或材料承住刺激的能力","公差：尺寸允许承受的偏差范围"]],
            ["tolerant","adjective","/ˈtɒlərənt/","toler（承受）+ -ant（具有…性质的）→ 能承受差异或不利条件的","拉丁语 tolerans，tolerare（承受）的现在分词","willing to accept differences, or able to withstand conditions","able to carry difference or stress without reacting destructively – 承住差异或压力而不失稳","不同颜色的积木放在同一平台上，平台仍稳稳托住全部",["宽容的","耐受的"],["They are tolerant of opposing views.","This plant is tolerant of drought."],["open-minded","resistant"],["intolerant"],["tolerance","tolerate"],["宽容的：能承受观点和生活方式的差异","耐受的：能承受干旱、温度等不利条件"]],
            ["tolerate","verb","/ˈtɒləreɪt/","toler（承受）+ -ate → 把不舒服或不同之处扛住而不阻止","拉丁语 tolerare（承受、忍耐）","to allow something disliked or withstand an adverse condition","continuing to bear something unpleasant without collapse or removal – 面对不适仍把它承住","机器在持续震动中运转，结构没有断裂",["容忍","忍受","耐受"],["The school will not tolerate bullying.","Some crops tolerate salty soil."],["endure","permit"],["reject"],["tolerance","tolerant"],["容忍/忍受：面对不喜欢的行为或感受仍承受下来","耐受：生物或材料在不利条件下仍维持功能"]]
        ]
    },
    {
        "root": {"id":"tithenai","root":"thesis","variants":["thes","thet"],"origin":"希腊语 thesis（放置、命题），来自 tithenai（放下、安置）","core_concept":"to place an idea in a position / 把一个观点放到桌面上","core_image":"一张写着主张的卡片被放到桌面中央，等待检验和组合","english_definition":"a placing; a proposition set down"},
        "concept": {"id":"concept-thesis-place","concept":"to set down a proposition","chinese":"放下命题","core_image":"一张主张卡片被放到桌面中央等待检验","root_ids":["tithenai"],"word_ids":[]},
        "domain":"domain-make",
        "words":[
            ["hypothesis","noun","/haɪˈpɒθəsɪs/","hypo-（在下方）+ thesis（放置）→ 先放在论证底下作为待验证的基础","希腊语 hypothesis（基础、假定）：hypo- + thesis","an explanation proposed for testing","an idea placed underneath an investigation as its starting support – 先垫在调查下面等待验证的解释","实验开始前，一张暂定说明被放在证据板最底层",["假设","假说"],["The experiment tests the hypothesis.","They proposed a new hypothesis about climate change."],["theory","proposal"],["certainty"],["synthesis","thesis"],["假设/假说：暂时放在研究底部、等待证据检验的解释"]],
            ["synthesis","noun","/ˈsɪnθəsɪs/","syn-（共同）+ thesis（放置）→ 把多个部分放到一起形成整体","希腊语 synthesis：syn- + thesis（共同放置）","the combination of parts or ideas into a connected whole","placing separate pieces together until one whole emerges – 把分散部分共同放成整体","几张不同颜色的碎片被拼到一起，中央出现完整图案",["综合","合成","结合体"],["The essay offers a synthesis of several theories.","The drug is produced by chemical synthesis."],["combination","integration"],["analysis"],["hypothesis","thesis"],["综合：把不同观点共同放进一个整体","合成：把不同物质组合成新整体","结合体：共同放置后形成的结果"]],
            ["thesis","noun","/ˈθiːsɪs/","thesis（放置、命题）→ 正式放出来供论证的主张或研究成果","希腊语 thesis（放置、命题），经拉丁语进入英语","a central proposition or a long research paper supporting one","a claim set down to be defended with evidence – 放到台面上并用证据支撑的主张","一张核心主张放在中央，周围证据用线与它相连",["论点","论文","命题"],["Her thesis challenges the standard account.","He completed his doctoral thesis."],["argument","dissertation"],["retraction"],["hypothesis","synthesis"],["论点/命题：正式放出并准备论证的主张","论文：围绕一个核心主张组织证据的长篇研究"]]
        ]
    },
    {
        "root": {"id":"integer","root":"integer","variants":["integr","teger"],"origin":"拉丁语 integer（完整、未触碰），由 in-（不）+ tangere（触碰）形成","core_concept":"whole and untouched / 完整得没有缺口","core_image":"一只密封圆环没有裂缝，任何部分都未被取走","english_definition":"whole, intact, untouched"},
        "concept": {"id":"concept-integer-whole","concept":"whole and untouched","chinese":"完整无缺","core_image":"密封圆环没有裂缝或缺失部分","root_ids":["integer"],"word_ids":[]},
        "domain":"domain-hold",
        "words":[
            ["integral","adjective","/ˈɪntɪɡrəl/","integr（完整）+ -al → 属于整体且不可缺少的","拉丁语 integralis（构成整体的），来自 integer（完整）","necessary to make a whole complete, or forming a whole","a part whose removal would break the whole – 一旦拿走整体就出现缺口的部分","齿轮组中一枚关键齿轮与其余部分严密咬合",["不可或缺的","完整的","积分的"],["Trust is integral to the partnership.","The machine has an integral control unit."],["essential","inherent"],["optional"],["integrate","integrity"],["不可或缺的：少了它整体便不完整","完整的：作为一个整体内置形成","积分的：数学中把微小部分重新合成整体量"]],
            ["integrate","verb","/ˈɪntɪɡreɪt/","integr（完整）+ -ate → 使分开的部分进入一个完整整体","拉丁语 integrare（使完整、恢复），来自 integer","to combine parts into a whole or bring people fully into a group","making separated parts function as one intact whole – 让分散部分合成无缺口的整体","几个独立模块接上接口后开始像一台机器共同运转",["整合","融入","使一体化"],["The platform integrates several services.","New students quickly integrated into the group."],["combine","unify"],["separate"],["integral","integrity"],["整合/使一体化：把分散部分接成完整系统","融入：让个体进入群体并成为其中完整一部分"]],
            ["integrity","noun","/ɪnˈteɡrəti/","integr（完整）+ -ity（状态）→ 结构没有破损，或人格没有被利益切走一块","拉丁语 integritas（完整、纯正），来自 integer","structural wholeness or firm adherence to moral principles","remaining whole under pressure, physically or morally – 面对压力仍不破裂、不缺失","密封结构经受冲击后仍无裂缝，内部也没有泄漏",["完整性","正直","诚实"],["Engineers checked the bridge's structural integrity.","She acted with integrity."],["wholeness","honesty"],["corruption"],["integral","integrate"],["完整性：结构在压力下仍保持无缺口","正直/诚实：原则没有被诱因削掉一部分"]]
        ]
    },
    {
        "root": {"id":"memor","root":"memor","variants":["mem","memor"],"origin":"拉丁语 memor（记得的、留心的）与 memoria（记忆）","core_concept":"to keep something present in the mind / 把事情留在心中不让它消失","core_image":"已经过去的场景被固定在脑中的一块亮屏上","english_definition":"mindful, remembering, memory"},
        "concept": {"id":"concept-memor-remember","concept":"to keep present in mind","chinese":"留存于心","core_image":"过去的场景被固定在脑中的亮屏上","root_ids":["memor"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ["commemorate","verb","/kəˈmeməreɪt/","com-（共同）+ memor（记住）+ -ate → 大家一起把某事留在记忆中","拉丁语 commemorare（提醒、纪念）：com- + memorare","to honor and remember an important person or event","keeping an event present in shared memory – 让一件事持续留在众人的共同记忆里","人群围在一块刻有日期的石碑旁，安静回望过去",["纪念","庆祝"],["The ceremony commemorates those who died.","A plaque commemorates the discovery."],["honor","remember"],["forget"],["memorial","memory"],["纪念：通过仪式或标志让重要的人与事留在共同记忆中","庆祝：以公开活动记住值得欢庆的事件"]],
            ["memorial","noun","/məˈmɔːriəl/","memor（记住）+ -ial（有关…的）→ 专门帮助人把过去留在心中的标志","晚期拉丁语 memoriale（纪念物），来自 memoria","something created to preserve the memory of a person or event","a visible object that keeps an absent past present – 用可见标志把已经离开的过去留下","广场中央立着刻名石碑，经过的人停步阅读",["纪念碑","纪念物","追悼的"],["They built a memorial beside the river.","A memorial service was held on Sunday."],["monument","tribute"],["oblivion"],["commemorate","memory"],["纪念碑/纪念物：帮助后人持续想起过去的实体标志","追悼的：用于共同记住逝者的"]],
            ["memory","noun","/ˈmeməri/","memor（记住）+ -y → 心中保存并可再次调出的过去内容或能力","拉丁语 memoria（记忆），来自 memor（记得的）","the ability to retain information or something remembered","a past scene kept available inside the mind – 被心智保存、之后还能调出的场景","关闭的相册重新翻开，旧画面再次清晰出现",["记忆力","回忆","存储器"],["The experience remains vivid in my memory.","The computer needs more memory."],["recollection","remembrance"],["forgetfulness"],["commemorate","memorial"],["记忆力：把信息留在心中的能力","回忆：被保存并再次调出的内容","存储器：机器中承担类似留存功能的部件"]]
        ]
    },
    {
        "root": {"id":"mekhane","root":"mēkhanē","variants":["mechan","mech"],"origin":"希腊语 mēkhanē（装置、巧妙手段、机器）","core_concept":"a contrived device that makes work happen / 用巧妙装置让工作发生","core_image":"几根杆、齿轮和绳索组合起来，轻轻一推便抬起重物","english_definition":"device, contrivance, machine"},
        "concept": {"id":"concept-mekhane-device","concept":"a device that makes work happen","chinese":"机械装置","core_image":"杆、齿轮和绳索组合后以小力抬起重物","root_ids":["mekhane"],"word_ids":[]},
        "domain":"domain-make",
        "words":[
            ["mechanic","noun","/məˈkænɪk/","mechan（机器装置）+ -ic（从事者）→ 处理机器结构与运转的人","希腊语 mēkhanikos（与机器有关的），经拉丁语和法语进入英语","a person who repairs and maintains machines","someone who understands how a device's parts produce motion – 看懂各部件如何传力并修复它的人","工作台上摊开齿轮和螺栓，一双手逐件检查磨损",["机械师","修理工"],["The mechanic inspected the engine.","A bicycle mechanic replaced the chain."],["technician","repairer"],[],["mechanical","mechanism"],["机械师/修理工：理解机器部件并维护其运转的人"]],
            ["mechanical","adjective","/məˈkænɪkl/","mechan（机器）+ -ical（有关…的）→ 属于机器运转，或像机器一样不经思考重复","晚期拉丁语 mechanicus，来自希腊语 mēkhanikos","relating to machines, or performed automatically without thought","working through fixed moving parts or fixed repetition – 按预定结构和动作运转","齿轮每转一圈，连杆都按同一路径重复升降",["机械的","机械性的","呆板的"],["The device suffered a mechanical failure.","His response sounded mechanical."],["automatic"],["spontaneous"],["mechanic","mechanism"],["机械的：由机器部件和传力结构完成的","机械性的/呆板的：像固定装置一样重复而缺少灵活判断"]],
            ["mechanism","noun","/ˈmekənɪzəm/","mechan（装置）+ -ism（体系）→ 各部件配合产生结果的内部系统","新拉丁语 mechanismus，来自希腊语 mēkhanē","a system of parts or processes that produces a result","the hidden arrangement through which inputs become an outcome – 输入沿内部结构传递并产生结果","透明外壳内，多枚齿轮依次咬合带动末端指针",["机制","机械装置","机理"],["The locking mechanism is simple.","Researchers studied the mechanism of infection."],["system","process"],["randomness"],["mechanic","mechanical"],["机械装置：实体部件配合运转的系统","机制/机理：任何过程内部使结果发生的连锁结构"]]
        ]
    },
    {
        "root": {"id":"graphein","root":"graphein","variants":["graph","gram"],"origin":"希腊语 graphein（刻写、书写、描画）","core_concept":"to mark lines onto a surface / 在表面刻下可读的线条","core_image":"尖笔在平面上划出线条，把看不见的信息固定成图形","english_definition":"to write, draw, record with marks"},
        "concept": {"id":"concept-graphein-write","concept":"to record with written lines","chinese":"刻写成图","core_image":"尖笔在平面划线，把信息固定成可读图形","root_ids":["graphein"],"word_ids":[]},
        "domain":"domain-perceive",
        "words":[
            ["graph","noun","/ɡrɑːf/","graph（写、画）→ 用线和位置把数量关系画出来的记录","希腊语 graphē（书写、图画），来自 graphein","a diagram showing relationships between quantities","quantities written as positions and lines on a surface – 数量被写成平面上的点和线","坐标纸上的数据点被一条上升曲线连接",["图表","曲线图","绘图"],["The graph shows a steady increase.","Plot the results on a graph."],["chart","diagram"],[],["graphic","paragraph"],["图表/曲线图：把数量关系刻写成位置和线条","绘图：把数据记录到图形表面上的动作"]],
            ["graphic","adjective","/ˈɡræfɪk/","graph（画、写）+ -ic → 通过清楚图形呈现，或描写得像画在眼前","希腊语 graphikos（适于书写或绘画的），来自 graphein","relating to visual images, or described in vivid detail","presented in marks vivid enough to be seen mentally – 用线条或细节呈现得清晰可见","文字旁边出现一幅轮廓鲜明的示意图，信息一眼可辨",["图形的","生动的","详细露骨的"],["The report includes graphic illustrations.","The witness gave a graphic account."],["visual","vivid"],["vague"],["graph","paragraph"],["图形的：以可见线条和图像呈现","生动的/详细露骨的：描述清晰得像直接画在眼前"]],
            ["paragraph","noun","/ˈpærəɡrɑːf/","para-（旁边）+ graph（写）→ 原指写在旁边的段落标记，后指由该标记分出的文字块","希腊语 paragraphos（写在旁边的标记），经拉丁语进入英语","a distinct section of written text dealing with one point","a block of writing marked off as one unit – 被边界标出、集中表达一点的文字块","长篇文字中一次换行缩进，圈出一个独立内容单元",["段落","分段符号"],["Each paragraph develops one idea.","Please divide the text into paragraphs."],["section","passage"],[],["graph","graphic"],["段落：被标记边界分开的一个书写单元","分段符号：早期写在行旁、提示新单元开始的记号"]]
        ]
    }
]

additions = {
    "press": [
        ["impression","noun","/ɪmˈpreʃn/","im-（压入）+ press（压）+ -ion → 外物压入心中留下的痕迹","拉丁语 impressio（压入、印痕），来自 imprimere","an idea or effect formed in the mind, or a mark pressed into a surface","a mark left after something presses inward – 接触之后被压留下来的痕迹","软蜡被印章压下，抬起后仍保留清晰纹路",["印象","印记","印数"],["She made a strong first impression.","The seal left an impression in the wax."],["effect","image"],["certainty"],["impress","impressive","pressure"],["印象：经历压入心中留下的整体痕迹","印记：物体受压后留下的形状","印数：印刷版被反复压印出的数量"]],
        ["impressive","adjective","/ɪmˈpresɪv/","impress（压入、留下印象）+ -ive → 强到能深深压进人心的","英语 impressive，来自 impress","causing admiration through size, quality, or skill","powerful enough to leave a deep mental mark – 力量或品质深深压入心中","宏大的建筑立在眼前，轮廓久久留在观看者脑中",["令人印象深刻的","令人钦佩的"],["The team achieved an impressive result.","The building is visually impressive."],["striking","remarkable"],["ordinary"],["impress","impression","pressure"],["令人印象深刻的/令人钦佩的：效果强到在人心中留下深刻压痕"]],
    ],
    "tain": [
        ["container","noun","/kənˈteɪnə/","con-（共同、在内）+ tain（握住）+ -er → 把内容物收在内部握住的东西","英语 contain + -er；contain 来自拉丁语 continere","an object used to hold or transport things","an enclosure that holds contents together inside – 把内容集中握在内部的外壳","透明盒子的四壁把散落零件稳稳收在里面",["容器","集装箱"],["Store the liquid in a sealed container.","The goods arrived in a shipping container."],["vessel","box"],["contents"],["contain","retain","tenant"],["容器：把物品收在内部的器具","集装箱：用于运输、把大量货物集中握住的标准箱体"]],
        ["tenant","noun","/ˈtenənt/","ten（握住、占有）+ -ant（人）→ 依法握有房屋使用权的人","古法语 tenant（持有者），来自拉丁语 tenere（握住）","a person who rents and occupies property","someone who holds the right to occupy a place for a period – 在约定时期握有空间使用权的人","钥匙被交到入住者手中，在租期内由其保管房屋",["租户","承租人"],["The tenant pays rent monthly.","Landlords must protect tenant rights."],["renter","occupant"],["landlord"],["contain","container","sustain"],["租户/承租人：通过租约暂时握有房屋使用权的人"]]
    ],
    "quir": [
        ["conquest","noun","/ˈkɒŋkwest/","con-（加强、完全）+ quest（寻求）→ 追索到底并取得控制","古法语 conqueste，来自拉丁语 conquirere（搜求、取得）","the act of taking control by force, or something won","a search pursued until the object is taken into one's control – 追求直到目标被取得并控制","旗帜越过城墙，寻找的领地被纳入控制范围",["征服","攻取","战利品"],["The conquest changed the region's borders.","The island became a colonial conquest."],["victory","capture"],["surrender"],["enquire","exquisite","quest"],["征服/攻取：追索目标直到取得控制","战利品：完成这种取得后落入手中的东西"]],
        ["enquire","verb","/ɪnˈkwaɪə/","en-（进入）+ quir（寻求）→ 通过提问深入寻找信息","古法语 enquérir，来自拉丁语 inquirere（寻求、调查）","to ask for information","seeking one's way into missing information through questions – 用问题进入未知处寻找答案","一个问号沿着线索深入档案，逐格照亮空白",["询问","打听","调查"],["I called to enquire about the schedule.","Police enquired into the complaint."],["ask","investigate"],["ignore"],["conquest","exquisite","inquiry"],["询问/打听：通过提问寻找缺少的信息","调查：沿线索深入寻找事实"]],
        ["exquisite","adjective","/ɪkˈskwɪzɪt/","ex-（彻底、向外）+ quisit（寻求）→ 被精挑细选出来的 → 极精美的","拉丁语 exquisitus，来自 exquirere（仔细搜寻、挑选）","extremely beautiful, delicate, or finely made","selected through an exceptionally careful search – 经过细密寻找才挑出的上乘之物","许多近似样品中，一件细节最完美的被单独取出",["精美的","精致的","剧烈的"],["The box contains exquisite carvings.","She felt exquisite pain in her hand."],["delicate","superb"],["crude"],["conquest","enquire","inquiry"],["精美的/精致的：像经过彻底搜选才留下的上品","剧烈的：感觉细密而强烈到每一点都清晰可辨"]]
    ]
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

assert len(words)==37
OUT.write_text(json.dumps({"roots":roots,"concepts":concepts,"domain_add":domain_add,"words":words},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"wrote {OUT} with {len(words)} words, {len(roots)} roots")
