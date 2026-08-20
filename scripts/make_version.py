#!/usr/bin/env python3
"""生成 data/version.json —— 前端 IndexedDB 缓存的版本键。

版本 = data/ 下所有 *.json 内容的 SHA-256（排除 version.json 自身），
任何数据文件变化都会产生新版本号，前端据此决定缓存是否失效。

用法：
    python3 scripts/make_version.py
"""
import hashlib
import json
import pathlib
import sys

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "version.json"


def main() -> int:
    files = sorted(p for p in DATA.glob("*.json") if p.name != "version.json")
    if not files:
        print("NO DATA FILES", file=sys.stderr)
        return 1

    h = hashlib.sha256()
    for f in files:
        h.update(f.read_bytes())
    version = h.hexdigest()[:16]

    payload = {
        "version": version,
        "files": [f.name for f in files],
        "generated_by": "scripts/make_version.py",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"version.json: {version}  ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())