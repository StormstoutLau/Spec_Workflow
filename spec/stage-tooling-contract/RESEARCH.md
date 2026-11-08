# 调研文档：分阶段工具与提示词契约

---

id: stage-tooling-contract-RESEARCH
type: design
version: 1.5
status: draft
date: 2026-10-21
depends: [SPEC-PROCESS, ADR-0010, FWK-ASSERTION]
upstream: null

---

> **Feature**: stage-tooling-contract（分阶段工具 / Skill / 提示词绑定——可行性、边界与代价）
> **创建日期**: 2026-10-21
> **修订**: v1.1（2026-10-21，P-115 · 裁决 5 = C 档：**U-2 全量核验**——19 条参考文献 + 3 条补充页逐条回原文；外部读数从「摘要级 E2/E3」升级为「T1 定位」；订正 **9 处**转述 / 归属 / 未取证缺陷〔含 1 处**方向倒置**〕；§4.2 按 T1 原文重写；U-2 **关闭**）→ v1.2（2026-10-21，P-116：U-3 关闭——§5.10 八条移出至 [ACADEMIC_REASONING_CONSTRAINTS.md](../academic-writing-workflow/ACADEMIC_REASONING_CONSTRAINTS.md) v1.0，本节只留指针；行数保持以稳定 P-115 会话锚点）→ v1.3（2026-11-06，P-161：**分阶段外部锚点与多方案裁决取证复核**——新增 §6.5：① 现状确认「外部信息源仅在 Step 1 有硬约束、Step 3 以回退方式间接要求、其余阶段无要求」（A-16 / A-20）；② 确认七维决策矩阵**已存在**（P-058）但有三个缺口——仅 Type-1 触发、无门禁、七维无操作化定义（A-17~A-19）；③ 提出 C-6~C-9 四条 Layer-0 建议（三档触发 / 触发式回退 / 两档矩阵 / 七维操作化）；A **15 → 20**、B **6 → 8**、C **5 → 9**；H 不变；零代码）→ v1.4（2026-11-07，P-162：**补充调研外部可借鉴的阶段映射实践**——新增 §6.6：回原文核验 **3 个社区反馈良好的开源项目**（GitHub Spec Kit / OpenSpec / BMAD-METHOD）的阶段模型、产物形态与门位点；判断 = 阶段映射的正确补强对象是「产物契约 + 门位点」而非阶段数量（B9）；建议 C-10~C-12（阶段产物契约表 / before-after 两型门 / 档位 × 必需阶段矩阵）；A **20 → 23**、B **8 → 9**、C **9 → 12**；零代码、不引入任何依赖）→ v1.5（2026-11-08，P-163：**契约取证字段形态化 + 前瞻预注册**——新增 §6.7：① **6 个真实批次只读核对**（P-115 / P-137 / P-151 / P-154 / P-161 / P-162）⇒ S10 机械读数 6/6，S1 / S2 / S7 / S9 形态面 0~50%；② 判断 = 唯一 100% 的行是唯一有机械门禁的行，其余靠自述；③ **C-13 五字段**（F1 日期 / F2 版本 / F3 降级链 / F4 验证表 / F5 先失败记录）已落地于 SPEC_PROCESS **v1.7.1 → v1.7.2** 文末节点；④ 前瞻预注册（观测对象 / 成功线 / 窗口 / 失败处置）；C **12 → 13**，A 23 / B 9 / H 4 不变；零代码、零门禁、零新依赖）
> **状态**: draft（草稿；v1.0 只出调研与建议、不改 SPEC_PROCESS 正文；**v1.5 起 C-13 五字段已落地于 SPEC_PROCESS v1.7.2 文末节点**，本节只留研究记录与预注册）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「落档 然后分析当前工作流的每个阶段是否可以精细化 指定特定 MCP skill 工具 或者提示词——例如调研阶段要求寻找学术源、开源社区等高质量信息；执行阶段要求 TDD 实现；设计阶段可能需要约束 taste；同时针对学术推理任务可能需要额外的提示词约束」→ 追加（2026-11-06）「分析当前工作流是否只在调研阶段显式要求搜索外部信息源 / 审计 设计 实施等阶段是否也应要求外部信息锚点 / 多方案裁决是否要求成本 收益 兼容 维护 升级 短期 长期多维度信息」→ 追加（2026-11-08）「调研文档：分阶段工具与提示词契约 是否可以进入吃狗粮执行」→「先补契约文本再开前瞻样本」

---

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|---|---|---|
| A 事实类 | 23 | 本仓 / 本机 / 外部 **T1 原文**的机械取证（E1，见附录 A） |
| B 推断类 | 9 | 由 A 类推出的判定（见附录 B） |
| C 类（决策） | 13 | 不参与 R7 机械对账（DR-2；C-6~C-9 为 P-161、C-10~C-12 为 P-162、C-13 为 P-163 五字段形态化 + 预注册） |
| 假设区 | 4 | 未实测项（见附录 C） |

> **取证口径（v1.1 起）**：本仓事实 = E1（逐字读文件 / 机械枚举）；外部结论 = **T1 原文定位**（arXiv 摘要 / HTML 章节 / 官方文档段落），逐条登记于 §7.1。T2 官方页（Anthropic 工程博客 / Spec Kit 站 / Contra / Glif）只作背景佐证，不与 T1 混级。**未定位到原文的数字不入 A 类**；v1.0 的 E3 二手数字已删除，不再作为论据。

---

## 1. 调研目标

**核心问题**：

1. **现状**：SPEC_PROCESS 的 10 步中，哪些步已有工具 / 提示词契约？哪些是「隐含在实践里但没写」？缺口有多大？
2. **外部证据**：给 agent 绑 skill、绑工具、绑提示词，**哪些真有增益、边界在哪**？（不是「能不能绑」，而是「绑了会不会反而更差」）
3. **逐阶段建议**：每步的最小工具集 / 可选 skill / 可机械核验的提示词硬约束该是什么？四类重点（学术源 / TDD / taste / 学术推理）分别怎么落？
4. **落地层与代价**：这些建议应落 Layer-0（文档纪律）还是 Layer-1（门禁）？代价、副作用与回退点是什么？

**边界声明（本轮不做的事）**：

- **不改** [SPEC_PROCESS.md](../../SPEC_PROCESS.md) 正文、**不新增** hook / 校验器 / 脚本、**不新增** 真值源；
- **不引入** 外部依赖，**不把 skill 安装状态写成本仓契约**（skill 属 agent 侧环境态，非仓内制品）；
- 本仓是**纯文档方法论仓**，与「写代码的仓」的绑法**不同**——Step 9 的 TDD 在本仓的等价物是「fixture 先于实现」（§5.8）。

---

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 / 操作 | 结果 |
|------|------|------------|------|
| Read / Grep | 本仓现状取证：十步定义、Review 规则、既有隐式绑定 | `SPEC_PROCESS.md` §10 步 / `dc_validator.py` M4-M6 / `AGENTS.md` | 成功（E1） |
| 文件系统枚举 | 本机实接面盘点 | `~/.trae-cn/mcps/**/SERVER_METADATA.json`、`~/.trae-cn/skills/` | 成功（E1） |
| `mcp_scholar-mirror_list_sources` | 学术镜像源清单 | 无参 | **成功**（返回 9 个 Google Scholar 镜像 + Semantic Scholar API） |
| `mcp_paper-search_search_papers` | 学术论文联合检索 | `test driven development large language model code generation`，源 = arxiv/semantic/openalex | **部分成功**（arxiv 4 条，semantic/openalex 0 条） |
| `mcp_english-search_search_web` / `search_academic` | 英文高质量检索 | 4 组查询 | **两次均 404**（服务端不可用，见 §6.3 风险 R2） |
| WebSearch（内置） | 外部证据线索发现 | 4 组共 14 条查询（SDD / TDD / 引用幻觉 / 工具过载 / skill 基准 / taste 评测） | 成功（线索级） |
| `WebFetch`（v1.1 新增） | **逐条回原文核验** | 19 条参考文献 + 3 条补充页 | 成功（T1/T2 定位，见 §7.1；**19/19 已核**） |

> **工具面实证的元观察**：同一「学术检索」意图，本机有 **5 个外部 MCP server** 可承接，但本次 **english-search 全部 404**、paper-search 仅 arxiv 源有结果 ⇒ **「有工具」不等于「工具可用」**。任何把工具写进流程的做法都必须配**降级链**（§5.2），否则提示词会指向一个不存在的通道。

### 2.2 调研范围

- **本仓**：`SPEC_PROCESS.md` 十步 + 五道 Review 门 + `AGENTS.md` 禁止事项 + 既有工具链（`dc_validator` / `m7_stats` / `repo_stats` / `console_gen` / `spec_runner`）。
- **本机 agent 环境**：MCP server 5 个（english-search / paper-search / research-tools / scholar-mirror / stackexchange）+ 集成能力 5 项（code_mode / browser / computer-use / goal / default）；本地 skill **213** 个 + 内置 skill **2** 个。
- **外部文献**：2023-2026 的 skill 基准、TDD-for-LLM、引用幻觉审计、tool overload、设计品味评测。
- **排除**：具体 skill 的安装/卸载、第三方模型选型、跨仓（`D:\Article` / `D:\RPC`）执行面。

---

## 3. 现状取证（本仓 + 本机）

### 3.1 SPEC_PROCESS 十步的工具契约现状

| Step | 现有工具条款 | 现有提示词 / 判据条款 | 缺口 |
|---|---|---|---|
| 1 调研 | **有**：「多种 MCP 工具」列举 4 类 + WebSearch/WebFetch + SearchCodebase | 无来源分级、无「≥N 独立来源」、无降级链 | 只有**枚举**，没有**质量门槛与失败处置** |
| 2 调研 Review | 无 | **有**：验证文献引用（arXiv 编号 / 作者 / 年份）、标注置信度 | 无「验证器是谁」的约束——**默认让模型自己核**（§4.4 证否） |
| 3 设计 | 无 | 模板要求架构 / 模块 / 接口 / 数据流 | **无「拒绝的替代方案」**、无 taste 判据 |
| 4 设计 Review | 无 | **有**：基于已验证结论 / 未验证假设 / 归因扭曲 | 无角色化审查、无机械面 |
| 5 实施文档 | 无 | **有**：版本 / 依赖 / 兼容性 / 接口签名 / 低效排除 | 无「依赖存在性」机械核验 |
| 6 实施 Review | 无 | **有**：依赖版本真实存在、签名可实现 | 同上（靠人眼） |
| 7 验收清单 | 无 | **有**：每项可测试、有明确通过条件 | 无 DoR/DoD 形态约束 |
| 8 一致性 Review | 无 | **有**：三对文档对齐 | 本仓已有机械面（`dc_validator`），但**未在流程正文声明** |
| 9 TDD 实现 | 无 | **有**：「先写测试（基于 CHECKLIST）」「测试通过 ≠ 设计落地」 | 无「测试上下文」要求（§4.3 的关键变量） |
| 10 审查验收 | 无 | **有**：ADD + 取证矩阵 + 开发日志 + PROGRESS | 无 skill 绑定（外部 `audit-driven-development` 位） |

**结论（B1）**：十步里**只有 Step 1 有工具条款、Step 2/9 有半句提示词条款**；其余 7 步的「工具 / 提示词」是**隐性惯例**，没写进宪法 ⇒ **同一步不同批次的做法可以完全不同，且无任何记录**。

### 3.2 本机实接面（E1）

**外部 MCP server 5 个**（按能力归组）：

| server | 覆盖 | 对哪步有用 |
|---|---|---|
| `mcp_paper-search` | 21 个学术源（arxiv / pubmed / semantic / crossref / openalex / dblp / ACL 类 …）+ 下载 + 读全文 | Step 1 / 2（学术） |
| `mcp_scholar-mirror` | 9 个 Google Scholar 镜像 + Semantic Scholar API | Step 1（学术，镜像兜底） |
| `mcp_english-search` | web / pdf / news / academic 四通道（**本次 404**） | Step 1（通用） |
| `mcp_research-tools` | arxiv / semantic 检索 + 论文下载 + **memory_search / artifact_record / decision_record** | Step 1 / 10 |
| `mcp_stackexchange` | 184+ 站点（math / stats / quant / cs / ai / academia / programming …） | Step 1（工程实践与反例） |

**本地 skill 213 个**（与本调研相关的分组；`~/.trae-cn/skills/` 机械枚举）：

| 面向 | 可用 skill（示例，非全量） |
|---|---|
| 调研 / 检索 | `research-scout` / `research-lookup` / `literature-review` / `deep-research` / `paper-lookup` / `exa-search` / `parallel-web` / `paperzilla` |
| 批判 / 审查 | `scientific-critical-thinking` / `peer-review` / `scholar-evaluation` / `hypothesis-generation` / `scientific-brainstorming` |
| 设计 | `brainstorming` / `writing-plans` / `frontend-design` / `huashu-design` / `brand-guidelines` / `theme-factory` / `what-if-oracle` / `consciousness-council` |
| 实施 / 验证 | `test-driven-development` / `executing-plans` / `audit-driven-development` / `verify-mode` / `webapp-testing` / `dogfood` |
| 学术推理 / 写作 | `academic-paper`（12-agent 流水线）/ `academic-pipeline` / `academic-paper-reviewer` / `paper-writing` / `scientific-writing` / `citation-management` / `math-finance-reasoning` / `statistical-analysis` / `venue-templates` |
| 工程质量 | `git-commit` / `gh-cli` / `TRAE-security-review` / `humanizer` / `avoid-ai-writing` |

> **注意**：这 213 个 skill **不是本仓制品**，它们的可用性随环境漂移。把某个 skill 名写进流程正文 = 引入一个**无法被本仓机械核验**的外部依赖（§6.3 R1）。

### 3.3 本仓已有的三个「隐式绑定」先例

| 先例 | 已有做法 | 对应哪步 | 说明 |
|---|---|---|---|
| `dc_validator` selftest **F27-F33**（P-106） | **先写 fixture 再写实现**，红→绿 | Step 9 | 这就是本仓事实上的 TDD：**fixture 是测试上下文**，不是提示词 |
| 断言分级 **A/B/C + E1-E5** | 按「证据来自哪一层」分档，E1 = 逐字读原件 | Step 1 / 2 / 10 | 已经是**来源分层的本仓版本**，只是没和「检索工具」连起来 |
| `hook-surface` v1.1 **P2-1**（2026-09-09） | 审查发现引证含来源里没有的杂词「MySQL」 | Step 2 | **反例**：检索→写作→审查链路上，来源污染真实发生过 |

**结论（B2）**：本仓**不缺「原则」**（证据分级、TDD、独立审查都在），缺的是**「哪一步用哪个通道、拿到什么形态的证据」这一步的连接件**。

---

## 4. 外部证据（五条关键发现，T1 定位）

> 本节所有数值均按 §7.1 的定位回原文核验；**不可定位的转述已删除**。v1.1 的核验本身即 §5.3 四步流水线的一次实例。

### 4.1 Skill 有正向增益，但「聚焦」优于「堆叠」

- **SkillsBench**（arXiv:2602.12670，T1 摘要 + HTML）：策展 skill 把平均通过率从 **33.9% → 50.5%（+16.6pp，25.5% 归一化增益）**，配置级增益 **+4.1~+25.7pp**；**≤3 个模块的聚焦 skill 优于更大或穷举式 bundles**；小模型 + skill 可追平大模型无 skill。
- **Anthropic Agent Skills 官方文档**（T1，`platform.claude.com` overview「How Skills work」+ best-practices「Progressive disclosure patterns」）：三级渐进披露——**Level 1 元数据常驻（约 100 tokens/个）**、**Level 2 正文按触发加载（< 5k tokens）**、**Level 3 资源按需读取**；`description` 必须同时写清 **what + when**；**SKILL.md 正文 < 500 行**。工程博客（T2，2025-10-16）只作发布事实与「按需加载」的二手佐证。
- **v1.1 订正**：v1.0 另称「不含时效性信息」为官方最佳实践——在 overview 与 best-practices 两页**均未定位**，本版删除。

⇒ **可绑，但必须「每步 ≤ 1-2 个、按触发条件加载」，而不是「全量挂载」。**

### 4.2 工具过载会反向降质（不是「多一点更好」）

- **RAG-MCP**（arXiv:2505.03275，T1 摘要 + HTML §1/§3）：工具选择准确率 **基线 13.62% → RAG-MCP 43.13%**（原文 "more than triples"）；prompt tokens 降低 **> 50%**；stress test 显示**随 MCP schema 数量增加，选择准确率与任务成功率下降**。
- **v1.0 的二手读数已证伪并删除**：原写「工具选择准确率从 **43% 基线降到 < 14%**」——原文方向**相反**：43.13% 是**检索增强后**的结果，13.62% 才是基线。该二手博客另称「约 50 个工具开始下滑 / 约 120 个崩塌 / 72% 上下文被工具定义占用」，在 T1 摘要与可见正文中**均未定位**，本版**不作为论据**。

⇒ **这条直接否掉「把 200 个 skill 全列进流程」的做法**（工具数量增长导致选择质量下降，T1 stress test 方向）。也解释了为什么本仓采用**懒加载架构门禁**（ADR-0010 三问）是正确方向。**同时它是 T4 转述风险的活样本：一次方向倒置可以完整反转结论。**

### 4.3 TDD 提示词单独不够，关键是「定向测试上下文」

- **TDAD**（arXiv:2603.17973，T1 arXiv HTML）：SWE-bench Verified 上回归率 **6.08% → 1.82%（-70%）**；**prompt-only 组（仅加 TDD 程序性指令、无定向测试上下文）回归率升至 9.94%，高于无干预基线 6.08%**。
- **TDD-Agent**（arXiv:2608.16742，T1）：test-first reasoning prompt 在 LiveCodeBench 上对 reasoning baseline 一致改进；RepoEval 上优于检索式 / agent 式基线。
- **TDD-Bench Verified**（arXiv:2412.02883，T1）：**449** 个 issue；LLM「先于修复写出能失败的测试」本身是独立能力，需要专门流程而非一句「请用 TDD」。
- **v1.1 订正**：v1.0 写 prompt-only「**未见同等改善**」——原文实际是「**更差**」（9.94% > 6.08%）。该转述**低估了原文**，本版按原文改写。

⇒ **「执行阶段要求 TDD」若只写成一句提示词，按现有证据不仅大概率是表演，还可能使回归率上升**；真正起作用的是**先把可执行的失败测试造出来**（本仓 = fixture + 可重放的 selftest 编号）。

### 4.4 引用幻觉是基线问题，且 LLM 不能自任验证器

- **GhostCite**（arXiv:2602.06718，T1 arXiv HTML v1「Key Findings」）：13 个 SOTA LLM **全部**出现引用幻觉，区间 **14.23%–94.93%**，且有领域敏感性；**LLM 作为引用验证器仅 38% 准确率——原文措辞 "even lower than random guessing"**。标题原文为 "…in the Age of **Large Language Models**"（v1.0 缩写为 "LLMs"，本版订正）。
- **Biomedical 26 模型审计**（arXiv:2609.14988，T1 摘要）：**55.4%** 的参考文献为编造，**仅 14.9%** 全部字段正确。
- **跨模型审计**（arXiv:2603.03299，T1）：幻觉率 **11.4%–56.8%**，**由 prompt 框架诱发**（不加提示时模型不主动编引用）；**">3 个 LLM 一致" 的共识准确率 95.6%**，被列为可用过滤手段。（v1.0 写「≥3」，边界错，本版订正为 **>3**。）
- **部署约束研究**（arXiv:2603.07287，T1）：17,443 条生成引用中**无模型**的「引用存在率」超过 **0.475**；输出仍然格式合规 ⇒ **格式合规 ≠ 引用真实**。
- **验证侧可行**：VeriCite（2510.11394，T1）、CiteGuard（2510.17853，T1：68.1% vs 人类 69.2%）、CiteFix（2504.15629，T1：行业引用准确率约 74%，相对提升 15.46%）——**事后机械核验有效**。

⇒ **Step 2 的「验证文献引用」必须指定为「DOI / arXiv ID 可解析」的机械动作**，而不是「再问模型一遍」。

### 4.5 taste 不能外包给现成 judge

- **TASTE**（arXiv:2605.20731；读数经 **T2** 页面 Glif / Contra 转述）：现成 judge 最高 **0.543**，人类设计师 **0.741**；专门训练的判别头 **0.611**。Contra（T2，2026-06-17）另报：无现成 judge 超 **55%**（最好 54.3%），人类 74.1%，训练后 61.1%；**在最难的 3-2 分歧上 0.602 vs 人类上限 0.600**。
- **Human Creativity Benchmark**（arXiv:2606.30561，T1）：创意质量须分离 **convergence（专业共识）** 与 **divergence（个体品味）** 两种信号；**它不承载 0.543 / 0.741 两个数字**（v1.0 的归属混淆，本版订正）。

⇒ **「设计阶段约束 taste」不能落成「✅ 好看 / ✅ 有品味」这种勾选**——那是本仓最反感的表演形态。只能落成：**可列举的判据维度 + 被拒绝的替代方案 + 代价**。

---

## 5. 逐阶段映射建议（核心）

> **共同原则**：① 每步**最小工具集 ≤ 2**；② skill **按触发条件**挂 1 个；③ 提示词硬约束**必须是能机械核验的形态**（有 / 无、可解析 / 不可解析、可重放 / 不可重放）；④ 每步声明**证据出口**（写回哪一节、什么形态）。

### 5.1 总表

| Step | 最小工具集 | 可选 skill（触发条件） | 提示词硬约束（可核验） | 证据出口 |
|---|---|---|---|---|
| 1 调研 | `WebSearch` 或 `mcp_english-search`（通用）+ `mcp_paper-search` / `mcp_scholar-mirror`（学术）+ `Grep/Read`（本仓） | `research-scout`（多源发散）/ `literature-review`（系统性综述） | 关键结论 **≥2 独立来源且 ≥1 个 T1**；每条来源标 **Layer + 日期 + 版本**；检索失败必须写**降级链走了哪一跳** | §3 发现表 + 附录来源清单 |
| 2 调研 Review | `mcp_paper-search_search_crossref` / `get_crossref_paper_by_doi`、`search_arxiv` | `scientific-critical-thinking`（反方角色） | **每条引用 DOI/arXiv 可解析**；不可解析 ⇒ 只能标「未验证」，**禁止标 ✅**；LLM **不得**自任验证器 | §5.1 验证表（`引用 / ID / 验证方式 / 状态`） |
| 3 设计 | 无（纯文档）；需要外部事实时回 Step 1 | `brainstorming`（发散未定）/ `writing-plans`（结构化成文）/ `what-if-oracle`（分支情景） | 每个关键决策必须写 **被拒绝的替代方案 + 拒绝理由**；新增面须过 **ADR-0010 三问** | §决策表 + §拒绝方案 |
| 4 设计 Review | 无 | `scientific-critical-thinking` | 逐条检查「是否基于已验证结论」；**归因扭曲**单列 | §Review 表 |
| 5 实施文档 | 无 | `spec-to-implementation`（多任务拆解） | 每个接口写**签名 + 回退点**；低效排除表非空 | §接口 / §回退点 |
| 6 实施 Review | `Shell`（版本存在性）/ 官方源 `WebFetch` | — | 依赖版本**可查到**；签名**可实现** | §版本核验表 |
| 7 验收清单 | 无 | — | 每项写 **DoR / DoD**；禁止无证据的 ✅ | CHECKLIST §2 |
| 8 一致性 Review | `scripts/dc_validator.py`（机械面） | — | 三对文档对齐；机械结果**必须贴读数** | §1 一致性表 |
| 9 TDD 实现 | `Shell`（跑测试） | `test-driven-development` | **先写会失败的测试**（本仓 = fixture 编号 + 红），**再写实现**；只写提示词不算 | §8.1 fixture 表 + 红→绿记录 |
| 10 审查验收 | `scripts/dc_validator.py` / `m7_stats.py` / `repo_stats.py` | `audit-driven-development` | ADD 四阶段 + 取证矩阵 E1-E5；每条 ✅ 绑证据 | CHECKLIST §8 / §10 |

### 5.2 Step 1 调研：三层来源阶梯（回答「学术源 / 开源社区」）

**分层（按可得证据强度，不按「听起来权威」）**：

| 层 | 内容 | 本机通道 | 用法约束 |
|---|---|---|---|
| **T1 一手** | 论文原文 / 标准 / 官方文档 / 源码 / 仓内文件 | `mcp_paper-search_download_*` + `read_*`；`WebFetch`；`Read/Grep` | **A 类断言只接受 T1**；必须能给出可解析 ID 或文件路径 |
| **T2 二手权威** | 维护者 issue / release note / 官方博客 | `mcp_english-search`、`WebFetch`、`gh`（若可用） | 可作为「事实状态」来源，但不能替代 T1 的方法学结论 |
| **T3 社区** | StackExchange / 论坛 / HN | `mcp_stackexchange_search_questions`（按票排序）、`WebSearch` | **只用于发现反例与工程陷阱**，不得作为「最佳实践」的唯一依据 |
| **T4 转述** | 聚合博客 / 二手解读 | `WebSearch` | **只能作线索**；其中的数字必须回溯到 T1/T2，否则标 E3 并显式写「未回原文」 |

**降级链（必写）**：`目标通道 → 备用通道 → 已读到的本仓/本机事实 → 「未取证」声明`。

> 本次调研本身就是实例：`mcp_english-search` 两次 404 ⇒ 降到 `WebSearch`；`paper-search` 的 semantic/openalex 返回 0 ⇒ 只采用 arxiv 4 条并标明「源覆盖不全」；v1.1 核验再证 **T4 不可直接采信**——§4.2 的二手读数方向倒置，回 T1 后才纠正。

**反模式（须显式避免）**：

- 「搜到了 = 事实」——T4 转述当 T1 用（本仓 `hook-surface` P2-1 已发生过一次；本批 §4.2 是第二例）；
- 「只有一个来源但写成共识」——必须写「单源」；
- 「工具失败静默跳过」——必须写降级走了哪一跳。

### 5.3 Step 2：引用核验流水线（四步，可机械执行）

1. **抽取**：把所有 `arXiv:xxxx` / DOI / URL 列成表（本仓已有 `§5.1 文献验证` 表的位）；
2. **解析**：逐条调 `search_crossref` / `get_crossref_paper_by_doi` / `search_arxiv`——**返回命中才算「存在」**；
3. **字段比对**：标题 / 作者 / 年份至少两项一致；不一致 ⇒ 标「元数据错配」（比「不存在」更常见）；
4. **落状态**：`已验证（T1 命中）` / `元数据错配（列出差异）` / `未验证（解析失败）`——**禁止出现「已验证」但无解析记录的行**。

**为什么不能让模型自查**：§4.4 的 38% 验证器准确率（GhostCite HTML v1「Key Findings」，低于随机）是直接反证；本仓的等价做法是 **E1 逐字读原件**，而不是「我确认过了」。

### 5.4 Step 3 设计：把 taste 变成「可审查」而非「可判定」

**三条约束**：

1. **禁止把 taste 写成勾选项**（§4.5：现成 judge 与人类一致率差距大，勾选 = 表演）；
2. **每个关键设计决策必须写「被拒绝的替代方案 + 拒绝理由 + 代价」**——这是 taste 唯一可被第三方复核的形态；
3. **品味分歧显式登记**：区分「专业共识」（可用判据表达）与「个体偏好」（只能由用户裁决）——对应 HCB 的 convergence / divergence。

**本仓可用的判据维度**（把「优雅」翻译成可操作项）：新增面数量 / 可逆性（回退点） / 单一真值源 / 副作用面（ADR-0010 Q3） / 认知负担（读者要记几个概念）。**这些能进 CHECKLIST；「好看」不能。**

### 5.5 Step 4/6/8：角色化审查 + 机械面分工

- **角色化**：Step 4 用「反方」角色（`scientific-critical-thinking` 的 stance），要求**先给最强反驳再给结论**；多智能体辩论对事实性有正向证据（arXiv 2305.14325，T1），但**成本高**，本仓只在「设计决策不可逆」时启用；
- **机械面优先**：能用 `dc_validator` / `repo_stats` 判的，不进人工 Review（否则人工会退化成「复述机器结果」）；
- **独立性**：守 RULE-1（时序独立）+ RULE-5（模型异质），这条**已经**比「绑 skill」更重要。

### 5.6 Step 5：实施文档

- 接口签名 + 回退点 + 低效排除表 = 本仓已成型的三件套（`IMPLEMENTATION.md` §3.x / §8.1）；
- 可选的 skill（`spec-to-implementation`）仅在**任务粒度失控**（一份文档塞 ≥3 个独立能力）时触发；
- **不引入**「自动生成实施文档」类工具：本仓的价值在**手工判据**，自动生成会直接制造形态 II。

### 5.7 Step 7：验收清单可测试性

- 每项必须有 **DoR（怎么进入验收）/ DoD（什么算过）**，且 DoD 是**可重放的命令或可逐字核对的形态**；
- 禁止：「功能正常」「体验良好」「代码优雅」——这类项一律改写为可判定的替代形态，或**移到设计文档的「拒绝方案」段**。

### 5.8 Step 9：TDD 双要素（提示词 + 测试上下文）

按 §4.3，**只写提示词不够，甚至可能更差**。本仓的可执行形态：

| 要素 | 本仓等价物 | 反例 |
|---|---|---|
| 失败的测试（先） | selftest 里新增 `F<n>` fixture，先跑出 **FAIL** | 先写函数再补测 |
| 定向测试上下文 | fixture 内含**目标形态 + 反例形态**（如 P-106 的 F27-F33：2 检出 + 4 不判定 + 1 逐链接） | 只写「请用 TDD」 |
| 红→绿记录 | IMPLEMENTATION §8.1 表 + §8.2 读数（39/39） | 「测试全过」但无失败记录 |

> **本仓已有最佳实例**：P-106 的 M6 实施——先写 7 个 fixture（含 4 个边界负例），再写 `check_version_refs`，最后 39/39。**这就是「执行阶段要求 TDD」在本仓的落地形态**。

### 5.9 Step 10：ADD 取证

- 机械三件（`dc_validator` / `m7_stats` / `repo_stats`）+ 门禁链（`step-gate` / `verify-anchor` / `step-enforce`）+ 只读诊断器（`backflow-audit` / `anchor-audit` / `rework_graph_check`）已是既定形态；
- **可绑但不必绑** `audit-driven-development`：它的四阶段与本仓 ADD 节同构，绑定收益主要是「提醒」，而提醒可以用 §8 节的表格承载——**避免为一个提醒挂一个 skill**（§4.2）。

### 5.10 学术推理任务的附加约束（八条）

> **规范本体已独立成文**：[ACADEMIC_REASONING_CONSTRAINTS.md](../academic-writing-workflow/ACADEMIC_REASONING_CONSTRAINTS.md)（v1.0，P-116）。
> 本节只保留指针，**不复制八条**（守「一份真值」）；学术域执行前必读该文档。

> **适用范围**：学术域产出；纯工程批可选用第 1 / 5 / 8 条。
> **为什么移出**：避免与 SPEC_PROCESS / ACADEMIC_FILE_SPEC 形成多副本；U-3 判据「唯一载体 + 被引用」由此闭合。
> **证据依据**：新文档 §1；本 RESEARCH §4.3–§4.5（T1 定位）。
> **边界**：形态约束，不承诺可机械检出；不新增门禁。

> 迁移记录：P-116（2026-10-21）；本节行数保持不变以稳定 P-115 会话锚点。
> 关联：SPEC_PROCESS §Step 工具与提示词契约（通用流程）/ ACADEMIC_FILE_SPEC §7（静态合规）。

---

## 6. 综合分析

### 6.1 三条结论

**C-1（结论）**：**可以精细化，但不是「给每步挂一堆工具」，而是「给每步定一条最小通道 + 一条硬约束 + 一个证据出口」。** 依据：§4.1（聚焦优于堆叠）+ §4.2（工具数量增长反向降质）+ §3.1（现状只有 Step 1 有契约，其余全是隐性惯例）。

**C-2（结论）**：**提示词只能约束「形态」，不能约束「质量」。** 依据：§4.3（TDD 提示词单独甚至更差：9.94% vs 6.08%）+ §4.4（LLM 自任验证器 38%）+ §4.5（taste 的 judge 与人类差距）。⇒ 写进流程的提示词必须**落到可机械核验的形态**（可解析 ID / 有失败 fixture / 有拒绝方案），否则就是**形式化审查表演**。

**C-3（结论）**：**「taste」在本仓应落为「被拒绝的替代方案 + 判据维度」，不落为勾选项。** 依据：§4.5。这是本仓能否避免「用品味之名行表演之实」的分水岭。

### 6.2 分档方案

| 档位 | 内容 | 代价 | 收益 | 判定 |
|---|---|---|---|---|
| **A 现状** | 不改；只在批次里凭经验选工具 | 零 | 零 | 已证不足（§3.1 七步无契约；§3.3 已发生来源污染） |
| **B 最小绑定（推荐）** | 在 `SPEC_PROCESS` 增**一张表**（Step × 最小工具集 × 硬约束 × 证据出口）+ 四类重点各一节（§5.2 / §5.8 / §5.4 / §5.10）；**Layer-0，零门禁** | 新增约 1 节文档；每批多写「来源分层 / 降级链」 | 让「用了什么通道」可复核；把已有隐性惯例显式化 | **推荐**：判据可核、零代码、可回退 |
| **C 全编排** | 把 213 个 skill 按步编排成路由表 + 自动触发 | 高（工具过载 §4.2；skill 可用性不在本仓控制内；新增大量可漂移声明） | 表面自动化 | **否决**：与 ADR-0010 Q3（未激活副作用 = 0）冲突，且制造新的权重面 |

> **B 档的边界**：B 档**不新增门禁**。若未来要机械核「来源分层」，只能核**形态**（如「§3 是否存在 Layer 列」「引用表是否每行有 ID」），**不能核「这条结论是否真的来自该来源」**——后者永远要人看。这条边界必须写清楚，否则 B 档会退化成 C 档的表演。

### 6.3 风险与诚实边界

| 编号 | 风险 | 证据 | 处置 |
|---|---|---|---|
| R1 | **skill 是环境态，不是仓内制品** ⇒ 写进流程正文会引入不可核验的外部依赖 | §3.2：213 个 skill 与 5 个 MCP 均为本机状态，随环境漂移 | 流程正文只写**能力类别**（「学术检索」「批判审查」），具体 skill 名放**附录 / 执行卡**，并标「按环境可用性取舍」 |
| R2 | **工具可用性不均**：本次 `mcp_english-search` 两次 404、`paper-search` 仅 arxiv 有结果 | §2.1 实测 | 每条工具条款必须配**降级链**（§5.2）；不允许「单点通道」 |
| R3 | **「绑了 = 做了」的表演风险**：把 skill 名写进 CHECKLIST 并打 ✅ | 本仓 M7 形态 II 的历史教训 | 硬约束只写**可核验形态**；skill 调用**不得**作为验收证据（只有产出形态才是证据） |
| R4 | **B 档仍不能消除手工回写**（同 P-105 教训） | P-103 / P-105 同族 4 例 | 预期管理：B 档是「可复核」，不是「自动化」；不承诺减工作量 |
| R5 | **二手转述可反转结论**；v1.0 的 E2/E3 读数存在方向与归属失真 | §4.2 的 43%→<14% 方向倒置；§4.5 的 TASTE 归属混淆；§4.3 的 TDAD 低估 | v1.1 已全量回原文（§7.1）；**外部数字只作背景，不作任何门禁判据**；新增数字未定位则只能标「未验证」 |

### 6.4 未决项登记（四元块）

- **U-1 B 档落点：改 `SPEC_PROCESS` 正文 vs 新增独立附录文档**
  - **判据**：落点确定且不产生第二真值源（同一规则不出现在两处）
  - **触发条件**：用户裁决「按 B 档实施」
  - **当前倾向**：**已裁决并落地**——P-108 在 `SPEC_PROCESS` 正文新增 §「Step 工具与提示词契约」（单节，约 60 行），未另建文档
  - **证据等级**：B5（推断）→ **已闭合（2026-10-21，P-108）**

- **U-2 外部读数是否回原文核验** —— **已闭合（2026-10-21，P-115）**
  - **判据**：§4 中被引用的每个数值都有对应的 T1 原文页码 / 段落
  - **达成情况**：**19/19 条已核**（17 条 T1 命中 + 2 条 T2 官方页），外加 3 条补充页（Anthropic best-practices / RAG-MCP / TASTE 读数页）；§4 现存的每个数值均标 T1 定位（摘要 / 章节 / Key Findings）；**不可定位的二手数字已删除**（§4.2 的 50/120/72%）；订正 9 处（§7.1 末列）
  - **残余边界**：T2 读数的 page 可能随厂商改版漂移；复算时以 §7.1 的 URL + 定位重取
  - **当前倾向**：**关闭**；后续新增外部数字须按 §5.3 四步登记 ID + 位置，否则只能标「未验证」
  - **证据等级**：**E1**

- **U-3 学术推理附加约束是否独立成文** —— **已闭合（2026-10-21，P-116）**
  - **判据**：八条约束有唯一载体，且被 `academic-writing-workflow` 引用而非复制
  - **触发条件**：学术域下一批（S3 首轮或 G-11b 点名）启动时
  - **当前倾向**：**独立成文**——[ACADEMIC_REASONING_CONSTRAINTS.md](../academic-writing-workflow/ACADEMIC_REASONING_CONSTRAINTS.md) v1.0 为唯一权威；SPEC_PROCESS / 本文件只留指针
  - **证据等级**：B6（推断）→ **已闭合（P-116）**

### 6.5 分阶段外部信息锚点与多方案裁决取证（P-161，2026-11-06）

**问题 1：外部信息源是否只在调研阶段被显式要求？**

A-16 现状 = **是**，且只到「Step 1 硬约束 + Step 3 回退」这一层：

| Step | 外部检索要求 | 形态 |
|---|---|---|
| 1 调研 | **有（唯一硬约束）** | 学术检索 + 通用检索 + 本仓检索；关键结论 **≥2 独立来源且 ≥1 个 T1**；证据出口 = §发现表 + 来源清单 |
| 2 调研 Review | 有（核验，非检索） | 每条引用 **ID 可解析**；不可解析只能标「未验证」 |
| 3 设计 | **无，仅回退** | 契约原文 = 「无（纯文档）；**需外部事实时回 Step 1**」 |
| 4 设计 Review | 无检索要求 | 只核「是否基于已验证结论 / 无未验证假设 / 替代方案 ≥2」 |
| 5 实施文档 | 无 | 只约束签名 + 回退点 + 低效排除表 |
| 6 实施 Review | **狭义外部核验** | 依赖版本**可查到**（存在性，不是「最佳实践」） |
| 7/8/9/10 | 无外部检索 | 验收 / 一致性 / TDD / ADD 取证矩阵（E1-E5，面向本仓代码） |

A-20 补充：Review 面存在**间接**约束——Step 4 要求「设计基于已验证的调研结论」，但它只约束**是否引用了已核结论**，不约束**该结论是否覆盖了外部成熟实践**；两者不等价。

**问题 2：多方案裁决的七维信息是否未提及？**

A-17 **已提及**：`SPEC_PROCESS` §迭代收敛与未决项登记的 Type-1/Type-2 委派规定「**Type-1（不可逆）⇒ 全维度取证（决策矩阵）**」；模板七维**逐行固定** = 成本 / 收益 / 可维护性 / 兼容 / 升级潜力 / 短期 / 长期，每格要求「证据等级 + 读数日期」。

A-18 但模板自陈「**无门禁、无校验器**」，可机械化仅四项形态（格齐全 / 证据等级非空 / 触发条件存在 / 引用完整），**结论正确性显式留给人工**。

A-19 实际使用仅 **3 处**，且全部集中在 project-console（§7.26 件② 目标路径 / §7.27 派生态启用 / §7.28 `§` 编号空间收口）；`DESIGN_TEMPLATE §11.2` 只引不复制。**尚无任何一批在「方案裁决」之外主动启用它**。

**缺口判定（B 类）**

B7 外部锚点的必要性应随**断言类型与不确定性**触发，而不是随阶段触发：A 类事实（涉及本仓外世界）必须有 T1；纯本仓事实（E1）不需要；方案裁决若缺本仓读数，可引外部「形态对照」，但**不构成有效性证据**（与 §4.5 / R5 同一边界）。

B8 七维矩阵的缺口**不是「没有」而是「不可判」**：Type-1 判定自陈、七维无操作化定义、无门禁 ⇒ 容易退化为「填满七格」的表演（与 C-2 同族）。

**建议（C 类，Layer-0、零门禁、零代码）**

C-6 **三档触发**（替代按阶段一刀切）：① 新引入外部技术 / 框架 / 协议 / 标准 ⇒ **T1 必需**；② 断言涉及本仓外事实且会改变设计 ⇒ **T1 必需**；③ 纯本仓可自证 ⇒ **E1 足够**，不要求外部检索。

C-7 **Step 3 / Step 5 契约各补一行「触发式回退」**：命中 C-6 ①/② ⇒ 回 Step 1，并在 §决策表标 T1 + 读数日期；未命中 ⇒ 允许纯文档并写明「无外部事实断言」。**不新增门禁**（只改形态约束文本）。

C-8 **矩阵两档化**：Type-1 七维全填；**Type-2 只强制「成本 / 收益 / 回退点」三格**——保留取证、避免分析瘫痪（守净收敛纪律与「Type-2 不启动矩阵」的原意兼容）。

C-9 **七维操作化**（每维一条可核验问句）：成本 = 改动文件数 / 新增依赖数（可复算）；收益 = 解决哪条已登记缺口（引编号）；可维护性 = 新增真值源 / 双写点数量；兼容 = 是否改动既有契约 / 词表 / 退出码；升级潜力 = 是否有显式回退点与触发条件；短期 = 本批能否独立回退；长期 = 是否制造需持续维护的第二载体。

**边界（诚实）**：本批只出分析与建议——**不改** `SPEC_PROCESS` 正文、**不改**模板、**不新增**门禁；C-6~C-9 是否落地须另行开批（Layer-0 文档批即可）。

### 6.6 外部可借鉴的阶段映射实践（P-162，2026-11-07）

**调研范围**：只取**社区反馈良好、且在真实仓库持续使用**的开源项目；不限于本机已安装工具。全部回原文（仓库 README）核验，证据等级 T1；只提炼**阶段模型 / 产物形态 / 门位点**三类形态，不评估其在本仓的有效性。

A-21 **GitHub Spec Kit**（MIT）：把流程拆成 `constitution → specify → plan → tasks → implement` 五个可独立调用的入口，并明说「**These are independent entry points, not mandatory phases**」；其补强面不是更多阶段，而是**可组合机制**——`Extension`（新增命令 / 质量门 / 完整流程）、`Extension hook`（在命令前后执行，即 **before/after 两型门位点**）、`Preset`（强制组织或监管标准）、`Workflow` + `overlay` + `step`（流程可叠加改造而不 fork）、`Bundle` / `Catalog`（按角色分发）。原文同时提示「Catalog listings are not audits or endorsements」。来源：<https://github.com/github/spec-kit>。

A-22 **OpenSpec**（MIT）：以**变更包**为单元——`explore → propose → apply → archive`；`propose` 一次产出四件（`proposal.md` 说明为什么/改什么、`specs/` 需求与场景、`design.md` 技术方案、`tasks.md` 实施清单），**纯 Markdown**、需求用 `WHEN/THEN` 场景表达；原文强调「**You review the plan before any code is written**」，`archive` 时把变更归档并更新 specs（specs 是长期真值，changes 是短生命周期）。`Stores`（beta）把 specs 与 changes 放到独立仓，跨仓共享单一真值源。来源：<https://github.com/Fission-AI/OpenSpec>。

A-23 **BMAD-METHOD**（MIT）：交付环 = **Clarify → Plan → Build and verify → Learn and adjust**，并明确「**Right-sized process**」——清晰的小改动**直达 build**，复杂工作才加深规划；同时提供多视角角色（product / architecture / UX / development / testing）与「durable context」（决策随产物前传，而非每次对话重讲）。来源：<https://github.com/bmad-code-org/BMAD-METHOD>。

**与本仓 10 步的对照（判断）**

| 外部形态 | 本仓现状 | 可借点 | 不借点 |
|---|---|---|---|
| Spec Kit：入口可独立、门挂在命令前后 | 10 步固定序 + 偶数步 Review | **before/after 两型门位点**（前置校验 / 后置证据）| Extension/Workflow 生态（引入工具链依赖） |
| OpenSpec：一个变更包 = proposal + specs + design + tasks | 四件套（R/D/I/C） | **「review before code」写成显式门**；变更包归档语义 | 另立 `changes/` 目录（与四件套双真值源） |
| BMAD：right-sized（小改动直达 build） | T1/T2/T3 档位（仅裁剪文档量） | **把档位与「必需阶段」显式成表** | 多角色 agent 编排（本仓无此负载） |
| 三者共同 | 阶段 = 产物 + 门 | **补强对象是产物契约与门位点，不是阶段数量** | — |

B9 阶段映射的正确补强对象是**产物契约 + 门位点**：三个项目都不靠增加阶段取胜（Spec Kit 明说入口非强制阶段；OpenSpec 把阶段收敛为一个变更包的四个产物；BMAD 让阶段随工作量伸缩），而都靠「每阶段产出什么、在哪里拦」取胜。

C-10 **阶段产物契约表**：在 `SPEC_PROCESS` 契约节补一张「Step × 产物文件 × 最小必含节 × 证据出口」表（本仓四件套已具备产物，缺的是**逐阶段最小节**），使「阶段完成」有可核形态。**不新增门禁。**

C-11 **门位点两型化**：若未来新增阶段门，形态只允许 before（进入前校验，如「调研未核引用不得进设计」）与 after（退出后取证，如「设计须有拒绝方案与代价」）两型；禁止无位点的「过程要求」。本批只登记形态，不实施。

C-12 **档位 × 必需阶段矩阵**：把 T1/T2/T3 从「文档量裁剪」升级为「可跳过哪些阶段」的显式矩阵（例：T3 是否强制 Step 4/6 Review），使裁剪理由可复核。

**边界（诚实）**：这些项目解决的是「agent 驱动的产品交付」，本仓是**单人 + 方法论仓**；外部形态只作**结构参照**，不构成本仓有效性证据，也**不引入任何依赖**（守 ADR-0010 Q3 与 §6.3 R1）。

### 6.7 契约取证字段形态化与前瞻预注册（P-163，2026-11-08）

**只读核对（6 个真实批次）**：样本 = P-115（T3 订正）/ P-137（T1 完整管线）/ P-151（T3 取证）/ P-154（T3 调研补充）/ P-161（T3 文档，任务来源明写「按吃狗粮方式」）/ P-162（T3 调研补充，本批自身）。判据 = 契约表 10 行中的**适用行**是否按形态出具（● 出具 / ◐ 部分 / — 不适用）。

| 批次 | S1 来源三字段 | S2 验证表 | S3 拒绝方案 + 代价 | S7 DoR/DoD | S9 红→绿 | S10 机械读数 |
|---|---|---|---|---|---|---|
| P-115 | ◐ 层✓ / 日期✗ / 版本✗ / 降级链✗ | ● 22 行六列表 | — | — | — | ● |
| P-137 | — 本批无新增外部检索 | — | ● DESIGN §5 四方案 + 否决理由 | ◐ 有 ✅ + 读数，无 DoR/DoD 词表 | ◐ 用例齐，无先失败记录 | ● |
| P-151 | — | — | — | — | — 无代码改动 | ● |
| P-154 | ◐ 12 条 T1 锚点，无日期 / 版本 / 降级链 | ◐ 有 URL 无表 | ● §13 方案对照含代价列 | — | — | ● |
| P-161 | ◐ 内部 E1 带行号，无文件版本 | ● E1 逐字读原件 | ◐ 建议无拒绝方案表 | — | — | ● |
| P-162 | ◐ 3 条 T1，无日期 / 版本；降级链实际发生未记录 | ◐ 有 URL 无表 | ◐ 可借 / 不借有理由，无代价列 | — | — | ● |

**三条读数（C 类判断）**：

1. **唯一 100% 的是 S10（6/6）——它也是唯一有机械门禁的行**；其余各行靠批次自觉。
2. **S1 的「日期 + 版本」在 4 个外部调研批中 0 次出现；「降级链」0 次记录**——P-162 实际发生 `raw.githubusercontent.com` 抓空后改用 `github.com` 页面的回退，未留痕（正是 R2 要防的形态）。
3. **S9 无一例「先失败」记录**：P-137 有 10 个集成 + 4 个变异用例，但只登记终态全过。

**反面同样要记**：S3 / S5 在 T1 管线里质量最好（P-137 四方案带否决理由、四处接口签名 + 回退点），说明四文档管线对设计面确有约束力，不是全盘失效。

C-13 **五字段形态化（已落地于 SPEC_PROCESS v1.7.2 §契约取证字段形态）**：**F1 来源日期 / F2 来源版本 / F3 降级链 / F4 引用验证表（外部引用 ≥3 条必须建表）/ F5 先失败记录（红→绿两读数）**。只定义形态，不新增门禁；缺项的唯一合法状态 = 「未验证」，不得事后补写。

**前瞻预注册（判据先于执行）**：

| 项 | 预注册内容 |
|---|---|
| 观测对象 | **下一个满足适用条件的真实批次**：外部引用 ≥3 条（触发 F1-F4）或含代码 / fixture 改动（触发 F5）；**不为狗粮造任务** |
| 首个排期样本 | **P-156**（`trigger=date:2026-11-15`）：只读复算批，S1 / S2 / S9 记 **N/A + 理由**，只验 S10 与「N/A 诚实标记」——**N/A 本身也是判据** |
| 判据 | 适用字段**出具率** = 出具 / 适用；**成功线 = 0 未出具**；◐ 部分单列，不并入成功率（不造合成分，同 C-15） |
| 记录位点 | 批次 PROGRESS 行 + session `metadata`（不新增账本、不新增真值源） |
| 窗口 | 3 个适用批次或 2026-12-31，先到为准 |
| 失败处置 | **记录不修补**；同一字段连续 2 批未出具 ⇒ 该字段降为观察项并在此登记（**不升级门禁**） |
| 诚实边界 | 预注册 ≠ 证据；本协议只验「可执行性」，不验「质量提升」（H1 / H2 仍需对照）；样本为目的性抽样，不外推全量 |

---

## 7. 参考文献

> **v1.1 状态**：19 条全部核验（17 条 T1 命中 + 2 条 T2 官方页）；另增补 3 条（RAG-MCP / TASTE / Anthropic best-practices）。逐条状态、定位与差异见 §7.1。T2 条目不替代 T1 方法学结论。

1. SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks. arXiv:2602.12670. https://arxiv.org/pdf/2602.12670v4
2. Anthropic. Equipping agents for the real world with Agent Skills. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
3. Anthropic. Agent Skills 概览. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
4. TDAD: Test-Driven Agentic Development — Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis. arXiv:2603.17973. https://arxiv.org/html/2603.17973
5. TDD-Agent: Test-Driven Reasoning for Code Generation. arXiv:2608.16742. https://arxiv.org/pdf/2608.16742
6. TDD-Bench Verified: Can LLMs Generate Tests for Issues Before They Get Resolved? arXiv:2412.02883. https://arxiv.org/pdf/2412.02883v1
7. GhostCite: A Large-Scale Analysis of Citation Validity in the Age of Large Language Models. arXiv:2602.06718. https://arxiv.org/html/2602.06718v1
8. Biomedical Reference Generation Remains Unreliable across 26 LLMs. arXiv:2609.14988. https://arxiv.org/abs/2609.14988
9. How LLMs Cite and Why It Matters: A Cross-Model Audit of Reference Fabrication. arXiv:2603.03299. https://arxiv.org/pdf/2603.03299v1
10. Do Deployment Constraints Make LLMs Hallucinate Citations? arXiv:2603.07287. https://arxiv.org/html/2603.07287
11. VeriCite: Towards Reliable Citations in RAG via Rigorous Verification. arXiv:2510.11394. https://arxiv.org/pdf/2510.11394
12. CiteGuard: Faithful Citation Attribution for LLMs via Retrieval-Augmented Validation. arXiv:2510.17853. https://arxiv.org/html/2510.17853
13. CiteFix: Enhancing RAG Accuracy Through Post-Processing Citation Correction. arXiv:2504.15629. https://arxiv.org/html/2504.15629v2/
14. Improving Factuality and Reasoning in Language Models through Multiagent Debate. arXiv:2305.14325. https://arxiv.org/pdf/2305.14325
15. The Human Creativity Benchmark. arXiv:2606.30561. https://arxiv.org/html/2606.30561
16. GitHub Spec Kit 文档（Specify → Plan → Tasks → Implement → Converge）. https://github.github.io/spec-kit/ ——**背景对照：正文未引用**（v1.0 孤儿引用，v1.1 显式标注）
17. Unblocked. How Many MCP Servers Is Too Many? The Tool Overload Problem. https://getunblocked.com/blog/mcp-tool-overload/ ——**T3 转述：其方向性读数已被 T1 证伪，仅作线索保留**
18. Glif. Teaching Our Agent to Judge Design. https://glif.app/use-cases/taste
19. Contra Labs. Design Crit: teaching AI to judge design like a designer. https://contralabs.com/research/design-crit
20. RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation. arXiv:2505.03275. https://arxiv.org/html/2505.03275v1
21. TASTE: 设计品味评测原始论文. arXiv:2605.20731.（本条为 §4.5 数值的**真实归属**；v1.0 误置于 HCB）
22. Anthropic. Skill authoring best practices. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

### 7.1 文献核验表（U-2 全量核验，2026-10-21）

| # | 引用（短名） | ID / URL | 验证方式 | 状态 | 命中或差异 |
|---|---|---|---|---|---|
| 1 | SkillsBench | arXiv:2602.12670 | 摘要 + HTML | **T1 命中** | 33.9%→50.5%（+16.6pp，25.5% 归一化）；≤3 模块聚焦优于 bundles |
| 2 | Anthropic 工程博客 | anthropic.com/engineering/... | 页面逐字 | T2 页面命中 | 2025-10-16 发布；2025-12-18 开放标准；三级披露细节在 docs 而非本篇 |
| 3 | Anthropic Agent Skills docs | platform.claude.com/.../overview | 页面逐字 | **T1 命中** | Level 1 约 100 tokens / Level 2 <5k tokens；description 须含 what + when |
| 4 | TDAD | arXiv:2603.17973 | arXiv HTML | **T1 命中** | 6.08%→1.82%；**prompt-only 9.94%（更差）**——v1.0 转述低估，已订正 |
| 5 | TDD-Agent | arXiv:2608.16742 | arXiv PDF | **T1 命中** | LiveCodeBench 一致改进；RepoEval 优于检索 / agent 基线 |
| 6 | TDD-Bench Verified | arXiv:2412.02883 | arXiv PDF | **T1 命中** | 449 issues；fail-to-pass 测试生成是独立能力 |
| 7 | GhostCite | arXiv:2602.06718 | arXiv HTML v1 | **T1 命中** | 14.23%–94.93%；38% 在 **Key Findings**；标题为 "Large Language Models"（v1.0 缩写已订正） |
| 8 | Biomedical 26 LLM | arXiv:2609.14988 | arXiv abs | **T1 命中** | 55.4% 编造；14.9% 全字段正确 |
| 9 | Cross-model audit | arXiv:2603.03299 | arXiv PDF | **T1 命中** | 11.4%–56.8%；**">3" 共识 95.6%**——v1.0 写「≥3」，已订正 |
| 10 | Deployment constraints | arXiv:2603.07287 | arXiv HTML | **T1 命中** | 17,443 条；无模型存在率 >0.475；格式仍合规 |
| 11 | VeriCite | arXiv:2510.11394 | arXiv PDF | **T1 命中** | SIGIR-AP 2025；事后核验可行 |
| 12 | CiteGuard | arXiv:2510.17853 | arXiv HTML | **T1 命中** | 68.1% vs 人类 69.2% |
| 13 | CiteFix | arXiv:2504.15629 | arXiv HTML | **T1 命中** | 行业准确率约 74%；相对提升 15.46% |
| 14 | Multiagent Debate | arXiv:2305.14325 | arXiv PDF | **T1 命中** | 事实性与推理均有提升 |
| 15 | Human Creativity Benchmark | arXiv:2606.30561 | arXiv HTML | **T1 命中** | convergence / divergence 两信号；**不含 0.543 / 0.741**（归属已订正） |
| 16 | GitHub Spec Kit | github.github.io/spec-kit/ | 页面逐字 | T2 页面命中 | Specify→Plan→Tasks→Implement→Converge；**正文未引用（孤儿引用）**，v1.1 标为背景 |
| 17 | Unblocked 工具过载博客 | getunblocked.com/blog/... | 页面逐字 | **T3 转述（方向倒置）** | 称「43% 基线→<14%」；T1 原文为 13.62%→43.13% ⇒ **误读**；50/120/72% 未定位 ⇒ 删除 |
| 18 | Glif TASTE | glif.app/use-cases/taste | 页面逐字 | T2 页面命中 | 0.543 / 0.741 / 0.611；指向 TASTE（arXiv:2605.20731） |
| 19 | Contra Design Crit | contralabs.com/research/design-crit | 页面逐字 | T2 页面命中 | 54.3% / 74.1% / 61.1%；最难 3-2 分歧 **0.602 vs 0.600** |
| 20 | RAG-MCP | arXiv:2505.03275 | 摘要 + HTML | **T1 命中** | 13.62%→43.13%；prompt tokens 降 >50%；工具数量增长致选择质量下降 |
| 21 | TASTE | arXiv:2605.20731 | 经 T2 页面指认 | T2 指认（未逐页读） | §4.5 数值的真实归属；**本仓不将 T2 读数升级为 T1** |
| 22 | Anthropic best practices | platform.claude.com/.../best-practices | 页面逐字 | **T1 命中** | SKILL.md 正文 < 500 行；description what + when；**「不含时效性信息」未定位** ⇒ 删除 |

> **核验结论**：19 条原参考文献 **19/19 已核**（17 条 T1 + 2 条 T2）；补 3 条。**订正 9 处** = §4.2 方向倒置 / §4.3 TDAD 低估 / §4.4 Cross-model 边界 / §4.4 GhostCite 标题 / §4.4 GhostCite 取证位置（摘要→Key Findings）/ §4.5 TASTE 归属 / §4.1 Anthropic 未取证项 / §4.2 三个未取证阈值 / 文献 16 孤儿引用。形态 II 入账见 [M7 样本 #40](../../docs/M7_EVIDENCE_LOG.md)。

---

## 附录 A. A 事实类断言清单（15 条）

| 编号 | 事实 | 取证方式 |
|---|---|---|
| A-01 | 【A】SPEC_PROCESS 十步中**仅 Step 1** 显式列举 MCP 工具（4 类）+ WebSearch/WebFetch + SearchCodebase | E1 逐字读 `SPEC_PROCESS.md` L21-L114 |
| A-02 | 【A】Step 2 的验证要求是「验证所有文献引用（arXiv 编号、作者、年份）」，**未指定验证器与验证方式** | E1 逐字读 L37-L39 |
| A-03 | 【A】Step 9 写「先写测试（基于 CHECKLIST.md）→ 再写实现」，**未要求测试先失败** | E1 逐字读 L99-L103 |
| A-04 | 【A】Step 3 / 5 / 7 / 10 **无任何工具条款**（模板只约束文档结构） | E1 逐字读 L46-L50 / L63-L67 / L81-L84 / L106-L111 |
| A-05 | 【A】本机外部 MCP server 实为 5 个：english-search / paper-search / research-tools / scholar-mirror / stackexchange | E1 机械枚举 `~/.trae-cn/mcps/**/SERVER_METADATA.json` |
| A-06 | 【A】本机本地 skill 213 个 + 内置 skill 2 个 | E1 机械计数 `~/.trae-cn/skills` 与 `builtin_skills` |
| A-07 | 【A】`mcp_scholar-mirror_list_sources` 实调成功，返回 9 个 Google Scholar 镜像 + Semantic Scholar API | E1 实调返回 |
| A-08 | 【A】`mcp_paper-search_search_papers`（arxiv/semantic/openalex）返回 arxiv 4 条、semantic 0 条、openalex 0 条 | E1 实调返回 |
| A-09 | 【A】`mcp_english-search` 的 `search_web` 与 `search_academic` 两次调用均返回 404 | E1 实调返回 |
| A-10 | 【A】`dc_validator` 现有 selftest 39 个 fixture（F1-F33，含 F3b/F3c/F8b/F11b/F11c 等扩展编号），M6 的 F27-F33 为「先 fixture 后实现」 | E1 实跑 `--selftest` + 读 `scripts/dc_validator.py` |
| A-11 | 【A】本仓已有断言分级 A/B/C + E1-E5，E1 = 逐字读原件 | E1 读 `docs/ASSERTION_EVIDENCE_FRAMEWORK.md` |
| A-12 | 【A】`hook-surface` RESEARCH v1.1 的 P2-1 记录：引证含来源中没有的杂词「MySQL」 | E1 读 `spec/hook-surface/RESEARCH.md` L19 |
| A-13 | 【A】SkillsBench（arXiv:2602.12670）：策展 skill 使通过率 33.9%→50.5%（+16.6pp，25.5% 归一化）；≤3 模块的聚焦 skill 优于更大 bundles | **E1 T1 原文**：arXiv 摘要 + HTML |
| A-14 | 【A】TDAD（arXiv:2603.17973）：SWE-bench Verified 回归率 6.08%→1.82%（-70%）；**prompt-only（无定向测试上下文）回归率 9.94%，高于无干预基线** | **E1 T1 原文**：arXiv HTML |
| A-15 | 【A】RAG-MCP（arXiv:2505.03275）：工具选择准确率 **13.62% 基线 → 43.13%**（more than triples）；prompt tokens 降低 >50%；工具数量增长致选择质量下降 | **E1 T1 原文**：arXiv 摘要 + HTML §1/§3 |
| A-16 | 【A】外部检索的**唯一硬约束在 Step 1**（≥2 独立来源且 ≥1 T1）；Step 3 契约为「无（纯文档）；需外部事实时回 Step 1」；Step 4/5/7/8/9/10 无外部检索条款 | E1 逐字读 `SPEC_PROCESS.md` §Step 工具与提示词契约表（L128-L139） |
| A-17 | 【A】多方案裁决七维取证**已存在**：`SPEC_PROCESS` 规定 Type-1（不可逆）⇒ 全维度取证（决策矩阵）；模板七维逐行固定 = 成本 / 收益 / 可维护性 / 兼容 / 升级潜力 / 短期 / 长期，每格要求证据等级 + 读数日期 | E1 读 `SPEC_PROCESS.md` L453-L458 + `spec/templates/DECISION_MATRIX_TEMPLATE.md` L34-L42 |
| A-18 | 【A】矩阵模板自陈「无门禁、无校验器」；可机械化仅四项形态（格齐全 / 证据等级非空 / 触发条件存在 / 引用完整），结论正确性显式留给人工 | E1 读 `spec/templates/DECISION_MATRIX_TEMPLATE.md` L80-L83 |
| A-19 | 【A】矩阵实际使用仅 **3 处**，全部在 `spec/project-console/RESEARCH.md`（§7.26 件② 目标路径 / §7.27 派生态启用 / §7.28 `§` 编号空间收口）；`DESIGN_TEMPLATE §11.2` 只引不复制 | E1 grep `决策矩阵\|DECISION_MATRIX`（`spec/` 全量） |
| A-20 | 【A】Review 面只有间接约束：Step 4 要求「设计基于已验证的调研结论」，但不要求外部锚点或其证据等级；Step 6 仅核「依赖版本真实存在」 | E1 读 `SPEC_PROCESS.md` L305-L329 |
| A-21 | 【A】GitHub Spec Kit：五入口 `constitution → specify → plan → tasks → implement`，明说「independent entry points, not mandatory phases」；补强面 = Extension / Extension hook（命令前后）/ Preset / Workflow + overlay + step / Bundle / Catalog | **T1 回原文**：<https://github.com/github/spec-kit> |
| A-22 | 【A】OpenSpec：变更包 `explore → propose → apply → archive`；`propose` 产出 proposal.md + specs/ + design.md + tasks.md；纯 Markdown + WHEN/THEN 场景；「review the plan before any code is written」；archive 时更新 specs | **T1 回原文**：<https://github.com/Fission-AI/OpenSpec> |
| A-23 | 【A】BMAD-METHOD：交付环 Clarify → Plan → Build and verify → Learn and adjust；「Right-sized process」小改动直达 build；多视角角色 + durable context | **T1 回原文**：<https://github.com/bmad-code-org/BMAD-METHOD> |

## 附录 B. B 推断类断言清单（9 条）

```json
[
  {"id": "B1", "claim": "十步中七步的工具/提示词契约缺位，同一步不同批次可做法完全不同且无记录", "basis": "A-01~A-04"},
  {"id": "B2", "claim": "本仓不缺原则（证据分级/TDD/独立审查），缺的是「哪一步用哪个通道、拿到什么形态证据」的连接件", "basis": "A-10, A-11, A-12"},
  {"id": "B3", "claim": "「执行阶段要求 TDD」若只写成一句提示词，不仅退化为表演，还可能提高回归率；起作用的是可执行的失败测试（fixture）", "basis": "A-14, A-10"},
  {"id": "B4", "claim": "「设计阶段约束 taste」不能落成勾选项，只能落成「被拒绝的替代方案 + 判据维度 + 代价」", "basis": "§4.5（T2 读数）"},
  {"id": "B5", "claim": "B 档（单节文档 + 最小绑定）是唯一性价比合理档；C 档（全编排）与 ADR-0010 Q3 冲突", "basis": "A-05, A-06, A-13, A-15"},
  {"id": "B6", "claim": "学术推理八条已独立成文（ACADEMIC_REASONING_CONSTRAINTS v1.0）；SPEC_PROCESS / RESEARCH 只留指针", "basis": "B2, P-116"},
  {"id": "B7", "claim": "外部锚点的必要性应随断言类型与不确定性触发（A 类外事实需 T1；纯本仓事实 E1 足够），不应按阶段一刀切要求检索", "basis": "A-16, A-20"},
  {"id": "B8", "claim": "七维决策矩阵的缺口不是「未提及」而是「不可判」：触发判据自陈 + 维度无操作化定义 + 无门禁 ⇒ 易退化为填格表演", "basis": "A-17, A-18, A-19"},
  {"id": "B9", "claim": "阶段映射的正确补强对象是「产物契约 + 门位点」而非阶段数量：三个社区项目都不靠增加阶段，而靠每阶段产出什么与在哪里拦", "basis": "A-21, A-22, A-23"}
]
```

## 附录 C. 假设区（4 条）

| 编号 | 假设 | 未验证点 |
|---|---|---|
| H1 | [H1] 把「来源分层 + 降级链」写进流程后，实际调研会减少「单源当共识」类缺陷 | 无前后对照样本；需下一批真实调研做 A/B |
| H2 | [H2] 每步 ≤2 个工具的绑定不会造成工具选择退化 | RAG-MCP 的 stress test 只证明「工具数量增长会降质」，未测「≤2」在本机的最优性；本机无对照样本 |
| H3 | [H3] skill 名放附录 / 执行卡即可避免「环境漂移进正文」 | 尚未出现「附录里的 skill 失效」实例 |
| H4 | [H4] 学术域八条约束与本仓 A/B/C 分级、E1-E5 口径不冲突 | 需在学术批首轮实际套用一次 |

---

**Review 签字**: _________ 日期: _________
