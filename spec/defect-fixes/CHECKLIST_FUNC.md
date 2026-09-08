# 验收清单：P-022 缺陷修复批实施（gate auto-commit A+B + DIS-008 规则化）

---
id: defect-fixes-CHECKLIST-FUNC
type: design
version: 1.0
status: draft
date: 2026-09-08
depends: [defect-fixes-DESIGN, spec-runner-DESIGN, ADR-0010, ADR-0009]
upstream: null
---

> **Feature**: P-022 缺陷修复批——用户裁决 D1 = A+B 修正后采纳 / D2 = 规则化 + 追记（2026-09-08）
> **前提**: DESIGN v1.1 subagent 审查完成（结论 = A+B 修正后采纳，无否决项）；DESIGN v1.2 定稿
> **流程裁剪注**: IMPLEMENTATION 文档裁剪（同 P-016/P-020 D3 先例）——实现 = spec_runner.py 局部扩展（git_snapshot 重写 + 常量 + selftest F25/F26）+ 文档四处；机械验证由 selftest + 三通道承载

---

## 1. 文档一致性验收

- [x] **D-1**：实现与 DESIGN §1.4（A+B 修正后采纳）一致——含审查修正项：① B 文件路径源自 `sessions_dir()`（非 ROOT 硬编码）② selftest 子进程 env 剥离 `SR_GIT_AUTOCOMMIT` ③ 激活路径 `--no-verify` 裁定
- [x] **D-2**：P-022 门禁链路闭合（方案落档 → subagent 审查 → 用户裁决 D1/D2 → 实施批）

## 2. 功能验收（对照 DESIGN §1.4 审查结论）

- [x] **F-1**：A 门控——`SR_GIT_AUTOCOMMIT != "1"` 时 `git_snapshot` 早退零副作用（F25 实证零提交）
- [x] **F-2**：B 范围——显式激活只提交 `sessions/<sid>.jsonl` 单文件，其他脏文件不捎带（F26 实证 real-002 不在提交内）
- [x] **F-3**：B cwd——git 根经 `git -C <sessions_dir> rev-parse --show-toplevel` 从会话目录派生；非 git 仓静默跳过（注释与行为一致）
- [x] **F-4**：commit 带 `--no-verify`；`git add` 失败则不 commit
- [x] **F-5**：selftest 子进程 env 剥离 `SR_GIT_AUTOCOMMIT`（审查修正项 ②，父环境不泄漏）
- [x] **F-6**：`VERSION = 1.2.0`；`git_snapshot` 签名 `(sid, message)`，gate/run 两个调用点全部传 sid

## 3. 机械验证

- [x] **T-1**：`selftest` = **28/28**（原 26 项 F1-F24 回归零破坏 + 新增 F25/F26 = 2 项 git_snapshot 覆盖）
- [x] **T-2**：三通道全绿（dc_validator 78 文件 / m7_stats / repo_stats 0 违规）

## 4. 文档同步验收

- [x] **W-1**：README 约束节补 `SR_GIT_AUTOCOMMIT` opt-in 说明（默认关 + 单文件 + --no-verify）
- [x] **W-2**：SPEC_RUNNER_DESIGN 四处修订（§2 目标(2)「+ git commit」/ mermaid / LOC 表 gate 行 / LOC 表 git 封装行）
- [x] **W-3**：AGENTS.md 禁止事项两条（同文件编辑严格串行 + batch 后全覆盖终验 grep）
- [x] **W-4**：DIS-008 追记（第 4/5 次复发逐字证据 + 规则化落地注）
- [x] **W-5**：DESIGN v1.2 定稿（用户裁决 D1/D2 决策记录 + 实施批记录 + 修订历史）

## 5. ADD 审计（Phase 0 质量门）

| 不变式 | 状态 | 证据 |
|--------|------|------|
| I-1 复用不新建 | ✅ | git_snapshot 扩展既有封装，无新模块/新依赖（stdlib only 维持） |
| I-2 append-only | ✅ | 事件流写路径未改；git_snapshot 只读文件系统（git add/commit 属既有快照语义） |
| I-3 单向依赖 | ✅ | 修复不新增契约→runner 引用（grep 复验） |
| I-4 零激活副作用 | ✅ | 默认关（F25 实证）——未设 SR_GIT_AUTOCOMMIT 时 gate/run/selftest 全链路零 git 写操作 |

## 6. 验收统计与决定

| 项 | 值 |
|----|-----|
| 功能/一致性/文档项 | 13/13（D×2 + F×6 + T×2 + W×5） |
| selftest | 28/28 |
| P1 项 | 0 |
| P2 项 | 0 |
| **验收决定** | ✅ 通过（自查）——待独立 pass 复核 |

**签字**: _________ 日期: _________

---

## 7. 独立 pass 记录（Step 8）

> 机械复核：selftest 28/28 独立重跑、三通道激活后复跑、git_snapshot 四调用点 grep 现状核验。

- [x] selftest 28/28 重跑通过
- [x] 三通道激活后复跑全绿（dc 78 文件 / m7 0 / repo 0）
- [x] 独立 pass 结论：**通过（accepted）**

**签字**: _________ 日期: 2026-09-08

---

## 8. 修订历史

| 日期 | 变更 |
|------|------|
| 2026-09-08 | v1.0 创建——P-022 实施批验收清单（D×2 + F×6 + T×2 + W×5 + ADD 审计） |