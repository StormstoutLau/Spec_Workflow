# 调研文档：L2 CI 门禁（远程兜底强制）

---
id: ci-gate-RESEARCH
type: design
version: 1.1
status: draft
date: 2026-10-03
depends: [SPEC-PROCESS, ADR-0010, hook-surface-RESEARCH, rework-and-decision-paths-RESEARCH]
upstream: null
---

> **Feature**: L2 CI 门禁（远程兜底强制，P-070）
> **创建日期**: 2026-10-03
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「先实现 L2 CI 门禁」（承 [RESEARCH §3.9](../rework-and-decision-paths/RESEARCH.md) 四层强度阶梯：L0 广播零强制 / L1 本地 hook 可违反 / L2 CI 兜底 / L3 运行时阻塞式真正强制）。

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 5 | 本仓机械取证（E1）+ 本机复跑（E2） |
| B 推断类 | 3 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 3 | 不参与 R7 机械对账 |
| 假设区 | 2 | 未实测项；均已于 2026-10-03 实测回填（见附录 C） |

## 1. 调研目标

**Q**：本仓当前是否具备 L2（远程/CI）强制位点？若不具备，把 L1 的判据搬到远端需要哪些前置事实？

## 2. 调研方法

| 工具 | 用途 |
|------|------|
| Read / Glob（本仓） | E1 取证：hook 清单、检查器 CLI、平台与依赖面 |
| RunCommand（本机复跑） | E2 取证：五 hook 等价命令 + 内嵌自测的现时读数 |
| 对照对象 | [hook-surface §3.2](../hook-surface/RESEARCH.md) 的 L1 绕过实证（不重复检索） |

## 3. 调研发现

### 3.1 现状：本仓无任何 CI 位点

A-1 创建前本仓**不存在** `.github/workflows/`（无任何 CI 配置）；远端仅 = GitHub `main`；本地 pre-commit 五 hook 是**唯一**机械执行位点【E1】。

### 3.2 L1 的天花板：本地 hook 可被绕过

A-2 五 hook = `dc-validator` / `m7-stats` / `repo-stats` / `step-enforce` / `console-gen`，前者全为 `repo: local`（[.pre-commit-config.yaml](../../.pre-commit-config.yaml)）【E1】。
A-3 本地 hook 是**诚实护栏而非绝对强制**：git 官方明示 `--no-verify`；[hook-surface §3.2](../hook-surface/RESEARCH.md) 已登记 block-no-verify 实测 **12 种绕过向量全放行** ⇒ **任何本地 hook 都无法 100% 阻挡绕过**【E1/E3 引自本仓既有登记】。

⇒ 绕过本地 hook 即放行，是本批要堵的缺口。

### 3.3 检查面盘点：判据已齐、只差远端位点

A-4 五 hook 等价的 CLI 面**已齐备且全部只读 + stdlib**，本机复跑（2026-10-03，**批后读数**）全绿：`dc_validator --check-all`（**161** 文件 0 违规）/ `m7_stats`（0 违规）/ `repo_stats`（0 违规、P3 0）/ `console_gen --check`（与源一致）/ `step_enforce` 全量四文档（**94 文件 exit 0**）【E2】。

⇒ 无需新判据、无需新脚本，**只差一个远端触发位点**。

### 3.4 平台与版本前置

A-5 本机 = **Windows + Python 3.11.16**；`spec_runner` / `repo_stats` 等使用 PEP 604 注解（`Path | None`、`list[str] | None`）⇒ 需 **Python ≥ 3.10**【E1/E2】。

## 4. 综合分析

### 4.1 关键发现

1. **L2 的缺口是「位点」而非「判据」**：五 hook 的判据与 CLI 已全部可用且只读（A-4），缺的是远端触发。【置信度 ★★★★★】
2. **L2 强制力已由外部开关开启（2026-10-03 回填）**：GitHub 侧 branch protection 已启用——`required_status_checks.contexts = ["verify"]`（`strict=false`）+ `required_pull_request_reviews.required_approving_review_count = 0` + `enforce_admins = true` ⇒ **直推 main 被拒**、改动须经 PR 且 `verify` 绿方可合并。`approvals=0` 为**单人仓防自锁的必需取值**（GitHub 不允许 PR 作者自 approve，设 ≥1 则永远无法合并）。【置信度 ★★★★★，E2 实测】
3. **平台选择影响假红风险**：本仓重 Windows 特性（前例多处记录 Windows 特有陷阱），远端 runner 选同平台可降漂移；**回填**：首次远端运行（2026-10-03）暴露的**并非行尾差异**，而是 CI 日志管道下 stdout 默认 **cp1252** ⇒ 校验器打印中文即 `UnicodeEncodeError`，**在打印违规之前** exit 1（非违规、纯环境面）；修复 = job 级 `env: PYTHONUTF8=1 + PYTHONIOENCODING=utf-8` ⇒ 复跑全绿。【置信度 ★★★★★，E2】

### 4.2 结论与建议

【C】**判定 = 可实施且增量极小**：新增一个远端 workflow，把五 hook 等价命令 + 内嵌自测搬到 CI；**零新判据 / 零新脚本 / 零新依赖 / 零 API 破坏**。
【C】**触发面** = `push`（main）+ `pull_request` + `workflow_dispatch`。
【C】**明确不做**：不新增本地五 hook 未覆盖的判据（守「只搬不扩」）；不把只读诊断器（`anchor-audit` / `backflow-audit` / `downstream_compliance`）接入 CI——它们检出即 exit 1，会把**信息性发现**变成 CI 红灯，与其「不接门禁」定位冲突。

## 5. 幻觉抑制审查（Step 2 Review）

- 全部 A 类为**本仓机械取证 + 本机复跑**；无外部检索断言（复用本仓既有 hook-surface 登记，不重复检索）。
- 已知局限（**已回填**）：H1（平台/行尾差异）与 H2（远端 required check 形态）于 2026-10-03 首次远端运行与保护态回读后**均实测**（见附录 C 回填注）；仍存局限 = **仅一次远端运行证据**，同类环境问题不排除再现。

## 6. 对设计的输入

- 设计落点 = **单个 workflow 文件**（[DESIGN](./DESIGN.md) §3）；
- 检查面 = **本地五 hook 的超集**（加内嵌自测），理由见 B-3；
- 平台 = `windows-latest` + Python `3.11`（对齐 A-5）；**实际首跑风险非行尾而是管道编码（cp1252），已修**（H1 回填，DR-1）；
- 边界 = 只在本仓触发，**不对消费仓产生强制**。

## 附录 A 断言登记（A 类，5 条）

【A】A-1 创建前本仓无 `.github/workflows/`（无 CI 位点）；远端仅 GitHub `main`；本地 pre-commit 五 hook 为唯一机械执行位点【E1】
【A】A-2 五 hook = `dc-validator` / `m7-stats` / `repo-stats` / `step-enforce` / `console-gen`，全为 `repo: local`【E1】
【A】A-3 本地 hook 可绕过：git 官方明示 `--no-verify`；hook-surface §3.2 已登记 block-no-verify 12 种绕过向量全放行【E1/E3 引自本仓登记】
【A】A-4 五 hook 等价 CLI 齐备且只读 stdlib；本机复跑全绿（dc **161** 文件 0 违规 / m7 0 / repo_stats 0 / console --check 与源一致 / step_enforce **94** 文件 exit 0；批后读数，批前为 157/90）【E2，2026-10-03】
【A】A-5 本机 Windows + Python 3.11.16；部分脚本用 PEP 604 注解 ⇒ 需 Python ≥ 3.10【E1/E2】

## 附录 B 机读登记（B 类，3 条）

```json
[
  {"id": "B1", "claim": "本地 hook 是 L1（可违反）、CI 是 L2（本地绕过不生效）；复验同一批命令即把「绕过硬护栏」变为「远端挡住」", "basis": "A-2/A-3"},
  {"id": "B2", "claim": "CI job 只提供可复验位点；真正「挡住合并」取决于 GitHub 侧 branch protection。本仓已于 2026-10-03 开启（required check=[verify] + Require PR(approvals=0) + enforce_admins=true）⇒ 直推 main 被拒、合并须 PR 且 check 绿；approvals=0 是单人仓防自锁的必需取值", "basis": "A-1"},
  {"id": "B3", "claim": "检查面应取本地五 hook 的超集（加内嵌自测），否则 CI 可能弱于本地", "basis": "A-4"}
]
```

## 附录 C 假设区（2 项）

- [H1] CI 平台/行尾差异（Windows runner 的 CRLF vs LF）是否影响 `console_gen --check` 与计数类读数——**已实测·回填（2026-10-03，E2）**：首次远端运行（run 37106315633）失败**非行尾所致**，而是 CI 日志管道 stdout 默认 **cp1252** ⇒ 校验器打印中文即崩（在打印违规前 exit 1，纯环境面）；修复 = job 级 `env: PYTHONUTF8=1 / PYTHONIOENCODING=utf-8`（run 37106881947 全绿）。行尾差异在本次运行中**未观察到影响**。
- [H2] 远端 required check（branch protection）的实际开启形态未在本仓侧登记——**已回填（2026-10-03，E2，gh api 回读）**：`required_status_checks = {strict:false, contexts:["verify"]}` + `required_pull_request_reviews = {required_approving_review_count:0, dismiss_stale_reviews:false, require_code_owner_reviews:false}` + `enforce_admins = true` + `allow_force_pushes = false` + `allow_deletions = false`。`approvals=0` 为**单人仓防自锁的必需取值**（PR 作者不可自 approve，设 ≥1 即永久无法合并）。

---

**Review 签字**: _________ 日期: _________