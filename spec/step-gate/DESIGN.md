# 设计文档：每步决策产物管线（step-gate，P-020）

---
id: step-gate-DESIGN
type: design
version: 1.0
status: draft
date: 2026-09-08
depends: [step-gate-CHECKLIST, community-ecosystem-RESEARCH, FWK-DECISION-RECORD, spec-runner-DESIGN, ADR-0010]
upstream: null
---

> **Feature**: step-gate —— 每步决策产物管线（P-020，CER §3.5 裁定「可行且优先」）
> **创建日期**: 2026-09-08
> **状态**: 草稿
> **Spec 步骤**: Step 3-4
> **基于调研**: [COMMUNITY_ECOSYSTEM_RESEARCH.md](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) §3.5 / [STEP_GATE_CHECKLIST.md](./STEP_GATE_CHECKLIST.md)（三问门禁 8/8 通过）
> **前提**: P-020 已通过 ADR-0010 三问门禁（懒加载审核 8 子项全过，获准立项）——见 [STEP_GATE_CHECKLIST.md](./STEP_GATE_CHECKLIST.md) §2

---

## 1. 设计目标

实现 「决策产物管线」：十步 Spec 流程**每步完成时强制产出一条决策记录事件**（`event: "decision"`，复用 FWK-DECISION-RECORD 八字段）写入 Spec_Runner 事件流；新增 `step-gate` 机械校验命令，保障「每个已登记 step_id 恰一条 decision 事件 + step 序单调递增 + evidence 非空」。目标 = **「声明=重数」从文档层推广到流程执行层**（CER §3.5）——下一轮审查（RULE-1/RULE-5 臂）以事件流为唯一输入，而非全文重读。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| 每步产出 decision 事件入 Spec_Runner 流，step-gate 机械校验三条件（字段完整/evidence 非空/每步恰一条单调） | `event: "decision"` 复用 FWK-DECISION-RECORD 八字段；新命令 `step-gate` | CER §3.5 管线形态 |
| FWK-DECISION-RECORD 八字段本身无 evidence/step → 落通用 metadata 通道 | step_id/evidence/severity 落 `metadata: Dict`（P-016 severity 同通道先例） | CER §3.5 v1.2 精化 |
| gate 校验"引用可解析"过严会阻塞流程 | 分级校验：硬性（schema 完整+evidence 非空）exit 1；软性（锚点可解析性）exit 2 提示人工复核 | CER §5.3 风险 |
| 决策记录从档案提升为驱动执行的输入（ARC/ADR Kit/本框架三方收敛） | step 序表驱动：每步一条事件链 = 下一轮审查唯一输入 | CER §3.4.1 每步决策产物管线行 |

### 2.2 相关 ADR / 契约

| 契约 | 决策 | 对本设计的影响 |
|------|------|--------------|
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 三问门禁 | step-gate 实现落 Layer-1（tools/spec_runner/），契约 Layer-0（FWK-DECISION-RECORD），单向依赖（契约→runner 零引用，Q1c 已证） |
| [FWK-DECISION-RECORD](../../docs/DECISION_RECORD_CONTRACT.md) | 八字段 + I-1~I-4 | decision 事件 input 主体 = 八字段 dict；severity 无损分流（P1/P2/P3 字符串入 metadata，confidence 不承载严重性） |
| [FWK-ASSERTION](../../docs/ASSERTION_EVIDENCE_FRAMEWORK.md) | E1-E4 证据分级 | evidence 数组含等级标注 + 锚点；等级标注由生成端负责，step-gate 仅机械检查"非空 + 可解析" |
| [spec-runner DESIGN](../spec-runner/SPEC_RUNNER_DESIGN.md) | L1/L2/L3/L7 事件流不变式 | decision 事件 append-only（L2）；不引入新状态（step 连续性由 step_id 显式标识，v1.2 精化） |

## 3. 架构设计

### 3.1 整体架构

```
十步流程每步完成 ──▶ 生成端写 decision 事件（EventWriter，append-only）
                          │  event: "decision"，input = FWK-DECISION-RECORD 八字段 dict
                          ▼
                   Spec_Runner 事件流（session JSONL）
                          │
                          ▼
                step-gate 命令（机械校验，三类规则）
                         ├─ 硬性：schema 字段完整 + evidence 非空 → exit 1
                         ├─ 软性：锚点可解析性 → exit 2 人工复核
                         └─ 秩序：step_id 单调 + 每步恰一条
                          │
                          ▼
             下一轮审查（RULE-1 时序独立 / RULE-5 异基座）= 事件流唯一输入
```

### 3.2 模块划分

| 模块 | 职责 | 输出 | 依赖 |
|------|------|------|------|
| EVENTS 扩展 | `EVENTS` 元组 + `"decision"` | 允许写 decision 事件 | stdlib |
| decision 写入（生成端） | `EventWriter.append(event="decision", input=八字段dict)` | 事件流行 | append 校验（source/event 白名单） |
| `cmd_gate_step` | 校验三类规则，exit 分级 | exit 0/1/2 | 事件流 read |

### 3.3 data 流

- 写：生成端 → `append(sid, "assistant", "decision", input_={八字段含 metadata.step_id/evidence})` → JSONL 追加
- 读：`cmd_gate_step(sid)` → `read(sid)` 过滤 `event=="decision"` → 逐条校验 → 汇总报告

## 4. 决策事件 schema（复用 FWK-DECISION-RECORD 八字段，Q1a 判定锚定）

`event: "decision"` 行结构（十字段 + input 扩展，断裂式隔离到 input）：

```json
{
  "ts": "...", "seq": 7, "session": "specwf-xxx-20260908", "source": "assistant",
  "model": null, "provider": null,
  "event": "decision",
  "input": {
    "category": "feature-design",
    "scenario": "P-021 桥设计需要决策落位",
    "reasoning": "CER C-01 裁定 Layer-0；替代方案 A/B/C 对比",
    "outcome": "采用方案 A：根 AGENTS.md 单一文件",
    "confidence": 0.9,
    "entities": ["AGENTS.md", "spec/agents-md-bridge"],
    "decision_maker": "scott+trae",
    "metadata": {
      "step_id": "design",
      "step_seq": 2,
      "evidence": [{"grade": "E1", "anchor": "CER §3.1 C-01"}],
      "severity": null
    }
  },
  "output": null, "gate": null
}
```

**字段约束**（对齐 FWK-DECISION-RECORD I-1~I-4）：
- 必填（硬性）：category / scenario / reasoning / outcome / confidence + metadata（含 step_id / evidence 数组非空）
- 可选：entities / decision_maker / metadata.severity / valid_from / valid_until
- severity 若存在必须为 "P1"/"P2"/"P3" 字符串（D2 无损分流，禁止浮点编码）

## 5. step 序表（Q2b 全链映射——十步流程 → step_id）

| step_id | 覆盖 Spec 步骤 | 事件时机 |
|---------|---------------|---------|
| `research` | Step 1-2（调研 + Review） | 调研文档完成、Step 2 门禁通过后 |
| `design` | Step 3-4（设计 + Review） | DESIGN 完成、Step 4 门禁通过后 |
| `implement` | Step 5-6（实施 + Review） | IMPLEMENTATION 完成、Step 6 门禁通过后 |
| `verify` | Step 7-8（验收 + 独立 pass） | CHECKLIST 完成、独立 pass 后 |
| `finalize` | Step 9-10（落档收束） | PROGRESS/CODE_WIKI 收束后 |

**连续性规则**：每条 decision 事件 `metadata.step_seq` 必须严格递增且等于其在 STEP_SEQUENCE 中的顺序；每个 step_id 在单 session 内恰一条（不可跳步、不可重复、不可回退）。软性例外：独立 feature 可选择子集（如小流程裁剪 DESIGN/IMPL/CHECKLIST 两件套）——此时 step-gate 接受"序表前缀子集"，但跳过的步骤后不可再补（已登记 step 单调）。**实施批复核时以首个真实 feature 全流程运行实证（Q2b E2）**。

## 6. step-gate 命令设计

### 6.1 命令行

```
python tools/spec_runner/spec_runner.py step-gate --sid <session-id> [--expect design,implement]
```

- `--sid`：必填，目标 session
- `--expect`：可选，期望 step_id 列表（默认 = 全部 STEP_SEQUENCE；给出则校验"恰好包含期望子集且每步恰一条"）

### 6.2 校验规则（三类，exit 分级）

| 类 | 规则 | 违规 → |
|----|------|--------|
| 硬性-1 schema 完整 | 每条 decision 行 input 含必填八字段 + metadata.step_id/step_seq + evidence 非空数组 | exit 1 + 列出缺失字段 |
| 硬性-2 秩序 | step_id ∈ STEP_SEQUENCE；step_seq 严格递增；step_id 每步 ≤1 条且无跳步（若给出 --expect，则恰好含期望子集） | exit 1 + 列违规事件序号 |
| 软性-3 锚点可解析 | evidence[].anchor 形如 `path#Lx` / `URL` / `spec/...§N`（正则形态） | exit 2 + 列可疑锚点（提示人工复核） |

**整体判定**：`exit 0` = 全链完整；`exit 1` = 硬性违规（阻断进入下一步）；`exit 2` = 软性存疑（人工复核）。无 decision 事件 = exit 1（空流 = 未执行决策记录纪律）。

### 6.3 与既有命令面整合

新增子命令 `step-gate`；不影响 run/gate/status/replay/fork（Q3a：未调用零副作用；不加入默认 gate hook 链——触发驱动，Q3c）。

## 7. 不变式（ADD 审计依据）

1. **I-1 复用不新建**：decision 事件不引入 FWK-DECISION-RECORD 八字段之外的顶层结构（metadata 通道为契约既有例外）。
2. **I-2 append-only**：decision 事件为追加写入（L2），无改写路径；`--expect`/`step-gate` 均只读。
3. **I-3 单向依赖**：契约文档 → runner 零引用；runner → 契约单向（设计/文档级，不 import）。
4. **I-4 零激活副作用**：未调用 step-gate 时，EVENTS 扩展为唯一变更（校验白名单放宽）；run/gate/status/replay/fork 行为逐字节不变——三通道对比实证（Q3c 复跑）。

## 8. 替代方案

### 8.1 方案 A：事件流承载 + 独立 step-gate 命令（选择）
- 描述：decision 事件复用既有 JSONL 流，新增只读校验命令。
- 优点：复用 L1/L2 不变式；零新存储；校验与写分离（校验只读）。
- 缺点：校验需全量读流（O(n)，n 小型可忽略）。
- **选择理由**：与 CER §3.5 采纳路径完全一致（Spec_Runner 增 decision 事件类型 + step-gate 命令）。

### 8.2 方案 B：独立 decision.jsonl 分离流（否决）
- 描述：决策记录单独一个 JSONL 文件。
- 优点：流隔离。
- 缺点：破坏单流状态（L1 唯一 state）；clone/fork 需双流同步；与 append-only 单文件纪律冲突。
- **否决理由**：I-1/L1 不变式——单事件流是 runner 和根基。

### 8.3 方案 C：gate 子类型（--type decision-check）扩展现有 gate 命令（否决）
- 描述：复用 cmd_gate 加类型参数。
- 缺点：cmd_gate 语义 = 执行外部命令 + verdict；decision 校验是流内读取，语义错配；透传 exit 会被 subprocess 包装。
- **否决理由**：职责混淆（执行器 vs 校验器）——独立命令更清晰。

## 9. 错误处理

| 错误场景 | 处理 |
|---------|------|
| session 不存在 | exit 1 + "no such session"（打印用法） |
| decision 事件缺字段 | exit 1 + 逐条列缺失字段 |
| evidence 空 | exit 1（硬性非空） |
| 锚点形态存疑 | exit 2 + 列可疑清单 |
| JSON 损坏行 | 跳过 + 警告计入违规（exit ≥ 1） |

## 10. 对实施的输入

### 10.1 关键约束

1. 修改点收敛：`EVENTS` 元组 + `cmd_gate_step()` + `build_parser()` 子命令 + `run_selftest()` 增 fixture——**不触碰** run/gate/status/replay/fork 逻辑。
2. `--expect` 默认 = 全序；命令只读不写。
3. selftest 覆盖：八字段完整通过 / 缺字段 fail / 跳步 fail / 不乱序 / 锚点软提示 / 空流 fail。

---

**Review 签字**: _________ 日期: _________