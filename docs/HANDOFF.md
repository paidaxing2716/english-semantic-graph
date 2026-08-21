# 交接文档 — English Semantic Graph 剩余任务

> 生成：2026-08-21（已按远端 721 词口径重算）
> 状态：**由新对话继续推进**（本会话结束）
> 上次状态：词库 **721 词 / 129 词根**，vetted_families 869 词次中 **剩 227 个独立词**待入库

---

## TL;DR

- 目标：把 `ai_pipeline/vetted_families.json`（203 族 / 869 词次）**剩余 227 个独立词**全部按管线推进入库，直到 869 词次/203 族收齐。
- 剩余工作分三类：
  1. **吸收到已建模词根**（25 词 / 17 族）——直接把 vetted 成员补进现有 root_ids
  2. **新品根族新建**（~202 词 / 67 族）——每族新建拉丁词根 + 概念 + 域，与词条原子落地
  3. **审核拆分族**（混在 2 中，~11 族必须先拆）——严禁整族并成一个根
- **不允许硬凑**：词根 id 撞同名单词 → 用拉丁词形；词源混合族 → 拆；无把握不开词根。
- 管线：`build_batchNN.py` → `review.py check` → 注册外部词 → `review.py merge` → `tests/validate.py` → `visual_audit.py` → 更新 roadmap → commit/push。
- 另记录一处**既有词源错配**（fac 根下挂了 5 个 capere 词），建 cep 族时一并修。

---

## 一、权威源与在库口径

| 数据 | 路径 | 说明 |
|---|---|---|
| 权威族清单 | `ai_pipeline/vetted_families.json` | 203 族 / 869 词次；本交接唯一取词来源 |
| 在库词库 | `data/words.json` | **721 词**（第三十六/三十七批已入库 27 词）|
| 已建模词根 | `data/roots.json` | **129 根** |
| 语义域 | `data/domains.json` | 6 域 |
| 外部词白名单 | `data/lexicon.json` | 不在考研词表也放行的词 |
| 自动核验源 | `data/english_reference.json` | 5299 词形，近/反义词在表中即自动通过 |

**口径**：余量 = vetted_families 中不在 words.json 的**独立词** = **227**。已核实 227 个独立词不跨族重复。

---

## 二、剩余工作全量清单（227 词）

### A. 吸收到已建模词根（25 词 / 17 族）✅ 无风险，可优先做

这些族的**部分成员已入库并已挂到某个已建模词根**，剩余成员直接补进同 root_ids 即可，无需新建词根、无需再开 domain。

| vetted 族 | 已入库 anchor 词根 | 待补成员 |
|---|---|---|
| accept | fac | acceptable, acceptance |
| domin | domus | predominant |
| flu | flu | flu |
| form | form | form, former, performance |
| pect | spect | expectation |
| port | port | importance, port, porter |
| prec | ced / pretium ⚠️ | preceding, precise |
| pref | ferre | preferable |
| pres::premere | press | press |
| ref | ferre / fin ⚠️ | reference |
| respond | spondere | corresponding |
| scrib | scrib-script | script |
| sta | sta | stationery, statistical, stay |
| sult::salire | salire | resultant |
| tain | tain | attain |
| trah | tract | attractive |
| vid | spect | envisage |

> `prec`、`ref` 两族锚点有两个词根，说明 vetted 族本身可能混两条源，先拆清再吸收。

### B. 新品根族新建（202 词 / 67 族）——主要工作量

每族 = 新建拉丁词根（进 roots.json）+ 新概念（concepts.json）+ 归 6 域之一 + 词条原子落地。以下 vetted 族名即候选词根 id，**用拉丁词形避开与英文同名单词撞 id**（自环边检查）。

| vetted 族 | 词 | vetted 族 | 词 |
|---|---|---|---|
| accord | accord, accordance, accordingly | mus | music, musical, musician |
| art::ars | art, artist, artistic | num | innumerable, numerical, numerous |
| cad | incidence, incident, incidentally | olog | apologise, apology, biology |
| cep | exception, exceptional, reception | ord | disorder, order, orderly |
| cern | concern, concerning, discern | origin | origin, original, originate |
| comp | comparable, compile, comply ⚠️ | pact | compact, impact, pact |
| conc | concession, concise, reconcile ⚠️ | paint | paint, painter, painting |
| custom | custom, customary, customer | pair | impair, pair, repair ⚠️ |
| cycl | bicycle, cycle, recycle | peri | experience, experiment, experimental |
| edi | edition, obedience, obedient ⚠️ | plan | explanation, plan, plane |
| edit | edit, editor, editorial | plant | plant, plantation, transplant |
| fav | favor, favorable, favorite | pleas | pleasant, please, pleasure |
| feat | defeat, feat, feature | polit | political, politician, politics |
| fort | comfort, comfortable, effort | post | post, postage, posture |
| fortun | fortunate, fortune, misfortune | pres::praeesse | presence, present, presently |
| fresh | fresh, refresh, refreshment | prev | prevalent, prevent, previous ⚠️ |
| gard::guarder | regard, regarding, regardless | prob | probability, probable, probe |
| grav | aggravate, grave, gravity | prof | profession, professor, profile |
| gul | regular, regulate, regulation | prop | proper, property, proportion ⚠️ |
| hero | hero, heroic, heroine | prosp | prosper, prosperity, prosperous |
| hibit | exhibit, inhibit, prohibit | qual | qualification, qualify, quality |
| host | host, hostage, hostess, hostile | quart | quart, quarter, quarterly |
| hum | hum, humor, humorous ⚠️ | res::sistere | resist, resistance, resistant |
| journ | journal, journalist, journey | sert | assert, desert, insert |
| larg | enlarge, large, largely | sid::sidus | consider, considerable, consideration |
| leg::lex-legis | delegate, legacy, legal ⚠️ | spac | space, spaceship, spacious |
| leg::lig | obligation, religion, religious ⚠️ | stitut | constitute, institute, substitute |
| lev | lever, levy, relevant | stor::instaurare | restore, storage, store |
| maj | majesty, major, majority | strain | constrain, restrain, strain |
| man::manus | manage, manner, manual | struc | construction, destruction, instruction |
| metr | metre, metric, symmetry | suit | suit, suitable, suite |
| mod | commodity, moderate, modify | temp | contemporary, temper, temporary |
| tempt | attempt, contempt, tempt | teri | deteriorate, exterior, interior |
| tin | continent, continual, continuous | | |

> 第三十六/三十七批已入库：auctor、clarus、crescere、gerere、habitare、punktum、limes、gubernare 八族 27 词（含 fac 补 fact/factor/factory）。以下族不再出现在上面清单：auth、clar、creas、gest、govern、habit、limit、point。

### C. 审核拆分族（必须先行，严禁直接整族入库）

以下 vetted 族**内部词不同源**（来自 vetted_families accuracy_note：启发式词干提取混入同形异源词根）。接任时必须拆成独立词根族再加入：

| vetted 族 | 内部分叉 |
|---|---|
| conc | concession ← cedere（让步）；concise ← caedere（切）；reconcile ← conciliare（和好）⇒ 拆为 ced 家族 + caed 族 + conciliare 族 |
| comp | comparable ← par(are)；compile ← compilare；comply ← complere ⇒ 不拆清并族会错 |
| edi | edition ← edere（出版）；obedience/obedient ← obedire ← audire（听）⇒ 应拆 |
| prec | preceding ← praecedere（ced）；precise ← praecidere（caed）⇒ 拆成两组，precise 建议 caed |
| prev | prevalent ← praevalere（valere）；prevent ← praevenire（venire）；previous ← praevius（via）⇒ 拆 3 组，不并族 |
| hum | hum(拟声) ← 哼声；humor ← 拉丁 humor(湿) ⇒ 两词不同源，split |
| prop | proper, property ← proprius（自己的）；proportion ← portio（份）⇒ 拆两组 |
| pair | pair ← par（一对）；repair ← reparare（再备好）；impair ← peior ⇒ 同族两源，需拆清 |
| leg::lex-legis | delegate, legacy, legal ← lex（法）；与 legere（读）不同根 ⇒ 新建 lex 词根 |
| leg::lig | obligation, religion, religious ← ligare（绑）⇒ 新建 ligare 词根 |
| suit | suit, suite ← suivre（跟随，法语）≠ sequi ⇒ 与 sequi 同 PIE *sekw，可并入 sequi 或单建，词条说明法语路径 |

> 规则：**当一个 vetted 族要入两个以上词根时，拆成多族，分别开词根**；若某词根在考研 5500 内只有 1-2 个成员，放进 demoted 或单独建成族亦可（参考已有 `demoted` 结构，不强制凑满 3 词）。

### D. 可吸收进已建模词根的"纯族"（建议当作 additions 不做新品根）

| vetted 族 | 拟吸收进 | 词 |
|---|---|---|
| accord | cors | accord, accordance, accordingly |
| feat | fac | defeat, feat, feature |
| prob | prob | probability, probable, probe |
| res::sistere | sta | resist, resistance, resistant |
| stitut | sta | constitute, institute, substitute |
| tin | tain | continent, continual, continuous |

> ⚠️ fact/factor/factory 已被第三十六批并入 fac（roadmap 已记），本表不重复。

---

## 二·五、既有词源错配（接手时修正）

- `data/words.json` 中 `fac`（facere 做/造）根下错误挂载了 5 个 capere（抓取/接）词：**concept, except, receipt, susceptible, accept**。这 5 词来自 capere，与 cep/cept 族（exception/reception/acceptable/acceptance）同族，**不是** facere。
- 建 **cep（capere）词根族**时，把这 5 词的 `root_ids` 从 `fac` 改挂到新 `cep` 根即可一并清掉这个历史错误。
- 改动前先跑一次 `validate.py` 记录基线，改完必须全绿。

---

## 三、风险族与不可硬造红线

1. **同形异源混淆**（根源在 vetted_families 自动提取）：
   - `sert`（assert/desert/insert）← 拉丁 serere（连接、编制），**可成立**，但注意 `dessert`（甜品）← 法语 desservir（清理餐桌）→ 英文 dessert，**不是** serere，绝对不要混入本族。
   - `temp`（contemporary/temper/temporary）：contemporary/temporary ← tempus（时间）；temper ← temperare（调和）——拉丁同一词根 tempus 的"按时/得当"引申，词条要讲清分支。
   - `host`（host/hostage/hostess ← hospes；hostile ← hostis）：拉丁 hospes 与 hostis 同源（PIE *ghos-），词条要写双支来源。
   - `tempt`（tempt/attempt/contempt）← 拉丁 temptare（试探），与 temptare 家族同源（tent），注意与 time 无关。
2. **Q12 泄题红线**：core_image 和 root 名**不得点名本词中文义项**（如 hostile 不能写"敌人"作画面、grave 不能写"坟墓"当画面——见 batch35/36 已写处理）。
3. **词根 id 撞同名单词** → 自环边。必须用拉丁词形（point 是单词，词根用 punktum 已有；suit 是单词，词根用 sequi 或单建，避免自环）。

---

## 四、管线 SOP（照抄已有批次模式）

每批固定流程：

```bash
# 1. 新建批脚本（照抄 scripts/build_batch35.py 结构）
#    families[]: {root, concept, domain, words[]}，可内联声明新词根/概念/域
#    additions{}: 按已建模 root_id 补成员
python scripts/build_batchNN.py            # 生成 ai_pipeline/batchNN.json

# 2. 结构检查
python ai_pipeline/review.py check ai_pipeline/batchNN.json

# 3. 外部词注册（check 会列出不在 english_reference 的"外部词"）
#    人工确认后写入 data/lexicon.json 的 external_words（见 register_batch35_lexicon.py 模板）

# 4. 合并（合并前后各跑一次 validate.py，不过则拒绝落库）
python ai_pipeline/review.py merge ai_pipeline/batchNN.json

# 5. 质量门
python tests/validate.py                    # Q1-Q12
python tests/visual_audit.py                # 5 界面，全部 0 重叠/0 泄露

# 6. 更新 roadmap.md（第三十八批…… 词数/词根数/新增 root 清单）
# 7. git add/commit/push（推 main 分支，GitHub Pages 自动部署）
```

**batch35 模板**：`scripts/build_batch35.py`（34 词 4 新根 5 补，架构就是你要的新写法）
**注意**：第三十六批踩过 `domain_add` 同域词根需**累积追加**（dict 覆盖会丢根）的坑；多词短语 synonym 需注册进 `external_words` 才过 Q8。

---

## 五、当前 git 状态（接手时确认）

- 分支 main，本地 = `ae7637e`（交接提交）叠在 `3aa6ff5`（第三十七批）之上，**未推送**。
- 推送前请先 `git fetch` 确认远端未再前进；若有新批，rebase 后按新口径重算剩余。
- 不要动 `data/lexicon.json` 已有词、不要回头重写旧批。

---

## 六、优先级建议

1. **A 类 25 词【吸收】+ D 类 21 词【并入】**：零风险，先清完，一次 commit。
2. **C 类【拆分族】先做决策**：逐个确认每个词的正确词根归属，产出拆分后新族清单。
3. **B 类【新品根族】**：按"高生产价值 + 好画面"优先（fort/temp/tempt/host/grav/sert/cep 是我已着手、词源已核实的），每批 3-8 族，直到 227 清完。
4. 每批都要过 validate + visual_audit + 更新 roadmap，**绝不跳过质量门**。

---

*本文件由人工作业生成，供新对话接手。所有词源判断均在文中标注了 ⚠️ 的位置待复核。*