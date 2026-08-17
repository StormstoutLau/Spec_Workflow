# PROGRESS 待办登记

> 依据 SPEC_PROCESS 约定建立（每步完成后更新）。状态词表: `pending / in-progress / blocked / done`。
> 登记日期: 2026-08-16

## 待办事项

| ID | 事项 | 依据 | 状态 | 验收标准 |
|----|------|------|------|---------|
| P-001 | Cpp_Hub 侧两文件迁移指针（ADR-0006 决策 3） | [ADR-0006](../adr/ADR-0006-assertion-framework-dual-copy-authority.md) / [调研文档](../spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md) | pending | 调研文档 §6 五项（含 grep "权威源已迁移" 2 命中 + Cpp_Hub 提交可溯 + dev-log 登记 + ADR-0006 追记） |
| P-002 | 第二次回流执行（6 项清单，优先级序） | [设计文档](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) v1.1（Step 4 Review 已过，P2 清零；基于[已审计差距分析](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md)；ADR-0007/0008/0009 已 accepted） | in-progress | 设计 §11 六项验收（Tier1 D1-D3 → Tier2 D4-D6 各立 ADR → Tier3 拒收记录）。**Tier1+Tier2 已完成（2026-08-17）**: 框架 v1.3 + [M7_EVIDENCE_LOG.md](M7_EVIDENCE_LOG.md) + SPEC_PROCESS v1.4（门禁/双向引用/断言延续/发现集成点×2）+ [ADR-0009](../adr/ADR-0009-discoveries-log-mechanism.md) + [discoveries 索引](discoveries/README.md)（DIS-008 首登）。剩 CHECKLIST 验收（Step 7-10） |
| P-003 | doc-contract 改造 Step A-G 执行 | [PLAN.md](../spec/doc-contract/PLAN.md) v1.4 | pending | PLAN §5 完成定义（四项 grep 复核） |
| P-004 | GAP_ANALYSIS 审计 P2 修正后异基座 S1 复验 | [审计报告](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md) §5 | pending | 异基座会话复验修正版报告，作为 M7 对比臂样本 |
| P-005 | 形态 II 复发跟踪指标入 M7 | 审计报告 §4.3 | pending | M7 数据单列"形态 II 复发计数"（载体 × 字段类型分桶）；§0 统计表计数改脚本生成规则入 ADR-0007 |

## 已完成（近三项）

| 日期 | 事项 | 产出 |
|------|------|------|
| 2026-08-16 | ADR-0006 方案 B 执行（v1.2 回吸收） | commit c428a58（已推送） |
| 2026-08-16 | 差距分析调研 | spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md v1.0（12A+4B+7C+3H） |
| 2026-08-16 | ADR-0006 决策 3 展开调研 + 待办登记 | spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md v1.0 + 本文件 |
