# 验收清单：drift-gate 缺口报告（repo_stats「意图→证据→缺口」定位对账）

---
id: drift-gate-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-09
depends: [drift-gate-IMPLEMENTATION, drift-gate-DESIGN]
upstream: null
---

> **Feature**: drift-gate 实施批（PROGRESS P-029）
> **创建日期**: 2026-09-09
> **状态**: accepting
> **Spec 步骤**: Step 7
> **基于实施**: [IMPLEMENTATION.md](./IMPLEMENTATION.md) v1.0

## 1. 功能验收

| # | 验收项 | 判据 | 结果 |
|---|--------|------|------|
| A1 | gap 字段采集 | rs-decl/树缺登幻影/§9 缺行幻影/doc_registry 版本失配结果携带非空 gap | ✅（F21 覆盖）|
| A2 | gap-report 输出 | version ≥2 且存在缺口 → `[gap-report]` 块含三元组明细 + 载体分布 | ✅（F22 覆盖）|
| A3 | 版本门控 | version=1 时缺口在场但不输出块（激活前能力不泄漏）| ✅（F23 覆盖）|
| A4 | version 解析 | stats 块 `pattern_lib_version=2` 读通 | ✅（F24 覆盖）|
| A5 | 静默正确 | 激活后无缺口时直跑不输出 gap-report（零噪音）| ✅（直跑实测）|
| A6 | 退出码兼容 | P1/P2→1、P3→0 不变；gap-report 不改变既有阻断语义 | ✅（行为兼容实测）|

## 2. ADD Phase 0 质量门

| # | 门 | 判据 | 结果 |
|---|----|------|------|
| G1 | 不变式 I-1（v1.0）| 「零实现」已随 v1.1 实施批闭环——本批为过渡面落地，不新增运行时依赖 | ✅ |
| G2 | 不变式 I-2 | 全部事实锚回 CER E1/E4，零新增外部 A/B 断言 | ✅ |
| G3 | 不变式 I-3 | 实施单向依赖 repo_stats 既有架构，无反向依赖 | ✅ |
| G4 | 不变式 I-4 | 激活 = pattern_lib_version 2 声明 + 工具门控双绑定，无触发不输出 | ✅ |

## 3. 回归与纪律

| # | 项 | 结果 |
|---|----|------|
| R1 | selftest 27/27（含 F21-F24）| ✅ |
| R2 | 三校验器全绿（dc / m7 / repo_stats）| ✅ |
| R3 | pre-commit 四 hook 通过（提交时执行）| ✅ |
| R4 | 决策流 specwf-p029-20260909 五步链 step-gate --expect exit 0 | ✅ |
| R5 | verify-anchor 锚点真实 | ✅ |
| R6 | 零新增 M7 样本（无新缺陷发现）| ✅ |

**验收统计**: 功能 A1-A6 全部通过；质量门 G1-G4 全部通过；回归 R1-R6 全部通过。

---

**Review 签字**: _________ 日期: _________