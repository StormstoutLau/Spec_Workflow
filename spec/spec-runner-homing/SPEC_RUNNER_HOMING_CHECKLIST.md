# 审查验收 Checklist：Spec_Runner 归巢实施批（P-019 spec-runner-homing）v1.0 (2026-09-08)

---
id: spec-runner-homing-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-08
depends: [spec-runner-homing-DESIGN, spec-runner-homing-IMPLEMENTATION]
upstream: null
---

> **Feature**: spec-runner-homing（PROGRESS P-019 实施批——Spec_Runner 并入本仓验收）
> **基于实施**: [SPEC_RUNNER_HOMING_IMPLEMENTATION.md](./SPEC_RUNNER_HOMING_IMPLEMENTATION.md) v1.0（verified）
> **对照设计**: [SPEC_RUNNER_HOMING_DESIGN.md](./SPEC_RUNNER_HOMING_DESIGN.md) v1.0（§3 验收标准 C1-C7）

## 1. 验收核对表

| # | 验收项 | 判定 | 证据 |
|---|--------|------|------|
| C1 | 8 文件完整落入 `tools/spec_runner/` | ☒ 通过 | hash 逐字节核对全 OK（IMPL §1 Step1） |
| C2 | spec_runner.py 逻辑零改动 | ☒ 通过 | 原样复制 + hash 一致（IMPL §1） |
| C3 | selftest 21/21（新路径自洽） | ☒ 通过 | `python tools/spec_runner/spec_runner.py selftest` exit 0（IMPL Step4） |
| C4 | 本仓三校验器 + repo_stats 全绿 | ☒ 通过 | dc_validator 68 文件 0 违规 / m7_stats 0 违规 / repo_stats 0 违规（P3 存量提示） |
| C5 | 上游修订注三处落地 | ☒ 通过 | LANGGRAPH §6 / SPEC_RUNNER_DESIGN D1 / IMPL 头部（IMPL Step3） |
| C6 | 事件流指针改写 | ☒ 通过 | 活动指针改写完毕；历史叙事保留（语义甄别原则，IMPL Step2） |
| C7 | 零新增 M7 样本 | ☒ 通过 | m7_stats verify 0 新增（并入 = 纯部署变更，零发现） |

**验收统计**: 7/7 通过，0 失败。验收维度：

| 维度 | 覆盖 | 说明 |
|------|------|------|
| 功能性 | C3 + gate 入流 + replay + dry-run | 新路径真实运行验证四件 |
| 一致性 | C1/C2 hash + C5 修订注 | 搬移完整性 + 上游裁决可追溯 |
| 对账性 | C4 三通道 | 工具边界内机械验证全绿 |
| 边界声明 | C6 语义甄别 | 活动/历史指针分清——历史不改写 |

## 2. 独立 pass 状态

**待触发**——同 P-009/P-010/P-014 收口先例（独立 pass 需 RULE-1 时序独立 / RULE-5 异基座，挂后续裁决）。

## 3. 签名

- 实施端：main agent（本批实施 + 自查）——2026-09-08
- 审查端：`自查（单视角）`（RULE-4），独立 pass 待触发
- 决定：**有条件通过**（7/7 绿色）——独立 pass 触发后若有修订按双目录各自版本化（tools/ 代码 + spec/ 文档）