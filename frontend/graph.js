/* English Semantic Graph — D3 force-directed graph
 * 三级钻取：语义域 → 词根 → 单词。搜索可直达任意层。
 */
(function () {
  "use strict";

  const DATA_FILES = [
    { key: "domains", path: "../data/domains.json" },
    { key: "roots", path: "../data/roots.json" },
    { key: "concepts", path: "../data/concepts.json" },
    { key: "words", path: "../data/words.json" },
    { key: "relations", path: "../data/relations.json" },
  ];

  let nodes = [];
  let links = [];
  let simulation = null;
  let highlightedId = null; // 搜索定位的临时高亮（3 秒后消失）

  const svg = d3.select("#graph");
  const detailPanel = d3.select("#detail-panel");
  const detailEmpty = d3.select("#detail-empty");
  const detailContent = d3.select("#detail-content");
  const searchInput = d3.select("#search-input");
  const searchResults = d3.select("#search-results");

  // 移动端检测（<768px 与 CSS 断点一致）
  const mqMobile = window.matchMedia("(max-width: 768px)");
  function isMobile() { return mqMobile.matches; }

  function openDrawer() {
    if (isMobile()) detailPanel.classed("drawer-open", true);
  }
  function closeDrawer() {
    detailPanel.classed("drawer-open", false);
  }

  // ---------- 数据加载 ----------
  // 性能策略（v0.2.1）：
  //  1) 并行拉取所有数据文件 —— 旧实现串行 await，5 个文件的往返延迟
  //     逐个叠加（慢网络下实测 25s+）；并行后首次加载 ≈ 最慢那一个文件。
  //  2) IndexedDB 应用级缓存 —— GitHub Pages 的 HTTP 缓存只有 max-age=600，
  //     十分钟后冷访问就要全量重下。用 data/version.json（部署时自动生成
  //     的内容哈希）做版本键：二次访问只拉 ~100B 的版本号，命中即秒开。
  //  3) 加载进度提示 —— 不白屏干等。
  function isLocalDev() {
    const h = location.hostname;
    const local = h === "localhost" || h === "127.0.0.1" || h === "0.0.0.0" || h === "::1";
    if (!local) return false;
    // ?cache=1 强制启用缓存 —— 本地调试缓存行为 / CI 冒烟测试用。
    // 正常本地开发（http.server）不带此参数，始终读最新数据。
    return new URLSearchParams(location.search).get("cache") !== "1";
  }

  const IDB_NAME = "esg-data-cache";
  const IDB_STORE = "files";
  function idbOpen() {
    return new Promise((resolve, reject) => {
      try {
        const req = indexedDB.open(IDB_NAME, 1);
        req.onupgradeneeded = () => req.result.createObjectStore(IDB_STORE);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      } catch (e) { reject(e); }
    });
  }
  function idbGet(version) {
    return idbOpen().then((db) => new Promise((resolve) => {
      const tx = db.transaction(IDB_STORE, "readonly");
      const req = tx.objectStore(IDB_STORE).get(version);
      req.onsuccess = () => { db.close(); resolve(req.result || null); };
      req.onerror = () => { db.close(); resolve(null); };
    })).catch(() => null);
  }
  function idbPut(version, files) {
    return idbOpen().then((db) => new Promise((resolve) => {
      const tx = db.transaction(IDB_STORE, "readwrite");
      // 只保留最新版本，避免缓存随词库增长无限膨胀
      tx.objectStore(IDB_STORE).clear();
      tx.objectStore(IDB_STORE).put(files, version);
      tx.oncomplete = () => { db.close(); resolve(); };
      tx.onerror = () => { db.close(); resolve(); };
    })).catch(() => {});
  }

  async function fetchVersion() {
    try {
      const res = await fetch("../data/version.json", { cache: "no-store" });
      if (!res.ok) return null;
      const j = await res.json();
      return j.version || null;
    } catch (e) { return null; }
  }

  // 并行拉取全部数据文件；任一失败即整体失败，并带上出错文件信息
  async function fetchAllData(onProgress) {
    const entries = DATA_FILES.map((f, i) =>
      fetch(f.path)
        .then((res) => {
          if (!res.ok) throw new Error(`${f.path} → HTTP ${res.status}`);
          return res.json();
        })
        .then((j) => {
          if (onProgress) onProgress(i + 1, DATA_FILES.length);
          return [f.key, j];
        })
    );
    try {
      const results = await Promise.all(entries);
      const data = {};
      results.forEach(([k, v]) => { data[k] = v; });
      return data;
    } catch (e) {
      throw new Error(
        `无法加载词库数据（${e.message}）。\n\n` +
        `本地直接双击打开会有浏览器安全限制。请用本地服务器：\n` +
        `在仓库根目录运行：python3 -m http.server 8000\n` +
        `然后访问 http://localhost:8000/frontend/`
      );
    }
  }

  async function loadData() {
    const progressEl = document.getElementById("load-progress");
    const setProgress = (t) => { if (progressEl && t) progressEl.textContent = t; };

    setProgress("正在加载词库…");

    let version = null;
    // 本地开发（http.server / file://）跳过缓存，始终读最新数据
    if (!isLocalDev()) {
      try {
        version = await fetchVersion();
        if (version) {
          const cached = await idbGet(version);
          if (cached && cached.files) {
            setProgress("");
            return cached.files;
          }
        }
      } catch (e) { /* 缓存不可用则走网络 */ }
    }

    const data = await fetchAllData((done, total) => {
      setProgress(`正在加载词库 ${done}/${total}…`);
    });

    // 写入缓存（仅线上；version 来自上面的首次请求，不再多发一次）
    if (!isLocalDev() && version) {
      try {
        await idbPut(version, data);
      } catch (e) { /* 写缓存失败不影响本次使用 */ }
    }
    setProgress("");
    return data;
  }

  // ---------- 构建图数据 ----------
  function buildGraph(data) {
    const idMap = new Map();

    // 语义域节点（唯一默认可见的一层）
    // 三级钻取：语义域 → 词根 → 单词。默认层节点数由语义域数量决定，
    // 不随词根数增长——这是词表扩大后图谱仍可用的前提。
    const domainOfRoot = new Map();
    (data.domains?.domains || []).forEach((dm) => {
      idMap.set(dm.id, {
        id: dm.id,
        label: dm.chinese,
        type: "domain",
        name: dm.name,
        concept: dm.name,
        chinese: dm.chinese,
        image: dm.core_image,
        description: dm.description,
        roots: dm.root_ids || [],
        vizVisible: true,
        expanded: false,
      });
      (dm.root_ids || []).forEach((rid) => domainOfRoot.set(rid, dm.id));
    });

    const hasDomains = idMap.size > 0;

    // 词根节点（有语义域时默认隐藏，展开域后出现）
    data.roots.roots.forEach((r) => {
      const node = {
        id: r.id,
        label: r.root,
        type: "root",
        origin: r.origin,
        concept: r.core_concept,
        image: r.core_image,
        definition: r.english_definition,
        domain: domainOfRoot.get(r.id) || null,
        vizVisible: !hasDomains,
        expanded: false,
      };
      idMap.set(node.id, node);
    });

    // 概念节点（跟随其词根的可见性；cluster 聚合概念始终可见）
    data.concepts.concepts.forEach((c) => {
      const isCluster = c.type === "cluster";
      const node = {
        id: c.id,
        label: c.chinese,
        type: "concept",
        concept: c.concept,
        chinese: c.chinese,
        image: c.core_image,
        roots: c.root_ids,
        words: c.word_ids,
        isCluster: isCluster,
        vizVisible: isCluster || !hasDomains,
      };
      idMap.set(node.id, node);
    });

    // 单词节点（默认隐藏，展开词根时显示）
    data.words.words.forEach((w) => {
      const node = {
        id: w.id,
        label: w.word,
        type: "word",
        pos: w.pos,
        phonetic: w.phonetic,
        origin: w.origin,
        rootLogic: w.root_logic,
        decomposable: w.decomposable,
        decomposableNote: w.decomposable_note,
        definition: w.native_definition,
        concept: w.core_concept,
        image: w.core_image,
        chinese: w.chinese,
        examples: w.examples,
        synonyms: w.synonyms,
        antonyms: w.antonyms,
        related: w.related,
        expansions: w.semantic_expansions,
        roots: w.root_ids,
        synonymGroup: w.synonym_group,
        synonymNote: w.synonym_note,
        vizVisible: false,
      };
      idMap.set(node.id, node);
    });

    nodes = Array.from(idMap.values());

    // 边：关系数据
    links = data.relations.relations
      .filter((r) => idMap.has(r.from) && idMap.has(r.to))
      .map((r) => ({ source: r.from, target: r.to, type: r.type, note: r.note }));

    // 边：语义域 → 其下词根
    nodes.filter((n) => n.type === "domain").forEach((dm) => {
      (dm.roots || []).forEach((rid) => {
        if (idMap.has(rid)) {
          links.push({ source: dm.id, target: rid, type: "root", note: "语义域→词根" });
        }
      });
    });

    // 边：概念节点与其词根相连
    nodes.filter((n) => n.type === "concept" && n.roots).forEach((c) => {
      c.roots.forEach((rid) => {
        links.push({ source: rid, target: c.id, type: "root", note: "词根→概念" });
      });
    });

    // 边：单词与其所属词根相连
    nodes.filter((n) => n.type === "word" && n.roots).forEach((w) => {
      w.roots.forEach((rid) => {
        const exists = links.some(
          (l) => (l.source === rid || l.source === rid.id) && (l.target === w.id || l.target === w.id)
        );
        if (!exists) {
          links.push({ source: rid, target: w.id, type: "root", note: "词根→单词" });
        }
      });
    });

    // 边：cluster 聚合概念 → 组内单词（近义词组，不画词对词连线）
    nodes.filter((n) => n.type === "concept" && n.isCluster && n.words).forEach((c) => {
      c.words.forEach((wid) => {
        links.push({ source: c.id, target: wid, type: "context", note: "近义词组" });
      });
    });
  }

  // ---------- 分层钻取 ----------
  function visibleNodeIds() {
    return new Set(nodes.filter((n) => n.vizVisible).map((n) => n.id));
  }

  // 收起某个语义域：隐藏其下词根、概念，以及词根下已展开的单词
  function collapseDomain(dm) {
    dm.expanded = false;
    const rootIds = new Set(dm.roots || []);
    nodes.forEach((n) => {
      if (n.type === "root" && rootIds.has(n.id)) {
        n.vizVisible = false;
        n.expanded = false;
        nodes.forEach((m) => {
          if (m.type === "word" && m.roots && m.roots.includes(n.id)) {
            m.vizVisible = false;
          }
        });
      }
      if (n.type === "concept" && !n.isCluster && n.roots
          && n.roots.some((r) => rootIds.has(r))) {
        n.vizVisible = false;
      }
    });
  }

  // 展开/收起语义域：显示其下词根与对应概念。
  // 收起时连带收掉该域下已展开的词族，避免留下悬空的单词节点。
  function toggleDomain(d) {
    d.expanded = !d.expanded;

    // 手机端一次只展开一个语义域。词根数长到 60+ 后，全部域展开会让
    // 390px 画布同时出现 130 多个节点（实测已到重叠临界），而手机上
    // 本来也是一域一域地看。与词根层"一次一族"的处理保持一致。
    if (d.expanded && isMobile()) {
      nodes.forEach((n) => {
        if (n.type === "domain" && n.id !== d.id && n.expanded) {
          collapseDomain(n);
        }
      });
    }

    const rootIds = new Set(d.roots || []);
    const revealed = [];

    nodes.forEach((n) => {
      if (n.type === "root" && rootIds.has(n.id)) {
        n.vizVisible = d.expanded;
        if (d.expanded) {
          revealed.push(n);
        } else {
          // 收起域：该词根下的单词一并隐藏
          n.expanded = false;
          nodes.forEach((m) => {
            if (m.type === "word" && m.roots && m.roots.includes(n.id)) {
              m.vizVisible = false;
            }
          });
        }
      }
      if (n.type === "concept" && !n.isCluster && n.roots) {
        if (n.roots.some((r) => rootIds.has(r))) {
          n.vizVisible = d.expanded;
          if (d.expanded) revealed.push(n);
        }
      }
    });

    if (d.expanded) {
      revealed.forEach((n, i) => {
        n.fx = null;
        n.fy = null;
        const a = (i / Math.max(revealed.length, 1)) * Math.PI * 2;
        n.x = d.x + Math.cos(a) * 95;
        n.y = d.y + Math.sin(a) * 95;
      });
    }

    applyVisibility();
    settleLocally();
  }

  function toggleRoot(d) {
    d.expanded = !d.expanded;

    // 手机端一次只展开一个词根：100 词全展开时 390px 画布放不下
    // （实测 118 个节点会产生近百对圆重叠），且手机上本来就是一族一族地看。
    if (d.expanded && isMobile()) {
      nodes.forEach((n) => {
        if (n.type === "root" && n.id !== d.id && n.expanded) {
          n.expanded = false;
          nodes.forEach((m) => {
            if (m.type === "word" && m.roots && m.roots.includes(n.id)) {
              m.vizVisible = false;
            }
          });
        }
      });
    }
    // 展开/收起该词族。只放开这一簇单词去找位置，
    // 其余节点保持钉住，整张图不会跟着重排。
    const family = [];
    nodes.forEach((n) => {
      if (n.type === "word" && n.roots && n.roots.includes(d.id)) {
        n.vizVisible = d.expanded;
        family.push(n);
      }
    });
    if (d.expanded) {
      family.forEach((n, i) => {
        n.fx = null;
        n.fy = null;
        // 以词根为圆心撒开，避免全部挤在同一点起步
        const a = (i / Math.max(family.length, 1)) * Math.PI * 2;
        n.x = d.x + Math.cos(a) * 70;
        n.y = d.y + Math.sin(a) * 70;
      });
    }
    applyVisibility();
    settleLocally();
  }

  // 展开某层后重新收敛。
  // 必须先松开所有可见节点：若沿用 pinAll 的钉死状态，新出现的节点
  // 四周全是不可移动的邻居，碰撞永远解不开（实测词与词根圆心仅 20px，
  // 需要 34px）。可见节点数量已由语义域分层限住，整体重排代价很小。
  function settleLocally() {
    if (!simulation) return;
    nodes.forEach((n) => {
      if (n.vizVisible) { n.fx = null; n.fy = null; }
    });
    simulation.alpha(0.9).alphaTarget(0).restart();
  }

  // 展开某词根所属的语义域（搜索直达要穿透三层）
  function revealDomainOf(rootNode) {
    if (!rootNode || !rootNode.domain) return;
    const dm = nodes.find((n) => n.id === rootNode.domain);
    if (!dm || dm.expanded) return;
    dm.expanded = true;
    const rootIds = new Set(dm.roots || []);
    nodes.forEach((n) => {
      if (n.type === "root" && rootIds.has(n.id)) n.vizVisible = true;
      if (n.type === "concept" && !n.isCluster && n.roots
          && n.roots.some((r) => rootIds.has(r))) {
        n.vizVisible = true;
      }
      if ((n.type === "root" || n.type === "concept") && n.vizVisible
          && n.x == null) {
        n.x = dm.x;
        n.y = dm.y;
      }
    });
  }

  // 强制显示某节点（用于搜索直达）
  function revealNode(node) {
    if (node.vizVisible) return;

    // 词根：先展开它所属的语义域
    if (node.type === "root") {
      revealDomainOf(node);
    }

    // 单词：展开其所属词根，以及词根所在的语义域
    if (node.type === "word" && node.roots) {
      node.roots.forEach((rid) => {
        const root = nodes.find((n) => n.id === rid);
        if (root) {
          revealDomainOf(root);
          root.vizVisible = true;
          root.expanded = true;
          const family = nodes.filter(
            (n) => n.type === "word" && n.roots && n.roots.includes(rid)
          );
          family.forEach((n, i) => {
            n.vizVisible = true;
            if (n.fx != null && n.x === root.x && n.y === root.y) return;
            n.fx = null;
            n.fy = null;
            const a = (i / Math.max(family.length, 1)) * Math.PI * 2;
            n.x = root.x + Math.cos(a) * 70;
            n.y = root.y + Math.sin(a) * 70;
          });
        }
      });
    }
    node.vizVisible = true;
    applyVisibility();
    settleLocally();
  }

  function applyVisibility() {
    const vis = visibleNodeIds();
    nodeSel.attr("opacity", (d) => (d.vizVisible ? 1 : 0))
      .attr("pointer-events", (d) => (d.vizVisible ? "auto" : "none"));
    linkSel.attr("opacity", (d) => {
      const s = d.source.id || d.source;
      const t = d.target.id || d.target;
      return vis.has(s) && vis.has(t) ? 0.5 : 0;
    }).attr("pointer-events", (d) => {
      const s = d.source.id || d.source;
      const t = d.target.id || d.target;
      return vis.has(s) && vis.has(t) ? "auto" : "none";
    });
    syncSimulationScope(vis);
    refreshScale();
  }

  // 只把可见节点交给力导向。
  // 否则隐藏节点同样受碰撞力并被夹在画布内，会从背后把可见节点挤开
  // （实测 5500 词规模下，仅 16 个可见节点也能被挤出 37 对重叠），
  // 且白白模拟数千个节点。
  function syncSimulationScope(vis) {
    if (!simulation) return;
    const activeNodes = nodes.filter((n) => n.vizVisible);
    const activeLinks = links.filter((l) => {
      const s = l.source.id || l.source;
      const t = l.target.id || l.target;
      return vis.has(s) && vis.has(t);
    });
    simulation.nodes(activeNodes);
    const lf = simulation.force("link");
    if (lf) lf.links(activeLinks);
  }

  // 取消选中：清空详情栏
  function clearSelection() {
    nodeSel?.classed("selected", false);
    detailContent.classed("hidden", true).style("display", "none").html("");
    detailEmpty.classed("hidden", false).style("display", "block");
    closeDrawer();
  }

  // ---------- 搜索 ----------
  function onSearchInput() {
    const q = searchInput.node().value.trim().toLowerCase();
    if (!q) {
      searchResults.classed("hidden", true).html("");
      return;
    }
    const results = [];
    nodes.forEach((n) => {
      // 只搜三类内容：单词、词根、中文
      const haystacks = [n.label, n.type === "word" ? n.word : null, n.type === "word" ? (n.chinese || []).join(" ") : null, n.concept];
      const hay = haystacks.filter(Boolean).join(" ").toLowerCase();
      if (n.type === "word" && n.label.toLowerCase().startsWith(q)) {
        results.push({ node: n, score: 0 });
      } else if (n.label.toLowerCase().startsWith(q)) {
        results.push({ node: n, score: 1 });
      } else if (hay.includes(q)) {
        results.push({ node: n, score: 2 });
      }
    });
    results.sort((a, b) => a.score - b.score || a.node.label.localeCompare(b.node.label));

    if (!results.length) {
      searchResults.classed("hidden", false).html(`<div class="search-item search-empty">未收录「${escapeHtml(q)}」</div>`);
      return;
    }
    searchResults.classed("hidden", false).html(
      results.slice(0, 10).map((r) => {
        const n = r.node;
        const typeLabel = { domain: "语义域", root: "词根", concept: "概念", word: "单词" }[n.type];
        return `<div class="search-item" data-id="${escapeHtml(n.id)}">
          <span class="search-type ${n.type}">${typeLabel}</span>
          <b>${escapeHtml(n.label)}</b>
          ${n.type === "word" ? `<span class="search-meta">${escapeHtml((n.chinese || []).slice(0, 3).join(" / "))}</span>` : ""}
        </div>`;
      }).join("")
    );
  }

  function onSearchSelect(id) {
    const node = nodes.find((n) => n.id === id);
    if (!node) return;
    revealNode(node);
    focusNode(node);
    showDetail(node);
    searchResults.classed("hidden", true).html("");
    searchInput.node().value = "";
  }

  // 定位并高亮节点
  function focusNode(node) {
    highlightedId = node.id;
    node.fx = node.x;
    node.fy = node.y;

    // 高亮样式
    nodeSel.classed("highlighted", (d) => d.id === node.id);

    // 缩放平移到中心
    const container = svg.node().parentElement;
    const width = container.clientWidth;
    const height = container.clientHeight;
    const transform = d3.zoomTransform(svg.node());
    const k = Math.max(transform.k, 1.2);
    const tx = width / 2 - node.x * k;
    const ty = height / 2 - node.y * k;
    svg.transition().duration(500).call(
      d3.zoom().transform,
      d3.zoomIdentity.translate(tx, ty).scale(k)
    );

    // 3 秒后取消高亮
    setTimeout(() => {
      nodeSel.classed("highlighted", false);
      highlightedId = null;
    }, 3000);
  }

  // ---------- 渲染 ----------
  let nodeSel = null;
  let linkSel = null;
  // 画布尺寸与边距：拖拽和 resize 都要用，故提到模块级
  let viewW = 0;
  let viewH = 0;
  let viewMargin = 34;

  // ---------- 节点尺寸 ----------
  const BASE_R = { domain: 34, root: 27, concept: 20, cluster: 18, word: 13 };
  let viewScale = 1;

  // 缩放系数取"画布尺寸"与"可见节点密度"两者的较小值：
  // 前者管小屏，后者管词库长大后全部展开的情形。
  function computeScale(width, height) {
    const byCanvas = Math.min(1, Math.sqrt(width * height) / 900);
    const visible = nodes.filter((n) => n.vizVisible).length || 1;
    // 每个节点需要的画布面积按最大碰撞直径估：(34+14)*2 ≈ 96px 见方
    const need = visible * 96 * 96;
    const byDensity = Math.sqrt((width * height) / need);
    // 下限 0.28：节点数很大时必须让它继续缩小，否则几何上放不下
    // （541 节点时按密度需 0.478，若卡在 0.5 就会出现重叠）。
    // 缩到这么小时标签已不易读，但图谱支持最多 5 倍缩放，
    // 此时它的作用是"全局俯视图"，看细节靠放大。
    return Math.min(1, Math.max(0.28, Math.min(byCanvas, byDensity)));
  }

  function radiusOf(d) {
    const base = d.type === "domain" ? BASE_R.domain
      : d.type === "root" ? BASE_R.root
      : d.type === "concept" ? (d.isCluster ? BASE_R.cluster : BASE_R.concept)
      : BASE_R.word;
    return Math.max(4, Math.round(base * viewScale));
  }

  // 碰撞半径 = 节点半径 + 标签留白
  function collideR(d) {
    return radiusOf(d) + 14 * viewScale;
  }

  // 可见节点数变化后重算尺寸：半径、碰撞、边界留白、连线距离都要跟着变
  function refreshScale() {
    if (!nodeSel || !simulation) return;
    const prev = viewScale;
    viewScale = computeScale(viewW, viewH);
    if (Math.abs(viewScale - prev) < 0.02) return;

    nodeSel.select("circle").attr("r", radiusOf);
    nodeSel.each(function (d) {
      const t = d3.select(this).select("text");
      let halfW = 0;
      try { halfW = t.node().getComputedTextLength() / 2; } catch (e) { halfW = 0; }
      const r = radiusOf(d);
      const dy = d.type === "word" ? (viewW < 520 ? 24 : 32) : 0;
      d.padX = Math.max(halfW, r) + 4;
      d.padTop = r + 4;
      d.padBottom = Math.max(dy + 8, r) + 4;
    });
    const cf = simulation.force("collide");
    if (cf) cf.radius(collideR);
    const lf = simulation.force("link");
    if (lf) {
      lf.distance((l) => {
        const want = (l.type === "root" ? 70 : 110) * viewScale;
        return Math.max(want, collideR(l.source) + collideR(l.target) + 6);
      });
    }
  }

  // 把节点夹在画布内（按标签实测尺寸，中文长标签也不会探出去）
  // 只处理可见节点：隐藏节点的位置无意义，大规模下夹紧它们纯属浪费
  function clampNodes(width, height, margin) {
    nodes.forEach((n) => {
      if (!n.vizVisible) return;
      const px = Math.min(n.padX || margin, width / 2 - 2);
      const top = Math.min(n.padTop || margin, height / 2 - 2);
      const bottom = Math.min(n.padBottom || margin, height / 2 - 2);
      n.x = Math.max(px, Math.min(width - px, n.x));
      n.y = Math.max(top, Math.min(height - bottom, n.y));
    });
  }

  // 重绘：从 tick 里抽出来，拖拽时直接调用，无需重启力导向
  function redraw() {
    if (!linkSel || !nodeSel) return;
    linkSel
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);
    nodeSel.attr("transform", (d) => `translate(${d.x},${d.y})`);
  }

  // 钉住 / 释放：钉住后图谱静止，是"拖一个不动其它"的关键
  function pinAll() {
    nodes.forEach((n) => { n.fx = n.x; n.fy = n.y; });
  }

  function unpinAll() {
    nodes.forEach((n) => { n.fx = null; n.fy = null; });
  }

  function render() {
    const width = svg.node().parentElement.clientWidth;
    const height = svg.node().parentElement.clientHeight;
    svg.attr("viewBox", [0, 0, width, height]);

    // 节点尺寸随画布缩放：手机画布只有桌面的 1/9 面积，
    // 沿用桌面半径会导致节点挤在一起（实测重叠十几对）。
    // 尺寸缩放同时看画布大小和当前可见节点数。
    // 只按画布缩放不够：词库长大后"全部展开"的节点数会翻几倍，
    // 面积没变而占位需求变了（实测 335 节点时出现重叠）。
    viewScale = computeScale(width, height);

    // 缩放
    const g = svg.append("g");
    svg.call(
      d3.zoom()
        .touchable(2) // 触屏：双指捏合缩放
        .scaleExtent([0.2, 5])
        .on("zoom", (event) => g.attr("transform", event.transform))
    );

    // 双击空白处重新布局 + 重置视图
    svg.on("dblclick.zoom", null);
    svg.on("dblclick", (event) => {
      if (event.target === svg.node()) {
        restartSimulation();
      }
    });

    // 单击空白处取消选中，收起关系名
    svg.on("click", (event) => {
      if (event.target === svg.node()) clearSelection();
    });

    // 连线
    linkSel = g
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", (d) => "link" + (d.type === "antonym" ? " antonym" : "") + (d.type === "semantic_extension" ? " semantic_extension" : "") + (d.type === "context" ? " context" : ""));

    // 节点
    nodeSel = g
      .append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", (d) => "node " + d.type)
      .call(drag());

    nodeSel
      .append("circle")
      .attr("r", radiusOf)
      .attr("class", (d) => d.type);

    // 单词标签挂在圆下方，偏移量随屏幕收敛，避免小屏触底越界
    const wordLabelDy = width < 520 ? 24 : 32;
    const labelSel = nodeSel
      .append("text")
      .text((d) => d.label)
      .attr("dy", (d) => (d.type === "word" ? wordLabelDy : 0));

    // 量出每个标签的实际半宽/垂直范围，供 tick 里的边界约束使用。
    // 概念节点是中文长标签（如"一个可被辨认的形态"），只约束圆心会让标签探出画布。
    labelSel.each(function (d) {
      let halfW = 0;
      try { halfW = this.getComputedTextLength() / 2; } catch (e) { halfW = 0; }
      const r = radiusOf(d);
      d.padX = Math.max(halfW, r) + 4;
      const dy = d.type === "word" ? wordLabelDy : 0;
      d.padTop = r + 4;
      d.padBottom = Math.max(dy + 8, r) + 4;
    });

    nodeSel.on("click", (event, d) => {
      if (d.type === "domain") {
        toggleDomain(d);
      } else if (d.type === "root") {
        toggleRoot(d);
      }
      showDetail(d);
    });

    // 力导向
    // 10 个词根簇互不相连，仅靠 charge + center 会互相排斥飘出画布，
    // 因此加 forceX/forceY 向心约束，并在 tick 中把节点夹在画布内。
    const margin = Math.min(34, Math.max(20, Math.min(width, height) * 0.08));
    viewW = width;
    viewH = height;
    viewMargin = margin;
    simulation = d3
      .forceSimulation(nodes)
      // 连线距离必须 >= 两端碰撞半径之和，否则连线会把节点拽进碰撞禁区，
      // 两个力互相矛盾且连线通常获胜（实测表现为「语义域+词根」贴在一起）。
      .force("link", d3.forceLink(links).id((d) => d.id)
        .distance((l) => {
          const want = (l.type === "root" ? 70 : 110) * viewScale;
          const need = collideR(l.source) + collideR(l.target) + 6;
          return Math.max(want, need);
        }))
      .force("charge", d3.forceManyBody().strength(-300 * viewScale * viewScale).distanceMax(320 * viewScale))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(width / 2).strength(0.06))
      .force("y", d3.forceY(height / 2).strength(0.09))
      .force("collide", d3.forceCollide().radius(collideR))
      .on("tick", () => {
        clampNodes(width, height, margin);
        redraw();
      })
      // 布局稳定后把所有节点钉住，图谱从此静止：
      // 之后拖动单个节点不会再牵动其它节点。
      .on("end", pinAll);

    applyVisibility();
  }

  // 全量重排：唯一会让所有节点重新排布的入口（双击空白处触发）
  function restartSimulation() {
    if (!simulation) return;
    unpinAll();
    simulation.alpha(0.9).alphaTarget(0).restart();
  }

  function drag() {
    // 关键：拖拽不再 restart 力导向。旧实现用 alphaTarget(0.3).restart()
    // 重新激活整个模拟，导致"拖一个球，其它全在动"。
    // 现在只移动被拖的节点并重绘，其余节点保持钉住不动。
    function dragstarted(event, d) {
      pinAll();          // 确保其它节点都被钉死
      d.fx = d.x;
      d.fy = d.y;
    }
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
      d.x = event.x;
      d.y = event.y;
      clampNodes(viewW, viewH, viewMargin);
      redraw();
    }
    function dragended(event, d) {
      // 停在松手的位置（不再回弹）
      d.fx = d.x;
      d.fy = d.y;
    }
    return d3
      .drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }

  // ---------- 详情面板 ----------
  function showDetail(d) {
    nodeSel?.classed("selected", (n) => n.id === d.id);
    openDrawer(); // 手机端打开底部抽屉
    detailEmpty.classed("hidden", true).style("display", "none");
    detailContent.classed("hidden", false).style("display", "block");

    const typeLabel = {
      domain: "语义域", root: "词根", word: "单词",
      concept: "核心概念" + (d.isCluster ? "（聚合）" : ""),
    }[d.type];

    let html = `
      <div class="detail-title">${escapeHtml(d.label)}
        <span class="detail-type ${d.type}">${typeLabel}</span>
        ${d.phonetic ? `<span class="detail-phonetic">${escapeHtml(d.phonetic)}</span>` : ""}
        ${d.type === "word" ? `<button class="speak-btn" data-word="${escapeHtml(d.label)}" title="点击发音">◍ 发音</button>` : ""}
      </div>`;

    if (d.pos) {
      html += `<div class="detail-block origin-src">词性 · ${escapeHtml(d.pos)}</div>`;
    }

    if (d.definition) {
      html += `<div class="detail-block detail-definition"><h3>英文释义 Definition</h3><p>${escapeHtml(d.definition)}</p></div>`;
    }

    if (d.concept) {
      html += `<div class="detail-block feature"><h3>核心概念 Concept</h3><p>${escapeHtml(d.concept)}</p></div>`;
    }

    if (d.image) {
      html += `<div class="detail-block feature concept-tone"><h3>核心画面 Core Image</h3><p>${escapeHtml(d.image)}</p></div>`;
    }

    if (d.rootLogic) {
      html += `<div class="detail-block"><h3>词根推导 Root Logic</h3><p>${escapeHtml(d.rootLogic)}</p></div>`;
    }

    // 不可拆的词如实说明，而不是留一片空白让人以为漏了内容
    const DECOMP_LABEL = {
      root_pending: "可由词根拆解，但该词根尚未收入本图谱",
      germanic: "日耳曼核心词 —— 它本身就是词根，无法再拆",
      loanword: "借词 —— 拆解没有认知价值，靠画面记",
      phrasal: "短语动词 —— 意义在介词的空间隐喻里",
      opaque: "词源不明，无法有效拆解",
    };
    if (d.type === "word" && DECOMP_LABEL[d.decomposable]) {
      html += `<div class="detail-block"><h3>为什么没有词根推导</h3>`
        + `<p class="origin-src">${escapeHtml(DECOMP_LABEL[d.decomposable])}`
        + `${d.decomposableNote ? "——" + escapeHtml(d.decomposableNote) : ""}</p></div>`;
    }

    if (d.origin) {
      html += `<div class="detail-block"><h3>词源 Origin</h3><p class="origin-src">${escapeHtml(d.origin)}</p></div>`;
    }

    // 单词的 chinese 是数组，语义域/概念的是字符串——统一成数组再渲染，
    // 否则点概念或语义域节点会抛 "d.chinese.map is not a function"
    const zh = Array.isArray(d.chinese) ? d.chinese
      : (typeof d.chinese === "string" && d.chinese ? [d.chinese] : []);
    if (zh.length && d.type === "word") {
      html += `<div class="detail-block"><h3>中文表达（输出层）</h3><p>${zh.map((c) => `<span class="chip zh">${escapeHtml(c)}</span>`).join("")}</p></div>`;
    }

    if (d.type === "word") {
      const expansions = d.expansions && d.expansions.length
        ? d.expansions.map((e) => `<li>${escapeHtml(e)}</li>`).join("")
        : "";
      if (expansions) {
        html += `<div class="detail-block"><h3>语义扩展</h3><ul>${expansions}</ul></div>`;
      }

      // 近义词组（概念层中转）
      if (d.synonymGroup) {
        const cluster = nodes.find((n) => n.id === d.synonymGroup);
        if (cluster) {
          const groupWords = (cluster.words || [])
            .filter((wid) => wid !== d.id)
            .map((wid) => {
              const wn = nodes.find((n) => n.id === wid);
              return wn ? `<span class="chip related">${escapeHtml(wn.label)}</span>` : "";
            })
            .join("");
          html += `<div class="detail-block feature concept-tone"><h3>近义词组 · 共享概念</h3>
            <p><b>${escapeHtml(cluster.concept)}</b></p>
            <p>${groupWords}</p>
            ${d.synonymNote ? `<p class="origin-src">${escapeHtml(d.synonymNote)}</p>` : ""}
          </div>`;
        }
      }

      if (d.synonyms && d.synonyms.length) {
        html += `<div class="detail-block"><h3>近义词</h3><p>${d.synonyms.map((s) => `<span class="chip related">${escapeHtml(s)}</span>`).join("")}</p></div>`;
      }
      if (d.antonyms && d.antonyms.length) {
        html += `<div class="detail-block"><h3>反义词</h3><p>${d.antonyms.map((a) => `<span class="chip antonym">${escapeHtml(a)}</span>`).join("")}</p></div>`;
      }
      if (d.related && d.related.length) {
        html += `<div class="detail-block"><h3>关联词</h3><p>${d.related.map((r) => `<span class="chip related">${escapeHtml(r)}</span>`).join("")}</p></div>`;
      }
      if (d.examples && d.examples.length) {
        html += `<div class="detail-block detail-examples"><h3>例句 Context</h3><ul>${d.examples.map((e) => `<li>${escapeHtml(e)}</li>`).join("")}</ul></div>`;
      }
    }

    // 语义域：列出其下词根，以及各自的词族规模
    if (d.type === "domain") {
      if (d.description) {
        html += `<div class="detail-block"><h3>说明</h3><p>${escapeHtml(d.description)}</p></div>`;
      }
      const rootNodes = (d.roots || [])
        .map((rid) => nodes.find((n) => n.id === rid))
        .filter(Boolean);
      if (rootNodes.length) {
        const items = rootNodes.map((r) => {
          const n = nodes.filter(
            (w) => w.type === "word" && w.roots && w.roots.includes(r.id)
          ).length;
          return `<li><b>${escapeHtml(r.label)}</b> — ${escapeHtml(r.concept)}`
            + `<span class="origin-src"> · ${n} 词</span></li>`;
        }).join("");
        html += `<div class="detail-block"><h3>词根（${rootNodes.length}）`
          + `${d.expanded ? " · 已展开" : " · 点击节点展开"}</h3><ul>${items}</ul></div>`;
      }
    }

    // 词根查看词族
    if (d.type === "root") {
      const family = nodes.filter((n) => n.type === "word" && n.roots && n.roots.includes(d.id));
      if (family.length) {
        html += `<div class="detail-block"><h3>词族（${family.length}）${d.expanded ? " · 已展开" : " · 点击节点展开"}</h3><ul>${family.map((w) => `<li><b>${escapeHtml(w.label)}</b> — ${escapeHtml(w.concept)}</li>`).join("")}</ul></div>`;
      }
    }

    // cluster 概念显示组内词
    if (d.type === "concept" && d.isCluster) {
      const members = (d.words || []).map((wid) => {
        const wn = nodes.find((n) => n.id === wid);
        return wn ? `<li><b>${escapeHtml(wn.label)}</b> — ${escapeHtml(wn.concept)}</li>` : "";
      }).join("");
      html += `<div class="detail-block"><h3>近义词组成员（${(d.words || []).length}）</h3><ul>${members}</ul></div>`;
    }

    detailContent.html(html);
  }

  // 点击详情面板中的近义词 chip → 定位到该词
  detailContent.on("click", (event) => {
    const chip = event.target.closest(".chip");
    if (!chip) return;
    const id = chip.textContent.trim();
    const node = nodes.find((n) => n.label === id && n.type === "word");
    if (node) {
      revealNode(node);
      focusNode(node);
      showDetail(node);
    }
  });

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str == null ? "" : String(str);
    return div.innerHTML;
  }

  // ---------- 昼夜主题 ----------
  // 白天：纸张地图 / 夜间：夜读档案。首屏主题已在 index.html 内联脚本中应用。
  function isNight() {
    return document.documentElement.getAttribute("data-theme") === "night";
  }

  function syncThemeButton() {
    const btn = document.getElementById("theme-toggle");
    if (!btn) return;
    const night = isNight();
    // 图标表示"点击后切换到的模式"
    btn.textContent = night ? "☀" : "☾";
    btn.title = night ? "切换到白天模式" : "切换到夜间模式";
  }

  function toggleTheme() {
    const night = !isNight();
    if (night) {
      document.documentElement.setAttribute("data-theme", "night");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    try {
      localStorage.setItem("esg-theme", night ? "night" : "day");
    } catch (e) { /* 隐私模式下 localStorage 不可写，主题仅在本次会话生效 */ }
    syncThemeButton();
  }

  // ---------- 发音（Web Speech API） ----------
  function speakWord(word) {
    if (!("speechSynthesis" in window)) {
      alert("当前浏览器不支持语音合成");
      return;
    }
    // 取消正在播报的（防止连续点击堆积）
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(word);
    utter.lang = "en-US";
    utter.rate = 0.85; // 稍慢，便于学习
    // 优先选英语语音
    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find((v) => v.lang.startsWith("en-US")) || voices.find((v) => v.lang.startsWith("en"));
    if (enVoice) utter.voice = enVoice;
    window.speechSynthesis.speak(utter);
  }

  // 详情面板：点击 🔊 发音
  detailContent.on("click", (event) => {
    const btn = event.target.closest(".speak-btn");
    if (btn && btn.dataset.word) {
      speakWord(btn.dataset.word);
      return;
    }
    const chip = event.target.closest(".chip");
    if (!chip) return;
    const id = chip.textContent.trim();
    const node = nodes.find((n) => n.label === id && n.type === "word");
    if (node) {
      revealNode(node);
      focusNode(node);
      showDetail(node);
    }
  });

  // ---------- 启动 ----------
  async function init() {
    try {
      const data = await loadData();
      buildGraph(data);

      // 学习模式复用同一份已加载数据，不重复请求
      window.ESG = window.ESG || {};
      window.ESG.speak = speakWord;
      if (typeof window.ESG.initStudy === "function") {
        window.ESG.initStudy(data);
      }
      render();

      // 主题切换
      document.getElementById("theme-toggle")?.addEventListener("click", toggleTheme);
      syncThemeButton();

      // 搜索事件
      searchInput.on("input", onSearchInput);
      searchInput.on("keydown", (event) => {
        if (event.key === "Enter") {
          const first = searchResults.select(".search-item:not(.search-empty)").node();
          if (first) onSearchSelect(first.dataset.id);
        }
        if (event.key === "Escape") {
          searchResults.classed("hidden", true).html("");
          searchInput.node().value = "";
        }
      });
      searchResults.on("click", (event) => {
        const item = event.target.closest(".search-item");
        if (item && item.dataset.id) onSearchSelect(item.dataset.id);
      });

      // 抽屉关闭按钮（手机端）
      d3.select("#drawer-close").on("click", clearSelection);
    } catch (e) {
      detailContent.classed("hidden", false).style("display", "block");
      detailEmpty.style("display", "none");
      detailContent.html(`
        <div class="detail-block" style="border-left-color:#ef476f">
          <h3>⚠️ 数据加载失败</h3>
          <p><pre style="white-space:pre-wrap;font-size:12px">${escapeHtml(e.message)}</pre></p>
        </div>`);
      console.error(e);
    }
  }

  window.addEventListener("resize", () => {
    if (simulation) {
      const container = svg.node().parentElement;
      const width = container.clientWidth;
      const height = container.clientHeight;
      svg.attr("viewBox", [0, 0, width, height]);
      viewW = width;
      viewH = height;
      viewMargin = Math.min(34, Math.max(20, Math.min(width, height) * 0.08));
      simulation.force("center", d3.forceCenter(width / 2, height / 2));
      simulation.force("x", d3.forceX(width / 2).strength(0.06));
      simulation.force("y", d3.forceY(height / 2).strength(0.09));
      // 视口变了：把节点夹回新边界并重绘，但不重排布局
      nodes.forEach((n) => { n.fx = null; n.fy = null; });
      clampNodes(viewW, viewH, viewMargin);
      pinAll();
      redraw();
    }
  });

  init();
})();