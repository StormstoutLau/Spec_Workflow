# DEV-LOG-020: ADR-0008 front-matter 状态回写（P-053：proposed → accepted）

> **日期**: 2026-09-29（回补）
> **会话**: `specwf-p053-20260929`（五步链，**补建**：五条 decision 均标【补建】，依该批 commit 与 PROGRESS P-053 行回溯重建）
> **涉及**: `adr/ADR-0008-spec-process-review-gate-and-bidirectional-check.md`（front-matter + 元数据表 + 「决策（Decision）」节标题 + 修订历史）· `spec/drift-gate/RESEARCH.md`（§4.4.2（三）同族登记表 + §4.4.3）· `docs/PROGRESS.md`（P-053 行）· `CODE_WIKI.md`（v1.77 → v1.78）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-053 行](../PROGRESS.md) · [ADR-0008](../../adr/ADR-0008-spec-process-review-gate-and-bidirectional-check.md) · [drift-gate RESEARCH §4.4](../../spec/drift-gate/RESEARCH.md) · [docs/adr/README](../../docs/adr/README.md) · [ADR-0007](../../adr/ADR-0007-unified-document-contract.md) · [cpp-hub-absorption IMPLEMENTATION](../../spec/cpp-hub-absorption/IMPLEMENTATION.md) · [CODE_WIKI](../../CODE_WIKI.md)

## 做了什么（时序）

1. **定位 = 回写欠账（非待裁决）**：ADR-0008 front-matter 停 `v1.0/proposed`，但其**实际状态已是 accepted** —— 属 P-052 观察项「声明 ≠ 制品状态」的**第 4 实例**。
2. **四方佐证一致**：① 本 ADR **自身修订历史**（2026-08-17 行）已记 `proposed → accepted`（v1.0 → v1.1、`depends` 增补 ADR-0007）；② `docs/adr/README.md`；③ `adr/ADR-0007` 附录 A；④ `spec/cpp-hub-absorption/IMPLEMENTATION.md`（commit `8ea38bf`「ADR-0007 v1.1 + ADR-0008 v1.1 定版」）。且 `SPEC_PROCESS` v1.4 已按 **D4 / D6** 生效。
3. **处置（front-matter 回写）**：`version 1.0 → 1.1` / `status proposed → accepted` / `depends` 补 `ADR-0007`（兑现其 v1.1 记录的增补）/ `date → 2026-09-29`；正文**元数据表「状态」行**与**「决策（Decision）」节标题**同步；**修订历史补回写行**（含四方佐证）。
4. **同批追加**：`spec/drift-gate/RESEARCH.md` **§4.4.2（三）**同族登记表补**第 4 实例**（ADR-0008 front-matter 欠账）+ **§4.4.3** 增第 5 条 ⇒ RESEARCH **v1.1 → v1.2**。
5. **性质 = adr-only 批次**：无 `spec/` 四文档改动 ⇒ `step-enforce` **不触发**（同 P-048 先例）；零代码。
6. **收束**：`docs/PROGRESS.md` P-053 行 + `CODE_WIKI` **v1.77 → v1.78**（banner + §2.1 树 + §9，含 drift-gate RESEARCH v1.2 同步 + §10 `declared.progress_tasks` 52 → 53 + PT-11 两处）。

## 决策依据

### ① 定性为「制品 front-matter 回写欠账」，而非「未生效」

四方佐证 + 本 ADR 自身修订历史**均记已 accepted**，且 SPEC_PROCESS v1.4 已按 D4/D6 生效 ⇒ 制品状态客观已是 accepted，欠的只是 front-matter 回写。故**无待裁决事项**，处置只剩「回写」一途（源：PROGRESS P-053 行 / session `research` 步）。

### ② 归入 P-052 观察项「第 4 实例」并同批登记

本处与 P-052 三处 CHECKLIST 回写欠账**同族**（「声明 ≠ 实物状态」）⇒ 于 `drift-gate/RESEARCH.md` §4.4.2（三）同族登记表**追加第 4 实例**（用户指令「先把 ADR-0008 补进 drift-gate §4.4 的同族登记表再提交」）；登记与回写**同批落档**（源：PROGRESS P-053 行）。

### ③ `depends` 补 `ADR-0007` 而非新造

其 v1.1 修订历史早已记录「depends 增补 ADR-0007」，回写只是**兑现既有记录**；不改 DC1 七字段结构（源：PROGRESS P-053 行 / ADR-0008 元数据表）。

## 遇到的问题

- **session 为补建**：原批未留决策事件流，`specwf-p053-20260929.jsonl` 五条 decision **均标【补建】**（依该批 commit `fa50fb8` 与 PROGRESS P-053 行回溯重建，`ts` 取批次日期，**不追溯勾销原记录**）⇒ 控制台方才可见该轮（同族先例 = P-042 v1.17 的 V2a 补建）（源：session 首步「【补建】」标注）。
- **adr-only 批次的 `step-enforce` 语义**：因无 `spec/` 四文档改动而不触发，须显式说明其「未触发」是**预期**而非漏跑（同 P-048 先例）（源：session `implement` 步）。

## 下一步

- **无新增待办**：P-053 为一次性状态回写批，闭环。
- **观察项同族登记表**已递增至第 4 实例；该观察项自身的激活评估落于 `drift-gate/RESEARCH.md` §4.4.4（属 P-054，不在本份范围）。
- **零新增 M7 样本**；`declared` 无新 feature 目录 / 新脚本 / 新 hook（源：PROGRESS P-053 行）。