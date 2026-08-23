# 实施文档：repo_stats 视图层机械枚举校验器

---
id: repo-stats-IMPLEMENTATION
type: design
version: 1.2
status: verified
date: 2026-08-23
depends: [repo-stats-DESIGN, repo-stats-RESEARCH]
upstream: null
---

> **Feature**: repo-stats（PROGRESS P-014，[DIS-010](../../docs/discoveries/README.md) 处置落地）
> **创建日期**: 2026-08-22
> **状态**: verified（Step 10 终验完成：真异基座独立 pass（DeepSeek V4 Pro）双满足 + 三校验器全绿 + CHECKLIST 状态 accepted；自查单视角 → 独立 pass 闭合）
> **Spec 步骤**: Step 5-6
> **基于设计**: [REPO_STATS_DESIGN.md](./REPO_STATS_DESIGN.md) v1.1
> **审查状态**: `真异基座独立 pass`（RULE-1 时序独立 + RULE-5 模型异质性双满足：生成端 GLM-5.3 / 审查端 DeepSeek V4 Pro——同样本⑬ 双满足形态）

---

## 1. 实施概述

单一脚本 `scripts/repo_stats.py`（零第三方依赖）承载 RS1-RS5 五模块：解析 CODE_WIKI §10 ```stats 机读块 → 多通道枚举真值（LS / hits 块 / front-matter / PROGRESS 表 / discoveries 索引）→ 三路对账（声明=重数 / 模式扫描 / 清单比对）→ 两模式 CLI（verify 默认 / --selftest）。`.pre-commit-config.yaml` 追加 repo-stats 第三 hook（files = 视图载体集 ∪ 真值源集，DESIGN §3.4）。

**与 m7_stats 的本质差异（对账器非重生成器）**：无 --write、无任何写通道（I-1）；prose 位点永不代改，只报偏差——视图 prose 是人工叙事，机械重建必产伪叙事（DESIGN 方案 D 否决）。

**实施前契约修正已发生（DESIGN v1.0→v1.1）**：`derived.view_layer_total` 真值口径由「view_layer_samples 样本列求和」（=35，错）修正为「分桶表视图载体行求和」（=33，对）——本 IMPLEMENTATION 撰写取证时对账发现，样本⑪ 三行分桶中仅 CODE_WIKI v1.5 行属视图载体。此修正本身即「实施前对账捕获设计契约错值」一例，如实记录于 DESIGN v1.1 变更注。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|------|------|------|---------|
| 语言 | Python（stdlib only） | 3.12（主控站实测环境，与 dc_validator / m7_stats 同） | ✅ |
| 解析 | re（正则） | stdlib | ✅ |
| JSON | json | stdlib | ✅ |
| 依赖 | **零第三方依赖** | — | ✅（三件套同约束） |

### 2.2 stdlib API 下限检查（Step 6 规则）

| API | 下限版本 | 本仓运行环境 | 状态 |
|-----|---------|------------|------|
| `dataclasses.dataclass(frozen=True)` | 3.7 | 3.12 | ✅ |
| `re`（findall/search/sub，含 re.S / re.M） | 3.0 | 3.12 | ✅ |
| `json.loads` / `json.dumps(ensure_ascii=False)` | 3.0 | 3.12 | ✅ |
| `os.listdir` / `os.path.join` / `os.path.isfile` | 3.0 | 3.12 | ✅ |
| `argparse` / `sys.exit` | 3.0 | 3.12 | ✅ |
| `tempfile.mkdtemp` / `shutil.rmtree` | 3.0 | 3.12 | ✅ |
| `ord` / `chr`（Unicode 码点算术，带圈数字转换） | 内置 | 3.12 | ✅ |

无 3.8+ 独占 API（无 walrus 于必需路径 / 无 match）；无 `Decimal.ulp` 类 3.12+ 陷阱（M6 教训自查）。

### 2.3 文件结构

```
scripts/
└── repo_stats.py            # 新增（RS1-RS5 单文件，三件套同形态）
.pre-commit-config.yaml      # 追加 repo-stats hook（不动既有两条目）
CODE_WIKI.md                 # 末尾追加 §10 ```stats 机读块（§1-§9 零重排）
```

### 2.4 解析契约（常量与正则，I-4 单一真值源）

```python
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_WIKI_PATH = "CODE_WIKI.md"
M7_PATH        = "docs/M7_EVIDENCE_LOG.md"
DIS_PATH       = "docs/discoveries/README.md"
PROGRESS_PATH  = "docs/PROGRESS.md"
HOOKS_PATH     = ".pre-commit-config.yaml"
SPEC_DIR       = "spec"                    # templates 排除规则固定于枚举器语义

RE_STATS_FENCE  = re.compile(r"```stats\n(.*?)\n```", re.S)   # CODE_WIKI 内恰一个
RE_HITS_FENCE   = re.compile(r"```hits\n(.*?)\n```", re.S)    # M7 内直读（契约同 m7_stats）
RE_MACHINE_FENCE = re.compile(r"```(?:stats|rules|assertions|hits)\n.*?\n```", re.S)
RE_DIS_ID       = re.compile(r"DIS-(\d{3})")
RE_P_TASK       = re.compile(r"^\|\s*P-\d{3}\s*\|")
RE_HOOK_ID      = re.compile(r"^\s*-\s*id:")
RE_FM_VERSION   = re.compile(r"^version:\s*(\S+)\s*$", re.M)
RE_S2_HEADER    = re.compile(r"^##\s*2[\.、]?\s*形态", re.M)   # §2 分桶表定位
RE_BUCKET_ROW   = re.compile(r"^\|")
RE_VIEW_CARRIER = re.compile(r"CODE_WIKI|README|evidence\.svg") # 分桶表载体列视图载体判定（v1.1 口径）
RE_S9_SPEC_LINK = re.compile(r"\(\./spec/([^/\s]+)/\)")        # §9 spec/*/ 索引链接
RE_VERSION_TOKEN= re.compile(r"v(\d+(?:\.\d+)+)")
RE_TREE_ENTRY   = re.compile(r"^    [├└]──\s+(\S+)")           # §2.1 树 spec/ 段条目（4 空格缩进）
RE_TREE_SPEC    = re.compile(r"^[├└]──\s+spec/\s*$")           # 树 spec/ 行锚
```

**关键判定逻辑**：
- **stats 块定位**：`RE_STATS_FENCE` 在 CODE_WIKI 全文匹配数 ≠ 1 → P1（0 或 ≥2）；内容 `json.loads` 失败 → P1
- **围栏外过滤的精确语义**（DESIGN §4.4「围栏外」的实施细化）：只剔除**机读四类围栏**（```stats / ```rules / ```assertions / ```hits——`RE_MACHINE_FENCE`），**普通围栏（目录树 / mermaid / 代码示例）保留在扫描面**——§2.1 树内注释是视图数字载体（L54「双 hook」/ L66「形态 II 53 处」活靶实证，树注释漂移与 prose 漂移同责）
- **分桶表视图载体行求和**（v1.1 修正口径）：定位 §2 节 → 逐 `RE_BUCKET_ROW` 行 split("|") → 首列（载体列）`RE_VIEW_CARRIER` 命中 → 末列（小计列）strip 去 `**` 取 int 累加；「合计」行首列不命中视图载体模式，天然排除
- **§2.1 树 spec/ 段提取**：树围栏内找 `RE_TREE_SPEC` 行 → 其后连续 `RE_TREE_ENTRY` 行（恰好 4 空格缩进）→ 条目名取 `/` 前首段（`doc-contract/PLAN.md` → `doc-contract`）；遇非该形态行即段结束
- **§9 spec 索引提取**：§9 节内 `RE_S9_SPEC_LINK` 全部捕获 → 目录名集合
- **doc_registry 版本对账**：§9 表中含 label 的行 → `RE_VERSION_TOKEN` 取该行首个版本号 → 去 `v` 前缀 → 与 path 文档 `RE_FM_VERSION` 直读值**字符串全等**比对（v1.4 ≠ 1.4.2 → P2；前缀匹配不豁免——活靶实证）
- **数字形态转换**（RS4 纯函数）：
  - `cn_to_int(s)`：零~九十九简单合成（「十」=10 / 「X十」=X×10 / 「X十Y」=X×10+Y / 单字一~九直取 / 「零」=0）；非法输入返回 None
  - `circled_to_int(ch)`：`ord(ch)` 落于 U+2460-U+2473 → 1-20；U+3251-U+325F → 21-35；否则 None

### 2.5 与双既有工具的运行隔离（DESIGN §2.2 复核）

- stats 围栏块内容不触发 dc_validator M5（fence 内链接跳过先例，m7-hits A14 同构）
- CODE_WIKI 无 front-matter、无 §0 统计表 → dc_validator M2/M4 不介入；CODE_WIKI 不在 `files: \.md$` 的断链扫描豁免范围（正常走 M5，链接仍须有效）
- 三 hook 独立运行无顺序依赖；hits 块损坏时 m7-stats 与 repo-stats 各自声波式报 P1，互不掩盖
- repo_stats 只读 M7（hits 块 + §2 分桶表），零写入——与 m7_stats 的 --write 通道无竞争

## 3. 模块实施

### 3.1 RS1 CLI 入口

```python
def main(argv: list[str] | None = None) -> int:
    """退出码：0 通过（含仅 P3）/ 1 发现 P1/P2 / 2 工具自身错误。"""

def in_scope(files: list[str]) -> bool:
    """staged 文件 ∩ 对账作用域（视图载体集 ∪ 真值源集）非空判定；
    反斜杠归一化；argv 无文件参数（本地直跑）→ True（全量对账）。"""
```

旗标：`--selftest` / 位置参数 files（pre-commit 传入）。**无 --write**（I-1，对账制）。

### 3.2 RS2 真值枚举器

```python
def build_truth_set(spec: StatsSpec) -> tuple[TruthSet, list[CheckResult]]:
    """七通道枚举 → TruthSet；真值源损坏产声波式 P1（DESIGN §4.4 rs-truth）。"""
```

| 通道 | 真值键 | 枚举方式 |
|------|--------|---------|
| T1 | fs.spec_feature_dirs | `os.listdir("spec")` 目录项 − {templates} |
| T2 | fs.adr_files / fs.dev_logs / fs.scripts / fs.templates | `os.listdir` 计数（adr/*.md、docs/dev-log/*.md、scripts/*.py、spec/templates/*.md——isfile 过滤） |
| T3 | fs.hooks | `.pre-commit-config.yaml` `RE_HOOK_ID` 行计数 |
| T4 | fs.progress_tasks | PROGRESS `RE_P_TASK` 行计数 |
| T5 | hits.samples / hits.form2_total | M7 `RE_HITS_FENCE` 直读（json 字段；块缺失/非法 → P1 声波式） |
| T6 | dis.range_min / dis.range_max | discoveries 全文 `RE_DIS_ID` findall → int min/max |
| T7 | derived.view_layer_total / view_layer_pct | M7 §2 分桶表视图载体行求和 / floor(100×total/form2_total)（v1.1 口径；form2_total 缺失时 pct 置 -1 并报 P1） |

依赖方向：T7 依赖 spec.view_layer_samples 仅用于口径追溯声明（非求和输入——v1.1）；TruthSet 构建顺序 = T1-T6 先行，T7 后算。

### 3.3 RS3 stats 块解析

```python
def parse_stats_block(text: str) -> tuple[StatsSpec, list[CheckResult]]:
    """RE_STATS_FENCE 计数==1 → json.loads → schema 校验：
    patterns 非空且逐条 {id, regex(可编译), truth(∈绑定集), scope(⊆carriers∪facade)}；
    declared 七键齐；carriers 两级非空互斥；facade_baseline 键 ⊆ 载体集；
    view_layer_samples 元素为正 int；suppress 条目 {pattern_id, file, note} 齐。"""
```

绑定集（truth 合法值封闭枚举，与 DESIGN §4.2 表逐字一致，代码常量）：`fs.spec_feature_dirs / fs.adr_files / fs.dev_logs / fs.scripts / fs.templates / fs.hooks / fs.progress_tasks / hits.samples / hits.form2_total / dis.range_min / dis.range_max / derived.view_layer_total / derived.view_layer_pct`。

### 3.4 RS4 对账引擎

```python
def reconcile(spec: StatsSpec, truth: TruthSet) -> list[CheckResult]:
    """三路对账：① rs-decl（P1）② rs-pattern（living P2 / facade P3）③ rs-list（P2）。"""
```

**① rs-decl**：spec.declared 逐字段 vs truth.fs 同键（declared/actual 报文）；P1。
**② rs-pattern**：对每个载体（carriers.living / carriers.facade 分类）取文本 → `RE_MACHINE_FENCE` 剔除机读围栏 → 逐 PatternSpec（scope 过滤）`finditer` → 命中捕获组值经数字转换（阿拉伯直取 / 中文 cn_to_int / 带圈 circled_to_int / 双捕获组 PT-3/PT-6/PT-11 各自转换）→ 与 truth[truth_key] 比较：
- living 载体：≠ → P2（报 pattern_id + 文件:行 + expected/actual）
- facade 载体：≠ facade_baseline[carrier].values[truth_key] → P3（prose 与基准漂移）；baseline 值 ≠ truth 当前值 → P3（快照滞后，as_of 标注）
- suppress 白名单命中（pattern_id + file 双匹配）→ 跳过该命中（显式豁免，非静默）
- **SVG 载体特殊通道**：不跑 prose 模式（图形布局无稳定锚，DESIGN §4.3 原则③）——只做 baseline values 的 `>N<` 文本节点包含性检查（SVG 内 `>20<` 形态存在性；缺失 → P3 与基准漂移）
**③ rs-list**：
- §2.1 树 spec/ 子目录集 vs T1 枚举集：缺登（LS 有树无）/ 幻影（树有 LS 无）双向报 P2
- §9 spec 索引链接集 vs T1 枚举集：缺行 / 幻影行双向报 P2
- doc_registry 逐条：§9 含 label 行版本号 vs front-matter version 全等比对 → P2

**行号报告**：CheckResult.line 由 finditer 的 `text.count("\n", 0, m.start()) + 1` 计算（围栏剔除后行号须映射回原文行号——实施采用**原文行号扫描**：逐行机读围栏状态机跳过，行号天然准确，避免剔除-映射二次错位）。

> 实施裁定（本节新增，DESIGN 未显式）：模式扫描采用**逐行状态机**（进入 ```(stats|rules|assertions|hits) 行 → 跳到围栏闭合行），非全文 sub 后 finditer——行号保真优先，且避免 sub 改变多字节字符切片边界的心智负担。

### 3.5 RS5 selftest

```python
def run_selftest() -> int:
    """fixture 矩阵（§8.1），tempfile 构造迷你仓（假 stats 块 + 假真值源 + 假载体），
    不触工作树；expect 计数自增机械计数（DR-6 同构）。"""
```

## 4. 接口实施汇总

| 接口 | DESIGN 出处 | 签名一致性 |
|------|------------|-----------|
| main / in_scope | §3.2 RS1 | ✅ |
| build_truth_set | §3.2 RS2 | ✅（spec 参数为实施细化：T7 口径追溯依赖声明，v1.1） |
| parse_stats_block | §3.2 RS3 | ✅ |
| reconcile | §3.2 RS4 | ✅（行号状态机为实施裁定，§3.4 注） |
| run_selftest | §3.2 RS5 | ✅ |

## 5. 兼容性

- **Python 3.12（主控站）/ 3.10+**：stdlib API 见 §2.2 下限表，无版本陷阱
- **Windows**：路径 os.path；pre-commit 传入路径反斜杠归一化；entry `python` 前缀（A13）
- **向后兼容**：CODE_WIKI §1-§9 零重排（stats 块追加文件末尾）；dc_validator / m7_stats / 既有双 hook 零改动；M7 / PROGRESS / discoveries 零改动（纯只读消费）

## 6. 错误处理实施

| 错误场景（DESIGN §7） | 处理代码位置 | selftest fixture |
|----------------------|------------|-----------------|
| stats 块缺失/多块/JSON 非法 | parse_stats_block 围栏计数 + json.loads | F2/F3 |
| regex 非法 / truth 越界 / scope 越界 | parse_stats_block schema 校验 | F4 |
| hits 块不可读 | build_truth_set T5 声波式 P1 | F13 |
| front-matter 不可解析 | reconcile ③ doc_registry 通道 P1 | F14 |
| LS 目录缺失 | build_truth_set T1/T2 哨兵 P1 | F15 |
| declared 失配 | reconcile ① | F5 |
| living 命中值 ≠ 真值 | reconcile ② | F6 |
| facade 基准漂移 / 快照滞后 | reconcile ② | F7/F8 |
| 树/索引缺登幻影 | reconcile ③ | F9/F10 |
| 版本声明失配 | reconcile ③ | F11 |
| 未知异常 | main 顶层 try/except → exit 2 | —（结构同 dc_validator/m7_stats） |
| staged 与作用域无交集 | main skip 分支 exit 0 | F16 |

## 7. 不变式实施

| 不变式（DESIGN §8） | 实施位置 | 验证方式 |
|-------------------|---------|---------|
| I-1 全模式只读 | main 无写分支（--write 旗标不存在于 argparse） | 代码审查 + F1 迷你仓文件 mtime/字节双跑不变 |
| I-2 确定性 | 无时间态/随机/网络/git 调用 | F17（双跑输出逐字节一致） |
| I-3 零新规则 | 校验规则集 == DESIGN §4.4 表逐行 | 代码审查（Step 10） |
| I-4 单一真值源 | §2.4 常量 + stats 块数据驱动（代码零模式常量） | F18（模式改 stats 块即生效） |
| I-5 异构于生成端 | 全文件无 LLM/网络 import | 结构性保证 |
| I-6 声明=重数两级 | reconcile ① + ② | F5/F6 |
| I-7 修正轮产出在扫描面 | 模式扫描载体含 CODE_WIKI 版本头区（无豁免区） | F19（版本头叙事数字活靶） |

## 8. 测试策略

### 8.1 selftest fixture 矩阵（23 项）

| # | 场景 | 断言 |
|---|------|------|
| F1 | 合规迷你仓（stats 块 + 五真值源 + 双载体全一致） | verify exit 0，TruthSet 精确断言 |
| F2 | stats 块缺失 | P1 |
| F3 | stats 块双份 / JSON 非法 | P1 |
| F4 | patterns schema 违规（regex 非法 / truth 越界 / scope 越界） | P1 逐条 |
| F5 | declared.spec_feature_dirs 失配 | P1（declared/actual 报文） |
| F6 | living 载体 PT-1 命中值 ≠ 真值 | P2 + 行号断言 |
| F7 | facade 命中值 ≠ baseline | P3 + exit 0 |
| F8 | baseline ≠ 当前真值（滞后） | P3 滞后提示 + exit 0 |
| F9 | §2.1 树缺登 / 幻影 | P2 双向 |
| F10 | §9 索引缺行 / 幻影行 | P2 双向 |
| F11 | doc_registry 版本失配（v1.4 vs 1.4.2） | P2 |
| F12 | 中文数字转换全区间（一~九十九逐值） | cn_to_int 精确断言 |
| F13 | hits 块缺失（真值源损坏） | P1 声波式 |
| F14 | front-matter 不可解析 | P1 |
| F15 | spec/ 目录缺失 | P1 |
| F16 | staged 与作用域无交集 | skip exit 0 |
| F17 | 确定性 | 双跑输出逐字节一致 |
| F18 | I-4 数据驱动：stats 块改模式 → 同仓不同命中 | 模式生效断言 |
| F19 | 版本头叙事数字（修正轮产物）在扫描面 | PT 命中版本头行 |
| F20 | doc_registry 链接形态定位（叙事子串不误命中） | 不命中 dev-log 叙事行 |

另：`circled_to_int` 1-35 逐值断言并入 F12（数字转换单测组）；F7 含双变体——F7b（SVG `>N<` 包含性通道）/ F7c（suppress 白名单单/双匹配，CHECKLIST §2.3 引用），加 I-1 只读断言；F20 为集成轮 DR-H 修复的 TDD fixture（先红后绿，§9.7）——selftest 机械计数 23 项。

### 8.2 集成验证（Step 10，E1 级——已执行，结果回填）

1. `python scripts/repo_stats.py --selftest` → **23/23 PASS** ✓
2. CODE_WIKI §10 stats 块人工起草 → verify 首跑：**实际报 10 项 P2 = 活靶表（§10.3）全部 7 项 + 3 项工具侧误报**（2 处 PT-4 误命中行号/版本片段 + 1 处 doc_registry label 子串定位误命中叙事行——§9.7 DR-H）——真靶全捕获（漏报 0），首跑全绿未发生 ✓
3. 活靶修正 + 误报修复（PT-4 负向后顾 + F20 TDD + 活靶 7 处 prose + CODE_WIKI v1.7 入册）→ **verify exit 0** ✓
4. `.pre-commit-config.yaml` 第三 hook 入册 → `pre-commit run repo-stats --all-files` → 通过 ✓
5. 三校验器全仓回归（dc_validator 49 文件 0 违规 / m7_stats 1 P3 预期 / repo_stats verify exit 0）+ `pre-commit run --all-files` 全绿 ✓（Step 10 终验见 CHECKLIST §8）

### 8.3 活靶集入账

verify 首跑捕获集（活靶全命中证据）入 CHECKLIST §8 验收登记——工具有效性以捕获真实漂移为证，非以全绿为证（DESIGN §4.5）。

## 9. 幻觉排除审查（Step 6 Review）

### 9.1 依赖版本验证

- [x] 零第三方依赖（§2.1）；stdlib API 下限逐条核对（§2.2）
- [x] 无虚构库/函数（ord/chr Unicode 算术为内置；RE_TREE_* 锚定格式已对 §2.1 实态取证）

### 9.2 接口签名验证

- [x] 全部签名可实现（§4 汇总表与 DESIGN §3.2 逐一对应；build_truth_set(spec) 参数为 v1.1 口径追溯的显式依赖）
- [x] 正则无不可达分支；RE_TREE_ENTRY 4 空格缩进锚对 CODE_WIKI §2.1 实树格式已 Read 核实（L74-L84）

### 9.3 实施与设计对齐

- [x] 模块 RS1-RS5 ↔ DESIGN §3.2；校验规则集 ↔ DESIGN §4.4 逐行；不变式 I-1~I-7 ↔ DESIGN §8
- [x] 实施裁定两处显式登记（§3.4 行号状态机 / §2.4 围栏过滤精确语义）——均为 DESIGN 语义的细化非偏离
- [x] v1.1 契约修正已回写 DESIGN（非 IMPLEMENTATION 私改口径——单一真值源纪律）

### 9.4 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| 每模式全文重扫 | 单遍逐行状态机 × 模式库循环（行内多模式 finditer），载体文件各读一次 |
| 围栏剔除后行号映射 | 逐行状态机原生行号（§3.4 裁定） |
| LS 重复枚举 | T1 目录项列表复用（T2 templates 计数同源） |

### 9.5 实施前对账新发现（如实登记）

- [x] DESIGN v1.0 `derived.view_layer_total` 口径错值（35≠33）已修正 v1.1——实施前取证对账的价值首证
- [x] 活靶表扩充：DESIGN §10.3 原列 5 项，本轮取证新增 §2.1 树缺 repo-stats/（活靶 5）+ §9 三版本号⑲发现③ 遗留批（活靶 2-4）+ L54 树注释「双 hook」并入活靶 7 位点集——见 §10.3

### 9.6 Step 9 实施期发现（selftest 首跑 FAIL 捕获，如实登记——DR-D~DR-G）

| # | 发现 | 根因 | 处置 |
|---|------|------|------|
| DR-D | T7 分桶行守卫逻辑反转：`cells[0] == ""` 对所有 `\|` 开头行恒真（split 首段必空）→ 全行跳过 → `view_layer_total` 恒 0 | 守卫本意滤非表格行，写成必真条件 | 改 `len(cells) < 4`（首尾空串 + 载体 + 小计最少段数）；F1/F18 首跑 FAIL 捕获 |
| DR-E | 迷你仓 fixture M7 载体名「Wiki v1/v2」不匹配 `RE_VIEW_CARRIER`（CODE_WIKI\|README\|evidence\.svg）→ T7 求和空转，PT-G/PT-H 基线假 P2 | fixture 与 T7 载体判定契约脱节（同一假值两面：DR-D 使其未暴露） | 载体名改「CODE_WIKI v1/v2」 |
| DR-F | F7 fixture 语义与 §8.1 契约不符：原实现改 living wiki 却断言 README 产 P3（README 未变必无 P3，恒 FAIL）；CHECKLIST §2.3 所引「F7 变体」（SVG `>N<` 通道 / suppress 白名单）未实现 | fixture 先于契约细化撰写，未回读 §8.1/CHECKLIST | 按契约重构：F7 = README prose ≠ baseline → P3 + exit 0；补 F7b（SVG 缺基准文本节点）/ F7c（suppress 单匹配不跳 + 双匹配跳过）；selftest 计数 22 项 = 19 fixture + F7 双变体 + I-1 只读断言 |
| DR-G | F9 树替换串字符错误：beta 为末条目（`└──`），替换串写 `├── beta/` → 未命中，树完整无缺登 P2，断言恒 FAIL | 树字符 ├/└ 语义（末条目 └）在 fixture 转写时失察 | 替换锚改「├── alpha/ + └── beta/」两行块 |

> DR-D/E 为同一失效的两面：解析器守卫 bug 被 fixture 契约脱节掩盖（两者叠加恰好「绿」不了也定位难）——selftest F1 精确断言（TruthSet 逐字段）是捕获器；DR-F/G 为 fixture 自身与文档契约/实树格式的漂移，与 DIS-010 同族（视图层手写枚举漂移的 fixture 微缩版）。22/22 全绿收口。

### 9.7 集成轮实施期发现（verify 首跑误报甄别，如实登记——DR-H~DR-J）

| # | 发现 | 根因 | 处置 |
|---|------|------|------|
| DR-H | doc_registry 行定位用 label 子串匹配：dev-log 索引行「002（cpp-hub-absorption）」含 label 子串「cpp-hub-absorption」，被误判为 §9 索引载体行 → 版本对账报「无版本号 token」而非 v1.1≠1.0 | 行定位语义缺陷：叙事性子串 ≠ 载体行（代码侧缺陷，非 prose 漂移） | 行定位改链接形态（`](./path)` 文件链接或 `](./dir/)` 父目录链接）；**F20 TDD 先红后绿**（复现叙事子串误命中 → 修复 → 23/23） |
| DR-I | PT-4 误命中 2 处：CODE_WIKI L3「L4 feature 目录」行号引用 + discoveries L26「v1.5 feature 目录」版本号片段（述史形态） | 模式设计未区分「计数声明」与「引用/述史」形态边界 | 正则加负向后顾 `(?<!L)(?<![.\d])`——L 前缀行号与 `.` 前缀版本号排除（能改正则不进 suppress，DESIGN §4.3 原则③） |
| DR-J | `declared.hooks: 2` 与第三 hook 入册后实际 3 不符 | 声明与落地时序差（hook 入册 yaml 在前、stats 块声明同步在后） | declared.hooks → 3；rs-decl 通道 P1 当场拦截——**对账器自身的声明也是视图**（元递归实例，同轮被自身看护） |

> 首跑 10 项 P2 = 7 真靶 + 3 误报（DR-H~J）：真靶全捕获证明扫描面有效，误报不姑息且全部 fixture 化/正则化修复（非当次输入补丁）——与样本⑨「校验器自身计数错」构成跨工具同构：**校验器自身缺陷由其 fixture 矩阵自证伪**。误报已登记 M7 样本㉑ 审查配置列，不入发现账。

> **标注（RULE-1/RULE-4）**：本 §9 由同会话自查勾选（单视角）；独立 pass 待 Step 10 或用户触发。

## 10. 实施步骤

| 步 | 动作 | 验证 |
|----|------|------|
| 1 | 写 `scripts/repo_stats.py` 骨架（RS1 CLI + 常量 + CheckResult/StatsSpec/TruthSet） | import 无错 |
| 2 | RS3 解析器 + RS2 枚举器 + 数字转换纯函数 | F2-F5/F12-F15 |
| 3 | RS4 三路对账 + 行号状态机 | F6-F11/F16-F19 |
| 4 | RS5 selftest（20 fixture 迷你仓） | `--selftest` N/N |
| 5 | CODE_WIKI §10 stats 块人工起草（模式库 PT-1~PT-11 全仓试扫定稿） | verify 首跑捕获 §10.3 全活靶 |
| 6 | 活靶修正 + CODE_WIKI v1.7 入册 | verify exit 0 |
| 7 | `.pre-commit-config.yaml` 第三 hook | `pre-commit run repo-stats --all-files` |
| 8 | 三校验器 + pre-commit 全量回归 | 全绿 |

**LOC 预估（DESIGN §10.1-3 核对义务，Step 9 后回填实际值）**: 预估 ~650 行（核心校验/枚举/对账 ~380 + 数字转换与常量 ~80 + selftest 19 fixture 迷你仓模板 ~190）。预估口径已含 selftest（P-008/m7_stats 双教训：口径必须显式）。**实际 1276 行**（wc -l / ReadAllLines.Count，2026-08-22 集成轮收口；Step 9 时点曾记 1257，F20 TDD + doc_registry 链接定位重构 +19）——超估 92%，主因三块：① stats 块 schema 校验（carriers/patterns/declared/view_layer_samples/doc_registry/facade_baseline/suppress 七节逐条 P1 报文）预估时按 m7_stats hits 五键规模估、实际七节；② facade 双通道（prose 基准比对 + SVG `>N<` 包含性）+ suppress 白名单为 DESIGN 后补契约、预估未单列；③ F7 双变体 + 19+1 fixture 迷你仓模板（含 MINI_M7 分桶表全结构）~470 行。核心校验/枚举/对账实际 ~560 行（超估 47%，schema 报文分支为主）。

### 10.3 已知活靶（verify 首跑预期捕获全集——E1 取证于本 IMPLEMENTATION 撰写轮）

| # | 位点 | 现值 | 真值 | 对应规则 | 取证 |
|---|------|------|------|---------|------|
| 1 | CODE_WIKI §9 缺 `spec/repo-stats/` 索引行 | 缺行 | 10 feature 目录（LS） | rs-list | DESIGN §10.3-1 |
| 2 | CODE_WIKI §9 L627「断言分级证据框架 v1.4」 | v1.4 | front-matter 1.4.2 | rs-list 版本对账 | DESIGN §10.3-2 + 本轮 Grep 复核 |
| 3 | CODE_WIKI §9 L635「文档规范改造方案 v1.5」 | v1.5 | front-matter 1.6 | rs-list 版本对账 | **本轮新取证**（Grep PLAN.md L4） |
| 4 | CODE_WIKI §9 L637「LangGraph 框架化调研 v1.1」 | v1.1 | front-matter 1.2 | rs-list 版本对账 | **本轮新取证**（Grep LANGGRAPH L4） |
| 5 | CODE_WIKI §2.1 树缺 `repo-stats/` 目录条目（L74-L84 段） | 缺条目 | 11 条（含 templates） | rs-list | **本轮新取证**（Read L48-L85） |
| 6 | CODE_WIKI L67 / L630「P-001~P-013」 | 013 | P-014（PROGRESS 表 14 行） | rs-pattern PT-11 | DESIGN §10.3-3 |
| 7 | CODE_WIKI L4/L5 + L54 树注释「双 hook」（repo-stats hook 入册后） | 双 | 三 | rs-pattern PT-8 | DESIGN §10.3-4 + L54 本轮扩展 |

> 活靶 2-4 为样本⑲发现③（「§9 三处版本号半修态」）的**遗留批**：⑲轮发现清单含此三项，但⑳轮 8 位点修正与 v1.6.2 终值修正均未覆盖（⑳轮只核对⑲发现①②④）——四连残留链⑰→⑱→⑲→⑳ 之外的第五环实证（发现声明与修正执行的分离在**发现条目粒度**上复发），repo_stats rs-list 版本对账通道的直接靶。活靶 5 为 spec 流程自身产生活漂移的最新实例（repo-stats/ 目录建于 P-014 Step 1，视图载体尚未同步——DIS-010 结构根因「视图同步无触发器」的过程实证）。**首跑全 7 项捕获 = 工具有效性实证；若首跑全绿即证伪扫描器。**
>
> **首跑实录（2026-08-22 集成轮）**：verify 首跑报 10 项 P2 = 上表全部 7 项（漏报 0）+ 3 项工具侧误报（DR-H~J，§9.7）——活靶预测与实跑全对齐；7 项活靶全修正（CODE_WIKI v1.7）+ 3 项误报 fixture 化修复后 verify exit 0。活靶集已入 M7 样本㉑（形态 II = 版本号×3 + 计数×4，规律② 第六层收束注）。

### 10.4 历史叙事位点处置预案（集成轮执行）

| 位点 | 现文 | 处置 | 理由 |
|------|------|------|------|
| CODE_WIKI §6 L561「P-011 扩为双 hook」 | 历史时点叙事 | 改写为「P-011 扩为双 hook、P-014 扩为三 hook」——PT-8 命中「三 hook」= 真值通过 | 历史叙事含当前值锚，机械可过且语义保真（suppress 豁免为次选——能改措辞不进白名单） |

---

**Review 签字**: _________ 日期: _________（自查（单视角）完成，独立 pass 待 Step 10 / 用户触发）
