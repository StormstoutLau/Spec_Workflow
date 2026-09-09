# 验收清单：ARC 决策图谱升级（吃狗粮模式，P-035）

---
id: arc-rollout-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-09
depends: [arc-rollout-IMPLEMENTATION, arc-rollout-DESIGN]
upstream: null
---

> **Feature**: ARC 升级实施批（PROGRESS P-035）
> **创建日期**: 2026-09-09
> **状态**: accepting
> **Spec 步骤**: Step 7
> **基于实施**: [IMPLEMENTATION.md](./IMPLEMENTATION.md) v1.0

## 1. 规避矩阵验收（DESIGN 1.2 对应）

| # | 规避项 | 判据 | 结果 |
|---|--------|------|------|
| E1 | skill 崩溃规避 | `arc_wrap.py skill` exit 2 拦截（白名单外）| ✅ 实测（13940 行 stack trace 未触发）|
| E2 | 版本失配规避 | `arc_wrap.py version` 输出事实源指针 exit 0；`arc.exe --version` 不复测为版本依据 | ✅ |
| E3 | linux bun 规避 | 基准 Windows 二进制（win32-x64，sha256 一致）| ✅ |
| E4 | import 关系空规避 | 预链接脚本补 7 条 depends_on 边 | ✅ |
| E5 | link 方向语义规避 | 实测校准：decision→decision = depends_on / decision→requirement = driven_by 两方向映射表入脚本 | ✅ |
| E6 | breaking change 规避 | 版本固化 = 0.8.0 sha256 登记 + 90 天观察项（README）| ✅ |

## 2. 功能验收（DESIGN §4）

| # | 验收项 | 判据 | 结果 |
|---|--------|------|------|
| A1 | 白名单生效 | init/add/list/check/next/context/trace/impact/link/import 全部 exit 0；skill/bogus exit 2 | ✅ 实测 |
| A2 | sha256 固化 | arc.exe sha256 = 登记值 8f4b3089...（官方一致）| ✅ Get-FileHash |
| A3 | ADR 导入 | 8 个 ADR 全部导入成功（D-001~D-008 中文保真）| ✅ |
| A4 | 预链接 | 7 条 depends_on 边链接成功（依赖簇正确）| ✅ |
| A5 | trace 递归 | D-008 trace ≥2 跳（D-008→D-004→D-003→...）| ✅ |
| A6 | impact 影响面 | D-004 impact 含 D-006/D-007/D-008 | ✅ |
| A7 | check 健康 | 8 实体 7 关系，0 断链（orphan 为 decision-only 结构性语义，§6）| ✅ 理解性通过 |
| A8 | 零 hook 改动 | pre-commit / 三校验器 / spec_runner 零改动 | ✅ |

## 3. ADD Phase 0 质量门

| # | 门 | 判据 | 结果 |
|---|----|------|------|
| G1 | 零依赖不变式 | 封装器/预链接 = stdlib only；ARC 二进制为外部工具非依赖 | ✅ |
| G2 | I-2 临时目录 | probe/npm_tmp 清理；arc.exe gitignore | ✅ |
| G3 | 单向依赖 | tools/arc/ 依赖仓根 adr/ 读取；无反向依赖 | ✅ |
| G4 | 生成端自由/验证端受控 | ARC 图不接 hook/校验器，仅辅助查询 | ✅ |

## 4. 回归与纪律

| # | 项 | 结果 |
|---|----|------|
| R1 | 三校验器全绿（dc / m7 / repo_stats）| ✅ |
| R2 | pre-commit 四 hook 通过（提交时执行）| ✅ |
| R3 | 决策流 specwf-p035-20260909 五步链 step-gate --expect exit 0 | ✅ |
| R4 | verify-anchor 锚点真实 | ✅ |
| R5 | 零新增 M7 样本（本批复测 = 外部工具行为取证，无本仓声明错误）| ✅ |

**验收统计**: 规避 E1-E6 全部通过；功能 A1-A8 全部通过；质量门 G1-G4 全部通过；回归 R1-R5 全部通过。

---

**Review 签字**: _________ 日期: _________