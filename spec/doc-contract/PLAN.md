---
id: doc-contract-refactor
type: design
version: 1.6
status: verified
date: 2026-08-18
depends: [SPEC-PROCESS, ADR-0004, ADR-0005, ADR-0006, ADR-0007, DIS-007, FWK-ASSERTION]
upstream: null
---

# 文档规范改造执行方案（v1.2 定稿）

> **性质**: 本文档规范改造的设计+执行方案。type 词表中 `design` ~~为待定第六类（G2 词表缺口，ADR-0007 定稿时裁决）~~ 已裁决入词表（[ADR-0007](../../adr/ADR-0007-unified-document-contract.md) D4；状态词表二档——一般设计文档 `draft/in-review/verified`，CHECKLIST 实例 `pending/accepting/accepted`，v1.6 §1 DC2 消歧）。
> **审计状态**: 同基座自查 10 项发现（2P1+5P2+3P3，`自查·单视角`）→ 异构复审（DeepSeek V4 Pro，双盲）12 项发现（7P2+5P3，`[已复核·异构]`）→ 本版含全部 P1/P2 修正。
> **执行裁决**: P1=0 / P2=0（已全部融入本版）/ P3=5（见 §8，不阻断）。

---

## 0. 修订历史

| 版本 | 日期 | 变更 | 依据 |
|------|------|------|------|
| v1.0 | 2026-08-16 | 初版方案（27 处修改点） | 本会话 |
| v1.1 | 2026-08-16 | P1×2 修正：DIS-001~006 改"拆分迁移"登记（探针实证）；P0 改名撤销、消歧入 ADR-0007 | 同基座自查 |
| v1.2 | 2026-08-16 | P2×7 修正融入（见 §7 修正记录）；E1 复核修正复审漏计 1 处（DIS-007 L68） | 异构复审 + E1 亲验 |
| v1.3 | 2026-08-16 | 双份并存差异实证（v1.0 vs v1.1 成对漂移）→ 新增 [ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md)（proposed，方案 B 待确认）；doc-contract 让位为 ADR-0007；P3-9 闭环入 ADR-0006，P3-10 部分缓解 | fc+Read 双侧取证 |
| v1.4 | 2026-08-16 | G1 增文件命名规则 `<FEATURE>_<DOCTYPE>.md`；两份调研文档按此重命名（RESEARCH.md → CPP_HUB_GAP_ANALYSIS_RESEARCH.md / ADR0006_POINTER_RESEARCH.md），id 同步 | 用户指令 + 模板 T1/Cpp_Hub 先例 |
| v1.5 | 2026-08-18 | ① G1-G4 全文改名 DC1-DC4（[ADR-0007](../../adr/ADR-0007-unified-document-contract.md) D2，防 Cpp_Hub 基准门禁 G1-G4 跨仓撞车）；② §6 M7 数据降为指针（D1：账本 `docs/M7_EVIDENCE_LOG.md` 为唯一活载体，两轮样本已迁入）；③ §3 配套新增四份实体全部落盘，条目状态改判；④ §8 P3-1/P3-2 按 ADR-0007 D4/D5 裁决闭环 | ADR-0007 accepted（2026-08-17） |
| v1.6 | 2026-08-18 | §1 DC2 状态词表消歧（P-007 复验 P2-1 触发）：① 增 `design` 两行（一般设计文档 `draft/in-review/verified`；CHECKLIST 实例 `pending/accepting/accepted`，判别规则 = id 后缀 `-CHECKLIST`）；② 原"template 实例"行改判 `template` type 行（当前全仓零使用，词表保留）；③ DC2 表 v1.5 前一直缺 design 行（词表仅载于头部注 + ADR-0007 D4）一并修复；E1 全仓实证 14 份 design 文档零违规，纯澄清无迁移 | [DESIGN §6.3](../precommit-dc-validator/DESIGN.md) P2-1 + [ADR-0007 D4](../../adr/ADR-0007-unified-document-contract.md) 澄清追记 |

---

## 1. 全局统一动作（DC1-DC4，原 G1-G4，含 P2-3/P2-4 修正）

> **改名说明（v1.5）**: G1-G4 → DC1-DC4（[ADR-0007](../../adr/ADR-0007-unified-document-contract.md) D2）——G1-G4 与 Cpp_Hub DEVELOPMENT_WORKFLOW §4.1 基准对齐门禁跨仓撞车；DC = Document Contract（本仓库作用域），Cpp_Hub 侧 G 系列不动。映射：G1→DC1（front-matter）/ G2→DC2（状态词表）/ G3→DC3（引用四档）/ G4→DC4（命名空间登记）。

### DC1. 统一 front-matter（七字段，P2-4 修正：六→七）

**文件命名规则（v1.4 新增）**: spec 产出文件名 = `<FEATURE>_<DOCTYPE>.md`（大写下划线，如 `CPP_HUB_GAP_ANALYSIS_RESEARCH.md`），front-matter id = `<feature-kebab>-<doctype>`（如 `cpp-hub-gap-analysis-RESEARCH`）。依据：模板 T1 id 约定 + Cpp_Hub 先例（`SLSQP_EXTENSION_RESEARCH.md`）；文件跨目录/跨仓库引用时保持全局唯一可 grep。存量 `PLAN.md` 为方案文档非四件套，保留原名。

每份文档顶部 YAML 块：

| 字段 | 语义 | 说明 |
|------|------|------|
| `id` | 稳定标识 | 如 SPEC-PROCESS / ADR-0004 / DIS-007 / FWK-ASSERTION |
| `type` | 文档类别 | 词表：`process-spec / adr / discovery / framework / template / design`（design 已裁决入词表，ADR-0007 D4） |
| `version` | 语义版本 | 存量文档首登取当前版（如 SPEC-PROCESS v1.3） |
| `status` | 状态 | 按 type 查 DC2 词表 |
| `date` | 最近修订日期 | |
| `depends` | 依赖文档 id 列表 | 替代散落的"相关文档"链接 |
| `upstream`（P2-4 新增） | **上游权威源声明** | 解决 Cpp_Hub 双份框架并存：本仓库份为权威源时置 `null`；为迁移副本时置源路径。DIS-007 与 FWK-ASSERTION 因源项目有同名文件，**必须**显式声明 |

### DC2. 状态词表（type 主轴；`design` 内按文档类别二档——v1.6 消歧）

| type | 文档类别 | 词表 |
|------|---------|------|
| adr | — | `proposed / accepted / superseded / deferred` |
| discovery | — | `open / resolved / toolized` |
| process-spec / framework | — | `active / deprecated` |
| template | — | `draft / in-review / verified`（当前全仓零使用，词表保留） |
| design | 一般设计文档（id 不以 `-CHECKLIST` 结尾：RESEARCH / DESIGN / IMPLEMENTATION / AUDIT / 方案文档） | `draft / in-review / verified` |
| design | CHECKLIST 实例（id 以 `-CHECKLIST` 结尾，含模板占位符 `<feature-kebab>-CHECKLIST`） | `pending / accepting / accepted` |

> **消歧裁决（v1.6，2026-08-18）**: ① v1.5 及此前该表混轴——"template 实例 / CHECKLIST 实例"两行首列是**文档类别**而非 type 值，且 design 入词表（ADR-0007 D4）后 DC2 表一直缺 design 行（词表仅载于本文件头部注与 ADR）；② 判别规则机械化为 **id 后缀 `-CHECKLIST`**（id 是 front-matter 规范键，判别不依赖文件名，DC 校验器 M2 可直接 grep）；③ E1 全仓实证（2026-08-18）：14 份 `type: design` 文档中 2 份 id 以 `-CHECKLIST` 结尾（status = pending / accepting，均在 CHECKLIST 词表内），其余 12 份 status ∈ {draft, in-review, verified}——**零存量违规**，纯澄清无迁移成本。触发：[P-007 复验 P2-1](../precommit-dc-validator/DESIGN.md)；决策澄清追记：[ADR-0007 D4](../../adr/ADR-0007-unified-document-contract.md)。

> **双语取舍（P3-8 遗留，已裁决）**: ~~三选一悬置~~ 终态 = **英文 token 为准**（ADR-0007 D5）；不建双语映射表。

### DC3. 引用标注四档（P2-3 修正：三→四档）

| 档 | 格式 | 适用 |
|----|------|------|
| 1 仓库内有效 | 原样相对链接 | 如 `../../SPEC_PROCESS.md` |
| 2 源项目可解析 | `[源项目·<path>]` | 探针已实证存在者（如 Cpp_Hub/docs/research/PHASE7C_RESEARCH.md、DIS-001~006） |
| 3 真悬空 | `[外部·未随迁]` | 三处零命中实证者（ADR-0001~0003、META_AUDIT_*.md） |
| 4 **本地工具**（P2-3 新增） | `[本地工具·仓库外]` | `scripts/assertion_audit.py`（本地 scripts/ 惯例，不进库） |

### DC4. 编号命名空间登记（ADR-0007 附录承载）

| 命名空间 | 状态 | 备注 |
|---------|------|------|
| ADR-0001~0003 | 源项目·未随迁 | f:\ 根 + Cpp_Hub + Crucix 三处零命中实证；断档显式登记，不补写 |
| ADR-0004/0005 | 本仓库 | |
| DIS-001~006 | 源项目·拆分迁移留存 | `Cpp_Hub/docs/discoveries/`（001_bh_fdr ~ 006_fp_determinism 全枚举实证） |
| DIS-007 | 本仓库 | 文件名不改，id↔文件名映射入登记表 |
| RULE-1~6 | 本仓库 | S3 赋名 |
| M1-M7 | 外部·元审计里程碑 | 首次出现处加脚注 |
| Phase-7B/7C | 外部·Cpp_Hub | |
| E1-E5 / A/B/C / H#·B#ID | 实例级 | 不入登记表 |

---

## 2. 逐文档修改清单（25 处，v1.1 基数）

### SPEC_PROCESS.md（6 处）

| # | 位置 | 修改点 |
|---|------|--------|
| S1 | L1-7 头部 | → front-matter（id: SPEC-PROCESS, type: process-spec, version: 1.3, status: active）；修订史从 L4 长行改文末标准修订历史表 |
| S2 | **7 行**（P2-1 修正：L28/38/56/73/107/110/295） | `docs/spec/` → `spec/` 全局替换；执行方式：grep 逐行替换后 `docs/spec/` 零命中复核（E1 闭环） |
| S3 | L119-173 规则 1-6 | 冠稳定 ID（RULE-1~RULE-6）；文末新增 ` ```rules ` 登记块：`{id, 来源事故, 失效条件, 拦截记录[]}` |
| S4 | L245 分级 | 正文 P1/P2/P3 不动 |
| S5 | ~~改名~~ | **已撤销**（P1-2）："P0 审计项"保留原名，消歧入 ADR-0007 术语节 |
| S6 | L285 + 正文 M 码首现处 | `docs/adr/` → `adr/`；M1/M2/M6/M7 加命名空间脚注 |

### adr/ADR-0004（3 处）

| # | 位置 | 修改点 |
|---|------|--------|
| A4-1 | L3-13 | + front-matter（id: ADR-0004, type: adr, status: accepted） |
| A4-2 | L11 | 2×META_AUDIT + 1×ADR-0003 → `[外部·未随迁]`（三处零命中实证）；SPEC_PROCESS 有效链接不动 |
| A4-3 | L16-47 | L1/S1-S5 码首现处 + 一行来源说明（外部·元审计改进报告） |

### adr/ADR-0005（2 处，v1.1 减 1）

| # | 位置 | 修改点 |
|---|------|--------|
| A5-1 | L3-13 | + front-matter（id: ADR-0005, status: accepted） |
| A5-2 | L11 | META_AUDIT_IMPROVEMENT_REPORT.md → `[外部·未随迁]` |

### docs/DIS-007 文件（4 处，v1.2 增 1）

| # | 位置 | 修改点 |
|---|------|--------|
| D1 | L1-8 头部 | → front-matter（id: DIS-007, type: discovery, status: toolized） |
| D2 | L3 | RESOLVED → `toolized`（词表化） |
| D3 | L4 模块字段 | → `depends` + `upstream`（源项目有同名 discovery，声明本仓库份身份） |
| D4 | **L68 + L86 两处**（P2-7 修正，含复审漏报的 L68） | `scripts/assertion_audit.py` → `[本地工具·仓库外]` 标注；L85 PHASE7C → `[源项目·Cpp_Hub/docs/research/PHASE7C_RESEARCH.md]` |

### docs/ASSERTION_EVIDENCE_FRAMEWORK.md（4 处，v1.2 增 1）

| # | 位置 | 修改点 |
|---|------|--------|
| F1 | L3-7 头部 | → front-matter（id: FWK-ASSERTION, type: framework, version: 1.0, status: active, **upstream: 声明与 Cpp_Hub 份的权威关系**） |
| F2 | §7 模板内状态词表（v1.2 行号 L262-264） | 状态词表声明为全局词表权威来源（DC2 引用此处） |
| F3 | assertion_audit.py 共 3 处（§4.3 / §7 引言 / §7 审计闭环，v1.2 行号 L137/L207/L258） | → `[本地工具·仓库外]`（DC3 第 4 档） |
| F4 | （新增）upstream 语义落地 | 与 Cpp_Hub/docs/ASSERTION_EVIDENCE_FRAMEWORK.md 的双份关系：本仓库份 = 权威源（ADR-0006 accepted，v1.2 合并已执行），Cpp_Hub 份待加迁移指针对齐 |

### spec/templates/ 4 份（9 处，v1.2 增 1）

| # | 模板 | 位置 | 修改点 |
|---|------|------|--------|
| T1 | RESEARCH | L1-7 | front-matter 模板化（id: `<feature>-RESEARCH` 占位） |
| T2 | RESEARCH | L113（v1.1 已正：非 L123） | 签字行 + `[自查·并发]`/`[已复核]` 标注位（RULE-1 执行接口） |
| T3 | DESIGN | L1-8 | front-matter（depends: [RESEARCH] 形式化） |
| T4 | DESIGN | L29 | `../../adr/` 随 S2 校验（路径统一后自然成立） |
| T5 | IMPL | L1-8 | front-matter（depends: [DESIGN, RESEARCH]） |
| T6 | IMPL | L20-25 | 验证状态列统一词表（P2-5 修正，目标明确）：**`✅已验证 / ⚠️待验证 / ❌不适用`** 三态，替换现存三种混用形态 |
| T7 | CHECKLIST | L1-8 | front-matter（status: pending/accepting/accepted） |
| T8a | CHECKLIST | L117 | §8.2 删 P0 行 → P1/P2/P3 三级 |
| T8b | CHECKLIST | L159（P2-2 修正） | §10.2 "所有 P0/P1 项通过" → "所有 P1 项通过"（随 T8a 消除孤立引用） |

---

## 3. 配套新增（4 份实体文件，v1.5 全部落盘）

0. **adr/ADR-0006-assertion-framework-dual-copy-authority.md** —— 双份并存差异分析 + 权威源决策：~~proposed，方案 B 待用户确认~~ **accepted（v1.5 改判，2026-08-17 方案 B 确认，v1.2 合并已执行）**
1. **adr/ADR-0007-unified-document-contract.md** —— ~~待建~~ **已落盘（v1.5 改判）**: accepted 2026-08-17，承载五项裁决 D1-D5（M7 账本唯一载体 / G1-G4→DC1-DC4 / 命名空间登记补全附录 A / design 入 type 词表 / 状态词英文 token）+ P0 消歧术语节附录 B
2. **spec/templates/ADR_TEMPLATE.md** —— ~~从 ADR-0004/0005 提取骨架~~ **已建成（2026-08-18，含 DC1 front-matter 占位）**
3. **spec/doc-contract/PLAN.md** —— 本方案（已落盘，v1.5）

## 4. 尾随同步（CODE_WIKI.md，P2-6 修正后账目）

| 项 | 内容 |
|----|------|
| 头部计数 | 存量 **9** 个文档 → 改造后 **13** 个（+ADR-0006 分歧 / +ADR-0007 / +ADR_TEMPLATE / +PLAN） |
| §3.3 分级注 | S4/T8 执行后改写（模板 P0 行已删） |
| §6.4 两处 | 路径差异（已统一 `spec/`）、分级差异（已统一 P1/P2/P3）→ 标记已解决 |
| §5.2 悬空表 | D7 行 → `[源项目·可解析]`；ADR/META_AUDIT 行 → "三处零命中实证" |
| 新增 | §2.1 目录树补 spec/doc-contract/ 与 adr/ADR-0007 |

## 5. 执行顺序

```
Step A  DC3/DC4 基础标注（零风险：断链/工具/源项目标注 + 命名空间登记素材）✅ 2026-08-17/18
Step B  S2 路径统一（7 行替换 + grep 零命中复核）✅ 2026-08-17
Step C  DC1/DC2 front-matter 批量（存量 + 4 模板占位）✅ 2026-08-17/18
Step D  S4/S5/T8 分级统一（T8a+T8b 联动）✅ 2026-08-18（T8a/T8b 落地；S4 正文不动；S5 已撤销）
Step E  S3 rules 登记块（RULE-1~6 冠名 + ```rules 登记块 + S6 M 码命名空间说明）✅ 2026-08-18
Step F  新增 3 份（ADR-0007 / ADR_TEMPLATE / PLAN 已在）✅ 2026-08-18（ADR_TEMPLATE 落盘）
Step G  CODE_WIKI 尾随同步 ✅ 2026-08-18（Wiki v1.2：路径/分级/悬空表/差异注记/索引/目录树）
```

**完成定义（P3-12 补）**: A-G 全步执行后复核四项 grep 零命中/命中——`docs/spec/`（零）、`RESOLVED` 于 DIS-007（零）、front-matter `id:`（12 文件全命中）、`P0` 于 CHECKLIST（零）。

> **复核结论（2026-08-18 执行，E1 grep 闭环）**: ① `P0` 于 CHECKLIST_TEMPLATE：**零命中** ✅；② front-matter `id:`：**21 文件命中**（≥12，含 ADR_TEMPLATE 新增）✅；③ `docs/spec/`：3 处命中均为改名元描述（本 PLAN 的 S2 定义行/完成定义行 + CODE_WIKI"已统一"注记），**实际路径引用零命中** ✅；④ `RESOLVED` 于 DIS-007：1 处命中为"原 RESOLVED，DC2 词表化改标"的历史说明，**状态字段实值 toolized** ✅。——描述替换动作的文字必然包含被替换字符串，此为字面 grep 的已知边界，语义甄别后四项全过。

## 6. M7 数据点留痕（v1.5 降为指针，ADR-0007 D1 裁决）

> **指针**: M7 审计轮数据的**唯一活载体** = [docs/M7_EVIDENCE_LOG.md](../../docs/M7_EVIDENCE_LOG.md)（样本登记表 / 形态 II 复发分桶 / 命中率 baseline）。本节原两轮数据（同基座自查 10 项 / 异构复审 12 项）已作为样本 ①② 迁入账本；后续每轮审计样本直接登记账本，本节不再更新——活数据不进决策快照（生命周期错配论证见 ADR-0007 §决策分析 D1）。

<details>
<summary>历史快照（v1.2 原文，仅供追溯，勿在此追加）</summary>

| 审计轮 | 基座 | 发现 | 特征 |
|--------|------|------|------|
| 自查 | GLM 5.3（既写又审） | 10 项（2P1+5P2+3P3） | 笔误级：行号/计数/断链数 |
| 异构复审 | DeepSeek V4 Pro（双盲） | 12 项（7P2+5P3） | 系统性遗漏：涟漪/档位越界/目标缺失 |
| 交叉 | P2 重叠率 1/12；异构复审自身漏计 1 处（DIS-007 L68，E1 亲验发现） | 双向印证：无单一审查视角充分 | |

</details>

## 7. 本版修正记录（P2×7 亲验融入）

| P2 | 修正 | E1 亲验结果 |
|----|------|------------|
| P2-1 | S2 覆盖 6 区域 → **7 行**清单化 + grep 闭环 | ✅ 7 行实测 |
| P2-2 | T8 拆 T8a(L117)+T8b(L159) | ✅ 2 行实测 |
| P2-3 | G3（现 DC3）三档 → 四档（+本地工具） | 定义级 |
| P2-4 | G1（现 DC1）六字段 → 七字段（+upstream 及语义） | 定义级 |
| P2-5 | T6 目标词表明确三态 | 定义级 |
| P2-6 | 尾随同步 8→9 更正为 **9→12**（含 PLAN 自身） | 计数级 |
| P2-7 | D4 扩展 L86 → **L68+L86**（复审漏报 L68，亲验补） | ✅ 3 行实测（L4/L68/L86） |

## 8. 遗留 P3（不阻断，ADR-0007 定稿时处理）

1. ~~G2 双语取舍（全英/全中/映射表）~~ 已裁决（ADR-0007 D5）：英文 token 为准，不建映射表
2. ~~`design` 是否入 type 词表（本 PLAN 自举暴露的缺口）~~ 已裁决（ADR-0007 D4）：入，状态词表 draft/in-review/verified
3. ~~upstream 权威源方向~~ 已解决：[ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) accepted（方案 B），v1.2 合并已执行
4. Crucix 消费方的变更通知机制（职责边界声明）
5. 规则 re-qualification（90 天重审）——学习回路升级独立议题，不在本方案范围
