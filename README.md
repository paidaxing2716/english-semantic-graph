# English Semantic Graph

> A concept-based English vocabulary knowledge graph.
> 一个基于概念网络的英语词汇认知系统。

**This project is NOT a vocabulary memorization tool.**
**这不是一个背单词软件。**

It aims to build an English semantic graph where words are connected through:

```
Concept
  → Core Image
  → Root
  → Word Family
  → Context
```

The goal is to help learners understand English concepts the way native speakers do — instead of memorizing Chinese translations.

核心理念：

```
英文单词 ≠ 中文翻译
英文单词 = 核心概念 (Concept) + 核心画面 (Core Image) + 语境 (Context)
```

中文只是最终输出，不是入口。Chinese is the output, not the entry point.

---

## 项目文档

- [项目宪章 / Project Charter](docs/PROJECT_CHARTER.md) — 目标、理念、里程碑
- [系统设计 / Design](docs/design.md) — 架构与数据模型
- [开发路线 / Roadmap](docs/roadmap.md) — 开发计划

---

## 目录结构

```
english-semantic-graph/
├── README.md                 # 项目理念
├── LICENSE                   # MIT
├── data/                     # 核心知识库（数据驱动）
│   ├── roots.json            # 词根
│   ├── concepts.json         # 核心概念
│   ├── words.json            # 单词
│   ├── relations.json        # 关系网络
│   ├── examples.json         # 例句
│   └── lexicon.json          # 外部词白名单（近/反义词防造词）
├── docs/
│   ├── PROJECT_CHARTER.md    # 项目宪章
│   ├── design.md             # 系统设计
│   └── roadmap.md            # 开发路线
├── frontend/                 # 图谱展示层
│   ├── index.html
│   ├── graph.js
│   └── style.css
├── ai_pipeline/              # AI 生成工具（v0.3 起）
└── tests/
    ├── validate.py           # 数据校验（含质量门 Q1-Q8）
    └── visual_audit.py       # 前端视觉质量门（对比度/重叠/越界）
```

---

## 里程碑

| 版本 | 内容 |
|------|------|
| v0.1 | 数据模型 + 10 核心词根 + D3 交互图谱 |
| v0.2 | 100 词实验集（验证"一个概念解释一整个词族"） |
| v0.3 | AI 自动生成词条 + 人工审核 |
| v1.0 | 考研 5500 词完整图谱 |

---

## 许可

MIT License