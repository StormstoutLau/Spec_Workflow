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
| 6 | 2026-08-18 | GAP_ANALYSIS_RESEARCH P2 修正版（本仓） | 异基座复验 DeepSeek V4 Pro（S1，RULE-5） | 1 P2（C 计数，审计修正自身含错） | 1（计数——审计修正自身的计数错误，形态 II 第四实例） | AUDIT §7 |
| 7 | 2026-08-18 | precommit-dc-validator RESEARCH v1.0 + DESIGN v1.0（本仓） | 同基座新上下文复验 DeepSeek V4 Pro（RULE-1 时序独立；RULE-5 异质性未满足——生成端同基座，如实降级） | 1P2+2P3（P2-1 词表双轴歧义 / P3-1 计数说明失实 / P3-2 退出码路径） | 1（计数——§0 扣减说明声称 1 处实为 3 处，防幻觉统计表自身说明失实，规律② 元断言逃逸又一实例） | 复验记录（两文档头部审查状态） |
| 8 | 2026-08-18 | precommit-dc-validator DESIGN v1.1 P2-1 修正注（本仓） | 实施期自查（P2-1 修复执行时发现，非独立审查轮，如实标注） | 1 P3（引证错误） | 1（行号——修正注称"PLAN L59 design 状态"，L59 实为"template 实例"行；design 词表实载于 PLAN 头注 + ADR-0007 D4，DC2 表 v1.6 前缺 design 行。规律④"修正自身含错"第二实例） | 本轮 P2-1 修复记录 + DESIGN v1.2 勘误注 |
| 9 | 2026-08-19 | ADR0006_POINTER_RESEARCH v1.0（存量）+ dc_validator.py v1.0 selftest（本仓） | 实施轮机械验证（P-007：M4/M5 预跑 + dry-run + selftest 复验——非 LLM 审查轮，拦截层 = 工具自身，如实标注） | 4（1P1 计数漏计 + 2P2 断链 + 1 工具自身计数缺陷） | 2（计数×2——① ADR0006 §0 声明 A=7 机械重数 8；② selftest 硬编码"12/12"实调 13 个 expect，DESIGN §10.2 风险 1 预注册场景命中） | IMPLEMENTATION §1 取证 + DR-5/DR-6；CHECKLIST §2.6/§8.2 |

> **追加队列**: ⑩ 后续审查轮次追加（LANGGRAPH v1.1 复核的 A 计数自引用为候选，见 PROGRESS P-006——是否补登记待用户裁决；⑨ 已被 P-007 实施轮占用）。

## 2. 形态 II 复发分桶（载体 × 字段类型）

> 依据 [GAP_ANALYSIS_AUDIT §4.3](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md) + PROGRESS P-005。字段类型 = 形态 II 偏好的"精确-looking 低语义载荷"字段；Phase 7C 六处细分按框架 §2.2 复盘表归类（#5 版本号 / #7#8 章节号 / #1#4#6 常量与默认值）。

| 载体 \ 字段类型 | 版本号 | 章节号 | 数值常量 | 行号 | 计数 | 转述引文 | 映射闭合 | 小计 |
|---|---|---|---|---|---|---|---|---|
| Phase 7C 调研报告（Cpp_Hub） | 1 | 2 | 3 | — | — | — | — | 6 |
| ADR-019 pilot 复核报告（Cpp_Hub） | — | — | — | — | — | 1 | — | 1 |
| GAP_ANALYSIS_RESEARCH（本仓） | — | — | — | 1 | 1 | — | — | 2 |
| CPP_HUB_ABSORPTION_DESIGN（本仓，Step 4 Review） | — | — | — | — | — | — | 1 | 1 |
| GAP_ANALYSIS_RESEARCH P2 修正版（本仓，S1 复验） | — | — | — | — | 1 | — | — | 1 |
| precommit-dc-validator RESEARCH（本仓，同基座复验） | — | — | — | — | 1 | — | — | 1 |
| precommit-dc-validator DESIGN P2-1 修正注（本仓，实施期自查） | — | — | — | 1 | — | — | — | 1 |
| ADR0006_POINTER_RESEARCH（本仓，M4 机械拦截） | — | — | — | — | 1 | — | — | 1 |
| dc_validator.py selftest（本仓，实施复验——审查臂自身） | — | — | — | — | 1 | — | — | 1 |
| **合计** | 1 | 2 | 3 | 2 | 5 | 1 | 1 | **15** |

**复发规律锚点**（AUDIT §4.2 三规律 + S1 复验实证）: ① 偏好低语义载荷字段；② 防幻觉机制自身不设防（元断言逃逸——统计表/映射表自身出错）；③ 拦截层是 E1 机械枚举，非 LLM 自查。④ **审计修正自身含计数错误**（S1 复验 P2-3，2026-08-18）：P2-1 修正的 C 计数仍差 1（漏计 §3.2【C】），证明形态 II 的复发不受基座切换影响——同基座与异基座审计者均可能漏计，但独立 grep 重跑可检测；**规律④ 第二实例见样本⑧**（P-007 P2-1 修正注自身行号引证错，实施期自查发现——"修正自身含错"跨通道复发）。"映射闭合"桶为 2026-08-17 Step 4 Review 新增变体（计数闭合假象：表面 3+3+5=11 替代逐项映射实质闭合）。**样本⑨ 双实证（2026-08-19，P-007 实施轮）**：其一 = 规律③ 的工具化兑现——M4/R7 机械枚举拦截 ADR0006 A 计数漏计（声明 7 实为 8，手填 vs 重数），拦截点从"审查轮独立 grep"前移至提交瞬间（pre-commit）；其二 = 规律② 的最极端实例——[DESIGN §10.2](../spec/precommit-dc-validator/DESIGN.md) 风险 1 预注册的"校验器自身含计数错误"精确命中（dc_validator.py v1.0 selftest 打印 13 行 PASS 汇总却称 12/12，硬编码手填计数），由实施复验捕获、expect 自增机械计数修复（R7 同构原则应用于工具自身）——**防幻觉机制自身不设防，即便该机制本身就是计数校验器**。

## 3. 命中率 baseline

| 来源 | review 修正数 | 锚点 |
|------|-------------|------|
| Cpp_Hub Phase 5 四波 | 14 处（2+1+6+5） | AUDIT_CHECKLIST L462-465（过审计 A9，算术复核正确） |

## 4. 待办挂钩

- **P-004**: 异基座 S1 复验（GAP_ANALYSIS 修正版）→ 完成后追加样本 ⑥
- ~~P-005: "§0 统计表计数改脚本生成"规则~~ ✅ 已落框架 v1.4 R7（2026-08-17，落点自"ADR-0007 修订候选"改判框架——报告模板规则的权威载体）
- **M7 成文**: 若需统计升 ```hits 机读块（DESIGN §6 既定，学习回路独立议题，不并入当前 feature）
