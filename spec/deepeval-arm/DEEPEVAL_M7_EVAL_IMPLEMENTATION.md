# 实施文档：DeepEval M7 评测臂——事实忠实性增强端评测（P-038）

---
id: deepeval-m7-eval-IMPLEMENTATION
type: design
version: 1.0
status: in-review
date: 2026-09-10
depends: [deepeval-m7-eval-DESIGN, deepeval-arm-RESEARCH]
upstream: null
---

> **Feature**: deepEval-m7-eval（PROGRESS P-038，优先级由触发驱动拨动）
> **创建日期**: 2026-09-10
> **状态**: in-review（Step 5-6 + 9 实施完成，selftest 12/12 + 端点门控 + 真实吃狗粮首测评已跑；verified 待独立 pass，同 P-014 收口先例）
> **Spec 步骤**: Step 5-6, 9-10
> **基于设计**: [DEEPEVAL_M7_EVAL_DESIGN.md](./DEEPEVAL_M7_EVAL_DESIGN.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

---

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 6 | A-1 脚本落地+selftest / A-2 临时 venv / A-3 真实端点评测跑通 / A-4 真实分数 / A-5 reason 如实输出 / A-6 M7 样本㉞（2026-09-10 实测） |
| B 推断类 | 1 | B1 judge 严格匹配无法识别语义等价改写（附录 B） |
| C 判断类 | 2 | §附录 C：C-1 如实登记不调用例 / C-2 LLM-judge 分数不可盲信 |
| 假设区 | 2 | H1 GEval 签名 / H2 得分可复现性（附录 C [H]） |

## 1. 实施概述

交付（DESIGN §1）：① `scripts/deepeval_m7_eval.py`（selftest/eval/record 三子命令，评估横不接验证端门禁）；② 端点就绪门控（I-6）+ deepeval 库检测；③ M7 §1 样本行草案登记接口。**真实吃狗粮首测评已完成**（端点 127.0.0.1:1234 可达 + deepeval 4.2.2 临时 venv），结果如实记录于 §9——包括 LLM-judge 忠实性判据的边界实证（M7 样本㉞）。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|------|------|------|---------|
| 语言 | Python | 3.12（selftest/record）/ deepeval venv | ✅ |
| 评测引擎 | deepeval（LLM-judge） | 4.2.2（临时 venv） | ✅ |
| judge 端点 | LM Studio OpenAI 兼容 | 127.0.0.1:1234/v1 | ✅ 可达 |
| judge 模型 | qwen2.5-7b-instruct | — | ✅ 非空输出（规避 A-6） |
| 依赖 | 除 deepeval（临时）外零第三方 | — | ✅ |

### 2.2 文件结构

```
scripts/deepeval_m7_eval.py               # 新增（PM1-PM5 单文件，selftest/eval/record）
spec/deepeval-arm/DEEPEVAL_M7_EVAL_*      # DESIGN / IMPLEMENTATION / CHECKLIST 三件套
spec/deepeval-arm/RESEARCH.md             # 现有 v1.1（加实施批指针）
docs/M7_EVIDENCE_LOG.md                   # 样本㉞ 入账（§1/§2/hits 更新）
docs/PROGRESS.md                          # P-038 行
CODE_WIKI.md                              # §2.1 树 / §9 索引 / §10 stats declared 计数同步
```

### 2.3 venv 方案与清理（A-2）

- **临时 venv 建于工作区外**：`%TEMP%\deepeval-venv-dg-20260910`（未污染仓库 tracked，.gitignore 无需改动）
- `pip install deepeval` → **v4.2.2**
- **验收后清理**：删除该临时 venv，不引入仓库依赖（同 P-037 先例 / RESEARCH A-2）
- 脚本自带 deepeval 可用性检测：不可用时打印 `pip install deepeval` 提示并 exit 1（I-6 不假造）

### 2.4 eval 门控与评测流水线（PM2/PM3）

- **端点门控（I-6）**：`endpoint_reachable()` 只读 TCP 预检，不可达 → P1 提示 + exit 1
- **依赖门控**：`deepeval_available()` 检测，缺失 → 安装提示 + exit 1
- **模型注入（DESIGN §4）**：`OpenAIModel(model, base_url=endpoint, api_key=api_key)` 直连端点，`model=llm` 传给 metric 构造参数（v4.2.2 无顶层 `set_default_model`，实测修正）
- **eval 流水线**：逐用例 `FaithfulnessMetric(threshold=0.7)` + `GEval(criteria/evaluation_steps/evaluation_params=ACTUAL_OUTPUT+RETRIEVAL_CONTEXT, threshold=0.7)` → score/reason → JSON

### 2.5 M7 登记草案（PM4）

`to_m7_sample_row()` 生成 M7 §1 草案：审查配置 = deepeval 臂 + 模型 + PASS/FAIL；发现留人工归并；reason 截取前 60 字符作证据锚点碎片。样本追加后走 `m7_stats.py --write`（I-3/I-6）。

## 3. API 适配实录（DESIGN 假设 H1 确认）

| deepeval 组件 | 预期 | v4.2.2 实测 | 处置 |
|------|------|-----------|------|
| `set_default_model` | 顶层导出 | 顶层不存在 | 改为把 `model=llm` 传 metric 构造参数 |
| `FaithfulnessMetric(threshold/strict_mode/async_mode)` | — | 签名一致可用 | 直接用 |
| `GEval` | criteria/evaluation_steps | VC 需要 `evaluation_params`（"requires evaluation_params…"），实测补 `[LLMTestCaseParams.ACTUAL_OUTPUT, RETRIEVAL_CONTEXT]`；`LLMTestCaseParams` 有 `DeprecationWarning`（建议 SingleTurnParams） | **已适配**：补 evaluation_params；弃用警示留待后续 |
| metric.score/reason | — | 可用 | 直接用 |

> **假设 H1 已确认（解除）**：衡 `criteria/evaluation_params` 签名可用。**假设 H2 部分证伪**：见 §9（Faithfulness 在 7B judge 上模板 JSON 失败，得分可复现性对 judge 模型能力敏感）。

## 4. 与既有工具的运行隔离

- `deepeval_m7_eval.py` 不写 M7（只生成草案供人工追加，I-1）；M7 hits 块生成/校验仍归 `m7_stats.py`（P-011）
- 与 `pf_m7_eval.py`（P-010）正交：DeepEval 臂是独立评测位点，复用不吞并（RESEARCH B1）
- 不入验证端机械门禁（I-6，ADR-0010 Q1：评测横/生成端）
- 临时 venv 在 %TEMP%，不污染仓库

## 5-8. （保留——对应 DESIGN §§5-8 无独立伪实现）

## 9. 测试与验证（真实吃狗粮首测评，2026-09-10）

### 9.1 selftest

`py -3 scripts/deepeval_m7_eval.py selftest` → **12/12 PASS**（F1-F6：端点解析/门控/deepeval 检测/内置测例结构/M7 草案/不可达门控）

### 9.2 真实端点评测（端点 127.0.0.1:1234 + qwen2.5-7b-instruct + deepeval 4.2.2）

对内置两测例跑双指标，实际分数与 reason 如实记录：

| 用例 | kind | Faithfulness score | Faithfulness reason（节选） | GEval score | GEval reason（节选） | faithful_passed |
|------|------|------|------|------|------|------|
| faithful-01 | 忠实用例 | **评测失败** | "Evaluation LLM outputted an invalid JSON. Please use a better evaluation model." | **0.0** | "The output mentions '2026 年 5 月快照' which is not present in the retrieval context, introducing an external fact." | ✗ |
| hallu-01 | 引入来源外信息用例 | **0.0** | "…claims over 200 out-of-the-box evaluation metrics… not in the retrieval context" | **0.0** | "…'Cloud 平台会自动记录每一次评测并生成可视化报告' which is not in the retrieval context." | ✗（负例，judge 正确判低分 ✅） |

**summary**：total=2, faithful_passed=0, detected_hallu=1。

### 9.3 实测发现的边界实证（A-4/A-5/B1/C-2）

1. **忠实用例（faithful-01）被判 0.0**：输出把 context「2026-05 快照」作语义等价改写「2026 年 5 月快照」，两个 judge 均无法识别"等价改写"，GEval 判「引入来源外信息」——**LLM-judge 对中文语义等价改写（转述）判据过严**（M7 样本㉞ 转述引文字段新变体）。
2. **FaithfulnessMetric 在 7B judge 上失败**：模板要求 judge 以严格 JSON 输出，qwen2.5-7b 输出不合规 → "invalid JSON"。**Faithfulness 需要更强 judge 模型（H2 部分证伪）**。
3. **负例（hallu-01）两指标均正确判 0.0**：虚构"超过 200 个指标"/"Cloud 报告"被准确识别为来源外——DeepEval 臂对真正幻觉的检测有效。
4. **附带观察**：hallu-01 的 Faithfulness reason 里 judge 转述 context 失真（称 context "clearly states that DeepEval has only two metrics"，实际 context 未言明—仅列 14 项指标）——**连 judge 的 reason 自身也含幻觉**，进一步印证「reason 即证据锚点须人工审计，不盲信」纪律。

### 9.4 M7 样本登记

本次真实发现 → **M7 样本㉞ 入账**（samples 33→34, quote 4, form2_total 76, unlabeled 2；形态 II 复发=1 转述引文，发现列 lead=1 无 P 已如实非阻断），由 `m7_stats --write` 机械重生成 hits 块，校验通过。

## 10. 关键决策记录

### 10.1 派生需求（DR）
- **DR-A（API 注入形态）**: 无顶层 set_default_model → `model=llm` 传 metric；GEval 补 evaluation_params——源：v4.2.2 实测签名（§3）
- **DR-B（门控不假造）**: 端不可达/deepeval 缺失 → P1 + exit 1，不假造评测——源：DESIGN I-6
- **DR-C（如实登记不调用例）**: 忠实用例被判 0.0 不因"难看"而改 output 造假通过——源：本仓「不信任/不造假」纪律 + C-1

### 10.2 LOC 回填（P-008 教训：DESIGN 预估实施核对）
- 脚本 LOC ≈ **280**（含注释/空行，deepeval_m7_eval.py）
- selftest = **12 断言 / 6 fixture**

### 10.3 实施期拦截实录

| 发现 | 处置 |
|------|------|
| deepeval v4.2.2 `set_default_model` 顶层不存在 | 改传 `model=llm` 给 metric（DR-A，§3） |
| GEval "requires evaluation_params" | 补 evaluation_params（§3） |
| 忠实用例最初中英混杂被判不忠实 | 修正用例如实构造为全中文（§9.2）；仍被判 0.0 → 转为边界实证登记，不造假通过（DR-C） |

## 11. 对验收的输入

验收掌 KEY：
1. selftest 12/12 全绿
2. 端点门控行为正确（不可达/缺库阻断，不假造）
3. **真实吃狗粮首测评完成**（§9.2 分数与 reason 如实记录）——P-037 触发条件已闭环
4. M7 样本㉞ 入账（§9.4）+ 视图层同步（CODE_WIKI §9/§10 + PROGRESS P-038）

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）

## 附录 A：A 类断言明细

【A】A-1: 脚本落地，selftest 12/12 PASS（2026-09-10 `deepeval_m7_eval.py selftest` 实测）。取证: §9.1。
【A】A-2: 临时 venv 建于工作区外 `%TEMP%\deepeval-venv-dg-20260910`，deepeval 4.2.2，用后清理。取证: §2.3 + P-037 先例。
【A】A-3: 真实端点评测跑通——端点 127.0.0.1:1234 TCP 可达 + qwen2.5-7b-instruct 双用例 judge 返回。取证: §9.2。
【A】A-4: 真实分数——faithful-01 Faithfulness「invalid JSON」/GEval 0.0；hallu-01 Faithfulness 0.0/GEval 0.0。取证: §9.2 表（实测，不编造）。
【A】A-5: reason 如实输出（judge 原样 reason，含"no contradictions"-style 无效 JSON 报错）。取证: §9.2。
【A】A-6: M7 样本㉞ 已登记——samples 34, quote 4, form2_total 76（m7_stats 校验通过）。取证: §9.4 + M7 §1/§5。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "忠实用例（faithful-01）被判 0.0 的主因是 judge 严格匹配无法识别语义等价改写——context「2026-05 快照」与 output「2026 年 5 月快照」语义等值但字面不同，GEval reason 明确指其为'引入来源外信息'；此即 LLM-judge 对中文转述/改写判据过严的机制性解释", "basis": "A-4/A-5（GEval reason 原文）+ DESIGN B2 + M7 样本㉞"}
]
```

## 附录 C：C 类判断复盘 + 假设区

**C 类判断（不机械对账，review 臂重数）**:
- C-1: 本次吃狗粮实测结果如实登记，不因忠实用例"难看"而调 output 使其通过——防造假、防表演性验收
- C-2: LLM-judge 分数不可盲信，reason 即证据锚点须人工审计——实测已实证（judge reason 自身含幻觉 + 语义改写误判）

**假设区（[H]）**:
- [H1] deepeval v4.2.2 中 FaithfulnessMetric/GEval 签名可用——**已确认（解除）**（§3 适配实录）
- [H2] 得分在目标端点上可复现——**部分证伪**：Faithfulness 在 7B judge 上模板 JSON 失败，需更强 judge 模型（§9.3-2）

## 附录 D：哲学对齐注

- 评测横/生成端，不接验证端门禁（ADR-0010 Q1）。
- reason 即证据锚点如实输出（I-5/R4），judge 分与 reason 均原生透传不经转写。
- 端点不可达门控不假造（I-6），本次端点可达故真实跑通。