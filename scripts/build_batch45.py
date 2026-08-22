#!/usr/bin/env python3
"""Generate batch45: 6 new roots (18 词) + 1 addition，清掉 HANDOFF 剩下的 C 类风险族。

C 类拆分（HANDOFF 第三节点名，严禁整族并根）:
  leg::lex-legis → lex-legis（法）    delegate / legacy / legal
  leg::lig       → ligare（绑）       obligation / religion / religious
        两族在 vetted 里同名 leg，实为 lex（法）与 ligare（绑）两条源，必须分立；
        与已建模的 legere（读，collect/elect 一支）也不同根。
  prop           → 拆两组：proper/property ← proprius（自己的）；
                   proportion ← portio ← pars（份），并入已有 pars 根，不另开根。
  teri           → ter-comparative（拉丁比较级 -ter/-terior）
                   deteriorate / exterior / interior

另两个词源清楚的族:
  modus（分寸尺度）  commodity / moderate / modify
  qualis（何种性质）  qualification / qualify / quality

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch45.json"


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

# ---------- lex-legis（法）----------
families.append({
    "root": {
        "id": "lex-legis", "root": "lex", "variants": ["leg", "legis"],
        "origin": "拉丁语 lex（属格 legis：成文的法条），动词 legare 表「依法委派、立遗嘱交付」；"
                  "与 legere（读、拣选）虽形近而不同根，本项目分立两根",
        "core_concept": "the written statute that binds all alike / 立成条文、对谁都一样管的法",
        "core_image": "石板上刻好的条文立在广场中央，谁走过都得照着办",
        "english_definition": "law, statute",
    },
    "concept": {
        "id": "concept-lex-statute", "concept": "the written statute that binds all alike",
        "chinese": "成文之法", "core_image": "广场中央立着刻好条文的石板，谁走过都照它办",
        "root_ids": ["lex-legis"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("legal", "lex-legis", "adjective", "/ˈliːɡl/",
          "leg（法条）+ -al（…的）→ 属于成文法的、法条许可的",
          "拉丁语 legalis（属于法的），来自 lex/legis（法条）",
          "relating to the law; allowed by the law",
          "standing on the side the statute allows – 站在条文许可的那一边",
          "翻到条文那一页，指着其中一行说这样办没问题",
          ["法律的", "合法的"],
          ["She sought legal advice at once.", "It is legal to park here on Sundays."],
          ["lawful", "judicial"], ["illegal"],
          ["legacy", "delegate"],
          ["法律的：属于成文法条的", "合法的：落在条文许可那一边的"],
          "leg（法条）+ -al → 属于成文法、为条文所许"),
        W("delegate", "lex-legis", "verb", "/ˈdelɪɡeɪt/",
          "de-（往下）+ leg（依法委派）+ -ate → 依法把职权往下交给人 → 委派",
          "拉丁语 delegare（委派、转交），来自 de＋legare（依法交付）← lex",
          "to give a task or authority to someone else; a person sent to represent others",
          "handing one's warrant down to another to act on it – 把自己那份凭据往下交给人去行使",
          "他在名册上点了一个人，把盖印的文书交到那人手里",
          ["委派", "代表", "授权"],
          ["A good manager knows how to delegate.", "Each branch sent two delegates."],
          ["assign", "entrust"], [],
          ["legal", "legacy"],
          ["委派/授权：依法把职权往下交出", "代表：受此委派、代人出面的那个人"],
          "de-（往下）+ leg（依法委派）→ 把凭据往下交给人"),
        W("legacy", "lex-legis", "noun", "/ˈleɡəsi/",
          "leg（立遗嘱交付）+ -acy → 依遗嘱交下来的东西 → 遗赠，引申为前人留下的",
          "中世纪拉丁语 legatia（遗赠），来自 legare（立遗嘱交付）← lex（法）",
          "money or property left in a will; something handed down from the past",
          "what a warrant hands on after its holder is gone – 立据人身后依据文书交下来的东西",
          "老人过世后，铁盒里的文书按写明的那样一件件交到后人手上",
          ["遗产", "遗赠", "遗留"],
          ["He left a small legacy to the school.", "The war left a legacy of mistrust."],
          ["inheritance", "bequest"], [],
          ["legal", "delegate"],
          ["遗产/遗赠：依文书身后交下来的东西", "遗留：前人手里传下来的那一份"],
          "leg（立遗嘱交付）+ -acy → 依文书交下来的东西"),
    ],
})

# ---------- ligare（绑）----------
families.append({
    "root": {
        "id": "ligare", "root": "ligare", "variants": ["lig", "li", "ly"],
        "origin": "拉丁语 ligare（捆、绑住），ligamentum（韧带）同根；"
                  "与 lex（法）、legere（读）都不同根，vetted 里同作 leg 是自动提取所致",
        "core_concept": "to tie a cord so the two cannot come apart / 用绳把两边系住，再分不开",
        "core_image": "一根绳把两只手腕系在一起，想抽也抽不出来",
        "english_definition": "to bind, tie",
    },
    "concept": {
        "id": "concept-ligare-bind", "concept": "to tie a cord so the two cannot come apart",
        "chinese": "系住不分", "core_image": "绳子把两只手腕系在一起，想抽也抽不出来",
        "root_ids": ["ligare"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("obligation", "ligare", "noun", "/ˌɒblɪˈɡeɪʃn/",
          "ob-（朝向）+ lig（绑）+ -ation → 被绑在某事上、不得不做的那份",
          "拉丁语 obligatio（束缚、义务），来自 obligare（绑住）← ob＋ligare",
          "something one is bound to do, by duty or by law",
          "the cord tying one to a task one cannot walk away from – 把人系在某事上、走不开的那根绳",
          "手腕上那圈绳一头系在事上，脚步再急也带着它",
          ["义务", "责任", "约束"],
          ["He has a legal obligation to pay.", "She felt no obligation to reply."],
          ["duty", "commitment"], ["freedom"],
          ["religion", "religious"],
          ["义务/责任：被系在某事上、非做不可的那份", "约束：那根绳本身的拉力"],
          "ob-（朝向）+ lig（绑）→ 被系在某事上走不开"),
        W("religion", "ligare", "noun", "/rɪˈlɪdʒən/",
          "re-（再、牢）+ lig（绑）+ -ion → 把人反复系向神明的那套联结",
          "拉丁语 religio（虔敬、戒律），一说来自 religare（牢牢系住）← re＋ligare",
          "belief in and worship of a god or gods, with its practices",
          "the cord that ties a people back to what they hold sacred – 把人一再系回所敬之物的那根绳",
          "众人依着同一套誓约聚在一处，绳结般彼此系住",
          ["宗教", "信仰"],
          ["Religion shapes much of the local custom.", "She studies comparative religion."],
          ["faith", "creed"], [],
          ["religious", "obligation"],
          ["宗教/信仰：把人一再系向所敬之物的那套联结"],
          "re-（牢）+ lig（绑）→ 把人一再系回所敬之物"),
        W("religious", "ligare", "adjective", "/rɪˈlɪdʒəs/",
          "religion（联结）+ -ous（…的）→ 属于那套联结的；引申为一丝不苟",
          "拉丁语 religiosus（虔敬的、谨守的），来自 religio",
          "relating to religion; believing strongly; done with scrupulous care",
          "holding to the cord without letting it slack – 攥着那根绳不让它松",
          "他每日照着同一套仪节做，一次也没落下",
          ["宗教的", "虔诚的", "严谨的"],
          ["He comes from a religious family.", "She keeps religious records of every payment."],
          ["devout", "scrupulous"], ["secular"],
          ["religion", "obligation"],
          ["宗教的：属于那套联结的", "虔诚的：攥住绳子不放松", "严谨的：同样这份不肯松的劲用在做事上"],
          "religion（联结）+ -ous → 攥着那根绳不放松"),
    ],
})

# ---------- proprius（自己的）----------
families.append({
    "root": {
        "id": "proprius", "root": "proprius", "variants": ["propr", "prop", "proper"],
        "origin": "拉丁语 proprius（自己的、专属的），由 pro privo（归私有）而来；"
                  "与 portio（份）一支的 proportion 不同源，vetted 同作 prop 是自动提取所致",
        "core_concept": "what belongs to this one and no other / 专属于这一个、别处不作数",
        "core_image": "一件物上刻着自己的名号，别人拿了也对不上",
        "english_definition": "one's own, particular",
    },
    "concept": {
        "id": "concept-proprius-own", "concept": "what belongs to this one and no other",
        "chinese": "专属自己", "core_image": "物件上刻着自己的名号，别人拿了对不上",
        "root_ids": ["proprius"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("proper", "proprius", "adjective", "/ˈprɒpə(r)/",
          "proprius（专属的）→ 正是这一个该有的样子 → 恰当、合规矩",
          "古法语 propre，来自拉丁语 proprius（自己的、专属的）",
          "right, suitable, or correct for the situation",
          "the one form that fits this case and no other – 只有这一种才对得上这场合",
          "钥匙插进去一转就开，别的哪一把都对不上这个孔",
          ["适当的", "正确的", "真正的"],
          ["Use the proper tool for the job.", "That is not the proper way to ask."],
          ["suitable", "correct"], ["improper"],
          ["property", "proportion"],
          ["适当的/正确的：正是这场合专该有的那一种", "真正的：名实相符、对得上的"],
          "proprius（专属的）→ 正对得上这场合的那一种"),
        W("property", "proprius", "noun", "/ˈprɒpəti/",
          "propr（自己的）+ -ty → 归自己名下之物；也指物本身专有的性状",
          "古法语 propriete，来自拉丁语 proprietas（所有权、特性）← proprius",
          "a thing owned; land and buildings; a quality belonging to something",
          "what stands under one's own name, or a trait belonging to a thing alone – 记在自己名下之物，或某物独有的性状",
          "文书上写明这几间屋归他名下；铁遇火会红，这是铁自带的脾性",
          ["财产", "房产", "特性"],
          ["All his property passed to his son.", "Salt has the property of preserving food."],
          ["possession", "attribute"], [],
          ["proper", "proportion"],
          ["财产/房产：记在自己名下之物", "特性：某物专有、别物没有的性状"],
          "propr（自己的）+ -ty → 归自己名下之物，及物自带的性状"),
    ],
})

# ---------- ter-comparative（拉丁比较级 -ter/-terior）----------
families.append({
    "root": {
        "id": "ter-comparative", "root": "-ter/-terior", "variants": ["ter", "terior"],
        "origin": "拉丁语用后缀 -ter/-terior 构成「两者相比」的对照级：exterus（外）→ exterior，"
                  "interus（内）→ interior，deterior（更差）→ deteriorate。"
                  "这三词共用的不是某个实义词根，而是这套对照级构词法",
        "core_concept": "of two sides compared, the one further that way / 两边一比，更偏那一头的那个",
        "core_image": "两样东西并排一放，指着更偏一头的那个说就是它",
        "english_definition": "the further of two, comparative",
    },
    "concept": {
        "id": "concept-ter-comparative", "concept": "of two sides compared, the one further that way",
        "chinese": "两相对照", "core_image": "两样东西并排一放，指着更偏一头的那个",
        "root_ids": ["ter-comparative"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("exterior", "ter-comparative", "noun", "/ɪkˈstɪəriə(r)/",
          "exter（外）+ -ior（对照级）→ 两边相比更靠外的那一面",
          "拉丁语 exterior（较外的），exterus（在外的）的比较级",
          "the outer surface or appearance of something",
          "the further-out of the two faces – 里外一比，更靠外的那一面",
          "手掌沿墙抹过去，摸到的是朝着风雨的那一面",
          ["外部的", "外表"],
          ["The exterior walls need painting.", "Beneath his calm exterior he was furious."],
          ["outside", "surface"], ["interior"],
          ["interior", "deteriorate"],
          ["外部的/外表：里外相比更靠外的那一面"],
          "exter（外）+ -ior（对照级）→ 更靠外的那一面"),
        W("interior", "ter-comparative", "noun", "/ɪnˈtɪəriə(r)/",
          "inter（内）+ -ior（对照级）→ 两边相比更靠里的那一面",
          "拉丁语 interior（较内的），interus（在内的）的比较级",
          "the inside part of something; the inland part of a country",
          "the further-in of the two faces – 里外一比，更靠里的那一面",
          "推门进去，脚步声在四壁之间来回撞",
          ["内部的", "内部", "内地"],
          ["The car has a leather interior.", "They travelled into the interior."],
          ["inside", "inland"], ["exterior"],
          ["exterior", "deteriorate"],
          ["内部的/内部：里外相比更靠里的那一面", "内地：一国之中更靠里、离海更远的那片"],
          "inter（内）+ -ior（对照级）→ 更靠里的那一面"),
        W("deteriorate", "ter-comparative", "verb", "/dɪˈtɪəriəreɪt/",
          "deterior（更差，比较级）+ -ate（使/变）→ 一路往更差那头去",
          "晚期拉丁语 deteriorare（使变坏），来自 deterior（较差的，de- 的比较级）",
          "to become progressively worse",
          "sliding step by step toward the worse of the two – 一步步滑向两者中更差那一头",
          "墙面一年比一年斑驳，去年补的那块今年又鼓起来",
          ["恶化", "变坏", "退化"],
          ["Her health deteriorated over the winter.", "Relations between them deteriorated fast."],
          ["worsen", "decline"], ["improve", "recover"],
          ["exterior", "interior"],
          ["恶化/变坏：一路滑向更差那一头", "退化：同一方向上功能一路走低"],
          "deterior（更差）+ -ate → 往更差那头一路去"),
    ],
})

# ---------- modus（分寸尺度）----------
families.append({
    "root": {
        "id": "modus", "root": "modus", "variants": ["mod", "moder"],
        "origin": "拉丁语 modus（量度、限度、办法），modestus（守分寸的）、modulus（小尺度）同根",
        "core_concept": "the measure kept, neither over nor under / 守住的那个量，不多也不少",
        "core_image": "量杯上刻着一道线，倒到那道线就停手",
        "english_definition": "measure, limit, manner",
    },
    "concept": {
        "id": "concept-modus-measure", "concept": "the measure kept, neither over nor under",
        "chinese": "分寸尺度", "core_image": "量杯上一道刻线，倒到那道线就停手",
        "root_ids": ["modus"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("moderate", "modus", "adjective", "/ˈmɒdərət/",
          "mod（量度）+ -er- + -ate → 守在刻线之内的 → 不过火",
          "拉丁语 moderatus（有节制的），moderare（节制）的过去分词 ← modus",
          "average in amount or degree; not extreme",
          "staying inside the line, never brimming over – 停在刻线之内，不满溢出来",
          "水倒到刻线就收手，杯子没溢也不见底",
          ["适度的", "温和的", "中等的"],
          ["Take moderate exercise every day.", "He holds moderate political views."],
          ["temperate", "mild"], ["extreme", "excessive"],
          ["modify", "commodity"],
          ["适度的/中等的：停在刻线之内、不过量", "温和的：主张同样不走极端"],
          "mod（量度）+ -ate → 守在刻线之内、不过火"),
        W("modify", "modus", "verb", "/ˈmɒdɪfaɪ/",
          "mod（量度）+ -ify（使…）→ 把尺度调一调 → 修改、使缓和",
          "拉丁语 modificare（限定、调整），来自 modus＋facere（做）",
          "to change something slightly, especially to improve it",
          "shifting the line a little rather than remaking the vessel – 把那道刻线挪一点，而非另造一只杯",
          "把刻线往下挪了半分，别处一概没动",
          ["修改", "调整", "使缓和"],
          ["They modified the design slightly.", "She modified her tone when he objected."],
          ["adjust", "alter"], [],
          ["moderate", "commodity"],
          ["修改/调整：把尺度挪动一点", "使缓和：把话或态度的分寸往回收一点"],
          "mod（量度）+ -ify → 把那道刻线挪一点"),
        W("commodity", "modus", "noun", "/kəˈmɒdəti/",
          "com-（合）+ mod（量度）+ -ity → 合于尺度、便于计量买卖之物",
          "拉丁语 commoditas（便利、合宜），来自 commodus（合尺度的）← com＋modus",
          "a thing bought and sold, especially a basic good",
          "goods cut to a common measure so they can be traded – 按公认尺度计量、可拿去交易之物",
          "秤上一斤一斤过，按同一把尺子记价开单",
          ["商品", "日用品"],
          ["Coffee is a global commodity.", "Water became a scarce commodity."],
          ["goods", "merchandise"], [],
          ["moderate", "modify"],
          ["商品/日用品：按公认尺度计量、可供买卖之物"],
          "com-（合）+ mod（量度）→ 合于尺度、可计量买卖之物"),
    ],
})

# ---------- qualis（何种性质）----------
families.append({
    "root": {
        "id": "qualis", "root": "qualis", "variants": ["qual"],
        "origin": "拉丁语 qualis（何种、什么样的），qualitas（性质）由此出；"
                  "英语 quality/qualify 均循此路",
        "core_concept": "what kind a thing is, and whether it measures up / 是什么成色，够不够格",
        "core_image": "两块料子对着光看纹理，分出哪一块成色更足",
        "english_definition": "of what kind, such as",
    },
    "concept": {
        "id": "concept-qualis-kind", "concept": "what kind a thing is, and whether it measures up",
        "chinese": "成色够格", "core_image": "两块料子对着光看纹理，分出哪块成色更足",
        "root_ids": ["qualis"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("quality", "qualis", "noun", "/ˈkwɒləti/",
          "qual（何种性质）+ -ity → 是什么成色 → 品质；也指人身上的特质",
          "拉丁语 qualitas（性质、属性），来自 qualis（何种）",
          "how good something is; a feature someone or something has",
          "what kind a thing turns out to be when looked at closely – 细看之下，它到底是什么成色",
          "对着光看那块料，纹理密实，一眼便知与别的不同",
          ["质量", "品质", "特质"],
          ["The quality of the cloth is excellent.", "Patience is her best quality."],
          ["standard", "attribute"], [],
          ["qualify", "qualification"],
          ["质量/品质：细看之下是什么成色", "特质：人或物身上那一样别处没有的性质"],
          "qual（何种性质）+ -ity → 到底是什么成色"),
        W("qualify", "qualis", "verb", "/ˈkwɒlɪfaɪ/",
          "qual（何种性质）+ -ify（使…）→ 使成色够得上 → 具备资格；也指给话加限定",
          "中世纪拉丁语 qualificare（定其性质），来自 qualis＋facere（做）",
          "to reach the required standard; to limit a statement",
          "coming up to the mark that the kind requires – 成色达到那一档所要求的线",
          "料子送去过筛，够得上那道线的才盖印放行",
          ["取得资格", "合格", "限定"],
          ["She qualified as a doctor last year.", "He qualified his praise with one caution."],
          ["certify", "restrict"], ["disqualify"],
          ["quality", "qualification"],
          ["取得资格/合格：成色够上所要求那道线", "限定：给话加一道界线，缩住它的适用范围"],
          "qual（何种性质）+ -ify → 使成色够上那道线"),
        W("qualification", "qualis", "noun", "/ˌkwɒlɪfɪˈkeɪʃn/",
          "qualify（使够格）+ -ation → 够格这件事，及作凭据的那纸；也指附加的限定",
          "中世纪拉丁语 qualificatio，来自 qualificare",
          "an official record of passing an exam; a skill making one suitable; a limiting remark",
          "the proof that one came up to the mark, or the limit set on a claim – 够上那道线的凭据，或给话加的那道界",
          "抽屉里那张盖了印的纸，写明他过了那道线",
          ["资格", "学历", "限定条件"],
          ["She has a teaching qualification.", "He agreed, with one qualification."],
          ["credential", "reservation"], [],
          ["quality", "qualify"],
          ["资格/学历：够上那道线的凭据", "限定条件：给话加的那道界"],
          "qualify（使够格）+ -ation → 够格的凭据，或所加的那道界"),
    ],
})

# ================= 补词：并入已建模词根 =================
# proportion 来自 pro portione，portio（份）与 pars/partis（部分）同源，
# 故并入已有 pars 根，不为它另开 portio 根（HANDOFF D 类思路）。
additions = [
    W("proportion", "pars", "noun", "/prəˈpɔːʃn/",
      "pro-（按照）+ portio（份）→ 按份切分后各占的那一份 → 比例",
      "拉丁语 proportio（比例），来自 pro portione（按份而言）；"
      "portio（份）与 pars/partis（部分）同源，故归 pars 一族",
      "a part considered in relation to the whole; the right relation between parts",
      "how large a share one piece takes of the whole – 一块在整体里占多大的一份",
      "圆饼切开，每人手里那块占整张多大，一眼比得出来",
      ["比例", "部分", "均衡"],
      ["A large proportion of the class agreed.", "The columns are pleasing in proportion."],
      ["ratio", "share"], [],
      ["part", "partial"],
      ["比例：一份占整体多大", "部分：切出来的那一份本身", "均衡：各份之间大小相称"],
      "pro-（按照）+ portio（份）→ 各占整体的那一份"),
]

# ================= 组装 =================
words = []
for fam in families:
    words.extend(fam["words"])
words.extend(additions)

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
assert len(roots) == 6, len(roots)
assert len({r["id"] for r in roots}) == 6, "新词根 id 有重复"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words "
      f"({len(words) - len(additions)} family + {len(additions)} additions), "
      f"{len(roots)} new roots")
