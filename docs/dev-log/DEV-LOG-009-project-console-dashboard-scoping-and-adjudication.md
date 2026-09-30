# DEV-LOG-009: 可视化看板剥离与视图分层（project-console）—— 诊断 BOARD.md「结构性简陋」、裁定底座归属，并延伸至状态归属契约与 P2b 迁移的多轮调研

> **日期**: 2026-09-11 至 2026-10-01（回补）
> **会话**: tools/spec_runner/sessions/ 下 `specwf-p042-20260911.jsonl` / `specwf-p042-20260911v2.jsonl` / `specwf-p042-20260911v3.jsonl` / `specwf-p042-20260929.jsonl`（含 v2~v9）/ `specwf-p042-20260930.jsonl`（含 v2~v8）/ `specwf-p042-20261001.jsonl`（含 v2/v3/v4），**共 24 条**
> **涉及**: spec/project-console/（RESEARCH v1.0 → v1.24 + DESIGN v1.0 → v1.11 + IMPLEMENTATION v1.0 → v1.20 + CHECKLIST v1.0 → v1.17）/ scripts/console_gen.py / tools/spec_runner/spec_runner.py / spec/independent-verify/DESIGN.md / spec/doc-contract/PLAN.md / spec/board-generator/DESIGN.md / docs/PROGRESS.md / CODE_WIKI.md / docs/CONSOLE.md
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [RESEARCH](../../spec/project-console/RESEARCH.md) / [DESIGN](../../spec/project-console/DESIGN.md) / [IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) / [CHECKLIST](../../spec/project-console/CHECKLIST.md) / [PROGRESS](../PROGRESS.md) / [CODE_WIKI](../../CODE_WIKI.md) / [CONSOLE](../../docs/CONSOLE.md) / [spec_runner.py](../../tools/spec_runner/spec_runner.py) / [independent-verify DESIGN](../../spec/independent-verify/DESIGN.md) / [doc-contract PLAN](../../spec/doc-contract/PLAN.md) / [board-generator DESIGN](../../spec/board-generator/DESIGN.md)

## 做了什么（时序）

1. **2026-09-11 调研立案（RESEARCH v1.0，16A+3B+4C+4H）**：用户指令指向 BOARD.md「看起来有些简陋」并追问三档状态定义、脉络/架构/流程展示、以及「可视化看板需要从学术推理调研单独剥离出来」。取证 = 源码核对 + 机械重数 + 六轮检索。现状诊断 A-1~A-4 = 三档 = `PROGRESS` 状态列**逐字直译**（A-1）/ 三组恒空为**结构性必然**（A-2：`done` 41 行 vs 活动态合计 0 行）/ 「⚠ 待你审」与 `pending` **语义错配**（A-3）/ 四维缺失（A-4）。
2. **社区四类取证 + 裁定 C-1~C-4**：①制品链与步骤时间线 ②diagram-as-code ③执行轨迹与决策链 ④双向追溯。裁定 = C-1 **简陋是结构性非审美**（改渲染无解）/ C-2 **剥离**为通用底座 feature `spec/project-console/`、**接续取代 P-041**（board-generator 记前身 L0 首落点）/ C-3 **Layer-1 只读派生视图**、止于 ADR-0010 懒加载 gate / C-4 承载 = markdown-native（Mermaid 优先），**零服务器零新依赖**。**真值源盘点（A-16）** = spec 子目录 32 / 会话 22 / 脚本 7 / hook 5 / ADR 8（零新增采集面）。本批**零工具改动**。
3. **v1.1 遗留四项关闭（28A+5B+8C+1H）**：H1 状态词表 → C-5 派生状态机 + 词表对齐（**废止「⚠ 待你审」升格标签**）；H2 主键粒度 → C-6 双主键分层 + 活动区上限 5~7；H3 渲染依赖 → C-7 限定 markdown 内嵌 Mermaid + 纯 CSS 折叠（**排除 mmdc 自建渲染**）；H4 依赖元数据 → C-8 不需要（`ast` 可机械消解；实测动态 import 仅 1 处且为字面量）。
4. **v1.2 三题（36A+7B+12C+3H，续编 §7.5-§7.7 刻意不改号）**：§7.5 描述列 → C-9 描述源取「制品自身 H1 标题」优先链；§7.6 架构/流程与交互 → C-10 默认项目级 + per-feature 折叠，**排除 Mermaid click**（三起 XSS 实证载体）；§7.7 两处真实问题 = **A-35 本仓 import 图实测为空** → C-12 架构图改「显式关系」口径；**A-33 feature→P 映射 4 空洞**（`step_enforce` 与 `console_gen` 共用「P 行内首个 `spec/<feature>/` 链接」语义）→ C-11。新开 H6/H7。
5. **追记轮（2026-09-29 起，登记型 Layer-0）**：v1.5 §7.11 正式观察项（「无决策事件的文档订正轮 ⇒ 控制台不可见」）+ H9；v1.6 §7.12 看板与架构可视化——九候选社区成熟件**无一可直接复用**（C-17）+ 四阶段升级路线（C-18）；v1.7 §7.12（八）「允许外部依赖」候选矩阵（C-19），**核心判定「换工具 ≠ 自动更新」**。
6. **v1.8 状态归属契约（47A+10B+20C+5H，**零代码**）**：§7.13 + 契约条款 S-1/S-2/S-3 + 落地 `PLAN §1` 新增 **DC2.1 任务状态词表（+「来源」列）**、`PROGRESS` L3 声明改指向；DESIGN v1.5 新增 D16。
7. **v1.9 P2 立项取证 → v1.10 V2 实测（**零代码**）**：§7.14 A-48 状态列时间序列机械重数 + A-49 拐点定位（`45cb402`）；§7.15 A-50 V2 双向完备率 = session→P **100%**（55 条合规流 / 34 个不同 P 值 / 孤儿 0）、P→session **59.6%**（57 行中 34 行）→ C-22 **V1 裁定 = 登记时点前移**。
8. **v1.11~v1.16 登记与复核（**零代码**）**：DR-18（`repo_stats` PT-11 把正文 P 区间误捕为读数）/ DR-19（session 非法 JSON 转义 + 门禁报错不定位文件行）；v1.12 §7.16 A-51/A-52/B13/C-23（**P2 拆 P2a/P2b**；兜底通道偏差 **18/35 = 51.4%**）；v1.13 DR-21（锚点路径约束未成文）；v1.14 §7.17 三项细化；v1.15 §7.18 三项待裁决裁定 + P0 批四文档实施设计；v1.16 §7.19 迭代回写机制评估 + DR-18 两条裁定回写。
9. **v1.17 P0 小实施批（Layer-1，**首次改 `scripts/console_gen.py`**）**：P2a `derive_state` 拆支（`state` 仍永远 = `task.status` 原词 ⇒ 不触 I-7）+ 实施期发现 DR-23 第四处可见位点；**selftest 37/37 → 41/41**；V2a 补建 4 条 session（P-048/P-053/P-054/P-055，首步明示【补建】）。
10. **v1.18 DR-19 + DR-21 合并小批（Layer-1，**首次改 `tools/spec_runner/spec_runner.py`**）**：前置 Ⅰ 锚点变量隔离实测（探针 session 置仓外，零触碰仓库）⇒ 候选①证伪 / 候选②确认 / 新发现「前缀白名单只存在于 `ANCHOR_RE`」；交付 `SessionParseError` 坏行定位 + `verify-anchor --detail`（默认关闭）+ 契约落 `independent-verify DESIGN`；selftest **43/43**。
11. **v1.19 §7.22 锚点形态裁定（**零代码**）**：存量 **74 文件 / 502 锚点**（行号区间 0 / 根级 0）⇒ Q-A **不扩展行号区间** / Q-B **认单向包含、不做集合合一**（唯一偏离 d 类转「候选扩权 + 触发条件」）。
12. **v1.20 §7.23 触发条件可核化（Layer-1）**：新增只读子命令 `anchor-audit`；真机 **76 session / 520 锚点**，`J2` 与 `J1` 的差集为 **0** ⇒ 触发未满足；selftest **47/47**。
13. **v1.21~v1.25 P2b 计划与派生态裁决（**零代码**；v1.22 除外）**：v1.21 §7.24 P2b 完整迁移计划（A-61 状态列唯一消费者 = `console_gen` 单文件 + A-62 `PROGRESS` 全仓无脚本写者）；v1.22 §7.25 **P2b 实施批件①+件③**（`_eff_status` + `derive_state(..., derived=False)` 开关 + (b) 三处直取改同源；**开关关与源逐字节一致 / 开关开差分 103 行**；selftest 41/41 → 47/47；件② 按 R-2 推迟）；v1.23 §7.26 依赖与优先级 + **决策矩阵首个活实例**（收敛出口 = 选 A）；v1.24 §7.27 派生态启用裁决（收敛建议 = **维持开关关 B′**）；v1.25 **采纳 B′**、U-7 关闭。

## 决策依据

### ① 「简陋」被定性为**结构性**而非审美（C-1）
根因是**维度缺失**（feature 级 step 投影 / 脉络链 / 架构与代码流程 / 量化进度），**改渲染无解、须补维度**；三组恒空因 `PROGRESS` 活动态为 0 行（A-2）——板子零独立判定，纯直译状态列。源 = PROGRESS P-042 行 + [RESEARCH](../../spec/project-console/RESEARCH.md) §3/§4。

### ② 剥离为**通用底座** feature 并接续取代 P-041（C-2）
可视化看板能力归属**底座（Layer-1 工具层）**，不再寄生于 academic-writing-workflow（其 C-6/C-7 降格为**来源指针**）；board-generator 记**前身 L0 首落点**，`board_gen.py` / `BOARD.md` 退役由 P-043 承接。源 = 同上。

### ③ Layer-1 只读派生视图 + markdown-native 承载（C-3 / C-4）
不接验证端门禁、本批止于 ADR-0010 懒加载 gate；承载 = markdown 内嵌 Mermaid（C-7 排除 mmdc 自建渲染：Node 18.19+ 与 Puppeteer/Chromium 依赖违零依赖定位），**零服务器零新依赖**。

### ④ P2 拆分与「登记时点前移」（C-22 / C-23）
`derive_state` 的 `sess is None` 分支把「未开工」与「确无 session」混同 ⇒ **P2 拆 P2a**（依据/行动档区分，不动状态来源与 I-7）/ **P2b**（状态来源迁移 + 载体迁移 + I-7 扩写 + 回退点）；V2 实测（P→session 59.6%）支撑**立项即登记**。

### ⑤ 派生态维持关闭（B′ 采纳）
「开关常开」属 Type-2（单点回退 R-1）⇒ 不启动矩阵但做五维评估；关键读数 = 收益面实测为零（差分 103 行**全来自那 19 条假缺口**）+ 观察窗无有效样本 ⇒ **用户裁决采纳 B′（维持开关关）**，`derived` 仍默认 `False`。

## 遇到的问题

- **DR-18（本批自捕）**：`repo_stats` PT-11 把 banner/树里写的 P 区间误捕为 `fs.progress_tasks` 读数（**19 ≠ 真值 57**）⇒ 首跑 2 条 P2；处置 = 改写为「P-001 至 P-019」，零工具改动。
- **DR-19**：session 写入非法 JSON 转义 ⇒ `step-gate` / `verify-anchor` / `step-enforce` **三命令同报** `Invalid escape` 且**不报文件名与行号**；门禁已覆盖该故障类 ⇒ 属**报错可读性**缺口（非覆盖缺口）。
- **DR-20**：把「从工具行为反推机制」的推断当 E1 用（结论对 ≠ 论据充分）；同批另订正一处**我方误读**。
- **DR-21**：`verify-anchor` 锚点路径约束未成文 + 报错**不定位锚点**（本轮为此多花 3 次往返）。
- **A-35**：本仓脚本 import 图实测为空 ⇒ C-8 前提被部分证伪，C-12 改「显式关系」口径（系**部分修正**）。
- **A-33 双源漂移**：同一事实在 `CODE_WIKI §9` 索引行正确、在映射实现里错误 ⇒ 一致性对账**抓不住**（两实现同错），收敛选**共享纯函数模块** `scripts/spec_map.py`（P-047 落地）。

## 下一步

- **P2b 件②（载体迁移）转触发驱动**（触发条件 = 状态列出现 `console_gen` 之外的第二个消费者）；**U-6**（存量豁免面处置口径）仍开，只在「拟启用派生态」时到期。
- **候选扩权（d 类根级载体）** 仍触发驱动（触发 = `anchor-audit` 报出 `J2` 与 `J1` 的差集非空 或 用户裁决）。
- **§7.11 观察项**（无决策事件的文档订正轮 ⇒ 控制台不可见）带触发条件（同类复现 ≥2 次 / 由该缺口导致的误判 / 用户裁决），当前不动。
- **ADR-0006 条件③** 裁定时点 **2026-11-15**（到期议题清单已登记，见 DEV-LOG-008）。