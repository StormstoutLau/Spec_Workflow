---
id: cpp-hub-gap-analysis-RESEARCH
type: design
version: 1.0
status: in-review
date: 2026-08-16
depends: [SPEC_PROCESS, FWK-ASSERTION, DIS-007, ADR-0006, doc-contract-refactor]
upstream: null
---

# Cpp_Hub spec 规范体系差距分析调研报告 v1.0 (2026-08-16)

> **任务来源**: 用户提问"当前框架是否已完全吸收 Cpp_Hub 规范且更先进"
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离
> **审计状态**: 已审计（[CPP_HUB_GAP_ANALYSIS_AUDIT.md](./CPP_HUB_GAP_ANALYSIS_AUDIT.md) v1.0，2026-08-16）——2 项 P2 已修正（§0 计数 + A12 行号），核心结论经独立 grep 重验成立

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 16 | §2 载体 1 + §3.1 机制证据 11 + §4 pilot 引文 4；每条附本地路径 + 行号 + 可 grep 引文 |
| B 推断类 | 4 | B1-B4，登记于附录 B |
| C 判断类 | 2 | §4 两条显式标注；§5 回流建议 6 条同为 C 类（未行内标注，审计后补登记于此） |
| 假设区 | 3 | H1-H3，未取证声明 |

> **审计修正记录（P2-1）**: 初版误计 A=12/C=7——漏计 §3.1 的 11 条机制证据行与 §4 的 4 条 pilot 引文（A 类），且 §5 六条 C 类判断未行内标注。修正依据：审计端 `grep -c '【A】'`=16 / `grep -c '【C】'`=2 机械重数（E1）。形态 II 复发实例，详见审计报告 §4。

**扫描范围声明（E4 语义）**: Cpp_Hub `docs/**/*.md` 枚举共 63 个文件，本轮**全读 4 个核心流程文件**（DEVELOPMENT_WORKFLOW / ADR_INDEX / AUDIT_CHECKLIST / ADR019_REVIEW_PILOT），其余 59 个（含 DEVELOPMENT_LOG 1500+ 行、4 个 ADR 完整文档、17 个 RESEARCH、15 个 phase 文档）**未读**。B1 的"11 项未吸收"是**下界**，非完备清单。

---

## 1. 调研问题与方法

**核心问题**:
1. Cpp_Hub 的 spec 相关规范（含审计规范）体系全貌是什么？
2. Spec_Workflow（含 v1.2 权威源）是否已完全吸收？
3. 双方相对领先性如何定性？

**工具**: Glob（枚举全集）+ Read（清洁取证，4 核心文件）+ 本会话前期对 Spec_Workflow 9 份的全读 + 双向对照。

## 2. Cpp_Hub 规范体系全景（枚举）

【A】Cpp_Hub 拥有独立演化的完整流程体系，核心载体四件：
(源: f:\Cpp_Hub\docs\DEVELOPMENT_WORKFLOW.md L3-4; 引文: "> **版本**: 1.1 / > **日期**: 2026-08-16 (v1.1: 新增阶段 0 调研证据审计 + R1-R4 门禁, Phase 7C 审计教训制度化; v1.0 2026-07-29)")

| 板块 | 文件 | 规模 |
|------|------|------|
| 开发工作流宪法 | DEVELOPMENT_WORKFLOW.md v1.1 | 362 行，阶段 0-3 + 双门禁 + 发现日志机制 |
| ADR 体系 | ADR_INDEX.md + 4 份完整 ADR | ADR-001~019（MADR 格式） |
| 审计清单 | AUDIT_CHECKLIST.md | Phase 1-7A 加权实例，三平台实测数据 |
| 调研审计 | ADR019_REVIEW_PILOT.md v1.1 | R 门禁首轮 pilot，量化结果 |

## 3. 逐机制吸收状态矩阵

### 3.1 Cpp_Hub 独有——Spec_Workflow 无对应物（11 项，B1）

| # | 机制 | A 类证据锚点 |
|---|------|-------------|
| 1 | R1-R4 调研证据门禁（阻断语义） | 【A】(源: DEVELOPMENT_WORKFLOW §4.2 L239; 引文: "\| R4 \| 阻断性清零 \| spec 将引用的阻断性断言：FALSIFIED 已改写、CONFLICT/STEP_GAP 已仲裁、双源满足") |
| 2 | R+G 双门禁串联流水线 | 【A】(源: 同上 L241; 引文: "两门禁串联：**R 清零 → spec 冻结 → 实施 → G 清零 → 合并**") |
| 3 | Discoveries 日志机制（三态索引） | 【A】(源: 同上 附录 L334-339; 引文: "\| **RESOLVED** \| 已有反例 + 理论解释, 可能有论文 \| … \| **OPEN** \| 已识别裂缝但未解决 \| … \| **KNOWN** \| 文献有方案但开源库未实现") |
| 4 | 发现-工作流三集成点 | 【A】(源: 同上 L342-345; 引文: "若遇到数值不稳定或边界 case 异常, 不是'修 bug', 而是**记录发现**") |
| 5 | 发现统计与论文转化跟踪 | 【A】(源: 同上 L356-360; 引文: "总发现数: 7 / RESOLVED: 2 … / 潜在论文: 6") |
| 6 | 加权审计实例体系（7 个 Phase 填好实例） | 【A】(源: AUDIT_CHECKLIST L308-313; 引文: "\| Phase 3 \| 2026-07-31 \| Scott (独立审计) \| 95% (A30✅ + B25✅…) \| ✅ 条件通过") |
| 7 | 条件通过 + 整改项追踪 + 签名制度 | 【A】(源: 同上 L315-319; 引文: "**条件通过整改项** (如有): 1. **E1/E2 性能基准** (Phase 4)…") |
| 8 | 三文档对齐审计（59 项双向链路） | 【A】(源: 同上 L654-664; 引文: "ADR-015 正文 (Accepted) ←→ 调研报告 v1.2 ←→ 执行规格 v2.0 三文档在…六个维度 100% 对齐") |
| 9 | Phase 5 命中率数据（review 修正计数） | 【A】(源: 同上 L462-465; 引文: "第一波 v1.4.0 … ✅ 正式通过 (严格 review 修正 2 处幻觉…)"——四波合计 2+1+6+5=14 处) |
| 10 | ADR 不可变规则（MADR） | 【A】(源: ADR_INDEX L5; 引文: "所有 ADR 必须在实施前创建，Accepted 后不可变更，仅能 Superseded") |
| 11 | 决策→阻断性断言→双源状态映射表 | 【A】(源: ADR019_REVIEW_PILOT §2 L27-43; 引文: "\| 决策组 \| 决策 # \| 阻断性断言 \| 双源状态 \|") |

### 3.2 Spec_Workflow 独有——Cpp_Hub 无对应物（9 项）

RULE-1~6 审查独立性规则（时序独立/统计溯源/单视角声明）、异构基座 + 单向权限（RULE-5）、ADD 四阶段审计 + Phase 0 Spec 质量门 + Iron Law、E1-E5 取证矩阵 + 诚实结果列 + 最高等级绑定（ADR-0005）、隔离四要素（quarantine）、派生需求登记（DO-178C 语义）、CHECKLIST 验收统计的逐项溯源约束、文档契约改造（进行中）、学习回路元诊断。【C】定性依据：Cpp_Hub docs 全目录脚本 grep "取证矩阵|Iron Law|隔离四要素|异构基座|派生需求|统计溯源|时序独立" **零命中**（审计轮 E1 重跑升级，2026-08-16；初版为 Read 目视核对 E4，见审计报告 P3-2）。

### 3.3 双方共有（同源继承）

断言 A/B/C 分级 + 不对称配置、机械反证探针五类、双盲重推导 + STEP_GAP 检测、§7 报告模板 + 机读登记块、"报告即审计输入"闭环、状态词表。

## 4. 关键发现

【B1】**未完全吸收**（见附录 B）——11 项下界。
【B2】**权威源 v1.2 落后于消费项目本地演进一项**：pilot 提出的 STEP_GAP 分型不在 v1.2 内（见附录 B）。
【A】pilot 全量量化结果：
(源: ADR019_REVIEW_PILOT §4 L62-76; 引文: "B1 … PROBE_SURVIVED … 2 处直接证据: vecm.py L733-734" / "Phase 2 双盲重推导 (独立 auditor agent…全部一手取证)" / §4 表 "B1-B5 VERDICT 全 TRUE")
【A】R2 门禁首轮拦截实录：
(源: 同上 §3 L52; 引文: "❌ **引文失准** (形态 II 弱记忆填充): 赋值关系成立 (断言结论不受影响), 但登记引文系转述非原文 → 附录 B 已同步修正")
【A】双盲增强效应（强于原链）：
(源: 同上 §4 L74; 引文: "**比原链更强**: `method` 参数在 fit 函数体 (L653-694) 中完全未被引用…→ '仅 ols'从文档与实现双重成立")
【A】pilot 版本日期标注：
(源: 同上 L3; 引文: "> **版本**: v1.1 (2026-08-17: 完成 Phase 1 探针 + Phase 2 双盲 + R1-R4 判定全通过…)")
【B3】**G1-G4 编号双义撞车**（见附录 B）。
【B4】**双 ADR 独立系列**（见附录 B）。
【C】M7 对比臂数据已有第一份现场样本：pilot §5.1 本身就是"框架自验证"的量化产出（双盲 5/5、R2 拦截 1/4、STEP_GAP 分型需求），可直接录入 PLAN.md §6 作 N=3。
【C】两分支关系定性：**同源分化、互补领先**——Spec_Workflow 是"审查宪法"（怎么审 spec 与实现），Cpp_Hub 是"调研流水线"（怎么把证据门禁化喂进决策）。"谁更先进"是错误问题，"如何合流"才是。

## 5. 回流建议（C 类，优先级序）

1. **STEP_GAP 分型** → 框架 v1.3：pilot 原文建议"框架 v1.2 将 STEP_GAP 细分为 gap-closed (无需仲裁) 与 gap-open (需仲裁) 两态"——因 v1.2 已被占用为回吸收版本号，落点改 v1.3。一行级改动，首轮 pilot 已验证必要（B1 轻微跳步被机械闭合的实例）。
2. **Pilot 量化数据 + Phase 5 命中率 14 处** → PLAN.md §6 M7 样本登记。零结构成本。
3. **R 门禁模式泛化** → SPEC_PROCESS Step 2 从 checklist 升格为门禁语义（R 清零才能进 Step 3）。结构性，建议立 ADR。
4. **Discoveries 日志机制** → Spec_Workflow 引入 docs/discoveries/ 三态索引。结构性（学习回路"事故→规则"的载体），建议立 ADR。
5. **三文档对齐审计** → Step 8 增强为双向链路检查（F1-F8 模式）。
6. **命名空间消歧** → ADR-0007（doc-contract）处理 G1-G4 撞车 + 双 ADR 系列登记补全。

## 6. 局限性与诚实声明

1. **覆盖率 4/63**：B1 为下界；DEVELOPMENT_LOG.md（1500+ 行）与 ADR-016~019 完整文档未读（H2/H3）。
2. §3.2 的"零命中"为目视核对（E4），复核时须脚本 grep 重跑升级为 E1。
3. 本报告自身未经独立审计（规则 4 单视角警示适用）；附录 B 登记块已备好，可直接 `assertion_audit.py audit --input` 本报告。
4. pilot 引用的 statsmodels 事实（如 vecm.py L733-734）系Cpp_Hub 侧已验证断言，本报告转引其报告为源，未独立重验。

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "Spec_Workflow (含 v1.2 权威源) 未完全吸收 Cpp_Hub 规范体系, 未吸收机制 ≥11 项 (下界)",
    "op": "counting",
    "claimed_chain": [
      {"step": 1, "text": "Glob 枚举 Cpp_Hub docs/**/*.md = 63 文件, 核心流程载体四件", "source": "Glob 枚举"},
      {"step": 2, "text": "Read 全读四件, 提取机制清单 (R 门禁/串联流水线/Discoveries/加权实例/对齐审计/命中率数据/MADR 不可变/双源映射表等)", "source": "四核心文件 Read"},
      {"step": 3, "text": "与 Spec_Workflow 9 份存量内容 (本会话全读) 逐项对照, 11 项无对应物", "source": "双向对照"}
    ],
    "sources": [
      {"label": "DEVELOPMENT_WORKFLOW.md", "path": "f:/Cpp_Hub/docs/DEVELOPMENT_WORKFLOW.md", "url": null, "quote": "v1.1: 新增阶段 0 调研证据审计 + R1-R4 门禁"},
      {"label": "AUDIT_CHECKLIST.md", "path": "f:/Cpp_Hub/docs/audit/AUDIT_CHECKLIST.md", "url": null, "quote": "Phase 3 … 95% … ✅ 条件通过"},
      {"label": "Spec_Workflow 全量", "path": "f:/Spec_Workflow", "url": null, "quote": "9 份存量: SPEC_PROCESS/ADR-0004~0006/007/框架/4 模板"}
    ],
    "probe": {"type": "counting", "files": ["f:/Cpp_Hub/docs", "f:/Spec_Workflow"], "params": {"definition_pattern": "机制定义点枚举", "expected_count": ">=11 (下界, 4/63 覆盖)"}}
  },
  {
    "id": "B2",
    "conclusion": "权威源框架 v1.2 缺失 pilot 已验证必要的 STEP_GAP 分型 (gap-closed/gap-open), 回流通道首次真实使用场景已出现",
    "op": "transitivity",
    "claimed_chain": [
      {"step": 1, "text": "v1.2 全文为本会话逐行 Write, §4.4-3 与 pilot 相关节无分型表述", "source": "Spec_Workflow 框架 v1.2 全文"},
      {"step": 2, "text": "pilot §5.1-3 明确提议两态分型并给出实例依据 (B1 轻微跳步被机械闭合)", "source": "ADR019_REVIEW_PILOT §5.1"},
      {"step": 3, "text": "pilot 头部日期标注 2026-08-17, 晚于 v1.2 合并执行 → 提案不可能已含于 v1.2", "source": "ADR019_REVIEW_PILOT L3"}
    ],
    "sources": [
      {"label": "pilot §5.1", "path": "f:/Cpp_Hub/docs/research/ADR019_REVIEW_PILOT.md", "url": null, "quote": "建议框架 v1.2 将 STEP_GAP 细分为 'gap-closed' (无需仲裁) 与 'gap-open' (需仲裁) 两态"},
      {"label": "框架 v1.2", "path": "f:/Spec_Workflow/docs/ASSERTION_EVIDENCE_FRAMEWORK.md", "url": null, "quote": "STEP_GAP 不是通过: 原链 3 步、重推 5 步且结论相同时…必须复查 (无分型)"}
    ],
    "probe": {"type": "existence", "files": ["f:/Spec_Workflow/docs/ASSERTION_EVIDENCE_FRAMEWORK.md"], "params": {"symbols": ["gap-closed", "gap-open"], "claim": "absent", "candidates": [{"name": "权威源框架", "path": "f:/Spec_Workflow/docs"}]}}
  },
  {
    "id": "B3",
    "conclusion": "G1-G4 编号在两仓库双义撞车: Spec_Workflow doc-contract 全局动作 vs Cpp_Hub 基准对齐门禁",
    "op": "equivalence",
    "claimed_chain": [
      {"step": 1, "text": "PLAN.md §1 定义 G1-G4 = front-matter/词表/断链标注/命名空间登记", "source": "PLAN.md §1"},
      {"step": 2, "text": "DEVELOPMENT_WORKFLOW §4.1 定义 G1-G4 = 基准来源标注/三源交叉/容差达标/索引完整", "source": "DEVELOPMENT_WORKFLOW §4.1"}
    ],
    "sources": [
      {"label": "PLAN.md", "path": "f:/Spec_Workflow/spec/doc-contract/PLAN.md", "url": null, "quote": "G1. 统一 front-matter…G4. 编号命名空间登记"},
      {"label": "DW §4.1", "path": "f:/Cpp_Hub/docs/DEVELOPMENT_WORKFLOW.md", "url": null, "quote": "| G1 | 基准来源标注 | … | G4 | 基准索引完整 |"}
    ],
    "probe": {"type": "equivalence", "files": ["f:/Spec_Workflow/spec/doc-contract/PLAN.md", "f:/Cpp_Hub/docs/DEVELOPMENT_WORKFLOW.md"], "params": {"falsifier_pattern": "G1-G4 双定义点 grep", "direction": "falsify_on_miss"}}
  },
  {
    "id": "B4",
    "conclusion": "两仓库 ADR 为独立编号系列 (Spec_Workflow 四位 0004-0006 / Cpp_Hub 三位 001-019), 此前登记表仅登记四位系列断档, 不完整",
    "op": "existence",
    "claimed_chain": [
      {"step": 1, "text": "Spec_Workflow adr/ 目录 = ADR-0004/0005/0006 三份 (Glob)", "source": "Glob f:/Spec_Workflow/adr"},
      {"step": 2, "text": "Cpp_Hub ADR_INDEX 列 ADR-001~019 (Read)", "source": "ADR_INDEX L13-29"},
      {"step": 3, "text": "ADR-0007 登记节 (docs/adr/README.md) 无 Cpp_Hub 系列条目 → 登记不完整", "source": "docs/adr/README.md"}
    ],
    "sources": [
      {"label": "ADR_INDEX", "path": "f:/Cpp_Hub/docs/decisions/ADR_INDEX.md", "url": null, "quote": "| ADR-001 | Header-only Core + 单一共享库 | Accepted | … | ADR-019 … |"}
    ],
    "probe": {"type": "existence", "files": ["f:/Spec_Workflow/docs/adr/README.md"], "params": {"symbols": ["ADR-001", "Cpp_Hub 系列"], "claim": "absent", "candidates": [{"name": "登记表", "path": "f:/Spec_Workflow/docs/adr/README.md"}]}}
  }
]
```

## 附录 C: 假设区

- [H1] Crucix/docs/SPEC_WORKFLOW.md 的内容、版本、消费形态未知（本轮未取证）— 查证路径: Read 该文件 + 对照本仓库各版本差异
- [H2] DEVELOPMENT_LOG.md（1500+ 行）及 59 个未读文件可能含更多未吸收机制 — 查证路径: 分批 Read + grep "门禁|审计|框架|workflow"
- [H3] Cpp_Hub ADR-016~019 完整文档的边界决策细节未盘点（仅读 ADR_INDEX 摘要节）— 查证路径: Read 四份完整 ADR

---

**Review 签字**: _________ 日期: _________（本报告为 `自查（单视角）` 产出，按 RULE-4 须经独立 pass 复核后方可标记 `[已复核]`）
