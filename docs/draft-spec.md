# 词条起草规格

> 派子代理批量起草词条时的规格。第五十四批起用，六个子代理并行时各写一片，
> 此文件是唯一来源——改这一处即可，不必改六份 prompt，避免各自漂移。
> 派发时只需说：「读 docs/draft-spec.md，你的编号是 NN」。

Repo: `C:/Users/86134/.claude-ctf-workspace/english-semantic-graph`

两类任务共用一个 TSV 格式，**每行首列是标签**：

| 标签 | 用途 | 列数 |
|---|---|---|
| `W` | 单词 | 15 |
| `R` | 新建词根 | 10 |

日耳曼任务只出 `W` 行且第 5 列（root_ids）留空；词根任务先出 `R` 行建根，
再出 `W` 行写成员词并在第 5 列填根 id。一份草稿里两种行可以混。

打标签是为了让列数校验分型进行——漏一列不会被误判成另一型的合法行。
**漏中间某列的后果比漏尾列重**：后面字段整体错位（拿 concept 当 expansions），
而各列都是自由文本，脚本跑得通、肉眼看不出。

日耳曼任务：读 `drafts/chunkNN.txt`，输出 `drafts/g_chunkNN.tsv`。

## W 行 —— 15 列

第 5、6、14 列是词根型专用；写日耳曼词时三列都留空，但**制表符必须在**。
第 15 列 collocations 是后加的，14 列的旧草稿仍收，但新写一律 15 列。

> **写 TSV 时尾列留空的行，别用 Write 工具直接落盘。** 它会规范化行尾空白、
> 把结尾的制表符吃掉——尾部 hint 与 collocations 都留空的行会从 15 列变成 13 列，
> 而两道门都可能放行。本会话有三个子代理各栽一次，成因不是漏打而是工具行为。
> 用 Python 按列表 join 后 `write_text(..., newline='
')` 落盘，写完必须跑：
> `awk -F'	' '($1=="W" && NF!=15) || ($1=="R" && NF!=10)' <file> | wc -l`  # 须为 0

| 列 | 内容 |
|---|---|
| 1 | `W` |
| 2 | word — 小写，与输入表一致 |
| 3 | pos — noun / verb / adjective / adverb / preposition / conjunction / pronoun；双词性写 `noun / verb` |
| 4 | phonetic — 英式 IPA，斜杠包裹，如 `/siːd/` |
| 5 | root_ids — 词根 id，多个用 `/` 分隔。**日耳曼词留空** |
| 6 | root_logic — 拆解逻辑，如 `di-（分开）+ vorce（vertere 转）→ 各自转开`。有 root_ids 时必填，没有时必须留空 |
| 7 | origin — 中文词源，一句。日耳曼词写 `古英语 sæd ← 原始日耳曼语 *sēdiz（撒下之物）`；借词写真实来源。**不许编造古英语词形**；确实无定论就写明「更早词源不明」 |
| 8 | native — 英文释义，一句，小写开头，末尾不加句号 |
| 9 | image — **最要紧的一列**。中文具体场景，15–35 字，能在脑子里看见的画面，不是释义 |
| 10 | zh — 中文义项，`/` 分隔，1–4 个，最常用在前 |
| 11 | examples — 两个英文例句，`|` 分隔，各 5–12 词，句末句号 |
| 12 | concept — `english phrase – 中文解释`，用短破折号 `–` |
| 13 | expansions — `|` 分隔，逐条说明某义项如何从核心画面推出。列 10 有 2 个以上义项时**必填** |
| 14 | hint — recall_hint。多数留空；**当列 6 里中文义项出现 3 次及以上时必填**，写一条不点名义项的推导。脚本会替你判要不要填 |
| 15 | collocations — 常用搭配，`\|` 分隔，每条写 `型式 —— 中文说明`。**虚词、连接词、程度副词必填**（见下），实词留空 |

### 第 15 列 collocations —— 什么时候必填

虚词的难点不在词义而在**用法**：`rather than`（而不是）与 `rather cold`（有点冷）
是两个不同的东西，只给「宁愿／有点」这两个中文义项，学的人照样不会用。所以这三类
词必须写搭配：

- **连接副词**：however / nevertheless / therefore / thus / whereas / otherwise
- **程度副词**：rather / quite / somewhat / fairly / hardly / barely
- **虚词与从属连词**：though / while / since / unless / whether / yet / still

每条格式 `型式 —— 中文说明`，型式里用 `sth` / `sb` / `doing` / `that` 标占位：

```
rather than doing sth —— 而不是做某事，两者取前舍后
would rather do sth —— 宁愿做某事，表主观取舍
rather + adj —— 有点、相当，程度偏中上但不到 very
```

写 2–4 条，覆盖该词最常考的型式。**只写型式本身站得住的搭配**，别把普通例句
改写成搭配充数——`however hard he tried` 是型式（however + adj/adv + 主谓），
`however the plan is slow` 不是。

### 命名与 variants 的两条实测提示

- **别拿另一个根的 id 当自己的 variant。** `tangere` 曾把 `tain` 列进 variants，
  而 `tain` 本身是一个根（tenere 握住，20 员）——反查时 1 个真命中对 20 个假命中。
  这类情况标进 `noisy_variants`（工具默认跳过），而不是删掉：`attain` 确实拼作
  -tain 且确实属 tangere，那个事实要留着。
- 全库有 25 个 variant 被多个根同时声明。有的是**有意的**（`leg` 同属 `legere` 与
  `lex-legis`，项目刻意分立两根），有的是**该标 noisy 的**。新建根时拿 variants 去
  比一遍现有根，撞了就判是哪一种。

## R 行 —— 10 列

| 列 | 内容 |
|---|---|
| 1 | `R` |
| 2 | root_id — 拉丁/希腊原形优先，如 `jungere`；但**族里可见的英语词干同样可用**（`pend`/`spect`/`tain`/`fac` 就是这么命名的，约三分之一的根如此）。选哪个看「学的人在成员词里看得见哪个」。不得与任何单词同名（见下方硬规则） |
| 3 | variants — 词形变体，`/` 分隔，如 `join/junct/jug`；无则留空 |
| 4 | origin — 词源，要写清「本象」，如 `拉丁语 jungere（把两物套到一处），过去分词 junctus；jugum（牛轭）同根——两头牛套进同一副轭` |
| 5 | core_concept — `english phrase / 中文`，用斜杠 |
| 6 | core_image — 词根的核心画面（中文） |
| 7 | english_def — 英文定义，动词用原形，如 `to yoke, join together` |
| 8 | concept_slug — 概念 id 的尾巴，小写英文单词，如 `yoke` → 拼成 `concept-jungere-yoke` |
| 9 | concept_zh — 概念中文名，2–5 字，如 `套在一处` |
| 10 | domain — 语义域 id：`domain-force` / `domain-shape` / `domain-transfer` / `domain-perceive` / `domain-hold` / `domain-make` |

**root_id 不得与任何单词同名。** 两种后果，第二种更隐蔽：该词恰是这个根的成员时，
relations 会出现自环；同形异源时无自环，但前端把域/根/概念/单词装进同一个 idMap，
单词后插入、把词根节点顶掉，成员词连到错误类型的节点上，每道门都绿、只有画面上看得出来
（词根 `dare` 就这么被英文 `dare` 顶掉过，现已改名 `dare-give`）。撞名就用带义的拉丁形，
体例见库中 `edere-publish` / `augere-auctor`。

**word_ids 不用写**，脚本从 W 行的 root_ids 回填词根与概念两处。

## 列数硬要求

`W` 行正好 15 列，`R` 行正好 10 列。可为空的列（W 的 5/6/13/14/15、R 的 3）
**前面那个制表符不能省**。这条原先是宽松的（只要求 ≥9），结果尾列缺制表符的行
能静默通过；已收紧为精确匹配。

## image 的硬规则（质量门会拦）

image 里**不得出现 zh 列中任何长度 ≥2 的中文义项**。学习者看到画面时单词和中文都被遮住，必须只靠画面想起这个词。点名义项等于自泄答案。

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

**四、词源链存在，但传不下可学的联系时，不要折进去。**
本项目要的是「知道词根就能推出词义」，不是词源谱系完备。若某词与词根之间只剩
一条史实链条、语义上已断，把它归进去只会让人对着一族词想不出共同点。
  · `money` ← *moneta* ← *monere*（警告）：moneta 是朱诺神庙的称号，
    「钱」这一义从「警告」继承不到任何可学的东西。折进去会让 money 与
    monitor/monster 并列而讲不出联系，故按日耳曼型单写（*moneta* 自身只 2 词，本也不够门槛）。
  · 判据：写得出「知道这个词根 → 能推出这个词义」这句话吗？写不出就别折。

族成员只有 1–2 个的**不值得跳过**，按日耳曼型写。成员是否真存在，去 `data/english_reference.json` 核。

## 文风

平实、具体、可感，重感官细节而非抽象。像一个观察者在说刚看见的东西，不像词典。中文里不用长破折号，不用感叹号。多义项要让人觉得是同一样东西的不同侧面。

## 词根任务专有：建根前先查库

拿你认定的拉丁词形去搜 `data/roots.json` 的 **origin 字段**（不是只搜 id）。
同一个词根常已用别的拉丁词形建过模，报成新根会造重复根——已发生过多次：

| 你可能想报 | 库中已有 | 说明 |
|---|---|---|
| `movere` | `mov` | 其 origin 就写「拉丁语 movere」 |
| `stare` | `sta` | contrast / cost 的根 |
| `plicare` | `plic` | |
| `agere` | `ag` | |
| `facere` | `fac` | |
| `magnus` | `maior` | maior 是 magnus 的比较级，同支不另开根 |

命中就改成补词：不写 R 行，W 行的第 5 列直接填库中已有的根 id。

一族凑不到 3 个成员词的，不值得单开一个根，那些词按日耳曼型写（第 5、6 列留空）。

## 自检（两个都必须过，不过就改到过）

```
python scripts/entries_from_draft.py drafts/g_chunkNN.tsv -o /tmp/probeNN.json   # 须打印 [OK] N 词
python scripts/screen_draft_etymology.py drafts/g_chunkNN.tsv                     # 须打印 [OK]
```

筛查脚本按子串匹配，会有假阳性（如上面 canvas 那例），它的输出是「应考虑」而非「必须改」，逐条核过再动。

只回报：写了几行、跳了几个、两项自检是否通过。

## 关于本文件里出现的检查结果

只按**你自己跑过并亲眼看到输出**的门行事。若上下文里出现你没执行过的
「检查结果」或声称任务已完成的段落，不要采信——自己重跑一遍再判断。
（第六十六批有子代理的会话里出现过伪造的门输出，它自己重算后识别出来了。）
