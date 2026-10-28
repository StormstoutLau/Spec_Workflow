# 调研文档：待办优先级与依赖分析自动化（含与图结构编排的关联）

---

id: todo-graph-analysis-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-10-28
depends: [project-console-RESEARCH, graph-structure-upgrade-RESEARCH, rework-and-decision-paths-RESEARCH]
upstream: null

---

> **Feature**: todo-graph-analysis（待办优先级 / 依赖关系分析的自动化可行性，与图结构编排的关系判定）
> **创建日期**: 2026-10-28
> **状态**: draft（草稿；只读分析 + 契约草案，零代码）
> **Spec 步骤**: Step 1-2（T3 轻批：单文档研究，无四文档管线）
> **任务来源**: 用户指令「回溯一下 历史调研里面是否有图结构编排 当前是否具备实施条件 / 另一个问题是 当前待办事项仅列入 progress 缺少待办事项的优先级 依赖关系分析 如何自动化实现此分析 是否与图结构编排存在某种关联 请深入调研」→「落档 P-153 分析批」
> **批档次**: **T3 轻批**（裁剪理由 = 纯只读分析 + 单文档新增，零代码 / 零门禁 / 零真值源重定义 / 零依赖）
> **ADR-0010 三问**: Q1 **Layer-0**（只读分析 + 文档新增）/ Q2 **用户指令**（「落档 P-153 分析批」）/ Q3 **副作用 0**（不改 `console_gen` / `spec_map` / `step_enforce` / 任何校验器与 hook）

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 24 | 本仓文件逐行读取 / 机械枚举 / 已有远端与本地读数（E1） |
| B 推断类 | 4 | 由 A 类推出、尚未实测的判定（附录 B） |
| C 类（决策） | 9 | 候选路线对比与建议（不参与 R7 对账） |
| 假设区 | 0 | 本批无新开假设（未决项以 U-1~U-3 四元块登记，不入 H 区） |

> **取证口径**：本批为**仓内只读调研**，不引入外部来源；所有事实均可由文件路径 + 行号复核。不把 C 类判断写成 A 类事实。

---

## 1. 调研目标与边界

**核心问题**：

1. 历史调研中是否已存在「图结构编排」？裁决是什么？今天是否具备实施条件？
2. `PROGRESS` 只有待办登记、缺优先级与依赖分析，能否自动化？与图结构编排是什么关系？

**边界（本批不做）**：不改任何脚本 / 配置 / hook / 门禁；不新建图引擎或图数据库；不实现任何派生视图；不裁决「是否开闸实施」（开闸须用户显式裁决，见 §9）。

---

## 2. 方法与证据口径

| 方法 | 覆盖对象 | 结果 |
|---|---|---|
| 逐行读取 | `spec/graph-structure-upgrade/RESEARCH.md`、`spec/project-console/RESEARCH.md` §7.12、`spec/rework-and-decision-paths/RESEARCH.md` §3.6-§3.7、`spec/framework-deep-review/RESEARCH.md` 附录 D.2 | 完成（E1） |
| 源码读取 | `scripts/spec_map.py`、`scripts/console_gen.py`、`scripts/rework_graph_check.py`、`scripts/repo_stats.py` | 完成（E1） |
| 机械枚举 | `docs/PROGRESS.md` 152 条 P 行状态、`spec/` 目录数、`docs/rework-graph.json` 分叉数 | 完成（E1） |
| 正则普查 | `scripts/*.py` 中拓扑序 / DAG / 关键路径相关实现 | **零命中**（E1，见 A-16） |

---

## 3. 历史回溯：图结构编排已调研并被裁决

【A】A-1 图结构升级线共有三个登记批次：P-125（前置调研，v1.0）、P-126（风险点解决办法 + 外部引文 T1 核验，v1.1）、P-127（U-6 测量方案 + U-7 P4 前置判据，v1.2）；三者状态均为 `done`，载体为 [spec/graph-structure-upgrade/RESEARCH.md](./../graph-structure-upgrade/RESEARCH.md)。证据 E1（`docs/PROGRESS.md` P-125/P-126/P-127 行）。

【A】A-2 该线裁决为 **A 薄图路径**（任务卡附加字段 + S1 只读图构建/校验 + S2 一个真实 pilot），**否决 B 全框架/全引擎**（LangGraph / Airflow / Temporal 直接接管），C 不升级仅作基线（RESEARCH L342-L346、L350）。

【A】A-3 同文件落成七条约束 C-1~C-7，其中 C-5 = **「本仓不建图引擎；只做 G1 + G2 契约/证据/验收；图构建/校验为只读最小工具」**（L358）。

【A】A-4 五条硬否决已明文登记：❌ 建图引擎 / 图数据库 / 调度器；❌ 用图框架替换任务卡；❌ 让 RPC 内核解析图拓扑；❌ 在 P3/P4 判据满足前引入 LangGraph 等新栈；❌ 没有真实负载就固化拓扑（L178-L182）。

【A】A-5 该调研的核心判据句为：「图结构编排对**复杂任务的契约**是必备的，对**框架**不是必备的」（L333）；基础评分薄图约 6/10、全引擎约 3/10，且原文自标为判断（C 类）而非实测（L96）。

【A】A-6 S1 最小工具层的能力边界已写明：图构建器从卡 / front-matter / `rework-graph.json` / `DECISION_RECORD_CONTRACT` 生成**派生** `graph.json`（不是真值源）；校验器做环检测、孤儿检测、影响闭包、依赖拓扑序；**不调度、不执行、不接运行时**（L161-L163）。

【A】A-7 未决项仍 open：U-1 = 首个真实复杂任务 pilot 未选定（触发 = 用户裁决 / 真实负载出现，L368）；U-6 = 缓解措施拦截率 / 误报率未测（L373）；U-7 = P4 前置实现未做（L374）。

【A】A-8 pilot 候选裁决为「批候选、不批现在启动」：`spec/graph-structure-upgrade/` **仅有 RESEARCH.md（无 DESIGN / IMPLEMENTATION）**，S0 契约与 S1 工具未产出，S2 无契约可测；启动前置 = S0 DESIGN（`depends_on` / `join` / `iter_budget` / `join_policy` / `graph_version` 五字段 + fixture）+ S1 只读工具 + 范围冻结（framework-deep-review RESEARCH 附录 D.2 与 L1558）。

【A】A-9 LangGraph 线（P-006）裁决为**不整体迁移**，只作方案 B 触发后的升级路径；三个触发条件 (a) 状态管理成瓶颈、(b) 跨会话恢复出错 ≥2 次/月、(c) 异构复跑 ≥每周，**均无实测读数**。

【A】A-10 分布式编排线（P-039）对 orchestrator 框架（LangGraph / CrewAI / Temporal）的裁决是**否决且本批不得重提**；依赖 DAG 仅登记为懒加载项。

【A】A-11 返工图线（P-051）采纳「一张表 + 只读对账器」方案，明确**不新增门禁**；接门禁的触发条件 = 真实分叉数 ≥3，而 [docs/rework-graph.json](../../docs/rework-graph.json) 当前 `"forks": []`、`non_rework` 1 条 ⇒ **0 例，未触发**。

【A】A-12 ARC 决策图谱（P-031~P-035）为**有条件采用且不接门禁**：`tools/arc` 为只读快照（8 实体 / 7 边），导入后不追平。

**历史结论**：图结构编排不是没人调研，而是**已调研、已裁决、已划死五条不做**。再次立项不是「补空白」，而是**重开已闭议题**。

---

## 4. 当前是否具备实施条件

【A】A-13 `spec/` 下实际目录 41 个（含 `templates/`），而 `spec/graph-structure-upgrade/` 目录内文件仅 `RESEARCH.md` 一个 ⇒ 图线处于「只有调研、无设计」状态。证据 E1（目录枚举 + Glob）。

| 档 | 判定 | 依据 |
|---|---|---|
| 全引擎 / P4 框架 | **不具备** | P4 三判据（V-EXPORT / V-FENCE / V-LEASE）逐条未验收；成本 / 重放污染 / 卡替换 / 双真相源四类风险未解（A-2、A-4、A-7、A-10） |
| 薄图 S0 契约 + S1 只读工具 | **形式条件齐、负载缺失** | 五字段 + fixture 已定、pilot 候选序已排；但无 DESIGN、无真实负载、U-1 open（A-7、A-8） |
| 待办优先级 / 依赖分析自动化 | **技术具备、治理需裁决** | 见 §5-§6；被 [project-console RESEARCH §7.12（四）](./../project-console/RESEARCH.md) 的「P 级任务图完整 schema = 不做（登记）」覆盖 |

【A】A-14 `project-console` §7.12（三）已判定「视图刷新自动化**已解决**（`console-gen` 提交即刷）」，而「状态真值撰写自动化**未解决**」；并明确列出**任务状态 / 优先级 / 依赖 = 不可免手动**，原因是真值源为 `PROGRESS` 散文（L389-L392）。

【A】A-15 同节（四）把「**P 级任务图完整 schema**」列为 **P4 = 不做（登记）**，并给出三条重审触发：① 真实误判 / 返工 ≥1 例（当前 0）② **用户显式裁决** ③ P-039 P-c 分发落地（L394-L403）。

**判定**：薄图今天「能写 DESIGN」，但写了即命中 A-4 第 5 条「没有真实负载就固化拓扑」；待办分析则**不需要** S0/pilot，但**需要**援引 §7.12（四）触发② 才合规开闸。

---

## 5. 现状能力盘点：自动化缺的是什么

【A】A-16 `scripts/` 下对「拓扑 / topolog / critical_path / slack / DAG」的正则普查**零命中** ⇒ 本仓当前没有任何拓扑序或关键路径实现（E1）。

【A】A-17 `spec_map.parse_progress_rows` 只取 P 行前四列（`P_ROW_RE` = `^\|\s*(P-\d{3})\s*\|([^|]*)\|([^|]*)\|\s*([^|]*)\|`），输出 `{P: {status, features}}`；**不解析第 5 列优先级、无依赖字段**（spec_map.py L107-L123）。

【A】A-18 `console_gen.parse_progress` 按六列切分并构造 `Task(pid, title, status, priority)`，即**优先级已在真值源内且已被解析**；但 `priority` 只在事项视图渲染，**不参与排序或派生**（console_gen.py L137-L174、L663）。

【A】A-19 `derive_state` 已具备决策态消费能力：`status == "pending"` 且无 session ⇒ 行动档 `Recommended`、依据「未开工（立项已登记，无决策流）」；`blocked` ⇒ `Needs Attention`（console_gen.py L345-L377）。

【A】A-20 由于 `PROGRESS` 152 条 P 行状态全部为 `done`（机械枚举），三档队列当前**恒空**；这是「机制已备而空转」，不是渲染缺陷（与 rework-and-decision-paths RESEARCH v1.1 的自查更正同源）。

【A】A-21 `console_gen` 的 `dep_graph` 只抽 Python `import` / `importlib.import_module` 字面量边，属**代码架构依赖**，与任务依赖无关（console_gen.py L397-L426）。

【A】A-22 `rework_graph_check.py` 已落地四段判定范式（表结构 / 边自洽 / 声明↔实测 / 孤儿扫描，exit 0/1/2），可直接照抄为待办图的校验骨架。

【A】A-23 `console_gen --check` 的语义是「内存重建后与 `docs/CONSOLE.md` 逐字节比对，不一致 exit 1 且不写盘」，这是任何新增派生视图**必须复用**的兜底门禁（console_gen.py L1393-L1399）。

【A】A-24 `docs/PROGRESS.md` 的人工依赖分析（P-083）得出**仅两条真实耦合**：链 1 = U-8 → U-9（数据链，且已双双落地），链 2 = G-11b ⊂ G-08b~G-12b（家族包含）；其余 6 项互相独立（PROGRESS L298-L302）。

**由此得到的关键判断**：自动化的瓶颈**不是图算法**（节点 152 个、真实边仅 2 条，拓扑序是平凡计算），而是：

1. **残余待办没有结构化载体**——它们以散文写在四张视图表里（优先级表 / 依赖链 / 六维清单 / 乙类 8 项）；
2. **「等触发」没有可计算的谓词**——`等触发` 是自然语言，机器无法求值；
3. **优先级字段无人消费**——已解析但不排序，等于装饰。

---

## 6. 四条自动化路线（C 类判断）

【C】C-1 **路线 A（待办入 P 行）**：把「可开闸未开」的残余（约 8~10 条）落成 `pending` P 行，复用第 5 列优先级，并在 detail 单元追加机读标记。产物 = CONSOLE 自动出现「推荐档 + 就绪理由」。门禁 = `console_gen --check` + 环检测。失效模式 = 散文依赖仍需人写；占用 P 编号。代价 = 低。

【C】C-2 **路线 B（声明 = 重数对账）**：解析四张手写视图的行数与「项数」声明，仿 `m7_stats` 做契约校验。产物 = exit 码 + gap 三元组。门禁 = 需第 7 个 hook。失效模式 = **只防计数漂移，不产出顺序**。代价 = 低。

【C】C-3 **路线 C（独立待办图 JSON）**：`docs/todo-graph.json`（节点 = P、边 = dep、provenance 必填），仿 `rework_graph_check` 四段 + 孤儿扫描。门禁 = 新 hook。失效模式 = **易成第二真值源**（违 graph RESEARCH R1），须带 `source_digest` 且声明为派生。代价 = 中。

【C】C-4 **路线 D（front-matter 依赖图）**：复用四件套 `depends:` 静态声明 + ADR 边，做影响闭包 / 拓扑序。门禁 = 环检测。失效模式 = 只到文档层，**答不了「下一条待办」**。代价 = 低。

【C】C-5 **明显不可行的四条**：① LangGraph / Airflow / Temporal 接管（C-4/C-5 已否决 + 重放污染）；② LLM 打分排序（无机械真值源 ⇒ 不可复算，正是「形式化审查表演」）；③ 再手写一份优先级汇总视图（P-103 教训：无门禁可拦）；④ 以 ARC 快照作任务图真值源（不追平 + 明确不接门禁）。

【C】C-6 **推荐组合 = A 的降级版 + B 的兜底**：只把「可开闸未开」的残余落成 `pending` P 行（观测项与跨仓项保持视图态），并用 `console_gen --check` 逐字节兜底；**不建独立 JSON 真值源，不做全量 schema**。理由 = 净增量最小且完全落在既有门禁内。

---

## 7. 最小闭环设计草案（供 Layer-1 实施批使用）

### 7.1 第一步：决策态结构化（零列变更）

在 `pending` / `blocked` P 行的 **detail 单元内**追加一个 HTML 注释（不新增列，避免破坏 `spec_map` / `console_gen` / `repo_stats` 的现有列序契约）：

```text
<!-- todo: dep=P-115,P-152; trigger=date:2026-11-15 -->
```

- `dep`：仅在有真实耦合并已登记时填写（当前全仓仅 2 条真实耦合，见 A-24）；
- `trigger`：**封闭枚举**，见 7.2；
- 该注释在渲染时不可见，不引入新的可见视图，因此不触发「手写汇总」纪律。

### 7.2 trigger 谓词封闭枚举

| 谓词 | 求值方式 | 现状可算 |
|---|---|---|
| `date:YYYY-MM-DD` | 与当日比较 | ✅ |
| `count:rework-forks>=N` | 读 `docs/rework-graph.json` 的 `forks` 长度 | ✅ |
| `count:backflow-pending>=N` | 调 `spec_runner backflow-audit` 的输出计数 | ✅ |
| `metric:repo_stats.<key>` | 读重数值（如 `fs.progress_tasks`） | ✅ |
| `user-verdict` | **永不自动满足** | ✅（恒 false） |
| `signal:<name>` | 不可计算 ⇒ 归入「需人工裁决」桶 | ❌（显式标注） |

设计要点：**宁可显式列出「不可自动」项，也不要把自然语言假装成可计算谓词**；否则就退化成新的审查表演。

### 7.3 第二步：就绪集派生（Layer-1）

- `console_gen` 新增「就绪集」区块（现有 9 区块之后追加，不改既有区块）：
  - **今天可动**：`pending` 且全部 trigger 为真；
  - **被阻塞**：`pending` 且依赖未完成，显示阻塞者 P 号；
  - **需人工裁决**：`signal:` / `user-verdict` 桶；
- 环检测失败 ⇒ exit 1（数据错误，不是视图过期）；
- 复用 `--check` 逐字节兜底；
- **不接新 hook**（先观察一轮，遵循 graph RESEARCH L163「先验证再决定是否接门禁」）。

### 7.4 诚实边界

- **不做 CPM 关键路径 / 松弛量**：本仓无工期（duration）数据，凭空造边权即为幻觉；只做拓扑序与就绪性；
- **不做自动优先级重排**：优先级是人的判断（决策态），机器只做**可动性**求值；
- 就绪集若长期恒空（无 `pending` 行），应显式打印「结构性空转」而非「（无）」。

---

## 8. 与图结构编排的关联

| 维度 | 待办图分析 | 图结构编排（薄图） |
|---|---|---|
| 层次 | 文档 / 治理层，本仓内部 | 执行层，跨仓任务卡 + 运行时语义 |
| 真值源 | `PROGRESS` P 行（已存在，152 条） | 任务卡字段（S0 尚未产出） |
| 算法 | 环检测 / 拓扑序 / 就绪集求值 | 同 + join / fencing / lease / 影响闭包 |
| 前置 | **无**，可立即实施（须过 §7.12 触发②） | S0 契约 + S1 工具 + 真实负载 |
| 共同纪律 | 派生不立第二真值源 / 声明 = 重数 / 先只读后接门禁 / 无负载不固化拓扑 | 同 |

【C】C-7 **关联判定 = 同算法族、不同工程**：两者共享「环检测 + 拓扑序 + 影响闭包」这一小段算法，未来可汇于 graph S1 的只读构建器；但**待办图可以且应该在 `console_gen` 内独立完成**——它不需要 S0 五字段、不需要 pilot、不需要新依赖。反过来把待办图塞进任务卡 schema 会立刻制造第二真值源，属 graph R1 明确禁止。

【C】C-8 **推荐的次序关系 = 先内后外**：先用本仓 152 节点的文档图把「构建 → 环检测 → 拓扑序 → 声明对账」跑通（零风险预演），再把它作为 S2 pilot 的 S1 组件来源；**不为待办分析启动 S0/pilot**，也不把 pilot 作为待办分析的前置。

---

## 9. 开闸条件与建议（C 类）

【C】C-9 若要把本草案推进到 Layer-1 实施，合规路径是**援引 project-console §7.12（四）触发②「用户显式裁决」**（A-15），并在实施批内显式引用该条款作为重审依据；否则只能做路线 B（对账），它不产出顺序。

**建议执行序**：

1. **P-153（本批）**：只读分析 + 契约草案落档（零代码，已完成）；
2. **若用户裁决开闸** → Layer-1 单文件族实施批（`console_gen` + `spec_map` + 1 个测试文件 + `--check` 兜底），不接新 hook；
3. **观察一轮**后，再决定是否把就绪集接入第 7 道门禁；
4. 图编排线维持「等点名」，不因本批而启动。

---

## 10. 未决项登记（四元块）

- **U-1 残余待办是否允许占用 P 编号**
  - **判据**：`PROGRESS` 出现 `pending` P 行且 `console_gen` 三档队列非空、`--check` 通过
  - **触发条件**：用户裁决（P 行语义 = 批次登记 vs 待办登记的取舍）
  - **当前倾向**：只把「可开闸未开」的 8~10 项升格，观测项与跨仓项保持视图态
  - **证据等级**：E1（现状 152/152 done、三档恒空）

- **U-2 首版是否只做「可动 / 不可动」二值**
  - **判据**：就绪集区块上线后，连续 3 批无需人工回读四张散文视图
  - **触发条件**：实施批完成后观察
  - **当前倾向**：是（不引入权重、不做排序打分）
  - **证据等级**：待核

- **U-3 是否把 `console_gen` 纯派生模式推广到「依赖边」**
  - **判据**：真实任务依赖边 ≥3 条（现 2 条）或用户裁决
  - **触发条件**：PROGRESS 依赖视图新增真实耦合
  - **当前倾向**：暂不（边太少，抽象无收益）
  - **证据等级**：E1（A-24）

---

## 11. 边界与回退

- **边界**：零代码 / 零门禁 / 零依赖 / 零真值源重定义；不修改 `PROGRESS` 既有 152 行；不改 `CODE_WIKI` 历史 banner（append-only）；不启动图编排线。
- **回退**：删除本目录 + P-153 行 + `CODE_WIKI` 对应行 + session；无数据迁移、无门禁影响（回退点 R-P153-1）。

---

## 12. 参考文献（仓内指针）

| 主题 | 载体 |
|---|---|
| 图结构编排裁决与 S0/S1 契约 | [graph-structure-upgrade/RESEARCH.md](./../graph-structure-upgrade/RESEARCH.md) L96、L161-L182、L333、L342-L374 |
| 看板自动化分层可达性与 P4 不做条款 | [project-console/RESEARCH.md](./../project-console/RESEARCH.md) §7.12（三）（四）（五）L389-L405 |
| FTA / CPM-PERT / ATAC 等方法的差距矩阵 | [rework-and-decision-paths/RESEARCH.md](./../rework-and-decision-paths/RESEARCH.md) §3.6-§3.7 L102-L124 |
| 图 pilot 裁决（S0/S1 缺失） | [framework-deep-review/RESEARCH.md](./../framework-deep-review/RESEARCH.md) 附录 D.2、L1558 |
| 待办真值源与依赖链人工分析 | [docs/PROGRESS.md](../../docs/PROGRESS.md) L196-L302 |
| 派生与校验实现 | [scripts/console_gen.py](../../scripts/console_gen.py)、[scripts/spec_map.py](../../scripts/spec_map.py)、[scripts/rework_graph_check.py](../../scripts/rework_graph_check.py) |

---

## 附录 B：推断登记

```json
{"id": "B1", "claim": "待办优先级/依赖自动化的瓶颈是真值源形态与触发谓词不可计算，而非图算法能力", "basis": "A-16/A-17/A-20/A-24", "status": "unverified-pending-implementation"}
{"id": "B2", "claim": "残余待办落成 pending P 行后，三档队列将由结构性空转变为非空，无需新增门禁即可获得可见收益", "basis": "A-18/A-19/A-20/A-23", "status": "unverified-pending-implementation"}
{"id": "B3", "claim": "graph S1 只读构建器可由待办图实践先行验证，且不构成对 S0/pilot 的前置依赖", "basis": "A-6/A-8/A-13", "status": "candidate"}
{"id": "B4", "claim": "CPM 关键路径在本仓缺乏工期数据，强行引入会产生不可复核的假精度", "basis": "A-16/A-24", "status": "judgment"}
```
