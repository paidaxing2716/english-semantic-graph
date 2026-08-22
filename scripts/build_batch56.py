#!/usr/bin/env python3
"""Generate batch56: 补 9 个已建模词根共 11 词——词根型批次的第一部分。

这些词是子代理起草日耳曼批次时筛出来的：它们词源上属已建模词根，
若做成孤立词条会把本该成簇的词族切碎（structus 重复 stru 那次已犯过）。
筛查工具见 scripts/screen_draft_etymology.py。

  cep（capere 抓取）   catch / chase
  cadere（落下）       chance / cheat
  civis（市民）        citizen / city
  habere（持有）       able / ability
  ligare（捆绑）       ally / alliance / alloy
  valere（有力）       avail
  gen（种、生育）      benign
  caedere（切砍）      cement

本批不新建根——新建的 11 个根另起一批，那部分错误面大，逐个核词源。

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch56.json"


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


words = [
    # ---------- cep（capere 抓取）----------
    W("catch", "cep", "verb", "/kætʃ/",
      "capere（抓取）经古北法语 cachier（追捕）→ 伸手把动着的东西拿住",
      "古北法语 cachier（追、捕）← 通俗拉丁语 captiare ← 拉丁语 capere（抓取）",
      "to take hold of something moving; to be in time for",
      "closing the hand on something already in motion – 把正动着的东西一把攥住",
      "球还在半空，他一伸手扣住了",
      ["抓住", "赶上", "染上"],
      ["She caught the ball with one hand.", "He just caught the last train."],
      ["seize", "grasp"], ["drop", "miss"],
      ["capture", "chase"],
      ["抓住：把动着的东西一把攥住", "赶上：在开走之前把它抓着", "染上：病像被抓住一样落到身上"],
      "capere（抓取）→ 把正动着的东西一把攥住"),
    W("chase", "cep", "verb", "/tʃeɪs/",
      "capere（抓取）经古法语 chacier（追猎）→ 一路追着要抓住",
      "古法语 chacier（追猎）← 通俗拉丁语 captiare ← 拉丁语 capere；与 catch 同源分支",
      "to run after someone or something to catch them",
      "keeping after a thing because the hand has not closed on it yet – 手还没抓住，脚就一直跟着",
      "狗撒开腿跟着那团影子跑，隔一段又追近些",
      ["追赶", "追捕", "追求"],
      ["The dog chased the rabbit.", "Police chased the car for miles."],
      ["pursue", "hunt"], ["flee"],
      ["catch", "capture"],
      ["追赶/追捕：手未及、脚先跟着不放", "追求：同一个追法用在人或目标上"],
      "capere（抓取）→ 手未及先追着，chacier 一支"),
    # ---------- cadere（落下）----------
    W("chance", "cadere", "noun", "/tʃɑːns/",
      "cadere（落下）→ 骰子落地那一面 → 碰巧、机会",
      "古法语 cheance（掷骰所得）← 通俗拉丁语 cadentia（落下之势）← 拉丁语 cadere（落下）",
      "a possibility of something happening; an opportunity",
      "which face the die shows when it stops rolling – 骰子停下来时朝上的那一面",
      "骰子在桌上滚了两圈，停下时朝上那面谁也没料到",
      ["机会", "可能性", "偶然"],
      ["This is your last chance.", "There is a chance of rain today."],
      ["opportunity", "possibility"], ["certainty"],
      ["accident", "incident"],
      ["机会：骰子恰好落成对你有利那面", "可能性：它可能落成的各面之一", "偶然：落成哪面并非人定"],
      "cadere（落下）→ 骰子停下时朝上那一面"),
    W("cheat", "cadere", "verb", "/tʃiːt/",
      "cadere（落下）→ escheat（无主财产归公）→ 借职权占人便宜 → 欺骗",
      "中古英语 cheten，截自 escheat（封建法中无嗣田产落归领主）← 古法语 eschete ← cadere（落下）",
      "to act dishonestly to gain an advantage",
      "taking what fell to another and calling it one's own – 把该落到别人手里的据为己有",
      "他把牌往袖口一带，抬头时脸上没有半点异样",
      ["欺骗", "作弊", "骗子"],
      ["He cheated in the exam.", "She felt cheated by the deal."],
      ["deceive", "trick"], ["honest"],
      ["chance", "accident"],
      ["欺骗/作弊：把该落给别人的悄悄占去", "骗子：惯做此事的那个人"],
      "cadere（落下）→ 把落归他人之物占去"),
    # ---------- civis（市民）----------
    W("city", "civis", "noun", "/ˈsɪti/",
      "civis（市民）→ civitas（市民共同体）→ 市民聚居之地",
      "古法语 cité ← 拉丁语 civitas（公民共同体、城邦）← civis（市民）",
      "a large town where many people live and work",
      "the place named after the body of people in it, not its walls – 以住在里头的人得名，而非以城墙",
      "屋顶一直连到天边，路口的人流从早到晚没断过",
      ["城市", "都市"],
      ["She moved to the city last year.", "The city has three million people."],
      ["town", "metropolis"], ["countryside"],
      ["citizen", "civil"],
      ["城市/都市：以聚居其中的市民得名的那处地方"],
      "civis（市民）→ civitas（市民共同体）→ 其聚居之地"),
    W("citizen", "civis", "noun", "/ˈsɪtɪzn/",
      "civis（市民）+ -zen（居者）→ 属这座城、有其权利与义务的人",
      "盎格鲁法语 citezein ← 古法语 citeain ← 拉丁语 civitas ← civis（市民）",
      "a person who legally belongs to a country and has its rights",
      "the one the city counts as its own – 被这座城认作自己人的那个",
      "他掏出那本册子，柜台后的人点点头就放行了",
      ["公民", "市民", "居民"],
      ["Every citizen may vote.", "She became a citizen last spring."],
      ["national", "resident"], ["foreigner"],
      ["city", "civil"],
      ["公民：被国家认作自己人、有权利义务的那个", "市民/居民：同理，落在城这一级"],
      "civis（市民）+ -zen（居者）→ 被这座城认作自己人的"),
    # ---------- habere（持有）----------
    W("able", "habere", "adjective", "/ˈeɪbl/",
      "habere（拿住）→ habilis（好操持的）→ 拿得住、使得动 → 有能力的",
      "古法语 able ← 拉丁语 habilis（易于操持的）← habere（拿住）",
      "having the skill or power to do something",
      "the hand that can actually hold and work the thing – 手真拿得住、使得动的那种",
      "别人拧不开那个盖子，递给他一转就开了",
      ["能够的", "有能力的"],
      ["She is able to speak three languages.", "He was not able to come."],
      ["capable", "competent"], ["unable"],
      ["ability", "exhibit"],
      ["能够的/有能力的：手真拿得住、使得动的那种"],
      "habere（拿住）→ habilis（好操持）→ 拿得住"),
    W("ability", "habere", "noun", "/əˈbɪləti/",
      "able（拿得住）+ -ity → 拿得住这件事本身 → 能力",
      "古法语 ablete ← 拉丁语 habilitas（易操持的性质）← habere（拿住）",
      "the power or skill needed to do something",
      "how much the hand can actually take on – 那双手到底拿得住多少",
      "同一副担子有人挑不起，有人挑起来还能走",
      ["能力", "才能"],
      ["She has great ability in maths.", "It is beyond my ability to fix."],
      ["skill", "capacity"], ["inability"],
      ["able", "exhibit"],
      ["能力/才能：手拿得住、使得动的那份分量"],
      "able（拿得住）+ -ity → 拿得住的那份分量"),
    # ---------- ligare（捆绑）----------
    W("ally", "ligare", "noun", "/ˈælaɪ/",
      "al-（ad- 朝）+ lig（绑）→ 绑到一处的那一方 → 盟友",
      "古法语 alier（结合）← 拉丁语 alligare（捆在一起）← ad＋ligare（绑）",
      "a country or person joined with another for a shared purpose",
      "the one tied to your side by the same cord – 被同一根绳系到你这边的那方",
      "两只手腕被一根绳系住，往哪走都得一块儿",
      ["盟友", "同盟者", "结盟"],
      ["Britain was a wartime ally.", "The two nations allied against the threat."],
      ["partner", "associate"], ["enemy", "rival"],
      ["alliance", "obligation"],
      ["盟友/同盟者：被同一根绳系到自己这边的那方", "结盟：把两方系到一处这个动作"],
      "al-（朝）+ lig（绑）→ 被同一根绳系到一处"),
    W("alliance", "ligare", "noun", "/əˈlaɪəns/",
      "ally（结盟）+ -ance → 系在一处这件事，及系成的那个组合",
      "古法语 aliance（结盟）← alier ← 拉丁语 alligare ← ad＋ligare（绑）",
      "a formal agreement between countries or groups to work together",
      "the knot itself, once two sides are corded together – 两方系妥之后那个结",
      "绳头交叉压紧，打成一个谁也抽不开的结",
      ["联盟", "同盟", "结盟"],
      ["The alliance lasted thirty years.", "They formed an alliance in 1949."],
      ["union", "coalition"], ["split"],
      ["ally", "obligation"],
      ["联盟/同盟：两方系妥之后成的那个结", "结盟：打这个结的过程"],
      "ally（结盟）+ -ance → 两方系妥后成的那个结"),
    W("alloy", "ligare", "noun", "/ˈælɔɪ/",
      "al-（ad- 朝）+ loy（绑）→ 两种金属绑成一体 → 合金",
      "古法语 aloi（成色）← aloier（混合）← 拉丁语 alligare（捆在一起）← ad＋ligare",
      "a metal made by melting two or more metals together",
      "two metals corded into one body that no longer comes apart – 两种金属绑成一体，再分不开",
      "炉里两样金属化在一处，冷了以后倒不出哪是哪",
      ["合金"],
      ["Brass is an alloy of copper and zinc.", "The frame is made of light alloy."],
      ["mixture", "compound"], [],
      ["ally", "alliance"],
      ["合金：两种金属绑成一体、再分不开的那种材料"],
      "al-（朝）+ loy（绑）→ 两种金属绑成一体"),
    # ---------- valere（有力）----------
    W("avail", "valere", "verb", "/əˈveɪl/",
      "a-（ad- 朝）+ vail（值、有力）→ 顶得上用 → 有助于",
      "中古英语 availen，由 a-（拉丁 ad 向）＋古法语 vail-（valoir 值）← 拉丁语 valere（有力、值）",
      "to be of use or help; to make use of something",
      "whether the thing turns out to carry any weight – 那东西到底顶不顶得上用",
      "带来的工具往锁上一试，居然真能拧开",
      ["有助于", "利用", "效用"],
      ["Nothing availed against the storm.", "She availed herself of the offer."],
      ["help", "profit"], ["fail"],
      ["prevalent"],
      ["有助于/效用：那东西顶得上用、有分量", "利用：把这份分量拿来用在自己身上"],
      "a-（朝）+ vail（值、有力）→ 顶得上用"),
    # ---------- gen（种、生育）----------
    W("benign", "gen", "adjective", "/bɪˈnaɪn/",
      "bene（好）+ gn（gen 出身、天性）→ 天性好的 → 和善、良性",
      "古法语 benigne ← 拉丁语 benignus（善良的）← bene（好）＋genus（出身、种）",
      "kind and gentle; not dangerous in nature",
      "born with a mild nature, so it does no harm – 生来性子温的，因此不伤人",
      "护士说话放轻，动作也慢，针扎下去几乎没觉出",
      ["和善的", "良性的", "温和的"],
      ["He gave a benign smile.", "The tumour turned out to be benign."],
      ["kindly", "harmless"], ["malignant", "hostile"],
      ["generous", "generate"],
      ["和善的/温和的：生来性子温、不伤人", "良性的：同一份「天性不凶」用在病灶上"],
      "bene（好）+ gn（出身天性）→ 生来性子温的"),
    # ---------- caedere（切砍）----------
    W("cement", "caedere", "noun", "/sɪˈment/",
      "caedere（切、砍）→ caementum（砍碎的石屑）→ 碎石烧成的胶结料",
      "古法语 ciment ← 拉丁语 caementum（采石场砍下的碎石）← caedere（切、砍）",
      "a grey powder that hardens when mixed with water, used in building",
      "the stone chips ground down and made to bind again – 砍碎的石头磨成粉，又让它重新黏合",
      "灰粉兑水搅成糊，抹进砖缝，第二天硬得抠不动",
      ["水泥", "胶结剂", "黏合"],
      ["They mixed cement and sand.", "The talks cemented their friendship."],
      ["mortar", "bond"], [],
      ["precise", "concise"],
      ["水泥/胶结剂：砍碎的石屑磨粉后重新黏合之物", "黏合：把两边像水泥那样固牢"],
      "caedere（切砍）→ caementum（碎石屑）→ 烧成胶结料"),
]

# ---- 生成期自检 ----
for w in words:
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"Q12 泄题：{w['id']} 的 core_image 点名义项「{zh}」"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert w["recall_hint"], f"Q12：{w['id']} 缺 recall_hint"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"
assert len({w["id"] for w in words}) == len(words), "词条 id 有重复"

OUT.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=2) + "\n",
               encoding="utf-8")
print(f"wrote {OUT}: {len(words)} 词，全部补进已建模词根，无新根")
