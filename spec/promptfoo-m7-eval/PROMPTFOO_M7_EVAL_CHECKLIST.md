# 审查验收 Checklist：Promptfoo M7 对比臂声明式评测

---
id: promptfoo-m7-eval-CHECKLIST
type: design
version: 1.1
status: accepting
date: 2026-08-23
depends: [promptfoo-m7-eval-IMPLEMENTATION, promptfoo-m7-eval-DESIGN]
upstream: null
---

> **Feature**: promptfoo-m7-eval（PROGRESS P-010，优先级 3）
> **创建日期**: 2026-08-23
> **状态**: 有条件通过（v1.1 Review 轮后：selftest 13/13 + 双臂门控 + DESIGN §7 全四行错误处理活靶实测通过 + Step 10 收束批四通道终验全绿；缺端点实评，方案 Z 门控；独立 pass 待触发——同 P-014 收口先例）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [IMPLEMENTATION.md](./PROMPTFOO_M7_EVAL_IMPLEMENTATION.md) v1.1
> **基于设计**: [DESIGN.md](./PROMPTFOO_M7_EVAL_DESIGN.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——独立 pass 待 Step 10 / 用户触发
> **v1.1 变更（2026-08-23，Review 轮）**: Review 捕获 P1×2（RESEARCH A/H 标记形态）+ P2×3（config 缺异基座臂 / 未安装兜底未实施 / 顶层兜底未实施）+ P3×3（死代码/旗标命名），全部修复并活靶复验；验收统计与 §8.2 审计发现同步更新

---

## 1. 文档一致性验收（Step 8）

### 1.1 RESEARCH.md ↔ DESIGN.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN.md 的设计决策可追溯到 RESEARCH.md | ☒ 通过 | §2.1 映射表逐条引 RESEARCH A1/A3/A4/A5/B1/H1 |
| RESEARCH.md 的关键发现被 DESIGN.md 使用 | ☒ 通过 | 触发条件/声明式矩阵/env 绕过/机械解析/方案 Z 全被采用 |
| 无文档间矛盾 | ☒ 通过 | 方案 Z 范围在 RESEARCH §4.2 与 DESIGN §5.1 一致 |

### 1.2 DESIGN.md ↔ IMPLEMENTATION.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN.md 的模块在 IMPLEMENTATION.md 中有对应实施 | ☒ 通过（v1.1） | PM1-PM5 ↔ §3.1 模块实施；v1.0 原「通过」断言过宽——DESIGN §4.2 双 provider 臂当时只落 1 个，Review 轮补齐后方真对应 |
| IMPLEMENTATION.md 的接口签名与 DESIGN.md 一致 | ☒ 通过 | run/record/selftest 三子命令 + EvalRecord/EvalSummary dataclass |
| DESIGN.md 的不变式在 IMPLEMENTATION.md 中有实施 | ☒ 通过 | I-1 只读 / I-4 机械 / I-6 门控均代码落地 |
| 无设计未覆盖的实施 | ☒ 通过 | record CLI 为 §3.1 标注的 Step 9 补全项，已闭合 |

### 1.3 IMPLEMENTATION.md ↔ CHECKLIST.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| IMPLEMENTATION.md 的功能点在本 checklist 有验收项 | ☒ 通过 | §2 逐条覆盖 5 fixture + 门控 + record |
| 本 checklist 的验收项可追溯到 IMPLEMENTATION.md | ☒ 通过 | 证据列引用 §9 实测 |

### 1.4 术语一致性

| 术语 | RESEARCH.md | DESIGN.md | IMPLEMENTATION.md | 一致 |
|------|------------|-----------|-------------------|------|
| 方案 Z | 基础设施先行 | 同 | 同（门控不假造） | ☒ |
| 同基座/异基座 | base/cross | base-model/cross-model | 同 | ☒ |
| 端点就绪门控 | LM Studio 不可达 | I-6 | endpoint_reachable | ☒ |

## 2. 功能验收

### 2.1 PM1 CLI 入口

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 三子命令分发 | `run`/`record`/`selftest` 各调 | 各返回正确退出码 | ☒ | §2.2-2.6 |
| record CLI 出口（Step 9 补全，v1.1 旗标对齐 DESIGN 为 --results） | `record --results` 合法/缺文件/目录 | 合法打印草案 exit 0；缺文件 P1+exit 2；目录触发顶层兜底 P2+exit 2 | ☒ | 实测 exit 0 / 2 / 2 |

### 2.2 PM3 结果解析

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 合法 results.json 解析 | selftest F1 | total_tests/stats/逐字段精确 | ☒ | 12/12 PASS |
| 缺字段零值兜底 | selftest F2 | 不崩 | ☒ | 12/12 PASS |

### 2.3 PM4 登记草案

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| M7 样本行草案生成 | selftest F5 + record 实测 | 列序对齐 + provider/状态标注 | ☒ | 实测 base-model（PASS）/cross-model（FAIL） |

### 2.4 双臂端点门控（I-6，v1.1 补齐第二臂）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 任一臂端点不可达即阻断 | `run`（默认双端点均不可达） | `[P1] 端点不可达` + exit 1，不调 promptfoo | ☒ | 实测 P1 提示 + EXIT=1 |

### 2.5 promptfoo 未安装兜底（v1.1 新增）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| FileNotFoundError 被捕获 | selftest F6 活靶（不存在命令） | 安装提示 + 返回 None 不崩栈 | ☒ | selftest 输出首行 `[P1] 未找到 promptfoo CLI` |

### 2.6 端点解析

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| host:port / 无端口默认 | selftest F4 | 解析正确 | ☒ | 12/12 PASS |

## 3. 接口验收

### 3.1 EvalRecord / EvalSummary

| 验收项 | 通过条件 | 状态 |
|--------|---------|------|
| 字段与 DESIGN §6 一致 | frozen dataclass 六/四字段 | ☒ |
| 解析正常返回记录 | F1 | ☒ |
| 缺失字段兜底 | F2 | ☒ |

### 3.2 CLI 子命令

| 验收项 | 通过条件 | 状态 |
|--------|---------|------|
| run --config/--endpoint/--endpoint2/--model/--model2/--api-key/--output | 参数可解析 | ☒ |
| record --results/--date（v1.1 旗标对齐 DESIGN §3.1） | 参数可解析 | ☒ |
| selftest 无参 | 返回 0 | ☒ |

## 4. 不变式验收

| 不变式（来自 DESIGN.md §8） | 验证方法 | 状态 |
|---------------------------|---------|------|
| I-1 默认只读 | 代码审查：无对 M7/config 的写操作，门控为只读 TCP | ☒ |
| I-2 确定性 | record 解析无时间戳/随机污染 | ☒ |
| I-3 零新登记规则 | 只生成草案，hits 块归 m7_stats | ☒ |
| I-4 登记 = 机械解析 | parse_results 直接取 JSON 字段，无 LLM | ☒ |
| I-5 异构于生成端 | stdlib 纯机械 | ☒ |
| I-6 运行触发门控 | 端点不可达不调 promptfoo（实测） | ☒ |

## 5. 错误处理验收

| 错误场景（来自 DESIGN.md §7，全四行） | 触发方式 | 预期行为 | 状态 |
|------------------------------|---------|---------|------|
| 端点不可达 | `run`（双臂任一不可达） | P1 提示 + exit 1 | ☒ |
| results.json 缺失/非法 | `record --results` 缺文件 | P1 + exit 2 | ☒ |
| promptfoo 未安装 | selftest F6 活靶 | 安装提示 + exit 1（经 call_promptfoo） | ☒ |
| 未知异常 | `record --results .promptfoo`（目录路径） | 顶层兜底 `[P2] 未预期异常` + exit 2 | ☒ |

## 6. 性能验收

| 性能指标 | 目标 | 实测 | 状态 |
|---------|------|------|------|
| selftest 耗时 | < 5s | 即时 | ☒ |
| 端点预检单次 | <= 1.5s timeout | TCP 即断 | ☒ |

## 7. 兼容性验收

| 环境 | 版本 | 状态 | 说明 |
|------|------|------|------|
| Python | 3.12 | ☒ | 主控站实测 |
| OS | Windows | ☒ | fs.run 实测 |
| promptfoo | 0.122.0 | ☒ | RESEARCH A3 实测（--version） |
| 零第三方 Python 依赖 | — | ☒ | stdlib only |

## 8. ADD 审计（Step 10）

### 8.1 Spec 质量门（Phase 0）

| 维度 | 得分（0-1） | 说明 |
|------|-----------|------|
| 可测试约束 | 1.0 | selftest 12 断言全覆盖；门控可实测 |
| 模块映射 | 1.0 | PM1-PM5 清晰映射 |
| 接口契约 | 1.0 | dataclass + CLI 参数契约 |
| 修正项 | 0.8 | H1/H2 如实携带，占位待确认 |
| 跨模块契约 | 1.0 | 与 m7_stats 对接明确（I-3） |
| **总分** | 4.8/5 | **档位**: A |

### 8.2 ADD 审计发现

| 严重性 | 发现 | 证据 | 修复建议 |
|--------|------|------|---------|
| P1×2 | RESEARCH 附录 A/H 标记形态违规（粗体 ≠ 行首【A】/`[H1]` 契约，M4 重数 0≠声明）——上轮验收只单文件验了 CHECKLIST | dc_validator 全量首跑 | **已修复**（行首【A】×5 / `[H1]`×2），55 文件复验 0 违规；已裁决入 M7 样本㉔（形态 II=0，同⑮ 处置，2026-08-23 用户确认） |
| P2 | record CLI 未接入 main（Step 9 缺口） | `record --help` invalid choice | **已修复**：补 p_record 子命令 + 实测 exit 0/2 |
| P2 | config 缺异基座臂 provider（DESIGN §4.2 双臂只落 1 个） | config providers 数组 vs DESIGN §4.2 表 | **已修复**：第二 provider + run 双臂注入与门控（DR-C） |
| P2 | DESIGN §7「promptfoo 未安装」未实施（FileNotFoundError 裸抛） | 代码无 except FileNotFoundError | **已修复**：call_promptfoo 兜底 + F6 活靶 |
| P2 | DESIGN §7「未知异常→exit 2」未实施（main 无顶层捕获） | 代码无顶层 try | **已修复**：__main__ try/except + 目录活靶实测 exit 2 |
| P3×3 | env_prefix 死参数 / tempfile 未用 import / record 旗标 --input ≠ DESIGN --results | 逐行代码审查 | **已修复**：清除/改名 |
| P3 | results.json schema 跨版本未回归 | RESEARCH H2 | record 已标注 promptfooVersion 占位；升级时回归 |

### 8.3 ADD Iron Law 检查

- [x] 测试通过的 4 类盲区已检查：
  - 断言恒真式 → selftest expect 为固定值比对，非恒真
  - 单文件检查盲区 → 门控活靶实测（run P1）
  - 设计文档独有约束无测试 → I-6 门控有实测
  - 修正阻断性项无测试 → record CLI 已补 + 实测

## 9. 文档完整性

| 文档 | 存在 | 与实现一致 |
|------|------|----------|
| RESEARCH.md | ☒ | ☒ |
| DESIGN.md | ☒ | ☒ |
| IMPLEMENTATION.md | ☒ | ☒ |
| CHECKLIST.md（本文件） | ☒ | ☒ |
| promptfooconfig.yaml | ☒ | ☒（占位结构） |
| 开发日志 | ☐ | ☐（Step 11 补） |

## 10. 验收结论

### 10.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|------|------|------|------|------|
| 文档一致性 | 4 | 4 | 0 | 0 |
| 功能 | 8 | 8 | 0 | 0 |
| 接口 | 6 | 6 | 0 | 0 |
| 不变式 | 6 | 6 | 0 | 0 |
| 错误处理 | 4 | 4 | 0 | 0 |
| 性能 | 2 | 2 | 0 | 0 |
| 兼容性 | 4 | 4 | 0 | 0 |
| ADD 审计 | 1 | 1 | 0 | 0 |
| **总计** | 35 | 35 | 0 | 0 |

### 10.2 验收决定

- [ ] **验收通过**：所有 P1 项通过，无阻塞性问题
- [x] **有条件通过**：基础设施验收通过（35/35，Review 轮 P1×2/P2×3/P3×3 修复并活靶复验）；「首轮评测结果入 M7 + LG H5 成本/延迟实测」两项以**端点就绪触发**为前置（方案 Z 门控，缺运行数据，不假造）；独立 pass（RULE-1/RULE-5）待触发
- [ ] **验收失败**：<原因>

### 10.3 签字

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | 自查（单视角）+ Review 轮 + 收束批（2026-08-23） | 2026-08-23 |
| 审查者 | 独立 pass 待触发 | — |

## 11. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|------|--------|------|------|
| 视图层同步（CODE_WIKI §2.1/§4/§9/§10 + PROGRESS P-010 + dev-log）→ repo_stats 全绿 | 实施者 | 收束批 | 已完成（2026-08-23 收束批：CODE_WIKI v1.8 + PROGRESS P-010 done + DEV-LOG-007，repo_stats 0 违规） |
| M7 样本㉔ 登记（Review 轮 P1×2+P2×3+P3×3 拦截实录） | 用户裁决 | 收束批 | 已完成（形态 II=0 同⑮ 处置入账，samples 23→24，form2_total 62 不变） |
| 首轮评测（端点就绪时）→ M7 登记 + H5 实测 | 触发驱动 | 端点恢复 | 待办 |
| IMPLEMENTATION status in-review → verified | 实施者 | 独立 pass 批 | 待办（遵循 P-014 收口先例：收口时保持 in-review，verified 待独立 pass——原「视图层同步后」计划与先例冲突，本轮修正） |
| 独立 pass（RULE-1/RULE-5） | 异步独立 | Step 10 | 待办 |