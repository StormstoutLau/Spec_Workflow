# 验收清单：AGENTS.md 桥（P-021）

---
id: agents-md-bridge-CHECKLIST
type: design
version: 1.0
status: accepted
date: 2026-09-08
depends: [agents-md-bridge-DESIGN, community-ecosystem-RESEARCH, ADR-0010]
upstream: null
---

> **Feature**: AGENTS.md 桥文件生成（CER C-01）
> **Spec 步骤**: Step 7-8
> **验收对象**: 根 `AGENTS.md` + [DESIGN.md](./DESIGN.md) + doc_registry 登记
> **验收运行**: 本清单为自查（生成端）检录；**独立 pass 见 §6**（RULE-1 时序独立惯例）

---

## 1. 文档一致性验收

- [x] **DC1-1**：AGENTS.md 四段（性质/流程/命令/禁止事项 + 指针表五段）与 DESIGN §6.1 结构一致
- [x] **DC1-2**：AGENTS.md 全部指针链接正确（6 个相对链接指向存在的文件）
- [x] **DC1-3**：DESIGN 引用 CER 断言编号正确（C-01 / §3.4 矩阵 / §5.4 H1 / A-04~A-06）
- [x] **DC1-4**：前向引用——AGENTS.md 指向 SPEC_PROCESS 为权威源（单向依赖）

## 2. 功能/内容验收

- [x] **F-1**：AGENTS.md **零可漂移声明**（无 feature 目录数/样本数/版本号/文件数/星数）——I-1
- [x] **F-2**：三个校验命令精确（`python scripts/dc_validator.py` / `m7_stats.py` / `repo_stats.py` + 用途）
- [x] **F-3**：禁止事项含 R6/M5 门禁四要义（不跳 hook / 不手改 M7 声明 / 破坏性操作先备份 / 声明=重数）——I-2 指针化
- [x] **F-4**：权威源指针表 6 行（SPEC_PROCESS/CODE_WIKI/ASSERTION_EVIDENCE_FRAMEWORK/M7_EVIDENCE_LOG/DECISION_RECORD_CONTRACT/PROGRESS）均指向真实文件

## 3. 懒加载审核验收（ADR-0010 三问，DESIGN §4 回填）

- [x] **L-1**：Q1 分层判定 = **Layer-0**（单一静态文件、无运行时、无激活管线；与 CER v1.3 预演一致）
- [x] **L-2**：Q2 激活条件 = **生成即激活**（无触发依赖；激活零副作用由 I-1 保证）
- [x] **L-3**：Q3 未激活副作用 = **0**（文件不存在即工具无接口；文档层自足）
- [x] **L-4**：无连坐依赖（AGENTS.md 不依赖任何其他候选）；审核结论 = **通过**

## 4. 兼容性验收（CER H1）

- [x] **C-1**：工具支持既有取证——CER A-04：AGENTS.md 23 款工具原生支持（较新规范由 Linux 基金会 Agentic AI Foundation 托管）；A-06/C-01 社区惯例
- [x] **C-2**：文件格式可用性——UTF-8、标准 GitHub-Flavored Markdown、无非法字符/控制符（`python scripts/dc_validator.py` 无报错，跳过非契约文件而非非法）
- [x] **C-3**：H1 实测定性——本仓为方法论文档仓，工具读取价值场景有限（CER §5.4 原述）；已满足"零成本 + 收益非零下限"（工具进入即行为对齐），残余价值不确定性登记观察，不阻塞

## 5. 环境/校验器验收

- [x] **E-1**：`dc_validator.py` 全仓 74 文件 0 违规（AGENTS.md 无 front-matter → skip，符合设计预期）
- [x] **E-2**：`m7_stats.py` 0 违规（P3 提示 1 = 已知非标准形态）
- [x] **E-3**：`repo_stats.py` 0 违规（declared.spec_feature_dirs 17→18 / §2.1 树 / §9 索引 / doc_registry 四处同步完成）
- [x] **E-4**：doc_registry 新条目 `agents-md-bridge → spec/agents-md-bridge/DESIGN.md` 被 repo_stats 枚举通过

## 6. ADD 审计（Phase 0 质量门）

**不变式满足检查**：

| 不变式 | 状态 | 证据 |
|--------|------|------|
| I-1 零可漂移声明 | ✅ | F-1 通过；repo_stats PT 模式对 AGENTS.md 零命中 |
| I-2 指针化不复制 | ✅ | F-3/F-4 通过；全文无规则全文复制 |
| I-3 零工具改动 | ✅ | 交付物 = AGENTS.md 1 文件 + doc_registry 1 行；无脚本/hook 改动 |
| I-4 单向依赖 | ✅ | AGENTS.md → SPEC_PROCESS；文档层无反向依赖 |

**Iron Law 盲区扫描**：

| 盲区 | 检查 | 结果 |
|------|------|------|
| 计数盲区（声明=重数） | AGENTS.md 无计数声明；doc_registry 枚举通过 | ✅ |
| 版本盲区 | DESIGN v1.0；CODE_WIKI §9 索引 v1.0 同步 | ✅ |
| 兼容盲区 | H1 定性 + C-1~C-3 | ✅ |
| 一致性盲区 | 四文档对齐（CER→DESIGN→AGENTS.md→CHECKLIST） | ✅ |

---

## 7. 验收统计与决定

| 项 | 值 |
|----|-----|
| 通过项 | 20/20（DC1×4 + F×4 + L×4 + C×3 + E×4 + ADD 不变式 4） |
| P1 项 | 0 |
| P2 项 | 0 |
| P3 观察 | 1（H1 残余价值不确定性——登记观察不阻塞，CER §5.4 [H1]） |
| **验收决定** | ✅ 通过（自查）——待独立 pass 复核 |

**签字**: _________ 日期: _________

---

## 8. 独立 pass 记录（Step 8，RULE-1 时序独立机械复核）

> 复核视角：对自查结论做独立重验（不依赖自查记忆），范围 = 自查 20 项的核心证据链。

| 复核项 | 独立验证 | 结果 |
|--------|---------|------|
| I-1 零可漂移声明 | 独立重扫 AGENTS.md 数字出现：全部为标识符/流程特征名（C-01/R7/M7/10 步/E1-E5），**无 feature 目录数/样本数/版本号/星数**；PT 敏感词（「feature 目录」「样本」「形态 II」）零命中 | ✅ |
| I-2 指针真实性 | 独立 Test-Path 复核 6 个指针目标：SPEC_PROCESS/CODE_WIKI/ASSERTION_EVIDENCE_FRAMEWORK/M7_EVIDENCE_LOG/DECISION_RECORD_CONTRACT/PROGRESS 全部存在 | ✅ |
| I-3 零工具改动 | git diff 仅新增 AGENTS.md + spec/agents-md-bridge/ 两文档 + CODE_WIKI 登记，无脚本/hook 改动 | ✅ |
| 校验器 | dc_validator 74 文件 0 违规 / m7_stats 0 违规 / repo_stats 0 违规（三通道独立重跑） | ✅ |

**独立 pass 结论**：自查 20 项与核心证据链一致，无表演性勾选；**通过（accepted）**。

**签字**: _________ 日期: 2026-09-08

---

- 2026-09-08：创建 AGENTS.md（五段式）；CODE_WIKI 四处同步（declared/目录树/§9/doc_registry）；三校验器全绿
- 懒加载审核：ADR-0010 三问正式执行（DESIGN §4），结论通过，本 feature 自身 = Layer-0 优先于 Layer-1 的再实证