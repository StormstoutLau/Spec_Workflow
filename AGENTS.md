# AGENTS.md

> **本文件 = SPEC_PROCESS 的操作摘要桥**（CER C-01，spec/agents-md-bridge/）：让主流 agent 工具（Cursor / Copilot / Codex 等）进入本仓时拿到行为对齐指引。
> **权威源**：[SPEC_PROCESS.md](SPEC_PROCESS.md) —— 本文件保持"指针 + 最小摘要"，不复制规则全文；如有出入以 SPEC_PROCESS 为准。

## 仓库性质

纯文档方法论仓库：Spec 驱动开发规范（单人开发者 + LLM Agent）+ 反幻觉证据账本。核心目标 = **最大限度抑制 LLM 生成内容中的幻觉与形式化审查表演**（任何 agent 框架无法消除幻觉，只能某种程度地抑制）。

## 开发流程

本仓采用文档驱动开发：每个功能产出 `RESEARCH → DESIGN → IMPLEMENTATION → CHECKLIST` 四文档管道，偶数步为 Review 门禁。所有功能开发须遵守 [SPEC_PROCESS.md](SPEC_PROCESS.md) 的 10 步 Spec 流程与 Review 独立性规则（RULE-1~6）。

## 校验命令

修改任何文档后、提交前，运行以下校验器（pre-commit 已配置，提交时自动执行）：

- `python scripts/dc_validator.py` —— DC 契约校验 + 机械重数（R7）
- `python scripts/m7_stats.py` —— M7 证据账本 hits 块对账
- `python scripts/repo_stats.py` —— 视图层声明 = 机械重数对账

## 禁止事项

- 不得跳过 pre-commit 检查
- 不得手改 M7 账本的统计声明（由机械脚本重写）
- 破坏性文件操作（覆盖 / 截断 / 批量替换）前必须备份
- 文档中的计数声明必须与机械重数一致（声明 = 重数纪律）

## 权威源指针

| 主题 | 权威源 |
|------|--------|
| 流程宪法（10 步 + Review 规则） | [SPEC_PROCESS.md](SPEC_PROCESS.md) |
| 知识库 / 索引 / 版本 | [CODE_WIKI.md](CODE_WIKI.md) |
| 断言分级框架（A/B/C + E1-E5） | [docs/ASSERTION_EVIDENCE_FRAMEWORK.md](docs/ASSERTION_EVIDENCE_FRAMEWORK.md) |
| 证据账本 | [docs/M7_EVIDENCE_LOG.md](docs/M7_EVIDENCE_LOG.md) |
| 决策记录契约 | [docs/DECISION_RECORD_CONTRACT.md](docs/DECISION_RECORD_CONTRACT.md) |
| 待办登记 | [docs/PROGRESS.md](docs/PROGRESS.md) |