# 实施文档：迭代回写形态件（四元登记块 / 决策矩阵模板 / 净收敛纪律）

---
id: iteration-backflow-IMPLEMENTATION
type: design
version: 1.0
status: draft
date: 2026-09-30
depends: [iteration-backflow-DESIGN, SPEC-PROCESS]
upstream: null
---

> **Feature**: 迭代回写形态件（`spec/iteration-backflow/`）
> **设计依据**: [DESIGN v1.0](./DESIGN.md)（D1-D6 + I-1~I-6 + 落点表）
> **Spec 步骤**: Step 5-6
> **本批范围**: 三件**形态件**落地 —— D1 载体 + D2 件 A + D3 件 B + D4 件 C + D5 纪律落点 + D6 零代码边界
> **v1.0 变更**: 首次落档。**本批**改 1 个宪法文档 + 1 个新建模板 + 2 个既有模板，并同步 3 处治理声明（`CODE_WIKI` / `README.md` / `README.en.md`）+ `PROGRESS`；**零代码**（`scripts/` 与 `tools/` 零变更、不改任何校验器、不新增门禁 / hook）

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 3 | A-1 落地实况（5 处落点逐项）/ A-2 声明同步点（模板计数与 feature 目录的机械看护面）/ A-3 边界复跑读数（零代码声明成立） |
| B 推断类 | 0 | 本批不新增（推断均在 RESEARCH 附录 B） |
| C 判断类 | 0 | 判定均在 RESEARCH §4 / DESIGN §3-§5 |
| 假设区 | 0 | 无（假设 H1/H2 属 RESEARCH 附录 C，本批不新开） |

## 1. 落地清单

| # | 文件 | 动作 | 设计依据 |
|---|------|------|----------|
| 1 | [`SPEC_PROCESS.md`](../../SPEC_PROCESS.md) | 新增「**迭代收敛与未决项登记**」节（件 A 权威定义 + 件 C 条文）；`version 1.4 → 1.5` + 修订行追加 | D2 / D4 / D5 |
| 2 | [`spec/templates/DECISION_MATRIX_TEMPLATE.md`](../../spec/templates/DECISION_MATRIX_TEMPLATE.md) | **新建**（件 B：选项 × 七维度 + 收敛出口 + Type-1/2 判定 + R7 同构条款） | D3 |
| 3 | [`spec/templates/RESEARCH_TEMPLATE.md`](../../spec/templates/RESEARCH_TEMPLATE.md) | 新增 `### 6.4 未决项登记（四元块）`（**只引不复制**） | D2 / I-2 |
| 4 | [`spec/templates/DESIGN_TEMPLATE.md`](../../spec/templates/DESIGN_TEMPLATE.md) | 新增 `## 11. 未决项登记（四元块）与决策矩阵`（**只引不复制**） | D2 / D3 / I-2 |
| 5 | 治理同步 | `CODE_WIKI.md`（§2.1 树 + §3.8 + §9 三行 + §10 `declared` / `doc_registry` / `facade_baseline`）+ `README.md` + `README.en.md`（模板计数三处）+ `docs/PROGRESS.md`（P-058 行） | D1 / §9 落点表 |

## 2. 逐项实施

### 2.1 件 A + 件 C：`SPEC_PROCESS.md` 新增独立节（D2 / D4 / D5）

- **位置** = 「**启动新 feature 的流程**」之后、「**规则登记（DC4）**」之前——**保持 `rules` 机读块为文末最后一块**（I-5）。
- **节内容** = ① **未决项登记（四元块）**（字段名与顺序固定：判据 / 触发条件 / 当前倾向 / 证据等级；表形态合法；就近骨架指向两模板）② **净收敛纪律**（关闭 ≥1 / 新开 ≥1 且必带触发条件，否则不予立项）③ **Type-1/2 委派**（含矩阵模板指针）④ **反模式** ⑤ **诚实边界**。
- **版本动作** = front-matter `version: 1.4 → 1.5`；banner「修订」行**追加** v1.5 段（**不删改历史修订段**）。
- **不新增 RULE 编号**、**不动** ```rules``` 块（I-5）⇒ 不触 DC4 命名空间扩权。

### 2.2 件 B：新建 `spec/templates/DECISION_MATRIX_TEMPLATE.md`（D3）

- **front-matter** 合 DC1 七字段 + DC2 词表：`id: DECISION-MATRIX-TEMPLATE` / `type: design` / `version: 1.0` / `status: draft` / `depends: [SPEC-PROCESS, iteration-backflow-DESIGN]`（与四件套模板同形）。
- **结构** = §0 何时启用（前置判据：Type-1 + ≥2 候选 + 会致返工）→ §1 矩阵本体（七维度逐行固定 + 每格 `评估（证据等级；读数日期）` + 复算示例）→ §2 **收敛出口（必填）** → §3 **Type-1/2 判定（必填）** → §4 反模式 → §5 诚实边界。
- **R7 同构条款** = 格内出现计数 / 占比时**须附复算命令**，无法复算者不得入格（I-3）。

### 2.3 件 A 就近骨架：两模板各增一节（D2 / I-2）

- `RESEARCH_TEMPLATE.md` 增 **§6.4**（置于 §6.3 风险 与 §7 参考文献 之间）。
- `DESIGN_TEMPLATE.md` 增 **§11**（置于 §10.2 与 文末签字行 之间）。
- 两节**均只引** `SPEC_PROCESS` 权威定义与矩阵模板路径，**不复制**四元形态全文（I-2 单一权威）。

### 2.4 治理同步（D1 落点 + §9 落点表）

| 位点 | 动作 |
|---|---|
| `CODE_WIKI` banner | `v1.99 → v1.100`（P-058 段前置，原 v1.99 段保留为「前批」） |
| `CODE_WIKI §2.1` 树 | `templates/` 行 `5 个标准模板` → **6 个标准模板**（+ `DECISION_MATRIX_TEMPLATE`）；新增 `iteration-backflow/` 行；`PROGRESS.md` 行 `P-001~P-057 / 57 项` → **P-001~P-058 / 58 项** |
| `CODE_WIKI §3.8` | 增 `DECISION_MATRIX_TEMPLATE` 表行（标注「辅助模板，不绑定单一 Step」） |
| `CODE_WIKI §9` | 增 **3 行** = `spec/iteration-backflow/`（首个版本令牌 = `DESIGN **v1.0**`，首个 `P-\d{3}` = **P-058**）+ `spec/templates/DECISION_MATRIX_TEMPLATE.md` + `docs/PROGRESS.md` 行计数同步 |
| `CODE_WIKI §10` | `declared`：`spec_feature_dirs 35 → 36` / `templates 5 → 6` / `progress_tasks 57 → 58`；`doc_registry` 增 `{"label": "iteration-backflow", "path": "spec/iteration-backflow/DESIGN.md"}`；`facade_baseline` 两载体 `fs.templates 5 → 6`（`as_of → 2026-09-30`） |
| `README.md` / `README.en.md` | 模板计数三处同步（树行 / 复制步 / 索引行）⇒ **PT-7B / PT-7C / PT-7D 全绿** |
| `docs/PROGRESS.md` | **新行 P-058**（**立项即登记 = V1a 首个活实例**：开工先写 `pending`，收尾回填 `done` + 验收标准 + 追记）；P-042 行追加**指针追记**（三处缺口已由 P-058 实施） |

## 3. 断言明细（本机实测）

【A】A-1: **落地实况**（本机实测，2026-09-30）——5 处落点**逐项完成**：① `SPEC_PROCESS.md` 新增节（`version 1.5`，`rules` 机读块**零改动**、**无 RULE-7**）；② `spec/templates/DECISION_MATRIX_TEMPLATE.md` **新建**；③ `RESEARCH_TEMPLATE.md` 增 §6.4；④ `DESIGN_TEMPLATE.md` 增 §11；⑤ 治理同步（`CODE_WIKI` / `README.md` / `README.en.md` / `PROGRESS`）。

【A】A-2: **声明同步点与机械看护面**（本机实测）——新增一个模板文件同时牵动**三处声明**：`CODE_WIKI §10 declared.templates`（**5 → 6**，由 **PT-7A** 看护）+ **`README.md` 两处**（PT-7B `(\d+) 个模板`）+ **`README.en.md` 两处**（PT-7C `(\d+) templates`）+ **`README.md` 索引行**（PT-7D 中文数字「份」）⇒ **单一 `declared` 值 × 四类模式 × 三个载体**；新增一个 feature 目录同时牵动 `declared.spec_feature_dirs`（**35 → 36**，`templates` 依枚举器语义**排除**）+ §2.1 树（rs-list 缺登）+ §9 索引行（rs-list 缺行 / 幻影）+ `doc_registry`（版本令牌对账）；新增一个 P 行牵动 `declared.progress_tasks`（**57 → 58**）+ `CODE_WIKI` 两处「P-001~P-057 / 57 项」prose（**PT-11**）。

【A】A-3: **边界复跑读数（零代码声明成立）**（本机实测）——`scripts/` 与 `tools/` **零变更**；`spec_runner selftest` **47/47**（零改动复跑一致）/ `console_gen --selftest` **41/41**（零改动复跑一致）/ `m7_stats` **0 违规**（**零新增样本**）/ `dc_validator` **0 违规** / `repo_stats` **0 违规、P3 0**；`step-enforce --pid P-058` **exit 0**（session 定位本批）；`docs/CONSOLE.md` 因**新增 P 行与 session** 由 hook 重生成。

## 4. 关键决策记录

| # | 决策 | 理由 |
|---|------|------|
| DR-1 | **模板计数与 feature 目录数的声明面 = 四类模式 × 三载体**，本批**逐处同步**而非只改 `declared` | 实证（A-2）：PT-7A/7B/7C/7D 分别作用于 `CODE_WIKI` / `README.md`（两种形态：阿拉伯 + 中文数字）/ `README.en.md` ⇒ **只改 `declared` 会立刻在门面侧失配**；且 `README.en.md` 的词形数字（`Five` → `Six`）**不被 PT-7C 覆盖**（在「已知未覆盖」清单内），本批**顺手订正**（诚实优先） |
| DR-2 | **新建模板的 front-matter 沿用 `type: design` + `status: draft`**，**不启用** `template` 词表 | 与既有 4 份四件套模板**同形**（DC2 词表中 `template` 类当前**全仓零使用**）；建档目的是「可被 DC1/DC2 校验通过」，**不引入词表新用法**（避免为形态件引入无先例的状态值） |
| DR-3 | **`facade_baseline` 的 `as_of` 一并推进到 2026-09-30** | 本批**实质改变**了门面载体（README×2）的 `fs.templates` 值 ⇒ 快照日期须反映「值被更新的时点」，否则 `as_of` 与值语义不一致（同 P-057 门面批的处置口径） |

## 5. 对验收的输入

- 落地面：`SPEC_PROCESS.md`（新节 + v1.5）/ `DECISION_MATRIX_TEMPLATE.md`（新建）/ `RESEARCH_TEMPLATE.md` §6.4 / `DESIGN_TEMPLATE.md` §11。
- 声明面：`CODE_WIKI §10 declared`（36 / 6 / 58）+ `doc_registry`（+1）+ `facade_baseline`（`fs.templates 6`）；`CODE_WIKI §2.1` 树 + §9 索引行。
- 门禁面：`dc_validator`（DC1/DC2 + R7 计数）/ `repo_stats`（树·§9·declared 三向）/ `m7_stats`（零新增样本）/ `console_gen --selftest` 与 `--check` / `step-enforce --pid P-058`。
- **边界**（I-1 / I-5）：**零代码**（`scripts/` 与 `tools/` 零变更）；**不新增 RULE 编号**、**不动** `rules` 机读块；**不新增门禁 / hook / 依赖**。

## 附录 A：A 类断言明细

- A-1 至 A-3：见 §3 各 `【A】` 行（**本机实测，E1**）。