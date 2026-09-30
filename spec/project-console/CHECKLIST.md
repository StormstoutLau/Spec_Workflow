---
id: project-console-CHECKLIST
type: design
version: 1.7
status: accepting
date: 2026-09-11
depends: [project-console-IMPLEMENTATION, project-console-DESIGN]
upstream: null
---

# 验收清单：项目控制台实施批（P-043）/ 视图增补批（P-044）/ 承载与步骤表批（P-046）/ 锚点与映射收敛批（P-047，含收口修正批）

> **Feature**: 项目控制台（`spec/project-console/`）
> **被验收物**: [DESIGN v1.6](./DESIGN.md) + [IMPLEMENTATION v1.10](./IMPLEMENTATION.md)
> **Spec 步骤**: Step 7-8
> **v1.1 变更（P-044）**: 新增功能验收 **F11-F15**（描述列 / 描述回退链 / per-feature 折叠与锚点 / 三口径架构图 / I-8 缺口清单）+ 不变式 **I-8** 行；§8 补 P-044 复跑记录；§9 回填 H6/H7 实测部分。
> **v1.2 变更（P-046，用户指令「先执行 C-13 和 C-14，C-16 共享模块单独处理」）**: 新增功能验收 **F16**（hook 链列表块 + `name` + 安全化通则）/ **F17**（步骤级动态描述六列 + 多轮 + 无 session 显式缺失）+ 不变式 **I-9** 行；§8 补 P-046 复跑记录（含 **I-9 全表机械核对**）；§9 再回填 H6/H7；**C-15 / C-16 显式登记为「不在本批」**。
> **v1.3 变更（P-047，用户指令「执行 C-15 和 C-16」）**: 新增功能验收 **F18**（锚点双属性）/ **F19**（映射来源语义反转 + 共享模块唯一实现）+ 不变式 **I-10** 行；新增 **门禁面验收 F20**（映射变更后全 feature 复核 0 阻断）；§8 补 P-047 复跑记录；§9 关闭 C-15/C-16 并登记新维护纪律（`CODE_WIKI §9` 行须与 feature 主 P 同步）。
> **v1.4 变更（P-047 收口修正批，用户指令「P-047 是否完全闭环 → 执行 A+B+C+D」）**: ① 新增 **F21**（§6 缺映射清单落地——修正 v1.3「声明未落地」）+ **F22**（兜底面归零 / 错值消解）；② §8 补收口批复跑 + **§8.2 独立 pass 记录**（同基座降级标注）；③ 三文档 status 升级（DESIGN / IMPLEMENTATION → `verified`，CHECKLIST → `accepted`）。
> **v1.5 变更（状态归属契约实施轮 · Layer-0，P-042 v1.8，用户指令「先按照结论顺序执行 符合完整spec工作流规范」；**零代码改动**）**: 新增功能验收 **F23**（`PLAN §1 DC2.1` 任务状态词表落档 + **轴正交**（不与 DC2 合轴）+ `PROGRESS` L3 声明**改指向 DC2.1**）/ **F24**（四取值**零改动** / I-7 词表对齐 / 同一位点**单来源**不双写）；§1 增一致性项（DESIGN **D16** → IMPLEMENTATION §7 零代码落地表可追溯 + D1-D16 逐条对应）；§8 补 v1.8 复跑记录（零代码：三校验器全绿 + selftest **37/37** + 门禁链）+ **§8.3 独立 pass 记录**（RULE-1 时序独立机械复核 / RULE-5 同基座降级标注）；§9 登记 **Layer-1（P2）边界**为后续行动。**被验收物**改为 DESIGN v1.5 + IMPLEMENTATION v1.5。
> **v1.6 变更（三项待裁决细化分析 + P0 批实施设计落档轮，P-042 v1.15，用户指令「待裁决项目细化分析 给出明确建议」→「请生成 P0 批的四文档实施设计草稿」→「先落档这一轮与上一轮结果」；**零代码改动**）**: 新增功能验收 **F25**（`pending` 且无 session → `tier=Recommended` fixture）/ **F26**（`pending` 且有 session，行为不变）/ **F27**（`done` 无 session 短路早退不变）/ **F28**（**门面回归**：`tier` 三处可见位点真机 CONSOLE 对照，A-54 / DR-22）/ **F29**（**幂等**：拆支后 I-3 保持）；§1 增一致性项（DESIGN **D17 → §5.2 → 本 CHECKLIST F25** 可追溯）；§8 补 **P-042 v1.15 复跑记录**（零代码：三校验器全绿 + selftest **37/37** + 门禁链）；§9 登记 **P0 批（V1a/V1a′/V2a/P2a）为后续行动**、**P2b 边界**顺延。**被验收物**改为 DESIGN **v1.6** + IMPLEMENTATION **v1.9**。
> **v1.7 变更（迭代调研回写机制评估 + DR-18 两条裁定回写轮 · 登记批，P-042 v1.16，用户裁决「落档『迭代调研回写机制』结论」「落档 DR-18 两条裁定」；**零代码改动**）**: 新增 §1 一致性项 **两条**（① **RESEARCH §7.19 / A-56 / B16 / C-27 四段可追溯**——登记项 ↔ 附录 A/B/C ↔ §0 计数；② **IMPLEMENTATION DR-18 正文与 C-25 一致**——触发条件① 语义已改写为「外部语境复现 ≥1 例（排除自指）」且方向 A 已标「即刻生效 + 作用域 5 视图载体」，**原文「留用户裁决」的悬置态已消除**）；§8 补 **P-042 v1.16 复跑记录**（零代码：三校验器全绿 + selftest **37/37** + 门禁链）；§9 登记 **§7.19 三处缺口（A 四元登记块 / B 多维度决策矩阵模板 / C 净收敛纪律 + Type-1/2 委派）为待裁决项**（**Layer-0、零代码、须用户裁决后另立批**）。**被验收物**改为 DESIGN **v1.6** + IMPLEMENTATION **v1.10**。

## 1. 文档一致性验收（Step 8）

- [x] DESIGN D1-D14 与 IMPLEMENTATION §2.3 判定落地表**逐条对应**（无「设计了未实现」项）
- [x] 不变式 I-1~I-10 全部有对应验收项（§4）
- [x] RESEARCH 裁定 C-5~C-8 → DESIGN §5-§6 → IMPLEMENTATION §2.3 三段可追溯（无断链）；**C-9/C-10/C-12 → DESIGN §6.2-§6.4 → IMPLEMENTATION §2.3 同样可追溯**
- [x] **C-13/C-14 → DESIGN §6.5/§6.6 → IMPLEMENTATION §2.3 同样可追溯**（含新不变式 **I-9** 的判据与实测）
- [x] **C-15/C-16 → DESIGN §6.7/§6.8 → IMPLEMENTATION §2.3 同样可追溯**（C-16 含新不变式 **I-10** 的判据与实测）
- [x] **C-11（映射空洞）显式登记为「不在本批」**（用户指定仅 C-9/C-10/C-12），缺口以 `—` 显式保留（I-8）
- [x] **C-15 / C-16 已在本批（P-047）执行完毕**——`—` 显式缺口保留（I-8）与「不改历史 PROGRESS 行」两项约束由 C-16 继承；DESIGN §9 边界条已同步更新
- [x] **收口批：C-16 ④「计入 §6 缺映射清单」已真正落地**（v1.3 时该句为**声明未落地**：实现只到 §2 的 `—`；收口批补 `_trace_section` 缺映射行，F21）
- [x] **收口批：§9 兜底面归零**（v1.3 仍有 2 feature 依赖 `PROGRESS` 兜底，其中 1 例实测错值 → 补 §9 两行后依赖兜底 0，F22）
- [x] 前身 [board-generator](../board-generator/DESIGN.md) 在 PROGRESS / CODE_WIKI 均登记为**前身**，无归属歧义
- [x] **DESIGN D1-D16 与 IMPLEMENTATION §7 判定/落地表逐条对应**（本批零代码——D16 落在 §7「本批（P-042 v1.8 / Layer-0）」条目，无「设计了未实现」项）
- [x] **C-20 → DESIGN §5.1 → IMPLEMENTATION §7 三段可追溯**（状态归属契约 Layer-0：真值源定义 / 值域分流 / 位点单来源）；D16 的**实现面**（派生状态机落地）显式登记为 **Layer-1 / P2**，不在本批
- [x] **DC2.1 与 DC2 轴正交**：任务状态词表作为**独立子块**承载（`PLAN §1` 新增 `DC2.1`），不与 DC2（type 主轴）合表——避免污染按轴分派的校验分支（DESIGN §8 方案 G 否决）
- [x] **`PROGRESS` L3 词表声明改指向 DC2.1**（单一权威）：原散落声明改为指针，四取值**零改动**（守 I-7 词表对齐）
- [x] **DESIGN D17 → §5.2 → 本 CHECKLIST F25~F28 三段可追溯**（P-042 v1.15 零代码：D17「未开工 vs 确无 session 判别」落在 DESIGN §5.2 判据表，本批**只落设计**、实施面 `derive_state` 拆支留 P0 批；F25 为唯一形态裁决 fixture，F28 为可见位点回归，DR-22 登记「验收不得只跑 `--selftest`」）
- [x] **RESEARCH §7.19 → 附录 A（A-56）/ 附录 B（B16）/ 附录 C（C-27）→ §0 计数 55A+15B+26C+5H → 56A+16B+27C+5H 四段一致**（P-042 v1.16 零代码：§7.19 为**评估登记项**，其**三处缺口实施面不在本批**；A-56 为 E1 组件在位盘点，B16 为可实现性推断，C-27 为三缺口与边界裁定）
- [x] **IMPLEMENTATION DR-18 正文与 RESEARCH C-25 一致**（P-042 v1.16 零代码：触发条件① 已改写为「**外部语境**复现 ≥1 例」并**显式排除自指**；方向 A 已标「**v1.13 起即刻生效、不等触发**」+ 作用域精确化为 **5 个视图载体**——**原文「该次是否计入「复现」留用户裁决」的悬置态已消除**）

## 2. 功能验收

| # | 验收项 | 实测 |
|---|--------|------|
| F1 | 生成器自测 **37/37** | ✅ `37/37 PASS`（S1-S37；P-043 16/16 → P-044 27/27 → P-046 34/34 → P-047 36/36 → 收口批 +1） |
| F2 | 词表对齐：输出含 PROGRESS 原词、**不含**升格标签 | ✅ selftest S2 |
| F3 | 三级行动队列 Needs Attention → Ready to Verify → Recommended | ✅ selftest S3 |
| F4 | feature 级制品链投影（R/D/I/C + 阶段） | ✅ selftest S4（**首轮拦截 DR-1 后修正**） |
| F5 | 活动区上限 7 + 超出折叠 | ✅ selftest S5 |
| F6 | 决策链 Mermaid（`stateDiagram-v2` 五步） | ✅ selftest S6 |
| F7 | 架构依赖图 Mermaid（`flowchart LR` + 仓内边） | ✅ selftest S7 |
| F8 | 动态 import 字面量补提取 | ✅ selftest S8 |
| F9 | hook 链解析（含 `pass_filenames`） | ✅ selftest S9 |
| F10 | 真实仓首次生成 `docs/CONSOLE.md` | ✅ 见 §6 |
| **F11** | **描述列三源优先链**（制品 H1 → P 行事项 → 目录名；**零视图层文本**） | ✅ selftest S17/S18/S19 |
| **F12** | **描述主名收敛与截断**（交替剥括号组 × `——`；`DESC_CAP`） | ✅ selftest S26/S27 + 真实仓 32 行描述无残留括号/断句（`independent-verify → 独立验证`） |
| **F13** | **per-feature 折叠 + 锚点目录 + 默认项目级在前** | ✅ selftest S20/S21/S25 + 真实仓 26 折叠块、折叠对 26:26 |
| **F14** | **架构图显式关系三口径**（hook→script / script→真值源 / import 有则绘）+ **排除 Mermaid `click`** | ✅ selftest S22/S23 + 真实仓 12 条显式关系边 |
| **F15** | **I-8 显式缺口清单**（未声明脚本 + 空 import 边如实标注） | ✅ selftest S24 + 真实仓 3 项（`deepeval_m7_eval` / `pf_m7_eval` / `spec_runner`） |
| **F16** | **hook 链列表块形态**（弃表格 + `name` 作用 + `pass_filenames` 三态 + **承载安全通则**） | ✅ selftest S28/S32 + 真实仓 **5 条列表块**（各带 `name`；4「否」+ 1「未设」）、**原 hook 表头消失**、全表 19 张 **0 列数不齐** |
| **F17** | **步骤级动态描述**（六列 / 多轮「最新一轮胜出」/ 修改历史全轮次 / 无 session 显式缺失） | ✅ selftest S29-S31/S33-S34 + 真实仓 **26 张步骤表 / 81 行**、多轮 2 例（`loop-engineering 3 轮` / `step-gate 2 轮`）、无 session 显式缺失 **9 处** |
| **F18** | **锚点双属性**（`<a name="feat-{f}" id="feat-{f}"></a>` 覆盖两类渲染器） | ✅ selftest S20（改断言）+ 真实仓 **26/26 双属性锚**（`<a name="feat-` 命中 26） |
| **F19** | **映射来源语义反转 + 唯一实现**（§9 行标注优先 → PROGRESS 兜底 → `—`；`spec_map` 共享模块，两处复用） | ✅ selftest S35（优先级/兜底/空表 + `feature_pid_map` 已不存在）/ S36（§9 补洞 P-009）+ **真实仓映射差异 13 项（4 空洞补齐 + 9 主 P 归位）**、缺映射 **0**（A-10） |
| **F20** | **门禁面复核**（映射语义变更对 `step-enforce` 只改 P 指向、不改规则；全 feature 0 新阻断） | ✅ 新语义 **32/32 exit 0**（逐 feature 模拟 hook 调用）；旧语义 **28/32 exit 0 + 4 feature 无映射**（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema` → hook exit 2，pre-commit 层为 de-facto 阻断）。**独立 pass 复核更正**：v1.3 记的「消除 `precommit-dc-validator`（P-008 无 session → exit 1）误阻断」**不可复现**（P-008 同为 P-020 前批次 → 历史豁免 → exit 0），见 §8.2（A-10 / A-11） |
| **F21** | **§6 缺映射清单**（I-8 显式缺口：有缺口列出 / 无缺口显式标无；D15） | ✅ selftest S37（双分支）+ 真实仓 §6 输出「**（无——32 个 feature 全部有映射）**」（A-11） |
| **F22** | **兜底面归零 + 错值消解**（32 feature 全部由 §9 人工标注覆盖；`cpp-hub-absorption` P-011 → P-002） | ✅ 依赖兜底 **2 → 0**；CONSOLE §2 该行关联 P 纠正为 P-002；门禁复跑 **32/32 exit 0**（A-11） |
| **F23** | **状态归属契约落档（Layer-0）**：`PLAN §1` 新增 `DC2.1 任务状态词表（+「来源」列）`（**与 DC2 轴正交**）+ `PROGRESS` L3 声明**改指向 DC2.1** | ✅ `PLAN §1` 新增 `DC2.1`（独立子块 + 轴正交声明 + 四行词表 + 位点单来源 + 轴正交消歧注）；`PROGRESS` L3 改为指向指针（四取值逐字保留） |
| **F24** | **四取值零改动 + 词表对齐 + 位点单来源**：`done` / `in-progress` / `blocked` / `pending` **取值不变**；「来源」列 = 执行态「机器派生」/ 决策态「人工」；同一位点不双写 | ✅ `DC2.1` 四取值与 `PROGRESS` L3 逐字一致（守 I-7）；「来源」列两档明确；`derive_state` 行为**零改动**（selftest 37/37 复跑一致） |
| **F25** | **`pending` 且无 session → `tier=Recommended`**（唯一设计点裁决，D17 / DESIGN §5.2）：拆支后该行 `tier` 由 `Needs Attention` 变 `Recommended`，**`state` 保持原词 `pending`** | ⏳ **设计已落**（D17 + §5.2 判据表）；**实施留 P0 批**（fixture 待建） |
| **F26** | **`pending` 且有 session**：走既有分支，`tier` = `Recommended`，行为与拆支前**一致**（回归不变量） | ⏳ 设计已落；实施留 P0 批 |
| **F27** | **`done` 无 session 短路早退不变**（A-55：存量 `done` 首分支短路 ⇒ 拆支影响面预期为零）：`if task.status == "done"` 优先于 `sess is None` 分支 | ⏳ 设计已落；实施留 P0 批（fixture 待建） |
| **F28** | **门面回归（`tier` 三处可见位点真机 CONSOLE 对照）**：① §状态表「行动档」列 ② 三级行动队列 ③ per-feature 折叠块——**单跑 `--selftest` 不可观测**该变更（A-54 / DR-22） | ⏳ 设计已落；实施留 P0 批（真机 CONSOLE 三处位点对照） |
| **F29** | **幂等（I-3）**：拆支后生成器双跑字节一致（首写 True / 二次 False）保持不变 | ⏳ 设计已落；实施留 P0 批 |

## 3. 接口验收

| # | 验收项 | 实测 |
|---|--------|------|
| I-1 | CLI 四模式齐备（`--stdout` / `--check` / `--stage` / `--selftest`） | ✅ selftest S14/S15 + hook 实测 |
| I-2 | 退出码语义：0 正常 / 1 过期 / 2 工具错误 | ✅ S15（0 与 1 双态）+ 顶层兜底分支 |
| I-3 | hook `console-gen` 与既有四 hook **语义不变**（仅 id/entry 更名） | ✅ §6 |

## 4. 不变式验收

| # | 不变式 | 验收方式 | 实测 |
|---|--------|---------|------|
| I-1 | 单写路径 | selftest S16（其余文件零变化） | ✅ |
| I-2 | 确定性（禁 wall clock） | selftest S10 + S13（双跑字节一致） | ✅ |
| I-3 | 幂等 | selftest S12（首写 True / 二次 False） | ✅ |
| I-4 | 零依赖（stdlib only） | 源码 `import` 清单核对（无第三方） | ✅ |
| I-5 | 纯派生 | `docs/CONSOLE.md` 可删可重生成；前身 `docs/BOARD.md` 移除即依此 | ✅ |
| I-6 | 不增真值 | 生成器不复制 M7 计数，只放指针（DR-3） | ✅ |
| I-7 | 词表对齐（P-043 新增） | selftest S2 断言「待你审」零出现 | ✅ |
| **I-8** | **显式缺口**（P-044 新增） | selftest S24（未声明脚本清单）；空 import 边如实标「（无）」；缺映射保留 `—` | ✅ |
| **I-9** | **承载安全**（P-046 新增） | selftest S32（竖线→全角 + 列数守恒）；真实仓全表扫描 **19 张 / 0 张列数不齐**；hook 正则已移出表格单元格 | ✅ |
| **I-10** | **语义同源**（P-047 新增） | selftest S35（本模块不再暴露 `feature_pid_map`）+ 源码核对（两处均 `import spec_map`，无本地实现残留）；映射优先级单测（§9 优先 / PROGRESS 兜底 / 皆无空表） | ✅ |

## 5. 错误处理验收（DESIGN §7）

- [x] `PROGRESS.md` 不可读 → `exit 2`（不当作「零任务」）
- [x] session 坏行 / 目录缺失 → 容错跳过
- [x] `.pre-commit-config.yaml` 缺失 → hook 段渲染「（不可读）」
- [x] `CODE_WIKI.md` 不可读 / 无 §9 节 → 映射退回「仅 PROGRESS 兜底」；缺位以 `—` 显式呈现（I-8，不静默补全）
- [x] git 不可用 → fork 段降级为空列表

## 6. 兼容性与归属迁移验收

| # | 验收项 | 实测 |
|---|--------|------|
| C1 | 前身脚本移除前**字节级备份一致** | ✅ `bak=16241` = `src=16241` |
| C2 | 前身两文件已从工作树与索引移除 | ✅ `git rm` 输出两行 `rm` |
| C3 | hook 更名且**计数不变** | ✅ 第五项 `console-gen`；hook 总数 5 |
| C4 | 三校验器全绿（含 `declared.scripts` 不因增删而失配） | ✅ 见 §8 |
| C5 | `step-enforce --pid P-043` 决策链通过 | ✅ 见 §8 |
| C6 | `verify-anchor` 锚点全真实 | ✅ 见 §8 |
| C7 | BOARD.md → CONSOLE.md 视图层同步（CODE_WIKI 四处 + PROGRESS） | ✅ 见 §8 |

## 7. ADD 审计（Step 10 前置）

| 维度 | 结论 |
|------|------|
| 过度设计 | 未发现——仍是**单产物 / 单 hook**；P-044 / P-046 增补均在既有 `render` 机制面内，P-047 唯一的文件面增量是 `scripts/spec_map.py`（**由 I-10 强制**：A-33 证伪「双实现 + 对账」后，唯一实现是成本最低的可行形态；30 行级纯函数、零依赖、零新采集面） |
| 设计漂移 | 未发现——DR-1~DR-14 均为设计内调整且已追记（DR-8/DR-9 为**首跑拦截**后实录；DR-11/DR-12 为形态与主源取舍；**DR-13/DR-14 为 P-047 的锚点形态与映射语义取舍**） |
| 死代码 | 前身脚本与产物已显式移除；`_dep_section` 被 `_arch_section` **取代**而非并存；hook **表格渲染已完全移除**（selftest S28 断言原表头不复存在）；**映射两处本地实现已删除**（selftest S35 断言 `feature_pid_map` 不存在，无双实现并存） |
| 第二真值源 | 未引入——§6 只放指针（I-6）；描述列**零视图层文本引用**（B6）；步骤表**以事件流为唯一主源**（DR-12）；**映射**改读 `CODE_WIKI §9`（见下行） |
| **视图依赖视图（P-047 新引入的张力，已明示）** | **C-16 让「映射」读 `CODE_WIKI §9`**——这与 B6/C-9「描述列不引 §9 以避免视图依赖视图」**方向相反**，属**有意为之**：① §9 是**人工维护的关系索引**（非叙事文本），A-34 实测其对 4 个空洞**全部正确**；② 描述是**内容**（可歧义、可膨胀），映射是**关系指针**（可机械抽取首个 `P-\d{3}`）；③ 代价已登记：`§9` 行须与 feature 主 P 同步维护（漂移由 I-8 缺口清单兜底，见 §9 后续行动） |
| 新增契约面 | `DECLARED_SOURCES` 属**架构契约声明**（非业务真值）：Layer-0 文档化于 DESIGN §6.4 / §3.1、只对实际存在的脚本绘边、漂移由「未声明关系」清单兜底（I-8）；P-047 新增 `spec_map → PROGRESS + CODE_WIKI §9` 一条同性质声明 |

## 8. 验收结论与复跑记录

**P-042 v1.16 复跑（2026-09-30，本机实测；迭代回写评估 + DR-18 裁定回写轮，零代码）**:

| 命令 / 核对 | 结果 |
|------|------|
| `python scripts/dc_validator.py` | **0 违规（127 文件）**——RESEARCH §0 声明 **56A / 16B / 27C / 5H**、本 IMPLEMENTATION §0 声明 **14A / 6B / 0C / 0H** 均与机械重数一致 |
| `python scripts/m7_stats.py` | **0 违规**（P3 提示 1——样本③ 历史形态 by-design，**禁止回改**） |
| `python scripts/repo_stats.py` | **0 违规、P3 0** |
| `python scripts/console_gen.py --selftest` | **37/37 PASS**（零代码复跑一致） |
| `spec_runner step-gate --session specwf-p042-20260930v3 --expect research design implement verify finalize` | **决策链一致 pass → exit 0**（5/5 步） |
| `spec_runner verify-anchor --session specwf-p042-20260930v3` | 锚点全真实 → **exit 0** |
| `spec_runner step-enforce --pid P-042` | **exit 0**（session 定位 `specwf-p042-20260930v3`，5/5 步） |
| 代码面核对（零代码声明） | `scripts/` / `.pre-commit-config.yaml` 零变更；`docs/CONSOLE.md` 因**新增 session** 由 hook 重生成（步骤表更新，属预期） |

**P-042 v1.15 复跑（2026-09-30，本机实测；P0 批实施设计落档轮，零代码）**:

| 命令 / 核对 | 结果 |
|------|------|
| `python scripts/dc_validator.py` | **0 违规（127 文件）**——本 IMPLEMENTATION §0 声明 **14A / 6B / 0C / 0H** 与机械重数一致 |
| `python scripts/m7_stats.py` | **0 违规**（P3 提示 1——发现列非标准形态，样本③ 历史形态 by-design，**禁止回改**） |
| `python scripts/repo_stats.py` | **0 违规、P3 0** |
| `python scripts/console_gen.py --selftest` | **37/37 PASS**（**零改动复跑一致**——本批零代码，`derive_state` 行为与 P-047 收口批完全相同；F25~F29 为**设计面验收项**，实施留 P0 批） |
| `spec_runner step-gate --session specwf-p042-20260930v2 --expect research design implement verify finalize` | **决策链一致 pass → exit 0**（5/5 步） |
| `spec_runner verify-anchor --session specwf-p042-20260930v2` | 锚点全真实 → **exit 0** |
| `spec_runner step-enforce --pid P-042` | **exit 0**（session 定位 `specwf-p042-20260930v2`，5/5 步） |
| 代码面核对（零代码声明） | `git status` 无 `scripts/` / `.pre-commit-config.yaml` 变更 ⇒ `declared.scripts` 不变；`docs/CONSOLE.md` 未重生成 |

**P-042 v1.8 复跑（2026-09-29，本机实测；Layer-0 契约批，零代码）**:

| 命令 / 核对 | 结果 |
|------|------|
| `python scripts/dc_validator.py` | **0 违规（127 文件）**——本 IMPLEMENTATION §0 声明 **12A / 6B / 0C / 0H** 与机械重数一致 |
| `python scripts/m7_stats.py` | **0 违规**（P3 提示 1——发现列非标准形态，样本③ 历史形态 by-design，**禁止回改**） |
| `python scripts/repo_stats.py` | **首跑 2 P2**（drift-gate 激活：`CODE_WIKI §9` 的 `doc-contract` / `project-console` 版本令牌 v1.7 ≠ front-matter 1.8）→ §2.1 树 + §9 四处同步后 **0 违规、P3 0** |
| `python scripts/console_gen.py --selftest` | **37/37 PASS**（**零改动复跑一致**——本批零代码，`derive_state` 行为与 P-047 收口批完全相同） |
| `spec_runner step-gate --session specwf-p042-20260929v4 --expect research design implement verify finalize` | **决策链一致 pass → exit 0**（5/5 步） |
| `spec_runner verify-anchor --session specwf-p042-20260929v4` | **锚点 9 真实 / 0 硬性 / 0 软性 → exit 0** |
| `spec_runner step-enforce --pid P-042` | **exit 0**（session 定位 `specwf-p042-20260929v4`，5/5 步） |
| 代码面核对（零代码声明） | `git status` 无 `scripts/` / `.pre-commit-config.yaml` 变更 ⇒ `declared.scripts` 不变；`docs/CONSOLE.md` 未重生成 |

**P-047 复跑（2026-09-11，本机实测）**:

| 命令 / 核对 | 结果 |
|------|------|
| `python scripts/console_gen.py --selftest` | **36/36 PASS**（S1-S36；P-046 34/34 → P-047 +2） |
| **源码核对（I-10 语义同源）** | `scripts/console_gen.py` / `scripts/step_enforce.py` 两处均 `import spec_map`；**本地映射实现已删除**（`console_gen` 的 `feature_pid_map` / `P_IMPL_RE` / `step_enforce` 的 `P_ROW_RE`）；`step_enforce.build_feature_pid_map` 保留为 **hook 入口薄委托**（2 行转调，非第二实现；selftest S35 另断言 `console_gen` 模块不再暴露 `feature_pid_map`） |
| **映射语义比对（逐 feature）** | v1.3 首轮 **13 项差异** = 4 空洞补齐（→P-016 / P-011 / P-010 / P-009）+ 9 主 P 归位；**收口批后 14 项**（+`cpp-hub-absorption` P-011 → P-002 错值消解）；真实 feature **缺映射 0**（`spec/templates/` 非 feature） |
| **门禁全 feature 复核** | 新语义 **32/32 exit 0**；旧语义 **28/32 exit 0 + 4 feature 无映射**（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema` → hook exit 2，pre-commit 层 de-facto 阻断）。**独立 pass 复核更正**：v1.3 记的「`precommit-dc-validator` P-008 无 session → exit 1 误阻断」**不可复现**（P-008 亦 < P-020 → 历史豁免 → exit 0，§8.2） |
| `python scripts/dc_validator.py` | 0 违规（114 文件；本 IMPLEMENTATION §0 声明 **10A / 4B / 0C / 0H** 与机械重数一致） |
| `python scripts/m7_stats.py` | 0 违规（P3 提示 1——发现列非标准形态） |
| `python scripts/repo_stats.py` | 0 违规（P3 提示 8——README / README.en / evidence.svg 快照滞后，择机刷新）；`declared.scripts` **7 → 8** 同批同步 |
| `spec_runner step-enforce --pid P-047` | 五步链 exit 0（5/5 步，硬性 0 / 软性 0） |
| `spec_runner verify-anchor --session specwf-p047-20260911` | **10 锚点全真实** / 0 硬性 / 0 软性 |
| `python scripts/console_gen.py` | `docs/CONSOLE.md` 已刷新（**722 行 / 44526 B**；P-046 为 729 行 / 45709 B） |
| 产物结构核对 | **双属性锚 26/26**（`<a name="feat-` 命中 26）；折叠块 26（26:26）；**步骤表 69 行**（映射归位后由 81 降）；**import 边非空**（`console_gen` → `spec_map`；`step_enforce` → `spec_map`）；「未声明关系的脚本」仍 3 项；全表 **0 列数不齐**（I-9） |

**P-046 复跑（2026-09-11，本机实测）**:

| 命令 | 结果 |
|------|------|
| `python scripts/console_gen.py --selftest` | **34/34 PASS**（S1-S34；P-044 27/27 → P-046 +7） |
| `python scripts/dc_validator.py` | 0 违规（114 文件；本 IMPLEMENTATION §0 声明 **8A / 3B / 0C / 0H** 与机械重数一致） |
| `python scripts/m7_stats.py` | 0 违规（P3 提示 1——发现列非标准形态，历史形态如实容纳） |
| `python scripts/repo_stats.py` | 0 违规（P3 提示 8——README / README.en / evidence.svg 快照滞后，择机刷新） |
| `spec_runner step-enforce --pid P-046` | 五步链 exit 0（5/5 步）。**首跑 soft=1**：seq5 锚点 `CODE_WIKI.md §9` 不满足 `ANCHOR_RE` 的路径前缀要求（须 `spec|adr|docs|tools|scripts` + `/`）→ 改用 `spec/project-console/DESIGN.md §9` 后 exit 0（软性规则按设计语义起效：自报锚点须形态可解析） |
| `spec_runner verify-anchor --session specwf-p046-20260911` | **10 锚点全真实** / 0 硬性 / 0 软性 |
| `python scripts/console_gen.py` | `docs/CONSOLE.md` 已刷新（**729 行 / 45709 B**） |
| 产物结构核对 + **I-9 机械核对** | hook 链 **5 条列表块**（各带 `name`；4「否」+ 1「未设」）；**原 hook 表头消失**；折叠块 **26**（`<details>`:`</details>` = 26:26）；锚点 26；**步骤表 26 张 / 81 行**；多轮进摘要 2 例（`loop-engineering 3 轮` / `step-gate 2 轮`）；无 session 显式缺失 9 处；**全表扫描 19 张 / 0 张列数不齐** |

**P-044 复跑（2026-09-11，本机实测）**:

| 命令 | 结果 |
|------|------|
| `python scripts/console_gen.py --selftest` | **27/27 PASS**（S1-S27） |
| `python scripts/dc_validator.py` | 0 违规（114 文件；本 IMPLEMENTATION §0 声明 **6A / 2B / 0C / 0H** 与机械重数一致） |
| `python scripts/m7_stats.py` | 0 违规 |
| `python scripts/repo_stats.py` | **首跑 3 违规**（P1 ×1 + P2 ×2 = `declared.progress_tasks` 与 PT-11 两处命中值停旧 43）→ 随 CODE_WIKI v1.46 同步后 **0 违规** |
| `spec_runner step-enforce --pid P-044` | 五步链 exit 0（5/5 步） |
| `spec_runner verify-anchor --session specwf-p044-20260911` | **11 锚点全真实** / 0 硬性 / 0 软性 |
| `python scripts/console_gen.py` | `docs/CONSOLE.md` 已刷新（**514 行 / 20027 B**） |
| 产物结构核对 | 描述列 32/32 非空；per-feature 折叠块 26 个；折叠对 **26 : 26**；§5 mermaid 显式关系边 12 条；未声明脚本 3 项 |

**P-043 复跑（2026-09-11，本机实测，历史留档）**:

| 命令 | 结果 |
|------|------|
| `python scripts/console_gen.py --selftest` | **16/16 PASS** |
| `python scripts/dc_validator.py` | 0 违规（**首跑拦截 7 项** = 迁移连锁：悬空链接 ×6 + 本 IMPLEMENTATION §0 计数组成项 ×1；均同批修正） |
| `python scripts/m7_stats.py` / `repo_stats.py` | 0 违规 |
| `spec_runner step-enforce --pid P-043` | 五步链 exit 0 |
| `spec_runner verify-anchor --session specwf-p043-20260911` | 锚点全真实 |

**§8.2 独立 pass 记录（Step 10，RULE-1 时序独立机械复核；RULE-5 同基座降级标注）**:

- **执行时点 / 基座**：2026-09-11（生成端之后 → RULE-1 **时序独立**满足）；**基座 = 本机 + 同一 agent 实例**——非真异基座（本机无第二可用模型/端点，同 P-014 / P-016 先例），故按 **RULE-5 降级标注**：结论为「同基座机械复核」，**不主张**模型异质性。
- **审查输入**：事件流 `specwf-p047-20260911` + `verify-anchor` 输出 + `git status`（+ 源码与产物）。
- **复核项与读数**：
  1. 锚点可达性：`spec_runner verify-anchor --session specwf-p047-20260911` → **10 锚点全真实 / 0 硬性 / 0 软性**（复跑一致）。
  2. 决策链：`spec_runner step-enforce --pid P-047` → **exit 0**（5/5 步）。
  3. **映射面重算（独立枚举，非复用 `spec_map` 结果）**：逐 feature 比对 §9 标注 / `PROGRESS` 兜底两源 → **映射差异 14 项**（4 空洞补齐 + 10 主 P 归位，含 `cpp-hub-absorption` P-011 → P-002）；**未映射仅 `spec/templates/`（非 feature）**；**依赖兜底 0**。
  4. **门禁面重跑（逐 feature 模拟 hook 调用）**：新语义 **32/32 exit 0**；旧语义 **28/32 exit 0 + 4 feature exit 2**（`spec-runner` / `promptfoo-m7-eval` / `m7-hits-block` / `decision-schema`）。
  5. 产物一致性：`console_gen --check` → **exit 0**；`docs/CONSOLE.md` **723 行 / 44588 B**；§2 `cpp-hub-absorption` 行关联 P = **P-002**；§6 缺映射行 = 「（无——32 个 feature 全部有映射）」。
  6. 三校验器复跑：dc_validator **0 违规**（114 文件）/ m7_stats **0 违规** / repo_stats **0 违规**。
- **独立 pass 捕获（2 P3，均同轮修正）**：
  - **P3-1（事实错误）**：v1.3 记述「消除一处既有误阻断：旧语义 `precommit-dc-validator` P-008 无 session → exit 1」**不可复现**——`P-008` 与 `P-007` 同为 P-020 前批次，`step_enforce` 的 `int(pid.split("-")[1]) < 20` 历史豁免对两者**均**生效 → **hook 层 exit 0**（实测输出「为 P-020 前历史批次 → 豁免」）；该记述把 `spec_runner step-enforce --pid P-008` 的 **runner 层** exit 1 误读为 **hook 层**阻断。**修正**：A-10 / §4 / §7 / B4 / F20 / §8 同轮改写为「旧语义实际消解的是 4 个无映射 feature 的 exit 2」。
  - **P3-2（计数漂移）**：映射差异计数在**收口批后应为 14 项**（v1.3 首轮 13 项 + `cpp-hub-absorption` 错值消解 1 项），而 v1.3/v1.4 多处仍记 13。**修正**：A-10 / A-11 / DESIGN §6.8 / F19 / §8 同轮补注「v1.3 = 13、收口批后 = 14」。
- **结论**：**通过（同基座降级）**——位置可达、计数一致、门禁 0 新阻断；两处 v1.3 记述经复核更正后与机械读数一致。

**§8.3 独立 pass 记录（P-042 v1.8，Step 10，RULE-1 时序独立机械复核；RULE-5 同基座降级标注）**:

- **执行时点 / 基座**：2026-09-29（生成端之后 → RULE-1 **时序独立**满足）；**基座 = 本机 + 同一 agent 实例**——非真异基座（本机无第二可用模型/端点，同 P-014 / P-016 / P-047 §8.2 先例），故按 **RULE-5 降级标注**：结论为「同基座机械复核」，**不主张**模型异质性。
- **审查输入**：事件流 `specwf-p042-20260929v4` + 四文档（RESEARCH v1.8 / DESIGN v1.5 / IMPLEMENTATION v1.5 / CHECKLIST v1.5）+ `PLAN §1 DC2.1` + `PROGRESS` L3 + `git status`。
- **复核项与读数（独立重算，不复用生成端结论）**：
  1. **重数再推导**（独立临时脚本，非复用 `dc_validator` 内建 grep）：RESEARCH **A=47 / B=10 / H=5**、IMPLEMENTATION **A=12 / B=6 / H=0**——与本 CHECKLIST §8 与 IMPLEMENTATION §0 声明**全等**。
  2. 锚点可达性：`spec_runner verify-anchor --session specwf-p042-20260929v4` → **9 锚点全真实 / 0 硬性 / 0 软性**（复跑一致）。
  3. 决策链：`spec_runner step-enforce --pid P-042` → **exit 0**（session 定位 v4 / 5/5 步）；`step-gate --session …v4` → **决策链一致 pass → exit 0**。
  4. 三校验器复跑：dc_validator **0 违规（127 文件）** / m7_stats **0 违规**（P3 提示 1 = 样本③ 历史形态 by-design） / repo_stats **0 违规（P3 0）**。
  5. 制品一致性：`console_gen --selftest` → **37/37 PASS**；`git status` 无 `scripts/` / `.pre-commit-config.yaml` 变更 ⇒ **零代码声明成立**（`derive_state` 行为与 P-047 收口批完全相同）。
  6. **全覆盖陈旧 token 扫描（不得抽样）**：`45A+9B+18C` / `45A+9B+19C` / `RESEARCH v1.7` / `PLAN v1.7` 全仓 grep——命中**全为可解释项**：① **版本跃迁描述**（`CODE_WIKI` banner「v1.7→v1.8」+ §2.1 树/§9 的 v1.6/v1.7 **历史批次快照**；`PROGRESS` L51 P-042 行版本链；session 事件流描述）；② **异 feature 同名**（`rework-and-decision-paths` 自身 RESEARCH v1.7、其 CHECKLIST 的 M7 样本 ㊲ 记述、`M7_EVIDENCE_LOG.md` 历史样本行）——**零真残留**，无 `PLAN v1.7` 命中。
- **独立 pass 捕获**：**0 新问题**（对照 P-047 §8.2 捕获 2 P3 不同，本批为纯契约零代码批，改动面仅文档 front-matter + 新增子块 + 视图层版本令牌）。
- **结论**：**通过（同基座降级）**——重数自洽、锚点全真实、门禁全 exit 0、零代码声明经制品核对成立、陈旧 token 零真残留。

## 9. 后续行动

- **§7.19 迭代调研回写机制三处缺口——待裁决项（Layer-0、零代码、本批只登记，P-042 v1.16）**：**判定 = 机制可实现且本仓已在运行**（§7.14~§7.18 连续五轮即活实例）。**三处缺口** = **A** 未决项未一等公民化（建议**四元登记块**：判据 / 触发条件 / 当前倾向 / 证据等级）/ **B** 无**多维度决策矩阵模板**（维度 = 成本·收益·可维护性·兼容·升级潜力·短期·长期；每格附**证据等级 + 读数日期**；格内含计数须 = 机械重数 ⇒ **R7 同构**）——**此件直击「避免随机选择」** / **C** 无**迭代收敛停止规则**（**净收敛纪律** + **Type-1/2 委派**）。**硬边界** = 三件全落 Layer-0、**零 Layer-1 位点 / 不加门禁**，且**可机械化仅「格齐全 / 证据等级非空 / 触发条件存在 / 引用完整」，绝不核结论正确性**（否则重犯 A-33 / DR-21 之病）。**实施须用户裁决后另立批**（可三件合批，或**仅取 B 单件**先试）。
- **P0 批（V1a / V1a′ / V2a / P2a）——本批只落设计、实施留 P0 批（P-042 v1.15）**：本批（v1.15）**只落四文档实施设计**（RESEARCH §7.18【二】/ DESIGN D17 + §5.2 / IMPLEMENTATION DR-22 / 本 CHECKLIST F25~F29），**零代码 / 不补建 session / 不落 P0 实施**。P0 批四件 = ① **V2a** 补建 4 条 session（P-048 / P-053 / P-054 / P-055）② **V1a** 立项即登记纪律 ③ **V1a′** 过渡期判据三件 ④ **P2a** `derive_state` 拆支（`pending` 无 session → `Recommended`；属**可见行为变更**，验收须含 F28 真机位点对照，见 DR-22）。**批内执行顺序与验证命令**见 RESEARCH §7.18【二】。
- **P2 拆分（C-23 / C-24）**：P2 拆为 **P2a**（改 `basis` / `tier`，即 `derive_state` 拆支，已并入 P0 批）与 **P2b**（**状态来源迁移 + 载体迁移 + I-7 扩写**，属 Layer-1 高风险）。**P2b 边界顺延**——其前置 = P0 批完成（V2a 补齐决策链 + P2a 生效）；**P2b 设计批（P1）**须先落「完整迁移计划」（Usage Inventory / 依赖矩阵 / 批次表，留作 P1 的 RESEARCH 输入）。
- **Layer-1（P2b）边界——状态归属契约的派生端实现（本批外置，P-042 v1.8）**：本批**只定义契约**（真值源归属 / 「来源」列 / 位点单来源），**不含任何派生端实现**。Layer-1 三件 = ① `console_gen.derive_state` **第一参改取派生值**（现直取 `PROGRESS` 状态列）；② `PROGRESS` **执行态位点迁往派生面**（事件流 step 序表 ∪ feature 四文档 front-matter），**决策态位点留人工面**；③ 须**先修订 `console_gen` 不变式 I-7**（词表对齐）并经 **ADR-0010 三问** + **设可回退点**。**风险面 = 高**（触及真值源与单写路径 I-1）；**触发** = 用户裁决 / 需求激活；**不由本批启动**。
- **H6（描述列单行长度上限）部分回填（P-044 / P-046 / P-047 三次）**：P-044 取设计时值 `DESC_CAP = 40`，真实仓 32 行描述**无一触顶**；P-046 新增步骤表，主题 / 简要描述取 `STEP_CAP = 48`（扫描性阈值），真实仓步骤表**未见触顶报告**（P-046 时 81 行 / P-047 归位后 69 行）——「渲染宽度校准」仍**待真机渲染实测**（本机无法验证宿主渲染宽度）。
- **H7（per-feature 折叠块体积预算）四度回填**：P-044 **514 行 / 20027 B**（折叠块 26 个）→ P-046 **729 行 / 45709 B**（+ 步骤表 81 行）→ P-047 **722 行 / 44526 B**（映射归位后步骤表降至 69 行，体积**略降**）→ **收口批 723 行 / 44588 B**（§6 增缺映射行 +1 行）——体积始终在展开面内；「26 个折叠块 × 六列步骤表是否仍属认知负载内」仍需真机浏览体验确认（A-45：折叠块**无数量上限**，属认知负载而非技术限制）。
- **H8（锚点真机存活率）仍待验，但风险面已收窄**：C-15 已把锚点改为**双属性** `<a name="feat-{f}" id="feat-{f}"></a>`（覆盖「只认 name」与「只认 id」两类渲染器）；**残余风险仅剩「两者皆被剥离」** → 退化为「可折叠不可跳转」（默认视图与折叠功能不受影响）。真机存活率**本机不可验**（需远端/宿主渲染），登记为待触发项。
- **新增维护纪律（P-047 引入，须随批次执行）**：`CODE_WIKI §9` 行**自此承担映射权威**（C-16）——新建 feature 或批次更替主 P 时，须同步维护该行标注（首个 `P-\d{3}` 即该 feature 的**主 P**）；若缺标注则自动退回 `PROGRESS` 兜底源，若两源皆缺则以 `—` **显式缺口**呈现（I-8 兜底，非静默）。
- **语义变更的观察项**：关联 P 由「末批 P」改为「§9 主 P」后，控制台显示的是 **feature 主 P** 而非最新触碰批次（例：project-console 显示 P-042 而非 P-047）。若后续认为「视图应显示最新批次 P」，则需**再裁决一次语义**（并同步 `spec_map` 与 §9 行维护方式）——本批不改（遵从 C-16）。
- **C-11 / C-15 / C-16 状态**：**全部关闭**——C-11 ① （`—` 显式缺口）由 C-16 继承强化；C-16 已执行（缺口 **4 → 0**、单一实现 `spec_map`、两处复用）；C-15 已执行（双属性锚）。
- **`DECLARED_SOURCES` 契约维护**：新增脚本须同批登记（本批已登记 `spec_map → PROGRESS + CODE_WIKI §9`），否则进入「未声明关系」清单（I-8 已兜底，非静默）。
- **独立 pass 已执行（2026-09-11，见 §8.2）**：RULE-1 **时序独立**满足、**RULE-5 同基座降级标注**（本机无第二基座）。捕获 **2 P3**（① v1.3「消除 `precommit-dc-validator` 误阻断」**不可复现**——P-008 同为 P-020 前批次 → 豁免 exit 0；② 映射差异计数漂移 **13 → 14**），均**同轮修正**（A-10 / §4 / §7 / B4 / F20 / §8）。
- **收口批新增教训（B5）**：「缺口数归零」类判据**必要不充分**——只覆盖**缺值**（`None`）、不覆盖**错值**（有值却指向错误对象）。凡「收敛到唯一来源」改造，验收须并核**来源分布**（仍依赖兜底/次级来源的对象数），而非只看缺口计数。
- **C-16 ④ 落地确认**：§6 缺映射清单已**真正落地**（收口批 F21，真实仓输出「（无——32 个 feature 全部有映射）」）；`—` 显式缺口保留策略不变。

---

**验收签字**: 自查（`console_gen --selftest` **37/37** / 三校验器 **0 违规** / 门禁新语义 **32/32 exit 0** / `step-enforce --pid P-047` exit 0 / `verify-anchor` **10 锚点全真实**）· **独立 pass 已执行（同基座降级，§8.2）** 日期: 2026-09-11
**验收签字（P-042 v1.8 / Layer-0 契约批，**零代码**）**: 自查（`console_gen --selftest` **37/37**（零改动复跑）/ 三校验器 **0 违规**（dc 127 文件 / m7 1 条 by-design P3 / repo P3 0）/ `step-enforce --pid P-042` **exit 0**（5/5 步）/ `verify-anchor --session specwf-p042-20260929v4` **9 锚点全真实**）· **独立 pass 已执行（同基座降级，§8.3）** 日期: 2026-09-29
**验收签字（P-042 v1.15 / P0 批实施设计落档轮，**零代码**）**: 自查（`console_gen --selftest` **37/37**（零改动复跑）/ 三校验器 **0 违规**（dc 127 文件 / m7 1 条 by-design P3 / repo P3 0）/ `step-enforce --pid P-042` **exit 0**（5/5 步，session `specwf-p042-20260930v2`）/ `verify-anchor --session specwf-p042-20260930v2` 锚点全真实）；**F25~F29 为设计面验收项，实施留 P0 批**） 日期: 2026-09-30
