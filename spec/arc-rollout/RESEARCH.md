---
id: arc-rollout-RESEARCH
type: design
version: 1.0
status: in-review
date: 2026-09-09
depends: [arc-probe-RESEARCH, community-ecosystem-RESEARCH, FWK-DECISION-RECORD]
upstream: null
---

# 调研文档：ARC 升级实施（吃狗粮模式，P-035）——调研输入引用

> **Feature**: ARC（kegesch/arc 0.8.0）决策图谱升级实施
> **创建日期**: 2026-09-09
> **状态**: in-review（审查中）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「按照吃狗粮模型执行ARC 升级 规避缺陷」——P-034 C-6 保留裁决触发实施

## 1. 调研输入（复用，零新增调研）

本批为**实施批**（非调研批）——完整调研已在 P-031~P-034 四批闭环，本批引用既有结论作为实施设计输入：

| 调研批次 | 结论 | 引用 |
|---------|------|------|
| P-031（arc-probe v1.0） | Windows 命令面实态可用 + 平台缺陷双实证 + H2 部分证伪 | [arc-probe RESEARCH](../arc-probe/RESEARCH.md) §3.1-3.4 |
| P-032（arc-probe v1.1） | 6 候选全景无完全替代，ARC 保持主选 | §3.6 |
| P-033（arc-probe v1.2） | 加权评分 ARC 升级 4.2 显著最优 | §3.7 |
| P-034（arc-probe v1.4） | 规避矩阵收敛缺陷面至可接受 + A-11 事实修正（driver 已发布） | §3.8 |
| CER v1.16 | ARC 行评估已执行，采用资质确认待裁决 | [CER §3.4.1](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) |

## 2. 实施设计输入（规避矩阵摘录）

[arc-probe RESEARCH §3.8](../arc-probe/RESEARCH.md) 已定义规避矩阵 6 行：
1. `arc skill` 崩溃 → 命令白名单排除
2. `arc --version` 失配 → 不信 CLI 版本，用 sha256 + tag
3. linux bun 缺失 → 基准平台 Windows
4. import 关系空 → 预链接脚本按 FWK-DECISION-RECORD 补
5. link 方向语义 → 预链接方向映射表
6. 0.x breaking → 版本固化 0.8.0 + 90 天观察项

## 3. 断言统计表

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 0 | 实施批零新增外部事实（复用 arc-probe 既有 A-1~A-22） |
| B 推断类 | 0 | 实施批零新增推断 |
| C 判断类 | 0 | 实施批零新增判断（裁决已由 P-034 C-6 做出） |

A/B/C 计数 = 0/0/0，H = 0。本批为实施批，断言计数留空（引用既有调研）。

## 4. 结论

实施输入完整（规避矩阵 + 选型对比 + 主选确认），进入 DESIGN 步（[DESIGN v1.0](DESIGN.md)）。

**Review 签字**: _________ 日期: _________