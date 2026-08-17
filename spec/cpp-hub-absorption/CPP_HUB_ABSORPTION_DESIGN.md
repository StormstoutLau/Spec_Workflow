---
id: cpp-hub-absorption-DESIGN
type: design
version: 1.0
status: draft
date: 2026-08-16
depends: [CPP_HUB_GAP_ANALYSIS_RESEARCH, CPP_HUB_GAP_ANALYSIS_AUDIT, FWK-ASSERTION, SPEC_PROCESS, ADR-0006, doc-contract-refactor]
upstream: null
---

# Spec_Workflow 吸收复用 Cpp_Hub 规范设计文档 v1.1 (2026-08-17)

> **Feature**: cpp-hub-absorption（PROGRESS P-002 的设计承载）
> **基于调研**: [CPP_HUB_GAP_ANALYSIS_RESEARCH.md](../cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md) v1.0（已审计，16A+4B+2C+3H；审计报告 2 项 P2 已修正）
> **Spec 步骤**: Step 3-4
> **审计状态**: Step 4 Review 已执行（2026-08-17 独立 pass：2 P2 + 6 P3；P2 两项已于 v1.1 修正清零）——详见 §10

---

## 1. 设计目标

将差距分析实证的 11 项未吸收机制中**属于方法论层**的部分，按分层策略吸收进 Spec_Workflow，使"审查宪法"分支补齐"调研流水线"分支已验证的能力，同时不吞并项目特定机制。一句话：**机制收进来，实例留在源头；每项吸收可溯源、可回滚、有验收。**

## 2. 设计依据

### 2.1 调研结论 → 设计决策

| 调研发现（RESEARCH §3/§4，E1 锚定） | 设计决策 | 引用 |
|---|---|---|
| B1: 11 项机制未吸收（下界，4/63 覆盖） | 分层吸收：Tier1 三项立即 / Tier2 三项结构（各立 ADR）/ Tier3 六项明确不收——11 项逐项落位映射见 §3.1（v1.1：#7 补录 Tier3，消除计数闭合假象） | RESEARCH §3.1 |
| B2: STEP_GAP 分型缺失（权威源落后消费项目一项） | D1: 框架升 v1.3 落分型（pilot 已验证必要：B1 轻微跳步被机械闭合的实例） | RESEARCH §4-B2 |
| pilot 量化数据（双盲 5/5 TRUE、R2 拦截 1/4） | D2: M7 样本登记（N=3） | RESEARCH §4 |
| Phase 5 四波 review 修正 14 处 | D3: 命中率 baseline 登记 | RESEARCH §3.1-9 |
| R 门禁串联语义（R 清零→spec 冻结→实施→G 清零→合并） | D4: SPEC_PROCESS Step 2 Review 升格为门禁语义 | RESEARCH §3.1-1/2 |
| Discoveries 三态日志机制 + 三集成点 | D5: 引入 docs/discoveries/（学习回路"事故→规则"的载体） | RESEARCH §3.1-3/4/5 |
| 三文档对齐审计 59 项双向链路 | D6: Step 8 增强为双向引用检查 | RESEARCH §3.1-8 |
| 双分支定性（审查宪法 vs 调研流水线） | Tier3 拒收边界的原则依据 | RESEARCH §4-C |
| 形态 II 三实例复发（审计报告 §4） | D2 附带：M7 单列形态 II 复发计数 | AUDIT §4 |

### 2.2 相关 ADR

| ADR | 关系 |
|-----|------|
| [ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) (accepted) | 权威源已落位本仓库——本设计是决策 4"回流通道"的**首次批量使用** |
| [ADR-0007](../../adr/ADR-0007-unified-document-contract.md)（accepted 2026-08-17） | D1 裁定 M7_EVIDENCE_LOG.md 为 M7 数据唯一活载体——本设计 D2/D3 是该裁决的首次消费（P2-2 由此闭环）；另承载 G1-G4→DC 消歧与登记补全（P-003 范围） |
| [ADR-0008](../../adr/ADR-0008-spec-process-review-gate-and-bidirectional-check.md)（accepted 2026-08-17）/ ADR-0009（Tier2 实施期产出，编号预留） | D4+D6（scope 经独立复核修正为双决策）/ D5 的决策记录 |

### 2.3 职责边界（ADR-0002 语义）

**职责内**: 方法论机制的跨仓库吸收（门禁语义、发现日志、对齐检查、词表演进、M7 数据资产）。

**职责外**（声明"不回答"）:
- Cpp_Hub 的 G1-G4 数值基准门禁、加权审计实例、波次交付追踪——项目工程治理，归 Cpp_Hub
- Cpp_Hub ADR-001~019 的具体架构决策内容——项目架构史，仅登记编号空间（ADR-0007 范围）
- assertion_audit.py 的功能演进——本地工具，不入本仓库

**能力边界**（声明"回答不了"）:
- 跨仓库自动同步——回流是人工纪律（ADR-0006 决策 4 已声明），本设计不建技术强制
- 11 项之外的存在性完备——调研覆盖率 4/63，"还有多少未吸收机制"本轮无法回答（H2）

## 3. 架构设计：三层吸收策略

### 3.1 整体架构

```
Tier 1 立即吸收（零/低结构成本，无新 ADR）
  D1 框架 v1.3: STEP_GAP 分型        → docs/ASSERTION_EVIDENCE_FRAMEWORK.md
  D2 M7 样本登记（N=3 + 形态II计数）  → docs/M7_EVIDENCE_LOG.md（新建）
  D3 命中率 baseline 登记             → docs/M7_EVIDENCE_LOG.md（同文件）
Tier 2 结构吸收（各立 ADR，改宪法/建机制）
  D4 Step 2 门禁语义（R 清零进 Step 3）→ SPEC_PROCESS v1.4 + ADR-0008
  D5 Discoveries 发现日志机制         → docs/discoveries/ + ADR-0009
  D6 Step 8 双向链路检查              → SPEC_PROCESS v1.4（随 D4 同版）
Tier 3 明确不吸收（拒收清单，防未来重提）
  G 数值门禁 / 加权实例 / 波次追踪 / ADR 不可变规则 / 决策-双源映射表 / 条件通过-整改-签名（#7）
```

**Tier3 拒收理由（不变式 4 的落地记录，v1.1 补全）**:

| 拒收项 | 来源 | 理由 |
|--------|------|------|
| G 数值门禁 | #2 的 G 侧 | Cpp_Hub 基准对齐工程治理（1e-10 容差/三源交叉），本仓无对应活动 |
| 加权审计实例 | #6 | 项目管理产物；本仓 CHECKLIST 已有逐项溯源约束（RESEARCH §3.2） |
| 波次追踪 | 清单外 | 交付管理，单人仓库无波次概念 |
| ADR 不可变规则 | #10 | 与本仓 ADR 版本化修订实践冲突（ADR-0006 修订历史先例）；MADR 不可变语义适合多人治理 |
| 决策-双源映射表 | #11 | pilot 项目产物；其机制语义已由 D4 门禁 (b)(c) 条覆盖 |
| 条件通过-整改-签名 | **#7（v1.1 补录，P2-1）** | 机制语义已内生——本仓审计报告裁决节即"有条件通过 + 修正要求 + 审计者声明"结构（实证: [GAP_ANALYSIS_AUDIT §5](../cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_AUDIT.md)）；签名/整改追踪制度化属多人项目治理，单人仓库成本不抵收益 |

**11 项机制落位映射（v1.1 新增，消除计数闭合假象）**:

| 机制 # | 落位 |
|--------|------|
| #1 R 门禁 / #2 R+G 串联 | D4（#2 的 G 侧拒收，见上表） |
| #3-#5 Discoveries 三机制 | D5 |
| #6 / #7 / #10 / #11 | Tier3（四项） |
| #8 三文档对齐 | D6 |
| #9 Phase 5 命中率 | D2/D3 |
| 校验 | 2+3+4+1+1 = **11/11 全落位**；D1 源自 B2 分型缺口（非 11 项清单项）；G 门禁/波次追踪为清单外拒收项 |

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| M1 框架词表演进 (D1) | STEP_GAP 两态化 + 状态词表增补 | pilot §5.1-3 提案 | 框架 v1.3（修订历史 +1 行） | ADR-0006 |
| M2 M7 证据账本 (D2/D3) | 对比臂样本 + 命中率 baseline + 形态 II 分桶计数的登记载体 | 本仓两轮审计 + pilot + Phase 5 数据 | docs/M7_EVIDENCE_LOG.md | AUDIT §4 |
| M3 门禁语义 (D4) | Step 2 Review 从 checklist 升格为阻断门禁 | Cpp_Hub R1-R4 语义 | SPEC_PROCESS v1.4 + ADR-0008 | D1（词表先行） |
| M4 发现日志 (D5) | 三态发现索引 + 与 10 步流程的集成点 | Cpp_Hub discoveries 机制 | docs/discoveries/ + ADR-0009 + DIS-007 迁入登记 | M3 |
| M5 对齐检查 (D6) | Step 8 增加双向引用完整性检查项 | Cpp_Hub F1-F8 模式 | SPEC_PROCESS Step 8 检查清单 +2 项 | M3 |

### 3.3 数据流

```
Cpp_Hub 现场产出（pilot/审计实例/发现）
  → [人工回流纪律, ADR-0006 决策4]
  → Spec_Workflow 吸收层（本设计 Tier1/2）
  → 权威源演进（框架 v1.3 / SPEC_PROCESS v1.4 / 新机制文件）
  → 消费方（Cpp_Hub / Crucix）经指针引用新版
```

### 3.4 控制流（执行顺序）

Tier1（D1→D2→D3，一次提交）→ Tier2 按 D4→D5→D6（D4/D6 同版 SPEC_PROCESS；D5 独立）。Tier3 无执行动作，仅本节拒收记录。

## 4. 接口定义（文档层契约）

### 4.1 D1: 框架 §4.4-3 与状态词表修改

```text
§4.4-3 改为:
  STEP_GAP 不是通过，分两态:
  - STEP_GAP_CLOSED (gap-closed): 差额步已被一手证据机械闭合 → 无需仲裁，标注闭合证据
  - STEP_GAP_OPEN   (gap-open):   差额步未闭合 → 进仲裁
§7 状态词表行改为:
  STEP_GAP_CLOSED 疑跳步已闭合 / STEP_GAP_OPEN 疑跳步待仲裁
  （原 STEP_GAP 单词废除；兼容: 历史报告中的 STEP_GAP 读作 STEP_GAP_OPEN）
```

来源: pilot §5.1-3（"建议框架…细分为 gap-closed 与 gap-open 两态"）；实例依据: pilot B1 轻微跳步被 auditor 全库穷举机械闭合。

### 4.2 D2/D3: M7_EVIDENCE_LOG.md 骨架

> **载体权威性（v1.1，P2-2 修正）**: [ADR-0007](../../adr/ADR-0007-unified-document-contract.md) D1（accepted 2026-08-17）已裁定本文件为 M7 数据**唯一活载体**——PLAN §6 随 P-003 降为指针，本设计不再与 PLAN §6 构成双载体冲突。

```markdown
# M7 证据账本 (对比臂数据累积)
## 样本登记表
| # | 日期 | 载体 | 审查配置 | 发现 | 形态II复发 | 来源 |
| 1 | 2026-08-16 | doc-contract 方案 | 同基座自查 GLM-5.3 | 10 (2P1+5P2+3P3) | 0 | PLAN §6 |
| 2 | 2026-08-16 | doc-contract 方案 | 异构双盲 DeepSeek V4 | 12 (7P2+5P3) | 0 | PLAN §6 |
| 3 | 2026-08-17 | ADR-019 决策集 | 探针+双盲 (Cpp_Hub pilot) | R2 拦截 1/4; 双盲 5/5 | 1 (转述引文) | pilot §5.1 |
| 4 | 2026-08-16 | GAP_ANALYSIS 报告 | 同基座审计 (本仓) | 4 (2P2+2P3) | 2 (计数/行号) | AUDIT §3 |
## 形态 II 复发分桶 (AUDIT §4.3)
[载体 × 字段类型 计数表，随样本追加]
## 命中率 baseline
| 来源 | review 修正数 | 锚点 |
| Cpp_Hub Phase 5 四波 | 14 处 (2+1+6+5) | AUDIT_CHECKLIST L462-465 |
```

### 4.3 D4: SPEC_PROCESS Step 2 门禁语义

```text
Step 2 Review 章末新增:
  【门禁】Step 2 Review 全项通过 + 断言审计结论满足 R 语义
  （阻断性断言: FALSIFIED 已改写 / CONFLICT·STEP_GAP_OPEN 已仲裁 / 双源满足；
    假设区条目已转 A/B 或以 [待定] 显式携带）——满足前禁止进入 Step 3。
```

### 4.4 D5: discoveries 机制（最小版）

```
docs/discoveries/
├── README.md          # 三态索引: RESOLVED / OPEN / KNOWN + 登记格式
└── DIS-007 迁入登记    # 现docs/007_*.md 不移动，README 登记映射（沿用 ADR-0006 的 id↔文件名映射惯例）
集成点（写入 SPEC_PROCESS 对应步）:
  Step 2 调研异常 → 记录发现而非"修 bug"
  Step 10 ADD 审计发现系统性模式 → 记录发现
  每条发现字段: {id, 状态, 一句话, 证据锚点, 潜在论文?}
```

### 4.5 D6: Step 8 检查清单 +2 项

```text
- [ ] 双向引用完整: 四文档 + 相关 ADR 互引均成立（正向: 文档引用的 ADR 存在;
      反向: 相关 ADR 的"相关文档"含本 feature 链接）——Cpp_Hub F1-F8 模式
- [ ] 断言延续: RESEARCH 的 B 类断言状态在 DESIGN/IMPLEMENTATION 引用处已按
      最新词表标注（含 STEP_GAP_CLOSED/OPEN）
```

## 5. 替代方案

### 5.1 方案 A: 全量吸收 11 项（否决）

- 描述: 机制与实例一并收编，Cpp_Hub 流程文档整体迁入
- 优点: 单一权威源覆盖全部；无"两套"心智负担
- 缺点: 吞并项目特定机制（数值 G 门禁/加权实例/波次追踪）违反职责边界；仓库从方法论宪法膨胀为项目档案；与"加法→减法"自我干预冲突
- 否决理由: 双分支定性（RESEARCH §4-C）表明两者是**互补**而非包含关系；合并消灭互补性

### 5.2 方案 B: 零吸收，各自演化（否决）

- 描述: 维持现状，Cpp_Hub 机制留在源头
- 优点: 零成本
- 缺点: B2 已实证分叉（STEP_GAP）；学习回路"事故→规则"数据触发腿持续开环（前轮诊断的 5 项缺失中 4 项与此相关）
- 否决理由: 权威源名存实亡——消费项目验证过的改进进不来，违背 ADR-0006 立权威源的初衷

### 5.3 方案 C: 分层选择性吸收（选择）

- 描述: Tier1/2/3 如 §3
- 优点: 每项吸收有独立验收与溯源；拒收清单防未来重复提案；与 doc-contract（ADR-0007）并行不冲突
- 缺点: 两仓库机制分布仍有心智映射成本（需靠 CODE_WIKI 更新缓解）

## 6. 数据结构

无代码数据结构。文档契约复用: front-matter G1 七字段 / 命名规则 `<FEATURE>_<DOCTYPE>.md` / 引用四档标注（G3）。M2 的 M7_EVIDENCE_LOG 为表格式登记（§4.2 骨架；载体权威性经 ADR-0007 D1 裁定），暂不机读化——待 M7 成文时若需统计再升 ```hits 块（学习回路升级独立议题，不并入本设计）。

## 7. 边界情形处置

| 情形 | 处置 |
|------|------|
| 历史报告含旧词 STEP_GAP | 兼容规则: 读作 STEP_GAP_OPEN（§4.1），不回改历史文档 |
| Cpp_Hub 侧 pilot 后续版本更新 | 回流走 ADR-0006 决策 4 通道，本设计不追版本（吸收的是机制不是快照） |
| D5 与学习回路升级（re-qualification）的关系 | D5 只建载体；命中率量化/90 天重审属学习回路独立议题（PLAN §8-5），防 scope 膨胀 |
| Tier2 ADR 编号冲突 | ADR-0008/0009 按 docs/adr/README.md 登记；若期间被占用则顺延并在 README 登记 |

## 8. 不变式（ADD 审计依据）

1. **单向权威不变式**: 吸收后的机制文本以本仓库为唯一权威；Cpp_Hub 侧对应物降为历史副本（P-001 指针落地后生效）
2. **溯源不变式**: 每项 Tier1/2 修改的修订历史行必须含来源锚点（源文件 + 行号/章节）
3. **词表封闭不变式**: 状态词表变更只能通过框架版本升级（v1.3+）进行，报告内不得自造（沿用"固定，不得自造"）
4. **拒收显式不变式**: Tier3 六项在本文档留拒收记录（v1.1: 含补录的 #7，理由表见 §3.1），未来重提须先推翻本设计（supersede 或修订）
5. **分型完备不变式**: STEP_GAP 判定后必须落两态之一，禁止悬空"STEP_GAP"旧态（历史兼容除外）

## 9. 对实施的输入（IMPLEMENTATION 输入）

### 9.1 关键工程约束

- D1 修改必须同步三处: §4.4-3 / §7 词表 / 修订历史——漏一处即制造内部不一致（S4 教训）
- D4/D6 同升 SPEC_PROCESS v1.4（一次版本变更承载两项，避免同日双版）
- M2 文件名遵守 G1 v1.4 命名规则的例外说明（docs/ 下非 feature 四件套文件，用大写下划线但无 `<FEATURE>_` 前缀约束——按 `M7_EVIDENCE_LOG.md` 直名，与 `PROGRESS.md` 同类）

### 9.2 风险与缓解

| 风险 | 缓解 |
|------|------|
| D4 门禁过重，单人流程被弃用（skip-and-forget 宪法版） | 门禁项保持 4 条以内；与 R4 语义对齐而非复制全文 |
| D5 discoveries 沦为僵尸目录（登记后无人维护） | 集成点绑定既有步骤（Step 2/10），不新增独立流程动作；README 登记格式含"潜在论文?"字段维持动机 |
| Tier2 两份 ADR + SPEC_PROCESS 升版同日交织 | 提交切分: D1-D3 一提交 / ADR-0008+SPEC_PROCESS 一提交 / ADR-0009+discoveries 一提交 |

## 10. 幻觉排除审查（Step 4 Review）

> 本节与正文同次生成，按 RULE-1 标注 `自查·并发`，待独立 pass 复核后升级。

- [ ] 设计决策可追溯到 RESEARCH（§2.1 表逐行有引用） `自查·并发`
- [ ] 无未经验证的假设——B1 计数为下界已显式声明；Tier3 拒收理由均来自已验证发现 `自查·并发`
- [ ] 无论证驱动的归因扭曲——未使用 Cpp_Hub 案例裁剪论证 `自查·并发`
- [ ] 替代方案 ≥2 已否决（§5） `自查·并发`
- [ ] 职责边界双声明（§2.3） `自查·并发`

## 11. 验收（CHECKLIST 输入要点）

| 项 | 通过条件 |
|----|---------|
| D1 | 框架 v1.3: grep "STEP_GAP_CLOSED" 三处命中（§4.4-3/词表/修订历史）；旧词单处不剩（兼容注释除外） |
| D2/D3 | M7_EVIDENCE_LOG 存在且样本表 4 行、形态 II 分桶含 3 实例、baseline 含 Phase 5 的 14 处锚点 |
| D4 | SPEC_PROCESS v1.4 含【门禁】块；ADR-0008 状态 accepted |
| D5 | docs/discoveries/README 存在；DIS-007 映射登记；SPEC_PROCESS 集成点 2 处 |
| D6 | Step 8 清单含双向引用 + 断言延续两项 |
| Tier3 | 本文档 §3.1 拒收清单 6 项（含 v1.1 补录 #7 及理由表；隐式验收: 无对应实施动作） |

---

**Review 签字**: 独立复核 pass——GLM-5.3（2026-08-17，RULE-4 单视角警示登记）｜用户确认: Scott _________ 日期: _________

## 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-08-16 | 初版（Step 3 产出，§10 `自查·并发`） |
| v1.1 | 2026-08-17 | Step 4 Review P2 修正清零：P2-1 机制 #7 补录 Tier3（五→六项）+ 新增拒收理由表与 11 项落位映射表（消除计数闭合假象）；P2-2 M7 载体指向 ADR-0007 D1 裁定（M7_EVIDENCE_LOG.md 唯一活载体）；§2.2 ADR-0007/0008 行同步 accepted 状态（ADR-0008 登记的联动项）；§10 五项升级 `[已复核]`。P3 六项不阻断，登记于复审记录（N=3 表述 / DeepSeek 型号 / D5 集成点裁剪理由 / 方案 B 缺点锚点 / 创建日期 / PROGRESS 存量计数） |
