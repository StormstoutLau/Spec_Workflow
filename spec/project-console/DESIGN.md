---
id: project-console-DESIGN
type: design
version: 1.6
status: draft
date: 2026-09-11
depends: [project-console-RESEARCH, board-generator-DESIGN, ADR-0010, FWK-DECISION-RECORD]
upstream: null
---

# 设计文档：项目控制台（多视图控制台生成器 + 归属迁移，P-043 / 视图增补 P-044 / 承载与步骤表 P-046 / 锚点与映射收敛 P-047）

> **Feature**: 项目控制台（`spec/project-console/`）——本仓通用底座的**只读可视化层**
> **设计来源**: [RESEARCH v1.13](./RESEARCH.md)（16A+3B+4C+4H → 28A+5B+8C+1H → 36A+7B+12C+3H → 45A+9B+16C+4H → 45A+9B+16C+5H → 45A+9B+18C+5H → 45A+9B+19C+5H → 47A+10B+20C+5H → 49A+11B+21C+5H → 50A+12B+22C+5H → 52A+13B+23C+5H → 53A+14B+24C+5H → **55A+15B+26C+5H**；裁定 C-1~C-26）
> **前身**: [board-generator DESIGN](../board-generator/DESIGN.md)（P-041，I-1~I-6 不变式被本设计继承并扩展）
> **Spec 步骤**: Step 3-4
> **本批范围**: P-043 = 归属迁移 + 多视图扩展；P-044 = 视图增补（描述列 / per-feature 流程 / 架构图口径）；P-046 = 承载修复与步骤级动态描述（hook 链表形态 / 步骤四字段）；P-047 = 锚点双属性（C-15）+ 映射来源语义反转与共享模块收敛（C-16）；**P-047 收口修正批 = §6 缺映射清单落地 + §9 兜底面归零**——均为 **Layer-1 生成端派生视图（+ hook 入口的只读映射）**，不接验证端门禁
> **v1.2 变更（P-046，用户指令「先执行 C-13 和 C-14，C-16 共享模块单独处理」）**: 新增 **D11 hook 链表形态**（C-13：弃表格改逐 hook 列表块 + 补 `name` 作用 + 外部文本安全化升为通则 → 新不变式 **I-9**）/ **D12 步骤级动态描述**（C-14：步骤 / 制品 / 主题 / 创建时间 / 简要描述 / 修改历史 六列，**以事件流为主源**）；**C-15（锚点双属性）与 C-16（映射语义与收敛）不在本批**（用户指定）。
> **v1.3 变更（P-047，用户指令「执行 C-15 和 C-16」）**: 新增 **D13 锚点双属性**（C-15：`<a name=… id=…>` 覆盖「只认 name / 只认 id」两类渲染器；失效退化面登记 H8）/ **D14 映射来源语义反转与共享模块**（C-16：`CODE_WIKI §9` 行标注**优先** → `PROGRESS` 行内链接**兜底** → `—`；两处实现收敛为共享纯函数模块 `scripts/spec_map.py` → 新不变式 **I-10 语义同源**）；**本批首次新增 `scripts/` 文件**（`declared.scripts` 7 → 8）。
> **v1.4 变更（P-047 收口修正批，用户指令「P-047 是否完全闭环 → 执行 A+B+C+D」）**: ① **D15 §6 缺映射清单落地**（`_trace_section` 增「缺映射（I-8 显式缺口）」行——修正 v1.3 的**声明未落地**：v1.3 §6.8 已要求「计入 §6 缺映射清单」，但实现只落到 §2 的 `—`）；② **`CODE_WIKI §9` 补两行标注**（`cpp-hub-absorption → P-002` / `cpp-hub-gap-analysis → P-004`）→ **兜底面归零**（残余 A-33 实例与 `cpp-hub-absorption → P-011` 错值一并消解）；③ 记入**判据教训**：C-16 的「缺口 4 → 0」只覆盖**缺值**，不覆盖**错值**——指标**必要不充分**。
> **v1.5 变更（状态归属契约实施轮 · Layer-0，P-042 v1.8，用户指令「先按照结论顺序执行 符合完整spec工作流规范」；**零代码改动**）**: 依 [RESEARCH v1.8 §7.13](./RESEARCH.md) 的 **C-20** 新增 **D16 状态归属契约（Layer-0）**——确立**任务粒度状态真值源 = 「事件流 step 序表 ∪ feature 四文档 front-matter」（派生面）∪「人工裁决」（非派生面）**、**按值域分流**（**执行态** `done` / `in-progress` **可派生 → 机器写**；**决策态** `pending` / `blocked` **不可派生 → 人写**）、**同一位点单来源（禁双写）**；契约落 **`PLAN §1` 新增 `DC2.1 任务状态词表（+「来源」列）`**（与 DC2 **type 主轴轴正交**，四取值**零改动**、仅加「来源」列 = 「机器派生」/「人工」，守 I-7），`PROGRESS` L3 声明**改指向 DC2.1**。**§5 标题扩为「派生状态机与状态归属契约（D3 / D16）」并新增 §5.1**（**不改 §5 既有状态表**——「派生状态机」的实现面仍属 Layer-1）；**§8 增方案 G/H/I（并列否决）**。**Layer-1 边界** = `derive_state` 首参改派生值 / `PROGRESS` 状态列载体迁移 / 修订 I-7 **均属 P2（Layer-1 高风险）**，**不在本批**。

> **v1.6 变更（P0 批实施设计落档轮，P-042 v1.15，用户指令「待裁决项目细化分析 给出明确建议」→「请生成 P0 批的四文档实施设计草稿」→「先落档这一轮与上一轮结果」；**零代码改动**、**P0 只落设计不落实施**）**: 依 [RESEARCH v1.13 §7.18](./RESEARCH.md) 落 **D17「未开工 vs 确无 session 的判别」**——**§5 派生标注② 修订**（原「② 活动且 `PROGRESS` 无对应 session → `Needs Attention`（决策链缺失）」→ 拆为「**② `in-progress` 且无 session → `Needs Attention`（决策链缺失）**」「**③ `pending` 且无 session → `Recommended`（未开工）**」）+ **新增 §5.2 判据表**；**§8 增方案 J（`pending` 无 session 落 `tier=""`）/ K（直接改 `state`）并列否决**。**缘由** = 现表与实现存在不一致（§5 表 `pending` 行动优先级标 `Recommended`，而 `console_gen.py` L305 对 `pending` 且无 session 实落 `Needs Attention`）——D17 把 §5 表的「`pending` → `Recommended`」**补全为显式分支**，使**表 = 实现**（P2a 尚未实施，故本批只改**设计面**，实现面留 P2a）。**唯一设计点裁定 = `pending` 无 session 落 `Recommended`（非 `""`）**——理由 = 与 §5 原表一致，否则修一处表-实现不一致又留一处。**本批边界** = **只改设计面**：**不改** `scripts/console_gen.py`（P2a 实施留 P0 批）/ **不落 P0 实施** / **零代码** / **不激活 P2**。**status → draft**（D17 属未实施设计）。

## 1. 设计目标

把 P-041 的**单视图任务看板**升级为**多视图项目控制台**，并把能力归属由 `board-generator`（前身）迁移至 `project-console`：

1. **修正状态语义错配**（RESEARCH A-3）：废止「⚠ 待你审」这类**升格标签**，改用与 `PROGRESS` 原词对齐 + **机械派生**的状态（C-5 / B4）。
2. **补四维缺失**（RESEARCH A-4）：feature 级制品链与步骤投影、脉络链、架构与代码流程、量化进度。
3. **双主键分层**（C-6 / B5）：feature 为分组键、P 为事项键；活动区设卡片上限并折叠完成段。
4. **承载限定 markdown 内嵌 Mermaid**（C-7）：依赖宿主渲染，**不引入** mmdc（Node + Chromium）与自包含静态 HTML。
5. **依赖图零依赖可得**（C-8）：stdlib `ast` 解析 + `importlib.import_module(<字面量>)` 补提取。
6. **feature 可读描述**（C-9 / B6）：feature 视图补「描述」列，来源 = **制品自身 H1 标题**优先链（**不引视图层文本**，避免「视图依赖视图」）。
7. **项目级 × per-feature 双层流程**（C-10 / B7）：**默认展示项目级**架构流程；per-feature 流程以 Markdown 原生折叠元素（`details` / `summary`）+ 锚点目录提供**手动交互选择**；**排除 Mermaid `click`**。
8. **架构图改「显式关系」口径**（C-12）：import 图实测为空 → 口径改为 `hook → script` + `script → 真值源` + 保留 import 边（有则绘）。
9. **承载不自我破坏**（C-13 / B8）：hook 链改**逐项列表块**（长正则不落表格单元格），补 `name`（作用）使链自解释；**外部文本安全化升为通则**（竖线等）——视图不得因真值源原文而破坏渲染。
10. **步骤级动态描述**（C-14 / B9）：per-feature 折叠块给出每步的**主题 / 创建时间 / 简要描述 / 修改历史**，**以决策链事件流为主源**（100% 齐备），文档元数据仅作逐级回退，缺失显式 `—`。
11. **锚点双属性保险**（C-15 / A-44）：折叠块锚点同时给 `name` 与 `id`，覆盖「只认 `name`（GitHub 官方背书，但不进 outline/TOC）」与「只认 `id`（HTML5 标准）」两类渲染器；宿主两者皆剥离时退化为「可折叠不可跳转」。
12. **映射来源语义反转与语义同源**（C-16 / A-33 / A-34）：feature ↔ P 映射改为 **`CODE_WIKI §9` 行标注（人工索引，真值源侧）优先 → `PROGRESS` 行内链接兜底 → `—`**，并把两处实现**收敛为共享纯函数模块**（`scripts/spec_map.py`，禁双实现）——消解「引用上游依据的 P 行劫持映射」这一缺陷类别（对账路径已被证伪）。
13. **缺口落到视图（收口批，D15）**：§6 追溯覆盖增设「**缺映射（I-8 显式缺口）**」行——映射缺位（§9 与 `PROGRESS` 两源皆无）在此**显式列出**；无缺口时显式标「（无——N 个 feature 全部有映射）」，与 §2 的 `—` 构成「点（哪一行）+ 面（清单）」双显式（C-16 ④ 的「计入 §6 缺映射清单」由此真正落地）。

## 2. 设计依据

| 依据 | 来源 | 落到本设计的哪一条 |
|------|------|------------------|
| 状态词表须与既有词表共用、每态附进入/退出条件 | RESEARCH A-17 / A-18 / A-19 | D3 派生状态机 |
| 视图与 CLI 同词汇表、只做重投影 | RESEARCH A-17 / B4 | D3（输出 PROGRESS 原词，不造新词） |
| 分组键/卡片键分层并存 + 活动区上限 + 单一认知块 | RESEARCH A-20 / A-21 / A-22 / B5 | D2 输出结构 |
| Mermaid 宿主渲染；mmdc 需 Node + Chromium | RESEARCH A-23 / A-24 | D4 承载形式 |
| stdlib `ast` 建图；AST 优于文本解析；动态 import 局限 | RESEARCH A-25 / A-26 | D5 依赖图 |
| 本仓 `.pre-commit-config.yaml` 结构化；动态 import 仅 1 处且为字面量 | RESEARCH A-27 / A-28 | D5 + D6 |
| 单写路径 / 确定性 / 幂等 / 零依赖 / 纯派生 / 不增真值 | 前身 I-1~I-6 | D7 不变式 |
| Layer-1 + 懒加载三问 | [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) / RESEARCH §6 | D1 落点 |
| 描述源取制品自身 H1、**不引视图层 §9 文本**；7 个 feature 缺 RESEARCH 故需回退链 | RESEARCH A-36 / B6 / C-9 | D8 描述列 |
| Markdown 原生折叠可用 + 宿主无 JS/无自定义样式；Mermaid `click` 默认禁用、`loose` 属 XSS 载体 | RESEARCH A-29 / A-30 / A-31 / A-32 / B7 / C-10 | D9 per-feature 流程与交互 |
| 本仓 import 图**实测为空**（口径信息量为零） | RESEARCH A-35 / C-12 | D10 架构图口径（对 D5 的部分修正） |
| 表列数不齐（未转义竖线）；长 token 压列；`name` 字段可得 | RESEARCH A-37 / A-38 / A-39 / B8 / C-13 | D11 hook 链表形态 |
| 事件流三字段 100% 齐备；四文档 H1 77/77；文档元数据稀疏且命名漂移 | RESEARCH A-40 / A-41 / A-42 / A-43 / B9 / C-14 | D12 步骤级动态描述 |
| 官方自定义锚点**只背书 `<a name>`** 且明示不进 TOC；`<a id>` 无背书且存在冲突证据（HTML5 标准） | RESEARCH A-44 / C-15 | D13 锚点双属性 |
| `PROGRESS` 行内链接位置被「引用上游依据」劫持（4 feature 永久无 P）且两实现**同错**；`CODE_WIKI §9` 对四空洞全部正确 | RESEARCH A-33 / A-34 / C-16 | D14 映射语义反转 + 共享模块 |

## 3. 架构设计

### 3.1 整体架构（D1 落点）

```
真值源（只读）                     生成器（唯一写者）              派生产物
──────────────────────────       ──────────────────────        ──────────────────
docs/PROGRESS.md      ─┐
tools/spec_runner/     │
  sessions/*.jsonl     ├──────►  scripts/console_gen.py  ──►   docs/CONSOLE.md
spec/<feature>/*.md    │          （stdlib only，纯派生）        （唯一写路径）
scripts/*.py           │                 ▲
.pre-commit-config.yaml┘                 │（feature ↔ P 映射的唯一实现，
CODE_WIKI.md §9 索引  ──────────────────┘  C-16/I-10：console_gen 与
                                           step_enforce 复用 spec_map）
```

- **唯一脚本**：`scripts/console_gen.py`（取代前身 `scripts/board_gen.py`）
- **唯一产物**：`docs/CONSOLE.md`（取代前身 `docs/BOARD.md`）
- **触发**：pre-commit hook **`console-gen`**（`--stage`，L0 档＝提交即刷新，继承前身机制）

### 3.2 模块划分

| 模块 | 职责 |
|------|------|
| `parse_progress` | `PROGRESS.md` P 行 → `Task`（id/标题/状态/优先级） |
| **`spec_map`（新模块，P-047）** | **feature ↔ P 映射的唯一实现**（D14 / I-10）：`wiki_pid_map`（§9 行标注）/ `progress_pid_map`（兜底）/ `build_pid_map`（合并：§9 优先 → PROGRESS 兜底 → 缺位不入表）；被 `console_gen` 与 `step_enforce` 共同复用 |
| `read_sessions` | `sessions/*.jsonl` → 每 P：**最新一轮**的最远 step / 软性 / 末 ts / 步序列；并累积**全部轮次**的 step 级记录 `records`（C-14：`(轮次, step, ts, scenario, outcome)`，按文件名序稳定） |
| `artifact_map` / `feature_stage` | `spec/<feature>/` 四文档存在性 → 制品链 + 生命周期阶段（阶段由制品存在性推断） |
| `first_h1` / `shorten_title` / `feature_desc` | **描述列（D8）**：制品 H1 优先链 → P 行事项 → 目录名；主名收敛 + 截断 |
| `derive_state` | **派生状态机**：由证据机械计算状态 + 依据串（D3） |
| `dep_graph` | stdlib `ast` → 仓内 import 边 + `importlib` 字面量补提取（D5 ③） |
| `hook_chain` | 极简解析 `.pre-commit-config.yaml` → hook 链表（D5 ①）；**D11：增解析 `name`（人类可读作用）** |
| `_arch_section` | **架构与流程（D10）**：`hook → script` + `script → 真值源` + import 边 + 未声明脚本清单（I-8） |
| `_hook_list` | **hook 链表形态（D11）**：逐 hook 列表块（`id` —— `name` + 缩进 命令 / 触发范围 / 传入文件名），**弃表格** |
| `_cell` / `_clip` / `_fmt_ts` | **承载安全与截断（D11/D12）**：单元格安全化（竖线→全角，**通则**）/ 长文本截断 / 时间格式化 |
| `_step_table` | **步骤级动态描述（D12）**：步骤 / 制品 / 主题 / 创建时间 / 简要描述 / 修改历史（事件流主源） |
| `_feature_process_section` | **per-feature 流程（D9）**：锚点目录 + 每 feature 一个折叠块（四文档管道 + 步骤表 + 决策链 + 派生状态） |
| `render_*` | 各视图 → markdown / Mermaid 片段（纯函数） |
| `write_console` | 幂等写盘（内容未变不写） |
| `main` | CLI：`--stdout` / `--check` / `--stage` / `--selftest` / `--root` |

### 3.3 不变式（Invariants，ADD 审计依据，继承 I-1~I-6 并扩展）

| # | 不变式 | 判据 |
|---|--------|------|
| I-1 | **单写路径** | 除 `docs/CONSOLE.md` 外零文件写入 |
| I-2 | **确定性** | 禁 wall clock（基准取源最大 ts）→ 同源双跑逐字节一致 |
| I-3 | **幂等** | 内容未变不写盘 |
| I-4 | **零依赖** | stdlib only（不引入 PyYAML / rich / mmdc） |
| I-5 | **纯派生** | 100% 可重生成；覆盖无需备份（AGENTS.md 备份纪律的派生物例外） |
| I-6 | **不增真值** | 视图不持有原始状态；一切可回溯到真值源 |
| **I-7** | **词表对齐（P-043 新增）** | 状态输出**只用 `PROGRESS` 原词**（`pending`/`in-progress`/`blocked`/`done`）+ 独立「派生依据」列，**不得重贴标签**（禁「待你审」） |
| **I-8** | **显式缺口（P-044 新增）** | 派生不出的关系必须**显式列出**，不得静默省略：映射缺口保留 `—`、「未声明关系的脚本」清单、空 import 边如实标注「（无）」——**诚实优于静默补全**（承 C-11 / C-12 精神） |
| **I-9** | **承载安全（P-046 新增）** | 凡进入**表格单元格**的外部文本必须经 `_cell()` 安全化（半角竖线 → 全角）；**长无断点 token（正则等）不得落入表格单元格**——视图不得因真值源原文而破坏自身渲染（A-37/A-38） |
| **I-10** | **语义同源（P-047 新增）** | feature ↔ P 映射**只有一份实现**（`scripts/spec_map.py`），`console_gen` 与 `step_enforce` 复用同一纯函数；**禁止双实现 + 一致性对账**——A-33 已证伪该路径（两实现同错时对账通过），故以「结构上只存在一处语义」替代「事后比对两处语义」 |

## 4. 输出契约（D2 输出结构）

`docs/CONSOLE.md` 章序（双主键分层 + 三级行动队列）：

| 章 | 内容 | 对应裁定 |
|----|------|---------|
| §0 生成基准 | 源最大 ts / P 行数 / session 数 / feature 数（一行，确定性） | I-2 |
| §1 ⚑ 需要你 / NEXT | **三级优先级**：`Needs Attention`（blocked / 软性存疑）→ `Ready to Verify`（活动批次已完成待验）→ `Recommended`（下一步 step） | A-8 / A-19 |
| §2 feature 视图（分组键） | 每 feature 一行认知块：**描述**（制品 H1 优先链）+ 制品链四文档 ✓/— + 生命周期阶段 + **关联 P（= `CODE_WIKI §9` 行标注的 feature 主 P，C-16）** + 最远 step | A-6 / B5 / B6 / C-6 / **C-9** / **C-16** |
| §3 事项视图（卡片键） | P 卡片：状态（原词）+ 派生依据 + 进入/退出条件；**活动区上限 7 张**，超出折叠 | A-22 / C-5 / C-6 |
| §4 决策链状态机 | Mermaid `stateDiagram-v2`：`STEP_SEQUENCE` 五步 + 各步 gate 结论 | B2 / C-7 |
| §5 架构与流程 | Mermaid `flowchart LR`：**① `hook → script` ② `script → 真值源`（显式契约）③ import 边（有则绘）** + **hook 链（逐项列表块：id —— name / 命令 / 触发范围 / 传入文件名）** + 未声明脚本清单 | A-27 / A-35 / A-37~A-39 / **C-12** / **C-13** / I-8 / **I-9** |
| §5.1 per-feature 流程（**默认折叠**） | 锚点目录 + 每 feature 一个折叠块：**双属性锚** `<a name=… id=…>`（C-15）、摘要 `{feature} ｜ {阶段} ｜ {关联 P}〔｜ {n} 轮〕`、四文档管道 `flowchart LR`、**步骤级动态描述表**（步骤 / 制品 / 主题 / 创建时间 / 简要描述 / 修改历史）、决策链 step 序、派生状态与依据；**默认展示上层项目级流程** | A-29~A-32 / A-40~A-43 / B7 / **B9** / **C-10** / **C-14** / **C-15** |
| §6 追溯覆盖 | M7 hits 直读（样本数 / 形态 II）+ 各 feature 决策链完整性摘要 + **缺映射清单（I-8 显式缺口，D15：有则列出 / 无则显式标「（无——N 个 feature 全部有映射）」）** | A-12 / **I-8** / **C-16 ④** |
| §7 ✅ 已完成（折叠） | 最近 N 条（`DONE_TAIL`），其余折叠 | A-22 / C-6 |
| §8 ⑂ fork / 支线 | git 分支 + 工作树 | 前身继承 |

## 5. 派生状态机与状态归属契约（D3 / D16）

**状态词汇表 = `PROGRESS` 原词**（I-7）；派生的只是**依据**与**行动优先级**：

| 状态 | 进入条件（机械可判） | 退出条件 | 行动优先级 |
|------|--------------------|---------|-----------|
| `blocked` | `PROGRESS` 状态列 = `blocked` | 状态列改为其他值 | Needs Attention |
| `in-progress` | 状态列 = `in-progress` **且** 有 session 且最远 step ≠ `finalize` | 状态列改 `done` 或最远 step = `finalize` | Recommended |
| `pending` | 状态列 = `pending` | 状态列改 `in-progress` / `done` | Recommended |
| `done` | 状态列 = `done` | —（终态） | （入折叠段） |
| **派生标注**（不是状态） | ① `gate exit 2`（软性存疑）→ `Ready to Verify`；② `in-progress` 且 `PROGRESS` 无对应 session → `Needs Attention`（决策链缺失）；③ `pending` 且 `PROGRESS` 无对应 session → `Recommended`（**未开工**，见 §5.2 D17） | — | 影响 §1 分级 |

> 退出条件复用本仓现成机制：`step-gate` 三类规则（exit 0/1/2）即机械退出判据（RESEARCH A-19）。

### 5.1 状态归属契约（D16，C-20，Layer-0）

> **本小节 = 契约定义（Layer-0，零代码）**；上表（派生状态机）为 **Layer-1 实现面目标**，二者**分层共存、不混轴**。来源 = [RESEARCH v1.8 §7.13](./RESEARCH.md)（C-20 / B10 / A-46 / A-47）。

**真值源（S-1）** = 任务粒度状态的真值源**分两面**：**派生面** = 「**事件流 step 序表 ∪ feature 四文档 front-matter**」（`sessions/*.jsonl` 的 step 序 + R/D/I/C 四文档的 `version` / `status` / `date`）；**非派生面** = 「**人工裁决**」（审查结论 / 阻塞裁定 / 待办登记）。

**值域分流（S-2）与「来源」列** = 现有四取值**零改动**，仅增「来源」列标注写者：

| 取值 | 归属 | 来源（新列） | 依据（机械可判 / 人工） |
|---|---|---|---|
| `done` | **执行态** | **机器派生** | 制品链齐备 + 最远 step = `finalize` |
| `in-progress` | **执行态** | **机器派生** | 有 session 且最远 step ≠ `finalize` |
| `pending` | **决策态** | **人工** | 待办登记（无机械真值源） |
| `blocked` | **决策态** | **人工** | 阻塞裁定（无机械真值源） |

**位点单来源（S-3）** = `PROGRESS` 状态列在任一时刻**只有一个写者**（按上表值域分流），**禁双写**——机器不覆写决策态、人不手填执行态。

**载体（契约落点）** = `spec/doc-contract/PLAN.md §1` 新增 **`### DC2.1 任务状态词表（+「来源」列）`**（**与 DC2 轴正交**：DC2 为 **type 主轴 = 文档状态**，本词表为**另一轴 = 任务状态**，并入即重犯 v1.6 已修的混轴回归，A-46）；`docs/PROGRESS.md` L3 词表声明**改指向 DC2.1**（单一权威）。

**Layer-1 边界（P2，本批不做）** = ① `console_gen.derive_state` 第一参照**改派生值**（现抄 `task.status` → 因全 `done` 致三档队列恒空，A-47）② `PROGRESS` 状态列**载体迁移**（执行态改机器写）③ **修订 I-7**（决策态原词 / 执行态派生）。三者**须另立批 + 过 ADR-0010 三问 + 设可回退点**。

**回退点** = 本批**零代码**，回退 = 撤销 `PLAN §1 DC2.1` 新增块 + `PROGRESS` L3 指向（**纯文档可逆**，无代码 / 产物 / 门禁面影响）。

### 5.2 未开工 vs 确无 session 的判别（D17，C-24 ③ / C-26，Layer-0 设计面）

> **本小节 = 设计面判据（Layer-0，零代码）**；其**实现面**（`derive_state` 拆支）属 **P2a（Layer-1）**，留 P0 批。来源 = [RESEARCH v1.13 §7.18](./RESEARCH.md)（A-54 / A-55 / B14）。

**问题** = `derive_state` 的 `sess is None` 分支把**两种情形混同**（B13）：① **未开工**（`pending` 立项已登记、本就无决策流）与 ② **确无 session**（`in-progress` 执行态却缺决策链）——两者产生**同一句不成立的依据**（「无 session（决策链缺失）」）与**同一误标的行动档**（`Needs Attention`）⇒ V1a 前移一生效即把「正常开工中的事项」标成「需要关注」。

**判据表（D17）**：

| 状态 | 有 session？ | 依据（basis） | 行动档（tier） | 语义 |
|---|---|---|---|---|
| `pending` | 否 | 「未开工（立项已登记，无决策流）」 | **`Recommended`** | **正常**（V1a 立项即登记，尚未开工） |
| `pending` | 是 | （按 §5 主表派生） | `Recommended` | 正常（罕见：登记后即开决策流） |
| `in-progress` | 否 | 「执行态但无 session（决策链缺失）」 | **`Needs Attention`** | **缺口**（V2 族：执行态缺决策链） |
| `done` | — | （首分支短路早退） | `""` | 终态，不参与队列 |

**判别要点** = 分支键 **不是「有无 session」单独**，而是 **「`status` × 有 session？」组合**：`pending` 无 session 是**预期态**（不是缺口），`in-progress` 无 session 才是**缺口**。

**落点** = **实现面**（P2a）= 在 `sess is None` 分支内**再拆一支**，仅 3 行（RESEARCH §7.18【二】）；**不改** `state` 来源（永远 `return task.status` 原词）/ **不动** I-7（`tier` 三档本不在 `PROGRESS` 词表内）/ **不加开关**（回退 = 改回原字符串常量）。

**唯一设计点裁定 = `pending` 无 session 落 `Recommended`（非 `""`）**——理由 = **与 §5 主表一致**（主表 `pending` 的行动优先级即 `Recommended`）；若落 `""`，则本批修一处表-实现不一致（主表 `Recommended` vs 代码 `Needs Attention`）又留一处。

**Layer-1 边界（P0 批，本批不做）** = 本小节**只落设计面**（判据表）；`derive_state` 拆支 / 三 fixture / 真机 `docs/CONSOLE.md` 复核**均属 P0 批**（须用户裁决后另立批）。

## 6. 承载、依赖图与视图增补（D4 / D5 / D8-D10）

### 6.1 承载与依赖图（D4 / D5）

- **D4 承载（C-7）**：仅 **markdown + Mermaid 代码块**（宿主渲染）+ **Markdown 原生折叠元素**。**排除** mmdc 自渲染与自包含静态 HTML。
- **D5 依赖图（C-8）**：
  - 节点 = `scripts/*.py` + `tools/spec_runner/spec_runner.py`；边 = `ast` 提取的 `Import` / `ImportFrom`，**仅保留仓内模块**（按已知模块名集合过滤 stdlib / 第三方）；
  - **补提取**：`ast` 遍历 `Call` → `Attribute(value=Name('importlib'), attr='import_module')` 且首参为 `Constant(str)` → 记边（覆盖 RESEARCH A-28 实测的唯一动态位点）；
  - hook 链 = 极简行式解析 `.pre-commit-config.yaml` 的 `- id:` / `entry:` / `files:` / `pass_filenames:`（**不引入 YAML 库**）。
  - **D5 由 D10 部分修正**：单纯 import 图在本仓**实测为空**（A-35），口径改为「显式关系」（见 §6.4）；import 边**保留**为 ③ 之一种。

### 6.2 描述列（D8，C-9）

**来源优先链**（逐级回退，取首个非空；**全部来自真值源侧**）：

| 序 | 来源 | 实现 |
|----|------|------|
| ① | `spec/<feature>/` 制品 H1 标题（`RESEARCH.md` → `DESIGN.md` → `CHECKLIST.md` / `CHECKLIST_FUNC.md`） | `first_h1` + `shorten_title`（后缀匹配兼容遗留前缀命名） |
| ② | 关联 P 行的「事项」列 | `shorten_title(task.title)` |
| ③ | 目录名 | `feature` 原名兜底 |

- **不引 `CODE_WIKI §9` 文本**——§9 属**派生视图**，引用会形成「视图依赖视图」并使描述成为第二真值源（B6 / I-6）。
- **主名收敛（`shorten_title`）**：① 去 `调研文档：` / `设计文档：` 类前缀（冒号位置 ≤ 12 字符才认定）→ ② **交替**剥「结尾配对括号组」与断 `——` 直至稳定（两种形态都要收敛：`ARC 升级实施（…）——调研输入引用` 与 `独立验证（出路 C——…）`）→ ③ 截断至 `DESC_CAP = 40` 字符（超出补 `…`）。
- **`DESC_CAP` 属设计时取值**——渲染宽度校准见 RESEARCH **H6**（仍待实测）。

### 6.3 per-feature 流程与交互（D9，C-10）

- **默认层 = 项目级「架构与流程」**（§5）；**per-feature 流程为次级层、默认折叠**（§5.1）。
- **交互形态**：Markdown 原生折叠元素（`details` / `summary`）+ **锚点目录**（**双属性锚** `<a name="feat-{feature}" id="feat-{feature}">`（C-15，见 §6.7）+ `[feature](#feat-feature)` 跳转）。
- **排除 Mermaid `click`**：官方 config schema 默认 `securityLevel: "strict"` 即禁用 click；启用的 `loose` 是**三起 XSS 实证载体**（A-32），且本仓**无法控制宿主渲染器安全等级**——该路径不可得且不安全。宿主对 `<script>` / `<style>` / 事件处理器一律剥离（A-30），故凡「交互」只能是**折叠 + 锚点跳转**。
- **收敛策略**（体积预算见 RESEARCH **H7**，待实测）：仅对「四文档不全 **或** 有关联 session」的 feature 出折叠块，其余保留 §2 行。
- **块内容**：摘要 `{feature} ｜ {阶段} ｜ {关联 P}`；体内 ① 派生状态与依据（复用 D3 派生状态机）② 四文档管道 `flowchart LR`（R→D→I→C 逐节点 ✓/—）③ 该 P 的决策链 step 序（取自 sessions）。

### 6.4 架构图口径修正（D10，C-12——对 D5 的部分修正）

A-35 实测本仓 import 图为空（7 脚本 + `spec_runner` 相互零 import），使 D5 的前提「`ast` import 图足以表达架构」**部分被证伪**。口径改为**显式关系**：

| # | 关系 | 来源 | 性质 |
|---|------|------|------|
| ① | `hook → script` | `.pre-commit-config.yaml` 的 `entry` 直读（`ENTRY_SCRIPT_RE`） | 派生 |
| ② | `script → 真值源` | **显式架构契约常量** `DECLARED_SOURCES`（Layer-0 文档化于本节） | **声明** |
| ③ | `import` 边 / 动态 import 清单 | `ast` 提取（`dep_graph`） | 派生（**有则绘、无则不占位**） |

- ② 的常量（本仓现态）：`dc_validator → docs/**/*.md` / `m7_stats → M7 账本` / `repo_stats → 视图载体` / `console_gen → PROGRESS + sessions + spec/` / `step_enforce → PROGRESS`。
- **与 C-8「不需要显式元数据」不矛盾**：C-8 否决的是「**为推断 import 而新增元数据**」；此处是「以**已声明的架构契约**替代不可得的推断」，且**不新增采集面**。取舍与社区两派一致（显式模型派 vs 代码推断派）——本仓因推断源为空而**取显式派**。
- **I-8 兜底**：② 只在脚本**实际存在**时绘制；归不入 ①~③ 的脚本一律列入「**未声明关系的脚本**」清单（现态：`deepeval_m7_eval` / `pf_m7_eval` / `spec_runner`）——契约漂移**可见**而非静默。

### 6.5 承载不自我破坏：hook 链表形态（D11，C-13）

**缺陷事实**（A-37）：P-044 产物 §5 的 hook 表**表列数不齐**——表头 5 列，而第 3/4/5 行实为 **11 / 8 / 10** 个单元格；根因是 `files:` 正则**原样**入格而正则内含**半角 `|`**，被 GFM 当列分隔符。**这是视图自身破坏渲染，不是宿主问题**。

| 决策 | 内容 |
|------|------|
| 形态 | **弃表格，改逐 hook 列表块**：`- **{id}** —— {name}` + 缩进三项（`命令` / `触发范围（files 正则）` / `传入文件名`）。理由 = A-38：表格单元格按内容取宽，长无断点 token 既撑宽本列又把后续列挤到 5–10px；列表块让长 token **独占一行**，从形态上同时消除「压列」与「竖线破坏表格」两类缺陷 |
| 补字段 | `hook_chain` 增解析 **`name`**（人类可读作用）——A-39 表明该字段**本就在真值源中**却未被取，是「看不懂」的一半原因；缺 `name` → 显式 `—`（I-8） |
| 可读化 | `pass_filenames`：`false` → 「否」；`true` → 「是」；未设 → 「未设（pre-commit 默认『是』）」；`entry` 原样展示（**不做美化转述**，避免与真值源产生第二叙事） |
| 通则化 | 竖线安全化**升级为不变式 I-9**：凡进入表格单元格的外部文本一律过 `_cell()`；P-044 只对描述列做了 `_cell()`，**hook 表遗漏正是本缺陷直接成因** |

### 6.6 步骤级动态描述（D12，C-14）

**问题**：per-feature 折叠块此前只有 `R→D→I→C` 四节点 ✓/—，看不出「这步做了什么、何时做的、结论是什么、改过几轮」。

**来源链（以事件流为主源）**：

| 字段 | ① 主源 | ② 回退 | ③ 回退 | 缺省 |
|------|--------|--------|--------|------|
| 主题 | 该 step 的 `scenario`（事件流） | 该制品 H1 主名 | — | `—` |
| 创建时间 | 该 step 的 `ts` | 制品 `> **创建日期**:` 行 | front-matter `date` | `—` |
| 简要描述 | 该 step 的 `outcome` | — | — | `—` |
| 修改历史 | 该 P 的 **session 轮次**（`#1`/`#2`… + 各轮日期） | 制品 front-matter `version` | — | `—` |
| 制品↔步骤 | 文档自声明 `Spec 步骤` 行（A-43） | 常量 `STEP_ARTIFACT`（research→RESEARCH / design→DESIGN / implement→IMPLEMENTATION / verify→CHECKLIST；finalize 不新增制品） | — | `—` |

- **主源为事件流 = 零新增采集面**（`read_sessions` 已在读同一批文件，A-40 实测三字段 100% 齐备）；
- **多轮语义**：同一 step 在多个轮次出现时**最新一轮胜出**（主题/时间/简要），「修改历史」列出**全部轮次与日期**；摘要行追加 `｜ {n} 轮`（仅 n > 1）；
- **无 session** → 不渲染空表，改**单行显式缺失**（I-8）：不用稀疏且命名漂移的文档元数据（A-42）「补得像有」；
- **裁剪**：`reasoning`（常数百字）**不进视图**，只保留 `outcome` 一句；主题/简要按 `STEP_CAP = 48` 截断（守 C-6 单一认知块；H6 渲染宽度校准待实测）；
- **体积**：折叠块由 26 行级扩为 26 × (5 列 × n 步)，实测产物 514 行 / 20027 B（P-044）→ **729 行 / 45709 B**（P-046；H7 部分回填：仍属展开面内，未失控）→ **722 行 / 44526 B**（P-047：映射归位使部分 feature 的步骤表 / 历史列变短，步骤表行 81 → 69，体积**略降**）→ **723 行 / 44588 B**（P-047 收口批：§6 增缺映射行 +1 行）。

### 6.7 锚点双属性（D13，C-15）

**事实面**（A-44）：宿主（GitHub GFM）**只官方背书** `<a name="…">`，并明示「custom anchors will not be included in the document outline/Table of Contents」；`<a id="…">` 是 HTML5 标准形态，但「GitHub 是否一并剥离 `class`/`id`」存在**相互冲突的证据**（含低可信度来源，已标注）；本仓**无法验证远端渲染**（E2）。

| 决策 | 内容 |
|------|------|
| 形态 | 每 feature 折叠块前输出 `<a name="feat-{f}" id="feat-{f}"></a>`——同一锚**并行两个属性**：只认 `name` 的渲染器（官方背书形态）与只认 `id` 的渲染器（HTML5 标准形态）都能命中；成本 = 每锚多一个属性 |
| 失效退化面 | 若宿主**两者皆剥离** → 退化为「**可折叠但不可跳转**」：默认项目级视图与折叠功能**不受影响**（仅目录跳转失效）；该残余风险登记为 **H8**（真机存活率待验） |
| 不选单属性 | 任一单属性都会把「另一类渲染器失效」变成**静默风险**；双属性无新机制面、无新依赖，属**纯承载层冗余**（与 C-13 的「承载不自我破坏」同源） |

### 6.8 映射来源语义反转与共享模块（D14，C-16）

**缺陷面**（A-33）：旧语义只认「`PROGRESS` P 行内**首个** `spec/<feature>/` 链接」，而该位置在历史批次被用于**引用上游依据**（实测 `P-009/P-010/P-011/P-016`）→ 4 个 feature（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema`）**永久拿不到 P**；更关键的是 `step_enforce.build_feature_pid_map` 与 `console_gen.feature_pid_map` 两处实现**同错**——一致性对账**抓不住**该类缺陷。

| 决策 | 内容 |
|------|------|
| 语义 | **反转优先级**：① **`CODE_WIKI §9` 行标注**（人工维护索引，属真值源侧；A-34 实测对四个空洞**全部正确**）→ ② `PROGRESS` 行内链接**兜底** → ③ **缺位不入表**（调用方以 `—` 显式缺口呈现，I-8，并计入 §6 缺映射清单） |
| 抽取规则（确定性） | §9 行取**首个** `P-\d{3}`（= 该 feature 的**主 P** 标注）；PROGRESS 取行内**首个** `spec/<feature>/`（末行胜出）——纯字符串、无 wall clock（I-2） |
| 收敛 | 抽共享纯函数模块 **`scripts/spec_map.py`**（`wiki_pid_map` / `progress_pid_map` / `build_pid_map`）；`console_gen` 与 `step_enforce` **复用同一实现** → 新不变式 **I-10 语义同源**。代价 = `scripts/` +1 文件（`declared.scripts` 7 → 8），`DECLARED_SOURCES` 同步登记 `spec_map → PROGRESS + CODE_WIKI §9` |
| 否决 (b) 双实现 + 对账 | A-33 已证伪：两实现**同错**时对账**通过**（对账只能发现「两处不一致」，发现不了「两处一致地错」） |
| 否决 (c) 只改一处 | 制造**双语义**（同一 feature 在视图与门禁中指向不同 P），比双实现更坏 |
| 不改历史 PROGRESS 行 | 读取端解决（维持 C-11 ④）：历史叙事零扰动 |
| 语义副作用（明示） | 「关联 P」由「**最后引用的批次 P**」变为「**§9 行标注的 feature 主 P**」；真实仓实测 **13 项映射差异**（v1.3 首轮）= 4 项空洞补齐 + 9 项主 P 归位——属**语义明确化**而非数据改动；**收口批后为 14 项**（+`cpp-hub-absorption` P-011 → P-002 错值消解，见下行）。`§9` 行自此承担映射权威，须与 feature 主 P 同步维护（漂移由 I-8 缺口清单兜底） |
| **收口批：兜底面归零** | v1.3 实施后仍有 **2 个 feature 无 §9 标注**（`cpp-hub-absorption` / `cpp-hub-gap-analysis`）→ 仍走「易被劫持」的兜底源，实测 **`cpp-hub-absorption` 被劫持为 P-011（应为 P-002）**——即 A-33 形态的**残余实例**。收口批补两行 §9 标注（→ P-002 / P-004）→ **兜底面 32/32 全部由人工索引覆盖**，残余与错值一并消解 |
| **判据教训（收口批记录）** | C-16 的验收判据「**缺口 4 → 0**」只覆盖**缺值**，不覆盖**错值**（`cpp-hub-absorption` 旧新语义都给 P-011，故不进入缺口统计，却仍是错值）→ 该指标**必要不充分**；后续同类收敛须同时核「来源分布」（多少 feature 依赖兜底源）而非只看缺口数 |
| 附带收益 | 新增 `spec_map` 后仓内**首次出现 import 边**（`console_gen → spec_map` / `step_enforce → spec_map`），D5 的 `ast` 依赖图口径由「实测为空」恢复为「有边则绘」 |

## 7. 错误处理

| 场景 | 行为 |
|------|------|
| `PROGRESS.md` 不可读 | 顶层兜底 → `exit 2`（工具自身错误，绝不当作「零任务」） |
| session 坏行 / 目录缺失 | 容错跳过（降级为空集，不中断） |
| `.pre-commit-config.yaml` 缺失 | hook 链段渲染「（不可读）」 |
| `CODE_WIKI.md` 不可读 / 无 §9 节 | 映射退化为「**仅 PROGRESS 兜底**」（`spec_map.wiki_pid_map` 返回空表）；缺位在视图里以 `—` **显式**呈现（I-8），不静默补全 |
| `git` 不可用 | fork 段降级为空列表 |
| `--check` 内容不一致 | `exit 1`（板过期，提示重跑） |

## 8. 替代方案

### 方案 A：保留单视图 + 只修标签文案（否决）
- 理由否决：RESEARCH C-1 已判「简陋是**结构性**的」，改渲染/改文案无解；且 A-3 的错配根源是**凭空升格**，改名不除根（I-7 因此明确禁重贴标签）。

### 方案 B：引入 mmdc 预渲染 SVG + 自包含 HTML（否决）
- 理由否决：mmdc 需 Node 18.19+ 与 Puppeteer/Chromium（A-23 三个独立实作佐证）——违 I-4 零依赖；自包含 HTML 的复杂图可读性上限未证（RESEARCH §7.3 已判「消解为不适用」）。

### 方案 C：per-feature 用 Mermaid 图内 `click` 做「点击切换」（否决）
- 理由否决：官方 config schema 默认 `securityLevel: "strict"` **即禁用 click**；启用需 `loose`，而 `loose` 是**三起独立 XSS 实证**的载体（A-32），且本仓**无法控制宿主渲染器的安全等级**——该路径**不可得且不安全**（B7）。可得形态只有「折叠 + 锚点跳转」。

### 方案 D：hook 链保留表格 + 仅转义竖线（否决）
- 理由否决：转义只解决**表结构被破坏**（A-37），不解决**列被压扁**（A-38）——长正则仍是表格里最宽的无断点 token，会把后续列挤到不可读；且「正则入格」这件事本身把**机器可读原文**当成**人类可读摘要**用。列表块一次解决两类缺陷，代价仅为行数增加。

### 方案 E：多视图 + 归属迁移（选择）
- 理由：以最小机制面（**单脚本 + 单产物 + 单 hook**）覆盖四维缺失；沿用前身已验证的确定性/幂等/门禁触发；依赖图与决策链图均落在 stdlib，零新增依赖。P-044 增补描述列、per-feature 折叠与显式关系架构图**仍在同一机制面内**（无新文件、无新产物、无新依赖）；P-046 的承载修复与步骤表同样**零新文件、零新依赖**；P-047 为**映射语义唯一化**新增一个共享纯函数模块（`scripts/spec_map.py`）——是全批唯一的文件面增量，代价 = `declared.scripts` +1（换 I-10 语义同源的结构性保证）。

### 方案 F：保留两处映射实现 + 增一致性对账（否决）
- 理由否决：A-33 实测两处实现**同错**（同一语义、同一缺陷、同一批受害 feature），对账**通过**——对账只能检出「两处不一致」，检不出「两处一致地错」；把「结构上只存在一处语义」（抽共享模块，I-10）换成「事后比对两处语义」，等于把已被证伪的失效模式**制度化**。

### 方案 G：把任务状态并入 DC2 主轴词表（否决）
- 理由否决：DC2 是 **type 主轴（文档状态）** 的统一词表（`adr` / `discovery` / `process-spec` / `framework` / `template` / `design`），任务状态是**另一轴**；并入会使同一张表承载**两个正交维度**，重犯 v1.6 已修的**混轴回归**（A-46）。且 `dc_validator` 按 `type` 取词表校验，塞入任务状态会污染 type 分支语义。

### 方案 H：只改 `PROGRESS` L3 声明、不上提 `PLAN`（否决）
- 理由否决：契约须有**单一权威源**——`PROGRESS` 是**载体（真值表）**而非**契约定义地**；声明留在载体里 = 无契约面（现状即如此，A-46 已实证「无校验器读该行」）。上提 `PLAN §1` 使任务状态契约与 DC1-DC4 同处一权威面，便于将来 Layer-1 校验器引用。

### 方案 I：本批直接实施派生（改 `derive_state` + 迁移状态列）（否决）
- 理由否决：属 **Layer-1 高风险**——须先修订 I-7、过 ADR-0010 三问、设可回退点；且状态列**全 `done`**（A-47）下贸然改派生会**同时改变**三档队列与折叠段形态，须独立批 + 门禁复跑。本批严守「**Layer-0 零代码**」边界。

### 方案 J：`pending` 且无 session 落 `tier=""`（无行动档）（否决）
- 理由否决：与 §5 主表不一致——主表 `pending` 的行动优先级为 `Recommended`；§5.2（D17）把 `pending` 无 session 显式定为 `Recommended`（**与主表对齐**）。若改落 `""`，则本批修一处表-实现不一致（主表 `Recommended` vs 代码 `Needs Attention`）又留一处（**新引入表-实现分歧**）。`pending` 是**正常预期态**、**非终态** ⇒ 应留在行动队列而非落「无档」。

### 方案 K：直接改 `state`（把 `pending` 派生为重标签）（否决）
- 理由否决：违 **I-7 词表对齐**——`state` 必须永远 `return task.status` 原词（A-3 / B13 源码实读）；D17 只改 `basis` / `tier`（**不在 `PROGRESS` 词表内的派生列**）⇒ **不触 I-7**；改 `state` 即把「派生状态机」的实现面（P2b：状态来源迁移 + I-7 扩写 + 回退点）**提前到 P2a**，混淆两级、放大风险面（C-24 ③(3a) 的解耦依据被破坏）。

## 9. 对实施的输入

- **必改（P-043，已完成）**：`scripts/console_gen.py`（新建）/ `docs/CONSOLE.md`（新产物）/ `.pre-commit-config.yaml`（hook 更名 `console-gen`）/ 移除前身 `scripts/board_gen.py` 与 `docs/BOARD.md`
- **必改（P-044）**：`scripts/console_gen.py` 增补 `first_h1` / `shorten_title` / `feature_desc`（D8）、`_feature_process_section`（D9）、`_arch_section` + `DECLARED_SOURCES` / `TRUTH_NODES`（D10）；`docs/CONSOLE.md` 重生成（§2 加描述列、§5 换口径、新增 §5.1）
- **必改（P-046）**：`scripts/console_gen.py` ① `hook_chain` 增解析 `name`；② 新增 `_hook_list`（弃表格改列表块）并在 `_arch_section` 内替换原 hook 表；③ `_cell` 升为**通则**安全化 + 新增 `_clip` / `_fmt_ts`；④ `SessionInfo` 增 `records`、`read_sessions` 累积**全部轮次** step 级记录；⑤ 新增 `_step_table` 并在 `_feature_process_section` 体内插入步骤表、摘要追加 `｜ {n} 轮`；⑥ 新增常量 `STEP_ARTIFACT` / `STEP_CAP`；`docs/CONSOLE.md` 重生成（§5 hook 链换形态、§5.1 补步骤表）
- **必改（P-047）**：**新增** `scripts/spec_map.py`（映射唯一实现，I-10）；`scripts/console_gen.py` ① 删除本地 `feature_pid_map` / `P_IMPL_RE`、改调 `spec_map.build_pid_map`；② 锚点改**双属性** `<a name=… id=…>`；③ `TRUTH_NODES` 增 `TS_wiki`、`DECLARED_SOURCES` 增 `spec_map` 与 `TS_wiki` 边；④ 新增 `_read_text`（容错读可选真值源）；`scripts/step_enforce.py` ① 删除本地 `P_ROW_RE` / `build_feature_pid_map`、改调共享模块；`docs/CONSOLE.md` 重生成；`CODE_WIKI.md`（`declared.scripts` 7 → 8 + §2.1 树登记 `spec_map.py`）
- **必测**：selftest（双主键 / 词表对齐 / 三级队列 / 制品链 / 活动区上限 / Mermaid 三图 / 禁 wall clock / 幂等 / 确定性 / `--stdout` / `--check` / I-1 / **描述优先链三源** / **per-feature 折叠与锚点** / **显式关系三口径** / **I-8 未声明清单** / **C-13 hook 列表块 + `name` + `pass_filenames` 三态** / **C-14 步骤表六列 + 多轮「最新一轮胜出」+ 无 session 显式缺失** / **I-9 竖线安全化通则** / **C-15 双属性锚** / **C-16 映射优先级与单一实现（S35）+ §9 补洞（S36）**）
- **必改（P-047 收口修正批）**：`scripts/console_gen.py` ① `_trace_section` 增参并输出「缺映射（I-8 显式缺口）」行（D15）；② selftest 增 S37（有缺口列出 / 无缺口显式标无）；`CODE_WIKI.md §9` 补两行 P 标注（`spec/cpp-hub-absorption/ → P-002` / `spec/cpp-hub-gap-analysis/ → P-004`）→ 兜底面归零；`RESEARCH.md §7.10` 追记（非新增断言）
- **门禁行为验证（P-047 特有）**：映射语义变更**直接影响 `step-enforce` hook 的 P 定位**，故须对**全部真实 feature** 逐一模拟 hook 调用并核对退出码（不得只验新增用例）；收口批后须**复跑**该复核（兜底归零改变 2 个 feature 的 P 指向）
- **视图层同步**：CODE_WIKI（版本头 / §2.1 脚本树与 docs 树 / §9 索引 / 覆盖对象 / declared / PT-11）
- **本批（P-042 v1.8 / Layer-0，零代码）**：**不做任何代码改动**——只落 **`spec/doc-contract/PLAN.md §1` 新增 `DC2.1 任务状态词表（+「来源」列）`** + `docs/PROGRESS.md` L3 声明**改指向 DC2.1**；`DESIGN §5.1`（D16）为**契约定义**，其 Layer-1 实现（`derive_state` 改派生值 / 状态列迁移 / 修订 I-7）**留待 P2**
- **本批（P-042 v1.15 / P0 批实施设计，零代码）**：**不做任何代码改动**——只落 **D17 / §5.2**（判定表）与 **§5 派生标注② 修订**、**§8 方案 J/K**；P2a 的实现面（`derive_state` 拆支 + 3 fixture + CONSOLE 真机复核）**属 P0 批**（须用户裁决后另立批）
- **边界**：不接验证端门禁（Layer-1）；不改三个校验器语义；不改 `sessions` 写入路径；**不改历史 PROGRESS 行**（读取端解决）；**C-11 ①（`—` 显式缺口）由 C-16 继承并强化，不单独实施**

---

**Review 签字**: _________ 日期: _________
