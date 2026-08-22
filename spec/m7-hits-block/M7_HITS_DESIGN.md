# 设计文档：M7 hits 机读块 + 样本登记脚本化

---
id: m7-hits-block-DESIGN
type: design
version: 1.0
status: draft
date: 2026-08-21
depends: [m7-hits-block-RESEARCH, SPEC-PROCESS, ADR-0007, precommit-dc-validator-DESIGN]
upstream: null
---

> **Feature**: m7-hits-block（PROGRESS P-011）
> **创建日期**: 2026-08-21
> **状态**: draft（草稿）
> **Spec 步骤**: Step 3-4
> **基于调研**: [M7_HITS_RESEARCH.md](./M7_HITS_RESEARCH.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验

---

## 1. 设计目标

把 M7 证据账本的聚合统计（样本数 / 形态 II 分桶算术 / 跨表对账 / P 分级汇总）从**手工登记**变成 **hits 机读块声明 + 机械重数校验**，并把校验前移到提交瞬间（pre-commit）。直接命中的失效模式是 M7 账本自身实证的：登记计数错误的账本，其统计恰是形态 II 计数桶的最顽固载体（RESEARCH B1）。

产出两件：① `docs/M7_EVIDENCE_LOG.md` 新增 §5 ```hits 机读块（统计的唯一声明处）；② `scripts/m7_stats.py`（校验 / 重生成 / 自测三模式）+ pre-commit 第二 hook。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| M7 可机械重数统计面 = 样本行数 / 分桶行列算术 / 跨表对账 / P 汇总（A1-A6） | hits 块字段集 = samples / form2_by_field / form2_total / form2_pre_ledger / form2_from_samples / findings | RESEARCH §3.1 |
| 历史数据两处非整齐形态（样本③ 非标准、样本⑨ 未标级） | 契约如实容纳：cells_nonstandard / unlabeled 为声明字段，禁止回改历史 | RESEARCH A5/A6 |
| dc_validator 已定型退出码 / selftest / 零依赖 / pre-commit 通道先例 | 三件套同构继承；entry 用 `python` 前缀 | RESEARCH A7/A8 |
| 机读围栏块先例 ```rules / ```assertions 均 JSON | ```hits 沿用围栏语言标注 + JSON | RESEARCH A9 |
| R7 不覆盖 M7、M5 跳过围栏内链接 | 独立脚本 + 独立 hook，与 dc_validator 零冲突 | RESEARCH A10/A11 |
| 三处计数风险面 = 形态 II 既有复发位点 | 校验项集合即按三风险面设计（行结构 / 行列算术 / 跨表不变式） | RESEARCH B1 |

### 2.2 相关 ADR / 规范

| 文档 | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [ADR-0007 D1](../../adr/ADR-0007-unified-document-contract.md) | M7_EVIDENCE_LOG.md 为 M7 数据唯一活载体 | hits 块落 M7 文件内（不另建数据文件）；本设计不改变"唯一载体"裁决，只是给载体加机读层 |
| [FWK-ASSERTION R7](../../docs/ASSERTION_EVIDENCE_FRAMEWORK.md) | §0 统计表计数 = 机械重数 | 不变式 I-6（声明 = 重数）的规则源头；hits 块是 R7 原则在非 §0 载体上的同构延伸 |
| [precommit-dc-validator-DESIGN §8](../precommit-dc-validator/DESIGN.md) | I-1~I-5 不变式族 | 本设计不变式族（I-1~I-6）逐条同构继承 + 新增 I-6 |
| [PROGRESS P-011](../../docs/PROGRESS.md) | 验收标准原文 | "统计可脚本重数/生成 + 样本追加脚本辅助 + 与 dc_validator R7 衔接"三要求逐一映射（§2.3） |

### 2.3 职责边界

**职责内（本设计回答）**
1. M7 §1 样本登记表的行结构校验（编号连续 / 日期合法 / 列数 / 形态II复发前导整数）
2. M7 §2 分桶表的行列算术校验（每行小计 = 行和；合计行 = 列和；合计小计 = 总和）
3. 跨表对账不变式：分桶合计 = pre_ledger 基线 + 样本"形态II复发"列之和
4. P 分级汇总抽取（p1/p2/p3 + unlabeled + cells_nonstandard，如实容纳历史非整齐形态）
5. hits 块声明 = 机械重数对账（R7 同构）；--write 确定性重生成
6. pre-commit 提交瞬间拦截（M7 文件变更时）

**职责外（不回答——独立范式，不吞并）**
- 样本行 / 分桶行的**语义内容**起草与归类判断（载体描述、字段类型归类）——人工职责（RESEARCH C3）
- M7 §3 命中率 baseline 表的对账——该表为外部快照（Cpp_Hub Phase 5），非本仓可重数数据
- 其他文档的统计块校验——hits 契约仅绑定 M7 载体；通用化属未来触发条件后议题

**能力边界（回答不了——如实声明）**
- pre_ledger 基线（6）是历史事实声明，非可推导量——首次落地须人工显式 seed（--seed-pre-ledger），此后由对账不变式持续看护
- 分桶行与样本行的**逐行对应关系**（哪行分桶对应哪个样本）语义上可对但格式上无稳定锚——不逐行对账，只做总量对账（总量失衡已能拦截"加样本忘加分桶"主失效模式）

## 3. 架构设计

### 3.1 整体架构

```
[git commit（M7_EVIDENCE_LOG.md 变更）]
    │ 触发（files: ^docs/M7_EVIDENCE_LOG\.md$）
    ▼
.pre-commit-config.yaml 第二 hook: m7-stats
    │ entry: python scripts/m7_stats.py（verify 模式，无旗标）
    ▼
scripts/m7_stats.py（MH1 CLI）
    ├─ MH2 样本表解析   ──  §1 行结构 + 形态II列 + P 抽取
    ├─ MH3 分桶表解析   ──  §2 行列算术 + 合计
    ├─ MH4 统计/对账    ──  Stats 计算 + 跨表不变式 + hits 块声明对账 + 序列化
    └─ MH5 selftest     ──  内嵌自测（tempfile fixture，不触工作树）

人工登记工作流（脚本辅助，C3 边界）:
  手工追加样本行 [+ 分桶行] → python scripts/m7_stats.py --write
  （校验先行：结构/算术/不变式全过才允许重写 hits 块）→ commit（hook 复验）
```

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| MH1 CLI | 旗标解析（--write / --selftest / --seed-pre-ledger / 文件参数）/ 聚合 / 退出码 | argv | Summary + exit code | MH2-MH5 |
| MH2 样本表解析 | §1 表 → SampleRow 列表 + 行结构校验结果 | M7 文本 | (rows, list[CheckResult]) | 无 |
| MH3 分桶表解析 | §2 表 → BucketRow 列表 + 行列算术结果 | M7 文本 | (rows, list[CheckResult]) | 无 |
| MH4 统计与对账 | Stats 计算 / 跨表不变式 / hits 声明对账 / 确定性序列化 | rows + M7 文本 | (Stats, list[CheckResult], str) | MH2/MH3 |
| MH5 selftest | fixture 全覆盖自测（expect 自增机械计数） | — | exit code | MH1-MH4 |

### 3.3 数据流

1. 默认（verify）：读 `docs/M7_EVIDENCE_LOG.md` → MH2/MH3 解析两表 → MH4 计算 Stats + 跨表不变式 + 与 hits 块声明对账 → 全部 CheckResult 聚合 → 退出码
2. `--write`：先跑全部校验；**仅 hits 声明失配（check_id=hits）不阻断**，其余任一 P1/P2 即拒绝写入（写守卫：绝不把失衡账本编码进 hits 块）；全过后用重数值重写 §5 围栏块内容
3. `--selftest`：tempdir 构造 fixture 矩阵，不触工作树
4. pre-commit：传入 staged 文件名，非 M7 文件即 skip（exit 0）；M7 文件走 verify

### 3.4 控制流（关键分派）

```
main()
  if --selftest: return run_selftest()
  targets = argv.files ∩ {docs/M7_EVIDENCE_LOG.md}   # pre-commit 语义
  if not targets and argv.files: return 0            # staged 无 M7 → skip
  target = targets[0] or "docs/M7_EVIDENCE_LOG.md"   # 无参默认即 M7
  rows_s, r1 = parse_sample_table(text)              # MH2
  rows_b, r2 = parse_bucket_table(text)              # MH3
  stats, r3, hits_declared = compute_and_compare()   # MH4（含不变式 + hits 对账）
  if --write:
      blocking = [r for r in all_results if r.check_id != "hits" and r.severity in (P1,P2)]
      if blocking or hits_declared is None and no --seed-pre-ledger: 拒绝写入, exit 1
      rewrite §5 block (seed: pre_ledger = --seed-pre-ledger if block missing)
  exit(0 if 无 P1/P2 else 1)
```

> **写守卫语义（本设计新增，dc_validator 无此形态）**：dc_validator 是纯只读校验器（I-1）；本工具因承担"重生成"职责，采用**默认只读 + 显式 --write + 写前校验先行**——--write 不是绕过校验的通道，而是校验通过后的机械落盘。

## 4. hits 机读块契约（核心数据契约）

### 4.1 块形态与落位

- 落位：M7_EVIDENCE_LOG.md 末尾新 §5（`## 5. 机读统计块（hits）`），不重排既有 §1-§4（保护既有跨文档引用）
- 围栏：```` ```hits ```` 围栏 + JSON 对象（先例：```rules / ```assertions，RESEARCH A9）
- 全文唯一：hits 围栏块在 M7 内必须恰好一个（多块/缺块均 P1）

### 4.2 字段集（全部字段 = 机械重数值，I-6）

| 字段 | 类型 | 语义 | 重数来源 |
|------|------|------|---------|
| `samples` | int | 样本登记表数据行数 | §1 行计数 |
| `form2_by_field` | object | 7 字段类型 → 合计数（键序：version/section/constant/line/count/quote/mapping ↔ 版本号/章节号/数值常量/行号/计数/转述引文/映射闭合） | §2 合计行各列 |
| `form2_total` | int | 形态 II 总数 | §2 合计行小计 |
| `form2_pre_ledger` | int | 先于账本的历史基线（当前 = Phase 7C 行小计） | **声明值**（历史事实，非推导量；由不变式看护） |
| `form2_from_samples` | int | 样本"形态II复发"列前导整数之和 | §1 该列求和 |
| `findings.p1/p2/p3` | int | 发现列 P 标记计数汇总（`(\d+)\s*P[123]` 抽取） | §1 发现列 |
| `findings.unlabeled` | int | 前导总数 − P 标记和的差额累计（未标级发现，样本⑨ 形态） | §1 发现列 |
| `findings.cells_nonstandard` | int | 无前导总数且无 P 标记的单元格数（样本③ 形态） | §1 发现列 |

**禁止字段**：时间戳 / git hash / 任何非确定值（RESEARCH C2）；冗余可推导字段（如 findings 总和）。

### 4.3 校验规则集（check_id × 严重性）

| check_id | 规则 | 严重性 |
|----------|------|--------|
| `m7-sample` | 样本编号 = 1..N 连续无重复 | P1 |
| `m7-sample` | 行列数 = 7 | P1 |
| `m7-sample` | 日期格式 YYYY-MM-DD 且日历合法 | P2 |
| `m7-sample` | "形态II复发"列有前导整数 | P1 |
| `m7-sample` | 发现列 P 标记和 > 前导总数 | P1 |
| `m7-sample` | 发现列非标准（无前导总数且无 P 标记） | P3（非阻断，计入 cells_nonstandard） |
| `m7-bucket` | 数据行小计 = 7 字段格之和 | P1 |
| `m7-bucket` | 合计行各列 = 上方各列竖加之和 | P1 |
| `m7-bucket` | 单元格 ∈ {非负整数, —} | P1 |
| `m7-xtable` | form2_total = form2_pre_ledger + form2_from_samples | P1 |
| `m7-hits` | 块存在且恰一个、JSON 可解析 | P1 |
| `m7-hits` | 各声明字段 = 机械重数值（逐字段报 declared/actual） | P1 |

> P3 语义（与 dc_validator 的差异点，如实声明）：本工具引入非阻断 P3 档承载"历史非整齐形态的如实计数"——P1/P2 才影响退出码；P3 行打印可见但不阻断（防止历史数据永久性挡提交，同时保住可见性）。

### 4.4 首次落地（bootstrap）

M7 现无 hits 块。流程：`python scripts/m7_stats.py --write --seed-pre-ledger 6`——基线 6 由人工显式声明（= Phase 7C 行小计，RESEARCH A3 取证核对），工具拒绝无 seed 的盲写（防静默把当前缺口烤进基线）。此后 pre_ledger 只从块内声明读取。

## 5. 替代方案

### 5.1 方案 A：独立脚本 + 独立 pre-commit hook（选择）

- 描述：`scripts/m7_stats.py`（三模式）+ `.pre-commit-config.yaml` 追加 m7-stats hook（files 收窄至 M7 路径）
- 优点：职责分离（dc_validator 保持 verified 状态零变更）；M7 表格式演化不影响通用工具；R7 同构原则共享
- 缺点：两 hook 两脚本的心智成本（微小——退出码/用法同构）
- 选择理由：RESEARCH C1 三链（职责分离 / 审查面冻结 / "衔接"语义）

### 5.2 方案 B：并入 dc_validator 作 M6 检查（否决）

- 描述：dc_validator 增加 --check-m7-hits，M7 解析逻辑入通用校验器
- 否决理由：单文件特化逻辑（M7 表结构耦合）进全仓通用工具，每次 M7 表演化连带变更 verified 工具并重开 P-008 审查面；收益为零

### 5.3 方案 C：CI / 事后脚本承载（否决）

- 否决理由：事后拦截与"提交瞬间前移"目标相反；单人本地仓 CI 属过度工程（同 [precommit DESIGN §5.2](../precommit-dc-validator/DESIGN.md) 先例裁决）

### 5.4 方案 D：只加 hits 块、不做脚本（否决）

- 描述：M7 手工维护 hits 块，无重数器
- 否决理由：**手填统计块 = 样本⑫ 同款失效模式的新实例**（计划数与实际数漂移——先填旧值、正文追加样本后忘回写）；无重数器的声明块比无块更危险（伪机读外衣）。P-011 验收标准明文要求"统计可脚本重数/生成"

## 6. 数据结构

```python
@dataclass(frozen=True)
class CheckResult:
    check_id: str      # "m7-sample" | "m7-bucket" | "m7-xtable" | "m7-hits"
    file: str
    severity: str      # "P1" | "P2" | "P3" | ""（空 = skip）
    message: str       # 含 declared/actual 可核对信息
    line: int | None

@dataclass(frozen=True)
class SampleRow:
    num: int           # 样本号
    date: str
    findings: str      # 发现列原文
    form2_count: int   # 形态II复发前导整数

@dataclass(frozen=True)
class Stats:           # 全部字段 = 机械重数（form2_pre_ledger 除外，声明量单独传）
    samples: int
    by_field: dict[str, int]        # 键序固定（§4.2）
    form2_total: int
    form2_from_samples: int
    findings_p: dict[str, int]      # p1/p2/p3/unlabeled/cells_nonstandard
```

字段类型键映射（单一真值源，I-4）：`[("版本号","version"),("章节号","section"),("数值常量","constant"),("行号","line"),("计数","count"),("转述引文","quote"),("映射闭合","mapping")]`——列序即 M7 §2 表头现行序。

## 7. 错误处理

| 错误场景 | 处理方式 | 退出码 | 用户可见信息 |
|---------|---------|-------|------------|
| §1/§2 表节缺失或零数据行 | P1（账本结构损坏，声波式失败） | 1 | `[P1] §1 样本登记表缺失/为空` |
| 行不匹配行文法（`\| <int> \|` 起始）| 逐行报 P1 | 1 | 行号 + 原因（列数/前导整数缺失） |
| hits 块缺失 | verify 报 P1；--write 需 --seed-pre-ledger | 1 | `[P1] hits 块缺失` |
| hits JSON 非法 | P1（--write 亦拒绝——声明块必须先可解析才可重生成） | 1 | 解析错误位置 |
| --write 时存在非 hits 类阻断违规 | 拒绝写入（写守卫） | 1 | 阻断违规清单 |
| 未知异常（文件 IO 等） | 顶层 try/except | 2 | stderr `[tool-error]`（工具错误 ≠ 校验通过） |
| staged 文件不含 M7 | skip | 0 | `[skip] 非 M7 目标` |

**退出码语义（与 dc_validator 逐字一致）**：`0`=通过；`1`=运行成功且发现违规；`2`=工具自身错误。

## 8. 不变式（Invariants）

1. **I-1 默认只读**：verify 模式零写入；写文件仅限显式 `--write` 且仅重写 M7 §5 的 hits 围栏块内容（不触表格与其余文本）
2. **I-2 确定性**：同一 M7 内容 → 校验输出与 --write 产物逐字节确定（无时间戳/随机/网络/git 状态依赖）
3. **I-3 零新规则**：只机器化 M7 登记纪律（ADR-0007 D1 载体 + 头注"追加一行/同步分桶"）与 P-011 验收标准隐含的对账要求；不发明新登记规则（如新必填列）
4. **I-4 单一真值源**：表结构契约（列名/列数/键映射）以 M7 现行表为准；变更须先改 M7（+本 DESIGN）再改脚本，同 commit
5. **I-5 异构于生成端**：纯机械解析/算术/对账，无 LLM、无语义判断
6. **I-6 声明 = 重数（R7 同构）**：hits 块全部字段必须等于机械重数值；--write 落盘的必为重数值；写守卫保证失衡账本不可被编码进块

## 9. 幻觉排除审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 设计决策可追溯 RESEARCH（§2.1 映射表 6 行逐一引用）——自查（单视角）
- [x] 无未验证假设（H1/H2 随 RESEARCH 附录 C 显式携带：H1 的看护机制已内化为 §4.2 pre_ledger 声明 + §4.3 m7-xtable 规则；H2 待 Step 10 实测）
- [x] 无论证驱动的归因扭曲（未裁剪历史非整齐形态——A5/A6 如实进契约而非"顺手归一"）

### 9.2 替代方案审查

- [x] 三个替代方案（B/C/D）各有明确否决理由；D 的否决与 M7 样本⑫ 实证自洽

### 9.3 职责边界审查

- [x] 职责边界清晰（§2.3）：语义起草归人工、§3 baseline 归外部快照、逐行对账声明为能力边界
- [x] 不越界：不动 dc_validator、不吞并其他文档统计块校验

> **标注（RULE-1/RULE-4）**：本 §9 由同会话自查勾选（单视角）；独立 pass 待 Step 10 或用户触发，届时以独立结论为准。

## 10. 对实施的输入

### 10.1 关键工程约束

1. Windows：entry `python scripts/m7_stats.py`；路径处理用 os.path（脚本位于 `<root>/scripts/`，ROOT 推导同 dc_validator L27）
2. 零第三方依赖（stdlib：argparse/re/os/sys/json/dataclasses/datetime/tempfile）
3. 代码量预估 ~300 行（±100；**实施时在 IMPLEMENTATION §10 记录实际 LOC**——P-008 P3 ③ 教训：DESIGN LOC 预估必须实施核对）
4. selftest expect 计数自增（DR-6 同构：计数不手填）
5. --write 的文件写入遵守 user_profile Operational Safety Rules（Edit/直接写单一目标段，非 PowerShell 管道截断）

### 10.2 风险与缓解

| 风险 | 缓解 |
|------|------|
| 解析器自身计数错（规律②——样本⑨ 校验器前科） | selftest fixture 覆盖行/列/跨表/hits 对账全算术路径 + 真实 M7 全量 dry-run（Step 10 E1） |
| M7 表格式演化使解析器过期 | 结构性失败声波式报 P1（不静默）；I-4 变更流程 |
| pre_ledger 基线漂移 | 声明值 + 不变式看护；失衡即 P1 强制人工裁决（H1 机制化） |
| P3 非阻断档被误读为"宽松" | P3 仅限历史非整齐形态两类；新违规仍 P1/P2；P3 行始终打印可见 |
| bootstrap seed 值错（6 ≠ 真基线） | seed 须人工对照 Phase 7C 行小计（RESEARCH A3 引文核对）；Step 10 ADD 复核 |

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）
