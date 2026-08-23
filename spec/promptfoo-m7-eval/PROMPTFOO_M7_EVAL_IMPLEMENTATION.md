# 实施文档：Promptfoo M7 对比臂声明式评测

---
id: promptfoo-m7-eval-IMPLEMENTATION
type: design
version: 1.1
status: in-review
date: 2026-08-23
depends: [promptfoo-m7-eval-DESIGN, promptfoo-m7-eval-RESEARCH]
upstream: null
---

> **Feature**: promptfoo-m7-eval（PROGRESS P-010，优先级 3）
> **创建日期**: 2026-08-23
> **状态**: in-review（Step 5-6 + 9 实施完成，selftest 13/13 + 双臂门控 + F6/顶层兜底活靶实测；Review 轮 P1×2/P2×3/P3×3 已修复；Step 10 收束批终验全绿 + 样本㉔ 已入账——verified 待独立 pass，同 P-014 收口先例）
> **Spec 步骤**: Step 5-6, 9-10
> **基于设计**: [PROMPTFOO_M7_EVAL_DESIGN.md](./PROMPTFOO_M7_EVAL_DESIGN.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验
> **v1.1 变更（2026-08-23，Review 轮）**: ① record CLI 接入 main（Step 9 补全）；② config 补异基座臂 provider + run 双端点注入与门控（DR-C）；③ call_promptfoo 未安装兜底 + 顶层 try/except（DESIGN §7 全四行落地）；④ record 旗标对齐 DESIGN（--results）；⑤ 死代码清除（env_prefix/tempfile）；⑥ selftest 12→13 断言（F6 活靶）；⑦ RESEARCH 附录 A/H 标记形态修复（P1×2，见 §10.3）

---

## 1. 实施概述

交付三件（DESIGN §1）：① `spec/promptfoo-m7-eval/promptfooconfig.yaml`（声明式评测矩阵模板）；② `scripts/pf_m7_eval.py`（run/record/selftest 三子命令，零第三方依赖）；③ 端点就绪门控（方案 Z）。实际跨基座评测由端点就绪触发，不假造评测数据（I-6）。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|------|------|------|---------|
| 语言 | Python（stdlib only） | 3.12（主控站实测） | ✅ |
| 评测引擎 | promptfoo CLI（子进程调用，零 npm 依赖进 Python） | 0.122.0 | ✅ |
| 解析 | json（脚本未用 re——v1.1 修正原表误记） | stdlib | ✅ |
| 依赖 | **零第三方依赖**（Python 侧） | — | ✅ |

### 2.2 文件结构

```
scripts/pf_m7_eval.py                        # 新增（PM1-PM5 单文件）
spec/promptfoo-m7-eval/promptfooconfig.yaml  # 新增（promptfoo 评测矩阵模板）
spec/promptfoo-m7-eval/PROMPTFOO_M7_EVAL_*   # 调研/设计/实施文档
```

### 2.3 运行封装要点（PM2）

- **env 三件套重定向**（沙箱绕过，RESEARCH A4）: run 时注入 `PROMPTFOO_CONFIG_DIR` / `PROMPTFOO_CACHE_PATH` / `PROMPTFOO_LOG_DIR` 到工作区 `.promptfoo/`
- **双臂端点门控**（I-6，v1.1）: `endpoint_reachable()` 只读 TCP 预检 **两臂端点**（--endpoint/--endpoint2），任一不可达 → P1 提示 + exit 1，**不调 promptfoo**（杜绝虚假评测）
- **双臂 provider 变量注入**（DESIGN §4.2，v1.1 补齐）: config 中 `${endpoint}`/`${model}` + `${endpoint2}`/`${model2}`（base-model/cross-model 双臂）+ 共用 `${apiKey}` 由 run 时 env 注入，不硬编码 IP
- **promptfoo 未安装兜底**: `call_promptfoo()` 捕获 FileNotFoundError → 安装提示 + exit 1（DESIGN §7）；顶层 try/except 兜未知异常 → exit 2
- promptfoo 调用用 `--no-share` + `--output results.json`，捕获 stdout/stderr

### 2.4 结果解析（PM3）

`parse_results()` 机械解析 results.json `results.stats`（successes/failures/errors + total_tests）与 `results.results[]`（provider.label / success / gradingResult.pass / latencyMs / cost / testCase.metadata）。字段直接取 JSON，**不经 LLM 转述**（I-4）。缺失字段零值兜底不崩（selftest F2）。登记脚本标注 promptfooVersion（H2，metadata 透传可加）。

### 2.5 M7 登记草案（PM4）

`to_m7_sample_row()` 生成 M7 §1 样本行草案，字段对齐既有列（编号/日期/载体/审查配置/发现/形态II复发/来源）。「审查配置」= provider.label + PASS/FAIL 状态；「发现」留人工归并（DESIGN §4.4——计数的 P 分级语义不经机械推断，防假精确）。样本行追加后走既有 `m7_stats.py --write` 通道（不新增登记声明块，I-3）。

## 3. 模块实施

### 3.1 PM1 CLI 入口

子命令 `run` / `record` / `selftest`。退出码：0 通过 / 1 门控或结算失败 / 2 工具或输入错误。`run` 双臂旗标（--endpoint/--endpoint2/--model/--model2）；`record` 出口为 `--results`/`--date`（v1.1 对齐 DESIGN §3.1 命名），实测将 results.json → M7 样本行草案打印（缺文件 P1+exit 2，空记录 P2+exit 1，目录当路径触发顶层兜底 P2+exit 2）。

### 3.2 selftest fixture（6 fixture，13 断言，expect 自增机械计数）

| # | 场景 | 断言 |
|---|------|------|
| F1 | 合法 results.json 子集解析 | total_tests=2 / stats 精确 / provider label / 逐字段 pass+latency / 第二记录 |
| F2 | 缺字段兜底 | 零值不崩 |
| F3 | 端点不可达预检 | 只读 False（不抛） |
| F4 | 端点解析 | host:port / 无端口默认 80 |
| F5 | M7 登记草案 | provider+状态 / 列序 |
| F6 | promptfoo 未安装兜底（v1.1 活靶） | 不存在命令 → FileNotFoundError 被捕获 → None（selftest 输出首行 `[P1] 未找到 promptfoo CLI` 即活靶证据） |

## 4. 与既有工具的运行隔离

- `pf_m7_eval.py` 不写 M7（只生成草案供人工追加，I-1）；M7 hits 块生成/校验仍归 `m7_stats.py`（P-011）
- promptfoo 存储经 env 重定向到 `.promptfoo/`，不污染仓库 tracked 文件（该目录已 gitignore 预置，见 .gitignore）
- 不入侵 dc_validator / repo_stats / m7_stats 三既有校验器

## 5-8. （保留——对应 DESIGN §§5-8 无独立伪实现）

## 9. 测试与验证

- selftest: `py -3 scripts\pf_m7_eval.py selftest` → 13/13 PASS（F6 活靶真实触发 FileNotFoundError 路径）
- 双臂端点门控实测: `run`（默认 --endpoint 192.168.1.11:1234 / --endpoint2 192.168.1.15:1234）→ `[P1] 端点不可达` + exit 1，未调 promptfoo
- record 出口实测: 合法 results.json → 草案打印 exit 0；缺文件 → P1 + exit 2；目录当路径 → 顶层兜底 `[P2] 未预期异常: PermissionError` + exit 2
- promptfoo 存储重定向实测: env 三件套注入后 `promptfoo --version` 正常（RESEARCH A2/A4）

## 10. 关键决策记录

### 10.1 派生需求（DR）
- **DR-A（provider 变量注入）**: config 不硬编码 IP，${endpoint}/${model}/${apiKey} 由 run 注入——源：DESIGN §4.2 占位策略 + 可移植性（I-1）
- **DR-B（门控不假造）**: 端点不可达 → P1 提示 + exit 1，不调 promptfoo——源：DESIGN I-6 + RESEARCH A5（方案 Z 哲学）
- **DR-C（双臂 env 注入，v1.1）**: `${endpoint2}`/`${model2}` 注入 + 双臂 TCP 门控（任一臂不可达即阻断）——源：DESIGN §4.2 双 provider 矩阵（Review 轮发现原实施只落单臂后补齐）

### 10.2 LOC 回填（P-008 P3③ 教训：DESIGN 预估必须实施核对）
- 实施实际 LOC = **275**（`scripts/pf_m7_eval.py` 含注释/空行，与 m7_stats 同口径；v1.1 = record CLI + 双臂 + 兜底）
- selftest = **13 断言 / 6 fixture**

### 10.3 实施期拦截实录（v1.1 Review 轮，2026-08-23）

Review 手段 = dc_validator 全量首跑（55 文件）+ repo_stats 首跑 + 逐行代码审查。捕获与处置：

| 严重性 | 发现 | 处置 |
|--------|------|------|
| P1×2 | RESEARCH 附录 A/H 标记形态违规：`**A1**` 粗体 ≠ 行首【A】契约、`**H1**` ≠ `[H1]` 方括号契约（dc_validator M4 重数 0 ≠ 声明 5/2）——上轮验收只单文件验了 CHECKLIST，新增 4 文件未逐个过契约致逃逸 | 已修复为行首【A】/`[H1]` 形态，复验 55 文件 0 违规；已裁决入 M7 样本㉔（形态 II=0 同⑮ 处置，2026-08-23 用户确认——㉓ 已被 P-014 独立 pass 批占用，编号顺延） |
| P2 | config 缺异基座臂 provider：DESIGN §4.2 声明双 provider（base-model/cross-model），config 只落 1 个；run 也只注入单端点——「同一报告 × 双基座」矩阵结构性缺失 | 已补第二 provider（${endpoint2}/${model2}）+ run 双臂注入与门控（DR-C） |
| P2 | DESIGN §7「promptfoo 未安装→提示安装命令 exit 1」未实施：subprocess FileNotFoundError 裸抛崩栈 | 已补 call_promptfoo 兜底 + F6 活靶（selftest 输出首行即证据） |
| P2 | DESIGN §7「未知异常→顶层 try/except exit 2」未实施：main() 无顶层捕获 | 已补 __main__ 顶层 try/except + 活靶实测（目录当 --results → PermissionError → exit 2） |
| P3×3 | env_prefix 死参数（默认值还是硬编码路径）/ tempfile 未用 import / record 旗标 --input ≠ DESIGN §3.1 的 --results | 均已清除/改名 |

## 11. 对验收的输入

验收掌 KEY（DESIGN §10.2 风险 + P-010 验收标准）:
1. selftest 全绿 + 端到端 record 解析（F1-F5 fixture 覆盖）
2. 端点门控行为正确（不可达阻断，不假造）
3. 方案 Z 范围如实——「首轮评测入 M7」验收项标记为**端点就绪触发**（缺端点数据，不假造）
4. 视图层同步（CODE_WIKI 工具清单 + PROGRESS P-010 状态）

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）