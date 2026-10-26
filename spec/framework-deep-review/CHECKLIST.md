# 审查验收 Checklist：批次绑定门禁（O3 Phase 1）

---

id: framework-deep-review-CHECKLIST
type: design
version: 1.1
status: accepting
date: 2026-10-26
depends: [framework-deep-review-IMPLEMENTATION, framework-deep-review-DESIGN]
upstream: null

---

> **Feature**: framework-deep-review（U-1 / O3 Phase 1 门禁实施）
> **创建日期**: 2026-10-26
> **状态**: 验收中（有条件通过：Linux 未实测）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [IMPLEMENTATION.md](./IMPLEMENTATION.md)
> **基于设计**: [DESIGN.md](./DESIGN.md)

---

## 1. 文档一致性验收（Step 8）

### 1.1 RESEARCH ↔ DESIGN 对齐

| 检查项 | 状态 | 说明 |
|---|---|---|
| DESIGN 的 O3 决策可追溯到 RESEARCH §11 | ☑ | §11.6 声明优先级 |
| RESEARCH 的 A-36~A-42 被 DESIGN 使用 | ☑ | §2.1 / §8 |
| 无文档间矛盾 | ☑ | 完整性规则已统一为「带文档改动必须 5/5」 |

### 1.2 DESIGN ↔ IMPLEMENTATION 对齐

| 检查项 | 状态 | 说明 |
|---|---|---|
| DESIGN §3.2 模块均有实施 | ☑ | `spec_map` + `step_enforce` |
| 接口签名一致 | ☑ | §4.1~§4.3 |
| 不变式 I-1~I-8 均有实施 | ☑ | §7 映射表 |
| 无设计未覆盖的实施 | ☑ | `_local_changed` 已回写 DESIGN §3.3 步 2 |

### 1.3 IMPLEMENTATION ↔ CHECKLIST 对齐

| 检查项 | 状态 | 说明 |
|---|---|---|
| 15 个测试用例均有验收项 | ☑ | §2.1 列 14 项；git 错误见 §5 |
| 验收项可追溯到 IMPLEMENTATION §3.5 | ☑ | 用例编号一致 |

### 1.4 术语一致性

| 术语 | RESEARCH | DESIGN | IMPLEMENTATION | 一致 |
|---|---|---|---|---|
| batch / session / branch / maintenance | §11.6 | §3.4 | §3.2 | ☑ |
| P 行声明 | §11.6 | §4.2 | §4.1 | ☑ |
| 完整性 5/5 | §11.6 | I-4 | §3.2 | ☑ |

## 2. 功能验收

### 2.1 模式与故障注入

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| #1 新 P 行 + 5/5 + 文档 | `test_batch_pass` | exit 0，mode=batch | ☑ | unittest ok |
| #2 新 P 行 + 1/5 + 文档 | `test_batch_one_step_fails` | exit 1 | ☑ | unittest ok |
| #3 旧 session + 语义文档 + 无声明 | `test_no_declaration_fails` | exit 1 | ☑ | unittest ok |
| #4 改 session + 文档（P 行已在 HEAD） | `test_session_mode_pass` | exit 0，mode=session | ☑ | unittest ok |
| #5 分支 p130 + 5/5 | `test_branch_mode_pass` | exit 0，mode=branch | ☑ | unittest ok |
| #6 whitespace-only | `test_maintenance_whitespace_pass` | exit 0，mode=maintenance | ☑ | unittest ok |
| #7 多 feature 批次 | `test_multi_feature_batch_pass` | exit 0 | ☑ | unittest ok |
| #8 新 P 行 0 链接 | `test_new_p_row_no_links_fails` | exit 1 | ☑ | unittest ok |
| #9 v9(1/5) + v10(5/5) | `test_no_filename_sort_trap` | exit 0 | ☑ | unittest ok |
| #10 feature 不在 P 行 | `test_feature_not_covered_fails` | exit 1 | ☑ | unittest ok |
| #11 只改 session 1/5 | `test_session_progress_passes` | exit 0 | ☑ | unittest ok |
| #12 只加 P 行 | `test_batch_registration_passes` | exit 0 | ☑ | unittest ok |
| #13 `--all-files` 全量 argv | `test_all_files_mode_ignores_unchanged` | 未变更不误判；真实变更仍 fail | ☑ | unittest ok + 真实仓全量复验 |
| #14 分块 argv（pre-commit chunk） | `test_partial_argv_uses_git_change_set` | 单块无声明文件不误判，仍 batch pass | ☑ | unittest ok + 六 hook 实测 |

## 3. 接口验收

| 验收项 | 通过条件 | 状态 |
|---|---|---|
| `parse_progress_rows` 签名 | 与 DESIGN §4.1 一致 | ☑ |
| `changed_pids` 签名 | 与 DESIGN §4.2 一致 | ☑ |
| `resolve` 签名 | 与 DESIGN §4.3 一致 | ☑ |
| `check_sessions` 签名 | 与 DESIGN §4.4 一致 | ☑ |

## 4. 不变式验收

| 不变式（DESIGN §8） | 验证方法 | 状态 |
|---|---|---|
| I-1 无声明不放行语义改动 | #3 | ☑ |
| I-2 声明必须可解析 | #8 | ☑ |
| I-3 覆盖闭合 | #7 / #10 | ☑ |
| I-4 完整性按边界 | #2 / #11 | ☑ |
| I-5 维护模式不冒充完成 | #6 | ☑ |
| I-6 exit 2 fail-closed | 坏仓实测（`test_git_error_returns_2`） | ☑ |
| I-7 不依赖文件名排序 | #9 | ☑ |
| I-8 本地/CI 同源 | 本地 hook + CI step（同一脚本与模式解析） | ☑ |

## 5. 错误处理验收

| 错误场景（DESIGN §7） | 触发方式 | 预期行为 | 状态 |
|---|---|---|---|
| 无声明语义改动 | #3 | exit 1 | ☑ |
| 新 P 行 0 链接 | #8 | exit 1 | ☑ |
| feature 未覆盖 | #10 | exit 1 | ☑ |
| 声明无 5/5 session | #2 | exit 1 | ☑ |
| 新 P 行无 session | #2 | exit 1 | ☑ |
| 只改 session 1/5 | #11 | exit 0 | ☑ |
| 只加 P 行 | #12 | exit 0 | ☑ |
| git 读取失败 | 临时坏仓 | exit 2 | ☑ |

## 6. 性能验收

| 性能指标 | 目标 | 实测 | 状态 |
|---|---|---|---|
| 单次 hook 墙钟（本仓全量，66 文档 + 154 session） | < 5 s | 1.14 s | ☑ |
| 批次绑定集成测试总时长 | < 60 s | 13.5 s（全套 23 例 11.6 s） | ☑ |

## 7. 兼容性验收

| 环境 | 版本 | 状态 | 说明 |
|---|---|---|---|
| Python | 3.11 | ☑ | 本机 / CI |
| OS | Windows | ☑ | 本机 / CI |
| OS | Linux | ☐ | 仅依赖 stdlib + git；未在本机实测 |

## 8. ADD 审计（Step 10）

### 8.1 Spec 质量门（Phase 0）

| 维度 | 得分（0-1） | 说明 |
|---|---|---|
| 可测试约束 | 1 | 12 例矩阵 |
| 模块映射 | 1 | `spec_map` / `step_enforce` |
| 接口契约 | 1 | §4 签名 |
| 修正项 | 1 | 边界与维护模式已修正 |
| 跨模块契约 | 1 | hook / CI / runner 三方一致 |
| **总分** | 5/5 | **档位**: A |

### 8.2 ADD 审计发现

| 严重性 | 发现 | 证据 | 修复建议 |
|---|---|---|---|
| P1 | 无 | - | - |
| P2 | 无 | - | - |
| P3 | 分支名弱声明在 detached HEAD 下不可用 | DESIGN §3.4 | 已登记 U-1 分支回退；不阻塞 |

### 8.3 ADD Iron Law 检查

- [x] 断言恒真式：测试使用 exit code / 输出字符串双断言
- [x] 单文件检查盲区：新增 `tests/test_batch_binding.py`，不改旧测试
- [x] 设计独有约束：I-1~I-8 均有测试映射
- [x] 修正阻断性项：维护模式 / exit 2 均有对应用例

## 9. 文档完整性

| 文档 | 存在 | 与实现一致 |
|---|---|---|
| RESEARCH.md | ☑ | ☑ |
| DESIGN.md | ☑ | ☑ |
| IMPLEMENTATION.md | ☑ | ☑ |
| CHECKLIST.md（本文件） | ☑ | ☑ |
| ADR（如有） | 不适用 | - |
| 开发日志 | 不适用 | - |

## 10. 验收结论

### 10.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|---|---|---|---|---|
| 文档一致性 | 12 | 12 | 0 | 0 |
| 功能 | 14 | 14 | 0 | 0 |
| 接口 | 4 | 4 | 0 | 0 |
| 不变式 | 8 | 8 | 0 | 0 |
| 错误处理 | 8 | 8 | 0 | 0 |
| 性能 | 2 | 2 | 0 | 0 |
| 兼容性 | 3 | 2 | 0 | 1 |
| ADD 审计 | 4 | 4 | 0 | 0 |
| **总计** | 55 | 54 | 0 | 1 |

> **统计口径（RULE-2）**：上表来自逐项核对，非事后汇总推算。

### 10.2 验收决定

- [ ] **验收通过**：所有 P1 项通过，无阻塞性问题
- [x] **有条件通过**：Linux 平台未在本机实测；其余 54 项全通过，无失败项
- [ ] **验收失败**：<原因>

### 10.3 签字

| 角色 | 签字 | 日期 |
|---|---|---|
| 实施者 | 单 Agent | 2026-10-26 |
| 审查者 | 单 Agent 自查（单视角） | 2026-10-26 |

## 11. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|---|---|---|---|
| 更新 PROGRESS.md（P-130） | 实施者 | 本批 | ☑ |
| 更新 CODE_WIKI / CONSOLE | 实施者 | 本批 | ☑ |
| Phase 2（session_start / digest） | 待裁决 | 未定 | 未开始 |
