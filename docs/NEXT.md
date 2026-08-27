# 下一轮做什么

> 现状更新于 2026-08-27，第九十九批（chunk109）之后。
> 分支 `fix/etymology-gates-and-engra-gaps`，PR #1 仍未合。
> 先读 [HANDOFF.md](HANDOFF.md) 的「先读这一条」，再读本文件末尾「这轮踩实的坑」。

## 现状（现场数的，不是抄的）

```
4023 词 / 308 根                考研表覆盖 3995/5299 = 75.4%
带 collocations 的词条 232 个    真实待办 1304 词（剔掉不可结构化的 76 个后）
已用 chunk 编号：1-36、41-56、61-64、71-78、100-111
```

**词数一律现场重数**，别引用上面这几个——这份文件上一版的数字滞后了 600 词，
照着它做会重复劳动：

```bash
python -c "import json;print(len(json.load(open('data/words.json',encoding='utf-8'))['words']))"
```

## 第一步：继续切批补词（当前主线）

**切批不要再手写档位清单**，走 `scripts/cut_next_chunks.py`：

```bash
python scripts/cut_next_chunks.py --start 112 --n 2 --size 30
```

它做了四件手写时会漏的事：剔已入库/已派/不可结构化词、族整体不跨片、按
engra × Wiktionary 双源打档位并摊平到各片、**校验 A 档猜的根真的存在于
roots.json**（最后这条是补的缺陷，见坑八）。派发指令模板见下面「派发指令
必须带的话」。

待办 1304 词按 30 词/片、2 片/批算约 **22 批**。池子是字母序，现在推到 `l`–`m`。
剩余量最大的是 s（443）、t（203）、w（136）、p（131）。

**并发上限 2 路**（6 路会把中转站打爆，见坑七）。

## 第二步：近反义词全库富化（用户明确要求放最后）

词根批与日耳曼批都把 synonyms/antonyms 留空（`[]`），全库绝大多数是空的。
**不要按批零敲**——该做一次统一的全库扫描，否则同一组近义词分散在不同批次里，
写出来的 `synonym_note` 彼此矛盾。

注意 Q8 白名单机制：`validate.py` 有一份已核验白名单，新加的近反义词若不在
白名单里会被挡。先读 `scripts/check_lexicon_gap.py` 弄清登记流程。

## 第三步：collocations 剩下的尾巴

**上一版列的两类都已做完，别再照着做：**

- ~~16 个高频动词一条搭配都没有~~ → 已全部补齐（现场核过，缺口为 0）。
- ~~`take`/`set`/`turn`/`stand` 不在库~~ → 四个都已入库且都有搭配。

**真正剩下的**（现场重数）：

1. **5 个连接副词缺搭配**：`nevertheless` `henceforth` `consequently`
   `accordingly` `meanwhile`。这批的价值在**句法位置**（句首还是句中、跟不跟
   逗号、能不能接从句），不是动词短语那种型式。
2. **5 个连接副词根本不在库**，而它们都在考研词表里：`thereby` `whereby`
   `nonetheless` `albeit` `notwithstanding`。这五个的用法坑比缺搭配更值得做：
   - `thereby` 接 **-ing** 不接从句
   - `whereby` ＝ by which，**前面必须有名词**
   - `albeit` **不接完整句**（albeit brief ✓ / albeit it was brief ✗）
   - `notwithstanding` 是介词，**可前置也可后置**，后置是它独有的
   先补词条再谈搭配。
3. 另有 77 个副词/代词类词条无搭配，但多数是反身代词与纯方位副词
   （`herself`/`everywhere`/`downstairs`），**没有值得教的型式**，不必强凑。
   筛的时候按「这个词有没有站得住的型式」判，别按词性一刀切。

回填走 `scripts/backfill_collocations.py`（两列 TSV），**不要走
`entries_from_draft.py`**——那条管道是给新词条用的，遇到已入库的词会拒绝，
且会重写其余 14 列。

## 派发指令必须带的话

每批派发前我都在重建这份清单，直接抄。缺任何一条都在实测里出过错：

**档位怎么用**——三档的解释，加上「档位是线索不是结论，假阳性 50% 假阴性 30%，
两个方向都核」，以及「B 档空白 ≠ 库里没有，自己查 roots.json」。

**本批特有的陷阱对**：切完片自己扫一遍 A 档，把明显假的先点出来写进指令。
实测每片 A 档有三到五成是假的（`log → logos`、`material → ter-comparative`、
`medical → medius` 这类），点名比让代理从零核省时间，也避免它照抄档位。

**判据优先级**：① 拿库内既有口径判比拿词源直觉判准（举 `danger`→`domus`）
② 规格第四条，词源链存在 ≠ 能传下可学联系（举 `grammar` 挂 / `gramme` 不挂）
③ 3 员下限，**成员要连库里已有的一起数** ④ 新根 id 两个方向都不能与单词撞名。

**拉丁近形异源对**（双源一致仍错 7.3%，全是这一类）：
```
manus/manere   planus/plangere   ferre/ferire   cadere/caedere
tendere/tener  liber/libra       servare/servire  humor(umor)/humus
carus/carrus   tenere/tangere    concilium/consulere   luere-lavare/solvere
fundus/fundere fames/fama        theos/theorein   secare/sequi
cors/chorda    portus/portio     minium/minus     mederi/medius
```

**七条操作规则**：① 不用 Write 写 TSV（尾列制表符留不住），写
`scripts/build_g_chunkNN.py` 用 list join ② W 行 15 列，**第 9 列是 image、
第 12 列是 concept**，第 15 列非空须含 `——` ③ 落盘跑
`awk -F'\t' '$1=="W" && NF!=15'` ④ **origin 里绝不写别的词根的拉丁原形**
⑤ 加 variants 前反查会不会吸走别族的词，会就进 `noisy_variants`
⑥ image 不泄露义项中文 ⑦ 孤立型字段名是 `decomposable` 不是 `type`，
`root_logic` 是必填空串，`decomposable_note` 要分档不能一律套「日耳曼核心词」。

**两片可能撞车时要说明**：同一族的词分到两片（chunk110 的 `master` 与
chunk111 的 `magistrate` 都是 magister）要写明「只写你片里的，若判断该建根就
回报由我统一建」，否则两片各建一次就是重复根。

**回报格式**：400 字以内，只报统计 + A 档核不成立的 + B/C 档自己查出能挂根的
（最有价值）+ 门二逐条判定 + 够 3 员但本片建不了的新根候选 + 库内既有问题
（只报不改）。别贴 TSV 内容。

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

### 2b. 匹配器的假阴性同样危险（29%）

单源匹配的 45% 假阳性已记在上面。但它**召回也差**：第八十八批 31 词里有 9 个
（29%）被判成「族凑不到 3 员、按孤立词条写」，实际库中早有能收它们的根——
arrest→sta（43 员）、amplify/benefit→fac（32 员）、allowance→loc、actress→ag、
appliance→plic、audio→audire、available→valere、agreeable→grat。

根因：判据问的是「该词元族在**未入库**考研词里够不够 3 个」，真正该问的是
**「库中是否已有能收它的根」**。派发这类清单时必须在指令里写明「档位只表示
匹配器没找到根，不等于该写成孤立词条，你自己再查一遍库」。

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

**同一签名还会打到主对话自己**：本会话有一段时间我的工具调用全部返回空
（Bash / Read / Grep / Glob 都是，绕过 sandbox 也一样），与派子代理同时发生，
两个代理的 transcript 是 0 字节。**症状是空结果不是报错**——工具不存在会报
「未知工具」，被 deny/hook 拦会回一段拦截说明，空返回是上游的事。
遇到这种：**别反复重试**，也**绝不能把「代理可能会返回什么」当成已收到的回报
写出来**（我犯过，把没收到的结论写进了回复）。等回报或验文件时间戳。

### 8. 自己新写的门也会有静默失效

`cut_next_chunks.py` 刚写好那一版，A 档的「疑 → X」直接用了 Wiktionary 词元
映射的结果，**没校验 X 是不是 roots.json 里真实存在的根**。于是 chunk107 整片
10 个 A 档词指向的全是库里没有的根（imitari / migrare / stallum / vitare…），
代理花整轮去核 10 个不存在的归属。`rids` 当时已经加载好、就是没用上。

这与本文件上面那六处缺陷是同一类。**新加的判据自己也要过一遍阳性对照**：
拿已知答案的输入喂进去，看它报不报、报得对不对。改门二那次做了两组对照
（剥掉 root_ids 的真信号必须仍报出、已挂对根的补词行不该报），才敢说
「伪报 22 → 2」而不是「把门弄哑了」。

## 附：这轮的数据来源

词根归属线索取自 [eslsoft/engra](https://github.com/eslsoft/engra)（MIT，2191 个词根，
覆盖 5299 考研词表的 73.1%）。**只取「词→根」这个事实，未取其 mnemonic 文本**——
仓库虽 MIT 但内容疑似源自出版物。

Wiktionary 缓存 2265 个 wikitext 在 `drafts/.etym_cache/`（gitignored，重跑不请求
网络）。测量脚本 `scripts/probe_etymology_coverage.py`：拿库里已挂根的词当标注集，
top1 与库一致 82.6%，有词元的词里 92.9%，判错仅 0.6%，其余是合并/拆分根造成的
多候选歧义——**那类歧义恰恰是你自己的教学决策，机器替不了**。
