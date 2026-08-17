# ADR 索引与编号登记

> 物理目录为仓库根 `adr/`（本索引放 `docs/adr/` 仅为编号登记入口；路径真值统一见 doc-contract 方案 S2/S6）。

## 本仓库 ADR

| 编号 | 标题 | 状态 | 一句话 |
|------|------|------|--------|
| [ADR-0004](../../adr/ADR-0004-adopt-external-benchmark-heterogeneity-quarantine.md) | 对抗审查异质性约束与测试隔离四要素 | accepted | 异构基座 + 单向权限 + quarantine 四要素 + RTM 反向追溯 |
| [ADR-0005](../../adr/ADR-0005-audit-evidence-binding-spec-workflow.md) | 审计证据绑定（取证矩阵标准化） | accepted | E1-E5 证据五分类 + 双向映射 + 诚实结果列 |
| [ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) | 断言证据框架双份并存——差异分析与权威源决策 | **proposed**（方案 B 待确认） | 本仓库为权威源，v1.2 回吸收 Cpp_Hub v1.1 增量 |

## 编号空间登记

| 编号段 | 状态 | 说明 |
|--------|------|------|
| ADR-0001 ~ 0003 | 源项目·未随迁 | f:\ 根 + Cpp_Hub + Crucix 三处零命中实证（2026-08-16 探针）；教训已内联 SPEC_PROCESS，不补写 |
| ADR-0007 | 预留 | 统一文档规范（doc-contract，见 [spec/doc-contract/PLAN.md](../../spec/doc-contract/PLAN.md) v1.3） |

> 完整编号命名空间登记（DIS/RULE/M/Phase 等）随 ADR-0007 附录正式化。
