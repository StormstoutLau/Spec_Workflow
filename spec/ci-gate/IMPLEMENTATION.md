# 实施文档：L2 CI 门禁（远程兜底强制）

---
id: ci-gate-IMPLEMENTATION
type: design
version: 1.1
status: draft
date: 2026-10-03
depends: [ci-gate-DESIGN, ci-gate-RESEARCH]
upstream: null
---

> **Feature**: L2 CI 门禁（远程兜底强制，P-070）
> **创建日期**: 2026-10-03
> **状态**: draft（草稿）
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md) **v1.1**
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.1**（5A+3B+3C+2H）

---

## 1. 实施概述

本批**只新增一个文件**：`.github/workflows/ci.yml`（L2 远端复验位点）。判据、命令面、脚本**均沿用既有**：

1. **落点**（DESIGN D1）：workflow = 唯一新增件；
2. **检查面**（DESIGN D3）：五 hook 等价命令 + 内嵌自测（超集）；
3. **边界**（DESIGN D5）：不接只读诊断器、不使用 `--stage`、不设 `continue-on-error`。

**零新脚本 / 零新依赖 / 零 API 破坏 / 零真值源回写**。

## 2. 文件与改动面

| 文件 | 改动 | 说明 |
|---|---|---|
| `.github/workflows/ci.yml` | **新增** | L2 门禁 job（只读复验） |
| `spec/ci-gate/*.md` | 新增 | 本批四件套（文档） |
| `docs/PROGRESS.md` / `CODE_WIKI.md` / `docs/CONSOLE.md` | 登记同步 | P-070 / 树 / §9 / 计数 |

**零改动**：`scripts/` 全体、`tools/spec_runner/`、`.pre-commit-config.yaml`、任何校验器逻辑。

## 3. workflow 逐步骤（`.github/workflows/ci.yml`）

| # | 步骤 | 命令 | 幂等/只读 |
|---|---|---|---|
| 0 | 检出 + Python | `actions/checkout@v4` + `setup-python@v5`（`3.11`）+ job 级 `env`（`PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8`，见 DR-1） | — |
| 1 | DC 契约 + R7 计数 | `python scripts/dc_validator.py --check-all` | 只读 |
| 2 | M7 账本 hits 块 | `python scripts/m7_stats.py` | 只读（**无** `--write`） |
| 3 | 视图层枚举 | `python scripts/repo_stats.py` | 只读 |
| 4 | 派生视图与源一致 | `python scripts/console_gen.py --check` | 只读（**无** `--stage`） |
| 5 | 决策流批次强制 | `python scripts/step_enforce.py $(git ls-files 'spec/*/*.md')` | 只读 |
| 6 | 内嵌自测 ×6 | `--selftest` ×4 + `spec_runner selftest` + `rework_graph_check --selftest` | 只读（selftest 用 tempfile） |

**fail-closed**：任一步非 0 ⇒ job 失败（DESIGN I-4）。

## 4. 本地等价比对与读数

**比对方式**（E2，2026-10-03 本机实跑）——**逐条以 CI 将要执行的同一命令**在开发机上复跑，证明「命令本身可过」，而平台差异另立 H1：

| CI 步骤 | 本机读数 |
|---|---|
| `dc_validator --check-all` | **161 文件 / 0 违规**（批后；批前 157） |
| `m7_stats` | 0 违规（P3 提示 1） |
| `repo_stats` | 0 违规（P3 0） |
| `console_gen --check` | 「与源一致」 |
| `step_enforce`（全量四文档） | **94 文件 / exit 0**（批后；批前 90） |
| 内嵌自测 ×6 | dc **27/27** / console_gen **52/52** / spec_runner **63/63** / rework_graph **30/30** / m7 与 repo_stats 各自通过 |

> **口径** = 开发机（Windows + Python 3.11.16）；`step_enforce` 的 **94** 文件 = `spec/<feature>/[*_]{RESEARCH,DESIGN,IMPLEMENTATION,CHECKLIST}.md` 全集（**批前 90 → 批后 94**，增量即本批自身 `spec/ci-gate/` 四文档）。
> **注意**：本比对证明「命令可过 + 版本/平台对齐」，**不等于**已在 GitHub 远端跑过（本批无远端运行证据，如实登记）。

## 5. 错误处理与回退

| 场景 | 处理 |
|---|---|
| 任一步失败 | job 失败（fail-closed），日志即定位面 |
| 平台/行尾造成假红（H1） | 回退点 = 把该步骤的 runner 换回/换地，或将该步骤标记为观察项（须显式裁决，不设静默 `continue-on-error`） |
| 需要临时关闭 | 在 GitHub 侧禁用 workflow（不删文件），或裁决后删除 workflow 单文件（**唯一回退动作**，零耦合） |
| **branch protection 回退（DR-2）** | 以 `.git/protection-rollback-body.json` 执行 `gh api --method PUT .../branches/main/protection --input <该文件>` ⇒ 恢复「仅 required check、无 Require PR、`enforce_admins=false`」的 A 态（**回退体本地持有、不入库**） |

## 6. 校验

- 三校验器全绿 + `console_gen --check` 与源一致 + 门禁链 `step-gate` / `verify-anchor` / `step-enforce` 全 exit 0；
- **远端首跑**（GitHub Actions run `37106881947`）八步全绿（DR-1）；
- **零新增 M7 样本**（本批为基础设施件，无新失效形态）。

## 7. 决策记录（DR）

| # | 决策 | 背景 | 结论 |
|---|---|---|---|
| DR-1 | 首跑失败定位与修复：**管道编码而非行尾** | 首次远端运行 `37106315633` 在**第 1 步 `dc_validator`** 失败：`UnicodeEncodeError: 'charmap' codec can't encode characters in position 18-19`（CI 日志管道下 stdout 默认 **cp1252** ⇒ 校验器打印中文即崩，**在打印违规之前**退出 ⇒ 非违规、纯环境面） | job 级 `env: PYTHONUTF8=1 / PYTHONIOENCODING=utf-8` + job name 改 ASCII `verify`（使 required-check context 为纯 ASCII）⇒ 复跑 `37106881947` 全绿（8 步）。**不设 `continue-on-error`**（守 I-4）；**不改任何校验器代码** |
| DR-2 | 直推 main 绕过 required check 的处置：**选 B（Require PR）** | required status checks **只拦 PR 合并、不拦直推**；本仓日常为「commit → 直推 main」⇒ CI 在**推送后**才跑，红了代码已落 main ⇒ 「绕过本地 hook ≠ 放行」在直推路径上**未兑现** | 开启 `required_pull_request_reviews`（`required_approving_review_count = 0`）+ `enforce_admins = true` + 保留 `required_status_checks=[verify]` ⇒ **直推被拒**、合并须 PR 且 check 绿。**`approvals=0` 是必需取值**（PR 作者不可自 approve，设 ≥1 即永久自锁）。自审 PR **不构成独立复核**（RULE-1~6），故如实声明 = **机械门**，非审查层。回退体 = `.git/protection-rollback-body.json` |

---

**Review 签字**: _________ 日期: _________