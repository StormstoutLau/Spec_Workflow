# 审查验收 Checklist：批次绑定门禁（O3 Phase 1）

---

id: framework-deep-review-CHECKLIST
type: design
version: 1.17
status: accepting
date: 2026-10-26
depends: [framework-deep-review-IMPLEMENTATION, framework-deep-review-DESIGN]
upstream: null

---

> **Feature**: framework-deep-review（U-1 / O3 Phase 1 门禁实施）
> **创建日期**: 2026-10-26
> **修订**: v1.3（2026-10-26，P-132：runner `step-gate` 显式声明验收 3 项）
> **修订**: v1.4（2026-10-26，P-134：CI fail-closed 验收 4 项（§2.4），功能 22 → 26）
> **修订**: v1.5（2026-10-27，P-137：digest 绑定验收 8 项（§2.5），功能 26 → 34、接口 4 → 6、不变式 8 → 13、错误处理 8 → 12；总计 67 → 86）
> **修订**: v1.6（2026-10-27，P-139：真实 runner 集成回归验收 14 项（§2.6），功能 34 → 48、不变式 13 → 16、文档一致性 12 → 13；总计 86 → 104）
> **修订**: v1.7（2026-10-27，P-140：CI 逐提交遍历验收 4 项（§2.7）＋不变式 I-11a~c（§4），功能 48 → 52、不变式 16 → 19；总计 104 → 111）
> **修订**: v1.8（2026-10-28，P-141：CI 远端读数回填验收 1 项（§2.7 #47），功能 52 → 53；总计 111 → 112）
> **修订**: v1.9（2026-10-28，P-142：`push(main)` 合并面实测验收 1 项（§2.7 #48），功能 53 → 54；总计 112 → 113）
> **修订**: v1.10（2026-10-28，P-143：`push(main)` 补充读数验收 1 项（§2.7 #49），功能 54 → 55；总计 113 → 114）
> **修订**: v1.11（2026-10-28，P-144：evil merge 检测验收 4 项（§2.8 #50~#53）＋不变式 I-11d / I-11e（§4），功能 55 → 59、不变式 19 → 21；总计 114 → 120）
> **修订**: v1.12（2026-10-28，P-145：阶段 1 远端读数验收 1 项（§2.8 #54），功能 59 → 60；总计 120 → 121）
> **修订**: v1.13（2026-10-28，P-146：阶段 1 远端第 2 样本验收 1 项（§2.8 #55），功能 60 → 61；总计 121 → 122）
> **修订**: v1.14（2026-10-28，P-147：阶段 1 远端第 3 样本验收 1 项（§2.8 #56），功能 61 → 62；总计 122 → 123）
> **修订**: v1.15（2026-10-28，P-148：阶段 1 远端第 4 样本验收 1 项（§2.8 #57），功能 62 → 63；总计 123 → 124）
> **修订**: v1.16（2026-10-28，P-149：阶段 1 远端第 5 样本验收 1 项（§2.8 #58），功能 63 → 64；总计 124 → 125）
> **修订**: v1.17（2026-10-28，P-150：PR 面阶段 1 命中读数订正验收 1 项（§2.8 #59），功能 64 → 65；总计 125 → 126）
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
| 42 个测试用例均有验收项 | ☑ | §2.1 列 14 项；§2.2 列 5 项；§2.5 列 8 项（P-137）；**§2.6 列 14 项（P-139）**；git 错误见 §5（1 项）；§2.3 另列 runner selftest 3 项（不计入 42 例矩阵） |
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

### 2.2 U-2 完整链注入（P-131）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| 0/5 session + 文档 | `test_zero_step_session_fails` | exit 1（内部不一致） | ☑ | unittest ok |
| 4/5 session + 文档 | `test_four_step_session_fails` | exit 1（无 5/5） | ☑ | unittest ok |
| P-128 维护模式 + 1/5 | `test_maintenance_boundary_128_legacy_partial_passes` | exit 0，mode=maintenance | ☑ | unittest ok |
| P-129 维护模式 + 1/5 | `test_maintenance_boundary_129_requires_complete` | exit 1（边界含 129） | ☑ | unittest ok |
| P-128 显式声明 + 文档 + 1/5 | `test_legacy_declaration_with_docs_still_requires_complete` | exit 1（声明不豁免） | ☑ | unittest ok |

### 2.3 runner 显式声明（P-132）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| 未声明（无 `--expect` / `--legacy`） | selftest F80 | exit 2 且含「必须显式声明」 | ☑ | `selftest: 83/83 passed` |
| 双声明（`--expect` + `--legacy`） | selftest F81 | exit 2 且含「互斥」 | ☑ | `selftest: 83/83 passed` |
| 内部调用方显式 legacy | `scripts/step_enforce.py` `_run_gate` | 无 expect 时显式传 `--legacy` | ☑ | 20 例批次绑定全通过 |

### 2.4 CI fail-closed 验收（P-134）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| 坏 base 显式红 | 本地注入：不存在引用传给 `git diff` | `exit 1` 且输出含 `fail-closed` | ☑ | 注入 5/5（临时仓 git-bash） |
| 无变更绿灯 | 本地注入：变更集为空 | `exit 0`，不调用门禁 | ☑ | 注入 5/5 |
| 根提交不误伤 | 本地注入：before 全零且无 `HEAD^` | `BASE=HEAD` 回退，`exit 0` | ☑ | 注入 5/5 |
| 归档数字订正一致 | 全覆盖 grep：`152 个 specwf` 与 `152 specwf` 与 `152/152` | 仅 RESEARCH 附录 D 归档报告原文（D.1~D.6 逐字收录）保留，以 D.0 订正表为准；PROGRESS / CODE_WIKI 均为 151；历史 session 事件流不重写 | ☑ | 终验 grep（提交前全覆盖执行） |

### 2.5 digest 绑定验收（P-137）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| #21 P-137 + 正确 digest | `test_digest_bound_pass_p137` | exit 0，`mode=batch`，输出 `digest_bound=1`；作用域 = 四文档命名 | ☑ | unittest ok |
| #22 P-137 缺 `evidence_digest` | `test_digest_missing_fails_p137` | exit 1 且含 `evidence_digest` | ☑ | unittest ok |
| #23 验后改文档（digest 后改并提交） | `test_digest_mismatch_after_finalize_fails` | exit 1 且含「digest 不匹配」 | ☑ | unittest ok |
| #24 finalize 后新增四文档 | `test_digest_file_set_mismatch_fails` | exit 1 且含「文件集不一致」 | ☑ | unittest ok |
| #25 rebind 无 `rebind_reason` | `test_digest_rebind_without_reason_fails` | exit 1 且含「rebind 缺原因」 | ☑ | unittest ok |
| #26 rebind 有原因 | `test_digest_rebind_with_reason_passes` | exit 0（受控回边 + 再入 finalize 仍判 5/5） | ☑ | unittest ok |
| #27 P-136 无 digest + 文档改动 | `test_digest_historical_p136_not_checked` | exit 0（历史不重验），无 `digest_bound` 输出 | ☑ | unittest ok |
| #28 无文档改动双模式 | `test_digest_not_applied_without_docs` | `session-progress` / `batch-registration` 均 exit 0 且不校验 | ☑ | unittest ok |

### 2.6 真实 runner 集成回归验收（P-139）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| #29 step-gate 完整链 | `test_step_gate_complete_chain_pass` | exit 0 且含「决策链一致 pass」 | ☑ | unittest ok |
| #30 step-gate 缺步 | `test_step_gate_missing_step_hard_fail` | exit 1 且含 `[HARD]` | ☑ | unittest ok |
| #31 step-gate 无显式声明 | `test_step_gate_requires_explicit_declaration` | exit 2 且提示 `--expect` | ☑ | unittest ok |
| #32 step-gate legacy | `test_step_gate_legacy_internal_consistency` | 4/5 步 exit 0 且含 `mode=legacy` | ☑ | unittest ok |
| #33 verify-anchor 真实锚点 | `test_verify_anchor_real_pass` | exit 0，`锚点 5 真实` + `[DETAIL]` | ☑ | unittest ok |
| #34 verify-anchor 文件缺失 | `test_verify_anchor_missing_file_hard_fail` | exit 1 且含「文件不存在」 | ☑ | unittest ok |
| #35 fork 前缀复制 | `test_fork_copies_prefix_rows` | exit 0，新流行数 = 请求前缀 | ☑ | unittest ok |
| #36 anchor-audit 不变量 | `test_anchor_audit_invariant_holds` | exit 0（`J2\J1` 差集空） | ☑ | unittest ok |
| #37 backflow-audit 零待处理 | `test_backflow_audit_zero_pending` | exit 0 | ☑ | unittest ok |
| #38 触发面 parity | `test_gate_surface_parity` | hook 触发面含 runner + CI 跑同一 `unittest discover` | ☑ | unittest ok + `pre-commit run --files runner` Passed |
| #39 M1 删除完整链检查 | `test_m1_delete_complete_chain_check` | 原版 exit ≠ 变异版 exit | ☑ | unittest ok |
| #40 M2 静态最新 P | `test_m2_revert_to_static_latest_pid` | 原版 exit 1 ≠ 变异版 exit 0 | ☑ | unittest ok |
| #41 M3 吞掉 gate 硬失败 | `test_m3_swallow_gate_hard_failure` | 原版 exit ≠ 变异版 exit | ☑ | unittest ok |
| #42 M4 破坏锚点解析 | `test_m4_break_anchor_path_resolution` | 原版 exit ≠ 变异版 exit | ☑ | unittest ok |

14/14 通过（P-139）；增量读数 = 新增两模块 **8.7 s**（全套 `unittest discover` **36 → 50**，39.6 s）⇒ U-3 判据「4/4 捕获 + 增量可接受」满足；CI 远端增量为**同命令代理读数**（本批不推送，如实登记）。

### 2.7 CI 逐提交遍历验收（P-140）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| #43 逐提交遍历全绿 | temp 克隆真实分支，逐提交跑 `step_enforce`（range `b0e6534..1ac992a`） | 16 个非合并提交逐条 pass，`EXIT=0` | ☑ | A-46（本地 temp 仓实测） |
| #44 digest 各自批次匹配 | 同上（P-137 / P-138 / P-139 三个提交） | 各输出 `digest_bound=1` | ☑ | A-46 |
| #45 合并提交跳过 | temp 仓合成 merge（父 = 分支头 + main 侧新提交） | range 17 条中 merge 被 skip、16 受判、`EXIT=0` | ☑ | A-46 |
| #46 CI 形态 guard | `test_ci_per_commit_walk` | 5 断言全过；`BASE...HEAD` 单次 diff 形态不存在 | ☑ | unittest ok |
| #47 CI 远端首次实测 | `gh run watch 40579430749 --exit-status` | `verify` job 成功（1m30s）、8 step 全 ✓（含 step-enforce 逐提交步）；PR #58 `verify = SUCCESS` | ☑ | A-47（P-141 回填） |
| #48 `push(main)` 合并面实测 | `gh run view 40585936395`（`push` 事件，合并提交 `adfec33`） | `verify` 成功（墙钟 68 s）、8 step 全 ✓；`skip merge commit adfec33`、受判 **18** 个非合并提交、无并集式假红 | ☑ | A-48（P-142 回填） |
| #49 `push(main)` 补充读数 | `gh run view 40589457291`（`push` 事件，合并提交 `3bb7680`） | `verify` 成功（墙钟 87 s）、8 step 全 ✓；`skip merge commit 3bb7680`、受判 **1** 个非合并提交（小 range 同样成立） | ☑ | A-48 第 2 样本（P-143 登记） |

4/4 通过（P-140）+ **#47（P-141 回填）** + **#48（P-142 回填）** + **#49（P-143 补充）** 全通过；对照实验 = HEAD 版执行器复验历史内容 ⇒ P-127 提交变红（追溯规则实证，A-46）⇒ 方案 B 否决依据；旧单次 diff 复跑（P-127 修后）= P-137/P-138 `digest 不匹配` exit 1（A-45 ②）。

### 2.8 evil merge 检测验收（P-144）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|---|---|---|---|---|
| #50 evil 内容判红 | `test_evil_merge_detected`（冲突解决写入两父皆无内容） | `--check-merge` exit 1；stderr 含「evil merge 内容（两父皆无）」+ 路径 | ☑ | A-50 |
| #51 干净合并不判 | `test_clean_merge_passes`（两侧改不同文件） | exit 0；输出「无 evil 内容」 | ☑ | A-50 |
| #52 等于第一父不判 | `test_merge_equals_first_parent_passes`（main 侧只改非受判文件） | exit 0；输出「0 个受判路径」 | ☑ | A-50 |
| #53 非合并提交 no-op | `test_check_merge_non_merge_commit_is_noop` | exit 0；输出「非合并提交」 | ☑ | A-50 |
| #54 阶段 1 远端首次判定 | `push(main)` run `40603730644`（合并提交 `e8154eb`） | `无 evil 内容（6 个受判路径均等于某一父）`；阶段 2 skip + 受判 1 个；88 s 全绿 | ☑ | A-50 远端样本 |
| #55 阶段 1 远端第 2 样本 | `push(main)` run `40660622448`（合并提交 `7bcce12`） | 再次 `无 evil 内容（6 个受判路径均等于某一父）`；阶段 2 skip + 受判 1 个；89 s 全绿 | ☑ | A-50 远端样本 2 |
| #56 阶段 1 远端第 3 样本 | `push(main)` run `40663831556`（合并提交 `023e456`） | 再次 `无 evil 内容（6 个受判路径均等于某一父）`；阶段 2 skip + 受判 1 个；66 s 全绿 | ☑ | A-50 远端样本 3 |
| #57 阶段 1 远端第 4 样本 | `push(main)` run `40666293529`（合并提交 `fb01568`） | 再次 `无 evil 内容（6 个受判路径均等于某一父）`；阶段 2 skip + 受判 1 个；82 s 全绿 | ☑ | A-50 远端样本 4 |
| #58 阶段 1 远端第 5 样本 | `push(main)` run `40676513311`（合并提交 `64c6313`） | 再次 `无 evil 内容（6 个受判路径均等于某一父）`；阶段 2 skip + 受判 1 个；81 s 全绿 | ☑ | A-50 远端样本 5 |
| #59 PR 面阶段 1 命中（订正） | 复读 6 个 `pull_request` run 日志（`40603562855` / `40660422565` / `40663491255` / `40666075396` / `40676348854` / `40677799676`） | 每个 PR 均命中 GitHub **合成 merge ref**（`refs/pull/N/merge`，`actions/checkout@v5` 在 `pull_request` 下默认检出）并判 `无 evil 内容（6 个受判路径均等于某一父）`；原记「未命中」订正为「命中」（根因 = 误读阶段 2 的 `受判提交 1 个`） | ☑ | RESEARCH §14.8.1 |

10/10 通过（#50~#53 本地四态 + #54~#58 远端五样本 + #59 PR 面命中订正）；**实验仓交叉验证**（A-49）：同一句内容走合并解决 ⇒ 循环 exit 0（逃逸）、走普通提交 ⇒ exit 1；`--check-merge` 对前者 exit 1、对非合并提交 exit 0。CI 接线 guard = `test_ci_per_commit_walk` 第 6 断言（含 `--check-merge`）。

## 3. 接口验收

| 验收项 | 通过条件 | 状态 |
|---|---|---|
| `parse_progress_rows` 签名 | 与 DESIGN §4.1 一致 | ☑ |
| `changed_pids` 签名 | 与 DESIGN §4.2 一致 | ☑ |
| `resolve` 签名 | 与 DESIGN §4.3 一致 | ☑ |
| `check_sessions` 签名 | 与 DESIGN §4.4 一致 | ☑ |
| `doc_digest` 签名（P-137） | 与 DESIGN §12.3 一致（`features, base=None, worktree=False`） | ☑ |
| `verify_digests` 签名（P-137） | 与 DESIGN §12.3 一致（`-> (int, list[str])`） | ☑ |

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
| I-9a 绑定存在（P-137，DESIGN §12.5） | #21 / #22 | ☑ |
| I-9b 内容一致（P-137） | #23 / #24 | ☑ |
| I-9c rebind 留因（P-137） | #25 / #26 | ☑ |
| I-9d 历史不重验（P-137） | #27（P-136 无 digest 仍 pass） | ☑ |
| I-9e 失败不静默（P-137） | #22 + 读取失败返回 1/2 | ☑ |
| I-10a 变异可感知（P-139，DESIGN §13.3） | #39~#42（四类变异体各使判定翻转） | ☑ |
| I-10b 同判定面（P-139） | #38（hook 触发面含 runner + CI 同入口） | ☑ |
| I-10c 零行为变更（P-139） | 本批 diff 面 = 3 测试文件 + 1 配置行；生产脚本字节不变 | ☑ |
| I-11a 逐提交 = 单一变更集（P-140，DESIGN §14.3） | #43 / #45（真实历史 16 提交 + 合成 merge） | ☑ |
| I-11b 执行器随提交（P-140） | 对照实验：HEAD 版执行器复验 P-127 提交 ⇒ 红 | ☑ |
| I-11c 合并提交显式跳过（P-140） | #45（17 条中 1 skip、16 受判） | ☑ |
| I-11d evil 内容 fail-closed（P-144，DESIGN §14.7） | #50（两父皆无 ⇒ exit 1） | ☑ |
| I-11e 干净合并不判（P-144） | #51~#53（等于任一父 / 非合并 ⇒ exit 0，无并集假红） | ☑ |

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
| P≥137 缺/非法 `evidence_digest`（P-137） | #22 | exit 1 | ☑ |
| digest 键集 ≠ 四文档集（P-137） | #24 | exit 1 | ☑ |
| digest 哈希不等（验后改文档，P-137） | #23 | exit 1 | ☑ |
| rebind 无 `rebind_reason`（P-137） | #25 | exit 1 | ☑ |

## 6. 性能验收

| 性能指标 | 目标 | 实测 | 状态 |
|---|---|---|---|
| 单次 hook 墙钟（本仓全量，100 文档 + 160 session） | < 5 s | 1.24 s（2026-10-27 P-137 复测，含 digest 4 次 `git show`） | ☑ |
| 批次绑定集成测试总时长 | < 60 s | 43.4 s（28 例；全套 36 例 39.9 s，2026-10-27 复测） | ☑ |

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
| 文档一致性 | 13 | 13 | 0 | 0 |
| 功能 | 65 | 65 | 0 | 0 |
| 接口 | 6 | 6 | 0 | 0 |
| 不变式 | 21 | 21 | 0 | 0 |
| 错误处理 | 12 | 12 | 0 | 0 |
| 性能 | 2 | 2 | 0 | 0 |
| 兼容性 | 3 | 2 | 0 | 1 |
| ADD 审计 | 4 | 4 | 0 | 0 |
| **总计** | 126 | 125 | 0 | 1 |

> **统计口径（RULE-2）**：上表来自逐项核对，非事后汇总推算。

### 10.2 验收决定

- [ ] **验收通过**：所有 P1 项通过，无阻塞性问题
- [x] **有条件通过**：Linux 平台未在本机实测；其余 **125** 项全通过，无失败项
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
| U-10 C 内容 digest 绑定（P-137，§2.5 八项） | 实施者 | P-137 | ☑ |
| U-9 扩 CONSOLE compact 当前状态块（P-138） | 实施者 | P-138 | ☑ |
| P1-1 真实 runner 集成回归（P-139，§2.6 十四项） | 实施者 | P-139 | ☑ |
| CI 逐提交遍历（P-140，§2.7 四项） | 实施者 | P-140 | ☑ |
| CI 远端读数回填（P-141，§2.7 #47） | 实施者 | P-141 | ☑ |
| `push(main)` 合并面读数回填（P-142，§2.7 #48） | 实施者 | P-142 | ☑ |
| `push(main)` 补充读数（P-143，§2.7 #49） | 实施者 | P-143 | ☑ |
| evil merge 检测（P-144，§2.8 四项） | 实施者 | P-144 | ☑ |
| 阶段 1 远端读数（P-145，§2.8 #54） | 实施者 | P-145 | ☑ |
| 阶段 1 远端第 2 样本（P-146，§2.8 #55） | 实施者 | P-146 | ☑ |
| 阶段 1 远端第 3 样本（P-147，§2.8 #56） | 实施者 | P-147 | ☑ |
| 阶段 1 远端第 4 样本（P-148，§2.8 #57） | 实施者 | P-148 | ☑ |
| 阶段 1 远端第 5 样本（P-149，§2.8 #58） | 实施者 | P-149 | ☑ |
| PR 面阶段 1 命中订正（P-150，§2.8 #59） | 实施者 | P-150 | ☑ |
| P1-2 每步执行证据绑定（U-4） | 待设计批 | 未定 | 未开始 |
| Phase 2b `session_start` 开场事件 | 待裁决 | 未定 | 未开始 |
