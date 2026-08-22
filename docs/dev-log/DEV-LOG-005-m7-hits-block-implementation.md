# DEV-LOG-005: m7-hits-block 全流程——spec 四件套 → m7_stats.py 落地 → hits 块 bootstrap → 样本⑮ 首次实战登记

> **日期**: 2026-08-21
> **会话**: Claude DeepSeek V4 Pro（主控站）
> **涉及**: spec/m7-hits-block/（RESEARCH/DESIGN/IMPLEMENTATION v1.1/CHECKLIST）/ scripts/m7_stats.py / .pre-commit-config.yaml / docs/M7_EVIDENCE_LOG.md / docs/FACT_CHECK_FRAMEWORK.md / docs/PROGRESS.md / CODE_WIKI.md
> **状态**: CHECKLIST 有条件通过（自查全绿，机械证据 E1 可重放；RULE-1 独立 pass 待触发，验收决定同 P-007 先例）

---

## 做了什么（时序）

1. **Step 1-2 RESEARCH.md**（11A+1B+3C+2H，仓库内部调研零外部文献如实声明）：盘点 M7 手工统计面四类可重数项（样本行数/分桶行列算术/跨表对账不变式/P 分级汇总）、历史非整齐形态两处（样本③非标准发现、样本⑨未标级发现）、dc_validator 三件套先例（退出码/selftest/零依赖）与 M4/M5 边界（R7 不覆盖 M7、围栏内链接跳过）。
2. **Step 3-4 DESIGN.md**：hits 机读块契约（六字段 + findings 五键，禁止时间态字段）+ 校验规则集（m7-sample/m7-bucket/m7-xtable/m7-hits 四类 12 条）+ 写守卫语义（--write 非绕过通道而是校验后落盘）+ P3 非阻断档（历史非整齐形态如实容纳）+ 不变式 I-1~I-6 + 四替代方案（含"只加块不做脚本"否决——无重数器的声明块比无块更危险）。
3. **Step 5-8 IMPLEMENTATION/CHECKLIST**：解析契约正则化（表头名序校验防列重排静默错位 = I-4 防护）+ 14 fixture 矩阵 + stdlib API 下限表。
4. **Step 9 TDD 实现**：`scripts/m7_stats.py` 828 行（MH1-MH5）+ `.pre-commit-config.yaml` 第二 hook（files 收窄 `^docs/M7_EVIDENCE_LOG\.md$`）。selftest 首跑 35/40——两处实现 bug（`_looks_like_ledger` 缺 `re.M` 导致无围栏账本误判 skip；--write 成功后仍聚合写前旧结果误报 exit 1）由 fixture 捕获修复，二跑 **40/40 PASS**。
5. **M7 bootstrap**：verify（缺块 P1）→ `--write --seed-pre-ledger 6`（基线人工声明 = Phase 7C 行小计，A3 取证核对）→ verify exit 0。生成值与 RESEARCH 人工重数全等：samples=14 / by_field 1|2|3|2|10|1|2 / total=21 / pre_ledger=6 / from_samples=15 / findings p1=5 p2=22 p3=25 unlabeled=1 nonstandard=1。
6. **实施期拦截（提交前 dry-run，dc_validator）**：① 本 feature RESEARCH 初稿 A 标记 `#### 【A】` 标题式 → M4 重数 0≠11 报 P1（标记格式即机读契约）；② 上轮 b541705（FWK-FACT-CHECK）遗留 3 条 P2 断链（file:/// 外链缺档 3 标注 ×2 + adr/ 相对路径 ×1）被 M5 捕获——b541705 当次提交未走 hook 通道。均已修复。
7. **样本⑮ 登记 + 新工作流首次实战**：手工追加样本行（1P1+3P2，形态II复发=0 如实登记不入分桶）→ `m7_stats.py --write` 重生成 hits（samples 14→15，findings p1 5→6 p2 22→25）→ verify exit 0。**P-011 交付的工作流在本 feature 收尾即自举使用**。
8. **登记收束**：PROGRESS P-011 → done；CODE_WIKI v1.6 工具层同步；本 DEV-LOG。

## 决策依据

### ① 独立脚本而非并入 dc_validator（RESEARCH C1）

dc_validator 是全仓通用 DC 契约执行器且 P-008 已 verified/accepted；M7 统计解析是单文件特化逻辑（表结构耦合）。"衔接"落地为三同构：R7 声明=重数原则、退出码 0/1/2 语义、pre-commit 通道。修改 verified 工具的审查成本收益比为零。

### ② pre_ledger 设计为声明量而非推导量

跨表不变式 `form2_total = pre_ledger + form2_from_samples` 若把 pre_ledger 定义为 `total − from_samples` 则恒真（循环推导）。Phase 7C 基线（6）是历史事实：首次 bootstrap 须 `--seed-pre-ledger` 人工显式声明，此后由不变式持续看护——新增非样本来源分桶行会打破对账触发 P1，强制人工同步基线声明（RESEARCH H1 机制化）。

### ③ LOC 预估口径失误（828 vs ~300±100）

预估只计了核心校验逻辑（~470 行），selftest 十四 fixture 的账本模板串与闭环断言（~360 行）未计入基数。与 P-008 P3 ③（DESIGN ~100 行 vs 实际 422）同族——**DESIGN LOC 预估必须写明口径（核心逻辑 vs 含测试）**，已在 IMPLEMENTATION v1.1 §10 如实登记。

### ④ 样本⑮ 的登记边界（形态II复发 = 0）

标记格式违规与断链均非"低语义载荷字段错值"（形态 II 定义），如实登记 0 不入 §2 分桶——与样本⑭（撞名风险同处置）一致，防分桶统计纯度稀释。但 1P1+3P2 的发现数如实计入 hits findings 汇总。

## 遇到的问题

- selftest 首跑 5 处 FAIL 均为真实实现 bug（见时序 4），fixture 矩阵有效性实证——F10 的"无围栏账本"用例正是抓 `re.M` 缺失的哨兵
- PowerShell 内嵌 python -c 多引号转义不可靠（SyntaxError）→ 改用 dc_validator 自身作 R7 机械重数通道（工具即证据）
- b541705 断链遗留提示：**绕过 hook 的提交会积累到下一次全量校验才爆**——commit 通道纪律 = 提交前 `pre-commit run --all-files` 或至少 dc_validator --check-all

## 独立审计追记（2026-08-22）

深度审计 review（异步独立 + 异基座视角）对账上一轮 P-011 交付，捕获一处文档一致性缺口：

- **发现（P3）**：CODE_WIKI.md v1.6 两处错误断言「样本⑫-⑮ 均非形态 II」，与 M7 账本实际登记冲突——⑫=计数、⑬=映射闭合均为形态 II 复发，仅 ⑭=撞名、⑮=格式非形态 II。根因 = P-011 落地同步 wiki 时，把「样本序范围」手写枚举与账本真实分桶脱节（形态 II 计数错误在 prose 层的复发）。
- **修复**：CODE_WIKI.md L3/L574 两处「样本⑫-⑮」→「样本⑭-⑮」，分类措辞「格式/撞名/映射类」→「格式/撞名类」（映射属样本⑬ 形态 II，不列入非形态 II 描述）。
- **教训**：聚合/索引类文档（CODE_WIKI）的「样本范围枚举」是低语义载荷字段，与 M7 §2 分桶同族。P-011 已让账本自身统计进机械对账，但 wiki 的 prose 枚举仍未纳入——本轮以全仓 grep 机械枚举兜底捕获（同「全仓 grep 拦截 prose 计数」既有防线）。
- **登记**：形态 II 复发（计数）已入 M7 样本⑯（2026-08-22）——本 feature 交付的登记工作流第二次实战（手工加行 → `m7_stats.py --write` → verify exit 0），hits 块 samples 15→16 / form2_total 21→22 / findings p3 25→26；分桶表新增 CODE_WIKI v1.6 行（计数 +1），CODE_WIKI 成为唯一两入分桶的载体（v1.5 见样本⑪）。

## 下一步

- 独立 pass（RULE-1 时序独立，真异基座优先）：审查对象 = m7-hits-block 四件套 + m7_stats.py（挂后续会话，触发条件同 P-008 先例；PROGRESS 后续行动已登记）
- P-010（promptfoo M7 对比臂声明式评测，优先级 3）：hits 机读块为评测结果登记自动化铺路（顺流弱依赖兑现）
- DR-B/DR-C 两个已知测试缺口（发现列空值 P1 / §5 无围栏守卫的专项 fixture）随独立 pass 一并补或另行登记
