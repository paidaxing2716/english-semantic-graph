# 系统设计（Design）— English Semantic Graph

> 版本：v0.1 draft

---

## 1. 架构总览

```
Knowledge Base（知识库）
      |
  data/*.json
      |
      ↓
Graph Renderer（图谱渲染层）
      |
  frontend/（D3.js 力导向图）
      |
      ↓
Web / Obsidian Vault /（未来）App
```

**核心原则：数据驱动。** 网页只是"播放器"——新增词条只需写入 JSON，图谱自动更新，无需修改代码。

```
新增 100 个单词
      ↓
写入 JSON
      ↓
图谱自动出现
```

---

## 2. 数据模型（Data Model）

### 2.1 roots.json — 词根

```json
{
  "id": "figur",
  "root": "figur",
  "variants": ["figur", "fig"],
  "origin": "拉丁语 figura（形状、轮廓）",
  "core_concept": "a recognizable form / 一个可被辨认的形态",
  "core_image": "一个清晰可见的轮廓",
  "english_definition": "shape, form, figure",
  "word_ids": ["figure", "configure", "figurative", "disfigure"]
}
```

### 2.2 concepts.json — 核心概念

```json
{
  "id": "concept-figur-recognizable-form",
  "concept": "a recognizable form",
  "chinese": "一个可被辨认的形态",
  "core_image": "一个清晰可见的轮廓",
  "root_ids": ["figur"],
  "word_ids": ["figure", "configure", "figurative", "disfigure"]
}
```

### 2.3 words.json — 单词

> 每个词条携带的信息分三层：**核心层**（必须，支撑理解概念）、**语境层**（必须至少 1 条例句）、**关系层**（推荐，构成图谱的边）。

```json
{
  "id": "configure",
  "word": "configure",
  "pos": "verb",
  "root_ids": ["figur"],
  "root_logic": "con-（一起）+ figur（形状）→ 把零件组合成目标形状",
  "origin": "拉丁语 configurare：con-（一起）+ figura（形状）",
  "native_definition": "to arrange parts into a particular structure",
  "core_concept": "arranging components into a desired form",
  "core_image": "工程师把散落的电路模块排列成目标结构",
  "chinese": ["配置", "设置", "组合"],
  "examples": [
    "The software can be configured to run in different modes."
  ],
  "synonyms": ["arrange", "set up"],
  "antonyms": [],
  "related": ["figure", "figurative"],
  "semantic_expansions": []
}
```

#### 字段定义（单词词条标准 Schema v0.1）

| 字段 | 必填 | 层级 | 说明 | 示例 |
|------|------|------|------|------|
| `id` | ✅ | 核心 | 全局唯一标识 | `configure` |
| `word` | ✅ | 核心 | 单词本身 | `configure` |
| `pos` | ✅ | 核心 | 词性 (noun/verb/adj/adv) | `verb` |
| `root_ids` | ✅ | 核心 | 关联词根 id 数组 | `["figur"]` |
| `root_logic` | ✅ | 核心 | 词根→词义的推导逻辑（为什么是这个词义） | `con-+figur → 组合成形状` |
| `origin` | ✅ | 核心 | 词源（拉丁语/希腊语） | `拉丁语 configurare` |
| `native_definition` | ✅ | 核心 | **英文**释义（先英文后中文） | `to arrange parts...` |
| `core_concept` | ✅ | 核心 | 核心概念——一个概念解释所有义项 | `arranging components into a desired form` |
| `core_image` | ✅ | 核心 | 核心画面/场景（画面记忆） | `工程师排列电路模块` |
| `chinese` | ✅ | 核心 | 中文表达数组（输出层，非入口） | `["配置","设置"]` |
| `examples` | ✅ | 语境 | 例句数组（真实语境，至少 1 条） | `[...]` |
| `synonyms` | ⬜ | 关系 | 近义词数组 | `["arrange"]` |
| `antonyms` | ⬜ | 关系 | 反义词数组 | `[]` |
| `related` | ⬜ | 关系 | 关联词（同词族/概念相关） | `["figure"]` |
| `semantic_expansions` | ⬜ | 关系 | 语义扩展（一词多义的底层规律） | `["figure out：把模糊变清晰"]` |

#### 可选扩展字段（v0.2+ 按需引入）

| 字段 | 说明 |
|------|------|
| `collocations` | 常见搭配（`make a decision`） |
| `level` | 考研频率星级 1-5 |
| `phrasal_verbs` | 动词短语 |
| `patterns` | 句型模式（`configure sth. to do`） |

### 2.4 relations.json — 关系网络

```json
{
  "from": "figure",
  "to": "configure",
  "type": "derived",
  "note": "把形状组合成目标结构"
}
```

关系类型（Edge Types）：

| type | 含义 |
|------|------|
| `root` | 词根关系（figure ← figur） |
| `derived` | 派生关系（configure ← figure） |
| `semantic_extension` | 语义扩展（figure 数字 ← figure 形状） |
| `synonym` | 近义 |
| `antonym` | 反义 |
| `context` | 场景/语境关系 |

### 2.5 examples.json — 例句

```json
{
  "id": "ex-configure-1",
  "word_id": "configure",
  "text": "Please configure the network settings before running the server.",
  "source": "自编/AI生成",
  "scene": "配置服务器网络"
}
```

---

## 3. JSON Schema 规范

- `id`：全局唯一，英文小写 + 连字符
- `root_ids` / `word_ids`：引用其他文件的 id，构成外键关系
- `type`：枚举值为上面 6 种关系类型之一
- 所有中文字段均可为空数组 `[]`，但 `word` / `native_definition` / `core_concept` 为必填

---

## 4. 图谱渲染

- 技术栈：D3.js 力导向图（force-directed graph）
- 节点分类：
  - 词根节点（`figur`、`con-`）
  - 概念节点（`a recognizable form`）
  - 单词节点（`configure`）
- 交互：
  - 拖动节点
  - 滚轮缩放
  - 点击节点 → 侧边栏显示详情（词源、概念、画面、例句、关联词）
  - 按关系类型着色连线

---

## 5. v0.1 范围

- ✅ 10 个核心词根
- ✅ 数据文件：roots / concepts / words / relations / examples
- ✅ 前端：单页 D3 图谱，静态加载 JSON
- ⏳ AI 生成管线（v0.3）
- ⏳ Obsidian Vault 生成器（v0.2+）

---

## 6. 校验

`tests/validate.py`：读取全部 JSON，校验：
- id 唯一性
- 外键引用存在
- 关系类型合法
- 必填字段非空