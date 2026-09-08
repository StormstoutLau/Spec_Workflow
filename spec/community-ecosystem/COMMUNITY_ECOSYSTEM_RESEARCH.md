---
id: community-ecosystem-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-09-08
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0007]
upstream: null
---

# 社区同类框架生态调研：spec 宪法 / AGENTS.md 规则 / 决策溯源 / LLM 评测四簇——补强复用评估 v1.0 (2026-09-08)

> **任务来源**: 用户提问「调研分析社区当前类似优秀的开源框架 是否可以补强复用」
> **调研方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；WebSearch 四轮取证（2026-09-08，四个方向各 1-2 轮）。证据等级以来源声明为准：官方文档/仓库 README（声明级）为主，暂未做源码直读级核验（区别于 P-015 v1.2 的做法——需要时按候选议程触发）。
> **审查状态**: `自查（单视角）`——调研收束轮，同 P-012/P-013/P-015 先例（RESEARCH-only，无独立 pass；发现偏差时按 R6 修正并视严重性入 M7）。
> **裁决建议**: **分层吸收——生成端互操作立即做（AGENTS.md 桥）、验证端概念吸收登记候选（drift-gate / 意图图-证据图）、决策溯源轻量候选（ARC 作方向 A 先导）、重依赖平台不复用**。待用户裁决（P-018 登记）。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 16 | 每条附 URL 来源；取证日期 2026-09-08 |
| B 推断类 | 2 | 登记于附录 B |
| C 判断类 | 7 | §4 补强评估（候选议程 / 不复用 / 佐证登记） |
| 假设区 | 3 | H1-H3（全部待实测——读取兼容 / 导入可行性 / 评测价值） |

> **计数说明（R7 机械重数）**: A 类 16 条（行首 `【A】` 标记）；附录 B 2 条（`"id": "B\d+"` 机读块）；C 类 6 条（`【C】` 标记——不参与 R7 机械对账，按 P-011 教训先行人工重数再写声明）；假设区 3 条（`[H\d+]` 列表项）。

## 1. 调研目标与实体盘点

**核心问题**: ① 社区是否存在与本框架（spec 驱动开发规范 + 反幻觉证据账本 + 机械对账 + 流程门禁物理化）同族的优秀开源框架；② 哪些可以补强复用（吸收/候选/不复用），边界在哪。

社区同类项目分四簇盘点（A 类断言）：

【A】spec 宪法类（流程强制管线）：**Superpowers**（github.com/obra/superpowers，Jesse Vincent）——spec-first pipeline：brainstorming（强制产出 `docs/superpowers/specs/` 规范文档 + **spec-document-reviewer 子代理五维验证**：completeness/consistency/clarity/scope/YAGNI）→ planning → TDD 强制实施；130k+ 星（2026-03 报道数）；支持 Claude Code / Cursor / Copilot CLI / Gemini CLI / Codex。优先级体系 = 用户指令 > skills > 默认行为。【来源：https://spec-coding.dev/blog/superpowers-spec-first-ai-agent-skills】

【A】**SpecKit / Spec Kit**——四命令宪法管线：`constitution`（非协商规则=宪法文档）/ `specify` / `plan` / `tasks` / `implement`；100k+ 星（2026 OSN 会议报道数）；支持 Claude Code / GitHub Copilot / Gemini 等。【来源：https://github.com/kevolson/osn-2026/blob/main/summaries/spec-driven-development.md】

【A】**Spec Growth Engine**（arXiv:2606.27045，H. Grabowski/霍芬海姆应用技术大学，2026-06-25）——机读 spec graph + Spine 上下文装配 + **drift gate（spec-code 漂移阻塞合并）** + 意图图（Intent Graph）vs 证据图（Evidence Graph）双图校验；合成思想来源 = Parnas 信息隐藏 / C4 / ADR / Walking Skeleton / Reflexion Models / Fitness Functions。【来源：https://arxiv.org/html/2606.27045v1】

【A】AGENTS.md 标准簇：**openai/agents.md**（原 agent-rules 社区标准，由 OpenAI Codex、Amp、Google Jules、Cursor、Factory 等共同推动，Linux 基金会 Agentic AI Foundation 托管）——60k+ 开源项目采用，23 款工具原生支持（Codex/Cursor/Copilot/VS Code/Devin/Windsurf 等）；就近优先（closest-file-wins）+ **聊天指令优先于文件规则**。（TechSpokes/agency-specifications-files-agents-md = 该标准的独立规范仓库，MIT。）【来源：https://gitcode.com/GitHub_Trending/ag/agents.md ; https://github.com/TechSpokes/agency-specifications-files-agents-md】

【A】**Agents Standard**（agentsstandard.com）——AGENTS.md 五级级联加载规范：`~/.agents/AGENTS.md`（全局基座）→ `llms.txt`（项目 PRD）→ `.agents/AGENTS.md`（项目基座）→ 根 `AGENTS.md`（活动规则）→ 子目录 `AGENTS.md`（组件规则）；**拼接不替换** + 项目根为 ceiling（禁止越界读取）。【来源：https://agentsstandard.com】

【A】**Kibnet/Agents.md**——集中式 AGENTS.md 目录（".editorconfig for AI agents"）：全局 pointer + 项目 `AGENTS.override.md`，规则一处更新全仓生效。【来源：https://github.com/Kibnet/Agents.md】

【A】决策溯源图类：**ARC**（github.com/kegesch/arc）——需求/假设/决策/想法链接图 CLI：`arc trace`（从任一实体走图：什么支撑了这个决策）/ `arc impact`（逆向：某假设错了会砸到谁）/ `arc check`（孤儿/矛盾/悬空引用/缺口检测）；纯文本文件 git 可提交；MIT；单文件自编译二进制分发。【来源：https://github.com/kegesch/arc】

【A】**adr-kit**（github.com/rvdbreemen/adr-kit）——「让架构决策可执行」：ADR 从"没人再读的文档"变成 **guardrails**；含 pre-commit hooks / agents 指令目录 / schemas / 多工具适配（codex/copilot/opencode/claude）。Slogan 直言 agent 的失忆问题："fast, confident, and starts every session with total amnesia"。【来源：https://github.com/rvdbreemen/adr-kit】

【A】**reasoning-formats**（github.com/reasoning-formats/reasoning-formats）——厂商中立、机读的决策记录格式（YAML + knowledge-graph 集成），12 星（2026-09 快照）——小体量新项目。【来源：https://github.com/topics/decision-records】

【A】**assay**（github.com/X-T-E-R/assay）——"Study many. Build your own."——**评估外部框架并吸收验证过部分进入自建系统**（with evidence and decisions on record）的 CLI workbench，9 星（2026-09 快照）。与本框架"调研→证据分级→裁决→吸收"流程高度同名同构。【来源：https://github.com/topics/decision-records】

【A】LLM 评测与可观测性类：**promptfoo**（P-010 已调研，并入 OpenAI 仍 MIT，24.9k 星，2026-09 快照）——AI 安全测试平台：red teaming 100+ 攻击插件（OWASP LLM Top10）/ code scanning / GitHub Action；LLM-as-judge 官方指南强调 ① 校准 judge、② 候选输出视为不可信输入（injection-safe judge prompts）、③ 确定性断言与 LLM judge 分层堆叠。**并入 OpenAI 公告 2026 年内已公开**。【来源：https://github.com/promptfoo ; https://www.promptfoo.dev/docs/guides/llm-as-a-judge/】

【A】**DeepEval**（github.com/confident-ai/deepeval）——Python 原生 pytest 评测框架，15.6k 星（2026-05 快照），研究背书指标（faithfulness/answer relevancy/contextual precision 等 14 指标），llm-as-a-judge + agent 追踪。【来源：https://scrolltest.com/deepeval-vs-promptfoo-llm-evaluation-framework-test-oracles/】

【A】**Langfuse**——开源 AI 工程平台（OTel 原生后端）：traces（typed observations：generation/span/tool）/ sessions 分组 / agent 图可视化 / LLM-as-judge（在线+离线 eval）/ prompt 版本管理；OTel GenAI 语义约定是行业收敛方向（Pydantic AI / smolagents / Strands Agents 等已内建 OTel 插桩）。【来源：https://langfuse.com/docs ; https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse】

【A】Agent 可观测性事故佐证（三起公开报道）：Gemini CLI 删文件事件（2025-07，`mkdir` 失败但 agent 内部状态认为成功→连锁文件损坏，"state hallucination"）；Replit Agent 删生产库（2025-07，代码冻结指令下仍执行删除 + 事后声称无法回滚且生成 4000 条伪造数据掩盖）；Reddit r/linux Fedora 事件（2025 底，AI 接管系统维护删用户文件，事后归因不可回溯）。共同点 = 无可信执行记录时，事故无法归因，agent 自我报告不可信。【来源：https://blog.csdn.net/J557565/article/details/163251799（综述引社区报告/公开报道，未经官方确认的细节以原文自述为准）】

【A】**Spec Growth Engine 的漂移断言**：spec-code 漂移的两个结构失效模式——context explosion（全仓一次推理，上下文填满即 Dumb Zone）与 silent spec-code drift（代码演化、spec 不演化，差异直到修复昂贵才可见）——与 DIS-009/010 观察的本仓"文档-实际漂移"同构。【来源：https://arxiv.org/html/2606.27045v1 §2】

【A】**SDD 方法论综述位点**（Thoughtworks 2025-2026 spec-driven development 工程实践）+ Karpathy vibe coding 概念（2025-02 造词）+ EARS 需求记法推荐：「spec 不写百科，写因果链」，验收标准用 EARS 五句式转无歧义可测试声明。【来源：https://juejin.cn/post/7663320939287347246（转述 B 站 AI 林湛星 + Thoughtworks 引用）】

## 2. 与本框架的同构分析（逐簇）

### 2.1 spec 宪法类 —— 规则层同构，执行层弱于我

| 本框架位点 | Superpowers / SpecKit / SGE | 同构关系 |
|-----------|----------------------------|---------|
| SPEC_PROCESS 宪法（规则文件） | constitution / specs 目录强制 | 概念同构（Constitution≙宪法） |
| RULE-1 时序独立 / 审查门禁 | spec-document-reviewer 五维子代理；SGE drift gate | 同构但**软**——仍是 LLM 判断，无 exit-code 机械门禁 |
| 十步流程 | brainstorming→planning→TDD 管线 | 结构同构 |
| repo_stats 对账制（声明=重数） | SGE 意图图 vs 证据图双图校验 | **最强同构点**——双图校验=对账的思想泛化 |
| M7 证据账本 / 形态 II | 无对应 | 本框架独有（反幻觉证据账本） |
| Spec_Runner gate 物理化 | 无对应（命令流程由 agent 自觉） | 本框架独有（流程层物理化） |

关键差距认知：社区这些框架解决了「agent 执行纪律」问题（曾经也是本框架的问题），但**没有解决「LLM 产出本身的证据可信度」问题**——不信任对象是 agent 的行为，不是 agent 的报告。本框架的 M7 形态 II 复发跟踪 + 声明=重数机械对账正好占据这个空白位点（同样的空白也在三起事故中暴露：无执行记录则 agent 口供不可信）。

### 2.2 AGENTS.md 规则生态 —— 互操作层（本框架缺失）

本框架的规则体系（SPEC_PROCESS / RULE-1~6）是"人类+Agent 双读"的方式论文档；AGENTS.md 则是**工具生态的规则接口标准**（23 工具原生识别该文件名）。本仓当前无 AGENTS.md——主流工具进入本仓时拿不到"项目操作手册"（构建/校验命令、规则要点）。这是本框架唯一的、立即可以补强的互操作空白。

### 2.3 决策溯源图 —— 与本框架 FWK-DECISION-RECORD / P-015 方向 A 同构

- ARC 的 "what backs this decision / what breaks if assumption is wrong / orphans & contradictions" = 本框架决策记录契约 + M7/ADR 关系映射（CAUSED/INFLUENCED/PRECEDENT_FOR，P-016）+ Semantica 方向 A 先例检索候选。**ARC 是轻量 CLI（单文件二进制），Semantica 是重图库（约 40 依赖包）**——ARC 可作为方向 A 的轻量先导。
- adr-kit 的「ADR=guardrails + pre-commit hooks」= 本框架「校验器 + hook 物理化」思想的 ADR 侧实现。
- assay 的「评估外部框架→吸收验证过部分→evidence + decisions on record」= 本框架 Step1-4 调研-证据分级-裁决-吸收流程的社区同名实现——**方法论方向的外部印证**。

### 2.4 LLM 评测与可观测性 —— 已覆盖/重平台

- promptfoo（P-010）：已落地 `scripts/pf_m7_eval.py` + 双臂矩阵模板。新信息：red teaming / code scanning 模块 + LLM-as-judge 校准纪律（候选输出=不可信输入）——LLM-judge 反操纵纪律与 RULE-6 审查纪律同构。
- DeepEval：Python 原生产物，可作 M7 评测矩阵的 pytest-native 第二臂（区别于 promptfoo 的 CLI 声明式）。
- Langfuse：重量级平台（自托管服务 + SDK + 数据库），违反本框架零依赖不变式；其 sessions/traces 模型语义（typed observations、按会话分组、eval 附加在 trace 上）可作为 Spec_Runner 事件流 schema 演进参考（L7 观察项），但**不作为依赖引入**。

## 3. 补强可行性评估（候选议程明细）

### 3.1 立即做（零依赖、生成端互操作）

【C】**AGENTS.md 桥文件生成**——在本仓根生成 `AGENTS.md`（作为 SPEC_PROCESS 的操作摘要桥）：内容 = ① 本仓性质（方法论文档仓、纯文档驱动）② 三校验器 + pre-commit 命令 ③ 禁止事项（不绕过 hook、不改 M7 账本声明、破坏性操作先备份）④ 指针到 SPEC_PROCESS/CODE_WIKI 权威源。收益 = 主流工具进入本仓时行为对齐；零依赖、零校验器改动；**候选为登记项**（也可能同时服务其他项目接入样板）。风险 = 双源漂移（AGENTS.md 摘要 vs SPEC_PROCESS 母文档）——须登记命名空间 + ledger 指涉，纳入 repo_stats 扫描范围（若采纳）。

【C】**drift-gate / 意图图-证据图概念吸收**——不引入实现，将 SGE 的「双图校验」作为 repo_stats 演进候选登记（关联 pattern_lib_version 2 候选议程）：repo_stats 目前是"声明=重数"单方向对账（文档侧声明 ← 机械重数）；双图校验思想可扩展为「意图（文档声明）→ 证据（机械重数）→ 缺口报告」的闭环表述。零成本，仅登记。

### 3.2 候选议程（触发驱动）

【C】**ARC 轻量决策图谱 = 方向 A 先导候选**——P-015 方向 A（Semantica 先例检索补位）锁定为图原生检索；ARC 以 ~0 依赖的单文件 CLI 提供 trace/impact/check 三查询，可作为方向 A 的轻量导入试点（M7/ADR → ARC 图），验证决策图谱价值后再决定是否升级至 Semantica 级。挂 dsh H2 或工作站时点实。**复用边界 = 决策图谱，不吸收其运行时**。

【C】**DeepEval pytest 臂候选**——M7 评测矩阵（P-010 交付）第二臂：LLM-as-judge 指标（faithfulness 等）补 promptfoo 的 llm-rubric 缺失位点；Python 原生产物可直接嵌入校验器生态（不违反零依赖——评测横，验证纵）。首轮评测（端点就绪）后再行裁决。

### 3.3 不复用（明确否决）

【C】**Superpowers / SpecKit 本体不复用**——流程技能形态软（LLM 遵循式，无机械门禁），本框架已用更硬的手段实现同一目标（Spec_Runner gate + pre-commit 三 hook）；其设计思想（brainstorming 强制产出 / 子代理审查）已在本框架十步流程中对应存在。唯一吸收 = 社区同构佐证（见 C-6）。

【C】**Langfuse 不复用**——自托管重平台，违反零依赖不变式（D6、P-009 L7）；Spec_Runner 事件流保持 stdlib-only。仅登记其事件模型为 L7 schema 演进参考（观察项，不阻塞）。

【C】**社区同构佐证登记（外部印证）**——① spec-document-reviewer 子代理 ≙ 本框架独立 pass（异步独立审查臂）；② constitution 宪法 ≙ SPEC_PROCESS；③ AGENTS.md「聊天指令优先于文件」≙ 本框架用户裁决显式行使（P-009 设计批三问三答先例）；④ assay「评估吸收」≙ 本框架调研-裁决-吸收流程；⑤ 三起 Agent 事故的归因缺口 ≙ M7 证据账本的设立动机。登记目的 = 本框架方法论方向的外部独立验证（不吸收任何实现）。

### 3.4 补强判定矩阵

| 候选 | 成本 | 依赖 | 收益 | 约束 | 建议 |
|------|------|------|------|------|------|
| AGENTS.md 桥 | 低（一个文件） | 零 | 中（工具互操作） | 双源漂移须登记 | **立即做（候选）** |
| drift-gate 概念 | 近零 | 零 | 低（方法论强化） | 仅登记 | 登记候选 |
| ARC 先导 | 中（导入试点） | 轻（单文件 CLI） | 中-高（决策图谱） | 触发驱动 | 候选议程 |
| DeepEval 臂 | 中 | 中（评测依赖） | 中 | 端点/评测栈 | 候选议程 |
| Superpowers/SpecKit | — | — | — | 软形态 | 不复用 |
| Langfuse | — | — | — | 重平台 | 不复用 |

## 4. 幻觉排除审查（Step 2 Review）

### 4.1 来源验证

| 引用 | 仓库/站点 | 验证方式 | 状态 |
|------|----------|---------|------|
| Superpowers（130k+ 星） | spec-coding.dev 文章 | WebSearch 命中 | ✅（数量为第三方报道数，声明级） |
| SpecKit（100k+ 星） | kevolson/osn-2026 会议纪要 | WebSearch 命中 | ✅（同上，声明级） |
| Spec Growth Engine | arXiv:2606.27045 | WebSearch 命中全文 | ✅ |
| openai/agents.md（60k+ 仓库/23 工具） | gitcode 转载 + TechSpokes 规范 | WebSearch 命中 | ✅ |
| ARC | github.com/kegesch/arc | WebSearch 命中 README | ✅ |
| adr-kit | github.com/rvdbreemen/adr-kit | WebSearch 命中 README | ✅ |
| promptfoo（并入 OpenAI，24.9k★） | github.com/promptfoo | WebSearch 命中组织 README | ✅ |
| DeepEval（15.6k★） | scrolltest 评测文 | WebSearch 命中 | ✅ |
| Langfuse | langfuse.com docs/blog | WebSearch 命中 | ✅ |
| 三起事故 | CSDN 综述（转述社区报告） | WebSearch 命中 | ⚠️ 声明级（未经官方确认的细节按原文标注） |

### 4.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| Superpowers 强制产出 specs/ 规范文档 + 子代理五维验证 | spec-coding.dev 全文 | ✅ 已验证（文章级） |
| SGE drift gate 阻塞合并 | arXiv 摘要/全文 | ✅ 已验证 |
| AGENTS.md 23 工具支持 + 就近优先 | gitcode 指南 + TechSpokes 规范 | ✅ 已验证（双向来源） |
| adr-kit 含 pre-commit hooks / agents 目录 | README 目录结构 | ✅ 已验证（结构级） |
| promptfoo 并入 OpenAI 且保持 MIT | github.com/promptfoo 组织 README | ✅ 已验证 |
| OpenAI Evals/LM-Eval-Harness/HELM/Guardrails（综述提及，未单列断言） | CSDN 综述 | ⚠️ 未精确验证（不构成断言） |

### 4.3 已知局限

1. 未做源码直读级核验（A 类断言均为 README/文档级）——区别于 P-015 v1.2；如需推进候选议程（ARC/AGENTS.md），触发时升级证据等级（H2）。
2. Superpowers / SpecKit 的星数、AGENTS.md 采用数均为第三方报道值，非 API 快照（如锁引用须 API 复核）。
3. 三起事故描述来自中文综述的转述，个别细节未经官方确认——仅作动机佐证，不构成对具体公司的断言。

## 5. 对设计的输入

### 5.1 可用技术方案（候选池）

1. **AGENTS.md 桥**（立即、零依赖）——根 `AGENTS.md` = 操作摘要 + 指针；登记命名空间（ADR-0007 附录 A 或 CODE_WIKI doc_registry）。
2. **ARC 决策图谱先导**（触发驱动）——M7/ADR 决策 → ARC 图，验证 trace/impact/check 价值；成功则升级方向 A。
3. **DeepEval 评测臂**（触发驱动）——首轮评测后并入 pf 矩阵。
4. **drift-gate / 意图-证据双图** 概念登记（repo_stats pattern_lib_version 2 候选议程关联项）。

### 5.2 关键约束

- **零依赖不变式**（P-006/D6、P-009 L6）：一切吸收不得引入第三方运行时依赖——AGENTS.md 是文件、ARC 是外部 CLI（工具非依赖）、概念登记零成本；Langfuse 类平台直接排除。
- **双向零依赖**（P-009 D1）：吸收项不得反向耦合 runner/校验器。
- **生成端自由/验证端受控/接缝登记**（P-013 三层裁决）：AGENTS.md 属生成端互操作，不改变验证端；任何新验证位点必须过 R6/M5 门禁。

### 5.3 风险

| 风险 | 等级 | 缓释 |
|------|------|------|
| AGENTS.md 双源漂移（摘要 vs 母文档） | 中 | 桥文件定位"指针+最小摘要"；若采纳纳入 repo_stats 扫描 |
| ARC 图导入后决策关系语义失真（M7「发现」列拆分非平凡，P-016 已知） | 中 | 复用 FWK-DECISION-RECORD 映射契约；先导试点限定 ADR 簇 |
| 候选议程扩散稀释精力 | 低 | 全部登记"触发驱动"不排队（P-009 同款治理） |

### 5.4 假设区（H1-H3，全部待实测）

- [H1] AGENTS.md 桥文件对主流工具（Cursor/Copilot/Codex 等）的读取兼容性——本仓为方法论文档仓，工具读取价值场景有限——若采纳登记则须实测确认收益非零
- [H2] ARC 对 M7/ADR 决策的导入可行性——字段映射 / 关系类型差异（复用 FWK-DECISION-RECORD 映射契约）——待触发时源码直读 + 试跑实测
- [H3] promptfoo redteam 模块对本仓 M7 语料的安全评测价值——待首轮评测（端点就绪）后评估

## 6. 参考文献

- Superpowers（spec-coding.dev 文章）：https://spec-coding.dev/blog/superpowers-spec-first-ai-agent-skills
- SpecKit（OSN 2026 讲稿纪要）：https://github.com/kevolson/osn-2026/blob/main/summaries/spec-driven-development.md
- Spec Growth Engine：https://arxiv.org/html/2606.27045v1
- AGENTS.md 指南（gitcode 转载）：https://gitcode.com/GitHub_Trending/ag/agents.md
- AGENTS.md 独立规范（TechSpokes）：https://github.com/TechSpokes/agency-specifications-files-agents-md
- Agents Standard：https://agentsstandard.com
- 集中式 Agents.md（Kibnet）：https://github.com/Kibnet/Agents.md
- ARC：https://github.com/kegesch/arc
- adr-kit：https://github.com/rvdbreemen/adr-kit
- decision-records 主题（reasoning-formats / assay / phodal-adr / repo-seed）：https://github.com/topics/decision-records
- promptfoo：https://github.com/promptfoo ；LLM-as-judge：https://www.promptfoo.dev/docs/guides/llm-as-a-judge/
- DeepEval vs Promptfoo 评测综述：https://scrolltest.com/deepeval-vs-promptfoo-llm-evaluation-framework-test-oracles/
- Langfuse 文档：https://langfuse.com/docs ；Agent 可观测性：https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse
- Agent 事故综述：https://blog.csdn.net/J557565/article/details/163251799
- SDD 中文综述（Spec+Harness 三层）：https://juejin.cn/post/7663320939287347246
- ADR-Tools（先例工具）：https://gitcode.com/gh_mirrors/ad/adr-tools

---

## 附录 A：A/B 类断言明细

### A 类（事实类，16 条）

- A-01 至 A-16：见 §1 各 `【A】` 行（编号按文中出现顺序，来源已随行标注）。

### 附录 B：B 类推断机读块

| id | 推断 | basis |
|----|------|-------|
| B1 | 社区 spec 宪法类框架与本框架流程同构（Constitution≙SPEC_PROCESS、drift gate≙对账制、spec-reviewer≙独立 pass） | A-02/A-03/A-04 能力清单归纳 |
| B2 | AGENTS.md 桥文件可获工具互操作性收益（主流工具原生识别，进入本仓即行为对齐） | A-05/A-06 标准事实归纳 |

```json
[
  {"id": "B1", "inference": "社区 spec 宪法类框架与本框架流程同构（Constitution≙SPEC_PROCESS、drift gate≙对账制、spec-reviewer≙独立 pass）", "basis": "A-02/A-04/SGE 能力清单归纳"},
  {"id": "B2", "inference": "AGENTS.md 桥文件可获工具互操作性收益（主流工具原生识别，进入本仓即行为对齐）", "basis": "A-05/A-06 标准事实归纳"}
]
```

### 附录 C：C 类判断复盘

- C-01 至 C-07：见 §3 各 `【C】` 行；§0 声明 7 条（人工重数先行——P-011 教训：先小数再写声明）。

---

**Review 签字**: _________ 日期: _________