# 设计文档：决策记录 schema 吸收（B 方案契约批）

---
id: decision-schema-DESIGN
type: design
version: 1.0
status: in-review
date: 2026-08-23
depends: [semantica-absorption-RESEARCH, ADR-0007, FWK-ASSERTION]
upstream: null
---

> **Feature**: decision-schema（PROGRESS P-016，依据 [SEMANTICA_ABSORPTION_RESEARCH](../semantica-absorption/SEMANTICA_ABSORPTION_RESEARCH.md) v1.3 §4.3 B 先行时序）
> **创建日期**: 2026-08-23
> **状态**: in-review（自查完成 + 机械校验全绿；独立 pass 待触发，同 P-014/P-010 收口先例）
> **Spec 步骤**: Step 3-4（设计）+ Step 9-10（执行与收口，见 §7 实施规格）
> **调研依据**: SEMANTICA_ABSORPTION_RESEARCH v1.3——§2.5 源码直读级签名（record_decision 十参 + bi-temporal）+ §4.3 联合实现分析（B 是 A 的数据契约层）

---

## 1. 设计目标

把 Semantica 决策记录 schema 吸收为本仓**决策记录契约**，服务双用途：

1. **结构化（当下）**：ADR / M7 样本行 / PROGRESS 裁决的决策内容获得规范化字段视角——「一个决策 = scenario（背景）+ reasoning（论证）+ outcome（结果）+ 时点」
2. **导入契约（方向 A 触发时）**：Context Graph 导入的唯一字段映射规范——有契约的映射才可溯、可复核、不可漂移（DIS-009 实证：无契约的字段对应产生指代漂移）

**非目标**：不改动任何现有文档的记录格式（ADR_TEMPLATE/M7 表结构不动——契约是叠加视角不是替换）；不引入 Semantica 依赖（零依赖不变式不触）；不建图（那是方向 A 的事）。

## 2. 关键设计决策

### D1. 落点 = 独立契约文档 `docs/DECISION_RECORD_CONTRACT.md`（id: FWK-DECISION-RECORD）

| 候选 | 裁决 | 理由 |
|------|------|------|
| **独立契约文档（采纳）** | ✅ | 与 FWK-ASSERTION / FWK-FACT-CHECK 同层（框架族）；可被方向 A 导入脚本独立引用；ADR-0007 DC4 命名空间登记体系现成（FWK- 前缀 + 附录 A 入册） |
| ADR_TEMPLATE 决策记录节 | ❌ | 模板是「新 ADR 的骨架」不是契约权威；改动波及所有未来 ADR；M7 样本/PROGRESS 裁决不在 ADR 模板管辖内 |
| 并入 FWK-ASSERTION 附录 | ❌ | 主题错位——断言分级管「证据强度」，决策 schema 管「决策结构」；P-005 先例（§0 计数规则落框架而非 ADR）同理需主题对位 |

### D2. severity 无损分流（否决 v1.3 §4.3 的有损编码 sketch）

v1.3 曾提出「severity→confidence 编码（如 P1=0.9/P2=0.5/P3=0.3）须显式契约」。本设计**否决有损编码本身**，改无损分流：

- **依据一（语义）**：Semantica `confidence` 语义 = 决策者对决策的置信度；本框架 P1/P2/P3 = 发现严重性。两者不同轴——编码即语义污染（高严重性发现 ≠ 高置信度决策）
- **依据二（源码，§2.5）**：find_similar_decisions 的检索相似度消费的是 `reasoning_embedding` 余弦，**不消费 confidence**——有损编码对检索质量零贡献，纯损失
- **裁决**：`severity` 以字符串原值入 `metadata`（"P1"/"P2"/"P3"——无损可逆）；`confidence` 登记固定占位值 0.9 + 契约注记（「已裁决」标记位语义，非质量度量——本框架无决策置信度数据源，不虚构）

### D3. 小流程裁剪：DESIGN + CHECKLIST 两件套（RESEARCH/IMPLEMENTATION 裁剪）

- **RESEARCH 裁剪**：调研已完成——semantica-absorption RESEARCH v1.3（25A 源码级）即本 feature 的调研依据，重复调研零增量
- **IMPLEMENTATION 裁剪**：实施 = 新建 1 份契约文档 + 视图同步 + ADR-0007 附录 A 补登（§7 实施规格已在本文档登记，CHECKLIST 逐项验收）——独立 IMPL 文档对单文档产出是过程空转
- **先例**：P-012/P-013 RESEARCH-only 单件套；本 feature 两件套居间，与 v1.3 §4.3 自身规定的「spec 小流程」一致

### D4. category = 记录类型，载体入 entities（细化 v1.3 映射 sketch）

v1.3 sketch 曾把「载体→category」。源码语义核正：Semantica `entities` 字段即「Related entities」（实体关联），载体（CODE_WIKI/PROGRESS/...）是实体不是决策类型。裁决：`category` = 记录类型枚举（m7_sample / adr / progress_ruling），`entities` = 载体/涉及模块列表。

## 3. schema 规格（契约核心，落地于 DECISION_RECORD_CONTRACT.md）

八字段（源码签名，§2.5 A 类断言）+ 本框架映射：

| 字段 | 类型 | M7 样本行映射 | ADR 映射 | PROGRESS 裁决映射 |
|------|------|--------------|----------|------------------|
| category | str≤100 | "m7_sample" | "adr" | "progress_ruling" |
| scenario | str≤5000 | 审查配置 + 发现摘要 | 背景（问题陈述） | 裁决问题 |
| reasoning | str≤10000 | 形态 II 归因 + 规律锚点分析 | 论证（含替代方案否决） | 裁决依据分析 |
| outcome | str≤1000 | 处置（入账/修正/分流） | 决策内容 | 裁决结果 |
| confidence | float | 0.9 固定占位（D2） | 0.9 固定占位 | 0.9 固定占位 |
| entities | List[str] | [载体名] | [涉及模块/工具] | [涉及 feature] |
| decision_maker | str | 审查臂（GLM-5.3 / DeepSeek V4 Pro / dc_validator 等工具名） | 决策主体（单人仓 = 用户/实施者） | 用户 / 实施者 |
| metadata | Dict | {样本号, severity, 形态II数, 来源锚点} | {ADR编号, status, 替代方案数} | {P 编号, 依据文档} |
| valid_from | datetime | 样本日期 | ADR date | 裁决日期 |
| valid_until | datetime? | null（开放） | superseded 时点（bi-temporal） | null |

关系类型映射（导入时图边）：

| Semantica | 本框架实例 |
|-----------|-----------|
| CAUSED | ADR 修订链（v1.1 因 v1.0 缺陷）；修正轮→前轮残留 |
| INFLUENCED | 调研→待办实施（P-015→P-016）；规律锚点→后续裁决 |
| PRECEDENT_FOR | M7 样本→规律锚点（⑫→「计划数漂移」规律）；先例裁决→同构后续裁决（㉕→㉖ 分类核验） |

## 4. 不变式

- **I-1（映射唯一权威）**：本契约是方向 A 导入的唯一字段映射规范——导入脚本不得自带映射表
- **I-2（severity 无损）**：P1/P2/P3 字符串原值入 metadata，禁止任何浮点编码（D2）
- **I-3（不可漂移）**：映射一经登记，修订须版本化（契约 front-matter version 递增）且在修订历史注明变更字段——跨批次导入的相似度排序依赖字段语义稳定
- **I-4（不进验证端）**：本契约规范记录结构，不构成验证机制；Semantica 侧任何输出不作 E1 证据（承 P-013/P-015 约束）

## 5. 替代方案（否决记录）

1. **完全不吸收（维持 v1.0 裁决态）**：否决——用户已裁决启动 B；且无契约的 A 导入已论证为 DIS-009 风险面
2. **吸收为 ADR_TEMPLATE 内嵌节**：否决（见 D1）
3. **有损 severity 编码**：否决（见 D2）

## 6. 风险

| 风险 | 缓解 |
|------|------|
| 契约与未来 Semantica 版本签名漂移（0.x 阶段 breaking 可能） | 契约锁定「依据 = v1.2 源码核验（semantica 0.6.6）」；方向 A 试点时核对签名，漂移则契约升版 |
| 无人消费的契约沦为僵尸文档 | 双用途中「结构化视角」即刻生效（M7 样本登记/ADR 撰写时可参照字段自查完整性）；ADR-0009 失效条件机制兜底 |

## 7. 实施规格（Step 9 执行清单）

| # | 动作 | 文件 |
|---|------|------|
| 1 | 新建契约文档 | docs/DECISION_RECORD_CONTRACT.md（FWK-DECISION-RECORD v1.0，type: framework） |
| 2 | 命名空间入册 | adr/ADR-0007 附录 A 加 FWK-DECISION-RECORD 行 + 修订历史一行（v1.3→v1.4，先例 2026-08-21 FWK-FACT-CHECK 补登） |
| 3 | 裁决激活注 | semantica-absorption RESEARCH v1.3 裁决记录节补一行（B 层激活 → 分层结合） |
| 4 | PROGRESS 登记 | P-016 行（done）+ 已完成表 |
| 5 | CODE_WIKI 同步 | v1.10：§2.1 树（docs 文件 + spec/decision-schema/）+ §9 索引两行 + §10 declared（spec_feature_dirs 13 / progress_tasks 16）+ doc_registry |
| 6 | 终验 | dc_validator --check-all / m7_stats / repo_stats / pre-commit 三 hook |

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成；独立 pass 待触发）
