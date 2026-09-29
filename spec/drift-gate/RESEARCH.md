# 调研文档：drift-gate / 意图图-证据图概念吸收（Layer-0 概念登记）

---
id: drift-gate-RESEARCH
type: design
version: 1.1
status: draft
date: 2026-09-29
depends: [community-ecosystem-RESEARCH, ADR-0010, SPEC-PROCESS]
upstream: null
---

> **Feature**: drift-gate / 意图图-证据图概念吸收（PROGRESS P-023——Layer-0 概念登记，作为 repo_stats 演进候选）
> **创建日期**: 2026-09-09
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「针对 drift-gate / 意图图-证据图概念吸收任务进行吃狗粮测试 按照 spec 工作流开始 运行到懒加载 gate 部分即可」——吃狗粮立项，走到 ADR-0010 懒加载 gate 三问判定处驻留（不实施 repo_stats 演进本身）。
>
> **v1.1 变更（2026-09-29，P-052 落档批）**: 用户指令「先落档 细化调研待裁定事项 给出证据支持的确定结论」+「把『front-matter 状态 vs PROGRESS 声称』的一致性问题登记为一个观察项」——新增 **§4.4 补充登记**（3 处状态漂移的机械复核结论 + 2 项新增发现 + 观察项登记 + 本批已执行处置）。**零新增外部断言**（全 E1 本仓机械取证）；**零 drift-gate 实现改动**（DC2 判别规则扩宽落在既存工具 `dc_validator`，非本 feature 交付，见 §4.4.3）。

---

## 1. 调研目标

**核心问题**（概念吸收登记型调研，非新外部调研）：

1. SGE 的「意图图（Intent Graph） vs 证据图（Evidence Graph）双图校验」思想，与本仓 repo_stats「声明=重数」对账制的同构关系与可迁移点在哪？
2. 作为概念吸收，应登记为何种形态、放哪一层（ADR-0010 Q1），边界在哪（吸收思想 vs 引入实现）？
3. 未激活副作用是否为 0（ADR-0010 Q3），激活条件是什么（Q2）？

> **调研边界说明**：本 feature 的素材已在 [COMMUNITY_ECOSYSTEM_RESEARCH.md](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md)（CER）v1.1~v1.7 中完整取证并稳定核验（SGE 双图校验为 CER 最强同构点且 v1.5 确认「无新信息，arXiv 稳定」）。本调研**不重复外部 WebSearch**，仅对既有 CER 资产做内聚性整理 + 登记级论证（复用式调研，贴合吃狗粮零新增外部断言纪律）。全部事实锚点指回 CER 的 E1/E4 证据。

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| Grep/Read | 既有 CER 资产内聚提取（SGE 双图校验 / repo_stats 对账 / ADR-0010 三问门禁） | `drift` / `意图` / `repo_stats` / `分层归属` |
| Read | repo_stats 校验器现状与 CODE_WIKI §10 stats 块位点核对 | 声明=重数说明 / declared / doc_registry |

### 2.2 调研范围

- **复用来源**: CER v1.7（26A+3B+13C+4H，含 SGE 逐条取证 + §3.4 分层归属列 + §3.4.1 深入建议）
- **不做**: 新增外部事实断言（A/B 类）——避免 R7 重数与 CER 漂移；SGE 双图校验事实以 CER 为准（v1.5 已核验 arXiv:2606.27045 稳定）

## 3. 调研发现

### 3.1 SGE 双图校验的既有取证（复用 CER）

【C】**同构关系已由 CER 确立**——SGE（Spec Growth Engine，arXiv:2606.27045）的 **drift gate（spec-code 漂移阻塞合并）+ 意图图 vs 证据图双图校验** 与本仓对账制同构。

- **最强同构点**：CER §2.1 判定「repo_stats 对账制（声明=重数）≙ SGE 意图图 vs 证据图双图校验」为**最强同构点**——双图校验 = 对账的思想泛化。【依据：https://arxiv.org/html/2606.27045v1 §2；CER §2.1 表】
- **漂移断言同构**：SGE 的两个结构失效模式（context explosion / silent spec-code drift「代码演化、spec 不演化」）与 DIS-009/010 观察的本仓「文档-实际漂移」同构。【依据：CER A-16；DIS-009/010】
- **分层归属预演**：CER v1.3 §3.4 补「分层归属（ADR-0010 Q1）」列已预演 **drift-gate = Layer-0**（概念吸收，仅登记 repo_stats 演进候选）。【依据：CER v1.3；ADR-0010 v1.4 修订历史】
- **深入建议**：CER §3.4.1 结论「登记候选（Layer-0）不变——repo_stats 演进候选（意图→证据→缺口闭环）。下一步 = 无（仅登记）。」【依据：CER §3.4.1】

### 3.2 repo_stats 现状（基准位点）

【C】**repo_stats 目前是「声明=重数」单向对账**：定义 = 机械真值枚举 + 声明侧（declared）逐键比对，**文档侧声明 ← 机械重数**（单向）。它回答「声明数量是否 = 机械数出的实际数量」。双图校验思想把它扩展为**闭环**表述：【依据：CODE_WIKI §10；scripts/repo_stats.py；PROGRESS P-014】

- 「**意图**」（文档侧声明/作者期望的契约）
- →「**证据**」（机械重数/实际枚举值）
- →「**缺口报告**」（void 缺口 analysis：意图与证据之差 = 缺口/漂移，可阻塞）

这使对账从「数是否对得上」（布尔通过/失败）升级为「差在哪、差多少、是否该阻塞」（带定位信息的缺口报告）。

### 3.3 ADR-0010 三问门禁的适用前提（本 feature 立项即被测对象）

【C】**懒加载门禁适用对象 = 候选吸收物**（本 feature 的 drift-gate 概念登记即候选吸收物的一种——Layer-0 概念）；调研报告本体（CER）不过门禁（ADR-0010 边界声明）。本 feature 直接以自身为被测对象吃狗粮（同 P-020/P-021 先例）。【依据：ADR-0010 边界声明】关联 pattern_lib_version 2 候选议程（P-014 立）。

## 4. 综合分析

### 4.1 关键发现总结

1. SGE 意图图 vs 证据图双图校验是本仓 repo_stats 对账制的**思想泛化与闭环表达**，迁移点为「意图→证据→缺口」三环节。【置信度: ★★★★★（CER §2.1 最强同构点 + 源码/摘要双取证）】
2. 概念吸收 = **仅登记、不引实现**：把该思想登记为 repo_stats 演进候选（关联 pattern_lib_version 2），不实现 drift gate、不建双图运行时、不引外部依赖。【置信度: ★★★★★（CER §3.1 C 区明确「零成本，仅登记」）】
3. 分层归属 = **Layer-0**（概念/方法论思想，无运行时）；激活条件 = **触发驱动**（pattern_lib_version 2 演进候选，无触发不实现）；未激活副作用 = **0**（不实现即不存在）。【置信度: ★★★★★（CER v1.3 预演 + ADR-0010 三问语义）】
4. 与 ADR 三层 / Ponytail 7 级阶梯同属「工具可拒、思想可留」的 Layer-0 概念族（ADR-0010 连锁否决辨析先例）。【置信度: ★★★★☆（ADR-0010 梳理红线）】

### 4.2 技术 landscape

概念吸收位点集中在**机械对账的语义升级**：repo_stats 现有「声明=重数」是计数级对账；双图校验思想指向**语义/意图级对账**（文档意图 vs 机械证据的缺口定位）。本仓 M7 形态 II 复发跟踪 + 视图层对账制已占据「计数一致性」位点，缺口报告思想是下一级演进候选（不发散、不立项——仅登记）。

### 4.3 研究空白（登记级）

- repo_stats 的 `void` 缺口报告能力（定位「哪个声明与真值不符」而非仅「总数不符」）——**尚未实现，登记为演进候选**，激活条件 = pattern_lib_version 2 候选议程触发（P-014 立）。
- 本批不实施（用户指定走到懒加载 gate 驻留），实施面细节（缺口报告 schema/exit-code 语义）留待激活时 DESIGN。

### 4.4 补充登记（P-052 批次，2026-09-29）：制品状态与声称的「一致性」无机械看护

> **触发** = 用户指令「先对那 3 处状态漂移跑一次机械复核，帮我判断以谁为准」→「先落档 细化调研待裁定事项 给出证据支持的确定结论」+「把『front-matter 状态 vs PROGRESS 声称』的一致性问题登记为一个观察项」。**零新增外部断言**（全 E1 本仓机械取证）。

#### 4.4.1 机械复核结论（待裁定事项 → 确定结论）

| # | 待裁定事项 | 机械取证（E1） | 确定结论 |
|---|-----------|---------------|---------|
| 1 | [step-gate/CHECKLIST_FUNC.md](../step-gate/CHECKLIST_FUNC.md) front-matter `v1.0/draft` vs [PROGRESS P-020](../../docs/PROGRESS.md)「CHECKLIST_FUNC v1.1 accepting 12/12」 | 该文件 §8 修订历史**自身**记「v1.0 → v1.1：状态 draft → accepting」；PROGRESS + CODE_WIKI §2.1/§9 三方一致 | **以 PROGRESS / CODE_WIKI 为准**（制品 front-matter 落后 = 回写欠账） |
| 2 | [defect-fixes/CHECKLIST_FUNC.md](../defect-fixes/CHECKLIST_FUNC.md) `v1.0/draft` vs PROGRESS P-022「CHECKLIST_FUNC v1.0 accepting 13/13」 | §7 独立 pass 已签字「通过（accepted）」；PROGRESS + CODE_WIKI 一致（该文件 §8 缺 promotion 行） | 同上 |
| 3 | [independent-verify/CHECKLIST.md](../independent-verify/CHECKLIST.md) `v1.0/pending` vs PROGRESS P-025「CHECKLIST v1.0 accepting」 | 正文 C1-C9 全 ✅ + 验收记录闭环；PROGRESS + CODE_WIKI 一致 | 同上 |
| 4 | independent-verify 的 [DESIGN](../independent-verify/DESIGN.md) / [RESEARCH](../independent-verify/RESEARCH.md) `draft` vs 同 feature [CHECKLIST C8](../independent-verify/CHECKLIST.md) 声称「DESIGN v1.0 → verified；RESEARCH v1.0 → verified」 | C8 单方自证；仓内惯例（feature 收束转 verified，如 defect-fixes DESIGN v1.2 verified） | **以 C8 声称 + 仓内惯例为准** → `verified` |
| 5 | PROGRESS P-025 声称 `spec_runner.py v1.4.0` vs 代码 [`VERSION`](../../tools/spec_runner/spec_runner.py) 常量 | `--version` 实测 = **1.3.0**；`git log -S 'VERSION = "1.4.0"'` **零命中**（P-025 提交 `ef8733f` 时即为 1.3.0） | **以代码为准**（1.4.0 从未存在）→ 订正 P-025 声明 |

**第 1/2 项根因（本批新发现，DC 契约层）**：两份 id = `step-gate-CHECKLIST-FUNC` / `defect-fixes-CHECKLIST-FUNC`，**不以 `-CHECKLIST` 结尾** ⇒ `dc_validator` M2 的 DC2 副轴判别（`id.endswith("-CHECKLIST")`）将其归为**「一般设计文档」**，其词表 `draft/in-review/verified/superseded` **无 `accepting`** ⇒ 独立 pass 后的状态回写**机械不可表达**（写入即报 P1）。**故二者长期停 `draft` 非疏忽，是被判别规则挡住**——这本身是一处「规则文本 < 实际语义」的边界缺口。

#### 4.4.2 观察项登记：「制品 front-matter 状态 vs PROGRESS 声称」一致性无机械看护

- **（一）登记缘由（E1）** = 本批机械复核（§4.4.1）——3 处 CHECKLIST + 1 处 DESIGN/RESEARCH 的 front-matter 状态与 PROGRESS 声称**不一致**，而三校验器**全绿**（`dc_validator` 只校验 `status ∈ 词表`；`repo_stats` drift-gate 只比 **version** 不比 **status**、且仅覆盖 `doc_registry` **已登记**制品；两份 `CHECKLIST_FUNC` **未登记** ⇒ 完全逃逸）。**无任何机械看护。**
- **（二）机制定性** = **看护缺口（管辖空白），非工具 bug**。三者合力：① `dc_validator` M2 管「状态是否合法」不管「状态是否与外部声称一致」；② `repo_stats` drift-gate 管「意图（§9 版本）↔ 证据（front-matter 版本）」不管 status、且只对 registered doc；③ `doc_registry` 每个 feature 只登记 1 份代表文档 ⇒ 同 feature 的 CHECKLIST/RESEARCH 常在覆盖面外。
- **（三）同族登记** = 同一「**声明 ≠ 实物/重数**」族的又一显形位点：[P-042 §7.11](../project-console/RESEARCH.md)（无决策事件的文档订正轮 ⇒ 控制台不可见，**视图层**显形位点）+ [rework-and-decision-paths §3.8.3](../rework-and-decision-paths/RESEARCH.md)（CHECKLIST 条目级状态无机械重数）+ **DIS-010**（[discoveries](../../docs/discoveries/README.md)，视图层计数漂移 = 真值源的「无失效检测缓存副本」）+ P-050 v1.2 P2-1 / **M7 样本 ㉛**（[M7 账本](../../docs/M7_EVIDENCE_LOG.md)，事件流 ≠ 文档最终状态）+ **本批新证**（[precommit-dc-validator IMPLEMENTATION §8.1](../precommit-dc-validator/IMPLEMENTATION.md) fixture 表声明 F1-F10 而代码实为 F1-F21——同类「声明未随实物更新」）。
- **（四）触发条件（任一即重审）** = ① 同类复现 **≥1 例**（本批已 4 例，达阈值）② 出现**由本缺口导致的误判**（据落后状态做错裁决或对外陈述）③ 用户显式裁决。
- **（五）载体预判（均须先过 ADR-0010 三问）** = **方向 A（Layer-1，候选）** = 把「front-matter `status` 与 PROGRESS 声称 一致性」纳入 `repo_stats` drift-gate（现只比 version 不比 status；扩到 status + 覆盖非 registered 制品）；**方向 B（Layer-0，纪律）** = 补一条弱纪律「制品状态变更须同步 front-matter，且与 PROGRESS / CODE_WIKI 声称一致」。**预登记否决** = 不在 `dc_validator` 内解析 PROGRESS（跨契约耦合，撞 **I-10** 语义同源）。
- **（六）未触发处置** = 维持现状；本批已把**可机械化的那一半**落地（DC2 判别规则扩宽 + 回写，见 §4.4.3）；**不新增门禁 / 不改 `console_gen` / 不新增校验器**。
- **（七）边界声明** = 只登记观测、触发条件与载体预判，**不实施方向 A/B 任何机制**。

#### 4.4.3 本批已执行处置（用户裁决「扩宽 DC2 判别规则」+「全部执行」）

1. **DC2 判别规则扩宽**（`dc_validator` M2）：`id.endswith("-CHECKLIST")` → `"CHECKLIST" in id.split("-")`——覆盖 `-CHECKLIST-<变体>`；selftest **24/24 → 27/27**（F19 段判别 `accepting` 合法 / F20 段判别 `draft` 非法 / F21 段判别**非子串**）；契约文本同步 [doc-contract PLAN §1 DC2 v1.7](../doc-contract/PLAN.md)。
2. **5 处 front-matter 回写**：step-gate/CHECKLIST_FUNC（v1.0/draft → **v1.1/accepting**）/ defect-fixes/CHECKLIST_FUNC（draft → **accepting**）/ independent-verify/CHECKLIST（pending → **accepting**）/ independent-verify/DESIGN 与 RESEARCH（draft → **verified**）。
3. **PROGRESS P-025 版本声称订正**：`v1.4.0` → **v1.3.0**（附机械取证注）。
4. **视图层同步**：CODE_WIKI（§2.1 树 / §9 / 版本头）。

## 5. 幻觉抑制审查（Step 2 Review）

### 5.1 文献验证

| 引用 | 验证方式 | 状态 |
|------|---------|------|
| SGE（arXiv:2606.27045）意图图 vs 证据图双图校验 | CER v1.1 六轮 WebSearch 取证 + v1.5 快照核验（arXiv 稳定）| ✅（复用 CER，不重复取证）|
| DIS-009/010 文档-实际漂移 | 本仓 discoveries 索引 | ✅ |

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| repo_stats 为单向「声明=重数」对账 | scripts/repo_stats.py + CODE_WIKI §10（P-014） | ✅ 已验证 |
| drift-gate 分层 = Layer-0 | CER v1.3 §3.4 分层归属列预演 | ✅ 已验证 |

### 5.3 待修正项

- 无（概念登记型调研，零新增断言，不引入外部新事实）。

## 6. 对设计的输入

### 6.1 可用的技术方案

- 概念登记形态 = 在本 feature DESIGN 中将 SGE 双图校验思想落为「repo_stats 演进候选（意图→证据→缺口闭环）」结构化登记，锚 CER 位点。

### 6.2 关键约束

1. **零实现**：不写 drift gate、不建双图运行时、不改 repo_stats.py（本批止于懒加载 gate，不实施）。
2. **零新增外部断言**：全部锚回 CER E1/E4，避免 R7 漂移。
3. **单向依赖**：登记文档依赖 CER/ADR-0010；文档层绝不反向依赖本 feature。

### 6.3 风险

- 概念登记可能被误读为「已立项演进」——须在 DESIGN 中显式标注「仅登记、触发驱动、未激活副作用 0」（ADR-0010 纪律）。
- 「意图图-证据图」术语与 SGE 原意过度绑定——登记时明确本仓取其**闭环对账思想**，非其图数据库实现。

## 7. 参考文献

- COMMUNITY_ECOSYSTEM_RESEARCH.md v1.7（SGE 取证 + §3.4 分层 + §3.4.1 建议）
- SPEC_PROCESS.md v1.4（10 步 Spec 流程）
- ADR-0010-lazy-loading-architecture-gate.md v1.4（三问门禁）
- docs/PROGRESS.md（P-014 repo_stats / P-023 本批）
- CODE_WIKI.md §10 stats 块（declared / doc_registry / pattern_lib）

---

**Review 签字**: _________ 日期: _________