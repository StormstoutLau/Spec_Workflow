---
id: deepseek-harness-RESEARCH
type: design
version: 1.0
status: in-review
date: 2026-08-20
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0005, ADR-0007, DIS-007]
upstream: null
---

# DeepSeek Harness（dsh）调研：机制 / 证据 / 吸收复用裁决 v1.0 (2026-08-20)

> **任务来源**: 用户提问"开源社区有人开发了一种 j space 的 deepseek hardness 插件 可以提升模型表现 深度调研分析 是否可以吸收复用"
> **实体消歧**: "j space 的 deepseek hardness 插件" = **DeepSeek Harness**（CLI 名 `dsh`）——DeepSeek 官方 2026-08-13 开源的 Agent 运行时框架。"hardness" 为 "Harness" 听写变形；"j space" 疑为 "JS/TS space"（TypeScript 生态）口误或纯听岔。**不是第三方插件，是 DeepSeek 官方框架本身**；其上的社区插件生态（ModLens / dsh-web-ui 等）是另一层。
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；WebSearch + WebFetch 双通道取证（2026-08-20）
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 14 | 每条附 URL + 可核对来源（GitHub 官方仓库 / 官方文档 / 官网为主，二手媒体源单独标注）；取证日期 2026-08-20 |
| B 推断类 | 3 | B1-B3，登记于附录 B |
| C 判断类 | 3 | §4 吸收裁决 2 条 + §5 风险判断 1 条 |
| 假设区 | 4 | H1-H4，未取证声明 |

> **计数说明（R7 机械重数）**: A 类 14 条（行首 `【A】` 标记，`grep -c '【A】'` 重数）、附录 B 3 条（`"id": "B\d+"` 机读块）、C 类 3 条（`【C】` 标记，DR-2 首版不对账）、假设区 4 条（`[H\d+]` 列表项）。**门禁拦截实录（2026-08-20，两跳）**: 初稿自创编号标记 `【A1】`-`【A14】` + 列表式 B/H 附录——dc_validator M5 提交瞬间拦截（"声明 14 实为 0"×3，P1×3）；格式回归 R1 契约后第二跳拦截（"声明 14 实为 12"——5 处标记位于列表项内，RE_A_MARK 仅认行首/表格位），§1 规格列表重组为行首断言段后清零。两次均为**格式契约违规而非形态 II 计数错**（不入 M7 形态 II 分桶）——dc_validator 首次实战拦截"生成端标记格式漂移"，门禁价值实录：生成端（本会话）对契约的记忆漂移在提交瞬间被机械纠正。

## 1. 实体定位：它是什么，不是什么

三层区分（官方页面自己强调的混淆点）：

1. **chat.deepseek.com** = 网页聊天产品（不是它）
2. **deepseek-v4-pro / flash API** = 模型本身（不是它）
3. **DeepSeek Harness（dsh）** = 模型外层的**运行时**：工具、文件系统、会话、循环、UI——官方分工公式"Agent = Model + Harness"，模型负责想，harness 负责做

【A】发布时点与许可证：2026-08-13 深夜随 V4 Pro 正式版后十余小时开源 v0.1 developer preview，**MIT 协议**；官方 README 明示 "THERE WILL BE COMPATIBILITY-BREAKING CHANGES"（原文大写强调）【来源：S1/S2】

【A】仓库规格：`deepseek-ai/deepseek-harness`——TypeScript 97.1% + Python 0.7%（python/ 目录为一等公民，含 SDK），12,940 commits（2026-08-20 快照），25 contributors，2026-06-10 初始化（内部开发约两个月后开源）。GitHub star 数各源分歧：CSDN 2026-08-19 报"近 40k"；第三方导航站 2026-08-20 快照称 167.3k；36kr 称开源当晚"3 小时破 3 万"——**数字冲突未核实，登记为假设 H1**【来源：S1/S5/S6/S8】

## 2. 事实层：架构与能力（A 类断言）

### 2.1 核心架构

【A】设计原则"**一切皆插件**"（Everything is a Plugin）：模型适配器、工具注册、Session Log、Agent Loop、沙箱、审批策略、UI 全部是插件，通过 Cordis 服务与事件协作，配置层组合，不改源码即可替换任何能力。Cordis 是经 Koishi 机器人生态四年生产验证的插件元框架，其设计有论文《A Programming Paradigm for Spatiotemporal Composability》【A3 来源：github.com/deepseek-ai/deepseek-harness README + deepseek.com/harness/en/】

【A】**Every run is traceable**：模型看到的一切——系统提示词、思维链、工具调用与结果、子代理调度、每次上下文注入——写入**仅追加（append-only）会话日志**；Trajectory 视图按来源检视；resume / fork / search / replay 共享同一事件流【来源：deepseek.com/harness/en/】

【A】四种运行模式：**标准**（全工具）、**PTC**（Programmatic Tool Calling——模型生成 TypeScript 代码编排多轮工具调用，中间数据留在运行环境，只回传最终结果，大幅省 token）、**极简**（仅 bash + str_replace_editor 两工具，专用于模型基准测试——V4 Pro 官方 Agent 基准成绩 DeepSWE 62.7 / Terminal Bench 2.1 87.9 均在极简模式跑出【来源：CSDN 2026-08-19 报道，二手源】）、**创造**（检查运行时、内存中试验插件、Agent 改装自身）【来源：deepseek.com/harness/en/】

### 2.2 Python SDK（对本仓库最关键的能力）

【A】`pip install deepseek-harness-sdk`，**bundled runtime，无需系统 Node.js**；Python 3.10+；核心 API 为 context manager：

```python
from deepseek_harness import DeepSeekHarness
with DeepSeekHarness(provider=..., model=..., cwd=str(workspace),
                     session_root=str(sessions), cordis=str(config)) as harness:
    result = harness.run("...", session_id="example-001")
```

【来源：deepseek-harness.github.io/deepseek-harness/en/guide/python-sdk】

【A】**session 持久化为未压缩 JSONL**，含"assembled model requests and tool calls"（装配后的完整模型请求与工具调用）——即每次运行自动产出可重放的事件流日志【来源：同上】

【A】**session 复用语义**：同一 harness + 同一 session_id 延续会话与持久 Bash 进程（含工作目录、环境变量、shell 函数）；新 session_id = 独立任务【来源：同上】

【A】**平台限制**：Linux x64 / Linux arm64 / macOS 14+ arm64；极简 composition "does not support Windows agents"（持久 PTY 后端需 POSIX 终端基底）——主控站 Win10 不可跑，工作站 A/B（Ubuntu）可跑【来源：同上】

【A】示例 composition 权限为 `danger-full-access`，官方要求只在一次性 checkout 或容器内运行；Bash 与编辑器可改运行时进程可见的任意路径【来源：同上】

### 2.3 模型接入

【A】**OpenAI 兼容端点一等支持**：环境变量 `DEEPSEEK_BASE_URL` 指向 OpenAI 兼容代理即可（SDK 层）；Web UI 层 custom provider 支持 `openai-completions` 协议 + baseURL + `GET /models` 模型发现【来源：python-sdk + providers 官方文档】

【A】模型目录含近 40 种主流模型适配器；DeepSeek 自有 chat-completions 路由是纯文本（不可配置为图像输入）【来源：providers 文档 + 腾讯云开发者社区转述（二手）】

### 2.4 迭代速度与官方工程实践

【A】rc.8（2026-08-19）发布：14 项更新——原生图片请求/图文混合输入、Claude Code 与 Codex 作为 Profile Bundle 接入子代理体系、Windows PTY 持久 PowerShell 会话（Web UI 层）、流式生成/自定义网关修复等【来源：36kr 2026-08-20 智东西报道（二手）】

【A】仓库自身工程实践与本仓库方法论同构：`.claude/` + `AGENTS.md`（CLAUDE.md symlink）存在；提交历史含 "docs: accuracy sweep, architecture restructure, two ADRs, review skill"；`lefthook.yml` git hooks；pytest.ini + vitest 全家桶（e2e/snapshot/stress/perf 五配置）——**DeepSeek 团队自己开发此仓库也用 ADR + 审查技能 + 精度清扫 + git hooks**【来源：GitHub 仓库页文件列表与提交信息，一手】

## 3. 与 Spec_Workflow 的结构映射

五个对应关系（本节为分析框架，具体裁决见 §4）：

| # | dsh 机制 | Spec_Workflow 对应物 | 关系 |
|---|---------|--------------------|------|
| M1 | append-only JSONL session log（每次运行的完整请求/工具调用记录） | RULE-6 取证矩阵 E1-E5 中的 E1（可重放机械证据） | **同构**：都是"不信任 LLM 断言，用机械记录兜底"。dsh 把 E1 证据的生产自动化了 |
| M2 | 极简模式（两工具标准化环境，官方基准在此跑） | M7 对比臂的标准化审查环境（同基座/异基座变量控制） | **同构**：控制变量的最小环境 |
| M3 | session 复用语义（新 session_id = 独立上下文） | RULE-1 Review 时序独立（新上下文审查，禁止同会话既写又审） | **可实现**：新 session_id 物理化"时序独立" |
| M4 | OpenAI 兼容端点 + 40 模型适配器 | RULE-5 异质性约束（审查端异构于生成端）+ LM Studio 本地端点 | **可实现**：LM Studio 端点接入后，审查端/生成端基座自由组合 |
| M5 | DeepSeek 团队自身的 ADR + review skill + accuracy sweep 开发实践 | SPEC_PROCESS + ADR-0004~0009 + 本仓 pre-commit | **互证**：工业一线团队独立演化出同构方法论（外部佐证，非因果） |

M5 值得展开：dsh 仓库的 `.claude/` 提交（"accuracy sweep, two ADRs, review skill"）说明其文档治理与 Spec_Workflow 的"调研→ADR→审查"回路是**趋同演化**——两个独立团队（一个工业一个单人）在 2026 年年中各自得出"LLM 开发必须配机械审查与决策记录"的结论。这不是可吸收的代码，是框架有效性的第三方证据。

## 4. 吸收复用裁决（C 类判断）

【C】**主判断：分层吸收——机制立即吸收，执行环境短期试点，runner 基座中期重裁决，本体不进仓。**

### 层 1 立即吸收（零成本，本调研已执行）

- **M5 互证**入方法论资产：DeepSeek 官方仓库的 ADR/review-skill 实践作为 SPEC_PROCESS 有效性的外部佐证（登记于本调研 + 可被 ADR-0009 有效性重审引用）
- **session log 设计思想**（append-only JSONL、装配级请求记录、resume/fork/replay 共享事件流）作为 P-009 薄壳 runner 的 JSON state 设计参考——**抄设计不抄代码**

### 层 2 短期试点（P-008 执行形态升级，最高 ROI）

P-008（P-007 产出独立 pass）原方案为"真异基座优先"的对话式审查。试点方案：在工作站 A（Ubuntu）用 dsh Python SDK 跑一轮——

- 审查端 = DeepSeek V4 Pro（经 `DEEPSEEK_BASE_URL` 或官方端点），生成端 = GLM-5.3（Trae）→ **真异基座**（RULE-5 满足）
- 新 session_id 一次性审查任务 → **时序独立物理化**（RULE-1 满足）
- 审查者通过 bash/str_replace_editor 工具**自己 grep 仓库验证断言**——审查从"读报告"升为"可动手复核"（M7 样本⑪ 的教训正是"prose 计数必须机械对账"，dsh 审查者可自带机械对账能力）
- JSONL session log → 审查过程本身产出 E1 证据入取证矩阵（RULE-6 满足）
- 产出 = 一份 IMPLEMENTATION/CHECKLIST 独立审查报告 + 一份可重放 JSONL 轨迹

风险对冲：与既有 DeepSeek 网页版直调审查（M7 样本⑥⑦形态）并行跑一次对比，验证 dsh 增量价值（工具调用 + 取证）是否兑现，未兑现则回退对话式审查。

### 层 3 中期重裁决（P-009 方案 B 的实现选择）

LANGGRAPH 调研（P-006）裁决"零框架依赖薄壳 runner（~500-1000 LOC）"。dsh 开源改变了权衡空间，但**不推翻裁决**：

- dsh 不替代方案 B 的核心（`--gate` 门禁命令物理化 RULE-1 仍需自建——dsh 不管流程门禁，它是 agent 运行时不是工作流引擎）
- 改变的是方案 B 内部的 agent 执行层选型：裸 API 调用 vs dsh SDK（后者免费获得工具注册/会话管理/JSONL 日志，即 500-1000 LOC 中的大头）
- **触发条件已满足**（Python SDK 发布 + LM Studio 兼容 + MIT），裁决时机 = P-009 启动时，届时以 H2 实测（工作站 A 可用性 + LM Studio 接入）为输入
- 与 LangGraph 路线的关系不变：dsh 同样是"触发条件后的升级路径候选"，且比 LangGraph 更贴（LangGraph 解决状态图编排，dsh 解决 agent 运行时——runner 需要的是后者）

### 层 4 不吸收（与本仓定位冲突）

- dsh 本体/Web UI/插件生态/创造模式**不进本仓库**——违反"纯文档 + 最小工具层"定位（本仓唯一可执行件 = dc_validator）；runner 归属独立仓库（P-009 既定）
- P-010 promptfoo 对比臂**不受影响**——dsh 是审查执行环境，promptfoo 是评测矩阵，互补不替代

【C】**次判断：dsh 的真实价值排序（对本仓库）= 取证基础设施（M1）> 异构审查执行环境（M3+M4）> runner 基座候选（层 3）> 其他一切。** 社区热炒的"一切皆插件"插件生态（288→800+ 插件）对本仓库无直接价值——那是对话式编码场景的长尾，不是审查场景的需求。

## 5. 风险与限制

【C】**风险判断：主要风险 = 生态早熟依赖。**

- **developer preview + 保证 breaking changes**：SDK API 形态（`DeepSeekHarness` 签名/composition 结构）可能变——层 2 试点用一次性脚本无妨；层 3 若采纳需锁版本 + 隔离 adapter 层
- **平台**：Python SDK 不支持 Windows agents（§2.2 平台限制断言）——主控站（Win10）出局，试点必须落工作站 A/B（Ubuntu AMD 395，三机集群现成）——这恰好复用既有基础设施，但增加跨机工作流摩擦（审查任务需 SSH 到工作站执行）
- **权限**：danger-full-access 是示例默认而非框架缺陷，但要求一次性 checkout/容器隔离纪律（B 站 36kr 转述的沙箱插件可配，未取证）
- **插件生态治理**（HN 社区质疑"社区插件六个月后腐烂"）：与本仓库无关（不进插件生态），不构成风险
- **star 数与热度数据冲突**（H1 假设，见附录 C）：不影响技术裁决，仅登记

## 6. 与在办任务的关系（PROGRESS 联动）

| 任务 | 影响 | 动作 |
|------|------|------|
| P-008 独立 pass | 执行形态多一个选项（层 2 试点） | 本调研登记为选项；是否采纳由执行时裁量（默认仍可走对话式，试点并行） |
| P-009 薄壳 runner | 实现选择重裁决（层 3），触发条件已满足 | P-009 验收标准追加"agent 执行层选型：dsh SDK vs 裸 API，以 H2 实测为输入" |
| P-010 promptfoo | 无影响 | 无 |
| P-011 M7 hits 机读块 | 无影响（dsh JSONL 是另一层取证，不并入 M7 统计） | 无 |
| P-012（本调研） | 新登记 | done（本文档） |

## 7. 开放问题（假设区，未取证）

- [H1] GitHub star 数分歧（40k@CSDN-08-19 vs 167.3k@第三方快照-08-20）— 查证路径: GitHub 页面直核（对结论无影响，纯数据卫生）
- [H2] dsh Python SDK 在工作站 A（Ubuntu + AMD 395）实测可用性 + LM Studio 端点（192.168.1.11/12:1234）经 custom provider 接入 — 查证路径: 工作站 A 装 SDK + `DEEPSEEK_BASE_URL` 指 LM Studio 端点跑 minimal.py（层 2/层 3 前置，验证 B2）
- [H3] dsh 审查者的"工具调用复核"实际增益 vs 纯对话式审查（DeepSeek V4 Pro 网页版直调）— 查证路径: 层 2 试点对比臂实测（同一审查任务双通道跑分）
- [H4] rc.8 的 Windows PTY 改进（Web UI 层）是否延伸到 Python SDK agent 层 — 查证路径: release notes 比对 + 主控站实测（若延伸则工作流摩擦消除）

## 附录 B: 断言登记表（机器可读）

```json
[
  {
    "id": "B1",
    "type": "推断",
    "claim": "dsh JSONL session log 可作 RULE-6 取证矩阵 E1 级证据（日志含 assembled model requests + tool calls，满足 E1 可重放机械证据语义）",
    "basis": "§2.2 JSONL 断言 + 取证矩阵 E1 定义",
    "verified": false
  },
  {
    "id": "B2",
    "type": "推断",
    "claim": "LM Studio 端点可经 OpenAI 兼容机制接入 dsh（DEEPSEEK_BASE_URL / custom provider 协议支持 × LM Studio OpenAI 兼容 API 的组合）",
    "basis": "§2.3 OpenAI 兼容端点断言 + LM Studio 接口事实",
    "verified": false
  },
  {
    "id": "B3",
    "type": "推断",
    "claim": "dsh SDK 可承载 P-008 独立 pass 审查执行（API + session 语义 + 平台三断言组合）",
    "basis": "§2.2 SDK/session/平台断言组合",
    "verified": false,
    "depends_on": "H2"
  }
]
```

## 附录 C：来源清单

| 编号 | 来源 | 类型 | 取证日 |
|------|------|------|--------|
| S1 | github.com/deepseek-ai/deepseek-harness（README + 文件列表 + 提交历史） | 一手 | 2026-08-20 |
| S2 | deepseek.com/harness/en/（官方产品页） | 一手 | 2026-08-20 |
| S3 | deepseek-harness.github.io/deepseek-harness/en/guide/python-sdk | 一手 | 2026-08-20 |
| S4 | deepseek-harness.github.io/deepseek-harness/en/guide/providers | 一手 | 2026-08-20 |
| S5 | CSDN《DeepSeek Harness 开源：一切皆插件、省 Token、Agent 还能改装自己》2026-08-19 | 二手 | 2026-08-20 |
| S6 | 36kr/智东西《昨夜，DeepSeek Harness首发新版本：14项更新》2026-08-20 | 二手 | 2026-08-20 |
| S7 | 腾讯云/阿里云开发者社区插件指南文（二手转载） | 二手 | 2026-08-20 |
| S8 | laojinchuhai.com DeepSeek Harness 导航页（star 快照 167.3k） | 二手 | 2026-08-20 |
