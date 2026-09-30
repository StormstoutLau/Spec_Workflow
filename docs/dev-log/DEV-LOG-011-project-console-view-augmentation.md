# DEV-LOG-011: 项目控制台视图增补（project-console）—— 描述列 + per-feature 折叠流程 + 架构图「显式关系」口径

> **日期**: 2026-09-11（回补）
> **会话**: `specwf-p044-20260911.jsonl`（五步决策链：research / design / implement / verify / finalize）
> **涉及**: spec/project-console/（DESIGN v1.0 → v1.1 + IMPLEMENTATION v1.0 → v1.1 + CHECKLIST v1.0 → v1.1 accepting）/ scripts/console_gen.py（三项增补）/ docs/CONSOLE.md（重生成 514 行 / 20027 B）/ docs/PROGRESS.md / CODE_WIKI.md（v1.45 → v1.46）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [DESIGN](../../spec/project-console/DESIGN.md) / [IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) / [CHECKLIST](../../spec/project-console/CHECKLIST.md) / [RESEARCH](../../spec/project-console/RESEARCH.md) / [PROGRESS](../PROGRESS.md) / [CODE_WIKI](../../CODE_WIKI.md) / [CONSOLE](../../docs/CONSOLE.md) / [session](../../tools/spec_runner/sessions/specwf-p044-20260911.jsonl)

## 做了什么（时序）

1. **立案（research 步）**：用户指令「好的，按 C-9/C-10/C-12 落代码」——承接 P-042 RESEARCH v1.2 三项裁定；**C-11 按用户指定排除**。勘察 = 采样 32 feature 的四文档 H1 形态（确认 H1 均在首个 `# ` 行、front-matter 与代码块内 `#` 天然排除）。
2. **设计（design 步，DESIGN v1.1）**：新增 D8 描述列 / D9 per-feature 流程与交互 / D10 架构图口径修正 + **不变式 I-8**；替代方案 C 否决（Mermaid `click`）。
3. **实施（implement 步）**：`scripts/console_gen.py` 三项增补——新增常量（`DESC_CAP` / `DESC_ARTIFACT_ORDER` / `DESC_TITLE_PREFIX_CAP` / `TRUTH_NODES` / `DECLARED_SOURCES` / `ENTRY_SCRIPT_RE` / `H1_RE`）+ 函数（`first_h1` / `_strip_tail_group` / `shorten_title` / `feature_desc` / `feature_stage` / `_cell` / `_arch_section` / `_feature_process_section`）；`render` 增 §5.1；`_dep_section` **取代**为 `_arch_section`（不并存）。
4. **验收（verify 步）**：selftest **16/16 → 27/27 PASS**（新增 S17-S27）+ 三校验器全绿 + `step-enforce --pid P-044` 五步链 exit 0 + `verify-anchor` 锚点全真实 + 产物体量核对（514 行 / 20027 B）。
5. **收束（finalize 步）**：IMPLEMENTATION v1.1 + CHECKLIST v1.1 + PROGRESS P-044 行 + CODE_WIKI v1.46；**仍是单脚本 / 单产物 / 单 hook，零新依赖**；**零新增 M7 样本**。

## 决策依据

### ① 描述列取「制品自身 H1 标题」优先链（C-9）
来源优先链 = 制品 H1（`RESEARCH` → `DESIGN` → `CHECKLIST*`）→ 关联 P 行「事项」→ 目录名；**刻意不引 `CODE_WIKI §9` 文本**——§9 属派生视图，引用会形成「视图依赖视图」并使描述成为**第二真值源**（B6 / I-6）。主名收敛 = 去「调研文档：」类前缀（冒号位置 ≤ 12 字符）→ **交替**剥「结尾配对括号组」与断 `——` 至稳定 → 截断 `DESC_CAP = 40`（H6 渲染宽度校准仍待实测）。

### ② per-feature 流程默认折叠，且**排除 Mermaid `click`**（C-10）
默认展示项目级「架构与流程」，per-feature 为次级层**默认折叠**（新增 §5.1：锚点目录 + 每 feature 一个折叠块，摘要 `{feature} ｜ {阶段} ｜ {关联 P}` + 四文档管道 `flowchart LR` + 决策链 step 序 + 派生状态）。`click` 被排除因官方 config schema 默认 `securityLevel: "strict"` 即禁用，`loose` 为**三起 XSS 实证载体**（本仓无法控制宿主渲染器 ⇒ 不可得且不安全）。收敛策略 = 仅对「四文档不全 **或** 有关联 session」的 feature 出图（实测 **26 个**，排除 6 个四文档齐备且无 session 者；折叠对 **26:26** 平衡）。

### ③ 架构图改「显式关系」口径（C-12，系对 C-8 的**部分修正**）
A-35 实测本仓 import 图**为空** ⇒ 口径改为 ① `hook → script`（`entry` 直读）② `script → 真值源`（**显式架构契约常量** `DECLARED_SOURCES`，Layer-0 文档化于 DESIGN §6.4）③ `import` 边（`ast` 提取，**有则绘、无则不占位**）；实测出 **12 条显式关系边**。**与 C-8「不需要显式元数据」不矛盾**——C-8 否决的是「为**推断 import** 加元数据」，此处以**已声明契约**替代不可得推断且不新增采集面。

### ④ 依据列刻意不落 `spec/<feature>/` markdown 链接
「行内首个 spec 链接」是 `feature_pid_map` 的映射语义，落链接会把 `project-console` 的关联 P 由 P-043 翻转为 P-044，而 C-11 已裁定「映射收敛」不在本批 ⇒ 避免引入新歧义。源 = PROGRESS P-044 行 + [session](../../tools/spec_runner/sessions/specwf-p044-20260911.jsonl) 第 5 条。

## 遇到的问题

- **DR-8（真实仓首跑即现）**：主名收敛必须**交替**剥括号组与断 `——`，否则 `独立验证（出路 C——…）` 会被截成 `独立验证（出路 C`；本已修正。
- **DR-9（首轮拦截）**：**S23 hook 节点 id** 命名不彻底 → 统一 `H_{id}` 前缀。
- **S4 fixture 未加描述列断言**（两次首跑拦截之一，已补）。源 = [IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) §6 + [session](../../tools/spec_runner/sessions/specwf-p044-20260911.jsonl) 第 3/4 条。

## 下一步

- **C-11（映射收敛）不在本批**——显式缺口保留 `—`，待后续批（P-045 起改由 C-16 承担）。
- **H6/H7 由本批实测部分回填但不关闭**（`DESC_CAP=40` 属扫描性阈值；折叠块体积预算部分回填）。源 = [CHECKLIST](../../spec/project-console/CHECKLIST.md) §9。