# DEV-LOG-010: 项目控制台实施（project-console）—— 多视图控制台生成器落地 + 归属迁移（前身 board-generator 退役）

> **日期**: 2026-09-11（回补）
> **会话**: `specwf-p043-20260911.jsonl`（五步决策链：research / design / implement / verify / finalize）
> **涉及**: spec/project-console/（DESIGN v1.0 + IMPLEMENTATION v1.0 + CHECKLIST v1.0 accepting）/ scripts/console_gen.py（新建，承接 scripts/board_gen.py）/ docs/CONSOLE.md（承接 docs/BOARD.md）/ .pre-commit-config.yaml（第五 hook 更名）/ spec/board-generator/DESIGN.md（前身）/ docs/PROGRESS.md / CODE_WIKI.md
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [DESIGN](../../spec/project-console/DESIGN.md) / [IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) / [CHECKLIST](../../spec/project-console/CHECKLIST.md) / [RESEARCH](../../spec/project-console/RESEARCH.md) / [PROGRESS](../PROGRESS.md) / [CODE_WIKI](../../CODE_WIKI.md) / [CONSOLE](../../docs/CONSOLE.md) / [前身 DESIGN](../../spec/board-generator/DESIGN.md) / [session](../../tools/spec_runner/sessions/specwf-p043-20260911.jsonl)

## 做了什么（时序）

1. **立案（research 步）**：承接 P-042 RESEARCH v1.1 的 C-5~C-8 四项裁定，实施范围冻结为**单脚本**（`console_gen.py`）+ **单产物**（`docs/CONSOLE.md`）+ **单 hook**（`console-gen`）+ 前身双文件退役。
2. **设计（design 步，DESIGN v1.0）**：D1 落点（唯一脚本 + 唯一产物 + L0 门禁触发）/ D2 八章输出契约 / D3 派生状态机（状态取 `PROGRESS` 原词，附派生依据与行动档，退出条件复用 `step-gate` 三类规则）/ D4 承载限定 markdown 内嵌 Mermaid / D5 依赖图 `ast` + `importlib` 字面量补提取 + 极简 YAML 文本自解析 / D6-D7 错误处理与不变式；**新增不变式 I-7 词表对齐**（禁重贴标签）；三替代方案（只改文案 / mmdc + 自包含 HTML）否决。
3. **实施（implement 步）**：① `scripts/console_gen.py`（stdlib only）：`parse_progress` / `feature_pid_map` / `read_sessions`（最远 step + 软性 + 末 ts + 步序列）/ `artifact_map`（**制品链四文档投影**，后缀匹配兼容遗留前缀命名）/ `derive_state` / `dep_graph` / `hook_chain`（**不引入 PyYAML**）/ `render` 八章；② **前身退役**（`board_gen.py` 移除前**字节级备份一致**（16241 B = 16241 B）+ `git add` 入对象库后 `git rm`；`docs/BOARD.md` 直接退役——**纯派生无需备份 I-5**）；③ `.pre-commit-config.yaml` 第五 hook `board-gen` → **`console-gen`**（**hook 计数仍为 5，`files` / `pass_filenames` 语义零改动**）。
4. **多视图交付（D1-D7 + I-1~I-7）**：三级行动队列 Needs Attention → Ready to Verify → Recommended + feature 分组键表 + P 卡片键表（活动区上限 7 + done 折叠）+ 决策链 `stateDiagram-v2` + 架构 `flowchart LR` + 追溯指针 + fork。**裁定落地** = C-5 词表对齐（「⚠ 待你审」废止，新增 I-7）/ C-6 双主键 + 活动区上限 / C-7 承载限定 markdown 内嵌 Mermaid（**无 mmdc、无 HTML 产物**）/ C-8 零依赖依赖图。
5. **验收（verify 步）**：selftest **16/16 PASS**（S1-S16）+ 三校验器全绿（dc_validator **114 文件** / m7_stats / repo_stats 0 违规）+ `step-enforce --pid P-043` 五步链 exit 0 + `verify-anchor` 锚点全真实 + **真实仓首次生成 `docs/CONSOLE.md`**（非 temp）。
6. **收束（finalize 步）**：PROGRESS P-043 行 + P-041/P-042 行前身与接续关系收口 + CODE_WIKI **v1.44**（版本头 / §2.1 脚本树与 docs 树 / §9 索引两行 / 覆盖对象脚本清单）；**零新增 M7 样本**。

## 决策依据

### ① 前身「接续取代」而非并存（归属迁移）
P-042 C-2 已裁定可视化层归**通用底座**、独立 feature `spec/project-console/`，**接续取代 P-041**（board-generator 记**前身 L0 首落点**）。故 `board_gen.py` / `docs/BOARD.md` 退役、能力迁入 `console_gen.py` / `docs/CONSOLE.md`，hook **更名不增数**。源 = PROGRESS P-043 行 + [前身 DESIGN](../../spec/board-generator/DESIGN.md)。

### ② 承载限定 markdown 内嵌 Mermaid（C-7）
依赖宿主渲染器渲染，**不引入** mmdc（Node + Chromium 依赖）与自包含静态 HTML ⇒ 守零新依赖定位。源 = [DESIGN](../../spec/project-console/DESIGN.md) §1 / [IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) §2。

### ③ §6 追溯段只放指针、不复制数字（I-6）
派生视图**不增真值**，避免与 `m7_stats` 的账本看护权冲突。源 = PROGRESS P-043 行。

### ④ 单脚本 + 单产物 + 单 hook（最小机制面）
以「最小机制面覆盖四维缺失」（C-1 结构性诊断的落点）；`derive_state` 新增 I-7 词表对齐后，「派生新标签」被设计面禁止。源 = [DESIGN](../../spec/project-console/DESIGN.md) §1。

## 遇到的问题

- **DR-1（首轮拦截，S4）**：`_feature_table` 误用**模块级 `SPEC` 常量**，致临时 root 下制品链全显 `—`；由 `build()` 传参修正——fixture 化的直接收益。源 = [session](../../tools/spec_runner/sessions/specwf-p043-20260911.jsonl) 第 3 条 + [IMPLEMENTATION](../../spec/project-console/IMPLEMENTATION.md) §6。

## 下一步

- **视图增补**（C-9 描述列 / C-10 per-feature 折叠 / C-12 架构图「显式关系」口径）留待实施批——由 P-044 号批落码（见 DEV-LOG-011）。
- **C-11（映射收敛）不在本批**——显式缺口保留 `—`，待后续批处置。源 = [CHECKLIST](../../spec/project-console/CHECKLIST.md) §9。