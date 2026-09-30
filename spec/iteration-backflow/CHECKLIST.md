# 验收清单：迭代回写形态件（四元登记块 / 决策矩阵模板 / 净收敛纪律）

---
id: iteration-backflow-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-30
depends: [iteration-backflow-IMPLEMENTATION, iteration-backflow-DESIGN]
upstream: null
---

# 验收清单：迭代回写三处缺口落地批（P-058）

> **Feature**: 迭代回写形态件（`spec/iteration-backflow/`）
> **被验收物**: [DESIGN v1.0](./DESIGN.md) + [IMPLEMENTATION v1.0](./IMPLEMENTATION.md)
> **Spec 步骤**: Step 7-8
> **v1.0 变更（P-058，用户指令「处理§7.19 迭代回写三处缺口（四元登记块 / 决策矩阵模板 / 净收敛纪律，Layer-0）」+ 三项裁决）**: 首次落档。验收面 = **三件形态件**（件 A 四元登记块 / 件 B 决策矩阵模板 / 件 C 净收敛纪律 + Type-1/2 委派）的**形态落地 + 声明同步 + 边界成立**（**零代码 / 不新增 RULE 编号 / 不接门禁**）。

## 1. 文档一致性验收（Step 8）

- [x] **RESEARCH §0 计数 ↔ 附录 A / 附录 B / 附录 C 四段一致**（A **5**（`【A】` 标记 5 条）/ B **2**（附录 B 机读条目 `"id": "B1"`、`"id": "B2"`）/ 假设区 **2**（`[H1]`、`[H2]`）；C 类 3 条为散文复盘，无机械计数）
- [x] **IMPLEMENTATION §0 计数 ↔ §3 标记一致**（A **3** ↔ `【A】` 标记 3 条；B / C / 假设区声明 **0** 且正文零相应标记）
- [x] **三处形态表述同向**（**SPEC_PROCESS 新节 ↔ RESEARCH_TEMPLATE §6.4 / DESIGN_TEMPLATE §11 ↔ DECISION_MATRIX_TEMPLATE**）——「四元字段名与顺序固定」「净收敛纪律两分支」「Type-1/2 委派」三处**逐项一致，无一处另造形态**
- [x] **DESIGN D1-D6 ↔ IMPLEMENTATION §1 落地清单 ↔ §2 逐项实施 三段可追溯**（无「设计了未实现」项）
- [x] **不变式 I-1~I-6 全部有对应验收项**（见 §4）
- [x] **单一权威（I-2）成立**：件 A / 件 C 形态权威**只在 `SPEC_PROCESS`**；件 B 权威**只在矩阵模板**；两模板**只引不复制**（模板内无四元形态全文的复制体——**副本形态示例除外**，其为「就近骨架」而非权威定义）
- [x] **承前一致**：本批**承 [P-042 §7.19](../project-console/RESEARCH.md)** 三处缺口登记并兑现其**触发条件①「用户裁决」**；**不回改** P-042 正文（其「本批不实施」为当时准确记述）

## 2. 功能验收

| # | 验收项 | 结果 |
|---|--------|------|
| **F1** | **件 A 四元登记块落 `SPEC_PROCESS`**：四元**字段名与顺序固定**（判据 / 触发条件 / 当前倾向 / 证据等级）+ 表形态合法 + 就近骨架指向两模板 | ✅ 落 [`SPEC_PROCESS.md`](../../SPEC_PROCESS.md)「迭代收敛与未决项登记」节（`version 1.4 → 1.5`）；「触发条件」条**显式要求可机械识别**（承 P-042 B15） |
| **F2** | **件 C 净收敛纪律 + Type-1/2 委派 + 反模式 + 诚实边界**落 `SPEC_PROCESS` | ✅ 四条齐备：净收敛（关闭 ≥1 / 新开 ≥1 且必带触发条件，否则**不予立项**）/ Type-1/2 表（含矩阵模板指针）/ 反模式（分析瘫痪 + criteria gaming）/ 诚实边界（**过程性、不可机械拦截**） |
| **F3** | **件 B 决策矩阵模板新建**：选项 × **七维度逐行固定** + 每格 `评估（证据等级；读数日期）` + **收敛出口必填** + **Type-1/2 判定必填** + **R7 同构条款** | ✅ 新建 [`spec/templates/DECISION_MATRIX_TEMPLATE.md`](../../spec/templates/DECISION_MATRIX_TEMPLATE.md)（三节必填齐备；含「不得以『还需更多维度』收尾」硬约束） |
| **F4** | **两模板就近骨架**：`RESEARCH_TEMPLATE` §6.4 + `DESIGN_TEMPLATE` §11（**只引不复制**） | ✅ 两节均引 `SPEC_PROCESS` 权威定义与矩阵模板路径；DESIGN §11.2 明确「Type-2 **不启动**矩阵」 |
| **F5** | **不新增 RULE 编号**：`rules` 机读块**零改动**、**无 RULE-7** | ✅ `SPEC_PROCESS` 文末 ```rules``` 块内容**逐字未变**（RULE-1~6）⇒ **不触 DC4 命名空间扩权、无需 ADR** |
| **F6** | **零代码边界**（I-1）：`scripts/` 与 `tools/` **零变更**；**不新增**门禁 / hook / 依赖；`ANCHOR_RE` 等既有判定零改动 | ✅ 见 §8 复跑记录「零代码声明核对」（A-3） |
| **F7** | **治理同步**：`declared`（`spec_feature_dirs 36` / `templates 6` / `progress_tasks 58`）+ `doc_registry`（+1）+ `facade_baseline`（`fs.templates 6`）+ `README.md` / `README.en.md` 模板计数三处 + §2.1 树 + §9 三行 | ✅ 见 §8（`repo_stats` **0 违规、P3 0**；新增模板牵动 **PT-7A/7B/7C/7D 四类模式 × 三载体**，逐处同步，A-2） |
| **F8** | **立项即登记**（V1a 首个活实例，机械边界 **P 编号 ≥ P-058**）：开工**先写 `pending`**，收尾回填 `done` | ✅ `PROGRESS` **P-058 行**：立项时 `pending`（本 session 首步之前落档）→ 收尾 `done` + 验收标准 + 追记；**过渡期如实登记 = 现形态下人写 2 次**（`pending` → `done`；`done` 尚非机器派生，待 P2b） |

## 3. 接口验收

| 接口 | 形态 | 结果 |
|------|------|------|
| 四元块（文档形态） | 块形态（四行 bullet）与表形态（四列）**皆合法** | ✅ `SPEC_PROCESS` 明示两种承载；两模板给块形态骨架 |
| 矩阵模板（文件形态） | front-matter 合 **DC1 七字段** + **DC2 词表**（`type: design` / `status: draft`） | ✅ `dc_validator` **0 违规**（含模板文件） |
| 纪律条文（宪法形态） | 独立节 + 版本 bump；**不入 RULE 编号空间** | ✅ `version 1.5`；`rules` 块零改动（F5） |

## 4. 不变式验收

| # | 不变式 | 结果 |
|---|--------|------|
| **I-1** | 零代码（Layer-0）：不改 `scripts/` 与 `tools/`、不改任何校验器、不新增门禁 / hook | ✅ §8 零代码声明核对通过 |
| **I-2** | 单一权威：件 A / 件 C 权威只在 `SPEC_PROCESS`；件 B 权威只在矩阵模板；其它位置只引不复制 | ✅ §1 第 6 项一致性检查通过 |
| **I-3** | 声明 = 重数（R7 同构）：矩阵格内含计数 / 占比须可复算 | ✅ 模板 §1 明示「须附复算命令；无法复算者不得入格」并给复算示例 |
| **I-4** | 诚实边界：可机械核仅形态完备性 | ✅ `SPEC_PROCESS` 与模板 §5 **逐字同向**声明 |
| **I-5** | 不触 DC4：不新增 RULE 编号、不动 `rules` 块 | ✅ F5 |
| **I-6** | 触发条件须可机械识别 | ✅ 四元「触发条件」与矩阵「收敛出口」均明文要求（承 P-042 B15 / DR-20） |

## 5. 错误处理与边界验收

| 情形 | 处置 | 结果 |
|---|---|---|
| 某轮未满足净收敛 | **不予立项**（人工裁决）；**不设自动阻断** | ✅ 条文如此；无门禁（I-1/I-4） |
| 未决项只有倾向、无触发条件 | 视为**形态残缺**，登记待补；**不阻断任何机械流程** | ✅ `SPEC_PROCESS` 与模板 §5 同向 |
| 矩阵格内计数无法复算 | **不得写入**格内 | ✅ 模板 §1 + I-3 |
| 纪律被**形式化满足**（凑数） | 属**已知盲区**（RESEARCH H1），触发 = 出现一次实例或观察窗 ≥3 批后复核 | ✅ 登记于 §9 |

## 8. 验收结论与复跑记录

**P-058 复跑（2026-09-30，本机实测；迭代回写形态件 · Layer-0，**零代码**）**:

| 命令 / 核对 | 结果 |
|------|------|
| `python scripts/dc_validator.py` | **0 违规**（含新建四文档 + 新建模板）——RESEARCH §0 声明 **5A / 2B / 2H**、IMPLEMENTATION §0 声明 **3A / 0B / 0C / 0H** 均与机械重数一致 |
| `python scripts/repo_stats.py` | **0 违规、P3 0**——`declared`（`spec_feature_dirs 36` / `templates 6` / `progress_tasks 58`）+ §2.1 树（新增 `iteration-backflow/`）+ §9 三行 + `doc_registry`（`iteration-backflow` → `spec/iteration-backflow/DESIGN.md` v1.0 令牌）+ `facade_baseline` 两载体 `fs.templates 6` |
| `python scripts/m7_stats.py` | **0 违规**（**零新增样本**——本批不涉证据账本） |
| `python tools/spec_runner/spec_runner.py selftest` | **47/47 PASS**（**零改动复跑一致**——本批不改 `spec_runner`） |
| `python scripts/console_gen.py --selftest` | **41/41 PASS**（零改动复跑一致）；`--check` = **与源一致 exit 0**（P 行 58 入源后由 hook 重生成） |
| `spec_runner step-gate --session <本批 session> --expect research design implement verify finalize` | **决策链一致 pass → exit 0**（5/5 步） |
| `spec_runner verify-anchor --session <本批 session>` | 锚点**全真实 → exit 0** |
| `spec_runner step-enforce --pid P-058` | **exit 0**（session 定位本批，5/5 步） |
| **零代码声明核对（A-3）** | `git status`：`scripts/` 与 `tools/` **零变更**；本批改动面 = `SPEC_PROCESS.md` + `spec/templates/`（新建 1 + 扩 2）+ 本 feature 四文档 + `CODE_WIKI` + `README.md` / `README.en.md` + `PROGRESS` + 本 session；**无新依赖 / 新门禁 / 新 hook**；**无 push**（待用户裁决） |
| **模板计数与目录数同步（A-2 / F7）** | `spec/templates/` 实为 **6 个 `.md`**（`declared.templates = 6`）；`spec/` feature 目录（排除 `templates`）实为 **36**（`declared.spec_feature_dirs = 36`）；`PROGRESS` P 行 **58**（`declared.progress_tasks = 58`）；`README.md` / `README.en.md` 模板计数三处同步（PT-7B/7C/7D 全绿） |

## 9. 后续行动

- **H1（净收敛纪律有效性）待触发**：纪律可被**形式化满足**（凑「关闭一项」或给虚假触发条件）；触发 = 出现一次形式化凑数实例，或观察窗 ≥3 批后复核。
- **H2（七维度矩阵诱发分析瘫痪）待触发**：全维度填写成本可能反而拖延决策；当前缓解 = **Type-1/2 委派**（可逆项不启动矩阵）；触发 = 首次真实启用矩阵后评估。
- **DC4 扩权候选（未激活）**：若日后需为纪律追加 `id` / 失效条件 / 拦截记录（即「规则化」），须**另立 ADR** 走 DC4 命名空间扩权（本批**显式不走**，代价已登记于 RESEARCH C-3）。
- **本批唯一有形产物** = `SPEC_PROCESS v1.5` 新节 + `DECISION_MATRIX_TEMPLATE.md` + 两模板两节；**无工具面后续**。

---

**验收签字（P-058 / 迭代回写形态件 · Layer-0，**零代码**）**: 自查（`dc_validator` **0 违规**（含新建四文档 + 新建模板）/ `repo_stats` **0 违规、P3 0**（`declared` 36 / 6 / 58 + 树 + §9 三行 + `doc_registry` + `facade_baseline` 同步）/ `m7_stats` **0 违规**（零新增样本）/ `spec_runner selftest` **47/47**（零改动复跑）/ `console_gen --selftest` **41/41** + `--check` 一致 / `step-enforce --pid P-058` **exit 0**（5/5 步）/ `verify-anchor` 锚点全真实 / **`scripts/` 与 `tools/` 零变更**（零代码声明成立））；**F1~F8 全部实测 ✅**；**不新增 RULE 编号**（`rules` 块零改动 ⇒ 无需 ADR）） 日期: 2026-09-30