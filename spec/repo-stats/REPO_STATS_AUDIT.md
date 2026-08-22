---
id: repo-stats-AUDIT
type: design
version: 1.0
status: in-review
date: 2026-08-22
depends: [repo-stats-CHECKLIST, repo-stats-IMPLEMENTATION, DIS-010]
upstream: null
---

# repo_stats 收口批独立审查记录（P-014 收口轮 review + 入账裁决）

> **审查对象**: P-014 收口轮的收口批交付物——[PROGRESS P-014 行](../../docs/PROGRESS.md)（done）、[REPO_STATS_CHECKLIST.md](./REPO_STATS_CHECKLIST.md) v1.1（accepting·有条件通过）、[DEV-LOG-006](../../docs/dev-log/DEV-LOG-006-repo-stats-implementation.md)、[DIS-010](../../docs/discoveries/README.md)（toolized）、[CODE_WIKI](../../CODE_WIKI.md) v1.7.1（§10 stats 块 + §9 索引）
> **审查类型**: 收口批数字链条自洽性审查（R7 机械重数对账 + 逐位点 Read 取证），非重构实现审计
> **审查者**: 本会话 GLM-5.3（`同基座独立审查`，**RULE-1 时序独立满足**——新会话与收口轮分离；**RULE-5 异质性未满足**——与被审对象同基座 GLM-5.3，如实降级标注，同样本⑦「同基座复验降级」形态）
> **核心原则执行**: 不信任收口批自带数字——全部独立 Read/Grep 重验，未复用收口轮记忆；审查结束后对审查建议自身再次做「排除幻觉」事实核查（A 类断言逐条重 Read 钉证据）

---

## 0. 审查范围与方法

**范围**: 收口批中全部可机械重数的数字断言——M7 hits 块（samples/form2_total/form2_by_field/findings）、M7 §2 分桶表（40 处口径）、PROGRESS P-014 行与 DIS-010/DEV-LOG-006/RESEARCH 的「实证度词 + 计数 + 占比」三元组、CODE_WIKI §10 stats 块声明值、facade_baseline 快照值。

**方法**（规则 6 取证矩阵约束）:
1. **数字链条重数**: 样本行数、分桶小计、七字段求和、findings 各级计数逐一重算，与 hits 块声明对账
2. **跨载体三元组对账**: 「实证度词（八/九度）× 视图层处数（33/40）× 占比（62%/66%）」在四文件（RESEARCH/DIS-010/DEV-LOG-006/PROGRESS）间的交叉一致性
3. **级联成本实测**: 入账后 pct 取整（floor）实算 + PT-9/PT-10 命中位点枚举 + 视图载体与真值源边界判定（RE_VIEW_CARRIER）
4. **排除幻觉核查**: 对审查建议自身的每个事实断言重新 Read 原文，区分「已实证 / 曾推断现已钉实 / 仍留未读」

**扫描范围声明（E4 语义）**: 本审查只对「可机械重数的数字断言」负责；收口批的代码正确性（repo_stats.py 实现）已有 selftest 23/23 与四通道终验背书，不在本审查范围（那是 P-014 独立 pass 的对象）。

---

## 1. 审查发现（1 P3）

### 1.1 发现: PROGRESS P-014 行「八度实证」计数词停旧

[PROGRESS.md L23](../../docs/PROGRESS.md) P-014 行「依据」列写有「八度实证」，但该行其余字段（40 处占 66%、样本㉑、㉑ 收口时点）全部是收口时点值——「八度」停在立项时点。

### 1.2 证据链（四文件「度词 × 处数 × 占比」三元组对账）

| 文件 | 行 | 原文（可 grep 引文） | 三元组 | 时点评判 |
|------|----|--------------------|--------|---------|
| [REPO_STATS_RESEARCH.md](./REPO_STATS_RESEARCH.md) | L17 | 「八度实证——视图层 33 处占形态 II 总量 62%」 | 八度 / 33 / 62% | **立项时点，正确** |
| [discoveries/README.md](../../docs/discoveries/README.md) | L26 | 「九度实证（…⑰⑱⑲⑳㉑…），视图层合计 40 处占形态 II 总量 66%」 | 九度 / 40 / 66% | **收口时点，正确** |
| [DEV-LOG-006](../../docs/dev-log/DEV-LOG-006-repo-stats-implementation.md) | L19 | 「DIS-010 → toolized（九度实证/七入载体/40 处占 66%）」 | 九度 / 40 / 66% | **正确** |
| [PROGRESS.md](../../docs/PROGRESS.md) | L23 | 「（八度实证——…40 处占…66%…㉑ 收口时点；立项时点 33 处/62%）」 | **八度** / 40 / 66% | **停旧值 ✗** |

**判定**: PROGRESS L23 的「八度」应随收口推进为「九度」。行内已并列标注「立项时点 33/62%」作区分，却独漏了「八度」本身的推进——计数词停旧，形态 II 计数桶字段错值。

**性质**: 位于 repo_stats 机械对账边界之外——「N 度实证」无任何 PT 模式覆盖（[CODE_WIKI §10 patterns L688-L708](../../CODE_WIKI.md) PT-1~PT-11 全部有锚定短语，无一匹配「度」），verify 四通道全绿无法捕获它（前轮终验全绿为真，但零问题结论不成立）。

### 1.3 级联事实（入账后的真值漂移，实测）

- 载体边界已实证：[repo_stats.py L57](../../scripts/repo_stats.py) `RE_VIEW_CARRIER = CODE_WIKI|README|evidence\.svg`——PROGRESS 非视图载体，`view_layer_total` 40 不变
- pct 公式已实证：[repo_stats.py L134](../../scripts/repo_stats.py) `floor(100 × total / form2_total)`——40/61 → floor(65.57) = **65**
- 位点已枚举：living 位点 = [CODE_WIKI L3/L67/L599/L651](../../CODE_WIKI.md)「①-㉑ / 60 处」+ [discoveries L26](../../docs/discoveries/README.md)「66%」（PT-10）；facade 位点 = [stats 块 L730-732](../../CODE_WIKI.md) `hits.samples:21 / hits.form2_total:60`

---

## 2. 入账裁决（三选项 + 推荐 A）

### 2.1 三选项

| 选项 | 内容 | 先例形态 |
|------|------|---------|
| **A 新样本㉒** | M7 §1 加行 + §2 分桶行 + hits 重生成 + 视图同步 | ⑯ / ⑰-⑳ 形态 |
| **B 并入㉑ 追记** | ㉑ 行追加注记，不拆新样本 | 追加队列 L21 追记形态 |
| **C 仅修正不入账** | 改 PROGRESS + CHECKLIST §8.2 注记，hits 不动 | 追加队列「收尾复核再修正」形态 |

### 2.2 判例法判别器（M7 五类先例提炼）

> **入账（新样本）⟺ 形态 II 字段错值复发 ∧（轮次分离 ∨ 新失效机制变体）**
> 同轮自查执行遗漏 → 注记；非形态 II 域捕获 → 追记。

本案三条件全中: ① 计数词停旧是标准形态 II 计数桶字段错值（⑪ 已有 PROGRESS 同载体先例）② 产出轮（收口轮 12f）≠ 捕获轮（本轮用户指令 review）③ 含新机制内容（见 §2.4）。

### 2.3 B/C 否决理由

- **B 被 ㉑ 自身裁决注否决**: [CHECKLIST §5](../../CODE_WIKI.md) ㉑ 合并成立条件 =「无独立审查轮 + 同轮首跑机械捕获」，本案逐项取反（有独立 review 轮 + 工具零覆盖零拦截）；且把 review 捕获写进工具捕获样本 = 污染 M7 审查配置列（对比臂分组变量）
- **C 造成会计口径分裂**: ⑰-㉑ 同 feature 逐轮全入账，本案入账方保持口径一致；且删除 P-014 效果评估的边界捕获观测值（见 §2.4）

### 2.4 A 的独立论证（对比臂价值）

㉒ 入账为 **repo_stats 落地后首个「工具边界外 review 臂捕获」数据点**: 「N 度」计数词无 PT 锚定覆盖，工具化当日即现模式库外复发——pattern 覆盖枚举性（非穷举性）首个 post-toolization 实证，喂给 pattern_lib_version 2 候选议程；与样本⑯（工具化前边界外）构成工具化前/后对照对，这是评估 P-014 效果的唯一持续观测方式。

### 2.5 级联成本（已实测，A 的真实代价）

与 B 等价：view_layer_total 40 不变；form2_total 60→61；pct 66→65（PT-10 位点漂移）；CODE_WIKI/门面三件「①-㉑→①-㉒ / 60→61 / 21→22」同步。B 成本相同却多付归因失真，故 B 被 cost-benefit 双重否决。

### 2.6 推荐结论

**采纳 A（新样本㉒，1 P3 + 形态 II 计数 1）**。诚实标注三点: ① 本轮 review 不构成 RULE-1+RULE-5 独立 pass（同基座，审查配置列降级标注）② 错误未流入版本历史（P-014 未 commit），pre-commit 属性如实标注，不先 commit 再捕获制造严重度 ③ 严重性定 P3（计数词描述级停旧，非 living 阻断级）。

---

## 3. 排除幻觉核查（对审查建议自身的事实核查）

审查建议（本记录 §2）在初次陈述时，部分数字断言于工具结果被 CLEARED 后按记忆重构。本核查逐条重新 Read 原文钉证据，结果如下:

| # | 断言 | 核查结果 | 证据 |
|---|------|---------|------|
| 1 | 「八度 vs 九度」不一致 | ✅ 确凿 | 四文件原文（§1.2 表） |
| 2 | pct = floor(100×total/form2_total) | ✅ | repo_stats.py L134 注释原文 |
| 3 | 40/61 → 65 | ✅ | 数学（前提 view_layer_total 不变，见 #7） |
| 4 | CODE_WIKI L3/L67/L599/L651 四「①-㉑/60 处」位点 | ✅ | grep 命中 + L67/L599/L651 Read 原文 |
| 5 | discoveries L26 含「66%」 | ✅ | L26 Read 原文 |
| 6 | 「N 度」不在模式库 | ✅（原推断，已钉实） | §10 patterns L688-L708 全表无「度」 |
| 7 | view_layer_total 40 不变（PROGRESS 非视图载体） | ✅（原推断，已钉实） | repo_stats.py L57 RE_VIEW_CARRIER |
| 8 | 样本⑦「降级标注」先例 | ✅ | M7 L17 原文 |
| 9 | 40 处 = 7 个 CODE_WIKI 分桶行求和 | ✅ | M7 §2 L51-L61，1+1+7+5+11+8+7=40 |

**审查边界提示（非缺陷）**: `RE_VIEW_CARRIER` 的 `README` 子串无词边界，理论上误匹配 `docs/discoveries/README.md`；但当前 §2 分桶表中 discoveries 从未独立成行（恒与 CODE_WIKI 联名），40 口径不受影响。属设计边界，执行 A 时无需处理。

**纪律反思**: 核查过程中再次验证样本⑯⑰ 的「教训记忆不提供免疫力」pattern——审查者在结果被 CLEARED 后凭残存印象自信断言，恰好正确属侥幸，不应成为常态。审查者自身的断言与审查对象同等受机械重数约束。

---

## 4. 取证矩阵（RULE-6 标准节）

| 取证手段（证据等级） | 覆盖项 | 结果 |
|--------------------|--------|------|
| Read 四文件原文逐行（E1） | §1.2 三元组对账 | 发现 1 项（PROGRESS 八度停旧） |
| Read M7 §1/§2/hits 块 + 手工重算（E1） | §0 数字链条 | 全部重数一致，0 违规 |
| grep patterns 全表（E1） | §1.3「N 度无 PT 覆盖」 | 确认无「度」模式 |
| Read repo_stats.py L57/L134（E1） | §1.3 级联载体边界 + pct 公式 | 确认 40 不变 + floor 公式 |
| Read 分桶表 + 求和重算（E1） | §2.5 级联成本 | 40 = 7 行求和确认，0 违规 |
| 排除幻觉核查重 Read（E1） | §3 建议自身断言 | 9 断言全实证，0 幻觉 |

> 全部结论绑定 E1 级证据（Read 原文 + 可重放算术），无 E4 盲区兜底于关键结论；零发现项已声明扫描范围（§0）。

---

## 5. 审查结论与后续行动

**结论**: 收口批存在 1 处 P3（PROGRESS P-014 行「八度实证」计数词停旧，应「九度」），性质为形态 II 计数桶复发、位于 repo_stats 机械对账边界外。入账裁决推荐 **A（新样本㉒）**，否决 B/C。

**审查状态**: `in-review`——审查已完成，但 (a) 结论待用户批准执行 A；(b) 本审查为同基座降级形态，待异基座独立 pass（真异基座优先）复核升级至 `verified` 后，A 的执行与㉒ 登记方获 RULE-1+RULE-5 双满足背书。

**后续行动（已批准 2026-08-22，八步，已全部执行完毕）**:
1. ✅ 修正 PROGRESS L23「八度 → 九度」
2. ✅ M7 §1 加㉒行 + §2 加分桶行（PROGRESS P-014 行，计数+1）+ 合计 60→61 + 规律锚点㉒注
3. ✅ `python scripts/m7_stats.py --write`（写守卫自证算术，hits 块 samples 21→22 / form2_total 60→61）
4. ✅ `python scripts/repo_stats.py` verify 首跑枚举活靶（9 P2 + 6 P3，与 §1.3 级联预测全吻合——living 停旧值族 + facade 三件快照滞后）
5. ✅ 修正 living 位点（CODE_WIKI ×4 / discoveries L26 66%→65%）→ verify exit 0
6. ✅ facade_baseline 22/61 + 门面三件同日刷新（README 双语 + evidence.svg）→ P3 提示 0
7. ✅ 追记三处（CHECKLIST §8.2 独立审查追记 / DEV-LOG-006 收口批独立审查追记节 / DIS-010 ㉒ 后注——「九度」不动、66%→65%）
8. ✅ 四通道终验全绿（repo_stats selftest 23/23 + verify 0 违规 0 P3 / m7_stats 0 违规（1 P3 = 样本③ 历史非整齐形态，预期非阻断）/ dc_validator 51 文件 0 违规（+1 = 本 AUDIT 文件入扫描面）/ pre-commit 三 hook 全 Passed）→ P-014 连同㉒ 一次 commit

> 执行期实测附注：八步执行中 dc_validator 曾捕获追记自身的 1 处断链（DEV-LOG-006 相对路径少一级上溯）——提交门禁拦截自身产出的链接错误，同轮修复后清零；形态 II 不入账（链接非计数字段，DC 契约域非形态 II 计数域）。

---

| 角色 | 签字 | 日期 |
|------|------|------|
| 审查者 | GLM-5.3（同基座独立审查，RULE-1 满足 / RULE-5 降级） | 2026-08-22 |
| 复核者 | 待异基座独立 pass | — |