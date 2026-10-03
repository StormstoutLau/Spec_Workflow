# 审查验收 Checklist：L2 CI 门禁（远程兜底强制）

---
id: ci-gate-CHECKLIST
type: design
version: 1.1
status: accepting
date: 2026-10-03
depends: [ci-gate-IMPLEMENTATION, ci-gate-DESIGN]
upstream: null
---

> **Feature**: L2 CI 门禁（远程兜底强制，P-070）
> **创建日期**: 2026-10-03
> **状态**: accepting（验收中；真异基座独立 pass 仍待触发）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [IMPLEMENTATION.md](./IMPLEMENTATION.md) **v1.1**
> **基于设计**: [DESIGN.md](./DESIGN.md) **v1.1**
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.1**（5A+3B+3C+2H）

---

## 1. 文档一致性验收（Step 8）

| 检查项 | 状态 | 说明 |
|--------|------|------|
| RESEARCH → DESIGN 决策可追溯 | ✅ | DESIGN §2 逐条引 RESEARCH A/B |
| DESIGN → IMPLEMENTATION 映射可追溯 | ✅ | IMPLEMENTATION §3 步骤表 = DESIGN §3.1/§4 |
| 检查面映射与本地 hook 逐条对应 | ✅ | DESIGN §4 五行映射（等价/超集标注） |

## 2. 功能验收

| # | 验收项 | 判据 | 状态 | 证据 |
|---|--------|------|------|------|
| F1 | workflow 存在且语法有效 | `.github/workflows/ci.yml` 可被 GitHub 解析（YAML 合法、`jobs.verify` 存在） | ✅ | 文件 + 本机 YAML 解析 |
| F2 | 检查面 = 五 hook 等价 | 五个等价命令齐备且顺序 = 门禁链 | ✅ | IMPLEMENTATION §3 |
| F3 | 内嵌自测纳入 | 六件 `--selftest`/`selftest` 全跑 | ✅ | IMPLEMENTATION §3 步骤 6 |
| F4 | 命令本机可过 | 逐条复跑全绿（**161**/0、0、0、与源一致、**94** exit 0、自测全过） | ✅ | IMPLEMENTATION §4 |
| F5 | 远端保护态已开启（真机械阻断） | branch protection = required check `verify`（`strict=false`）+ Require PR（`approvals=0`）+ `enforce_admins=true`；直推 main 被拒 | ✅ | gh api 回读（2026-10-03）+ DR-2 |

## 3. 接口验收

| # | 验收项 | 判据 | 状态 |
|---|--------|------|------|
| I1 | 触发/权限/运行时声明齐 | `on`（push/PR/dispatch）+ `permissions: contents: read` + `windows-latest` + Python 3.11 | ✅ |

## 4. 不变式验收

| 不变式（DESIGN §8） | 验证方式 | 状态 |
|---|---|---|
| I-1 只搬不扩 | 全文核查：无本地未有的新判据 | ✅ |
| I-2 只读零副作用 | 步骤全为 check/selftest；**无** `--stage`、无 `--write` | ✅ |
| I-3 入口命令单一权威 | 直接调既有 CLI，无新包装脚本（`declared.scripts` 不变） | ✅ |
| I-4 fail-closed | 无 `continue-on-error` | ✅ |
| I-5 不回写真值源 | 无 commit/push/写盘步骤 | ✅ |
| I-6 边界诚实 | workflow 头 + DESIGN §7 显式声明三条边界 | ✅ |

## 5. 错误处理验收

| # | 场景 | 预期 | 状态 |
|---|------|------|------|
| E1 | 任一步非 0 | job 失败（fail-closed）且日志可定位 | ✅ |

## 6. 性能验收

| # | 项 | 判据 | 状态 |
|---|---|------|------|
| P1 | 复验成本可接受 | 无网络、无第三方安装；仅 stdlib 脚本 + 六件自测 | ✅ |

## 7. 兼容性验收

| # | 项 | 判据 | 状态 |
|---|---|------|------|
| C1 | 本地开发零影响 | `.pre-commit-config.yaml` 与五 hook 零改动 | ✅ |
| C2 | 平台对齐开发环境 | runner = Windows + Python 3.11（= 本机 3.11.16） | ✅ |

## 8. ADD 审计（Step 10）

### 8.1 Spec 质量门

| 维度 | 得分（0-1） | 说明 |
|------|-----------|------|
| 可测试约束 | 1.0 | 六条不变式均有文件级核查方式 |
| 模块映射 | 1.0 | 设计步骤 ↔ workflow 步骤一一对应 |
| 接口契约 | 1.0 | 触发/权限/运行时显式固定 |
| 修正项 | 1.0 | 无实施期修正 |
| 跨模块契约 | 1.0 | 只触 workflow 单文件 + 登记面 |
| **总分** | 5/5 | **档位**: A |

### 8.2 ADD 审计发现

| 严重性 | 发现 | 证据 | 处置 |
|--------|------|------|------|
| P3 | 首跑暴露**环境面编码假设**：CI 日志管道 stdout 默认 cp1252 ⇒ 校验器打印中文即 `UnicodeEncodeError`（**在打印违规之前** exit 1，非违规） | run 37106315633 日志（DR-1） | **已修**（job 级 `PYTHONUTF8` / `PYTHONIOENCODING`）；属环境面，非规格缺陷 |
| P2 | L2 首跑 PR（run 37112565627）：`console_gen --check` 报「CONSOLE.md 已过期」——**根因 = ⑂ 支线段取本地分支名（环境态）入产物** ⇒ 跨环境不可复现 | DR-3 | **已修**（§8 改由 `docs/rework-graph.json` 派生 + project-console DESIGN v1.13）；**属真实确定性缺口，非环境假红** |
| — | 判据 / 命令全沿用既有，无**规格级**修正 | IMPLEMENTATION §4 | 无需修 |

### 8.3 ADD Iron Law 检查

- [x] 断言恒真式：F1-F5 均指向可独立复核的机械读数，非恒真断言；
- [x] 单文件检查盲区：F4 为**逐条命令**复跑（非仅 YAML 存在性）；
- [x] 设计文档独有约束无测试：六条不变式各有文件级核查；
- [x] 修正阻断性项无测试：本批零修正项。

### 8.4 独立 pass（RULE-1 / RULE-5）

- [ ] **真异基座独立 pass（待触发）**：需换基座模型方可关闭；本环境不可得。

## 9. 文档完整性

| 文档 | 存在 | 与实现一致 |
|------|------|----------|
| RESEARCH.md | ✅ | ✅ |
| DESIGN.md | ✅ | ✅ |
| IMPLEMENTATION.md | ✅ | ✅ |
| CHECKLIST.md（本文件） | ✅ | ✅ |
| ADR（本批无新增） | — | — |

## 10. 验收结论

### 10.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|------|------|------|------|------|
| 文档一致性 | 3 | 3 | 0 | 0 |
| 功能 | 5 | 5 | 0 | 0 |
| 接口 | 1 | 1 | 0 | 0 |
| 不变式 | 6 | 6 | 0 | 0 |
| 错误处理 | 1 | 1 | 0 | 0 |
| 性能 | 1 | 1 | 0 | 0 |
| 兼容性 | 2 | 2 | 0 | 0 |
| ADD 审计 | 4 | 3 | 0 | 1 |
| **总计** | 23 | 22 | 0 | 1 |

> **统计口径（RULE-2）**：上表来自本文件**逐项核对**（每一项均有独立标记），非事后汇总推算。
>
> **规范形态（P-050 交付 A，由 `dc_validator` M4 分支② 机械校验）**：① 章节号固定 `### 10.1 验收统计`；② 数值单元格 = **纯十进制整数**；③ 表内两条算术必须成立——逐行 `总数 = 通过 + 失败 + 待办`，总计行 = 8 类行**按列求和**。

### 10.2 验收决定

- [ ] **验收通过**：所有 P1 项通过，无阻塞性问题
- [x] **有条件通过**：**22/23** 通过；唯一待办 = 真异基座独立 pass（§8.4）；四件套 + workflow + 远端保护态已落地
- [ ] **验收失败**

### 10.3 签字

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | | |
| 审查者 | | |

## 11. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|------|--------|------|------|
| **真异基座独立 pass**（RULE-1/RULE-5） | — | — | 待触发 |
| **H1**（平台/行尾差异是否致假红） | — | — | ✅ 已回填（实为管道编码 cp1252，已修；DR-1） |
| **H2**（远端 required check / branch protection 形态） | — | — | ✅ 已回填（保护态已开启，见 F5 / DR-2） |
| **直推 main 绕过处置（选 B）** | — | — | ✅ 已开启（Require PR `approvals=0` + `enforce_admins=true`） |
| 更新 PROGRESS.md / CODE_WIKI.md | — | — | ✅ |

---

**Review 签字**: _________ 日期: _________