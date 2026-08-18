# 开发路线（Roadmap）

> 更新：2025-08-18

---

## 总路线

```
v0.1  数据模型 + 10 核心词根 + D3 交互图谱   ← 当前
v0.2  100 词实验集（验证核心概念模型）
v0.3  AI 自动生成词条 + 人工审核
v1.0  考研 5500 词完整图谱
```

---

## v0.1 — 地基（当前阶段）

- [x] GitHub 仓库 `english-semantic-graph`
- [x] 项目宪章（目标明确）
- [x] 数据模型 schema（design.md）
- [ ] 10 个核心词根数据入库
- [ ] D3 交互图谱（frontend/）
- [ ] 数据校验脚本（tests/validate.py）
- [ ] 首次提交推送

**验收**：打开 `frontend/index.html`，能看到 10 个词根 + 首批单词的交互图谱，点节点可看详情。

---

## v0.2 — 100 词实验集

- [ ] 100 词全部入库（10 词根 × 每根 ~10 词）
- [ ] Obsidian Vault 生成器（data → .md）
- [ ] 学习模式验证（探索模式）

**验证问题**：一个核心概念是否能解释一整个词族？

---

## v0.3 — AI 生成管线

- [ ] `ai_pipeline/word_analyzer.py`：输入单词 → 自动生成全字段词条
- [ ] 人工审核流程（生成 → 审核 → 入库）
- [ ] 词条批量生成脚本

---

## v1.0 — 考研 5500 词

- [ ] 5500 词图谱
- [ ] 学习模式：探索 / 复习 / 测试
- [ ] 部署为可访问的 Web 页面

---

## 核心词根清单（v0.1 首批 10 个）

```
figur       形状        → figure, configure, figurative, disfigure
press       压          → pressure, impress, express, suppress, compress
form        形状/形成   → form, formal, inform, transform, perform
tract       拉/拖      → attract, extract, contract, distract, tractor
pose        放置       → position, compose, expose, propose, oppose
mit/miss    送         → admit, commit, permit, transmit, mission
spect       看         → inspect, respect, prospect, spectator
scrib/script 写        → describe, prescribe, transcript, manuscript
duc/duct    引导       → conduct, produce, introduce, educate, reduce
port        运送       → import, export, transport, portable, report
```

> 这 10 个词根覆盖数百个考研词，是验证模型的最小集。