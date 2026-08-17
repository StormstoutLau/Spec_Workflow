---
id: ADR-0007
type: adr
version: 1.1
status: accepted
date: 2026-08-17
depends: [doc-contract-refactor, CPP_HUB_GAP_ANALYSIS_RESEARCH, CPP_HUB_ABSORPTION_DESIGN, ADR-0006]
upstream: null
---

# ADR-0007: 统一文档契约——命名空间消歧与 M7 证据账本权威载体

## 元数据

| 字段 | 值 |
|------|-----|
| 编号 | ADR-0007 |
| 日期 | 2026-08-17 |
| 状态 | accepted（2026-08-17 用户确认 D1-D5 整批通过；DC token 占用检查 E1 闭合后定版） |
| 决策者 | Scott (鹏) + Claude GLM-5.3（草案生成） |
| 相关文档 | [PLAN.md](../spec/doc-contract/PLAN.md) v1.4、[CPP_HUB_GAP_ANALYSIS_RESEARCH.md](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md)、[CPP_HUB_ABSORPTION_DESIGN.md](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md)、[ADR-0006](./ADR-0006-assertion-framework-dual-copy-authority.md) |
| 取代 | 无 |

> **范围声明**: 本 ADR 承载 [PLAN.md](../spec/doc-contract/PLAN.md) §3 预留的"文档规范本体"的**决策职能**，收敛为五项裁决（D1-D5）；G1 七字段等契约全文仍由 PLAN §1 承载、P-003 执行时落入各文档，本 ADR 不复制契约文本。其中 **D1 为 cpp-hub-absorption Step 4 Review（2026-08-17）新增裁决**（P2-2 载体冲突）；D2/D3 对应差距分析 B3/B4；D4/D5 对应 PLAN §8 两项悬置 P3。

## 背景（Context）

### 1. M7 数据载体三方冲突（D1 触发，Step 4 Review P2-2）

同一批 M7 数据的承载表述两两不一致：

| 来源 | 表述 | 取证 |
|------|------|------|
| PLAN.md §6 | "M7 数据点留痕（**ADR-0007 附录承载**）" | E1 Read L178 |
| 吸收设计 D2/D3 | 新建 `docs/M7_EVIDENCE_LOG.md` 作登记载体 | E1 Read §4.2 |
| 用户第二次回流清单第 2 项 | 目标 "PLAN.md §6 / DEV-LOG（M7 样本）" | 会话输入 2026-08-17 |

实施前必须裁决唯一权威载体，否则产生双重登记悬空。

### 2. G1-G4 编号双义撞车（B3，已审计闭合）

PLAN §1 定义 G1-G4 = 文档契约全局动作（front-matter/词表/断链标注/命名空间）；Cpp_Hub DEVELOPMENT_WORKFLOW §4.1 定义 G1-G4 = 基准对齐门禁。两侧均为高频引用 token，跨仓库阅读需持续脑内消歧。审计轮 E1 重跑闭合（PLAN L33/49/61/70 vs DW §4.1 双义实证）。

### 3. 编号命名空间登记不全（B4，已审计闭合）

PLAN §4 G4 登记表缺两行：Cpp_Hub 三位 ADR 系列（001-019）与 ADR-0006 自身。审计轮 existence 探针闭合（README grep ADR-001 零命中）。

### 4. 两项 P3 悬置（PLAN §8，指派本 ADR 定稿时处理）

- P3-2: `design` 是否入 type 词表——但三份存量文档（gap-analysis RESEARCH/AUDIT、absorption DESIGN）front-matter 已事实使用 `type: design`（E1）
- P3-1: G2 状态词表双语取舍（全英/全中/映射表三选一）

## 决策（Decision，accepted 2026-08-17）

### D1. M7 证据账本权威载体 = `docs/M7_EVIDENCE_LOG.md`【新增裁决】

1. 新建账本为 M7 数据**唯一活载体**：样本登记表 / 形态 II 复发分桶 / 命中率 baseline，骨架采用吸收设计 §4.2
2. PLAN §6 降为**指针**（"数据见 M7_EVIDENCE_LOG.md"，两轮已有数据随 D2/D3 实施迁入账本）；本 ADR **不设数据附录**
3. PROGRESS P-005（形态 II 复发计数指标）同落此账本
4. DEV-LOG 语义界定：记录事件叙事（何时何轮何发现），**不承载聚合表**——账本管表，日志管事

### D2. doc-contract 全局动作 G1-G4 重命名为 DC1-DC4

- 映射: G1→DC1（front-matter）/ G2→DC2（状态词表）/ G3→DC3（引用四档）/ G4→DC4（命名空间登记）
- Cpp_Hub 侧 G1-G4（基准门禁）**保持不变**——已固化于其宪法 §4.1 表格，且属其项目内命名空间
- 联动（登记不执行）: PLAN §1/§4 全文替换（P-003 前置小改，v1.5）；吸收设计 §6 的 "G1 七字段/G3" 表述随其 P2 修正批同步——**不并入本草案**

### D3. 命名空间登记表补全（附录随本 ADR 落地）

- **入册标准**（裁决细则）: 仅跨文档复用的稳定 ID（ADR / DIS / RULE / M / Phase / E）入全局登记；实例级编码（PLAN 的 S#/T#/F# 逐文档修改点、报告内 B#ID/H#）**不入**，撞名由文档语境消解
- 补全行: 本仓库 ADR-0006~0009；[源项目·Cpp_Hub] ADR-001~019（仅登记编号空间与主题，**不吞并内容**）
- **P0 术语节**（PLAN S5 指派）: 仓库内唯一 P0 token = "P0 审计项"（SPEC_PROCESS 取证矩阵风险分级语义，保留）；问题分级 ladder 定死 P1/P2/P3（T8a 已删模板 P0 行）

### D4. `design` 入 type 词表（六类）

- 词表定稿: `process-spec / adr / discovery / framework / template / design`
- design 状态词表: `draft / in-review / verified`（与模板实例同）
- 依据: 存量三份已事实使用（E1），拒绝入册即制造存量违规

### D5. G2 双语取舍 = 英文 token 为准

- 终态: 英文 token；P-003 执行期允许"英文 + 中文括注"过渡；**不建双语映射表**（第三选项否决——维护两套词表的持续成本无对应收益）

## 决策分析（D1-D5：依据 × 收益 × 成本）

### 0. 总览：证据强度 × 成本矩阵

| 决策 | 问题性质 | 证据强度 | 实施成本 | 不决策的代价 | 性质 |
|------|---------|---------|---------|------------|------|
| D1 M7 账本 | **硬冲突**（三方表述打架） | E1 实证 | 低（新建 1 文件 + PLAN 指针化） | **阻塞**：P2-2 不清零，Tier1 无法实施 | 强制决策 |
| D3 登记补全 | 登记缺口 | E1 实证（B4 探针闭合） | 极低（附录加行） | 低但累积：跨仓 ADR 编号误读风险 | 低成本清理 |
| D4 design 入词表 | 词表滞后于事实 | E1 实证（三份存量） | ≈0（词表加一行） | P-003 执行时三份存量违规，返工 | 追认既成事实 |
| D5 英文 token | 双语并存 | 无实证（纯判断） | ≈0 | 低（三选一均可行的悬置） | 轻量判断 |
| D2 DC 重命名 | 双义撞车 | E1 实证**存在**（B3）+ 外部类比实证（§2.1）——摩擦**机制**有据，本仓摩擦**量**未量化 | 中（PLAN v1.5 + grep 复核 + 心智切换） | **随时间增长**：G 引用每多一处，未来改名成本 +1 | 需权衡（外部证据使其从"纯判断"升为"有佐证判断"） |

### 1. D1: M7 权威载体 = M7_EVIDENCE_LOG.md

**依据**
- 硬冲突实证（E1）：PLAN L178 自称"ADR-0007 附录承载" / 吸收设计 §4.2 新建账本 / 用户回流清单写"PLAN.md §6"——三方两两矛盾，实施前必须裁决，**五项中唯一的阻塞性决策**
- 生命周期错配（结构性理由）：M7 数据是**活数据**（每轮审计追加样本），ADR/PLAN 均为**快照**（定稿即归档）。活数据放快照里，每次追加都迫使决策文档修订——ADR 修订历史被数据噪声淹没

**收益**
1. 解锁 P2-2 → 吸收设计 Tier1（D2/D3 样本登记）可先行，**与 P-003 解耦**（否则 M7 登记被 doc-contract 执行进度牵制）
2. P-005（形态 II 复发分桶指标）有落点——该指标是验证"机械枚举拦截幻觉"实际有效性的唯一数据基础
3. M7 对比臂研究（同基座 vs 异基座审查能力差异）的前提是数据持续积累；载体不定，每轮样本都在丢失
4. 职责分离：账本管表（聚合数据）、DEV-LOG 管事（事件叙事）、ADR 管决策——三者查询场景不同

**成本**
- +1 文件维护负担：**僵尸账本风险**（登记后无人追加）——失效条件已登记"连续两轮无追加 → 重审并回 ADR 附录"
- PLAN §6 两轮已有数据需一次性迁入（约 10 行，机械）
- 单人仓库多一处查询点

### 2. D2: G1-G4 → DC1-DC4 重命名

**依据**
- B3 双义实证（E1，审计轮探针闭合）：本仓库 G1-G4 = 文档契约动作；Cpp_Hub G1-G4 = 基准对齐门禁，固化于其宪法 §4.1
- **证据的诚实边界**：B3 证明撞车**存在**，未证明撞车**昂贵**——摩擦无量化数据。撞车实际是单向的：各自仓库内语境自动消歧，真正混淆场景是**跨仓库对照文档**（如差距分析、吸收设计）

**收益**
1. 消除跨仓库阅读的持续脑内消歧（频率取决于回流任务量——回流越频繁收益越大）
2. **现在改名是成本最低点**：当前 G 引用仅集中在 PLAN + 少数文档；每拖延一个 feature，G1-G4 新引用 +N 处，未来改名成本线性增长
3. 为跨仓库命名空间卫生立先例（与 D3 同一原则的两面：D3 管登记，D2 管去重）

**成本**
- PLAN v1.5 一次改写：全文替换 + **grep 甄别复核**（须区分本仓库 G1-G4 引用 vs 对 Cpp_Hub G1-G4 的引文——如 B3 探针定义那两处，误替换会破坏证据记录）
- DC 缩写潜在新撞车（M1-M7 里程碑、未来 DC 语义），替换前须 grep `DC[1-4]` 零命中验证（见验证节 ⏳ 项）
- 会话/记忆软成本：对话上下文中 G1-G4 已建立，需切换

**权衡结论**：回流任务常态化 → 现在改名；回流低频 → 翻转为"登记共存"（替代方案节已备，翻转零成本）。判断参数唯一：**回流任务的预期频率**。

### 2.1. D2 外部证据补充（MCP 检索，2026-08-17）

> 检索记录（诚实声明）：`search_semantic` 两轮空返回（服务端异常，无证据采信）；`search_web` 镜像三次超时后改用内置 WebSearch 兜底。实际采证通道：`search_arxiv`（2 篇命中）、StackExchange `search_questions`+`get_answers`（1 题三答案）、WebSearch（K8s 官方文档 + 原始提案）。
>
> **页面级 grep 复核记录（2026-08-17，独立 pass）**：四源引文逐条重验，4/4 命中。证据等级由"检索级 A 类"升级为"页面级/API 级复核 A 类"。
>
> | 证据 | 复核通道 | 结果 |
> |------|---------|------|
> | E1 引文一 | WebFetch 页面 + grep → **L61 逐字命中** | ✅ |
> | E1 引文二 | 同页 grep → **L87 逐字命中**（且第二引文上下文"To support identically named kinds in different groups, We need to expand…"进一步佐证映射解读） | ✅ |
> | E2 两引文 | HTML 页面被反爬安全验证拦截（StackPrinter 镜像兜底亦失败）——引文源为 StackExchange 官方 API（`get_answers` 返回 `body_markdown`，页面渲染的同一数据源），**API 级逐字命中**；页面级不可达如实登记 | ✅（API 级） |
> | E3 | WebFetch arXiv abs 页 → 摘要子串逐字命中；升级元数据：**ICSE'2023 正式接收**（v2） | ✅ |
> | E4 | WebFetch arXiv abs 页 → 摘要逐字命中（v2）；期刊元数据：Int'l Journal of Computer and Information Technology 2014（中等venue，权重如实登记） | ✅ |

**E1. Kubernetes API group 设计提案——"歧义 → 强制限定"是业界标准处置**

【A】(源: https://github.com/zevarito/Kubernetes/blob/master/docs/proposals/api-group.md （k8s 原始提案 api-group.md 的 fork 镜像）; 引文: "Supporting identically named kinds to exist in different groups. This is useful when we experiment new features of an API in the experimental group while supporting the stable API in the original group" / "If group is not specified and there is ambiguity (i.e., the resource exists in multiple groups), an error should be returned to force the user to specify the group")

映射：全球最大规模的基础设施系统在遇到"同名资源跨组并存"时，选择**分组命名空间化**而非"靠语境消歧"，且歧义时**强制显式限定**。更关键的同构细节：K8s 保留 legacy core 组原名（空组名 `/api/v1`），只为**新增组**加域名前缀（`networking.k8s.io`、`rbac.authorization.k8s.io`）——与 D2 的方向完全同构：**Cpp_Hub 侧（既有、项目内）不动，本仓库侧（新增语义、跨仓可见）改名**。

**E2. StackExchange 社区共识——项目前缀是撞车的标准解**

【A】(源: https://softwareengineering.stackexchange.com/questions/330987/namespaces-and-header-guards-with-naming-conflicts 票首答案（score 3，Sebastian Redl）; 引文: "A common convention is to add a project and in-project path as a prefix, e.g. `#ifndef MYPROJECT_UTILITY_CONTAINERS_LINKED_LIST_HPP`")

【A】(源: 同题采纳答案（user22815）; 引文: "One method I use is to build a more complex macro name that has a practically zero chance of colliding with other names. This could be built from the following components: Project name / Namespace name / File name")

映射：C++ 头文件卫兵的跨项目撞车（与 G1-G4 撞车结构同构：预处理符号无命名空间、跨编译单元全局可见）的社区标准答案即**项目作用域前缀**。DC1-DC4（DC = Document Contract，仓库作用域）是该模式的直接实例。

**E3. arXiv 2207.11104——同 token 双义对模型的误导有实证机制**

【A】(源: http://arxiv.org/abs/2207.11104v2 （Gao et al., cs.SE）; 摘要引文: "neural code comprehension models are vulnerable to identifier naming. By renaming as few as one identifier in the source code, the models would output completely irrelevant results, indicating that identifiers can be misleading for model prediction")

映射（三角互证）：本仓摩擦主体**不是人类读者而是跨仓作业的 LLM agent**（回流任务由 agent 执行）。外部实证：标识符语义误导是模型级现象，非仅人类认知负担。与本仓内部实证互证——AUDIT §4 形态 II 规律一（弱记忆填充偏好低语义载荷字段）意味着：agent 凭印象填写"G1"语义时，两个仓库的双义定义恰是弱记忆填充的**激活温床**。内部（三实例复发）× 外部（模型易感性实证）共同将"摩擦未量化"升级为"摩擦有实证机制，量级未知"。

**E4. arXiv 1401.5300——前缀的反面教训（约束条件）**

【A】(源: http://arxiv.org/abs/1401.5300v2 （Wang et al., 48 个 OSS 项目实证）; 摘要引文: "For the identifier naming popularity, it is found that Camel and Pascal naming conventions are leading the road while Hungarian notation is vanishing")

映射（反向约束）：前缀消歧**不可滥用**——匈牙利命名法的消亡证明全词表无差别前缀化是净损耗。D2 的 DC 前缀仅作用于撞车的 G 系列 4 个 token（scoped prefix），非全词表前缀化，符合该实证给出的存活边界。

**证据综合后的修订判断**

1. 上述证据**不改变** D2 的成本项（PLAN v1.5 + grep 甄别 + 心智切换），也**不替代**核心判断参数（回流频率）——外部证据提供的是机制佐证与先例，不是本仓摩擦的量化数据
2. 但证据改变了摩擦的性质认定：从"可能是理论洁癖"升为"有 K8s 级先例 + 社区标准解 + 模型级易感性实证的真实失效模式"，且本仓工作流（LLM 跨仓作业 + 形态 II 已三实例复发）恰好落在该失效模式的暴露面上
3. 修订后的决策建议维持双分支，但阈值下调：原判断"回流常态化才改名"修订为——**只要预期存在第三次及以上回流（本仓已执行两次），改名即有正期望**；因每次回流都是一次跨仓双义暴露，而暴露成本的主承载者（agent 误读 → 形态 II 错误 → 审计轮拦截）的单位成本远高于一次 PLAN v1.5 机械改写

### 3. D3: 命名空间登记补全

**依据**
- B4 探针闭合（E1）：登记表缺 Cpp_Hub ADR-001~019 系列与 ADR-0006 自身
- P0 术语节为 PLAN S5 指派任务（否则 P-003 执行时 S5 无落点）

**收益**
1. 防跨仓误读：ADR-0006（本仓库，双份权威源决策）vs ADR-019（Cpp_Hub，复核 pilot）是**两个独立系列**——不登记，读者默认同系列连续编号，会得出"0006 早于 019、被 019 取代"类错误推断
2. "仅登记编号空间与主题，不吞并内容"是 Tier3 拒收原则在登记层的镜像——为"吸收机制不吸收实例"立可查边界
3. **入册标准**（稳定 ID 入全局 / 实例编码入文档语境）是可扩展规则，未来 M8+/RULE-7+ 出现时不再逐案讨论

**成本**
- 极低：附录加行 + 一次入册判断
- 长期纪律成本：新 ID 诞生时需判断是否入册（一次性规则，边际成本递减）

### 4. D4: `design` 入 type 词表

**依据**
- 纯事实追认（E1）：gap-analysis RESEARCH/AUDIT、absorption DESIGN 三份 front-matter 已 `type: design`；PLAN 头部自认"G2 词表缺口"并指派本 ADR 裁决
- AUDIT 文档 `status: verified` 在现有五类词表无合法归属（process-spec/framework 用 active/deprecated，template 实例才用 verified）

**收益**
1. P-003 Step C（G1 front-matter 批量）执行时三份存量合法，避免"改造动作制造违规再返工"的回路
2. SPEC_PROCESS 10 步流程的 Step 3-4 产出（DESIGN 文档）自此有正式类型归属——词表与流程对齐

**成本**
- ≈0：词表一行 + design 状态映射（draft/in-review/verified，复用模板实例词表）
- 唯一隐性约束：第六类定型后，未来"方案类文档"（如 PLAN 自身）是否归 design 成为新问题（PLAN 目前无 type，属 G1 批量范围，P-003 时自然处理）

### 5. D5: G2 双语 = 英文 token

**依据**
- 纯 C 类判断（无实证，三选一悬置）：现状中文状态（草稿/Review 中/已验证）与提案英文 token 并存
- **与框架自身哲学的一致性**是主要论据：本框架核心是 E1 机械可重放证据——英文 token 可 grep（`status: verified` 一条命令全仓复核），中文状态对脚本不友好（编码/分词）；front-matter 是 YAML，生态惯例英文

**收益**
1. 机械可验证性：P-003 的完成定义（grep 复核四项）直接依赖英文 token 可 grep
2. 与 front-matter 生态对齐，跨项目复制（v1.2.1 自包含化目标）无翻译层
3. 三方案中维护面最小

**成本**
- 中文可读性下降（缓解：过渡期"英文 + 中文括注"，已写入决策节）
- 一次性心智切换（单人成本，一次性）
- **映射表方案否决理由**：双维护面 + 同步失败风险（两套词表必然漂移——本仓库刚处理过 G1-G4 撞车，不应再造一个）

### 6. 确认优先级建议（草案期辅助节，2026-08-17 已完成确认——D1-D5 整批通过）

```
必确认（阻塞项）:  D1          —— P2-2 不清零则 Tier1 停摆            ✅ 已确认
低风险顺带确认:    D3 + D4     —— 成本近零，证据扎实，无下游联动      ✅ 已确认
轻判断确认:        D5          —— 无实证支撑但三选一代价都小          ✅ 已确认
需权衡（已升级）:  D2          —— 外部证据补充后（§2.1）：K8s 先例 + SE 共识 +
                                  模型易感性实证，摩擦从"未量化"升为"有实证机制"
                                  修订阈值：预期 ≥ 第三次回流（本仓已两次）即正期望 ✅ 已确认
```

## 考虑的替代方案（Alternatives Considered）

### D1 替代

- **B: ADR-0007 附录承载**（PLAN §6 原案，否决）: 决策文档是快照不是活账本——每轮审计样本追加都迫使 ADR 修订，决策记录被数据噪声淹没；且本 ADR 定稿时点受 P-003 牵制，M7 登记被无关任务阻塞
- **C: PLAN §6 承载**（用户清单原表述，否决）: PLAN 状态 final-pending-execution，执行后归档；活数据放执行方案里生命周期错配

### D2 替代

- **双登记共存**（仅附录声明双义，否决）: 治标——登记表能查到撞车存在，但每次阅读仍需人工消歧，B3 的实际摩擦不消除
- **Cpp_Hub 侧重命名**（否决）: 跨仓库改动面大（其宪法多处固化），且 G1-G4 在 Cpp_Hub 是项目内 token，无义务为外部仓库让名

### D4 替代

- **拒绝入词表**（否决）: 三份存量违规在前，回改三份 front-matter 的成本高于词表扩一行

## 后果（Consequences）

### 正面

- M7 载体唯一化，P2-2 冲突闭环；M7 登记与 P-003 解耦（吸收设计 Tier1 可先行）
- G1-G4 撞车在 P-003 执行前消除，此后新增文档引用 DC 系列无歧义
- B3/B4/P3-1/P3-2 四项悬置一次性清账

### 负面

- PLAN 需一次 v1.5 小改（§6 指针化 + G→DC 全文替换，含 grep 复核）
- "DC" 与既有 M/DC 类缩写潜在新撞需在替换时目检（目前仓库无 DC token 占用，E1 grep 零命中可先行验证）

### 中性 / 后续行动

- P-003 Step F 以本 ADR accepted 版为准
- 本 ADR accepted 后，CODE_WIKI 尾随同步（PLAN §4 既定动作，随 P-003 一并）

## 验证（Validation）

### 已有实证

| 依据 | 取证方式 | 等级 | 状态 |
|------|---------|------|------|
| 三方载体冲突 | Read PLAN L178 / DESIGN §4.2 / 会话清单 | E1 | ✅ |
| G1-G4 双义 | 差距分析审计轮探针重跑（B3 闭合） | E1 | ✅ |
| 登记表缺行 | existence 探针（B4 闭合） | E1 | ✅ |
| type: design 存量使用 | Read 三份 front-matter | E1 | ✅ |
| DC token 未被占用 | grep `DC[1-4]` 全仓（accepted 定版时执行，2026-08-17）——仅本 ADR 自身 4 处定义性引用，外部零占用 | E1 | ✅ |

### 待验证项

- ~~用户确认 D1-D5（逐项或整批）~~ ✅ 2026-08-17 用户确认 ADR-0007 通过（D1-D5 整批）
- PLAN v1.5 联动改写 + grep 复核（`G[1-4]` 语义甄别后替换，防误伤 Cpp_Hub 引文）——**未执行**，随 P-003 / D2 实施时进行

### 失效条件（何时重审）

- M7_EVIDENCE_LOG 连续两轮审计无追加（僵尸账本）→ 重审是否并回 ADR 附录（回到方案 B）
- DC 系列在消费方（Crucix/Cpp_Hub）引起新歧义 → 重审命名策略

## 修订历史

| 日期 | 变更 |
|------|------|
| 2026-08-17 | 初始草案（proposed）：五项决策（D1 载体裁决为 Step 4 Review P2-2 修复；D2/D3 对应 B3/B4；D4/D5 清 PLAN §8 两项 P3），待用户确认 |
| 2026-08-17 | 补充"决策分析"节（D1-D5 依据 × 收益 × 成本 + 证据强度矩阵 + 确认优先级建议），供用户逐项确认参考 |
| 2026-08-17 | D2 外部证据补充（§2.1，MCP 检索）：K8s API group 提案 / SE 330987 / arXiv 2207.11104 / arXiv 1401.5300 四条检索级 A 类证据 + 修订决策阈值（预期 ≥ 第三次回流即正期望）；总览矩阵 D2 行同步 |
| 2026-08-17 | §2.1 页面级 grep 复核（独立 pass）：4/4 引文命中（E1 L61/L87 逐字、E3/E4 arXiv 摘要逐字且 E3 升级为 ICSE'2023 接收、E2 API 级命中 + 反爬拦截如实登记），证据等级升级为页面级/API 级复核 A 类 |
| 2026-08-17 | proposed → **accepted**（用户确认 D1-D5 整批通过）；DC token 占用检查 E1 闭合（全仓 grep 仅本 ADR 4 处定义性引用，零外部占用）；版本 v1.0 → v1.1；确认优先级节/待验证项同步定版 |
