#!/usr/bin/env python3
"""手工探针：把三层钻取走一遍，打印每层可见的节点/连线/导航条状态。

不是 CI 测试（回归断言在 tests/smoke_drill.py），只用来人眼确认画面对不对。
用法：python scripts/drill_probe.py [url]
"""
import sys
import time
from playwright.sync_api import sync_playwright

COUNT_JS = """() => {
  // SVG 节点/连线靠 opacity 隐藏，HTML 图例靠 display:none —— 两套判据都要顾，
  // 只看 opacity 会把 display:none 的图例项也数进来。
  const vis = (s) => [...document.querySelectorAll(s)]
    .filter((e) => e.getAttribute('opacity') !== '0').length;
  const shown = (s) => [...document.querySelectorAll(s)]
    .filter((e) => e.offsetParent !== null).length;
  const bar = document.getElementById('nav-bar');
  const crumb = document.getElementById('nav-crumb');
  const labels = [...document.querySelectorAll('#nav-crumb > span')]
    .map((e) => e.textContent.trim()).filter(Boolean);
  return {
    domain: vis('.node.domain'),
    root: vis('.node.root'),
    concept: vis('.node.concept'),
    word: vis('.node.word'),
    links: vis('.link'),
    nav: bar.classList.contains('hidden') ? '(hidden)'
         : (labels.length ? labels.join(' | ') : '(no crumb)'),
    legend: shown('#legend .legend-item'),
    hint: document.getElementById('hint').textContent,
  };
}"""

CLICK_FIRST_VISIBLE = """(sel) => {
  const el = [...document.querySelectorAll(sel)]
    .find((e) => e.getAttribute('opacity') !== '0');
  if (el) el.dispatchEvent(new MouseEvent('click', {bubbles: true}));
  return !!el;
}"""


def show(label, c):
    print(f"{label}  域={c['domain']} 根={c['root']} 概念={c['concept']} "
          f"词={c['word']} 连线={c['links']} 图例={c['legend']}")
    print(f"    导航条: {c['nav']}")
    print(f"    提示  : {c['hint']}")


def main(url):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url, wait_until="domcontentloaded")
        for _ in range(60):
            if pg.evaluate("document.querySelectorAll('.node.domain').length") > 0:
                break
            time.sleep(0.5)
        time.sleep(2)
        show("L1 语义域层", pg.evaluate(COUNT_JS))

        pg.evaluate(CLICK_FIRST_VISIBLE, ".node.domain")
        time.sleep(2.5)
        show("L2 词根层  ", pg.evaluate(COUNT_JS))

        pg.evaluate(CLICK_FIRST_VISIBLE, ".node.root")
        time.sleep(2.5)
        show("L3 词族层  ", pg.evaluate(COUNT_JS))

        pg.click("#nav-back")
        time.sleep(2)
        show("回退→L2   ", pg.evaluate(COUNT_JS))

        pg.click("#nav-back")
        time.sleep(2)
        show("回退→L1   ", pg.evaluate(COUNT_JS))

        print("pageerrors:", errs or "(none)")
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/frontend/"))
