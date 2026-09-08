# 设计文档：step-gate 流程强制（出路 A——批次级提交门禁）

---
id: step-gate-enforcement-DESIGN
type: design
version: 1.1
status: verified
date: 2026-09-09
depends: [step-gate-enforcement-RESEARCH, ADR-0011, ADR-0010, step-gate-DESIGN, SPEC-PROCESS]
upstream: null
---

> **Feature**: step-gate 流程强制（P-024）
> **创建日期**: 2026-09-09
> **状态**: draft
> **Spec 步骤**: Step 3-4
> **基于调研**: [RESEARCH](./RESEARCH.md) v1.0（形态 = 批次级强制 + 判定全机械 + P-022 教训内化）

---

## 1. 设计目标

把「应走管线批次必须存在决策流」从**值守纪律**（生成端自觉调用 step-gate）固化为**提交门禁**（pre-commit hook 强制）：当一次提交变更了应走管线文件（`spec/<feature>/` 四文档之一），该 feature 对应 P 批次必须已存在 `specwf-p0xx-*` session 且 decision 链非空通过 step-gate 基础校验，否则阻断提交（exit 1）。

**目标 = 消除 ADR-0011 已实证的主失效**：P-021/022/023 三连批零 decision 流（样本 ㉚）。强制粒度 = **批次级**（存在 + 非空），步骤级纪律仍由 `step-gate --expect` 每步收尾调用（既有能力，不合并）。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| spec_runner 已有 cmd_gate_step（schema/秩序/锚点三类 + --expect） | step-enforce 复用 cmd_gate_step 校验逻辑，新增 session 定位层 | RESEARCH §3.1 |
| PROGRESS P 行 ↔ spec/<feature>/ 映射可正则提取 | hook 从变更文件 → feature → P 编号机械映射 | RESEARCH §3.2 |
| session 命名前缀 `specwf-p0xx-` 可锚定 | step-enforce 按前缀定位 session | RESEARCH §3.1 |
| 步骤级 step 推断不可靠 | 选**批次级**（存在 + 非空），不引入启发式 | RESEARCH §3.3 |
| P-022 教训（hook 门控副作用：cwd/add 范围/无条件提交） | **只读零副作用**：不触碰 git、不创建文件 | ADR-0011 §2 / P-022 |

### 2.2 相关 ADR / 契约

| 契约 | 决策 | 对本设计的影响 |
|------|------|--------------|
| [ADR-0011](../../adr/ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md) v1.4 | 决策 = A+C 组合（accepted）；A = 流程强制 | 本批即出路 A 实施；判定准则（§应走管线）机械化 |
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 候选吸收三问 | 本批正式执行三问审核（见 §6） |
| [step-gate DESIGN](../../spec/step-gate/DESIGN.md) v1.0 | step-gate 命令 + STEP_SEQUENCE | step-enforce 复用其校验；不改变既有命令面（I-4） |
| [P-022](../../spec/defect-fixes/DESIGN.md) v1.2 | git_snapshot opt-in + 精确 sid + 零无条件提交 | step-enforce 只读，无 git 操作 |

## 3. 架构设计

### 3.1 整体架构

```
commit 变更文件
      │  files: ^spec/（触发面）
      ▼
scripts/step_enforce.py（hook 入口，本仓薄壳）
      │  ① 提取变更中 spec/<feature>/(RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST*).md → feature 集
      │  ② 读 docs/PROGRESS.md 正则提取 feature ↔ P-0xx 映射
      │  ③ 对每个 P 调用：spec_runner.py step-enforce --pid P-0xx
      ▼
spec_runner.py step-enforce（通用校验，新子命令）
      │  ① sessions_dir 前缀匹配 specwf-p0xx-*.jsonl
      │  ② 无匹配 session → exit 1（阻断）
      │  ③ 复用 cmd_gate_step 校验（决策非空 + 无硬性违规）→ exit 0/1/2
      ▼
pre-commit 门禁结果（阻断/放行）
```

### 3.2 模块划分

| 模块 | 职责 | 依赖 |
|------|------|------|
| `cmd_step_enforce`（spec_runner 新子命令） | 给定 `--pid`，前缀定位 session，复用 step-gate 校验 | spec_runner（stdlib only） |
| `scripts/step_enforce.py`（hook 入口） | 变更文件 → feature → P 映射 + 循环调用 runner | stdlib + PROGRESS.md 读取 |

### 3.3 数据流

- 写：无（本批零写入，只读校验——P-022 教训）
- 读：hook 读变更文件列表（pre-commit 传入）+ PROGRESS.md（映射）+ sessions/（session 定位）

## 4. 接口定义

### 4.1 spec_runner 新子命令 `step-enforce`

```
python tools/spec_runner/spec_runner.py step-enforce --pid P-0xx [--session-name <specwf-p0xx-*>]
```

- `--pid`：必填，P 编号（如 P-024）——session 前缀锚点
- 定位：`sessions_dir()` 下文件名匹配 `^specwf-{pid.lower()}-` 的 jsonl（P-020 先例命名）；无匹配 → exit 1「无 session（决策记录纪律未执行）」
- 定位成功 → 复用 cmd_gate_step 校验逻辑（仅"非空 + 无硬性违规"判定，不强制 --expect 全链）→ exit 0/1/2
- **只读**：不创建/修改 session，无 git 操作

### 4.2 pre-commit 第四 hook

```yaml
- id: step-enforce
  name: Step decision-stream enforcement (P-024, ADR-0011 A)
  entry: python scripts/step_enforce.py
  language: system
  files: ^spec/[a-z0-9-]+/(?:[A-Z0-9_]+_)?(?:RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST(?:_FUNC)?)\.md$
```

- `files` 收窄：仅四文档（RESEARCH/DESIGN/IMPLEMENTATION/CHECKLIST*，v1.1 起含 `[A-Z0-9_]+_` 前缀——P-003 命名约定前遗留的非标准命名文档，如 `COMMUNITY_ECOSYSTEM_RESEARCH.md` / `STEP_GATE_CHECKLIST.md`，均属应走管线交付物）——纯文档批、spec/ 下非四文档（如 CHANGELOG / `*_TEMPLATE.md` / `*_AUDIT.md` / PLAN）不触发
- entry 脚本逻辑：
  1. `sys.argv[1:]`（pre-commit 传入匹配文件）→ 提取 feature 名（`spec/<feature>/` 第二段）
  2. 读 `docs/PROGRESS.md`，正则提取 `P-(\d{3})` 行内是否含 `spec/<feature>/` 链接 → feature↔P 映射
  3. feature 无对应 P 行 → 降级 exit 2 提示（不阻断——避免 P 登记滞后的误伤）
  4. 有 P → 调用 `spec_runner.py step-enforce --pid P-0xx`，透传 exit

## 5. 替代方案

### 方案 A1（选择）：spec_runner 新命令 + hook 薄壳

- 优点：判定逻辑在 runner（通用、可测），hook 只做本仓映射；复用 cmd_gate_step；只读零副作用
- 缺点：两处代码（runner 命令 + scripts 脚本）
- 选择理由：分层清晰（通用校验 vs 本仓映射），符合 spec_runner 薄壳定位与三 hook 先例

### 方案 A2（备选）：纯 hook 脚本（不入 spec_runner）

- 优点：零改动 runner
- 缺点：校验逻辑复制在 hook（双源）；无法手动复用 step-enforce（CLI 缺位）；与"spec_runner 是执行层唯一载体"惯例冲突
- 否决理由：逻辑分裂

### 方案 A3（否决）：步骤级强制（每步恰一条 --expect 全链）

- 优点：最严格
- 缺点：hook 无法可靠推断"当前在哪个 step"（RESEARCH §3.3）；一次 commit 跨步骤/先文档后 decision 均误拦截
- 否决理由：判定不可靠，过度工程（批次级已消除主失效）

## 6. ADR-0010 懒加载三问审核（正式执行）

| 问 | 审理 | 结论 |
|----|------|------|
| **Q1 放哪层** | step-enforce = pre-commit hook + spec_runner 子命令——**Layer-1 工具层**（激活后常驻校验链）；契约/准则 = Layer-0（ADR-0011 + 本 DESIGN，纯文档消费者零工具依赖可用） | **Layer-1**（实现）+ **Layer-0**（契约） |
| **Q2 激活条件** | **已激活**：用户裁决 A+C 组合收口（ADR-0011 accepted）+ 失效条件命中（P-021/022/023 三连批，90 日窗口，E1）+ 用户指令「开启后续吃狗粮 spec 工作流」——本批即激活实施 | **激活中**（非触发驱动候选，是既定决策实施） |
| **Q3 未激活副作用** | 实施前零足迹（hook/命令不存在即零成本）；激活后 = hook 常驻 pre-commit（对"应走管线"变更阻断零决策流提交——副作用为**期望的强制行为**，非意外污染） | **0**（实施前）→ **期望副作用**（激活后） |

**边界声明**：本设计适用对象 = 出路 A 实施物（hook + 命令）；契约层（ADR-0011 判定准则）为既有 accepted 资产，不重审。

## 7. 错误处理

| 场景 | 处理 |
|------|------|
| session 不存在（应走未走） | exit 1 +「无 session：需先创建 specwf-p0xx-* 并写入 ≥1 decision」 |
| decision 链空 / 硬性违规 | exit 1（复用 cmd_gate_step 判定） |
| 锚点形态存疑 | exit 2（软性，人工复核） |
| PROGRESS 无该 feature 的 P 行 | exit 2 提示（不阻断——P 登记可能滞后于文档 commit） |
| spec_runner.py 不可达 | exit 1 + 安装指引（同 P-009 adapter RUNNER 探测语义） |

## 8. 对实施的输入

### 8.1 关键约束

1. **只读零副作用**（P-022 教训）：step-enforce 与 hook 均不创建/修改/提交文件
2. **判定全机械**：session 存在性 + decision 非空 + PROGRESS 映射，无启发式
3. **files 收窄**：hook 仅触发 `spec/<feature>/` 四文档
4. **兼容既有命令面**：run/gate/status/replay/fork/step-gate 行为逐字节不变（I-4 三通道对比实证）
5. selftest 覆盖：无 session fail / 空链 fail / 合法链 pass / 软性 exit 2 / PROGRESS 映射提取

### 8.2 验证计划

- selftest 增 F2x：step-enforce 四场景（无 session / 空链 / 合法 / 软性）
- 三通道复跑：dc-validator / m7-stats / repo-stats 全绿（hook 新增 = .pre-commit-config.yaml 变更 → repo-stats 对账）
- **吃狗粮实证**：本批（P-024）自身 commit 走 step-enforce 门禁——RESEARCH.md 首 commit 即要求 session 存在 → 自证

## 9. 追记（P-027 盲区修复，2026-09-09）

> 用户指令「登记并修复 step-enforce 的盲区」。

### 9.1 盲区登记（M7 样本 ㉛）

- **失效面**：v1.0 `files` 正则仅收四文档**精确名**（`RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST(_FUNC)?\.md$`），不匹配 P-003 命名约定前遗留的 `*_四文档` 前缀形态（`COMMUNITY_ECOSYSTEM_RESEARCH.md` / `STEP_GATE_CHECKLIST.md` 等）——**P-026 批次实际未被 hook 门禁强制**（吃狗粮手动补跑 step-gate 掩盖），应走管线批次可静默绕过门禁。
- **根因**：v1.0「files 收窄仅四文档」假设非四文档均非管线交付物，忽略遗留前缀命名；「四文档」判定以文件名精确匹配实现而非语义类型（RESEARCH/DESIGN/IMPLEMENTATION/CHECKLIST）匹配。
- **修复**：files 正则 + FEATURE_RE 扩展 `[A-Z0-9_]+_` 前缀（语义类型匹配）；**历史批次豁免**（P-020 前批次不追溯强制——决策流纪律 P-020 起建立，早于 P-020 的 feature 无 specwf session，强制即误伤）。
- **覆盖核对**：新纳入 15 feature 中 13 个为 P-020 前历史批次（豁免），仅 step-gate（P-020）/ community-ecosystem（P-026）纳入强制且均有 session（五场景验收 §8.2 见 P-027 记录）。
- **形态 II = 0**：机制覆盖盲区非字段级错误值，不入分桶（同 DIS-009 处置逻辑）。

### 9.2 版本说明

v1.0 → v1.1（§4.2 files 收窄说明 + 本追记）。PROGRESS P-024 行 / CODE_WIKI v1.27 历史叙事不回溯改写，P-027 行登记修复事实。

---

**Review 签字**: _________ 日期: _________
