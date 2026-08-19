# ADR-0004: 采纳外部对标结论——对抗审查异质性约束与测试隔离四要素

---
id: ADR-0004
type: adr
version: 1.0
status: accepted
date: 2026-08-01
depends: [SPEC-PROCESS, ADR-0001, ADR-0002, ADR-0003]
upstream: null
---

## 元数据

| 字段 | 值 |
|------|-----|
| 编号 | ADR-0004 |
| 日期 | 2026-08-01 |
| 状态 | 接受 |
| 决策者 | Scott (鹏) + Claude GLM-5.2 |
| 相关文档 | [META_AUDIT_EXTERNAL_BENCHMARK.md]（[外部·未随迁]）、[META_AUDIT_IMPROVEMENT_REPORT.md]（[外部·未随迁]）、[ADR-0003]（[外部·未随迁]，三处零命中实证 2026-08-16）、[SPEC_PROCESS.md](../SPEC_PROCESS.md) |
| 取代 | 无（扩展 ADR-0003 后的流程决策，不取代任何 ADR） |

## 背景（Context）

> **编号说明**: 下文 L1-L4 / S1-S5 为[外部·未随迁]元审计改进报告的建议编号体系（L=流程层 / S=统计层），仅本背景节引用；与 SPEC_PROCESS 的 Step 1-10 及本仓 RULE/M 编号无关联。

[META_AUDIT_IMPROVEMENT_REPORT.md]（[外部·未随迁]） 提出 N/S/L 三级改进建议后，[META_AUDIT_EXTERNAL_BENCHMARK.md]（[外部·未随迁]） 对其执行了外部对标审查（7 次检索、10 组文献交叉验证）。三条关键结论要求修订原建议：

1. **L1（对抗式审查 Agent）面临 MAD 文献清算风险**：2025 年系统性实证（arXiv:2502.08788, ICLR 2025；arXiv:2311.17371, ICML 2024）表明同质 Multi-Agent Debate 在 36 个实验场景中对简单 CoT 的胜率无一个超过 20%，消耗 3-5x token；When Debate Fails（2025）报告辩论使模型 33% 更可能强化偏见，且存在 answer corruption（弱 agent 的自信错误带偏强 agent）。幸存区间仅限：**异质角色 + 可验证对象 + 反驳导向**。
2. **S2（skip 审计）落后于业界 test quarantine pattern**：业界方案多三要素——Owner（责任人）、Deadline（30 天修复或删除）、Re-qualification（重新上岗需证明稳定性），且隔离 ≠ 跳过（降权运行而非停跑）。"skip-and-forget" 是公认反模式。
3. **S3/L4（验收映射）自研了半个轮子**：DO-178C §5.5.e 的 RTM（Requirements Traceability Matrix）要求**双向**追溯——不仅"每个需求有测试"（forward），还要"每个测试有需求依据"（backward）；且 **derived requirements（派生需求）必须单独标识与验证**。

## 决策（Decision）

我们决定**选择性吸收**外部对标结论，对原建议体系做 5 项修订：

### 1. L1 追加两条强制约束（异质性 + 单向权限）

- **(a) 异质性要求**：对抗式审查的 reviewer 与 implementer 必须使用**异构基座**（不同模型家族）。依据：同基座新会话只消除记忆污染（Self-Correction Blind Spot, arXiv:2507.02778），不消除同分布盲区；MAD 文献表明模型异质性（heterogeneity）才是增益主源（Heter-MAD）。
- **(b) 单向权限**：reviewer 输出只进入 dev-log 作为标记项，**永不直接改写实现**。依据：防 answer corruption 的流程层版本——自信但错误的批评不得腐蚀正确实现（与 ADD skill"永不自动修复"原则同构）。
- L1 前置条件由"S1 试点验证有效"升级为"**S1 试点 + 异质性对比数据支持**"（S1 试点需对比"同基座新会话 vs 异基座新会话"的检出率差）。

### 2. S2 升级为测试隔离（quarantine）四要素

skip 审计升级为：**Owner**（每个隔离测试有责任人）+ **Deadline**（隔离超 30 天必须修复或删除，无例外）+ **降权运行**（隔离 ≠ 跳过——仍每次运行、仍记录结果，只是不阻塞验收）+ **Re-qualification**（重新上岗需证明稳定性，单次通过不够）。现有条件 skip 测试改造为"无条件运行 + 结果记录"。

### 3. S3 增加反向追溯链（RTM backward traceability）

验收映射脚本的"存在但未被任何验收行引用的测试"告警从 P3（提示）升为 **P1**——未被引用 = 验收表不完整（DO-178C backward 语义：每个测试必须有需求依据）。

### 4. 新增 S5：派生需求登记（derived requirements）

实施中产生、但未在 DESIGN 显式声明的每个设计决策（如 StubLLMClient 评分规则、判定容差 `_EPS=1e-9` 的选择），登记为 derived-requirement 并单独验收。取代 CHECKLIST §1 中"无设计未覆盖的实施"的人工判断。

### 5. L2 补充 equivalent mutant 排除与增量策略

- 增量 mutation：只 mutate 本 feature 变更行（Stryker `--mutate path:L1-L2` 语义；Google IEEE TSE 2022 同向实践）。
- **equivalent mutant 排除**：抽查中 survived 的变异不必然指向测试弱——需先排除行为等价变异（不可杀死且不计分），否则产生假警报。

## 考虑的替代方案（Alternatives Considered）

### 替代方案 A: 维持原建议不变（否决）

- 优点：无需返工
- 缺点：L1 大概率落入已被文献清算的"昂贵集成"陷阱（同质辩论 ≈ 3-5x 成本的 Self-Consistency）；S2 的 skip-and-forget 风险已被业界证实
- 否决理由：有外部证据却不修正 = 重演 M1（自查确认偏差）——本 ADR 的存在意义就是不让元审计建议自身成为新的盲区

### 替代方案 B: 完整引入 DO-178C 级 RTM 工具链与流程（否决）

- 优点：标准成熟、认证级严谨
- 缺点：DAL A/B 级的独立性要求、MC/DC 覆盖、工具鉴定对单人+Agent 项目过重；我们是研究原型而非适航软件
- 否决理由：吸收**语义**（双向追溯、派生需求登记、独立验证分级思想）而非**形式**（认证文书）。按 DO-178C 分级类推：本项目自评约 DAL C-E 级，采用与其风险相称的子集

### 替代方案 C: 选择性吸收（选择）

- 优点：每项吸收都有文献/标准/工业实证背书；成本近零（模板与规则改动）；保留原创部分（L3 review 覆盖率指标无直接对标，保留并标注原创性）
- 缺点：异质性约束在单用户订阅条件下有执行成本（需 ≥2 个不同基座的模型访问）

## 后果（Consequences）

### 正面

- L1 从"合理推测"变为"文献幸存区间内的受约束设计"，规避已知的 answer corruption 与昂贵集成陷阱
- S2 获得业经验证的防 skip-and-forget 机制；隔离测试从"消失"变为"降权可见"
- S3/S5 补上验收映射的反向盲区与派生决策盲区——元审计发现的 M2 模式（统计推算）在两个方向都被封堵
- 所有修订有可引用的外部依据（arXiv / IEEE TSE / DO-178C / 业界实践），不再是自我循环论证

### 负面

- 异质性约束要求访问 ≥2 个模型家族，增加 S1 试点的执行成本与复杂度
- Deadline（30 天）引入时间管理负担；单人项目需自律执行
- 派生需求登记增加每个 feature 的文书开销

### 中性 / 需要后续行动

- SPEC_PROCESS 升级 v1.2（本 ADR 的规则落地）
- M7 启动时 S1 试点须设计异质性对比组
- L3（review 覆盖率指标）保留原创，标注"无外部对标，置信度自负"

## 验证（Validation）

### 文献验证（对标报告 §6 已执行，2026-08-01）

| 依据 | 来源 | 状态 |
|------|------|------|
| MAD 胜率 <20% / 3-5x token | arXiv:2502.08788 + ICLR 2025 blog 双源交叉 | ✅ |
| 偏见强化 33% / answer corruption | When Debate Fails（2025-03，二手转述，标注 ⚠️） | ⚠️ 转述 |
| 异质性为增益主源（Heter-MAD） | arXiv:2502.08788 原文 | ✅ |
| Self-Correction Blind Spot 64.5% / fresh context 有效 | arXiv:2507.02778 原文 | ✅ |
| DO-178C §5.5.e 双向追溯 / derived requirements / §6.3 独立验证 | LDRA + Jama + RTMify 三源交叉 | ✅ |
| quarantine 四要素（owner/deadline/re-qualify/降权运行） | deflaky.com + pie.inc（行业实践类） | ✅ |
| Google 增量 mutation / mutant 选择 | IEEE TSE 2022 官方页 | ✅ |

### 待验证项（移交 S1 试点）

- 异构基座 reviewer 在本项目 spec 文档上的实际检出率增益（对比同基座新会话）
- quarantine 四要素在单人+Agent 工作流中的执行摩擦
- derived-requirement 登记的实际文书成本

### 失效条件（何时重审本 ADR）

- 若 S1 试点显示异构 reviewer 检出率与同基座无显著差异 → 放宽约束 (a)
- 若 quarantine Deadline 在研究节奏下不可执行 → 调整期限而非删除要素
- 若 MAD 文献后续被推翻（新的大规模实证支持同质辩论）→ 重审约束 (a)

## 修订历史

| 日期 | 变更 |
|------|------|
| 2026-08-01 | 初始版本 |
