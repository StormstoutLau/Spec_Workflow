# DEV-LOG-021: drift-gate §4.4 观察项激活裁决——方向 A 显式否决、方向 B 落 AGENTS.md 弱纪律

> **日期**: 2026-09-29（回补）
> **会话**: `tools/spec_runner/sessions/specwf-p054-20260929.jsonl`（首步明示【补建】，依该批 commit `d7f1c85` body 与 PROGRESS P-054 行回溯重建）
> **涉及**: `spec/drift-gate/RESEARCH.md`（v1.2 → v1.3，§4.4.4）/ `AGENTS.md`（禁止事项第 7 条）/ `docs/PROGRESS.md`（P-054 行）/ `CODE_WIKI.md`（v1.78 → v1.79）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-054](../PROGRESS.md) / [drift-gate RESEARCH §4.4.4](../../spec/drift-gate/RESEARCH.md) / [AGENTS.md](../../AGENTS.md) / `tools/spec_runner/sessions/specwf-p054-20260929.jsonl`

## 做了什么（时序）

1. **触发**：用户指令「执行 drift-gate §4.4 是否激活任务」→ 裁决「采判定：A 否决 / B 激活」+「复核无误后落档」。背景 = [drift-gate RESEARCH §4.4](../../spec/drift-gate/RESEARCH.md) 已登记「制品状态一致性看护」观察项（P-052 立），其触发条件①（同类复现 ≥1 例）**已达阈值（4 实例）**。
2. **ADR-0010 三问机械复核（E1）**：Q1 分层 —— 方向 A（`repo_stats` 扩 status 一致性）= **Layer-1**；方向 B（弱纪律）= **Layer-0**。
3. **Q2 激活条件复核（方向 A 否决的两条实证）**：复核① `repo_stats` 现有模式的 truth 键**全为 `fs.` / `hits.` / `derived.`（计数 / 百分比，零语义比对）**；复核② `doc_registry` **每 feature 仅 1 条**（31 条）⇒ 漂移的三份 `CHECKLIST_FUNC` / `CHECKLIST` **不在覆盖面**。
4. **Q3 未激活副作用 = 0**（方向 A 本未实现；方向 B 纯文档）。
5. **判定**：方向 A **显式否决**（理由就此固化，免未来重复评估）；方向 B **激活** ⇒ 弱纪律落 [AGENTS.md](../../AGENTS.md) 禁止事项**第 7 条**（仿 DIS-008 规则化先例）。
6. **落档**：[drift-gate RESEARCH §4.4.4](../../spec/drift-gate/RESEARCH.md)（v1.2 → **v1.3**）+ AGENTS.md + CODE_WIKI **v1.78 → v1.79**（banner + §2.1 树 + §9 + `declared.progress_tasks` 53 → 54 + PT-11 两处）。
7. **校验**：三校验器全绿；**零新增 M7 样本**。

## 决策依据

### ① 为什么方向 A 被否决

三条理由（源 = §4.4.4）：**定形判据** —— 建 Layer-1 等于对**散文**（§9 行 / PROGRESS 行 / ADR 索引行）做**双侧语义比对** + bespoke 模式，而 status 声称面**无定形**，违反本仓判据「**有定形 + 有机械数据源 ⇒ 补位点；无定形 ⇒ 只立纪律**」；**覆盖面 E1 实证** —— 上述复核① / 复核②；**撞 I-10 语义同源**（同 P-051 候选的显式否决理由）。另有**即时性理由** = 4 实例的即时根因均已闭环（3 例 = DC2 判别规则过窄 → P-052 扩宽；1 例 = 人工疏忽 → P-053 回写；1 例 = 声明错误 → 已订正），且 **P-052 / P-053 后零新增**。

### ② 为什么方向 B 落 AGENTS.md 而非新增 ADR

方向 B 为 **Layer-0 纯文档弱纪律**，载体选 `AGENTS.md` 禁止事项（**仿 DIS-008 规则化先例**），**不新增 ADR**；纪律文本 = 「制品状态变更（`status` / `version` / `depends` 等）必须同步 front-matter，且与对外声称（`PROGRESS` 行 / `CODE_WIKI §9` 行 / ADR 索引行）保持一致」。

### ③ 已知快照滞后为什么登记为「快照」而非「缺口」

[hook-surface §3.5](../../spec/hook-surface/RESEARCH.md) 与 [CER §3.5](../../spec/community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) 的「禁止事项 **6 条**」为**时点快照**（原文自带「全量原文核对，**2026-09-09**」时点）⇒ 新增第 7 条后**不追改**，如实登记（同 README 门面 `as_of` 快照模式）。

## 遇到的问题

- **已知快照滞后（本批不追改）**：hook-surface §3.5 / CER §3.5 的「禁止事项 6 条」与新增第 7 条产生已知差异；按「快照非缺口」处置，**不追改**。
- **不做的事**：本批**未碰** `repo_stats` / 未新增校验器 / 未新增门禁；方向 A 的否决是**登记级**结论，非工具变更。

## 下一步

- 方向 B 弱纪律**已生效**（不等触发）；方向 A 否决理由**已固化**，不再重复评估。
- 观察项本体（§4.4）状态 = **已闭环**（方向 A 否决 / 方向 B 激活）。