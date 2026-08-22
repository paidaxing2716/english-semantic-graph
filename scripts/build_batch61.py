#!/usr/bin/env python3
"""Generate batch61: 6 新词根 + 19 补词。

新根（各族在考研词表内均有 3 个以上成员）：
  putare（算、估）    compute / count / discount / dispute / deputy
  fallere（使失足）   fail / failure / false / fault / faulty
  densus（稠密）      dense / density / condense
  discus（圆盘）      disc / dish / desk
  phainein（显现）    emphasis / fantasy / fancy
  fatum（所言定数）   fate / fatal / fairy

补进已建模根（含两处「同根不同拉丁词形」的纠正）：
  plic  ← employ / employee / employer / exploit
        子代理报作新根 plicare，但 plic 的 origin 就写 plicare，是同一个根
  ag    ← embassy / essay / exam
        同理，子代理报作 agere，而 ag 的 origin 已写 agere
  habere ← enable / disable / endeavor    dare ← endow / dose
  legere ← elite       integer ← entire   cura ← ensure
  liber ← deliver / delivery              plic ← display
  gradus ← degree      sidus ← desire     spirare ← expire
  cernere ← discreet   charta ← discard   serere ← exert
  fidere ← defy

写法：W() 定参函数。Q12/Q1 自检与自环断言均在生成期。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch61.json"


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

# ---------- putare（算、估）----------
families.append({
    "root": {
        "id": "putare", "root": "putare", "variants": ["put", "pute", "count"],
        "origin": "拉丁语 putare（修剪，引申为清点、估算）；computare（com＋putare 合起来算）"
                  "经古法语 conter 派出 count 一支",
        "core_concept": "reckoning a thing up to settle what it comes to / 把东西点算一遍，定出它算多少",
        "core_image": "手指点着桌上的钱一枚枚过，嘴里跟着报数",
        "english_definition": "to prune, reckon, estimate",
    },
    "concept": {
        "id": "concept-putare-reckon", "concept": "reckoning a thing up to settle what it comes to",
        "chinese": "点算估定", "core_image": "手指点着桌上的钱一枚枚过，嘴里跟着报数",
        "root_ids": ["putare"], "word_ids": [],
    },
    "domain": "domain-perceive",
    "words": [
        W("count", "putare", "verb", "/kaʊnt/",
          "com-（合起来）+ put（算）→ computare（合算）经古法语 conter → 一个个点过",
          "古法语 conter ← 拉丁语 computare（合算）← com＋putare（清点）",
          "to say numbers in order; to find the total of things",
          "going over items one by one so none is passed twice – 一件件点过去，不重不漏",
          "他指着一排箱子挨个点，点到哪儿手就停在哪儿",
          ["数", "计数", "算作"],
          ["She counted the coins twice.", "Every vote counts here."],
          ["number", "tally"], [],
          ["compute", "discount"],
          ["数/计数：一件件点过去定出总数", "算作：把某物点进这一类里"],
          "com-（合起来）+ put（算）→ 一个个点过"),
        W("compute", "putare", "verb", "/kəmˈpjuːt/",
          "com-（合起来）+ pute（算）→ 把各项合起来算出结果",
          "拉丁语 computare（合算）← com＋putare（清点、估算）",
          "to calculate an answer using numbers",
          "putting all the parts together to get one figure – 把各项合到一处，算出一个数",
          "各栏数字挨着加下来，最后一格填出总数",
          ["计算", "算出"],
          ["The program computes the average.", "He computed the cost in minutes."],
          ["calculate", "reckon"], [],
          ["count", "discount"],
          ["计算/算出：把各项合起来得出一个数"],
          "com-（合起来）+ pute（算）→ 合起来算出结果"),
        W("discount", "putare", "noun", "/ˈdɪskaʊnt/",
          "dis-（去掉）+ count（算）→ 从原数里算掉一部分 → 折扣",
          "古法语 desconter（扣除）← dis＋conter ← 拉丁语 computare",
          "an amount taken off the usual price; to treat as unimportant",
          "the part struck off the total before you pay – 付钱之前从总数里划掉的那一截",
          "标价被笔划掉，旁边写了个小些的数",
          ["折扣", "打折", "不予考虑"],
          ["They offered a ten percent discount.", "Do not discount her advice."],
          ["reduction", "rebate"], [],
          ["count", "compute"],
          ["折扣/打折：从总数里算掉的那一截", "不予考虑：把某说法从考量里划掉"],
          "dis-（去掉）+ count（算）→ 从原数里算掉一部分"),
        W("dispute", "putare", "noun", "/dɪˈspjuːt/",
          "dis-（分开）+ pute（算）→ 各算各的、算不到一处 → 争执",
          "古法语 desputer ← 拉丁语 disputare（各自估算、辩论）← dis＋putare",
          "a disagreement or argument between sides",
          "two reckonings that will not come out the same – 两边各算一遍，算出来的数对不上",
          "两人各拿一张纸算同一笔账，末了数字差着一截",
          ["争执", "争论", "质疑"],
          ["The dispute lasted for months.", "Nobody disputes her skill."],
          ["quarrel", "argue"], ["agreement"],
          ["compute", "count"],
          ["争执/争论：各算各的、算不到一处", "质疑：不认对方那笔算法"],
          "dis-（分开）+ pute（算）→ 各算各的、对不上"),
        W("deputy", "putare", "noun", "/ˈdepjuti/",
          "de-（往下）+ put（派定）→ 被指派下来顶事的人 → 副职",
          "古法语 deputé ← 晚期拉丁语 deputare（指派）← de＋putare（估定、派定）",
          "a person given authority to act for someone else",
          "the one named to stand in when the first is away – 被点定、正主不在时顶上的那个",
          "名册上头一个名字底下写着第二个，正主不在就他签字",
          ["副手", "代理人", "议员"],
          ["The deputy signed in her absence.", "He was elected deputy last year."],
          ["assistant", "delegate"], [],
          ["compute", "count"],
          ["副手/代理人：被点定、正主不在时顶上的那个", "议员：受选派代表一方的那个"],
          "de-（往下）+ put（派定）→ 被指派顶事的人"),
    ],
})
