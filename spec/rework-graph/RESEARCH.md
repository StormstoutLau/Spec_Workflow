# 调研文档：回写返工图（分叉关联登记 + 触发条件 + 只读对账）

---

id: rework-graph-RESEARCH
type: design
version: 1.1
status: draft
date: 2026-09-27
depends: [rework-and-decision-paths-RESEARCH, ADR-0010]
upstream: null
---

> **Feature**: 回写返工图（rework graph）——回写流的**完整形态**：分叉原语 + 原/新流关联登记 + 触发条件
> **创建日期**: 2026-09-27
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「回写流上两个仓各占一半 —— spec workflow 缺『关联登记』（自己登记为缺口）、RPC 缺『分叉原语』；完整形态 = 分叉原语 + 原/新流关联 + 触发条件。根据 RPC 框架分析 当前是否可以实现完整形态」→ 用户裁决「走路径 A 实施 按照完整吃狗粮规范执行」。
> **与 P-050 的关系**: 本文承 [P-050](../../spec/rework-and-decision-paths/RESEARCH.md) 的 Q1 判定（「有原语、缺语义」）与其 §6 的 H-RPC1/H-RPC2 观察项；**本 feature 实施的是 P-050 明确推迟的那一半**（[IMPLEMENTATION L261](../rework-and-decision-paths/IMPLEMENTATION.md) 记「回写通路的另两半（事件流 `fork` 回写 / 新流-原流关联登记）属**使用纪律**，非本次代码改动」）。
> **v1.1 变更（2026-09-27，Step 8 独立审查整改）**：以**子代理**执行 **Step 8 独立审查**（RULE-1 时序独立；**RULE-5 同基座降级**，如实标注），**6 项发现（3 P2 + 3 P3）全部整改**——本文件内的整改 = **P2-2**：A-9 的「七种『缺』」**计数与枚举不符**（枚举仅 6 项）⇒ 改**免计数枚举**并复读 RPC 源码得**实为 8 类**（`rpc_check.py` **L1147-1164**，行号由 L1140-1165 订正）；同源三处（正文 §3.2 / 附录 A / §5.2 验证表）同步。其余 5 项落在 DESIGN / IMPLEMENTATION / CHECKLIST（见各文档 v1.1 变更行）。断言计数**不变（16A+5B+4C+3H）**——只订正计数口径与行号，无新增/删除断言行。

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 16 | 本仓与 RPC 侧源码/数据文件机械取证（E1） |
| B 推断类 | 5 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 4 | 不参与 R7 机械对账（DR-2） |
| 假设区 | 3 | 未实测项（见附录 C） |

---

## 1. 调研目标

**核心问题**:

1. 「回写流完整形态」的三件（**分叉原语 / 原-新流关联登记 / 触发条件**）在本仓**当前**可否实现？各件现状如何？
2. 若可实现，**载体与方法**是什么（数据放哪、对账器放哪、是否接门禁）？

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| Read / Grep（本仓） | E1 取证：`spec_runner` fork 实现、事件 schema、sessions 命名、根目录结构、DC 校验器扫描面 | `cmd_fork` / `sessions/` / `gather_md_files` |
| Read / Grep（`D:\RPC`） | E1 取证：RPC 侧「关联登记」与「触发条件」范式 | `edges.yaml` / `multi-round.yaml` / `rpc_check.py` |
| 承接 | 复用 P-050 第 ⑩ 批已完成的跨仓对照判定（不重复取证） | P-050 RESEARCH §6 |

### 2.2 调研范围

- **时间范围**: 无外部文献检索（本 feature 是**仓内工程**：范式来源 = RPC 框架 + 本仓源码，均为 E1 直读）
- **领域**: 单人开发者 + LLM Agent 的 spec 流程工具链
- **排除**: 不引入任何外部引擎/重型流程（守 D6 零依赖）

## 3. 调研发现

### 3.1 Q1 本仓实测：三件中「一有、两缺」

A-1 `spec_runner fork`（`--session --seq --new`）语义 = **复制前 N seq 行至新流**（`spec_runner.py` L487-507）——本仓唯一**能产出新事件流的命令**【E1】
A-2 **`fork` 不落任何关联**：`cmd_fork` 只把 `fork: <new> <- <session>` **打到 stdout**（L505-506），**未**在新/旧任何一侧写入父流指针【E1】
A-3 **事件 schema 无 lineage 字段**：事件行字段 = `ts/seq/session/source/model/provider/event/input/output/gate`，**无** `parent` / `from`【E1】
A-4 **本仓已自登记该缺口**：P-050 RESEARCH A-2 / L109 / 洞察 1(c) 三处明写「新流与原流**无关联登记**」，DESIGN §9.5 **B-9** 补记「§7.2 使用时机增第 3 步」【E1】
A-5 **命名后缀已是「非正式」lineage**：`tools/spec_runner/sessions/` 实测存在 `specwf-p020-20260908v2` / `p028-*v2`·`v3` / `p042-*v2`·`v3` / `p050-*v2`…`v9` 等同族多流——**人可读、机不可判**【E1】
A-6 **本仓无 `inventory/` 目录**（根目录 = `adr/ docs/ scripts/ spec/ tools/`）⇒ RPC 的 `inventory/*.yaml` 载体**无现成落点**【E1】
A-15 `dc_validator` 只扫 `**/*.md`（`gather_md_files` L348-355）⇒ 非 `.md` 数据文件**不在 DC 契约范围**（无 front-matter 义务）【E1】
A-16 `CODE_WIKI` stats 块 declared 现值 = `spec_feature_dirs 34 / scripts 9 / hooks 5 / progress_tasks 50 / templates 5 / adr_files 8`【E1】

### 3.2 Q1 RPC 侧实测：两个半的**范式**都现成

A-7 RPC `inventory/edges.yaml` 的每条**边强制 `provenance`**：形式 `<前缀>:<载荷>`（L53-63），语义明写「记的是这条依赖的**可核来源**，**不是『我觉得有关系』**」（L59-60）【E1】
A-8 RPC 对 `kinds` 与 `provenance_prefixes` 各设**封闭枚举**（`kinds` 13 项含 **`manual_backflow`**；`provenance_prefixes` = `hash/filetrack/manual/tool`）（L28-50）【E1】
A-9 RPC `provenance` 判据**把各类「缺」全判无效**（枚举 **8 类**：字段不存在 / 非字符串 / 空串 / 仅含空白 / 命中禁用词 `unknown` / 缺 `<前缀>:<载荷>` 形式 / 前缀不在封闭集 / 载荷为空）（`rpc_check.py` L1147-1164，且有 `tests/test_rpc_check_edges.py` 正反夹测）【E1】
A-10 RPC `multi-round.yaml` 的 `cap_state` = **三值封闭集**（`capped/unbounded-by-design/undecided`，**必居其一**）+ `on_exceed_kind` = **四值封闭枚举**（`escalate/terminate/fail-record/undecided`）；`capped` 却 `undecided` ⇒ **判红**（「上限只有一半」）（`rpc_check.py` L5793-5808）【E1】
A-11 RPC **自己也没定「触发条件的值」**：主回环 `plan-review-loop` 停在 `cap_state: undecided`，且明写「『定稿』是**人的判断**……本表**不替它定，只点名**」（`multi-round.yaml` L38-44）【E1】
A-12 RPC `decide_invalidation`（U-4，H-1~H-4）把「变更 → 影响 → 处置」做成**可复算函数** → `(action, class, reason)`（`rpc_check.py` L1466-1508；且自陈「只产出决策，不执行重算」）【E1】
A-13 RPC 最成熟的两处机制共用**同一形态**：**真值表（YAML）+ 封闭枚举 + 声明→实测→对账（只读门禁）**——`id_storage_census`（P-050 ⑩ 已取）与 `edges.yaml` 同构【E1】

### 3.3 Q2 载体与对账器

A-14 本仓既有「独立只读检查器**不接门禁**」的先例：`scripts/downstream_compliance.py`（P-049 明记「**不接三校验器**——守 ADR-0006 §D『纪律 + 可复算命令』定位」）【E1】

## 4. 综合分析

### 4.1 关键发现总结

1. **「三件」在本仓的现状 = 1 有 2 缺**（分叉原语 ✅ / 关联登记 ❌ 已自登记 / 触发条件 ❌）——但**缺的都不是原语，是登记物**（附录 B B1）。【置信度: ★★★★★】
2. **RPC 半给的正是「登记物」的现成范式**：`edges.yaml` 的 `provenance` 义务（封闭前缀 + 禁 `unknown` + 缺则无效）= 关联登记；`cap_state`/`on_exceed_kind` 封闭枚举 = 触发条件（B2/B3）。【置信度: ★★★★★】
3. **机制层可实现、数值层不可自动**：RPC 自己的触发条件停在 `undecided`（A-11）⇒ 我们同样只能「**逼显式回答 + 机检一致性**」，不能替治理定值（B3）。【置信度: ★★★★★】
4. **载体须另择**：本仓无 `inventory/`（A-6），且非 `.md` 不在 DC 契约范围（A-15）⇒ 数据文件放 `docs/` 下最省事（B4）。【置信度: ★★★★☆】
5. **「软约束 vs 门禁」是个真取舍**：不接门禁 = 同 `downstream_compliance` 先例；接门禁 = RPC 的答案（真值表就是门禁）。本轮取前者 + 登记观察项（B5）。【置信度: ★★★★☆】

### 4.2 技术 landscape

- **本仓范式**：真值表/声明以**围栏机读块**寄居于 markdown（CODE_WIKI ```` ```stats ````、M7 ```` ```hits ````）；独立脚本只读、**能不接门禁就不接**（`downstream_compliance` 先例）。
- **RPC 范式**：真值表以**独立 YAML** 存放（`inventory/*.yaml`），每张表配一个**只读门禁**，并有「全仓零代码命中」式的**消费面核查**（`sensitivity.yaml` §283）。
- **共同点**：**声明 ≠ 事实** ⇒ 一律「声明 → 回库/回盘实测 → 对账」，且**穷举式列举「缺」的形态**（**免计数枚举**：RPC 口径 **8 类** / 本仓 **7 类**；三值必居其一）。

### 4.3 研究空白

- 两仓**都没做**的：**把「返工图」（谁 fork 了谁）当成一等真值表来登记与对账**——RPC 有边图但无**事件流分叉**（它只有同会话 `--continue`）；本仓有分叉但无登记。本 feature 填的就是这个交叉空白。

## 5. 幻觉抑制审查（Step 2 Review）

### 5.1 文献验证

本 feature **零外部文献引用**（范式来源 = RPC 与本仓源码，均 E1 直读）⇒ 无 arXiv/DOI 可验对象；不适用「虚构文献」风险。

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| `fork` 不落关联 | `spec_runner.py` L487-507 直读 | ✅ E1 |
| RPC `provenance` 把 8 类「缺」全判无效 | `rpc_check.py` L1147-1164 直读 + 其测试文件 | ✅ E1 |
| RPC `cap_state` 三值 / `on_exceed_kind` 四值 | `rpc_check.py` L5793-5808 直读 | ✅ E1 |
| 本仓无 `inventory/` / 根目录五项 | 根目录 LS | ✅ E1 |

### 5.3 待修正项

- [ ] 无（本批首轮，无先验修正项；后续 Step 4/8 Review 若发现另记）。

## 6. 对设计的输入

### 6.1 可用的技术方案

1. **数据载体**：`docs/rework-graph.json`（承 RPC「独立真值表文件」范式 + 规避本仓无 `inventory/`；**用 JSON 而非 YAML** 以守 stdlib 零依赖——本仓机读声明块同为 JSON）。
2. **对账器**：`scripts/rework_graph_check.py`（只读；「声明 → 实测 → 对账」三段式）。
3. **封闭枚举**（承 A-8/A-10）：`trigger_kind` 封闭集 + `provenance` 式「缺」形态穷举。

### 6.2 关键约束

- **零新依赖**（stdlib only）——承 D6；
- **不改 `fork` 语义**（路径 A 的全部价值 = fork 零改动）；
- **单一真值源**：命名后缀 `vN`（A-5）与登记表若并存 ⇒ 必须指定**谁是真值**（本仓 I-10 语义同源纪律）；
- **不 LLM 自评**（P-028 约束）：触发判定不得来自 LLM。

### 6.3 风险

- **软约束空转**：登记表若无人读、不与实测对账 ⇒ 沦为「填了就算数」的软约束（RPC 原话）⇒ 对账器必须**至少可手动复算**；
- **清单是线索不是事实**：登记表本身是清单 ⇒ 必须对**实际 session 文件**对账；
- **触发条件的值**：只能人裁或登记 `undecided`。

## 7. 参考文献

1. `D:\RPC\inventory\edges.yaml`（v1，2026-09-26）——`kinds` / `provenance_prefixes` 双封闭枚举 + 边 `provenance` 义务
2. `D:\RPC\inventory\multi-round.yaml`（v1，2026-09-26）——`cap_state` 三值 / `on_exceed_kind` 四值 / `stop_on_agreement`
3. `D:\RPC\ops\rpc_check.py`——`validate_edges` / `_bad_provenance` / `LOOP_CAP_STATES` / `ON_EXCEED_KINDS` / `decide_invalidation`
4. `D:\RPC\inventory\id-storage-census.yaml` + `ops/id_storage_census.py`——「声明目标列 → 回库实测 → 对账」三段式
5. 本仓 [P-050 RESEARCH](../rework-and-decision-paths/RESEARCH.md) §6——H-RPC1 / H-RPC2 观察项与三项意见判定
6. 本仓 [P-050 IMPLEMENTATION](../rework-and-decision-paths/IMPLEMENTATION.md) §11——交付 B 实施记录（回写通路另两半属使用纪律）
7. 本仓 `scripts/downstream_compliance.py`（P-049）——「独立只读检查器不接门禁」先例

---

## 附录 A 断言登记

### A 类（事实类，16 条）

【A】A-1 `spec_runner fork` 语义 = 复制前 N seq 行至新流（`spec_runner.py` L487-507），本仓唯一能产出新事件流的命令【E1】
【A】A-2 `cmd_fork` 只 print `fork: <new> <- <session>`（L505-506），**不落任何关联**【E1】
【A】A-3 事件 schema 字段 = ts/seq/session/source/model/provider/event/input/output/gate，**无 lineage 字段**【E1】
【A】A-4 P-050 自登记该缺口（RESEARCH A-2 / L109 / 洞察 1(c) / DESIGN B-9）【E1】
【A】A-5 sessions 目录存在 `v2`/`v3`…`v9` 同族多流（命名后缀 = 非正式 lineage）【E1】
【A】A-6 本仓无 `inventory/` 目录（根 = adr/docs/scripts/spec/tools）【E1】
【A】A-7 RPC `edges.yaml` 边强制 `provenance: <前缀>:<载荷>`（L53-63），语义 = 可核来源非「我觉得有关系」（L59-60）【E1】
【A】A-8 RPC `kinds`（13 项，含 `manual_backflow`）与 `provenance_prefixes`（hash/filetrack/manual/tool）**双封闭枚举**（L28-50）【E1】
【A】A-9 RPC `provenance` 把 **8 类「缺」**全判无效（`rpc_check.py` L1147-1164）【E1】
【A】A-10 RPC `cap_state` 三值封闭集 + `on_exceed_kind` 四值封闭枚举；`capped` 却 `undecided` 判红（`rpc_check.py` L5793-5808）【E1】
【A】A-11 RPC `plan-review-loop` 停在 `cap_state: undecided`，自陈「不替它定，只点名」（`multi-round.yaml` L38-44）【E1】
【A】A-12 RPC `decide_invalidation`（U-4）把变更→影响→处置做成可复算函数 `(action, class, reason)`（`rpc_check.py` L1466-1508）【E1】
【A】A-13 RPC 两处最成熟机制同形 = 真值表 + 封闭枚举 + 声明→实测→对账【E1】
【A】A-14 本仓既有「独立只读检查器不接门禁」先例 = `downstream_compliance.py`（P-049，守 ADR-0006 §D）【E1】
【A】A-15 `dc_validator` 只扫 `**/*.md`（`gather_md_files` L348-355）⇒ 非 `.md` 数据文件不在 DC 契约范围【E1】
【A】A-16 CODE_WIKI stats declared = spec_feature_dirs 34 / scripts 9 / hooks 5 / progress_tasks 50 / templates 5 / adr_files 8【E1】

## 附录 B 机读登记（B 类，5 条）

[
  {"id": "B1", "claim": "完整形态三件在本仓现状 = 分叉原语有、关联登记缺、触发条件缺；缺的是登记物而非原语", "basis": "A-1/A-2/A-3 与 A-4 并列"},
  {"id": "B2", "claim": "RPC 的 edge `provenance` 义务（封闭前缀 + 禁用词 + 缺则无效）是本仓「关联登记」的可搬范式", "basis": "A-7/A-8/A-9"},
  {"id": "B3", "claim": "RPC 的 cap_state/on_exceed_kind 封闭枚举是「触发条件」的可搬范式；机制可搬、数值不可自动（RPC 自陈 undecided）", "basis": "A-10/A-11"},
  {"id": "B4", "claim": "载体应取 docs/ 下独立数据文件 + 独立只读脚本（本仓无 inventory/，且非 .md 不在 DC 契约范围）", "basis": "A-6/A-15 与 A-13"},
  {"id": "B5", "claim": "「不接门禁」是本仓既有取舍（downstream_compliance 先例）；接门禁登记为触发驱动观察项", "basis": "A-14 与 A-13 的张力"}
]

## 附录 C 假设区（3 项）

- [H1] 命名后缀 `vN` 与登记表**并存**时谁是真值源（若两者不一致，对账器判定口径未定）
- [H2] 「什么条件触发回写」的**值**未裁（治理决定；本轮只立封闭枚举的**形状**）
- [H3] 对账器若将来接门禁，是否会与既有 5 hook 的耗时/语义冲突（未实测）

---

**Review 签字**: _________ 日期: _________
