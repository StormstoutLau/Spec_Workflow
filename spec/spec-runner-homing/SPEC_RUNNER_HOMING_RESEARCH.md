# Spec_Runner 归巢调研（spec-runner-homing）：双仓 vs 并入——管理便利动机重审 v1.1 (2026-09-08)

---
id: spec-runner-homing-RESEARCH
type: design
version: 1.1
status: in-review
date: 2026-09-08
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0007, langgraph-upgrade-RESEARCH, spec-runner-RESEARCH, community-ecosystem-RESEARCH]
upstream: null
---

> **Feature**: spec-runner-homing（PROGRESS P-019——Spec_Runner 外部仓库路径依赖面取证，评估「并入本仓 vs 维持双仓」）
> **任务来源**: 用户指令「按照 spec_workflow 的规范进行吃狗粮开发 先基于上两轮分析进行调研」+ 裁决修正输入「我的目的是当前似乎不值得为 spec_runner 单独设立一个仓库 spec_runner 放在 spec_workflow 文件夹下面可以方便管理 读写 请重新分析」
> **吃狗粮定位**: 本批为 P-019 调研批（Spec 工作流 Step 1），调研对象 = 本框架最近一次接入扩散（P-017）暴露的双仓结构假设——self-dogfooding：把上一轮交付物当作本批审查对象
> **编号协调**: P-018 报告 §3.5 曾预告「采纳路径 = P-019 小流程」指决策产物管线；本批调研登场后 P-019 编号被本 feature 占用——已在 PROGRESS 行内登记撞号处理（决策产物管线候选编号顺延，见 §5）
> **v1.1 变更（用户裁决修正轮，2026-09-08）**: 用户纠正调研动机——目的 **不是「去除外部依赖」而是「单仓管理便利」**（Spec_Runner 放本仓文件夹下统一管理/读写）。据此重审 C1：补充取证 **A6（Spec_Runner 仓无 remote / 单分支 / 5 commit 全服务本仓——「独立生命周期/可能推送远程」论据实证弱化为零）**；**C1 改判：从「否决并入」改为「采纳并入为候选方向」**——管理便利动机成立（单人仓双仓运维成本实证：跨仓提交/切换/检索），且 D1 反对理由三的「独立生命周期」在实施后 27 天被证伪（无独立用户、无远程、无独立用途，实为本仓内聚组件被隔离在外仓）。保留的权衡 = 并入改动面（上游 LANGGRAPH §6 明文修订 + DESIGN D1 修订 + repo_stats 对账 + 双仓漂移防线退役）需设计批量化评估；本批裁决 = 方向采纳 + 实施批待触发。A 5→6 / B 2 / C 3 / H 2。
> **调研方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；E1 仓内取证（grep 盘点 + 文件直读 + git remote 核验），无 WebSearch（本批问题纯仓内结构问题，不涉外部事实）
> **审查状态**: `自查（单视角）`（RULE-4）——RESEARCH-only 调研收束，同 P-012/P-013/P-015/P-018 先例；独立 pass 挂后续实施批触发
> **核心结论预告**: **采纳并入为候选方向（v1.0 否决废止）**——本仓对 runner 的依赖面 = 零代码依赖（全部文档指针，E1 取证，不变）；新增裁决依据 = 用户管理便利动机 + A6 实证（Spec_Runner 无独立生命周期理由）。并入成本 = 上游两层裁决修订 + repo_stats 对账 + 漂移防线退役，落定实施批评估；懒加载分层降级为并入前的过渡机制（若并入，RUNNER 探测自然消失——runner 就在本仓）

---

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 6 | E1 仓内取证（grep 盘点 + 文件直读 + git remote 核验，2026-09-08；v1.1 +A6 remote 核验） |
| B 推断类 | 2 | 登记于附录 B（B1 并入冲突面 / B2 管理便利收益） |
| C 判断类 | 3 | §4 裁决 3 条（v1.1 改判：采纳并入 / 懒加载降级过渡 / 撞号处理） |
| 假设区 | 2 | H1-H2（并入改动面量化 / 双仓漂移观测） |

> **计数说明（R7 机械重数）**: A 类 6 条（行首 `【A】`）；B 类 2 条（附录 B `"id"` 机读块）；C 类 3 条（`【C】` 标记——不参与 R7 机械对账，人工重数）；假设区 2 条（`[H\d+]` 列表项）。
> **自引用剔除注记（机械重数不免疫，同 LANGGRAPH §0 样本⑩附随观察）**: `rg -c "【A】"` 原始命中 8 / `【C】` 原始命中 5——两行自引用各贡献 2（§0 计数说明行 + 本自引用注记行均含 `【A】` 与 `【C】` 字符各 1），剔除后 = A 6 / C 3，与声明一致。

## 1. 调研问题（v1.1 修正）

1. **依赖面实况**：本仓对 Spec_Runner（`F:\Spec_Runner`）的外部路径引用，哪些是代码级依赖、哪些是文档指针？（结论不变：零代码依赖）
2. **上游裁决张力**：LANGGRAPH §6「独立仓库」+ DESIGN D1「双仓结构」的原文与理由链，与用户真实动机（单仓管理便利）是否冲突？
3. **v1.1 动机重审**：用户目的 = **单仓统一管理/读写便利**（非去依赖）。D1 反对理由三「runner 有独立生命周期（自身版本、自身 git 历史、可能推送远程）」在实施 27 天后是否成立？—— A6 实证核验
4. **三方案对比**：A 完全并入 / B 懒加载分层（v1.0 候选）/ C 维持双仓——按「管理便利」维度重评
5. **懒加载分层的地位变化**：若并入采纳，其 RUNNER 探测机制自然退役（runner 在本仓），懒加载降级为过渡项

**背景**：P-017 把接入模板/示例扩散到独立仓库 `F:\Spec_Runner`。用户上轮问过「是否需要把 spec_runner 放进 spec_workflow 文件夹以去除外部依赖」（接入示例中 `RUNNER = r"F:\Spec_Runner\spec_runner.py"` 是唯一指向外部仓库的路径位点）。本批把这个问题正式调研化。

## 2. 仓内取证（E1，A 类）

### 2.1 引用位点全盘点（grep `Spec_Runner|spec_runner|spec-runner` @ 2026-09-08）

【A】本仓对 Spec_Runner 的全部引用可分四类，**无一为代码级 import/subprocess 依赖**（grep 输出 30KB，逐一分类）：
- **账本/视图指针**（docs/）：PROGRESS P-009/P-017/P-018 行 + 已完成表（事件流指针 `Spec_Runner:sessions/...jsonl#seq`）、CODE_WIKI v1.15.2 版本头 + feature 表行 + 机读块
- **spec 四件套设计引用**（spec/spec-runner/）：RESEARCH/DESIGN/IMPL/CHECKLIST 对 `F:\Spec_Runner` 的绝对路径锚（IMPL 锚 commit `4ea703d`，双仓漂移防线）
- **方法论引用**（spec/community-ecosystem/）：gate 物理化对照、§3.5 采纳路径
- **本仓代码**：三校验器（dc_validator/m7_stats/repo_stats）+ 三 hook **零引用** runner（grep `Spec_Runner|spec_runner` 在 scripts/ 与 .pre-commit-config.yaml 命中 0 处）——D1「双向零依赖」实施态与声明态一致【E1: `rg "Spec_Runner|spec_runner|spec-runner" F:\Spec_Workflow -g "!.git/**" -g "!spec/spec-runner/**"` 输出分类 + scripts/ 定向重查】

【A】反向依赖：Spec_Runner 仓对 `F:\Spec_Workflow` 的引用仅 4 处文档指针（README 设计规格指针 `F:\Spec_Workflow\spec\spec-runner\...` ×1 + 自举示例 docstring 描述 ×3），runner 本体代码零内置本仓路径（`SR_SESSIONS_DIR` env 注入 + `ROOT / "sessions"` 自派生，spec_runner.py L39）【E1: `rg "Spec_Workflow|F:\\Spec_Workflow" F:\Spec_Runner` 输出】

### 2.2 上游裁决原文复核（LANGGRAPH §6 + DESIGN D1）

【A】LANGGRAPH §6 主判断原文含「独立仓库」明文：「**主判断：不整体迁移。方法论文档仓保持纯文档；若需自动化，走方案 B（薄壳纯 Python runner，独立仓库）**」——「独立仓库」是方案 B 定义的一部分而非可选项【E1: LANGGRAPH_UPGRADE_RESEARCH.md L133】

【A】DESIGN D1 理由链原文：「本仓身份 = 纯文档 + 最小工具层，runner 是执行器不是文档契约——三校验器是本仓契约的机械化，runner 是工作流的机械化，**两类可执行件分属两仓**」；候选「代码进本仓 scripts/」被标记 ❌（理由：违反「纯文档 + 最小工具层」定位的扩张方向 + runner 有独立生命周期）【E1: SPEC_RUNNER_DESIGN.md L37-39】

### 2.3 唯一「外部路径」位点

【A】P-017 接入示例 `templates/examples/spec_workflow_adapter.py` 配置区 `RUNNER = r"F:\Spec_Runner\spec_runner.py"` 是本仓全部文件中**唯一指向外部仓库的可执行路径引用**（其余均为文档指针）。该路径属「接入配置区」（adapter 设计 = 新项目照抄后必改 RUNNER/PREFIX/CWD/GATES 四处），即对 Spec_Workflow 自身而言是自举配置而非依赖【E1: spec_workflow_adapter.py L78 + README「具体接入示例」节】

### 2.4 D1「独立生命周期」论据实证核验（v1.1 新增，A6）

【A】**Spec_Runner 仓「独立生命周期」论据在实施 27 天后被实证弱化为零**：该仓 `git remote -v` 为空（**无任何远程**）、单分支 `master`、5 个 commit（`4ea703d`→`71c7ae6`）**全部服务于本仓工作流**（P-009 骨架 / P-017 模板 / P-018 gpt-researcher 补注）——无独立用户、无推送行为、无独立用途，实为本仓内聚组件（事件流取证 + gate 机械化）被隔离在外仓。D1 反对理由三「runner 有独立生命周期（自身版本、自身 git 历史、可能推送远程）」中「可能推送远程」未发生、无第三用户，仅自身版本/git 历史两项成立（但该两项在并入后由本仓统一版本化接管，不构成损失）【E1: `git -C F:\Spec_Runner remote -v`（空）+ `git log --oneline` + `git branch -a`，2026-09-08】

## 3. 上游裁决重审（B 类推断，v1.1 重写）

### 3.1 v1.0 的动机判定失效，新动机 = 管理便利

【B】v1.0 判定「去除外部依赖动机对象不存在 → 并入收益为零」——该判定对「依赖消除」维度成立，但**对用户真实动机（单仓管理便利）不成立**。管理便利维度实证：① 双仓运维摩擦 = 每次 runner 变更需两次 commit（本仓 spec 指针 + 外仓代码）+ 跨仓路径切换 + 双仓 git 状态检查（本会话即发生：P-017/P-018 交付物落外仓、本仓仅登记指针）；② 事件流证据（sessions/*.jsonl）是 E1 级证据资产，却存储在外仓，与 M7 账本同仓可读的管理诉求相悖；③ 单人仓没有分布式协作需求，「双仓 = 各自独立演进」的收益场景（多人/多项目共享 runner）为零。**新权衡 = 管理便利收益 vs 并入改动成本**（上游两层裁决修订 + repo_stats 对账 + 漂移防线退役）。

### 3.2 并入的改动面（v1.0 §3.2 保留，量化责任下放设计批）

【B】并入本仓的已物理化约束改动面（逐条保留，量化评估归实施批）：
- LANGGRAPH §6「独立仓库」明文 + DESIGN D1「两类可执行件分属两仓」「代码进本仓 scripts/ ❌」——需版本化修订（D1 修订注 + LANGGRAPH §6 追记）
- 双仓漂移防线机制（IMPL 锚 commit hash）退役——runner 无独立 commit 可锚，改由本仓统一版本化
- repo_stats 视图层对账：新增目录/文件触发模式库与门面快照重新对账
- sessions/ 目录入库（当前 .gitignore 无 sessions 排除项，jsonl 事件流可作为 E1 证据随仓提交——与 M7 账本指针形态 `Spec_Runner:sessions/...` 改为本仓相对路径）

## 4. 三方案对比与裁决（C 类，v1.1 改判）

| 维度 | A. 完全并入（v1.1 转向采纳） | B. 懒加载分层（v1.0 候选，降级过渡） | C. 维持双仓（v1.0 原判） |
|------|-----------|---------------------|-----------|
| 单仓管理便利 | ✅ 统一读写/检索/提交 | ❌ 双仓切换 | ❌ 双仓切换 |
| 对上游裁决 | 需修订 LANGGRAPH §6 + D1 | 遵守 | 遵守 |
| 事件流 E1 与账本同仓 | ✅ 同仓可读 | ❌ 分离 | ❌ 分离 |
| 本仓身份 | 纯文档→文档+工具（D1 需修订） | 不变 | 不变 |
| 双仓漂移防线 | 退役（统一版本化取代） | 保留 | 保留 |
| 懒加载探测 | 不需要（runner 即本仓） | 需要（过渡项） | 需要 |
| 决策产物管线（P-018 §3.5=P-020）衔接 | ✅ 事件流位点不动 | ✅ 同左 | ✅ 同左 |

### 4.1 裁决 1（改判）：采纳并入为候选方向，v1.0 否决废止

【C】**v1.1 改判：采纳「Spec_Runner 并入 Spec_Workflow 文件夹」为候选方向**。理由链：① 用户裁决 = 权威动机输入（单仓管理便利——统一读写、免双仓切换、事件流证据与账本同仓）；② A6 实证 D1「独立生命周期」论据弱化为零（无 remote / 全 commit 服务本仓）——双仓结构的核心反对理由失效；③ 并入改动面（§3.2）均为机械性/版本化工作，可由实施批量化评估后一次性落地；④ 与决策产物管线（P-020）无路径冲突（事件流位点不动）。**边界**：v1.0 的取证事实（零代码依赖）仍成立，但结论从「收益为零」修正为「收益 = 管理便利与证据同仓，成本 = 一次性改动面」。**【证据引用】A1-A6 E1 取证 + B1（管理便利收益）+ 用户裁决输入**

### 4.2 裁决 2（降级）：懒加载分层退为并入前过渡机制

【C】**懒加载分层从 v1.0 「采纳」降级为「并入实施前的过渡机制」**：若实施批确认并入，runner 在本仓内，`RUNNER` 外部路径探测自然退役（无需探测本仓自身文件）；过渡期（并入前）若需缓解 RUNNER 绝对路径断裂，仍可做存在性探测，但不再作为独立交付项。**【证据引用】裁决 1 的并入采纳方向 + 懒加载的路径探测职责随并入消失**

### 4.3 裁决 3：P-019 编号撞号处理（v1.1 不变）

【C】**P-019 编号归本批（spec-runner-homing），P-018 §3.5 预告的决策产物管线候选编号顺延 P-020**——撞号 = P-018 报告写作时 P-019 尚空、未预登记；PROGRESS 是编号唯一权威载体，以登记行先到先得。决策产物管线（step-gate）采纳路径不变，仅编号顺延，零逻辑影响。**【证据引用】PROGRESS P-018 行 + 本批登记行的并立关系**

## 5. 假设区（v1.1 更新）

- [H1] 并入改动面可在实施批量化落地（LANGGRAPH §6 / DESIGN D1 版本化修订 + repo_stats 模式库与门面快照重新对账 + sessions/ 目录随仓入库 + M7 账本指针形态 `Spec_Runner:sessions/...` → 本仓相对路径改写）且不破坏现有 gate/事件流语义 — 查证路径: 实施批 Dry-Run + 三通道验证 + selftest 重跑
- [H2] 双仓漂移观测期（runner 独立演进 vs 本仓 spec 四件套指针）在并入实施前的过渡期保持零漂移（IMPL 锚 commit 机制继续有效直到退役）— 查证路径: 过渡期 IMPL 锚点核对

## 6. 综合结论（v1.1）

1. 本仓对 Spec_Runner 的外部依赖面 = **纯文档指针 + 1 处自举配置**，零代码级依赖（A1-A5）——事实不变
2. **v1.1 裁决修正**：用户真实动机 = 单仓管理便利（非去依赖）→ 采纳并入为候选方向（C1）；A6 实证 D1「独立生命周期」论据弱化为零（无 remote / 全 commit 服务本仓）（A6 + B1）
3. 懒加载分层降级为并入前过渡机制（C2）；决策产物管线顺延 P-020（C3）
4. 并入改动面 = 上游两层裁决修订 + repo_stats 对账 + 漂移防线退役 + sessions 入库（B2 → 量化归实施批），本批为方向定案 + 实施批触发输入

---

## 附录 B: 断言登记表（机器可读，v1.1 重写）

```assertions
[
  {
    "id": "B1",
    "conclusion": "用户管理便利动机成立：单人仓双仓运维摩擦（跨仓双提交/路径切换/事件流证据与 M7 账本分离）为已实证成本，而 D1「独立生命周期」反对论据经 A6 证伪（Spec_Runner 无 remote、全 commit 服务本仓）",
    "op": "tradeoff",
    "claimed_chain": [
      {"step": 1, "text": "本仓对 runner 引用全部为文档指针，scripts/ 与 hook 零引用（依赖消除维度：无物可去）", "source": "grep 盘点 2026-09-08（E1）"},
      {"step": 2, "text": "Spec_Runner 仓 git remote -v 为空、单分支 master、5 commit 全服务本仓（P-009/P-017/P-018）", "source": "git 核验 2026-09-08（E1，A6）"},
      {"step": 3, "text": "单仓管理便利（统一读写/检索/提交 + 事件流证据与账本同仓）为用户明示动机", "source": "用户裁决输入 2026-09-08"}
    ],
    "sources": [
      {"label": "DESIGN D1", "path": "spec/spec-runner/SPEC_RUNNER_DESIGN.md", "quote": "两类可执行件分属两仓 + runner 有独立生命周期"},
      {"label": "git 核验", "path": null, "quote": "git -C F:/Spec_Runner remote -v 为空；log --oneline -5 全为 Spec_Workflow 服务"}
    ],
    "probe": {"type": "existence", "files": [], "params": {"symbols": ["remote"], "claim": "absent-in-F:/Spec_Runner"}}
  },
  {
    "id": "B2",
    "conclusion": "并入改动面（上游裁决修订 + repo_stats 对账 + 漂移防线退役 + sessions 入库）为机械性/版本化一次性工作，可量化落地；懒加载探测随并入自然退役",
    "op": "design",
    "claimed_chain": [
      {"step": 1, "text": "LANGGRAPH §6 / DESIGN D1 版本化修订（修订注 + 追记）", "source": "版本化先例（P-014/P-016 版本头）"},
      {"step": 2, "text": "repo_stats 模式库/门面快照重新对账（新增目录/文件计数）", "source": "§3.2 改动面清单"},
      {"step": 3, "text": "runner 在本仓后 RUNNER 外部路径探测无对象（自体内置）", "source": "推论"}
    ],
    "sources": [
      {"label": "改动面清单", "path": "spec/spec-runner-homing/SPEC_RUNNER_HOMING_RESEARCH.md", "quote": "§3.2 并入的改动面"}
    ],
    "probe": {"type": "existence", "files": [".gitignore", "scripts/repo_stats.py"], "params": {"symbols": ["sessions", "spec_feature_dirs"], "claim": "present"}}
  }
]
```

## 附录 C: 任务来源与上两轮衔接（v1.1）

- **P-017**（上轮 1）：接入模板 + 具体示例扩散——本批的审查对象（adapter RUNNER 位点）
- **P-018 §3.5**（上轮 2）：强制决策产物管线裁定「采纳路径 = P-019」——本批撞号协调（裁决 3），管线本身顺延 P-020
- **用户裁决修正轮（v1.1，2026-09-08）**：动机从「去除外部依赖」纠正为「单仓管理便利」，C1 改判为采纳并入候选方向
- 本批呈现形式 = 用户指令「吃狗粮开发」的执行：以 P-019 为例跑 Spec 工作流 Step 1（调研），调研对象 = 上一轮交付物的结构假设 + 用户对裁决的修正输入