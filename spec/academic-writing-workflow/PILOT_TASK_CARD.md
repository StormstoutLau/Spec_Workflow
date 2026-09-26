---
id: academic-writing-workflow-PILOT_TASK_CARD
type: template
version: 0.4
status: draft
date: 2026-09-13
depends: [academic-writing-workflow-RESEARCH]
upstream: academic-writing-workflow-RESEARCH
---

# Pilot 最小任务卡模板——论文仓逐仓迁移（P-040 落地）

> **用途**: 作为「广播清理」首个 pilot 仓的执行清单。每行一个原子迁移动作，右侧两列给出**可机械检出的判据**与**通过门（gate）**——取代"凭感觉做"的执行方式，改由"跑脚本、看输出、对号"驱动。
> **地位**: 模板，随 pilot 一起实测修订。**验证通过后升格为规范文档 #4；若证明是负担则丢弃**（懒加载，进可升格、退可弃）。
> **上级调研**: [RESEARCH.md](RESEARCH.md) §15-17（C-15/C-16/C-18/C-19 + B24/B25 + H12/H16）。
> **隐私约束**: 本卡**每步都不得触碰 `data_policy.md` 红线内容**。C-19：隐私隔离优先级最高，`data_policy.md` 为**首件交付**，先划红线，再谈整洁。

---

## 0. Pilot 仓指定（2026-09-13 实测）

| 项 | 值 |
|---|---|
| **pilot 仓** | `D:\Article\Working paper\LGMM\LGMM 8.0`（C-22：最接近 compendium 的仓） |
| **实测基线** | 单批盘点（2026-09-13）：一级目录 12 子 + 8 顶层文件；lean4=16 非 14；paper/ 24 编译产物；状态词文件名 21；同名文件集中在 `data/co_pricing_zoo`/`OpenSourceAP_CrossSection` 子仓 |
| **数据策略** | `data/policy.md` 定稿前施行**只读**：本卡所有判据只扫描、不删改（H14 裁决前不删任何文件） |
| **首个迁移动作** | §2.1（编译产物排除）——最无争议、纯机械、零风险 |
| **进入门槛** | H12/H13 裁决不跳过；**Lean 双源判据已修正**（见 §2.3）：`LGMM_Lean/` 为 mathlib 全量（7735 .lean），非第二专有源

---

## 1. 前置：立契约层（一次性，S1）

| # | 动作 | 可机械检出判据（LGMM 8.0 实测命令） | 通过门（gate） |
|---|---|---|---|
| 1.1 | 写 **一页 `CONVENTIONS.md`** | `Test-Path "$root\CONVENTIONS.md"`；命名词表 grep（`.tex` 无状态词 / 无空格）、派生物黑名单、单一真值声明、脚本分层四节齐全；总行数 `(Get-Content …).Count -le 80` | 四节各 ≥1 行；行数 ≤80 |
| 1.2 | 铺设**三模板**（compendium / codebook / 命名标签） | 模板文件存在；`.gitignore` 已有 LaTeX 产物段（实测已具备）即视为 compendium 模板已铺 | MANIFEST 目录骨架 + gitignore LaTeX 段均在 |
| 1.3 | 写 **`data_policy.md`**（红线，首件） | `Test-Path "$root\data_policy.md"`；列出该仓不可公开项（`data/manual_llm/`、对话记录等） | 红线清单落档 |
| 1.4 | 确立 **`INDEX.md`** 登记 | 共享层索引含 LGMM 8.0 条目（名称/状态/关联） | 条目与 MANIFEST §6 目录骨架一致 |

> **信任检查点**：本步只产"文档"不产"迁移"。用 `repo_stats` 类对账确认声明 = 机械重数。**实测发现 README 顶层目录树仍列已废弃 `MAPPING.md`，与 MANIFEST 归档声明冲突——记入 §2.4 处置。**

---

## 2. 逐仓迁移（S2，原子动作）

> **判据 = 真实可跑命令（PowerShell，`$root="D:\Article\Working paper\LGMM\LGMM 8.0"`）**，每完成一行记 gate 通过结果，不堆批。**实测基线：`paper/` 有 24 个编译产物、状态词文件 21 个、lean4=16 非 14、README/MANIFEST 声明冲突 1 处。**

| # | 动作 | 可机械检出判据（LGMM 8.0 实测命令） | 通过门（gate） |
|---|---|---|---|
| 2.1 | 排除**编译产物混放** | `Get-ChildItem $root\paper -File -Include *.aux,*.bbl,*.blg,*.log,*.out,*.toc,*.dvi,*.fls,*.fdb_latexmk,*.synctex.gz` → 输出必须为空 | 扫描读数 = 0（实测 24 → 迁移后 0） |
| 2.2 | 拆解**状态词入名** | `… -File | Where Name -match '_?(final\|corrected\|reviewed\|rigorous\|complete\|v\d)'` → 无命中 | grep 状态词 = 0（实测 21 → 0） |
| 2.3 | **单一真值 + 版本外置（双源实测修正 v0.3）** | **实测结论**：`LGMM 8.0/lean4/`（16 专有）与 `LGMM_Lean/LGMM/`（陈旧同名副本）**存在双源**。只读 hash 对比（2026-09-13）：16 专有 → 12 同名且内容一致 / **1 DIFF（`EWNLS.lean`，hash 不同）** / 3 仅在本仓。判据 = `Get-FileHash` 逐对对比同名 `.lean`，DIFF 计数必须 = 0；12 一致者可指向单一真值（本仓 `lean4/`），EWNLS 与 3 单宾语需 H13 裁决 | DIFF = 0；唯一真值源 = `lean4/` |
| 2.4 | **同名文档收敛 + 声明对齐** | 根层同名 = 0（实测：仅 README.md 1 份，无重复）；**README 目录树删除已废弃 `MAPPING.md` 条目**（与 MANIFEST 归档声明冲突）；文档声明内容编码一致 | 根层同名 ≤1；README/MANIFEST 声明互不矛盾 |
| 2.5 | **脚本分层对齐** | MANIFEST §6 已声明 `code/scripts/{data_download,monte_carlo,empirical,figures_tables,exploratory}` 分层；校验 `code/` 无 stray 脚本（非 `src/`/`scripts/`/`tests`/`archive/deprecated`/`lgmm`） | 目录树与 MANIFEST 声明一致；无游离脚本 |
| 2.6 | **辅助资产归属（B24）** | `data/factor_papers/`（PDF）→ 依 A-86 判定移出或标注 VoR；codebook 升一等 `data/CODEBOOK.md`（A-88 列齐）；`data/manual_llm/` 归红线 | B24 归属表逐项勾选；无残留 |
| 2.7 | **归档快照处置（H14 后）** | `paper/archive/` 卡片核对：`LGMM-7_0`/`LGMM-8_0`/`_methodology` 均已被 MANIFEST §7 声明归档 | 归档表与 MANIFEST §7 一致；裁决前不删 |

> **信任检查点**：每行 gate 通过结果落档。若某动作出现「判据无法机械检出」，记入模板修订意见（H12 最小充分集观测），勿强留在任务卡。

---

## 2.8 只读实测报告（2026-09-13，零写入）

在 LGMM 8.0 **只读**跑全部 §2 判据的实证矩阵（不越过 H14）：

| 判据 | 结果 | 实测读数 | 修正/备注 |
|---|---|---|---|
| 2.1 编译产物 | ❌ 未通过 | paper/ 共 26（live 20 + archive 6） | 首个迁移动作 |
| 2.2 状态词 | ⚠️ 部分 | 排除 archive 18，其中 ~12 在 `data/co_pricing_zoo/` 第三方子仓（**不计本仓缺陷**）；LGMM 真态 ≈6 | 判据须排除子仓目录 |
| 2.3 Lean 真值 | ❌ 判据曾设错→已修正 | 双源存在：12 同名一致 / 1 DIFF(`EWNLS.lean`) / 3 仅本仓 | **推翻 v0.2「双源不存在」错误结论** |
| 2.4 同名+声明 | ⚠️ | 根层同名 0 ✅；README 引用 MAPPING vs MANIFEST 已归档 → 冲突；MANIFEST 声明 lean=14 实测 16 | 声明漂移 ×2 |
| 2.5 脚本分层 | ✅ 通过 | code/ 根层游离 0；7 子层与声明一致 | — |
| 2.6 辅助资产 | ⚠️ | factor_papers 31 PDF；CODEBOOK 缺；manual_llm 2 文件待归红线 | 待 A-86/A-88 |
| 2.7 归档快照 | ⚠️ | paper/archive 12 文件 + 2 散落 zip/rar | H14 裁决前不删 |

**结论**：本卡判据已从「假设可执行」被实测验证为「可用真命令跑出对/错」。其中 2.2 需排除第三方子仓、2.3 依赖 hash 对比——两者是 pilot 暴露的最小充分集差异（H12 观测 #1、#2）。

---

## 3. 后置：实证最小充分集（H12 产出）

| # | 动作 | 可机械检出判据 | 通过门（gate） |
|---|---|---|---|
| 3.1 | 用本卡重跑一遍 pilot 仓 | 全 gate 复验通过；**无「判据列不可执行」**的空洞 | 所有判据均有真实脚本/计数 |
| 3.2 | 记录 H12 最小充分集结论 | 得出「一页契约 + 三模板」**覆盖 / 覆盖不足**的明确结论（含新出现的差异项） | 结论落档，标注依据 |
| 3.3 | 决议 H16（广播粒度） | 依据 3.2：选 **gap-fill 全量翻新 / strangler-fig 渐进** 之一 | 决议 + 理由落档 |
| 3.4 | 升格/弃用本卡 | 若 3.1/3.2 证明 {卡有用 → 升格规范文档 #4；卡是负担 → 丢弃} | 最终处置明确 |

---

## 4. 与既有机制衔接

- **信任链**：本卡是「执行态」辅助（怎么按序做、怎么算过），不取代「产物态」校验器（`dc_validator`/`repo_stats`/`m7_stats`）。两者层级分离（Diátaxis 禁混模式，A-82）。
- **触发一致**：C-22 的 pilot 选择 = C-15 的"首个迁移仓"，同一动作；C-23 已裁定。
- **懒加载**：本卡 zero 工具/zero 依赖；仅当 pilot 实测证明其减口径漂移才保留，否则丢弃。

---

## 5. 附录：共享层 `INDEX.md` 模板（B25 交付物之一）

> **用途**：B25 判定的「共享层三件套」之②——`Working paper/` 根的项目登记索引，取代当前模糊的根 `CODE_WIKI.md` 定位（B23）。**登记 LGMM 8.0 为 #1**，其余 ~17 仓待逐仓补齐。
> **纪律**：本索引**只登记指针**（名称 / 路径 / 状态 / 关联 / 红线），**不复制**各仓真值内容（I-1 一份真值；C-20 层间唯一连接是引用键）。

```markdown
# INDEX — 论文仓登记索引

> **作用**: monorepo 顶层项目登记（B25）。**只放指针，不放内容**。
> **配套**: `WORKSPACE.md`（规范）/ `data_policy.md`（红线清单）。三类文件合为一套契约层。

## 项目登记

| # | 项目 | 路径 | 版本目录 | 状态 | 关联 | 红线 | 规范度 |
|---|------|------|---------|------|------|:----:|:------:|
| 1 | LGMM | `LGMM/LGMM 8.0` | `LGMM 8.0` | 活跃（四份拆分中） | `LGMM_Lean/`（Lean 依赖） | 待 `data_policy.md` 定稿 | 接近 compendium（pilot） |
| 2 | … | … | … | … | … | … | … |

**列义**：
- **版本目录**：版本作为**目录名**的既成形态（≥5 种，需在 `WORKSPACE.md` 归一为 ISO 8601 或标签式）
- **状态**：活跃 / 冻结 / 归档（与 A-81 的版本标签范式对齐，勿用 `_Final` 类状态词入名）
- **关联**：跨仓依赖（如 Lean 依赖库、共享数据、子模块）
- **红线**：该仓是否有**绝不外传**内容（取值：`无` / `有（见 data_policy.md §X）`）
- **规范度**：`compendium` / `部分` / `裸 tex 堆`（三档，用于排定迁移顺序）

## 缺口（显式，勿静默跳过）

- 未登记仓：…
- 未决项：H14（归档快照处置）/ H15（363 PDF 版本构成）——**裁决前不得删除**
```

---

## 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 0.1 | 2026-09-13 | 初稿：按 C-15/C-19/B24 + H12/H16 起草三阶段待实测模板 |
| 0.2 | 2026-09-13 | **LGMM 8.0 实测定档**：填充 pilot 仓；判据全部替换为真实 PowerShell 命令；**修正 Lean 双源判据**（`LGMM_Lean` = mathlib 全量 7735 .lean，非第二专有源，原 H13 双源假设不成立）；检出 README/MANIFEST 声明冲突 |
| 0.3 | 2026-09-13 | **§2 只读实测**：跑完全部判据产出矩阵；**推翻 v0.2 结论**——`LGMM_Lean/LGMM/` 是一项目根非 mathlib，双源漂移真实存在（hash=12 一致/1 DIFF/3 仅本仓）；2.3 判据改回 hash 对比；补 §2.8 实测报告与 H12 观测 |
| 0.4 | 2026-09-13 | 补 **§5 共享层 `INDEX.md` 模板**（B25 交付物之二；登记 LGMM 8.0 为 #1，其余待补；只放指针纪律） |