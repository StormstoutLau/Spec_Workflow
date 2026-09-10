# 实施文档：board-generator / 任务看板生成器（L0 门禁钩子落地）

---
id: board-generator-IMPLEMENTATION
type: design
version: 1.0
status: verified
date: 2026-09-11
depends: [board-generator-DESIGN, academic-writing-workflow-RESEARCH]
upstream: null
---

> **Feature**: board-generator / 任务看板生成器（P-041 实施批）
> **创建日期**: 2026-09-11
> **状态**: verified（实测通过：selftest 11/11 + 「提交即刷板」端到端经 pre-commit 通道实测）
> **Spec 步骤**: Step 5-7
> **基于设计**: [DESIGN.md](./DESIGN.md) v1.0
> **任务来源**: 用户指令「按 L0 门禁钩子方案落地看板生成器，并验证提交即刷板功能」

---

## 1. 实施内容总览

| # | 交付物 | 路径 | 性质 |
|---|-------|------|------|
| 1 | 看板生成器脚本 | `scripts/board_gen.py`（**P-043 已退役**，由 `scripts/console_gen.py` 承接） | 新增（stdlib only） |
| 2 | 派生视图产物 | `docs/BOARD.md`（**P-043 已退役**，由 `docs/CONSOLE.md` 承接） | 新增（100% 机器生成） |
| 3 | pre-commit 第五 hook | `.pre-commit-config.yaml`（`board-gen`） | 新增（L0 触发） |
| 4 | 批次决策流 | `tools/spec_runner/sessions/specwf-p041-20260911.jsonl` | 新增（五步 decision 链） |
| 5 | 待办登记 | [docs/PROGRESS.md](../../docs/PROGRESS.md) | 追加 P-041 行 |
| 6 | 视图层同步 | [CODE_WIKI.md](../../CODE_WIKI.md) | 版本头 + 目录树 + §9 索引 + stats 块 |

## 2. 落地映射（DESIGN → 实现）

| 设计条目 | 实现落点 | 实测证据 |
|---------|---------|---------|
| D1 落点 = `scripts/board_gen.py` + `docs/BOARD.md` | 两文件均落地 | §4.1 直跑 |
| D2 输出形态（认知块 + 3 状态分组 + NEXT） | `render()` + `_next_queue()` + `_table()` | selftest S2/S3 |
| D3 触发 = L0 门禁（写 + git add） | hook `board-gen`（`--stage`） | §4.2 端到端 |
| D4 输入 = 只读既有真值源 | `parse_progress` / `read_sessions` / `list_features` / `list_branches` | selftest S1/S4 |
| D5 确定性 = 禁 wall clock | `_basis()` 取源最大 ts | selftest S5/S8 |
| D6 写边界 = 唯一写路径 | `write_board()` 仅写 `docs/BOARD.md` | selftest S11（I-1） |
| D7 零依赖 = stdlib only | import 仅 argparse/json/os/re/subprocess/sys/tempfile/dataclasses/pathlib | 源码复核 |
| I-2 确定性 | 见 D5 | selftest S8 |
| I-3 幂等 | `write_board` 内容比对 | selftest S7 + §4.2 二次运行 |

## 3. 依赖与签名验证

| 项 | 声明 | 实测 | 结论 |
|----|------|------|------|
| 第三方依赖 | 零（stdlib only） | import 清单复核（无第三方） | ✅ |
| Python 版本 | 3.7+（同仓内既有脚本） | 本机 3.11.x 运行通过 | ✅ |
| 对既有校验器影响 | 零语义改动 | 新增脚本/hook 仅改变 `fs.scripts` / `fs.hooks` 真值 → 已同步 stats 块 `declared` | ✅ |
| 对既有 hook 影响 | 零 | 既有 dc-validator / m7-stats / repo-stats / step-enforce 定义未改（board-gen 为**新增第五项**） | ✅ |

## 4. 验收实录

### 4.1 脚本直跑（人工/CI 通道）

```
$ python scripts/board_gen.py
board_gen: docs/BOARD.md 已刷新
$ python scripts/board_gen.py          # 二次（幂等）
board_gen: docs/BOARD.md 无变化
$ python scripts/board_gen.py --check
BOARD.md 与源一致                        # exit 0
```

首次生成基准：`P 行 = 40；session = 16；feature 目录 = 31`（与 `repo_stats` 真值一致）。

### 4.2 「提交即刷板」端到端实测（pre-commit 通道）

真实源变更（PROGRESS 加 P-041 行 + 新增 `specwf-p041-20260911.jsonl`）后，经 pre-commit 通道执行：

```
$ pre-commit run board-gen --files docs/PROGRESS.md
Task board generator (derived view, P-041)...............................Passed

$ git status --short docs/BOARD.md
A  docs/BOARD.md                        # ← 已暂存（提交将包含最新板）

$ Select-String docs/BOARD.md -Pattern "生成基准"
> 生成基准：源最大 ts = 2026-09-11T09:50:00+08:00；P 行 = 41；session = 17；feature 目录 = 31
                        # P 行 40→41，session 16→17：板已随源刷新
$ Select-String docs/BOARD.md -Pattern "P-041"
| P-041 | 任务看板生成器落地（L0 门禁钩子：提交即刷板） | finalize | 2026-09-11 | — |
                        # step 投影 = finalize（读自新 session 的最远 step）
```

**幂等确认**（二次运行零扰动）：

```
$ pre-commit run board-gen --files docs/PROGRESS.md
Task board generator (derived view, P-041)...............................Passed   # 无变化
$ python scripts/board_gen.py
board_gen: docs/BOARD.md 无变化
$ python scripts/board_gen.py --check
BOARD.md 与源一致
```

### 4.3 内嵌自测

```
$ python scripts/board_gen.py --selftest
selftest: 11/11 PASS
```

| 用例 | 覆盖 |
|------|------|
| S1 | P 行解析（4 条 + 状态/优先级） |
| S2 | 状态分组齐（in-progress / pending / blocked / done 四段） |
| S3 | NEXT 队列（阻塞 + 软性存疑 + 待你审 三来源） |
| S4 | 最远 step 投影（implement） |
| S5 | 禁 wall clock（基准取源最大 ts） |
| S6 | 纯派生标注（请勿手改） |
| S7 | 幂等（首写 True / 二次 False） |
| S8 | 确定性（双跑字节一致） |
| S9 | `--stdout` 不写盘 |
| S10 | `--check` 双态（一致 exit 0 / 过期 exit 1） |
| S11 | I-1 单写路径（其余文件零变化） |

### 4.4 三校验器回归

`dc_validator` / `m7_stats` / `repo_stats` 全绿（详见 [CHECKLIST.md](./CHECKLIST.md) §3）。

## 5. 实施期发现（修正实录）

| # | 发现 | 处置 |
|---|------|------|
| DR-1 | 表格列名笔误：「排序」应为「优先级」（列语义 = PROGRESS 优先级列投影） | 当场修正（`_table()` 表头） |
| DR-2 | 新增脚本/hook 会使 `repo_stats` 的 `fs.scripts` 6→7、`fs.hooks` 4→5 失配 | 同批同步 stats 块 `declared`（+ `spec_feature_dirs` 30→31 / `progress_tasks` 40→41） |
| DR-3 | PT-8 正则 `(双\|两\|三\|四) hook` 既漏「五 hook」（新值）又会误捕**非总数**用法：序数「第**四** hook」、范围「一~**四** hook」、历史叙事「四可执行件**四** hook」 | 先试 `(?<!第)` 仍留 6 处误捕（实测）→ 最终**收紧为锚定当前态位点** `repo-local (双\|两\|三\|四\|五) hook`（仅 §2.1 树行声明当前总数，序数/范围/历史叙事不匹配） |
| DR-4 | CODE_WIKI「覆盖对象」行遗留漂移（`spec/ 二十六 feature 目录` 停旧、`deepeval_m7_eval.py` 未登记） | 顺手校正为 `三十一` 并补齐脚本清单（声明=重数纪律） |
| DR-5 | DESIGN.md 内 ADR 链接文件名臆造（`ADR-0010-lazyload-absorption-gate.md` / `ADR-0005-audit-evidence-binding.md`）→ dc_validator P2 断链 ×2（机械拦截实证） | 按 `LS adr/` 实际名修正为 `ADR-0010-lazy-loading-architecture-gate.md` / `ADR-0005-audit-evidence-binding-spec-workflow.md` |

## 6. 上游修订注

无（本批为新增能力，未推翻任何既有裁决；RESEARCH C-7 的懒加载 gate 由「用户明确要求落地」这一预注册触发条件显式激活，符合 ADR-0010 Q2）。

## 7. 后续可选增量（未实施）

| 档 | 内容 | 状态 |
|----|------|------|
| L1 | FileSystemWatcher 监听源文件自动重生成（免提交即刷） | 未实施（保留，RESEARCH §11.5） |
| L2 | 终端轮询渲染（`watch -n` 常驻实时） | 未实施（保留） |
| — | H5 各档常驻开销实测 | 未实测 |

---

**实施签字**: 见 [CHECKLIST.md](./CHECKLIST.md) §4 验收结论
