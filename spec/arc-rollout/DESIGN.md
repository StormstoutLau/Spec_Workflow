---
id: arc-rollout-DESIGN
type: design
version: 1.0
status: draft
date: 2026-09-09
depends: [arc-probe-RESEARCH, FWK-DECISION-RECORD, ADR-0007]
upstream: null
---

# 设计文档：ARC 决策图谱升级实施（吃狗粮模式，P-035）

> **Feature**: ARC（kegesch/arc 0.8.0）决策图谱升级——规避矩阵落地实施
> **创建日期**: 2026-09-09
> **状态**: draft（草稿）
> **Spec 步骤**: Step 3-4（设计 + Review）
> **任务来源**: 用户指令「按照吃狗粮模型执行ARC 升级 规避缺陷」——P-034 C-6 保留裁决触发实施

---

## 1. 背景与设计输入

### 1.1 调研输入（P-031~P-034 四批调研已闭环）

- [arc-probe RESEARCH v1.4](RESEARCH.md)（本仓）——实态试跑（Windows 命令面可用）+ 平台缺陷双实证 + H2 部分证伪 + 缺陷规避矩阵（§3.8）
- [CER §3.4.1 ARC 行](../community-ecosystem/COMMUNITY_ECOSYSTEM_RESEARCH.md) v1.16——ARC 保持主选，选型对比 4.2 分显著最优，规避矩阵收敛缺陷面至可接受
- [FWK-DECISION-RECORD v1.1](../../docs/DECISION_RECORD_CONTRACT.md)——决策记录八字段 schema（预链接映射契约）

### 1.2 规避矩阵（RESEARCH §3.8，实施批设计输入）

| 缺陷 | 规避方案（设计输入） |
|------|---------------------|
| `arc skill` 崩溃（Windows） | 命令白名单排除 skill/init-agent |
| `arc --version` = 0.1.0 ≠ 包版本 | 不信 CLI 版本；版本事实源 = 下载产物 sha256 + tag |
| linux bun 依赖（#30） | 基准平台 = Windows（官方 win32-x64.exe） |
| import 关系空 + date=导入日 | 预链接脚本按 FWK-DECISION-RECORD 映射补 |
| link 方向语义 | 预链接脚本统一出边方向 + 方向映射表 |
| 0.x breaking change | 版本快照固化 0.8.0 + sha256 登记 + 90 天观察项 |

---

## 2. 设计决策（D1-D7）

### D1：落地形态 = 薄壳封装器（wrapper）非集成

ARC 是**外部 CLI 工具（非依赖）**——不引入 pip/npm 包，不修改任何校验器。落地为 `tools/arc/` 目录下的薄壳封装：

- **文件布局**：`tools/arc/arc_wrap.py`（白名单封装器）+ `tools/arc/arc_prelink.py`（预链接脚本）+ `tools/arc/arc.exe`（二进制，gitignore）+ `tools/arc/README.md`
- **原理**：封装器 = 命令白名单门 + JSON 输出透传。所有 ARC 调用经 `python tools/arc/arc_wrap.py <cmd> ...`，未授权命令 exit 2。

### D2：命令白名单（规避 skill 崩溃 + init-agent 缺陷面）

白名单 = 实测可用主命令链（RESEARCH A-8 实测）：`init / add / list / show / trace / impact / check / next / context / import / link / validate / status / graph`

排除：`skill / init-agent / edit / remove / rename / promote / invalidate / unobsoleted / query / diff / related / unlink`（skill/init-agent = 崩溃面；其余 = 未实测或写操作面窄）

**补充设计（v1.4 增量）**：`context/diff` 等新命令面若实测可用则纳入白名单（见 IMPLEMENTATION 实测清单）。

### D3：二进制获取与版本固化

- 下载官方 release `arc-win32-x64.exe`（v0.8.0，94.4MB）→ `tools/arc/arc.exe`
- **sha256 登记**：`tools/arc/arc.sha256`（git 提交），二进制本体 gitignore
- 版本事实源 = sha256 表 + tag，不信 `arc --version`

### D4：预链接脚本（规避 import 关系空 + link 方向语义）

`arc_prelink.py`：
- 输入：本仓 ADR 文件列表（`adr/*.md`）
- 解析 ADR frontmatter 的 `depends` 字段 + 正文「取代」引用 → 生成 ARC 实体间链接
- 方向映射表（实测校准）：ADR | depends → ARC `drives`（requirement ─drives─▶ decision）
- 输出：`arc link` 命令序列 + 执行日志

### D5：试点范围 = ADR 簇（限定）

- 导入范围：`adr/` 下全部 ADR（8 个）
- 实体类型：import 为 decision（D-xxx）
- 关系：depends 依赖簇 × 取代链 → `drives` 边
- 目标：trace/impact/check 递归可用，孤儿率 ≤ 20%

### D6：不接入门禁（与 step-gate 正交）

- ARC CI-enforcement（#14）未发布——ARC 不进 pre-commit/step-enforce
- ARC 图 = **生成端辅助查询工具**，验证端仍由三校验器把守
- 零 hook / 零校验器改动，仅新增 `tools/arc/` 目录

### D7：停滞观察项

- 90 天无新 release → 评估启用 P-033 C-5 退路（adr-explorer 看板 + ARC 受限使用 / 自研薄查询壳）
- 登记于 README + PROGRESS

---

## 3. 关键约束

- **零依赖不变式**：封装器与预链接脚本 = stdlib only（Python），ARC 二进制为外部工具非依赖
- **I-2 临时目录**：二进制下载/试跑不落仓（gitignore）；导入最终产物 = `tools/arc/data/`（git 提交）
- **吃狗粮纪律**：本批自身走 step-gate 五步链 + verify-anchor 锚点核查
- **授权范围**：ARC 图仅登记决策关系，不接管三校验器

---

## 4. 验收标准

1. `arc_wrap.py` 白名单生效：白名单命令 exit 0，非白名单（skill）exit 2
2. `arc.exe` sha256 = 登记值（8f4b3089...）
3. `arc_prelink.py` 对 8 个 ADR 导入成功 + 预链接 ≥ 5 条边
4. `arc check` 孤儿率 ≤ 20%（含孤 decision）
5. `arc trace D-xxx` 递归可达（至少 1 条 2 跳链）
6. 三校验器全绿 + step-gate 五步链 exit 0 + verify-anchor 全真实
7. 零 hook / 零校验器改动

---

## 5. 风险

| 风险 | 等级 | 缓释 |
|------|------|------|
| 二进制下载失败（网络） | 低 | 重试 + npm 备选（临时 npm install，不用 skill） |
| ADR frontmatter 不一致 | 中 | 预链接脚本容错（缺 depends 字段跳过 + 日志） |
| 导入实体冲突 | 低 | 每 ADR 独立 D-xxx 编号，实测校准 |

**Review 签字**: _________ 日期: _________