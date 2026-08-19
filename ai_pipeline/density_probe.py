#!/usr/bin/env python3
"""密度压力探测：用合成数据跑真实力导向布局，找出图谱在哪个规模失效。

不猜测、不外推——真在浏览器里渲染 N 词的图谱并测重叠。
合成数据只写到临时目录，不碰 data/。

用法：
    python ai_pipeline/density_probe.py                 # 默认几档规模
    python ai_pipeline/density_probe.py 100 500 2000
"""

import json
import shutil
import socket
import sys
import tempfile
import threading
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def synth(n_words, words_per_root=10, n_domains=16):
    """按当前数据模型生成 n_words 个合成词条。

    词根数 = n_words / words_per_root，与真实扩展方式一致：
    词量增长时词根数同步增长（5500 词不可能只靠 10 个词根）。
    语义域数量固定——这正是分组层的意义：默认层不随词量增长。
    """
    n_roots = max(1, round(n_words / words_per_root))
    roots, concepts, words, relations = [], [], [], []
    domains = [{"id": f"domain-{k:02d}", "name": f"domain {k}", "chinese": f"语义域{k}",
                "core_image": "合成语义域用于压力测试", "description": "合成",
                "root_ids": []} for k in range(min(n_domains, n_roots))]

    for i in range(n_roots):
        rid = f"root{i:03d}"
        fam = [f"word{i:03d}_{j}" for j in range(words_per_root)]
        roots.append({
            "id": rid, "root": rid, "origin": "合成", "core_concept": f"concept {i}",
            "core_image": "合成画面用于压力测试", "word_ids": fam,
        })
        concepts.append({
            "id": f"concept-{rid}", "concept": f"concept {i}", "chinese": f"合成概念{i}",
            "core_image": "合成画面用于压力测试", "root_ids": [rid], "word_ids": fam,
        })
        domains[i % len(domains)]["root_ids"].append(rid)
        for w in fam:
            words.append({
                "id": w, "word": w, "pos": "verb", "phonetic": "/x/", "root_ids": [rid],
                "root_logic": "合成", "origin": "合成", "native_definition": "synthetic",
                "core_concept": "synthetic", "core_image": "合成画面用于压力测试",
                "chinese": ["合成"], "examples": ["Synthetic example."],
                "synonyms": [], "antonyms": [], "related": [], "semantic_expansions": [],
            })
            relations.append({"from": rid, "to": w, "type": "root", "note": "合成"})

    return {
        "domains.json": {"schema_version": "0.1", "domains": domains},
        "roots.json": {"schema_version": "0.1", "roots": roots},
        "concepts.json": {"schema_version": "0.1", "concepts": concepts},
        "words.json": {"schema_version": "0.1", "words": words},
        "relations.json": {"schema_version": "0.1", "relations": relations},
        "examples.json": {"schema_version": "0.1", "examples": []},
    }, n_roots


MEASURE = r"""() => {
  const box = document.querySelector('#graph').getBoundingClientRect();
  const pts = [];
  let clipped = 0;
  document.querySelectorAll('.node').forEach(g => {
    if (parseFloat(g.getAttribute('opacity') ?? '1') === 0) return;
    const m = /translate\(([-\d.]+),([-\d.]+)\)/.exec(g.getAttribute('transform') || '');
    const c = g.querySelector('circle');
    if (m && c) pts.push({x: +m[1], y: +m[2], r: +c.getAttribute('r')});
    const t = g.querySelector('text');
    if (t) {
      const q = t.getBoundingClientRect();
      if (q.width && (q.left < box.left - 2 || q.right > box.right + 2 ||
                      q.top < box.top - 2 || q.bottom > box.bottom + 2)) clipped++;
    }
  });
  let overlap = 0;
  for (let i = 0; i < pts.length; i++) {
    for (let j = i + 1; j < pts.length; j++) {
      const d = Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y);
      if (d < (pts[i].r + pts[j].r) * 0.85) overlap++;
    }
  }
  const area = box.width * box.height;
  return {
    visible: pts.length, overlap: overlap, clipped: clipped,
    px_per_node: pts.length ? Math.round(area / pts.length) : 0,
  };
}"""


def settle(pg, max_ms=14000, step=700):
    """等到节点位置不再变化再测。
    固定等待会在布局未收敛时误报重叠——实测 5500 词等 2.8s 报 3 对，
    等够时间是 0 对。"""
    prev = None
    waited = 0
    while waited < max_ms:
        pg.wait_for_timeout(step)
        waited += step
        cur = pg.evaluate("""() => {
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


def probe(scales):
    from playwright.sync_api import sync_playwright

    tmp = Path(tempfile.mkdtemp(prefix="esg-density-"))
    try:
        shutil.copytree(ROOT / "frontend", tmp / "frontend")
        (tmp / "data").mkdir()

        port = free_port()
        httpd = ThreadingHTTPServer(
            ("127.0.0.1", port), functools.partial(Quiet, directory=str(tmp)))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{port}/frontend/index.html"

        print(f"{'词数':>6} {'词根':>5} | {'默认层':>7} {'重叠':>5}"
              f" | {'展开一域':>8} {'重叠':>5} | {'再展一族':>8} {'重叠':>5}")
        print("-" * 76)

        with sync_playwright() as p:
            b = p.chromium.launch()
            for n in scales:
                files, n_roots = synth(n)
                for name, obj in files.items():
                    (tmp / "data" / name).write_text(
                        json.dumps(obj, ensure_ascii=False), encoding="utf-8")

                pg = b.new_page(viewport={"width": 1440, "height": 900})
                pg.goto(url, wait_until="networkidle")
                settle(pg)
                base = pg.evaluate(MEASURE)

                # 三级钻取：先展开一个语义域
                pg.evaluate("""() => {
                  const d = document.querySelector('.node.domain');
                  if (d) d.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                }""")
                settle(pg)
                dom = pg.evaluate(MEASURE)

                # 再展开该域下的一个词根
                pg.evaluate("""() => {
                  const r = [...document.querySelectorAll('.node.root')]
                    .find(g => parseFloat(g.getAttribute('opacity') ?? '1') > 0);
                  if (r) r.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                }""")
                settle(pg)
                one = pg.evaluate(MEASURE)
                pg.close()

                print(f"{n:>6} {n_roots:>5} | {base['visible']:>7} {base['overlap']:>5}"
                      f" | {dom['visible']:>8} {dom['overlap']:>5}"
                      f" | {one['visible']:>8} {one['overlap']:>5}")
            b.close()
        httpd.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    scales = [int(x) for x in sys.argv[1:]] or [100, 300, 500, 1000, 2000, 5500]
    probe(scales)
