---
id: semantica-absorption-RESEARCH
type: design
version: 1.3
status: in-review
date: 2026-08-23
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0005]
upstream: null
---

# Semantica（semantica-agi）调研：图原生决策溯源基础设施——与本框架的同构分析与结合可能评估 v1.3 (2026-08-23)

> **任务来源**: 用户提问"调研一下 gitHub Semantica 项目，分析此项目与本框架的联系，是否有结合可能"
> **实体消歧**: GitHub 存在多个同名 "Semantica"。用户确认目标 = **semantica-agi/semantica**（"The Open Source Palantir for AI Agents"，2025-06 建仓）。同名异实的另外两个：Hawksight-AI/semantica（语义智能框架——fork 网络仅显示第三方 fork 各自指向两组织，**semantica-agi 与 Hawksight-AI 的组织关系未查证**，v1.1 修正：原文"前身组织"系无源断言）、jean-bovet/Semantica（macOS 本地文档语义搜索 app，与本框架无关）。本调研证据全部指向 semantica-agi/semantica。
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；WebSearch + WebFetch 双通道取证（2026-08-23）。主证据源 = 仓库 README（74.5KB，已全文抓取核实）+ GitHub API 元数据。
> **审查状态**: `自查（单视角）` + `同基座深度 review（RULE-1 时序独立，RULE-5 未满足如实降级标注）`——v1.1 review 深度审计轮完成（发现 1P1+3P2+6P3，形态 II=4 处，见 §5.3）；独立 pass 待触发
> **裁决记录（2026-08-23 用户裁决，先于本轮审计）**: **暂不结合，登记候选**——方向 A（先例检索补位）为候选议程，方向 C 否决；登记于 [PROGRESS P-015](../../docs/PROGRESS.md)。本报告 §4 的"推荐"为裁决前调研结论，以裁决记录为准。
> **v1.1 变更（review 深度审计轮）**: §0 C 类计数 3→4（方向 B 漏计，机械看护边界外 review 臂捕获）/ 消歧段"前身组织"无源断言降级 / 补版本成熟度 A 类断言（0.6.5）/ H2 样本数 25 自指涉修正 + 新增 H4/H5 环境假设 / B1/B2 basis 锚点修正（编号引用悬空）/ "125 open issues"字段语义修正 / §5.2 技术声明验证表补全 + 证据强度分级
> **v1.2 变更（源码补充核验轮）**: 用户下载源码至 F:\semantica-main，README 自述级证据升级为**源码直读级**——新增 §2.5（9 条源码核验 A 类断言）；版本修正 0.6.5→**0.6.6**（pyproject.toml 直读，v1.1 的 0.6.5 系 README 示例值，证据升级非形态 II）；**H1 解除**（依赖树声明已核实——重量级：torch/transformers/spacy/faiss-cpu/opencv/librosa 等约 40 包为核心依赖）；**H5 解除**（包名 semantica 声明 + 仓库 URL 自洽）；H4 部分解除（OS Independent 分类器 + 全依赖有 Windows wheel 属声明级，安装实测仍未做）；record_decision 实际签名超 README 展示（valid_from/valid_until bi-temporal）——B1 字段对应加强；find_similar_decisions 机制源码确认（embedding 余弦 + 词法回退）——B2 依据升级；§6 方向 A 试点成本评估上修（依赖树多 GB，建议工作站而非主控站）
> **v1.3 变更（A+B 联合实现补充分析轮）**: 用户提问「方向 A B 是否可以都实现」——新增 §4.3：结论**可以且互补**（契约-实现分层：B 的 schema 吸收产物即 A 的导入字段映射契约，A 试点反测 B 映射质量）；字段映射质量预检表（ADR 映射干净 / M7「发现」列拆分非平凡 / severity→confidence 有损编码须显式契约）；B 先行（半天零环境成本）→ A 后行（工作站 1-2 天）时序；不改变现行「暂不结合」裁决——联合方案作为候选议程完整规格登记

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 25 | 每条附 URL/源码路径 + 可核对来源；取证日期 2026-08-23；v1.2 增源码直读级 9 条（§2.5） |
| B 推断类 | 2 | 登记于附录 B |
| C 判断类 | 6 | §4 结合方向评估 3 条（A/B/C）+ 风险 1 条 + §4.3 联合可行性 1 条 + 有损映射裁决项 1 条（v1.3 新增 2 条） |
| 假设区 | 5 | H1-H5（v1.2 后：H1/H5 已解除，H4 部分解除，H2/H3 待实测——编号保留） |

> **计数说明（R7 机械重数，两轮拦截/捕获实录）**: A 类 25 条（行首 `【A】` 标记——v1.0 首跑 M4 拦截声明 14 实为 15；v1.1 review 轮补 1 条后 16；v1.2 源码核验轮新增 §2.5 共 9 条后 25）；附录 B 2 条（`"id": "B\d+"` 机读块）；C 类 6 条（`【C】` 标记——**v1.0 声明 3 实为 4，【C】不参与 R7 机械对账，M4 无覆盖，由 v1.1 review 深度审计人工重数捕获**——A 类有 M4 门禁而 C 类裸奔的覆盖不对称实证；v1.3 新增 §4.3 两条后 6，本轮先行人工重数再写声明——㉖ 教训当日应用）；假设区 5 条（`[H\d+]` 列表项）。

## 1. 实体定位：它是什么，不是什么

三层区分（README 自身强调的定位）：

1. **不是 embedding 向量库 / RAG 检索器**——"They store embeddings, not meaning: context that can't be explained"（README §Why Semantica 引言）
2. **不是 LLM 或 agent 框架**——它"之下"（underneath）LLM、向量库与 agent 框架
3. **是确定性基础设施层**——Context Graph + 决策记录 + 溯源 + 推理引擎，"no LLM required for graph construction, reasoning, or provenance"（README §引言）

【A】仓库身份：`semantica-agi/semantica`——GitHub Organization（semantica-agi）名下公开仓库，Python 主语言，10,361 stars / 1,118 forks / 125 open issues+PRs（GitHub API `open_issues_count` 字段含 pull requests，v1.1 修正字段语义；2026-08-23 快照），homepage = getsemantica.ai。【来源：https://api.github.com/repos/semantica-agi/semantica】

【A】许可证：**MIT License**（GitHub API licenses 官方字段 spdx_id = "MIT"）。【来源：https://api.github.com/repos/semantica-agi/semantica 字段 license】

【A】活跃度：created_at = 2025-06-25；pushed_at = 2026-08-22（API 快照时点为 2026-08-23，即约一天前仍有推送）——活跃维护中。【来源：https://api.github.com/repos/semantica-agi/semantica 字段 created_at / pushed_at】

【A】版本成熟度（v1.2 源码修正）：**version = 0.6.6**（pyproject.toml `[project] version` 字段直读——v1.1 的 0.6.5 系 README Quick Start 的 doctor 示例输出值，源码为权威）。项目处于 0.x 阶段（接口稳定性无承诺，对照 dsh v0.1 明示 breaking changes 的先例，方向 A 试点须锁定版本）。【来源：F:\semantica-main\pyproject.toml L7（本地源码副本，2026-08-23 下载）】

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

### 2.5 源码补充核验（v1.2，2026-08-23——本地源码副本 F:\semantica-main，README 自述级证据升级为源码直读级）

【A】包身份与运行要求：PyPI 包名 `semantica`，requires-python = ">=3.8"，classifier 声明 "Operating System :: OS Independent" 与 "Development Status :: 5 - Production/Stable"；入口点 5 个（semantica / semantica-server / semantica-worker / semantica-explorer / semantica-mcp）；Repository URL 自洽指向 github.com/semantica-agi/semantica——**H5 解除（声明级）**。【来源：F:\semantica-main\pyproject.toml L6/L15/L17-35/L92-98/L260-265】

【A】核心依赖树为**重量级**（H1 解除——比 v1.1 假设更重）：核心 dependencies 约 40 包，含 **torch ≥1.13.1、transformers ≥4.20.0、sentence-transformers ≥2.2.0、spacy ≥3.4.0、faiss-cpu ≥1.7.0、opencv-python、librosa、umap-learn、gensim、scikit-learn、scipy、networkx、rdflib、matplotlib、plotly、pyarrow**——重 ML 栈是**核心依赖而非可选 extra**；pyoxigraph 属可选（extra `tripletstore-oxigraph`），Neo4j/Qdrant/weaviate/pinecone/milvus/pgvector 等存储后端全部为可选 extra。安装体积量级 = 多 GB（torch+transformers+spacy 模型）。附带发现：numpy 约束 ">=2.0.2" 实际不兼容 requires-python ">=3.8"（numpy 2.x 最低 3.9）——打包元数据自不一致（轻微，不影响 3.10+ 环境）。【来源：F:\semantica-main\pyproject.toml L46-90 / L100-257】

【A】ContextGraph 规模与 API 全定位：`semantica/context/context_graph.py` 单文件 **4,781 行**；README 声明的 8 个 API 全部在源码定位——get_neighbors（L936）/ state_at（L3485）/ add_causal_relationship（L3629）/ record_decision（L4078）/ find_similar_decisions（L5007）/ analyze_decision_impact（L5033）/ trace_decision_chain（L5063）/ check_decision_rules（L5087）。semantica/ 包共 **354 个 Python 文件**，模块目录与 README pipeline 声明一一对应（ingest/parse/normalize/split/semantic_extract/conflicts/dedup/kg/context/reasoning/provenance/export/graph_store/triplet_store/vector_store/ontology/pipeline/embeddings/visualization/explorer/mcp）。【来源：F:\semantica-main\semantica\context\context_graph.py 行号直读 + 目录枚举】

【A】record_decision 实际签名**超 README 展示**：`record_decision(category, scenario, reasoning, outcome, confidence, entities=None, decision_maker=None, metadata=None, valid_from=None, valid_until=None, **kwargs)`——README 示例只展示 6 参，实际还有 entities（关联实体）、decision_maker（决策者）、**valid_from/valid_until（bi-temporal 有效期）**；带输入校验（category ≤100 字符 / scenario ≤5000 / reasoning ≤10000 / outcome ≤1000，超限 ValueError）。【来源：F:\semantica-main\semantica\context\context_graph.py L4078-4132】

【A】因果关系类型与别名归一化：add_causal_relationship 接受 CAUSED / INFLUENCED / PRECEDENT_FOR 三型，且做别名归一化（小写 "causes" 等映射到规范大写形式），无效输入 ValueError；两端节点须为 decision 类型节点否则静默跳过。【来源：F:\semantica-main\semantica\context\context_graph.py L3629-3673】

【A】state_at 是真实 bi-temporal 实现：按 `node.is_active(at_time)` 与 `edge.is_active(at_time)` 过滤活跃节点/边后输出快照（含 valid_from/valid_until 字段），非简单日志回放。【来源：F:\semantica-main\semantica\context\context_graph.py L3485-3524】

【A】find_similar_decisions 的语义检索机制确认：委托 `find_precedents_by_scenario`（decision_query.py）——查询侧 EmbeddingGenerator 生成 embedding，与 decision 节点的 `reasoning_embedding` 做**余弦相似度**，embedding 不可用时回退词法/结构评分（含 Node2Vec 结构嵌入通道）——**B2 依据从 README 自述升级为源码确认**。【来源：F:\semantica-main\semantica\context\decision_query.py L288-330 + context_graph.py L5007-5031】

【A】推理引擎文件全在：reasoning/ 目录含 rete_engine.py / datalog_reasoner.py / sparql_reasoner.py / deductive_reasoner.py / abductive_reasoner.py / graph_reasoner.py + explanation_generator.py——README "Rete/Datalog/SPARQL" 声明对应真实模块文件。【来源：F:\semantica-main\semantica\reasoning\ 目录枚举】

【A】安全工程痕迹（补充观察）：conflicts/ 模块独立成体系（detector/resolver/analyzer/investigation_guide/provenance）；仓库含 CodeQL workflow / SSRF 防护测试（test_ssrf_protection.py）/ Cypher 注入测试（test_cypher_injection.py）/ 依赖审计门（pyproject 注明 crewai 因 chromadb CVE-2026-45829 被排除出 `all` extra）——工程成熟度高于典型 0.x 项目。【来源：F:\semantica-main\.github\workflows\ + tests\ + pyproject.toml L249-257】



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

- **空白 1（最高价值）**：本框架缺"历史先例语义召回"——裁决时无法回答"形态 II 在同类载体上怎么处置过""哪个决策模式被否决过"。find_similar_decisions 直接补这个位点。与 pattern_lib_version 2 候选议程的关系（v1.1 修正措辞）：该议程实为**模式锚定扩展**（更多 PT 正则覆盖边界外计数词，仍是机械匹配），Semantica 语义召回是更强的覆盖形态——两者同指"覆盖 pattern 库边界外位点"但机制不同层级，语义召回为机械模式扩展的上位替代候选，非同一议程。
- **空白 2**：本框架溯源是文本契约（引用四级标注 + doc_registry），无机器可查询的因果图——Semantica 的 PROV-O 是可选升级路径（下位兼容，导出层）。

## 4. 结合可能评估（C 类判断）

### 4.1 结论：有真实结合可能，集中在"语义先例检索"空白位点——推荐方向 A（检索视角层，不侵入验证端）

【C】方向 A（高价值、低侵入，推荐试点）：把 M7 账本/ADR/PROGRESS 的决策记录导入 Semantica Context Graph（只读文档 + 外部独立进程），换取 find_similar_decisions 式语义先例召回。不违反本仓零依赖不变式（Semantica 是外部工具不是仓库依赖）；姿态 = "检索视角层"，验证端（dc_validator/m7_stats/repo_stats/独立 pass）一律不动——与 P-013 结论一致（skill/MCP 出策略与证据，硬规则出裁决）。

【C】方向 B（方法论互认，零成本）：Semantica 决策记录 schema（scenario/reasoning/outcome/confidence + 关系类型）值得吸收进 decision_record 模板；本框架的反幻觉分级（P1/P2/P3 + 形态 II 分桶 + 对比臂审查）是 Semantica 自身缺失的机制（其 README 无此层）——双向论文级别互渗。

【C】方向 C（不建议）：全量引入图存储/推理引擎作为本仓库基础设施——与"纯文档 + 零依赖"定位直接冲突（P-006 已裁决"不整体迁移"同款判断）；且 Semantica 的 LLM 增强回答不能当机械证据（验证端必须保留硬规则）。

### 4.2 风险

【C】试点风险：README 所述能力（state_at 时间旅行、polyglot 存储、PROV-O 导出）未经本仓实测——文档示例与真实行为可能存在 gap（本框架 A 类断言纪律要求：引入前必须 clone + 实测，不能信 README 自述；v1.2 后核心子集已源码直读级确认，残余 gap 面 = PROV-O 导出行为/polyglot 实际切换/冲突检测运行时行为）。

### 4.3 A+B 联合实现可行性（v1.3 补充分析——用户提问"方向 A B 是否可以都实现"）

【C】联合可行性判断：**可以都实现，且两者是"契约-实现"分层关系而非并列竞争**——B（schema 吸收）的产物恰好是 A（Context Graph 导入）的字段映射契约：先 B 后 A 使导入有据可依、字段语义有登记可溯；A 的试点反过来成为 B 映射质量的实测检验（有损位点在导入时表面化）。单独看：B 独立成立（即使 A 试点失败——H3 中文召回质量差——schema 吸收对 ADR/decision_record 的结构化价值仍在）；A 无 B 也可行，但映射沦为临时拼凑——无登记契约的字段对应正是 DIS-009（实例级编号跨文档引用无限定规则）已实证过的风险面。

分维度兼容性检查：

| 维度 | B（schema 吸收） | A（先例检索试点） | 联合兼容性 |
|------|-----------------|------------------|-----------|
| 零依赖不变式 | 纯文档改动，不触 | 外部进程，不进 requirements | 双过 |
| 验证端硬规则 | 不触（记录格式非验证机制） | 输出仅作检索视角（非 E1 证据） | 双过 |
| 环境成本 | 零（文档批） | 工作站 A/B + 多 GB 依赖（v1.2 核验） | 分层解耦——B 无环境门槛 |
| spec 流程 | 小 feature（模板/契约改动须过 review 门禁 + DC 契约） | 试点脚本外部运行不入仓 | 各自独立走流程，互不阻塞 |
| 失效连坐 | — | H3 失败不连坐 B；H2 失败仅推迟 A | 单点失效不互毁 |

字段映射质量预检（B 的实质内容 = A 导入前须冻结的契约）：

| 本框架源字段 | Semantica 目标字段 | 映射质量 |
|------------|-------------------|---------|
| ADR：背景 / 决策 / 论证 | scenario / outcome / reasoning | **干净**（逐列直映） |
| M7 样本行：载体 / 日期 / 来源列 | category / valid_from / metadata | 干净 |
| M7 样本行：「发现」列 | scenario + reasoning + outcome 三字段 | **非平凡**——该列混合发现叙述与处置讨论，导入须拆分解析，非纯字段复制（ADR 决策映射比 M7 行映射干净——试点可先 ADR 后 M7 分两批） |
| 严重性 P1/P2/P3 | confidence（float 0-1） | **有损**——序数→连续需人为编码，见下条【C】 |
| 分桶→规律锚点 | PRECEDENT_FOR 边 | 结构映射（表格→图边），非字段映射 |

【C】有损映射裁决项：severity→confidence 编码（如 P1=0.9 / P2=0.5 / P3=0.3）是语义判断非机械转换——若实现 B，编码规则须作为显式契约登记（否则 find_similar_decisions 的 min_similarity=0.3 默认阈值在本仓语料上语义不明）；且编码一经登记不可漂移（否则跨批次导入的相似度排序失真）。

时序与成本（联合实现路径）：

1. **B 先行（半天级，零环境成本）**：契约批——decision_record schema 吸收（ADR_TEMPLATE 决策记录节或独立契约文档）+ 字段映射表 + severity 编码规则登记；走 spec 小流程（模板改动过 review 门禁 + DC 契约校验）
2. **A 后行（1-2 天，工作站 A/B 落点）**：以 B 契约为导入规范——ADR 决策批（映射干净，先行验证管道）+ M7 样本批（含「发现」列拆分解析）+ 召回测试（H2/H3 解除 + H4 安装实测）
3. **联合产出回路**：若 A 导入时暴露 B 映射有损位点（字段表面化），回写 B 契约修订——**A 是 B 的实测检验层，B 是 A 的数据契约层**

裁决影响：实现 A+B = 裁决从「暂不结合」改为「分层结合」（B 契约层立即 + A 试点触发驱动）；**本分析不改变现行裁决**——联合实现方案作为候选议程的完整规格登记，触发时可直接按 1→2 时序执行，无需重新调研。

## 5. 幻觉排除审查（Step 2 Review）

### 5.1 来源验证

| 引用 | 验证方式 | 状态 |
|------|---------|------|
| semantica-agi/semantica README（74.5KB） | WebFetch 全文抓取核对（2026-08-23） | ✅ |
| GitHub API 仓库元数据（license/stars/created_at） | WebFetch https://api.github.com/repos/semantica-agi/semantica 字段直读 | ✅ |
| 实体消歧（同名项目） | WebSearch 多结果比对（Hawksight-AI / jean-bovet / semantica-agi） | ✅（组织间关系除外——见消歧段 v1.1 修正） |
| 源码副本 F:\semantica-main（v1.2） | 用户下载；pyproject.toml / context_graph.py / decision_query.py / reasoning\ / 目录结构 Read+Grep 直读核验（2026-08-23） | ✅（9 条 A 类断言，§2.5） |

### 5.2 技术声明验证（v1.1 补——证据强度分级；v1.2 增源码直读级）

| 声明组 | 证据等级 | 说明 |
|--------|---------|------|
| §2.5 源码核验 9 条（版本/依赖树/API 行号/签名/机制） | **源码直读级**（最高，v1.2） | 本地源码副本文件与行号直读，可重复核验 |
| stars/forks/issues/license/created_at/pushed_at/homepage（API 字段） | **API 元数据级**（v1.0） | GitHub API 直读，真实性由 API 保证 |
| §2 能力断言（record_decision 签名/PROV-O/Rete/Datalog/state_at/polyglot/冲突检测） | **README 自述级 → 核心子集已源码确认**（v1.2） | README 声明已验证存在；其中 ContextGraph 8 API / 推理引擎文件 / 语义检索机制已升源码直读级（§2.5）；其余（PROV-O 导出/polyglot 切换/冲突检测行为）仍为自述级——引入前实测条款仍然适用 |
| 版本 0.6.6 | **源码直读级**（v1.2；v1.1 时为 README 示例级 0.6.5） | pyproject.toml `[project] version` |
| 引文照引（"They store embeddings, not meaning" 等四处） | **原文 grep 级** | 抓取文本逐字比对一致 |

### 5.3 v1.1 review 深度审计实录（盲区扫描）

审查配置：同基座深度 review（GLM-5.3，RULE-1 时序独立——新会话；RULE-5 未满足如实降级）。扫描面 = Iron Law 四类盲区 + 证据分级 + 环境维度 + R7 全级别重数。

| 严重性 | 发现 | 处置 |
|--------|------|------|
| P1 | §0 C 类计数声明 3 实为 4（方向 A/B/C 三条【C】+ 风险一条；声明"评估 2 条+风险 1 条"漏计方向 B）——【C】不参与 R7 机械对账，M4 无覆盖边界，review 臂人工重数捕获 | 已修正为 4 + 计数说明实录 |
| P2 | 消歧段"Hawksight-AI = semantica-agi 前身组织"实质断言未分级未附源（fork 网络未证两组织直接关系） | 降级为"组织关系未查证" |
| P2 | 版本成熟度维度缺失（0.x 阶段对结合决策的影响未评估） | 补 A 类断言（0.6.5 示例值） |
| P2 | 环境兼容性盲区：三机 Win10/Ubuntu × faiss/torch 依赖，试点第一道门槛未评估（Iron Law 边界条件盲区命中） | 新增 H4 |
| P3 | B1/B2 basis 编号引用悬空错位（A 类无编号体系却引"A2/A6"/"A5"） | 改节锚 + 修正注 |
| P3 | H2"24 个样本"自指涉停旧（㉕ 入账后 = 25） | 修正为 25 + 注记 |
| P3 | §3.3"pattern_lib_version 2 同向"语义拉伸（议程实为模式锚定扩展非语义跃迁） | 措辞修正 |
| P3 | "125 open issues"字段语义（open_issues_count 含 PR） | 修正为 issues+PRs |
| P3 | 用户裁决"暂不结合"未回写报告头部 | 头部补裁决记录 |
| P3 | A 类证据强度未分级 + §5.2 技术声明验证表缺失（自查深度不足——Iron Law 自我验证盲区命中）；PyPI 包名归属未查证 | 补 §5.2 分级表 + 新增 H5 |

> **形态 II 判定（4 处）**：计数×2（C 类声明 3→4——同⑫㉕ 计划-实际漂移，§0 统计表同载体第三、四例；H2 停旧 24→25——同㉓ 落地未回写）+ 锚点编号×2（B1/B2 basis 凭印象填 A 序号——章节号族新变体：锚点体系不存在 + 序号错位双重失效）。其余发现（无源断言/语义拉伸/信息缺失）非形态 II，如实区分。

### 5.4 待修正项

- [x] v1.0 遗留：方向 A 试点的假设需 clone + 实测解除（H1-H5，v1.1 扩充）
- [x] v1.1 review 轮 10 项发现全部同轮修正（本节实录）
- [x] v1.2 源码补充核验：H1/H5 解除（声明级）、H4 部分解除、版本 0.6.5→0.6.6 修正、B1/B2 依据升级（§2.5 实录）；剩余待实测 = pip install 安装行为（H4 残余）+ 导入适配（H2）+ 召回质量（H3）——均为试点执行时点事项，非文档修正项

## 6. 对设计的输入

### 6.1 可用技术方案

- 方案 A1：M7 样本 → Context Graph 节点（category=载体，scenario=发现，outcome=处置，confidence=严重性，metadata=来源，valid_from=样本日期），决策链 = 样本→分桶→规律锚点边（v1.2：bi-temporal 字段可用 valid_from 映射样本日期）
- 方案 A2：ADR → 决策节点 + PRECEDENT_FOR 边（修订历史链映射）
- 方案 B1：decision_record 模板吸收 Semantica schema（scenario/reasoning/outcome/confidence + 关系类型枚举 + valid_from/valid_until 时点字段）
- **成本注（v1.2 源码核验后上修）**：方向 A 试点须先安装多 GB 重依赖栈（torch/transformers/spacy/faiss-cpu 为核心依赖不可裁剪）——建议落工作站 A/B（Ubuntu + 128G 统一内存）而非主控站（Win10 32G 可行但吃紧）；导入用 25 样本 × record_decision 输入校验限制（scenario ≤5000 / reasoning ≤10000 字符）对本仓样本行长度无压力

### 6.2 关键约束

- 本仓零第三方依赖不变式不可破（Semantica 只能作外部进程/工具，不能入 requirements）
- 验证端硬规则不可替换（Semantica 输出只能作检索视角，不能当 E1 证据）
- MIT 许可允许复制借鉴（决策 schema / 导出格式），不存在许可障碍

### 6.3 风险（假设区）

- [H1] ~~Semantica 实际安装体积与依赖树未核实~~ **已解除（v1.2 源码核验，声明级）**：核心依赖约 40 包、重 ML 栈为核心依赖（torch/transformers/spacy/faiss-cpu/opencv/librosa），安装体积量级多 GB——**解除方向为"比假设更重"**，方向 A 试点成本相应上修；剩余未验 = pip install 实际安装行为（与 H4 合并）
- [H2] Context Graph 导入 25 个样本的适配成本（中文内容 + 自定义字段映射）未实测（v1.1 修正：原"24"系写作时点值，㉕ 入账后停旧——报告触发的样本使自身假设陈述漂移，自指涉时点案例）
- [H3] 先例检索的召回质量在"方法论裁决语义"（非企业合规语义）上未经验证——领域漂移风险（v1.2 补：检索机制已源码确认 = reasoning_embedding 余弦——中文 reasoning 字段的 embedding 质量是本假设的核心变量）
- [H4] 环境兼容性（v1.1 review 轮新增，Iron Law 边界盲区）：**部分解除（v1.2）**——pyproject 声明 OS Independent，且 torch/faiss-cpu/opencv 等核心依赖在 PyPI 均有 Windows wheel（声明级）；剩余未验 = 三机实际 pip install + import 冒烟（Win10 主控站 32G 内存对多 GB 栈可行但吃紧，建议试点落工作站 A/B——Ubuntu + 128G 统一内存）
- [H5] ~~PyPI 包名占用未查证~~ **已解除（v1.2 源码核验，声明级）**：pyproject `name = "semantica"` + Repository URL 自洽指向 semantica-agi/semantica；剩余未验 = PyPI 实际发布页与声明一致性（低风险，源码仓库即权威）

## 7. 参考文献

1. semantica-agi/semantica README — https://github.com/semantica-agi/semantica/blob/main/README.md（2026-08-23 抓取）
2. GitHub API 仓库元数据 — https://api.github.com/repos/semantica-agi/semantica（2026-08-23）
3. semantica-agi/semantica 主页 — https://github.com/semantica-agi/semantica
4. 同名项目（消歧用）：Hawksight-AI/semantica — https://github.com/arafathusayn/semantica（fork 源 page）
5. 同名项目（消歧用）：jean-bovet/Semantica — https://github.com/jean-bovet/Semantica/blob/main/README.md

## 附录 B：B 推断类登记

```json
{"id": "B1", "level": "B", "claim": "Semantica 决策记录 schema 与本框架 ADR/M7 样本行字段结构几乎逐列对应（v1.2 加强：bi-temporal 字段亦对应）", "basis": "§2.1 record_decision 签名（v1.2 源码直读级）与本仓 M7 样本行列结构逐字段比对：category↔载体、scenario↔发现、outcome↔处置、confidence↔严重性、metadata↔来源列；**valid_from/valid_until ↔ 本框架 front-matter date + facade_baseline as_of 时点语义**（双向时点化是 schema 级同构，超出 v1.0 预期）", "confidence": "高（源码确认）"}
{"id": "B2", "level": "B", "claim": "find_similar_decisions 可填补本框架历史先例语义召回空白（当前仅 grep 机械匹配）", "basis": "§2.5 源码确认：find_precedents_by_scenario 用 EmbeddingGenerator 查询 embedding vs decision.reasoning_embedding 余弦相似度 + 词法回退——机制真实存在（v1.0 时为 README 自述级，v1.2 升源码直读级）；剩余不确定 = 中文方法论语义的召回质量（H3）", "confidence": "中高（机制确认，效果待测）"}
```

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待触发）