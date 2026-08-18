# 开发路线（Roadmap）

> 更新：2025-08-18

---

## 总路线

```
v0.1    数据模型 + 10 核心词根 + D3 交互图谱   ✅ 已完成
v0.1.1  图谱可用性升级（搜索 + 分层钻取 + 近义词组合）✅ 已完成
v0.1.2  移动端响应式改造（手机/平板适配）← 当前
v0.2    100 词实验集（验证核心概念模型）
v0.3    AI 自动生成词条 + 人工审核
v1.0    考研 5500 词完整图谱
```

---

## v0.1 — 地基（已完成 ✅）

- [x] GitHub 仓库 `english-semantic-graph`
- [x] 项目宪章（目标明确）
- [x] 数据模型 schema（design.md）
- [x] 10 个核心词根数据入库（50 词 + 70 关系 + 54 例句）
- [x] D3 交互图谱（frontend/）
- [x] 数据校验脚本（tests/validate.py，含质量门 Q1-Q6）
- [x] 语义扩展补全 + 词源修正（质量红线落地）

---

## v0.1.1 — 图谱可用性升级（已完成 ✅）

> 详见 [plan-ux-graph.md](plan-ux-graph.md)

- [x] 搜索框：单词/词根/中文三路搜索，定位高亮 + 弹详情
- [x] 图谱分层钻取：默认只显词根+概念，点击展开词族
- [x] 近义词概念中转：concepts.json 增加 `type: cluster` 聚合概念
- [x] words.json 增加 `synonym_group` / `synonym_note`
- [x] 试点 2 组近义词（make a choice / make clear）+ 4 新词（库 54 词）
- [x] 详情面板显示「近义词组 + 语境差异」
- [x] validate.py 校验 synonym_group 引用

---

## v0.1.2 — 移动端响应式改造（当前阶段 · 已确认方案）

> 详见 [plan-mobile.md](plan-mobile.md)

- [ ] CSS：768px 断点 + 上下布局 + 底部详情抽屉（含动画）
- [ ] JS：详情面板抽屉化（class 切换 + 关闭按钮）、touch 手势适配
- [ ] 手机端图例/提示折叠
- [ ] 小屏节点/字号/连线密度微调
- [ ] 推送部署 + 线上验证（桌面 + 手机 UA）

**验收**：375px 宽度下搜索置顶、图谱可双指缩放单指拖动、点击节点底部抽屉出详情；桌面端不变。

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