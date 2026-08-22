# 审查验收 Checklist：repo_stats 视图层机械枚举校验器

---
id: repo-stats-CHECKLIST
type: design
version: 1.1
status: accepting
date: 2026-08-22
depends: [repo-stats-IMPLEMENTATION, repo-stats-DESIGN, repo-stats-RESEARCH]
upstream: null
---

> **Feature**: repo_stats（PROGRESS P-014，[DIS-010](../../docs/discoveries/README.md) 处置落地）
> **创建日期**: 2026-08-22
> **状态**: accepting（验收决定 = **有条件通过**——自查全绿 + 机械证据 E1 可重放；条件 = RULE-1 独立 pass，同 P-007/P-011 先例，不冒充 accepted）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [REPO_STATS_IMPLEMENTATION.md](./REPO_STATS_IMPLEMENTATION.md) v1.1
> **基于设计**: [REPO_STATS_DESIGN.md](./REPO_STATS_DESIGN.md) v1.1
> **验收者**: 自查（单视角，RULE-4）——GLM-5.3；独立 pass 待触发（同 P-007/P-011 先例）

---

## 1. 文档一致性验收（Step 8）

### 1.1 RESEARCH ↔ DESIGN 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN 决策可追溯 RESEARCH（A1-A15/B1/C1-C3） | ☒ | DESIGN §2.1 映射表 8 行逐一引用；A1/A2→扫描制、A3→清单比对、A4→载体两级、A5→口径声明、A6-A8→真值枚举器、A9-A11/C1→第三类职责、A12-A14→三件套继承、A15→核心校验循环、B1→对账制、C2→模式库、C3→分级校验 |
| RESEARCH 关键发现被 DESIGN 使用（无孤儿发现） | ☒ | H1→§4.3 模式库初版 + 实施期全仓试扫验收；H2→doc_registry + PoC；H3→落地后观察期挂本 §6 |
| 无文档间矛盾 | ☒ | v1.1 契约修正（view_layer_total 口径）已三文档同口径（DESIGN §4.2/§4.4/§6 + IMPL §1/§2.4） |

### 1.2 DESIGN ↔ IMPLEMENTATION 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 模块 RS1-RS5 ↔ IMPLEMENTATION §3/§4 | ☒ | 签名汇总表逐行对应；build_truth_set(spec) 参数细化已声明（IMPL §9.2） |
| 校验规则集（DESIGN §4.4）↔ IMPLEMENTATION §2.4/§6 逐行 | ☒ | 11 条规则 + 错误场景表逐行映射 fixture |
| 不变式 I-1~I-7 ↔ IMPLEMENTATION §7 | ☒ | I-7（修正轮产出在扫描面）为 DESIGN 新增项，IMPL F19 对应 |
| 实施裁定显式登记非私改 | ☒ | 两处：行号状态机（IMPL §3.4 注）+ 围栏过滤精确语义（IMPL §2.4——普通围栏保留扫描面，树注释是载体） |
| LOC 预估核对义务登记 | ☒ | IMPL §10 预估 ~650（口径含 selftest 显式声明）——**Step 9 后回填实际值** |
| DESIGN v1.1 修正追溯完整 | ☒ | 变更注（35≠33 对账证据）+ 四触点（§4.2 字段表/绑定集/§4.4/§6）+ IMPL §1 如实登记 |

### 1.3 IMPLEMENTATION ↔ CHECKLIST 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| IMPLEMENTATION 功能点在本 checklist 有验收项 | ☒ | §2（RS1-RS5）/§3（不变式）/§4（集成）逐模块覆盖 |
| 本 checklist 验收项可追溯到 IMPLEMENTATION | ☒ | 各表「测试方法」列引 IMPL fixture 号 |
| 活靶表双向引用 | ☒ | IMPL §10.3 七项 ↔ 本 §5 活靶捕获验收逐项对应 |

### 1.4 术语一致性

| 术语 | RESEARCH | DESIGN | IMPLEMENTATION | 一致 |
|------|----------|--------|----------------|------|
| stats 机读块 / ```stats 围栏 | ✅ | ✅ | ✅ | ☒ |
| 对账制（vs 重生成制） | ✅（B1） | ✅（§1/方案 D） | ✅（§1） | ☒ |
| living / facade 载体两级 | ✅（C3） | ✅（§4.2） | ✅（§3.4） | ☒ |
| 视图载体行求和（v1.1 口径） | ✅（A5） | ✅（§4.2 v1.1） | ✅（§2.4 T7） | ☒ |
| suppress 白名单 | ✅（§6.3） | ✅（§4.2） | ✅（§3.4） | ☒ |
| facade_baseline / as_of 快照 | ✅（A4） | ✅（§4.2） | ✅（§3.4） | ☒ |

### 1.5 双向引用与断言延续（ADR-0008 D6）

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 四件套 + PROGRESS P-014 + DIS-010 互引成立 | ☒ | 正向：四件套→DIS-010/PROGRESS/ADR-0007/m7-hits-DESIGN/precommit-DESIGN；反向：PROGRESS P-014→spec/repo-stats/、DIS-010 处置→P-014（dc_validator M5 全仓通道将于终验实证） |
| B1 断言状态按最新词表标注 | ☒ | RESEARCH 附录 B audit_status: OPEN——独立 pass 后闭合（如实，未冒充） |
| Step 8 派生需求项（双向引用/断言延续）无新增 | ☒ | 无实施期派生断言（IMPL 两处裁定为细化非派生需求；Step 9 若产生派生需求登记 IMPL §10 派生表——m7-hits DR-A/B/C 先例） |

## 2. 功能验收（Step 9-10 完成——RS1-RS5）

> **真值前移注记（如实双时点登记）**：本节通过条件列的预期值按 **Step 10 收口时点**刷新（DEV-LOG-006 创建 + M7 样本㉑ 登记致真值前移：dev_logs 5→6 / samples 20→21 / form2_total 53→60 / view_layer_total 33→40 / pct 62→66）；Step 7-8 撰写时点旧值已随事件过时——**本表预期值自身即视图，验证以运行时真值对账为准（verify 全绿为准）**，与 DIS-010 现象同构的验收层实例，如实登记不静默改值。

### 2.1 RS3 stats 块解析

| 验收项 | 测试方法 | 通过条件 | 状态 |
|--------|---------|---------|------|
| 块存在/唯一/JSON 合法 | F2/F3 | 缺失/多块/非法均 P1 | ☒ |
| schema 校验（patterns/declared/carriers/baseline/suppress） | F4 | 越界逐条 P1 | ☒ |
| 真实 CODE_WIKI §10 stats 块解析 | dry-run | 无结构性 P1 | ☒ |

### 2.2 RS2 真值枚举器（七通道）

| 验收项 | 测试方法 | 通过条件 | 状态 |
|--------|---------|---------|------|
| T1-T4 fs 枚举（目录/文件/hook/P-号） | F1 + 真实仓 dry-run | spec=10/adr=6/dev-log=6/scripts=3/templates=5/hooks=3/P=14（收口时点；撰写时点 dev-log=5） | ☒ |
| T5 hits 直读 | F13 + 真实仓 | samples=21 / form2_total=60（收口时点；撰写时点 20/53）；损坏声波式 P1 | ☒ |
| T6 dis 范围 | F1 + 真实仓 | min=1 / max=10 | ☒ |
| T7 视图载体行求和（v1.1 口径） | F1 + 真实仓 | total=40 / pct=66（收口时点；撰写时点 33/62）（**回归锚：样本列求和不复现**——撰写时点 35 / 收口时点 42，两时点均 ≠ 求和值，口径分离再证） | ☒ |

### 2.3 RS4 三路对账

| 验收项 | 测试方法 | 通过条件 | 状态 |
|--------|---------|---------|------|
| ① rs-decl 声明=重数 | F5 | 失配 P1 + declared/actual 报文 | ☒ |
| ② living 模式扫描（P2） | F6 | 命中值≠真值逐位点报告 + 行号 | ☒ |
| ② facade 基准漂移/滞后（P3 非阻断） | F7/F8 | exit 0 + [P3] 可见 | ☒ |
| ② SVG `>N<` 包含性通道 | F7 变体（F7b） | 缺失 P3 | ☒ |
| ③ 树/索引清单比对（双向） | F9/F10 | 缺登/幻影均 P2 | ☒ |
| ③ doc_registry 版本全等比对 | F11 | v1.4≠1.4.2 报 P2 | ☒ |
| suppress 白名单 | F7 变体（F7c） | 双匹配跳过、单匹配不跳 | ☒ |
| 数字形态转换全区间 | F12 | 中文一~九十九 + 带圈 1-35 逐值精确 | ☒ |

### 2.4 RS1 CLI + RS5 selftest

| 验收项 | 测试方法 | 通过条件 | 状态 |
|--------|---------|---------|------|
| verify 默认模式 | 真实仓 dry-run | 活靶修正后 exit 0 | ☒ |
| skip 语义 | F16 | 作用域外交集空 exit 0 | ☒ |
| selftest 23 fixture（19 基础 + F7b/F7c 双变体 + F20 TDD） | `--selftest` | 23/23 PASS（N = 机械计数，IMPL §8.1） | ☒ |
| 退出码三值语义 | F2/F6/F16 | 0/1/2 与 dc_validator/m7_stats 逐字一致 | ☒ |

## 3. 不变式验收（Step 9-10 完成）

| 不变式 | 验证方式 | 状态 |
|--------|---------|------|
| I-1 全模式只读（无写通道） | argparse 无 --write + F1 迷你仓字节不变 | ☒ |
| I-2 确定性 | F17 双跑逐字节一致 | ☒ |
| I-3 零新规则 | 代码规则集 == DESIGN §4.4 逐行（Step 10 审查） | ☒ |
| I-4 单一真值源（数据非代码） | F18 stats 块改模式即生效 + 代码零模式常量 | ☒ |
| I-5 异构于生成端 | 零 LLM/网络 import（结构性） | ☒ |
| I-6 声明=重数两级 | F5（第一级）/F6（第二级） | ☒ |
| I-7 修正轮产出在扫描面 | F19 版本头叙事数字命中 | ☒（⑳轮需求「校验对象含修正轮产出自身」落地实证——v1.7 改写批全程同轮 verify 看护） |

## 4. 集成验收（Step 9-10 完成）

| 验收项 | 通过条件 | 状态 |
|--------|---------|------|
| CODE_WIKI §10 stats 块落位 | 文件末尾追加，§1-§9 零重排（diff 仅尾部） | ☒ |
| 模式库 PT-1~PT-11 全仓试扫定稿 | 误报/漏报双清单（H1 验收），EN 变体入册 | ☒（EN 变体 PT-1E/2E/6D/7C 入册；误报清单 = DR-H~J 三项全部 fixture 化/正则化修复，漏报 0——首跑 7 真靶全捕获） |
| `.pre-commit-config.yaml` 第三 hook | `pre-commit run repo-stats --all-files` 通过 | ☒ |
| CODE_WIKI v1.7 入册同步 | 三 hook / repo_stats 可执行件 / §2.1 树 + §9 索引补 repo-stats 行 | ☒ |
| L561 历史叙事位点处置 | 按 IMPL §10.4 预案改写（非 suppress） | ☒ |
| 三校验器全仓回归 | dc_validator 0 违规 + m7_stats 通过 + repo_stats exit 0 + `pre-commit run --all-files` 全绿 | ☒（Step 10 终验见 §8.3） |

## 5. 活靶捕获验收（工具有效性实证——首跑全捕获）

**验收判据（IMPL §8.2/§10.3）**: verify 首跑预期捕获七项活靶——**首跑全绿 = 扫描器证伪**（活靶在手）；捕获集 = 工具有效性以捕获真实漂移为证，非以全绿为证（DESIGN §4.5）。

| # | 活靶（IMPL §10.3） | 首跑捕获 | 修正后复验 | 状态 |
|---|-------------------|---------|-----------|------|
| 1 | §9 缺 spec/repo-stats/ 索引行 | ☒ | ☒ | ☒ |
| 2 | §9「断言分级证据框架 v1.4」→ 1.4.2 | ☒ | ☒ | ☒ |
| 3 | §9「文档规范改造方案 v1.5」→ 1.6 | ☒ | ☒ | ☒ |
| 4 | §9「LangGraph 框架化调研 v1.1」→ 1.2 | ☒ | ☒ | ☒ |
| 5 | §2.1 树缺 repo-stats/ 目录条目 | ☒ | ☒ | ☒ |
| 6 | L67/L630「P-001~P-013」→ P-014（PT-11） | ☒ | ☒ | ☒ |
| 7 | L4/L5/L54「双 hook」→ 三（PT-8，hook 入册后复跑） | ☒ | ☒ | ☒ |

> 活靶 2-4（⑲发现③ 遗留批——发现条目粒度的声明/执行分离）+ 活靶 5（spec 流程自身产生活漂移）为 IMPLEMENTATION 撰写轮新取证，捕获后按 M7 登记纪律评估入账（是否独立样本 vs 并入 P-014 实施轮实录——届时裁决）。
>
> **入账裁决（Step 10 收口）**：并入 P-014 实施轮实录，以 **M7 样本㉑** 单样本登记（7 P2 = 版本号×3 + 计数×4，含活靶 1-7 全部七项——各靶位无独立审查轮、同轮首跑机械捕获，不拆独立样本）；首跑另 3 项误报为工具侧缺陷（DR-H~J），fixture 化修复后不入发现账。**首跑实录**：verify 首跑报 10 项 P2 = 上表 7 真靶（漏报 0）+ 3 误报——「首跑全绿 = 扫描器证伪」判据通过（活靶在手，全绿未发生）。

## 6. ADD 审计（Step 10 完成）

### 6.1 Phase 0 质量门（测试通过 ≠ 设计落地）

| 检查项 | 状态 |
|--------|------|
| 测试通过且不变式逐条核验（非仅 exit code） | ☒（§3 七条逐条核验 + F1-F20 fixture 映射，IMPL §7/§8.1） |
| Iron Law：无「绿即验收」——活靶捕获实证在案（§5） | ☒（首跑 7 真靶全捕获、漏报 0——全绿前先证捕获） |
| 派生需求登记（若有，IMPL §10 派生表） | ☒（实施期发现 DR-D~J 六项全数登记 IMPL §9.6/§9.7，无未登记派生） |
| LOC 预估回填 + 口径声明核对 | ☒（IMPL §10：预估 ~650 → 实际 1276，超估 92% 三主因分解；口径含 selftest 显式声明） |

### 6.2 取证矩阵（E1-E5）

| 证据 | 覆盖项 | 等级 | 状态 |
|------|--------|------|------|
| `python scripts/repo_stats.py --selftest` 23/23 输出 | RS5 全 fixture | E1 | ☒（§8.3 终验实录） |
| verify 首跑活靶捕获 stdout 留痕 | §5 七项 | E1 | ☒（IMPL §10.3 首跑实录 + M7 样本㉑ 审查配置列） |
| 修正后 verify exit 0 + 三校验器全仓回归输出 | §4 集成 | E1 | ☒（§8.3 终验实录） |
| `pre-commit run --all-files` 三 hook 全绿 | hook 通道 | E1 | ☒（§8.3 终验实录） |
| 盲区声明（E4）: 模式库漏检新表达形态 / 门面快照「曾为真值」不可判定（B1） | 能力边界 | E4 | ☒（落位 = CODE_WIKI §10 stats 块「试扫否决记录」+「已知未覆盖」注记区：PT-3 否决 / SVG 规律数大数 / EN 词形数字 / 树 scripts/ 文件级 / 述史负向后顾排除） |

## 7. 验收统计

**统计口径（规则 2 统计溯源——不手填，来源逐项声明）**:

| 类别 | 计数 | 来源 |
|------|------|------|
| 文档一致性验收项（§1） | 15 | 本表机械计数（1.1×3 + 1.2×6 + 1.3×3 + 1.5×3，勾选项） |
| 功能验收项（§2） | 19 | §2 各表机械计数（2.1×3 + 2.2×4 + 2.3×8 + 2.4×4） |
| 不变式验收项（§3） | 7 | DESIGN §8 逐条 |
| 集成验收项（§4） | 6 | §4 表机械计数 |
| 活靶捕获项（§5） | 7 | IMPL §10.3 逐项（首跑捕获/修正复验/状态三列全勾） |
| ADD 审计项（§6） | 9 | 6.1×4 + 6.2×5 |
| **当前勾选 / 总项** | 63 / 63 | §1-§6 全勾（Step 10 收口）；§8 独立 pass 待触发（不计入自查勾选面） |

## 8. 独立审查追记（预留）

### 8.1 独立 pass 记录

待触发（RULE-1 时序独立 + RULE-5 异质性；触发条件 = 用户指令或 Step 10 裁决）。

### 8.2 追记区

（独立审查/异基座复验结论与修正记录——P-011 先例：异步独立审计曾捕获 CODE_WIKI v1.6 两处错误断言，追记入本节并同步 M7）

**【收口批独立审查追记·2026-08-22】** 收口批独立 review（[REPO_STATS_AUDIT.md](./REPO_STATS_AUDIT.md) v1.0；RULE-1 时序独立满足——新会话与收口轮分离；RULE-5 同基座降级标注，同样本⑦形态）对收口批数字链条自洽性审查（R7 机械重数 + 逐位点 Read 取证），捕获 1 P3：[PROGRESS](../../docs/PROGRESS.md) P-014 依据列「八度实证」计数词停旧——行内其余字段均为收口时点值，独计数词停在立项时点；位于 repo_stats 机械对账边界外（「N 度实证」无 PT 模式锚定，verify 四通道零拦截——**pattern 覆盖枚举性首个 post-toolization 边界实证**，pattern_lib_version 2 候选议程）。入账裁决 A（新样本㉒，判例法三条件全中：形态 II 计数复发 ∧ 轮次分离 ∧ 新机制变体；B/C 否决——review 臂捕获须入对比臂归因，不可并入工具捕获样本㉑）。八步后续行动全执行（2026-08-22）：① PROGRESS 八度→九度 ② M7 §1 ㉒行 + §2 分桶行（PROGRESS P-014 行，计数 +1）+ 合计 60→61 ③ `m7_stats.py --write`（写守卫自证算术）④ repo_stats verify 首跑枚举活靶 9 P2 + 6 P3（living 停旧值族 + facade 三件快照滞后，与审计 §1.3 级联预测吻合）⑤ living 位点修正（CODE_WIKI ×4 / discoveries 66%→65%）→ exit 0 ⑥ facade_baseline 22/61 + 门面三件刷新 → 0 P3 提示 ⑦ 追记三处（本节 / DEV-LOG-006 / DIS-010 后注）⑧ 四通道终验 + 一次 commit。错误未流入版本历史（P-014 未 commit，提交前拦截）。本轮 review 不构成独立 pass（同基座降级），§8.1 待触发不变。

### 8.3 Step 10 终验实录（E1 留痕，2026-08-22 收口轮）

收口同步批（CHECKLIST v1.1 勾选 + PROGRESS P-014 → done + CODE_WIKI v1.7.1 §9 状态行同步）完成后全量重跑：

| 通道 | 命令 | 输出（exit code） |
|------|------|------------------|
| RS5 selftest | `python scripts/repo_stats.py --selftest` | `selftest: 23/23 PASS`（0） |
| RS1 verify | `python scripts/repo_stats.py` | `repo_stats 视图层对账通过：0 违规（P3 提示 0）`（0） |
| M7 账本 | `python scripts/m7_stats.py` | `M7 统计校验通过：1 结果，0 违规（P3 提示 1）`（0；P3 = 样本③ 发现列历史非整齐形态，预期非阻断） |
| DC 契约 | `python -S -E scripts/dc_validator.py` | `50 文件、13 skip、0 违规`（0） |
| 提交门禁 | `pre-commit run --all-files` | dc-validator / m7-stats / repo-stats 三 hook 全 Passed（0） |

> **收口批自身在扫描面（I-7 收口轮实证）**：本批改动含 CODE_WIKI（living 载体）与 PROGRESS（真值源），verify 于改动后重跑即全绿——「修完即绿」由模式扫描对账确认，与⑳轮「声明性修完即绿」（无对账）成对照。

---

**验收决定**: **有条件通过**（自查全绿 63/63 + E1 机械证据可重放——§8.3 五通道；条件 = RULE-1 独立 pass（真异基座优先）后 IMPLEMENTATION → verified、本 CHECKLIST → accepted，同 P-007/P-011 先例节奏，不冒充 accepted）

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | GLM-5.3（自查·单视角，RULE-4） | 2026-08-22 |
| 审查者 | 待独立 pass | — |

**后续行动**: 独立 pass（触发驱动，含 fixture 矩阵与 stats 块契约复核）；PROGRESS P-014 → done ✅；DEV-LOG-006 ✅；CODE_WIKI v1.7/v1.7.1 同步 ✅。
