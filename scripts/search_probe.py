#!/usr/bin/env python3
"""搜索直达检查。

revealNode 在 v0.3 被整体重写（旧实现是"逐层展开直到目标露出来"，钻取模型下改成
"把导航状态设到目标所在层"），这是它唯一的入口路径，单独验一遍。

用法：python scripts/search_probe.py [url]
"""
import sys
import time
from playwright.sync_api import sync_playwright

STATE_JS = """() => {
  const vis = (s) => [...document.querySelectorAll(s)]
    .filter((e) => e.getAttribute('opacity') !== '0');
  const hl = document.querySelector('.node.highlighted text');
  return {
    domain: vis('.node.domain').length,
    root: vis('.node.root').length,
    word: vis('.node.word').length,
    links: vis('.link').length,
    crumbRoot: (document.querySelector('.crumb-root') || {}).textContent || '',
    crumbDomain: (document.querySelector('.crumb-domain') || {}).textContent || '',
    highlighted: hl ? hl.textContent : '(none)',
    detailTitle: (document.querySelector('#detail-content h2, #detail-content h1')
                  || {}).textContent || '',
  };
}"""


def search(page, term):
    page.fill("#search-input", "")
    page.type("#search-input", term, delay=25)
    page.wait_for_timeout(600)
    first = page.query_selector("#search-results .search-item:not(.search-empty)")
    if not first:
        return None
    label = first.inner_text().strip().replace("\n", " ")[:40]
    first.click()
    # focusNode 的高亮只留 3 秒（graph.js 里 setTimeout 3000）。等太久会采到
    # 高亮已经自然消失的时刻，误报成"没高亮"——1800ms 足够切层动画收完，
    # 又稳稳落在高亮窗口内。
    page.wait_for_timeout(1800)
    return label


def main(url):
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url, wait_until="domcontentloaded")
        deadline = time.time() + 30
        while time.time() < deadline:
            if page.evaluate("document.querySelectorAll('.node.domain').length") > 0:
                break
            time.sleep(0.3)
        page.wait_for_timeout(2000)

        # --- 搜一个单词：应落在它所属词根的词族层 ---
        hit = search(page, "press")
        s = page.evaluate(STATE_JS)
        print(f"搜「press」→ 命中 {hit}")
        print(f"  域={s['domain']} 根={s['root']} 词={s['word']} 连线={s['links']} "
              f"位置=「{s['crumbDomain']} › {s['crumbRoot']}」高亮={s['highlighted']}")
        if s["word"] == 0:
            print("[FAIL] 搜单词后词族层没有可见单词")
            fails.append(1)
        if s["root"] or s["domain"]:
            print(f"[FAIL] 搜单词后父层节点仍可见（根 {s['root']} / 域 {s['domain']}）")
            fails.append(1)
        if not s["crumbRoot"].strip():
            print("[FAIL] 搜单词后导航条没写当前词根")
            fails.append(1)

        # --- 搜一个词根：按设计直接进词族层 ---
        hit = search(page, "spect")
        s = page.evaluate(STATE_JS)
        print(f"\n搜「spect」→ 命中 {hit}")
        print(f"  域={s['domain']} 根={s['root']} 词={s['word']} 连线={s['links']} "
              f"位置=「{s['crumbDomain']} › {s['crumbRoot']}」")
        if s["word"] == 0:
            print("[FAIL] 搜词根后没有进到词族层")
            fails.append(1)
        if s["root"]:
            print(f"[FAIL] 搜词根后词根节点仍可见（{s['root']} 个）")
            fails.append(1)

        # --- 搜中文 ---
        hit = search(page, "压力")
        s = page.evaluate(STATE_JS)
        print(f"\n搜「压力」→ 命中 {hit}")
        print(f"  域={s['domain']} 根={s['root']} 词={s['word']} "
              f"位置=「{s['crumbDomain']} › {s['crumbRoot']}」")
        if s["word"] == 0 and s["root"] == 0 and s["domain"] == 0:
            print("[FAIL] 搜中文后画面全空")
            fails.append(1)

        # --- 概念节点：已不上画面，但仍在搜索索引里，必须能落到某个词族 ---
        # 先回到第一层，否则"没反应"会被上一次的画面掩盖住
        for _ in range(2):
            page.evaluate("document.getElementById('nav-back')?.click()")
            page.wait_for_timeout(1500)
        before = page.evaluate(STATE_JS)
        hit = search(page, "施加压力")
        s = page.evaluate(STATE_JS)
        print(f"\n搜概念「施加压力」→ 命中 {hit}")
        print(f"  跳转前 域={before['domain']} 词={before['word']} / "
              f"跳转后 域={s['domain']} 根={s['root']} 词={s['word']} "
              f"位置=「{s['crumbDomain']} › {s['crumbRoot']}」高亮={s['highlighted']}")
        if s["word"] == 0:
            print("[FAIL] 搜概念后没落到词族层（概念节点不上画面，点了等于没反应）")
            fails.append(1)
        if s["highlighted"] == "(none)":
            print("[FAIL] 搜概念后没有高亮任何成员词，看不出命中的是哪个词")
            fails.append(1)

        # --- 回退键在搜索直达之后仍然可用 ---
        page.evaluate("document.getElementById('nav-back')?.click()")
        page.wait_for_timeout(2000)
        s = page.evaluate(STATE_JS)
        print(f"\n搜索后回退 → 域={s['domain']} 根={s['root']} 词={s['word']}")
        if s["root"] == 0 and s["domain"] == 0:
            print("[FAIL] 搜索直达后回退落到空画面")
            fails.append(1)

        if errors:
            print(f"\n[FAIL] 页面错误: {errors[:3]}")
            fails.append(1)
        else:
            print("\n[PASS] 无 pageerror")
        browser.close()

    if fails:
        print(f"搜索直达: {len(fails)} 项不通过 ❌")
        return 1
    print("搜索直达: 全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/frontend/"))
