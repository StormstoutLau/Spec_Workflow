# 调研文档：框架深度评审与前沿对标

---

id: framework-deep-review-RESEARCH
type: design
version: 1.22
status: draft
date: 2026-10-26
depends: [ADR-0010, FWK-ASSERTION]
upstream: null

---

> **Feature**: framework-deep-review（当前框架深度评审、前沿对标与分优先级升级建议）
> **创建日期**: 2026-10-26
> **修订**: v1.22（2026-10-28，P-150：**PR 面读数订正 + evil 侧远端路径裁决**——① 订正 P-145~P-149 五行「PR 面阶段 1 未命中」的错误表述（实测 5 个 PR run 均命中 GitHub 合成 merge ref 并判 `无 evil 内容`）；② 新增 §14.8 两条 evil 侧构造路径对比（社区实践分级）+ **裁决 = 路径 2（分支内构造合并提交 → 失败 PR）**；③ A 类计数不变）
> **修订**: v1.21（2026-10-28，P-149：**阶段 1 远端第 5 样本**——§14.7 追加真实 `push(main)` 读数（run `40676513311` / 合并提交 `64c6313` / `无 evil 内容（6 个受判路径均等于某一父）` / 墙钟 81 s 全绿）；同一断言 A-50 的第 5 远端样本，A 类计数不变）
> **修订**: v1.20（2026-10-28，P-148：**阶段 1 远端第 4 样本**——§14.7 追加真实 `push(main)` 读数（run `40666293529` / 合并提交 `fb01568` / `无 evil 内容（6 个受判路径均等于某一父）` / 墙钟 82 s 全绿）；同一断言 A-50 的第 4 远端样本，A 类计数不变）
> **修订**: v1.19（2026-10-28，P-147：**阶段 1 远端第 3 样本**——§14.7 追加真实 `push(main)` 读数（run `40663831556` / 合并提交 `023e456` / `无 evil 内容（6 个受判路径均等于某一父）` / 墙钟 66 s 全绿）；同一断言 A-50 的第 3 远端样本，A 类计数不变）
> **修订**: v1.18（2026-10-28，P-146：**阶段 1 远端第 2 样本**——§14.7 追加真实 `push(main)` 读数（run `40660622448` / 合并提交 `7bcce12` / `无 evil 内容（6 个受判路径均等于某一父）` / 墙钟 89 s 全绿）；同一断言 A-50 的第 2 远端样本，A 类计数不变）
> **修订**: v1.17（2026-10-28，P-145：**阶段 1 远端首次生效读数登记**——§14.7 追加真实 `push(main)` 读数（run `40603730644` / 合并提交 `e8154eb` / `无 evil 内容（6 个受判路径均等于某一父）` / 墙钟 88 s 全绿）；同一断言 A-50 的远端样本，A 类计数不变）
> **修订**: v1.16（2026-10-28，P-144：**U-11 合并面实测与关闭**——新增 §14.7（A-49 逃逸实测 / A-50 检测四态）；`step_enforce` 新增 `--check-merge`；§10 U-11 行 → 已实测并关闭；A 类 48 → 50）
> **修订**: v1.15（2026-10-28，P-143：**`push(main)` 补充读数登记**——§14.5 追加第 2 次真实 push 读数（run `40589457291` / 合并提交 `3bb7680` / 受判 1 个 / 墙钟 87 s 全绿）；A 类计数不变（同一断言 A-48 的第二样本））
> **修订**: v1.14（2026-10-28，P-142：**`push(main)` 合并面读数回填**——新增 §14.5（A-48：run `40585936395` / 合并提交 `adfec33` / verify 68 s 全绿 / merge skip + 受判 18 个）；原 §14.5 边界与回退顺延 §14.6；§10 U-11 补实测证据；A 类 47 → 48）
> **修订**: v1.13（2026-10-28，P-141：**CI 远端读数回填**——新增 §14.4（A-47：run `40579430749` / `22976eb` / verify 1m30s 全绿 / PR #58 SUCCESS）；原 §14.4 边界与回退顺延 §14.5；A 类 46 → 47）
> **修订**: v1.12（2026-10-27，P-140：**CI 逐提交遍历**——新增 §14（单次 diff 的两条独立假红面 A-45 / 四方案裁决 / 逐提交读数 A-46 / 合成合并提交实验 / 边界）；原 §14 参考文献顺延 §15；§10 新增 U-11（合并面残留）；A 类 44 → 46）
> **修订**: v1.11（2026-10-27，P-139：**P1-1 真实 runner 集成回归**——新增 §13（门禁缺口实测 A-43 / 最小改动 / 四类变异体 / 读数 A-44 / 边界）；§10 U-3 行状态改为「已实测」；原 §13 参考文献顺延 §14；A 类 42 → 44）
> **修订**: v1.10（2026-10-27，P-138：**U-9 执行件落地**——`console_gen` 新增 compact「当前状态」5 行块 + selftest S56（57 → 58）；§10 U-9 行状态由「P-138 候选」改为「已实施」；判据⑤（连续 3 批人工触点 ≤6 处）待复测；A/B/C/H 计数不变）
> **修订**: v1.9（2026-10-27，P-137：**U-10 C 实施——内容 digest 绑定门禁**——新增 §12（三处未决裁决 R1 finalize 时点 / R2 per-batch 作用域与 rebind / R3 边界 137 + 数据结构 + 六臂注入 + 残余风险）；原 §12 参考文献顺延为 §13；§10 U-10 行状态更新；A/B/C/H 计数不变）
> **修订**: v1.8（2026-10-27，P-136：**U-5 / U-6 / U-9 三裁决落档**——U-5 采 D.3 方案 C 分阶段〔Phase 1 = 20 项读数预注册、达标后扩 30+30 当门禁〕/ U-6 采 D.4 方案 E〔prereg v1.1 修订实施 + 不改名 + 新引用加限定〕/ U-9 采 D.5 方案 D〔否独立 SUMMARY.md，扩 CONSOLE = P-138 候选，C 先占 P-137〕；A/B/C/H 计数不变）
> **修订**: v1.7（2026-10-27，P-135：**U-10 / U-7 裁决与复审过程完整落档**——新增附录 E（时间线 / 两轮裁决 / 复审四偏差与幻觉排除确认）；C 候选批预标 P-135 顺延 **P-136**；A/B/C/H 计数不变）
> **修订**: v1.6（2026-10-26，P-134：**U-10 F 实施 + 归档数字订正**——CI step-enforce 段 fail-closed 化；D.0 订正 specwf 批次计数 152 → **151**（naive 子串误计）；§10 U-10/U-7 裁决落档）
> **修订**: v1.5（2026-10-26，P-133：**五项裁决子代理完整报告落档**——U-10 / U-7 / U-5 / U-6 / U-9 全文入附录 D；主臂复核三条读数订正；A/B/C/H 计数不变）
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
| A 事实类 | 50 | 本仓只读代码 / 机械实测（E1）+ 已回原文核验的外部一手来源（T1） |
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

- **U-3 真实 runner 集成测试成本：已实测（P1-1 已实施，P-139）**
  - **判据**：CI 增量时间可接受，且 4 类变异体全部被捕获；
  - **触发条件**：P1-1 实施前（**已于 2026-10-27 实施**）；
  - **当前倾向**：stdlib unittest + 临时仓（`SR_SESSIONS_DIR` / `SR_REWORK_REGISTRY` 注入），零新依赖；触发面已补 `tools/spec_runner/spec_runner.py`；
  - **证据等级**：**E1（A-43 / A-44）**——门禁缺口实测（单独改 runner 原先不触发任何本地 hook）+ 4/4 变异体被感知 + 新增 14 例（全套 36 → 50，全绿）+ 增量 **8.7 s**（同 `unittest discover` 命令口径）；**CI 远端增量未直接实测**（本批不推送）以本地同命令读数代理。

- **U-4 每步必需 gate 事件集未定**
  - **判据**：能机械列出「哪些步骤缺执行证据」且不误伤历史 session；
  - **触发条件**：P1-2 设计；
  - **当前倾向**：只强制 `verify` 步，其他步骤先登记；
  - **证据等级**：待核。

- **U-5 reviewer 校准集规模与成本：已裁决（采 D.3 方案 C 分阶段）**
  - **判据**：能分别报告 catch 与 false-rejection，且成本可承受；
  - **触发条件**：**用户裁决（2026-10-27，P-136）**：采 **D.3 方案 C（分阶段）**——Phase 1 预注册 = **10 缺陷 + 10 干净（共 20 项）配对读数**（同一 digest 双盲；基线臂 = RULE-4 单 Agent 自查、处理臂 = RULE-1 独立 Review、尽量 RULE-5 异构；catch = TP/(TP+FN)、误拒 = FP/(FP+TN)，报 Wilson 95% CI + McNemar 精确检验；ground truth 双标注 kappa ≥0.6）；**升级判据** = catch ≥0.70 ∧ 误拒 ≤0.20 ∧ ≥6 个单向不一致 ⇒ 扩 30+30；Phase 2 门禁只绑 T1 高风险、用置信界 + 容差（**不得 0/30 硬门**）、T3 不绑；回退点 = 门禁误拦 >2 次/季或单轮评审 >2h ⇒ 退回读数模式（样本库保留）；
  - **当前倾向**：Phase 1 读数执行 = **独立后续批**（样本构造约 7–10h；污染控制 = 评审臂不给 session / M7 / PROGRESS、生成臂与评审臂异 session 尽量异模型族、历史缺陷只作 dev set、测试集用冻结后新缺陷或跨仓样本并分列 seen/unseen）；
  - **证据等级**：E1（D.3 报告：M7 48 样本池实测 + Wilson / McNemar 复算——20 项 Wilson 区间宽约 ±17pp 仅支撑读数；30 缺陷仅支撑「catch 下界 ≥0.70」（需 ≥27/30）；「误拒 ≤0.10」需 0/60；真 catch 0.90 过「≥27/30」硬门仅 64.7% 概率）。

- **U-6〔framework-deep-review 命名空间〕外部有效性指标修订：v1.1 已修订、执行未启动**
  - **判据**：预注册版本化补充终态 / 工时 / 后续缺陷 / 成本 / 误报；
  - **触发条件**：**用户裁决（2026-10-27，P-136）**：采 **D.4 方案 E（修订 + 新引用加限定词，不改名）**——[EXTERNAL_VALIDITY_PREREG](../../docs/EXTERNAL_VALIDITY_PREREG.md) **v1.0 → v1.1** 已实施：§4.1 增 **M6-M10 五项辅助指标**（终态一致率 / 客观人工工时 / 后续缺陷密度 / 总成本三分列 / 门禁误报率；全带 N/A 规则、**不参与 §6 判据、不接门禁**；与 M7 证据账本及 `dc_validator` M1-M6 检查编号分属不同命名空间）+ 干预协议（对外部仓只读零写入；消解 §4「脚本归档本仓」与 §8「本仓只留指针」表述矛盾）+ §12 修订历史（**三锁** = §5/§6 与 M1-M5 表逐字不变 / M6-M10 不入门禁 / 修订注明依据）；**D.4 的 status 改 `registered` 建议未采纳**——DC2 枚举约束（`type: framework` 仅 active / deprecated）实跑 P1 拦截（P-136 verify 捕获），登记为已知残留；**改名 = 否**（`U-6` 全仓 266 处 / 14 文件 / 3 命名空间同名，改 U-6a/b 只消一个命名空间且破 P-068 历史锚点；**新引用一律加限定词「framework-deep-review U-6」**，旧文零改动）；
  - **当前倾向**：执行仍未启动（`registered / unexecuted`；触发 = 用户点名 G-11b 候选仓）；M6-M10 在候选仓的预计 N/A 率高（多数缺 session / 返工记录，D.4 §7），落盘前可再补、落盘后本节冻结；
  - **证据等级**：E1（D.4 报告 + prereg 全文直读；§6 冻结条款字面边界 =「执行开始后」⇒ 执行前修订合法——COS Registered Reports T1 锚：冻结方法不冻结结果，修订须在见数据前）。

- **U-7 图 S2 pilot 对象（实为 graph U-1，编号错位见 D.0）**
  - **判据**：具备真实片间依赖 / 写汇聚 / 迭代需求的任务，**且 graph S0 契约与 S1 只读工具已落地**；
  - **触发条件**：**用户裁决（2026-10-26）**：**Cpp_Hub 二次吸收第 1 批 = 首选候选，现在不启动**（graph 目录仅 RESEARCH.md，S2 无契约可测）；启动前置 = graph S0 DESIGN（`depends_on` / `join` / `iter_budget` / `join_policy` / `graph_version` 五字段 + fixture）+ S1 只读工具 + 第二轮吸收范围冻结（3 机制 → 3 片 + 1 join + 1 有界 Review 迭代）；
  - **当前倾向**：候选序 = Cpp_Hub 二次吸收 > Cpp_Hub 代码批走 RPC 卡 > Spec_Workflow 多阶段批 > Auto_Prover P3；pilot 读数入 pilot 报告、不进 M7（承 graph RESEARCH §13）；不固化拓扑；
  - **证据等级**：E1（D.2 实证画像：三条 INTERFACE 依赖链 / 多账本写汇聚 / 1−Φ 族第 4 例迭代闭环 / agent-run digest 装置；引用口径订正见 D.0 增补）。

- **U-8 `strict: true` 对单人流程的影响未测**
  - **判据**：多 PR 并行时仍能合并且不产生额外等待；
  - **触发条件**：出现并行 PR；
  - **当前倾向**：暂维持 `strict=false`；
  - **证据等级**：E1（现状已读）。

- **U-9 派生视图生成化：已实施（否独立 SUMMARY.md；采扩 CONSOLE，执行件 P-138 已落地）**
  - **判据**：人工回写触点下降且 `--check` 仍可防漂移；
  - **触发条件**：**用户裁决（2026-10-27，P-136）**：**不接受「独立 SUMMARY.md + 指针」**；采 **D.5 方案 D（扩展现有生成视图）**——`console_gen` 增 compact「当前状态」生成块 + 1 条 selftest，为 **P-138 候选**（Layer-1 单文件批；C〔digest 门禁〕先占 P-137 候选；含 project-console DESIGN / IMPLEMENTATION / CHECKLIST 对应更新 + 验收判据⑤ = 连续 3 批人工触点 ≤6 处且无 P-052/053/103 型欠账；回退 R-S1 = 删块与 selftest，删后与现状逐字节一致）；**P-138 已实施（2026-10-27）** = `docs/CONSOLE.md` 头部 `## 当前状态（compact）` 5 行（在册批次状态分布 / 最近批次 / session 覆盖 / 行动队列 / feature 阶段分布），逐行纯机械派生、零判断性文案；selftest S56（**57 → 58**）；project-console DESIGN **v1.18**（§4.2 D22 + I-13 + 回退点 R-9）/ IMPLEMENTATION **v1.24**（§9）/ CHECKLIST **v1.20**（F62）；**判据⑤ 待复测**（本批为首批样本；后 2 批复测后回填）；**A′ 升级路径保留** = 仅当扩视图后回写欠账仍复发（同族 ≥1 新例）才按 A′ 最小步骤升级（I-1 改「声明产物集」+ 引用块指针 + 同批删 CONSOLE 重复块防第三载体）；
  - **当前倾向**：拒绝理由 = compact 当前状态已有 100% 机械载体（CONSOLE `--check` 字节级防漂移），新增 SUMMARY 只增第三载体不降触点（Keep a Changelog 1.1.0 T1 锚：「不一致的日志与没有一样危险」）；触点实测 = 近 10 批每批必改 3 视图文件（CODE_WIKI 5–11 行 / PROGRESS 1–7 行 / CONSOLE 4–32 行），SUMMARY 不降 CODE_WIKI banner / §9 与 PROGRESS 汇总表的真实成本；**P-138 后** = 触点下降需 3 批样本才有读数（D.5 §4 / §7 不确定项①）；
  - **证据等级**：E1（D.5 报告：console_gen / repo_stats / spec_map 源码级取证 + `git numstat` 近 10 批触点表 + 8 条外部锚点〔7 T1〕；P-138 实施读数见 project-console IMPLEMENTATION A-28）。

- **U-10 Phase 2（证据增强）立项与批次边界**
  - **判据**：F（CI fail-open 修补）与 C（内容 digest 绑定）可分批实施、互不阻塞回退；
  - **触发条件**：**用户裁决（2026-10-26）**：F 单独立项 **P-134（已实施）**；C 不并入，另批候选（预标 P-135 → P-136 两次被占用 ⇒ **P-137 已实施**，2026-10-27）——三处未决已在 §12.2 裁决并落为机械判据（digest 记录时点 = **finalize**、per-batch 作用域 + 同 session rebind 留因、边界 `EVIDENCE_MIN_P = **137**`）；`session_start` 留 Phase 2b 单独裁决；
  - **当前倾向**：C 六臂注入落为 8 例（临时 git 仓 + 真实 runner，`tests/test_batch_binding.py` 20 → 28）；回退 = 边界常量置哨兵值（9999）降为观察；跨批 rebind 原因**不作要求**（理由见 §12.2 R2）；
  - **证据等级**：E1（批次 session gate/digest 读数：160 jsonl / **155 批次 session** / 5 非批次 / 批次最大 P = P-136 ⇒ 全 < 137，2026-10-27 实测；坏 base → git diff exit 128 且包装层跳过；41bb0c4/3bc99fa/c779e6d 三提交同改同一组文档 ⇒ per-batch 作用域必要；P-134 本地注入 5/5；P-137 注入 8/8）。

- **U-11 逐提交遍历的合并面残留**（**已实测并关闭（P-144）**）
  - **判据**：合并提交（≥2 父）的内容变更须有覆盖路径，且 `push(main)` 走查不因并集 diff 重复判红；
  - **触发条件**：出现 evil merge（合并结果含父提交均无的内容）导致漏检，或 `main` 的 push 走查出现并集式假红（P-140 已实施，2026-10-27）；
  - **当前倾向**：常规 diff 仍**显式跳过**（变更 = 父提交并集，逐父已被同循环覆盖）；**evil 内容**（两父皆无）由 `step_enforce --check-merge` 单独判红（P-144 实施），该内容须由后续声明批次承载；**不做并集 diff**（避免 P-140 假红复发）；
  - **证据等级**：E1（A-49 逃逸实测：同内容走合并解决 exit 0 / 走普通提交 exit 1；A-50 检测四态：evil→1、干净→0、=第一父→0、非合并→0；`push(main)` 面无并集假红，A-48）；**边界 = 非受判路径**（`spec/**` / `sessions/**` / `docs/PROGRESS.md` 之外）不在本门禁内——合并与非合并同口径，非合并特有残留。

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


## 12. U-10 C 实施：内容 digest 绑定门禁（P-137，2026-10-27）

> **定位**：Phase 2 的 **C 项**（内容 digest 绑定）实施记录。F（CI fail-closed）已在 P-134 实施（§10 U-10 行）。本节只记录 **三处未决的裁决 + 数据结构 + 六臂注入 + 残余风险**；`session_start`（Phase 2b）仍留未决。
> **要回答的问题**：该批次 `finalize` 记录的证据内容，**是否就是提交出去的内容**？

### 12.1 目标与不变式（I-9，三子句）

| 子句 | 表述 | 机械判据 |
|---|---|---|
| **I-9a 绑定存在** | P ≥ `EVIDENCE_MIN_P` 且带四文档改动的 batch / session / branch 声明，其声明 P 的最新 5/5 session 的**末次** `finalize` 必须带 `metadata.evidence_digest` | 块存在、`algorithm = sha256`、`files` 为非空对象 |
| **I-9b 内容一致** | digest 的 `files` 键集 = 该 P 声明 feature 的四文档集（`FEATURE_RE` 口径），每个值 = **即将提交的内容**的 sha256 | 键集相等 + 逐文件哈希相等 |
| **I-9c rebind 留因** | 同一 session 出现 ≥2 次 `finalize`（受控回边后重入）时，末次须带非空 `metadata.rebind_reason` | 非空字符串 |

**作用面**：只在 `batch` / `session` / `branch` 三种**带文档改动的显式声明**上生效；`maintenance` / `session-progress` / `batch-registration` / `nothing` 四模式不校验（见 §12.5 第 4 条对 maintenance 的诚实边界）。

### 12.2 三处未决裁决

**（R1）digest 记录时点 = `finalize`（否决 `verify`）**

- 依据：本仓文档生命周期实测——41bb0c4 / 3bc99fa / c779e6d（P-130 / P-131 / P-132）三提交**同改同一组 4 文档**（`E1`）⇒ 在 `verify` 记录的 digest 到终稿前必然失效；`finalize` 是五步链末步，是「内容冻结」的唯一机械时点。
- `verify` 的既有职责 = 锚点真实性（`verify-anchor` 与 `ANCHOR_RE` 同一口径，只验位置可达），与内容字节无关；把 digest 塞进 `verify` 会让两个不同语义共享同一个步位。
- **明示代价**：`finalize` 之后的任何文档改动都必须 **rebind**（追加 `verify` 受控回边 + 再入 `finalize`），成本 = 2 条 decision。该代价由 `_decision_chain` 的 P-069 受控回边机制天然承载，**无需新 schema、无需转义行**（`seen` 首现序保证 `--expect` 仍判 5/5）。

**（R2）作用域 = per-batch；rebind 原因只在同 session 内要求**

- **作用域**：绑定对象 = **声明 P 行的 feature 集**；校验对象 = **该 P 的最新 5/5 session 的末次 finalize**；历史 session **永不重验**。这是存量零回归的结构性保证（不靠边界豁免，而靠作用域本身）——与 U-2 边界纪律同思路。
- **rebind 留因的边界 = 同 session 内**：跨批次不要求原因——新 P 行 + 新 session 本身即声明，PROGRESS 行记录变更理由；再要求一份「跨批 rebind 原因」= 同一事实的第二 claim 面，违反本仓「声明 = 重数」纪律。
- 依据：上述三提交属**跨批**同改，由 per-batch 作用域吸收；同批内「finalize 后改文档」才是 I-9 要拦的缺陷。

**（R3）过渡边界 `EVIDENCE_MIN_P = 137`**

- 预注册提案 135 已被 P-135（裁决落档批）占用，改标 136 后又被 P-136（三裁决批）占用 ⇒ 取**实施批自身 137**（同 P-092 `FINALIZE_IMPACT_MIN_P = 92` 先例：边界取实施批编号，本批吃狗粮自证）。
- **独立常量**：不与 `BATCH_BINDING_MIN_P = 129`（入口完整性）、`FINALIZE_IMPACT_MIN_P = 92`（finalize 字段）合并——三者语义不同（入口 / 字段 / 内容绑定）。
- 存量读数（`E1`，2026-10-27 实测）：`tools/spec_runner/sessions` 160 jsonl / **155 批次 session** / 5 非批次文件 / 批次最大 P = **P-136** ⇒ 全部 < 137。

### 12.3 数据结构与唯一实现

```text
metadata.evidence_digest = {"algorithm": "sha256",
                            "files": {"spec/<feature>/RESEARCH.md": "<64 hex>", ...}}
metadata.rebind_reason   = "<非空原因>"      # 仅 rebind 时（末次 finalize）
```

- **无 aggregate 单值字段**：单值汇总会掩盖「哪个文件变了」；per-file 文件表既是「验后改文档」判据，又是改动定位的最小充分声明。冗余汇总 = 额外 claim 面。
- 作用域 = `FEATURE_RE` 口径（feature 目录下四文档命名），与门禁管辖面**同一口径**（PLAN / README 类非四文档不绑，避免 finalize 后误触）。
- 规范化 = CRLF → LF（git 规范形态）；路径排序固定（生成与校验逐字节同序）。
- **读面分工**：生成侧（`--doc-digest <feature>`）读**工作树**（终稿此刻）；门禁侧本地模式读 **index**（即将提交的内容，与 `_read_progress` 同源，pre-commit 会暂存未暂存改动 ⇒ 两者一致）、CI 模式读工作树（= checkout 出的提交）。
- **唯一实现**：`scripts/step_enforce.py` 的 `doc_digest` / `verify_digests`（生成与校验共用同一函数，守 I-10 语义同源纪律）；不新增 runner 子命令、不改 decision schema（`metadata` 为自由字段，与 `upstream_impact` 同级先例）。

### 12.4 六臂注入（落为 8 例，临时 git 仓 + 真实 `spec_runner`）

| # | 臂（预注册六臂 → 细分） | 注入 | 期望 | 用例 |
|---|---|---|---|---|
| 1 | 基线 | P-137 + 正确 digest（生成侧自算） | pass，输出 `digest_bound=1` | `test_digest_bound_pass_p137` |
| 2 | P≥边界缺 digest | finalize 无 `evidence_digest` | exit 1 | `test_digest_missing_fails_p137` |
| 3 | 验后改文档 | digest 记录后改同一文档并提交 | exit 1（digest 不匹配） | `test_digest_mismatch_after_finalize_fails` |
| 4 | 作用域漂移（细分自臂 3） | finalize 后新增四文档 | exit 1（文件集不一致） | `test_digest_file_set_mismatch_fails` |
| 5 | rebind 无原因 | 受控回边 + 再入 finalize，`rebind_reason` 为空 | exit 1 | `test_digest_rebind_without_reason_fails` |
| 6 | rebind 有原因 | 同上 + 非空原因 | pass（仍判 5/5） | `test_digest_rebind_with_reason_passes` |
| 7 | 历史批次不误伤 | P-136 session 无 digest + 文档改动 | pass（不检查） | `test_digest_historical_p136_not_checked` |
| 8 | 无 document 改动（细分自臂 7） | `session-progress` 与 `batch-registration` 两模式 | pass（不检查） | `test_digest_not_applied_without_docs` |

实跑（2026-10-27）：`python -m unittest tests.test_batch_binding` **28/28**（20 既有零回归 + 8 新增）；`spec_runner selftest` **83/83**（runner 未改动，零回归）。

### 12.5 残余风险与诚实边界

1. **`session_start`（Phase 2b）未实施**：不引入 `input.metadata = {pid, features, tier}` 的开场声明，批次身份仍由「PROGRESS 声明 + session 文件名 + finalize digest」三面表达。
2. **digest 不证明审查充分性**：它只证明「finalize 记录的字节 = 提交的字节」。`verify-anchor` 仍只验锚点可达（RULE-1 的边界不变），语义正确性不在任何机械门禁的可证范围内。
3. **JSONL 无哈希链**：session 行本身可被改写而 digest 不可检出（承附录 D.1 报告 §7 同项不确定，未在本批处理）。
4. **maintenance 模式不校验 digest**：仅空白改动的语义面为零，且 P≥129 的维护模式已要求完整链；但字节确实变了 ⇒ 其后同批 strict 提交须 rebind。这是**明示代价**，不是静默豁免。
5. **跨批 rebind 原因不作要求**（R2 的取舍）；若未来出现「跨批同改且无新 P 行」的真实形态，须另立裁决而非默认沿用。

### 12.6 回退

`EVIDENCE_MIN_P` 置哨兵值 **9999**（大于全部现存 P）⇒ 校验整体降为观察（`digest_bound` 不再输出、无红），其余行为零变更；`--doc-digest` 生成侧保留可用。不涉及 runner / session schema / hook 配置的回退。

## 13. P1-1 真实 runner 集成回归（P-139，2026-10-27）

### 13.1 门禁缺口实测（A-43，E1）

【A】A-43 门禁触发面缺口实测（E1）：读 `.pre-commit-config.yaml` 六 hook 的 `files` 正则——`blackbox-tests` 原覆盖 `tests/.*\.py` 与 `scripts/(step_enforce|spec_map)\.py`；`repo-stats` 覆盖 `CODE_WIKI.md` / `README` / `.pre-commit-config.yaml` / `docs/` / `spec/` / `adr/` / `scripts/`；`console-gen` 覆盖 `docs/PROGRESS.md` / `sessions/` / `spec` 四文档；其余三道只覆盖 `.md`。**三者叠加仍不含 `tools/spec_runner/spec_runner.py`** ⇒ 单独改 runner 的提交在本地**不触发任何 hook**（CI 仍跑 runner `selftest`，但只看内嵌自测）。P-137 的 digest 注入测试虽已用真实 runner，但只有 `tests/` 变更才触发测试——**被被测对象变更却不触发其测试**即本批的直接缺口（非覆盖缺口，是触发面缺口）。

### 13.2 最小改动（与 §7.3 逐条对应）

1. `blackbox-tests` 触发面补 `tools/spec_runner/spec_runner.py`（唯一生产配置改动）；
2. 新增 `tests/harness.py`：临时仓 + 三个脚本副本 + `SR_SESSIONS_DIR` / `SR_REWORK_REGISTRY` 显式注入；
3. 新增 `tests/test_runner_integration.py`（10 例 = step-gate 四态 / verify-anchor 两态 / fork / anchor-audit / backflow-audit / 门禁面 parity guard）；
4. 新增 `tests/test_runner_mutation.py`（4 例变异体 guard proof）；
5. 既有 `test_hook_blackbox.py`（纯函数与命名契约）与 `test_batch_binding.py`（step_enforce 批次面）**保留不替换**——stub 与真实 runner 互不替代。

### 13.3 四类变异体

| # | 变异 | 载体 | 探针 | 原版 exit | 变异 exit |
|---|---|---|---|---|---|
| M1 | 删除完整链检查 | runner `step-gate` 期望链比较 | 4/5 步 + `--expect` 5 | 1 | 0 |
| M2 | 改回静态最新 P | `step_enforce.resolve` 的声明解析 | 只改 P 行描述 + 四文档变更（无新行） | 1 | 0 |
| M3 | 吞掉 gate 硬失败 | runner `step-gate` 硬性分支 | 4/5 步 + `--expect` 5 | 1 | 0 |
| M4 | 破坏锚点路径解析 | runner `_check_anchor` 调用 | 指向不存在文件的锚点 | 1 | 0 |

变异体实现 = **复制到 temp 后就地改字**（原字面量须唯一命中；源码漂移 ⇒ harness 断言失败，测试红）；真实仓脚本永不改动（无污染路径）。

### 13.4 读数（A-44，E1，2026-10-27）

【A】A-44 本批集成与变异读数（E1，2026-10-27）：

- 新增用例 **14/14 PASS**；全套 `python -m unittest discover -s tests` **36 → 50 例，全绿**；
- 增量 = **新增两模块 8.7 s**（全套 39.6 s；与 CI 同命令、同平台口径）；CI `step` 未改 ⇒ 增量即 14 例；
- 4/4 变异体被感知（原版 exit ≠ 变异版 exit，见 §13.3）；
- 触发面实证 = `pre-commit run blackbox-tests --files tools/spec_runner/spec_runner.py` → **Passed**（改造前该文件不触发该 hook）；
- **U-3 判据 = 满足**（4/4 捕获 + 增量可接受）；**CI 远端增量未直接实测**（本批不推送）——以同一命令的本地读数代理，如实登记。

### 13.5 边界与回退

- 只加测试与一条 `files` 正则；**不改 runner / `step_enforce` / `spec_map` 任何行为**，零新依赖、零新 hook、零 session schema 变更；
- 回退 = 删三个测试文件 + 还原 `blackbox-tests` 的 `files` 一行 ⇒ 逐字节回到 P-138 后状态；
- 不覆盖：runner 的 `run` / `gate` / LLM 端点路径（需 mock server，属 runner `selftest` 面，不重复建设）；
- 本批**不新增**「每步执行证据」判据——那是 P1-2（U-4），须另立设计批。

## 14. CI 逐提交遍历：门禁假红的第二类成因（P-140，2026-10-27）

### 14.1 缺陷实测：单次 diff 的两条独立假红面（A-45，E1）

【A】A-45 PR #58 结构性假红的两条面（E1，2026-10-27）：

| # | 面 | 复现（只读命令，等价 CI 原 `BASE...HEAD`） | 读数 |
|---|---|---|---|
| ① | 历史 P 行被整批重复点名 | `step_enforce --base <main> <分支全量变更集>` | `changed_pids` = **15 条**（P-125~P-139）；首错 `P-127 未声明任何 spec/<feature>/ 链接`；exit 1 |
| ② | 跨批 digest 与 PR 头不等 | 同一命令 + 先把 P-127 行补 feature 链接 | `specwf-p137-20261027` / `specwf-p138-20261027` **digest 不匹配**（四个 framework-deep-review 文档）；exit 1 |

- **机制**：CI 用 `BASE...HEAD` 单次 diff ⇒ 整条分支 15 个批次被塞进**一个**变更集；每批声明被按「本批」口径重审，且 `verify_digests` 的 **per-batch 作用域无法区分「同批 rebind」与「跨批演进」**（P-138/P-139 改动同一组四文档）。
- **远端读数一致**：`gh run list`（PR #58）**4 连败**（`c251692` / `7101c0a` / `5f759f8` / `1ac992a`），失败步骤均为 `决策流批次强制（step-enforce）`，日志末行 `pid=P-125,…,P-139 -> exit 1`。
- **本地不可见**：本地 hook 逐提交运行（`--base HEAD^` 只含本批）⇒ 同一提交本地绿、远端红。**I-8（本地/CI 同源）在变更集构造层被破坏**，脚本层始终同源。
- **结论**：这是**判定面构造缺陷**，不是规则缺陷；补数据（P-127 链接）只能消 ①，② 仍在。

### 14.2 候选方案与裁决

| 方案 | 内容 | 结论 |
|---|---|---|
| **A** | 逐提交遍历 + 执行器取**该提交自身版本** | **选择**：与本地逐提交语义逐字等价（I-11a / I-11b）；真实历史 16 提交实测全绿 |
| B | 逐提交遍历 + 执行器取 HEAD 版本 | **否决**：追溯施加当时不存在的新规则——实测 P-127 的提交在 P-130 新规则下变红（A-46），只是把假红换成另一种 |
| C | 保留单次 diff + 只补 P-127 链接 | **否决**：A-45 ② 的 digest 面仍在（实测 exit 1） |
| D | 只判末提交 | **否决**：丢失中间批次的声明与 digest 校验，等于取消逐批门禁 |

方案 A 的合并提交处理：**显式跳过**（`git rev-list --parents -n 1` 词数 > 2）——合并提交的变更 = 父提交并集，逐父已被同循环覆盖；对它求 diff 正是方案 C 的假红形态。残留见 §10 U-11（**P-144 已实测并关闭**）。

### 14.3 读数（A-46，E1，2026-10-27）

【A】A-46 逐提交遍历在本仓真实历史上的读数（E1，2026-10-27，temp 克隆 + 真实分支）：

- **全绿**：range `b0e6534..1ac992a` 共 **16 个非合并提交**逐条 pass，`EXIT=0`；P-137/P-138/P-139 各输出 `digest_bound=1`（各自批次字节在各自提交处匹配）；
- **合并面**：在 temp 仓合成一个合并提交（父 = 分支头 + main 侧新提交）⇒ range 17 条，merge 被 skip、**16 受判**、`EXIT=0`（未把并集当单一提交）；
- **对照（方案 B）**：用 HEAD 版执行器复验历史内容 ⇒ P-127 的提交 `e2c6beb` 变红（`_resolve_declared` 的 feature 链接要求由 P-130 引入）——追溯红实证；
- **执行器能力面**：P-130 之前的 `step_enforce.py` **无 `--base` 参数**（只收位置参数，按 `spec/` 前缀过滤），故按能力探测分派：有 `--base` ⇒ 传父提交 ref；无 ⇒ 按原调用约定。

### 14.4 远端复验（A-47，E1，2026-10-28）

【A】A-47 逐提交遍历的 CI 远端首次实测（E1，2026-10-28，GitHub Actions run `40579430749`，提交 `22976eb`）：

| 项 | 读数 |
|---|---|
| 事件 / 分支 | `pull_request`（PR #58）/ `docs/p125-graph-structure-preresearch` |
| 结果 | `verify` job **成功**，耗时 **1m30s**；8 个 step 全 ✓（含 `决策流批次强制（step-enforce，逐提交）`） |
| PR 状态 | `OPEN / MERGEABLE`；`statusCheckRollup` 为 `verify = COMPLETED SUCCESS` |
| 对照 | 同一分支此前 **4 连败**（`c251692` / `7101c0a` / `5f759f8` / `1ac992a`），失败步骤均为 step-enforce |

- **检出面** = PR 合并提交（`refs/pull/58/merge`）：`rev-list` 命中的合并提交被 skip，**17 个非合并提交**逐条受判（与本地合成合并提交实验同形，A-46）；
- 本读数把 A-46 的「本地代理」补成「远端实测」；**P-140 行⑦ 的「CI 远端未实测」由 P-141 回填**（不改写历史提交，只改活载体——同 P-139 订正 P-138 的先例）。

### 14.5 合并面实测：`push(main)` 的合并提交跳过（A-48，E1，2026-10-28）

【A】A-48 逐提交遍历在 `push(main)` 合并面上的首次真实走查（E1，2026-10-28，GitHub Actions run `40585936395`，合并提交 `adfec33`）：

| 项 | 读数 |
|---|---|
| 事件 / 分支 | `push`（`main`）；标题 = `merge(P-125~P-141): 图结构调研 + 框架深度评审升级链（PR #58）` |
| 基线 / 头 | `BASE = github.event.before = b0e6534`（main 原头）；`HEAD = adfec33` |
| 结果 | `conclusion = success`；墙钟 `createdAt 21:20:22Z → updatedAt 21:21:30Z` = **68 s**；8 个 step 全 ✓ |
| 受判面 | `step-enforce: 逐提交遍历完成，受判提交 **18** 个（range `b0e6534..adfec33`）` |
| 合并提交 | `step-enforce: skip merge commit adfec33…（变更 = 父提交并集）` — **按设计跳过**，未产生并集式假红 |

- **三面同形**：本地合成合并提交（A-46，16 受判）/ PR 合成合并提交（A-47，17 受判）/ 真实 `push(main)` 合并提交（A-48，18 受判）——三面均「合并提交 skip + 其余逐条受判 + exit 0」；17 → 18 之差 = P-141 合入多 1 个提交；
- **`BASE` 语义**：`push` 事件取 `github.event.before`（非 merge-base），故分支全部提交各判一次——这正是逐提交遍历的预期语义，非「重复判」；
- **U-11 判据**「`push(main)` 走查不因并集 diff 重复判红」**由本读数满足**；**evil merge 内容当时仍未构造实测**（残留不变；**P-144 §14.7 已实测并关闭**）；
- **P-141 行⑤ 的「`push(main)` 的 merge 跳过路径仍未实测」由 P-142 回填**（就地订正，同 P-141 订正 P-140 的先例）。
- **补充读数（第 2 次真实 `push(main)`，P-143 登记）**：PR #59 以 `--merge` 合并 ⇒ 合并提交 `3bb7680`（父 = `adfec33` + `bc690dc`）；run `40589457291`：`conclusion = success`、墙钟 `21:45:45Z → 21:47:12Z` = **87 s**、8 step 全 ✓；日志 = `skip merge commit 3bb7680…（变更 = 父提交并集）` + `受判提交 1 个（range adfec33..3bb7680）`——同一断言 A-48 的**第二样本**，复核跳过路径在**小 range（1 个非合并提交）**下同样成立；A 类计数不变。

### 14.6 边界与回退

- 唯一生产改动 = `.github/workflows/ci.yml` 的 step-enforce 段；**零脚本行为变更**（`step_enforce` / `spec_map` / `spec_runner` 字节不变）、零新依赖、零新 hook；
- 数据修复 = PROGRESS 的 P-127 行补 `spec/graph-structure-upgrade/` 链接（该行原是全表唯一无 feature 链接的行；对派生视图无影响——§9 行标注优先 ⇒ 仍映射 P-125）；
- 新增 guard = `tests/test_runner_integration.py` 的 `test_ci_per_commit_walk`（5 断言：`rev-list --reverse` / `checkout -q -f` / `--base` 能力探测 / merge skip / 无 `BASE...HEAD`）；
- 回退 = 还原 ci.yml 该段 + 还原 P-127 行 + 删该测试 ⇒ 回到 P-139 后状态；
- 不覆盖：已在 `main` 上的历史提交不再重走（range 限定）；**evil merge 内容已由 P-144 的 `--check-merge` 兜底（§14.7）**，非受判路径（`spec/**` / sessions / PROGRESS 之外）不在本门禁内。

### 14.7 合并面残留的实测与关闭（A-49 / A-50，E1，2026-10-28）

【A】A-49 evil merge 内容逃逸实测（E1，2026-10-28，临时克隆 + 与 ci.yml 同形的逐提交循环）：

| 步骤 | 读数 |
|---|---|
| 构造 | main 侧把 RESEARCH 的 `date:` 行改成尾随空格（空白提交 B）；分支侧同一行改成双空格（空白提交 C，单提交判 `mode=maintenance` 通过）；`git merge main` → **冲突 rc=1**，解决块 **1** 处，解析写入两父皆无的语义行 |
| 循环（range `B..M`） | C 受判 → `mode=maintenance pid=P-128 source=whitespace` 通过；M **被 skip**；`受判提交 1 个`、**exit 0** |
| 内容定位 | `EVIL_LINES_IN_MERGE=1` / `EVIL_IN_P1=0` / `EVIL_IN_P2=0`；`git diff P2..M` 命中该标记 1 次 ⇒ **内容只存在于合并树** |
| 对照 | 同一句内容改走**普通提交** → `语义性四文档改动缺少批次声明`，**exit 1** |

- **结论**：同一内容、两条通道、两种判定 ⇒ 合并解决通道构成**永久逃逸**（下一次 `push(main)` 的 `event.before` 正是该合并提交，它不会再进入任何 range）；
- **现实暴露面**不是 GitHub 合并按钮（服务端生成、有冲突即拒绝合并），而是**分支内部的本地合并提交**（`git merge main` 解决冲突时手写的内容）随 PR 进入 main。

【A】A-50 `--check-merge` 检测四态（E1，2026-10-28，真实脚本 + 临时仓 4 例）：

| 用例 | 期望 | 实测 |
|---|---|---|
| 冲突解决写入两父皆无的内容 | exit 1 | **exit 1**，stderr 打印 `evil merge 内容（两父皆无）: <路径>` |
| 干净合并（两侧改不同文件） | exit 0 | **exit 0**，`无 evil 内容（2 个受判路径均等于某一父）` |
| 受判路径上合并结果 = 第一父（main 侧只改非受判文件） | exit 0 | **exit 0**，`无 evil 内容（0 个受判路径…）` |
| 非合并提交 | exit 0 | **exit 0**，`非合并提交（跳过 evil 检测）` |

- 判定定义：受判路径（`spec/**` / `sessions/**` / `docs/PROGRESS.md`）上**同时不等于两个父提交** ⇒ evil；等于任一父 ⇒ 干净合并（不判）；
- 与 A-49 的实验仓交叉验证：`--check-merge <M>` → exit 1 且路径与标记一致；`--check-merge <C2>` → exit 0（非合并）；
- **不引入 P-140 假红**：只对「两父皆无」的路径判红，不做并集 diff（A-46/A-48 的逐提交判定完全不变）。

**【A-50 远端样本】真实 `push(main)` 的阶段 1 首次判定（E1，2026-10-28，P-145 登记）**：

| 面 | 读数 |
|---|---|
| PR #61（`pull_request`） | run `40603562855`：`verify` **1m12s 通过**；**阶段 1 命中 GitHub 合成合并提交 `aabec54` 并判 `无 evil 内容（6 个受判路径均等于某一父）`**，阶段 2 skip 合成合并 + 受判 1 个普通提交（`ca456a4..aabec54`）；〔原记「阶段 1 循环未命中」有误，P-150 订正〕 |
| 合并 | `gh pr merge --merge` ⇒ 合并提交 `e8154eb`（父 = `ca456a4` + `c255272`） |
| `push(main)` run `40603730644` | `conclusion = success`、`23:40:30Z → 23:41:58Z` = **88 s**、8 step 全 ✓ |
| 阶段 1（首次对真实合并提交判定） | `step-enforce: merge e8154eb… **无 evil 内容（6 个受判路径均等于某一父）**`（6 = 四文档 + `docs/PROGRESS.md` + session） |
| 阶段 2 | `skip merge commit e8154eb…（变更 = 父提交并集）` + `受判提交 1 个（range ca456a4..e8154eb）` |

- **判据**：新门禁在真实远端、真实合并提交上产出**非空判定**（6 个受判路径逐一比较）且 exit 0 ⇒ 干净合并不误判，与 A-50 本地四态同形（`无 evil 内容` 分支）；
- **口径**：**不新增 A 编号**（同一断言 A-50 的远端样本，A 类计数保持 50）；CHECKLIST §2.8 **#54** 为该样本的验收位点；
- **边界（诚实）**：本样本只覆盖**干净合并**一侧；evil 侧的远端验证需构造真实冲突解决提交（本仓受保护分支 + PR 流程下不可自然产生）⇒ 仍以 A-49 / A-50 的临时仓读数为准，不以本样本冒充 evil 侧远端实测。

**【A-50 远端样本 · 第 2 样本】真实 `push(main)` 的阶段 1 判定（E1，2026-10-28，P-146 登记）**：

| 面 | 读数 |
|---|---|
| PR #62（`pull_request`） | run `40660422565`：`verify` **1m20s 通过**；**阶段 1 命中合成合并提交 `6e1a1a9` 并判 `无 evil 内容（6 个受判路径均等于某一父）`**；〔原记「未命中」有误，P-150 订正〕 |
| 合并 | `gh pr merge --merge` ⇒ 合并提交 `7bcce12`（父 = `e8154eb` + `ac6d194`） |
| `push(main)` run `40660622448` | `conclusion = success`、`08:58:13Z → 08:59:42Z` = **89 s**、8 step 全 ✓ |
| 阶段 1 | `step-enforce: merge 7bcce12… **无 evil 内容（6 个受判路径均等于某一父）**` |
| 阶段 2 | `skip merge commit 7bcce12…（变更 = 父提交并集）` + `受判提交 1 个（range e8154eb..7bcce12）` |

- **补充意义**：第 1 样本（`e8154eb`）之后紧接一次新的真实合并提交，阶段 1 **再次**产出非空判定（同为 6 个受判路径）且 exit 0 ⇒ 「干净合并不误判」不是一次性的；PR 面同时**命中合成合并提交**并判 `无 evil 内容`（原记「未命中」有误，P-150 订正）⇒ 两级读数均为「命中且无 evil」；
- **口径**：**不新增 A 编号**（A-50 的第 2 远端样本，A 类计数保持 50）；CHECKLIST §2.8 **#55** 为该样本的验收位点；
- **边界**：与第 1 样本同——只覆盖干净合并一侧，evil 侧远端仍未构造。

**【A-50 远端样本 · 第 3 样本】真实 `push(main)` 的阶段 1 判定（E1，2026-10-28，P-147 登记）**：

| 面 | 读数 |
|---|---|
| PR #63（`pull_request`） | run `40663491255`：`verify` **1m25s 通过**；**阶段 1 命中合成合并提交 `71f858e` 并判 `无 evil 内容（6 个受判路径均等于某一父）`**；〔原记「未命中」有误，P-150 订正〕 |
| 合并 | `gh pr merge --merge` ⇒ 合并提交 `023e456`（父 = `7bcce12` + `f5f08a9`） |
| `push(main)` run `40663831556` | `conclusion = success`、`09:23:18Z → 09:24:24Z` = **66 s**、8 step 全 ✓ |
| 阶段 1 | `step-enforce: merge 023e456… **无 evil 内容（6 个受判路径均等于某一父）**` |
| 阶段 2 | `f5f08a9` → `mode=batch pid=P-146 source=P-row`、`digest_bound=1`；`skip merge commit 023e456…（变更 = 父提交并集）` + `受判提交 1 个（range 7bcce12..023e456）` |

- **补充意义**：第 3 个连续真实合并提交上阶段 1 **再次**产出非空判定（受判路径恒为 6 个）且 exit 0 ⇒ 「干净合并不误判」在三个连续样本上稳定；PR 面同时命中合成合并提交并判 `无 evil 内容`（原记「未命中」有误，P-150 订正）；
- **口径**：**不新增 A 编号**（A-50 的第 3 远端样本，A 类计数保持 50）；CHECKLIST §2.8 **#56** 为该样本的验收位点；
- **边界**：与第 1 / 第 2 样本同——只覆盖**干净合并**一侧，evil 侧远端仍未构造。

**【A-50 远端样本 · 第 4 样本】真实 `push(main)` 的阶段 1 判定（E1，2026-10-28，P-148 登记）**：

| 面 | 读数 |
|---|---|
| PR #64（`pull_request`） | run `40666075396`：`verify` **1m20s 通过**（墙钟 `09:40:25Z → 09:41:49Z`）；**阶段 1 命中合成合并提交 `a326f9f` 并判 `无 evil 内容（6 个受判路径均等于某一父）`**；〔原记「未命中」有误，P-150 订正〕 |
| 合并 | `gh pr merge --merge` ⇒ 合并提交 `fb01568`（父 = `023e456` + `ec10e62`） |
| `push(main)` run `40666293529` | `conclusion = success`、`09:42:07Z → 09:43:29Z` = **82 s**、8 step 全 ✓ |
| 阶段 1 | `step-enforce: merge fb01568… **无 evil 内容（6 个受判路径均等于某一父）**` |
| 阶段 2 | `mode=batch pid=P-147 source=P-row`、`digest_bound=1`；`skip merge commit fb01568…（变更 = 父提交并集）` + `受判提交 1 个（range 023e456..fb01568）` |

- **补充意义**：第 4 个连续真实合并提交上阶段 1 **再次**产出非空判定（受判路径恒为 6 个）且 exit 0 ⇒ 「干净合并不误判」在四个连续样本上稳定；PR 面同时命中合成合并提交并判 `无 evil 内容`（原记「未命中」有误，P-150 订正）；
- **口径**：**不新增 A 编号**（A-50 的第 4 远端样本，A 类计数保持 50）；CHECKLIST §2.8 **#57** 为该样本的验收位点；
- **边界**：与前三个样本同——只覆盖**干净合并**一侧，evil 侧远端仍未构造。

**【A-50 远端样本 · 第 5 样本】真实 `push(main)` 的阶段 1 判定（E1，2026-10-28，P-149 登记）**：

| 面 | 读数 |
|---|---|
| PR #65（`pull_request`） | run `40676348854`：`verify` **58 s 通过**（墙钟 `10:58:49Z → 10:59:51Z`）；**阶段 1 命中合成合并提交并判 `无 evil 内容（6 个受判路径均等于某一父）`**；〔原记「未命中」有误，P-150 订正〕 |
| PR #66（`pull_request`，**P-150 取证补录**） | run `40677799676`：`verify` **1m22s 通过**；阶段 1 命中合成合并提交 `ed49d47` 并判 `无 evil 内容（6 个受判路径均等于某一父）`；阶段 2 `commit 52e72c0` + `skip merge commit ed49d47` |
| 合并 | `gh pr merge --merge` ⇒ 合并提交 `64c6313`（父 = `fb01568` + `9f1aebb`） |
| `push(main)` run `40676513311` | `conclusion = success`、`11:00:06Z → 11:01:27Z` = **81 s**、8 step 全 ✓ |
| 阶段 1 | `step-enforce: merge 64c6313… **无 evil 内容（6 个受判路径均等于某一父）**` |
| 阶段 2 | `mode=batch pid=P-148 source=P-row`、`digest_bound=1`；`skip merge commit 64c6313…（变更 = 父提交并集）` + `受判提交 1 个（range fb01568..64c6313）` |

- **补充意义**：第 5 个连续真实合并提交上阶段 1 **再次**产出非空判定（受判路径恒为 6 个）且 exit 0 ⇒ 「干净合并不误判」在五个连续样本上稳定；PR 面同时命中合成合并提交并判 `无 evil 内容`（原记「未命中」有误，P-150 订正）；
- **边际信息量（诚实）**：本样本与前 4 个**完全同形**，新增信息仅「再复现一次」；不改变任何判据，也不构成对 evil 侧的补充证据；
- **口径**：**不新增 A 编号**（A-50 的第 5 远端样本，A 类计数保持 50）；CHECKLIST §2.8 **#58** 为该样本的验收位点；
- **边界**：与前四样本同——只覆盖**干净合并**一侧，evil 侧远端仍未构造。

## 14.8 evil 侧远端样本的构造路径裁决（P-150）

### 14.8.1 订正：PR 面阶段 1 实为「命中」而非「未命中」

**事实（E1，2026-10-28 复读 6 个 `pull_request` run 日志）**：`actions/checkout@v5` 在 `pull_request` 事件下默认检出 **GitHub 合成 merge ref**（`refs/pull/N/merge`），故 `HEAD` 本身就是合成合并提交，阶段 1 必然命中：

| PR | run | 阶段 1 日志（合成合并提交） |
|---|---|---|
| #61 | `40603562855` | `merge aabec54… 无 evil 内容（6 个受判路径均等于某一父）` |
| #62 | `40660422565` | `merge 6e1a1a9… 无 evil 内容（6 个受判路径均等于某一父）` |
| #63 | `40663491255` | `merge 71f858e… 无 evil 内容（6 个受判路径均等于某一父）` |
| #64 | `40666075396` | `merge a326f9f… 无 evil 内容（6 个受判路径均等于某一父）` |
| #65 | `40676348854` | （同类行，见 §14.7 第 5 样本表订正） |
| #66 | `40677799676` | `merge ed49d47… 无 evil 内容（6 个受判路径均等于某一父）` |

**误记根因**：日志里的 `受判提交 1 个` 指**分支侧普通提交**（阶段 2 计数），被误读为「range 内无合并提交 ⇒ 阶段 1 未命中」。**订正范围** = §14.7 五行 PR 行 + 四条「补充意义」bullet；`PROGRESS` P-145~P-149 与 `IMPLEMENTATION §3.11` 同批就地订正；`CODE_WIKI` v1.194~v1.198 历史 banner 保留原貌（版本历史 append-only），订正统一记入 v1.199。

**结构含义（重要）**：本仓**每次 PR 都已天然包含一次合并提交判定**——只是合成合并提交的树恒等于 head 树（等于某一父），故恒判「无 evil」。这条路径无法证明 evil 判红。

### 14.8.2 两条 evil 侧构造路径

| 维度 | 路径 1：临时放宽保护 → 直推 evil 合并到 `main` | 路径 2：分支内构造 evil 合并 → 失败 PR |
|---|---|---|
| 机制 | 关 `enforce_admins`（GitHub「Do not allow bypassing」）→ `git push origin main`（本地 merge 冲突解决写入两父皆无内容） | 特征分支上 `git merge` 制造冲突 → 解决写入两父皆无内容 → push 分支 → 开 PR |
| 能否**阻断** | **不能**：`push(main)` CI 在内容进入 main **之后**才跑，只证明「能检测」 | **能**：required check 失败 ⇒ `mergeStateStatus = BLOCKED` |
| main 污染 | **永久**：合并提交进历史；`allow_force_pushes=false` ⇒ 连 revert 也无法清除该提交 | **零**（PR 关闭 + 分支删除，两个探针提交不进 main） |
| 保护规则风险 | 窗口期内**全部**保护失效；恢复漏项 ⇒ 仓库静默降级 | 全程不动保护规则 |
| 失败面层级 | Layer-1（仓库设置） | Layer-0（分支 + PR） |
| 可重复性 | 每次都要改设置 | 一次性夹具，可脚本化 |
| 残留 | main 历史 + 两次设置变更 | 一个 closed PR + 一条红 run（本身即证据） |

### 14.8.3 社区实践检索（分级）

- **T1（官方一手，已回原文）** gitglossary（2.56.0）：*“An evil merge is a merge that introduces changes that do not appear in any parent.”* —— 与 §14.7 判据（同时不等于两父）逐字一致 ⇒ 判据无争议，争议只在「怎么造样本」；
- **T1（官方一手，已回原文）** GitHub「About protected branches」：① *“By default, the restrictions of a branch protection rule do not apply to people with admin permissions…”* ⇒ 路径 1 必须解除的正是这条默认（本仓 `enforce_admins=true` 已开启「Do not allow bypassing」）；② required check 须为 `successful / skipped / neutral` 才允许合并 ⇒ 路径 2 的判红天然落在「不 success ⇒ 不可合并」；
- **T3（社区教程）** CI/CD 实操文中的同款手法：*“Open a pull request … but do not merge it. GitHub Actions runs Verify, reports the failed test, and the active ruleset blocks the merge. … That proves the first gate works.”* —— 「用一次性失败 PR 证明门禁有效」是常见做法；
- **T3（GitLab 议题）** evil merge 在托管平台 UI 中极难辨识（*“hard to work out what happened in a merge commit”*）⇒ 这类样本应只存在于一次性分支，不应进主干。

**诚实边界**：未检索到专门讨论「evil merge 检测门禁」的权威实践文献，也未检索到「为验证门禁而临时关闭 branch protection」的正面案例；上述材料只能支撑「用失败 PR 演示门禁」与「不动生产保护配置」两条一般做法，本仓判据与检测器为自研。

### 14.8.4 机制实测（E1，临时仓，2026-10-28）

在一次性仓复现「分支内合并提交是否进入 PR 式 range」：

```text
git rev-list --parents -n 1 HEAD   → 04dc0b2 35303a9 3566355   （words = 3）
git rev-list --reverse main..HEAD  → 3566355 C2 (words=2)
                                     35303a9 C1 (words=2)
                                     04dc0b2 MERGE (words=3)   ← 分支内合并提交确实在 range 内
```

⇒ [ci.yml](../../.github/workflows/ci.yml) 阶段 1 会对该提交调 `--check-merge`；且 `set -eo pipefail` 下 exit 1 **立即中止**（阶段 2 不执行）⇒ 归因单一。

### 14.8.5 裁决：走路径 2

**理由**：① 唯一能证明「阻断」（本门禁最核心、至今未被证明的属性）；② 零 main 污染 + 不动保护规则（代价最小）；③ 可重复、可脚本化，失败面停留在 Layer-0；④ 路径 1 在 `push(main)` 面本就只能事后检测，且永久留痕与保护窗口风险不可逆。

**执行步骤（P-151）**：

1. `git checkout -b probe/evil-merge main` → 改 `spec/framework-deep-review/RESEARCH.md` 某行 → 提交 C1；
2. 从**同一 `main`** 再开 `probe/evil-side` → 改同一行 → 提交 C2（同源保证 GitHub 能算出合成 merge，否则 CI 不跑）；
3. 回 `probe/evil-merge`：`git merge probe/evil-side` → 冲突 → 解决为**两父皆无**的新文本 → 合并提交 M；
4. push + `gh pr create` → 取读数；
5. `gh pr close` + 删远端 / 本地分支。

**判据（三项同时成立才算闭环）**：① `verify` = failure 且日志含 `evil merge 内容（两父皆无）: spec/framework-deep-review/RESEARCH.md` + `-> exit 1`；② `gh pr view --json mergeStateStatus` = `BLOCKED`；③ `main` 历史无该合并提交（`git log --oneline main | grep -c MERGE` 不增）。

**边界**：探针分支上的 C1 / C2 也会被阶段 2 受判（无批次声明 ⇒ 同样判红），但阶段 1 fail-fast 先中止，故日志归因唯一；探针 PR 关闭后不并入 `main`，不产生任何真值源改动。

## 15. 参考文献

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

A-1~A-20 为本仓机械实测 / 源码直读；A-21~A-28 为已回原文的外部一手来源 / 标准原文；A-29~A-35 为本次核验的官方文档与安全公告；A-36~A-42 为 U-1 专项实测；A-43~A-44 为 P1-1 门禁缺口与真实 runner 集成回归实测（§13）；A-45~A-46 为 P-140 CI 结构性假红与逐提交遍历实测（§14）；**A-47 为 P-141 CI 远端首次实测回填（§14.4）；A-48 为 P-142 `push(main)` 合并面实测回填（§14.5；第 2 样本由 P-143 补充）；A-49～A-50 为 P-144 evil merge 逃逸实测与检测四态（§14.7；**A-50 含 P-145 / P-146 / P-147 / P-148 / P-149 的五个真实 `push(main)` 远端样本**）**。逐条证据已在 §3~§5、§11、§13~§14 就地给出，此处不重复。

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

---

## 附录 D：五项裁决子代理完整报告（P-133，2026-10-26）

> **落档说明**：本附录逐字收录 2026-10-26 五个子代理的完整报告（U-10 / U-7 / U-5 / U-6 / U-9），保留其结论、五维对比、故障注入、外部锚点、验证记录与不确定项。**证据分级沿用各报告内部标注（T1/T2/T3、E1/E3），不并入本文件 §0 的 A/B/C/H 统计**（§0 计数保持 42/27/9/14）。主臂已对报告中的关键读数做独立复核，复核结论见 D.0；**报告与 D.0 冲突时以 D.0 为准**。
> **检索降级**：本环境未暴露 MCP 搜索端点（ToolSearch 仅返回内置 WebSearch/WebFetch；承前批 `mcp_english-search_search_web` 404 实测）⇒ 五个子代理均降级 WebSearch + WebFetch，并在各自报告开头登记降级链。

### D.0 主臂复核摘要（E1）

| 复核项 | 子代理读数 | 主臂实测 | 裁定 |
|---|---|---|---|
| specwf session 数 | 152 | **151**（156 个 jsonl，含 **5** 个非批次文件；P-134 订正：152 系 naive 子串 `specwf-p` 误计 `specwf-probe` 所致） | ❌ 订正 151（P-134） |
| decision / gate / session_start | 729 / 7 / 0 | 729 / 7 / 0；7 个 gate 全在 5 个非批次文件 | ✅ 采纳 |
| CI fail-open | `git diff ... \|\| true` 可静默跳过 | 坏 base → git diff exit 128 + 零输出；`step_enforce --base` exit 2 | ✅ 包装层 fail-open、工具层 fail-closed |
| graph S0/S1 | 仅有 RESEARCH.md | `spec/graph-structure-upgrade/` 仅 `RESEARCH.md` | ✅ 无 DESIGN/IMPLEMENTATION |
| U-6 命名空间 | 266 处 / 14 文件 / 3 命名空间 | 266 处 / 14 文件；PC 171、CODE_WIKI 36、PROGRESS 31、graph 9、framework 1 | ✅ 采纳 |
| M7 形态 II 总数 | 117（hits 块） | `hits.form2_total = 117`；CODE_WIKI 两处写 116 | ❌ 发现 1 处计数漂移（本批连带订正） |
| U-7 编号 | 实为 graph U-1 | graph RESEARCH §10：U-1 = pilot 未选定；U-7 = P4 前置 | ✅ 编号错位成立 |

**本批连带订正**：`CODE_WIKI.md` 树行与 §9 行的「形态 II 116 处」改为 **117 处**（真值 = `docs/M7_EVIDENCE_LOG.md` §5 hits `form2_total: 117`）。该漂移此前无机械门禁覆盖。

**P-134 复核增补（2026-10-26，裁决审查轮）**——对五份报告与主臂裁决文本的四项订正：

1. **批次计数 off-by-one（上表第 1 行已订正）**：子代理与 P-133 时点主臂均误记 152；严格正则 `specwf-p\d{3}-` 实测 151（`specwf-probe-20260907.jsonl` 含子串 `specwf-p` 被误计；非批次文件为 5 个非 4 个）。**对 U-10 结论零影响**（151/151 gate=0 比例不变）；P-133 行与 CODE_WIKI banner 已同批订正。D.1 报告原文保留 152 不改（逐字收录原则），以本表为准。
2. **pipefail 默认旗标（订正主臂裁决 justification）**：GitHub Actions `shell: bash` 默认即 `bash --noprofile --norc -eo pipefail {0}`（官方 workflow-syntax 页本次抓取被截断未回读原文；多源 T2 一致且无反例 ⇒ 采信并标注层级）。子代理标 E3 属实；主臂原文「显式 set -eo pipefail 消除默认差异」**不成立**——显式写出为防御性冗余/自文档化，P-134 保留并订正措辞。
3. **引用号混叠（U-7 报告 D.2 与裁决文本）**：「B6 负载未满足」应为「**D6 链**负载未满足（主张登记号 B6，graph RESEARCH L633）」；「D6 禁托管」应为「**A-13** 托管禁令：不让本框架托管 Auto_Prover 图执行外壳（ADR-0013 D6/D7，graph RESEARCH L118）」。Cpp_Hub 并发撞树行号为 `docs/DEVELOPMENT_LOG.md` **L3127**（D.2 引 3126，漂 1）。语义方向均不变。
4. **F 的两个新红边（裁决文本已登记）**：fail-closed 化后，① 根提交/孤儿分支 `BASE="HEAD^"` 会失败 → P-134 回退 `BASE=HEAD`（三点空 diff ⇒ 显式绿灯）；② force-push 非祖先 base ⇒ git diff 失败 ⇒ 显式 exit 1 红（有意 fail-closed）。「F 零回归」限定为**零历史 session 回归 + 2 个新 CI 失败边**。本地注入 5/5（坏 base 红 / 无变更绿 / 根提交不误伤 / push 有变更进门禁 / PR 基线进门禁）。

### D.1 U-10：Phase 2 是否立项（F 必做，C 是否同批）

**子代理检索降级**：MCP 检索端点在当前环境未暴露（ToolSearch 无检索类工具；承前批 `mcp_english-search_search_web` 404 实测）⇒ 走 WebSearch + WebFetch。

**0 读数订正（E1）**：`specwf-p*.jsonl` 实为 **152**（目录 156：+4 演示/探针；「154」不成立）；113 PID；decision 729；**gate 事件 7 条全在 5 个非批次文件，152 个真实批次 session 的 gate=0**；session_start=0。RESEARCH 文件 713 行，§11.9 在 L706（报告时点）。

**1 结论**：推荐 **A（F only）**。若已定 F 必做：**C 不同批**。三条硬理由：① C 规格仅一行、三处未决（§7）；② F 约 5 行、零历史回归，C 每批新增手工义务，混批回退不原子；③ F 是 C 的前提——CI 能静默跳过时 digest 门禁同样被跳过。

**2 五维（1-5，高分优）**

| 方案 | 成本 | 收益 | 兼容 | 维护 | 升级 | 合计 |
|---|---|---|---|---|---|---|
| A F only | 5 | 3 | 5 | 5 | 3 | 21 |
| B F+C | 3 | 4 | 2 | 2 | 4 | 15 |
| C 全 Phase 2 | 2 | 4 | 1 | 1 | 5 | 13 |
| D 暂缓 | 5 | 1 | 5 | 5 | 0 | 16 |

**3 故障注入（A/B/C）**

| 注入 | A | B | C |
|---|---|---|---|
| 删 gate 事件 | 不检出（无依赖） | P≥N 缺失→红 | 红 |
| 验后改文档 | 不检出 | 检出，但 finalize 正常改文档自伤→须 rebind | 同 B |
| 伪造 digest | — | 文档+行同改→仍绿（无签名，E3 推断） | 同 B |
| git diff 失败 | 修后红；不修则整步跳过 | 不修 F 时同样跳过 | 同 |
| 无 session_start | 无影响 | 无影响 | 152/152 全红（无边界） |
| `--base` 空/坏 | 实测 exit 2 | 同 | 同 |

实测：坏 ref → git diff exit 128 且零输出 ⇒ `|| true` 使 FILES 空 ⇒ step 跳过；`step_enforce --base 坏ref` → exit 2（工具 fail-closed、包装层 fail-open）。

**4 回归面/边界**：152/152 gate=0 ⇒ B/C 任何「必须有 digest/session_start」均全红。先例：`FINALIZE_IMPACT_MIN_P=92`（103 session 全缺字段）、`BATCH_BINDING_MIN_P=129`。建议 C 边界取**实施批自身**（P-092 吃狗粮先例），否则 P≥实施批+1。E1：P-130/131/132 三次改同一组 4 文档 ⇒ digest 须 **per-batch 作用域**并在 finalize 末次改文档后 rebind；现行「verify 记录」写法与本仓文档生命周期冲突。

**5 锚点（2026-10-26 访问）**

| 层级 | 标题 | URL | 关键结论 |
|---|---|---|---|
| T1 | SLSA v1.2 Verifying artifacts | https://slsa.dev/spec/v1.2/verifying-artifacts | 须校验 subject digest、buildType、externalParameters |
| T1 | OCI Content Descriptors | https://github.com/opencontainers/image-spec/blob/main/descriptor.md | digest 为必需字段，不可信源须按 digest 复验 |
| T1 | DSSE protocol v1.0.2 | https://github.com/secure-systems-lab/dsse/blob/master/protocol.md | 签名绑定 type+body；验签体须与送应用层同体 |
| T1 | in-toto Statement v1 | https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md | subject 每项 MUST 带 digest，subject 视为不可变 |
| T1 | git-diff | https://git-scm.com/docs/git-diff | `A...B`=merge-base→B；出错即非零退出 |
| T1 | GitHub Actions Workflow syntax | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | step 非零退出即 job 失败 |
| T2 | Reproducible Builds Definitions | https://reproducible-builds.org/docs/definition/ | 同源同环境同指令可逐位复现，用哈希比对 |

**6 验收/回退**：F：坏 base 必红（不得落 no changed）；无变更打印 no-changed 且绿；三校验器 + 28 测试 + selftest 83/83 不变；回退 = revert 单 commit。C（另批）：P≥N 无 digest→红、验后改文档→红、finalize rebind 留原因、重放一致；回退 = 边界常量置满值即降为观察。

**7 不确定**：GitHub `bash` 默认 `-eo pipefail` 未在本轮回原文见到该串（E3）⇒ F 应显式 `set -eo pipefail`；force-push/首提交/新分支三种 BASE 未实测（E3）；digest 规范化（LF、front-matter、排序）未定；JSONL 无哈希链，改写历史行不可检出。

**验证记录**：只读统计脚本（Python，`tools/spec_runner/sessions`）：152 个 `specwf-p*`、156 个 jsonl、729 decision、7 gate（全部来自 demo/probe/homing 4 文件）、session_start 0。PowerShell：`git diff --name-only nonexistentrev...HEAD` → exit 128、零输出（印证 `|| true` 的 fail-open）。`python scripts/step_enforce.py --base <坏 SHA> spec/.../RESEARCH.md` → exit 2 + 「git error」。`git show --stat` 41bb0c4 / 3bc99fa / c779e6d：三次提交均改同一组四文档。测试面计数：`tests/` 共 28 个 test 方法。未运行三校验器与 unittest（只读分析，未修改任何文件）。

**未验证项**：GitHub Actions `bash` 默认 `-eo pipefail` 未取到原文字符串，标 E3。伪造 digest 的可行性为代码推断（cmd_gate_step 只读 decision；JSONL 无链），未做实际篡改实验（受只读约束）。首次提交 / force-push / 新分支三种 BASE 情形未构造实测；未在真实 PR 上验证 CI 修复效果（需改文件）。未验证 `session_start` 若入库后与 `run` 子命令现有 input 形态（task/model/provider/endpoint）的双形态兼容问题，仅为代码阅读推断。

**关键制品**：`spec/framework-deep-review/RESEARCH.md`（§3.7 A-19、§7.6-7.8、§11.7 Phase 2 一行式规格、§11.9 L706）、`DESIGN.md`（§8 I-4 边界、§10.2「CI 变更集为空 exit 0」风险行）、`IMPLEMENTATION.md`（§3.6 P-132 声明面）、`.github/workflows/ci.yml` L52-70、`scripts/step_enforce.py`、`tools/spec_runner/spec_runner.py` L176-180 / L314-337 / L715。

**下一步**：先按 A 立项 F（改 ci.yml 变更集段：去 `|| true`、显式 `set -eo pipefail`、坏 base 显式失败）；C 另批需先裁决三处未决：digest 记录时点（建议 finalize 而非 verify）、per-batch 作用域与 rebind 规则、过渡边界常量。

### D.2 U-7：是否批准 Cpp_Hub 第二轮吸收作为 pilot

**子代理检索降级**：本环境无 MCP 检索工具，改用 WebSearch/WebFetch，已逐条回原文。

**1 结论摘要**：**不批（现在启动）。** A 的实证画像合格（三类真实依赖齐备），但 **S0 契约与 S1 工具尚未产出**——`spec/graph-structure-upgrade/` 仅有 RESEARCH.md（v1.2），无 DESIGN / IMPLEMENTATION，S2 无契约可测；且第二轮吸收在本仓**未立项**。另需订正：用户所称「U-7」实为 **U-1**（§10 第 368 行，pilot 对象未定）；U-7 = P4 前置三件（§14），与 pilot 选择无关。建议 **U-1 保持 open，U-7 不变**。

**2 Cpp_Hub 实证画像**（E1，HEAD `8748995` 2026-10-26）
- 跨模块依赖**真实**：`CMakeLists.txt:75-107` 三条 INTERFACE 目标链（core ← econometrics / timeseries_mat）；`README.md:52-76` 分层头目录；`DEVELOPMENT_LOG.md:3123` 缺陷随 statsmodels 源码转录（上游同病）。
- 写汇聚**真实**：每批同改 header+test+CMake+README+`CHECKLIST.md:314-330`+日志并互相引证（C-129/C-131 需 CI run id）；`DEVELOPMENT_LOG.md:3126` 实测并发构建撞树 MSB6003/MSB3073（真争用）。
- 迭代**真实**：`CHECKLIST.md:329`「1−Φ 族**第 4 例**」+ TDD 行为红先；`DEVELOPMENT_LOG.md:3114` 遗留登记 → `:3118` 下批闭环（跨批依赖链）。
- 执行装置已在：`agent-out/202609251226552846/.agent-run.json:11,36,63-140` 有 content_digest、prompt_sha256、evidence_manifest（10 subject 各 sha256）、`sensitivity: local-only`、slot gated、status=failed(exit 1)；`.agentsync` 排除 `.agent-lock`/`.agent-state.json`（单写者锁）。
- 卡字段缺口实证：`D:\RPC\spec\d6-agent-standard\test-cards\cpphub-beta.md:1-13` front-matter 无 depends_on/join/iter_budget/join_policy/graph_version。
- 存量材料：`spec/mcp-server/`（5 文档）+ 4 份 P2 RESEARCH 可支撑第二轮；但 `spec/cpp-hub-absorption/CHECKLIST.md:224-230` 仅 P-001/P-003/P-004 待排，无第二轮行。

**3 五维对比**

| 方案 | 成本 | 收益（可验字段/风险） | 兼容 | 维护 | 升级潜力 |
|---|---|---|---|---|---|
| A 二次吸收 | 中高；**未立项=范围未冻** | 五字段全可验；R1/R2/R4/R9 可测 | 高（纯文档 fail-soft） | 中 | 高（兼存量价值） |
| B Auto_Prover P3 | 高（Lean+真实形式化输入，B6 负载未满足） | 仅迭代预算；G3 层 ≠ 卡契约；D6 禁托管 | 低 | 高 | 中 |
| C 本仓多阶段批 | 中低 | 同 A 但无外部依赖方；自指→R8 | 高 | 低 | 中 |
| D 继续 open | 0 | 0；U-5/U-6 冻结 | — | 0 | 低 |
| E Cpp_Hub 代码批走 RPC 卡 | 中（触 P1/P2 未立项） | 最强：真 digest/local-only/slot/外部效应 | 中（D5 允附加字段） | 中 | 最高 |

**4 S2 判据核对**（◆可测 ◇部分 ×不可测）

| 判据 | 出处 | A | B | C | E |
|---|---|---|---|---|---|
| 真实复杂任务 | 7.3 | ◆ | ×(H1) | ◆ | ◆ |
| 片间依赖 | 7.3 | ◆ | ◆ | ◇ | ◆ |
| 写汇聚 | 7.3 | ◆ | ◇ | ◇ | ◆ |
| 迭代/重试 | 7.3 | ◆ | ◆ | ◆ | ◆ |
| 可机判条件边 | R4 | ◆（三校验器 exit） | ◆ | ◆ | ◆ |
| 崩溃注入 | R3 | ◇（无 checkpointer） | × | ◇ | ◇ |
| 并发 resume | R3/A-23 | ×（单写者） | × | × | ◇ |
| 产物 digest | M3/R9 | ◆（git blob） | ◇ | ◆ | ◆（已有 manifest） |
| 外部效应登记 | M4/X1 | ◇（仅 commit） | × | ◇ | ◆ |
| 预注册故障子集 | H8 | ◆ | ◇ | ◆ | ◇ |
| 不固化拓扑 | R6/7.5 | ◆ | ◇ | ◇ | ◇ |

**5 最小范围（待批时）**：1 个真实任务 = 第二轮吸收第 1 批 3 项机制（R→G 串联、证据回填-签收、行为红先登记）→ 3 片 + 1 join + 1 有界 Review 迭代；用全 5 字段；故障注入 2 点（写产物前/后）+ 1 例非法 graph_version + 1 例环种子。**非目标**：不改 RPC 内核、不引框架、不做并发 resume/分区演练（R5/R11 留 P4）、不手填读数、不重排既有拓扑。

**6 外部锚点**（2026-10-26 访问）
1. **T1** van Teijlingen & Hundley 2001, SRU35, https://sru.soc.surrey.ac.uk/SRU35.html — pilot = 缩小版正式研究，须显式报告过程与结果 ⇒ 读数必须落档。
2. **T1** Fowler, Strangler Fig (2024-08-22), https://martinfowler.com/bliki/StranglerFigApplication.html — 每段可独立回退 ⇒ S2→S3 分段。
3. **T1** Sato/Fowler, Canary Release (2014-06-25), https://martinfowler.com/bliki/CanaryRelease.html — 小流量先行、回退即改路由，代价是同时管多版本 ⇒ 双跑期成本。
4. **T1** Temporal, Workflow Definition (`#workflow-versioning`), https://docs.temporal.io/workflow-definition — 重放需确定性，改代码即需 versioning/patching ⇒ graph_version 须先冻结。
5. **T1** Airflow Best Practices (3.3.2), https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html — 任务须幂等、禁 now()、读写固定分区 ⇒ 文档幂等靠分区写+无时间戳。
6. **T2** Yin 2018《Case Study Research and Applications》6th ed.（书目级）— 单案例按理论复制选样，只支持分析性泛化 ⇒ 已登记 X5。

**7 验收/回退/不确定**：验收（若日后批 A）：5 条机械读数齐——拓扑序实测、join 后 digest 集合相等、重复副作用 0、fault 单元 TPR/FPR+基率+Wilson CI、图查询计数>0。回退：删图字段与派生视图，回退卡直读；不动既有权威源。不确定：① U-1 与 framework-deep-review 的 U-1（批次绑定）**重名**，已被本次提问误指为 U-7；② 第二轮机制清单未定；③ 单人仓并发 resume 能否「真实」而非模拟未定；④ Phase 2 落地后 digest 判据可从 ◇ 升 ◆。

**验证记录**：只读核查（全部实际执行）：Read `spec/graph-structure-upgrade/RESEARCH.md`（§7.3/§9/§13/§14/§10 全文）、`spec/cpp-hub-absorption/{DESIGN,IMPLEMENTATION,CHECKLIST}.md`、`spec/cpp-hub-gap-analysis/*`、`docs/PROGRESS.md:131-150`（P-118~P-132）、`docs/rework-graph.json`（forks=[]）；Grep 确认 `spec/graph-structure-upgrade/` 仅 1 个文件 RESEARCH.md（无 DESIGN）；Grep 确认 `scripts/` 与 `tools/spec_runner/` 无 digest/sha256（Phase 2 未实施），但存在 `gate` 事件写入（spec_runner.py:31,115,176）。Cpp_Hub 只读核查：README/CMakeLists/DEVELOPMENT_LOG/CHECKLIST/p1-fixes spec 目录、`git log`（HEAD 8748995，工作区 2 个 M 未提交）、`agent-out/.../.agent-run.json`、`.agentsync`、`D:\RPC` 卡文件。全部零写入。外部锚点：WebFetch 实取 4 页全文（SRU35 / Strangler / Canary / Temporal / Airflow），WebSearch 补 2 条书目级；Yin 未回出版社页，故标 T2 书目级并声明。未运行任何校验器（本任务为只读分析，不产生改动）。

**未验证项**：**U 编号错配**——用户问的「U-7」在 RESEARCH §10 中是 P4 前置（V-EXPORT/V-FENCE/V-LEASE），pilot 对象是 **U-1**；本报告按实质问题（pilot 裁决）作答并标注此错配，未修改文档更正。**第二轮吸收范围未定**：本仓无第二轮机制清单/Tier 分级（无 DESIGN、无 PROGRESS 行），故「A 的成本与收益」是按首轮结构与 Cpp_Hub 现存材料**推估**，非实测。**并发 resume「不可测」判断**基于单人开发者 + 单 agent 的现状推断；未做实际并发写实验。**R3 崩溃注入信息量低**的结论基于「A 路径无框架 checkpointer」推断（RESEARCH §7.1/§7.2 无运行时），未实测。Cpp_Hub 的 `MSB6003/MSB3073 撞树` 是构建产物争用证据，**不等于**文档级多写者收敛；文档级写汇聚只用「多账本互证」佐证。未核验 Cpp_Hub `spec/mcp-server/` 具体机制是否已被本仓吸收（仅读了 RESEARCH 目录结构）。

**关键制品**：`spec/graph-structure-upgrade/RESEARCH.md`（§7.3 L165-169 / §9 L329-360 / §10 L364-375 / §13 L456-519 / §14 L523-580）；`docs/PROGRESS.md:138-150`（P-125~P-132）；`spec/framework-deep-review/RESEARCH.md:464,501,689`；`F:\Cpp_Hub\README.md:19-27,52-76`；`F:\Cpp_Hub\CMakeLists.txt:75-107`；`F:\Cpp_Hub\spec\p1-fixes\CHECKLIST.md:308-330`；`F:\Cpp_Hub\docs\DEVELOPMENT_LOG.md:3114-3130`；`F:\Cpp_Hub\agent-out\202609251226552846\.agent-run.json:11,36,63-140`；`F:\Cpp_Hub\.agentsync`；`D:\RPC\spec\d6-agent-standard\test-cards\cpphub-beta.md:1-13`。

**下一步**：让用户确认「U-1 vs U-7」编号错配并按实质裁决：U-1 保持 open。若仍要推进，先立 S0 契约 DESIGN（5 字段词表 + 四组 fixture）与 S1 只读工具，再裁 pilot；pilot 候选优先级：A（第一）> E > C > B。

### D.3 U-5：校准集取 20 项读数还是 30+30 当门禁

**1 结论摘要**：推荐 **C（分阶段）**：先做 10 缺陷 + 10 干净（共 20 项）配对读数，达标后再扩到 30+30，且扩后先做「报告门」再升硬门禁。理由：20 项只能证明仪器在工作（区间宽约 ±17pp）；30+30 若直接做二值门禁，会把真 catch=0.90、误拒=0.10 的 reviewer 分别以 **35.3% / 95.8%** 概率误杀。

**2 五维对比**

| 方案 | 成本（构造+每轮） | 收益 | 兼容 | 维护 | 升级 |
|---|---|---|---|---|---|
| A 20 项读数 | 7–10h + 2–3h | 仅读数，CI 宽 0.27–0.40 | 高（零门禁） | 低 | 可加臂 |
| B 30+30 门禁 | 20–30h + 5–10h + 裁断 | catch/误拒可报告、可门禁 | 低（撞 §9「不加门禁」、RULE-6 Goodhart、T3 不加成本） | 高（阈值/老化/模型漂移） | 中（新模型须过门） |
| **C 分阶段** | 7–10h，达标后 +15–20h | 先可报告、后可门禁 | 高→中 | 中 | 最高 |
| D 暂不建 | 0 | 无读数，P1-3「有读数」验收不满足，U-5 悬置 | 最高 | 0 | 无 |

**3 统计功效（Wilson 95%，z=1.96）**：公式：中心 `(p̂+z²/2n)/(1+z²/n)`，半宽 `z√(p̂(1−p̂)/n+z²/4n²)/(1+z²/n)`。示例：n=20、k=16（p̂=.80）→ **[0.584, 0.919]，宽 0.335**；n=30、k=27 → [0.744, 0.965]，宽 0.222；n=60、k=54 → [0.799, 0.953]，宽 0.155。误拒 0/30 → [0, 0.114]；3/30 → [0.035, 0.256]。结论：20 项只支撑「读数」；30 缺陷仅支撑「catch 下界 ≥0.70」（需 ≥27/30）；「误拒 ≤0.10」需 0/60。配对比较：20 对需 **6 个单向不一致**才 McNemar p=0.031（b=5,c=0 仅 0.0625）。门禁操作特性：真 catch 0.90 过「≥27/30」仅 64.7%；真误拒 0.10 过「0/30」仅 4.2%。

**4 缺陷池与筛选成本**：M7 现有 **48 样本**（hits：P1 18 / P2 62 / P3 97 / 未标 8；形态 II **117**，**非任务背景所称 116**）。含 ≥1 P1/P2 的样本 35，其中 19 为工具拦截（非 LLM 审查）；LLM 臂约 18 样本、约 **51 条 P1/P2**。可直接重放的「脏快照」不足：至少 9 条明确「提交前拦截 / 未流入版本历史」，30 缺陷需重建或注入 15–20 条。成本：缺陷 20–40 min/条、干净 15–25 min/条 → 10+10 约 7–10h；30+30 约 20–30h；每轮 5–10 min/项（20 项 2–3h，60 项 5–10h），另加分歧裁断 30–50%。样本老化：文档版本/行号漂移，季度约 20–30% 失效。污染控制：生成臂与评审臂须不同 session、尽量不同模型族，记录模型版本；评审只给 digest，不给 session / M7 / PROGRESS。历史缺陷已在 M7 与仓库上下文中公开 ⇒ 已被现有审查与模型「见过」，只能作 dev set；测试集用冻结后新缺陷或跨仓样本，并分列 seen/unseen。

**5 外部锚点（访问 2026-10-26）**
1. **T1** Wilson (1927) *Probable Inference…*，JASA 22:209–212，https://www.jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf —— 小样本比例区间应 score 反演，非 Wald。
2. **T1** NIST/SEMATECH §7.2.4.1，https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm —— Wilson 对几乎所有 n/p 推荐，小 n 用精确二项。
3. **T1** QUADAS-2（Whiting 2011），https://www.bristol.ac.uk/population-health-sciences/projects/quadas/history/quadas-2/ —— 诊断准确性需四域偏倚评估；官方页已标由 QUADAS-3（2026）取代。
4. **T2** Cohen (1960)，https://doi.org/10.1177/001316446002000104 —— 机遇校正一致性，用于双标注 ground truth 认证（页码未回原文 E3）。
5. **T2** Jia & Harman (2011) 变异测试综述，https://huang.isis.vanderbilt.edu/cs4278-sp24/readings/mutation-testing.pdf —— 等价变异体仍未解决 ⇒ 干净样本须人工判定。
6. **T1** NIST AI RMF 1.0（AI 100-1），https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf —— MEASURE 1.1：不可测风险须显式记录。
7. **T2** 基准污染，https://arxiv.org/html/2311.09783v2/ —— 污染抬高读数，须登记公开时间与切分。
（仓内 T1 补充：Groundability arXiv:2610.01023 —— catch 与 over-rejection 必须成对报告。）

**6 验收判据 + 回退点**：Phase 1 预注册：10 缺陷 + 10 干净；同一 digest 双盲；基线 = 单 Agent 自查（RULE-4），处理臂 = 独立 Review（RULE-1，尽量 RULE-5 异构）；catch=TP/(TP+FN)、误拒=FP/(FP+TN)，报 Wilson CI + McNemar；ground truth 双标注 kappa ≥0.6。升级判据：catch ≥0.70、误拒 ≤0.20、≥6 个单向不一致 → 扩 30+30。Phase 2 门禁只绑 T1 高风险，用置信界 + 容差（**不得 0/30 硬门**），连续两轮或非劣效 δ=15pp；T3 不绑。回退点：门禁误拦 >2 次/季，或单轮评审 >2h → 退回读数模式，样本库保留。

**7 不确定项与降级**：无 MCP 搜索端点，降级 WebSearch（登记于本节）；仅 NIST 与 Bristol 两页回原文，其余为检索摘要级 T2/E3。Cohen/Jia 卷期页码未回原文（E3）。池子计数由 M7 正则解析（E1 近似，±2）。干净样本无金标准，存在参照标准不完美偏倚（QUADAS-2）。

**验证记录**：读取 `spec/framework-deep-review/RESEARCH.md`（§7.5 / §10 U-5 / §12）、`docs/M7_EVIDENCE_LOG.md`、`docs/PROGRESS.md` 相关行、`SPEC_PROCESS.md` RULE-1~6；确认全仓无任何校准集/标注集（Grep 仅命中 RESEARCH 中的设计意图）。用 Python 复算 Wilson 区间、McNemar 精确检验、二项操作特性；用正则解析 M7 48 行样本表，得 P1 19 / P2 64（含非标准计数），与 hits 块 18/62 存在 ±1~2 差。WebSearch 命中 Wilson、NIST、QUADAS、Cohen、Jia & Harman、NIST AI RMF、污染论文；WebFetch 回读了 NIST §7.2.4.1 与 Bristol QUADAS 两页原文。

**未验证项**：任务背景称形态 II 116 处，机械读数为 **117**，报告已按真值订正。M7 行内 P1/P2 的正则解析（19/64）与 hits 块（18/62）不完全一致，属口径/非标准单元差，未逐条人工核对。Cohen 1960、Jia & Harman 2011 的卷期页码未回原文；污染锚点为 T2 摘要级。「干净样本」缺乏金标准，false-rejection 率可能被低估（若干净样本实含缺陷）。成本估算（人时）为基于样本构造步骤的推断，未实测。

**关键制品**：`spec/framework-deep-review/RESEARCH.md`（§7.5 P1-3、§10 U-5、§12）；`docs/M7_EVIDENCE_LOG.md`（§1 48 样本、§5 hits：P1 18 / P2 62 / P3 97 / 形态 II 117）；`docs/PROGRESS.md`（132 个 P 行；无校准集）；`SPEC_PROCESS.md`（L233–285，RULE-1~6）。

**下一步**：若采纳 C：先立 Phase 1 预注册（20 项、10+10、双盲、Wilson+McNemar、kappa≥0.6），并在 M7 追加读数样本；30+30 仅作为达标后的第二阶段，门禁阈值须用置信界+容差。

### D.4 U-6：是否现在做 v2 修订（不执行）与是否改名 U-6a/U-6b

**子代理检索降级**：本环境无 MCP 检索工具，降级 WebFetch/WebSearch（`osf.io/prereg` 空返回，改用 `cos.io/initiatives/prereg`）；访问日 2026-10-26。

**1 结论摘要**：修订：**是**（v1.0→v1.1，仅执行前）。改名：**否**（旧编号零改动，仅新引用加限定 `framework-deep-review U-6`）。推荐 **E**。依据：① `U-6` 全仓 266 处/14 文件，**三个命名空间**同名——project-console 已关（120+36+13+12 处）、graph-structure-upgrade 未决（9 处）、framework 未决（仅 1 处）；只改一个命名空间不消除歧义，且撞「不改历史正文」（P-068 已关闭）。② §6 冻结条款字面边界是「执行开始后」，执行前修订合法。③ 真缺口是「只有文档指标、缺效果/成本指标」，不是编号。

**2 五维对比**

| 方案 | 成本 | 收益 | 兼容 | 维护 | 升级 |
|---|---|---|---|---|---|
| A 修订+U-6a/b | 高（≈265 处含历史） | 中（指标↑，歧义仅部分消） | 低（破 P-068 锚点） | 高（仍三同名） | 低 |
| B 修订不改名 | 低（1 文档+3 视图+1 P 行+session） | 高 | 高（grep 仍歧义） | 低 | 中 |
| C 只登记 | ≈0 | 0（点名后须临时改） | 最高 | 0 | 低 |
| D 只改名 | 高 | ≈0（歧义不减） | 低 | 高 | 低 |
| **E 修订+新引用限定** | **低**（0 历史改动） | **高** | **高** | **低** | **高** |

**3 v2 最小字段集（M6-M10 辅助，不参与判据）**
- M6 终态一致率 = 终态=立案声明目标批次数÷已关闭批次数（done/blocked/abandoned/superseded）；源=外部仓状态列；缺→N/A。
- M7 客观人工工时 = Σ 相邻事件间隔≤30min 的连续片段（分钟，中位+IQR）；源=session JSONL；仅 commit 时间戳→降级「跨度工时」标 E3；无→N/A，禁自评替代。
- M8 后续缺陷密度 = 后续≤2 批同源再修正数÷千行变更；源=外部返工图等价物；无记录→N/A（不记 0）。
- M9 总成本 = 人时+机时（hook/CI 墙钟）+外部调用费，三项分列不折单一货币；缺项标「不完整」。
- M10 门禁误报率 = 复核判合法阻断数÷总阻断数（Wilson 95%CI）；无门禁→N/A。
- 主观满意度 1-5 单列，不作判据、不替代 M7；并列报告差值方向（A-26：自评 −20% vs 客观 +19%）。
- 干预协议：本仓零写入；执行卡/回填块存外部仓；本仓只留指针+M7 摘要行（补 A-17 的 §4/§8 矛盾）。

**阈值纪律**：M1-M5 表与 §6 逐字不变（70%/20%/≥2-3 仓/不确定）；新增指标无阈值；只在「任一外部仓 T0 数据落盘前」可加，之后作废；v1.1 冻结日=落档日；§10 增 v1.1 条目、旧版不可编辑。三锁=§6 diff 为空 / M6-M10 不入门禁 / 修订历史注明依据。

**4 改名影响与迁移清单**
- U-6a/b：grep「U-6」仍命中 graph 9+PC 248 处；须改 CODE_WIKI 36、PROGRESS 31、dev-log 7、CONSOLE 1——违「不改历史正文」。
- U-6(EXT)/U-6(PC)：grep 需转义 `\(`，裸「U-6」仍歧义。
- 仅新引用加限定（推荐）：旧文零改，grep 单值仍唯一，靠既有「先甄别 feature」纪律。
迁移（只读）：`docs/EXTERNAL_VALIDITY_PREREG.md` L4(版本)、L13/L16(状态仍 registered-unexecuted)、§4 L39-45(+5 行)、§6 L56-62(不动)、§7 L64-73、§8 L75-78、§10 L86-89、新增 §12；`CODE_WIKI.md` L8(banner)、L141(树 v1.0→v1.1，5→10 指标)、L798(§9 同)、§10 `progress_tasks` 132→133；`adr/ADR-0007` L314(附录 A「5 项机械指标」)、L346(修订行)；`docs/PROGRESS.md` 新 P-133 行+(必要时)L199/L216/L257；`docs/CONSOLE.md` 重生成；新增 `specwf-p133-20261026` session。

**5 外部锚点（T1，2026-10-26 抓取）**
1. [COS Registered Reports](https://www.cos.io/initiatives/registered-reports)：数据前评审、依注册方法则临时接受 ⇒ 冻结方法不冻结结果。
2. [OSF Preregistration](https://www.cos.io/initiatives/prereg)：计划/非计划二分，同一数据不得既生成又检验假设 ⇒ 修订须在见数据前。
3. [SPIRIT 2025 / CONSORT 2025](https://www.consort-statement.org/)：34 项协议+30 项报告清单 ⇒ 指标可逐项核。
4. [Cochrane Handbook Ch.13](https://training.cochrane.org/handbook/current/chapter-13)：non-reporting bias ⇒ 缺测记 N/A 不记 0。
5. [METR task-horizon](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)：以任务时长作能力量纲 ⇒ 客观工时可作主指标。
6. [arXiv:2505.23419 SWE-bench-Live](https://arxiv.org/abs/2505.23419)：活基准抗污染 ⇒ 外部仓须登记时点。

**6 验收判据 + 回退点**：1) §6 与 M1-M5 逐字 diff 为空；2) M6-M10 全带 N/A 规则；3) 干预协议消解 §4/§8 矛盾；4) 三校验器 0 违规+`console_gen --check` 一致+`step-enforce` 5/5；5) 状态仍 unexecuted、零外部写入；6) 三视图+ADR 附录 A 同步；7) 新引用含限定词。回退：还原 v1.0+删 §12+还原视图行+删 P-133/session——单文件可逆、零数据迁移。

**7 不确定项**：多数 G-11b 候选仓缺 session/返工记录（Coupla 仅 `research_log.md`）⇒ M7-M9 预计 N/A 率高，须预先声明防事后补造；graph 亦持 U-6 ⇒ 议题应扩为「U-* 引用书写纪律」；front-matter `status: active` 与正文 unexecuted 不一致（DC1 不校验枚举），建议 v1.1 改 `registered`；CODE_WIKI/ADR 的「5 项」属自然语言，DC5 不覆盖，无机械门禁。

**验证记录**：直读 `docs/EXTERNAL_VALIDITY_PREREG.md` 全文、`spec/framework-deep-review/RESEARCH.md` §7.6/§10/§12、`spec/project-console/RESEARCH.md` §7.29、`docs/PROGRESS.md` P-104/P-114/P-124 行、`scripts/dc_validator.py` M6 判据面（L388-440）。机械计数：全仓 `U-6` = 266 处/14 文件；framework 1 处、graph 9 处、PC 120/36/13/12/36/31/7/1；`CODE_WIKI` `progress_tasks` = 132。六个 URL 实际抓取成功；`osf.io/prereg` 返回空，已降级并登记。未修改任何文件（`git` 未执行，纯读）。

**未验证项**：无 MCP 检索可用，属强制降级，非全量学术检索（未做系统检索式复核）。未验证 `repo_stats` 对「docs 目录计数/指标数声明」是否有机械模式；「指标数 5→10」是否触发门禁仅按 P-106 边界推断，未实跑校验器。未核验 `adr/ADR-0007` 附录 A 是否另有版本写法受 DC5 约束（该行无版本号，判断为不受约束，未实跑）。未核验三个 G-11b 候选仓实际具备哪些数据源（仅 Coupla 依据 P-124 快照），M7-M9 可得性为推断。未产出实施补丁（任务为只读分析，符合范围）。

**关键制品**：`docs/EXTERNAL_VALIDITY_PREREG.md`、`spec/framework-deep-review/RESEARCH.md`、`adr/ADR-0007-unified-document-contract.md`、`CODE_WIKI.md`（L141/L798/L8）、`docs/PROGRESS.md`（L127/L199/L216/L257）、`spec/graph-structure-upgrade/RESEARCH.md`（L373/L455）。

**下一步**：若用户选 E：按第 4 节清单执行 v1.1 修订（同文件编辑严格串行，改后全覆盖终验 grep + 三校验器 + `console_gen` 重生成）。

### D.5 U-9：是否接受独立 SUMMARY.md + 指针，而不是写 PROGRESS

**子代理检索降级**：本环境无可用 MCP 搜索（插件清单无 search MCP），全程降级 WebSearch/WebFetch；8 条锚点均 2026-10-26 访问，其中 7 条 T1 为官方页逐字读取。

**1 结论**：不接受「独立 SUMMARY.md + 指针」作为当前动作；选 **D（扩展现有生成视图）**。理由：compact 当前状态已有 100% 机械载体（CONSOLE，`--check` 字节级防漂移），新增 SUMMARY 只增第三载体而不降触点；真实成本在 CODE_WIKI banner/§9 与 PROGRESS 汇总表（判断性、不可派生）。

**2 五维对比**（A=SUMMARY+指针 / B=现状 / C=PROGRESS 内嵌生成块 / D=扩 CONSOLE）

| 维度 | A | B | C | D |
|---|---|---|---|---|
| 成本 | 中：新脚本或改 I-1、新 hook/CI、`declared.scripts` 10→11 | 0 | 高：首个 PROGRESS 写者（现全仓无） | 低：`console_gen` 单文件 + 1 条 selftest |
| 收益 | 无（触点不减，除非同时删 PROGRESS 汇总行） | 0（同族欠账已 3 例：P-052/053/103） | 低 | 中：compact 可见、零漂移面 |
| 兼容 | 需目标同批存在（M5 否则 P2）、避 PT 形态、scripts 自增 | 全兼容 | 高危：块内 `\| P-xxx \|` 行污染 `progress_tasks` 与 `spec_map.changed_pids` | 全兼容（console 非 stats 载体） |
| 维护 | 双载体（SUMMARY↔CONSOLE） | 双载体 | 生成器与人写共处一文件 | 单载体 |
| 升级 | 跨仓可搬（需 digest） | 差 | 差 | 中（同源输入，跨仓仍需 digest） |

**3 单一真值与 digest**：SUMMARY 只能是生成物，输入 = PROGRESS 字节 + CODE_WIKI §9 切片 + feature 四文档存在位 + sessions 清单哈希；真值仍是 PROGRESS/§9/sessions，生成物**不得含判断性文案**（否则即第二真值）。digest = sha256(生成器源码 + 输入按固定顺序带长度前缀)，写头部 `source_digest`；校验以字节比对为主（现有 `--check` 即足），digest 仅跨仓消费（RESEARCH Phase 3）才必要，现在加属过度设计。exit 0/1/2 沿用；**并入 console-gen 而非第 7 道 hook**（输入面相同、files 正则已覆盖、CI 已有 `--check`+selftest；独立 hook 连带 `declared.hooks` 6→7、PT-8、树、README 四处）。指针用**引用块** `> 当前状态摘要：<链接>` 而非表格行——`P_ROW_RE`/`RE_P_TASK` 只匹配 `^\| P-xxx |`，`progress_tasks` 仍 132。

**4 触点实测**（git numstat，P-123~P-132 十批）：每批必改 3 个视图文件——CODE_WIKI 5–11 行、PROGRESS 1–7 行、CONSOLE 4–32 行（人工 0）；P-126 例外再 +4（README×2/SVG/M7）。故 B=D「2 文件/5–14 处」，A「3 文件/6–15 处」且不降，C 同 A 且带污染风险。降触点的唯一杠杆 = 把 PROGRESS 汇总区（152 行后 94 行表格）降级为「登记态」，与是否新增 SUMMARY 无关。

**5 外部锚点**（T1 7 / T2 1）
- **T1** mdBook [SUMMARY.md](https://rust-lang.github.io/mdBook/format/summary.html)：章节清单/顺序/层级的**目录结构**（原文 "Without this file, there is no book"），**不是状态摘要**，不可直接类比，仅可类比「指针文件」形态。
- **T1** [towncrier](https://towncrier.readthedocs.io/en/stable/)：小 fragment 汇聚成 digest，为读者非写者；官方含 pre-commit 集成页。
- **T1** [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)：「不一致的日志与没有一样危险，用户会误以为是唯一真值源」⇒ 直接印证双载体风险。
- **T1** [Changesets](https://github.com/changesets/changesets)：贡献者声明变更 → 工具生成版本与 changelog。
- **T1** [Sphinx toctree](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree)：文件关系与 TOC 的集中机制（纯结构）。
- **T1** [GitHub 自动 release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)：由 PR/标签机械生成、可配 categories；生成物**可人工改**⇒ 漂移面。
- **T1** [Backstage descriptor-format](https://backstage.io/docs/features/software-catalog/descriptor-format/)：声明式输入（catalog-info.yaml），非生成汇总。
- **T2** [Diátaxis](https://diataxis.fr/)：按读者需要组织文档 ⇒ 读者向「当前状态」与维护者向「裁决/历史」应分置。

**6 验收判据 + 回退**：D 验收 = ①selftest 全绿（新增 1 例覆盖 compact 块）；②`--check` 0 且双跑字节一致；③三校验器 + 六 hook 全绿；④P 行仍 132、`declared.progress_tasks` 不变、§6 缺口行不变；⑤连续 3 批人工触点 ≤6 处且无 P-052/053/103 型欠账；⑥块内每行可机械派生。回退 **R-S1** = 删块与 selftest（先 `--check` 存基线），删后与现状逐字节一致。若复审升级 A′：I-1 改「声明产物集」+ 引用块指针 + **同批删掉 CONSOLE 重复 compact 块**（防第三载体）+ 不登记 §9/doc_registry（无 front-matter ⇒ DC 契约不适用、无版本漂移面）；回退 = 删文件/指针 + 还原 I-1。

**7 不确定项**：①触点下降未实测（U-9 判据需 3 批样本）；②PROGRESS 汇总行哪些属「非每批必更」是裁决非机械；③digest 跨仓收益无证据；④近 10 批多为 T3/T1 工具批，纯 T1 完整管线批次触点未采样。

**验证记录**：已读 `console_gen.py`（I-1~I-10、`--check`）、`repo_stats.py`（PT 模式、declared 七键、`RE_P_TASK`）、`spec_map.py`（`P_ROW_RE`/`changed_pids`）、`.pre-commit-config.yaml`（6 hook）、`ci.yml`、CODE_WIKI §9/§10（132/scripts 10/hooks 6）、CONSOLE 头、PROGRESS 头与 P-128~P-132、RESEARCH §7.7 与 U-9。实测 `git log --name-only/--numstat -10` → 触点表；计数 → PROGRESS 405 行/544,474 B/132 P 行/汇总区 94 行、CONSOLE 941 行、CODE_WIKI 597,727 B；8 条外部页 WebFetch 逐字读取。未运行任何校验器（只读代理，未修改仓内文件）。

**未验证项**：「触点下降」未复测（需实施 D 后取 3 批样本），仅给出判据。digest 方案无实现、无跨仓需求证据；A′ 去重工作量未估算。PROGRESS 汇总行的可降级范围只估算，未逐行定性。

**关键制品**：`scripts/console_gen.py`、`scripts/repo_stats.py`、`scripts/spec_map.py`、`.pre-commit-config.yaml`、`.github/workflows/ci.yml`、`docs/PROGRESS.md`、`CODE_WIKI.md`、`docs/CONSOLE.md`、`spec/framework-deep-review/RESEARCH.md`。

**下一步**：采纳则先在 `console_gen` 加 compact「当前状态」块 + 1 条 selftest，重生成 CONSOLE 并按判据⑤做 3 批复测；仍复发再按 A′ 最小步骤升级。

### D.6 五项推荐汇总（主臂整理）

| 项 | 直接回答 | 关键理由 |
|---|---|---|
| **U-10** | **F 单独立项先做；C 不同批** | C 有三处未决（digest 记录时点 verify/finalize、per-batch 作用域与 rebind、过渡边界）；152/152 历史 session 无 gate/digest，同批会把「历史零回归」变成全红。若必须同批：同 PR 两提交，commit 1=F，commit 2=C，且 C 边界/rebind 规则先预注册 |
| **U-7** | **批候选，不批现在启动；继续 open** | Cpp_Hub 实证画像合格（CMake 三条 INTERFACE 依赖链、多账本写汇聚、1−Φ 族第 4 例迭代、agent-out 已有 digest/manifest），但 S0/S1 未产出，S2 无契约可测；第二轮吸收范围未冻结 |
| **U-5** | **20 项先读数，30+30 达标后当门禁** | 20 项 Wilson 95% 区间约宽 0.335（示例 [0.584,0.919]），只能证明仪器在工作；30+30 直接硬门会误杀真 catch=0.90 的 reviewer（过「≥27/30」概率约 65%）、真误拒=0.10 过「0/30」概率仅 4.2% |
| **U-6** | **现在做 v2 修订（不执行），不改名；新引用加限定词** | `U-6` 全仓 266 处/14 文件、三个命名空间；改成 U-6a/b 只改一个命名空间，仍剩 graph U-6，且破坏 P-068 历史锚点；执行前修订合法 |
| **U-9** | **不接受独立 SUMMARY.md 取代 PROGRESS；先扩 CONSOLE** | CONSOLE 已是 100% 机械载体（`--check` 字节级防漂移）；新增 SUMMARY 只增第三载体。近 10 批触点主要在 CODE_WIKI 与 PROGRESS，SUMMARY 不降这些判断性回写 |

**与上一轮推荐的差异**：U-10 上轮 F+C → 本轮 F 单批、C 另批（新证据：C 三处未决 + 152 历史零 gate）；U-7 上轮批 Cpp_Hub → 本轮批候选、不批启动（新证据：S0/S1 缺失）；U-6 上轮改名 → 本轮不改名（新证据：U-6 三命名空间 266 处）；U-9 上轮独立 SUMMARY → 本轮扩 CONSOLE（新证据：CONSOLE 已存在、SUMMARY 不降触点）；U-5 与上轮一致（20 先读数，30+30 后门禁）。

> **本附录状态**：五份报告已全文落档，**未据此修改 DESIGN / IMPLEMENTATION / CHECKLIST 的裁决**（五项目前仍为未决；用户裁决后另开批次）。主臂复核订正与 M7 计数漂移订正已登记于 D.0。

---

## 附录 E：U-10 / U-7 裁决与复审过程记录（P-135，2026-10-27）

> **定位**：本附录 = P-133 附录 D（五份子代理报告）与 P-134（订正后实施）之间两轮过程的完整档——**裁决建议轮**（对话内给出推荐与理由，未改仓）与**复审轮**（用户指令「review上述裁决 检查逻辑链 事实锚点 排除幻觉」）。D.0 复核增补块 = 四项订正的**摘要落点**；本附录 = 过程与依据的**完整落点**，两者互补。裁决建议轮的逐字对话文本不回写入档，本附录以 D.6 推荐汇总表 + 复审订正记录为准绳复述。

### E.0 过程时间线（四段，U-10 / U-7 范围）

| 段 | 时点 | 动作 | 载体 |
|---|---|---|---|
| 1 | 2026-10-26 | 五份子代理报告全文落档（含 D.6 推荐汇总表 U-10 / U-7 行） | P-133 · 附录 D |
| 2 | 2026-10-26 | 用户点名 U-10 / U-7 待决项 ⇒ 裁决建议轮（对话内推荐 + 理由，未改仓） | 本附录 E.1 / E.2 |
| 3 | 2026-10-26 | 用户指令「review上述裁决 检查逻辑链 事实锚点 排除幻觉」⇒ 复审轮发现 4 项偏差并订正裁决文本 | 本附录 E.3 |
| 4 | 2026-10-26 → 10-27 | 用户指令「按订正后的裁决文本执行」⇒ P-134 实施 + 归档数字订正；随后「完整落档」⇒ 本附录 E（P-135） | P-134 / P-135 |

### E.1 U-10 裁决过程（Phase 2 立项与批次边界）

**待决项（用户原文）**：「U-10 是否立项 Phase 2（F 必做，C 是否同批）」。

**裁决建议（对话内，2026-10-26）**：采纳 D.6 推荐汇总表 U-10 行「**F 单独立项先做；C 不同批**」，并补两条结构性理由——(i) **F 是 C 的前提**：CI run 块中变更集为空 ⇒ `step_enforce` 不被调用 ⇒ 未来 digest 门禁同被跳过，先修 fail-open 是 C 的前置条件；(ii) C 同批会把「历史零回归」变成全红——151/151 历史批次 session 均无 gate / digest 记录（D.0 订正口径），任何「必须带 digest」的门禁将立即全量判红，违反分批的可回退性。若必须同批，唯一可接受形态 = 同 PR 两提交（commit 1 = F / commit 2 = C）且 C 的边界与 rebind 规则**先预注册**（D.6 行原文）。

**用户裁决（订正后执行，2026-10-26）**：F = P-134（T1，命中 `.github/workflows/` 路径集，已实施 + 本地注入 5/5）；C 不并入，另批候选；三处未决**预注册**——digest 记录时点（倾向 finalize 而非 verify）、per-batch 作用域与 rebind 规则（finalize 末次改文档后 rebind 并留原因）、过渡边界（提案 `EVIDENCE_MIN_P = 135`）；`session_start` 留 Phase 2b 单独裁决。

**候选批编号顺延（2026-10-27）**：预标 P-135 被本落档批（P-135）占用 ⇒ C 顺延 **P-136 候选**（§10 U-10 行 v1.7 起以此为准；传导面见 E.4）。

**复审对裁决的修正**：无主体推翻；两处表述面订正（E.3 ②④）。

### E.2 U-7 裁决过程（pilot 启动与否）

**待决项（用户原文）**：「U-7 是否批准 Cpp_Hub 第二轮吸收作为 pilot；若不批，U-7 继续 open」。

**编号澄清（复审同轮确认）**：U-7 在图 S2 语境的 pilot 对象实为 **graph U-1**（编号错位，D.0 表登记；§10 U-7 行标题已随 P-134 重写并标注）。U-7 本体议题 = Cpp_Hub 二次吸收 pilot。

**候选资格实证（裁决建议引用，复审确认无幻觉，E1）**：Cpp_Hub 实证画像七项锚点——三条 INTERFACE 依赖链（CMakeLists L75 / L94 / L106）、多账本写汇聚、1−Φ 族第 4 例迭代闭环（L3114→L3118）、agent-run.json 五字段、RPC 卡缺五图字段、mcp-server 恰 5 文件、absorption CHECKLIST 无第二轮行。

**裁决**：**批候选、不批现在启动**（U-7 维持 open）——graph 目录仅 RESEARCH.md（无 DESIGN / IMPLEMENTATION），S0 契约与 S1 只读工具未产出，S2 无契约可测；启动前置 = graph S0 DESIGN（`depends_on` / `join` / `iter_budget` / `join_policy` / `graph_version` 五字段 + fixture）+ S1 只读工具 + 第二轮吸收范围冻结；候选序四档 = Cpp_Hub 二次吸收 > Cpp_Hub 代码批走 RPC 卡 > Spec_Workflow 多阶段批 > Auto_Prover P3（§10 U-7 行）。

**复审修正**：编号错位澄清并入裁决文本（D.0 表 + §10 U-7 行标题）。

### E.3 复审轮记录（逻辑链 / 事实锚点 / 幻觉排除）

**方法（三轮）**：(a) **逻辑链检查**——推荐理由的前提-结论链逐条复走（同批全红风险 / F 是 C 的前提 / S0 缺失不可测 / 编号错位是否影响结论）；(b) **事实锚点核验**——推荐文本中每个可数、可定位声明回源码或回文件（Cpp_Hub 七项锚点 / 批次计数 / GitHub 默认旗标）；(c) **幻觉排除**——对「听起来具体但未锚定」的表述逐一索证，无锚即降级或订正。

**发现四项偏差（全部为表述 / 计数面，无主体推翻）**：

| # | 偏差 | 根因 | 订正 | 落点 |
|---|---|---|---|---|
| ① | 批次计数 off-by-one：152 → 151 | naive 子串前缀 `specwf-p` 误计 `specwf-probe-20260907.jsonl`（非批次文件） | 严格正则 `specwf-p\d{3}-` 复测 = **151**（156 jsonl / 5 非批次文件，P-133 时点）；151/151 gate=0 比例不变 ⇒ 对 U-10 结论零影响 | D.0 第 1 行 + D.0 增补① + PROGRESS P-133 行 + CODE_WIKI banner（均 P-134） |
| ② | pipefail justification 错误 | 原表述「显式 `set -eo pipefail` 消除默认差异」不成立——GitHub Actions `shell: bash` 官方默认即 `bash --noprofile --norc -eo pipefail {0}`（T2 双源） | 定性改「自文档化冗余」，不构成行为变更 | ci.yml 注释 + D.0 增补② |
| ③ | B6 / D6 引用号混叠 | 附录报告正文引用编号与附录编号混叠（L3127 行号锚） | 登记，D.1 原文逐字保留不改、以 D.0 为准 | D.0 增补③ |
| ④ | F 方案两个新红边未登记 | 裁决文本漏记 fail-closed 化的完整行为变化面 | 补登记：根提交回退 `BASE=HEAD`（三点空 diff ⇒ 显式绿灯不崩溃）+ force-push 非祖先 base ⇒ 红；并本地注入 5/5 验证 | D.0 增补④ + ci.yml + DESIGN §8 注记（均 P-134） |

**幻觉排除确认（核验通过锚点）**：Cpp_Hub 七项（E.2 清单，E1）；GitHub Actions `shell: bash` 默认旗标（官方文档，T2 双源）；git 三点 diff 依赖 merge-base、空树 hash `4b825dc642cb6eb9a060e54bf8d69288fbee4904`（git 官方文档，T2）。

**复审结论**：裁决主体成立（F / C 分批；U-7 批候选不批启动）；四项偏差均为表述 / 计数面，**订正后文本即 P-134 执行依据**。

### E.4 登记面与残留（诚实边界）

- **编号顺延传导**：C 候选批 P-135 → **P-136**；同步位点 = §10 U-10 行（本版 v1.7）+ PROGRESS P-134 行 ⑤ + 本节；**不回改**的时点记录 = CODE_WIKI v1.183 banner / 树与 §9 的 P-134 描述 / DESIGN §8 注记块（2026-10-26 时点记载）/ session `specwf-p134` 事件流——历史记载不重写，标签以本节为准。
- **对话内裁决建议不逐字入档**：本附录以 D.6 推荐汇总表 + 复审订正为准绳复述（对话文本无独立真值价值，入档反而制造第二真值源）。
- **范围**：本附录仅 U-10 / U-7（用户指令范围）；U-5 / U-6 / U-9 仍为推荐态，见 D.3~D.5 与 D.6 表。
