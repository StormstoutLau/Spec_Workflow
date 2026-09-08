# 实施文档：Spec_Runner 归巢实施批（P-019 spec-runner-homing）v1.0 (2026-09-08)

---
id: spec-runner-homing-IMPLEMENTATION
type: design
version: 1.0
status: verified
date: 2026-09-08
depends: [spec-runner-homing-DESIGN, spec-runner-homing-RESEARCH]
upstream: null
---

> **Feature**: spec-runner-homing（PROGRESS P-019 实施批——RESEARCH v1.1 C1 改判采纳并入 → DESIGN v1.0 → 用户指令「好的，进入实施批」触发）
> **实施日期**: 2026-09-08
> **对照设计**: [SPEC_RUNNER_HOMING_DESIGN.md](./SPEC_RUNNER_HOMING_DESIGN.md) v1.0（D1-D4 + §3 验收标准 C1-C7 + §5 五步规格）

---

## 1. 实施记录（依 DESIGN §5 五步）

### Step 1：代码聚合平移（DESIGN D1 落点 = `tools/spec_runner/`）

外仓 `F:\Spec_Runner` 8 文件全量复制至本仓 `tools/spec_runner/`：

| 文件 | 源大小 | 目标 | hash 核对 |
|------|--------|------|-----------|
| spec_runner.py | 22,638 B | tools/spec_runner/spec_runner.py | ✅ 一致 |
| README.md | 5,680 B | tools/spec_runner/README.md（P-019 归巢注改写） | ✅ 一致 |
| sessions/myproj-probe-20260907.jsonl | 398 B | tools/spec_runner/sessions/ | ✅ 一致 |
| sessions/p009-first-run-001-fork-demo.jsonl | 3,142 B | 同上 | ✅ 一致 |
| sessions/p009-first-run-001.jsonl | 5,878 B | 同上 | ✅ 一致 |
| sessions/specwf-probe-20260907.jsonl | 400 B | 同上 | ✅ 一致 |
| templates/spec_runner_adapter.py | 8,901 B | tools/spec_runner/templates/ | ✅ 一致 |
| templates/examples/spec_workflow_adapter.py | 11,306 B | tools/spec_runner/templates/examples/（RUNNER 路径改写） | ✅ 一致 |

（C1 达成：8 文件 hash 逐字节核对，命令 = PowerShell `Get-FileHash` 源/目标比对，全 OK）

### Step 2：指针改写（活动指针；历史叙事保留——语义甄别原则）

| 位点 | 类型 | 处理 |
|------|------|------|
| tools/spec_runner/README.md 头部 | 活动文档 | P-019 归巢注 + 设计规格相对路径化 + sessions 落点说明 |
| tools/spec_runner/README.md「约束」节 | 活动文档 | 「双向零依赖」→「契约零耦合 + sessions 随仓版本化」 |
| tools/spec_runner/templates/examples/spec_workflow_adapter.py 配置区 | 活动代码 | `RUNNER = r"F:\Spec_Workflow\tools\spec_runner\spec_runner.py"` |
| PROGRESS/CODE_WIKI 版本头中 `Spec_Runner:sessions/...` | **历史叙事** | **不动**（P-009/P-017 事件时点的真实记录；改写即篡改历史——同 P-003 改名操作元描述命中的语义甄别规则） |
| M7 账本 | — | 无事件流指针（来源列用 commit 路径），零改动 |

（C6 达成：活动指针改写完毕；历史叙事保留——C6 判定标准按语义甄别执行，非机械 grep 归零）

### Step 3：上游裁决修订（DESIGN D3 版本化修订注形态）

| 文档 | 修订 |
|------|------|
| LANGGRAPH_UPGRADE_RESEARCH.md §6 | 追加 P-019 修订注（独立仓库子句修订；主判断其余保留） |
| SPEC_RUNNER_DESIGN.md D1 | 「独立仓库」裁决表追加修订注（`✅➡️`；scripts/ 候选注亦更新） |
| SPEC_RUNNER_IMPLEMENTATION.md 头部 | 追加 P-019 归巢追记（commit 锚退役，新路径复测通过） |

（C5 达成：三处修订注落地）

### Step 4：验证（C3/C4/C7）

| 验证 | 结果 |
|------|------|
| `python tools/spec_runner/spec_runner.py selftest` | **21/21 passed**（新路径 ROOT 派生自洽） |
| gate 真实入流 `p019-homing-verify-1` | verdict=pass exit=0，事件落 `tools/spec_runner/sessions/p019-homing-verify-1.jsonl` |
| `replay --session p019-homing-verify-1` | 1 rows OK（seq 单调 + schema 可解析） |
| adapter dry-run gate dc-validator | 命令装配正确（新 RUNNER + 四门禁） |
| dc_validator --check-all | 68 文件 0 违规 |
| m7_stats | 0 违规（P3 提示 1，存量非本批引入） |
| repo_stats | 0 违规（P3 门面快照滞后为历史存量 as_of=2026-08-23） |

（C3/C4/C7 达成；C2 = spec_runner.py 源码零改动——复制原样 + hash 一致）

## 2. 交付物清单

| 交付物 | 位置 | 状态 |
|--------|------|------|
| runner 执行器 | `tools/spec_runner/spec_runner.py` | ✅ v1.0.0（原样搬移） |
| runner README | `tools/spec_runner/README.md` | ✅ v1.0（P-019 归巢注） |
| 事件流证据 ×4 + 新增验证流 ×1 | `tools/spec_runner/sessions/` | ✅ 随仓版本化 |
| 接入模板 ×2 | `tools/spec_runner/templates/` + `examples/` | ✅ 配置区改写 |
| 实施批四件套（本批） | `spec/spec-runner-homing/` | RESEARCH v1.1 + DESIGN v1.0 + 本文件 + CHECKLIST v1.0 |

## 3. 外仓冻结声明

`F:\Spec_Runner` 保留为历史存档（git 历史 5 commit 完整：4ea703d→71c7ae6），**不再作为活跃代码仓**。回滚基线：若 `tools/spec_runner/` 方案后续出现问题，外仓 hash 一致可随时恢复工作副本。

## 4. 遗留与观察项

- **归巢后暴露的行为缺陷（发现于本批实施验证）**: spec_runner.py L109-111 的 gate 自动提交逻辑（写流后 `git add -A sessions && git commit`）在外仓语境正确（sessions 在自己仓根），归巢后其 cwd=ROOT 指向 `tools/spec_runner/`，但 git 仓根上溯到 `F:\Spec_Workflow`——**在验证 gate 时触发了两次独立自动 commit（0b64e3b/d779902），把 sessions/ 混入主仓历史且早于 code 文件提交**（历史破碎）。处置：`git reset --soft e0b71c1` 撤销后与 code 统一提交（本批已执行）。**修复候选（挂后续 P-020 或独立小流程）**：runner 自动提交范围限定 `tools/spec_runner/sessions/`（相对本仓根），或改用 `--cwd` 限定 + 前置校验仓根。本批不扩大范围（deployment-only 原则），仅登记。
- P3 门面快照滞后（README/en/evidence.svg，as_of=2026-08-23）：历史存量，随下一次 P-019/P-020 收口批择机刷新（本批不扩大范围）
- spec-runner 四件套（SPEC_RUNNER_*）与 tools/ 的职责分界：设计文档仍在 `spec/spec-runner/`（P-009 治理轨道），代码在 `tools/spec_runner/`——与 DESIGN D1「两类可执行件分属两仓」修订为「分属两目录」一致