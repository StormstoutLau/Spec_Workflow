# 设计文档：board-generator / 任务看板生成器（L0 门禁钩子落地）

---
id: board-generator-DESIGN
type: design
version: 1.0
status: verified
date: 2026-09-11
depends: [academic-writing-workflow-RESEARCH, ADR-0010, SPEC-PROCESS]
upstream: null
---

> **Feature**: board-generator / 任务看板生成器（把 per-feature 多流状态压缩为单行认知块，L0 门禁钩子自动刷新）
> **创建日期**: 2026-09-11
> **状态**: verified（实施批 P-041，实测通过）
> **Spec 步骤**: Step 3-4（设计）+ Step 5-7（实施验收）
> **基于调研**: [academic-writing-workflow RESEARCH](../academic-writing-workflow/RESEARCH.md) §10（任务看板与自动化追踪）+ §11（看板能否不依赖用户指令自动实时更新）
> **任务来源**: 用户指令「按 L0 门禁钩子方案落地看板生成器，并验证提交即刷板功能」——即 RESEARCH C-7 懒加载 gate 的**显式触发**（触发条件 = 用户明确要求落地 board 生成器）。

---

## 1. 设计目标

把 RESEARCH §10.5 的「markdown-native 只读看板生成器」概念落地为最小可执行件：扫描既有真值源（PROGRESS / 事件流 / spec 目录 / git 分支），把 per-feature 的**多流状态压缩为单行认知块**，按状态分组并暴露「需要你 / NEXT」队列；并以 **L0 门禁钩子**（RESEARCH §11.5）在 pre-commit 时**自动重生成并暂存**，实现「提交即刷板」，**完全脱依赖用户指令**。

**目标约束**：零第三方依赖（stdlib only）；唯一写路径 = 自己的派生产物；不改动任何既有校验器语义；不引入 GUI 服务器 / 常驻守护进程（FileSystemWatcher 与终端轮询 L1/L2 档本批不启用）。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| 本仓 per-feature 事件流独立 = 多流并存，认知过载真实 | 以「单行认知块 + 3 状态分组 + NEXT 队列」为主结构 | RESEARCH §10.1 / C-6 |
| Magentic-One 二账本「Task Ledger（想做的事）vs Progress Ledger（实际进度）」 | 输入映射：PROGRESS=Task Ledger；sessions 事件流=Progress Ledger | RESEARCH §10.2 / A-28 |
| do-knowledge-studio「hook/CI 自动更新生成节」+ ProjectOdyssey「pre-commit 自动计数防 drift」 | 触发选 **L0 门禁钩子**（并进既有 pre-commit），非 L1 监听 / L2 轮询 | RESEARCH §11.3 / A-33 |
| 三路径自动强度 L0/L1/L2 均零新依赖 | 本批只落 L0（零成本档），L1/L2 保留为增量可选 | RESEARCH §11.5 / C-7 |
| 看板=只读视图，职责=从真值源被动重算 | 输出为**纯派生产物**（100% 机器生成，无人工内容） | RESEARCH §11.1 / B9 |

### 2.2 相关 ADR

| ADR | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 懒加载三问门禁（放哪层 / 激活条件 / 未激活零副作用） | 本 feature 由 C-7 懒加载 gate 的**显式触发**（用户指令）激活；分层 = Layer-1（工具层生成器）；未激活时零副作用 |
| [ADR-0005](../../adr/ADR-0005-audit-evidence-binding-spec-workflow.md) | 审计证据绑定 | 看板每行 = 真值源的机械投影，不做推断性归因 |
| ADR-0007 | 统一文档契约（front-matter 七字段） | 四件套与 CODE_WIKI 登记遵守 DC1-DC4 |

### 2.3 职责边界

**职责内**：从既有源机械投影状态 → 写单一派生产物；在 pre-commit 时重生成并暂存。

**职责外（明确不做）**：
- 不新增任何**状态真值**（看板不是真值源，改看板不改变任何状态）；
- 不做推断性判断（不猜测阻塞原因、不判定「应该做什么」）；
- 不介入既有校验器（dc_validator / m7_stats / repo_stats / step_enforce 语义零改动）；
- 不引入 GUI 服务器、常驻进程、第三方 TUI 库。

## 3. 架构设计

### 3.1 整体架构

```
                  [真值源（只读）]                       [派生视图（唯一写路径）]
  docs/PROGRESS.md ─────────────┐
  tools/spec_runner/sessions/*.jsonl ─┤
  spec/*/（feature 目录）──────┼──► scripts/board_gen.py ──► docs/BOARD.md
  git branch / worktree ───────┘            ▲
                                            │ pre-commit 第五 hook（board-gen）
                                      写 + git add → 提交即刷板
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| `parse_progress` | 解析 P 行（ID/事项/状态/优先级） | PROGRESS.md 文本 | `list[Task]` | stdlib re |
| `read_sessions` | 每 P 编号取最新 session，提取最远 step + verdict 软性 | sessions/*.jsonl | `dict[pid, SessionInfo]` | stdlib json |
| `list_branches` | 列 git 分支/工作树（fork 支线） | git 子进程 | `list[str]` | stdlib subprocess |
| `render` | 组装 markdown 看板（认知块 + 分组 + NEXT） | 上述三者 | str | 纯函数 |
| `write_board` | 幂等写（内容变才写），返回是否变化 | str | bool | stdlib |
| CLI | `--stdout` / `--check` / `--selftest` | argv | exit code | stdlib argparse |

### 3.3 数据流

`PROGRESS + sessions + spec + git` →（解析）→ 中间结构 →（渲染）→ markdown 文本 →（幂等写）→ `docs/BOARD.md`。

### 3.4 控制流

**人工/CI**：`python scripts/board_gen.py`（默认写）→ exit 0。
**pre-commit**：hook `board-gen` 以变更文件为参数 → in-scope 判定 → 生成 → 内容变化时写 + `git add docs/BOARD.md`（使提交包含最新板）→ exit 0。
**门禁/CI 校验**：`--check` 不写，仅当 `docs/BOARD.md` 与最新源不一致时 exit 1（供只读复核）。

## 4. 接口定义

### 4.1 数据结构

```python
@dataclass(frozen=True)
class Task:
    pid: str            # "P-041"
    title: str          # 事项
    status: str         # pending / in-progress / blocked / done
    priority: str       # 优先级列原文（"—" 常见）
    evidence: str       # 依据列原文

@dataclass(frozen=True)
class SessionInfo:
    sid: str            # specwf-p041-20260911
    last_step: str      # 最远 step_id（research/design/implement/verify/finalize）
    soft: bool          # 末条 gate 事件 exit==2（软性存疑）
    last_ts: str        # 末事件时间戳（确定性基准来源）
```

### 4.2 关键函数

```python
def parse_progress(text: str) -> list[Task]: ...
def read_sessions(sessions_dir: Path) -> dict[str, SessionInfo]: ...
def list_branches(root: Path) -> list[str]: ...
def render(tasks, sessions, features, branches, basis: str) -> str: ...
def write_board(path: Path, content: str) -> bool: ...   # True = 内容变化已写
def main(argv=None) -> int: ...                          # 0 ok / 1 --check 失配 / 2 工具错误
```

## 5. 替代方案

### 5.1 方案 A: 门禁钩子自动重生成 + 暂存（选择）

- 描述: pre-commit 第五 hook 调 `board_gen.py` 生成后 `git add docs/BOARD.md`。
- 优点: **提交即刷板**（板随提交一并入库）；零常驻进程；零新依赖；失败面小（单文件幂等写）。
- 缺点: 依赖 pre-commit 通道（`--no-verify` 可旁路——与本仓既有 hook 同一诚实护栏边界）。
- 选择理由: 与本仓已有四 hook 同构，L0 档零成本（RESEARCH §11.5）。

### 5.2 方案 B: FileSystemWatcher 常驻监听（否决）

- 描述: 后台守护监听源文件变化即重生成（L1 档）。
- 否决理由: 引入常驻进程（与「单写者 + 零常驻」定位冲突）；本批不需秒级实时性；L1 保留为增量可选档。

### 5.3 方案 C: 终端轮询渲染（否决）

- 描述: `watch -n 5` 或 Rich Live 全屏常驻看板（L2 档）。
- 否决理由: 需占用终端会话；rich/tqdm 属第三方依赖（违零依赖）；L2 保留为增量可选档。

### 5.4 方案 D: 独立 web 看板（否决）

- 描述: 起本地 HTTP 服务渲染可交互看板（如 Markdown Task Board）。
- 否决理由: 引入服务器进程与前端资产；违「最小工具层」定位（RESEARCH §10.3 已判重平台排除）。

## 6. 数据结构（BOARD.md 输出结构）

```markdown
# BOARD｜任务看板（派生视图）
<!-- GENERATED by scripts/board_gen.py —— 纯派生产物，请勿手改；重跑即刷新 -->
> 生成基准：源最大 ts = <max ts>；P 行 = <n>；session = <m>；feature 目录 = <k>

## ⚑ 需要你 / NEXT
- P-XXX 事项 —— 原因（阻塞 / 软性存疑 / 待你审）

## ▶ 进行中（in-progress）
| P | 事项 | 最远 step | 上次事件 | 阻塞 |
|---|------|----------|---------|------|

## ⚠ 待你审（pending）
| P | 事项 | 最远 step | 上次事件 | 阻塞 |
|---|------|----------|---------|------|

## ✖ 阻塞（blocked）
| P | 事项 | 最远 step | 上次事件 | 阻塞 |
|---|------|----------|---------|------|

## ✅ 已完成（最近 N 条）
| P | 事项 |
|---|------|

## ⑂ fork / 支线
- <branch / worktree 列表>
```

## 7. 错误处理

| 错误场景 | 处理方式 | 用户可见信息 |
|---------|---------|------------|
| PROGRESS.md 不可读 | exit 2（工具错误），不写盘 | `[tool-error] PROGRESS.md 不可读` |
| sessions 目录缺失/为空 | 降级：step 列显示 `—`，不报错 | 无（正常降级） |
| 单个 jsonl 行不可解析 | 跳过该行（容错），继续 | 无 |
| git 不可用 | 分支段显示「（git 不可用）」 | 无（正常降级） |
| `--check` 且板已过期 | exit 1，不写盘 | `BOARD.md 已过期（源已变），请重跑 board_gen` |

## 8. 不变式（Invariants）

1. **I-1 单写路径**：唯一写路径 = `docs/BOARD.md`；绝不写其他任何文件（保持其余校验器的零副作用语义）。
2. **I-2 确定性**：输出**禁 wall clock**（基准取源最大 ts）→ 同源双跑**逐字节一致**。
3. **I-3 幂等**：内容未变则不写盘（`write_board` 返回 False）→ hook 二次运行零扰动。
4. **I-4 零依赖**：stdlib only（argparse/json/re/subprocess/pathlib）。
5. **I-5 纯派生**：BOARD.md 不含人工内容，100% 可重生成 → 覆盖无需备份（AGENTS.md 备份纪律的例外条件：纯派生物非源文件）。
6. **I-6 不增真值**：看板不持有任何原始状态；改板不改变 PROGRESS/sessions/spec 任何内容。

## 9. 幻觉抑制审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 所有设计决策可追溯到 RESEARCH §10/§11（A-28~A-34 / B8/B9 / C-6/C-7）
- [x] 无未经验证的假设（触发机制、输出结构均有社区先例锚点）
- [x] 无归因扭曲（看板只做机械投影，不含推断）

### 9.2 替代方案审查

- [x] 列 4 个替代方案（L1/L2/web/——含门禁方案自身共 4 否决）
- [x] 每个替代方案有明确否决理由

### 9.3 职责边界审查

- [x] 职责边界清晰（§2.3：不增真值、不推断、不改既有校验器）
- [x] 不越界（不吞并 observability 平台 / 不承担真值源）

## 10. 对实施的输入

### 10.1 关键工程约束

1. 输出 byte-deterministic（禁 `datetime.now()`）——用源最大 ts 作基准。
2. 写盘仅在内容变化时（幂等）。
3. hook 需 `git add docs/BOARD.md` 才能实现「提交即刷板」。
4. Windows 环境：用 `sys.executable` 前缀（同既有 hook 先例）。
5. 新增脚本 + 新增 hook 会改变 repo_stats 的 `fs.scripts` 与 `fs.hooks` 真值 → 必须同步 CODE_WIKI stats 块 `declared`。

### 10.2 风险与缓解

| 风险 | 缓解措施 |
|------|---------|
| hook 写盘引发「修改后未暂存」导致 pre-commit 报失败 | 生成后立即 `git add docs/BOARD.md`，使暂存区与工作区一致 |
| 板内容含 wall clock → 每次提交都产生 diff | I-2 禁 wall clock（实测双跑字节一致） |
| 输出漂移被误当真值 | 板首行显式标注「派生视图 / 请勿手改」+ 每行来自源 |
| repo_stats 因新脚本/新 hook 报 declared 失配 | 同批同步 stats 块 `declared.scripts` / `declared.hooks` |

---

**Review 签字**: 见 [CHECKLIST.md](./CHECKLIST.md) 与 [IMPLEMENTATION.md](./IMPLEMENTATION.md) 验收记录
