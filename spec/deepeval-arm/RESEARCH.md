---
id: deepeval-arm-RESEARCH
type: design
version: 1.1
status: in-review
date: 2026-09-10
depends: [promptfoo-m7-eval-IMPLEMENTATION, community-ecosystem-RESEARCH, ADR-0010]
upstream: null
---

# 调研文档：DeepEval 臂实施可行性——吃狗粮评估（P-037）

> **Feature**: DeepEval 评测臂（CER §3.2 C-04 候选，M7 评测矩阵 pytest-native 第二臂的补全评估）
> **创建日期**: 2026-09-10
> **状态**: in-review（审查中）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「DeepEval 臂 是否已经评估过实施可行性 检查一下」→ 检查发现仅浅层候选定位（15.6k 星快照，无本机实测/版本核验/三问门禁）→ 用户指令「对它做吃狗粮评估」
> **参考先例**: P-036 promptfoo-first-run（懒加载分析）、P-030 hook 面评估、P-031~P-034 ARC 四批（arc-probe）、P-035 ARC 升级实施
> **实施批指针（2026-09-10，P-038）**: 本 RESEARCH 三问判定「触发 = 评测样本库就绪 / 用户指定首用例」——本次用户已明确指令升级实施，触发满足；设计与实施文档见 [DEEPEVAL_M7_EVAL_DESIGN.md](./DEEPEVAL_M7_EVAL_DESIGN.md) / [DEEPEVAL_M7_EVAL_IMPLEMENTATION.md](./DEEPEVAL_M7_EVAL_IMPLEMENTATION.md) / [DEEPEVAL_M7_EVAL_CHECKLIST.md](./DEEPEVAL_M7_EVAL_CHECKLIST.md)。
> **v1.1 变更（升级价值分析轮，用户指令「DeepEval 臂升级价值是什么 需要在 research 文档内补充」）**: 新增 **§4 升级价值分析**（§4.1 价值锚点 = 补 promptfoo 声明式断言覆盖不到的「事实忠实」盲区 / §4.2 三重增量价值 = ①事实忠实定量化（FaithfulnessMetric 量化幻觉）②可解释审计（reason 即证据锚点）③判据可塑形（GEval 编码本仓纪律）/ §4.3 价值边界），**注重编号**：原 §4 三问→§5、原 §5 分层→§6、原 §6 文献→§7；断言 **B 1→2**（+B2 价值成立推断）+ **C 2→3**（+C-3 价值成立判定）。A 6 不变、H 0 不变。**声明计数 6/2/3/0**。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 6 | A-1 版本/ A-2 安装/ A-3 命令面/ A-4 端点兼容/ A-5 端到端闭环/ A-6 模型空输出（2026-09-10 本机实测 + 官方文档） |
| B 推断类 | 2 | B1 集成边界 + B2 升级价值成立（§4） |
| C 判断类 | 3 | §5 C-1 资质达标 + C-2 止于懒加载 gate + C-3 升级价值已成立（§4.1） |
| 假设区 | 0 | 无待触发假设（本批吃狗粮实测已覆盖，无需歧义假设） |

## 1. 调研目标

**核心问题**:
1. DeepEval 臂是否具备实施资质？（对照 ARC P-035 先例：本机实测 + 版本核验 + 端点兼容 + 三问门禁）
2. DeepEval v4.x 与主控站 LM Studio（OpenAI 兼容端点）实际连通性与评测效果？
3. 与本仓既有 P-010 pf_m7_eval.py 的集成边界——"第二臂"概念在实现层是否有预留？
4. ADR-0010 三问懒加载 gate 的判定走向——实施 or 止于调研？

## 2. 调研方法与实测取证

### 2.1 版本快照核验（A-1）

【A】A-1: **DeepEval 已演进至 v4.2.2**（本机 `--version` 实测，2026-09-10）——颠覆 CER §3.2 C-04 快照所据的 v1.x 时代认知（15.6k 星 2026-05 快照）。GitHub confident-ai/deepeval：9483 commits、活跃（latest commit 2026-05-26），Apache-2.0。**v4 重大演进** = 本地 runner（`deepeval test run` 本地评测 harness）+ terminal trace inspector（`deepeval inspect` TUI）+ 50+ research-backed 指标 + 多模态默认 + OTel 导出。【来源：https://github.com/confident-ai/deepeval ; https://deepeval.com/docs/introduction】

### 2.2 本机安装与命令面（A-2/A-3）

【A】A-2: **本机安装成功**：Python 3.11.16 临时 venv `pip install deepeval` → v4.2.2，无版本冲突。
【A】A-3: **CLI 命令面可用**（`deepeval --help` 实测）：`generate`（合成 goldens）/ `inspect`（TUI trace）/ `diagnose`（配置诊断）/ `login`/`logout`/`gate`（治理检查）/ `test run`（pytest 集合）。`deepeval diagnose` 明确输出 **5 级配置解析优先级**（process env → .env.local → .env → .deepeval keystore → builtin defaults），与本仓「注入 env → 调用」的 P-010 模式兼容。

### 2.3 端点兼容与端到端评测（A-4/A-5，核心）

【A】A-4: **OpenAIModel 直连 LM Studio OpenAI 兼容端点可行**：`OpenAIModel(model=..., base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")` 无需任何配置形态改动——与 P-010 双臂模式（env 注入端点）同构，不违反零依赖不变式（评测横）。

【A】A-5: **端到端评测闭环（本机实测）**——`GET /v1/models` 指出主控站已加载 8 模型（qwen3.8-27b-uncensored / openai/gpt-oss-20b / qwen2.5-7b-instruct / qwen3.6-35b-a3b 系列 / qwen/coder / nomic-embed）。用 qwen2.5-7b-instruct 跑 CER 真实语料：
- **FaithfulnessMetric** = **1.00 pass=True**（reason 正常："no contradictions present"）
- **GEval**（Correctness 自定义判据）= **1.00 pass=True**（reason：中文「回答准确地涵盖了...每一句都能在上下文中找到依据」）
→ **LLM-as-judge 双指标端到端通过，中文语料支持良好。**

### 2.4 实测发现的关键问题（A-6，端点层注意项）

【A】A-6: **用户指定的 `qwen3.8-27b-uncensored-hauhaucs-aggressive-mtp@iq4_xs` 模型生成空输出**（裸 POST /v1/chat/completions 返回空 reply，latency 9.4s）；换 `qwen2.5-7b-instruct` 后正常（12.7s 返回 "OK"）。→ **模型生成异常系端点侧问题**（uncensored-aggressive 变体输出被自身生成逻辑抑制），**非 deepeval 兼容问题**——登记为 endpoint 层注意项（评估部署前须验证目标模型能产出非空 completion）。

### 2.5 与 P-010 的集成边界（关键认知修正）

| 维度 | P-010（promptfoo） | DeepEval 臂（本批） | 关系 |
|------|-------------------|---------------------|------|
| 评测形态 | CLI 声明式 config（YAML providers） | Python pytest-native（代码内 metric） | 互补 |
| "第二臂"含义 | **promptfoo 内部 base/cross-model 双 provider**（同基座对比） | CER 调研层设想的 M7 评测矩阵 pytest 臂 | **概念不对应** |
| 实现层预留 | P-010 DESIGN/IMPL **从未提及 DeepEval** | 无契约、无 hook、无脚本位点 | **需新契约**（若实施） |
| 端点 | promptfoo env 注入双臂 | OpenAIModel(base_url) | 同端点惯用 |

> **结论（B1）**: CER §3.2 C-04 的"第二臂"是**调研层概念**，P-010 实现层的"双臂"是**promptfoo 内部双 provider**——两者**不指同一物**。若 DeepEval 臂要落地，不是"复用 P-010 双臂预留"，而是**新增独立评测位点**（新脚本/新契约），与 pf_m7_eval.py 正交。

## 3. 适配性判断（对照 ARC P-035 先例资质清单）

| 资质维度 | ARC（P-035 已实施） | **DeepEval 臂（本批）** | 是否达标 |
|---------|---------------------|------------------------|---------|
| 本机实装/命令面 | ✅ | ✅ v4.2.2 实测 | **达标** |
| 版本快照核验 | ✅ v0.8.0 sha256 | ✅ v4.2.2（且纠正 CER 过时快照） | **达标** |
| 端点/OAI 兼容实测 | n/a | ✅ OpenAIModel 直连 LM Studio 端到端通过 | **达标** |
| 独立调研文档 | ✅ arc-probe/ | ✅ 本批 spec/deepeval-arm/ | **达标** |
| ADR-0010 三问 | ✅ | §5（下表） | 见 §5 |
| 与既有工具重叠 | 与 step-gate 正交 | **与 promptfoo 互补（pytest-native vs CLI 声明式），与已有 mcp_paper-search 无重叠** | 无重叠 |

## 4. 升级价值分析（v1.1 新增：本批实测支撑的「为何值得升级」论证）

> **定位**: §3 回答「能不能升」（资质达标），§5 回答「何时能升」（触发条件），本节回答**「为何值得升」**——价值独立于触发条件：价值已成立（基于 A-5 端到端实测），只是触发尚未满足。价值与 §3/§5 是正交维度，不因"止于懒加载"而贬损价值。

### 4.1 价值锚点：补 promptfoo 的「事实忠实」评测盲区

本仓 M7 = **反幻觉证据账本**，其评测对象的本质是「**LLM 生成断言/决策的可信度**」。两条评测臂能力分工：

| 评测臂 | 形态 | 回答的问题 | 覆盖维度 |
|--------|------|-----------|---------|
| promptfoo（P-010） | CLI 声明式断言（expected vs actual） | 「输出**是否等于/匹配**预期」 | **一致性**（deterministic 比较） |
| **DeepEval 臂（本批）** | pytest-native LLM-as-judge 语义指标 | 「输出**是否忠实于源/是否自洽**」 | **忠实性**（faithfulness/hallucination） |

→ **DeepEval 补的是 promptfoo 声明式断言覆盖不到的盲区**：声明式只能判"对没对"，判不了"**是不是编的**"。faithfulness/hallucination 指标直接量化「LLM 生成断言相对其检索上下文是否引入来源外信息」——这与本仓 A 类断言「每条附 E1 取证（断言必须可溯源）」的方法论**同构**，是把反幻觉纪律从「文档层声明」推进到「**生成内容机械可评测**」的天然工具。

### 4.2 三重增量价值（基于 A-5 本机实测支持）

**① 事实忠实定量化**（收益 = 反幻觉核心强化的量尺）：`FaithfulnessMetric` 输出 0-1 分数 + 判据，本机实测得 **1.00** + reason「no contradictions present」——**将"LLM 输出是否幻觉"从人工判断变成可复现的量化信号**，与本仓 A/B/C 断言分级 + M7 形态 II 复发跟踪形成互补证据源。

**② 可解释审计（reason 即证据锚点）**（收益 = 证据账本纪律延伸）：DeepEval 每条 judge 产出 `reason`（本机实测 Faithfulness/GEval 均正常输出中英文 reason），**judge 的判断过程可审计、可登记为证据锚点**——符合本仓「证据账本可审」「LLM 自报不可信」纪律，把 LLM-judge 从黑盒打分变成**可追溯事件**（reason 可入 M7 样本行 draft，同 P-010 record 子命令的登记形态）。

**③ 能力可塑形为本仓专用判据**（收益 = 评测正交扩展）：GEval 支持 `criteria` + `evaluation_steps` 自定义判据（本机实测中文判据跑通），可把本仓「断言分级 E1-E4」「声明=重数」等纪律**编码为评测判据**，形成本仓专用 LLM 生成质量门——补 promptfoo 的 llm-rubric 缺失位点（§2.5 确认）。

### 4.3 价值边界（防过度宣称）

- **不替代验证端**：M7 机械对账 / 声明=重数 / step-gate 是**验证纵**（deterministic 门禁），LLM-judge 是**评测横**（语义信号）——两者不混用，LLM-judge 不接任何机械门禁（§5 Q1）。
- **不替代 promptfoo**：声明式一致性 vs 语义忠实性互补，非竞争（§2.5）。
- **价值 ≠ 触发**：本节论证「值得升」，§5 登记「何时升」（评测样本库就绪/用户指定首用例）——价值已成立，触发待样本。

## 5. ADR-0010 三问懒加载 gate 判定

> 候选吸收物 = "DeepEval 评测臂"（M7 评测矩阵 pytest-native 补充；生成端/评测横，非验证端门禁）。

- **Q1 放哪层**：Layer-1（外部 Python 库 + 评测脚本，生成端/评测横）。**不接验证端门禁**（M7 机械对账/声明=重数/step-gate 均与 LLM-judge 无关）——同 P-010 先例（评测横，验证纵）。
- **Q2 激活条件**：**端点就绪 = 已实质满足**（主控站 LM Studio qwen2.5-7b-instruct 端到端通过；规避 qwen3.8-27b-uncensored 空输出 A-6）。但 DeepEval 臂的**评测对象（M7 LLM 生成输出样本库）尚未建立**——pf_m7_eval.py 当前用 promptfoo 对语料断言做评测，DeepEval 臂要评测的"LLM 生成输出"样本集是本仓尚未系统采集的资产。**触发条件 = 评测样本库就绪 或 用户明确指定首用例后实施**。
- **Q3 未激活副作用 = 0**：是。不引入 venv 依赖进仓库（临时 venv 已清理），零 hook/校验器改动，脚本零位点（I-1）。

**判定：可实施（资质全达标），但当前止于懒加载 gate**——非「无法实施」，而是「实施对象（评测样本库）未系统建立 + 用户未指定首用例」，同 P-036 结论「扩展暂时挂起」的形态。登记触发条件激活项。

## 6. 分层结论

- **DeepEval 臂 = Layer-1 候选（生成端/评测横），实施资质已确认**（补全 CER §3.2 C-04 缺失的全部评估维度）。
- **实施前须满足的触发条件**（登记为候选议程）：
  1. 评测样本库（M7 LLM 生成输出）系统建立，或用户指定首个评测用例；
  2. 明确 DeepEval 臂独立契约（新脚本，正交 pf_m7_eval.py，不复用其"双臂"预留）；
  3. 目标模型非空输出验证（规避 A-6 qwen3.8-27b-uncensored 空输出）。
- **本批零工具改动（I-1）**，临时 venv 已清理，工作区无残留依赖。

## 7. 参考文献

- DeepEval GitHub：https://github.com/confident-ai/deepeval
- DeepEval 官方文档/Quickstart：https://deepeval.com/docs/getting-started
- DeepEval 2026 changelog：https://deepeval.com/changelog/changelog-2026
- DeepEval v4 教程（qaskills）：https://qaskills.sh/blog/deepeval-llm-testing-guide
- CER：https://github.com/...（社区生态调研，本仓 spec/community-ecosystem/）

---

## 附录 A：A 类断言明细

- A-1 至 A-6：见 §2 各 `【A】` 行。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "CER §3.2 C-04 的 DeepEval「第二臂」是调研层概念，P-010 实现层的「双臂」是 promptfoo 内部 base/cross-model 双 provider，两者不指同一物；DeepEval 臂落地需新增独立评测位点，与 pf_m7_eval.py 正交", "basis": "A-3/A-4/A-5 + P-010 DESIGN/IMPL 全文检索（零 DeepEval 引用）"},
  {"id": "B2", "inference": "DeepEval 臂升级价值成立且三重：①事實忠实定量化（FaithfulnessMetric 量化 LLM 输出是否幻觉，与 A 类 E1 取证方法论同构）②可解释审计（reason 即证据锚点，符合"LLM 自报不可信"纪律）③判据可塑形（GEval criteria/evaluation_steps 可编码本仓断言分级纪律）——价值独立于触发条件", "basis": "A-5 本机实测（Faithfulness/GEval 1.00 + reason 正常输出）+ §4.1/§4.2 + P-010 盲区分析（llm-rubric 缺失）"}
]
```

## 附录 C：C 类判断复盘

- C-1: DeepEval 臂实施资质达标（对照 ARC P-035 全维度）
- C-2: 但止于懒加载 gate（评测样本库未建立 + 用户未指定首用例），登记触发条件激活项
- C-3: **DeepEval 臂升级价值已成立**——三重增量（§4.1/§4.2）实证支撑，价值独立于触发条件（§4.3），触发满足后即实施该价值

---

**Review 签字**: _________ 日期: _________