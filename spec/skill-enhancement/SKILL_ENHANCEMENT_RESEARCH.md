---
id: skill-enhancement-RESEARCH
type: design
version: 1.1
status: in-review
date: 2026-08-20
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0005, ADR-0009, DIS-007, langgraph-upgrade-RESEARCH, deepseek-harness-RESEARCH]
upstream: null
---

# 开源 Skill 生态对 SPEC_PROCESS 十步流程的增强调研 v1.0 (2026-08-20)

> **任务来源**: 用户提问"当前 spec 工作流每一个步骤是否可以被开源社区的 skill 增强细化？比如 review 是否可以复用吸收开源社区的 skill，调研阶段是否可以复用 deep-research 等 skill，实现 skill 与硬规则并存"
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；WebSearch + WebFetch 取证（2026-08-20）
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验
> **v1.1 补充（2026-08-20）**: §8 MCP 工具层增强调研——任务来源"相比于 skill，增强 MCP 工具使用是否可以提升框架性能、信息真实性（如学术调研用 paper-search MCP、stack-exchange MCP）"。**本节方法升级**：§2 为文献级证据，§8 含 5 组本会话直测（E1 级——MCP 响应即机械证据，恰是本节论题的现场演示）。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 21 | 每条附 URL + 可核对来源（GitHub 仓库 / agentskills.io 标准 / skillsmp 页面为主，二手源单独标注）；取证日期 2026-08-20；v1.1 §8 新增 5 条（其中 4 条为本会话 MCP 直测 E1 级） |
| B 推断类 | 4 | B1-B4，登记于附录 B（B4 为 v1.1 新增） |
| C 判断类 | 4 | §4 吸收裁决 2 条 + §5 风险判断 1 条 + §8.5 MCP/skill 结构裁决 1 条（v1.1） |
| 假设区 | 6 | H1-H6，未取证声明（H5/H6 为 v1.1 新增） |

> **计数说明（R7 机械重数）**: A 类 21 条（行首 `【A】` 标记，`grep -c '【A】'` 重数；v1.0 主体 16 + v1.1 §8 新增 5）、附录 B 4 条（`"id": "B\d+"` 机读块；B4 为 v1.1 新增）、C 类 4 条（`【C】` 标记，DR-2 首版不对账）、假设区 6 条（`[H\d+]` 列表项；H5/H6 为 v1.1 新增，登记于 §8.6 补充假设区）。格式契约遵 P-012 门禁拦截实录教训（[DEEPSEEK_HARNESS_RESEARCH](../deepseek-harness/DEEPSEEK_HARNESS_RESEARCH.md) §0 计数说明）。**门禁拦截实录（2026-08-20）**: 初稿统计表手填 A=14，dry-run 机械重数 **16**——写作时先填计划数（14），正文展开中新增独立条目（wshobson / swell-agents 各自成条 + oh-rid 拆两条）后未回写统计表，计划数与实际数漂移（少报 +2）。**形态 II 实例，入账 M7 样本⑫**（M5 提交瞬间拦截——样本⑨ 同性质：工具拦截，非 LLM 审查轮）。发生在"调研 skill 增强以反幻觉"的报告上——规律②"防幻觉机制自身不设防"再次实证：即便作者刚复盘完 P-012 的两跳拦截教训，手填计数仍在下一份文档复发，R7 机械重数是唯一可靠拦截层。

## 1. 实体与范围：什么是 skill

【A】Agent Skills 开放标准（agentskills.io，Anthropic 2025-12 发起，30+ agent 产品采用）：skill = 一个目录，必含 `SKILL.md`（YAML frontmatter：`name` + `description` 必填）+ 可选 scripts/references/assets；核心机制 = **渐进式披露**——description 常驻上下文（约几十 token），正文按需加载，模型据 description 自动判断何时激活【来源：agentskills.io 规范转述（barrosohub/context-for-agent-skills-review-and-authoring）】

【A】Claude Code 对标准的私有扩展字段与本调研直接相关：`context: fork`（skill 在隔离子代理中运行，**独立上下文窗口**）、`disable-model-invocation`（仅用户可经 `/` 调用，防自动误触发）、`allowed-tools`（预授权工具白名单）、`hooks`（skill 生命周期钩子）【来源：同上规范文档】

【A】生态三头部仓库（2026-05 一周合计新增 ~34k stars，Juejin Valhalla 评测统计）：`anthropics/skills`（官方参考实现，165k+ stars，Apache 2.0，含 skill-creator 元技能——draft→测试 prompt→定性定量 eval→迭代循环）；`obra/superpowers`（方法论框架，~271k stars，MIT）；`mattpocock/skills`（工具集合，MIT）。另有社区市场 skillsmp.com 提供 `npx skills add <repo> --skill <name>` 标准化安装【来源：Juejin Valhalla 评测 + skillsmp.com 页面 + GitHub】

## 2. 事实层：候选 skill 证据（按本仓库步骤需求分组）

### 2.1 调研增强（Step 1/2）

【A】oh-rid/deep-research（MIT，Claude Code 插件）：`/research` 在 worktree 隔离中跑**三个独立 LLM 家族**（Claude WebSearch + Gemini 3.1 Pro via agy CLI + GPT-5 via codex CLI，各自不同搜索后端），结果分四组仲裁（Agreements/Gemini-only/GPT-only/Conflicts）；防御模型明文 = **"evidence weight > vote count"**——一条带主源 URL 且通过机械验证的少数派意见，胜过无源的双 LLM 共识；引用 consensus hallucination 文献（arXiv:2407.16604 Shared Imagination + arXiv:2510.19507）【来源：github.com/oh-rid/deep-research README】

【A】oh-rid 的主源验证是机械的：URL resolves 2xx + 引文段落**实际出现在抓取页面文本中**（grep 级），通过才准许入报告——非 LLM 自评【来源：同上】

【A】HadiFrt20/deepresearch：dr-adversary 对抗 agent 每 5 个完成任务攻击一次研究声明，四类检查——源验证（抓取被引 URL 核对内容）、反证搜索（negated queries 找 counter-evidence）、交叉引用独立性（"独立来源"是否其实同源）、时效检查（来源对时间敏感声明是否过旧）【来源：github.com/HadiFrt20/deepresearch README】

【A】Whiskysu/smart-search（搜索策略 skill，非工具）：五行为——recency triage（按信息保质期强制实时搜索）、领域源路由（五矩阵：地缘/技术/金融/生活/学术各配权威源）、anti-SEO 查询构造（避开 "best/top" 词型，强制追加反向查询 `[topic] problems/criticism/alternatives`）、利益层分析（谁在说/谁受益/省略了什么）、矛盾显式化（有标签的多立场而非单一自信结论）【来源：github.com/Whiskysu/smart-search README】

### 2.2 设计与实施流程（Step 3/5/7/9）

【A】obra/superpowers 14 skills 覆盖完整开发流（8 阶段）：brainstorming（创造性任务前置强制）、writing-plans、executing-plans、subagent-driven-development、dispatching-parallel-agents、test-driven-development、systematic-debugging、verification-before-completion、requesting-code-review、receiving-code-review、using-git-worktrees、finishing-a-development-branch、writing-skills、using-superpowers（元技能总开关）——**全部自动触发**（按 description 匹配，无需手动调用）【来源：github.com/obra/superpowers + CSDN/webreactiva 评测（二手）】

【A】superpowers brainstorming 的门禁设计：三路径分类（Spike/Bounded/Architectural）+ 单向棘轮（中途发现隐藏复杂度只能升档不能降档）+ **批准门不可缩放**（"a bounded task's approval is as hard a gate as an architectural one"——最简单任务也须呈现意图并获批准，防"太简单不需要审批"反模式）【来源：skillsmp.com/creators/obra/superpowers/skills-brainstorming SKILL.md 全文】

【A】superpowers verification-before-completion：AI 声称任务完成时强制要求**全新验证证据**（fresh evidence，非引用记忆），明示防"我觉得没问题"幻觉【来源：CSDN 评测表（二手）+ augmentclaude.com 条目】

【A】superpowers test-driven-development：RED-GREEN-REFACTOR 强制——先写失败测试、亲眼看它失败、写最小实现、亲眼看它通过、提交，"No skipping the red"【来源：augmentclaude.com 条目 + obra/superpowers README】

### 2.3 Review 增强（Step 4/6/8/10）

【A】swe-workflow/code-review-ensemble（nolanlawson triple-agent gist 的仓库化）：配置驱动多审查者（GitHub bots Bugbot/CodeRabbit + Claude 子代理 + Codex/Gemini/DeepSeek/Kimi CLI），审查者集合存 JSON 每仓可改；流程 = bot 触发→本地审查者并行→**编排者只在全部返回后才读代码**（"judges the reviewers instead of becoming a biased fourth one"）→交叉引用过滤幻觉，产出含 severity 排序 + per-reviewer agreement 表 + 被驳回幻觉条目（"issues reported by agents that turned out to be hallucinations — briefly explain why each was dismissed"）+ 合并建议；`disable-model-invocation: true` 显式调用【来源：github.com/swe-workflow/code-review-ensemble + nolanlawson gist】

【A】gthimmes/code-reviewer 设计规格（Draft v1）：北极星一句 = **"A review with zero findings is a valid output. A review with ten findings and one hallucination is a failure."**；硬性规则 = 零幻觉发现——每个 finding 必须引用 file + line range + **agent 输出前重新读取的引文片段**（"No line numbers from memory"）；精度优先于覆盖（3 真 1 漏 严格好于 10 真 2 幻）；四阶段管线（前置条件/大小门 → find → verify → 报告）+ 三档 strictness 参数化【来源：github.com/gthimmes/code-reviewer SPEC.md】

【A】swell-agents/coding-skills：`/coding-skills:review` = code-reviewer + security-auditor + architect-reviewer 三并行审查 agent 聚合为 Quality Gate Summary；AI-native review pass 默认关闭（opt-in，默认门 = 四遍机械 pass）——作者 2026-07 提交记录显示曾将 AI 审查从默认降为可选【来源：github.com/swell-agents/coding-skills README + 提交历史】

【A】wshobson/agents code-review-excellence（37.9k stars / 24.7k installs）：人因审查方法论——四阶段（上下文收集/高层/逐行/总结决策）+ 反馈规范（具体可行动/教育性非评判性/[nit] 标注非阻断）+ "Not the Goals"（不秀技/不 nitpick 格式/不无谓阻塞）【来源：claudemarketplaces.com/skills/wshobson/agents/code-review-excellence】

### 2.4 本地资产（零安装成本）

【A】当前 Trae 环境已内置大量可用 skill（system prompt available_skills 实测枚举）：deep-research（13-agent 管线）、literature-review、paper-lookup（10 学术库 REST）、exa-search、parallel-web、academic-paper-reviewer（5 独立评审人模拟）、peer-review、grill-me（计划拷问）、hook-analyzer 等 150+——**本地已具备大部分增强能力，无需社区安装**【来源：本会话环境实测（E1 级：system prompt 枚举）】

## 3. 十步 × skill 映射矩阵

> 判定维度：**接缝性质**（skill 与该步骤的硬规则是否同向）× **增量价值**（相对现有机制的净增益）。"生成端" = 提升产出质量/覆盖面；"验证端" = 强制拦截/取证（本仓库硬规则领地）。

| Step | 现有机制 | 候选 skill（A 类锚点） | 接缝判定 | 增量价值 |
|------|---------|----------------------|---------|---------|
| 1 调研 | 多 MCP 工具清单（§流程图） | smart-search（源路由/anti-SEO）+ 本地 paper-lookup/exa-search | 生成端同向 | 中——搜索策略纪律化，但工具已有 |
| 2 RESEARCH.md | A/B/C 分级 + 双源规则 + 门禁 (a)-(d) | oh-rid deep-research（三家族交叉 + 机械主源验证） | **混合**：其机械验证段与 RULE-5/A 类双源同构；其 LLM 仲裁段是自查 | **高**——三家族 = RULE-5 的执行形态；"evidence weight > vote count" 与 M7 规律③（机械枚举 > LLM 共识）完全同构，外部独立印证 |
| 3 DESIGN.md | design 模板 + 替代方案≥2 + 职责边界 | superpowers brainstorming（三路径 + 批准门 + 单向棘轮） | 生成端同向 | 中——批准门 ≈ 用户确认环节；棘轮 ≈ 门禁不可绕过精神 |
| 4 Review（设计） | RULE-1/4/5 + 门禁 | code-review-ensemble 模式（多审查者 + agreement 表 + 幻觉驳回栏） | **验证端接缝——受限复用** | 高（若审查者真异构）——agreement 表即 M7 对比臂的 skill 化 |
| 5 IMPLEMENTATION.md | 模板 + 版本/兼容性核查 | superpowers writing-plans（任务拆解到文件路径级） | 生成端同向 | 中 |
| 6 Review（实施） | RULE-4/5 + stdlib 下限检查 | gthimmes code-reviewer（零幻觉发现 + 引文重读 + 零发现合法） | **混合** | **高**——"No line numbers from memory" = E3 证据（行号绑 commit hash）的 skill 层先例；"zero findings is valid" = RULE-6(c) 诚实结果列同构 |
| 7 CHECKLIST.md | 可测试验收项 | superpowers writing-plans + requesting-code-review | 生成端同向 | 低——模板已覆盖 |
| 8 一致性 Review | 双向引用 + 断言延续（ADR-0008 D6） | 无直接对应（dc_validator 已机械化部分） | — | 低——本步已被本仓工具化领先 |
| 9 TDD | 先测试 + ADD Iron Law | superpowers test-driven-development（RED-GREEN 强制）+ verification-before-completion | 生成端同向 | 中——"防我觉得没问题" 与 Iron Law 同构 |
| 10 ADD 审计 | 取证矩阵 E1-E5 + 双向映射 + 诚实结果 | gthimmes（show your work）+ code-review-ensemble（交叉驳回） | **验证端接缝——受限复用** | 中——skill 可提升审查覆盖面，但**取证等级判定必须留在本仓硬规则** |

## 4. 吸收复用裁决（C 类判断）

【C】**主判断：三层吸收——"skill 供弹药（生成端），硬规则守边界（验证端），接缝处显式登记"。**

### 层 1 生成端自由吸收（skill 无强制语义的步骤）

Step 1/3/5/7/9 的 skill 增强直接可用（smart-search 搜索策略 / brainstorming 设计流程 / writing-plans 任务拆解 / TDD 强制）：这些步骤的产出本就要过下游 Review 与门禁，skill 只提升进入审查时的初稿质量。**零治理成本，无并存冲突**。

### 层 2 验证端受控复用（skill 触碰 RULE 领地的步骤）

Step 2/4/6/8/10 的 skill 复用受一条铁律约束：**skill 内置的"验证"仍是 LLM 自查，不可替代 E1 机械证据与门禁**（DIS-007 规律③：拦截层是机械枚举非 LLM 自查——skill 是更精致的 prompt，不改变这一层）。可复用的是其**结构性设计**而非其验证结论：
- code-review-ensemble 的 agreement 表 + 幻觉驳回栏 → M7 对比臂的输出格式强化
- gthimmes 的"引文重读后输出" → 审查者行为纪律（skill 可注入此行为，但重读结果仍须落取证矩阵）
- oh-rid 的机械主源验证（URL 2xx + 引文 grep）→ 与 dc_validator M5 同族的机械层，**该段可越过铁律**（它本身是机械检查的 skill 包装）

### 层 3 并存架构（"skill 与硬规则并存"的操作形态）

```
skill 层（软，生成端）──产出──→ 文档/代码
                                │
                                ↓
硬规则层（强制，验证端）：门禁 (a)-(d) → RULE-1~6 → dc_validator pre-commit → 取证矩阵 E1-E5
                                │
                                ↓
                        通过 → 入库（git commit）
```

并存的三条接缝：(i) **`context: fork` 是 RULE-1 的 skill 层物理化**——skill 在隔离子代理独立上下文运行，审查 skill 若配 fork 则时序独立天然成立（但 RULE-1 的判定权仍归流程：fork 是实现手段非规则本身）；(ii) skill 产出**必须流经同一硬规则漏斗**——无任何 skill 输出可豁免 pre-commit/门禁/取证；(iii) skill 的选用登记在 SPEC_PROCESS 附录（步骤 × 推荐候选 × 接缝条件），skill 本身**不进本仓库**（纯文档 + 最小工具层定位，P-012 层 4 先例）。

【C】**次判断：最高增量价值排序 = oh-rid 机械主源验证思想（Step 2，与 dc_validator M5 同族互证）> gthimmes 零幻觉审查纪律（Step 6，E3 同构）> code-review-ensemble agreement 表（Step 4，M7 对比臂同构）> superpowers 流程 skills（Step 3/5/9，与 SPEC_PROCESS 平行演化的外部互证）> 其余。**

值得单独登记的互证事实：superpowers（批准门/棘轮/验证前完成）、oh-rid（证据权重 > 投票）、gthimmes（零发现合法/禁记忆行号）三个独立社区项目，在未接触本仓库的情况下各自演化出与 RULE-1/RULE-6(c)/E3 同构的纪律——**这是 SPEC_PROCESS 有效性的第三次外部互证**（继 dsh 仓库工程实践、LANGGRAPH 反框架证据之后），且与前两次不同：这次是社区对"LLM 审查幻觉"问题的**平行解**，不是单一团队实践。

## 5. 风险与限制

【C】**风险判断：主要风险 = skill 层的信任越位与生态噪声。**

- **信任越位**（结构性风险）：skill 的自动触发（description 匹配）+ 预授权工具（`allowed-tools`）意味着生成端权限扩大；若使用者误将 skill 内置的 LLM 自查当验证（oh-rid 的机械验证段除外），DIS-007 的元断言逃逸就有了新入口。防御 = 层 2 铁律（skill 结论不豁免硬规则漏斗）
- **生态噪声**：社区 skill 无准入审查（Juejin Valhalla 评测对 anthropics/skills 自身都标注 injection_risk 命中项待人工复核）；三头部仓库 2026-05 一周 34k stars 的热度 ≠ 质量。防御 = 只吸收设计思想 + 本地已有 skill 优先（2.4 节：Trae 内置 150+ skill 已覆盖大部分需求）
- **触发不可控**：description 驱动的自动触发有漏触发与误触发双向风险（swell-agents 把 AI review 从默认降为 opt-in 即社区对误触发的实证反应）；多 skill 同时激活时优先级未定义
- **本调研局限**：未实测任何 skill 在本仓库工作负载上的表现（文献级证据）；skill 生态迭代极快（各仓库 last commit 均在数日内），快照即过时

## 6. 与在办任务的关系（PROGRESS 联动）

| 任务/机制 | 影响 | 动作 |
|-----------|------|------|
| SPEC_PROCESS | 步骤说明可增"推荐 skill 候选"注记（层 3 接缝 iii） | 本调研裁决后另行 ADR/修订（不并入本 feature） |
| P-008 独立 pass | oh-rid 模式（三家族交叉）为审查执行形态再添一选项 | 登记为选项（与 dsh 试点并列，优先级低于 dsh——后者有 JSONL 取证） |
| P-010 promptfoo | 互补不替代：promptfoo 评测矩阵 vs skill 执行增强 | 无 |
| M7 账本 | code-review-ensemble 的 agreement 表格式可强化对比臂登记 | 挂 P-010 执行时裁量 |
| P-012（dsh 调研） | 同属"外部生态吸收"谱系，层 1-4 分层框架同构 | 已互引 |
| P-013（本调研） | 新登记 | done（本文档） |

## 7. 开放问题（假设区，未取证）

- [H1] Trae 内置 skill（deep-research 等）的实际触发可靠性——system prompt 枚举了 150+ skill，但自动触发率/误触发率未在本仓库语境实测 — 查证路径: 下一个 feature 的 Step 1 实测记录触发行为
- [H2] oh-rid 三家族模式在本仓库可行——需要 agy/codex CLI 可用且其许可允许；三家族 = Claude+Gemini+GPT-5，与 RULE-5 的"异构基座"判定是否等价（家族 vs 基座的粒度差）未裁决 — 查证路径: P-008 执行时若选此形态，先跑单次 PoC
- [H3] `context: fork` 在 Trae 环境的可用性与语义（标准字段，但各 agent 产品实现程度不一）— 查证路径: Trae 文档/实测
- [H4] 社区 skill 的供应链安全（Valhalla 评测对 anthropics/skills 标注的 injection_risk 命中项性质未查明细）— 查证路径: 若采纳任何社区 skill，先读其 SKILL.md + scripts 全文

## 附录 B: 断言登记表（机器可读）

```json
[
  {
    "id": "B1",
    "type": "推断",
    "claim": "oh-rid 的'evidence weight > vote count'与 M7 规律③（拦截层是 E1 机械枚举非 LLM 自查）同构——两者都主张机械可验证证据优先于 LLM 共识，且 oh-rid 引用的 consensus hallucination 文献（arXiv:2407.16604）与本仓库 RULE-5 依据的 MAD 文献（arXiv:2502.08788）指向同一失效模式",
    "basis": "§2.1 oh-rid README 实证 + M7 规律锚点 + RULE-5 依据文献",
    "verified": false
  },
  {
    "id": "B2",
    "type": "推断",
    "claim": "层 2 铁律（skill 内置验证不可替代 E1 机械证据）可由 DIS-007 直接推出——skill 本质是上下文注入（渐进式披露的 prompt），其内置'验证'行为仍是生成端 LLM 自查，规律②'防幻觉机制自身不设防'适用于任何 prompt 级机制",
    "basis": "§1 开放标准机制 + DIS-007 命题 + 规律②③",
    "verified": false
  },
  {
    "id": "B3",
    "type": "推断",
    "claim": "Trae 内置 skill 已覆盖本调研识别的大部分增强需求（150+ 枚举含 deep-research/literature-review/peer-review/academic-paper-reviewer），社区安装的净增量主要在 code-review-ensemble 式多审查者编排与 superpowers 式流程门禁",
    "basis": "§2.4 本地枚举 × §3 映射矩阵对照",
    "verified": false,
    "depends_on": "H1"
  },
  {
    "id": "B4",
    "type": "推断",
    "claim": "MCP 工具响应可直接登记为 RULE-6 取证矩阵 E1 级证据（API 调用可重放、第三方可复核），使 Step 2 引文验证从'WebSearch 快照旁证（E2/E3）'升级为'结构化 API 记录（E1）'——依据 §8.2 直测（返回结构化 paper_id/DOI/摘要字段）与 E1 定义（可重放命令/输出）的组合，尚未在真实 feature 的取证矩阵中实际登记过 MCP 响应",
    "basis": "§8.2 直测实证 + SPEC_PROCESS 取证矩阵 E1 定义",
    "verified": false,
    "depends_on": "H6"
  }
]
```

## 附录 C：来源清单

| 编号 | 来源 | 类型 | 取证日 |
|------|------|------|--------|
| S1 | agentskills.io 规范（经 barrosohub/context-for-agent-skills-review-and-authoring 转述） | 一手（标准）转述 | 2026-08-20 |
| S2 | github.com/anthropics/skills（README + 目录 + skill-creator SKILL.md） | 一手 | 2026-08-20 |
| S3 | github.com/oh-rid/deep-research（README） | 一手 | 2026-08-20 |
| S4 | github.com/HadiFrt20/deepresearch（README + 提交历史） | 一手 | 2026-08-20 |
| S5 | github.com/Whiskysu/smart-search（README） | 一手 | 2026-08-20 |
| S6 | skillsmp.com/creators/obra/superpowers/skills-brainstorming（SKILL.md 全文预览） | 一手 | 2026-08-20 |
| S7 | github.com/obra/superpowers + tiboo00 fork（README） | 一手 | 2026-08-20 |
| S8 | github.com/swe-workflow/code-review-ensemble（README + CONFIG） | 一手 | 2026-08-20 |
| S9 | gist.github.com/nolanlawson/4150b0ca（code-review-turbo SKILL.md 全文） | 一手 | 2026-08-20 |
| S10 | github.com/gthimmes/code-reviewer（SPEC.md 全文） | 一手 | 2026-08-20 |
| S11 | github.com/swell-agents/coding-skills（README + 提交历史） | 一手 | 2026-08-20 |
| S12 | claudemarketplaces.com/skills/wshobson/agents/code-review-excellence | 一手（SKILL.md 全文） | 2026-08-20 |
| S13 | Juejin Valhalla《anthropics-skills 源码证据驱动评测》（三仓库定位/star 统计/injection_risk） | 二手 | 2026-08-20 |
| S14 | CSDN《Claude Code 中 Superpowers 的使用》+ webreactiva.com superpowers 评测（14 skills 清单） | 二手 | 2026-08-20 |
| S15 | augmentclaude.com/s/superpowers-obra（TDD/verification 细节） | 二手 | 2026-08-20 |
| S16 | 本会话 Trae 环境 system prompt skill 枚举 | E1 实测 | 2026-08-20 |
| S17 | github.com/openags/paper-search-mcp（README 全文 + fork 生态：mtnnn/upascal/BlaineHeffron/its-antony） | 一手 | 2026-08-20 |
| S18 | 本会话 mcp_paper-search `search_arxiv` 直测（主题查询 + 标题精确检索，两组） | E1 实测 | 2026-08-20 |
| S19 | 本会话 mcp_stackexchange `search_questions` 直测（默认站点/site 参数/单词宽匹配/多词 AND，四组） | E1 实测 | 2026-08-20 |

---

## 8. 补充调研：MCP 工具层 vs Skill 层（v1.1 新增，2026-08-20）

> **任务来源**: 用户追问"相比于 skill，增强 MCP 工具使用是否可以提升框架性能、信息真实性？比如学术调研使用 paper-search MCP 工具，或者 stack-exchange MCP 工具"
> **方法差异**: §2 为文献级取证（读 README）；本节对本地已连接的 MCP 工具做**本会话直测**——MCP 响应即机械可重放证据（E1），"用 MCP 调研 MCP"本身是本节论题的现场演示。

### 8.1 本地 MCP 资产现状

SPEC_PROCESS Step 1 已登记四个 MCP：mcp_paper-search / mcp_english-search / mcp_research-tools / mcp_scholar-mirror；本会话另连接 mcp_stackexchange（五工具：search_questions / get_answers / get_question / list_sites / list_pipeline_sites）。**MCP 增强不是引入新事物，而是深化既有配置的使用模式与证据地位**——与 skill 增强（引入新生态）性质不同。

### 8.2 直测实录（E1 级证据）

【A】mcp_paper-search `search_arxiv` 主题查询实测（query="multi-agent debate large language models", max_results=3）：返回 3 条真实 arXiv 论文的**结构化记录**——paper_id / title / authors / abstract / doi / pdf_url / url / source / categories 字段齐全（首条 2511.13930 仿真材料发现，次条 2203.08975 MADRL 综述）【来源：S18】

【A】标题精确检索实测（query="Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs"）：**精确命中** arXiv 2311.17371（Smit et al.，含完整摘要与 pdf_url）——Step 2 Review 的"引文验证"场景可直接用 MCP 完成，且命中记录本身即 E1 证据【来源：S18】

【A】mcp_stackexchange `search_questions` 直测：**默认 site = mathoverflow**（CS 查询须显式传 site=stackoverflow）；site 参数生效后（query="python list comprehension"）返回 10 条高相关结构化结果——question_id / title / url / score / answer_count / accepted_answer_id / tags / view_count / owner.reputation 字段齐全【来源：S19】

【A】mcp_stackexchange 召回偏差实测：单词宽匹配（query="hallucination"@stackoverflow）返回 10 条**主题无关**结果（Switch enum 自动填充、UIView 属性等——StackExchange API 文本匹配命中正文/答案而非标题）；多词 AND 匹配（query="LLM hallucination detection"@stackoverflow）**零命中**。结论：**E1 真实性 ≠ 语义相关性**——返回的是真实 API 数据，但可能答非所问【来源：S19】

【A】本地 mcp_paper-search 工具清单（search_papers / search_arxiv / search_pubmed / download_with_fallback / read_arxiv_paper / search_semantic / search_crossref / search_openalex 等 40+ 工具）与开源项目 **openags/paper-search-mcp**（Python，MIT，free-first 原则，两层架构：Layer 1 统一 `search_papers` 多源并发去重 + `download_with_fallback` 顺序回退；Layer 2 平台连接器）完全吻合；该项目有活跃 fork 生态（mtnnn / upascal / BlaineHeffron Rust 重写 / its-antony 服务化重构）——**本地资产即开源社区主流项目的部署实例**【来源：S17】

### 8.3 MCP 与 Skill 的结构对比

| 维度 | Skill（§1-§4 已调研） | MCP 工具（本节） |
|------|----------------------|-----------------|
| 本质 | 上下文注入——教模型**怎么做**（策略层） | 工具接口——让模型**能触达什么**（数据层） |
| 产出证据等级 | **E4**（LLM 判断陈述——skill 再好，"我验证过了"仍是自述） | **E1**（API 响应——结构化、可重放、第三方可复核） |
| 对信息真实性 | 间接：改变行为 → 希望产出更真 | 直接：返回真实数据，引文可机械核对 |
| 对框架性能 | 提升搜索策略质量（smart-search 式） | 扩展可达性（30+ 学术库一接口） |
| 失效模式 | 元断言逃逸（规律②——防幻觉机制自身不设防） | 内容错配（EuropePMC 前科）/ 召回偏差（8.2 实测）/ 镜像差异（scholar-mirror 前科）/ 默认配置陷阱（site=mathoverflow） |
| 验证责任 | 仍需下游门禁兜底 | 仍需证据身份验证（双源 + 内容核对） |
| 与硬规则关系 | skill 产出必须流经硬规则漏斗（层 2 铁律） | MCP 响应**本身是漏斗要生产的证据**（E1） |

本仓 MCP 失效前科（E3 级，历史登记）：EuropePMC DOI 查询返回无关 PLOS One 论文（链接有效内容错配，CODE_WIKI 案例库）；scholar-mirror 镜像差异曾致四源冻结裁决（NP2 τ_T(k) 案例）。两条均支持同一结论：**MCP 提高证据的机械真实性，但不豁免内容核验**。

### 8.4 对十步流程的落点

| Step | MCP 增强落点 | 证据升级 |
|------|------------|---------|
| 1 调研 | paper-search 统一接口替代散装 WebSearch（多源并发 + 去重） | 覆盖面：30+ 学术库一接口 |
| 2 RESEARCH + Review | "arXiv 编号已验证"项：WebSearch 快照旁证 → `search_arxiv` 精确命中记录 | **E2/E3 → E1**（B4 推断） |
| 2（工程域） | stackexchange 补充源（site 显式指定 + 查询公式纪律） | 新增工程问答域 |
| 10 取证矩阵 | 新行型：取证手段 = "mcp_paper-search search_arxiv（E1）"，结果 = paper_id 命中 | 取证手段扩容 |

### 8.5 裁决（C 类判断）

【C】**主判断：对"信息真实性"目标，MCP 增强结构性优于 skill 增强——因为两者的证据等级由构造决定（E1 vs E4），不是使用水平问题；但对"框架性能"目标两者正交互补（MCP 供数据可达性，skill 供搜索策略），最优形态是"MCP 出证据、skill 出策略、硬规则出裁决"三层分工，与 P-013 主判断（skill 供弹药/硬规则守边界）合并为完整架构：MCP 是弹药的原材料（真数据），skill 是使用弹药的战术（怎么搜），硬规则是开火授权（何时必须验）。**约束不变：MCP 响应的 E1 真实性不豁免证据身份验证（双源规则与内容核对仍适用——8.2 召回偏差实测与本仓 EuropePMC 前科共同证明"真实 API 也返回无关内容"）。

### 8.6 补充假设区（v1.1 新增）

- [H5] mcp_stackexchange 对本仓工程问答域的净增益为正——本仓目前零使用记录，且召回对查询公式敏感（8.2 实测）— 查证路径: 下一个涉及工程实现细节的 feature（如 P-009 runner）Step 1 实测登记命中率
- [H6] MCP 响应入取证矩阵的登记格式可行且成本可接受（B4 的验证）——取证矩阵目前零 MCP 行 — 查证路径: 下一个 feature 的 Step 10 首次登记 MCP 响应行（含工具名 + 参数 + 关键返回字段）

---

**Review 签字**: _________ 日期: _________（本报告为 `自查（单视角）` 产出，按 RULE-4 须经独立 pass 复核后方可标记 `[已复核]`）
