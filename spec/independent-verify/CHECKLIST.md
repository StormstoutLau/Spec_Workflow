# 验收清单：独立验证（出路 C——verify-anchor + 审查臂输入重定义）

---
id: independent-verify-CHECKLIST
type: design
version: 1.0
status: pending
date: 2026-09-09
depends: [independent-verify-DESIGN, independent-verify-RESEARCH]
upstream: null
---

> **Feature**: 独立验证（P-025——ADR-0011 出路 C）
> **创建日期**: 2026-09-09
> **Spec 步骤**: Step 7-8

## 验收项

| # | 验收项 | 结果 |
|---|--------|------|
| C1 | spec_runner 新增 `verify-anchor --session` 子命令（decision 锚点真实性核查：文件存在 + 章节标题精确匹配 + 行号上界，URL soft，只读零副作用） | ✅ |
| C2 | selftest 增 F30-F36（真实锚点 / 文件不存在 / 章节不存在 / 行号越界 / URL soft / §5 精确 / §5.3 精确）→ **38/38**（原 31 + 7） | ✅ |
| C3 | SPEC_PROCESS RULE-1 补独立 pass 取证清单（审查输入 = 事件流 + verify-anchor + git 状态；纯登记型无 diff 合法；verify-anchor 只验位置可达不验断言对错） | ✅ |
| C4 | **吃狗粮自证**：P-025 session 决策链 3 步（research/design/implement）过 `step-gate --expect` exit 0 + 自身锚点 3 条过 `verify-anchor` exit 0 | ✅ |
| C5 | 历史 session 取证：p020 v2（6 锚点含行号引用）/ p023（2）/ p024（1）全真实 exit 0 | ✅ |
| C6 | **只读零副作用**（P-022 教训）：verify-anchor 无 git 操作、无文件创建（F30-F36 临时 session 由 selftest 自清理） | ✅ |
| C7 | 三通道全绿（dc-validator 87 文件 / m7-stats / repo-stats 0 违规——CODE_WIKI 登记后对账 spec_feature_dirs 21→22 / hooks 4 / scripts 5 / progress 24→25） | ✅ |
| C8 | DESIGN v1.0 → verified；RESEARCH v1.0 → verified | ✅ |
| C9 | **独立 pass 复核**：三通道重跑（dc 88 文件 0 违规 / m7 0 违规 / repo_stats 0 违规——CODE_WIKI 登记后 P1 21≠22 + PT-11 24≠25 两处活靶修正归零）+ selftest 重跑（38/38）+ 调用点 grep（verify-anchor 命令/parser/selftest F30-F36 全一致）+ P-025 完整链 step-gate exit 0 + 锚点 5 条 verify-anchor exit 0 + 历史 session（p020 v2 6 / p023 2 / p024 1）全量取证 | ✅ |

## 验收记录

- **2026-09-09**：C1-C8 逐项核验通过（实施 + 吃狗粮实证 + 三通道）。C9 独立 pass 复核通过（2026-09-09，四通道：三通道重跑 + selftest 38/38 + 调用点 grep + 历史 session 全量取证）。
