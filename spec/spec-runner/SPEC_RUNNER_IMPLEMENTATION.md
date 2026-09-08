# 实施文档：Spec_Runner 薄壳 runner（P-009 方案 B）实施批 v1.0 (2026-08-27)

---
id: spec-runner-IMPLEMENTATION
type: design
version: 1.0
status: verified
date: 2026-08-27
depends: [spec-runner-DESIGN, spec-runner-RESEARCH]
upstream: null
---

> **Feature**: spec-runner（PROGRESS P-009 实施批——设计批 2026-08-26 收口后用户指令「继续」触发）
> **代码仓**: `F:\Spec_Runner`（独立仓库，commit **`4ea703d`**——双仓漂移防线锚，DESIGN §5.3）
> **实施日期**: 2026-08-27
> **对照设计**: [SPEC_RUNNER_DESIGN.md](./SPEC_RUNNER_DESIGN.md) v1.0（D1-D7 + §4 LOC 预算 + §6 五步清单）
> **P-019 归巢追记（2026-09-08，spec-runner-homing 实施批）**: 双仓漂移防线锚（commit `4ea703d`）**退役**——runner 已按 P-019 修订并入本仓 `tools/spec_runner/`（8 文件 hash 逐字节核对一致），代码归本仓统一版本化；外仓 `F:\Spec_Runner` 冻结存档（git 历史 5 commit 完整保留可回溯）。本表原指外仓路径的交付物（spec_runner.py/README/sessions/selftest 复验）已在新路径复测通过：selftest 21/21、`p019-homing-verify-1` gate 入流 replay OK、adapter dry-run 命令装配正确。

---

## 1. 交付物清单

| 交付物 | 状态 | 证据（E1 可重放） |
|--------|------|------------------|
| `F:\Spec_Runner\spec_runner.py` | ✅ v1.0.0，519 行（代码 428 + 注释/空行 91） | 仓 commit 4ea703d |
| `F:\Spec_Runner\README.md` | ✅ 命令面 + schema + 约束 | 同上 |
| `sessions/p009-first-run-001.jsonl` | ✅ 首个真实运行（本仓三 gate 入流） | 同上（3 事件，replay OK） |
| selftest | ✅ 21/21 passed | `python F:\Spec_Runner\spec_runner.py selftest` exit 0 |
| git 仓 | ✅ init + root-commit 4ea703d（4 文件，+593 行） | git log |

## 2. 模块 LOC 实测对照（DESIGN §4 预算）

| 模块 | 预算 | 实测（约） | 判定 |
|------|------|-----------|------|
| 事件流写入器（EventWriter + schema 校验） | ~100-150 | ~85 | ✅ 低于预算（紧凑） |
| gate 执行器 + gate_passed | ~80-120 | ~40 | ✅ |
| adapter 接口 + NativeHTTPAdapter | ~120-180 | ~65 | ✅（重试/门控含） |
| run 命令（L2/L6/D5） | ~60-100 | ~75 | ✅ |
| status/replay/fork 派生件 | ~60-90 | ~85 | ✅ |
| git 持久化封装 | ~40-60 | ~15 | ✅ |
| CLI 入口 + 命令分发 | ~60-100 | ~70 | ✅ |
| selftest（21 项 + mock server） | ~150-250 | ~170 | ✅ |
| **合计** | **~550-850** | **519** | ✅ 落入区间（低于上界 39%） |

**LG H2 实施级收口**：设计级拆解 ~550-850（RESEARCH B1）+ 实施级实测 519——估算成立且偏保守（薄壳哲学兑现：需要的能力全部落地，无 LOC 膨胀）。

## 3. 七步设计决策落地验证（D1-D7 逐项）

| 决策 | 落地验证 | E1 |
|------|---------|-----|
| D1 双仓结构 | 代码在 F:\Spec_Runner；spec 四件套在本仓；runner 零引用本仓路径（grep `Spec_Workflow` 仅 README 文档指针）；本仓校验器零引用 runner | 仓内容 + selftest F14（SR_SESSIONS_DIR 注入隔离） |
| D2 L1-L7 | L1 唯一写路径 `open("a")`（无 rewrite 函数）/ L2 llm_request 记装配后 messages / L3 ensure_ascii=False / L4 fork=复制+replay=校验+resume=追加 / L5 source 五档 / L6 F11（同 sid 无 --resume exit 2）/ L7 写入器为内置类无插件点 | selftest F11/F15/F16 |
| D3 gate 语义 | subprocess 执行 + exit 透传（F1/F2）+ verdict 机械映射 + `--require-gate` 前置检查（F17 exit 3） | selftest F1/F2/F17 |
| D4 adapter 开放结构 | LLMAdapter 协议 + NativeHTTPAdapter 唯一实现；DshSDKAdapter 候选位（无代码，实测后增） | 代码结构 |
| D5 端点门控 | endpoint_ready() GET /v1/models 3s 超时；不可达 → endpoint_unreachable 事件 + exit 1 | selftest F12/F13 |
| D6 零依赖 | import 清单：argparse/json/os/re/subprocess/sys/time/urllib/datetime/pathlib + selftest 专属 http.server/threading/tempfile/shutil——全部 stdlib | 代码头部 import 区 |
| D7 五命令面 | run/gate/status/replay/fork 全落地；search = grep（README 声明，零代码） | §4 首个真实运行 |

## 4. selftest 实录（21 项，计数机械自增——R7 同构）

首跑 20/21（F14/F15 失败 + F18 断言格式），修正两轮后全绿：

| 轮次 | 失败项 | 根因 | 处置 |
|------|--------|------|------|
| 第 1 轮 | F14/F15/F16（连锁） | **语义发现**：`--require-gate` 是同流查询（D3 原文「检查前置 gate 的通过事件存在」隐含同 session 流），测试错误地在异流 gate 后跨流引用 | selftest 改为 gate 建流 → `run --resume` 同流续写（这也是 DESIGN §6 第 4 步的真实用法形态：gate 序列独立建流，run 以 resume 续接） |
| 第 2 轮 | F18 | 断言字符串格式与 status 输出不匹配（`always-pass: pass` vs 实际 `gate[always-pass]: pass`） | 断言对齐输出格式 |

**教训登记**：两处失败均为测试侧问题（非实现缺陷）；F14 语义发现属实施期澄清——DESIGN D3 的 require-gate 同流语义在 selftest 中被首次显式行使，无 DESIGN 修订需求（原文语义一致，仅测试误解）。

## 5. 首个真实运行实录（DESIGN §6 第 4 步——自身落地即 E1）

```
session: p009-first-run-001（3 事件，seq 1-3）
  gate[dc-validator]:  pass (seq 1, exit 0)  # python scripts/dc_validator.py --check-all
  gate[m7-stats]:      pass (seq 2, exit 0)  # python scripts/m7_stats.py
  gate[repo-stats]:    pass (seq 3, exit 0)  # python scripts/repo_stats.py
replay: 3 rows OK (seq monotonic, schema parseable)
fork: p009-first-run-001-fork-demo <- p009-first-run-001 (seq 1..1, 1 rows)
```

- gate 以 `--cwd F:\Spec_Workflow` 注入工作目录（runner 不内置本仓路径，D1 兑现）
- 事件流文件 = 本实施批的 E1 级证据（M7 来源列指针形态：`Spec_Runner:sessions/p009-first-run-001.jsonl#seq1-3`）
- fork demo 文件保留（L4 活证据）

## 6. 解锁项与假设状态更新

| 项 | 状态 | 证据 |
|----|------|------|
| LG H2（LOC 估算） | **完全解除**（设计级 ~550-850 + 实施级 519 双吻合） | §2 对照表 |
| LG H3（端点模型池） | 维持未解除（三端点不可达，2026-08-26 复核） | RESEARCH §2.2；run 异构审查臂待端点就绪 |
| dsh H2（SDK 实测） | 维持阻塞（工作站 A + 端点双前置） | RESEARCH §2.3；DshSDKAdapter 候选位就绪 |
| LangGraph (a)/(b)/(c) | 未现（骨架刚落地，观察期开始） | DESIGN §8 复查机制挂 PROGRESS P-009 追记 |

## 7. 与本仓的集成状态

- spec 四件套：RESEARCH v1.0 + DESIGN v1.0（设计批）+ 本 IMPL v1.0 + CHECKLIST v1.0（实施批）——齐
- PROGRESS P-009：设计批 in-progress → 实施批 done（本轮）
- E1 回流：事件流路径已具备，M7 样本行「来源」列可指针化引用（首个消费者 = 本文档 §5）

## 8. 实施偏差登记（对照 DESIGN）

- **无实质偏差**。require-gate 同流语义为实施期澄清（§4），不构成 DESIGN 修订
- LOC 全模块低于预算上界（§2），无需超限裁决

---

**Review 签字**: _________ 日期: _________（自查完成；独立 pass 按流程待用户触发——P-010/P-014/P-016 收口先例）
