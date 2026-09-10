---
id: academic-writing-workflow-RESEARCH
type: design
version: 1.3
status: in-review
date: 2026-09-11
depends: [community-ecosystem-RESEARCH, loop-engineering-RESEARCH, DISTRIBUTED_AGENT_RESEARCH, ADR-0010]
upstream: null
---

# 调研文档：学术推理写作工作流——与当前框架的同构分析（P-040）

> **Feature**: 学术推理写作工作流的工程化管理（LGMM 场景驱动）
> **创建日期**: 2026-09-11
> **状态**: in-review（调研批，Step 1-2）
> **Spec 步骤**: Step 1-2（调研 + 三问懒加载门禁）
> **任务来源**: 用户指令「执行另一个与当前框架存在同构关系的调研任务 以学术推理写作为例 一般包含 调研 缺口分析 初步设想 模型方法构建 数据获取 初步结果 草稿撰写 模拟评审 反馈迭代 每一个步骤都会产生连锁式影响 且需要频繁进行审查 修改 需要控制版本 保持数学-算法实现-数据-结果-论文表达一致性 每一步改动都要自动产生下一步状态提醒 以用户学术仓库为例 D:\Article\Working paper\LGMM ... 同时需要记录研究日志 路线 变更历史 用户在学术推理中面临各种复杂的管理 验证 请结合用户场景 开源社区优秀案例进行分析」
> 参考先例: P-039 分布式 Agent 执行（同构框架调研批）、P-028 loop engineering、P-018 community-ecosystem
> **v1.1 补充调研（用户指令「补充调研 学术推理写作与当前框架开发中 有什么UI工具框架可以实时反馈工作流 状态 阶段 防止用户认知过载出现漂移 遗忘 / 学术推理中也包含ai工作流 也需要进行结果审计 决策链追溯 严格抑制幻觉 且每一个步骤可能包含微工作流 如何实现 / 学术写作中的连锁反应必须建立某种硬规则 类似图结构 状态机等模式 请仔细搜索开源社区 学术研究等信息 进行深度调研」）**: 新增 **§7 补充调研——UI 实时反馈与认知防过载**（AgentGUI / 认知负荷心理物理实证 / Msft AI brain fry / Racc 认知设计原则 / LLM observability / AutoGPT 三级粒度）、**§8 补充调研——AI 工作流审计·决策链追溯·幻觉抑制·微工作流嵌套**（COCO / AWorld Guard / 形式化护栏 AgentGuardian+ACM / W3C PROV / auditable-ai 谱系 / 幻觉抑制生成侧 / HAACS 层级 Petri 网）、**§9 补充调研——链条连锁反应硬规则（图/状态机）**——**13 条新 A**（A-15~A-27）+ **B5/B6/B7** + **C-4/C-5** + **H3/H4**；断言 **A 14→27 / B 4→7 / C 3→5 / H 2→4**（附录同步，参考文献顺延 **§10**）。
> **v1.2 补充调研（用户指令「本仓 doc-first + 每 feature 事件流独立 但是存在上下文问题 ai输出冗长且大量信息需要用户反馈 用户缺失存在认知过载 且用户在开发研究过程中需要经常注入外部信息 在主线开发研究过程中也需要fork形成支线探索 / UI 实时反馈 / 认知防过载 实现自动化追踪 任务看板等类似功能 需要仔细调研分析一下」）**: **织界线修正 C-5 前提**（per-feature 事件流独立 = **多流并存**非单流，+ fork 支线 + 长输出 + 频繁外部反馈 → 本仓认知过载**真实存在**，故不"免征"亦不"排除一切 UI 层"）——新增 **§10 补充调研四——任务看板与自动化追踪**（Magentic One Task/Progress Ledger 二账本 / Backlog.md + Markdown Task Board + Kanban.md markdown 原生看板 / git worktree + log graph fork 可视化）——**4 条新 A**（A-28~A-31）+ **B8** + **C-6** + **H5**；断言 **A 27→31 / B 7→8 / C 5→6 / H 4→5**；**裁定=C-6**（本仓认知过载缓解的正确形态 = **markdown-native 只读看板生成器**（stdlib，聚合 PROGRESS+sessions verdict 为单行认知块，按状态分组）+ git worktree/log graph 表达 fork——**零 GUI 服务器/零新依赖/AI 可写**；**仍按懒加载 gate**，仅登记概念，零代码改动，触发条件=用户明确要求落地 board 生成器）；参考文献顺延 **§11**。
> **v1.3 补充分析（用户指令「看板生成器具体设计是否能够实时反馈 自动抓取 自动状态更新 而不用依赖用户指令 请补充分析」）**: 明确回答 = **可以，且三条自动触发路径均已成熟**——① **事件驱动自动抓取**（改 PROGRESS/SOURCES 源头即触发；`watch-inbox.ps1` FileSystemWatcher 实作"文件变化→自动处理"模式、.NET FileSystemWatcher 为 Windows 本地零新依赖方案）；② **门禁钩子自动重生成**（do-knowledge-studio/*_skill `update-docs.mjs` + GitHub Actions push→自动更新生成节 + pre-commit 自动更新文档区、ProjectOdyssey badge 自动计数防 drift——本仓已有 pre-commit 四 hook/repo_stats 机械对账，**直接把 board 生成器并进 step-gate/pre-commit 即为"提交即刷板"，零新依赖**）；③ **终端实时渲染**（agent_pulse/cc-aio-mon = 轮询 temp(500ms 刷新 snapshots → 全屏 TUI progress bar，非阻塞不依赖用户指令 / Rich Live refresh_per_second=4 / minimal-tui rich+tqdm stdlib 主、省依赖）——纯 stdlib `watch -n` + 终帧重绘即可达同效（无需引入 rich/tqdm/Textual 重依赖，与零依赖 D6 一致）；**按 Clash 断言分层 A-32~A-34 + B9**，**裁定 C-7 = 看板可"被动由事件/hook 自动更新 + 可选主动终端轮询展示"，完全脱依赖用户指令**；三档自动强度（L0 门禁触发=提交自动刷 / L1 文件监听=源头改动即刷 / L2 终端轮询=常驻实时刷新）；懒加载 gate 保持，触发仍=用户要求落地 board 生成器；参考文献顺延 §12。
> **核心目的**: 确认"学术推理写作工作流"与本仓 Spec 驱动框架的**同构性**——把 LGMM 场景的痛点映射到本仓既有机制，识别社区可借鉴构件，判定是否需吸收/承接。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 34 | A-1 用户步骤链 / A-2 LGMM 证据链痛点实证 / A-3 数学-实现断点 / A-4 SciTeX 交口控制 / A-5 交互 literate 编程（Quarto/knitr） / A-6 跨模型审稿 / A-7 PaperJury / A-8 Agentic_Paper 多臂 / A-9 eLabFTW ELN / A-10 auto-research 阶段门 / A-11 Lean4-Coq 一致性 / A-12 预注册-版本化（paper-template Zotero） / A-13 LGMM 已有机制盘点 / A-14 本仓同构机制盘点 / A-15 AgentGUI 观察+转向 / A-16 认知负荷心理物理实证 / A-17 微软 AI brain fry / A-18 Racc 认知设计原则 / A-19 LLM observability 平台 / A-20 AutoGPT 三级事件粒度 / A-21 COCO 连续监督 / A-22 AWorld Guard 防幻觉 / A-23 形式化护栏（AgentGuardian CFG+ACM） / A-24 W3C PROV 溯源标准 / A-25 可审计 AI 谱系 / A-26 幻觉抑制生成侧 / A-27 层级状态机/嵌套子网 / A-28 Magentic One 二账本 / A-29 Backlog.md markdown 看板 / A-30 Markdown Task Board 零依赖板 / A-31 git worktree+log graph fork / A-32 FileSystemWatcher 事件驱动自动抓取 / A-33 hook+CI 门禁自动重生成 / A-34 终端实时轮询渲染（agent_pulse/Rich Live） |
| B 推断类 | 9 | B1 步骤链=非线性依赖图 / B2 状态提醒=宏写者序列的推进提示 / B3 一致性=多对象证据绑定 / B4 分步治理=spec 门禁的推广 / B5 认知防过载=状态压缩+主动微介入 / B6 硬规则=状态机+物证门+seq 记录 / B7 审计幻觉抑制=证据锚点化跨层校验 / B8 本仓多流=需聚合看板 / B9 自动刷新=事件/hook/轮询三路径 |
| C 判断类 | 7 | C-1 同构成立 / C-2 分阶段吸收 / C-3 门禁判定（本期止于调研） / C-4 三新维度同构成立 / C-5 补充裁定（仍止于调研，零工具改动） / C-6 织界线修正（markdown 看板生成器方向，仍懒加载） / C-7 自动刷新可行（事件/hook/轮询，脱用户指令） |
| 假设区 | 5 | H1 步骤链是否需要 DAG 依赖映射 / H2 数学-实现上场时是否引入 Lean4 性价比未实测 / H3 本仓是否需要可视化/UI 展示层 / H4 链条上游依赖发现是否需要显式依赖元数据 / H5 看板生成时机（按需 vs 自动刷新）——v1.3 部分回答=三档自动强度（L0 门禁/L1 监听/L2 轮询）但各档开销未实测 |

---

## 1. 调研目标

**核心问题**:
1. 学术推理写作工作流（调研→缺口→设想→模型→数据→初结果→草稿→模拟评审→反馈迭代）与本仓 Spec 驱动框架是否**同构**？同构点在哪？
2. LGMM 实证审计暴露的"数学-算法-数据-结果-论文表达一致性"问题，能否被本仓的"声明=重数 + 证据链 + 门禁"机制承接？
3. 社区开源案例中哪些是可直接借鉴构件，哪些需改造，哪些与本仓重叠应规避？
4. "每步改动自动产生下一步状态提醒"、"研究日志/路线/变更历史"的需求，社区如何实现，本仓的 spec_runner 事件流是否已覆盖？

## 2. 用户场景解剖（AGENT 即用户，LGMM 为锚点）

### 2.1 用户给出的九步学术推理写作链（A-1）

【A】A-1: 用户将学术推理写作分解为九步，每步间**连锁式影响**且需**频繁审查修改**、**控制版本**、保持**数学-算法-数据-结果-论文表达一致性**、每步改动**自动产生下一步状态提醒**，同时需记录**研究日志、路线、变更历史**：
> 调研 → 缺口分析 → 初步设想 → 模型方法构建 → 数据获取 → 初步结果 → 草稿撰写 → 模拟评审 → 反馈迭代

### 2.2 LGMM 证据链审计揭示的工程痛点实证（A-2 / A-3）

【A】A-2: **LGMM 8.0 证据链审计（2026-09-10）已定稿**，暴露实证管线的一致性断裂：论文数学（`eq:lgmm_obj` 横截面 GMM 因子溢价 λ̂ = (Ḡ'ŴḠ)⁻¹Ḡ'Ŵḡ，Σ_i 跨资产 + 工具变量 Z + HAC 权重）与主实证代码（`rolling_lgmm_*` 三副本，λ̂_jt = Σ_t w_t·r_jt / Σ_t w_t，**收益加权平均**）**估的不是同一个对象**。来源：[外部·证据链审计](file:///D:/Article/Working%20paper/LGMM/LGMM%208.0/docs/audit/2026-09-10-empirical-estimator-evidence-chain.md)
【A】A-3: **该断点的性质 = "类型差异"升级为"估计对象不同"**：设计文档 `<docs/spec/review_repair_m1_m8_design.md> §3.1 符号核对表与论文一致，但代码三副本未消费 `lgmm_core.lgmm_at_t0`（真正实现横截面矩条件的唯一版本）。数值铁证：探针 `lam[0,30]=0.004935` == Epanechnikov 加权平均==相等。→ **同一符号 λ̂ 在 论文/设计/代码 三层指代不同对象，恰是本仓最痛恨的"声明≠重数"。**

## 3. 社区开源案例调研

### 3.1 手稿版本控制与审稿反馈（SciTeX Writer / paper-template）（A-4）

【A】A-4: **SciTeX Writer** 提供模块化 LaTeX 手稿管理：`make archive`（时间戳+版本号归档）→ `make diff`（**latexdiff 高亮版本间改动**）→ revision 目录承载多轮审稿（subdirectories per round）。**paper-template**（GitHub Actions）每次 commit 自动编译 PDF + Pages 发布，解决"最新版本在哪"。→ 命中用户"控制版本 + 频繁审查修改"痛点，对应本仓 `git` + 版本化。

### 3.2 可执行论文 / 交互编程（Quarto / knitr / Jupyter）（A-5）

【A】A-5: **literate programming**（Knuth 1984）使"数据→代码→输出→手稿"单一来源：Quarto 成为主流，**改数据/代码自动重跑并传播到手稿**，消除"结果复制粘贴进论文"的断点。研究仅 8.5% 的 Jupyter 笔记可原样复现。→ **直接对应"数学-算法-数据-结果"一致性**：把结果内联到手稿，从根上防 A-3 式数字断章取义。

### 3.3 跨模型模拟评审 + 反馈迭代（ARIS / PaperJury / Agentic_Paper / AutoReviewLoop）（A-6/A-7/A-8）

【A】A-6: **ARIS（Auto research in sleep）核心 = 跨模型审稿**：Claude Code 执行，外部 LLM（Codex 等）评审，明确论证"单模型自审是 stochastic bandit（噪声可预测）→ adversarial bandit（审稿者探测执行者盲区）更难被 game"；两模型逼近 Nash 均衡是打破自我博弈的最小配置。持 `REVIEW_STATE.json`（round/status/score）+ `AUTO_REVIEW.md`（累计变化日志）。→ **与本仓 RULE-5 异基座第二会话高度同构**，且给出"2 个审稿者为何最优"的论据。
【A】A-7: **PaperJury**：CONF-venue 三模式（direct-edit / **review 对抗式法庭** / auto），review 引擎 = N 域 reviewer → contestability routing → 双向庭审 → 三方判决 → **clerk-converged 多轮循环**，**共识门控 + 作者签字**，issue 记入 **durable ledger**。auto 模式：drift-bounded 安全修复 + 风险项排队待人工。
【A】A-8: **Agentic_Paper**：12 个并行 reviewer agent（Methodology/Results/Citation Validator/Statcheck 等）+ 协调器综合裁决。arXiv 2511.10902：RQ-OpenReview 审稿模拟 + **Action:Objective[#] 可执行 to-do** 列表。→ 命中"模拟评审+反馈迭代"，比本仓现有人工异基座 pass 更结构化。

### 3.4 电子实验记录本 ELN（eLabFTW / OSF）（A-9）

【A】A-9: **eLabFTW**：审计防篡改（**数据不可删、改动带时间戳留痕**）+ 版本历史 + 锁定归档 + FAIR 元数据；解决"记录断档/文件分散/版本失控"三丢。OSF 提供预注册+项目全生命周期管理。→ 对应本仓 M7 证据账本（append-only）+ 事件流。

### 3.5 全生命周期阶段化研究（auto-research 8 phases / 4 gates）（A-10）

【A】A-10: **auto-research**（Claude Code 插件）：研究全生命周期 **8 phases / 4 user gates** 自动工作流（survey→idea→实验→draft），`LAB_NOTEBOOK.md` 作**单一 living document 时序"思考航海日志"**。→ 与本仓 SPEC_PROCESS 十步阶段化 + per-feature session + step-gate 高度同构。

### 3.6 数学-实现一致性：形式化验证（Lean4 / Coq）（A-11）

【A】A-11: 形式化验证（Lean4 Mathlib / Coq, LF-lean 类型同构验证 / Lean Workbook 57K 题）把"数学结论成立"变成**机器可校验**。但桥接成本高（数学被形式化 → 手动翻译易错 → 需求类型同构）。→ 对应本仓"数学表达一致性"痛点：Lean4 是**终极但最重**的解法；对本仓 M7（文档断言）+ A-3 式"实现对象"抽查而言，**替代方案 = 符号核对表 + 探针断言**（LGMM 已用数值探针）。

### 3.7 版本化文献（Zotero + Better BibTeX + Git 锚定）（A-12）

【A】A-12: Zotero+LaTeX+Git 模板用 **Git Submodule + 触发式导出 + git notes 元数据锚定**解耦 BBT 导出与 GUI，构建确定性文献版本控制。→ 命中"引用一致性"。

## 4. 同构性分析：学术写作链 ↔ 本仓 Spec 框架

### 4.1 九步链的本质 = 非线性依赖图，非线性流水线（B1）

【B】B1（见附录 B）: 用户"九步连锁影响"表明**上游改动向右游传播、下游发现反噬上游**——这是**依赖图**而非线性管道。本仓 SPEC_PROCESS 十步 + step-gate 的 STEP_SEQUENCE 是线性骨架，但**事件流（append-only + seq 单调）天然支持 fork/replay**。社区（auto-research 8 phases / PaperJury 多轮）也把链当作**可循环**而非一次性。→ 同构成立点为"**分步 + 门禁 + 可回溯**"。

### 4.2 "每步改动自动产生下一步状态提醒" = 推进提示（B2）

【B】B2（见附录 B）: 社区实现 = spec_runner 事件流 append-only 后，由**读取方**消费 seq 判定推进；auto-research 用 8 phases 明确 next gate；ARIS 用 REVIEW_STATE.json。本仓 spec_runner 已落 append-only + seq + replay/fork，**"自动提醒"= 一个读取 seq 并打印"下一步该做 Gate N"的轻壳**，机制零新增。→ **最大同构点：不欠账**。

### 4.3 "数学-算法-数据-结果-论文一致性" = 多对象证据绑定（B3）

【B】B3（见附录 B）: A-3 断点的根治 = 让 **λ̂ 在论文/设计/代码/结果四层绑定到同一对象标识**。社区三条路：(a) literate（Quarto 内联结果，A-5）；(b) Lean4 形式化（A-11）；(c) 符号核对表 + 数值探针（LGMM 已用）。→ 本仓对应 = "声明=重数" + verify-anchor + M7 证据分级 E1（可重放命令）。**LGMM 缺的是把这条绑定做成例行 guard**（审记建议"固化为例行 guard，M-12 引述"）。

### 4.4 分步治理 = spec 门禁的推广（B4）

【B】B4（见附录 B）: "模拟评审→反馈迭代" 社区用跨模型/multi-arm（A-6/7/8）；本仓用 RULE-5 异基座独立 pass。**两者同旨**：把"作者自评"替换为"独立评审者"。ARIS 的"两模型即最优"论据直接支持本仓 RULE-5。

### 4.5 LGMM 仓库已有机制盘点（A-13）

【A】A-13: LGMM 8.0 已在实践（非本仓）：`docs/spec/`（engineering_constraints_* 四份：research/design/implementation/checklist —— 直接对标本仓四件套）、`docs/audit/`（含 2026-09-10 证据链）、`memory/`、`roadmap/`、`lean4/`、`data_lineage_v8.1.md`、`MAPPING_v8.2.md`、`review_repair_m1_m8_*` 族、`SPEC_DRIVEN_DEVELOPMENT.md`。→ **用户已在用 spec-driven + 审计 + lineage + lean4 的组合，本仓框架是这套的自举/增强，非全新引入。**

### 4.6 本仓既有同构机制盘点（A-14）

【A】A-14: 本仓已具备承接学术写作链的全部机制：SPEC_PROCESS 十步 + spec_runner 事件流（append-only/seq/replay/fork）+ step-gate 三类规则 + verify-anchor 锚点核查 + **FWK-DECISION-RECORD 八字段**（决策记录）+ **M7 证据账本**（反幻觉 + 分级 E1-E5）+ RULE-5 异基座独立 pass + 三校验器（dc_validator/m7_stats/repo_stats）」+ PROGRESS（进度/路线）+ CODE_WIKI（变更历史/索引）。**研究日志=事件流，路线=PROGRESS/roadmap，变更历史=git+CODE_WIKI。**

## 5. 收敛裁定

【C】C-1（见附录 C）: **同构成立**。学术推理写作工作流与本仓 Spec 驱动框架共享同一组不变量：分步阶段化、每步一个决策/产物、门禁审查、证据绑定、可回溯、声明=重数。用户九步链 ↔ SPEC_PROCESS 十步；模拟评审↔异基座独立 pass；一致性↔视重数+证据链；状态提醒↔事件流 seq。**特色项（数学-实现一致性）是本仓的 feature 级应用，不改变框架同构性。**

【C】C-2（见附录 C）: **分阶段吸收该概念**（Layer-0 概念登记 + 分步采纳）：
- **立即候选（零新依赖）**：把"同符号跨层指代不同对象"的检查固化为**例行 guard**（对应 LGMM M-12/M-08）——符号核对表 + 数值探针断言，挂到本仓 step-gate/校验器同族。
- **候选（懒加载）**：literate 结果内联（Quarto）若在 LGMM 采用则与本仓 verify-anchor 重叠定位需对齐；跨模型模拟评审（含 ARIS "2 模型最优"论据）若在 LLM 端落地则复用 RULE-5。
- **否决/重（代价）项**：Lean4 全量形式化（A-11）在字数/工作量上不划算（本仓/实证文档层，非定理级），仅当"数学断言需机器级确证"时按用例进 ADR-0010 三问。

【C】C-3（见附录 C）: **本期止于调研（懒加载 gate）**，不实施工具改动。理由：Q1 属 Layer-0 概念登记 + 通过本仓既有机制承接，不新增 layer-1 组件；Q2 无明确激活触发（LGMM 一致性 guard 属外部仓库，非本仓 feature）；Q3 零工具副作用。**不重复造轮子**，不引入社区框架本体（SciTeX/Quarto/eLabFTW 均为外部重型平台，与本仓单写者+文档层的轻量定位冲突）。

【C】C-4（见附录 C，v1.1）: **三新维度同构成立**：① **UI/认知防过载**（§7）→ 本仓 doc-first + 每 feature 事件流独立（**v1.2 修正**：实为 per-feature **多流并存**非单流，过载真实存在；见 §10.1/C-6）；缓解=吸收"状态压缩 / 主动微介入 / 嗅探线索"为聚合**看板**展示原则，无需引入重型 UI 框架。② **AI 工作流审计/决策链追溯/幻觉抑制**（§8）→ = 本仓 M7（断言分级 E1-E5，同 COCO 集成分歧/AWorld 双角色/ACM 形式护栏同旨）+ RULE-5（异基座独立臂）+ decision 八字段（决策链，同 PROV）+ verify-anchor（证据锚点）；LGMM 证据链审计即其实证。③ **链条连锁反应硬规则**（§9）→ = 本仓 spec step-gate **状态机**（steps=状态 / gate=转移守卫 / seq=状态历史），与 AgentGuardian CFG / ACM security automaton / PROV-CONSTRAINTS 同一手法。
【C】C-5（见附录 C，v1.1）: **补充裁定——仍止于调研（懒加载 gate 保持，零工具改动）**：① 认知防过载 UI = **Layer-0 概念登记**（Racc 四原则 + AutoGPT 三级粒度）；**v1.2 修正**——本仓实为多流并存故过载真实，正确缓解 = markdown 看板生成器（§10/C-6），**不引入** AgentGUI/LangSmith/Langfuse 重型平台本体（仍成立）。② 幻觉抑制 = **复用既有**（RULE-5 + M7 + verify-anchor + C-2 已承诺的"同符号跨层对象绑定"例行 guard），不新增；③ 链条硬规则 = 明确"**状态机表达 + 每转移物证门 + seq 状态记录**"，无需新引擎。新样本零新增。
【C】C-6（见附录 C，v1.2）: **织界线修正——本仓认知过载真实，缓解形态 = markdown-native 只读看板生成器 + git worktree/log graph，仍懒加载**：per-feature 事件流独立 ≠ 单写者单流（每 feature 一条 + fork 派生 = **多流并存**），叠加 AI 长输出 + 频繁外部反馈 → 认知过载/漂移真实。最小治愈 = 一个 stdlib 只读 Board 生成器：扫描 PROGRESS.md（Task Ledger）+ spec/*/ 四文档 + sessions/ 事件流 verdict（Progress Ledger）→ 压缩每 feature 为**单行认知块**（pid+状态+下一步+阻塞），按 3 状态分组（进行中/待你审/阻塞），暴露"需要你/下一步"= 外部信息注入 + 主动微介入入口；fork 派生用 **git worktree + `git log --graph`** 原生表达（零新增）。**零 GUI 服务器、零新依赖、AI 可写 markdown**。按 ADR-0010 仍**止于调研（懒加载 gate）**：零代码改动，仅登记概念，触发条件 = 用户明确要求落地 board 生成器（见 §10.6/H5）。
【C】C-7（见附录 C，v1.3）: **看板可自动（事件/hook/轮询三路径），完全脱依赖用户指令**：① **自动抓取** = 事件驱动——源头文件（PROGRESS / `.jsonl` 事件流 / spec 四文档）一改即触发重新生成，无需手敲命令；② **自动状态更新** = 门禁钩子——并进本仓既有 pre-commit 四 hook / step-gate / repo_stats 机械对账，**提交即刷板**（"声明=重数"外推到看板自身，防 drift）；③ **实时反馈** = 终端轮询渲染（纯 stdlib `watch -n`+终帧重绘即可，无需 rich/tqdm/Textual 重依赖）或常驻 FileSystemWatcher。**三档自动强度**：L0 门禁触发（最弱，提交时刷）/ L1 文件监听（源头改动即刷，`watch-inbox.ps1` FileSystemWatcher 现成）/ L2 终端轮询（常驻实时刷新，agent_pulse 500ms 模式）。仍懒加载 gate，触发=用户要求落地。

## 7. 补充调研一：UI 实时反馈与认知防过载（Q1，v1.1）

### 7.1 AgentGUI：观察 + 转向长时 agent（A-15）

【A】A-15: **AgentGUI**（ETH Zürich，[arXiv:2607.26300](https://arxiv.org/abs/2607.26300)，本地开源 GUI）：统一展示多个并发长时 agent 的轨迹可视化，支持手动+自动**转向（steering）**、与开源/前沿框架集成。受控用户研究=从混乱 trace 定位关键要素**提速 38%（p=0.023）**；自动"漂移预防"特性使本地小模型任务完成率跨 0.8B–9B 阶梯**最多 +34pp**（每模型 N=50 次）。→ 命中"实时反馈 + 防漂移"双目标，且给出"agent 越弱、越需防漂移"的实证。

### 7.2 认知负荷的心理物理实证（A-16）

【A】A-16: 三条跨学科实证锚定"防认知过载"设计边界：① **Cowan ~4±1 chunk**——工作记忆真实容量（Miller 7±2 高估）；② Sophie Leroy **attention residue**——任务间切换残留占用认知，切换性能下降 **40–60%** 直到 15–30 分钟才消退；③ Norman Mackworth **vigilance decrement**——被动持续监视 15–20 分钟内显著衰退，且**自动化监视比手操更严重**；Pop et al. 2012：叠加次级交互小任务可**抵消**该衰退（主动微介入保全注意力）。

### 7.3 微软 "AI brain fry"：并行监督的 POMDP 实证（A-17）

【A】A-17: 微软/UC Berkeley/清华《The Agentic AI Oversight Problem》把人类监督建模为 **POMDP**（agent 数 N、单 agent 错误率 ε、注意容量 C≈3–5 流），预测**监督失败概率在 N>C 时指数上升**并实测：监督准确率 1 agent **92%** → 5 agent **62%** → 20 agent **17%**，响应从 <10s 升到 >2min；NASA-TLX 主观负荷陡增。→ 启示：**长链（单流线性）不触发过载，多流并行才爆**——本仓单写者单流恰好避开。

### 7.4 Racc 认知设计原则：状态压缩 + 嗅探线索 + 主动微介入（A-18）

【A】A-18: **Racc**（多 agent IDE）把上述研究合成可落地原则：每会话压缩为**单个认知块**（状态色+任务+进度+耗时）；按 3 类状态（正常/待审/阻塞）**分组削减 chunk 数**；用**信息嗅探线索**（错误计数 / stuck 徽章 / 距上次进展时长 / 微摘要）引导"信息觅食"；agent 周期性请求**轻量人工输入**维持主动监督。→ 设计体检：始终护住"工作记忆 ≤4 chunk + 主动微介入 + 线索"。

### 7.5 既有 LLM observability 平台（A-19）

【A】A-19: LangSmith / Langfuse / Arize Phoenix / MLflow 均以 **span trace 树 + agent 图可视化 + 逐轮 replay + 版本化评测**为基座（OpenTelemetry/OpenInference 统一 ingest）；核心洞察="**trace 是新的 log**"——单 LLM call 不是 agent，失败在 call **之间**（工具选择/重试/子 agent/未退出的环）。→ 这些是重型平台（SaaS 或 ClickHouse self-host），与本仓"单写者 + 纯文档 + 零依赖"定位冲突，纳入 C-5 懒加载排除。

### 7.6 AutoGPT 三级事件粒度 + DAG 布局（A-20）

【A】A-20: AutoGPT 实时进度可视化落点=**事件驱动 + 三级粒度**：L1 用户级（主干任务）/ L2 开发级（工具调用+状态变更）/ L3 调试级（LLM 输入输出），按角色切层**防信息过载**；用 **Dagre 有向无环图布局**排依赖，颜色编码（绿完成/蓝进行/红失败重试/灰跳过）。→ **粒度分层 = 多流混合时的"救生筏"**；本仓单流场景只需 L1。

## 8. 补充调研二：AI 工作流审计·决策链追溯·幻觉抑制·微工作流嵌套（Q2，v1.1）

### 8.1 错误级联与连续监督：COCO（A-21）

【A】A-21: **COCO**（BUPT，[arXiv:2508.13815](https://arxiv.org/abs/2508.13815)）用多点连续监督阻断多 agent **错误级联**（下游放大上游幻觉——正是本仓 A-3 LGMM 断点的泛化）：**Contextual Rollback**（按执行历史回滚，非盲目重试）、**Bidirectional Reflection Protocol**（防振荡控制环）、**Heterogeneous Cross-Validation**（用**集成分歧**识别偏差/幻觉——与本仓 RULE-5 异基座同构）；30× 参数削减仍达大模型性能 **95.1%**，平均提升 6.5%。

### 8.2 执行 + 守卫双角色防幻觉：AWorld（A-22）

【A】A-22: **AWorld**（[arXiv:2508.09889](https://arxiv.org/abs/2508.09889)，GAIA 开源第一）：Execution Agent 由 **Guard Agent** 运行时"动态驾驶"监管，用 **System Identification** 离线建档执行者固有弱点（性能指纹）→ Guard **profile-aware** 定向纠错；严格防幻觉护栏 = **明令禁止编造数据、关键信息缺失必须输出"cannot solve"终止**（拒答优于臆造）。→ 对应本仓 M7 断言分级 + 拒绝表演性自信。

### 8.3 形式化护栏：AgentGuardian 控制流图 + ACM 形式证明（A-23）

【A】A-23: 两条形式化硬护栏：① **AgentGuardian**（BGU，[arXiv:2601.10440](https://arxiv.org/abs/2601.10440)）从执行日志**学习控制流图 CFG**（合法工具的合法序列）+ 输入正则约束，运行时访问控制，实测**缓解幻觉驱动错误与编排级故障**；② ACM《Guardians of the Agents》（Erik Meijer，2025）：要求 agent 在授权执行前**生成安全性的形式证明**，把安全不变量表达为 **security automaton**（约束执行全程成立）——evals 只能证有不能证无，形式证明给出确定性保证。→ 与本仓"证据链 + 门禁先于放行"同旨。

### 8.4 决策链追溯标准：W3C PROV（A-24）

【A】A-24: **W3C PROV 家族**（PROV-DM/O/N/XML + **PROV-CONSTRAINTS**）是"决策/数据链可追溯"的互操作标准：Entity/Activity/Agent 三要素 + wasGeneratedBy/usedBy/wasAttributedTo/derivedFrom 关系；**PROV-CONSTRAINTS** 形式化**时序与因果约束**（编辑不能先于文档存在、因果不能反向），防止溯源记录自相矛盾。→ 本仓事件流（append-only）+ seq 即 PROV 的纯文档层实例。

### 8.5 可审计 AI 谱系：trace 质量决定归因（A-25）

【A】A-25: awesome-auditable-ai（201 条目）实证**可审计性取决于记录质量**：**TraceElephant**（ACL'26）显示完整执行 trace 把 step 级归因准确率 **17%→30%**（相对 +76%）；Who&When（ICML'25）最强归因法定位责任 agent **53.5%**、决定性错误步 **14.2%**；AgentAuditor（NeurIPS'25）、SpecBench（reward hacking 测量）量化"能力增长快于可靠性增长"。→ 直接支持本仓"每步恰一条决策 + 证据锚点 + status seq"的价值。

### 8.6 幻觉抑制的生成侧：grounding + 自验证引用（A-26）

【A】A-26: 幻觉抑制分三层：① **检索-grounding**（RAG 用 DPR/ColBERT 检索证据锚定生成；本仓 research-lookup 即此）；② **自验证-引用**（**VeriFact-CoT** [arXiv:2509.05741]：事实核验→反思→引用整合多级；多模态事实核验框架 [arXiv:2510.22751] 跨结构化库+网络+学术文献交叉核对，幻觉 **-67%**、领域专家 89% 满意）；③ **训练无关检测器集成**（token 熵 + 自一致性 + 证据覆盖 + 零样本 NLI 蕴含/矛盾）。→ 文本框引用锚定 = 本仓 M7 锚点的学术写作等价物。

### 8.7 每步内嵌微工作流 = 层级状态机/子网（A-27）

【A】A-27: 社区把"每步含微工作流"建为**层级形式结构**：① **HAACS**（[arXiv:2505.00018](https://arxiv.org/abs/2505.00018)）用**层级 Petri 网**形式化 agent 协作——MIMO 转移、子网并发执行、冲突消解，step=可再分的子网；② **NVIDIA Deep Researcher / artificial-agent-lab**：owner/orchestrator → planner/researcher/PI → PhD 逐层委派，每层一个 loop；③ **LangGraph StateGraph**：节点+边+state reducer+checkpointer+human-in-the-loop interrupt——**状态机作为图引擎硬骨架**。→ 与本仓 P-039 P-b 裁定呼应：层级用于探讨口，本仓 flat-feature 结构不引入内层 agent 递归（复利误差）。

## 9. 补充调研三：链条连锁反应硬规则（图/状态机）（Q3，v1.1）

### 9.1 诉求与本质

用户要求把"写作链条的连锁式影响"固化为**硬规则**（图结构/状态机/类 模式）而非口头纪律——每一步改动引发的上游/下游连锁修改必须**被机器强制、可追溯**（A-1 的"连锁式影响 + 频繁审查修改"）。

### 9.2 本仓已是状态机（B6 引）

【B】B6（见附录 B）: 本仓 spec 流程**本质上就是一个确定性状态机**：STEP_SEQUENCE=状态集，step-gate（schema 硬性-1 / evidence 非空 / 同符号核对）=状态转移守卫，事件流 seq=状态历史（append-only）。"连锁反应硬规则"落点=**每步产物标注"被下游消费的对象"**（B3 的跨层绑定）+ 转移合法性由 gate 机械裁决。→ 与 AgentGuardian CFG / ACM security automaton / PROV-CONSTRAINTS 同一手法，**无需新引擎**。

### 9.3 硬规则形态选型：状态机 vs 全量 DAG 依赖图

社区形态折中：**状态机（合法转移集）**比 **全量 DAG 依赖图**更贴合"门禁编排"——状态机声明哪些转移合法、谁必须被 gate；DAG 声明全部祖先。前者贪心、可叠加、逐点裁决，与本仓 gate 逐步骤机制一致；后者需显式依赖发现成本（→ H4）。

### 9.4 与既有裁定收敛

上述映射已并入 §5 C-4/C-5；三条红线（机械物证门先于语义门、seq 单调记录、跨层同符号绑定）与 P-039 P-c 的三条红线同族。

## 10. 补充调研四：任务看板与自动化追踪——本仓认知过载的真实落点（v1.2）

### 10.1 前提修正：per-feature 多流并存 = 真实过载（B8 引）

【B】B8（见附录 B）: 先前 C-4/C-5 以"doc-first + 每 feature 事件流独立 = 单写者单流，天然免征 attention residue/vigilance decrement"为据排除一切 UI 层——该前提被用户场景证伪：**per-feature 事件流独立恰恰意味着多流并存**（每 feature 一条独立流 + fork 派生支线），叠加 AI 输出冗长需逐条反馈 + 频繁外部信息注入 → 本仓认知过载/漂移**真实存在**（A-16/A-17 的过载机理直接适用）。故正确姿态不是"免征"也不是"引入重型 GUI 平台"，而是**在既有事件流之上加一层轻量聚合视图**（§10.5）。

### 10.2 Task Ledger / Progress Ledger 二账本：想做的事 vs 实际进度（A-28）

【A】A-28: **Magentic-One**（Microsoft，[arXiv:2411.04468](https://arxiv.org/abs/2411.04468)）确立二账本模式：**Task Ledger**（given facts / facts to look up / educated guesses / step-by-step plan = 想做的事）vs **Progress Ledger**（per-tick **五问判题**：is_request_satisfied / is_in_loop / is_progress_being_made / who_to_speak_to / what_to_say = 实际进度），**"账本即人工审查面"**；stall counter 把"继续或重规划"从判断转成**确定性门**（≤2 即 re-plan）。→ 本仓天然对应：**Task Ledger≈PROGRESS.md（待办/路线）+ spec 四文档（计划）**；**Progress Ledger≈事件流**（event:decision + step-gate verdict exit 0/1/2 = per-step 判题）——**二账本分离已在隐式存在，缺的是显式聚合读取**。

### 10.3 Markdown-native 任务看板：AI 可写 + 零后端（A-29 / A-30）

【A】A-29: **Backlog.md**（npm，AI-ready）：每个任务=仓库里一个普通 `.md` 任务文件（frontmatter+验收标准+DoD+milestone/deps），`backlog board` 终端看板 + `backlog board export` markdown 报告 + `backlog browser` 本地 web；**三审查检查点 = 审 spec → 审 plan → 审 code**，一任务 = 一上下文窗口 = 一 PR；核心动机="瓶颈不再是写代码，是你的注意力——AI 一小时产出比人类一天能读的还多，但你可以先读一屏任务规格+验收标准再让代码写一行"。→ 与本仓 **doc-first + one-feature-one-context** 高度同构，且全部输出 markdown（AI 与人两可读）。
【A】A-30: **Markdown Task Board**（ad-halfspace）：纯 **Python 标准库** web server（仅绑 127.0.0.1）+ 单 HTML，list/kanban 双视图、按状态/优先级/领域分组、**依赖自动阻塞**；**Kanban.md**（VSCode 扩展）把 `.kanban.md` 渲染成可交互板；**Nullboard** = 单个 HTML 文件零配置。→ 印证"**看板可零第三方依赖 + markdown 作单一事实源**"，与本仓 stdlib 约束兼容。

### 10.4 fork 支线探索：git worktree + log graph（A-31）

【A】A-31: **git worktree**（Git≥2.5）= 一仓多工作目录、共享历史、按分支隔离——是"主线开发中 fork 支线探索"的**原生载体**（OpenAI Codex 每线程自动建 worktree；spaarke 并行 Claude 会话 3-5 个 worktree + 顺序 merge 防冲突；冲突检测可早提示）；`git log --oneline --graph --decorate --all` **原生可视化分支 DAG**（`*` 提交 / `|/` 合并线）。→ 本仓"主线 + fork 支线"= **git branch/worktree + 事件流 fork/replay**，零新增工具，板只需标注分支派生与"diverge/merge 回主线"状态。

### 10.5 最小落地方案：只读看板生成器 + git 可视化（B8 落点）

综合 A-28~A-31，本仓"自动化追踪 / 任务看板"的最小形态 = **一个 stdlib 只读 Board 生成器**（可作 spec_runner `board` 子命令或独立脚本）：

- **输入**（全部既有，零新状态）：
  - `docs/PROGRESS.md`（Task Ledger：P-id + 状态词表 pending/in-progress/blocked/done + 验收标准）
  - `spec/*/` 四文档（feature 计划呈现）
  - `tools/spec_runner/sessions/*.jsonl` 事件流（Progress Ledger：event:decision + step-gate verdict exit 0/1/2）
  - `git log --graph`（fork/分支派生）
- **输出**：终端看板 + `docs/BOARD.md`（可提交、AI/人两可读）。每 **feature = 单行认知块**：`pid | 状态(色) | 当前 step/Next | 阻塞标记 | fork 派生标记`；按 **3 状态分组**（▶进行中 / ⚠待你审 / ✖阻塞）；顶部独立 "**需要你 / NEXT**" 队列 = 外部信息注入 + step-gate exit 2(soft)/blocked 的汇聚点（主动微介入入口）。
- **满足 Racc 认知设计四原则**（A-18）：单认知块（一行一 feature）、状态分组（3 桶）、嗅探线索（阻塞徽章/距离上次进展/色）、主动微介入（NEXT 队列）；对应用户三大痛点：长输出→压缩为一行；外部注入+反馈→NEXT 队列；fork 支线→git graph 标注。
- **零新增依赖**：纯 stdlib 读文件 + 重新排列 + 写 markdown/stdout；**无 GUI 服务器、无 watch 常驻进程**（按需生成；H5 挂自动 watch 之需未实测）。

### 10.6 收敛与触发条件（C-6 引）

- 结论 = C-6（§5）：改编织界线，给出方向，**仍止于调研（懒加载 gate）**——零代码改动，仅登记概念设计与社区案例。
- **触发条件（Q2）**：用户明确要求落地 board 生成器（或指定首用例），此时按 ADR-0010 走实施小流程。
- 与 P-039 P-c 的关联：看板 = 主控站"任务卡 + 状态聚合"的本地单机版（无集群）；与 PROGRESS/CODE_WIKI 视图层一致性由 repo_stats 机械对账（声明=重数外推）天然兜底。

## 11. 补充分析：看板能否不依赖用户指令自动实时更新（v1.3）

### 11.1 结论先行（B9 引）

【B】B9（见附录 B）: **能**。看板的"自动抓取 / 自动状态更新 / 实时反馈"是标准的一类**派生产物自动重生成**问题，社区已有三条成熟且与零依赖兼容的触发路径，本仓无需任何第三方依赖即可全部具备。看板 = "只读视图"，其唯一职责是从既有真值源（PROGRESS/事件流/spec 四文档/git）**被动重算**——因此**不存在"需用户主动唤醒"的固有理由**，只需选一个自动触发时机（B9/C-7：L0/L1/L2）。

### 11.2 路径一：事件驱动自动抓取（A-32）

【A】A-32: 文件变化→自动处理 = **FileSystemWatcher** 的标准用途（.NET 内置，Windows 本机零新依赖，NotifyFilter=FileName/LastWrite/DirectoryName，IncludeSubdirectories，事件 Created/Changed/Deleted/Renamed 触发 Action）；`watch-inbox.ps1` 完整实作"文件落盘→自动归纳→写每日笔记"模式。→ 本仓 = watch `docs/PROGRESS.md` + `spec/*/` + `tools/spec_runner/sessions/*.jsonl` 任何 one 变化即重跑板生成器，**源头改动即自动刷新**，无需任何用户指令。

### 11.3 路径二：门禁钩子自动重生成（A-33）

【A】A-33: **do-knowledge-studio** `update-docs.mjs`：静态分析 + 模板驱动 API-GIT 钩子/CI 自动更新文档"生成节"（`<!-- AUTO-START -->`/`<!-- AUTO-END -->` 栅栏，只改写生成区，保留人工内容；pre-commit + GitHub Actions），**零外部 LLM、确定性、~1-2s**；**ProjectOdyssey** 把 test-count badge 做成 pre-commit 自动计数防 drift。→ 本仓已有 pre-commit 四 hook + repo_stats 机械对账 + step-gate，**把板生成器并进同一 pre-commit/step-gate 即"提交即刷板"**，且 repo_stats 对账天然保证"看板声明 = 真值"（声明=重数外推）。

### 11.4 路径三：终端实时轮询渲染（A-34）

【A】A-34: **agent_pulse / cc-aio-mon**（Claude Code 终端监视器）：轮询 temp 目录 snapshots（约 500ms 刷新）→ 全屏 TUI progress bar/指标渲染，**非阻塞、不依赖用户指令**；**Rich Live** 自带 `refresh_per_second` 定时自动刷新 + 可 `screen=True` 切换备屏；**minimal-tui** 强调"rich+tqdm 主、stdlib 兜底"。→ 本仓最小形态 = 纯 stdlib：`watch -n 5 board_cmd`（每隔 5s 重渲染终帧）+ 可选的 Wi-Fi 行内状态条，**无需引入 rich/tqdm/Textual 重依赖**（与零依赖 D6 一致）。

### 11.5 三档自动强度与裁定（C-7 落地）

| 档 | 触发 | 实时性 | 依赖 | 本仓现状 |
|----|------|--------|------|---------|
| L0 | pre-commit/step-gate 门禁 | 提交时刻 | 零（既有 hook）| ✅ 已有四 hook + repo_stats |
| L1 | FileSystemWatcher 监听源头 | 次秒-秒级 | 零（.NET 内置）| 可选 |
| L2 | 终端轮询 `watch -n` 渲染 | 秒级常驻 | 零（stdlib）| 可选 |

- **L0 已零成本可办**（并进既有 hook）；**L1/L2 为增量可选档**，开销 H5 未实测（但均为 stdlib + 轻轮询，成本低）。
- 综合 = **C-7**（§5）：看板可由事件/hook 自动更新 + 可选终端轮询展示，**完全脱依赖用户指令**；仍懒加载 gate，触发=用户要求落地 board 生成器。
- **归属转移（2026-09-11，P-042 剥离）**: C-7 触发的落地物已由 [project-console](../project-console/RESEARCH.md) 承接——可视化层归**通用底座**独立 feature，P-041 [board-generator](../board-generator/DESIGN.md) 记为其**前身（L0 首落点）**；本节自此降格为**来源指针**（只记录 C-6/C-7 概念来源），不再拥有看板能力的归属。

## 12. 参考文献

- LGMM 证据链审计（用户仓库）：[外部·2026-09-10-empirical-estimator-evidence-chain.md](file:///D:/Article/Working%20paper/LGMM/LGMM%208.0/docs/audit/2026-09-10-empirical-estimator-evidence-chain.md)
- SciTeX Writer（模块化版本控制手稿 + latexdiff + revision 轮次）：https://github.com/scitex-ai/scitex-writer
- paper-template（GitHub Actions 自动编译 PDF）：https://github.com/specialpointcentral/paper-template
- Quarto（literate programming）：https://quarto.org ；knitr：https://yihui.org/knitr/
- reproducible analysis five pillars（literate 即五柱之一）：https://github.com/depaul-uni/depaul-open-science/blob/main/chapters/04-reproducible-analysis.md
- ARIS 跨模型审稿（adversarial bandit / REVIEW_STATE / AUTO_REVIEW）：https://github.com/LeoLin990405/Auto-claude-code-research-in-sleep
- PaperJury（对抗式法庭审稿 + durable ledger）：https://github.com/u7079256/paperjury
- Agentic_Paper（12 并行 reviewer agent）：https://github.com/albertogerli/Agentic_Paper
- Multimodal Peer Review Simulation（Action:Objective to-do，WWW'26）：https://arxiv.org/html/2511.10902v2
- auto-research（8 phases / 4 gates / LAB_NOTEBOOK.md）：https://github.com/0h-n0/auto-research
- eLabFTW（开源 ELN，审计防篡改）：https://github.com/elabftw/elabftw
- Open Science Framework（预注册）：https://osf.io
- Lie-algebra/Lean4 一致性 / lf-lean 类型同构验证：https://github.com/theorem-labs/lf-lean ；Lean Workbook：https://arxiv.org/html/2406.03847v3
- Zotero+LaTeX+Git 文献版本锚定：https://wenku.csdn.net/column/1dwf16jqotan
- Auto Review Loop（review-2-fix 循环 + MARK_ROUNDS）：https://lobehub.com/skills/comeonoliver-skillshub-auto-review-loop-llm
- AgentGUI（观察 + 转向长时 agent，38% 提速 / 防漂移 +34pp）：https://github.com/eth-medical-ai-lab/agent-gui ；arXiv：https://arxiv.org/abs/2607.26300
- Msft/Berkeley/清华《The Agentic AI Oversight Problem》（AI brain fry / POMDP 监督容量 C≈3-5）：https://forum.gnoppix.org/t/study-warns-of-ai-brain-fry-as-workers-hit-cognitive-limits-overseeing-ai-agents/4876
- Racc（多 agent IDE 认知设计研究，Cowan 4±1 / attention residue / info foraging / 主动微介入）：https://github.com/liu1700/racc/wiki/Cognitive-Design-Research
- Top LLM observability tools 2026（LangSmith / Langfuse / Arize Phoenix / MLflow，trace 是新的 log）：https://mlflow.org/articles/top-llm-observability-tools-in-2026-a-pro-guide/
- AutoGPT 实时进度可视化（三级事件粒度 + Dagre DAG 布局 + 颜色编码）：https://blog.csdn.net/weixin_35829279/article/details/155927006
- COCO（连续监督 / heterogeneous cross-validation / 30× 参数削减 95.1%）：https://arxiv.org/abs/2508.13815
- AWorld（Execution+Guard 双角色，System Identification 建档，防幻觉护栏）：https://arxiv.org/abs/2508.09889
- AgentGuardian（从日志学习 CFG 控制流图 + 输入约束，缓解幻觉驱动错误）：https://arxiv.org/abs/2601.10440
- ACM Guardians of the Agents（Erik Meijer，security automaton + 执行前形式证明）：https://cacm.acm.org/practice/guardians-of-the-agents/
- W3C PROV 家族（Entity/Activity/Agent + PROV-CONSTRAINTS 时序因果约束）：https://www.w3.org/TR/prov-overview/ ；PROV-O：https://www.w3.org/TR/prov-o/
- awesome-auditable-ai（201 条目；TraceElephant 17%→30% / Who&When / AgentAuditor）：https://github.com/yzhao062/awesome-auditable-ai/
- VeriFact-CoT（事实核验-反思-引用整合）：https://arxiv.org/abs/2509.05741 ；多模态事实核验（网络+文献交叉核对，-67% 幻觉）：https://arxiv.org/abs/2510.22751
- HAACS（层级 Petri 网形式化多 agent 协作，step=可再分子网）：https://arxiv.org/abs/2505.00018
- NVIDIA Deep Researcher（orchestrator-planner-researcher 层级 loop）与 artificial-agent-lab（PI+PhD investigators + knowledge_graph.jsonl）
- Magentic-One Task Ledger / Progress Ledger（Microsoft，二账本 + 五问判题 + stall counter）：https://arxiv.org/abs/2411.04468 ；模式解读：https://www.agentpatterns.ai/multi-agent/magentic-orchestration/
- Backlog.md（markdown 原生任务看板 + 终端 kanban + 三审查检查点，AI-ready）：https://www.npmjs.com/package/backlog.md ；https://github.com/MrLesk/Backlog.md
- Markdown Task Board（ad-halfspace，纯 Python stdlib + 单 HTML，依赖自动阻塞）：https://github.com/ad-halfspace/markdown-task-board
- Kanban.md（VSCode 扩展，`.kanban.md` 交互板）：https://marketplace.visualstudio.com/items?itemName=wguilherme.kanban-md ；Nullboard（单 HTML 零配置）：https://gitcode.com/GitHub_Trending/nu/nullboard
- git worktree 并行 agent 开发 + `git log --graph` fork 可视化：https://araisun.com/git-worktree-parallel-ai-codex/ ；https://github.com/spaarke-dev/spaarke/blob/master/docs/procedures/parallel-claude-sessions.md
- PowerShell FileSystemWatcher（.NET 内置，事件驱动自动抓取，零新依赖）：https://gist.github.com/mobzystems/d81b46733c1868ed916e0859d4929e2b ；https://gist.github.com/16892434/8677af78f247bfd5d3208df7ad838912 （watch-inbox.ps1）
- do-knowledge-studio 自动更新文档（`update-docs.mjs` + AUTO-START/AUTO-END 栅栏 + pre-commit/CI）：https://github.com/d-oit/do-knowledge-studio/issues/34
- ProjectOdyssey 自动计数 badge 防 drift（pre-commit）：https://github.com/HomericIntelligence/ProjectOdyssey/issues/3307
- agent_pulse（GitHub Copilot CLI 实时终端看板）：https://github.com/DUBSOpenHub/copilot-cli-agent-pulse ；cc-aio-mon（Claude Code 终端监视器，500ms 轮询）：https://github.com/iM3SK/cc-aio-mon
- Rich Live（`refresh_per_second` 自动刷新 + screen）：https://rich.readthedocs.io/en/latest/live.html ；minimal-tui（rich+tqdm stdlib 兜底）：https://www.skillmd.ai/skills/minimal-tui/

## 附录 A：A 类断言明细

- A-1 至 A-3：见 §2 各 `【A】` 行（用户场景）。A-4 至 A-12：见 §3 各 `【A】` 行（社区案例）。A-13/A-14：见 §4.5/§4.6。A-15 至 A-20：见 §7 各 `【A】` 行（v1.1 UI/认知防过载）。A-21 至 A-27：见 §8 各 `【A】` 行（v1.1 审计·决策链·幻觉抑制·微工作流）。A-28 至 A-31：见 §10 各 `【A】`/`【B】` 行（v1.2 任务看板·自动化追踪）。A-32 至 A-34：见 §11 各 `【A】` 行（v1.3 自动刷新三路径）。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "用户九步学术推理写作链的本质是非线性依赖图而非线性管道——上游改动向右游传播、下游发现反噬上游（连锁式影响）；本仓 SPEC_PROCESS 十步 + step-gate 的 STEP_SEQUENCE 是线性骨架，但事件流 append-only + seq 单调天然支持 fork/replay，社区（auto-research 8 phases / PaperJury 多轮）也把链当可循环过程。同构成立点为『分步 + 门禁 + 可回溯』，故无新增机制要求", "basis": "A-1/A-10/A-7 + SPEC_RUNNER_DESIGN"},
  {"id": "B2", "inference": "『每步改动自动产生下一步状态提醒』的社区实现本质是读取方消费 append-only 事件流按 seq 判定推进（auto-research 用 8 phases 显式 next gate、ARIS 用 REVIEW_STATE.json）；本仓 spec_runner 已落 append-only + seq + replay/fork，自动提醒 = 一个读取 seq 并打印『下一步该做 Gate N』的轻壳，机制零新增，最大同构点是不欠账", "basis": "A-1/A-10/A-6 + SPEC_RUNNER_DESIGN"},
  {"id": "B3", "inference": "『数学-算法-数据-结果-论文表达一致性』的本质是多对象证据绑定——让 λ̂ 在论文/设计/代码/结果四层绑定同一对象标识；社区三条路（literate 内联结果 / Lean4 形式化 / 符号核对表+数值探针）中本仓对应 = 声明=重数 + verify-anchor + M7 证据分级 E1（可重放命令）。LGMM 缺的是把这条绑定做成例行 guard（对应其 M-12/M-08）", "basis": "A-2/A-3/A-5/A-11 + SPEC_PROCESS R7"},
  {"id": "B4", "inference": "『模拟评审→反馈迭代』社区用跨模型/multi-arm（ARIS adversarial bandit、PaperJury 对抗式法庭、Agentic_Paper 12 reviewer），本仓用 RULE-5 异基座独立 pass，两者同旨：把作者自评替换为独立评审者；ARIS『两模型逼近 Nash 即最优』论据直接支持本仓 RULE-5 异基座第二会话的价值", "basis": "A-6/A-7/A-8 + SPEC_PROCESS RULE-5"},
  {"id": "B5", "inference": "『防认知过载/漂移/遗忘』不是新机制而是一组展示与介入设计原则——社区共识（Cowan 4±1 / attention residue / vigilance decrement / Msft POMDP）都指向『多流并行才过载、单流线性不触发』（v1.2 修正：本仓 per-feature 事件流独立 = 多流并存，过载真实，见 B8/C-6）；需要吸收的只是『状态压缩成单个认知块 + 主动微介入确认 + 嗅探线索』三条展示原则（对应 verify-anchor 结果色 + step-gate 确认提示），落地为 markdown 聚合看板，而非引入 AgentGUI/LangSmith 重型平台", "basis": "A-15/A-16/A-17/A-18/A-19/A-20 + B2/B8"},
  {"id": "B6", "inference": "链条式连锁反应的硬规则 = 本仓已是确定性状态机：STEP_SEQUENCE=状态集、step-gate（schema 硬性/evidence 非空/同符号核对）=状态转移守卫、事件流 seq=状态历史，与 AgentGuardian CFG、ACM security automaton、PROV-CONSTRAINTS 同一手法；『连锁』落点 = 每步产物标注被下游消费的对象（B3 跨层绑定）+ gate 机械裁决转移合法性，无需引入 DAG 引擎或新状态机库", "basis": "A-23/A-24/A-14 + SPEC_PROCESS R7/gate"},
  {"id": "B7", "inference": "AI 工作流的结果审计/决策链追溯/严格抑制幻觉，在本仓 = 证据锚点化 + 跨层机械校验：M7（断言分级 E1-E5，同 COCO 集成分歧/AWorld 双角色），RULE-5（异基座独立臂，同 heterogeneous cross-validation），decision 八字段（决策链，同 PROV wasGeneratedBy/derivedFrom），verify-anchor（锚点核查）；社区（TraceElephant 17%→30%）实证『可审计性取决于记录质量』，直接支持本仓『每步恰一条决策 + 物证锚点』——幻觉抑制不是模型层补丁而是记录与门禁纪律", "basis": "A-21/A-22/A-23/A-24/A-25/A-26 + M7/RULE-5"},
  {"id": "B8", "inference": "本仓认知过载真实存在（C-4/C-5『单写者单流天然免征』前提被证伪）：per-feature 事件流独立 = 多流并存（每 feature 一条 + fork 派生），叠加 AI 长输出 + 频繁外部反馈；正确缓解形态 = 在既有事件流之上加一层轻量聚合视图——stdlib 只读看板生成器，扫描 PROGRESS(Task Ledger)+spec 四文档+sessions 事件流 verdict(Progress Ledger，Magentic-One 二账本已隐式存在) → 压缩每 feature 为单行认知块，按 3 状态分组 + NEXT 队列（外部注入/主动微介入入口）；fork 派生用 git worktree + git log --graph 原生表达；『声明=重数』由 repo_stats 机械对账兜底；零 GUI 服务器/零新依赖/AI 可写 markdown", "basis": "A-16/A-17/A-18/A-28/A-29/A-30/A-31 + C-6"},
  {"id": "B9", "inference": "看板『自动抓取/自动状态更新/实时反馈』本质是派生产物自动重生成问题——看板=只读视图，职责=从真值源被动重算，故无『需用户主动唤醒』固有理由；社区三路径（FileSystemWatcher 事件驱动 / hook+CI 门禁自动重生成 / 终端轮询渲染）均零第三方依赖可达成；本仓 L0 档已零成本（并进既有 pre-commit 四 hook + step-gate + repo_stats 对账，提交即刷板），L1/L2 为增量可选档（stdlib + 轻轮询）——完全脱依赖用户指令", "basis": "A-32/A-33/A-34 + C-7"}
]
```

## 附录 C：C 类判断与假设区

- C-1/C-2/C-3：见 §5。C-4/C-5：见 §5（v1.1，新增三同构维度 + 仍止于调研的补充裁定）。C-6：见 §5 + §10（v1.2，织界线修正——本仓多流并存过载真实，缓解=markdown 只读看板生成器 + git worktree/log graph，仍懒加载 gate）。C-7：见 §5 + §11（v1.3，看板可自动刷新——事件/hook/轮询三路径，脱用户指令）。
- [H1] 九步链是否需要显式 **DAG 依赖映射**（vs 现状线性 + 事件流跳相）未裁决——当前 spec_runner 用 STEP_SEQUENCE 线性 + --expect，若学术写作链确现分支合并，需评估是否有补充依赖表达的必要。
- [H2] **数学-实现一致性**是否引入 Lean4 形式化的性价比未实测——A-11 示 Lean4 为终极工具但成本高，LGMM 已用数值探针替代，需在真正的定理级断言场景做成本收益实测。
- [H3] 本仓是否需要引入任何**可视化/UI 展示层**？未实测（v1.2/v1.3 部分回答）——事件流 seq + doc 单读单位可能已满足"状态/阶段/下一步提醒"；v1.2 指向 markdown 只读看板生成器（§10.5）为最小形态，v1.3 确认其可自动刷新（§11），但**是否真的值得落地**（维护开销 vs 单写者低并发收益）仍未实测。
- [H4] 链条式连锁反应的**上游依赖发现**是否需要显式依赖元数据（全量 DAG）？未实测——§9.3 社区状态机路线主张"逐点 gate 裁决"（贪心增量），全量 DAG 需依赖推理/反向传播成本，本仓 topic 以 review 人工发现反噬切入（B1），显式自动依赖发现的性价比未实测。
- [H5] 看板生成器的**生成时机**：按需生成（手动/CI 触发）vs 上游 watch 自动重生成（改 PROGRESS/事件流即刷新）？**v1.3 部分回答** = 三档自动强度（L0 门禁触发 / L1 FileSystemWatcher 监听 / L2 终端轮询 `watch -n`），三者均零新依赖可行，但各档**常驻开销与实用性未实测**；默认建议 L0（提交即刷）+ L1 可选。

## 附录 D：与既有候选池的关系

- 本调研同构于 P-039（同属"把当前框架应用到另一个工作流"）；不新增候选 UID（无外部框架本体吸收，仅概念登记 + 复用，符合 ADR-0010 懒加载）。
- v1.1 补充三个新维度均映射本仓既有机制（M7/RULE-5/decision/verify-anchor/step-gate/事件流 seq），**零新依赖**；未引入 AgentGUI/LangSmith/Langfuse/AgentGuardian 等重型平台或运行时本体——与 C-5 裁定一致。
- v1.2 补充（任务看板/自动化追踪）：**候选形态 = markdown 只读看板生成器（Layer-0/1 概念，stdlib，可作 spec_runner `board` 子命令或独立脚本）**，从 Backlog.md/Magentic-One 二账本取模式但**不吸收框架本体**；fork 支线用 git worktree/log graph 原生能力。未落地（C-6 懒加载 gate），触发条件=用户明确要求。
- v1.3 补充（自动刷新）：三条自动触发路径（FileSystemWatcher 事件 / hook+CI 门禁 / 终端轮询渲染）均为**零新依赖**方案；L0（并进既有 pre-commit 四 hook）已零成本，L1/L2 为增量可选档——**完全脱依赖用户指令**（C-7/B9）；仍未落地，懒加载 gate 保持。