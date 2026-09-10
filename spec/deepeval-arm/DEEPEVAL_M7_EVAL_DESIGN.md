# 设计文档：DeepEval M7 评测臂——事实忠实性增强端评测（P-038）

---
id: deepeval-m7-eval-DESIGN
type: design
version: 1.0
status: draft
date: 2026-09-10
depends: [deepeval-arm-RESEARCH, promptfoo-m7-eval-IMPLEMENTATION, SPEC-PROCESS, FWK-ASSERTION, ADR-0010]
upstream: null
---

> **Feature**: deepEval-m7-eval（PROGRESS P-038，DeepEval 臂升级实施）
> **创建日期**: 2026-09-10
> **状态**: draft（草稿）
> **Spec 步骤**: Step 3-4
> **基于调研**: [DEEPEVAL_ARM_RESEARCH](./RESEARCH.md) v1.1（6A+2B+3C+0H）
> **任务来源**: P-037 三问判定「触发 = 评测样本库就绪 或 用户指定首用例」——本次用户已明确指令升级实施，触发满足，进入实施。
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

---

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 6 | A-1 三子命令 / A-2 双指标+reason / A-3 端点门控 / A-4 reason 锚点键 / A-5 缺库提示 / A-6 临时 venv（可 grep 脚本取证，2026-09-10 实施） |
| B 推断类 | 2 | B1 互补关系 + B2 吃狗粮测例价值落地（附录 B） |
| C 判断类 | 3 | §附录 C：C-1 方案 Z / C-2 不接门禁 / C-3 触发满足 |
| 假设区 | 2 | H1 GEval 签名 / H2 得分可复现性（附录 C [H]） |

## 1. 设计目标

把「LLM 生成断言相对其来源上下文是否忠实」从人工判断升级为 **DeepEval LLM-judge 定量评测 + reason 证据锚点 + M7 样本登记草案**——补 P-010 promptfoo 声明式断言覆盖不到的「事实忠实」盲区（faithfulness/hallucination）。产出三件：

① `scripts/deepeval_m7_eval.py`（selftest/eval/record 三子命令，评估横不接验证端门禁）；
② 端点就绪触发门控（I-6，不可达不假造评测）；
③ M7 §1 样本行草案登记接口（record 子命令，人工确认归类后追加）。

**范围裁决（继承 RESEARCH §5 Q1/Q3）**：Layer-1（外部 Python 库 + 评测脚本，生成端/评测横）；**不接验证端机械门禁**（M7 对账 / 声明=重数 / step-gate 均与 LLM-judge 无关，同 P-010 先例）。deepeval 为临时 venv 依赖（用后清理，不引入仓库依赖，同 RESEARCH A-2/P-037 先例）。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| 触发条件已满足（P-037 Q2：端点已就绪 + 用户指定首用例） | 进入实施宝，交付可真实运行的评测助手 | RESEARCH §5 |
| OpenAIModel(base_url=127.0.0.1:1234/v1) 直连 LM Studio 端到端通过 | eval 子命令默认端点指向主控站 | RESEARCH A-4/A-5 |
| FaithfulnessMetric/GEval 双指标中文 reason 正常输出 | 双指标并行评测，reason 即证据锚点 | RESEARCH A-5/§4.2② |
| reason 可入 M7 样本行 draft（同 P-010 record 形态） | record 子命令生成 M7 §1 草案 | RESEARCH §4.2② |
| qwen3.8-27b-uncensored 生成空输出（A-6） | 默认模型用 qwen2.5-7b-instruct；模型可配 | RESEARCH A-6 |
| DeepEval 臂与 P-010 互补、正交（P-037 B1） | 新脚本/新契约，复用不吞并 | RESEARCH §2.5/B1 |

### 2.2 相关 ADR / 规范

| 文档 | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [ADR-0010 Q1](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | Layer-1 补全，不接验证端门禁 | 评测横；默认只读（I-1） |
| [FWK-ASSERTION R7](../../docs/ASSERTION_EVIDENCE_FRAMEWORK.md) | 声明 = 机械重数 | 评测结果登记须机械解析 JSON，reason 经 judge 如实输出不经转写 |
| [promptfoo-m7-eval-IMPLEMENTATION](../promptfoo-m7-eval/PROMPTFOO_M7_EVAL_IMPLEMENTATION.md) | record 结构性 + I-6 门控 + I-4 机械解析先例 | 脚本结构与不变式同构复用 |

### 2.3 职责边界

**职责内（本设计回答）**
1. `deepeval_m7_eval.py` 三子命令（selftest / eval / record）
2. eval 门控：端点 TCP 预检 + deepeval 库检测，不可用即如实提示（不假造）
3. 评测用例构造：内置吃狗粮两测例（忠实用例 + 引入来源外信息用例）或 `--cases` 自定义
4. 双指标评测：FaithfulnessMetric + GEval，输出 0-1 分数 + reason，落 JSON
5. record：eval 结果 JSON → M7 §1 样本行草案（reason 作证据锚点碎片）

**职责外（不回答——独立职责，不吞并）**
- **样本行的语义归类判断**（发现字段的 P 分级、形态 II 与否）——人工 + 既有 m7_stats 对账职责（m7-hits-block 边界）
- M7 hits 块生成/校验——已有 m7_stats（P-011），本脚本不重复
- 验证端机械门禁——不接（I-6 只做评测门控，不入验证流水线）
- 视图层同步（CODE_WIKI/repo_stats/progress）——P-038 收束批人工同步后由 repo_stats 校验

**能力边界（回答不了——如实声明）**
- deepeval v4.2.2 中 GEval 的 criteria/evaluation_steps 签名可用性（假设 H1）——实施时实测确认
- 评测得分的跨模型/跨端点可复现性（假设 H2）——judge 为 LLM，得分是语义信号，非机械闸值（R4 语义）

## 3. 架构设计

### 3.1 整体架构

```
[端点就绪触发]（127.0.0.1:1234 TCP 可达 + deepeval 库已装）
    │
    ▼
eval: python scripts/deepeval_m7_eval.py eval [--cases json] [--endpoint ...]
    │  内部: endpoint_reachable 门控 → deepeval_available 检测 → 注入 OpenAIModel
    │        → 对命例跑 FaithfulnessMetric + GEval → score + reason → JSON
    ▼
结果 JSON（faithfulness_score / faithfulness_reason / geval_score / geval_reason）
    │
    ▼
record: python scripts/deepeval_m7_eval.py record --results <json>
    │  机械解析 → M7 §1 样本行草案（reason 作证据锚点碎片）
    ▼
[人工确认归类]（发现/形态 II 判定）→ 追加 M7 §1 → m7_stats.py --write
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| PM1 CLI | 子命令（selftest/eval/record）+ 旗标 + 退出码 | argv | Summary + exit code | PM2-PM5 |
| PM2 检测与门控 | endpoint TCP 预检 + deepeval 库检测 + OpenAIModel 注入 | endpoint/model/api_key | readiness | socket / deepeval |
| PM3 评测执行 | 双指标 measure → score/reason → JSON | LLMTestCase | JSON 负载 | deepeval.metrics |
| PM4 M7 登记 | 结果 JSON → M7 §1 样本行草案 | eval 结果 JSON | 草案文本 | 无 |
| PM5 selftest | 内嵌自测（解析/门控/草案，零真实端点零 deepeval） | — | exit code | PM2-PM5 |

### 3.3 数据流

1. `eval`: 门控（端点不可达 → exit 1；deepeval 缺失 → 安装提示 + exit 1）→ `get_deepeval_api` 注入端点 → 逐用例 `FaithfulnessMetric.measure`（+`GEval.measure`，失败不阻断主信号）→ 汇总 JSON（summary + cases）
2. `record`: 读 eval 结果 JSON → PM4 生成草案（含 model/status/reason 碎片）→ 打印供人工归类后追加 M7 + 跑 `m7_stats --write`
3. `selftest`: 纯机械 assert，不触工作树 / 不调真实端点 / 不依赖 deepeval

### 3.4 控制流（关键分派）

```
main()
  sub = argparse subcommand
  if sub == selftest: return run_selftest()
  if sub == eval:
      if not endpoint_reachable(ep): print 提示 + return 1          # I-6 门控
      if not deepeval_available():   print 安装提示 + return 1        # 如实登记
      api = get_deepeval_api(ep, model, key)                        # 注入端点
      for case in cases: fs,fr = measure_faithfulness(); gs,gr = measure_geval()
      payload = {summary, cases}; write/print JSON; return 0
  if sub == record:
      data = parse_results(results)                                  # PM4
      for i,c in cases: print to_m7_sample_row(...)
```

## 4. 契约（核心数据契约）

### 4.1 评测用例契约（--cases JSON）

```json
{"name": "faithful-01", "kind": "忠实用例", "input": "...指令...",
 "output": "...待评 LLM 输出...", "context": ["...来源上下文..."], "expected_faithful": true}
```

- `context` 数组 = DeepEval `retrieval_context`（judge 判忠实性的来源集）
- `expected_faithful` = 待验证标签（用于 selftest/复查统计 detected_hallu）
- 缺省 `--cases` 时用内置 DEFAULT_CASES（两测例，构造于 CER 语料）

### 4.2 M7 样本行草案（record）

字段对齐既有样本表列（编号/日期/载体/审查配置/发现/形态II复发/来源）。「审查配置」= DeepEval 臂 + 模型 + PASS/FAIL；「发现」留人工归并（P 分级语义不经机械推断，I-4）；「形态II复发」草案先置 0，由人工确认。reason 截取前 60 字符作证据锚点碎片附于来源列之后（便于人工复核真实 judge 输出）。登记后走既有 `m7_stats.py --write` 通道（不新增登记声明块，I-3）。

## 5. 替代方案

### 5.1 方案 Z：基础设施先行 + 端点就绪触发（选择，继承 RESEARCH）

- 描述：交付可真实运行的评测脚本 + 门控；真实评测由端点可达触发
- 优点：零假造（门控 I-6）；端点恢复即可跑；吃狗粮首用例本次直接实测
- 选择理由：REQ 断言可执行（端点可达是客观环境事实）；与「声明=机械重数」「对账制」哲学自洽

### 5.2 方案 Y：仅文档管线不动手（否决）

- 否决理由：P-037 三问已判定触发满足，用户明确指令升级实施——仅文档不落地脚本则无法产出真实评测结果，违背实施目的

### 5.3 方案 W：接入验证端门禁（否决）

- 否决理由：与本仓「验证纵（deterministic 门禁）/ 评测横（LLM-judge 语义信号）分离」核心纪律冲突（RESEARCH §4.3 / ANR-0010 Q1）——LLM-judge 得分非机械闸值，误接门禁会污染验证层确定性

## 6. 数据结构

```python
@dataclass(frozen=True)
class MetricRec:
    name: str
    kind: str
    faithful_score: float
    faithful_reason: str
    geval_score: float | None
    geval_reason: str | None
    expected_faithful: bool
    faithful_passed: bool

@dataclass(frozen=True)
class EvalSummary:        # 顶层汇总
    total: int
    faithful_passed: int
    detected_hallu: int   # 负例中被 Faithfulness 正确判低分（score<0.7）的个数
```

## 7. 错误处理

| 错误场景 | 处理方式 | 退出码 |
|---------|---------|-------|
| 端点不可达（eval） | P1 提示 + exit 1，不调 judge（I-6） | 1 |
| deepeval 库缺失（eval） | P1 安装提示 + exit 1 | 1 |
| --cases 读取/解析失败 | P1 提示 + exit 2 | 2 |
| judge 中途失败（网络/模型） | P2 如实标注，不阻断其他用例；该用例 score=0 标记失败 | 0（逐案失败） |
| 结果 JSON 缺失/非法（record） | P1/P2 提示 exit 2 | 2 |
| 未知异常 | 顶层 try/except | 2 |

## 8. 不变式（Invariants）

1. **I-1 默认只读**：deepeval_m7_eval.py 不写 M7（只生成草案供人工追加）；不写非 --output 指定文件；门控是只读 TCP
2. **I-2 确定性**：selftest/record 解析确定性（同输入 → 同输出）；reason 为 judge 产物如实透传，不截断改写语义
3. **I-3 零新登记规则**：复用 M7 既有样本列结构与 m7_stats 登记通道；不发明第二份统计声明
4. **I-4 登记 = 机械解析**：草案的 model/status/score 来自 eval JSON 机械字段；语义归类（发现/形态 II）留人工
5. **I-5 异构于生成端**：脚本对 M7 的写入一律经既有 m7_stats 通道；judge 输出如实透传不转述
6. **I-6 评测门控**：端点不可达 / deepeval 缺失 → 不假造评测（与 P-010 门控同构）

## 9. 幻觉排除审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 设计决策可追溯 RESEARCH（§2.1 映射表）——自查（单视角）
- [x] 无未验证硬依赖（H1/H2 须实测确认，见附录 C；H1 GEval 签名不作为设计主依赖——双指标之一的 GEval 失败不阻断 Faithfulness 主信号）
- [x] 无归因扭曲（端点可达以实测为准；不可达如实以门控承载，不假装已评测）

### 9.2 替代方案审查

- [x] 三方案（Y/W，Z 选择）各有明确理由；W 否决与本仓「验证纵/评测横」纪律自洽

### 9.3 职责边界审查

- [x] 职责边界清晰（§2.3）：语义归类归人工、hits 块归 m7_stats、不动既有三工具
- [x] 不越界：不入验证端门禁、不写 M7 统计声明

> **标注（RULE-1/RULE-4）**：本 §9 由同会话自查勾选（单视角）；独立 pass 待 Step 10 或用户触发，届时以独立结论为准。

## 10. 对实施的输入

### 10.1 关键工程约束

1. Windows：`python scripts/deepeval_m7_eval.py`；路径用 os.path
2. 依赖最小：除 deepeval（临时 venv，用后清理）外零第三方；selftest/record 纯 stdlib
3. script 自带 deepeval 可用性检测与安装提示
4. selftest expect 自增机械计数（同 dc_validator/m7_stats R7 同构）
5. eval 默认模型 qwen2.5-7b-instruct（规避 A-6）

### 10.2 风险与缓解

| 风险 | 缓解 |
|------|------|
| deepeval v4 API 签名与预期不符 | H1 实测确认；GEval 失败不阻断 Faithfulness 主信号 |
| 端点不可达阻塞实测 | 门控不假造；如实报告未评测 |
| judge 得分为语义信号非闸值 | 只作评测横信号，不接验证门禁（§5.3） |
| 临时 venv 污染工作区 | venv 建于 %TEMP%（或工作区外确认 gitignore 忽略），用后清理，不入仓 |

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）

## 附录 A：A 类断言明细

【A】A-1: 脚本提供 `selftest`/`eval`/`record` 三子命令（可于 `scripts/deepeval_m7_eval.py` main() 逐字 grep）。取证: 脚本 main() 三 branch。
【A】A-2: eval 用 `FaithfulnessMetric` + `GEval` 双指标，reason 一并落 JSON（可 grep `get_deepeval_api` 的 import + `_measure_faithfulness`/`_measure_geval`）。取证: 脚本 import/metrics 实测。
【A】A-3: 端点不可达 TCP 门控 exit 1，不调 judge（可 grep `endpoint_reachable` + `run_eval` 返回 1 分支）。取证: selftest F2/F6 + 脚本分支。
【A】A-4: reason 即证据锚点，落 JSON `faithfulness_reason`/`geval_reason`（可 grep cmd_eval payload 键）。取证: 脚本 payload 构造。
【A】A-5: 缺 deepeval 库时打印安装提示返回 1（可 grep `deepeval_available`）。取证: selftest F3 + 脚本分支。
【A】A-6: 临时 venv 建于工作区外（%TEMP%\deepeval-venv-*），用后清理，不入仓。取证: 安装路径 + P-038 清理实录（见 IMPLEMENTATION §2）。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "DeepEval 臂与 P-010 promptfoo 为互补关系：前者 LLM-judge 语义忠实性（faithfulness/hallucination），后者声明式一致性断言——两者正交，DeepEval 臂实施为独立评测位点，不是复用 P-010 '双臂'预留", "basis": "RESEARCH §2.5/B1（P-010 DESIGN/IMPL 全文检索零 DeepEval 引用）+ §4.1"},
  {"id": "B2", "inference": "内置吃狗粮两测例（忠实用例 expected=True + 引入来源外信息用例 expected=False）可验证 judge 是否区分忠实/虚构——若实测 Faithfulness 对负例正确给低分（<0.7），则 DeepEval 臂 '事实忠实定量化' 价值在本仓语料上首次落地实证（B2 价值自 P-037 B2 推断延伸）", "basis": "脚本 DEFAULT_CASES 构造 + A-2（双指标）+ RESEARCH §4.2①"}
]
```

## 附录 C：C 类判断复盘 + 假设区

**C 类判断（不机械对账，review 臂重数）**:
- C-1: 方案 Z 选择——基础设施先行 + 端点触发，弃 Y（纯文档不落地）与 W（接门禁）
- C-2: 不接验证端门禁——评测横与验证纵分离（RESEARCH §4.3/ANR-0010 Q1）
- C-3: 触发条件已满足（用户指定首用例 + 端点就绪）→ 实施

**假设区（[H]）**:
- [H1] deepeval v4.2.2 中 `FaithfulnessMetric(threshold/strict_mode/async_mode)` 与 `GEval(criteria/evaluation_steps/...)` 的签名与预期一致。查证路径: 实施时 venv 实测 measure 调用。
- [H2] judge 得分在目标端点（127.0.0.1:1234 + qwen2.5-7b-instruct）上可复现（同一用例多次 run，忠实/虚构区分方向稳定）。查证路径: 实施时真实测评。

## 附录 D：脚本 posix 语义注

- selftest/record 零 deepeval 依赖，全仓回绿色；eval 仅在显式调用且门控通过时触碰 deepeval。
- M7 草案不代写统计声明，样本追加后 `m7_stats.py --write` 重生成（I-3/I-6）。