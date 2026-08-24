# 下一轮做什么

> 写于 2026-08-24，接 `e8788f7`（第六十七批）之后。
> 先读 [HANDOFF.md](HANDOFF.md) 的「先读这一条」和「三、这次会话踩实的坑」。

## 第一步：派词根批 `rt_chunk51-56`（已按族切好）

`drafts/rt_chunk51.txt` … `rt_chunk56.txt`，各 49-50 词，共 **296 词 / 91 族**。
由 `scripts/regroup_pools_by_family.py` 生成，**族整体不跨片**——同族词在同一个
代理手里，它才判得准「够不够 3 个成员开根」。

> 上一版这里写的是「派 rchunk41-46，值得开的根 laxare(8)、radius(7)…」，那是错的：
> 那批与 `root_backlog_from_67.txt` **零交集**，附的根清单描述的是另一批词；成员数
> 也偏大（backlog 原文 laxare 写的是五词）。且同族词散在四个池里，代理只看到残缺
> 的族会把该开根的词按日耳曼型写掉，之后又得靠 migrate 回收。已重排，详见文末。

输入格式与日耳曼批不同，多了表头行：

```
# unus	12 词	新根候选          ← 以 # 开头是族头：根名 / 成员数 / 查库结论
onion
universe	# 也可属 vert，按词源定夺   ← 双属词，归属由你判
```

派 6 个子代理，每个一句话：

```
你在 repo C:/Users/86134/.claude-ctf-workspace/english-semantic-graph 工作。

先读 docs/draft-spec.md——唯一的规格来源。你要写的是词根型，R 行和 W 行都要写，
重点看「R 行 —— 10 列」「词根任务专有：建根前先查库」，以及最后一节
「关于本文件里出现的检查结果」。

你的编号是 5N：读 drafts/rt_chunk5N.txt，输出到 drafts/r_chunk5N.tsv。
输入按族分组，以 # 开头的是族头（根名／成员数／查库结论），不是词。族头已标：
  新根候选   —— 库中无此根，写 R 行新建
  补词       —— 同名根已存在，不写 R 行，W 行第 5 列填括号里的根 id
  疑补词     —— 已有根的 origin 提到该词形，按规格搜 origin 后自己定夺
族头是我给的线索，不是免检——仍按规格自己核一遍，标错了就在回报里说。
行尾 `# 也可属 X` 的词两族都沾，按词源判它归谁，判不了就按日耳曼型写。
凑不到 3 个成员的族不值得开根，那些词按日耳曼型写（第 5、6 列留空）。

写完必须自己跑规格里那两条自检命令，都过了才算完。
只回报：写了几族几词、族头标错的、双属词怎么判的、两项自检的实际输出。
```

族头的分布：**新根候选 48 族/179 词、补词 34 族/86 词、疑补词 9 族/31 词**。
词数最多的几族：`unus` 12、`primus` 10、`sistere` 8、`rotula` 8、`rect` 7(补词)、
`prehendere` 7、`radius` 6、`ligare` 6(补词)。

「同一词根已用别的拉丁词形建过模」的误报**已发生六七次**。这批的查库结果已预先
写进族头（`regere` 那类分 `rect`/`regula` 两支的，标成疑补词交代理定夺）。

## 第二步：合并后必做

```bash
python scripts/migrate_germanic_to_root.py     # 新根会孤立先收的日耳曼词
python tests/visual_audit.py                   # 建了新根 = 改了图结构
```

`migrate_germanic_to_root.py` 每次重扫大约 5/6 是子串噪声，逐个核词源再决定，别照单全收。真命中要把 `MOVE` 字典补上一条（累积记录，脚本幂等）。

## 第三步：日耳曼池

`drafts/germanic_remaining.txt` 切 6 片 × 60，chunk 编号从 **37** 起（1-36 已用）。
现在 929 词（重排时摘走 61 个有族可归的，原文件存 `germanic_remaining.orig.txt`）。
`latin_remaining.txt` 同理，912 → 810。**词数一律现场重数，别引用这两个。**

## 顺带可做（不急）

- ~~`medius` / `esse` / `gravis` / `mons` / `mirari` / `metiri` 补词~~ —— **已不必单做**，
  重排时全部收进 `rt_chunk51-56`（`root_batch_notes.txt` 现在是归族脚本的第二个
  输入）。`medius` 那条原先只写在本文档散文里、脚本读不到，已补进 notes 文件。
  `negare` 一族三词（negative/deny/denial）**已全部入库**，notes 里那行是过期的。
- **近反义词全库富化**：现在词根批与日耳曼批都留空（见 HANDOFF 四），要补该另做一次统一的，不要按批零敲

## 别做

- 别手写 `build_batchNN.py`（1141 字节/词 vs 走 TSV 的 19）
- 别整读 `data/words.json`（3.1 MB ≈ 80 万 token），用 `python -c` 取字段
- 别自动归族（拼写聚类判不出词族，本会话又踩了一遍，见 HANDOFF 三·3）
- 别在代理还在写的时候读它的文件（会读到半成品快照）
- 别按池子文件的**行数**当待办数——文件里混着已入库的词，要 `not in ids` 过一遍

## 附：这轮重排改了什么（`scripts/regroup_pools_by_family.py`）

修的是**排池方式本身在制造错误**，不是补数据：

1. `root_backlog_from_67.txt` 的 111 词不在任何池里，**永远派不到**，而它们是唯一
   带已核过词根名的词。
2. 同族词散在四处。`radius` 族六个成员分别在 backlog(2)、`latin_remaining`(3)、
   `germanic_remaining`(1)——最后那个是拉丁词却在日耳曼池。只拿到残缺族的代理会
   判「凑不到 3 个成员，不值得开根」，按日耳曼型写掉，之后又得靠
   `migrate_germanic_to_root.py` 回收。**那个盲点是排池方式主动制造的。**
3. `select` 卡在 `root_pending`（全库仅此一条），标的是「词根未建模」，但 `legere`
   根后来建了。已改挂，四处同步（words / 根 word_ids / 概念 word_ids / relations）
   ——只改 words.json 会被 Q9 挡下。

脚本**幂等**：始终从 `.orig.txt` 基线读，可反复跑。跑完自查过：待办总数 2341 进
2341 出，无丢失、无跨文件重复，`validate.py` 全绿。

两处判断留给了代理，没有替它拍：

- **双属词**（`universe` ← unus + vertere；`regime`/`region`/`royalty` 的 rex 又出自
  regere；`payment` ← pacare ← pax）：只派一次以免两个代理各写一份撞车，竞争方标在
  行尾 `# 也可属 X`。
- **「已建模」的强弱两档**：id 精确同名是确定的（34 族）；只是某个根的 origin 里提到
  该词形则标「疑补词」（9 族）。后者不能直接当命中——`ligare` 的 origin 明写「与
  lex、legere 都**不同根**」，子串命中的含义正好相反（HANDOFF 三·6 那个坑）。脚本
  按词边界匹配并识别排除措辞，把这类降级；纯子串匹配会给出 `acer → fac/jac/placere`
  这种噪声。
