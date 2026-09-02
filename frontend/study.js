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

  let words = [];
  let roots = [];
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
    // 只用 root 型：其余词没有词根推导可给，出题信息不足
    // 排除 stub：占位词条的释义、中文、例句都是模板，揭示面板会显示
    // 「a thing or action related to stall」并把 stall 当成中文义项——一张坏卡。
    return shuffle(words.filter((w) => w.decomposable === "root" && w.core_image && !w.stub));
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
    html += `<div class="card-logic">${esc(maskAnswer(w.recall_hint || w.root_logic, w))}</div>`;

    if (revealed) {
      html += `<div class="card-answer">
        <div class="answer-word">${esc(w.word)}
          <span class="answer-ipa">${esc(w.phonetic || "")}</span>
          <button class="speak-btn" data-word="${esc(w.word)}">◍ 发音</button>
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

    progEl.innerHTML = `回想模式 · 第 ${idx + 1} / ${queue.length} 词`
      + (score.asked ? ` · 已答 ${score.asked}，想起 ${score.self_ok}` : "");
  }

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
      html += `<tr>
        <td class="fam-word">${revealed ? esc(w.word) : MASK}</td>
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
      + (score.asked ? ` · 已答 ${score.asked}，对上 ${score.self_ok}` : "");
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

  // 数据由 graph.js 加载后共享，避免重复请求
  window.ESG.initStudy = function (data) {
    words = data.words.words;
    roots = data.roots.roots;
    document.querySelectorAll(".mode-btn").forEach((b) => {
      b.addEventListener("click", () => setMode(b.dataset.mode));
    });
    // 键盘：空格显示答案 / 回车下一题
    document.addEventListener("keydown", (e) => {
      if (mode === "explore" || !queue.length) return;
      if (e.target.tagName === "INPUT") return;
      if (e.code === "Space") {
        e.preventDefault();
        if (!revealed) { revealed = true; render(); }
      } else if (e.code === "Enter" && revealed) {
        next(true);
      }
    });

  };
})();
