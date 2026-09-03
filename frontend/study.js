/* 学习模式 —— 回想 / 词族
 *
 * 目的不是做一个背单词软件，而是检验本项目的核心主张：
 *   1) 回想：只给核心画面 + 词根推导，能否想起这个词（检验画面记忆是否成立）
 *   2) 词族：给一个词根和它的核心概念，能否把前缀与词义对上
 *      （检验"一个核心概念解释一整族"是否为真）
 *
 * 与 graph.js 解耦：只依赖 data/*.json 与几个容器元素。
 */
(function () {
  "use strict";

  const MASK = "▢▢▢";

  /* ---------- 记忆进度 ----------
   * 存的是"连续想起次数"而不是布尔值。布尔标记有个必然会碰到的失效：
   * 今天标了已背，三周后真忘了，它还是绿的。次数本来就在数（原来算完就丢），
   * 做成分层几乎不额外花钱，而且「没想起来」归零后颜色会自己退回去，
   * 反映的是当前状态而不是历史上某一刻的声明。
   *
   * 必须走 localStorage，不能进 IndexedDB —— 那边是数据缓存，idbPut 里有
   * clear()，每次词库更新都会整个清掉，进度会跟着蒸发。
   *
   * 词条 id 就是单词本身且全库唯一，所以词库重新生成后进度仍然对得上。
   * 只存 streak > 0 的词：标了 500 词也就 7KB。
   */
  const PROGRESS_KEY = "esg-progress";
  const FILTER_KEY = "esg-skip-mastered";
  const SCOPE_KEY = "esg-recall-scope";
  const TIER_MAX = 3;
  const TIER_LABEL = ["生词", "眼熟", "已背", "牢固"];

  let streaks = Object.create(null);
  const changeHooks = [];

  function loadProgress() {
    try {
      const raw = localStorage.getItem(PROGRESS_KEY);
      if (!raw) return;
      const j = JSON.parse(raw);
      if (j && j.s && typeof j.s === "object") streaks = Object.assign(Object.create(null), j.s);
    } catch (e) { /* 存档损坏或 localStorage 不可用：当作没有进度，不要让整页挂掉 */ }
  }

  /* 申请持久化存储。默认的存储是"best-effort"，磁盘紧张时浏览器可以直接
   * 回收掉；拿到 persistent 之后只有用户手动清除才会消失。
   * 已安装的 PWA（加到主屏幕）在 Chrome 里几乎总能拿到，这是加 manifest 的
   * 实际理由之一。
   *
   * 故意等到第一次真的要存东西时才申请，而不是一进页面就问：
   * Chrome 不弹窗（按站点参与度静默判定），但 Firefox 会弹权限框 ——
   * 让一个还没记录任何进度的新访客先看到弹窗是没道理的。
   */
  let persistState = null;   // null=还不知道 true=已持久化 false=没拿到或不支持
  let persistAsked = false;

  // 只读地问一次当前状态，不触发申请（persisted() 不会弹权限框，persist() 才会）。
  // 页面一打开就要知道真实状态 —— 否则已有进度的老用户在第一次答题前
  // 界面只能显示"不知道"。
  function probePersisted() {
    try {
      const s = navigator.storage;
      if (!s || !s.persisted) { persistState = false; return; }
      s.persisted().then((ok) => {
        persistState = !!ok;
        if (ok) persistAsked = true;   // 已经是持久化的，不必再申请
        refreshProgressBar();
      }).catch(() => { persistState = false; });
    } catch (e) { persistState = false; }
  }

  // 装成 app 打开时 display-mode 是 standalone。用来区分
  // "还在浏览器里，建议去装" 和 "已经装了但仍没拿到持久化"。
  function isInstalled() {
    try {
      return window.matchMedia("(display-mode: standalone)").matches
        || window.matchMedia("(display-mode: fullscreen)").matches
        || window.navigator.standalone === true;   // iOS 的私有属性
    } catch (e) { return false; }
  }

  function ensurePersistent() {
    if (persistAsked) return;
    persistAsked = true;
    try {
      const s = navigator.storage;
      if (!s || !s.persist || !s.persisted) { persistState = false; return; }
      s.persisted()
        .then((already) => (already ? true : s.persist()))
        .then((ok) => { persistState = !!ok; refreshProgressBar(); })
        .catch(() => { persistState = false; });
    } catch (e) { persistState = false; }
  }

  function saveProgress() {
    try {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify({ v: 1, s: streaks }));
      ensurePersistent();
    } catch (e) { /* 隐私模式下不可写，进度仅在本次会话有效 */ }
  }

  function tierOf(id) {
    const n = streaks[id] || 0;
    return n > TIER_MAX ? TIER_MAX : n;
  }

  function notifyChange(id) {
    changeHooks.forEach((fn) => { try { fn(id); } catch (e) { /* 单个订阅者出错不影响其余 */ } });
  }

  function setStreak(id, n) {
    if (n > 0) streaks[id] = n; else delete streaks[id];
    saveProgress();
    notifyChange(id);
  }

  function skipMastered() {
    try { return localStorage.getItem(FILTER_KEY) !== "0"; } catch (e) { return true; }
  }

  /* ---------- 回想范围选择（issue #3） ----------
   * 三种范围：全部 / 语义域（其下可选词根） / 日耳曼核心词（按词性细分）。
   * 词根不是顶层筛选项：它是选定语义域后的第二级，和图谱钻取模型一致。
   * 与「跳过已牢固」叠加：先按范围圈定，再按记忆状态过滤。
   * 持久化在 localStorage，和进度同级——换设备本来也不跟进度，不必同步。
   */
  function defaultScope() { return { type: "all", domainId: null, rootId: null, pos: null }; }

  function loadScope() {
    try {
      const raw = localStorage.getItem(SCOPE_KEY);
      if (!raw) return defaultScope();
      const j = JSON.parse(raw);
      if (!j || typeof j !== "object") return defaultScope();
      // 旧版顶层 root 会在数据加载后迁到「该词根所属语义域 + 该词根」。
      const s = {
        type: j.type,
        domainId: j.domainId || (j.type === "domain" ? j.id : null) || null,
        rootId: j.rootId || (j.type === "root" ? j.id : null) || null,
        pos: j.pos || null,
      };
      return ["all", "domain", "root", "germanic"].includes(s.type) ? s : defaultScope();
    } catch (e) { return defaultScope(); }
  }

  function saveScope(s) {
    try { localStorage.setItem(SCOPE_KEY, JSON.stringify(s)); } catch (err) { /* 不可写就只影响本次 */ }
  }

  function setScope(s) {
    recallScope = s;
    saveScope(s);
    startMode(mode); // 范围变了，队列要重建
  }

  // 词是否落在当前范围内。root 型挂在词根上，germanic 型没有 root_ids，
  // 于是既不在任何语义域也不在任何词根下——只能靠「日耳曼核心词」档圈住。
  function inScope(w) {
    const s = recallScope;
    if (s.type === "all") return true;
    if (s.type === "domain") {
      if (s.rootId) return (w.root_ids || []).includes(s.rootId);
      const dm = domainsById[s.domainId];
      return !!dm && (w.root_ids || []).some((rid) => dm.has(rid));
    }
    if (s.type === "germanic") {
      if (w.decomposable !== "germanic") return false;
      return !s.pos || posTokens(w.pos).includes(s.pos);
    }
    return true;
  }

  function posTokens(p) {
    return String(p || "").split("/").map((x) => x.trim()).filter(Boolean);
  }

  // 范围名：进度行与按钮上显示「范围 · 施力」这样的一句话。
  function scopeName() {
    const s = recallScope;
    if (s.type === "all") return "全部";
    if (s.type === "domain") {
      const dm = domains.find((d) => d.id === s.domainId);
      const domainLabel = dm ? dm.chinese : "语义域";
      if (!s.rootId) return domainLabel;
      const r = roots.find((x) => x.id === s.rootId);
      return r ? `${domainLabel} › ${r.root}` : domainLabel;
    }
    if (s.type === "germanic") return s.pos ? `日耳曼·${s.pos}` : "日耳曼核心词";
    return "全部";
  }

  // 统计：语义域词数、词根词数、日耳曼词词性分布。数据加载后算一次，
  // 范围选择器里的每个选项显示「名称（N 词）」。
  let domains = [];
  let domainsById = Object.create(null);
  let domainCounts = Object.create(null);
  let rootCounts = Object.create(null);
  let germanicPos = [];
  let germanicPosCounts = Object.create(null);
  let germanicTotalCount = 0;
  let rootToDomain = Object.create(null);

  function buildScopeStats() {
    domainsById = Object.create(null);
    domainCounts = Object.create(null);
    rootCounts = Object.create(null);
    germanicPosCounts = Object.create(null);
    germanicTotalCount = 0;
    rootToDomain = Object.create(null);
    const posSet = new Set();
    for (const dm of domains) {
      domainsById[dm.id] = new Set(dm.root_ids || []);
      domainCounts[dm.id] = 0;
      for (const rid of dm.root_ids || []) {
        if (!rootToDomain[rid]) rootToDomain[rid] = dm.id;
      }
    }
    for (const w of words) {
      if (w.stub || !w.core_image) continue;
      if (w.decomposable === "germanic") {
        germanicTotalCount += 1;
        posTokens(w.pos).forEach((p) => {
          posSet.add(p);
          germanicPosCounts[p] = (germanicPosCounts[p] || 0) + 1;
        });
        continue;
      }
      const seen = new Set();
      for (const rid of w.root_ids || []) {
        rootCounts[rid] = (rootCounts[rid] || 0) + 1;
        const did = rootToDomain[rid];
        if (did && !seen.has(did)) {
          seen.add(did);
          domainCounts[did] += 1;
        }
      }
    }
    germanicPos = [...posSet].sort((a, b) => (germanicPosCounts[b] || 0) - (germanicPosCounts[a] || 0));
    migrateScope();
  }

  function migrateScope() {
    const s = recallScope;
    // 旧顶层「词根」迁到「该词根所属语义域 + 该词根」。
    if (s.type === "root") {
      const rid = s.rootId;
      const did = rid ? rootToDomain[rid] : null;
      recallScope = did && rootCounts[rid]
        ? { type: "domain", domainId: did, rootId: rid, pos: null }
        : defaultScope();
      saveScope(recallScope);
      return;
    }
    if (s.type === "domain") {
      if (!s.domainId || !domainsById[s.domainId]) {
        recallScope = defaultScope();
        saveScope(recallScope);
        return;
      }
      if (s.rootId && (!rootCounts[s.rootId] || !domainsById[s.domainId].has(s.rootId))) {
        recallScope = { type: "domain", domainId: s.domainId, rootId: null, pos: null };
        saveScope(recallScope);
      }
      return;
    }
    if (s.type === "germanic" && s.pos && !germanicPos.includes(s.pos)) {
      recallScope = { type: "germanic", domainId: null, rootId: null, pos: null };
      saveScope(recallScope);
    }
  }

  loadProgress();
  probePersisted();

  let words = [];
  let roots = [];
  let recallScope = loadScope();
  let mode = "explore";
  let queue = [];
  let idx = 0;
  let revealed = false;
  let score = { asked: 0, self_ok: 0 };

  const study = document.getElementById("study");
  const cardEl = document.getElementById("study-card");
  const actEl = document.getElementById("study-actions");
  const progEl = document.getElementById("study-progress");

  function esc(s) {
    const d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  /* 遮罩泄题内容。
   * 词源里常出现拉丁词形（respectus / importare），它包含英语词形，
   * 直接显示等于给出答案；核心画面里若出现该词的中文义项，
   * 就退化成中译英——恰是本项目反对的记法。两者都要遮。 */
  function maskAnswer(text, w) {
    if (!text) return "";
    let out = text;
    const stem = w.word.length > 4 ? w.word.slice(0, Math.ceil(w.word.length * 0.7)) : w.word;
    for (const t of [w.word, stem]) {
      if (t && t.length >= 3) {
        out = out.replace(new RegExp(t, "gi"), MASK);
      }
    }
    for (const zh of w.chinese || []) {
      if (zh && zh.length >= 2) out = out.split(zh).join(MASK);
    }
    return out;
  }

  function shuffle(a) {
    const r = a.slice();
    for (let i = r.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [r[i], r[j]] = [r[j], r[i]];
    }
    return r;
  }

  // ---------- 回想模式 ----------
  function buildRecallQueue() {
    // root 与 germanic 全量出题（issue #2）：日耳曼词本身就是词根、无法再拆，
    // 核心画面即题面，推导行对 germanic 词显示提示（见 renderRecall）。
    // 排除 stub：占位词条的释义、中文、例句都是模板，揭示面板会显示
    // 「a thing or action related to stall」并把 stall 当成中文义项——一张坏卡。
    // 范围（issue #3）：先按范围圈定，再与「跳过已牢固」叠加。范围圈不出词
    // （比如某词根下全是 stub 或没有可用词）时退回全量，和"全牢固退回全量"同理。
    const scoped = words.filter((w) => w.core_image && !w.stub && inScope(w));
    const pool = scoped.length ? scoped : words.filter((w) => w.core_image && !w.stub);

    // 跳过已牢固的词。队列 5248 词、一轮 50 词要走 105 轮，不过滤的话
    // 会反复撞见同一批熟词 —— 这是分层状态的实际用处，颜色只是它的可视化。
    if (!skipMastered()) return shuffle(pool);
    const left = pool.filter((w) => tierOf(w.id) < TIER_MAX);
    // 全都背牢了就退回全量，否则界面会变成一句"这一轮结束"再无下文
    return shuffle(left.length ? left : pool);
  }

  function renderRecall() {
    const w = queue[idx];
    if (!w) return renderDone();

    const rootNames = (w.root_ids || [])
      .map((r) => (roots.find((x) => x.id === r) || {}).root)
      .filter(Boolean).join(" / ");

    let html = `<div class="card-label">看画面，想这个词</div>`;
    html += `<div class="card-image">${esc(maskAnswer(w.core_image, w))}</div>`;
    html += `<div class="card-meta">词性 ${esc(w.pos)}`;
    // 词根名也要过遮罩：拉丁词形常包含英语词本身
    // （signum 含 sign、publicus 含 public、classis 含 class、organon 含 organ），
    // 直接显示等于把答案写在题面上。
    if (rootNames) html += ` · 词根 <b>${esc(maskAnswer(rootNames, w))}</b>`;
    html += `</div>`;
    // recall_hint 是专为本模式写的推导：不点名中文义项，遮罩后仍完整。
    // root_logic 通常以"→ 中文义项"收尾，遮完只剩一串方块，提示不足。
    // germanic 词没有这两个字段（设计使然：它本身就是词根），给一句提示
    // 而不是空行——既解释为什么没有推导，也呼应"日耳曼核心词靠画面记"的主张。
    const logic = w.recall_hint || w.root_logic;
    const logicLine = logic
      ? esc(maskAnswer(logic, w))
      : (w.decomposable === "germanic" ? "日耳曼核心词，靠画面记" : "");
    html += `<div class="card-logic">${logicLine}</div>`;

    if (revealed) {
      // 当前状态放在揭晓区：此刻正是"我到底记住没有"的判断时点。
      // 题面上不显示，免得未答就先看到自己的进度而影响自评。
      const t = tierOf(w.id);
      html += `<div class="card-answer">
        <div class="answer-word">${esc(w.word)}
          <span class="answer-ipa">${esc(w.phonetic || "")}</span>
          <button class="speak-btn" data-word="${esc(w.word)}">◍ 发音</button>
          <span class="chip tier-${t}">${TIER_LABEL[t]}</span>
        </div>
        <div class="answer-def">${esc(w.native_definition)}</div>
        <div class="answer-zh">${(w.chinese || []).map((c) => `<span class="chip zh">${esc(c)}</span>`).join("")}</div>
        ${(w.examples || []).length ? `<ul class="answer-ex">${w.examples.slice(0, 2).map((e) => `<li>${esc(e)}</li>`).join("")}</ul>` : ""}
      </div>`;
    }
    cardEl.innerHTML = html;

    actEl.innerHTML = revealed
      ? `<button class="act primary" data-act="ok">想起来了</button>
         <button class="act" data-act="miss">没想起来</button>`
      : `<button class="act primary" data-act="reveal">显示答案</button>
         <button class="act" data-act="skip">跳过</button>`;

    progEl.innerHTML = `回想模式 · 范围「${esc(scopeName())}」 · 第 ${idx + 1} / ${queue.length} 词`
      + (score.asked ? ` · 已答 ${score.asked}，想起 ${score.self_ok}` : "")
      + progressBar(true);
  }

  /* 进度条：各层计数 + 范围选择 + 过滤开关 + 导出/导入。
   * 塞在 #study-progress 里而不是新开一块，是因为视觉审计会查 #study 的
   * 横向溢出，多一块就多一处要在 390px 上让位的东西。
   * showScope 只在回想模式为真：范围是回想队列的口径，词族模式不适用。 */
  function progressBar(showScope) {
    const c = window.ESG.progress.counts();
    const done = c[1] + c[2] + c[3];
    const chips = TIER_LABEL.map((lab, t) =>
      t === 0 ? "" : `<span class="chip tier-${t}">${lab} ${c[t]}</span>`).join("");
    return `<div class="prog-row">
      ${showScope ? scopeSelector() : ""}
      ${done ? chips : '<span class="prog-hint">答过的词会记在这里</span>'}
      <label class="prog-toggle"><input type="checkbox" data-act="toggle-skip"
        ${skipMastered() ? "checked" : ""}>跳过已牢固</label>
      <button class="prog-btn" data-act="export" title="${esc(exportHint())}">导出</button>
      <button class="prog-btn" data-act="import">导入</button>
      ${storeBadge()}
    </div>`;
  }

  /* 范围选择器：原生 select 按层级展开。
   * 语义域：类型 → 域 → 该域下的词根（可空，表示练整个域）
   * 日耳曼词：类型 → 词性（可空，表示全部日耳曼词）
   * 在 390px 上靠 .prog-row 的 flex-wrap 换行，不引入自定义下拉。 */
  function scopeSelector() {
    const s = recallScope;
    const typeOpts = [
      ["all", "全部"],
      ["domain", "语义域"],
      ["germanic", "日耳曼词"],
    ].map(([v, lab]) =>
      `<option value="${v}"${s.type === v ? " selected" : ""}>${lab}</option>`).join("");

    let extra = "";
    if (s.type === "domain") {
      extra += `<select class="scope-select" data-act="scope-domain" aria-label="语义域">`
        + domains.map((d) =>
          `<option value="${esc(d.id)}"${s.domainId === d.id ? " selected" : ""}>`
          + `${esc(d.chinese)}（${domainCounts[d.id] || 0} 词）</option>`).join("")
        + `</select>`;
      extra += `<select class="scope-select" data-act="scope-root" aria-label="词根">`
        + `<option value=""${!s.rootId ? " selected" : ""}>整个语义域（${domainCounts[s.domainId] || 0} 词）</option>`
        + rootsInDomain(s.domainId).map((r) =>
          `<option value="${esc(r.id)}"${s.rootId === r.id ? " selected" : ""}>`
          + `${esc(r.root)}（${rootCounts[r.id] || 0} 词）</option>`).join("")
        + `</select>`;
    } else if (s.type === "germanic") {
      extra += `<select class="scope-select" data-act="scope-pos" aria-label="词性">`
        + `<option value=""${!s.pos ? " selected" : ""}>全部 ${germanicTotalCount} 词</option>`
        + germanicPos.map((p) =>
          `<option value="${esc(p)}"${s.pos === p ? " selected" : ""}>${esc(p)}（${germanicPosCounts[p] || 0} 词）</option>`).join("")
        + `</select>`;
    }

    return `<span class="prog-toggle scope-sel">范围
      <select class="scope-select" data-act="scope-type" aria-label="范围类型">${typeOpts}</select>${extra}</span>`;
  }

  function rootsInDomain(domainId) {
    const ids = domainsById[domainId];
    if (!ids) return [];
    return roots
      .filter((r) => ids.has(r.id) && rootCounts[r.id])
      .sort((a, b) => (rootCounts[b.id] || 0) - (rootCounts[a.id] || 0));
  }

  /* 存储状态做成看得见的文字，不是 tooltip。
   * 手机上长按基本看不到 title，而"我的进度到底保不保得住"恰恰是只有在
   * 手机真机上才能确认的事 —— 藏在 hover 里等于没有。 */
  function storeBadge() {
    if (persistState === null) return "";           // 还没问出来，别闪一下
    if (persistState === true) {
      return '<span class="prog-store ok" title="只有你手动清除浏览器数据才会丢失">'
        + "存储已锁定</span>";
    }
    // 没拿到持久化。区分两种情形，给的建议不一样。
    return isInstalled()
      ? '<span class="prog-store warn" title="浏览器未授予持久化配额，磁盘紧张时可能回收。请偶尔导出备份。">'
        + "存储未锁定 · 建议导出备份</span>"
      : '<span class="prog-store warn" title="菜单里选「添加到手机」装成应用，浏览器通常就会授予持久化配额">'
        + "存储未锁定 · 可加到主屏幕</span>";
  }

  // 存储状态是异步问出来的，问到了要把已渲染的进度条换掉。
  // 只替换 .prog-row 而不重写整个 progEl —— 前面那句"第 N / M 词"是同级文本，
  // 整片重写会把它一起冲掉。
  function refreshProgressBar() {
    const row = progEl.querySelector(".prog-row");
    // 范围选择器只在回想模式渲染，刷新进度条时要按当前模式恢复
    if (row) row.outerHTML = progressBar(mode === "recall");
  }

  function exportHint() {
    const p = persistState;
    if (p === true) return "进度已持久化：只有你手动清除浏览器数据才会丢失。仍建议偶尔导出备份。";
    if (p === false) return "进度是 best-effort 存储：磁盘紧张时可能被浏览器回收。把本站加到主屏幕可提升为持久化。";
    return "导出进度为 JSON 文件。进度只存在这台浏览器，换设备不会同步。";
  }

  // 进度只存在这台浏览器，清缓存就没了 —— 导出是唯一的备份手段
  function exportProgress() {
    const blob = new Blob([window.ESG.progress.exportJSON()], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "esg-progress.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }

  function importProgress() {
    const inp = document.createElement("input");
    inp.type = "file";
    inp.accept = ".json,application/json";
    inp.addEventListener("change", () => {
      const f = inp.files && inp.files[0];
      if (!f) return;
      const rd = new FileReader();
      rd.onload = () => {
        try {
          const n = window.ESG.progress.importJSON(String(rd.result));
          startMode(mode); // 队列依赖进度，导入后要重建
          alert(`已导入 ${n} 个词的进度`);
        } catch (e) {
          alert("导入失败：" + e.message);
        }
      };
      rd.readAsText(f);
    });
    inp.click();
  }

  progEl.addEventListener("click", (e) => {
    const el = e.target.closest("[data-act]");
    if (!el) return;
    if (el.dataset.act === "export") exportProgress();
    else if (el.dataset.act === "import") importProgress();
  });

  progEl.addEventListener("change", (e) => {
    const typeEl = e.target.closest('[data-act="scope-type"]');
    if (typeEl) {
      const type = typeEl.value;
      if (type === "domain") {
        setScope({ type, domainId: (domains[0] || {}).id || null, rootId: null, pos: null });
      } else if (type === "germanic") {
        setScope({ type, domainId: null, rootId: null, pos: null });
      } else {
        setScope(defaultScope());
      }
      return;
    }
    const domainEl = e.target.closest('[data-act="scope-domain"]');
    if (domainEl) {
      setScope({ type: "domain", domainId: domainEl.value || null, rootId: null, pos: null });
      return;
    }
    const rootEl = e.target.closest('[data-act="scope-root"]');
    if (rootEl) {
      setScope({
        type: "domain",
        domainId: recallScope.domainId,
        rootId: rootEl.value || null,
        pos: null,
      });
      return;
    }
    const posEl = e.target.closest('[data-act="scope-pos"]');
    if (posEl) {
      setScope({ type: "germanic", domainId: null, rootId: null, pos: posEl.value || null });
      return;
    }
    const el = e.target.closest('[data-act="toggle-skip"]');
    if (!el) return;
    try { localStorage.setItem(FILTER_KEY, el.checked ? "1" : "0"); } catch (err) { /* 不可写就只影响本次 */ }
    startMode(mode); // 过滤条件变了，队列要重建
  });

  // ---------- 词族模式 ----------
  // 给出词根与核心概念，列出该族各词的"词义"，让人把词与义配对。
  // 检验的是：知道词根含义后，能否靠前缀推出各词分工。
  function buildFamilyQueue() {
    // 单趟扫词库建 root_id → 成员词 的索引。原来是对每个词根都把整个词库
    // filter 一遍（309 词根 × 5248 词 = 162 万次），切一次词族模式实测 100ms。
    const byRoot = new Map();
    for (const w of words) {
      if (w.decomposable !== "root" || w.stub) continue;
      for (const rid of w.root_ids || []) {
        let fam = byRoot.get(rid);
        if (!fam) { fam = []; byRoot.set(rid, fam); }
        fam.push(w);
      }
    }
    // 仍按 roots 的顺序产出，成员也保持词库原序 —— 与旧实现逐词根 filter 等价。
    // shuffle 内部先 slice 再洗，不会动到索引里的数组。
    const out = [];
    for (const r of roots) {
      const fam = byRoot.get(r.id);
      if (fam && fam.length >= 4) out.push({ root: r, family: shuffle(fam).slice(0, 6) });
    }
    return shuffle(out);
  }

  function renderFamily() {
    const q = queue[idx];
    if (!q) return renderDone();
    const { root, family } = q;

    let html = `<div class="card-label">同一个词根，各词分工是什么</div>`;
    html += `<div class="card-root">${esc(root.root)}
      <span class="card-root-concept">${esc(root.core_concept)}</span></div>`;
    html += `<div class="card-meta">${esc(root.core_image)}</div>`;

    html += `<table class="fam-table"><tbody>`;
    for (const w of family) {
      const zh = (w.chinese || []).slice(0, 3).join(" / ");
      // 只在揭晓后按状态着色。未揭晓时单词列必须是纯遮罩 —— 审计会断言
      // .fam-word 全部匹配 /^▢+$/，着色不影响文本但没必要提前给暗示。
      const tc = revealed ? ` tier-${tierOf(w.id)}` : "";
      html += `<tr>
        <td class="fam-word${tc}">${revealed ? esc(w.word) : MASK}</td>
        <td class="fam-logic">${esc(maskAnswer(w.recall_hint || w.root_logic, w))}</td>
        <td class="fam-zh">${revealed ? esc(zh) : ""}</td>
      </tr>`;
    }
    html += `</tbody></table>`;
    if (!revealed) {
      html += `<p class="card-hint">先按推导想出每个词，再核对</p>`;
    }
    cardEl.innerHTML = html;

    actEl.innerHTML = revealed
      ? `<button class="act primary" data-act="ok">对上了</button>
         <button class="act" data-act="miss">没对上</button>`
      : `<button class="act primary" data-act="reveal">显示答案</button>
         <button class="act" data-act="skip">跳过</button>`;

    progEl.innerHTML = `词族模式 · 第 ${idx + 1} / ${queue.length} 族`
      + (score.asked ? ` · 已答 ${score.asked}，对上 ${score.self_ok}` : "")
      + progressBar(false);
  }

  function renderDone() {
    const rate = score.asked ? Math.round(score.self_ok / score.asked * 100) : 0;
    cardEl.innerHTML = `<div class="card-label">这一轮结束</div>
      <div class="card-image">共答 ${score.asked} 题，自评想起 ${score.self_ok} 题（${rate}%）</div>
      <p class="card-hint">自评结果不保存——这一版只用来检验词条信息够不够支撑回想</p>`;
    actEl.innerHTML = `<button class="act primary" data-act="restart">再来一轮</button>`;
    progEl.innerHTML = "";
  }

  function render() {
    if (mode === "recall") renderRecall();
    else if (mode === "family") renderFamily();
  }

  function next(selfOk) {
    if (selfOk !== null) {
      score.asked++;
      if (selfOk) score.self_ok++;
      // 只有回想模式的自评计入单词状态。词族模式一次出 6 个词、只收一个
      // 「对上了」，它检验的是词根推导能力而不是单个词的记忆，
      // 混进来会让状态失真。
      if (mode === "recall") {
        const w = queue[idx];
        if (w && w.id) window.ESG.progress.record(w.id, selfOk);
      }
    }
    idx++;
    revealed = false;
    render();
  }

  actEl.addEventListener("click", (e) => {
    const b = e.target.closest("[data-act]");
    if (!b) return;
    switch (b.dataset.act) {
      case "reveal": revealed = true; render(); break;
      case "ok": next(true); break;
      case "miss": next(false); break;
      case "skip": next(null); break;
      case "restart": startMode(mode); break;
    }
  });

  // 答案区的发音按钮：复用 graph.js 暴露的实现
  cardEl.addEventListener("click", (e) => {
    const b = e.target.closest(".speak-btn");
    if (b && window.ESG && typeof window.ESG.speak === "function") {
      window.ESG.speak(b.dataset.word);
    }
  });

  function startMode(m) {
    mode = m;
    idx = 0;
    revealed = false;
    score = { asked: 0, self_ok: 0 };
    queue = m === "recall" ? buildRecallQueue() : m === "family" ? buildFamilyQueue() : [];
    render();
  }

  function setMode(m) {
    mode = m;
    document.querySelectorAll(".mode-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.mode === m);
    });
    const isStudy = m !== "explore";
    study.classList.toggle("hidden", !isStudy);
    document.querySelector("main").classList.toggle("hidden", isStudy);
    document.body.classList.toggle("study-active", isStudy);
    // 图谱从隐藏的学习面板切回时，容器尺寸刚刚恢复，通知 D3 重新量尺寸。
    if (!isStudy) window.dispatchEvent(new Event("resize"));
    if (isStudy) startMode(m);
  }

  // 测试钩子：返回某个词在回想模式下的完整题面（未揭晓部分）。
  // 审计据此逐词扫泄题——若让测试自己实现一份遮罩，改坏渲染时测试仍会通过，
  // 这个坑真踩过一次（词根名没遮，而测试自带的遮罩把它遮了）。
  window.ESG = window.ESG || {};
  window.ESG.recallPrompt = function (word) {
    const w = typeof word === "string" ? words.find((x) => x.id === word) : word;
    if (!w) return null;
    const rootNames = (w.root_ids || [])
      .map((r) => (roots.find((x) => x.id === r) || {}).root)
      .filter(Boolean).join(" / ");
    return [
      maskAnswer(w.core_image, w),
      maskAnswer(w.recall_hint || w.root_logic, w),
      maskAnswer(rootNames, w),
      // pos 也要过遮罩：noun 这个词的词性就是 "noun"，直接拼接等于把答案
      // 印在题面上。全库目前只此一例，但缺陷是通用的——凡词性名本身也是词条
      // 的（noun / verb / adjective…）都会中。
      maskAnswer(w.pos, w),
    ].join(" ");
  };

  /* 进度 API。graph.js 用它给词节点上色、在详情面板做手动标记。
   * 放在 window.ESG 上而不是各自读 localStorage：只有一处负责写盘和广播，
   * 否则图谱标记完学习卡不知道，得刷新才同步。 */
  window.ESG.progress = {
    TIER_LABEL: TIER_LABEL,
    TIER_MAX: TIER_MAX,
    tierOf: tierOf,
    labelOf: function (id) { return TIER_LABEL[tierOf(id)]; },

    // 回想模式的自评落到这里。想起来 +1，没想起来归零。
    record: function (id, ok) {
      setStreak(id, ok ? Math.min((streaks[id] || 0) + 1, TIER_MAX) : 0);
    },

    // 手动标记：生词 → 已背 → 牢固 → 生词。
    // 不做成两态开关，是为了让"标了但还想再见到"和"标了别再出题"能分开表达。
    cycle: function (id) {
      const next = { 0: 2, 1: 2, 2: TIER_MAX, 3: 0 }[tierOf(id)];
      setStreak(id, next);
      return tierOf(id);
    },

    counts: function () {
      const c = [0, 0, 0, 0];
      Object.keys(streaks).forEach((id) => { c[tierOf(id)] += 1; });
      return c;
    },

    onChange: function (fn) { if (typeof fn === "function") changeHooks.push(fn); },

    // null=还没申请过 true=已持久化（只有手动清除才会丢） false=best-effort
    persisted: function () { return persistState; },

    // 进度只存在这台浏览器，清缓存就没了。导出是唯一的备份手段。
    exportJSON: function () { return JSON.stringify({ v: 1, s: streaks }, null, 1); },
    importJSON: function (text) {
      const j = JSON.parse(text);
      if (!j || !j.s || typeof j.s !== "object") throw new Error("格式不对：缺少 s 字段");
      const clean = Object.create(null);
      let n = 0;
      Object.keys(j.s).forEach((k) => {
        const v = Number(j.s[k]);
        if (Number.isFinite(v) && v > 0) { clean[k] = Math.min(Math.round(v), TIER_MAX); n += 1; }
      });
      streaks = clean;
      saveProgress();
      notifyChange(null);
      return n;
    },
  };

  // 数据由 graph.js 加载后共享，避免重复请求
  window.ESG.initStudy = function (data) {
    words = data.words.words;
    roots = data.roots.roots;
    domains = (data.domains && data.domains.domains) || [];
    buildScopeStats();
    document.querySelectorAll(".mode-btn").forEach((b) => {
      b.addEventListener("click", () => setMode(b.dataset.mode));
    });
    // 键盘：空格显示答案 / 回车下一题
    document.addEventListener("keydown", (e) => {
      if (mode === "explore" || !queue.length) return;
      // INPUT 是跳过开关；SELECT 是范围选择器——聚焦时按空格/回车
      // 是原生控件操作，不能同时触发学习卡的快捷键
      if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT") return;
      if (e.code === "Space") {
        e.preventDefault();
        if (!revealed) { revealed = true; render(); }
      } else if (e.code === "Enter" && revealed) {
        next(true);
      }
    });

  };
})();
