# ADR 索引与编号登记

> 物理目录为仓库根 `adr/`（本索引放 `docs/adr/` 仅为编号登记入口；路径真值统一见 doc-contract 方案 S2/S6）。

## 本仓库 ADR

| 编号 | 标题 | 状态 | 一句话 |
|------|------|------|--------|
| [ADR-0004](../../adr/ADR-0004-adopt-external-benchmark-heterogeneity-quarantine.md) | 对抗审查异质性约束与测试隔离四要素 | accepted | 异构基座 + 单向权限 + quarantine 四要素 + RTM 反向追溯 |
| [ADR-0005](../../adr/ADR-0005-audit-evidence-binding-spec-workflow.md) | 审计证据绑定（取证矩阵标准化） | accepted | E1-E5 证据五分类 + 双向映射 + 诚实结果列 |
| [ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) | 断言证据框架双份并存——差异分析与权威源决策 | accepted（2026-08-16，方案 B 已执行；**v1.1 定稿 2026-09-26**：决策 1-4 维持 accepted，**决策 5/6 已转 accepted**） | 本仓库为权威源，v1.2 已回吸收 Cpp_Hub v1.1 增量；决策 4 回流通道已于 2026-08-17 首次批量使用（P-002）；**v1.1 草案（2026-09-23）**——失效条件重审 #1（②重开残余 R-1/R-2、③窗口 37/90 天未满 → 复核到期 **2026-11-15**）+ 决策 5 判定权拆分 + 决策 6 机械漂移检查 J-1~J-4；**v1.1 定稿 + 落地（2026-09-26，P-049）**——**重审 #2 实测**（**R-2 消解**：`origin/main...HEAD` 同步 `0 0`；**R-1 精化**：AEF 指针已入库，`DIS-007` 因 `.gitignore:82` 的**整目录** `docs/discoveries/` 被忽略而仍不入库）+ J-1~J-4 机械化为可复算检查器（`spec/downstream-compliance/`）+ 判定表三列格式与骨架生成器；**v1.2（2026-09-29，P-056）**——**§B3 重审 #3**（观测窗 **43/90 天**：①用户裁决方案 A 未命中 / ②**形式解除**（R-1 存续未扩大、R-2 维持消解）/ ③**未满窗不判负** ⇒ **维持 accepted**；独有读数 = Cpp_Hub `docs/COMPLIANCE_TABLE.md` **未落盘**；条件③ 裁定维持 **2026-11-15**） |
| [ADR-0007](../../adr/ADR-0007-unified-document-contract.md) | 统一文档契约——命名空间消歧与 M7 证据账本权威载体 | accepted（2026-08-17，D1-D5 整批） | M7_EVIDENCE_LOG 唯一活载体 / G1-G4→DC1-DC4 / design 入词表 / 英文 token |
| [ADR-0008](../../adr/ADR-0008-spec-process-review-gate-and-bidirectional-check.md) | SPEC_PROCESS v1.4——Step 2 门禁语义与 Step 8 双向链路检查 | accepted（2026-08-17，D4+D6 双决策） | R4 语义门禁 (a)-(d) + 双向引用/断言延续两项 |
| [ADR-0009](../../adr/ADR-0009-discoveries-log-mechanism.md) | Discoveries 发现日志机制——学习回路"事故→规则"的载体 | accepted（2026-08-17） | 三态索引 + Step 2/10 双集成点；DIS-008 首登 |
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 懒加载架构原则——Layer-0/Layer-1 分层作为候选吸收的强制门禁 | accepted（2026-09-08，用户确认） | 候选吸收三问（放哪层/激活条件/零副作用）+ 与 D6 互补防过重 |
| [ADR-0011](../../adr/ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md) | step-gate 未生效排查——触发依赖与表演性决策软肋 + 社区解法映射 | accepted（2026-09-09，用户裁决 A+C 组合收口） | P-021/022/023 三连批决策链缺失根因诊断 + 决策 = A+C 组合（B 排除暂缓）；A 已落地（step-enforce，P-024）/ C 已落地（verify-anchor，P-025）；2026-09-11 **v1.8 追记**（存量缺失 5 条 session 回溯补建）；2026-09-29 **v1.9 追记**（P-052 版本声称订正：P-025 实施行 v1.4.0 → v1.3.0） |

## 编号空间登记

| 编号段 | 状态 | 说明 |
|--------|------|------|
| ADR-0001 ~ 0003 | 源项目·未随迁 | f:\ 根 + Cpp_Hub + Crucix 三处零命中实证（2026-08-16 探针）；教训已内联 SPEC_PROCESS，不补写 |
| ADR-001~019（三位） | **[源项目·Cpp_Hub/docs/decisions/] 独立系列** | 与本仓四位系列无连续编号关系（B4 补全登记，2026-08-17） |

> 完整编号命名空间登记（DIS/RULE/M/Phase 等）的**权威载体** = [ADR-0007 附录 A](../../adr/ADR-0007-unified-document-contract.md)（accepted 2026-08-17）；本节仅为 ADR 系列摘要。
