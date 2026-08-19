---
id: precommit-dc-validator-DESIGN
type: design
version: 1.2
status: draft
date: 2026-08-18
depends: [precommit-dc-validator-RESEARCH, ADR-0007, SPEC-PROCESS, FWK-ASSERTION, doc-contract-refactor]
upstream: null
---

# 设计文档：pre-commit + DC 契约校验器

> **Feature**: precommit-dc-validator（PROGRESS P-007）
> **创建日期**: 2026-08-18
> **状态**: draft（草稿）
> **Spec 步骤**: Step 3-4
> **基于调研**: [RESEARCH.md](./PRECOMMIT_DC_VALIDATOR_RESEARCH.md) v1.1（经同基座复验）
> **审查状态**: v1.1 经复验（2026-08-18，DeepSeek V4 Pro，**同基座新上下文**——RULE-1 时序独立满足、RULE-5 模型异质性未满足，真异基座需另开 GLM 会话）：§2.1 六行映射全部可追溯；引用文件/章节/行号（PLAN L55-60）全核实；发现 P2-1（§6.3 词表双轴歧义未裁决，已升格为实施前置条件）+ P3-2（§3.4 退出码 2 路径，已补注）并修正
> **v1.2 变更（2026-08-18）**: P2-1 前置条件闭合——[PLAN v1.6 §1 DC2](../doc-contract/PLAN.md) 消歧落地（design 增两行，判别规则 = id 后缀 `-CHECKLIST`；E1 全仓 14 份 design 文档零违规）+ [ADR-0007 D4](../../adr/ADR-0007-unified-document-contract.md) 澄清追记。**v1.1 引证勘误**：v1.1 P2-1 注称"PLAN L59 design 状态"——实际 L59 为"template 实例"行，design 词表 v1.6 前载于 PLAN 头部注 + ADR-0007 D4（DC2 表原缺 design 行）；该引证错误入 M7 样本⑧（行号桶，实施期自查发现，规律④ 第二实例）

---

## 1. 设计目标

把 DC1-DC4 契约 + R7 计数规则从"文档纪律"变成"提交瞬间机器拦截"。校验器是**契约的机器可读定义**——只读、只报、永不自动修复（与 RULE-5 单向权限、ADD"审计者永不自动修复"同构）。直接命中的失效模式是 M7 账本实证的最高频形态（形态 II：低语义载荷字段靠弱记忆手填，11 处复发），拦截层 = E1 机械枚举而非 LLM 自查（M7 规律③）。

同时保持仓库"纯文档方法论"身份：脚本是契约的执行器而非业务代码，代码量最小化（~100 行，见 RESEARCH H2），不引入运行时、不绑定模型、不依赖部署（RESEARCH §3.1）。

## 2. 设计依据

### 2.1 调研结论

| 调研发现 | 设计决策 | 引用 |
|---------|---------|------|
| `repo: local` + `language: system` 完全覆盖承载需求 | 校验器落点 = `.pre-commit-config.yaml`（`repo: local`）+ `scripts/dc_validator.py`（`language: system`） | RESEARCH §2.1 / §3.2.1 |
| Windows 下 shell entry 触发 `/bin/sh not found` | entry 一律 `python scripts/dc_validator.py`，禁用 shell 命令 / bash 脚本 | RESEARCH §2.1【A】/ §5.2.1 |
| 五大机械检查点可全部映射为本地 hook（B1） | 校验器五检查 = M2-M5 + 前置 YAML 解析 | RESEARCH §2.3 B1 / §5.1 |
| 计数检查可前移到提交瞬间，拦截形态 II（B2） | R7 计数检查绑定到 pre-commit `--check-counting` | RESEARCH §2.3 B2 |
| 只读校验约束（§5.2 约束 2） | 不变式 I-1 | RESEARCH §5.2 |
| 单一真值源约束（§5.2 约束 3） | 不变式 I-3 / I-4 | RESEARCH §5.2 |

### 2.2 相关 ADR

| ADR | 决策 | 对本设计的影响 |
|-----|------|--------------|
| [ADR-0007 D4/D5](../../adr/ADR-0007-unified-document-contract.md) | `design` 入 type 词表（六类）+ 英文 token 为准 | 校验器 DC2 词表取值的权威源；本设计 front-matter `type: design`/`status: draft` 合法 |
| [ADR-0007 附录 A](../../adr/ADR-0007-unified-document-contract.md) | 编号命名空间登记（稳定 ID 入全局） | DC4 检查的"id 是否已登记"判定依据 |
| [ADR-0008](../../adr/ADR-0008-spec-process-review-gate-and-bidirectional-check.md) | Step 2 门禁 + Step 8 双向引用（grep 级机械检查） | 双向引用 grep 检查与 §10 风险"v1 范围外"的关联，见 §2.3 能力边界 |
| [SPEC-PROCESS v1.4 Step 8](../../SPEC_PROCESS.md) | 文档一致性双向引用/断言延续 | 同 ADR-0008，属相邻非核心检查 |

### 2.3 职责边界

**职责内（本设计回答）**
1. DC1：front-matter 七字段（`id/type/version/status/date/depends/upstream`）齐全性
2. DC2：`type` 六类 + 各 `type` 状态词表取值（权威定义见 PLAN §1 DC2 与 ADR-0007 D4/D5）
3. DC4：`id` 全仓唯一 + 命名空间登记状态可查
4. R7：`§0 断言统计表`各计数 = grep 机械重数
5. DC3：相对链接四档标注（档 1 仓库内相对路径可解析）

**职责外（不回答——独立研究范式，不吞并）**
- 论证质量 / 归因扭曲（DC 契约只管形态）——属 ADD 审计（Step 10）与 Step 4 人工审查职责，机器不可判
- 拼写 / 排版格式——属 markdownlint / prettier 通用工具职责，本设计不内建

**能力边界（回答不了——工具极限，如实声明）**
- DC3 档 2（`[源项目·<path>]`）需访问 Cpp_Hub 外部仓库实体——校验器只校验**标注格式**，不跨仓解析目标文件存在性
- R7 计数的**自引用边界**（grep 命令本身包含标记字符，如 RESEARCH §0 已扣 1 处）——首版登记为 derived-requirement，用排除规则处理，不追求零自引用
- Step 8 双向引用 grep 检查（ADR-0008 D6）——与"链接可解析"相邻但语义不同，**不入 v1**，留作触发条件后的扩展检查（见 §10 风险）

## 3. 架构设计

### 3.1 整体架构

```
[git commit]
    │ 触发
    ▼
.pre-commit-config.yaml (repo: local, language: system)
    │ files: \.md$  →  传入 staged 文件名
    ▼
scripts/dc_validator.py  (CLI 入口, M1)
    ├─ M2 frontmatter  ──  YAML 解析 → DC1 七字段 → DC2 词表
    ├─ M4 counting     ──  R7 §0 计数 = grep 重数 (逐文件)
    ├─ M5 linkcheck    ──  DC3 档1 相对链接可解析 (逐文件)
    └─ M3 namespace    ──  DC4 id 全仓唯一 (全仓扫描, 非 staged-only)
```

校验器自身为仓库首个入库代码，但定位为**契约的机器可读定义**，非业务代码（RESEARCH §5.3）。

### 3.2 模块划分

| 模块 | 职责 | 输入 | 输出 | 依赖 |
|------|------|------|------|------|
| M1 CLI 入口 | 子命令解析 / 分发 / 聚合结果 / 退出码 | argv | `Summary` + exit code | M2-M5 |
| M2 frontmatter | YAML 解析 + DC1 七字段齐全 + DC2 type/status 词表取值 | 单文件路径 | `list[CheckResult]` | 无（stdlib PyYAML 待验证） |
| M3 namespace | DC4 `id` 全仓唯一 + 登记状态 | 全仓 `.md` 文件集 | `list[CheckResult]` | 无 |
| M4 counting | R7 §0 计数 = grep 机械重数 | 单文件路径 | `list[CheckResult]` | 无（stdlib `re`） |
| M5 linkcheck | DC3 档 1 相对链接可解析 | 单文件路径 | `list[CheckResult]` | 无 |

> **依赖验证（Step 6 前置提示）**：M2 的 YAML 解析库与 M4 的 grep 实现方式，属实施文档（Step 5-6）确认项。RESEARCH §2.1 已证 `language: system` 零隔离环境依赖；是否引入 PyYAML 第三方库 vs stdlib 手写 front-matter 解析，是 v1 的模块级决策，落 IMPLEMENTATION §2.1 验证。

### 3.3 数据流

1. pre-commit 依 `files: \.md$` 收集 staged `.md` → 作为文件名参数传入 `dc_validator.py`
2. M1 解析子命令，把**逐文件检查**（M2/M4/M5）应用到 staged 文件集
3. M3 不依赖 staged 列表，独立枚举全仓 `.md`（`git ls-files '*.md'` 或等价遍历）做 id 唯一性——因 DC4 唯一性是**全仓性质**，仅查 staged 会漏未暂存的既有文档
4. 各模块产 `CheckResult` → M1 聚合为 `Summary` → 映射退出码

### 3.4 控制流

```
main()
  parse_subcommand()                 # --check-all / --check-<x>
  results = []
  if check in {frontmatter, counting, links}:
      files = staged_files(argv)     # pre-commit 传入; 独立调用时默认全仓
      for f in files:
          results += dispatch(check, f)
  if check in {all, namespace}:
      results += namespace_check(all_md_files())
  summary = aggregate(results)
  exit(0 if summary.passed else (1 if any_violation else 2))
```

关键点：逐文件检查对**外部传入文件列表**处理（pre-commit 语义），命名空间检查**强制全仓**（不依赖外部传入），二者在 M1 显式分派，避免"staged-only 造成 DC4 假通过"。

> **退出码 2 触发路径（v1.1 复验补注，P3-2）**：伪码主体未展开异常路径——M1 顶层以 try/except 包裹各检查分发，未捕获异常映射退出码 2（§7 语义：工具自身错误 ≠ 校验通过）；"Python/依赖缺失"发生在 pre-commit 层（工具尚未运行），由 pre-commit 自行报环境错误，不属本工具退出码范畴。

## 4. 接口定义

### 4.1 CLI 入口（M1）

```python
# scripts/dc_validator.py
def main(argv: list[str] | None = None) -> int:
    """
    DC 契约校验器 CLI 入口。

    Returns:
        int: 退出码——0 全部通过 / 1 发现契约违规 / 2 工具自身错误
    """
```

子命令（`--check-*` 可组合，`--check-all` 默认）：

| 子命令 | 对应模块 | 检查 |
|--------|---------|------|
| `--check-frontmatter` | M2 | DC1 七字段 + DC2 词表 |
| `--check-namespace` | M3 | DC4 id 唯一 |
| `--check-counting` | M4 | R7 计数 = grep 重数 |
| `--check-links` | M5 | DC3 档 1 相对链接 |

### 4.2 `check_frontmatter`（M2）

```python
def check_frontmatter(file: str) -> list[CheckResult]:
    """
    校验单文件的 front-matter。

    Returns:
        至少一个 CheckResult；YAML 无法解析时返回 severity=P1 的
        CheckResult（标记 `yaml-unparsable`），而非抛异常。
    """
```

检查项：七字段逐一存在性 → `type` ∈ 六类词表 → `status` ∈ 该 type 对应状态词表（`design` 二档判定：id 后缀 `-CHECKLIST` → CHECKLIST 词表，PLAN v1.6 DC2）。

### 4.3 `check_namespace`（M3）

```python
def check_namespace(files: list[str]) -> list[CheckResult]:
    """
    校验 DC4 id 全仓唯一。输入为全仓 .md 文件集（非 staged-only）。

    Returns:
        每个重复 id 至少一条 P1 结果；无重复返回空列表。
    """
```

### 4.4 `check_counting`（M4）

```python
def check_counting(file: str) -> list[CheckResult]:
    """
    校验 R7 —— §0 断言统计表各计数必须等于该标记字符的机械枚举数。

    Returns:
        声明的计数与实际重数不一致时，每条计数差一条结果（附 declared/actual）。
    """
```

### 4.5 `check_links`（M5）

```python
def check_links(file: str) -> list[CheckResult]:
    """
    校验 DC3 档 1 —— 仓库内相对链接（markdown `](...)`）目标文件存在。

    Returns:
        每个不可解析的仓库内相对链接一条 CheckResult；档 2-4 标注仅做格式存在性
        检查，不跨仓解析。
    """
```

## 5. 替代方案

### 5.1 方案 A：pre-commit 本地 hook + 纯 Python 脚本（选择）

- 描述：`repo: local` + `language: system` + `scripts/dc_validator.py`（RESEARCH §2.1）
- 优点：git 层元工具，零运行时/零模型/零部署；本地 1 秒拦截；`files: \.md$` 精确作用域
- 缺点：脚本是仓库首个入库代码（与"纯文档"身份的张力，已由 §1/§2.3 界定）
- 选择理由：唯一满足"提交瞬间拦截 + 零基础设施 + 命中形态 II 前移"三目标的方案（RESEARCH §3.1 主判断）

### 5.2 方案 B：CI（GitHub Actions）承载校验器（否决）

- 描述：校验逻辑放 CI workflow，提交后异步跑
- 优点：环境统一、不依赖本地 PATH
- 缺点：**事后拦截**——修复成本 = amend/push/协调，正是 RESEARCH §2.2【A】OpenMMLab 先例论证要消除的形态
- 否决理由：与"把事后审计前移为提交瞬间拦截"的核心目标相反；且本仓库为单人本地仓，CI 基础设施属过度工程

### 5.3 方案 C：独立 hook 仓库 + pip 分发包（否决）

- 描述：把校验器发布为单独 pip 包 / 独立 hook 仓库再引用
- 优点：跨仓库复用
- 缺点：单人 + 文档仓库，发布/版本管理成本远超收益
- 否决理由：`repo: local` 已满足本仓需求，独立发包是面向"多仓库复用"的过度设计（RESEARCH §3.2.3 明确"通用 hooks 作为补充而非替代"，本校验器是特化工具）

### 5.4 方案 D：LLM-based 校验（prompt 检查）（否决）

- 描述：让 LLM 读文档并判断是否符合 DC 契约
- 优点：能捕捉语义级违规
- 缺点：**LLM 恰是形态 II 的生成端**，用生成端做拦截端违背 M7 规律③"拦截层 = E1 机械枚举而非 LLM 自查"
- 否决理由：与 R7 的机械枚举原则、与"异构于生成端"的不变式（I-5）直接冲突

## 6. 数据结构

### 6.1 `CheckResult`

```python
@dataclass(frozen=True)
class CheckResult:
    check_id: str      # "dc1" | "dc2" | "dc4" | "r7" | "dc3"
    file: str          # 相对路径
    severity: str      # "P1" | "P2" | "P3"（SPEC_PROCESS 分级 ladder）
    message: str       # 人类可读，含 declared/actual 等可核对信息
    line: int | None   # 尽可能定位到行，弱化"低语义载荷字段"的定位成本
```

### 6.2 `Summary`

```python
@dataclass
class Summary:
    results: list[CheckResult]
    @property
    def passed(self) -> bool: ...
    @property
    def violations(self) -> list[CheckResult]: ...   # severity 非空的结果
```

### 6.3 词表常量（单一真值源原则）

```python
# DC2 词表权威源 = PLAN §1 DC2 v1.6（type 主轴 + design 二档）+ ADR-0007 D4（含澄清追记）。
# 改词表必须先改权威文档，同 commit 改此常量。见不变式 I-4。
TYPE_VOCAB = {
    "adr":              {"proposed", "accepted", "superseded", "deferred"},
    "discovery":        {"open", "resolved", "toolized"},
    "process-spec":     {"active", "deprecated"},
    "framework":        {"active", "deprecated"},
    "template":         {"draft", "in-review", "verified"},
    "design":           {"draft", "in-review", "verified"},  # 一般设计文档（id 不以 -CHECKLIST 结尾）
}

# 副轴（v1.2，PLAN v1.6 DC2 消歧）：id 以 "-CHECKLIST" 结尾的 design 文档用 CHECKLIST 词表
# （E1 存量实证：cpp-hub-absorption-CHECKLIST=accepting、模板占位符=pending）
CHECKLIST_STATUS_VOCAB = {"pending", "accepting", "accepted"}
```

> **P2-1 已闭合（v1.2，2026-08-18）**: [PLAN v1.6 §1 DC2](../doc-contract/PLAN.md) 消歧落地——design 增两行（一般设计文档 / CHECKLIST 实例），判别规则 = id 后缀 `-CHECKLIST`（机械可 grep，M2 直接实现）；[ADR-0007 D4](../../adr/ADR-0007-unified-document-contract.md) 澄清追记在案；E1 全仓实证 14 份 design 文档零违规（含存量 [cpp-hub-absorption/CHECKLIST.md](../cpp-hub-absorption/CHECKLIST.md) 的 `accepting`，消歧后合法）。M2 可按本节常量实施，前置条件解除。

## 7. 错误处理

| 错误场景 | 处理方式 | 退出码 | 用户可见信息 |
|---------|---------|-------|------------|
| front-matter YAML 无法解析 | 返回 `yaml-unparsable` P1 结果，不抛异常 | 1 | `[P1] <file>: front-matter 非合法 YAML: <详情>` |
| 七字段缺失 / 词表取值非法 | 逐字段报 P1/P2 | 1 | 明确缺失字段名 / 非法值 vs 允许词表 |
| id 重复 | 报所有重复方（不只一方） | 1 | 每个重复 id 的双方文件路径 |
| §0 计数 ≠ grep 重数 | 报 declared vs actual | 1 | `[P1] §0 <级别> 声明 n 实为 m` |
| Python/依赖缺失（PATH） | 交由 pre-commit 报环境错误 | 2 | stderr 明确"工具无法运行"而非"校验通过" |
| 目标文件不存在（非 .md scope 内） | 跳过并可选 verbose 提示 | 0 | `[skip] <file> 不在 DC 契约范围` |

**退出码语义（关键不变式）**：`0`=通过；`1`=运行成功且发现违规；`2`=工具自身错误。`1` 与 `2` 都阻断提交（pre-commit 见非零即 fail），但区分二者确保**工具崩溃绝不静默放行**（不被误读为"无一违规"）。

## 8. 不变式（Invariants）

1. **I-1 只读**：校验器任何路径不得写文件、不改动工作树（与 RULE-5 单向权限 / ADD"审计者永不自动修复"同构）
2. **I-2 确定性**：同一仓库状态 + 同一检查 → 输出与退出码确定，无时间/环境/网络依赖（DC3 档 2-4 不联网解析，见 §2.3 能力边界）
3. **I-3 零新规则**：校验器不新增任何契约规则，只机器化执行 ADR-0007 / PLAN / FWK-ASSERTION R7 已定义的规则
4. **I-4 单一真值源**：词表/字段常量变更必须先在权威文档（ADR-0007 / PLAN）生效，同 commit 改 `dc_validator.py` 常量，禁止反向
5. **I-5 异构于生成端**：计数（R7）与唯一性（DC4）用独立 grep / 文件枚举，绝不依赖 LLM 判断（M7 规律③）

## 9. 幻觉排除审查（Step 4 Review）

### 9.1 设计基于已验证的调研结论

- [x] 所有设计决策可追溯到 RESEARCH.md（§2.1 映射表 6 行逐一引用）——复验核对通过（2026-08-18 独立 pass）
- [x] 无未经验证的假设（H1-H3 已随 RESEARCH 附录 C 显式携带，不转正）——复验补强：v1.0 遗留的词表双轴歧义（P2-1）已升格为显式实施前置条件（§6.3/§10.1）；v1.2 该前置条件已闭合（PLAN v1.6 DC2 消歧落地）
- [x] 无论证驱动的归因扭曲——五大检查未裁剪 DC3 档 2 的跨仓解析（已如实声明为能力边界）

### 9.2 替代方案审查

- [x] 三个替代方案（B/C/D）各有明确否决理由
- [x] 方案 D 否决与 M7 规律③、不变式 I-5 自洽

### 9.3 职责边界审查

- [x] 职责边界清晰（§2.3）：语义审查归 ADD、格式归 markdownlint、档 2 跨仓解析归能力外
- [x] 未越界吞并 Step 8 双向引用检查（ADR-0008 D6，已声明入 v1 范围外）

> **复验标注（2026-08-18）**: 本 §9 checkbox 由独立 pass（DeepSeek V4 Pro 同基座新上下文，RULE-1 时序独立）勾选——RULE-5 模型异质性未满足（生成端同基座），真异基座复验为可选项待 GLM 会话；若执行，以 GLM 复验结论为准覆盖本标注。

## 10. 对实施的输入

### 10.1 关键工程约束

1. Windows 无 bash：entry 一律 `python scripts/dc_validator.py`（RESEARCH §2.1 陷阱实证）
2. 只读 + 确定性（I-1 / I-2）
3. `files: \.md$` + 逐文件检查走 pre-commit staged 列表；namespace 检查强制全仓（§3.4）
4. 代码量 ~100 行（RESEARCH H2 规模，实施时核对）
5. YAML 解析依赖选型（stdlib vs PyYAML）在 IMPLEMENTATION §2.1 验证真实存在与版本
6. ~~词表双轴歧义先行裁决（P2-1）~~ ✅ 已闭合（v1.2，2026-08-18）：PLAN v1.6 §1 DC2 消歧落地——M2 判定规则 = id 后缀 `-CHECKLIST` 二档选词表（见 §6.3）

### 10.2 风险与缓解

| 风险 | 缓解 |
|------|------|
| 校验器自身含计数/分类错误（形态 II 于"反幻觉工具"本身复发） | 计数/唯一性用独立 grep 实现；测试用固定 fixture 覆盖；校验器自身受 R7 纪律约束（RESEARCH §5.3） |
| 脚本与"纯文档"身份张力 | §1/§2.3 界定为"契约的机器可读定义"；代码最小化 |
| 非契约范围 .md 误报（如 README / CODE_WIKI 轻契约） | scope 过滤 + allowlist，作为 derived-requirement 在 Step 8 登记 |
| R7 计数自引用边界（grep 命令自身的标记字符） | 排除规则，首版登记 derived-requirement（§2.3 能力边界） |
| Step 8 双向引用检查（ADR-0008 D6）一度被认为属本 feature | 已声明 v1 范围外，触发条件后扩展，防范围蔓延 |

---

**Review 签字**: DeepSeek V4 Pro（同基座新上下文独立 pass）日期: 2026-08-18 —— P2-1（升格实施前置条件）+ P3-2（退出码 2 补注）已修正（v1.1）；RULE-5 真异基座复验为可选项待 GLM 会话