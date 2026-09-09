# 调研文档：hook 面扩展调研评估（禁止性负例通道 + 分阶段 hook——CER「ADR 三层 enforcement」候选的触发驱动评估）

---
id: hook-surface-RESEARCH
type: design
version: 1.0
status: draft
date: 2026-09-09
depends: [community-ecosystem-RESEARCH, ADR-0010, SPEC-PROCESS]
upstream: null
---

> **Feature**: hook 面扩展调研评估（PROGRESS P-030——CER「ADR 三层 enforcement」候选的触发驱动评估，Layer-0 概念调研登记）
> **创建日期**: 2026-09-09
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「执行后续 hook 面扩展调研评估」——触发 [COMMUNITY_ECOSYSTEM_RESEARCH.md](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md)（CER）§3.4.1 ADR 三层 enforcement 行「下一步 = 触发驱动（后续 hook 面扩展时评估）」的登记触发条件。

---

## 1. 调研目标

**核心问题**（触发型评估，非新外部调研）：

1. 社区 pre-commit / pre-push / CI 分层 hook 实践的最佳形态是什么？本仓当前 4 hook 全在 pre-commit 单层的现状与社区形态差距多大？
2. forbid / ban 通道（禁止性负例通道）在社区如何显式化与机械化（deny-list / allowlist / policy 块）？
3. 本仓 AGENTS.md「禁止事项」6 条逐条的机械化可行性如何？分阶段 hook 的增量价值几何？
4. hook 面扩展作为候选吸收物，过 ADR-0010 三问（放哪层 / 激活条件 / 未激活副作用）的结局是什么？结论建议是什么？

> **调研边界说明**：本 feature 的候选本体已在 CER（v1.1~v1.9）中完整登记（ADR 三层 enforcement = 禁止性负例通道 + 分阶段 hook，Layer-0 模式吸收候选）。本调研**不改变候选分层**（仍为 Layer-0 概念），仅对「后续 hook 面扩展时评估」这一触发条款执行评估并给出确定性结论。评估对象 = 本仓 hook 面（`.pre-commit-config.yaml` 四 hook）自身，不引入任何新依赖。

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| WebSearch | 社区分层 hook 实践 / --no-verify 旁路 / forbid-ban 通道形态三轮取证（2026-09-09） | `pre-push vs pre-commit layered enforcement` / `git hook forbid deny banned pattern git-secrets` / `--no-verify bypass re-run pre-push backstop` / `adr require forbid lint rules staged enforcement` |
| Grep/Read | 本仓 hook 面现状（`.pre-commit-config.yaml`）+ AGENTS.md 禁止事项原文 + ADR-0010 三问门禁与失效条件 | `禁止` / `不得` / `必须` / `pre-commit` / `失效条件` |

### 2.2 调研范围

本仓现状快照（2026-09-09）：

- **hook 面**: `.pre-commit-config.yaml` 4 hook（dc-validator / m7-stats / repo-stats / step-enforce），全部挂 pre-commit 单层；无 pre-push / commit-msg / CI。
- **禁止事项**: AGENTS.md「禁止事项」6 条（不得跳过 pre-commit / 不得手改 M7 统计声明 / 破坏性操作前必须备份 / 计数声明=机械重数 / 同文件修改严格串行 / batch 后全覆盖终验 grep）。
- **门禁**: ADR-0010 三问（候选吸收强制门禁）+ 失效条件（工具数 >8 升执行件; 连续 3 个吸收裁决未引用三问 → 重审门禁是否需要机械化（hook 级））。

---

## 3. 调研发现

### 3.1 社区分层 hook 实践（pre-commit 快查 / pre-push 慢查 / CI 兜底）

社区主流工具生态（Husky / overcommit / 各 lint 框架文档）与 **ADR Kit 的分阶段 enforcement** 已形成「分层成本-深度」共识，典型参数（ADR Kit 实证）:

| 层 | 触发点 | 检查粒度 | 预算 | 典型内容 |
|----|--------|---------|------|---------|
| pre-commit | commit 时 | 增量（仅暂存文件 `git diff --cached`） | <2-5s | 格式/风格/导入限制（可自动修复） |
| pre-push | push 时 | 全量 / 变更影响域 | <15s | 全量测试 / 类型检查 / 架构边界 |
| CI/PR | 远程 | 全量 | 分钟级 | 构建 / 集成 / 端到端 + 本地 hook 旁路兜底 |

社区共识：**本地层 = 拦截明显低级错误的快速反馈环；远程层 = 兜底强制闸门**。过长检查放本地会诱导跳过（门槛过高 → 开发者为效率绕过）。

### 3.2 --no-verify 旁路与兜底

- git 官方文档明示：`pre-commit` 可用 `--no-verify` 绕过；pre-push 同理。
- 社区实测（block-no-verify 项目，2026-06）：**12 种绕过向量全部能使本地 hook 失效且被工具放行**——引号拆分命令 / `--no-veri` 前缀缩写 / `GIT_CONFIG_PARAMETERS` 环境变量注入 / `GIT_CONFIG_COUNT` 覆盖 core.hooksPath / `LEFTHOOK=0` / `SKIP=pre-push` 等 hook 管理器禁用开关。
- 结论：**任何本地 hook 都无法 100% 阻挡绕过**。本地 hook 是"诚实的护栏"，远程/CI 才是真正的强制层。

对**纯本地单人仓库（本仓无 CI）**的影响：
- 本地环上优化到极致也只是最外层，无法达到绝对强制；
- 更现实的定位 = 「记录性禁止事项显式化 + 机械扫描证据」，而非依赖 hook 做最终强制；
- 绕过场景的实际发生频率才是激活判据（本仓 P-020 起吃狗粮全过 hook，旁路零发生）。

### 3.3 forbid / ban 通道（禁止性负例）社区形态

社区禁止性规则的落点形态 = **显式 deny-list 正则文件 + 例外 allowlist**，机制统一为「policy 显式落文档/规则文件 → 工具自动生成可执行检查（正则/lint 规则）→ 激活于 hook/CI → 命中即拒绝」：

| 项目 | 形态 | 机制 |
|------|------|------|
| awslabs/git-secrets | 禁止正则列表 | 扫描 commits / commit messages / --no-ff merges，命中拒绝 |
| nhsd-git-secrets-precommit | `rules/nhsd-rules-deny.txt` | deny 规则文件 + `.gitallowed` 例外白名单 |
| detect-secrets / gitleaks | 正则 + 基线文件 | `.secrets.baseline`（已知误报 allowlist） |
| kschlt/adr-kit | **policy 块 → 生成 lint 规则** | ADR 里 require/forbid 策略块自动生成 ESLint/Ruff/import-linter 规则，pre-commit 查导入限制 / pre-push 查架构边界 |
| wakatchi.dev ADR 侵食三层防御 | ADR 禁止事项 → 差分静态检查脚本 → CI/pre-commit | 禁止事项标识符级显式化 + git merge-base 差分扫描违规引入 |

**关键分类**：
- **记录性禁止事项**（禁止引入某依赖 / 禁止使用某 API / 禁止手改某统计声明）→ **可机械化**（搜索 + 阻止 + 例外白名单）。
- **过程性禁止事项**（提交前必须备份 / 不得跳过检查 / batch 后必须终验）→ **不可机械化**（tool 执行的环境状态不可机械校验；git 只能看最终结果，无法判断"提交前是否备份"或"编辑过程是否串行"），只能文档显式化 + 审查臂监督。

### 3.4 本仓 hook 面现状（4 hook 全在 pre-commit 单层）

| hook | 校验器 | 覆盖 | 触发层 |
|------|--------|------|--------|
| dc-validator | scripts/dc_validator.py | DC1-DC4 + R7（.md） | pre-commit |
| m7-stats | scripts/m7_stats.py | M7 账本 hits 块对账 | pre-commit |
| repo-stats | scripts/repo_stats.py | 视图层声明=重数 | pre-commit |
| step-enforce | scripts/step_enforce.py | 批次级流程强制（P-024） | pre-commit |

现状 = 社区分层形态的**第一层完备、第二/三层缺失**（本仓无 CI 是架构事实，pre-push 可能补第二层）。

### 3.5 本仓禁止事项逐条机械化可行性矩阵

AGENTS.md「禁止事项」6 条（全量原文核对，2026-09-09）：

| # | 禁止事项 | 类型 | 机械化可行性 | 现状（已有机械位点） | 候选新增机械位点 |
|---|---------|------|------------|--------------------|----------------|
| 1 | 不得跳过 pre-commit 检查 | 过程性 | **部分**（只能兜底，不能强制；`--no-verify` 旁路不可根除） | step-enforce（批次级，P-024）；四 hook 配置齐备 | pre-push 复验（三校验器 + step-enforce 全量重跑，拦截被跳过的批次）——唯一有真实增量的点 |
| 2 | 不得手改 M7 账本统计声明（由机械脚本重写） | 记录性 | **完全** | m7-stats hook（M7_EVIDENCE_LOG.md 单文件）+ `--write` 再生成制 | 追加 pre-push 复验（防止 edit 后 skip hook）——当前已可防，增量近零 |
| 3 | 破坏性文件操作（覆盖/截断/批量替换）前必须备份 | 过程性 | **不可**（tool 执行环境不可校验；git 只能看最终 diff） | 无（依赖生成端纪律 + RULE-1 审查臂 + git 历史可回滚） | 不可机械拦截——保持文档纪律 + 审查臂监督 |
| 4 | 文档计数声明必须与机械重数一致（声明=重数） | 记录性 | **完全** | dc-validator（R7 机械重数）+ repo-stats（视图层声明=重数） | pre-push 复验——增量近零（hook 已全量覆盖） |
| 5 | 同一文件修改必须严格串行（DIS-008） | 过程性 | **不可**（发生于 agent 编辑流程，工具层不可见） | 编辑工具单次 Edit 仅处理一个文件 + 强制先 Read（天然串行约束） | 不可机械拦截——工具层约束已近似强制 |
| 6 | batch 编辑后必须全覆盖终验 grep（不得抽样） | 过程性 | **不可**（agent 行为，工具层不可见） | 三校验器全量扫描（近等价机械终验）；全量覆盖 grep 纪律由审查臂复核 | 不可机械拦截——三校验器已近似强制终验 |

**结论**：6 条中 **3 条（#1/#2/#4）已机械化或可在现有位点强化**（均为记录性/可复验类），**3 条（#3/#5/#6）为过程性行为纪律，git hook 层不可机械拦截**。hook 面扩展的增量价值集中在 #1 的 pre-push 复验兜底（唯一有真实增量的点）。

### 3.6 分阶段 hook 增量价值分析

| 阶段 | 建议能力 | 增量价值 | 成本 | 判定 |
|------|---------|---------|------|------|
| 阶段 0（现状） | pre-commit 四 hook | 当前基线 | — | 已具备 |
| 阶段 1 | pre-push 复验兜底（重跑三校验器 + step-enforce） | 拦截 `--no-verify` 旁路 / hook 未装（P-026 盲区类）产生的坏产物出仓；全量复验兜底 | 中（新增 pre-push hook 文件；三校验器全量 ~200ms 级） | **增量真实但触发证据不足**（旁路零发生；P-026 盲区已修） |
| 阶段 2 | forbid 策略块机读显式化（禁止事项 → 机械扫描） | 记录性禁止事项显式落位；但 #2/#4 已全机械化，#1 有更轻的复验替代 | 中-高（新脚本 + 契约 + 对账维护） | **增量近零**（已机械化） |
| 阶段 3 | 禁止性正则 deny-list 通道（git-secrets 式） | 对纯文档仓无 secret 场景，无导入限制场景 | 高（无适用对象） | **不适用**（纯 md 文档仓） |

---

## 4. 综合分析

### 4.1 ADR-0010 失效条件②观察项登记

- 失效条件原文：「连续 3 个吸收裁决未引用三问 → 重审门禁是否需要机械化（hook 级）」。
- 失效条件**当前未命中**（P-028/P-029 均显式引用三问；P-023 亦走三问——连续引用在案）。
- 本评估将「hook 面扩展 = ADR-0010 失效条件②的机械化候选」登记为**观察项**：若未来连续 3 个吸收裁决未引用三问，触发重审时本评估即为缓存结论，避免重复评估。

### 4.2 ADR-0010 三问懒加载门禁（候选吸收物 = "hook 面扩展机制"）

| 问 | 回答 |
|----|------|
| **Q1 放哪层？** | 若实施 = **Layer-1**（`.pre-commit-config.yaml` / `.pre-push` hook 配置 + 新脚本）；记录性禁止事项的机读显式化（policy 块）= Layer-0。 |
| **Q2 激活条件？** | **未满足 → 不实施**。本仓 = 纯文档仓（零应用代码），#2/#4 已完全机械化，#1 的 pre-push 复验兜底是唯一增量，但：① `--no-verify` 纪律已被 AGENTS.md + step-enforce 强约束；② P-020 起吃狗粮全过 hook，旁路场景零发生；③ 社区证据（block-no-verify）表明无法械绝对强制。**无真实失败案例 → 无触发**（触发驱动不排队）。 |
| **Q3 未激活副作用 = 0？** | **是**。不引入任何 hook 改动，三校验器 / 既有 hook / 文档层零变化。 |

### 4.3 结论与建议

- **hook 面扩展当前不实施**（阶段 1 增量真实但触发证据不足；阶段 2/3 增量近零或不适用）。止于懒加载 gate（Q2 触发条件未满），同 P-028/P-023 先例。
- **评估本身闭环 CER §3.4.1 ADR 三层行「下一步 = 触发驱动（后续 hook 面扩展时评估）」**——以"已评估"的确定性替代"未评估"的悬置；候选保持 **Layer-0 模式吸收**状态不变。
- **观察项登记**：hook 面扩展（尤其阶段 1 pre-push 复验）挂 ADR-0010 失效条件②，触发条件 = ① 连续 3 个吸收裁决未引用三问，或 ② 出现真实 `--no-verify` 旁路失败案例（E1/E2 实证）。
- **既有禁止事项纪律维持**：记录性（#2/#4）由机械校验器 + hook 持续看护；过程性（#3/#5/#6）由文档纪律 + 审查臂（RULE-1）监督——本次评估未发现需要立即机械化的缺口。

---

## 5. 局限

1. 社区取证为文档/README/实测文章级（声明级），未做源码直读核验——不引入本体故不需升级证据等级（同 Ponytail 先例）。
2. block-no-verify 的 12 向量为第三方实测（2026-06 MySQL/版本 1.3.0 快照），非本仓环境实测——本仓旁路零发生已由吃狗粮历史（P-020 起）支撑。
3. 本仓无 CI 是架构事实，pre-push 复验的价值评估基于"本地单人 + GitHub 托管"场景；若未来引入 CI，阶段 1 增量进一步弱化（CI 兜底接管）。
4. 禁止事项 #3/#5/#6 的"不可机械化"判定基于 git hook 层视角；工具平台层（编辑器权限/沙箱）可能提供部分约束，超出本评估范围。

---

## 6. 关联登记

- **上游候选**: CER §3.4.1 ADR 三层 enforcement 行（触发条款「后续 hook 面扩展时评估」→ 本评估闭环）+ CER §3.4.2（v1.10 新增独立评估节）。
- **门禁**: ADR-0010 三问（Q1=Layer-1 候选 / Q2 未满足不实施 / Q3 = 0）+ 失效条件②观察项登记。
- **关联机制**: AGENTS.md 禁止事项（6 条，评估对象）/ `.pre-commit-config.yaml`（4 hook 现状）/ P-024 step-enforce（批次级强制先例）/ P-027（hook 覆盖盲区修复先例）。
- **结论落位**: PROGRESS P-030 + CODE_WIKI（feature 目录 / doc_registry / stats declared 同步）。