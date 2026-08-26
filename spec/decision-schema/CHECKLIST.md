# 审查验收 Checklist：决策记录 schema 吸收（B 方案契约批）

---
id: decision-schema-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-08-23
depends: [decision-schema-DESIGN, FWK-DECISION-RECORD]
upstream: null
---

> **Feature**: decision-schema（PROGRESS P-016）
> **创建日期**: 2026-08-23
> **状态**: 有条件通过（自查全绿 + 四通道机械校验全绿；独立 pass 待触发——同 P-014/P-010 收口先例）
> **Spec 步骤**: Step 7-8, 10
> **基于设计**: [DESIGN.md](./DESIGN.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——独立 pass 待用户触发

---

## 1. 设计一致性验收

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN 决策 D1-D4 均有否决记录与理由 | ☒ 通过 | §2 四决策各含被否决候选（落点 2 候选 / 有损编码 / 单件套余量 / v1.3 sketch 修正） |
| 契约文档与 DESIGN §3 规格一致 | ☒ 通过 | 八字段表 + 三载体映射 + 关系类型 + I-1~I-4 逐项对应 |
| schema 字段锚定源码签名（非转述） | ☒ 通过 | 依据 = SEMANTICA_ABSORPTION_RESEARCH §2.5（A 类源码直读级，record_decision L4078 十参签名） |
| 替代方案 ≥2 否决（DESIGN 模板要求） | ☒ 通过 | §5 三条否决记录 |

## 2. 契约内容验收

| 验收项 | 通过条件 | 状态 | 证据 |
|--------|---------|------|------|
| schema 八字段 + 校验约束完整 | 字段/类型/语义/必填四列齐 | ☒ | 契约 §1 |
| severity 无损分流落地 | metadata.severity 字符串 + confidence 0.9 占位注记 + 禁编码禁令 | ☒ | 契约 §3（I-2） |
| 三载体映射表（M7/ADR/PROGRESS） | 每载体逐字段映射 + 非平凡拆分标注 | ☒ | 契约 §2.1-2.3（M7「发现」列三路拆分已标非平凡） |
| 关系类型三型映射 | CAUSED/INFLUENCED/PRECEDENT_FOR 各有本框架实例 | ☒ | 契约 §2.4 |
| 不变式 I-1~I-4 | 唯一权威 / 无损 / 不可漂移 / 不进验证端 | ☒ | 契约 §4 |
| 与 FWK-ASSERTION/FACT-CHECK 分工表 | 三框架边界无重叠 | ☒ | 契约 §0（分工红线：结构完整性 ≠ 证据强度 ≠ 事实核查） |

## 3. 契约合规与命名空间验收

| 验收项 | 通过条件 | 状态 | 证据 |
|--------|---------|------|------|
| front-matter 七字段（DC1） | id/type/version/status/date/depends/upstream | ☒ | FWK-DECISION-RECORD 头部 |
| type: framework + status: active（DC2 词表） | 同 FWK-FACT-CHECK 形态 | ☒ | 头部 |
| ADR-0007 附录 A 命名空间入册（DC4） | FWK-DECISION-RECORD 行 + 修订历史同步 | ☒ | ADR-0007 v1.3→v1.4 |
| 跨文档引用相对路径（DC3） | 契约内链接可解析 | ☒ | dc_validator M5 验证 |

## 4. 流程裁剪验收（D3）

| 验收项 | 状态 | 说明 |
|--------|------|------|
| RESEARCH 裁剪理由登记 | ☒ | DESIGN 头部「调研依据」+ D3 |
| IMPLEMENTATION 裁剪理由登记 | ☒ | DESIGN D3 + §7 实施规格（单文档产出的过程空转判定） |
| 先例依据 | ☒ | P-012/P-013 单件套先例 + v1.3 §4.3 自身规定「spec 小流程」 |

## 5. 视图层同步验收

| 验收项 | 状态 | 证据 |
|--------|------|------|
| CODE_WIKI §2.1 树（docs 文件 + spec 目录） | ☒ | v1.10 |
| CODE_WIKI §9 索引两行 | ☒ | 契约行 + decision-schema 行 |
| CODE_WIKI §10 declared（13 目录 / 16 任务）+ doc_registry | ☒ | repo_stats 对账 exit 0 |
| PROGRESS P-016 登记 + 已完成表 | ☒ | |
| RESEARCH v1.3 裁决激活注（B 层 → 分层结合） | ☒ | |

## 6. 机械验证（E1 通道）

| 通道 | 结果 |
|------|------|
| dc_validator --check-all | ☒ 通过（新增 3 文件全过 DC1-DC4） |
| m7_stats（账本未被本轮触碰，维持 26/67） | ☒ 通过 |
| repo_stats（视图对账） | ☒ 通过 |
| pre-commit run --all-files（三 hook） | ☒ Passed |

## 7. 验收统计与决定

- **通过项**: 22/22（自查 + 机械）
- **发现**: 本轮实施期 dc_validator/repo_stats 首跑均一次通过——无新增 M7 样本（契约批产出为规范文档，无计数声明位点；D2/D4 在设计期已消解 v1.3 sketch 的有损映射风险）
- **决定**: **有条件通过**——独立 pass（RULE-1 时序独立，真异基座优先）待用户触发；触发后 IMPLEMENTATION 若有修订按契约 I-3 版本化

## 8. ADD 审计（Phase 0 质量门）

| 维度 | 档位 | 说明 |
|------|------|------|
| 可测试约束 | B | I-1~I-4 可机械/review 验证（I-2 severity 无损可 grep 导入产物） |
| 模块映射 | A | 契约 ↔ DESIGN §3 逐节对应 |
| 接口契约 | A | schema 表即接口（字段/类型/约束/必填） |
| 修正项追溯 | A | D1-D4 各含否决记录 |
| 跨模块契约 | A | 与 FWK-ASSERTION/FACT-CHECK 分工表显式 |

**Iron Law 四类盲区自查**: ① 未验证即声明——契约字段全部锚定 §2.5 源码断言，无自述级混入 ✅ ② 边界条件——M7「发现」列拆分已标非平凡（导入期风险前置登记）✅ ③ 自我验证——CHECKLIST 自查 + 四通道机械验证双通道 ✅ ④ 环境维度——契约批零环境依赖（方向 A 环境门槛已在 RESEARCH H4 登记，不属本批）✅

---

**审查签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待触发）
