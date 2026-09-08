# Spec_Runner 归巢调研（spec-runner-homing）：双仓 vs 并入——外部依赖面取证与懒加载分层评估 v1.0 (2026-09-08)

---
id: spec-runner-homing-RESEARCH
type: design
version: 1.0
status: in-review
date: 2026-09-08
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0007, langgraph-upgrade-RESEARCH, spec-runner-RESEARCH, community-ecosystem-RESEARCH]
upstream: null
---

> **Feature**: spec-runner-homing（PROGRESS P-019——Spec_Runner 外部仓库路径依赖面取证，评估「并入本仓 vs 懒加载分层」）
> **任务来源**: 用户指令「按照 spec_workflow 的规范进行吃狗粮开发 先基于上两轮分析进行调研」——上两轮 = P-017（接入模板/示例扩散）与 P-018（社区生态 + §3.5 决策产物管线 P-019 采纳路径预告）
> **吃狗粮定位**: 本批为 P-019 调研批（Spec 工作流 Step 1），调研对象 = 本框架最近一次接入扩散（P-017）暴露的外部路径依赖面——self-dogfooding：把上一轮交付物当作本批审查对象
> **编号协调**: P-018 报告 §3.5 曾预告「采纳路径 = P-019 小流程」指决策产物管线；本批调研登场后 P-019 编号被本 feature 占用——已在 PROGRESS 行内登记撞号处理（决策产物管线候选编号顺延，见 §5）
> **调研方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离；E1 仓内取证（grep 盘点 + 文件直读），无 WebSearch（本批问题纯仓内结构问题，不涉外部事实）
> **审查状态**: `自查（单视角）`（RULE-4）——RESEARCH-only 调研收束，同 P-012/P-013/P-015/P-018 先例；独立 pass 挂后续实施批触发
> **核心结论预告**: **维持双仓 + 懒加载分层，否决并入**——本仓对 runner 的依赖面 = 零代码依赖（全部文档指针，E1 取证），并入会推翻上游 P-006/P-009 明文裁决（LANGGRAPH §6「独立仓库」+ DESIGN D1 理由链）而收益为零；唯一可补强点 = adapter 的 RUNNER 配置命中探测（懒加载第一步，probe 先行）

---

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 5 | E1 仓内取证（grep 盘点 + 文件直读，2026-09-08） |
| B 推断类 | 2 | 登记于附录 B（B1 并入冲突面 / B2 懒加载收益） |
| C 判断类 | 3 | §4 裁决 3 条（维持双仓 / 懒加载分层采纳 / 撞号处理） |
| 假设区 | 2 | H1-H2（懒加载探测实现细节 / 双仓漂移观测） |

> **计数说明（R7 机械重数）**: A 类 5 条（行首 `【A】`）；B 类 2 条（附录 B `"id"` 机读块）；C 类 3 条（`【C】` 标记——不参与 R7 机械对账，人工重数）；假设区 2 条（`[H\d+]` 列表项）。
> **自引用剔除注记（机械重数不免疫，同 LANGGRAPH §0 样本⑩附随观察）**: `rg -c "【A】"` 原始命中 6 / `【C】` 原始命中 4——本行（§0 计数说明）自身含 `【A】` 与 `【C】` 字符各贡献 +1，剔除本行后 = A 5 / C 3，与声明一致。

## 1. 调研问题

1. **依赖面实况**：本仓对 Spec_Runner（`F:\Spec_Runner`）的外部路径引用，哪些是代码级依赖、哪些是文档指针？
2. **上游裁决张力**：LANGGRAPH §6 主判断「独立仓库」+ DESIGN D1「双仓结构」的原文与理由链，与「并入本仓去除外部依赖」的动机是否冲突？
3. **三方案对比**：A 完全并入 / B 懒加载分层 / C 维持现状——各自成本、收益、风险？
4. **懒加载分层的具体形态**是什么？（这决定 B 方案是否成立、以及它与 P-018 §3.5 决策产物管线的衔接）

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

## 3. 上游裁决重审（B 类推断）

### 3.1 并入动机是否成立

【B】「并入本仓去除外部依赖」的动机 = 单仓可移植（克隆 spec_workflow 即含 runner 全部能力）。但取证显示：本仓**当前全部工作流路径（三校验器 + 三 hook + 文档治理）零依赖 runner**——runner 是可选增强层（事件流取证/gate 门禁物理化），非工作流运行前提。并入的经济性 = 为「可选增强层的路径便利」付出「推翻两层上游明文裁决 + 本仓身份扩张」的代价，动机收益 < 冲突成本。

### 3.2 并入的冲突面

【B】并入本仓将与以下已物理化约束直接冲突（逐条核对）：
- LANGGRAPH §6「独立仓库」明文（§2.2）
- DESIGN D1「两类可执行件分属两仓」+「代码进本仓 scripts/ ❌」（§2.2）
- 双仓漂移防线机制（IMPL 锚 commit hash）失效——runner 无独立 commit 可锚
- repo_stats 视图层数量发生漂移（scripts/ 新增工具脚本会触发模式库/门面快照重新对账）

## 4. 三方案对比与裁决（C 类）

| 维度 | A. 完全并入 | B. 懒加载分层（采纳） | C. 维持现状 |
|------|-----------|---------------------|-----------|
| 对上游裁决 | 推翻 LANGGRAPH §6 + D1 | 遵守（双仓保留） | 遵守 |
| 代码依赖移除 | ✅（路径消失） | ✅（路径本就非依赖） | ⚠️ 依赖面已为零，无移除对象 |
| 单仓可移植 | ✅ | ❌（需 clone 双仓） | ❌ |
| 本仓身份 | 纯文档→代码仓（存在级扩张） | 不变 | 不变 |
| 双仓漂移防线 | 失效 | 保留 | 保留 |
| 懒加载机制 | 不需要（已内置） | **adapter RUNNER 探测**（缺失即 exit 提示） | 无探测（RUNNER 路径断裂时仅报 FileNotFoundError） |
| 决策产物管线（P-018 §3.5）衔接 | runner 结构破坏，需重移植 | ✅ 事件流位点不动，可叠加 | ✅ 同左 |

### 4.1 裁决 1：维持双仓，否决并入

【C】**否决「Spec_Runner 并入 Spec_Workflow 文件夹」**。理由链：① 取证证明本仓对 runner 的依赖面 = 零代码依赖（§2.1），「去除外部依赖」的动机对象不存在；② 并入即推翻 P-006/P-009 两层明文裁决（§3.2），且触发 repo_stats 对账漂移；③ P-017 接入模板的设计意图 = 任何项目（含本仓自身自举）经配置区接入双仓 runner，并入本仓违背该模板的通用性定位。**【证据引用】§2.1-2.2 E1 取证 + §3.2 推断**

### 4.2 裁决 2：采纳懒加载分层（B 方案）

【C】**采纳懒加载分层 = 文档层自足（现状） + 工具层按需激活**：本仓文档/治理层保持零 runner 依赖（已实证）；工具层（Spec_Runner）作为**可选增强项**，其接入唯一外部路径位点（adapter RUNNER 配置区）升级为**存在性探测**——`probe`/`gate` 子命令前先校验 `RUNNER` 路径可执行，缺失即打印安装指引（`git clone <Spec_Runner 远端>` 或指向本地路径）并以 exit 2 拒绝，替代现状的 `FileNotFoundError` 裸抛。**【证据引用】§2.3 位点定位；落地形态 = adapter 单文件小改（~15 行），不触 runner 本体，不违「薄壳不膨胀」**

### 4.3 裁决 3：P-019 编号撞号处理

【C】**P-019 编号归本批（spec-runner-homing），P-018 §3.5 预告的决策产物管线候选编号顺延 P-020**——撞号 = P-018 报告写作时 P-019 尚空、未预登记；PROGRESS 是编号唯一权威载体，以登记行先到先得。决策产物管线（step-gate）采纳路径不变，仅编号顺延，零逻辑影响。**【证据引用】PROGRESS P-018 行 + 本批登记行的并立关系**

## 5. 假设区

- [H1] adapter 懒加载探测的精确形态（`Path(RUNNER).is_file()` 校验 + `SR_SESSIONS_DIR` 可写校验）可在 Windows 主控站实测通过、且不破坏现有 `probe` 成功路径（dry-run/probe 已实测先行）— 查证路径: adapter 小改后 `probe`/`dry-run gate` 重跑比对
- [H2] 双仓漂移观测期（runner 独立演进 vs 本仓 spec 四件套指针）在 P-019 后续批次中保持零漂移（IMPL 锚 commit 机制继续有效）— 查证路径: 后续实施批 IMPL 锚点更新时核对

## 6. 综合结论

1. 本仓对 Spec_Runner 的外部依赖面 = **纯文档指针 + 1 处自举配置**，零代码级依赖（A1-A5）
2. 「并入去除外部依赖」动机不成立——已无依赖可去，且并入成本 = 推翻两层明文裁决 + 身份扩张（B1/B2）
3. 采纳懒加载分层：工具层探测 README 化 + adapter 小改，作为 P-019 后续实施批（Step 5-10）范围；决策产物管线（P-018 §3.5）顺延 P-020，与懒加载分层无路径冲突（C1-C3）

---

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "Spec_Runner 并入 Spec_Workflow 的成本超过收益：依赖面为零代码依赖（纯文档指针），并入需推翻 LANGGRAPH §6 独立仓库明文 + DESIGN D1 双仓裁决，且触发 repo_stats 对账漂移",
    "op": "tradeoff",
    "claimed_chain": [
      {"step": 1, "text": "本仓对 runner 引用全部为文档指针，scripts/ 与 hook 零引用", "source": "grep 盘点 2026-09-08（E1）"},
      {"step": 2, "text": "LANGGRAPH §6 明文「独立仓库」+ DESIGN D1「两类可执行件分属两仓」", "source": "LANGGRAPH_UPGRADE_RESEARCH.md §6 / SPEC_RUNNER_DESIGN.md D1"},
      {"step": 3, "text": "并入使 IMPL 锚 commit 漂移防线失效 + 触发 repo_stats 视图漂移", "source": "推断（机制对照）"}
    ],
    "sources": [
      {"label": "LANGGRAPH §6", "path": "spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md", "quote": "走方案 B（薄壳纯 Python runner，独立仓库）"},
      {"label": "DESIGN D1", "path": "spec/spec-runner/SPEC_RUNNER_DESIGN.md", "quote": "两类可执行件分属两仓"}
    ],
    "probe": {"type": "existence", "files": ["scripts/dc_validator.py", "scripts/m7_stats.py", "scripts/repo_stats.py", ".pre-commit-config.yaml"], "params": {"symbols": ["spec_runner", "Spec_Runner"], "claim": "absent"}}
  },
  {
    "id": "B2",
    "conclusion": "懒加载分层（文档层自足 + 工具层按需探测）是并入之外的最优解：零上游裁决违背 + 修复 RUNNER 路径断裂时的裸抛体验",
    "op": "design",
    "claimed_chain": [
      {"step": 1, "text": "文档层已自足（三校验器/hook 零依赖 runner）", "source": "§2.1 grep 取证"},
      {"step": 2, "text": "唯一外部路径位点 = adapter RUNNER 配置区（自举配置非依赖）", "source": "§2.3 定位"},
      {"step": 3, "text": "探测缺失即 exit 2 + 安装指引，不改 gate 语义不膨胀", "source": "推断（适配器单文件小改）"}
    ],
    "sources": [
      {"label": "adapter 配置区", "path": "F:/Spec_Runner/templates/examples/spec_workflow_adapter.py", "quote": "RUNNER = r\"F:\\Spec_Runner\\spec_runner.py\""}
    ],
    "probe": {"type": "existence", "files": ["F:/Spec_Runner/templates/examples/spec_workflow_adapter.py"], "params": {"symbols": ["RUNNER", "probe"], "claim": "present"}}
  }
]
```

## 附录 C: 任务来源与上两轮衔接

- **P-017**（上轮 1）：接入模板 + 具体示例扩散——本批的审查对象（adapter RUNNER 位点）
- **P-018 §3.5**（上轮 2）：强制决策产物管线裁定「采纳路径 = P-019」——本批撞号协调（裁决 3），管线本身顺延 P-020，懒加载分层为其铺路（工具层入口更健壮）
- 本批呈现形式 = 用户指令「吃狗粮开发」的执行：以 P-019 为例跑 Spec 工作流 Step 1（调研），调研对象 = 上一轮交付物的结构假设