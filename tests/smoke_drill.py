#!/usr/bin/env python3
"""v0.3 三层钻取回归测试。

守的是这次改动的核心诉求：点进某一层后，父节点不许留在画面上——否则每个子节点
都跟它连一根线，又变回那坨放射状的刺球。

因此断言写在"可见连线数"和"父节点是否可见"上，而不是"某个函数被调用了"：
前者是用户真正看到的东西，后者换个实现就失效。

用法：python tests/smoke_drill.py [url]
"""
import sys
import time
from playwright.sync_api import sync_playwright

# 计数口径：SVG 节点/连线用 opacity 隐藏，HTML 图例用 display:none
COUNT_JS = """() => {
  const vis = (s) => [...document.querySelectorAll(s)]
    .filter((e) => e.getAttribute('opacity') !== '0').length;
  const shown = (s) => [...document.querySelectorAll(s)]
    .filter((e) => e.offsetParent !== null).length;
  const bar = document.getElementById('nav-bar');
  return {
    domain: vis('.node.domain'),
    root: vis('.node.root'),
    concept: vis('.node.concept'),
    word: vis('.node.word'),
    links: vis('.link'),
    navHidden: !bar || bar.classList.contains('hidden'),
    crumbRoot: (document.querySelector('.crumb-root') || {}).textContent || '',
    crumbDomain: (document.querySelector('.crumb-domain') || {}).textContent || '',
    legend: shown('#legend .legend-item'),
    backBtn: !!document.getElementById('nav-back'),
  };
}"""

CLICK_FIRST_VISIBLE = """(sel) => {
  const el = [...document.querySelectorAll(sel)]
    .find((e) => e.getAttribute('opacity') !== '0');
  if (el) el.dispatchEvent(new MouseEvent('click', {bubbles: true}));
  return !!el;
}"""

# 详情面板换词后必须回到顶部。
# 滚动容器是 #detail-panel 本身（不是 #detail-content），而 showDetail 只换内容，
# 于是上一个词看到哪、下一个词就从哪开始 —— 新词的标题在视口外，看到的是例句区。
# 桌面实测残留 507px、手机 905px（几乎整屏）。
#
# 断言前先确认面板真的能滚：若 scrollable 为假，scrollTop 恒为 0，
# 这条检查就变成永真的空转，回归了也发现不了。
CLICK_NTH_WORD = """(n) => {
  const ws = [...document.querySelectorAll('.node.word')]
    .filter((e) => e.getAttribute('opacity') !== '0');
  if (!ws[n]) return null;
  ws[n].dispatchEvent(new MouseEvent('click', {bubbles: true}));
  return true;
}"""

PANEL_STATE = """() => {
  const p = document.querySelector('#detail-panel');
  if (!p) return null;
  return {
    top: p.scrollTop,
    scrollable: p.scrollHeight > p.clientHeight + 2,
    title: ((document.querySelector('.detail-title') || {}).textContent || '')
      .trim().split(/\\s+/)[0],
  };
}"""

SCROLL_PANEL_BOTTOM = """() => {
  const p = document.querySelector('#detail-panel');
  if (p) p.scrollTop = p.scrollHeight;
}"""


def wait_settle(page, ms=2200):
    """等力导向收敛 + 切层的 300ms 缩放过渡跑完。"""
    page.wait_for_timeout(ms)


def check(ok_list, cond, msg):
    if cond:
        return True
    print(f"[FAIL] {msg}")
    ok_list.append(False)
    return False


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
        # C 方案默认进入回想卡；钻取回归从关系地图入口开始。
        page.click('.mode-btn[data-mode="explore"]')
        wait_settle(page)

        # --- L1 语义域层 ---
        c = page.evaluate(COUNT_JS)
        print(f"[L1] 域={c['domain']} 根={c['root']} 概念={c['concept']} "
              f"词={c['word']} 连线={c['links']}")
        check(fails, c["domain"] > 0, "L1 没有可见的语义域节点")
        check(fails, c["root"] == 0, f"L1 不该出现词根节点（有 {c['root']} 个）")
        # 概念节点（尤其恒可见的 cluster）会各自拉一圈成员词，是放射状连线的来源
        check(fails, c["concept"] == 0, f"L1 不该出现概念节点（有 {c['concept']} 个）")
        check(fails, c["links"] == 0, f"L1 不该有连线（有 {c['links']} 条）")
        check(fails, c["navHidden"], "L1 是顶层，导航条该隐藏")

        # --- L1 → L2 词根层 ---
        page.evaluate(CLICK_FIRST_VISIBLE, ".node.domain")
        wait_settle(page)
        c = page.evaluate(COUNT_JS)
        print(f"[L2] 域={c['domain']} 根={c['root']} 概念={c['concept']} "
              f"词={c['word']} 连线={c['links']} 位置=「{c['crumbDomain']}」")
        check(fails, c["root"] > 0, "L2 没有可见的词根节点")
        # 这条就是本次改动的核心：父节点必须离开画面
        check(fails, c["domain"] == 0, f"L2 仍有语义域节点可见（{c['domain']} 个），放射状连线会回来")
        check(fails, c["concept"] == 0, f"L2 不该出现概念节点（有 {c['concept']} 个）")
        check(fails, c["links"] == 0, f"L2 该是零连线（有 {c['links']} 条）")
        check(fails, not c["navHidden"], "L2 该显示导航条")
        check(fails, c["backBtn"], "L2 缺回退按钮")
        check(fails, c["crumbDomain"].strip() != "", "L2 导航条没写当前语义域")
        check(fails, c["legend"] > 0, "图例全灭——visual_audit 会因此挂掉")

        # --- L2 → L3 词族层 ---
        page.evaluate(CLICK_FIRST_VISIBLE, ".node.root")
        wait_settle(page)
        c = page.evaluate(COUNT_JS)
        print(f"[L3] 域={c['domain']} 根={c['root']} 概念={c['concept']} "
              f"词={c['word']} 连线={c['links']} 位置=「{c['crumbRoot']}」")
        check(fails, c["word"] > 0, "L3 没有可见的单词节点")
        check(fails, c["root"] == 0, f"L3 仍有词根节点可见（{c['root']} 个），放射状连线会回来")
        check(fails, c["domain"] == 0, f"L3 仍有语义域节点可见（{c['domain']} 个）")
        check(fails, c["concept"] == 0, f"L3 不该出现概念节点（有 {c['concept']} 个）")
        # 词根圈没了，当前词根只能靠导航条交代——这是用户明确要的
        check(fails, c["crumbRoot"].strip() != "", "L3 导航条没写当前词根")
        check(fails, c["legend"] > 0, "图例全灭——visual_audit 会因此挂掉")

        # --- 详情面板换词后回到顶部 ---
        if page.evaluate(CLICK_NTH_WORD, 0):
            page.wait_for_timeout(600)
            page.evaluate(SCROLL_PANEL_BOTTOM)
            page.wait_for_timeout(250)
            a = page.evaluate(PANEL_STATE)
            page.evaluate(CLICK_NTH_WORD, 1)
            page.wait_for_timeout(600)
            b = page.evaluate(PANEL_STATE)
            print(f"[详情面板] 滚到底 {a['top']}px（可滚={a['scrollable']}）→ 换词后 {b['top']}px")
            check(fails, a["scrollable"],
                  "详情面板不可滚动，这条断言等于空转——换个视口或更长的词条再测")
            check(fails, a["top"] > 0, "面板没滚动起来，断言前提不成立")
            check(fails, a["title"] != b["title"],
                  f"没换词（都是「{a['title']}」），滚动位置检查无意义")
            check(fails, b["top"] == 0,
                  f"换词后详情面板仍停在 {b['top']}px，新词的标题在视口外")
        else:
            check(fails, False, "L3 没有可点的单词节点，无法验证详情面板滚动位置")

        # --- 回退 L3 → L2 ---
        page.click("#nav-back")
        wait_settle(page)
        c = page.evaluate(COUNT_JS)
        print(f"[回退→L2] 根={c['root']} 词={c['word']} 连线={c['links']}")
        check(fails, c["root"] > 0, "从 L3 回退后没有词根节点")
        check(fails, c["word"] == 0, f"从 L3 回退后仍残留 {c['word']} 个单词节点")

        # --- 回退 L2 → L1 ---
        page.click("#nav-back")
        wait_settle(page)
        c = page.evaluate(COUNT_JS)
        print(f"[回退→L1] 域={c['domain']} 根={c['root']} 连线={c['links']}")
        check(fails, c["domain"] > 0, "从 L2 回退后没有语义域节点")
        check(fails, c["root"] == 0, f"从 L2 回退后仍残留 {c['root']} 个词根节点")
        check(fails, c["navHidden"], "回到 L1 后导航条该重新隐藏")

        if errors:
            print(f"[FAIL] 页面错误 {len(errors)} 个:")
            for e in errors[:5]:
                print("   ", e[:200])
            fails.append(False)
        else:
            print("[PASS] 无 pageerror")

        browser.close()

    if fails:
        print(f"钻取测试: {len(fails)} 项不通过 ❌")
        return 1
    print("钻取测试: 全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/frontend/"))
