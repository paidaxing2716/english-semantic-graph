#!/usr/bin/env python3
"""调模型生成词条候选。

模型通道通过环境变量配置（任意 OpenAI 兼容端点）：
    ESG_API_BASE   如 https://api.example.com/v1
    ESG_API_KEY
    ESG_MODEL      默认 gpt-4o

没配端点时不报错，而是把提示词写到文件，
你可以贴给任意对话模型，再把返回的 JSON 交给 review.py。
这样管线在没有可用 API 的机器上依然能走完。

用法：
    python ai_pipeline/word_analyzer.py depress:press compose:pose -o candidates.json
    python ai_pipeline/word_analyzer.py --prompt-only depress:press -o prompt.txt
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt_builder import build  # noqa: E402


def call_model(prompt, base, key, model, timeout=180):
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system",
             "content": "你是英语词源与语义分析专家。只输出合法 JSON，不要 markdown 代码块。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }).encode()

    req = urllib.request.Request(
        f"{base.rstrip('/')}/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]


def extract_json(text):
    """模型常会包 ```json 或加前后说明，容错提取。"""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1] if "```" in t[3:] else t[3:]
        t = t.lstrip("json").lstrip()
    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"响应中找不到 JSON：{text[:200]}")
    return json.loads(t[start:end + 1])


def main():
    ap = argparse.ArgumentParser(description="生成词条候选")
    ap.add_argument("targets", nargs="+", help="格式 word:root_id")
    ap.add_argument("-o", "--out", default="candidates.json")
    ap.add_argument("-n", "--examples", type=int, default=3)
    ap.add_argument("--prompt-only", action="store_true", help="只导出提示词，不调模型")
    a = ap.parse_args()

    parsed = []
    for t in a.targets:
        if ":" not in t:
            raise SystemExit(f"格式错误：{t}，应为 word:root_id")
        w, r = t.split(":", 1)
        parsed.append((w, r))

    prompt = build(parsed, a.examples)

    base = os.environ.get("ESG_API_BASE")
    key = os.environ.get("ESG_API_KEY")
    model = os.environ.get("ESG_MODEL", "gpt-4o")

    if a.prompt_only or not (base and key):
        out = Path(a.out if a.prompt_only else "prompt.txt")
        out.write_text(prompt, encoding="utf-8")
        if not a.prompt_only:
            print("未配置 ESG_API_BASE / ESG_API_KEY，跳过模型调用。")
        print(f"提示词已写入 {out}（{len(prompt)} 字符）")
        print("把模型返回的 JSON 存为 candidates.json，然后运行：")
        print("    python ai_pipeline/review.py check candidates.json")
        return 0

    print(f"调用 {model} 生成 {len(parsed)} 个词条…")
    try:
        raw = call_model(prompt, base, key, model)
    except urllib.error.HTTPError as e:
        print(f"[FAIL] HTTP {e.code}: {e.read()[:200].decode(errors='replace')}")
        return 1
    except Exception as e:
        print(f"[FAIL] 调用失败：{e}")
        return 1

    try:
        obj = extract_json(raw)
    except Exception as e:
        Path("raw_response.txt").write_text(raw, encoding="utf-8")
        print(f"[FAIL] 解析失败：{e}\n原始响应已存到 raw_response.txt")
        return 1

    Path(a.out).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    n = len(obj.get("words", []))
    print(f"已生成 {n} 条 → {a.out}")
    print("下一步：python ai_pipeline/review.py check " + a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
