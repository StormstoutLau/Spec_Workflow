# DEV-LOG-019: 制品状态漂移治理（P-052：三处机械复核 + DC2 判别规则扩宽 + 一致性观察项登记）

> **日期**: 2026-09-29（回补）
> **会话**: `specwf-p052-20260929`（五步链）
> **涉及**: `scripts/dc_validator.py`（M2 DC2 判别由 id 后缀扩宽为 id 含 `CHECKLIST` 段）· `spec/doc-contract/PLAN.md`（§1 DC2 v1.6 → v1.7）· `spec/step-gate/CHECKLIST_FUNC.md` · `spec/defect-fixes/CHECKLIST_FUNC.md` · `spec/independent-verify/CHECKLIST.md`（及同 feature DESIGN / RESEARCH）· `spec/drift-gate/RESEARCH.md`（§4.4 观察项）· `spec/precommit-dc-validator/IMPLEMENTATION.md`（§8.1 fixture 表）· `docs/PROGRESS.md`（P-025 版本声称订正 + P-052 行）· `CODE_WIKI.md`（v1.76 → v1.77）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-052 行](../PROGRESS.md) · [drift-gate RESEARCH §4.4](../../spec/drift-gate/RESEARCH.md) · [dc_validator.py](../../scripts/dc_validator.py) · [PLAN.md](../../spec/doc-contract/PLAN.md) · [step-gate CHECKLIST_FUNC](../../spec/step-gate/CHECKLIST_FUNC.md) · [defect-fixes CHECKLIST_FUNC](../../spec/defect-fixes/CHECKLIST_FUNC.md) · [independent-verify CHECKLIST](../../spec/independent-verify/CHECKLIST.md) · [precommit-dc-validator IMPLEMENTATION](../../spec/precommit-dc-validator/IMPLEMENTATION.md) · [CODE_WIKI](../../CODE_WIKI.md)

## 做了什么（时序）

1. **三处状态漂移机械复核（结论 = 以 PROGRESS / CODE_WIKI 为准）**：① `spec/step-gate/CHECKLIST_FUNC.md`（front-matter `v1.0/draft` vs 声称 v1.1 accepting —— **铁证 = 该文件 §8 修订历史自身记「v1.0 → v1.1：状态 draft → accepting」**）；② `spec/defect-fixes/CHECKLIST_FUNC.md`（`v1.0/draft` vs v1.0 accepting；§7 独立 pass 已签字）；③ `spec/independent-verify/CHECKLIST.md`（`v1.0/pending` vs v1.0 accepting；C1-C9 全 ✅）。三处均为**制品 front-matter 回写欠账**，非「未验收」。
2. **两项新增发现**：**(A)** PROGRESS P-025 声称 `spec_runner.py v1.4.0` 与代码 `VERSION` 常量 **1.3.0** 不符（`git log -S 'VERSION = "1.4.0"'` **零命中** ⇒ 1.4.0 从未存在）；**(B)** `independent-verify` 的 DESIGN / RESEARCH 仍 `draft` 而同 feature CHECKLIST **C8** 声称 `verified`。
3. **根因定位（DC 契约层新发现）**：两份 id（`step-gate-CHECKLIST-FUNC` / `defect-fixes-CHECKLIST-FUNC`）**不以 `-CHECKLIST` 结尾** ⇒ `dc_validator` M2 的 DC2 副轴判别（`id.endswith("-CHECKLIST")`）将其归为**一般设计文档**，其词表 `draft/in-review/verified/superseded` **无 `accepting`** ⇒ 独立 pass 后的状态回写**机械不可表达**（写入即 P1）——**非疏忽，是被判别规则挡住**。
4. **用户裁决「扩宽 DC2 判别规则」**：判别由 id **后缀** `-CHECKLIST` 扩宽为 id **含 `CHECKLIST` 段**（`"CHECKLIST" in id.split("-")`，取「段」非「子串」）；selftest **24/24 → 27/27**（**F19** 段判别 `accepting` 合法 / **F20** 段判别 `draft` 非法 / **F21** 段非子串 `x-FOOCHECKLIST` 走一般档）；契约文本 `PLAN.md` §1 DC2 **v1.6 → v1.7**。
5. **全部执行（回写）**：step-gate/CHECKLIST_FUNC **v1.0/draft → v1.1/accepting**（§8 补回写行）/ defect-fixes/CHECKLIST_FUNC **draft → accepting**（§8 补 promotion 行）/ independent-verify CHECKLIST **pending → accepting** / independent-verify DESIGN 与 RESEARCH **draft → verified** / PROGRESS **P-025 版本声称订正 v1.4.0 → v1.3.0**（附机械取证注）；`dc_validator` 全仓复跑 **127 文件 0 违规**。
6. **观察项正式登记**：落 `spec/drift-gate/RESEARCH.md` **§4.4**（v1.0 → **v1.1**）——落档调研结论表（5 项待裁定 → 确定结论）+ **七段式观察项**（登记缘由 E1 / 机制定性 / 同族登记表 / 触发条件 3 条 / 载体预判 / 未触发处置 / 边界声明）；同族实例补录 = `spec/precommit-dc-validator/IMPLEMENTATION.md` §8.1 fixture 表补 F19-F21 行（v1.2 → v1.3）。

## 决策依据

### ① 以 PROGRESS / CODE_WIKI 为准（背靠机械取证）

三处漂移均**背靠可复算铁证**：step-gate 那份 §8 修订历史**自身即记该 promotion**（文件内自相矛盾）；defect-fixes 与 independent-verify 各有独立 pass 签字闭环 ⇒ 制品 front-matter 落后、外部声称正确（源：`drift-gate/RESEARCH.md` §4.4.1）。

### ② 三方案权衡后选「扩宽 DC2 判别规则」

① 归一 id（改为以 `-CHECKLIST` 结尾）会变动 **DC1 稳定标识**；② 判其为一般设计文档写 `verified` 与「验收清单」语义不符且与声称冲突；③ **扩宽判别规则**最贴合「CHECKLIST 变体仍是 CHECKLIST 实例」语义，且 E1 实测全仓仅这 2 份 id 受影响 ⇒ **零迁移、零误伤**。改「段」判别（非「子串」）以免 `FOOCHECKLIST` 类 id 被误纳（源：PROGRESS P-052 行 ④）。

### ③ 观察项落 `drift-gate` 且预登记否决两处

观察项属主 = drift-gate（「声明 → 证据 → 缺口」对账层）。**预登记否决** = 不在 `dc_validator` 内解析 PROGRESS（跨契约耦合，撞 **I-10 语义同源**）。载体预判给两方向（方向 A `repo_stats` 扩 status / 方向 B Layer-0 弱纪律），本批**不实施**任一机制（源：`drift-gate/RESEARCH.md` §4.4.2（五）/（七））。

## 遇到的问题

- **机制定性 = 看护缺口（管辖空白），非工具 bug**：三者合力——`dc_validator` 管「状态是否合法」不管「是否与外部声称一致」；`repo_stats` drift-gate 只比 version 不比 status 且仅覆盖 `doc_registry` 已登记制品；`doc_registry` 每 feature 仅 1 条代表文档 ⇒ 两份 `CHECKLIST_FUNC` **完全逃逸**、三校验器却**全绿**（源：`drift-gate/RESEARCH.md` §4.4.2（一）/（二））。
- **第 1/2 项根因非疏忽**：是「规则文本 < 实际语义」的边界缺口（被 `id.endswith` 判别规则挡住）；此结论直接支撑「扩宽判别规则」而非「改 id」。
- **本批新证**：`precommit-dc-validator IMPLEMENTATION` §8.1 fixture 表滞后（声明 F1-F10 实为 F1-F21）——同类「声明未随实物更新」，已登记为同族实例并补 F19-F21 行（源：PROGRESS P-052 行 ⑥）。

## 下一步

- **观察项触发条件 3 条**：① 同类复现 ≥1 例（本批已 4 例，**达阈值**）② 出现由本缺口导致的误判 ③ 用户显式裁决。
- **激活评估**：本观察项的方向 A 否决 / 方向 B 激活裁决其后落于 `drift-gate/RESEARCH.md` **§4.4.4**（属 P-054，不在本份范围）。
- **零新增 M7 样本**；`declared` 无新 feature 目录 / 新脚本 / 新 hook（源：PROGRESS P-052 行 ⑦）。