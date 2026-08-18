/* English Semantic Graph v0.1 — D3 force-directed graph */
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

  const svg = d3.select("#graph");
  const detailEmpty = d3.select("#detail-empty");
  const detailContent = d3.select("#detail-content");

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

    // 词根节点
    data.roots.roots.forEach((r) => {
      const node = {
        id: r.id,
        label: r.root,
        type: "root",
        origin: r.origin,
        concept: r.core_concept,
        image: r.core_image,
        definition: r.english_definition,
      };
      idMap.set(node.id, node);
    });

    // 概念节点
    data.concepts.concepts.forEach((c) => {
      const node = {
        id: c.id,
        label: c.chinese,
        type: "concept",
        concept: c.concept,
        chinese: c.chinese,
        image: c.core_image,
        roots: c.root_ids,
      };
      idMap.set(node.id, node);
    });

    // 单词节点
    data.words.words.forEach((w) => {
      const node = {
        id: w.id,
        label: w.word,
        type: "word",
        pos: w.pos,
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
      };
      idMap.set(node.id, node);
    });

    nodes = Array.from(idMap.values());

    // 边：关系数据
    links = data.relations.relations
      .filter((r) => idMap.has(r.from) && idMap.has(r.to))
      .map((r) => ({ source: r.from, target: r.to, type: r.type, note: r.note }));

    // 边：词根 → 概念 / 概念 → 单词 的桥接关系
    // 概念节点与其词根相连
    nodes.filter((n) => n.type === "concept" && n.roots).forEach((c) => {
      c.roots.forEach((rid) => {
        links.push({ source: rid, target: c.id, type: "root", note: "词根→概念" });
      });
    });

    // 单词与其所属词根相连（如果关系数据里没有，则补上）
    nodes.filter((n) => n.type === "word" && n.roots).forEach((w) => {
      w.roots.forEach((rid) => {
        const exists = links.some(
          (l) => l.source === rid && l.target === w.id
        );
        if (!exists) {
          links.push({ source: rid, target: w.id, type: "root", note: "词根→单词" });
        }
      });
    });
  }

  // ---------- 渲染 ----------
  function render() {
    const width = svg.node().parentElement.clientWidth;
    const height = svg.node().parentElement.clientHeight;
    svg.attr("viewBox", [0, 0, width, height]);

    // 缩放
    const g = svg.append("g");
    svg.call(
      d3.zoom()
        .scaleExtent([0.2, 5])
        .on("zoom", (event) => g.attr("transform", event.transform))
    );

    // 双击空白处重新布局
    svg.on("dblclick.zoom", null); // 禁用缩放的双击放大
    svg.on("dblclick", (event) => {
      if (event.target === svg.node()) {
        restartSimulation();
      }
    });

    // 连线
    const link = g
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", (d) => "link" + (d.type === "antonym" ? " antonym" : "") + (d.type === "semantic_extension" ? " semantic_extension" : ""));

    // 连线标签（关系类型）
    const linkLabel = g
      .append("g")
      .attr("class", "link-labels")
      .selectAll("text")
      .data(links.filter((d) => d.type !== "root"))
      .join("text")
      .attr("class", "link-label")
      .text((d) => EDGE_TYPE_LABEL[d.type] || d.type)
      .attr("font-size", 9)
      .attr("fill", "#5a6275")
      .attr("text-anchor", "middle");

    // 节点
    const node = g
      .append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", (d) => "node " + d.type)
      .call(drag());

    node
      .append("circle")
      .attr("r", (d) => (d.type === "root" ? 26 : d.type === "concept" ? 18 : 14))
      .attr("class", (d) => d.type);

    node
      .append("text")
      .text((d) => d.label)
      .attr("dy", (d) => (d.type === "word" ? 32 : 0));

    node.on("click", (event, d) => showDetail(d));

    // 力导向
    simulation = d3
      .forceSimulation(nodes)
      .force("link", d3.forceLink(links).id((d) => d.id).distance((d) => (d.type === "root" ? 70 : 110)))
      .force("charge", d3.forceManyBody().strength(-420))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(40))
      .on("tick", () => {
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);
        linkLabel
          .attr("x", (d) => (d.source.x + d.target.x) / 2)
          .attr("y", (d) => (d.source.y + d.target.y) / 2 - 4);
        node.attr("transform", (d) => `translate(${d.x},${d.y})`);
      });
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
    detailEmpty.classed("hidden", true).style("display", "none");
    detailContent.classed("hidden", false).style("display", "block");

    const typeLabel = { root: "词根", concept: "核心概念", word: "单词" }[d.type];

    let html = `
      <div class="detail-title">${escapeHtml(d.label)}
        <span class="detail-type ${d.type}">${typeLabel}</span>
      </div>`;

    if (d.pos) {
      html += `<div class="detail-block origin-src">词性 POS：${escapeHtml(d.pos)}</div>`;
    }

    if (d.origin) {
      html += `<div class="detail-block origin-src">📜 词源：${escapeHtml(d.origin)}</div>`;
    }

    if (d.rootLogic) {
      html += `<div class="detail-block" style="border-left-color:#ffd166"><h3>🧩 词根推导</h3><p>${escapeHtml(d.rootLogic)}</p></div>`;
    }

    if (d.concept) {
      html += `<div class="detail-block"><h3>核心概念 Concept</h3><p>${escapeHtml(d.concept)}</p></div>`;
    }

    if (d.definition) {
      html += `<div class="detail-block"><h3>英文释义 Definition</h3><p>${escapeHtml(d.definition)}</p></div>`;
    }

    if (d.image) {
      html += `<div class="detail-block"><h3>🧠 核心画面 Core Image</h3><p>${escapeHtml(d.image)}</p></div>`;
    }

    if (d.chinese && d.chinese.length) {
      html += `<div class="detail-block"><h3>中文表达</h3><p>${d.chinese.map((c) => `<span class="chip">${escapeHtml(c)}</span>`).join("")}</p></div>`;
    }

    if (d.type === "word") {
      const expansions = d.expansions && d.expansions.length
        ? d.expansions.map((e) => `<li>${escapeHtml(e)}</li>`).join("")
        : "";
      if (expansions) {
        html += `<div class="detail-block"><h3>语义扩展</h3><ul>${expansions}</ul></div>`;
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
        html += `<div class="detail-block"><h3>例句</h3><ul>${d.examples.map((e) => `<li>${escapeHtml(e)}</li>`).join("")}</ul></div>`;
      }
    }

    // 词根查看词族
    if (d.type === "root") {
      const family = nodes.filter((n) => n.type === "word" && n.roots && n.roots.includes(d.id));
      if (family.length) {
        html += `<div class="detail-block"><h3>词族（${family.length}）</h3><ul>${family.map((w) => `<li><b>${escapeHtml(w.label)}</b> — ${escapeHtml(w.concept)}</li>`).join("")}</ul></div>`;
      }
    }

    detailContent.html(html);
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str == null ? "" : String(str);
    return div.innerHTML;
  }

  // ---------- 启动 ----------
  async function init() {
    try {
      const data = await loadData();
      buildGraph(data);
      render();
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
      const width = svg.node().parentElement.clientWidth;
      const height = svg.node().parentElement.clientHeight;
      simulation.force("center", d3.forceCenter(width / 2, height / 2));
    }
  });

  init();
})();