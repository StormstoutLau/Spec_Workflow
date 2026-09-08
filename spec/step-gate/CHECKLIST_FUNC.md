# 验收清单：step-gate 决策产物管线（P-020 实施批）

---
id: step-gate-CHECKLIST-FUNC
type: design
version: 1.0
status: draft
date: 2026-09-08
depends: [step-gate-DESIGN, step-gate-CHECKLIST, FWK-DECISION-RECORD, spec-runner-DESIGN]
upstream: null
---

> **Feature**: step-gate 实施批（P-020）
> **前提**: 三问门禁 8/8 通过（[STEP_GATE_CHECKLIST.md](./STEP_GATE_CHECKLIST.md) §2.1，P-020 获准立项）
> **流程裁剪注**: IMPLEMENTATION 文档裁剪（同 P-016 D3 先例）——实现 = spec_runner.py 单文件局部扩展（EVENTS + 1 函数 + parser 子命令 + selftest fixture）+ README 命令面，无部署/无配置面，机械验证由 selftest 承载

---

## 1. 文档一致性验收

- [x] **D-1**：实现与 DESIGN §4（schema 八字段）/§5（step 序表）/§6（三类规则 exit 分级）一致
- [x] **D-2**：P-020 CHECKLIST（门禁）→ DESIGN → 本 CHECKLIST 链路闭合

## 2. 功能验收（对照 DESIGN §4-§6）

- [x] **F-1**：`EVENTS` 含 `"decision"`；`EventWriter._validate` 接受该事件（source ∈ SOURCES）
- [x] **F-2**：`STEP_SEQUENCE = (research, design, implement, verify, finalize)` 落位
- [x] **F-3**：`cmd_gate_step` 只读不写流（无 append/fork 调用）；三类规则齐全（schema 硬性 / 秩序硬性 / 锚点软性）
- [x] **F-4**：硬性-1：八字段必填 + metadata.step_id/step_seq + evidence 非空 → exit 1
- [x] **F-5**：硬性-2：step_id 非法 / step_seq 位错 / 重复 → exit 1；`--expect` 全链不一致 → exit 1
- [x] **F-6**：软性-3：锚点形态（`path#Lx` / `path §N` / URL）正则校验 → exit 2
- [x] **F-7**：空流无 decision → exit 1
- [x] **F-8**：parser 子命令 `step-gate --session --expect` 装配正确

## 3. 机械验证

- [x] **T-1**：`selftest` = **26/26**（原 21 项 F1-F19 全过 = 回归零破坏 + 新增 F20-F24 = 5 项 step-gate 覆盖）
- [x] **T-2**：F21 完整链 --expect 一致 → exit 0；F22 缺字段 → 1；F23 锚点存疑 → 2；F24 非法 step_id → 1；F20 空流 → 1
- [x] **T-3**：**吃狗粮运行实证**（Q2b E2）——`specwf-p020-20260908v2` session 四步 decision 链（research/design/implement/verify）`step-gate --expect ...` → **exit 0**；首版 `§selftest` 锚点被软性校验真实捕获（exit 2 → 修正行号锚点）

## 4. Q3c 工具链零变化复验（激活前后对比）

| 校验器 | 激活前基线 | 激活后 | 判定 |
|--------|-----------|--------|------|
| dc_validator | 75 文件 0 违规 | 77 文件 0 违规（+2 为本次新增设计文档，非工具行为变化） | ✅ |
| m7_stats | 0 违规 | 0 违规 | ✅ |
| repo_stats | 0 违规 | 0 违规 | ✅ |

## 5. ADD 审计（Phase 0 质量门）

| 不变式 | 状态 | 证据 |
|--------|------|------|
| I-1 复用不新建 | ✅ | decision 事件 input = FWK-DECISION-RECORD 八字段；无顶层新结构（run_selftest/read 均未改） |
| I-2 append-only | ✅ | cmd_gate_step 无任何写路径；`--expect` 只读 |
| I-3 单向依赖 | ✅ | 实施未新增契约→runner 引用（grep 复验） |
| I-4 零激活副作用 | ✅（T-1 复验：selftest 26/26，F1-F19 回归零破坏） | 未调用 step-gate 时 26 项 selftest 中 F1-F19 = 原 21 项逐字节行为不变（回归通过） |

## 6. 验收统计与决定

| 项 | 值 |
|----|-----|
| 功能/一致性项 | 12/12（D×2 + F×8 + T×3） |
| selftest | 26/26 |
| P1 项 | 0 |
| P2 项 | 0 |
| P3 观察 | 1（锚点正则可以更严——URL 允许任何 \S+；登记软性校验已兜底，不阻塞） |
| **验收决定** | ✅ 通过（自查）——待独立 pass 复核 |

**签字**: _________ 日期: _________

---

## 7. 独立 pass 记录（Step 8）

> 机械复核：selftest 26/26 独立重跑、三通道激活后复跑、decision 事件链独立重读。

- [x] selftest 26/26 重跑通过
- [x] 三通道激活后复跑全绿（Q3c 闭环）
- [x] 吃狗粮 session `specwf-p020-20260908v2` 事件流重读（4 条 decision 链）→ step-gate exit 0 复现
- [x] 独立 pass 结论：**通过（accepted）**

**签字**: _________ 日期: 2026-09-08

---

## 8. 修订历史

| 日期 | 变更 |
|------|------|
| 2026-09-08 | v1.0 创建——实施批验收清单（D×2 + F×8 + T×3 + Q3c 对比表 + ADD 审计） |
| 2026-09-08 | v1.0 → v1.1：状态 draft → accepting；I-4 补 T-1 复验实证（selftest 26/26 回归零破坏）；独立 pass 机械复核闭环（§7，2026-09-08 签字） |