# DEV-LOG-015: ARC 快照漂移清债 + ID 稳定性实测 + 新增 tools/arc/arc_drift_check.py

> **日期**: 2026-09-26（回补；批次日据 PROGRESS P-048 行）
> **会话**: `specwf-p048-20260927.jsonl`（五步链 research / design / implement / verify / finalize，**首步明示【补建】**——依该批 commit `def03d0` body 与 PROGRESS P-048 行回溯重建，ts 取 2026-09-27）
> **涉及**: tools/arc/README.md（快照语义登记）/ tools/arc/arc_drift_check.py（**新增**）/ tools/arc/data/.arc/decisions/（全量重建，8 副本）/ adr/ADR-0006-assertion-framework-dual-copy-authority.md（§D J-3 泛化）/ docs/PROGRESS.md（P-048 行）/ CODE_WIKI.md（v1.59 → v1.60）
> **状态**: done（**回补说明**: 本份为 2026-10-01 **统一回补批**产出的**事后叙事**，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；**源中未出现的内容一律不写**，无法确认处标「未核」）
> **源指针**: [PROGRESS P-048](../PROGRESS.md) / [ADR-0006](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) / [tools/arc/README](../../tools/arc/README.md) / [arc-rollout RESEARCH](../../spec/arc-rollout/RESEARCH.md) / [arc-rollout DESIGN](../../spec/arc-rollout/DESIGN.md) / [arc-rollout IMPLEMENTATION](../../spec/arc-rollout/IMPLEMENTATION.md) / 会话 `tools/spec_runner/sessions/specwf-p048-20260927.jsonl`

## 做了什么（时序）

> **承接**：ADR-0006 v1.1 草案 §F **R-3** 开放项；用户指令「先做 ID 稳定性实测」→「按这个方案来」。

1. **漂移面实测（E1 / E2）**：`tools/arc/data/.arc/decisions/` 8 副本中 **2 份已漂**——`D-003` 停 v1.0 vs 真值 **1.1**、`D-008` 停 v1.7 vs 真值 **1.8**；导入 **2026-09-09** → 观测 **2026-09-26**，**17 天即 25% 漂移**。
2. **ID 稳定性实测（沙箱镜像，零触碰真库）**：① **目录一次导入确定性可复现**（空库 `arc init` + `arc import adr/` → 复现 `D-001` 至 `D-008`、文件名逐字一致）；② **增量重导入只追加不更新**（重复目录导入 `skipped 0`，每次各新增 8 副本；同身份单文件导入另得新号）⇒「**再 `import` 一次追平**」是**陷阱**（产出 `D-009` 至 `D-016` 副本、使漂移**加倍**）；③ `arc link` **幂等**（同边二跑回 `already has depends_on`）；④ 重建唯一代价 = 丢手工 `depends_on` 边与 `date`（前者由 prelink 幂等补回）。
3. **全量重建清债（已执行）**：备份 → 清 `.arc/decisions` → `arc init` → `arc import adr/` → `arc_prelink.py --execute` → 复核 **8/8 版本追平 + ID 逐字不变 + 7 条边完整**（git 足迹 8 文件：`D-003` 内容刷新 75 行，余为 `date` 与边）。
4. **快照语义登记 + J-3 泛化 + 新增核查脚本**：`.arc` = ARC 数据层**导入时点快照（不追平）**，记于 `tools/arc/README.md`（含「**不得增量 import 追平**」铁律）；`ADR-0006 §D` 的 J-3 由「跨仓下游副本」**泛化**为「**任意副本**：跨仓下游 + 本仓派生物」；新增可复算命令 `tools/arc/arc_drift_check.py`（`git` + 文本级版本行对账，**零 ARC 二进制依赖**、**不接三校验器**——守 P-035 **D6**；双向验证 = 清洁态 exit 0 / 备份漂移态 exit 1 命中 2/8）。
5. **措辞订正**：R-3 中 `version` 归属（属**被嵌入原文自带 front-matter**，非 ARC 独立字段）。
6. **收束**：守 P-035 `.arc` 豁免语义（登记不改）；决策 1 至 4 维持 accepted、**决策 5 / 6 仍 proposed**；**零新增 M7 样本**；CODE_WIKI v1.59 → **v1.60**（declared progress_tasks 47 → 48 + §2.1 tools 树补登 + §9 / §10 两行）。

## 决策依据

### ① 为什么全量重建而非增量追平（清债路径）
ID 稳定性实测证明**增量 `import` 只追加、永不更新**（重复导入每次各新增 8 副本）⇒ 增量追平不仅无效，还会**产出副本使漂移加倍**；追平唯一可行路径 = **全量重建**（已实测可复现、`D-001` 至 `D-008` **ID 逐字保留**，代价 = `date` 刷新 + 手工边由 `arc_prelink.py` 幂等补回）。

### ② 为什么把 J-3 泛化并新增核查脚本
`ADR-0006 §D` 的 J-3 由「跨仓下游副本」扩为「**任意副本**」（跨仓下游 + 本仓派生物），`.arc` 快照即本仓派生物实例；据此新增 `arc_drift_check.py` 使漂移**可复算检出**。

### ③ 为什么核查脚本不接门禁
守 **P-035 D6**（ARC 薄壳工具链不接 pre-commit / 校验器，验证端仍由三校验器把守）⇒ 定位为「**可复算检出**」而非「提交即阻断」。

## 遇到的问题

- **漂移速度**：17 天即 **25%**（2/8）⇒ 佐证「导入时点快照不追平」必须**显式登记**（README）+ 提供可复算检出，而非依赖人工记忆。
- **「再 import 一次追平」陷阱**：实测会产出 `D-009` 至 `D-016` 副本、使漂移**加倍**；处置 = 写入 `tools/arc/README.md` 铁律。
- **本 session 为补建**：非当时实时记录（首步明示【补建】）；批次日据 PROGRESS P-048 行为 **2026-09-26**，补建 session 文件名 `specwf-p048-20260927.jsonl` 与 `ts` 为 **2026-09-27**。

## 下一步

- **决策 5 / 6 仍 proposed**：判定权拆分与 J-1 至 J-4 的机械化落地留待后续批（P-049 承接）。
- 快照漂移由 `tools/arc/arc_drift_check.py` 可见化，**不接门禁**（守 D6）。