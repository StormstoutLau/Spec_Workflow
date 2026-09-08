# 设计文档：独立验证（出路 C——verify-anchor 锚点真实性 + 审查臂输入重定义）

---
id: independent-verify-DESIGN
type: design
version: 1.0
status: draft
date: 2026-09-09
depends: [independent-verify-RESEARCH, ADR-0011, ADR-0010, step-gate-DESIGN, SPEC-PROCESS]
upstream: null
---

> **Feature**: 独立验证（P-025——ADR-0011 出路 C：审查臂从「读事件流」→「查系统真实状态」）
> **创建日期**: 2026-09-09
> **状态**: draft
> **Spec 步骤**: Step 3-4
> **基于调研**: [RESEARCH](./RESEARCH.md) v1.0（形态 = verify-anchor 只读命令 + 审查臂规则 + 纯登记型查证范围）

---

## 1. 设计目标

给审查臂（RULE-1/5 独立 pass）一条**机械取证通道**：当审查臂面对 decision 事件流的自报锚点时，可当场用 `verify-anchor` 验证「锚点指向的位置真实存在且可达」（文件存在 / 章节标题精确匹配 / 行号有效），把 ADR-0011 诊断二「表演性决策软肋」中**可机械压缩的表演空间**（指向不存在文件/章节的假锚点）用确定性程序封死；语义层（锚点断言内容对错）仍由 RULE-5 异基座审查臂把关。

**目标 = 落地 ADR-0011 出路 C**：审查输入从「只读自报流」→「自报流 + verify-anchor 取证 + git 状态对照」；纯登记型批次（P-023 式零 diff）查证范围显式化。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| ANCHOR_RE 只查锚点形态，零真实性校验（12 条 E1 自报实证） | verify-anchor 机械核查：文件存在 + 章节精确匹配 + 行号上界 | RESEARCH §3.1 |
| 锚点两种形态：`§N` 章节引用（9 条）+ `#Lxx` 行号引用（3 条） | 解析器支持两形态；URL → soft（外部不可本地核） | RESEARCH §3.1 |
| 既有独立 pass = 文档产出审核，非决策链真实性 | SPEC_PROCESS RULE-1 补充独立 pass 取证清单（审查输入重定义） | RESEARCH §3.2 |
| 纯登记型批次（P-023）零 diff 合法 | 查证范围 = 文档存在 + 章节真实 + session↔文档状态一致；无 diff 不判违规 | RESEARCH §3.3 |
| 只验位置可达，不验断言对错 | verify-anchor 边界声明：语义层归 RULE-5 异基座 | RESEARCH §4.1-4 |

### 2.2 相关 ADR / 契约

| 契约 | 决策 | 对本设计的影响 |
|------|------|--------------|
| [ADR-0011](../../adr/ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md) v1.5 | A+C 组合（accepted）；C = 审查臂查系统真实状态；**C 触发 = A 落地后或用户裁决** | 本批即出路 C 实施（用户指令触发）；B 暂缓 |
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 候选吸收三问 | 本批正式执行三问审核（见 §6） |
| [step-gate DESIGN](../../spec/step-gate/DESIGN.md) v1.0 | decision schema + 锚点规则 + STEP_SEQUENCE | verify-anchor 复用 ANCHOR_RE 解析 + decision 提取逻辑 |
| [step-gate-enforcement DESIGN](../../spec/step-gate-enforcement/DESIGN.md) v1.0 | 出路 A 落地形态（只读命令 + hook） | 本批参照其形态（只读零副作用 + 复用既有逻辑 + selftest 扩展） |
| [SPEC_PROCESS](../../SPEC_PROCESS.md) v1.4 | RULE-1/5 独立 pass | RULE-1 补充取证清单（§5 本设计修订点） |

## 3. 架构设计

### 3.1 整体架构

```
审查臂（RULE-1/5 独立 pass）
      │  输入 = 事件流 + 系统真实状态
      ▼
spec_runner.py verify-anchor --session <sid>（机械取证，只读）
      │  ① read(sid) 过滤 decision 事件 → 提取全部 evidence[].anchor
      │  ② 解析锚点：path §N / path#Lxx / URL
      │  ③ 逐条核查：文件存在 + 章节标题精确匹配 / 行号上界
      ▼
取证报告（exit 0/1/2）+ 审查臂人工对照 git diff/status
```

### 3.2 模块划分

| 模块 | 职责 | 依赖 |
|------|------|------|
| `cmd_verify_anchor`（spec_runner 新子命令） | session → 锚点提取 → 真实性核查 → 分级报告 | stdlib only |
| `_resolve_anchor`（内部函数） | 锚点解析：`path §N` / `path#Lxx` / URL 三形态 → (path, kind, loc) | re |
| `_check_section` / `_check_line`（内部函数） | 章节标题精确匹配 / 行号上界 | Path / re |
| SPEC_PROCESS RULE-1 取证清单（文档修订） | 独立 pass 审查输入 = 事件流 + verify-anchor + git 状态 | — |

### 3.3 数据流

- 写：无（本批零写入，只读取证——P-022 教训）
- 读：session JSONL（decision 锚点）+ 文件系统（文件存在/章节/行号）

## 4. 接口定义

### 4.1 spec_runner 新子命令 `verify-anchor`

```
python tools/spec_runner/spec_runner.py verify-anchor --session <sid>
```

- `--session`：必填，目标 session
- 流程：
  1. `read(sid)` 过滤 `event=="decision"` → 提取每条 `metadata.evidence[].anchor`
  2. 锚点解析（三形态）：
     - `path §N`（N = 数字+点序列，如 `3.5`）→ 章节引用
     - `path#Lxx`（xx = 正整数）→ 行号引用
     - `https?://...` → URL（外部证据，本地不可核 → soft）
     - 其他 → 形态不可解析（hard，因为 ANCHOR_RE 应已拦截——防御性）
  3. 真实性核查（`path` 相对仓库根解析，仓库根 = spec_runner.py parents[1]）：
     - **文件存在**：`(ROOT_REPO / path).is_file()`，否则 hard
     - **章节 §N**：文件全文 `^#{1,6}\s+<N>(?:\s|$)` 精确匹配（`3.5` 只匹配标题 token `3.5`，不匹配 `3.5.1`；`3` 不匹配 `3.5`）——否则 hard
     - **行号 #Lxx**：`len(content.splitlines()) >= xx`——否则 hard
  4. 分级报告：hard 汇总 → exit 1；soft（URL/不可解析）汇总 → exit 2；全真实 → exit 0
- **只读**：不创建/修改 session，无 git 操作

### 4.2 SPEC_PROCESS RULE-1 取证清单（修订）

RULE-1 条目追加取证要求（独立 pass 执行时）:

> 独立 pass 取证清单（P-025 出路 C 增补）：审查输入 = ① 事件流（session JSONL，含 decision 事件）② `verify-anchor --session <sid>` 取证输出 ③ git diff/status 系统状态对照。
> - 锚点真实性：以 verify-anchor 输出为准，不信自报形态通过
> - 纯登记型批次（零代码变更）：查证范围 = 锚点文档存在 + 章节真实 + session 内容与文档状态一致（如声称版本与 front-matter version 匹配）；**无 diff 为合法态**，不判违规
> - verify-anchor 只验证「锚点位置可达」，不验证「断言内容对错」——语义真实性由 RULE-5 异基座审查把关

## 5. 替代方案

### 方案 C1（选择）：spec_runner 新命令 verify-anchor + SPEC_PROCESS 修订

- 优点：判定逻辑在 runner（通用、可测、stdlib only）；复用 ANCHOR_RE/cmd_gate_step 既有锚点逻辑；只读零副作用；审查臂有机械取证通道
- 缺点：两处改动（命令 + 文档规则）
- 选择理由：与出路 A 同构（命令承载机械判定 + 契约层规则）；符合 spec_runner「执行层唯一载体」惯例

### 方案 C2（备选）：纯审查臂人工取证（无命令）

- 优点：零代码改动
- 缺点：审查臂逐条人工核锚点 = 高成本 + 不可重放（无 E1 取证产物）；与「审查降本」「机械取证」方向背道而驰
- 否决理由：C 的机械可核面（锚点真实性）明确存在，人工放弃 = 表演空间未压缩

### 方案 C3（否决）：verify-anchor 并入 step-gate（加 --verify 旗标）

- 优点：命令面收敛
- 缺点：step-gate 语义 = 流程完整性校验（schema/秩序/锚点形态）；真实性核查 = 审查取证——职责不同（本批「审查输入升级」vs step-gate「流程门禁」）；混入后 step-gate exit 语义膨胀（被 step-enforce 复用，动一发牵全身）
- 否决理由：职责分离（校验 vs 取证），独立命令更清晰

## 6. ADR-0010 懒加载三问审核（正式执行）

| 问 | 审理 | 结论 |
|----|------|------|
| **Q1 放哪层** | verify-anchor = spec_runner 新子命令——**Layer-1 工具层**（审查臂激活时取证）；契约/规则 = Layer-0（ADR-0011 + SPEC_PROCESS RULE-1，纯文档消费者零工具依赖可用） | **Layer-1**（实现）+ **Layer-0**（契约） |
| **Q2 激活条件** | **已激活**：用户裁决触发（ADR-0011 L113「C 的触发 = A 落地后或用户裁决」）+ 用户指令「按照吃狗粮执行出路 C」——本批即激活实施 | **激活中**（非触发驱动候选，是既定决策实施） |
| **Q3 未激活副作用** | 实施前零足迹（命令不存在即零成本）；激活后 = 审查臂主动调用的取证命令（对不调用批次零影响）——副作用为**期望的审查能力**，非意外污染 | **0**（实施前）→ **期望副作用**（激活后） |

**边界声明**：本设计适用对象 = 出路 C 实施物（命令 + 规则修订）；契约层（ADR-0011 A+C 决策）为既有 accepted 资产，不重审。

## 7. 错误处理

| 场景 | 处理 |
|------|------|
| session 不存在 | exit 1 +「no such session」 |
| session 无 decision 事件 | exit 1（无锚点可验） |
| 锚点指向文件不存在 | hard → exit 1，列文件路径 |
| 锚点章节标题不存在 | hard → exit 1，列 §N 与文件 |
| 锚点行号越界 | hard → exit 1，列 Lxx 与总行数 |
| 锚点为 URL（外部证据） | soft → exit 2（本地不可核，人工/审查臂处理） |
| JSON 损坏行 | 跳过 + 警告计入违规（exit ≥ 1） |

## 8. 对实施的输入

### 8.1 关键约束

1. **只读零副作用**（P-022 教训）：verify-anchor 不创建/修改 session、无 git 操作、不写文件
2. **判定全机械**：文件存在 / 章节标题精确匹配 / 行号上界，无启发式；§3 精确匹配不命中 §3.5
3. **兼容既有命令面**：run/gate/status/replay/fork/step-gate/step-enforce 行为逐字节不变（I-4 三通道对比实证）
4. **仓库根解析**：锚点路径相对仓库根（spec_runner.py parents[1]），与既有锚点写法（`spec/...` 前缀）一致
5. selftest 覆盖：真实锚点 pass / 文件不存在 fail / 章节不存在 fail / 行号越界 fail / URL soft / §3 不命中 §3.5

### 8.2 验证计划

- selftest 增 F30-F34：verify-anchor 五场景（真实 / 文件缺失 / 章节缺失 / 行号越界 / URL soft + §3≠§3.5 精确性）
- 三通道复跑：dc-validator / m7-stats / repo-stats 全绿（spec/ 新 feature 目录 → repo-stats 对账）
- **吃狗粮实证**：本批（P-025）decision 锚点自身过 verify-anchor → exit 0；历史 session（p020/p023/p024）跑 verify-anchor 暴露既有表演空间 → 取证修正或登记

---

**Review 签字**: _________ 日期: _________
