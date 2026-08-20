# 审查验收 Checklist：precommit-dc-validator

---
id: precommit-dc-validator-CHECKLIST
type: design
version: 1.1
status: accepted
date: 2026-08-19
depends: [precommit-dc-validator-IMPLEMENTATION, precommit-dc-validator-DESIGN]
upstream: null
---

> **Feature**: precommit-dc-validator（PROGRESS P-007）
> **创建日期**: 2026-08-19
> **状态**: 已验收（2026-08-20 独立 pass 通过——真异基座 DeepSeek V4 Pro，RULE-1 时序独立 + RULE-5 模型异质性双满足；v1.0"有条件通过"的条件已满足，升 accepted）
> **v1.1 变更（2026-08-20）**: 独立 pass 修正——§8.1 跨模块契约行映射断言修正（M4 不共享解析器，M7 样本⑬）；§8.2 补录独立轮 3 P3 发现；§10.2/§10.3/§11 落地验收决定与签字
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [IMPLEMENTATION.md](./IMPLEMENTATION.md) v1.2（独立 pass 审查对象为 v1.1；v1.2 为修正版）
> **基于设计**: [DESIGN.md](./DESIGN.md) v1.2
> **验收配置**: 同基座自查（GLM-5.3，既写又审——如实标注；机械证据全部 E1 可重放，非记忆断言）

---

## 1. 文档一致性验收（Step 8）

### 1.1 RESEARCH.md ↔ DESIGN.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN.md 的设计决策可追溯到 RESEARCH.md | ☑ | §2.1 六行映射表逐一引用（repo: local/Windows entry 陷阱/B1 五检查点/B2 计数前移/只读约束/单一真值源）；2026-08-18 复验已核对 |
| RESEARCH.md 的关键发现被 DESIGN.md 使用 | ☑ | H3 环境风险 → §10.1-1 Windows entry 约束；H2 代码规模 → §10.1-4；OpenMMLab 先例 → §5.2 方案 B 否决依据 |
| 无文档间矛盾 | ☑ | RESEARCH §3.1 主判断与 DESIGN §5.1 选择理由一致；无冲突表述 |

### 1.2 DESIGN.md ↔ IMPLEMENTATION.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN.md 的模块在 IMPLEMENTATION.md 中有对应实施 | ☑ | M1-M5 ↔ IMPLEMENTATION §3.1-3.5 一一对应；数据结构 §4.6 ↔ DESIGN §6.1/6.2 |
| IMPLEMENTATION.md 的接口签名与 DESIGN.md 一致 | ☑ | 五接口一致；`+text` 参数差异（读盘复用优化）已在 IMPLEMENTATION §4.2/4.4/4.5 显式声明——语义不变，属实施优化非契约偏离 |
| DESIGN.md 的不变式在 IMPLEMENTATION.md 中有实施 | ☑ | I-1~I-5 ↔ IMPLEMENTATION §7（验证方式含 E1 重放路径） |
| 无设计未覆盖的实施 | ☑ | 实施期决策全部显式登记为 DR-1~DR-6（IMPLEMENTATION §10），无隐式偏离 |

### 1.3 IMPLEMENTATION.md ↔ CHECKLIST.md 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| IMPLEMENTATION.md 的功能点在本 checklist 有验收项 | ☑ | §2.1-2.5 对应 M1-M5；§3 对应五接口；DR-5/DR-6 修复对应 §2.6 |
| 本 checklist 的验收项可追溯到 IMPLEMENTATION.md | ☑ | 各验收项注明来源节号 |

### 1.4 术语一致性

| 术语 | RESEARCH.md | DESIGN.md | IMPLEMENTATION.md | 一致 |
|------|------------|-----------|-------------------|------|
| 五检查点 | B1（五大机械检查点） | M2-M5 + 前置解析 | M1-M5（M1=CLI 入口） | ☑（M1 为实施期 CLI 承载显式化，DESIGN §3.2 表内已列） |
| 退出码三态 | §2.2 先例 | 0/1/2（§7） | 0/1/2（§3.1） | ☑ |
| CHECKLIST 词表二档 | —（先于 RESEARCH） | §6.3 副轴常量 | §3.2 DC2 判定规则 | ☑（v1.2 前置条件闭合后三文档同轴） |

## 2. 功能验收

### 2.1 M1 CLI 入口

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 子命令解析与分发 | `--help` / `--check-all` / `--selftest` 实测 | 五子命令 + 默认全仓语义正确 | ☑ | `.tmp_help.txt`（E1，2026-08-19）；`--check-all` 输出 §2.6 证据 |
| 退出码三态 | dry-run（0）/ 违规注入（1）/ 异常注入（2） | 0=通过 1=违规 2=工具错误 | ☑ | dry-run exit 0 实测；selftest F7 异常路径；exit 2 路径 = DESIGN §3.4 补注（M1 顶层 try/except，代码结构审查） |
| namespace 强制全仓 | staged-only 场景推演 + 代码审查 | M3 不受 staged 列表约束 | ☑ | IMPLEMENTATION §3.1 实施要点；dry-run 全仓行为实证 |

### 2.2 M2 frontmatter

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| DC1 七字段检查 | selftest F1 | 缺 `depends` 报 P1 含字段名 | ☑ | selftest 13/13 PASS |
| YAML 结构错误检测 | selftest F2 | `yaml-unparsable` P1 | ☑ | 同上 |
| DC2 词表（主轴） | selftest F3 | 非法 status 报 P1 含允许词表 | ☑ | 同上 |
| DC2 词表（CHECKLIST 副轴） | selftest F3b/F3c | `-CHECKLIST` 后缀 → pending 合法 / draft 非法 | ☑ | 同上 |
| 双形态检测窗口 | dry-run 全仓 | 首行式 + 标题后式（10 文件）全覆盖 | ☑ | 34 文件 dry-run：25 契约文件全查、零漏 |
| 装饰性分隔线排除 | selftest F10 | README/CODE_WIKI 式 `---` 判 [skip] | ☑ | 同上；dry-run 首跑 5 误报 → 修复后清零（回归覆盖） |

### 2.3 M3 namespace

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| DC4 id 全仓唯一 | dry-run（含 26 个含 id 文件） | 零重复零违规 | ☑ | dry-run 0 违规 |
| 重复双方各报 | selftest F6 | 两文件同 id → 各一条 P1 | ☑ | selftest 13/13 PASS |

### 2.4 M4 counting

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| R7 A 类对账 | selftest F4 + dry-run 存量 4 文档 | declared ≠ actual 报 P1（附双方数值）；存量对账通过 | ☑ | selftest F4；**ADR0006 A=7→8 漏计被捕获**（DR-5，修复后对账通过） |
| 表格单元格口径 | dry-run CPP_HUB_GAP（11 条表格内【A】） | 表格内标记计入机械重数 | ☑ | dry-run 该文件零违规（A=16 全形态命中对） |
| C 类不对账（DR-2） | 代码审查 + IMPLEMENTATION §3.4 | 首版显式跳过，不误报 | ☑ | dry-run 零 C 类误报 |

### 2.5 M5 linkcheck

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 档 1 断链检测 | selftest F8 + dry-run | 真断链报 P2；档 2 标注/引文行跳过 | ☑ | selftest F8；**ADR-0004/0005 两处真断链被捕获**（DR-5，修复后通过） |
| templates 占位排除 | selftest F8b | `spec/templates/` 内链接不解析 | ☑ | selftest 13/13 PASS |
| fenced block 排除 | dry-run（附录 B assertions 块内链接） | 引文快照链接零误报 | ☑ | dry-run 零该类误报 |

### 2.6 存量违规修复（DR-5/DR-6）

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| ADR0006 A 计数 7→8 | findstr 机械枚举 + dry-run | 8 条【A】标记 vs 声明 8 对账通过 | ☑ | `.tmp_scan2_out.txt` L30/L41/L45/L48/L51/L54/L61/L62 八行；修复后 dry-run 零违规 |
| ADR-0004/0005 断链 | findstr 定位 + Edit 修复 + dry-run | `../../` → `../` 后链接可解析 | ☑ | `.tmp_link_scan.txt` 两处 L21；修复后 dry-run 零违规 |
| selftest 计数 12/12→机械计数（DR-6） | 重跑 selftest | 13 个 expect 实调 = 汇总计数 13/13 | ☑ | `.tmp_selftest2.txt`：`selftest: 13/13 PASS`（v1.0 曾打印 13 行 PASS 却称 12/12——DESIGN §10.2 风险 1 预注册场景的实际命中，M7 样本⑨登记） |

## 3. 接口验收

### 3.1 五接口（M1-M5）

| 验收项 | 通过条件 | 状态 |
|--------|---------|------|
| 签名与 DESIGN §4.1-4.5 一致 | 函数名/参数/返回类型一致（`+text` 差异已显式登记） | ☑ |
| 正常输入返回正确结果 | 合规文件 → 零违规结果（selftest F9） | ☑ |
| 边界输入处理正确 | 无 front-matter / 装饰线 / 非 .md → [skip]（F5/F10） | ☑ |
| 异常输入不崩溃 | 不可读文件 → P2 不抛异常（F7）；YAML 坏结构 → P1 结果（F2） | ☑ |

### 3.2 数据结构

| 验收项 | 通过条件 | 状态 |
|--------|---------|------|
| CheckResult 五字段 frozen dataclass | 与 DESIGN §6.1 逐字段一致 | ☑ |
| Summary.results/passed/violations | 与 DESIGN §6.2 一致 | ☑ |

## 4. 不变式验收

| 不变式（来自 DESIGN §8） | 验证方法 | 状态 |
|---------------------------|---------|------|
| I-1 只读 | 代码审查（无 `open(..., 'w')` 于检查路径；selftest tempfile 属系统临时目录）+ dry-run 后工作树无越界改动 | ☑ |
| I-2 确定性 | 无时间/网络/随机调用；`os.walk` 稳序；dry-run 多轮输出一致 | ☑ |
| I-3 零新规则 | 检查项 ↔ DC1-DC4/R7 逐一对应（§1.2 对齐验收）；实施决策全部 DR 登记 | ☑ |
| I-4 单一真值源 | TYPE_VOCAB/CHECKLIST_STATUS_VOCAB 常量 ↔ DESIGN §6.3 逐字符一致 | ☑ |
| I-5 异构于生成端 | 计数/唯一性/链接 = 纯 `re`/`os` 机械枚举，无 LLM 调用 | ☑ |

## 5. 错误处理验收

| 错误场景（来自 DESIGN §7） | 触发方式 | 预期行为 | 状态 |
|------------------------------|---------|---------|------|
| front-matter 无法解析 | selftest F2 | `yaml-unparsable` P1，不抛异常 | ☑ |
| 七字段缺失/词表非法 | selftest F1/F3/F3b/F3c | 逐字段 P1，含字段名与允许词表 | ☑ |
| id 重复 | selftest F6 | 所有重复方各一条 P1 | ☑ |
| §0 计数 ≠ 重数 | selftest F4 + ADR0006 实例 | P1 含 declared/actual | ☑ |
| 工具自身异常（IO） | selftest F7 | P2 结果不崩溃；顶层异常 → exit 2 | ☑ |
| 非 DC 范围 .md | selftest F5/F10 + dry-run 9 文件 | `[skip]` 零违规 | ☑ |

## 6. 性能验收

| 性能指标 | 目标 | 实测 | 状态 |
|---------|------|------|------|
| 全仓 dry-run 耗时 | < 1s（RESEARCH §3.1 "本地 1 秒拦截"） | 34 文件毫秒级（bash 往返内完成，无感知延迟） | ☑ |
| Python 启动开销 | 绕过 hermes venv 353s site 延迟 | `python -S -E` + Python 3.12 实测 0.04s（IMPLEMENTATION §2.1） | ☑ |

## 7. 兼容性验收

| 环境 | 版本 | 状态 | 说明 |
|------|------|------|------|
| Python | 3.12 | ☑ | 主验环境（pre-commit 4.6.2 安装处；dry-run/selftest/pre-commit 三通道实测） |
| Python | 3.8-3.11 | ☑ | 语法层兼容（stdlib 下限检查，IMPLEMENTATION §5.1）；hermes venv 3.11 经 `-S -E` 路径实测可运行 |
| OS | Windows | ☑ | 主控站全流程实测（entry 走 `python` 前缀规避 `/bin/sh` 陷阱） |
| OS | Linux | ☑ | 结构性保证（`os.walk`/`os.path` 跨平台，无硬编码分隔符）；未实机验证（工作站 A/B 未跑，如实标注） |

## 8. ADD 审计（Step 10）

### 8.1 Spec 质量门（Phase 0）——自查评分

| 维度 | 得分（0-1） | 说明 |
|------|-----------|------|
| 可测试约束 | 1 | 五检查全部有 fixture + dry-run 双通道 E1 证据 |
| 模块映射 | 1 | M1-M5 ↔ DESIGN §3.2 ↔ IMPLEMENTATION §3 闭合 |
| 接口契约 | 1 | §4 五接口签名一致（`+text` 差异显式登记） |
| 修正项 | 1 | P2-1/P3-2（复验轮）+ DR-1~DR-6（实施轮）全部闭合或显式挂起（DR-2 挂起有依据） |
| 跨模块契约 | 1 | front-matter 解析器为 M2/M3 共享单一实现（**v1.1 修正注**：v1.0 作"M2/M3/M4"系映射闭合假象——独立 pass 逐项核对，M4 `check_counting` 独立扫描 §0 节、从不调用 `parse_frontmatter`；M7 样本⑬） |
| **总分** | 5/5 | **档位**: A（自查 2026-08-19；独立 ADD 审计已完成 2026-08-20——见 §8.2 独立轮 3 P3，全登记修正，档位维持 A） |

### 8.2 ADD 审计发现

| 严重性 | 发现 | 证据 | 修复建议 |
|--------|------|------|---------|
| P2 | selftest 汇总计数硬编码 12/12（实调 13 个 expect）——形态 II 于审查工具自身，DESIGN §10.2 风险 1 预注册场景命中 | `.tmp_selftest.txt` 13 行 PASS vs "12/12" | 已修复（DR-6：expect 自增机械计数）；M7 样本⑨登记 |
| P3 | Linux 兼容性为结构性保证未实机验证 | IMPLEMENTATION §5.4 | 可选：工作站 A/B 跑一次 dry-run 补证实（非阻塞） |
| P3（独立轮） | IMPLEMENTATION §4.3/§4.5 签名一致性声明未覆盖 `root=ROOT` 实施参数（selftest 隔离所需，同类于已声明 `+text`） | 独立 pass 代码对账（2026-08-20） | 已补 IMPLEMENTATION v1.2 §4.3/§4.5 修正注 |
| P3（独立轮） | §8.1 跨模块契约行"M2/M3/M4 共享解析器"不实——M4 不调用 `parse_frontmatter`（映射闭合假象，M7 样本⑬） | 独立 pass 逐项核对（2026-08-20） | 本文件 v1.1 §8.1 修正注 |
| P3（独立轮） | DESIGN §10.1-4 代码量"~100 行（实施时核对）"核对缺位——独立 pass 实测 422 行（selftest 块 ~104 行） | 独立 pass（2026-08-20） | IMPLEMENTATION v1.2 DR-7 登记 |

### 8.3 ADD Iron Law 检查

- [x] 测试通过的 4 类盲区已检查：
  - 断言恒真式：selftest F1-F10 断言均含具体 message/severity 匹配，非恒真（F6 断言 `len(r)==2` 精确计数）
  - 单文件检查盲区：M3 namespace 为全仓检查，dry-run 覆盖 34 文件全集，非单文件视角
  - 设计文档独有约束无测试：I-1~I-5 每条均有 §4 验证方法与证据路径
  - 修正阻断性项无测试：DR-5 三处存量修复 + DR-6 计数修复均以 dry-run/selftest 重跑验证（修复后归零）

## 9. 文档完整性

| 文档 | 存在 | 与实现一致 |
|------|------|----------|
| RESEARCH.md（[PRECOMMIT_DC_VALIDATOR_RESEARCH.md](./PRECOMMIT_DC_VALIDATOR_RESEARCH.md) v1.1） | ☑ | ☑ |
| DESIGN.md v1.2 | ☑ | ☑ |
| IMPLEMENTATION.md v1.1 | ☑ | ☑（13/13、34 文件等 v1.1 事实同步） |
| CHECKLIST.md（本文件） | ☑ | ☑ |
| ADR | ☑（不新增——工具为 ADR-0007 契约的执行器，无新架构决策；DR-1 检测窗口若契约显式化另行裁决） |
| 开发日志 | ☑（DEV-LOG-003 随本 feature 登记） |

## 10. 验收结论

### 10.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|------|------|------|------|------|
| 文档一致性 | 10 | 10 | 0 | 0 |
| 功能 | 17 | 17 | 0 | 0 |
| 接口 | 6 | 6 | 0 | 0 |
| 不变式 | 5 | 5 | 0 | 0 |
| 错误处理 | 6 | 6 | 0 | 0 |
| 性能 | 2 | 2 | 0 | 0 |
| 兼容性 | 4 | 4 | 0 | 0（Linux 实机为可选项） |
| ADD 审计 | 5 + 4 盲区 | 5 + 4 | 0 | 独立轮（Step 10） |
| **总计** | **50 + 4** | **50 + 4** | **0** | **1（独立 pass）** |

### 10.2 验收决定

- [x] **验收通过**：所有 P1 项通过，无阻塞性问题（2026-08-20 独立 pass：E1 四通道复核全过 + 3 P3 全登记修正，无 P1/P2 遗留）
- [x] **有条件通过**（2026-08-19 自查时点历史状态）：自查全绿 + 机械证据齐备（dry-run 双通道 0 违规 + selftest 13/13）；条件 = RULE-1 时序独立 pass（含 Step 10 ADD 独立审计）——**已于 2026-08-20 满足**（真异基座 DeepSeek V4 Pro），升 accepted
- [ ] **验收失败**：

### 10.3 签字

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | GLM-5.3（自查，机械证据 E1 可重放） | 2026-08-19 |
| 审查者 | DeepSeek V4 Pro（真异基座独立 pass：RULE-1 时序独立 + RULE-5 异构于生成端 GLM-5.3，双满足） | 2026-08-20 |

## 11. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|------|--------|------|------|
| M7 样本⑨登记（2 形态 II 实例：ADR0006 A 漏计 + selftest 硬编码计数；分桶合计 13→15） | 本轮完成 | 2026-08-19 | ✅（docs/M7_EVIDENCE_LOG.md） |
| RULE-1 独立 pass（IMPLEMENTATION v1.1 + 本 CHECKLIST；真异基座优先） | DeepSeek V4 Pro（对话式默认形态） | 2026-08-20 | ✅ 3 P3 登记修正（IMPLEMENTATION v1.2 修正注 + DR-7 / 本文件 v1.1）；M7 样本⑬ 入账（映射闭合 1 处，分桶 20→21） |
| DR-2：C 类计数对账启用（待 FWK-ASSERTION 统一 C 类标记格式） | 待 FWK 演进 | — | 挂起 |
| DR-1：front-matter 检测窗口契约显式化（PLAN DC1 注记） | 另行裁决 | — | 候选 |
| Linux 实机 dry-run（工作站 A/B） | 可选 | — | 候选 |
| 更新 PROGRESS.md（P-007 → done） | 本轮完成 | 2026-08-19 | ✅ |
| 记录开发日志（DEV-LOG-003） | 本轮完成 | 2026-08-19 | ✅ |
