# 调研文档：框架深度评审与前沿对标

---

id: framework-deep-review-RESEARCH
type: design
version: 1.4
status: draft
date: 2026-10-26
depends: [ADR-0010, FWK-ASSERTION]
upstream: null

---

> **Feature**: framework-deep-review（当前框架深度评审、前沿对标与分优先级升级建议）
> **创建日期**: 2026-10-26
> **修订**: v1.4（2026-10-26，P-132：**runner `step-gate` 显式声明面**——隐式 legacy 移除，`--expect` / `--legacy` 二选一；selftest 81 → 83；A/B/C/H 计数不变）
> **修订**: v1.3（2026-10-26，P-131：**U-2 完整链迁移边界裁决**——取 129；边界只作用于维护/登记；显式声明不豁免；注入测试 5 例；A/B/C/H 计数不变）
> **修订**: v1.2（2026-10-26，P-130：**U-1 O3 Phase 1 门禁实施**——O3 解析器 + 21 测试；U-10 状态更新；A/B/C/H 计数不变）
> **修订**: v1.1（2026-10-26，P-129：**U-1 当前批次绑定方案分析**——新增 §11；补 14 条 A（官方文档 / 标准 / 本仓实测）、7 条 B、3 条 C、5 条 H；结论 = 否决静态最新 P，推荐「新 P 行声明 + 变更 session + 维护模式」混合）
> **状态**: draft（只读评审落档；不改任何代码 / 配置 / 门禁；不合并 PR）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「深度review一下当前框架 对标前沿 给出改进 升级建议」→「先把上一轮详细分析结果全部落档 包含subagent的全部调研细节」

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 42 | 本仓只读代码 / 机械实测（E1）+ 已回原文核验的外部一手来源（T1） |
| B 推断类 | 27 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 9 | 不参与 R7 机械对账（DR-2） |
| 假设区 | 14 | 未实测 / 未裁决项（见附录 C） |

> **取证口径**：本仓事实 = E1（逐字读文件、机械枚举、临时目录探针）；外部来源分两档——**T1** = 本次亲自 WebFetch 回 arXiv abs / 标准原文并核对标题、版本与摘要数字；**T2** = 子代理返回的官方文档或论文摘要，未逐字回原文，只作设计启发，不进入门禁判据。2026 年新论文按**预印本**对待，不当作领域共识。

---

## 1. 调研目标与边界

**核心问题**：

1. **变更是否真正被约束**：当前门禁验证的是「本次变更所属的当前批次」，还是可能被旧批次 session 替代？
2. **结论是否可复核**：三校验器、锚点、session 与 Review 记录，能证明到什么程度、不能证明什么？
3. **故障是否被实测**：现有 guard proof 与黑盒测试覆盖了哪些真实失效，缺哪些故障注入？
4. **控制成本是否值得**：哪些前沿实践值得吸收，哪些属于本仓当前阶段的过度工程？

**边界声明（本轮不做的事）**：

- 不改任何代码、配置、hook、CI 或真值源；不提交、不合并 PR #58；
- 不执行外部仓对照实验（G-11b 仍未点名）；
- 不把预印本结论写成「本框架有效 / 无效」的因果证据；
- 不进入 DESIGN / IMPLEMENTATION；升级建议只到「最小改动 + 验收判据」。

---

## 2. 调研方法与证据口径

### 2.1 工具与执行

| 工具 | 用途 | 结果 |
|---|---|---|
| Read / Grep | 读取 `SPEC_PROCESS` / `CODE_WIKI` / `PROGRESS` / `ASSERTION_EVIDENCE_FRAMEWORK` / 校验器 / runner / hook / CI / 图调研 | 成功（E1） |
| Shell（Python 探针） | 临时目录 + `SR_SESSIONS_DIR` 构造 session，跑真实 `spec_runner.py` | 成功（E1，零写入真实仓） |
| git / GitHub API | 分支、提交、PR 状态、branch protection 实测 | 成功（E1） |
| 子代理 A（73 次工具调用） | 前沿规范、Agent 评测、自纠、污染与外部有效性 | 完成（12 条来源） |
| 子代理 B（66 次工具调用） | provenance、供应链、恢复语义、lease/fencing、可观测性、AI 治理 | 完成（9 条来源） |
| WebFetch | 对关键一手来源做二次核验 | 成功（TestJack / Groundability / Contracts / Self-preference / τ-bench / METR / PROV-DM / SLSA） |

### 2.2 子代理的原始分工

- **子代理 A「调研前沿规范评测」**：6 条设计级结论 + 6 维同维度对照表 + 12 条来源；覆盖契约与 oracle、reviewer groundability、自纠、Agent 验收、污染控制、外部有效性。
- **子代理 B「调研工程控制前沿」**：6 条取舍结论（必需 / 跨仓）+ 9 条来源；覆盖 provenance、attestation、恢复语义、lease 与 fencing、可观测性、AI 风险闭环。
- 两个子代理均未被要求写代码；其结论只作为**设计启发**，本文件对关键数字做了独立回原文核验，未能回原文者明确标 T2。

### 2.3 来源分级与限制

| 层级 | 本文件用法 |
|---|---|
| T1 | 进入 A 类事实；数字与版本可复核 |
| T2 | 进入正文作设计依据，但**不进入门禁判据**、不写成共识 |
| T3 | 只用于发现反例与工程陷阱 |
| E1 / E2 | 本仓实测 / 既有会话与文档证据 |

**限制**：单仓、单人、未执行外部对照；评审只覆盖当前工作树与远端状态；时间截至 2026-10-26；不声称覆盖所有 agent 框架。

---

## 3. 本仓现状：已实测读数

### 3.1 运行基线

【A】A-1 本仓当前六道 pre-commit hook 全 Passed；`python -m unittest discover -s tests` 15/15 OK；`dc_validator` 168 文件 / 47 结果 / 0 违规；`m7_stats` 0 违规（P3 提示 1）；`repo_stats` 0 违规；`console_gen --check` 与源一致。证据级 E1（2026-10-26 实跑）。

【A】A-2 当前分支 `docs/p125-graph-structure-preresearch`，工作树干净，相对 `main` 为 0 behind / 4 ahead；PR #58 OPEN、MERGEABLE、`verify` SUCCESS、尚未合并。E1。

【A】A-3 远端主分支保护实测：required status check = `verify`；`enforce_admins=true`；`allow_force_pushes=false`；`allow_deletions=false`；`strict=false`；`required_approving_review_count=0`；`required_signatures.enabled=false`。E1。

### 3.2 P0-1：自动门禁验证旧批次，而非当前修订批次

【A】A-4 [step_enforce.py](../../scripts/step_enforce.py) 以 `FEATURE_RE` 提取 feature，经 `spec_map.build_pid_map` 得到**单个** PID，再调用 `spec_runner step-enforce --pid <PID>`。E1。

【A】A-5 [spec_map.py](../../scripts/spec_map.py) 的 `wiki_pid_map` 取 `CODE_WIKI.md §9` 行正文中**首个** `P-\d{3}`；`build_pid_map` 先取 PROGRESS 映射、再用 Wiki 映射覆盖（Wiki 优先）。E1。

【A】A-6 机械枚举（2026-10-26）：PROGRESS 映射 36 个 feature，Wiki 映射 39 个，同 feature 不同 PID 共 **21 个**，PROGRESS-only 2 个（`plan` / `templates`）。E1。

【A】A-7 实测：修改 `spec/graph-structure-upgrade/RESEARCH.md` 时，自动 hook 输出 `step-enforce[P-125]: session 定位 specwf-p125-20261024` 并以 5/5 pass；手动 `--pid P-127` 才定位 `specwf-p127-20261024`。E1。

**判定**：自动门禁能证明「该 feature 的某个历史批次有合法 session」，不能证明「本次提交属于并满足当前批次」。「主 P + 后续修订 P」是正常历史模型，问题不在 21 个差异本身，而在**单值映射无法表达当前变更属于哪个批次**。

### 3.3 P0-2：真实 runner 会把 1/5 步 session 判为通过

【A】A-8 [spec_runner.py](../../tools/spec_runner/spec_runner.py) 的 `cmd_step_enforce` 以文件名排序取末位 session，并调用 `cmd_gate_step` 时固定传 `expect=None`。E1。

【A】A-9 真实 runner 探针（临时目录 + `SR_SESSIONS_DIR`，2026-10-26）：仅 1 条 `research` decision 的 session，自动 `step-enforce --pid P-999` 返回 **exit 0**，输出「已登记 1/5 步（未声明 --expect 完整性）」；同一 session 显式 `--expect research design implement verify finalize` 返回 **exit 1**（期望链 ≠ 已登记）。E1。

```text
自动 step-enforce：已登记 1/5 步 → exit 0
显式完整链：期望 5 步 ≠ 已登记 1 步 → exit 1
```

**判定**：完整性在自动路径上是**打印提示**，不是硬失败；与 `SPEC_PROCESS` 对 T3「1 条 session（5 步决策流）」的口径存在差异。历史 session 存在不完整链，因此不能无迁移边界地直接全量强制。

### 3.4 测试与触发面

【A】A-10 [test_hook_blackbox.py](../../tests/test_hook_blackbox.py) 在临时镜像仓写入 `STUB_RUNNER` 替代真实 `spec_runner.py`；15/15 通过。E1。

【A】A-11 [.pre-commit-config.yaml](../../.pre-commit-config.yaml) 的 `blackbox-tests` 触发面只含 `tests/.*\.py` 与 `scripts/(step_enforce|spec_map)\.py`，**不含** `tools/spec_runner/spec_runner.py`。E1。

【A】A-12 [ci.yml](../../.github/workflows/ci.yml) 使用 `windows-latest` + Python 3.11 + `PYTHONUTF8` / `PYTHONIOENCODING` + `contents: read`；复验 DC / M7 / repo_stats / console / step_enforce，并跑六件内嵌 selftest 与外置黑盒。E1。

**判定**：CI 对核心 runner 有 selftest 兜底，但本地修改核心 runner 时不会触发黑盒 hook；本地与远端反馈面不一致。黑盒测试本身无法发现真实 runner 的 `expect=None` 与 session 选择缺陷。

### 3.5 文档规模与维护成本

【A】A-13 文档规模（2026-10-26 实测，行数 / 字节）：`AGENTS.md` 42 / 3,936；`SPEC_PROCESS.md` 578 / 51,846；`CODE_WIKI.md` 942 / 590,442；`ASSERTION_EVIDENCE_FRAMEWORK.md` 347 / 24,035；`PROGRESS.md` 395 / 537,862；`M7_EVIDENCE_LOG.md` 158 / 93,098；`CONSOLE.md` 915 / 63,543；graph `RESEARCH.md` 659 / 55,959。E1。

**判定**：`CODE_WIKI` 与 `PROGRESS` 的体量与超长行意味着维护和 Agent 上下文成本不可忽略；不应再增加需要人工重复回写的派生汇总。

### 3.6 语义审查与可移植边界

【A】A-14 [CODE_WIKI.md](../../CODE_WIKI.md) §4.1 明确 `assertion_audit.py` 为本地工具、**有意不进本仓**；全仓 Glob `**/assertion_audit.py` 为 0 结果。E1。

【A】A-15 [SPEC_PROCESS.md](../../SPEC_PROCESS.md) RULE-1 明示 `verify-anchor` 只验证锚点位置可达、**不验证断言内容对错**；RULE-4 允许单 Agent 自查并标注；RULE-5 仅在引入第二会话时要求异构基座。E1。

【A】A-16 `SPEC_PROCESS.md` 的 T1 证据出口写「独立 pass（如适用）」；T3 明文要求「1 条 session（5 步决策流）」。E1。

【A】A-17 [EXTERNAL_VALIDITY_PREREG.md](../../docs/EXTERNAL_VALIDITY_PREREG.md) 状态为 `registered / unexecuted`；M1/M3 主测文档一致性与形态 II，M2 返工，M4 轮次，M5 独立评审（无则记 N/A）；§4 声明本仓只读零写入，§8 又写每仓执行记录存外部仓侧。E1。

【A】A-18 [graph RESEARCH](../graph-structure-upgrade/RESEARCH.md) v1.2：37A+15B+7C+9H；A 薄图路径；G1/G2/G3 分开；任务卡唯一接口；图能力默认关闭；P4 三判据；S2 前不固化拓扑。E1。

### 3.7 执行证据的现状

【A】A-19 `spec_runner` 的 `gate` 事件已记录 `cmd` / `cwd` / `exit` / `verdict` / `stdout_tail`，且 `gate_passed` 可由流派生查询；但 session 的 decision 文本写「已复验」时，**不强制**对应 gate 事件存在。E1。

【A】A-20 现有 `spec_runner` 无 lease / fencing 概念；graph RESEARCH §14 只登记了 V-EXPORT / V-FENCE / V-LEASE 判据，未实现。E1。

---

## 4. 前沿对标一：规范、契约与评测（子代理 A 全部细节）

### 4.1 契约要半形式化，验收器本身也要被验收

【A】A-21 *Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation*（arXiv:2608.17177v2；SpecOps 2026，与 SPLASH 2026 同址；DOI 10.1145/3842652.3843195）：让 agent 先显式写出前置条件、后置条件与未定义行为，再生成测试。Google 生产 bug 上，bug detection rate 提升 **9.8 个百分点**（p=0.0352），branch coverage 提升 **2.5 个百分点**（p=0.0034）；LLM-as-a-Judge 判定其测试套件在 **77.8%** 的案例优于传统 agent baseline、在 **56.7%** 的案例优于人工测试。T1（2026-10-26 回 abs 原文）。

**边界**：单一 Google 生产 bug集；证明的是「契约脚手架改善测试生成」，不证明十步管道整体有效。

【A】A-22 *TestJack: Should you trust the results in coding benchmarks? Agentic Coding Benchmarks Auditing via Evaluator Evolution*（arXiv:2610.10619v1，2026-10-07）：对每个 trial 按 prompt 需求生成测试、只保留 ground-truth patch 能通过的测试，并复查失败 trial。6 个前沿模型后端 × 5 个基准（含 DeepSWE、SWE Marathon）上，**34.4%** 当前被判正确的 trial 实际违反需求；总体解决率从 **50.6% 降至 33.2%**。T1（回 abs 原文）。

**设计含义**：固定单测会漏需求并遭受 reward hacking；评测器需要**需求驱动增广与抽审**，而不是只增加文档或测试数量。

### 4.2 Review 的首要变量是 groundability，而非模型数量

【A】A-23 *Groundability, Not Scale Alone: When Weak Reviewers Can Audit Strong Coding Agents*（arXiv:2610.01023v1，2026-10-01）：411 条执行标注轨迹 / 3 个 agent / 101 个受控案例；154 条 GPT-5.4 轨迹上，结构化但未核验的证据同时提高缺陷捕获与过度拒绝；提供官方执行证据后，5/6 个 reviewer 在 122 条 held-out 上双率提升，2 个全对；reviewer 规模不是一致预测器。冻结级联在 121 条 GPT-5.4 / 59 条 Gemini 上：coverage **0.89 / 0.86**、risk **0.33 / 0.26**、catch **0.76 / 0.80**、over-rejection **0.66 / 0.67**；多数误拒发生在未解决案例进入 reviewer 时。T1（回 abs 原文）。

【A】A-24 *Do LLM Evaluators Prefer Themselves for a Reason?*（arXiv:2504.03846v3，2025-12-12）：7 个模型族；强模型自偏好更高，但大部分与客观更优表现一致；当评估者作为生成者犯错时，有害自偏好持续存在，强模型更明显；长 CoT 等推理时扩展可降低有害自偏好。T1（回 abs 原文）。

**设计含义**：保留异构实验臂，但不要把「异构基座」当作质量保证；应建立 reviewer 标注集，分别报告 **catch rate 与 false-rejection rate**，并让 reviewer 拿到可核验的执行证据。

### 4.3 自纠应是有回滚的修订策略，不是固定第二轮

**T2（子代理摘要，未逐字回原文）**：

- *Large Language Models Cannot Self-Correct Reasoning Yet*（arXiv:2310.01798，ICLR 2024）：无外部反馈的内在自纠可能使推理退化。
- *When Should LLMs Trust Their Own Revisions? A Risk-Aware Study of Intrinsic Self-Correction*（arXiv:2609.35832v1，2026-09-23）：29 个模型；净准确率会掩盖「对→错」，应记录修订转移矩阵并做风险感知接受。

**设计含义**：每轮 Review 应记录 **错→对 / 对→错 / 新增证据**；高风险修订必须可回滚，不能自动接受「第二轮更好」的叙事。

### 4.4 Agent 验收应从「一次全绿」改为「分布 + 终态 + 成本」

【A】A-25 *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*（arXiv:2406.12045v1，2024-06-17）：用对话结束时的**数据库终态**与标注目标态比对；提出 pass^k 衡量多次试验可靠性；gpt-4o 成功率 <50%，retail 的 pass^8 <25%。T1（回 abs 原文）。

**T2（子代理摘要）**：*Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite*（arXiv:2609.11987v1，2026-09-08）：80 对配对任务；harness 效应与模型效应需分离，比较时应锁定模型与 harness 版本。

**设计含义**：pilot 应报告完成率、pass^k、墙钟、费用与人工裁断时间；一次全绿不足以支撑「流程有效」。

### 4.5 污染控制应进入任务卡

**T2（子代理摘要）**：

- *SWE-bench Goes Live!*（arXiv:2505.23419v2）：持续引入新题降低静态基准污染。
- *Does SWE-Bench-Verified Test Agent Ability or Model Memory?*（arXiv:2512.10218v2）：仅给 issue 文本时出现异常文件定位优势，提示记忆污染。

**设计含义**：模型 / agent 对比应登记任务公开时间、私有或时间切分，并增加「无仓库上下文定位」探针与隔离 oracle。

### 4.6 外部效果只能条件化声称

**T2（子代理摘要）**：*The Impact of AI on Developer Productivity: Evidence from GitHub Copilot*（arXiv:2302.06590v1）：单一 HTTP 任务 RCT 提速 **55.8%**。

【A】A-26 *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*（arXiv:2507.09089v2，2025-07-25）：16 名熟悉仓库的开发者、246 项任务；允许使用 AI 时完成时间**增加 19%**；事前预测减少 24%、事后自评减少 20%；经济学与 ML 专家预测分别缩短 39% / 38%。T1（回 abs 原文）。

**设计含义**：两组结果语境不同，既不矛盾，也不证明本流程有效或无效。本仓外部实验必须补客观工时、后续缺陷、任务类型与仓库熟悉度分层，主观满意度另列。

### 4.7 同维度对照（子代理 A 原表，本文件复核后保留）

| 维度 | 本仓已有优势 | 优先缺口 / 改法 |
|---|---|---|
| 契约与测试 | 外置黑盒回归、ADD | 高风险项补 pre/post/undefined；记录 oracle 版本并做增广审计 |
| 审查独立性 | 双盲重推导、异基座、单向权限 | 将「异质性是增益主源」降为本地待验假设；补 reviewer 校准集 |
| 修订 | 独立 pass、机械探针 | 增加修订转移矩阵与回滚 |
| 运行评测 | 薄图 pilot 已列墙钟、重放、人工裁断时间 | 增加重复试验、终态断言、harness 锁版及成本 |
| 污染 | pilot 已关注模型版本漂移 | 模型比较补 cutoff / private split 与记忆探针 |
| 外部有效性 | 预注册允许负结果、不夸大因果 | M1/M3 之外补客观工时、后续缺陷及任务分层 |

---

## 5. 前沿对标二：工程控制、provenance 与 AI 治理（子代理 B 全部细节）

### 5.1 provenance 是唯一事实源，图只读

【A】A-27 *PROV-DM: The PROV Data Model*（W3C Recommendation，2013-04-30）：以 Entity / Activity / Agent 及 Derivation / Usage 等关系表达来源；标准只规定可互操作的 provenance 表达，不规定存储实现。T1（回 W3C 原文）。

**T2（子代理摘要）**：OpenLineage Object Model v1.54.0：设计期 JobEvent / 运行期 RunEvent + 输入输出 Dataset。

**取舍**：本仓应借鉴「任务、run/attempt、输入输出摘要、commit、执行者、父事件」写入规范字段；Mermaid 只作渲染，内核与门禁不读图。图数据库、OpenLineage 后端当前过度。

**验收**：同一账本可重建同图；改删 Mermaid 不改变判定。

### 5.2 门禁应验证 attestation，而非「通过」字样

【A】A-28 *SLSA v1.2: Verifying artifacts*（Approved）：验证步骤包括 builder identity 可信、provenance 信封签名、`buildType` 与 `externalParameters` 符合期望、以及对 subject digest 的绑定。T1（回 slsa.dev 原文）。子代理 B 另引 SLSA v1.2 attestation model（T2）：provenance 作为可签名 attestation 供验证方按策略校验。

**T2（子代理摘要）**：

- Sigstore Bundle Format v0.3.2（2025-01-14）：签名材料打包与分发格式。
- in-toto（USENIX Security '19）：farm-to-table 供应链保证，布局与环节签名。

**取舍**：跨仓发布或 RPC 产生外部副作用后，应验证「制品 digest + 策略版本 + 来源 ref + 外部参数 + 验证者身份」；自建透明日志、追逐 SLSA 等级当前过度。

**验收**：改文档、换 commit、伪造 pass、错签名者均失败；同证据与策略重放判定一致。

### 5.3 按「至少一次」设计恢复，不承诺端到端 exactly-once

**T2（子代理摘要）**：

- Temporal Architecture / Activity Definition：持久事件历史支撑确定性重放；activity 至少一次；run 与 attempt 分账。
- Azure Durable Task Programming Model：编排器与 activity 的持久化模型。

**取舍**：RPC 侧副作用端使用幂等键，重试有期限与退避；产物写出与状态提交分离；共享存储原子 claim 决定唯一执行者（consume-once）；run 与 attempt 分账。纯文档校验引入 Temporal 过度。

**验收**：在 RPC 成功、响应丢失处杀 worker，可续跑且不双写；毒任务最终进入可处理终态。

### 5.4 lease 不等于 fencing

**T2（子代理摘要）**：

- *The Chubby lock service for loosely-coupled distributed systems*（OSDI 2006）：sequencer / lock generation number，接收方校验。
- Martin Kleppmann, *How to do distributed locking*（2016-02-08）：lease 只约束期限，不能阻止暂停后的旧写者；需单调 fencing token 且由被保护资源原子校验。

**取舍**：graph RESEARCH 已明确「lease ≠ fencing」，本评审维持该判定；单写者本仓部署锁服务当前过度。

**验收**：旧 leader 暂停至 lease 过期，新 leader 写入后，旧 leader 恢复仍不能写。

### 5.5 可观测性默认元数据，正文显式 opt-in

**T2（子代理摘要）**：OpenTelemetry GenAI observability（2026-05-14，09-14 修订）：trace 串起 model / tool / RPC / evidence；记录版本、耗时、token、错误、策略结果；提示词与工具参数、结果默认关闭，开启须脱敏、限 TTL 与权限。

**取舍**：本仓已有 session JSONL 与 gate 事件，可先补「策略结果 + 执行版本 + digest」，不引入完整 OTel 栈。

**验收**：秘密 canary 不进入遥测，调用链仍可追踪。

### 5.6 AI RMF 做风险闭环，不做认证表演

**T2（子代理摘要）**：NIST AI RMF 1.0（2023-01-26）与 Generative AI Profile（NIST AI 600-1，2024-07-26）；AI RMF 为自愿框架，1.0 正在修订。

**取舍**：落实责任、内容来源、上线前测试、事件披露与回滚；企业 GRC 平台当前过度。

**验收**：每类 agent 有 owner、工具/数据边界、拒收阈值、人工接管与事故记录；幻觉证据抽测确被阻断。

### 5.7 子代理 B 的取舍总表

| 事项 | 本纯文档仓 | 跨仓 / RPC 外部副作用后 | 当前过度 |
|---|---|---|---|
| provenance | **必需**：规范字段 + 图只读 | 必需 | 图数据库 / OpenLineage 后端 |
| attestation | 门禁验 digest + 策略版本 | 必需：in-toto / DSSE / Sigstore Bundle | 自建透明日志 / 追 SLSA 等级 |
| 恢复语义 | 事件历史 + 可重放 | 必需：at-least-once + 幂等键 + claim | Temporal 全栈 |
| lease / fencing | 登记判据 | 必需：fencing token 由资源侧校验 | 本仓锁服务 |
| 可观测性 | 轻量：元数据 + gate 结果 | trace 串 model/tool/RPC | 全文集中采集平台 |
| AI 治理 | 必需轻量：责任 + 边界 + 回滚 | 必需 | 企业 GRC 平台 |

---

## 6. 综合分析

### 6.1 当前框架真正强于常见 Spec 工具的部分

1. **控制链分层完整**：本地六 hook + CI + required `verify` + 管理员同样受保护约束，构成 L1/L2 双层。
2. **单一实现与机械重数**：`spec_map` 为映射唯一实现；`repo_stats` / `m7_stats` 把「声明 = 重数」机械化；guard proof 防止「全绿但规则没生效」。
3. **诚实边界**：预注册允许负结果、M5 无评审记 N/A、图调研把未实测项放入假设区、lease ≠ fencing 等区分清楚。
4. **证据分级与外部来源分层**：A/B/C + E1-E5 + T1-T4，避免了「搜到了 = 事实」。

### 6.2 四维评价

| 维度 | 结论 | 依据 |
|---|---|---|
| 变更是否被约束 | **部分**：门禁形态完整，但当前批次绑定与完整链不成立 | A-4~A-9 |
| 结论是否可复核 | **部分**：位置与计数可复核，语义真实性与执行证据未绑定 | A-14~A-16、A-19 |
| 故障是否被实测 | **部分**：guard proof 与 15 例黑盒有效，但真实 runner 与运行时故障未覆盖 | A-10~A-12、A-19 |
| 控制成本是否值得 | **部分**：视图维护成本高；独立语义 Review 仍条件化；B 类工具链有移植断点 | A-13~A-17 |

### 6.3 关键判定

见附录 B（B1~B20）。其中最重要的四条：

- **B1**：全绿 ≠ 当前变更被当前批次验证。
- **B2**：单值 feature→PID 映射在结构上无法表达多修订批次。
- **B3**：`expect=None` 使完整链成为提示而非门禁。
- **B4**：仅用 stub 的黑盒测试无法捕获真实 runner 回归。

---

## 7. 改进升级路线

> 以下 P0/P1/P2 为本次评审的修复优先级，**不是**批次号或 RPC 阶段。每项给出最小改动、故障注入与验收判据；未获用户指令前不实施。

### 7.1 P0-1：修复「当前变更 ↔ 当前批次」绑定

**最小改动（推荐：混合式）**：

1. 保留 `spec_map` 作为 **feature ↔ 主 P** 的索引，但不再用它决定当前批次；
2. pre-commit 直接接收本次提交的 **session 变更**（新增或修改的 `tools/spec_runner/sessions/*.jsonl`），从 session id 解析 PID；
3. 校验规则：变更的 feature 必须与 session 的 PID 存在映射关系；一个批次可覆盖多个 feature；
4. 无 session 变更时，才回退到 `feature → 主 P`，但输出必须标注「主 P 回退，不声明当前批次」；
5. CI 分 `verify-change` 与 `audit-all` 两模式：前者只验当前变更绑定，后者只做存量审计、不追溯制造历史失败。

**故障注入**：

- 只提交旧 P-125 session、修改 graph 文档 → 必须失败；
- 提交 P-127 session + graph 文档 → 必须验 P-127；
- 提交无关 P-999 session + graph 文档 → 必须失败；
- 一提交覆盖两个 feature + 两个 session → 两个关系都须闭合；
- 历史全量审计不得因新规则批量变红。

**验收判据**：

- 自动 hook 的输出必须打印「本次绑定的 session id / PID / 关系来源」；
- 任何「用旧 session 放行当前修订」的路径均为 0；
- 迁移边界机械可判（按 P 编号或提交时间），并有回退开关。

**不建议**：把 21 个主 P / 后续 P 差异全部改成冲突失败；这会误伤正常历史模型。

### 7.2 P0-2：明确并实测完整链门禁

**最小改动**：

1. 自动路径不再以 `expect=None` 作为默认放行；
2. 新批次按档位派生期望链：T3 = 5 步；T1 = 对应文档管线的步集；
3. 当前变更直接验指定 session，不再仅靠「文件名排序末位」；
4. 历史批次保留 legacy 模式，但输出必须写「仅内部一致性通过，不声明完整链通过」；
5. 过渡边界写入配置或常量，附回退开关。

**故障注入**：

- 0/5、1/5、4/5 步 → 全部失败；
- 合法 5/5 → 通过；
- 缺步、错位、同位重复 → 分别有独立用例；
- 历史不完整 session → 不判红，但不得显示为完整通过。

**验收判据**：

- 真实 runner 集成测试覆盖上述矩阵；
- 自动与显式两条路径对同一 session 结论一致；
- 输出中的「通过」必须带 completeness 声明。

### 7.3 P1-1：让真实 runner 进入外置黑盒回归

**最小改动**：

- 在 `tests/` 增加真实 runner 集成测试（临时 `SR_SESSIONS_DIR` + 临时 `SR_REWORK_REGISTRY`）；
- 把 `tools/spec_runner/spec_runner.py` 加入 `blackbox-tests` 触发面；
- 保留现有 stub 测试作为包装层契约测试，不替换。

**故障注入**：删除完整链检查、改回旧 PID 绑定、吞掉 gate 硬失败、破坏 `verify-anchor` 路径解析——每个变异体必须使至少一个测试变红。

**验收判据**：CI 与本地 hook 对同一变异体给出相同结论；真实 runner 的 selftest 与集成测试互不替代。

### 7.4 P1-2：把「已复验」绑定到真实执行证据

**最小改动**：

- 复用现有 `gate` 事件，不新增平台；
- `verify` 步的 decision 必须引用规定命令的 gate 记录（name / cmd / exit / verdict）；
- gate 记录绑定：变更 digest、策略版本、执行者、时间；
- 语义：「session 记录存在」与「命令实际执行且通过」分开声明。

**故障注入**：

- 验后修改文档 → 证据 digest 失效；
- 删除 gate 事件 → 必失败；
- 换命令或退出码非 0 → 必失败；
- 同证据与策略重放 → 判定一致。

**验收判据**：`step-gate` 能机械输出「哪些步骤有执行证据、哪些只有文本声明」；高风险批次不得仅凭文本声明通过。

### 7.5 P1-3：按风险强制独立语义 Review

**最小改动**：

- 复用现有 T1 强制升级条件：RULE / DC / 门禁 / 真值源 / 运行时改动 → 必须独立 Review；
- 低风险 T3 不增加强制成本；
- 建立小型 reviewer 标注集（历史真实缺陷 + 干净样本），分别报告 catch 与 false-rejection；
- reviewer 输入 digest 必须对应最终版本。

**故障注入**：在标注集中注入已知缺陷与无缺陷样本；变更有缺陷但无独立 Review 时不得标 `done`。

**验收判据**：高风险批次无独立 Review → 不能闭合；reviewer 的 catch 与误拒率有读数；不以「异构基座」代替校准。

### 7.6 P1-4：修订外部有效性预注册的效果与成本指标

**最小改动**：

- 在执行前补：任务终态、客观人工工时、后续缺陷、总成本、门禁误报；
- 澄清「本仓只读」与「执行记录存外部仓侧」的干预协议；
- 阈值继续冻结，修改即作废；
- 主观满意度与客观工时分列。

**验收判据**：预注册修订版本化；执行后不得移动阈值；允许并如实登记负结果。

### 7.7 P2：可移植性、维护成本与供应链

1. **Core / Full 两档迁移声明**：Core = 十步规范 + 仓内校验器 + 基础 session；Full = 额外包含可执行的 B 类断言审计器。验收：全新克隆无源项目路径时，Core 明确可用；Full 有固定离线 demo 且结果一致。
2. **减少人工派生视图回写**：优先自动生成高频汇总行与 compact 当前状态；保留 append-only 历史；生成物带 `source_digest`，`--check` 防漂移。目标是减少人工触点，不再增加统计声明。
3. **供应链加固（低优先级）**：Actions 固定到完整 SHA 并自动更新；多 PR 并行时再考虑 `strict: true`；单人仓不机械要求 PR approver；in-toto / Sigstore 只在跨仓发布或 RPC 外部副作用阶段引入。

### 7.8 排序总表

| 顺序 | 项 | 最小改动 | 故障注入 | 验收判据 |
|---|---|---|---|---|
| 1 | P0-1 批次绑定 | session-first + 关系集 + 迁移边界 | 旧 session / 无关 session / 多 feature | 旧 session 放行 = 0 |
| 2 | P0-2 完整链 | 自动路径派生期望链 + legacy 模式 | 0/5、1/5、4/5、5/5 | 自动与显式结论一致 |
| 3 | P1-1 真实 runner 回归 | 集成测试 + 触发面补齐 | 4 类变异体 | 变异体必红 |
| 4 | P1-2 执行证据 | gate 事件 + digest + 策略版本 | 改文档 / 删 gate / 换命令 | 文本声明不可替代执行证据 |
| 5 | P1-3 风险化独立 Review | 高风险强制 + 标注集 | 缺陷 / 干净样本 | 无独立 Review 不得 done |
| 6 | P1-4 外部有效性 | 补终态 / 工时 / 成本 / 误报 | 阈值移动 / 负结果 | 预注册可复核 |
| 7 | P2 可移植 / 维护 / 供应链 | Core-Full + 生成化 + SHA | 旧克隆 / 漂移 | 声明与可执行能力一致 |

---

## 8. 与图结构升级的关系

1. **图设计本身不是当前最高风险**：A 薄图路径、G1/G2/G3 分离、任务卡唯一接口、默认关闭、S2 前不固化拓扑，均成立。
2. **在 P0 修复前扩大图能力会放大流程证据失真**：如果图变更的 session 仍可能被旧批次替代，图 pilot 的「已验收」同样不可信。
3. **建议顺序**：修 P0-1 / P0-2 → 真实 runner 与执行证据 → graph DESIGN / S1 只读工具 → 一个真实 S2 pilot → 按终态、成本与故障注入结果决定是否继续。
4. **RPC 侧维持**：at-least-once 恢复假设、幂等键、产物 digest、原子 claim、lease ≠ fencing；不承诺端到端 exactly-once。
5. **P4 三判据不变**：P3 跑通 + 具体不可表达实例 + 实测成本；未满足前不引入完整引擎。

---

## 9. 明确不建议做

- 现在引入 LangGraph / Temporal / 图数据库或统一三图内核；
- 给所有轻批强制增加第二模型 Review；
- 继续增加人工汇总计数与形式化门禁数量；
- 把「异构 reviewer」直接当作质量保证；
- 把当前全绿或预注册文件当作外部有效性证明；
- 把 21 个主 P / 后续 P 差异全部改成冲突失败。

---

## 10. 未决项登记

- **U-1 当前批次绑定形态未定**
  - **判据**：pre-commit 能仅凭本次提交机械确定 PID 与 session，且旧 session 无法放行；
  - **触发条件**：用户裁决 O3 并批准 Phase 1 立项（§11.7）；
  - **当前倾向**：**新 P 行声明优先 → 变更 session 证据 → 维护模式回退**（§11 推荐 O3）；静态最新 P 已实测否决；
  - **证据等级**：E1（缺陷与方案成本已实测）/ Phase 1 已实施（P-130）；Phase 2 待裁决。

- **U-2 完整链迁移边界未定**
  - **判据**：新批次强制完整链、历史批次不回溯判红，边界机械可判；
  - **触发条件**：P0-2 设计；
  - **当前倾向**：**已裁决 129（2026-10-26）**：边界只作用于维护模式与仅登记模式；显式 batch/session/branch 声明带文档改动一律要求 ≥1 个 5/5，不因 P<129 豁免；runner `FINALIZE_IMPACT_MIN_P=92` 保持独立，不合并；**runner 声明面已改为显式 `--expect` / `--legacy`（P-132）**——隐式 legacy 下「忘记声明完整链」与「有意 legacy」机械读数不可区分；
  - **证据等级**：E1（P-129/P-130 均 5/5；128/129 边界与 0/5、4/5 注入测试已补，P-131；隐式 legacy 移除后 selftest 83/83，P-132）。

- **U-3 真实 runner 集成测试成本未测**
  - **判据**：CI 增量时间可接受，且 4 类变异体全部被捕获；
  - **触发条件**：P1-1 实施前；
  - **当前倾向**：stdlib unittest + 临时目录，零新依赖；
  - **证据等级**：待测。

- **U-4 每步必需 gate 事件集未定**
  - **判据**：能机械列出「哪些步骤缺执行证据」且不误伤历史 session；
  - **触发条件**：P1-2 设计；
  - **当前倾向**：只强制 `verify` 步，其他步骤先登记；
  - **证据等级**：待核。

- **U-5 reviewer 校准集规模与成本未定**
  - **判据**：能分别报告 catch 与 false-rejection，且成本可承受；
  - **触发条件**：P1-3 实施前；
  - **当前倾向**：先用历史真实缺陷 + 干净样本各 ≥10；
  - **证据等级**：待测。

- **U-6 外部有效性指标修订未执行**
  - **判据**：预注册版本化补充终态 / 工时 / 后续缺陷 / 成本 / 误报；
  - **触发条件**：用户点名 G-11b 或批准修订；
  - **当前倾向**：先修订再执行，避免只优化文档指标；
  - **证据等级**：E1（现状已读）。

- **U-7 图 S2 pilot 对象仍未选**
  - **判据**：具备真实片间依赖 / 写汇聚 / 迭代需求的任务；
  - **触发条件**：P0 修复完成；
  - **当前倾向**：承 graph RESEARCH H1，不提前固化拓扑；
  - **证据等级**：待选。

- **U-8 `strict: true` 对单人流程的影响未测**
  - **判据**：多 PR 并行时仍能合并且不产生额外等待；
  - **触发条件**：出现并行 PR；
  - **当前倾向**：暂维持 `strict=false`；
  - **证据等级**：E1（现状已读）。

- **U-9 派生视图生成化的收益 / 成本未测**
  - **判据**：人工回写触点下降且 `--check` 仍可防漂移；
  - **触发条件**：视图回写欠账再次复发；
  - **当前倾向**：先生成高频汇总行，不整体拆分文档；
  - **证据等级**：待测。

- **U-10 U-1 Phase 1 门禁实施未立项**
  - **判据**：O3 解析器落地，§11.6 的 11 类故障注入全过，旧 session 放行路径为 0；
  - **触发条件**：用户批准 Phase 1 + 完成 DESIGN；
  - **当前倾向**：边界 P≥129；先本地 hook，再 CI 变更集；
  - **证据等级**：方案已分析（§11）/ 已实施（P-130，2026-10-26）。

---


## 11. U-1 方案分析：当前批次绑定

> **检索说明（降级链）**：`mcp_english-search_search_web` 对 4 组查询均返回 `status 404`，判定为工具端点不可用；改用 `WebSearch` + `WebFetch` 直接读取官方文档与标准页。该降级不影响结论，但按 SPEC_PROCESS 的检索纪律如实登记。

### 11.1 不变量与三个子问题

U-1 的目标不是「让静态映射更聪明」，而是让下面这条不变量在提交门禁上成立：

> 对任意受门禁约束的变更集 C，存在一个**当前批次声明** B(C)；C 中每个管线文档都属于与 B(C) 关联的 feature；B(C) 的 session 满足该档位的完整性；任何旧批次 session 都不能替代 B(C)。

拆成三个子问题：

1. **识别当前批次**：C 属于哪个 P？
2. **关联文档**：C 中每个四文档属于哪些 feature，是否都被该 P 覆盖？
3. **证明完整性**：该 P 的 session 是否满足档位要求，且不能拿旧 session 充数。

当前实现只回答了「这个 feature 曾经关联过某个 P」，没有回答「C 属于哪个 P」。

### 11.2 实测约束

【A】A-29 pre-commit 官方文档（T1）：`pass_filenames` 默认 `true`；`files` 决定哪些文件进入 hook；`stages` 可选择 git hook 阶段（含 `commit-msg` 与 `prepare-commit-msg`）。来源：[pre-commit.com](https://pre-commit.com/)。

【A】A-30 Git `githooks` 官方文档（T1）：`pre-commit` 不接收参数，且在**获得提交信息之前**运行；`commit-msg` 接收 message 文件；`prepare-commit-msg` **不被 `--no-verify` 抑制**。来源：[git-scm.com/docs/githooks](https://git-scm.com/docs/githooks)。

【A】A-31 Git `git-diff` 官方文档（T1）：`A...B` 等价于 `git diff $(git merge-base A B) B`，用于计算分支相对共同祖先的变更集。来源：[git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)。

【A】A-32 Gerrit Change-Id 官方文档（T1）：Change-Id 位于提交信息 footer；共享同一 Change-Id 的多个 patchset 视为同一变更；amend 时保留。来源：[Gerrit Change-Ids](https://gerrit-documentation.storage.googleapis.com/beta/user-changeid.html)。

【A】A-33 Changesets 官方 dictionary（T1）：changeset = 「an intent to release a set of packages at particular bump types with a summary of the changes made」；存放于 changeset folder，可叠加。来源：[changesets dictionary](https://raw.githubusercontent.com/changesets/changesets/HEAD/docs/dictionary.md)。

【A】A-34 towncrier 官方文档（T1）：读取 news fragments 生成 changelog，避免所有人写同一文件产生冲突。来源：[towncrier docs](https://towncrier.readthedocs.io/en/stable/)。

【A】A-35 NVD CVE-2025-30066（T1）：`tj-actions/changed-files` 46 之前版本受影响；v1–v45.0.7 标签于 2025-03-14/15 被改指向 commit `0e58ed8`，可在 Actions 日志泄露 secrets。来源：[NVD](https://nvd.nist.gov/vuln/detail/cve-2025-30066)。第三方报告称影响 23,000+ 仓库（T2，未回原文）。

【A】A-36 本仓 session 机械枚举（E1，2026-10-26）：`specwf-p*.jsonl` 共 **148** 个，覆盖 **109** 个 PID；**7** 个 PID 有多个 session（P-042 有 **24** 个、P-050 有 10 个）；**8** 个 session 少于 5 步（最大编号 P-051）；`session_start` 事件**使用 0 次**。

【A】A-37 真实 runner 探针（E1）：临时目录构造 `specwf-p999-...v9`（1 步）与 `...v10`（5 步），`step-enforce --pid P-999` 选中 **v9**（字典序 `v10 < v9`），输出「1/5 步」并 **exit 0**。

【A】A-38 `step_enforce.py` 只处理以 `spec/` 开头的参数；直接传 session 文件时 feature 集为空并 exit 0；session 文件不在 `step-enforce` hook 的 `files` 正则内（E1）。

【A】A-39 映射源结构（E1）：PROGRESS **128** 行 P 记录中，**27** 行没有任何 `spec/<feature>/` 链接，其余行含 2–26 个链接；`CODE_WIKI §9` **40** 行中，单行含 1–33 个 P 编号，**13** 行的 P 编号非升序。

【A】A-40 静态 first→max 实测（E1）：40 个 §9 行中 **15** 行会改变映射；例：`doc-contract` 003→106、`precommit-dc-validator` 007→106、`project-console` 042→102、`academic-writing-workflow` 040→124。

【A】A-41 当前 CI 的 `step-enforce` 以 `git ls-files 'spec/*/*.md'` 传入**全量文档**，不是变更集（E1）。

【A】A-42 本仓 P 行实践（E1）：P-125 与 P-127 的 P 行均在与文档同一提交中以 `done` 新增（`git show 7a91e01` / `git show e2c6beb`）；这是当前实践，不是普遍保证。

**表 11.1 约束 → 设计含义**

| 实测 | 数值 | 对 U-1 的约束 |
|---|---|---|
| 多 session PID | 7 个；P-042 24 个 | 不能依赖「文件名末位」；必须显式声明或使用变更 session |
| 版本后缀排序 | `v10 < v9` | 当前 `sorted()[-1]` 会选错；需自然排序或废除此启发式 |
| 不完整 session | 8 个，max P-051 | 完整链强制必须有历史边界 |
| `session_start` | 0 次使用 | 可作为 Phase 2 schema 扩展，但当前无先例 |
| PROGRESS 多链接 / 零链接 | 27 行零链接；2–26 链接 | 行内「首个链接」不能作为批次绑定 |
| §9 多 P / 非升序 | 1–33 个 P；13 行非升序 | 首/末/最大都不是语义安全的「当前批次」 |
| 静态 max P | 15/40 行会变 | 静态最新 P 不能作为终态门禁 |
| CI 全量文档 | 非变更集 | CI 必须改为 merge-base 变更集 |
| P 行同提交新增 | P-125/P-127 实测 | 新 P 行可作为批次声明，但需门禁固化 |

### 11.3 候选方案

**O0 维持现状**：`feature → 主 P` 单值映射 + 文件名末位 session。成本最低，但保留 P0。

**O1 静态最新 P**：把 §9 行内 P 编号改为取**数值最大**，PROGRESS 兜底保持首个链接。改动面小，但仍是静态单值。

**O2 变更 session 优先**：hook 同时接收四文档与 session 文件；由本次变更的 session id 解析 PID；四文档的 feature 必须与该 PID 有关联。无 session 变更时回退旧映射。

**O3 新 P 行声明 + session 证据 + 维护模式**：以本提交新增/修改的 P 行为批次声明；否则以变更 session 为证据；否则仅允许「维护模式」（格式类改动）。批次模式下四文档 feature 必须由该 P 行的 spec 链接覆盖，且 session 完整。

**O4 独立 batch manifest**：新增 `batches/<P>.json`，显式登记 PID、features、session、tier、doc digests；hook 与 CI 只读 manifest。显式、可扩展，但新增工件与双真相源。

**O5 commit trailer / Change-Id 风格**：提交信息 footer 写 `Batch: P-129` / `Session: specwf-p129-...`；由 `commit-msg` 或 `prepare-commit-msg` 校验。`pre-commit` 阶段看不到提交信息，因此无法替代现有 L1。

### 11.4 五维对比

> 评分为相对判断；「改动面」按代码与配置触点计，不按时间计。等权仅用于排序，不作量化结论。

| 方案 | 改动面 | 收益 | 兼容 | 维护负担 | 升级潜力 | 结论 |
|---|---|---|---|---|---|---|
| O0 现状 | 无 | 无 | 高 | 无 | 无 | 基线；P0 保留 |
| O1 静态最新 P | 小（`spec_map` + 少量测试） | 低—中（15/40 变化，含错误绑定） | 高 | 低 | 低 | **否决** |
| O2 session 优先 | 中（hook 面 + resolver + CI + 测试） | 中 | 中（chore / 多 commit 批次会误伤） | 中 | 高 | 作为 O3 组件 |
| **O3 混合** | 中（resolver + PROGRESS diff + 维护模式） | **高** | 高（新批次边界可设） | 中 | 高 | **推荐** |
| O4 manifest | 高（新工件 + schema + 生成器） | 中—高 | 低（新批次都要建 manifest） | 高 | 最高 | 暂缓 |
| O5 trailer | 中（commit-msg / prepare-commit-msg + CI 解析） | 中 | 低（提交习惯 + L1 不可见） | 中 | 高 | 跨仓阶段再评估 |

### 11.5 为何否决「静态最新 P」

O1 看起来能立刻把 graph 从 P-125 改到 P-127，但机械实测暴露了两个反例：

- `doc-contract` 的 §9 行最大 P 是 **P-106**，而 P-106 是「DC5 版本引用一致性」工具批，其 session 记录的是 `dc_validator` / `PLAN v1.9` 的改动，不是一次新的 doc-contract 文档修订；
- `precommit-dc-validator` 的最大 P 同样是 **P-106**，而该 feature 的主批是 P-007/P-008。

如果按 max P 绑定，未来一次 doc-contract 文档修订会被 P-106 的旧 session 放行——这正是 P0 的另一种形态，不是修复。**任何静态单值映射（首个 / 末个 / 最大）都无法区分「这个 P 曾经改过这个 feature」与「本次变更属于这个 P」。** 因此 O1 只能作为诊断读数，不能作为门禁语义。

### 11.6 推荐：O3 混合解析器

**声明优先级**（从强到弱）：

1. **新 P 行**：staged `docs/PROGRESS.md` 出现新的 `| P-\\d{3} |` 行（或状态从 `pending` 变为 `done`）⇒ 该 P 为当前批次；该行的 `spec/<feature>/` 链接定义允许的 feature 集；
2. **变更 session**：没有新 P 行，但本次提交包含 session 文件 ⇒ 由 session id 解析 PID；四文档 feature 必须与该 PID 有关联；
3. **分支名辅助**：没有新 P 行 / session，但当前分支名匹配 `p(\\d{3})` 且该 PID 有完整 session ⇒ 作为弱声明，输出 `branch-declared`；
4. **维护模式**：以上皆无 ⇒ 仅当四文档改动是**格式类**（`git diff -w` 为空）时放行，输出 `maintenance-only`，**不得声明批次完成**；
5. **否则失败**：语义性四文档改动但无任何声明 ⇒ exit 1。

**完整性规则**：

- 批次模式：本次声明的 P 至少有一个 **5/5 步** session；同一 P 的多个变更 session 必须各自内部合法，且至少一个完整；
- 维护模式：该 feature 的既有映射 P 至少有一个完整 session，否则失败；
- 历史边界：`P < BATCH_BINDING_MIN_P` 走 legacy；建议 `BATCH_BINDING_MIN_P = 129`（P-128 为本次评审批，已完整；P-001~P-128 不追溯）。

**关联规则**：

- 新 P 行有 `spec/<feature>/` 链接 ⇒ 每个变更的四文档 feature 必须出现在该 P 行的链接集内；新批次 P 行若 0 链接 ⇒ 失败（新批次必须声明 feature）；
- 无新 P 行 ⇒ 用 `spec_map` 的 feature→P 关系集做「至少一个关联」校验，并要求 session PID 是该 feature 的**当前声明 P**（§9 行内最大 P）或分支声明 P。

**输出与退出码**：

- 必须打印 `mode`（batch / session / branch / maintenance）、`pid`、`session`、`relation_source`；
- exit 0 = 通过；1 = 违规；2 = 映射缺位，**按失败处理**（修正 `step_enforce.py` 当前「提示，不阻断」的文案）。

**表 11.2 故障注入矩阵**

| # | 注入 | 期望 |
|---|---|---|
| 1 | 改 graph 文档 + 旧 P-125 session，无新 P 行 | 失败（无当前声明） |
| 2 | 改 graph 文档 + 新 P-129 行 + P-129 完整 session | 通过（batch） |
| 3 | 新 P-129 行 + 只有 P-125 session | 失败（PID 不匹配） |
| 4 | 新 P-129 行 + P-129 1/5 步 session | 失败（完整链） |
| 5 | 一提交改两个 feature + P-129 行链接两者 + 一个 5 步 session | 通过（batch 多 feature） |
| 6 | 只改 session，不改四文档 | 通过（session 自证；若 session 不完整则失败） |
| 7 | 只做行尾归一 / 空白改动，无声明 | 通过（maintenance-only，输出警告） |
| 8 | 语义性四文档改动，无声明 | 失败（exit 1） |
| 9 | 新 P 行 0 个 spec 链接 | 失败（新批次未声明 feature） |
| 10 | `v9` 与 `v10` 两个 session 同时存在 | 必须按自然序选择，不得选 `v9` |
| 11 | CI 与本地对同一变更集 | 输出 mode/pid/session 一致 |

### 11.7 分阶段路线

- **Phase 1（P0 修复）**：实现 O3 解析器；`BATCH_BINDING_MIN_P = 129`；本地 hook 接收四文档 + session + PROGRESS；CI 改为 `git diff --name-only base...head` 的变更集；补 11 类故障注入测试。**验收**：上表 11 项全过；旧 session 放行路径为 0；维护模式不能声明批次完成。
- **Phase 2（证据增强）**：新增 `session_start` 事件，`input.metadata = {pid, features, tier}`；`verify` 步记录变更文档 digest；gate 重算 digest。**验收**：验后修改文档必失败；同证据与策略重放判定一致。
- **Phase 3（跨仓/外部副作用）**：在 RPC 外部副作用或跨仓发布时，引入 manifest / in-toto / SLSA attestation；本仓纯文档阶段不做。**验收**：subject digest、策略版本、验证者身份可校验。

### 11.8 外部锚点

| 来源 | 事实 | 对 U-1 的用法 | 等级 |
|---|---|---|---|
| [pre-commit docs](https://pre-commit.com/) | `pass_filenames` 默认 true；`files` / `stages` 可配 | hook 可同时接收文档、session、PROGRESS；阶段选择影响可见信息 | T1 |
| [Git githooks](https://git-scm.com/docs/githooks) | `pre-commit` 在提交信息之前运行；`prepare-commit-msg` 不被 `--no-verify` 抑制 | trailer 方案不能替代 L1；只能作为 commit-msg 层补充 | T1 |
| [git-diff](https://git-scm.com/docs/git-diff) | `A...B` = merge-base 到 B | CI 必须用变更集，不得用全量 `git ls-files` | T1 |
| [Gerrit Change-Id](https://gerrit-documentation.storage.googleapis.com/beta/user-changeid.html) | footer 中的稳定 Change-Id 绑定多个 patchset | 「稳定变更身份」可行，但需外部系统或专门 hook 维护 | T1 |
| [Changesets](https://raw.githubusercontent.com/changesets/changesets/HEAD/docs/dictionary.md) | changeset = 发布意图 + summary，存于文件夹 | O4 manifest 的社区同构；显式但多一个工件 | T1 |
| [towncrier](https://towncrier.readthedocs.io/en/stable/) | news fragment 逐条记录，避免单文件冲突 | fragment 模式适合变更声明，但本仓已有 P 行，无需重复 | T1 |
| [CVE-2025-30066](https://nvd.nist.gov/vuln/detail/cve-2025-30066) | `tj-actions/changed-files` 标签被改指向恶意 commit | 不引入第三方 changed-files action；用 git 自算变更集，Actions 固定 SHA | T1 |
| [SLSA v1.2](https://slsa.dev/spec/v1.2/verifying-artifacts) | 验证 subject digest、builder、externalParameters | Phase 3 的 attestation 形态 | T1 |
| [in-toto](https://in-toto.io/) | link metadata 记录步骤、材料与产物 | Phase 3 的跨仓链路形态 | T1 |

### 11.9 结论与不做什么

- **结论**：U-1 的终态应是 **事件绑定，而非静态映射**；O3 混合以现有 PROGRESS + session 为真值源，成本最低、兼容最好、可升级。
- **不做**：不把 max P 改成门禁；不引入 manifest / commit trailer / 第三方 changed-files action；不在 Phase 1 做签名或透明日志。
- **待裁决**：`BATCH_BINDING_MIN_P` 取 129 还是更早的 52（当前不完整 session 最大 P-051）；新 P 行 0 链接是否一律失败；维护模式是否只允许 `git diff -w` 为空。


## 12. 参考文献

按第一作者 / 机构字母序；括号内为本次核验状态。

1. Axelsson, S. *The Base-Rate Fallacy and the Difficulty of Intrusion Detection*（2000）——T2，子代理摘要（P-127 已用）。
2. Becker, J., Rush, N., Barnes, E., Rein, D. *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*（arXiv:2507.09089v2）——T1，2026-10-26 回 abs。
3. Chen, W.-L., Wei, Z., Zhu, X., Feng, S., Meng, Y. *Do LLM Evaluators Prefer Themselves for a Reason?*（arXiv:2504.03846v3）——T1，回 abs。
4. Google / SLSA. *Build: Verifying artifacts*（SLSA v1.2，Approved）——T1，回 slsa.dev。
5. Guo, J., Gu, S., Jin, M., Lavaei, J. *Groundability, Not Scale Alone: When Weak Reviewers Can Audit Strong Coding Agents*（arXiv:2610.01023v1）——T1，回 abs。
6. Huang, J. et al. *Large Language Models Cannot Self-Correct Reasoning Yet*（arXiv:2310.01798，ICLR 2024）——T2，子代理摘要。
7. Kleppmann, M. *How to do distributed locking*（2016-02-08）——T2，子代理摘要。
8. NIST. *AI Risk Management Framework 1.0*（NIST AI 100-1，2023-01-26）与 *Generative AI Profile*（NIST AI 600-1，2024-07-26）——T2，子代理摘要。
9. OpenLineage. *Object Model* v1.54.0——T2，子代理摘要。
10. OpenTelemetry. *Inside the LLM Call: GenAI Observability with OpenTelemetry*（2026-05-14）——T2，子代理摘要。
11. Sigstore. *Bundle Format* v0.3.2（2025-01-14）——T2，子代理摘要。
12. Temporal. *Architecture* / *Activity Definition*——T2，子代理摘要。
13. Torres-Arias, S. et al. *in-toto: Providing farm-to-table guarantees for bits and bytes*（USENIX Security '19）——T2，子代理摘要。
14. Tufano, M., McClure, J., Cambronero, J., et al. *Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation*（arXiv:2608.17177v2；DOI 10.1145/3842652.3843195）——T1，回 abs。
15. W3C. *PROV-DM: The PROV Data Model*（Recommendation，2013-04-30）——T1，回原文。
16. Yao, S., Shinn, N., Razavi, P., Narasimhan, K. *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*（arXiv:2406.12045v1）——T1，回 abs。
17. Yao, S., Wang, H., Sen, K., Chen, S., Ray, B., Song, D. *TestJack: Should you trust the results in coding benchmarks?*（arXiv:2610.10619v1）——T1，回 abs。
18. 其他子代理摘要来源：arXiv:2505.23419v2、arXiv:2512.10218v2、arXiv:2609.11987v1、arXiv:2609.35832v1、arXiv:2302.06590v1、Chubby OSDI 2006、Azure Durable Task——T2，未逐条回原文。

---

## 附录 A：A 类断言索引

A-1~A-20 为本仓机械实测 / 源码直读；A-21~A-28 为已回原文的外部一手来源 / 标准原文；A-29~A-35 为本次核验的官方文档与安全公告；A-36~A-42 为 U-1 专项实测。逐条证据已在 §3~§5、§11 就地给出，此处不重复。

## 附录 B：B 类推断（机读登记）

```json
[
{"id": "B1", "claim": "全绿 ≠ 当前变更被当前批次验证：自动门禁可能用旧批次 session 放行。", "basis": "A-4~A-9"},
{"id": "B2", "claim": "单值 feature→PID 映射在结构上无法表达多修订批次；21 个差异是模型结果，不是偶发 bug。", "basis": "A-5/A-6"},
{"id": "B3", "claim": "expect=None 使完整链成为打印提示而非硬门禁；自动与显式路径结论不一致。", "basis": "A-8/A-9"},
{"id": "B4", "claim": "仅用 stub 的黑盒测试无法捕获真实 runner 的完整性与 session 选择缺陷。", "basis": "A-9/A-10"},
{"id": "B5", "claim": "本地 hook 触发面遗漏核心 runner，造成本地与 CI 反馈不对称。", "basis": "A-11/A-12"},
{"id": "B6", "claim": "required check + enforce_admins 是实质强项；strict=false 只留下多 PR 并行时的陈旧风险。", "basis": "A-3"},
{"id": "B7", "claim": "固定单测会漏需求并遭受 reward hacking；评测器本身需要增广与抽审。", "basis": "A-22"},
{"id": "B8", "claim": "Review 质量主要取决于可核验的执行证据，而非 reviewer 规模；必须同时报告 catch 与误拒。", "basis": "A-23"},
{"id": "B9", "claim": "异构基座不是质量保证；自偏好既有合理部分也有有害部分。", "basis": "A-24"},
{"id": "B10", "claim": "自纠无外部反馈可能退化；净准确率会掩盖对→错，需转移矩阵与回滚。", "basis": "子代理 A T2 来源（自纠两篇）"},
{"id": "B11", "claim": "Agent 验收应报告终态、pass^k、成本与人工裁断，而非一次全绿。", "basis": "A-25"},
{"id": "B12", "claim": "污染控制应进入任务卡：登记公开时间、私有切分与记忆探针。", "basis": "子代理 A T2 来源"},
{"id": "B13", "claim": "外部效果只能条件化声称；客观工时可能与主观感受相反。", "basis": "A-26"},
{"id": "B14", "claim": "provenance 应绑定制品 digest、策略版本与验证者，而非只写 pass 文本。", "basis": "A-27/A-28"},
{"id": "B15", "claim": "恢复语义应按 at-least-once + 幂等键 + digest 设计，不承诺端到端 exactly-once。", "basis": "子代理 B T2 来源"},
{"id": "B16", "claim": "lease ≠ fencing；旧 holder 恢复后仍可能写，必须由资源侧校验单调 token。", "basis": "子代理 B T2 来源（Chubby / Kleppmann）"},
{"id": "B17", "claim": "高风险批次应强制独立语义 Review，低风险 T3 不应增加同等成本。", "basis": "A-15/A-16 + B8"},
{"id": "B18", "claim": "「规范文本自包含」不等于「完整 B 类工具闭环可重放」；迁移声明应分 Core / Full。", "basis": "A-14"},
{"id": "B19", "claim": "人工派生视图回写是结构性成本与漂移源；应生成高频汇总、保留 append-only 历史。", "basis": "A-13"},
{"id": "B20", "claim": "图升级应排在他门禁保真度修复之后；薄图路径保留，完整引擎继续后置。", "basis": "A-18 + B1/B2/B3"},
{"id": "B21", "claim": "静态单值映射（首个/末个/最大 P）在语义上不足：15/40 行会变，且 doc-contract / precommit 的 max P 是交叉工具批，不是该 feature 的文档批。", "basis": "A-39/A-40"},
{"id": "B22", "claim": "session-first 单独不足：多 session PID、v10<v9 排序陷阱、chore 提交与多 commit 批次会产生误判。", "basis": "A-36/A-37"},
{"id": "B23", "claim": "本仓 P 行「同提交新增 done」的实践使新 P 行可作为批次声明，但必须门禁化，不能依赖习惯。", "basis": "A-42"},
{"id": "B24", "claim": "O3 混合（新 P 行 > 变更 session > 维护模式）是成本/收益最优；不需要新 manifest。", "basis": "A-29/A-30/A-42 + B21/B22/B23"},
{"id": "B25", "claim": "commit trailer 更接近 Gerrit Change-Id，但 pre-commit 阶段看不到提交信息，不能替代 L1；只能作为 CI / commit-msg 层补充。", "basis": "A-30/A-32"},
{"id": "B26", "claim": "不应引入第三方 changed-files action；应使用 merge-base 变更集，并将 Actions 固定到完整 SHA。", "basis": "A-31/A-35"},
{"id": "B27", "claim": "内容 digest 绑定应作为第二阶段：先解决批次识别，再解决「验后修改」。", "basis": "A-19/A-28 + B24"}
]
```

## 附录 C：C 类决策与假设区

**C 类决策**：

- C-1 本轮只评审落档，不改代码 / 配置 / 门禁；
- C-2 P0-1 采用「session-first + 关系集 + legacy 回退」，不把历史差异全部判冲突；
- C-3 P0-2 自动路径派生期望链，历史批次保留 legacy 模式；
- C-4 执行证据复用现有 `gate` 事件，不新建平台；
- C-5 高风险批次强制独立语义 Review，低风险 T3 不增加成本；
- C-6 图升级延后到 P0 修复之后，继续走 A 薄图路径；
- C-7 否决「静态最新 P」作为门禁语义（仅可作诊断读数）；
- C-8 采用 O3 混合：新 P 行声明 > 变更 session > 维护模式；新批次边界 P≥129；
- C-9 暂不引入 manifest / commit trailer / 第三方 changed-files action；内容 digest 留 Phase 2。

**假设区**：

- [H1] 当前批次绑定的具体实现形态未定（session-first / 关系集 / 混合）。
- [H2] 完整链迁移边界（按 P 编号或提交时间）未定。
- [H3] 真实 runner 集成测试的运行时成本未测。
- [H4] 每步必需 gate 事件集未定。
- [H5] reviewer 校准集规模与成本未定。
- [H6] 外部有效性指标修订未执行（需用户裁决）。
- [H7] 图 S2 pilot 对象未选。
- [H8] `strict: true` 对单人流程的影响未测。
- [H9] 派生视图生成化的收益 / 成本未测。
- [H10] 「新 P 行」判定语义（新增 / 状态变更 / 仅文案订正）未在 DESIGN 定稿。
- [H11] 完整链边界取 P-129 还是 P-052（当前不完整 session 最大 P-051）未裁决。
- [H12] 多 PID / 多 session 提交的选择与聚合规则未定。
- [H13] `session_start` metadata 是否启用未定（当前 0 使用）。
- [H14] 文档 digest 绑定与 gate 事件的 Phase 2 范围未定。
