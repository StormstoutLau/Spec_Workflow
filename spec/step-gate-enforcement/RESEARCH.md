# 调研文档：step-gate 流程强制（出路 A 实施）

---
id: step-gate-enforcement-RESEARCH
type: design
version: 1.0
status: verified
date: 2026-09-09
depends: [ADR-0011, step-gate-DESIGN, ADR-0010, SPEC-PROCESS]
upstream: null
---

> **Feature**: step-gate 流程强制（出路 A——P-024）
> **创建日期**: 2026-09-09
> **状态**: draft
> **Spec 步骤**: Step 1-2
> **基于**: [ADR-0011](../../adr/ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md) v1.4（accepted，决策 = A+C 组合；A = 流程强制）——**失效条件已命中**（P-021/022/023 三连批应走未走，E1 实证 + 样本 ㉚）

---

## 1. 调研目标

**核心问题**（基于 ADR-0011 出路 A 形态定义，实施前细化）:
1. 出路 A 的**可机械判定形态**是什么——「把 session 必须存在 + decision 链完整固化为进入下一 spec step 的硬性入口」在本仓 pre-commit 基建上如何落地？
2. 「应走管线批次」判定准则（ADR-0011 v1.3 补）如何**机械化**——hook 从提交内容中提取 P 编号与 step 进度的可靠路径？
3. 强制粒度——**批次级**（有决策流即可）还是**步骤级**（每步恰一条）？最小有效形态与边界在哪？

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| Read | 现状资产核对 | spec_runner.py cmd_gate_step / .pre-commit-config.yaml / PROGRESS 行 / ADR-0011 判定准则 |
| Grep | 模式提取 | PROGRESS P 行 ↔ spec/<feature>/ 映射 / session 命名 |
| E1 机械取证 | 失效实证 | sessions/ 目录 decision 计数（P-021/022/023 全 0，仅 p020 系列 4+5 条） |

### 2.2 调研范围

- **前置资产**：ADR-0011（出路 A 形态 + 判定准则 + P-022 教训）、step-gate DESIGN v1.0（管线设计）、spec_runner.py v1.2.0（step-gate 命令）、.pre-commit-config.yaml（三 hook 结构）
- **社区参照**：ADR-0011 §4 已登记（SpecD 状态机 / Superpowers 强制管线 / MCP Task Orchestrator 阻塞进展 / StepProof hooks 唯一硬强制）——**不重复调研，直接引用**
- **排除**：出路 B/C 实施（B 排除暂缓、C 待 A 落地，本批不做）

## 3. 调研发现

### 3.1 现状资产核对（E1 机械取证）

**spec_runner.py v1.2.0 已有能力**（`cmd_gate_step`，L184-239）：
- `STEP_SEQUENCE = (research, design, implement, verify, finalize)`（L175）
- `DREQ` 八字段必填 + `metadata.step_id/step_seq/evidence`（L176/L203-207）
- 硬性-1 schema / 硬性-2 秩序 / 软性-3 锚点三类规则，exit 0/1/2（L228-239）
- `--expect` 可校验全链一致性（L222-224）
- **缺口**：无「session 存在性」检查入口（session 不存在时 read 返回空 → 无 decision → exit 1，但错误语义混在"纪律未执行"里）；**无「指定 P 编号 → 找对应 session」的能力**

**.pre-commit-config.yaml 三 hook 结构**（repo-local + language: system）：
- `dc-validator`（files: `\.md$`）/ `m7-stats`（files: `^docs/M7_EVIDENCE_LOG\.md$`）/ `repo-stats`（files: `^(CODE_WIKI\.md|README...|docs/|spec/|adr/|scripts/)`）
- **模式可循**：entry 走 `python scripts/xxx.py`，files 收窄作用域

**PROGRESS P 行 ↔ feature 目录映射**（Grep 实证）：
- 模式：验收列含 `../../spec/<feature>/` 链接 + 行首 `| P-0xx |`
- 例：P-023 行含 `[drift-gate 两件套](../../spec/drift-gate/)`；P-020 行含 `[step-gate 三件套](../../spec/step-gate/DESIGN.md)`
- **机械可提取**：hook 可从 PROGRESS 行正则提取 `P-(\d{3})` 与 `spec/([a-z0-9-]+)/` 的映射

**session 命名约定**（sessions/ 实证）：
- 现有 = `specwf-p020-20260908v2.jsonl`、`p009-first-run-001.jsonl`、`specwf-probe-20260907.jsonl`
- **P 批次 session 命名可锚定**：`specwf-p0xx-*` 前缀（P-020 先例）

**失效实证**（ADR-0011 样本 ㉚）：P-021/022/023 均无 session（sessions/ 下零 `p021*`/`p022*`/`p023*` 文件）——「无触发器」结构根因直接支持 pre-commit 强制。

### 3.2 判定准则机械化（ADR-0011 v1.3 补落地）

ADR-0011 判定准则：「应走管线」= ① PROGRESS 登记新 P 编号 ② 关联产出含 RESEARCH/DESIGN/IMPL/CHECKLIST 文档之一 ③ 满足任一即应走；适用于 P-020 起新批次。

**机械化方案**：hook 在 commit 时对**本次变更文件集合**做两步判定：
1. 变更文件含 `spec/<feature>/*.md`（RESEARCH/DESIGN/IMPL/CHECKLIST 之一，文件名匹配）
2. 从 PROGRESS 行提取该 feature 的 P 编号
3. 命中任一 → 该 P 批次「应走管线」→ 强制 session 存在 + decision 非空

**边界**：纯文档批（无 spec/<feature>/ 产出，如 DEV-LOG 追记）不触发——与准则②「关联产出含四文档之一」一致。变更不涉及 spec/<feature>/ 的 P 行（如 PROGRESS 状态字更新）——不触发（无新产出）。

### 3.3 强制粒度分析（批次级 vs 步骤级）

| 粒度 | 机制 | 优点 | 缺点 | 判定可靠性 |
|------|------|------|------|-----------|
| **批次级**（有决策流即可，非空 + step-gate 基础校验） | hook 要求 `specwf-p0xx-*` session 存在 + ≥1 条合法 decision | 实现简单、判定可靠（存在性 + 非空 = 纯机械）；消除"零决策流"主失效 | 不保证"每步恰一条"（步骤级纪律仍靠 step-gate 手动调用） | **高**（session 文件名 + decision 计数 = E1 可证） |
| **步骤级**（每步恰一条，--expect 全链） | hook 要求 decision 链覆盖当前进度 step | 完整实现「每步强制」 | **hook 无法可靠推断"当前在哪个 step"**（一次 commit 可能跨步骤或先提交文档后写 decision）；误拦截风险高 | 低（step 推断 = 启发式，不可靠） |

**选择批次级**为最小有效形态：消除主失效（零决策流），判定全机械（存在性 + 非空），不引入启发式 step 推断。步骤级纪律由 step-gate 命令在每步收尾时调用（已有能力），本批不强行合并。

### 3.4 与 P-022 教训的对齐（ADR-0011 成本表已登记）

P-022 教训（gate auto-commit F1/F2/F3）：cwd 硬编码 / 全目录 add / 无条件提交——hook 级门控典型副作用。本批 hook 设计必须：
- **只读不写**：step-enforce 只读 sessions/ + PROGRESS，绝无 git 操作（不触碰 git_snapshot）
- **无副作用**：不创建/修改任何文件（区别于 P-022 的 git_snapshot 提交副作用）
- **白名单收窄**：files 收窄至 `spec/` + PROGRESS（避免全目录扫描）

## 4. 综合分析

### 4.1 关键发现总结

1. **形态确定**：pre-commit 第四 hook `step-enforce`（repo-local + language: system，对齐三 hook 先例），批次级强制 [置信度: ★★★★★]
2. **判定全机械**：session 存在性（文件名前缀 `specwf-p0xx-`）+ decision 非空（计数）+ PROGRESS↔feature 映射（正则提取）——无启发式 [置信度: ★★★★☆]
3. **强制边界清晰**：只对"应走管线"变更（spec/<feature>/ 四文档之一）触发；纯文档批/追记批不触发 [置信度: ★★★★☆]
4. **实现收敛**：spec_runner 增 `step-enforce --pid` 子命令（session 定位 + step-gate 复用）+ hook 薄壳（PROGRESS 解析 + 调用）[置信度: ★★★★☆]
5. **P-022 教训内化**：只读零副作用，不触碰 git_snapshot [置信度: ★★★★★]

### 4.2 技术 landscape

本仓已有三层校验（dc-validator 契约 / m7-stats 账本 / repo-stats 视图）+ spec_runner step-gate 命令。出路 A 是**流程执行层的第四道机械防线**——把「决策流存在」从纪律（值守）提升为提交门禁（强制）。社区参照（SpecD 状态机 / StepProof hooks 唯一硬强制）已验证此方向。

### 4.3 研究空白

- 步骤级强制的 step 推断可靠性问题（hook 无法知"当前步"）——留待后续（出路 A 批次级落地后评估是否需要 + 如何可靠推断）
- 历史批次（P-018/019 等 pre-step-gate 批次）不追溯——判定准则已限定 P-020 起

## 5. 幻觉抑制审查（Step 2 Review）

### 5.1 文献验证

本批为仓内实施调研，无外部文献引用（社区参照直接引用 ADR-0011 已登记的结论，不重复取证）。断言全为仓内 E1 机械取证。

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| spec_runner 已有 cmd_gate_step + STEP_SEQUENCE + --expect | spec_runner.py L175-239 直读 | ✅ E1 |
| 三 hook 结构（repo-local + language: system + files 收窄） | .pre-commit-config.yaml 直读 | ✅ E1 |
| PROGRESS P 行 ↔ spec/<feature>/ 映射可正则提取 | PROGRESS.md 行模式 grep | ✅ E1 |
| session 命名前缀 `specwf-p0xx-` | sessions/ 目录枚举 | ✅ E1 |
| P-021/022/023 零 session（失效实证） | sessions/ decision 计数 | ✅ E1 |

### 5.3 待修正项

- 无（调研收束，实现细节入 DESIGN）

## 6. 对设计的输入

### 6.1 可用的技术方案

- 方案 A1（选择）：spec_runner 新命令 `step-enforce --pid P-0xx` + pre-commit 第四 hook（薄壳解析 PROGRESS + 调用）
- 方案 A2（备选）：纯 hook 脚本（不入 spec_runner）——优点零改动 runner；缺点逻辑分裂（判定在 hook、校验在 runner 两处）
- 方案 A3（否决）：步骤级强制——step 推断不可靠（§3.3）

### 6.2 关键约束

1. **零副作用**（P-022 教训）：step-enforce 只读，不创建/修改/提交任何文件
2. **判定全机械**：无启发式 step 推断
3. **files 收窄**：hook 作用域 = `spec/` + `docs/PROGRESS.md`（避免全目录）
4. **与既有命令兼容**：不改变 run/gate/status/replay/fork/step-gate 行为（I-4）
5. 遵守 ADR-0010 三问（DESIGN 阶段执行）

### 6.3 风险

- hook 误拦截：变更文件在 spec/ 但非四文档（如 spec/ 下 CHANGELOG）→ files 正则收窄到四文档文件名
- PROGRESS 行提取失败（P 编号与 feature 无直接链接的行）→ 降级为提示（exit 2）而非阻断，避免误伤
- 批次跨多次 commit：首批 commit 无 RESEARCH 产出（先登记 P 行）→ 只触发 session 存在性（decision 可后续补）？——**需 DESIGN 裁定**：本批设计为「commit 时命中应走管线 → 要求 session 存在 + decision ≥1」，若先写 PROGRESS 行后写文档，首次 commit 即被要求有 session——这是**期望行为**（开档即入流），不构成误伤

## 7. 参考文献

- [ADR-0011](../../adr/ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md) v1.4（accepted：决策 A+C / 判定准则 / P-022 教训）
- [step-gate DESIGN](../../spec/step-gate/DESIGN.md) v1.0（管线设计）
- [P-022 缺陷修复](../../spec/defect-fixes/DESIGN.md) v1.2（git_snapshot 教训）
- .pre-commit-config.yaml（三 hook 结构）
- tools/spec_runner/spec_runner.py v1.2.0（cmd_gate_step / sessions_dir）

---

**Review 签字**: _________ 日期: _________
