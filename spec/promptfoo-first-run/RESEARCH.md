---
id: promptfoo-first-run-RESEARCH
type: design
version: 1.1
status: in-review
date: 2026-09-09
depends: [promptfoo-m7-eval-IMPLEMENTATION, community-ecosystem-RESEARCH, ADR-0010]
upstream: null
---

# 调研文档：promptfoo 首轮评测——调研-懒加载分析（吃狗粮模式，P-036）

> **Feature**: promptfoo 首轮评测（H3 触发驱动项——promptfoo redteam 模块对本仓 M7 语料的安全评测价值）
> **创建日期**: 2026-09-09
> **状态**: in-review（审查中）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「promptfoo 首轮评测 按照吃狗粮模型进行调研-懒加载分析」——CER §5.4 H3（待首轮评测端点就绪后评估）+ P-010 CHECKLIST §11（首轮评测待办，端点就绪触发）
> **v1.1 变更（2026-09-10，用户指令「将这部分补充到调研文档中 本地大模型已经组建集群 参考 D:\RPC\docs\三机推理集群使用手册.md promptfoo扩展暂时挂起 需要等后续工作站集群完善之后再进行升级」）**: **端点认知修正**——P-036 时探测的 `192.168.1.x:1234` 为**漂移前旧 LM Studio 地址**；参考 `D:\RPC\docs\三机推理集群使用手册.md` v1.8（2026-09-09 C 站接入）：**三机推理集群已组建**，OpenAI 兼容端点 = LiteLLM 网关 `scott-lau-GTR-Pro.local:4000` + A 站 `10.10.10.1:8080`（gpt-oss）+ B 站 `:8080`（nemotron）+ C 站 `192.168.1.37:8080`（独立端点），E2E 已验证——「端点就绪」触发条件已实质成立；**新增 §3.5 promptfoo 问题域说明**；**gate 判定更新**：Q2 端点条件已实质满足，但**用户主动裁决 = 扩展暂时挂起**（非无法实施，是暂缓升级），登记触发条件 = 工作站集群完善后升级评估。断言计数不变（6A+1B+2C+1H——A 5→6 补集群现状断言）。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 6 | 每条附 E1 取证（2026-09-09 本机实测 / 官方文档 / D:\RPC 集群手册） |
| B 推断类 | 1 | B1 登记于附录 B |
| C 判断类 | 2 | §4 懒加载 gate 判定 + red team 适配判定 |
| 假设区 | 1 | H1 待触发 |

## 1. 调研目标

**核心问题**:
1. 首轮评测的触发条件（端点就绪）当前是否成立？（P-010 CHECKLIST §11 待办前置）
2. promptfoo redteam 模块（CER H3）对本仓 M7 语料是否具备评测价值？
3. ADR-0010 三问懒加载 gate 对「首轮评测 + red team」的判定走向——实施 or 止于懒加载？

## 2. 调研方法

| 工具 | 用途 | 查询 |
|------|------|------|
| Test-NetConnection | 三机 LM Studio 端点 TCP 探活（E1） | 192.168.1.11/15/10:1234 |
| RunCommand | promptfoo 版本 + redteam 命令面本机实测（E1） | `promptfoo --version` / `promptfoo redteam --help` |
| WebSearch | promptfoo red team 能力快照（2026，E2 官方文档） | red team plugins / OWASP LLM Top 10 / release notes |
| Read | P-010 四件套 + pf_m7_eval.py CLI（E1 仓内） | CHECKLIST/RESEARCH/IMPLEMENTATION |

## 3. 调研发现

### 3.1 端点现状（探活记录 + 集群演进修正，2026-09-10 v1.1）

**v1.0 探活记录（2026-09-09，旧地址）**:

| 端点 | 归属 | 结果 |
|------|------|------|
| 192.168.1.11:1234 | 工作站 A | **不可达**（CLOSED/timeout） |
| 192.168.1.15:1234 | 工作站 B | **不可达**（CLOSED/timeout） |
| 192.168.1.10:1234 | 主控站（可选） | **不可达**（CLOSED/timeout） |

**v1.1 端点认知修正（D:\RPC 三机推理集群手册 v1.8，2026-09-09 C 站接入）**:

P-036 探活的 `192.168.1.x:1234` 是**漂移前的旧 LM Studio 端点地址**——三机推理集群组建后端点形态已彻底演进（IP 漂移：A .11→.33 / B .15→.32，主控站 .10→.9；协议从 LM Studio 切换为 llama.cpp/vLLM + LiteLLM 网关）。**当前集群端点（OpenAI 兼容，E2E 已验证）**:

| 服务 | 地址 | 用途 |
|------|------|------|
| **LiteLLM 网关** | `http://scott-lau-GTR-Pro.local:4000` | 统一 API 入口（nemotron/gpt-oss 路由，fallback + 限流） |
| llama-server B | `http://scott-lau-GTR-Pro.local:8080` | nemotron 主力端点（llama.cpp, 直连免 key） |
| llama-server A | `http://scott-lau-NEX.local:8080`（USB4 10.10.10.1） | gpt-oss 速度档端点（双端点） |
| llama-server C | `http://192.168.1.37:8080` | C 站独立端点（2026-09-09 接入，常驻 nemotron） |

**含义（v1.1 修正）**: P-010 方案 Z 的触发前置「端点就绪」**已实质成立**——集群已组建且 OpenAI 兼容端点 E2E 验证通过（claudecode/opencode 双 agent CLI 已接通）。首轮评测不再受端点不可达阻塞（阻塞认知基于旧地址，已作废）。

### 3.2 promptfoo 本机工具链（E1 实测 2026-09-09）

- **版本**: `promptfoo --version` = **0.122.0**（与 P-010 同版本，无漂移）
- **redteam 命令面**: `promptfoo redteam init/eval/discover/generate/run` 可用（`--help` 实测正常）
- **既有评测臂**: [pf_m7_eval.py](../../scripts/pf_m7_eval.py) 三子命令 `run/selftest/record` + 双臂端点门控（I-6）就绪（P-010 交付）

### 3.3 promptfoo red team 能力快照（2026，官方文档 E2）

| 维度 | 快照 |
|------|------|
| 插件总量 | **157 插件 / 6 类**（brand / compliance / dataset / security / trust-safety / custom） |
| 框架映射 | OWASP LLM Top 10（2025 版）/ NIST AI RMF / MITRE ATLAS / ISO 42001 / GDPR / EU AI Act |
| **financial 族插件**（与本仓同构观察） | `financial:counterfactual`（虚假金融叙事）/ `financial:hallucination`（编造市场数据）/ `financial:sycophancy`（迎合高风险投资）/ `financial:defamation` |
| 相关通用插件 | `hallucination` / `unverifiable-claims` / `harmful:misinformation-disinformation` / `overreliance` |
| 许可形态 | OpenAI 收购（2026-07 公告）后仍 **MIT 开源**（2026 release notes 确认） |

【A】A-01: 2026-09-09 探测三机旧 LM Studio 端点（192.168.1.11/15/10:1234）全部不可达——**已确认 = 漂移前旧地址**（IP 漂移 A .11→.33 / B .15→.32，协议切换 llama.cpp），探测事实成立但端点认知 v1.1 已修正。取证: Test-NetConnection 实测（v1.0 记录）
【A】A-02: 本机 promptfoo 0.122.0（与 P-010 同版本零漂移）且 `redteam` 命令面可用（init/eval/discover/generate/run）。取证: `promptfoo --version` + `promptfoo redteam --help`
【A】A-03: promptfoo red team 支持 157 插件 / 6 类 + 多框架映射（OWASP LLM Top 10 2025/NIST AI RMF/MITRE ATLAS/ISO 42001/GDPR/EU AI Act）。取证: promptfoo.dev 官方文档（plugins/owasp-llm-top-10/releases）
【A】A-04: financial 族插件存在（counterfactual/hallucination/sycophancy/defamation），与本仓「幻觉检测/断言分级」方法论同构观察成立。取证: promptfoo.dev 官方文档 financial 插件
【A】A-05: P-010 方案 Z 基础设施完整交付（pf_m7_eval.py run/selftest/record + 双臂门控 I-6），首轮评测仅剩端点触发待办。取证: PROMPTFOO_M7_EVAL_CHECKLIST.md §11
【A】A-06: **三机推理集群已组建并运行**（`D:\RPC\docs\三机推理集群使用手册.md` v1.8，2026-09-09 C 站接入）——OpenAI 兼容端点 = LiteLLM 网关 `scott-lau-GTR-Pro.local:4000` + A `10.10.10.1:8080`（gpt-oss）+ B `:8080`（nemotron）+ C `192.168.1.37:8080`（独立端点），E2E 已验证（claudecode/opencode 双 agent CLI 接通）——「端点就绪」前置已实质成立。取证: D:\RPC 集群手册 v1.8 §1.2/§2（2026-09-10 Read）

### 3.4 M7 语料适配分析（red team 评测价值研判）

- 本仓 M7 语料 = 审查对比臂样本（A/B/C 断言分级 + 形态 II 复发跟踪），是**文档声明准确性证据**而非 LLM 应用的用户输入
- red team 插件生态的评测对象 = **面向用户的 LLM 应用的攻击面**（prompt injection / PII 泄漏 / 输出处理等 OWASP 维度）
- **适配交点有限**: financial:hallucination / unverifiable-claims 等「事实性/一致性」插件与 M7 断言分级**同构概念**（都是"产出的声明是否真实"），但评测载体制约——本仓 M7 语料为**静态文档声明证据**，red team 的目标是「运行中的 LLM 应用攻击面」（prompt injection 等要打实时端点），本仓语料非运行应用、无攻击面可打（集群端点虽已组建，但评测对象是文档语料本身而非端点上跑的模型服务）
- 结论研判: red team 模块对本仓 M7 语料的直接评测价值 = **低**（概念同构，载体不适用——v1.1 澄清：不适用原因为语料静态性而非端点缺失）；不排除未来在 M7 stitches 评测（promptfoo eval 双臂）接入时顺带观察

### 3.5 promptfoo 到底解决什么问题（问题域说明，v1.1 补充——用户指令「将这部分补充到调研文档中」）

**核心问题**: LLM 应用没有传统软件工程的可靠测试手段——传统单元测试可写死期望值断言，但 LLM 输出是概率性的、不可精确预测，导致"改 prompt 后变好还是变坏"无法量化、无法自动化、无法回归。

promptfoo 把该问题拆为四个子问题并逐一解决：

| 子问题 | promptfoo 机制 |
|--------|---------------|
| ① 输出不可断言 | **声明式测试**：YAML 定义用例 + 断言器（`contains`/`equals`/`javascript`/`llm-rubric`），机械判定 pass/fail，替代人工目测 |
| ② 改完不知好坏 | **测试矩阵**：同一组用例 × 多 prompt × 多模型横向对比，锁定回归 |
| ③ 进不了 CI | **results.json + 退出码**（有 FAIL 时 EXIT=100），可接入流水线与门禁 |
| ④ 对抗面未知 | **red team**：按 OWASP LLM Top 10 等框架自动生成注入/PII 泄漏等攻击输入 |

**对本仓的定位置**（关联 P-010/P-036 评估）:
- 本仓非 LLM 应用开发者，而是**借其前三项能力作审查对比臂**——P-010 复用「声明式矩阵 + 机械结果 + 退出码门控」，把「同基座/异基座审查」变成可回归评测
- 第④项（red team）正因本仓**语料为静态文档声明证据**（非运行 LLM 应用）而评测价值低（P-036 C-2）

## 4. ADR-0010 懒加载三问 gate（候选吸收物 = promptfoo 首轮评测 + red team 模块）

- **Q1 放哪层**: 若实施 = Layer-1（外部评测工具，pf_m7_eval 双臂真实运行 + red team 插件评测）；概念吸收（financial 同构观察）= Layer-0
- **Q2 激活条件**: **端点维度已实质满足**（v1.1：三机集群 OpenAI 兼容端点 E2E 已验证，A-06）——但 **red team 评测价值仍低**（C-2，语料静态性）；且**用户主动裁决 = 扩展暂时挂起**（2026-09-10，等待工作站集群完善后升级），故整体激活条件未满（挂起态）
- **Q3 未激活副作用 = 0**: 是——仅调研登记，零工具改动、零校验器改动

【C】C-1: **扩展暂时挂起（用户裁决，2026-09-10）**——promptfoo 首轮评测与 red team 模块本批不实施；端点已实质就绪（A-06）但用户主动暂缓，登记触发条件 = 工作站集群完善后升级评估（非"端点不可达"阻塞）。依据: 用户指令 + A-06 + ADR-0010 Q2 门禁
【C】C-2: red team 模块对本仓 M7 语料评测价值 = **低**（概念同构但载体不适用——语料为静态文档声明证据）；financial 族插件 = 方法论同构登记（Layer-0 概念，不实施）。依据: A-03/A-04 + §3.4 适配分析

## 5. 结论

1. **端点前置已实质成立**（v1.1 修正）：三机推理集群已组建，OpenAI 兼容端点 E2E 已验证（A-06）——原"端点不可达"阻塞认知基于漂移前旧地址，已作废
2. **red team 评测价值低**（C-2）：语料静态性致载体不适用——概念同构、载体不适用
3. **扩展暂时挂起**（C-1，用户裁决）：promptfoo 扩展本批不实施，待工作站集群完善后升级评估；同 P-030 先例零工具改动
4. **触发条件登记**：工作站集群完善后 → 评估 promptfoo 升级（首轮双臂评测 + financial 同构观察随 M7 stitches 评测顺带）

- [H1] 工作站集群完善后 promptfoo 升级评估中首轮双臂评测（同基座/异基座 provider 对比 + 成本/延迟）的实际价值待实测——P-010 H5 成本/延迟未决项延续，集群完善后述职

**Review 签字**: _________ 日期: _________

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "promptfoo red team 模块对本仓 M7 语料的评测价值低——工具生态面向 LLM 应用攻击面（OWASP 维度），本仓为文档声明证据无攻击面；仅 financial/事实性插件与本仓断言分级同构概念可 Layer-0 观察", "basis": "A-03/A-04 + §3.4 适配分析归纳"}
]
```