# 设计文档：Spec_Runner 归巢实施批（P-019 spec-runner-homing）v1.0 (2026-09-08)

---
id: spec-runner-homing-DESIGN
type: design
version: 1.0
status: in-review
date: 2026-09-08
depends: [spec-runner-homing-RESEARCH, spec-runner-RESEARCH, langgraph-upgrade-RESEARCH]
upstream: null
---

> **Feature**: spec-runner-homing（PROGRESS P-019——Spec_Runner 从独立仓库 `F:\Spec_Runner` 并入本仓，单仓管理）
> **任务来源**: 用户裁决「spec_runner 放在 spec_workflow 文件夹下面可以方便管理 读写 请重新分析」→ RESEARCH v1.1 C1 改判采纳并入 → 用户指令「好的，进入实施批」
> **性质声明**: 小流程实施批——上游调研（RESEARCH v1.1）已完成方向定案，本批 = DESIGN（本文件）→ 实施 → IMPLEMENTATION + CHECKLIST 落档
> **审查状态**: `自查（单视角）`（RULE-4）——独立 pass 挂收口后触发（同 P-009 先例）

---

## 1. 设计目标

把 Spec_Runner（`F:\Spec_Runner`：spec_runner.py 519 行 / README / templates ×2 / sessions ×4 事件流）并入本仓，实现：

1. **单仓管理**：统一读写/检索/提交，免双仓切换（RESEARCH v1.1 B1 实证的管理便利收益）
2. **证据同仓**：事件流（sessions/*.jsonl，E1 级）与 M7 账本同仓可读，指针形态 `Spec_Runner:sessions/...` → 本仓相对路径
3. **上游裁决修订**：LANGGRAPH §6「独立仓库」明文 + spec-runner DESIGN D1「两类可执行件分属两仓」随并入版本化修订（HOMING 是本框架首次"执行层裁决反悔"实例——修订机制与先例同等重要）
4. **对账零破坏**：repo_stats 机读块/模式库/树清单在并入后重算一致，不遗留 P1/P2

**非目标**：不改 spec_runner.py 逻辑与事件流 schema（纯搬移 + 指针改写，行为零变化——并入是部署变更不是功能变更）；不删除外仓 `F:\Spec_Runner`（冻结为历史存档，双仓漂移防线退役但保留 git 历史可回溯）。

## 2. 关键设计决策

### D1. 落点 = 根级 `tools/spec_runner/`（独立工具目录），否决 scripts/

| 候选 | 裁决 | 理由 |
|------|------|------|
| **`tools/spec_runner/`（采纳）** | ✅ | ① 与三校验器 + pf_m7_eval（scripts/，契约机械化）语义分离——runner 是工作流机械化，工具目录独立成层；② repo_stats 对账键不受扰：`scripts` 计数键仍 4、`spec_feature_dirs` 仍 16、`templates` 键仍 5，零键变更，仅需 CODE_WIKI 树登记 + 覆盖对象描述更新；③ 目录自含（spec_runner.py + README + sessions/ + templates/），ROOT 由 `__file__` 派生（spec_runner.py L39 `ROOT / "sessions"`），搬移后路径自洽零改码 |
| `scripts/spec_runner.py` | ❌ | ① scripts/ 语义 = 本仓契约的机械化校验器（三校验器）/评测运行器，runner 是工作流执行器，混放稀释两层语义；② 触发 repo_stats `scripts` 计数 4→5 键变更 + 树/索引对账 |
| `spec/` 下 | ❌ | spec/ = feature 文档目录（十六目录全为 four件套/调研），代码混入违反「feature 目录 = 文档」契约（dc_validator 会扫 spec/ 下 md 而非 py，语义错位） |

**E1 取证回流**：事件流随仓入库路径 = `tools/spec_runner/sessions/<sid>.jsonl`；M7 账本「来源」列指针形态改为相对路径（`tools/spec_runner/sessions/...jsonl#seq`）——账本不复制内容原则不变，仅锚点改写。

### D2. 外仓处理 = 冻结存档，不删除

`F:\Spec_Runner` 目录保留（git 历史 5 commit 完整），不再作为活跃代码仓；本仓 README/PROGRESS 登记「外仓冻结」状态。理由：① 双仓漂移防线演进为单仓版本化，外仓 git 历史是 P-009 实施批的完整证据链，删除即丢证据；② 万一单仓方案后续发现实操问题，外仓可作为回滚基线（RESEARCH H2 过渡期假设保留外仓直到验收稳定）。

### D3. 上游裁决修订形态 = 版本化修订注（不推翻文档本体）

- **LANGGRAPH §6**：版本 v1.2 → 追加「P-019 修订注」段（保持原主判断原文不变 + 修订注说明该条被本仓内聚化事实修订）——先例：P-014 的「修正注 + DR-7」模式
- **spec-runner DESIGN D1**：v1.0 → 追加修订注（D1 原双仓裁决被 HOMING 修订，理由 = RESEARCH A6 实证）
- **spec-runner IMPLEMENTATION**：锚 commit hash 防线 → 追加 P-019 追记（锚点退役，代码已入本仓）

### D4. 实施步骤（五步，DESIGN §5 规格）

1. 建 `tools/spec_runner/` 目录结构，Copy-Item 外仓 8 文件（spec_runner.py/README/sessions×4/templates×2）——**纯复制，不覆盖本仓任何现有文件**
2. 指针改写：README 设计规格指针（`F:\Spec_Workflow\spec\spec-runner\...` 相对化）、adapter docstring、M7 账本来源列、PROGRESS/CODE_WIKI 事件流指针
3. 上游裁决修订注（LANGGRAPH §6 + DESIGN D1 + IMPL）
4. CODE_WIKI 树登记 + 覆盖对象描述 + 版本头 v1.16.1→v1.17；PROGRESS P-019 收口
5. 三通道验证（dc_validator/m7_stats/repo_stats）+ selftest 重跑（spec_runner.py 21 项）→ commit + push

## 3. 验收标准（CHECKLIST 依据）

| # | 标准 | 验证方法 |
|---|------|---------|
| C1 | 8 文件完整落入 `tools/spec_runner/`（目录树与源 hash 逐字节核对） | `Get-FileHash` 源/目标比对 |
| C2 | spec_runner.py 逻辑零改动（搬移原样） | 源码 diff 为空（除路径相关注释） |
| C3 | selftest 21/21 通过（新路径自洽） | `python tools/spec_runner/spec_runner.py selftest` exit 0 |
| C4 | 本仓三校验器 + repo_stats 全绿（对账键不变） | dc_validator/m7_stats/repo_stats exit 0 |
| C5 | 上游修订注落地（LANGGRAPH §6 / DESIGN D1 / IMPL 各一处） | grep 修订注标记 |
| C6 | 事件流指针形态改写（`Spec_Runner:sessions/` 全仓 grep 归零） | grep 校验 |
| C7 | M7 账本零新增样本（并入零发现——纯部署变更） | m7_stats verify |

## 4. 风险与缓解

| 风险 | 缓解 |
|------|------|
| repo_stats/PT 模式误扫新目录（tools/ 不在现有 regex 覆盖） | D1 已选独立目录绕开对账键；验证步骤 C4 实跑兜底 |
| 事件流 jsonl 内含旧绝对路径指针 | C6 grep 归零兜底 + 事件流内容不改（append-only 证据） |
| LANGGRAPH/D1 修订注被误判为"文档篡改" | D3 修订注模式（保留原文 + 追加注）与 P-014 先例一致 |
| spec_runner.py ROOT 派生路径变化（L39 `ROOT/"sessions"`） | C3 selftest + 一次真实 gate 入流实测新路径 |

## 5. 实施批五步规格（Step 5-10 对应）

| 步骤 | Spec 步 | 动作 | 产出 |
|------|---------|------|------|
| 1 | Step 5 实施 | 复制 8 文件 + hash 核对 | `tools/spec_runner/` 目录 |
| 2 | Step 5 实施 | 指针改写（README/adapter/M7/PROGRESS/CODE_WIKI） | 相对路径指针 |
| 3 | Step 5 实施 | 上游修订注（LANGGRAPH §6 + DESIGN D1 + IMPL） | 三处修订注 |
| 4 | Step 7 验收 | 三通道 + selftest + C1-C7 核对 | 绿色报告 |
| 5 | Step 8-10 收束 | IMPLEMENTATION + CHECKLIST 落档 + PROGRESS done + CODE_WIKI v1.17 + commit + push | 交付物归档 |