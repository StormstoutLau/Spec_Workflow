# 审查验收 Checklist：Spec_Runner 薄壳 runner 实施批 v1.0 (2026-08-27)

---
id: spec-runner-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-08-27
depends: [spec-runner-IMPLEMENTATION, spec-runner-DESIGN]
upstream: null
---

> **Feature**: spec-runner（PROGRESS P-009 实施批）
> **创建日期**: 2026-08-27
> **状态**: 有条件通过（自查全绿 + 机械验证全绿；独立 pass 待触发——P-010/P-014/P-016 收口先例）
> **基于设计**: [SPEC_RUNNER_DESIGN.md](./SPEC_RUNNER_DESIGN.md) v1.0
> **基于实施**: [SPEC_RUNNER_IMPLEMENTATION.md](./SPEC_RUNNER_IMPLEMENTATION.md) v1.0（代码仓锚 = Spec_Runner commit `4ea703d`）
> **审查状态**: `自查（单视角）`（RULE-4）

---

## 1. 设计一致性验收（D1-D7）

| 检查项 | 状态 | 说明 |
|--------|------|------|
| D1 双仓结构（代码独立仓 + spec 留本仓 + 双向零依赖） | ☒ 通过 | runner 零内置本仓路径（gate --cwd 注入）；本仓校验器零引用 runner |
| D2 L1-L7 逐条落地 | ☒ 通过 | IMPL §3 逐项 E1 表（L1 唯一写路径 / L6 强制新 sid / L7 无插件点） |
| D3 gate 语义（exit 透传 + 前置检查 + 无 LLM 判断） | ☒ 通过 | selftest F1/F2（透传）+ F17（前置 exit 3）+ verdict 纯机械映射 |
| D4 adapter 开放结构 | ☒ 通过 | LLMAdapter 协议 + NativeHTTPAdapter；DshSDKAdapter 候选位 |
| D5 端点配置化 + 就绪门控 | ☒ 通过 | selftest F12/F13（不可达 exit 1 + 事件入流） |
| D6 零依赖 stdlib only | ☒ 通过 | import 清单全 stdlib（IMPL §3） |
| D7 五命令面 + schema 十字段 | ☒ 通过 | run/gate/status/replay/fork 全实测（§4/§5） |

## 2. 机械验证（E1 通道）

| 通道 | 结果 |
|------|------|
| selftest（21 项，计数机械自增） | ☒ 21/21 passed（exit 0） |
| 首个真实运行（本仓三 gate 入流） | ☒ 3 gate 全 pass + replay OK + fork OK |
| dc_validator --check-all（本仓，spec 新文件含 IMPL/CHECKLIST） | ☒ 通过 |
| m7_stats / repo_stats（本仓） | ☒ 通过（本 CHECKLIST 收口批实测） |
| pre-commit run --all-files（本仓三 hook） | ☒ Passed |

## 3. LOC 预算验收（DESIGN §4）

| 项 | 结果 |
|----|------|
| 七模块全部 ≤ 预算 ×1.2 | ☒ 全模块低于预算上界（合计 519 vs 预算 ~550-850） |
| 超限登记需求 | ☒ 无（无模块超限） |
| LG H2 实施级收口 | ☒ 完全解除（设计级 + 实施级双吻合） |

## 4. selftest 质量验收

| 检查项 | 状态 | 说明 |
|--------|------|------|
| mock server 用 stdlib http.server（无第三方） | ☒ | _mock_server + threading |
| 计数自增机械计数（R7 同构，样本⑨ 教训） | ☒ | `passed = sum(results)` / `total = len(results)`——无硬编码 |
| 失败可见性（FAIL 行 + stderr detail） | ☒ | check() 输出 + exit 1 |
| 修正实录留档 | ☒ | IMPL §4 两轮修正（require-gate 同流语义 + F18 断言格式） |

## 5. 集成与视图验收

| 验收项 | 状态 | 证据 |
|--------|------|------|
| 双仓漂移防线（IMPL 锚 Spec_Runner commit hash） | ☒ | IMPL 头部 + §1：`4ea703d` |
| E1 回流指针形态（M7 来源列可引用事件流） | ☒ | IMPL §5：`Spec_Runner:sessions/p009-first-run-001.jsonl#seq1-3` |
| PROGRESS P-009 → done | ☒ | 本批同步 |
| CODE_WIKI 视图同步（四件套齐 + 版本头） | ☒ | 本批同步 |
| 解锁项状态登记（LG H2 解除 / LG H3 维持 / dsh H2 维持） | ☒ | IMPL §6 |

## 6. 验收统计与决定

- **通过项**: 22/22（自查 + 机械）
- **发现**: 实施期两处 selftest 修正（测试侧非实现缺陷，IMPL §4 留档）；无 DESIGN 偏差；无 M7 样本（测试代码修正属常规迭代，非审查轮发现——selftest 首跑失败-修正-全绿是 TDD 形态非形态 II 载体）
- **决定**: **有条件通过**——独立 pass（RULE-1 时序独立，真异基座优先）待用户触发；触发后若有修订按双仓各自版本化（runner 仓 semver + spec 仓 front-matter）

## 7. ADD 审计（Phase 0 质量门）

| 维度 | 档位 | 说明 |
|------|------|------|
| 可测试约束 | A | 21 项 selftest 全 E1 可重放（exit code 断言） |
| 模块映射 | A | D1-D7 ↔ IMPL §3 逐项 E1 表 |
| 接口契约 | A | 事件行十字段 schema 写入端强制（F6/F7 拒绝测试） |
| 修正项追溯 | A | 两轮 selftest 修正实录（IMPL §4） |
| 跨模块契约 | A | 双仓漂移防线（commit hash 锚）+ E1 指针形态 |

**Iron Law 四类盲区自查**: ① 未验证即声明——IMPL 所有断言附 selftest/事件流/命令输出 E1 ✅ ② 边界条件——端点不可达（F12）/ 坏 seq（F19）/ 同 sid 复用（F11）/ require-gate 未过（F17）四边界均有测试 ✅ ③ 自我验证——selftest 即 runner 对自身的机械验证 + 本仓四通道独立看护 ✅ ④ 环境维度——零依赖使环境面最小（Python ≥3.8 唯一前提，主控站 3.11 实测）✅

---

**审查签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待触发）
