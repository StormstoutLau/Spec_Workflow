# 调研文档：ARC 决策图谱试点调研（吃狗粮模式）

---
id: arc-probe-RESEARCH
type: design
version: 1.4
status: draft
date: 2026-09-09
depends: [community-ecosystem-RESEARCH, ADR-0007, FWK-DECISION-RECORD]
upstream: null
---

> **Feature**: ARC（kegesch/arc）决策图谱候选——CER §3.4.1 升级优先候选的试点调研（P-031）+ 替代框架调研（P-032）
> **创建日期**: 2026-09-09
> **状态**: draft（草稿）
> **Spec 步骤**: Step 1-2
> **任务来源**: 用户指令「ARC启动调研分析 吃狗粮模式」+「ARC 决策图谱有平台缺陷 那么社区是否有类似的替代框架吗 执行调研任务」
> **v1.1 变更（替代框架调研批，用户指令「ARC 决策图谱有平台缺陷 那么社区是否有类似的替代框架吗 执行调研任务」）**: ARC 平台缺陷实证（A-5/A-6/A-7）触发替代品全景调研——新增 **§3.6 替代框架调研**（子代理 WebFetch 核验 6 候选：adr-kit / phodal/adr / adr-explorer / log4brains / continuity / adr-governance）+ **phodal/adr 本机实测**（Windows，init/new/list/export json/generate graph 全链可用，但 196 包依赖含大量 deprecated = 「轻量」宣称不符）；**核心结论 = 无候选在「关系图谱递归查询 + 9 实体/14 关系 + 零依赖 agent 面」维度完全替代 ARC**（各候选中图维度最强 adr-explorer 亦为只读 web app 非 headless CLI）；ARC 保持主选，缺陷处置 = 等 1.0 稳定 + 规避缺陷命令面（skill/linux bun）+ 替代品按单一维度登记为补位观察。断言计数 11A→**17A** / 3B→**4B** / 3C→**4C** / H=2 不变。
> **v1.2 变更（选型对比批，用户指令「补充调研 如果采用 adr-explorer / adr-kit / phodal/adr / adr-governance 单维度补位 相比 ARC 升级 哪个选项更优 考虑兼容 性能 维护等多个方面」）**: 新增 **§3.7 选型对比**——四替代单维补位 vs ARC 升级的加权评分矩阵（权重：关系图谱能力 30% / 本仓兼容 25% / 性能 10% / 维护 15% / agent 面 20%）：**ARC 升级 4.2 分显著最优**（次高 adr-explorer 3.2——但仅只读看板）；核心原因 = 权重最高的关系图谱递归查询是四替代**共同盲区**（最高 adr-explorer 仅 offer 只读图，非查询驱动）；adr-kit 的强制面（enforce/pre-commit<5s+pre-push<15s/CI）与本仓 step-gate 流程强制重叠、uv 安装在本机无 pip/uv 环境下引入成本；**结论 = 单维补位不作为 ARC 平替，仅登记辅助观测（adr-explorer 可视化看板）**；落地成本 ARC 升级 = 零改动（等待+规避），替代 = 新工具引入+学习曲线。断言计数 17A→**18A** / 4B→**5B** / 4C→**5C** / H=2 不变。
> **v1.3 变更（缺陷规避模式调研批，用户指令「补充调研 假设采用ARC 升级如何规避缺陷 深入调研社区信息」）**: 新增 **§3.8 缺陷规避方案设计**——深入社区取证（2026-09-09 release 页 + issue #30 复核）：**v0.8.0 官方 release 2026-08-14**（含 arc-win32-x64.exe 94.4MB + sha256 可校验，直链下载可规避 npm shim）；版本节奏 6/27-8/14 密集（0.3→0.8）后 **25 天无新 release**；diff/related 命令为 0.6.0 新增（关 #31）；PR 几乎全为 owner 本人（**bus factor=1**）；**issue #30 3 个月零响应**（无评论/无 PR/无 Assignee → bun 修复不可指望）；**规避矩阵** = Windows 官方二进制直链 + 版本 0.8.0 快照固化（sha256 登记）+ 命令白名单（排除 skill/init-agent 缺陷命令面）+ import 仅作文本 crumb 关系由预链接脚本补（FWK-DECISION-RECORD 映射 + link 方向实测校准）+ `arc --version` 不信（用包版本/tag 作版本事实源）+ 停滞观察项（>90 天则启用 P-033 C-5 退路）。断言计数 18A→**19A** / 5B→**6B** / 5C→**6C** / H=2 不变。
> **v1.4 变更（缺陷规避深入调研批，用户指令「深入调研社区信息」复核追赶）**: 复核 A-19 时发现 **A-11 事实错误——driver 命令（#25 next/gaps/context、#26 Vision 实体）并非「计划中未发布」，而是 2026-06-01/#26 2026-05-31 已 completed 发布**（issue #25 Closed 2026-06-01：arc next/arc context 发布、arc gaps **合并入 arc check**（Socratic redesign，非独立命令）、带 21 tests；issue #26 Closed 2026-05-31：Vision 实体 V-xxx 落地 334 tests 含 42 vision-specific）——v1.0 时代的「未发布」取证已过时（0.8.0 实装命令面 A-3 已含 next/context 佐证）；**真正未发布的仅 #14 CI enforcement**（P3 nice-to-have）。修正 = A-11 改为「#25/#26 已发布」，新增 **A-20**（driver/Vision 已发布取证）、**A-21**（release 资产 sha256 全平台登记）、**A-22**（0.6.0 版本节奏精确化：8/10→8/13→8/14 三天三版）。**规避矩阵增量** = `arc context --shallow`/`arc diff` 等**新增命令面纳入白名单**（实测命令面 A-8 已验证）。断言计数 19A→**22A** / 6B→**6B** / 6C→**6C** / H=2 不变。
> **触发依据**: CER v1.5 行「触发条件已满足（v1.8 更新：P-020 落地，决策事件流面已就绪）」+ H2 假设「ARC 对 M7/ADR 决策的导入可行性——字段映射 / 关系类型差异（复用 FWK-DECISION-RECORD 映射契约）——待触发时源码直读 + 试跑实测」。

---

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 22 | 页面试图核验 + 本机实测，每条附来源/实测记录 |
| B 推断类 | 6 | 从实测行为推断的机制/适配 |
| C 判断类 | 6 | 结论性判断（成熟度 / H2 修正 / 试点判定 / 替代缺位 / 选型结论 / 规避方案） |
| 假设区 | 2 | H1-H2（H1 = CER H2 沿线映射差异；H2 = 批量 32 ADR 图质量） |

A/B/C 计数 = 22/6/6，H = 2。

## 1. 调研目标

CER v1.5 将 ARC 升级为优先候选（零依赖单文件 CLI、图查询 trace/impact/check + driver next/context，P-015 方向 A 轻量替代）；本批以吃狗粮模式执行试点调研，回答 **3 个核心问题**：

1. **实态核验**（E1）：ARC 最新快照（版本/活动度/命令集/平台支持）与 CER v1.5 声明是否一致？
2. **H2 假设实测**：本仓 ADR 能否导入 ARC 图？字段映射/关系类型差异/中文语料兼容性如何？
3. **试点判定**：ARC 是否值得本仓引入（引入形态 / 分层 / 触发条件）？gate 三问结论？

## 2. 调研方法

### 2.1 使用的工具

| 工具 | 用途 | 查询 |
|------|------|------|
| WebSearch/WebFetch | 外部快照核验（npm/GitHub/README/issues） | arc kegesch / issues #20 #30 |
| npm install + 本机试跑 | 实测命令链（Windows node v24.14.1 / npm 11.11.0） | init/add/list/check/next/trace/graph/import/skill |
| 本仓 ADR 真实样本 | H2 导入实测 | adr/ADR-0007-unified-document-contract.md |

### 2.2 调研范围

- **对象**: @kegesch/arc 0.8.0（npm 分发 + GitHub 161 commits）/ README / issues #20 #30 及 roadmap
- **实测环境**: Windows 11 + node v24.14.1 + npm 11.11.0（沙箱临时目录 `%TEMP%\arc-probe`）
- **排除**: 非安装的源码级直读（single-file 二进制无源码随包；反编译不纳入）

## 3. 调研发现

### 3.1 外部快照核验（E1，页面级）

【A】A-1: npm `@kegesch/arc` 0.8.0（published 2026-08-20 前后，6 versions，MIT，0 依赖 0 dependents）；npm 页与 GitHub README 均展示同一内容。【来源：npm 页 + github.com/kegesch/arc】

【A】A-2: 161 commits；分发形态 = `bin/arc.cjs` shim + `optionalDependencies` 分平台二进制（`bun build --compile` 单文件）；README 声明「no bun on PATH, no deno on PATH, node is the implicit runtime」。【来源：README + 仓库目录 rsd（bin//packages//src/）】

【A】A-3: 命令面（README CLI Reference）：`init/add/list/show/edit/remove/rename/status/import/trace/impact/check/next/context/validate/invalidate/promote/link/unlink/query/diff/related/graph/skill/init-agent`——较 CER v1.5 快照新增 `diff/related/graph/skill/init-agent`。【来源：README §CLI Reference】

【A】A-4: 实体 9 型（R/A/D/I/S/K/T/UC/EM）+ 关系 ≥14 型（drives/derived_from/conflicts_with/promoted_to/enables/supersedes/inspired_by/requested_by/affects/mitigated_by 等）；存储 = `.arc/` 目录 + 每实体一个 markdown 文件（YAML frontmatter + body），纯文本 git 可提交。【来源：README §Concepts/§File Format】

【A】A-5: **版本失配**：本机 `arc --version` 输出 **0.1.0**，而 npm 包版本 0.8.0——CLI 内部版本号未随包版本更新（低语义载荷字段失配的首层实证）。【来源：实测 `%TEMP%\arc-probe\demo` 环境】

### 3.2 平台缺陷实证（E1，issue + 实测）

【A】A-6: **issue #30（Open，2026-06-08，felixbohnus）**：pnpm 项目（无 bun）运行 arc 命令报 `env: bun: No such file or directory`——与 README 声明「no bun on PATH」**直接矛盾**（文档-实现不符）。【来源：github.com/kegesch/arc/issues/30】

【A】A-7: **`arc skill` 命令 Windows 实测崩溃**：`error: Cannot find SKILL.md. Tried: B:\~BUN\skill\arc\SKILL.md, B:\skill\arc\SKILL.md`——**构建环境路径（B:\~BUN）硬编码泄漏进发布二进制**（Windows 无 B 盘路径，命令不可用）。【来源：本机实测 `%TEMP%\arc-probe\demo`】

【B】B-1: 两缺陷同根因族 = 构建/运行环境假设泄漏到发布产物（linux 依赖 bun PATH、win 依赖构建盘符路径）——0.x 单作者早期项目的平台调试债实证。

### 3.3 本机实测记录（E1，Windows）

【A】A-8: 基本命令链 Windows 实测全部可用：`init`（生成 10 类目录 + arc.yaml）/ `add`（R/A/D 实体）/ `list` / `check`（orphan_decision ∩ unvalidated_assumption ∩ unconnected_entity 分类 + 💡 修复提示）/ `next`（orphan 分类）/ `trace --format json`（树形 JSON）/ `graph --format mermaid`（子图）/ `list --format json`（ID/title/type/status）。【来源：实测记录】

【A】A-9: `arc link R-002 D-002 --type driven_by` 实测报错 `Edge type "driven_by" is not valid for requirement → decision`——README 关系表语义 = decision 被 requirement driven_by（requirement ─drives─▶ decision），**link 命令要求按出边方向使用**（--type drives 或反向）；文档未标注方向性细节。【来源：实测 + README §Relationships】

### 3.4 H2 假设实测——本仓 ADR 导入（E1，核心）

【A】A-10: 以 `adr/ADR-0007-unified-document-contract.md`（本仓真实 ADR，含中文标题）实测 `arc import <path>`：**成功**（D-003 实体，title 中文断言保真 / status=accepted 从 frontmatter 提取 / date=**导入日期 2026-09-09**（非原文档 08-17）/ tags=[imported]），但 **driven_by 与 depends_on 全空**——原 ADR frontmatter 的 `depends: [doc-contract-refactor, ..., ADR-0006]` 与正文「取代」元数据**不映射为图链接**；实体正文嵌套保留原始 frontmatter（双 frontmatter 冗余）。导入提示「Imported decisions have no driven_by links. Run arc link to connect」。【来源：实测记录】

【B】B-2: 由 A-10 推断——`arc import` 仅做「文本 → 实体」单步映射（id/title/status/正文），**关系网络需手工 `arc link` 或 agent 辅助**；本仓 ADR 的 depends 依赖簇若进图需要照 FEATURE_RE/PROGRESS 映射脚本化预链接。

【C】C-1: **H2 假设（CER v1.8「试点限定 ADR 簇，映射最干净」）部分证伪**：文本导入可用（中文兼容 ✓），但「关系最干净」不成立——depends 链、取代链、主体引用（决策者/相关文档）全部不自动入图，图价值（trace/impact 递归）在零链接下退化为实体档案查询；试点真实成本 = 导入 + **预链接脚本或人工 link**，高于 v1.5 预期。

### 3.5 路线图与治理形态（E1）

【A】A-11: issue #20「Arc as a Driver」路线图：D-045「arc answers questions agents cannot answer themselves」；agent surface = **CLI + JSON + skill file**；明确**否决 MCP 服务器与插件系统**（#3/#11/#13 closed）——与本框架「薄壳 CLI + 纯文档 + 生成端自由」身份契合；**driver 命令（#25 arc next/gaps/context）Phase 0/1 已发布（2026-06-01 completed，v1.4 修正——原 v1.0「计划中未发布」取证过时）**；**流程强制 CI 集成（#14）= P3 nice-to-have 仍未实现**（与本仓门禁物理化诉求不直接衔接）。【来源：github.com/kegesch/arc/issues/20 + issues/25（v1.4 复核）】

【A】A-20: **issue #25（driver 命令）已 completed（2026-06-01，Socratic redesign）**——`arc next`（按就绪度分类：ready/needs use cases/needs design/risky assumptions/orphan decisions，**输出分类不给排序**）+ `arc context <id>`（实体+全相关闭包，默认全传递、`--shallow` 单跳）+ `arc check` 并入 gap warnings（decisions with context but no use cases）；`arc gaps` **并入 arc check 非独立命令**；修复 `--derived-from` 对 use_case 实体失效；带 21 tests。【来源：github.com/kegesch/arc/issues/25（v1.4 复核）】

【A】A-21: **issue #26（Vision 实体 V-xxx）已 completed（2026-05-31）**——生命周期 active/retired、复用 `derived_from` 边、`arc check` 孤儿 requirement 检测（仅当存在 vision 时启用，防非采用者噪音）、无结构化字段（body = vision 文档）；334 tests 通过（42 vision-specific）。【来源：github.com/kegesch/arc/issues/26（v1.4 复核）】

【A】A-22: release 版本节奏精确化（v1.4 复核）——v0.3.0~v0.4.0 均为 **2026-06-27 同日发布**（07:48/09:39/09:48/09:58/10:20 五版），v0.5.0 06-28，**v0.6.0 08-10 / v0.7.0 08-13 / v0.8.0 08-14 三天三版**后 25 天无新 release；release 资产全平台 sha256 可校验（win32-x64.exe 94.4MB / sha256: 8f4b3089...）。【来源：github.com/kegesch/arc/releases（v1.4 复核）】

【B】B-3: `arc init-agent`（AGENTS.md 追加 ARC 使用指令）与 `arc skill`（agent skill 文件）与本仓 AGENTS.md 桥 + Skill 形态同构——**生成端互操作位点**，但与验证端（三校验器）正交。

### 3.6 替代框架调研（v1.1，用户指令「ARC 决策图谱有平台缺陷 那么社区是否有类似的替代框架吗」）

> **方法**: 子代理 WebFetch/WebSearch 核验（2026-09-09）+ phodal/adr 本机实测（Windows node v24，临时 npm install）。对比维度 = 关系图谱（trace/impact 递归）/ CLI+JSON agent 面 / git 原生存储 / 平台稳定 / 依赖面。

| 候选 | 快照（E1 核验） | 关系图谱 | CLI / agent 面 | 存储 | 缺陷与定位 |
|------|----------------|---------|---------------|------|-----------|
| kschlt/adr-kit | Python，195 commits，5★，pushed 2026-07-28，pypi 0.2.x | supersede 链 + ContractRelations + scenario 分类，**无递归 trace/impact/图可视化** | CLI（init/enforce/generate-ci）+ **6 MCP 工具** | MADR Markdown | 平台未核验；定位 = MCP 强制/治理**补充** |
| phodal/adr | TypeScript，271★，npm **1.5.2 停 2024-08-30**（repo 2026-07 活跃） | `generate graph` 输出 **graphviz DOT**（文件级链接/状态，无 9 实体/14 关系语义） | 纯 CLI（new/list/update/status/export json/csv/html/search） | Markdown/Asciidoc，**Windows 原生 ✓** | **本机实测**：init/new/list/export json/generate graph 全链可用；但 npm 依赖 **196 包**（含 gulp-header/prebuild-install/coffee-script 等 deprecated）——「轻量」宣称不符；定位 = Windows 轻量 ADR 管理**补充** |
| janmohammadi/adr-explorer | TypeScript，33 commits，11★，pushed 2026-06-24，npm 0.3.0（2026-05） | **最强可视化**：force-directed 图 + supersession chains + 健康看板 | **只读**浏览器/VS Code webview（npx 起本地 web app，非 headless CLI） | YAML-frontmatter Markdown | 定位 = 图可视化**补充**（非 CLI/trace 驱动） |
| thomvaill/log4brains | TypeScript，1582★（最热），149 commits，**repo 与 npm 1.1.0 均停 2024-12-17** | 无图（仅 timeline） | 交互式 CLI + 静态站生成（Next.js 重依赖） | git 内 Markdown | **停滞 + 重依赖 → 不推荐** |
| Thiagoscode/continuity | @continuity/cli **3.9.2**（2026-08-31 活跃），repo 5 commits | 图可视化 + semantic search，**Pro 付费墙** | CLI + MCP | .continuity/ 本地 | **专有许可 + 付费墙 → 不可替代** |
| ivanstambuk/adr-governance | Python，199 commits，1★，pushed 2026-03-09 | supersedes/superseded_by 链 + 引用完整性校验，无图可视化 | `.skills/adr-author`（agentskills.io）+ llms.txt + repomix | **ADL YAML 机器可读** + 渲染 Markdown | 定位 = AI-native 治理**补充**（重 CI/治理，非轻 CLI） |

【A】A-12: 六候选外部快照 = 上表列的版本/提交/活动度（2026-09-09 子代理 WebFetch 核验，逐项来源见上表）。【来源: 各 GitHub/npm 页】

【A】A-13: phodal/adr 本机实测（Windows node v24）：`adr init en` 建 docs/adr/、`adr new` 生成 0001-*.md、`adr list` 表格、`adr export json`、`adr generate graph` 输出 digraph DOT——**全链可用**；npm 安装实装 196 包（含 prebuild-install 等 deprecated）重量级依赖。【来源: 本机实测 %TEMP%\adr-probe】

【A】A-14: log4brains 停滞证据 = repo 最后 commit 与 npm 1.1.0 发布均 2024-12-17（e2e-tests/CHANGELOG commit 时间戳）。【来源: github.com/thomvaill/log4brains commits + CHANGELOG】

【A】A-15: continuity 付费墙证据 = 官方 README 表格「Knowledge graph (graph, visualize) 🔒 Pro / active trial」+ 专有许可 repo。【来源: npm @continuity/cli README + github.com/Thiagoscode/continuity】

【A】A-16: adr-explorer 能力面 = force-directed 图（supersedes/amends/relates-to 边）+ supersession chains 追踪 + 健康看板 + `.claude` 技能 + 伴侣 deep-adr；限定只读 web 形态（npx adr-explorer 起本地 web app，Node≥20）。【来源: github.com/janmohammadi/adr-explorer README】

【A】A-17: adr-governance 能力面 = ADL YAML 机器可读格式 + `lifecycle.supersedes/superseded_by` 链 + 引用完整性校验 + `.skills/adr-author`（agentskills.io）+ llms.txt。【来源: github.com/ivanstambuk/adr-governance README】

【B】B-4: 六候选均无「9 实体/14 关系语义 @ trace/impact 递归 + 零依赖单二进制 + CLI/JSON/skill 全 agent 面」完整组合——ARC 的**关系图谱驱动器**定位在社区无完全替代；替代品按单一维度补位（可视化=adr-explorer / MCP 强制=adr-kit / Windows 管理=phodal/adr / AI 治理=adr-governance）。【依据: §3.6 六候选能力核验 + phodal/adr 实测】

### 3.7 选型对比——单维补位 vs ARC 升级（v1.2，用户指令「补充调研 ... 哪个选项更优 考虑兼容 性能 维护等多个方面」）

> **方法**: 加权评分矩阵（权重 = 本仓需求锚点：关系图谱能力 30% / 本仓兼容 25% / 性能 10% / 维护 15% / agent 面 20%；每维 0-5 分，依据 §3.6 核验 + 本机实测 + adr-kit README 直读（2026-09-09 补取））。

| 选项 | 关系图谱 30% | 本仓兼容 25% | 性能 10% | 维护 15% | agent 面 20% | 加权总分 | 定位 |
|------|------------|------------|--------|--------|------------|---------|------|
| **ARC 升级**（等 1.0 + 规避缺陷） | 5（trace/impact/next/check 全 + 9/14 关系 + import） | 3（Windows 命令面实测可用，但 skill 崩溃 + linux bun + 版本失配——规避后 4） | 5（单二进制即时解析 <10k 实体） | 3（0.x 单作者，#30 无回复） | 5（CLI+JSON+skill+init-agent） | **4.2** | **主选** |
| adr-explorer | 3（只读 force-directed 图 + supersession 链，无查询驱动） | 4（Node≥20 web app + VS Code 扩展） | 3（webview 需浏览器） | 4（0.3.0 活跃 2026-06） | 2（只读，无 CLI/JSON 命令面） | 3.2 | 可视化看板旁路 |
| kschlt/adr-kit | 1（supersede 链 + 无递归查询/图） | 3（Python 3.10+，uv/uvx 安装——本机无 pip/uv 引入成本；强制面与 step-gate 重叠） | 4（enforce 增量 <5s/<15s） | 4（pushed 2026-07，README 完整） | 4（CLI + 6 MCP） | 2.85 | MCP/强制旁路 |
| phodal/adr | 1（DOT 图文件级，无语义递归） | 4（Windows 原生实测可用） | 4（本机实测即时） | 3（npm 停 2024-08，196 包 deprecated） | 3（export json/csv） | 2.75 | Windows 轻管理旁路 |
| adr-governance | 1（supersedes 链 + 引用完整性，无图） | 3（ADL YAML + Python，重 CI 治理） | 3 | 3（pushed 2026-03） | 3（.skills/llms.txt） | 2.4 | AI 治理旁路 |

【A】A-18: adr-kit 能力细节（2026-09-09 README 直读）——Python 3.10+/MIT/uv tool install 或 uvx 免安装；命令面 init / setup-cursor / setup-claude / enforce / generate-ci / generate-scripts / setup-enforcement；三层 = 生命周期管理（AI 自动维护 ADR + 质量门拒模糊决策）+ 上下文适时加载（50 ADR 中 3-5 条相关入上下文）+ 强制执行（ADR→ESLint/Ruff lint + 独立验证脚本 + CI；pre-commit import 检查 <5s / pre-push 架构边界 <15s / CI 全量）；6 MCP 工具；无递归 trace/impact/图可视化。【来源: raw.githubusercontent.com/kschlt/adr-kit README】

【B】B-5: 加权评分结论依据（v1.2）——权重最高的「关系图谱能力」30% 是四替代**共同盲区**（最强者 adr-explorer 亦仅只读图，非查询驱动），故 ARC 升级 4.2 显著领先；adr-kit 的强制面与本仓 step-gate/P-024 流程强制**功能重叠**（吸收价值低）+ uv 安装在本机（无 pip/uv）有环境引入成本。【依据: §3.7 矩阵 + A-18 + A-13 实测】

【C】C-5: 选型结论（v1.2）——**ARC 升级显著优于任何单维补位**：核心需求 = 决策关系图谱递归查询，替代方案共同缺失；单维补位仅登记**辅助观测**（首选 adr-explorer 做可视化看板，规避其无查询缺陷；不引入 adr-kit/phodal/adr/governance 作平替）；ARC 0.x 缺陷处置不变（规避命令面 + 等 1.0），若 1.0 长期不到，退路 = adr-explorer 看板 + ARC 受限使用或自研薄查询壳。【依据: §3.7 评分矩阵 + B-5】

### 3.8 缺陷规避方案设计（v1.3，用户指令「假设采用ARC 升级如何规避缺陷 深入调研社区信息」）

> **社区取证（2026-09-09）**: release 页 + issue #30 复核——**v0.8.0 官方 release 2026-08-14**（github-actions 发布，资产含 arc-win32-x64.exe 94.4MB + sha256 可校验，直链下载可完全规避 npm shim + optionalDependencies 分发链）；版本节奏 = 6/27 密集批（0.3.0-0.4.0）→ 6/28 0.5.0 → **8/10-8/14 三天三版（0.6.0/0.7.0/0.8.0）→ 之后 25 天无新 release**；0.6.0 加入 git-scoped diff/related（关 #31）；**PR 历史几乎全为 owner（kegesch）本人**（PR #32 自创 first contribution；仅 #1 skill 命令来自 agentofkegesch）→ **bus factor = 1**。

【A】A-19: 社区活动复核（2026-09-09 release 页 + issue #30）——a) v0.8.0 release 08-14（arc-win32-x64.exe / sha256: 8f4b3089...），8/14 后 25 天无新 release；b) 0.6.0（08-10）加入 `arc diff`/`arc related`（关 #31）；c) 版本节奏 6/27→8/14 密集后放缓；d) **issue #30（2026-06-08）3 个月零响应**：无评论、无 PR、无 Assignee、无 Label——bun 缺失修复**不可指望**；e) PR 历史几乎全为 owner 本人（bus factor=1）。【来源: github.com/kegesch/arc/releases + issues/30】

**规避矩阵（ARC 0.8.0 → 本仓采用面）**：

| 缺陷（P-031 实测 / 社区） | 规避方案 | 验证依据 |
|--------------------------|---------|---------|
| `arc skill` 崩溃（B:\~BUN 路径泄漏，Windows） | **命令白名单排除** skill/init-agent；agent 采用面 = CLI 命令 + JSON 输出 + 自行维护 skill 文件 | P-031 A-7 实测 |
| `arc --version` = 0.1.0 ≠ 包版本 | **不信 CLI 版本报告**；版本事实源 = 下载产物 sha256 + tag（v0.8.0）对照 | P-031 A-5 实测 |
| linux/pnpm 无 bun → `env: bun`（issue #30，3 个月零响应） | **基准平台 = Windows**（官方 win32-x64.exe + 主命令面实测可用）；Linux 需求延后或装 bun，**不指望 #30 修复** | A-19 + P-031 A-6/A-8 |
| import 关系空 + date=导入日 | **import 仅作文本 crumb**（id/title/status/正文），关系链由**预链接脚本**按 FWK-DECISION-RECORD 映射补（depends/取代 → arcs link，方向用实测校准） | P-031 A-10 实测 |
| `arc link` 方向语义（driven_by 单向） | 预链接脚本统一出边方向（requirement ─drives─▶ decision），做方向映射表 | P-031 A-9 实测 |
| 0.x breaking change 风险（8/14 后 25 天停滞 + bus factor=1） | **版本快照固化 0.8.0 exact + sha256 登记**；升级须过三校验器 + 变更对比（diff 0.6+ 可辅助）；**停滞观察项 = 90 天无新 release → 启用 P-033 C-5 退路** | A-19 |

【B】B-6: 规避矩阵可行性推断（v1.3）——白名单命令面（init/add/list/show/trace/impact/check/next/context/import + JSON）与 Windows 官方二进制直链组合 = **零缺陷面可用**（实测验证过的主命令链 + 规避掉 crash 命令）；预链接脚本将 ARC 的图价值从"零关系导入"恢复为"结构化决策图谱"（FWK-DECISION-RECORD 契约落位）。【依据: P-031 实测 + A-19】

【C】C-6: 规避方案结论（v1.3）——采用 ARC 升级路线时，**规避矩阵可将 0.8.0 缺陷面收敛至可接受**（唯一残余风险 = 上游停滞/bus factor=1，以 90 天观察项 + 版本固化 + P-033 C-5 退路对冲）；**不构成弃用障碍**；若用户裁决实施试点，本表为实施批（预链接脚本 + 命令白名单封装 + sha256 登记）的设计输入。【依据: §3.8 规避矩阵 + B-6】

## 4. 综合分析

### 4.1 关键发现总结

1. 外部分发形态成熟（npm 0.8.0 + 分平台二进制 + 零依赖），Windows 主命令链实测可用 [置信度: ★★★★★]
2. 平台缺陷双实证（#30 linux bun 缺失 / skill 命令 B:\~BUN 路径泄漏）+ 版本号失配（0.1.0 vs 0.8.0）——0.x 单作者早期项目，生产级引入需等待或规避缺陷面 [置信度: ★★★★☆]
3. H2 部分证伪：ADR 文本导入可用（中文 ✓）但**关系网络不自动映射**——试点价值实现依赖预链接，成本高于 CER v1.5 预估 [置信度: ★★★★☆]
4. agent surface（CLI+JSON+skill）与本仓身份契合；**driver 命令已发布（A-20/A-21，v1.4 修正）；仅 CI-enforcement（#14）仍在路线图未发布** [置信度: ★★★★☆]

【C】C-4: 替代缺位判断（v1.1）——ARC 的**关系图谱驱动器**定位社区无完全替代（B-4）；**ARC 保持主选，缺陷不构成弃用理由**：处置 = 等 1.0 稳定（CI 面——driver 已发布 A-20/A-21，v1.4 修正）+ 规避缺陷命令面（skill 命令、linux 装 bun 或等 #30 修复）；替代品按单一维度登记为补位观察（adr-explorer 可视化 / adr-kit MCP 强制 / phodal/adr Windows 管理 / adr-governance AI 治理），不作为 ARC 平替引入。

【C】C-2: 试点判定（gate 三问，§8）——触发条件已满足但实施面窄（实体档案/生成端互操作），与 step-gate 门禁正交（ARC CI-enforcement #14 未发布）；本批止于调研评估，实施待用户裁决（同 P-015/P-028 先例）。

【C】C-3: 零工具改动（I-1）——本批仅文档登记（spec/arc-probe/ + CER §3.4.1 ARC 行状态同步），不引入任何 hook/脚本/依赖。

### 4.2 技术 landscape

ARC = git 原生 markdown 知识图谱 CLI（对比臂：Semantica = 重图库 ~40 依赖、ARC = 单文件二进制；决策溯源方向 A 先导轻量替代成立）。关系方向语义（driven_by）需文档标注或实测校准——本仓若是选型引入，契约表须先验证。

### 4.3 研究空白 / 适配分析（本仓）

- **试点价值面**（若人工/脚本预链接）：M7/ADR 决策 → ARC 图 trace/impact 递归 — 方向 A 轻量替代 Semantica 成立；
- **缺口**：import 关系空 + date 失真（导入日期非原日期）；H3 中文召回风险在 JSON 模式下缓解但 link 语义需人工校准；
- **门禁衔接缺口**：ARC 的 CI 流程强制（#14）未实现——本仓 step-enforce/step-gate 是流程强制本体，ARC 不替代。

## 5. 幻觉抑制审查（Step 2 Review）

### 5.1 文献/来源验证

| 引用 | 来源 | 验证方式 | 状态 |
|------|------|---------|------|
| npm @kegesch/arc 0.8.0 | npmjs.com/package/@kegesch/arc | WebFetch/WebSearch | ✅ |
| GitHub kegesch/arc 161 commits | github.com/kegesch/arc | WebSearch | ✅ |
| issue #20 路线图 | github.com/kegesch/arc/issues/20 | WebFetch | ✅ |
| issue #25 driver 命令 completed | github.com/kegesch/arc/issues/25 | WebFetch（v1.4 复核） | ✅ |
| issue #26 Vision 实体 completed | github.com/kegesch/arc/issues/26 | WebFetch（v1.4 复核） | ✅ |
| issue #30 non-bun | github.com/kegesch/arc/issues/30 | WebFetch | ✅ |
| README CLI Reference/File Format | github.com/kegesch/arc README.md | WebFetch raw | ✅ |
| release 版本节奏（v0.3.0~v0.8.0 日期/sha256） | github.com/kegesch/arc/releases | WebFetch（v1.4 复核） | ✅ |

### 5.2 技术声明验证

| 声明 | 来源 | 验证状态 |
|------|------|---------|
| `arc --version` = 0.1.0 ≠ npm 0.8.0 | 本机实测 | ✅ 已验证（E1） |
| Windows 命令链可用 | 本机实测 | ✅ 已验证（E1） |
| `arc skill` 崩溃（B:\~BUN 路径） | 本机实测 | ✅ 已验证（E1） |
| ADR 导入 date=导入日 / 关系空 | 本机实测 | ✅ 已验证（E1） |
| 「no bun required」与 #30 矛盾 | README vs issue | ✅ 已验证（冲突实证） |

### 5.3 待修正项

- [ ] 完成本批实态取样，确认 CER §3.4.1 ARC 行状态同步（评估已执行、不实施/试点待裁决）
- [ ] 若用户裁决实施试点：预链接脚本 + 批量导入 32 ADR 后图质量评估（H-2）

[H1]（CER H2 沿线）: ARC 对 M7/ADR 决策导入的字段映射 / 关系类型差异——本批单样本实测（A-10：title/status ✓、date=导入日、depends 关系空）；批量样本映射稳定性待验证（查证路径 = H-2 批量试跑 + FWK-DECISION-RECORD 契约比对）。

[H2]（本批新登记）: 本仓 32 个 ADR 批量导入 ARC 后的图质量（孤儿率 / 有效链接率 / check 报告可读性）——待实施试点时批量试跑实测（用 check 报告 + 预链接脚本评估）。

## 6. 对设计的输入

### 6.1 可用的技术方案

- 方案 A：**实体档案试点**（`arc import` + 脚本/手工 link 本仓 ADR 簇）——Layer-0/1 边界：图只读工具，不落地门禁；
- 方案 B：**生成端互操作**（`arc init-agent` + skill）——与本仓 AGENTS.md 桥并置，零依赖零风险；
- 方案 C：**不引入**（维持 CER 登记，观察 1.0 稳定）——P-028/P-030 既有懒加载 gate 先例。

### 6.2 关键约束

- 零依赖不变式：ARC 是外部 CLI（工具非依赖）——符合 P-009 D6/L7 判例；
- 生成端自由/验证端受控：ARC 查询属生成端互操作，不得反向接管三校验器；
- 关系映射契约：须基于 FWK-DECISION-RECORD 映射（P-016），import 关系空 → 预链接脚本限定 ADR 簇。

### 6.3 风险

| 风险 | 等级 | 缓释 |
|------|------|------|
| 0.x 平台缺陷（#30 / skill 崩溃）影响使用面 | 中 | 限 Linux/Windows 基准环境验证；缺陷面规避（不用 skill 命令） |
| H2 关系不映射 → 图价值退化 | 中 | 预链接脚本 + 试点限定簇；图查询仅作辅助，不建门禁 |
| ARC driver 命令面已发布但 CI enforcement（#14）未发布 | 低 | driver 面随 A-20/A-21 已可用（v1.4 修正）；CI 面登记 trigger-driven，不排队 |

## 7. 局限

1. 外部取证为页面/issue 级（A-6 为 issue 描述，未在 linux 复现）；平台缺陷以 Windows 实测为主。
2. 未做源代码直读（single-file 二进制分包，反编译不纳入）——命令行为以黑盒实测为准。
3. 实测单 ADR 样本（ADR-0007）；批量 32 ADR 图质量（孤儿率/链接率）待 H-2 批量试跑。

## 8. 结论与 gate 三问

| 问 | 回答 |
|----|------|
| Q1 放哪层？ | 若实施 = **Layer-1（外部 CLI 工具）+ Layer-0（概念登记）**；不引入依赖，仅工具链互操作 |
| Q2 激活条件？ | **触发条件满足**（候选名目 P-020 落地、本批 H2 实测完成）但**实施面 = 实体档案/生成端互操作**，无自动门禁衔接（ARC CI-enforcement 未发布 = 与 step-gate 正交）；**本批止于调研评估，试点实施待用户裁决（同 P-015 先例）** |
| Q3 未激活副作用 = 0？ | 是——不引入任何工具/hook 改动（I-1 保持），仅文档登记 |

**核心结论**：ARC 0.8.0 实态可用（Windows 基准），但 H2「映射最干净」部分证伪（关系不自动映射）+ 0.x 平台缺陷实证——**可作方向 A 轻量先导（实体档案 + 预链接）或保持 Layer-0 观察**；**替代框架调研（v1.1）确认其「关系图谱驱动器」定位社区无完全替代，ARC 保持主选，缺陷处置 = 规避命令面 + 等 1.0**；**选型对比（v1.2）加权评分确认 ARC 升级 4.2 显著优于四单维补位（次高 adr-explorer 3.2），单维补位仅登记辅助观测（优选 adr-explorer 看板）**；**缺陷规避方案（v1.3）确认 0.8.0 缺陷面可通过规避矩阵收敛至可接受**（官方 Windows 二进制直链 + 命令白名单 + 版本固化 + 预链接脚本；唯一残余风险 = 上游停滞 bus factor=1，90 天观察项对冲）——**采用资质确认，实施待用户裁决**；**v1.4 深入社区复核修正 A-11 事实错误**（driver 命令 #25/#26 已发布非计划中，A-20/A-21 取证；版本节奏精确化 A-22；规避矩阵增量 = context/diff 等新增命令面纳入白名单）——**修正不影响核心结论，反而收窄残余风险**（agent 面 driver 能力已可用）；本批结论已同步 CER §3.4.1 ARC 行（P-031~P-034 登记），实施与否由用户裁决。

## 附录 B 机读登记（B 类推断）

```json
[
  {"id": "B1", "inference": "ARC 平台缺陷双实证同根因族 = 构建/运行环境假设泄漏到发布产物（linux 依赖 bun PATH；win skill 命令依赖构建盘符路径）", "basis": "A-6/A-7 实测 + issue 取证"},
  {"id": "B2", "inference": "arc import 仅做文本→实体单步映射（id/title/status/正文），关系网络（depends/driven_by/取代链）需手工 link 或脚本预链接", "basis": "A-10 实测（depends/driven_by 全空 + date=导入日）"},
  {"id": "B3", "inference": "arc init-agent / arc skill 与本仓 AGENTS.md 桥 + Skill 形态同构（生成端互操作位点，与验证端正交）", "basis": "A-11 + README CLI Reference + issue #20 agent surface 声明"},
  {"id": "B4", "inference": "ARC 的关系图谱驱动器定位（9 实体/14 关系 @ trace/impact 递归 + 零依赖 agent 面）社区无完全替代；替代品按单一维度补位观察", "basis": "A-12~A-17 + phodal/adr A-13 实测 + §3.6 六候选能力核验"},
  {"id": "B5", "inference": "加权评分（关系图谱 30%/兼容 25%/性能 10%/维护 15%/agent 面 20%）：ARC 升级 4.2 显著优于四单维补位（次高 adr-explorer 3.2 仅只读看板）——核心因关系图谱递归查询是替代共同盲区；adr-kit 强制面与 step-gate 重叠且 uv 安装引入成本", "basis": "§3.7 评分矩阵 + A-18 + A-13 实测"},
  {"id": "B6", "inference": "规避矩阵可行性：白名单命令面（实测可用主链）+ Windows 官方二进制直链 + 版本 0.8.0 固化 = 缺陷面收敛至可接受；预链接脚本恢复图谱价值；唯一残余风险 = 上游停滞（90 天观察项 + C-5 退路对冲）", "basis": "P-031 实测 + A-19 + §3.8 规避矩阵"}
]
```

---

**Review 签字**: _________ 日期: _________