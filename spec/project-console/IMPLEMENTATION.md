---
id: project-console-IMPLEMENTATION
type: design
version: 1.9
status: verified
date: 2026-09-11
depends: [project-console-DESIGN, board-generator-IMPLEMENTATION]
upstream: null
---

# 实施文档：项目控制台多视图生成器与归属迁移（P-043）/ 视图增补（P-044）/ 承载与步骤表（P-046）/ 锚点与映射收敛（P-047，含收口修正批）

> **Feature**: 项目控制台（`spec/project-console/`）
> **设计依据**: [DESIGN v1.6](./DESIGN.md)（D1-D17 + I-1~I-10）
> **Spec 步骤**: Step 5-6
> **本批范围**: P-043 = 归属迁移（前身退役）+ 多视图扩展；**P-044 = 视图增补（描述列 / per-feature 流程 / 架构图口径）**；**P-046 = 承载修复与步骤级动态描述（hook 链表形态 / 步骤四字段）**；**P-047 = 锚点双属性（C-15）+ 映射来源语义反转与共享模块（C-16）+ 收口修正批（§6 缺映射清单 / 兜底面归零）**；**Layer-1 生成端派生视图 + hook 入口只读映射**
> **v1.1 变更（P-044，用户指令「好的，按 C-9/C-10/C-12 落代码」）**: `scripts/console_gen.py` 增补 **D8 描述列**（`first_h1` / `shorten_title` / `feature_desc`）+ **D9 per-feature 流程**（`_feature_process_section`）+ **D10 架构图显式关系口径**（`_arch_section` + `DECLARED_SOURCES` / `TRUTH_NODES`）+ 新增不变式 **I-8**；selftest **16/16 → 27/27**；**C-11 不在本批**。
> **v1.2 变更（P-046，用户指令「先执行 C-13 和 C-14，C-16 共享模块单独处理」）**: `scripts/console_gen.py` 落 **D11 hook 链表形态**（`hook_chain` 增解析 `name` + 新增 `_hook_list` **弃表格** + `_cell` 升为**通则**安全化 → 新增不变式 **I-9**）与 **D12 步骤级动态描述**（`SessionInfo.records` + `read_sessions` 累积多轮 + `_step_table` 六列 + `_clip` / `_fmt_ts` / `STEP_ARTIFACT` / `STEP_CAP`）；selftest **27/27 → 34/34**；产物 **514 行 / 20027 B → 729 行 / 45709 B**；**C-15（锚点双属性）与 C-16（映射语义反转 + 共享模块）不在本批**（用户指定）。
> **v1.3 变更（P-047，用户指令「执行 C-15 和 C-16」）**: **新增 `scripts/spec_map.py`**（映射唯一实现，建立不变式 **I-10 语义同源**）→ `console_gen.py` 与 `step_enforce.py` **同时改为复用该模块**（删除各自本地实现）；锚点改**双属性**（**D13/C-15**）；`console_gen.py` 架构图 `TRUTH_NODES` 增 `TS_wiki`、`DECLARED_SOURCES` 增 `spec_map` / `TS_wiki` 边（新增 import 边首次入图）；selftest **34/34 → 36/36**；`declared.scripts` **7 → 8**；真实仓映射 **13 项差异**（4 空洞补齐 + 9 主 P 归位）、全 feature 门禁复核 **32/32 exit 0**。
> **v1.4 变更（P-047 收口修正批，用户指令「P-047 是否完全闭环 → 执行 A+B+C+D」）**: ① **D15 §6 缺映射清单落地**（`_trace_section` 增参 + 输出「缺映射（I-8 显式缺口）」行；selftest **36/36 → 37/37**）——修正 v1.3 的**声明未落地**；② **`CODE_WIKI §9` 补两行标注**（`cpp-hub-absorption → P-002` / `cpp-hub-gap-analysis → P-004`）→ **兜底面 32/32 归零**，一并消解 **A-33 残余实例与实测错值**（`cpp-hub-absorption` 原被劫持为 P-011）；③ 记入 **B5 判据教训**（「缺口 4 → 0」只覆盖缺值、不覆盖错值 → 必要不充分）。
> **v1.5 变更（状态归属契约实施轮 · Layer-0，P-042 v1.8，用户指令「先按照结论顺序执行 符合完整spec工作流规范」；**零代码改动**）**: 落 [DESIGN v1.5 §5.1](./DESIGN.md) 的 **D16 状态归属契约（Layer-0）**——**本批不做任何代码改动**（`scripts/` 零变更 / selftest 保持 **37/37** / `docs/CONSOLE.md` 不重生成 / 无新依赖 / 无新门禁）；落点 = **`spec/doc-contract/PLAN.md §1` 新增 `DC2.1 任务状态词表（+「来源」列）`**（**与 DC2 轴正交**、四取值**零改动**、仅加「来源」列）+ **`docs/PROGRESS.md` L3** 词表声明**改指向 DC2.1**（单一权威）。**Layer-1 实现**（`derive_state` 首参改派生值 / `PROGRESS` 状态列载体迁移 / 修订 I-7）**属 P2（Layer-1 高风险），不在本批**。新增 **A-12**（本批复跑读数：零代码 + 三校验器全绿 + selftest 37/37 + 门禁链 exit 0）与 **B6**（契约面 > 载体声明）、**DR-17**；§0 表 A **11 → 12**、B **5 → 6**。
> **v1.6 变更（实施期发现登记轮，P-042 v1.11，用户指令「先登记那两个实施期拦截问题」；**零代码改动**）**: 登记 P-042 v1.10 实施期的**两条首跑拦截**——**DR-18 = `repo_stats` PT-11 模式把正文 P 区间误捕为 `fs.progress_tasks` 读数**（本批在 `CODE_WIKI.md` banner 与 §2.1 树写入「豁免面区间 `P-001~P-019`」⇒ PT-11 正则 `P-(数字3位)~(数字3位)` **不区分语义**、取首个匹配得 **19 ≠ 真值 57** ⇒ 首跑 2 条 P2；处置 = 就地改写为「`P-001 至 P-019`」，**零工具改动**；**同族** = M7 §4 候选「R7 管辖边界显式化 + 正文枚举计数弱纪律」）+ **DR-19 = session 写入非法 JSON 转义 + 门禁报错不报文件名/行号**（`specwf-p042-20260929v6.jsonl` **第 4 行**含**未按 JSON 转义**的反斜杠 ⇒ `step-gate` / `verify-anchor` / `step-enforce` **三命令同报** `Invalid escape: line 1 column 834` ⇒ exit 1；根因两条 = ① **写入端**（jsonl 内嵌正则字面量时反斜杠须转义；**同一文件第 1 行**写法正确 ⇒ **同文件两种写法并存**）② **报错端可用性缺口**（异常只给**被解析行内**的 `line 1 column N`、**不报文件名与文件行号**，与「line 1」的字面直觉冲突——本臂据此先查第 1 行、实际故障在第 4 行）；**门禁已覆盖该故障类**（三命令均解析 session ⇒ 非法 JSON 立刻 exit 1）⇒ **非覆盖缺口，而是报错可读性缺口**；处置 = 就地重写该行）。两条均附**触发条件 + 载体预判 + 边界**（见 §6 DR-18/DR-19），本批**只登记**：**不改 `repo_stats` / 不改 `spec_runner`**；新增 **A-13**（v1.11 复跑读数 + 两条首跑拦截实录）；§0 表 A **12 → 13**。
> **v1.7 变更（复核订正轮，P-042 v1.12，用户指令「检查一下上一轮分析 论据理由是否充分 论断是否准确」→「好的，执行吧」；**零代码改动**）**: 登记**自我订正**——**DR-20 = 证据等级虚高：把「从工具行为反推机制」的推断当 E1 使用**（本次实证：§7.15 A-50 的两个 feature→P 映射值（`drift-gate → P-023` / `academic-writing-workflow → P-040`）原为**未核推断**却随段标 E1，经 §7.16 A-51 ④ **实测确认正确**——**结论对 ≠ 论据充分**；同批另有一条属**误读**：我方复述「后五分支不可达」时**去掉了数据前提**，而仓内 §3.8.6/§3.8.1 原文前提齐备、措辞无误 ⇒ 缺陷在复述方）；**修正动作** = 新增 **A-51**（判定链结构核实，读源码）+ **A-52**（兜底通道偏差实测 18/35）+ **B13** + **C-23**（P2 拆分与顺序修正），本批**只登记不改代码**；**边界** = **不改** `console_gen` / `step_enforce.py` / `spec_map.py` / **不新增门禁** / **不落 P0 实施**（须另批）。
> **v1.8 变更（verify-anchor 锚点约束登记轮，P-042 v1.13，用户指令「先登记 verify-anchor 的路径约束问题」；**零代码改动**）**: 登记 **DR-21 = `verify-anchor` 的锚点路径约束未成文 + 报错不定位锚点**（本批 v1.12 实施期又踩一次：根级 `CODE_WIKI.md` 锚点判**硬性违规**；`scripts/spec_map.py` 纯文件锚点判**软性**；`scripts/spec_map.py#L76-L83` 与 `scripts/console_gen.py#L298-L310` **均判硬性违规**；而 `spec/project-console/RESEARCH.md §7.16` 与 `docs/PROGRESS.md#L3` 判**真实**）⇒ 定位只能靠试错，**本轮为此多花 3 次往返**。**变量未隔离（如实登记）** = 判别因素有二候选（① 仅 `.md` 可作锚点载体 ② 行号**区间**形态不被支持而单行 `#L3` 支持），本批**未做单变量对照** ⇒ 留待修复批首步实测。**边界** = 本批**不改** `spec_runner.py` / **不动** `spec/independent-verify/` 文档 / **不新增门禁**。
> **v1.9 变更（三项待裁决细化分析 + P0 批实施设计落档轮，P-042 v1.15，用户指令「待裁决项目细化分析 给出明确建议」→「请生成 P0 批的四文档实施设计草稿」→「先落档这一轮与上一轮结果」；**零代码改动**）**: 落 [DESIGN v1.6 §5.2](./DESIGN.md) 的 **D17 未开工 vs 确无 session 判别（Layer-0 设计面）** 与 [RESEARCH v1.13 §7.18](./RESEARCH.md) 的 **三项待裁决裁定 + P0 批四文档实施设计**。**本批只落设计与分析**：**零代码变更**（不改 `scripts/console_gen.py` / `spec_map.py` / `step_enforce.py` / **不修订 I-7** / 不改校验器 / **不新增门禁** / **不补建 session** / **不落 P0 实施**）。**三项待裁决裁定** = ① 开 (B) 全批 + 加固四条件（V1a 与 P2a **硬耦合**，拆批制造真实误标窗口）② **DR-18 同批自证第 2 例不计入复现**（自指即自满足）+ 方向 A 即刻生效（作用域限 5 视图载体）③ **DR-19 与 DR-21 方向 B 合并开一小批** + 三条前置。**P0 批四文档实施设计**（承 §7.17 / C-24）= 四件（V2a 补建 4 条 session / V1a 立项即登记 / V1a′ 过渡期判据三件 / P2a `derive_state` 拆支）；**唯一设计点裁定** = `pending` 且无 session 落 **`Recommended`**（非 `""`，与 DESIGN §5 原表对齐）；**ADR-0010 三问答录** = Q1 **Layer-1**（改 `console_gen.py` `derive_state`）/ Q2 **用户裁决** / Q3 **副作用 0 + 无常驻回退点**。**P2a 实施形态（设计目标，未实施）**：`sess is None` 分支拆为「`pending` → `Derived("pending", "未开工（立项已登记，无决策流）", "Recommended")`」与「其余执行态 → `Derived(task.status, "执行态但无 session（决策链缺失）", "Needs Attention")`」两路。新增 **A-14**（本批复跑读数：零代码 + 三校验器 + selftest 37/37 + 门禁链）与 **DR-22**（P2a 属**可见行为变更**：`tier` 三处可见输出位点实测，验收不得只跑 `--selftest`）；§0 表 A **13 → 14**。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 14 | A-1 selftest 结果（P-043）/ A-2 归属迁移文件态 / A-3 hook 更名 / A-4 三校验器与 step 链结果 / **A-5 P-044 selftest 27/27** / **A-6 P-044 真实仓重生成读数** / **A-7 P-046 selftest 34/34** / **A-8 P-046 真实仓重生成读数 + I-9 机械核对** / **A-9 P-047 selftest 36/36** / **A-10 P-047 映射语义差异 + 全 feature 门禁复核 + 真实仓读数** / **A-11 P-047 收口批读数（selftest 37/37 + 兜底面归零 + 错值消解 + 门禁复跑）** / **A-12 P-042 v1.8 复跑读数（Layer-0 零代码：三校验器全绿 + selftest 37/37 + 门禁链 exit 0）** / **A-13 P-042 v1.11 复跑读数 + 两条首跑拦截实录（DR-18 / DR-19）** / **A-14 P-042 v1.15 复跑读数（零代码：三校验器 + selftest 37/37 + 门禁链）**（均为本机实测） |
| B 推断类 | 6 | B1 视图机制的充分性（P-043）/ **B2 显式契约替代推断的充分性** / **B3 列表块形态消除两类缺陷的充分性** / **B4 语义唯一化（结构保证）优于事后对账（观察保证）** / **B5 缺口计数判据必要不充分（须并核来源分布）** / **B6 契约面（`PLAN §1`）优于载体声明（`PROGRESS` L3）**（附录 B） |
| C 判断类 | 0 | 判定均在 RESEARCH §7 / DESIGN §5-§9，本批不新增 |
| 假设区 | 0 | 无（H5~H8 属 RESEARCH，本批不新开；本批实测部分的回填见 CHECKLIST §9） |

## 1. 实施概述

| 项 | 值 |
|----|-----|
| 落点 | `scripts/console_gen.py` + `scripts/spec_map.py`（共享映射模块，P-047 新增）→ `docs/CONSOLE.md`（唯一产物） |
| 触发 | pre-commit 第五 hook `console-gen`（`--stage`，L0 档）；映射变更同步影响第四 hook `step-enforce` 的 P 定位（只读映射层） |
| 规模 | stdlib only；selftest **37/37**（P-043 16/16 → P-044 27/27 → P-046 34/34 → P-047 36/36 → 收口批 +1） |
| 归属 | `project-console`（前身 [board-generator](../board-generator/DESIGN.md) 退役） |
| 产物体量 | `docs/CONSOLE.md` **723 行 / 44588 B**（P-047 收口批实测；P-047 为 722 行 / 44526 B，P-046 为 729 行 / 45709 B）；per-feature 折叠块 26 个 / 折叠对 26:26；步骤表 69 行 |

## 2. 工程细节

### 2.1 文件清单

| 文件 | 动作 | 说明 |
|------|------|------|
| `scripts/console_gen.py` | **新增（P-043）** | 多视图生成器（见 §2.2） |
| `scripts/console_gen.py` | **修改（P-044）** | 增补 D8 描述列 / D9 per-feature 流程 / D10 显式关系架构图；新增 `DESC_CAP` / `DESC_ARTIFACT_ORDER` / `TRUTH_NODES` / `DECLARED_SOURCES` / `ENTRY_SCRIPT_RE` / `H1_RE` 常量；selftest 16 → 27 |
| `scripts/console_gen.py` | **修改（P-046）** | 增补 **D11**（`hook_chain` 解析 `name`；新增 `_hook_list` **弃表格**；`_cell` 升为**通则**）与 **D12**（`SessionInfo.records`；`read_sessions` 累积多轮；新增 `_step_table` / `_clip` / `_fmt_ts`；`_feature_process_section` 插步骤表 + 摘要轮次）；新增 `STEP_ARTIFACT` / `STEP_CAP` 常量；selftest 27 → 34 |
| `scripts/spec_map.py` | **新增（P-047）** | **feature ↔ P 映射的唯一实现**（I-10）：`wiki_pid_map`（`CODE_WIKI §9` 行标注）/ `progress_pid_map`（兜底）/ `build_pid_map`（§9 优先 → PROGRESS 兜底 → 缺位不入表）；stdlib only，被 `console_gen` 与 `step_enforce` 复用 |
| `scripts/console_gen.py` | **修改（P-047）** | ① 删除本地 `feature_pid_map` / `P_IMPL_RE` → 改调 `spec_map.build_pid_map`；② 锚点改**双属性**（D13/C-15）；③ `TRUTH_NODES` 增 `TS_wiki`、`DECLARED_SOURCES` 增 `spec_map` 与两处 `TS_wiki` 边；④ 新增 `_read_text` 容错读；selftest 34 → 36 |
| `scripts/step_enforce.py` | **修改（P-047）** | 删除本地 `P_ROW_RE` / `build_feature_pid_map` 实现 → 改调 `spec_map`（语义与视图层同源）；hook 入口参数与退出码语义**零改动**（0 就绪 / 1 阻断 / 2 映射缺位） |
| `scripts/console_gen.py` | **修改（P-047 收口批）** | `_trace_section` 增参（`features` / `mapping`）并输出**「缺映射（I-8 显式缺口）」行**（D15）；selftest 36 → 37（新增 S37） |
| `CODE_WIKI.md` | **修改（P-047 收口批）** | §9 索引补两行 P 标注（`spec/cpp-hub-absorption/` → P-002、`spec/cpp-hub-gap-analysis/` → P-004）→ **兜底面 32/32 归零**（消解 A-33 残余实例与 `cpp-hub-absorption` 的实测错值 P-011） |
| `scripts/board_gen.py` | **移除** | 前身脚本；移除前完成字节级备份（`%TEMP%\board_gen.p043.bak`，16241 B = 源 16241 B 一致）且 `git add` 后再 `git rm`（对象留存可恢复） |
| `docs/BOARD.md` | **移除** | 前身产物（纯派生，无需备份——I-5） |
| `docs/CONSOLE.md` | **新增（P-043）/ 重生成（P-044 / P-046 / P-047）** | 控制台产物（纯派生）；P-044 后 514 行 / 20027 B；P-046 后 729 行 / 45709 B；**P-047 后 722 行 / 44526 B** |
| `.pre-commit-config.yaml` | 修改 | hook `board-gen` → `console-gen`（entry/name/注释同步；**P-044/P-046/P-047 未改动**） |

### 2.2 模块与签名

【A】A-1: **selftest 16/16 PASS（P-043）**（`python scripts/console_gen.py --selftest` 本机实测）——覆盖 P 行解析 / 词表对齐 / 三级队列 / 制品链投影 / 活动区上限 / 决策链 Mermaid / 依赖图 Mermaid / 动态 import 补提取 / hook 链 / 禁 wall clock / 纯派生标注 / 幂等 / 确定性 / `--stdout` / `--check` / I-1 单写路径。

【A】A-5: **selftest 27/27 PASS（P-044，本机实测）**——新增 **S17-S27** 十一项：描述列 H1 主名提取（S17）/ 描述回退链②无制品→P 行事项（S18）/ 回退链③无映射→目录名（S19）/ per-feature 折叠（锚点目录 + 锚 + 摘要三段式，S20）/ 默认项目级在前（§5 先于 §5.1，S21）/ **排除 Mermaid `click`**（S22）/ C-12 显式关系双口径（S23）/ I-8 未声明脚本清单（S24）/ 四文档管道节点（S25）/ 主名收敛 × 「——」交替剥（S26）/ 截断上限 + 省略号（S27）。**S23 首轮拦截**：hook 节点 id 初版为 `{id}_hook`（含连字符替换不彻底），断言与实现不一致 → 统一为 `H_{id}` 前缀（见 §6 DR-9）。

【A】A-7: **selftest 34/34 PASS（P-046，本机实测）**（`python scripts/console_gen.py --selftest`）——新增 **S28-S34** 七项：**S28** C-13 hook 链表形态（`- **demo-hook-2** —— demo2` 列表块存在且**原 hook 表头不复存在**）/ **S29** C-14 步骤表头六列（步骤 / 制品 / 主题 / 创建时间 / 简要描述 / 修改历史）/ **S30** 步骤表内容（多轮时**最新一轮胜出** + 制品列带 ✓/— + 时间格式化）/ **S31** 无 session → 四字段**单行显式缺失**（I-8）/ **S32** `_cell` 安全化通则（scenario 内嵌半角竖线 → 全角 `／`，且该行**列数守恒 = 6**）/ **S33** 多轮轮次进摘要（`｜ 2 轮`）/ **S34** `_fmt_ts` 与 `_clip` 单元（`2026-09-11T15:00:00+08:00` → `2026-09-11 15:00`；`STEP_CAP = 48` 截断补 `…`）。

【A】A-8: **P-046 真实仓重生成读数 + I-9 机械核对（本机实测，2026-09-11）**——`docs/CONSOLE.md` **729 行 / 45709 B**（P-044 为 514 行 / 20027 B）；§5 hook 链 **5 条列表块**（`dc-validator` / `m7-stats` / `repo-stats` / `step-enforce` / `console-gen`，各带 `name` 作用，例：`- **dc-validator** —— DC contract validator (DC1-DC4 + R7)`；`pass_filenames` 三态：4 条「否」+ `console-gen`「未设（pre-commit 默认『是』）」）；§5.1 折叠块 **26 个**（`<details>` : `</details>` = **26 : 26**，锚点 `<a id="feat-">` **26 个**）；**步骤表 26 张 / 步进行 81 行**；多轮进摘要 **2 例**（`loop-engineering ｜ 调研 ｜ P-028 ｜ 3 轮` / `step-gate ｜ 验收 ｜ P-020 ｜ 2 轮`）；无 session → 显式缺失行 **9 处**。**I-9 机械核对**：产物全表扫描 **19 张表格 / 0 张列数不齐**（P-044 首跑为 hook 表 3 行列数不齐 → 本批 0）。

【A】A-9: **selftest 36/36 PASS（P-047，本机实测）**（`python scripts/console_gen.py --selftest`）——新增 **S35-S36** 两项：**S35** 映射**单一实现与优先级**（单元：§9 行标注覆盖 PROGRESS（`{"a": "P-002"}`）/ `wiki_text` 为空 → 退回 PROGRESS 兜底 / 两源皆无 → 空表；并断言本模块**不再暴露** `feature_pid_map`，即旧双实现已被删除）；**S36** §9 行标注**补 PROGRESS 映射洞**（fixture 新增 `spec/epsilon/` 仅 §9 有标注 → 关联 P 由 `—` 变为 `P-009`）；**S20 改断言**：锚点由 `<a id=…>` 改为**双属性** `<a name="feat-alpha" id="feat-alpha"></a>`（C-15）。

【A】A-10: **P-047 映射语义差异 + 全 feature 门禁复核 + 真实仓读数（本机实测，2026-09-11）**——① **映射差异 13 项**（新语义 vs 旧语义，逐 feature 机械比对）：**4 项空洞补齐**（`decision-schema` None→P-016 / `m7-hits-block` None→P-011 / `promptfoo-m7-eval` None→P-010 / `spec-runner` None→P-009，**与 RESEARCH C-16 ④ 的预期「缺口 4 → 0」一致**）+ **9 项主 P 归位**（`arc-probe` P-034→P-031 / `community-ecosystem` P-026→P-018 / `deepeval-arm` P-038→P-037 / `drift-gate` P-029→P-023 / `langgraph-upgrade` P-010→P-006 / `precommit-dc-validator` P-008→P-007 / `project-console` P-045→P-042 / `semantica-absorption` P-016→P-015 / `step-gate-enforcement` P-027→P-024）；真实 feature 缺映射数 **0**（仅 `spec/templates/` 非 feature 不入表，且其文件不匹配 hook `FEATURE_RE`）。**收口批后为 14 项**（+`cpp-hub-absorption` P-011 → P-002 错值消解，见 A-11 ③）。② **全 feature 门禁复核 32/32 exit 0**（对每个 `spec/<feature>/` 模拟 hook 调用 `step_enforce.main([...])`）；旧语义实测 **28/32 exit 0 + 4 feature 无映射**（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema` → hook 返回 exit 2，在 pre-commit 层为 de-facto 阻断）。**【独立 pass 复核更正，2026-09-11】**：v1.3 曾记「消除一处既有误阻断 = `precommit-dc-validator` 旧语义 P-008 无 session → exit 1」，**不可复现**——P-008 与 P-007 同为 P-020 前批次（`int(pid.split("-")[1]) < 20`）→ 两者均走**历史豁免** → exit 0；该记述把 `spec_runner step-enforce --pid P-008` 的 **runner 层** exit 1 误当作 **hook 层**阻断。实际消解的是上述 4 个 feature 的 exit 2。③ **真实仓读数**：`docs/CONSOLE.md` **722 行 / 44526 B**（P-046 为 729 行 / 45709 B）；**双属性锚 26/26**；**import 边首次非空**（`console_gen → spec_map`；`step_enforce → spec_map` —— D5 的 `ast` 口径由「实测为空」恢复为「有边则绘」）。

【A】A-11: **P-047 收口批读数（本机实测，2026-09-11）**——① **selftest 36/36 → 37/37 PASS**（新增 **S37**：§6 缺映射清单「有缺口列出 / 无缺口显式标无」双分支）；② **兜底面归零**（`spec/` 32 个真实 feature 全部由 `CODE_WIKI §9` 人工标注覆盖，**依赖 `PROGRESS` 兜底者 0**，v1.3 时为 2）；③ **错值消解**：`cpp-hub-absorption` 映射由 **P-011 → P-002**（原为 A-33 劫持形态的残余实例；成因 = `P-011` 行把该 feature 当依据引用，兜底「末行胜出」取到它），CONSOLE §2 相应行同步纠正（`| cpp-hub-absorption | … | P-002 | — |`）；④ **门禁复跑 32/32 exit 0**（兜底归零改变 2 个 feature 的 P 指向后复核）；⑤ **产物 723 行 / 44588 B**（§6 增缺映射行 +1 行）；⑥ 三校验器 0 违规 + `step-enforce --pid P-047` exit 0 + `verify-anchor` 锚点全真实。

| 模块 | 签名 | 要点 |
|------|------|------|
| 解析 | `parse_progress(text) -> list[Task]` | 取第 4 列状态**原词**（I-7） |
| **映射（P-047）** | `spec_map.wiki_pid_map(text)` / `spec_map.progress_pid_map(text)` / `spec_map.build_pid_map(progress, wiki)` | **C-16/I-10 映射唯一实现**：§9 行标注（取行内**首个** `P-\d{3}`）**优先** → PROGRESS 行内首个 `spec/<feature>/` 链接**兜底** → 缺位不入表（调用方以 `—` 显式缺口）；`console_gen` 与 `step_enforce` **复用同一实现**（两处本地实现已删除；旧语义「C-11 未收敛」由本项收敛） |
| 解析 | `read_sessions(sessions_dir) -> dict` | 每 P 取最新 session：最远 step + `gate exit 2` 软性 + 末 ts + 步序列；**P-046（C-14）**：并累积**全部轮次**的 step 级记录 `SessionInfo.records`（`(轮次, step, ts, scenario, outcome)`，按「文件名序 → seq 序」稳定排列；轮次标签 = `specwf-pNNN-*` 文件名排序序号，同源双跑稳定） |
| 派生 | `derive_state(task, sess) -> Derived` | **状态 = PROGRESS 原词**；派生的是 `basis`（依据）与 `tier`（行动档） |
| 派生 | `artifact_map(feature_dir) -> dict` / `feature_stage(am) -> str` | 四文档存在性，**后缀匹配**兼容遗留前缀命名；阶段由制品存在性推断 |
| **派生（P-044）** | `first_h1(path) -> str` | 取文档**首个** H1（front-matter 与代码块内 `#` 天然排除） |
| **派生（P-044）** | `shorten_title(text, cap=DESC_CAP) -> str` | 去文档类型前缀 → **交替**剥尾括号组与断 `——` 至稳定 → 截断 |
| **派生（P-044）** | `feature_desc(feature, mapping, tasks_by_pid, spec_dir) -> str` | **C-9 三源优先链**：制品 H1 → P 行事项 → 目录名 |
| 图 | `dep_graph(paths, known) -> (edges, dyn)` | `ast` 静态提边 + `importlib.import_module(<Constant str>)` 补提取 |
| 图 | `hook_chain(path) -> list` | 极简行式解析（`- id:` / `entry:` / `files:` / `pass_filenames:`），**不引入 YAML 库**；**P-046（C-13）增解析 `name:`**（人类可读作用；缺 → `—`，I-8） |
| **渲染（P-044）** | `_arch_section(edges, dyn, hooks, declared, script_names) -> list` | **D10**：`hook → script`（entry 直读）+ `script → 真值源`（`DECLARED_SOURCES`，**仅对实际存在的脚本绘边**）+ import 边（有则绘）+ **未声明脚本清单（I-8）** |
| **渲染（P-044）** | `_feature_process_section(features, mapping, sessions, spec_dir, tasks_by_pid) -> list` | **D9**：锚点目录 + 每 feature 折叠块（摘要三段式 / 四文档管道 / 决策链 / 派生状态）；收敛策略 = 四文档不全 **或** 有 session；**P-047（D13/C-15）**：锚点改**双属性** `<a name="feat-{f}" id="feat-{f}"></a>` |
| **渲染（P-046）** | `_hook_list(hooks) -> list` | **D11（C-13）**：逐 hook **列表块**（`- **{id}** —— {name}` + 缩进 命令 / 触发范围（`files` 正则）/ 传入文件名），**弃表格**；`pass_filenames` 三态可读化（`false`→否 / `true`→是 / 未设→「未设（pre-commit 默认『是』）」），`entry` 原样展示不做美化转述 |
| **渲染（P-046）** | `_step_table(records, am) -> list` | **D12（C-14）**：六列步骤表（步骤 / 制品 / 主题 / 创建时间 / 简要描述 / 修改历史）；同 step 多轮**最新一轮胜出**，修改历史列全轮次（`n 轮：#1 {日期} · #2 {日期}`，n > 1 才加前缀）；无 session → **单行显式缺失**（I-8） |
| **工具（P-046）** | `_cell(text) -> str` | **升为通则（I-9）**：半角竖线 → 全角 `／` + 空白折叠；**凡入表格单元格的外部文本一律过此函数** |
| **工具（P-046）** | `_clip(text, cap=STEP_CAP) -> str` / `_fmt_ts(ts) -> str` | `_clip`：空白折叠 + `STEP_CAP = 48` 截断补 `…`（空 → `—`）；`_fmt_ts`：`2026-09-11T15:00:00+08:00` → `2026-09-11 15:00`（非该形态不动） |
| **渲染（P-047 收口批）** | `_trace_section(tasks, sessions, features, mapping) -> list` | **D15**：§6 追溯覆盖 = 决策链完整性 + **缺映射清单（I-8 显式缺口）**——有缺位列出（反引号包裹）／无缺位显式标「（无——N 个 feature 全部有映射）」；selftest S37 覆盖双分支 |
| 渲染 | `render(..., spec_dir, tasks_by_pid, script_names) -> str` | 8 章（§0 基准 / §1 NEXT 三级 / §2 feature **含描述列** / §3 事项 / §4 决策链 / §5 架构流程 **+ hook 列表块 + §5.1 per-feature 折叠含步骤表** / §6 追溯 **含缺映射清单** / §7 完成 / §8 fork） |
| 写盘 | `write_console(path, content) -> bool` | 内容未变不写（I-3） |

### 2.3 判定落地对照

| 裁定 | 落地位点 |
|------|---------|
| C-5 派生状态机 + 词表对齐 | `derive_state` + 新增 **I-7**；输出仅 `pending`/`in-progress`/`blocked`/`done`；「⚠ 待你审」**不再出现**（selftest S2 断言） |
| C-6 双主键分层 + 活动区上限 | §2 feature 表（分组键）+ §3 P 卡片表（卡片键，`ACTIVE_CAP = 7`，超出折叠）+ §7 done 折叠 |
| C-7 承载限定 markdown 内嵌 Mermaid | §4/§5 输出 ```mermaid 代码块；**无 mmdc 调用、无 HTML 产物** |
| C-8 零依赖依赖图 | `dep_graph` 走 stdlib `ast`；hook 链自解析 YAML 文本 |
| **C-9 描述列**（P-044） | `feature_desc` 三源优先链（制品 H1 → P 行事项 → 目录名）+ `shorten_title` 主名收敛；§2 表新增「描述」列；**零视图层文本引用**（B6 / I-6）；selftest S17-S19 / S26-S27 |
| **C-10 per-feature 流程与交互**（P-044） | `_feature_process_section` → §5.1：锚点目录 + 折叠块（摘要 `{feature} ｜ {阶段} ｜ {P}` / 四文档管道 / 决策链 / 派生状态）；**默认项目级在前**、**无 Mermaid `click`**；selftest S20-S22 / S25 |
| **C-12 架构图显式关系口径**（P-044） | `_arch_section` + `DECLARED_SOURCES` / `TRUTH_NODES`：① `hook → script` ② `script → 真值源` ③ import 边（有则绘）；selftest S23 |
| **不变式 I-8 显式缺口**（P-044） | 「未声明关系的脚本」清单 + 空 import 边如实标「（无）」+ 缺映射保留 `—`；selftest S24 |
| **C-13 hook 链表形态**（P-046） | `hook_chain` 增解析 `name` + `_hook_list` **弃表格改列表块** + `_cell` 升为**通则**；§5 hook 链换形态；selftest S28 / S32 |
| **C-14 步骤级动态描述**（P-046） | `SessionInfo.records` + `read_sessions` 累积多轮 + `_step_table` 六列 + 摘要轮次；**主源 = 事件流**（`scenario` / `ts` / `outcome`），回退链与缺省见 DESIGN §6.6；`reasoning` **不进视图**（守 C-6）；selftest S29-S31 / S33-S34 |
| **不变式 I-9 承载安全**（P-046） | 凡入表格单元格的外部文本一律过 `_cell()`（竖线 → 全角）；长无断点 token 不入表格单元格（hook 正则改入列表块）；selftest S32 + **真实仓 19 张表格 0 列数不齐**（A-8） |
| **C-15 锚点双属性**（P-047） | `_feature_process_section` 输出 `<a name="feat-{f}" id="feat-{f}"></a>`（同一锚两属性）；§5.1 锚点目录不变；selftest S20（改断言）+ A-10（真实仓 26/26 双属性锚） |
| **C-16 映射来源语义反转 + 共享模块**（P-047） | 新增 `scripts/spec_map.py`（`wiki_pid_map` / `progress_pid_map` / `build_pid_map`）；`console_gen` 与 `step_enforce` **同时改为复用**（本地实现删除；`step_enforce.build_feature_pid_map` 仅为 hook 入口薄委托，非第二实现）；§2 关联 P 与 §5.1 摘要随之归位；selftest S35/S36 + A-10（13 项映射差异 / 门禁 32/32 exit 0） |
| **不变式 I-10 语义同源**（P-047） | 映射只有一份实现（`spec_map`）——以**结构保证**替代「双实现 + 对账」（A-33 证伪对账路径）；selftest S35 断言 `console_gen` 模块不再暴露 `feature_pid_map` + 源码层两处均 `import spec_map` |
| **收口批：§6 缺映射清单（D15）** | `_trace_section` 增参并输出「**缺映射（I-8 显式缺口）**」行（有则列出 / 无则显式标「（无——N 个 feature 全部有映射）」）——落地 C-16 ④ 的「计入 §6 缺映射清单」；selftest S37 + A-11 |
| **收口批：兜底面归零** | `CODE_WIKI §9` 补两行 P 标注（`cpp-hub-absorption` → P-002 / `cpp-hub-gap-analysis` → P-004）；实测**依赖兜底 0**（v1.3 为 2）、**错值消解**（`cpp-hub-absorption` P-011 → P-002）、门禁复跑 **32/32 exit 0**（A-11） |

## 3. 归属迁移实录

【A】A-2: **前身两文件已从工作树与索引移除**（`git rm` 实测输出 `rm 'scripts/board_gen.py'` / `rm 'docs/BOARD.md'`）；脚本移除前完成**备份 + 入对象库**双保险。

【A】A-3: **hook 更名且总数不变**（`.pre-commit-config.yaml` 实测）：第五项由 `board-gen` 改为 `console-gen`，`files` 正则与 `pass_filenames: false` 语义**零改动**——既有四项 hook 与本项语义均不变（hook 计数仍为 5）。

## 4. 兼容性与隔离

- **与三校验器**：`console_gen.py` / `spec_map.py` / `step_enforce.py` 均不修改 `dc_validator.py` / `m7_stats.py` / `repo_stats.py` 任一语义；**P-047 新增 1 个 `scripts/` 文件** → `declared.scripts` **7 → 8** 同批同步（P-043 的「前身退役 → 计数不变」不再适用本批）。
- **与验证端门禁**：`console_gen` **不参与** gate 裁决（Layer-1）；但 **P-047 的映射语义变更直接作用于第四 hook `step-enforce` 的 P 定位**——这是本批**唯一触及门禁路径**的改动，且只改「feature → P 指向」（只读映射层），**不改** hook 触发条件、gate 规则与退出码语义（0 就绪 / 1 阻断 / 2 映射缺位）。实测门禁面**无新增阻断**（新语义 32/32 exit 0；旧语义 28/32 + 4 feature 无映射 exit 2），并**消解旧语义下 4 个 feature 的 de-facto 阻断**（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema` 无映射 → hook exit 2）。**独立 pass 更正**：v1.3 所记「消除 `precommit-dc-validator` P-008 无 session → exit 1 误阻断」**不可复现**（P-008 与 P-007 同为 P-020 前批次 → 均豁免 exit 0，A-10）。
- **`verify-anchor` 行为**：零改动（不消费映射）。
- **与 sessions 写入路径**：只读；不触碰 `EventWriter` 唯一写路径。
- **可回退**：映射语义回退 = 恢复 `PROGRESS` 单一来源（视图侧 `—` 缺口恢复为 4 个）；`spec_map.py` 为纯函数模块，删除即回退（两处调用点需同步恢复本地实现）；前身脚本另有字节级备份 + git 对象留存；`docs/CONSOLE.md` 为纯派生可重生成（I-5）。

## 5. 测试与验证（本机实测）

| 项 | 命令 | 结果 |
|----|------|------|
| 生成器自测 | `python scripts/console_gen.py --selftest` | **37/37 PASS**（P-043 16/16 → P-044 27/27 → P-046 34/34 → P-047 36/36 → 收口批 +1） |
| **缺映射清单（P-047 收口批）** | §6 行核对 / selftest S37 | 真实仓输出「**（无——32 个 feature 全部有映射）**」；双分支（有缺口列出 / 无缺口显式标无）由 S37 覆盖 |
| **兜底面归零（P-047 收口批）** | 逐 feature 映射来源比对 | 依赖 `PROGRESS` 兜底者 **0**（v1.3 为 2）；`cpp-hub-absorption` P-011 → **P-002**（错值消解） |
| **映射唯一实现（P-047）** | 源码核对：`grep -n "feature_pid_map\|import spec_map" scripts/*.py` | 两处本地实现已删除、两处均 `import spec_map`（I-10）；selftest S35 断言模块不再暴露 `feature_pid_map` |
| **门禁全 feature 复核（P-047）** | 对每个 `spec/<feature>/` 模拟 hook 调用 `step_enforce.main([...])` | **32/32 exit 0**（`spec/templates/` 非 feature 不入表且其文件不匹配 `FEATURE_RE`） |
| 三校验器 | `dc_validator` / `m7_stats` / `repo_stats` | 见 §7（验收输入） |
| 决策链 | `spec_runner step-enforce --pid P-047` | 见 CHECKLIST |
| 锚点 | `spec_runner verify-anchor --session specwf-p047-20260911` | 见 CHECKLIST |
| 真实仓生成 | `python scripts/console_gen.py` | `docs/CONSOLE.md` 已刷新（**723 行 / 44588 B**，A-11；P-047 为 722 行 / 44526 B） |

【A】A-6: **P-044 真实仓重生成读数（本机实测，2026-09-11）**——`docs/CONSOLE.md` **514 行 / 20027 B**；feature 表 32 行**全部带描述**（例：`project-console → 项目控制台` / `hook-surface → hook 面扩展调研评估` / `independent-verify → 独立验证`；修复前 `independent-verify` 曾被截成 `独立验证（出路 C`，见 DR-8）；§5.1 折叠块 **26 个**（收敛策略排除 6 个「四文档齐备且无 session」的 feature：`m7-hits-block` / `precommit-dc-validator` / `promptfoo-m7-eval` / `repo-stats` / `spec-runner` / `spec-runner-homing`）；折叠对 **26 : 26** 平衡；§5 mermaid 出 **12 条显式关系边**（5 hook→script + 7 script→真值源）× 3；「未声明关系的脚本」= `deepeval_m7_eval` / `pf_m7_eval` / `spec_runner`。

【A】A-4: **P-043 复跑读数（本机实测，2026-09-11）**——`dc_validator` **0 违规**（**首跑拦截 7 项** = 前身两文件退役引发的「档 1 相对链接不可解析」×6（前身 IMPLEMENTATION ×2 + 本 feature RESEARCH ×4）+ 本 IMPLEMENTATION §0 A 类计数声明组成项未落笔 ×1；均于同批修正，见 §6 DR-6）；`m7_stats` 0 违规；`repo_stats` 0 违规；`step-enforce --pid P-043` 五步链 exit 0；`verify-anchor` **9 锚点全真实 / 0 硬性 / 0 软性**；真实仓首次生成 `docs/CONSOLE.md`。

【A】A-12: **P-042 v1.8 复跑读数（本机实测，2026-09-29）**——本批 **零代码变更**（`scripts/` 与 `docs/CONSOLE.md` 均未改）：`dc_validator` **0 违规**；`m7_stats` 恰 **1 条 by-design P3**（样本③ 历史形态，**禁止回改**）；`repo_stats` **P2/P3 归零**；`console_gen.py --selftest` **37/37**（与 P-047 收口批一致）；`step-enforce --pid P-042` 五步链 **exit 0**；`verify-anchor` 锚点全真实。**本批产出** = **纯文档**（`PLAN §1 DC2.1` + `PROGRESS` L3 指向 + 本 feature 四文档 + `CODE_WIKI`）。

**首轮拦截实录（DR-1）**：selftest S4 失败——`_feature_table` 内使用了**模块级常量** `SPEC` 而非传入的 `root/spec`，导致 temp 根下制品链全显 `—`（真实仓恰好有同名目录而"看起来正常"）。修正 = 由 `build()` 显式传入 `spec_dir`，`render`/`_feature_table` 签名同步。**该缺陷只有在「非默认 root」场景才暴露**，是 fixture 化的直接收益（若仅手测真实仓将漏检）。

【A】A-13: **P-042 v1.11 复跑读数 + 两条首跑拦截实录（本机实测，2026-09-30）**——本批**零代码变更**（`scripts/` 零变更 / selftest 保持 **37/37** / `docs/CONSOLE.md` 不重生成）：`dc_validator` **0 违规**（127 文件）；`m7_stats` **0 违规**（1 条 by-design P3；**零新增样本**）；`repo_stats` **0 违规、P3 0**（**首跑 2 P2** → DR-18）；`step-gate` 五步链 / `verify-anchor`（**8 锚点全真实**）/ `step-enforce --pid P-042`（定位 `specwf-p042-20260929v6`）全 **exit 0**（**首跑三命令同报 JSON 解析失败** → DR-19）。

【A】A-14: **P-042 v1.15 复跑读数（本机实测，2026-09-30）**——本批**零代码变更**（`scripts/` 零变更 / selftest 保持 **37/37** / `docs/CONSOLE.md` 不重生成）：`dc_validator` **0 违规**（127 文件）；`m7_stats` **0 违规**（1 条 by-design P3；**零新增样本**）；`repo_stats` **0 违规、P3 0**；`console_gen.py --selftest` **37/37**；`step-gate` 五步链 / `verify-anchor` / `step-enforce --pid P-042`（定位 `specwf-p042-20260930v2`）全 **exit 0**。**本批产出** = **纯文档**（`RESEARCH v1.13 §7.18` + `DESIGN v1.6 D17/§5.2` + 本 IMPLEMENTATION + `CHECKLIST v1.6` + `CODE_WIKI v1.93` + `PROGRESS` P-042 v1.15 追记）。

## 6. 关键决策记录

| # | 决策 | 理由 |
|---|------|------|
| DR-1 | 生成器**取代**而非并列前身 | 用户裁定「接续取代」；并列会留下两套状态词表（与 I-7 冲突） |
| DR-2 | 状态输出**不新增词表**，另设「派生依据」列 | B4/A-17：视图只重投影既有词表；错配根源是升格而非措辞 |
| DR-3 | §6 追溯段**只放指针不复制数字** | I-6 不增真值——复制 M7 计数会造出第二真值源，与 `m7_stats` 看护权冲突 |
| DR-4 | 依赖图**只画仓内边**，动态 import 单列清单 | 外部依赖无稳定节点集；字面量清单足以覆盖 A-28 实测位点 |
| DR-5 | hook 链**自解析 YAML 文本** | 引入 PyYAML 违 I-4；该文件结构稳定且本仓自持 |
| DR-6 | 前身退役必须**同批清理全仓悬空链接** | `dc_validator` 档 1 机械兜底捕获 ×6（前身 IMPLEMENTATION 2 处 + 本 feature RESEARCH 4 处）——**退役动作的连锁面大于直觉**；历史文档的链接应转为纯文本 + 退役注，而非保留死链 |
| DR-7 | 描述**不引 `CODE_WIKI §9`**，采制品自身 H1 | §9 属派生视图，引用会形成「视图依赖视图」并使描述成为第二真值源（B6 / I-6）；代价是需回退链（7 个 feature 缺 RESEARCH，A-36） |
| DR-8 | 主名收敛须**交替**剥「尾括号组」与断 `——` | 单次顺序处理会漏：`独立验证（出路 C——审查臂…）` 若先断 `——` 会截成 **`独立验证（出路 C`**（真实仓首跑即现）、`ARC 升级实施（…）——调研输入引用` 若只剥一次括号也残留括号；两种形态只能靠**迭代至稳定**同时收敛（selftest S26 固化） |
| DR-9 | hook 节点 id 统一为 `H_{id}` 前缀 | selftest S23 首轮拦截：初版 `{id}_hook` 在连字符替换后仍产生歧义命名，与断言不一致；统一前缀后 Mermaid 节点 id 合法且可读 |
| DR-10 | `DECLARED_SOURCES` **只对实际存在的脚本**绘边，另设「未声明关系」清单 | ① 避免在非本仓 root（含 selftest fixture）绘出**幽灵节点**；② 契约漂移（新增脚本未登记）**可见**而非静默（I-8）；现态缺口 = `deepeval_m7_eval` / `pf_m7_eval` / `spec_runner` |
| DR-11 | hook 链**弃表格改列表块**（而非「保留表格 + 仅转义竖线」） | 转义只解决**表结构被破坏**（A-37），不解决**列被压扁**（A-38）：长正则仍是表中最宽的无断点 token，会把后续列挤到 5–10px；列表块让长 token **独占一行**，一次消除两类缺陷。附属收益：`name` 字段可完整展示（A-39 表明该字段本就在真值源中却未被取，是「看不懂」的另一半原因） |
| DR-12 | 步骤表**以事件流为主源**，文档元数据仅作逐级回退；同 step 多轮**最新一轮胜出** | A-40 实测事件流 `scenario`/`outcome`/`reasoning` **100% 齐备**，而文档侧 `创建日期` 仅 50/77、`Spec 步骤` 54/77、front-matter 25/77、修订历史 13/77 且**四种以上标题形态**（A-42）——以稀疏且命名漂移的元数据为主源会「补得像有」；多轮取最新一轮符合「当前态」语义，全轮次以「修改历史」列显式保留（历史不丢、当前不漏）。`reasoning`（常数百字）**不进视图**以守 C-6 单一认知块 |
| DR-13 | 锚点**双属性**（`name` + `id` 并行），不选任一单属性 | 两形态各有失效面且**本机不可验远端渲染**：GitHub 官方只背书 `name`（但明示不进 outline/TOC），`id` 是 HTML5 标准但「GitHub 是否剥离 `class`/`id`」有冲突证据（A-44）。双属性 = 每锚多一个属性、零新机制面/零新依赖，把「另一类渲染器失效」从**静默风险**变为被覆盖；残余风险（两者皆剥离）退化为「可折叠不可跳转」并登记 H8 |
| DR-14 | 映射语义**反转**（§9 行标注优先）且**收敛为共享模块**（`spec_map`，禁双实现） | A-33 的失效形态是**两实现同错**（`PROGRESS` 行内链接被「引用上游依据」劫持 → 4 feature 永久无 P），对账**抓不住**；故 (a) 抽共享纯函数模块（结构上只存在一处语义，I-10）优于 (b) 双实现 + 对账（已证伪）、(c) 只改一处（制造双语义）。**语义副作用已明示**：关联 P 由「末批 P」变为「§9 主 P」，真实仓 13 项差异（v1.3 首轮 4 空洞补齐 + 9 主 P 归位；**收口批后 14 项** = +`cpp-hub-absorption` 错值消解）——属语义明确化，且 `§9` 行自此须与 feature 主 P 同步维护（漂移由 I-8 缺口清单兜底） |
| DR-15 | 收口批：**兜底面归零 + §6 缺映射清单落地**（而非「缺口=0 即视为闭环」） | 复核发现 v1.3 有两处未闭环：① 「计入 §6 缺映射清单」**声明未落地**（实现只到 §2 的 `—`）→ 补 `_trace_section` 行；② 仍有 **2 个 feature 依赖兜底源**，其中 `cpp-hub-absorption` 实测被**劫持为 P-011（应为 P-002）**——即 A-33 残余实例。二者都不在「缺口 4 → 0」的判据范围内 → 补两行 §9 标注使**兜底面 32/32 归零**，并把「判据必要不充分」固化为 **B5** |
| DR-16 | **独立 pass 复核更正**（v1.3 记述与机械读数不符 → **改记述、不改读数**） | Step 10 独立 pass（同基座降级）复跑发现两处 v1.3 记述不可复现/漂移：① 「消除 `precommit-dc-validator` 误阻断」——`P-008` 与 `P-007` 同为 P-020 前批次，`int(pid.split("-")[1]) < 20` 历史豁免对两者**均**生效 → **hook 层 exit 0**（实测输出「为 P-020 前历史批次 → 豁免」）；旧语义实际消解的是 **4 个无映射 feature 的 hook exit 2**；② 映射差异计数收口批后为 **14**（非 13）。读数经**独立重算**确认无误，故更正记述侧（A-10 / §4 / §7 / B4 同轮），并登记「**runner 层读数 ≠ hook 层结论**」这一读法陷阱 |
| DR-17 | 状态归属契约**上提 `PLAN §1`（新增 `DC2.1`）而非留在 `PROGRESS`**，且**不与 DC2 合轴** | A-46 实证任务状态**无契约面**（DC2 为 type 主轴、无校验器读 `PROGRESS` L3）⇒ 须给它一个**权威定义地**（**契约面 > 载体声明**，B6）；同时**不并入 DC2**（另一轴，并入即**混轴回归**）⇒ 以**轴正交**的 `DC2.1` 承载，`PROGRESS` L3 仅保留**指向**。本批**零代码**：只定义归属与「来源」列，实现面（`derive_state` 首参 / 状态列迁移 / 修订 I-7）留 **P2** |
| DR-18 | **`repo_stats` PT-11 模式把正文 P 区间误捕为 `fs.progress_tasks` 读数**（P-042 v1.10 首跑 2 条 P2）→ **只改正文、不改模式** | 事实（E1）：本批在 `CODE_WIKI.md` banner 与 §2.1 树写入「豁免面区间 `P-001~P-019`」，而 PT-11 的正则（`P-` + 三位数字 + `~` + `P-` + 三位数字，取第 2 组）**不区分语义**，把**任何**该形态都当作 progress_tasks 的声明读数 ⇒ 取首个匹配得 **19 ≠ 真值 57**。**性质 = 模式库正则的语义限定缺失（Layer-1 工具面）**；**同族** = M7 §4 候选「**R7 管辖边界显式化 + 正文枚举计数弱纪律**」（同为「正文散文 vs 机械读数」的边界）+ P-041 期 PT-8 正则过宽曾收敛 6 处误捕。**触发条件（任一即重审）** = ① 同类误捕复现 **≥1 例**（本次第 1 例；**同批自证第 2 例**——v1.11 的 DR-18 描述本身**引述**了被误捕的字面写法，首跑再现 1 条 P2，改用不引述的表述后复跑归零；**该次是否计入「复现」留用户裁决**）② 用户裁决。**载体预判** = 方向 A（**Layer-0，优先**）**弱纪律**：正文写 P 区间时**避开与真值声明同形**（用「至」而非 `~`）或就地附重数命令；方向 B（Layer-1）**给 PT-11 加语义限定**（如要求区间终点 = 真值，或限定出现在「登记在册 / 在册」上下文）——**倾向否决**（引入启发式 ⇒ 误报面扩张 + 撞 I-10：每模式 bespoke 化）。**边界** = 本批**不改 `repo_stats`** |
| DR-19 | **session 写入非法 JSON 转义 ⇒ 三个门禁命令同时失败，且报错不报文件名/行号** → **就地重写该行；门禁行为不改** | 事实（E1）：`specwf-p042-20260929v6.jsonl` **第 4 行**含**未按 JSON 转义**的反斜杠 ⇒ `step-gate` / `verify-anchor` / `step-enforce` **三命令同报** `JSONDecodeError: Invalid escape: line 1 column 834` ⇒ exit 1。**根因两条**：① **写入端**——jsonl 内嵌正则字面量时反斜杠须按 JSON 转义，而**同一文件第 1 行**写法正确 ⇒ **同文件内两种写法并存**（无机械看护）；② **报错端（可用性缺口）**——异常只给**被解析行内**的 `line 1 column N`，**不报文件名与文件行号**，与「line 1」的字面直觉冲突（本臂据此先查第 1 行、实际故障在第 4 行，定位成本显著）。**性质** = ① 生成端纪律（可机械自检：写后逐行 `json.loads`）② Layer-1 工具面**报错可读性**；**门禁已覆盖该故障类**（三命令均解析 session ⇒ 非法 JSON 立刻 exit 1）⇒ **非覆盖缺口**。**触发条件（任一即重审）** = ① 同类复现 **≥1 例**（本次第 1 例）② 用户裁决。**载体预判** = 方向 A（Layer-0，弱纪律）**写入端自检 + 避免转义写法**（本批已实证「改写为无转义表述」可行）；方向 B（Layer-1）**改进 `spec_runner` 读 session 的异常包装**（输出 `<path>:<行号>: <msg>`）——**成本低、零新依赖、不撞 I-10** ⇒ **倾向可采**，但须**另立批**。**边界** = 本批**不改 `spec_runner`** |
| DR-20 | **证据等级虚高：把「从工具行为反推机制」的推断当 E1 使用**（P-042 v1.12 自我订正）→ **补实测 + 立纪律** | 事实（E1）：上一轮（v1.10）在 §7.15 A-50 的根因段写出两个**具体映射值**（`drift-gate → P-023` / `academic-writing-workflow → P-040`）并随段标 **E1**，但该二值当时**未核**（系从「三条改 `spec/` 的批次未被要求 session」的**行为反推**得出）⇒ 经 v1.11 实跑 `spec_map.build_pid_map()` **确认二值正确**——即 **结论对 ≠ 论据充分**（运气成分未被排除）。**同批第二例（性质不同：属误读）** = 我方复述「其后五分支**不可达**」时**去掉了数据前提**，而仓内 [§3.8.6/§3.8.1](../rework-and-decision-paths/RESEARCH.md) 原文为「PROGRESS 50/50 全 `done` ⇒ `done` 首分支短路 ⇒ 后四分支不可达」——**前提齐备、措辞无误** ⇒ 缺陷在**复述方**，仓内文档不改。**性质 = 证据纪律缺陷（Layer-0 弱纪律面）**；**同族** = M7 §4 候选「**R7 管辖边界显式化 + 正文枚举计数弱纪律**」（同属「声明与机械读数的边界」）+ drift-gate §4.4（front-matter 状态 vs 对外声称）。**触发条件（任一即重审）** = ① 同类复现 **≥1 例**（本次为**第 1 例**，且含**误读型**变体 1 例）② 用户裁决。**载体预判** = 方向 A（**Layer-0，优先**）**弱纪律**：凡**推断句**（证据为「从行为反推」）**不得使用 E1 标级**，须标 **E2 或「待核」**，并在同批或次批补实测；方向 B（Layer-1）**在 `dc_validator` 增加「E1 句须附可复算命令或实测出处」的机械约束**——**倾向否决**（自然语言断言无法可靠判定证据来源，机械实现会退化为关键词启发式 ⇒ 撞 I-10）。**边界** = 本批**不改任何校验器**、**不新增门禁**。 |
| DR-21 | **`verify-anchor` 锚点路径约束未成文 + 报错不定位锚点**（P-042 v1.12 实施期首跑拦截）→ **改锚点写法；工具行为不改** | 事实（E1）：使 `verify-anchor` 判 **9 真实 / 2 硬性 / 0 软性 → exit 1** 后逐项试错定位，实测四类形态判别如下——**判真实** = `spec/project-console/RESEARCH.md §7.16`（`spec/` 前缀 + `.md` + §章节）、`docs/PROGRESS.md#L3`（`docs/` 前缀 + `.md` + **单行** `#L`）；**判硬性违规** = 根级 `CODE_WIKI.md`（**无 `spec|adr|docs|tools|scripts` + `/` 前缀**）、`scripts/spec_map.py#L76-L83`、`scripts/console_gen.py#L298-L310`（**`.py` 载体 + 行号区间**）；**判软性** = `scripts/spec_map.py`（纯文件、无章节、无行号）⇒ 软性又使 `step-gate` **exit 2（人工复核）**。**变量未隔离（如实登记）** = 硬性违规的判别因素有二候选——① **仅 `.md` 可作锚点载体**（`.py` 一律不受理）② **行号区间形态不被支持**而单行 `#L` 支持；本批**未做单变量对照**（未在 `.md` 上试行号区间、未在 `.py` 上试单行 `#L`）⇒ 留作修复批首步实测。**报错端（可用性缺口）** = 失败输出**只给三类计数**（`锚点 N 真实 / M 硬性 / K 软性`），**不指出是哪一个锚点、也不给原文** ⇒ 定位只能逐条删改试错（**本轮 3 次往返**）。**性质** = ① 工具**契约未成文**（`ANCHOR_RE` 前缀白名单与载体/行号形态限制未落在 `spec/independent-verify/` 文档中，属 I-8 显式缺口的反面：**约束隐式**）② Layer-1 工具面**报错可定位性**；**门禁行为本身正确**（错误锚点确应拦）⇒ **非覆盖缺口**。**同族** = **DR-19**（同一工具族的报错信息量不足）+ P-051 族 / M7 样本㉛（工具报错不指向具体位点）。**触发条件（任一即重审）** = ① 同类复现 **≥1 例**（本次第 1 例）② 用户裁决。**载体预判** = 方向 A（**Layer-0，优先**）**弱纪律**：写 session 锚点只用「`spec|adr|docs|tools|scripts` 前缀的 **`.md`** + **§章节**」（本批已实证可行，且不需任何工具改动）；方向 B（Layer-1）**两件，均成本低、零新依赖、不撞 I-10**：(i) `verify-anchor` 增开发期开关**输出逐锚点明细与失败锚点原文**（对齐 DR-19 方向 B 的 `<path>:<行号>` 包装）(ii) 在 `spec/independent-verify/` 文档中**显式登记 `ANCHOR_RE` 契约与受支持形态表**（消隐式约束）⇒ **倾向可采**，但须**另立批**（本批只登记）。**边界** = 本批**不改 `spec_runner.py`**、**不动 `spec/independent-verify/` 文档**、**不新增门禁**。 |
| DR-22 | **P2a（`derive_state` 拆支）属可见行为变更** → 验收**不得只跑 `--selftest`** | 事实（E1，A-54）：`tier` 有**三处可见输出位点**——① §状态表「行动档」列 ② 三级行动队列 ③ per-feature 折叠块；`pending` 且无 session 的 feature 在真实仓**存在**（V2a 补建 session 前至少 4 例：P-048 / P-053 / P-054 / P-055）⇒ 拆支后这些行由「`Needs Attention`」变为「`Recommended`」，属**可见输出变化**。`--selftest` 只跑 fixture、不渲染真实仓 ⇒ 单跑 selftest **无法**观测该变更。**正确性只能由 fixture 观测**（三 fixture：`pending` 无 session / `pending` 有 session / `done` 无 session 短路早退）**+ 真机 CONSOLE 三处位点对照**（F25~F28）。**同族** = DR-12（步骤表主源取舍时同样区分「fixture 可观测」与「真机可观测」）。**边界** = 本批**只登记该验收要求**，不改代码；P2a 实施留 P0 批。 |

## 7. 对验收的输入

- selftest **37/37**（P-047 收口批；A-11）；三校验器全绿；`step-enforce --pid P-047` 五步链 exit 0（P-044/P-046 复跑留档见 CHECKLIST §8）；`verify-anchor` 锚点全真实
- **门禁面**：全 feature 复核 **32/32 exit 0**（新语义；A-10 与收口批复跑 A-11）——映射语义变更**未引入新阻断**，并消解旧语义下 4 个无映射 feature 的 de-facto 阻断（hook exit 2）；**独立 pass 更正**：v1.3 所记「消除 `precommit-dc-validator` 误阻断」不可复现（P-008 同为 P-020 前批次 → 豁免 exit 0）
- **收口批**：§6 缺映射清单落地（真实仓显式「（无——32 个 feature 全部有映射）」）；**兜底面归零**（依赖兜底 0，v1.3 为 2）；`cpp-hub-absorption` 错值 **P-011 → P-002** 消解
- 真实仓产物：`docs/CONSOLE.md` **723 行 / 44588 B**（A-11）；hook 链 5 条列表块 / 折叠块 26（26:26）/ 步骤表 69 行 / 双属性锚 26 / **import 边非空**（`console_gen → spec_map` / `step_enforce → spec_map`）/ 全表 **0 列数不齐**（I-9）
- 源码层：映射唯一实现（两处 `import spec_map`；本地实现已删，`step_enforce.build_feature_pid_map` 仅为 hook 入口薄委托；I-10）
- 视图层同步位点：CODE_WIKI（版本头 / §2.1 脚本树与 docs 树 / §9 索引 / 覆盖对象 / declared / PT-11）
- **本批（P-042 v1.8 / Layer-0）**：**零代码变更**（`scripts/` 与 `docs/CONSOLE.md` 未改；A-12）——落点 = `spec/doc-contract/PLAN.md §1` 新增 `DC2.1 任务状态词表（+「来源」列）` + `docs/PROGRESS.md` L3 指向；`derive_state` 首参 / `PROGRESS` 状态列迁移 / I-7 修订 **留 P2（Layer-1）**
- **本批（P-042 v1.15 / P0 批实施设计）**：**零代码变更**（`scripts/` 与 `docs/CONSOLE.md` 未改；A-14）——落点 = `RESEARCH v1.13 §7.18`（三项待裁决裁定 + P0 批四文档实施设计）/ `DESIGN v1.6 D17 + §5.2` / 本 IMPLEMENTATION（A-14 + DR-22）/ `CHECKLIST v1.6 F25~F29`；**P2a 实施**（`derive_state` 拆支）**留 P0 批**（属可见行为变更，验收见 DR-22 / F25~F28）
- 独立 pass：**已执行（P-047 收口批；同基座降级标注，见 CHECKLIST §8.2）**

## 附录 A：A 类断言明细

- A-1 至 A-14：见 §2.2 / §3 / §5 各 `【A】` 行（本机实测；A-5/A-6 为 P-044 新增，A-7/A-8 为 P-046 新增，A-9/A-10/A-11 为 P-047 及收口批新增，**A-12 为 P-042 v1.8 新增**，**A-13 为 P-042 v1.11 新增**，**A-14 为 P-042 v1.15 新增**）。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "以「单脚本 + 单产物 + 单 hook」的最小机制面即可同时满足四维诉求（feature 级制品链投影 / 决策链状态机 / 架构与依赖流程 / 追溯覆盖），无需新增第二个生成器或第二产物；三视图共用同一确定性基准可保证跨视图一致性", "basis": "A-1 selftest 16/16（八章渲染齐备）+ DESIGN §3.1 单写路径 + RESEARCH B1 真值源零新增采集面"},
  {"id": "B2", "inference": "以「显式架构契约常量」（hook→script + script→真值源）替代不可得的 import 推断，可在不新增采集面的前提下使架构图恢复信息量；代价是常量须随新增脚本同批维护，故必须以「未声明关系」清单兜底——否则契约漂移会静默", "basis": "A-6 实测 import 图为空（口径信息量为零）+ RESEARCH A-35 / C-12 + IMPLEMENTATION DR-10（只对实际存在脚本绘边 + I-8 清单）"},
  {"id": "B3", "inference": "「承载安全」不能只靠单元格转义：转义只消解**结构破坏**，消解不了**列宽坍缩**——后者的根因是长无断点 token 与表格列宽自适应机制的相互作用。故承载不自我破坏的充分条件是「形态选择」与「文本安全化」两条同时成立（长 token 移出表格 + 余下外部文本一律安全化），单靠任一条都不充分", "basis": "A-8 I-9 机械核对（19 张表格 0 列数不齐）+ RESEARCH A-37（表列数不齐）/ A-38（长 token 压列）分离为两类缺陷 + IMPLEMENTATION DR-11（弃表格而非仅转义）"},
  {"id": "B4", "inference": "当同一语义存在两份实现时，**「结构上只保留一处」是比「事后对账两处」更强的保证**：对账的检验力上限是「两处是否一致」，而该缺陷类（同源同错）恰好在一致侧，故对账通过 ≠ 语义正确。可行的替代只有「唯一实现」——因为它把「一致」从需要被验证的性质变成构造上不可违反的性质", "basis": "A-10 门禁复核（新语义 32/32 exit 0；旧语义 28/32 + 4 feature 无映射 exit 2；独立 pass 更正「precommit-dc-validator 误阻断」不可复现）+ RESEARCH A-33（两实现同错、对账抓不住）+ DESIGN §6.8 方案 (a)/(b)/(c) 对比（(b) 证伪、(c) 更坏）"},
  {"id": "B5", "inference": "以「缺口数归零」作为「缺陷类是否消解」的验收判据是**必要而不充分**的：缺值（None）会被计数覆盖，错值（有值但指向错误对象）不会被计数覆盖。故凡「收敛到唯一来源」类改造，判据须同时含**来源分布**（多少对象仍依赖兜底/次级来源）而非只看缺口计数——来源分布能暴露「未被人工确认的对象集」，缺口计数不能", "basis": "A-11 收口批复核：`cpp-hub-absorption` 在旧新语义下同为 P-011（错值，应为 P-002）→ 不进「缺口 4 → 0」统计，却造成视图内事实错误；补 §9 两行后**依赖兜底者 2 → 0**，错值同时消解（A-11 ③④）"},
  {"id": "B6", "inference": "对「词表 / 契约」类定义，权威性来自「契约面」而非「载体声明」——同一组取值声明在载体（真值表）里只是数据、无契约效力（无校验器读、无定义性），上提到契约文档（`PLAN §1`）才获得与 DC1-DC4 同级的权威；且同一契约文档内**不同「轴」的维度须分块承载**（轴正交），不可合表，否则会污染按轴分派的校验分支", "basis": "A-46 DC2 为 type 主轴、任务状态另属一轴且无校验器读 `PROGRESS` L3 + IMPLEMENTATION DR-17（上提 `PLAN §1 DC2.1` + 不合轴）+ DESIGN §8 方案 G/H（并入 DC2 / 只改 `PROGRESS` 均否决）"}
]
```

---

**Review 签字**: _________ 日期: _________
