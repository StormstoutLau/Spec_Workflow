# 设计文档：缺陷修复方案（gate auto-commit + DIS-008 并行 Edit 竞态，P-022）

---
id: defect-fixes-DESIGN
type: design
version: 1.2
status: verified
date: 2026-09-08
depends: [SPEC-PROCESS, ADR-0010, ADR-0009, spec-runner-DESIGN, step-gate-CHECKLIST]
upstream: null
---

> **Feature**: P-022 缺陷修复批——两个缺陷均来自 P-020 吃狗粮全流程活体实证（2026-09-08，commit 90040fb）
> **状态**: 定稿（v1.2）——用户裁决 D1 = A+B 修正后采纳 / D2 = 规则化+追记；实施批完成（spec_runner v1.2.0 + selftest 28/28 + 文档四处 + CHECKLIST_FUNC v1.0 accepting）
> **来源**: ① gate auto-commit 缺陷 = P-019 独立 pass 登记的 P3 观察项（P-020 候选）在 P-020 吃狗粮中活体复现（selftest 触发 gate 自动提交把真实 session finalize 行卷入 `gate:always-pass:pass` 噪音 commit，已软重置回并）；② DIS-008 竞态 = P-020 收束批 CODE_WIKI 同文件 6 并行 Edit 竞态复发（4 处回滚，串行重放修复）

---

## 1. 缺陷一：spec_runner gate auto-commit（代码缺陷）

### 1.1 根因分析（证据链）

`git_snapshot()`（tools/spec_runner/spec_runner.py L106-114）被 cmd_gate（L130）与 run（L308）无条件调用。三个结构性故障：

| # | 故障 | 证据 | 后果 |
|---|------|------|------|
| F1 | **隔离失效**：`cwd=ROOT` 硬编码真实仓，绕过 `SR_SESSIONS_DIR` 注入 | L109 `git add -A sessions` 相对 ROOT 解析；selftest 设 temp 目录期望零副作用，但 git 路径固定在真实仓 | 注释「非 git 环境（selftest 临时目录）」与实际行为矛盾（谎言注释）；selftest 的 st-001 测试 gate 在真实仓 git add/commit |
| F2 | **语义错配**：message 用调用方 session 名，stage 全目录 | L110 `add -A sessions`（全目录无差别）+ L130 message=`(session st-001)` | 测试 session 名义提交用户真实 session 的未提交变更（本轮 = specwf-p020-20260908v2.jsonl finalize 行） |
| F3 | **无条件自动提交**：无 opt-in/opt-out | 无任何环境/参数门控；且 commit 无 `--no-verify` | 全仓 dirty 的开发中间态被自动化时刻无差别落 commit；pre-commit 三 hook 在编辑中途态可能失败打断开发 |

**方法论关联**：F3 = ADR-0010 Q3「未激活零副作用」的反面教材——工具便利以隐式副作用形式入侵。修复方向天然通向**懒加载化门控**（显式激活才生效）。

### 1.2 修复方案（三选项 + 推荐）

| 方案 | 内容 | 代价/风险 |
|------|------|----------|
| **A 门控（默认关）** | `git_snapshot` 首行：`if os.environ.get("SR_GIT_AUTOCOMMIT") != "1": return` | 最小侵入；run/gate 调用点不变；改变 DESIGN「gate 后自动 commit」语义 → 需 DESIGN 追记 |
| **B 范围与信息绑定** | `add -A sessions` → `git add -- <sid>.jsonl`（实际写入文件）；cwd 由 `git rev-parse --show-toplevel` 派生，非 git 环境静默跳过 | 彻底修 F1/F2；需处理 git 根探测回落 |
| **C 兜底** | selftest 环境不设 `SR_GIT_AUTOCOMMIT` → 天然零写入 | 只治 selftest 场景，不治日常 gate 捎带 |

**推荐 = A+B 组合**：门控默认关（Q3 零副作用）+ 即使显式激活也只提交本次实际写入的 sid 文件且消息与内容一致（F1/F2 同时消除）。C 作为 A 的自然结果无需单独实现。

### 1.3 影响面

- 语义变化：SPEC_RUNNER_DESIGN D3「gate 后 git commit 钩子」+ L1「事件流 + git commit 持久化」表述需追记（I-3 版本化纪律）
- README 命令面补充 `SR_GIT_AUTOCOMMIT` 说明
- 既有 selftest F1-F19 不受影响（门控默认关）

### 1.4 subagent 技术审查结果（v1.1 增补，2026-09-08，general-purpose 只读审查）

**审查裁定：A+B 组合可采纳（修正后采纳），无否决项。**

| 审查项 | 裁定 | 要点 |
|--------|------|------|
| 根因 F1/F2/F3 准确性 | ✅ 全成立 | 提交 f39f29b（st-001）与真实 session 同处 sessions/ 实证；selftest L467 仅注入 SR_SESSIONS_DIR=tmp 但 git 在真实仓操作；F3 的 commit 无 --no-verify，pre-commit 三校验器会跑 |
| 方案 A 门控充分性 | ✅ 默认关可根除 | ⚠️ 小绕过：selftest `env=dict(os.environ,...)` 拷贝父环境——若宿主已导 `SR_GIT_AUTOCOMMIT=1` 仍会提交 → **实施需在 selftest fixture 显式 pop 该变量**（与 C 自然衔接） |
| 方案 B 技术细节 | ✅ 正确，1 处关键 | **文件路径必须取自 `sessions_dir()`（与 EventWriter 同 base），不得硬编码 ROOT/"sessions"**，否则 tmp 隔离失效复发；rev-parse 起始 cwd 仍是 ROOT |
| 设计一致性 | ✅ | SPEC_RUNNER_DESIGN 四处需修订：§2 目标(2)「+ git commit」/ §4「gate 后 git commit 钩子」/ mermaid「gate 后自动 commit」/ LOC 表「gate 后触发」→ 均改「opt-in（SR_GIT_AUTOCOMMIT=1）默认关」；**ADR-0010 宜表述为"借懒加载原则"而非门禁强制项**（Q1-Q3 对象 = 候选吸收物，本修复是既有工具改造） |
| 边界/遗漏 | ⚠️ 2 项 | B 只提交单文件 = 行为比既往"全目录清扫"收窄，需文档声明；激活路径是否加 `--no-verify` 未决策（保留为实施时裁定项） |
| 过度工程 | ✅ A+B 不算过度 | A 单用已足以关闭事故；B 为激活路径加固 + 结构性修 F1，成本极低 |

**实施最需警惕 2 点**：① B 的文件路径必须源自 `sessions_dir()`；② 决定激活路径是否 `--no-verify` + selftest 显式 pop `SR_GIT_AUTOCOMMIT`。

## 2. 缺陷二：DIS-008 并行 Edit 竞态（工具行为缺陷）

### 2.1 复发记录

[docs/discoveries/README.md DIS-008](../../docs/discoveries/README.md)（open）：**第 4 次复发**（2026-09-08 P-020 收束批）——CODE_WIKI.md 单消息 6 个并行 Edit，4 处（L70/L99/L705/L707）回滚为旧文本，经串行重放修复。前三次：2026-08-17 Tier1 执行 6/10 回滚 / 同日 v1.4 头部行 + §9 残留 / 2026-09-08 P-018 行 97 回滚。

### 2.2 根因

Edit 工具对同一文件无「基于最新版本」的乐观并发控制：batch 内后发写入以陈旧快照为基覆盖先发编辑 → 静默回滚。操作缓解（同文件串行 + 编辑前 Read + 终验全覆盖 grep）已登记但**无执行强制**——batch 优化驱动下同文件并发是 agent 常态行为。

### 2.3 修复方案（推荐双做）

1. **规则化**：AGENTS.md「禁止事项」增两条——「同一文件的多个修改必须串行（前一 Edit 结果返回后再发下一 Edit）；不同文件可并行」+「batch 编辑后必须对全部修改行做全覆盖终验 grep」
2. **追记**：DIS-008 维持 open（无工具层普适方案），登记第 4 次复发逐字证据
3. **不做**：M7 样本不入账（工具行为非文档声明错误）；不为任意 md 文件构建通用竞态检测器（过度工程）

## 3. 验收路线（待决策后进入实施批小流程）

1. 本方案落档（本文件）→ **subagent 详细审查完成（v1.1，§1.4：auto-commit 方案 = A+B 修正后采纳，无否决项）** → 用户决策（D1/D2/D3）
2. 决策通过 → 实施批（DESIGN 定稿 + CHECKLIST 两件套，P-016/P-020 小流程先例）：
   - 代码：spec_runner.py git_snapshot 门控 + 范围绑定；selftest 增补 fixture
   - 文档：SPEC_RUNNER_DESIGN 追记 + README + AGENTS.md 规则 + DIS-008 追记
   - 落档：PROGRESS P-022 + CODE_WIKI + 三校验器全绿
3. 无新增 M7 样本预期（修复为编程变更非文档声明错误）

## 4. 决策记录（v1.2，2026-09-08 用户裁决 + 实施批）

| # | 决策项 | 裁决 | 实施落点 |
|---|--------|------|---------|
| D1 | auto-commit 修复粒度 | **A+B 修正后采纳**（含审查修正项：B 路径源自 sessions_dir / selftest pop env / --no-verify） | spec_runner.py v1.2.0：`git_snapshot(sid, message)` 门控默认关 + 精确单文件 + 会话目录 git 根派生；selftest F25/F26 |
| D2 | AGENTS.md 规则化 | **双做**（规则化 + DIS-008 追记） | AGENTS.md 禁止事项两条；docs/discoveries/README.md DIS-008 第 4/5 次复发追记 |
| D3 | 编号登记 | **P-022 立项**（方案落档即登记 in-progress，随本批 done） | PROGRESS P-022 |

**实施批产物**：DESIGN v1.2 verified + CHECKLIST_FUNC v1.0 accepting（13/13 + selftest 28/28 + 三通道全绿）；文档四处（README / SPEC_RUNNER_DESIGN / AGENTS.md / DIS-008）。

## 5. 修订历史

| 日期 | 变更 |
|------|------|
| 2026-09-08 | v1.0 创建——缺陷根因分析（F1/F2/F3）+ 修复三选项 A/B/C 推荐 A+B + DIS-008 复发与规则化方案 |
| 2026-09-08 | v1.1 —— subagent 技术审查结果回填（§1.4：A+B 修正后采纳无否决项；实施警惕点 = sessions_dir 派生路径 / --no-verify 裁定 / selftest pop env） |
| 2026-09-08 | v1.2 —— 用户裁决 D1/D2/D3 记录（§4）+ 实施批完成 → 状态 verified |