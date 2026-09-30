# DEV-LOG-024: 门面快照刷新 + R-1 复核 + P3 微残留处置（优先表 P2/P3 合并轻批）

> **日期**: 2026-09-29（回补）
> **会话**: `tools/spec_runner/sessions/specwf-p057-20260929.jsonl`（五步链）
> **涉及**: `CODE_WIKI.md`（§10 `facade_baseline` + §2.1 树 + §9；v1.81 → v1.82）/ `README.md` / `README.en.md` / `docs/assets/readme/evidence.svg` / `spec/arc-probe/RESEARCH.md`（v1.4 → v1.5）/ `docs/PROGRESS.md`（P-057 行 + 优先表三行）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [CODE_WIKI](../../CODE_WIKI.md) / [evidence.svg](../assets/readme/evidence.svg) / [arc-probe RESEARCH §5.3](../../spec/arc-probe/RESEARCH.md) / [ADR-0006 §B3](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) / [PROGRESS P-057](../PROGRESS.md) / `tools/spec_runner/sessions/specwf-p057-20260929.jsonl`

## 做了什么（时序）

1. **触发**：用户指令「继续按照优先级处理其他未闭环事项」（承接 [PROGRESS 优先表](../PROGRESS.md) 的 P2 门面快照 / P2 R-1 / P3 微残留三行）。
2. **Step 1 机械取证**：`repo_stats.py` 实跑得 **P3 提示 8 条**，逐条均为 `facade_baseline` 快照滞后（[CODE_WIKI §10](../../CODE_WIKI.md) 三载体的 `hits.samples 26` / `hits.form2_total 67` / `fs.adr_files 6` ≠ 真值）；判据语义 = **prose 对 baseline（P3）+ baseline 对真值（P3）** ⇒ 清零须**双侧同步**。真值取 M7 §5 hits 块（`samples 38` / `form2_total 97`）+ `adr/` 实为 **8 份**（ADR-0004 至 0011）。
3. **门面快照刷新（`repo_stats` 8 条 P3 归零）**：三载体 `as_of` 2026-08-23 → **2026-09-29** + 真值同步（`hits.samples 26 → 38` / `hits.form2_total 67 → 97` / `fs.adr_files 6 → 8`）+ 三处门面 prose 同步 —— `README.md` / `README.en.md`（样本上界与 97 处、`ADR-0004~0011` ×8、八份 ADR）+ [evidence.svg](../assets/readme/evidence.svg)（38 / 97 + 时点）。`fs.adr_files` 属**内容真滞后**（README 树停 `ADR-0004~0009` 六份，实为八份 ADR），非纯快照。同族顺手订正 CODE_WIKI §2.1 树与 §9 的 M7 计数（原被 PT-1 / PT-2 的**文件级 suppress** 遮蔽而零机械看护）。
4. **R-1 复核（不需批）**：依 P-056 元观察「同类复核以窗口到期为准、**不重复提前复算**」，本批**不重跑** `downstream_compliance.py`；以 [ADR-0006 §B3](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md)（同日 2026-09-29 实测：R-1 存续未扩大 / R-2 维持消解 / 消费仓判定表未落盘）为**证据指针**；真闭合动作在消费仓（**其仓库自治，本仓不代改**）。
5. **P3 微残留处置**：[arc-probe RESEARCH §5.3](../../spec/arc-probe/RESEARCH.md) 两项**陈旧未勾**订正（CER §3.4.1 状态同步 = **P-034 已完成** / 预链接脚本 = **P-035 已完成**；H-2 图质量评估如实保留为待办）+「批量 **32** ADR」**事实订正为 8 ADR**（**四处**：§0 假设区行 / §5.3 / H2 假设行 / §7 局限；「32」系与 `spec/` feature 目录数混淆之误）⇒ RESEARCH **v1.4 → v1.5**（**零断言计数变更** 22A+6B+6C+2H）；`m7_stats` 形态 P3（`cells_nonstandard=1`）经复核 = **样本③ 历史形态、by-design 非缺陷**（工具注解明文「历史非整齐形态如实容纳，**禁止回改**」）⇒ **本批不改**、登记为**永久 P3**。
6. **新登记覆盖边界**：`repo_stats` §10「已知未覆盖」补 **PT-2 / PT-2E 带圈数字区间上界 = 35**（< 当前 `samples` 38）⇒ 门面 `samples` 上界表达**溢出模式覆盖**、该 prose 位点不再被自动对账（扩区间属 **Layer-1 工具变更须另立批次**）。
7. **校验**：决策流 `specwf-p057-20260929` 五步链 `step-gate` **exit 0** + `verify-anchor` **锚点全真实 exit 0** + `step-enforce --pid P-031`（arc-probe 为受门禁 feature）**exit 0** + 三校验器全绿（`repo_stats` **P3 提示 8 → 0**）；**零新增 M7 样本**；CODE_WIKI **v1.81 → v1.82**。

## 决策依据

### ① 门面刷新口径（双侧同步、不追实时）

门面是「**时点快照 + 真值指针**」（P-017 后定型，**不追实时同步**）⇒ 刷新 = 把 `as_of` 推到 2026-09-29 并**三载体五处数字一次写齐**；因判据同时比 prose 与 baseline，**清零须双侧同改**。

### ② 为什么不扩带圈区间（samples 上界溢出）

`samples = 38` 而 PT-2 / PT-2E 的带圈区间上界 = 35 ⇒ 门面写带圈区间后**不再被自动对账**；**裁定 = 不扩区间**（扩正则 + 扩转换函数 = **Layer-1 工具变更**，违本批「轻批」范围，且撞已固化的 Layer-1 否决方向）⇒ **如实登记到 §10 已知未覆盖**（同类先例 = SVG 复发规律数 / README.en 词形数字）。

### ③ R-1 为什么以证据指针核讫、不重跑

同批隔 0 天复算**信息增量 ≈ 0**（P-056 元观察）⇒ 不重跑，改以 ADR-0006 §B3 同日实测为**证据指针**；真闭合动作在消费仓。

### ④ `m7_stats` 形态 P3 为什么「该不改」

回改历史发现形态违**工具明文纪律**（「禁止回改」）⇒ 复核定性为 **by-design**，登记为**永久 P3，非待办**。

## 遇到的问题

- **门面快照无触发器**：本批是 P-017 定性后的**首次真值前进触发**（前次 `as_of` 停 2026-08-23，其间样本 26 → 38、form2 67 → 97、ADR 6 → 8 均未回写）⇒ 佐证「门面快照只在人工择机时刷新」为**设计内行为**（P3 非阻断语义），非遗漏。
- **活靶拦截 1 处**：改 arc-probe front-matter 后 `repo_stats` 立即报 P2「§9 版本 v1.4 ≠ front-matter 1.5」⇒ **连带订正 §9 与 §2.1 树两行**（drift-gate 活靶，验证「制品状态变更必须同步视图层」纪律）。
- **新增覆盖边界**：`samples` 越过带圈区间上界 ⇒ 模式库覆盖随真值增长而**相对收窄**，已入册 §10。

## 下一步

- 本批**零代码**（无脚本 / 无 hook / 无 feature 目录变动）⇒ 适用 RULE-1 补充取证清单的**纯文档批**范围。
- samples 上界表达溢出属**已登记的已知未覆盖**（扩区间须另立 Layer-1 批次）。
- R-1 / 消费仓判定表**跨仓未闭环**，据实登记不记为通过。