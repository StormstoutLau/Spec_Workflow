# 设计文档：L2 CI 门禁（远程兜底强制）

---
id: ci-gate-DESIGN
type: design
version: 1.1
status: in-review
date: 2026-10-03
depends: [ci-gate-RESEARCH, ADR-0010, ADR-0011]
upstream: null
---

> **Feature**: L2 CI 门禁（远程兜底强制，P-070）
> **创建日期**: 2026-10-03
> **状态**: 评审中（首版；异基座独立 pass 待触发）
> **Spec 步骤**: Step 3-4
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.1**（5A+3B+3C+2H）
> **本批范围**: 用户指令「先实现 L2 CI 门禁」——新增远端 workflow，复验与本地五 hook 等价的判据 + 内嵌自测。**零新判据 / 零新脚本 / 零新依赖 / 零 API 破坏**。

---

## 1. 设计目标

把 L1（本地 pre-commit 五 hook）的判据**原样**搬到远端复验，使「绕过本地 hook」不再等于「放行」：

1. **不新增判据**：只搬已存在的机械判据（守「只搬不扩」）；
2. **不新增脚本**：复用既有校验器 CLI（`declared.scripts` 不变）；
3. **只读零副作用**：不写文件、不需网络、无第三方依赖（与三校验器同栈 stdlib）。

一句话：**L2 的正确形态 = 给既有判据补一个远端触发位点**，而非新立规则。

## 2. 设计依据

| 调研发现 | 设计决策 | 引用 |
|---|---|---|
| 本仓无 CI 位点；五 hook 为唯一机械执行位点 | **D1**：新增 `.github/workflows/ci.yml`（**唯一新增文件**） | A-1/A-2 |
| 本地 hook 可 `--no-verify` 绕过 | **D2**：远端复验同一批命令（**同判据、同 CLI**），绕过本地即被远端挡住 | A-3/B1 |
| 检查面 CLI 已齐且只读 stdlib | **D3**：检查面 = 五 hook 等价命令 + 内嵌自测（**超集**，非新判据） | A-4/B3 |
| 本机 Windows + Python 3.11 | **D4**：runner = `windows-latest`、Python `3.11`（对齐开发环境以降假红） | A-5 |
| 只读诊断器「检出即 exit 1」与其「不接门禁」定位冲突 | **D5**：**不接入** `anchor-audit` / `backflow-audit` / `downstream_compliance`（它们读跨仓/信息面） | RESEARCH §4.2 |
| 远端 required check 只拦 PR 合并、**不拦直推**（H2 回填） | **D6**：在 GitHub 侧开启 `required_status_checks=[verify]` + Require PR（`required_approving_review_count=0`）+ `enforce_admins=true` ⇒ 直推被拒、PR 门生效（治理面；`approvals=0` 为单人仓防自锁必需值） | H2/B2 |

## 3. 架构设计

### 3.1 workflow 结构

```text
.github/workflows/ci.yml
  on: push(main) / pull_request / workflow_dispatch
  permissions: contents: read
  jobs.verify: runs-on: windows-latest   steps:
    [1] setup-python 3.11
    [2] dc-validator  --check-all          ← 五 hook 之一（等价复验）
    [3] m7-stats                           ← 五 hook 之二
    [4] repo-stats                         ← 五 hook 之三
    [5] console-gen  --check               ← 五 hook 之四
    [6] step-enforce（git ls-files 全量四文档）← 五 hook 之五
    [7] 内嵌自测 ×6（dc / m7 / repo_stats / console_gen / spec_runner / rework_graph）
```

**fail-closed**：任一步非 0 退出即 job 失败；步骤顺序 = 门禁链顺序（契约 → 账本 → 视图 → 派生 → 决策流 → 自测）。

### 3.2 「只搬不扩」的边界

- **不接** 三个只读诊断器（理由见 D5）：它们的设计语义是「报告待处理」而非「阻断提交」；
- **不新增** 本地没有的判据（如需扩权，须另立批并过 ADR-0010 三问）。

## 4. 检查面映射（本地 hook ↔ CI 步骤，逐条等价）

| 本地 hook（id） | 本地 entry | CI 步骤 | 等价性 |
|---|---|---|---|
| `dc-validator` | `python scripts/dc_validator.py`（staged） | `--check-all`（全仓） | **超集**（CI 查全仓，本地查 staged） |
| `m7-stats` | `python scripts/m7_stats.py`（M7 路径） | 同命令 | **等价** |
| `repo-stats` | `python scripts/repo_stats.py` | 同命令 | **等价** |
| `step-enforce` | `python scripts/step_enforce.py`（staged 四文档） | `git ls-files 'spec/*/*.md'` 全量 | **超集**（本地 staged / CI 全量） |
| `console-gen` | `python scripts/console_gen.py --stage`（提交即刷） | `--check`（只读核对） | **等价**（本地写盘 + add；CI 只核对，不写） |

> CI 侧**不**使用 `--stage`（不写盘、不 add）——CI 只做「是否已一致」的判定。

## 5. 接口定义

| 载体 | 内容 |
|---|---|
| 触发 | `push`（`main`）/ `pull_request` / `workflow_dispatch` |
| 运行时 | `windows-latest` + `actions/setup-python@v5`（`3.11`） |
| 权限 | `contents: read`（只读仓） |
| 退出语义 | 任一步非 0 ⇒ job 失败（fail-closed） |

## 6. 替代方案

| 方案 | 内容 | 结论 |
|---|---|---|
| **A（选择）** | 单 workflow + 五 hook 等价命令 + 内嵌自测 | **采纳**——零新判据/脚本/依赖，最小增量 |
| B | 把 CI 命令抽成 `scripts/ci_check.py` 统一入口 | **否决**——新增脚本会改 `declared.scripts`，且与「五 hook 已是唯一权威命令面」形成第二实现（撞 I-10 语义同源） |
| C | `ubuntu-latest` 跑 | **本轮否决**——本仓重 Windows 特性，跨平台漂移可能造成假红；行尾/平台差异未实测（H1）⇒ 先取同平台，跨平台另立观察项 |
| D | 把只读诊断器也接进 CI | **否决**——检出即 exit 1，会把信息性发现变 CI 红灯（D5） |
| E | 不建 CI，只登记候选 | **否决**——用户显式指令要求实施；且判据已齐（A-4），属纯位点补位 |

## 7. 边界声明

1. **只在本仓触发**——对消费仓（Cpp_Hub 等）**不产生任何强制**；跨仓 L3 属 P-039 **P-c**、未实现。
2. **强制力已开启（2026-10-03）**——GitHub 侧 branch protection 已启用：`required_status_checks.contexts=["verify"]`（`strict=false`）+ `required_pull_request_reviews.required_approving_review_count=0` + `enforce_admins=true` ⇒ **直推 main 被拒**、改动须经 **PR 且 `verify` 绿**方可合并。`approvals=0` 为**单人仓防自锁的必需取值**（PR 作者不可自 approve）。**回退体**存于 `.git/protection-rollback-body.json`（本地、不入库）。
3. **不覆盖「绕过 CI 本身」**——若远端策略允许直推绕过 required check，则 L2 亦失效；这是**平台治理**面，非本仓可解（与 L1 的 `--no-verify` 同源限制）。**已收窄（2026-10-03）**：`enforce_admins=true` 关闭了管理员豁免 ⇒ **直推路径已堵**；残余面 = 管理员在 Settings 主动改写 branch protection 本身（**平台治理面，非本仓可解**）。
4. **不追溯历史**——CI 自本批起生效，不回改历史提交。

## 8. 不变式（Invariants）

1. **I-1 只搬不扩**：CI 复验的判据集 ⊆ 本地既有判据集（仅等价或超集于**同一批命令**）；新增判据须另立批。
2. **I-2 只读零副作用**：CI 步骤不写任何文件（尤其**不用** `console_gen --stage`）、不需网络、无第三方依赖。
3. **I-3 入口命令单一权威**：CI 直接调既有校验器 CLI，**不新建**包装脚本（避第二实现，I-10 语义同源）。
4. **I-4 fail-closed**：任一步非 0 ⇒ job 失败；不设 `continue-on-error`。
5. **I-5 不回写真值源**：CI 不 commit、不 push、不改 `PROGRESS` / 事件流 / 派生视图。
6. **I-6 边界诚实**：workflow 头部显式声明「不强制消费仓 / 强制力受远端策略约束 / 非运行时阻塞」。

## 9. 幻觉抑制审查（Step 4 Review）

- 设计决策逐条挂 A/B 锚点（§2 表「引用」列），无悬空决策；
- §6 五个替代方案均给否决理由；
- §7 四条边界为**关键诚实声明**（防把 CI 读成「跨仓强制」或「运行时强制」）。

## 10. 对实施的输入

1. **唯一新增文件** = `.github/workflows/ci.yml`（§3.1 结构 + §4 映射）；
2. **禁止项**：不新增脚本 / 不接只读诊断器 / 不使用 `--stage` / 不设 `continue-on-error`；
3. **登记项（已回填）**：H1（平台/行尾差异 ⇒ 实为管道编码，已修）/ H2（远端 required check 形态 ⇒ 保护态已开启，见 §7 第 2 条）均于 2026-10-03 实测回填；**强制力开关（D6）已实施**，回退体见 §7。

---

**Review 签字**: _________ 日期: _________