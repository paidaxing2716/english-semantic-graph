# 日耳曼型词条起草规格

> 派子代理批量起草「不可拆词」词条时的规格。第五十四批起用，
> 六个子代理并行时各写一片，此文件是唯一来源——改这一处即可，
> 不必改六份 prompt，避免各自漂移。
> 派发时只需说：「读 docs/germanic-draft-spec.md，你的编号是 NN」。

Repo: `C:/Users/86134/.claude-ctf-workspace/english-semantic-graph`

读 `drafts/chunkNN.txt`，为每个词写一行 10 列（制表符分隔），输出到 `drafts/g_chunkNN.tsv`。

## 10 列

| 列 | 内容 |
|---|---|
| 1 | word — 小写，与输入表一致 |
| 2 | pos — noun / verb / adjective / adverb / preposition / conjunction / pronoun；双词性写 `noun / verb` |
| 3 | phonetic — 英式 IPA，斜杠包裹，如 `/siːd/` |
| 4 | origin — 中文词源，一句。日耳曼词写 `古英语 sæd ← 原始日耳曼语 *sēdiz（撒下之物）`；借词写真实来源。**不许编造古英语词形**；确实无定论就写明「更早词源不明」 |
| 5 | native — 英文释义，一句，小写开头，末尾不加句号 |
| 6 | image — **最要紧的一列**。中文具体场景，15–35 字，能在脑子里看见的画面，不是释义 |
| 7 | zh — 中文义项，`/` 分隔，1–4 个，最常用在前 |
| 8 | examples — 两个英文例句，`|` 分隔，各 5–12 词，句末句号 |
| 9 | concept — `english phrase – 中文解释`，用短破折号 `–` |
| 10 | expansions — `|` 分隔，逐条说明某义项如何从核心画面推出。列 7 有 2 个以上义项时**必填** |

**列数必须正好 10。** 单义词第 10 列可以为空，但**前面那个制表符不能省**——写成 9 列会被 `germanic_from_draft.py` 拦下。这条原先是宽松的（只要求 ≥9），结果尾列缺制表符的行能静默通过；已收紧。

## 第 6 列的硬规则（质量门会拦）

image 里**不得出现列 7 中任何长度 ≥2 的中文义项**。学习者看到画面时单词和中文都被遮住，必须只靠画面想起这个词。点名义项等于自泄答案。

- 错：`dusk`，zh `黄昏/暮色`，image `天色渐晚，到了黄昏` ← 含「黄昏」
- 对：`dusk`，zh `黄昏/暮色`，image `屋里没开灯，书页上的字一行行糊成一片`
- 对：`blade`，zh `刀刃/叶片/桨叶`，image `一片扁而薄的钢，边上磨出一道亮线，指腹一挨就发凉`

## 第二条规则：属于真词族的词要跳过

本批只收**没有可迁移拉丁/希腊词根**的词。若某词词源可追到一个拉丁/希腊动词或名词，且该词根在考研词表里有 **3 个以上**成员，就**不要写这一行**，改列到 `drafts/skipped_chunkNN.txt`，格式 `word<TAB>拉丁词根（该族在词表内的成员）`。

判定族大小时有三个坑，都踩过：

**一、只数「该词根承载词义」的词，不数仅含它作前缀的词。**
- `benefit` = bene＋facere，承载词义的是 **facere** → 属 `fac` 族，不属 bonus
- `benign` = bene＋genus → 属 `gen` 族
- 所以 `bonus` 不是 4 词族，它只有自己，须按日耳曼型写

**二、同形异源要分清，看常用义的真来源。**
- `bull`（公牛）← 古英语 *bula*，日耳曼源；只有「教皇诏书」那义才出拉丁 *bulla*
- `trade` ← 中古低地德语（与 *tread* 同源），与拉丁 *tradere* 无关
- `canvas` ← *cannabis*（大麻），与 *canna*（芦苇）是两个词，不属 canalis 族

**三、同一个词根可能已用别的拉丁词形建过模。**
上报前先拿你认定的拉丁词形去搜 `data/roots.json` 的 origin 字段。例：contrast/cost 的词根是 *stare*，但库中已建模为 `sta`（其 origin 就写「拉丁语 stare」），属补词而非新根。

族成员只有 1–2 个的**不值得跳过**，按日耳曼型写。成员是否真存在，去 `data/english_reference.json` 核。

## 文风

平实、具体、可感，重感官细节而非抽象。像一个观察者在说刚看见的东西，不像词典。中文里不用长破折号，不用感叹号。多义项要让人觉得是同一样东西的不同侧面。

## 自检（两个都必须过，不过就改到过）

```
python scripts/germanic_from_draft.py drafts/g_chunkNN.tsv -o /tmp/probeNN.json   # 须打印 [OK] N 词
python scripts/screen_draft_etymology.py drafts/g_chunkNN.tsv                     # 须打印 [OK]
```

筛查脚本按子串匹配，会有假阳性（如上面 canvas 那例），它的输出是「应考虑」而非「必须改」，逐条核过再动。

只回报：写了几行、跳了几个、两项自检是否通过。
