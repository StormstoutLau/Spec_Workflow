# DEV-LOG-023: ADR-0006 失效条件复核吃狗粮批（重审 #3）——独立 pass 检出 J-4 两处实现缺陷 + 追加修复轮

> **日期**: 2026-09-29（回补）
> **会话**: `tools/spec_runner/sessions/specwf-p056-20260929.jsonl`（首轮纯登记型，五步链）+ `tools/spec_runner/sessions/specwf-p056-20260929v2.jsonl`（追加修复轮，首步明示【补建】）
> **涉及**: `adr/ADR-0006-assertion-framework-dual-copy-authority.md`（§B3；v1.1 → v1.2）/ `scripts/downstream_compliance.py`（J-4 三处修复）/ `spec/downstream-compliance/`（四件套 v1.0 → v1.1，IMPLEMENTATION 新增 §3.4）/ `docs/adr/README.md` / `docs/PROGRESS.md`（P-056 行）/ `CODE_WIKI.md`（v1.80 → v1.81）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [ADR-0006 §B3](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) / [downstream-compliance IMPLEMENTATION §3.4](../../spec/downstream-compliance/IMPLEMENTATION.md) / [downstream-compliance DESIGN](../../spec/downstream-compliance/DESIGN.md) / [downstream_compliance.py](../../scripts/downstream_compliance.py) / [PROGRESS P-056](../PROGRESS.md) / 两份 session 文件

## 做了什么（时序）

1. **触发**：用户指令「直接开吃狗粮批做 ADR-0006 复核」（**编号经校正为 P-056**，因 P-055 已用于 open issue 盘点批）。
2. **Step 1 机械取证（E2）**：`python scripts/downstream_compliance.py` 对 `F:\Cpp_Hub` 复算 J-1~J-4 ——
   - **J-1 分叉**：AEF 副本指针 `git ls-files` 命中**且在库**（✓）；`DIS-007` 副本指针在文但**未入库**（✗）；`git check-ignore -v` 复核根因 = `.gitignore:82` 的 `docs/discoveries/` **整目录前缀**（非单文件）。
   - **J-2**：`rev-list --left-right --count origin/main...HEAD` = **`0 0`** ⇒ **R-2 维持消解**。
   - **J-3 + `[决策5]`**：Cpp_Hub `docs/COMPLIANCE_TABLE.md` **未落盘**（structural）⇒ 决策 5 落地形态**维持未闭环**。
   - **J-4**：**有效回流 0 条 / 回流标记 1 条**（= 指针提交 `96edc5c` 自身）；**观测窗 43/90 天（47.8%）**、窗内 **40** commits（`rev-list --count --since="2026-08-17 00:00:00 +0800"` **钉死时刻**复算 —— 裸日期会随执行时刻漂移得 39/36/35）。
3. **裁决（三项均不构成改判）**：① 用户裁决方案 A **未命中**；② **形式解除**（R-1 存续未扩大 / R-2 维持消解）；③ **未满窗不判负** ⇒ **ADR-0006 维持 accepted**（决策 1-6 不动）。
4. **落档**：[ADR-0006 §B3](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md)（三项逐条对照表 + 结论与处置 6 条）+ 修订历史 + front-matter（**v1.1 → v1.2**，按 ADR-0011「v1.9 追记」先例；`date` 2026-08-16 → 2026-09-29 陈旧项订正）+ 元数据表；`docs/adr/README` + CODE_WIKI §9 同步。
5. **独立 pass（异基座，RULE-1 时序独立 + RULE-5）检出 4 项、全部处置**：**J-4 两处实现缺陷**（① 窗口起点用**裸日期** → git `approxidate` 以**当前时钟补齐时刻** ⇒ 读数随执行时刻漂移 39/36/35，钉死 `+0800` 0 点 = **40**；② `--grep` 缺 **`-E`** ⇒ 竖线为 BRE **字面量**、回流标记**恒 0 假阴性**）；**首报的「`splitlines()` 高估 1」经复算证伪撤回**；**视图层同步须与 session 声称一致**（随收束完成）；元观察补 **`[判断]`** C 类标注；`.arc` 漂移回顾**实为 4/8**（含本 ADR 自身 v1.2）。
6. **追加修复轮（v2 session）**：`reflux_since` 改**含时区完整时刻** + 命令补 `-E` + 计数改 **`git rev-list --count`**（权威整数）+ verdict 改为**信息性**（判读归人）；`spec/downstream-compliance/` 四件套 **v1.0 → v1.1**（IMPLEMENTATION 新增 **§3.4** 两缺陷机制表 + 加固 + 修后读数）。
7. **元观察（登记纪律）**：本批与 #2 相隔 3 天且读数实质一致 ⇒ 提前复算**信息增量 ≈ 0**〔`[判断]`〕⇒ 同类复核**以窗口到期为准**，不重复提前复算。
8. **校验**：决策流 `specwf-p056-20260929` 五步链 `step-gate` **exit 0** + `verify-anchor` **10 锚点全真实** + `step-enforce --pid P-056` **exit 0** + 三校验器全绿；**零新增 M7 样本**；CODE_WIKI **v1.80 → v1.81**。

## 决策依据

### ① 为什么维持 accepted 且不提前裁决条件③

条件③ 原文「回流频度 <1 次/季度 ⇒ 通道名存实亡」的**判据内置语义 = 窗口未满不得判负**；本批属**提前复算**（窗口 43/90 天）⇒ 仅记录读数 + 不判负声明，裁定时点**维持 2026-11-15**。三项失效条件均不构成改判依据。

### ② 为什么落 ADR-0006 §B3 而不建新 `spec/` 四件套

复核类批依**重审 #1 / #2 先例**，就地记入 ADR-0006 §B（仅 P-049 等**工具交付批**才建四件套）⇒ 记录型追加，不改判。

### ③ 独立 pass 首报根因为什么会被「证伪撤回」

按纪律**逐条复算而非照单全收**：复跑原命令多次皆得 **35**（确定性）且与 `rev-list --count` 一致 ⇒ 首报「`splitlines()` 空行高估 1」**不可复现 ⇒ 撤回**；真因经**切割实验**（同一冻结仓、窗内零新提交，不同时刻先后得 39 / 36 / 35；钉死 `+0800` 0 点 = 40）定位为**裸日期 + 缺 `-E`** 两处。

### ④ `[决策5]` / `[J-3]` 归属

判定表本体**归消费仓**（`docs/COMPLIANCE_TABLE.md` 未落盘）；本仓只给**格式与生成器**（`--emit-table`），**不代填、不代判**（守决策 5 归属规则）。

## 遇到的问题

- **工具读数缺陷（两处）**：J-4 的窗口起点裸日期致读数随执行时刻漂移；`--grep` 缺 `-E` 致回流标记结构性假阴性（原 `"✓" if hits` 分支**从未执行**）。**已修**（追加修复轮）。
- **审查臂假阳性**：独立 pass 首报根因**不可复现、已撤回** ⇒ 审查臂结论须**逐条复核**。
- **历史读数漂移**：钉死时刻后的「总 40」与 ADR-0006 §B2（09-26 记 39）及 §3.1 不一致 ⇒ **如实标注「历史读数系缺陷产物」，不静默改写历史**。

## 下一步

- 条件③ 裁定时点维持 **2026-11-15**（到期一次做完：J-1~J-4 复算 + 分母人工语义筛查 + 三态裁定）。
- R-1（跨仓）/ 决策 5 判定表（现场）**留证据指针**，不代改代判。