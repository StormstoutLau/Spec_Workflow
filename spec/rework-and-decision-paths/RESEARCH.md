# 调研文档：回写流与多方案决策路径（Q1 上游被推翻 / Q2 方案与故障链分析）

---
id: rework-and-decision-paths-RESEARCH
type: design
version: 1.2
status: draft
date: 2026-09-27
depends: [ADR-0006, ADR-0007, ADR-0010, SPEC-PROCESS, loop-engineering-RESEARCH, project-console-DESIGN, FWK-DECISION-RECORD]
upstream: null
---

> **Feature**: 回写流与多方案决策路径（P-050）
> **创建日期**: 2026-09-27
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户提问——① 当前是否具备回写流（调研→设计→实施→重新调研…，且某阶段推翻上游输入）；② 当前能否处理多方案、故障依赖链排查、方案优先级、顺序依赖、短/长期成本收益。要求结合社区与学术信息，基于当前框架详细调研。
> **v1.1 变更（2026-09-27，补充扫描轮）**：用户追加指令「除回写与依赖分析外，是否还有其他同类『状态未表达但已具备实施基础』」。新增 **[§3.8](#38-补充扫描q1q2-之外的三项候选与一项负结果v11)**——三项成立候选（PROGRESS 四态退化 / 决策记录契约零机械消费 / CHECKLIST 条目级无机械重数）+ **一项被推翻候选的负结果登记**（`upstream` 字段）+ 两项反例（`confidence` / ADR `superseded`）；§4.2 结构性观察**精确化**为「状态表达只有『完成态』一档真实可用」。
> **v1.2 变更（2026-09-27，吃狗粮整改轮）**：用户指令「是否可以对 P-050 进行吃狗粮开发」→ 执行 **同基座独立 pass**（RULE-1 取证清单 + RULE-5 降级标注），**发现 7 项（2 P1 + 2 P2 + 3 P3）且全部整改**：新增 **§5.3 独立 pass 记录**（含发现表与整改状态）；F2/F3（**P1，把眼估当机械重数**）→ §3.8.6 / §3.8.1 及 A-24 / A-18 订正；F4（引用来源错位，「契约 §6」实出 `decision-schema` DESIGN §6）→ §3.8.2；F5 / F6 / F7（P3：分支数、计数口径、文件性质）→ §3.8.6 / §3.8.3 / §3.8.2 订正；**F1（结构性覆盖缺口）→ 补建 `specwf-p050-20260927v2.jsonl` 覆盖 v1.1 轮**（原 session 仅覆盖 v1.0）。本批两处自我更正与审查发现合并登记为 **M7 样本 #35**。断言计数**不变（24A+12B+5C+6H）**——本轮为订正与整改，无新增断言行。

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 24 | 本仓机械取证（E1 源码/文档读取）+ 三处运行面实证（E2，含一处跨仓复核） |
| B 推断类 | 12 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 5 | 不参与 R7 机械对账（DR-2） |
| 假设区 | 6 | 未实测项（见附录 C） |

---

## 1. 调研目标

**Q1（回写流）**：当工作阶段推进到「实施」甚至「验证」后**推翻了上游输入**（调研结论错 / 设计前提不成立），当前框架是否具备回到上游并继续的**机械通路**？通路的缺口在哪一层？

**Q2（多方案与故障链）**：面对「同一任务存在多个方案 + 某个故障需要沿依赖链排查 + 方案优先级 + 顺序依赖 + 短期/长期成本收益」这五件事，当前框架**哪些已有载体、哪些完全空白**？

**Q3（v1.1 追加，同类缺口横向扫描）**：除 Q1/Q2 已识别的缺口外，是否还有**同一族**的位置——「状态/关系**应当表达**、载体**已存在**（字段 / 模板 / 已写入数据）、**确实有人在写**，但**契约未表达或机械未消费**」？判据与结果见 §3.8。

三问共同指向同一件事：**当前框架的「关系」表达能力**（阶段之间的关系、方案之间的关系、故障之间的关系）。

## 2. 调研方法

| 工具 | 用途 |
|------|------|
| Grep/Read（本仓） | E1 取证：命令面、状态词表、依赖字段、既有先例（加权评分 / gap 三元组 / M7 分桶） |
| RunCommand（`spec_runner --help` / 源码） | E2 取证：子命令清单与 `fork` 的确切语义 |
| WebSearch（社区/学术） | E3：回写/返工的经典过程模型、ADR supersede 惯例、FTA、CPM/PERT、ATAM/CBAM、CoD/WSJF/技术债利息 |
| 对照对象 | 承接 `loop-engineering`（P-028）已有结论（80% 底座 / 缺自动回流），**本批做的是能力实测而非概念重述** |

## 3. 调研发现

### 3.1 Q1 本仓实测：已有「回写的机械原语」，但只到事件流层

A-1 事件流层：`tools/spec_runner/sessions/*.jsonl` **只增不改**；`SPEC_PROCESS` 十步管道（RESEARCH→DESIGN→IMPLEMENTATION→CHECKLIST）**单向推进**，批次之间无自动反馈【E1】
A-2 命令面层：`spec_runner` 存在 **`fork`** 子命令——"复制前 N seq 行至新流（L4）"，实现为 `kept = [r for r in src if r["seq"] <= args.seq_from]` 后写入**新 session 文件**（`spec_runner.py` L487-507）【E1】。**这是本仓唯一的分叉写入原语**，也是「回到上游第 i 步重新开始」的机械底座
A-3 命令面构成：`run / gate / status / replay / fork / step-gate / step-enforce / verify-anchor / selftest`——其中校验类四者（`step-gate` / `step-enforce` / `verify-anchor` / `selftest`）**均为只读**，`fork` 是**唯一**能产出新事件流的命令【E1】
A-4 实践先例（人工回写已发生过）：P-028 的 v1.1 补充采用**新 session** `specwf-p028-20260909v2` 重入上游；P-023 亦以 `research+design` 两条 decision 回溯登记（step-enforce 落地**之前**批次缺决策流，提交被 P-024 门禁阻断后**补记真实发生的事实**）【E1】⇒ **回写在实践中靠「新建 session + 人工补记」完成，不靠工具触发**

### 3.2 Q1 本仓实测：ADR 层有完整失效语义，四件套层没有

A-5 ADR 层**已有 `superseded`**：ADR-0006 §B 失效条件①即写作"用户裁决方案 A → 本 ADR 状态改 **superseded**，`upstream` 反向设置"【E1】
A-6 契约层**已有 bi-temporal 时间语义**：`DECISION_RECORD_CONTRACT` §…「状态（accepted/superseded）| `metadata.status`；**superseded 时点 → `valid_until`（bi-temporal）**」【E1】⇒ 决策级失效**可被表达为两个时间点之间的有效区间**
A-7 **但四件套（design 类）的词表内没有失效态**：ADR-0007 D5 定 `design` 状态词表 = **`draft / in-review / verified`**（CHECKLIST 实例为 `pending / accepting / accepted`），**不含 `superseded` / `deprecated`**【E1】
A-8 且**不得自造**：全仓状态词表"固定, 不得自造"（`ASSERTION_EVIDENCE_FRAMEWORK` 状态词表章 + DC2 权威声明）【E1】⇒ 上游 RESEARCH/DESIGN 被推翻时，**在现有契约下无合法状态可标记它作废**；唯一合规做法是**追加文字（追记）**，即 P-045 至 P-049 反复使用的形态

### 3.3 Q2 本仓实测：五项能力中「两项有载体、三项空白」

A-9 **依赖图有机械载体，但只覆盖 ADR 层**：ARC 决策图谱 `tools/arc/data/.arc/` = **8 实体 / 7 `depends_on` 边**，并配 `arc trace` / `arc impact` 查询【E1】。四件套的 front-matter **只有 `depends:` 静态声明**（七字段之一），**无「上游变更 → 下游标记失效」的传播机制**【E1】
A-10 **多方案加权评分有先例，但为一次性**：P-033 对「ARC 升级 vs 四单维补位」用 5 维加权矩阵（关系图谱 30% / 兼容 25% / 性能 10% / 维护 15% / agent 面 20%）得出 ARC 4.2 优于次高 3.2【E1】⇒ 方法可用，但**未契约化**（无模板、无权重异议登记、无复用入口）
A-11 **缺口量化已有雏形**：`repo_stats` 的 drift-gate `CheckResult.gap` 输出**意图 X → 证据 Y → 缺口 ±N** 三元组（P-029）【E1】⇒ 「缺口」的表达已有机械先例，但仅用于视图层对账，**未用于方案比较或故障链**
A-12 **失效模式有台账**：M7 证据账本按**形态分桶**（形态 II = 未入分桶的独立样本，P-027 样本 ㉛）【E1】⇒ 故障**模式**可沉淀，但**故障之间的依赖关系**（A 导致 B、A 与 B 需同时成立）无任何载体

### 3.4 Q1 社区/学术对照：返工问题的经典解法是「风险驱动 + 显式回环」

A-（外）**Waterfall 的结构性缺陷正是「禁止回环」**：各阶段须 100% 完成并签字方可推进，后期发现的问题"或被忽略（保进度），或触发昂贵的正式变更请求"；其致命处在于**需求与交付之间的时间差**（Phase 1 写规格、Phase 5 才见到软件）【E3】
A-（外）**Boehm 螺旋模型（1986）明确把「go-back 返工」写进模型**：四象限（目标设定 / **风险分析与削减** / 开发与测试 / 下一轮规划）循环，"accommodates reworks on go-backs to earlier stages as more attractive alternatives are identified on as new risk issues need resolution"；**距中心的半径 = 累计成本**——早期回环便宜、后期昂贵【E3】
A-（外）**返工代价的量化锚点**（Boehm 系错误代价升级数据）：需求阶段 1×、设计 5-10×、编码/单元测试 10-20×、集成/验收 50×+、发布/维护 **200×+**【E3】⇒ **回写越晚越贵**，这为「何时必须回写、何时只能追记」提供了量化依据

### 3.5 Q1 社区对照：ADR 的失效惯例 = **追加新记录 + 互链**，不是改旧记录

A-（外）**AWS Prescriptive Guidance**：ADR 在 accepted 后应视为**不可变**；变更须**新建 ADR** → 评审 → 通过后把**旧 ADR 状态改为 `Superseded`**【E3】
A-（外）**Microsoft Azure Well-Architected**：ADR 是 **append-only log**，"Don't go back and edit accepted records. If a decision changes, write a new record that supersedes the original and **link the two together**"；状态建议含 **Proposed / Accepted / Superseded**；并明确**长中短期应拆成多条记录**（"Break one decision into multiple if an architectural decision is going to result in multiple phases, such as short-term, mid-term, long-term approaches"）【E3】

⇒ **本仓 ADR 层已与社区惯例一致**（A-5/A-6：`superseded` + `upstream` 反向设置 + bi-temporal），**差距在四件套层**（A-7/A-8）。

### 3.6 Q2 社区/学术对照：四项能力各有成熟方法，且均为「图 + 量化」

| Q2 子问题 | 社区/学术方法 | 核心机制 |
|---|---|---|
| **故障依赖链排查** | **FTA**（Fault Tree Analysis；NASA SWEHB 8.07；IEC 61025 / MIL-STD-882E / ISO 26262 等标准） | 自顶事件（Top Event）**向下**分解，用 **AND / OR 逻辑门**表达"单个原因即致"vs"须同时成立"；分解至 Basic Event（根因）；定性产出 **最小割集（Minimal Cut Sets）**，单元素割集 = **单点故障**（最高优先）【E3】 |
| **顺序依赖分析** | **CPM / PERT**（1950s 运筹学；DuPont + 美海军 Polaris） | 任务建成 **DAG**；**拓扑序**保证每个任务的所有前驱先完成；**正推**算最早开始/完成、**逆推**算最晚开始/完成；**松弛量（float/slack）= 0 的任务构成关键路径**——关键路径决定最短工期，其上任一延误等量推迟整个项目【E3】 |
| **方案优先级分析** | **ATAM**（SEI，CMU/SEI-2000-TR-004） | 以**质量属性场景 + 效用树**结构化，识别**风险点 / 非风险点 / 敏感点 / 权衡点**；目的**不是精确分析而是发现风险**【E3】 |
| **成本收益（短/长期）** | **CBAM**（ATAM 的经济扩展）+ **CoD / WSJF** + **实物期权 / 技术债利息** | CBAM 以「效用 × 业务重要性权重」= 收益、除以成本，按**收益/成本比**排序【E3】；CoD 把延迟损失拆为**直接开销（线性）+ 价值衰减（非线性，含"硬悬崖"型）**，WSJF = CoD / 工期【E3】；技术债利息 = 以**速度损失**折算（Fowler 例：本应 3 天而实耗 5 天 ⇒ 2 天即利息），且有"越晚修越贵"的量化共识（晚修最高可达早期 100×）【E3】 |

### 3.7 差距矩阵（两问合并，逐项判定）

| 能力 | 当前载体 | 判定 |
|---|---|---|
| 事件流分叉（回到上游第 i 步） | `spec_runner fork --seq-from`（唯一写入原语） | **已有**（但无触发、无登记） |
| 决策级失效 | ADR `superseded` + `upstream` 反向 + `valid_until`（bi-temporal） | **已有**（仅 ADR 层） |
| 文档级失效（RESEARCH/DESIGN 被推翻） | 无合法状态（design 词表无 `superseded`，且不得自造） | **空白** |
| 依赖关系 | ARC `depends_on`（8/7，仅 ADR 层）+ 四件套 `depends:` 静态声明 | **部分**（无传播） |
| 多方案比较 | P-033 5 维加权矩阵（一次性先例） | **部分**（未契约化） |
| 缺口量化 | `repo_stats` gap 三元组（意图→证据→缺口±N） | **部分**（仅视图对账用） |
| 失效模式沉淀 | M7 账本形态分桶 | **已有** |
| **故障依赖链（AND/OR 门 / 最小割集 / 单点故障）** | 无 | **空白** |
| **顺序依赖（拓扑序 / 关键路径 / 松弛量）** | 无（PROGRESS 有 P 号与触发项，但无 DAG 与 slack） | **空白** |
| **短期/长期成本收益（CoD / CBAM / 利息 / 期权）** | 无（P-028 v1.1 引入过成本实证，但为单点引用） | **空白** |
| 自动回流（校验失败→反思→注入） | 无（P-028 结论不变） | **空白** |

### 3.8 补充扫描：Q1/Q2 之外的三项候选与一项负结果（v1.1）

**扫描判据（「已具备实施基础」三条件）**：① 载体**已存在**（字段 / 模板 / 已写入数据）；② **确实有人在写**（非空想）；③ 缺的只是**契约表达或机械消费**。三条同时满足才登记为候选；任一不满足即登记为负结果或反例。

#### 3.8.1 候选 ①：PROGRESS 状态词表四态**实际退化为一态**，`blocked` 零使用【E1】

- 词表**声明为四态**（`PROGRESS.md` L3：`pending / in-progress / blocked / done`），实测使用分布 = **`done` 50 次 / `pending` 0 / `in-progress` 0 / `blocked` 0**【E1】
- 而「等待外部触发」**真实存在且持续书写**：`PROGRESS.md` 中含「触发」的**行数 = 63**（口径 = 行数，读数日期 2026-09-27；**⚠ 该计数随 PROGRESS 增长漂移，属本仓形态 II「计数」族——原稿「59 次」经 P-050 独立 pass 机械复算证伪，见 §5.3**）；P-009、P-030、P-036、P-037 均为「止于懒加载 gate，触发条件 = …」形态【E1】
- **代偿手法 = 用编号表达状态**：`PROGRESS.md` L102 原文——「P-009 记为 5 而非 4，标识其属**「触发驱动」异质类（不排队、等外部条件）**，语义上与主动队列隔开，避免被误读为『下一个要做的第 4 项』」【E1】
- ⇒ 与 Q1 的「四件套无失效态 → 只能追记文字」（A-7/A-8）**同构**：状态词滞后于事实，用非状态手段（编号 / 散文 / 「零（等待触发即设计状态）」）代偿。把该项升级为 `blocked` 属**分类工作而非采集工作**——触发条件早已写在文档里。
- **看板侧反证（本批追加核实，用户质疑触发）**：`console_gen.py` 的 `derive_state` **已为「什么在等」设计了位置**——`blocked` → `Needs Attention`、无 session → `Needs Attention`、gate 软性存疑 → `Ready to Verify`、非终态 → `Recommended`（`TIER_ORDER` 三档），且 `Recommended` 分支还会调 `next_step()` **推导「下一步」**。**但它当前完全空转**：`derive_state` **第一分支**即 `if task.status == "done": return Derived("done", …, "")`（tier = 空），而 PROGRESS **50/50 全为 `done`** ⇒ 其后**四个分支全部不可达**，`docs/CONSOLE.md` 的「⚑ 需要你 / NEXT」三档渲染为 **「（无）」×3**，`next_step()` 对当前集合**成为不可达代码**；且 `console_gen.py` L17/L60 的 **I-7「状态只用 PROGRESS 原词，不重贴标签」**明文**禁止视图层自救**。
⇒ **不是「不擅长表达」，而是「表达层已备、真值层无值」**——「机制缺失」与「输入缺失」是两回事。本候选因此由「缺表达」**升级为「机制空转」**，后者更严重：**空转的机制会制造「已覆盖」的错觉**（三档队列恒显「（无）」读起来像「无待办」，实为「无值可判」）。

#### 3.8.2 候选 ②：决策记录契约十字段——契约齐备、数据已写入、**零机械消费**【E1】

- `DECISION_RECORD_CONTRACT` v1.1 定义八字段 + 两时点（含 `decision_maker` / `valid_from` / `valid_until`），并含三载体映射表与 I-1~I-4 不变式，**契约文本完整**【E1】
- 全仓检索 `decision_maker|valid_from|valid_until` 命中 **12 文件**（**口径订正**：其中 **9 个文档 + 3 个 session JSONL**——session 内为契约字段名出现，非消费）；`scripts/` 侧**零消费**【E1】（原稿「全部为文档」经 P-050 独立 pass 证伪，见 §5.3）
- 而 session jsonl 中 `"confidence": 0.9` **已按契约写入 153 次 / 33 个 session**【E1】
- `spec/decision-schema/DESIGN.md` §6 风险表**自认**：「无人消费的契约沦为僵尸文档」【E1】（**来源订正**：原稿作「契约 §6 风险表」，但 `DECISION_RECORD_CONTRACT` 仅至 §5、**无 §6**；该句实出 decision-schema DESIGN §6，见 §5.3）
- ⇒ 数据**已经在写**，缺的只是**校验器**——且「结构完整性」（scenario / reasoning / outcome / valid_from 是否齐）是**可机械判定**的，属低成本切口。

#### 3.8.3 候选 ③：CHECKLIST 条目级状态**无机械重数**【E1】

- 条目级「通过 / 待办 / 失败」标记形态稳定存在（全仓 **37 行 / 9 文件**；口径 = `spec/**/*.md` 中含该三标记之一的行数，读数日期 2026-09-27——原稿「约 30 处」经 P-050 独立 pass 机械复算修正，见 §5.3）【E1】
- `repo_stats.py` **仅解析 PROGRESS 的 P 号**（L387-**394**；原稿作 387-390，经独立 pass 校订）；`dc_validator.py` 的四项检查（frontmatter / namespace / counting / links）**均不解析 CHECKLIST 条目**（counting 只对 §0 断言统计表）【E1】
- ⇒ 全仓「**声明 = 重数纪律**」（R7）在此**唯一豁免**：P-049 CHECKLIST 的「39 项 / 33 通过 / 6 待办」为**手写计数**；那 6 项待办**无任何机械追踪**，是漂移的必然位点。

#### 3.8.4 负结果登记：`upstream` 字段是**被推翻的候选**（本批自我更正）【E1】

- **初始假设**：`upstream` 字面 = 反向依赖指针 ⇒ 疑似「字段闲置」。实测支持该假设：`spec/` 88 份中 87 为 `null`（唯一非 null = `PILOT_TASK_CARD.md`）、`adr/` 8/8、`docs/` 4/4 ⇒ **100 份中 99 为 `null`**；而 `depends:` 在 `spec/` 下 **88/88 全填**【E1】
- **推翻依据**：`PLAN.md` L51 定 `upstream` 语义 = **「上游权威源声明」**，明文「**本仓库份为权威源时置 `null`**；为迁移副本时置源路径」；ADR-0006 方案 B 已采纳「本仓为权威源」⇒ **全 null 是契约正确值，不是缺口**【E1】
- **跨仓复核**：Cpp_Hub 侧 `docs/ASSERTION_EVIDENCE_FRAMEWORK.md` **无 front-matter**（L1 为标题行），以正文「⚠️ 权威源已迁移」指针行（L5）代偿声明 ⇒ 属 P-049 `downstream_compliance.py` 的 J-1 检测面，**非本批新增缺口**【E2】
- ⇒ **教训（可复用）**：字段名的**字面直觉**（"upstream = 上游依赖"）与**契约定义**（"上游权威源"）不一致时会直接导致误判——本仓 ADR-0007 治理过的「同名双义」风险，在**同一份 front-matter 的七字段内部**同样存在。**负结果同样是结论**：本次把它登记下来，以免后续重复假设。

#### 3.8.5 反例登记：两项「未表达」但**不该表达**【E1】

- `confidence` / `severity` 的量化：已被 decision-schema DESIGN **D2** 与 **I-2 不变式**裁决为「固定 0.9 占位 / **禁止浮点编码** / 无数据源不虚构」⇒ **不是缺口，是已被裁决为不表达**【E1】
- ADR `superseded`：`adr/` 下 **0 命中**（8 份 ADR 无一失效）⇒ **失效尚未发生**，非缺口【E1】
- ⇒ 二者共同指向一条规律：全仓**只有「成功路径」被反复走过**（`done` 50 / 其余 0；`superseded` 0），**失效与阻塞侧从未被真实走过**——`done 50/0/0/0`、`upstream 99/100 null`、`superseded 0` 是同一件事的三个侧面。

#### 3.8.6 I-7 约束对看板机制的专项影响分析（用户追加指令）【E1】

**I-7 原文**（`spec/project-console/DESIGN.md` L112）：「状态输出**只用 `PROGRESS` 原词**（`pending`/`in-progress`/`blocked`/`done`）+ 独立「派生依据」列，**不得重贴标签**（禁「待你审」）」；动机见同文件 L26 = 修正 P-042 **A-3 状态语义错配**——废止「⚠ 待你审」这类**凭空升格标签**。

**影响一：I-7 把视图层能力切成两半**（这是理解其余影响的钥匙）

| 通道 | I-7 裁定 | 代码落点 |
|---|---|---|
| 状态**词** `status` | **冻结**——只读源，不得改写 | `derive_state` 返回 `Derived(status, …)`，**第一参直传** `task.status` |
| **派生依据** `basis` / **行动档** `tier` | **允许派生** | 后两参由分支计算 |

⇒ I-7 的实质是**一次刻意的能力交换**：以「视图层不可自愈」换「状态层不可造假」。它把「凭空升格」的通道关死，代价是**放弃视图层的语义补偿能力**。

**影响二：源层状态退化被制度性封死为「不可自愈」**

PROGRESS 50/50 全 `done` ⇒ `derive_state` 的 `done` 首分支短路 ⇒ 后四分支不可达 ⇒ `TIER_ORDER` 三档恒空（§3.8.1）。**若 I-7 不存在**，视图层本可用「制品链 / step / session 有无」把 `done` 项**重贴**为「待触发」而让队列复活；**I-7 明文禁止这条路** ⇒ **唯一合法修复点在源层（PROGRESS）**。故「机制空转」是**制度性结果，不是实现疏漏**。

**影响三：「触发驱动」散文项在视图层既读不到、也不许救**

P-009 等的「等待触发」语义写在 PROGRESS 的**事项 / 散文列**，**不在 `status` 列**；视图只读 `status` ⇒ 该语义（a）**读不到**（不在取值面）；（b）即使读到也**不许重贴**（I-7）。二者叠加使其在看板上**结构性不可见**。

**影响四：新增「等待」态的实现位置被 I-7 锁定为 Layer-0**

若将来要新增「等待触发」类状态，按 I-7 的精神它**必须先进 DC2 / PROGRESS 词表（Layer-0 契约）**，而**不得**只在 `console_gen.py` 内加一层映射——后者正是 I-7 所禁的「重贴标签」。⇒ **I-7 直接支撑 §4.3 最小切口的「分层归属 = Layer-0」判定**。

**同族发现：看板存在三处「定义档位 > 实际可达档位」**

| 机制 | 定义档位 | 实际可达 | 不可达原因 |
|---|---|---|---|
| `derive_state` 状态分支 | **6**（`done` / `blocked` / 无 session / soft / `finalize` / else；原稿计 5，经独立 pass 校订） | **1**（`done`） | `done` 首分支短路（PROGRESS 50/50 全 done） |
| `TIER_ORDER` 行动档 | 3 | **0** | `tier` 由 `status` 分支决定 ⇒ 恒空 |
| `feature_stage` 阶段 | 5（未启动/调研/设计/实施/验收） | **3** | 制品链**降序互斥**：`C` 存在即遮蔽 `I`/`D` ⇒ **「实施」「设计」两档结构性不可达**（实测 CONSOLE **34** feature 行：调研 **14** / 验收 **19** / 未启动 **1**，**设计 0 / 实施 0**——原稿作 15/18，经独立 pass 机械重数订正） |

⇒ 三处**共因**：**视图定义的档位空间宽于上游真实取值空间**。而 I-7 恰是**禁止视图用重贴标签去填这个差**的那条约束——故「档位不可达」在本仓是**结构性**的，**只能由源层扩值解决**（与影响二同一结论）。

**I-7 边界口径未登记（本批新发现）**：CONSOLE 头部声明「状态词表 = `PROGRESS` 原词（I-7）」，但同页 §2 feature 表的「**阶段**」列使用了 **3 个实际出现的词**（未启动 / 调研 / 验收；定义 5 个）**均不在 PROGRESS 词表内**。按 I-7 **字面**（约束「**状态**输出」）该列不在管辖内；但「阶段」承载的正是**状态类语义**（处于哪个阶段）⇒ **「I-7 是否管辖派生词表」属口径未登记**（既非违规、亦非已豁免）。登记为待裁口径（见 §6）。

## 4. 综合分析

### 4.1 关键发现总结

1. **Q1 的答案是「有原语、缺语义」**：回到上游的机械通路**已存在**（`fork`），但(a) 无「谁触发」的判据，(b) 无「上游被推翻」的**标记词汇**（四件套无失效态），(c) fork 出的新流与原流**无关联登记**（不构成可追溯的返工图）。【置信度: ★★★★★】
2. **失效表达的不对称是本仓最尖锐的结构缺口**：ADR 层有 `superseded` + bi-temporal（与 AWS/Azure 惯例一致），四件套层却**只有 `draft/in-review/verified`**；而四件套恰恰是最常被推翻的层（调研错→设计崩）。这解释了为何历史上「推翻上游」一律以**追记文字**表达（P-045 至 P-049 反复出现）。【置信度: ★★★★★】
3. **Q2 的五项能力里两项半有载体、三项全空白**（§3.7）：依赖图有但只覆盖 ADR；多方案评分是先例而非契约；而**故障链 / 关键路径 / 成本收益**三项无任何形式化载体。【置信度: ★★★★☆】
4. **社区对 Q2 三项空白给的是「图 + 量化」而非「流程」**：FTA 给逻辑门与最小割集，CPM 给 DAG 与松弛量，CBAM/WSJF 给效用-成本比与延迟损失分解。三者都**不依赖重型流程**，与单人开发者规模相称——门槛在**建模**而非**工具**。【置信度: ★★★★☆】
5. **回写越晚越贵有量化依据**（Boehm 系 1×→200×+），故正确的设计目标不是"禁止回写"也不是"随时回写"，而是**让上游失效尽早可见**（= 本仓"机械可检出判据优先"的同一逻辑）。【置信度: ★★★★☆】
6. **同类缺口不止 Q1/Q2 两处，但成立者集中在「异常态 / 中间态」一侧**（§3.8，v1.1）：三项候选成立（PROGRESS 四态退化 / 决策记录契约零机械消费 / CHECKLIST 条目级无机械重数），另有一项候选被**推翻**（`upstream`）、两项被判为**不该表达**（`confidence` 量化 / ADR `superseded`）。⇒ 「未表达」不等于「该表达」，判据是**有无机械数据源且非自评**。【置信度: ★★★★☆】

### 4.2 结构性观察：本仓的「关系表达能力」落后于「状态表达能力」（v1.1 精确化）

**原表述（v1.0）**：本仓已把**状态**做到很细（front-matter 七字段 + DC2 词表 + M7 分桶 + PROGRESS 四态），但**关系**只有两处：ARC `depends_on`（ADR 层）与四件套 `depends:`（静态声明）。两问暴露的缺口**全部落在"关系"这一侧**：阶段之间的失效传播（Q1）、方案之间的比较（Q2 优先级）、故障之间的因果与先后（Q2 故障链 / 顺序依赖）。

**v1.1 精确化（§3.8 取证后）**：「状态表达强」这一判断**只在形式上成立**——实测显示本仓**只有「完成态」一档被真实使用**：PROGRESS 四态中 `done` 占 50/50（`pending` / `in-progress` / `blocked` 全为 0）；ADR 层 `superseded` 0 命中；`upstream` 99/100 为 `null`。故更准的表述是：

> **本仓擅长记录「什么已完成」；对「什么被卡住 / 什么作废了 / 什么在等」并非没有表达设计**（看板已备三档行动队列 `Needs Attention / Ready to Verify / Recommended` + `next_step()` 下一步推导 + `blocked`→`Needs Attention` 映射），**而是这些设计当前全部空转**——源层 PROGRESS 状态列 50/50 为 `done`，`done` 短路使其余分支不可达。**缺的是「值」，不是「机制」。**

> **自查更正（2026-09-27，用户质疑「我记得看板里面有记录」触发）**：本批初稿写作「**不**擅长记录什么被卡住 / 作废 / 在等」**不成立**——`console_gen.py` 的 `derive_state` 与 `docs/CONSOLE.md` 的三档队列确有该表达设计。经追查后更正为「**机制已备而空转**」，并据此把候选 ① 由「缺表达」**升级为「机制空转」**（§3.8.1 末条）。原判断的错因与上游 `upstream` 误判同类——**由字面印象代替机制核查**。

三者共用同一失效机制：**状态词表滞后于事实 ⇒ 一旦无合法状态可用，即退化为散文代偿**（追记文字 / 编号 hack / 「零（等待触发即设计状态）」）；且该退化会**向下传导**——派生视图（看板）的 `done` 短路把它转化为**恒空队列**（「（无）」×3），而 I-7 又**禁止视图层自救**。故 §4.3 的最小切口（补四件套失效态）与 §3.8.1 候选 ①（启用 `blocked`）本质是**同一处修复的两个入口**，且后者的收益不止于 PROGRESS——**它同时让看板三档队列从「空转」恢复为「可用」**。

### 4.3 结论与建议（登记，不实施）

【C】**Q1 现状判定 = 部分具备**：具备**手工可达**的回写路径（新建 session / `fork` / ADR `superseded` / 追记），**不具备**「上游失效的机械识别与标记」。

【C】**Q2 现状判定 = 部分具备**：具备多方案加权评分先例与 ADR 依赖图，**不具备**故障依赖链、顺序依赖（关键路径）、短期/长期成本收益的形式化载体。

【C】**建议的下一步（本次止于调研，不实施）**：优先补「**四件套的失效语义**」（最小切口：为 design 词表引入 `superseded` 并定义 `superseded_by` 关系字段，与 ADR 层对齐），因为它同时是 Q1 的缺口与 Q2「关系表达」的入口；故障链 / 关键路径 / 成本收益三项建议**各按自身规模单独评估**（FTA 与 CPM 已证与单人规模相称，可优先），不做打包。**分层归属 = Layer-0（契约层）/ Layer-1（工具层）候选**；激活条件 = 触发驱动；未激活副作用 = 0。

【C】**Q3 补充扫描判定（v1.1）**：三项候选成立——① PROGRESS 四态实际退化（`blocked` 零使用，§3.8.1；**并连带使看板三档行动队列与 `next_step()` 空转**）；② 决策记录契约十字段零机械消费（§3.8.2）；③ CHECKLIST 条目级无机械重数（§3.8.3）。三项均**登记不实施**，按实施成本从低到高排序为 ③（一次 grep 级对账）< ①（分类工作）< ②（新增校验器）。

【C】**「未表达 ≠ 该表达」判据（v1.1 新增）**：仅当**存在机械数据源且非 LLM 自评**时才登记为候选。`confidence`（D2 已裁决固定占位、无数据源）、ADR `superseded`（失效尚未发生）为**反例，不登记**；`upstream` 全 `null` 经契约复核为**正确值，不登记**（§3.8.4 负结果）。

## 5. 幻觉抑制审查（Step 2 Review）

### 5.1 证据验证

| 事实 | 验证方式 | 状态 |
|------|---------|------|
| 命令面清单与 `fork` 语义 | 源码读取 + `--help`（E1/E2） | ✅ |
| design 词表无失效态 | ADR-0007 D5 原文（E1） | ✅ |
| ADR 层 `superseded` + bi-temporal | ADR-0006 §B + DECISION_RECORD_CONTRACT（E1） | ✅ |
| ARC 8 实体 / 7 边 | P-049 实测读数（E1/E2） | ✅ |
| P-033 加权矩阵维度与得分 | PROGRESS P-033 与 arc-probe RESEARCH（E1） | ✅ |
| 社区/学术方法（FTA/CPM/ATAM/CBAM/CoD/ADR 惯例） | WebSearch 多源（E3） | ✅ |
| `upstream` 契约语义 = 上游权威源声明 | PLAN.md L51 原文 + ADR-0006 方案 B（E1） | ✅（**推翻**初始假设） |
| PROGRESS 四态使用分布 50/0/0/0 | PROGRESS.md 逐态机械计数（E1） | ✅ |
| 决策记录契约零脚本消费 | 全仓检索 + `scripts/` 复核（E1） | ✅ |
| CHECKLIST 条目级不在任一校验器范围 | `repo_stats.py` / `dc_validator.py` 源码复核（E1） | ✅ |
| Cpp_Hub 侧无 front-matter、以指针行代偿 | 跨仓读取（E2） | ✅ |

### 5.2 已知局限

1. E3 证据以检索摘要为主源（AWS/Azure 官方文档、NASA SWEHB、SEI 讲义、期刊摘要），**未做原文精读**；
2. P-033 加权矩阵的权重来源为**当时裁决**，本批仅引用其存在，**未复核权重合理性**；
3. 本批**未实测** `fork` 是否已被实际用于回写（仅取证其存在与语义），登记为 H1；
4. 社区方法与本仓规模的适配性**未做成本评估**，登记为 H3；
5. 本批含**两处自我更正**（均由机制核查推翻字面印象）：① `upstream` 由「字段闲置」被推翻为「契约正确值」（§3.8.4）；② 「**不**擅长记录什么被卡住 / 作废 / 在等」被 `console_gen.py` 的 `derive_state` + 三档行动队列推翻为「**机制已备而空转**」（§4.2 自查更正）。**共性教训 = 两处均因「以字面印象代替机制核查」而误判**（前者把 `upstream` 读成反向依赖、后者把「状态列退化」直接推成「无表达设计」）。→ **已于 v1.2 登记入 M7 账本**（与独立 pass 的 7 项发现合并为样本 #35，见 §5.3）。
6. **本批独立 pass 的 7 项发现全部未被文档自认**（含 2 P1），其中计数类断言因「读数未标口径与日期 + 载体持续增长」而天然脆弱——详见 §5.3。

### 5.3 独立 pass 记录（RULE-1 + RULE-5，v1.2 追加）

**审查配置**：**同基座独立 pass**——审查会话与被审文档的生成会话**无共享上下文**（时序独立满足 RULE-1）；**模型异质性未达成，按 RULE-5 降级标注**。

**审查输入**（RULE-1 补 · 取证清单）：① 事件流 `specwf-p050-20260927.jsonl`；② `verify-anchor --session specwf-p050-20260927` → **锚点 10 真实 / 0 硬性 / 0 软性、exit 0**；③ `git status` / `git log` → HEAD = `d37e090`，除未跟踪 `workflow.svg` 外**零变更** ⇒ 纯登记型批次，**无 diff 为合法态**。

**发现（7 项：2 P1 + 2 P2 + 3 P3）与整改**

| # | 级别 | 发现 | 整改 |
|---|---|---|---|
| **F1** | P2 | **事件流未覆盖最终文档状态**：session 5 条 decision 全述 RESEARCH **v1.0**（12A+4B+3C+3H），而交付文档为 v1.1（24A+12B+5C+6H）；**v1.1 补充扫描轮无任何决策事件** ⇒ RULE-1 补的「session 内容与文档状态一致」**不满足** | 补建 `specwf-p050-20260927v2.jsonl` 覆盖 v1.1 轮（承接 P-028 v1.1 分 session 先例） |
| **F2** | **P1** | **机械重数不符**：CONSOLE feature 阶段分布实测 调研 **14** / 验收 **19** / 未启动 1，原稿作 15/18（**眼估未重数**） | 已订正（§3.8.6 + A-24） |
| **F3** | **P1** | **机械重数不符**：`PROGRESS.md` 含「触发」**63 行**，原稿作 59 | 已订正（§3.8.1 + A-18） |
| **F4** | P2 | **引用来源错位**：「契约 §6 风险表」实出 `spec/decision-schema/DESIGN.md` §6；`DECISION_RECORD_CONTRACT` 仅至 §5、**无 §6** | 已订正（§3.8.2） |
| **F5** | P3 | `derive_state` 实为 **6** 个分支（漏 `finalize`→`Ready to Verify`），原稿计 5 | 已订正（§3.8.6 + A-23/A-24） |
| **F6** | P3 | CHECKLIST 条目计数**口径未登记且偏低**（原稿「约 30 处」；实测 **37 行 / 9 文件**） | 已订正并显式登记口径（§3.8.3 + A-21） |
| **F7** | P3 | 「12 文件全为文档」不确：实为 **9 文档 + 3 session JSONL** | 已订正（§3.8.2 + A-19） |

**审查结论**：两条主轴**均成立**——`upstream` 语义推翻（§3.8.4，`PLAN.md` L51 + 99/100 null 实测吻合）与看板「机制已备而空转」（§4.2，`done` 短路 + 三档恒「（无）」实测吻合）。但 **7 项发现全部未被文档自认**。**F1 属结构性覆盖缺口**：`step-enforce` 只校验 session **存在性**，不校验事件流是否覆盖**最终文档状态**——与 P-027 发现的「覆盖盲区」**同族**。

**教训（可复用）**：**两项 P1 同因 = 把「眼估」当「机械重数」**。本仓 R7 已立「声明 = 重数」纪律，但**未规定读数须标注口径与日期**；而计数类断言落在**会持续增长的载体**（PROGRESS / CONSOLE）上**天然脆弱**（本次即为实证：同一断言在不同时点机械复算可得 59 / 63 两值）。⇒ 建议登记为流程改进候选：**凡对增长型载体的计数声明，须附口径 + 读数日期**。

## 6. 对设计的输入（若后续触发）

- **最小切口**候选：design 词表增 `superseded` + front-matter 增 `superseded_by`（须过 ADR-0010 三问 + DC2 契约变更流程）；
- **不引入**重型流程：FTA/CPM 的建议形态是「**图 + 少量量化**」，可复用 ARC 的 `depends_on` 载体扩展，而非新建系统；
- **保持"只消费机械信号"**（P-028 约束）：任何失效判定不得来自 LLM 自评。
- **v1.1 三项候选的切口形态**（均登记不实施，按成本升序）：
  1. **CHECKLIST 条目级重数**（最低成本）：在 `repo_stats.py` 内加一项条目级对账，使「N 项 / M 通过 / K 待办」不再手写——与既有 R7 同构，**不新增契约**；
  2. **PROGRESS `blocked` 启用**（分类工作）：把现有「触发驱动」散文项归入 `blocked`（或按 DC2 变更流程新增「等待触发」态），**信息已在文档中，无需新采集**；**附带收益 = 解除看板三档队列空转**（`derive_state` 的 `blocked` / 非 done 分支将首次可达，`next_step()` 从不可达恢复可用）；
  3. **决策记录契约校验器**（新增校验）：对 `scenario` / `reasoning` / `outcome` / `valid_from` 做结构完整性检查——与 I-4「本契约不是验证机制」存在张力，须先裁决边界。
- **本批的负结果同样是设计输入**：`upstream` 不得被当作「反向依赖指针」使用（其语义是上游权威源声明）；若将来需要「反向依赖 / 返工图」，应**另立字段**而非复用 `upstream`。
- **I-7 边界口径待裁（v1.1 追加，用户指令触发）**：若 I-7 的精神是「不得新增 / 改写状态词」，则 `feature_stage` 引入的 5 档阶段词（未启动 / 调研 / 设计 / 实施 / 验收）与 PROGRESS 词表**并行**这一事实需先落口径——二选一：① 明确 **I-7 只管 P 行状态列**（阶段列属合法派生词表，但须在 DESIGN 中**登记该词表**）；② **扩展 I-7** 使其管辖全部状态类词表。**未裁决前，任何新增状态词都应走 Layer-0（DC2 / PROGRESS 词表）**，不得在 `console_gen.py` 内加映射。
- **「档位不可达」应由源层扩值解决，而非视图层补渲染**（v1.1 追加）：三处不可达（`derive_state` 5→1 / `TIER_ORDER` 3→0 / `feature_stage` 5→3）**同因**；其中 `feature_stage` 的「实施」「设计」两档因制品链**降序互斥**（`C` 遮蔽 `I`/`D`）而**结构性不可达**——若要保留该词表，须先裁决其判定口径（现行 = 取「最高已存在制品」，是否应改为「全部已存在制品的集合」需另议）。

## 7. 参考文献

1. B. Boehm, *A Spiral Model of Software Development and Enhancement*, IEEE Computer, 1988（MSU 存档 PDF）——回环 + 风险驱动 + 累计成本半径
2. W. Royce, *Managing the Development of Large Software Systems*, 1970（经 Jamie Little 课程讲义转述其缺陷分析）
3. AWS Prescriptive Guidance, *Using architectural decision records…*——ADR Superseded 惯例
4. Microsoft Learn, *Maintain an architecture decision record (ADR)*——append-only + supersedes 互链 + 长中短拆分
5. NASA SWEHB 8.07 *Software Fault Tree Analysis* / IEC 61025 / MIL-STD-882E——FTA 逻辑门与最小割集
6. SEI, *Architecture Tradeoff Analysis Method (ATAM)*（CMU/SEI-2000-TR-004 讲义）——效用树 / 风险点 / 敏感点 / 权衡点
7. Dhaya & Zayaraz, *Combined architectural framework… ATAM, FAHP and CBAM*, IJ CAT 2016——CBAM 收益/成本比
8. 社区工程文献：Cost of Delay（直接开销 + 价值衰减两分量，WSJF = CoD/工期）、Technical Debt 利息度量（Fowler 例 / 速度损失折算 / 晚修成本倍数）
9. 本仓既有：`spec/loop-engineering/RESEARCH.md`（P-028，循环底座与自动回流缺口）

---

**Review 签字**: _________ 日期: _________

---

## 附录 A 断言登记

### A 类（事实类，24 条）

【A】A-1 `tools/spec_runner/sessions/*.jsonl` 只增不改；`SPEC_PROCESS` 十步管道单向推进，批次间无自动反馈【E1】
【A】A-2 `spec_runner` 含 `fork` 子命令，语义 = 复制前 N seq 行至新 session（`spec_runner.py` L487-507）【E1】
【A】A-3 命令面 = `run/gate/status/replay/fork/step-gate/step-enforce/verify-anchor/selftest`；`fork` 为唯一产出新事件流的命令，其余校验类皆只读【E1】
【A】A-4 回写实践先例：P-028 v1.1 用新 session `specwf-p028-20260909v2` 重入上游；P-023 以 research+design 两条 decision 回溯补记【E1】
【A】A-5 ADR-0006 §B 失效条件①明写「本 ADR 状态改 `superseded`，`upstream` 反向设置」【E1】
【A】A-6 `DECISION_RECORD_CONTRACT` 定义 `accepted/superseded` 与「superseded 时点 → `valid_until`（bi-temporal）」【E1】
【A】A-7 ADR-0007 D5：design 状态词表 = `draft / in-review / verified`（CHECKLIST 实例 = `pending / accepting / accepted`），不含失效态【E1】
【A】A-8 全仓状态词表「固定, 不得自造」（`ASSERTION_EVIDENCE_FRAMEWORK` + DC2 权威声明）【E1】
【A】A-9 ARC 决策图谱 = 8 实体 / 7 `depends_on` 边，配 `arc trace` / `arc impact`；四件套仅有 `depends:` 静态声明【E1】
【A】A-10 P-033 用 5 维加权矩阵（关系图谱 30%/兼容 25%/性能 10%/维护 15%/agent 面 20%）比较方案，得 ARC 4.2 vs 次高 3.2【E1】
【A】A-11 `repo_stats` drift-gate `gap` 三元组 = 意图 X → 证据 Y → 缺口 ±N（P-029）【E1】
【A】A-12 M7 账本按失效形态分桶（形态 II 为未入分桶的独立样本，P-027 样本 ㉛）【E1】
【A】A-13 `dc_validator.py` L41 定义 `SEVEN_FIELDS = (id, type, version, status, date, depends, upstream)`；L118-120 仅校验字段**存在性**（缺则 P1），**不校验取值**【E1】
【A】A-14 `upstream` 契约语义 = **上游权威源声明**（`PLAN.md` L51）：本仓库份为权威源时置 `null`，为迁移副本时置源路径；ADR-0006 方案 B 已采纳「本仓为权威源」【E1】
【A】A-15 实测 `upstream` 填充：`spec/` 88 份中 87 为 `null`（唯一非 null = `PILOT_TASK_CARD.md`）、`adr/` 8/8 `null`、`docs/` 4/4 `null` ⇒ **100 份中 99 为 `null`**；对照 `depends:` 在 `spec/` 下 **88/88 全填**【E1】
【A】A-16 Cpp_Hub 侧 `docs/ASSERTION_EVIDENCE_FRAMEWORK.md` **无 front-matter**（L1 为标题行），以正文「⚠️ 权威源已迁移」指针行（L5）声明迁移关系【E2】
【A】A-17 `PROGRESS.md` L3 状态词表 = `pending / in-progress / blocked / done`；实测使用分布 = `done` 50 / `pending` 0 / `in-progress` 0 / `blocked` 0【E1】
【A】A-18 `PROGRESS.md` L102 以「P-009 记为 5 而非 4」的**编号手段**表达「触发驱动（不排队、等外部条件）」；含「触发」的行数 = **63**（口径 = 行数，2026-09-27 读数；原稿「59 次」经 P-050 独立 pass 机械复算证伪，见 §5.3）【E1】
【A】A-19 `DECISION_RECORD_CONTRACT` v1.1 定义八字段 + 两时点（含 `decision_maker` / `valid_from` / `valid_until`）；全仓检索三者命中 **12 文件（9 文档 + 3 session JSONL；原稿作「全为文档」，经独立 pass 证伪）**，`scripts/` **零消费**【E1】
【A】A-20 session jsonl 中 `"confidence": 0.9` 出现 153 次，分布于 33 个 session 文件【E1】
【A】A-21 CHECKLIST 条目级状态标记（「通过 / 待办 / 失败」形态）全仓 **37 行 / 9 文件**（口径 = `spec/**/*.md` 含标记行数，2026-09-27；原稿「约 30 处」经独立 pass 修正）；`repo_stats.py` L387-**394** 仅解析 PROGRESS P 号，`dc_validator.py` 四项检查均不解析 CHECKLIST 条目【E1】
【A】A-22 `adr/` 下 `status: superseded` **0 命中**（8 份 ADR 无一失效）【E1】
【A】A-23 **看板已备「什么在等」的表达机制而当前空转**：`console_gen.py` `derive_state` **6 分支** = `done`→tier 空（**首分支，短路**）/ `blocked`→`Needs Attention` / 无 session→`Needs Attention` / soft→`Ready to Verify` / `finalize`→`Ready to Verify` / else→`Recommended`（`TIER_ORDER` 三档，L79；原稿计 5 并漏 `finalize` 支，经独立 pass 校订），`Recommended` 分支调 `next_step()` 推导下一步（L414）；PROGRESS 50/50 为 `done` ⇒ 后**五**分支**不可达**，`docs/CONSOLE.md` 三档渲染 **「（无）」×3**（L7-14）、`next_step()` **不可达**；`console_gen.py` L17/L60 **I-7「只用 PROGRESS 原词、不重贴标签」**禁止视图层自救【E1】
【A】A-24 **I-7 的文本与影响面**：`DESIGN.md` L112 定义 I-7「状态输出只用 `PROGRESS` 原词（`pending`/`in-progress`/`blocked`/`done`）+ 独立派生依据列，**不得重贴标签**（禁「待你审」）」，动机 = P-042 **A-3 升格标签错配**；`derive_state` **第一参直传** `task.status`（状态**冻结**）、`basis`/`tier` 可派生；**三处「定义档位 > 可达档位」**——`derive_state` **6**→**1**、`TIER_ORDER` 3→**0**、`feature_stage` 5→**3**（实测 CONSOLE **34** feature 行：调研 **14** / 验收 **19** / 未启动 **1**、**设计 0 / 实施 0**，因制品链**降序互斥** `C` 遮蔽 `I`/`D`；**档位数与阶段分布均经独立 pass 机械复算订正**）；CONSOLE feature 表「阶段」列 3 个实际用词**均不在 PROGRESS 词表内**【E1】

> 外部证据（E3）以「（外）」标记列于 §3.4-§3.6，不占用 A 类编号（其主源为检索摘要，非本仓机械取证），详见 §7 参考文献。

## 附录 B 机读登记（B 类，12 条）

```json
[
  {"id": "B1", "claim": "Q1 是「有原语、缺语义」：fork 提供回到上游的机械通路，但缺触发判据、缺失效标记词汇、缺返工图登记", "basis": "A-2/A-3 与 A-7/A-8 并列"},
  {"id": "B2", "claim": "失效表达能力在 ADR 层与四件套层不对称，是最尖锐的结构缺口", "basis": "A-5/A-6 对比 A-7/A-8"},
  {"id": "B3", "claim": "Q2 五项能力中两项半有载体、三项空白，且空白全落在「关系」侧", "basis": "A-9/A-10/A-11/A-12 与 §3.7 矩阵"},
  {"id": "B4", "claim": "社区对 Q2 空白的解法是「图 + 量化」而非重型流程，门槛在建模不在工具部署", "basis": "§3.6 FTA 逻辑门/最小割集、CPM 拓扑序/松弛量、CBAM 效用-成本比"},
  {"id": "B5", "claim": "PROGRESS 四态实际退化为一态：「等待外部触发」无合适状态可用，被迫以编号（P-009 记为 5）与散文代偿", "basis": "A-17/A-18"},
  {"id": "B6", "claim": "PROGRESS 四态退化与 Q1「四件套无失效态」同构——状态词滞后于事实时统一退化为散文代偿", "basis": "A-17/A-18 对比 A-7/A-8"},
  {"id": "B7", "claim": "决策记录契约十字段属「僵尸契约」形态：数据已按契约写入（153 处 confidence）但零机械消费", "basis": "A-19/A-20"},
  {"id": "B8", "claim": "CHECKLIST 条目级计数是「声明 = 重数纪律」（R7）的唯一豁免区，其待办项无机械追踪必然漂移", "basis": "A-21"},
  {"id": "B9", "claim": "全仓只有「成功路径」被反复走过（done 50 / 其余 0、superseded 0），失效与阻塞侧从未被真实走过", "basis": "A-17/A-22"},
  {"id": "B10", "claim": "精确化结构性结论：本仓状态表达看似强，实际只有「完成态」一档真实可用，中间态与异常态统一退化为散文代偿", "basis": "A-17/A-22 与 §4.2"},
  {"id": "B11", "claim": "「什么在等」不是缺表达设计而是机制空转：看板三档队列与 next_step 因 done 短路 + 源层 50/50 done 而恒空，且 I-7 明文禁止视图层自救", "basis": "A-23 与 A-17"},
  {"id": "B12", "claim": "I-7 冻结状态词、仅允许派生依据/行动档，使源层退化不可被视图层自愈（唯一合法修复点在 PROGRESS）；且看板三处「定义档位 > 可达档位」同因 = 视图档位空间宽于上游取值空间，而 I-7 正是禁止重贴标签填差的那条约束", "basis": "A-23/A-24"}
]
```

## 附录 C 假设区（6 项）

- [H1] `fork` **是否已被实际用于回写**未实测——本批只取证其存在与语义，未枚举 sessions 中的 fork 产物。
- [H2] 「短期 / 长期」的**时间尺度**未定义——Azure 建议按阶段拆记录，但本仓以「批次」为时间单位的尺度换算未评估。
- [H3] 社区方法与本仓规模的**适配成本**未评估——FTA / CPM / CBAM 在单人 + LLM 规模下是否划算，需另做成本收益评估。
- [H4] PROGRESS 中「等待触发」项的**准确条数**未机械枚举——本批仅取证其存在与代偿手法（编号 / 散文），未做逐项清点。
- [H5] §3.8 三项候选（PROGRESS 状态实使用 / 决策契约校验器 / CHECKLIST 重数）的**实施成本未评估**。
- [H6] `upstream` 全 `null` 在未来**跨仓新场景**下是否需非 `null` 未评估——本批仅证明当前状态为契约正确值。
