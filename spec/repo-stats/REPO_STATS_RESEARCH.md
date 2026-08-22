# 调研文档：repo_stats 视图层机械枚举校验器

---
id: repo-stats-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-08-22
depends: [SPEC-PROCESS, ADR-0007, precommit-dc-validator-DESIGN, m7-hits-block-DESIGN]
upstream: null
---

> **Feature**: repo-stats（PROGRESS P-014，[DIS-010](../../docs/discoveries/README.md) 处置落地）
> **创建日期**: 2026-08-22
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: [DIS-010](../../docs/discoveries/README.md)（八度实证——视图层 33 处占形态 II 总量 62%，四连残留链 ⑰→⑱→⑲→⑳）+ [PROGRESS P-014](../../docs/PROGRESS.md)
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 15 | 每条附仓库内 E1 取证（文件 + 行号 + 可 grep 引文），2026-08-22 Read/Grep/LS 取证 |
| B 推断类 | 1 | B1，登记于附录 B |
| C 判断类 | 3 | §4.2 决策判断 |
| 假设区 | 3 | H1-H3，未取证声明 |

**扫描范围声明**: 本调研为仓库内部调研（无外部文献需求）——覆盖 CODE_WIKI.md 全部数字位点、README.md/README.en.md 快照段、evidence.svg、discoveries/README.md、M7_EVIDENCE_LOG.md（样本表 + 分桶表 + hits 块）、scripts/m7_stats.py 与 dc_validator.py 头部契约、.pre-commit-config.yaml、PROGRESS、spec/ 与 adr/ 与 docs/dev-log/ 目录实态。未覆盖：m7_stats.py 全文逐行（仅取证头部契约与 hook 行为，属 Step 9-10 范围）、CODE_WIKI §3-§6 段落级 prose（本轮盘点以枚举位点为对象，自由叙述段不含可机械重数的实体计数）。

## 1. 调研目标

**核心问题**:
1. 视图层（CODE_WIKI/README/SVG/discoveries 索引）的枚举位点全景是什么？每个位点的真值源在哪？（枚举面盘点 + 真值源分类）
2. 为什么双校验器（dc_validator + m7_stats）没有拦截 DIS-010 的八度实证？工具的覆盖盲区边界在哪？（失效分析）
3. repo_stats 与 m7_stats 的本质区别是什么——视图位点为什么不能"重生成"只能"对账"？（拦截模型）
4. 门面层（README/SVG）采用"时点快照+真值指针"模式不追实时同步，机械校验对它的边界在哪？（豁免契约）

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| Read | CODE_WIKI / README 双语 / evidence.svg / discoveries/README / M7 hits 块 / .pre-commit-config.yaml 逐行取证 | 逐文件 |
| Grep | 视图载体数字位点模式扫描（`形态 II (27\|29\|34\|45) 处` / `样本①-⑮` / `DIS-007~009` 等）——本轮即"模式扫描制"原型执行 | 全仓 |
| LS | spec/ adr/ docs/dev-log/ scripts/ 文件系统真值枚举 | 四目录 |
| 机械重数 | 视图层分桶行求和 / hits 块字段核对 | 人工枚举（Step 9 由脚本接管） |

### 2.2 调研范围

- **范围**: 仓库内部（视图层四载体 + 真值源三类 + 双校验器先例 + M7 八度实证链）
- **排除**: 外部文献（本 feature 无技术选型不确定性——工具形态已被 P-007/P-011 双先例完全定型）

## 3. 调研发现

### 3.1 视图层枚举面盘点（位点全景）

【A】A1: CODE_WIKI 单文件含 M7 统计的 4 个副本位点——同源数字多处并存是六连击的结构基础

- **取证**: [CODE_WIKI.md](../../CODE_WIKI.md) L3（版本头「M7 样本①-⑲（形态 II 分桶 45 处——样本⑭⑮ 非形态 II）」）、L66（§2.1 目录树「样本①-⑳ + §5 hits 机读块，形态 II 53 处」）、L576（§7 教训表「M7 样本①-⑳，53 处」）、L628（§9 索引「样本①-⑳ + 形态 II 复发分桶（53 处/7 字段类型）」）——同文件的 4 处独立转抄（可 grep: `形态 II`）
- **关键结论**: M7 统计在 CODE_WIKI 内天然 4 副本（版本头/目录树/教训表/索引），修正轮凭记忆选点必漏（样本⑲② L576·L628 残留实证）——位点清单不可枚举穷举是结构性困难，**模式扫描（扫全部「形态 II N 处」模式）优于位点登记**。

【A】A2: CODE_WIKI 覆盖对象行（L4）单行含 8 类实体枚举——每类都是独立漂移面

- **取证**: CODE_WIKI L4 引文（可 grep: `覆盖对象`）: `宪法 SPEC_PROCESS v1.4、ADR-0004~0009 六份、Discovery 007 v1.3 + DIS-007~010、断言证据框架 v1.4.2 + 事实核查框架 v1.0、5 个模板（四件套 + ADR）、M7 证据账本（含 §5 hits 机读块）、discoveries 索引、PROGRESS、dev-log ×5、spec/ 九 feature 目录、scripts/dc_validator.py + scripts/m7_stats.py + .pre-commit-config.yaml 双 hook`
- **关键结论**: 8 类实体计数（SPEC_PROCESS 版本 / ADR 份数 / DIS 范围 / 框架版本 / 模板数 / dev-log 数 / feature 目录数 / 脚本与 hook 数）单行密集并存；本轮 P-014 登记瞬间「九 feature 目录」即变「十」（repo-stats 目录建立），L67 PROGRESS 行「P-001~P-013」同步过期——**视图陈旧不需要任何错误动作，真值源前进即触发**。

【A】A3: §2.1 目录树与 §9 索引区是"实体清单"位点（非单数字）——完整性不可用计数表达

- **取证**: CODE_WIKI L50-L85（目录树：spec/ 下列 templates + 9 feature 目录，与 LS 实态全等）；L617-L634（§9 索引区：每文档一行，含版本号/状态字段）
- **关键结论**: 目录树与索引区的漂移形态是**条目缺失**（样本⑰② 目录树漏登两目录、样本⑱⑤ feature 索引缺 5 目录）而非数字错——机械校验须做**清单比对**（视图枚举集 vs 文件系统枚举集）而非仅计数对账。

【A】A4: README 双语与 evidence.svg 为门面快照位点——已带时点标注与真值指针

- **取证**: [README.md](../../README.md) L43: `截至 2026-08-22：样本 ①-⑳...登记形态 II 复发 53 处...本段数字为时点快照，累积真值以 M7 账本为准`；[evidence.svg](../../docs/assets/readme/evidence.svg) L12/L18（大数字 20/53）+ L31（`数字为 2026-08-22 时点快照 · 累积真值以 M7 证据账本为准`）
- **关键结论**: 门面层已落地「时点快照+真值指针」标注模式（DIS-010 处置裁决）；快照的合法性与"写入值为当时真值"绑定（⑲轮假值 27 实证：真值序列 21→22→29→34→45→53 从无 27）。

【A】A5: DIS-010 条目自身含派生统计位点——登记漂移的 DIS 条目内嵌漂移计数

- **取证**: [discoveries/README.md](../../docs/discoveries/README.md) DIS-010 行: `视图层合计 33 处占形态 II 总量 62%`（可 grep: `视图层合计`）——该值为 M7 分桶表六行求和的派生统计，随每轮样本登记漂移（⑲轮曾手算 15 处/44% 为错值，样本⑲④）
- **关键结论**: 派生统计位点的真值 = M7 分桶表计算结果，口径必须显式声明（六行宽口径 vs CODE_WIKI/README/SVG 严格口径），否则"机械重数"自身无确定基准。

### 3.2 真值源分类

【A】A6: 真值源一类——文件系统枚举（LS 即真值，零解析成本）

- **取证**: LS 实态（2026-08-22）: `spec/` = templates + 9 feature 目录（adr0006-pointer / cpp-hub-absorption / cpp-hub-gap-analysis / deepseek-harness / doc-contract / langgraph-upgrade / m7-hits-block / precommit-dc-validator / skill-enhancement）；`adr/` = 6 份（ADR-0004~0009）；`docs/dev-log/` = 5 份（DEV-LOG-001~005）；`scripts/` = 2 个（dc_validator.py / m7_stats.py）
- **关键结论**: 四组实体计数真值 = 目录列表长度，枚举器实现即 `os.listdir` + 过滤（排除 templates 等非 feature 项），无解析不确定性。

【A】A7: 真值源二类——M7 hits 块（JSON 机读，声明=机械重数已由 m7_stats 看护）

- **取证**: [M7_EVIDENCE_LOG.md](../../docs/M7_EVIDENCE_LOG.md) L79-L101 hits 块: `"samples": 20` / `"form2_total": 53` / `"findings": {"p1": 6, "p2": 25, "p3": 41, ...}`——m7_stats verify 通过（1 P3 预期，2026-08-22 本轮执行）
- **关键结论**: 视图层的 M7 统计位点真值 = hits 块字段值；repo_stats 直接消费 hits 块（不重复解析样本表——单一真值源原则），校验 = 视图声明值 vs hits 字段值。

【A】A8: 真值源三类——各文档 front-matter（version/status 字段，YAML 头）

- **取证**: Grep `^version:|^status:` docs/ 结果（2026-08-22）: FACT_CHECK v1.0/active、ASSERTION v1.4.2/active、007 v1.3/toolized；spec/ 四件套与 ADR 各自携带（如 M7_HITS_RESEARCH front-matter `version: 1.0 / status: draft`）
- **关键结论**: §9 索引区版本号位点的真值 = 各文档 front-matter 字段；样本⑲③ 三处版本号半修态（ASSERTION v1.4→实 v1.4.2 等）证明该位点无对账必漂移；枚举器 = 逐文档 front-matter 提取（dc_validator M2 front-matter 解析器同构，但按 C1 裁决不并入）。

### 3.3 失效分析：双工具为何零拦截

【A】A9: ⑳轮活捕获——修正轮声明与执行分离，8 位点未写入而版本头已称"修完即绿"

- **取证**: M7 样本⑳（L30，本轮登记）: ⑲轮版本头声称「修复以登记后终值一次写齐，修完即绿」，实态 8 位点未写入（CODE_WIKI L66/L69/L576/L628/L4 + README 双语 L43 + evidence.svg + DIS-010 条目）；由本轮撰写前 Grep 全位点模式对账捕获（Grep 模式 `形态 II (27|29|34|45) 处|样本①-⑮|样本①-⑰|...` vs hits 真值 19/45）
- **关键结论**: 修正轮的版本头描述自身也是视图（修正动作的自我叙事）——声明性修正与执行性修正分离且无对账；四连残留链 ⑰→⑱→⑲→⑳ 证明这不是某轮偶然而是无机械对账下的必然递归。

【A】A10: 双工具覆盖盲区——m7_stats 的 files 限定 M7 单文件，dc_validator 只查 DC 契约，视图位点零覆盖

- **取证**: [.pre-commit-config.yaml](../../.pre-commit-config.yaml) L16-L20: m7-stats hook `files: ^docs/M7_EVIDENCE_LOG\.md$`（作用域收窄至账本）；dc_validator `files: \.md$` 但校验内容为 DC1-DC4 契约（front-matter 七字段/词表/断链/R7 计数）——均不比对视图载体数字 vs 真值源
- **关键结论**: 八度实证全部发生在两工具作用域之外——不是工具失效而是覆盖边界；repo_stats 填补的是「视图声明值 vs 真值源」这一类对账，与既有双工具正交。

【A】A11: 视图层已成为形态 II 第一大载体面——33 处占 62%

- **取证**: M7 分桶表 L55-L59 六行求和: 1(⑯) + 7(⑰) + 5(⑱) + 11(⑲) + 8(⑳) + 1(⑪ CODE_WIKI v1.5 行) = 33；hits 块 form2_total = 53；33/53 = 62.3%
- **关键结论**: 过半复发集中于一类载体一类字段（计数）——集中度本身就是工具化优先级论证（ROI 最高点位）。

### 3.4 先例对齐

【A】A12: m7_stats 先例三件套 + 写守卫——repo_stats 同构继承

- **取证**: m7_stats --write 本轮执行输出: `hits 块已重生成: docs/M7_EVIDENCE_LOG.md（samples=20, form2_total=53...）` + `M7 统计校验通过：1 结果，0 违规`；退出码 0/1/2 语义与 --selftest 内嵌自测（[M7_HITS_DESIGN](../m7-hits-block/M7_HITS_DESIGN.md) 契约）
- **关键结论**: 退出码/selftest/零依赖/python 前缀 hook 全部继承；**但 --write 语义不可继承**（见 B1——视图 prose 无可重生成结构）。

【A】A13: pre-commit 第三 hook 追加形态——files 收窄至视图载体集

- **取证**: .pre-commit-config.yaml 现双 hook（L9-L13 dc-validator `files: \.md$`、L16-L20 m7-stats `files: ^docs/M7_EVIDENCE_LOG\.md$`）；注释 L5: `entry 走 python 前缀（Windows 无 /bin/sh，RESEARCH §2.1 陷阱实证）`
- **关键结论**: repo-stats hook 的 files 须覆盖视图载体集（CODE_WIKI.md + README 双语 + discoveries/README.md + M7_EVIDENCE_LOG.md——真值源变更也须触发对账），`files: (CODE_WIKI\.md|README(\.en)?\.md|docs/(discoveries/)?README\.md|docs/M7_EVIDENCE_LOG\.md)$` 形态。

【A】A14: 围栏机读块先例——```hits JSON 形态可扩展 ```stats

- **取证**: SPEC_PROCESS L331 ```rules 块、LANGGRAPH L152 ```assertions 块、M7 L79 ```hits 块（三先例均 JSON 数组/对象 + 围栏语言标注）
- **关键结论**: ```stats 块沿用同族形态；dc_validator M5 对 fenced code block 内链接跳过（围栏内零干扰已实证）。

【A】A15: 本轮 Grep 模式对账即"模式扫描制"原型——方法论已在本会话验证

- **取证**: 本轮捕获⑳的执行记录: Grep 模式 `形态 II (27|29|34|45) 处|样本①-⑮|样本①-⑰|样本①-⑱|样本①-⑲|DIS-007~009|DIS-007~010|spec/ (七|八|九|十) feature` 于 CODE_WIKI 命中 6 行（L3 长行/L4/L66/L69/L576/L628）——全部残留位点一网打尽，无需位点清单
- **关键结论**: 「模式库 + 真值注入」的扫描制已人工验证可行——repo_stats 的核心校验循环 = 该 Grep 的脚本化（正则模式集 × 视图载体 × hits/LS/front-matter 真值）。

### 3.5 拦截模型（B 类推断）

#### 【B】B1: 视图位点不可重生成只能对账——repo_stats 与 m7_stats 的本质区别

- **推理链**（附录 B 机读登记）: ① m7_stats --write 可行因 hits 块是纯数据结构（JSON 围栏块），表内真值 → 声明块是单向派生，重生成确定；② 视图位点是 prose 自由文本内的数字（「样本①-⑳ + §5 hits 机读块，形态 II 53 处」嵌在目录树注释里），无法从真值机械重建周边 prose；③ 故 repo_stats 的操作只能是**对账**（扫描视图数字模式 → 与真值源比对 → 报告偏差），无 --write 模式；④ 对账制的代价：模式库须覆盖全部数字表达形态（漏模式 = 漏检，与样本⑩ grep 自引用盲区同族风险），selftest 须含模式库覆盖回归。
- **边界（不可脚本化，须保留人工）**: 视图 prose 的措辞演化（「样本①-⑳」→「第 20 个样本」等新表达形态）会逃逸旧模式库——模式库是活契约，须随新表达形态登记（误报/漏报复盘入 M7）。

## 4. 综合分析

### 4.1 关键发现总结

1. 视图层枚举面 = CODE_WIKI 四区（版本头/覆盖对象行/目录树/§9 索引）+ README 双语快照段 + evidence.svg 大数字 + DIS-010 派生统计，全部为真值源的无失效检测缓存副本（A1-A5）[置信度: ★★★★★]
2. 真值源三类清晰可机读：文件系统枚举（LS）、M7 hits 块（JSON）、各文档 front-matter（YAML）——三类均已有解析先例（A6-A8）[置信度: ★★★★★]
3. 八度实证全部发生在双工具覆盖边界之外；⑳轮"声明与执行分离"是最新最深失效形态——修正轮自身成为最大新漂移源（A9-A11）[置信度: ★★★★★]
4. 工程形态已被双先例定型（退出码/selftest/零依赖/hook 追加/围栏块），唯一新设计面 = 对账制拦截模型与门面层豁免契约（A12-A15 + B1）[置信度: ★★★★☆]

### 4.2 技术判断（C 类）

【C】**C1: 独立脚本 + 独立第三 hook，不并入双既有工具。** 理由链同 m7-hits C1 先例（职责分离 + verified 状态不重开 + 作用域正交）：dc_validator 是 DC 契约执行器、m7_stats 是账本统计校验器、repo_stats 是**视图对账器**——第三类职责（跨文件声明 vs 真值比对），files 作用域亦不同（跨载体集合）。

【C】**C2: 模式扫描制为主 + 枚举清单比对为辅，不做位点登记制。** 理由链：① 位点登记制（登记文件+行号+期望值）有行号漂移固有缺陷（样本⑧ 行号引证错前科）且新副本位点逃逸（⑲凭记忆选点必漏实证）；② 模式扫描制（正则扫数字表达形态 vs 真值）已在本轮人工验证（A15）且天然覆盖未知副本位点；③ 清单比对（目录树/索引区条目集 vs LS/front-matter 枚举集）补足非数字位点（A3 条目缺失形态）；④ 模式库与枚举集登记于 stats 机读块（数据非代码），漏检可追溯。

【C】**C3: 分级校验——活文档阻断（CODE_WIKI/discoveries），门面层提示（README/SVG）。** 理由链：① CODE_WIKI 与 discoveries/README 是活文档（应与真值同步，不等即违规）；② README/SVG 裁决为时点快照不追实时（DIS-010 处置既定），机械上只能校验「快照值合法」而非「快照值最新」；③ 快照合法性近似判据 = 快照值与 hits 当前值不等时报 P3 信息性提示（非阻断）——提示维护者择机刷新；快照值无法判定"曾为真值"（历史序列未存档，B1 边界），P3 提示是诚实上限，不虚构更强校验。

### 4.3 研究空白（本 feature 填补）

「声明 = 机械重数」原则已覆盖生成端统计表（R7/dc_validator M4）与账本端 hits 块（m7_stats），但**聚合视图层**（文档系统的读界面）仍是零覆盖——视图数字是真值源的缓存副本，缓存失效检测是文档工程的标准问题却在本仓八度实证后才被识别（DIS-010）。本 feature 把对账原则延伸到视图层，闭合「生成端 → 账本端 → 视图端」三段链。

## 5. 幻觉排除审查（Step 2 Review）

### 5.1 事实验证

| 引用 | 取证 | 验证方式 | 状态 |
|------|------|---------|------|
| A1-A3（CODE_WIKI 位点） | CODE_WIKI.md L3/L4/L50-L85/L576/L617-L634 | Read 逐行 + Grep `形态 II`/`覆盖对象` | ✅ 2026-08-22 |
| A4（README/SVG 快照） | README.md L43 / README.en.md L43 / evidence.svg L12/L18/L31 | Read 逐行 | ✅ |
| A5（DIS-010 派生统计） | discoveries/README.md DIS-010 行 | Read + 分桶表六行机械求和（33/53=62%） | ✅ |
| A6（文件系统真值） | spec/ adr/ docs/dev-log/ scripts/ | LS 四目录（2026-08-22） | ✅ |
| A7（hits 块真值） | M7 L79-L101 | Read + m7_stats verify 执行（1 P3 预期） | ✅ |
| A8（front-matter 真值） | docs/ 三文档 + spec/ 四件套 | Grep `^version:\|^status:` | ✅ |
| A9（⑳轮捕获） | M7 样本⑳行 + 本轮 Grep 执行记录 | 本会话 E1（工具输出留存） | ✅ |
| A10-A13（工具边界/先例） | .pre-commit-config.yaml 全文 + m7_stats --write 执行输出 | Read + RunCommand 执行 | ✅ |
| A15（模式扫描原型） | 本轮 Grep 命中 6 行 | 本会话 E1（工具输出留存） | ✅ |

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| 真值序列 21→22→29→34→45→53 从无 27 | M7 样本⑰⑱⑲⑳登记序列 + hits 块演化 | ✅ 逐样本核对 |
| 视图层 33 处占 62% | 分桶表 L49/L54-L59 六行求和 vs hits total | ✅ 机械重数（1+1+7+5+11+8=33；33/53=62.3%） |

### 5.3 待修正项

- 无（本调研零外部引用，无文献验证面；内部取证全部 E1 级）

> **门禁自查（ADR-0008 D4）**: (a) 无 FALSIFIED 断言；(b) 无 CONFLICT/STEP_GAP；(c) 阻断性断言（A1-A15 位点/真值/先例契约）全部 E1 取证，B1 推理链依赖源各自附 A 级证据；(d) 假设区 H1-H3 以 [待定] 显式携带进 DESIGN。**标注**: 本节为 `自查（单视角）`（RULE-4，同会话完成）——独立 pass 待 Step 10 或用户触发。**同轮修正声明**: 本调研撰写轮自身执行了样本⑳登记与八载体终值写齐（以⑳登记后终值 53/①-⑳ 为准）——修正动作先于本节自查完成，Grep 复验零残留（修完即绿于本轮由模式扫描对账确认，区别于⑲轮的仅声明）。

## 6. 对设计的输入

### 6.1 可用的技术方案

1. 独立脚本 `scripts/repo_stats.py`：校验（默认，无 --write）/ `--selftest` 内嵌自测；三模块 = 枚举器（LS/front-matter/hits 消费）+ 模式扫描器（正则模式库 × 视图载体）+ 清单比对器（目录树/索引条目集 vs 枚举集）
2. pre-commit 第三 hook `repo-stats`：files 覆盖视图载体集 + 真值源文件集
3. stats 机读声明块（```stats 围栏 JSON）：登记模式库版本、枚举集快照哈希（或声明计数）、门面层快照基准——**不含可重生成字段**（B1：对账制无重生成）

### 6.2 关键约束

1. 对账制（无 --write）：视图 prose 不可机械重建，只报偏差不代改（C3 门面分级 + RULE-5 单向权限同构——审计者永不自动修复）
2. 模式库 = 活契约：新表达形态须登记，漏检复盘入 M7（B1 边界）；模式库数据存 stats 块非代码常量（I-4 单一真值源同构）
3. 确定性：同输入双跑逐字节一致（I-2 同构）；无时间戳字段（C2 先例）
4. Windows：entry 用 `python` 前缀（A13）
5. 与双既有工具零冲突：stats 块围栏内不触发 M5；CODE_WIKI 无 §0 节不触发 M4（A14 同族边界）
6. 门面层 P3 非阻断、活文档 P1/P2 阻断（C3 分级）
7. **校验对象含修正轮产出自身**：版本头描述中的统计数字（L3 类位点）在扫描范围内（⑳轮新证——声明视图也是视图）

### 6.3 风险

| 风险 | 缓解 |
|------|------|
| 模式库漏检（新表达形态逃逸，样本⑩ grep 盲区同族） | 模式库版本化登记 + selftest 覆盖回归 + 漏检如实入 M7（模式库是活契约不是银弹，DIS-010 维护纪律同构） |
| 扫描器自身计数错（规律②：防幻觉工具自身不设防——样本⑨ 前科） | selftest expect 自增机械计数（DR-6 同构）+ 本脚本自身位点入扫描范围（三度递归防护：repo_stats 的 selftest 计数也被机械重数） |
| 正则误报（prose 元描述含被描述数字——改名复核语义甄别教训） | 模式锚定上下文词（`形态 II`/`样本①-`/`DIS-00\d~` 等限定前缀）+ 误报白名单登记于 stats 块（显式非静默） |
| 真值源三类的解析漂移（front-matter 格式演化/hits 块字段扩展） | 解析失败 ≠ 静默通过：结构性失败报 P1（声波式失败，m7_stats 同构） |

## 7. 参考文献

全部为仓库内部文档（正文已逐条链接取证）：CODE_WIKI.md、README.md、README.en.md、docs/assets/readme/evidence.svg、docs/M7_EVIDENCE_LOG.md、docs/discoveries/README.md、docs/PROGRESS.md、scripts/m7_stats.py、scripts/dc_validator.py、.pre-commit-config.yaml、spec/m7-hits-block/M7_HITS_DESIGN.md、spec/precommit-dc-validator/DESIGN.md。

---

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "视图位点不可重生成只能对账——repo_stats 无 --write 模式，与 m7_stats 的重生成模型本质不同；代价是模式库成为活契约（漏检风险须靠版本化登记与 selftest 回归兜底）",
    "op": "transitivity",
    "claimed_chain": [
      {"step": 1, "text": "m7_stats --write 可行因 hits 块是纯 JSON 数据结构，表内真值到声明块是单向派生", "source": "M7_EVIDENCE_LOG.md L79-L101 hits 块 + m7_stats --write 执行输出（本报告 A12）"},
      {"step": 2, "text": "视图位点是 prose 自由文本内嵌数字（目录树注释/教训表单元格/索引行），周边文字不可从真值机械重建", "source": "CODE_WIKI.md L66/L576/L628 位点形态（本报告 A1）"},
      {"step": 3, "text": "故拦截模型只能是扫描-比对-报告（对账制），且扫描模式库须随表达形态演化登记（grep 盲区前科：M7 样本⑩ 自引用 +1、⑳轮 Grep Omitted 长行复核纪律）", "source": "M7_EVIDENCE_LOG.md 样本⑩ 描述 + 本轮 Grep 执行记录（本报告 A15）"}
    ],
    "evidence_strength": "E1（依赖源逐条 Read/执行取证）",
    "audit_status": "OPEN（待独立 pass）"
  }
]
```

## 附录 C: 假设区（未取证声明）

- [H1] 视图载体数字表达形态可穷举为有限正则模式集且误报率可控（当前已知形态：`样本①-⑳`、`形态 II N 处`、`DIS-00X~00Y`、`N feature 目录`、`dev-log ×N`、`ADR-000X~000Y N 份`、`N 个模板`、`双/三 hook`）——查证路径: DESIGN 模式库全仓试扫 + 误报/漏报双清单
- [H2] §9 索引区版本号/状态字段可由 front-matter 机械提取并逐行对账（含四件套与 ADR 与框架文档）——查证路径: DESIGN 枚举器 PoC（front-matter 解析先例 = dc_validator M2，同构不并入）
- [H3] 门面层 P3 非阻断提示策略足以维持快照卫生（无阻断压力下维护者仍会择机刷新）——查证路径: 落地后两个 feature 周期观察 README/SVG 快照滞后幅度（M7 登记纪律同构）

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）
