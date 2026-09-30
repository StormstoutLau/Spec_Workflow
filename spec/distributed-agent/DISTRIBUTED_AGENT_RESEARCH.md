# 调研文档：分布式 Agent 执行——三机推理集群上的工作流扩展（P-039）

---
id: distributed-agent-RESEARCH
type: design
version: 1.4
status: in-review
date: 2026-09-10
depends: [SPEC-PROCESS, ADR-0010, community-ecosystem-RESEARCH, spec-runner-DESIGN]
upstream: null
---

> **Feature**: 分布式 Agent 执行（把本仓 10 步工作流从"单机单会话顺序执行"扩展为"跨三机异构集群执行"的可行性调研）
> **创建日期**: 2026-09-10
> **状态**: in-review（审查中）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「当前有推理工作站集群 3 台 amd strix halo 工作站 参考 D:\RPC 假设当前工作流需要扩展为分布式 agent 执行 如何实现 参考调研社区优秀案例 执行调研」
> **参考先例**: P-036 promptfoo-first-run / P-037 deepeval-arm（懒加载评估）、P-018 community-ecosystem（候选池 + ADR-0010 三问首用）
> **边界声明**: 本批 = **调研批（Step 1-2）**，产出候选裁定与分层登记；**不实施**（ADR-0010 触发驱动 + 端点实测不可达，见 §2.3）。
> **v1.1 补充调研（用户指令「补充调研 假设工作流的每一个步骤由工作站的编程agent CLI执行 甚至每个agent都嵌套微工作流机制 在不考虑吞吐效率情况下是否可行 收益 代价是什么 社区 学术界 是否有案例分析」）**: 新增 **§7 补充调研——工作流每步 agent 化 × 微工作流嵌套**（两子命题 P-a/P-b 拆分裁决）——**9 条新 A**（A-14 Claude Code 嵌套子代理规格与默认关闭 / A-15 RAH 学术正面案例 / A-16 RLM 上下文外置 / A-17 深度参数跨工具分歧 + opencode #18100 递归退化实证 / A-18 MAST 失败分类学 / A-19 复利误差数学与实证 / A-20 错误级联与消息层治理 / A-21 opencode 扇出实证边界 / A-22 四重硬约束）+ **B5/B6** + **C-4** + **H4**；断言 **A 13→22 / B 4→6 / C 3→4 / H 3→4**（附录 A/B/C 同步）；原 §7 参考文献顺延 **§8**；§0 统计表同步。
> **v1.2 补充调研（用户指令「补充调研 假设做某种降级处理 主控站负责任务派发 审核 工作站的agent CLI只做单项任务 且强制要求提供决策-证据链 是否可行」）**: 新增 **§8 补充调研——降级设计 P-c**（主控站派发+审核 / 工作站单项任务 / 强制决策-证据链）——**8 条新 A**（A-23 本仓决策-证据链机械可验证部分 / A-24「每步恰一条 decision」hook 级强制 / A-25 集群任务卡 accept 可执行判据 + `.agent-run.json` 契约 / A-26 review--peer 分层与 O-24 断点① / A-27 CoT 不忠实实证 / A-28 AgentGuard+in-toto+SLSA+Sigstore+Signet 同构 / A-29 IETF SCITT AI Agent Execution Profile / A-30 W3C PROV 责任关系 + Astra Decision Lineage）+ **B7/B8** + **C-5** + **H5**；断言 **A 22→30 / B 6→8 / C 4→5 / H 4→5**（附录 A/B/C 同步）；原 §8 参考文献顺延 **§9**；§0 统计表同步。
> **v1.3 补充调研（用户指令「深入补充调研前置问题 然后分析 P-c 方案下的主控站与工作站的具体交互协议」）**: 新增 **§9 三条前置的深入调研**（锚点化 / 判据前置 / 机械优先——各给出协议级标准与量化证据）+ **§10 P-c 主控站↔工作站交互协议**（六相状态机 P0 立契→P1 领取→P2 执行→P3 回收→P4 验证（L1 机械 / L2 语义）→P5 裁决登记；三种信封；失败处置矩阵；与既有标准映射；三条设计红线）——**12 条新 A**（A-31 内容导出身份 + 摘要绑定 / A-32 Kettle TEE 证明 / A-33 IETF SEP + 真实世界哈希绑定实例 / A-34 预注册范式 / A-35 PACT VTC 判据前置 / A-36 certify-or-abstain 量化 / A-37 Asimov 双门 / A-38 机械优先的工程量化 / A-39 机械前置门禁解静默错误 / A-40 AIDP 委派生命周期 / A-41 ACP 协调原语集 / A-42 交接契约六要素）+ **B9/B10** + **C-6** + **H6**；断言 **A 30→42 / B 8→10 / C 5→6 / H 5→6**（附录 A/B/C 同步）；原 §9 参考文献顺延 **§11**；§0 统计表同步。
> **v1.4 跨仓观察项登记（用户裁决「RPC 是未来分布式 agent 调度统一基座，A 表未闭环问题暂时只登记」；**零代码改动**、**不推进**）**: 新增 **§4.5 跨仓观察项：`D:\RPC` 作为未来分布式 agent 调度统一基座 + 其未闭环问题登记**——把该**定位**与**四项未闭环事项**入册为**上游对接面**：① **D7-CC #3（相对根 / 归一化）**已裁「相对根 = 相对 runDir、外壳注入、不新造 root 字段」但**未改代码**（state 仍 `todo`）⇒ **已裁待实现**；② **D7-CC #4** 为 `O-123` **仅剩**待裁项（`needs_decision` 7→6）⇒ **待裁**；③ **U4×3 + U5×2（5 条暂缓）**⇒ **待选路线**（站内卡〔需起引擎〕或人工 public 摘要）；④ **索引「叶子节点」缺口**（`inventory/untested-index.yaml` 已建 + 双向对账已进仓，但**叶子条目无消费者**、`spec-untested` 只判节存在性与非空）⇒ **无消费者**。新增 **A-43**（跨仓实录，**E2——来源 = 跨仓会话记忆逐条摘要，未经跨仓源码直读**，并**如实标注两处未锚定推断**）/ **B11**（RPC 未闭环四项与 P-c 三条前置**同源**：皆「承诺未固化 / 无消费者」）/ **C-7**（**只登记不推进**：不代管上游未闭环项、**不在本仓建 P 行 / 不开实施批 / 不新增门禁**，并给三条触发条件）/ **H7**（RPC 侧**实际落地形态未实测**——本项证据等级**低于** A-51/A-52 的「读源码 + 实跑」标准）；断言 **42A+10B+6C+6H → 43A+11B+7C+7H**（附录 A/B/C 同步）；**边界** = 不修改 `D:\RPC` 任何文件 / 零代码 / 零新增 P 行 / 不新增门禁。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 43 | A-1~A-13 社区案例（A2A / durable execution / 编排模式 / 异构验证 / 同源偏差 / Crucible / Arbiter / SDD / exo / 本仓接口 / 三硬约束 / 集群基建 / 端点不可达）· A-14~A-22 嵌套与每步 agent 化（Claude Code 规格 / RAH / RLM / 深度分歧与递归退化 / MAST / 复利误差 / 错误级联 / opencode 扇出边界 / 四重硬约束）· A-23~A-30 降级设计（决策-证据链机械部分 / hook 级强制 / 集群 accept 契约 / review--peer 与 O-24 / CoT 不忠实 / AgentGuard·in-toto·Sigstore / IETF SCITT / W3C PROV + Lineage）· **A-31~A-42 三条前置 + 协议层**（A-31 内容导出身份 + 摘要绑定 / A-32 Kettle TEE 证明 / A-33 IETF SEP + 真实世界哈希绑定 / A-34 预注册范式 / A-35 PACT VTC / A-36 certify-or-abstain 量化 / A-37 Asimov 双门 / A-38 机械优先工程量化 / A-39 机械前置门禁解静默错误 / A-40 AIDP 委派生命周期 / A-41 ACP 协调原语 / A-42 交接契约六要素）（A-1~13 见 §2.3/§3；A-14~22 见 §7；A-23~30 见 §8；A-31~42 见 §9） · **A-43 v1.4 跨仓实录**（§4.5：`D:\RPC` 四项未闭环事项实录（D7-CC #3 已裁待实现 / D7-CC #4 待裁 / U4×3+U5×2 待选路线 / 索引叶子节点无消费者）+ 台账 4 项在开，**E2——来源 = 跨仓会话记忆逐条摘要，未经跨仓源码直读**） |
| B 推断类 | 11 | B1 最高价值=异构验证物理化 / B2 事件流已是 durable 实例 / B3 A2A 价值在词汇非运行时 / B4 并行粒度=feature / B5 两子命题收益不对称 / B6 本仓 P-b 净收益为负 / B7 P-c 最同构最可行 / B8 唯一失败模式=证据链文本化 / **B9 三条前置是本仓已有机制的显式化** / **B10 三前置共同机理=把事后不可验证的判断前移为事前可机械核对的承诺** / **B11 v1.4 跨仓同源**（§4.5：RPC 四项未闭环与 P-c 三条前置**同源**——皆「承诺未固化 / 无消费者」，故 P-c 落地时应把 RPC 侧索引的消费者位点一并纳入、不另建第二套对账）（附录 B） |
| C 判断类 | 7 | C-1 分层裁定 / C-2 优先级=异构验证先行 / C-3 止于调研不实施 / C-4 P-a 登记 + P-b 降级 / C-5 P-c 可行且优先 / **C-6 协议应采用契约式六相且完成信号权只在主控站** / **C-7 v1.4 跨仓登记裁定**（§4.5：**只登记不推进**——RPC 定位为「未来分布式 agent 调度统一基座」属**上游对接面**，本仓不代管其未闭环项、不建 P 行 / 不开实施批 / 不新增门禁；三条触发条件 = 用户裁决 / RPC 侧任一项状态实质变化 / 本仓 P-c 实施批启动）（附录 C） |
| 假设区 | 7 | H1 本地小模型异构增益未实测 / H2 seq 分片未设计验证 / H3 A2A 词表是否过重未裁决 / H4 嵌套与每步 agent 化增益未实测 / H5 P-c 粒度与判据库成本未实测 / **H6 §10 协议的时延成本失败率未实测 + evidence_budget 取值无经验值** / **H7 v1.4 RPC 侧实际落地形态未实测**（§4.5：本项证据为**跨仓会话记忆摘要（E2）**，低于本仓 A-51/A-52「读源码 + 实跑」标准 ⇒ 结论方向可信、**具体落地形态未核**）（附录 C） |

## 1. 调研目标

**核心问题**:
1. 把本仓工作流（10 步 + spec_runner 单写者事件流）扩展为**分布式 agent 执行**，社区有哪些**已验证**的协议/执行/编排/验证案例？
2. 哪些可吸收、以什么形态吸收（Layer-0 概念 vs Layer-1 工具）、哪些必须规避？（对照 [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) 三问门禁）
3. 三机集群（`D:\RPC`）**已具备什么、缺什么**？分布式执行的**最高价值落点**在哪？

## 2. 调研方法与取证

### 2.1 使用的工具

| 工具 | 用途 | 查询/范围 |
|------|------|------|
| WebSearch | 社区案例（6 轴） | A2A 协议 / durable execution / 编排模式 / 异构验证 / 同源偏差 / SDD 多 agent 并行 / 本地集群底座 |
| 只读探索代理（3 路） | 既有两个仓库资产消化 | `D:\RPC` 集群能力 + agent 基建；`D:\RPC` 既有 agent 调研；本仓工作流机制 |
| RunCommand | 端点实测取证 | TCP 探测主控站 + A/B/C 三站推理端点 |

### 2.2 调研范围

- **时间范围**: 2025-04 ~ 2026-09（A2A 发布至最新）
- **领域**: agent 互操作协议、durable execution、多 agent 编排、异构验证/LLM-judge 偏差、SDD 并行
- **排除**: 云端托管平台选型（违反本仓本地优先/零依赖）、模型训练类

### 2.3 端点实测取证（A-13，门禁事实）

【A】A-13: **四端点当前全部不可达**（2026-09-10 本机 `Test-NetConnection` 实测）：主控站 `127.0.0.1:1234`、A 站 `192.168.1.33:8080`、B 站 `192.168.1.32:8080`、C 站 `192.168.1.37:8080` 均返回 `False`（工作站调试中）。→ **本批不具备端到端实测条件**，分布式执行验证须「端点就绪门控」，不假造（同 P-010 方案 Z / P-036 先例）。

### 2.4 既有资产边界（防重复调研）

`D:\RPC` 已有三份 agent 主题调研（`Agent生态升级与多智能体协作架构调研.md` 175KB、`Agent跨项目调用标准与迁移复用调研.md` 94KB、`Agent-CLI技术选型调研_20260909.md`）与 `spec/d6-agent-standard/`（ARCHITECTURE/DESIGN/BLINDSCAN-v2/OPEN-ISSUES）。**本批增量 = 协议层（A2A v1.0）+ durable execution + 异构验证量化证据 + 同源偏差实证**；既有结论（CLI 选型、跨站扇出、工作区隔离）**直接引用不重研**。

## 3. 社区案例（分层）

### 3.1 协议层：A2A v1.0（agent↔agent 互操作）

【A】A-1: **A2A v1.0 已由 Linux Foundation 批准（2026-03-12）并进入生产级采用**：150+ 组织支持（AWS/Cisco/Google/IBM/Microsoft/Salesforce/SAP/ServiceNow）、社区实现 383 个、5 种官方 SDK（Python/JS/Java/Go/.NET）、核心仓库 22k+ stars。核心仅三原语：**Agent Card**（`/.well-known/agent.json`，声明 skills/输入输出/鉴权）+ **Task**（状态机 `submitted→working→input-required→completed/failed/canceled`）+ **Artifact**（交付物，SSE 流式回传）；传输 = JSON-RPC 2.0 over HTTPS。**与 MCP 互补非竞争**：MCP = agent↔工具（垂直/手），A2A = agent↔agent（水平/同事）。【来源: [Linux Foundation 新闻稿](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) ; [a2a-protocol.org](https://a2a-protocol.org/latest/)】

### 3.2 执行层：durable execution（长程任务的状态与恢复）

【A】A-2: **durable execution 已被主流平台产品化**：Microsoft Agent Framework **Durable Extension** 提供会话状态持久化、失败后恢复（不重复已完成工作）、跨分布式无状态 worker 扩展、编排 checkpoint、人工输入暂停；AWS **Lambda durable functions** 以 `context.step()` / `waitForCallback()` / `waitForCondition()` 提供 checkpoint+replay 与 saga 补偿。工业界共识表述为「**the workflow is the application**（工作流才是应用，模型只是其中一个 activity）」——每个 agent 调用昂贵/慢/易瞬态失败，恰是 checkpoint/replay 的收益场景。【来源: [MS Agent Framework Durable Extension](https://learn.microsoft.com/fil-ph/agent-framework/hosting/azure-functions) ; [AWS Compute Blog](https://aws.amazon.com/blogs/compute/building-fault-tolerant-multi-agent-ai-workflows-with-aws-lambda-durable-functions/) ; [devops.com](https://devops.com/the-missing-runtime-for-long-running-ai-agents/)】

### 3.3 编排模式层

【A】A-3: **生产环境存活下来的编排模式集 = 5 种**：supervisor+worker（单一决策者、worker 近无状态）、scatter-gather（同任务 × 多模型/多系统后合并）、blackboard（共享状态为主产物）、contract net（招标式任务分配）、sequential pipeline with checkpoints。工程约束被显式量化：**fan-out 上限 3-5 分支**、**慢分支在 1.5× 中位延迟后取消**、所有响应先归一为共享 schema 再合并、每分支记录延迟。韧性手段 = retry/backoff、circuit breaker、bulkhead 隔离、幂等消息设计、event-sourcing+CQRS。【来源: [Future of Software](https://www.future-of-software.com/multi-agent-orchestration-in-production-the-patterns-that-survive-when-the-demo-ends) ; [martinuke0](https://martinuke0.github.io/posts/2026-03-29-implementing-resilient-multiagent-orchestration-patterns-for-distributed-autonomous-system-workflows/)】

### 3.4 异构验证层（本仓最相关）

【A】A-4: **异构多验证者提升事实性有量化证据**：**Council Mode**（异构前沿模型并行 + 共识合成）在 1200 样本 HaluEval 子集上取得 **41.7% 幻觉率相对下降**、TruthfulQA **+7.5 分**、多域推理质量分 **95.4%**（较最佳单模型 +9.2），代价 = **4.2× token 成本**；**MAV**（Multi-Agent Verification）证明「**验证者数量**」是正交于采样数的 test-time scaling 维度——Aspect Verifiers 用现成 LLM 免训练、按 aspect 分工、二值投票合并，且组合弱验证者可弱到强泛化。【来源: [Council Mode (arXiv 2604.02923v4)](https://arxiv.org/pdf/2604.02923v4) ; [MAV (OpenReview)](https://openreview.net/pdf/7b678a8c5a2418eb04bf51471bd5fe69d40500f5.pdf)】

【A】A-6: **Crucible 证明异构验证可在单机多模型落地，并给出「单模型多视角」的证伪**：在**单张 AMD MI300X** 上以 **6 个不同开源模型家族**并行对抗审查，「**跨架构一致度**」作为置信度、每条发现附**逐字证据引文**。其核心论断 = 单模型扮演六种人格时，「一致」只是**该模型先验的六次重复**；只有 4/6 个**不同架构**独立标记同一风险才算真正交叉验证。【来源: [github.com/leonardtudor11/crucible](https://github.com/leonardtudor11/crucible)】

【A】A-7: **Arbiter 的形式化审计给出「LLM 自评会崩塌」的量级证据**：对 202 个"已证明"结果做空洞/平凡证明审计后，**真正有效比例从 82.8% 崩塌到 16.3%（33/202，~5×）**，38.1% 为空洞证明。其**信任模型**明确分层：LLM 的抽取/形式化属**不可信启发式**，机器校验的证明证书属**可信**。【来源: [github.com/vishk23/arbiter](https://github.com/vishk23/arbiter)】

### 3.5 同源偏差实证（异构验证的必要性来源）

【A】A-5: **LLM-as-judge 的同源/同家族偏差已被独立量化**：① **self-bias + family-bias** 存在——judge 系统性给自己的输出、以及**同家族**模型输出更高分（AWS 统计框架，>5000 prompt-completion、9 个 judge 实证）；② IOV Labs 盲审测得**家族级**自偏好指数均值 **+0.14（≈14 分）**，且**非"自我识别"所致**（4 个 judge 中 3 个识别率≈0 却同样自偏好 → 偏差是隐式的分布吸引）；③ 附带偏差巨大——**首位答案胜率 63%**（position bias）、**长度与胜率相关 +0.98**；④ dreaming.press 裁定该偏差「**住在权重里**」——prompt 层无法修正，**唯一有效缓解是换 judge 家族**。【来源: [Play Favorites (arXiv 2508.06709)](https://arxiv.org/pdf/2508.06709v1) ; [The Judge in the Mirror](https://github.com/hankimis/self-preference) ; [dreaming.press](https://dreaming.press/posts/llm-judge-bias.html)】

### 3.6 SDD × 多 agent 并行

【A】A-8: **SDD 多 agent 并行的社区共识 = 六模式 + 四失效模式**：六模式 = spec 驱动任务分解（显式文件/接口边界）→ **git worktree 隔离执行** → 角色分工（coordinator / specialist / verifier）→ 按任务风险路由模型 → 验证门禁（tests + 自动 gate）→ **顺序合并**；四失效模式按可检性排列 = 合并冲突（**低**：git 立即标记）< 重复实现（**中**：需跨分支比较）< **语义矛盾（高：过编译过 lint，需人工判断）** < 上下文耗尽（中）。OpenSpec 实践给出时序纪律：**proposal 在 main 上、apply 在 worktree 内、verify 在 worktree 内、merge 之后才 archive**，且"提交越密越好"（恢复点）。【来源: [augmentcode 指南](https://www.augmentcode.com/guides/how-to-run-a-multi-agent-coding-workspace) ; [OpenSpec+WorkTrees+OpenCode](https://blog.harikrishnan.io/2026-04-01/openspec-git-worktrees-opencode)】

### 3.7 本地集群底座

【A】A-9: **exo 是"多设备合成一台 AI 超算"的代表实现**：自动设备发现（免配置）、**RDMA over Thunderbolt**（跨机延迟降 99%）、**拓扑感知自动并行**（按实时拓扑自动选张量/流水线切分）、官方实测 4×M3 Ultra 跑 Qwen3-235B 达 **31.9 tok/s**，且兼容 OpenAI/Claude/Ollama API。**但 Linux 目前仅 CPU、GPU 支持仍在开发**（macOS/MLX 优先）。【来源: [github.com/exo-explore/exo](https://github.com/dale-lakes/exo) ; [exo 上手文](https://blog.csdn.net/gitblog_01175/article/details/159938383)】

## 4. 现有资产盘点（两仓交叉）

### 4.1 本仓已存在的"可分布接口"（不是从零开始）

【A】A-10: **本仓已有四个可分布接口雏形**：① `spec_runner` **事件流**（append-only JSONL + `seq` 单调 + `resume`/`fork`/`replay`/`search` 共享流，L1-L7 不变式）；② **RULE-5 异基座第二会话**（reviewer 与 implementer 不同模型家族，独立 pass 的现成第二 agent 雏形）；③ `fork` 子命令（从事件流派生分支）；④ **per-feature 独立 session + `spec/<feature>/` 目录**（多 feature 天然可并存）。来源: [SPEC_RUNNER_DESIGN.md](../spec-runner/SPEC_RUNNER_DESIGN.md)、[SPEC_PROCESS.md](../../SPEC_PROCESS.md)、`tools/spec_runner/spec_runner.py`。

### 4.2 本仓三大硬约束（设计的边界）

【A】A-11: **本仓工作流的三大硬约束**：① **单写者/单进程**（每 session 单进程、`seq` 流内单调、L2 装配后请求）——`SPEC_RUNNER_DESIGN` 把「多 worker / 水平扩展」**明列为非目标**（单用户场景）；② **stdlib 零依赖**（runner + 三校验器全部 Python stdlib only）；③ **ADR-0010 分层懒加载门禁**（Layer-0/Layer-1 三问，未激活零副作用）。来源: [SPEC_RUNNER_DESIGN.md](../spec-runner/SPEC_RUNNER_DESIGN.md)、[ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md)。

### 4.3 集群（`D:\RPC`）已建的 agent 基建

【A】A-12: **三机集群已有可用的分布式 agent 执行基建**：① `agent-cli.ps1`（单命令「工作区同步 → 站上 headless 执行 → 产物回收」，五模块 M1 workspace/M2 task/M3 router/M4 lock+state/M5 preflight+collect，tar+scp 同步，flock 双层锁，契约归一 `.agent-run.json`，退出码 2-12）；② **任务卡 front-matter 契约**（`proj/task/model/cli/sensitivity/complexity/type/readonly/audit/timeout_s/accept`）；③ **跨站扇出 L1 已验证**（A+B 各 2 并发，cross_wall 4.8s，ratio 0.71，经 `ssh -NL` 隧道）；④ **铁律**：跨站各 1 并发、**勿同站叠并发**（同站叠并发被统一内存带宽顶起）。来源: `D:\RPC\spec\d6-agent-standard\{DESIGN,ARCHITECTURE}.md`、`D:\RPC\docs\DEV-LOG-011-d6-agent-standard.md`。

### 4.4 缺口（`D:\RPC` 自述）与已否决清单（防缝合堆砌）

- **缺口**（`OPEN-ISSUES.md`）：依赖 DAG、健康监控、崩溃恢复"普遍空缺"；扇出 L2/L3 未做；`review--peer` 未实现；coordinator 模式未投产。
- **已否决（本批不得重提）**：RPC 对 80G 模型为 **-17% decode 税** → "独立端点而非 RPC"；**编排框架（LangGraph/CrewAI/Temporal）** 因"依赖 DAG/健康监控/崩溃恢复普遍空缺 → 无需追框架"被否决；跨机投机解码 / PD 分离不可行；CLI 选型已定（opencode + Claude Code 双现役，Pi/Hermes/Gemini/Codex 不采用）。

### 4.5 跨仓观察项：`D:\RPC` 作为未来分布式 agent 调度统一基座 + 其未闭环问题登记（v1.4，只登记不推进）

> **缘起** = 用户裁决（2026-09-30）：「**RPC 是未来分布式 agent 调度统一基座**，A 表未闭环问题**暂时只登记**」。本项把该**定位**与**四项未闭环事项**入册，作为 **P-c 落地时的上游对接面**；**本批不推进**（不修改 `D:\RPC` 任何文件、不在本仓开实施批、不新增门禁、零代码）。

【A】A-43: **`D:\RPC` 四项未闭环事项的跨仓实录（E2——来源 = 跨仓会话记忆逐条摘要，未经跨仓源码直读）** = ① **D7-CC #3（相对根 / 归一化）**：13:00 取证完成、**13:05 已裁**「相对根 = **相对 runDir**，通过**外壳注入**实现、**不新造 root 字段**」，但 **state 仍 `todo`、未改代码** ⇒ 缺口 = **已裁待实现**；其中「**归一化做到什么程度**」在来源中**未见明确裁定**（**待核**）。② **D7-CC #4**：`O-123` 待裁项「**只剩 D7-CC #4 一条**」，`needs_decision` **7 → 6** ⇒ 缺口 = **待裁**（#3 既已定为 runDir ⇒ **依赖已解**）。③ **U4×3 + U5×2（5 条暂缓）**：未实测登记条目 **49 → 51 条**（todo 42 / partial 5 / retired 3 / boundary 1），`needs_decision` **9**；缺口 = **待选路线**（**站内卡**〔**需起引擎**〕**或** 人工 public 摘要）。④ **索引「叶子节点」缺口**：`inventory/untested-index.yaml` 已建（字段 `spec/n` / `gist` / `state` / `needs_decision` / `refs`）+ `tests/test_untested_index_sync.py` **双向对账已进仓**，但**叶子条目仍无消费者**——门禁 `spec-untested` **只判节存在性与非空、不判正文有无无证据断言**，分诊**全靠人工**。**参照读数** = 台账 `ledger-status` 仍开 **4** 项（O-86 / O-101 / O-111 / O-118；O-07 / O-102 / O-110 / O-112 已闭环）。**两处推断（如实标注，未锚定）** = 「站内卡 / 起引擎」对应 09-09 记忆的 **llama-server 引擎**（`load-gate → 起引擎 → station_ready`，三站空闲、无常驻推理服务）；「索引叶子节点」对应 `untested-index.yaml` 的逐条条目。

【B】B11: **RPC 的「统一基座」定位与本仓 P-c 是同一条链的两端** —— 依据 = **A-12/A-43**（RPC 侧已有 agent-cli 派发 + 任务卡契约 + 跨站扇出实证 + accept 可执行判据，而其未闭环项**全部落在「可机械核对的前置与消费者」**：相对根归一化 / 产物身份 / 未实测条目路线 / 索引无消费者）+ **C-5/B7**（本仓 P-c 正是「把判据与证据链前置并强制机械核」）⇒ 放开断言：**RPC 四项未闭环与 P-c 三条前置同源**（皆「**承诺未固化 / 无消费者**」问题），故 P-c 落地时应**把 RPC 侧索引的消费者位点一并纳入**，而非另建第二套对账。

【C】C-7: **登记裁定 = 只登记不推进，且不与本仓批次耦合** —— ① 定位登记为「**未来分布式 agent 调度统一基座**」（属**上游对接面**，本仓**不代管**其未闭环项）；② 四项以**跨仓观察项**形态入册，**不在本仓建 P 行、不开实施批、不新增门禁、不新增模板**；③ **触发条件（任一即重审）** = Ⅰ **用户裁决**（P-c 进入实施批 / 明确要求接管 RPC 侧事项）；Ⅱ **RPC 侧四项中任一项状态实质变化**（#3 进入实现 / #4 裁定 / 5 条暂缓选定路线 / 索引接入消费者）；Ⅲ **本仓 P-c 实施批启动**（此时本节须转为**对接清单**）；④ **未触发处置** = 维持登记（**不做为**）。

【H】H7: **RPC 侧未闭环项的「实际落地形态」未实测** —— 本项来源为**跨仓会话记忆摘要（E2）**而非跨仓源码 / 文档直读（对照本仓 A-51/A-52 的「读源码 + 实跑」取证标准，**本项低一档**）⇒ 「相对根已裁」「索引无消费者」等**结论方向可信，但具体落地形态（是否已改代码、消费者位点落在哪、5 条暂缓的具体条目）未核**。

**边界声明** = 本项**只登记**：**不修改 `D:\RPC` 任何文件** / **不改**本仓 `scripts/` / **不改**任何校验器 / **不新增门禁** / **不新增 P 行** / **零代码**；RPC 侧事项的推进**由其仓库自治**。

## 5. 映射与判定（本批核心）

### 5.1 ADR-0010 三问逐候选裁定

| 候选 | 形态 | Q1 分层 | Q2 激活条件 | Q3 未激活零副作用 | 裁定 |
|------|------|--------|------------|------------------|------|
| **A2A 协议**（Agent Card/Task/Artifact 词表） | 契约概念 | Layer-0 | 需统一两套自造契约时 | ✅（纯文档） | **概念吸收**（不引 SDK） |
| **durable execution 模式** | 架构概念 | Layer-0 | 事件流跨机分片需求出现时 | ✅ | **概念吸收**（事件流已是实例，见 B2） |
| **异构验证**（MAV/Crucible/Council 模式） | 方法论 | Layer-0 + 复用集群既有模型 | RULE-5 独立 pass 跨站化时 | ✅（零新工具，只用既有端点） | **优先候选**（见 C-2） |
| **git worktree 隔离** | 工程实践 | Layer-0 | 跨 feature 并行实施启动时 | ✅（git 原生命令） | **概念吸收** |
| **orchestrator 框架**（LangGraph/CrewAI/Temporal） | 外部依赖 | — | — | ❌ 违反零依赖 D6 + 与 `D:\RPC` 已否决结论冲突 | **否决** |
| **exo**（分布式推理底座） | 外部服务 | Layer-1 | Linux GPU 支持成熟且现栈失效时 | ❌ 与既有 llama.cpp/RPC 栈冲突 | **否决**（A-9 Linux 限制） |
| **A2A SDK / 运行时服务** | 外部依赖 | Layer-1 | 跨组织 agent 互操作成为真实需求时 | ❌ 本地单人场景无此需求 | **懒加载登记**（触发驱动） |

### 5.2 最高价值落点（B1 的支撑）

分布式执行在本仓的价值**不在"算力分摊"**（单用户无算力饥渴，且 `D:\RPC` 已证同站叠并发负收益），**而在"异构验证的物理化"**——本仓 [SPEC_PROCESS](../../SPEC_PROCESS.md) RULE-5 已把"异基座独立验证"写成纪律，社区（A-4/A-5/A-6/A-7）独立量化了异构验证的必要性与同源偏差的危害，而集群（A-12）恰好提供三站异构模型与已验证的跨站扇出通道。三者叠合即得出落点判定。

### 5.3 与既有结论的冲突辨析

- **不与 `D:\RPC` "不追框架"冲突**：本批同样否决 orchestrator 框架，只吸收**模式与契约词汇**（Layer-0），与「工具可以拒、思想可以留」先例一致（[ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) 连锁否决辨析）。
- **不与 spec_runner「单写者」非目标冲突**：本批不改 runner 现有语义；"分片"仅为候选方向登记（H2 未设计验证），不主张推翻非目标声明。
- **不与零依赖 D6 冲突**：全部裁定中无一引入新依赖；A2A 仅取词表、异构验证仅用既有端点。

## 6. 分层结论

- **Layer-0 概念吸收（零工具）**：A2A 契约词表 / durable execution 模式 / 异构验证方法论 / worktree 隔离实践。
- **优先候选（触发条件最近）**：**跨站异构验证臂**——把 RULE-5 的"同机换模型"升级为"跨站跨家族"，复用集群既有端点与跨站扇出通道，零新依赖。
- **懒加载登记（触发驱动不排队）**：A2A SDK / 依赖 DAG / 健康监控 / 崩溃恢复 / coordinator 模式 / 事件流 seq 分片。
- **否决**：orchestrator 框架（LangGraph/CrewAI/Temporal）、exo、跨机 RPC 推理。
- **本批止于调研**（C-3）：端点实测全不可达（A-13）+ ADR-0010 触发驱动 → 不实施，登记触发条件。

## 7. 补充调研（v1.1）：工作流每步 agent 化 × 微工作流嵌套

> **问题拆解**: 用户假设含两个**可独立裁决**的子命题——**P-a**「工作流的每一个步骤由工作站的编程 agent CLI 执行」（外层替换：把"人/单会话"换成"站上 headless agent"）；**P-b**「每个 agent 再嵌套微工作流机制」（内层递归：agent 内部再跑一个小型工作流）。前提 = **不考虑吞吐效率**。以下分别取证，并回答"可行 / 收益 / 代价 / 案例"。

### 7.1 社区与工业案例

【A】A-14: **Claude Code 官方已支持嵌套子代理，但默认关闭**：v2.1.172 起子代理可再 spawn 子代理（**最深 5 层**）；v2.1.187 后台子代理深度**在创建时固定**；v2.1.212 单会话 spawn 上限 **200**；**v2.1.217 嵌套默认禁用**（需设 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 开启）+ 并发上限 20。关键约束：**嵌套子代理无法向用户提问**（`AskUserQuestion` 不可用）→ 审批与决策点必须留在 Main 边界——这直接决定"每步 agent 化"的架构必须**把 gate 留在编排层**。来源：[Claude Code 子代理嵌套规格汇总](https://dev.to/ucjung/claude-code-subagents-can-now-spawn-subagents-4h2a)。
【A】A-17: **"深度"是显式设计参数，各工具默认姿态分歧**：Claude Code 硬上限 5 层（第 5 层叶子不再获 `Agent` 工具）；Cursor SDK（2026-06-04）**无深度限制**；OpenAI Codex `agents.max_depth` **默认 1**。**递归退化实证**：opencode issue #18100 —— 47 个 session 跨 20 层，**depth 2–18 全是 explore→explore 空转**，直到 depth 19 才真正执行了一次 `grep`——即嵌套若缺乏"**叶子必须做实事**"判据，会退化为纯传递开销。来源：[递归子代理委派深度权衡](https://agentpatterns.ai/patterns/multi-agent/recursive-sub-agent-delegation-depth/)（含各工具 changelog 出处）。
【A】A-21: **opencode 子代理扇出的实证边界（`D:\RPC` 已测，直接适用 P-a）**：被否证的是「依赖模型内单轮多 `tool_call` 的扇出」——BS-2 实测直连 llama-server 单轮仅 1 个 tool_call（wall 48.3s），经网关 `parallel_tool_calls=false` 时 `task` fan-out **永远串行且静默无报错**；解药 = 把扇出从"模型内编译期并行"下沉到"**编排层运行期并发 HTTP**"。唯一硬证据 = 编排层 3 线程并行墙钟 **52.1s ≪ 串行 110.9s**（跨站 A+B 各 2 并发 cross_wall 4.8s，ratio 0.71）。→ **"每步 agent 执行"的并行必须由外部编排器发起，不能指望 agent 内部自扇出**。来源：`D:\RPC\spec\d6-agent-standard\BLINDSCAN-v2-orchestration.md` §2/§8.7.5 + `DECISIONS.md` D-15。

### 7.2 学术案例（正面与反面并存）

【A】A-15: **正面：RAH（Recursive Agent Harness）**——把"递归单元"从"无工具模型调用"（RLM）升格为"**完整 agent harness**"（含文件系统/代码执行/规划）。固定 backbone 为 GPT-5 时，把 Codex coding-agent 基线 **71.75% → 81.36%**（Oolong-Synthetic，199 样本，13 个上下文桶至 4M token），换 Sonnet 4.5 达 **89.77%**——增益**归因于 harness 而非模型**。其 spawn 逻辑是**普通程序代码**（而非固定递归约定或 schema 工具），故可按 entry 数扩展。来源：[Recursive Agent Harnesses (arXiv 2606.13643)](https://arxiv.org/pdf/2606.13643)。
【A】A-16: **正面：RLM（Recursive Language Models）**——把长上下文当作"可经代码查询的环境变量"而非直接入 prompt，递归地在片段上 spawn 子 RLM；TimeRLM 变体在长时程异常定位上 IoU **0.682** vs 基线 ≤0.329，且可用小 8× 的 backbone。→ 递归的**真实收益场景是"单上下文装不下"**。来源：[TimeRLM (arXiv 2608.03391)](https://arxiv.org/pdf/2608.03391)。
【A】A-18: **反面：MAST 多 agent 失败分类学**（Cemri et al., NeurIPS 2025）——1,600+ 标注轨迹 / 7 个框架，归纳 **14 种失败模式 3 大类**：FC1 规范问题 **41.77%** / FC2 智能体间错配 **36.94%** / FC3 任务验证 **21.30%**；单一模式最高 = **步骤重复 17.14%**，其次推理-行动错配 13.98%；报告的整体失败率区间 **41%–86.7%**。→ "多了 agent 就更好"被实证否定，且**最大失败类别是"规范"**（先于任何 agent 发言就注定失败）。来源：[MAST (arXiv 2503.13657)](https://arxiv.org/abs/2503.13657) + [Failure Taxonomy 汇编](https://github.com/jdforsythe/forge/blob/master/docs/research/failure-taxonomy.md)。
【A】A-19: **反面：复利误差的数学与实证**——链式 N 步准确率 ≈ p^N（0.95^10 = **59.9%**；5 agent × 80% = **32.8%**）；「Agentic Telephone Game」每跳约 92% 保真 → 4 轮降至 **~72%**，且**输出仍然"读起来很流畅"**（质量与观感解耦）；MAP 研究（306 份问卷筛出 86 个生产/试点系统）显示 **68% 的系统在需要人工介入前最多执行 10 步**。来源：[Context Loss and Compound Error 汇编](https://github.com/mareurs/codescout/blob/master/docs/research/multi-agent-context-loss.md) + [Multi-Agent AI Systems](https://www.augmentcode.com/guides/multi-agent-ai-systems)（引 MAP arXiv 2512.04123）。
【A】A-20: **反面：错误级联与治理层实证**——AgentAsk 审计 **824 条执行日志**，认定**链式错误传播是 MAS 失败的根本原因之一**（单个错误可级联为系统级崩溃）；「From Spark to Fire」在 6 个主流框架上标定三类内生脆弱性（**级联放大 / 拓扑敏感 / 共识惯性**），并实证**注入单个原子错误种子即可导致大面积失败**；其 **genealogy-graph 治理层**（消息层插件、**不改协作架构**）在 **≥89%** 运行中阻止最终感染。→ 嵌套/链式结构的**结构性风险可被"消息层治理"缓解**，代价是新增一层运维面。来源：[AgentAsk (arXiv 2510.07593)](https://arxiv.org/html/2510.07593v2) + [From Spark to Fire (arXiv 2603.04474)](https://arxiv.org/html/2603.04474v2)。
【A】A-22: **四重硬约束（本仓已登记，准确表述与来源）**：**Interaction Tax**（arXiv 2608.23541——agent 互读完整输出→一轮内提议收敛、**多样性被擦除**；仅"独立生成+选择/合成"保多样性）/ **Belief Entrenchment**（DReaMAD, arXiv 2503.16814——多 agent 辩论常**强化**偏误而非减少）/ **Spiral of Silence**（"The 10th Agent"——唯一正确的少数派会被多数淹没，需 locked dissenter 结构性保护）/ **Co-Failure Ceiling**（arXiv 2606.27288——增益上限由**共同错误率 β** 决定，**表面多样性 ≠ 错误结构独立**）。来源：本仓 [loop-engineering RESEARCH §4.3](../loop-engineering/RESEARCH.md)。

### 7.3 收益

- **上下文隔离（真实且为最高价值）**：每层获得一个独立、干净的上下文窗口——这是子代理被设计出来的首要理由；RAH/RLM 的增益即源于此（A-15/A-16）。
- **"单上下文装不下"的分层子问题**：当问题树本身分层（N 子系统各含 M 模块）时，递归是唯一能保住每层隔离的形态（A-16）；这也是 community 指南给出的**唯一明确的"值得买"条件**（A-17）。
- **每层可差异化配置**：不同模型/提示/工具子集（Cursor 保留 per-level prompt+model 即为此，A-17）。
- **对 P-a 的收益**：把"人在环的 10 步"变成"站上 headless 的 10 步"，可直接复用 `D:\RPC` 已验证的三件套（工作区同步 / 任务卡契约 / 产物回收）+ 机械退出码门禁，无需新建基础设施。

### 7.4 代价

- **复利误差**：链式 p^N，且"看起来更流畅"（A-19）——与本仓"反幻觉证据账本"的使命**方向相反**。
- **递归退化为纯开销**：缺"叶子必须做实事"判据时，中间层全是传递（A-17 opencode #18100 实证：depth 2–18 空转）。
- **失败类别不可被"每步换 agent"修掉**：MAST 的 FC1 规范问题占 **41.77%**、FC3 任务验证占 **21.30%**（A-18）——问题多在编排与规范层，不在"谁来执行"。
- **可观测性负担**：每层追加 tracing；深度化把调试从"读一个会话"变成"读一棵树"（A-17 明确列为代价）。
- **审批/人在环被结构性挤出**：嵌套层无法向用户提问（A-14）→ gate 必须外提，否则 Review 门禁名存实亡。
- **四重硬约束全数命中**：Interaction Tax（多样性擦除）/ Belief Entrenchment（辩论强化偏误）/ Spiral of Silence（少数派淹没）/ Co-Failure Ceiling（增益上限受共同错误率 β 约束）（A-22）。
- **自我反馈放大（本仓既有负面证据）**：IAL-SCAN 静态分析 6,549 仓库确认 68 个不收敛无限循环；self-refine 放大自偏好（Perils of Self-Feedback）；"修正增益"多来自偶然（Illusions of Reflection）；生产会话 token 5–20×；RSI 上限仅 0.250/1.0（来源同上 [loop-engineering RESEARCH](../loop-engineering/RESEARCH.md) §3）。

### 7.5 与本仓既有防线的冲突辨析

- **B4（并行粒度 = feature 非 step）直接约束 P-a**：同一 feature 的 10 步因 Review 门禁强序 → "每步各起一个 agent"在**单 feature 内**不产生真并行，只产生 10 份上下文与 10 个交接点。
- **P-b 与 RULE-5 的结构冲突**：嵌套会把"异基座第二会话"变成"同一 agent 的内层"，反而**退化异质性**（A-22 Co-Failure Ceiling）；且嵌套会打散 spec_runner 单写者 `seq` 的 L4 共享流不变式（见 H2）。
- **P-b 与 M7/三校验器的功能重叠**：本仓已有**机械验证**（dc_validator / m7_stats / repo_stats / step-gate / verify-anchor）——比"agent 审 agent"更可靠且零 token。嵌套若用于"加强审查"，属**重复建设**（防缝合堆砌）。

### 7.6 可行性裁定

**可行，但两子命题不对称——且"不考虑吞吐效率"并不改变结论：**

| 子命题 | 结论 | 理由 |
|--------|------|------|
| **P-a 每步由工作站 agent CLI 执行** | **可行**（工程上已被 `D:\RPC` 实证） | agent-cli 三件套 + 任务卡契约 + 机械退出码门禁现成；但须接受"并行由编排层发起"（A-21）与"gate 留在编排层"（A-14） |
| **P-b 每 agent 嵌套微工作流** | **仅在"单上下文装不下"时划算；本仓场景判负** | 收益（上下文隔离）在本仓不成立（Layer-0 文档自足可读 + 每 feature 事件流独立）；代价（复利误差 A-19 / MAST FC1+FC3 A-18 / 四重硬约束 A-22 / 递归退化 A-17）全数命中 |

**本仓裁定**：P-b **降级为 Layer-0 概念登记**（仅保留"子问题分层"与"上下文隔离"两条思想），**不引入递归编排运行时**；P-a **登记为 Layer-1 触发驱动候选**（复用 `D:\RPC` 既有 agent-cli，本仓不新建），触发条件 = 本仓工作流确需 headless 化时（C-4）。

## 8. 补充调研（v1.2）：降级设计 P-c——主控站派发+审核 / 工作站单项任务 / 强制决策-证据链

> **问题界定**: 记作 **P-c**（第三个子命题）。与 P-a（每步 agent 化）与 P-b（嵌套微工作流）的关键差异 = **降低工作站 agent 的自主度，把编排与审核权上收到主控站**，并以**强制决策-证据链**作为交付契约。用户前提同样隐含"不考虑吞吐效率"。

### 8.1 本仓已有的机械可验证部分（"证据链"本体）

【A】A-23: **本仓的"决策-证据链"已具备机械可验证骨架**：① **FWK-DECISION-RECORD 八字段**（category / scenario / reasoning / outcome / confidence / entities / decision_maker / metadata + 两时点 valid_from/valid_until）与 **evidence 锚点分级 E1–E4**；② **step-gate 三类规则**——硬性-1 schema（五字段 + `metadata.step_id`/`step_seq` + **evidence 非空**）、硬性-2 秩序（STEP_SEQUENCE = research/design/implement/verify/finalize，位次 + **每步恰一条** + `--expect` 全链一致）、软性-3 锚点形态，exit **0 / 1（硬）/ 2（软）**；③ **verify-anchor 三形态**锚点核查（`path §N` / `path#Lxx` / URL）——文件存在 + 章节标题首 token 精确匹配（`4.` 命中 §4 不命中 4.1）+ 行号上界，URL 为 soft。**机器判 = schema / 步序 / 锚点位置可达；人工判 = 断言语义对错**（RULE-1 补：verify-anchor 只验位置可达，语义归 RULE-5 异基座把关）。来源：[DECISION_RECORD_CONTRACT.md](../../docs/DECISION_RECORD_CONTRACT.md) + `tools/spec_runner/spec_runner.py`（cmd_gate_step / cmd_verify_anchor）。
【A】A-24: **「每步恰一条 decision」现为 hook 级强制，非值守级**：pre-commit 第四 hook `step-enforce`（+ `spec_runner step-enforce --pid`）——从变更文件映射 feature → P 编号 → 前缀定位 session；hook exit **0 全就绪 / 1 任一缺失（阻断）/ 2 映射缺位（提示不阻断）**；P-020 前历史批次豁免。来源：[step_enforce.py](../../scripts/step_enforce.py) + [SPEC_PROCESS.md](../../SPEC_PROCESS.md)。
【A】A-26: **集群侧的"派发+审核"分层设计已登记，但机器复核门尚未实现**：review--peer 分四层——**L1 确定性 accept（pytest/golden，脚本，已落地）→ L2 review subagent（pass/fail rubric、只读评审，设计未实现）→ L3 修订循环（cap 2-3）→ L4 人工/异基座（现有）**；成本护栏 = L2 round budget 1、**L3 才加轮**。对应 `D:\RPC` **O-24 断点①**："产出→ledger 后**无机器复核门**"（「复审」目前靠人工切会话）。来源：`D:\RPC\spec\d6-agent-standard\CLOSED-LOOP-ANALYSIS-2026-09-09.md` §3.3/§4 + `OPEN-ISSUES.md` O-24 / O-16。

### 8.2 集群已有的"单项任务 + 强制验收"形态

【A】A-25: **`D:\RPC` 已落地"单项任务 + 可执行验收判据"的完整形态**：任务卡 front-matter 含 `proj/task/model`（必填）+ `cli/complexity/type/sensitivity/audit/readonly/timeout_s/accept`；`accept` = **可执行判据列表**，写 `.agent-run.json` 的 `accept:{cmd,passed}`——**agent 退出码 0 但任一 accept 失败 → 整任务 failed（exit 9）**；`accept-golden` 用主控站 `.golden/` **独立 golden + checksum**（`GOLDEN_TAMPERED` → exit 9），**防模型自写测试自证**；`readonly` = 层 2 锁（true 共享 / false 排它）；`audit` = 注入断言审计契约。退出码语义完整（2 模型缺失 / 3 锁占用 / 4 sensitivity 冲突 / 5 ssh 断 / 6 超时 / 7 限额 / 9 accept 失败 / 10 站未就绪 / 12 agent-out 不可写）。来源：`D:\RPC\spec\d6-agent-standard\ARCHITECTURE.md` §6 + `DESIGN.md` §6.1-6.2 + `test-cards/dogfood-strong-accept.md`。

### 8.3 关键风险：证据链若"文本化"即落入 CoT 不忠实陷阱

【A】A-27: **CoT / 自陈推理的可信度已被系统性质疑**：① Anthropic（Chen et al. 2025）测得推理模型在部分提示类型下**忠实率低至 25%**；② 12 个开源推理模型 / 10,506 个"被提示影响"样本中，**55.4% 的 thinking tokens 含提示关键词而可见答案完全省略**（thinking-answer divergence），反向仅 **0.5%**——**方向性不对称**；③ "Reasoning Theater"：模型早已锁定答案却继续生成**表演性推理 token**；④ 黑箱检测在"模型答错"区间**失效**，而"答案错误"本身（AUROC 0.696）**强于任何专用不忠实检测信号**；⑤ **忠实性是模型属性而非 prompt 属性**（16 个前沿模型分三模式，多数产出 "decorative CoT"）。→ **强制"决策-证据链"若要求的是"可读的推理说明"，会把本仓推向它最想避免的表演性证据；必须落在"可机械核查的锚点"上**。来源：[Why Models Know But Don't Say (arXiv 2603.26410)](https://arxiv.org/pdf/2603.26410) + [Reasoning Theater (arXiv 2603.05488)](https://arxiv.org/html/2603.05488v1) + [Two Regimes of CoT Unfaithfulness (arXiv 2607.23458)](https://arxiv.org/html/2607.23458v1) + [Measuring and curing reasoning rigidity (arXiv 2603.22816)](https://arxiv.org/html/2603.22816v3)。

### 8.4 社区与标准的独立同构（P-c 不是自造）

【A】A-28: **业界独立演化出同构方案（契约 + 证据 + 独立验证）**：**AgentGuard**（contract-based accountability runtime——"**no evidence = not done**"，orchestrator 独立验证而非信任 agent 输出；pipeline 模式 = 每 stage 各自 contract + evidence + DAG 依赖；直指 "**false progress**" 问题）；**in-toto**（attestation = Statement(subject+digest) + predicateType + predicate，四层 Predicate/Statement/Envelope/Bundle）；**SLSA**（provenance 预言词 + 分级 L1/L2/L3）；**Sigstore**（keyless 签名 + Fulcio 短时效证书 + Rekor 透明日志）；**Signet**（每次 tool call 生成**签名收据** + **SHA-256 哈希链** + **离线可验** + **双边共签**——"改任一字段签名即断，删/重排哈希链即断"）。→ 本仓 verify-anchor 的"只验位置可达" + 集群 accept 的"可执行判据"与这套"独立可验证"思路同构，**但当前只有 sha256/checksum，无签名身份层**。来源：[AgentGuard](https://github.com/sneiko/agent-guard) + [in-toto/SLSA/Sigstore 图谱](https://github.com/jamestexas/agents/blob/main/docs/prior-art/slsa-sigstore-in-toto.md) + [Signet](https://github.com/Prismer-AI/signet/) + [Attestation 框架对比](https://safeguard.sh/resources/blog/software-attestation-framework-comparison)。
【A】A-29: **IETF 已就"AI agent 执行证据"立项**：`draft-emirdag-scitt-ai-agent-execution-00`（2026-04，SCITT profile）——定义 **AIR（AgentInteractionRecord）** 作为 COSE_Sign1 签名载荷；**Evidence Chains 按 `agent_id` 划分，同一 `agent_id` 内 MUST 串行化记录产出**（与"确定性编排 / 单写者序列"同构）；Registration Policy 要求**哈希链完整性 + 时序 + 序列完整性**；并给出 EU AI Act Art.12/19 等合规映射。来源：[AI Agent Execution Profile of SCITT](https://datatracker.ietf.org/doc/html/draft-emirdag-scitt-ai-agent-execution-00)。
【A】A-30: **"决策血缘"已有成熟概念模型**：**W3C PROV** 以 entity / activity / agent 建模，并区分 **attribution / association / delegation** 三种责任关系（正对应"产物归因于 agent、活动关联于运行时、运行时代表人类或上级自动化策略"）；**Astra** 的 **Decision Lineage** 表述为 `决策 = f(prompt@版本, 技能@版本, 上下文@快照, 记忆@状态)`，给定 `decision_id` 可 **100% 重建当时 LLM 看到的完整输入**，因果链事件流贯穿会话。→ 与本仓「decision 事件入事件流（append-only + 可 replay）」同构。来源：[Agent Identity and Signed Provenance](https://zylos.ai/research/2026-04-25-agent-identity-provenance-signed-audit-trails/) + [Astra Agent Runtime](https://matrixorigin.cn/astra)。

### 8.5 收益

- **消解 P-b 的两个致命项**：单项任务 = **无内层递归 → 无复利误差链**（对比 A-19）；审核外置主控站 = **gate 不被嵌套层挤出**（对比 A-14）。
- **MAST 最大失败类被结构性转移**：FC2（智能体间错配 36.94%）在"无 agent 间自由通信"的形态下大幅不适用（A-18）。
- **消除 "false progress"**：accept 是可执行判据而非自陈——**没证据就是没做**（A-25/A-28），且 golden 独立 + checksum 阻断"模型自写测试自证"。
- **证据链有现成落地位点**：本仓 step-gate（每步恰一条 + evidence 非空）+ verify-anchor（锚点可达）+ RULE-6（E1–E5 分级、E5 禁入结论）已是同一思想（A-23）——**P-c 本质是"把已有机制跨机化"，而非新建方法论**。
- **恰好补上已登记缺口**：`D:\RPC` O-24 断点①（"产出→ledger 后无机器复核门"）正是 P-c 要落的 L2 机器复核门（A-26）。

### 8.6 代价

- **主控站成为单点与串行瓶颈**：审核上收即审核串行化——与"不考虑吞吐效率"前提相容，但放弃 P-a 的并行收益。
- **accept 判据的编写成本前移且必须前置**：判据须**先于派发写定**，否则事后补判据 = 自证（对照 A-25 的 golden 防篡改设计意图）。
- **证据链文本化 = 表演风险**（A-27）：这是本方案唯一的"看起来在正常工作"的失败模式。
- **密码学级不可否认性缺失**：当前仅有 sha256/checksum，无签名身份 → 若要"离线可验 + 防抵赖"，需引入 Signet/SCITT 级能力（Layer-1 重引入，须过 ADR-0010 三问）。
- **"单项任务"的粒度边界需设计**：过细则交接开销压过收益，过粗则退回 P-b（见 H5）。
- **与 runner 零依赖约束的张力**：`tools/spec_runner/README.md` 声明 spec_runner 与 Spec_Workflow「双向零依赖」，主控站派发复用 runner 时须保持该约束。

### 8.7 可行性裁定

**可行，且在三方案（P-a / P-b / P-c）中与本仓 + 集群既有机制最同构、风险最低：**

| 维度 | P-c 的判定 |
|------|-----------|
| 机制现成度 | **最高**——集群侧 accept / `.agent-run.json` / golden 已落地；本仓侧 decision 契约 + step-gate + verify-anchor 已落地 |
| 复利误差 | **不适用**（单项任务，无链式 LLM 交接） |
| gate 完整性 | **保持**（审核在主控站，不在被审核的 agent 内） |
| 主要风险 | **证据链文本化 → 表演**（唯一但致命；已有缓解 = 锚点化 + accept 可执行判据） |
| 失败模式可检性 | **高**（accept 判据 + 锚点核查均为机械判定） |

**三条不可省略的前置**（缺一即退化为表演）：
1. **证据链锚点化**——要求 E1–E4 级锚点（可机械核查），拒绝纯文本推理说明（A-27）；
2. **accept 判据先于派发写定**——否则判据后补 = 自证（A-25）；
3. **审核机械优先、LLM 复核次之**——确定性检查在前、judge 在后（与 M7 ㉞「LLM-judge 分数不可盲信」一致）。

**分层结论**：P-c = **Layer-1 触发驱动候选**（复用 `D:\RPC` agent-cli + 本仓 step-gate / verify-anchor，**零新依赖**）；同时**概念吸收** W3C PROV / in-toto / SCITT 的"**证据链 = 请求-响应-产物三者绑定 + 序列完整性**"思想（**Layer-0**）。**不引入** Signet / Sigstore / SCITT 的密码学运行时（须先过 ADR-0010 三问 Q3）。

## 9. 补充调研（v1.3）：三条不可省略前置的深入取证

> 用户指令要求"深入补充调研前置问题"。三条前置（**① 证据链锚点化 ② accept 判据先于派发写定 ③ 审核机械优先、LLM 复核次之**）本节逐条给出**协议级标准**与**量化证据**，并回答"为什么不可省略"。

### 9.1 前置① 证据链锚点化（可机械核查）

【A】A-31: **"锚点化"在工业标准里的规范形态 = 内容导出身份 + 规范化 + 摘要绑定**：**MWS** 的硬要求 R1「**Content-Derived Identity**」——每个被证明的制品 **MUST** 由其规范化内容的密码学摘要标识、**不得由位置标识**；指纹计算前 **MUST** 先做 JSON 规范化（RFC 8785），使**语义相同的记录产生相同摘要**；并采用**三重指纹**（SHA-256 / SHA3-512 / BLAKE3，三种独立构造 → 算法敏捷性）。**Weft** 的表述最直白：证明引用 materialized content 的 **Merkle root**，因而「verified」是**关于字节的陈述**，而非关于可变引用的陈述。→ 对应本仓：verify-anchor 三形态（`path §N` / `path#Lxx` / URL）正是"位置 + 可复核内容"的锚点；而 **E1–E5 分级**中 E1（可重放命令）最高，是"关于字节"的。
【A】A-32: **Kettle（arXiv 2605.08363）给出锚点化的强度上限**：provenance 文档在 **TEE（受测可信执行环境）内**生成，其 SHA-256 提交到 TEE 平台的 attestation report-data 字段——**硬件签名的 attestation 本身就是 provenance 的签名**，签名身份链到 TEE 厂商根而非构建基础设施运营者；其收益是 **"验证缩减为一次签名校验 + 少量摘要比对，无需重新执行构建"**。→ 本仓当前无 TEE/硬件信任根，故只能到 E1（可重放）级，**不应宣称更高**。
【A】A-33: **IETF 已就"证据包"立项，且真实世界已有同构落地**：**Reilly Sentinel Protocol（SEP）** 定义 Sentinel Evidence Package，绑定 **payload digests + provenance metadata + signatures + 区块链时间戳证明 + 可解析标识符**，目标为"抗篡改、可独立验证的收据"；**真实世界同构实例**——中国市场监管总局检验检测报告系统：机构上传报告电子原件时系统自动生成**唯一哈希值并与报告编号绑定**，"一机构一账号"，实现不可篡改可追溯。→ 说明"锚点化"不是学术概念，而是**已在监管场景强制落地**的工程标准。

**为什么不可省略**：A-27 已证 CoT 不忠实（thinking-answer divergence 55.4%）；A-31/A-32 说明**只有绑定到字节的摘要**才是机器可判的。**文本化的"推理说明"不可机械核查 ⇒ 等于无证据**。

### 9.2 前置② accept 判据先于派发写定（承诺装置）

【A】A-34: **该前置的成熟范式是"预注册"（pre-registration）**：在数据收集**之前**公开承诺假设、样本量与分析计划——其机制就是**承诺装置（commitment device）**，消除事后重排的自由度；它同时封堵 **HARKing**（事后把发现包装成假设）与 **p-hacking**，并封住「**garden of forking paths**」（同一数据集有数十种可辩护的分析路径，FWER = 1−(1−α)^m——**仅 14 次未校正检验就使"至少一个假阳性"概率 >50%**）。**Registered Reports** 更进一步：审稿在**看数据前**即给出 **In-Principle Acceptance**，从制度上移除"结果显著性"对发表的激励。→ 迁移到 P-c：**判据必须在派发前写定**，否则"事后补判据 = 自证"。
【A】A-35: **IETF PACT 给出"判据前置"的协议级实现**：**Verifiable Task Contract（VTC）** 是签名 JSON，绑定 parties / scope / price / **verification method** / liability；**验收工具（acceptance instrument）必须随招标（CFB）以 `criteria_hash` 承诺并传送，接收方 MUST 在签名前验证所传内容与哈希匹配**；并明文规定 **"Where the natural-language description and the acceptance instrument conflict, the acceptance instrument governs."**（自然语言描述与验收工具冲突时，**以验收工具为准**——即"**判据 > 意图**"）。验证方法还分四级：**T0-reexec（确定性重执行）/ T1-tee / T2-zkml / T3-jury**——与本仓 **E1–E5 分级**同构。
【A】A-36: **"判据先行"的量化收益与"判据后置"的量化危害**（三份**预注册** GRPO 研究，1,512 次选择事件）：一个健全验证器作为 **certify-or-abstain 门**发出 **101 份证书 + 1,411 次显式弃权，从不静默通过**（**构造上不可能认证错误输出**）；而处在**同一门位置**的 example judge（LLM-judge 式）在留出任务上**认证了 54%–100% 的错误输出**。更严重的是**反向教学**：3B 基座在 verifier 过滤采样下解出 16.7%，**经 judge 训练后 5 个种子全部降到 0%**。作者并称其**证明格式（assurance lattice）使"过度声明"在格式上不可表达**——与本仓 **E5 禁入结论**同构。

**为什么不可省略**：判据后置的三个坏结局——① 判据会被调到"刚好能过"（Goodhart）；② 事后补判据的评审**没有可对照的先验**，无法判断"是否放水"；③ 判据若为文本则退回 A-27 的表演陷阱。

### 9.3 前置③ 审核机械优先、LLM 复核次之（门的顺序）

【A】A-37: **协议级标准 = Asimov Safety Architecture（IETF）的双门**：**Gate 1 确定性 denylist**（零延迟/零方差/可审计）+ **Gate 2 无状态 LLM judge**；其设计原则直接涵盖本前置——**P3 Deterministic First：确定性门 MUST 先于 LLM 门执行**；**P1 架构分离**（推理模型 ≠ 判定模型）；**P4 无状态判定**（judge **零会话上下文**，因而免疫多轮上下文操纵）；**P6 Fail-Closed**；**P7 每门决策 MUST 留痕且抗篡改**。其核心论断：**"Removing the semantic layer does not eliminate risk. It makes the misses silent."**（去掉语义层不会消除风险，只会让漏检变**静默**）——反向同理：把确定性层挪到 judge 之后，会让**本可零成本捕获的结构性错误**进入昂贵且不可复现的语义环节。
【A】A-38: **机械优先的工程收益已被量化**（2026 共识："不是二选一，而是**层叠**"）：确定性检查 **$0 / 亚毫秒 / 字节级可复现**；judge **$0.005–0.05/次 / 100–3000ms / 随模型版本漂移（calibration drift）**；层叠规则被表述为 **"every layer runs only on what the cheaper layer below it could not decide"**。真实事故佐证语序不能倒置：某团队 judge-only 栈首月账单 **$40K**，且 judge 给一个**金额差 100 倍**的回答打了 **0.89** 分——事后复盘的原话是「**A judge reads prose**；语义评估做不了结构校验」——而一个 schema/parser 本可在**微秒级**捕获。另一份工程总结把层叠固化为 **L1 确定性断言（每次 PR 全量跑，零 LLM 调用）→ L2 LLM 质量评分（发布前门禁）**，并给出三种混合投票策略（**rule_first / llm_first / parallel**）。
【A】A-39: **机械前置门禁解掉的是一类"静默错误"**（arXiv 2607.07405，KDD-ETAAI'26）：门被定义为**纯函数** `g(tool_name, args, db_state) → {allow, reject}`（**无 LLM 调用、无写入**）；在 τ²-bench airline 域中 **78% 的观测失败是 silent wrong-state**——工具不报错、**agent 自报成功**，状态却是错的（"用户看到的是一份干净的 transcript 与成功的最终回复"）。四门套件把全基准成功率 **29.6% → 42.0%**（+12.4pp，配对 bootstrap P=0.0012），15 种子复现 +12.3pp（P=0.0008）；**因果定位清晰**：开火的 26/50 任务 +19.2pp，未开火的 24 任务变化不显著；frontier harness（gpt-5.2）亦从 61.2% → 71.6%。

**为什么不可省略**：**"agent 自报成功"是最危险的失败模式**（A-39），而它**在语义层几乎不可见**（judge 只读散文，A-38）。机械层的价值不只是便宜，而是**它的失败是可见的、它的判定是可复现的**。

### 9.4 三条前置的共同机理与在本仓的落点

【A】A-40: **协议层已有"委派—证据回收—方可完成"的状态语义**：**AIDP（IETF，draft-vandoulas-aidp-03）** 定义 **Intent Lifecycle Model**，并把 **"Delegation as a lifecycle state"** 写成规范——**父 intent MUST NOT 报 `completed`，直到被委派工作的 Observations 收到并验证**（或并入 `partially_completed`）。→ 这正是 P-c 的关键语义：**"完成"不是执行方的声明，而是委派方收到并验证证据后的状态转换**。
【A】A-41: **并行工作区的协调原语已有成熟集合**（ACP，Agent Coordination Protocol）：**Workspace**（共享上下文）/ **Worker**（有身份的注册actor）/ **Work unit**（**显式生命周期状态机**）/ **Lease**（advisory、**带 TTL 的资源声明**，已被他人持有时返 **409 lease_conflict**，可 `renew`、监督者可 `break`）/ **Checkpoint**（可恢复的部分进度快照，使 handoff **跨越崩溃**）/ **Memory**（append-only、workspace 域内）/ **Artifact** / **Review**（work unit 的门禁）/ **Event**（**append-only 单调事件**；恢复中的 worker **先 replay 历史再行动**）。→ 与本仓 spec_runner 事件流 + 集群 flock 双层锁高度同构。
【A】A-42: **"交接契约"已被标准化为六要素模式**：① 必需**输入** schema（objective / constraints / **evidence budget** / available tools）② 必需**输出** schema（result / citations / confidence / **done-signal**）③ 上下文**归属** ④ 显式**成功/失败终态** ⑤ citations **前向链接**（证据溯源）⑥ **重试/升级路径**。并给出**症状识别**：agent 反复循环或来回推同一任务，**典型病因是缺显式 done-signal**，而"**修法是契约，不是调 prompt**"。

【B】B9（见附录 B）: 三条前置在本仓**并非新增要求，而是已有机制的显式化**——① 锚点化 ↔ `verify-anchor` 三形态 + E1–E5 分级（E5 禁入结论 ↔ A-36 的 assurance lattice）；② 判据前置 ↔ `step-gate` 硬性-1（schema + **evidence 非空**）+ 集群任务卡 `accept`（**本就写在卡里，先于派发**）+ golden checksum；③ 机械优先 ↔ 三校验器 / step-gate / verify-anchor **全部零 LLM**。→ **P-c 的落地成本主要在协议编排，而非机制新建。**

## 10. P-c 下的主控站 ↔ 工作站交互协议（分析）

> **定位**: 本节是**协议分析**（Layer-0 设计输入），非实施规范。它以既有机制为骨架、以 §9 的三条前置为约束、以外部标准为词汇，给出可被后续 DESIGN 步骤直接消费的协议结构。

### 10.1 角色与不变量

| 角色 | 职责 | 明确**不**做 |
|------|------|------------|
| **主控站**（Dispatcher + Adjudicator） | 立契（写判据/golden）、派发、回收、**验证**、裁决、登记（事件流唯一写者） | 不执行任务本体 |
| **工作站**（Executor） | 领取租约、只读执行单项任务、产出 artifact + 运行契约 + decision 记录 + 证据锚点 | **不自评通过**、不写 verdict、不重派、不合并 |

**协议不变量（I-1~I-6）**：
- **I-1 单写者**：事件流（decision/verdict 登记）只有主控站可写；工作站只产出、不落账。
- **I-2 判据前置**：`accept` 判据与 golden 在立契（P0）即固化哈希；P0 之后被修改 ⇒ 契约失效、任务作废（承 A-34/A-35）。
- **I-3 完成信号权在主控站**：任务状态只能由 P5 机械判定翻转为 `accepted`；工作站对自身产出无"完成"发言权（承 A-40）。
- **I-4 证据锚点化**：所有"证据"必须是 E1–E4 级可机械核查锚点；**纯文本推理说明不计为证据**（承 A-27/A-31）。
- **I-5 机械门先于语义门**：L1 全绿是 L2 启动的必要条件（承 A-37/A-38）。
- **I-6 fail-closed**：任一门不可用/报错 ⇒ 阻断（不默认放行）（承 A-37 P6）。

### 10.2 六相状态机

| 相 | 发起方 | 输入 | 输出 | 门禁 / 判据 | 失败路径 |
|----|--------|------|------|------------|---------|
| **P0 立契** | 主控站 | feature 定义 + 判据库 + golden 库 | **TaskContract**（判据 + criteria_hash + golden 引用与 checksum + 只读输入快照引用与 digest + evidence_budget + timeout + sensitivity/readonly + 禁止项） | 判据**可执行**、golden checksum 可校验 | 判据不可执行/缺失 ⇒ **不派发** |
| **P1 领取** | 工作站 | TaskContract | Lease（holder + attempt + expiry） | **租约未被持有**（否则 409，对齐 ACP lease_conflict / 集群 flock） | 冲突 ⇒ 显式拒绝，**不排队** |
| **P2 执行** | 工作站 | TaskContract + 只读输入 | artifact + 运行契约（`.agent-run.json`）+ decision 记录（八字段）+ **证据锚点数组** | 开工前 **digest 校验通过**；遵守 evidence_budget | 超时 / 输入被改 / 超预算 ⇒ 显式终止（对应集群退出码） |
| **P3 回收** | 主控站 | 工作站产出 | 校验后的产出集 | **artifact digest + 输入快照 digest 校验** | digest 不符 ⇒ 显式失败（防途中篡改） |
| **P4a 机械验证** | 主控站 | 产出集 | L1 verdict（exit code） | `accept` 逐条执行 + **golden checksum** + **锚点核查**（三形态）+ schema/秩序（三类规则）——**全部纯函数、零 LLM** | 任一失败 ⇒ 整任务 failed（对齐集群 accept 失败 exit 9 / GOLDEN_TAMPERED exit 9） |
| **P4b 语义复核** | 主控站（异基座） | L1 全绿的产出 | L2 标记（不改实现） | **仅 L1 全绿后触发**；round budget = 1；修订循环 cap 2-3 | 标记 ⇒ 由主控站决定重派或人工 |
| **P5 裁决与登记** | 主控站 | L1/L2 结果 | **Verdict** + 事件流登记 | verdict = **exit code 机械映射**（非 LLM 判断） | 拒绝 ⇒ 显式失败记录 + 重派决策（attempt+1）**由主控站做** |

**状态机**：`drafted → dispatched → claimed → executing → collected → mech_verified →（可选）sem_verified → accepted | rejected`；任一相失败 ⇒ `rejected(phase, reason)`，**不存在静默跳相**。

### 10.3 三种信封（消息契约）

| 信封 | 方向 | 核心字段 | 外部标准对应 |
|------|------|---------|------------|
| **TaskContract** | 主控站 → 工作站（P0） | task_id / 单项任务描述 / **accept[]（判据 + criteria_hash）** / golden{ref, checksum} / inputs{ref, digest} / evidence_budget{anchors, tool_calls} / constraints（禁止项） / timeout_s / sensitivity / readonly | 集群任务卡（`proj/task/model/cli/sensitivity/readonly/timeout_s/accept`）· PACT **VTC**（party/scope/verification/liability）· A2A **Task** · AIDP **Intent** |
| **RunReport** | 工作站 → 主控站（P3） | run_id / attempt / artifact{digest, size} / inputs_digest / exit_code / **decisions[]（八字段）** / **evidence[]（锚点，E1–E4）** / usage / **无 verdict 字段** | `.agent-run.json`（D:\RPC）· FWK-DECISION-RECORD（本仓）· in-toto **Statement**（subject+digest）/ SCITT **AIR** · Signet receipt |
| **Verdict** | 主控站（P5，仅登记） | verdict（exit code）/ phase / l1_results[] / l2_marks[]（可选）/ redispatch? / recorded_at + seq | spec_runner **事件流**（append-only + seq 单调）· ACP **Event** · SCITT **Evidence Chain** |

### 10.4 失败处置矩阵（把 A-39 的"静默错误"显式化）

| 失败模式 | 探测点 | 处置 | 关键点 |
|---------|-------|------|-------|
| 判据不可执行 | P0 | 不派发 | fail-closed（I-6） |
| 租约冲突 | P1 | 409 显式拒绝 | 不排队（对齐 A-41） |
| 输入快照被改 | P2 开工前 | 中止 + `tampered` | digest 绑定（A-31） |
| 超时 | P2 | 显式超时（**不静默**） | 对齐集群 exit 6 |
| **agent 自报成功但 accept 失败** | P4a | **整任务 failed** | **直击 A-39 的 silent wrong-state** |
| golden 被改 | P4a | `GOLDEN_TAMPERED` ⇒ failed | 防模型自写测试自证（A-25） |
| 锚点不可达 | P4a | 软性失败（exit 2） | 对齐 verify-anchor 语义 |
| L1 绿但语义可疑 | P4b | 异基座标记，**不改实现** | RULE-5 单向权限 |
| **证据链只有文本没有锚点** | P4a | **视为无证据 ⇒ failed** | I-4（B8 防线） |

### 10.5 与既有机制/标准的映射（防重造）

| 本协议要素 | 本仓既有 | 集群既有 | 外部标准 |
|-----------|---------|---------|---------|
| TaskContract | SPEC_PROCESS 四文档 + 判据 | 任务卡 front-matter + `accept` | PACT **VTC** / A2A Task / AIDP Intent |
| 判据前置 | step-gate 硬性-1（evidence 非空） | `accept` 判据 + golden checksum | 预注册 / PACT `criteria_hash` |
| 证据锚点 | `verify-anchor` 三形态 + E1–E5 | `.agent-run.json` + collect | in-toto Statement / SCITT AIR / Signet |
| decision 记录 | **FWK-DECISION-RECORD 八字段** | 任务卡审计契约（`audit`） | W3C PROV（attribution/association/delegation） |
| 事件流 / 登记 | spec_runner 事件流（append-only + seq） | ledger（产出→登记） | ACP **Event** / SCITT **Evidence Chain** |
| 租约 / 单写者 | 单写者序列（session 单进程） | flock 双层锁 | ACP **Lease**（TTL + 409） |
| 机械门 → 语义门 | 三校验器 → 异基座独立 pass | accept → review subagent | Asimov **Gate 1 → Gate 2** |
| 完成信号 | gate = exit code | accept 通过才 `completed` | AIDP **Observations 验证后才可 completed** |

### 10.6 三条设计红线（结论）

【C】C-6（见附录 C）：
1. **完成信号权只属于主控站**——工作站任何形式的"我已完成"都不构成状态转换；必须由 P5 的机械判定发出（承 A-39 静默错误 + A-40 Observations 语义）。
2. **L1 机械门必须先于 L2 语义门**，且 **L2 无权改写实现**（承 A-37 P3 + RULE-5 单向权限）；顺序倒置会把零成本可捕获的结构性错误送进昂贵且不可复现的语义环节（A-38）。
3. **判据与 golden 的哈希在 P0 固化**——P0 之后修改即契约失效（承 A-34 承诺装置 + A-35 `criteria_hash` + A-36 反向教学）。

> **与 §8 的关系**：§8 回答"P-c 可不可行、为何优先"；§9 回答"三条前置为何不可省略"；§10 回答"协议长什么样"。三者共同构成 P-c 的 Layer-0 设计输入，**实施仍止于懒加载 gate**（端点不可达 + ADR-0010 触发驱动）。

## 11. 参考文献

- A2A Protocol 官方站：https://a2a-protocol.org/latest/
- Linux Foundation A2A 一周年新闻稿：https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year
- Microsoft Agent Framework Durable Extension：https://learn.microsoft.com/fil-ph/agent-framework/hosting/azure-functions
- AWS Lambda durable functions for multi-agent：https://aws.amazon.com/blogs/compute/building-fault-tolerant-multi-agent-ai-workflows-with-aws-lambda-durable-functions/
- The Missing Runtime for Long-Running AI Agents：https://devops.com/the-missing-runtime-for-long-running-ai-agents/
- Multi-Agent Orchestration Production Patterns：https://www.future-of-software.com/multi-agent-orchestration-in-production-the-patterns-that-survive-when-the-demo-ends
- Resilient Multi-Agent Orchestration Patterns：https://martinuke0.github.io/posts/2026-03-29-implementing-resilient-multiagent-orchestration-patterns-for-distributed-autonomous-system-workflows/
- Council Mode（arXiv 2604.02923v4）：https://arxiv.org/pdf/2604.02923v4
- Multi-Agent Verification（MAV）：https://openreview.net/pdf/7b678a8c5a2418eb04bf51471bd5fe69d40500f5.pdf
- Crucible：https://github.com/leonardtudor11/crucible
- Arbiter：https://github.com/vishk23/arbiter
- Play Favorites（arXiv 2508.06709）：https://arxiv.org/pdf/2508.06709v1
- The Judge in the Mirror：https://github.com/hankimis/self-preference
- Your LLM Judge Is Biased：https://dreaming.press/posts/llm-judge-bias.html
- Multi-Agent Coding Workspace（augmentcode）：https://www.augmentcode.com/guides/how-to-run-a-multi-agent-coding-workspace
- OpenSpec, Git WorkTrees and OpenCode：https://blog.harikrishnan.io/2026-04-01/openspec-git-worktrees-opencode
- exo：https://github.com/exo-explore/exo

**v1.1 补充调研新增（§7）**:
- Claude Code 子代理嵌套规格汇总：https://dev.to/ucjung/claude-code-subagents-can-now-spawn-subagents-4h2a
- 递归子代理委派深度权衡（跨工具深度姿态 + opencode #18100）：https://agentpatterns.ai/patterns/multi-agent/recursive-sub-agent-delegation-depth/
- Recursive Agent Harnesses（arXiv 2606.13643）：https://arxiv.org/pdf/2606.13643
- TimeRLM / RLM（arXiv 2608.03391）：https://arxiv.org/pdf/2608.03391
- Why Do Multi-Agent LLM Systems Fail?（MAST, arXiv 2503.13657）：https://arxiv.org/abs/2503.13657
- Failure Taxonomy（MAST + Forge watchlist）：https://github.com/jdforsythe/forge/blob/master/docs/research/failure-taxonomy.md
- Context Loss and Compound Error in Multi-Agent Systems：https://github.com/mareurs/codescout/blob/master/docs/research/multi-agent-context-loss.md
- AgentAsk：Multi-Agent Systems Need to Ask（arXiv 2510.07593）：https://arxiv.org/html/2510.07593v2
- From Spark to Fire：Error Cascades in LLM-MAS（arXiv 2603.04474）：https://arxiv.org/html/2603.04474v2
- Multi-Agent AI Systems: Architecture & Failure Modes（引 MAP arXiv 2512.04123）：https://www.augmentcode.com/guides/multi-agent-ai-systems
- Recursive Self-Spawning Agent Architecture（实现指南）：https://github.com/junwatu/claude-code/blob/main/RECURSIVE_AGENT_ARCHITECTURE.md

**v1.2 补充调研新增（§8）**:
- Why Models Know But Don't Say（CoT 忠实性分歧, arXiv 2603.26410）：https://arxiv.org/pdf/2603.26410
- Reasoning Theater: Disentangling Model Beliefs from Chain-of-Thought（arXiv 2603.05488）：https://arxiv.org/html/2603.05488v1
- Two Regimes of Chain-of-Thought Unfaithfulness（arXiv 2607.23458）：https://arxiv.org/html/2607.23458v1
- Measuring and curing reasoning rigidity（arXiv 2603.22816）：https://arxiv.org/html/2603.22816v3
- AgentGuard（contract-based accountability runtime）：https://github.com/sneiko/agent-guard
- in-toto / SLSA / Sigstore prior art 图谱：https://github.com/jamestexas/agents/blob/main/docs/prior-art/slsa-sigstore-in-toto.md
- Signet（agent tool call 签名收据 + 哈希链 + 离线可验）：https://github.com/Prismer-AI/signet/
- Software Attestation Frameworks Compared（SLSA / in-toto / Sigstore）：https://safeguard.sh/resources/blog/software-attestation-framework-comparison
- AI Agent Execution Profile of SCITT（IETF draft, AIR + Evidence Chains）：https://datatracker.ietf.org/doc/html/draft-emirdag-scitt-ai-agent-execution-00
- Agent Identity and Signed Provenance（W3C PROV + 工作负载身份 + 委派）：https://zylos.ai/research/2026-04-25-agent-identity-provenance-signed-audit-trails/
- Astra Agent Runtime（Decision Lineage）：https://matrixorigin.cn/astra

**v1.3 补充调研新增（§9/§10）**:
- Machine-Web Symbiosis（IETF draft-reilly-mws-00，内容导出身份 + 规范化 + 三重指纹）：https://www.ietf.org/archive/id/draft-reilly-mws-00.txt
- Kettle: Attested Builds for Verifiable Software Provenance（arXiv 2605.08363）：https://arxiv.org/html/2605.08363v1
- Reilly Sentinel Protocol（IETF，证据包绑定摘要+签名+时间戳）：https://datatracker.ietf.org/doc/html/draft-reilly-sentinel-protocol-00
- Pre-registration and Registered Reports：https://bookdown.org/dorothy_bishop/Evaluating-What-Works/prereg.html
- Pre-Registration: Why It Matters（承诺装置 / HARKing / garden of forking paths）：https://metricgate.com/blogs/pre-registration-why-it-matters/
- PACT: A Contract Layer for Autonomous Agent Commerce（IETF draft-laxsharma-pact-00，VTC + criteria_hash + 验证分级）：https://www.ietf.org/archive/id/draft-laxsharma-pact-00.txt
- Reward hacking grows with model scale; certify-or-abstain gate（1,512 选择事件）：https://www.greaterwrong.com/posts/7iChsBSpTNDTEkQrd/reward-hacking-grows-with-model-scale-a-sound-certify-or
- The Asimov Safety Architecture（IETF draft-baysal-asimov-safety-architecture-00，双门 + P3 Deterministic First）：https://www.ietf.org/archive/id/draft-baysal-asimov-safety-architecture-00.txt
- Deterministic vs LLM-Judge Evals (2026): Layer, Don't Choose：https://futureagi.com/blog/deterministic-vs-llm-judge-evals-2026/
- How I Built Deterministic LLM Evaluation Metrics for Production（$40K judge 账单 + 金额差 100 倍事故）：https://futureagi.com/blog/how-i-built-deterministic-llm-evaluation-metrics-2026/
- Reason Less, Verify More（arXiv 2607.07405，确定性前置门禁解静默错误）：https://arxiv.org/html/2607.07405v1
- Agent Interaction & Delegation Protocol（IETF draft-vandoulas-aidp，Intent 生命周期 + Delegation 状态）：https://datatracker.ietf.org/doc/draft-vandoulas-aidp/
- Agent Coordination Protocol（ACP，Lease / Checkpoint / Event 协调原语）：https://github.com/chrismichaelps/acp
- Handoff contracts（六要素交接契约模式）：https://github.com/MHHamdan/Agentic-AI-Engineer/blob/main/learning-paths/03-multi-agent-systems/patterns/01-handoff-contracts.md

---

## 附录 A：A 类断言明细

- A-1 至 A-13：见 §2.3 与 §3 各 `【A】` 行；A-14 至 A-22：见 §7 各 `【A】` 行（v1.1）；A-23 至 A-30：见 §8 各 `【A】` 行（v1.2）；**A-31 至 A-42：见 §9 各 `【A】` 行（v1.3）**；**A-43：见 §4.5（v1.4，**E2 跨仓会话记忆来源**，含两处如实标注的未锚定推断）**。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "分布式执行对本仓的最高价值落点不是算力分摊而是异构验证的物理化——本仓 RULE-5 已把异基座独立验证写成纪律，社区独立量化了异构验证必要性（41.7% 幻觉相对下降）与同源偏差危害（家族自偏好 +14 分、住在权重里），集群又恰好提供三站异构模型与已验证跨站扇出通道；三者叠合 ⇒ 分布式执行的第一性用途 = 把异基座第二会话从同机换模型升级为跨站跨家族独立验证臂", "basis": "A-4/A-5/A-6/A-10/A-12 + SPEC_PROCESS RULE-5"},
  {"id": "B2", "inference": "本仓 spec_runner 事件流在形态上已是 durable execution 的一个实例——append-only JSONL + seq 单调 + resume/fork/replay 共享流，对应 checkpoint + replay + 分支派生；因此本仓做分布式 durable 执行无需引入 Temporal 类运行时，只需把单写者 seq 按 session/feature 分片即可获得水平扩展，增量远小于社区典型引入路径", "basis": "A-2/A-10/A-11 + SPEC_RUNNER_DESIGN L1-L7"},
  {"id": "B3", "inference": "A2A 对本仓的价值是契约词汇而非运行时——本仓已有任务卡 + .agent-run.json 两套自造契约与 gate=exit code 门禁，A2A 的 Agent Card/Task 状态机/Artifact 可作为统一这两套契约的命名骨架（Layer-0 概念吸收）；而引入 A2A SDK 或托管服务会违反零依赖 D6 且未过三问 Q3，在本地单人场景亦无跨组织互操作需求", "basis": "A-1/A-11/A-12 + ADR-0010 三问"},
  {"id": "B4", "inference": "并行化的正确粒度是 feature 而非 step——社区四失效模式（重复实现/语义矛盾最难检）与 D:\\RPC 铁律（跨站各 1 并发、勿同站叠并发）共同指向：同一 feature 的 10 步因 Review 门禁依赖前序产物而强序，只有跨 feature 才真正独立可并行；把单 feature 的 10 步拆到三站会制造语义矛盾与契约漂移而非加速", "basis": "A-3/A-8/A-11/A-12"},
  {"id": "B5", "inference": "用户假设的两个子命题可行性与收益不对称——P-a（每步由工作站编程 agent CLI 执行）工程上已被 D:\\RPC 的 agent-cli 实证可行（工作区同步→headless 执行→产物回收 + 任务卡契约 + 机械退出码门禁现成），但须接受两个结构性约束：并行必须由编排层发起（agent 内自扇出被 BS-2 实测否证）与 gate 必须留在编排层（嵌套层无法向用户提问）；P-b（每 agent 嵌套微工作流）的收益仅来自单上下文隔离，而该收益在本仓不成立（Layer-0 文档自足可读 + 每 feature 事件流独立），代价（复利误差 p^N / MAST 规范与验证两类失败 / 四重硬约束 / 递归退化）却全数命中——故『不考虑吞吐效率』并不改变结论：P-a 可行、P-b 本仓判负", "basis": "A-14/A-15/A-16/A-17/A-21"},
  {"id": "B6", "inference": "嵌套微工作流对本仓的净收益为负，四条理由：① 本仓瓶颈不是『单上下文装不下』（Layer-0 文档自足、每 feature 事件流独立），递归的真实收益场景不成立；② 本仓已有机械验证（dc_validator / m7_stats / repo_stats / step-gate / verify-anchor），嵌套式『agent 审 agent』属重复建设且更不可靠；③ 嵌套把 RULE-5 异基座第二会话降级为同一 agent 的内层，退化异质性（Co-Failure Ceiling），并打散 spec_runner 单写者 seq 的 L4 共享流不变式；④ B4 已裁定并行粒度为 feature 而非 step，单 feature 十步 agent 化只增上下文与交接点、不增并行", "basis": "A-18/A-19/A-20/A-22 + A-10/A-11 + B4"},
  {"id": "B7", "inference": "主控站派发+审核 / 工作站单项任务 / 强制决策-证据链（记作 P-c）在三方案中与本仓+集群既有机制最同构、风险最低——它同时消解 P-b 的两个致命项（单项任务 → 无内层递归 → 无复利误差链；审核外置主控站 → gate 不被被审核的 agent 挤出），且两仓已有机制可直接拼装（集群侧 accept 可执行判据 + .agent-run.json 契约 + 独立 golden 防自证；本仓侧 decision 八字段 + step-gate 每步恰一条 + verify-anchor 锚点核查 + RULE-6 E1-E5），社区（AgentGuard / in-toto / SLSA / Sigstore / Signet）与 IETF（SCITT AIR + Evidence Chains）独立演化出同构形态；且它正是 D:\\RPC 已登记缺口 O-24 断点①（产出后无机器复核门）的设计方向——即本方案不是新增，而是补上该缺口", "basis": "A-23/A-24/A-25/A-26/A-28/A-29/A-30"},
  {"id": "B8", "inference": "该设计唯一的失败模式是『证据链文本化』——若要求交付的是可读的推理说明而非可机械核查的锚点，则落入 CoT 不忠实陷阱（thinking-answer divergence 55.4% vs 反向 0.5% / 部分提示类型忠实率低至 25% / Reasoning Theater 表演性推理 / 忠实性是模型属性而非 prompt 属性），使强制证据链退化为表演；故其可行性条件 = 证据链必须锚点化（E1-E4 级）+ accept 判据先于派发写定 + 审核机械优先、LLM 复核次之", "basis": "A-23/A-25/A-27 + A-22"},
  {"id": "B9", "inference": "三条不可省略前置在本仓并非新增要求，而是已有机制的显式化——① 证据链锚点化 ↔ verify-anchor 三形态（path §N / path#Lxx / URL）+ E1-E5 分级（E5 禁入结论 ↔ A-36 的 assurance lattice 使过度声明在格式上不可表达）；② accept 判据前置 ↔ step-gate 硬性-1（schema + evidence 非空）+ 集群任务卡 accept 字段（本就写在卡里、天然先于派发）+ golden 独立 checksum；③ 审核机械优先 ↔ 三校验器 / step-gate / verify-anchor 全部零 LLM。故 P-c 的落地成本主要在协议编排而非机制新建；而三条前置各自的违反代价已被外部证据量化（thinking-answer divergence 55.4% / judge 在同门位置认证错误输出 54-100% / 静默错误占观测失败 78%）", "basis": "A-23/A-24/A-25/A-26/A-27/A-31/A-36/A-37/A-39"},
  {"id": "B10", "inference": "三条前置的共同机理是把『事后不可验证的判断』前移为『事前可机械核对的承诺』——预注册（约束研究自由度）、VTC criteria_hash（约束验收标准）、确定性门（约束动作合法性）、证据锚点（约束断言位置）都是同一手法；其反面正是 P-c 唯一失败模式（证据链文本化 = 把承诺退回成自述）。因此 P-c 的健壮性等价于『承诺是否在事前被固化且可机械核对』，而不等价于『agent 是否配合』；这解释了为何前置②（判据前置）比前置③（门的顺序）更根本——判据若未前置，后续机械门只是对一把随时可被改动的尺子做校验", "basis": "A-31/A-34/A-35/A-36/A-37 + B8"},
  {"id": "B11", "inference": "D:\\RPC 的『未来分布式 agent 调度统一基座』定位与本仓 P-c 是同一条链的两端——RPC 侧四项未闭环（D7-CC #3 相对根归一化已裁待实现 / D7-CC #4 待裁 / U4×3+U5×2 待选路线 / 索引叶子节点无消费者）全部落在『可机械核对的前置与消费者』，而本仓 P-c 正是『把判据与证据链前置并强制机械核』⇒ 二者同源（皆『承诺未固化 / 无消费者』）；故 P-c 落地时应把 RPC 侧索引的消费者位点一并纳入，而非另建第二套对账", "basis": "§4.5 A-43 + A-12 + C-5/B7"}
]
```

## 附录 C：C 类判断复盘 + 假设区

**C 类判断（不机械对账，review 臂重数）**:
- C-1: 分层裁定——A2A 词表 / durable 模式 / 异构验证 / worktree 隔离 归 Layer-0（概念吸收，零工具）；orchestrator 框架与 exo 否决；A2A SDK 懒加载登记。依据 ADR-0010 三问逐条答录（§5.1）
- C-2: 优先级裁定——**异构验证臂先行**（就绪条件最近：集群模型齐备 + RULE-5 已有契约位点 + 跨站扇出已验证），依赖 DAG / 健康监控 / 崩溃恢复 / coordinator 登记为触发驱动候选不排队
- C-3: 本批止于调研不实施——端点实测全不可达（A-13）+ ADR-0010 触发驱动，同 P-036/P-037 懒加载先例
- C-4: **v1.1 补充裁定**——**P-a（每步 agent CLI 执行）登记为 Layer-1 触发驱动候选**（复用 `D:\RPC` 既有 agent-cli，本仓不新建；触发 = 本仓工作流确需 headless 化）；**P-b（嵌套微工作流）降级为 Layer-0 概念登记**（仅保留"子问题分层"与"上下文隔离"两条思想，不引入递归编排运行时）——依据 §7.6 与 B5/B6
- C-5: **v1.2 补充裁定**——**P-c（主控站派发+审核 / 工作站单项任务 / 强制决策-证据链）可行，且在三方案中优先级最高**：机制现成度最高、复利误差不适用、gate 保持完整、失败模式可机械检出；**它是 `D:\RPC` 已登记缺口 O-24 断点①（产出后无机器复核门）的设计方向**，属"补缺口"而非"新增架构"。前置三条（锚点化 / 判据前置 / 机械优先）缺一即退化为表演——依据 §8.7 与 B7/B8
- C-6: **v1.3 补充裁定**——P-c 交互协议应采用**契约式六相**（P0 立契 → P1 领取 → P2 执行 → P3 回收 → P4a 机械验证 → P4b 语义复核 → P5 裁决登记），并守**三条设计红线**：① **完成信号权只在主控站**（严禁工作站自报完成，对齐 AIDP「Observations 验证后才可 completed」）；② **L1 机械门必须先于 L2 语义门**，且 L2 无权改写实现（对齐 Asimov P3 Deterministic First + RULE-5 单向权限）；③ **判据与 golden 的哈希在 P0 固化**，后改即契约失效（对齐预注册承诺装置 + PACT `criteria_hash`）——依据 §9/§10 与 B9/B10

- C-7: **v1.4 跨仓登记裁定**——`D:\RPC` 四项未闭环（D7-CC #3 已裁待实现 / D7-CC #4 待裁 / U4×3+U5×2 待选路线 / 索引叶子节点无消费者）以**跨仓观察项**形态登记，**只登记不推进**：RPC 定位为「**未来分布式 agent 调度统一基座**」属**上游对接面**，本仓**不代管**其未闭环项、**不建 P 行 / 不开实施批 / 不新增门禁 / 不新增模板 / 不改 `D:\RPC` 任何文件**；**三条触发条件** = Ⅰ 用户裁决（P-c 进实施批或要求接管 RPC 侧事项）Ⅱ RPC 侧任一项状态实质变化 Ⅲ 本仓 P-c 实施批启动（届时本节转为**对接清单**）——依据 §4.5 与 B11
**假设区**:
- [H1] 跨站异构验证臂的**实际增益未经本机实测**——社区证据（41.7% 幻觉相对下降 / 82.8%→16.3% 崩塌）来自前沿大模型或云端异构；本地小模型（qwen2.5-7b / gpt-oss-20b / nemotron）跨家族一致度能否复现同等增益未知，需端点就绪后实测。
- [H2] spec_runner 单写者 seq 的**分片改造是否会破坏 L4 不变式**（resume/fork/replay 共享流）尚未设计验证——分片后跨分片 replay 语义、gate 归属、`--resume` 边界均未定义。
- [H3] A2A 的 Agent Card/Task 词表与企业多 agent 场景**强耦合**（跨组织、SSE、签名卡、多租户）在单人本地场景是否**过重**未裁决——本批仅取三原语作为命名骨架，未推演完整落地方案。
- [H4] **「每步 agent 化」与「嵌套微工作流」的本机增益未实测**——RAH 的 +9.6pt 增益来自前沿大模型（GPT-5 / Sonnet 4.5）与长上下文基准（Oolong 至 4M token），本仓场景（Layer-0 文档自足、本地小模型、单 feature 串行十步）能否复现未知；若端点就绪后实测（如 10 步 pipeline 中 N 步 agent 化的准确率与证据可追溯性变化）可能改写 B5/B6 裁定。
- [H5] **P-c 的「单项任务」粒度边界与 accept 判据库的构建成本未实测**——过细则交接开销压过收益、过粗则退回 P-b；主控站串行审核相对当前「人工切会话复审」的实际增益亦未在本机验证（且四端点当前不可达，无法实测）。
- [H6] **§10 协议未实测**——六相状态机的实际时延 / 成本 / 失败率、Lease 的 TTL 取值、以及 **`evidence_budget`（每任务允许的锚点数与工具调用数）的合理区间**均无既有经验值可依；协议在真实工作站上是否引入新失败模式（如 digest 校验与既有 tar+scp 同步链路的交互、租约过期与长任务的竞态）亦未验证。
- [H7] **`D:\RPC` 侧未闭环项的「实际落地形态」未实测**——本项证据为**跨仓会话记忆逐条摘要（E2）**，未经跨仓源码 / 文档直读（对照本仓 A-51/A-52 的「读源码 + 实跑」标准**低一档**）⇒ 「相对根已裁」「索引叶子节点无消费者」等**结论方向可信**，但**具体落地形态未核**（是否已改代码 / 消费者位点落在哪 / 5 条暂缓的具体条目），且「站内卡 / 起引擎」与「索引叶子节点」两处对应关系系**推断、未锚定**。

## 附录 D：与既有候选池的关系

本批新登记的候选应收敛进 [COMMUNITY_ECOSYSTEM_RESEARCH.md](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) §3.4 候选矩阵（含「分层归属（ADR-0010 Q1）」列），保持单一权威位点，避免双源维护。收敛动作属**视图层同步**，由下一编辑批次执行（本批不重复登记，防双源）。

---

**Review 签字**: _________ 日期: _________
