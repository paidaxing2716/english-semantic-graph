#!/usr/bin/env python3
"""English Semantic Graph — 前端视觉质量门

用真实浏览器渲染页面，量化检查肉眼难发现的问题：
- 文字对比度是否达到 WCAG AA（正文 4.5:1，大字 3:1）
- 顶栏 / 图例 / 详情栏是否重叠或横向溢出
- 力导向图的节点标签是否跑出画布（含中文长标签）

覆盖 桌面白天 / 桌面夜间 / 手机 390px 三个视口。

用法：
    python tests/visual_audit.py              # 自动起本地服务并审计
    python tests/visual_audit.py --port 8899  # 指定端口
    python tests/visual_audit.py --url http://127.0.0.1:8000/frontend/index.html

依赖 playwright（可选依赖，未安装时跳过而不算失败）：
    pip install playwright && playwright install chromium
"""

import argparse
import functools
import socket
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 需要检查对比度的文字元素（覆盖顶栏、画布脚注、详情栏各层级）
CONTRAST_JS = r"""() => {
  function lum(c) {
    const [r,g,b] = c.map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
    return 0.2126*r + 0.7152*g + 0.0722*b;
  }
  function parse(s) {
    const m = s.match(/[\d.]+/g);
    return m ? m.slice(0,3).map(Number) : null;
  }
  function bgOf(el) {
    let n = el;
    while (n && n !== document.documentElement) {
      const c = getComputedStyle(n).backgroundColor;
      const p = parse(c);
      if (p && !c.includes('rgba(0, 0, 0, 0)')) return p;
      n = n.parentElement;
    }
    return parse(getComputedStyle(document.body).backgroundColor) || [255,255,255];
  }
  function ratio(fg, bg) {
    const a = lum(fg), b = lum(bg);
    return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
  }
  const sels = ['header h1','.subtitle','.badge','#search-input','#hint','#legend .legend-item',
                '.detail-title','.detail-phonetic','.detail-block h3','.detail-definition p',
                '.detail-block.feature p','.origin-src','.chip','.chip.zh','.detail-examples li',
                '.speak-btn','footer'];
  const out = [];
  for (const s of sels) {
    const el = document.querySelector(s);
    if (!el) { out.push({sel:s, missing:true}); continue; }
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const fg = parse(cs.color);
    if (!fg) continue;
    const size = parseFloat(cs.fontSize);
    const bold = (parseInt(cs.fontWeight,10) || 400) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);   // WCAG 大字定义
    out.push({sel:s, size:+size.toFixed(1), ratio:+ratio(fg,bgOf(el)).toFixed(2),
              min: large ? 3 : 4.5});
  }
  return out;
}"""

LAYOUT_JS = r"""() => {
  const issues = [];
  const vis = s => {
    const el = document.querySelector(s);
    if (!el) return null;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return null;
    return el.getBoundingClientRect();
  };

  const sub = vis('.subtitle'), tools = vis('.header-tools');
  if (sub && tools && sub.right > tools.left + 1) issues.push('subtitle 与 header-tools 重叠');

  const lg = vis('#legend'), ht = vis('#hint');
  if (lg && ht && lg.right > ht.left + 1) issues.push('legend 与 hint 重叠');

  const p = document.querySelector('#detail-panel');
  if (p && p.scrollWidth > p.clientWidth + 2) {
    issues.push(`详情栏横向溢出 ${p.scrollWidth - p.clientWidth}px`);
  }

  for (const el of document.querySelectorAll('header *, #detail-content *')) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > window.innerWidth + 2) {
      issues.push(`${el.className || el.tagName} 超出视口右侧 ${Math.round(r.right - window.innerWidth)}px`);
      break;
    }
  }

  // 节点标签越界：隐藏节点用 opacity:0（非 display:none），必须排除否则误报
  const svg = document.querySelector('#graph');
  if (svg) {
    const box = svg.getBoundingClientRect();
    let clipped = 0, visible = 0, worst = '';
    for (const t of document.querySelectorAll('.node text')) {
      const g = t.closest('.node');
      if (!g || parseFloat(g.getAttribute('opacity') ?? '1') === 0) continue;
      const r = t.getBoundingClientRect();
      if (r.width === 0) continue;
      visible++;
      if (r.left < box.left - 2 || r.right > box.right + 2 ||
          r.top < box.top - 2 || r.bottom > box.bottom + 2) {
        clipped++;
        if (!worst) worst = t.textContent.trim();
      }
    }
    if (clipped) issues.push(`${clipped}/${visible} 个可见节点标签超出画布（如「${worst}」）`);
  }
  return issues;
}"""

# 密度检查：把所有词根展开，看节点是否挤成一团。
# 词量增长时这是最先失效的地方，且默认收起状态查不出来。
DENSITY_JS = r"""() => {
  const pts = [];
  document.querySelectorAll('.node').forEach(g => {
    if (parseFloat(g.getAttribute('opacity') ?? '1') === 0) return;
    const m = /translate\(([-\d.]+),([-\d.]+)\)/.exec(g.getAttribute('transform') || '');
    const c = g.querySelector('circle');
    if (m && c) pts.push({x: +m[1], y: +m[2], r: +c.getAttribute('r')});
  });
  let overlap = 0;
  for (let i = 0; i < pts.length; i++) {
    for (let j = i + 1; j < pts.length; j++) {
      const d = Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y);
      if (d < (pts[i].r + pts[j].r) * 0.85) overlap++;
    }
  }
  return {visible: pts.length, overlap: overlap};
}"""


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve(port):
    """在仓库根目录起静态服务，供页面 fetch ../data/*.json。"""
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def open_sample_word(page):
    """展开 figur 词根并打开 configure，让详情栏各层级都渲染出来。"""
    page.evaluate("""() => {
      const t = [...document.querySelectorAll('.node.root')]
        .find(n => n.textContent.trim().startsWith('figur'));
      if (t) t.dispatchEvent(new MouseEvent('click', {bubbles:true}));
    }""")
    page.wait_for_timeout(1300)
    page.evaluate("""() => {
      const w = [...document.querySelectorAll('.node.word')]
        .find(n => n.textContent.trim() === 'configure');
      if (w) w.dispatchEvent(new MouseEvent('click', {bubbles:true}));
    }""")
    page.wait_for_timeout(700)


def audit(name, page):
    """返回 (是否通过, 问题列表)。"""
    print(f"\n===== {name} =====")
    ok = True

    rows = page.evaluate(CONTRAST_JS)
    fails = [r for r in rows if not r.get("missing") and r["ratio"] < r["min"]]
    missing = [r["sel"] for r in rows if r.get("missing")]
    if fails:
        ok = False
        print("[FAIL] 对比度不足：")
        for r in sorted(fails, key=lambda x: x["ratio"]):
            print(f"        {r['sel']:<26} {r['ratio']:>5}:1  (需 {r['min']}, {r['size']}px)")
    else:
        print("[PASS] 对比度全部达标 WCAG AA")
    if missing:
        print(f"[WARN] 选择器未渲染（可能是改名或该视口隐藏）：{', '.join(missing)}")

    issues = page.evaluate(LAYOUT_JS)
    if issues:
        ok = False
        print("[FAIL] 布局问题：")
        for i in issues:
            print(f"        {i}")
    else:
        print("[PASS] 无重叠 / 无溢出 / 无裁切")

    # 展开全部词根后再查一次密度
    page.evaluate("""() => {
      document.querySelectorAll('.node.root').forEach(
        n => n.dispatchEvent(new MouseEvent('click', {bubbles: true})));
    }""")
    page.wait_for_timeout(3800)
    d = page.evaluate(DENSITY_JS)
    if d["overlap"]:
        ok = False
        print(f"[FAIL] 全展开后节点重叠 {d['overlap']} 对（可见 {d['visible']} 个）")
    else:
        print(f"[PASS] 全展开后 {d['visible']} 个节点无重叠")
    clip = page.evaluate(LAYOUT_JS)
    if clip:
        ok = False
        print("[FAIL] 全展开后布局问题：")
        for i in clip:
            print(f"        {i}")

    # 点词根会把详情栏换成词根内容，这里复位成单词，
    # 否则后续视口查不到 phonetic / chip / 例句等单词专属元素
    open_sample_word(page)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="已在运行的页面地址；不传则自动起本地服务")
    ap.add_argument("--port", type=int, help="自动起服务时使用的端口")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[SKIP] 未安装 playwright，跳过视觉审计。")
        print("       pip install playwright && playwright install chromium")
        return 0

    httpd = None
    url = args.url
    if not url:
        port = args.port or free_port()
        httpd = serve(port)
        url = f"http://127.0.0.1:{port}/frontend/index.html"
    print(f"审计目标：{url}")

    results = []
    errors = []
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception as e:
                print(f"[SKIP] 无法启动 Chromium：{str(e)[:120]}")
                print("       playwright install chromium")
                return 0

            desktop = browser.new_page(viewport={"width": 1440, "height": 900})
            desktop.on("pageerror", lambda e: errors.append(f"[桌面] {e}"))
            # 从白天基线开始，避免受本机 localStorage / 系统深色偏好影响
            # 仅在未设置时写入，否则会在 reload 时覆盖掉切换结果，误判持久化失败
            desktop.add_init_script(
                "try { if (!localStorage.getItem('esg-theme')) "
                "localStorage.setItem('esg-theme','day'); } catch (e) {}")
            desktop.goto(url, wait_until="networkidle")
            desktop.wait_for_timeout(2500)
            open_sample_word(desktop)
            results.append(audit("桌面 1440px · 白天", desktop))

            desktop.click("#theme-toggle")
            desktop.wait_for_timeout(700)
            if desktop.get_attribute("html", "data-theme") != "night":
                errors.append("主题切换未生效：data-theme 未变为 night")
            results.append(audit("桌面 1440px · 夜间", desktop))

            desktop.reload(wait_until="networkidle")
            desktop.wait_for_timeout(1500)
            if desktop.get_attribute("html", "data-theme") != "night":
                errors.append("主题未持久化：刷新后丢失夜间模式")
            desktop.close()

            mobile = browser.new_page(viewport={"width": 390, "height": 844},
                                      is_mobile=True, has_touch=True)
            mobile.on("pageerror", lambda e: errors.append(f"[手机] {e}"))
            mobile.add_init_script(
                "try { if (!localStorage.getItem('esg-theme')) "
                "localStorage.setItem('esg-theme','day'); } catch (e) {}")
            mobile.goto(url, wait_until="networkidle")
            mobile.wait_for_timeout(2400)
            open_sample_word(mobile)
            if not mobile.evaluate("() => document.querySelector('#detail-panel')"
                                   ".classList.contains('drawer-open')"):
                errors.append("手机端点击节点后底部抽屉未打开")
            results.append(audit("手机 390px · 白天", mobile))
            mobile.close()

            browser.close()
    finally:
        if httpd:
            httpd.shutdown()

    print()
    if errors:
        print("[FAIL] 运行时问题：")
        for e in errors:
            print(f"        {e}")
    if all(results) and not errors:
        print(f"[PASS] {len(results)} 个视口全部通过 ✅")
        return 0
    print("[FAIL] 存在视觉问题 ❌")
    return 1


if __name__ == "__main__":
    sys.exit(main())
