# 下一轮做什么

> 现状更新于 2026-08-31。分支 `fix/etymology-gates-and-engra-gaps`，PR #1 仍未合。
> 先读 [HANDOFF.md](HANDOFF.md) 的「先读这一条」，再读本文件末尾「这轮踩实的坑」。

## 现状（现场数的）

```
5248 词条 / 309 根 / 311 概念 / 2168 关系 / 10536 例句
  ├─ 4114 可用
  └─ 1134 占位（stub: true）

考研词表 5299 词形
  名义覆盖 5219  98.5%      ← 别只报这个
  真实覆盖 4085  77.1%      ← 剔掉占位词条
  可结构化 4075  78.2%      ← 再剔掉 a/he/it/and 这类功能词
  无条目     80             按项目规则本就不建条
```

**这三个数不要手算，跑脚本**，它同时报三个口径并列出占位词条的字段缺口：

```bash
python scripts/mark_stubs.py          # 只报
python scripts/audit_all.py           # summary.json 也带 usable / stubs
```

已用 chunk 编号 130 个，最大 149。

## 第一步：补占位词条的内容字段（当前主线）

2026-08-28 有一次批量生成，用 `build_g_chunk*.py` 把考研词表尾段（s/t/w/y/z 段为主）
灌成了 1134 条占位词条，只有结构合法。**覆盖率 98.5% 里有 21.4 个百分点是这批。**
音标、词性已在 08-31 离线补完，剩下的必须逐词写：

| 字段 | 待补 | 说明 |
|---|---|---|
| native_definition | 1134 | 全是 `a thing or action related to X` |
| core_concept | 1134 | 全是 `a clear scene connected with X` |
| examples | 1134 | 全是 `The X changed the situation.` |
| semantic_expansions | 1134 | 全是「从核心场景引出的常用义」 |
| chinese | 901 | 生成器 `zh.get(w,w)` 回退成英文词本身 |
| phonetic | 91 | 机器能补的已补完，剩下的见第二步 |
| core_image | 89 | overall→plaster 段，从未派过 |

清单直接取 `audit/stubs.tsv`（跑一次 `audit_all.py` 生成），或
`python -c "import json;print('\n'.join(w['id'] for w in json.load(open('data/words.json',encoding='utf-8'))['words'] if w.get('stub')))"`。

这批好在几乎全是日耳曼型（1133/1134），**不用判词根归属**，比前面 4000 词那轮轻。
按 30 词/片、2 路并发算约 38 批。派发指令见下面「派发指令必须带的话」，但词根归属
那几条可以省掉。

**别用生成器批量填**——这一轮的问题就是这么来的。见「这轮踩实的坑」第一条。

## 第二步：音标已做完，剩 91 条要人工

08-31 已补抓 283 个缺失缓存（`scripts/fetch_stub_wikitext.py`）并二次写回，
假音标 1109 → 91。**剩下的 91 条别再喂脚本**，它们是两道门有意挡下的：

| 原因 | 条数 | 为什么不能自动写 |
|---|---|---|
| 同形异读 | 35 | 多个 Pronunciation 段，取首个会取错词源支 |
| 重音歧义 | 35 | 名动异重，取错支等于把重音教反 |
| 无 IPA | 11 | Wiktionary 该词条没给音标 |
| 窄式记音 | 7 | 只有方言变体（`ɚ ɝ ʉ ɐ` 那类），折成英式等于伪造 |
| 无 English 段 | 2 | `september` / `thursday`，Wiktionary 收的是首字母大写形 |

清单跑 `python scripts/extract_phonetic_pos.py`（不加 `--apply`），
看 `drafts/phonetic_pos.tsv` 的 `note` 列。重音歧义那 35 条的 note 里带
`重音歧义(候选之一 …)`，人只需判该取哪一支。

## 第三步：collocations 的尾巴

现有 328 条带 collocations（306 条在可用词条上）。老文档列的两类都已做完，
**真正剩下的**：

- `whereby` `nonetheless` `albeit` **三个词不在库**，且都在考研词表里。
  用法坑比缺搭配更值得做：`whereby` ＝ by which，前面必须有名词；
  `albeit` 不接完整句（albeit brief ✓ / albeit it was brief ✗）。先补词条再谈搭配。
- `thereby` 在库但是占位词条，会被第一步一起处理。它接 **-ing** 不接从句。
- 另有一批副词/代词类无搭配，多数是反身代词与纯方位副词（`herself`/`everywhere`/
  `downstairs`），**没有值得教的型式**，不必强凑。按「这个词有没有站得住的型式」判，
  别按词性一刀切。

回填走 `scripts/backfill_collocations.py`（两列 TSV），**不要走
`entries_from_draft.py`**——那条管道是给新词条用的，遇到已入库的词会拒绝，
且会重写其余 14 列。

## 第四步：近反义词（用户明确要求放最后）

可用词条里 1227 条有 synonyms、663 条有 antonyms，占位词条 0 条。
**不要按批零敲**——该做一次统一的全库扫描，否则同一组近义词分散在不同批次里，
写出来的 `synonym_note` 彼此矛盾。

注意 Q8 白名单机制：`validate.py` 有一份已核验白名单（`data/lexicon.json`，
1819 词），新加的近反义词若不在白名单里会被挡。先读 `scripts/check_lexicon_gap.py`
弄清登记流程。

## 派发指令必须带的话

每批派发前都在重建这份清单，直接抄。缺任何一条都在实测里出过错。补占位词条内容的
那批（第一步）不涉及词根归属，档位与近形异源两节可以省。

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

**两片可能撞车时要说明**：同一族的词分到两片要写明「只写你片里的，若判断该建根就
回报由我统一建」，否则两片各建一次就是重复根。

**回报格式**：400 字以内，只报统计 + A 档核不成立的 + B/C 档自己查出能挂根的
（最有价值）+ 门二逐条判定 + 够 3 员但本片建不了的新根候选 + 库内既有问题
（只报不改）。别贴 TSV 内容。

## 顺带可做

- `admire` 可凑 `mirari` 族（`miracle`/`mirror` 已入库，三个都还是 germanic 型）、
  `cage`/`cave` 可凑 `cavea` 族。两族都因「凑不到 3 个成员」被写成日耳曼型，
  现在够数了，但要回改已入库条目。
- `amount` 的 origin 写着「拉丁语 ad montem」却以 germanic 入库。
- **1123 条非占位词条的 `decomposable_note` 用默认文案**（另有 1123 条在占位词条上，
  会随第一步处理）。需逐条查证才能分流，origin 有明确线索的 578 条上一轮已改。
- `validate.py` 的 Q2 警告 7 条 `root_logic` 含「就是」式简单推导，待人工复核：
  `nature` `cattle` `comprise` `content` `type` `engineer` `genuine`。
- 老文档说 `alternate` 错挂 `ternus`——**已不成立**，现在挂的是 `alter-other`，正确。

## 别做

- 别用生成器批量填内容字段（这一轮的 1134 条占位词条就是这么来的）
- 别手写 `build_batchNN.py`（1141 字节/词 vs 走 TSV 的 19）
- 别整读 `data/words.json`（6.0 MB），用 `python -c` 取字段
- 别自动归族（拼写聚类判不出词族，已踩过多次）
- 别在代理还在写的时候读它的文件（会读到半成品快照）
- 别按池子文件的**行数**当待办数——文件里混着已入库的词，要 `not in ids` 过一遍
- **别只看 `git status` 判断某批做过没有**——`drafts/` 在 .gitignore 里，git 查不到
  痕迹。曾因此重派一整轮 6 个代理做已完成的活。**看文件时间戳。**

## 这轮踩实的坑

### 1. 批量生成器把覆盖率虚推了 21 个百分点

08-28 为补完考研词表，主对话自己写了 `build_g_chunk*.py`（不经子代理）灌进 1193 条
空壳。`validate.py` 全绿、`critical` 为 0、覆盖率报 98.5%，**真实可用只有 77.1%**。
核心几行：

```python
image='一张卡片放在桌面中央，旁边摆着几件相关物品，窗光从左侧照来'   # 固定串
native=f'a thing or action related to {w}'                        # 模板
ex=f'The {w} changed the situation.|Researchers discussed the {w} carefully.'
z=zh.get(w,w)                          # ← 查不到就拿英文词当中文释义，901 条
rows.append(['W',w,p,'/ˈ'+w+'/', ...]) # ← 音标 = 拼写套斜杠，1109 条
```

后续 15 个「重写模板化核心画面」提交只修了 `core_image` 一个字段，其余五项原样留着，
所以那批提交看着做了很多、实际只动了七分之一。

**教训不是「别用生成器」而是「静默回退必须报警」**——`zh.get(w,w)` 那种默认值回退
不留任何痕迹，是最难发现的一类。

### 2. 审计自己也会瞎

`audit_all.py` 的 `TEMPLATE_IMAGE` 常量停在第一代生成器的画面串上，第二代换了串之后
那 89 条模板画面**一条没报出来**，是靠字段无关的重复值检查才露出来的。已改成元组容纳
两代，并补了假音标、中文=英文、模板语义展开三条判据。

风险排序当时对全库无条件静态加权（有词根 +1、多义 +1），**3516 条报警栏全空**，
5174/5248 词都算「有风险」，榜单等于把库抄一遍。已改成加权只在有报警的词之间分次序，
占位词条另出 `stubs.tsv`。`risk_words` 5174 → 344。

**新加的判据自己也要过阳性对照**：拿已知答案喂进去，看报不报、报得对不对。
这一条与上一版坑八（`cut_next_chunks.py` 的 A 档不校验根是否存在）是同一类。

### 3. 音标抽取的四道门都是踩出来的

`extract_phonetic_pos.py` 从 `drafts/.etym_cache/` 抽 IPA，每道门都对应一次实测失败：

- **无标注 IPA 必须排在显式 UK 之后**。Wiktionary 顶端那条不带 `a=` 的往往是美式：
  `only` 首条是 `/ˈoʊn.li/`，英式 `/ˈəʊn.li/` 反而嵌在 `a=UK` 里。
- **窄式记音先剥组合变音符再校验字符集**。直接拒收会挡掉正确项而放行错误项——
  `out` 的 RP 是 `/ˈäʊ̯t/` 被挡后，唯一通过字符集的是 `a=Pittsburgh` 的 `/ˈaːt/`。
  `ɹ→r`、`ɛ→e`、`əː→ə` 是记法差异可折算；`ɚ ɝ ʉ ɐ ʈ ɻ ʍ` 是真方言标记，整条拒收。
- **重音歧义不写**（22 条）。名动异重词取错支等于把重音教反：`compress` 库内是动词
  `/kəmˈpres/`，Wiktionary 首条是名词 `/ˈkɒmpres/`。判据**数音节不数音段**，否则
  `ourselves` 的 `/aʊəˈselvz/` 与 `/ɑːˈselvz/` 会误判成歧义（只是 our 的拼法不同）。
- **同形异读不写**（27 条）。多个 Pronunciation 段说明各词源支读音不同：`paste` 会抽成
  `/ˈpæsteɪ/`（英语是 `/peɪst/`）、`spread` 抽成 `/spriːd/`、`shower` 抽到「展示者」。

### 4. 库内音标本身是混合口径，别拿它当唯一判准

`probe_phonetic_accuracy.py` 拿库内 2410 条已知音标反查抽取器：完全一致 40.7%、
记法差异内一致 22.8%、口径差异内一致 15.9%、重音位置不同 0.5%、其余 20.1%。

**「与库内不一致」不等于抽错**——库自己就不自洽：儿化 309 条对非儿化 295 条，
`oʊ` 30 条对 `əʊ` 223 条，且**按词族成簇**（`compose`/`expose`/`propose`/`oppose`
整族用美式 `oʊ`）。不同批次用了不同口径。20.1% 残差主要是弱元音 ə/ɪ 交替与 yod
有无这类合法变体。

新写的音标一律按英式 RP（`/lɒt/` `/ˈdɒktə/` `/bɜːd/` 那一路），但**别去统一存量**，
那是另一个决定，得先问用户。

### 5. 词性不能照抄 Wiktionary 的首个标题

Wiktionary 按词源顺序排词性不按频次，且会把边缘义项也立成标题：
`occasion` 的 Verb 是「to cause」这种古旧用法、`optical` 的 Noun 带 `{{lb|en|film}}`
是电影业行话、`outing` 的 Verb 其实是 `{{infl of|en|out}}` 屈折形式不是独立词性。
全收进来是在制造错误。

现在只改生成器的默认值 `noun`，原值是别的词性就保留（30 条）——那些是 build 脚本
手写的三组硬编码集合，按主用法选过，比抽取可靠。`overlook`/`overflow` 若照抄
Wiktionary 会被改成 noun，而动词才是主用法。

### 6. 改多处同步的字段要数清有几处

改词根 id 要同步**五处**：`roots.id`、`words.root_ids`、`concepts.root_ids`、
`relations.from/to`、**`domains.root_ids`**。漏第五处时 `validate.py` 报
「domain-shape.root_ids 引用不存在的词根」+ Q10。见 `scripts/rename_root_id.py`。

日耳曼型词条的字段名是 **`decomposable`** 不是 `type`，且 `root_logic` 是必填的
**空串**而非删除。写错会报「缺少必填字段」+ Q11。

`stub` 是独立字段，不要塞进 `decomposable`——占位与可拆性是正交的两个维度，
一个占位词条同样可以是 germanic 或 root 型（`stall` 就是唯一那个 root 型占位词条）。

### 7. 出错就回退到基线重跑，别在改坏的状态上叠加

`data/` 每次改动前先确认 `git status --short data/` 是干净的，出错 `git checkout --
data/` 回基线后用改正版重跑。

### 8. 中转站并发上限

6 路并行会把中转站打爆（HTTP 200 空响应），5 个代理同批阵亡。**最多 2 路。**
另外有一次代理写完文件但回报没送达——文件落盘近两小时后才发现。若文件已停止
写入且内容完整，可直接验文件，不必等回报。

**同一签名还会打到主对话自己**：曾有一段时间工具调用全部返回空（Bash / Read /
Grep / Glob 都是，绕过 sandbox 也一样），与派子代理同时发生。**症状是空结果不是
报错**——工具不存在会报「未知工具」，被 deny/hook 拦会回一段拦截说明，空返回是
上游的事。遇到这种：**别反复重试**，也**绝不能把「代理可能会返回什么」当成已收到
的回报写出来**（犯过两次：一次把没收到的子代理结论写进回复，一次把根本没做的
编辑写成做过并编出了 NameError 与「权限墙」）。等回报或验文件时间戳。

## 附：数据来源

词根归属线索取自 [eslsoft/engra](https://github.com/eslsoft/engra)（MIT，2191 个词根，
覆盖 5299 考研词表的 73.1%）。**只取「词→根」这个事实，未取其 mnemonic 文本**——
仓库虽 MIT 但内容疑似源自出版物。

Wiktionary 缓存 3880 个 wikitext 在 `drafts/.etym_cache/`（gitignored，重跑不请求
网络）。缺词补抓走 `scripts/fetch_stub_wikitext.py`。测量脚本 `scripts/probe_etymology_coverage.py`：拿库里已挂根的词当标注集，
top1 与库一致 82.6%，有词元的词里 92.9%，判错仅 0.6%，其余是合并/拆分根造成的
多候选歧义——**那类歧义恰恰是你自己的教学决策，机器替不了**。
