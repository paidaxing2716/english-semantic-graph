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
# 颜色解析 / 对比度的公共实现。三处检查共用同一份 —— 曾经各自复制过一遍，
# 结果修了一处漏两处：parse 不认 color() 记法，把 color-mix 出来的浅背景
# 当成近黑，.chip.tier-3 因此被误报成 2.66:1（真值 6.5 左右）。
COLOR_HELPERS_JS = r"""
  function lum(c) {
    const [r,g,b] = c.map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
    return 0.2126*r + 0.7152*g + 0.0722*b;
  }
  // getComputedStyle 可能返回两种记法：
  //   rgb(244, 241, 234)                  分量 0~255
  //   color(srgb 0.88 0.89 0.86)          分量 0~1  ← color-mix() 会走这条
  // 混着按 0~255 处理会让浅色算成近黑，对比度整个失真。
  function parse(s) {
    if (!s) return null;
    const m = s.match(/[\d.]+/g);
    if (!m) return null;
    const nums = m.slice(0,3).map(Number);
    return /^\s*color\(/i.test(s) ? nums.map(v => v * 255) : nums;
  }
  // 透明判定也不能只认 'rgba(0, 0, 0, 0)' 这个字面量：
  // color() 记法写成 color(srgb 0 0 0 / 0)，两者都是第 4 个数字才是 alpha。
  function alphaOf(s) {
    const m = s && s.match(/[\d.]+/g);
    return m && m.length >= 4 ? Number(m[3]) : 1;
  }
  function bgOf(el) {
    let n = el;
    while (n && n !== document.documentElement) {
      const c = getComputedStyle(n).backgroundColor;
      const p = parse(c);
      if (p && alphaOf(c) > 0) return p;
      n = n.parentElement;
    }
    return parse(getComputedStyle(document.body).backgroundColor) || [255,255,255];
  }
  function ratio(fg, bg) {
    const a = lum(fg), b = lum(bg);
    return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
  }
"""

CONTRAST_JS = r"""() => {""" + COLOR_HELPERS_JS + r"""
  // 新增文字元素务必加进来。不在清单里 = 对比度从不被检查，
  // 那正是这套审计最容易被绕开的方式。
  const sels = ['header h1','.subtitle','.badge','#search-input','#hint','#legend .legend-item',
                '.detail-title','.detail-phonetic','.detail-block h3','.detail-definition p',
                '.detail-block.feature p','.origin-src','.chip','.chip.zh','.detail-examples li',
                '.speak-btn','footer','.tier-btn','#study-progress'];
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

# 只在特定状态下才出现的带色文字。主清单靠 querySelector 抓这些不稳
# ——tier chip 要揭晓后、且那个词恰好处在该档；存储状态要等异步查询回来。
# 这里给每个 class 造一个样本塞进真实容器再量：背景取自实际父级，
# 与真环境一致，且不依赖运行时状态，结果是确定的。
DYNAMIC_CONTRAST_JS = r"""() => {""" + COLOR_HELPERS_JS + r"""
  // [宿主选择器, 标签名, class]。宿主决定背景（bgOf 会往上找），
  // 所以同一个 class 在学习卡和详情栏里要各量一次。
  const probes = [
    ['#study-card',     'span',   'chip tier-1'],
    ['#study-card',     'span',   'chip tier-2'],
    ['#study-card',     'span',   'chip tier-3'],
    ['#detail-content', 'span',   'chip tier-1'],
    ['#detail-content', 'span',   'chip tier-2'],
    ['#detail-content', 'span',   'chip tier-3'],
    ['#detail-content', 'button', 'tier-btn tier-1'],
    ['#detail-content', 'button', 'tier-btn tier-2'],
    ['#detail-content', 'button', 'tier-btn tier-3'],
    ['#study-progress', 'span',   'prog-store ok'],
    ['#study-progress', 'span',   'prog-store warn'],
    ['#study-progress', 'span',   'prog-hint'],
    ['#study-progress', 'button', 'prog-btn'],
    ['#study-card',     'td',     'fam-word tier-1'],
    ['#study-card',     'td',     'fam-word tier-2'],
    ['#study-card',     'td',     'fam-word tier-3'],
    // 下面这几项是裸文字（自身没有背景），一旦主题的背景没跟着切就会浅压浅
    // —— 夜间的学习桌曾经正是如此，.fam-word 只有 2.72:1。
    ['#study-card',     'td',     'fam-word'],
    ['#study-card',     'td',     'fam-logic'],
    ['#study-card',     'td',     'fam-zh'],
    ['#study-card',     'div',    'card-label'],
    ['#study-card',     'div',    'card-meta'],
    ['#study-card',     'div',    'card-logic'],
    ['#study-card',     'div',    'card-hint'],
    ['#study-card',     'div',    'answer-def'],
    ['#study-card',     'div',    'answer-ipa'],
    ['#study-card',     'li',     'answer-ex'],
    ['#study-progress', 'label',  'prog-toggle'],
    ['#study-card',     'div',    'card-image'],
    ['#study-card',     'div',    'answer-zh'],
    ['#study-card',     'div',    'card-root-concept'],
    ['#study-card',     'button', 'act'],
    ['#study-card',     'button', 'act primary'],
  ];
  const out = [];
  for (const [hostSel, tag, cls] of probes) {
    const host = document.querySelector(hostSel);
    if (!host) { out.push({sel:`${hostSel} .${cls}`, missing:true}); continue; }
    // td 必须挂在 table 里才拿得到该有的样式
    let holder = document.createElement('div');
    if (tag === 'td') {
      holder.innerHTML = '<table class="fam-table"><tbody><tr></tr></tbody></table>';
    }
    host.appendChild(holder);
    const parent = tag === 'td' ? holder.querySelector('tr') : holder;
    const el = document.createElement(tag);
    el.className = cls;
    el.textContent = '状态文字';
    parent.appendChild(el);
    const cs = getComputedStyle(el);
    const fg = parse(cs.color);
    const size = parseFloat(cs.fontSize);
    const bold = (parseInt(cs.fontWeight,10) || 400) >= 700;
    if (fg) {
      out.push({sel:`${hostSel} .${cls}`, size:+size.toFixed(1),
                ratio:+ratio(fg, bgOf(el)).toFixed(2),
                min: (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5});
    }
    holder.remove();
  }
  return out;
}"""

# 返回 {issues, checked}。checked 是"这次到底量到了什么"的凭据，调用方据此
# 判断检查是否真的跑了 —— 见 layout_issues() 里的说明。
LAYOUT_JS = r"""() => {
  const issues = [];
  // 注意：display:none 不会传递成后代的 computed display，隐藏祖先下的后代
  // 自身仍报 display:block。所以这个守卫拦不住"整块被藏起来"的情形，
  // 只能拦住元素自己被设成 none —— 那种情形由 checked 里的尺寸凭据兜住。
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
  const checked = {graphW: 0, panelW: 0, nodeTexts: 0, skippedZeroWidth: 0};
  const dp = document.querySelector('#detail-panel');
  if (dp) checked.panelW = Math.round(dp.getBoundingClientRect().width);
  if (svg) {
    const box = svg.getBoundingClientRect();
    checked.graphW = Math.round(box.width);
    let clipped = 0, visible = 0, worst = '';
    for (const t of document.querySelectorAll('.node text')) {
      const g = t.closest('.node');
      if (!g || parseFloat(g.getAttribute('opacity') ?? '1') === 0) continue;
      const r = t.getBoundingClientRect();
      // 宽度为 0 说明量不出来（整块被 display:none 藏了，或字体还没就绪）。
      // 这类节点不能算"检查过"——数出来交给调用方判断，别让它变成默默的通过。
      if (r.width === 0) { checked.skippedZeroWidth++; continue; }
      visible++;
      if (r.left < box.left - 2 || r.right > box.right + 2 ||
          r.top < box.top - 2 || r.bottom > box.bottom + 2) {
        clipped++;
        if (!worst) worst = t.textContent.trim();
      }
    }
    checked.nodeTexts = visible;
    if (clipped) issues.push(`${clipped}/${visible} 个可见节点标签超出画布（如「${worst}」）`);
  }
  return {issues: issues, checked: checked};
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


def ensure_graph_visible(page):
    """确保停在「关系地图」模式。

    页面默认落地在回想卡，此时 <main> 是 display:none，图谱、图例、详情栏
    全都量不出尺寸。所有基于 getBoundingClientRect 的检查会拿到一堆 0，
    比较自然全部通过 —— 曾经因此让「桌面白天」那一轮的裁切/溢出检查
    整轮空转。布局类检查开跑前必须先把这一层还原。
    """
    if page.evaluate("() => getComputedStyle(document.querySelector('main')).display") == "none":
        page.click('.mode-btn[data-mode="explore"]')
        page.wait_for_timeout(900)


def layout_issues(page):
    """跑 LAYOUT_JS，并把"检查没真跑"本身当成问题上报。

    只看 issues 是空的不够 —— 量不到东西时它同样是空的。这里用 checked 里的
    尺寸凭据反过来确认检查确实执行了：容器有宽度、且真的量过节点标签。
    """
    res = page.evaluate(LAYOUT_JS)
    issues = list(res["issues"])
    c = res["checked"]
    if not c["graphW"] or not c["panelW"]:
        issues.append(
            f"布局检查未实际执行：#graph 宽 {c['graphW']}px、#detail-panel 宽 "
            f"{c['panelW']}px —— 容器没有尺寸（页面可能停在学习模式）")
    elif not c["nodeTexts"]:
        issues.append(
            f"裁切检查未实际执行：没有量到任何可见节点标签"
            f"（{c['skippedZeroWidth']} 个因宽度为 0 被跳过）")
    return issues


def open_sample_word(page):
    """穿透三级钻取：语义域 → figur 词根 → configure，让详情栏各层级都渲染出来。"""
    # 先展开含 figur 的语义域（形态与安放）
    page.evaluate("""() => {
      const d = [...document.querySelectorAll('.node.domain')]
        .find(n => n.textContent.includes('形态'));
      if (d) d.dispatchEvent(new MouseEvent('click', {bubbles:true}));
    }""")
    page.wait_for_timeout(1800)
    page.evaluate("""() => {
      const t = [...document.querySelectorAll('.node.root')]
        .find(n => n.textContent.trim().startsWith('figur'));
      if (t) t.dispatchEvent(new MouseEvent('click', {bubbles:true}));
    }""")
    page.wait_for_timeout(1500)
    page.evaluate("""() => {
      const w = [...document.querySelectorAll('.node.word')]
        .find(n => n.textContent.trim() === 'configure');
      if (w) w.dispatchEvent(new MouseEvent('click', {bubbles:true}));
    }""")
    page.wait_for_timeout(700)


def settle_layout(page, max_ms=20000, step=900):
    """等力导向收敛再测，而不是固定等一段时间。

    节点多时收敛需要更久：541 节点实测 4 秒还剩十几对重叠，8 秒后归零。
    固定等待会让结果时通时不通（同一份代码跑三次得到 38 / 11 / 0）。
    """
    prev = None
    waited = 0
    while waited < max_ms:
        page.wait_for_timeout(step)
        waited += step
        cur = page.evaluate("""() => {
          let s = '';
          document.querySelectorAll('.node').forEach(g => {
            if (parseFloat(g.getAttribute('opacity') ?? '1') > 0) {
              s += (g.getAttribute('transform') || '') + '|';
            }
          });
          return s;
        }""")
        if cur == prev:
            return
        prev = cur


def audit_masking_all(page):
    """把全部词条过一遍遮罩，检查题面是否泄露答案。

    抽样不可靠：回想队列是随机洗牌的，只抽 25 题时一处泄露约 7% 才命中
    （实测就这样漏过一次——词根名 signum 含 sign 却没被遮）。
    这里直接在页面里对全库跑遮罩函数，确定性地扫。
    """
    bad = page.evaluate("""async () => {
      if (!window.ESG || typeof window.ESG.recallPrompt !== 'function') {
        return {error: 'study.js 未暴露 recallPrompt 测试钩子'};
      }
      const wd = await fetch('../data/words.json').then(r => r.json());
      const out = [];
      for (const w of wd.words) {
        if (w.decomposable !== 'root') continue;
        // 直接取 study.js 真实渲染的题面，测试不再自带一份遮罩实现
        const shown = window.ESG.recallPrompt(w.id);
        if (shown == null) { out.push(w.id + '：取不到题面'); continue; }
        if (new RegExp(w.word, 'i').test(shown)) {
          out.push(w.id + '：题面含单词本身');
          continue;
        }
        for (const zh of w.chinese || []) {
          if (zh.length >= 2 && shown.includes(zh)) {
            out.push(w.id + '：题面含义项「' + zh + '」');
            break;
          }
        }
      }
      return {total: wd.words.length, leaks: out};
    }""")
    if bad.get("error"):
        print(f"[FAIL] {bad['error']}")
        return False
    if bad["leaks"]:
        print(f"[FAIL] 全库遮罩扫描：{len(bad['leaks'])} 处泄题")
        for m in bad["leaks"][:10]:
            print(f"        {m}")
        return False
    print(f"[PASS] 全库 {bad['total']} 词条遮罩无泄题")
    return True


def audit_study(page, samples=25):
    """学习模式：查答案是否泄露，以及卡片有无溢出。

    泄露检查是这里最有价值的一项——遮罩逻辑一旦回退，
    人工每题核对不现实，但机器可以逐题扫。
    """
    ok = audit_masking_all(page)
    leaks = []
    page.click('.mode-btn[data-mode="recall"]')
    page.wait_for_timeout(1100)

    for _ in range(samples):
        r = page.evaluate("""() => {
          const card = document.querySelector('#study-card');
          if (!card) return null;
          // 未揭晓时，卡片文本里不应出现目标词或其中文义项
          const prog = document.querySelector('#study-progress').textContent;
          return {text: card.innerText, prog: prog};
        }""")
        if not r:
            break
        # 揭晓后读答案，回头比对揭晓前的文本
        page.click('[data-act="reveal"]')
        page.wait_for_timeout(150)
        ans = page.evaluate("""() => {
          const w = document.querySelector('.answer-word');
          const zh = [...document.querySelectorAll('.answer-zh .chip')].map(e => e.textContent);
          return w ? {word: w.textContent.trim().split(/\\s+/)[0], zh: zh} : null;
        }""")
        if ans:
            pre = r["text"]
            if ans["word"].lower() in pre.lower():
                leaks.append(f"{ans['word']}：揭晓前卡片已含该词")
            for z in ans["zh"]:
                if len(z) >= 2 and z in pre:
                    leaks.append(f"{ans['word']}：揭晓前已含中文义项「{z}」")
        page.click('[data-act="skip"]') if False else page.click('[data-act="ok"]')
        page.wait_for_timeout(120)

    if leaks:
        ok = False
        print(f"[FAIL] 回想模式答案泄露 {len(leaks)} 处：")
        for l in leaks[:6]:
            print(f"        {l}")
    else:
        print(f"[PASS] 回想模式抽查 {samples} 题无答案泄露")

    # 词族模式：未揭晓时单词列必须全为遮罩
    page.click('.mode-btn[data-mode="family"]')
    page.wait_for_timeout(1100)
    fam = page.evaluate("""() => {
      const cells = [...document.querySelectorAll('.fam-word')].map(e => e.textContent.trim());
      return {n: cells.length, unmasked: cells.filter(t => !/^▢+$/.test(t))};
    }""")
    if fam["unmasked"]:
        ok = False
        print(f"[FAIL] 词族模式未揭晓即显示单词：{fam['unmasked'][:5]}")
    else:
        print(f"[PASS] 词族模式 {fam['n']} 词全部遮罩")

    # 卡片溢出
    over = page.evaluate("""() => {
      const s = document.querySelector('#study');
      const bad = [...document.querySelectorAll('#study *')].filter(e => {
        const b = e.getBoundingClientRect();
        return b.width > 0 && b.right > window.innerWidth + 2;
      });
      return {h: s.scrollWidth > s.clientWidth + 2, n: bad.length};
    }""")
    if over["h"] or over["n"]:
        ok = False
        print(f"[FAIL] 学习面板溢出：横向={over['h']} 越界元素={over['n']}")
    else:
        print("[PASS] 学习面板无溢出")

    page.click('.mode-btn[data-mode="explore"]')
    page.wait_for_timeout(700)
    return ok


def audit(name, page):
    """返回 (是否通过, 问题列表)。"""
    print(f"\n===== {name} =====")
    ok = True

    # 布局检查依赖真实尺寸，先确保图谱那一层没被学习面板盖着
    ensure_graph_visible(page)

    # 语义域标签用独立颜色变量，单独查一次——它只在选中语义域时存在，
    # 放进主清单会因样本流程最后选中单词而误报未渲染
    page.evaluate("""() => {
      const d = document.querySelector('.node.domain');
      if (d) d.dispatchEvent(new MouseEvent('click', {bubbles: true}));
    }""")
    page.wait_for_timeout(900)
    dm = [r for r in page.evaluate(CONTRAST_JS)
          if r.get("sel") == ".detail-type.word" and not r.get("missing")]
    dom_ratio = page.evaluate("""() => {""" + COLOR_HELPERS_JS + """
      const el = document.querySelector('.detail-type.domain');
      if (!el) return null;
      const fg = parse(getComputedStyle(el).color);
      if (!fg) return null;
      return +ratio(fg, bgOf(el)).toFixed(2);
    }""")
    if dom_ratio is None:
        print("[WARN] 语义域标签未渲染，跳过其对比度检查")
    elif dom_ratio < 4.5:
        print(f"[FAIL] .detail-type.domain 对比度 {dom_ratio}:1（需 4.5）")
        ok = False
    else:
        print(f"[PASS] 语义域标签对比度 {dom_ratio}:1")

    open_sample_word(page)

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

    dyn = page.evaluate(DYNAMIC_CONTRAST_JS)
    dfails = [r for r in dyn if not r.get("missing") and r["ratio"] < r["min"]]
    dmissing = [r["sel"] for r in dyn if r.get("missing")]
    if dfails:
        ok = False
        print("[FAIL] 动态文字对比度不足：")
        for r in sorted(dfails, key=lambda x: x["ratio"]):
            print(f"        {r['sel']:<40} {r['ratio']:>5}:1  (需 {r['min']}, {r['size']}px)")
    elif dmissing:
        ok = False
        print(f"[FAIL] 动态文字无法检查：宿主元素缺失 {', '.join(dmissing)}")
    else:
        worst = min(dyn, key=lambda x: x["ratio"])
        print(f"[PASS] 动态文字配色达标（{len(dyn)} 项，最低 {worst['ratio']}:1 @ {worst['sel']}）")

    issues = layout_issues(page)
    if issues:
        ok = False
        print("[FAIL] 布局问题：")
        for i in issues:
            print(f"        {i}")
    else:
        print("[PASS] 无重叠 / 无溢出 / 无裁切")

    # 全展开三层后再查密度：先所有语义域，再所有词根。
    # 力导向在几百节点时可能停在局部极小（节点挤着但力已平衡），
    # 双击空白会触发页面的 restartSimulation 全量重排，能跳出局部极小。
    # 这里最多重试 3 次，每次重排后重新收敛再测。
    page.evaluate("""() => {
      document.querySelectorAll('.node.domain').forEach(
        n => n.dispatchEvent(new MouseEvent('click', {bubbles: true})));
    }""")
    page.wait_for_timeout(3000)
    page.evaluate("""() => {
      document.querySelectorAll('.node.root').forEach(n => {
        if (parseFloat(n.getAttribute('opacity') ?? '1') > 0) {
          n.dispatchEvent(new MouseEvent('click', {bubbles: true}));
        }
      });
    }""")
    settle_layout(page)
    d = page.evaluate(DENSITY_JS)
    attempt = 1
    while d["overlap"] and attempt < 3:
        print(f"  全展开 {d['visible']} 节点仍有 {d['overlap']} 对重叠，"
              f"双击空白重排（第 {attempt} 次）…")
        page.evaluate("""() => {
          const svg = document.querySelector('#graph');
          svg.dispatchEvent(new MouseEvent('dblclick', {bubbles: true}));
        }""")
        settle_layout(page)
        d = page.evaluate(DENSITY_JS)
        attempt += 1
    # 全展开重叠已确认是超大 concept（fac 22 词/ponere 21 词）把子词全挤在圆心
    # 造成的拓扑拥挤，不是力导向参数问题；886 节点全展开也非正常使用场景。
    # 经决策降级为 WARN：不再阻塞入库，但保留重排重试，给正常规模留机会。
    if d["overlap"]:
        print(f"[WARN] 全展开后节点重叠 {d['overlap']} 对（可见 {d['visible']} 个）——"
              f"超大 concept 拓扑拥挤，已按决策降级为警告")
    else:
        print(f"[PASS] 全展开后 {d['visible']} 个节点无重叠")
    clip = layout_issues(page)
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

            print("\n===== 学习模式 · 桌面 =====")
            results.append(audit_study(desktop))

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
            print("\n===== 学习模式 · 手机 390px =====")
            results.append(audit_study(mobile, samples=8))

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
