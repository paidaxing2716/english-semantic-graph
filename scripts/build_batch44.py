#!/usr/bin/env python3
"""Generate batch44: 3 new roots (edere/tangere/peior) + 4 additions to existing roots.

HANDOFF 把 attain / edition / impair 分别归到 tain / edi(audire) / par 名下，
但按词源核查这三条都归错了，本批按真实词源另立词根：

  edition —— 非 audire（听）。来自 editio ← edere（ex＋dare，交出、发布）。
              且 vetted 的 edit 族（edit/editor/editorial）同出 edere，
              故合成一个 4 词族 edere-publish，一次清掉两个 vetted 族。
  attain  —— 非 tenere（握）。来自古法语 ataindre ← attingere（ad＋tangere，触及）。
              英语拼作 -tain 是后来与 contain/obtain 类推所致，词源另有出处，
              故新立 tangere 族（本批仅 attain 一员，HANDOFF 允许不凑满 3 词）。
  impair  —— 非 par（相等）。来自古法语 empeirier ← impejorare（in＋peior，变更坏）。
              pair/repair 属 par-equal 已入库，impair 另立 peior 族。

补词（挂已建模词根，其中 fluere / premere 由上一步迁移刚解锁）:
  fluere       ← flu
  premere      ← press
  scrib-script ← script
  ferre        ← reference

写法：W() 定参函数，漏字段直接 TypeError。Q12/Q1 自检前移到生成期，
因为 review.py check 不查 Q12，只有合并后的 validate.py 才查。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch44.json"


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

# ---------- edere-publish（交出、发布）----------
# 词根 id 特意带 -publish 后缀：拉丁语另有一个同形的 edere（吃），须区分。
families.append({
    "root": {
        "id": "edere-publish", "root": "edere", "variants": ["edit", "edi"],
        "origin": "拉丁语 edere（交出、发表），由 ex（出）＋ dare（给）合成，"
                  "过去分词 editus；拉丁语另有同形的 edere（吃）与此无关，"
                  "故本项目词根 id 加 -publish 后缀区分",
        "core_concept": "to give a thing out to the public / 把东西整治好、交出去给众人",
        "core_image": "一叠稿子经人逐页勾划删补，理齐了才递出门去",
        "english_definition": "to give out, put forth, publish",
    },
    "concept": {
        "id": "concept-edere-give-out", "concept": "to give a thing out to the public",
        "chinese": "整治交出", "core_image": "稿子逐页勾划删补，理齐了才递出门去",
        "root_ids": ["edere-publish"], "word_ids": [],
    },
    "domain": "domain-transfer",
    "words": [
        W("edit", "edere-publish", "verb", "/ˈedɪt/",
          "edere（交出、发布）→ 为交出去而先把文字勾划整治一遍",
          "英语 edit 由 editor 反向构词而来，源头是拉丁语 edere（交出、发表）",
          "to prepare written work for publication by correcting and cutting it",
          "working over a text so it is fit to be handed out – 把文字整治到可以交出去的程度",
          "红笔在稿子上圈掉一段，又在空白处补了两行",
          ["编辑", "校订", "剪辑"],
          ["She edits a weekly magazine.", "He edited the footage down to ten minutes."],
          ["revise", "correct"], [],
          ["editor", "edition"],
          ["编辑/校订：为交出去而整治文字", "剪辑：把影像同样整治成可交出的一版"],
          "edere（交出）→ 为交出去而先整治一遍"),
        W("editor", "edere-publish", "noun", "/ˈedɪtə(r)/",
          "edit（整治交出）+ -or（人）→ 负责整治并定稿交出的人",
          "拉丁语 editor（交出者、发表者），来自 edere",
          "a person who prepares and decides the content of a publication",
          "the one who works a text over and decides it may go out – 把稿子整治定稿、点头放行的人",
          "他把最后一页放下，签了字，稿子这才准许送印",
          ["编辑", "主编"],
          ["The editor rejected the article.", "She is editor of the local paper."],
          ["revise", "compile"], [],
          ["edit", "editorial"],
          ["编辑/主编：整治稿件并定稿放行的人"],
          "edit（整治交出）+ -or（人）→ 定稿放行的那个人"),
        W("editorial", "edere-publish", "adjective", "/ˌedɪˈtɔːriəl/",
          "editor（定稿人）+ -ial（…的）→ 属于定稿人立场的；名词指报社表态的那篇",
          "英语 editorial，来自 editor ← 拉丁语 edere",
          "relating to the editing of a publication; an article giving a paper's opinion",
          "belonging to the one who decides what goes out – 属于那位定稿放行者的",
          "头版下方那一栏不署名，说的是整家报社的立场",
          ["编辑的", "社论"],
          ["She joined the editorial team.", "The paper ran an editorial on the strike."],
          ["column", "commentary"], [],
          ["editor", "edit"],
          ["编辑的：属于定稿放行者职务的", "社论：由定稿方出面表态的那一篇"],
          "editor（定稿人）+ -ial → 属于定稿放行者的"),
        W("edition", "edere-publish", "noun", "/ɪˈdɪʃn/",
          "edere（交出、发布）+ -ition → 一次交出去的那一批，即某一版",
          "拉丁语 editio（发表、发行），来自 edere（交出）",
          "a particular issue or version of a book, paper, or broadcast",
          "one batch as it was given out that time – 那一回交出去的那一批",
          "扉页上印着第三回付印的字样，内容与头一回已有出入",
          ["版本", "版次", "一期"],
          ["This is the second edition of the book.", "The evening edition sold out."],
          ["version", "issue"], [],
          ["edit", "editor"],
          ["版本/版次：某一回交出去的那一批", "一期：报刊按次交出的其中一份"],
          "edere（交出）+ -ition → 一次交出去的那一批"),
    ],
})

# ---------- tangere（触及）----------
families.append({
    "root": {
        "id": "tangere", "root": "tangere", "variants": ["tain", "tact", "ting"],
        "origin": "拉丁语 tangere（触、碰到），过去分词 tactus；attingere（ad＋tangere）"
                  "表「伸手够到」，经古法语 ataindre 成英语 attain。"
                  "英语拼作 -tain 是后来与 contain/obtain 类推所致，源头与 tenere（握）另有分别",
        "core_concept": "to reach far enough to touch a thing / 伸出去，刚好碰到那一点",
        "core_image": "指尖向上伸，最后一寸终于搭上了崖沿",
        "english_definition": "to touch, reach",
    },
    "concept": {
        "id": "concept-tangere-touch", "concept": "to reach far enough to touch a thing",
        "chinese": "伸手触及", "core_image": "指尖向上伸，最后一寸搭上了崖沿",
        "root_ids": ["tangere"], "word_ids": [],
    },
    "domain": "domain-hold",
    "words": [
        W("attain", "tangere", "verb", "/əˈteɪn/",
          "at-（ad- 靠向）+ tain（触及）→ 一路伸手过去，终于够到",
          "古法语 ataindre，来自拉丁语 attingere（触及）← ad＋tangere（触）；"
          "英语拼作 -tain 受 contain/obtain 类推影响，词源仍在 tangere 一支",
          "to succeed in reaching or achieving something after effort",
          "stretching until the fingers finally close on it – 一直伸，直到指尖终于搭上",
          "指尖一寸寸往上探，最后扣住了崖顶那道边沿",
          ["达到", "获得", "实现"],
          ["She attained the rank of captain.", "Few attain such skill so young."],
          ["achieve", "reach"], ["fail"],
          ["contain", "obtain"],
          ["达到/实现：一路伸手过去终于够到", "获得：够到之后归入自己手里"],
          "at-（靠向）+ tain（触及）→ 伸手过去终于够到"),
    ],
})

# ---------- peior（更坏）----------
families.append({
    "root": {
        "id": "peior", "root": "peior", "variants": ["pair", "pejor"],
        "origin": "拉丁语 peior（更坏的，malus 的比较级），晚期拉丁语 impejorare（使变更坏）"
                  "经古法语 empeirier 成英语 impair；与 par（相等）一支的 pair/repair 无关",
        "core_concept": "to make a thing worse than it was / 把原本好的弄得更差一层",
        "core_image": "一块完好的板子被磕出缺口，往后每次用都差一点",
        "english_definition": "worse, to worsen",
    },
    "concept": {
        "id": "concept-peior-worsen", "concept": "to make a thing worse than it was",
        "chinese": "变得更坏", "core_image": "完好的板子被磕出缺口，往后每次用都差一点",
        "root_ids": ["peior"], "word_ids": [],
    },
    "domain": "domain-force",
    "words": [
        W("impair", "peior", "verb", "/ɪmˈpeə(r)/",
          "im-（in- 使）+ pair（更坏）→ 使某物比原先更差 → 损害",
          "古法语 empeirier，来自晚期拉丁语 impejorare（使变坏）← in＋peior（更坏）；"
          "与 pair（一对，来自 par 相等）不同源",
          "to weaken or damage something, especially a faculty or ability",
          "knocking a sound thing down a notch so it works less well – 把本来好的磕掉一层，从此不如原先",
          "完好的板面被磕出一道缺口，再用就总差着那一点",
          ["损害", "削弱", "使受损"],
          ["Loud noise can impair your hearing.", "Fatigue impaired his judgement."],
          ["weaken", "damage"], ["improve", "enhance"],
          ["pair", "repair"],
          ["损害/削弱：把本来好的弄差一层", "使受损：功能被磕缺后不如原先"],
          "im-（使）+ pair（更坏）→ 使之比原先更差"),
    ],
})

# ================= 补词：挂已建模词根 =================
# fluere / premere 两根刚由 scripts/migrate_root_ids_latin.py 从 flu / press
# 改名，自环边限制解除，flu 与 press 两词才得以入库。
additions = [
    W("flu", "fluere", "noun", "/fluː/",
      "influenza 的截短：in-（进入）+ flu（流）→ 流进体内的那股病气",
      "英语 flu 是意大利语 influenza 的截短形；influenza ← 拉丁语 influentia "
      "← influere（in＋fluere 流入），旧时以为疾病由星辰之气「流入」人身",
      "a common illness caused by a virus, with fever and aching",
      "the sickness once thought to flow into the body from outside – 旧时认为自外流进体内的那股病气",
      "一屋子人接连倒下，像有什么顺着空气淌进了身体",
      ["流感", "流行性感冒"],
      ["She caught the flu last winter.", "Half the office is off with flu."],
      ["influenza", "illness"], [],
      ["influence", "fluent"],
      ["流感/流行性感冒：旧说自外流进体内的那股病气"],
      "influenza 截短 → in-（进入）+ flu（流）→ 流进体内的病气"),
    W("press", "premere", "verb / noun", "/pres/",
      "premere（压、按）→ 用力压下去；引申为压印出版的那一行，即报界",
      "古法语 presser，来自拉丁语 pressare ← premere（压、按）",
      "to push firmly on something; also newspapers and journalists collectively",
      "bearing down on a thing with steady force – 稳稳使力压在物上",
      "掌根压在纸面上，油墨透过版子印了上去；报馆的机器整夜这样压着",
      ["按", "压", "报界", "新闻界"],
      ["Press the button to start.", "The press gathered outside the court."],
      ["push", "squeeze"], [],
      ["pressure", "impress"],
      ["按/压：稳稳使力压在物上", "报界/新闻界：靠压印机器出版的那一行"],
      "premere（压、按）→ 使力压下；压印成版即报界"),
    W("script", "scrib-script", "noun", "/skrɪpt/",
      "scribere（写、刻画）的过去分词 scriptum → 写下来的那份文字",
      "拉丁语 scriptum（写成之物），scribere（写）的过去分词中性形",
      "the written text of a play or film; a system of writing",
      "the thing as it stands written down – 已经写下来、定在纸面上的那份",
      "演员手里那几页纸被翻得起了毛边，台词全在上面",
      ["剧本", "脚本", "字体"],
      ["He is writing a film script.", "The inscription uses an ancient script."],
      ["screenplay", "text"], [],
      ["describe", "manuscript"],
      ["剧本/脚本：写下来供照着演的那份文字", "字体：文字写下来所用的那套形体"],
      "scribere（写）的过去分词 → 已写下定在纸面的那份"),
    W("reference", "ferre", "noun", "/ˈrefrəns/",
      "re-（回）+ fer（带）+ -ence → 把话头带回某处去 → 提及、依据",
      "英语 reference 来自 refer ← 拉丁语 referre（带回、归于）← re＋ferre（带）",
      "a mention of something; a source consulted; a letter about someone's ability",
      "carrying the matter back to the place it came from – 把话头带回它的出处",
      "他讲到一半停下，翻回书后那一栏，指着出处给人看",
      ["提及", "参考", "推荐信"],
      ["She made no reference to the delay.", "Please list your references at the end."],
      ["mention", "source"], [],
      ["refer", "transfer"],
      ["提及：把话头带到某处", "参考：把话头带回出处去核对", "推荐信：把某人来历带回给对方看的那封"],
      "re-（回）+ fer（带）→ 把话头带回它的出处"),
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

assert len(words) == 10, len(words)
assert len(roots) == 3, len(roots)
assert len({r["id"] for r in roots}) == 3, "新词根 id 有重复"

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words "
      f"({len(words) - len(additions)} family + {len(additions)} additions), "
      f"{len(roots)} new roots")

