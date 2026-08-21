# PROGRESS 待办登记

> 依据 SPEC_PROCESS 约定建立（每步完成后更新）。状态词表: `pending / in-progress / blocked / done`。
> 登记日期: 2026-08-16

## 待办事项

| ID | 事项 | 依据 | 状态 | 优先级 | 验收标准 |
|----|------|------|------|--------|---------|
| P-001 | Cpp_Hub 侧两文件迁移指针（ADR-0006 决策 3） | [ADR-0006](../adr/ADR-0006-assertion-framework-dual-copy-authority.md) 修订历史（决策 3 执行记录）/ [调研文档](../spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md) §6 | done | — | 五项验收：① P1/P2 指针 grep 双命中 ✅ ② Cpp_Hub 提交 `96edc5c`（AEF，选择性提交）✅ ③ DEVELOPMENT_LOG 代登（随现场提交入库）✅ ④ ADR-0006 追记 ✅ ⑤ pilot v1.1 引用=历史快照不改（开放项裁决）。注：DIS-007 属 Cpp_Hub gitignore 范围，指针本地生效；Cpp_Hub ahead 11 未推送（现场裁量） |
| P-002 | 第二次回流执行（6 项清单，优先级序） | [设计文档](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) v1.1 + [CHECKLIST](../spec/cpp-hub-absorption/CHECKLIST.md)（验收 39/40，1 P3 归 P-003） | done | — | 设计 §11 六项验收全过；[DEV-LOG-002](dev-log/DEV-LOG-002-cpp-hub-absorption-execution.md)；commits 8ea38bf/eed0906/f79fa49/b7a7f58（已推送） |
| P-003 | doc-contract 改造 Step A-G 执行 | [PLAN.md](../spec/doc-contract/PLAN.md) v1.5（verified） | done | — | Step A-G 全过（2026-08-17/18）：四项 grep 复核语义全过（`P0`@CHECKLIST 零 / `id:` 21 文件 / `docs/spec/`+`RESOLVED` 命中均为改名元描述，复核结论入 PLAN §5）；RULE-1~6 冠名 + rules 登记块；ADR_TEMPLATE 新建；PLAN v1.5（G→DC/§6 指针化/P3-1·2 闭环）；CODE_WIKI v1.2 尾随同步 |
| P-004 | GAP_ANALYSIS 审计 P2 修正后异基座 S1 复验 | [审计报告 S1 复验](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md) §7 | done | — | S1 复验完成（2026-08-18，DeepSeek V4 Pro 异构于 GLM-5.3）：P2-1(A 计数)/P2-2(行号)/P3-2(E1) 修正正确；发现 P2-3（C 计数仍差 1，审计修正自身含错，形态 II 第四实例）→ 已修正 C=2→3；B1-B4 核心结论成立；M7 样本 ⑥ 入表（形态 II 分桶 10→11） |
| P-005 | 形态 II 复发跟踪指标入 M7 | 审计报告 §4.3 | done | — | ① 分桶指标 ✅（[M7 §2](M7_EVIDENCE_LOG.md)，4 载体 × 7 字段类型 = 10 处，含映射闭合新桶）；② §0 计数脚本生成规则 ✅ 落 [框架 v1.4 R7](ASSERTION_EVIDENCE_FRAMEWORK.md)（原设想"入 ADR-0007"经评估主题错位改落框架——报告模板规则的权威载体，Tier1 同通道先例） |
| P-006 | LangGraph 框架化升级调研 | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) v1.1（复核后） | done | — | v1.0（14A→实为 11A，形态 II 第五实例，R7 机械重数修正）：不整体迁移，方法论仓库保持纯文档，自动化走薄壳 runner（方案 B），LangGraph 为触发条件后升级路径。v1.1 补充：最高 ROI = pre-commit + DC 契约校验器（形态 II 机械拦截，先于方案 B 可执行）；次高 = promptfoo（M7 对比臂声明式评测，触发条件样本≥10）。复核（2026-08-18）：推荐无幻觉（coograph/OpenMMLab 先例经 WebSearch 证实真实存在），补 coograph URL + OpenMMLab URL + A=15 重数自引用修正（`grep -c '【A】'` 原始 16 含本行自引用）。**决策已闭合（2026-08-19 治理收束轮）**：A 计数错误补登为 M7 样本⑩（自引用观察作附随观察不单列），见 M7 §1 |
| P-007 | pre-commit + DC 契约校验器（全流程 Step 1-7） | [调研报告](../spec/precommit-dc-validator/PRECOMMIT_DC_VALIDATOR_RESEARCH.md) v1.1 + [设计](../spec/precommit-dc-validator/DESIGN.md) v1.2 + [实施](../spec/precommit-dc-validator/IMPLEMENTATION.md) v1.1 + [验收](../spec/precommit-dc-validator/CHECKLIST.md) v1.0 | done | — | Step 1-4（2026-08-18）：调研+设计+复验（1P2+2P3 修正，M7 样本⑦⑧）。Step 5-7（2026-08-19）：IMPLEMENTATION v1.1（DR-1~DR-6）+ `scripts/dc_validator.py`（M1-M5，零依赖）+ `.pre-commit-config.yaml` 落地；dry-run 双通道 35 文件/9 skip/0 违规（独立调用 + pre-commit run 均 exit 0）+ selftest 13/13；存量违规修复 DR-5（ADR0006 A 计数 7→8 + ADR-0004/0005 断链 `../../`→`../`）+ DR-6（selftest 硬编码 12/12 → expect 自增机械计数，DESIGN §10.2 风险 1 预注册场景命中）；M7 样本⑨入账（形态 II ×2，分桶 13→15）。CHECKLIST 有条件通过（自查全绿，独立 pass 见 P-008） |
| P-008 | P-007 产出独立 pass（RULE-1 时序独立；真异基座优先） | [IMPLEMENTATION](../spec/precommit-dc-validator/IMPLEMENTATION.md) §9 + [CHECKLIST](../spec/precommit-dc-validator/CHECKLIST.md) §10.2 | done | — | 对话式默认形态执行（2026-08-20，DeepSeek V4 Pro 真异基座 vs 生成端 GLM-5.3——RULE-1 时序独立 + RULE-5 模型异质性双满足）：E1 四通道复核全过（selftest 13/13 重跑 / 全仓 dry-run 39 文件 0 违规 / 双跑逐字节一致 I-2 / pre-commit 通道 Passed）+ 词表 I-4 逐字符核对 + DR-5/DR-6 修复重验。发现 3 P3（① §4.3/§4.5 签名声明未覆盖 `root=ROOT` 实施参数 ② CHECKLIST §8.1"M2/M3/M4 共享解析器"映射不实——M4 从不调用 ③ DESIGN §10.1-4 LOC 核对缺位——实际 422 行）→ IMPLEMENTATION v1.2（修正注 + DR-7，status → verified）+ CHECKLIST v1.1（§8.1 修正 / §8.2 补录 / §10.3 签字，status → accepted）；M7 样本⑬ 入账（映射闭合 1 处，分桶 20→21——规律② 再实证："自查全绿不豁免逐项复核"） |
| P-009 | 薄壳纯 Python runner（方案 B，独立仓库） | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §5/§6 主判断（P-006 裁决方向）+ §9 session log 设计规范（v1.2，P-012 层 1 吸收：state 模型升格 append-only JSONL 事件流）+ LG H2/H7 PoC 查证 | pending | 5（触发驱动） | 方向性候选（自动化需求出现时启动）：runner 骨架独立仓库落地——显式 `--gate` 门禁命令物理化 RULE-1 + append-only JSONL 事件流 state（§9 规范：L1-L7 七原则 + 事件行 schema，状态 = 事件流派生视图，E1 取证为运行副产物）+ git 持久化 + LM Studio 端点异构审查 + **agent 执行层选型裁决（dsh SDK vs 裸 API，以 dsh H2 实测为输入——P-012 层 3，触发条件已满足）**；零框架依赖（~500-1000 LOC 待 LG H2 实测，事件流写入器 ~100 行内属替换非增量）；LangGraph 升级触发条件 (a)/(b)/(c)（调研 §6）随 runner 落地登记复查 |
| P-010 | promptfoo M7 对比臂声明式评测 | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §8.2/§8.3（次高 ROI）+ LG H5 PoC 查证 | pending | 3 | 触发条件已满足（M7 样本 12 ≥ 10，样本⑫ 已入账——P-013 调研轮 M5 拦截；混轴修正注见 M7 样本⑪③）：promptfooconfig.yaml（LM Studio 本地端点作 provider）+ 首轮声明式对比评测（同一报告 × 同基座/异基座审查）结果入 M7 登记；LG H5 成本/延迟实测 |
| P-011 | M7 统计升 ```hits 机读块 + 样本登记脚本化 | [M7 §4](M7_EVIDENCE_LOG.md) 待办挂钩（[CPP_HUB_ABSORPTION_DESIGN](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) §6 既定）+ [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §6 零成本项 | pending | 2 | 学习回路独立议题（不并入其他 feature）：M7 增设 ```hits 机读块（统计可脚本重数/生成）+ 样本追加由手工登记改脚本辅助（`grep -c` 重数先例）；与 dc_validator R7 计数检查衔接 |
| P-012 | DeepSeek Harness（dsh）调研与吸收复用裁决 | [调研报告](../spec/deepseek-harness/DEEPSEEK_HARNESS_RESEARCH.md) v1.0（14A+3B+3C+4H，R7 机械重数一致） | done | — | 四层裁决：①机制立即吸收（session log 设计思想 + M5 方法论互证入资产）——**层 1 已落地（2026-08-20）**：LANGGRAPH v1.2 §9（七原则 L1-L7 + SPEC_PROCESS 规则映射 + 事件行 schema + 不吸收清单），P-009 依据/验收同步；②P-008 执行形态增 dsh 试点选项（工作站 A + DeepSeek V4 Pro 真异基座 + JSONL 取证，默认仍对话式、试点并行）；③P-009 agent 执行层选型重裁决（dsh SDK vs 裸 API，触发条件已满足，以 H2 实测为输入）——**已登记入 P-009 验收标准（2026-08-20 补执行）**；④本体不进仓（纯文档 + 最小工具层定位不变）。待办挂钩：dsh H2/H3/H4 实测挂 P-008/P-009 执行时 |
| P-013 | 开源 skill 生态对十步流程的增强调研（含 MCP 补充） | [调研报告](../spec/skill-enhancement/SKILL_ENHANCEMENT_RESEARCH.md) v1.1（21A+4B+4C+6H——v1.0 初稿手填 14A 为 M5 拦截，M7 样本⑫；v1.1 §8 MCP 补充一次通过） | done | — | 三层吸收裁决："skill 供弹药（生成端），硬规则守边界（验证端），接缝处显式登记"。①生成端自由吸收（Step 1/3/5/7/9：smart-search/brainstorming/writing-plans/TDD）；②验证端受控复用（Step 2/4/6/8/10 铁律：skill 内置验证仍是 LLM 自查，不可替代 E1 机械证据与门禁——可复用其结构设计：agreement 表/引文重读/机械主源验证段）；③并存架构（`context: fork` 是 RULE-1 的 skill 层物理化；skill 产出必须流经同一硬规则漏斗；skill 不进本仓，推荐候选登记挂 SPEC_PROCESS 修订另行裁决）。三次外部互证：superpowers/oh-rid/gthimmes 独立演化出与 RULE-1/RULE-6(c)/E3 同构纪律。P-008 执行形态增 oh-rid 三家族选项。**v1.1 §8（MCP vs skill）**：5 组本会话直测（E1）——paper-search 主题/精确检索可用且结构化、stackexchange 默认 site=mathoverflow 陷阱 + 召回偏差（E1 真实性 ≠ 语义相关性）、本地 mcp_paper-search = openags/paper-search-mcp 开源部署实例；主判断 = 对信息真实性 MCP 结构性优于 skill（证据等级由构造决定：E1 vs E4），完整三层分工"**MCP 出证据（真数据）、skill 出策略（怎么搜）、硬规则出裁决（何时必验）**"；约束不变：E1 不豁免证据身份验证（EuropePMC 前科 + 召回偏差实证）。SKL H5/H6（stackexchange 净增益 / MCP 入取证矩阵格式）挂后续 feature 实测 |

## 待办事项优先级裁决（2026-08-20）

> 对 4 项 pending（P-008/P-009/P-010/P-011）的综合排序。四维（ROI / 依赖 / 难度 / 风险）分析，断言全部追溯至源文档：[LANGGRAPH_UPGRADE_RESEARCH](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §5/§6/§8/附录、[M7 账本](M7_EVIDENCE_LOG.md) §1/§4、[SPEC_PROCESS](../SPEC_PROCESS.md)、P-012/P-013 调研报告。
> 样本数「12」为 2026-08-20 快照值（M7 样本登记表 12 行，样本⑫ 为最新），随账本追加顺延。
> **H 编号命名空间消歧（跨文档撞名防误读）**：PROGRESS 中裸「H」分属两套独立假设编号——[LANGGRAPH](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md)（P-006）H1-H7 与 [DEEPSEEK_HARNESS](../spec/deepseek-harness/DEEPSEEK_HARNESS_RESEARCH.md)（P-012）H1-H4。P-009 依据列「H2/H7 PoC」= LANGGRAPH（H2=LOC 估算、H7=事件流状态）；P-009 验收列「以 H2 实测为输入（P-012 层 3）」与 P-012 行「H2/H3/H4 实测」= dsh/P-012（H2=SDK 工作站可用性）；「~500-1000 LOC 待 H2 实测」= LANGGRAPH H2。

### 评估维度定义

- **ROI**：高（解决核心痛点/方法论自洽）/ 中（提效/降风险）/ 低（锦上添花/未来需求）
- **依赖**：零（独立可执行）/ 弱（依赖其他低优先级项）/ 强（依赖未完成前置）
- **难度**：低（≤0.5 人天）/ 中（1-2 人天）/ 高（>2 人天或架构级）
- **风险**：高（形态选型/技术选型/悬置成本）/ 中（实测依赖/验收标准）/ 低（流程性/机械性）

### 四维评估矩阵

| 项 | ROI | 依赖 | 难度 | 风险 | 悬置成本 |
|---|-----|------|------|------|---------|
| **P-008** | 极高（P-007 闭环门禁 + RULE-1 自我兑现 + M7 样本⑬） | 零（对话式形态） | 低-中（一个审查会话） | 形态选择拖延 | 最高（方法论自洽性债务） |
| **P-011** | 中（登记负担随样本线性增长） | 零 | 低（~0.5 天） | 近零（脚本须过 ADD） | 低但递增 |
| **P-010** | 高（M7 从手工账本变声明式评测矩阵） | 零 | 中（配置 + 首轮评测） | LG H5 成本/延迟未知 | 低 |
| **P-009** | 当前低/潜在高 | LG H2/H7 实测（选型前置） | 高（500-1000 LOC） | 过度工程 + dsh breaking | 零（等待触发即设计状态） |

### 依赖链

```
主动队列：P-008 → P-011 → P-010（优先级 1 → 2 → 3）

交叉影响：
  P-008（可选并行 dsh 试点，P-012 层 2）──顺产──→ dsh H2/H3 实测 ──解除──→ P-009 选型前置
  P-011 ──产出──→ M7 hits 机读块 ──顺流（弱）──→ P-010 评测结果登记自动化
  P-008 / P-010 / P-011 执行经验 ──→ SPEC_PROCESS 修订（有实测依据；LG H5 随 P-010 顺产验证，SKL H5/H6 挂后续 feature 实测不在此链——原 H1/H5/H6 压缩表述无指代一致读法，2026-08-20 H 撞名调研轮重写）
  P-009 ←── 外部触发（自动化需求出现；LANGGRAPH §6 触发条件 (a)/(b)/(c) 未现，不主动启动）
```

### 综合排序结论

1. **P-008（优先级 1，立即，对话式先行）**：4 项 pending 中唯一收口阻塞项——P-007 的 CHECKLIST 为「有条件通过（自查全绿）」，其转 `accepted`、IMPLEMENTATION 转 `verified` 均依赖 P-008 独立 pass（RULE-1 时序独立，[SPEC_PROCESS](../SPEC_PROCESS.md)）。零依赖（对话式 DeepSeek V4 Pro 直调即默认路径）× 最低成本（一个审查会话）× 最高治理收益（闭环 P-007 + 自我兑现 RULE-1 + 追加 M7 样本⑬）。风险仅在形态选择拖延，对话式先行即可消解。
2. **P-011（优先级 2，P-008 同周可并行）**：半天级 + 近零风险。双重背书：M7 账本 §4 待办挂钩（[CPP_HUB_ABSORPTION_DESIGN §6 既定](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md)）+ LANGGRAPH §6【C】「零成本项」。产出 hits 机读块为 P-010 评测结果登记自动化铺路（顺流弱依赖），并与 dc_validator R7 计数检查衔接。
3. **P-010（优先级 3，P-011 后）**：触发条件已满足（M7 样本 12 ≥ 10，LANGGRAPH §8.3 触发阈值「≥10」）。值次高 ROI（LANGGRAPH §8.3【C】），把 S1 异构复验手动切基座 + 样本人工登记升级为声明式对比评测；P-008 审查产出可作首轮评测材料。
4. **P-009（优先级 5，触发驱动，不主动启动）**：方向性候选，待自动化需求出现。LG H2（LOC 估算）/LG H7（事件流状态）PoC 与 dsh SDK vs 裸 API 选型（P-012 层 3）为前置，P-008 并行 dsh 试点可顺产部分实测输入。

> **优先级编号说明**：1/2/3 为主动执行队列序（P-008 → P-011 → P-010）；P-009 记为 5 而非 4，标识其属「触发驱动」异质类（不排队、等外部条件），语义上与主动队列隔开，避免被误读为「下一个要做的第 4 项」。

## 已完成（近期）

| 日期 | 事项 | 产出 |
|------|------|------|
| 2026-08-20 | P-008 独立 pass（对话式真异基座 DeepSeek V4 Pro，RULE-1+RULE-5 双满足）：E1 四通道复核全过 + 3 P3 登记修正（签名 root 参数 / 映射断言 / LOC 对账）；IMPLEMENTATION → v1.2 verified、CHECKLIST → v1.1 accepted；M7 样本⑬（映射闭合——"自查全绿不豁免逐项复核"）；同日待办优先级裁决（P-008→P-011→P-010 主动队列 + P-009 触发驱动）与 H 撞名消歧登记 | spec/precommit-dc-validator/IMPLEMENTATION.md v1.2 + CHECKLIST.md v1.1 + M7 样本⑬ |
| 2026-08-20 | P-013 开源 skill 生态增强调研：十步 × skill 映射矩阵 + 三层并存裁决（生成端自由/验证端受控/接缝登记）；初稿手填 A=14 被 M5 拦截（实为 16）→ M7 样本⑫（分桶 19→20，规律② 第三层实证：教训记忆不提供免疫力）；同日 P-012 层 1 落地（LANGGRAPH v1.2 §9 session log 设计规范） | spec/skill-enhancement/SKILL_ENHANCEMENT_RESEARCH.md v1.0 |
| 2026-08-20 | P-012 DeepSeek Harness 调研（实体消歧 "j space deepseek hardness"→dsh）：14A+3B+3C+4H，四层吸收裁决（机制吸收/P-008 试点选项/P-009 选型重裁决/本体不进仓）；R7 机械重数一致（A14 独立编号修正记录在案） | spec/deepseek-harness/DEEPSEEK_HARNESS_RESEARCH.md v1.0 |
| 2026-08-19 | 治理收束轮（遗留任务调研 + 收敛）：M7 样本⑩ 补登（分桶 15→16）+ ADR-0009 失效条件首次重审（机制保留）+ DIS-007 v1.3 追记 DR-6 + LANGGRAPH L26 标注收束 + P-009~P-011 登记 + CODE_WIKI v1.5；**dry-run 自查追加样本⑪**（分桶 16→19——收束轮自身产出 3 计数错 + 1 超前断言，人工机械枚举拦截，规律② 最强实例） | DEV-LOG-004；PROGRESS / ADR-0009 / discoveries README / 007 / LANGGRAPH 全收敛 |
| 2026-08-19 | P-007 Step 5-7（实施+验收）：DC 契约校验器落地 | `scripts/dc_validator.py` + `.pre-commit-config.yaml` + IMPLEMENTATION v1.1 + CHECKLIST v1.0 + M7 样本⑨（分桶 13→15） |
| 2026-08-18 | P-004/P-005/P-006 收束 + P-007 Step 1-4（调研+设计+复验） | commits 7d0255b / 5a5cbd0（已推送）；RESEARCH v1.1 + DESIGN v1.2 |
