/* English Semantic Graph v0.1.1 — D3 force-directed graph
 * 功能：分层钻取（默认词根+概念，点击展开词族）+ 搜索直达 + 详情面板
 */
(function () {
  "use strict";

  const DATA_FILES = [
    { key: "roots", path: "../data/roots.json" },
    { key: "concepts", path: "../data/concepts.json" },
    { key: "words", path: "../data/words.json" },
    { key: "relations", path: "../data/relations.json" },
  ];

  const EDGE_TYPE_LABEL = {
    root: "词根关系",
    derived: "派生关系",
    semantic_extension: "语义扩展",
    synonym: "近义关系",
    antonym: "反义关系",
    context: "场景关系",
  };

  let nodes = [];
  let links = [];
  let simulation = null;
  let highlightedId = null; // 当前高亮节点 id

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
  async function loadData() {
    const results = {};
    for (const f of DATA_FILES) {
      try {
        const res = await fetch(f.path);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        results[f.key] = await res.json();
      } catch (e) {
        throw new Error(
          `无法加载 ${f.path}（${e.message}）。\n\n` +
          `本地直接双击打开会有浏览器安全限制。请用本地服务器：\n` +
          `在仓库根目录运行：python3 -m http.server 8000\n` +
          `然后访问 http://localhost:8000/frontend/`
        );
      }
    }
    return results;
  }

  // ---------- 构建图数据 ----------
  function buildGraph(data) {
    const idMap = new Map();

    // 词根节点（默认可见）
    data.roots.roots.forEach((r) => {
      const node = {
        id: r.id,
        label: r.root,
        type: "root",
        origin: r.origin,
        concept: r.core_concept,
        image: r.core_image,
        definition: r.english_definition,
        vizVisible: true,
        expanded: false,
      };
      idMap.set(node.id, node);
    });

    // 概念节点（默认可见，含 cluster 聚合概念）
    data.concepts.concepts.forEach((c) => {
      const node = {
        id: c.id,
        label: c.chinese,
        type: "concept",
        concept: c.concept,
        chinese: c.chinese,
        image: c.core_image,
        roots: c.root_ids,
        words: c.word_ids,
        isCluster: c.type === "cluster",
        vizVisible: true,
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

  function toggleRoot(d) {
    d.expanded = !d.expanded;
    // 展开/收起该词根的词族
    nodes.forEach((n) => {
      if (n.type === "word" && n.roots && n.roots.includes(d.id)) {
        n.vizVisible = d.expanded;
      }
    });
    applyVisibility();
    restartSimulation();
  }

  // 强制显示某节点（用于搜索直达）
  function revealNode(node) {
    if (node.vizVisible) return;
    // 单词：展开其所属词根
    if (node.type === "word" && node.roots) {
      node.roots.forEach((rid) => {
        const root = nodes.find((n) => n.id === rid);
        if (root) {
          root.expanded = true;
          nodes.forEach((n) => {
            if (n.type === "word" && n.roots && n.roots.includes(rid)) n.vizVisible = true;
          });
        }
      });
    }
    node.vizVisible = true;
    applyVisibility();
    restartSimulation();
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
        const typeLabel = { root: "词根", concept: "概念", word: "单词" }[n.type];
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

  function render() {
    const width = svg.node().parentElement.clientWidth;
    const height = svg.node().parentElement.clientHeight;
    svg.attr("viewBox", [0, 0, width, height]);

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

    // 连线
    linkSel = g
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", (d) => "link" + (d.type === "antonym" ? " antonym" : "") + (d.type === "semantic_extension" ? " semantic_extension" : "") + (d.type === "context" ? " context" : ""));

    // 连线标签（关系类型）
    const linkLabel = g
      .append("g")
      .attr("class", "link-labels")
      .selectAll("text")
      .data(links.filter((d) => d.type !== "root" && d.type !== "context"))
      .join("text")
      .attr("class", "link-label")
      .text((d) => EDGE_TYPE_LABEL[d.type] || d.type);

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
      .attr("r", (d) => (d.type === "root" ? 27 : d.type === "concept" ? (d.isCluster ? 18 : 20) : 13))
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
      d.padX = Math.max(halfW, d.type === "root" ? 27 : d.type === "concept" ? 20 : 13) + 4;
      const dy = d.type === "word" ? wordLabelDy : 0;
      d.padTop = (d.type === "root" ? 27 : d.type === "concept" ? 20 : 13) + 4;
      d.padBottom = Math.max(dy + 8, d.type === "root" ? 27 : 13) + 4;
    });

    nodeSel.on("click", (event, d) => {
      if (d.type === "root") {
        toggleRoot(d);
      }
      showDetail(d);
    });

    // 力导向
    // 10 个词根簇互不相连，仅靠 charge + center 会互相排斥飘出画布，
    // 因此加 forceX/forceY 向心约束，并在 tick 中把节点夹在画布内。
    const margin = Math.min(34, Math.max(20, Math.min(width, height) * 0.08));
    simulation = d3
      .forceSimulation(nodes)
      .force("link", d3.forceLink(links).id((d) => d.id).distance((d) => (d.type === "root" ? 70 : 110)))
      .force("charge", d3.forceManyBody().strength(-300).distanceMax(320))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(width / 2).strength(0.06))
      .force("y", d3.forceY(height / 2).strength(0.09))
      .force("collide", d3.forceCollide().radius(38))
      .on("tick", () => {
        // 硬边界：按标签实际尺寸夹住，保证圆和文字都留在画布内
        nodes.forEach((n) => {
          const px = Math.min(n.padX || margin, width / 2 - 2);
          const top = Math.min(n.padTop || margin, height / 2 - 2);
          const bottom = Math.min(n.padBottom || margin, height / 2 - 2);
          n.x = Math.max(px, Math.min(width - px, n.x));
          n.y = Math.max(top, Math.min(height - bottom, n.y));
        });
        linkSel
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);
        linkLabel
          .attr("x", (d) => (d.source.x + d.target.x) / 2)
          .attr("y", (d) => (d.source.y + d.target.y) / 2 - 4);
        nodeSel.attr("transform", (d) => `translate(${d.x},${d.y})`);
      });

    applyVisibility();
  }

  function restartSimulation() {
    if (!simulation) return;
    simulation.alpha(0.6).alphaTarget(0).restart();
  }

  function drag() {
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    return d3
      .drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }

  // ---------- 详情面板 ----------
  function showDetail(d) {
    openDrawer(); // 手机端打开底部抽屉
    detailEmpty.classed("hidden", true).style("display", "none");
    detailContent.classed("hidden", false).style("display", "block");

    const typeLabel = { root: "词根", concept: "核心概念" + (d.isCluster ? "（聚合）" : ""), word: "单词" }[d.type];

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

    if (d.origin) {
      html += `<div class="detail-block"><h3>词源 Origin</h3><p class="origin-src">${escapeHtml(d.origin)}</p></div>`;
    }

    if (d.chinese && d.chinese.length) {
      html += `<div class="detail-block"><h3>中文表达（输出层）</h3><p>${d.chinese.map((c) => `<span class="chip zh">${escapeHtml(c)}</span>`).join("")}</p></div>`;
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
      d3.select("#drawer-close").on("click", closeDrawer);
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
      simulation.force("center", d3.forceCenter(width / 2, height / 2));
      simulation.force("x", d3.forceX(width / 2).strength(0.06));
      simulation.force("y", d3.forceY(height / 2).strength(0.09));
      simulation.alpha(.25).restart();
    }
  });

  init();
})();