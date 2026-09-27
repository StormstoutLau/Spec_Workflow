# 实施文档：回写流与多方案决策路径（P-050 后续阶段）

---
id: rework-and-decision-paths-IMPLEMENTATION
type: design
version: 1.0
status: draft
date: 2026-09-27
depends: [rework-and-decision-paths-DESIGN, rework-and-decision-paths-RESEARCH, precommit-dc-validator-DESIGN]
upstream: null
---

> **Feature**: 回写流与多方案决策路径（P-050 后续阶段）
> **创建日期**: 2026-09-27
> **状态**: draft（草稿）
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md) **v1.1**
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.4**
> **本批范围**：**交付 A 实施**（`dc_validator` M4 分支② + `CHECKLIST_TEMPLATE` §10.1 规范约束）；**交付 B 零改动**（DESIGN §7 规格，守 I-15）。

---

## 1. 实施概述

本批把 CHECKLIST 验收统计纳入 R7 射程，做法是**补一个既存机制的空位**，而非新立规则或新工具：

1. **落点**（DESIGN D-A2）：扩展 `scripts/dc_validator.py` 的 M4 `check_counting` 为双分支——分支 ① 保持 `## 0. 断言统计表`（A/B/H）逻辑**逐字不变**，分支 ② 新增 `### 10.1 验收统计`（8 类行 + 总计行）的形态判定与算术重数。
2. **规范形态**（DESIGN D-A3）：在 `spec/templates/CHECKLIST_TEMPLATE.md` §10.1 后追加规范约束说明（章节号 / 纯整数单元格 / 两条算术），**表结构零改动**。
3. **渐进**（I-13）：形态异形或缺失一律 **skip（`severity=""`）**——只提示、不阻断；历史 20/21 文件不受影响（唯一全规范的 `promptfoo-m7-eval` 自然通过）。

**零新增 hook / 零新增脚本 / 零新增依赖 / 零 API 破坏**。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|------|------|------|---------|
| 语言 | Python | 3.x（stdlib only） | ✅ 与既有三校验器同栈 |
| 依赖 | 无第三方 | — | ✅ 零新增（复用 `argparse/re/os/sys/dataclasses`） |
| 载体 | pre-commit 既有 hook `dc-validator` | — | ✅ files 已覆盖 `spec/**/*.md`，无需改 hook |

### 2.2 文件结构与改动面

| 文件 | 改动 | 行 |
|------|------|----|
| `scripts/dc_validator.py` | 新增分支②（正则 4 / 函数 4）+ `check_counting` 拆为双分支 + selftest F12-F18 | §3、§4 |
| `spec/templates/CHECKLIST_TEMPLATE.md` | §10.1 表后追加规范约束说明（2 行 blockquote） | §3.3 |
| `spec/rework-and-decision-paths/{DESIGN,IMPLEMENTATION}.md` | 本批文档 | — |

**零改动**：分支① 逻辑、`Summary` 判定语义、`.pre-commit-config.yaml`、其余校验器/脚本。

## 3. 模块实施

### 3.1 `dc_validator.py` M4 分支②

#### 职责

对形态规范的 CHECKLIST §10.1 表做**声明 = 机械重数**对账（DESIGN §4）。

#### 实施要点

- **先剥围栏**（`_strip_fences`）：文档在正文自我演示规范形态（如本 DESIGN §4.2）时，围栏内的示例标题会误触本校验——首次全量实跑即复现（DESIGN.md 自身命中），故只认正文（同 `check_links` 的 `in_fence` 处置）。
- **标题两段式判定**：`RE_CL_STAT_HEAD`（精确 `### 10.1 验收统计`）→ 走解析；未命中但 `RE_CL_STAT_ANY` 命中（如 `### 8.1 验收统计` / `### 10.1 验收统计（…）`）→ skip 提示。
- **形态门槛**：`{类别} == CL_CATEGORIES`（模板 8 类）且总计行存在，否则 skip——避免「少一类行但总计含它」造成的假 P1。
- **单元格**：`_cl_int` = 去 `*` 后 `fullmatch(\d+)` → int，否则 None；任一 None → skip（文字算术/括注）。
- **算术**：逐行 `总数 = 通过+失败+待办`；总计 = 8 类行按列求和；违者 **P1**。

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| 大文件多次整体扫描 | 单次 `_strip_fences` → 单次 `splitlines` 解析；无嵌套循环 |
| 正则回溯 | 全部锚定行首 `^`，量词为 `*`/`?`，无嵌套量词 |

### 3.2 `check_counting` 拆分为双分支

```python
def check_counting(file, text):
    """M4：R7——① §0 断言统计表（A/B/H）② CHECKLIST §10.1 验收统计（P-050 交付 A）。"""
    return _counting_assertions(file, text) + _counting_checklist(file, text)
```

- 分支① 原逻辑**逐字平移**至 `_counting_assertions`（I-14）；
- 分支② 新增 `_counting_checklist`；
- 两者**各自独立命中**，一文件可同时受两者约束。

### 3.3 `CHECKLIST_TEMPLATE.md` §10.1 规范约束

在既有表（8 类行 + 总计行，**结构不动**）之后追加：

```
> **统计口径（RULE-2）**：上表来自本文件**逐项核对**（每一项均有独立标记），非事后汇总推算。
>
> **规范形态（P-050 交付 A，由 `dc_validator` M4 分支② 机械校验）**：① 章节号固定
> `### 10.1 验收统计`（禁改号、禁标题加括注）；② 数值单元格 = **纯十进制整数**（禁
> `**N + M**` / `N 项 + M 发现` / 括注；`**N**` 加粗允许）；③ 表内两条算术必须成立——
> 逐行 `总数 = 通过 + 失败 + 待办`，总计行 = 8 类行**按列求和**。
```

## 4. 接口实施

### 4.1 `parse_checklist_stats(body) -> (rows, total)`

```python
def parse_checklist_stats(body):
    """解析 §10.1 表体（规范标题行之后）。返回 (rows, total)。"""
    rows, total, started = [], None, False
    for ln in body.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            if started:
                break
            continue
        started = True
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5:
            continue
        label = cells[0].replace("*", "").strip()
        if not label or set(label) <= set("-: "):   # 空 label / 分隔行
            continue
        vals = tuple(_cl_int(c) for c in cells[1:5])
        if label == "总计":
            total = vals
        elif label in CL_CATEGORIES:
            rows.append((label, vals))
    return rows, total
```

**签名一致性**: 与 DESIGN.md §5.1 一致 ✅

### 4.2 `_counting_checklist(file, text) -> list[CheckResult]`

判定表见 DESIGN §5.2（六种条件 → 通过 / P1 / skip / 无结果）。**签名一致性**: 与 DESIGN.md §5.2 一致 ✅

## 5. 兼容性

### 5.1 向后兼容（I-14 的机械核验）

| 项 | 处理 | 证据 |
|---|---|---|
| 分支① §0 断言统计表 | **逐字平移**，行为零变化 | selftest F4 `声明 3 实为 2` 仍 PASS |
| 历史 CHECKLIST（Phase 0 时点 21 中 20 非规范） | 一律 skip，不阻断 | 全量实跑：6 条 §10.1 skip（5 历史文件 + 模板）、零 P1/P2 |
| `Summary` 判定语义 | **不改**（异形用 `severity=""` 而非 P3，见 DESIGN §4.3 修正说明） | `--selftest` 23/23→24/24，F9 零违规仍 PASS |

### 5.2 首次全量实跑的自我命中 → 加固

初次全量运行时，**本 DESIGN.md 自身**被分支②命中（§4.2 的规范形态示例块 + §3.1 的普通小节标题 `### 3.1 验收统计形态三族与子偏差`），暴露两处**工具缺陷**（非文档缺陷）：

| 缺陷 | 根因 | 加固 |
|---|---|---|
| 围栏内示例触发 | 校验器未跳代码围栏 | `_strip_fences`（F17 回归） |
| 普通小节标题误判为异形 | `RE_CL_STAT_ANY` 过宽（`验收统计.*` 吞掉后续散文） | 收紧为 `验收统计\s*(?:[（(].*)?$`（F18 回归） |

> **这是「吃狗粮」的直接收益**：把校验器跑在自己的产出上，立刻暴露两类仅在「文档自指」场景出现的缺陷。两处均已加 fixture 锁死。

## 6. 错误处理实施

| 错误场景（来自 DESIGN §7） | 处理 | 测试 |
|--------------------------|------|------|
| 表结构不全（缺类行/总计行） | skip（`severity=""`） | F14/F15 族 |
| 单元格非纯整数 | skip（`severity=""`） | F14 |
| 总计列 ≠ 类行求和 | P1 | F13 |
| 行内 总数 ≠ 通过+失败+待办 | P1 | F13b |
| 无 §10.1 / 围栏内示例 / 普通小节标题 | 无结果 | F16 / F17 / F18 |
| 文件不可读 | P2（既有 M1 逻辑，未改） | F7 |

## 7. 不变式实施

| 不变式（来自 DESIGN §8） | 实施位置 | 验证方式 |
|---|---|---|
| I-11 规范即自洽 | `_counting_checklist` 两条算术 | F12（自洽零违规）/ F13 / F13b |
| I-12 R7 位点单一宿主 | 唯一实现于 `dc_validator` M4；`repo_stats`/新脚本零复制 | 改动面表（§2.2）+ 全文 grep |
| I-13 渐进不追溯 | 异形/缺失 → `severity=""` | F14 / F15 + 全量实跑零 P1/P2 |
| I-14 分支互不干扰 | `check_counting` 两段求和 | F4（分支①）与 F12-F18（分支②）并存 PASS |
| I-15 交付 B 零运行时足迹 | `dc_validator` 词表零改动 | F3b/F3c 仍 PASS（词表未动） |

## 8. 测试策略

### 8.1 内嵌自测（`--selftest`）

| 模块 | fixture | 断言数 | 结果 |
|------|---------|--------|------|
| M4 分支②（P-050） | F12 / F13 / F13b / F14 / F15 / F16 / F17 / F18 | 8 | ✅ |
| 既有（F1-F11c） | — | 16 | ✅ 零破坏 |
| **合计** | — | **24** | **24/24 PASS** |

### 8.2 全量实跑

`python scripts/dc_validator.py` → **123 文件 / 25 结果 / 0 违规**（结果 = **19 条「范围外 skip」**（无 front-matter 载体）+ **6 条 §10.1 skip**（5 历史异形文件 + `CHECKLIST_TEMPLATE` 占位））。新 CHECKLIST **未入 skip 列表** ⇒ 其 §10.1 通过本校验（自我样本）。

### 8.3 属性/边界

边界由 fixture 覆盖：规范+自洽、规范+两种算术错、规范+非整数、异形标题、无标题、围栏内示例、普通小节标题。**未做**属性测试（单文件线性解析，无组合状态）。

## 9. 幻觉抑制审查（Step 6 Review）

### 9.1 依赖版本验证

- [x] 无新增第三方依赖（DESIGN §10.1 约束 4；全程 stdlib）；
- [x] 无虚构 API/函数——全部复用 `dc_validator` 既有 `CheckResult` / `_read` / import。

### 9.2 接口签名验证

- [x] `parse_checklist_stats` / `_counting_checklist` 与 DESIGN §5 一致；
- [x] 签名可实现（已实现并 selftest 通过）。

### 9.3 实施与设计对齐

- [x] 每个模块对应 DESIGN §3.2 的一个模块（分支② / 模板约束）；
- [x] 每个接口对应 DESIGN §5 的一个接口；
- [x] **无设计未覆盖的实施**；
- [x] 交付 B **零实施**（I-15）。

### 9.4 低效操作排除

- [x] 无 O(n²)（单遍线性解析）；
- [x] 无不必要 I/O；
- [x] 无重复计算（`_strip_fences` 每次调用一次）。

## 10. 实施步骤（实录）

| # | 步骤 | 结果 |
|---|---|---|
| 1 | `dc_validator.py` 增正则 + `_strip_fences` / `_cl_int` / `parse_checklist_stats` | ✅ |
| 2 | `check_counting` 拆为 `_counting_assertions`（逐字平移）+ `_counting_checklist`（新） | ✅ |
| 3 | `CHECKLIST_TEMPLATE.md` §10.1 追加规范约束 | ✅ |
| 4 | selftest 增 F12-F15 → 22/22 | ✅ |
| 5 | **首跑全量暴露两处工具缺陷**（围栏 / 过宽正则）→ 加固 + F17/F18 | ✅ |
| 6 | 复跑 `--selftest` 24/24 + 全量 123 文件 0 违规 | ✅ |

**实施期发现（DR 登记）**：

| # | 发现 | 处置 |
|---|---|---|
| **DR-A1** | `dc_validator.Summary` 把非空 severity（含 P3）全算违规，与 `repo_stats` 的 P3 语义**相反** | 设计中即改用 `severity=""`（DESIGN §4.3 修正说明）；P3 语义统一另立观察项 |
| **DR-A2** | 文档自我演示规范形态会误触本校验（围栏未跳） | `_strip_fences` + F17 |
| **DR-A3** | `RE_CL_STAT_ANY` 过宽，吞掉普通小节标题 | 收紧正则 + F18 |

---

**Review 签字**: _________ 日期: _________
