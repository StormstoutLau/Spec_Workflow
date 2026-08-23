# 调研文档：Promptfoo M7 对比臂声明式评测

---
id: promptfoo-m7-eval-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-08-23
depends: [SPEC-PROCESS, FWK-ASSERTION, langgraph-upgrade-RESEARCH, m7-hits-block-RESEARCH, precommit-dc-validator-DESIGN]
upstream: null
---

> **Feature**: promptfoo-m7-eval（PROGRESS P-010，优先级 3，主动队列末位）
> **创建日期**: 2026-08-23
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: [PROGRESS P-010](../../docs/PROGRESS.md)——"promptfoo M7 对比臂声明式评测"，源依据 [LANGGRAPH_UPGRADE_RESEARCH §8.2/§8.3/附录D-H5](../langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md)

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 5 | 每条附 E1 取证（本机实测 / 官方文档 / 仓库内可 grep），2026-08-23 Read/Grep/实测取证 |
| B 推断类 | 1 | B1，登记于附录 B |
| C 判断类 | 4 | §4.2 决策判断 |
| 假设区 | 2 | H1-H2，未取证声明 |

## 1. 调研目标

**核心问题**:
1. promptfoo 能否把「同一报告 × 同基座/异基座审查」变成声明式测试矩阵，并将结果机械喂给 M7 登记？（能力与接口）
2. LM Studio 端点不可达时，P-010 评测如何落地？（运行前提——本次实测发现）
3. 与 M7 hits 机读块 / dc_validator R7 如何衔接？（§5 hits 块已是声明=机械重数，promptfoo 结果登记应复用该通道）

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| RunCommand | promptfoo 安装/实测/环境探测 | `npm install -g promptfoo` / 端点 TCP 探测 / `promptfoo eval` PoC |
| WebSearch | promptfoo 官方文档（存储路径 env） | promptfoo env var config dir db cache path |
| Read | results.json 结构解析 / M7 §5 hits 块 / LANGGRAPH 源依据 | 逐文件 |
| Grep | M7 机械重数（samples=23）/ spec 目录现状 | 全仓 |
| 机械重数 | M7 §5 hits 块 `"samples": 23` 直接 Read | — |

### 2.2 调研范围

- **时间范围**: 2026（promptfoo 当前版本 0.122.0）
- **领域**: LLM 评测工具（promptfoo）适配本仓库的 M7 对比臂
- **排除**: 非评测工具横向对比（LiteLLM/Langfuse 已由 P-006/LANGGRAPH 调研裁决，不重复）；promptfoo 代码级内部实现

## 3. 调研发现

### 3.1 触发条件与源依据

- **触发条件成立**（A 类，E1）: M7 §5 hits 块 `"samples": 23`（[M7_EVIDENCE_LOG.md §5](../../docs/M7_EVIDENCE_LOG.md)），远超 LANGGRAPH §8.3 定义阈值「≥10」。源依据 [LANGGRAPH §8.2 表 promptfoo 行 + §8.3 次高 ROI 裁决 + 附录 D-H5](../langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md)。
- P-010 设计意图（源自 LANGGRAPH §8.3）: `promptfooconfig.yaml` 把「同一报告 × 同基座/异基座审查」变声明式测试矩阵，本地直调 LM Studio 端点作 provider，结果直接喂 M7 登记。

### 3.2 环境就绪（A 类，E1 实测）

#### promptfoo 0.122.0 安装与运行

- **安装**: `npm install -g promptfoo` 成功（702 packages），版本 0.122.0。
- **沙箱存储限制与解法**: 默认在 `~/.promptfoo`（Windows `%USERPROFILE%\.promptfoo`）建 SQLite DB 与 cache，被当前沙箱限制写入（`SQLITE_IOERR` + hit restricted）。解法 = 三个环境变量重定向到工作区内目录（官方文档证实）：`PROMPTFOO_CONFIG_DIR`（配置+数据库）/ `PROMPTFOO_CACHE_PATH`（缓存）/ `PROMPTFOO_LOG_DIR`（日志）。重定向后 `promptfoo --version` 正常，无 SQLite 报错。
- **Node 版本符合要求**: Node v24.14.1 ≥ 官方要求的 22.22.0（npm 需 Node ≥22.22.0）。

### 3.3 核心机制（A 类，E1 实测 PoC）

用 `echo` provider + contains/equals/javascript 断言 + `--output results.json` 跑最小 eval，验证:

| 机制 | 实测结果 | E1 证据 |
|------|---------|---------|
| 声明式测试矩阵 | 2 tests / 1 PASS / 1 FAIL 跑通 | eval 日志 |
| 断言机制 | contains/equals 逐 assertion 判定，pass/fail 到 componentResult 粒度 | results.json `gradingResult.componentResults` |
| 退出码 | 有 FAIL 时 EXIT=100（非零，CI 可拦截） | 实测 `EXIT=100` |
| JSON 输出 | results.json 含 stats / 逐 test success/pass / metrics (testPassCount 等) / tokenUsage / provider | results.json 全文 |

**接口发现**（对 P-010 登记设计的关键输入）: results.json 的 `results.results[]` 每项含 `provider.label`、`success`、`gradingResult.pass`、`testCase.metadata`；`stats` 顶层含 `successes/failures/errors`。这些可直接机械解析注入 M7 样本行。

**PoC 缺陷（如实记录，不影响结论）**:
- `javascript` 断言用了 `[output] => ...` 箭头语法，promptfoo 0.122.0 报 `Malformed arrow function parameter list`——语法需改为 `(output) => ...` 或字符串体；非核心机制问题，仅该断言写法错误（此断言原本设为本应 pass，因语法错被判 fail，反证断言判定是真实执行的）。
- `echo` provider 输出含提示词前缀，`equals` 精确匹配需前后缀一致——评测断言设计时需注意 provider 输出形态。

### 3.4 运行障碍：LM Studio 端点不可达（A 类，E1 实测）

三机 LM Studio 端点经 TCP 探测（1500ms 超时）全部不可达:

| 端点 | 归属 | 结果 |
|------|------|------|
| 192.168.1.11:1234 | 工作站 A | CLOSED/timeout |
| 192.168.1.15:1234 | 工作站 B | CLOSED/timeout |
| 192.168.1.10:1234 | 主控站（可选） | CLOSED/timeout |

**含义**: P-010 设计依赖「本地直调 LM Studio 端点作 provider」（LANGGRAPH §8.3），端点不可达使评测实际运行受阻，H5（LM Studio provider 对长文本审查 prompt 的成本/延迟）无法实测。这是本调研新发现的、源依据未预见的环境前提变化。

## 4. 综合分析

### 4.1 关键发现总结

1. **触发条件成立**：M7 samples=23 ≥ 10（机械重数，E1）[置信度: ★★★★★]
2. **promptfoo 能力适配**：声明式矩阵 / 断言 / JSON 输出 / 退出码均实测可用，满足「声明式评测 + 结果机械喂 M7」的设计意图 [置信度: ★★★★★]
3. **存储沙箱可绕过**：三 env 变量重定向到工作区 `.promptfoo/` [置信度: ★★★★★]
4. **运行障碍：LM Studio 端点全不可达**，评测实际运行与 H5 实测受阻 [置信度: ★★★★★]
5. **结果→M7 登记接口清晰**：results.json 可机械解析注入样本行 [置信度: ★★★★☆]

### 4.2 技术 landscape 与关键决策点

promptfoo 支持 `openai-compatible` provider（可指任意 OpenAI 兼容端点：LM Studio / 云端 API）。LANGGRAPH §8.2 ROI 矩阵将其列为「本地直调 LM Studio 端点」。端点不可达构成 **provider 选型决策点**：

- **方案 X（维持 LM Studio）**: 待端点恢复后运行——设计正确但当下不可执行，H5 继续挂起。
- **方案 Y（云端 OpenAI 兼容端点）**: 若用户持可用云端 key（DeepSeek/GLM 等），可绕过三机端点立即执行；但引入外部网络依赖 + 成本，与仓库"本地优先"身份有张力（LANGGRAPH §8.2 明确痛点对准本地 LM Studio）。
- **方案 Z（评测基础设施先行）**: 本 feature 交付「声明式评测基础设施」（config/脚本/登记接口）但不实际跨基座运行，端点不可达记为 H5 未决；待端点就绪即运行——《对账制非再生成制》哲学可类比：工具/设计先行，运行是触发器门控。

> 三方案为调研输出，最终 provider 选型与 feature 范围由用户/后续设计裁决，不在调研定案。

### 4.3 研究空白

本仓库此前无从「声明式评测工具」到「M7 机械登记」的衔接实现。P-010 若方案 Z 落地，将产出第一个「测试驱动评测基础设施」（相应于 dc_validator/m7_stats/repo_stats 三可执行件之外的可选评测运行通道），并把「对比臂审查」从手工切基座升级为声明式矩阵。

## 5. 幻觉排除审查（Step 2 Review）

### 5.1 外部事实验证

| 引用 | 来源 | 验证方式 | 状态 |
|------|------|---------|------|
| promptfoo 存储路径 env（CONFIG_DIR/CACHE_PATH/LOG_DIR） | promptfoo.dev/docs/installation | WebSearch 抓取官方文档 | ✅ E1 |
| promptfoo 需 Node ≥22.22.0 | promptfoo.dev/docs/installation | WebSearch | ✅ |
| promptfoo openai-compatible provider | 已知能力（未在本调研复验 provider 文档） | 依赖既有知识，标注待后续确认 | ⚠️ |

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| 声明式评测/断言/JSON/退出码 | 本机实测 PoC | ✅ 已验证（E1） |
| 三端点不可达 | 本机 TCP 探测 | ✅ 已验证（E1） |
| M7 samples=23 | M7 §5 hits 块 Read | ✅ 已验证（E1） |

### 5.3 待修正项

- [ ] §5.1 openai-compatible provider 声明待后续 provider 文档实测确认（本轮未复验）

## 6. 对设计的输入

### 6.1 可用的技术方案

1. `promptfooconfig.yaml` 声明式矩阵 + `--output results.json` + 退出码门禁
2. env 三件套重定向存储到工作区 `.promptfoo/`
3. provider 选型三方案（X 维持 LM Studio / Y 云端 / Z 基础设施先行）
4. results.json → M7 样本登记接口（机械解析 stats + 逐 test）

### 6.2 关键约束

- 仓库身份：纯文档仓库为体、最小工具层为用（CODE_WIKI v1.7.4 定位）——promptfoo 是独立 CLI provider，不侵入仓库，符合 LANGGRAPH §8.2「不侵入仓库」判定
- `声明 = 机械重数`（R7，M7 hits 块同构）：promptfoo 结果登记须经机械解析，不经 LLM 转手转写
- provider 输出形态影响断言设计（echo 含前缀、真实模型含格式差异）

### 6.3 风险

| 风险 | 等级 | 说明 |
|------|------|------|
| 端点不可达→评测不可运行 | 高 | 方案 Z 缓解（基础设施先行，运行触发门控） |
| promptfoo 版本演进 breaking | 中 | results.json schema 可能随版本变动，登记解析需标注 promptfooVersion |
| provider 长文本审查成本/延迟（H5） | 中 | 未实测，端点就绪后 PoC 验证 |
| 外部网络依赖（方案 Y） | 中 | 与仓库本地优先身份张力 |

## 附录 A: 事实类断言（A1-A5）取证

【A】A1: 触发条件成立——M7 §5 `"samples": 23`，LANGGRAPH §8.3 阈值 ≥10。取证: grep M7_EVIDENCE_LOG.md "samples" → 23
【A】A2: promptfoo 可运行——v0.122.0，env 重定向后 --version 正常。取证: 本机实测日志
【A】A3: 核心机制——声明式/断言/退出码100/JSON。取证: PoC eval 输出 + results.json
【A】A4: 存储 env——官方文档列 CONFIG_DIR/CACHE_PATH/LOG_DIR。取证: WebSearch promptfoo.dev/docs/installation
【A】A5: 端点不可达——三端点 TCP 探测超时。取证: Test-NetConnection / TcpClient 实测

## 附录 B: 推断类断言（B1）

```json
{
  "id": "B1",
  "conclusion": "promptfoo 的声明式评测 + JSON 输出 + 退出码门禁机制适配本仓库 M7 对比臂需求，结果可由脚本机械解析注入样本登记，但端点不可达使实际跨基座运行受阻，需 provider 选型裁决",
  "op": "transitivity",
  "claimed_chain": [
    {"step": 1, "text": "promptfoo 支持声明式测试矩阵 + 断言 + JSON 输出 + 退出码门禁（A3，E1 实测）", "source": "PoC eval 日志 + results.json"},
    {"step": 2, "text": "results.json 含 stats/逐 test/级 provider/机械可解析字段（A3，E1 实测）", "source": "results.json 结构解析"},
    {"step": 3, "text": "但 LM Studio 三端点全不可达，评测实际运行受阻（A5，E1 实测）→ 需 provider 选型（方案 X/Y/Z）或标记 H5 未决", "source": "TCP 探测"}
  ],
  "evidence_strength": "E1（依赖源逐条 Read/实测取证）",
  "audit_status": "OPEN（待设计裁决 provider 选型）"
}
```

## 附录 C: 假设区（H1-H2）

- [H1] openai-compatible provider 可指 LM Studio/云端——promptfoo 支持 openai-compatible 接入本地端点，未在本轮实测确认具体 provider 配置语法。查证路径: provider 文档 + 端点就绪后 PoC
- [H2] results.json schema 跨版本稳定——0.122.0 schema 已验证，后续版本可能变动。查证路径: 升级时回归 / 解析器标注 promptfooVersion

---

**Review 签字**: _________ 日期: _________