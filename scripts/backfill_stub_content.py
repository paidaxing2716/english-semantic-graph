#!/usr/bin/env python3
"""把子代理起草的内容字段回填进占位词条。

    python scripts/backfill_stub_content.py drafts/sb_chunk01.tsv --dry-run
    python scripts/backfill_stub_content.py drafts/sb_chunk01.tsv

输入是 10 列 TSV，**列数必须精确等于 10**（空列前面的制表符不能省）：

    1 word        小写，必须已在库且带 stub 标记
    2 origin      中文词源一句。照 drafts/.etym_cache/ 的真实词源写，不许编词形
    3 native      英文释义一句，小写开头，末尾不加句号
    4 zh          中文义项，/ 分隔，1–4 个，最常用在前
    5 examples    两句英文，| 分隔，各 5–12 词，句末句号
    6 concept     `english phrase – 中文解释`，短破折号 –
    7 expansions  | 分隔，逐条说明某义项如何从核心画面推出。zh 有 2 个以上时必填
    8 image       **仅当该词的 core_image 仍是模板时才填**，否则留空表示不动
    9 phonetic    **仅当切片标了「是拼写套斜杠」时才填**，否则留空表示不动
    10 pos        **仅当现有 pos 判错时才填**，否则留空表示不动

第 8、9、10 列都是「留空即不动」。

加第 9 列是因为 91 词的音标仍是生成器的占位串（重音歧义与同形异读两道门有意挡下
没自动写），这些必须由人补。

加第 10 列是因为 extract_phonetic_pos 的「取首个词性标题」规则实测 95.2% 准，
反过来说约 5% 是错的：people 被改成 verb（应为 noun）、topic 与 submarine 被改成
adjective、soon 被改成 adjective（应为 adverb）。写内容时本来就要读该词的词源与
义项，顺手判一下 pos 比另开一轮审计省事。

【为什么不走 entries_from_draft.py】那条是给新词条的，遇到已入库的词会报
「已在词库中，勿重复入库」并拒绝。这里恰恰只改已入库词条的若干字段。

【为什么不走 backfill_collocations.py】那条只写 collocations 一个字段。

写完会做三件事：
  - 用 entries_from_draft.classify_note() 按新 origin 重新判 decomposable_note。
    原值全是「日耳曼核心词」——那是生成器一律套的，而这批里有大量法语/拉丁借词
    （pamphlet ← 法语 pamphilet、plaster ← 拉丁 emplastrum）。不重判就是错标。
  - 同步 data/examples.json（那边另存 10536 条，含 1193 对模板例句）。
  - 该词的模板字段全部补齐后摘掉 stub 标记。补一半的保留标记，便于续做。
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NCOL = 10
# 库内 4114 条真音标只用这些字符（extract_phonetic_pos.LIB_CHARSET 同一套）。
# 卡住这个集合是为了拦窄式记音与美式符号，让新写的音标与全库一致。
PHONETIC_CHARSET = set("()./abdefghijklmnoprstuvwz·æðŋɑɒɔəɜɡɪʃʊʌʒˈˌːθ")
# 与 validate.py 的 VALID_POS 同一套；多词性写 'noun / verb'（带空格，库内 885 条如此）
VALID_POS = {"noun", "verb", "adjective", "adverb", "preposition",
             "conjunction", "pronoun", "interjection"}
# 与 audit_all.NON_IPA_SPELLING 同一套：英语 IPA 里不会出现的正字法特征
NON_IPA_SPELLING = re.compile(r"[cqxy]|sh|ch|th|ph|wh|ck|oo|ee|ea|ou|ay|ai|oa|igh|ss|ll|tt|pp|mm|nn|gg|ff|dd|bb|rr")
# classify_note 只在「← 后紧跟外语名」时判借词。origin 提到外语却没让箭头带出来，
# 就会静默落回「日耳曼核心词」默认档。这个坑实测连栽三次（optical、paralyze、
# periodical），靠记性挡不住，改成门。
FOREIGN = ("法语", "拉丁", "希腊", "意大利", "西班牙", "荷兰", "阿拉伯", "梵语", "俄语", "日语")
# 外语名出现在这些措辞里时不是来源，不该带箭头——bird「非拉丁借词」、brain 的希腊语
# 是远亲、flock 提拉丁只为区分同形异源，库内 25 条属此类，一律放行。
# 「同源」必须在列：荷兰语、低地德语都是日耳曼语支，说某词「与中古荷兰语 X 同源」是
# 陈述亲缘不是陈述来源，那种词条判成日耳曼核心词才对。而 FOREIGN 里有「荷兰」
# （因为「借自荷兰语」确实是一个档），两者会撞——scream 实测被误拦。
HEDGE = ("可能", "一说", "或与", "或出", "或来自", "非", "不是", "而非", "无关",
         "不属", "并非", "远亲", "同类", "同源", "同族", "未定", "不明", "为区分", "另一个")


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
    entries = load("entries_from_draft")

    wp, ep = DATA / "words.json", DATA / "examples.json"
    db = json.loads(wp.read_text(encoding="utf-8"))
    exdb = json.loads(ep.read_text(encoding="utf-8"))
    idx = {w["id"]: w for w in db["words"]}

    # 已被占用的英文释义 → 词。用于拦近义词撞车。
    native_taken = {}
    for w in db["words"]:
        nd = (w.get("native_definition") or "").strip()
        if nd and not audit.is_template_native(nd):
            native_taken.setdefault(nd, w["id"])

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
            if not w.get("stub"):
                errs.append(f"{Path(f).name}:{n} {word} 不是占位词条，拒绝改写")
                continue
            rows.append((Path(f).name, n, word, c))

    for name, n, word, c in rows:
        w = idx[word]
        zh = [x.strip() for x in c[3].split("/") if x.strip()]
        ex = [x.strip() for x in c[4].split("|") if x.strip()]
        image = c[7].strip() or (w.get("core_image") or "")
        # image 不得含 zh 里长度≥2 的义项：学习者看画面时词与中文都被遮住，
        # 点名义项等于自泄答案。这道门与 audit_all 的 critical 判据一致。
        for t in zh:
            if len(t) >= 2 and t in image:
                errs.append(f"{name}:{n} {word} 画面含中文义项「{t}」")
        if len(ex) != 2:
            errs.append(f"{name}:{n} {word} 例句 {len(ex)} 句，须 2 句")
        for s in ex:
            if not s.endswith((".", "!", "?")):
                errs.append(f"{name}:{n} {word} 例句未以句号结束：{s[:30]}")
            if not 5 <= len(s.rstrip(".").split()) <= 20:
                errs.append(f"{name}:{n} {word} 例句词数 {len(s.split())} 越界：{s[:30]}")
        note = entries.classify_note(c[1].strip())
        if note == entries.NOTE_DEFAULT and any(f in c[1] for f in FOREIGN)                 and not any(h in c[1] for h in HEDGE):
            errs.append(f"{name}:{n} {word} origin 提到外语却判成「日耳曼核心词」，"
                        f"多半是漏了 ← 箭头：{c[1][:46]}")
        if len(zh) > 1 and not c[6].strip():
            errs.append(f"{name}:{n} {word} zh 有 {len(zh)} 个义项，expansions 必填")
        # 近义词最容易被写成同一句释义。库内已有 amaze|astonish、bare|naked、
        # gigantic|huge、ponder|contemplate 四对撞车，本轮又新造了 perplex|bewilder
        # 与 seldom|rarely 两对。撞车说明这一条没把两个词区分开，等于白写。
        nd = c[2].strip()
        if nd and nd in native_taken and native_taken[nd] != word:
            errs.append(f"{name}:{n} {word} 英文释义与 {native_taken[nd]} 完全相同，"
                        f"须写出区别：{nd}")
        if "–" not in c[5]:
            errs.append(f"{name}:{n} {word} concept 缺短破折号 –")
        if c[7].strip() and (w.get("core_image") or "").strip() not in audit.TEMPLATE_IMAGES:
            errs.append(f"{name}:{n} {word} core_image 已是真画面，第 8 列不该填")
        ph_new = c[8].strip()
        ph_fake = (w.get("phonetic") or "") == "/ˈ" + word + "/"
        if ph_new:
            if not ph_fake:
                errs.append(f"{name}:{n} {word} 音标已是真音标，第 9 列不该填")
            if not (ph_new.startswith("/") and ph_new.endswith("/") and len(ph_new) > 2):
                errs.append(f"{name}:{n} {word} 音标须用斜杠包裹：{ph_new}")
            # 「与原值相同」是这里唯一可靠的判据：原值本就是占位串，填回同一个值等于
            # 没改。不能靠「等于拼写」来判——单音节词的正确音标本来就可能等于拼写，
            # /rest/ /net/ /bed/ /help/ /step/ 都对，库内有 28 条这样的真音标，
            # 按拼写判会把正确答案挡回去（rest 那条实测被拦过）。
            if ph_new == (w.get("phonetic") or ""):
                errs.append(f"{name}:{n} {word} 第 9 列与原值相同，等于没改：{ph_new}")
            bad = set(ph_new) - PHONETIC_CHARSET
            if bad:
                errs.append(f"{name}:{n} {word} 音标含库外字符 {''.join(sorted(bad))}：{ph_new}")
        elif ph_fake:
            errs.append(f"{name}:{n} {word} 音标是占位串，第 9 列必填")
        pos_new = c[9].strip()
        if pos_new:
            parts = [x.strip() for x in pos_new.split("/") if x.strip()]
            if not parts or any(x not in VALID_POS for x in parts):
                errs.append(f"{name}:{n} {word} pos 不在允许集合：{pos_new}")
            if pos_new == (w.get("pos") or ""):
                errs.append(f"{name}:{n} {word} pos 与原值相同，第 10 列不该填")

    if errs:
        print(f"[FAIL] {len(errs)} 处问题，未写入：", file=sys.stderr)
        for e in errs[:40]:
            print("  " + e, file=sys.stderr)
        return 1

    ex_by_word = {}
    for e in exdb["examples"]:
        ex_by_word.setdefault(e["word_id"], []).append(e)

    done = 0
    for _name, _n, word, c in rows:
        w = idx[word]
        w["origin"] = c[1].strip()
        w["native_definition"] = c[2].strip()
        w["chinese"] = [x.strip() for x in c[3].split("/") if x.strip()]
        w["examples"] = [x.strip() for x in c[4].split("|") if x.strip()]
        w["core_concept"] = c[5].strip()
        w["semantic_expansions"] = [x.strip() for x in c[6].split("|") if x.strip()]
        if c[7].strip():
            w["core_image"] = c[7].strip()
        if c[8].strip():
            w["phonetic"] = c[8].strip()
        if c[9].strip():
            w["pos"] = " / ".join(x.strip() for x in c[9].split("/") if x.strip())
        w["decomposable_note"] = entries.classify_note(w["origin"])
        # examples.json 与 words.json 各存一份，只改一边会让审计报数不一致
        for i, e in enumerate(ex_by_word.get(word, [])[:2]):
            if i < len(w["examples"]):
                e["text"] = w["examples"][i]
        if not audit.is_stub(w) and (w.get("core_image") or "").strip() not in audit.TEMPLATE_IMAGES:
            w.pop("stub", None)
            done += 1

    print(f"待写 {len(rows)} 词，其中 {done} 词补齐并摘掉 stub 标记")
    if a.dry_run:
        print("[DRY-RUN] 未落盘")
        return 0
    wp.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ep.write_text(json.dumps(exdb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] 已写入 {wp.relative_to(ROOT)} 与 {ep.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
