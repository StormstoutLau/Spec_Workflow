# 实施文档：pre-commit + DC 契约校验器

---
id: precommit-dc-validator-IMPLEMENTATION
type: design
version: 1.2
status: verified
date: 2026-08-19
depends: [precommit-dc-validator-DESIGN, precommit-dc-validator-RESEARCH]
upstream: null
---

> **Feature**: precommit-dc-validator（PROGRESS P-007）
> **创建日期**: 2026-08-19
> **状态**: verified（独立 pass 通过，2026-08-20）
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md) v1.2
> **基于调研**: [RESEARCH.md](./PRECOMMIT_DC_VALIDATOR_RESEARCH.md) v1.1
> **审查状态**: v1.1 经独立 pass（2026-08-20，DeepSeek V4 Pro **真异基座**——生成端 GLM-5.3，RULE-1 时序独立 + RULE-5 模型异质性双满足）：E1 四通道复核全过（selftest 13/13 重跑 / 全仓 dry-run 39 文件 0 违规 / 双跑逐字节一致 I-2 / pre-commit 通道 Passed）；词表常量与 DESIGN §6.3 逐字符核对一致（I-4）；DR-5/DR-6 修复重验通过。发现 3 P3（§4.3/§4.5 签名声明未覆盖 `root=ROOT` 实施参数 / CHECKLIST §8.1 跨模块映射断言不实 / DESIGN §10.1-4 LOC 核对缺位）→ v1.2 修正注 + DR-7；M7 样本⑬（映射闭合 1 处）
> **v1.2 变更（2026-08-20）**: 独立 pass 修正——§4.3/§4.5 补 `root=ROOT` 实施参数声明（P3-1）；§10 增 DR-7（LOC 对账登记）；status draft → verified

---

## 1. 实施概述

实施方案 = 单文件零依赖 Python 脚本 `scripts/dc_validator.py`（五模块 M1-M5）+ `.pre-commit-config.yaml`（`repo: local` / `language: system` 单 hook）。落点与承载形态完全沿用 [DESIGN §3](./DESIGN.md)。本实施文档的关键增量是三项**实施期已完成的机械取证**（2026-08-19，全仓扫描，E1 可重放）：

1. **DC 契约范围实测**：全仓 33 个 `.md` 中 24 个带七字段 front-matter（14 个首行式 + 10 个标题后式——`SPEC_PROCESS.md`、`ADR-0004/0005`、`FWK-ASSERTION`、`DIS-007`、5 个模板的 front-matter 位于标题后 L3-4），9 个轻契约文档（README×2、CODE_WIKI、M7、PROGRESS、dev-log×2、discoveries README、docs/adr README）无 front-matter。**M2 检测窗口由此定为"前 10 行内 `---` 围栏 + 开围栏后首个非空行必须为 `key: value` 形态"**——严格首行判定会漏掉 10 个契约文件；而仅凭围栏判定会把 README/CODE_WIKI/dev-log 的**装饰性 `---` 分隔线**误判为 front-matter（dry-run 首跑实测 5 处误报，解析器加"首个非空行"规则后清零，selftest F10 覆盖）。
2. **§0 计数对账预跑**（M4 规则验证）：4 份含断言统计表的调研文档中，LANGGRAPH（A/B/H 全对）、PRECOMMIT（全对）、CPP_HUB_GAP（A=16 全形态命中对、B/H 对）三份与机械重数吻合；**ADR0006_POINTER 声明 A=7 实测 8 条**——逐条核实 L30/L41/L45/L48/L51/L54/L61/L62 均为"本地路径+引文锚定"形态的真 A 类断言，声明值为手填漏计（形态 II 实例，M7 登记见 CHECKLIST）。修复随本 feature 提交。
3. **断链预扫**（M5 规则验证）：真断链 2 处（ADR-0004/0005 L21 的 `../../SPEC_PROCESS.md`——`adr/` 上一级即仓库根，`../../` 跳出仓库，应为 `../`）；引文内链接 3 处（ADR0006_POINTER L49/L113，属源仓库路径空间的原文快照，不改）；模板占位链接 6 处（`spec/templates/` 天然不指向真实文件）。

## 2. 工程细节

### 2.1 技术栈

| 组件 | 技术 | 版本 | 验证状态 |
|------|------|------|---------|
| 语言 | Python（stdlib only） | 3.8+ 语法 / 3.12 主验 | ✅ 主控站 3.12 实测启动 0.04s |
| front-matter 解析 | **stdlib 手写解析器**（`re`） | — | ✅ 全仓 23 文件实测解析（见 §2.2 决策） |
| hook 承载 | pre-commit | 4.6.2 | ✅ 已装于主控站 Python 3.12（pip 实测） |
| 依赖管理 | 无（零第三方依赖） | — | ✅ |
| YAML 解析库 | PyYAML | 6.0.3（Python 3.12 site-packages） | ✅ 已验证存在，**但不采用**（见下） |

**YAML 解析选型决策（DESIGN §10.1-5 落定）**：采用 stdlib 手写解析器，不引入 PyYAML。理由：

1. **I-2 确定性最大化**：实测 hermes venv Python 3.11 的 site 初始化延迟 353 秒（2026-08-19 计时取证），其 `-S -E` 绕过模式下 PyYAML 不可用（`No module named 'yaml'`）；零依赖脚本对**任何** PATH 上的 Python 3.8+ 可运行，消除 RESEARCH H3 环境风险。
2. **契约格式规整**：全仓 23 个 front-matter 均为"单行 `key: value` + 流式数组 `[a, b]` + `null`"三种值形态（机械扫描实证），无多行列表/锚点/引号转义——手写解析器 ~30 行覆盖全集，且能按同一规则检测"值内裸冒号"类结构错误（YAML 解析错误检测先例，RESEARCH §2.2）。
3. **pre-commit 依赖巧合不构成可用性保证**：pre-commit 自身依赖 PyYAML，但 `language: system` hook 的 `entry` 在系统 PATH 环境执行，**不继承 pre-commit 的安装环境**——不能假设运行脚本的 Python 就是装 pre-commit 的 Python。

### 2.2 依赖版本验证

| 依赖 | 声明版本 | 实测 | 兼容性 | 验证方式 |
|------|---------|------|--------|---------|
| pre-commit（承载层） | 4.x | 4.6.2 已装 Python 3.12 | ✅ | `pre-commit --version`（pip 安装日志 2026-08-19） |
| Python stdlib（`re/os/sys/argparse/dataclasses`） | 3.8+ | 3.12 全可用 | ✅ | 本机实测；无 3.12+ 专属 API（Step 6 stdlib 下限检查） |
| PyYAML | 不采用 | — | — | 见 §2.1 决策 |

### 2.3 文件结构

```
Spec_Workflow/
├── .pre-commit-config.yaml          # 新增：单 hook 声明（repo: local）
└── scripts/
    └── dc_validator.py              # 新增：M1-M5 五模块 + --selftest（单文件）
```

无包结构、无 pyproject.toml、无独立测试文件——仓库"纯文档"身份下代码面最小化（DESIGN §1）；自测内嵌 `--selftest` 子命令（fixture 经 `tempfile` 构造于系统临时目录，I-1 只读不破坏工作树），测试入口与被测对象同文件，E1 可重放（`python scripts/dc_validator.py --selftest`）。

## 3. 模块实施

### 3.1 M1 CLI 入口

#### 职责

子命令解析（DESIGN §4.1 四个 `--check-*` + `--check-all` 默认 + `--selftest`）/ 分发 / 聚合 / 退出码映射。

#### 接口签名

```python
def main(argv: list[str] | None = None) -> int:
    """0 全部通过 / 1 发现契约违规 / 2 工具自身错误"""
```

#### 实施要点

- 位置参数 = pre-commit 传入的 staged 文件列表；**无位置参数时默认全仓枚举**（DESIGN §3.4 独立调用语义）
- namespace 检查（M3）**永远全仓枚举**，不受 staged 列表约束（防"staged-only 造成 DC4 假通过"）
- 顶层 `try/except` 包裹分发，未捕获异常 → exit 2（DESIGN §3.4 补注：工具崩溃绝不静默放行）
- `--check-frontmatter/--check-counting/--check-links/--check-namespace` 可组合，`--check-all` = 全选

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| 每文件重复读盘（M2/M4/M5 各读一次） | 每文件读一次 `text` 传入三检查 |
| 全仓枚举走 `git ls-files`（子进程开销 + git 依赖） | `os.walk` 纯 stdlib，排除 `.git`/`__pycache__`，33 文件毫秒级 |

### 3.2 M2 frontmatter

#### 职责

front-matter 存在性/范围判定 + DC1 七字段齐全 + DC2 type/status 词表（design 二档）。

#### 接口签名

```python
def check_frontmatter(file: str, text: str) -> list[CheckResult]:
    """YAML 无法解析时返回 severity=P1 的 yaml-unparsable 结果，不抛异常"""
```

#### 实施要点

- **检测窗口**：前 10 行内首个 `---` 行为开围栏，至下一个 `---` 行闭围栏——覆盖首行式（14 文件）与标题后式（10 文件）两种实测形态（§1 取证 1）；**开围栏后首个非空行必须为 `key: value` 形态**，否则视为装饰性分隔线（README/CODE_WIKI/dev-log 场景，dry-run 首跑 5 处误报的修复规则，selftest F10 覆盖）
- 手写解析：逐行 `re.match(r"^([A-Za-z_-]+):\s*(.*)$")`；值形态三分支——`[a, b, c]` 流式数组 / `null` / 裸标量（剥引号）；**结构错误检测**：围栏内已有 key: value 行后出现无结构行 → `yaml-unparsable` P1
- 无 front-matter → 返回 `[skip]` 空结果（非违规，DC 契约范围外，DESIGN §7 末行）
- DC1：七字段 `id/type/version/status/date/depends/upstream` 逐一存在，缺失报 P1
- DC2：`type` ∈ 六类词表（非法报 P1）；`status` 判定——`type: design` 且 `id` 以 `-CHECKLIST` 结尾 → CHECKLIST 词表 `{pending, accepting, accepted}`，否则按 TYPE_VOCAB（PLAN v1.6 DC2 消歧，DESIGN §6.3 常量原样落地）
- 词表常量逐字符复制 DESIGN §6.3（单一真值源 I-4：本文件不新定义任何取值）

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| PyYAML 全量 YAML 语义解析（超集能力闲置） | 30 行定向解析器只覆盖契约声明的三种值形态 |

### 3.3 M3 namespace

#### 职责

DC4 id 全仓唯一。

#### 接口签名

```python
def check_namespace(files: list[str]) -> list[CheckResult]:
    """每个重复 id 至少一条 P1；无重复返回空列表"""
```

#### 实施要点

- 输入 = 全仓 `.md` 枚举（M1 强制传入，非 staged-only）
- 每文件提取 front-matter `id`（复用 M2 解析器）；无 id 的文件跳过
- 重复 id → **所有重复方各一条 P1**（不只报后者，DESIGN §7）
- 实测基线：当前 23 个 id（含 5 个模板占位 id）零重复——dry-run 应零违规

### 3.4 M4 counting

#### 职责

R7——§0 断言统计表各计数 = 机械重数。

#### 接口签名

```python
def check_counting(file: str, text: str) -> list[CheckResult]:
    """declared ≠ actual 时每条计数差一条结果（附 declared/actual）"""
```

#### 实施要点（规则经全仓预跑校准，§1 取证 2）

- 范围：含 `## 0.` 断言统计表节的文件（当前 4 份调研文档）；无 §0 的文件跳过
- **A 类机械口径**：`(?:^|\|\s*)【A】` 计数 = 行首断言标记 + 表格单元格内标记（CPP_HUB_GAP 的 11 条机制证据为表格内形态，纯行首口径会漏）；修正记录行的句中自引用字面（LANGGRAPH L26 场景）因前驱字符非 `|`/行首而天然不匹配
- **B 类机械口径**：`"id":\s*"B\d+"` 计数（附录 B 机读登记）
- **H 类机械口径**：`\[H\d+\]` 计数（附录 C 假设区条目）
- **C 类首版不对账**（derived-requirement DR-2，见 §10）：实测 C 类标记格式无统一契约——原生文档（LANGGRAPH/PRECOMMIT）行首 `【C】` = 声明值，吸收文档（ADR0006 1/3、CPP_HUB_GAP 2/3）为语义计数（选项表/ rationale 未行内标注），无单一机械口径可对账；待 FWK-ASSERTION 统一 C 类标记格式后启用
- declared 提取：§0 表格行 `^\|\s*A\s*事实类\s*\|\s*(\d+)` 等四行
- 不一致 → P1，报 `[P1] §0 <级别> 声明 n 实为 m`（DESIGN §7）

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| §0 节定位全文正则回溯 | 单遍行扫描状态机（进入/退出 `## ` 节标题即切换） |

### 3.5 M5 linkcheck

#### 职责

DC3 档 1——仓库内相对链接可解析。

#### 接口签名

```python
def check_links(file: str, text: str) -> list[CheckResult]:
    """每个不可解析的仓库内相对链接一条结果；档 2-4 标注仅格式检查不跨仓解析"""
```

#### 实施要点（规则经全仓预扫校准，§1 取证 3）

- 提取 `](...)`，跳过 `http://`/`https://`/`#`/`mailto:`
- **排除上下文一**：fenced code block（``` 围栏之间）——附录 B `assertions` 登记块内的链接属引文快照
- **排除上下文二**：引文行（行含 `引文:` 或 `"quote":`）——被引原文的链接描述源仓库路径空间，非本仓导航（ADR0006_POINTER L49/L113 实测场景；改引文 = 篡改证据）
- **排除上下文三**：`spec/templates/` 目录——模板占位链接（`./DESIGN.md` 等）实例化前天然不指向真实文件（derived-requirement DR-3）
- 档 2-4 标注识别：链接文本以 `源项目·` / `外部·` / `本地工具·` 开头 → 跳过解析（DC3 四档，PLAN §1）
- 其余相对路径：剥 `#锚点`，以文件所在目录 resolve，`os.path.exists` 判存在；不存在 → P2
- 实测基线：修复 ADR-0004/0005 两处真断链后 dry-run 应零违规

#### 低效操作排除

| 潜在低效 | 排除措施 |
|---------|---------|
| 每链接一次 `stat` 系统调用 | 33 文件 × ~10 链接量级下无感知开销，不做缓存（避免过度工程） |

## 4. 接口实施

### 4.1 main（M1）

```python
def main(argv: list[str] | None = None) -> int:
    """实现: argparse 解析 --check-*/--selftest + 位置参数文件列表；
    分发逐文件检查（staged 或全仓）+ 强制全仓 namespace；
    聚合 Summary；0/1/2 三态退出码，顶层异常兜底 exit 2"""
```

**签名一致性**: 与 DESIGN §4.1 一致 ✅

### 4.2 check_frontmatter（M2）

```python
def check_frontmatter(file: str, text: str) -> list[CheckResult]:
    """实现: 前 10 行窗口找围栏 → 手写解析 → 七字段 → 词表（design 二档）"""
```

**签名一致性**: 与 DESIGN §4.2 一致（+`text` 参数为读盘复用的实施优化，语义不变）✅

### 4.3 check_namespace（M3）

```python
def check_namespace(files: list[str]) -> list[CheckResult]:
    """实现: dict[id] -> [files] 倒排，len>1 的 id 全方各报 P1"""
```

**签名一致性**: 与 DESIGN §4.3 一致 ✅
**v1.2 修正注（独立 pass P3-1）**: 实际签名 `check_namespace(files, root=ROOT)` 另含 `root=ROOT` 默认参数（selftest F6 以 `root=tmp` 隔离 fixture 所需）——与 `+text` 同类实施参数，生产缺省即全仓语义、契约不变；v1.1"一致"声明未覆盖该参数，补记

### 4.4 check_counting（M4）

```python
def check_counting(file: str, text: str) -> list[CheckResult]:
    """实现: §0 节定位 → declared 提取 → A/B/H 三类机械重数 → 差值报告"""
```

**签名一致性**: 与 DESIGN §4.4 一致（+`text` 参数，同 4.2）✅

### 4.5 check_links（M5）

```python
def check_links(file: str, text: str) -> list[CheckResult]:
    """实现: 链接提取 → 三排除上下文 → 档 2-4 标注识别 → 相对路径存在性"""
```

**签名一致性**: 与 DESIGN §4.5 一致（+`text` 参数，同 4.2）✅
**v1.2 修正注（独立 pass P3-1）**: 实际签名 `check_links(file, text, root=ROOT)` 另含 `root=ROOT` 默认参数（selftest F8b 的 fixture 根解析所需），同类实施参数，v1.1 未声明，补记

### 4.6 CheckResult / Summary（数据结构）

DESIGN §6.1/§6.2 `dataclass` 原样落地（`frozen=True` CheckResult 五字段；`Summary.results/passed/violations`）。✅

## 5. 兼容性

### 5.1 Python 版本兼容

| Python 版本 | 支持 | 说明 |
|------------|------|------|
| 3.12 | ✅ | 主控站主验环境（pre-commit 4.6.2 安装处） |
| 3.8-3.11 | ✅ | 语法层兼容（无 match/`X | Y` 运行时注解依赖——注解用 `from __future__ import annotations` 或字符串化） |
| 3.7- | ❌ | 不声明支持（dataclasses 3.7 可用但无验证环境，不做虚假承诺） |

### 5.2 依赖兼容

| 依赖组合 | 兼容性 | 验证 |
|---------|--------|------|
| 零第三方依赖 × 任意 Python 3.8+ | ✅ | 结构性保证（仅 stdlib） |

### 5.3 向后兼容

无历史版本——本脚本为仓库首个入库代码，无兼容负担。`.pre-commit-config.yaml` 不影响未安装 pre-commit 的环境（文件存在但 hook 未安装时不生效；`pre-commit install` 后才拦截提交）。

### 5.4 操作系统

Windows（主控站，entry 走 `python` 前缀规避 `/bin/sh`，RESEARCH §2.1 陷阱）✅；Ubuntu（工作站 A/B，`os.walk`/`os.path` 跨平台）✅。路径分隔符统一 `os.path.join`/`normpath`，不硬编码 `\` 或 `/`。

## 6. 错误处理实施

### 6.1 错误场景与处理

| 错误场景（DESIGN §7） | 异常类型 | 处理代码 | 测试 |
|------------------------------|---------|---------|------|
| front-matter 无法解析（无 key 结构/围栏不闭合） | 不抛异常 | `check_frontmatter` 返回 `yaml-unparsable` P1 | selftest F2 |
| 七字段缺失 / 词表非法 | 不抛异常 | M2 逐字段 P1/P2 结果 | selftest F1/F3 |
| id 重复 | 不抛异常 | M3 全方 P1 | selftest F6 |
| §0 计数 ≠ 重数 | 不抛异常 | M4 declared/actual P1 | selftest F4 |
| 工具自身异常（IO 等） | 任意 | M1 顶层 except → exit 2 | selftest F7（异常注入） |
| 非 DC 范围 .md | 不抛异常 | `[skip]` 空结果 | selftest F5 + dry-run（10 个轻契约文件） |

## 7. 不变式实施

| 不变式（DESIGN §8） | 实施位置 | 验证方式 |
|---------------------------|---------|---------|
| I-1 只读 | 全脚本无写文件调用（selftest 的 tempfile 属系统临时目录，不触工作树） | grep 无 `open(..., 'w')`（dry-run 后 git status 工作树无越界改动，E1） |
| I-2 确定性 | 无时间/网络/随机调用；`os.walk` sort 稳序 | dry-run 两次运行输出逐字节一致 |
| I-3 零新规则 | 检查项逐一对应 DC1-DC4/R7，无额外发明 | CHECKLIST §1 文档一致性验收逐项核对 |
| I-4 单一真值源 | 词表常量逐字符复制 DESIGN §6.3（源头 PLAN v1.6/ADR-0007 D4） | 常量 diff 核对 |
| I-5 异构于生成端 | 计数/唯一性 = 纯 `re`/`os` 机械枚举，无 LLM 判断 | 代码结构审查（无网络/模型调用） |

## 8. 测试策略

### 8.1 单元测试（--selftest，E1 可重放）

| fixture | 覆盖 | 断言 |
|---------|------|------|
| F1 七字段缺 `depends` | DC1 缺字段 | P1 且 message 含字段名 |
| F2 围栏内无键值行 | yaml-unparsable | P1 标记 `yaml-unparsable` |
| F3 `status: bogus` | DC2 词表 | P1 且 message 含允许词表 |
| F4 §0 声明 A=3 实写 2 | R7 计数差 | P1 含 declared=3 actual=2 |
| F5 无 front-matter 文件 | 范围外跳过 | 零结果零违规 |
| F6 两文件同 id | DC4 重复 | 双方各一条 P1 |
| F7 构造非 .md 传入 | 异常路径 | 不崩溃，exit ∈ {0,1} |
| F8 断链 + 档 2 标注链接 + 引文行链接 | DC3 分档 | 仅真断链报 P2 |
| F9 合规七字段文件 | 零误报 | 零结果 |
| F10 无 front-matter 但含装饰性 `---` 分隔线 | 范围判定（dry-run 首跑 5 误报的回归覆盖） | [skip] 非违规 |

selftest 输出 `N/N PASS` 或首条失败详情，退出码 0/1。

### 8.2 集成测试（dry-run）

`pre-commit run dc-validator --all-files`（staged 语义全量模拟）+ `python scripts/dc_validator.py`（独立全仓调用）双通道，全仓 `.md` 零违规为通过线（真违规修复后；文件数随 feature 文档落地递增，v1.1 实测 34 = 33 存量 + IMPLEMENTATION.md 自身，CHECKLIST.md 落地后 35）。

### 8.3 属性测试

不适用（无代数性质可测；确定性 I-2 以"双跑一致"替代，见 §7）。

## 9. 幻觉排除审查（Step 6 Review）

> 以下 checkbox 为 2026-08-19 实施自查标注（历史保留）。**独立 pass 已完成（2026-08-20，DeepSeek V4 Pro 真异基座，RULE-1 时序独立 + RULE-5 模型异质性双满足）**：§9.1-§9.4 逐项复核确认；复核证据 = selftest 13/13 重跑 + 全仓 dry-run 39 文件 0 违规 + 双跑逐字节一致（I-2）+ pre-commit 通道 Passed + 词表常量逐字符核对（I-4）。接口签名一项发现 P3-1（`root=ROOT` 实施参数漏声明），已补 §4.3/§4.5 修正注。

### 9.1 依赖版本验证

- [x] pre-commit 4.6.2 本机实测安装（pip 日志 2026-08-19，`.tmp_pip.txt` 已核）——自查
- [x] 零第三方依赖声明与 §2.1 决策一致——自查
- [x] stdlib API 下限检查：`re/os/sys/argparse/dataclasses/pathlib/tempfile` 均 3.8+ 可用（无 `Decimal.ulp` 类 3.12+ 专属 API）——自查

### 9.2 接口签名验证

- [x] 五接口与 DESIGN §4 一致（`text` 参数差异已在 §4 显式声明为读盘复用优化）——自查
- [x] 无虚构库/函数——自查

### 9.3 实施与设计对齐

- [x] M1-M5 ↔ DESIGN §3.2 一一对应；数据结构 ↔ §6 一致——自查
- [x] 设计未覆盖的实施决策（检测窗口 10 行 / A 类表格口径 / C 类不对账 / 三排除上下文 / templates 排除 / selftest 内嵌）全部显式登记（§3 各模块 + §10 DR 表）——自查

### 9.4 低效操作排除

- [x] §3 各模块低效排除表——自查

## 10. 派生需求登记（Step 8 预登记）

| # | 派生需求 | 来源 | 处置 |
|---|---------|------|------|
| DR-1 | front-matter 检测窗口 = 前 10 行内围栏（非严格首行） | 实施期全仓扫描发现双形态（§1 取证 1） | 本文档 §3.2 声明；后续可提契约显式化（PLAN DC1 注记，另行裁决） |
| DR-2 | M4 首版不对账 C 类计数 | C 类标记格式无统一契约（§3.4） | 待 FWK-ASSERTION 后续版本统一 C 类标记格式后启用对账 |
| DR-3 | M5 排除 `spec/templates/`、引文行、fenced block 内链接 | 模板占位符/引文快照天然不可解析（§3.5） | 本文档 §3.5 声明；语义依据 = DC3 档 2-4 的"非本仓路径空间"外延 |
| DR-4 | 自测内嵌 `--selftest` 而非独立测试文件 | 仓库纯文档身份的代码面最小化（§2.3） | 本文档 §8.1 |
| DR-5 | 修复 2 处存量真断链（ADR-0004/0005 `../../` → `../`）+ 1 处存量计数漏计（ADR0006 A 7→8） | M4/M5 预跑捕获（§1 取证 2/3） | 随本 feature 同 commit 修复；M7 登记见 CHECKLIST |
| DR-6 | selftest 汇总计数由硬编码 `12/12` 改为 expect 自增机械计数（v1.0 打印 13 行 PASS 却声称 12/12——**计数校验工具自身犯计数错**，形态 II 在审查臂的实例） | Step 6 复验发现（2026-08-19） | 已修复（`total[0] += 1` 自增，R7 同构原则应用于工具自身）；实测 13/13 PASS；M7 登记见 CHECKLIST |
| DR-7 | 代码量与 DESIGN §10.1-4 "~100 行"估算的核对缺位——独立 pass 实测 **422 行**（selftest 块 ~104 行） | P-008 独立 pass 发现（2026-08-20；DESIGN 约束 4 明示"实施时核对"，v1.1 无 LOC 对账） | 本行即核对登记：膨胀源 = 内嵌 selftest（DR-4）+ CLI 参数矩阵 + 错误处理路径（均有对应验收项承载），功能契约与 I-3 零新规则不受影响；RESEARCH H2 估算按 ~3× 偏差入账，作后续规模估算校准参考 |

## 11. 实施步骤

### Step 1: 脚本落地

- 文件: `scripts/dc_validator.py`
- 内容: M1-M5 + CheckResult/Summary + TYPE_VOCAB 常量 + `--selftest`
- 测试: `python scripts/dc_validator.py --selftest` → 13/13 PASS（v1.1 机械计数；v1.0 硬编码 12/12 为手填计数缺陷，见 DR-6）

### Step 2: hook 配置落地

- 文件: `.pre-commit-config.yaml`
- 内容: `repo: local` 单 hook（id: dc-validator, entry: python scripts/dc_validator.py, language: system, files: \.md$）
- 测试: `pre-commit run dc-validator --all-files` → Passed

### Step 3: 存量违规修复（DR-5）

- 文件: `adr/ADR-0004...md`、`adr/ADR-0005...md`（断链）、`spec/adr0006-pointer/ADR0006_POINTER_RESEARCH.md`（A 计数 7→8 + 修正注）
- 测试: dry-run 零违规

### Step 4: 全仓 dry-run 双通道验收

- `pre-commit run dc-validator --all-files` + 独立 `python scripts/dc_validator.py`
- 通过线（v1.1 实测）: 34 文件，25 契约文件全检查通过，9 轻契约 [skip]，exit 0

---

**Review 签字**: DeepSeek V4 Pro（真异基座独立 pass：RULE-1 时序独立 + RULE-5 异构于生成端 GLM-5.3，双满足） 日期: 2026-08-20 —— 3 P3 全登记修正（本文件 v1.2），无 P1/P2，验收通过
