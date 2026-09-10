---
id: community-ecosystem-RESEARCH
type: design
version: 1.23
status: in-review
date: 2026-09-08
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0007, ADR-0010]
upstream: null
---

# 社区同类框架生态调研：spec 宪法 / AGENTS.md 规则 / 决策溯源 / LLM 评测四簇——补强复用评估 v1.23 (2026-09-10)

> **任务来源**: 用户提问「调研分析社区当前类似优秀的开源框架 是否可以补强复用」+ 补充提问「当前工作流规定了流程 但每个步骤比如调研 审查 设计方案 实施方案等具体步骤 社区是否有类似的框架 skill MCP工具可以补强 同时当前是否可以强制要求每个步骤给出决策 引用信息依据 提供给下一轮审查」
> **调研方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；WebSearch 六轮取证（2026-09-08，四方向 + 本轮步骤级工具两方向）。
> **审查状态**: `自查（单视角）`——调研收束轮，同 P-012/P-013/P-015 先例（RESEARCH-only，无独立 pass）。
> **v1.23 变更（编排重构批，用户指令「这份文档需要重构一下 顺序 编排 请分析」+ 裁决 = 保守收敛 + 压缩移附录）**: **结构重构（零内容丢失、编号框架全不动**——§2.2/§2.5/§3.1/§3.4/§3.4.1/§3.5/§4/§5.3/§5.4 等外部引用保持稳定）：① **21 条逐轮变更日志（v1.2~v1.22 mega-line）压缩为下方「§0.1 版本历史摘要表」**，逐轮详细日志原文迁附录 D（可追溯性保留）；② **新增目录（TOC）**；③ **新增 §3.0 候选状态总表**（单一权威位点，§3.4 矩阵 + §3.4.1 + §5.1 状态叙事改为指针引用）；④ **§5.1 候选池指针化**（指向 §3.4 矩阵消除双源维护）；⑤ 版本 1.22→1.23。**断言计数不变（36/4/14/4——纯结构编排，零新增断言/零内容删改）**。逐轮详档见 [附录 D](#附录-d变更日志详档v122--v12-迁入)。
>
> ## 目录
>
> - §0 断言统计表（审计入口）
> - §0.1 版本历史摘要表（v1.1→v1.23 一句话要点）
> - §1 调研目标与实体盘点（A-01~A-16）
> - §2 同构分析（2.1 spec 宪法 / 2.2 AGENTS.md 生态 / 2.3 决策溯源 / 2.4 LLM 评测 / 2.5 步骤级工具盘点 / 2.6 兼容与可行性矩阵）
> - §3 补强可行性评估（3.0 候选状态总表 / 3.1 立即做 / 3.2 候选议程 / 3.3 不复用 / 3.4 补强判定矩阵 / 3.4.1 候选逐项深入调研 / 3.4.2 hook 面独立评估 / 3.5 强制决策产物管线 / 3.6 每阶段定制 agent / 3.7 全环节增强工具全景 / 3.8 多工具吸收方法论）
> - §4 幻觉排除审查（4.1 来源验证 / 4.2 技术声明验证 / 4.3 已知局限）
> - §5 对设计的输入（5.1 候选池 / 5.2 关键约束 / 5.3 风险 / 5.4 假设区）
> - §6 参考文献
> - 附录 A 断言明细 / 附录 B 推断机读块 / 附录 C 判断复盘 / **附录 D 变更日志详档（v1.22→v1.2 迁入）**
>
> ### 0.1 版本历史摘要表（v1.23 新增；逐轮详档 = 附录 D）
>
> | 版本 | 时点 | 主题/批号 | 一句话要点 | 计数变化 |
> |------|------|----------|-----------|---------|
> | v1.1 | 2026-09-08 | 初版四簇盘点 + 步骤级工具盘点 | 四簇框架盘点 + §2.5 步骤级工具 + 补强裁决初版；A 25/B 3/C 12/H 4 | —（基线） |
> | v1.2 | 2026-09-08 | 吃狗粮 review 深度审计轮 | 1P1+2P2+8P3 修正（C 10→12 实为重数，M7 样本 ㉙）+ 新增 §2.6 兼容矩阵 | C 修正 12 |
> | v1.3 | 2026-09-08 | ADR-0010 验收之二落地轮 | §3.4 矩阵补「分层归属（Q1）」列，6 候选批量预演，闭环验收条件 | 不变 |
> | v1.4 | 2026-09-08 | Ponytail 补充调研批 | §2.5 增代码实现步骤子节 + A-26；插件不复用，7 级阶梯概念吸收（Layer-0） | A 26 / C 13 |
> | v1.5 | 2026-09-08 | 候选池深入调研批 | 新增 §3.4.1 候选逐项核验；ARC 升优先候选待裁决；ADR Kit 双仓确认 | 不变 |
> | v1.6 | 2026-09-08 | §3.4/§3.4.1 吃狗粮审计轮 | 6P2+5P3 修正（Ponytail 版本锁 v4.8.x / B3 编号同步 / 引用修正） | 不变 |
> | v1.7 | 2026-09-08 | P-020 step-gate 落地轮 | 矩阵「每步决策产物管线」行更新为已吸收（step-gate 三件套 + spec_runner v1.1.0） | 不变 |
> | v1.8 | 2026-09-08 | 吸收状态同步轮 | AGENTS.md 桥 P-021 已吸收 + 决策管线 P-020/A/C 出路 P-024/P-025 全落地 | 不变 |
> | v1.9 | 2026-09-09 | §2.6 可行性判定补充调研批 | 四路取证清晰判定（u14app 可行 / Alibaba 不复用 / AAT 可行 / Gigaxity 不可行）+ step-gate 吃狗粮实证 | 不变 |
> | v1.10 | 2026-09-09 | hook 面扩展独立评估批（P-030） | 新增 §3.4.2；分层 hook + --no-verify 旁路 + 6 禁事项矩阵；Q2 未满 → 不实施 | 不变 |
> | v1.11 | 2026-09-09 | 审查修复轮 | hook 口径统一四 hook（M7 样本 ㉜㉝） | 不变 |
> | v1.12 | 2026-09-09 | 状态同步轮 | drift-gate 已实施（P-029）+ ADR 三层评估已执行（P-030） | 不变 |
> | v1.13 | 2026-09-09 | ARC 试点调研批（P-031） | ARC 行评估已执行——本机实测 0.x 缺陷双实证 + H2 部分证伪，试点待裁决 | 不变 |
> | v1.14 | 2026-09-09 | ARC 替代框架调研批（P-032） | 6 候选全景无完全替代，ARC 保持主选（规避命令面 + 等 1.0） | 不变 |
> | v1.15 | 2026-09-09 | ARC 选型对比批（P-033） | 加权评分 = ARC 升级 4.2 显著最优，单维补位仅辅助观测 | 不变 |
> | v1.16 | 2026-09-09 | ARC 缺陷规避方案批（P-034） | 规避矩阵（二进制直链/版本固化/白名单/预链接/停滞观察）+ A-11 事实修正；采用资质确认 | 不变 |
> | v1.17 | 2026-09-09 | ARC 升级实施批（P-035） | 规避矩阵落地 tools/arc/ + data/.arc 8 ADR 图；ARC → Layer-1 已实施 | 不变 |
> | v1.18 | 2026-09-09 | 假设区状态同步轮 | H1 已随 P-021 激活 / H2 已实测（部分证伪 + P-035 规避落地） | 不变 |
> | v1.19 | 2026-09-09 | promptfoo 首轮评测懒加载批（P-036） | H3 已研判评测价值低；端点不可达；Q2 未满 → 止于懒加载 gate | 不变 |
> | v1.20 | 2026-09-10 | 每阶段定制 agent 可行性批 | 新增 §3.6 环节-工具映射；阶段 agent 可行（学术+生态双实证） | A 30 / B 4 / C 14 |
> | v1.21 | 2026-09-10 | 全环节增强工具扩展批 | 新增 §3.7 全景（调研/审查两链补证 STORM/Cloudflare 等） | A 33 |
> | v1.22 | 2026-09-10 | 工具吸收方法论批 | 新增 §3.8 五问（适配/边际/去重/防缝合/对齐；OSS 选型 + Agent Atlas + ToolScope + OPENTOOLS） | A 36 |
> | v1.23 | 2026-09-10 | 编排重构批（本次） | 结构重构：TOC + 版本史表 + §3.0 状态总表 + §5.1 指针化 + 日志移附录 D；编号框架全不动 | 不变 |
> **裁决建议**: 不变（分层吸收 + §3.5 强制决策产物管线可行且优先；v1.5 增补：ARC 升级为优先候选待用户裁决）。待用户裁决（P-018 登记）。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 36 | 每条附 URL 来源；取证日期 2026-09-08（v1.1 +9 条步骤级工具；v1.4 +A-26 ponytail；v1.5 无新增行首断言——ARC 快照就地修订 A-10；v1.20 +A-27~A-30 每阶段定制 agent 五路取证；v1.21 +A-31~A-33 全环节工具链补证；v1.22 +A-34~A-36 工具吸收方法论多轮取证） |
| B 推断类 | 4 | 登记于附录 B（v1.20 +B4 阶段化 agent 可行性推断） |
| C 判断类 | 14 | §3.1-3.3 补强评估 10 条 + §3.5 强制决策产物管线裁定 3 条 + v1.20 +C14 阶段化 agent 分层判定（v1.2 修正：v1.1 声明 10 实为 12，M7 样本 ㉙；v1.4 +1 Ponytail 判定；v1.22 工具吸收方法论不涉新裁定，C 14 不变） |
| 假设区 | 4 | H1-H4（H1/H2/H3 已实测已闭合——读取兼容 P-021 / ARC 导入 P-031+P-035 / red team 价值 P-036 已研判；H4 仍待触发——MCP 服务形态） |

> **计数说明（R7 机械重数）**: A 类 36 条（行首 `【A】` 标记）；附录 B 4 条（`"id": "B\d+"` 机读块）；C 类 14 条（`【C】` 标记——**不参与 R7 机械对账，按 P-011 教训先行人工重数再写声明；v1.1 声明 10 实为 12 由 v1.2 吃狗粮 review 重数捕获（M7 样本 ㉙）；v1.4 +1 C（ponytail 判定）人工重数核对；v1.5 + v1.6 无新增行首断言，重数 26/13/4 复核通过（v1.6 吃狗粮审计轮机械复核）；v1.20 +A-27~30 +B4 +C14 人工重数核对 = 30/4/14 通过；v1.21 +A-31~33 人工重数核对 = 33/4/14 通过；v1.22 +A-34~36 人工重数核对 = 36/4/14 通过**）；假设区 4 条（`[H\d+]` 列表项）。

## 1. 调研目标与实体盘点

**核心问题**: ① 社区是否存在与本框架（spec 驱动开发规范 + 反幻觉证据账本 + 机械对账 + 流程门禁物理化）同族的优秀开源框架；② 哪些可以补强复用（吸收/候选/不复用），边界在哪；③（v1.1）每个流程步骤（调研/审查/设计/实施）的具体执行是否有社区框架/skill/MCP 可补强；④（v1.1）可否强制每步产出「决策 + 引用依据」供下一轮审查。

社区同类项目分四簇盘点（A 类断言，A-01~A-16）：

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

### 2.5 步骤级工具盘点（v1.1 新增：答题主问「每步骤的具体执行」）

社区对「步骤级执行」的补强可分三大类（A-17~A-26；v1.2 修正措辞——v1.1 写"三类"但当时实际只列两类，§2.5 原审缺失；v1.4 增「代码实现步骤」子节成三类）：

#### 调研/发现步骤（Step 1 调研 → 弹药层）

【A】**gpt-researcher**（github.com/assafelovic/gpt-researcher，29.2k 星 2026-09 主题页快照 / 27.2k 星 mcpgee 快照；MCP 侧版本 **v1.0.0、2026-05-22 更新、维护状态 active**）——开源深度研究代理：**规划者-执行者架构**（planner 生成研究问题 → 爬虫执行代理收集 → publisher 汇总；多代理流水线含 **Reviewer「研究-审核-修正」循环**——材料不达标打回，v1.2 补取证）；生成带引用（20+ 来源汇总）的客观报告；提供 MCP server 形态（GTP Researcher MCP，规划者-执行者 + 上下文优化）。**兼容取证（v1.2，直接答本仓可行性）**：官方文档明确支持自定义 OpenAI 兼容端点（`OPENAI_BASE_URL` 指向本地 OpenAI 兼容服务 + `FAST_LLM/SMART_LLM/STRATEGIC_LLM=openai:*`）→ **三机 LM Studio（OpenAI 兼容，P-009/P-010 已实测）可直接接**；搜索轴 `TAVILY_API_KEY` 可替换为 duckduckgo/google/bing/searchapi/serper/**searx**（含本地 SearXNG，免商业 key）；运行门槛 Python 3.11+。【来源：https://github.com/topics/deepresearch ; https://cloud.tencent.com/developer/mcp/server/11518 ; https://docs.gptr.dev/docs/gpt-researcher/llms（OPENAI_BASE_URL） ; https://www.mcpgee.com/servers/gpt-researcher（v1.0.0/27,217★）】

【A】**Alibaba-NLP/DeepResearch**（github.com/Alibaba-NLP/DeepResearch，19.9k 星）——Tongyi Deep Research，开源深度研究 agent（信息检索式，web-agent）。【来源：https://github.com/topics/deepresearch】

【A】**u14app/deep-research**（4.7k 星）——任意 LLM 深度研究，**支持 SSE API + MCP server 形态**（可直接接入 MCP-capable agent）。【来源：https://github.com/topics/deepresearch】

【A】**Gigaxity Deep Research**（github.com/yoloshii/gigaxity-deep-research，53 星，MIT）——MCP 深度研究流水线：六工具（search/research/discover/synthesize/reason），**多源搜索 + RRF 融合 + 引用绑定 + 矛盾检测**；synthesize 带 CRAG 式质量门 + 大纲引导；可实现本地推理（local-inference 分支换 vLLM/SGLang/llama.cpp）。**「引用绑定 + 矛盾检测 + 质量门」三要素与本框架证据分级 + M7 复发跟踪语义同构度最高**。【来源：https://mcprepository.com/yoloshii/gigaxity-deep-research】

【A】**Academic Agent Toolkit（AAT）**（github.com/JhonHander/academic-agent-toolkit，MIT）——**一条命令为多个 agent（Claude Code/OpenCode/Cursor/Copilot/Codex）统一安装学术研究 skills + Paper Search MCP**（20+ 学术源：arXiv/PubMed/Semantic Scholar/Crossref…+ PDF 下载）+ 实验协议设计/可复现性验证。**与本框架 P-007 校验器多工具适配、P-018 AGENTS.md 桥属同一形态**。【来源：https://github.com/JhonHander/academic-agent-toolkit】

【A】**Agent Leaderboard**（github.com/jaychempan/Agent-Leaderboard，agentskills.media）——**发现入口**：500+ Agent Skills / 1500+ MCP Servers / 1100+ Prompt Libraries / 100+ Auto Research 排行榜，自动按星数更新。【来源：https://github.com/jaychempan/Agent-Leaderboard】

#### 决策强制/审查衔接步骤（Step 4 裁决 → 强制层）

【A】**adr-governance**（github.com/ivanstambuk/adr-governance）——**ADL（Architecture Decision Log）= 机器可读 source of truth**：CI 管线对代码库强制执行 ADR——"closing the gap between deciding and doing"（决策与代码的闭合循环）；含 .githooks / schemas / CI / ADR author skill。【来源：https://github.com/ivanstambuk/adr-governance】

【A】**ADR Kit**（github.com/kschlt/adr-kit，MIT）——**三层分阶段 enforcement**：pre-commit 查导入限制（<5s）→ pre-push 查架构边界（<15s）→ CI 全量复跑；**lint rules 直接从 ADR 生成**（require/forbid 模式）；决策演进**只 supersede 永不编辑**（保留全历史）；质量门拒绝模糊决策（"use a modern framework" 类直接拒）。【来源：https://github.com/kschlt/adr-kit】

【A】**ADR 侵食三层防御模式**（社区实践文章，wakatchi.dev 2026-05）——「ADRs are eroded」对策：① ADR 禁止事项显式化到标识符级（如 `plan_tier` 列禁止新代码引用）→ ② 静态检查脚本（git diff 差分扫描违规引入）→ ③ CI/pre-commit 自动执行 + PR 模板自查清单——**人工（ADR 本文 + PR 清单）与机械（检查脚本 + CI）双防线，不依赖 reviewer 记忆**。【来源：https://wakatchi.dev/adr-guardrails-as-code/】

#### 代码实现步骤（Step 5-7 实施 → 生成端防过度工程）

【A】**Ponytail**（github.com/DietrichGebert/ponytail，**v4.8.x**（v1.4 记录 v4.8.4 / v1.5 核验 release v4.8.3@2026-06-24——多源差异，锁区间声明），MIT，147 commits，2026-06-26 活跃）——**"懒惰资深开发者"规则集 + 插件形态**（非模型/非独立工具/非框架）：跨 16+ AI 代理平台（Claude Code/Cursor/Copilot/Codex/Gemini/OpenCode/Windsurf/Pi…）工作。核心 = **7 级决策阶梯**——写代码前停在第一个成立的阶梯：① YAGNI（这东西需要存在吗？不需要就跳过）→ ② 代码库已有？复用之 ← ③ 标准库能做？用它 → ④ 原生平台功能？用它 → ⑤ 已装依赖能解？用它 → ⑥ 一行能搞定？一行 → ⑦ 以上都不行才写最少能工作的代码。**关键纪律 = 阶梯在理解问题之后运行（对解决方案懒惰，对阅读理解从不懒惰）**；Bug 修复 = 根因而非症状（修前 grep 每个调用者）；安全/信任边界/数据丢失处理/可访问性 = 不可偷懒区。附带 5+1 skills（`ponytail` 懒惰模式 / `ponytail-review` 过度工程审查 / `ponytail-audit` 全仓库过度工程审计 / `ponytail-debt` 技术债收集）+ 3 lifecycle hooks + MCP 形态（ponytail-mcp 高级）。**基准测试**（真实 Claude Code headless，编辑 tiangolo/full-stack-fastapi-template，12 功能任务，Haiku 4.5，n=4）：代码量 **-54%**（最高 -94%）、token -22%、成本 -20%、速度 -27%、安全性 100%（vs 基线 95%）。**与本框架同构度**：7 级阶梯 = 本框架「纯文档 + 最小工具层」哲学 + ADR-0010 懒加载门禁（Layer-0 优先于 Layer-1 的生成端镜像）+ CODE_WIKI「薄壳不膨胀」；ponytail-review/audit = 本框架独立 pass / repo_stats 对账的生成端对照（审查过度工程）；ponytail-debt = DEV-LOG 技术债登记形态。【来源：https://github.com/DietrichGebert/ponytail ; https://blog.csdn.net/yanceyxin/article/details/162553680 ; https://openclawapi.org/en/blog/2026-06-21-ponytail-overengineering-fix】

【A】**mattpocock/skills（A-27）**——Matt Pocock 开源工程 skill 集（aihero.dev 出品，TypeScript 教育者），2026-04-末发布→2026-08-30 **~241k stars**，MIT，459 commits，25 skills；跨 Claude Code（官方 marketplace 插件 mattpocock-skills）/Cursor/Codex/Copilot；**主链 = `grill-with-docs → to-spec → to-tickets → implement → code-review`**（想法→ship 主干）；关键设计 = SKILL.md 懒加载（description 常驻 ~100 tokens/个，body 仅 invoke 载入）+ **TDD phase gate**（/tdd：Red 测试真失败才允许 Green，phase gate 非 prompt nudge）+ /research（引用 + 一手源）+ /wayfinder（决策地图）+ /ask-matt（路由）。【来源：https://github.com/mattpocock/skills ; https://www.aihero.dev/skills ; https://www.shareuhack.com/ja/posts/claude-code-community-skills-agent-fleet-guide-2026（241k★ 快照）】
【A】**Spec Kit Agents（A-28）**——学术多 agent SDD 管线（arXiv:2604.05278v1，Pardis Taghavi/Santosh Bhavani）：GitHub Spec Kit 四阶段加 **phase-level context-grounding hooks**（每阶段前只读 discovery 探测仓库 + 阶段后 validation 校验中间产物）；**128 runs/32 features/5 仓库实证：LLM-judge 复合质量 +0.15（1-5 量表，Wilcoxon p<0.05），SWE-bench Lite 58.2% Pass@1（基线 +1.7%），测试兼容性 99.7-100%**。【来源：https://arxiv.org/pdf/2604.05278v1】
【A】**Spec-Kit 生态分阶段 skills（A-29）**——GitHub Spec Kit 原生四阶段 workflow（specify/plan/tasks/implement + plan review gate）；社区衍生 Spec-Kit Antigravity 展开为 **17 skills**（clarify/constitution/specify/migrate/analyze/plan/tasks/taskstoissues/**quizme**（红队找缺口）/implement/tester/reviewer/checker/validate/status/diff/checklist）跨 Antigravity/Claude Code（.agent↔.claude 互转）；**addyosmani/agent-skills** 六阶段七命令（/spec /plan /build /test /review /ship）+ 20 skills（spec-driven-development PRD 先于代码等）跨 Claude/Cursor/Copilot/Gemini/Windsurf/OpenCode。【来源：https://github.com/compnew2006/Spec-Kit-Antigravity-Skills ; https://agskills.dev/addyosmani/agent-skills/spec-driven-development】
【A】**AGENTIC-STACK（A-30）**——obviousworks Claude-AI-skills-collection 推荐栈（2026-07）：Superpowers + Pocock 组合四阶段（Clarify→Specify→Implement→Debug-Review = brainstorming+grill-with-docs / writing-plans / tdd / systematic-debugging+diagnose）；明确 4 层架构（CLAUDE.md / Skills / Subagents / Hooks = 概率约束→确定性强制分层）；Pocock 选中 = grill-with-docs + caveman + diagnose。【来源：https://github.com/obviousworks/Claude-AI-skills-collection-2026/blob/main/AGENTIC-STACK.md】

#### 与十步流程的映射

| 十步流程 | 已有的本框架执行件 | 社区可补强（候选） |
|---------|------------------|------------------|
| Step 1-2 调研+复验 | WebSearch/MCP（已直测：paper-search/stackexchange/english-search，P-013） | gpt-researcher / Gigaxity / AAT Paper Search MCP（MCP 服务形态，H4 待实测） |
| Step 3 设计 | DESIGN 模板 + 决策契约 | adr-kit guardrails（候选）、Superpowers brainstorming 技能形态 |
| Step 4 裁决 | 用户/评审裁决 + M7/ADR 登记 | adr-governance enforcement loop（概念印证）、ADR 侵食三层防御（模式吸收候选） |
| Step 5-7 实施+校验 | TDD + IMPLEMENTATION/CHECKLIST + 三校验器 + pre-commit hook | Superpowers TDD skill 形态（生成端）、ADR Kit 三层 hook 分阶段（候选）、**Ponytail 7 级阶梯（生成端防过度工程——概念吸收候选）** |
| Step 8-10 独立 pass+收束 | RULE-1/RULE-5 审查臂 + Spec_Runner gate | spec-reviewer 子代理（同构印证）、promptfoo/DeepEval 评测臂（候选） |

### 2.6 兼容与可行性矩阵（v1.2 新增：答「可行性 版本 兼容」盲区）

| 工具 | 三机 LM Studio OpenAI 兼容端点 | 搜索轴要求 | 版本/维护 | 环境门槛 | 可行性判定 |
|------|------------------------------|-----------|-----------|---------|-----------|
| gpt-researcher | ✅ **官方支持**（OPENAI_BASE_URL，A-17 v1.2 取证） | Tavily（免费额）或 duckduckgo/searx+ 等（可免商业 key） | MCP v1.0.0 / 2026-05-22 / active | Python 3.11+ | **可行（触发驱动，H4 实测后接）** |
| Gigaxity Deep Research | ✅（local-inference 分支换 vLLM/SGLang/llama.cpp，OpenAI 兼容） | 默认 OpenRouter（云端 key）；本地分支可 | 53★ / MIT（版本号未见） | Python 3.11+ / FastAPI | **不可行（v1.9 判定）**——Qwen3-30B-A3B 合成模型重资源 + Exa/Brightdata 外部 key 依赖；gpt-researcher 已覆盖同功能且更轻 |
| u14app/deep-research | ✅ 未证到**已核验**（v1.9：README 明示 "any OpenAI Compatible LLMs" + Ollama + OpenRouter，含 Atlas Cloud——三机 LM Studio 可接） | ✅ **Searxng 本地轴**（v1.9 核验：支持 Searxng/Tavily/Firecrawl/fastCRW/Exa/Bocha/Brave） | **v1.0.0 @ 2026-05-21 / 维护 active / MIT**（v1.9 核验，4.6k★） | Node.js 18+ + pnpm/npm/yarn（Docker 可选）；MCP 形态 streamable-http+SSE / SaaS / PWA | **可行（v1.9 判定，触发驱动）**——本地数据处理 + OpenAI 兼容端点 + 本地搜索轴，MCP 形态适配调研链；**安全提示：SSRF 漏洞 issue #153 未修** |
| Alibaba DeepResearch | 未核验（通义 30B-A3B 模型经 OpenRouter 托管有免费档；但本仓判定已排除） | — | 19.4k★ / Apache-2.0 / **repo 2026-02 起停滞**（v1.9 核验：唯一发布 2025-09 30B-A3B；spring-ai-alibaba 变体 = Java 栈 2026-02 停滞） | 30B-A3B 模型推理（重资源）或 Java/Spring AI 栈 | **不复用（v1.9 判定）**——训练级模型方案超出调研弹药层定位 + repo 停滞；轻量替代 = u14app/gpt-researcher |
| AAT | n/a（只装 skills+MCP，不跑 LLM） | n/a | **PyPI v0.1.2 / MIT**（v1.9 核验，18 commits） | **Python 3.11+ + uv**（`uvx academic-agent-toolkit` 免安装直跑） | **可行（v1.9 判定，生成端互操作，触发驱动）**——一键装 skills + Paper Search MCP（20+ 学术源）跨 agent 配置；**与既有 mcp_paper-search 重叠 → 可选，不优先** |
| ARC | n/a（CLI 图查询） | n/a | **v0.8.0 / 161 commits / 0 依赖（v1.5 快照核验）** | 任意 OS 单文件二进制 | 升级为优先候选（P-020 后触发） |
| adr-governance / ADR Kit | n/a | n/a | kschlt/adr-kit v0.2.x（CHANGELOG 0.2.7 锚，声明级） | git hooks / Python | 模式印证（不强引；吸收点并入 P-020） |
| Ponytail（v1.4） | n/a（规则集无需端点） | n/a | **v4.8.x / MIT / 147 commits / 2026-06-26 active**（v1.5 核验：release v4.8.3@06-24，v1.6 统一锁区间） | 跨 16+ agent 平台规则（无运行时依赖） | **概念吸收（Layer-0）——插件本体不引入** |
| promptfoo（P-010） | ✅（双臂模板端点运行时注入，已实测） | n/a | 24.9k★ / 并入 OpenAI / MIT | CLI | 已落地 |

> v1.6 更新版盲区登记（v1.9 再更新）：v1.5 快照已核验 **ARC（v0.8.0）/ kschlt-adr-kit（v0.2.x）/ Ponytail（v4.8.x）** 版本；**v1.9（2026-09-09）再核验 u14app（v1.0.0@2026-05-21）/ AAT（PyPI v0.1.2）/ Alibaba DeepResearch（19.4k★ 但 repo 停滞）/ Gigaxity（53★ 无版本号）**——四个模糊项判定已落地（可行×2 / 不可行×2）；剩余无版本号标注 = **gpt-researcher MCP（v1.0.0 已标注）** + Gigaxity（已排除）——采纳任一前须 P-015 v1.2 式源码/API 直读核验（§4.3 局限 5）。

## 3. 补强可行性评估（候选议程明细）

### 3.0 候选状态总表（v1.23 编排重构新增：单一权威位点）

> **v1.23 说明**: 本节汇总全部候选的**当前状态**（截至 v1.23），作单一权威位点；§3.4 判定矩阵、§3.4.1 逐项调研、§5.1 候选池中的状态叙事均为**指针引用**，改状态只改本节 + 对应 P 落档，不再散落各节。逐轮状态演变见 §0.1 版本史表 + 附录 D 详档。

| 候选 | 当前状态 | 分层（ADR-0010 Q1） | 权威取证/落档 | 对应批次 |
|------|---------|---------------------|---------------|---------|
| AGENTS.md 桥 | **已实施**（2026-09-08） | Layer-0 | §3.1 C-01 + §3.4 矩阵 | P-021 |
| 每步决策产物管线（step-gate） | **已实施**（P-020 + ADR-0011 A/C 出路 P-024/P-025 全落地） | Layer-1（契约 Layer-0） | §3.5 三裁定 + §3.4 矩阵 | P-020/P-024/P-025 |
| drift-gate / 意图-证据双图 | **已实施**（2026-09-09 缺口报告落地） | Layer-0→Layer-1 | §3.1 C-02 + spec/drift-gate/ | P-023/P-029 |
| ARC 决策图谱 | **已实施**（Layer-1 生成端辅助查询，2026-09-09） | Layer-1 | §3.4.1 ARC 行 + spec/arc-rollout/ | P-031~P-035 |
| DeepEval 臂 / 调研链 MCP | **吃狗粮评估已执行，资质达标但止于懒加载 gate**（P-037，2026-09-10——端点已就绪但评测样本库未建；触发 = 评测样本库就绪/用户指定首用例；独立落档 spec/deepeval-arm/） | Layer-1 | §3.2 C-04 + spec/deepeval-arm/ | P-010/P-037 前向 |
| ADR 三层 enforcement | **评估已执行，不实施**（Q2 未满，登记观察项） | Layer-0（模式） | §3.4.2 + spec/hook-surface/ | P-030 |
| Ponytail 7 级阶梯 | 概念吸收候选（Layer-0 仅登记） | Layer-0 | §2.5 实施子节 + §3.2 C-07 | — |
| 每阶段定制 agent 工具 | Layer-0 概念登记 + 生成端候选（零引入） | Layer-0 | §3.6 + A-27~A-30 | v1.20 调研轮 |
| 全环节增强工具 | Layer-0 概念登记（逐环节映射表） | Layer-0 | §3.7 + A-31~A-33 | v1.21 调研轮 |
| 多工具吸收方法论 | Layer-0 概念登记（五问框架） | Layer-0 | §3.8 + A-34~A-36 | v1.22 调研轮 |
| Superpowers / SpecKit / Langfuse / gpt-researcher 本体 | **不复用**（D6 先例，不过门禁） | 不适用 | §3.3 C-08/09/10 + §3.4 矩阵 | — |

### 3.1 立即做（零依赖、生成端互操作）

【C】**AGENTS.md 桥文件生成**——在本仓根生成 `AGENTS.md`（作为 SPEC_PROCESS 的操作摘要桥）：内容 = ① 本仓性质（方法论文档仓、纯文档驱动）② 三校验器 + pre-commit 命令 ③ 禁止事项（不绕过 hook、不改 M7 账本声明、破坏性操作先备份）④ 指针到 SPEC_PROCESS/CODE_WIKI 权威源。收益 = 主流工具进入本仓时行为对齐；零依赖、零校验器改动；**候选为登记项**（也可能同时服务其他项目接入样板）。风险 = 双源漂移（AGENTS.md 摘要 vs SPEC_PROCESS 母文档）——须登记命名空间 + ledger 指涉，纳入 repo_stats 扫描范围（若采纳）。**→ 已吸收（P-021 done，2026-09-08：根 AGENTS.md 落地（五段式，零可漂移声明 I-1）+ ADR-0010 三问 Layer-0/生成即激活/副作用 0 审核通过）**。

【C】**drift-gate / 意图图-证据图概念吸收**——不引入实现，将 SGE 的「双图校验」作为 repo_stats 演进候选登记（关联 pattern_lib_version 2 候选议程）：repo_stats 目前是"声明=重数"单方向对账（文档侧声明 ← 机械重数）；双图校验思想可扩展为「意图（文档声明）→ 证据（机械重数）→ 缺口报告」的闭环表述。零成本，仅登记。**→ 已登记（P-023 done，2026-09-09：ADR-0010 三问 Layer-0/触发驱动/副作用 0 全过，spec/drift-gate/ 两件套落档）→ 已实施（P-029 done：repo_stats「意图→证据→缺口」缺口报告落地 = `CheckResult.gap` 三元组 + `_gap_report()` 块 + pattern_lib_version 2 激活，2026-09-09，v1.12 状态同步）**。

### 3.2 候选议程（触发驱动）

【C】**ARC 轻量决策图谱 = 方向 A 先导候选**——P-015 方向 A（Semantica 先例检索补位）锁定为图原生检索；ARC 以 ~0 依赖的单文件 CLI 提供 trace/impact/check 三查询，可作为方向 A 的轻量导入试点（M7/ADR → ARC 图），验证决策图谱价值后再决定是否升级至 Semantica 级。挂 dsh H2 或工作站时点实。**复用边界 = 决策图谱，不吸收其运行时**。

【C】**DeepEval pytest 臂候选**——M7 评测矩阵（P-010 交付）第二臂：LLM-as-judge 指标（faithfulness 等）补 promptfoo 的 llm-rubric 缺失位点；Python 原生产物可直接嵌入校验器生态（不违反零依赖——评测横，验证纵）。首轮评测（端点就绪）后再行裁决。

【C】**gpt-researcher / Gigaxity / AAT 调研链候选（v1.1 新增）**——调研步骤弹药层补强：gpt-researcher（29.2k★，规划者-执行者 + 引用报告）与 Gigaxity（MCP、引用绑定 + 矛盾检测 + 质量门）为候选登记；AAT 的「跨 agent 统一安装 skills+MCP」形态本身印证 AGENTS.md 桥方向。均触发驱动（H4 端点/服务形态实测后）；**不引入重依赖**——gpt-researcher 本体是独立服务，接入形态 = MCP 调用而非库依赖。【来源：A-17/A-20/A-21】

【C】**ADR 三层 enforcement 模式吸收候选（v1.1 新增）**——「ADR 禁止事项显式化 → 静态检查 → CI/hook 自动执行 + 提交自查清单」三层防御与本框架「文档声明 → 校验器 → pre-commit hook」同构，且提供两个补强点：① 禁止事项标识符级显式化（本框架 Spec_Runner gate 的 cmd 是正例命令，缺"禁止性"负例通道的显式登记位点）；② 分阶段 hook（pre-commit 快查/pre-push 慢查）——登记为 gate 演进候选（先不编号，挂 §3.5 P-019 采纳路径一并设计，v1.2 去除自造编号）。**→ v1.10 起触发驱动评估执行（P-030，2026-09-09：hook 面扩展独立评估落档 spec/hook-surface/ RESEARCH v1.1——gate 三问 Q2 激活条件未满 → 不实施，登记 ADR-0010 失效条件②观察项，见 §3.4.2；v1.12 状态同步）**。

【C】**Ponytail 7 级阶梯 = 概念吸收候选（v1.4 新增，用户提问「代码实现阶段 ponytail 是否可复用」）**——判定：**插件/规则集本体不复用**（跨 16+ agent 平台的软形态规则，与本框架纯文档 + 最小工具层身份无运行时贴合，同 Superpowers 不复用先例）；**7 级决策阶梯本身吸收为方法论思想**——① 它是 ADR-0010 懒加载三问门禁的**生成端镜像**（阶梯 ① YAGNI = 三问 Q2 无触发不实现；②-⑤ 复用先于新建 = Q1 Layer-0 优先于 Layer-1；⑥-⑦ 最少代码 = 零副作用纪律），外部项目独立演化出与本框架同一架构约束 = 方法论方向获又一独立印证；② 其「对解决方案懒惰、对阅读理解从不懒惰」= 本框架 Step 2 调研纪律 + 最小工具层的哲学同构；③ ponytail-review/audit 唯一补强位点 = 生成端（写码前）的过度工程自审——本框架现以验证端（ADD 审计 + repo_stats）为主，生成端纪律可作 Step 5-7 增强候选。**分层归属 = Layer-0（概念）**；激活条件 = 触发驱动（若未来在实施阶段补入生成端自审纪律，先登记不实施）。【来源：A-26 + ADR-0010 对应关系（见 §2.5 实施子节）】

### 3.3 不复用（明确否决）

【C】**Superpowers / SpecKit 本体不复用**——流程技能形态软（LLM 遵循式，无机械门禁），本框架已用更硬的手段实现同一目标（Spec_Runner gate + pre-commit 四 hook——三校验器 + step-enforce，P-024 起，2026-09-09 审查追正口径）；其设计思想（brainstorming 强制产出 / 子代理审查）已在本框架十步流程中对应存在。唯一吸收 = 社区同构佐证（见 C-12，v1.2 修正编号错位）。

【C】**Langfuse 不复用**——自托管重平台，违反零依赖不变式（D6、P-009 L7）；Spec_Runner 事件流保持 stdlib-only。仅登记其事件模型为 L7 schema 演进参考（观察项，不阻塞）。

【C】v1.1 确认：**gpt-researcher 等本体亦不复用为库依赖**——报道级服务（独立 agent/python 包）与零依赖不变式冲突；仅保留 MCP 服务形态为触发驱动候选（H4）。

### 3.4 补强判定矩阵

> **分层归属列（v1.3 补注）**: 依 ADR-0010 三问门禁 Q1 批量预演（2026-09-08）——分层 = 事实判定，不随用户裁决改变；"不复用"组已按 D6 等先例否决，不适用门禁。此列闭环 ADR-0010 验收条件之二。

| 候选 | 成本 | 依赖 | 收益 | 约束 | 建议 | 分层归属（ADR-0010 Q1） |
|------|------|------|------|------|------|------------------------|
| AGENTS.md 桥 | 低（一个文件） | 零 | 中（工具互操作） | 双源漂移须登记 | **已吸收（P-021 done，v1.8）** | **Layer-0**（单一文件，零激活成本） |
| **每步决策产物管线**（§3.5，v1.1） | 中（gate 扩展 + 契约） | 零 | **高**（决策全程可追溯/审查有输入） | 契约 & 机械校验须定义 | **已吸收（P-020 done + ADR-0011 A/C 出路 P-024/P-025 全落地，v1.8）** | **Layer-1**（扩展 tools/spec_runner；契约 Layer-0 = FWK-DECISION-RECORD 复用） |
| drift-gate 概念 | 近零 | 零 | 低（方法论强化） | 仅登记 | **已实施（P-029 done，2026-09-09）** | **Layer-0→Layer-1**（P-023 概念登记走后启用 Q2 触发驱动，P-029 实施落地：repo_stats「意图→证据→缺口」缺口报告 + pattern_lib_version 2 激活） |
| ARC 先导 | 中（导入试点） | 零（v1.5 核验 0 依赖） | 中-高（决策图谱） | **P-020 落地后触发**（v1.6 同步 §3.4.1） | **评估已执行（P-031，试点实施待用户裁决）** | **Layer-1**（外部 CLI 工具） |
| DeepEval 臂 / 调研链 MCP | 中 | 中（评测/服务） | 中 | 端点/服务形态 | 候选议程 | **Layer-1**（外部服务/依赖） |
| ADR 三层 enforcement | 低（模式吸收） | 零 | 中（禁止性通道 + 分阶段 hook） | （v1.2 去 G2 编号；吸收点并入 P-020 设计面） | **评估已执行，不实施（P-030，2026-09-09）** | **Layer-0**（纯模式吸收，无运行时） |
| **Ponytail 7 级阶梯**（v1.4） | 近零（概念吸收） | 零 | 中（生成端防过度工程纪律） | 插件本体不复用（同 Superpowers 先例） | 概念吸收候选 | **Layer-0**（方法论思想吸收；插件 = 外部 agent 平台资产不入本仓） |
| Superpowers/SpecKit/Langfuse/gpt-researcher 本体 | — | — | — | 软形态/重依赖 | 不复用 | 不适用（已按 D6 等先例否决，不过门禁） |

### 3.4.1 候选逐项深入调研与清晰建议（v1.5，用户指令「候选项目需要执行深入调研 能够清晰化给出建议」）

> **方法**: 2026-09-08 WebSearch 逐项核验最新快照（npm/GitHub 页面/issues + 多方评测文）；深入调研事实以内联 URL 登记（本子节**不新增行首 A/C 断言**——A/B/C 计数维持 26/3/13/4；大规模事实更新以就地修订 A-10 + 内联取证承载，避免对账漂移）。下表给出每候选「核验快照 → 清晰建议（吸收方式 / 分层 / 优先级 / 下一步）」。

| 候选 | 深入调研核验（v1.5 快照） | 清晰建议 |
|------|--------------------------|---------|
| AGENTS.md 桥 | 生态持续扩大（60k+ 仓库/23 工具/Linux 基金会托管）；**本轮观察 = "规则文件 + agent 适配"已成社区默认传播形态**：ARC 自带 AGENTS.md + skill file、Ponytail 规则源即根 AGENTS.md（~20 行）、ADR Kit 含 CLAUDE.md + .mcp.json + skills。【内联来源：ARC/ponytail/adr-kit 仓库页】 | **已吸收（Layer-0，P-021 done 2026-09-08）**——根 AGENTS.md 落地（五段式 = 性质/流程/校验命令/禁止事项/权威源指针，零可漂移声明 I-1）+ ADR-0010 三问审核通过（Layer-0/生成即激活/副作用 0）。下一步 = 无（登记命名空间 + ledger 指涉已随 P-021 完成）。 |
| 每步决策产物管线（step-gate，P-020） | **三方独立收敛**：ARC ledger-to-driver 路线图（#20：arc next "what should I work on next"，把决策图谱当 agent 驱动源，Phase 1 P0，agent surface = CLI+JSON+skill）；ADR Kit adr_planning_context 的 scenario taxonomy（strategic_planning/focused_implementation/pre_decision/supersession_impact 四场景）+ ContractRelations（supersedes 链/depends_on/related_to 双向索引）；本框架 §3.5 决策事件流。【内联来源：github.com/kegesch/arc/issues/20 ; github.com/kschlt/adr-kit CANONICAL+CHANGELOG】 | **已吸收（Layer-1，契约 FWK-DECISION-RECORD 为 Layer-0）——完整实例化**："决策记录从档案提升为驱动执行的输入"方向三项目独立印证 → P-020 step-gate 落地（2026-09-08：decision 事件 + step-gate 命令 + STEP_GATE_CHECKLIST 三问 8/8）→ **ADR-0011 accepted A+C 两出路全落地**（2026-09-09：P-024 出路 A 流程强制 = pre-commit 第四 hook step-enforce；P-025 出路 C 独立验证 = spec_runner verify-anchor 锚点真实性机械核查 + RULE-1 独立 pass 取证清单）。下一步 = 无（含流程强制与审查取证，本方向闭环）。 |
| drift-gate 概念 | SGE 双图校验（无 v1.5 新信息，arXiv 稳定）。 | **已实施（v1.12 状态同步）**——P-023 概念登记（2026-09-09，Layer-0/触发驱动/副作用 0）后，**P-029 实施落地（2026-09-09）**：「意图→证据→缺口」闭环进入 repo_stats（`CheckResult.gap` 三元组 + `_gap_report()` 块 + pattern_lib_version 2 激活）。下一步 = 无（已闭环）。 |
| ARC 先导 | **重大演进**（2026-09-08 核验）：npm @kegesch/arc v0.8.0（2026-08 下旬发布）/161 commits/**0 依赖**单文件二进制；实体 9 型、关系 14+；命令 arc init/add/trace/impact/check/**next/context**/list；D-045 "Arc answers questions agents cannot answer themselves"；**明确否决 MCP 与插件系统（#3/#11/#13），agent surface = CLI+JSON+skill file**——与本框架"薄壳 CLI + 纯文档 + 生成端自由"身份高度契合；`arc import --from-adr` 支持 ADR 导入（反向工程#15 关闭=由 agent 导入）。【内联来源：npm @kegesch/arc 页；issues #20/#15；README】 | **升级为优先候选（Layer-1，外部 CLI 非依赖）**：① 零依赖单文件二进制 = 与本仓零依赖不变式兼容；② 其 graph-query（trace/impact/check）+ driver（next/gaps）= P-015 方向 A 的**轻量替代**（vs Semantica 多 GB 重栈，增量成本近零）；③ 结构化图查询非语义检索 → **H3 中文召回风险不适用**（比 Semantica 更适配本仓中文语料）。**触发条件已满足（v1.8 更新：P-020 落地 2026-09-08，决策事件流面已就绪——P-024 流程强制 + P-025 锚点取证后事件流更完备）**。**评估已执行（v1.13，P-031）：2026-09-09 吃狗粮试点调研落档 spec/arc-probe/ RESEARCH v1.0**——本机实测 Windows 命令面可用，但 0.x 平台缺陷双实证（版本号失配 0.1.0 vs 0.8.0 / skill 命令 B:\~BUN 路径崩溃 / issue #30 linux bun 缺失）**+ H2 部分证伪（ADR 导入成功但 date=导入日、depends/driven_by 关系全空——「映射最干净」失效，图关系需预链接）**；gate 三问：实施面窄（实体档案 + 预链接）+ 与 step-gate 门禁正交（ARC CI-enforcement 未发布）→ 可作方向 A 轻量先导或保持 Layer-0 观察，**试点实施待用户裁决（同 P-015/P-028 先例）**。**替代调研完成（v1.14，P-032：RESEARCH v1.1）**：6 候选全景核验 + phodal/adr 实测——**无候选在「关系图谱递归 + 零依赖 agent 面」维度完全替代 ARC，ARC 保持主选**（缺陷处置 = 规避命令面 + 等 1.0）；替代品单维补位观察（adr-explorer 可视化 / adr-kit MCP / phodal/adr Windows 管理 / adr-governance AI 治理）。**选型对比完成（v1.15，P-033：RESEARCH v1.2）**：加权评分矩阵 = **ARC 升级 4.2 显著优于四单维补位**（次高 adr-explorer 3.2 仅只读看板），单维补位仅登记辅助观测。**缺陷规避方案完成（v1.16，P-034：RESEARCH v1.4——用户指令「假设采用ARC 升级如何规避缺陷 深入调研社区信息」）**：§3.8 规避矩阵 = 官方 Windows 二进制直链（v0.8.0 sha256 可校验）+ 版本快照固化 + 命令白名单（排除 skill 崩溃面）+ import 预链接脚本（FWK-DECISION-RECORD 映射）+ 90 天停滞观察项对冲 bus factor=1；**深度复核捕获 A-11 事实错误并修正**（driver 命令 #25/#26 已发布于 2026-06-01/05-31，非「计划中未发布」——A-20/A-21 补证）——**采用资质确认，实施仍待用户裁决**。**【实施完成（v1.17，P-035，2026-09-09，用户指令「按照吃狗粮模型执行ARC 升级 规避缺陷」）】**：规避矩阵落地于 tools/arc/ 薄壳工具链——arc_wrap.py 命令白名单封装器（skill/init-agent 崩溃面拦截 exit 2）+ arc_prelink.py ADR 预链接脚本（depends→depends_on 边）+ 版本 0.8.0 sha256 固化（8f4b3089 与官方一致）+ data/.arc 8 ADR 决策图（7 depends_on 边）；实测发现 link 合法边按实体类型动态决定（--help ≠ 运行时）；trace/impact/check 递归可用；D6 不接门禁（与 step-gate 正交）。**ARC 从「候选待裁决」→「Layer-1 已实施（生成端辅助查询）」**。 |
| DeepEval 臂 | 15.6k 星（2026-05 快照）；无 v1.5 重大变更信息。 | 候选议程（Layer-1）不变——首轮评测（端点就绪）后作 M7 评测矩阵第二臂（pytest-native 补 promptfoo CLI 盲区）。下一步 = 触发驱动。 |
| ADR 三层 enforcement | **双仓独立演化确认**：kschlt/adr-kit（195 commits、MADR、policy 块自动生成 ESLint/Ruff/import-linter/mypy/tsconfig 规则、MCP adr_preflight/create/approve/planning_context、ContractRelations+supersession chains+scenario taxonomy）；rvdbreemen/adr-kit（CER A-08 原记录，v1.6 修正：A-13 实为 Langfuse；dev 539 commits）。两仓独立实现同一"ADR=可执行 guardrail"模式 = 方向已获竞争性验证。**分层 hook 方案已明确（v1.10 补取证）**：`pre-commit` 做**增量快查**（<5s）→ `pre-push` 做**全量/影响域复验**（<15s）→ CI 做**完整兜底检查**；核心思想 = "禁止策略显式落文档 → 工具自动生成正则/lint 规则 → 差分扫描违规引入 → 分层 hook 递进拦截"。【内联来源：kschlt/adr-kit README/TECHNICAL；decision-records 话题页 2026-07-28 快照；wakatchi.dev 2026-05 实操文章】 | **模式吸收候选（Layer-0）不变，吸收点未单独立项（v1.8 更新）**：禁止性负例通道（require/forbid 显式化）+ 分阶段 hook（pre-commit 快查/pre-push 慢查）——P-020 已落地（2026-09-08）但吸收点**未随 P-020 实施**（step-gate 批未含禁止性负例通道），仍为触发驱动候选（不与 step-gate 并列编号）。**后续 hook 面扩展评估已执行（v1.10，见新 §3.4.2 独立评估 + 落档 spec/hook-surface/ RESEARCH v1.1）**。**评估结局 = 不实施（2026-09-09，v1.12 状态同步）：gate 三问 Q2 激活条件未满 → 止于懒加载 gate，登记 ADR-0010 失效条件②观察项（触发 = 连续 3 裁决未引三问 或 真实 --no-verify 旁路失败案例），避免重复评估**。 |
| Ponytail 7 级阶梯 | star 多源声明级差异大（5w+ juejin 2026-06-23 / 16k+ pyshine / 84k+ awesome-prompts——不锁单值）；v4.8.3（2026-06-24 release）+ 147 commits（活跃 06-26）；**ponytail: 注释 = 技术债账本**（/ponytail-debt 收集防"later means never"）；AGENTS.md 即规则源（~20 行）。【内联来源：github.com/DietrichGebert/ponytail；juejin/pyshine/awesome-prompts 评测文】 | **概念吸收（Layer-0）不变**——7 级阶梯 = ADR-0010 生成端镜像（v1.4 已判）；**唯一补强点位登记**：`ponytail:` 注释约定（有意简化的机械可收集标记）可借鉴为本仓生成端"有意简化"登记形态（与 repo_stats 扫描位点兼容），登记为 pattern 演进候选，**不实施**。下一步 = 无（触发驱动）。 |
| 不复用组 + 生态观察 | Superpowers/SpecKit（流程技能软形态）/Langfuse（重平台）/gpt-researcher 本体（服务）——v1.5 维持否决；**新观察**：decision-records 话题同族小体量项目（phodal/adr 271★ 轻量 ADR CLI / watercooler 13★ MCP 共享推理层 / repo-seed 8★ "self-governing repos：AGENTS.md+MADR+deterministic gates+pre-commit hooks"——与本框架门禁物理化同构度最高但未成熟）。【内联来源：github.com/topics/decision-records 2026-09-08 快照】 | 不复用（D6 先例，不过门禁）；repo-seed 等登记为生态观察（不入候选池——体量 <10★，待其成熟再评估）。下一步 = 无。 |

### 3.4.2 hook 面扩展独立评估（v1.10，2026-09-09，P-030——「ADR 三层 enforcement」候选的触发驱动评估）

> **触发**：§3.4.1 ADR 三层行"下一步 = 触发驱动（后续 hook 面扩展时评估）"被用户指令「执行后续 hook 面扩展调研评估」触发；亦与 ADR-0010 失效条件之「连续 3 个吸收裁决未引用三问 → 重审门禁是否需要机械化（hook 级）」候选项同题。
> **方法**：社区 WebSearch 三轮取证（2026-09-09，分层 hook 实践 / --no-verify 旁路与兜底 / forbid-ban 通道形态）+ 本仓禁止事项（AGENTS.md）逐条机械化可行性评估 + ADR-0010 三问懒加载门禁（本候选吸收物 = "hook 面扩展机制"）。
> **结论速览**：hook 面扩展现状 = 4 hook 全在 pre-commit 单层；社区证据显示记录性禁止事项应显式落 policy 块 + 机械扫描；分层（pre-push/CI 兜底）增量价值**有限**；可行性矩阵显示 3/6 禁止事项可机械化、3/6 不可（过程性行为）；**结论 = 仅零星增量，当前不实施，触发登记在案，止于懒加载 gate（Q2 触发条件未满）**——注册为 ADR-0010 失效条件②观察项，避免重复评估。

#### ① 社区分层 hook 实践（预提交快查 / 预推送中查 / CI 兜底）

社区主流实践（Husky / jest / commitlint 等工具生态）与 ADR Kit 的分阶段 enforcement 已形成「分层成本-深度」共识（ADR Kit：pre-commit 查导入限制 <5s → pre-push 查架构边界 <15s → CI 全量复跑）：

- **pre-commit = 本地增量快查层**：只检查**暂存区文件**（`git diff --cached`），<2s 完成，可自动修复（lint-staged 限定范围）。目标 = 拦截明显低级错误，速度优先。
- **pre-push = 本地全量/影响域慢查层**：可检查整个项目或变更影响域，<15s。常用于本地无法低成本完成的完整校验（全量测试/类型检查/架构边界）。
- **CI/PR = 远程完整兜底层**：执行最重最完整的检查（构建/集成/端到端），作为本地 hook 被绕过后的兜底闸门。

wakatchi.dev 的 ADR 侵食三层防御（见 CER §2.5）即禁止事项→差分扫描→pre-commit+CI 的静态检查脚本实现。

#### ② --no-verify 旁路与兜底

git 原生 pre-commit/pre-push 均可被 `--no-verify` 跳过（git 官方文档明示：pre-commit "can be bypassed with the --no-verify option"）。社区实证（[git 官方 githooks 文档](https://git-scm.com/docs/githooks)；[block-no-verify](https://github.com/tupe12334/block-no-verify)——实测 12 种绕过向量全放行：引号拆分 / `--no-veri` 前缀缩写 / `GIT_CONFIG_PARAMETERS` 环境变量注入 / `LEFTHOOK=0` 等 hook 管理器禁用开关）证实：**任何本地 hook 都无法 100% 阻挡绕过**——本地 hook 是"诚实的护栏"，远程/CI 才是真正的强制层。

对纯本地单人仓库（本仓无 CI），这意味着：
- 本地环上优化到极致也只是**最外层**，无法达到绝对强制
- 更现实的定位 = "记录性禁止事项显式化 + 机械扫描证据"，而非"依赖 hook 做最终强制"

#### ③ forbid-ban 通道社区形态

社区禁止性规则的落点形态 = **显式 deny-list 正则文件 + 例外 allowlist**（[git-secrets](https://github.com/awslabs/git-secrets) 扫描 commits/commit messages；[nhsd-git-secrets-precommit](https://github.com/nhsengland/nhsd-git-secrets-precommit) `rules/nhsd-rules-deny.txt`；detect-secrets `.secrets.baseline`）。核心机制：**policy 显式落文档/规则文件 → 工具自动生成可执行检查（正则/lint 规则）→ 激活于 hook/CI → 命中即拒绝**。

- **记录性禁止事项**（如：禁止引入某依赖、禁止使用某 API）→ **可机械化**：搜索 + 阻止 + 例外白名单（允许场景）。社区格式 = `policy 块`（adr-kit）或 `deny.txt 规则文件`（git-secrets）。
- **过程性禁止事项**（如：不得提交前不备份、不得 skip-hook）→ **不可机械化**：tool 执行的环境状态不可机械校验（无法判断"提交前是否备份"），只能文档显式化 + 审查监督。

#### ④ 本仓禁止事项逐条机械化可行性矩阵

本仓 AGENTS.md「禁止事项」共 6 条。逐条评估：

| # | 禁止事项 | 类型 | 机械化可行性 | 现状（已有机械位点） | 候选新增机械位点 |
|---|---------|------|------------|--------------------|----------------|
| 1 | 不得跳过 pre-commit 检查 | 过程性 | **部分**（只能兜底，不能强制；`--no-verify` 旁路） | step-enforce（batch 级，P-024）；全仓四 hook 均 arm（dc/m7/repo 三校验器 + step-enforce） | pre-push 复验（三校验器+step-enforce 全量重跑，拦截被跳过的批次） |
| 2 | 不得手改 M7 账本统计声明（由机械脚本重写） | 记录性 | **完全** | m7-stats hook（M7_EVIDENCE_LOG.md 单文件）+ `--write` 再生成制 | commit-msg/pre-push 复验（防止 edit 后 skip hook） |
| 3 | 破坏性文件操作（覆盖/截断/批量替换）前必须备份 | 过程性 | **不可**（tool 执行环境不可校验；git 只能看最终结果） | 无（依赖审查臂 RULE-1 复核 + git 本身可回滚） | 不可机械拦截——保持生成端纪律 + 审查臂监督 |
| 4 | 文档计数声明必须与机械重数一致（声明=重数） | 记录性 | **完全** | dc-validator（R7 机械重数）+ repo-stats（视图层声明=重数） | pre-push 复验 |
| 5 | 同一文件修改必须严格串行（DIS-008） | 过程性 | **不可**（发生在 agent 编辑流程，工具层不可见） | 无（依赖 agent 遵守 + 编辑工具自身单次请求限制） | 不可机械拦截——Ext 工具调用本身即强制单请求，已天然缓解 |
| 6 | batch 编辑后必须全覆盖终验 grep（不得抽样） | 过程性 | **不可**（agent 行为，工具层不可见） | 无（依赖 agent 遵守；repo-stats/dc-validator 全量扫描近等价兜底） | 不可机械拦截——三校验器全量扫描已近似强制终验 |

**结论**：6 条禁止事项中 **3 条（#1/#2/#4）已机械化或可在现有工具位点内强化**，**3 条（#3/#5/#6）本质上是过程性行为纪律，git hook 层不可机械拦截**。hook 面扩展的增量价值集中在：#1 的 pre-push 复验兜底（拦截 `--no-verify` 旁路的批次）——这是唯一有真实增量的点。

#### ⑤ 结论与建议（gate 三问）

**ADR-0010 三问懒加载门禁（候选吸收物 = "hook 面扩展机制"）**：

- **Q1 放哪层**：若实施 = Layer-1（`.pre-commit-config.yaml`/`.pre-push` hook 配置）。记录性禁止事项的机读显式化（policy 块）= Layer-0。
- **Q2 激活条件**：**未满足**。本仓为纯文档仓，无应用代码库；记录性禁止事项（#2/#4）已机械化，增量仅剩 #1 的 pre-push 复验兜底（防 `--no-verify` 旁路）。但 `--no-verify` 纪律属本仓流程层已强约束项（AGENTS.md + step-enforce），旁路场景实际未发生过（P-020 起吃狗粮全过 hook）。**无真实失败案例 → 触发条件不成立**。
- **Q3 未激活副作用 = 0**：是。不引入任何 hook 改动，三校验器/hook 零变化。

**结论**：hook 面扩展**当前不实施**（零/极小增量），登记为 ADR-0010 失效条件②观察项（若连续 3 个吸收裁决未引用三问，则升级为机械化门禁再评估）。**本次评估本身闭环本候选的"下一步 = 触发驱动（后续 hook 面扩展时评估）"条目**——提供"已评估"替代"未评估"的确定性。完整评估落档 `spec/hook-surface/RESEARCH.md`（P-030）。

### 3.5 强制决策产物管线（v1.1 新增：答题主问「每步强制决策+引用依据供下轮审查」）

**裁定：可行且优先——已具备全部基础资产，零新依赖，社区独立演化佐证方向。**

【C】**管线形态**——十步流程每步完成时，强制产出一条「**决策记录事件**」（复用 FWK-DECISION-RECORD 契约）写入 Spec_Runner 事件流（`event: "decision"`；**step 标识 = `metadata.step_id`（如 "research-1"/"design"/"review"），evidence 锚点数组 = `metadata.evidence`（URL / 源码路径 / 文件行号 + 证据等级 E1-E4）——v1.2 精化：FWK-DECISION-RECORD 八字段本身无 evidence/step，落在通用 `metadata: Dict` 通道（P-016 severity 同通道先例）**）。`step-gate`（新 gate 名）机械校验：① 决策记录 schema 字段完整 ② evidence 非空（E1-E4 等级标注存在 + 锚点非空）③ **步骤连续性（该 session 内每个已登记 step_id 恰一条 decision 事件 + 按 step 序单调递增——v1.2 精化："每步恰一条"的 step 概念 = step_id 显式标识，无需在 runner 引入新状态**）——不满足即 exit 非 0 阻止进入下一步。**下一轮审查（RULE-1 时序独立臂 / RULE-5 异基座臂）以事件流为唯一输入**——审查对象 = 前置步骤的决策 + 引用，而非全文重读——这是"声明=重数"从文档层推广到**流程执行层**。

【C】**与已有资产咬合**——① 格式 = FWK-DECISION-RECORD（已有，免新契约）；② 校验 = Spec_Runner gate（已有 execute 骨架，新增 decision 事件类型 + 校验规则，LOC 增量小）；③ 审查管线 = RULE-1/RULE-5 已物理化（特异session + 异基座），只差"决策事件是否每个步骤都有"的强制；④ 引用分级 = FWK-ASSERTION E1-E4 + M7 既有的行号/源码锚点纪律——**本方案是本框架全部核心机制（决策契约 + 事件流 + 门禁 + 证据分级 + 时序独立）的一次组合落地**，不引入任何新概念。

【C】**社区佐证**——adr-governance"ADL = 机器可读 spec + CI 强制执行"（决策与代码闭合循环）、ADR Kit"三层 enforcement + 质量门拒绝模糊决策 + supersede 不编辑"、ADR 侵食"禁止事项显式化 + 机械检测 + 清单自查"——三个独立项目演化出与本方案同构的「决策产物化 + 机械强制」模式；**v1.2 补第四佐证：gpt-researcher 多代理流水线原生含 Reviewer「研究-审核-修正」循环（材料不达标打回重查，A-17 取证）——审查闭环在生成端的又一独立实现**；差异 = 本方案更进一步：把决策产物绑定到**流程步骤粒度**（每步一行）并作为**下一轮审查的唯一输入**（时序独立审查），社区方案停留在仓库级 ADR 强制。

**采纳路径（已实施，v1.8 更新）**：P-020 feature（2026-09-08 落地）：Spec_Runner 增 `decision` 事件类型 + `step-gate` 命令（机械校验）→ DESIGN/IMPL/CHECKLIST 三件套 → 本仓首个真实运行 = P-020 自身全流程每步决策事件入流（五步链 `step-gate --expect research design implement verify finalize` exit 0 实证）。**ADR-0011 后续补强（2026-09-09）**：A 流程强制（P-024，pre-commit 第四 hook step-enforce——批次级门禁）+ C 独立验证（P-025，verify-anchor 锚点真实性机械核查 + RULE-1 独立 pass 取证清单）——本方向闭环。

### 3.6 每阶段定制 agent：可行性 + 环节-工具映射（v1.20，2026-09-10，用户指令「假设每个阶段的工作都可以定制化一个agent 是否可行 如果可行 那么每个环节的工作可以用社区哪些工具增强 例如编程agent 可以使用 matt pocock的skill」）

> **方法**: WebSearch 五路取证（2026-09-10：mattpocock/skills 官方仓库 + aihero.dev + Spec Kit Agents arXiv + Spec-Kit Antigravity + addyosmani/agent-skills + AGENTIC-STACK）。
> **主问题**: ①「每阶段一个定制 agent」是否可行；② 各阶段可用社区哪些工具增强；③ 与本仓十步流程 + RULE 体系的映射与分层。

#### ① 可行性判定：可行，学术 + 生态双向实证（A-27/A-28）

**学术实证（Spec Kit Agents，arXiv:2604.05278）**：SDD 多 agent 管线（PM + developer 角色）在 GitHub Spec Kit 四阶段（Specify→Plan→Tasks→Implement）加 **phase-level context-grounding hooks**（每阶段前只读 discovery 探测仓库证据 + 每阶段后 validation 校验中间产物）——128 runs/32 features/5 仓库：LLM-judge 复合质量 **+0.15**（1-5 量表，Wilcoxon p<0.05），SWE-bench Lite **58.2% Pass@1**（+1.7%），测试兼容性 99.7-100%。**结论 = 阶段级 agent + 阶段级证据锚定显著提升可靠性**——与本仓「每步决策产物 + evidence 锚点 + step-gate 机械校验」同构的实验支撑。

**生态实证（Spec Kit 生态）**：GitHub Spec Kit 原生即分阶段 workflow（specify/plan/tasks/implement + plan review gate）；社区衍生 Spec-Kit Antigravity 把四阶段展开为 **17 个 skills**（clarify/constitution/specify/migrate/analyze/plan/tasks/taskstoissues/quizme/implement/tester/reviewer/checker/validate/status/diff/checklist），每 skill = 一个阶段的 agentic 能力封装。

#### ② 各环节社区工具增强（环节-工具映射表）

| 本仓十步环节 | 社区增强工具（v1.20 取证） | 机制要点 |
|------------|--------------------------|---------|
| Step 1-2 调研 | mattpocock `/research`；gpt-researcher（A-17 既有）；u14app | `/research` = 有引用 + 读一手源（**= 本仓 A 类断言 URL 纪律的生成端镜像**） |
| Step 3 设计 | mattpocock `/grill-with-docs`（对计划结构化面试 + 决策记录）、`/wayfinder`（大任务决策地图）；Superpowers brainstorming（A-02 既有） | grill-with-docs = 本仓「裁决前追问」的生成端镜像 |
| Step 4 裁决 | Spec-Kit `quizme`（Socratic 找 spec 逻辑缺口 = 红队）；mattpocock `/grill-with-docs` | 红队式找缺口 = 本仓「寻找裂缝」生成端同构 |
| Step 5-7 实施 | mattpocock `/tdd` + `/implement`（**phase gate：Red 测试真失败才允许 Green 实现**——statements 非 nudge 是门）；Superpowers test-driven-development（A-02 既有）；Spec-Kit `implement`/`diff`（anti-regression） | **phase gate = 本仓 step-gate 的生成端镜像**（A-29）|
| Step 8-10 审查 | mattpocock `/code-review`（对照 spec + 标准审 diff）；Superpowers subagent review（cold diff）；Spec-Kit `reviewer`/`checker`；addyosmani `/review` | cold diff vs spec = 本仓 RULE-1 独立 pass / verify-anchor 的生成端同构 |

**mattpocock/skills 本体（A-27）**：Mitchell 开源工程 skill 集（aihero.dev 出品，PrdPocock/TypeScript 教育者），2026-04 发布 → 08-30 **~241k stars**，MIT；25 skills，跨 Claude Code/Cursor/Codex/Copilot；**主链 = `grill-with-docs → to-spec → to-tickets → implement → code-review`**（想法→ship 主干），关键设计 = SKILL.md 懒加载（description 常驻 100 tokens/个，body 仅 invoke 时载入）+ **TDD phase gate**（/tdd 定义 Red 失败才允许 Green）+ implement 内置 code review 收尾。**与本仓十步流程同构的又一独立印证**。

**addyosmani/agent-skills（A-29）**：6 阶段七命令（DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP = /spec /plan /build /test /review /ship）+ 20 skills（含 spec-driven-development PRD 先于代码、api-and-interface-design 等），跨 Claude/Cursor/Copilot/Gemini/Windsurf/OpenCode 多 agent 适配。**AGENTIC-STACK（A-30）**：Superpowers + Pocock 组合四阶段推荐栈（Clarify→Specify→Implement→Debug-Review：brainstorming+grill-with-docs / writing-plans / tdd / systematic-debugging+diagnose），并明确 4 层架构（CLAUDE.md / Skills / Subagents / Hooks——概率约束 vs 确定性强制分层）。

#### ③ 与本仓的分层归属（C14）

【C】C-14: **阶段化 agent 可行（B4）但本仓不引入插件本体**——判定 = **Layer-0 概念吸收 + 生成端工具候选（同 Ponytail/Superpowers 先例）**：① 每阶段定制 agent 的学术实证（Spec Kit Agents +0.15）与本仓「每步决策产物 + evidence 锚点 + step-gate」**验证同一机制**（阶段证据锚定提升可靠性），是方法论方向的第 N 独立印证；② Pocock 主链（grill→spec→tickets→implement→review）= 本仓十步流程的软流程镜像，但其 **phase gate 是 prompt 级而非机械门禁**——本仓已用更硬的 step-gate/pre-commit 覆盖（§3.3 C-8 Superpowers 同款先例）；③ 唯一可借鉴增量 = **生成端纪律模块化**（阶段级 skill 封装 = 本仓 DEV-LOG 的「上下文压缩」同类），登记候选不实施。**激活条件** = 若未来将生成端辅助（调研/设计/实施）封装为可复用 skill 时评估；本仓验证端（三校验器 + step-gate + verify-anchor）零改动。

### 3.7 全环节增强工具全景（按十步流程逐环节，v1.21，2026-09-10，用户指令「每个工作环节如何采用优秀社区工具增强 扩展搜索调研范围」）

> **方法**: v1.20 已有六路取证（mattpocock/Spec Kit Agents/Spec-Kit Antigravity/addyosmani/AGENTIC-STACK/arXiv）；本批补 WebSearch 三路（调研生态综述 + Cloudflare AI 审查编排 + agent 框架横评），与既有断言（A-02/A-04/A-15/A-17/A-20/A-27~A-30）汇合成全环节全景。
> **核心答复**: 用户以 mattpocock 增强编程为例——**编程仅是十步流程 Step 5-7 的一环；其余每环均有对应社区工具，多数已有既有断言覆盖**（本批仅补调研/审查两链 + agent 框架横评）。

#### ① 调研环节（Step 1-2）——A-31 新增

【A】A-31: 调研/文献环节开源工具生态（2026-06 综述，AI 科研 agent 分三类：文献综述 / 深度调研报告 / 实验编排）——**gpt-researcher**（A-17 既有，灵活深度报告 + MCP + 引用）；**Stanford STORM**（大纲先行综述生成，知识策展向）；**Agent Laboratory**（端到端：文献综述 + 研究规划 + 实验 + 报告，人反馈环）；**AI-Researcher**（HKUDS，NeurIPS 2025 Spotlight，覆盖文献综述→假设→算法→可投稿论文）；**Feynman**（本地优先研究助手：读论文/搜 web/写稿/审计声明/引用主张）。各项目均支持多模型/OpenAI 兼容端点。取证: blog.gatsbi.com/wordsmith/best-open-source-ai-research-agents + Grenzlinie/Awesome-Auto-Research-Tools README_CN

#### ② 设计环节（Step 3）——复用既有

- **Pocock `/grill-with-docs`**（A-27）：设计前的计划面试 + 决策记录 = 本仓「裁决前追问」生成端镜像
- **Pocock `/wayfinder`**（A-27）：大任务决策地图（探索开放问题→决策/答案喂给流程）
- **Superpowers `brainstorming`**（A-02 既有）：四步（上下文探索/clarify/方案变体/设计签收）阻断过早实现
- **Spec-Kit `analyze`/`clarify`**（A-29）：一致性检查/歧义消解
- **_结论: 零新增断言_（A-02/A-27/A-29 已覆盖）**

#### ③ 裁决环节（Step 4）——复用既有

- **Spec-Kit `quizme`**（A-29）：Socratic 追问找 spec 逻辑缺口（红队）= 本仓「寻找裂缝」同构
- **Pocock `/grill-with-docs`**（A-27）：计划纵深质询
- _结论: 零新增断言_（A-27/A-29 已覆盖）

#### ④ 实施/编程环节（Step 5-7）——v1.20 已覆盖

- **Pocock `/tdd` + `/implement`**（A-27）：phase gate（Red 真失败才 Green）+ 边界内实现 + 收尾 code review
- **Superpowers `test-driven-development`**（A-02 既有）、**Spec-Kit `implement`/`tester`**（A-29）
- _本环节即用户所举 matt 技能示例，A-27 已完整覆盖_

#### ⑤ 审查环节（Step 8-10）——A-32 新增

【A】A-32: 审查环节开源/生产级工具生态（2026-04 Cloudflare Agents Week 实证 + 2026 工具横评）——**Cloudflare「7 专精审查员编排」**（开源基础 = **OpenCode**：security/performance/code quality/documentation/release/compliance 六类专精审查员 + coordinator agent 去重/判定严重度/输出单条结构化评审，跑在 CI 门禁，拦截真实 bug 与安全漏洞——**多专精 agent = 本仓 RULE-1/RULE-5 审查臂的生成端放大镜像**）；**OpenCodeReview**（阿里开源，205 commits，读 git diff + 可配置模型端点，曾服务数万开发者检出数百万缺陷）；**CodeRabbit**（diff+context，多平台 GitHub/GitLab/Bitbucket 支持，~44% 抓取率）；**Greptile**（repo 索引级，82% bug 抓取率基准最高但 ~11 假阳性/run）；**Graphite Diamond**（工作流内嵌，82% fix-rate 最低噪音，stacked PR/merge queue 集成）。取证: blog.cloudflare.com/ai-code-review + github.com/alibaba/open-code-review + designkey.studio agentic code review 2026
- _警示（横评关键结论）_: 「agent 审 agent」模式危险（87% AI 生成 PR 引入安全漏洞，AI 审查器训练自同分布）；生产力 pair 模式 = **agent 首过机械类 + 资深人审架构/判断，人审 gate 不可豁免**——与本仓「审查机械取证 + 人工裁决」分层一致

#### ⑥ 对齐环节（Step 结合校验/漂移）——复用既有

- **Spec Kit Agents `validation hooks`**（A-28）：每阶段后校验中间产物 vs 环境 = 本仓 verify-anchor 的学术同构
- **SGE `drift gate`**（A-04 既有）：spec-code 漂移阻塞合并 = 本仓 repo_stats 对账的社区同构
- **Spec-Kit `diff`/`checker`/`checklist`**（A-29）：产物比对/静态分析聚合/需求验证器
- _结论: 零新增断言_（A-04/A-28/A-29 已覆盖）

#### ⑦ 文档/收束环节——复用既有 + A-31 附带

- **Agent Laboratory / AI-Researcher**（A-31）：论文级报告管线（AI 研究场景）
- **document-skills**（xlsx/docx/pptx/pdf，本仓 D:\RPC 已装 claude 插件）：文档生成
- _结论: 零新增断言_（A-31 覆盖研究文管，D:\RPC 资产非仓外新工具）

#### ⑧ agent 框架底座（定制化 agent 的平台依赖）——A-33 新增

【A】A-33: Agent 开发框架横向（2026-09 横评，OpenClaw vs LangChain vs Dify vs AutoGPT vs CrewAI 六维）——**OpenClaw**（生产级优先：运维/成本控制，多代理全自主）；**LangChain**（快速验证、Python 生态最丰富）；**Dify**（非技术团队低代码）；**AutoGPT**（实验性）；**CrewAI**（角色化 agent 团队编排）。**与本仓关系**: 本仓为纯文档方法论仓，agent 框架 = 生成端外部底座候选（H4 服务形态同议题），Layer-1 候选登记——不引入（零依赖不变式）。取证: CSDN agent 框架横评（2026-09-08）

**环节全景汇总表（十步 → 工具）**:

| 十步环节 | 首选工具（社区） | 本仓既有对应 |
|---------|----------------|-------------|
| Step 1-2 调研 | gpt-researcher / STORM / Agent Laboratory / Feynman（A-31） | WebSearch/MCP 链路（P-013） |
| Step 3 设计 | Pocock grill-with-docs + wayfinder；Superpowers brainstorming（A-27/A-02） | DESIGN 模板 + 决策契约 |
| Step 4 裁决 | Spec-Kit quizme（红队）；Pocock grill（A-29/A-27） | 用户/评审裁决 + M7/ADR 登记 |
| Step 5-7 实施 | Pocock tdd + implement；Superpowers TDD（A-27/A-02） | TDD + 三校验器 + pre-commit |
| Step 8-10 审查 | Cloudflare 7 专精编排；OpenCodeReview；Greptile（A-32） | RULE-1/RULE-5 异基座独立 pass |
| 对齐/漂移 | Spec Kit validation hooks；SGE drift gate（A-28/A-04） | verify-anchor + repo_stats 对账 |
| 文档/收束 | Agent Laboratory / document-skills（A-31） | DEV-LOG / CHECKLIST 四件套 |

**分层结论（本批）**: 各环节工具全数属 **Layer-0 概念登记 + 生成端工具候选**（同 v1.20 判定延伸）；本仓验证端（步-gate/pre-commit/三校验器）零改动；**「agent 审 agent」警示（A-32）与本仓「异基座独立 pass + 机械取证」设计高度一致 = 方法论方向又一印证**。

### 3.8 多工具吸收方法论：适配评估 / 边际贡献 / 去重叠 / 防缝合堆砌 / 对齐（v1.22，2026-09-10，用户指令「假设需要吸收不同的开源工具 如何评估工具与场景的适配 每个工具的边际贡献 如何吸收复用避免重叠 避免缝合堆砌 如何将不同工具进行对齐」）

> **方法**: WebSearch 多轮取证（2026-09-10，OSS 选型框架 + OSS 选型学术 + 打分矩阵实践 + ToolScope 重叠合并 + Agent Atlas 使用频率审计 + OPENTOOLS 工具可靠性 + Stormhelm 框架对比 + agent 工具选型）。本子节是 **v1.20/v1.21 两张环节-工具映射表的"吸收前评估"方法论**——回答吸收多个工具时如何排序、如何避免浪费。
> **主问题五连**: ① 工具与场景适配如何评估；② 每个工具的边际贡献如何量化；③ 如何复用避免重叠；④ 如何避免缝合堆砌；⑤ 多个工具如何对齐。

#### ① 适配评估：结构化打分框架（A-34）

【A】A-34: OSS/工具选型评估框架生态（多源取证）——**① OSS 评估"三支柱"框架**（hufocw 讲稿《Selecting the Right Open Source Software》）：PRODUCT（功能/稳定性/安全/许可）/ PROJECT（社区健康/贡献者多样/治理）/ PREPAREDNESS（TCO/概念验证/风险缓释），并给出 **requirements 优先级矩阵**（高价值-高可行性 = 必须项，核心焦点）；**② OSS 8-Point 企业评估框架**（ossalt.com 2026-03）：成熟度与稳定性/安全/许可/支持与 SLA/可扩展性/集成/治理与可持续性/合规，附评估记分卡（scorecard）+ 概念验证清单；**③ OSS PESTO 学术共识**（Tampere University，arXiv:2102.12267——35 个 OSS 评估模型综述）：评估实践共识 = 「**候选识别 → 因子评估 → 打分**」三个核心活动，OSMM（加权求和算成熟度）/OpenBRR（多指标索引）/QSOS 谱系均用**因子加权求和**形态；**④ 打分矩阵实践**（hufocw「weighted matrix 比较 top 2-3 候选，准则 = Feature Match/许可风险/Bus Factor/POC 结果」）。**与工具场景适配的最终形态 = 准则权重加权求和**——本仓已实例化：P-033 ARC 加权评分矩阵（关系图谱 30%/兼容 25%/性能 10%/维护 15%/agent 面 20%）= 4.2 分选型结论；§3.7 A-30 各工具评分亦同形态。【来源：https://hufocw.org/Download/file/31249 ; https://ossalt.com/guides/how-to-evaluate-open-source-software-enterprise ; https://arxiv.org/pdf/2102.12267】

#### ② 边际贡献：使用频率审计 + 工具固有正确性（A-35/A-36）

【A】A-35: **Agent Atlas**（github.com/Pycomet/agent-atlas，MIT）——「一张你 AI 环境的地图」：扫描 skills/subagents/MCP servers/hooks 并读配置与 **session 历史**，按节点尺寸可视化「你真正在用谁 / 从未用谁 / 缺什么」——**「装了 vs 用了 vs 含义」三问**（每个已装 MCP server 无时无刻把 schema 载入上下文 = 未使用的 server 每天悄悄烧 tokens；两个做几乎同件事的 skill = 重叠；整块能力零覆盖 = 缺口）。**回答边际贡献问题 = 用调用频率证明真实贡献**，与「装了即算数」的幻觉式自评对立。【来源：https://github.com/Pycomet/agent-atlas】
【A】A-36: **OPENTOOLS**（github.com/hydang99/opentools，**arXiv:2604.00137**，Apache-2.0，Notre Dame）——社区驱动工具框架：断言 TALM 可靠性的**双失效模式 = 工具使用正确性（agent 会不会调）+ intrinsic tool accuracy（工具自身正确性，绝大多数研究只关注前者）**；三件套 = ① **工具 schema 标准化 + 轻量 plug-and-play wrapper**（跨 agent 框架即插即用）② **自动化测试套件** ③ **持续监控 + 社区贡献协议**（web demo 让可靠性报告随工具演化持续更新）；实证 = 高质量任务特定工具带来下游任务 **6%-22% 相对增益**（跨多 agent 架构）。**回答边际贡献问题 = 不仅问"是否被使用"还问"工具本身是否正确/稳定/抗漂移"**。【来源：https://arxiv.org/pdf/2604.00137v1 ; https://github.com/hydang99/opentools】
**A-35 并**: **ToolScope**（Oracle AI，**arXiv:2510.20036**，ACL 2026）——去重叠的另一面是量化贡献：ToolScopeMerger 可自动审计工具重叠度 + Auto-Correction 修复错并（见③），实证在 3 LLM × 3 基准上工具选择准确率 **+8.38%~38.6%**——合并后精确度反而**上升** = "重叠不是性能冗余的个人观感，而是可测量的准确率损耗"。（ToolScope 同一名称另有独立项目，如 ilya-kolchinsky/ToolScope 语义检索过滤、dengmengjie/ToolScope 视觉引导——本仓取证明确指 Oracle AI 2510.20036 号；下文③同源）【来源：https://arxiv.org/pdf/2510.20036v2】

#### ③ 去重叠：语义相似合并（A-35 并）

**ToolScope 三阶段合并流程**（arXiv:2510.20036）＝机械去重叠的操作蓝图：**S1 候选生成**（工具索引）→ **S2 关系分类与构图**（LLM 验证语义相似关系，构图）→ **S3 合并与 Auto-Correction**（自动审计合并正确性并修复，保留工具能力的同时缩小选择集）。与本仓去重叠的对应关系：本仓候选池经 §3.4 矩阵 + §3.4.1 逐项调研天然避免重叠（每候选一次性裁决，不复用组明确否决）；若未来候选工具观感重叠（如 §2.6 矩阵 AAT Paper Search MCP 与既有 mcp_paper-search 已注「重叠可选不优先」），可参考 S2 的 LLM 关系验证（而非直接整并）。

#### ④ 防缝合堆砌：窄 scope + 分层 + 取件不整装

- **原子工具窄 scope 原则**：单职责、无重叠的工具才不会稀释选择准确率（ToolScope 证：重叠 description 引入歧义、劣化 agent 工具选择）。与本仓薄壳不膨胀哲学同构（CODE_WIKI「薄壳不膨胀」）。
- **本仓 ADR-0010 Q1 分层 = 天然护栏（零新增机制）**：Layer-0 概念吸收 vs Layer-1 工具/依赖分道——方法论概念（如 7 级阶梯、加权评分）归 Layer-0 只登记不引入；外部工具（ARC）属 Layer-1 不接验证端门禁（D6）。缝合堆砌的病根 = 把不同层的工具整装进同一管道，Q1 分层从结构上阻断。
- **「composability 取件不整装」准则**（Stormhelm 框架对比分析，yeison-gutierrez-simetrik/stormhelm）：对 6 个 AI 开发框架（Spec-Kit/AI Hero/agent-skills/Superpowers/BMAD/GSD）做**多准则评分矩阵**（Spec-Kit 28/33 居首，AI Hero 与 agent-skills 并列 27/33）后**建议混合 harness＝选取各自最强组件**而非整体搬入整套框架——「评分矩阵取件、不整装叠加」= 本文①打分框架与④防堆砌的接缝。【来源：https://github.com/yeison-gutierrez-simetrik/stormhelm（Análisis-Comparativo-Frameworks-AI-Development.md）】

#### ⑤ 对齐：schema 标准化 + 副作用门禁

- **工具 schema 标准化**（OPENTOOLS wrapper）：把不同工具的输入/输出规范成统一 schema，跨框架即插即用——对齐的机械基础 = 统一接口层。
- **本仓 Q3 副作用门禁 = 工具引入前的对齐预检**（ADR-0010 三问之三）：任何新候选引入前过「未激活副作用 = 0」检查（如 P-028/P-030/P-036 止于懒加载 gate、零工具改动 I-1 先例）——对齐不是事后粘连，而是引入门禁里的前置条件。吸收增量 = 若未来多工具叠加，用 Agent Atlas 式使用审计（②）量化每工具真实贡献作对齐裁决输入。

**分层结论（本批）**: **Layer-0 全部（方法论概念）+ 本仓门禁延伸**——适配评估 = ADR-0010 三问 + P-033 加权评分已实例化（A-34 归 Layer-0 方法论）；边际贡献 = 登记 Agent Atlas 使用审计为**生成端候选**（多工具叠加时量化贡献，不引入）；去重叠 = ToolScope 机读合并为**概念候选**（阈值触发，Layer-0 登记）；防缝合堆砌 = Q1 分层即护栏（零新增机制）；对齐 = schema 标准化为外部 wrapper 形态观察（Layer-1 候选，与零依赖不变式 D6 冲突故不优先）。**验证端零改动**。A 33→**36**（+A-34 选型框架 / A-35 重叠合并+使用审计 / A-36 工具可靠性）；B 4 不变、C 14 不变（方法论吸收不涉新裁定）。

## 4. 幻觉排除审查（Step 2 Review）

### 4.1 来源验证

| 引用 | 仓库/站点 | 验证方式 | 状态 |
|------|----------|---------|------|
| Superpowers（130k+ 星） | spec-coding.dev 文章 | WebSearch 命中 | ✅（数量为第三方报道数，声明级） |
| SpecKit（100k+ 星） | kevolson/osn-2026 会议纪要 | WebSearch 命中 | ✅（同上，声明级） |
| Spec Growth Engine | arXiv:2606.27045 | WebSearch 命中全文 | ✅ |
| openai/agents.md（60k+ 仓库/23 工具） | gitcode 转载 + TechSpokes 规范 | WebSearch 命中 | ✅ |
| ARC | github.com/kegesch/arc | WebSearch 命中 README | ✅ |
| adr-kit（rvdbreemen） | github.com/rvdbreemen/adr-kit | WebSearch 命中 README | ✅ |
| promptfoo（并入 OpenAI，24.9k★） | github.com/promptfoo | WebSearch 命中组织 README | ✅ |
| DeepEval（15.6k★） | scrolltest 评测文 | WebSearch 命中 | ✅ |
| Langfuse | langfuse.com docs/blog | WebSearch 命中 | ✅ |
| 三起事故 | CSDN 综述（转述社区报告） | WebSearch 命中 | ⚠️ 声明级（未经官方确认的细节按原文标注） |
| gpt-researcher（29.2k★）/ Alibaba DeepResearch / u14app / Gigaxity | github.com/topics/deepresearch + MCP 广场 | WebSearch 命中 | ✅（星数为主题页 2026-09 快照） |
| AAT | github.com/JhonHander/academic-agent-toolkit | WebSearch 命中 README | ✅ |
| adr-governance / ADR Kit | github.com/ivanstambuk/adr-governance ; kschlt/adr-kit | WebSearch 命中 README | ✅ |
| ADR 侵食三层防御 | wakatchi.dev 文章 | WebSearch 命中 | ✅ |
| Ponytail（DietrichGebert v4.8.x） | github.com/DietrichGebert/ponytail + CSDN/openclawapi 评测文 | WebSearch 命中 README + 两篇评测 | ✅ |
| ARC（v0.8.0） | npm @kegesch/arc 页 + github.com/kegesch/arc issues #20/#15 | WebSearch 命中（v1.5 快照核验） | ✅ |
| ADR Kit（kschlt） | github.com/kschlt/adr-kit README/TECHNICAL/CHANGELOG | WebSearch 命中（v1.5 快照核验） | ✅ |

### 4.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| Superpowers 强制产出 specs/ 规范文档 + 子代理五维验证 | spec-coding.dev 全文 | ✅ 已验证（文章级） |
| SGE drift gate 阻塞合并 | arXiv 摘要/全文 | ✅ 已验证 |
| AGENTS.md 23 工具支持 + 就近优先 | gitcode 指南 + TechSpokes 规范 | ✅ 已验证（双向来源） |
| gpt-researcher 规划者-执行者 + 引用报告 | MCP 广场 README | ✅ 已验证 |
| gpt-researcher **OPENAI_BASE_URL 自定义 OpenAI 兼容端点**（v1.2 增） | docs.gptr.dev LLM 配置页 | ✅ 已验证（官方文档，含 llama.cpp 本地端点示例） |
| gpt-researcher 多代理流水线含 Reviewer 修正循环（v1.2 增） | gitcode 指南（multi_agents reviewer.py） | ✅ 已验证（文章级 + 目录结构佐证） |
| Gigaxity 引用绑定 + 矛盾检测 + CRAG 质量门 | MCP 广场 README | ✅ 已验证 |
| AAT 一命令多 agent 安装 + 20+ 学术源 MCP | 仓库 README | ✅ 已验证 |
| ADR Kit 三层 enforcement + lint 从 ADR 生成 + supersede 不编辑 | 仓库 README FAQ | ✅ 已验证 |
| adr-governance ADL 机器可读 + CI 强制执行闭环（v1.2 补 4.2 表缺行） | 仓库 README | ✅ 已验证 |
| ADR 侵食三层防御 禁止事项显式化→差分静态检查→CI（v1.2 补 4.2 表缺行） | wakatchi.dev 文章 | ✅ 已验证 |
| Ponytail 7 级决策阶梯 + 基准（-54% 代码/-22% token）（v1.4 增） | 仓库 README + openclawapi 评测文 | ✅ 已验证（README/评测文级，未源码直读——不引入本体故不需升级） |
| ponytail: 注释 = 技术债账本（/ponytail-debt 收集）（v1.5 增） | github README + pyshine 评测文 | ✅ 已验证（README/评测文级） |
| mattpocock/skills 主链 + TDD phase gate + 懒加载（A-27，v1.20 增） | GitHub 仓库 + aihero.dev + 评测文 | ✅ 已验证（README/文档级，未源码直读） |
| Spec Kit Agents 学术实证 +0.15 / SWE-bench 58.2%（A-28，v1.20 增） | arXiv:2604.05278 全文 | ✅ 已验证（arXiv 全文级） |
| Spec-Kit Antigravity 17 skills / addyosmani 六阶段（A-29，v1.20 增） | GitHub README + agskills.dev | ✅ 已验证（README/文档级） |
| AGENTIC-STACK 四阶段推荐栈 + 4 层架构（A-30，v1.20 增） | GitHub README | ✅ 已验证（README级） |
| 调研生态 STORM/Agent Laboratory/AI-Researcher/Feynman（A-31，v1.21 增） | gatsbi 综述 + Awesome-Auto-Research README | ✅ 已验证（综述/README级） |
| 审查生态 Cloudflare 7 专精编排 / OpenCodeReview / Greptile 等（A-32，v1.21 增） | Cloudflare 官方博客 + GitHub + 2026 横评 | ✅ 已验证（博客/README/横评级） |
| Agent 框架横评 OpenClaw/LangChain/Dify/AutoGPT/CrewAI（A-33，v1.21 增） | CSDN 横评（2026-09） | ✅ 已验证（第三方横评级） |
| OSS 选型框架：三支柱/8-Point/requirements 优先级矩阵/weighted matrix（A-34，v1.22 增） | hufocw 讲稿 + ossalt 8-Point 指南 | ✅ 已验证（讲稿/指南级） |
| OSS PESTO 学术共识：35 模型综述 + 三活动 + 加权谱系（A-34 并，v1.22 增） | arXiv:2102.12267 全文 | ✅ 已验证（arXiv 全文级） |
| Agent Atlas 使用频率审计 + 三问（A-35，v1.22 增） | github.com/Pycomet/agent-atlas README | ✅ 已验证（README/文档级） |
| ToolScopeMerger 三阶段合并 + Auto-Correction +8.38%~38.6%（A-35 并，v1.22 增） | arXiv:2510.20036 全文 | ✅ 已验证（arXiv 全文级） |
| OPENTOOLS 双失效模式 + schema 标准化 + 测试套件 + 6-22% 增益（A-36，v1.22 增） | arXiv:2604.00137 全文 + GitHub README | ✅ 已验证（arXiv 全文/README 级） |
| Stormhelm 多准则评分矩阵 + Spec-Kit 28/33 + 取件不整装（A-30 佐证，v1.22 增） | github.com/yeison-gutierrez-simetrik/stormhelm 对比分析 | ✅ 已验证（对比文档级） |
| ARC v0.8.0 快照：0 依赖单文件二进制 + arc next/context + D-045 定位句（v1.5 增） | npm 页 + GitHub issue #20 | ✅ 已验证（npm 元数据 + issue 级） |
| ADR Kit 三层 enforcement 细节：policy 块生成 lint / MCP / ContractRelations（v1.5 增） | kschlt/adr-kit README/TECHNICAL/CHANGELOG | ✅ 已验证（README/文档级，未源码直读） |
| Alibaba DeepResearch / u14app / Agent Leaderboard（v1.2 补 4.2 表缺行） | github topics / 仓库 README | ⚠️ 声明级（星数为快照，功能细节未展开） |
| 三起事故 / 星数 / 采用数 | 见 4.1 标注 | ⚠️ 声明级 |

### 4.3 已知局限

1. A 类断言均为 README/文档级（声明级）——未做源码直读级核验（区别于 P-015 v1.2）；候选议程触发时升级证据等级。
2. Superpowers / SpecKit / gpt-researcher 星数为第三方报道或主题页快照，非 API 快照；锁引用时须复核。
3. 三起事故描述来自中文综述转述，个别细节未经官方确认——仅作动机佐证。
4. ADR Kit 的 LOC/接口细节未核验（README 级）——采纳其模式时须 P-015 式源码直读。
5. **版本成熟度盲区（v1.2 新增，v1.6 更新，v1.9 收窄）**：已核验 ARC（v0.8.0）/kschlt-adr-kit（v0.2.x）/Ponytail（v4.8.x）/u14app（v1.0.0）/AAT（PyPI v0.1.2）/Alibaba DeepResearch（19.4k★ 但 2026-02 停滞）版本；Gigaxity 已判定排除（53★ 无版本号）；仍无版本号标注 = Superpowers/SpecKit（软形态不复用，不采纳即不需核验）——采纳任一候选前须源码/API 直读核验（P-015 v1.2 先例；H4 触发时一并执行）。
6. **兼容性盲区部分解除（v1.2）**：gpt-researcher 与 OpenAI 兼容端点兼容性已官方文档确认（OPENAI_BASE_URL）——三机实测仍待 H4；Gigaxity 默认 OpenRouter 云端 key、本地分支待实测。

## 5. 对设计的输入

### 5.1 可用技术方案（候选池）

> **v1.23 指针化说明**: 候选池判定/状态以 **§3.0 候选状态总表**（单一权威位点）为准，详细评估见 §3.4 补强判定矩阵 + §3.4.1 候选逐项深入调研。本节仅作**设计输入汇总指针**（设计阶段取用方案编号），内容不再复制状态叙事（消除双源维护漂移）。

| # | 方案（编号来源） | 权威详情位点 | 当前状态（指针 → §3.0） |
|---|-----------------|-------------|-------------------------|
| 1 | **AGENTS.md 桥** | §3.1 C-01 / §3.4 矩阵 | 已实施（P-021） |
| 2 | **每步决策产物管线** | §3.5 三裁定 / §3.4 矩阵 | 已实施（P-020 + P-024/P-025） |
| 3 | **ARC 决策图谱先导** | §3.4.1 ARC 行 / spec/arc-probe/ + arc-rollout/ | 已实施（P-035，Layer-1） |
| 4 | **DeepEval 评测臂 / 调研链 MCP**（gpt-researcher/Gigaxity/AAT） | §2.6 矩阵 / §3.2 C-04 | 候选（触发驱动） |
| 5 | **ADR 三层 enforcement 模式** | §3.4.2 / spec/hook-surface/ | 评估已执行，不实施（P-030） |

### 5.2 关键约束

- **零依赖不变式**（P-006/D6、P-009 L6）：一切吸收不得引入第三方运行时依赖——AGENTS.md 是文件、ARC 是外部 CLI（工具非依赖）、概念登记零成本；Langfuse/gpt-researcher 本体直接排除，MCP 服务形态为触发驱动候选（H4）。
- **双向零依赖**（P-009 D1）：吸收项不得反向耦合 runner/校验器。
- **生成端自由/验证端受控/接缝登记**（P-013 三层裁决）：skills/MCP 属生成端互操作，不改变验证端；任何新验证位点必须过 R6/M5 门禁。
- **§3.5 管线约束**：decision 事件为 append-only 追加（L2 不变式），supersede 语义用新事件表达（ADR Kit"永不编辑"同构）；引用锚点可解析性须机械校验仍可判定（E1-E4 分级保留语义判断边界——机械校验"非空+可解析"，分级标注由 LLM 负责，等价于现有 A 类断言纪律）。

### 5.3 风险

| 风险 | 等级 | 缓释 |
|------|------|------|
| AGENTS.md 双源漂移（摘要 vs 母文档） | 中 | 桥文件定位"指针+最小摘要"；若采纳纳入 repo_stats 扫描 |
| §3.5 决策事件引入了「每步一记」的执行摩擦 | 中 | 校验仅机械（非空+可解析），单事件数百字符量级；同 session 复用强制 --resume 已有（RULE-1） |
| gate 校验"引用可解析"若过严阻塞流程 | 中 | 分级校验：硬性（字段完整+非空）exit 1；软性（锚点可解析性）exit 2 提示人工复核 |
| ARC 图导入后决策关系语义失真（M7「发现」列拆分非平凡，P-016 已知） | 中 | 复用 FWK-DECISION-RECORD 映射契约；先导试点限定 ADR 簇 |
| 候选议程扩散稀释精力 | 低 | 全部登记"触发驱动"不排队（P-009 同款治理） |

### 5.4 假设区（H1-H4；H1/H2/H3 已闭合，H4 待触发）

- [H1] AGENTS.md 桥文件对主流工具（Cursor/Copilot/Codex 等）的读取兼容性——**已随 P-021 实施激活（2026-09-08：根 AGENTS.md 落地，主流工具进入本仓即读取，无独立实测门槛）**——观测无负面，标注闭合；若未来引入新工具栈另实测
- [H2] ARC 对 M7/ADR 决策的导入可行性——字段映射 / 关系类型差异（复用 FWK-DECISION-RECORD 映射契约）——**已实测（P-031 试点：ADR 导入成功但 date=导入日 + 关系全空——部分证伪「映射最干净」）+ 已规避（P-035 预链接脚本：7 depends_on 边链接成功）**——标注闭合，后续仅同 P-035 流程增补 ADR 时重跑预链接
- [H3] promptfoo redteam 模块对本仓 M7 语料的安全评测价值——**已研判（v1.19/P-036 + v1.1 追记：评测价值低——red team 面向 LLM 应用攻击面，本仓语料为静态文档声明证据无攻击面；仅 financial/事实性插件与断言分级同构概念可 Layer-0 观察；2026-09-10 v1.1 端点认知修正 = 三机推理集群已组建（D:\RPC）OpenAI 兼容端点 E2E 已验证，但 red team 价值判定不受影响）**——标注闭合；promptfoo 扩展按用户裁决**暂时挂起**（工作站集群完善后升级评估）
- [H4] 调研链 MCP（gpt-researcher/Gigaxity/AAT Paper Search）三机端点兼容性与服务形态——**v1.2 部分解除：gpt-researcher 对 OpenAI 兼容端点的兼容性已官方文档确认（OPENAI_BASE_URL，省略 Tavily 换 searx/duckduckgo 亦可）**；剩余待实测 = 三机 LM Studio 实际接入 + Gigaxity 本地分支 + AAT uv/Python3.11 环境（v1.1 新增，v1.2 精化）

## 6. 参考文献

- Superpowers（spec-coding.dev 文章）：https://spec-coding.dev/blog/superpowers-spec-first-ai-agent-skills
- SpecKit（OSN 2026 讲稿纪要）：https://github.com/kevolson/osn-2026/blob/main/summaries/spec-driven-development.md
- Spec Growth Engine：https://arxiv.org/html/2606.27045v1
- AGENTS.md 指南（gitcode 转载）：https://gitcode.com/GitHub_Trending/ag/agents.md
- AGENTS.md 独立规范（TechSpokes）：https://github.com/TechSpokes/agency-specifications-files-agents-md
- Agents Standard：https://agentsstandard.com
- 集中式 Agents.md（Kibnet）：https://github.com/Kibnet/Agents.md
- ARC：https://github.com/kegesch/arc
- ARC npm 页（v0.8.0 快照，v1.5）：https://www.npmjs.com/package/@kegesch/arc
- ARC ledger-to-driver 路线图（issue #20，v1.5）：https://github.com/kegesch/arc/issues/20
- adr-kit：https://github.com/rvdbreemen/adr-kit
- decision-records 主题（reasoning-formats / assay / phodal-adr / repo-seed）：https://github.com/topics/decision-records
- promptfoo：https://github.com/promptfoo ；LLM-as-judge：https://www.promptfoo.dev/docs/guides/llm-as-a-judge/
- DeepEval vs Promptfoo 评测综述：https://scrolltest.com/deepeval-vs-promptfoo-llm-evaluation-framework-test-oracles/
- Langfuse 文档：https://langfuse.com/docs ；Agent 可观测性：https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse
- Agent 事故综述：https://blog.csdn.net/J557565/article/details/163251799
- SDD 中文综述（Spec+Harness 三层）：https://juejin.cn/post/7663320939287347246
- ADR-Tools（先例工具）：https://gitcode.com/gh_mirrors/ad/adr-tools
- deepresearch 主题（gpt-researcher / Alibaba DeepResearch / u14app）：https://github.com/topics/deepresearch
- GOP Researcher MCP：https://cloud.tencent.com/developer/mcp/server/11518
- gpt-researcher LLM 配置（OPENAI_BASE_URL 自定义端点）：https://docs.gptr.dev/docs/gpt-researcher/llms
- gpt-researcher MCP 目录页（v1.0.0/27,217★）：https://www.mcpgee.com/servers/gpt-researcher
- Gigaxity Deep Research：https://mcprepository.com/yoloshii/gigaxity-deep-research
- Academic Agent Toolkit：https://github.com/JhonHander/academic-agent-toolkit
- Agent Leaderboard：https://github.com/jaychempan/Agent-Leaderboard
- adr-governance：https://github.com/ivanstambuk/adr-governance
- ADR Kit（kschlt）：https://github.com/kschlt/adr-kit
- ADR 侵食三段防御：https://wakatchi.dev/adr-guardrails-as-code/
- ADR 状态机（docsie）：https://www.docsie.io/blog/glossary/architectural-decision-record/
- Ponytail（DietrichGebert）：https://github.com/DietrichGebert/ponytail
- Ponytail 介绍文（CSDN）：https://blog.csdn.net/yanceyxin/article/details/162553680
- Ponytail 过度工程修复评测（openclawapi）：https://openclawapi.org/en/blog/2026-06-21-ponytail-overengineering-fix
- OSS 选型三支柱讲稿（hufocw）：https://hufocw.org/Download/file/31249
- OSS 8-Point 企业评估框架（ossalt）：https://ossalt.com/guides/how-to-evaluate-open-source-software-enterprise
- OSS PESTO 学术综述（Tampere University）：https://arxiv.org/pdf/2102.12267
- ToolScope 工具合并与情境过滤（Oracle AI，ACL 2026）：https://arxiv.org/pdf/2510.20036v2
- Agent Atlas 使用频率审计：https://github.com/Pycomet/agent-atlas
- OPENTOOLS 社区驱动工具框架（Notre Dame）：https://arxiv.org/pdf/2604.00137v1 ; https://github.com/hydang99/opentools
- Stormhelm AI 开发框架对比分析：https://github.com/yeison-gutierrez-simetrik/stormhelm

---

## 附录 A：A/B 类断言明细

### A 类（事实类，36 条）

- A-01 至 A-36：见 §1/§2.5/§3.8 各 `【A】` 行（编号按文中出现顺序，来源已随行标注）。

### 附录 B：B 类推断机读块

| id | 推断 | basis |
|----|------|-------|
| B1 | 社区 spec 宪法类框架与本框架流程同构（Constitution≙SPEC_PROCESS、drift gate≙对账制、spec-reviewer≙独立 pass） | A-02/A-04/SGE 能力清单归纳 |
| B2 | AGENTS.md 桥文件可获工具互操作性收益（主流工具原生识别，进入本仓即行为对齐） | A-05/A-06 标准事实归纳 |
| B3 | 「每步决策产物管线」（§3.5）可行——已具备全部基础资产（FWK-DECISION-RECORD 格式 + Spec_Runner 事件流/gate + FWK-ASSERTION 证据分级 + RULE-1/RULE-5 审查臂），且社区三独立项目（adr-governance/ADR Kit/ADR 侵食防御）已演化出同构「决策产物化 + 机械强制」模式 | C-11/C-12/C-13 裁定 + A-23/A-24/A-25 佐证归纳（v1.6 修正：v1.4 插入 ponytail 致 §3.5 三裁定编号 +1，表版 C-08/09/10 与 JSON 版 C-10/11/12 均为旧编号） |
| B4 | 每阶段定制 agent 可行且与本仓「每步决策产物 + evidence 锚点 + step-gate」验证同一机制（阶段证据锚定提升可靠性）——Spec Kit Agents 学术实证 + Spec-Kit/Pocock/addyosmani 生态分阶段封装为双重印证；但 phase gate 为 prompt 级非机械门禁，本仓以更硬机制已覆盖，仅生成端纪律模块化作 Layer-0 概念吸收 | A-27/A-28/A-29 事实归纳（v1.20） |

```json
[
  {"id": "B1", "inference": "社区 spec 宪法类框架与本框架流程同构（Constitution≙SPEC_PROCESS、drift gate≙对账制、spec-reviewer≙独立 pass）", "basis": "A-02/A-04/SGE 能力清单归纳"},
  {"id": "B2", "inference": "AGENTS.md 桥文件可获工具互操作性收益（主流工具原生识别，进入本仓即行为对齐）", "basis": "A-05/A-06 标准事实归纳"},
  {"id": "B3", "inference": "每步决策产物管线可行（基础资产齐备 + 社区三项目独立演化同构模式）", "basis": "C-11/C-12/C-13 + A-23/A-24/A-25（v1.6 修正：§3.5 三裁定编号同步至 C-13 体系）"},
  {"id": "B4", "inference": "每阶段定制 agent 可行且与阶段证据锚定机制同构——学术（Spec Kit Agents +0.15）+ 生态（Spec-Kit/Pocock/addyosmani 分阶段封装）双实证；phase gate 属 prompt 级 vs 本仓机械门禁，故仅生成端 Layer-0 概念吸收", "basis": "A-27/A-28/A-29（v1.20）"}
]
```

### 附录 C：C 类判断复盘

- C-01 至 C-14：见 §3 各 `【C】` 行；§0 声明 14 条（v1.2 吃狗粮 review 重数修正自 v1.1 的 10——P-011 教训的 reverse：声明写少漏计 2，M7 样本 ㉙；v1.4 +1 Ponytail 判定；v1.20 +1 C-14 阶段化 agent 分层判定）。

---

## 附录 D：变更日志详档（v1.2→v1.22 迁入，v1.23 编排重构轮自顶部迁入）

> **迁移说明（v1.23）**: 本附录由 v1.23 编排重构轮自文档顶部迁入——原 21 条逐轮变更日志 mega-line（v1.2~v1.22）压缩为 §0.1 版本历史摘要表后，**详细原文在此保留可追溯性**（零内容丢失）。每条原文 = 当时逐轮提交记录，含用户指令 + 取证要点 + 计数变化，供审计复核调用。

- **v1.2 变更（吃狗粮 review 深度审计轮，用户指令「以本次开发为例进行吃狗粮测试 按 spec 流程盲区扫描 可行性 版本 兼容」）**: 对本报告自身做同基座深度 review（RULE-1 时序独立/self-dogfooding，盲区扫描 = 计数/版本/兼容/一致性四维）捕获 **1P1 + 2P2 + 8P3**：P1 = **C 类计数声明 10 实为 12**（§3 实际【C】12 条：3.1×2 + 3.2×4 + 3.3×3 + 3.5×3——v1.1 全文重写时重数漏 2，dc_validator 不覆盖 C 类边界外，同 P-015 ㉖ 族）→ **M7 样本 ㉙ 入账**（计数声明错误）；P2 = C-10 编号引用错位（佐证实为 C-12）+ §4.2 验证表未同步 v1.1 新增断言 5 行（Alibaba/u14app/Agent Leaderboard/adr-governance/ADR 侵食）；P3 = §2.5「三类」实为两类措辞过度 / 版本成熟度缺失族（gpt-researcher MCP v1.0.0@2026-05-22 补入、u14app/Alibaba/AAT/adr-governance/ADR Kit 无版本号标注）/「G2」自造编号悬空去除 / §3.5 的 step 与 evidence 落点精化（metadata.evidence + metadata.step_id）/ **兼容矩阵缺失（新增 §2.6：gpt-researcher 官方支持 OPENAI_BASE_URL 本地 OpenAI 兼容端点→三机 LM Studio 可直接接、搜索轴可切 duckduckgo/searx 免 Tavily key、多代理流水线含 Reviewer「研究-审核-修正」循环=第三同构佐证补入 C-12）**。核心结论与 §3.5 裁定不受影响（v1.2 修正全部为表述/版本/兼容取证精化）。A/B/C/H 计数不变（25/3/12/4——C 由 10 修正为实际 12）。
- **v1.3 变更（ADR-0010 验收条件之二落地轮，用户指令「好的，执行补列」）**: §3.4 补强判定矩阵新增**「分层归属（ADR-0010 Q1）」列**——依 ADR-0010 三问门禁 Q1 对候选池批量预演（6 候选分层 + 不复用组标"不适用"）：AGENTS.md 桥 Layer-0 / 决策产物管线 Layer-1（契约 FWK-DECISION-RECORD 复用 Layer-0）/ drift-gate Layer-0 / ARC Layer-1 / DeepEval 臂+调研链 MCP Layer-1 / ADR 三层 Layer-0；附批量预演注（分层 = 事实判定不随裁决改变；不复用组已按 D6 先例否决不过门禁）——**闭环 ADR-0010 验收条件之二**。核心裁定与 §3.5 不变；断言计数不变（25/3/12/4，无新增断言）。
- **v1.4 变更（Ponytail 补充调研批，用户指令「社区同类框架生态调研 补充调研 代码实现阶段 ponytail 框架 是否可复用」）**: §2.5 新增**「代码实现步骤（Step 5-7 实施）→ 生成端防过度工程」**子节 + A-26（Ponytail v4.8.4 MIT——"懒惰资深开发者"规则集+插件，7 级决策阶梯：YAGNI→库内复用→stdlib→平台原生→已装依赖→一行→最少代码；基准 -54% 代码/-22% token；阶梯在理解后运行+根因修复+安全不可偷懒）；判定 C = **插件/规则集本体不复用**（同 Superpowers 先例）+ **7 级阶梯概念吸收候选（Layer-0）**——它是 ADR-0010 三问门禁的**生成端镜像**（方法论方向第 N 独立印证）；矩阵 + 十步映射 Step 5-7 行同步；A 25→26 / C 12→13（人工重数核对）；depends 补 ADR-0010。
- **v1.5 变更（候选池深入调研批，用户指令「§3.4 补强判定矩阵 候选项目需要执行深入调研 能够清晰化给出建议」）**: §3.4 后新增**§3.4.1 候选逐项深入调研与清晰建议**——对候选池逐项 WebSearch 核验最新快照（2026-09-08）：**ARC 重大演进**（npm @kegesch/arc **v0.8.0**/161 commits/0 依赖单文件二进制；实体 9 型 + 关系 14+；命令扩展 arc next/context；D-045 "Arc answers questions agents cannot answer themselves" + ledger-to-driver 路线图 issue #20——**建议升级为优先候选**，P-020 落地后触发）；**ADR Kit 双仓独立演化确认**（kschlt/adr-kit 195 commits + policy 块自动生成 lint 规则 + MCP + ContractRelations/supersession chains/scenario taxonomy；rvdbreemen/adr-kit 539 commits——**模式吸收点更新**：禁止性负例通道并入 P-020 设计）；**Ponytail v4.8.3 核验**（ponytail: 注释=技术债账本，与本仓 DEV-LOG 同构——登记 pattern 演进候选）；**AGENTS.md 规则源传播生态观察**（ARC/ponytail/ADR Kit 均以规则文件+agent 适配为标准形态）；decision-records 生态同族小体量观察（phodal/adr/watercooler/repo-seed，不入候选池）。A-10（ARC）就地更新快照；**A/B/C 计数不变（26/3/13/4）——无新增行首 A/C 断言**（深入调研事实以内联 URL 登记于 §3.4.1）。
- **v1.6 变更（§3.4/§3.4.1 吃狗粮审计轮，用户指令「3.4 补强判定矩阵 3.4.1 候选逐项深入调研与清晰建议 进行一次吃狗粮审计」）**: 对本报告 §3.4 矩阵 + §3.4.1 子节做同基座深度 review（盲区扫描 = 计数/版本/兼容/一致性四维，同 v1.2 先例）捕获 **6 P2 + 5 P3，无 P1**：P2 = ① Ponytail 版本号内部分裂（A-26 行/§2.6 v4.8.4 vs §3.4.1 v1.5 核验 v4.8.3——统一锁 v4.8.x 区间声明）② ARC 建议状态矩阵未同步（矩阵仍"候选议程/触发驱动" vs §3.4.1/§2.6"升级优先候选"）③ 附录 B B3 basis C 编号错位（v1.4 插入 ponytail 致编号 +1，§3.5 三裁定实为 C-11/12/13，表版 C-08/09/10 与 JSON 版 C-10/11/12 均未同步）④ §3.5 采纳路径 P-019 过时（编号已顺延 P-020 未回写）⑤ §3.4.1 ADR 三层行 A-13 引用错位（A-13 实为 Langfuse，rvdbreemen/adr-kit 应为 A-08）⑥ §2.6 盲区登记 + §4.3 局限 5 未随 v1.5 快照更新（仍称 ARC/adr-kit/Ponytail"未标版本号"）；P3 = G2 悬空编号残留（矩阵/§5.1）/ 计数说明未记 v1.5+1.6 重数 / ARC「19 天前」时点相对值 / ADR 三层矩阵行未标 v1.5 注 / §3.4.1 内联取证形态偏移观察。**核心裁定不变**；计数不变（26/3/13/4，无新增断言）。修正全部为同步/编号/版本精化。
- **v1.7 变更（P-020 step-gate 决策产物管线吃狗粮落地，2026-09-08）**: 矩阵「每步决策产物管线」行建议列更新为**「已吸收（P-020 done，v1.7）」**——CER §3.5 裁定落地：step-gate 三件套（STEP_GATE_CHECKLIST v1.2 accepted 三问 8/8 + DESIGN v1.0 + CHECKLIST_FUNC v1.1 accepting 12/12）+ spec_runner v1.1.0（decision 事件 + step-gate 命令）；§3.5 采纳路径 P-020 完成。断言计数不变（26/3/13/4）。
- **v1.8 变更（吸收状态同步轮，用户指令「更新一下 已经吸收复用需要更新状态」）**: 对 §3.1/§3.2/§3.4/§3.4.1/§3.5/§5.1 中**已实际吸收复用**条目的状态位点全面同步：**AGENTS.md 桥 → 已吸收（P-021 done，2026-09-08，根 AGENTS.md 落地 + ADR-0010 三问 Layer-0 审核通过）**；**每步决策产物管线（§3.5）→ 已吸收（P-020 done 2026-09-08 step-gate 决策流 + step-gate 命令；**ADR-0011 accepted A+C 决策两出路全落地**：P-024 出路 A 流程强制 = pre-commit 第四 hook step-enforce（2026-09-09）+ P-025 出路 C 独立验证 = spec_runner verify-anchor 锚点真实性机械核查 + SPEC_PROCESS RULE-1 独立 pass 取证清单（2026-09-09）——"决策记录从档案提升为驱动执行的输入"方向三项目独立印证 → 本仓完整实例化含流程强制与审查取证）**；**drift-gate 概念 → P-023 概念登记已落（2026-09-09，Layer-0 仅登记不实施）**；§3.5 采纳路径更新为已实施态；§5.1 候选池前两条改已实施。**断言计数不变（26/3/13/4——纯状态同步零新增断言）**。
- **v1.9 变更（§2.6 可行性判定补充调研批，用户指令「2.6 兼容与可行性矩阵 可行性判定需要补充调研 给出清晰的判断 吃狗粮执行 测试step-gate是否起效」）**: 对 §2.6 矩阵四个可行性模糊项做 **2026-09-09 四路 WebSearch 补充取证**给出清晰判定：**u14app/deep-research H4 待测 → 可行**（MCP 形态 streamable-http+SSE，任意 OpenAI 兼容端点可接（三机 LM Studio），Searxng 本地搜索轴，v1.0.0@2026-05-21 维护 active，Node 18+；**安全提示：SSRF 漏洞 issue #153 未修**）；**Alibaba DeepResearch H4 待测 → 不复用**（通义 30B-A3B 模型方案 = 训练级重栈 + repo 2026-02 起停滞（19.4k★ 但唯一发布 2025-09），spring-ai-alibaba 变体 = Java 栈 + 2026-02 停滞——均超出调研弹药层定位）；**AAT 环境门槛高 → 可行（生成端互操作）**（PyPI v0.1.2，`uvx` 免安装直跑，Python 3.11+ + uv 确认；其 Paper Search MCP（20+ 学术源）与本仓既有 mcp_paper-search 重叠 → 可选触发驱动）；**Gigaxity 云端依赖 → 不可行（本仓）**（Qwen3-30B-A3B 合成模型重资源 + Exa/Brightdata 外部 key；gpt-researcher 已覆盖同功能且更轻）。版本盲区登记更新（u14app v1.0.0 / AAT v0.1.2 已核验；Alibaba/Gigaxity 判定排除）；§4.3 局限 5 同步。**断言计数不变（26/3/13/4——本批纯内联取证 + 判定更新，无新增行首断言）**；§2.6 表可行/不可行判定即「清晰的判断」。
- **v1.10 变更（hook 面扩展独立评估批，用户指令「执行后续 hook 面扩展调研评估」——§3.4.1 ADR 三层 enforcement 行"下一步 = 触发驱动（后续 hook 面扩展时评估）"触发）**: 新增**§3.4.2 hook 面扩展独立评估**——社区三轮 WebSearch 取证（2026-09-09：分层 hook 实践 = pre-commit 增量快查 <5s / pre-push 全量复验 <15s / CI 完整兜底（ADR Kit 分阶段 enforcement 实证）；\--no-verify 旁路 = git 官方文档明示可跳过 + block-no-verify 实测 12 种绕过向量全放行 → 本地 hook 是"诚实护栏"非绝对强制；forbid-ban 通道形态 = deny-list 正则 + allowlist 例外（git-secrets / nhsd-rules-deny.txt / detect-secrets baseline）+ policy 块显式化）+ **本仓 AGENTS.md 禁止事项 6 条逐条机械化可行性矩阵**（记录性 #2/#4 已完全机械化、过程性 #3/#5/#6 不可机械拦截、#1 仅 pre-push 复验可兜底）+ **ADR-0010 三问结局 = Q2 激活条件未满（无真实旁路失败案例 → 不实施）**，注册为 ADR-0010 失效条件②观察项；§3.4.1 ADR 三层行同步"评估已执行"标注；完整评估落档 `spec/hook-surface/RESEARCH.md`（P-030）。**断言计数不变（26/3/13/4——本批纯内联取证 + 评估结论，无新增行首断言）**。
- **v1.11 变更（审查修复轮，用户指令「审查上一轮评估过程」——P-030 批次独立复核）**: §3.4.2 禁止事项矩阵行 #1「现状」列口径修正——「三 hook 均 arm」歧义表述（可误读为全仓仅 3 hook）统一为「全仓四 hook 均 arm（dc/m7/repo 三校验器 + step-enforce）」；与 `spec/hook-surface/RESEARCH.md` v1.1 同矩阵「四 hook 配置齐备」口径一致（M7 样本 ㉜，P2-2）；复核轮（M7 样本 ㉝）再扫捕获 §3.4 【C】行「pre-commit 三 hook」同族残留——跨文档口径一致性扫面未覆盖 CER 全文（半修态），同步为「四 hook（三校验器 + step-enforce，P-024 起）」。**断言计数不变（26/3/13/4——纯表述同步，无新增行首断言）**。
- **v1.12 变更（状态同步轮，用户指令「3.4.1 候选逐项深入调研与清晰建议 更新状态」）**: 对 §3.1/§3.2/§3.4/§3.4.1/§5.1 状态位点再同步——**drift-gate 概念 → P-029 已实施（2026-09-09：repo_stats「意图→证据→缺口」缺口报告落地 = `CheckResult.gap` 三元组 + `_gap_report()` 块 + pattern_lib_version 2 激活，升格自 P-023 仅登记态）**；**ADR 三层 enforcement → P-030 评估已执行（2026-09-09：hook 面扩展独立评估，gate 三问 Q2 激活条件未满 → 不实施，登记 ADR-0010 失效条件②观察项，见 §3.4.2）**，§3.4 矩阵行 + §3.2 C 行 + §5.1 第 5 条同步标注；ARC 仍为优先候选待用户裁决（无状态变化，v1.8 触发条件满足标注保持）。**断言计数不变（26/3/13/4——纯状态同步零新增断言）**。
- **v1.13 变更（ARC 试点调研批，用户指令「ARC启动调研分析 吃狗粮模式」——§3.4.1 ARC 行「下一步 = 待用户裁决」条款裁决触发）**: ARC 行更新为「**评估已执行（P-031，2026-09-09，试点实施待用户裁决）**」——独立调研落档 `spec/arc-probe/RESEARCH.md`（第 25 feature 目录，11A+3B+3C+2H）：**本机实态试跑（Windows node v24，临时安装 @kegesch/arc 0.8.0）** = 命令面 init/add/list/check/next/trace/graph/import 全可用 + check 分类/JSON 输出正常；**0.x 平台缺陷双实证** = `arc --version` 输出 0.1.0（≠ npm 0.8.0 失配）+ `arc skill` Windows 崩溃（`B:\~BUN` 构建路径硬编码泄漏）+ issue #30（linux/pnpm 无 bun → `env: bun` 失败，与 README「no bun required」矛盾）；**H2 假设部分证伪** = 本仓 ADR-0007 导入成功（title/status 中文保真）但 **date = 导入日期 + depends/driven_by 关系全空**（图关系不自动映射——「映射最干净」失效，需预链接）；`arc link` 方向语义文档未标注需实测校准；agent surface（CLI+JSON+skill）+ `init-agent` 与本仓 AGENTS.md 桥同构；driver 命令/#14 CI 强制均在路线图未发布。**断言计数不变（26/3/13/4——本批纯状态位点更新 + 内联取证，无新增行首断言）**。
- **v1.14 变更（ARC 替代框架调研批，用户指令「ARC 决策图谱有平台缺陷 那么社区是否有类似的替代框架吗 执行调研任务」）**: ARC 行补录替代调研结论（P-032，落档 `spec/arc-probe/RESEARCH.md` v1.1，17A+4B+4C+2H）——**6 候选全景核验 + phodal/adr 本机实测：无候选在「关系图谱递归查询 + 零依赖 agent 面」维度完全替代 ARC，ARC 保持主选**（0.x 缺陷处置 = 规避缺陷命令面 skill/linux bun + 等 1.0）；替代品按单一维度登记补位观察 = adr-explorer（可视化，最强但只读 web app）/ adr-kit（MCP 强制）/ phodal/adr（Windows 轻量管理，但 npm 196 包依赖 deprecated）/ adr-governance（ADL YAML AI 治理）；log4brains（1582★ 但 2024-12 停滞）与 continuity（付费墙 + 专有许可）排除。**断言计数不变（26/3/13/4——本批仅候选行状态位点 + 内联取证，无新增行首断言）**。
- **v1.15 变更（ARC 选型对比批，用户指令「补充调研 如果采用 adr-explorer / kschlt/adr-kit / phodal/adr / adr-governance 单维度补位 相比 ARC 升级 哪个选项更优 考虑兼容 性能 维护等多个方面」）**: ARC 行补录选型对比结论（P-033，落档 `spec/arc-probe/RESEARCH.md` v1.2，18A+5B+5C+2H）——**加权评分矩阵（关系图谱能力 30% / 本仓兼容 25% / 性能 10% / 维护 15% / agent 面 20%）= ARC 升级 4.2 分显著最优**（次高 adr-explorer 3.2 仅只读看板；adr-kit 2.85 强制面与 step-gate 重叠 + uv 安装成本；phodal/adr 2.75 npm 停更；adr-governance 2.4 重 CI）；**单维补位不作为 ARC 平替，仅登记辅助观测（首选 adr-explorer 可视化看板）**。**断言计数不变（26/3/13/4——本批仅候选行状态位点 + 内联取证，无新增行首断言）**。
- **v1.16 变更（ARC 缺陷规避方案批，用户指令「补充调研 假设采用ARC 升级如何规避缺陷 深入调研社区信息」）**: ARC 行补录缺陷规避方案结论（P-034，落档 `spec/arc-probe/RESEARCH.md` v1.4，22A+6B+6C+2H）——§3.8 规避矩阵 = 官方 Windows 二进制直链（v0.8.0 sha256 可校验）+ 版本快照固化 + 命令白名单（排除 skill 崩溃面）+ import 预链接脚本（FWK-DECISION-RECORD 映射）+ 90 天停滞观察项对冲 bus factor=1；**深度复核捕获 A-11 事实错误并修正 = driver 命令（#25 next/context/#26 Vision 实体）已于 2026-06-01/05-31 completed 发布（gaps 并入 arc check），非「计划中未发布」**（A-20/A-21 补证）——**采用资质确认，实施仍待用户裁决**。**断言计数不变（26/3/13/4——本批仅候选行状态位点 + 内联取证，无新增行首断言）**。
- **v1.17 变更（ARC 升级实施批，用户指令「按照吃狗粮模型执行ARC 升级 规避缺陷」）**: ARC 行补录实施完成（P-035，落档 `spec/arc-rollout/` 四件套）——**规避矩阵落地 tools/arc/ 薄壳工具链**：arc_wrap.py 命令白名单封装器（skill/init-agent 崩溃面拦截 exit 2）+ arc_prelink.py ADR 预链接脚本（frontmatter depends→depends_on 边）+ 版本 0.8.0 sha256 固化（**8f4b3089 与官方一致**，npm 途径获取=GitHub 直连超时备选）+ data/.arc **8 ADR 决策图**（7 depends_on 边）；**实测发现 link 合法边按实体类型动态决定**（decision→decision 仅 enables/supersedes/depends_on，--help 展示集 ≠ 运行时校验集）——预链接用 depends_on 校准；trace/impact/check 递归可用；**ARC 从「候选待裁决」→「Layer-1 已实施（生成端辅助查询）」**，D6 不接门禁（与 step-gate 正交）。**断言计数不变（26/3/13/4——本批仅候选行状态位点 + 内联取证，无新增行首断言）**。
- **v1.18 变更（假设区状态同步轮，用户指令「先更新 H1/H2 假设区状态」）**: §5.4 假设区 **H1/H2 由「待实测」同步为「已实测/已实施」**——**H1（AGENTS.md 读取兼容性）**：P-021 已实施（根 AGENTS.md 落地 + 主流工具进入本仓即读取，无独立实测门槛）→ 标注**已随 P-021 实施激活，观测无负面**；**H2（ARC 导入可行性）**：P-031 试点实测（ADR 导入成功 + date=导入日 + 关系全空——**部分证伪**）+ P-035 预链接脚本规避（7 depends_on 边链接成功）→ 标注**已实测（部分证伪 + P-035 规避落地）**。§0 假设区说明同步（4 条：H1/H2 已闭合，H3/H4 仍待触发）。**断言计数不变（26/3/13/4——纯状态同步零新增断言）**。
- **v1.19 变更（promptfoo 首轮评测调研-懒加载分析批，用户指令「promptfoo 首轮评测 按照吃狗粮模型进行调研-懒加载分析」——P-036，CER §5.4 H3 触发 + P-010 CHECKLIST §11 待办前置）**: **H3 由「待首轮评测后评估」同步为「已研判 = 评测价值低」**——调研落档 `spec/promptfoo-first-run/RESEARCH.md`（P-036，第 27 feature 目录）：端点三机不可达实测（P-010 方案 Z 触发前置「端点就绪」未成立）+ promptfoo 0.122.0 redteam 命令面实测 + red team 能力快照（157 插件 6 类 + OWASP LLM Top 10 2025/NIST/MITRE/ISO/GDPR/EU 映射 + **financial 族插件与本仓断言分级方法论同构观察**）+ **H3 研判 = 评测价值低**（概念同构但载体不适用——本仓为文档声明证据，无 LLM 应用攻击面）；**ADR-0010 三问 Q2 激活条件未满足 → 止于懒加载 gate**（同 P-030 先例，零工具改动 I-1）；M7 断言计数不变（26/3/13/4——本批独立 RESEARCH 断言 5A+1B+2C+1H 于 promptfoo-first-run 文档内登记，CER 零新增）。**断言计数不变（26/3/13/4）**。
- **v1.20 变更（每阶段定制 agent 可行性补充调研轮，用户指令「进行一轮补充调研 如果假设每个阶段的工作都可以定制化一个agent 是否可行 如果可行 那么每个环节的工作可以用社区哪些工具增强 例如编程agent 可以使用 matt pocock的skill」）**: 新增 **§3.6「每阶段定制 agent：可行性 + 环节-工具映射」**——WebSearch 取证（2026-09-10，mattpocock/skills 官方页 + Spec Kit Agents arXiv + Spec-Kit Antigravity + addyosmani/agent-skills + AGENTIC-STACK 五路）：**可行性判定 = 可行且已有学术+生态双向实证**（Spec Kit Agents 多 agent SDD 管线 128 runs/32 features LLM-judge +0.15 + SWE-bench 58.2% Pass@1；Spec Kit 分阶段 agents 形态）；**环节-工具映射表**（调研→Pocock /research、设计→Pocock /grill-with-docs + /wayfinder、裁决→quizme/grill-me、实施→Pocock /tdd + /implement（phase gate）、审查→Pocock /code-review + Superpowers subagent review（cold diff））；**Pocock 主链 = grill-with-docs→to-spec→to-tickets→implement→code-review = 与本仓十步流程同构的独立印证**；**分层归属 = Layer-0 全部（概念吸收）+ 生成端工具候选（同 Ponytail 先例：插件本体不入仓）**——阶段级 agent 化深植 llama 生成端纪律，本仓验证端已用机械门禁覆盖。A 26→**30**（+A-27 Pocock / A-28 Spec Kit Agents / A-29 Spec-Kit Antigravity+addyosmani / A-30 AGENTIC-STACK）；B 3→**4**（+B4 阶段化 agent 可行性推断）；C 13→**14**（+C14 阶段化 agent 分层判定）。断言人工重数核对通过。M7 承诺声明计数变更（26/3/13/4→30/4/14/4）同步于附录 A/B/C 与 §0。
- **v1.21 变更（全环节增强工具扩展调研轮，用户指令「补充调研 我的意思是 当前每个工作环节如何采用优秀的社区工具进行增强 例如matt的技能可以用来增强编程 那么别的环节 调研 设计 审查 对齐 等环节有什么优秀的开源工具可以增强 可以定制化agent matt的技能只是举例 你需要扩展搜索调研范围」）**: 新增 **§3.7「全环节增强工具全景（按十步流程逐环节）」，matt 为编程环节示例，扩展覆盖调研/设计/裁决/实施/审查/对齐/文档全链**——WebSearch 补证（2026-09-10，调研生态 + 审查生态 + agent 框架横评八路）：**调研环节** = gpt-researcher（A-17 既有）/ STORM（Stanford 大纲式综述）/ Agent Laboratory / AI-Researcher（HKUDS NeurIPS 2025 Spot）/ Feynman（本地优先论文阅读）**新增 A-31**；**审查环节** = Cloudflare「7 专精审查员编排 + coordinator 去重 + 机械门禁」（OpenCode 基础，A-32）/ OpenCodeReview（阿里开源 205 commits）/ CodeRabbit / Greptile（82% 基准）/ Graphite Diamond（A-32 合并取证）**新增 A-32**；**对齐环节** = Spec Kit Agents validation hooks（A-28 既有）/ SGE drift gate（A-04 既有）/ Spec-Kit quizme 红队（A-29 既有）——**对齐 = 已有机制复用，零新增搜索**；**设计/裁决环节** = Pocock /wayfinder + /grill-with-docs（A-27 既有）+ Superpowers brainstorming（A-02 既有）+ Spec-Kit analyze/clarify（A-29 既有）——结论**零新增**；**文档/收束环节** = Agent Laboratory / AI-Researcher 论文管线（A-31 内一并）+ document-skills（本仓 D:\RPC 已装，非仓外新工具）——**各环节多数已有既有断言覆盖，本批仅补调研/审查两链**。**分层 = Layer-0 全部（概念登记）+ 生成端候选**（同 v1.20 判定延伸，验证端零改动）。A 30→**33**（+A-31 调研生态 / A-32 审查生态 / A-33 agent 框架横评）；B 4 不变；C 14 不变。断言人工重数核对通过。声明计数同步（30/4/14/4→33/4/14/4）。
- **v1.22 变更（工具吸收方法论调研轮，用户指令「补充调研 假设需要吸收不同的开源工具 如何评估工具与场景的适配 每个工具的边际贡献 如何吸收复用避免重叠 避免缝合堆砌 如何将不同工具进行对齐」）**: 新增 **§3.8「多工具吸收方法论：适配评估 / 边际贡献 / 去重叠 / 防缝合堆砌 / 对齐」**——WebSearch 取证（2026-09-10，OSS 选型框架 + OSS 选型学术 + 加权矩阵实践 + ToolScope 重叠合并 + Agent Atlas 使用频率审计 + OPENTOOLS 工具可靠性 + Stormhelm 框架对比 + agent 工具选型多轮）：**①适配评估** = OSS 三支柱/八点评估框架（PRODUCT/PROJECT/PREPAREDNESS 或 maturity/security/licensing/support 八点，hufocw 讲稿 + ossalt 8-Point）**A-34** + OSS 选型学术（**OSS PESTO**，Tampere University arXiv:2102.12267——35 个评估模型综述共识 = 「候选识别→因子评估→打分三个核心活动」+ OSMM/OpenBRR/QSOS 加权求和谱系）**A-34 并** + 打分矩阵实践（requirements 优先级矩阵 + 权重比较矩阵，hufocw 讲稿「weighted matrix 比较 top 2-3 候选」，ossalt 8-Point scorecard）**A-34 并**——本仓已实例化（P-033 ARC 加权评分 = 4.2 分，§3.7 A-30 类先例）；**②边际贡献** = Agent Atlas「使用频率审计 = 装了 vs 用了 vs 含义」资产盘点（skills/subagents/MCP/hooks 重叠/缺口诊断，session/调用记录定尺寸 = 每个会话都在为未用的 MCP 付 token 成本）**A-35** + OPENTOOLS「intrinsic tool accuracy 工具固有正确性（错误率/稳定性/漂移鲁棒）+ 自动化测试套件 + 持续监控 + 社区贡献协议」，高质任务特定工具下游任务相对增益 6%-22%（arXiv:2604.00137）**A-36**；**③去重叠** = ToolScope「语义相似候选 → LLM 关系验证 → 图合并 + Auto-Correction」，工具选择准确率 +8.38%~38.6%（Oracle AI arXiv:2510.20036，3 LLM × 3 基准）**A-35 并**；**④防缝合堆砌** = 原子工具窄 scope 原则（单职责无重叠）+ 本仓 ADR-0010 Q1 分层天然防（Layer-0 概念 vs Layer-1 工具分道）+「多准则评分矩阵比较、取件不整装」准则（Stormhelm 框架对比：Spec-Kit 28/33 居首、多准则评分 + 混合 harness 建议，不整装整套叠加）；**⑤对齐** = 工具 schema 标准化（OPENTOOLS wrapper）+ 本仓 Q3 副作用门禁 = 工具引入前的对齐预检。**分层 = Layer-0 全部（方法论概念）+ 本仓门禁延伸**：适配评估 = ADR-0010 三问 + P-033 加权评分已实例化；边际贡献 = 登记 Agent Atlas 使用审计为生成端候选（多工具叠加时量化贡献）；去重叠 = ToolScope 机读合并为概念候选（阈值触发）；防缝合堆砌 = Q1 分层即护栏（零新增机制）。A 33→**36**（+A-34 选型框架 / A-35 重叠合并+使用审计 / A-36 工具可靠性）；C 14 不变（方法论吸收不涉新裁定）。断言人工重数核对通过。声明计数同步（33/4/14/4→36/4/14/4）。

---

**Review 签字**: _________ 日期: _________