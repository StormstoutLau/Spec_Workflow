# P-020 三问门禁验收检查清单：决策产物管线（step-gate）作为 ADR-0010 首例 v1.0 (2026-09-08)

---
id: step-gate-CHECKLIST
type: design
version: 1.0
status: pending
date: 2026-09-08
depends: [ADR-0010, community-ecosystem-RESEARCH, FWK-DECISION-RECORD, spec-runner-DESIGN]
upstream: null
---

> **Feature**: step-gate（PROGRESS P-020——决策产物管线：Spec_Runner 增 `decision` 事件类型 + `step-gate` 命令）
> **来源**: P-018 §3.5 裁定「可行且优先」+ ADR-0010 验收条件「首个候选吸收（P-020）完整走三问」（2026-09-08 accepted）
> **本清单职责**: **仅验收"三问门禁"**（ADR-0010 决策节）——P-020 以首例身份通过三问、获准从"登记候选"转入"正式立项"；不覆盖 P-020 自身实现验收（那属于 P-020 实施批的 DESIGN/IMPL/CHECKLIST）

---

## 1. 背景：本清单与 ADR-0010 的挂接

ADR-0010（accepted 2026-09-08）决策节确立**候选吸收三问门禁**：

> 1. **放哪层？** Layer-0（纯文档/文件）还是 Layer-1（工具/服务）？
> 2. **激活条件？** 什么触发它从"登记"变"实现"？无触发即不实现
> 3. **未激活副作用 = 0？** 不 import / 不启动 / 不扫描 / 文档层无感知

其验收条件明确：「**首个候选吸收（P-020）完整走三问**」。本清单将该验收条件实例化——每一步骤给出判定标准、机械可验证方法、证据锚点（E1-E4）。**三问通过 = P-020 获准立项；任一问不通过 = 否决或退回补材料。**

## 2. 三问门禁验收表（核心）

| # | 三问 | 判定标准（P-020 实例化） | 验证方法 | 证据等级 | 判定 |
|---|------|------------------------|---------|---------|------|
| Q1a | 放哪层：契约落位 | `decision` 事件 schema **复用 FWK-DECISION-RECORD 八字段**（Layer-0 既有契约，docs/DECISION_RECORD_CONTRACT.md）——不新建重复契约、不偏离字段语义；step 标识 (`metadata.step_id`) 与 evidence 锚点 (`metadata.evidence`) 走通用 metadata 通道（P-016 severity 同通道先例） | 对照文档字段逐一核 diff（新增 schema 即违规） | E1 | ☐ |
| Q1b | 放哪层：实现落位 | 校验逻辑 `step-gate` 落 **tools/spec_runner/**（Layer-1 工具，扩展既有 runner）；不落入 scripts/ 与 spec/ 文档层 | 文件树核验 + repo_stats 对账 | E1 | ☐ |
| Q1c | 放哪层：单向依赖 | Layer-0（FWK-DECISION-RECORD 契约）**不依赖** step-gate；step-gate 单向依赖契约（并依赖 FWK-ASSERTION 的 E1-E4 等级标注） | grep 契约文档对 runner 的引用 = 0 | E1 | ☐ |
| Q2a | 激活条件：显式声明 | P-020 激活触发器 = **独立 feature 裁决**（用户指令触发实施批）——未裁决 = 停留登记态，不排队 | PROGRESS P-020 行登记 + 状态词 | E1 | ☐ |
| Q2b | 激活条件：激活即全链 | 激活后产出完整决策事件链：DESIGN/IMPL/CHECKLIST 每步 = step_id 一条 decision 事件（十步流程映射，如 "research"/"design"/"review"） | step-gate 真实运行验证（首个 feature 全流程） | E2（运行） | ☐ |
| Q3a | 未激活零副作用：源码足迹 | 未激活时 spec_runner 无 step-gate 相关残留（无半实现命令、无幽灵 import、无默认激活校验） | grep "step-gate\|decision" 于 spec_runner.py = 0（或激活前核验） | E1 | ☐ |
| Q3b | 未激活零副作用：文档层 | 未激活时 spec/ 与 docs/ 无强制新增（FWK-DECISION-RECORD 为既有契约，零新增）；候选状态仅登记于 PROGRESS/CODE_WIKI 候选位点 | 候选位点 grep（登记态 ≠ 实现态） | E1 | ☐ |
| Q3c | 未激活零副作用：工具层 | 未激活时三校验器（dc_validator/m7_stats/repo_stats）+ 三 hook 行为零变化（step-gate 不是默认 hook 链成员，触发驱动） | 三通道验证前后对比 | E1 | ☐ |

**验收统计**: Q1 三子项 + Q2 二子项 + Q3 三子项 = 8 项。

## 3. 判定逻辑

| 三问 | 通过条件 | 不通过处置 |
|------|---------|-----------|
| Q1 放哪层 | Q1a/Q1b/Q1c 全过 | 契约重复 → 精简为复用；实现落错 → 改位；单向依赖破 → 重设计 |
| Q2 激活条件 | Q2a/Q2b 全过 | 触发器模糊 → 补声明；无全链映射 → 补 step 映射表 |
| Q3 零副作用 | Q3a/Q3b/Q3c 全过 | 源码残留 → 清理；文档强制 → 降级登记；工具链侵入 → 改设计（按 ADR-0010 方案 A 直接否决的先例） |

**整体判定**: 三问全过 → **P-020 获准立项**（proposed 状态 → 可进入实施批）；任一问否决 → 记录否决原因，P-020 退回候选池。

## 4. 与既有契约的核对约束

- FWK-DECISION-RECORD 八字段：category/scenario/reasoning/outcome/confidence/entities/decision_maker/metadata（+ valid_from/valid_until）——`decision` 事件不得自造脱离八字段的新结构
- I-1~I-4 不变式沿用：如触发方 A 导入，映射唯一权威 = 契约文档
- E1-E4 证据分级沿用 FWK-ASSERTION；step-gate 校验"evidence 非空 + 锚点可解析"为机械检查，E1-E4 等级标注由生成端负责（与现有 A 类断言纪律等价）
- 零依赖不变式（D6）：step-gate 实现 stdlib only，与 spec_runner 既有纪律一致（本批无需新增判断，P-020 实施批复核）

## 5. 验证（本清单自身的）

### 验收条件

- [ ] 三问 8 子项全部判定通过（本清单 §2）
- [ ] P-020 获准立项登记（PROGRESS P-020 行 pending → 实施批触发输入）
- [ ] community-ecosystem §4 候选表补 P-020「分层归属 = Layer-1（工具），契约 Layer-0」标注（ADR-0010 验收条件之二）
- [ ] 三通道（dc_validator/m7_stats/repo_stats）全绿

### 失效条件（何时重审本门禁）

- step-gate 实施中出现未预见依赖（契约层/工具层任一）→ 三问判定重跑
- 8 子项中任一判定在实施批被推翻 → 本清单升版本 + 追记原因（I-3 版本化纪律）

## 6. 签名

- 制定端：main agent（2026-09-08，依据 ADR-0010 decision 节 + P-018 §3.5）
- 裁决端：用户（P-020 立项裁决）
- 状态：pending（本清单制定完成，待执行三问判定）

## 7. 修订历史

| 日期 | 变更 |
|------|------|
| 2026-09-08 | v1.0 创建——三问门禁操作化为 8 子项验收表；判定逻辑 + 核对约束 + 验证节落档 |