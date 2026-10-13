---
id: project-console-OBSIDIAN_READONLY_LAYER
type: template
version: 1.0
status: draft
date: 2026-10-14
depends: [project-console-RESEARCH]
upstream: null
---

# 非权威 Obsidian 只读探索层指引（C-39 落地）

> **用途**: 落地 [C-39](RESEARCH.md)（[RESEARCH §7.30](RESEARCH.md) 判定 B-27 + C-39）的**非权威只读探索层**——把 `spec/*/*.md` 的 **front-matter** 映射为一个**只读**、**不入 git**、**不接门禁**的 Obsidian 视图，供人工**探索 / 浏览** feature 元数据。**不取代** [docs/CONSOLE.md](../../docs/CONSOLE.md)。
> **定位**: **外部运行时辅助层**（Layer-2）。console 回答「项目整体状态是什么」（权威、纯派生、双侧门禁）；本层回答「有哪些 feature、各自元数据如何」（**非权威、只读、不入 git**）。两者**不互换权威**。
> **上级**: [RESEARCH.md](RESEARCH.md) **§7.33**（C-39 落地记录）+ **§7.30**（判定）。
> **边界（优先于本文全文）**: ① **非权威 · 不入 git · 不接门禁**；② **只读 · 不回写**；③ **console 保持权威**。

---

## 0. 三条边界（红线）

| # | 边界 | 含义 | 违约后果 |
|---|------|------|---------|
| ① | **非权威 · 不入 git · 不接门禁** | 本层**不参与**「声明 = 机械重数」，**不取代** `docs/CONSOLE.md`，视图产物**不进本仓版本控制** | 造第二个「看起来权威」的状态面 |
| ② | **只读 · 不回写** | **不写**任何 front-matter / 表 / 派生视图（Obsidian 侧须关闭一切回写与自动提交） | 撞 **I-1**（一份真值）——同事实两处为权威 |
| ③ | **console 保持权威** | `docs/CONSOLE.md` + pre-commit `console-gen` + CI `console_gen --check` 双侧门禁**不变** | 撞 **I-7**（视图不重贴标签）/ **I-10**（语义同源） |

> **本层的唯一正当用途 = 人工探索**（浏览 / 筛选 / 分组 feature 元数据）。**任何**「以它代替 console」「以它为状态真值」「由它驱动回写」的用法**均越界**。

## 1. 数据基座（E1，本仓实测 2026-10-14）

| 项 | 值 | 说明 |
|---|---|---|
| 载体 | `spec/*/*.md` 的 **YAML front-matter** | 非正文解析（避开大 vault 性能代价） |
| 字段（**DC1 七字段**） | `id` / `type` / `version` / `status` / `date` / `depends` / `upstream` | 全仓契约统一，逐件齐备 |
| 覆盖面（E1，2026-10-14 实测） | `spec/*/*.md` 共 **108 件**；带 front-matter 者 **30 件** | 其余 **78 件**无 front-matter ⇒ **不在**本探索面内（诚实声明，非缺陷） |
| `type` 现值（E1） | `design` **25** / `template` **4** / `framework` **1** | 词表六类，当前三值在用 |
| `status` 现值（E1） | `in-review` **12** / `draft` **9** / `verified` **6** / `accepting` **2** / `active` **1** | 词表**随 `type` 分档**（`design` 一般档 + CHECKLIST 副轴 + `framework` 档） |

> **口径**: 上述读数为 `spec/` 目录逐文件 front-matter 解析计数（本仓机械重数），**非目估**。

## 2. 可达面 / 不可达面（对照）

console 八项功能中，**仅「feature 元数据」一项**落在本层可达面内（承 [RESEARCH §7.30](RESEARCH.md) 判定表）：

| console 功能 | 数据来源 | 本层可达？ |
|---|---|---|
| **feature 元数据**（version / status / depends） | `spec/*/*.md` **front-matter** | **✅ 可达** |
| P 卡片 / 三级行动队列 | `PROGRESS.md` 表 + session 存在性 | ❌ |
| 决策链状态机（Mermaid） | session JSONL | ❌ |
| 派生状态机（执行态派生） | session + front-matter | ❌ |
| 步骤级动态描述表 | session JSONL | ❌ |
| hook 链 | `.pre-commit-config.yaml` | ❌（除非转写） |
| fork / 支线 | `docs/rework-graph.json` | ❌ |
| 追溯覆盖对账 | 三校验器输出 | ❌ |

## 3. 视图规格（字段 × 展示）

本层**要展示什么**（与具体插件语法无关的**数据契约**）：

| 字段 | 来源 | 展示建议 |
|---|---|---|
| **feature** | 目录名 `spec/<feature>/`（探针目录，非 front-matter 键） | **分组键**（每 feature 一行/一卡） |
| **type** | `type` | 列 / 筛选（六类词表） |
| **version** | `version` | 列 |
| **status** | `status` | 列 / 分组（**须注明词表随 type 分档**，勿跨档比较） |
| **date** | `date` | 列 |
| **depends** | `depends` | 列（数组） |
| **upstream** | `upstream` | 列（多为 `null`） |

> **建议的落点**: 一张 **table 视图**（feature × type × version × status × date × depends）+ 可选 **board 视图**（按 `status` 分组）。**按 `status` 分组的读法须显式标注「词表随 type 分档」**，否则会把 `accepting`（CHECKLIST 档）与 `verified`（一般档）误作同一把尺子。

## 4. 施工口径（外部面，本仓不载语法）

- **视图语法（Obsidian Bases 的 `*.base` / Dataview 的 DQL / JS）属外部运行时面**。**本卡不复制任何插件语法**——避免以**未在真机验证的语法**冒充「可用配置」（反幻觉纪律：本仓只承载 **E1 可核**的数据契约，语法须在 vault 侧自行核实）。
- **施工位置** = Obsidian vault 侧（**非本仓**）。**挂载** = 以本仓为数据源**只读**打开（vault 或其子集指向 `f:\Spec_Workflow`）。
- **证据等级**: 本文 §1 / §2 / §3 = **E1**（本仓机械重数）；§4 语法面 = **E4**（外部，本仓**不背书**成功），须由使用者在 vault 侧按**官方文档**实测。

## 5. 不做清单（显式否决）

| 不做 | 理由 |
|---|---|
| 迁移 console 到 Obsidian | 运行时 GUI **不可提交 / 不可 `--check`**；撞 **I-1 / I-7 / I-10** |
| 采 SQLite / HTTP / MCP 类插件 | 违本仓**零依赖** |
| 由本仓引入 Obsidian Git 自动提交 | vault 侧用户可自配，**不属本仓机制**；本仓零外部件 |
| 回写任何 front-matter / 表 / 派生物 | 防**第二真值源**（边界 ②） |
| 把本层当状态真值或接门禁 | 边界 ① / ③ |

## 6. 边界与回退

- **本卡** = **Layer-0 文档**（零代码；可删）；**探索层** = **Layer-2**（外部，仓内**零足迹**）。
- **回退** = 停用 / 删除该视图，或删本卡 ⇒ 无仓内数据迁移、无门禁影响。
- **不变量保持**: 本层**不新增**任何真值源、**不新增**门禁、**不新增**外部依赖。

## 7. 参考

- [RESEARCH.md](RESEARCH.md) **§7.30**（Obsidian 插件复用判定与 console 升级可行性；判定 **B-27**（基座不匹配）+ **C-39**（非权威只读探索层））
- [RESEARCH.md](RESEARCH.md) **§7.33**（C-39 落地记录）
- [DESIGN.md](DESIGN.md)（console 设计；权威视图契约）
- [docs/CONSOLE.md](../../docs/CONSOLE.md)（**权威**只读派生态）
