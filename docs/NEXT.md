# 下一轮做什么

> 写于 2026-08-26，接第六十八～七十批之后（分支 `fix/etymology-gates-and-engra-gaps`，PR #1）。
> 先读 [HANDOFF.md](HANDOFF.md) 的「先读这一条」，再读本文件末尾「这轮踩实的坑」。

## 现状（现场数的，不是抄的）

```
3403 词 / 271 根 / 273 概念        带 collocations 的词条 85 个
待办池：germanic_remaining 881 词未入库、latin_remaining 677 词未入库
已用 chunk 编号：1-36、51-56、61-64、71-75    已合并批次：…65-70
```

**词数一律现场重数**，别引用上面这几个：

```bash
python -c "import json;print(len(json.load(open('data/words.json',encoding='utf-8'))['words']))"
```

## 第一步：近反义词全库富化

现在词根批与日耳曼批都把 synonyms/antonyms 留空（`[]`），全库 3403 词里绝大多数
是空的。这件事**不要按批零敲**——要补该做一次统一的全库扫描，否则同一组近义词
分散在不同批次里，写出来的 `synonym_note` 彼此矛盾。

注意 Q8 白名单机制：`validate.py` 有一份 1819 词的已核验白名单，新加的近反义词
若不在白名单里会被挡。先读 `scripts/check_lexicon_gap.py` 弄清登记流程。

## 第二步：日耳曼池 881 词

切 6 片 × 60，chunk 编号从 **37** 起（1-36 已用，51-56/61-64/71-75 也已用）。
拉丁池 677 词同理，两者都要**现场重数**。

派发流程见 HANDOFF.md「派发流程」一节，规格只看 `docs/draft-spec.md`。

## 第三步：把 collocations 铺开

第 15 列是这轮新加的（规格见 draft-spec.md「第 15 列 collocations」）。已回填 85 个
虚词/介词/连接副词。**剩下两类还没有：**

1. 库里还有约 74 个副词/连词/介词类词条没搭配（137 个候选里筛出 63 个已做完，
   剩下的评分较低但仍有价值）。用这段筛：
   ```bash
   python -c "
   import json;W=json.load(open('data/words.json',encoding='utf-8'))['words']
   print([w['id'] for w in W if not w.get('collocations') and any(p in (w.get('pos') or '').lower() for p in ('adverb','conjunction','preposition','pronoun'))][:40])"
   ```
2. **高频动词的搭配比虚词更该做**——短语动词量极大，而这 16 个在库的高频动词
   现在**一条搭配都没有**（实测全为 0）：
   ```
   get make put come go give hold bring run look keep break carry call cut fall
   ```
   顺带一个缺口：**`take` / `set` / `turn` / `stand` 四个根本不在库**，而它们都在
   5299 考研词表里。四个都是短语动词的核心词（take on/over/up、set up/off/aside、
   turn out/down/into、stand for/out/by），缺它们比缺搭配更严重。先补词条再谈搭配。

回填走 `scripts/backfill_collocations.py`（两列 TSV），**不要走
`entries_from_draft.py`**——那条管道是给新词条用的，遇到已入库的词会拒绝，且会
重写其余 14 列。

## 关于「覆盖率」这个数怎么算

`data/english_reference.json`（5299 词形）**同时是两样东西**：考研词表，以及
近反义词的自动核验白名单（它的 `purpose` 字段写的是后者）。拿它直接算覆盖率会
得出「36.3% 未入库」这种数，但那 1922 个里混着 `a` / `he` / `it` / `in` / `and`
这类功能词——它们没有画面也没有词族，按项目自己的规则本就不建词条。

**所以别把「5299 减去已入库」当待办数。** 要算真实覆盖率得先剔掉不可结构化的部分，
`docs/roadmap.md` v1.0 一节做过这个分析（结论是「考研词表中可结构化的部分」），
接手前先读那一节，别自己重算一遍得出个虚高的缺口。

## 顺带可做

- `admire` 可凑 `mirari` 族（miracle/mirror 已入库）、`cage`/`cave` 可凑 `cavea` 族。
  两族都因「凑不到 3 个成员」被写成日耳曼型，现在够数了，但要回改已入库条目。
  chunk54 的子代理点出的。
- `alternate` 挂在 `ternus`（externus/internus）下，而它自己的 root_logic 写着
  「alter（另一个）+ -nate」——看着是错挂。chunk56 的子代理点出的，未核实。
- `amount` 的 origin 写着「拉丁语 ad montem」却以 germanic 入库，同类问题。
- 83 条 `decomposable_note` 用默认文案但 origin 无任何语源线索，需逐条查证才能
  分流（这轮只改了 origin 有明确线索的 578 条）。

## 别做

- 别手写 `build_batchNN.py`（1141 字节/词 vs 走 TSV 的 19）
- 别整读 `data/words.json`（3.4 MB ≈ 80 万 token），用 `python -c` 取字段
- 别自动归族（拼写聚类判不出词族，已踩过多次）
- 别在代理还在写的时候读它的文件（会读到半成品快照）
- 别按池子文件的**行数**当待办数——文件里混着已入库的词，要 `not in ids` 过一遍
- **别只看 `git status` 判断某批做过没有**——`drafts/` 在 .gitignore 里，git 查不到
  痕迹。这轮因此重派了一整轮 6 个代理，做的是上次会话已完成的活。**看文件时间戳。**

## 这轮踩实的坑

### 1. 六处「输出绿色但什么都没发生」的缺陷

| 位置 | 缺陷 | 已修 |
|---|---|---|
| `entries_from_draft` | 撞名门只查「新根撞已有词」，补词批 `new_r` 为空集时形同不存在 | ✅ 加 `batch_w & have_r` |
| `screen_draft_etymology` | 把根 origin 里「与 X 无关」的 X 抽成匹配键，写明不同源反而制造误报 | ✅ 排除措辞过滤 + 词边界 + 前缀不做键，报警 25→10 |
| `regroup_pools_by_family` | `existing()` 只查 id 与 origin，漏查 variants | ✅ 建 variants 索引 |
| `migrate_germanic_to_root` | **压根没有扫描环节**，只套用手写字典，`--dry-run` 恒输出「共 0 词」 | ✅ 加 `--scan` |
| `entries_from_draft` | 只要没挂根就套「日耳曼核心词」文案，578 条借词被写成日耳曼词 | ✅ 按 origin 分流 |
| `frontend/study.js` | `recallPrompt` 把 `w.pos` 直接拼进题面，`noun` 的词性就是 noun → 泄题 | ✅ pos 也过 maskAnswer |

### 2. 双源一致 ≠ 独立验证

engra 词根库与 Wiktionary 交叉出的「一致」档，四片 219 词里子代理仍逐词核出
**16 个真错（7.3%）**，全是拉丁近形异源：

```
manus/manere   planus/plangere   ferre/ferire   cadere/caedere
tendere/tener  cors/chorda       humor(umor)/humus   portus/portio   minium/minus
```

两个源共享拼写驱动的失败模式，会同时错。这类清单是**「值得派」而非「可免检」**。
21 组已沉淀进 `scripts/audit_trap_pairs.py`，但它误报率约 10%，只作线索不作判据。

### 3. 「15 列」这个错位特征已失效

以前 W 行 15 列 = `|` 被打成制表符（本会话发生三次：universal、promote、
accommodate）。现在 15 列是合法的 collocations 格式，那个特征没了。门改成内容
判别：第 15 列非空须含 `——`；**为空时也不能免检**——错位可能把原本为空的 hint
挤到第 15 位，于是空列「看起来合法」而义项说明被挤进 hint 列。

自己检查仍用 `awk -F'\t' '$1=="W" && NF!=15'`（新批）或 `NF!=14`（旧批）。

### 4. 改多处同步的字段要数清有几处

改词根 id 要同步**五处**：`roots.id`、`words.root_ids`、`concepts.root_ids`、
`relations.from/to`、**`domains.root_ids`**。漏第五处时 `validate.py` 报
「domain-shape.root_ids 引用不存在的词根」+ Q10。见 `scripts/rename_root_id.py`。

日耳曼型词条的字段名是 **`decomposable`** 不是 `type`，且 `root_logic` 是必填的
**空串**而非删除。写错会报「缺少必填字段」+ Q11。

### 5. 出错就回退到基线重跑，别在改坏的状态上叠加

这轮改错两次（上面两条），两次都 `git checkout -- data/` 回基线后用改正版重跑。
`data/` 每次改动前先确认 `git status --short data/` 是干净的。

### 6. 写派发指令前先查库

给 chunk75 的指令里要求写 `once`（实际已分在 chunk74，重复派发）、`latter` 与
`farther`（两个都不在库）。子代理以输入文件为准并把对照写进 `later`/`further`
名下，处理是对的。**指令里提到的词，先确认它在哪、在不在库。**

### 7. 中转站并发上限

6 路并行会把中转站打爆（HTTP 200 空响应），5 个代理同批阵亡。**最多 2 路。**
另外有一次代理写完文件但回报没送达——文件落盘近两小时后才发现。若文件已停止
写入且内容完整，可直接验文件，不必等回报。

## 附：这轮的数据来源

词根归属线索取自 [eslsoft/engra](https://github.com/eslsoft/engra)（MIT，2191 个词根，
覆盖 5299 考研词表的 73.1%）。**只取「词→根」这个事实，未取其 mnemonic 文本**——
仓库虽 MIT 但内容疑似源自出版物。

Wiktionary 缓存 2265 个 wikitext 在 `drafts/.etym_cache/`（gitignored，重跑不请求
网络）。测量脚本 `scripts/probe_etymology_coverage.py`：拿库里已挂根的词当标注集，
top1 与库一致 82.6%，有词元的词里 92.9%，判错仅 0.6%，其余是合并/拆分根造成的
多候选歧义——**那类歧义恰恰是你自己的教学决策，机器替不了**。
