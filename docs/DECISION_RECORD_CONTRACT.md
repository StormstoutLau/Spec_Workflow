# 决策记录契约 (Decision Record Contract) — schema 规范与字段映射

---
id: FWK-DECISION-RECORD
type: framework
version: 1.1
status: active
date: 2026-08-23
depends: [FWK-ASSERTION, ADR-0007]
upstream: null
---

> **版本**: v1.1 (2026-08-26; 独立 pass 修正——§3 D2 论据表述修正:检索机制路径从「find_similar_decisions 余弦」改准为「分路径」;P-016 独立 pass 捕获 M7 样本㉗)
> **来源**: 外部框架 schema 吸收，经裁决以独立契约文档形态落地（[ADR-0007](../adr/ADR-0007-unified-document-contract.md) DC4 命名空间登记、front-matter 七字段）
> **定位**: 本仓决策记录的**结构化字段视角契约**——双用途：① 当下为 ADR / M7 样本行 / PROGRESS 裁决提供规范化字段自查视角；② 方向 A（Context Graph 导入）触发时的**唯一字段映射权威**
> **设计裁决**: 落点 / severity 无损分流 / category-entities 分工等关键决策见 [decision-schema DESIGN](../spec/decision-schema/DESIGN.md)（D1-D4）
> **命名约定**: 本契约编号 `FWK-DECISION-RECORD`（FWK 框架族，ADR-0007 附录 A 登记）；字段语义锚定 Semantica `record_decision` 签名，不另造词

---

## 0. 定位与分工（与 FWK-ASSERTION / FWK-FACT-CHECK 的关系）

| | FWK-ASSERTION | FWK-FACT-CHECK | 本契约 (FWK-DECISION-RECORD) |
|---|---|---|---|
| 管什么 | 断言的**证据强度**（A/B/C） | 事实的**内部核查**（单位/时点/归属） | 决策的**结构完整性**（背景/论证/结果/时点/主体） |
| 回答的问题 | 这条断言有没有证据 | 这个事实写没写错 | 这个决策的构成要素齐不齐、可不可溯 |
| 粒度 | 断言级 | 事实类型级 | 决策级 |

**分工红线**：本契约不评估决策对错（那是 REVIEW/审计的事），不评估证据强度（FWK-ASSERTION 管），只规范决策记录的结构字段。**本契约不是验证机制**——它服务的记录视角与验证端（三校验器 + 独立 pass）正交（I-4）。

---

## 1. schema 定义（八字段 + 两时点）

锚定 Semantica `record_decision` 签名（源码级，含输入校验约束）：

| 字段 | 类型 / 约束 | 语义 | 必填 |
|------|------------|------|------|
| category | str，≤100 字符 | 决策类型（本仓枚举：m7_sample / adr / progress_ruling） | ✅ |
| scenario | str，≤5000 字符 | 决策背景——面临什么问题/情境 | ✅ |
| reasoning | str，≤10000 字符 | 决策论证——为什么这样裁（含替代方案否决） | ✅ |
| outcome | str，≤1000 字符 | 决策结果——裁了什么 | ✅ |
| confidence | float 0.0-1.0 | 决策置信度 | ✅（本仓固定 0.9 占位，见 §3 D2 注） |
| entities | List[str] | 关联实体（载体/模块/工具） | 可选 |
| decision_maker | str | 决策主体 | 可选 |
| metadata | Dict | 附加结构化数据（severity 无损存放处） | 可选 |
| valid_from | datetime | 决策生效时点 | 可选 |
| valid_until | datetime | 决策失效时点（bi-temporal；开放决策为 null） | 可选 |

**完整性自查视角（当下用途）**：撰写 ADR / 登记 M7 样本 / 作 PROGRESS 裁决时，可对照本表自查——「背景说了吗（scenario）/ 论证给了吗（reasoning）/ 结果明确吗（outcome）/ 时点标了吗（valid_from）/ 主体是谁（decision_maker）」。缺项即结构不完整（如 DEV-LOG-004「未跑先称 dry-run exit 0」= outcome 无 valid_from 支撑的教训实例）。

---

## 2. 本框架字段映射表（方向 A 导入的唯一权威）

### 2.1 M7 样本行 → record_decision

| M7 列 | 目标字段 | 映射说明 |
|-------|---------|---------|
| #（样本号） | metadata.sample_id | ㉕ 式编号 |
| 日期 | valid_from | |
| 载体 | entities | D4：载体是实体不是类型 |
| 审查配置 | decision_maker + scenario 前缀 | 审查臂（GLM-5.3 / DeepSeek V4 Pro / 工具名）入 decision_maker；配置叙述入 scenario |
| 发现 | scenario（摘要）+ reasoning（归因）+ metadata.severity | **非平凡拆分**（v1.3 §4.3 预检）：发现列混合叙述——严重性概入 scenario、归因分析入 reasoning、P 标记无损入 metadata.severity |
| 形态II复发列 | metadata.form2_count + reasoning（规律锚点引用） | |
| 来源 | metadata.source_anchor | |

### 2.2 ADR → record_decision

| ADR 节 | 目标字段 |
|--------|---------|
| 背景 | scenario |
| 决策 | outcome |
| 论证（含替代方案否决） | reasoning |
| 状态（accepted/superseded） | metadata.status；superseded 时点 → valid_until（bi-temporal） |
| 修订历史 | CAUSED 边链（版本间） |
| id（ADR-000N） | metadata.adr_id |

### 2.3 PROGRESS 裁决 → record_decision

| PROGRESS 元素 | 目标字段 |
|--------------|---------|
| P 编号 | metadata.pid |
| 事项 | scenario |
| 依据列 | reasoning + metadata.basis_docs |
| 验收标准列 | outcome（完成态） |
| 状态 | metadata.status |

### 2.4 关系类型（图边映射）

| Semantica 关系 | 本框架实例 |
|---------------|-----------|
| CAUSED | ADR 修订链（v1.1 因 v1.0 缺陷）；修正轮→前轮残留批 |
| INFLUENCED | 调研→待办实施（P-015→P-016）；规律锚点→后续裁决 |
| PRECEDENT_FOR | M7 样本→规律锚点（⑫→「计划数漂移」规律）；先例裁决→同构后续裁决（㉕→㉖ 分类核验先例引用） |

---

## 3. 关键裁决注记（继承 DESIGN D1-D4）

- **severity 无损分流（D2）**：P1/P2/P3 以字符串原值入 `metadata.severity`，**禁止浮点编码**——Semantica confidence 语义 = 决策置信度 ≠ 发现严重性；且**检索相似度各路径均不消费 confidence**：默认检索（find_similar_decisions → context_graph.py find_precedents_by_scenario）为词袋 Jaccard + 图结构分，语义增强路径（decision_query.py find_precedents_hybrid）为 reasoning_embedding 余弦——两路径均与 confidence 无关（有损编码对检索零贡献）。`confidence` 本仓固定 0.9 占位（「已裁决」标记位语义，非质量度量——本框架无决策置信度数据源，不虚构）
- **category-entities 分工（D4）**：category = 记录类型枚举（m7_sample/adr/progress_ruling），载体入 entities——源码语义：entities 即 Related entities
- **M7「发现」列拆分（非平凡）**：导入时发现列须拆为 scenario（严重性概要）/ reasoning（归因）/ metadata.severity（无损）三路，非整列直拷——方向 A 试点分 ADR 先行（映射干净）/ M7 后行（拆分解析）两批

## 4. 不变式

- **I-1（映射唯一权威）**：本契约是方向 A 导入的唯一字段映射规范——导入实现不得自带映射表（DIS-009 教训：无契约的字段对应产生指代漂移）
- **I-2（severity 无损）**：P1/P2/P3 字符串原值入 metadata，禁止任何浮点编码
- **I-3（不可漂移）**：映射一经登记，修订须版本化（front-matter version 递增 + 修订历史注明变更字段）——跨批次导入的相似度排序依赖字段语义稳定
- **I-4（不进验证端）**：本契约规范记录结构，不构成验证机制；Semantica 侧任何输出不作 E1 证据（承 P-013「硬规则出裁决」/ P-015 约束）

## 5. 修订历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-08-23 | v1.0 | 初版——schema 八字段 + 三载体映射表 + 关系类型 + I-1~I-4（P-016 B 方案契约批；依据 Semantica 0.6.6 源码签名核验） |
| 2026-08-26 | v1.1 | 独立 pass 修正（M7 样本㉗）——§3 D2 论据表述改准：原「find_similar_decisions 检索消费 reasoning_embedding 余弦」改为分路径准确表述（默认 = 词袋 Jaccard + 图结构，语义增强 = hybrid 余弦；两路径均不消费 confidence）。D2 裁决本身不变，仅论据更正（I-3 版本化） |
