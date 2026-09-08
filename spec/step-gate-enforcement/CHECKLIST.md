# 验收清单：step-gate 流程强制（P-024）

---
id: step-gate-enforcement-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-09
depends: [step-gate-enforcement-DESIGN]
upstream: null
---

> **Feature**: step-gate 流程强制（P-024）
> **Spec 步骤**: Step 5-8
> **设计**: [DESIGN](./DESIGN.md) v1.0

## 验收项

| # | 验收项 | 结果 |
|---|--------|------|
| C1 | spec_runner 新增 `step-enforce --pid` 子命令（前缀定位 session + 复用 step-gate 校验） | ✅ |
| C2 | selftest 增 F27-F29（无 session exit 1 / 空链 exit 1 / 合法链 exit 0）→ **31/31** | ✅ |
| C3 | `scripts/step_enforce.py` hook 入口：feature → P 映射；映射缺位 → exit 2 提示 | ✅ |
| C4 | `.pre-commit-config.yaml` 第四 hook（files 收窄至 spec/ 四文档） | ✅ |
| C5 | **吃狗粮自证**：P-024 session `specwf-p024-20260909` + research decision 过 `step-enforce --pid P-024` → exit 0；hook 全链路（RESEARCH/DESIGN/CHECKLIST 三文件）→ exit 0 | ✅ |
| C6 | **只读零副作用**（P-022 教训）：step-enforce / hook 均无 git 操作、无文件创建（F27-F29 临时 session 由 selftest 自清理） | ✅ |
| C7 | 三通道全绿（dc-validator 85 文件 / m7-stats / repo-stats 0 违规）——hook 新增后 repo-stats 对账（hooks 3→4 / scripts 4→5 / feature 20→21 / progress 23→24） | ✅ |
| C8 | DESIGN v1.0 → verified；RESEARCH v1.0 → verified | ✅ |

## 独立 pass 待触发

同 P-021/P-022 先例：机械复核（三通道重跑 + selftest 重跑 + 调用点 grep）待本批收口时执行。

---

**Review 签字**: _________ 日期: _________
