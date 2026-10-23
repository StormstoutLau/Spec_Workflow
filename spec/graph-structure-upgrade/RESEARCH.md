# 调研文档：图结构升级与 RPC 集群接入前置调研

---

id: graph-structure-upgrade-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-10-24
depends: [ADR-0010, FWK-ASSERTION]
upstream: null

---

> **Feature**: graph-structure-upgrade（图结构升级 / RPC 集群接入的前置调研——基础、代价、收益、风险）
> **创建日期**: 2026-10-24
> **状态**: draft（本轮只出调研与 A 路径建议；不改任何代码/配置；`D:\RPC` 侧零写入）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「补充调研 本框架会接入 D盘 RPC 集群框架 图结构编排是否属于必备 如果需要使用集群执行复杂任务 / 其次 当前框架先进行补全升级 先构建完善的基础 再进行试运行升级 是否更合适 请详细分析调研」→「先落档 然后按照方案A进行补充前置调研 调研社区案例 外部锚点 实现方法 风险点等具体细节 按照吃狗粮模式执行」

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 20 | 本仓 / RPC 只读代码与文档的机械取证（E1）+ 外部锚点（E3/T2，摘要级） |
| B 推断类 | 6 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 5 | 不参与 R7 机械对账（DR-2） |
| 假设区 | 5 | 未实测项（见附录 C） |

> **取证口径**：本仓与 RPC 事实 = E1（本会话逐字读文件 / 机械枚举）；外部框架与论文 = E3/T2（RPC 图调研已收集的官方文档 / arXiv / 期刊链接，**本批未逐条回原文**）；未回原文的数字不入 A 类，正式设计前须 T1 核验。

---

## 1. 调研目标与边界

**核心问题**：

1. **本仓是否具备图结构升级的基础**？哪些边已经存在，哪些缺口？
2. **本框架接入 `D:\RPC` 集群后，图结构编排是否属于必备**？单任务、只读扇出、片间依赖、写汇聚、迭代/搜索分别怎么判？
3. **路径选择**：先补全基础再试运行，还是先上框架/全引擎？「补全」的边界是什么？
4. **代价、收益、风险**：薄图 vs 全引擎；社区案例与学术锚点给出什么判据？

**边界声明（本轮不做的事）**：

- **不改**任何代码 / 配置 / 门禁；**不新增**真值源；
- **零写入** `D:\RPC`（只读其 README / ADR / 调研 / 设计文档）；
- **不引入** LangGraph / CrewAI / AutoGen / MAF / ADK / Temporal / Airflow 等任何框架；
- 外部锚点为**摘要级 E3/T2**，不升级为 T1，不作为门禁判据；
- 本批只落 **Step 1-2**（调研 + 审查），不进入 DESIGN / IMPLEMENTATION。

---

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 结果 |
|---|---|---|
| Read / Grep | 本仓 G1 现状与 RPC G2 文档取证 | 成功（E1） |
| Read（`D:\RPC`） | RPC README、ADR-0013、图编排调研 v1.3、P3 建图语义设计 | 成功（E1，只读） |
| 既有会话（P-006 / P-050 / P-107） | LangGraph 否决先例、返工图/决策路径、研究批模板 | 成功（E2） |
| RPC 图调研的外部链接 | LangGraph / CrewAI / AutoGen / MAF / ADK / Temporal / HTPS / LeanDojo-v2 / LongCat / Gödel-Code-Prover / 一致性测试 / Build Systems à la Carte / Workflow Patterns / DSM | 复用（E3/T2，未回原文） |

> **元观察**：本批的外部锚点不是本会话新查的，而是**复用 RPC 图调研 v1.3 已收集并标注的链接**。这避免了重复检索，但也意味着**外部读数仍为 E3/T2**；正式 DESIGN 前必须做 T1 核验（见 U-4）。

### 2.2 调研范围

- **本仓 G1**：`depends` / `upstream` / DC5 / `rework-graph.json` / `DECISION_RECORD_CONTRACT` / CONSOLE 派生状态机 / `spec_runner` 线性步骤链。
- **RPC G2**：三机推理集群、D6/D7 任务卡、`split`/`decompose`、join/依赖边/迭代缺口、三资源池、P0-P4 阶梯、ADR-0013 D2/D3/D5/D6/D7。
- **Auto_Prover G3**：P3 AND-OR 超图设计（零实现、不引框架）。
- **外部**：图工作流引擎、DAG/可复现工作流、provenance、决策图、DSM、HTPS。

---

## 3. 本仓 G1 现状（E1）

**已有节点/边**：

【A】A-1 本仓规模读数（E1，2026-10-24）：P-001~P-124、39 个 feature 目录（P-125 前 38 + 本批新增 1）、8 个 ADR、29 篇 dev-log、10 个脚本、6 个 hook、M7 47 个样本。

【A】A-2 本仓已存在多类声明边：front-matter `depends` / `upstream`、DC5 版本引用、session `upstream_impact`、`rework-graph.json` 的 fork 边、`DECISION_RECORD_CONTRACT` 的关系类型。

【A】A-3 `docs/rework-graph.json` + `scripts/rework_graph_check.py` 已实现「声明 → 实测 → 对账」的返工图真值表；这是本仓最接近「图作为一等真值」的载体。

【A】A-4 CONSOLE 已派生状态机/流程图视图（Mermaid `stateDiagram` / `flowchart` / 架构图）；`spec_runner` 仍为线性 `STEP_SEQUENCE` + `--expect`，**没有 DAG 调度**。

**缺口**：统一图 schema、全局图构建器、传递闭包/影响分析、环/孤儿检测、图查询 CLI、图驱动门禁、真实依赖图视图。

**判定**：薄图基础约 **6/10**；全引擎基础约 **3/10**〔判断，C 类〕。

---

## 4. RPC G2 现状（E1：只读 `D:\RPC`）

【A】A-5 RPC 是三机本地推理集群 + D6/D7 agent 协议：`ops/cluster.py`（引擎/加载/路由）、`agent-cli.ps1`（任务卡派发/回收/复核）、`rpc_check.py`（约 50 项门禁），三层各有唯一面。

【A】A-6 RPC 已有扇出 `split` + `decompose`（跨站 round-robin A/B/C），并有真并行实测（2 片/2 站、3 片/3 站，墙钟低于串行下界）。

【A】A-7 RPC 缺三样：**join**（`SPLIT_ABORT: writable merge not supported [exit 2]`，无归并语义）、**片间依赖边**（`decompose` 是有序列表但实际并行派发，无拓扑序）、**迭代/搜索**（只有 ≤3 有界重试，无搜索树/分支预算/状态复用）。

【A】A-8 RPC 的 `$stationPool = @('A','B','C')` 硬编码；并行上界是物理量（站数 × 每站 1 本地腿），**图框架不能提高本地引擎池上界**；出网池与 Lean 池是另外两条腿。

【A】A-9 RPC 有三个资源池：① 本地引擎池（跨站各 1，受 `O-18` 内存带宽约束）；② 出网 API 池（三站独立 OpenRouter 账户，1000 请求/日/账户，20 请求/分，官方未写 per account）；③ Lean 验证池（A/B 两站，物理核 16/站，边际 0.54 GB/会话，4.7 ms/命令检查、11.7 ms/tactic）。

【A】A-10 RPC 的 P0-P4 阶梯：P0 池实测 + `$stationPool` 改「站 × 腿」；P1 `split` 汇聚语义；P2 条件分支从文档表变可机判判据；P3 AND-OR 超图 + verifier 闭环（**自研侧、零框架**）；P4 执行外壳外置（**须 ADR**）。

【A】A-11 P4 三判据（写死在 RPC 图调研 §4）：① P3 已跑通；② 能给出具体「现有表达不出来」的实例；③ 有 P3 的实测成本数据。**不接受**「项目变复杂了」这类不可机判理由。

【A】A-12 ADR-0013 D2/D3/D5：任务卡是跨边界**稳定接口**；任何升级（含图编排）只能**附加式**扩展卡、默认 fail-soft、**不得替换卡**；单例集合 = 判据本体 / `I-1` 台账 / load-gate 与槽位仲裁 / `egress`-`sensitivity` 门；图升级 = 片间依赖边 / join / 有界迭代三类**附加字段**。

【A】A-13 ADR-0013 D6/D7：各仓自编图编排 + `agent-cli` 仅作 worker 的硬前置 = 稳定 worker 契约、站级跨租户锁、`egress`/scrubber 迁 worker、台账分租户、非产出方裁决；Auto_Prover **先接受理面、编排面自研**；现在不让本框架托管它的图执行外壳。

【A】A-14 P3 设计（`D:\RPC\.trae\documents\P3-建图语义-设计方案.md`）：goal/subgoal **AND-OR 超图**（节点 = goal、边 = tactic、AND = 子目标全证才证父、OR = 同 goal 多 tactic）+ 依赖聚合 + Lean verifier 闭环 + best-first；**零实现、不引框架**，实施在 `F:\Auto_Prover`。

---

## 5. 三层图必须分开

【A】A-15 三层图的对象不同：**G1** 文档/决策依赖图（节点 = 文档/ADR/决策/返工流）；**G2** 任务执行图（节点 = 任务/片/汇聚/重试）；**G3** 证明搜索超图（节点 = goal/subgoal，边 = tactic）。三者唯一连接是**任务卡与引用键**，不是同一张图。

【A】A-16 RPC 内核**不解析图拓扑**（ADR-0013 护栏①）；图语义归租户，内核只做 worker/门禁；`I-1` 台账、load/槽位、`egress` 门必须单例。

**判定**：把三层混成一张「大一统图」会同时制造**双真相源**（同一拓扑两处定义）、**领域语义错位**（内核替租户决定 join/冲突/搜索）、**判据漂移**（门随租户实现）。〔判断，C 类〕

---

## 6. 外部案例与外部锚点（E3/T2，摘要级）

【A】A-17 RPC 图调研的外部能力对照（官方文档声称、无独立评测）：LangGraph 1.2/1.2.9、CrewAI Flows、AutoGen/AG2（已进入维护模式）、MS Agent Framework 1.0、Google ADK 2.0 均具备条件边/循环/扇出/持久化/人审/子图中的多数项；Temporal 是通用 durable-execution，非 agent 原生，常与图框架叠用。

【A】A-18 外部已知坑（E3）：独立一致性契约测试（arXiv:2608.03836）报 LangGraph 1.2.9 在真实 `SIGKILL` 后会**重跑已记录的工作**（at-least-once），且多框架 resume 语义互相矛盾；checkpoint/rollback 五类失效可致**重复副作用**（arXiv:2608.29381）；checkpoint 无界增长需 prune；本地模型工具调用质量影响条件边（`llama-server` 需 `--jinja`，小模型 5+ 工具误报率 >35%）。

【A】A-19 学术锚点（E3）：HTPS（arXiv:2205.11491）逐字给出「hypergraph / tactics as edges / subgoals as nodes」；*Build Systems à la Carte*（arXiv:1809.02942）把构建系统 = 任务图 + 调度器 + 重建器；*Workflow Patterns*（2003）列 20+ 控制流模式；DSM（Steward 1981 / Eppinger & Browning 2012）用依赖矩阵表达依赖。

【A】A-20 可复现工作流锚点（E3）：Snakemake（Bioinformatics 2012）/ Nextflow（Nature Biotechnology 2017）以显式 DAG 支持部分重跑与溯源，但需要 DSL/运行时；W3C PROV / RO-Crate 1.1 提供 provenance 图与制品元数据标准；Sandve et al. 2013 的十条可复现规则强调依赖与溯源。

**关键启示**：
- 图框架提供的是**可替换的执行外壳**（扇出/汇聚/恢复/人审），**不提供领域语义与搜索策略**；
- 全框架的引入会带来**新栈/运行时/迁移/运维**成本，且 checkpointer 重放会污染证据链；
- **任务图/依赖矩阵**本身可以用 JSON/邻接表 + 只读校验实现，不需要图数据库或运行时。

---

## 7. 实现方法（A 路径）

### 7.1 S0 契约层（Layer-0）

- **任务卡附加字段**（全部可选、fail-soft、存量卡行为不变）：`depends_on`（片间依赖边）、`join`（汇聚声明）、`iter_budget`（迭代上界）、`join_policy`（冲突/归并策略）、`graph_version`（契约版本）。
- **语义归租户**：join 怎么归并、冲突听谁的、迭代停止条件——由卡声明，内核**只判「有没有声明 / 是否越界」**，不解析内部语义。
- **任务卡仍是唯一接口**：不替换卡、不新增第二真值源；图拓扑只作为卡的附加字段。

### 7.2 S1 最小工具层（Layer-0/1，只读）

- **图构建器**：从卡/front-matter/`rework-graph.json`/`DECISION_RECORD_CONTRACT` 生成派生 `graph.json`（**不是真值源**）。
- **校验器**：环检测、孤儿检测、影响闭包（`graph impact <node>`）、依赖拓扑序；**不调度、不执行、不接运行时**。
- **接入点**：`spec_runner` 可选子命令或独立只读脚本；零第三方依赖；不新增 hook（先验证再决定是否接门禁）。

### 7.3 S2 Pilot（一个真实复杂任务）

- **候选 1**：只读扇出 + 汇聚（RPC 当前 `split` 支持只读，join 用卡声明的 reducer 在租户侧归并）。
- **候选 2**：Auto_Prover P3 的真实形式化输入（AND-OR 超图 + Lean verifier），在 `F:\Auto_Prover` 自研侧跑通。
- **测量**：墙钟、失败模式、重放次数、人工裁断时间、是否真的用到图查询；**没有测量就不进入 S3**。

### 7.4 S3 决策（P1/P2/P3 或 P4）

- 若 Pilot 证明「片间依赖 / 写汇聚 / 迭代」是真实缺口：RPC 做 P1（join 语义）/ P2（条件分支可机判）/ P3（AND-OR 超图），或租户自持。
- **P4 只在三判据全满足后评估**：P3 跑通 + 具体不可表达实例 + 实测成本；且须另立 ADR、解决双真相源与重放污染。

### 7.5 明确不做

- ❌ 在 Spec_Workflow 建图引擎 / 图数据库 / 调度器；
- ❌ 用图框架替换任务卡（破 D2）；
- ❌ 让 RPC 内核解析图拓扑（破护栏①）；
- ❌ 在 P3/P4 判据满足前引入 LangGraph 等新栈；
- ❌ 没有真实负载就固化拓扑（对空气设计外壳）。

---

## 8. 风险点

| ID | 风险 | 机制 | 处置 |
|---|---|---|---|
| R1 | **双真相源** | 拓扑在卡里一份、框架/租户代码里再一份 | 卡 = 唯一接口；内核不解析拓扑；拓扑只以附加字段表达 |
| R2 | **任务卡被替换** | 图框架直接取代卡派发 | 只允许附加式扩展；fail-soft；存量卡行为不变 |
| R3 | **checkpointer 重放** | 崩溃后 at-least-once 重跑已记录工作 | 复核早于入链；checkpointer 不得接管产物写出；长搜索先用自研 |
| R4 | **条件边判错** | 本地模型工具调用质量不足（`--jinja` / 小模型多工具误报） | 条件分支先做可机判判据（P2），不把自由文本判据当边 |
| R5 | **门随租户漂移** | 多 master 下 `egress`/scrubber/槽位门各持一套 | 门留 worker 侧单例；站级跨租户锁；台账单写者 |
| R6 | **对空气设计** | 没有真实复杂任务负载就固化拓扑 | 先 Pilot；P4 三判据之一 = 具体不可表达实例 |
| R7 | **big-bang** | 一次性重写派发/编排 | strangler-fig；S0→S1→S2→S3 逐段 |
| R8 | **graph theater** | 图建好了但没人查 | 只做被真实查询驱动的图能力；无查询需求不建 |
| R9 | **证据链污染** | 重放/多写者/产物写出被框架接管 | `I-1` 单写者；digest 对账；复核时序 |
| R10 | **硬编码** | `$PROJECTS` / `$stationPool` 写死关键路径 | 先数据化；P0 改「站 × 腿」 |
| R11 | **敏感外发** | 图/卡被外仓编排器带出 | `local-only` 门留 worker；fail-closed |
| R12 | **过早抽象** | 五层图强行统一 | G1/G2/G3 分开；按层建最小图 |

---

## 9. 结论与分档

**结论**〔判断，C 类〕：

1. **图结构编排对「复杂任务的契约」是必备的，对「框架」不是必备的**：单任务/只读扇出不需要；片间依赖/写汇聚/迭代搜索需要，但应是任务卡附加字段 + 租户语义，不是新引擎。
2. **本仓具备薄图基础（约 6/10），不具备全引擎基础（约 3/10）**：G1 的边已大量存在，但缺统一 schema、全局构建、影响闭包、环检测、图查询。
3. **「先补全基础，再试运行」更合适，但补全 = 契约 + 最小语义 + 最小工具；试运行 = 一个真实复杂任务 pilot**。全框架留到 RPC P4 三判据满足之后。
4. **三层图分开**：Spec_Workflow 做 G1 + G2 契约/证据/验收；RPC 做 G2 执行（P1/P2/P3）；Auto_Prover 做 G3 领域语义。

**分档**：

| 档 | 内容 | 判定 |
|---|---|---|
| **A 薄图 + 最小工具 + pilot** | S0 契约、S1 只读图构建/校验、S2 一个真实 pilot、S3 再决策 | **推荐** |
| **B 全框架/全引擎** | LangGraph/Airflow/Temporal 直接接管编排 | 否决（成本/重放/卡替换/双真相源；P4 三判据未满足） |
| **C 不升级** | 维持现有异质边 + 人工影响扫描 | 基线；复杂任务只能串行/人工拼接 |

**C 类决策**：

【C】C-1 采用 **A 路径**（契约 + 最小工具 + pilot），否决 B 全引擎与 C 不升级。

【C】C-2 任务卡是**唯一接口**；图字段附加式、fail-soft、不替换卡。

【C】C-3 **领域语义归租户**（join/冲突/搜索）；RPC 内核不解析拓扑。

【C】C-4 **P4 框架**只在三判据满足后评估，且须另立 ADR。

【C】C-5 **本仓不建图引擎**；只做 G1 + G2 契约/证据/验收；图构建/校验为只读最小工具。

---

## 10. 未决项

| ID | 未决项 | 触发 / 下一步 |
|---|---|---|
| U-1 | 首个真实复杂任务 pilot 未选定（Auto_Prover P3 或 Spec_Workflow 多阶段批） | 用户裁决 / 真实负载出现 |
| U-2 | 任务卡图字段的命名、类型、`join_policy` 词表未定 | DESIGN 段 |
| U-3 | 图构建/校验器归属（Spec_Workflow vs RPC）未定 | DESIGN 段 + ADR-0013 边界 |
| U-4 | 外部锚点为 E3/T2 摘要级，T1 原文核验未做 | 正式 DESIGN 前逐条回原文 |
| U-5 | pilot 的实际成本（墙钟/失败率/重放次数）未测 | S2 pilot |

---

## 11. 参考文献

**本仓（E1）**：
- [rework-graph/RESEARCH.md](../rework-graph/RESEARCH.md)
- [rework-and-decision-paths/RESEARCH.md](../rework-and-decision-paths/RESEARCH.md)
- [academic-writing-workflow/RESEARCH.md](../academic-writing-workflow/RESEARCH.md) §9 / §12 / H1 / H4
- [project-console/RESEARCH.md](../project-console/RESEARCH.md)
- [decision-schema/DESIGN.md](../decision-schema/DESIGN.md)
- [DECISION_RECORD_CONTRACT.md](../../docs/DECISION_RECORD_CONTRACT.md)
- [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) / [ADR-0007](../../adr/ADR-0007-unified-document-contract.md)

**RPC（E1，只读）**：
- `D:\RPC\README.md`（三机推理集群 / D6/D7）
- `D:\RPC\adr\ADR-0013-跨仓库使用本框架的准入与派发分界.md`（D2/D3/D5/D6/D7）
- `D:\RPC\docs\research\2026-10-01_图结构编排升级潜力与机群算力利用调研.md`（v1.3，P0-P4）
- `D:\RPC\.trae\documents\P3-建图语义-设计方案.md`（AND-OR 超图，零实现）

**外部（E3/T2，摘要级，未回原文）**：
- LangGraph / CrewAI Flows / AutoGen / MS Agent Framework / Google ADK / Temporal（RPC 图调研 §2.1 链接）
- HTPS, Lample et al., arXiv:2205.11491
- LeanDojo-v2, https://leandojo.org/leandojo
- LongCat-Flash-Prover, arXiv:2603.21065；Gödel-Code-Prover, arXiv:2603.19329
- 一致性契约测试, arXiv:2608.03836；checkpoint/rollback, arXiv:2608.29381
- *Build Systems à la Carte*, arXiv:1809.02942
- *Workflow Patterns*, van der Aalst et al., 2003
- DSM, Steward 1981 / Eppinger & Browning 2012
- Snakemake, Bioinformatics 2012；Nextflow, Nature Biotechnology 2017
- W3C PROV；RO-Crate 1.1；Sandve et al., PLoS Comput Biol 2013

---

## 附录 A：A 类事实清单

| ID | 事实 | 等级 |
|---|---|---|
| A-1 | 本仓规模读数（P-124 批次 / 39 feature（含本批新增） / 8 ADR / 29 dev-log / 10 脚本 / 6 hook / 47 样本） | E1 |
| A-2 | 本仓已有 depends/upstream/DC5/session/rework/decision 多类边 | E1 |
| A-3 | rework-graph.json + rework_graph_check.py 已实现返工图真值表与对账 | E1 |
| A-4 | CONSOLE 派生状态机；spec_runner 仍为线性 STEP_SEQUENCE | E1 |
| A-5 | RPC 三机推理集群 + D6/D7 三层单一面 | E1 |
| A-6 | RPC 已有 split/decompose 扇出与真并行实测 | E1/E2 |
| A-7 | RPC 缺 join / 片间依赖边 / 迭代搜索 | E1 |
| A-8 | RPC stationPool 硬编码；并行上界是物理量 | E1 |
| A-9 | RPC 三资源池与 Lean 吞吐读数 | E1 |
| A-10 | RPC P0-P4 阶梯 | E1 |
| A-11 | P4 三判据 | E1 |
| A-12 | ADR-0013 D2/D3/D5（卡接口 / 单例 / 附加字段） | E1 |
| A-13 | ADR-0013 D6/D7（worker 契约 / Auto_Prover 先接受理面） | E1 |
| A-14 | P3 AND-OR 超图设计（零实现、不引框架） | E1 |
| A-15 | G1/G2/G3 三层图对象不同 | E1 |
| A-16 | RPC 内核不解析拓扑；门留 worker | E1 |
| A-17 | 外部框架能力对照（LangGraph/CrewAI/AutoGen/MAF/ADK/Temporal） | E3 |
| A-18 | 外部已知坑（重放 / checkpoint / 本地工具调用） | E3 |
| A-19 | 学术锚点（HTPS / Build Systems à la Carte / Workflow Patterns / DSM） | E3 |
| A-20 | 可复现工作流与 provenance 锚点（Snakemake/Nextflow/PROV/RO-Crate/Sandve） | E3 |

## 附录 B：B 类推断（机读登记）

```json
{"id": "B1", "claim": "单任务/只读扇出不需要图编排；片间依赖/写汇聚/迭代搜索才需要。", "basis": "A-6/A-7"}
{"id": "B2", "claim": "全框架不是必备；图契约 + 租户语义 + RPC 执行是当前最优。", "basis": "A-10/A-11/A-12"}
{"id": "B3", "claim": "G1/G2/G3 必须分开，否则双真相源/领域语义错位/内核漂移。", "basis": "A-15/A-16"}
{"id": "B4", "claim": "先补全再试运行 = 契约 + 最小语义 + 最小工具 + 一个真实 pilot，不是先建全引擎。", "basis": "A-10/A-11"}
{"id": "B5", "claim": "Spec_Workflow 应做 G1 + G2 契约/证据/验收，不做 G2 执行引擎。", "basis": "A-12/A-13/A-16"}
{"id": "B6", "claim": "Auto_Prover P3 是 G3 的正确试点，但需真实形式化输入，当前 D6 链负载未满足。", "basis": "A-13/A-14"}
```

## 附录 C：C 类决策与假设区

**C 类决策** = C-1 采用 A 路径 / C-2 任务卡唯一接口且附加式 / C-3 领域语义归租户 / C-4 P4 须三判据 + ADR / C-5 本仓不建图引擎。

**假设区**：

- [H1] 首个真实复杂任务 pilot 未选定（Auto_Prover P3 或 Spec_Workflow 多阶段批）。
- [H2] 任务卡图字段的命名、类型、`join_policy` 词表未定。
- [H3] 图构建/校验器归属（Spec_Workflow vs RPC）未定。
- [H4] 外部锚点为 E3/T2 摘要级，T1 原文核验未做。
- [H5] pilot 的实际成本（墙钟/失败率/重放次数）未测。
