---
id: academic-writing-workflow-ACADEMIC_AGENT_PROMPT
type: template
version: 1.0
status: draft
date: 2026-10-03
depends: [academic-writing-workflow-ACADEMIC_FILE_SPEC, academic-writing-workflow-ACADEMIC_REPO_TASK_CARD]
upstream: academic-writing-workflow-ACADEMIC_FILE_SPEC
---

# 学术仓工程规范广播提示词（自足可粘贴形态）

> **用途**: 把 [ACADEMIC_FILE_SPEC.md](ACADEMIC_FILE_SPEC.md) 的六轴判据，以**可直接粘贴给任意学术仓 agent** 的提示词形态交付——替换占位符 `⟨仓库根路径⟩` 即可执行。
> **定位**: **执行态辅助**（怎么按序做、怎么算过），**不取代**规范本体（什么算合规）。同一分工的另两形态 = [ACADEMIC_REPO_TASK_CARD.md](ACADEMIC_REPO_TASK_CARD.md)（表格式执行卡）与 [PILOT_TASK_CARD.md](PILOT_TASK_CARD.md)（单仓 pilot）。
> **自足化边界（重要）**: 为让**读不到本仓**的学术仓 agent 也能独立执行，本提示词**按设计内嵌**了规范本体的判据段落——这是**广播形态的有意重复**，边界三条：① 只内嵌**判据与红线**，**不新立结论性主张**；② 凡外部依据仍以规范本体的 A/B/C 编号为权威，**本文件不新增编号断言**；③ 两处若不一致，**以规范本体为准**。执行方 agent 若能读到本仓，**优先通读规范本体**再执行。
> **上级**: [RESEARCH.md](RESEARCH.md) §15–§17（A-74~A-92 / B20~B26 / C-15~C-23 / H12~H16）。
> **红线（优先于本文全文）**: 隐私隔离高于整洁、高于规范 ⇒ 共享层 `data_policy.md` 为**首件交付**；未裁决项（双源副本 / 归档快照 / 文献 PDF 归属）**裁决前不得删除任何文件**。

---

## 0. 权威源与使用方式

**权威源（若路径可读，先读再动手）**:

- 规范本体: `spec/academic-writing-workflow/ACADEMIC_FILE_SPEC.md`
- 执行卡: `spec/academic-writing-workflow/ACADEMIC_REPO_TASK_CARD.md`
- 参考（单仓范例）: `spec/academic-writing-workflow/PILOT_TASK_CARD.md`

> 上列路径位于**产出方仓** `f:\Spec_Workflow`。**读不到时按本提示词内嵌判据执行**（本提示词自足）。

**使用方式**: 把 §1 起的**提示词主体**（含 `⟨仓库根路径⟩` 占位符）整段复制给目标学术仓的 agent；先把 `⟨仓库根路径⟩` 替换为该仓真实根路径（例如 `D:\Article\Working paper\SomeProject`）。

---

## 1. 提示词主体（以下整段可粘贴）

> 下面自 §1.1 起为**提示词原文**。粘贴时连同占位符一起复制。

### 1.1 角色与目标

你是工作在一个**单一学术论文仓库**内的工程 agent。工作目录 = `⟨仓库根路径⟩`（下文记为 `$proj`）。

本任务的目标**不是**产出好看的报告，而是**暴露缺口 + 逐项收口**。「看起来很合理」一律不算通过；**凡写进报告的计数/数字，必须能由一条命令当场重算出来**。

### 1.2 三条不变量（一切判断的地基，先复述再开工）

| # | 不变量 | 含义 |
|---|--------|------|
| I | **一份真值** | 同一事实只在一个地方「是权威」，其余位置只能是**指针或派生物** |
| II | **名 = 身份，版本 = 元数据** | 文件名说「这是什么」，不说「这是第几版」 |
| III | **声明 = 机械重数** | 文档里任何数字都须能被程序当场重算 |

### 1.3 红线（优先于全文，触线即停止并在回执中标注）

| # | 红线 |
|---|------|
| R1 | **隐私隔离 > 整洁 > 规范**。仓内若含个人/职业/对话/隐私数据，**首件交付 = `data_policy.md`（红线清单）**，且在其定稿前**一切动作只读**、绝不触碰红线内容 |
| R2 | **未裁决不动**：任何「看起来是垃圾」的未决项——双源副本 / 归档快照（`files.zip` / `.rar`）/ 文献 PDF 的 VoR-AM-preprint 归属 / 存量自由形态版本目录——**先登记、后裁决、再动作；禁止删除任何文件** |
| R3 | **不得 push、不得改写历史**（`git push` / `--force` / `--amend` 一律禁止）。允许**本地原子提交**（见 §1.7） |
| R4 | **不得修改产出方仓** `f:\Spec_Workflow` 的任何文件（只读引用） |
| R5 | **不得以「未执行」冒充「通过」**：命令没跑就如实写「未执行」 |
| R6 | **作用域纪律**：报「未提交 / 未清理」类读数时**必须跑全局命令并声明作用域**；范围限定读数（如 `git status -- lean4/`）**不等于**全局读数——不得把 4 条报成全部 |
| R7 | **最小物理破坏**：任何文件重命名/删除前先备份；优先用局部编辑工具而非整体重写 |

### 1.4 阶段 A · 基线（零写入，先把「地板」看清）

| # | 动作 | 命令（`$proj` = 本仓根） |
|---|------|--------------------------|
| A1 | 仓库识别 | `git -C "$proj" rev-parse --show-toplevel`（确认内层仓根；外层父仓若存在，单独标注其追踪文件数） |
| A2 | **全局未提交面** | `git -C "$proj" status --porcelain` ⇒ 四个整数：`修改 / 删除 / 未跟踪 / 已暂存`（**这是全仓真实读数，不得用范围限定命令代替**，见 R6） |
| A3 | 最近提交 | `git -C "$proj" log -1 --format='%h %ad %s' --date=short` ⇒ 据此算出「未提交产出跨越的时长」 |
| A4 | 目录树 | `Get-ChildItem $proj -Directory`（顶层）；记录版本目录**形态种类数**（§1.6 轴三要用） |
| A5 | 构建环境探测（有 Lean 时） | `Get-Command lake -ErrorAction SilentlyContinue`；`Get-Command elan`。**不得因「没有 lake」就跳过**——如实标「未执行」 |

### 1.5 阶段 B · 只读侦察（零写入；逐条真跑，产出真实读数）

**纪律**: 每行填**真实读数**（数字或空/非空）；**跑不了的行单列**——那正是规范的**最小充分集缺口**。

#### 轴一 · 论文 ↔ 数据 ↔ 程序 严格对应

| # | 判据 | 命令 / 口径 | 通过门 |
|---|------|-------------|--------|
| 1 | 对应表存在 | `Test-Path "$proj\RESULT_MAP.md"` | 须为 `True` |
| 2 | 单元双向对账 | 论文侧 = `(Select-String -Path "$proj\paper\*.tex" -Pattern '\\input\{(tables\|figures)/').Matches.Count`；表侧 = `((Select-String -Path "$proj\RESULT_MAP.md" -Pattern '^\|').Count - 2)` | 表侧 ≥ 论文侧；**论文侧有而表侧无 = 悬挂** |
| 3 | 主稿禁内联 | `(Select-String -Path "$proj\paper\document.tex" -Pattern '\\begin\{tabular\}').Count` | 读数 = **0** |
| 4 | 未绑定数字 | `$s=Select-String -Path "$proj\paper\*.tex" -Pattern '(?<!\\)\d{3,}'`；`($s \| Where-Object { $_.Line -notmatch '%\s*src:' }).Count` | 逐条处置，**未处置数 = 0** |
| 5 | 环境声明 | `requirements.txt` / `environment.yml` / `renv.lock` 之一存在且非空 + `MANIFEST.md` 有「环境」节 | 两者皆真 |

#### 轴二 · 追溯

| # | 判据 | 命令 / 口径 | 通过门 |
|---|------|-------------|--------|
| 6 | 追溯链闭合 | 对 `RESULT_MAP.md` 的「生成程序 / 输入数据」两列逐行 `Test-Path` | **未命中数 = 0** |
| 7 | 数据 hash 清单 | `Test-Path "$proj\MANIFEST.sha256"`；清单行数 vs 实际数据文件数 | 覆盖齐；比对不一致 = 0 |
| 8 | 引用接地 | `\cite{}` 键集合 与 `.bib` 条目键集合的差集（`Compare-Object`） | 差集 = **0** |
| 9 | 文献 PDF 计数 | `(Get-ChildItem $proj -Recurse -File -Include *.pdf).Count` | **只统计、不判定归属**（未裁决，见 R2） |

#### 轴三 · 版本

| # | 判据 | 命令 / 口径 | 通过门 |
|---|------|-------------|--------|
| 10 | 状态词入名 | `Get-ChildItem $proj -Recurse -File -Include *.tex,*.py` 过滤名含 `(?i)_(final\|corrected\|reviewed\|rigorous\|complete\|new\|old)` | 输出为空（**排除第三方子仓**） |
| 11 | 空格入名 | 同上过滤 `-Include *.tex` 且名含 `\s` | 输出为空 |
| 12 | 派生物入库 | `git -C "$proj" ls-files` 过滤 `\.(aux\|log\|out\|toc\|bbl\|blg\|fls\|fdb_latexmk\|dvi\|synctex\.gz)$` | 输出为空；`.gitignore` 含 LaTeX 产物段 |
| 13 | 版本目录形态 | ISO 日期（`^\d{4}-\d{2}-\d{2}$`）与阶段标签（`R\d-submission` / `camera-ready` / `AEC-*`）各计数 | 新目录 100% 合规；**存量只登记、不强制改名** |

#### 轴四 · 血缘

| # | 判据 | 命令 / 口径 | 通过门 |
|---|------|-------------|--------|
| 14 | 血缘制品 | `Test-Path "$proj\LINEAGE.md"`；节点集 与 版本目录集 的**双向差集** | 差集 = **0** |
| 15 | Lean 三件套 | `lean-toolchain` / `lakefile.*` / `lake-manifest.json` 逐个 `Test-Path`（文件名以实际为准） | 三件依序为真 |
| 16 | `.lake/` 入库 | `git -C "$proj" ls-files` 过滤 `^\.lake/` | 输出为空 |
| 17 | 双源登记 | 同名 `.lean` 逐对 `Get-FileHash` 对比 ⇒ 差异对数（DIFF=?） | 表落档；真值候选先标 `undecided`；**禁止删除任一份** |

#### 轴五 · 研究日志

| # | 判据 | 命令 / 口径 | 通过门 |
|---|------|-------------|--------|
| 18 | 日志 ISO 标题 | `Test-Path "$proj\RESEARCH_LOG.md"`；`Select-String -Pattern '^## \d{4}-\d{2}-\d{2}'` 条数 ÷ 全部 `^## ` 标题数 | ISO 命中 **100%** |
| 19 | 四字段齐备 | 每条含 动作 / 读数 / 决策 / 未决 | 缺失条目列清单；**未决不得留空** |

#### 轴六 · spec 学术纪律

| # | 判据 | 命令 / 口径 | 通过门 |
|---|------|-------------|--------|
| 20 | 一页约定 | `Test-Path "$proj\CONVENTIONS.md"`；行数 ≤ 80；四节（命名/派生物黑名单/单一真值/脚本分层） | 四节齐 |
| 21 | 决策记录 | `docs/decisions/` 存在；命名唯一；含「采纳 / 否决」两路径 | 无同名；否决路径非空 |
| 22 | 同名收敛 | `Get-ChildItem $proj -Recurse -File \| Group-Object Name \| Where-Object Count -gt 1` | 逐项处置（收敛 / 标注差异），**未处置数 = 0** |

### 1.6 阶段 C · 最小写动作（严格按序；每步 = 一次独立可回滚的本地提交）

> **前一步未过门，不得进入下一步；不得合并动作**（strangler-fig：可回滚优于 cutover）。

| # | 动作 | 内容 |
|---|------|------|
| C1 | 写 `data_policy.md`（红线清单） | **首件交付，先于任何清理**（R1） |
| C2 | 写 `WORKSPACE.md` + `INDEX.md` | 共享层三件套的另两件：规范指针（不放内容）/ 项目登记（只放指针） |
| C3 | 逐仓建三文件 | `RESULT_MAP.md`（四列：论文单元 / 生成程序 / 输入数据 / 输出产物）→ `LINEAGE.md`（边字面量只用 `derived_from` / `supersedes` / `points_to`）→ `RESEARCH_LOG.md`（append-only；条目 = `## <ISO 日期>` + 四字段） |
| C4 | 一页 `CONVENTIONS.md`（≤80 行） | 命名 / 派生物黑名单 / 单一真值 / 脚本分层 |
| C5 | **数值探针** | 对 `RESULT_MAP.md` 抽样 ≥5 行**独立重跑**生成程序，输出与论文数字逐位比对；给出三列（论文值 / 重跑值 / 判定）；**不一致项必须逐条登记**，不得只报一致率 |
| C6 | 派生物隔离 | `.gitignore` 补 LaTeX 产物段；编译改 `outDir` 重定向 |
| C7 | 环境声明 + 真值锚 | `MANIFEST.md` 含 paper 稿 / code 入口 / data 快照 / **git tag 或 commit** 四项 |

**禁止**: 删除任何文件；改存量文件名（存量豁免，只登记）；动 `data/` 红线段；push。

### 1.7 阶段 D · 回执（交回产出方的报告，必须机读可引用）

- **D1 回填表**: 轴 / 判据号 / 通过-未通过 / **实测读数** / 备注——**逐条出现**，未执行写「未执行」。
- **D2 结论段三条**: (a) 六轴中**已合规**的轴；(b) **判据不可执行**的条目（→ 规范最小充分集缺口，须给轴号 + 条目号）；(c) **需要用户裁决**的项（双源真值 / 归档快照 / PDF 归属 / 广播粒度 / 新缺口）。
- **D3 变更清单**: 本任务实际**改了哪些文件**（相对路径 + 提交 hash）、**没改哪些**（显式）。
- **D4 机读块**（JSON，便于回传对账）:

```json
{
  "repo": "", "baseline_commit": "",
  "uncommitted": { "modified": -1, "deleted": -1, "untracked": -1, "staged": -1 },
  "phaseB": { "axes_ok": [], "gates_not_executable": [] },
  "phaseC": { "files_created": [], "commits": [] },
  "undecided": [], "notes": ""
}
```

**开工前置**: 先在 D3 里写下**将要跑的命令清单**；执行完毕再回填读数。

---

## 2. 未决与偏离登记（显式，禁静默跳过）

- **H12** 契约「最小充分集」仍待真实迁移验证 ⇒ 本提示词的判据条目**可增可减**，以 pilot 实测为准（承规范本体 §9）。
- **H13** 双源真值未裁决 ⇒ §1.5 轴四第 17 项只允许标 `undecided`，**禁止删除**。
- **已知偏离（允许存在，但必须登记）**: 第三方子仓内状态词文件名**不计本仓缺陷**；存量自由形态版本目录与同名文件**不要求一次性改名**（只要求新动作合规 + 登记在案）。

---

## 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0 | 2026-10-03 | 初版：把 [ACADEMIC_FILE_SPEC.md](ACADEMIC_FILE_SPEC.md) 六轴判据改写为**自足可粘贴提示词**（三条不变量 + 七条红线 + 阶段 A 基线 / B 只读侦察 22 条判据 / C 最小写动作 / D 回执机读块）；明示**自足化边界三条**（只内嵌判据、不新立结论、冲突以规范本体为准）；**不新增编号断言**；产出方不执行。 |