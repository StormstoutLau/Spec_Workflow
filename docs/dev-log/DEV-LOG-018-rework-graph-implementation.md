# DEV-LOG-018: 回写返工图路径 A 实施（P-051：分叉关联登记 + 触发条件 + 只读对账）

> **日期**: 2026-09-27 至 2026-09-29（回补）
> **会话**: `specwf-p051-20260927`（五步链）· `specwf-p051-20260927v2`（事件流补建三步链，首步明示【补建】）
> **涉及**: `spec/rework-graph/`（RESEARCH v1.1 / DESIGN v1.1 / IMPLEMENTATION v1.1 / CHECKLIST v1.1 → v1.3 accepting）· `docs/rework-graph.json`（返工图真值源）· `scripts/rework_graph_check.py`（只读对账器，351 → 358 行）· `docs/PROGRESS.md`（P-051 行）· `CODE_WIKI.md`（v1.71 → v1.75）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-051 行](../PROGRESS.md) · [RESEARCH](../../spec/rework-graph/RESEARCH.md) · [DESIGN](../../spec/rework-graph/DESIGN.md) · [IMPLEMENTATION](../../spec/rework-graph/IMPLEMENTATION.md) · [CHECKLIST](../../spec/rework-graph/CHECKLIST.md) · [rework-graph.json](../rework-graph.json) · [rework_graph_check.py](../../scripts/rework_graph_check.py) · [CODE_WIKI](../../CODE_WIKI.md)

## 做了什么（时序）

1. **Step 1-2 调研与设计落档**：核验「完整形态 = 分叉原语 + 原/新流关联登记 + 触发条件」——**判定 = 机制层可实现（路径 A）**，三件现状 **1 有 2 缺**（`spec_runner fork` 已有；关联登记 P-050 已自登记为缺口；触发条件无）。四件套落档：RESEARCH **v1.1**（16A+5B+4C+3H）+ DESIGN **v1.1** + IMPLEMENTATION **v1.1** + CHECKLIST **v1.1 pending**，**31/32 有条件通过**，唯一待办 = 真异基座独立 pass。
2. **实施（`fork` 零改动）**：交付 ① `docs/rework-graph.json`（`forks: []` —— 本仓尚无真实返工回写；1 条 `non_rework` 豁免 = P-009 `fork` 能力演示）；② `scripts/rework_graph_check.py`（三段式「声明 → 实测 → 对账」；判定表 **19 条** = A 表结构 4 / B 边自洽 7 / C 对账 6 / D 孤儿 2；selftest **30/30**）。替代方案 5 全否决；不变式 I-1 至 I-7；实施期 3 发现 DR-1/DR-2/DR-3。
3. **Step 8 独立审查（同基座降级标注）**：**6 项发现（3 P2 + 3 P3）全部整改**，selftest **28/28 → 30/30**；**元发现「声明计数 ≠ 枚举明细长度」+「验证命令未复算即充作证据」**；同轮全覆盖终验补漏 3 处同族残留。
4. **候选登记批**：于 **M7 账本 §4** 登记**兄弟候选**「R7 管辖边界显式化 + 正文枚举计数弱纪律」（候选池未激活；显式否决 Layer-1 通用校验器，撞 I-10）。
5. **真异基座独立 pass 批（2026-09-29，异基座子代理，RULE-1 / RULE-5 双满足）**：判定 **有条件通过 → 7 项发现（2 P2 + 5 P3）整改后转「验收通过 32/32」**；其中 **1 项审查臂假阳性经本臂复核证伪**（fork 锚点 off-by-one 不成立）。
6. **事件流补建批（2026-09-29）**：新增 `specwf-p051-20260927v2.jsonl`（`implement` / `verify` / `finalize` 三步，**首步明示【补建】**）——根因 = 控制台步骤级描述**主源 = 事件流**而候选登记 / 独立 pass 两批零新决策事件，且 `console-gen` **幂等**（非 bug 而是覆盖缺口，与 P-050 v1.2 的 P2-1 同族）；CHECKLIST **v1.2 → v1.3**，CONSOLE 摘要转 2 轮。

## 决策依据

### ① 载体 = `docs/rework-graph.json`（而非新建 `inventory/` 或 YAML）

本仓无 `inventory/` 目录；取 **JSON** 是为守 **I-3 零依赖（stdlib only）**（数据取 JSON 而非 YAML，为使用例中 DR-3 的载体改判）。真值源裁定 = `registry` 唯一真值，`vN` 后缀不承担 lineage（源：DESIGN §4 / PROGRESS P-051 行）。

### ② 关键机械信号 = `fork` 复制行逐字保留源 `session` 名

`cmd_fork` 只把 `fork: <new> <- <session>` 打到 stdout，事件 schema 无 lineage 字段。但 **`fork` 复制行时逐字复制原行（含 `session` 字段）** ⇒ 「行内 `session` ≠ 文件名 stem」即一次 `fork` 的输出，据此做**孤儿扫描**（判定表 D），**零新增契约**（源：`rework_graph_check.py` docstring / PROGRESS P-051 行）。

### ③ 不接门禁（同 `downstream_compliance` 先例）

「是否接门禁」登记为**触发驱动观察项**（真实返工 fork ≥ 3 例 或 用户裁决）；本批只交付**只读对账器**，`--selftest` 的临时文件写入是唯一写点，**仓库路径零写入**（源：PROGRESS P-051 行 ⑪/⑫）。

### ④ 边界声明 = 「清单不是事实」

本器只保证「**已登记的分叉属实**」+「**fork 输出无漏登**」，**不保证**「所有返工都被登记」（无信号者不可判），也**不评价**「该不该回写」（源：`rework_graph_check.py` docstring §边界）。

## 遇到的问题

- **P2-2 计数与枚举不一致**：「七种『缺』」语音计数与枚举不符 ⇒ 复读 RPC 源码 `rpc_check.py`（**L1147-1164**）得**实为 8 类**，改**免计数枚举**（本仓 **7 类** / RPC **8 类**）（源：PROGRESS P-051 行 Step 8）。
- **P2-3「只读」证据不可复现**：`rg` 命令的 `|` 在 ripgrep 中非 alternation ⇒「零命中」实为规则失效，措辞改为「仓库路径零写入（唯一写点在 selftest tempfile）」（源：同上）。
- **元发现 = 本批 Step 8 的「全覆盖终验」自身未全覆盖**（grep 模式只搜「七种」未搜「六种」+ 范围漏 §2.2 与脚本 docstring）⇒ R7 管辖边界候选再 +1 实证（源：PROGRESS P-051 行 ⑫）。
- **`trigger_kinds` 的「值」不可自动**：RPC 自身亦停在 `undecided`，故触发条件的值不可自动推定（源：RESEARCH H2）。

## 下一步

- **接门禁观察项**触发驱动：真实返工 fork ≥ 3 例 或 用户裁决（当前 `forks=0`）。
- **P-051 全部待办清零**：真异基座独立 pass 已于第 5 阶段完成（32/32）；事件流已补齐（源：PROGRESS P-051 行 ⑫/⑬）。