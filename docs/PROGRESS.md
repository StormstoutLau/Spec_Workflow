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
| P-006 | LangGraph 框架化升级调研 | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) v1.1（复核后） | done | v1.0（14A→实为 11A，形态 II 第五实例，R7 机械重数修正）：不整体迁移，方法论仓库保持纯文档，自动化走薄壳 runner（方案 B），LangGraph 为触发条件后升级路径。v1.1 补充：最高 ROI = pre-commit + DC 契约校验器（形态 II 机械拦截，先于方案 B 可执行）；次高 = promptfoo（M7 对比臂声明式评测，触发条件样本≥10）。复核（2026-08-18）：推荐无幻觉（coograph/OpenMMLab 先例经 WebSearch 证实真实存在），补 coograph URL + OpenMMLab URL + A=15 重数自引用修正（`grep -c '【A】'` 原始 16 含本行自引用）。**决策已闭合（2026-08-19 治理收束轮）**：A 计数错误补登为 M7 样本⑩（自引用观察作附随观察不单列），见 M7 §1 |
| P-007 | pre-commit + DC 契约校验器（全流程 Step 1-7） | [调研报告](../spec/precommit-dc-validator/PRECOMMIT_DC_VALIDATOR_RESEARCH.md) v1.1 + [设计](../spec/precommit-dc-validator/DESIGN.md) v1.2 + [实施](../spec/precommit-dc-validator/IMPLEMENTATION.md) v1.1 + [验收](../spec/precommit-dc-validator/CHECKLIST.md) v1.0 | done | Step 1-4（2026-08-18）：调研+设计+复验（1P2+2P3 修正，M7 样本⑦⑧）。Step 5-7（2026-08-19）：IMPLEMENTATION v1.1（DR-1~DR-6）+ `scripts/dc_validator.py`（M1-M5，零依赖）+ `.pre-commit-config.yaml` 落地；dry-run 双通道 35 文件/9 skip/0 违规（独立调用 + pre-commit run 均 exit 0）+ selftest 13/13；存量违规修复 DR-5（ADR0006 A 计数 7→8 + ADR-0004/0005 断链 `../../`→`../`）+ DR-6（selftest 硬编码 12/12 → expect 自增机械计数，DESIGN §10.2 风险 1 预注册场景命中）；M7 样本⑨入账（形态 II ×2，分桶 13→15）。CHECKLIST 有条件通过（自查全绿，独立 pass 见 P-008） |
| P-008 | P-007 产出独立 pass（RULE-1 时序独立；真异基座优先） | [IMPLEMENTATION](../spec/precommit-dc-validator/IMPLEMENTATION.md) §9 + [CHECKLIST](../spec/precommit-dc-validator/CHECKLIST.md) §10.2 | pending | 审查 IMPLEMENTATION v1.1 + CHECKLIST v1.0（含 Step 10 ADD 独立审计）；通过后 IMPLEMENTATION status → verified、CHECKLIST → accepted；完成后 M7 追加样本⑫ |
| P-009 | 薄壳纯 Python runner（方案 B，独立仓库） | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §5/§6 主判断（P-006 裁决方向）+ H2 PoC 查证 | pending | 方向性候选（自动化需求出现时启动）：runner 骨架独立仓库落地——显式 `--gate` 门禁命令物理化 RULE-1 + JSON state + git 持久化 + LM Studio 端点异构审查，零框架依赖（~500-1000 LOC 待 H2 实测）；LangGraph 升级触发条件 (a)/(b)/(c)（调研 §6）随 runner 落地登记复查 |
| P-010 | promptfoo M7 对比臂声明式评测 | [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §8.2/§8.3（次高 ROI）+ H5 PoC 查证 | pending | 触发条件已满足（M7 样本 11 ≥ 10，样本⑪ 入账后；混轴修正注见 M7 样本⑪③）：promptfooconfig.yaml（LM Studio 本地端点作 provider）+ 首轮声明式对比评测（同一报告 × 同基座/异基座审查）结果入 M7 登记；H5 成本/延迟实测 |
| P-011 | M7 统计升 ```hits 机读块 + 样本登记脚本化 | [M7 §4](M7_EVIDENCE_LOG.md) 待办挂钩（[CPP_HUB_ABSORPTION_DESIGN](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) §6 既定）+ [调研报告](../spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §6 零成本项 | pending | 学习回路独立议题（不并入其他 feature）：M7 增设 ```hits 机读块（统计可脚本重数/生成）+ 样本追加由手工登记改脚本辅助（`grep -c` 重数先例）；与 dc_validator R7 计数检查衔接 |

## 已完成（近三项）

| 日期 | 事项 | 产出 |
|------|------|------|
| 2026-08-19 | 治理收束轮（遗留任务调研 + 收敛）：M7 样本⑩ 补登（分桶 15→16）+ ADR-0009 失效条件首次重审（机制保留）+ DIS-007 v1.3 追记 DR-6 + LANGGRAPH L26 标注收束 + P-009~P-011 登记 + CODE_WIKI v1.5；**dry-run 自查追加样本⑪**（分桶 16→19——收束轮自身产出 3 计数错 + 1 超前断言，人工机械枚举拦截，规律② 最强实例） | DEV-LOG-004；PROGRESS / ADR-0009 / discoveries README / 007 / LANGGRAPH 全收敛 |
| 2026-08-19 | P-007 Step 5-7（实施+验收）：DC 契约校验器落地 | `scripts/dc_validator.py` + `.pre-commit-config.yaml` + IMPLEMENTATION v1.1 + CHECKLIST v1.0 + M7 样本⑨（分桶 13→15） |
| 2026-08-18 | P-004/P-005/P-006 收束 + P-007 Step 1-4（调研+设计+复验） | commits 7d0255b / 5a5cbd0（已推送）；RESEARCH v1.1 + DESIGN v1.2 |
