---
id: ADR-0011
type: adr
version: 1.7
status: accepted
date: 2026-09-09
depends: [ADR-0007, ADR-0010, step-gate-DESIGN, community-ecosystem-RESEARCH, FWK-DECISION-RECORD]
upstream: null
---

# ADR-0011: step-gate（P-020 决策产物管线）未生效排查——触发依赖与表演性决策软肋 + 社区解法映射登记

## 元数据

| 字段 | 值 |
|------|-----|
| 编号 | ADR-0011 |
| 日期 | 2026-09-09 |
| 状态 | accepted（2026-09-09 用户裁决「ADR-0011 决策为 A + C 组合收口」） |
| 决策者 | Scott (鹏) + Trae |
| 相关文档 | [step-gate DESIGN](../spec/step-gate/DESIGN.md) v1.0（管线设计）、[FWK-DECISION-RECORD](../docs/DECISION_RECORD_CONTRACT.md) v1.1（决策契约）、[ADR-0010](./ADR-0010-lazy-loading-architecture-gate.md)（三问门禁）、[step-gate CHECKLIST](../spec/step-gate/STEP_GATE_CHECKLIST.md) v1.2（三问 8/8）、[spec_runner.py](../tools/spec_runner/spec_runner.py) v1.2.0（实现）、[COMMUNITY_ECOSYSTEM_RESEARCH.md](../spec/community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) v1.7（CER §3.5 裁定） |
| 取代 | 无 |

## 背景（Context）

### 1. 排查触发事实（E1 机械可证）

P-023（drift-gate 概念吸收，2026-09-09）按 spec 工作流走完 RESEARCH → DESIGN → 懒加载 gate → 落档全流程，但：

- `tools/spec_runner/sessions/` 下**无任何 P-021 / P-022 / P-023 session**（唯一含 `decision` 事件流 = p020 系列两个 session：`specwf-p020-20260908.jsonl` 4 条 + `specwf-p020-20260908v2.jsonl` 5 条 + 5 步链 `step-gate --expect` exit 0 实证）
- P-023 全流程 **0 条 decision 事件入流，step-gate 命令未调用**
- 对照：P-020 自身走的是完整 5 步决策链（research/design/implement/verify/finalize）

### 2. 诊断一：step-gate 是值守机制，非强制机制（触发依赖）

回溯 [step-gate DESIGN §1/§3.1/§3.2](../spec/step-gate/DESIGN.md) 与实现 [spec_runner.py L184-238](../tools/spec_runner/spec_runner.py#L184-L238)：

- 管线第一步角色 = **「生成端写 decision 事件」**（§3.2 模块「decision 写入（生成端）」），产出权完全在生成端（agent）手里
- `cmd_gate_step()` 只能在**已有 session 被调用**时检查空流/缺步（无 decision 事件 = exit 1）；**无法检测「session 根本没被创建」**
- DESIGN §6.3 明示「不加入默认 gate hook 链——触发驱动（Q3c）」
- 结论：P-020 生效是因任务本身就是测它（必然调用）；P-021（桥落地）/ P-022（缺陷修复）/ P-023（概念登记）三类批次**均未唤起 runner**（无 session 文件，E1 实证）→ 整条管线不显现。**管线只在生成端「选择调用它」时存在——P-020 之后三连批失效，值守机制失效是系统性而非 P-023 特例**

### 3. 诊断二：decision 事件存在表演性决策软肋（反幻觉目标直接威胁）

[FWK-DECISION-RECORD §0/I-4](../docs/DECISION_RECORD_CONTRACT.md) 明示：契约管**记录的结构完整性**，且「本契约不是验证机制」。step-gate 用法放大了这一点：

- decision 事件被当作**下一轮审查唯一输入**（step-gate DESIGN §1「下一轮审查以事件流为唯一输入」）
- 但其内容（reasoning / outcome / **evidence 锚点**）**全部由生成端自填**；`step-gate` 只机械查「非空 + 锚点形态（硬性-1/软性-3）」，**验证不了决策是否真实发生、锚点是否客观**
- 生成端完全可以填一份结构满格、锚点漂亮的 decision 流而不反映任何真实决策——审查臂会把这份「表演性决策流」当真吃掉。这与本仓「反形式化审查表演」核心目标直接对撞

### 4. 社区检索取证（2026-09-09，4 轮 WebSearch）

两缺口在社区均有验证解法，且社区已收敛出同一结论：**自治 agent 的自愿流程不可信；出路 = 流程级强制 + 证据客观化**。

| 缺口 | 社区方案 | 机制要点 |
|------|---------|---------|
| 缺口 1：流程依赖自觉 | MCP Task Orchestrator | schema 定义 agent 每阶段**必须产出**的产物，server **阻塞进展**直到产物完成（不止 gate 转换，设"规划下限"） |
| | Superpowers（130k★） | spec-first 强制：无 spec 无规划无代码；brainstorming 派**独立 spec-reviewer** 校验五维 |
| | SpecD | 生命周期状态机 `designing→ready→implementing⇄verifying→done→archivable`，verification 强制、漂移回退 revision |
| | StepProof | **hooks 是唯一硬强制**（PreToolUse 阻断）；每个 tool call 后 hook 触发**独立 verifier 查系统真实状态**（原文自白：「I can't be trusted to follow a process voluntarily. The system has to force it.」） |
| | Schema-gated orchestration（arXiv:2603.06394） | schema 作为 workflow 级**执行边界**：nothing runs unless 机器可校验 spec 通过 |
| 缺口 2：决策自填→表演 | OPERA（Verifiability-First） | 每次外部调用（API/文件/工具）**自动生成签名收据** append 到 Provenance Log，不依赖 agent self-report |
| | agent-prov | 无侵入 middleware 经 callbacks **自动捕获** Agent Step/Tool 记录，SHA-256 密封——decision 从「agent 手写 append」→「自动捕获」 |
| | StepProof 验证 agent | worker 声称完成 → verifier（异上下文/异激励）**独立查 git/db/真实状态**，不信 worker 的话 |
| | PROVENANCE-GUARD | provenance 判定 tool call 是否被 context 中**可溯源证据支撑**，pre-execution 拦截 |
| | From Agent Traces to Trust（arXiv:2606.04990） | W3C PROV 建模证据图；open problem = 统一 trace schema + claim-level 语义 provenance（本仓「意图图-证据图」= 此方向特殊化） |
| 兜底（非根治） | OpenAI confessions（忏悔报告） | 任务后额外诚实自报 + 重合度评分——**仍属自报**，社区视为兜底 |

**映射结论**：本仓 step-gate 现状两点都没做——① 流程强制没有（step-gate 是可选命令，未做成「进入下一步的阻塞 precondition」；本仓已有 pre-commit hook 可挂）；② 决策证据自报（`evidence.anchor` 为 agent 手填行号，`step-gate` 只查非空+形态）——而社区已实证这抗不住表演。

## 决策（Decision，proposed 2026-09-09）

**确认两项诊断成立（事实登记）**。**2026-09-09 用户裁决收口：决策 = A + C 组合**（A 流程强制根治缺口 1 触发依赖 + C 独立验证根治缺口 2 表演性决策；B 排除暂缓）。实施保持 ADR-0010 触发驱动——**A 的失效条件已命中**（P-021/022/023 三连批应走未走，90 日窗口，E1 实证），A 为下一候选实施批（待用户独立指令，收口不自动实施）；C 待 A 落地后触发。原「登记不实施」表述废止，改为「决策收口 + 触发驱动实施」。

1. **诊断确认**：step-gate 存在「触发依赖」（值守机制非强制机制）+「表演性决策软肋」（决策证据自报抗不住表演）。两者为 P-020 后 P-021/P-022/P-023 **三连批事件流缺失**的根因（E1 实证，4 应走批次仅 1 走），且与 CER §3.5 管线形态预期不符。
2. **出路 A（流程强制）**：把「session 必须存在 + decision 链完整」固化为**进入下一 spec step 的硬性入口**（本仓 pre-commit hook 级）。社区参照：SpecD / Superpowers / MCP Task Orchestrator（阻塞式进展）。
3. **出路 B（证据客观化）**：decision 事件锚点从**自报**→**机械可核**（机械可核 = 可由确定性程序验证——文件 hash / 结构校验 / 机械枚举，区别于 LLM/人工判断；本仓 E1 证据分级同构）。社区参照：OPERA 签名收据 / agent-prov middleware 自动捕获。
4. **出路 C（独立验证）**：审查臂（RULE-1/5）从「读事件流」→「查系统真实状态」（StepProof 式异上下文 verifier）。社区参照：StepProof / PROVENANCE-GUARD。
5. **三问预演（ADR-0010）**：Q1 出路 A/B/C 均为 **Layer-1**（spec_runner 演进）；Q2 激活条件 = **触发驱动**（用户裁决 / 失效条件触发，当前不排队不实现）；Q3 未激活副作用 = **0**（不实现即不存在，三校验器/scripts/hook 零改动）。

**边界声明**：本 ADR 只登记诊断与演进方向，**不引入任何实现**。step-gate 现有功能（EVENTS decision + cmd_gate_step）保持原状；spec_runner v1.2.0 不动。

## 三出路优先级与成本收益（v1.1 增补，2026-09-09 用户指令「补进 ADR-0011」）

### 1. 三出路解决的是不同层面

| 出路 | 解决什么 | 本仓现状 |
|------|---------|---------|
| A 流程强制 | 管线**不存在**（触发依赖）——session 不建、decision 不写 | 无 hook 强制，P-023 已实证缺席 |
| B 证据客观化 | 证据**可表演**（自报锚点）——锚点行号为 agent 手填 | decision 事件 self-report |
| C 独立验证 | 审查**信谁**——读自报流 vs 查系统真实状态 | 已有 RULE-1/5 独立 pass 机制，审查臂可增强 |

### 2. 成本收益分析

| 出路 | 成本 | 收益 | 局限 |
|------|------|------|------|
| **A 流程强制** | **低-中**：1 个 pre-commit hook + session 命名约定（`specwf-p0xx-*`）+ step-gate DESIGN 一处修订；**hook 实现需"应走管线"检测逻辑 + 失败阻断 + 错误恢复三件套**——P-022 教训（gate auto-commit F1/F2/F3 = cwd 硬编码/全目录 add/无条件提交）已实证 hook 级门控典型副作用，实施时须遵守 P-022 修复形态（`git_snapshot` opt-in 默认关 + 精确 sid 单文件 + 会话目录 git 根派生 + --no-verify） | 决策链必然存在、step-gate 真正生效、审查臂有稳定输入 | **必要不充分**——只保证"存在"，不保证"真实"；表演性决策软肋仍在 |
| **B 证据客观化** | **中**：spec_runner 增自动捕获/签名（agent-prov 式 middleware）；但**文档锚点的"机械可核"定义模糊**（§3.1 C-01 这类引用无法用文件 hash 验证——hash 只能验证"文件存在且未变"，验证不了"§3.1 确实支持该断言"） | 锚点可机械核对、压缩表演空间 | 文档型仓库中"可核"上限是文件级非断言级；与 C 目标重叠 |
| **C 独立验证** | **中-高**：**复用既有 RULE-1/5 独立 pass 形态**（P-008/P-014/P-016 已有先例），但既有独立 pass = 文档产出审核，C 审查对象 = 决策链真实性——**两者不同构，需重新定义审查输入**（从"读事件流"→ git diff / 文件状态 / 锚点真实性 + 纯登记型批次的查证范围定义）。本质是审查臂输入升级而非形态复用 | 审查查真实状态、不信自报——**最接近根治表演性决策** | 审查臂本身仍是 LLM，需机械取证支撑；纯登记型批次（无代码变更）查什么需定义 |

### 3. 优先级裁决（登记为触发序，非实施令）

**A → C → B**：

- **第一优先 A（低垂果实，消除已实证失效）**：成本最低-中、直接消除 P-023 这类缺席；本仓已有 pre-commit 三 hook 基建。价值上限 = 保证存在——但这是后续一切的前提。
- **第二优先 C（根治核心威胁，审查臂输入升级）**：本仓已有独立 pass 先例作为参考，但 C 不是形态复用而是**输入重定义**——成本比表面高；直击"表演性决策"这一与反幻觉目标直接对撞的软肋；**与 B 目标重叠且覆盖更广**（审查臂查真实状态本身就包含"验证锚点真实性"）。
- **B 暂缓至 C 落地后重评**：实现复杂度最高 + 文档仓中"机械可核锚点"定义模糊（文件 hash 验不了 §N 引用）；其目标（证据客观化）被 C 部分覆盖；若 C 落地后仍觉自报空间大，再回头做 B 的"自动捕获"（届时评估是否并入 C 实现）。

**组合结论（2026-09-09 用户裁决收口 = accepted 决策）**：采纳 **A + C 组合**——A 根治缺口 1（触发依赖），C 最接近根治缺口 2（表演性决策），组合覆盖两个缺口；**B 排除暂缓**（C 落地后重评）。实施符合 ADR-0010：A 失效条件已命中（P-021/022/023 三连批应走未走，90 日窗口，E1 实证）→ A 为下一候选实施批（待用户独立指令）；C 待 A 落地后触发。

**触发条件登记**：
- **A 的触发** = 失效条件命中（step-gate 连续 3 个应走管线批次无 decision；时间窗 90 日内防长期停顿误触发）或用户裁决
- **C 的触发** = A 落地后或用户裁决
- **B 的触发** = C 落地后仍发现自报表演空间（届时评估并入 C 或独立实施）
- **"应走管线"判定准则**（补 P2-3 漏洞）：**适用于 step-gate 实现后（P-020 起）的新批次**（早于实现的历史批次不追溯）。① PROGRESS 登记新 P 编号；② 关联产出含 RESEARCH/DESIGN/IMPL/CHECKLIST 文档之一；③ 满足任一即视为"应走管线"。**E1 实测四批**：P-020 走（首例，p020 两 session 4+5 条 decision）/ P-021 应走未走（桥落地，无 session）/ P-022 应走未走（缺陷修复，无 session）/ P-023 应走未走（概念登记，无 session）——**4 应走批次仅 1 走 3 未走，值守失效为系统性**，强化出路 A（流程强制）必要性

## 考虑的替代方案（Alternatives Considered）

### 方案 A：维持现状（step-gate 保持值守命令）（否决）

- 优点：零改动
- 缺点：P-023 已实证失效模式——下个同类批次（低决策密度纯登记型）大概率再次缺席；「强制决策」承诺与事实不符
- 否决理由：诊断已确认，维持现状 = 明知失效仍保留虚假承诺

### 方案 B：文档层加强纪律（AGENTS.md 加「每步必须调用 step-gate」）（否决）

- 优点：成本最低
- 缺点：与诊断二同源——**advisory 约束不可信**（社区 StepProof 明确「instructions are advisory. I can read it and ignore it」）；本仓 DEV-LOG 三重要求靠 review 臂持续看守的教训同构
- 否决理由：软约束等价回到口头纪律，失效模式不改变

### 方案 C：登记演进候选，触发驱动不实施（选择）

- 描述：如决策节——诊断确认 + 出路 A/B/C 三问预演登记为候选
- 优点：① 诊断事实留档（下一批次的审查输入）；② 演进方向有据（避免下次重新口头论证）；③ 符合 ADR-0010 懒加载纪律（不因"可能有用"而实现）；④ 社区映射为未来裁决提供已验证参照
- 缺点：管线仍值守，下个批次可能再次缺席——由失效条件监控（见验证节）
- 选择理由：与既有「触发驱动不排队」「Layer-0 优先于 Layer-1」惯例一致；本仓是方法论文档仓，不因单个缺陷立即膨胀

## 后果（Consequences）

### 正面

- P-020 后三连批（P-021/P-022/P-023）决策链缺失的根因（触发依赖 + 表演性决策软肋）成为显式登记的诊断，后续批次审查有据可依
- 社区三出路映射完毕，未来裁决（用户裁决 / 失效条件触发）可直接引用已验证参照，避免重复调研
- 演进方向登记符合 ADR-0010：不实现即零副作用，本仓不膨胀

### 负面

- step-gate「强制每步决策」的承诺与事实仍有差距（值守状态），需失效条件监控兜底
- 若未来实现出路 A/B/C，spec_runner 改动幅度未知（Layer-1 演进成本待实施时评估）

### 中性 / 后续行动

- P-023 决策链缺失可登记 M7 样本 / DEV-LOG（本 ADR 不代行，待用户指令或独立 pass 捕获）
- step-gate DESIGN 可考虑补「触发依赖」note（v1.1 候选项，本 ADR 不强制）
- docs/adr/README.md 索引 + ADR-0007 附录 A 补登本 ADR

## 验证（Validation）

### 已有实证

| 依据 | 取证方式 | 等级 | 状态 |
|------|---------|------|------|
| P-021/P-022/P-023 事件流缺失（各 0 session / 0 decision） | `ls tools/spec_runner/sessions/` + decision 计数——仅 p020 系列两 session 含 decision（4+5 条），余 7 文件全 0 | E1（机械枚举） | ✅ |
| step-gate 实现存在但值守（EVENTS + cmd_gate_step + parser + selftest F20-F23） | `grep spec_runner.py`——L30-31/L184-238/L443-447/L619-648 | E1 | ✅ |
| step-gate DESIGN 触发驱动声明（§6.3 不加入默认 gate hook 链） | step-gate DESIGN 原文核对 | E1 | ✅ |
| FWK-DECISION-RECORD「不是验证机制」（I-4）+ 契约管结构不管对错 | 契约 §0/§4 原文核对 | E1 | ✅ |
| 社区方案存在性与机制 | 2026-09-09 WebSearch 4 轮取证（URL 见 CER 候选表 / 各源主页） | E4（判断类，人工甄别） | ✅ |

### 验收条件（approved 后）

- docs/adr/README.md 索引出现 ADR-0011
- ADR-0007 附录 A 补登 ADR-0011 行
- CODE_WIKI declared.adr_files 7→8 + 版本头 v1.24
- 诊断结论被下一批次审查引用（或用户裁决演进方向）

### 失效条件（何时重审）

- **step-gate 连续 3 个应走管线的批次未产生 decision 事件**（含纯登记型；时间窗 90 日内；判定准则见 §三出路 P2-3 补）→ 触发出路 A 重审（流程强制是否落地）
- 用户对 P-023 决策链缺失作出裁决（如「补建事件流」/「登记 M7 样本」）→ 本 ADR 追记
- 任何出路（A/B/C）获准实施 → 本 ADR 升 accepted 并追加实施追记

### 失效条件重审记录

| # | 日期 | 触发事实 | 结论 | 依据 |
|---|------|---------|------|------|
| — | 2026-09-09 | 初始登记（proposed） | 待确认 | P-023 排查 + 社区检索 |
| 1 | 2026-09-09 | 用户裁决「决策为 A + C 组合收口」；**失效条件命中**（P-021/022/023 三连批应走未走，90 日窗口，E1 实证 + 样本㉚） | **accepted（2026-09-09）**；A 实施待独立指令、C 待 A 落地 | 用户裁决 + sessions E1 取证 |

## 修订历史

| 日期 | 变更 |
|------|------|
| 2026-09-09 | 初始版本（proposed）：P-023 事件流缺失排查 → 诊断一（触发依赖：值守机制非强制，DESIGN §3.1 生成端自写 + §6.3 触发驱动）+ 诊断二（表演性决策软肋：证据自报抗不住表演，契约 I-4「非验证机制」）+ 社区 4 轮检索映射（缺口 1 流程强制 / 缺口 2 证据客观化五方案 + confessions 兜底）→ 决策 = 确认诊断 + 出路 A/B/C 三问预演登记不实施；方案 A/B 否决；验证表 E1 实证 |
| 2026-09-09 | 增补"三出路优先级与成本收益"节（用户指令「补进 ADR-0011」）：三出路解决层面辨析（A 存在性 / B 证据可信 / C 审查信谁）+ 成本收益表 + **优先级裁决 A → C → B**（A 低垂果实消除缺席 / C 复用既有独立 pass 形态根治表演 / B 暂缓或并入 C——文档仓"机械可核锚点"定义模糊且与 C 重叠）+ 组合结论（A+C 覆盖两缺口，B 可选增强）+ 触发条件登记。版本 v1.0 → v1.1 |
| 2026-09-09 | 复核修复（用户指令「复核上一轮结果 执行修复」，E1 机械取证）：**发现 P1 事实错误**——上轮例证「P-021 走 / P-022 走」与实测不符（sessions 仅 p020 系列两文件含 decision = 4+5 条，P-021/P-022/P-023 均无 session）→ 真实实证 = **4 应走批次仅 1 走 3 未走**（值守失效为系统性，强化出路 A）；修正六处（L30 精确化「仅 p020 系列」/ L41 结论改三连批 / L75 诊断确认改三连批根因 / L115 例证重写 + 判定准则适用限定「P-020 起新批次，历史不追溯」/ L142 后果改三连批 / L163 E1 枚举补全 P-021/022）+ 补「机械可核」定义（P3-2 残留，L77）。版本 v1.2 → v1.3 |
| 2026-09-09 | **用户裁决收口（用户指令「ADR-0011 决策为A + C 组合收口」）**：决策 = **A + C 组合**（A 流程强制根治缺口 1 触发依赖 + C 独立验证根治缺口 2 表演性决策；B 排除暂缓）；**proposed → accepted**；**失效条件命中登记**（P-021/022/023 三连批应走未走，90 日窗口，E1 实证 + 样本㉚）→ A 为下一候选实施批待用户独立指令、C 待 A 落地后触发；原「登记不实施」废止为「决策收口 + 触发驱动实施」；docs/adr/README + ADR-0007 附录 A + CODE_WIKI 状态同步。版本 v1.3 → v1.4 |
| 2026-09-09 | **P-024 实施追记（用户指令「开启后续吃狗粮spec工作流」）**：出路 A 落地 = pre-commit **第四 hook `step-enforce`**（files 收窄 spec/ 四文档）+ **spec_runner.py v1.3.0**（`step-enforce --pid` 前缀定位 specwf-p0xx-* session + 复用 cmd_gate_step；selftest 31/31 = 28 + F27-F29）+ `scripts/step_enforce.py`（feature→P 映射，缺位 exit 2）；**批次级强制**（存在 + decision 非空）+ **只读零副作用**（P-022 教训）；**吃狗粮自证** = P-024 session 过 step-enforce exit 0；三通道全绿。**C 待 A 落地后触发**（下一候选，用户裁决或后续批次暴露表演空间时）。版本 v1.4 → v1.5 |
| 2026-09-09 | **P-025 实施追记（用户指令「按照吃狗粮执行出路 C」）**：出路 C 落地 = spec_runner **v1.4.0**（`verify-anchor --session` 子命令——decision 锚点真实性机械核查：文件存在 + 章节标题**精确匹配**（标题首 token 去尾点，`4.` 命中 §4 不命中 4.1）+ 行号上界，URL soft exit 2；selftest **38/38** = 31 + F30-F36）+ **SPEC_PROCESS RULE-1 补独立 pass 取证清单**（审查输入 = 事件流 + verify-anchor + git 状态；纯登记型无 diff 合法；只验位置可达不验断言对错）；吃狗粮自证 = P-025 session 决策链 3 步过 step-gate exit 0 + 自身锚点 3 条过 verify-anchor exit 0；历史 session 取证（p020 v2 6 锚点含行号 / p023 2 / p024 1）全真实；三通道全绿；**B 仍暂缓**（C 落地后重评——后续批次暴露自报空间时评估）。版本 v1.5 → v1.6 |
| 2026-09-09 | **P-027 盲区修复追记（用户指令「登记并修复 step-enforce 的盲区」）**：出路 A 实施物（step-enforce hook）暴露**覆盖盲区**——v1.0 files 正则仅收四文档精确名，不匹配 P-003 前遗留前缀命名（COMMUNITY_ECOSYSTEM_RESEARCH.md / STEP_GATE_CHECKLIST.md）→ **P-026 批次实际未被 hook 门禁强制**（手动吃狗粮掩盖）→ **M7 样本 ㉛ 入账**（1 P2，形态 II = 0 不入分桶）；修复 = FEATURE_RE/files 扩展 `[A-Z0-9_]+_` 前缀四文档 + **历史批次豁免（P-020 前不追溯）**（新纳入 15 feature 中 13 个为 P-020 前批次豁免，step-gate P-020 / community-ecosystem P-026 纳入强制且均有 session）；step-gate-enforcement DESIGN v1.0→v1.1 追记；三通道全绿 + 五场景验收；**A+C 两路闭环后新增机制自身盲区已修复**——B 仍暂缓。版本 v1.6 → v1.7 |
