# 设计文档：回写返工图（分叉关联登记 + 触发条件 + 只读对账）

---

id: rework-graph-DESIGN
type: design
version: 1.1
status: in-review
date: 2026-09-27
depends: [rework-graph-RESEARCH, ADR-0010]
upstream: null
---

> **Feature**: 回写返工图（rework graph）
> **创建日期**: 2026-09-27
> **状态**: 评审中（v1.0 首版，含 §9 Step 4 同基座自审）
> **Spec 步骤**: Step 3-4
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.1**（16A+5B+4C+3H）
> **本批范围**: 用户裁决「走路径 A 实施」——**路径 A = 外部登记表 + 只读对账器**（`fork` 零改动）。
> **v1.1 变更（2026-09-27，Step 8 独立审查整改）**：Step 8 独立审查（**同基座降级**）**6 项发现（3 P2 + 3 P3）全部整改**——本文件内 3 项：**P2-2** §4.4-B8 原写「六种缺」而口径与 RPC 不一致 ⇒ 改**枚举化**并标明本仓 **7 类** / RPC **8 类**；**P3-3** §4.4-A2 只写「为空」而「含重复项」分散在 §5.2 ⇒ A2 补**「或含重复项」**（判据单点化）；**P2-1** 相关：判定表**总条数**本文件未声明（声明落在 CHECKLIST/CODE_WIKI/PROGRESS），此处不改。**判定表实现零改动**（`check()` 已逐条覆盖 19 条）。**设计本体零变动**（仅订正计数口径与判据单点化）。

---

## 1. 设计目标

把「回写流完整形态」的**两件缺失物**落地为**可复算的登记与对账**：

1. **原/新流关联登记**（返工图）——让「谁 fork 了谁、从第几步、因何触发」成为**一等真值表**；
2. **触发条件**——把触发原因做成**封闭枚举**（只定形状，不替治理定值）；
3. **只读对账器**——把「登记表」（声明）与「实际 session 文件」（事实）机械对账。

一句话：**不新建原语、不改 `fork`、不接门禁**——只补「一张表 + 一个只读对账器」。

## 2. 设计依据

| 调研发现 | 设计决策 | 引用 |
|---|---|---|
| 完整形态三件 = 分叉原语 ✅ / 关联登记 ❌ / 触发条件 ❌ | **D1**：本批只做缺的两件；**不碰 `fork`**（守 I-4） | RESEARCH B1 |
| RPC `edges.yaml` 边强制 `provenance: <前缀>:<载荷>` + 双封闭枚举 + 「缺」判无效（**免计数枚举**：RPC 口径 **8 类** / 本仓 **7 类**） | **D2**：登记表每条 fork 亦强制 `provenance`，前缀取封闭集 | RESEARCH A-7/A-8/A-9 |
| RPC `cap_state` 三值 / `on_exceed_kind` 四值封闭枚举（**数值可 undecided**） | **D3**：`trigger_kinds` 取**封闭枚举**且含 `undecided` | RESEARCH A-10/A-11 |
| 本仓无 `inventory/`；非 `.md` 不在 DC 契约范围 | **D4**：数据落 `docs/rework-graph.json`（不新增顶层概念、无 front-matter 义务；**JSON 守 stdlib**） | RESEARCH A-6/A-15 |
| 本仓既有「独立只读检查器不接门禁」先例 | **D5**：本轮**不接门禁**；接门禁登记为触发驱动观察项 | RESEARCH A-14 |
| sessions 目录存在 `vN` 后缀多流（**非** fork，系直接新建） | **D6**：**命名后缀不承担 lineage 语义**；`docs/rework-graph.json` 是 lineage **唯一真值源**（守 I-5） | RESEARCH A-5 |

## 3. 现状诊断

### 3.1 缺口（RESEARCH A-1~A-4）

`fork` 是唯一能产出新事件流的命令，但**只把 `new <- session` 打到 stdout**（`spec_runner.py` L505-506），事件 schema 亦无 lineage 字段 ⇒ 分叉事实**只存在于操作者的记忆与终端历史里**。

### 3.2 关键机械信号（本设计得以成立的支点）

**`fork` 复制行时**逐字复制原行——**包括 `session` 字段**。故：

> **一个 session 文件，若其行内 `session` 值 ≠ 该文件名词干 ⇒ 它就是一次 `fork` 的输出。**

该信号**完全机械、零新增契约**（不需给 `fork` 加字段）。本仓当前实测命中 **1 例**：`p009-first-run-001-fork-demo`（携带 `session = p009-first-run-001`，1 行）【E1，2026-09-27 扫描】。

## 4. 架构设计

### 4.1 数据载体：`docs/rework-graph.json`

**JSON 而非 YAML**：本仓自有脚本守 **stdlib only**（D6），YAML 需 PyYAML（外部依赖）⇒ 违规；且本仓既有机读声明块（CODE_WIKI 的 `stats` 块 / M7 的 `hits` 块）**同为 JSON**。RPC 侧用 YAML 是其环境选择——**可搬的是「独立真值表文件」这个形态，不是文件格式**。

```json
{
  "version": 1,
  "updated": "<date>",
  "owner": "<name>",
  "truth_source": "registry",
  "trigger_kinds": ["<封闭枚举，非空无重复>"],
  "provenance_prefixes": ["<封闭枚举，非空无重复>"],
  "forks": [
    {"new": "<新流名>", "origin": "<源流名>", "seq_from": 1,
     "trigger_kind": "<∈ trigger_kinds>", "reason": "<非空，禁 unknown>",
     "provenance": "<前缀>:<载荷>", "date": "<YYYY-MM-DD>"}
  ],
  "non_rework": [
    {"name": "<fork 输出但非返工>", "why": "<非空，禁 unknown>", "date": "<YYYY-MM-DD>"}
  ]
}
```

> `forks` **空也必须显式写 `[]`**（守 I-7）；`truth_source` 恒 `registry`（守 I-5）；`updated` 仅记录、**不参与判定**（守 I-2）。
> `non_rework` = **「是 fork 输出、但不构成返工」的显式豁免**（如能力演示）——承 RPC「**不适用也要写下来**」纪律（否则 §4.4-D17 的孤儿扫描会把它们误报为漏登）。

**封闭枚举取值（v1，形状承 RPC，**值**为本仓自定且可扩张）**：

- `trigger_kinds`：`upstream-overturned`（上游结论被推翻）/ `verify-failed`（机械校验失败不可原地修补）/ `scope-change`（范围变更）/ `user-verdict`（用户显式裁决）/ `undecided`（未裁——**合法状态**，不得省略）。
- `provenance_prefixes`：`manual`（人工操作）/ `tool`（工具产出）/ `filetrack`（文件级追踪）/ `hash`（内容寻址）。

### 4.2 对账器：`scripts/rework_graph_check.py`（只读）

三段式（承 RPC `id_storage_census` 范式）：

1. **声明**：读 `docs/rework-graph.json`；
2. **实测**：扫 `tools/spec_runner/sessions/*.jsonl`（每个文件的首行 `session` 值 + 行数 + 前 N 行内容）；
3. **对账**：按 §4.4 判定表逐条判；**只写 stdout**（守 I-1）。

### 4.3 判定与退出码

| exit | 含义 |
|---|---|
| 0 | 登记表自洽 **且** 与实测一致（含孤儿扫描为空） |
| 1 | 硬性不一致（判定表任一命中） |
| 2 | 降级：数据文件缺失/不可解析（**不当作通过**） |

### 4.4 判定表（「缺」的形态穷举——逐条判红）

**A 表结构**
1. `forks` 字段**缺失** ⇒ 判红（**无法区分「清单为空」与「忘了写」**——空必须显式）
2. `trigger_kinds` / `provenance_prefixes` 为空**或含重复项** ⇒ 判红（无封闭集可判 / 封闭集自身不洁）
3. `truth_source` 不等于 `registry` ⇒ 判红（真值源未声明为本表）
3b. `non_rework` 字段**缺失** ⇒ 判红（同 1 的理由）；其条目缺 `name`/`why`，或 `why` 为空/仅空白/`unknown` ⇒ 判红

**B 边自洽**
4. `new` / `origin` 缺、空串或仅空白 ⇒ 判红
5. `new == origin` ⇒ 判红（自环不是返工）
6. `new` 重复登记 ⇒ 判红
7. `trigger_kind` ∉ `trigger_kinds` ⇒ 判红
8. `provenance` **各类「缺」全判红**（本仓 `_prov_bad` 覆盖 **7 类**：非字符串 / 空串 / 仅含空白 / 命中禁用词 `unknown` / 缺 `<前缀>:<载荷>` 形式 / 前缀 ∉ `provenance_prefixes` / 载荷为空；承 RPC A-9 口径——RPC 侧另有「字段不存在」一类，共 **8 类**）
9. `reason` 空、仅空白或 `unknown` ⇒ 判红
10. `seq_from` 非正整数 ⇒ 判红

**C 声明 → 事实对账**
11. `origin` session 文件**不存在** ⇒ 判红
12. `new` session 文件**不存在** ⇒ 判红
13. `rows(new) ≠ seq_from` ⇒ 判红（`fork` 恰复制 `seq ≤ seq_from` 的行）
14. `rows(origin) < seq_from` ⇒ 判红
15. `new` 的前 `seq_from` 行 ≠ `origin` 的前 `seq_from` 行（逐行 JSON 相等）⇒ 判红
16. `new` 行内携带的 `session` 值 ≠ 登记的 `origin` ⇒ 判红

**D 孤儿扫描（反向）**
17. `sessions/*.jsonl` 中存在 fork 输出（首行 `session` ≠ 名词干）但**既未登记为任何 `new`、也不在 `non_rework`** ⇒ 判红（漏登即漂移）
18. `non_rework` 的 `name` 在 sessions 中**不存在**或**不是 fork 输出** ⇒ 判红（豁免也不能凭空写）

### 4.5 真值源裁定（D6）

- **`docs/rework-graph.json` = lineage 唯一真值源**；
- session 文件名的 `vN` 后缀**只是便利命名，不构成 lineage 声明**（实测其多数并非 `fork` 产物——先把旧名改成别的是另一件事，本批不动历史文件名）；
- 若将来要「文件的 `vN` 也参与 lineage」，须先改本表 `truth_source` 并补对账规则（**不得两个定义点并存**）。

## 5. 接口定义

### 5.1 CLI

```
python scripts/rework_graph_check.py            # 默认 = check（对账）
python scripts/rework_graph_check.py --json     # 机读输出
python scripts/rework_graph_check.py --selftest # 内嵌自测（合成 fixture，零依赖真表）
```

### 5.2 数据 schema 字段

| 字段 | 类型 | 必填 | 语义 |
|---|---|---|---|
| `version` | int | 是 | 表格式版本 |
| `updated` | str | 是 | 最后更新日（**仅记录，不参与判定**——守 I-2 确定性） |
| `owner` | str | 是 | 责任人 |
| `truth_source` | str | 是 | 恒 `registry` |
| `trigger_kinds` | list[str] | 是 | 封闭枚举（非空、无重复） |
| `provenance_prefixes` | list[str] | 是 | 封闭枚举（非空、无重复） |
| `forks` | list[map] | 是 | 边集；可为 `[]`（**必须显式**） |
| `forks[].new` | str | 是 | 新流名（不含 `.jsonl`） |
| `forks[].origin` | str | 是 | 源流名 |
| `forks[].seq_from` | int | 是 | 分叉点 `N`（`fork --seq N`） |
| `forks[].trigger_kind` | str | 是 | ∈ `trigger_kinds` |
| `forks[].reason` | str | 是 | 非空，禁 `unknown` |
| `forks[].provenance` | str | 是 | `<前缀>:<载荷>` |
| `forks[].date` | str | 是 | `YYYY-MM-DD` |
| `non_rework` | list[map] | 是 | **fork 输出但非返工**的显式豁免；可为 `[]`（**必须显式**） |
| `non_rework[].name` | str | 是 | 会话名（须**确为** fork 输出，否则判红） |
| `non_rework[].why` | str | 是 | 非空，禁 `unknown` |
| `non_rework[].date` | str | 是 | `YYYY-MM-DD` |

## 6. 替代方案

| 方案 | 内容 | 结论 |
|---|---|---|
| **A（选择）** | 外部登记表 + 只读对账器 | **采纳**——`fork` 零改动、零新依赖、零门禁面 |
| B | **流内自带关联**：`fork` 在新流首行写 `forked_from` 事件 | **否决**——动**唯一写入原语** + 事件 schema 属 **Layer-0 契约变更**；且与"薄壳 runner 不膨胀"取向冲突。关联「随流走」是它的唯一优点，可由对账器（§4.2 三段式）弥补 |
| C | **扩展 `repo_stats.py` 承载** | **否决**——`repo_stats` 的语义 = **视图层声明对账**（R7 同构）；返工图不是视图层对象，塞进去会污染其 pattern 库与定位 |
| D | **新建顶层 `inventory/`** | **否决**——为一个文件新增顶层概念；`docs/` 已是数据落脚地（M7 账本/CODE_WIKI stats） |
| E | **接为第 6 hook（提交即拦）** | **本轮否决、登记触发驱动**——先有真实数据（当前仅 1 例）再谈强制；承 `downstream_compliance.py` 先例（守 I-6） |

## 7. 边界声明

1. **登记表是清单，不是事实**（RPC 原话）——对账器只保证「**已登记的分叉属实**」，**不保证「所有分叉都已登记」**；后者靠 §4.4-D17 的孤儿扫描**尽可能**兜（能兜住的仅「fork 输出」一类真凭据）。
2. **触发条件的「值」未裁**——本设计只立**形状**（封闭枚举 + 必居其一）；具体什么条件触发回写是**治理决定**（RPC 同款；见 RESEARCH H2）。
3. **不保证分叉的「必要性」**——登记不评价「该不该回写」，只记录「发生了回写」。
4. **不追溯历史**——除首条真实分叉（§3.2）外，不为历史 `vN` 会话补登记（它们多数**不是** fork 产物）。
5. **对账器不接门禁** ⇒ 它是**纪律的执行者**而非**纪律的强制者**（RPC 的「软约束」警告在此**已知并接受**，接门禁见方案 E）。

## 8. 不变式（Invariants）

- **I-1 只读**：对账器不写任何 session / 表 / 派生视图（只 stdout）。
- **I-2 确定性**：不读 wall clock；同输入 → 同输出（`updated` 字段不参与判定）。
- **I-3 零依赖**：stdlib only（`yaml` 不可用 ⇒ 用极简行式解析或改用 JSON；实现见 IMPLEMENTATION）。
- **I-4 `fork` 语义零改动**：本批不碰 `tools/spec_runner/`。
- **I-5 单一真值源**：lineage 只由本表声明；命名后缀不承担该语义。
- **I-6 不新增门禁**：本轮不接 hook（接门禁为触发驱动观察项）。
- **I-7 缺失显式**：空 `forks` 必须写出；不可区分「空」与「忘写」者一律判红。

## 9. 幻觉抑制审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

§2 六条决策逐条挂 RESEARCH A/B 锚点（见表格「引用」列），无悬空决策。

### 9.2 替代方案审查

§6 五个方案均给出**否决理由**（B/C/D/E），且 B/E 的**唯一优点**已指明（随流走 / 强约束）及其替代补偿路径。

### 9.3 职责边界审查

§7 五条边界中，第 1、5 条为**关键诚实声明**（清单≠事实、软约束已知并接受）——防止把「对账器」读成「保证无漏登」。

### 9.4 同基座自审（RULE-5 降级标注）

本表的 §4.4 判定表与 §3.2 支点均经 `fork` 源码（L487-507）+ sessions 实扫复核；**异基座独立 pass 未执行**（RULE-5 未达成，如实降级）。

## 10. 对实施的输入

1. **数据文件**：`docs/rework-graph.json`（§5.2 schema；首版 **`forks: []`**——**本仓至今尚无一次真实的「返工回写」**——+ 1 条 `non_rework` 豁免 = P-009 的 `fork` 能力演示）。
2. **对账器**：`scripts/rework_graph_check.py`（§4.2 三段式 + §4.4 判定表 + `--selftest`）。
3. **禁止项**：不碰 `fork`（I-4）；不接 hook（I-6）；不追溯历史（§7-4）。
4. **登记项**：把「是否接门禁」登记为**触发驱动观察项**（触发 = 真实分叉数 ≥3 或 用户裁决）。
