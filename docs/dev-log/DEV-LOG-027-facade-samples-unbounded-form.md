# DEV-LOG-027: 门面 samples 改无界阿拉伯区间（PT-2/PT-2E 带圈区间溢出处置）

> **日期**: 2026-10-01（回补）
> **会话**: `specwf-p060-20261001.jsonl`（`tools/spec_runner/sessions/`，五步链 research → design → implement → verify → finalize）
> **涉及**: `README.md` L43 / `README.en.md` L43 / `CODE_WIKI.md`（§10 模式库 PT-2 与 PT-2E 与 `pattern_lib_version`、§10 已知未覆盖、banner v1.106 → v1.107）/ `docs/PROGRESS.md`（P-060）；零代码（模式库属数据非代码）
> **状态**: done（**回补说明**: 本份为 2026-10-01 统一回补批产出的事后叙事，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；源中未出现的内容一律不写，无法确认处标「未核」）
> **源指针**: [PROGRESS P-060](../PROGRESS.md)、[README L43](../../README.md)、[README.en L43](../../README.en.md)、[session 事件流](../../tools/spec_runner/sessions/specwf-p060-20261001.jsonl)

## 做了什么（时序）

1. **research 步**：确认溢出根因（E1）——`repo_stats` **PT-2** 模式为「样本 + 带圈区间」、**PT-2E** 为其 EN 变体（scope `README.en.md`），二者捕获带圈区间上界并与 `hits.samples` 比对；而带圈字符类上界 **㉟ = U+325F = 35**，且 `circled_to_int` 亦只解 1-35。当前 `samples = 38`，门面却写「样本 ①-㊳」（㊳ 已超字符类）⇒ 正则**不匹配** ⇒ 该位点**静默失效**（工具报 P3 = 0 是「未匹配」而非「对得上」）。
2. **design 步**：选定处置——门面表达由**带圈区间**改**无界阿拉伯区间**；模式库 PT-2 / PT-2E 同步改**阿拉伯区间捕获**（取区间上界与 `hits.samples` 比对）；`pattern_lib_version` **2 → 3**；§10「已知未覆盖」该条改判**已解决**并另立 v3 注。
3. **implement 步**：落档——`README.md` L43「样本 ①-㊳」改「样本 1-38」；`README.en.md` L43「samples ①–㊳」改「samples 1–38」（`evidence.svg` 早已为阿拉伯数字 38，**无需改**）；`CODE_WIKI` §10 模式库与版本同步 + banner v1.107 + §2.1 树 + §9 + `declared.progress_tasks` 59 → **60**（PT-11 两处载体同形）；补 session。
4. **verify 步**：三校验器全绿（`repo_stats` 0 违规且 P3 0，**独立复算** PT-2 / PT-2E 命中 **38** = `hits.samples` 真值、`pattern_lib_version` = 3）；`console_gen` 与源一致；两 selftest 零改动一致；门禁链全 exit 0；全覆盖终验 grep（不抽样）= 门面双语旧带圈形态**零残留**。
5. **finalize 步**：P-060 回填 `done` 并写验收标准。

## 决策依据

### ① 为何改「门面表达」而非「扩带圈区间」

带圈 Unicode 三段（①-⑳ / ㉑-㉟ / ㊱-㊿）**止于 50** ⇒ 扩带圈区间属**有界补丁**、越过 50 必复发（用户已否决）；改门面表达为**无界阿拉伯区间**才根治。

### ② 为何保留「区间」语义

取「阿拉伯区间」而非裸数字：保留区间语义（`样本 1-38` / `samples 1–38`），**仅替换字符集**，改动最小。

### ③ 为何 `pattern_lib_version` 递增

模式修改须递增（I-4 纪律）；工具侧门控为 `>=2`，递增不改变 gap-report 行为，回退 = 改回模式串与版本。

### ④ 边界：改的是门面表达，非工具能力

`circled_to_int` 的 1-35 上限**不变**；`spec/repo-stats/` 四文档的 PT-2 带圈描述为 **P-014 时点设计记录**，不在本批追改（守「时点快照不追平」）。

## 遇到的问题

- **`dc_validator` 首跑 3 条 P2「相对链接不可解析」**：根因定位 = 我写正则字面量时，**字符类紧邻圆括号捕获组**恰好拼成「右方括号紧跟左圆括号」的相邻形态，被 M5 的 markdown 链接语法**误判**（M5 不做 markdown 语义解析、且不排除行内代码跨度）⇒ **pre-commit 阻断提交**。**改写措辞**后 `dc_validator` **0 违规**。该根因后续被登记为 M7 §4 候选③（见 DEV-LOG-028 / DEV-LOG-029）。

## 下一步

- 2026-10-01 盘点批认定的「唯一现在可做」项本批闭环。
- 剩余唯一真阻塞 = **U-6**；唯一硬期限 = ADR-0006 失效条件③（2026-11-15，到期前不开批）。
- 其余全部等触发。