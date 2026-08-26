#!/usr/bin/env python3
"""筛查草稿里的拉丁近形异源错挂。

    python scripts/audit_trap_pairs.py drafts/r_chunk52.tsv ...

两道现有的门都查不到这类错：词条格式合规、origin 与所挂根「看起来」一致，
错在词源事实本身。本会话四片 219 词里子代理逐词核出 16 个（7.3%），全是这一类。
本脚本做两件机器能做的：
  一、陷阱表比对——该根的 origin 里若出现它的已知混淆对象，报出来
  二、Wiktionary 独立复核——词元完全不指向所挂根的，报出来
两者都只是线索，判定仍需看词源。
"""
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_etymology_coverage as P  # noqa: E402

# 已实证的近形异源对：键 = 库中根 id，值 = 容易被误收进来的另一个拉丁/希腊词
TRAPS = {
    "manus": ["manere", "maneo", "permaneo"],
    "planus": ["plangere", "plango", "planctus"],
    "ferre": ["ferire", "ferio"],
    "cadere": ["caedere", "caedo"],
    "caedere": ["cadere", "cado"],
    "tendere": ["tener"],
    "cors": ["chorda", "khorde"],
    "humor-moist": ["humus", "humilis"],
    "legere": ["lex", "legis"],
    "lex-legis": ["legere", "lego"],
    "portus": ["portio"],
    "minus-less": ["minium"],
    "putare": ["putten", "pytan"],
    "fundere": ["refutare", "recusare"],
    "vid": ["dividere", "divido"],
    "tempus": ["templum"],
    "secare": ["secta"],
    "posse": ["potio"],
    "ars": ["artus"],
    "cura": ["accuratus"],
    "spect": ["species"],
}


def rows_of(path):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        p = line.split("\t")
        if p and p[0] == "W" and len(p) >= 7:
            yield p


def main():
    files = sys.argv[1:]
    if not files:
        print("用法: audit_trap_pairs.py <tsv> [<tsv> ...]")
        return 1

    print("=== 一、陷阱表：origin 里出现了所挂根的已知混淆对象 ===")
    hits = 0
    for f in files:
        for p in rows_of(f):
            word, root, origin = p[1], p[4], p[6]
            for bad in TRAPS.get(root, []):
                if re.search(r"(?<![a-z])" + re.escape(bad), origin.lower()):
                    hits += 1
                    print(f"  {Path(f).name:16} {word:14} 挂 {root:12} "
                          f"但 origin 提到 {bad}")
                    print(f"      {origin[:100]}")
    if not hits:
        print("  无命中")

    print()
    print("=== 二、Wiktionary 独立复核（词元完全不指向所挂根的）===")
    roots = P.load_json_roots() if hasattr(P, "load_json_roots") else None
    import json
    roots = json.loads((P.DATA / "roots.json").read_text(
        encoding="utf-8"))["roots"]
    keys = P.root_keys(roots)
    sizes = {r["id"]: len(r.get("word_ids") or []) for r in roots}
    n = flagged = nocache = 0
    for f in files:
        for p in rows_of(f):
            word, root = p[1], p[4]
            if not root:
                continue
            n += 1
            c = P.CACHE / (urllib.parse.quote(word, safe="") + ".txt")
            if not c.exists():
                nocache += 1
                continue
            lms = P.lemmas(P.english_etymology(c.read_text(encoding="utf-8")))
            if not lms:
                continue
            m = [r for r, _ in P.match(lms, keys, sizes)]
            if m and root not in m:
                flagged += 1
                print(f"  {word:14} 挂 {root:14} Wiktionary 指向 {m[:3]}")
    print(f"\n  共核 {n} 个词根型词条：{flagged} 个存疑，{nocache} 个无缓存未核")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
