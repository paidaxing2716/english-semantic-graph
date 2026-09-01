#!/usr/bin/env python3
"""替换模板例句。只动 examples 一列，不碰其余任何字段。

    python scripts/backfill_template_examples.py drafts/tex_batch1.tsv --dry-run
    python scripts/backfill_template_examples.py drafts/tex_batch1.tsv

输入是 2 列 TSV：

    1 word        小写，必须已在库
    2 examples    两句英文，| 分隔，各 4–20 词，句末标点

【为什么另开一个脚本】
backfill_stub_content.py 只改带 `stub` 标记的词条（那是有意的，防止误改已完成
词条的十列内容）。而这批 59 词不带 stub 标记——它们的释义、中文、画面、概念、
语义展开全是真值，只有 examples 是生成器签名 `The X changed the situation.`。
走那条管道会被「不是占位词条，拒绝改写」挡下，且它会重写十列。

【为什么这批没被 is_stub 抓到】
is_stub 要求「模板例句 **且** 模板释义」同时成立。m–o 段那次生成写了真释义，
所以这 59 条一直落在 is_stub 之外，只由 audit_all 的「疑似通用模板例句」报出，
而我此前的收尾核查恰好没查例句这一项。
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NCOL = 2


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    audit = load("audit_all")
    wp, ep = DATA / "words.json", DATA / "examples.json"
    db = json.loads(wp.read_text(encoding="utf-8"))
    exdb = json.loads(ep.read_text(encoding="utf-8"))
    idx = {w["id"]: w for w in db["words"]}

    rows, errs = [], []
    for f in a.tsv:
        for n, line in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) != NCOL:
                errs.append(f"{Path(f).name}:{n} 列数 {len(c)} ≠ {NCOL}")
                continue
            word = c[0].strip()
            w = idx.get(word)
            if not w:
                errs.append(f"{Path(f).name}:{n} {word} 不在库")
                continue
            # 只准改模板例句。已是真例句的不该经这条管道——那种改动要说得出理由，
            # 走这里等于绕过审查。
            old = [str(x) for x in (w.get("examples") or [])]
            if not (old and audit.TEMPLATE_EX.match("|".join(old))):
                errs.append(f"{Path(f).name}:{n} {word} 现有例句不是模板，拒绝改写")
                continue
            rows.append((Path(f).name, n, word, c))

    for name, n, word, c in rows:
        ex = [x.strip() for x in c[1].split("|") if x.strip()]
        if len(ex) != 2:
            errs.append(f"{name}:{n} {word} 例句 {len(ex)} 句，须 2 句")
        for s in ex:
            if not s.endswith((".", "!", "?")):
                errs.append(f"{name}:{n} {word} 例句未以句号结束：{s[:30]}")
            if not 4 <= len(s.rstrip(".").split()) <= 20:
                errs.append(f"{name}:{n} {word} 例句词数 {len(s.split())} 越界：{s[:30]}")
            # 例句里必须出现该词或其屈折形。这批词的画面与释义都是真值，例句写偏
            # 到近义词上（库内已有 beast 配 animal、gravity 配 grave 的先例）不易
            # 察觉，故加这道门。强变化动词由下面的兜底放行。
            toks = set(re.findall(r"[a-z]+", s.lower()))
            stem = word.rstrip("e")
            # 强变化动词的词干对不上（mistake→mistook、misunderstand→misunderstood），
            # 故加一条前 4 字符的兜底。这条兜底是钝的：它会放过 gravity 配 grave
            # 那种派生词漂移（共享 grav）。取舍是有意的——这道门要拦的是 beast 配
            # animal 那种整词跑偏（animal 与 beas 不共享前缀，仍拦得住），
            # 派生词漂移得读语义，不是前缀匹配能判的。
            head = word[:4]
            if not any(t == word or t.startswith(stem) or t.startswith(head) for t in toks):
                errs.append(f"{name}:{n} {word} 例句里没有这个词：{s[:40]}")
        if len(set(ex)) != len(ex):
            errs.append(f"{name}:{n} {word} 两句例句相同")

    if errs:
        print(f"[FAIL] {len(errs)} 处问题，未写入：", file=sys.stderr)
        for e in errs[:40]:
            print("  " + e, file=sys.stderr)
        return 1

    ex_by_word = {}
    for e in exdb["examples"]:
        ex_by_word.setdefault(e["word_id"], []).append(e)

    for _name, _n, word, c in rows:
        w = idx[word]
        w["examples"] = [x.strip() for x in c[1].split("|") if x.strip()]
        # examples.json 与 words.json 各存一份，只改一边会让审计报数不一致
        for i, e in enumerate(ex_by_word.get(word, [])[:2]):
            if i < len(w["examples"]):
                e["text"] = w["examples"][i]

    print(f"待写 {len(rows)} 词的例句")
    if a.dry_run:
        print("[DRY-RUN] 未落盘")
        return 0
    wp.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ep.write_text(json.dumps(exdb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] 已写入 {wp.relative_to(ROOT)} 与 {ep.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
