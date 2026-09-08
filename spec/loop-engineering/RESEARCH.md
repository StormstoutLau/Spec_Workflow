# 调研文档：loop engineering 循环工作流调研（社区概念 + 开源项目 + 学术论文 + 本仓组建循环的收益代价）

---
id: loop-engineering-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-09-09
depends: [SPEC-PROCESS, ADR-0007, ADR-0010, community-ecosystem-RESEARCH]
upstream: null
---

> **Feature**: loop engineering 循环工作流调研（PROGRESS P-028——Layer-0 概念调研登记，循环组建为触发驱动候选）
> **创建日期**: 2026-09-09
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「一个问题 当前流程是单向的 没有循环工作流 调研社区所谓loop engineering 当前工作流是否可以组建循环 收益 代价 同时调研社区开源项目 学术论文进行调研」+ 落档裁决「落档为新 feature RESEARCH（推荐）」。

---

## 1. 调研目标

**核心问题**（新外部调研，WebSearch 取证）：

1. 社区所谓 **loop engineering** 是什么？与 prompt / context / harness engineering 的演进关系？
2. 当前工作流（Spec_Workflow 十步管道）的**单向性**在哪里？现有机制哪些已是"半循环"？
3. 本仓能否组建循环工作流？**收益与代价**是什么（须有学术/实证支撑，不凭直觉）？
4. 社区开源项目与学术论文中有哪些可参考形态？

> **调研边界说明**：本 feature 为**概念调研登记**（同 P-023 drift-gate 先例），产出 RESEARCH 落档，**不实施循环本身**。组建循环（如 L1 反思循环）登记为触发驱动候选（ADR-0010 Q2），止于懒加载 gate。

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| WebSearch | 社区 loop engineering 概念溯源 + 开源项目快照 | `loop engineering` / `agent loop` / `OpenClaw` / `LangGraph` / `Self-Evolving-Agents` |
| WebSearch | 学术论文检索 | `Reflexion` / `Self-Refine` / `LATS` / `AgentOptimizer` / `ExpeL` / `self-evolution survey` / `recursive self-improvement` |
| Grep/Read | 本仓工作流结构取证（spec_runner 命令面 / M7 账本 / PROGRESS） | `def cmd_` / `step-gate` / `verify-anchor` / `step-enforce` |

### 2.2 调研范围

- **社区概念**: loop engineering 起源（2026-06，Peter Steinberger + Addy Osmani）、五步闭环、与 harness engineering 关系
- **开源项目**: OpenClaw / LangGraph / AutoGPT / AutoGen / EvoAgentX / EdgeClaw 循环机制快照
- **学术论文**: Reflexion / Self-Refine / MAR / ERL / EvolveR / Self-Evolving Survey / AI4AI-Bench / Agent-in-the-Loop
- **本仓现状**: spec_runner.py 命令面（run/gate/step-gate/step-enforce/verify-anchor/selftest）+ M7 账本 + 三通道校验器
- **不做**: 循环功能实现（L1/L2/L3 仅登记为候选）；新机制代码；外部工具引入

## 3. 调研发现

### 3.1 社区 loop engineering 概念

【A】**loop engineering 是 2026-06 兴起的概念**——6-07 Peter Steinberger（OpenClaw 作者）提出「相关技能不再是 prompt 编码 agent，而是设计驱动 prompt 的循环」，帖子约 650 万浏览量；6-08 Addy Osmani（Google）发表《Loop Engineering》给出解剖结构（automations / worktrees / skills / connectors / sub-agents / external state）。【依据：https://tosea.ai/blog/loop-engineering-ai-agents-complete-guide-2026 ；https://addyosmani.com/blog/loop-engineering/】

【A】**定义**：设计、运行并持续改进 AI Agent 内部反馈循环的工程实践；基本单元从单条 prompt 变为循环——模型行动 → 环境反馈 → 依据反馈决策下一步 → 直到定义的终止条件。Kilo.ai 2026-06 给出权威定义（五步闭环 = 意图设定 → 上下文采集 → 行动执行 → 结果观察 → 动态调整）。【依据：https://tosea.ai/blog/loop-engineering-ai-agents-complete-guide-2026 ；CSDN《打破AI模型内卷！Loop与Harness工程》】

【A】**核心理念 = 错误是新上下文**：测试失败、编译报错、审查问题不再是终止信号，而是推翻错误假设、指导下一轮迭代的素材——「每一次报错都是智能体自我优化的宝贵素材」。这与本仓反幻觉/反形式化审查表演的目标同构（失败样本进入下一轮输入）。【依据：CSDN《打破AI模型内卷！Loop与Harness工程》；LangChain《The agent improvement loop starts with a trace》——「在软件中，代码文档化应用；在 AI 中，trace 文档化应用」】

【A】**演进线**：prompt engineering（优化表达）→ context engineering（优化模型所见信息）→ harness engineering（优化运行环境，Viv Trivedy 团队不改模型仅重构外部系统即 Top30→Top5）→ loop engineering（优化驱动循环）。各层嵌套包裹而非替代。【依据：https://tosea.ai/blog/loop-engineering-ai-agents-complete-guide-2026 ；Terminal Bench 2.0 引用数据（Claude Opus 4.6 官方工具链排名 33，第三方工具链排名 5）】

### 3.2 开源项目调研

【A】**OpenClaw**（自托管个人 Agent 框架，350k+ stars）：核心循环 = Observe-Plan-Act；append-only transcript + Markdown-first 记忆（SOUL.md/AGENTS.md/TOOLS.md）+ SQLite 索引 + activation-decay；多模型 fallback。2026 年安全事件（ClawJacked/Claw Chain）说明自治循环引入的攻击面。【依据：https://github.com/franklimag/harness/blob/main/repos/openclaw-openclaw.md】

【A】**LangGraph**（~27k stars，PyPI 月下载 ~34.5M）：图编排有状态 agent——Pregel/Beam 执行模型，durable execution + human-in-the-loop + streaming，循环是图结构一等公民。【依据：https://github.com/bg-l2norm/awesome-ai-agent-papers--#general-purpose-frameworks】

【A】**AutoGPT / AutoGen**：AutoGPT（~183k stars）开创自治 agent 类别；AutoGen（~54k stars，ICLR 2024 LLM Agents Workshop best paper）定义多 agent 会话范式。【依据：https://github.com/bg-l2norm/awesome-ai-agent-papers--#general-purpose-frameworks】

【A】**EvoAgentX**（EMNLP'25 Demo）：自动演化 agentic workflow 的开源框架；其配套 Awesome-Self-Evolving-Agents 清单系统梳理 2023-2025 单 agent/多 agent/领域特化三条演化方向。【依据：https://github.com/EvoAgentX/EvoAgentX ；https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents】

【A】**EdgeClaw**（OpenBMB，OpenClaw 分支）：Self-Driven Loop——tick scheduling + sleep tool + 后台命令自动化 + async sub-agents，使 agent 自主持续工作。【依据：https://github.com/Openbmb/edgeclaw】

【C】**开源项目对本仓的参考形态**：OpenClaw 的 append-only transcript + Markdown-first 记忆 = 本仓事件流 + M7 账本的同构印证（社区第 N 个独立印证，同 CER §3.4 先例）；LangGraph 说明循环需图结构 + durable state + 人机协同（human-in-the-loop）；EvoAgentX 说明 workflow 本身可被演化优化（对应 L3 配置循环候选）。本体均**不复用**（本仓为纯文档方法论仓，无运行时依赖需求，同 Ponytail/Superpowers 不复用先例）。【置信度: ★★★★☆】

### 3.3 学术论文调研

【A】**Reflexion**（arXiv:2303.11366，NeurIPS'23）：verbal reinforcement learning——不更新权重，通过语言反思 + 情景记忆强化 agent。三模型结构（Actor/Evaluator/Self-Reflection）；HumanEval pass@1 91% vs GPT-4 80%。反馈放大为自然语言反思 =「语义梯度」。【依据：https://arxiv.org/abs/2303.11366】

【A】**MAR**（arXiv:2512.20845）：复现 Reflexion 发现单 agent 自评自省的系统性缺陷——同一模型既生成行动又评估自己又产生反思，导致重复推理错误、确认偏误、纠错反馈受限；多 agent 分工可缓解。【依据：https://arxiv.org/html/2512.20845v2】

【A】**ERL**（arXiv:2603.24639，Experiential Reflective Learning）：从任务轨迹反思**提取可迁移启发式原则**而非存原始轨迹，测试时按任务检索注入上下文。Gaia2 +7.8%；消融显示选择性检索至关重要、启发式比 few-shot 轨迹更可迁移。【依据：https://arxiv.org/html/2603.24639v2】

【A】**EvolveR**（arXiv:2510.16079）：离线蒸馏（轨迹 → 可复用策略原则库）+ 在线交互（检索原则指导执行）+ 策略强化，形成持续闭环；性能随轮次持续上升而非触顶。【依据：https://arxiv.org/abs/2510.16079 ；CSDN《近一年 Agent 自进化的两大方向和四大趋势》】

【A】**A Survey of Self-Evolving Agents**（arXiv:2507.21046）：首个系统综述，what / when / how to evolve 三维分类（模型/上下文/工具/架构 × 测试时/测试间 × 奖励/演示/进化）。【依据：https://arxiv.org/html/2507.21046v2】

【A】**AI4AI-Bench**（arXiv:2608.20318）：递归自改进（RSI）基准——10 个冻结研究仓，agent 改写训练算法后重跑评分。29 配置 6 系统均值 0.166，最强 0.250（最优 1.0）。**实证警告：递归自改进远未成熟**——多数提交只改"如何运行"不改"如何学习"。【依据：https://arxiv.org/html/2608.20318v1】

【A】**Agent-in-the-Loop**（arXiv:2510.06674，Airbnb）：data flywheel——四类在线反馈信号（响应偏好/采纳决策/知识相关/缺失知识）回流模型更新，retraining 周期月 → 周；检索 recall@75 +11.7%。【依据：https://arxiv.org/pdf/2510.06674】

【C】**学术结论对组建循环的三条约束**：① 反馈信号必须是**机械可验证**的——Reflexion 靠 LLM 自评导致确认偏误（MAR 实证），本仓天然有机械三通道 + 异基座独立 pass，是结构性优势而非缺失；② **启发式原则比轨迹可迁移**（ERL）——循环沉淀物应为失败模式/原则而非原始轨迹；③ **递归自修改远未成熟**（AI4AI 0.250/1.0）——自动化改写校验规则/统计声明的 L3 形态须暂缓，人类必须在环。【置信度: ★★★★★】

### 3.4 本仓工作流单向性诊断

【B】**spec_runner 命令面全只读校验**（本仓取证）：`run / gate / status / replay / fork / step-gate / step-enforce / verify-anchor / selftest`——step-gate（P-020）/ step-enforce（P-024）/ verify-anchor（P-025）均为只读校验器（P-022「只读零副作用」教训），输出不回流下一批次。【依据：tools/spec_runner/spec_runner.py 命令面；PROGRESS P-020/P-022/P-024/P-025】

【B】**事件流 append-only + 流程管道线性**：`tools/spec_runner/sessions/*.jsonl` 只增不改；十步管道 RESEARCH → DESIGN → IMPLEMENTATION → CHECKLIST 单向推进，批次间无自动反馈。【依据：tools/spec_runner/sessions/ 目录；SPEC_PROCESS 十步流程】

【B】**已存在"半循环"基础设施**（组建循环的底子）：M7 账本（31 样本 + 形态 II 分桶 + hits 机读块）= episodic memory；三通道校验器（dc_validator / m7_stats / repo_stats）+ selftest 38/38 = 机械 evaluator；独立 pass 异基座审查臂（RULE-1）= 第二评估者；每批次人工引用 M7 教训 / repo_stats 活靶落档修正 = 人工版反思注入。【依据：docs/M7_EVIDENCE_LOG.md；scripts/ 三校验器；SPEC_PROCESS RULE-1】

【C】**单向性的精确定位**：缺的不是"校验"（校验已闭环），而是**校验失败 → 反思生成 → 持久化 → 注入下一批次**的自动回流环节。当前反思注入完全依赖 LLM 会话记忆 + 人工登记（M7 样本追加工作流 = 手工加行），批次一旦更换会话即丢失。【置信度: ★★★★★】

## 4. 综合分析

### 4.1 关键发现总结

1. loop engineering 的本质 = 把失败从"终止信号"重定义为"下一轮上下文"——与本仓"反形式化审查表演"目标同构。【置信度: ★★★★★】
2. 本仓已具备循环的 80% 底座（M7 账本 / 机械三通道 / 异基座独立 pass / 事件流），缺的是自动回流环节。【置信度: ★★★★★】
3. 循环的反馈信号必须坚持机械信号 + 异基座，不能引入 LLM 自评（MAR 确认偏误实证）。【置信度: ★★★★★】
4. 递归自修改（L3）远未成熟（AI4AI 实证最强者仅 0.250/1.0），须暂缓；人类必须在环收口。【置信度: ★★★★★】

### 4.2 组建循环的收益与代价

**三种循环形态（由轻到重）**：

| 形态 | 机制 | 对应学术/社区参考 | 反馈信号 |
|------|------|-------------------|----------|
| **L1 反思循环**（最轻） | 三通道校验失败 → 自动生成反思文本（失败模式+根因）→ 持久化为 M7 样本 → 注入下一批次 prompt | Reflexion / ERL 启发式抽象 / LangChain trace loop | 机械校验失败输出（exit code + stdout） |
| **L2 账本循环** | M7 账本 hits 机读块 → 自动提取高频失败模式 → 注入 | EvolveR 原则库 / OpenClaw memory | M7 机读块统计（机械重数） |
| **L3 配置循环**（最重） | 自动修改校验规则 / 命令面 | EvoAgentX / Artemis 进化优化 | 基准回归分数 |

**收益**：

- **直接服务仓库核心目标**：失败模式（形式化审查表演、覆盖盲区、计数漂移）成为下一批次结构化输入，同类问题不复发——把 M7 从"审计资产"升级为"学习资产"。
- **改进可度量**：M7 hits 命中率 baseline 成为循环有效性度量（循环有效 = 同族失败不复发 → 命中率下降）。
- **审查降本**：审查臂输入从"人工整理"变为"自动取证 + 反思事件流"（延续 P-025 出路 C 的取证方向）。
- **跨会话记忆**：解决批次换会话即丢失教训的现状（LLM 会话记忆不可靠，事件流可靠）。

**代价 / 风险**（按证据分级）：

- **确认偏误放大**（MAR 实证）：若反馈信号来自 LLM 自评，循环即成为"表演放大环"——本仓的结构性防线 = 三通道机械信号 + 异基座独立 pass，L1 必须只消费机械输出，不得引入 LLM 自评分数。
- **不收敛**：循环需终止条件（迭代上限 / 收敛判定 / 注入量上限），loop engineering 定义即含"直到定义的终止条件"。
- **自我修改引入新幻觉**（AI4AI 实证）：自动化改写统计声明违反"声明=重数"纪律（账本可信度由人工登记 + 机械复验维持）——**人工必须在环**，循环只沉淀"输入材料"（反思文本/失败模式），不自动改账本统计。
- **上下文成本**：31 样本全量注入的 token 开销——需选择性检索（ERL 实证：检索质量比数量重要）。
- **工程成本**：L1 需新子命令（如 `reflect`）+ 反思文本 schema + 注入管线，属 Layer-1 工具层新增，须过 ADR-0010 三问门禁。

### 4.3 结论与建议

【C】**本仓可以组建循环，且应走 L1 反思循环起步**：以机械校验失败输出为唯一反馈信号（反表演防线），反思文本人工在环审阅后登记入账（维护声明=重数纪律），按 P 编号检索注入后续批次 prompt。L2 账本循环次之（hits 机读块已就绪），L3 配置循环暂缓（AI4AI 实证 RSI 未成熟 + 与"声明=重数"纪律冲突）。

【C】**分层归属 = Layer-1 工具层候选**（循环需新子命令与注入管线，非纯概念）；激活条件 = 触发驱动（本调研登记后，无触发不实施）；未激活副作用 = 0（不实施即不存在）。**本次调研止于懒加载 gate，不实施**（同 P-023 先例）。【置信度: ★★★★☆】

## 5. 局限

1. 学术检索以 WebSearch 摘要为取证主源（arXiv 页面直接抓取），未做全文精读；关键论文（Reflexion / MAR / ERL / AI4AI）建议后续吃狗粮时全文核验。
2. loop engineering 概念为 2026-06 新兴词汇，社区定义仍在漂移期，本文以 Kilo.ai 定义 + Addy Osmani 解剖结构为锚。
3. 开源项目快照（stars/版本）为检索时点值，非全量枚举（聚焦循环机制相关项目）。
4. 本调研为 RESEARCH-only 落档，循环功能设计（L1 的具体 schema/命令面/注入管线）留待触发后 DESIGN。

## 6. 关联登记

- **候选登记**（触发驱动，同 drift-gate 先例）：L1 反思循环 = repo_stats 演进 / pattern_lib_version 2 族外的独立候选；M7 账本 hits 机读块 = L2 的现成输入。
- **CER 关联**：loop engineering 与 CER §3.4.1「AGENTS.md 规则源传播生态」「决策产物管线」同属生成端方法论演进观察，本调研为其补充"循环层"视角。
- **不新增 M7 样本**：本调研为零计数声明（无新缺陷发现，零形态 II）。
