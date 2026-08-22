#!/usr/bin/env python3
"""Generate batch53: 日耳曼核心词样品 12 个——不拆词根，只给画面。

【为什么这批不拆】
项目的核心是「概念 + 核心画面」，词根只是通往它的一条路，不是唯一那条。
日耳曼核心词本身就是词根，硬拆等于编词源（质量门 Q11 明确拒绝）。
库里已有 choose/pick/miss 三词走这条路：root_ids 留空、root_logic 留空，
但 core_concept / core_image / chinese / examples / semantic_expansions 一样不缺，
miss 的三个义项（未击中/错过/思念）就被同一个「指尖擦空」的画面串起来。

本批照这个模式做，验证它对成批日耳曼词同样成立。

【字段口径】
review.py 第 172 行会拦「标为不可拆却写了 root_logic」，故 root_logic 必须留空；
root_ids 同理留空。validate 的 REQUIRED_WORD_FIELDS 仍要求
id/word/pos/phonetic/origin/native_definition/core_concept/core_image/chinese/examples。
decomposable_note 用来说明「为什么不拆」，即词源到此为止。

Q12 只查 decomposable=="root" 的词，本批不受约束；但 core_image 是这类词
唯一的记忆抓手，仍主动避开本词任一中文义项（长度≥2），保证回想模式可用。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_pipeline" / "batch53.json"


def G(wid, pos, ph, origin, note, native, concept, image, zh, ex, syn, ant, exp):
    """日耳曼核心词：不拆词根，故 root_ids / root_logic 留空。"""
    return {
        "id": wid, "word": wid, "pos": pos, "phonetic": ph,
        "decomposable": "germanic", "decomposable_note": note,
        "root_ids": [], "root_logic": "",
        "origin": origin, "native_definition": native,
        "core_concept": concept, "core_image": image,
        "chinese": zh, "examples": ex,
        "synonyms": syn, "antonyms": ant, "related": [],
        "semantic_expansions": exp,
    }


words = [
    G("seed", "noun", "/siːd/",
      "古英语 sæd，来自原始日耳曼语 *sēdiz（撒下之物），与 sow（播种）同源",
      "日耳曼核心词，本身即词根，无拉丁词缀可拆",
      "the small hard part of a plant from which a new plant grows",
      "the small dry thing that holds a whole plant folded inside – 一粒干硬的小东西，里头折着一整株",
      "一粒干瘪的小东西落进土缝，几天后顶开土冒出两片嫩芽",
      ["种子", "籽", "起因"],
      ["Plant the seeds in early spring.", "That meeting sowed the seeds of change."],
      ["grain", "kernel"], [],
      ["种子/籽：里头折着一整株的那粒小东西", "起因：一件事最初那粒、后来长成全局的东西"]),
    G("bird", "noun", "/bɜːd/",
      "古英语 bridd（雏鸟），词源不明，非拉丁借词",
      "日耳曼核心词，古英语 bridd 之后再无更早可考，无词根可拆",
      "a creature with feathers and wings that can usually fly",
      "the light thing on the branch that leaves before your hand arrives – 枝上那个轻东西，手还没到它已经走了",
      "枝头一动，那团轻飘飘的东西已经蹿到另一棵树上",
      ["鸟", "禽"],
      ["A small bird landed on the sill.", "Birds fly south in autumn."],
      ["fowl", "creature"], [],
      ["鸟/禽：带羽有翅、手还没伸到就飞开的那类活物"]),
    G("tool", "noun", "/tuːl/",
      "古英语 tōl，来自原始日耳曼语 *tōwlam（用来做事的器具），与 taw（加工）同源",
      "日耳曼核心词，本身即词根，无拉丁词缀可拆",
      "a device held in the hand and used to do a particular job",
      "the handle worn smooth by the palm that keeps reaching for it – 被同一只手掌磨得发亮的那根柄",
      "柄上那一处被手心磨得发亮，一摸就知道用了多少年",
      ["工具", "用具", "手段"],
      ["He put every tool back in the box.", "Language is a tool for thinking."],
      ["instrument", "device"], [],
      ["工具/用具：握在手里用来做活的器械", "手段：把某物当器械使的那种用法"]),
    G("breath", "noun", "/breθ/",
      "古英语 bræþ（气味、呼出的热气），来自原始日耳曼语 *brēthaz（热气）",
      "日耳曼核心词，本义是「呼出的热气」，无拉丁词缀可拆",
      "the air taken into and let out of the lungs",
      "the white cloud that shows on cold glass and then fades – 冷玻璃上现出的那团白，一会儿又散了",
      "冷玻璃上凑近一呵，现出一团白，转眼淡下去",
      ["呼吸", "气息", "一口气"],
      ["Take a deep breath and relax.", "She was out of breath after the climb."],
      ["air", "puff"], [],
      ["呼吸/气息：吸进吐出的那股气", "一口气：一次吐纳的分量"]),
    G("brain", "noun", "/breɪn/",
      "古英语 brægen，来自原始日耳曼语 *bragnam，与希腊语 brekhmos（前额）或有远亲关系",
      "日耳曼核心词，无拉丁词缀可拆",
      "the organ inside the head that controls thought and feeling",
      "the folded grey thing inside the skull where everything gets decided – 颅骨里那团盘着褶子的东西，事都在那儿定",
      "颅骨掀开，里头那团盘满褶子的东西还温着",
      ["大脑", "头脑", "智力"],
      ["The brain uses a fifth of our energy.", "Use your brain before you answer."],
      ["mind", "intellect"], [],
      ["大脑：颅骨里那个器官", "头脑/智力：用它想事的那份能力"]),
    G("throat", "noun", "/θrəʊt/",
      "古英语 þrote，来自原始日耳曼语 *thrut-（肿起、鼓起的部位）",
      "日耳曼核心词，本义指颈前鼓起处，无拉丁词缀可拆",
      "the passage at the front of the neck through which food and air pass",
      "the place that moves once when you swallow – 咽下去时鼓一下的那个地方",
      "水咽下去，颈前那处鼓一下又落回原样",
      ["喉咙", "嗓子", "咽喉"],
      ["He has a sore throat today.", "The words stuck in her throat."],
      ["gullet", "neck"], [],
      ["喉咙/咽喉：颈前供食物与空气通过的那条道", "嗓子：从这条道里发出的声音"]),
    G("shiver", "verb", "/ˈʃɪvə(r)/",
      "中古英语 chiveren，词源不确，可能与古英语 ceafl（颌）相关，形容牙关打战",
      "日耳曼核心词，词源到中古英语为止，无拉丁词缀可拆",
      "to shake slightly because of cold or fear",
      "the small fast shake that runs through you before you notice it – 一阵细而快的动，人还没反应它已经过去了",
      "风一穿过湿衣服，背上那阵细而快的动自己就起来了",
      ["颤抖", "发抖", "哆嗦"],
      ["She shivered in the cold rain.", "He shivered at the thought of it."],
      ["tremble", "quiver"], [],
      ["颤抖/发抖/哆嗦：因冷或怕而起的那阵细快的动"]),
    G("choke", "verb", "/tʃəʊk/",
      "古英语 ācēocian（塞住），来自原始日耳曼语，与 cheek（腮）或有关联",
      "日耳曼核心词，本义是「塞住气道」，无拉丁词缀可拆",
      "to be unable to breathe because the throat is blocked",
      "the moment the way in shuts and nothing gets past – 通道一下合上，什么也过不去那一刻",
      "一口卡在半途，脸涨红，手往喉前抓",
      ["窒息", "呛住", "堵塞"],
      ["He choked on a fish bone.", "Weeds choked the narrow stream."],
      ["suffocate", "clog"], [],
      ["窒息/呛住：气道被塞住、过不去气", "堵塞：同一个「塞住使不通」用在通道上"]),
    G("oath", "noun", "/əʊθ/",
      "古英语 āþ，来自原始日耳曼语 *aithaz（郑重之言）",
      "日耳曼核心词，本身即词根，无拉丁词缀可拆",
      "a formal promise, often made in public or in court",
      "the hand raised and held there while the words come out – 手举起来不放下，话就在那姿势里说出口",
      "他一手按在书上，另一手举着不放，一字一句说完",
      ["誓言", "宣誓", "咒骂"],
      ["She took an oath to tell the truth.", "He muttered an oath under his breath."],
      ["vow", "pledge"], [],
      ["誓言/宣誓：郑重当众说定的那番话", "咒骂：借神明之名出口的那种话，同源另一支用法"]),
    G("fool", "noun", "/fuːl/",
      "古法语 fol（疯子、小丑）← 晚期拉丁语 follis（风箱、空袋），但英语已不作词根用",
      "词源虽可溯至拉丁 follis（空袋），但英语中 fool 已无同族词可迁移，按不可拆处理",
      "a person who behaves in a silly or unwise way",
      "the one everyone else has already seen through, still going – 旁人早看穿了、他还在往下演的那个",
      "满屋人都憋着笑，只有他还认真往下说",
      ["傻瓜", "愚人", "上当者"],
      ["Do not be a fool about money.", "They made a fool of him."],
      ["idiot", "clown"], ["sage"],
      ["傻瓜/愚人：行事不明智、被旁人看穿的那个", "上当者：因此被人耍了的那个"]),
    G("hawk", "noun", "/hɔːk/",
      "古英语 hafoc，来自原始日耳曼语 *habukaz（猛禽）",
      "日耳曼核心词，本身即词根，无拉丁词缀可拆",
      "a bird of prey with sharp eyes and curved claws",
      "the shape that hangs still high up, then drops all at once – 高处悬着不动的那个影子，忽然一头扎下来",
      "高处那影子悬了半天不动，一收翅直扎下去",
      ["鹰", "隼", "主战派"],
      ["A hawk circled above the field.", "The hawks in cabinet urged action."],
      ["falcon", "raptor"], ["dove"],
      ["鹰/隼：目锐爪弯、悬空俯冲的猛禽", "主战派：政见上像它一样主张下扑的那些人"]),
    G("dusk", "noun", "/dʌsk/",
      "古英语 dox（暗色的），来自原始日耳曼语 *dusk-（发暗）",
      "日耳曼核心词，本义是「转暗」，无拉丁词缀可拆",
      "the time of day when the light is nearly gone",
      "the hour you stop being able to tell colours apart – 到这会儿，颜色彼此就分不出来了",
      "屋里没开灯，书页上的字一行行糊成一片",
      ["黄昏", "暮色", "薄暮"],
      ["The lamps come on at dusk.", "They walked home in the dusk."],
      ["twilight", "nightfall"], ["dawn"],
      ["黄昏/暮色/薄暮：光将尽、颜色分不出来的那一段时候"]),
]

# ---- 生成期自检 ----
for w in words:
    assert w["decomposable"] == "germanic"
    assert w["root_ids"] == [] and w["root_logic"] == "", \
        f"{w['id']}: germanic 词的 root_ids/root_logic 必须留空（review.py 会拦）"
    assert w.get("decomposable_note"), f"{w['id']}: 缺 decomposable_note（说明为何不拆）"
    # Q12 对 germanic 不生效，但 core_image 是这类词唯一的记忆抓手，仍不许点名义项
    for zh in w["chinese"]:
        assert not (len(zh) >= 2 and zh in w["core_image"]), \
            f"{w['id']}: core_image 点名义项「{zh}」，遮罩后就没提示了"
    if len(w["chinese"]) >= 2:
        assert w["semantic_expansions"], f"Q1：{w['id']} 多义却无 semantic_expansions"
    assert len(w["examples"]) >= 2, f"{w['id']} 例句不足 2 条"

assert len({w["id"] for w in words}) == len(words), "词条 id 有重复"

OUT.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=2) + "\n",
               encoding="utf-8")
print(f"wrote {OUT}: {len(words)} 个日耳曼核心词（不拆词根，只给画面）")
