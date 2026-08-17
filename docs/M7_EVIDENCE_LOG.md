# M7 证据账本（对比臂数据累积）

> **权威载体**: 本文件为 M7 数据**唯一活载体**（[ADR-0007](../adr/ADR-0007-unified-document-contract.md) D1，accepted 2026-08-17）——PLAN §6 为历史快照（随 P-003 降为指针），DEV-LOG 记事件叙事，聚合数据只在此登记。
> **建立**: 2026-08-17（cpp-hub-absorption D2/D3，Tier1）；骨架源自 [CPP_HUB_ABSORPTION_DESIGN.md](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) §4.2
> **登记纪律**: 每轮审查/审计完成后追加一行样本，形态 II 分桶随样本同步追加。连续两轮无追加即触发 ADR-0007 失效条件重审（僵尸账本 → 并回 ADR 附录）。

## 1. 样本登记表

| # | 日期 | 载体 | 审查配置 | 发现 | 形态II复发 | 来源 |
|---|------|------|---------|------|-----------|------|
| 1 | 2026-08-16 | doc-contract 方案 | 同基座自查 GLM-5.3（既写又审） | 10（2P1+5P2+3P3） | 0 | PLAN §6 |
| 2 | 2026-08-16 | doc-contract 方案 | 异构双盲 DeepSeek V4 Pro | 12（7P2+5P3） | 0 | PLAN §6 |
| 3 | 2026-08-17 | ADR-019 决策集（Cpp_Hub） | 探针 + 双盲（pilot） | R2 拦截 1/4；双盲 5/5 TRUE | 1（转述引文） | pilot §5.1 |
| 4 | 2026-08-16 | GAP_ANALYSIS 报告（本仓） | 同基座独立审计 GLM-5.3 | 4（2P2+2P3） | 2（计数/行号） | AUDIT §3 |
| 5 | 2026-08-17 | cpp-hub-absorption DESIGN（本仓） | 同基座独立 pass GLM-5.3 | 2P2+6P3 | 1（映射闭合） | DESIGN §10（CHECKLIST 验收时点追加） |

> **追加队列**: ⑥ P-004 异基座 S1 复验完成后追加。样本 ⑤ 已于 CHECKLIST 验收（2026-08-17）时点入表。

## 2. 形态 II 复发分桶（载体 × 字段类型）

> 依据 [GAP_ANALYSIS_AUDIT §4.3](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md) + PROGRESS P-005。字段类型 = 形态 II 偏好的"精确-looking 低语义载荷"字段；Phase 7C 六处细分按框架 §2.2 复盘表归类（#5 版本号 / #7#8 章节号 / #1#4#6 常量与默认值）。

| 载体 \ 字段类型 | 版本号 | 章节号 | 数值常量 | 行号 | 计数 | 转述引文 | 映射闭合 | 小计 |
|---|---|---|---|---|---|---|---|---|
| Phase 7C 调研报告（Cpp_Hub） | 1 | 2 | 3 | — | — | — | — | 6 |
| ADR-019 pilot 复核报告（Cpp_Hub） | — | — | — | — | — | 1 | — | 1 |
| GAP_ANALYSIS_RESEARCH（本仓） | — | — | — | 1 | 1 | — | — | 2 |
| CPP_HUB_ABSORPTION_DESIGN（本仓，Step 4 Review） | — | — | — | — | — | — | 1 | 1 |
| **合计** | 1 | 2 | 3 | 1 | 1 | 1 | 1 | **10** |

**复发规律锚点**（AUDIT §4.2 三规律）: ① 偏好低语义载荷字段；② 防幻觉机制自身不设防（元断言逃逸——统计表/映射表自身出错）；③ 拦截层是 E1 机械枚举，非 LLM 自查。"映射闭合"桶为 2026-08-17 Step 4 Review 新增变体（计数闭合假象：表面 3+3+5=11 替代逐项映射实质闭合）。

## 3. 命中率 baseline

| 来源 | review 修正数 | 锚点 |
|------|-------------|------|
| Cpp_Hub Phase 5 四波 | 14 处（2+1+6+5） | AUDIT_CHECKLIST L462-465（过审计 A9，算术复核正确） |

## 4. 待办挂钩

- **P-004**: 异基座 S1 复验（GAP_ANALYSIS 修正版）→ 完成后追加样本 ⑥
- **P-005**: "§0 统计表计数改脚本生成"规则——ADR-0007 D1-D5 未含，遗留为后续 ADR 修订候选
- **M7 成文**: 若需统计升 ```hits 机读块（DESIGN §6 既定，学习回路独立议题，不并入当前 feature）
