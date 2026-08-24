# 下一轮做什么

> 写于 2026-08-24，接 `e8788f7`（第六十七批）之后。
> 先读 [HANDOFF.md](HANDOFF.md) 的「先读这一条」和「三、这次会话踩实的坑」。

## 第一步：派词根批（已切好，不用再切）

`drafts/rchunk41.txt` … `rchunk46.txt`，各 60 词，共 360，全是分类器判为拉丁的词。

派 6 个子代理，每个一句话：

```
你在 repo C:/Users/86134/.claude-ctf-workspace/english-semantic-graph 工作。

先读 docs/draft-spec.md——唯一的规格来源。你要写的是词根型，R 行和 W 行都要写，
重点看「R 行 —— 10 列」「词根任务专有：建根前先查库」，以及最后一节
「关于本文件里出现的检查结果」。

你的编号是 4N：读 drafts/rchunk4N.txt（60 词），输出到 drafts/r_chunk4N.tsv。
凑不到 3 个成员的族不值得开根，那些词按日耳曼型写（第 5、6 列留空）。

写完必须自己跑规格里那两条自检命令，都过了才算完。
只回报：写了几族几词、哪些根其实已建模、两项自检的实际输出。
```

**这批里已知值得开的根**（数字是 `drafts/root_backlog_from_67.txt` 里的成员数）：

```
laxare   8    radius   7    pax      6    primus   6
linum    4    coquere  4    idein    4    nomen    4
```

**下面这三个不是新根，是补词**——我核过 `roots.json` 的 origin：

| 代理可能报的 | 库中已有 | 依据 |
|---|---|---|
| `plicare` | `plic` | |
| `ligare` | `ligare` | 同名已存在 |
| `regere`（5 词） | `rect` **或** `regula` | 两个都是 regere：`rect` 收分词 rectus 一支（correct/direct），`regula` 收木尺一支（regular/regulate）。分给哪支要按词义判 |

这类「同一词根已用别的拉丁词形建过模」的误报**已发生六七次**，派发时务必让代理按规格搜 origin 字段而不是只搜 id。

## 第二步：合并后必做

```bash
python scripts/migrate_germanic_to_root.py     # 新根会孤立先收的日耳曼词
python tests/visual_audit.py                   # 建了新根 = 改了图结构
```

`migrate_germanic_to_root.py` 每次重扫大约 5/6 是子串噪声，逐个核词源再决定，别照单全收。真命中要把 `MOVE` 字典补上一条（累积记录，脚本幂等）。

## 第三步：日耳曼池

`drafts/germanic_remaining.txt`（974 词未入库）切 6 片 × 60，chunk 编号从 **37** 起（1-36 已用）。

## 顺带可做（不急）

- **`medius` 补词**：`medium` / `immediate` / `intermediate` / `medieval` / `meanwhile` 都在考研词表里未收，这族现在只 2 词（means / meantime），补上就稳了
- **`esse` 族**：`drafts/root_batch_notes.txt` 里挂着，entity / essence / essential / absent / interest 五词，`praeesse` 复合词已先建（与 `dare` 同一模式）
- **`root_batch_notes.txt` 其余待接**：`gravis` ← grief/grieve；`mons` ← mount/mountain/amount；`mirari` ← admire/miracle/mirror；`metiri` ← measure/immense/dimension（与希腊 `metron` 同源但异语，未合并）
- **近反义词全库富化**：现在词根批与日耳曼批都留空（见 HANDOFF 四），要补该另做一次统一的，不要按批零敲

## 别做

- 别手写 `build_batchNN.py`（1141 字节/词 vs 走 TSV 的 19）
- 别整读 `data/words.json`（3.1 MB ≈ 80 万 token），用 `python -c` 取字段
- 别自动归族（拼写聚类判不出词族，本会话又踩了一遍，见 HANDOFF 三·3）
- 别在代理还在写的时候读它的文件（会读到半成品快照）
