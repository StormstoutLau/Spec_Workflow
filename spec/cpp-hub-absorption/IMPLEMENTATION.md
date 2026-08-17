---
id: cpp-hub-absorption-IMPLEMENTATION
type: design
version: 1.0
status: verified
date: 2026-08-17
depends: [CPP_HUB_ABSORPTION_DESIGN, ADR-0007, ADR-0008, ADR-0009, FWK-ASSERTION, SPEC_PROCESS]
upstream: null
---

# cpp-hub-absorption 实施记录 IMPLEMENTATION.md v1.0 (2026-08-17)

> **性质声明**: 本 feature 为文档型——实施 = 文档编辑本体。本文件为**事后补齐的实施记录**（原偏差声明见 [CHECKLIST.md](./CHECKLIST.md) 头部：实施曾以 4 commits 记录替代独立 IMPLEMENTATION.md；2026-08-17 文档合规审计判定四件套应完整，补齐本文件使每处修改可独立追溯）。内容全部来自已推送的 git 提交与验证 grep，无新增实施动作。
> **验证状态**: 每行附 commit hash（E1 可重放：`git show <hash>`）+ 验证 grep 模式。

## 1. 实施清单（设计 §4 接口 → 编辑位点 → 提交）

### D1: 框架 v1.2 → v1.3（STEP_GAP 两态分型）

| # | 编辑位点 | 内容 | commit | 验证 |
|---|---------|------|--------|------|
| 1 | 框架 L3 头部 | 版本链 +v1.3 | f79fa49→**8a4bfda 修复**（首编辑被 DIS-008 竞态回滚，v1.4 批次 Read 拦截后补） | grep `v1\.3.*STEP_GAP` L3 |
| 2 | §4.3 双盲流程注释 ×2 | STEP_GAP flag → 两态判定；仲裁触发条件改 OPEN | f79fa49 | grep L164/L167 |
| 3 | §4.4-3 | 两态定义块（CLOSED/OPEN/兼容规则，含 pilot B1 实例） | f79fa49 | grep `STEP_GAP_CLOSED` |
| 4 | §6 效率账 | "STEP_GAP 分型复查" | f79fa49 | grep L201 |
| 5 | §7 状态词表 | 两态词表 + 兼容行 | f79fa49 | grep L265 |
| 6 | §7.1 闭环动作 | OPEN→仲裁 / CLOSED→标注闭合证据 | f79fa49 | grep L276 |
| 7 | §7.2 报告骨架 | double_blind 行双态语义 | f79fa49 | grep L287 |
| 8 | §9 同步对声明 | v1.3/v1.2 分列 + 007 不随升 | **8a4bfda 修复**（同 #1 回滚） | grep L312 |
| 9 | 修订历史 | v1.3 行（含来源锚点 pilot §5.1-3） | f79fa49 | grep L327 |
| 10 | DIS-007 L4 | 硬编码版本指针解耦（同步对声明移框架 §9） | f79fa49 | grep 007 L4 |

### D2/D3: M7 证据账本

| # | 动作 | 内容 | commit |
|---|------|------|--------|
| 1 | 新建 docs/M7_EVIDENCE_LOG.md | 样本表 4 行（PLAN §6 两轮 + pilot + GAP_AUDIT）+ 形态 II 分桶（4 载体 × 7 字段 = 10 处）+ Phase 5 baseline 14 处 | f79fa49 |
| 2 | 样本 ⑤ 追加 | cpp-hub-absorption DESIGN Step 4 Review 轮（2P2+6P3，映射闭合 1） | 1ae64a4 |
| 3 | P-005 挂钩勾销 | §0 计数规则落框架 v1.4 R7 | 8a4bfda |

### D4/D6: SPEC_PROCESS v1.3 → v1.4

| # | 编辑位点 | 内容 | commit | 验证 |
|---|---------|------|--------|------|
| 1 | L4 头部修订链 | +v1.4（ADR-0008/0009 锚点） | b7a7f58 | grep L4 |
| 2 | Step 2 Review 章末 | 【门禁】块 (a)-(d) + D5 集成点①注记 | b7a7f58 | grep `【门禁】` L183 |
| 3 | Step 8 清单 | +双向引用完整 / +断言延续 | b7a7f58 | grep L233/L236 |
| 4 | ADD 产出循环 | D5 集成点②（系统性模式→discoveries） | b7a7f58 | grep L264 |

### D5: ADR-0009 + discoveries

| # | 动作 | 内容 | commit |
|---|------|------|--------|
| 1 | 新建 adr/ADR-0009 | accepted；最小版三态索引决策 + DIS-008 实测背景 | b7a7f58 |
| 2 | 新建 docs/discoveries/README.md | 登记格式（五字段）+ 索引（001~006 源项目 / 007 映射 / 008 首登） | b7a7f58 |
| 3 | DIS-008 复发追记 | v1.3 头部/§9 回滚两处 + 终验教训升级 | 8a4bfda |

### Tier3: 无实施动作（设计 §3.1 拒收清单六项 + 理由表，eed0906）

### 追加（P-005 收口）: 框架 v1.3 → v1.4

| # | 编辑位点 | 内容 | commit |
|---|---------|------|--------|
| 1 | L3 头部 / §3 自检 / §7 R7 / 修订历史 | R7 统计表计数机械枚举规则（4 处） | 8a4bfda |

## 2. 版本与依赖

无运行时依赖（纯 Markdown 文档）。git 为唯一依赖（E1 证据链）。

## 3. 提交映射总表

| commit | 类型 | 对应设计项 |
|--------|------|-----------|
| 8ea38bf | adr | ADR-0007 v1.1 + ADR-0008 v1.1 定版（决策层先行） |
| eed0906 | spec | DESIGN v1.1（P2-1/P2-2 修正清零） |
| f79fa49 | feat(tier1) | D1-D3（框架 v1.3 + M7 账本 + 007 解耦） |
| b7a7f58 | feat(tier2) | D4-D6（SPEC_PROCESS v1.4 + ADR-0009 + discoveries） |
| 1ae64a4 | checklist | CHECKLIST 验收 + DEV-LOG-002 + M7 样本⑤ |
| 8a4bfda | feat(framework) | 框架 v1.4 R7 + DIS-008 复发修复（D1 两处回滚补） |

> 与设计 §9.2 提交切分的偏差：原方案"ADR-0008+SPEC_PROCESS 一提交"——实际 ADR 定版批次先行（用户逐份确认节奏所致），双向链接同批闭合，CHECKLIST §1.2 已声明。

## 4. 已知问题与缓解

| 问题 | 缓解 | 状态 |
|------|------|------|
| DIS-008 同文件并行 Edit 静默回滚（D1 两处漏网至 v1.4 批次） | 同文件编辑严格串行 + 编辑前 Read + 终验 grep 全覆盖修改行 | 登记于 discoveries（open） |
| PowerShell 无 heredoc | 多 `-m` 参数替代 | 已解决 |
| MCP search_semantic 空返回 / web 镜像超时 ×4 | arXiv/WebSearch/StackExchange API 多通道兜底，失败如实登记 | 已解决 |

## 5. 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-08-17 | 事后补齐（文档合规审计）：从 git 提交与验证 grep 汇编实施记录，含 DIS-008 回滚修复的完整轨迹 |
