#!/usr/bin/env python3
"""从 drafts/.etym_cache/ 的 Wiktionary wikitext 抽占位词条的音标与词性。

    python scripts/extract_phonetic_pos.py --limit 50      # 试样，只出 TSV
    python scripts/extract_phonetic_pos.py                 # 全量出 TSV
    python scripts/extract_phonetic_pos.py --apply         # 写回 data/words.json

只处理 audit_all.is_stub() 判定的占位词条，且只覆盖两个可机器验证的字段。
释义、概念、例句、中文属于教学内容，机器补不了，不在本脚本范围内。

音标取英式 RP：库内 4114 条真词条是 /lɒt/ /ˈdɒktə/ /bɜːd/ /kɑː(r)/ 这种非儿化
RP（ɒ 295 条、词尾非儿化 ə 256 条、纯 ɜː 135 条），美式独有标记只有 7 条。
所以优先级是 RP > 无口音标注 > 英国地区 > 其它，明确避开 US/GA。
"""
import argparse
import collections
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "drafts" / ".etym_cache"
POS_MAP = {"Noun": "noun", "Verb": "verb", "Adjective": "adjective", "Adverb": "adverb",
           "Preposition": "preposition", "Conjunction": "conjunction", "Pronoun": "pronoun",
           "Interjection": "interjection"}
# 口音优先级，数字越小越优先。
# 无标注必须排在显式 UK/RP 之后：Wiktionary 词条顶端那条不带 a= 的 IPA 往往是美式
# （only 的首条是 /ˈoʊn.li/，英式 /ˈəʊn.li/ 反而嵌在 a=UK 里）。把无标注当通用会取错。
ACCENT_RANK = [
    (re.compile(r"\bRP\b"), 0),
    (re.compile(r"\b(Received Pronunciation|British|UK|England)\b", re.I), 2),
    (re.compile(r"\b(AU|NZ|Australia|Scotland|Ireland|India|Wales|Northumbria)\b", re.I), 80),
    (re.compile(r"\b(GA|US|American|GenAm|Canada|SSB)\b"), 90),
]
UNLABELED_RANK = 10
# 库内 4114 条真音标只用这 46 个字符，且零组合变音符。
LIB_CHARSET = set("()./abdefghijklmnoprstuvwz·æðŋɑɒɔəɜɡɪʃʊʌʒˈˌːθ")
# 记法差异，可安全折算成库内写法：Wiktionary 用精确符号，库内用 EFL 简化式
# （bed 在库内是 /bed/ 而非 /bɛd/）。这类替换不改变读音，只统一记法。
NOTATION_MAP = {"ɹ": "r", "ɛ": "e", "ʰ": "", "ʲ": ""}
# SSB 把非儿化的 -er 词尾记成长弱音 əː（teacher /ˈtiːtʃəː/），库内一律写 ə。
# 同一读音的两种记法，折算掉。实测只影响 5 条，全是 -er 施事名词。
NOTATION_SEQ = (("əː", "ə"),)
# 真方言标记，绝不映射。ɚ/ɝ 是美式儿化元音、ʉ 苏格兰与澳洲、ɐ 澳洲与加拿大、
# ʈ ɖ ɻ 印度英语卷舌、ʍ 苏格兰 wh-、ɵ ø 加拿大。把它们折成英式等于伪造读音，
# 宁可整条拒收、留给人工或联网补。


def load_audit():
    spec = importlib.util.spec_from_file_location("audit_all", ROOT / "scripts" / "audit_all.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def english_section(text):
    """取 ==English== 到下一个二级标题之间。跨语言段的词性标题会污染结果。"""
    m = re.search(r"^==\s*English\s*==", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^==[^=]", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def normalize_ipa(token):
    """剥离窄式记音的组合变音符，再把记法差异折算成库内写法。

    组合符必须剥离而不是拒收：RP 的 /ˈäʊ̯t/ 只是在 a 上带分音符、ɪ 上带反breve，
    剥掉就是 /ˈaʊt/，与库内写法一致。不剥的话 out 那条会被挡下，而当天所有变体里
    唯一能通过字符集的是 a=Pittsburgh 的 /ˈaːt/——挡掉正确项反而放行了错误项。
    """
    plain = "".join(c for c in unicodedata.normalize("NFD", token) if not unicodedata.combining(c))
    out = "".join(NOTATION_MAP.get(c, c) for c in plain)
    for a, b in NOTATION_SEQ:
        out = out.replace(a, b)
    return out


def accent_rank(label):
    for pattern, rank in ACCENT_RANK:
        if pattern.search(label):
            return rank
    return 50 if label else UNLABELED_RANK


def pick_ipa(section):
    """收集 {{IPA|en|/…/|a=…}} 并按口音优先级取一个，超出库内字符集的丢弃。

    a= 可能挂在同行的 enPR 上而不在 IPA 里（singular 就是），所以口音标签按整行取。
    返回 (音标, 丢弃原因)：取到就是 ('…', '')，被字符集挡下是 ('', '窄式记音')。
    """
    # 多个 Pronunciation 段意味着同形异读：不同词源支各有读音，取首个多半取错支。
    # 实测 27 个占位词属此类，paste 抽成 /ˈpæsteɪ/（英语是 /peɪst/）、spread 抽成
    # /spriːd/（应为 /spred/）、shower 抽到「展示者」而非「淋浴」。整类不自动写。
    if len(re.findall(r"^===+\s*Pronunciation[^=]*===+", section, re.M)) > 1:
        return "", "同形异读（多个读音段）"
    best, rejected, accepted = None, False, []
    for line in section.splitlines():
        if "{{IPA|en|" not in line:
            continue
        label = "".join(re.findall(r"\ba=([^}|]+)", line))
        rank = accent_rank(label)
        for call in re.findall(r"\{\{IPA\|en\|([^}]*)\}\}", line):
            for token in call.split("|"):
                token = token.strip()
                if not (token.startswith("/") and token.endswith("/") and len(token) > 2):
                    continue
                token = normalize_ipa(token)
                if set(token) - LIB_CHARSET:
                    rejected = True  # 剩下的是真方言标记，见 NOTATION_MAP 上方注释
                    continue
                accepted.append((rank, token))
                if best is None or rank < best[0]:
                    best = (rank, token)
    if not best:
        return "", ("窄式记音超出库内字符集" if rejected else "无 IPA")
    # 名动异重词的重音歧义必须标出，不能默默取一个。实测拿库内 2602 条已知音标反查，
    # 153 条（5.9%）的分歧就是这一类：compress 库内是动词重音 /kəmˈpres/，Wiktionary
    # 首条却是名词的 /ˈkɒmpres/。取错支等于把重音教反，比留空更糟。
    positions = {stress_syllable(t) for _r, t in accepted}
    positions.discard(-1)  # 无重音符的方言变体不参与比较，否则处处是假歧义
    if len(positions) > 1:
        return best[1], "重音歧义"
    return best[1], ""


VOWELS = "aeiouæɑɒɔəɜɪʊʌ"


def stress_syllable(ipa):
    """主重音落在第几个音节。-1 表示没标主重音。

    数音节而非音段：ourselves 的 /aʊəˈselvz/ 与 /ɑːˈselvz/ 只是 our 的元音拼法不同，
    重音都在第二音节，按音段数会误判成歧义。连续元音字符算一个音节（双、三元音）。
    """
    i = ipa.find("ˈ")
    if i < 0:
        return -1
    return len(re.findall(rf"[{VOWELS}]+", ipa[:i]))


def pick_pos(section):
    """只取主词性，不取罕用义与屈折形式。

    Wiktionary 会把边缘义项也立成词性标题，全收进来是在制造错误而非补全：
    occasion 的 Verb 是「to cause」这种古旧用法、optical 的 Noun 带 {{lb|en|film}}
    是电影业行话、outing 的 Verb 其实是 {{infl of|en|out}} 屈折形式不是独立词性。
    库内这批词的 pos 要么本就正确（build 脚本手写的那几组），要么被默认成 noun；
    取首个词性标题足以纠正默认值，而不会引入罕用义。真需要双词性的留给内容轮。
    """
    for m in re.finditer(r"^====?\s*(Noun|Verb|Adjective|Adverb|Preposition|Conjunction|Pronoun|Interjection)"
                         r"\s*====?\n(.{0,200})", section, re.M | re.S):
        body = m.group(2)
        if re.search(r"\{\{(head\|en\|[^}]*\bform\b|infl of|inflection of|plural of|en-past|en-third)", body):
            continue  # 屈折形式，不是独立词性
        return POS_MAP[m.group(1)]
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个，用于试样")
    ap.add_argument("--apply", action="store_true", help="写回 data/words.json")
    ap.add_argument("--out", default="drafts/phonetic_pos.tsv")
    a = ap.parse_args()

    audit = load_audit()
    path = ROOT / "data" / "words.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    stubs = [w for w in data["words"] if audit.is_stub(w)]
    if a.limit:
        stubs = stubs[:a.limit]

    rows, stat = [], collections.Counter()
    for w in stubs:
        wid = w["id"]
        cache = CACHE / f"{wid}.txt"
        if not cache.exists():
            stat["无缓存"] += 1
            rows.append([wid, w.get("phonetic", ""), "", w.get("pos", ""), "", "无缓存"])
            continue
        section = english_section(cache.read_text(encoding="utf-8", errors="replace"))
        if not section:
            stat["无 English 段"] += 1
            rows.append([wid, w.get("phonetic", ""), "", w.get("pos", ""), "", "无 English 段"])
            continue
        ipa, why = pick_ipa(section)
        pos = pick_pos(section)
        note = []
        if ipa and why == "重音歧义":
            stat["重音歧义，不自动写"] += 1
            note.append(f"重音歧义(候选之一 {ipa})")
            ipa = ""
        elif ipa:
            stat["得音标"] += 1
        else:
            note.append(why)
            stat[why] += 1
        old_pos = w.get("pos") or ""
        if pos:
            stat["得词性"] += 1
            if pos != old_pos:
                stat["词性与原值不同"] += 1
                # 只改写生成器的默认值 'noun'。原值是别的词性说明 build 脚本手写过
                # （verb/adj/adv 三组硬编码集合），那是按主用法有意选的，比 Wiktionary
                # 的首个词性可靠——后者按词源顺序排不按频次，overlook 会给成 noun 而
                # 动词才是主用法。原值含分隔符的多词性同理更全，也不动。
                if old_pos != "noun":
                    note.append(f"保留原词性({old_pos})")
                    stat["保留原词性"] += 1
                    pos = ""
        else:
            note.append("无词性")
        if ipa and pos:
            stat["两者齐全"] += 1
        rows.append([wid, w.get("phonetic", ""), ipa, old_pos, pos, ",".join(note)])

    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    header = ["word", "old_phonetic", "new_phonetic", "old_pos", "new_pos", "note"]
    out.write_text("\n".join("\t".join(r) for r in [header] + rows) + "\n", encoding="utf-8", newline="")

    print(f"占位词条 {len(stubs)}  →  {out.relative_to(ROOT)}")
    for k, v in stat.most_common():
        print(f"  {k:14} {v}")

    if a.apply:
        wm = {w["id"]: w for w in data["words"]}
        n_ph = n_pos = 0
        for wid, _old_ph, ipa, _old_pos, pos, _note in rows:
            if ipa:
                wm[wid]["phonetic"] = ipa
                n_ph += 1
            if pos:
                wm[wid]["pos"] = pos
                n_pos += 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[APPLY] 音标 {n_ph} 条，词性 {n_pos} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
