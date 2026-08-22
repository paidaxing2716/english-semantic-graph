#!/usr/bin/env python3
"""Generate batch65: 9 新词根 27 词 + 19 补词。

新根：
  merx（货）        market / merchant / commerce / mercy
  maritus（配偶）   marry / marriage / married / marital
  medius（居中）    means / meantime / medal
  mens（心念）      mental / mention / comment
  mergere（浸没）   merge / emerge / immerse
  gnoscere（识得）  ignore / ignorant / noble
  negare（否决）    deny / denial / negative
  nutrire（哺育）   nurse / nourish / nurture
  labi（滑脱）      lapse / elapse / collapse

补进已建模根（含两处纠正）：
  mov ← mob / mobile / mobilize / moment / momentum
      子代理报作新根 movere，但 mov 的 origin 就写「拉丁语 movere」，同一个根
  maior ← magnify / maximum / mayor
      子代理报作新根 magnus，而 maior 的 origin 已写明它是 magnus 的比较级；
      mayor ← maior 本身，maximum ← maximus（最高级），magnify ← magnus＋facere，
      三者同出一支，并入 maior 不另开根
  audire ← obey    caput ← mischief    domus ← madame    fendere ← offend
  ligare ← league  mekhane ← machine   minus ← menu      nasci ← naive
  via ← obvious

写法：W() 定参函数。Q12/Q1 自检与自环断言均在生成期。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch65.json"


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
additions = []

# ---------- merx（货）----------
families.append({
    "root": {
        "id": "merx", "root": "merx", "variants": ["merc", "market", "merch"],
        "origin": "拉丁语 merx（属格 mercis：货物）；mercari 是「做买卖」，"
                  "merces 是「报酬、恩惠」——同一批货，看的是它换来什么",
        "core_concept": "goods put out to be exchanged / 摆出来供交换的那批东西",
        "core_image": "布摊在地上，货一样样码开，等着有人过来问价",
        "english_definition": "merchandise, goods",
    },
    "concept": {
        "id": "concept-merx-goods", "concept": "goods put out to be exchanged",
        "chinese": "待换之货", "core_image": "布摊在地上，货一样样码开，等着有人来问价",
        "root_ids": ["merx"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("market", "merx", "noun", "/ˈmɑːkɪt/",
          "merx（货）→ mercatus（交易、集市）→ 摆货交换的那个场",
          "古北法语 market ← 拉丁语 mercatus（买卖、集市）← mercari ← merx（货）",
          "a place where goods are bought and sold; demand for something",
          "the ground where sellers lay out and buyers walk through – 卖的人摆开、买的人穿行的那片地",
          "一早地上就摊满了，人挨着货走，边看边问",
          ["市场", "集市", "行情"],
          ["She sells eggs at the market.", "There is no market for that."],
          ["fair", "demand"], [],
          ["merchant", "commerce"],
          ["市场/集市：摆货交换的那片场地", "行情：某样货在那片场上换得动多少"],
          "merx（货）→ mercatus（集市）→ 摆货交换的场"),
        W("merchant", "merx", "noun", "/ˈmɜːtʃənt/",
          "merx（货）→ mercatans（做买卖的）→ 靠贩货为业的人",
          "古法语 marchant ← 通俗拉丁语 mercatans ← mercari（买卖）← merx（货）",
          "a person who buys and sells goods, especially in large amounts",
          "the one who owns neither field nor workshop, only the goods in transit – 既不种地也不开工坊，手里只有在途那批货的人",
          "他自己不做也不种，一船拉进来，一船运出去",
          ["商人", "批发商"],
          ["The merchant traded in silk.", "Wool merchants grew rich here."],
          ["trader", "dealer"], [],
          ["market", "commerce"],
          ["商人/批发商：靠买进卖出货物为业的人"],
          "merx（货）→ mercatans → 靠贩货为业的人"),
        W("commerce", "merx", "noun", "/ˈkɒmɜːs/",
          "com-（一起）+ merce（货）→ 众人拿货互换 → 商业",
          "法语 commerce ← 拉丁语 commercium（贸易）← com＋merx（货）",
          "the buying and selling of goods on a large scale",
          "goods moving between many hands, not just two – 货在许多手之间流转，不止两方对换",
          "船进港、车出城，货一批批换了主人又往前走",
          ["商业", "贸易"],
          ["Commerce between the two grew.", "The port thrives on commerce."],
          ["trade", "business"], [],
          ["market", "merchant"],
          ["商业/贸易：众人拿货互换、货在多手间流转"],
          "com-（一起）+ merce（货）→ 众人拿货互换"),
        W("mercy", "merx", "noun", "/ˈmɜːsi/",
          "merces（报酬、恩惠）← merx（货）→ 不索价而给的那份 → 宽恕",
          "古法语 merci ← 拉丁语 merces（报酬、恩惠）← merx（货）；"
          "由「该收的价」转指「不收价而施的恩」",
          "kindness shown in not punishing someone as much as one could",
          "the payment owed but not collected – 该收的那笔，收方却不要了",
          "账本上写着数目，那人把本子合上，说不必了",
          ["仁慈", "宽恕", "怜悯"],
          ["The judge showed mercy.", "They begged for mercy."],
          ["pity", "leniency"], ["cruelty"],
          ["market", "commerce"],
          ["仁慈/宽恕/怜悯：该收的那笔不收了，即不索价而施的恩"],
          "merces（报酬）← merx（货）→ 该收却不收的那份"),
    ],
})

# ---------- maritus（配偶）----------
families.append({
    "root": {
        "id": "maritus", "root": "maritus", "variants": ["marit", "marri", "mari"],
        "origin": "拉丁语 maritus（有配偶的、丈夫），maritare 表「使成配偶」；"
                  "经古法语 marier 入英语",
        "core_concept": "two joined into one household by vow / 一纸约把两人并成一户",
        "core_image": "两个名字并排写在同一张纸上，底下按了两个手印",
        "english_definition": "husband, wedded",
    },
    "concept": {
        "id": "concept-maritus-wedded", "concept": "two joined into one household by vow",
        "chinese": "结为一户", "core_image": "两个名字并排写在同一张纸上，底下按了两个手印",
        "root_ids": ["maritus"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("marry", "maritus", "verb", "/ˈmæri/",
          "maritare（使成配偶）→ 把两人并成一户",
          "古法语 marier ← 拉丁语 maritare（嫁娶）← maritus（配偶）",
          "to become the husband or wife of someone",
          "the moment two names go onto one paper – 两个名字落到同一张纸上那一刻",
          "他们在那张纸上依次签了名，回身时已是一户",
          ["结婚", "娶", "嫁"],
          ["They married last autumn.", "She married her old classmate."],
          ["wed", "unite"], ["divorce"],
          ["marriage", "married"],
          ["结婚/娶/嫁：把两人并成一户这个动作"],
          "maritare（使成配偶）→ 把两人并成一户"),
        W("marriage", "maritus", "noun", "/ˈmærɪdʒ/",
          "marry（结婚）+ -age → 结成一户这件事，及此后那个关系",
          "古法语 mariage ← 通俗拉丁语 maritaticum ← maritus（配偶）",
          "the legal union of two people; the state of being married",
          "the arrangement that holds after the paper is signed – 纸签完之后一直立着的那层关系",
          "那张纸收进抽屉，往后几十年都按它上面的算",
          ["婚姻", "结婚", "结合"],
          ["Their marriage lasted forty years.", "The marriage took place in June."],
          ["union", "wedding"], ["divorce"],
          ["marry", "married"],
          ["婚姻：纸签完后一直立着的那层关系", "结婚：签那张纸的那一场", "结合：两者并成一体，泛用"],
          "marry（结婚）+ -age → 结成一户这件事及其关系"),
        W("married", "maritus", "adjective", "/ˈmærid/",
          "marry（结婚）+ -ed → 已经并成一户的",
          "英语 married，来自 marry ← 拉丁语 maritare ← maritus",
          "having a husband or wife",
          "the state of already being on that one paper – 名字已经在那张纸上的状态",
          "他左手无名指上有一圈没晒到的白痕",
          ["已婚的"],
          ["They have been married ten years.", "She is married to a doctor."],
          ["wed", "wedded"], ["single"],
          ["marry", "marriage"],
          ["已婚的：名字已经在那张纸上的状态"],
          "marry（结婚）+ -ed → 已经并成一户的"),
        W("marital", "maritus", "adjective", "/ˈmærɪtl/",
          "marit（配偶）+ -al（…的）→ 与婚姻有关的",
          "拉丁语 maritalis（属于配偶的）← maritus（配偶）",
          "relating to marriage or to being married",
          "belonging to what that one paper set up – 属于那张纸所立起来的那层关系",
          "表格上有一栏专问这一项，只能填其中一个选项",
          ["婚姻的", "夫妻的"],
          ["They discussed marital problems.", "Please state your marital status."],
          ["conjugal", "wedded"], [],
          ["marry", "marriage"],
          ["婚姻的/夫妻的：属于那纸所立起的那层关系"],
          "marit（配偶）+ -al → 与婚姻有关的"),
    ],
})

# ---------- medius（居中）----------
families.append({
    "root": {
        "id": "medius", "root": "medius", "variants": ["medi", "mean", "med"],
        "origin": "拉丁语 medius（居中的）；medianus 经古法语 moien 派出 mean 一支，"
                  "medialia（挂在中间的饰片）派出 medal",
        "core_concept": "the point standing between two ends / 站在两头之间的那一点",
        "core_image": "一根杆两头各压一物，手指在中间那点托住，杆不偏不倒",
        "english_definition": "middle, midway",
    },
    "concept": {
        "id": "concept-medius-middle", "concept": "the point standing between two ends",
        "chinese": "两头之间", "core_image": "杆两头各压一物，手指托在中间那点，杆不偏不倒",
        "root_ids": ["medius"], "word_ids": [],
    },
    "domain": "domain-shape",
    "words": [
        W("means", "medius", "noun", "/miːnz/",
          "medianus（居中的）→ 居于目的与人之间的那个中介 → 手段",
          "古法语 moiens（中介、方法）← 晚期拉丁语 medianus（居中的）← medius",
          "a method for achieving something; money and resources",
          "whatever stands between you and what you want – 横在人与所求之间、借它过去的那个",
          "河隔在中间，那条船就是过去的唯一凭借",
          ["手段", "方法", "财力"],
          ["Use any means necessary.", "They live beyond their means."],
          ["method", "resources"], [],
          ["meantime", "medal"],
          ["手段/方法：横在人与所求之间、借它达成的那个", "财力：同样是借以办事的那份凭借"],
          "medianus（居中）→ 居于人与所求之间的中介"),
        W("meantime", "medius", "noun", "/ˈmiːntaɪm/",
          "mean（居中）+ time（时候）→ 两件事之间那段时候",
          "英语复合词 mean＋time；mean ← 古法语 moien ← 拉丁语 medianus ← medius",
          "the period between two events",
          "the stretch that sits between one thing ending and the next starting – 一件事完与下一件起之间那一段",
          "前一场散了，后一场还没开，中间那阵子人都在门口站着",
          ["其间", "同时"],
          ["In the meantime, please wait here.", "He read a book in the meantime."],
          ["interval", "interim"], [],
          ["means", "medal"],
          ["其间/同时：一事完与下一事起之间那一段时候"],
          "mean（居中）+ time（时候）→ 两事之间那段时候"),
        W("medal", "medius", "noun", "/ˈmedl/",
          "medialia（挂在胸前正中的饰片）← medius（居中）→ 奖牌",
          "法语 médaille ← 意大利语 medaglia ← 通俗拉丁语 medalia ← 拉丁语 medius（居中）",
          "a flat piece of metal given as an award",
          "the disc hung at the middle of the chest for all to see – 挂在胸前正中、供人看见的那枚扁片",
          "带子从颈后绕过来，那枚圆片正落在胸口中间",
          ["奖牌", "勋章"],
          ["She won a gold medal.", "He wore his war medals."],
          ["award", "decoration"], [],
          ["means", "meantime"],
          ["奖牌/勋章：挂在胸前正中、供人看见的那枚扁片"],
          "medialia（挂在正中的饰片）← medius（居中）"),
    ],
})