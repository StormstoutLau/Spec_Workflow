# 调研文档：图结构升级与 RPC 集群接入前置调研

---

id: graph-structure-upgrade-RESEARCH
type: design
version: 1.2
status: draft
date: 2026-10-24
depends: [ADR-0010, FWK-ASSERTION]
upstream: null

---

> **Feature**: graph-structure-upgrade（图结构升级 / RPC 集群接入的前置调研——基础、代价、收益、风险、缓解）
> **创建日期**: 2026-10-24
> **修订**: v1.2（2026-10-24，P-127：**补充 U-6/U-7 专项调研**——§13 给出拦截率/误报率的故障矩阵 + 双样本 + 基率 + 置信区间测量方案；§14 给出 P4 前置三件 V-EXPORT / V-FENCE / V-LEASE 的验收判据；新增 11 条外部来源（T1 8 / T2 3）；A 26→37 / B 10→15 / C 5→7 / H 7→9）
> **修订**: v1.1（2026-10-24，P-126：**补充风险点解决办法**——§8 按「预防 / 检测 / 响应 / 机械核验 / 残余」五段重写；新增 §12 外部引文 T1 核验，订正 1 处 arXiv ID 误引；A 20→26 / B 6→10 / H 5→7）
> **状态**: draft（本轮只出调研与缓解建议；不改任何代码/配置；`D:\RPC` 侧零写入）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「补充调研 本框架会接入 D盘 RPC 集群框架 图结构编排是否属于必备 如果需要使用集群执行复杂任务 / 其次 当前框架先进行补全升级 先构建完善的基础 再进行试运行升级 是否更合适 请详细分析调研」→「先落档 然后按照方案A进行补充前置调研 调研社区案例 外部锚点 实现方法 风险点等具体细节 按照吃狗粮模式执行」→「补充调研风险点的解决办法」

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 37 | 本仓 / RPC 只读代码与文档的机械取证（E1）+ 外部锚点（v1.1 起：6 条回原文 T1，其余 E3/T2） |
| B 推断类 | 15 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 7 | 不参与 R7 机械对账（DR-2） |
| 假设区 | 9 | 未实测项（见附录 C） |

> **取证口径（v1.2 起）**：本仓与 RPC 事实 = E1（逐字读文件 / 机械枚举）；外部框架与论文 = **T1（arXiv abs 原文 / 官方文档 / 会议页 / API 参考）或 T2（官方页片段或书目级，未回全文）/ E3（二手转述）**。v1.1 核验 6 条（§12）：2 条升 T1（A-23 / A-24）、3 条仅确认 ID/标题（A-26）、1 条 ID 误引订正（A-25）。v1.2 追加 11 条（§13.2 / §14.4）：8 条 T1（A-27 / A-28 / A-29 / A-32 / A-33 / A-35 / A-36 / A-37）、3 条 T2（A-30 / A-31 / A-34），未发现新引文缺陷。未回原文的条目不进 A 类。

---

## 1. 调研目标与边界

**核心问题**：

1. **本仓是否具备图结构升级的基础**？哪些边已经存在，哪些缺口？
2. **本框架接入 `D:\RPC` 集群后，图结构编排是否属于必备**？单任务、只读扇出、片间依赖、写汇聚、迭代/搜索分别怎么判？
3. **路径选择**：先补全基础再试运行，还是先上框架/全引擎？「补全」的边界是什么？
4. **代价、收益、风险与缓解**：薄图 vs 全引擎；每条风险的最小解决办法是什么、能否机械核验？

**边界声明（本轮不做的事）**：

- **不改**任何代码 / 配置 / 门禁；**不新增**真值源；
- **零写入** `D:\RPC`（只读其 README / ADR / 调研 / 设计文档）；
- **不引入** LangGraph / CrewAI / AutoGen / MAF / ADK / Temporal / Airflow 等任何框架；
- 外部锚点 v1.1/v1.2 已对 17 条做 T1/T2 核验（§12 / §13.2 / §14.4）；其余仍为 **E3**，不作为门禁判据；
- 本批只落 **Step 1-2**（调研 + 审查），不进入 DESIGN / IMPLEMENTATION。

---

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 结果 |
|---|---|---|
| Read / Grep | 本仓 G1 现状与 RPC G2 文档取证 | 成功（E1） |
| Read（`D:\RPC`） | RPC README、ADR-0013、图编排调研 v1.3、P3 建图语义设计 | 成功（E1，只读） |
| 既有会话（P-006 / P-050 / P-107） | LangGraph 否决先例、返工图/决策路径、研究批模板 | 成功（E2） |
| RPC 图调研的外部链接 | LangGraph / CrewAI / AutoGen / MAF / ADK / Temporal / HTPS / LeanDojo-v2 / LongCat / Gödel-Code-Prover / 一致性测试 / Build Systems à la Carte / Workflow Patterns / DSM | 复用（E3/T2） |
| **WebFetch / WebSearch（v1.1 起）** | 逐条回原文核验（arXiv abs / 官方文档 / 会议页） | 成功（v1.1 6 条 + v1.2 11 条；2 条升 T1、1 条误引订正、3 条 T2） |
| **arXiv API（v1.1 新增）** | 标题精确检索（`ti:"Build Systems a la Carte"`） | 成功：`totalResults = 0`（无 arXiv 版） |
| **WebSearch（v1.1 新增）** | 会议页交叉核验（ICFP 2018 / ACM DL） | 成功（DOI 10.1145/3236774） |

> **元观察（v1.1 更新）**：v1.0 的外部锚点全部复用 RPC 图调研的链接、未回原文；v1.1 的回原文核验**发现 1 处 arXiv ID 误引**（`1809.02942` 指向一篇细胞自动机论文，而 *Build Systems à la Carte* 无 arXiv 版）——说明「复用二手链接」本身即引文幻觉的入口，凡进入正文的外部 ID 都应做一次「ID/标题/作者」三连核验（B10）。

### 2.2 调研范围

- **本仓 G1**：`depends` / `upstream` / DC5 / `rework-graph.json` / `DECISION_RECORD_CONTRACT` / CONSOLE 派生状态机 / `spec_runner` 线性步骤链。
- **RPC G2**：三机推理集群、D6/D7 任务卡、`split`/`decompose`、join/依赖边/迭代缺口、三资源池、P0-P4 阶梯、ADR-0013 D2/D3/D5/D6/D7。
- **Auto_Prover G3**：P3 AND-OR 超图设计（零实现、不引框架）。
- **外部**：图工作流引擎、DAG/可复现工作流、provenance、决策图、DSM、HTPS、恢复语义一致性。

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

【A】A-14 P3 设计（`D:\RPC\.trae\documents\P3-建图语义-设计方案.md`）：goal/subgoal **AND-OR 超图**（节点 = goal、边 = tactic，AND = 子目标全证才证父、OR = 同 goal 多 tactic）+ 依赖聚合 + Lean verifier 闭环 + best-first；**零实现、不引框架**，实施在 `F:\Auto_Prover`。

---

## 5. 三层图必须分开

【A】A-15 三层图的对象不同：**G1** 文档/决策依赖图（节点 = 文档/ADR/决策/返工流）；**G2** 任务执行图（节点 = 任务/片/汇聚/重试）；**G3** 证明搜索超图（节点 = goal/subgoal，边 = tactic）。三者唯一连接是**任务卡与引用键**，不是同一张图。

【A】A-16 RPC 内核**不解析图拓扑**（ADR-0013 护栏①）；图语义归租户，内核只做 worker/门禁；`I-1` 台账、load/槽位、`egress` 门必须单例。

**判定**：把三层混成一张「大一统图」会同时制造**双真相源**（同一拓扑两处定义）、**领域语义错位**（内核替租户决定 join/冲突/搜索）、**判据漂移**（门随租户实现）。〔判断，C 类〕

---

## 6. 外部案例与外部锚点（E3/T2，摘要级）

【A】A-17 RPC 图调研的外部能力对照（官方文档声称、无独立评测）：LangGraph 1.2/1.2.9、CrewAI Flows、AutoGen/AG2（已进入维护模式）、MS Agent Framework 1.0、Google ADK 2.0 均具备条件边/循环/扇出/持久化/人审/子图中的多数项；Temporal 是通用 durable-execution，非 agent 原生，常与图框架叠用。

【A】A-18 外部已知坑（E3）：独立一致性契约测试（arXiv:2608.03836）报 LangGraph 1.2.9 在真实 `SIGKILL` 后会**重跑已记录的工作**（at-least-once），且多框架 resume 语义互相矛盾；checkpoint/rollback 五类失效可致**重复副作用**（arXiv:2608.29381）；checkpoint 无界增长需 prune；本地模型工具调用质量影响条件边（`llama-server` 需 `--jinja`，小模型 5+ 工具误报率 >35%）。

【A】A-19 学术锚点（E3）：HTPS（arXiv:2205.11491，**E3 转述；摘要未含「hypergraph / tactics as edges」措辞，见 §12**）被称为以 hypergraph 表达证明搜索；*Build Systems à la Carte*（**ICFP 2018，DOI 10.1145/3236774；v1.0 的 arXiv:1809.02942 为误引，v1.1 已订正，见 §12**）把构建系统 = 任务图 + 调度器 + 重建器；*Workflow Patterns*（2003）列 20+ 控制流模式；DSM（Steward 1981 / Eppinger & Browning 2012）用依赖矩阵表达依赖。

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

## 8. 风险点与解决办法

> **v1.1 重写说明**：v1.0 的 §8 只有一句「处置」；本版把每条风险拆成 **预防（P）/ 检测（D）/ 响应（R）/ 机械核验点（V）/ 残余风险（X）** 五段，并标注落点阶段（S0 契约 / S1 只读工具 / S2 pilot / P4 框架外置）。**判据：没有 D 段的缓解不可核验；没有 V 点的缓解只是口号**（B7）。

### 8.1 横切原则（M1-M5）

- **M1 单一真值源 + 派生视图可复算**：拓扑只存于任务卡；`graph.json` 是派生视图，带 `source_digest` 与生成器版本，头部 `DO NOT EDIT`，只读、不手改、不新增第二份拓扑。
- **M2 附加式契约 + fail-soft + 契约测试**：新字段全部可选；未知字段忽略并告警、缺失字段走默认；升级前后跑同一组卡 fixture，存量卡行为逐字节不变（A-12 D2/D5）。
- **M3 幂等 + 消费闸 + digest 去重**：`run_id + step_id + effect_id` 作幂等键；产物写出与状态提交分离；**共享存储原子 claim**（消费闸）决定唯一执行者；重放后按产物 digest 去重。
- **M4 provenance-first**：每次执行落「输入 / 输出 / 判据版本 / 写者」四元组，且可由第三方复算；未记录的外部效应必须显式登记（A-24 的失效面）。
- **M5 安全侧 fail-closed、兼容侧 fail-soft**：`local-only` / `egress` / 单写者冲突一律拒绝；卡字段缺失 / 图版本未知一律降级并告警；每条缓解自带触发条件与「未激活副作用 0」（ADR-0010）。

### 8.2 逐风险解决办法

【A】A-21 ADR-0013 D7 给出五条**可机判**护栏（E1）：① 卡 = 唯一接口（拓扑只能附加式写入，内核不解析内部语义）② 门留 worker 侧（每站一份且总在执行路径上）③ 合规判据只在本框架一处定义（租户只消费、不自带）④ 入链时序写进编排（复核早于入链；checkpointer 不得接管产物写出）⑤ 把漂移变成可机判（复用既有 `dialect` / `id-census`，不新造机制）。

【A】A-22 ADR-0013 D3 的单例集合（E1）：判据本体 / `I-1` 台账单写者 / load-gate 与槽位仲裁 / `egress`-`sensitivity` 门（`local-only → REJECT exit 4`，**无覆盖通道**）；多写者 ⇒ 事件流分叉、计数不可复算；fork 旧 wrapper 即丢门 ⇒ 未发表语料外发（`O-16` 先例）。

【A】A-23 Resume Contract（arXiv:2608.03836v3，T1 摘要）：持久化层应满足六性质——prefix continuation / effect exactly-once / fork determinism / checkpoint validity / consume-once / recovery determinism；实测 LangGraph 1.2.9 **同一 API 上「中断 = exactly-once、崩溃 = at-least-once」**，并会静默持久化 schema 非法状态；CrewAI 1.15.2 重跑已完成的有副作用方法；并发 resume 时 **k 个进程可让同一 gated effect 触发 k 次（40 单元中 36 个饱和为 1.0，且跨主机）**；REMIT 参考实现的修复点 = **在读路径加 opt-in 消费闸，在共享存储中原子 claim，只服务一个竞争者、其余在任何节点执行前拒绝**。

【A】A-24 Checkpoint/Rollback 安全研究（arXiv:2608.29381v1，T1 摘要）：**正确回滚 ≠ 安全恢复**——被忠实恢复的 checkpoint 可能续上一个「状态、假设与外部效应从未在任何合法历史中共存」的执行；五类失效跨「内部状态不完整/不一致、外部依赖过期、非确定性重放、未记录的外部效应」；三种端到端攻击含**重复付款**；根因 = 恢复的状态与安全续行所需依赖之间的缺口。

**R1 双真相源**
- **P（S0）**：拓扑只在卡附加字段；`graph.json` 为派生视图（`source_digest` + 生成器版本 + `DO NOT EDIT`）；不手改、不新增第二份拓扑。
- **D（S1）**：每次构建复算 `source_digest`；输入未变而产物变 ⇒ 报漂移；`graph_version` 不在支持集 ⇒ fail-soft 告警并跳过图校验。
- **R**：停用派生视图，回退卡直读；不自动修图。
- **V**：`source_digest` 可复算；同一输入两次构建逐字节一致；产物无手写时间戳/随机序。
- **X**：框架内部若持第二拓扑且不可导出 ⇒ D 失效（X2）；P4 前置「拓扑导出 API」。
- **依据**：A-21 护栏①⑤；A-19（构建系统 = 任务图 + 调度器 + 重建器）。

**R2 任务卡被替换**
- **P（S0）**：卡 schema 版本化；解析 fail-soft（未知字段忽略 + 告警，缺失字段走默认）；框架只**消费**卡，不拥有卡。
- **D（S0/S1）**：四组契约 fixture（无字段 / 部分字段 / 非法字段 / 未知字段）+ 旧卡回归集；解释语义变更必须递增 schema 版本。
- **R**：回退上一解析器；存量卡零改动。
- **V**：四组 fixture 全绿；旧卡产出与升级前逐字节一致（除新增可选字段）。
- **X**：框架升级改变默认值解释 ⇒ 锁版本 + 升级前跑回归集。
- **依据**：A-12 D2/D5；A-23 的「契约可机检」思路。

**R3 checkpointer 重放**
- **P（S2/P4）**：中断与崩溃**分开测试**；checkpointer 不接管产物写出；`run_id + step_id + effect_id` 幂等键；产物 digest 去重；**共享存储原子 claim**，未 claim 成功者在任何节点执行前被拒。
- **D（S2）**：崩溃注入（step 边界 `SIGKILL`）+ 并发 resume（k 进程同时 resume 同一中断）两类测试；重放后产物 digest 集合不变；重复副作用计数 = 0。
- **R**：出现重放 ⇒ 停用框架 checkpointer，退回自研 ≤3 有界重试。
- **V**：同输入重放的产物 digest 集合相等；消费闸「一赢家、其余在任何节点执行前拒绝」；中断场景 exactly-once、崩溃场景至少不产生重复副作用。
- **X**：已发出的外部副作用不可回滚（X1）；框架内部隐式重试不可见（X2）。
- **依据**：A-23（六性质 + 36/40 饱和 + 读路径消费闸）；A-24（未记录外部效应/重复付款）。

**R4 条件边判错**
- **P（S2）**：条件边判据必须**可机判**（枚举 / 正则 / JSON schema / 退出码）；自由文本只作「建议」；条件函数纯函数化；非法输出走 default（fail-closed 到人工）。
- **D（S2）**：每次判定落「理由码 + 判据版本」；统计 fallback 率与非法输出率；工具调用 schema 校验；`llama-server` 必须 `--jinja`；5+ 工具的模型不用于条件边。
- **R**：连续 N 次 fallback ⇒ 停用该边；非法输出 ⇒ 人工复核。
- **V**：同输入同输出（纯函数测试）；非法输出必走 default；工具调用 JSON schema 通过。
- **X**：模型版本漂移（X3）⇒ 回归集 + 锁版本。
- **依据**：A-18（`--jinja` / 5+ 工具 >35%）；A-21 护栏⑤（复用 `dialect`）；A-24（非确定性重放）。

**R5 门随租户漂移**
- **P（P4 前置）**：门留 worker 单例；租户只声明策略、不得实现门；台账单写者；站级跨租户锁。
- **D（S2/P4）**：门实现哈希清单逐站一致；台账主键唯一 + 双写检测。
- **R**：哈希不一致 ⇒ 拒绝启动（fail-closed）；台账分叉 ⇒ 停派发 + 人工合并。
- **V**：哈希清单一致；台账主键唯一；每次 egress 带 sensitivity 决策记录。
- **X**：多 master 分区 ⇒ fencing token / 租约（X4，D4 未裁）。
- **依据**：A-21 护栏②③；A-22 单例集合；A-23 的共享存储原子 claim（同构）。

**R6 对空气设计**
- **P（S0/S2）**：S2 pilot 先于拓扑固化；图能力默认关闭；P4 三判据。
- **D（S1）**：图查询调用计数；30 天零查询 ⇒ 下线候选；每个图字段须有真实用例引用。
- **R**：下线未使用能力；保留字段但停用校验。
- **V**：调用日志可复算；ADR-0010 三问「未激活副作用 0」。
- **X**：pilot 代表性不足（X5）。
- **依据**：A-11 P4 三判据；ADR-0010。

**R7 big-bang**
- **P（S0→S3）**：strangler-fig；每段独立可回退；影子运行（旧派发 vs 新派发只读比对）。
- **D（S2/S3）**：每段上线前差异清单；回退演练。
- **R**：任一段失败只回退该段，不连带回退前段。
- **V**：每段有回退点；无破坏性 schema 变更；影子差异 = 0 或已解释。
- **X**：双跑期成本翻倍（短期）。
- **依据**：A-12 D2（卡不替换）；S0→S3 分段本身。

**R8 graph theater**
- **P（S1）**：只做被真实查询驱动的图能力；图构建默认关（lazy）。
- **D（S1）**：图产物读/写比；视图层是否有消费者。
- **R**：零读取 ⇒ 停建；已建 ⇒ 标记 deprecated。
- **V**：ADR-0010 三问；调用计数。
- **X**：隐性需求未被发现（X5）。
- **依据**：ADR-0010；A-11。

**R9 证据链污染**
- **P（S1/S2）**：`I-1` 单写者；产物 digest 入链；复核早于入链；框架不得接管产物写出；未记录外部效应必须显式登记。
- **D（S2）**：链上 digest vs 重算 digest；写者身份；「未记录效应」标记；恢复时校验外部依赖时点（A-24）。
- **R**：digest 不符 ⇒ 该 run 不入链 + 人工复核；写者非单例 ⇒ fail-closed。
- **V**：digest 可复算；每事件带 writer id；「无未记录效应」声明可对照副作用清单审计。
- **X**：框架缓存/隐式重试（X2）；恢复后的状态与外部依赖可能从未共存（A-24）⇒ 恢复时须重新验证依赖时点。
- **依据**：A-23 effect exactly-once；A-24 五类失效；A-21 护栏④；A-22 `I-1` 单写者。

**R10 硬编码**
- **P（P0）**：`$PROJECTS` / `$stationPool` 数据化；配置单一源；站池改「站 × 腿」。
- **D（S1）**：硬编码扫描（路径 / 池 / 端口）；配置漂移对账；启动断言。
- **R**：发现硬编码 ⇒ 登记排期；不得在硬编码上加分支。
- **V**：配置 schema 校验；启动时配置 = 真值源；扫描清单 0 命中。
- **X**：环境差异。
- **依据**：A-8 / A-9（E1 读数）；ADR-0013 D7 前置①。

**R11 敏感外发**
- **P（P4 前置）**：`local-only` 门留 worker；fail-closed；图/卡只含引用键不含敏感原文；egress 白名单。
- **D（S2）**：每次出网请求带 sensitivity 决策；缺失即拒；出网审计日志。
- **R**：违规 ⇒ 阻断 + 事件登记；已发出内容不可回滚 ⇒ 通报。
- **V**：`local-only` 请求数 = 0；缺失决策记录的请求 = 0。
- **X**：模型输出侧泄露（X6）。
- **依据**：A-22（无覆盖通道 + `O-16` 先例）。

**R12 过早抽象**
- **P（S0/S1）**：G1/G2/G3 分开；图 schema 带 `layer` 字段；跨层边默认拒绝；按层建最小图。
- **D（S1）**：跨层边扫描；同一节点出现在两层 ⇒ 报错。
- **R**：回退按层独立图；层间只留引用键。
- **V**：`layer` 必填；跨层边需显式豁免清单。
- **X**：层边界随需求演化。
- **依据**：A-15 / A-16；I-1（层间唯一连接是引用键）。

### 8.3 落点与验证归属

| 措施 | 落点 | 验证方式 | 责任侧 |
|---|---|---|---|
| 卡附加字段 + fail-soft 解析 | S0 | 四组卡 fixture（R2-V） | 本仓 |
| `graph.json` + `source_digest` | S1 | 同输入两次构建逐字节一致（R1-V） | 本仓 |
| 环 / 孤儿 / 跨层边检测 | S1 | selftest + 真实仓复跑（R12-V） | 本仓 |
| 幂等键 + 消费闸 | S2 / P4 | 崩溃注入 + 并发 resume（R3-D） | 租户 / RPC |
| 条件边纯函数 + default 分支 | S2 | 回归集 + 工具 schema（R4-V） | 租户 |
| 单写者台账 + 门哈希 | RPC 侧（D3） | 主键唯一 + 哈希清单（R5-V） | RPC |
| 拓扑导出 API | P4 前置 | 导出可解析（R1-X） | 框架选型 ADR |
| fencing token / 租约 | P4（多 master） | 分区演练（R5-X） | RPC |
| 影子运行 | S2 / S3 | 差异清单（R7-V） | 本仓 + RPC |

### 8.4 残余风险登记

- **X1 已发出的外部副作用不可回滚**：出网 API 调用、已投递消息、已写外部库——只能补偿 / 登记 + 事前 `egress` 门（A-24 的「未记录外部效应」）。
- **X2 框架内部状态不可导出**：若框架持有第二拓扑或隐式重试且不可观测，R1-D 与 R3-D 失效 ⇒ P4 前置「拓扑导出 + 重试可见」。
- **X3 模型版本漂移**：本地模型升级会改变条件边判定 ⇒ 需回归集与锁版本；当前未建（H6）。
- **X4 多 master 网络分区**：台账单写者与门单例在分区下需 fencing token / 租约；RPC D4 形态未裁。
- **X5 pilot 代表性不足**：一个真实任务不能证明泛化；只承诺「该任务可表达」，不承诺「所有复杂任务可表达」。
- **X6 模型输出侧敏感泄露**：输入侧 `egress` 门管不到模型输出；需输出侧 scrubber + 事后审计。

---

## 9. 结论与分档

**结论**〔判断，C 类〕：

1. **图结构编排对「复杂任务的契约」是必备的，对「框架」不是必备的**：单任务/只读扇出不需要；片间依赖/写汇聚/迭代搜索需要，但应是任务卡附加字段 + 租户语义，不是新引擎。
2. **本仓具备薄图基础（约 6/10），不具备全引擎基础（约 3/10）**：G1 的边已大量存在，但缺统一 schema、全局构建、影响闭包、环检测、图查询。
3. **「先补全基础，再试运行」更合适，但补全 = 契约 + 最小语义 + 最小工具；试运行 = 一个真实复杂任务 pilot**。全框架留到 RPC P4 三判据满足之后。
4. **三层图分开**：Spec_Workflow 做 G1 + G2 契约/证据/验收；RPC 做 G2 执行（P1/P2/P3）；Auto_Prover 做 G3 领域语义。
5. **缓解措施按阶段落地**（v1.1 新增）：S0/S1 只做预防与只读检测；R3/R4/R9/R11 的运行时检测留 S2 pilot；R1 的拓扑导出、R5 的 fencing 属 P4 前置——**未到阶段的缓解只登记，不预先实施**（否则即 ADR-0010 的「未激活副作用」与 R8 的 graph theater）。
6. **U-6/U-7 已从「无判据」转为「有方案 / 判据、实现待阶段」**（v1.2 新增）：U-6 采用「故障矩阵 + 双样本 + 基率 + 置信区间」（§13）；U-7 采用 V-EXPORT / V-FENCE / V-LEASE 三件验收（§14）；二者仍 open，但不再是不可裁的空项。

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
【C】C-6 **U-6 测量口径** = 故障语料 + 干净语料双样本，报告 TPR / FPR / 基率 / Wilson 95% CI，并预注册最小故障矩阵单元；**禁止只报单一准确率或只报 TPR**（§13）。
【C】C-7 **U-7 前置判据** = V-EXPORT + V-FENCE + V-LEASE 三件**同时满足**；框架自称「有图 API / 有 checkpointer / 有 leader election」不作数，须逐条机械验收（§14）。

---

## 10. 未决项

| ID | 未决项 | 触发 / 下一步 |
|---|---|---|
| U-1 | 首个真实复杂任务 pilot 未选定（Auto_Prover P3 或 Spec_Workflow 多阶段批） | 用户裁决 / 真实负载出现 |
| U-2 | 任务卡图字段的命名、类型、`join_policy` 词表未定 | DESIGN 段 |
| U-3 | 图构建/校验器归属（Spec_Workflow vs RPC）未定 | DESIGN 段 + ADR-0013 边界 |
| U-4 | 未回原文的外部锚点仍为 E3/T2（v1.1 已核 6 条，余 6 类未核） | 正式 DESIGN 前逐条回原文 |
| U-5 | pilot 的实际成本（墙钟/失败率/重放次数）未测 | S2 pilot |
| U-6 | **缓解措施的实际拦截率 / 误报率未测**（方案已定于 §13；崩溃注入、并发 resume、条件边回归集均未建） | S2 pilot 按 §13.3 故障矩阵实测；读数入 pilot 报告 |
| U-7 | **P4 前置实现未做**（判据已定于 §14：V-EXPORT / V-FENCE / V-LEASE） | P4 立项 ADR 逐条机械验收；不满足则不采用框架 |

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

**外部（v1.1 已 T1 核验）**：
- Resume Contract: arXiv:2608.03836v3（六性质 / at-least-once / 消费闸）——**T1**
- Checkpoint & rollback security: arXiv:2608.29381v1（五类失效 / 重复付款）——**T1**
- HTPS: Lample et al., arXiv:2205.11491（ID / 标题 / 作者已核；**结构表述仍为 E3**，摘要未含「hypergraph / tactics as edges」原文）
- LongCat-Flash-Prover: arXiv:2603.21065（ID / 标题已核；数字仍 E3）
- Gödel-Code-Prover: arXiv:2603.19329v3（ID / 标题已核；数字仍 E3）
- *Build Systems à la Carte*: Mokhov / Mitchell / Peyton Jones, **ICFP 2018, DOI 10.1145/3236774**（**无 arXiv 版；v1.0 的 arXiv:1809.02942 为误引，已订正**）

**外部（v1.2 U-6/U-7 专项）**：
- Axelsson 2000, *The Base-Rate Fallacy and the Difficulty of Intrusion Detection*（ACM TISSEC）——**T1**
- ALICE / BOB, OSDI 2014, *All File Systems Are Not Created Equal*——**T1**
- FoundationDB Simulation and Testing（官方文档）——**T1**
- *Principles of Chaos Engineering*（2019 版）——**T2**
- Jia & Harman 2011, *An Analysis and Survey of the Development of Mutation Testing*（IEEE TSE 37(5):649-678, DOI 10.1109/TSE.2010.62）——**T2（书目级）**
- OpenLineage Object Model（官方文档）——**T1**
- LangChain `draw_mermaid` API reference——**T1**
- Chubby OSDI 2006, *The Chubby lock service for loosely-coupled distributed systems*（§2.4 sequencer）——**T2（官方页片段）**
- Kubernetes Lease（官方文档）——**T1**
- etcd Lease（官方文档）——**T1**
- Gray & Cheriton 1989, *Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency*（SOSP）——**T1**

**外部（仍 E3/T2，未回原文）**：
- LangGraph / CrewAI Flows / AutoGen / MS Agent Framework / Google ADK / Temporal（RPC 图调研 §2.1 链接）
- LeanDojo-v2, https://leandojo.org/leandojo
- *Workflow Patterns*, van der Aalst et al., 2003
- DSM, Steward 1981 / Eppinger & Browning 2012
- Snakemake, Bioinformatics 2012；Nextflow, Nature Biotechnology 2017
- W3C PROV；RO-Crate 1.1；Sandve et al., PLoS Comput Biol 2013

---

## 12. 外部引文核验（v1.1）

### 12.1 方法

- **T1 定位**：对正文实际使用的 6 条外部引文，逐条取 arXiv `abs` 页原文（WebFetch），只把**摘要可见的事实**升级为 T1；摘要未含的表述**不升级**。
- **ID 三连核验**：标题 / 作者 / 年份与正文声称一致；对无 arXiv 版者用 arXiv API 标题精确检索 + 会议页交叉核验。
- **不核验项**：未在正文承担判据的文献保持 E3/T2，登记为 U-4。
- **v1.2 追加（U-6/U-7 专项）**：另有 11 条来源单独核验（T1 8 / T2 3），方法同「回原文取摘要或官方页」；结果见 §13.2 / §14.4。本轮未发现新引文缺陷，故不新增 M7 样本。

### 12.2 结果

| 引文 | 核验动作 | 结果 | 处置 |
|---|---|---|---|
| Build Systems à la Carte | arXiv `abs/1809.02942` + API `ti:"Build Systems a la Carte"` + ICFP 2018 会议页 | **ID 不成立**：`1809.02942` = *Cellular automata as convolutional neural networks*（Gilpin, Phys. Rev. E 100, 032402）；标题检索 `totalResults = 0` ⇒ 该文无 arXiv 版；会议页确认 = ICFP 2018，DOI `10.1145/3236774` | **P2 订正**：删除 arXiv ID，改引 ICFP 2018 DOI；A-19 / §11 同步 |
| Resume Contract | arXiv `abs/2608.03836v3` | 成立：六性质 + LangGraph 中断 exactly-once / 崩溃 at-least-once + 36/40 并发消费饱和 + 读路径消费闸（REMIT） | 升 **T1**（A-23） |
| Checkpoint/Rollback | arXiv `abs/2608.29381v1` | 成立：正确回滚 ≠ 安全恢复 + 五类失效 + 三攻击（含重复付款） | 升 **T1**（A-24） |
| HTPS | arXiv `abs/2205.11491` | **ID / 标题 / 作者成立**；摘要**不含**「hypergraph / tactics as edges / subgoals as nodes」 | 保持 **E3** 标注；不据摘要改写 A-19 |
| LongCat-Flash-Prover | arXiv `abs/2603.21065` | ID / 标题 / 作者成立 | 保持 **E3**（未用其数字） |
| Gödel-Code-Prover | arXiv `abs/2603.19329v3` | ID / 标题成立（原文拼写 `Goedel`） | 保持 **E3**（未用其数字） |

### 12.3 结论

【A】A-25 引文 ID 误引事实（T1，2026-10-24）：arXiv:1809.02942 的标题为 *Cellular automata as convolutional neural networks*（Gilpin），与 *Build Systems à la Carte* 无关；arXiv API 标题精确检索 `Build Systems a la Carte` 返回 `totalResults = 0`；该文实际为 ICFP 2018 论文（DOI 10.1145/3236774）。

【A】A-26 三条既有 ID 核验通过（T1，2026-10-24）：arXiv:2205.11491（HTPS，Lample et al.）、arXiv:2603.21065（LongCat-Flash-Prover）、arXiv:2603.19329（Goedel-Code-Prover）的 ID / 标题 / 作者均与正文声称一致；但 HTPS 的结构表述不在摘要中，故其证据级维持 E3。

---


## 13. U-6：缓解措施的拦截率 / 误报率怎么测

### 13.1 为什么「测过了」不成立

- **只报拦截率 = 不可复核**：拦截率（TPR = TP/(TP+FN)）与误报率（FPR = FP/(FP+TN)）必须成对出现；只有 TPR 无法回答「正常运行时会不会误报」。
- **基率支配**：用户真正关心的是 P(故障 | 告警) = TPR·π / (TPR·π + FPR·(1−π))，其中 π 是故障基率；π 很小时 FPR 是限制因素——这正是 Axelsson 的结论（A-27）。因此报告必须同时给 **π、TPR、FPR**，否则「99% 拦截率」在低基率下仍可能几乎全是误报。
- **双样本缺一不可**：没有干净语料（无故障运行）⇒ FPR 无定义；没有故障语料（注入）⇒ TPR 无定义。只跑其中一种，结论都是半截。
- **缓解分两类，测法不同**：
  - **预防型**（R1/R2/R10/R12）：没有「告警」动作，只能测「违规实例数 = 0」+ 用种子违规测「校验器逃逸率」（变异测试思路，A-31）。
  - **检测型**（R3/R4/R5/R9/R11）：有告警/阻断动作，才可测 TPR / FPR / P(故障|告警)。

### 13.2 社区与学术案例

【A】A-27 Axelsson 2000（T1，PDF 原文）：对一组合理假设，**误报率是入侵检测系统性能的限制因素**；由于基率谬误，要让贝叶斯检测率 P(Intrusion|Alarm) 达到可观值，必须把误报率压到（有时不可达的）极低水平。⇒ 本仓报告「缓解有效率」时必须同时给基率与 FPR。

【A】A-28 ALICE / BOB（T1，OSDI 2014 摘要）：对 11 个广泛使用的系统（数据库、KV 存储、版本控制、分布式系统、虚拟化）分析应用级崩溃一致性协议，共发现 **60 个崩溃漏洞**；方法 = 先测持久化属性（BOB），再**违反属性生成 crash states**，跑应用恢复并判定一致性（ALICE）。⇒ 故障注入应按「属性 × crash point」枚举单元，而不是随机重启。

【A】A-29 FoundationDB Simulation（T1，官方文档）：**确定性**单线程模拟整个集群；夜间运行**数万次**模拟，累计约 **1 万亿 CPU 小时**等效；模拟网络、机器、数据中心级故障，真实/模拟时间约 **10:1**；确定性使失败可完美重放。⇒ 先确定性模拟，再真机注入；确定性 harness 每单元一次即可复现。

【A】A-30 Chaos Engineering 四步（T2，官方原则页）：① 定义稳态（可测输出）② 对控制组与实验组做同一假设 ③ 注入真实世界事件 ④ 找稳态差异以证伪假设；要求**最小爆炸半径**与**持续自动化**。⇒ 实验必须有对照组与稳态指标，不能在「没有基线」的情况下注入。

【A】A-31 变异测试（T2，书目级：Jia & Harman, IEEE TSE 37(5):649-678, 2011, DOI 10.1109/TSE.2010.62）：用变异体被测试集杀死的比例衡量测试集的故障发现能力；等价变异体是已知偏差。⇒ 可用于估计「条件边回归集」与「校验器」的拦截强度，但须报告等价变异体处理口径。

### 13.3 三层测量设计

**L1 契约 / 预防层（S0/S1，可先做）**

- 对象：R1 双真相源、R2 卡替换、R10 硬编码、R12 跨层边。
- 语料：四组卡 fixture（无字段 / 部分字段 / 非法字段 / 未知字段）+ 种子违规（手写一份「故意错误」的图/卡，测校验器是否捕获）。
- 指标：违规实例数（必须 0）、种子逃逸数（必须 0）、digest 复算一致率。
- 报告：`runs` / `violations` / `seeded_mutants` / `escaped`；不适用 TPR/FPR（无告警动作）。

**L2 故障注入层（S2，需 pilot）**

- 对象：R3 重放、R9 证据链污染、R5 门漂移、R11 敏感外发。
- **R3 故障矩阵（建议维度）**：
  - crash point：写产物前 / 写产物中 / 写后入链前 / 入链后（4）
  - 并发 resume：1 / 2 / 4 进程（3）
  - checkpoint 有效性：合法 / schema 非法（2）
  - 外部效应：无 / 幂等 API / 非幂等 API（3）
  - ⇒ 名义 72 单元；**预注册最小子集**（例如 24 单元）与每单元运行次数，禁止事后挑单元。
- 判据（每单元）：产物 digest 集合不变、重复副作用计数 = 0、消费闸一赢家、未记录外部效应 = 0。
- **R9**：注入「重放 / 双写者 / 入链后改写 / 未记录效应」四类故障 + 干净语料；指标 = 四类各自检出率、每 100 次干净运行的误报数。
- **R5/R11**：分区 / 暂停旧 holder / `local-only` 请求注入；判据 = 旧 token 写入被拒数 = 全部尝试、`local-only` 出网 = 0。
- 工具（社区案例，T2）：容器级 Chaos Mesh / LitmusChaos；网络 `tc netem` 或 Toxiproxy；进程 `SIGKILL` harness；分布式历史检查 Jepsen 风格。**工具只作执行手段，判据仍以本仓契约为准。**
- 确定性 harness 每单元 1 次即可复现；含 LLM 的单元须每单元 ≥30 次、锁模型版本与温度、报告 Wilson 95% CI。

**L3 条件边回归层（S2）**

- 对象：R4 条件边判错。
- 语料：正例（应走 A/B）、负例（不应触发）、边界（非法输出 / 超时 / 工具缺失 / 参数畸形）。
- 指标：TPR、FPR、fallback 率、非法输出率；用变异测试（翻阈值 / 删 default / 改枚举）估计回归集强度（A-31）。
- 报告 Wilson 95% CI；**禁止只报 accuracy**（基率陷阱，A-27）。

### 13.4 报告模板（拟议，不落脚本 / 不新增真值源）

- 预防型单元：`{"risk":"R2","suite":"card-fixtures","runs":N,"violations":0,"seeded_mutants":M,"escaped":0}`。
- 检测型单元：`{"risk":"R3","suite":"crash-matrix","cells_total":72,"cells_run":24,"tp":..,"fn":..,"fp":..,"tn":..,"tpr":..,"fpr":..,"base_rate":..,"ci":"wilson95","clean_runs":..,"fault_runs":..,"harness":"deterministic|llm","as_of":"YYYY-MM-DD"}`。
- **纪律**：模板只是形态；数值必须由 harness 机械生成，不得手填（R7 同构）。本批**不建 harness、不写账本、不接门禁**。

### 13.5 最小第一步与触发

- **现在可做（S1 内）**：R2 四组 fixture + R4 三类语料 + 种子违规集；纯测试资产，不改运行时。
- **S2 pilot 才做**：R3/R9 崩溃注入与并发 resume、R5/R11 分区与外发注入、R4 回归集实测。
- **U-6 保持 open 直到 S2 出读数**；读数入 pilot 报告，**不进 M7**（M7 记审查轮，不记可靠性读数）。

---

## 14. U-7：P4 前置判据（拓扑导出 / fencing / 租约）

### 14.1 V-EXPORT：拓扑导出 API 六条

1. **机器可读 schema**（JSON / JSONL / Protobuf），且有版本号；**Mermaid 渲染文本不算**。
2. **完整**：节点、边、条件边、子图、join 节点；每节点带 `layer` 与语义类型。
3. **运行期真值**：导出 = 实际执行拓扑（含运行时选择的分支），不是仅设计期声明。
4. **只读、无副作用**：运行中与结束后都可调用，不改变状态。
5. **稳定 ID + 可复算 digest**：同一 run 两次导出逐字节一致。
6. **版本协商**：未知字段 fail-soft；schema 版本不匹配 ⇒ 拒绝托管。

【A】A-33 反例（T1）：LangGraph 的 `draw_mermaid(nodes, edges, ...)` 是一个渲染函数，返回 **Mermaid 字符串**；`get_graph()` 返回结构（T2 二手页）。⇒ **有图 API ≠ 满足 V-EXPORT**：若只能导出图片/文本，无法做拓扑对账与 digest 校验。

【A】A-32 正例参考（T1）：OpenLineage 对象模型把 **设计期**（`JobEvent` / `DatasetEvent`）与 **运行期**（`RunEvent`）分开，Run 内记录输入/输出 Dataset；另有 `lineage` job facet 显式记录数据流边（T2 官方页片段）。它不是控制流拓扑，但给出了「设计期声明 × 运行期观测」双事件的导出形态，可借用其分层，不直接采用其本体。

### 14.2 V-FENCE：fencing token 六条

1. 每次获锁生成**单调 token**（generation / epoch）。
2. **资源侧校验 token**，拒绝旧 token；不信任「客户端声称仍持锁」。
3. token 与锁**同一共识存储 / 同一单调序列**派生。
4. token 随每次写请求携带；资源记录已见最大 token。
5. **分区 / 暂停演练**：旧 holder 恢复后写入必须被拒。
6. 验收读数：旧 token 写入尝试 **全部被拒**（拒绝数 = 尝试数）。

【A】A-34 案例（T2）：Chubby 的锁携带 **lock generation number**；客户端把它作为 **sequencer** 传给受保护资源，接收方应校验该 sequencer（OSDI'06 官方页 §2.4 片段；本批未回全文，标 T2）。

### 14.3 V-LEASE：租约五条 + 与 fencing 的区别

1. **TTL + 续租 + 到期释放**；租约到期后资源不得再接受旧 holder 写入（需 V-FENCE 配合）。
2. **holder identity + 单调版本**（如 `holderIdentity` / `renewTime` / `resourceVersion`）。
3. **时钟偏斜上界** + 单调时钟；租约长度 > 续租间隔 + 偏斜。
4. **无双 holder 窗口**：任意时刻至多一个 holder；旧 holder 暂停后恢复不得写。
5. **验收读数**：到期释放、续租成功、旧 holder 写入拒绝三项均有记录。

【A】A-35 案例（T1）：Kubernetes `coordination.k8s.io` Lease 以 `holderIdentity` / `leaseDurationSeconds` / `renewTime` 表达持有者与续租，用于 leader election 与 node heartbeat；**K8s Lease 本身不做资源侧 token 校验**，所以它满足 V-LEASE 的一部分，不自动满足 V-FENCE。
【A】A-36 案例（T1）：etcd 的 lease 有 TTL、keepalive 流、键绑定租约；TTL 到期后租约及其键被删除。
【A】A-37 理论（T1）：Gray & Cheriton 1989 的 lease 是**时间型缓存一致性机制**，短租约把非拜占庭失败的影响限制在租约期内；**它不是 fencing token**。

> **关键区分（B15）**：lease ≠ fencing。只做租约、不做资源侧 token 校验，旧 holder 在暂停后恢复仍可写入——这正是 V-FENCE 要单独存在的原因。把「有 leader election / 有 lease」当成「已 fencing」是常见误读。

### 14.4 三件关系与裁定

- **P4 托管执行外壳的前置 = V-EXPORT + V-FENCE + V-LEASE 三件同时满足**；缺一不采用。
- 框架自称「有 checkpointer / 有图 API / 有 leader election」**不作数**；须逐条机械验收。
- 验收动作：导出 schema 解析 + 两次导出 digest 一致；分区 / 暂停演练 + 旧 token 拒绝计数；租约到期 / 续租读数。
- 与 P-125 的 P4 三判据关系：三判据回答「**要不要**外置」，本节回答「**外置前必须满足什么**」；两者叠加，不互相替代。


### 14.5 社区案例对照

| 来源 | 提供什么 | 不提供什么 | 对本仓的含义 |
|---|---|---|---|
| OpenLineage（A-32） | 设计期 / 运行期双事件；输入输出 Dataset | 控制流、条件边、join | 借「双事件」形态，不直接采用本体 |
| LangGraph `draw_mermaid`（A-33） | Mermaid 文本渲染 | 稳定 schema、运行期真值 | 反例：有图 API 仍需另验 V-EXPORT |
| Chubby sequencer（A-34） | 单调 sequencer + 接收方校验 | 开源实现、TTL 细节 | V-FENCE 判据原型 |
| Kubernetes Lease（A-35） | holderIdentity / renewTime / TTL | 资源侧 token 校验 | V-LEASE 原型，仍需 V-FENCE |
| etcd lease（A-36） | TTL / keepalive / 键绑定 | fencing token | V-LEASE 实现参考 |
| Gray & Cheriton（A-37） | 时间型 lease 理论 | fencing | 纠正「lease = fencing」误读 |

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
| A-21 | ADR-0013 D7 五条可机判护栏（卡唯一接口 / 门留 worker / 判据单点 / 入链时序 / 漂移可机判） | E1 |
| A-22 | ADR-0013 D3 单例集合（I-1 单写者 / load 与槽位 / egress 门无覆盖通道） | E1 |
| A-23 | Resume Contract 六性质 + 并发消费饱和 + 读路径消费闸 | T1 |
| A-24 | Checkpoint/Rollback 五类失效 + 三攻击（含重复付款） | T1 |
| A-25 | arXiv:1809.02942 误引（实为 CA-as-CNN；标题检索 0） | T1 |
| A-26 | 三条既有 ID 核验通过（2205.11491 / 2603.21065 / 2603.19329） | T1 |
| A-27 | Axelsson 2000：误报率是 IDS 性能限制因素；基率谬误（T1） | T1 |
| A-28 | ALICE/BOB：11 系统 60 崩溃漏洞；属性违反→crash states（T1） | T1 |
| A-29 | FoundationDB Simulation：确定性全集群模拟；夜间数万次；~1 万亿 CPU 小时等效（T1） | T1 |
| A-30 | Chaos Engineering 四步：稳态→假设→注入→证伪；最小爆炸半径（T2） | T2 |
| A-31 | 变异测试：变异体杀死率衡量测试集故障发现能力（T2 书目级） | T2 |
| A-32 | OpenLineage：设计期/运行期双事件 + 输入输出 Dataset（T1） | T1 |
| A-33 | LangGraph draw_mermaid 返回 Mermaid 字符串，非 schema（T1） | T1 |
| A-34 | Chubby sequencer：lock generation number + 接收方校验（T2 官方页片段） | T2 |
| A-35 | Kubernetes Lease：holderIdentity / renewTime / leaseDurationSeconds（T1） | T1 |
| A-36 | etcd lease：TTL / keepalive / 键绑定 / 到期删除（T1） | T1 |
| A-37 | Gray & Cheriton 1989：时间型 lease；非 fencing token（T1） | T1 |

## 附录 B：B 类推断（机读登记）

```json
{"id": "B1", "claim": "单任务/只读扇出不需要图编排；片间依赖/写汇聚/迭代搜索才需要。", "basis": "A-6/A-7"}
{"id": "B2", "claim": "全框架不是必备；图契约 + 租户语义 + RPC 执行是当前最优。", "basis": "A-10/A-11/A-12"}
{"id": "B3", "claim": "G1/G2/G3 必须分开，否则双真相源/领域语义错位/内核漂移。", "basis": "A-15/A-16"}
{"id": "B4", "claim": "先补全再试运行 = 契约 + 最小语义 + 最小工具 + 一个真实 pilot，不是先建全引擎。", "basis": "A-10/A-11"}
{"id": "B5", "claim": "Spec_Workflow 应做 G1 + G2 契约/证据/验收，不做 G2 执行引擎。", "basis": "A-12/A-13/A-16"}
{"id": "B6", "claim": "Auto_Prover P3 是 G3 的正确试点，但需真实形式化输入，当前 D6 链负载未满足。", "basis": "A-13/A-14"}
{"id": "B7", "claim": "缓解须五段（预防/检测/响应/机械核验/残余）；缺检测段或核验点的缓解不可核验。", "basis": "A-21/A-22"}
{"id": "B8", "claim": "崩溃语义下「恰好一次」不能由单一框架自证，须消费闸 + 单写者 + 产物 digest 三件共同保证。", "basis": "A-23/A-24/A-22"}
{"id": "B9", "claim": "缓解落点必须绑定阶段；运行时缓解未经 pilot 不得宣称有效。", "basis": "A-11/A-21"}
{"id": "B10", "claim": "进入正文的外部 ID 必须机械可解析；标题级检索为 0 时不得保留 arXiv ID。", "basis": "A-25/A-26"}
{"id": "B11", "claim": "拦截率与误报率必须双样本（故障+干净）+ 基率 + 置信区间；只报 TPR 或单一 accuracy 不可复核。", "basis": "A-27/A-30"}
{"id": "B12", "claim": "预防型缓解用「违规数 0 + 变异逃逸率」，检测型缓解才用 TPR/FPR；两者不可混测。", "basis": "A-28/A-31"}
{"id": "B13", "claim": "P4 前置 = V-EXPORT + V-FENCE + V-LEASE 三件同时满足；框架自称能力不作数。", "basis": "A-32/A-33/A-34/A-35/A-36"}
{"id": "B14", "claim": "拓扑导出必须是机器可读 schema；Mermaid 渲染文本不满足 V-EXPORT。", "basis": "A-33/A-32"}
{"id": "B15", "claim": "lease ≠ fencing；租约单独不能阻止旧 holder 恢复后写入。", "basis": "A-37/A-34"}
```

## 附录 C：C 类决策与假设区

**C 类决策** = C-1 采用 A 路径 / C-2 任务卡唯一接口且附加式 / C-3 领域语义归租户 / C-4 P4 须三判据 + ADR / C-5 本仓不建图引擎。

**假设区**：

- [H1] 首个真实复杂任务 pilot 未选定（Auto_Prover P3 或 Spec_Workflow 多阶段批）。
- [H2] 任务卡图字段的命名、类型、`join_policy` 词表未定。
- [H3] 图构建/校验器归属（Spec_Workflow vs RPC）未定。
- [H4] 未回原文的外部锚点仍为 E3/T2（v1.1 已核 6 条）。
- [H5] pilot 的实际成本（墙钟/失败率/重放次数）未测。
- [H6] 缓解措施的实际拦截率 / 误报率未测（S2 才可测）。
- [H7] 崩溃注入与并发 resume 未做（S2 才可测）。
- [H8] 故障矩阵的最小单元数与每单元运行次数未预注册（S2 前定）。
- [H9] P4 候选框架的导出 API / fencing / lease 未实测（P4 验收）。
