#!/usr/bin/env python3
"""构建生成提示词：从现有人工词条里抽 few-shot 范例 + schema 约束。

不联网、不调模型，纯文本处理，可单独测试。
生成的提示词交给 word_analyzer.py 调模型，或直接贴给任意对话模型。
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# 与 tests/validate.py 的 REQUIRED_WORD_FIELDS 保持一致
REQUIRED = ["id", "word", "pos", "phonetic", "root_ids", "root_logic", "origin",
            "native_definition", "core_concept", "core_image", "chinese", "examples"]
OPTIONAL = ["synonyms", "antonyms", "related", "semantic_expansions",
            "synonym_group", "synonym_note", "decomposable"]

SCHEMA_RULES = """字段规则（违反任何一条该词条都会被质量门拒绝）：

必填：id, word, pos, phonetic, decomposable, origin,
      native_definition, core_concept, core_image, chinese, examples
仅 decomposable="root" 时必填：root_ids, root_logic
可选：synonyms, antonyms, related, semantic_expansions, synonym_group, synonym_note

硬性约束：
0. decomposable 必须如实填写，取值之一：
   - root          确由拉丁/希腊词根派生，且该词根在下方清单里
   - root_pending  确可拆，但所属词根尚未在本项目建模 → root_ids 留空、不写 root_logic
   - germanic      日耳曼核心词，本身即词根（如 choose 来自古英语 ceosan）
   - loanword      借词/专名，拆解无认知价值
   - phrasal       短语动词，意义在介词的空间隐喻里
   - opaque        词源不明或无法有效拆解
   非 root 型必须把 root_ids 留空、不写 root_logic。
   **词源对不上就如实改标，绝不能硬安一个词根。**
   反面案例：seclude 来自 claudere（关闭），与 ducere（引导）不同源，
   却被挂到 duc 词根下，还在 root_logic 里写"注意此处词源不同，按…理解"——
   这种自己都承认推导不成立还硬挂的写法会被直接拒绝。
1. id 用单词本身的小写形式，全局唯一。
2. phonetic 必须以 / 开头结尾，IPA 格式，例如 /kənˈfɪɡjər/。
3. root_ids 只能引用下面列出的已有词根 id，不要发明新词根。
4. related 只能引用已存在于词库的词条 id（清单见下）。
   宁可留空数组，也不要指向词库里没有的词——那会在图谱上产生点不开的死链。
5. synonyms / antonyms 必须是真实存在的英语词。
   绝对不要用"前缀 + 已知词"的方式造词。
   反面案例：configure 的反义写成 disconfigure（该词不存在）。
   想不出真实反义词就留空数组 []，留空不算缺陷。
6. chinese 是中文表达数组，属于输出层。它不是入口——先有英文概念，中文只是落地译法。
7. examples 至少 1 条真实语境句子，能体现 core_concept。
8. 若 chinese 有 2 个及以上义项，semantic_expansions 必须至少 1 条，
   解释这些义项为何共享同一个核心概念（不能只列义项不解释）。
   若是真正词义分叉的多义词（如 figure 数字/人物/理解），至少 2 条。
9. core_concept 要能解释该词的所有义项，是一句概括而非翻译。
10. core_image 是一个具体可视的画面/场景，不要复述 core_concept。
11. root_logic 说明"词根 + 词缀 → 为什么是这个词义"的推导过程。
    不要写"XX 就是 XX"式的同义反复。若该词的词义与词根只是间接相关，
    要如实说明是间接引申，不要硬凑。
"""


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def build(targets, n_examples=3):
    """targets: [(word, root_id), ...] 要生成的词及其归属词根。"""
    roots = load("roots.json")["roots"]
    words = load("words.json")["words"]

    root_by_id = {r["id"]: r for r in roots}
    existing_ids = sorted(w["id"] for w in words)

    # few-shot：优先选目标词根下的现有词条，最贴近待生成词的语感
    target_roots = {rid for _, rid in targets}
    same_root = [w for w in words if set(w["root_ids"]) & target_roots]
    others = [w for w in words if w not in same_root]
    # 优先挑带 semantic_expansions 的，示范"多义如何解释"
    same_root.sort(key=lambda w: -len(w.get("semantic_expansions") or []))
    others.sort(key=lambda w: -len(w.get("semantic_expansions") or []))
    examples = (same_root + others)[:n_examples]

    lines = []
    lines.append("你在为一个英语概念图谱生成词条。这个项目的核心理念是：")
    lines.append("英文单词 ≠ 中文翻译，而是 核心概念(Concept) + 核心画面(Core Image) + 语境(Context)。")
    lines.append("中文是输出层，不是入口。词条要让学习者像母语者那样理解概念，而不是背中文对应词。\n")

    lines.append("## 可用词根")
    for rid in sorted(target_roots):
        r = root_by_id[rid]
        lines.append(f"- {rid}: {r['core_concept']} | 词源 {r['origin']} | 核心画面 {r['core_image']}")
    lines.append("")

    lines.append("## 词库现有词条 id（related 只能引用这些）")
    lines.append(", ".join(existing_ids))
    lines.append("")

    lines.append("## " + SCHEMA_RULES.split("\n", 1)[0])
    lines.append(SCHEMA_RULES.split("\n", 1)[1])

    lines.append("## 合格词条范例")
    for w in examples:
        keep = {k: w[k] for k in REQUIRED + OPTIONAL if k in w}
        lines.append(json.dumps(keep, ensure_ascii=False, indent=2))
        lines.append("")

    lines.append("## 现在生成以下词条")
    for word, rid in targets:
        lines.append(f"- {word}（归属词根 {rid}）")
    lines.append("")
    lines.append('只输出 JSON，格式为 {"words": [...]}，不要任何解释文字或 markdown 代码块标记。')

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="构建词条生成提示词")
    ap.add_argument("targets", nargs="+", help="格式 word:root_id，如 depress:press")
    ap.add_argument("-o", "--out", help="写入文件；默认打印到 stdout")
    ap.add_argument("-n", "--examples", type=int, default=3, help="few-shot 范例数量")
    a = ap.parse_args()

    parsed = []
    for t in a.targets:
        if ":" not in t:
            raise SystemExit(f"格式错误：{t}，应为 word:root_id")
        word, rid = t.split(":", 1)
        parsed.append((word, rid))

    text = build(parsed, a.examples)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"已写入 {a.out}（{len(text)} 字符）")
    else:
        print(text)
