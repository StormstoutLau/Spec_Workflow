# 实施文档：回写返工图（分叉关联登记 + 触发条件 + 只读对账）

---

id: rework-graph-IMPLEMENTATION
type: design
version: 1.1
status: draft
date: 2026-09-27
depends: [rework-graph-DESIGN, rework-graph-RESEARCH]
upstream: null
---

> **Feature**: 回写返工图（rework graph）
> **创建日期**: 2026-09-27
> **状态**: draft（草稿）
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md) **v1.1**
> **基于调研**: [RESEARCH.md](./RESEARCH.md) **v1.1**
> **v1.1 变更（2026-09-27，Step 8 独立审查整改）**：Step 8 独立审查（**同基座降级**）**6 项发现（3 P2 + 3 P3）全部整改**——本文件内 4 项：**P2-1** 判定表**总条数**由「18」订正为 **19**（A1~A3b = 4 / B4~B10 = 7 / C11~C16 = 6 / D17~D18 = 2），§1/§3 同步；**P2-3** §4 的 I-1 措辞「全文无 write」**不实**（脚本 L242 在 `_selftest` 内写 `tempfile` fixture）⇒ 改「**对仓库零写入**（唯一写点在 selftest 的临时目录）」，且 §6 的验证命令 `rg` 参数由转义误用（`\|` 在 ripgrep 中非 alternation）**订正为正确形式**并补「唯一写点为 selftest tempfile」；**P3-1** 增长型载体计数漂移：§5/§6 的 `sessions=48` → **49**（本批自身 session `specwf-p051-20260927.jsonl` 落地所致，如实标注）；**P3-2** §3 映射表**补 B4 与 C14 两行**（原漏，致「逐条」过度声明）+ **selftest 补 F29/F30 两 fixture** ⇒ **28/28 → 30/30 PASS**（脚本 351 → **358** 行）。**交付物本体语义零变动**（判定表实现与数据结构未改，仅补 fixture 与订正计数/证据）。

---

## 1. 交付清单

| # | 文件 | 行数 | 性质 | 说明 |
|---|---|---|---|---|
| 1 | `docs/rework-graph.json` | 27 | **新增**数据 | 返工图真值源（`forks: []` + 1 条 `non_rework` 豁免） |
| 2 | `scripts/rework_graph_check.py` | 358 | **新增**脚本 | 三段式对账器（**对仓库只读**，stdlib only；含 `--selftest` **30 项**） |

**零改动**：`tools/spec_runner/`（守 I-4）；`.pre-commit-config.yaml`（守 I-6，本轮不接门禁）；三校验器；既有 5 个 hook。

## 2. 接口签名

### 2.1 CLI（对 DESIGN §5.1）

```
python scripts/rework_graph_check.py            # 默认 = check（exit 0/1/2）
python scripts/rework_graph_check.py --json     # 机读输出（追加一行 JSON）
python scripts/rework_graph_check.py --selftest # 内嵌自测（合成 fixture，不读真表）
```

### 2.2 内部函数（对 DESIGN §4.2 三段式）

| 函数 | 签名 | 职责 |
|---|---|---|
| `_s(v)` / `_blank(v)` | `(Any) -> str / bool` | 归一化 / 「空·仅空白·禁用词」三态判定 |
| `_prov_bad(prov, prefixes)` | `(Any, list) -> str \| None` | `provenance` **7 类「缺」**判定（承 RPC A-9；免计数枚举口径，与 DESIGN §4.4-B8 一致） |
| `scan(dir)` | `(Path) -> dict` | **实测**：`stem → {rows, first_session, head}`；不可解析记 `error` |
| `fork_outputs(sessions)` | `(dict) -> set` | **关键信号**：行内 `session` ≠ 文件名 stem |
| `check(reg, sessions)` | `(Any, dict) -> (list, list)` | **判定表**（DESIGN §4.4 A/B/C/D），**纯函数** |

## 3. 实施记录（逐条对 DESIGN §4.4）

| DESIGN 判定表 | 实现位点 | 自测 |
|---|---|---|
| A1 `forks` 缺 ⇒ 红 | `check()` `REQ_KEYS` 循环 | F02 |
| A3b `non_rework` 缺 ⇒ 红 | 同上 | F03 |
| A3 `truth_source ≠ registry` | `check()` | F04 |
| A2 两个封闭集为空/重复 | `check()` | F05 / F06 |
| B4 `new`/`origin` 缺或空 | `check()` | F29 |
| B5 `new == origin` | `check()` | F08 |
| B6 `new` 重复 | `seen_new` | F17 |
| B7 `trigger_kind` ∉ 集 | `check()` | F07 |
| B8 `provenance` 七类「缺」 | `_prov_bad()` | F11-F16 |
| B9 `reason` 空/禁用词 | `_blank()` | F09 |
| B10 `seq_from` 非正整数 | `check()` | F10 |
| C11/C12 会话不存在 | `check()` | F18 / F19 |
| C13 `rows(new) ≠ seq_from` | `check()` | F20 |
| C14 `rows(origin) < seq_from` | `check()` | F30 |
| C15 前 N 行不等 | `dn["head"][:sf] != do["head"][:sf]` | F21 |
| C16 new 携带 `session` ≠ origin | `first_session` | F22 |
| D17 孤儿未登记 | `fork_outputs() - registered` | F23 |
| D18 `non_rework` 凭空写 | `check()` | F24 / F25 / F26 |

**实施期发现（DR）**：

- **DR-1（关键信号获证）**：设计假设「`fork` 复制行保留源 `session` 字段」在实施前**已实证**——`p009-first-run-001-fork-demo.jsonl` 首行 `session = p009-first-run-001`（全仓扫描**仅此 1 例** fork 输出）。该信号使「孤儿扫描」（D17）成立，且**零新增契约**。
- **DR-2（`non_rework` 的由来）**：初稿只设计 `forks`，实施时发现**存在「是 fork 输出但不构成返工」的一类**（P-009 能力演示）⇒ 若无豁免位，D17 会把能力演示**误报为漏登**。故补 `non_rework`（承 RPC「不适用也要写下来」纪律）。**这是设计缺陷在实施期被捕获并修复**，DESIGN 已同步（§4.1/§4.4-A3b/§4.4-D17/D18/§5.2）。
- **DR-3（载体格式改判）**：DESIGN 初稿写 YAML；实施时据 **I-3（stdlib only）** 改判为 **JSON**（YAML 需 PyYAML = 外部依赖）⇒ DESIGN §4.1/§2-D4/§4.2/§4.5/§10.1 + RESEARCH §6.1 同步订正为 `docs/rework-graph.json`。

## 4. 不变式实施（对 DESIGN §8）

| 不变式 | 实施位点 | 验证 |
|---|---|---|
| **I-1 对仓库只读** | 无任何写入**仓库路径**的调用；唯一写点在 `_selftest()` 的 `tempfile` fixture | 源码 grep（§6，含 selftest 写点说明） |
| **I-2 确定性** | 不 import `time`/`datetime`；`updated` 不进 `check()`；`sorted()` 遍历 | 同输入双跑字节一致（§6） |
| **I-3 零依赖** | import 仅 `argparse/json/sys/pathlib`（+ selftest 内 `tempfile/shutil`） | §6 grep |
| **I-4 `fork` 零改动** | 未触碰 `tools/spec_runner/` | `git status`（§6） |
| **I-5 单一真值源** | `truth_source` 必须为 `registry`（A3 判红兜底） | F04 |
| **I-6 不新增门禁** | 未改 `.pre-commit-config.yaml` | §6 |
| **I-7 缺失显式** | `forks`/`non_rework` 缺 ⇒ 判红（A1/A3b） | F02 / F03 |

## 5. 测试策略

- **内嵌自测 `--selftest` = 30 项**（F01-F30）：正例 3（F01/F27/F28）+ 反例 27，**合成 fixture**（`tempfile` 建临时 sessions 目录）⇒ **不读真表、不写仓库**（守 I-1；且真表内容漂移不影响判据自测）。
- **真实仓首跑**（E2；**读数时点 = 本批 session 落地后**）：`[登记] forks=0 · non_rework=1 · trigger_kinds=[upstream-overturned, verify-failed, scope-change, user-verdict, undecided]（5 值封闭集，stdout 打印为值列表非计数）· truth_source=registry` / `[实测] sessions=49 · fork 输出=1（p009-first-run-001-fork-demo）` ⇒ **`[PASS]` exit 0**。
- **离线可正反夹测**：`check()` 为纯函数（只吃 `(reg, sessions)`）⇒ 无需真实仓即可夹测全部判定表。

## 6. 验证实录（Step 6）

| 验证 | 命令 | 结果 |
|---|---|---|
| 自测 | `python scripts/rework_graph_check.py --selftest` | **30/30 PASS** |
| 真实仓 | `python scripts/rework_graph_check.py` | **PASS**（exit 0；`sessions=49` / `fork 输出=1`） |
| 对仓库只读 | `rg -n -e 'write_text' -e "open\(.*'w'" scripts/rework_graph_check.py` | 命中 **1 处**（`_selftest` 的 `tempfile` fixture，L242）⇒ **仓库路径零写入** |
| 零依赖 | 源码 import 清单 | `argparse/json/sys/pathlib`（+ selftest `tempfile/shutil`） |
| 确定性 | 双跑比对 stdout | 一致（无 wall clock） |
| `fork` 零改动 | `git status tools/spec_runner/` | 仅 `sessions/` 有本批外新增（P-050 ⑩ 批 v9 + 本批 p051），**无 runner 源码改动** |

## 7. 兼容性

| 项 | 说明 |
|---|---|
| Python | 3.9+（只用 `pathlib` / `json` / `argparse` / `from __future__ import annotations`） |
| OS | Windows / Linux 均可（路径由 `pathlib` 处理） |
| 外部依赖 | **零**（不引入 PyYAML / 任何第三方包） |

## 8. 错误处理

| 场景 | 行为 |
|---|---|
| 登记表缺失 | `[FAIL] 登记表缺失` ⇒ **exit 2**（降级，**不当作通过**） |
| 登记表不可解析 | `[FAIL] 登记表不可解析: <异常>` ⇒ **exit 2** |
| 某 session 文件不可解析 | 记 `error` ⇒ 涉及它的 fork 判「无法对账」（C 段）⇒ 不静默跳过 |
| 判定表命中 | 逐条打印 `[FAIL] <项>` ⇒ **exit 1** |

## 9. 边界与未做（对 DESIGN §7）

1. **不保证「所有返工都已登记」**——只保证「已登记的属实」+「fork 输出无漏登」（后者有机械信号，前者无）；
2. **触发条件的值未裁**——`trigger_kinds` 只给封闭**形状**；
3. **不接门禁**（I-6）——「接门禁」登记为触发驱动观察项（CHECKLIST §11）；
4. **不追溯历史**——除 `p009-first-run-001-fork-demo` 的豁免登记外，不为历史 `vN` 会话补登记（它们多数**不是** fork 产物）。
