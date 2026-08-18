# 项目宪章（Project Charter）— English Semantic Graph

> 版本：v0.1 draft
> 日期：2025-08-18
> 状态：待用户确认

---

## 一、一句话定位

**不是背单词软件，而是一个"英语概念认知系统"** —— 用图的方式，让学习者用接近英语母语者的方式理解词义。

---

## 二、要解决的问题（核心痛点）

中国英语学习者的典型困境：

```
背了 5500 词，认识中文翻译
      ↓
但阅读时仍然理解不准确、不全面
      ↓
因为掌握的是：word → 中文翻译
而不是：      word → concept → context
```

具体表现：

1. **含义理解不准确**：只记住一个中文对应词，遇到其他语境就懵。
   - 例：`run` 只记得"跑"，遇到 `The machine is running` 就卡住。
2. **一词多义记不住**：`figure` = 数字/人物/图形/身材/认为，看起来毫无关联，只能死记。
3. **用中文思维学英文**：中文翻译只是英文概念在某个场景下的"投影"，不是概念的本身。

---

## 三、核心理念（Core Philosophy）

```
英文单词 ≠ 中文翻译

英文单词 = 核心概念（Concept）
         + 核心画面（Core Image）
         + 语境（Context）
```

学习路径（**中文只是结果，不是入口**）：

```
英文单词
   ↓
核心概念（Concept）
   ↓
核心意象/画面（Core Image）
   ↓
词族网络（Word Family Network）
   ↓
真实语境（Context）
   ↓
中文表达（仅作为最终输出）
```

---

## 四、项目目标（Goals）

### 长期目标

1. 建立一套**稳定的英语语义模型**：一个核心概念解释一整个词族。
2. 建成**数据驱动的英语知识图谱**（English Knowledge Graph）。
3. 覆盖**考研英语 5500 词**，让学习者按"概念网络"而非"孤立符号"的方式掌握词汇。

### 中期目标（产品形态）

1. **Graph View 图谱**：类似 Obsidian，可拖动、缩放、探索词族关系。
2. **学习模式**：
   - 探索模式：自由浏览图谱
   - 复习模式：AI 提问"为什么 configure 有'设置'的意思？"
   - 测试模式：场景化测试（选词填空式，而非"configure = ?"）
3. **AI 助手**：输入一个词（如 `abandon`），自动输出词源、核心概念、画面、词族、语境、记忆方法。

### 可交付的最小目标（MVP）

```
v0.1  数据模型设计 + 10 个核心词根 + D3 交互图谱
v0.2  100 词实验集（验证"一个核心概念解释一整个词族"）
v0.3  AI 自动生成词条 + 人工审核流程
v1.0  考研 5500 词完整图谱
```

---

## 五、非目标（What We Are NOT Doing）

- ❌ 不做传统"英译中"背单词软件
- ❌ 不做普通词根词缀词典（词根只是辅助解释，不是核心）
- ❌ 不在一开始就铺开 5500 词（先验证 100 词模型，再扩展）
- ❌ 不做"AI 生成的大词典"（没有认知模型支撑的数据堆砌）

---

## 六、系统架构（Architecture）

```
Knowledge Base（知识库，数据驱动）
      |
   roots.json / concepts.json / words.json / relations.json / examples.json
      |
      ↓
Graph Renderer（图谱渲染）
      |
Web Graph / Obsidian Vault /（未来）App
```

核心原则：**网页只是"播放器"，数据是核心**。
新增 100 词 = 写入 JSON = 图谱自动出现，不需要改代码。

---

## 七、图谱关系类型（Edge Types）

不能只有 `A ─ B` 一条线，需要：

- `root` — 词根关系（figure ← figur）
- `derived` — 派生关系（configure ← figure）
- `semantic_extension` — 语义扩展（figure 数字 ← figure 形状）
- `synonym` — 近义
- `antonym` — 反义
- `context` — 场景/语境关系

---

## 八、数据模型（Data Model，每个词条须包含）

```
{
  "word": "configure",
  "root": ["con", "figur"],
  "origin": "拉丁语 configurare",
  "native_definition": "to arrange parts into a particular structure",
  "core_concept": "arranging components into desired form",
  "core_image": "工程师把电路模块排列成目标结构",
  "chinese": ["配置", "设置"],
  "examples": [],
  "synonyms": [],
  "antonyms": [],
  "related": [],
  "semantic_expansions": []
}
```

---

## 九、第一阶段：100 词实验集

优先覆盖 10 个高频核心词根（可派生数百个考研词）：

```
figur / press / form / tract / pose /
mit-miss / spect / scrib-script / duc-duct / port
```

验证方法：**一个核心概念是否能解释一整个词族**。
跑通模型后，再扩展到 5500 词。

---

## 十、里程碑（Milestones）

| 版本 | 内容 | 验收标准 |
|------|------|----------|
| v0.1 | 数据模型 + 10 词根 + D3 图谱 | JSON schema 定稿、交互图谱可跑 |
| v0.2 | 100 词实验集 | 100 词全部进入知识库，图谱可浏览 |
| v0.3 | AI 自动生成词条 | 输入单词 → 自动生成全字段词条，人工审核入库 |
| v1.0 | 考研 5500 词图谱 | 词库覆盖 5500 词，学习模式可用 |

---

## 十一、成功标准（Success Criteria）

1. **概念解释力**：学习者看完 `figure` 的核心概念后，能自行推出 `figure out`、`configure`、`figurative` 的含义。
2. **理解准确性**：不再是"中英一对一"，而是"概念 → 场景 → 中文"。
3. **记忆持久性**：画面记忆（core image）让词义长期留存。
4. **可扩展性**：5500 词全部数据驱动，新增词无需改代码。

---

## 十二、项目原则（Working Principles）

1. **数据先行**：先定 JSON schema，再写渲染层。
2. **模型优先**：先用 100 词验证语义模型，再铺数量。
3. **中文是输出，不是入口**：任何词条必须先有英文概念和画面。
4. **图谱要有关系类型**：边（edge）必须有语义类型，否则图谱只是装饰。
5. **AI 生成 + 人工审核**：AI 负责批量生成，人负责质量把关。

---

*本文档为项目宪章 v0.1，待用户确认后定稿，并作为仓库 README 的核心内容。*