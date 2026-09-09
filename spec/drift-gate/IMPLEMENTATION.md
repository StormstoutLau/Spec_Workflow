# 实施文档：drift-gate 缺口报告（repo_stats「意图→证据→缺口」定位对账）

---
id: drift-gate-IMPLEMENTATION
type: design
version: 1.0
status: verified
date: 2026-09-09
depends: [drift-gate-DESIGN, drift-gate-RESEARCH]
upstream: null
---

> **Feature**: drift-gate 实施批（PROGRESS P-029——P-023 Layer-0 概念登记的落地）
> **创建日期**: 2026-09-09
> **状态**: verified（selftest 27/27 + 三通道全绿）
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md) v1.1（§7 对实施的输入 / §9 实施追记）
> **基于调研**: [RESEARCH.md](./RESEARCH.md) v1.0
> **任务来源**: 用户指令「按照吃狗粮模式 继续执行」（drift-gate 实施裁决）+ 懒加载 gate 重审通过（Q1 Layer-1 / Q2 用户裁决激活 / Q3 行为兼容）

---

## 1. 实施概述

把 [DESIGN §6.1](./DESIGN.md#61-候选登记形态repo_stats-演进候选仅登记) 的演化候选（意图→证据→缺口闭环）落地为 repo_stats 工具层能力：
对账从「声明=重数」布尔通过/失败升级为**带定位信息的缺口报告**——每条数值/集合比对类违规携带「意图 → 证据 → 缺口」三元组，`pattern_lib_version ≥ 2` 时自动输出 `[gap-report]` 块（缺口明细 + 载体分布）。零新依赖、零新命令（沿用既有 verify 路径）、退出码语义不变（P1/P2=1 阻断 / P3=0 提示）。

## 2. 工程细节

### 2.1 技术栈与改造面

| 组件 | 变更 | 说明 |
|------|------|------|
| `scripts/repo_stats.py` `CheckResult` | +1 字段 | `gap: str \| None = None`（dataclass 尾部默认值，既有 14 处构造零改动） |
| `reconcile()` rs-decl | +gap 填充 | `意图(声明) {key}={declared} → 证据(重数) {actual} → 缺口 ±{差}（欠/过声明）` |
| `_reconcile_lists()` | +gap 填充 | 树缺登/幻影、§9 缺行/幻影、doc_registry 版本失配三类集合/数值对账 |
| `_gap_report(results)` | **新增** | 提取带 gap 结果 → `[gap-report]` 块 + 载体分布；无缺口返回空串 |
| `main()` | +门控 | `spec.pattern_lib_version >= 2` 时自动输出 gap-report（无缺口静默，零噪音） |
| `run_selftest()` | +4 用例 | F21-F24（见 §3） |
| `CODE_WIKI.md` §10 stats 块 | 1→2 | `pattern_lib_version`: 2 + drift-gate 激活注（声明=重数） |

### 2.2 关键设计决策

1. **缺口三元组 = 既有 message 的并行结构化层**：不重写 message（保持人工可读 + 既有阻塞语义），新增 gap 字段承载「意图→证据→缺口」定位语义——最小 diff、零回归。
2. **版本门控 = 声明与工具双绑定**：`pattern_lib_version` 2 既是 stats 块声明（文档侧）也是工具侧激活开关（`>=2` 才输出 gap-report）——防「声明了没实现/实现了没声明」的表演性漂移。
3. **静默即正确**：激活后无缺口不输出任何额外块——drift-gate 不产生噪音，仅在漂移存在时报告（SGE drift gate「阻塞性漂移才出声」语义）。

## 3. 兼容性验证

| 验证 | 结果 |
|------|------|
| `python scripts/repo_stats.py --selftest` | **27/27 全过**（原 23 + F21-F24：三元组捕获 / gap-report 块输出 / v1 门控不激活 / version 2 解析）|
| 三校验器回归 | dc 89 文件 0 违规 / m7 0 违规 / repo_stats 0 违规（P3 提示 8 为既有快照滞后项）|
| 行为兼容 | version 2 激活后直跑全绿 → 无缺口不输出 gap-report（默认路径输出与 v1 逐字节一致）|
| 只读性 | gap-report 纯 stdout 派生，无写入路径（沿用 I-1 只读断言，selftest 覆盖）|

## 4. 回归记录

- **selftest 首跑捕获自身缺陷**（证据注入有效性实证）：F21/F22 断言方向写反（declared=9 > actual=2 应为「过声明」，误写「欠声明」）→ 修正断言后全绿。
- **drift-gate 激活首跑即抓真实缺口（上线自证）**：`pattern_lib_version` 升 2 后首次直跑，`[gap-report]` 块捕获 **P2**——CODE_WIKI §9 索引 drift-gate 行首个版本 token 仍为 RESEARCH v1.0，与 DESIGN front-matter 1.1 失配（doc_registry 对账取行内首个 `v\d` token）；调整行内 token 顺序（DESIGN v1.1 前置）后归零。**该缺口的暴露与修复即 drift-gate 能力的首次真实生效**——激活即刻抓到「文档声明 vs 事实」漂移，修复后 gap-report 正确静默。
- **drift-gate 激活闭环**：CODE_WIKI stats 块 version 1→2 → repo_stats 直跑自动启用 gap 采集与输出 → 全绿静默验证激活链路 | 声明=重数 | 工具门控 | 一致。

---

**Review 签字**: _________ 日期: _________