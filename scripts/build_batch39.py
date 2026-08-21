#!/usr/bin/env python3
"""Generate batch39: three new roots (cep/vid/caedere) + absorption.

词源核查结论（子代理核实）：
- cep（capere 抓取）：accept ← ad+capere。收 acceptable/acceptance，
  后续把 concept/except/receipt/susceptible/accept 从 fac 迁入（迁移脚本另做）。
- vid（videre 看）：envisage ← en+visage ← videre。envisage 归 vid。
- caedere（切砍）：precise ← praecidere ← caedere。precise 归 caedere。

本批吸收 5 新词：acceptable, acceptance（→cep）、envisage（→vid）、
precise（→caedere）。
exception/exceptional/reception 已在 HANDOFF B 类清单（cep 族）——
但 verify 词汇量，先查它们是否已在库。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch39.json"


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


families = [
    # ---------- cep（capere 抓取）----------
    {
        "root": {
            "id": "cep", "root": "cep", "variants": ["cep", "capt", "cept", "cap"],
            "origin": "拉丁语 capere（抓取、拿住、接收）",
            "core_concept": "to grasp, to take hold and receive / 一把抓住、接过来",
            "core_image": "手探出去，把飞来的球一把接住握住",
            "english_definition": "to take, to grasp, to receive",
        },
        "concept": {
            "id": "concept-cep-grasp", "concept": "to grasp and take in, holding what comes",
            "chinese": "抓取接收", "core_image": "伸手一把接住飞来的球",
            "root_ids": ["cep"], "word_ids": [],
        },
        "domain": "domain-hold",
        "words": [
            W("acceptable", "cep", "adjective", "/əkˈseptəbl/",
              "ac-（ad- 朝向）+ cept（抓取）+ -able（可…的）→ 能接过来、收得下的 → 可接受的",
              "拉丁语 acceptabilis：ad-（朝向）+ capere（抓取）",
              "good enough to be accepted or agreed to",
              "fit to be taken in without complaint – 值得收下、不会皱眉的",
              "对方开出的条件摆到桌上，掂量一番觉得能收下就点头",
              ["可接受的", "可容忍的"],
              ["The offer is acceptable to both sides.", "His behavior was barely acceptable."],
              ["satisfactory", "reasonable"], ["unacceptable"],
              ["accept", "acceptance", "reception"],
              ["可接受：收得下、不皱眉","可容忍：勉强算过得去"],
              "ac-（朝向）+ cept（抓取）+ -able → 收得下的"),
            W("acceptance", "cep", "noun", "/əkˈseptəns/",
              "ac-（朝向）+ cept（抓取）+ -ance（名词）→ 接过来的动作或状态 → 接受",
              "accept 的名词：ad-（朝向）+ capere（抓取）",
              "the act of taking something offered; approval",
              "taking what is offered into one's hand – 把递过来的东西接住",
              "老师傅看了一眼递来的方案，点点头接了过去",
              ["接受", "认可"],
              ["Her acceptance of the job delighted us.", "The idea gained wide acceptance."],
              ["approval", "adoption"], ["rejection"],
              ["accept", "acceptable", "reception"],
              ["接受：把递来的接住","认可：众人愿意收下"],
              "ac-（朝向）+ cept（抓取）+ -ance → 接过来"),
            W("exception", "cep", "noun", "/ɪkˈsepʃn/",
              "ex-（向外）+ cept（抓取）+ -ion → 从整体里被抓出去的那一项 → 例外",
              "拉丁语 exceptio：ex-（向外）+ capere（抓取）",
              "something that does not follow the usual rule",
              "the item taken out from the whole – 从整体里被抓出来单独放的一项",
              "全班都穿了校服，独独有个人没穿，那份不同就是它",
              ["例外", "除外"],
              ["Everyone came, with few exceptions.", "Without exception, the rules apply."],
              ["anomaly", "outlier"], [],
              ["except", "exceptional", "acceptable"],
              ["例外：被抓出去单放的一项","除外：从规则里摘出去"],
              "ex-（向外）+ cept（抓取）+ -ion → 被抓出的例外"),
            W("exceptional", "cep", "adjective", "/ɪkˈsepʃənl/",
              "exception（例外）+ -al → 超出常例的 → 杰出的/异常的",
              "exceptio 的形容词",
              "unusually good; out of the ordinary",
              "standing outside the common run – 立在常例之外、超出寻常",
              "别人都画三小时，她半小时就完成还最精致，明显不在一个水平线上",
              ["杰出的", "异常的"],
              ["She is an exceptional student.", "The results were exceptional."],
              ["extraordinary", "outstanding"], ["ordinary"],
              ["exception", "except", "reception"],
              ["杰出：超出常例的好","异常：与通常不同的"],
              "exception（例外）+ -al → 超乎常例"),
            W("reception", "cep", "noun", "/rɪˈsepʃn/",
              "re-（往回）+ cept（抓取）+ -ion → 把来客接过来的动作 → 接待；接受到的信息",
              "拉丁语 receptio：re-（往回）+ capere（抓取）",
              "the act of welcoming someone; the way a signal is received",
              "taking the arriving one in – 把到来的人(物)接进来",
              "酒店前台，来人一进门先被接住、办入住，行李也在这里被安顿",
              ["接待", "接收", "反响"],
              ["The reception was warm.", "Radio reception is poor here."],
              ["welcome", "admission"], [],
              ["except", "accept", "exceptional"],
              ["接待：把来客接进来","接收：把信号接进来","反响：外界如何接收它"],
              "re-（往回）+ cept（抓取）+ -ion → 把来客接过来"),
        ],
    },
    # ---------- vid（videre 看）----------
    {
        "root": {
            "id": "vid", "root": "vid", "variants": ["vid", "vis", "vey"],
            "origin": "拉丁语 videre（看、看见）",
            "core_concept": "to see, to look / 看、看见",
            "core_image": "目光落在某处，把那东西看进眼里",
            "english_definition": "to see, to view",
        },
        "concept": {
            "id": "concept-vid-see", "concept": "to see and take in with the eyes",
            "chinese": "看见", "core_image": "目光落定，把那物看进眼里",
            "root_ids": ["vid"], "word_ids": [],
        },
        "domain": "domain-perceive",
        "words": [
            W("envisage", "vid", "verb", "/ɪnˈvɪzɪdʒ/",
              "en-（使）+ vis（看）+ -age → 使它在眼前显现 → 设想",
              "法语 envisager：en-（在内）+ visage（面容）← visio ← videre（看）",
              "to imagine or picture something as likely to happen",
              "seeing it take shape before the eyes – 在眼前把它看成形",
              "脑子里已经把那座桥建起来的样子放了一遍，连桥上走车的画面都有",
              ["设想", "想象", "展望"],
              ["We envisage a bright future.", "The plan envisages a new library."],
              ["imagine", "foresee"], [],
              ["invisible", "advisable"],
              ["设想/展望：在眼前把将来看成形"],
              "en-（使）+ vis（看）+ -age → 在眼前显现 → 设想"),
        ],
    },
    # ---------- caedere（切砍）----------
    {
        "root": {
            "id": "caedere", "root": "caedere", "variants": ["caed", "caes", "cis", "cid"],
            "origin": "拉丁语 caedere（切、砍、斩断）",
            "core_concept": "to cut, to strike off / 切、砍、斩断",
            "core_image": "一刀落下，把整块东西齐齐切开",
            "english_definition": "to cut, to strike off",
        },
        "concept": {
            "id": "concept-caedere-cut", "concept": "to cut through cleanly",
            "chinese": "切砍", "core_image": "一刀落下，整块齐齐切开",
            "root_ids": ["caedere"], "word_ids": [],
        },
        "domain": "domain-force",
        "words": [
            W("precise", "caedere", "adjective", "/prɪˈsaɪs/",
              "pre-（预先）+ cis（切）→ 预先切定、分毫不差的 → 精确的",
              "拉丁语 praecisus：prae-（预先）+ caedere（切）——'预先切定'",
              "exact and accurate, with no error",
              "cut in advance to the exact mark – 预先切到那条准线上",
              "木匠在木料上先画好线，下刀正落线心，不偏一丝",
              ["精确的", "准确的"],
              ["The measurements must be precise.", "Give me the precise figures."],
              ["exact", "accurate"], ["vague", "approximate"],
              ["exact", "accurate", "precede"],
              ["精确：预先切定到准线"],
              "pre-（预先）+ cis（切）→ 切到准线 → 精确"),
        ],
    },
]

roots = [dict(f["root"]) for f in families]
concepts = [dict(f["concept"]) for f in families]
domain_add = {}
for f in families:
    domain_add.setdefault(f["domain"], []).append(f["root"]["id"])

words = []
for fam in families:
    words.extend(fam["words"])

OUT.write_text(json.dumps({
    "roots": roots,
    "concepts": concepts,
    "domain_add": domain_add,
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(words)} words, {len(roots)} new roots")
