# DEV-LOG-017: 回写流与多方案决策路径能力盘点（P-050：Q1/Q2 判定与多轮后续阶段）

> **日期**: 2026-09-27 至 2026-09-29（回补）
> **会话**: `specwf-p050-20260927`（五步链）· `specwf-p050-20260927v2` 至 `v9`（补充扫描 / 吃狗粮整改 / 引用订正 / 交付 A 实施 / 交付 B 规格自审 / FTA 判据 / FTA 观察项 / Step 8 独立审查 / 交付 B 实施 / 跨仓对照）· `specwf-p050-20260929`（状态真值源位置候选登记）
> **涉及**: `spec/rework-and-decision-paths/`（RESEARCH v1.0 → v1.10 / DESIGN v1.0 → v1.6 / IMPLEMENTATION v1.0 → v1.3 / CHECKLIST v1.0 → v1.4 accepting）· `scripts/dc_validator.py`（交付 A 扩展 M4 双分支；交付 B 增 design 词表 `superseded`）· `spec/doc-contract/PLAN.md`（DC2 词表增补追记）· `adr/ADR-0007`（D4 追记）· `docs/PROGRESS.md`（P-050 行）· `CODE_WIKI.md`（v1.61 → v1.71）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-050 行](../PROGRESS.md) · [RESEARCH](../../spec/rework-and-decision-paths/RESEARCH.md) · [DESIGN](../../spec/rework-and-decision-paths/DESIGN.md) · [IMPLEMENTATION](../../spec/rework-and-decision-paths/IMPLEMENTATION.md) · [CHECKLIST](../../spec/rework-and-decision-paths/CHECKLIST.md) · [CODE_WIKI](../../CODE_WIKI.md)

## 做了什么（时序）

1. **Step 1-2 调研落档（RESEARCH-only，第 34 个 feature 目录）**：先本仓机械取证（E1/E2）再引外部证据（E3）。**Q1 判定 = 部分具备**（`spec_runner fork` 是唯一**能产出新事件流**的写入命令，但缺触发判据、缺失效标记词汇、缺返工图登记）；**Q2 判定 = 部分具备**（依赖图与多方案加权评分两项半有载体；故障依赖链 / 顺序依赖 / 短长期成本收益三项空白）。结构性结论 = 本仓**状态表达能力远强于关系表达能力**，缺口全落在关系侧。RESEARCH **v1.0**（12A+4B+3C+3H）。
2. **补充扫描轮（v1.1）**：用户追加第三问 ⇒ §3.8 三项成立候选（PROGRESS 四态实际退化为一态 / 决策记录契约十字段零机械消费 / CHECKLIST 条目级无机械重数）+ **一项负结果**（`upstream` 候选被推翻：`null` 系契约正确值而非字段闲置）+ 两项反例（`confidence` / ADR `superseded`）。断言计数升为 **24A+12B+5C+6H**。
3. **吃狗粮整改轮（v1.2）**：同基座独立 pass（RULE-5 降级标注），**7 项发现（2 P1 + 2 P2 + 3 P3）全部整改**；补建 `specwf-p050-20260927v2.jsonl`（F1 结构性覆盖缺口）；M7 样本 **#35** 入账（samples 34 → 35）。
4. **引用订正轮（v1.3）**：全篇 A-7 引的「ADR-0007 D5」实为「G2 双语取舍」，design 入词表的正确出处 = **ADR-0007 D4** + `PLAN.md` §1 DC2；M7 样本 **㊱**。
5. **交付 A 实施（CHECKLIST 条目级重数）**：扩展 `dc_validator` **M4 为双分支**（§0 断言统计表逐字平移 + §10.1 验收统计新增）；selftest **15 → 24/24**；实测 21 个 CHECKLIST 分三族 + 四种子偏差。
6. **交付 B 规格自审批（v1.4 / DESIGN v1.1）**：对 DESIGN §7 做同基座规格自审，**10 项发现（3 P1 + 3 P2 + 4 P3）全部修订**；**关键改判 = 只增一词、不增字段**（DC1 零改动）；M7 样本 **㊲**。
7. **R2/R3 故障链（FTA）判据批（v1.5 / DESIGN v1.2）**：R3 倾向否决（不设 `superseded_by`）、R2 判**不可裁**（对称）；方法边界 = **判据选择器而非生成器**。
8. **FTA 工具化观察项登记（v1.6 / DESIGN v1.3）**：固化 3 条触发条件 + 载体预判 + 未触发处置。
9. **Step 8 独立审查批（v1.7）**：7 项发现（2 P2 + 5 P3）全整改；**元发现 = 增长型载体计数漂移第三度复发**；M7 样本 **㊳**。
10. **交付 B 实施批（v1.8 / DESIGN v1.5）**：`superseded` 入 design **一般档**，改 **4 权威位点 + 3 模板**；**R2 触发驱动** ⇒ CHECKLIST 档与 `template` 类不增；**R3 未采纳**。
11. **跨仓对照观察项登记批（v1.9）**：核验 `D:/RPC` 三条意见，意见 1/2 可采纳机制升级为 **H-RPC1 / H-RPC2** 观察项，意见 3 未纳入。
12. **状态真值源位置候选登记批（v1.10，2026-09-29）**：§3.8.7 候选 ④ + 观察项（零代码、零断言计数变更）。

## 决策依据

### ① 两问判定均为「部分具备」而非「具备 / 不具备」

取证先行：本仓已有 `spec_runner fork`（复制前 N seq 行至新流）这一机械通路，且实践中回写已发生（P-028 v1.1 用新 session 重入上游、P-023 以两条 decision 回溯补记）——但**失效表达能力严重不对称**：ADR 层有 `superseded` + `upstream` 反向设置与 bi-temporal，四件套 design 词表却只有 `draft/in-review/verified` 且全仓词表「不得自造」⇒ 上游被推翻时**无合法状态可标记作废**，只能追记。故判「部分具备」（源：RESEARCH §3 / PROGRESS P-050 行）。

### ② 交付 B 最小切口 = 「只增一词、不增字段」

规格自审 **P1-B2** 发现：将 `superseded_by` 作「front-matter 第 8 字段」与 **DC1 七字段**冲突，且 `check_frontmatter` 只检缺字段 ⇒ 冲突会**静默通过**机械校验。故改判为**只增 design 词表一词**（DC1 零改动），并采纳本仓既有 `upstream` 反向约定而非新造字段（新造字段会过载 `downstream_compliance.py` 的语义消费，产错误标签）。落 4 权威位点 + 3 模板（源：PROGRESS P-050 行 ⑤/⑨）。

### ③ R3 不设 `superseded_by`（FTA 倾向否决）

以 FTA 建树：不设（仅正向 `upstream`）割集 3 元素；设则消除 T2 但**新增「链不一致」2 元素割集**（欲消需加一致性校验器 ⇒ 校验器自身成新失效面）。结论与 **I-10「单一实现」论证结构独立收敛**（交叉验证而非重复）（源：PROGRESS P-050 行 ⑥）。

### ④ R2 判「不可裁」而非强判

R2 不覆盖割集 3 元素、覆盖后降 2 但新增割集 2 ⇒ 规模相当、方向相反 = **对称**，FTA 不产生裁决（**否定性结论有效**）⇒ 依 ADR-0010 **Q2 回归触发驱动**（源：PROGRESS P-050 行 ⑥）。

## 遇到的问题

- **增长型载体计数漂移三度复发**：Step 8 独立审查刷新四项读数（CONSOLE 阶段、触发行数、confidence、CHECKLIST 标记），**同日即漂移** ⇒ 强化候选规则「读数须附口径 + 读数日期」（源：PROGRESS P-050 行 ⑧）。
- **「声明计数 ≠ 枚举明细」**：交付 B 规格自审与 Step 8 均出现正文散文计数与枚举不符，根因指向 **R7 管辖边界缺口**（机械重数只落 §0 / §10.1）（源：PROGRESS P-050 行 ⑤/⑧）。
- **四项局限显式登记**：E3 均为检索摘要未原文精读 / P-033 权重未复核 / H1（`fork` 是否已实际用于回写）未实测 / H2 短长期时间尺度未定义 / H3 社区方法适配成本未评估（源：RESEARCH §5.2 与附录 C）。

## 下一步

- **交付 B 已实施**；**故障链 / 关键路径 / 成本收益三项各自单独评估**、触发驱动、未激活副作用 0（源：PROGRESS P-050 行）。
- **FTA 工具化观察项**与 **H-RPC1 / H-RPC2 观察项**均登记、触发未满：结构化分叉需求累计 < 3 例时不动（源：RESEARCH §6）。
- **§3.8.7 状态真值源位置候选 ④**：触发条件三者均未现（真实误判或返工 0 例 / 用户裁决 / P-039 P-c 分发落地），当前不动（源：PROGRESS P-050 行 ⑪）。