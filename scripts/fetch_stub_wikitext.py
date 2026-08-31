#!/usr/bin/env python3
"""为缺 Wiktionary 缓存的占位词条补抓 wikitext。

    python scripts/fetch_stub_wikitext.py --dry-run   # 只列要抓的词
    python scripts/fetch_stub_wikitext.py             # 实际抓取

为什么需要单独一个脚本：`probe_etymology_coverage.py` 里的 fetch() 正是要复用的
抓取实现（50 词一批、带缓存、0.2s 间隔、maxlag=5），但那个脚本的 main() 只把
**有 root_ids 的词**喂进去，占位词条是无根 germanic，直接跑它抓不到——会输出
「取 wikitext：N 词」然后一个占位词都没覆盖，看着正常其实没发生。

抓完跑 `python scripts/extract_phonetic_pos.py --apply` 即可写回音标与词性，
抽取器的口音优先、字符集折算、重音歧义、同形异读四道门已经调好。
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    audit = load("audit_all")
    probe = load("probe_etymology_coverage")   # 复用其 fetch() 与 CACHE
    cache = probe.CACHE

    words = json.loads((ROOT / "data" / "words.json").read_text(encoding="utf-8"))["words"]
    missing = [w["id"] for w in words
               if audit.is_stub(w) and not (cache / f"{w['id']}.txt").exists()]
    if a.limit:
        missing = missing[:a.limit]

    print(f"占位词条缺缓存 {len(missing)} 个")
    if not missing:
        return 0
    if a.dry_run:
        print(" ".join(missing))
        return 0

    got = probe.fetch(missing)
    sys.stderr.write("\n")

    # 抓回空串说明 Wiktionary 没有该词条，不是网络失败——两者要分开报，
    # 否则会误以为该重试。
    empty = [t for t in missing if not (got.get(t) or "").strip()]
    written = [t for t in missing if (cache / f"{t}.txt").exists()]
    print(f"  落盘        {len(written)}")
    print(f"  内容为空    {len(empty)}  （Wiktionary 无该词条，重试也没用）")
    if empty:
        print("  " + " ".join(empty[:30]))
    print("\n下一步：python scripts/extract_phonetic_pos.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
