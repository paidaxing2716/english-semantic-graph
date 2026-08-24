# 交接文档 — English Semantic Graph 剩余任务

> 重写：2026-08-24（上一版是 08-21 的 721 词口径，已整篇作废）
> 状态：词库 **2865 词 / 239 词根**，考研词表覆盖 **53.6%**（2841/5299）
> 最近提交：`e8788f7` 第六十七批，已推送 main

---

## 先读这一条

**别信任何文档里的词数，包括本文件。开工第一件事是自己数：**

```bash
python -c "
import json
w=json.load(open('data/words.json',encoding='utf-8'))['words']
r=json.load(open('data/roots.json',encoding='utf-8'))['roots']
f=json.load(open('data/english_reference.json',encoding='utf-8'))['words']
ids={x['id'] for x in w}; c=sum(1 for x in f if x in ids)
print(f'{len(w)} 词 / {len(r)} 根 / 覆盖 {c}/{len(f)} = {c/len(f)*100:.1f}%')"
```

本会话早期我照信 roadmap 里的「694 词、下一批是 36」，花了很长一段去修一个**早已合并**的 build_batch36.py。实际是 773 词、36-40 批都已合并；那个 694 是 vetted 清单覆盖数，不是总词数。`roadmap.md` 里的数字同样可能滞后。

另一条同源教训：**代理还在写的文件不要读**。本轮我在 chunk32 写到一半时读它，先看到 `[REVIEW]` 后看到 `[OK]`，两次都是半成品快照。等通知到齐再验。

---

## 一、这个项目现在怎么加词

两种词条类型，**共用一条 TSV 管道**（本会话改的，第六十五/六十七批已验）：

| 类型 | `decomposable` | 关键字段 | 图上表现 |
|---|---|---|---|
| 词根型 | `root` | `root_ids` + `root_logic`（+ 条件性 `recall_hint`） | 有边，连到词根 |
| 日耳曼型 | `germanic` | `root_ids` 与 `root_logic` **必须为空**，用 `decomposable_note` | 孤立节点 |

孤立节点是**用户明确认可**的：「日耳曼核心词也不需要拆，只需要一个意象、画面能让我记住就可以，单音节词也一样……剩下实在难以描述的就先放着」。所以不要为了连边硬造词根。

### 派发流程

```bash
# 1. 切片（60 词一片，6 片并行）
# 2. 派 6 个子代理，每个只说一句：
#    「读 docs/draft-spec.md，你的编号是 NN」+ 输入文件 + 输出文件
# 3. 代理产出 drafts/g_chunkNN.tsv，自己跑两道自检
# 4. 拼批 → 过门 → 合并
cat drafts/g_chunk*.tsv > drafts/batchNN.tsv
python scripts/entries_from_draft.py drafts/batchNN.tsv -o ai_pipeline/batchNN.json
python scripts/screen_draft_etymology.py drafts/batchNN.tsv
python ai_pipeline/review.py check ai_pipeline/batchNN.json
python scripts/check_lexicon_gap.py ai_pipeline/batchNN.json      # 日耳曼批恒为 0
python ai_pipeline/review.py merge ai_pipeline/batchNN.json
python tests/validate.py
python scripts/migrate_germanic_to_root.py    # 只在本批建了新根时跑
python tests/visual_audit.py                  # 只在改了图结构时跑，2-4 分钟
```

`docs/draft-spec.md` 是派发的唯一来源，改那一处即可，不必改六份 prompt。

### 成本

实测我方（主对话）输出字节／词：

| 路径 | 字节/词 |
|---|---|
| 走 TSV，代理起草 | **约 19** |
| 我手写 build_batchNN.py | 1141 |

**不要再手写 build_batchNN.py。** 词根型也走 TSV（`R` 行建根 + `W` 行成员）。
`data/words.json` 现在 3.1 MB，整读一次约 80 万 token——查东西一律用 `python -c` 只取需要的字段。

---

## 二、剩余工作

待处理约 **2390 词**（已剔除 113 个功能词——`a`/`and`/`about` 这类用户说不用加）。

| 池 | 文件 | 未入库 | 说明 |
|---|---|---|---|
| 日耳曼 | `drafts/germanic_remaining.txt` | 974 | 已分类，可直接切片派发 |
| 拉丁 | `drafts/latin_remaining.txt` | 900 | 同上，但要建新根，慢 |
| 已切好待派 | `drafts/rchunk41-46.txt` | 360 | **下一轮就派这批** |
| 本轮回流 | `drafts/root_backlog_from_67.txt` | 111 | 带代理核过的词根名 |

拉丁那 1272 词里，词首严格命中已有词根的只 **244**（补词，快），其余 **1028 要新建根**（慢：定拉丁原形、写本象画面、查是否已用别的词形建过）。所以后半程比日耳曼批慢，按 236 词/批估**还有 10 批**，这个数偏乐观。

### 下一步（按序）

1. **派 rchunk41-46**（已切好，360 拉丁词）。优先把这些根建起来：`laxare`(8 词)、`radius`(7)、`plicare`(6)、`pax`(6)、`primus`(6)、`regere`(5)、`ligare`(5)——数字来自 `root_backlog_from_67.txt` 的统计。它们建好后反查能自动接上后续批次的同族词，**跳过率会往下走**。
2. 每建一批新根，**重跑 `migrate_germanic_to_root.py`**（见下方「自我更新的盲点」）。
3. 日耳曼池继续切片派发。

---

## 三、这次会话踩实的坑（会重演的那些）

### 1. 后建的根会孤立先收的词 —— 自我更新的盲点

先按日耳曼型入库的词，等到后面某批建了它真正的词根，它就变成一条**自相矛盾**的记录：origin 写着拉丁来源，`decomposable_note` 却写「日耳曼核心词，本身即词根」。

- 本轮 `acquaint` 就是：origin 一直写着「← 拉丁语 ad- + cognoscere」，只是此前没有 `gnoscere` 可挂
- `scripts/migrate_germanic_to_root.py` **设计成可重复跑**，`MOVE` 字典累积记录。**每建一批新根就重扫一遍**，已累计三轮
- 重扫时 5/6 是子串噪声，逐个核，别照单全收

### 2. 长度从来不是筛子

反复栽在同一处。`cip`(3 字母)很准，`lat`(3 字母)只 17% 准。区分度要用 `roots.json` 的 **`noisy_variants`** 字段显式标注：

- `ment`（mens）撞拉丁 `-mentum` 后缀：未收词里 29 个命中**全是后缀，真族 0 个**
- `dat`（dare-give）撞 `-ate/-ation`：8 个候选里 6 个是噪音
- `mari`（maritus）撞 `mare`（海）；`nor`（gnoscere）撞 `norma`/`honos`/`north`

标之前先量：`python scripts/find_root_members.py <rootid>`。

### 3. 拼写聚类判不出词族 —— 我这次又踩了一遍

试了两种自动归族，都产出垃圾：

- 按变体前缀：`sta` 拉进 `sister`/`staff`/`stain`，`mov` 拉进 `mother`，`tain` 拉进 `tennis`/`tiny`
- 按共同词干：`comp` 把 `companion`/`company`/`compare`/`compete` 归一族，而它们的根是 *panis*、*par*、*petere*

第二个正是项目文档早写明的失败模式（`find_root_members.py` 就是为替换拼写聚类而写的，其 docstring 直接说「输出是候选清单，须逐词核词源」）。**词源判断交给子代理，主对话只管切片和路由。**

### 4. 改了行格式必须跟着改消费方 —— 同一类半修连出两次

`screen_draft_etymology.py` 两次都是**静默失效**，不是报错：

- 第一次：origin 列位置写死 `row[3]`，而 `W` 行的 `row[3]` 是音标。它拿拉丁词元比对 IPA 串，任何带标签草稿都得到空洞的 `[OK]`
- 第二次：不看第 5 列 `root_ids`，导致词根批**每行都自报**（`mobile` 的 origin 天然要写 *movere*），而脚本给的处理办法是「删掉这些行」，照做会删掉正确成员词

两次都是子代理发现的。**改数据格式后，把所有读该格式的脚本列出来逐个过。**

### 5. 词根 id 与单词撞名有两种后果，第二种隐蔽

- 该词恰是这个根的成员 → `relations` 自环（已栽过）
- **同形异源** → 无自环，但 `frontend/graph.js:169` 起把域/根/概念/单词装进**同一个 `idMap`**，顺序 domain→root→concept→word，后插入者覆盖前者。词根节点被单词顶掉、从 `nodes` 里消失，成员词连到错误类型的节点上。**每道门都绿，只有画面上看得出来**

本轮 `dare` 就是（英文 ← 古英语 *durran* 敢；拉丁 *dare* 给），已改名 `dare-give`。`validate.py` 现有跨集合撞名门挡这个，`entries_from_draft.py` 生成期也挡。撞名就用带义拉丁形，体例见 `edere-publish`/`augere-auctor`。

### 6. 别在词根 origin 里提「某词不属此族」

`screen_draft_etymology.py` 会从词根 origin 里抽 4+ 字母词当该根的**候选形**。想写明排除关系，等于把那个词元加进匹配表，**连报三次假阳性**（本轮 `medius` × `medal`）。排除理由只能记在词条自己的 origin 里。

### 7. 词源链存在 ≠ 可教

规格第四条，判据是：**写得出「知道这个词根 → 能推出这个词义」这句话吗？写不出就别折。**

- `money` ← *moneta* ← *monere*：moneta 是朱诺神庙称号，「钱」从「警告」继承不到任何可学的东西
- `pint` ← *pincta* ← *pingere*：量器壁上画的刻度线
- `medal` ← *medalia*（值半个第纳尔的小钱币）← *medius*：「一半」到「表彰」已断

**`medal` 这条是我自己编错的**：我手写的 root_logic 是「medialia（挂在胸前正中的饰片）← medius（居中）」——「挂在胸前正中」不是词源，是我编的。子代理给出正确词源并判定不该折进去，它对。已撤下重入。手写词源比代理写的更容易出这种事，因为没人复核。

---

## 四、质量红线

| 门 | 内容 |
|---|---|
| **Q12** | `core_image` 不得出现任何长度 ≥2 的中文义项。遮住单词和中文后，画面是唯一抓手，点名义项等于自泄答案 |
| Q12 后半 | `root_logic` 里中文义项出现 ≥3 次时必须有 `recall_hint`（`entries_from_draft.py` 会替你判） |
| Q1 | ≥2 个中文义项必须有 `semantic_expansions` |
| Q8 | 近/反义词必须在 `words.json` ∪ `lexicon.json` 的 external_words 里。**日耳曼与词根批一律留空**，故恒无缺口 |
| 自环 | 词根 id ≠ 任何单词 id（另见上文第 5 条） |
| 例句对齐 | `words.json` 内嵌例句 ↔ `examples.json` 双向一致，`scripts/backfill_examples_json.py` 补 |

近反义词留空是**有意的**：`related` 曾是重复的死链来源（`formerly`/`letter`/`value`/`elect` 都修过），而同族关系图上本来就有；非空还会触发 Q8 登记往返。既有约 1580 条日耳曼词条都是空的，要补该另做一次全库统一的富化，不要按批零敲。

---

## 五、子代理的事

- 用什么模型都行（用户已明确解除限制）
- 6 个并行、每片 60 词是实测的合适规模
- 它们**多次找出我的错**：脚本的列数洞、`screen_draft_etymology` 的两次半修、我给错的词源（`magnify` 的 `facere`、`league` 的 `legare`）、我算错的补词数（19→17）、`medal` 的假词源。**它们的报告要独立复核，但不要预设它们错。**
- 曾有一片的会话里出现**伪造的门输出**（一个假的完成声明、一个假的长度越界报告）。那个代理自己重算四个值发现都在界内、判为伪造，只按亲自跑的门行事。这条判断已写进 `draft-spec.md` 最后一节，不指望每次靠代理自己想到。

---

## 六、跳过率

第六十七批 36%，历史 17%。高是**我选的**：分类器把 `uncertain`（6-8 字母那段，真 latin 占 43-63%）全并进日耳曼批，本就该有一半跳掉——「宁可跳，不可写错型」。

跳掉的词不白费：带着代理核过的词根名进 `skipped_chunkNN.txt`，正是词根批的输入。

`scripts/classify_pool.py --eval` 可复现分类器精度（当前 89.4%，判 latin 86.1% / 判 germanic 94.2%）。**它的阈值全部实测自库内已有的 `decomposable` 标注**，改规则前先跑 `--eval` 拿基线，别凭感觉调。

---

*本文件是给新对话的唯一入口。词数一律现场重数，不要引用本文件里的数字做决策。*
