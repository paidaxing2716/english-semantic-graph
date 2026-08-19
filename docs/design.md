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

#### `decomposable` —— 可拆性标记（必填）

考研词表中只有约两成词能靠拉丁/希腊词根拆解（见 `ai_pipeline/classify_wordlist.py`）。
给不可拆的词硬安词根，等于教给学习者错的词源，所以必须如实标记：

| 取值 | 含义 | root_ids / root_logic |
|------|------|----------------------|
| `root` | 确由词根派生，且词根已建模 | 必填 |
| `root_pending` | 确可拆，但词根尚未建模 | 必须留空 |
| `germanic` | 日耳曼核心词，本身即词根 | 必须留空 |
| `loanword` | 借词/专名，拆解无认知价值 | 必须留空 |
| `phrasal` | 短语动词，意义在介词隐喻 | 必须留空 |
| `opaque` | 词源不明，无法有效拆解 | 必须留空 |

质量门 Q11 会拒绝两种写法：非 root 型却挂了词根；root 型但 root_logic 里
出现"词源不同""此处按…理解"这类承认推导不成立的对冲措辞。
后者是真实发生过的形态——`seclude` 曾被挂到 duc 词根下，
而它来自 claudere（关闭），与 ducere（引导）不同源。

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

## 3.5 数据质量标准（Quality Gates）

> 以下为质量红线，AI 生成与人工审核均须遵守。**宁缺毋滥：解释不了的义项要诚实标注，绝不能编造牵强词源。**

### Q1 多义词覆盖规则

- 每个中文义项都应有对应的解释路径：`core_concept`（概念统一）或 `semantic_expansions`（逐义项解释）至少覆盖其一。
- 若某义项既无法用核心概念统一、也没有清晰的词源链，**必须**在 `semantic_expansions` 中标注 `[词义独立，非词根直接推导]`，不得强解释。
- 判断标准：一个词 `chinese` 义项数 N，其解释应能覆盖其中「非直接衍生」的义项，解释覆盖率下限 60%。

### Q2 词源诚实原则

- `root_logic` 只写**可靠的词根组合推导**（con- + press → 压到一起 → 压缩）。
- 间接引申（figure→数字、contract→感染 这类链条长的）必须注明「间接引申」并给出真实链条，禁止写「XX 就是 XX 的形状」这类想当然推导。
- 无法确认来源的义项标注 `[来源存疑]`，禁止猜测。

### Q3 英文定义优先

- `native_definition` 必须是**英文**释义（不是中英混写），供学习者建立概念。
- `core_concept` 用英文短语，中文只出现在 `chinese` 和 `core_image` 中。

### Q4 画面有效性

- `core_image` 必须是**一个可想象的场景**（有人/物/动作），不能是抽象概念复述（"压力就是压"无效）。
- 画面服务于记忆：越具体、越有画面感越好。

### Q5 例句真实性

- `examples` 至少 1 条，优先真实语料（新概念英语、真题、语料库），AI 生成需人工确认无语法/语义错误。
- 例句场景 `scene` 标注该句的使用情境。

### Q6 可追溯

- 所有词条保留 `origin` 来源；AI 生成词条在 `source` 标记生成方式，人工审核后置为 `human-reviewed`。

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