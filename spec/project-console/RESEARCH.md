---
id: project-console-RESEARCH
type: design
version: 1.4
status: verified
date: 2026-09-11
depends: [board-generator-DESIGN, academic-writing-workflow-RESEARCH, ADR-0010]
upstream: null
---

# 调研文档：项目控制台——可视化看板剥离与视图分层（P-042）

> **Feature**: 项目控制台（`spec/project-console/`）——本仓通用底座的**只读可视化层**
> **创建日期**: 2026-09-11
> **状态**: in-review（审查中）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「BOARD.md 这个看起来有些简陋 P-XX项目没有描述当前状态 进行中待你审阻塞 这几个是如何定义的 / 没有开发研究脉络 架构 代码流程相关的展示 无法可视化的展示当前在做什么功能 做到什么步骤了 / 搜索下开源社区优秀案例 进行调研 / 可视化看板需要从学术推理调研单独剥离出来形成一个 PR 当前框架类似一个通用底座 学术推理是一个深度改造的 fork」——用户裁决「PR 形态 = 独立 feature 四件套 / 落点 = `spec/project-console/` / 与 P-041 关系 = 接续取代（P-041 记前身）/ 本批范围 = 仅调研落档」
> **参考先例**: P-040 academic-writing-workflow（看板概念的来源调研）、P-041 board-generator（L0 首落点 = 前身）、P-037/P-039（调研批止于懒加载 gate 的形态先例）、P-023（概念登记型 feature 两件套）
> **归属裁定（剥离）**: 可视化看板能力归属**底座**（Layer-1 工具层），不再寄生于 `academic-writing-workflow`（该 feature 的 C-6/C-7 降格为**来源指针**）。P-041 board-generator 记为本 feature 的**前身（L0 首落点）**；归属迁移与多视图扩展在**实施批**执行（本批零代码改动）。
> **v1.3 变更（补充调研轮 · 实施反馈回填 + 剩余待办，用户指令「- **hook 链**（`.pre-commit-config.yaml` 直读）：表格里面有乱码 其次我看不太懂这个表格 / per-feature 流程 里面 都是research-design-implementation-checklist 缺少每个步骤的动态描述 需要每个步骤 主题 创建时间 简要描述 修改历史 / 剩余待办一并调研」）**: 新增 **§7.8-§7.10 三题**——① **hook 链表乱码**：机械确证**表列数不齐**（表头 5 列；第 3/4/5 行实为 **11/8/10** cells）→ 根因 = `files` 正则内**未转义的半角 `|`** 被 GFM 当作列分隔符（**视图自身破坏渲染的 P1 缺陷**，非宿主问题）→ **C-13**（改逐 hook 列表块 + 补 `name`（作用）列 + 长 token 不落表格单元格）；② **步骤级动态描述**：实测**事件流主源齐备**（31 session / **130 decision rows**，`scenario`+`outcome`+`reasoning` **100% 齐备**）而**文档元数据源稀疏**（四文档 H1 **77/77** 齐、`创建日期` 行 50/77、`Spec 步骤` 行 54/77、front-matter `date`+`version` 仅 25/77、文档内「修订历史」章节仅 13/77 **且命名漂移**）→ **C-14**（主题/创建时间/简要描述/修改历史 四字段来源链，**以事件流为主源**、文档元数据逐级回退、缺失显式 `—`）；③ **剩余待办**：**C-11 映射语义再度修正**（对账抓不住「两实现同错」，故改为**改来源语义**：§9 行标注为**优先源**）→ **C-16**；**锚点形态**（官方文档背书 `<a name>` 且明示「不进 outline/TOC」，`<a id>` 无官方背书）→ **C-15 双属性保险**；H6/H7 由实施读数**部分回填但不关闭**；新增 **H8**（双属性锚点真机存活率）。断言 **36A+7B+12C+3H → 45A+9B+16C+4H**（+9A / +2B / +4C / +1H）；**续编 §7.8-§7.10，仍刻意不改号**。
> **v1.2 变更（补充分析轮，用户指令「feature 视图表格 需要增加一列描述 / 架构与流程方面 能否实现对项目架构流程 与 每个feature流程的展示 默认展示项目架构流程 可以手动交互选择feature的流程展示 / 新视图暴露的真实问题也进行调研 / 请补充分析」）**: 新增 **§7.5-§7.7 三题分析**——① **描述列**：描述源取「制品自身标题」优先链（**不引视图层 §9 文本**，避视图依赖视图）→ **C-9**；② **架构/流程交互**：默认项目级 + per-feature 折叠图，交互形态 = **`<details>` 折叠 + 锚点目录**，**排除 Mermaid `click`**（官方 schema 默认 `strict` 即禁用 click；`loose` 为三起 XSS 实证载体）→ **C-10**；③ **新视图暴露两问题**：脚本 import 图**实测为空** → **C-12 架构图口径修正**（改「显式关系」口径：hook→script + script→真值源 + 保留 import/动态 import）；feature→P 映射 4 空洞根因（首个 spec 链接指向**上游依据**而非本批产出）+ §9 行标注不一致 → **C-11**（保留显式缺口 + §9 标注为第二源 + **统一双实现映射函数**）。断言 **28A+5B+8C+1H → 36A+7B+12C+3H**（+8A / +2B / +4C / +2H）；**§7 章节改称「补充调研与补充分析」并续编 7.5-7.7——刻意避免改号**（否则 §8 参考文献顺延会再次触发 session 锚点连锁修正，见 v1.1 教训）。
> **v1.1 变更（补充调研轮，用户指令「遗留问题进行补充调研」）**: 新增 **§7 补充调研：遗留四项（H1~H4）**——逐项「社区实证 + 本仓可核」双通道取证并**全部判定关闭假设**：H1 状态词表 → **C-5**（派生状态机 + 词表对齐）/ H2 主键粒度 → **C-6**（双主键分层）/ H3 承载上限 → **C-7**（限定 markdown 内嵌 Mermaid，排除 mmdc 与自包含 HTML）/ H4 依赖元数据 → **C-8**（不需要；stdlib `ast` + 一处字面量补提取即可覆盖）；**编号顺延**：原 §7 参考文献 → **§8**；断言 **16A+3B+4C+4H → 28A+5B+8C+1H**（+12A / +2B / +4C；假设区 4 → 1，仅余 H5）；**C-5~C-8 为本 feature 局部编号**（与 `academic-writing-workflow` 的 C-6/C-7 不同命名空间）。
> **本批边界**: 调研/分析落档（RESEARCH + 决策链），止于 ADR-0010 三问懒加载 gate——**零工具改动、零新依赖**（I-1）。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 45 | A-1~A-4 本仓现状（源码核对 + 机械重数，E1）；A-5~A-15 社区案例（E2-E4）；A-16 真值源机械盘点（E1）；A-17~A-28 遗留四项取证（§7.1-§7.4，E1-E2）；A-29~A-36 v1.2 三题取证（§7.5-§7.7，E1-E2）；**A-37~A-45 v1.3 三题取证**（§7.8-§7.10：hook 表列数不齐机械确证 / 长 token 压列实证 / hook `name` 字段未解析 / 事件流 130 rows 三字段齐备 / 四文档 H1 77/77 / 文档元数据稀疏度盘点 / `Spec 步骤` 自声明映射 / 官方自定义锚点形态 / 折叠块官方约束，E1-E2） |
| B 推断类 | 9 | B1 三层视图零依赖可得 / B2 决策链 ↔ FSM 视图同构 / B3 剥离归属成立 / B4 派生状态机形态 / B5 双主键分层 / B6 描述取制品自身标题 / B7 交互形态 = 折叠 + 锚点 / **B8 hook 链表形态 = 列表优于表格** / **B9 步骤级动态描述主源 = 事件流而非文档元数据**（附录 B） |
| C 判断类 | 16 | C-1 简陋为结构性（非审美）/ C-2 剥离裁定 / C-3 分层与懒加载 gate / C-4 承载形式 / C-5~C-8 遗留四项判定 / C-9~C-12 v1.2 三题判定 / **C-13~C-16 v1.3 三题判定**（hook 链表重构 / 步骤级四字段来源链 / 锚点双属性 / 映射来源语义与收敛；附录 C） |
| 假设区 | 4 | H5（派生状态机状态集最小完备性）/ H6（描述列单行长度上限——**已获间接依据，未关闭**）/ H7（per-feature 流程视图体积预算——**已部分回填，未关闭**）/ **H8（双属性锚点在宿主的存活率）**——均未完全实测（附录 C） |

## 1. 调研目标

**核心问题**:
1. **现状诊断**：`docs/BOARD.md` 为何"简陋"？「进行中 / 待你审 / 阻塞」三档究竟由什么定义？缺失哪些维度？
2. **社区形态**：开源社区有哪些成熟做法可覆盖「开发研究脉络 / 架构 / 代码流程 / 当前在做什么、做到哪一步」？
3. **剥离归属**：可视化看板应归**通用底座**还是**学术推理 fork**？与既有 P-041 的关系如何处理？
4. **门禁走向**：本 feature 在 ADR-0010 三问下放哪层、激活条件是什么、未激活副作用是否为零？

## 2. 调研方法与取证

| 方法 | 用途 | 取证 |
|------|------|------|
| 源码核对 | 三档状态的定义链（`parse_progress` / `STATUS_LABEL` / `_next_queue`） | 诊断时点为前身 `board_gen.py`（**P-043 已退役**）；承接者 [console_gen.py](../../scripts/console_gen.py) |
| 机械重数（grep） | 三组恒空实证、真值源盘点 | [PROGRESS.md](../../docs/PROGRESS.md) / `spec/` / `tools/spec_runner/sessions/` |
| WebSearch（6 轮） | 社区四类形态取证 | spec 制品链 / diagram-as-code / agent trace / 双向追溯 |
| 官方仓库与文档页 | 版本与机制的一手确认 | 见 §8 参考文献 |

**调研范围**: 时间 2026 年当期活跃项目为主；领域 = spec-driven development 工具链、架构可视化、agent 可观测性、需求追溯；**排除**: 需常驻服务器/云端的重型平台本体（与本仓零依赖定位冲突，仅作对照）。

## 3. 现状诊断（E1：源码核对 + 机械重数）

### 3.1 三档状态的定义链

【A】A-1: **三档分组不是看板计算出来的，是 `PROGRESS.md`「状态」列的逐字直译**——`parse_progress` 取 P 行第 4 列原样作 `Task.status`；`STATUS_LABEL` 为纯映射表 `in-progress → ▶ 进行中` / `pending → ⚠ 待你审` / `blocked → ✖ 阻塞`，`done` 单独进「最近 8 条」尾表。**板子不具备任何独立状态判定逻辑**。（诊断时点源码 = 前身 `board_gen.py`，**P-043 已退役**；承接者 [console_gen.py](../../scripts/console_gen.py) 沿用同一 `parse_progress` 取列逻辑，但**已废止 `STATUS_LABEL` 重贴标签**。）

【A】A-2: **三个分组恒空（机械重数实证）**——`PROGRESS.md` 中 `| done |` 命中 **41** 行，而 `| pending | / | in-progress | / | blocked |` 合计命中 **0** 行。故三组永远渲染「（无）」，看板实际只剩「最近 8 条 done」+ fork 支线 → **"简陋"是结构性必然，不是渲染缺陷**。

【A】A-3: **标签语义错配**——`pending` 在 PROGRESS 语义 = 「待办」，被渲染为「⚠ **待你审**」；但代码内**不存在任何审查队列判定**（无独立 pass 状态读取、无 gate 结论消费）。该标签把「待办」误升格为「等你审查」，是**凭空多出一层的语义**——正属本仓「声明 ≠ 重数」纪律要拦截的形态。

【A】A-4: **四个维度缺失**——① **feature 级 step 投影缺失**：`list_features()` 结果仅喂给基准行，从未生成 per-feature 的「四文档 / 五步链」投影表；② **无脉络**：feature → P → session → 四文档 → 决策链的关联链未表达；③ **无架构与代码流程**：脚本、hook 链、`spec_runner` 模块间关系零可视化；④ **无量化进度**：无 step 完成度百分比、无 gate / verify-anchor 通过率。另「需要你/NEXT」队列的构成为 `blocked → 带软性 gate 的项 → pending`（前身源码，**P-043 已退役**；承接者 [console_gen.py](../../scripts/console_gen.py) 的 `_tier_lines` 已改为**三级行动档**），同样因全 `done` 而恒空。

## 4. 社区调研发现（四类分层）

### 4.1 Spec 制品链与步骤时间线（同构度最高）

【A】A-5: **OpenSpec UI**（ToruAI/openspec-ui）：per-change **制品链** `proposal → design → specs → tasks`，每件标注 **written / ready-to-write-next / blocked**；README 明示"同词汇表读自 `openspec status`，**直接读盘**"；**只读、本地运行、单二进制、从不写 specs**——与本仓「纯派生只读视图」定位完全同构。

【A】A-6: **SpecKit Tracker**（VS Code 扩展，`summitpatil.speckit-tracker`）：**7 阶段垂直时间线**（constitution → specify → clarify → plan → tasks → checklist → implement，每阶段带命令与关键制品）+ **3 个 SVG 环形进度图**（Stages / Tasks / Checks）+ 实时解析 `- [x]` / `- [ ]` + **FileSystemWatcher 自动刷新** + git 分支推断当前 feature + 状态栏百分比——直接回答「做到什么步骤了」。

【A】A-7: **Spec Kitty**：`spec-kitty dashboard` 本地看板 = 泳道 `planned → doing → for review → done` + 实时完成百分比与任务计数 + **多 agent 归属**（哪个 agent 在做哪个任务）+ 制品状态 + 自动刷新。

【A】A-8: **OpenSpec VS Code 扩展**（randysss/openspec-workflow）：**"Recommended actions" 行动栏 = 最多 3 条下一步**，按 **Needs Attention → Ready to Verify → Recommended** 三级优先级排序（resolver-backed）——比「需要你/NEXT」的平铺队列多一层**优先级分类**。

### 4.2 架构与代码流程（diagram-as-code）

【A】A-9: **AgentLens**（Salesforce，开源）：单份 execution trace → **三层联动视图**——**agent DAG**（谁与谁交接、顺序是否对）/ **子代理内部 FSM 图**（状态与转移、为何分叉）/ **逐步执行 inspector**；**零依赖、完全离线、数据不出机**。

【A】A-10: **AgentTracer / tracesage**：**JSONL（append-only、人可读）+ 本地 dashboard**（timeline 视图 / 图视图 / 嵌套 span / 过滤 / diff 视图 / **fork-merge DAG**），`pip install` 即用、`localhost` 打开——「事件流即视图数据源」范式。

【A】A-11: **AgentGUI**（ETH Zürich，arXiv 2607.26300）：轨迹可视化使**关键要素识别快 38%（p=0.023）**；自动防漂移使 0.8B–9B 小模型任务完成率**最高 +34pp**——可视化的收益有受控实验支撑，非主观偏好。

【A】A-12: **`spec-kit-v-model` 的 `trace` 命令**：产出**双向 RTM**（Matrix A 验证 + Matrix B 确认）+ **gaps（需求无测试）/ orphans（测试无需求）显式分区** + **版本基线**（制品 hash / timestamp 证明矩阵对应当前版本）+ **粒度执行状态五态**（⬜Pending / ✅Passed / ❌Failed / 🚫Blocked / ⏸Deferred）。

【A】A-13: **RQML**（`requirements.rqml` 单文件 + VS Code 扩展 + `@rqml/cli`）：`rqml check` 在 CI 非零退出；且官方**明示**「任何编辑器扩展都无法否决文件保存，CI 层才是权威门」——与本仓「hook = 诚实护栏、非绝对强制」的定位同构。

【A】A-14: **Structurizr**（C4 模型参考实现）：**models-as-code**，一份模型产出多张架构图；**可直接发布 ADR**；替代可视含树视图与力导向图；提供 **MCP server** 供 agent 读写模型。

【A】A-15: **LikeC4**（5.4k★，"always actual and live diagrams from your code"）/ **Archlette**（code as source of truth + **pre-commit hook** 保图不腐）/ **Kroki**（4.3k★，文本 → 图，覆盖 C4 / PlantUML / Graphviz / Mermaid，**可 CI 渲染**）；配套经验共识 = **Mermaid 三优**（git-diffable / LLM-native / CI 可渲）。

## 5. 同构映射与本仓落点

### 5.1 三层视图映射（社区形态 → 本仓真值源）

| 视图层 | 社区对应 | 本仓真值源 | 零依赖可得 |
|--------|---------|-----------|-----------|
| **制品链 / 步骤时间线** | A-5 制品链、A-6 七阶段时间线、A-7 泳道 | `spec/<feature>/` 四文档 + `sessions` 决策链 step_id 序列 + `STEP_SEQUENCE` 五步序表 | ✅ 是 |
| **决策链状态机** | A-9 FSM 图、A-10 fork-merge DAG | `sessions/*.jsonl` 事件流（`seq` + `gate` + `decision.metadata.step_id/step_seq`） | ✅ 是 |
| **架构 / 代码流程** | A-14 C4、A-15 diagram-as-code | `scripts/*.py` + `.pre-commit-config.yaml` 五 hook + `tools/spec_runner` 模块 | ✅ 是（Mermaid） |
| **追溯与覆盖** | A-12 双向 RTM + gaps/orphans、A-13 `rqml check` | `repo_stats.py` 三通道对账（已具备 gaps 语义）+ `verify-anchor` 锚点核查 | ✅ 已具备 |

【A】A-16: **本仓真值源机械盘点（E1 枚举）**：`spec/` 子目录 **32** 个（含本目录）/ `sessions` 内 `specwf-p*` 会话 **22** 个（含决策链）/ `scripts/` 脚本 **7** 个 / pre-commit hook **5** 个 / ADR **8** 份 / `STEP_SEQUENCE` 五步序表——**三层视图所需的全部输入已在仓内，无需新增采集面**。

### 5.2 必须继承的约束（C-6 / C-7 传承）

- **零新依赖**（stdlib only）、**无常驻服务器**、**markdown-native（Mermaid）**、**纯派生可重生成**
- 视图**只读、不持有真值**（I-6 不增真值）；覆盖无需备份（派生物例外）
- 沿用 P-041 已验证机制（[board-gen hook](../../.pre-commit-config.yaml)）+ 既有三校验器兜底「声明 = 重数」

### 5.3 剥离裁定（底座 vs fork）

现状：看板能力的**触发来源**写在 [academic-writing-workflow RESEARCH](../academic-writing-workflow/RESEARCH.md) §11 的 **C-7**——即通用看板**寄生于学术推理这一深度改造 fork**。用户裁定：可视化层属**通用底座**能力，应独立立项；`academic-writing-workflow` 侧降格为**来源指针**；P-041 [board-generator](../board-generator/DESIGN.md) 记为本 feature **前身（L0 首落点）**，其归属迁移与多视图扩展在**实施批**执行。

## 6. ADR-0010 三问懒加载 gate 判定

| 问 | 判定 | 依据 |
|----|------|------|
| **Q1 放哪层** | **Layer-1**（工具层：生成端派生视图，**不接验证端门禁**） | 视图不参与 gate 裁决，与 `step-enforce` / `verify-anchor` 正交 |
| **Q2 激活条件** | **已满足**（用户显式指令 + 本批已产出 RESEARCH + 落点/关系已裁决） | 但**实施范围待实施批裁决**（视图清单与承载形式见 C-4） |
| **Q3 未激活副作用** | **0**（本批零工具改动、零新依赖、零新文件于 `scripts/`） | I-1：未激活即零足迹 |

**本批判定 = 止于懒加载 gate**（同 P-037 / P-039 先例）：调研落档 + 决策链，不实施。

## 7. 补充调研与补充分析（v1.1 四项 / v1.2 三题 / v1.3 三题）

> 触发：**v1.1** = 用户指令「遗留问题进行补充调研」（§7.1-§7.4，四项 H1~H4，全部关闭假设）；**v1.2** = 用户指令「…请补充分析」（§7.5-§7.7，三题：描述列 / 架构与流程交互 / 新视图暴露的真实问题）；**v1.3** = 用户对 P-044 产物的实施反馈 + 剩余待办（§7.8-§7.10，三题：hook 链表乱码与可读性 / 步骤级动态描述 / 剩余待办）。三轮均取「社区实证 + 本仓可核」双通道；**v1.3 的主证据是 P-044 真实产物的机械核对**（E1）。

### 7.1 H1 状态词表口径（对齐原词 vs 独立状态机）

【A】A-17: **OpenSpec UI 的视图状态与 CLI 共用同一套词表**——per-change 制品状态（written / ready to write next / blocked）明示 "same vocabulary as `openspec status`, read straight from disk"：视图**不另造标签**，只做既有词表的重投影。

【A】A-18: **SpecKit Tracker 的 7 阶段不是人工状态列，而是由制品存在性推断**——constitution / specify / clarify / plan / tasks / checklist / implement 各绑定关键制品（`constitution.md` / `spec.md` / `plan.md` / `tasks.md` / `checklists/*.md`），阶段进度 = 制品 + `- [x]` 勾选的**机械重数**。

【A】A-19: **看板 UX 研究的共识 = 列必须是「小、有序、团队真实在用」的状态集，且每列需有进入/退出条件（DoR/DoD）**；列头承载 count / limit / sum，使**列头本身即状态行**（2026 板式模式综述）；中文项目管理看板五要素同样把「统一状态语言 + 每列进入/退出条件」列为要素 2。

**判定 → C-5**：采用**派生状态机**——状态由既有证据机械计算（`PROGRESS` 状态列 + `step-gate` exit 0/1/2 + `verify-anchor` 硬/软 + 软性存疑），**词表与 PROGRESS 原词对齐**（禁止「待你审」这类升格标签），每个状态附进入/退出条件（本仓 step-gate 三类规则即现成退出条件）。

### 7.2 H2 视图主键粒度（feature vs P）

【A】A-20: **三种粒度在不同开源工具里分层并存**——SpecKit Tracker 以 **feature 目录** 为列表主键（`specs/###-feature/`，阶段为二级）；OpenSpec UI / MCP 以 **change** 为主键（spec / task 为二级）；Spec Kitty 以 **task 为卡片**、feature 作泳道（`planned → doing → for review → done`）。

【A】A-21: **Racc 的 UI 设计（含认知科学约束）**：按**状态类别**分组（needs attention → running normally → completed），使「管理 10 个」感觉像「管理 3 类」；每张卡压缩为**单一认知块**（状态色 + 描述 + 进度 + 耗时），并显式对齐 **Cowan 4±1** 工作记忆上限。

【A】A-22: **活动列须设卡片上限**——看板实践建议「Today / This Week」列严格限制 **5~7 项**，其余入 Backlog 不外显；并建议 WIP 限制（In Progress 2~3）与「阻塞列胜于阻塞标签」。

**判定 → C-6**：采用**双主键分层**——**feature 为分组键**（一行认知块，32 个目录）、**P 为事项键**（卡片，42 项）；活动区卡片上限按 5~7 收紧，`done` 段折叠（P-041 已取「最近 8 条」方向一致，但**未设活动区上限**）。

### 7.3 H3 自包含静态 HTML 与渲染依赖

【A】A-23: **官方 `@mermaid-js/mermaid-cli` 渲染需 Node.js 18.19+，且 Puppeteer 为 peer 依赖、需 Chromium/Chrome headless**（首次运行会下载浏览器）；Go 重写版 `mermaid-cli` 亦「**Requires Chrome or Chromium at runtime**」；Neos 集成实作需 `npx puppeteer browsers install chrome-headless-shell`。→ **自建渲染 = 引入 Node + 浏览器二进制，违本仓零依赖定位**。

【A】A-24: **Mermaid 可直接由既有宿主渲染**——社区工具（如 `py-dep-visualizer`）以 Mermaid 为默认输出格式并明示「paste this into any Mermaid renderer（**GitHub markdown, Notion, mermaid.live**）」，无需自建 renderer。

**判定 → C-7**：承载**限定为 markdown 内嵌 Mermaid**（依赖宿主渲染）+ 可选**纯 CSS 折叠**（`<details>`）；**排除** mmdc 自建渲染与自包含静态 HTML——H3 原假设的「无 JS 构建下可读性上限」随之**消解为不适用**，而非留作待测假设。

### 7.4 H4 依赖图是否需要显式元数据

【A】A-25: **`py-dep-visualizer` 仅用 Python 标准库 `ast` 即可生成 import 依赖图**（"using only the standard library `ast` module"、"without executing a single line of code"），支持 Graphviz DOT / **Mermaid** / JSON 输出。

【A】A-26: **AST 静态解析优于文本解析**（免注释 / 多行 / 别名陷阱，直接得结构化节点）；两遍 AST（先 import、后调用/IO）为社区通行做法；**已知局限 = 动态 import（`__import__` / `importlib.import_module`）静态不可见**。

【A】A-27: **本仓 hook 链已是结构化声明，无需推断**——`.pre-commit-config.yaml` 为 `repo: local` + `hooks:` 列表，每项含 `id` / `name` / `entry` / `language` / `files`（/ `pass_filenames`）字段（本机原文核对，E1）。

【A】A-28: **本仓动态 import 实测仅 1 处，且为字面量形式**——`scripts/deepeval_m7_eval.py` L19 `import importlib` / L109 `importlib.import_module("deepeval")`（可选依赖懒加载门控，E1 机械枚举）。**字面量实参可被 AST 常量提取覆盖**，故 A-26 的「动态 import 不可见」局限在本仓**可机械消解**（仅需一条「`importlib.import_module(<str 常量>)` → 记边」的补充规则）。

**判定 → C-8**：**不需要显式依赖元数据**——脚本依赖图用 stdlib `ast`（零依赖、可 CI、不执行代码），hook 链直接解析既有 YAML；A-26 的局限由 A-28 的**字面量补提取规则**覆盖（残留风险 = 非字面量动态 import，本仓实测为零）。

### 7.5 feature 视图「描述」列（v1.2）

【A】A-36: **feature 描述源的可核性实测**——`spec/<feature>/` 下四文档的 H1 标题**自带一句话描述**（如 `spec/project-console/RESEARCH.md` 的 H1 = 「调研文档：项目控制台——可视化看板剥离与视图分层（P-042）」）；但**并非每个 feature 都有 RESEARCH**：机械枚举 32 个 feature 目录，**7 个缺 RESEARCH**（agents-md-bridge / board-generator / cpp-hub-absorption / decision-schema / defect-fixes / doc-contract / step-gate），其中 `doc-contract` 四文档全缺 → **必须设计描述回退链**（E1）。

**判定 → C-9（描述列裁定）**：

- **来源优先链**（逐级回退，取首个非空）：① `RESEARCH.md` H1 标题 → ② `DESIGN.md` H1 → ③ `CHECKLIST*.md` H1 → ④ 关联 P 行的「事项」列 → ⑤ 目录名（兜底）；
- **不引 `CODE_WIKI §9` 行文本**——§9 是**视图层**（由 `repo_stats` 对账的派生视图），从派生物取描述会形成「视图依赖视图」，违 I-6 精神与单一真值源纪律（B6）；
- **单行截断**：取 H1 中「：」或「——」之后的主名，并设字符上限（**上限值待 H6 实测**）。

### 7.6 项目架构流程 × per-feature 流程 × 交互选择（v1.2）

【A】A-29: **GitHub 官方支持 `<details>` / `<summary>` 折叠**——`<details>` 块内 markdown 在用户点击前折叠；`<details open>` 可默认展开；官方文档明示该特性用于「按需展开技术细节」；GFM 允许元素清单含 `<details>`/`<summary>`，且在 `.md` / Issue / PR / Wiki 均支持（E2 官方文档）。

【A】A-30: **GitHub 渲染器剥离一切交互能力**——`<script>` / `<style>` / `class` / `style` 属性 / `onclick` 等事件处理器**均被剥离**，定位为「**No interactivity on GitHub**」（`<script>`/`<style>` 属 GFM 规范显式中和的标签）→ markdown 内**无 JS、无自定义样式**（E2）。

【A】A-31: **Mermaid 官方 schema 的 `securityLevel` 默认即禁用点击**——`"strict"`（**默认**）= HTML 标签编码 + **click functionality is disabled**；`"loose"` = 允许 HTML + **click 启用**；`"antiscript"` = 允许 HTML 但移除 script + click 启用；`"sandbox"` = iframe 沙箱且「可能阻碍图内交互功能」（E2 官方 config schema）。

【A】A-32: **`securityLevel: "loose"` 是已登记的 XSS 载体（三起独立实证）**——① OneUptime **CVE-2026-32308**（高危 stored XSS：`loose` + `innerHTML` 注入使 `click` 指令可执行任意 JS）；② ai-code-reviewer #52（LLM 生成的 Mermaid + `loose` = 任意 JS 执行，攻击面来自 prompt injection）；③ BaseIntelligence #21400（Tauri webview 内 `loose` 使 click 可触达 IPC 桥）→ **图内点击交互在本仓不可控渲染器下既不可得也不应引入**（E2/E4）。

【A】A-35: **本仓脚本 import 图实测为空**——P-043 产物 `docs/CONSOLE.md` 的「架构与流程」实测输出 `（无仓内 import 边）`：7 个脚本 + `spec_runner` **相互零 import**（各自独立可执行），唯一动态 import 指向**外部** `deepeval` → 以「import 图」为架构视图口径时**信息量为零**（E1，可复跑核验）。

**判定 → C-10（默认层 + per-feature 流程 + 交互形态）**：

- **默认层 = 项目级「架构与流程」**（现状 §5 保持，口径按 C-12 修正）；per-feature 流程为**次级层、默认折叠**；
- **per-feature 流程视图** = 新增 **§5.1「per-feature 流程（折叠）」**：每 feature 一个 `<details>`，`<summary>` 显示「{feature}｜{阶段}｜{关联 P}」，体内含 ① `flowchart LR` 的**四文档管道**（R→D→I→C 逐节点标 ✓/—）② 该 feature 关联 P 的**决策链 step 序列**（取自 sessions）③ 派生状态与依据（复用 C-5）；
- **交互形态 = `<details>` 折叠 + 顶部 feature 锚点目录**——A-29/A-30 表明这是 markdown 内**唯一可得**的「按需展开」；`open` 属性可控制默认态；
- **排除 Mermaid `click` 图内跳转/切换**——A-31 默认 `strict` 即禁用 click；A-32 三起 XSS 实证表明启用 `loose` 会引入执行面；而本仓**无法控制宿主渲染器的 securityLevel** → 该路径**不可得且不安全**；
- **体积策略**（H7 待实测）：仅对「四文档不全 **或** 有 session」的 feature 生成折叠图，其余保留 §2 行，避免展开面膨胀。

**判定 → C-12（架构图口径修正——对 C-8 的部分修正）**：

- C-8 的前提「stdlib `ast` import 图足以表达架构」**被 A-35 部分证伪**（实测空图）→ **改「显式关系」口径**：① `hook → script`（`.pre-commit-config.yaml` 已结构化，A-27）② `script → 真值源`（已知常量：dc_validator→全 `.md` / m7_stats→M7 账本 / repo_stats→视图载体 / console_gen→PROGRESS+sessions+spec / step_enforce→PROGRESS）③ **保留** import 边与动态 import 清单（有则绘，无则不占位）；
- ② 引入的是**显式架构契约声明**（Layer-0 文档化），**与 C-8「不需要显式元数据」不矛盾**——C-8 否决的是「为**推断 import** 而加元数据」，此处是「以**已声明的契约**替代不可得的推断」，且不新增采集面；此取舍与社区两派一致（A-14 Structurizr「models-as-code」显式模型派 vs A-15 LikeC4/Archlette「code as source of truth」推断派）——本仓因推断源（import）为空而**取显式派**。

### 7.7 新视图暴露的真实问题（v1.2）

**问题一：脚本依赖图为空（A-35）** → 已并入 **C-12**（换口径，非缺陷）。

**问题二：feature → P 映射存在 4 个空洞**

【A】A-33: **空洞根因（E1 实测）**——`step_enforce` 与 `console_gen` 共用同一映射语义「P 行内**首个** `spec/<feature>/` 链接」，而该约定在旧批次被用于**引用上游依据**：实测 `P-009 → langgraph-upgrade`、`P-010 → langgraph-upgrade`、`P-011 → cpp-hub-absorption`、`P-016 → semantica-absorption`（**均指向触发来源/前置依据，而非本批产出**）→ `spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema` 四个 feature **永远拿不到 P**；且 `langgraph-upgrade` 被 P-009/P-010 重复认领（末行胜出 = P-010）。

【A】A-34: **同一事实在另一源中是正确的**——`CODE_WIKI §9` 索引行**均带正确 P 编号**（`spec/spec-runner` = P-009 / `spec/promptfoo-m7-eval` = P-010 / `spec/m7-hits-block` = P-011 / `spec/decision-schema` = P-016；原文核对，E1）→ **两源对同一映射不一致**，属「同一事实双源漂移」（本仓「声明 = 重数」纪律的既有拦截对象类型）。

**判定 → C-11（映射空洞裁定）**：

- ① **保留 `—` 为显式缺口**——诚实优于静默补全（静默补全会让「缺映射」这一**真实缺陷**从视图上消失，违本仓反幻觉纪律）；并在 §6 追溯覆盖中**显式列出缺映射清单**；
- ② 引入 **`CODE_WIKI §9` 行的 P 标注为第二映射源**，并**显式声明优先级**：`PROGRESS 行首链接`（以本批产出为主）→ `§9 行标注`（补缺）→ `—`（显式缺口）。§9 行虽在 `CODE_WIKI` 内，但该表是**人工维护的索引**（非派生），属真值源侧，可接受（须在 DESIGN 写明）；
- ③ **收敛双实现**——`step_enforce.build_feature_pid_map` 与 `console_gen.feature_pid_map` 是**两份同语义实现**（漂移风险已有实证：两者对同一批数据给出**相同错误**映射）→ 收敛为**单一映射函数**（一处实现、另一处复用），符合「单一真值源」精神；
- ④ **不改历史 PROGRESS 行**（历史叙事改写成本高且会扰动既有链接审计）——以 ②③ 在读取端解决。

### 7.8 hook 链表的乱码与可读性（v1.3）

【A】A-37: **表列数不齐（机械确证，P-044 产物实测）**——`docs/CONSOLE.md` §5 hook 链表的**表头 5 列**，但第 1/2 行 = 5 cells 而**第 3/4/5 行 = 11 / 8 / 10 cells**。根因 = `hook_chain` 把 `files:` 正则**原样**塞进表格单元格，而正则内含**未转义的半角 `|`**（如 `^(CODE_WIKI\.md|README(\.en)?\.md|...)`），被 GFM 当作**列分隔符** → 表格结构被破坏、渲染错位。**这是视图自身破坏渲染的 P1 缺陷，不是宿主或字体问题**（E1，可复跑核验）。

【A】A-38: **表格单元格不适合放长无断点 token**——Markdown 表格按内容宽度分配列宽，**长无断点 token（长正则 / 长路径 / URL）不换行**，会撑宽本列并把后续列**挤压到 5–10 px**（社区实证：react-markdown 表格末列被压至不可读；另一实作则以 `overflow-wrap: anywhere` + `break-word` 修复）；且 GitHub **不截断**单元格文本（只有长文本换行，无省略号）。→ 现设计把**最长的正则**放进**最宽的列**，是「看不懂 + 乱码」的共同成因（E2）。

【A】A-39: **hook 的 `name:` 字段已在真值源中却未被解析**——`.pre-commit-config.yaml` 每个 hook 均含 `name:`（人类可读作用，如 `DC contract validator (DC1-DC4 + R7)`），但 `hook_chain` 只取 `id` / `entry` / `files` / `pass_filenames`。**「看不懂」的一半原因 = 该取的字段没取**，而修正**零新增采集面**（同一文件已直读）（E1）。

**判定 → C-13（hook 链表重构）**：

- **形态改为逐 hook 列表块**（放弃表格）：每项 `**{id}** —— {name}` + 缩进三项（`命令` / `触发范围`（`files` 正则**独立成行**）/ `传入文件名`）。理由：A-38 表明长正则落表格单元格必然压列；列表块让长 token 独占一行，**从形态上消除压列**；
- **补 `name`（作用）**：`hook_chain` 增解析 `name:`（A-39）；**缺 `name` 时显式 `—`**（I-8）；
- **竖线一律安全化**：`files` 正则内的 `|` → `｜`（全角）或转义为 `\|`；且**该修法提升为通则**——凡进入表格/列表的**外部文本**必须过统一安全化函数（P-044 仅对描述列做了 `_cell()`，**hook 表遗漏 = 本缺陷直接成因**）；
- 附带：`entry` 去掉 `python ` 前缀冗余展示可保留原样（**不做美化转述**，避免与真值源产生第二叙事）。

### 7.9 步骤级动态描述（主题 / 创建时间 / 简要描述 / 修改历史）（v1.3）

**问题**：per-feature 流程当前只有 `R→D→I→C` 四节点 ✓/—，**没有每步的动态信息**——看不出「这步做了什么、什么时候做的、结论是什么、改过几轮」。

**双通道取证**：

【A】A-40: **事件流产出主源齐备（E1 机械枚举）**——`tools/spec_runner/sessions/` 共 **31 个 `specwf-p*.jsonl`**、**130 条 `decision` 事件**；逐条核验 `input.scenario` / `input.outcome` / `input.reasoning` —— **100% 齐备（零缺失）**。step 分布 = `research 30 / design 26 / implement 25 / verify 25 / finalize 24`（差额来自「只跑到 research 的批次」与「补建/多轮 session」）。

【A】A-41: **四文档 H1 全量齐备**——32 个 feature 目录下 **77 个四文档 .md，无一缺 H1**（`# …` 首行）→ 「主题」可**全量兜底**，不依赖事件流。

【A】A-42: **文档元数据源稀疏且命名漂移（E1 机械盘点）**——`创建日期` 行 **50/77**；`Spec 步骤` 行 **54/77**；front-matter（`date` + `version` 同现）仅 **25/77**；文档内**「修订历史」类章节仅 13/77**，且标题形态**四种以上**（`5. 修订历史` / `7.5 修订历史` / `附录 D：变更日志详档` / `7. 上游修订注` …）→ **不可作首选机械来源**（命名无稳定契约，抽取即幻觉风险）。

【A】A-43: **步骤↔制品映射在文档内有自声明**——`> **Spec 步骤**: Step X-Y` 行 **54/77**（如 RESEARCH = `Step 1-2`、IMPLEMENTATION = `Step 5-6`、CHECKLIST = `Step 7-8`）→ 映射应以**文档自声明为主源**、常量兜底，而非在生成器里硬编一份可能与文档漂移的表。

**判定 → C-14（四字段来源链：以事件流为主源）**：

| 字段 | ① 主源 | ② 回退 | ③ 回退 | ④ |
|------|--------|--------|--------|---|
| **主题** | 该 step 的 `scenario`（事件流） | 该制品 H1 主名 | — | — |
| **创建时间** | 该 step 的 `ts` | 制品 `> **创建日期**:` 行 | front-matter `date` | `—` |
| **简要描述** | 该 step 的 `outcome`（截断） | — | — | `—` |
| **修改历史** | 该 P 的 **session 轮次清单**（`specwf-pNNN-*` 多文件 → 轮次 + 各自 ts + 最远 step） | 制品 front-matter `version` | — | `—` |
| **制品↔步骤映射** | 文档自声明 `Spec 步骤` 行（A-43） | 常量兜底（research→RESEARCH / design→DESIGN / implement→IMPLEMENTATION / verify→CHECKLIST；finalize 不新增制品） | — | — |

- **主源为事件流 = 零新增采集面**（`read_sessions` 已在读同一批文件）；
- **缺失一律显式 `—`**（I-8）；无 session 的 feature 其「主题/时间/简要/修改历史」全列 `—`——这是**真实的决策链缺口**，应可见而非用文档元数据「补得像有」；
- **超出四字段的裁剪**：`reasoning`（往往数百字）**不进视图**，只保留 `outcome` 一句（避免把折叠块变成读全文的入口，违 C-6「单一认知块」）。

### 7.10 剩余待办（v1.3）

**（一）锚点形态（原「`<a id>` 存活率」残留风险）**

【A】A-44: **官方背书的形态是 `<a name="…">` 而不是 `<a id="…">`**——GitHub 官方文档「Custom anchors」节明示：用标准 HTML 锚标签 **`<a name="unique-anchor-name"></a>`**；并注明「**Custom anchors will not be included in the document outline/Table of Contents**」。**`<a id>` 无官方背书**：另有第三方技术文称 GitHub 会「**在允许的标签上一并剥离 `class`/`id`**」，与官方文档**相互冲突**；而 HTML5 中 `name` 已弃用、`id` 才是标准（MDN），GitHub 之外（如 Doxia）已实测出现「只认 `id` 不认 `name`」的分歧 → **两形态各有失效面，且本机无法验证远端渲染**（E2，含**低可信度来源**，已标注）。

**判定 → C-15（锚点改双属性保险）**：输出 `<a name="feat-{f}" id="feat-{f}"></a>`（**同时给 `name` 与 `id`**）——覆盖「只认 name」与「只认 id」两类渲染器，成本为每锚多一个属性；**若宿主两者皆剥离**，退化为「**可折叠但不可跳转**」（默认视图与折叠功能不受影响）→ 登记为 **H8**（真机存活率待验）。

**（二）H6 / H7 回填**

- **H6（描述列长度上限）**：A-38 提供**间接依据**——长 token 压列、末列被压至不可读，故保留短描述**有机制性理由**；`DESC_CAP = 40` 由「纯待测取值」升级为「**取扫描性阈值以避免压列**」。但**列宽真机的具体截断点仍未实测** → **H6 不关闭**。
- **H7（per-feature 体积预算）**：A-45 表明折叠块**无数量上限**（官方仅约束「`<summary>` 后需空行」「嵌套 ≤ 4 层」），26 块属**认知负载**问题而非技术限制；实测 26 块 / 514 行 / 20027 B 未失控 → **H7 部分回填、不关闭**（真机浏览体验待确认）；建议保留收敛策略并采用**稳定排序**（阶段 → P 号），保证同源双跑与跨轮可比。

【A】A-45: **折叠块的官方约束与该约束之外**——官方文档给出 `<details>` + `<summary>` 的用法与 `open` 默认态；社区实证补充两条硬约束（`<summary>` 后需空行、**嵌套最多 4 层**）与一条**非约束**（无数量上限）（E2）。

**（三）C-11 映射语义的再修正**

**A-33（复述，非新增断言）**: **失效形态是「两实现同错」**——`step_enforce.build_feature_pid_map` 与 `console_gen.feature_pid_map` 共用「P 行内**首个** `spec/<feature>/` 链接」语义，而该位置在 P-009/010/011/016 被用于**引用上游依据**，导致 4 个 feature 永远拿不到 P。**关键推论：一致性对账无法发现该缺陷**（两个实现给出一致的错误答案）。

**判定 → C-16（映射来源语义与收敛，修正 C-11 ②③）**：

- **① 改语义（核心）**——映射优先级**反转**为：**`CODE_WIKI §9` 行标注（人工维护索引，对 4 个空洞均为正确值）优先** → `PROGRESS` 行首 `spec/<feature>/` 链接兜底 → `—` 显式缺口。理由：A-34 已证 §9 对四个空洞**全部正确**，而 §9 是**人工索引（真值源侧）**而非派生视图；把「按约定易被误用」的行内位置降为兜底，才能从语义上消解该缺陷类别；
- **② 收敛（修正 C-11 ③）**——因语义变更必须同时落到两处，三选项对比：
  - (a) **抽共享纯函数模块**（如 `scripts/spec_map.py`，两处复用）→ **选择**：唯一能保证「语义同源」的做法；代价 = `scripts/` 增 1 文件（视图层 `declared.scripts` 7→8）；
  - (b) 双实现 + 一致性对账 → **证伪**：A-33 表明「两实现同错」可通过对账，对账**抓不住该类缺陷**；
  - (c) 只改一处 → 制造**双语义**，比双实现更坏。
- **③ 不改历史 PROGRESS 行**（维持 C-11 ④）：读取端解决，历史叙事零扰动；
- **④ 与 C-11 ① 的关系**：`—` 仍为显式缺口（I-8），但**预期缺口数由 4 → 0**（四个空洞被 §9 补上）；若 §9 亦无标注，则保留 `—` 并计入 §6 缺映射清单。

**§7.10 追记（P-047 及收口修正批执行结果，2026-09-11 —— 用户指令「执行 C-15 和 C-16」→「P-047 是否完全闭环 → 执行 A+B+C+D（含独立 pass 与入库）」）**

- **C-15 已执行**：折叠块锚点落为**双属性** `<a name="feat-{f}" id="feat-{f}"></a>`（`scripts/console_gen.py`）；真实仓 **26/26 双属性锚**（selftest S20 改断言）。**H8 仍不关闭**——真机存活率本机不可验；残余风险面收窄为「两者皆被剥离」（后果仅「可折叠不可跳转」）。
- **C-16 已执行**：① 语义反转落地（`CODE_WIKI §9` 行标注**优先** → `PROGRESS` 行首链接**兜底** → `—`）；② 收敛落地 = 新增 **`scripts/spec_map.py`** 为**唯一实现**（`console_gen` / `step_enforce` 删除本地实现改为复用；建立不变式 **I-10 语义同源**）；③ **不改历史 PROGRESS 行**（读取端解决）。实测：**映射差异 13 项**（4 空洞补齐 + 9 主 P 归位）。
- **判据的必要不充分（B5，收口批提取）**：C-16 ④ 的验收判据「**缺口 4 → 0**」只覆盖**缺值**（`None`）、**不覆盖错值**（有值但指向错误对象）。收口批复核发现 `cpp-hub-absorption` 在旧新语义下**同取 P-011**（错值，应为 P-002）→ **不进入缺口统计**，却仍造成视图内事实错误。故该类「收敛到唯一来源」改造的验收须并核**来源分布**（多少 feature 仍依赖兜底源），而非只看缺口计数。
- **残余已消解（收口批）**：`CODE_WIKI §9` 补两行标注（`cpp-hub-absorption → P-002` / `cpp-hub-gap-analysis → P-004`）→ **兜底面 32/32 归零**（依赖兜底 2 → 0），`cpp-hub-absorption` 错值 **P-011 → P-002** 一并消解；**映射差异收口批后 14 项**（13 + 错值消解 1）。C-16 ④「计入 §6 缺映射清单」原为**声明未落地**，收口批补 `_trace_section` 缺映射行后真正落地（真实仓输出「（无——32 个 feature 全部有映射）」）。
- **独立 pass 更正（RULE-5 同基座降级）**：v1.3 实测记述中「消除 `precommit-dc-validator` P-008 无 session 误阻断」**不可复现**——P-008 与 P-007 同为 P-020 前批次 → **均**历史豁免 → hook 层 exit 0；旧语义实际消解的是 **4 个无映射 feature 的 hook exit 2**（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema`）。详见 [CHECKLIST §8.2](./CHECKLIST.md)。
- **状态**：C-11 / C-15 / C-16 **全部关闭**；H6 / H7 部分回填**不关闭**；H8 待真机。本节（一）（二）（三）三项判定均已执行或保持观察。

## 8. 参考文献

- OpenSpec UI：https://github.com/ToruAI/openspec-ui
- SpecKit Tracker（VS Code 扩展）：https://open-vsx.org/extension/summitpatil/speckit-tracker
- OpenSpec VS Code 扩展：https://open-vsx.org/extension/randysss/openspec-workflow
- OpenSpec MCP（含 Web dashboard）：https://github.com/Lumiaqian/openspec-mcp
- Spec Kitty：https://github.com/bruj0/spec-kitty
- GitHub Spec Kit：https://github.com/github/spec-kit
- AgentLens：https://github.com/forcedotcom/AgentLens
- AgentTracer：https://pypi.org/project/agenttracer-ai/
- tracesage：https://github.com/kjgpta/tracesage
- AgentGUI（arXiv 2607.26300）：https://arxiv.org/html/2607.26300v1
- Structurizr：https://structurizr.com/
- Structurizr 社区工具：https://docs.structurizr.com/community
- LikeC4：https://github.com/likec4/likec4
- Archlette：https://github.com/chrislyons-dev/archlette
- Kroki：https://github.com/yuzutech/kroki
- spec-kit-v-model `trace` 命令：https://github.com/leocamello/spec-kit-v-model
- RQML for VS Code：https://marketplace.visualstudio.com/items?itemName=rqml.rqml-vscode
- Codex CLI 架构图工作流：https://codex.danielvaughan.com/2026/05/13/codex-cli-architecture-diagrams-mermaid-c4-plantuml-source-code-visualisation/

**v1.1 补充（§7 遗留四项）**:

- mermaid-cli（官方，Node + Puppeteer/Chromium）：https://github.com/mermaid-js/mermaid-cli
- mermaid-cli（Go 重写版，运行时需 Chrome/Chromium）：https://github.com/coolamit/mermaid-cli
- Mermaid MCP Server（Puppeteer 自动下载 Chromium 实证）：https://github.com/abekdwight/mermaid-mcp-server
- Neos Flow Mermaid 集成（`chrome-headless-shell` 安装实证）：https://github.com/fucodo/flow.mermaid
- Jekyll Mermaid Prebuild（mmdc + Puppeteer 依赖说明）：https://github.com/texarkanine/jekyll-mermaid-prebuild
- py-dep-visualizer（仅用 stdlib `ast` → Mermaid / DOT / JSON，不执行代码）：https://github.com/jishanahmed-shaikh/py-dep-visualizer
- Python Code Flow Graph Maker（AST 两遍解析：import → 调用/IO）：https://github.com/virkha-kumari/python_codeflow_graph_maker
- 静态 import 图 vs 文本解析（AST 结构化优势）：https://habr.com/en/articles/946740/
- SaaS Kanban & Board View UX 模式（2026：列语义 / DoR-DoD / 列头承载 count·limit·sum）：https://www.saasui.design/blog/saas-kanban-board-ux-patterns
- 项目管理看板五要素（状态语言统一 + 每列进入/退出条件 + WIP 限制 + 阻塞显性化）：https://blog.csdn.net/weixin_45356695/article/details/157032134
- Professional Project Board Design（列设计 / Blocked 列 / 卡片解剖）：https://learn.oreate.ai/articles/professional-project-board-design-for-streamlined-team-workflows
- Why Kanban Boards Burn You Out（WIP 限制与「活动列 5~7 项」上限）：https://www.taskloco.com/articles/why-kanban-boards-burn-you-out-and-the-visual-fix.html
- Racc UI Design（状态类别分组 + 单一认知块 + Cowan 4±1 + 主动微介入）：https://github.com/liu1700/racc/wiki/UI-Design

**v1.2 补充（§7.5-§7.7 三题）**:

- GitHub 折叠区块（`<details>`/`<summary>`，含 `open` 默认态）：https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections
- GFM 规范（`<script>`/`<style>` 显式中和；「No interactivity on GitHub」）：https://github.github.com/gfm/
- Mermaid 配置 schema（`securityLevel` 默认 `strict` / `loose` 启用 click）：https://mermaid.js.org/config/schema-docs/config.html
- Mermaid 安全说明（XSS 与 `securityLevel` 取舍）：https://mermaid.js.org/config/usage.html
- OneUptime CVE-2026-32308（`loose` + `innerHTML` → stored XSS）：https://github.com/advisories?query=CVE-2026-32308
- ai-code-reviewer #52（LLM 生成 Mermaid + `loose` = 任意 JS 执行 / prompt injection 攻击面）：https://github.com/ai-code-reviewer/ai-code-reviewer/issues/52
- BaseIntelligence #21400（Tauri webview 内 `loose` 使 click 触达 IPC 桥）：https://github.com/BaseIntelligence/BaseIntelligence/issues/21400

**v1.3 补充（§7.8-§7.10 三题）**:

- GitHub 官方 · 自定义锚点（**背书 `<a name="…">`**；明示 custom anchors 不进 outline/TOC）：https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#custom-anchors
- GitHub 官方 · 折叠区块（`<details>` / `<summary>` / `open` 默认态）：https://docs.github.com/en/enterprise-server@3.15/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections
- 锚点 `name` vs `id` 的渲染器分歧实证（Doxia 只认 `id`；引 GitHub 官方仍推荐 `name`；MDN 载 `name` 于 HTML5 弃用）：https://github.com/apache/maven-doxia/issues/1020
- 表格长 token 撑宽列、**末列被压至 5–10 px** 实证：https://github.com/Juliusolsson05/agent-code/issues/95
- 表格长文本**换行而非截断**的修复实录（`break-word` / `overflow-wrap: anywhere`）：https://github.com/dnl-fm/md/pull/13
- 折叠块实证约束（`<summary>` 后需空行；**嵌套 ≤ 4 层**；`open` 默认展开）：https://gist.github.com/pierrejoubert73/902cc94d79424356a8d20be2b382e1ab
- **【存疑来源 · 已标注】** 第三方技术文称 GitHub 会「在允许标签上一并剥离 `class`/`id`」（与官方文档冲突，未获一手证实）：https://www.mdtool.dev/blog/html-to-markdown-github

---

## 附录 A：A 类断言明细

- A-1 至 A-45：见 §3 / §4 / §5 / §7 各 `【A】` 行（本仓源码与机械核对 **17 条** = A-1~A-4 / A-16 / A-27 / A-28 / A-33~A-36 / **A-37 / A-39 / A-40 / A-41 / A-42 / A-43**；社区与标准案例 **28 条** = A-5~A-15 / A-17~A-26 / A-29~A-32 / **A-38 / A-44 / A-45**）。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "本仓真值源已足以派生三层视图（制品链/步骤时间线 + 决策链状态机 + 架构与代码流程 + 追溯覆盖），无需引入 Structurizr / Kroki / observability 平台等重栈；承载可维持 markdown-native（Mermaid）+ 可选自包含静态 HTML，零服务器零新依赖", "basis": "A-5/A-6/A-7 制品链与时间线形态 + A-9/A-10 事件流→视图 + A-14/A-15 diagram-as-code + A-16 真值源机械盘点 + C-6/C-7 既裁约束"},
  {"id": "B2", "inference": "本仓「决策链」与 AgentLens 的 FSM 视图同构——STEP_SEQUENCE 五步序表即状态集、gate 即转移守卫、事件流 seq 即状态历史，故决策链状态机视图可由 sessions 直接派生而无需新增元数据", "basis": "A-9 三层视图机制 + tools/spec_runner/spec_runner.py（STEP_SEQUENCE / cmd_gate_step）+ decision.metadata.step_id/step_seq 契约"},
  {"id": "B3", "inference": "剥离归属成立：可视化层属通用底座（Layer-1 工具层），academic-writing-workflow 的 C-7 仅构成来源线索、不构成归属依据；P-041 board-generator 可无损降格为前身（其单写路径/确定性/幂等不变式可被继承）", "basis": "用户架构裁定（底座 vs 深度改造 fork）+ P-041 DESIGN I-1~I-6 + ADR-0010 分层定义"},
  {"id": "B4", "inference": "状态词表的正确形态是「派生状态机 + 词表对齐」，而非给 PROGRESS 原词重贴标签——状态须由既有证据机械计算并附进入/退出条件，故「⚠ 待你审」这类升格标签应废止而非改名", "basis": "A-17 视图与 CLI 共用词表 + A-18 阶段由制品存在性推断 + A-19 列需进入/退出条件（DoR/DoD）+ 本仓 step-gate 三类规则 exit 0/1/2 即现成退出条件"},
  {"id": "B5", "inference": "视图宜采双主键分层（feature 为分组键 / P 为事项键）并给活动区设卡片上限，可在不增加认知负载的前提下同时表达「32 个 feature 的宏观进度」与「42 项事项的微观状态」", "basis": "A-20 三工具粒度分层并存 + A-21 状态类别分组与单一认知块（Cowan 4±1）+ A-22 活动列 5~7 项上限建议"},
  {"id": "B6", "inference": "feature 描述应取「制品自身 H1 标题」优先链（RESEARCH→DESIGN→CHECKLIST→P 行事项→目录名），而非引用 CODE_WIKI §9 的说明文本——后者虽信息最全，但属派生视图，引用它会形成「视图依赖视图」并使描述成为第二真值源", "basis": "A-36 描述源可核性（H1 自带描述；7 个 feature 缺 RESEARCH 故需回退链）+ I-6 不增真值 + repo_stats 对 §9 的既有对账关系"},
  {"id": "B7", "inference": "「手动交互选择 per-feature 流程」在 markdown 内唯一可得的形态是 <details> 折叠（+ 顶部锚点目录），默认折叠即等价于「默认展示项目级架构流程」；Mermaid 图内 click 因默认 strict 禁用且 loose 属 XSS 载体而不应引入", "basis": "A-29 <details> 官方支持（含 open 默认态）+ A-30 GitHub 无 JS/无 style + A-31 securityLevel 默认 strict 禁用 click + A-32 三起 loose XSS 实证"},
  {"id": "B8", "inference": "hook 链的正确承载不是表格而是逐项列表块——表格单元格按内容取宽，长无断点 token（正则）既撑宽本列又挤压后续列，且正向渲染无法容纳未转义竖线；列表块让长 token 独占一行，从形态上同时消除「列被压扁」与「表格被竖线破坏」两类缺陷", "basis": "A-37 表列数不齐机械确证（11/8/10 vs 表头 5）+ A-38 长 token 压列与不截断实证 + A-39 name 字段可得（可补「作用」使列表块自解释）"},
  {"id": "B9", "inference": "步骤级动态描述（主题/创建时间/简要描述/修改历史）的主源应是**事件流**而非文档元数据——事件流三字段 100% 齐备且天然按 step 切分，而文档侧的创建日期/版本/修订历史既稀疏（50/25/13 of 77）又命名漂移，以它为主源会把「缺记录」伪装成「无内容」", "basis": "A-40 事件流 31 session/130 rows 三字段零缺失 + A-41 四文档 H1 77/77 兜底 + A-42 元数据稀疏度与命名漂移 + A-43 步骤自声明映射 54/77"}
]
```

## 附录 C：C 类判断复盘 + 假设区

**C 类判断复盘**:
- C-1: **BOARD.md "简陋" 是结构性的，不是审美问题**——三组因全 `done` 恒空（A-2）+ 标签语义错配（A-3）+ feature 级 step 投影与脉络/架构/量化四维缺失（A-4）；改渲染样式无解，须补维度。
- C-2: **剥离裁定**——可视化看板独立为底座 feature `spec/project-console/`；**接续取代** P-041 board-generator（后者记前身）；`academic-writing-workflow` C-6/C-7 降格为来源指针。
- C-3: **分层与门禁**——Layer-1 只读派生视图（不接验证端门禁）；本批止于 ADR-0010 懒加载 gate，零代码改动；实施批再定视图清单。
- C-4: **承载形式**——markdown-native（Mermaid 优先，git-diffable / LLM-native / CI 可渲）+ 可选自包含静态 HTML（无服务器、无构建）；明示排除任何常驻服务与第三方前端工具链。**（v1.1 修正：其中「自包含静态 HTML」项已被 C-7 排除，C-4 现有效内容 = markdown 内嵌 Mermaid + 纯 CSS 折叠。）**

**v1.1 遗留四项判定（§7）**:
- C-5: **H1 状态词表裁定 = 派生状态机 + 词表对齐**——状态由 `PROGRESS` 状态列 + `step-gate` exit 0/1/2 + `verify-anchor` 硬软 + 软性存疑**机械计算**，词表沿用 PROGRESS 原词，废止「⚠ 待你审」这类升格标签；每状态附进入/退出条件。
- C-6: **H2 主键粒度裁定 = 双主键分层**——feature 为分组键（32 目录）、P 为事项键（42 项）；活动区卡片上限收紧至 5~7，`done` 段折叠。
- C-7: **H3 承载裁定 = 限定 markdown 内嵌 Mermaid（宿主渲染）+ 纯 CSS 折叠**；**排除** mmdc 自建渲染（Node + Chromium 违零依赖）与自包含静态 HTML。
- C-8: **H4 依赖元数据裁定 = 不需要**——脚本图用 stdlib `ast`（不执行代码、可 CI），hook 链解析既有 YAML；「动态 import 不可见」由**字面量补提取规则**覆盖（本仓唯一动态 import 位点即字面量形式）。

**v1.2 三题判定（§7.5-§7.7）**:
- C-9: **描述列裁定 = 制品自身 H1 标题优先链**——`RESEARCH.md` H1 → `DESIGN.md` H1 → `CHECKLIST*.md` H1 → 关联 P 行「事项」列 → 目录名；**不引 `CODE_WIKI §9` 文本**（避「视图依赖视图」，B6）；单行截断取主名（上限待 H6 实测）。
- C-10: **默认层 + per-feature 流程 + 交互形态裁定**——默认展示**项目级**「架构与流程」；per-feature 流程为次级层、**默认折叠**（新增 §5.1 `<details>` 折叠块，`<summary>` = 「{feature}｜{阶段}｜{关联 P}」，体内含四文档管道 `flowchart LR` + 决策链 step 序列 + 派生状态）；交互 = **`<details>` 折叠 + 顶部 feature 锚点目录**；**排除 Mermaid `click`**（A-31 默认 `strict` 禁用；A-32 `loose` 属 XSS 载体）。
- C-11: **映射空洞裁定 = 保留显式缺口 + §9 标注为第二源 + 收敛双实现**——① `—` 保留为显式缺口并在 §6 列出缺映射清单（诚实优于静默补全）；② 映射优先级 = `PROGRESS 行首链接` → `CODE_WIKI §9 行标注`（人工维护索引，属真值源侧）→ `—`；③ `step_enforce.build_feature_pid_map` 与 `console_gen.feature_pid_map` 收敛为**单一映射函数**；④ 不改历史 PROGRESS 行（读取端解决）。
- C-12: **架构图口径修正 = 改「显式关系」口径（对 C-8 的部分修正）**——A-35 实测 import 图为空使 C-8 前提被部分证伪 → 口径改为 ① `hook → script`（既有 YAML，A-27）② `script → 真值源`（显式契约常量）③ 保留 import / 动态 import 边（有则绘、无则不占位）；**与 C-8「不需要显式元数据」不矛盾**（C-8 否决的是为**推断 import** 加元数据；此处以**已声明契约**替代不可得推断，且不新增采集面）——取舍与社区 A-14 显式模型派 / A-15 推断派对齐，本仓因推断源为空而取显式派。

**v1.3 三题判定（§7.8-§7.10）**:
- C-13: **hook 链表重构裁定 = 逐 hook 列表块（弃表格）**——`**{id}** —— {name}` + 缩进 `命令` / `触发范围`（正则独立成行）/ `传入文件名`；补解析 `name:`（A-39）、缺则 `—`（I-8）；**外部文本安全化升为通则**（`|` → `｜`，覆盖表格与列表）——P-044 仅对描述列做 `_cell()`，hook 表遗漏即 A-37 缺陷直接成因。
- C-14: **步骤级四字段来源链 = 以事件流为主源**——主题 ①`step.scenario` ②制品 H1 主名；创建时间 ①`step.ts` ②`> **创建日期**:` 行 ③front-matter `date`；简要描述 ①`step.outcome`；修改历史 ①该 P 的 session 轮次清单（多文件 → 轮次 + ts + 最远 step）②front-matter `version`；制品↔步骤映射 ①文档自声明 `Spec 步骤` 行 ②常量兜底；**缺失一律显式 `—`**（I-8）；`reasoning` 不进视图（守 C-6 单一认知块）。
- C-15: **锚点改双属性保险** = `<a name="feat-{f}" id="feat-{f}"></a>`（官方背书 `name`（A-44）+ 标准 `id` 并存）；两者皆被剥离时退化为「可折叠不可跳转」，不影响默认视图与折叠 → 登记 **H8**。
- C-16: **映射来源语义与收敛（修正 C-11 ②③）**——① **改语义**：`CODE_WIKI §9` 行标注（人工索引，对四空洞全对）**优先** → `PROGRESS` 行首链接兜底 → `—`；② **收敛选 (a) 抽共享纯函数模块**（如 `scripts/spec_map.py`，语义同源的唯一保证；(b) 一致性对账已被 A-33 证伪——两实现同错可对账通过；(c) 只改一处 = 制造双语义）；③ 不改历史 PROGRESS 行（维持 C-11 ④）；④ 预期映射缺口 **4 → 0**。

**假设区**（未实测，待触发）:
- [H5] 派生状态机的**状态集最小完备性**未实测——现有候选状态源（`PROGRESS` 状态列 / `step-gate` exit 0-1-2 / `verify-anchor` 硬软 / 软性存疑）是否覆盖全部必需状态，尚缺反例检验。
- [H6] 描述列的**单行长度上限**未完全实测——v1.3 已获**间接依据**（A-38：长 token 压列 → 短描述有机制性理由），`DESC_CAP = 40` 已升格为「扫描性阈值」；但**具体截断阈值仍需真机渲染宽度校准**（本机不可验）。
- [H7] per-feature 流程折叠块的**体积预算**未完全实测——v1.3 已部分回填（26 块 / 514 行 / 20027 B；A-45 表明无技术数量上限），但「26 块是否仍在认知负载内」待真机浏览确认。
- [H8] **双属性锚点（`name` + `id`）在宿主的存活率**未实测——官方仅背书 `name`（A-44），`id` 是否被剥离存在**冲突证据**（官方文档 vs 第三方技术文）；本机无法验证远端渲染，需真机确认；失效后果为「可折叠不可跳转」（非阻断）。

---

**Review 签字**: _________ 日期: _________
