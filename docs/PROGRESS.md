# PROGRESS 待办登记

> 依据 SPEC_PROCESS 约定建立（每步完成后更新）。状态词表: `pending / in-progress / blocked / done`。
> 登记日期: 2026-08-16

## 待办事项

| ID | 事项 | 依据 | 状态 | 验收标准 |
|----|------|------|------|---------|
| P-001 | Cpp_Hub 侧两文件迁移指针（ADR-0006 决策 3） | [ADR-0006](../adr/ADR-0006-assertion-framework-dual-copy-authority.md) 修订历史（决策 3 执行记录）/ [调研文档](../spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md) §6 | done | 五项验收：① P1/P2 指针 grep 双命中 ✅ ② Cpp_Hub 提交 `96edc5c`（AEF，选择性提交）✅ ③ DEVELOPMENT_LOG 代登（随现场提交入库）✅ ④ ADR-0006 追记 ✅ ⑤ pilot v1.1 引用=历史快照不改（开放项裁决）。注：DIS-007 属 Cpp_Hub gitignore 范围，指针本地生效；Cpp_Hub ahead 11 未推送（现场裁量） |
| P-002 | 第二次回流执行（6 项清单，优先级序） | [设计文档](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) v1.1 + [CHECKLIST](../spec/cpp-hub-absorption/CHECKLIST.md)（验收 39/40，1 P3 归 P-003） | done | 设计 §11 六项验收全过；[DEV-LOG-002](dev-log/DEV-LOG-002-cpp-hub-absorption-execution.md)；commits 8ea38bf/eed0906/f79fa49/b7a7f58（已推送） |
| P-003 | doc-contract 改造 Step A-G 执行 | [PLAN.md](../spec/doc-contract/PLAN.md) v1.5（verified） | done | Step A-G 全过（2026-08-17/18）：四项 grep 复核语义全过（`P0`@CHECKLIST 零 / `id:` 21 文件 / `docs/spec/`+`RESOLVED` 命中均为改名元描述，复核结论入 PLAN §5）；RULE-1~6 冠名 + rules 登记块；ADR_TEMPLATE 新建；PLAN v1.5（G→DC/§6 指针化/P3-1·2 闭环）；CODE_WIKI v1.2 尾随同步 |
| P-004 | GAP_ANALYSIS 审计 P2 修正后异基座 S1 复验 | [审计报告 S1 复验](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md) §7 | done | S1 复验完成（2026-08-18，DeepSeek V4 Pro 异构于 GLM-5.3）：P2-1(A 计数)/P2-2(行号)/P3-2(E1) 修正正确；发现 P2-3（C 计数仍差 1，审计修正自身含错，形态 II 第四实例）→ 已修正 C=2→3；B1-B4 核心结论成立；M7 样本 ⑥ 入表（形态 II 分桶 10→11） |
| P-005 | 形态 II 复发跟踪指标入 M7 | 审计报告 §4.3 | done | ① 分桶指标 ✅（[M7 §2](M7_EVIDENCE_LOG.md)，4 载体 × 7 字段类型 = 10 处，含映射闭合新桶）；② §0 计数脚本生成规则 ✅ 落 [框架 v1.4 R7](ASSERTION_EVIDENCE_FRAMEWORK.md)（原设想"入 ADR-0007"经评估主题错位改落框架——报告模板规则的权威载体，Tier1 同通道先例） |
| P-006 | LangGraph 框架化升级调研 | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) v1.1（复核后） | done | v1.0（14A→实为 11A，形态 II 第五实例，R7 机械重数修正）：不整体迁移，方法论仓库保持纯文档，自动化走薄壳 runner（方案 B），LangGraph 为触发条件后升级路径。v1.1 补充：最高 ROI = pre-commit + DC 契约校验器（形态 II 机械拦截，先于方案 B 可执行）；次高 = promptfoo（M7 对比臂声明式评测，触发条件样本≥10）。复核（2026-08-18）：推荐无幻觉（coograph/OpenMMLab 先例经 WebSearch 证实真实存在），补 coograph URL + OpenMMLab URL + A=15 重数自引用修正（`grep -c '【A】'` 原始 16 含本行自引用，候选 M7 样本⑨）；决策待用户 |
| P-007 | pre-commit + DC 契约校验器（调研 + 设计） | [调研报告](../spec/precommit-dc-validator/PRECOMMIT_DC_VALIDATOR_RESEARCH.md) v1.1 + [设计](../spec/precommit-dc-validator/DESIGN.md) v1.2 | in-progress | Step 1-4 产出 + 复验（2026-08-18）：调研 7A+2B+1C+3H；设计五检查（M2-M5 覆盖 DC1/DC2/DC4/R7/DC3）+ 五不变式 + 三替代方案否决。复验（同基座新上下文 DeepSeek V4 Pro，RULE-1 满足 / RULE-5 异质性未满足如实降级）：A 类 7 条页面级全闭合（pre-commit.com/4.6.2/sentinel local/fixdevs/lychee#2238 逐字命中）；发现 1P2（DESIGN §6.3 词表双轴歧义，升格实施前置条件——PLAN §1 DC2 须先消歧）+ 2P3（RESEARCH §0 计数说明失实已修正；退出码 2 路径已补注），形态 II 复发 1 入 M7 样本⑦（分桶 11→12）。P2-1 前置已闭合（2026-08-18：PLAN v1.6 §1 DC2 消歧——design 两行 + id 后缀 -CHECKLIST 判别，E1 全仓 14 份 design 文档零违规；ADR-0007 D4 澄清追记；v1.1 P2-1 注自身引证错 L59 勘误入 M7 样本⑧，形态 II 分桶 12→13）。下一步：Step 5-7 |

## 已完成（近三项）

| 日期 | 事项 | 产出 |
|------|------|------|
| 2026-08-16 | ADR-0006 方案 B 执行（v1.2 回吸收） | commit c428a58（已推送） |
| 2026-08-16 | 差距分析调研 | spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md v1.0（12A+4B+7C+3H） |
| 2026-08-16 | ADR-0006 决策 3 展开调研 + 待办登记 | spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md v1.0 + 本文件 |
