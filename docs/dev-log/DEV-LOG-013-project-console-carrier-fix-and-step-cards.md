# DEV-LOG-013: 项目控制台承载修复与步骤级动态描述（hook 链弃表格改列表块 + 步骤六列表 + 不变式 I-9）

> **日期**: 2026-09-11（回补）
> **会话**: `specwf-p046-20260911.jsonl`（五步链：research / design / implement / verify / finalize）
> **涉及**: spec/project-console/（DESIGN v1.1 → v1.2 / IMPLEMENTATION v1.1 → v1.2 / CHECKLIST v1.1 → v1.2 accepting）/ scripts/console_gen.py / docs/CONSOLE.md（重生成 514 行 20027 B → 729 行 45709 B）/ docs/PROGRESS.md（P-046 行）/ CODE_WIKI.md（v1.47 → v1.48）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-046](../PROGRESS.md) / [project-console RESEARCH](../../spec/project-console/RESEARCH.md) / [project-console DESIGN](../../spec/project-console/DESIGN.md) / [project-console IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) / [project-console CHECKLIST](../../spec/project-console/CHECKLIST.md) / 会话 `tools/spec_runner/sessions/specwf-p046-20260911.jsonl`

## 做了什么（时序）

1. **research 步**：承接 P-045 RESEARCH v1.3 已完成的调研面（§7.8 / §7.9 的 A-37 至 A-43 取证与 C-13 / C-14 四字段来源链），本步只做**落码输入确认**；用户指令「先执行 C-13 和 C-14，C-16 共享模块单独处理」⇒ C-15 / C-16 **不在本批**。
2. **design 步**：DESIGN v1.2 落档，新增 **D11（hook 链表形态，§6.5）** + **D12（步骤级动态描述，§6.6）**，并在 §3.3 新增不变式 **I-9（承载安全）**；§6.5 记录替代方案 D（保留表格 + 仅转义竖线）否决；其余变更面 = §1 新增设计目标第 9 / 10 条、§2 依据表新增 A-37 至 A-39 与 A-40 至 A-43 两行、§3.2 模块表同步、§4 输出契约 §5 / §5.1 行更新、§9 增 P-046 必改与边界。
3. **implement 步**：`scripts/console_gen.py` 落码——`hook_chain` 增解析 `name`（缺则 `—`）；新增 `_hook_list` 弃表格改逐 hook 列表块并替换 hook 表；`_cell` 升为**通则**，新增 `_clip` / `_fmt_ts`；`SessionInfo` 增 `records`，`read_sessions` 累积全部轮次（轮次标签 = session 文件名排序序号，守 I-2 确定性）；新增 `_step_table` 六列并插入 per-feature 折叠块，摘要追加 `｜ n 轮`；新增 `STEP_ARTIFACT` / `STEP_CAP` 常量。selftest **27/27 → 34/34 PASS**（新增 S28 至 S34）。IMPLEMENTATION v1.2（A-7 / A-8 实测 + 新签名 + DR-11 / DR-12 + 附录 B 增 B3）与 CHECKLIST v1.2（F16 / F17 + I-9 行）落档。
4. **verify 步**：真实仓读数 = hook 链 **5 条列表块**（各带 `name`；4「否」+ 1「未设」）、折叠块 **26**（`<details>` : `</details>` = 26:26）、锚点 26、步骤表 **26 张 / 81 行**、多轮进摘要 2 例、无 session 显式缺失 9 处；**I-9 全表机械核对 19 张表格 / 0 张列数不齐**（P-044 首跑为 hook 表 3 行不齐，本批归零）；三校验器 0 违规；`step-enforce --pid P-046` 五步链 exit 0；`verify-anchor` 锚点全真实。
5. **finalize**：PROGRESS 新增 P-046 行（依据列**不落** spec 目录 markdown 链接，保持 `feature_pid_map` 语义稳定）+ CODE_WIKI v1.47 → v1.48（§2.1 树 / §9 索引 / declared.progress_tasks 45 → 46 / PT-11 P 区间）+ `docs/CONSOLE.md` 重生成；**零新增 M7 样本**（本批为准入性修复与视图增补，无新增计数声明位点）。

## 决策依据

### ① 为什么弃表格改列表块（D11，C-13）
根因双条：**A-37** 产物 hook 表**表列数不齐**（表头 5 列 vs 第 3/4/5 行实为 11/8/10 个单元格），因 `files` 正则原样入格且正则内含**未转义半角 `|`**，被 GFM 当列分隔符——**视图自身破坏渲染，非宿主问题**；**A-38** 长无断点 token 撑宽本列并把后续列挤至 5 至 10px，GitHub 表格**不截断**。弃表格改列表块让长 token **独占一行**，从形态上**同时**消除两类缺陷；「保留表格 + 仅转义竖线」（方案 D）只消解前一类（DESIGN §6.5）。可读化处置 = `pass_filenames` 三态（`false` → 「否」/ `true` → 「是」/ 未设 → 「未设（pre-commit 默认『是』）」），`entry` **原样展示、不做美化转述**（避免与真值源产生第二叙事）。

### ② 为什么以事件流为步骤描述主源（D12，C-14）
**A-40** 实测事件流三字段（`scenario` / `ts` / `outcome`）**100% 齐备**，对照 **A-42** 文档元数据稀疏且命名漂移（创建日期 50/77、Spec 步骤 54/77、front-matter 25/77、文档内修订历史 13/77 且四种以上标题形态）⇒ 以事件流为主源、文档元数据仅**逐级回退**；主源为事件流 = **零新增采集面**。同 step 多轮**最新一轮胜出**、修改历史列全轮次；`reasoning` **不进视图**（守 C-6 单一认知块）。

制品↔步骤映射以文档自声明 `Spec 步骤` 行为第一来源（A-43，实测 54/77），回退常量 `STEP_ARTIFACT`（research→RESEARCH / design→DESIGN / implement→IMPLEMENTATION / verify→CHECKLIST；finalize 不新增制品）。

### ③ 为什么把竖线安全化升为不变式 I-9
P-044 仅对**描述列**做 `_cell()`，**hook 表遗漏**正是本缺陷直接成因 ⇒ 通则化为「凡进入表格单元格的外部文本一律过 `_cell()`」+「长无断点 token 不得落入表格单元格」，落 §3.3 I-9。

## 遇到的问题

- **hook 链表乱码**：即 P-045 遗留的 P1 缺陷（A-37），本批 C-13 修复；根因是视图自身（未转义半角竖线），非宿主渲染器问题。
- **无 session 的 feature 步骤描述**：处置为**单行显式缺失**（I-8），不用稀疏且命名漂移的文档元数据「补得像有」（A-42）。
- **H6 / H7 未关闭**：渲染宽度校准与体积预算本批**部分回填但未关闭**（详见 feature 四文档）。

## 下一步

- **C-15（锚点双属性）/ C-16（映射语义反转 + 共享模块）保留后续批**；C-16 因需新增共享模块而单独处理。
- 维护纪律：`CODE_WIKI §9` 行与 feature 主 P 的同步要求本批尚未建立（于 P-047 建立）。