---
id: academic-writing-workflow-ACADEMIC_REASONING_CONSTRAINTS
type: framework
version: 1.0
status: active
date: 2026-10-21
depends: [academic-writing-workflow-ACADEMIC_FILE_SPEC, academic-writing-workflow-RESEARCH, stage-tooling-contract-RESEARCH]
upstream: academic-writing-workflow-ACADEMIC_FILE_SPEC
---

# 学术推理任务的附加约束（八条）

> **定位**: 学术域 **reference / what 层**（Diátaxis，同 [ACADEMIC_FILE_SPEC](ACADEMIC_FILE_SPEC.md) §定位）：回答「学术推理产出什么算合规」，不回答「今天先做哪一行」（执行卡负责）。本文件是八条的**唯一权威载体**；其他文档只许引用，不得复制（守 ACADEMIC_FILE_SPEC §0 不变量 I「一份真值」）。
> **适用范围**: `spec/academic-writing-workflow/` 及跨仓学术执行卡。**纯工程批**可选用第 1 / 5 / 8 条，其余不适用。
> **边界**: 只约束**形态**，不承诺可机械检出，也不承诺质量；不新增门禁、不新增依赖。质量仍由 Review / ADD / 用户裁决承担。
> **依据**: 外部读数见 [stage-tooling-contract RESEARCH v1.1](../stage-tooling-contract/RESEARCH.md) §4.3–§4.5（U-2 已核，T1 定位）；本文件不新增 A/B/C 断言。

## 0. 为什么独立成文（U-3 裁决）

- 此前八条同时存在于 `SPEC_PROCESS` 与 `stage-tooling-contract/RESEARCH`，形成双副本；P-115 订正后两份出现 3 处漂移（适用范围 / 第 6 条精度 / TDD 依据读数）。
- 学术域已有独立的 reference 层（[ACADEMIC_FILE_SPEC](ACADEMIC_FILE_SPEC.md)）；八条属于同一层，移入独立文档后可被跨仓执行卡**引用而非复制**。
- 外部同构：TOP Guidelines / PRISMA 均为独立标准，由使用方按引用采纳，而非各自内嵌（E2 官方页）。

## 1. 八条

1. **主张—证据绑定**：每条实质主张后跟「来源 ID + 定位（页 / 节 / 定理号）」；无定位的主张降级为「推测」。
2. **区分探索与确证**：探索性发现（exploratory）与确证性结论（confirmatory）不得混写；确证须写**样本量 / 口径 / 判定规则**。
3. **禁止「研究表明」**：无引用不得使用该措辞；有引用按 [ASSERTION_EVIDENCE_FRAMEWORK](../../docs/ASSERTION_EVIDENCE_FRAMEWORK.md) 与引用核验四步处理。
4. **统计口径前置**：估计量、样本、缺失处理、显著性阈值写在结论之前，而不是附录。
5. **反例义务**：每个模型 / 方法结论至少给一个失效条件（否则视为未完成）。
6. **多模型共识只作过滤**：**>3** 模型一致可降低引用幻觉（[RESEARCH §4.4](../stage-tooling-contract/RESEARCH.md)），但**不作为证据强度**。
7. **形式化优先**：能写成定义 / 命题 / 反例的，不写成散文。
8. **执行面隔离**：跨仓只读、只登记快照指针，**不复制真值**（承 P-104 纪律）。

## 2. 与现有文档的关系

| 文档 | 分工 | 本文件如何被使用 |
|---|---|---|
| [SPEC_PROCESS](../../SPEC_PROCESS.md) | 通用流程宪法（十步 / RULE / 批次档位） | 只留指针；不复制八条 |
| [ACADEMIC_FILE_SPEC](ACADEMIC_FILE_SPEC.md) | 论文仓静态合规（六轴 / 三不变量） | 并列引用；文件规范管「文件怎么放」，本文件管「推理怎么写」 |
| [ACADEMIC_S3_RUN_CARD](ACADEMIC_S3_RUN_CARD.md) | S3 运行口径（怎么跑、什么算过） | 运行卡引用本文件；不复制 |
| [RESEARCH v1.1](../stage-tooling-contract/RESEARCH.md) | 调研 provenance（外部读数 / U-2 核验） | 只引用 §4.3–§4.5；不复制断言 |

## 3. 边界与非目标

- 不是门禁：不接入 `dc_validator` / `m7_stats` / `repo_stats` / pre-commit；违反只影响**证据可复核性**。
- 不是执行卡：不回答「今天先做哪一行」；执行顺序见 S3 运行卡与学术任务卡。
- 不是质量保证：满足八条仍可能得出错误结论；质量靠 Review、ADD 与用户裁决。
- 不新增断言：本文件不引入 A/B/C/H 编号；外部读数一律回溯到 RESEARCH v1.1 与 M7 账本。

## 4. 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0 | 2026-10-21 | 初版：八条从 SPEC_PROCESS / stage-tooling-contract RESEARCH 移出，成为学术域唯一权威载体；修正第 6 条为「>3」；明确适用范围（纯工程批可选 1 / 5 / 8）；U-3 闭合。 |
