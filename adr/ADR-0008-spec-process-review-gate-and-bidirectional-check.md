---
id: ADR-0008
type: adr
version: 1.0
status: proposed
date: 2026-08-17
depends: [CPP_HUB_ABSORPTION_DESIGN, CPP_HUB_GAP_ANALYSIS_RESEARCH, SPEC-PROCESS, FWK-ASSERTION]
upstream: null
---

# ADR-0008: SPEC_PROCESS v1.4——Step 2 门禁语义与 Step 8 双向链路检查

## 元数据

| 字段 | 值 |
|------|-----|
| 编号 | ADR-0008 |
| 日期 | 2026-08-17 |
| 状态 | proposed（草案，待用户确认） |
| 决策者 | Scott (鹏) + Claude GLM-5.3（草案生成） |
| 相关文档 | [SPEC_PROCESS.md](../SPEC_PROCESS.md) v1.3、[CPP_HUB_ABSORPTION_DESIGN.md](../spec/cpp-hub-absorption/CPP_HUB_ABSORPTION_DESIGN.md) §4.3/§4.5（D4/D6 接口）、[CPP_HUB_GAP_ANALYSIS_RESEARCH.md](../spec/cpp-hub-gap-analysis/CPP_HUB_GAP_ANALYSIS_RESEARCH.md) §3.1-1/2/8 |
| 取代 | 无 |

> **scope 声明（相对吸收设计的修正）**: 吸收设计 §2.2 原将本 ADR 范围写为"D4 的决策记录"，D6（Step 8 增强）无 ADR 承载——Step 4 Review 判定为决策记录悬空（缺口 B）。本草案显式承载 **D4 + D6 两项决策**，与设计 §9.1 "D4/D6 同升 SPEC_PROCESS v1.4" 的同版裁定对齐。

## 背景（Context）

### 1. R 门禁语义源（已审计 A 类证据）

Cpp_Hub DEVELOPMENT_WORKFLOW v1.1 §4.2 定义 R1-R4 调研证据门禁，核心语义：

- R4 阻断性清零（源: §4.2 L239; 引文: "spec 将引用的阻断性断言：FALSIFIED 已改写、CONFLICT/STEP_GAP 已仲裁、双源满足"）——过审计 A12
- 串联流水线（源: 同上 L241; 引文: "两门禁串联：**R 清零 → spec 冻结 → 实施 → G 清零 → 合并**"）——过审计 A2
- 实效实证: ADR-019 复核 pilot R2 门禁首轮即机械拦截 1/4 引文失准（形态 II 转述填充）——过审计 A14

### 2. Spec_Workflow 现状缺口

SPEC_PROCESS v1.3 的 Step 2 Review 是 **checklist 语义**（五项勾选，无阻断条件）；Step 8 一致性检查为单向列举（RESEARCH↔DESIGN↔IMPL↔CHECKLIST 逐对），无 ADR 反向登记检查、无断言状态延续检查。Cpp_Hub 侧三文档对齐审计（59 项双向链路，过审计 A8）证明反向链路是真实失效位。

### 3. 决策悬空修复

吸收设计将 D6 归为"随 D4 同版"但未给决策记录载体。若 ADR-0008 只覆盖 D4，D6 的裁剪依据（F1-F8 模式取两项、集成点选择）无据可查，违反设计自身不变式 4 的精神。

## 决策（Decision，proposed 待确认）

### 决策 1（D4）: Step 2 Review 升格为门禁语义

Step 2 Review 章末新增【门禁】块，**满足前禁止进入 Step 3**：

```text
【门禁】Step 2 Review 全项通过 + 断言审计结论满足 R 语义:
  (a) FALSIFIED 断言已改写并记入修订记录
  (b) CONFLICT / STEP_GAP_OPEN 已仲裁
  (c) 阻断性断言双源满足（单源须标 [单源-待二核]）
  (d) 假设区条目已转 A/B 或以 [待定] 显式携带
```

- **最小化原则**: 门禁保持 4 条，与 R4 语义对齐而非复制 R1-R4 全文（单人流程 skip-and-forget 风险缓解，设计 §9.2 既定）
- 依赖: (b) 的 STEP_GAP_OPEN 词表由框架 v1.3（吸收设计 D1，Tier1）先行提供——**执行顺序 D1 → D4**

### 决策 2（D6）: Step 8 检查清单 +2 项

```text
- [ ] 双向引用完整: 四文档 + 相关 ADR 互引均成立
      （正向: 文档引用的 ADR 存在; 反向: 相关 ADR 的"相关文档"含本 feature 链接）
- [ ] 断言延续: RESEARCH 的 B 类断言状态在 DESIGN/IMPLEMENTATION 引用处
      已按最新词表标注（含 STEP_GAP_CLOSED/OPEN）
```

- 依据: Cpp_Hub 三文档对齐审计 F1-F8 模式（59 项双向链路实践）裁剪为两项
- 依赖: 断言延续项使用 v1.3 分型词表（同决策 1 的 D1 前置）

### 版本与提交

- 两项决策同落 SPEC_PROCESS **v1.4**（一次版本变更承载，设计 §9.1 既定）
- 提交切分: 本 ADR + SPEC_PROCESS v1.4 为一提交（设计 §9.2）

## 决策分析（依据 × 收益 × 成本）

### 0. 总览：证据强度 × 成本矩阵

| 决策 | 问题性质 | 证据强度 | 实施成本 | 不决策的代价 | 性质 |
|------|---------|---------|---------|------------|------|
| 决策1 (D4) Step 2 门禁 | checklist 无阻断力——形式化失效已三例实证 | 内部 E1 三例（pilot 拦截 / M6 全绿表演 / 本仓计数错漏网）+ 库内文献锚点 + 外部 1 篇（§3） | 低：4 条布尔判定/feature（基于已有审计结论）；v1.4 改版与 D6 摊薄 | 高且已发生：M6 单事件 = 22 测试失败 + 验收虚报 | 强制决策（教训制度化） |
| 决策2 (D6) Step 8 双向链路 | 悬空引用已双例实证 | 内部 E1 双例 + A8 规模先例（59 项） | 极低：+2 项 grep 级检查/feature；ADR 元数据表已有"相关文档"字段（零新增结构） | 累积：悬空随 ADR 数量线性增长 | 低成本补强 |

### 1. 决策1 (D4): Step 2 门禁语义

**依据（内部实证三例 + 库内文献锚点）**

- 实证一（门禁有效·首轮即拦截）：Cpp_Hub pilot R2 门禁首轮机械拦截 1/4 抽检引文失准（形态 II 转述填充）【A14，E1】——门禁不是理论构造，是首次使用即抓到真实幻觉的机制
- 实证二（checklist 失效·全绿表演）：M6"并发自查"——`Decimal.ulp` 为 3.12+ API，Step 6"版本已验证"声明失实导致 22 个测试失败；§10.1 验收统计从 pytest 总数推算，4 项零测试被虚报为 7/7 通过【SPEC_PROCESS v1.1 规则 1 背景内联，E1】
- 实证三（失效模式本仓复发）：GAP_ANALYSIS §0 计数错（12A→16A）——自查 pass 未拦截，独立 grep 重数才拦截【AUDIT P2-1，E1】。同一失效模式三周内跨两仓库复发
- 文献锚点（已在库转引，不新验）：同上下文反思式自查纠错率 <2%（arXiv:2510.08308）；LLM 自我纠错盲区率 64.5%（arXiv:2507.02778）——SPEC_PROCESS 规则 4 已内联

**关键语义区分（本决策的核心增量）**：checklist 是建议性（跳过无流程后果），门禁是阻断性（不满足不能进 Step 3）。M6 实证的失效不是"缺少检查项"——五项 checklist 全部打勾照样漏——而是"检查项无阻断力"。D4 的增量不是清单内容（Step 2 五项保留），是给审计结论加装阻断语义。

**收益**

1. 跳步路径关闭："review 全绿但断言未清零"在流程上不可达
2. 成本不对称：门禁 4 条为布尔判定，基于 Step 2 审计已有结论，边际成本分钟级；对照 M6 单事件损失（22 测试失败 + 返工 + 事后三轮元审计）
3. 与既有规则互补封边：规则 1 管"何时勾"（时序独立）、规则 4 管"谁勾的"（单视角声明）、规则 6 管"凭什么勾"（证据绑定）、D4 管"勾完能不能走"（阻断）——四个逃逸面各自封堵
4. Goodhart 防御继承：门禁约束过程与证据形态，不约束结论倾向（规则 6 执行语义警示原文适用）

**成本**

- 每 feature 边际：4 条判定（分钟级），无新增取证动作
- 结构成本：SPEC_PROCESS v1.4 一次改版（与 D6 同版摊薄）
- 依赖成本：(b) 条使用 STEP_GAP_OPEN 词表 → 框架 v1.3 先行（D1→D4 顺序已定）
- 主要风险：单人流程 skip-and-forget。缓解：4 条最小化（对齐 R4 语义不复制 R1-R3 全文）+ 失效条件登记（连续 3 feature 跳过 → 重审降级）

### 2. 决策2 (D6): Step 8 双向链路检查

**依据（悬空实证双例 + 规模先例）**

- 实证一（正向悬空）：本仓迁移即产生 ADR-0001~0003 引用悬空——f:\ 根 + Cpp_Hub + Crucix 三处零命中实证，PLAN G3 档 3 登记【E1】。"文档引用的 ADR 存在"这一正向检查靠事后专门一轮取证才发现
- 实证二（反向悬空·自指证据）：本 ADR 的诞生缺口——吸收设计 §2.2 正向引用"ADR-0008 = D4 的决策记录"，但 D6 无载体、ADR-0008 范围未声明涵盖。Step 4 Review 抓到的缺口 B 正是"正向引用存在、反向登记缺失"。**本 ADR 的 scope 修正即 D6 反向检查项的首次实际执行**
- 规模先例：Cpp_Hub 三文档对齐审计 59 项双向链路六维度 100% 对齐【A8，E1】——证明该检查在真实项目规模下可执行且有效

**收益**

1. 两项检查均 grep 级机械可执行（正/反向引用存在性），E1 可重放——与门禁同为"机械拦截优先于 LLM 自查"的形态 II 对策
2. 悬空发现时点前移：从"读者踩坑时"提前到"Step 8 门内"（ADR-0001~0003 悬空是迁移后专项审计才发现的，代价是 PLAN 专门一轮 G3 取证）
3. 断言延续项封住词表演进后的陈旧标注（v1.3 分型落地后存量文档需延续标注——本 ADR 与吸收设计自身已在消费 STEP_GAP_OPEN 新词表）

**成本**

- 每 feature 边际：+2 项 grep 检查（分钟级）
- 反向登记纪律：相关 ADR 元数据表需维护"相关文档"行——本仓 ADR 元数据表已有该字段（ADR-0006/0007/0008 均在用），零新增结构
- 心智成本："断言延续"需查询最新词表——词表封闭不变式保证查询点唯一（框架修订历史）

### 3. 外部证据补充（MCP 检索，2026-08-17）

> 检索诚实声明：`search_web` 镜像第 4 次超时（无证据采信）；`search_arxiv` 返回 6 篇，1 篇强相关、1 篇边缘（学生 checklist 教育研究，未采信）、4 篇不相关。强相关篇已做页面级复核（WebFetch abs 页，摘要逐字命中）。

**E1. arXiv 2603.03406——"Review Beats Planning"：review 门禁优于前置规划，且有效性随规格丰富度放大**

【A】(源: https://arxiv.org/abs/2603.03406v1 （Jan Miller, cs.SE, 2026-03-03，单作者预印本 10 页 + 开源代码）; 摘要引文: "When the code specialist generates freely and the reasoning model reviews instead of plans, the same two models on the same hardware achieve 90.2% pass@1" / "review effectiveness scales with specification richness, yielding 4x more improvement on richly-specified problems (+9.8pp) than on lean ones (+2.3pp)")

映射（两点）：

1. **方向佐证**：双 LLM 流水线中，"生成自由 + 事后 review 门禁"优于"前置规划约束"（plan-then-code 反而 −2.4pp）——D4 在 Step 2→3 边界安装 review 门禁而非加重前置规范，与该实证方向一致
2. **机制佐证（更重要）**：review 有效性随**规格丰富度** 4x 放大。本框架的断言分级 + 机读登记 + 取证矩阵恰是"富规格"——该实证预测 D4 门禁的回报因既有规格投资而放大（穷规格流程装门禁收益 +2.3pp 级，富规格流程 +9.8pp 级）

**权重登记**：单作者预印本、无 venue 标注——作方向/机制佐证引用，不作定量依据；实验域为代码合成（HumanEval+/MBPP+），迁移到文档审查域属类比推理（C 类判断）。

### 4. 组合效应

- D4 守 Phase 1→2 边界（调研→设计），D6 守 Phase 4 边界（文档一致性）——不同 phase 的两道门，非重叠防御
- 共享前置：两项均依赖框架 v1.3 词表（D1）→ 一次词表升级解锁两项
- 同版 v1.4 + 同提交：版本治理成本 1 次（设计 §9.1/§9.2 既定）

## 考虑的替代方案（Alternatives Considered）

### 方案 A: D4 单独成 ADR，D6 不立 ADR（吸收设计现状，否决）

- 优点: ADR 数量最少
- 缺点: D6 决策悬空——Step 8 清单变更无决策依据可溯，未来重提"为什么只有两项"无账可查
- 否决理由: 违反本仓库 ADR 使用约定（SPEC_PROCESS"与 ADR 的关系"节: 流程语义变更应记 ADR）

### 方案 B: D4/D6 各立一份 ADR（否决）

- 优点: 决策粒度最细
- 缺点: 同一版本（v1.4）的两份 ADR 同日交织，提交切分与阅读顺序复杂化；两项共享 D1 前置依赖，拆分无收益
- 否决理由: 设计 §9.1/§9.2 已裁定同版同提交，ADR 拆分与执行结构错位

### 方案 C: 复制 Cpp_Hub R1-R4 全文入 SPEC_PROCESS（否决）

- 优点: 语义完备，无裁剪损耗
- 缺点: 门禁条目膨胀（单人流程弃用风险）；R1-R3 含 Cpp_Hub 项目语境（调研任务书/spec 冻结仪式）非本仓库流程原生概念
- 否决理由: 吸收的是机制语义不是快照（设计 §7 边界情形既定）

## 后果（Consequences）

### 正面

- Step 2→3 边界获得阻断语义，"review 全绿但断言未清零"的跳步路径关闭
- Step 8 补上反向链路（ADR 登记侧）与断言状态延续两个真实失效位
- D6 决策记录闭环（缺口 B 修复）

### 负面

- 单人流程门禁弃用风险：门禁若被连续跳过将形式化（缓解: 4 条最小化 + 本 ADR 失效条件登记）
- Step 8 执行成本 +2 项/feature（可接受：均为 grep 级机械检查）

### 中性 / 后续行动

- SPEC_PROCESS v1.4 版本行与【门禁】块措辞以本 ADR accepted 版为准
- 吸收设计 §2.2 表 ADR-0008 行的范围描述需随其 P2 修正批同步为"D4+D6"（登记不执行，不并入本草案）

## 验证（Validation）

### 已有实证

| 依据 | 取证方式 | 等级 | 状态 |
|------|---------|------|------|
| R4 阻断性清零语义 | Read DEVELOPMENT_WORKFLOW §4.2 L239（过审计 A12） | E1 | ✅ |
| R 清零→冻结串联 | Read 同上 L241（过审计 A2） | E1 | ✅ |
| 双向链路实效（59 项） | Read AUDIT_CHECKLIST 对齐审计节（过审计 A8） | E1 | ✅ |
| R 门禁机械拦截实录 | Read ADR019_REVIEW_PILOT §3 L52（过审计 A14） | E1 | ✅ |
| Step 2/8 现状为 checklist 语义 | Read SPEC_PROCESS v1.3 L175-223 | E1 | ✅ |

### 验收条件（随吸收设计 §11 执行）

- SPEC_PROCESS v1.4 含【门禁】块（≤4 条）+ Step 8 清单含双向引用/断言延续两项
- grep `STEP_GAP_OPEN` 于 SPEC_PROCESS v1.4 命中（门禁 b 项 + Step 8 断言延续项）

### 失效条件（何时重审）

- 门禁 4 条连续 3 个 feature 被跳过 → 重审降级为强提醒或精简条目（90 天重审语义，学习回路独立议题）
- 框架 v1.3 分型词表若被 superseded → (b) 条与断言延续项措辞随词表同步修订

## 修订历史

| 日期 | 变更 |
|------|------|
| 2026-08-17 | 初始草案（proposed）：scope 修正为 D4+D6 双决策（Step 4 Review 缺口 B 修复），待用户确认 |
| 2026-08-17 | 补充"决策分析"节（依据 × 收益 × 成本：内部 E1 实证五例 + 库内文献锚点 + 外部 1 篇页面级复核 + 组合效应），供用户确认参考 |
| 2026-08-17 | proposed → **accepted**（用户确认 D4+D6 双决策通过）；版本 v1.0 → v1.1；depends 增补 ADR-0007（词表与载体语境）。执行序待办：框架 v1.3（D1）先行 → 本 ADR 与 SPEC_PROCESS v1.4 同提交落地 |
