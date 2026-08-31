#!/usr/bin/env python3
"""给批量生成器留下的占位词条打 stub 标记，并报诚实的覆盖率。

    python scripts/mark_stubs.py            # 只报，不改
    python scripts/mark_stubs.py --apply    # 写入 stub 字段

判据复用 audit_all.is_stub()：模板例句与模板释义同时命中。两项都是生成器
build_g_chunk*.py 的签名，单独一项可能是真词条撞上通用写法。

为什么要显式标记：validate.py 对这些词条全绿（结构合法），覆盖率算出来 98.5%，
但其中 1134 条的释义、概念、例句、语义展开都是模板，实际可用的只有 77.1%。
不打标记的话，下次接手照样会被「全绿 + 98.5%」骗过去——这一轮就是这么滑过去的。
标记之后 stub 可以直接查询，覆盖率口径也能落到脚本里而不是靠人记得剔除。

字段用 stub 而非 decomposable 那种既有字段：占位与可拆性是两个正交的维度，
一个占位词条同样可以是 germanic 或 root 型。
"""
import argparse
import collections
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 功能词等按项目规则本就不建词条，不该算进缺口。判据与 build_g_chunk* 用的一致。
FUNCTION_WORDS = set(
    "a an the all and any at be being been both but by can could do does did each few for he her "
    "here him his i if in is it its may me might must my no not of on one or our she shall should "
    "so some such than that their them then there these they this those to us very was we were "
    "what when where which who whom whose will with would you your first second third five four "
    "six seven eight nine ten eleven twelve twenty thirty forty fifty hundred thousand million "
    "billion zero".split()
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    spec = importlib.util.spec_from_file_location("audit_all", ROOT / "scripts" / "audit_all.py")
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)

    path = ROOT / "data" / "words.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    words = data["words"]
    ref = json.loads((ROOT / "data" / "english_reference.json").read_text(encoding="utf-8"))["words"]
    refs = {(r if isinstance(r, str) else r.get("word", "")).lower() for r in ref}

    stubs = [w for w in words if audit.is_stub(w)]
    stub_ids = {w["id"] for w in stubs}
    have = {w["id"].lower() for w in words}
    usable = {w["id"].lower() for w in words if w["id"] not in stub_ids}
    structurable = {x for x in refs if x not in FUNCTION_WORDS and " " not in x and "-" not in x}

    print(f"词条总数        {len(words)}")
    print(f"  可用          {len(words) - len(stubs)}")
    print(f"  占位(stub)    {len(stubs)}")
    print()
    print(f"考研词表 {len(refs)} 词形：")
    print(f"  有条目        {len(refs & have):5}  {100 * len(refs & have) / len(refs):5.1f}%   ← 名义覆盖率")
    print(f"  可用条目      {len(refs & usable):5}  {100 * len(refs & usable) / len(refs):5.1f}%   ← 真实覆盖率")
    stub_lower = {i.lower() for i in stub_ids}
    print(f"  占位条目      {len(refs & stub_lower):5}  {100 * len(refs & stub_lower) / len(refs):5.1f}%")
    print(f"  无条目        {len(refs - have):5}  （功能词等，按项目规则不建条）")
    print()
    print(f"剔掉功能词后可结构化 {len(structurable)} 词形：")
    print(f"  可用覆盖      {len(structurable & usable):5}  {100 * len(structurable & usable) / len(structurable):5.1f}%")

    # 占位词条还缺哪些字段，供排后续工作量
    miss = collections.Counter()
    for w in stubs:
        if audit.is_template_native(w.get("native_definition")):
            miss["native_definition"] += 1
        if audit.is_template_concept(w.get("core_concept")):
            miss["core_concept"] += 1
        if (w.get("core_image") or "").strip() in audit.TEMPLATE_IMAGES:
            miss["core_image"] += 1
        if w.get("phonetic", "") == "/ˈ" + w["id"] + "/":
            miss["phonetic"] += 1
        zh = [x.strip() for x in (w.get("chinese") or []) if x.strip()]
        if zh and all(audit.ASCII_WORD.match(x) for x in zh):
            miss["chinese"] += 1
        se = [str(x) for x in (w.get("semantic_expansions") or [])]
        if se and all(audit.TEMPLATE_SEM_SUB in x for x in se):
            miss["semantic_expansions"] += 1
        miss["examples"] += 1  # 判据本身，全部命中
    print("\n占位词条待补字段：")
    for k, v in miss.most_common():
        print(f"  {k:22} {v}")

    if a.apply:
        n = 0
        for w in words:
            if w["id"] in stub_ids:
                if not w.get("stub"):
                    n += 1
                w["stub"] = True
            elif "stub" in w:
                del w["stub"]  # 内容补齐后重跑即自动摘掉标记
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\n[APPLY] 新增 stub 标记 {n} 条，共 {len(stub_ids)} 条带标记")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
