# 调研文档：独立验证（出路 C——审查臂查系统真实状态）

---
id: independent-verify-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-09-09
depends: [ADR-0011, ADR-0010, step-gate-DESIGN, step-gate-enforcement-DESIGN, SPEC-PROCESS]
upstream: null
---

> **Feature**: 独立验证（P-025——ADR-0011 出路 C 实施，审查臂从「读事件流」→「查系统真实状态」）
> **创建日期**: 2026-09-09
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「按照吃狗粮执行出路 C」——ADR-0011 accepted A+C 决策的 C 部分（触发条件 = A 落地后或用户裁决，本批即用户裁决触发）

---

## 1. 调研目标

**核心问题**（基于 ADR-0011 出路 C 形态定义，实施前细化）:

1. 出路 C 的**可机械判定形态**是什么——「审查臂从读自报流 → 查系统真实状态」中，哪部分是**确定性程序可核**（E1 级），哪部分必须留给异基座审查臂判断？
2. decision 事件 `evidence.anchor`（自报锚点）的**真实性核查**如何机械化——文件存在性 / 章节标题匹配 / 行号有效性的判定准则与边界？
3. **纯登记型批次**（P-023 式零代码变更）的查证范围如何定义——审查臂对无 diff 批次查什么？

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| Grep/Read | 既有 session 锚点分布枚举（p020/p023/p024 三 session 12 条 decision） | `anchor` / `evidence` |
| Read | cmd_gate_step 锚点形态检查（ANCHOR_RE）与 FWK-DECISION-RECORD evidence 结构 | spec_runner.py L174-239 / 契约 §1 |
| Read | ADR-0011 出路 C 定义与成本收益（L78/L99） | 三出路表 + 成本收益分析 |
| Read | SPEC_PROCESS RULE-1/5（独立 pass 时序 + 异基座审查） | L137-165 |

### 2.2 调研范围

- **复用来源**: ADR-0011（出路 C 定义 + 社区映射）、step-gate DESIGN（decision schema + 锚点规则）、step-gate-enforcement DESIGN（出路 A 落地形态 = 本批参照）、SPEC_PROCESS（RULE-1/5 审查臂规则）
- **不做**: 新增外部 WebSearch（社区参照已在 ADR-0011 §4 取证完成：StepProof / PROVENANCE-GUARD / OPERA / agent-prov）——复用式调研，零新增外部断言纪律

## 3. 调研发现

### 3.1 锚点现状：形态已查、真实性零校验（机械缺口）

【E1】**step-gate 的软性-3 只查锚点「形态可解析」，不查「指向真实存在」**——`ANCHOR_RE`（spec_runner.py L177-181）仅正则匹配 `path#Lx` / `URL` / `spec/...§N` 形态，`cmd_gate_step`（L217-220）对形态不匹配才报 soft；**文件是否存在于仓库、§N 章节标题是否真实存在、Lxx 行号是否越界——零校验**。

【E1】12 条 decision 锚点全为 E1 自报（p020 系列 7 条 + p023 追溯 2 条 + p024 吃狗粮 3 条），形态分布：`spec/...md §N[.N]` 章节引用（9 条）+ `tools/...py#Lxx` / `docs/...md#Lxx` 行号引用（3 条）。

> **机械缺口确认**：锚点真实性 = 确定性程序可判（文件存在性 + 章节标题匹配 + 行号上界），完全满足 ADR-0011 L77「机械可核 = 可由确定性程序验证」定义——当前零校验 = 表演空间。生成端可填 `spec/不存在.md §9` 结构满格通过 step-gate。

### 3.2 审查臂现状：独立 pass = 文档产出审核，非决策链真实性

【E1】**RULE-1/5 的既有独立 pass 是「文档产出审核」**（SPEC_PROCESS L137-165）：时序独立勾选 + 异基座审查者。step-gate DESIGN §1 声称「下一轮审查以事件流为唯一输入」——但 ADR-0011 已实证：审查臂读的自报流**没有独立取证通道**，锚点真实性无法当场核验，审查臂只能选择「信」或「全文重读」——前者表演，后者成本爆炸。

### 3.3 纯登记型批次的查证范围（P-023 式）

【E1】P-023（drift-gate 概念登记）决策链 2 条（research/design），锚点指向 `spec/drift-gate/RESEARCH.md §3` 与 `DESIGN.md §4`——**零代码变更、零 git diff**。查证范围定义：此类批次审查臂应验证 ① 锚点指向文档存在且章节真实；② session 内容（scenario/outcome）与文档状态一致（如声称「RESEARCH v1.0」→ front-matter version 匹配）；③ 纯登记型无 diff 是**合法态**而非缺陷（区别于实施批）。

### 3.4 社区参照（复用 ADR-0011 §4 已取证映射）

| 方案 | 机制 | 本批可迁移点 |
|------|------|------------|
| StepProof | worker 声称完成 → verifier（异上下文/异激励）**独立查 git/db/真实状态** | 审查臂查系统真实状态（非自报）；verifier 与生成端分离 |
| PROVENANCE-GUARD | provenance 判定 tool call 是否被**可溯源证据支撑**，pre-execution 拦截 | 锚点 = 证据支撑点；pre-execution 拦截 = hook 位点（本批为 verify 命令，hook 化留触发驱动） |
| OPERA | 每次外部调用**自动生成签名收据**，不依赖 self-report | 锚点真实性 = 收据核查的文档仓等价物 |

## 4. 综合分析

### 4.1 关键发现总结

1. **机械可核面 = 锚点真实性**：文件存在（git 跟踪中）+ 章节标题匹配（§N 精确匹配 `^#{1,6} N`）/ 行号上界（#Lxx ≤ 总行数）——确定性程序判定，E1 级。URL 锚点（外部证据）本地不可核 → soft（人工）。【置信度: ★★★★★（源码直读 + 12 条锚点枚举实证）】
2. **审查臂输入重定义**：独立 pass 输入 = 事件流 + `verify-anchor` 取证结果 + git 状态——「读自报流 → 查系统真实状态」的机械支撑。【置信度: ★★★★★（ADR-0011 L78/L99 定义直读）】
3. **纯登记型查证范围**：文档存在 + 章节真实 + session 与文档状态一致（version 匹配）；无 diff 合法。【置信度: ★★★★☆（P-023 追溯登记为唯一先例）】
4. **边界（防过度工程）**：verify-anchor 验证「锚点指向位置真实存在且可达」，**不验证断言内容对错**（那是 E1 分级 + 异基座审查臂的职责）——机械层压缩表演空间，语义层仍靠 RULE-5。【置信度: ★★★★★（反幻觉框架层级纪律）】

### 4.2 技术 landscape

锚点真实性核查落在 spec_runner 只读命令（复用 ANCHOR_RE 解析 + cmd_gate_step 提取）；审查臂规则落 SPEC_PROCESS RULE-1 补充（独立 pass 取证清单）；git 状态对照为审查臂人工取证项（机械化留给未来，不膨胀）。

### 4.3 研究空白（登记级）

- 锚点「章节匹配的语义边界」：§3 是否应拒绝匹配 §3.5（精确 vs 前缀）——本批裁决**精确匹配**（§3 ≠ §3.5），防宽松匹配制造假阳性真实感
- 跨批锚点（引用其他批次文档）的时点有效性（如引用已删章节）——本批查「当前文件状态」，历史时点有效性留审查臂判断

## 5. 幻觉抑制审查（Step 2 Review）

### 5.1 文献验证

| 引用 | 验证方式 | 状态 |
|------|---------|------|
| ADR-0011 出路 C / 社区映射（StepProof/PROVENANCE-GUARD/OPERA） | ADR-0011 §4 已 4 轮 WebSearch 取证（本批复用，不重复取证） | ✅（复用） |
| RULE-1/5 独立 pass 定义 | SPEC_PROCESS 原文直读 | ✅ |

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| ANCHOR_RE 只查形态不查真实性 | spec_runner.py L177-181 + L217-220 直读 | ✅ 已验证 |
| 12 条 decision 锚点 E1 自报 | sessions/ 三文件 Grep 枚举 | ✅ 已验证 |
| 锚点两种形态（§N 章节 / #Lxx 行号） | p020/p023/p024 session 直读 | ✅ 已验证 |

### 5.3 待修正项

- 无（复用式调研，零新增外部断言）。

## 6. 对设计的输入

### 6.1 可用的技术方案

- **机械支撑**：spec_runner 新子命令 `verify-anchor`（只读）——复用 ANCHOR_RE 解析锚点，对每条 decision 的 evidence.anchor 做真实性核查：文件存在（git 跟踪或工作区）+ §N 章节标题精确匹配 / #Lxx 行号上界；URL → soft；exit 0/1/2。
- **审查臂规则**：SPEC_PROCESS RULE-1 补充独立 pass 取证清单——审查输入 = 事件流 + verify-anchor 输出 + git diff/status 对照；纯登记型批次查证范围显式化（文档存在 + 版本一致 + 无 diff 合法）。

### 6.2 关键约束

1. **只读零副作用**（P-022 教训）：verify-anchor 只读 sessions/ + 文件系统，不创建/修改/提交文件。
2. **判定全机械**：文件存在 / 章节精确匹配 / 行号上界，无启发式；§3 精确匹配不命中 §3.5。
3. **兼容既有命令面**：verify-anchor 不影响 run/gate/status/replay/fork/step-gate/step-enforce（I-4 三通道对比实证）。
4. **不膨胀**：git 状态对照为审查臂人工取证（文档化），不机械化为命令（未来触发驱动候选）。
5. selftest 覆盖：真实锚点 pass / 文件不存在 fail / 章节不存在 fail / 行号越界 fail / URL soft / §3 不命中 §3.5。

### 6.3 风险

- 历史 session（p020/p023/p024）锚点若存在不真实引用 → verify-anchor 首跑会暴露既有表演空间（真靶）——处置 = 取证后修正或登记（非本批预先假定）。
- verify-anchor 被误读为「断言内容验证器」——设计中显式声明：只验锚点位置可达，不验断言对错。

## 7. 参考文献

- ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md v1.5（出路 C 定义 + 社区映射 + 触发条件）
- spec/step-gate/DESIGN.md v1.0（decision schema + 锚点规则 + STEP_SEQUENCE）
- spec/step-gate-enforcement/DESIGN.md v1.0（出路 A 落地形态 = 本批参照）
- SPEC_PROCESS.md v1.4（RULE-1/5 独立 pass）
- docs/DECISION_RECORD_CONTRACT.md v1.1（evidence 结构）

---

**Review 签字**: _________ 日期: _________
