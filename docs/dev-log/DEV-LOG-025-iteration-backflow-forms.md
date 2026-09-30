# DEV-LOG-025: 迭代回写形态件（四元登记块 + 决策矩阵模板 + 净收敛纪律）

> **日期**: 2026-09-30（回补）
> **会话**: `specwf-p058-20260930.jsonl`（`tools/spec_runner/sessions/`，五步链 research → design → implement → verify → finalize）
> **涉及**: `SPEC_PROCESS.md`（v1.4 → v1.5）/ `spec/templates/DECISION_MATRIX_TEMPLATE.md`（新建）/ `spec/templates/RESEARCH_TEMPLATE.md`（§6.4）/ `spec/templates/DESIGN_TEMPLATE.md`（§11）/ `spec/iteration-backflow/`（RESEARCH + DESIGN + IMPLEMENTATION + CHECKLIST）/ `docs/PROGRESS.md`（P-058）/ `CODE_WIKI.md`（v1.99 → v1.100）/ `README.md` 与 `README.en.md`（模板计数）
> **状态**: done（**回补说明**: 本份为 2026-10-01 统一回补批产出的事后叙事，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；源中未出现的内容一律不写，无法确认处标「未核」）
> **源指针**: [PROGRESS P-058](../PROGRESS.md)、[SPEC_PROCESS 新节](../../SPEC_PROCESS.md)、[DECISION_MATRIX_TEMPLATE](../../spec/templates/DECISION_MATRIX_TEMPLATE.md)、[iteration-backflow RESEARCH](../../spec/iteration-backflow/RESEARCH.md)、[session 事件流](../../tools/spec_runner/sessions/specwf-p058-20260930.jsonl)

## 做了什么（时序）

1. **research 步**：承接 [P-042 §7.19](../../spec/project-console/RESEARCH.md) 登记的三处缺口（未决项散在散文 / 无多维度决策矩阵模板 / 无迭代收敛停止规则），先做缺口现状取证（E1）：模板系统现为 5 个文件（四件套 + ADR 模板）、`SPEC_PROCESS` v1.4 无对应节、未决项现存载体形态不统一。该轮触发条件①「用户裁决」在本批兑现。
2. **design 步**：定三件具体形态规格——件 A 四元块（字段名与顺序固定：判据 / 触发条件 / 当前倾向 / 证据等级）；件 B 独立矩阵模板（选项乘七维度，三节必填 = 矩阵本体 / 收敛出口 / Type-1/2 判定）；件 C 纪律条文（净收敛 + Type-1/2 委派 + 反模式 + 诚实边界）；落确定性量 D1~D6 与不变式 I-1~I-6。
3. **implement 步**：落地 5 处——① `SPEC_PROCESS` **v1.4 → v1.5** 新增独立节「迭代收敛与未决项登记」（置于启动新 feature 流程之后、规则登记之前，`rules` 机读块为文末最后一块，**零改动**）；② 新建 `spec/templates/DECISION_MATRIX_TEMPLATE.md`；③ RESEARCH_TEMPLATE 增 §6.4、DESIGN_TEMPLATE 增 §11（两节只引不复制）；④ 治理同步（CODE_WIKI + 双语 README 模板计数）；⑤ PROGRESS 新行 P-058（立项即登记先写 `pending`）。
4. **verify 步**：三校验器复跑（`dc_validator` 含新建模板 0 违规、`repo_stats` 0 违规且 P3 0、`m7_stats` 0 违规且零新增样本）；门禁链 `step-gate` 5/5 + `verify-anchor` 10 锚点全真实 + `step-enforce` 全 exit 0；`spec_runner selftest` 47/47 与 `console_gen --selftest` 41/41 零改动复跑一致；零代码声明核对（`scripts/` 与 `tools/` 除新增 session 外零变更）。
5. **finalize 步**：PROGRESS 行由 `pending` 回填 `done` 并写验收标准；处置记录结论——三件缺口定形落地、`ADR-0010` 三问 = Layer-0 / 用户裁决 / 副作用 0。

## 决策依据

### ① 三件为何全落 Layer-0（模板 + 纪律），且不新增 RULE 编号

承 RESEARCH 结论：三件**无需新工具**，可机械化上限仅「形态完备性」（四元齐全 / 触发条件非空 / 引用完整），**结论正确性不可机核**。故落**模板 + 纪律**，**不改任何校验器、不新增门禁、零代码**；纪律落 `SPEC_PROCESS` 新增独立节而**不新增 RULE 编号** ⇒ 不触 DC4 `rules` 机读块的命名空间扩权，**无需另立 ADR**（源见 [SPEC_PROCESS 迭代收敛与未决项登记节](../../SPEC_PROCESS.md) 的来源注）。

### ② 载体为何是「新 P 行 + 新 feature 目录」

框架级产物**不寄生** `spec/project-console`，故新立 `spec/iteration-backflow/` 四文档：RESEARCH v1.0（5A+2B+3C+2H）+ DESIGN v1.0（D1-D6 + I-1~I-6 + 四方案否决）+ IMPLEMENTATION v1.0（3A + DR-1~DR-3）+ CHECKLIST v1.0 accepting（F1~F8）。

### ③ 两模板为何「只引不复制」

守 I-2 单一权威：RESEARCH_TEMPLATE §6.4 与 DESIGN_TEMPLATE §11 仅引用 `SPEC_PROCESS` 新节，不复制条文，避免同一规则出现两处权威。

### ④ 替代方案四条全否决

方案 G（只落宪法不扩模板）/ 方案 H（并入四件套模板不新建文件）/ 方案 I（升格 RULE-7）/ 方案 J（做成 Layer-1 生成器）——否决理由留档于 DESIGN。

## 遇到的问题

- **过渡期如实登记**：立项即登记（V1a）在本批为**首个活实例**（机械边界 = P 编号 ≥ P-058）；但 `done` 尚非机器派生，现形态下人写 2 次，待 **P2b**。
- **零代码边界须机械核验**：`scripts/` 与 `tools/` 除新增 session 外零变更，作为「Layer-0」声明的证据（非仅文字声称）。

## 下一步

- **H1** 净收敛纪律有效性、**H2** 七维度矩阵诱发分析瘫痪的风险——均**待触发**（未满即不动）。
- **DC4 扩权候选未激活**（若需为纪律追加 id 与失效条件与拦截记录，须另立 ADR）。
- 其余移交指针见 PROGRESS P-058 行与 session finalize 步。