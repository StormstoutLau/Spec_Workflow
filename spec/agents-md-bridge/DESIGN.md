# 设计文档：AGENTS.md 桥（C-01 落地）

---
id: agents-md-bridge-DESIGN
type: design
version: 1.1
status: verified
date: 2026-09-08
depends: [community-ecosystem-RESEARCH, SPEC-PROCESS, ADR-0010]
upstream: null
---

> **Feature**: AGENTS.md 桥文件生成（CER C-01）
> **创建日期**: 2026-09-08
> **状态**: 草稿
> **Spec 步骤**: Step 3-4
> **基于调研**: [COMMUNITY_ECOSYSTEM_RESEARCH.md](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) §3.1 C-01 / §2.2 / §3.4.1 / H1

---

## 1. 设计目标

在本仓根生成 `AGENTS.md` = SPEC_PROCESS 的**操作摘要桥**：把本仓性质、校验命令、禁止事项压缩为指针化摘要，使主流 agent 工具（Cursor/Copilot/Codex 等）进入本仓时拿到行为对齐指引——这是 CER §2.2 判定的"本框架唯一、立即可以补强的互操作空白"。设计约束 = **零依赖、零校验器改动、双源漂移免疫**（AGENTS.md 摘要永不与 SPEC_PROCESS 母文档漂移）。

## 1.1 收益分析（v1.1 增补，用户指令「按这个收益分析更新 AGENTS.md 桥的文档说明」）

基于 CER 既有判定（§2.2 / §3.1 C-01 / §3.4 矩阵 / §5.4 H1）+ P-021 落地验证，本 feature 收益分四层：

| 层 | 收益 | 成本/性质 |
|----|------|----------|
| **1. 工具互操作入口** | 主流工具（Cursor/Copilot/Codex/Devin/Windsurf 等 **23 款原生识别** `AGENTS.md` 文件名，CER A-04）进入本仓时自动读取操作手册——无需人工喂 prompt 解释"这个仓库怎么干活"；一次拿到：仓库性质 / 三校验器命令 / 禁止事项 / 权威源指针 | CER §2.2 判定的"本框架唯一、立即可补的互操作空白" |
| **2. 行为对齐 + 安全护栏前置** | agent 从首次交互起遵守 10 步 Spec 流程与 RULE-1~6（减少绕过 hook / 手改 M7 声明 / 不跑校验器类越界）；破坏性纪律（先备份 / 声明=重数 / 不跳 hook）变成工具可见的硬约束 | R6/M5 门禁的工具层可见化 |
| **3. 零成本正收益** | 成本 = 一个文件、零依赖、零校验器改动（I-3）；漂移免疫 = 零可漂移声明（I-1，全指针化，与母文档永不失真）；未激活副作用 = 0（ADR-0010 三问审核：不存在即无成本） | 边际成本近零而收益为正 → 判为"立即做"（Layer-0） |
| **4. 方法论收益** | 传播形态与社区惯例同步（"规则文件 + agent 适配"已成默认：ARC/Ponytail/ADR Kit 均自带根规则文件，CER §3.4.1）；本 feature 自身 = 懒加载「Layer-0 优先于 Layer-1」的活例证 | CER §3.4.1 观察 + ADR-0010 再实证 |

**诚实边界（CER H1 残余）**：本仓为**方法论文档仓**，工具读取价值场景有限（不写代码、少构建步骤）——收益非零的下限是"工具进入即行为对齐"，但**不会带来频繁可见的操作收益**。由此：**升级保持触发驱动**（如未来接入工具变多、或出现子目录规则需求时再迭代），当前 v1.0 薄壳形态即最优解——这本身就是懒加载纪律（ADR-0010）的要求：Layer-0 不因"可能有用"而膨胀。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| AGENTS.md 是本框架唯一的互操作空白（主流工具原生识别该文件名） | 根单一文件 AGENTS.md，不引入 .agents/ 级联 | CER §2.2 / A-04~A-06 |
| AGENTS.md 桥 = "立即做"候选（Layer-0，零依赖，成本 = 一个文件） | 内容极薄：性质 + 命令 + 禁止事项 + 指针，四段式 | CER §3.1 C-01 / §3.4 矩阵 |
| 双源漂移风险（摘要 vs 母文档）须登记命名空间 + ledger 指涉 | 内容全部指针化，不复制规则全文；入 repo_stats doc_registry | CER §3.1 C-01 风险 |
| H1 待实测：桥文件对主流工具读取兼容性 | 实施后轻量兼容性实测记录（查证工具规范 + 本仓文件格式校验） | CER §5.4 [H1] |
| "规则文件 + agent 适配"已成社区默认传播形态（ARC/Ponytail/ADR Kit 均自带） | 采用社区惯例根 AGENTS.md；正文不超过 ~30 行 | CER §3.4.1 观察 |

### 2.2 相关 ADR

| ADR | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) | 候选吸收三问门禁：Q1 分层 / Q2 激活条件 / Q3 未激活副作用 | 本 feature 执行懒加载审核（见 §4）；AGENTS.md 全域 Layer-0 |
| ADR-0007（D3） | 编号命名空间登记（仅跨文档稳定 ID 入册） | AGENTS.md 非编号命名空间，不入附录 A；改用 repo_stats doc_registry 登记 |

### 2.3 职责边界

- **职责内**：根 AGENTS.md 一个文件；doc_registry 登记；双源漂移纪律说明。
- **职责外**：改动 SPEC_PROCESS / CODE_WIKI 母文档内容；新建校验器；引入 .agents/ 级联或 Agents Standard 五级结构；为 AGENTS.md 配专属机械校验（其内容零可漂移声明，无需校验器）。

## 3. 架构设计

### 3.1 整体架构

单文件 Layer-0 桥（`AGENTS.md` @ 仓库根）：agent 工具进入时自动读取 → 与本仓行为对齐。

```
┌─────────────┐  读取于衔接时   ┌──────────────────────────────┐
│ agent 工具    │ ─────────────▶ │  AGENTS.md（Layer-0 桥）      │
│ Cursor/Codex │                │  四段：性质/流程/命令/指针     │
└─────────────┘                └──────────┬───────────────────┘
                                         │ 指针（权威源）
                                         ▼
                     SPEC_PROCESS.md / CODE_WIKI.md / KGS 契约
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| 四段式内容 | 性质/流程摘要/校验命令/权威源指针 | SPEC_PROCESS + CODE_WIKI 素材 | AGENTS.md 文本 | 无（静态文本） |
| doc_registry 登记 | CODE_WIKI §10 stats 块加 label 指向 | 本 feature 目录 | repo_stats 可枚举 | repo_stats.py（只读） |

### 3.3 不变式（Invariants，ADD 审计依据）

1. **I-1 零可漂移声明**：AGENTS.md 不含任何数值性/计数性声明（不写 feature 目录数、样本数、版本号、文件数）——从源头免疫双源漂移，repo_stats PT 模式零命中。
2. **I-2 指针化不复制**：AGENTS.md 只保留「性质一句话 + 命令 + 禁止事项」，其余全部指针到 SPEC_PROCESS/CODE_WIKI 权威源；规则全文不复制。
3. **I-3 零工具改动**：不新增校验器、不改 pre-commit、不改任何脚本——本 feature 交付物 = 1 个文件 + 1 处 doc_registry 登记。
4. **I-4 单向依赖**：AGENTS.md 依赖文档层；文档层绝不依赖 AGENTS.md（与 ADR-0010 单向依赖一致）。

## 4. 懒加载审核（ADR-0010 三问门禁——正式执行）

> 依据 [ADR-0010](../../adr/ADR-0010-lazy-loading-architecture-gate.md) 三问门禁，对本 feature 的候选吸收物（AGENTS.md 桥文件）逐问审理。CER v1.3 已做 Q1 预演（Layer-0），本设计为该预演的正式审核记录。

| 问 | 审理 | 结论 |
|----|------|------|
| **Q1 放哪层** | AGENTS.md 是**单一静态文件**，生成即存在，无任何运行时、无激活管线、无依赖安装——满足 Layer-0 定义（文档层；纯文档消费者零工具依赖即可使用，Layer-1 按需激活的前提不成立）。它自身不"做"任何事，只是工具衔接时的规则接口。 | **Layer-0**（与 CER v1.3 预演一致） |
| **Q2 激活条件** | 无触发依赖：文件提交即"激活"（存在即被工具读取），不存在"待触发"状态。激活零副作用：不污染既有文档、不改写工具、不给后续引入隐式负担（I-1 保证零可漂移内容）。 | **无触发条件（生成即激活）** |
| **Q3 未激活副作用** | 未生成 AGENTS.md = 该文件"不存在"（懒加载语义 = 未激活即不存在）：文档层完全自足（SPEC_PROCESS/CODE_WIKI 本就人类可读），唯一损失 = 工具互操作入口（CER §2.2 判定的空白），副作用 = 0。 | **0** |

**审核结论：通过。** AGENTS.md 桥是 Layer-0 候选的教科书实例——三问全部满足，无连坐依赖（不依赖任何候选），与 CER §3.4 矩阵「分层归属 = Layer-0（单一文件，零激活成本）」一致。**审核注**：本 feature 自身即懒加载原则的产物（Layer-0 优先于 Layer-1 的再实证）。

## 5. 替代方案

### 5.1 方案 A：根 AGENTS.md 单一文件（选择）

- 描述：仓库根一个 `AGENTS.md`，四段式指针摘要。
- 优点：主流工具（Cursor/Copilot/Codex/Devin/Windsurf 等，CER A-04：23 工具原生支持）标准识别位点；零依赖；文件极少（薄壳）。
- 缺点：单一文件无法按目录细分规则（本仓方法论文档仓，无子目录规则需求）。
- 选择理由：应与社区传播形态一致（ARC/Ponytail/ADR Kit 均为根文件 + 平台适配，CER §3.4.1 观察）；本仓是纯文档方法论仓，全局单规则集即可。

### 5.2 方案 B：详细复制 SPEC_PROCESS（否决）

- 描述：把 10 步流程、Review 六规则全文复制进 AGENTS.md。
- 优点：agent 单文件内自足。
- 缺点：双源漂移必然发生（母文档修订后摘要失真，CER §3.1 C-01 明示风险；DIS-009/010 文档-实际漂移族）。
- 否决理由：违反 I-2 指针化纪律 + CER 风险登记；本框架的漂移认知（SGE silent drift）直接排除此方案。

### 5.3 方案 C：Agents Standard 五级级联 / .agents/ 子目录（否决）

- 描述：`~/.agents/AGENTS.md` + `.agents/AGENTS.md` + 根 + 子目录四级（agentsstandard.com，CER A-05）。
- 优点：大规模组织场景的层级规则。
- 缺点：单仓库单人方法论场景过度工程；引入目录结构与拼接语义（与薄壳原则冲突）。
- 否决理由：ADR-0010 懒加载 + 薄壳不膨胀（P-009 同款）——最小可行形态 = 根单文件。

## 6. 接口定义

### 6.1 AGENTS.md 文件结构（agent 读取接口）

四段，总行数 ≤ 40：

```
# 头注释（定位声明 + 权威源指针 + CER C-01 出处）
## 仓库性质（一句话 + 核心目标）
## 开发流程（10 步 Spec 流程一句话 + 四文档管道）
## 校验命令（三个命令 + 用途 + pre-commit 提示）
## 禁止事项（R6/M5 门禁：不绕过 hook / 不手改 M7 声明 / 破坏性操作先备份 / 声明=重数）
## 权威源指针表（主题 → 文档链接）
```

### 6.2 doc_registry 登记（repo_stats 接口）

CODE_WIKI §10 stats 块 `doc_registry` 数组追加：

```json
{"label": "agents-md-bridge", "path": "spec/agents-md-bridge/DESIGN.md"}
```

（登记 feature 设计文档路径即可；AGENTS.md 根文件由 DESIGN 文档指针承载，不入 doc_registry——避免将工具接口文件当作对账文档。）

## 7. 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| AGENTS.md 含计数声明触发 repo_stats PT 误报 | I-1 规避（设计期克制）；若仍命中走 suppress 白名单登记（P-014 先例） |
| 母文档规则更新后桥内容失真 | 观点指针化 + 修订历史注（桥内注明"以 SPEC_PROCESS 为准"）；漂移风险登记 CER §3.1 |
| 工具对 AGENTS.md 的读取差异 | H1 实测记录于本 feature（兼容性快照），发现异常登记观察 |

## 8. 对实施的输入

### 8.1 关键工程约束

1. AGENTS.md 字数 ≤ 40 行、零数字声明、命令精确复制（dc_validator.py / m7_stats.py / repo_stats.py）。
2. doc_registry 只登记 DESIGN 文档。
3. 实施后运行三校验器确认零违规（含 repo_stats doc_registry 新条目）。

### 8.2 实施步骤

1. 创建根 `AGENTS.md`（内容见 6.1）
2. CODE_WIKI §10 doc_registry 追加 label
3. 三校验器验证
4. CER 侧不动（调研文档已收束）；PROGRESS/CODE_WIKI 落档走 Step 8 收束

---

**Review 签字**: _________ 日期: _________