#!/usr/bin/env python3
"""切占位词条的派发批次，每词附上真实词源与现有画面。

    python scripts/cut_stub_batches.py --start 1 --n 2 --size 30

产出 drafts/sb_chunkNN.txt。每词一段，含：
  - pos 与 phonetic（已由 extract_phonetic_pos 补正，代理不要改）
  - 现有 core_image（1045 词已是真画面，必须沿用；模板的会标出来要求重写）
  - Wiktionary Etymology 段的原始 wikitext

【为什么要附原始 wikitext 而不是清洗过的】清洗会丢词形。实测把
`{{inh|en|enm|pamphilet}}` 按第二个参数抽取会得到语言码 `enm` 而不是词
`pamphilet`，plaster 的 emplastrum 也会整个丢掉——喂给代理的就是错信息，
而它没法察觉。原始标记 `{{der|en|la|emplastrum||a plaster, bandage}}` 人读得懂。

【为什么必须附词源】规格里「不许编造古英语词形」这条，光靠嘱咐挡不住：这批 1134 词
的 origin 全是生成器写的「英语词条 X，现代词义按整体记」，代理没有可参照的真词源就
只能猜。库里已因此有过编造词源的先例（medal 的「挂在胸前正中」）。
"""
import argparse
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "drafts" / ".etym_cache"
MAX_ETY = 700
# 图片与引文块占篇幅且无信息量（pamphlet 的 Etymology 段前 300 字全是 multiple images）
NOISE = re.compile(r"\{\{(?:multiple images|wikipedia|wp|swp|slim-wikipedia|picdic)[^}]*\}\}", re.S)


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def etymology(wid, english_section):
    p = CACHE / f"{wid}.txt"
    if not p.exists():
        return "（无缓存）"
    sec = english_section(p.read_text(encoding="utf-8", errors="replace"))
    blocks = []
    for m in re.finditer(r"===+\s*Etymology[^=]*===+\n(.*?)(?=^===|\Z)", sec, re.M | re.S):
        t = m.group(1)
        t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "", t)
        t = NOISE.sub("", t)
        t = re.sub(r"^\s*\|.*$", "", t, flags=re.M)   # 残留的模板参数行
        t = " ".join(t.split())
        if t:
            blocks.append(t)
    if not blocks:
        return "（Wiktionary 无 Etymology 段，按通行词典写，无定论就写「更早词源不明」）"
    out = "  ┃  ".join(blocks)
    return out[:MAX_ETY] + ("…（已截断）" if len(out) > MAX_ETY else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--size", type=int, default=30)
    a = ap.parse_args()

    audit, ex = load("audit_all"), load("extract_phonetic_pos")
    words = json.loads((DATA_WORDS := ROOT / "data" / "words.json").read_text(encoding="utf-8"))["words"]

    # 已派过的不再派：按 drafts/sb_chunk*.txt 里出现过的词排除，避免重复劳动
    sent = set()
    for f in sorted((ROOT / "drafts").glob("sb_chunk*.txt")):
        sent |= set(re.findall(r"^## (\S+)", f.read_text(encoding="utf-8"), re.M))

    todo = [w for w in words if w.get("stub") and w["id"] not in sent]
    todo.sort(key=lambda w: w["id"])
    print(f"占位词条待办 {len(todo)}（已派 {len(sent)}）")

    for k in range(a.n):
        nn = a.start + k
        part = todo[k * a.size:(k + 1) * a.size]
        if not part:
            print(f"  chunk{nn:02d} 无词可派，停止")
            break
        lines = [f"# 第 {nn} 片 —— 占位词条内容回填，共 {len(part)} 词",
                 "# 读 docs/stub-backfill-spec.md，输出 drafts/sb_chunk%02d.tsv" % nn, ""]
        for w in part:
            tmpl_img = (w.get("core_image") or "").strip() in audit.TEMPLATE_IMAGES
            # 91 词的音标仍是生成器的「拼写套斜杠」——重音歧义与同形异读那两道门有意
            # 挡下了它们。切片若照说「已核正、照抄不要改」，就会让占位音标被抄进 TSV
            # 固定下来。必须逐词判并标出来。
            ph = w.get("phonetic", "")
            ph_fake = ph == "/ˈ" + w["id"] + "/"
            zh_cur = w.get("chinese") or []
            zh_fake = bool(zh_cur) and all(re.fullmatch(r"[a-zA-Z\s'-]+", x) for x in zh_cur)
            lines.append(f"## {w['id']}")
            lines.append(f"pos: {w.get('pos', '')}    phonetic: {ph}"
                         + ("   ← 【是拼写套斜杠，不是音标，需你写英式 IPA】" if ph_fake else ""))
            lines.append(f"现有画面: {'【是模板，需重写】' if tmpl_img else w.get('core_image', '')}")
            lines.append(f"现有中文: {'/'.join(zh_cur) or '（无）'}"
                         + ("   ← 是英文词本身，需重写" if zh_fake else ""))
            lines.append(f"词源(Wiktionary 原文): {etymology(w['id'], ex.english_section)}")
            lines.append("")
        out = ROOT / "drafts" / f"sb_chunk{nn:02d}.txt"
        out.write_text("\n".join(lines), encoding="utf-8")
        print(f"  {out.relative_to(ROOT)}  {len(part)} 词：{part[0]['id']} … {part[-1]['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
