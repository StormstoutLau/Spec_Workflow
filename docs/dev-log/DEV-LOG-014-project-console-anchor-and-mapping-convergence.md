# DEV-LOG-014: 项目控制台锚点双属性 + 映射语义反转与共享模块（新增 scripts/spec_map.py，建立不变式 I-10）

> **日期**: 2026-09-11（回补）
> **会话**: `specwf-p047-20260911.jsonl`（五步链：research / design / implement / verify / finalize；含同日**收口修正批**）
> **涉及**: spec/project-console/（DESIGN v1.2 → v1.3 / IMPLEMENTATION v1.2 → v1.3 / CHECKLIST v1.2 → v1.3 accepting）/ scripts/spec_map.py（**新增**）/ scripts/console_gen.py / scripts/step_enforce.py / docs/CONSOLE.md（重生成）/ docs/PROGRESS.md（P-047 行）/ CODE_WIKI.md（v1.48 → v1.49 → v1.50）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-047](../PROGRESS.md) / [project-console RESEARCH](../../spec/project-console/RESEARCH.md) / [project-console DESIGN](../../spec/project-console/DESIGN.md) / [project-console IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) / [project-console CHECKLIST](../../spec/project-console/CHECKLIST.md) / 共享模块 `scripts/spec_map.py` / 会话 `tools/spec_runner/sessions/specwf-p047-20260911.jsonl`

## 做了什么（时序）

1. **research 步**：承接 P-045 RESEARCH v1.3 §7.10 的 C-15 / C-16 裁定（P-046 时按用户指定延后），用户指令「执行 C-15 和 C-16」；确认落码输入：C-15 = 锚点改**双属性**；C-16 = 映射**语义反转** + **收敛为共享纯函数模块**，预期缺口 4 → 0，不改历史 PROGRESS 行。
2. **design 步**：DESIGN v1.3 落档，新增 **D13（锚点双属性，§6.7）** + **D14（映射来源语义反转与共享模块，§6.8）**，并在 §3.3 新增不变式 **I-10（语义同源）**；§6.8 **明示语义副作用**（「关联 P」由「末批 P」变为「§9 主 P」）。
3. **implement 步**：**本批首次新增 `scripts/` 文件**——新增 `scripts/spec_map.py`（`wiki_pid_map` / `progress_pid_map` / `build_pid_map`，stdlib only）；`console_gen.py` 删本地 `feature_pid_map` / `P_IMPL_RE` 改调共享模块 + 锚点改双属性 + `TRUTH_NODES` 增 `TS_wiki` + `DECLARED_SOURCES` 增 `spec_map → PROGRESS + CODE_WIKI §9`；`step_enforce.py` 删本地 `P_ROW_RE` / `build_feature_pid_map` 改调共享模块（hook 参数与退出码语义不变）。selftest **34/34 → 36/36 PASS**（S20 改断言双属性锚；新增 **S35** 优先级 / 兜底 / 空表 + 断言 `feature_pid_map` 已不存在、**S36** §9 行标注补 PROGRESS 映射洞）。
4. **verify 步**：**映射语义变更为本批最大风险面**，以**逐 feature 机械比对**替代抽样——实测**映射差异 13 项**（4 项空洞补齐 + 9 项主 P 归位），真实 feature **缺映射 0**；门禁行为复核 **32/32 exit 0**；真实仓 **双属性锚 26/26**；**import 边首次非空**（`console_gen` / `step_enforce` → `spec_map`）；全表仍 0 列数不齐（I-9）；三校验器 0 违规 + 五步链 exit 0 + 锚点全真实。
5. **finalize**：PROGRESS 新增 P-047 行 + CODE_WIKI v1.48 → v1.49 + `declared.scripts` 7 → 8 + `docs/CONSOLE.md` 重生成；**零新增 M7 样本**。
6. **收口修正批（同日）**：D15 §6 缺映射清单落地（`_trace_section` 增「缺映射（I-8 显式缺口）」行，修正 v1.3「声明未落地」；selftest **36/36 → 37/37**）；`CODE_WIKI §9` 补两行标注（`spec/cpp-hub-absorption/` → P-002、`spec/cpp-hub-gap-analysis/` → P-004）⇒ **兜底面 32/32 归零**并消解 `cpp-hub-absorption` **错值 P-011 → P-002**；实测 `docs/CONSOLE.md` **723 行 44588 B**、门禁 **32/32 exit 0**；四文档升 **v1.4**（verified / accepted）；CODE_WIKI v1.49 → **v1.50**。

## 决策依据

### ① 为什么锚点用双属性而非单属性（D13）
**A-44**：宿主（GitHub GFM）**只官方背书** `<a name>` 且明示不进 outline/TOC；`<a id>` 是 HTML5 标准形态，但「GitHub 是否剥离 `class`/`id`」存在**相互冲突的证据**。任一单属性都会把「另一类渲染器失效」变为**静默风险**；双属性零新机制面、零新依赖，属纯承载层冗余。两者皆剥离则退化为「可折叠不可跳转」，残余风险登记 **H8**（真机存活率，本机不可验远端渲染）。

### ② 为什么收敛为共享模块而非「双实现 + 对账」（D14，建立 I-10）
**A-33** 的失效形态是**两实现同错**（`console_gen.feature_pid_map` 与 `step_enforce.build_feature_pid_map`），一致性对账**只能检出「不一致」、检不出「两处一致地错」**⇒ 选项 (b) 双实现 + 对账已被证伪；选项 (c) 只改一处会制造**双语义**（同一 feature 在视图与门禁中指向不同 P），比双实现更坏 ⇒ 取 (a) **抽共享纯函数模块**，以「结构上只存在一处语义」替代「事后比对两处语义」。

### ③ 为什么不改历史 PROGRESS 行
读取端解决（维持 C-11 ④）：历史叙事**零扰动**，映射权威改由 `CODE_WIKI §9` 行标注承担。

### ④ 收口批的判据教训（B5）
C-16 的验收判据「**缺口 4 → 0**」只覆盖**缺值**、不覆盖**错值**（`cpp-hub-absorption` 旧新语义都给 P-011，故不入缺口统计却仍是错值）⇒ 该指标**必要不充分**，须并核**来源分布**（多少 feature 仍依赖兜底源）。

## 遇到的问题

- **映射语义变更 = 最大风险面**：处置 = 逐 feature 机械比对而非抽样（13 项差异与 C-16 ④ 预期一致）。
- **兜底面残余（收口批）**：v1.3 实施后仍有 2 个 feature 无 §9 标注（`cpp-hub-absorption` / `cpp-hub-gap-analysis`）⇒ 仍走「易被劫持」的兜底源，实测 `cpp-hub-absorption` **被劫持为 P-011**（应为 P-002）；收口批补两行 §9 标注消解。
- **独立 pass 更正 v1.3 两处记述**：如「消除 `precommit-dc-validator` P-008 误阻断」**不可复现**；收口批后映射差异合计 **14 项**（首轮 13 + 错值消解 1）。

## 下一步

- **C-13 至 C-16 已全数执行**（P-045 RESEARCH v1.3 §7.10 剩余待办清空）。
- **新增维护纪律**：`CODE_WIKI §9` 行须与 feature 主 P 同步维护；漂移由 I-8 缺口清单兜底（I-8 缺映射行已落地）。