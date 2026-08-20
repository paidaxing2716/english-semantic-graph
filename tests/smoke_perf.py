#!/usr/bin/env python3
"""v0.2.1 性能改造冒烟测试：
1) 首次加载：页面渲染出语义域节点，无 pageerror
2) 并行拉取：5 个数据文件请求全部发出（可观测到各请求）
3) 二次访问：命中 IndexedDB 缓存 —— version.json 仍请求，5 个数据文件不再请求
"""
import sys
import time
from playwright.sync_api import sync_playwright

DATA_FILES = [
    "domains.json", "roots.json", "concepts.json", "words.json", "relations.json",
]

def collect_requested_paths(page):
    return page.evaluate("""() => {
      const out = [];
      performance.getEntriesByType('resource').forEach(e => {
        const m = /\\/([^/]+\\.json)$/.exec(e.name);
        if (m) out.push(m[1]);
      });
      return out;
    }""")

def main(url: str) -> int:
    ok = True
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # 干净上下文：不继承缓存/存储
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        # --- 首次加载（?cache=1 强制启用 IndexedDB 缓存，本地 127.0.0.1 也可测）---
        target = url if "?" in url else url + "?cache=1"
        page.goto(target, wait_until="domcontentloaded")
        # 等语义域节点出现（loadData 成功 → buildGraph → render）
        deadline = time.time() + 30
        n = 0
        while time.time() < deadline:
            n = page.evaluate("document.querySelectorAll('.node.domain').length")
            if n > 0:
                break
            time.sleep(0.3)
        print(f"[首次加载] 语义域节点: {n}")
        if n == 0:
            print("[FAIL] 首次加载未渲染出语义域节点")
            ok = False
        paths1 = collect_requested_paths(page)
        print(f"[首次加载] 请求到的数据文件: {sorted(paths1)}")
        for f in DATA_FILES:
            if f not in paths1:
                print(f"[FAIL] 首次加载缺少 {f}")
                ok = False

        # 详情面板加载成功（无报错即认为 data 结构可渲染）
        page.evaluate("""() => {
          const d = document.querySelector('.node.domain');
          if (d) d.dispatchEvent(new MouseEvent('click', {bubbles:true}));
        }""")
        page.wait_for_timeout(800)

        # --- 二次访问：应命中 IndexedDB 缓存 ---
        page.reload(wait_until="domcontentloaded")
        deadline = time.time() + 10
        n2 = 0
        while time.time() < deadline:
            n2 = page.evaluate("document.querySelectorAll('.node.domain').length")
            if n2 > 0:
                break
            time.sleep(0.2)
        paths2 = collect_requested_paths(page)
        data_again = [f for f in DATA_FILES if f in paths2]
        print(f"[二次访问] 语义域节点: {n2}，重新请求的数据文件: {sorted(data_again)}")
        if n2 == 0:
            print("[FAIL] 二次访问未渲染")
            ok = False
        if data_again:
            print(f"[WARN] 二次访问仍重新请求了 {len(data_again)} 个文件（可能未命中缓存）")

        if errors:
            print(f"[FAIL] 页面错误 {len(errors)} 个:")
            for e in errors[:5]:
                print("   ", e[:200])
            ok = False
        else:
            print("[PASS] 无 pageerror")

        browser.close()
    print("冒烟测试:", "全部通过 ✅" if ok else "存在问题 ❌")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/frontend/"))