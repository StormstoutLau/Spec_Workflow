# 实施文档：M7 hits 机读块 + 样本登记脚本化

---
id: m7-hits-block-IMPLEMENTATION
type: design
version: 1.1
status: in-review
date: 2026-08-21
depends: [m7-hits-block-DESIGN, m7-hits-block-RESEARCH]
upstream: null
---

> **Feature**: m7-hits-block（PROGRESS P-011）
> **创建日期**: 2026-08-21
> **状态**: in-review（实施完成 + 自查勾选；独立 pass 待触发）
> **Spec 步骤**: Step 5-6, 9
> **基于设计**: [M7_HITS_DESIGN.md](./M7_HITS_DESIGN.md) v1.0
> **审查状态**: `自查（单视角）`（RULE-4）——待独立 pass 或异基座复验
> **v1.1 变更（2026-08-21）**: Step 9 实施完成——实际 LOC 828 回填（§10）+ 派生需求 DR-A/B/C 登记 + 实施期拦截实录（M4 标记格式 P1 + M5 断链 P2×3，入 M7 样本⑮）

---

## 1. 实施概述

单一脚本 `scripts/m7_stats.py`（零第三方依赖）承载 MH1-MH5 五模块：解析 M7 §1 样本表与 §2 分桶表 → 机械重数 Stats → 跨表不变式 + hits 块声明对账 → 三模式 CLI（verify 默认 / --write 重生成 / --selftest）。`.pre-commit-config.yaml` 追加 m7-stats hook（files 收窄至 M7 路径）。M7_EVIDENCE_LOG.md 落地 §5 hits 块（bootstrap: --write --seed-pre-ledger 6）。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|------|------|------|---------|
| 语言 | Python（stdlib only） | 3.12（主控站实测环境，与 dc_validator 同） | ✅ |
| 解析 | re（正则） | stdlib | ✅ |
| JSON | json | stdlib | ✅ |
| 依赖 | **零第三方依赖** | — | ✅（与 dc_validator 同约束） |

### 2.2 stdlib API 下限检查（Step 6 规则）

| API | 下限版本 | 本仓运行环境 | 状态 |
|-----|---------|------------|------|
| `dataclasses.dataclass(frozen=True)` | 3.7 | 3.12 | ✅ |
| `re`（findall/match/search，含 lookahead） | 3.0 | 3.12 | ✅ |
| `argparse` / `json.dumps(ensure_ascii=False, indent=2)` | 3.0 | 3.12 | ✅ |
| `tempfile.mkdtemp` / `shutil.rmtree` | 3.0 | 3.12 | ✅ |
| `datetime.date(y,m,d)`（日历合法性） | 3.0 | 3.12 | ✅ |

无 3.8+ 独占 API（无 walrus 于必需路径 / 无 match）；无 `Decimal.ulp` 类 3.12+ 陷阱（M6 教训自查）。

### 2.3 文件结构

```
scripts/
└── m7_stats.py          # 新增（MH1-MH5 单文件，同 dc_validator 形态）
.pre-commit-config.yaml  # 追加 m7-stats hook（不动 dc-validator 条目）
docs/M7_EVIDENCE_LOG.md  # 追加 §5 hits 块 + 头注登记纪律补一句 + §4 待办挂钩行更新
```

### 2.4 解析契约（表结构 → 正则，I-4 单一真值源）

```python
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M7_PATH = "docs/M7_EVIDENCE_LOG.md"

S1_HEADER = "## 1. 样本登记表"          # 前缀匹配（^##\s*1[\.、]?）
S2_HEADER = "## 2. 形态 II 复发分桶"     # 前缀匹配（容忍全角空格变体）
SAMPLE_COLS = ["#", "日期", "载体", "审查配置", "发现", "形态II复发", "来源"]
BUCKET_COLS = ["载体 \\ 字段类型", "版本号", "章节号", "数值常量", "行号",
               "计数", "转述引文", "映射闭合", "小计"]
FIELD_KEYS = [("版本号", "version"), ("章节号", "section"), ("数值常量", "constant"),
              ("行号", "line"), ("计数", "count"), ("转述引文", "quote"), ("映射闭合", "mapping")]

RE_SAMPLE_ROW = re.compile(r"^\|\s*(\d+)\s*\|")        # 数据行探针
RE_FORM2_LEAD = re.compile(r"^\s*(\d+)")               # 形态II复发列前导整数
RE_P_TOKEN    = re.compile(r"(\d+)\s*P([123])")        # 发现列 P 标记
RE_LEAD_IS_P  = re.compile(r"^\s*(\d+)(?=\s*P[123])")  # 前导整数实为 P 标记（无总数形态）
RE_DATE       = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_HITS_FENCE = re.compile(r"```hits\n(.*?)\n```", re.S)
```

**关键判定逻辑**：
- 表头行校验：首行单元格序列 == SAMPLE_COLS / BUCKET_COLS（逐名比对，防列重排静默错位——I-4 防护）；不符报 P1
- 数据行：split("|") 去首尾空段 → strip 各格；样本表 7 格、分桶表 9 格
- 分桶合计行：首格 strip 去 `**` 后 == "合计"
- 前导总数（发现列）：`RE_LEAD_IS_P` 命中 → 该前导整数是 P 标记（如 `2P2+6P3`），**无**前导总数；否则 `^\s*(\d+)` 命中 → 前导总数（如 `10（2P1+…）`）；两者皆否 → 非标准单元格（P3，计入 cells_nonstandard）
- unlabeled = Σ max(0, 前导总数 − P 标记和)；P 标记和 > 前导总数 → P1

**hits 块定位**：`RE_HITS_FENCE` 全文匹配数 ≠ 1 → P1（0 或 ≥2）；块内容 `json.loads` 失败 → P1。--write 替换仅发生在围栏内部（首尾 ```hits / ``` 行保留），块缺失时追加整个 §5 节（标题 + 说明行 + 围栏块）。

### 2.5 与 dc_validator 的运行隔离（A10/A11 复核）

- hits 围栏块内容不触发 dc_validator M5（fence 内 continue）
- M7 无 "## 0. 断言统计表" 节 → M4 不介入
- 两 hook 独立运行，互不传参；m7-stats 的 `files:` 收窄避免对非 M7 提交空跑

## 3. 模块实施

### 3.1 MH1 CLI 入口

接口签名（与 DESIGN §3.2 对应）：

```python
def main(argv: list[str] | None = None) -> int:
    """退出码：0 通过 / 1 违规或拒绝写入 / 2 工具自身错误。"""

def gather_targets(argv_files: list[str]) -> list[str]:
    """pre-commit 语义：传入文件 ∩ {M7_PATH}（反斜杠归一化）；空交集且 argv 非空 → []（skip）。"""
```

旗标：`--write` / `--seed-pre-ledger N`（仅块缺失时必需）/ `--selftest` / 位置参数 files。

### 3.2 MH2 样本表解析

```python
def parse_sample_table(text: str) -> tuple[list[SampleRow], list[CheckResult]]:
    """§1 节内：表头名序校验 → 逐数据行（编号连续/列数/日期/前导整数/P 抽取）。"""
```

编号连续性：收集行首整数后统一断言 == list(range(1, N+1))（断档/重复/乱序各报 P1）。

### 3.3 MH3 分桶表解析

```python
def parse_bucket_table(text: str) -> tuple[list[BucketRow], list[CheckResult]]:
    """§2 节内：表头名序校验 → 逐行（单元格域/行算术）→ 合计行（列算术）。"""
```

单元格域：`^\d+$` 或 `—`；行算术：小计 == Σ 前 7 格；列算术：合计行每列 == 上方同列和，合计小计 == Σ 数据行小计。

### 3.4 MH4 统计与对账

```python
def compute_stats(rows_s: list[SampleRow], rows_b: list[BucketRow]) -> Stats: ...
def check_xtable(stats: Stats, pre_ledger: int | None) -> list[CheckResult]:
    """form2_total == pre_ledger + form2_from_samples（pre_ledger 为块内声明值）。"""
def compare_hits(declared: dict, stats: Stats, pre_ledger: int | None) -> list[CheckResult]:
    """逐字段声明 vs 重数（form2_pre_ledger 为声明量，不参与比对，仅受 xtable 约束）。"""
def serialize_hits(stats: Stats, pre_ledger: int) -> str:
    """json.dumps(..., ensure_ascii=False, indent=2)，字段序固定（DESIGN §4.2）——确定性产物。"""
```

**pre_ledger 数据流**：块存在 → 读声明值（--write 保留不改）；块缺失 → verify 跳过 xtable（缺块 P1 已阻断）；--write 无块 → 必须 --seed-pre-ledger。

### 3.5 MH5 selftest

```python
def run_selftest() -> int:
    """14 fixture（§8.1），tempfile 构造于系统临时目录（I-1 变体：不触工作树），
    expect 计数自增机械计数（DR-6 同构）。"""
```

## 4. 接口实施汇总

| 接口 | DESIGN 出处 | 签名一致性 |
|------|------------|-----------|
| main / gather_targets | §3.2 MH1 | ✅ |
| parse_sample_table | §3.2 MH2 | ✅ |
| parse_bucket_table | §3.2 MH3 | ✅ |
| compute_stats / check_xtable / compare_hits / serialize_hits | §3.2 MH4 | ✅ |
| run_selftest | §3.2 MH5 | ✅ |

## 5. 兼容性

- **Python 3.12（主控站）/ 3.10+**：全部 stdlib API 见 §2.2 下限表，无版本陷阱
- **Windows**：路径 os.path 处理；pre-commit 传入路径反斜杠归一化；entry `python` 前缀（A8）
- **向后兼容**：M7 现有 §1-§4 文本零改动（仅追加 §5 + 头注一句 + §4 一行更新）；dc_validator 零改动

## 6. 错误处理实施

| 错误场景（DESIGN §7） | 处理代码位置 | selftest fixture |
|----------------------|------------|-----------------|
| 表节缺失/空 | parse_* 入口哨兵 | F1 反例变体 |
| 行结构违规 | parse_sample_table 行循环 | F2/F3/F5 |
| 日期非法 | datetime.date try/except | F4 |
| 分桶算术 | parse_bucket_table 行/列算术 | F6/F7 |
| 跨表失衡 | check_xtable | F8 |
| hits 缺失/非法/失配 | RE_HITS_FENCE 计数 + json.loads + compare_hits | F9/F10 |
| --write 写守卫 | main 写前过滤（check_id != "hits" 的 P1/P2） | F12 |
| 工具自身错误 | main 顶层 try/except → exit 2 | —（结构同 dc_validator L296-298） |

## 7. 不变式实施

| 不变式（DESIGN §8） | 实施位置 | 验证方式 |
|-------------------|---------|---------|
| I-1 默认只读 | main：仅 --write 分支调用写入函数 | F12（写守卫拒绝时字节不变） |
| I-2 确定性 | serialize_hits 无时间态字段 | F13（双跑逐字节一致） |
| I-3 零新规则 | 校验规则集 == DESIGN §4.3 表逐行 | 代码审查（Step 10） |
| I-4 单一真值源 | SAMPLE_COLS/BUCKET_COLS/FIELD_KEYS 常量 + 表头名序校验 | F1（列名错位报 P1） |
| I-5 异构于生成端 | 全文件无 LLM/网络调用 | 结构性保证（零 import 网络库） |
| I-6 声明 = 重数 | compare_hits + 写守卫 | F9/F12 |

## 8. 测试策略

### 8.1 selftest fixture 矩阵（14 项）

| # | 场景 | 断言 |
|---|------|------|
| F1 | 合规迷你账本（2 样本 + 2 分桶行 + hits 一致） | verify exit 0，Stats 各值精确断言 |
| F2 | 样本编号断档（1,3） | P1 |
| F3 | 样本行列数 6 | P1 |
| F4 | 日期 2026-13-01 | P2（exit 1） |
| F5 | 形态II复发无前导整数 | P1 |
| F6 | 分桶行小计 ≠ 行和 | P1 |
| F7 | 合计列 ≠ 列和 | P1 |
| F8 | 跨表对账失衡 | P1（m7-xtable） |
| F9 | hits samples 声明失配 → P1；--write 修复后 verify exit 0 | 修复闭环 |
| F10 | hits 缺失：verify P1；--write 无 seed 拒绝；--seed-pre-ledger 6 落盘且 verify 过 | bootstrap 全路径 |
| F11 | P 抽取五形态（总数齐 / P 超总数 / unlabeled / 非标准 / 无总数有 P） | p1/p2/p3/unlabeled/cells_nonstandard 精确断言 |
| F12 | --write 写守卫（存在 m7-bucket 违规） | 拒绝写入 + 文件字节不变 |
| F13 | 确定性 | --write 双跑产物逐字节一致 |
| F14 | P3 非阻断 | 含非标准发现单元格 → exit 0 + [P3] 行打印 |

### 8.2 集成验证（Step 10，E1 级）

1. `python scripts/m7_stats.py --selftest` → N/N PASS
2. 真实 M7 dry-run：verify（块缺失预期 P1）→ `--write --seed-pre-ledger 6` → verify exit 0
3. `python scripts/dc_validator.py --check-all` → 0 违规（两工具共存回归）
4. `pre-commit run m7-stats --all-files` → M7 通道通过
5. bootstrap 后 hits 值人工核对：samples=14 / form2_total=21 / pre_ledger=6 / from_samples=15（RESEARCH A1-A4 已验值）

## 9. 幻觉排除审查（Step 6 Review）

### 9.1 依赖版本验证

- [x] 零第三方依赖（§2.1）；stdlib API 下限逐条核对（§2.2，无 3.12+ 陷阱）
- [x] 无虚构库/函数

### 9.2 接口签名验证

- [x] 全部签名可实现（§4 汇总表与 DESIGN §3.2 逐一对应；`pre_ledger: int | None` 双态为实施细化，语义 = DESIGN §3.4 "块缺失 → 跳过 xtable"）
- [x] 正则无不可达分支（RE_LEAD_IS_P lookahead 为 stdlib re 支持语法）

### 9.3 实施与设计对齐

- [x] 模块 MH1-MH5 ↔ DESIGN §3.2；校验规则集 ↔ DESIGN §4.3 逐行；不变式 I-1~I-6 ↔ DESIGN §8
- [x] 无设计未覆盖实施（--seed-pre-ledger 为 DESIGN §4.4 bootstrap 的接口化，非新增行为）

### 9.4 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| 每行多次正则全扫 | 单遍逐行解析，findall 仅作用于发现列单元格 |
| --write 全文重写 | 围栏内替换（字符串切片拼接），表区文本零接触 |

> **标注（RULE-1/RULE-4）**：本 §9 由同会话自查勾选（单视角）；独立 pass 待 Step 10 或用户触发。

## 10. 实施步骤

| 步 | 动作 | 验证 |
|----|------|------|
| 1 | 写 `scripts/m7_stats.py` 骨架（MH1 CLI + 常量 + CheckResult/Summary） | import 无错 |
| 2 | MH2/MH3 解析器 + MH4 统计/对账/序列化 | F1-F11 |
| 3 | MH5 selftest（14 fixture） | `--selftest` N/N |
| 4 | `.pre-commit-config.yaml` 追加 m7-stats hook | `pre-commit run m7-stats --all-files` |
| 5 | M7 bootstrap：头注/§4 更新 + `--write --seed-pre-ledger 6` | verify exit 0 + §8.2 值核对 |
| 6 | 全仓回归（dc_validator + 两 hook 双通道） | 0 违规 |

**实际 LOC 记录（DESIGN §10.1-3 核对义务）**: **828 行**（预估 ~300±100——**预估口径失误如实登记**：预估仅计核心校验逻辑（~470 行），selftest 十四 fixture 的迷你账本模板串（MINI/HITS_VALID）与写守卫/确定性等闭环断言（~360 行）未计入预估基数；与 P-008 P3 ③ 同族教训：DESIGN LOC 预估须明确口径（核心 vs 含测试））。

**实施期派生需求登记（Step 8 规则，DESIGN 未显式声明、实施中自行产生）**：

| 派生需求 | 内容 | 验收 |
|---------|------|------|
| DR-A 写后内存自检 | --write 落盘前对新文本全量 re-analyze，任何 P1/P2 即拒绝落盘（exit 2 工具错误语义）——比 DESIGN §3.4 写守卫更强的自洽保证：序列化与重数不一致在落盘前拦截 | 结构审查 + F9 修复闭环（写后 verify 过） |
| DR-B 发现列空值 P1 | 发现列为空 = 行结构损坏报 P1（DESIGN §4.3 未列举——空值既非"非标准 P3"亦非可统计形态，实施期裁定归行结构类） | 代码路径审查（selftest 未设专项 fixture，登记为已知测试缺口） |
| DR-C §5 节无围栏守卫 | 文件已有 `## 5.` 节却无 hits 围栏时 --write 拒绝（防追加第二个 §5 节），报 P1 提示人工修复 | 代码路径审查（同上，已知测试缺口） |

**实施期拦截实录（提交前 dry-run，dc_validator M4/M5）**：① M7_HITS_RESEARCH 初稿 A 标记用 `#### 【A】` 标题式（仓内契约 = 行首【A】，LANGGRAPH 先例）→ M4 重数 0 ≠ 声明 11 报 P1，改行首标记后过——**标记格式即机读契约，格式偏离等同计数不可验**；② 上轮 commit b541705（FWK-FACT-CHECK）遗留 3 条 P2 断链（`file:///` 外链缺档 3 `外部·` 标注 ×2 + `adr/` 相对路径应为 `../adr/` ×1）被本轮 M5 提交前拦截——b541705 当次提交未走 hook 通道（现场裁量/绕过），遗留至本轮捕获。两项均入 M7 样本⑮。

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）
