# 调研文档：M7 hits 机读块 + 样本登记脚本化

---
id: m7-hits-block-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-08-21
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0007, precommit-dc-validator-DESIGN]
upstream: null
---

> **Feature**: m7-hits-block（PROGRESS P-011，优先级 2，主动队列次位）
> **创建日期**: 2026-08-21
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: [PROGRESS P-011](../../docs/PROGRESS.md)——"M7 统计升 \`\`\`hits 机读块 + 样本登记脚本化"，双重背书：[M7 §4](../../docs/M7_EVIDENCE_LOG.md) 待办挂钩（[CPP_HUB_ABSORPTION_DESIGN §6](../cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) 既定）+ [LANGGRAPH_UPGRADE_RESEARCH §6](../langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) 零成本项
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 11 | 每条附仓库内 E1 取证（文件 + 行号 + 可 grep 引文），2026-08-21 Read/Grep 取证 |
| B 推断类 | 1 | B1，登记于附录 B |
| C 判断类 | 3 | §4.2 决策判断 |
| 假设区 | 2 | H1-H2，未取证声明 |

**扫描范围声明**: 本调研为仓库内部调研（无外部文献需求）——覆盖 M7_EVIDENCE_LOG.md 全文、scripts/dc_validator.py 全文、.pre-commit-config.yaml 全文、SPEC_PROCESS/LANGGRAPH 机读块先例、PROGRESS P-011 条目。未覆盖：pre-commit 框架源码（仅用其既证配置形态）、dc_validator selftest 13 fixture 逐条复跑（属 Step 9-10 范围）。

## 1. 调研目标

**核心问题**:
1. M7 账本当前的手工统计面有哪些，哪些可机械重数？（hits 机读块的内容契约）
2. 样本登记流程中哪些环节可脚本化，哪些必须保留人工判断？（脚本辅助的边界）
3. 与 dc_validator R7 计数检查如何衔接——并入 dc_validator 还是独立脚本？

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| Read | M7 账本 / dc_validator.py / .pre-commit-config.yaml / 机读块先例全文取证 | 逐文件 |
| Grep | hits / 机读 / pre-commit 衔接点定位 | 全仓 |
| 机械重数 | 样本"形态II复发"列求和 / 分桶表行列算术 / P 计数抽取 | 人工枚举（Step 9 由脚本接管） |

### 2.2 调研范围

- **范围**: 仓库内部（docs/M7_EVIDENCE_LOG.md、scripts/、SPEC_PROCESS、spec/ 先例文档、PROGRESS）
- **排除**: 外部文献（本 feature 无技术选型不确定性——工具形态已被 P-007 先例完全定型）

## 3. 调研发现

### 3.1 M7 账本的手工统计面（hits 块内容契约的输入）

【A】A1: 样本登记表 = 14 行 × 7 列

- **取证**: [M7_EVIDENCE_LOG.md](../../docs/M7_EVIDENCE_LOG.md) L9-L24，表头引文（可 grep）: `| # | 日期 | 载体 | 审查配置 | 发现 | 形态II复发 | 来源 |`
- **关键结论**: 行数与列结构是机械可数的；行首整数（样本号 1-14）+ 第二列日期（YYYY-MM-DD）可作行合法性探针。

【A】A2: 分桶表 = 15 载体行 + 合计行，7 字段类型列 + 小计列

- **取证**: M7 L32-L49，合计行引文: `| **合计** | 1 | 2 | 3 | 2 | 10 | 1 | 2 | **21** |`
- **关键结论**: 行算术（每行小计 = 7 字段格之和）与列算术（合计行 = 各列竖加）均可机械复验——正是 M7 样本⑪③"混轴"与样本④"计数/行号"类错误的高危面。

【A】A3: 分桶表含 1 行先于账本的历史行（Phase 7C，小计 6）

- **取证**: M7 L34: `| Phase 7C 调研报告（Cpp_Hub） | 1 | 2 | 3 | — | — | — | — | 6 |`；样本登记表 1-14 行中无 Phase 7C 行（其 6 处形态 II 为账本建立前的历史数据，载于框架 §2.2 复盘表）
- **关键结论**: 跨表对账不变式存在且当前成立：分桶合计 21 = 历史基线 6 + 样本"形态II复发"列之和。

【A】A4: 样本"形态II复发"列前导整数之和 = 15

- **取证**: 机械枚举 M7 L11-L24 该列: 0, 0, 1, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 0 → 合计 15；且 15 = 21 − 6（A3 不变式当前成立）。该列值形如 `1（转述引文）` / `3（计数×3——…）`，前导整数即计数。
- **关键结论**: 跨表对账可脚本化，是 hits 块最有价值的单一校验项（手工登记"加了样本行忘加分桶行"或反之的最常见遗漏将被拦截）。

【A】A5: "发现"列 P 计数可机械抽取，样本③ 为非标准形态

- **取证**: 该列两种标准形态: `10（2P1+5P2+3P3）`（L11）/ `2P2+6P3`（L15）；样本③（L13）为 `R2 拦截 1/4；双盲 5/5 TRUE`——pilot 特殊配置，无 P 分解，不计入 P 汇总（须显式声明排除，防"静默少算"）。
- **关键结论**: P1/P2/P3 汇总统计可行，但须带"非标准单元格计数"字段如实登记排除面。

【A】A6: 样本⑨ 含 1 项未标级发现（前导总数 > P 标记和）

- **取证**: M7 L19: `4（1P1 计数漏计 + 2P2 断链 + 1 工具自身计数缺陷）`——P 标记和 = 3，前导总数 = 4，差额 1 为未标 P 级的第 4 项（工具自身计数缺陷）。
- **关键结论**: "前导总数 = P 标记和"不能作为硬校验（历史数据如实含未标级项）——差额须作为 `unlabeled` 统计字段机械登记，P 标记和 **大于** 前导总数才是真违规。**禁止回改历史单元格补标级**（虚造历史分级 = 数据造假）。

【A】A7: dc_validator 先例——退出码 0/1/2 + 内嵌 selftest + 零第三方依赖

- **取证**: [dc_validator.py](../../scripts/dc_validator.py) L10: `退出码：0 全部通过 / 1 发现契约违规 / 2 工具自身错误`；L321 起 `run_selftest()`（tempfile 构造 fixture 于系统临时目录，不触工作树）。
- **关键结论**: 新脚本应同构继承三件套（退出码语义 / --selftest / 零依赖），用户心智与 pre-commit 通道零新增学习成本。

【A】A8: pre-commit 配置现有单 hook，Windows 陷阱已实证

- **取证**: [.pre-commit-config.yaml](../../.pre-commit-config.yaml) L9-L13: `entry: python scripts/dc_validator.py` + `language: system` + `files: \.md$`；注释 L5: `entry 走 python 前缀（Windows 无 /bin/sh，RESEARCH §2.1 陷阱实证）`。
- **关键结论**: 新增第二 hook 只需追加条目，`files:` 可收窄到 M7 文件路径；entry 必须沿用 `python` 前缀。

【A】A9: 机读围栏块先例——```rules 与 ```assertions 均 JSON

- **取证**: [SPEC_PROCESS.md](../../SPEC_PROCESS.md) L331 ```rules 块（JSON 数组）；[LANGGRAPH_UPGRADE_RESEARCH.md](../langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) L152 ```assertions 块（JSON 数组）。
- **关键结论**: ```hits 块沿用同族形态（围栏语言标注 + JSON），不发明新记法。

【A】A10: dc_validator M5 对 fenced code block 内链接跳过——hits 块零干扰

- **取证**: dc_validator.py L211-L214: 围栏行 `in_fence = not in_fence` 翻转、围栏内行 `continue`。
- **关键结论**: hits 块（围栏内）不会被 M5 链接检查误报，两工具可并行。

【A】A11: dc_validator M4 仅对含 "## 0. 断言统计表" 的文档生效——R7 当前不覆盖 M7

- **取证**: dc_validator.py L168 `RE_STAT_SECTION = re.compile(r"^##\s*0[\.、]?\s*断言统计表", re.M)` + L174 `if not RE_STAT_SECTION.search(text): return []`；M7_EVIDENCE_LOG.md 无该节标题（Grep 零命中）。
- **关键结论**: "衔接"不是"已覆盖"——M7 的统计对账目前完全依赖人工，正是 P-011 要填的空档；hits 块 + 新脚本是 R7 在 M7 载体上的同构延伸，而非 dc_validator 的行为变更。

### 3.2 样本登记流程的脚本化边界

#### 【B】B1: M7 手工登记的计数风险面 = 三处，全部是形态 II 计数桶的既有复发位点

- **推理链**（附录 B 机读登记）: ① 样本行数与行结构（样本⑪③ 混轴：称 16 实为 10/11）→ 行合法性探针可拦；② 分桶行/列算术（样本④ GAP_ANALYSIS 计数错、样本⑩ A=14→11）→ 行列算术复验可拦；③ 跨表对账（样本⑪② 复制同错至 DEV-LOG-004——同一错误多处出现仅改一处）→ A3/A4 不变式可拦。三处对应 M7 §2 计数桶 10 处复发（合计 21 中的 10）——**登记计数错误的账本，自身统计恰是最顽固载体**（规律② 元断言逃逸的载体级实例）。
- **边界（不可脚本化，须保留人工）**: 样本行的语义内容（载体描述、审查配置、发现描述、来源锚点）与分桶行的归类判断（哪类字段类型、载体标签措辞）——机械探针只验形态与算术，不判语义。

### 3.3 与 dc_validator 的衔接形态

事实基础（A7/A8/A10/A11）之上的关键判断见 §4.2 C1。

## 4. 综合分析

### 4.1 关键发现总结

1. M7 的可机械重数统计面 = 样本行数、分桶行列算术、跨表对账不变式、P 分级汇总四类，当前全部手工（A1-A6）[置信度: ★★★★★]
2. 历史数据含两处"非整齐"形态（样本③ 非标准发现、样本⑨ 未标级发现），hits 契约必须如实容纳而非强行归一（A5/A6）[置信度: ★★★★★]
3. dc_validator 已定型全部工程先例（退出码/selftest/零依赖/pre-commit 通道），且 R7 明确不覆盖 M7（A7/A8/A11）[置信度: ★★★★★]
4. 三处计数风险面与形态 II 计数桶复发位点一一对应——脚本拦截的是本仓库已付费的失效模式，不是假设性需求（B1）[置信度: ★★★★☆]

### 4.2 技术判断（C 类）

【C】**C1: 独立脚本 + 独立 pre-commit hook，不并入 dc_validator。** 理由链：① 职责分离——dc_validator 是全仓通用 DC 契约执行器（I-3 零新规则、I-4 单一真值源），M7 统计解析是单文件特化逻辑（表结构耦合，M7 表格式演化会迫使通用工具连带变更）；② P-008 已将 dc_validator 定为 verified/accepted 状态，为其追加非 DC 契约功能将重开审查面，收益为零；③ "衔接"语义 = 同构原则共享（R7 声明 vs 机械重数 + 退出码语义 + pre-commit 通道），PROGRESS P-011 措辞为"衔接"非"并入"。

【C】**C2: hits 块只承载可机械重数的统计，禁含时间戳/哈希等非确定字段。** 理由：--write 重生成必须逐字节确定（dc_validator I-2 同构）；`generated_at` 类字段会让每次重跑产出不同文本，制造无意义 diff 噪音并破坏"重数 = 声明"的可证伪性。

【C】**C3: "脚本辅助登记"的边界 = 校验 + 重生成 + 提交拦截，不自动起草样本行。** 理由：B1 已界定语义内容须人工；脚本若代起草反而引入新的生成端幻觉面（与 M7 规律③"拦截层 ≠ 生成端"冲突）。

### 4.3 研究空白（本 feature 填补）

M7 账本是 ADR-0007 D1 钦定的唯一活载体，但其聚合统计（样本数/分桶/跨表对账）无任何机械校验层——与"登记纪律"条款（连续两轮无追加即触发失效重审）所要求的账本可信度不匹配。本 feature 填补该空档。

## 5. 幻觉排除审查（Step 2 Review）

### 5.1 事实验证

| 引用 | 取证 | 验证方式 | 状态 |
|------|------|---------|------|
| A1-A6（M7 表结构/数值） | M7_EVIDENCE_LOG.md L9-L49 | Read 逐行 + 机械枚举（形态II列求和 / 行列算术 / P 标记抽取） | ✅ 2026-08-21 |
| A7（dc_validator 先例） | dc_validator.py L10/L321 | Read 读码 | ✅ |
| A8（pre-commit 配置） | .pre-commit-config.yaml L1-13 | Read 全文 | ✅ |
| A9（机读块先例） | SPEC_PROCESS L331 / LANGGRAPH L152 | Read | ✅ |
| A10/A11（M4/M5 行为边界） | dc_validator.py L168-L174/L211-L214 | Read 读码 | ✅ |

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| 历史数据两处非整齐形态（A5/A6） | M7 L13/L19 | ✅ 引文逐字符核对 |
| R7 不覆盖 M7（A11） | dc_validator.py L168/L174 + M7 Grep 零命中 | ✅ 双向验证（正则定义 + 目标文件无该节） |

### 5.3 待修正项

- 无（本调研零外部引用，无文献验证面；内部取证全部 E1 级）

> **门禁自查（ADR-0008 D4）**: (a) 无 FALSIFIED 断言；(b) 无 CONFLICT/STEP_GAP；(c) 阻断性断言（A1-A11 表结构契约）全部 E1 取证，B1 推理链依赖源各自附 A 级证据；(d) 假设区 H1/H2 以 [待定] 显式携带进 DESIGN。**标注**: 本节为 `自查（单视角）`（RULE-4，同会话完成）——独立 pass 待 Step 10 或用户触发。

## 6. 对设计的输入

### 6.1 可用的技术方案

1. 独立脚本 `scripts/m7_stats.py`：校验（默认）/ `--write` 重生成 hits 块 / `--selftest` 内嵌自测
2. pre-commit 第二 hook：`files: ^docs/M7_EVIDENCE_LOG\.md$` 收窄作用域
3. hits 块 JSON 契约：samples / form2_by_field / form2_total / form2_pre_ledger / form2_from_samples / findings（p1/p2/p3/unlabeled/cells_nonstandard）

### 6.2 关键约束

1. 历史非整齐形态如实容纳：非标准发现单元格计数入 hits（A5）、未标级差额入 unlabeled（A6）、禁止回改历史数据
2. 确定性：--write 逐字节稳定，无时间戳（C2）
3. Windows：entry 用 `python` 前缀（A8）
4. 与 dc_validator 零冲突：hits 块围栏内内容不触发 M5；M7 无 §0 节不触发 M4（A10/A11）
5. 只读校验 + 显式 --write 才写（dc_validator I-1 的变体：默认只读，写操作须显式旗标）

### 6.3 风险

| 风险 | 缓解 |
|------|------|
| 解析器自身计数错（规律②：防幻觉工具自身不设防——样本⑨ 前科） | selftest fixture 覆盖全部行/列/跨表算术 + expect 自增机械计数（dc_validator DR-6 同构） |
| M7 表格式未来演化使解析器过期 | 解析失败 ≠ 静默通过：结构性解析失败报 P1（声波式失败，强制人工介入） |
| pre_ledger 基线（6）硬编码漂移 | 基线值声明于 hits 块（数据非代码常量），对账失衡即 P1 强制同步 |

## 7. 参考文献

全部为仓库内部文档（正文已逐条链接取证）：M7_EVIDENCE_LOG.md、scripts/dc_validator.py、.pre-commit-config.yaml、SPEC_PROCESS.md、LANGGRAPH_UPGRADE_RESEARCH.md、CPP_HUB_ABSORPTION_DESIGN.md、docs/PROGRESS.md。

---

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "M7 手工登记的计数风险面 = 样本行结构 / 分桶行列算术 / 跨表对账三处，全部是形态 II 计数桶既有复发位点，脚本拦截有已付费的失效模式实证",
    "op": "transitivity",
    "claimed_chain": [
      {"step": 1, "text": "M7 §2 计数桶 10 处复发（合计 21 中），含样本④ GAP_ANALYSIS 计数错、样本⑩ A=14→11、样本⑪ 三处计数错+混轴", "source": "M7_EVIDENCE_LOG.md L36-L49 分桶表 + L21 样本⑪"},
      {"step": 2, "text": "三处风险面（行结构/行列算术/跨表对账）与 ① 的复发位点一一对应：行结构↔⑪③ 混轴、行列算术↔④⑩、跨表对账↔⑪② 复制同错", "source": "M7_EVIDENCE_LOG.md L21 样本⑪ 描述"},
      {"step": 3, "text": "三处均可用机械探针拦截（行合法性格式、行列求和复验、合计=基线+样本列和不变式）", "source": "本报告 A1-A4 取证 + 算术验证"}
    ],
    "evidence_strength": "E1（依赖源逐条 Read 取证）",
    "audit_status": "CLOSED（同基座降级独立 pass 完成——RULE-1 时序独立满足，RULE-5 模型异质性未满足，如实降级）"
  }
]
```

## 附录 C: 假设区（未取证声明）

- [H1] 分桶表"先于账本"行当前仅 Phase 7C 一行（小计 6）——查证路径: 脚本落地后跨表对账不变式将持续验证；若未来新增非样本来源分桶行，对账失衡将强制更新 `form2_pre_ledger` 声明值（P1 拦截，不静默）
- [H2] pre-commit hook 对 M7 单文件变更的运行成本可忽略（~百行级解析）——查证路径: Step 10 实测提交耗时

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）
