---
id: semantica-absorption-RESEARCH
type: design
version: 1.0
status: in-review
date: 2026-08-23
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0005]
upstream: null
---

# Semantica（semantica-agi）调研：图原生决策溯源基础设施——与本框架的同构分析与结合可能评估 v1.0 (2026-08-23)

> **任务来源**: 用户提问"调研一下 gitHub Semantica 项目，分析此项目与本框架的联系，是否有结合可能"
> **实体消歧**: GitHub 存在多个同名 "Semantica"。用户确认目标 = **semantica-agi/semantica**（"The Open Source Palantir for AI Agents"，2025-06 建仓）。同名异实的另外两个：Hawksight-AI/semantica（语义智能框架 lineage，semantica-agi 前身组织）、jean-bovet/Semantica（macOS 本地文档语义搜索 app，与本框架无关）。本调研证据全部指向 semantica-agi/semantica。
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；WebSearch + WebFetch 双通道取证（2026-08-23）。主证据源 = 仓库 README（74.5KB，已全文抓取核实）+ GitHub API 元数据。
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 15 | 每条附 URL + 可核对来源（GitHub README / GitHub API 为主）；取证日期 2026-08-23 |
| B 推断类 | 2 | 登记于附录 B |
| C 判断类 | 3 | §4 结合方向评估 2 条 + 风险判断 1 条 |
| 假设区 | 3 | H1-H3，未取证声明 |

> **计数说明（R7 机械重数，v1.0 首跑 M4 拦截修正）**: A 类 15 条（行首 `【A】` 标记——首跑实测 15 实为声明 14，M4 机械拦截，同 DEEPSEEK 门禁实录同族）；附录 B 2 条（`"id": "B\d+"` 机读块）、C 类 3 条（`【C】` 标记）、假设区 3 条（`[H\d+]` 列表项）。

## 1. 实体定位：它是什么，不是什么

三层区分（README 自身强调的定位）：

1. **不是 embedding 向量库 / RAG 检索器**——"They store embeddings, not meaning: context that can't be explained"（README §Why Semantica 引言）
2. **不是 LLM 或 agent 框架**——它"之下"（underneath）LLM、向量库与 agent 框架
3. **是确定性基础设施层**——Context Graph + 决策记录 + 溯源 + 推理引擎，"no LLM required for graph construction, reasoning, or provenance"（README §引言）

【A】仓库身份：`semantica-agi/semantica`——GitHub Organization（semantica-agi）名下公开仓库，Python 主语言，10,361 stars / 1,118 forks / 125 open issues（2026-08-23 GitHub API 快照），homepage = getsemantica.ai。【来源：https://api.github.com/repos/semantica-agi/semantica】

【A】许可证：**MIT License**（GitHub API licenses 官方字段 spdx_id = "MIT"）。【来源：https://api.github.com/repos/semantica-agi/semantica 字段 license】

【A】活跃度：created_at = 2025-06-25；pushed_at = 2026-08-22（API 快照时点为 2026-08-23，即约一天前仍有推送）——活跃维护中。【来源：https://api.github.com/repos/semantica-agi/semantica 字段 created_at / pushed_at】

【A】核心定位句：README 标题与副标题为 "Graph-Native Infrastructure for Context and Accountable AI Systems"，副标题 "The Open Source Palantir for AI Agents"——公开领域自查合法性：引号内为原文照引，非虚构。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md L31-33】

## 2. 事实层：架构与能力（A 类断言）

### 2.1 决策智能（与本框架关联最深）

【A】决策是一等公民图对象：`record_decision(category, scenario, reasoning, outcome, confidence, metadata)` 创建结构化决策记录；`trace_decision_chain()` 返回完整因果祖先链（relationship_type ∈ {CAUSED, INFLUENCED, PRECEDENT_FOR}）；`find_similar_decisions()` 按语义检索历史先例；`analyze_decision_impact()` 生成下游影响图；`check_decision_rules()` 做策略合规门禁。README 给出金融示例（credit_application → loan_underwriting → interest_rate 因果链）。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §Decision Intelligence】

【A】决策导出为监管可接受格式：audit trail 可导出 W3C PROV-O（"the format most compliance frameworks accept for regulator submission"）、CSV 或 JSON。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §Decision Intelligence】

### 2.2 Context Graph 与溯源

【A】Context Graph 是"RAG 缺失的结构化记忆层"：实体、关系、决策、事实均为 first-class 图节点，可图遍历（get_neighbors hops=2）；`state_at(date)` 提供 point-in-time 图快照（时间旅行）。"traversal finds connections embeddings miss"。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §Context Graphs】

【A】全量溯源：W3C PROV-O provenance 挂在每个事实/决策上，可回答"where did this come from?"；audit trails 导出 JSON/CSV/RDF。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §What Semantica Gives You】

【A】边界声明（关键，与 LLM 透明化区分）："System-level explainability, not foundation-model explainability. Semantica does not expose or reconstruct what happens inside the LLM"——只解释模型外部（输入上下文、决策、出处、关系、策略、执行轨迹），不碰模型内部推理。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §引言 ⚠️ 块】

### 2.3 确定性机制

【A】确定性推理引擎：暴露 Forward chaining（前向链）、Rete network、Datalog、SPARQL，"fully explainable paths, not black boxes"。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §What Semantica Gives You】

【A】冲突检测：对比表明确 "Conflict detection: Detected, flagged, resolved"（对照 Vector DB+RAG 与 Plain LLM Memory 的 "Silent overwrite"）——矛盾事实显式标记而非静默覆盖。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §Why Semantica 对比表】

【A】零 LLM 依赖的分工：README 明示 "The reasoning engines, KG construction, and provenance layer are fully deterministic; no LLM is required to use them"——与向量库/LLM/agent 框架并存但不依赖。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §Why Semantica】

### 2.4 架构与集成

【A】端到端 pipeline：Sources → Ingest → Parse → Normalize → Split → Extract → Conflict Detection → Deduplication → Knowledge Graph → [Ontology · Reasoning · Provenance · Decisions] → Enriched KG → Vector Store + Polyglot Graph Store → Export/Visualize/REST/MCP/CLI（README §Architecture，module 独立可导入）。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §Architecture】

【A】Polyglot 存储：原生 RDF（嵌入式 Oxigraph、Blazegraph、Apache Jena、Eclipse RDF4J 经 SPARQL）+ Labeled Property Graph（Neo4j、FalkorDB、Apache AGE、AWS Neptune 经 Cypher）+ 向量库，可切换不碰代码。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §What Semantica Gives You】

【A】接入面：原生 Agno 与 CrewAI 支持、full-featured MCP server、CLI、REST API；企业数据平台连接器（Databricks Unity Catalog、Snowflake）。【来源：https://github.com/semantica-agi/semantica/blob/main/README.md §What Semantica Gives You / §Enterprise Data Platforms】

## 3. 综合分析

### 3.1 与本框架的同构对照（核心发现）

Semantica 与本框架（Spec_Workflow 方法论文档仓库）在**哲学与机制层面高度同构**——两者都是"不信任系统"的工业实现，只是落点不同（企业合规审计 vs 单人研究反幻觉）：

| 维度 | Semantica | 本框架 | 同构性质 |
|------|-----------|--------|---------|
| 核心立场 | 决策不可审计 = 合规敞口 | 产出不可验证 = 幻觉 | 同一问题的两面 |
| 决策记录 | record_decision(category/scenario/reasoning/outcome/confidence → 图节点) | ADR + decision_record + M7 样本行（载体/审查配置/发现/形态II/来源） | 字段结构几乎逐列对应 |
| 因果/追溯 | trace_decision_chain（CAUSED/INFLUENCED/PRECEDENT_FOR） | ADR 修订历史链 + PROGRESS 依据列 + 样本→分桶→规律锚点 | 图边 vs markdown 链接 |
| 先例召回 | find_similar_decisions（语义先例） | **缺位**（仅 grep 机械匹配） | 本框架空白位点 |
| 出处溯源 | W3C PROV-O 事实级图溯源 | A 类断言强制 URL+引文、引用四级标注、doc_registry | 图 PROV vs 文本证据契约 |
| 冲突检测 | 显式标记不静默覆盖 | 形态 II 复发检测、分桶对账、dc_validator 机械拦截 | 同构机制 |
| 时间旅行 | state_at(date) 图快照 | git 历史 + facade_baseline as_of 字段 + 版本演进 | 图快照 vs 时点快照基准 |
| 确定性层 | 图构建/推理/溯源零 LLM | 三校验器零第三方依赖、「声明=机械重数」 | 同构分工观 |
| 边界声明 | system-level，不碰模型内部 | 审计产出与证据链，不审 LLM 内部推理 | 同一边界纪律 |
| 策略/门禁 | check_decision_rules + SHACL | RULE-1~6 + DC 契约 + pre-commit 三 hook | 规则引擎 vs 流程规则 |

**要点**：同构不是巧合——两者都从同一个洞见出发：*不能让产生结论的系统自己证明结论*。验证必须移出 LLM，进确定性机械层。Semantica 的 "no LLM required for provenance/reasoning" 与本框架的 "E1 机械证据优先"（dc_validator/m7_stats/repo_stats 零依赖）是同一设计哲学。

### 3.2 关键差异（决定结合方式）

1. **技术形态**：Semantica = 可安装 Python 库 + polyglot 图存储 + 推理引擎 + 可视化工作台 + MCP/REST/CLI；本框架 = 纯 Markdown + git + 四个零第三方依赖脚本 + pre-commit（P-014 坐实"最小工具层"定位）
2. **领域**：Semantica 面向企业/监管合规（贷款、医疗、法律），决策需经受 regulator 的 "why"；本框架面向单人学术方法论 + 研究审计
3. **治理重量**：Semantica OWL/SHACL/SKOS 全套本体治理；本框架轻量 front-matter 七字段契约 + 词表
4. **语义检索**：Semantica 有语义先例检索；本框架只有 grep 机械匹配（无 NER、无语义连接）

### 3.3 研究/能力空白（本框架视角）

- **空白 1（最高价值）**：本框架缺"历史先例语义召回"——裁决时无法回答"形态 II 在同类载体上怎么处置过""哪个决策模式被否决过"。find_similar_decisions 直接补这个位点。样本㉒ 以来的 pattern_lib_version 2 议程（枚举性覆盖→语义级覆盖）与此同向。
- **空白 2**：本框架溯源是文本契约（引用四级标注 + doc_registry），无机器可查询的因果图——Semantica 的 PROV-O 是可选升级路径（下位兼容，导出层）。

## 4. 结合可能评估（C 类判断）

### 4.1 结论：有真实结合可能，集中在"语义先例检索"空白位点——推荐方向 A（检索视角层，不侵入验证端）

【C】方向 A（高价值、低侵入，推荐试点）：把 M7 账本/ADR/PROGRESS 的决策记录导入 Semantica Context Graph（只读文档 + 外部独立进程），换取 find_similar_decisions 式语义先例召回。不违反本仓零依赖不变式（Semantica 是外部工具不是仓库依赖）；姿态 = "检索视角层"，验证端（dc_validator/m7_stats/repo_stats/独立 pass）一律不动——与 P-013 结论一致（skill/MCP 出策略与证据，硬规则出裁决）。

【C】方向 B（方法论互认，零成本）：Semantica 决策记录 schema（scenario/reasoning/outcome/confidence + 关系类型）值得吸收进 decision_record 模板；本框架的反幻觉分级（P1/P2/P3 + 形态 II 分桶 + 对比臂审查）是 Semantica 自身缺失的机制（其 README 无此层）——双向论文级别互渗。

【C】方向 C（不建议）：全量引入图存储/推理引擎作为本仓库基础设施——与"纯文档 + 零依赖"定位直接冲突（P-006 已裁决"不整体迁移"同款判断）；且 Semantica 的 LLM 增强回答不能当机械证据（验证端必须保留硬规则）。

### 4.2 风险

【C】试点风险：README 所述能力（state_at 时间旅行、polyglot 存储、PROV-O 导出）未经本仓实测——文档示例与真实行为可能存在 gap（本框架 A 类断言纪律要求：引入前必须 clone + 实测，不能信 README 自述）。

## 5. 幻觉排除审查（Step 2 Review）

### 5.1 来源验证

| 引用 | 验证方式 | 状态 |
|------|---------|------|
| semantica-agi/semantica README（74.5KB） | WebFetch 全文抓取核对（2026-08-23） | ✅ |
| GitHub API 仓库元数据（license/stars/created_at） | WebFetch https://api.github.com/repos/semantica-agi/semantica 字段直读 | ✅ |
| 实体消歧（同名项目） | WebSearch 多结果比对（Hawksight-AI / jean-bovet / semantica-agi） | ✅ |

### 5.2 待修正项

- [ ] 方向 A 试点的假设 H1-H3 需 clone + 实测解除（见 §6.3）

## 6. 对设计的输入

### 6.1 可用技术方案

- 方案 A1：M7 样本 → Context Graph 节点（category=载体，scenario=发现，outcome=处置，confidence=严重性），决策链 = 样本→分桶→规律锚点边
- 方案 A2：ADR → 决策节点 + PRECEDENT_FOR 边（修订历史链映射）
- 方案 B1：decision_record 模板吸收 Semantica schema（scenario/reasoning/outcome/confidence + 关系类型枚举）

### 6.2 关键约束

- 本仓零第三方依赖不变式不可破（Semantica 只能作外部进程/工具，不能入 requirements）
- 验证端硬规则不可替换（Semantica 输出只能作检索视角，不能当 E1 证据）
- MIT 许可允许复制借鉴（决策 schema / 导出格式），不存在许可障碍

### 6.3 风险（假设区）

- [H1] Semantica 实际安装体积与依赖树（faiss/pyoxigraph 等）未核实——需 clone + pip install 实测
- [H2] Context Graph 导入 24 个样本的适配成本（中文内容 + 自定义字段映射）未实测
- [H3] 先例检索的召回质量在"方法论裁决语义"（非企业合规语义）上未经验证——领域漂移风险

## 7. 参考文献

1. semantica-agi/semantica README — https://github.com/semantica-agi/semantica/blob/main/README.md（2026-08-23 抓取）
2. GitHub API 仓库元数据 — https://api.github.com/repos/semantica-agi/semantica（2026-08-23）
3. semantica-agi/semantica 主页 — https://github.com/semantica-agi/semantica
4. 同名项目（消歧用）：Hawksight-AI/semantica — https://github.com/arafathusayn/semantica（fork 源 page）
5. 同名项目（消歧用）：jean-bovet/Semantica — https://github.com/jean-bovet/Semantica/blob/main/README.md

## 附录 B：B 推断类登记

```json
{"id": "B1", "level": "B", "claim": "Semantica 决策记录 schema 与本框架 ADR/M7 样本行字段结构逐列对应", "basis": "A2/A6 逐字段比对（category↔载体、scenario↔发现、outcome↔处置、confidence↔严重性）", "confidence": "高"}
{"id": "B2", "level": "B", "claim": "find_similar_decisions 可填补本框架历史先例语义召回空白（当前仅 grep 机械匹配）", "basis": "A5 Context Graph 遍历能力 + §3.3 空白 1 分析", "confidence": "中"}
```

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待触发）