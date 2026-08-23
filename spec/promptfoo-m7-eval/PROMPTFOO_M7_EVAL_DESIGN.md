# 设计文档：Promptfoo M7 对比臂声明式评测

---
id: promptfoo-m7-eval-DESIGN
type: design
version: 1.0
status: draft
date: 2026-08-23
depends: [promptfoo-m7-eval-RESEARCH, SPEC-PROCESS, FWK-ASSERTION, m7-hits-block-DESIGN]
upstream: null
---

> **Feature**: promptfoo-m7-eval（PROGRESS P-010，优先级 3）
> **创建日期**: 2026-08-23
> **状态**: draft（草稿）
> **Spec 步骤**: Step 3-4
> **基于调研**: [PROMPTFOO_M7_EVAL_RESEARCH.md](./PROMPTFOO_M7_EVAL_RESEARCH.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

---

## 1. 设计目标

把「同一报告 × 同基座/异基座审查」从手工切基座 + 人工登记（P-004 刚经历的形态）升级为 **promptfoo 声明式评测矩阵 + 结果机械登记**（LANGGRAPH §8.3 次高 ROI 裁决 + P-010 验收标准）。

产出三件：① `spec/promptfoo-m7-eval/promptfooconfig.yaml`（声明式评测矩阵模板，provider 指向可配端点）；② `scripts/pf_m7_eval.py`（结果结果解析 + M7 样本登记辅助 + 自测）；③ 运行门控说明（端点就绪触发）。

**范围裁决（RESEARCH §4.2 方案 Z）**：LM Studio 三端点不可达，本 feature 交付**评测基础设施**（config + 登记脚本 + 运行插件），实际跨基座评测运行由端点就绪触发（运行触发器门控）；端点不可达如实登记为 H5 未决，不引入云端外部依赖。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| 触发条件成立（M7 samples=23 ≥ 10，机械重数） | feature 范围 = 声明式评测基础设施 + 登记接口 | RESEARCH A1 |
| promptfoo 声明式矩阵/断言/JSON/退出码100 全实测可用 | 采用 promptfoo 0.122.0 作评测引擎；config 声明式矩阵 | RESEARCH A3 |
| 存储沙箱限制可被 env 三件套绕过 | 运行期注入 PROMPTFOO_CONFIG_DIR/CACHE_PATH/LOG_DIR 到工作区 | RESEARCH A4 |
| results.json 可机械解析（stats/逐 test/provider） | 登记脚本解析 results.json → M7 样本行 | RESEARCH A3/B1 |
| **LM Studio 三端点全不可达**（运行障碍） | 方案 Z：基础设施先行 + 运行触发门控；不引入云端 | RESEARCH A5/§4.2 |
| openai-compatible provider 可指任意 OpenAI 兼容端点 | provider 配置为可替换端点（默认待填 LM Studio 地址） | RESEARCH H1（待确认） |

### 2.2 相关 ADR / 规范

| 文档 | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [FWK-ASSERTION R7](../../docs/ASSERTION_EVIDENCE_FRAMEWORK.md) | §0 统计表计数 = 机械重数 | 评测结果登记须机械解析 results.json，不经 LLM 转手转写；登记结构对账同不变式 |
| [m7-hits-block-DESIGN §4/§8](../m7-hits-block/M7_HITS_DESIGN.md) | hits 块 = M7 唯一统计声明处 + 声明=重数 | 评测登记复用 M7 §1/§2 载体现有结构；登记脚本不生产新统计声明块（避免第二真值源） |
| [ADR-0007 D1](../../adr/ADR-0007-unified-document-contract.md) | M7_EVIDENCE_LOG.md 为 M7 数据唯一活载体 | 评测结果样本行追加到 M7 §1，走既有样本登记工作流（+m7_stats --write） |
| [PROGRESS P-010](../../docs/PROGRESS.md) | 验收标准原文 | "promptfooconfig.yaml + 首轮声明式对比评测（同一报告 × 同基座/异基座审查）结果入 M7 + LG H5 成本/延迟实测"三要求映射（§2.3） |

### 2.3 职责边界

**职责内（本设计回答）**
1. promptfooconfig.yaml 声明式评测矩阵模板（同一报告 × 多 provider 的阵列）
2. results.json → M7 样本行登记的机械解析脚本（pf_m7_eval.py）
3. 运行门控：端点就绪检测 + 评测运行命令封装 + H5 成本/延迟记录
4. 通过/失败判定与退出码（promptfoo 断言 + pf_m7_eval 登记校验）

**职责外（不回答——独立范式，不吞并）**
- **实际评测运行**（调用真实模型端点）——受端点就绪门控，非本 feature 固定交付
- 样本行的**语义归类判断**（该次审查是同基座还是异基座、发现是否形态 II）——人工 + 既有 m7_stats 对账职责（m7-hits-block 边界）
- M7 hits 块的生成/校验——已有 m7_stats（P-011），本设计不重复
- dc_validator / repo_stats 的校验职责——不动既有三可执行件

**能力边界（回答不了——如实声明）**
- results.json schema 跨版本稳定性（H2）——登记脚本标注 promptfooVersion，升级时回归
- openai-compatible provider 配置的确切语法（H1）——端点就绪时 PoC 确认；本 design 提供占位结构

## 3. 架构设计

### 3.1 整体架构

```
[端点就绪触发]（LM Studio 端点 TCP 可达）
    │
    ▼
运行封装: python scripts/pf_m7_eval.py run --config spec/promptfoo-m7-eval/promptfooconfig.yaml
    │  内部: 注入 PROMPTFOO_CONFIG_DIR/CACHE_PATH/LOG_DIR → promptfoo eval --output results.json
    ▼
[promptfoo eval] 声明式矩阵（同一报告 × 同基座/异基座 provider）
    │  断言（contains/equals/javascript）判定 pass/fail，退出码门禁
    ▼
results.json
    │
    ▼
登记封装: python scripts/pf_m7_eval.py record --results results.json
    │  机械解析 stats/逐 test/provider → 生成 M7 §1 样本行草案
    ▼
[人工确认归类]（同基座/异基座 + 形态II判定）→ 追加 M7 §1 → m7_stats.py --write
    │
    ▼
[pre-commit m7-stats hook 复验]
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| PM1 CLI | 子命令（run/record/selftest）+ 旗标解析 + 退出码 | argv | Summary + exit code | PM2-PM4 |
| PM2 运行封装 | 注入 env → 调 promptfoo eval → 端点就绪预检 | config 路径 | eval 结果 + latency/cost 度量 | promptfoo CLI |
| PM3 结果解析 | results.json → EvalRecord（stats/逐 test/pass/fail/provider） | results.json | list[EvalRecord] + Summary | 无 |
| PM4 M7 登记 | EvalRecord → M7 §1 样本行草案（供人工归类后追加） | EvalRecord | 样本行草案文本 | 无 |
| PM5 selftest | fixture 自测（结果解析/登记草案/端点预检逻辑） | — | exit code | PM2-PM4 |

### 3.3 数据流

1. `run`: 端点预检（TCP 探测，不可达 → 明确报错提示启动端点/改 provider）→ 注入 env → `promptfoo eval -c <config> --output <out>` → 解析退出码 + latency 记录（H5 数据）
2. `record`: 读 results.json → PM3 解析 → PM4 生成 M7 §1 样本行草案（含 provider.label / pass-fail / findings 计数占位）→ 打印供人类确认归类后追加 M7 + 跑 m7_stats --write
3. `selftest`: tempdir fixture，不触工作树/不调真实端点

### 3.4 控制流（关键分派）

```
main()
  sub = argparse subcommand
  if sub == selftest: return run_selftest()
  if sub == run:
      if not endpoint_reachable(cfg.endpoint): 报错+列出可用端点+exit 1   # 门控
      env.extend(PROMPTFOO_*_DIR → workdir)
      subprocess promptfoo eval ... --output results.json
      print latency/cost metrics（H5 数据点）
      return promptfoo exit code（断言门禁）
  if sub == record:
      records = parse_results(results.json)          # PM3
      draft_rows = to_m7_sample_rows(records)        # PM4
      print draft 供确认
```

## 4. promptfooconfig.yaml 契约（核心数据契约）

### 4.1 结构

- 落位：`spec/promptfoo-m7-eval/promptfooconfig.yaml`（feature 随 spec 版本化）
- 核心：`prompts`（审查 prompt 模板，含 `{{body}}` 报告片段变量）+ `providers`（**同一报告 × 同基座/异基座 provider 阵列**）+ `tests`（声明式用例，vars + assert）

### 4.2 providers 设计

| provider | 标签 | 说明 |
|----------|------|------|
| `openai-compatible:base`（端点占位 `http://<ip>:1234/v1/chat/completions`） | base-model | 同基座臂（默认占位，运行时按 cfg 注入地址） |
| 第二个 provider（占位） | cross-model | 异基座臂（LANGGRAPH 目标：同报告 × 双基座对比） |

> **端点占位策略**: config 中 endpoint 用占位符（非硬编码 IP），由 pf_m7_eval.py `run` 时经 `--endpoint` 注入，避免把具体机器地址固化进版本化 config（可移植性 + 不因端点变动重开 feature）。

### 4.3 assert 设计

| assertion 类型 | 用途 | 备注 |
|---------------|------|------|
| `contains` | 审查必须覆盖的关键元素存在性 | 机械判定 |
| `equals` | 输出精确匹配（需注意 provider 输出形态） | RESEARCH PoC 教训：echo 含前缀 |
| `javascript` | 结构化复核（如计数包含断言） | 语法用 `(output) => ...`（Padding 教训） |

### 4.4 登记结构（M7 §1 样本行）

评测结果经 record 生成 M7 §1 新增行草案，字段对齐既有样本表列（编号/日期/载体/审查配置/发现/形态II复发/来源）；「审查配置」字段标注 provider 标签（同基座/异基座），「发现」字段由断言语义 + 人工归综合并。登记后走既有 `m7_stats.py --write` 通道（不新增登记声明块）。

## 5. 替代方案

### 5.1 方案 Z：基础设施先行（选择，源自 RESEARCH §4.2）

- 描述：交付 config + 登记脚本 + 运行门控；实际评测由端点就绪触发
- 优点：仓库身份零损耗（本地优先，不引入云端）；端点恢复即可跑，无返工；H5 未决如实标注
- 缺点：当下无法产出「首轮评测结果入 M7」这一验收项（缺运行数据）
- 选择理由：REQ 断言可执行（端点不可达是客观环境事实，非设计可解）；与仓库「声明=机械重数」「对账制非再生成制」哲学最自洽

### 5.2 方案 Y：云端 OpenAI 兼容 provider（备选）

- 描述：用户提供云端 key，config 指云端端点，立即跨基座运行
- 否决理由（本 feature 范围）：引入外部网络依赖 + 成本，与 LANGGRAPH §8.2「本地直调 LM Studio」痛点对准有张力；需用户显式提供 key 方可行——**保留为可选项**，用户调 `--endpoint` 与 provider 即可切换，设计不排斥

### 5.3 方案 X：仅待端点恢复（否决为默认）

- 否决理由：被动等待使 feature 全时阻塞；先交付基础设施，端点恢复即激活运行，主动性与方案 Z 的灵活切换优于纯等待

### 5.4 方案 W：手写脚本自建评测器（否决）

- 否决理由：LANGGRAPH §8.2 已裁决 promptfoo 是已验证标准模式（声明式/断言/CI 原生，均 E1 实测）；自建评测器重复造轮子且引入新维护面，违背复用决策

## 6. 数据结构

```python
@dataclass(frozen=True)
class EvalRecord:
    provider_label: str      # "base-model" | "cross-model"
    success: bool            # 逐 test success
    pass_: bool              # gradingResult.pass
    findings_count: int      # 发现列计数（断言命中性，占位由语义归并）
    metadata: dict           # 透传 testCase.metadata
    latency_ms: float        # H5 数据
    cost: float              # token 成本（H5 数据）

@dataclass(frozen=True)
class EvalSummary:           # 顶层 stats 机械重数
    successes: int
    failures: int
    errors: int
    total_tests: int
```

## 7. 错误处理

| 错误场景 | 处理方式 | 退出码 |
|---------|---------|-------|
| 端点不可达（run） | 明确报错 + 列出探测端点 + 提示改 provider | 1 |
| results.json 缺失/非法（record） | P1 式报错 | 1 |
| promptfoo 未安装 | 提示安装命令 | 1 |
| 未知异常 | 顶层 try/except | 2 |

## 8. 不变式（Invariants）

1. **I-1 默认只读**：pf_m7_eval.py 不写 M7（只生成样本行草案供人工确认追加）；不改 config；端点预检是只读 TCP
2. **I-2 确定性**：record 解析确定性（同 results.json → 同草案）；无时间戳污染样本行
3. **I-3 零新登记规则**：复用 M7 既有样本列结构与 m7_stats 登记通道；不发明第二份统计声明
4. **I-4 登记 = 机械解析**：样本行草案的 provider/结果/度量来自 results.json 机械字段，不经 LLM 转述；语义归类（同/异基座、形态II）留人工
5. **I-5 异构于生成端**：脚本纯机械，无 LLM
6. **I-6 运行触发器门控**：评测实际运行以端点可达为前置；亏欠承诺（未运行不声称已评测）

## 9. 幻觉排除审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 设计决策可追溯 RESEARCH（§2.1 映射表）——自查（单视角）
- [x] 无未验证假设（H1/H2 随 RESEARCH 附录 C 显式携带；H1 不作为硬依赖——provider 结构占位、run 时确认）
- [x] 无归因扭曲（端点不可达如实以方案 Z 承载，不假装可运行）

### 9.2 替代方案审查

- [x] 四方案（Y/X/W）各有明确理由；W 否决与 LANGGRAPH §8.2 决策自洽

### 9.3 职责边界审查

- [x] 职责边界清晰（§2.3）：语义归类归人工、hits 块归 m7_stats、不动既有三工具
- [x] 不越界：不动 M7 hits 声明块生成逻辑

> **标注（RULE-1/RULE-4）**：本 §9 由同会话自查勾选（单视角）；独立 pass 待 Step 10 或用户触发，届时以独立结论为准。

## 10. 对实施的输入

### 10.1 关键工程约束

1. Windows：`python scripts/pf_m7_eval.py`；路径用 os.path
2. 零第三方依赖（stdlib：argparse/os/sys/json/dataclasses/socket/subprocess/tempfile）——promptfoo 走 CLI 子进程，不引其 npm 包为 Python 依赖
3. data 输出/运行目录：工作区 `.promptfoo/`（经 env 注入）
4. selftest expect 自增机械计数（DR-6 同构）
5. config 中 endpoint 为占位符，运行时注入（I-1 可移植性）

### 10.2 风险与缓解

| 风险 | 缓解 |
|------|------|
| 端点不可达阻塞验收项 | 方案 Z 明确范围 = 基础设施；「首轮评测」验收项标记为端点就绪触发（不假造数据） |
| results.json schema 跨版本变动 | record 标注 promptfooVersion；H2 随升级回归 |
| promptfoo CLI 行为差异（Windows） | run 封装实测（Step 10 PoC） |
| openai-compatible provider 语法（H1） | 占位结构 + run 时 PoC 确认，不作为验收主依赖 |

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）