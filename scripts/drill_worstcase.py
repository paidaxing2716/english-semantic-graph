#!/usr/bin/env python3
"""最密视图的重叠/裁切检查。

visual_audit 只抽第一个语义域的第一个词根（29 根 / 16 词），而实际最密的是
感知与记录（51 根）和 ponere（26 词）。钻取模型下每层只画一层，密度上限就落在
这两个视图上——抽样测不到它们，所以单独跑。

判据与 visual_audit 一致：圆心距 < 半径和 × 0.85 记为重叠。
用法：python scripts/drill_worstcase.py [url]
"""
import sys
import time
from playwright.sync_api import sync_playwright

MEASURE_JS = """() => {
  const pts = [];
  document.querySelectorAll('.node').forEach((g) => {
    if (g.getAttribute('opacity') === '0') return;
    const c = g.querySelector('circle');
    if (!c) return;
    const b = g.getBoundingClientRect();
    pts.push({
      x: b.left + b.width / 2,
      y: b.top + b.height / 2,
      r: parseFloat(c.getAttribute('r')) || 0,
      label: (g.querySelector('text') || {}).textContent || '',
    });
  });
  let overlap = 0, worstPair = '';
  for (let i = 0; i < pts.length; i++) {
    for (let j = i + 1; j < pts.length; j++) {
      const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < (pts[i].r + pts[j].r) * 0.85) {
        overlap++;
        if (!worstPair) worstPair = pts[i].label + ' / ' + pts[j].label;
      }
    }
  }
  // 标签是否被画布裁切
  const svg = document.querySelector('#graph').getBoundingClientRect();
  let clipped = 0, worstClip = '';
  document.querySelectorAll('.node').forEach((g) => {
    if (g.getAttribute('opacity') === '0') return;
    const t = g.querySelector('text');
    if (!t) return;
    const b = t.getBoundingClientRect();
    if (b.width === 0) return;
    if (b.left < svg.left - 1 || b.right > svg.right + 1
        || b.top < svg.top - 1 || b.bottom > svg.bottom + 1) {
      clipped++;
      if (!worstClip) worstClip = t.textContent;
    }
  });
  return {visible: pts.length, overlap, worstPair, clipped, worstClip};
}"""

# 按中文名进入语义域，再按词根名进入词族
ENTER_DOMAIN_JS = """(name) => {
  const g = [...document.querySelectorAll('.node.domain')]
    .find((e) => (e.querySelector('text') || {}).textContent === name);
  if (g) g.dispatchEvent(new MouseEvent('click', {bubbles: true}));
  return !!g;
}"""

ENTER_ROOT_JS = """(name) => {
  const g = [...document.querySelectorAll('.node.root')]
    .filter((e) => e.getAttribute('opacity') !== '0')
    .find((e) => (e.querySelector('text') || {}).textContent === name);
  if (g) g.dispatchEvent(new MouseEvent('click', {bubbles: true}));
  return !!g;
}"""

CASES = [
    # (语义域, 词根 or None, 说明)
    ("感知与记录", None, "L2 最密：51 个词根"),
    ("形态与安放", "ponere", "L3 最密：26 个单词"),
]

VIEWPORTS = [(1440, 900, "桌面 1440px"), (390, 844, "手机 390px")]


def main(url):
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vw, vh, vlabel in VIEWPORTS:
            page = browser.new_context(viewport={"width": vw, "height": vh}).new_page()
            page.goto(url, wait_until="domcontentloaded")
            deadline = time.time() + 30
            while time.time() < deadline:
                if page.evaluate("document.querySelectorAll('.node.domain').length") > 0:
                    break
                time.sleep(0.3)
            page.wait_for_timeout(2000)
            print(f"\n===== {vlabel} =====")

            for dm, rt, note in CASES:
                if not page.evaluate(ENTER_DOMAIN_JS, dm):
                    print(f"[SKIP] 找不到语义域「{dm}」")
                    continue
                page.wait_for_timeout(2600)
                if rt:
                    if not page.evaluate(ENTER_ROOT_JS, rt):
                        print(f"[SKIP] 在「{dm}」下找不到词根「{rt}」")
                        page.evaluate(
                            "document.getElementById('nav-back')?.click()")
                        page.wait_for_timeout(1800)
                        continue
                    page.wait_for_timeout(2600)

                m = page.evaluate(MEASURE_JS)
                tag = "PASS" if not m["overlap"] and not m["clipped"] else "FAIL"
                print(f"[{tag}] {note} → 可见 {m['visible']} 节点，"
                      f"重叠 {m['overlap']} 对，裁切 {m['clipped']} 个")
                if m["overlap"]:
                    print(f"       重叠示例: {m['worstPair']}")
                if m["clipped"]:
                    print(f"       裁切示例: {m['worstClip']}")
                if tag == "FAIL":
                    fails.append(f"{vlabel} · {note}")

                # 回到第一层，准备下一个用例
                for _ in range(2):
                    page.evaluate("document.getElementById('nav-back')?.click()")
                    page.wait_for_timeout(1600)
            page.close()
        browser.close()

    print()
    if fails:
        print(f"最密视图检查: {len(fails)} 项不通过 ❌")
        for f in fails:
            print("  -", f)
        return 1
    print("最密视图检查: 全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/frontend/"))
