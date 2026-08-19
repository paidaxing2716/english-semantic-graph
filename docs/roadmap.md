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
v0.4    语义域分层 + 词表可拆性分析      ✅ 已完成
v1.0    考研词表中可结构化的部分（~1000 词）← 当前
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

## v0.4 — 语义域分层（已完成 ✅）

三级钻取：语义域 → 词根 → 单词。默认层节点数由语义域数量决定，不随词量增长。

- [x] `data/domains.json`：语义域层，10 词根归入 4 域
- [x] 图谱三级钻取；搜索可穿透三层直达单词
- [x] 质量门 Q10：语义域必须恰好覆盖每个词根一次
- [x] `ai_pipeline/density_probe.py`：合成数据实测各规模密度
- [x] 力导向只模拟可见节点（隐藏节点会从背后挤开可见节点）
- [x] 连线距离不得小于两端碰撞半径之和（否则两力矛盾）
- [x] 展开时松开可见节点（钉死状态下碰撞永远解不开）

**实测密度**（1440×790，各层均 0 重叠）：

```
  词数   词根 | 默认层 重叠 | 展开一域 重叠 | 再展一族 重叠
   100    10 |     10   0 |      12   0 |      22   0
   500    50 |     16   0 |      24   0 |      34   0
  1200   120 |     16   0 |      32   0 |      42   0
  2500   250 |     16   0 |      48   0 |      58   0
  5500   550 |     16   0 |      86   0 |      96   0
```

分层前对比：500 词已出现重叠，1000 词 129 对，5500 词 258990 对。

---

## v1.0 — 考研词表中可结构化的部分

> **范围调整**：不是所有词都能拆成词根。对 5299 个考研词条做数据驱动分析
> （从词表自身发现词族，词干至少被 3 个词共享才算真词根）：
>
> | 类别 | 数量 | 占比 |
> |---|---|---|
> | 孤立词，拆了也无同族词可迁移 | 3682 | 69.5% |
> | **可拆（词缀 + 有词族的词根）** | **1081** | **20.4%** |
> | 日耳曼核心词，本身即词根 | 219 | 4.1% |
> | 词族基词 | 125 | 2.4% |
> | 功能词 | 117 | 2.2% |
> | 借词/专名 | 33 | 0.6% |
>
> 适用本方法约 1206 词（22.8%），且这是**上限**：自动匹配靠拼写，
> 会把同形异源的词根混成一族（抽查 6 个高产词族，混入率 16%，
> 如 leg 把 legere/读 与 lex/法 与 leg/肢 混在一起）。
> 人工审词源后预计 800–1000 词。

- [x] 291 个自动发现的词族逐个审词源（判断记录在 `ai_pipeline/etymology_verdicts*.json`）
      - 整族作废 56 个（拼写巧合，如 `adv` 底下混了 venire/ante/visum 三个词根）
      - 拆族 33 个（如 `leg` 拆成 legere 读 / lex 法 / lig 绑缚）
      - 合并 6 个（同一词根被拼写变体拆开，如 duc 与 duce）
      - 剔除混入词 44 个（如 sister 混进 stare 族、mineral 混进 minus 族）
      - **产出 203 族 / 869 词次**，见 `ai_pipeline/vetted_families.json`
      - 另 61 族清理后仅剩 2 词被降级，其词根本身高产（如 spirare、tangere），
        只是考研范围内成员少；含这些则为 264 族 / 970 词次
      - ⚠️ 此数为**下限**：对已知高产词根抽样校准，约 35% 的成员被词干提取
        误判为"孤立词"（如 capere 的 capable/capacity/capture）
- [ ] 词条加 `decomposable` 字段，不可拆的词显式标记而非硬编词根
- [ ] 可结构化词批量入库（~1000 词）
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