# 审查验收 Checklist：DeepEval M7 评测臂——事实忠实性增强端评测

---
id: deepeval-m7-eval-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-10
depends: [deepeval-m7-eval-IMPLEMENTATION, deepeval-m7-eval-DESIGN]
upstream: null
---

> **Feature**: deepEval-m7-eval（PROGRESS P-038）
> **创建日期**: 2026-09-10
> **状态**: 有条件通过（selftest 12/12 + 端点门控 + 真实吃狗粮首测评完成 + M7 样本㉞ 入账；独立 pass 待触发——同 P-014 收口先例）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [IMPLEMENTATION.md](./DEEPEVAL_M7_EVAL_IMPLEMENTATION.md) v1.0
> **基于设计**: [DESIGN.md](./DEEPEVAL_M7_EVAL_DESIGN.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——独立 pass 待 Step 10 / 用户触发

---

## 1. 文档一致性验收（Step 8）

### 1.1 RESEARCH.md ↔ DESIGN.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN 决策可追溯到 RESEARCH | ☒ | §2.1 映射表逐条引 RESEARCH A-4/A-5/A-6/B1/§5 |
| RESEARCH 关键发现被 DESIGN 用 | ☒ | 触发满足/OpenAIModel 端点/双指标/qwen2.5-7b 规避全部采用 |
| 无文档间矛盾 | ☒ | 端点端到端 + 评测横不接门禁与 RESEARCH 一致 |

### 1.2 DESIGN ↔ IMPLEMENTATION 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN 模块在 IMPLEMENTATION 有对应实施 | ☒ | PM1-PM5 ↔ §2/§3 |
| 接口签名一致 | ☒ | selftest/eval/record 三子命令 + MetricRec/EvalSummary |
| DESIGN 不变式在 IMPLEMENTATION 实施 | ☒ | I-1 只读/I-4 机械/I-6 门控均代码落地 |
| 无设计未覆盖的实施 | ☒ | API 注入修正（set_default_model 缺失）为实施期适配，已回录 DESIGN 假设 H1 |

### 1.3 IMPLEMENTATION ↔ CHECKLIST 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 功能点在本 checklist 有验收项 | ☒ | §2 逐条覆盖 |
| 验收项可追溯到 IMPLEMENTATION | ☒ | 证据列引用 §9 实测 |

## 2. 功能验收

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 三子命令分发 | `selftest/eval/record` | 各返回正确退出码 | ☒ | IMPL §9 |
| selftest 全绿 | `py -3 scripts/deepeval_m7_eval.py selftest` | 12/12 PASS | ☒ | IMPL §9.1 |
| 端点不可达门控 | `eval`（不可达端点） | P1 + exit 1，不调 judge | ☒ | selftest F6 |
| deepeval 缺失门控 | 未装库环境 | 安装提示 + exit 1 | ☒ | IMPL §2.3 |
| 真实端点评测 | `eval`（127.0.0.1:1234 + qwen2.5-7b-instruct） | 双用例 judge 返回 score+reason | ☒ | IMPL §9.2 |
| M7 草案生成 | `record` + selftest F5 | 列序 + model/status/reason 碎片 | ☒ | IMPL §2.5 |

## 3. 接口验收

| 验收项 | 通过条件 | 状态 |
|--------|---------|------|
| eval --endpoint/--model/--api-key/--cases/--output | 参数可解析 | ☒ |
| record --results/--date | 参数可解析 | ☒ |
| selftest 无参 | 返回 0 | ☒ |

## 4. 不变式验收

| 不变式（DESIGN §8） | 验证方法 | 状态 |
|---------------------|---------|------|
| I-1 默认只读 | 代码审查：无对 M7/config 写操作，门控只读 TCP | ☒ |
| I-2 确定性 | selftest/record 解析确定性 | ☒ |
| I-3 零新登记规则 | 草案 + m7_stats --write 通道 | ☒ |
| I-4 登记 = 机械解析 | 草案字段直接取 eval JSON | ☒ |
| I-5 异构于生成端 | judge 输出如实透传不经转写 | ☒ |
| I-6 评测门控 | 端点/库不可用不假造评测（实测） | ☒ |

## 5. 错误处理验收（DESIGN §7）

| 错误场景 | 触发方式 | 预期 | 状态 |
|---------|---------|------|------|
| 端点不可达 | `eval` 不可达端点 | P1 + exit 1 | ☒ |
| deepeval 缺失 | 未装库环境 | 安装提示 + exit 1 | ☒ |
| judge 中途失败 | 真实运行（Faithfulness invalid JSON） | P2 标注、不阻断其他用例、score=0 | ☒ |
| 结果 JSON 缺失/非法 | `record --results` 缺文件 | P1 + exit 2 | ☒ |

## 6. 兼容性验收

| 环境 | 版本 | 状态 | 说明 |
|------|------|------|------|
| Python（selftest/record） | 3.12 | ☒ | 零 deepeval 依赖 |
| deepeval（eval） | 4.2.2 | ☒ | 临时 venv |
| judge 模型 | qwen2.5-7b-instruct | ☒ | 非空输出（规避 A-6） |
| 端点 | 127.0.0.1:1234/v1 | ☒ | TCP 可达 |

## 7. ADD 审计（Step 10）

### 7.1 Spec 质量门（Phase 0）

| 维度 | 得分（0-1） | 说明 |
|------|-----------|------|
| 可测试约束 | 1.0 | selftest 12 断言 + 端点门控可实测 |
| 模块映射 | 1.0 | PM1-PM5 清晰映射 |
| 接口契约 | 1.0 | dataclass + CLI 参数契约 |
| 修正项 | 0.8 | H1/H2 如实携带（H1 已解除，H2 部分证伪） |
| 跨模块契约 | 1.0 | 与 m7_stats 对接明确（I-3） |
| **总分** | 4.8/5 | **档位**: A |

## 8. 验收结论

### 8.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|------|------|------|------|------|
| 文档一致性 | 3 | 3 | 0 | 0 |
| 功能 | 7 | 7 | 0 | 0 |
| 接口 | 3 | 3 | 0 | 0 |
| 不变式 | 6 | 6 | 0 | 0 |
| 错误处理 | 4 | 4 | 0 | 0 |
| 兼容性 | 4 | 4 | 0 | 0 |
| ADD 审计 | 1 | 1 | 0 | 0 |
| **总计** | 28 | 28 | 0 | 0 |

### 8.2 验收决定

- [x] **有条件通过**：基础设施验收通过（28/28）；真实吃狗粮首测评完成（§9.2）但揭示 LLM-judge 边界（忠实用例被判 0.0 / Faithfulness 7B judge JSON 失败）——如实登记 M7 样本㉞，不造假通过；独立 pass（RULE-1/RULE-5）待触发

### 8.3 签字

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | 自查（单视角）+ 真实端点评测 + 收束（2026-09-10） | 2026-09-10 |
| 审查者 | 独立 pass 待触发 | — |

## 9. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|------|--------|------|------|
| 视图层同步（CODE_WIKI §2.1/§9/§10 + PROGRESS P-038）→ repo_stats 全绿 | 实施者 | 收束批 | 待办（本轮实施） |
| 临时 venv 清理（%TEMP%\deepeval-venv-dg-20260910） | 实施者 | 收束批 | 待办 |
| Faithfulness 需更强 judge 模型（H2 部分证伪）→ 适配后回归 | 触发驱动 | 端点/模型升级 | 待办 |
| 独立 pass（RULE-1/RULE-5） | 异步独立 | Step 10 | 待办 |

---
**Review 签字**: _________ 日期: _________