# 审查验收 Checklist：回写流与多方案决策路径（P-050 后续阶段）

---
id: rework-and-decision-paths-CHECKLIST
type: design
version: 1.8
status: accepting
date: 2026-10-19
depends: [rework-and-decision-paths-IMPLEMENTATION, rework-and-decision-paths-DESIGN]
upstream: null
---

> **Feature**: 回写流与多方案决策路径（P-050 后续阶段）
> **创建日期**: 2026-09-27
> **状态**: accepting（验收中；**v1.8 增记 P-101 U-9 实施（视图侧返工行动档；经用户裁决支路开闸、推翻 P-097 defer；P-103 回写订正）** / **v1.7 增记 P-092 U-8 门禁链实施** / v1.6 增记 P-089 U-10′ 薄壳实施 / v1.5 增记 P-069 三问续研 Layer-1 最小实施 / v1.4 版本引用收口 / v1.3 增记交付 B 实施 / v1.2 增记 Step 8 独立审查 7 项整改）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [IMPLEMENTATION.md](./IMPLEMENTATION.md) **v1.6**
> **基于设计**: [DESIGN.md](./DESIGN.md) **v1.9**
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.13**
> **v1.5 变更（2026-10-03，三问续研 Layer-1 最小实施）**：用户指令「按这个方案落档并实施」⇒ 记录 **P-069**（受控回边受理 + `backflow-audit` 只读子命令 + selftest **54/54 → 63/63**）的验收——新增 **F9~F12**（功能）/ **I5**（接口）/ **E5**（错误处理）/ **C4**（兼容性）/ 不变式 **I-16~I-18** 三行；§1 交叉版本同步至 **RESEARCH v1.11 / DESIGN v1.7 / IMPL v1.4**；**§10.1 计数 33 → 44（通过 32 → 43）**。**既有 F1~F8 / I1~I4 / E1~E4 / C1~C3 判定语义零改动**（回边受理为**放宽**，不触碰分支①②）。
> **v1.6 变更（2026-10-12，U-10′ 薄壳实施 · P-089）**：用户指令「按照顺序 用吃狗粮模式执行下一个」（承 [DESIGN §10.5](./DESIGN.md) 裁定 B）⇒ 记录 **P-089**（`fork` 注册三件 all-or-none + 写入端 fail-fast 子集直写返工图 + selftest **63/63 → 71/71**）的验收——新增 **F13~F16**（功能）/ **I6**（接口）/ **E6~E7**（错误处理）/ **C5**（兼容性）/ 不变式 **I-19~I-21** 三行；§1 新增 P-089 可追溯行并同步交叉版本至 **RESEARCH v1.12 / DESIGN v1.8 / IMPL v1.5**；**§10.1 计数 44 → 56（通过 43 → 55）**。**既有 F1~F12 / I1~I5 / E1~E5 / C1~C4 判定语义零改动**（本批只扩 `fork` 命令面）。
> **v1.7 变更（2026-10-13，U-8 门禁链实施 · P-092）**：用户指令「继续执行下一个任务」（承 [DESIGN §10.6](./DESIGN.md) 三轴裁定）⇒ 记录 **P-092**（`finalize` 决策强制 `metadata.upstream_impact` 三态 + 过渡期机械边界 `P ≥ 92` + selftest **71/71 → 81/81**）的验收——新增 **F17~F19**（功能）/ **I7**（接口）/ **E8**（错误处理）/ **C6**（兼容性）/ 不变式 **I-22**；§1 新增 P-092 可追溯行并同步交叉版本至 **RESEARCH v1.13 / DESIGN v1.9 / IMPL v1.6**；**§10.1 计数 56 → 64（通过 55 → 63）**。**既有 F1~F16 / I1~I6 / E1~E7 / C1~C5 判定语义零改动**（本批只增一处门禁硬性组）。
> **v1.4 变更（2026-09-27，跨仓对照观察项登记 + 版本引用收口）**：用户指令「D盘 RPC框架对本框架的意见 请分析是否合理」⇒ 观察项登记落 [RESEARCH §6](./RESEARCH.md) / [DESIGN §10.2](./DESIGN.md)（**H-RPC1 / H-RPC2**）；本文件**收口版本引用 + 同步交付 B 状态**——§1 交叉表与三条「基于」行此前**滞后**于 RESEARCH v1.8 / DESIGN v1.5 / IMPL v1.2（与 S8-1/S8-2 同族复发），现同步至 **v1.9 / v1.6 / v1.3**；§10.2「交付 B 未实施」与 §11 矛盾（v1.3 遗漏）→ 改为「已实施」；§11 新增 **H-FTA / H-RPC1 / H-RPC2** 观察项行。**§10.1 计数不变**（真异基座 pass 仍为唯一待办）。
> **v1.3 变更（2026-09-27，交付 B 实施）**：用户裁决「两项都做」⇒ 记录 **D-B2 实施**（`superseded` 入 design 一般档，4 权威位点 + 3 模板；[IMPLEMENTATION §11](./IMPLEMENTATION.md)）+ §11 交付 B 行由此前「待裁决」改为「已裁决并实施」（R2 触发驱动 / R3 倾向否决）。**§10.1 计数不变**（真异基座 pass 仍为唯一待办）。
> **v1.2 变更（2026-09-27，Step 8 独立审查整改）**：记入 **Step 8 独立审查**（子代理 / 同基座降级）结果 —— **7 项发现（2 P2 + 5 P3）全部整改**（记录见 [RESEARCH §5.5](./RESEARCH.md)）；同步 §1 交叉版本表、§8.4、§11 与三条「基于」行版本（S8-1/S8-2）。**§10.1 计数不变**（真异基座 pass 仍为唯一待办）。

---

## 1. 文档一致性验收（Step 8）

| 检查项 | 状态 | 说明 |
|--------|------|------|
| RESEARCH → DESIGN 设计决策可追溯 | ✅ | DESIGN §2.1 逐条引 RESEARCH §3.1/§3.8 |
| DESIGN → IMPLEMENTATION 模块可追溯 | ✅ | IMPLEMENTATION §3.1/§3.2 对应 DESIGN §4 |
| 无文档间矛盾（RESEARCH v1.13 ↔ DESIGN v1.9 ↔ IMPL v1.6） | ✅ | 机械复核（v1.7 重数） |
| P-069 三问可追溯（RESEARCH §3.9 ↔ DESIGN §8 I-16~I-18 / §10.4 ↔ IMPL §12） | ✅ | 逐条对应（三问判定 / 三条不变式 / 三条未决项 / 实施读数） |
| P-089 U-10′ 薄壳可追溯（RESEARCH §3.9.5 ↔ DESIGN §8 I-19~I-21 / §10.5 ↔ IMPL §13） | ✅ | 逐条对应（A/B 裁定 B / 三条不变式 / 回退点 R-7 / 通过门 / 实施读数） |
| P-092 U-8 门禁链可追溯（RESEARCH §3.9.5 ↔ DESIGN §8 I-22 / §10.6 ↔ IMPL §14） | ✅ | 逐条对应（三轴裁定 A/B/C / 不变式 I-22 / 回退点 R-10 / 通过门 / 实施读数） |

## 2. 功能验收

| # | 验收项 | 判据 | 状态 | 证据 |
|---|--------|------|------|------|
| F1 | 分支② 规范+自洽 → 通过 | 零结果 | ✅ | selftest F12 |
| F2 | 分支② 总计列错 → P1 | `总计列 总数 9 ≠ 类行求和 8` | ✅ | selftest F13 |
| F3 | 分支② 行内算术错 → P1 | `行「功能」总数 2 ≠ 通过+失败+待办 1` | ✅ | selftest F13b |
| F4 | 分支② 非整数单元格 → skip | `severity=""` + `非纯整数` | ✅ | selftest F14 |
| F5 | 分支② 异形标题 → skip | `severity=""` + `标题形态异形` | ✅ | selftest F15 |
| F6 | 模板 §10.1 追加规范约束 | 3 条约束落文档 | ✅ | `CHECKLIST_TEMPLATE.md` §10.1 |
| F7 | 全量实跑：Phase 0 全规范文件零违规 | `promptfoo-m7-eval` 不报 | ✅ | 123 文件 0 违规 |
| F8 | 全量实跑：历史异形零阻断 | 6 条 §10.1 skip、P1/P2=0 | ✅ | 123 文件 0 违规 |
| F9 | 受控回边受理 | `step-gate` 对 `research→design→implement→research` 判 **exit 0** 且打印 `[REWORK]` | ✅ | selftest F55 |
| F10 | 同位重复仍判硬性 | 连续同 `step_seq` 重复 → **exit 1** | ✅ | selftest F56 |
| F11 | `backflow-audit` 三信号 | 干净链 exit 0 / 回边·trigger 待处理 exit 1 / 非法枚举 exit 1 | ✅ | selftest F53/F54/F57/F58/F59 |
| F12 | `backflow-audit` 真机读数 | 93 session（含本批 1 条）/ 待处理 0 例 → **exit 0** | ✅ | IMPLEMENTATION §12（2026-10-03） |
| F13 | `fork` 注册成功（三件给定） | exit 0 + 边字段齐（new/origin/seq_from/trigger_kind/reason/provenance/date）+ `seq_from` = 实际复制行数 + `updated` 盖戳 | ✅ | selftest F62 |
| F14 | 无注册参数零回归 | registry 字节不变 + 无 `register:` 行（F9/F10 原断言并存） | ✅ | selftest F63 |
| F15 | 注册输入 fail-fast 族 → exit 2 且零写入 | all-or-none 缺件 / 非法触发枚举 / provenance 三臂（缺冒号 · 前缀越界 · 载荷空）/ 登记表缺失，四种输入全拒且无半成品 | ✅ | selftest F64/F65/F66/F68 |
| F16 | `new` 在已登记名集 → 拒绝 | exit 2 且零写入（注册层去重；与 target-exists 为两道独立闸） | ✅ | selftest F67 |
| F17 | `finalize` 缺 / 非法 `upstream_impact` → 硬性 | exit 1（`upstream_impact` ∉ `IMPACT_STATES` 三态封闭集） | ✅ | selftest F72/F73 |
| F18 | `finalize` `upstream_impact` 三态判定 | `none` → 通过；非 `none` 未登记返工图 → exit 1；非 `none` 已登记 → exit 0 | ✅ | selftest F74/F75/F76 |
| F19 | 过渡期机械边界（P 编号 ≥ 92 才适用） | 历史批次 / sid 形态不匹配 → **不适用**（判定为空）；返工图不可用 → 降级**软性** | ✅ | selftest F77/F78/F79 |

## 3. 接口验收

| # | 验收项 | 判据 | 状态 |
|---|--------|------|------|
| I1 | `parse_checklist_stats` 签名与 DESIGN §5.1 一致 | 返回 `(rows, total)` | ✅ |
| I2 | `_counting_checklist` 判定表六条件齐 | 通过/P1×2/skip×3/无结果 | ✅ |
| I3 | `check_counting` 双分支可独立命中 | F4（分支①）+ F12（分支②）并存 | ✅ |
| I4 | 无 §10.1 → 无结果 | 零结果 | ✅ |
| I5 | `backflow-audit` CLI + 单一实现 | `[--session <sid>]` exit 0/1/2；`_decision_chain` 由 `step-gate` 与 `backflow-audit` 共用（守 I-10） | ✅ |
| I6 | `fork` 注册三件 all-or-none + 值域读真值源 | 全缺 = 原行为；缺一 = exit 2；触发枚举 / 前缀不复制常量（守 I-17）；registry 解析由注册写入与 `backflow-audit` 共用（`_load_registry_raw` / `_registry_derive`） | ✅ |
| I7 | `_finalize_impact_check` 单点实现 + 四类规则 | `cmd_gate_step` 规则由三类 → **四类**（`step-enforce` 经复用自动继承）；**不写入** `_decision_chain`（保其纯性并被 `backflow-audit` 共用，守 I-10） | ✅ |

## 4. 不变式验收

| 不变式（DESIGN §8） | 验证方式 | 状态 |
|---|---|---|
| I-11 规范即自洽 | F12（通过）/ F13 / F13b（P1） | ✅ |
| I-12 R7 位点单一宿主 | 全文 grep：判定仅存于 `dc_validator` M4 | ✅ |
| I-13 渐进不追溯 | F14 / F15 + 全量实跑 P1/P2=0 | ✅ |
| I-14 分支互不干扰 | F4 与 F12-F18 并存 PASS | ✅ |
| I-15 交付 B 零运行时足迹 | 词表未动，F3b/F3c 仍 PASS | ✅ |
| I-16 受控回边受理（回归面只减不增） | F9（回边 exit 0）/ F10（同位重复 exit 1）+ 全量回归 87 pass 逐例一致 | ✅ |
| I-17 触发枚举单一真值源 | `backflow-audit` 读 `docs/rework-graph.json`；全文 grep 无复制常量 | ✅ |
| I-18 `backflow-audit` 只读不接门禁 | `.pre-commit-config.yaml` 未改；只 stdout；F53~F61 全通过 | ✅ |
| I-19 写入端只做 fail-fast 子集 | F65/F66/F67/F68（子集拒绝）+ 单判定 E2E（真对账器对写入边零判红）；C/D 段零复刻（全文可见） | ✅ |
| I-20 `fork` 复制语义零改动 | F63（registry 字节不变）+ F9/F10 原断言并存；校验先于写入（F64~F68 零写入断言） | ✅ |
| I-21 登记值 = 机械真值 | F62（`seq_from` = 请求值 = 实际行数）/ F69（请求超末端按实况）；dump 往返字节保真（E1 实测） | ✅ |
| I-22 `finalize` 三态强制面与过渡期机械边界（P-092） | F17/F18（强制面 + 耦合）/ F19（过渡期边界 + 降级臂）/ C6（存量逐例零回归） | ✅ |

## 5. 错误处理验收

| # | 错误场景（DESIGN §7） | 预期 | 状态 | 证据 |
|---|----------------------|------|------|------|
| E1 | 表结构不全（缺类行/总计行） | skip | ✅ | `M7_HITS_CHECKLIST.md` 实跑 |
| E2 | 单元格非纯整数 | skip | ✅ | `downstream-compliance` 实跑 |
| E3 | 围栏内示例 | 无结果 | ✅ | selftest F17 |
| E4 | 普通小节标题（正文含「验收统计」） | 无结果 | ✅ | selftest F18 |
| E5 | `backflow-audit` 登记表缺失/不可解析 | 降级 **exit 2**（不当作通过） | ✅ | selftest F61 |
| E6 | 登记表缺失/不可解析（注册路径，P-089） | 前置失败 **exit 2**（fork 不发生——校验先于一切写入） | ✅ | selftest F68 |
| E7 | provenance 形态非法（缺冒号 / 前缀越界 / 载荷空，P-089） | **exit 2** 且零写入 | ✅ | selftest F66 |
| E8 | `finalize` 三态强制面错误族（DESIGN §10.6 边界⑤，P-092） | 缺 / 非法 `upstream_impact` → **硬性 exit 1**；非 `none` 耦合未登记 → 硬性；返工图不可用 → 非 `none` 耦合**降级软性**（人工复核，**不静默当作通过**） | ✅ | selftest F72/F73/F75/F79 |

## 6. 性能验收

| # | 项 | 判据 | 状态 |
|---|---|------|------|
| P1 | 单遍线性解析（无嵌套循环/回溯） | 代码审查 | ✅ |
| P2 | 零新增 I/O（逐文件一次读取） | 与既有 M4 同形态 | ✅ |

## 7. 兼容性验收

| # | 项 | 判据 | 状态 |
|---|---|------|------|
| C1 | 分支① 逐字平移零破坏 | F4 / F9 仍 PASS | ✅ |
| C2 | stdlib only（零新依赖） | import 面零新增第三方 | ✅ |
| C3 | pre-commit hook 零改动 | `.pre-commit-config.yaml` 未改 | ✅ |
| C4 | 既有 session 回归逐例一致 | 93 session：87 pass / 5 无 decision / 1 soft，与改前一致（零新硬性错误） | ✅ |
| C5 | 既有 `fork` / `backflow-audit` 行为零变化（P-089） | F9/F10/F63（fork 零回归）；`backflow-audit` 真机 exit 0（registry 解析拆分后语义逐字保持） | ✅ |
| C6 | 存量 session 逐例零回归（P-092） | 115 session（含 finalize 103）：U-8 新增组新增判定项 **0**（硬 0 / 软 0），旧判定分布逐例不变 | ✅ |

## 8. ADD 审计（Step 10）

### 8.1 Spec 质量门（Phase 0）

| 维度 | 得分（0-1） | 说明 |
|------|-----------|------|
| 可测试约束 | 1.0 | 5 条不变式全部有 fixture 对应 |
| 模块映射 | 1.0 | 设计模块 ↔ 实施位置一一对应 |
| 接口契约 | 1.0 | DESIGN §5 签名 = 实现 |
| 修正项 | 1.0 | DR-A1/D2/D3 三处实施期发现均处置 |
| 跨模块契约 | 1.0 | 仅触 `dc_validator` + 模板，边界清晰 |
| **总分** | 5/5 | **档位**: A |

### 8.2 ADD 审计发现

| 严重性 | 发现 | 证据 | 修复建议 |
|--------|------|------|---------|
| P1 | **交付 B 规格**：原语命令面事实错误（`fork --seq-from` 非 CLI flag；漏必需 `--new`/`--session`） | DESIGN §9.5 **B-1**（源码 L485-505/L540-544 实读） | ✅ 已修（DESIGN **v1.1** §7.1） |
| P1 | **交付 B 规格**：`superseded_by` 作「第 8 字段」与 **DC1 七字段**冲突，且未列影响面/未裁决 | DESIGN §9.5 **B-2** | ✅ 已修（§7.2 改判「不增字段」+ §7.3 预留 DC1 条件行） |
| P1 | **交付 B 规格**：方案不最小（未采纳既有 `upstream` 约定，反新增字段） | DESIGN §9.5 **B-3** | ✅ 已修（§7.2 补四点论证） |
| P2 | **交付 B 规格** 3 项：模板计数自相矛盾 / 词表**档**未指明 / 资格丢失 | DESIGN §9.5 **B-4/B-5/B-6** | ✅ 已修 |
| P2 | **同缺陷源留痕**：B-1/B-6 两处同时存在于 **RESEARCH L103**，已连续逃过 2 轮审查 | DESIGN §9.5 元发现 | ✅ 已修（RESEARCH **v1.7**）；登记 **M7 样本 ㊲** |
| P3 | **交付 B 规格** 4 项：引用行号偏差 / 三问 Q1 无论证 / 新流-原流关联登记缺 / 部分推翻未声明边界 | DESIGN §9.5 **B-7~B-10** | ✅ 已修（§7.3/§7.4/§7.2-3/§7.5） |
| P3 | `dc_validator` 与 `repo_stats` 的 **P3 语义分歧**（前者把 P3 算违规，后者非阻断） | DR-A1 | 另立观察项；本批不改 `Summary` |

> **来源声明**：上表与「交付 B 规格」相关的 6 行均来自 **v1.1 同基座自审**（RULE-5 异质性**未达成**，**不替代** §8.4 的异基座独立 pass）。

### 8.3 ADD Iron Law 检查

- [x] 断言恒真式：F13/F13b 断言的 P1 由**错误 fixture** 触发，非恒真；
- [x] 单文件检查盲区：全量实跑 123 文件（非仅 fixture）；
- [x] 设计文档独有约束无测试：5 条不变式各有 fixture；
- [x] 修正阻断性项无测试：DR-A2/A3 各补 F17/F18。

### 8.4 独立 pass（RULE-1 / RULE-5）

- [x] **规格自审（同基座，v1.1）**：对**交付 B 规格**（DESIGN §7）执行专项审查 → **10 项发现（3 P1 / 3 P2 / 4 P3）全部修订**（DESIGN §9.5）；**异质性未达成**（同模型、同时序）⇒ 结论**降级标注**，**不替代**下行
- [x] **Step 8 独立审查（子代理，同基座降级，v1.2）**：对**四件套整体**执行 Step 8 审查 —— **RULE-1 取证清单** = 决策流 `specwf-p050-20260927v3`~`v6` 全部 `verify-anchor` exit 0（锚点 10/6/5/5 全真实）+ git HEAD `fbfe3ff` 工作区净；**RULE-5 异质性未达成**（子代理**同基座**、本环境无换基座能力）⇒ 降级标注。**7 项发现（2 P2 + 5 P3）全部整改**（记录见 [RESEARCH §5.5](./RESEARCH.md)；**M7 样本 ㊳**）。**元发现 = 增长型载体计数漂移第三度复发**
- [ ] **真异基座独立 pass（仍待触发）**：需**换基座模型**（RULE-5 完全满足）方可关闭；本环境不可得（审查输入 = 决策流 + `verify-anchor` + `git status`）

## 9. 文档完整性

| 文档 | 存在 | 与实现一致 |
|------|------|----------|
| RESEARCH.md | ✅ | ✅ |
| DESIGN.md | ✅ | ✅ |
| IMPLEMENTATION.md | ✅ | ✅ |
| CHECKLIST.md（本文件） | ✅ | ✅ |
| ADR（本批无新增） | — | — |
| 开发日志 | — | — |

## 10. 验收结论

### 10.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|------|------|------|------|------|
| 文档一致性 | 6 | 6 | 0 | 0 |
| 功能 | 19 | 19 | 0 | 0 |
| 接口 | 7 | 7 | 0 | 0 |
| 不变式 | 12 | 12 | 0 | 0 |
| 错误处理 | 8 | 8 | 0 | 0 |
| 性能 | 2 | 2 | 0 | 0 |
| 兼容性 | 6 | 6 | 0 | 0 |
| ADD 审计 | 4 | 3 | 0 | 1 |
| **总计** | 64 | 63 | 0 | 1 |

> **统计口径（RULE-2）**：上表来自本文件**逐项核对**（每一项均有独立标记），非事后汇总推算。
>
> **规范形态（P-050 交付 A，由 `dc_validator` M4 分支② 机械校验）**：① 章节号固定 `### 10.1 验收统计`（禁改号、禁标题加括注）；② 数值单元格 = **纯十进制整数**（禁 `**N + M**` / `N 项 + M 发现` / 括注；`**N**` 加粗允许）；③ 表内两条算术必须成立——逐行 `总数 = 通过 + 失败 + 待办`，总计行 = 8 类行**按列求和**。

### 10.2 验收决定

- [ ] **验收通过**：所有 P1 项通过，无阻塞性问题
- [x] **有条件通过**：交付 A 全部验收项通过（**63/64**）；**唯一待办 = 异基座独立 pass**（§8.4）；交付 B **已实施**（v1.3，[IMPLEMENTATION §11](./IMPLEMENTATION.md)），其规格已经 **v1.1 同基座自审**并修订 10 项（DESIGN §9.5）；**P-069 三问续研 Layer-1 最小实施已验收**（v1.5，[IMPLEMENTATION §12](./IMPLEMENTATION.md)）；**P-089 U-10′ 薄壳已验收**（v1.6，[IMPLEMENTATION §13](./IMPLEMENTATION.md)；selftest **71/71**）；**P-092 U-8 门禁链已验收**（v1.7，[IMPLEMENTATION §14](./IMPLEMENTATION.md)；selftest **81/81**；存量零回归 115 session 逐例）
- [ ] **验收失败**

### 10.3 签字

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | | |
| 审查者 | | |

## 11. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|------|--------|------|------|
| **交付 B 规格自审**（同基座，v1.1） | — | — | ✅ 10 项（3 P1 / 3 P2 / 4 P3）已修（DESIGN §9.5） |
| **异基座独立 pass**（RULE-1/RULE-5） | — | — | ✅ Step 8 独立审查已执行（子代理，**同基座降级**），7 项发现全整改（RESEARCH §5.5）；**真异基座**仍待触发 |
| 交付 B（回写流契约变更）交 Review 裁决 | — | — | ✅ **已裁决并实施**（用户裁决「两项都做」）——`superseded` 入 design **一般档**，落 **4 权威位点 + 3 模板**（[IMPLEMENTATION §11](./IMPLEMENTATION.md)）；**R2** = 触发驱动（CHECKLIST 档 / `template` 类不增）/ **R3** = FTA 倾向否决（不设 `superseded_by`） |
| **M7 样本 ㊲**（转述失真族）入账 | — | — | ✅ |
| **M7 样本 ㊳**（增长型载体计数漂移第三度复发）入账 | — | — | ✅ |
| H-CL2（L2 条目级真对账）/ H-CL3（skip 驱动收敛）观察 | — | — | 观察项 |
| **H-FTA / H-RPC1 / H-RPC2** 观察项（工具化触发 / 跨仓对照可迁移性） | — | — | 观察项（[RESEARCH §6](./RESEARCH.md) / [DESIGN §10.2](./DESIGN.md)） |
| **P-069 三问续研 Layer-1 最小实施**（`backflow-audit` + 受控回边受理） | — | — | ✅ 已实施（[IMPLEMENTATION §12](./IMPLEMENTATION.md)；selftest **63/63**） |
| **U-10′ `fork` 注册薄壳**（P-089，乙类执行序 2） | — | — | ✅ 已实施（[IMPLEMENTATION §13](./IMPLEMENTATION.md)；规格 [DESIGN §10.5](./DESIGN.md)；selftest **71/71**；回退点 **R-7**） |
| **U-8 `finalize` 三态强制**（P-092，乙类执行序 5） | — | — | ✅ 已实施（[IMPLEMENTATION §14](./IMPLEMENTATION.md)；规格 [DESIGN §10.6](./DESIGN.md)；selftest **81/81**；回退点 **R-10**） |
| **U-9 CONSOLE 视图侧返工行动档**（「待重写 / 待重入」队列；P-101） | — | — | ✅ 已实施（[project-console DESIGN §5.5](../project-console/DESIGN.md) **D21** + **I-12** + 回退点 **R-8**；实施 [project-console IMPLEMENTATION §8](../project-console/IMPLEMENTATION.md)；selftest **55/55 → 57/57**）——**开闸支路 = 用户裁决**（推翻 P-097「明文不提前开」裁定，同 U-8 / U-10 先例） |
| 更新 PROGRESS.md / CODE_WIKI.md | — | — | ✅ |
