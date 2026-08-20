---
id: langgraph-upgrade-RESEARCH
type: design
version: 1.1
status: in-review
date: 2026-08-18
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0005, ADR-0007]
upstream: null
---

# LangGraph 框架化升级调研报告 v1.0 (2026-08-18)

> **任务来源**: 用户提问"是否可能将当前工作流升级为 LangChain/LangGraph 等 agent 开发框架，收益与代价是什么"
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 15 | 每条附 URL + 可核对引文（WebSearch 取证，2026-08-18）；v1.0 §2 主体 11 条 + v1.1 §8 补充 4 条 |
| B 推断类 | 3 | B1-B3，登记于附录 B |
| C 判断类 | 6 | §6 决策分析 4 条 + §8.3 补充裁决 2 条 |
| 假设区 | 6 | H1-H6，未取证声明 |

> **计数修正记录（R7 机械重数，2026-08-18）**: v1.0 初版声明 A=14 系手填错误——`grep -c '【A】'` 实测 v1.0 主体为 **11** 条（虚报 +3）。v1.1 补充 4 条后登记 **15**。**形态 II 第五实例**（计数凭印象，同 P2-1/P2-3 模式），发生在"反幻觉方法论自己的调研报告"上——RULE "统计表计数必须脚本生成"（框架 v1.4 R7）再次被实证为必要。已入账 **M7 样本⑩**（2026-08-19 存量补登——写作时自称候选⑦，惟 ⑦ 已被 precommit-dc-validator 复验占用，治理收束轮裁决实登为⑩）。**复核补记（2026-08-18）**：`grep -c '【A】'` 原始命中 **16**——本行自引用（命令行里的 `【A】` 字符）贡献 +1，剔除此行后为 15。机械重数工具对自引用不免疫——该观察未单列样本，已作为样本⑩ 附随观察入账（[M7 §1](../../docs/M7_EVIDENCE_LOG.md)；⑨ 已被 P-007 实施轮占用，2026-08-19 治理收束裁决）。

**扫描范围声明**: 覆盖 LangGraph 官方文档（interrupt/persistence/thinking-in-langgraph 三页）+ 4 份独立生产复盘 + 1 篇 NeurIPS 2025 论文 + 反框架证据 4 源。未覆盖：LangGraph 源码实测、Pydantic AI 官方文档、本仓库 PoC 实测。

---

## 1. 调研问题

1. Spec_Workflow 的 10 步流程映射到 LangGraph 的成本与贴合度如何？
2. 框架化带来的核心收益是什么，能否量化？
3. 代价与风险是什么，哪些与仓库现有身份冲突？
4. 替代路径（纯 Python runner / 维持现状）的相对位置？

## 2. 核心发现

### 2.1 映射可行性：概念对齐度极高

【A】LangGraph 的三原语与本工作流的门禁机制一一对应——官方文档定义节点为"discrete steps"、条件边做路由、`interrupt()` 实现人工审批：
(源: https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph.md; 引文: "you will first break it apart into discrete steps called **nodes**... connect nodes together through a shared **state**")

【A】`interrupt()` + checkpointer 支持跨会话暂停/恢复（数小时或数天）：
(源: https://docs.langchain.org.cn/oss/python/langgraph/interrupts; 引文: "当触发中断时，LangGraph 会使用其持久化层保存图状态，并**无限期等待**，直到你恢复执行")

**映射表**：

| Spec_Workflow 概念 | LangGraph 对应物 | 对齐度 |
|---|---|---|
| Step 1-10 | nodes（约 12 个含审计回环） | 高 |
| Step 2/4/6/8 Review 门禁 | `interrupt()` + `Command(resume=...)` | **极高**——门禁从"文档纪律"变"物理阻断" |
| RULE-1 时序独立 | 图引擎强制（无法同次写入越门） | 结构性消灭 M6 失效模式 |
| RULE-5 异构审查 | 每节点绑定不同模型（LM Studio 三机端点） | 高——已有基础设施 |
| Step 10 审计回环（P1 清零） | conditional edge 循环 | 高 |
| 四文档产出 | state schema（TypedDict）字段 | 中 |
| 取证矩阵 E1-E5 | checkpointer 轨迹（每节点状态快照） | 中——见 §4.4 代价 |

### 2.2 收益（正反证据并存）

【A】生产复盘（230 万文档/日管线，LangChain→LangGraph 迁移 6 个月）量化收益：
(源: https://communities.stackinsight.net/community/aitr-langgraph/migrated-from-langchain-to-langgraph-6-month-report-on-stability-and-cost/; 引文: "reducing total pipeline failures by approximately **70%**" / "cut our mean time to resolution (MTTR) for processing faults by **over half**" / "consistent **15-20% increase** in sustained documents per second")

【A】同报告的诚实账目——LLM 成本不变、可观测性需自建：
(源: 同上; 引文: "**LLM Costs: Remained effectively flat** per document" / "You must instrument your own logging and metrics within each node. The framework provides structure but **not visibility out-of-the-box**")

【A】MAST（NeurIPS 2025 D&B，1642 条轨迹 × 7 框架）直接支撑本工作流的设计直觉——**带显式验证器的系统失效更少，增加高层目标验证带来 +15.6% 改进**：
(源: https://arxiv.org/abs/2503.13657; 引文: "failure rate on 7 state-of-the-art (SOTA) open-source MAS **41% to 86.7%**" / 评述源 https://christophermeiklejohn.com/ai/agents/mas-series/2026/04/27/mas-series-04-wave-two.html; 引文: "Systems with explicit verifiers (MetaGPT, ChatDev) had fewer failures" / "Adding high-level objective verification gave **+15.6 percent** improvement")

**B1**（见附录 B）：Spec_Workflow 的 RULE-6 取证矩阵正是 MAST FC3 类（task verification，占失效 21%）的结构性防御——框架化会把这层防御从纪律变成代码。

### 2.3 代价与风险

【A】生产部署复杂度——五个必须同时解决的问题：
(源: https://rapidclaw.dev/blog/deploy-langgraph-production-tutorial-2026; 引文: "Durable state that survives crashes and redeploys. Checkpoint storage that multiple workers can share. Horizontal scaling... Observability at the node level... Safe guardrails against recursion" / "LangGraph is a joy in a notebook and a **nightmare on a Friday night deploy**")

【A】调试税与序列化陷阱（双份生产实证）：
(源: https://www.kalviumlabs.ai/blog/langgraph-vs-langchain-production/; 引文: "LangGraph's debugging story is still **worse than a custom loop**" / "We've hit this twice: once with a Pydantic v2 model that used a custom serializer, once with a numpy array... Both caused **silent failures** that only surfaced when trying to resume a paused session")

【A】框架层反对证据——Anthropic 自身立场与 Octomind 弃用案例：
(源: https://zenvanriel.com/ai-engineer-blog/ditching-langchain-for-plain-python/; 引文: "Anthropic recently shared something revealing: **most successful AI companies don't use frameworks** for their agents... **Octomind, after 12 months of using LangChain in production, made the decision to drop it entirely**")

【A】生态活性下降（LangChain 主库，非 LangGraph）：
(源: https://www.banandre.com/blog/collapse-of-langchain-decline-agent-frameworks-shift-leaner-llm-architectures; 引文: "According to the LLM Development Landscape 2.0 report from Ant Open Source, LangChain, LlamaIndex, and AutoGen now rank among the **'steepest declining' projects** by community activity")

【A】API 稳定性历史污点：
(源: https://www.unpromptedmind.com/langchain-llamaindex-plain-python-architecture/; 引文: "LangChain has **broken API compatibility more than once**. If you're not pinning versions, a `pip install --upgrade` will break your production system")

【A】多步复合失败算术（对 10 步流程直接适用）：
(源: https://layerlens.ai/blog/compounding-failure-math-agents; 引文: "If each step in a multi-step agent fails at rate f, the probability that a complete N-step run succeeds is **(1 - f)^N**... At 5% per-step failure rate: 10 steps: **40% of runs fail**")

### 2.4 身份冲突（本仓库特有代价）

【C】Spec_Workflow 的核心资产是**模型无关性**：当前任何 agent（GLM/DeepSeek/Claude/Trae 会话）都能执行工作流，因为宪法是 Markdown。框架化后执行器变成"Python 运行时 + LangGraph 特定版本"，可移植性与"纯文档仓库"定位（CODE_WIKI："本仓库只管流程不管代码"）直接冲突。B4 探针见附录 B。

## 3. 收益汇总（对准本仓库痛点）

| # | 收益 | 证据强度 | 对应痛点 |
|---|------|---------|---------|
| 1 | 门禁物理化：RULE-1 由纪律变代码强制 | 定义级对齐 | M6 并发自查已真实发生 |
| 2 | 跨会话状态持久：interrupt + checkpointer | A 类（官方文档） | **本会话两次被压缩摘要**——会话态即痛点 |
| 3 | RULE-5 原生化：节点级模型绑定 | 高（LM Studio 三机已有） | S1 复验靠手动切基座 |
| 4 | 失效下降参照：70%（管线类，2.3M docs/日规模） | ⚠️ 单实例且规模远大于本场景 | — |
| 5 | 审计轨迹自动化：每节点快照 ≈ 免费 E2 证据 | B 类推断 | 取证矩阵目前手工维护 |

## 4. 代价汇总

| # | 代价 | 严重性 |
|---|------|--------|
| 1 | 部署五件套（durable state/Postgres/可观测/护栏/蓝绿） | 高——单人维护者是主要成本承受者 |
| 2 | 调试比自制循环更差（kalvium 实证）+ 序列化静默失败陷阱 | 高 |
| 3 | 仓库身份逆转：纯文档→代码依赖，模型无关性丧失 | 高（对本仓库是存在级） |
| 4 | LangChain 生态 API 稳定性污点（LangGraph 本体较健康但同生态） | 中 |
| 5 | 10 步流程形状偏线性（~12 节点、主流顺序、4 门禁、1 回环）——纯 Python 状态机 + JSON 状态文件 + git 可覆盖 ~80% 收益 | 中（机会成本） |
| 6 | 单实例生产数据（错误率 -38% 的金融审查案例）不可外推 | 低 |

## 5. 三方案对比

| 维度 | A. 整体迁移 LangGraph | B. 薄壳纯 Python runner（独立仓库） | C. 维持现状 + 增量自动化 |
|------|----------------------|-----------------------------------|------------------------|
| 门禁物理化 | ✅ interrupt() 原生 | ✅ 显式 `--gate` 命令 + 状态文件锁 | ❌ 靠纪律 |
| 跨会话状态 | ✅ checkpointer | ✅ JSON state + git commit | ❌ 会话压缩丢态 |
| 异构审查 | ✅ 节点绑模型 | ✅ HTTP 调 LM Studio 端点（已有） | ⚠️ 手动切基座 |
| 代码量/维护 | ~800-1500 LOC + 框架版本 pin + 部署五件套 | ~500-1000 LOC，零框架依赖 | 0（仅扩 assertion_audit.py） |
| 模型无关性 | ❌ 绑定 LangGraph 运行时 | ⚠️ 绑定 Python 但框架无关 | ✅ 完全无关 |
| 与 Anthropic "no framework" 指引一致性 | ❌ | ✅ | ✅ |
| 失败模式引入面 | 框架抽象层 + 序列化陷阱（A 类实证） | 自写循环的 bug 面 | 无新增 |

## 6. 决策分析（C 类判断）

【C】**主判断：不整体迁移。方法论仓库保持纯文档；若需自动化，走方案 B（薄壳纯 Python runner，独立仓库），LangGraph 作为方案 B 触发条件后的升级路径而非起点。**理由链：
1. 本工作流的最大风险不是"缺框架"而是"门禁被绕过 + 会话态丢失"——前者用 500 行显式门禁命令即可物理化，后者用 JSON+git 即可持久化（Octomind/Anthropic 实证支持无框架路线）
2. MAST 数据反向支撑：带显式验证器的门禁式管线（而非自由多智能体）本就是失效最少的形态——现有方法论已是正确形状，缺的只是执行器
3. 仓库身份（纯文档宪法、模型无关、单人维护）与框架绑定的冲突是存在级的，收益不足以对冲
4. LangGraph 真正的差异化能力（水平扩展、多 worker 共享检查点、子图编排）在单用户场景用不到

【C】**触发条件（何时值得引入 LangGraph）**：方案 B 运行后出现以下任一——(a) 状态管理本身成为瓶颈（条件分支/回环数翻倍以上）；(b) 跨会话恢复成为高频日常操作且 JSON 状态文件出错 ≥2 次/月；(c) 需要 S1 异构复验完全自动化跑批（≥每周一次）。届时 runner 的图结构可 1:1 平移（node 函数签名不变），迁移成本受控。

【C】**无论如何都值得做的零成本项**：把 M7 账本的样本追加也做成 E1 脚本化（`grep -c` 重数已有先例），这是现状方案 C 的自然延伸，不依赖任何框架决策。

## 7. 局限性与诚实声明

1. 本报告未做 PoC 实测——所有收益/代价均为文献级证据，未在本仓库工作负载上验证
2. LangGraph 版本活性好于 LangChain 主库（banandre 数据针对 LangChain/LlamaIndex/AutoGen 三者），本报告未单独取 LangGraph 的社区活性数据
3. 生产复盘中 -70% 失效、-38% 错误率均为单实例叙事（各自注明），不可外推
4. 本报告自身为 `自查（单视角）`（RULE-4）；附录 B 已备好，可交异基座复验

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "Spec_Workflow 的 RULE-6 取证矩阵是 MAST FC3 类失效（task verification, 21%）的结构性防御；框架化将把这层防御从纪律变成代码，预期降低 FC3 类失效",
    "op": "transitivity",
    "claimed_chain": [
      {"step": 1, "text": "MAST 实证 FC3 占多智能体失效 21%（premature 6.2% + incomplete 8.2% + incorrect 9.1%）", "source": "arXiv:2503.13657 Fig.1"},
      {"step": 2, "text": "MAST 实证显式验证器系统失效更少，+15.6% 改进", "source": "christophermeiklejohn.com Wave 2 评述"},
      {"step": 3, "text": "RULE-6/取证矩阵 即显式验证器的文档形态；代码化后成为结构性强制", "source": "本仓库 SPEC_PROCESS v1.4"}
    ],
    "sources": [
      {"label": "MAST paper", "path": null, "url": "https://arxiv.org/abs/2503.13657", "quote": "41% to 86.7% failure rate"},
      {"label": "MAST 评述", "path": null, "url": "https://christophermeiklejohn.com/ai/agents/mas-series/2026/04/27/mas-series-04-wave-two.html", "quote": "Systems with explicit verifiers had fewer failures"}
    ],
    "probe": {"type": "existence", "files": ["SPEC_PROCESS.md"], "params": {"symbols": ["RULE-6", "取证矩阵"], "claim": "present"}}
  },
  {
    "id": "B2",
    "conclusion": "LangGraph interrupt()+checkpointer 直接解决本工作流的跨会话状态丢失痛点（本调研会话自身被压缩摘要两次，即现场实例）",
    "op": "causal",
    "claimed_chain": [
      {"step": 1, "text": "interrupt 触发时持久化图状态并无限期等待", "source": "docs.langchain.org.cn/oss/python/langgraph/interrupts"},
      {"step": 2, "text": "Trae 会话压缩导致上下文摘要、状态衰减（本对话两次 summary 即实例）", "source": "会话现场观察"},
      {"step": 3, "text": "外部化状态（checkpointer 或 JSON+git）使流程推进不依赖会话存续", "source": "推断"}
    ],
    "sources": [
      {"label": "interrupts 文档", "path": null, "url": "https://docs.langchain.org.cn/oss/python/langgraph/interrupts", "quote": "保存图状态，并无限期等待"}
    ],
    "probe": {"type": "existence", "files": [], "params": {"symbols": ["conversation compaction", "session summary"], "claim": "observed-in-current-session"}}
  },
  {
    "id": "B3",
    "conclusion": "纯 Python 薄壳 runner 可覆盖整体迁移约 80% 的收益，因 10 步流程形状偏线性（~12 节点、4 门禁、1 回环），LangGraph 的差异化能力（水平扩展/多 worker/子图）在单用户场景闲置",
    "op": "equivalence",
    "claimed_chain": [
      {"step": 1, "text": "Anthropic 指引与 Octomind 案例支持无框架路线", "source": "zenvanriel.com"},
      {"step": 2, "text": "本工作流图形状：枚举 SPEC_PROCESS 10 步 + 4 Review + 1 审计回环", "source": "SPEC_PROCESS v1.4"},
      {"step": 3, "text": "线性主导形状下自制状态机与 StateGraph 表达力等价（差异在运维层）", "source": "推断"}
    ],
    "sources": [
      {"label": "no-framework 证据", "path": null, "url": "https://zenvanriel.com/ai-engineer-blog/ditching-langchain-for-plain-python/", "quote": "most successful AI companies don't use frameworks"}
    ],
    "probe": {"type": "counting", "files": ["SPEC_PROCESS.md"], "params": {"pattern": "Step \\d+|Review|门禁", "expected": "线性主导"}}
  }
]
```

## 附录 C: 假设区

- [H1] LangGraph 社区活性与 API 稳定性显著优于 LangChain 主库（本报告未单独取证）— 查证路径: GitHub stars/commits 趋势 + CHANGELOG breaking 标记计数
- [H2] 方案 B 的 ~500-1000 LOC 估算准确（未做 PoC 拆解）— 查证路径: 写 runner 骨架实测
- [H3] LM Studio 三机端点可直接作为 runner 的异构模型池（SSH_OPENCODE_SETUP.md 佐证但未在 runner 语境实测）— 查证路径: curl /v1/chat/completions 三端点连通性测试

---

## 8. 补充调研：开源组件的最高 ROI 改进（v1.1 新增，2026-08-18）

> **任务来源**: 用户追问"是否有某种最高 ROI 的改进，借助开源社区的组件提升框架性能"
> **"性能"的界定**: 本仓库是方法论仓库，性能 = **已实证痛点的解除效率**。按 M7 账本与形态 II 分桶排序痛点，对准找组件——不引入无人使用的"能力"，只为已付费的失效模式买单。

### 8.1 候选组件证据（A 类）

【A】pre-commit + front-matter 校验是 2026 社区标准做法，三个独立先例（含"现有验证器全部漏过 YAML 解析错误"的实证）：
(源: https://github.com/webbertakken/takken.io/pull/239; 引文: "The colon after `work` made YAML treat the next line as a mapping key. Prettier formats this without complaint, so **nothing caught it until the build blew up**" / 源: https://github.com/ievo-ai/skills/issues/119; 引文: "This bug survived **all existing validators and code review** because none of them parse YAML frontmatter" / 源: https://github.com/paullukic/coograph/issues/6; 引文: "every `SKILL.md` ... must have YAML frontmatter with `name` ... and `description`" / "Link checker — `lychee` over all `*.md` files. Validates relative paths exist")

【A】promptfoo：MIT 开源评测 CLI，声明式 YAML，本地优先（隐私），50+ provider 含本地模型，CI/CD 原生；2026-03 被 OpenAI 收购但承诺保持 MIT + model-agnostic（35 万开发者，Fortune 500 渗透 >25%）：
(源: https://www.promptfoo.dev/docs/intro/; 引文: "Private: This software runs completely locally... **test-driven LLM development**, not trial-and-error" / 源: https://recatools.com/ai-directory/promptfoo/; 引文: "OpenAI acquired the company in March 2026 but Promptfoo stays **MIT-licensed, model-agnostic**")

【A】LiteLLM：40k stars、100+ provider 统一 OpenAI 兼容接口，SDK 模式零依赖、proxy 模式需 PostgreSQL+Redis；2026-03 曾有供应链安全事件（v1.82.7/1.82.8）：
(源: https://www.seaflux.tech/blogs/explore-litellm-effortless-ai-projects/; 引文: "**40,000 GitHub stars, 1,300+ contributors, and 240 million Docker pulls**" / "In March 2026, LiteLLM disclosed a **supply chain security incident** affecting versions 1.82.7 and 1.82.8" / 源: https://markaicode.com/architecture/litellm-multi-provider-routing/; 引文: "it's not the right starting point for a small team calling one API directly")

【A】Langfuse：MIT 开源 LLM 可观测平台，自托管 Docker Compose ~5 分钟，OTel 原生，100+ 集成：
(源: https://langfuse.com/handbook/chapters/why; 引文: "You can self-host it... All product capabilities... are **MIT licensed without any usage limits**" / 源: https://blog.csdn.net/weixin_42681866/article/details/156492088; 引文: "自托管可部署至内网集群，数据本地存储**无云端依赖**")

### 8.2 ROI 矩阵（痛点对准 × 成本 × 身份兼容）

| 组件 | 对准的已实证痛点 | 成本 | 仓库身份兼容 | ROI 判定 |
|------|----------------|------|-------------|---------|
| **pre-commit + DC 契约校验器** | 形态 II（M7 实证 11 处，规律③④明说拦截层是 E1 机械枚举而非 LLM 自查）+ DC1-DC4 执行 | ~半天，~100 行 Python + `.pre-commit-config.yaml`，零运行时零部署（本地 hook + GitHub Actions 双跑） | ✅ git 元工具，非应用框架 | **最高** |
| **promptfoo**（M7 对比臂评测） | S1 异构复验手动切基座（P-004 刚经历）；M7 样本积累慢（N=6，人工登记） | 一个 YAML 配置 + ~半天学习；本地跑，LM Studio 端点可直接当 provider | ✅ 独立 CLI，不侵入仓库 | 高 |
| **LiteLLM SDK 模式**（非 proxy） | RULE-5 异构模型池统一（三机端点 + 云端 API 一套接口） | ~50 行配置；⚠️ 需 pin 版本（供应链前科） | ⚠️ 引入依赖，属方案 B 配套 | 中 |
| **Langfuse 自托管** | 取证矩阵 E2 证据自动生成（span 即证据） | Docker 服务常驻 + SDK 装饰器改造 | ❌ 违背纯文档仓库身份 | 中低（后置到方案 B） |

### 8.3 最高 ROI 裁决（C 类判断）

【C】**最高 ROI = pre-commit + DC 契约校验器（含形态 II 计数机械检查）**。理由链：

1. **命中最高频已付费痛点**：形态 II 在 M7 账本登记 11 处、4 条复发规律，且规律③（"拦截层是 E1 机械枚举，非 LLM 自查"）与规律④（"审计修正自身含计数错误"）都是本仓库自己的实证——目前唯一拦截手段是事后人工 grep 重跑（P2-1/P2-3 均由此发现）。校验器把"事后审计发现"前移为"提交瞬间拦截"——OpenMMLab 先例的论证（源: https://github.com/open-mmlab/pre-commit-hooks）：修复成本在本地 1 秒 vs CI 失败后的 amend/push/协调
2. **输入已就绪**：P-003 刚完成 DC1-DC4 改造，全仓 21 个文件已带七字段 front-matter——校验器的完整输入刚铺好，边际成本正是最低点
3. **与最高调的反框架证据完全一致**：Anthropic "no framework" 指引针对的是 agent 编排框架；pre-commit 是 git 层元工具，不引入运行时、不绑定模型、不需要部署——纯文档仓库身份零损耗
4. **社区已验证的标准模式**：三个 2026 独立先例（takken.io / coograph / ievo-ai skills）证明"front-matter 校验 + markdownlint + 链接检查"三件套是文档仓库的成熟做法

**校验器最小检查集**（直接从仓库既有裁决派生，零新发明）：

```yaml
检查项（源自）:
  - front-matter 可解析为 YAML（ievo-ai 先例：现有工具全漏过此错误）
  - 七字段齐全 + type/status 取值在 DC2 词表（ADR-0007 D4/D5）
  - id 全仓唯一（DC4）
  - 统计表计数 = grep 机械重数（框架 v1.4 R7 规则——形态 II 计数检查）
  - 相对链接可解析 / 断链标 DC3 档位标注（P-003 刚清理完的债）
```

【C】**次高 ROI = promptfoo 做 M7 对比臂声明式评测**：M7 账本是本仓库独有的方法论资产，但样本积累靠人工（6 样本/4 天）。promptfoo 的 `promptfooconfig.yaml` 把"同一报告 × 同基座/异基座审查"变成声明式测试矩阵，本地直调 LM Studio 端点，结果直接喂 M7 登记——测试驱动开发的哲学与 SPEC_PROCESS 同构（它的口号就是 "test-driven LLM development"）。**触发条件**：M7 样本积累到 ≥10 或 S1 复验频次升到月级时启动。

### 8.4 补充结论对主报告的影响

主报告 §6 判断不变且被加强：方案 B（薄壳 runner）的排序提前于任何框架——因为最高 ROI 改进（pre-commit 校验器）甚至**先于方案 B**，在现状（方案 C）下即可执行，且不与任何未来路径冲突（校验规则即 DC 契约的机器可读定义，runner 与 LangGraph 路线都将复用）。

## 附录 D: 补充调研假设区（v1.1）

- [H4] pre-commit 校验器可在 Trae/主控站 Windows 环境顺畅运行（pre-commit 官方支持 Windows，但未在本机实测）— 查证路径: `pip install pre-commit && pre-commit run --all-files` 实测
- [H5] promptfoo 的 LM Studio provider（openai-compatible 接入）对审查类长文本 prompt 的成本/延迟可接受（未实测）— 查证路径: 单次 S1 复验场景 PoC
- [H6] GitHub Actions 免费额度对本仓库的校验器 workload 足够（文档仓库，无构建，预期远低于限额）— 查证路径: 接入后观察一个月

---

**Review 签字**: _________ 日期: _________（本报告为 `自查（单视角）` 产出，按 RULE-4 须经独立 pass 复核后方可标记 `[已复核]`）
