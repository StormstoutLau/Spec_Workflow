---
id: precommit-dc-validator-RESEARCH
type: design
version: 1.1
status: draft
date: 2026-08-18
depends: [SPEC-PROCESS, FWK-ASSERTION, ADR-0007, langgraph-upgrade-RESEARCH]
upstream: null
---

# pre-commit + DC 契约校验器调研报告 v1.1 (2026-08-18)

> **任务来源**: [LANGGRAPH_UPGRADE_RESEARCH.md](../langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md) §8.3 裁决"最高 ROI = pre-commit + DC 契约校验器"，本调研为其实施前的 Step 1-2
> **方法**: 本框架 §3/§7 自举——A/B/C 断言分级 + 机读登记 + 假设区隔离
> **审查状态**: v1.1 经复验（2026-08-18，DeepSeek V4 Pro，**同基座新上下文**——RULE-1 时序独立满足、RULE-5 模型异质性未满足，真异基座需另开 GLM 会话）：A 类 7 条全闭合（5 条本轮页面级逐字命中 + 2 条 P-006 转引）；B=2/C=1/H=3 机械重数全符；M7"11 处"属实。修正 §0 计数说明失实（P3-1，形态 II 复发 1 处，M7 样本⑦）

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 7 | 每条附 URL + 可核对引文（WebSearch 取证，2026-08-18；含 3 条自 LANGGRAPH §8.1 已验证先例的转引） |
| B 推断类 | 2 | B1-B2，登记于附录 B |
| C 判断类 | 1 | §3.1 主判断（转引 LANGGRAPH §8.3 裁决，不重复论证） |
| 假设区 | 3 | H1-H3，未取证声明 |

> **计数说明（R7，v1.1 复验修正）**: 各计数由机械枚举生成（`grep -n` 逐行核对，E1 可重放）。A 类标记机械计数 10 = 实质断言 7 + 非断言性出现 3（§5.2 转引 1 处 + 附录 B claimed_chain 内 2 处），非断言出现均已扣除（本说明行刻意不写标记字面，防说明自身进入计数）。v1.0 原说明"脚注命令行 1 处自引用"系措辞误植（本文件无脚注命令行，为 LANGGRAPH v1.1 修正场景的复制残留），扣减对象与数量均失实——形态 II 计数桶复发，入 M7 样本⑦（2026-08-18 同基座复验发现并修正；修正稿初版曾在说明内引入 3 处标记字面致机械数短暂为 13，闭环重数后去除——R7 自引用边界处置先例）。

---

## 1. 调研问题

1. pre-commit 框架能否承载 DC1-DC4 契约的机械校验？关键能力（本地 hook / 文件模式匹配 / Windows 环境）是否成立？
2. 形态 II 计数错误能否通过 pre-commit 前移到"提交瞬间"拦截，而非"事后审计"发现？
3. 校验器与仓库"纯文档方法论"身份是否冲突？成本边界与 Windows 陷阱是什么？

## 2. 调研发现

### 2.1 pre-commit 框架能力（承载性验证）

【A】pre-commit 是跨语言的 pre-commit hook 包管理器，pip 安装、`.pre-commit-config.yaml` 声明式配置、`pre-commit install` 写入 `.git/hooks/pre-commit`：
(源: https://pre-commit.com/?ref=sfeir.dev; 引文: "It is a multi-language package manager for pre-commit hooks. You specify a list of hooks you want and pre-commit manages the installation and execution of any hook written in any language before every commit.")

【A】仓库本地 hook 通过 `repo: local` 哨兵值声明，本地 hook 可用任何受支持的语言（不要求单独的 hook 仓库）：
(源: https://github.com/pre-commit/pre-commit.com/blob/main/sections/advanced.md; 引文: "You can configure repository-local hooks by specifying the repo as the sentinel local. local hooks can use any language which supports the...")

【A】`files:` 正则限定 hook 作用文件 + `language: system` 直接执行本地脚本（不建隔离环境、零额外依赖）是本地 hook 的标准配置形态：
(源: https://www.fixdevs.com/blog/pre-commit-not-working/; 引文: "entry: python scripts/validate.py" / "language: system" / "files: ^src/.*\.py$")

【A】Windows 陷阱：`language: system` / `language: script` 的 entry 若写成 shell 命令或 bash 脚本，在 Windows 会因缺少 `/bin/sh`/bash 而失败（`/bin/sh not found` 或 `exit 127`）：
(源: https://silon.vip/post/102; 引文: "ExecutableNotFoundError: Executable /bin/sh not found" / 源: https://github.com/lycheeverse/lychee/issues/2238; 引文: "exit code: 127" / "/bin/bash: C:Users...scriptslychee_pre_commit.sh: No such file or directory")

【A】当前 pre-commit 版本线为 4.6.x（官方文档即时快照）：
(源: https://pre-commit.com/?ref=sfeir.dev; 引文: "pre-commit 4.6.2")

### 2.2 社区先例（front-matter 校验 + 链接检查三件套）

【A】2026 年三个独立先例证实"front-matter 校验 + markdownlint + 链接检查"是文档仓库的成熟 pre-commit 做法，且"现有验证器全部漏过 YAML 解析错误"有实证（已在本仓 LANGGRAPH §8.1 验证，2026-08-18 WebSearch 取证，此处转引 URL+引文）：
(源: https://github.com/webbertakken/takken.io/pull/239; 引文: "The colon after `work` made YAML treat the next line as a mapping key. Prettier formats this without complaint, so nothing caught it until the build blew up" / 源: https://github.com/ievo-ai/skills/issues/119; 引文: "This bug survived all existing validators and code review because none of them parse YAML frontmatter" / 源: https://github.com/paullukic/coograph/issues/6; 引文: "every `SKILL.md` ... must have YAML frontmatter with `name` ... and `description`" / "Link checker — `lychee` over all `*.md` files. Validates relative paths exist")

【A】OpenMMLab 官方维护 pre-commit-hooks 仓库作为"把事后审计前移为提交瞬间拦截"的工程先例（LANGGRAPH §8.3 引用）：
(源: https://github.com/open-mmlab/pre-commit-hooks; 引文: 见 LANGGRAPH §8.3 转引——"修复成本在本地 1 秒 vs CI 失败后的 amend/push/协调")

### 2.3 DC 契约校验点映射（从既有裁决派生，零新发明）

**B1**（见附录 B）：DC1-DC4 契约的五大机械可检查点可全部映射为 pre-commit 本地 hook 检查，无需任何新规则——检查项直接从 ADR-0007 与框架 v1.4 R7 派生。

**B2**（见附录 B）："statistics 表计数 = 机械重数"检查（R7 规则）可用 pre-commit 前移到提交瞬间，对形态 II（M7 已登记 11 处复发）构成提交级拦截而非事后审计发现。

## 3. 综合分析

### 3.1 主判断（C 类）

【C】**本调研确认 LANGGRAPH §8.3 的最高 ROI 裁决，不重复论证**：pre-commit 是 git 层元工具，不引入运行时、不绑定模型、不需要部署；五种能力（本地 hook / files 正则 / YAML 解析 / 计数检查 / 链接检查）经 §2 逐条验证成立，唯一工程约束是 Windows 下 entry 必须走 `python scripts/dc_validator.py` 而非 shell。校验器把 DC 契约从"文档纪律"变成"提交瞬间机器拦截"，直接命中 M7 账本实证的最高频失效模式（形态 II，11 处）。

### 3.2 关键发现总结

1. pre-commit 的 `repo: local` + `language: system` 机制完全覆盖本 feature 的承载需求，无需单独建 hook 仓库、无需隔离环境、无需运行时部署 [置信度: ★★★★★]
2. 形态 II 计数检查可机械化为独立 grep 重数，异构于生成端 LLM，是"拦截层 = E1 机械枚举而非 LLM 自查"（M7 规律③）的直接实现 [置信度: ★★★★★]
3. Windows 环境需规避 `language: system` + shell entry 的 `/bin/sh` 依赖，改走 `python` entry——这是唯一有实证的工程陷阱 [置信度: ★★★★☆]
4. 社区"front-matter + 链接检查"三件套是 2026 成熟做法，本 feature 的 DC 契约校验是其在"带编号空间/词表约束的文档契约"上的特化 [置信度: ★★★★☆]

### 3.3 技术 landscape 与空白

现有 landscape：markdownlint（格式）、lychee（链接）、prettier（排版）等通用 hook 覆盖"形式"，但不理解本仓的 DC1-DC4 语义（七字段、type/status 词表、id 唯一性、计数 = grep 重数）。空白：**把 DC 契约本身做成机器可读校验**——这正是本 feature 的位置，通用 hooks 作为补充而非替代。

## 4. 幻觉排除审查（Step 2 Review）

### 4.1 技术声明验证

| 声明 | 来源 | 验证方式 | 状态 |
|------|------|---------|------|
| pre-commit 本地 hook（repo: local / language: system） | pre-commit.com advanced.md + fixdevs | WebSearch 页面级引文 | ✅ |
| files 正则限定作用文件 | fixdevs | WebSearch 页面级引文 | ✅ |
| Windows /bin/sh/bash 依赖陷阱 | silon.vip + lychee issue#2238 | WebSearch 页面级引文 | ✅ |
| 三先例 + OpenMMLab | LANGGRAPH §8.1/§8.3 | 转引已验证（2026-08-18） | ✅ |

### 4.2 待修正项

- [x] 本报告 v1.0 为 `自查（单视角）`（RULE-4）——独立 pass 已完成（2026-08-18，DeepSeek V4 Pro 同基座新上下文，见头部审查状态）：P3-1 §0 计数说明失实已修正（v1.1）；A 类断言 7 条页面级/转引全闭合；B1/B2 probe 引用文件存在性核实通过。RULE-5 真异基座复验仍待 GLM 会话（可选追加）

## 5. 对设计的输入

### 5.1 可用的技术方案

- 校验器落点：`scripts/dc_validator.py` + `.pre-commit-config.yaml`（`repo: local`，`language: system`，`entry: python scripts/dc_validator.py`，`files: \.md$`）
- 五大检查：YAML 可解析 / DC1 七字段齐全 + DC2 词表取值 / DC4 id 全仓唯一 / R7 计数 = grep 重数 / DC3 相对链接可解析

### 5.2 关键约束

1. **Windows 无 bash 依赖**：entry 一律 `python` 前缀，不用 shell 命令 / bash 脚本（§2.1【A】陷阱实证）
2. **只读校验**：校验器永不自动改写文档（与 RULE-5 单向权限、ADD"审计者永不自动修复"同构）
3. **单一真值源**：校验规则 = DC 契约机器可读定义，改规则须先改 ADR-0007/PLAN 契约本体

### 5.3 风险

| 风险 | 缓解 |
|------|------|
| 校验器自身含计数/分类错误（形态 II 于"反幻觉工具"本身复发） | 校验器的计数检查用独立 grep 命令实现，其测试用固定 fixture 覆盖；校验器自身同样被 R7 纪律约束 |
| 脚本是仓库首个入库代码，与"纯文档"身份张力 | 明确脚本为"契约的机器可读定义"而非业务代码，代码量最小化（~100 行） |
| Windows 用户未装 `python`（PATH 缺失） | `language: system` 依赖 PATH；作为单人仓库 + 三机均装 Python 为前提，登记 H3 |

---

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "DC1-DC4 契约的五大机械可检查点（YAML 可解析 / 七字段齐全+词表取值 / id 唯一 / 计数=grep重数 / 相对链接可解析）可全部映射为 pre-commit 本地 hook 检查，无需任何新规则",
    "op": "equivalence",
    "claimed_chain": [
      {"step": 1, "text": "DC1 定义七字段 front-matter（id/type/version/status/date/depends/upstream）", "source": "PLAN §1 DC1"},
      {"step": 2, "text": "DC2 定义各 type 状态词表、DC4 定义 id 命名空间登记", "source": "PLAN §1 + ADR-0007 D4/D5"},
      {"step": 3, "text": "R7 要求统计表计数由机械枚举生成", "source": "FWK-ASSERTION v1.4 §7 R7"},
      {"step": 4, "text": "pre-commit 本地 hook 可对 .md 文件执行任意本地脚本检查", "source": "本报告 §2.1【A】"}
    ],
    "sources": [
      {"label": "pre-commit local hooks", "path": null, "url": "https://github.com/pre-commit/pre-commit.com/blob/main/sections/advanced.md", "quote": "You can configure repository-local hooks by specifying the repo as the sentinel local"}
    ],
    "probe": {"type": "existence", "files": ["adr/ADR-0007-unified-document-contract.md", "spec/doc-contract/PLAN.md", "docs/ASSERTION_EVIDENCE_FRAMEWORK.md"], "params": {"symbols": ["DC1", "DC2", "DC4", "R7"], "claim": "present"}}
  },
  {
    "id": "B2",
    "conclusion": "\"统计表计数 = 机械重数\"检查可用 pre-commit 前移到提交瞬间，对 M7 已登记的形态 II 复发（11 处）构成提交级拦截而非事后审计",
    "op": "causal",
    "claimed_chain": [
      {"step": 1, "text": "形态 II 复发 11 处，规律③ 定拦截层是 E1 机械枚举而非 LLM 自查", "source": "M7_EVIDENCE_LOG §2"},
      {"step": 2, "text": "R7 定义统计表计数 = grep 机械重数（独立于生成端 LLM）", "source": "FWK-ASSERTION v1.4 §7 R7"},
      {"step": 3, "text": "pre-commit 在 git commit 前置触发任意本地脚本，故可把 grep 重数校验绑定到提交动作", "source": "本报告 §2.1【A】"}
    ],
    "sources": [
      {"label": "M7 账本", "path": "docs/M7_EVIDENCE_LOG.md", "url": null, "quote": "拦截层是 E1 机械枚举，非 LLM 自查"},
      {"label": "pre-commit 文档", "path": null, "url": "https://pre-commit.com/", "quote": "before every commit"}
    ],
    "probe": {"type": "counting", "files": ["docs/M7_EVIDENCE_LOG.md"], "params": {"pattern": "形态 II|11", "expected": "分桶合计 11"}}
  }
]
```

## 附录 C: 假设区

- [H1] 全仓 21 个带 front-matter 的文档其七字段均已齐全（P-003 完成定义声明 `id:` 21 文件命中，但未逐文件核对七字段完整性）— 查证路径: 校验器首跑 `--check-frontmatter` 全量扫
- [H2] 校验器首版 ~100 行 Python 的规模估算准确（未写骨架实测）— 查证路径: 设计文档 §3 模块划分落地时核对
- [H3] 主控站 Windows 环境 `python` 在 PATH 中、且 `pre-commit` 可 pip 安装（`language: system` 依赖）— 查证路径: `pip install pre-commit && pre-commit --version` 实测

---

**Review 签字**: DeepSeek V4 Pro（同基座新上下文独立 pass）日期: 2026-08-18 —— P3-1 已修正（v1.1），核心结论（B1/B2/§3.1 主判断）成立；RULE-5 真异基座复验为可选项待 GLM 会话