# 审查验收 Checklist：M7 hits 机读块 + 样本登记脚本化

---
id: m7-hits-block-CHECKLIST
type: design
version: 1.2
status: accepted
date: 2026-08-23
depends: [m7-hits-block-IMPLEMENTATION, m7-hits-block-DESIGN]
upstream: null
---

> **Feature**: m7-hits-block（PROGRESS P-011）
> **创建日期**: 2026-08-21
> **状态**: accepted（同基座降级独立 pass 完成——RULE-1 时序独立满足，RULE-5 模型异质性未满足（生成端/审查端均为 DeepSeek V4 Pro），如实降级标注；DR-B/C 专项 fixture 补齐（F15/F16）+ 审计发现全处置）
> **Spec 步骤**: Step 7-8, 10
> **基于实施**: [M7_HITS_IMPLEMENTATION.md](./M7_HITS_IMPLEMENTATION.md) v1.2
> **基于设计**: [M7_HITS_DESIGN.md](./M7_HITS_DESIGN.md) v1.0
> **验收者**: 自查（单视角，RULE-4）DeepSeek V4 Pro；独立 pass = 同基座降级审查（RULE-1 满足，RULE-5 降级标注）已完成

---

## 1. 文档一致性验收（Step 8）

### 1.1 RESEARCH ↔ DESIGN 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| DESIGN 决策可追溯 RESEARCH（A1-A11/B1/C1-C3） | ☒ | §2.1 映射表 6 行逐一引用；A1-A6→hits 字段集、A7/A8→三件套继承、A9→JSON 围栏、A10/A11→独立脚本、B1→三风险面校验集 |
| RESEARCH 关键发现被 DESIGN 使用（无孤儿发现） | ☒ | A1-A11 全部映射；H1→§4.2 pre_ledger 声明 + §4.3 xtable；H2→§6 性能验收 |
| 无文档间矛盾 | ☒ | |

### 1.2 DESIGN ↔ IMPLEMENTATION 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 模块 MH1-MH5 ↔ IMPLEMENTATION §3/§4 | ☒ | |
| 校验规则集（DESIGN §4.3）↔ IMPLEMENTATION §2.4/§6 逐行 | ☒ | 12 条规则逐一实现；DR-B（空值 P1）/DR-C（§5 守卫）为实施期派生，已登记 IMPL §10 |
| 不变式 I-1~I-6 ↔ IMPLEMENTATION §7 | ☒ | |
| 接口签名一致（含 pre_ledger 双态细化说明） | ☒ | IMPL §9.2 显式声明细化语义 |
| LOC 预估核对义务登记（IMPLEMENTATION §10） | ☒ | 828 行回填 + 口径失误如实登记（预估仅计核心 ~470，selftest ~360 未计） |

### 1.3 IMPLEMENTATION ↔ CHECKLIST 对齐

| 检查项 | 状态 | 说明 |
|--------|------|------|
| IMPLEMENTATION 功能点在本 checklist 有验收项 | ☒ | §2-§7 |
| 本 checklist 验收项可追溯到 IMPLEMENTATION | ☒ | |

### 1.4 术语一致性

| 术语 | RESEARCH | DESIGN | IMPLEMENTATION | 一致 |
|------|----------|--------|----------------|------|
| hits 机读块 / ```hits 围栏 | ✅ | ✅ | ✅ | ☒ |
| form2_pre_ledger（先于账本基线） | ✅（A3） | ✅（§4.2） | ✅（§3.4） | ☒ |
| cells_nonstandard / unlabeled | ✅（A5/A6） | ✅（§4.2） | ✅（§2.4） | ☒ |
| 写守卫（write-guard） | —（C3 边界） | ✅（§3.4） | ✅（§6） | ☒ |

### 1.5 双向引用与断言延续（ADR-0008 D6）

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 四文档 + PROGRESS P-011 + M7 §4 互引成立 | ☒ | 正向：四件套→M7/PROGRESS/ADR-0007/LANGGRAPH/precommit-DESIGN 全部可解析（dc_validator M5 全仓 0 违规实证）；反向：PROGRESS P-011 → spec 目录链接、M7 §4 → M7_HITS_DESIGN、CODE_WIKI §4.5 → 四件套 |
| B1 断言状态按最新词表标注 | ☒ | RESEARCH 附录 B audit_status: CLOSED（同基座降级独立 pass 完成——RULE-1 满足，RULE-5 降级） |

## 2. 功能验收

### 2.1 MH2 样本表解析

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 行结构校验（编号/列数/日期/前导整数） | F2/F3/F4/F5 | 各报对应严重性 | ☒ | selftest 44/44（E1） |
| P 抽取五形态 | F11a-f | ptok/lead/nonstandard 精确值 | ☒ | 同上 |
| 真实 M7 §1 解析 | dry-run | samples=15 无违规 | ☒ | verify exit 0 + hits 块 samples=15（E1） |

### 2.2 MH3 分桶表解析

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 行算术（小计=行和） | F6 | P1 | ☒ | selftest 44/44 |
| 列算术（合计=列和） | F7 | P1 | ☒ | 同上 |
| 真实 M7 §2 解析 | dry-run | form2_total=21 无违规 | ☒ | verify exit 0（E1） |

### 2.3 MH4 统计/对账/序列化

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| 跨表不变式 | F8 + 真实 M7 | 21 = 6 + 15 | ☒ | F8 P1 + 真实账本 verify 过（E1） |
| hits 声明对账（逐字段） | F9 | 失配报 declared/actual | ☒ | "samples 声明 3 实为 2"（E1） |
| 确定性序列化 | F13 | 双跑逐字节一致 | ☒ | selftest 44/44 |

### 2.4 MH1 CLI 三模式 + 写守卫

| 验收项 | 测试方法 | 通过条件 | 状态 | 证据 |
|--------|---------|---------|------|------|
| verify 默认模式 | 真实 M7 dry-run | bootstrap 后 exit 0 | ☒ | E1（本轮三次运行输出留痕） |
| --write 修复闭环 | F9 | 失配→写入→verify 过 | ☒ | selftest 44/44 |
| bootstrap（--seed-pre-ledger） | F10 + 真实执行 | 无 seed 拒绝；seed=6 落盘 | ☒ | F10 全路径 + 真实 bootstrap（E1） |
| 写守卫 | F12 | 非 hits 违规时文件字节不变 | ☒ | selftest 44/44 |
| P3 非阻断 | F14 | exit 0 + [P3] 打印 | ☒ | selftest 44/44（stdout 捕获断言） |
| staged 非 M7 文件 skip | 伪文件名调用 | exit 0 [skip] | ☒ | F1 内 skip 断言（plain.md） |

## 3. 接口验收

| 接口（IMPLEMENTATION §4） | 签名一致 | 正常输入 | 边界/异常 | 状态 |
|--------------------------|---------|---------|----------|------|
| main / gather_targets | ☒ | ☒ | 未知异常→exit 2（顶层 try/except，结构同 dc_validator） | ☒ |
| parse_sample_table | ☒ | ☒ | 节缺失→P1 哨兵 | ☒ |
| parse_bucket_table | ☒ | ☒ | 节缺失→P1 哨兵 | ☒ |
| compute_stats / check_xtable / compare_hits / serialize_hits | ☒ | ☒ | pre_ledger=None→跳过 xtable（F10 验证） | ☒ |
| run_selftest | ☒ | 40/40 PASS | FAIL→exit 1 | ☒ |

## 4. 不变式验收

| 不变式 | 验证方法 | 状态 |
|--------|---------|------|
| I-1 默认只读 | F12（写守卫拒绝时字节不变）+ 本轮 verify 运行 git 工作树仅预期文件变更 | ☒ |
| I-2 确定性 | F13 双跑逐字节一致 | ☒ |
| I-3 零新规则 | 规则集 ↔ DESIGN §4.3 逐行核对（人工 E3）；DR-B/C 派生已显式登记不冒充既有规则 | ☒ |
| I-4 单一真值源 | 表头名序校验（F1 变体：列名错位报 P1——mini fixture 表头即契约）+ 常量注释指向 M7 | ☒ |
| I-5 异构于生成端 | import 清单审查：argparse/datetime/json/os/re/sys/dataclasses/tempfile/shutil/io/contextlib——零网络/LLM 库 | ☒ |
| I-6 声明=重数 | F9/F12 + bootstrap 值与 RESEARCH A1-A4 人工重数全等（samples/total/pre_ledger/from_samples 四值） | ☒ |

## 5. 错误处理验收

| 场景 | 触发 | 预期 | 状态 |
|------|------|------|------|
| hits JSON 非法 | analyze 路径（unfixable 判定覆盖） | P1（--write 拒绝——unfixable 列表含"不可解析"） | ☒ |
| 表节缺失 | parse_* 入口哨兵 | P1 | ☒ |
| 工具自身异常 | main 顶层 try/except | exit 2（结构审查） | ☒ |

## 6. 集成验收

| 项 | 方法 | 通过条件 | 状态 |
|----|------|---------|------|
| pre-commit hook | `pre-commit run m7-stats --all-files` | M7 通道通过 | ☒ Passed（E1） |
| dc_validator 回归 | `python scripts/dc_validator.py --check-all` | 0 违规 | ☒ 44 文件 11 结果 0 违规（E1） |
| 双工具共存 | 同轮全量校验 | 全过 | ☒ |
| bootstrap 值核对 | M7 §5 人工 Read | samples=14→15 / total=21 / pre_ledger=6 / from_samples=15 | ☒ 与 RESEARCH A1-A4 全等 |
| 性能（H2 查证） | hook 实测 | 秒级内 | ☒ pre-commit 通道无感知延迟（E1 观测） |

## 7. 兼容性验收

| 环境 | 版本 | 状态 | 说明 |
|------|------|------|------|
| Python | 3.12（主控站实测运行） | ☒ | stdlib API 下限表见 IMPL §2.2 |
| OS | Windows（PowerShell 5 会话） | ☒ | entry python 前缀；路径反斜杠归一化 |
| pre-commit | 4.6.2 | ☒ | 双 hook 并存（dc-validator + m7-stats） |

## 8. ADD 审计（Step 10）

### 8.1 Spec 质量门（Phase 0）

| 维度 | 得分（0-1） | 说明 |
|------|-----------|------|
| 可测试约束 | 1.0 | 校验规则集全量化（§4.3 表，check_id × 严重性） |
| 模块映射 | 1.0 | MH1-MH5 ↔ IMPL §3 逐一对应 |
| 接口契约 | 0.8 | pre_ledger 双态（int/None）为实施期细化（IMPL §9.2 已声明） |
| 修正项 | 1.0 | 偏离全部显式登记（DR-A/B/C + LOC 口径） |
| 跨模块契约 | 0.9 | pre_ledger 数据流 §3.4 定义；DR-B/C 两处行为初始未显式（后补登记） |
| **总分** | **4.7/5** | **档位**: A |

### 8.2 ADD 审计发现

| 严重性 | 发现 | 证据 | 修复建议 |
|--------|------|------|---------|
| P1 | RESEARCH §0 A 标记用 `#### 【A】` 标题式，非行首契约格式 → M4 重数 0≠11 | dc_validator dry-run 输出（E1） | 已修复（行首标记）；入 M7 样本⑮ |
| P2 | 上轮 b541705 遗留断链 3 条（file:/// 外链缺档 3 标注 ×2 + adr/ 相对路径 ×1） | 同上（E1） | 已修复（外部· 前缀 + ../adr/）；入 M7 样本⑮ |
| P3 | LOC 预估口径失误（~300 vs 实际 828——selftest 未计入预估基数） | IMPL §10 回填（E1） | 已登记 + 教训固化（预估须写明口径） |
| P3 | DR-B/DR-C 两派生行为无专项 fixture（空发现列 P1 / §5 无围栏守卫） | 代码路径审查（E3） | 已补 F15/F16 专项 fixture（2026-08-23 同基座降级独立 pass），selftest 40→44 断言 |
| P3 | 【独立审计追记·2026-08-22】CODE_WIKI.md v1.6 两处错误断言「样本⑫-⑮ 均非形态 II」，与 M7 账本实际登记冲突（⑫=计数、⑬=映射闭合均为形态 II；⑭=撞名、⑮=格式非形态 II） | M7 §1 样本⑫-⑮ vs CODE_WIKI.md L3/L574 比对 | 已修正为「样本⑭-⑮ 均非形态 II」，措辞「格式/撞名/映射类」→「格式/撞名类」；形态 II 复发（计数）入 M7 样本⑯（新工作流：手工加行 → --write → verify） |

### 8.3 ADD Iron Law 检查

- [x] 断言恒真式——草稿期曾误留一条恒真占位断言（`== 1 or True`），自查发现删除；终稿 44 断言全部绑定具体值/退出码
- [x] 单文件检查盲区——真实 M7 全量 dry-run 三轮（bootstrap 前/后 + 样本⑮ 后），非 fixture 替代
- [x] 设计独有约束无测试——写守卫（F12）/确定性（F13）/P3 档（F14）均有专项 fixture
- [x] 修正阻断性项无测试——F9/F10 覆盖两条修复路径（失配重写 / 缺块 seed）

### 8.4 取证矩阵（RULE-6）

| 取证手段（等级） | 覆盖项 | 结果 |
|----------------|--------|------|
| selftest 输出（E1） | §2.1-2.4 全部 fixture 验收项 + §3 selftest | **44/44 PASS**（v1.2 独立 pass 补 F15/F16；首跑 35/40 → 修 2 bug → 40/40 的 14-fixture 迭代留痕） |
| 真实 M7 dry-run 输出（E1） | §2.1-2.3 真实值 / §6 bootstrap 核对 | 三轮运行：缺块 P1 → bootstrap（samples=14→15）→ verify exit 0 |
| dc_validator 全仓回归（E1） | §6 回归 / §1.5 正向引用 | 44 文件，11 结果，0 违规（M7_HITS_RESEARCH 的 M4 检查同轮通过 = R7 A=11 对账） |
| pre-commit 通道输出（E1） | §6 hook | m7-stats Passed |
| 静态读码（E3 @工作树 m7_stats.py） | §4 不变式人工核对项 / §8.2 P3 | import 清单审查 + 规则集逐行核对 |
| 盲区扫描（E4，范围：恒真式 44 断言逐条 + DR-B/C 代码路径 + LOC 口径） | Iron Law 四盲区 | **发现 3 项**（恒真占位 1 + DR-B/C 缺口 2——后两项转 §8.2 P3 登记，v1.2 已补 F15/F16 关闭） |

### 8.5 独立 pass 记录（同基座降级，2026-08-23）

| 维度 | 结论 |
|------|------|
| RULE-1 时序独立 | ☒ 满足（新会话与生成/收口轮分离，异步独立） |
| RULE-5 模型异质性 | ☐ 未满足（生成端/审查端均为 DeepSeek V4 Pro——同基座降级标注，同理样本⑦形态） |
| 机械校验重放 | ☒ `--selftest` 44/44（F15/F16 新增 4 断言）+ verify 于真实 M7 exit 0 + dc_validator 全绿 |
| 审查发现 | 无 P1/P2；1 P3 已处置（DR-B/C 专项 fixture 补齐，原 §8.2 P3 行已闭合） |
| 结论 | **同基座降级独立 pass 通过**；IMPLEMENTATION → verified、本 CHECKLIST → accepted；RULE-5 异质性待异基座升级复验 |

## 9. 文档完整性

| 文档 | 存在 | 与实现一致 |
|------|------|----------|
| M7_HITS_RESEARCH.md | ☒ | ☒（A=11 经 M4 机械重数一致） |
| M7_HITS_DESIGN.md | ☒ | ☒ |
| M7_HITS_IMPLEMENTATION.md v1.2（含实际 LOC） | ☒ | ☒（845 行回填 + DR-A/B/C——B/C 随独立 pass 补 F15/F16 fixture） |
| M7_HITS_CHECKLIST.md（本文件） | ☒ | ☒ |
| 开发日志 DEV-LOG-005 | ☒ | ☒ |
| PROGRESS P-011 → done | ☒ | ☒（验收证据三要求逐一映射） |
| M7_EVIDENCE_LOG §5 hits 块 + 头注/§4 更新 | ☒ | ☒（样本⑮ 以新工作流登记） |

## 10. 验收结论

### 10.1 验收统计

| 类别 | 总数 | 通过 | 失败 | 待办 |
|------|------|------|------|------|
| 文档一致性 | 12 | 12 | 0 | 0 |
| 功能 | 14 | 14 | 0 | 0 |
| 接口 | 5 | 5 | 0 | 0 |
| 不变式 | 6 | 6 | 0 | 0 |
| 错误处理 | 3 | 3 | 0 | 0 |
| 集成 | 5 | 5 | 0 | 0 |
| 兼容性 | 3 | 3 | 0 | 0 |
| ADD 审计 | 4 盲区 + 4 发现 | 4 盲区全查；发现 4 项全数处置（1P1+3P2 修复入样本⑮；2P3 登记，其中 DR-B/C 缺口随独立 pass 补 F15/F16 关闭） | 0 | 0 |
| **总计** | **52 项 + 4 发现** | **52** | **0** | **0** |

### 10.2 验收决定

- [x] **验收通过**：所有 P1 项通过，无阻塞性问题；同基座降级独立 pass（RULE-1 时序独立满足，RULE-5 异质性降级标注）完成——IMPLEMENTATION → verified、本 CHECKLIST → accepted
- [ ] ~~**有条件通过**~~：~~自查全绿 + E1 机械证据可重放；条件 = RULE-1 独立 pass（真异基座优先）后 IMPLEMENTATION → verified、本 CHECKLIST → accepted~~（条件已满足，转验收通过）
- [ ] **验收失败**

### 10.3 签字

| 角色 | 签字 | 日期 |
|------|------|------|
| 实施者 | DeepSeek V4 Pro（自查·单视角，RULE-4） | 2026-08-21 |
| 审查者 | DeepSeek V4 Pro（同基座降级独立 pass，RULE-1 满足；RULE-5 异质性待异基座升级复验） | 2026-08-23 |

## 11. 后续行动

| 行动 | 责任人 | 期限 | 状态 |
|------|--------|------|------|
| 独立 pass（RULE-1 时序独立，真异基座优先；含 DR-B/C fixture 补齐） | 触发驱动 | — | ✅ 已完成（同基座降级——RULE-1 满足，RULE-5 待异基座升级复验；DR-B/C fixture F15/F16 已补，selftest 44/44） |
| ~~更新 PROGRESS.md（P-011 → done）~~ | — | — | ✅ 已完成 |
| ~~记录 DEV-LOG-005~~ | — | — | ✅ 已完成 |
| ~~CODE_WIKI 工具层同步（§4.5/结构树/拦截表）~~ | — | — | ✅ 已完成（v1.6） |
