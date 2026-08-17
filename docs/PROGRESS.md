# PROGRESS 待办登记

> 依据 SPEC_PROCESS 约定建立（每步完成后更新）。状态词表: `pending / in-progress / blocked / done`。
> 登记日期: 2026-08-16

## 待办事项

| ID | 事项 | 依据 | 状态 | 验收标准 |
|----|------|------|------|---------|
| P-001 | Cpp_Hub 侧两文件迁移指针（ADR-0006 决策 3） | [ADR-0006](../adr/ADR-0006-assertion-framework-dual-copy-authority.md) / [调研文档](../spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md) | pending | 调研文档 §6 五项（含 grep "权威源已迁移" 2 命中 + Cpp_Hub 提交可溯 + dev-log 登记 + ADR-0006 追记） |
| P-002 | 第二次回流执行（6 项清单，优先级序） | [设计文档](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) v1.1 + [CHECKLIST](../spec/cpp-hub-absorption/CHECKLIST.md)（验收 39/40，1 P3 归 P-003） | done | 设计 §11 六项验收全过；[DEV-LOG-002](dev-log/DEV-LOG-002-cpp-hub-absorption-execution.md)；commits 8ea38bf/eed0906/f79fa49/b7a7f58（已推送） |
| P-003 | doc-contract 改造 Step A-G 执行 | [PLAN.md](../spec/doc-contract/PLAN.md) v1.4 | pending | PLAN §5 完成定义（四项 grep 复核） |
| P-004 | GAP_ANALYSIS 审计 P2 修正后异基座 S1 复验 | [审计报告](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md) §5 | pending | 异基座会话复验修正版报告，作为 M7 对比臂样本 |
| P-005 | 形态 II 复发跟踪指标入 M7 | 审计报告 §4.3 | in-progress | ~~分桶指标落地~~ ✅（[M7 §2](M7_EVIDENCE_LOG.md)，4 载体 × 7 字段类型 = 10 处，含映射闭合新桶）；剩"§0 统计表计数改脚本生成"规则——登记为 ADR-0007 修订候选（[M7 §4](M7_EVIDENCE_LOG.md)） |

## 已完成（近三项）

| 日期 | 事项 | 产出 |
|------|------|------|
| 2026-08-16 | ADR-0006 方案 B 执行（v1.2 回吸收） | commit c428a58（已推送） |
| 2026-08-16 | 差距分析调研 | spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md v1.0（12A+4B+7C+3H） |
| 2026-08-16 | ADR-0006 决策 3 展开调研 + 待办登记 | spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md v1.0 + 本文件 |
