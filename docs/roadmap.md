# 开发路线（Roadmap）

> 更新：2026-08-19

---

## 总路线

```
v0.1    数据模型 + 10 核心词根 + D3 交互图谱   ✅ 已完成
v0.1.1  图谱可用性升级（搜索 + 分层钻取 + 近义词组合）✅ 已完成
v0.1.2  移动端响应式改造（手机/平板适配）  ✅ 已完成
v0.2.0  纸张词源地图改版 + 昼夜模式 + 视觉质量门  ✅ 已完成
v0.3    AI 自动生成词条 + 人工审核        ✅ 已完成（提前）
v0.2    100 词实验集                      ✅ 已完成
v0.4    语义域分层 + 词表可拆性分析      ✅ 已完成
v1.0    考研词表中可结构化的部分（441/869 词，51%）← 当前
```

---

## v0.1 — 地基（已完成 ✅）

- [x] GitHub 仓库 `english-semantic-graph`
- [x] 项目宪章（目标明确）
- [x] 数据模型 schema（design.md）
- [x] 10 个核心词根数据入库（54 词 + 70 关系 + 54 例句）
- [x] D3 交互图谱（frontend/）
- [x] 数据校验脚本（tests/validate.py，含质量门 Q1-Q6）
- [x] 语义扩展补全 + 词源修正（质量红线落地）

---

## v0.1.1 — 图谱可用性升级（已完成 ✅）

> 详见 [plan-ux-graph.md](plan-ux-graph.md)

- [x] 搜索框：单词/词根/中文三路搜索，定位高亮 + 弹详情
- [x] 图谱分层钻取：默认只显词根+概念，点击展开词族
- [x] 近义词概念中转：concepts.json 增加 `type: cluster` 聚合概念
- [x] words.json 增加 `synonym_group` / `synonym_note`
- [x] 试点 2 组近义词（make a choice / make clear）+ 4 新词（库 54 词）
- [x] 详情面板显示「近义词组 + 语境差异」
- [x] validate.py 校验 synonym_group 引用

---

## v0.1.2 — 移动端响应式改造（当前阶段 · 已确认方案）

> 详见 [plan-mobile.md](plan-mobile.md)

- [x] CSS：768px 断点 + 上下布局 + 底部详情抽屉（含动画）
- [x] JS：详情面板抽屉化（class 切换 + 关闭按钮）、touch 手势适配
- [x] 手机端图例/提示折叠
- [x] 小屏节点/字号/连线密度微调
- [x] 推送部署 + 线上验证（桌面 + 手机 UA）
- [x] 数据质量门 Q7/Q8：related 死链 + 近反义词造词拦截

**验收**：375px 宽度下搜索置顶、图谱可双指缩放单指拖动、点击节点底部抽屉出详情；桌面端不变。

## v0.3 — AI 生成管线（已完成 ✅）

> 调整顺序：原计划先手写满 100 词（v0.2）再做管线。
> 但"一个概念解释整个词族"在 10 个词根 × 5 词时已得到验证，
> 再手写 46 词验证的是同一件事；而 v1.0 的 5500 词只可能靠管线。
> 故先建管线，再用它扩词——避免手写内容之后又要用管线重跑一遍。

- [x] `ai_pipeline/prompt_builder.py`：从现有词条抽 few-shot + schema 约束
- [x] `ai_pipeline/word_analyzer.py`：调模型生成候选（OpenAI 兼容端点可插拔）
- [x] `ai_pipeline/review.py`：结构检查 → 人工确认 → 合并入库
- [x] 首批 10 词通过管线入库（54 → 64 词）
- [x] 质量门 Q9：概念反向引用完整性

**管线用法**：

```bash
# 1. 生成候选（未配 API 时导出提示词，贴给任意对话模型）
python ai_pipeline/word_analyzer.py depress:press impose:pose -o candidates.json

# 2. 检查（结构错误必须修；外部词需人工确认后加入 lexicon.json）
python ai_pipeline/review.py check candidates.json

# 3. 合并（合并前后各跑一次 validate.py，不过则拒绝落库）
python ai_pipeline/review.py merge candidates.json
```

---

## v0.2 — 100 词实验集（已完成 ✅）

- [x] 100 词入库（每根 9-11 词，figur 6 词——该词族在英语中本就较小）
- [x] 分三批经管线生成 + 审核 + 合并（64 → 76 → 88 → 100）
- [x] 密度压力测试：全展开 112 节点无重叠
- [x] 节点尺寸随画布缩放；手机端一次只展开一个词根
- [x] 视觉质量门新增密度检查
- [ ] Obsidian Vault 生成器（data → .md）
- [x] 学习模式验证：回想 + 词族（`frontend/study.js`）
      - 回想：只给核心画面 + 词根推导，遮住单词与中文，检验画面记忆是否成立
      - 词族：给词根与核心概念，列出全族推导，检验"一个概念解释整族"
      - 遮罩是动态的：拉丁词源（respectus / importare）含英语词形，
        画面里也可能出现中文义项，两者都会泄题，故在渲染时遮而非改数据
      - 视觉审计新增答案泄露检查——遮罩回退时人工逐题核对不现实，机器可以
- [x] 按学习模式暴露的问题回填 schema（趁 138 词时改，比 1000 词时便宜七倍）
      - 新增 `recall_hint`：27 个词条，专为回想模式写的推导，不点名中文义项
      - 改写 20 个 `core_image`：不再点名自己的中文义项（如 spectator 的"观众"）
      - 2 个裸词根推导补明"本身即词根，无词缀"（figure / state）
      - 质量门 Q12 守住这两点，已验证能拦回归
      - 复习排期**不进数据文件**：那是用户状态而非词条属性，应放 localStorage

**验证结论**：词量从 54 涨到 100 后，桌面端全展开 112 个节点仍无重叠；
手机端 390px 画布原本会出现 98 对节点重叠，改为"一次展开一个词根"
加上节点尺寸随画布缩放后降为 0。密度上限已知：小屏靠限制同时展开量来解决。

---

## v0.4 — 语义域分层（已完成 ✅）

三级钻取：语义域 → 词根 → 单词。默认层节点数由语义域数量决定，不随词量增长。

- [x] `data/domains.json`：语义域层，10 词根归入 4 域
- [x] 图谱三级钻取；搜索可穿透三层直达单词
- [x] 质量门 Q10：语义域必须恰好覆盖每个词根一次
- [x] `ai_pipeline/density_probe.py`：合成数据实测各规模密度
- [x] 力导向只模拟可见节点（隐藏节点会从背后挤开可见节点）
- [x] 连线距离不得小于两端碰撞半径之和（否则两力矛盾）
- [x] 展开时松开可见节点（钉死状态下碰撞永远解不开）

**实测密度**（1440×790，各层均 0 重叠）：

```
  词数   词根 | 默认层 重叠 | 展开一域 重叠 | 再展一族 重叠
   100    10 |     10   0 |      12   0 |      22   0
   500    50 |     16   0 |      24   0 |      34   0
  1200   120 |     16   0 |      32   0 |      42   0
  2500   250 |     16   0 |      48   0 |      58   0
  5500   550 |     16   0 |      86   0 |      96   0
```

分层前对比：500 词已出现重叠，1000 词 129 对，5500 词 258990 对。

---

## v1.0 — 考研词表中可结构化的部分

> **范围调整**：不是所有词都能拆成词根。对 5299 个考研词条做数据驱动分析
> （从词表自身发现词族，词干至少被 3 个词共享才算真词根）：
>
> | 类别 | 数量 | 占比 |
> |---|---|---|
> | 孤立词，拆了也无同族词可迁移 | 3682 | 69.5% |
> | **可拆（词缀 + 有词族的词根）** | **1081** | **20.4%** |
> | 日耳曼核心词，本身即词根 | 219 | 4.1% |
> | 词族基词 | 125 | 2.4% |
> | 功能词 | 117 | 2.2% |
> | 借词/专名 | 33 | 0.6% |
>
> 适用本方法约 1206 词（22.8%），且这是**上限**：自动匹配靠拼写，
> 会把同形异源的词根混成一族（抽查 6 个高产词族，混入率 16%，
> 如 leg 把 legere/读 与 lex/法 与 leg/肢 混在一起）。
> 人工审词源后预计 800–1000 词。

- [x] 291 个自动发现的词族逐个审词源（判断记录在 `ai_pipeline/etymology_verdicts*.json`）
      - 整族作废 56 个（拼写巧合，如 `adv` 底下混了 venire/ante/visum 三个词根）
      - 拆族 33 个（如 `leg` 拆成 legere 读 / lex 法 / lig 绑缚）
      - 合并 6 个（同一词根被拼写变体拆开，如 duc 与 duce）
      - 剔除混入词 44 个（如 sister 混进 stare 族、mineral 混进 minus 族）
      - **产出 203 族 / 869 词次**，见 `ai_pipeline/vetted_families.json`
      - 另 61 族清理后仅剩 2 词被降级，其词根本身高产（如 spirare、tangere），
        只是考研范围内成员少；含这些则为 264 族 / 970 词次
      - ⚠️ 此数为**下限**：对已知高产词根抽样校准，约 35% 的成员被词干提取
        误判为"孤立词"（如 capere 的 capable/capacity/capture）
- [x] 词条加 `decomposable` 字段（root / root_pending / germanic / loanword / phrasal / opaque）
- [x] 质量门 Q11：拒绝给不可拆的词硬编词根，拒绝含"词源不同"等对冲措辞的推导
- [x] 生成管线同步该约束；详情栏对不可拆的词如实说明原因
- [x] 回填现有 100 词：root=96 germanic=2 root_pending=2
- [ ] 可结构化词批量入库（~1000 词）
  - [x] 第一批新词根：sta（立）/ tain（握）/ clud（关），新语义域「持存与围合」
        118 词 · 13 词根 · 5 语义域
  - [x] `state` 从 root_pending 转正（sta 词根已建模）
  - [x] `seclude` 归入正确的 clud 词根——此前因被硬挂到 duc 下而撤除
  - [x] 第二批：fac（facere 做/造），新语义域「行为与造作」
        126 词 · 14 词根 · 6 语义域。affect/effect 的区别在词条里讲清了
  - [x] 管线改进（做过三批后发现的重复劳动）：
        批次文件可内联声明新词根/概念/语义域，与词条原子落地——
        此前每次新建词根都要手写临时脚本，且会制造"空词根导致校验不过"的中间态；
        新增 `data/english_reference.json`（考研词表 5299 词形）作自动核验源，
        近/反义词若在表中即自动通过，每批人工确认项从 ~20 降到 ~7
  - [x] 第三批：tend（伸展，归入「施力」）+ ced（行进，归入「位移与传递」）
        138 词 · 16 词根。extensive/intensive 这对反义靠同词根反方向讲清
  - [x] 第四批：jac（投掷，归「位移与传递」）+ pend（悬挂/称量，归「持存与围合」）
        153 词 · 18 词根。object/subject/objective/subjective 四词靠 ob-/sub- 的
        方位对立一次讲清；expend/expensive 保留了"付钱要称银子"的词源画面
  - [x] 第五批：pars（部分）+ fin（界限），均归「形态与安放」
        167 词 · 20 词根。finite/infinite 只差一个否定前缀，是词根法最见效的一类
  - [x] 审核门新增 id 冲突检查：词根与词条共用命名空间，同名会产生自环边
        （词根 part 与单词 part 撞车，词根改用拉丁词形 pars）
  - [x] 第六批：ag（agere 驱动，词根名避开同名单词 act）+ stru（堆叠建造）
        181 词 · 22 词根。「行为与造作」域从 1 根扩到 3 根；
        construct/destructive 靠 con-/de- 前缀对立成对
  - [x] 第七批：dict（说）+ sci（知）+ crit（判别），均归「感知与记录」
        196 词 · 25 词根。该域从 2 根扩到 5 根：看、写、说、知、判
  - [x] 第八批：signum（记号）+ quir（寻求）+ rect（导正）
        214 词 · 28 词根。sign/design/assign/resign/designate 五词共享"记号"
  - [x] 第九批：mov（移动）+ vert（转）+ pel（推），229 词 · 31 词根
        repel 与 attract 构成"推回/拉来"一对；compel/compulsory 同族异形
  - [x] 第十批：serv（守住）+ cov（盖住）+ flu（流动），244 词 · 34 词根
        cover/discover/uncover/recover 四词只靠前缀分工；
        affluent（流向此处）与 superfluous（漫过边沿）同根反义
  - [x] 第十一批：gen（生出）+ plic（折叠）+ loc（地点），259 词 · 37 词根
        plic 一族全靠"往哪折"分工：贴上去(apply)、叠一起(complicate)、
        折进里面(implication)——中文"申请/复杂/含意"看不出任何关联
  - [x] 第十二批：sequ（跟随）+ pet（追求）+ texere（编织），274 词 · 40 词根
        texere 一族把"编织"贯到底：text 是织成的整片，context 是与它同织的周围，
        pretext 是织在前面挡住真相的那道帘子；词根 id 再次因与单词同名而改拉丁词形
  - [x] 第十三批：curr（跑/流）+ prob（检验）+ minus（更小），290 词 · 43 词根
        occur/recur/incur/excursion 全靠前缀定"往哪跑"；
        minister 的本义是"居下承事的人"，这解释了它与 minor/diminish 同族
  - [x] 节点尺寸改为随"可见节点密度"动态缩放：
        原先只按画布面积算，词库长大后全部展开会挤（335 节点时 2 对重叠）；
        现在展开层级时重算半径、碰撞、边界与连线距离，381 节点仍 0 重叠
  - [x] 第十四批：posse（能够）+ publicus（属于众人）+ res（实在之物）
        305 词 · 46 词根。republic 拆出 res publica"众人之公事"，
        一次讲清它与 public / real 两族的血缘
  - [x] 第十五批：classis（等级）+ plere（填满）+ organon（部件）
        320 词 · 49 词根。organ 一词三义（器官/机关/风琴）共享"各司其职的部件"；
        complement（补齐缺口）与 supplement（额外外加）的差别靠前缀讲清
  - [x] 第十六批：补全已建模词根的成员（不新增词根），340 词
        ponere 族补到 16 词、spect 族补到 19 词；
        词根 pose 改名 ponere（与单词 pose 撞名，且统一为拉丁词形）
  - [x] 修回想模式泄题：词根名未过遮罩，而 signum/publicus/classis/organon
        分别包含 sign/public/class/organ，等于把答案印在题面上
  - [x] 审计改为全库确定性扫描，并改用 study.js 暴露的 recallPrompt 钩子：
        原先抽样 25 题只有约 7% 命中率；且测试自带一份遮罩实现，
        把渲染改坏也照样通过——两个缺陷都已修正
  - [x] 第十七批：aequus（相等）+ claimare（喊出）+ liber（自由），356 词 · 52 词根
        deliberate 归入 liber 时标明取 libra（天平）义——"称量过才做"
        才解释得通"故意的"与"从容的"两义；clud 族补 close/disclose/enclose
  - [x] 第十八批：sumere（取用）+ spirare（呼吸）+ socius（同伴），374 词 · 55 词根
        conspiracy 的本义是"几人凑一起同呼吸"，这才连得上 inspire；
        capere 支补 concept/except/receipt/accept/susceptible 五词
  - [x] 第十九批：certus（已定）+ norma（角尺）+ testis（见证）+ mun（共有）
        390 词 · 59 词根。norma 本义是木匠的角尺，normal/abnormal 就是
        "拿尺一比合不合得上"；test 源自试炼金属的陶钵，故与 testify 同族
  - [x] 第二十批：gradus（步/级）+ fundere（倒出）+ optare（选择）+ civis（市民）
        406 词 · 63 词根。refuse 本义"把递来的倒回去"，与 confuse/diffuse 同根；
        optional 与 compulsory 构成"由你挑/推着你做"一对
  - [x] 手机端语义域也改为一次只展开一个：词根数到 63 后全展开会让
        390px 画布同时出现 138 节点，已到重叠临界（时通时不通）。
        与词根层"一次一族"一致，现在手机端全展开只 36 节点，三次复跑稳定
  - [x] 第二十一批：spondere（应许）+ ternus（内外）+ apparere（显现）+ nasci（出生）
        426 词 · 67 词根。responsible 的本义是"出了事须由你作答"；
        nation/native/nature 同出 nasci，"天性"与"自然"都是"生来如此"
  - [x] 第二十二批：centrum（圆心）+ identus（同一）+ durare（持续）+ domus（家）
        441 词 · 71 词根，过半。concentrate 是"全聚到一个中心"，
        domestic/dominate 同出 domus——门内那一摊与当家的人
  - [x] 缩放下限从 0.5 放宽到 0.28：541 节点时按密度需 0.478，
        卡在 0.5 几何上放不下。图谱可缩放 5 倍，此时它是"全局俯视图"
  - [x] 审计改为等力导向收敛再测：541 节点 4 秒还剩十几对重叠，8 秒后归零，
        固定等待导致同一份代码跑出 38 / 11 / 0 三种结果
  - [ ] 剩余高价值词族（>=5 词，共 141 词）优先，之后是
        47 个四词族（188 词）与 107 个三词族（321 词）
- [ ] 学习模式：探索 / 复习 / 测试
- [ ] 部署为可访问的 Web 页面

---

## 核心词根清单（v0.1 首批 10 个）

```
figur       形状        → figure, configure, figurative, disfigure
press       压          → pressure, impress, express, suppress, compress
form        形状/形成   → form, formal, inform, transform, perform
tract       拉/拖      → attract, extract, contract, distract, tractor
pose        放置       → position, compose, expose, propose, oppose
mit/miss    送         → admit, commit, permit, transmit, mission
spect       看         → inspect, respect, prospect, spectator
scrib/script 写        → describe, prescribe, transcript, manuscript
duc/duct    引导       → conduct, produce, introduce, educate, reduce
port        运送       → import, export, transport, portable, report
```

> 这 10 个词根覆盖数百个考研词，是验证模型的最小集。