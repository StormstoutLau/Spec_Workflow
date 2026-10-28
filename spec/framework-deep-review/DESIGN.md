# 设计文档：批次绑定门禁（O3 Phase 1）

---

id: framework-deep-review-DESIGN
type: design
version: 1.17
status: draft
date: 2026-10-26
depends: [framework-deep-review-RESEARCH]
upstream: null

---

> **Feature**: framework-deep-review（U-1 / O3 Phase 1 门禁实施）
> **创建日期**: 2026-10-26
> **修订**: v1.1（2026-10-26，P-131：U-2 边界裁决 129 + §8 边界语义注记）
> **修订**: v1.2（2026-10-26，P-132：runner `step-gate` 显式声明面——`--expect` / `--legacy` 二选一，隐式 legacy 移除）
> **修订**: v1.3（2026-10-26，P-134：U-10 F 实施注记（§8）——CI step-enforce 段 fail-closed 化 + 两红边；C 留 P-135 候选）
> **修订**: v1.4（2026-10-27，P-137：U-10 C 实施设计（§12）——内容 digest 绑定：finalize 时点 / per-batch 作用域 / rebind 留因 / `EVIDENCE_MIN_P=137` / `--doc-digest` 生成侧；不改 runner schema）
> **修订**: v1.5（2026-10-27，P-139：P1-1 真实 runner 集成回归设计（§13）——触发面补 runner + 集成用例 + 四类变异体 + 不变式 I-10；零行为变更）
> **修订**: v1.6（2026-10-27，P-140：CI 逐提交判定面（§14）——逐提交变更集 + 执行器随提交 + 合并提交跳过 + 不变式 I-11a~c；零脚本行为变更）
> **修订**: v1.7（2026-10-28，P-141：CI 远端读数回填——§14.6 补远端首次实测〔run `40579430749` / verify 1m30s 全绿〕；设计面零变更）
> **修订**: v1.8（2026-10-28，P-142：`push(main)` 合并面读数回填——§14.6 补真实合并提交走查〔run `40585936395` / merge `adfec33` skip + 受判 18 个 / 68 s 全绿〕；设计面零变更）
> **修订**: v1.9（2026-10-28，P-143：`push(main)` 补充读数——§14.6 补第 2 样本〔run `40589457291` / merge `3bb7680` skip + 受判 1 个 / 87 s 全绿〕；设计面零变更）
> **修订**: v1.10（2026-10-28，P-144：**U-11 合并面关闭**——新增 §14.7 evil merge 判定面〔= 两父皆无 ⇒ 判红；= 任一父 ⇒ 不判〕+ 不变式 I-11d / I-11e + 三替代方案否决；CI 新增阶段 1 检测）
> **修订**: v1.11（2026-10-28，P-145：**阶段 1 远端读数登记**——§14.7 补真实 `push(main)` 读数（run `40603730644` / 合并提交 `e8154eb` / `无 evil 内容（6 个受判路径均等于某一父）` / 88 s 全绿）；设计面零变更）
> **修订**: v1.12（2026-10-28，P-146：**阶段 1 远端第 2 样本**——§14.7 补 run `40660622448`（合并提交 `7bcce12` / 同为 6 个受判路径 / 89 s 全绿）；设计面零变更）
> **修订**: v1.13（2026-10-28，P-147：**阶段 1 远端第 3 样本**——§14.7 补 run `40663831556`（合并提交 `023e456` / 同为 6 个受判路径 / 66 s 全绿）；设计面零变更）
> **修订**: v1.14（2026-10-28，P-148：**阶段 1 远端第 4 样本**——§14.7 补 run `40666293529`（合并提交 `fb01568` / 同为 6 个受判路径 / 82 s 全绿）；设计面零变更）
> **修订**: v1.15（2026-10-28，P-149：**阶段 1 远端第 5 样本**——§14.7 补 run `40676513311`（合并提交 `64c6313` / 同为 6 个受判路径 / 81 s 全绿）；设计面零变更）
> **修订**: v1.16（2026-10-28，P-150：**PR 面读数订正 + evil 侧路径裁决**——§14.7 补订正段（PR 面 HEAD = 合成 merge ref ⇒ 阶段 1 恒命中）；新增 §14.8 裁决 = 路径 2（分支内构造合并提交 → 失败 PR）作为 evil 侧唯一取证路径；设计面判据不变）
> **修订**: v1.17（2026-10-28，P-151：**evil 侧远端阻断实测**——§14.7 补 A-51 读数（探针 PR #67：阶段 1 exit 1 / verify failure / `mergeStateStatus = BLOCKED` / main 无污染）；I-11d / I-11e 判据不变，仅补「阻断力」远端证据）
> **状态**: 草稿
> **Spec 步骤**: Step 3-4
> **基于调研**: [RESEARCH.md](./RESEARCH.md) §11

---

## 1. 设计目标

在不引入新工件、不改变 session schema、不引入第三方 changed-files action 的前提下，让提交门禁回答一个问题：

> 本次变更属于哪个批次，且该批次的 session 是否满足完整性要求？

本设计只实施 U-1 Phase 1（批次识别与门禁），不实施 U-2（runner 内部完整链默认值）与 Phase 2（digest / `session_start`）。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---|---|---|
| 静态 first/max P 都会绑错交叉工具批 | 放弃静态单值；以「本次变更的声明」为主 | RESEARCH §11.5 / A-40 |
| 148 session / 7 个多 session PID；v10<v9 | 不按文件名排序选 session；扫描全部候选 | RESEARCH §11.2 / A-36/A-37 |
| PROGRESS 27 行零链接、§9 13 行非升序 | 新 P 行的链接集作为批次 feature 声明 | RESEARCH §11.6 / A-39 |
| CI 当前验全量文档 | 改为 merge-base 变更集 | RESEARCH §11.6 / A-41 |
| 旧 session 可替代当前批次 | 任何语义性四文档改动必须有声明 | RESEARCH §11.5 |

### 2.2 相关 ADR

| ADR | 决策 | 对本设计的影响 |
|---|---|---|
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 懒加载三问 | 本设计为 Layer-1 门禁改动，必须显式激活并保留回退点 |
| [ADR-0011](../../adr/ADR-0011-step-gate-trigger-dependency-and-theatrical-decision.md) | 决策流门禁 | 沿用 session / step-gate 既有语义，不新建决策格式 |

### 2.3 职责边界

**职责内**：识别当前批次、校验 feature 覆盖、校验 session 完整性、区分维护模式、统一本地 / CI 判定。

**职责外**：不修改 `spec_runner` 的 decision schema；不实现 digest 绑定；不实现跨仓 attestation；不修改 `step-gate` 的规则；不重写历史 session。

## 3. 架构设计

### 3.1 整体架构

```text
pre-commit / CI
  → changed files（docs / sessions / PROGRESS）
  → step_enforce.py
      → ProgressRows（新/旧 PROGRESS）
      → DeclarationResolver（batch / session / branch / maintenance）
      → SessionChecker（调用真实 spec_runner step-gate）
      → Decision(mode, pids, sessions, features, source)
  → exit 0 / 1 / 2 + 机读输出
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|---|---|---|---|---|
| `spec_map.parse_progress_rows` | 解析 P 行、状态、feature 链接 | PROGRESS 文本 | `{P: Row}` | stdlib `re` |
| `spec_map.changed_pids` | 识别新增 P 行 / 状态变更 | 新旧 PROGRESS | PID 列表 | 上者 |
| `step_enforce.resolve` | 模式判定与覆盖检查 | changed files + 新旧 PROGRESS + branch | `Decision` | `spec_map` |
| `step_enforce.check_sessions` | 调用真实 runner 校验 session | session id 列表 | complete/internal 结果 | `spec_runner.py` |
| `step_enforce.main` | 组装、输出、exit code | argv / git | stdout / exit | 上者 |

### 3.3 数据流

1. 归一化路径（Windows `\` → `/`）；
2. 本地模式（无 `--base`）**直接以 git 实际变更集为准**：`暂存 ∪ 工作树改动 ∪ 未跟踪`（仅保留门禁路径）——预提交钩子会**分块传参**，单次 argv 可能只是四文档子集，信 argv 会把同一提交的声明拆散误判；`pre-commit run --all-files` 的全量 argv 亦由此收敛；
3. 从（本地 git / CI argv）变更集分类：四文档 / session / PROGRESS；
4. 读新旧 PROGRESS（本地 `HEAD:` vs `:`；CI `base:` vs working tree）；
5. 计算声明（新 P 行 / 状态变更 / 变更 session / 分支）；
6. 校验声明 P 行的 feature 集覆盖所有变更四文档；
7. 校验 session（内部合法 + 至少一个 5/5，按边界）；
8. 无声明时：仅允许 whitespace-only 维护模式；
9. 输出 `mode / pid / sessions / features / source`，返回 exit。

### 3.4 控制流

- 有文档、有声明 → 严格模式；
- 有文档、无声明 → 维护模式或失败；
- 无文档、有 session → `session-progress`（允许部分链）；
- 无文档、有 P 行 → `batch-registration`（新 P 行必须有链接）；
- 无任何相关变更 → exit 0。

## 4. 接口定义

### 4.1 `spec_map.parse_progress_rows`

```python
def parse_progress_rows(text: str) -> dict[str, dict]:
    """P-xxx -> {"status": str, "features": set[str]}。"""
```

### 4.2 `spec_map.changed_pids`

```python
def changed_pids(old_text: str, new_text: str) -> list[str]:
    """新增 P 行，或 status 列发生变化；按新文本顺序返回。"""
```

### 4.3 `step_enforce.resolve`

```python
@dataclass
class Decision:
    mode: str
    pids: list[str]
    sessions: list[str]
    features: set[str]
    source: str
    errors: list[str]

def resolve(changed_docs, changed_sessions, progress_changed,
            old_progress, new_progress, branch, whitespace_only) -> Decision:
    ...
```

### 4.4 `step_enforce.check_sessions`

```python
def check_sessions(sids: list[str], require_complete: bool) -> tuple[list[str], list[str]]:
    """返回 (complete_sids, errors)。内部合法性对所有 sid 强制。"""
```

## 5. 替代方案

### 5.1 方案 A：O3 混合（选择）

- 描述：新 P 行 > 变更 session > 分支名 > 维护模式。
- 优点：复用现有真值源；无新工件；兼容多 session PID；维护模式不冒充批次完成。
- 缺点：语义性文档改动必须有声明，提交粒度变严。
- 选择理由：唯一能同时满足 P0 修复、成本、兼容与升级潜力的方案。

### 5.2 方案 B：静态最新 P（否决）

- 描述：§9 行取最大 P。
- 否决理由：15/40 行改变；doc-contract / precommit 会被绑到交叉工具批 P-106（RESEARCH §11.5）。

### 5.3 方案 C：独立 manifest（暂缓）

- 描述：每批写 `batches/<P>.json`。
- 否决理由：新增工件与双真相源；当前收益不足以抵消维护成本；留 Phase 3 跨仓阶段。

### 5.4 方案 D：commit trailer（暂缓）

- 描述：footer 写 `Batch: P-130`。
- 否决理由：`pre-commit` 在提交信息之前运行（A-30），不能替代 L1；只可作 CI / commit-msg 补充。

## 6. 数据结构

### 6.1 ProgressRow

```python
@dataclass(frozen=True)
class ProgressRow:
    pid: str
    status: str
    features: tuple[str, ...]
```

### 6.2 Decision

见 §4.3。字段语义：`mode` ∈ {batch, session, branch, maintenance, session-progress, batch-registration}；`source` 记录声明来源（`P-row` / `session` / `branch` / `whitespace`）。

## 7. 错误处理

| 错误场景 | 处理方式 | 用户可见信息 |
|---|---|---|
| 语义性四文档改动、无声明 | exit 1 | `no declaration for changed docs` |
| 新 P 行 0 个 spec 链接 | exit 1 | `P-xxx declares no feature` |
| 变更 feature 不在声明 P 行 | exit 1 | `feature not covered: <f>` |
| 有文档改动的声明无 5/5 session | exit 1 | `incomplete session for P-xxx` |
| 新 P 行无 session | exit 1 | `no session for P-xxx` |
| 只改 session、链不完整 | exit 0 | `session-progress`（允许） |
| 只改 P 行、无文档/session | exit 0 | `batch-registration` |
| git 读取失败 | exit 2 | `git error: ...`（fail-closed） |
| 无相关变更 | exit 0 | `nothing to gate` |
| 全量传参（`--all-files`） | 本地模式以 git 变更集为准，全量 argv 自动收敛 | `mode=...` 同提交态 |
| 分块传参（pre-commit chunk） | 单块缺声明文件不影响判定（看整批变更集） | `mode=...` 同提交态 |
| 本地变更集不可计算 | exit 2 | `git error: ...`（fail-closed） |

## 8. 不变式（Invariants）

1. **I-1 无声明不放行语义改动**：任何四文档语义改动必须有 batch/session/branch 声明。
2. **I-2 声明必须可解析**：声明 P 必须存在于 PROGRESS，且至少有 1 个 `spec/<feature>/` 链接。
3. **I-3 覆盖闭合**：每个变更四文档 feature 必须属于声明 P 的 feature 集。
4. **I-4 完整性按边界**：带四文档改动的 batch/session/branch 声明，其 P 必须至少有一个 5/5 session；P<129 仅在无文档的 session-only 与维护模式放宽完整性。
5. **I-5 维护模式不冒充完成**：仅 whitespace-only 放行，输出 `maintenance-only`。
6. **I-6 exit 2 = fail-closed**：pre-commit / CI 均视为失败，不保留「提示不阻断」语义。
7. **I-7 不依赖文件名排序**：扫描全部候选 session，v10/v9 不参与选择。
8. **I-8 本地/CI 同源**：同一 `resolve` 逻辑，仅输入来源不同（index vs base...HEAD）。

> **U-2 裁决（2026-10-26，P-131）**：`BATCH_BINDING_MIN_P = 129`。该边界**只适用于维护模式与仅登记模式**；显式 batch/session/branch 声明带文档改动一律要求 ≥1 个 5/5，**不因 P<129 豁免**——否则旧的不完整 session 可借旧 P 行放行新语义改动。runner 的 `FINALIZE_IMPACT_MIN_P = 92` 是 finalize 字段专项边界，**不与本边界合并**。注入测试：0/5、4/5、P-128 维护放行、P-129 维护判红、P<129 显式声明仍须 5/5。

> **U-2 声明面（2026-10-26，P-132）**：runner `step-gate` 的完整性声明改为**显式二选一**——`--expect <steps>`（校验完整链）或 `--legacy`（仅校验已登记链内部一致性）；两者都缺 ⇒ exit 2，两者同给 ⇒ exit 2，`--expect` 空列表 ⇒ exit 2。**隐式 legacy 已移除**：原默认行为让「忘记声明完整链」与「有意 legacy」在机械读数上不可区分，违反本仓「声明 = 重数」纪律。所有内部调用方（`scripts/step_enforce.py` 的内部一致性检查、runner `step-enforce` 子命令）改为**显式传 `--legacy`**，不依赖缺省。该改动只调整 CLI 声明面，**不触碰 decision schema / 事件写入路径**。

> **U-10 F 裁决实施（2026-10-26，P-134）**：CI step-enforce 段 **fail-closed 化**（`.github/workflows/ci.yml`）——移除「`|| true` 吞 git diff 失败 ⇒ 空 FILES ⇒ 绿灯」的 fail-open 形态，diff 失败显式 `exit 1`，与 I-6 对齐。`set -eo pipefail` 为**自文档化冗余**：GitHub Actions `shell: bash` 官方默认已含 `-eo pipefail`（T2 双源证实），显式写出只为可读性。**两个新红边（有意 fail-closed）**：① 根提交 / 孤儿分支——before 为全零空树时回退，有父提交取 `HEAD^`，无父取 `BASE=HEAD`（三点空 diff ⇒ 显式绿灯，不崩溃）；② force-push 非祖先 base ⇒ 三点 diff 无 merge-base ⇒ 红。**零回归限定**：20 例批次绑定 / runner selftest 83 / unittest 28 零回归；新增 2 个 CI 失败边不属回归，本地注入 5/5（坏 base 红 / 无变更绿 / 根提交不误伤 / push 与 PR 有变更均进门禁）。**C（digest 门禁）不并入本批**：另批 P-135 候选，三处未决预注册——digest 计算时点（finalize vs 校验时）、per-batch rebind、边界 `EVIDENCE_MIN_P=135`（沿用 U-2 边界步进惯例）；`session_start` 留 Phase 2b。裁决全文见 RESEARCH §10（v1.6）。

## 9. 幻觉抑制审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 所有设计决策可追溯到 RESEARCH §11 / A-29~A-42
- [x] 无未经验证的假设（`v10<v9`、148 session、15/40 均为实测）
- [x] 无「声明即事实」：所有模式均有机械判据

### 9.2 替代方案审查

- [x] 至少列 4 个替代方案
- [x] 每个替代方案有明确否决 / 暂缓理由

### 9.3 职责边界审查

- [x] 不修改 decision schema、不新增门禁类型、不改历史 session
- [x] 不把「分支名」当强声明，仅作弱回退

> **Review 声明（RULE-4）**：本轮为单 Agent 自查（单视角），非异基座独立 pass；高风险项（exit 语义、legacy 边界）已在 DESIGN 与 CHECKLIST 中登记，待实施后以故障注入复核。

## 10. 对实施的输入

### 10.1 关键工程约束

- 仅 stdlib；Python 3.11+；Windows/Linux 双平台路径归一化。
- `step_enforce.py` 必须能在 pre-commit（index）与 CI（base...HEAD）两种模式运行。
- 不引入 `dorny/paths-filter` 或 `tj-actions/changed-files`；用 git 自算变更集。
- `spec_runner.py` 只作为只读被调用方，不修改其 decision schema。
- 允许调整 runner 的 `step-gate` CLI 声明面（P-132：显式 `--expect` / `--legacy`），但不得触碰 decision schema 与事件写入路径。

### 10.2 风险与缓解

| 风险 | 缓解措施 |
|---|---|
| 维护模式被滥用 | 仅 whitespace-only；语义改动必须声明 |
| 分支名误绑 | 分支名仅弱回退，且 P 行必须存在、feature 必须覆盖 |
| 多 feature 批次漏检 | P 行链接集 + 并集覆盖检查 |
| 旧批次被新规则误伤 | P<129 仅在无文档的 session-only / 维护模式放宽；带文档改动仍要求完整，避免旧 session 替身 |
| CI 变更集为空 | `git diff` 成功且为空 ⇒ exit 0；空 before / 根提交回退 `HEAD^`，无父提交则 `BASE=HEAD`（P-134）；diff 失败 ⇒ exit 1（fail-closed） |

## 11. 未决项登记（四元块）与决策矩阵

- **U-1 「新 P 行」判定语义**
  - **判据**：新增行 / status 变更是否足以区分「新批次」与「文案订正」；
  - **触发条件**：首个非新增但改 P 行的真实提交；
  - **当前倾向**：新增行或 status 变化算；纯描述修改不算；
  - **证据等级**：E1（P-125/P-127 实践）。

- **U-2 维护模式的 whitespace 判定**
  - **判据**：`git diff -w --ignore-blank-lines` 为空是否覆盖行尾归一与纯空白；
  - **触发条件**：首个维护模式提交；
  - **当前倾向**：是；非空白 typo 必须声明；
  - **证据等级**：待实测。

- **U-3 多 PID 提交的聚合**
  - **判据**：一个提交声明多个 P 时，是否要求每个 P 都有完整 session；
  - **当前倾向**：是；
  - **触发条件**：首个多 PID 批次；
  - **证据等级**：待实测。

**决策矩阵**：不启用（本设计为 Type-2 可逆门禁改动，先做再改）。

## 12. U-10 C：内容 digest 绑定（P-137）

> **定位**：本设计的第一阶段（§1）明确声明「不实现 digest 绑定」；U-10 裁决把 C 拆为另批（RESEARCH §10 / 附录 E.1），本批实施。§12 = 该子项的设计，**不改变 §1~§11 的既有语义**。

### 12.1 设计目标与职责边界

**解决**：`finalize` 记录的证据内容，是否就是**提交出去的内容**？（`verify-anchor` 只验锚点位置可达，不验内容字节。）

**职责内**：在 `scripts/step_enforce.py` 内新增 digest 生成与校验，作用于 batch / session / branch 三种显式声明。

**职责外**：不改 `spec_runner` 的 decision schema 与事件写入路径（`metadata` 为自由字段，沿用 `upstream_impact` 先例）；不新增 session 事件类型；不新增工件（无 manifest / 无 digest 文件）；不改 `.pre-commit-config.yaml` 与 CI 段（触发面已覆盖 `scripts/` 与四文档）；不实现 `session_start`（Phase 2b）。

### 12.2 三项设计决策（承 RESEARCH §12.2 的 R1/R2/R3）

| 决策 | 取值 | 否决项与理由 |
|---|---|---|
| 记录时点 | `finalize` 末次 | `verify`——文档终稿晚于 verify（P-130/131/132 同改同一组文档），且 verify 职责是锚点真实性 |
| 作用域 / rebind | per-batch（声明 P 的 feature 集）+ 同 session 内 rebind 须留因 | 全量历史重验（155 批次全红）；跨批原因强制（第二 claim 面，重复 PROGRESS 已记事实） |
| 过渡边界 | `EVIDENCE_MIN_P = 137`（独立常量） | 135 / 136 已被占用；与 129 / 92 合并（语义不同：入口 / 字段 / 内容绑定） |

### 12.3 接口定义

```python
EVIDENCE_MIN_P = 137
DOC_DIGEST_ALGO = "sha256"

def doc_digest(features, base: str | None = None, worktree: bool = False) -> dict:
    """{"algorithm": "sha256", "files": {"spec/<f>/XXX.md": "<hex>"}}；唯一实现。"""

def verify_digests(d: Decision, rows: dict, base: str | None) -> tuple[int, list[str]]:
    """返回 (已绑定 PID 数, 错误)；只作用于 batch / session / branch。"""
```

CLI：`python scripts/step_enforce.py --doc-digest <feature>`（可重复）打印**可直接粘贴**的 digest 块，退出 0；feature 目录缺失 / 读失败 ⇒ 2。

### 12.4 数据流

```text
终稿（工作树） --doc-digest--> metadata.evidence_digest（写入 finalize decision）
提交前门禁（index / CI 工作树） --> verify_digests：
    P < 边界 或 模式 ∉ {batch,session,branch} → 跳过
    声明 P 的最新 5/5 session → 末次 finalize
      缺/非法块 → 红；键集不等 → 红；逐文件哈希不等 → 红（验后改文档）
      ≥2 次 finalize 且末次无 rebind_reason → 红
```

### 12.5 不变式

1. **I-9a 绑定存在**：P ≥ 边界且带四文档改动 ⇒ 末次 finalize 必须有 `evidence_digest`。
2. **I-9b 内容一致**：digest 键集 = 声明 P 的 feature 四文档集；逐文件哈希 = 提交内容。
3. **I-9c rebind 留因**：同 session 多次 finalize ⇒ 末次须带非空 `rebind_reason`。
4. **I-9d 历史不重验**：历史 session 永不因 digest 判红（per-batch 作用域，不靠边界豁免）。
5. **I-9e 失败不静默**：读失败 / 坏 JSON ⇒ 错误入 `errors` ⇒ exit 1 或 2，绝不当作通过。

### 12.6 替代方案

| 方案 | 否决理由 |
|---|---|
| A. `verify` 时点记录 digest | 终稿晚于 verify（实测三提交）⇒ 记录即失效 |
| B. aggregate 单值 digest | 掩盖「哪个文件变了」；无法定位改动 ⇒ 只增 claim 面 |
| C. 独立 digest 文件（manifest） | 新增工件 + 双真相源（§5.3 同结论，留 Phase 3） |
| D. 全量历史 session 重验 | 155 批次无 digest ⇒ 全红（存量零回归破坏） |
| E. 跨批强制 rebind 原因 | 与 PROGRESS 变更理由重复（第二 claim 面） |

### 12.7 风险与回退

| 风险 | 缓解 |
|---|---|
| 手工写错 digest | 生成侧唯一实现（`--doc-digest`），测试用同一实现自算 |
| finalize 后改文档 | I-9b 判红；修法 = rebind（回边 + 再入 finalize + 原因）|
| 维护模式豁免被滥用 | 维护模式本身要求 `git diff -w` 为空 + P≥129 完整链；字节变了其后须 rebind |
| 边界常量误合并 | 三常量语义独立，注释互指（129 入口 / 92 字段 / 137 内容）|

**回退**：`EVIDENCE_MIN_P` 置 9999 ⇒ 整体降为观察（无红、`digest_bound` 不再输出）。

## 13. P1-1 真实 runner 集成回归（P-139）

### 13.1 设计目标与职责边界

让「真实 runner 的行为」进入**提交门禁的常规观测面**：被被测对象（`tools/spec_runner/spec_runner.py`）变更时，其集成测试必须在本地 hook 上运行；且测试对四类已登记缺陷**有感知**（变异可感知），而不是只在全绿时给出存在性安慰。

**职责内**：`.pre-commit-config.yaml` 的 `blackbox-tests` 触发面、`tests/` 下的集成与变异用例。
**职责外**：不改 runner / `step_enforce` / `spec_map` 任何行为；不改 CI workflow（同一入口已存在）；不引入 mock server（runner `selftest` 面）；不做 P1-2「每步执行证据」。

### 13.2 测试形态

| 面 | 形态 | 理由 |
|---|---|---|
| 仓 | 每例独立 temp 仓（`git init` + 初始提交），脚本副本 | 真实 `git show :path` / 工作树语义，零写入真实仓 |
| 注入 | `SR_SESSIONS_DIR` + `SR_REWORK_REGISTRY`（既有先例） | 真实 CLI 路径，不 monkeypatch 内部函数 |
| 会话 | JSONL 直接落盘（decision 八字段 + `metadata.step_id/step_seq/evidence`） | 与 runner `EventWriter` 读取面一致 |
| 变异 | 复制脚本到 temp 后**单点改字**（原字面量须唯一命中） | 源码漂移 ⇒ harness 断言失败，变异体不会静默失配 |
| 触发面 | `blackbox-tests.files` 补 runner | 单独改 runner 必须触发其测试 |

### 13.3 不变式

| # | 不变式 | 验证 |
|---|---|---|
| I-10a | **变异可感知**：§13.4 四类变异体每个至少使一例的判定翻转 | 变异 guard 4 例（M1~M4） |
| I-10b | **同判定面**：本地 hook 与 CI 跑同一入口（`python -m unittest discover -s tests`） | parity guard（读 `.pre-commit-config.yaml` + `ci.yml`） |
| I-10c | **零行为变更**：生产脚本字节不变，只增测试与一条 `files` 正则 | 本批 diff 面（3 新测试文件 + 1 配置行） |

### 13.4 四类变异体（与 RESEARCH §7.3 逐条对应）

M1 删除完整链检查 / M2 改回静态最新 P / M3 吞掉 gate 硬失败 / M4 破坏锚点路径解析 —— 探针与原版/变异版退出码见 RESEARCH §13.3。

### 13.5 替代方案

| 方案 | 判定 | 理由 |
|---|---|---|
| A. 只补触发面（不加用例） | 否决 | 触发面扩了但没有针对性用例，等于把 runner 变更送进旧用例（覆盖率不变） |
| B. 复用 `test_batch_binding` 夹具 | 否决 | 该文件面向 `step_enforce`（批次面），混入 runner 命令面会让失败归因变模糊 |
| C. 新建独立 CI job | 否决 | 与「同判定面」冲突且增 CI 维护面；现有 `unittest discover` 已覆盖 |
| D. 加入 runner `selftest` 作替代 | 否决 | selftest 是内嵌自证（同源），不能替代外置集成（RULE-5 同精神） |

### 13.6 风险与回退

| 风险 | 缓解 |
|---|---|
| 变异体与源码漂移（改 runner 后 needle 失配） | harness 断言「原字面量命中数 == 1」⇒ 立即红并指明变异点 |
| 测试变慢拖累提交 | 增量实测 8.7 s（14 例）；仍属同一步 |
| temp 仓污染真实仓 | 全部路径在 `tempfile.mkdtemp` 下；`addCleanup` 清理 |

**回退**：删 `tests/harness.py` / `tests/test_runner_integration.py` / `tests/test_runner_mutation.py` + 还原 `blackbox-tests.files` 一行 ⇒ 逐字节回到 P-138 后状态。

## 14. CI 逐提交判定面（P-140）

### 14.1 设计目标与职责边界

目标：让 CI 的 step-enforce 段的**变更集构造**与本地逐提交语义一致——每个非合并提交只对该提交自身的变更负责，且判定所用执行器 = 该提交所在时点的版本（RESEARCH §14.1 的两条假红面均由此消失）。

**职责内**：`.github/workflows/ci.yml` 的 step-enforce 段构造方式；一条形态 guard 测试。
**职责外**：不改 `step_enforce` / `spec_map` / `spec_runner` 任何行为；不改其他 CI step；不重写历史（P-127 的数据缺口按**新提交补数据**处理，不动历史提交）。

### 14.2 判定面定义

| 维度 | 本地 hook | CI（本设计） |
|---|---|---|
| 变更集 | 本次提交的 staged 集（`--cached` + 未跟踪） | `git rev-list --reverse BASE..HEAD` 逐提交，再按 `C^ → C` 求路径过滤后的文件集 |
| 旧 PROGRESS | `HEAD`（提交前） | 该提交的父提交 ref（`--base C^`） |
| 执行器 | 工作树当前版本（= 该提交自身版本） | **该提交自身版本**（checkout 到 C 后运行仓内脚本） |
| 合并提交 | 不适用（本地不产生） | 显式跳过（变更 = 父提交并集） |
| 失败语义 | exit 非 0 阻断提交 | 任一提交 exit 非 0 ⇒ step 失败（`set -eo pipefail`） |

### 14.3 不变式

| # | 不变式 | 验证 |
|---|---|---|
| I-11a | **逐提交 = 单一变更集**：每个非合并提交只按自身 diff 判定，绝不把分支并集当作一个提交 | A-46 真实历史 16 提交；合成 merge 实验 |
| I-11b | **执行器随提交**：判定所用门禁脚本取该提交自身版本（无 `--base` 的旧版按原调用约定分派） | 对照实验：HEAD 版执行器复验 P-127 提交 ⇒ 红 |
| I-11c | **合并提交显式跳过**：`git rev-list --parents -n 1` 词数 > 2 即跳过并打印原因 | 合成 merge：17 条中 1 skip、16 受判 |

### 14.4 控制流

1. 取 `BASE`（PR = `base.sha`；push = `before`；零/缺 ⇒ `HEAD^` 回退，仍缺 ⇒ `HEAD`）；
2. `git rev-list --reverse BASE..HEAD` 取有序提交表（失败 ⇒ exit 1，fail-closed）；
3. 逐提交：合并提交跳过 → 根提交跳过 → `git checkout -f C` → 取 `C^` 与路径过滤后的变更文件（失败 ⇒ exit 1）→ 空集跳过 → 按 `scripts/step_enforce.py` 是否声明 `--base` 分派调用；
4. `trap` 保证 step 结束恢复 `HEAD`（同 job 后续 step 仍在 PR 头工作树上运行）；
5. 结束打印受判提交数（观测面，不参与判定）。

### 14.5 替代方案

| 方案 | 判定 | 理由 |
|---|---|---|
| A. HEAD 版执行器 + 逐提交 | 否决 | 追溯施加当时不存在的新规则（P-127 提交在 P-130 规则下变红 = A-46 对照实验） |
| B. 保留 `BASE...HEAD` + 补 P-127 数据 | 否决 | 跨批 digest 面仍在（A-45 ②） |
| C. 只判末提交 | 否决 | 中间批次的声明与 digest 失去校验 |
| D. 按 `spec/<feature>` 目录聚合判定 | 否决 | 同一 feature 多批次共用目录（framework-deep-review = P-128~P-140），无法按目录回推批次 |

### 14.6 风险与回退

| 风险 | 缓解 |
|---|---|
| 逐提交 checkout 拖慢 CI | 实测 **8.95 s**（16 提交全走查，含 6 次历史 runner 子进程）；同 job 的 `unittest discover` 为 39.6 s 量级；**远端首次实测（P-141 回填）= run `40579430749` verify job 1m30s 全绿**；**`push(main)` 合并面实测（P-142 回填）= run `40585936395` 墙钟 68 s 全绿（merge `adfec33` skip + 受判 18 个）**；**补充读数（P-143）= run `40589457291` 墙钟 87 s 全绿（merge `3bb7680` skip + 受判 1 个）** |
| 历史执行器本身有缺陷 | 同判定面优先：本地当时即如此判定；新规则只对**新提交**生效，不回判历史 |
| evil merge 内容不被覆盖 | **P-144 已关闭**：`--check-merge` 只判「两父皆无」的受判路径 ⇒ exit 1（A-49 逃逸实测 / A-50 检测四态）；`push(main)` 面无并集式假红（A-48） |
| checkout 后工作树与 PR 头不一致 | `trap ... EXIT` 恢复 `HEAD_SHA`；后续 step 沿用原工作树 |

**回退**：还原 ci.yml 的 step-enforce 段 ⇒ 回到 P-139 后状态（其余面零改动）。

**Review 签字**: 单 Agent 自查（单视角） 日期: 2026-10-27

### 14.7 evil merge 判定面（P-144 / U-11）

**缺陷**（A-49）：合并提交被逐提交循环跳过（变更 = 父提交并集），冲突解决时手写进去、两父皆无的内容因此**永久逃逸**——同一内容走普通提交 `exit 1`，走合并解决 `exit 0`。

**判定定义**（三值判据，逐受判路径）：

| 合并结果 vs 两父 | 含义 | 判定 |
|---|---|---|
| 等于第一父 | main 侧内容（已被本循环或历史覆盖） | 不判 |
| 等于第二父 | 分支侧内容（已被本循环覆盖） | 不判 |
| **两父皆无** | 冲突解决时手写的新内容（evil） | **exit 1** |

受判路径集与逐提交循环完全一致：`spec/**`、`tools/spec_runner/sessions/**`、`docs/PROGRESS.md`（唯一常量 `JUDGED_PATHS`，单一实现）。

**控制流**（CI 阶段 1，先于逐提交判定）：

```
for C in $COMMITS; do
  if 父数 > 1; then
    python scripts/step_enforce.py --check-merge "$C"   # exit!=0 ⇒ 步骤失败（fail-closed）
  fi
done
```

- 位置选择：必须在**任何 checkout 之前**完成（逐提交循环会切换工作树；阶段 1 只读 git 对象，不动工作树）；
- 执行器版本：取 CI 自身 checkout 的 `step_enforce.py`（新规则**前向生效**）；分支若删掉该旗标 ⇒ argparse 报错 ⇒ exit 2 ⇒ 红（无静默旁路）。

**不变式**：

- **I-11d evil 内容 fail-closed**：#50 —— 两父皆无的受判路径必须 `exit 1`；
- **I-11e 干净合并不判**：#51~#53 —— 等于任一父 / 非合并提交必须 `exit 0`（**不做并集 diff**，不复发 P-140 假红）。

**替代方案**：

| 方案 | 结论 |
|---|---|
| A 并集 diff（`--base parent1` 判整个 merge） | **否决**：整条分支重灌进单一变更集，P-140 假红复发 |
| B `--base parent2` 判 merge | **否决**：main 侧分支点后的新提交会被卷入 ⇒ 结构性假红 |
| C 只依赖同 job 四道全仓校验 | **否决**：它们判结构与计数，不判「这段变更属于哪批 / session 是否完整」（A-49 实证内容在不违反契约时全绿） |
| **D 检测两父皆无（选中）** | 只判逃逸面，干净合并不判，零假红 |

**风险与回退**：检测成本 = O(受判路径数 × 2 次 `git diff --quiet`），与逐提交走查同量级；回退 = 删 ci.yml 阶段 1 + 删 `--check-merge` 与 4 例测试 ⇒ 回到 P-143 后状态。

**远端读数（P-145 登记）**：真实 `push(main)` run `40603730644`（合并提交 `e8154eb`，父 = `ca456a4` + `c255272`）阶段 1 首次对合并提交判定 = `无 evil 内容（6 个受判路径均等于某一父）`，随后阶段 2 `skip merge commit` + 受判 1 个、墙钟 88 s 全绿 ⇒ 干净合并不误判在设计面成立（evil 侧仍以 A-49/A-50 临时仓读数为准）。

**远端读数（P-146 登记，第 2 样本）**：run `40660622448`（合并提交 `7bcce12`，父 = `e8154eb` + `ac6d194`）阶段 1 再次判定 `无 evil 内容（6 个受判路径均等于某一父）`、阶段 2 skip + 受判 1 个、墙钟 89 s 全绿 ⇒ 「干净合并不误判」可重复，非一次性。

**远端读数（P-147 登记，第 3 样本）**：run `40663831556`（合并提交 `023e456`，父 = `7bcce12` + `f5f08a9`）阶段 1 再次判定 `无 evil 内容（6 个受判路径均等于某一父）`、阶段 2 skip + 受判 1 个（`digest_bound=1`）、墙钟 66 s 全绿 ⇒ 三个连续真实合并样本同形，「干净合并不误判」稳定成立。

**远端读数（P-148 登记，第 4 样本）**：run `40666293529`（合并提交 `fb01568`，父 = `023e456` + `ec10e62`）阶段 1 再次判定 `无 evil 内容（6 个受判路径均等于某一父）`、阶段 2 skip + 受判 1 个（`digest_bound=1`）、墙钟 82 s 全绿 ⇒ 四个连续真实合并样本同形，「干净合并不误判」持续成立。

**远端读数（P-149 登记，第 5 样本）**：run `40676513311`（合并提交 `64c6313`，父 = `fb01568` + `9f1aebb`）阶段 1 再次判定 `无 evil 内容（6 个受判路径均等于某一父）`、阶段 2 skip + 受判 1 个（`digest_bound=1`）、墙钟 81 s 全绿 ⇒ 五个连续样本同形；边际信息量仅「再复现一次」，不改变设计面判据。

**订正（P-150）**：§14.7 各样本表「PR 面阶段 1 未命中」的表述有误。`actions/checkout@v5` 在 `pull_request` 事件下检出 GitHub 合成 merge ref（`refs/pull/N/merge`），`HEAD` 即合成合并提交，故阶段 1 **每次 PR 都命中**并判 `无 evil 内容（6 个受判路径均等于某一父）`（6 个 PR run 实测，#61~#66）；`受判提交 1 个` 是阶段 2 的分支侧普通提交计数。结构含义 = 合成合并提交的树恒等于 head 树（等于某一父）⇒ **PR 面无法证明 evil 判红**，evil 侧必须另行构造（见下）。

**设计面裁决（P-150，§14.8）**：evil 侧取 **路径 2 = 分支内构造合并提交 → 失败 PR**。理由 = ① 唯一能证明「阻断」（required check 失败 ⇒ `mergeStateStatus=BLOCKED`）；② 零 `main` 污染、不动保护规则；③ 失败面停留 Layer-0 可重复。否决路径 1（临时放宽保护直推 `main`）——`push(main)` 面只能事后检测，且合并提交永久留痕（`allow_force_pushes=false`）、恢复窗口风险不可逆。不变式层面：I-11d / I-11e 判据**不变**，本裁决只决定取证方式。

**远端阻断读数（P-151，A-51）**：按 §14.8.5 五步执行，探针 PR #67（head `bdc9a96`，父 = C1 `6524fbe` + C2 `743b29c`）三项判据全部成立——① run `40681417404`（`pull_request`，25 s）`conclusion = failure`，失败 step = `决策流批次强制（step-enforce，逐提交）`，日志 = `evil merge 内容（两父皆无）: spec/framework-deep-review/RESEARCH.md` + `-> exit 1`；② `mergeStateStatus = BLOCKED`（`mergeable = MERGEABLE` ⇒ 阻断来自 required check）；③ `origin/main` 仍为 `6b599b5`（探针提交只存在于已删除的探针分支）。阶段 2 未执行（日志无 `skip merge commit` / `受判提交` 运行期输出）⇒ fail-fast 归因唯一。**口径**：I-11d / I-11e 判据不变；**边界** = 夹具为行尾空白变体（语义级 evil 合并提交会在本地 pre-commit 被拦，构造需 `--no-verify`，故未取）；由此暴露「本地 maintenance 模式 `-w` 放行空白 vs `--check-merge` 逐字节判红」的口径不一致 = 观察项，本批不开。

**Review 签字**: 单 Agent 自查（单视角） 日期: 2026-10-28
