# 开发路线（Roadmap）

> 更新：2026-08-19

---

## 总路线

```
v0.1    数据模型 + 10 核心词根 + D3 交互图谱   ✅ 已完成
v0.1.1  图谱可用性升级（搜索 + 分层钻取 + 近义词组合）✅ 已完成
v0.1.2  移动端响应式改造（手机/平板适配）  ✅ 已完成
v0.2.0  纸张词源地图改版 + 昼夜模式 + 视觉质量门  ✅ 已完成
v0.3    AI 自动生成词条 + 人工审核        ✅ 已完成（提前）
v0.2    100 词实验集                      ✅ 已完成
v1.0    考研 5500 词完整图谱 ← 当前
```

---

## v0.1 — 地基（已完成 ✅）

- [x] GitHub 仓库 `english-semantic-graph`
- [x] 项目宪章（目标明确）
- [x] 数据模型 schema（design.md）
- [x] 10 个核心词根数据入库（54 词 + 70 关系 + 54 例句）
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

- [x] CSS：768px 断点 + 上下布局 + 底部详情抽屉（含动画）
- [x] JS：详情面板抽屉化（class 切换 + 关闭按钮）、touch 手势适配
- [x] 手机端图例/提示折叠
- [x] 小屏节点/字号/连线密度微调
- [x] 推送部署 + 线上验证（桌面 + 手机 UA）
- [x] 数据质量门 Q7/Q8：related 死链 + 近反义词造词拦截

**验收**：375px 宽度下搜索置顶、图谱可双指缩放单指拖动、点击节点底部抽屉出详情；桌面端不变。

## v0.3 — AI 生成管线（已完成 ✅）

> 调整顺序：原计划先手写满 100 词（v0.2）再做管线。
> 但"一个概念解释整个词族"在 10 个词根 × 5 词时已得到验证，
> 再手写 46 词验证的是同一件事；而 v1.0 的 5500 词只可能靠管线。
> 故先建管线，再用它扩词——避免手写内容之后又要用管线重跑一遍。

- [x] `ai_pipeline/prompt_builder.py`：从现有词条抽 few-shot + schema 约束
- [x] `ai_pipeline/word_analyzer.py`：调模型生成候选（OpenAI 兼容端点可插拔）
- [x] `ai_pipeline/review.py`：结构检查 → 人工确认 → 合并入库
- [x] 首批 10 词通过管线入库（54 → 64 词）
- [x] 质量门 Q9：概念反向引用完整性

**管线用法**：

```bash
# 1. 生成候选（未配 API 时导出提示词，贴给任意对话模型）
python ai_pipeline/word_analyzer.py depress:press impose:pose -o candidates.json

# 2. 检查（结构错误必须修；外部词需人工确认后加入 lexicon.json）
python ai_pipeline/review.py check candidates.json

# 3. 合并（合并前后各跑一次 validate.py，不过则拒绝落库）
python ai_pipeline/review.py merge candidates.json
```

---

## v0.2 — 100 词实验集（已完成 ✅）

- [x] 100 词入库（每根 9-11 词，figur 6 词——该词族在英语中本就较小）
- [x] 分三批经管线生成 + 审核 + 合并（64 → 76 → 88 → 100）
- [x] 密度压力测试：全展开 112 节点无重叠
- [x] 节点尺寸随画布缩放；手机端一次只展开一个词根
- [x] 视觉质量门新增密度检查
- [ ] Obsidian Vault 生成器（data → .md）
- [ ] 学习模式验证（探索模式）

**验证结论**：词量从 54 涨到 100 后，桌面端全展开 112 个节点仍无重叠；
手机端 390px 画布原本会出现 98 对节点重叠，改为"一次展开一个词根"
加上节点尺寸随画布缩放后降为 0。密度上限已知：小屏靠限制同时展开量来解决。

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