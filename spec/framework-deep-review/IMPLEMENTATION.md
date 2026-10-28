# 实施文档：批次绑定门禁（O3 Phase 1）

---

id: framework-deep-review-IMPLEMENTATION
type: design
version: 1.13
status: draft
date: 2026-10-26
depends: [framework-deep-review-DESIGN, framework-deep-review-RESEARCH]
upstream: null

---

> **Feature**: framework-deep-review（U-1 / O3 Phase 1 门禁实施）
> **创建日期**: 2026-10-26
> **修订**: v1.1（2026-10-26，P-131：U-2 注入测试 5 例，批次绑定测试 15 → 20）
> **修订**: v1.2（2026-10-26，P-132：runner `step-gate` 显式声明 `--expect` / `--legacy`，selftest 81 → 83）
> **修订**: v1.3（2026-10-26，P-134：ci.yml step-enforce 段 fail-closed 化（§3.7）+ 本地注入 5 例 + §2.3/§8.1 变更面同步）
> **修订**: v1.4（2026-10-27，P-137：U-10 C 实施（§3.8）——digest 生成 / 校验 + `--doc-digest` + 8 例注入，批次绑定测试 20 → 28）
> **修订**: v1.5（2026-10-27，P-139：P1-1 真实 runner 集成回归（§3.9）——触发面补 runner + `tests/harness.py` + 集成 10 例 + 变异 4 例，`unittest discover` 36 → 50）
> **修订**: v1.6（2026-10-27，P-140：CI 逐提交遍历（§3.10）——`rev-list --reverse` + `checkout -f` + 执行器能力分派 + 合并提交跳过；`test_ci_per_commit_walk` 5 断言；零脚本行为变更）
> **修订**: v1.7（2026-10-28，P-141：CI 远端读数回填——§3.10 补远端首次实测读数；实施面零变更）
> **修订**: v1.8（2026-10-28，P-142：`push(main)` 合并面读数回填——§3.10 补真实合并提交走查读数；实施面零变更）
> **修订**: v1.9（2026-10-28，P-143：`push(main)` 补充读数——§3.10 补第 2 样本读数；实施面零变更）
> **修订**: v1.10（2026-10-28，P-144：**U-11 合并面关闭**——§3.11 新增 `step_enforce --check-merge` + CI 阶段 1 + 4 例测试；`unittest discover` 51 → 55）
> **修订**: v1.11（2026-10-28，P-145：**阶段 1 远端读数登记**——§3.11 补真实 `push(main)` 读数（run `40603730644` / 合并提交 `e8154eb` / `无 evil 内容（6 个受判路径均等于某一父）` / 88 s 全绿）；实施面零变更）
> **修订**: v1.12（2026-10-28，P-146：**阶段 1 远端第 2 样本**——§3.11 补 run `40660622448`（合并提交 `7bcce12` / 89 s 全绿）；实施面零变更）
> **修订**: v1.13（2026-10-28，P-147：**阶段 1 远端第 3 样本**——§3.11 补 run `40663831556`（合并提交 `023e456` / 66 s 全绿）；实施面零变更）
> **状态**: 草稿
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md)
> **基于调研**: [RESEARCH.md](./RESEARCH.md) §11

---

## 1. 实施概述

把 `step_enforce.py` 从「feature → 单个主 P → 文件名末位 session」改为 **O3 混合解析器**：

1. 新/变更 P 行声明优先；
2. 变更 session 次之；
3. 分支名弱回退；
4. 仅 whitespace-only 进入维护模式；
5. 其余语义性四文档改动一律失败。

同时把 pre-commit 触发面扩到 session 与 PROGRESS，把 CI 从全量文档改为 merge-base 变更集，并新增真实 runner 集成测试。零新依赖、零 session schema 变更、零第三方 action。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|---|---|---|---|
| 语言 | Python | 3.11+ | ✅ 与 CI / 开发环境一致 |
| 依赖 | 无（stdlib：`re` / `subprocess` / `pathlib` / `dataclasses` / `json`） | - | ✅ |
| VCS | git | 2.40+ | ✅ `git show` / `git diff --cached` / `git diff A...B` |
| CI | GitHub Actions | `windows-latest` + `checkout@v5`（fetch-depth 0） | ✅ |

### 2.2 依赖版本验证

| 依赖 | 声明版本 | 实测 | 兼容性 | 验证方式 |
|---|---|---|---|---|
| Python | 3.11+ | 3.11.16 | ✅ | 本机 / CI |
| git | 2.x | 2.54 文档行为 | ✅ | `git-diff` / `githooks` 官方文档 |
| pre-commit | 3.x | 现有六 hook | ✅ | `.pre-commit-config.yaml` |

无新增 PyPI / npm 依赖。

### 2.3 文件结构（变更面）

```text
scripts/spec_map.py                    # + parse_progress_rows / changed_pids
scripts/step_enforce.py                # 重写为 O3 解析器；P-137：+ doc_digest / verify_digests / --doc-digest
tests/test_batch_binding.py            # 新增：真实 runner + git 集成测试（P-137：20 → 28）
tests/harness.py                       # P-139：临时仓 + 脚本副本 + env 注入共享夹具
tests/test_runner_integration.py       # P-139：真实 runner 10 例（step-gate / verify-anchor / fork / 两审计 / parity）；P-140：+ CI 逐提交 guard
tests/test_runner_mutation.py          # P-139：四类变异体 guard proof
.pre-commit-config.yaml                # step-enforce files 扩到 session + PROGRESS；P-139：blackbox files 补 runner
.github/workflows/ci.yml               # checkout fetch-depth 0 + 变更集 step-enforce；P-134 fail-closed 化；P-140 逐提交遍历
tools/spec_runner/spec_runner.py       # P-132：step-gate 显式 --expect / --legacy + selftest F80/F81
tools/spec_runner/README.md            # P-132：CLI 声明面 + selftest 83 项
spec/framework-deep-review/
├── DESIGN.md                          # 本设计
├── IMPLEMENTATION.md                  # 本文件
└── CHECKLIST.md                       # 验收
```

## 3. 模块实施

### 3.1 `spec_map.py`

#### 职责

提供 P 行解析与批次变更识别；保持现有 `build_pid_map` / `is_historical_exempt` 不变，避免破坏 `console_gen` 与旧测试。

#### 接口签名

```python
PROGRESS_ROW_RE = re.compile(
    r"^\|\s*(P-\d{3})\s*\|([^|]*)\|([^|]*)\|\s*([^|]*)\|")
SPEC_LINK_RE = re.compile(r"spec/([a-z0-9-]+)/")

def parse_progress_rows(text: str) -> dict[str, dict]:
    """返回 {P-xxx: {"status": str, "features": tuple[str, ...]}}。"""

def changed_pids(old_text: str, new_text: str) -> list[str]:
    """新增 P 行或 status 列变化；按新文本顺序返回。"""
```

#### 实施要点

- P 行解析只取前四列，避免描述列中的 `|` 干扰；
- `status` 去 `*` 与空白；
- features 去重保序；
- 旧函数不改签名、不改返回值。

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---|---|
| 每 feature 重扫全文 | 一次解析成 dict，O(n) |
| 正则回溯 | 固定前缀 + 字符类，无嵌套量词 |

### 3.2 `step_enforce.py`

#### 职责

判定模式、校验覆盖与完整性、输出机读决策、统一 exit 语义。

#### 接口签名

```python
BATCH_BINDING_MIN_P = 129
STEP_SEQUENCE = ("research", "design", "implement", "verify", "finalize")
SESSION_RE = re.compile(
    r"^tools/spec_runner/sessions/(specwf-p(\d{3})-[a-z0-9-]+)\.jsonl$")

@dataclass
class Decision:
    mode: str
    pids: list[str]
    sessions: list[str]
    features: set[str]
    source: str
    errors: list[str]

def resolve(changed_docs: set[str], changed_sessions: list[tuple[str, str]],
            progress_changed: bool, old_progress: str, new_progress: str,
            branch: str, whitespace_only: bool) -> Decision: ...

def check_sessions(sids: list[str], require_complete: bool) -> tuple[list[str], list[str]]: ...

def main(argv: list[str]) -> int: ...
```

#### 实施要点

- 路径归一化：`arg.replace("\\", "/")`，去掉 `./`；绝对路径转相对 `ROOT`；
- 本地模式：旧 PROGRESS = `git show HEAD:docs/PROGRESS.md`，新 = `git show :docs/PROGRESS.md`；
- CI 模式：`--base <ref>`，旧 = `git show <ref>:docs/PROGRESS.md`，新 = 工作树；
- 变更集：CI 传 `git diff base...HEAD` 结果；本地见下条；
- 本地模式：**忽略 argv 分块**，直接取 `git diff --cached` ∪ `git diff` ∪ `git ls-files --others` 的门禁路径集合（`pre-commit` 会按块传参，单块 argv 可能缺少 PROGRESS / session；`--all-files` 亦由此收敛）；git 失败 → exit 2；
- session 校验：`step-gate --session <sid>` 内部合法；`--expect research design implement verify finalize` 判 5/5；
- 不按文件名排序选 session：扫描该 PID 的全部 session；
- 弱声明：分支名 `(?:^|[/_-])p(\d{3})(?:$|[/_-])`，且 P 行存在、feature 覆盖；
- 维护模式：`git diff ... -w --ignore-blank-lines -- <docs>` 为空才放行；
- exit：0 通过；1 违规；2 git / 映射错误（fail-closed）。

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---|---|
| 每个 session 调一次 runner 且重复读文件 | 只对候选 PID 的 session 调；每个 session 最多两次（内部 + 完整） |
| 每次 hook 全仓扫描 session | 只扫描声明 PID 前缀 |
| git diff 多次 | 一次取 changed files；一次取 whitespace diff |

### 3.3 `.pre-commit-config.yaml`

```yaml
- id: step-enforce
  files: ^(spec/[a-z0-9-]+/(?:[A-Z0-9_]+_)?(?:RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST(?:_FUNC)?)\.md|tools/spec_runner/sessions/.*\.jsonl|docs/PROGRESS\.md)$
```

`blackbox-tests` 触发面加入 `tests/test_batch_binding.py`（`tests/.*\.py` 已覆盖）。

### 3.4 `.github/workflows/ci.yml`

- `actions/checkout@v5` 增 `with: fetch-depth: 0`；
- `step-enforce` step 改变更集：

```bash
BASE="${{ github.event.pull_request.base.sha }}"
[ -z "$BASE" ] && BASE="${{ github.event.before }}"
{ [ -z "$BASE" ] || [ "$BASE" = "0000000000000000000000000000000000000000" ]; } && BASE="HEAD^"
FILES=$(git diff --name-only "$BASE"...HEAD -- 'spec/**' 'tools/spec_runner/sessions/**' 'docs/PROGRESS.md' || true)
[ -n "$FILES" ] && python scripts/step_enforce.py --base "$BASE" $FILES || echo "step-enforce: no changed gate files"
```

不使用 `dorny/paths-filter` 或 `tj-actions/changed-files`（CVE-2025-30066）。

### 3.5 `tests/test_batch_binding.py`

真实 `spec_runner.py` + 临时 git 仓；不复制 stub。20 个用例：

| # | 用例 | 期望 |
|---|---|---|
| 1 | 新 P 行 + 5/5 session + 文档 | pass batch |
| 2 | 新 P 行 + 1/5 session + 文档 | fail |
| 3 | 旧 session、无声明、语义文档 | fail |
| 4 | P 行已在 HEAD，改 session + 文档 | pass session |
| 5 | 分支 `p130` + P 行 + 5/5 session | pass branch |
| 6 | whitespace-only 文档、无声明 | pass maintenance |
| 7 | 多 feature 批次 | pass |
| 8 | 新 P 行 0 链接 | fail |
| 9 | v9(1/5) + v10(5/5)，无新 session | pass（扫描全部，不排序） |
| 10 | feature 不在 P 行 | fail |
| 11 | 只改 session、1/5 | pass session-progress |
| 12 | 只加 P 行 | pass batch-registration |
| 13 | `--all-files` 全量 argv（含未变更文档） | pass；同 argv 下真实变更仍 fail |
| 14 | 分块 argv（只传文档子集） | pass batch（以整批变更集判定） |
| 15 | 非 git 目录 | exit 2（fail-closed） |
| 16 | 0/5 session + 文档（U-2） | fail（内部不一致） |
| 17 | 4/5 session + 文档（U-2） | fail（无 5/5） |
| 18 | P-128 维护模式 + 1/5 session（U-2） | pass maintenance（边界外放行） |
| 19 | P-129 维护模式 + 1/5 session（U-2） | fail（边界含 129） |
| 20 | P-128 显式声明 + 文档 + 1/5（U-2） | fail（声明不豁免） |

### 3.6 `spec_runner.py` / `scripts/step_enforce.py`（P-132）

#### 职责

把 runner `step-gate` 的完整性声明从**隐式缺省**改为**显式二选一**，并让所有内部调用方显式表达意图。

#### 接口签名

```python
# spec_runner.py（VERSION 1.10.0 → 1.11.0）
sg.add_argument("--expect", nargs="*", default=None)
sg.add_argument("--legacy", action="store_true")

def cmd_gate_step(args) -> int: ...
def cmd_step_enforce(args) -> int:
    return cmd_gate_step(argparse.Namespace(session=sid, expect=None, legacy=True))

# scripts/step_enforce.py
def _run_gate(sid: str, expect: tuple[str, ...] | None = None) -> int:
    cmd = [sys.executable, str(RUNNER), "step-gate", "--session", sid]
    cmd += ["--expect", *expect] if expect else ["--legacy"]
```

#### 实施要点

- 三重守卫：`--expect` 空列表 ⇒ exit 2；`--expect` 与 `--legacy` 同给 ⇒ exit 2；两者都缺 ⇒ exit 2（提示「必须显式声明」）；
- legacy 模式输出 `mode=legacy 已登记 n/5 步`，明确「仅内部一致性，未声明完整链」；
- 解析错误（坏 JSON）仍在声明守卫之前抛出，保持 F38 的「`<路径>:<行号>` + exit 1」不变；
- selftest 新增 F80（无声明 → exit 2）/ F81（双声明 → exit 2）；既有 18 处 `step-gate` 调用全部补 `--legacy` 或保留 `--expect`；
- `scripts/step_enforce.py` 的内部一致性检查显式传 `--legacy`；完整链检查传五个 step_id；
- 不触碰 decision schema、事件写入路径与 `cmd_gate_step` 的三类校验规则。

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---|---|
| 每次调用重复解析 argv | 单次 argparse，守卫为 O(1) |
| 为 legacy 另写校验路径 | 复用同一 `_decision_chain`，仅跳过 `--expect` 比对 |

### 3.7 `.github/workflows/ci.yml`（P-134）

#### 职责

把 step-enforce step 从 fail-open（`|| true` 吞 git diff 失败 ⇒ 空 FILES ⇒ 绿灯）改为 **fail-closed**，与 step_enforce 的 I-6（exit 2 fail-closed）语义对齐。

#### 实施

```yaml
- name: 决策流批次强制（step-enforce，merge-base 变更集）
  shell: bash
  run: |
    set -eo pipefail
    if [ "${{ github.event_name }}" = "pull_request" ]; then
      BASE="${{ github.event.pull_request.base.sha }}"
    else
      BASE="${{ github.event.before }}"
    fi
    if [ -z "$BASE" ] || [ "$BASE" = "0000000000000000000000000000000000000000" ]; then
      if git rev-parse --verify --quiet "HEAD^" >/dev/null 2>&1; then
        BASE="HEAD^"
      else
        BASE="HEAD"
      fi
    fi
    if ! FILES=$(git diff --name-only "$BASE"...HEAD -- 'spec/**' 'tools/spec_runner/sessions/**' 'docs/PROGRESS.md'); then
      echo "step-enforce: git diff failed for base $BASE (fail-closed)" >&2
      exit 1
    fi
    if [ -n "$FILES" ]; then
      python scripts/step_enforce.py --base "$BASE" $FILES
    else
      echo "step-enforce: no changed gate files"
    fi
```

#### 实施要点

- `set -eo pipefail` 为**自文档化冗余**：GitHub Actions `shell: bash` 官方默认已含 `-eo pipefail`（T2 双源证实），显式写出只为可读性，不构成行为变更；
- 空 FILES 绿灯仅在 `git diff` 成功后成立——失败路径显式 `exit 1`（P-130 的 `|| true` 形态移除）；
- 根提交 / 孤儿分支：before 为全零空树时，有父提交取 `HEAD^`，无父（根提交）取 `BASE=HEAD` ⇒ 三点空 diff ⇒ 显式绿灯，不崩溃；
- force-push 非祖先 base ⇒ 三点 diff 无 merge-base ⇒ 红（有意 fail-closed 新红边）；
- 仍由 git 自算变更集，不引入第三方 changed-files action（CVE-2025-30066）。

#### 本地注入测试（5 例）

注入方式：从 ci.yml 提取真实 run 块，GitHub 表达式换环境变量、`step_enforce.py` 调用换 echo 桩，在临时 git 仓以 git-bash 执行（注意：PATH 上默认 bash 为 WSL，须显式使用 `Git\bin\bash.exe` 并做 Windows→POSIX 路径转换）。

| # | 场景 | 期望 | 结果 |
|---|---|---|---|
| 1 | 坏 base（不存在引用） | `exit 1` 且输出含 `fail-closed` | ✅ |
| 2 | 变更集为空 | `exit 0`，不调用门禁 | ✅ |
| 3 | 根提交（无 `HEAD^`，before 全零） | `BASE=HEAD` 回退，`exit 0` | ✅ |
| 4 | push：before + 变更集含门禁路径 | 门禁桩被调用 | ✅ |
| 5 | PR：`pull_request.base.sha` + 变更集含门禁路径 | 门禁桩被调用 | ✅ |

5/5 通过（P-134，零回归限定见 DESIGN §8 U-10 F 注记）。

### 3.8 `scripts/step_enforce.py` 内容 digest 绑定（P-137）

#### 职责

为 P ≥ `EVIDENCE_MIN_P` 的显式声明提供「finalize 记录的字节 = 提交的字节」机械校验，并提供生成侧入口，使 digest 由工具算出而非人工书写。

#### 接口签名

```python
EVIDENCE_MIN_P = 137            # 独立常量（不并入 129 / 92）
DOC_DIGEST_ALGO = "sha256"

def _norm_bytes(data: bytes) -> bytes: ...                       # CRLF → LF
def _read_doc_bytes(rel, base, worktree=False) -> bytes | None: ...
def _digest_scope(features) -> list[str]: ...                    # FEATURE_RE 口径
def doc_digest(features, base=None, worktree=False) -> dict: ...
def _finalize_decisions(sid) -> list[dict]: ...
def verify_digests(d: Decision, rows: dict, base: str | None) -> tuple[int, list[str]]: ...
```

CLI：`--doc-digest FEATURE`（`action="append"`，可重复）⇒ 打印 `{algorithm, files}` 块并 exit 0；读失败 exit 2。

#### 实施要点

- **单一实现**：生成（`--doc-digest`）与校验（`verify_digests`）共用 `doc_digest`，测试也调用 CLI 生成，**不重算 sha256**（守「两实现漂移」教训）；
- **读面分工**：生成侧读工作树；校验侧本地读 **index**（`git show :path`，即将提交内容）、CI 读工作树（`--base`）——与 `_read_progress` 的 INDEX/WORKTREE 分工同源（I-8）；
- **作用面**：仅在 `resolve` **无错**后执行（避免错误叠加）；模式 ∈ {batch, session, branch}；PID 数 ≥ 137；session = 已判定 5/5 的最新一个；只读**末次** finalize；
- **四类错误**：块缺失/非法、文件集不一致、逐文件哈希不等（验后改文档）、rebind 缺原因（≥2 次 finalize 且末次 `rebind_reason` 空）；
- **不改 runner**：不新增子命令、不触碰 decision schema / 事件写入路径 / `cmd_gate_step`；
- **输出**：通过时追加一行 `digest_bound=<n>`（仅在有校验时输出，历史批次输出零变化）。

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---|---|
| 每 session 调一次 runner | 复用 `_check_sessions` 已得的 complete 列表，零额外 runner 进程 |
| 全仓 session 扫描找 digest | 只读声明 P 的最新 session 文件（单文件流式读） |
| 逐文件 `git show` 重复启动 | 每个 feature 四文档各一次（上限 4×feature 数）；CI 模式改为直接读盘 |
| 校验与生成两套哈希逻辑 | 单函数 `doc_digest`，出参即入参形态 |

#### 注入测试（8 例，落于 `tests/test_batch_binding.py`）

| # | 场景 | 期望 | 结果 |
|---|---|---|---|
| 21 | P-137 + 正确 digest | pass + `digest_bound=1` | ✅ |
| 22 | P-137 缺 `evidence_digest` | exit 1 | ✅ |
| 23 | digest 记录后改同一文档并提交 | exit 1（digest 不匹配） | ✅ |
| 24 | finalize 后新增四文档 | exit 1（文件集不一致） | ✅ |
| 25 | rebind 无 `rebind_reason` | exit 1 | ✅ |
| 26 | rebind 有原因 | pass（仍判 5/5） | ✅ |
| 27 | P-136 无 digest + 文档改动 | pass（历史不重验） | ✅ |
| 28 | 无文档改动（session-progress / batch-registration） | pass（不校验） | ✅ |

8/8 通过（P-137）；`python -m unittest tests.test_batch_binding` 28/28；`spec_runner selftest` 83/83（runner 未改动）。

### 3.9 真实 runner 集成回归（P-139 / P1-1）

**配置面（唯一生产改动）**：`.pre-commit-config.yaml` 的 `blackbox-tests.files` 追加 `tools/spec_runner/spec_runner\.py`——改造前单独改 runner 不触发任何本地 hook（RESEARCH §13.1 / A-43）。`entry` 与 CI step 零改动（同入口 = I-10b）。

**夹具 `tests/harness.py`**：

| 函数 | 作用 |
|---|---|
| `make_repo(prefix, progress=None, mutate=None)` | 建 temp 仓 + 复制 `step_enforce` / `spec_map` / `spec_runner` + 初始 commit；`mutate=(rel, needle, repl)` 只改 temp 副本，且断言 needle 唯一命中 |
| `write_session(root, sid, n=5, anchor=...)` | 写 decision JSONL（八字段 + `metadata.step_id/step_seq/evidence`；finalize 带 `upstream_impact: none`） |
| `run_cli(root, rel, *args)` | 注入 `SR_SESSIONS_DIR` / `SR_REWORK_REGISTRY` / UTF-8 后的真实子进程调用 |

**集成用例（10 例，`tests/test_runner_integration.py`）**：step-gate 完整链 pass / 缺步硬红 / 无显式声明 exit 2 / legacy 内部一致；verify-anchor 真实 pass（含 `--detail`）/ 文件缺失硬红；fork 前缀复制；anchor-audit 不变量成立；backflow-audit 零待处理；**parity guard**（hook 触发面含 runner + CI 跑同一 `unittest discover`）。

**变异用例（4 例，`tests/test_runner_mutation.py`）**：M1 完整链检查 / M2 静态最新 P / M3 gate 硬失败 / M4 锚点路径解析——探针见 RESEARCH §13.3，判定式 = `原版 exit ≠ 变异版 exit`。

**读数**：新增 **14/14 PASS**；全套 `unittest discover` **36 → 50**；增量 **8.7 s**（全套 39.6 s）；`pre-commit run blackbox-tests --files tools/spec_runner/spec_runner.py` = **Passed**（触发面实证）。

### 3.10 CI 逐提交遍历（P-140 / U-11 前置）

#### 职责

把 CI step-enforce 的变更集构造从「`BASE...HEAD` 一次 diff」改为「**逐提交** `C^ → C`」，使远端判定面与本地 hook 的逐提交语义一致（DESIGN §14.2 / I-11a~c），并消除两类结构性假红（RESEARCH §14.1）。

#### 实施要点

| # | 要点 | 位置 |
|---|---|---|
| 1 | `BASE` 取法沿用（PR = `base.sha` / push = `before`；零或缺失 ⇒ `HEAD^` 回退，仍缺 ⇒ `HEAD`） | step 前段 |
| 2 | `COMMITS=$(git rev-list --reverse "$BASE..HEAD")`；取表失败 ⇒ `exit 1`（fail-closed） | 同上 |
| 3 | 合并提交跳过：`git rev-list --parents -n 1 "$C"` 词数 > 2（变更 = 父提交并集） | 循环头 |
| 4 | 根提交跳过（无 `C^`）；`git checkout -q -f "$C"` 后按 `C^ → C` 求路径过滤集（失败 ⇒ exit 1） | 循环体 |
| 5 | 空变更集跳过（不调门禁，计数不加） | 循环体 |
| 6 | **执行器能力分派**：`grep -q 'add_argument("--base"' scripts/step_enforce.py` ⇒ 传 `--base "$PARENT"`；否则按原调用约定（P-130 前版本无 `--base`） | 循环体 |
| 7 | `trap 'git checkout -q -f "$HEAD_SHA"' EXIT`：step 结束恢复 PR 头，后续 step 不受影响 | step 头 |
| 8 | `echo` 受判提交数（观测面，不参与判定） | step 尾 |

#### 低效操作排除

- 不引入第三方 changed-files action（CVE-2025-30066 先例，P-130）；路径过滤全由 `git diff --name-only -- 'spec/**' …` 完成；
- 不重复 checkout 同一提交（`rev-list` 天然去重）；合并/根/空集三条分支在任何 git 操作前短路；
- 实测 16 提交全走查 **8.95 s**（含 6 次历史 runner 子进程），相对同 job 的 `unittest discover`（39.6 s 量级）可忽略；**远端复验（P-141 回填）= run `40579430749` 的 verify job 1m30s 全绿**（8 step 全过）；**`push(main)` 合并面（P-142 回填）= run `40585936395`：merge `adfec33` 被 skip、受判 18 个、墙钟 68 s 全绿**（8 step 全过）；**补充读数（P-143）= run `40589457291`：merge `3bb7680` 被 skip、受判 1 个、墙钟 87 s 全绿**。

#### 形态 guard（`tests/test_runner_integration.py::test_ci_per_commit_walk`）

5 断言：含 `git rev-list --reverse`、含 `git checkout -q -f`、含 `--base` 能力探测、含 `skip merge commit`、**不含** `"$BASE"...HEAD`（回归单次 diff 形态）。只读文本，不执行 CI（P-144 追加第 6 断言：CI 含 `--check-merge`）。

### 3.11 evil merge 检测（P-144 / U-11）

**代码面（1 文件）**：`scripts/step_enforce.py`

| 项 | 内容 |
|---|---|
| 常量 | `JUDGED_PATHS = ("spec/**", "tools/spec_runner/sessions/**", "docs/PROGRESS.md")` —— 与 CI 逐提交过滤同口径（单一实现） |
| 纯函数 | `_parents(sha)` / `_same(ref_a, ref_b, path)`（`git diff --quiet`：0=同 / 1=异 / 其它=None） |
| 入口 | `check_merge(sha)` —— 非合并 ⇒ exit 0（打印说明）；逐受判路径比较两父，**两父皆无** ⇒ 打印路径 + exit 1；git 失败 ⇒ exit 2（fail-closed） |
| CLI | `--check-merge <COMMIT>`（子命令式，与 `--doc-digest` 并列；两者互斥） |

**CI 面（1 文件）**：`.github/workflows/ci.yml` 的 step-enforce 段新增**阶段 1**（先于逐提交循环、零 checkout）：

```bash
for C in $COMMITS; do
  if [ "$(git rev-list --parents -n 1 "$C" | wc -w)" -gt 2 ]; then
    python scripts/step_enforce.py --check-merge "$C"
  fi
done
```

- 阶段 1 只读 git 对象、不动工作树 ⇒ 与阶段 2（逐提交 checkout）无耦合；
- 逐提交循环对 merge 的 `skip` 保留（其并集 diff 仍是假红面），注释改为「evil 内容已由阶段 1 兜底」；
- 执行器取 CI 自身 checkout（新规则前向生效）；删旗标 ⇒ argparse exit 2 ⇒ 红（无静默旁路）。

**测试面（1 文件 4 例）**：`tests/test_runner_integration.py`

| 用例 | 断言 |
|---|---|
| `test_evil_merge_detected` | 冲突解决写入两父皆无内容 ⇒ exit 1 + stderr 含路径 |
| `test_clean_merge_passes` | 两侧改不同文件 ⇒ exit 0 + `无 evil 内容` |
| `test_merge_equals_first_parent_passes` | 受判路径 = 第一父 ⇒ exit 0 + `0 个受判路径` |
| `test_check_merge_non_merge_commit_is_noop` | 非合并 ⇒ exit 0 + `非合并提交` |

**读数（E1）**：新增 **4/4 PASS**；`unittest discover` **51 → 55**；实验仓交叉验证 `--check-merge <M>` → exit 1、`<C2>` → exit 0（A-49/A-50）。

**远端读数（P-145 登记）**：真实 `push(main)` run `40603730644`（合并提交 `e8154eb`）阶段 1 输出 `无 evil 内容（6 个受判路径均等于某一父）`，阶段 2 `skip merge commit` + 受判 1 个、**88 s** 全绿；PR #61 `verify` **1m12s 通过**（range 仅 1 个非合并提交 ⇒ 阶段 1 循环未命中）。

**远端读数（P-146 登记，第 2 样本）**：run `40660622448`（合并提交 `7bcce12`）阶段 1 再次输出 `无 evil 内容（6 个受判路径均等于某一父）`，阶段 2 skip + 受判 1 个、**89 s** 全绿；PR #62 `verify` **1m20s 通过**（range 同样仅 1 个非合并提交 ⇒ 阶段 1 未命中）。

**远端读数（P-147 登记，第 3 样本）**：run `40663831556`（合并提交 `023e456`）阶段 1 再次输出 `无 evil 内容（6 个受判路径均等于某一父）`，阶段 2 skip + 受判 1 个（`mode=batch pid=P-146`、`digest_bound=1`）、**66 s** 全绿；PR #63 `verify` **1m25s 通过**（range 同样仅 1 个非合并提交 ⇒ 阶段 1 未命中）。

## 4. 接口实施

### 4.1 `parse_progress_rows`

```python
def parse_progress_rows(text: str) -> dict[str, dict]:
    rows = {}
    for line in text.splitlines():
        m = PROGRESS_ROW_RE.match(line)
        if not m:
            continue
        pid = m.group(1)
        status = m.group(4).replace("*", "").strip()
        features = tuple(dict.fromkeys(SPEC_LINK_RE.findall(line)))
        rows[pid] = {"status": status, "features": features}
    return rows
```

**签名一致性**：与 DESIGN §4.1 一致 ✅

### 4.2 `changed_pids`

```python
def changed_pids(old_text: str, new_text: str) -> list[str]:
    old, new = parse_progress_rows(old_text), parse_progress_rows(new_text)
    out = []
    for pid, row in new.items():
        if pid not in old or old[pid]["status"] != row["status"]:
            out.append(pid)
    return out
```

**签名一致性**：与 DESIGN §4.2 一致 ✅

### 4.3 `resolve`

按 DESIGN §3.4 的优先级实现；返回 `Decision`，不直接退出。所有错误写入 `errors`，由 `main` 决定 exit。

## 5. 兼容性

### 5.1 Python 版本兼容

| Python 版本 | 支持 | 说明 |
|---|---|---|
| 3.11+ | ✅ | 与 CI / 本机一致 |
| 3.10 | ⚠️ | 未在 CI 覆盖；仅用 3.10 已有语法 |

### 5.2 依赖兼容

| 依赖组合 | 兼容性 | 验证 |
|---|---|---|
| stdlib + pre-commit 3.x | ✅ | 现有六 hook |
| stdlib + GitHub Actions windows-latest | ✅ | 官方 bash 可用 |

### 5.3 向后兼容

- `spec_map.build_pid_map` / `is_historical_exempt` 签名与语义不变；
- `console_gen` 继续使用 `build_pid_map`，不受影响；
- `spec_runner.py step-enforce --pid`（P-024 子命令，独立实现）不受影响；`scripts/step_enforce.py` 的 hook 入口不再提供 `--pid`，改为 argv 变更集 / `--base`；
- P<129 的历史 session 不被追溯判红（只在维护 / session-only 放宽）；
- 语义性文档改动仍必须声明——这是 P0 修复，不是兼容性回归；
- **runner `step-gate` 的隐式 legacy 是显式断裂（P-132）**：无 `--expect` / `--legacy` 的旧调用现在 exit 2；仓内调用面已全量迁移（`scripts/step_enforce.py` + runner 自身 `step-enforce` + selftest 18 处），README 同步；外部调用方须补声明，这是有意的 fail-closed。
- **digest 绑定是新增面（P-137）**：`step_enforce` 新增 `--doc-digest`（纯读、零副作用），P < 137 的批次与无文档改动模式行为零变化；历史 session 永不重验（per-batch 作用域）。失败时的修法 = 重新生成 digest + rebind（受控回边 + 再入 finalize + 原因），无需重写 session。

## 6. 错误处理实施

| 错误场景（DESIGN §7） | 异常类型 | 处理代码 | 测试 |
|---|---|---|---|
| 无声明语义改动 | 无异常，返回 1 | `resolve` errors | #3 |
| 新 P 行 0 链接 | 无异常，返回 1 | `resolve` errors | #8 |
| feature 未覆盖 | 无异常，返回 1 | `resolve` errors | #10 |
| 声明无 5/5 session | 无异常，返回 1 | `check_sessions` | #2 |
| 新 P 行无 session | 无异常，返回 1 | `check_sessions` | #2 |
| 只改 session 1/5 | 无异常，返回 0 | `session-progress` | #11 |
| 只加 P 行 | 无异常，返回 0 | `batch-registration` | #12 |
| git 读取失败 | 捕获 `OSError` / 非零 | `main` 返回 2 | 手工注入 |
| 无相关变更 | 无异常，返回 0 | `main` | 现有 no-arg 测试 |
| step-gate 未显式声明（P-132） | 无异常，返回 2 | `cmd_gate_step` 守卫 | runner F80 |
| step-gate `--expect` / `--legacy` 同给（P-132） | 无异常，返回 2 | `cmd_gate_step` 守卫 | runner F81 |
| P≥137 finalize 缺/非法 `evidence_digest`（P-137） | 无异常，返回 1 | `verify_digests` errors | #22 |
| digest 键集 ≠ 四文档集（P-137） | 无异常，返回 1 | `verify_digests` errors | #24 |
| digest 哈希不等（验后改文档，P-137） | 无异常，返回 1 | `verify_digests` errors | #23 |
| rebind 无 `rebind_reason`（P-137） | 无异常，返回 1 | `verify_digests` errors | #25 |
| digest 生成侧读文档失败（P-137） | 无异常，返回 2 | `main --doc-digest` | 手工注入 |

## 7. 不变式实施

| 不变式（DESIGN §8） | 实施位置 | 验证方式 |
|---|---|---|
| I-1 无声明不放行语义改动 | `resolve` | #3 / #6 |
| I-2 声明必须可解析 | `resolve` + `parse_progress_rows` | #8 |
| I-3 覆盖闭合 | `resolve` | #7 / #10 |
| I-4 完整性按边界 | `check_sessions` | #2 / #11 |
| I-5 维护模式不冒充完成 | `resolve` + 输出 | #6 |
| I-6 exit 2 fail-closed | `main` | 手工注入 |
| I-7 不依赖文件名排序 | `sessions_for_pid` + 扫描 | #9 |
| I-8 本地/CI 同源 | `main --base` | CI step + 本地 hook |
| I-9a 绑定存在（P-137） | `verify_digests` | #21 / #22 |
| I-9b 内容一致（P-137） | `doc_digest` + `verify_digests` | #23 / #24 |
| I-9c rebind 留因（P-137） | `verify_digests` | #25 / #26 |
| I-9d 历史不重验（P-137） | `_pid_num < EVIDENCE_MIN_P` + per-batch 作用域 | #27 |
| I-9e 失败不静默（P-137） | `verify_digests` errors / exit 2 | #22 / 读取失败 |

## 8. 测试策略

### 8.1 单元测试

| 模块 | 测试文件 | 测试数 | 覆盖率目标 |
|---|---|---|---|
| `spec_map` | `tests/test_batch_binding.py` | 28（含集成） | 关键分支全覆盖 |
| `step_enforce`（模式 / 覆盖 / 完整性） | 同上 | 20 | 关键分支全覆盖 |
| `step_enforce`（digest 生成 / 校验，P-137） | 同上 | 8 | 六臂 + 作用域漂移 + 双无文档模式 |
| `spec_runner step-gate` | `spec_runner.py selftest` | 83（含 F80/F81） | 声明守卫 + 既有三臂回归 |
| `spec_runner` CLI 集成（P-139） | `tests/test_runner_integration.py` | 10 | step-gate 四态 / verify-anchor 两态 / fork / 两审计 / 触发面 parity |
| 变异可感知（P-139） | `tests/test_runner_mutation.py` | 4 | M1~M4 各使判定翻转（I-10a） |
| `ci.yml` step-enforce 段（P-134） | 临时 git 仓注入（IMPLEMENTATION §3.7） | 5 | fail-closed 两红边 + 三绿灯边 |

### 8.2 集成测试

临时 git 仓 + 真实 `spec_runner.py`；每个用例独立 commit，零写入真实仓。

### 8.3 属性测试（如适用）

不引入 hypothesis；用 12 例矩阵覆盖模式与失败分支。

## 9. 幻觉抑制审查（Step 6 Review）

### 9.1 依赖版本验证

- [x] 无新增 PyPI / npm 依赖
- [x] 仅使用 Python 3.11 stdlib 与 git 官方命令
- [x] 未虚构库或函数

### 9.2 接口签名验证

- [x] `parse_progress_rows` / `changed_pids` / `resolve` / `check_sessions` 与 DESIGN §4 一致
- [x] 所有签名可实现（无不可能类型组合）

### 9.3 实施与设计对齐

- [x] 每个模块对应 DESIGN §3.2
- [x] 每个接口对应 DESIGN §4
- [x] 无设计未覆盖的实施

### 9.4 低效操作排除

- [x] 一次解析 PROGRESS，不逐 feature 重扫
- [x] 只对候选 PID 调 runner
- [x] 单次 git diff 取变更集

> **Review 声明（RULE-4）**：单 Agent 自查（单视角）；故障注入结果见 CHECKLIST §2。

## 10. 实施步骤

### Step 1: `spec_map` 扩展

- 文件: `scripts/spec_map.py`
- 内容: 新增 `PROGRESS_ROW_RE` / `SPEC_LINK_RE` / `parse_progress_rows` / `changed_pids`
- 测试: `test_batch_binding.py` 的 P 行解析与声明用例

### Step 2: `step_enforce` 重写

- 文件: `scripts/step_enforce.py`
- 内容: 模式解析、覆盖、完整性、维护模式、exit 语义
- 测试: 20 例矩阵

### Step 3: hook 与 CI

- 文件: `.pre-commit-config.yaml` / `.github/workflows/ci.yml`
- 内容: files 正则 + fetch-depth 0 + 变更集
- 测试: 本地 `pre-commit run --all-files`；CI 远端

### Step 4: 本批自证

- 文件: `spec/framework-deep-review/RESEARCH.md` / `DESIGN.md` / `IMPLEMENTATION.md` / `CHECKLIST.md` + P-130 row + session
- 内容: 用新门禁验本批；P-130 5/5
- 测试: `step_enforce.py --base HEAD`（或 pre-commit 自动）

### Step 5: runner 声明面（P-132）

- 文件: `tools/spec_runner/spec_runner.py` / `scripts/step_enforce.py` / `tools/spec_runner/README.md`
- 内容: `step-gate` 三重声明守卫 + selftest F80/F81 + 内部调用方显式 `--legacy`
- 测试: `spec_runner.py selftest` 83/83；`python -m unittest discover -s tests` 28/28

### Step 6: 内容 digest 绑定（P-137）

- 文件: `scripts/step_enforce.py` / `tests/test_batch_binding.py`
- 内容: `doc_digest`（gen/verify 单一实现）+ `verify_digests`（per-batch 作用域）+ `--doc-digest` CLI + `EVIDENCE_MIN_P = 137`
- 测试: `python -m unittest tests.test_batch_binding` 28/28；`python -m unittest discover -s tests` 36/36；`selftest` 83/83 零回归
- 本批自证: `python scripts/step_enforce.py --doc-digest framework-deep-review` → 写入 `specwf-p137-20261027` 的 finalize `metadata.evidence_digest`

### Step 7: 真实 runner 集成回归（P-139）

- 文件: `.pre-commit-config.yaml` / `tests/harness.py` / `tests/test_runner_integration.py` / `tests/test_runner_mutation.py`
- 内容: `blackbox-tests.files` 补 runner + 共享夹具 + 集成 10 例 + 变异 4 例
- 测试: 新增 14/14 PASS；`python -m unittest discover -s tests` 36 → 50；`selftest` 83/83 零回归
- 触发面自证: `pre-commit run blackbox-tests --files tools/spec_runner/spec_runner.py` → Passed

### Step 8: CI 逐提交遍历（P-140）

- 文件: `.github/workflows/ci.yml` / `docs/PROGRESS.md`（P-127 行补 feature 链接）/ `tests/test_runner_integration.py`
- 内容: step-enforce 段改为 `rev-list --reverse` 逐提交 + `git checkout -f` + 执行器能力分派 + 合并提交跳过 + `trap` 恢复
- 数据: P-127 行补 `spec/graph-structure-upgrade/` 链接（全表唯一无 feature 链接的行；派生视图零变化）
- 测试: `test_ci_per_commit_walk` 5 断言；真实历史 16 提交走查 `EXIT=0`（含 P-137/P-138/P-139 `digest_bound=1`）

---

**Review 签字**: 单 Agent 自查（单视角） 日期: 2026-10-27
