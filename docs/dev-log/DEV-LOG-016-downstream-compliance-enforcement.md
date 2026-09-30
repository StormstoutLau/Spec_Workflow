# DEV-LOG-016: 下游符合性（ADR-0006 决策 5 / 6 落地 + 新增 scripts/downstream_compliance.py 的 J-1 至 J-4）

> **日期**: 2026-09-26（回补）
> **会话**: `specwf-p049-20260926.jsonl`（五步链：research / design / implement / verify / finalize）
> **涉及**: spec/downstream-compliance/（RESEARCH v1.0 8A+3B+4C+2H / DESIGN v1.0 / IMPLEMENTATION v1.0 / CHECKLIST v1.0 accepting）/ scripts/downstream_compliance.py（**新增**）/ scripts/dc_validator.py（连带缺陷修复）/ adr/ADR-0006-assertion-framework-dual-copy-authority.md（v1.1 定稿）/ docs/adr/README.md / docs/PROGRESS.md（P-049 行）/ docs/CONSOLE.md（重生成）/ CODE_WIKI.md（v1.60 → v1.61）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-049](../PROGRESS.md) / [ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) / [downstream-compliance RESEARCH](../../spec/downstream-compliance/RESEARCH.md) / [downstream-compliance DESIGN](../../spec/downstream-compliance/DESIGN.md) / [downstream-compliance IMPLEMENTATION](../../spec/downstream-compliance/IMPLEMENTATION.md) / [downstream-compliance CHECKLIST](../../spec/downstream-compliance/CHECKLIST.md) / 会话 `tools/spec_runner/sessions/specwf-p049-20260926.jsonl`

## 做了什么（时序）

1. **research 步（调研对象 = 消费仓实况，非文献）**：用户指令「ADR-0006决策accepted 然后开始实现」（承接 §C / §D 决策 5 / 6 由 proposed 转 accepted）。对 `F:\Cpp_Hub` **直接实跑** J-1 至 J-4（E2）——**J-1** AEF 副本指针**存在且已入库**、`DIS-007` 副本指针**存在但未入库**（同批指针入库状态**分叉**，单看 grep 会把两者判为同态——重审 #1 即此错误）；**J-1 根因精化** = `git check-ignore -v` 显示被忽略者是 `.gitignore:82` 的 **`docs/discoveries/` 整目录前缀**、**非「单文件」**；**J-2** `rev-list --left-right --count origin/main...HEAD` = **`0 0`** ⇒ **R-2 消解**（「ahead 11 未推送」记载失效）；**J-3 首测** = 副本冻结 **1.1** vs 权威源 **1.4.2**（AEF）/ **1.3**（DIS-007）；**J-4** 40 天窗、回流 **0** 次（唯一 grep 命中为指针提交 `96edc5c` 自身）。**核心发现 = 手记残余状态 3 天内自身漂移**（一处消解 + 一处根因失真）——「人工纪律」载体不可靠性的**二次实证**。
2. **design 步**：DESIGN v1.0 落档——**D1** 单脚本 + `CONSUMERS` 常量登记 / **D2** 判定表本体归消费仓（不代填不代判）/ **D3** 三态 exit（blocking 优先）/ **D4** 判据单点判定（I-1）/ **D5** 不接门禁；ADR-0010 三问 = **Layer-1 / 已激活 / 零副作用**；替代方案 **A 选择 + B / C / D 否决**。
3. **implement 步**：新增 `scripts/downstream_compliance.py`（J-1 至 J-4 可复算检查器 + `--emit-table` 判定表三列骨架；**只读消费仓、只写 stdout**；三态 exit 0/1/2，blocking 优先）；首轮实跑 **exit 1**（唯一阻塞 = J-1 未入库）、`--emit-table` exit 0；实施期发现 **DR-1**（exit 判定序会掩盖 blocking → 改 blocking 优先）/ **DR-2**（无判定表时报「差异未记录」属**双重归因** → 改 `— 无判定表（待消费仓落盘）`）/ **DR-3**（J-3 首测差异量此前无任何记录）。
4. **连带缺陷修复（ADR-0006 §D J-3 泛化的必然要求）**：`dc_validator` 的 `.arc` 排除**只在 `os.walk` 生效**、显式传参（pre-commit staged 列表）绕过 ⇒ 抽 `EXCLUDE_DIRS` + `is_excluded()` 使两路径**共用同一判定**（I-10 语义同源）+ selftest 十三 → **十四 fixture**：**缺陷场景 18 违规 → 0 文件 0 违规**、`pre-commit run --all-files` dc-validator **Failed → Passed**、selftest **16/16 PASS**、全量回归 **115 文件 0 违规**。
5. **ADR-0006 v1.1 定稿**：决策 5 / 6 **proposed → accepted**（`§C` / `§D` 标题 + `§F` 首项关闭 + 新增 **§B2 失效条件重审 #2** 记录本批实测 + 修订历史两行）+ `docs/adr/README.md` 同步。
6. **finalize / verify**：验收 = **有条件通过**（统计口径按 RULE-2 逐项核对：39 项 / 33 通过 / 0 失败 / 6 待办，全为未实测或跨仓依赖）；ADD 审计 **4.7/5 档位 A**，两项发现（P2 exit 2 未实证 / P3 路径硬编码）登记后续行动；PROGRESS P-049 行 + CODE_WIKI v1.60 → **v1.61**（declared：spec_feature_dirs 32 → 33 / scripts 8 → 9 / progress_tasks 48 → 49）+ `docs/CONSOLE.md` 重生成 + 三校验器 + `step-gate` + `verify-anchor` + pre-commit 五 hook；**零新增 M7 样本**。

## 决策依据

### ① 为什么判定表本体归消费仓（决策 5 边界）
**集中代持 = 把「委托」变成「替代」**——正是 `ADR-0006 §E` 明确不采纳方案的变体；本仓只给**格式与生成器**，判定表本体归消费仓（不代填不代判）。DESIGN §6.3 方案 C 据此否决。方案 A（登记常量 + 单脚本）的选择理由 = 当前消费仓**仅 1 个**（Cpp_Hub），配置外置收益为零而引入新文件面；跨机风险由「不可达 → exit 2 显式提示」兜住（I-3）。

### ② 为什么不接 pre-commit 门禁
**直接违 `ADR-0006 §D`**（J-1 至 J-4 定位为「**纪律 + 可复算命令**」，非门禁）；且判据依赖**另一仓**（Cpp_Hub）的可达性，把外部环境不确定性引入本仓门禁 = 制造**脆弱门禁**。DESIGN §6.2 方案 B 据此否决。

### ③ 为什么 J-1 两事实同函数一次判定（I-1）
防退化为**单一 grep**：同批指针「存在但未入库」若只看 grep 会把两者判为同态（重审 #1 即此错误），故 J-1 须在同一循环体内合成「指针存在」与「已入库」两事实判定。

J-1 未入库的根因经 `git check-ignore -v` 精化为 `.gitignore:82` 的**整目录前缀**（非单文件）⇒ 判据须核「**入库状态**」而非仅「文件被忽略」。

## 遇到的问题

- **手记残余状态自身漂移**：J-2 记载失效（R-2 消解）+ J-1 根因失真，**3 天内自身漂移** ⇒ 「人工纪律」载体不可靠性二次实证。
- **exit 2 两分支本机无法触发**：消费仓不可达 / 版本行解析不全 —— 登记为**未实测项**而非记为通过（按 ADD Iron Law 与 RULE-6 取证矩阵要求）。
- **连带缺陷**：`dc_validator` 的 `.arc` 排除在两路径语义分叉（P-035 声明 vs 实现），经 `EXCLUDE_DIRS` / `is_excluded()` 单点化修复。

## 下一步

- **独立 pass 待触发**（RULE-1 时序独立；本批为同基座生成端自审，RULE-5 异质性未达成）。
- 后续行动两项：**P2 exit 2 未实证** / **P3 路径硬编码**。