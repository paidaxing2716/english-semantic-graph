#!/usr/bin/env python3
"""拿库内已有真音标的词当标注集，量 extract_phonetic_pos 的准确率。

    python scripts/probe_phonetic_accuracy.py

抽取器只在占位词条上跑，无法自证。这里反过来喂它已知答案：库内 4114 条真词条里
有缓存的那些，抽出来的音标与库内人工写的比对。完全一致率是下限（记法细节如
音节点 . 与括号可选成分会造成合法差异），所以另报「去掉音节点与括号后一致」。
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def loose(p):
    """去掉音节点、括号可选成分、次重音——这些是记法自由度，不算判错。"""
    p = re.sub(r"\([^)]*\)", "", p)
    return p.replace(".", "").replace("·", "").replace("ˌ", "").strip("/")


def canon(p):
    """再折掉口径差异，用于区分「换了口音」与「读音真不同」。

    库内 4114 条本身是混合口径：儿化 309 条、非儿化 295 条，oʊ 30 条、əʊ 223 条，
    ɑː 172 条、ɒ 295 条，且按词族成簇（compose/expose/propose 全用美式 oʊ）。
    所以「与库内不一致」不等于抽错——库自己就不自洽。真正要抓的是读音差异。
    """
    p = loose(p)
    for a, b in (("oʊ", "əʊ"), ("ɑː", "ɒ"), ("ɔːr", "ɔː"), ("ɜːr", "ɜː"), ("ɑːr", "ɑː")):
        p = p.replace(a, b)
    p = re.sub(r"ər", "ə", p).replace("ɚ", "ə").replace("ɝ", "ɜː")
    # 成音节辅音：库内写 /ˈmɪʃn/ /ˈfɔːrml/ /ɪmˈpɔːrtnt/，Wiktionary 写成 ən/əl，
    # 同一读音的两种记法。位置不限词尾（important 的 tnt 在中间）。
    p = re.sub(r"(?<=[a-zæðŋɑɒɔəɜɡɪʃʊʌʒθ])([nlm])(?![aeiouæɑɒɔəɜɪʊʌ])", r"ə\1", p)
    p = re.sub(r"ə+", "ə", p)
    p = p.replace("j", "")   # yod 有无属方言变体（introduce /duːs/ 与 /dʒuːs/ 都对）
    return p.replace("r", "")


def stress_syllable(p):
    """单音节词标不标主重音是自由的（库内 /pruːv/，Wiktionary /ˈpruːv/），
    所以只有一个音节时统一归 0，否则会把记法自由度算成重音分歧。"""
    syl = len(re.findall(r"[aeiouæɑɒɔəɜɪʊʌ]+", p))
    if syl <= 1:
        return 0
    i = p.find("ˈ")
    return -1 if i < 0 else len(re.findall(r"[aeiouæɑɒɔəɜɪʊʌ]+", p[:i]))


def main():
    audit, ex = load("audit_all"), load("extract_phonetic_pos")
    words = json.loads((ROOT / "data" / "words.json").read_text(encoding="utf-8"))["words"]
    real = [w for w in words if not audit.is_stub(w)]

    import collections
    cat = collections.Counter()
    n = miss = nocache = gated = 0
    resid, stressed = [], []
    for w in real:
        ph = (w.get("phonetic") or "").strip()
        # 只用单读音、纯 IPA 的当标注：带 (v.)/(n.) 双读音的那 7 条本身格式特殊
        if not (ph.startswith("/") and ph.endswith("/") and " " not in ph):
            continue
        cache = ROOT / "drafts" / ".etym_cache" / f"{w['id']}.txt"
        if not cache.exists():
            nocache += 1
            continue
        section = ex.english_section(cache.read_text(encoding="utf-8", errors="replace"))
        got, why = ex.pick_ipa(section)
        if not got:
            miss += 1
            continue
        if why == "重音歧义":
            gated += 1  # 实际运行时这类不写回，不该计入准确率
            continue
        n += 1
        if got == ph:
            cat["完全一致"] += 1
        elif loose(got) == loose(ph):
            cat["记法差异内一致"] += 1
        elif canon(got) == canon(ph):
            cat["口径差异内一致"] += 1
        elif stress_syllable(got) != stress_syllable(ph):
            cat["重音位置不同"] += 1
            stressed.append((w["id"], ph, got))
        else:
            cat["读音真不同"] += 1
            resid.append((w["id"], ph, got))

    print(f"标注集（库内真音标、有缓存、未被歧义门挡下）  {n}")
    for k in ("完全一致", "记法差异内一致", "口径差异内一致", "重音位置不同", "读音真不同"):
        print(f"  {k:14} {cat[k]:5}  {100 * cat[k] / n:5.1f}%")
    print(f"\n  被歧义门挡下（不写回）    {gated}")
    print(f"  抽不出（无 IPA/方言拒收） {miss}")
    print(f"  无缓存                    {nocache}")
    print("\n重音位置不同（歧义门漏掉的，库内值 vs 抽取值）:")
    for wid, ph, got in stressed[:12]:
        print(f"  {wid:16} {ph:20} {got}")
    print("\n读音真不同（前 18 条）:")
    for wid, ph, got in resid[:18]:
        print(f"  {wid:16} {ph:20} {got}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
