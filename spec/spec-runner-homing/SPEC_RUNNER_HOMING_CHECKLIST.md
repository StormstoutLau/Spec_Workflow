# 审查验收 Checklist：Spec_Runner 归巢实施批（P-019 spec-runner-homing）v1.0 (2026-09-08)

---
id: spec-runner-homing-CHECKLIST
type: design
version: 1.1
status: accepted
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
| C4 | 本仓三校验器 + repo_stats 全绿 | ☒ 通过 | dc_validator **70 文件** 0 违规 / m7_stats 0 违规（P3 提示 1） / repo_stats 0 违规（P3 提示 6 门面快照滞后）——文件数 68→70 系实施批期间新增 spec-runner-homing 四件合理增长 |
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

## 2. 独立 pass 结果（v1.1，2026-09-08）

**触发**: 用户指令「执行 CHECKLIST 独立 pass」
**审查视角**: 验证者模式——不接受上一轮执行者结论，独立运行全部机械验证 + 逐项证据核对（RULE-1 时序独立 / RULE-5 异构基座）

### 2.1 机械通道（独立运行，非复述）

| 通道 | 命令 | 结果 | 与 IMPL 记录差异 |
|------|------|------|-----------------|
| selftest | `python tools/spec_runner/spec_runner.py selftest` | **21/21 passed** exit 0 | 无 |
| dc_validator | `python scripts/dc_validator.py` | **70 文件，0 违规** | ⚠️ 文件数 68→70，新增 = 实施批期间 spec-runner-homing 四件文档（合理增长，不影响违规判定） |
| m7_stats | `python scripts/m7_stats.py` | **0 违规**（P3 提示 1） | 无 |
| repo_stats | `python scripts/repo_stats.py` | **0 违规**（P3 提示 6：门面快照滞后 as_of=2026-08-23） | 无 |
| spec_runner.py hash 对比 | 外仓 vs 本仓 SHA-256 | **5C05E1DE... 一致** | 零改动确认，与 IMPL C2 一致 |
| git diff HEAD~2..HEAD -- M7_EVIDENCE_LOG | M7 账本变动 | **空输出 = 零新增样本** | 与 C7 一致 |
| git status --porcelain | 工作区状态 | **干净** | 确认无未提交变更污染验证 |

### 2.2 逐项独立判定

| # | 独立 pass 判定 | 关键证据 |
|---|---------------|---------|
| C1 | ✅ 通过 | 目录清单 10 项（8 原始 + 1 实施验证 session + README），与 IMPL §1 表列一致；文件 size 全部匹配 |
| C2 | ✅ 通过 | spec_runner.py SHA-256 = `5C05E1DE4CA59BE6DD696C742DBC006130A7CECB256139B33882C33B1A26B889`，外仓与本仓完全一致 |
| C3 | ✅ 通过 | selftest 21/21 全 PASS，F1-F19 覆盖 gate 入流、replay、fork、异常路径、schema 校验 |
| C4 | ✅ 通过 | 三通道 0 违规；dc_validator 文件数 70（68→70 合理增长）；repo_stats P3 提示为历史存量 |
| C5 | ✅ 通过 | 三处 grep 独立命中：LANGGRAPH §6 / SPEC_RUNNER_DESIGN D1 / SPEC_RUNNER_IMPLEMENTATION 头部 |
| C6 | ✅ 通过 | PROGRESS P-017 历史记录保留 "F:\Spec_Runner 仓" 原叙述；P-019 条目已改 tools/spec_runner/；M7_EVIDENCE_LOG 零改动 |
| C7 | ✅ 通过 | git diff M7_EVIDENCE_LOG 空；m7_stats 零违规；P-019 纯部署变更零发现 |

### 2.3 发现与观察

| 级 | 项目 | 说明 |
|----|------|------|
| P3 | dc_validator 文件数漂移 | IMPL Step4 记录 68，独立 pass 跑出 70。原因 = 实施批期间 spec-runner-homing 四件文档写入 git，属于正常 spec 管道增长。但暴露一个记账问题：**IMPL 中的数字是快照还是最终值**——若为快照应标注时间，否则应更新。当前不影响本批验收。 |
| P3 | P-020 候选 | IMPL §4 已登记 spec_runner.py L109-111 gate 自动提交 cwd 问题（归巢后可能误提交主仓），建议独立修复批。独立 pass 确认此问题存在但不影响本批验收（deployment-only 原则）。 |

## 3. 签名

- 实施端：main agent（本批实施 + 自查）——2026-09-08
- 审查端：main agent 独立 pass（验证者视角，机械通道独立运行 + 逐项证据核对）——2026-09-08
- 决定：**通过**（7/7 绿色，独立 pass 与实施端结论一致；P3 观察项不阻塞验收，按 IMPL §4 遗留处理）
- 后续动作：push 到远程；P-020 修复 gate 自动提交 cwd 问题；门面快照刷新随下次收口批处理