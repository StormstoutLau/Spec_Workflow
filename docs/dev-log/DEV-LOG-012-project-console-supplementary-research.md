# DEV-LOG-012: 项目控制台补充调研（project-console）—— hook 链表乱码定位 + 步骤级动态描述 + 锚点与映射收敛待办

> **日期**: 2026-09-11（回补）
> **会话**: `specwf-p045-20260911.jsonl`（五步决策链：research / design / implement / verify / finalize）
> **涉及**: spec/project-console/RESEARCH.md（v1.2 → **v1.3**，45A+9B+16C+4H）/ docs/PROGRESS.md / CODE_WIKI.md（v1.46 → v1.47）/ docs/CONSOLE.md
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [RESEARCH](../../spec/project-console/RESEARCH.md) / [DESIGN](../../spec/project-console/DESIGN.md) / [CHECKLIST](../../spec/project-console/CHECKLIST.md) / [PROGRESS](../PROGRESS.md) / [CODE_WIKI](../../CODE_WIKI.md) / [CONSOLE](../../docs/CONSOLE.md) / [session](../../tools/spec_runner/sessions/specwf-p045-20260911.jsonl)

## 做了什么（时序）

1. **立案（research 步）**：用户指令三问——hook 链表格「有乱码、看不懂」/ per-feature 流程缺每步骤的动态描述（主题、创建时间、简要描述、修改历史）/ 剩余待办一并调研。三题拆分后先做**机械确证**。
2. **证据采集（A-37~A-45，9 条）**：
   - **A-37** 表列数不齐机械确证：表头 **5 列** vs 第 3/4/5 行 **11/8/10 cells**；根因 = `files` 正则内**未转义的半角 `|`** 被 GFM 当列分隔符（**视图自身破坏渲染**，非宿主问题）。
   - **A-38** 长无断点 token 撑宽列，挤压后续列至 5–10px，且 GitHub 表格**不截断**。
   - **A-39** hook 的 `name:`（人类可读作用）**已在真值源却未被解析**。
   - **A-40** 事件流主源齐备：**31 session / 130 decision rows**，`scenario` + `outcome` + `reasoning` **100% 零缺失**；step 分布 research 30 / design 26 / implement 25 / verify 25 / finalize 24。
   - **A-41** 四文档 H1 **77/77** 齐备；**A-42** 文档元数据稀疏且命名漂移（`创建日期` 50/77、`Spec 步骤` 54/77、front-matter 25/77、文档内「修订历史」章节仅 13/77 且**四种以上标题形态**）；**A-43** `Spec 步骤` 行可作制品↔步骤映射第一来源（54/77）。
   - **A-44** 官方「Custom anchors」节**只背书 `<a name>`** 且明示不进 outline/TOC；`<a id>` 无官方背书且存在**冲突证据**（第三方称 GitHub 剥离 `class`/`id`，已标注为存疑来源）；HTML5 中 `name` 已弃用而 `id` 为标准 ⇒ 两形态各有失效面。
   - **A-45** 折叠块**无数量上限**（官方仅约束 summary 后空行 + 嵌套 ≤4 层），26 块属**认知负载**而非技术限制。
3. **四项判定落档（design 步，RESEARCH v1.3）**：C-13 hook 链表重构 / C-14 四字段来源链 / C-15 锚点双属性 / C-16 映射语义与收敛；新增推断 **B8**（列表优于表格）/ **B9**（事件流为步骤描述主源）；开新假设 **H8**；附录 A 扩至 A-45（本仓 17 / 社区 28）。
4. **落档（implement 步）**：新增 §7.8（hook 链表乱码与可读性）/ §7.9（步骤级动态描述）/ §7.10（剩余待办），**续编 §7.8-§7.10 刻意不改号**（规避 v1.1 编号顺延连锁修正）；§0 断言表改 45A+9B+16C+4H。**本批零工具改动**（`scripts/` 与 hook 零 diff）——止于调研，C-13/C-14 待实施批落码。
5. **验收（verify 步）**：三校验器全绿 + `step-enforce --pid P-045` 五步链 exit 0 + `verify-anchor` 锚点全真实 + **不改号核验**（v1/v2/v3 session 既有锚点无需连锁修正）。
6. **收束（finalize 步）**：PROGRESS P-045 行（依据列同样**不落 `spec/<feature>/` markdown 链接**）+ CODE_WIKI v1.47（版本头 / `declared.progress_tasks` 44→45 / §2.1 树 / §9 索引）+ `docs/CONSOLE.md` 重生成；**零新增 M7 样本**。

## 决策依据

### ① hook 链表乱码定性为「视图自身破坏渲染」（C-13）
机械确证表列数不齐（A-37），根因是**未转义半角竖线被 GFM 当列分隔符**——**非宿主问题**；叠加 A-38 长 token 压列。⇒ 处置 = **弃表格改逐 hook 列表块**（`id` —— `name` 作用 + 缩进 `命令` / `触发范围`（正则独立成行）/ `传入文件名`）+ **补解析 `name`**（缺则 `—`）+ **外部文本安全化升为通则**（P-044 仅对描述列做 `_cell()`，**hook 表遗漏即本缺陷直接成因**）。

### ② 步骤级四字段以**事件流为主源**（C-14）
主题 `scenario` / 创建时间 `ts` / 简要 `outcome` / 修改历史 = 该 P 的 **session 轮次清单**；文档元数据（A-42 稀疏且命名漂移）仅逐级回退、缺失显式 `—`（守 I-8）；`reasoning` **不进视图**（守 C-6 单一认知块）。

### ③ 锚点用**双属性保险**（C-15）
官方只背书 `name`、`id` 是 HTML5 标准但存活率有冲突证据（A-44）⇒ `<a name=… id=…></a>` 覆盖两类渲染器；新开 **H8**（真机存活率；失效后果仅「可折叠不可跳转」）。

### ④ C-11 映射再修正为 **C-16**（语义反转 + 收敛为共享模块）
A-33 的失效形态是**两实现同错** ⇒ 一致性对账**抓不住**（已证伪选项「双实现 + 对账」）⇒ ① **改语义**（`CODE_WIKI §9` 行标注**优先**、`PROGRESS` 行首链接**兜底**、`—` 显式缺口，预期缺口 **4 → 0**）② **收敛选抽共享纯函数模块**（如 `scripts/spec_map.py`，语义同源唯一保证；代价 `declared.scripts` 7→8）③ **不改历史 `PROGRESS` 行**（读取端解决）。源 = PROGRESS P-045 行 + [RESEARCH](../../spec/project-console/RESEARCH.md) §7.8-§7.10。

## 遇到的问题

- **表列数不齐（A-37）**：视野内第一条**由视图自身造成**的渲染缺陷（未转义竖线）。
- **长无断点 token 压列（A-38）**：GitHub 表格不截断 ⇒ 末列被压至 5–10px。
- **文档元数据命名漂移（A-42）**：四文档「修订历史」章节仅 13/77 且四种以上标题形态 ⇒ 元数据不可作主源。
- **存疑来源（A-44）**：关于 GitHub 是否剥离 `id`/`class` 存在**冲突证据**，已**标注为存疑**、未作定论。

## 下一步

- **C-13 / C-14 待实施批落码**（后由 P-046 号批落地：hook 链列表块 + 步骤级六列表）。
- **C-15 / C-16 单独处理**（后由 P-047 号批落地：锚点双属性 + 映射改调共享模块 `spec_map`）。
- **H6 / H7 部分回填但不关闭**；**H8**（双属性锚真机存活率）待实测。源 = [CHECKLIST](../../spec/project-console/CHECKLIST.md) §9。