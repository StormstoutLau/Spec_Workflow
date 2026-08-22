# 设计文档：repo_stats 视图层机械枚举校验器

---
id: repo-stats-DESIGN
type: design
version: 1.1
status: draft
date: 2026-08-22
depends: [repo-stats-RESEARCH, SPEC-PROCESS, ADR-0007, precommit-dc-validator-DESIGN, m7-hits-block-DESIGN]
upstream: null
---

> **Feature**: repo-stats（PROGRESS P-014，[DIS-010](../../docs/discoveries/README.md) 处置落地）
> **创建日期**: 2026-08-22
> **状态**: draft（草稿）
> **Spec 步骤**: Step 3-4
> **基于调研**: [REPO_STATS_RESEARCH.md](./REPO_STATS_RESEARCH.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验
> **v1.1 变更（2026-08-22，实施前契约修正）**: `derived.view_layer_total` 真值口径修正——原 v1.0 定义「view_layer_samples 各样本形态II复发列求和」在 IMPLEMENTATION 撰写取证时对账不成立：样本求和 = 3+1+7+5+11+8 = 35 ≠ DIS-010 登记值 33（样本⑪ 三行分桶中仅 CODE_WIKI v1.5 行属视图载体，DEV-LOG-004/PROGRESS P-010 两行非视图层错误）。正确口径 = M7 §2 分桶表**载体列匹配视图载体模式集（CODE_WIKI / README / evidence.svg）的行小计求和** = 1+1+7+5+11+8 = 33 ✓；view_layer_samples 降为追溯性语义声明（非求和基础）。修正触及 §4.2 字段表 / §4.2 绑定集表 / §4.4 rs-decl / §6 TruthSet 四处

---

## 1. 设计目标

把聚合视图层（CODE_WIKI / README 双语 / evidence.svg / discoveries 索引）的手写枚举数字从**无失效检测的缓存副本**（DIS-010：八度实证、视图层 33 处占形态 II 总量 62%、四连残留链 ⑰→⑱→⑲→⑳）变成 **stats 机读声明块 + 模式扫描对账 + 提交瞬间拦截**。与 m7_stats 的本质区别（RESEARCH B1）：视图 prose 不可机械重生成，故本工具是**对账器**（扫描-比对-报告，只报偏差、永不代改），无 --write 模式。

产出两件：① `CODE_WIKI.md` 末尾新增 §10 ```stats 机读块（模式库 + 载体分类 + 实体计数声明 + 视图层口径 + 门面快照基准的唯一登记处）；② `scripts/repo_stats.py`（verify / --selftest 两模式）+ pre-commit 第三 hook `repo-stats`。

直接对症的失效形态是⑳轮新证：修正轮的版本头声明（「修完即绿」）与正文执行分离且无对账。本设计的回应有二：把**修正轮产出自身**（版本头叙事里的统计数字）纳入扫描范围（I-7）；让声明（stats 块）与执行（prose 位点）被同一工具对账——两个失效面共用一个看护层。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| CODE_WIKI 单文件 4 副本 M7 统计 + 覆盖对象行 8 类实体计数，位点集不可穷举 | 模式扫描制（正则模式库 × 载体全集），不做位点登记 | RESEARCH A1/A2 |
| 目录树/§9 索引的漂移形态是条目缺失（非数字错） | 清单比对器（视图枚举集 vs LS/front-matter 枚举集） | RESEARCH A3 |
| 真值源三类可机读（LS / hits 块 / front-matter） | 真值枚举器多通道 → TruthSet 单一汇聚 | RESEARCH A6-A8 |
| 门面层已带时点标注（「时点快照+真值指针」裁决） | 载体两级分类（living/facade）数据化入 stats 块；facade P3 非阻断 | RESEARCH A4 + C3 |
| DIS-010 派生统计口径必须显式（33 处/62% = 六样本分桶求和） | view_layer_samples 口径声明进 stats 块，工具只做声明后算术 | RESEARCH A5 |
| 双工具零拦截 = 覆盖边界（m7_stats 单文件 / dc_validator 单契约），非工具失效 | 第三类职责：跨文件「视图声明 vs 真值」对账，正交不吞并 | RESEARCH A9-A11 + C1 |
| 模式扫描原型已于调研轮人工验证（Grep 全位点 6 行全捕获） | 核心校验循环 = 该 Grep 的脚本化 + 真值注入 | RESEARCH A15 |
| 三件套先例（退出码/selftest/零依赖/hook/围栏块） | 同构继承；**--write 显式不继承**（prose 不可重建） | RESEARCH A12-A14 + B1 |

### 2.2 相关 ADR / 规范

| 文档 | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [ADR-0007 D1](../../adr/ADR-0007-unified-document-contract.md) | M7 唯一活载体 | repo_stats **消费** hits 块（不重复解析样本表）——单一真值源；M7 文件零改动 |
| [FWK-ASSERTION R7](../../docs/ASSERTION_EVIDENCE_FRAMEWORK.md) | 声明 = 机械重数 | I-6 的规则源头；本设计是 R7 从账本端到视图端的外推 |
| [m7-hits-block-DESIGN](../m7-hits-block/M7_HITS_DESIGN.md) | 三件套 + 写守卫 + I-1~I-6 | 工程形态逐项继承；写守卫不适用（无写入面）→ I-1 强化为全模式只读 |
| [precommit-dc-validator-DESIGN §8](../precommit-dc-validator/DESIGN.md) | I-1~I-5 不变式族 | 逐条同构继承 |
| [DIS-010 处置](../../docs/discoveries/README.md) | P-014 + 门面「时点快照+真值指针」 | C3 分级校验与 facade 豁免契约的裁决源头 |
| [PROGRESS P-014](../../docs/PROGRESS.md) | 验收标准原文 | 四件套 + repo_stats.py + stats 块接入 + 第三 hook + 校验对象含修正轮自身——逐一映射（§2.3 / §4 / §8-I-7） |

**与双既有工具零冲突**（RESEARCH A14 边界）：stats 围栏块内文本不触发 dc_validator M5（围栏内链接跳过先例）；CODE_WIKI 无 front-matter、无 §0 统计表，不触发 M2/M4；m7-stats 与 repo-stats 双 hook 独立运行无顺序依赖（hits 块损坏时两者各自声波式报 P1，互不掩盖）。

### 2.3 职责边界

**职责内（本设计回答）**
1. stats 机读块契约校验（存在性 / JSON 合法性 / 模式库 schema / 载体分类 / 口径声明）
2. 真值源枚举：LS 四目录 + hook 计数 + PROGRESS 表 P-号枚举（fs.*）；M7 hits 块读取（hits.*）；docs front-matter 版本提取（doc_registry 登记）
3. 声明=重数第一级：stats 块 declared 各计数 vs 真值机械重数（P1）
4. 模式扫描第二级：living 载体围栏外 prose 命中值 vs 真值（P2）；facade 载体命中值 vs 快照基准（P3）+ 基准 vs 当前真值滞后提示（P3）
5. 清单比对：§2.1 目录树 spec/ 子目录集、§9 spec/*/ 索引链接集 vs LS；§9 版本声明 vs front-matter
6. pre-commit 提交瞬间拦截（对账作用域内任一文件变更即全量对账）

**职责外（不回答——独立范式，不吞并）**
- prose 措辞起草与门面快照刷新时机（人工裁量——工具只对账不代改，RULE-5 单向权限同构）
- M7 表内校验（m7_stats 职责）；DC 契约校验（dc_validator 职责）——双既有工具零改动（C1：verified 状态不重开）
- 历史文档旧值合法性：PROGRESS / M7 / dev-log / spec 四件套 / ADR 是历史记录，合法携带时点值，**不入扫描面**（扫描范围 = 当前态视图载体，RESEARCH §0 扫描范围声明同构）

**能力边界（回答不了——如实声明）**
- 门面快照「曾为真值」不可判定（真值历史序列未存档，RESEARCH B1 边界）——P3 提示是诚实上限，不虚构更强校验
- 模式库漏检新表达形态（prose 措辞演化逃逸旧模式）——模式库是活契约，漏检如实入 M7（样本⑩ grep 盲区同族）
- §2.1 树内缩写文件名（`007_hallucination_audit_...md` 形态）不逐字比对——缩写无稳定锚；只比对目录级条目与全名条目
- 视图层口径（哪些样本属视图载体）是语义归类——stats 块人工声明 `view_layer_samples`，工具只做声明后算术

## 3. 架构设计

### 3.1 整体架构

```
[git commit（对账作用域内任一文件变更）]
    │ 触发（files: 视图载体集 ∪ 真值源集——§3.4 hook 契约）
    ▼
.pre-commit-config.yaml 第三 hook: repo-stats
    │ entry: python scripts/repo_stats.py（verify 模式，无旗标）
    ▼
scripts/repo_stats.py（RS1 CLI）
    ├─ RS3 stats 块解析   ──  CODE_WIKI §10 ```stats（模式库/载体分类/声明/口径/基准）
    ├─ RS2 真值枚举器     ──  LS + hook 计数 + PROGRESS 表 + hits 块 + front-matter → TruthSet
    ├─ RS4 对账引擎       ──  ① 声明=重数（P1） ② 模式扫描（living P2 / facade P3） ③ 清单比对（P2）
    └─ RS5 selftest       ──  内嵌自测（tempfile fixture，不触工作树）

人工维护工作流（对账制——与 m7_stats 的 --write 再生成制相反）:
  真值源前进（新样本/新目录/新文档/新 hook）→ 人工同步视图 prose + stats 块声明
  → python scripts/repo_stats.py（verify）→ commit（hook 复验）
  工具永不代改、只报偏差；声明（stats 块）与执行（prose 位点）由同一工具对账
  ——⑳轮「修正的声明与修正的执行分离」的对症结构
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| RS1 CLI | 旗标解析（--selftest / 文件参数）/ 对账作用域判定 / 聚合 / 退出码 | argv | Summary + exit code | RS2-RS5 |
| RS2 真值枚举器 | TruthSet 构建：fs 计数（spec 特征目录 / adr / dev-log / scripts / templates / hooks / P-号）+ hits + dis_range + fm 版本 | 文件系统 + M7 + front-matter | TruthSet | 无 |
| RS3 stats 块解析 | ```stats JSON → PatternSpec / 载体分类 / DeclaredStats / 口径 / FacadeBaseline + 结构校验 | CODE_WIKI 文本 | (Spec, list[CheckResult]) | 无 |
| RS4 对账引擎 | 三路对账 + 围栏外过滤 + 数字形态转换（中文数字 / 带圈数字 / EN 变体） | TruthSet + Spec + 载体文本 | list[CheckResult] | RS2/RS3 |
| RS5 selftest | fixture 全覆盖自测（expect 自增机械计数） | — | exit code | RS1-RS4 |

### 3.3 数据流

1. verify（唯一对账运行模式）：读 CODE_WIKI stats 块（RS3）→ 构 TruthSet（RS2）→ 三路对账（RS4）→ CheckResult 聚合 → 退出码（任一 P1/P2 即 1；仅 P3 为 0）
2. pre-commit：staged 文件 ∩ 对账作用域 ≠ ∅ → **全量对账**（视图漂移本质是跨文件：spec/ 前进影响 CODE_WIKI，不做增量）；∩ = ∅ → skip（exit 0）
3. `--selftest`：tempdir 构造 fixture 矩阵（迷你仓：假 stats 块 + 假真值源 + 假载体），不触工作树

### 3.4 控制流（关键分派）

```
main()
  if --selftest: return run_selftest()
  staged = argv.files
  if staged and not (staged ∩ 对账作用域): return 0     # pre-commit skip 语义
  spec, r0   = parse_stats_block(CODE_WIKI)             # RS3（结构性 P1 在此产生）
  truth      = build_truth_set()                        # RS2（真值源损坏 → 声波式 P1）
  results    = reconcile(spec, truth)                   # RS4 三路对账
  exit(0 if 无 P1/P2 else 1)                            # P3 打印可见不阻断
```

**hook 契约**（`.pre-commit-config.yaml` 追加第三个 local hook）：

```yaml
- id: repo-stats
  name: View-layer enumeration reconciler
  entry: python scripts/repo_stats.py
  language: system
  files: ^(CODE_WIKI\.md|README(\.en)?\.md|\.pre-commit-config\.yaml|docs/|spec/|adr/|scripts/)
```

> files 设计理由（RESEARCH A13 收窄先例的**受限扩展**）：真值前进分散在 spec/、adr/、docs/dev-log/、scripts/、配置与账本——任一处前进都使视图漂移，触发集必须覆盖真值源全集；对账为全量只读（毫秒级），广触发无性能代价；skip 分支保住非相关提交零噪音。

## 4. stats 机读声明块契约（核心数据契约）

### 4.1 块形态与落位

- 落位：CODE_WIKI.md 末尾新 §10（`## 10. 机读声明块（stats）`），不重排 §1-§9（保护既有跨文档引用与行号锚）
- 围栏：```` ```stats ```` + JSON 对象（先例：```rules / ```assertions / ```hits，RESEARCH A14）
- 全文唯一：stats 围栏块在 CODE_WIKI 内必须恰好一个（多块/缺块均 P1）

### 4.2 字段集

| 字段 | 类型 | 语义 | 性质 |
|------|------|------|------|
| `pattern_lib_version` | int | 模式库版本（模式增删/修改时人工递增） | 声明（历史事实式版本号） |
| `carriers` | object | 载体两级分类 `{living: [...], facade: [...]}`——C3 分级裁决的数据化 | 声明 |
| `patterns` | array | 模式库 `[{id, regex, truth, scope}]`（scope 缺省 = 全载体；命中严重性由载体分类决定） | 声明（**数据非代码**，I-4） |
| `declared` | object | 实体计数声明 `{spec_feature_dirs, adr_files, dev_logs, scripts, templates, hooks, progress_tasks}` | **= 机械重数**（I-6 第一级） |
| `view_layer_samples` | array | 视图层口径追溯声明：贡献了视图载体分桶行的样本号（当前 [11,16,17,18,19,20]）——**非求和基础**（样本级求和会把样本⑪ 的 DEV-LOG-004/PROGRESS 两处非视图错误计入，v1.1 修正） | 声明（语义归类，人工） |
| `doc_registry` | array | 版本对账登记 `[{label, path}]`（§9 索引行 prose 称谓 → front-matter 文档路径） | 声明 |
| `facade_baseline` | object | 门面快照基准 `{carrier: {as_of, values: {truth_key: 值}}}` | 声明（历史事实，同 pre_ledger 性质） |
| `suppress` | array | 误报白名单 `[{pattern_id, file, note}]`（显式登记非静默；初版为空） | 声明 |

**禁止字段**：时间戳（生成态）/ git hash / declared 之外可从真值机械重数的数字副本。

**truth 绑定集**（patterns.truth 合法值，封闭枚举）：

| 绑定 | 真值来源 | 重数方式 |
|------|---------|---------|
| `fs.spec_feature_dirs` | LS `spec/` 排除 `templates` | 目录计数 |
| `fs.adr_files` / `fs.dev_logs` / `fs.scripts` / `fs.templates` | LS `adr/` / `docs/dev-log/` / `scripts/*.py` / `spec/templates/*.md` | 文件计数 |
| `fs.hooks` | `.pre-commit-config.yaml` | `- id:` 行计数 |
| `fs.progress_tasks` | `docs/PROGRESS.md` 待办表 | `^\| P-\d{3} \|` 行计数 |
| `hits.samples` / `hits.form2_total` | M7 §5 hits 块 | 字段直读（m7_stats 看护其准确性——单一真值源，不重复解析样本表） |
| `dis.range_min` / `dis.range_max` | discoveries/README 索引表 | DIS-\d{3} 编号 min/max |
| `derived.view_layer_total` | M7 §2 分桶表载体列匹配视图载体模式集（CODE_WIKI / README / evidence.svg——固定于枚举器语义，同「spec/ 排除 templates」性质）的行小计求和 | 枚举器重数（v1.1 修正口径） |
| `derived.view_layer_pct` | floor(100 × view_layer_total / hits.form2_total) | 声明后算术 |

### 4.3 模式库初版（PT-1~PT-11，实施期全仓试扫定稿）

| id | regex（示意，实施定稿） | truth | 备注 |
|----|------------------------|-------|------|
| PT-1 | `形态 II [^。\n；]{0,20}?(\d+) 处` | hits.form2_total | 有界惰性间隙容纳「分桶 53 处」「复发分桶（53 处/…」等变体 |
| PT-2 | `样本\s?①[–-]` + 带圈字符捕获组 | hits.samples | 带圈数字映射（1-20 U+2460+，21-35 U+3251+）；EN 变体（README.en `samples ①–⑳`）实施期同库登记。精确字面量于 Step 9 起草 stats 块时登记（表内 `](` 相邻形态与 markdown 链接语法撞车，示意列改述——dc_validator M5 拦截实录，2026-08-22） |
| PT-3 | `DIS-(\d{3})~(\d{3})` | dis.range_min/max | 双捕获组对账 |
| PT-4 | `([一二三四五六七八九十]+|\d+) feature 目录` | fs.spec_feature_dirs | 中文数字转换（⑳轮 L4「九→十」活靶） |
| PT-5 | `dev-log ×(\d+)` | fs.dev_logs | |
| PT-6 | `ADR-(\d{4})~(\d{4})\s*(\S+?)份` | fs.adr_files | 中文数字份数；README 双语变体（`×6` / `Six ADRs`）实施期登记 |
| PT-7 | `(\d+) 个模板` | fs.templates | README 变体（`5 templates` / `五份` / `Five`）实施期登记 |
| PT-8 | `(双|两|三|四) hook` | fs.hooks | 中文数字 hook 数（repo-stats 入册后「双」→「三」） |
| PT-9 | `视图层合计 (\d+) 处` | derived.view_layer_total | DIS-010 派生统计（A5 口径） |
| PT-10 | `占形态 II 总量 (\d+)%` | derived.view_layer_pct | 同上 |
| PT-11 | `P-(\d{3})~P-(\d{3})` | fs.progress_tasks | 声明区间上限须 = 真值最大号（P-014 登记后 L67/L630「P-001~P-013」活靶） |

> 模式库三原则：① **锚定上下文词**（`形态 II` / `样本①-` / `feature 目录` 前缀限定）——prose 元描述（描述替换动作的文字必然含被替换字符串）靠锚定 + suppress 白名单双防护（改名复核语义甄别教训，RESEARCH §6.3）；② **EN 表达变体**（README.en.md `53 logged recurrences of Pattern II` 等）为独立模式条目，实施期全仓试扫补全；③ **SVG 载体不走 prose 模式**——门面基准用 `>N<` 文本节点包含性检查（图形布局无稳定锚，RESEARCH A4 边界）。

### 4.4 校验规则集（check_id × 严重性）

| check_id | 规则 | 严重性 |
|----------|------|--------|
| `rs-stats` | stats 块存在且恰一个、JSON 可解析 | P1 |
| `rs-stats` | patterns 非空、regex 可编译、truth ∈ 绑定集、scope ⊆ 载体集；declared 键集完整；carriers 两级非空且互斥 | P1 |
| `rs-truth` | hits 块可解析（消费前提）；doc_registry 文档 front-matter 可解析；LS 四目录存在 | P1（声波式：真值源坏 ≠ 校验通过） |
| `rs-decl` | declared 各计数 = TruthSet 机械重数（逐字段报 declared/actual） | P1 |
| `rs-decl` | view_layer_total = 分桶表视图载体行求和（**非**样本形态II列求和——v1.1 修正）；pct = floor(100×total/form2_total) | P1 |
| `rs-pattern` | living 载体：围栏外命中值 ≠ 真值 | P2 |
| `rs-pattern` | facade 载体：命中值 ≠ facade_baseline 声明值（prose 与基准漂移） | P3 |
| `rs-pattern` | facade_baseline ≠ 当前真值（快照滞后，信息性提示） | P3（非阻断） |
| `rs-list` | §2.1 树 spec/ 子目录集 = LS（缺登/幻影双向） | P2 |
| `rs-list` | §9 spec/*/ 索引链接集 = LS（缺行/幻影行） | P2 |
| `rs-list` | §9 文档版本声明（doc_registry 登记）vs front-matter version | P2 |

> P3 语义与 m7_stats 同族（非阻断但打印可见）；差异：本工具 P3 承载门面快照滞后（合法时点态）与基准/prose 漂移两类——facade 的阻断压力由 P3 档位显式豁免（C3 裁决），非静默跳过。

### 4.5 首次落地（bootstrap）

CODE_WIKI 现无 stats 块。流程：人工起草 §10 初版（模式库 PT-1~PT-11 + declared 真值 + view_layer_samples + doc_registry + facade_baseline）→ `python scripts/repo_stats.py` 首跑——**预期捕获现存活漂移**（§10.3 已知活靶清单）→ 人工修正视图与声明至全绿 → 捕获集入 CHECKLIST 验收登记。与 m7_stats `--seed-pre-ledger` 的差异：stats 块全部字段为人工声明（无推导型基线），无需 seed 通道——首跑对账本身就是 bootstrap 的验收（工具有效性以捕获真实漂移为证，非以全绿为证）。

## 5. 替代方案

### 5.1 方案 A：独立脚本 + 独立第三 hook + stats 机读块（选择）

- 描述：`scripts/repo_stats.py`（verify / --selftest）+ `.pre-commit-config.yaml` 追加 repo-stats hook + CODE_WIKI §10 stats 块
- 优点：职责分离（第三类对账职责，双既有工具零改动）；模式库数据化（演化走 stats 块编辑 + pattern_lib_version 递增，可追溯）；对账制与 B1 推理链自洽
- 缺点：三 hook 三脚本心智成本（微小——退出码/用法/零依赖全同构）
- 选择理由：RESEARCH C1（职责分离/审查面冻结）+ C2（扫描制）+ B1（对账制）三链合流

### 5.2 方案 B：并入 dc_validator 作 M6 检查（否决）

- 否决理由：跨文件对账（视图 ↔ 真值源）与单文件契约校验是不同范式；并入则每次模式库/真值源演化连带重开 P-008 审查面，收益为零（RESEARCH C1，m7-hits §5.2 同族裁决）

### 5.3 方案 C：位点登记制（登记文件+行号+期望值）（否决）

- 否决理由：行号漂移固有缺陷（样本⑧ 前科）+ 新副本位点逃逸（⑲ 凭记忆选点必漏实证——CODE_WIKI 4 副本结构下位点集不可穷举，RESEARCH A1/C2）

### 5.4 方案 D：--write 重生成视图数字（否决）

- 否决理由：prose 不可机械重建（B1）；自动改 prose 违反对账制纪律与 RULE-5 单向权限（审计者永不自动修复）；⑳轮证明修正轮自身需被**对账**而非被自动化——自动修复会掩盖「声明与执行分离」这一被测失效形态本身

### 5.5 方案 E：只覆盖 CODE_WIKI，不纳入 README/SVG/discoveries（否决）

- 否决理由：⑰轮 evidence.svg「6 轮/11 处」双数字漂移实证图形资产在 prose grep 视野外同为载体；⑲④ DIS-010 条目派生统计漂移实证聚合索引也是载体——只守 CODE_WIKI 等于把 DIS-010 的载体面裁剪一半（论证驱动归因扭曲，Step 4 检查项）

### 5.6 方案 F：模式库硬编码于脚本、无 stats 块（否决）

- 否决理由：I-4 单一真值源（数据非代码）——模式演化须显式登记且可追溯（pattern_lib_version）；静默改代码常量 = 在代码层新增一个无对账的缓存失效面（与 DIS-010 同构问题复发）

## 6. 数据结构

```python
@dataclass(frozen=True)
class CheckResult:
    check_id: str      # "rs-stats" | "rs-truth" | "rs-decl" | "rs-pattern" | "rs-list"
    file: str
    severity: str      # "P1" | "P2" | "P3" | ""（空 = skip）
    message: str       # 含 pattern_id / declared / actual 可核对信息
    line: int | None

@dataclass(frozen=True)
class PatternSpec:
    pid: str           # "PT-1"...
    regex: re.Pattern
    truth: str         # 绑定集键
    scope: tuple[str, ...]   # 载体相对路径；空 = 全载体

@dataclass(frozen=True)
class DeclaredStats:   # declared 字段的强类型镜像
    spec_feature_dirs: int
    adr_files: int
    dev_logs: int
    scripts: int
    templates: int
    hooks: int
    progress_tasks: int

@dataclass(frozen=True)
class FacadeBaseline:
    carrier: str
    as_of: str         # "2026-08-22"（历史事实声明，非生成态时间戳）
    values: dict       # {truth_key: int}

@dataclass
class TruthSet:        # 全部字段 = 机械重数（RS2 产出）
    fs: dict[str, int]           # 与 DeclaredStats 同键
    hits: dict[str, int]         # samples / form2_total
    dis_range: tuple[int, int]
    view_layer_total: int        # 分桶表视图载体行求和（v1.1 修正口径）
    view_layer_pct: int          # floor(100 × total / form2_total)
```

数字形态转换（RS4 内部，纯函数）：中文数字（一~十、十一~九十九简单合成）/ 带圈数字（①-㉟ 三段 Unicode 区间）/ 阿拉伯数字 → 统一 int 后与 TruthSet 比较。转换函数全区间 selftest 用例覆盖（1-35 逐值）。

## 7. 错误处理

| 错误场景 | 处理方式 | 退出码 | 用户可见信息 |
|---------|---------|-------|------------|
| stats 块缺失/多块/JSON 非法 | P1（契约损坏，声波式） | 1 | `[P1] CODE_WIKI stats 块缺失/非唯一/不可解析` |
| 模式 regex 非法 / truth 绑定越界 / scope 越界 | P1 | 1 | pattern_id + 原因 |
| hits 块不可读（M7 损坏） | P1（不静默——真值源坏 ≠ 通过；m7_stats 为第一看护者） | 1 | `[P1] hits 块不可解析` |
| front-matter 解析失败（doc_registry 内文档） | P1 | 1 | 文档路径 + 原因 |
| LS 目录缺失（spec/ 等被删） | P1 | 1 | 目录路径 |
| living 模式命中值 ≠ 真值 | P2 逐位点报告 | 1 | pattern_id + 文件:行 + declared/actual |
| facade 滞后 / 基准漂移 | P3（不阻断） | 0 | 同上格式，标注 `快照滞后（as_of=…）` |
| 未知异常（IO 等） | 顶层 try/except | 2 | stderr `[tool-error]` |
| staged 与对账作用域无交集 | skip | 0 | `[skip] 非对账作用域目标` |

**退出码语义（与 dc_validator / m7_stats 逐字一致）**：`0`=通过（含仅 P3）；`1`=发现 P1/P2；`2`=工具自身错误。

## 8. 不变式（Invariants）

1. **I-1 全模式只读**：verify 与 selftest 均零写入——比 m7_stats 更严（其有显式 --write）；本工具无任何写通道，对账制无重生成面（B1）
2. **I-2 确定性**：同仓库态 → 输出逐字节确定；无时间戳/随机/网络/git 状态依赖；双跑逐字节一致入 selftest
3. **I-3 零新规则**：只机器化既有维护意图（CODE_WIKI 头注「当前态」同步义务 + DIS-010 处置裁决 + C3 分级）；不发明新登记义务（如强制 prose 措辞模板）
4. **I-4 单一真值源**：模式库/载体分类/口径/基准 = stats 块数据（代码零模式常量）；真值 = LS/hits/front-matter/PROGRESS 表；模式变更 = stats 块编辑 + pattern_lib_version 递增，代码不动
5. **I-5 异构于生成端**：纯机械正则/枚举/算术，无 LLM、无语义判断（语义归类——视图层口径——以声明形式由人工前置）
6. **I-6 声明 = 重数（R7 视图层外推，两级）**：第一级 stats declared vs 真值重数（P1）——声明层错在此拦；第二级 prose 模式值 vs 真值（P2/P3）——副本层错在此拦
7. **I-7 修正轮产出自身在扫描范围内**（⑳轮新证，本设计新增）：版本头叙事中的统计数字是视图（声明性修正的载体）；repo_stats 自身的入册描述（hook 数/脚本数）同受 PT-8 等模式看护——工具描述自身也被工具对账（自举）

## 9. 幻觉排除审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 设计决策可追溯 RESEARCH（§2.1 映射表 8 行逐一引用；B1/C1/C2/C3 判断全部落设计决策）——自查（单视角）
- [x] 无未验证假设进入契约（H1 模式可穷举 → §4.3 模式库初版 + 实施期全仓试扫误报/漏报双清单验收；H2 front-matter 对账 → doc_registry 机制 + 实施期 PoC；H3 P3 足以维持快照卫生 → 落地后两 feature 周期观察，挂 CHECKLIST）
- [x] 无论证驱动的归因扭曲（载体面不裁剪——方案 E 否决即此审查的产物；误报不静默——suppress 显式登记）

### 9.2 替代方案审查

- [x] 五个替代方案（B/C/D/E/F）各有明确否决理由且与 M7 实证自洽（C↔样本⑧⑲；D↔⑳轮；E↔⑰⑲④；F↔DIS-010 同构论证）

### 9.3 职责边界审查

- [x] 职责边界清晰（§2.3）：prose 起草归人工、M7 表内归 m7_stats、DC 契约归 dc_validator、历史文档合法旧值出扫描面
- [x] 不越界：双既有工具零改动；不吞并通用化议题（跨仓视图对账属未来触发条件后议题）

> **标注（RULE-1/RULE-4）**：本 §9 由同会话自查勾选（单视角）；独立 pass 待 Step 10 或用户触发，届时以独立结论为准。

## 10. 对实施的输入

### 10.1 关键工程约束

1. Windows：entry `python scripts/repo_stats.py`（python 前缀先例，RESEARCH A13）；路径 os.path，ROOT 推导同 dc_validator
2. 零第三方依赖（stdlib：argparse/re/os/sys/json/dataclasses/tempfile）
3. 代码量预估 ~600 行（±200；**实施时在 IMPLEMENTATION §10 记录实际 LOC**——P-008 P3③ 教训：DESIGN LOC 预估必须实施核对；m7_stats 预估 300 实际 828 的校准教训计入区间宽度）
4. selftest expect 计数自增（DR-6 同构：计数不手填）；fixture 覆盖：模式命中/失配 × living/facade、数字形态转换全区间、清单比对缺登/幻影、声明失配、结构性 P1、skip 语义、确定性双跑
5. stats 块起草与 CODE_WIKI 修正用 Edit 工具（user_profile Operational Safety Rules——.md 大文件禁 PowerShell 管道）

### 10.2 集成顺序（Step 9 内）

1. `scripts/repo_stats.py` TDD 实现（selftest 先行）→ 2. CODE_WIKI §10 stats 块人工起草 → 3. verify 首跑捕获活靶 → 4. 视图修正（含 CODE_WIKI v1.7 入册：三 hook / repo_stats 可执行件 / §9 补 repo-stats 行）→ 5. `.pre-commit-config.yaml` 第三 hook 入册 → 6. 终验全绿（三校验器 + `pre-commit run --all-files`）

### 10.3 已知活靶（verify 首跑预期捕获集——E1 取证于本设计撰写轮）

| # | 位点 | 现值 | 真值 | 对应规则 |
|---|------|------|------|---------|
| 1 | CODE_WIKI §9 缺 `spec/repo-stats/` 索引行 | 缺行 | 10 目录（LS） | rs-list |
| 2 | CODE_WIKI L627「断言分级证据框架 v1.4」 | v1.4 | front-matter 1.4.2 | rs-list（版本对账） |
| 3 | CODE_WIKI L67/L630「P-001~P-013」 | 013 | P-014（PROGRESS 表） | rs-pattern PT-11 |
| 4 | CODE_WIKI L4/L5「双 hook」（repo-stats 入册后） | 双 | 三 | rs-pattern PT-8 |
| 5 | discoveries DIS-010「视图层合计 33 处/62%」 | 33/62% | 33/62%（当前自洽——回归确认项） | rs-decl + PT-9/10 |

> 活靶 1-3 为现存漂移（本设计撰写轮 LS/Grep/Read 取证：§9 表 L615-L646 无 repo-stats 行 / front-matter Grep `^version:` 实 1.4.2 / PROGRESS 表 P-014 在册）；4 为集成动作自身产生的预期漂移（hook 入册与视图同步同 commit 完成）；5 为当前自洽值的回归锚。**首跑按序捕获 1-3（4 在 hook 入册后由复跑捕获）= 工具有效性首次实证，捕获集入 CHECKLIST；若首跑全绿反而证伪扫描器（活靶在手，全绿即漏检）**。

### 10.4 风险与缓解

| 风险 | 缓解 |
|------|------|
| 模式库漏检（新表达形态逃逸，样本⑩ 同族） | pattern_lib_version 版本化 + 漏检如实入 M7（活契约非银弹）；suppress 白名单显式登记 |
| 正则误报（prose 元描述含被描述数字——改名复核教训） | 锚定上下文词 + 有界间隙 + suppress 白名单（显式非静默） |
| 扫描器自身计数错（规律②——样本⑨ 校验器前科） | selftest expect 自增 + I-7 自举（工具自身描述位点入扫描范围） |
| 真值源解析漂移（front-matter 格式演化 / hits 字段扩展） | 声波式 P1（解析失败 ≠ 通过）；doc_registry/绑定集封闭枚举，扩展走 stats 块 + pattern_lib_version |
| 中文数字/带圈数字转换错（十一以上合成、㉑ 以上区间） | 转换函数纯函数化 + selftest 全区间用例（1-35 逐值） |

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）
