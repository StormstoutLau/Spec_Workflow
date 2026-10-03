---
id: academic-writing-workflow-RESEARCH
type: design
version: 1.15
status: in-review
date: 2026-10-01
depends: [community-ecosystem-RESEARCH, loop-engineering-RESEARCH, DISTRIBUTED_AGENT_RESEARCH, ADR-0010]
upstream: null
---

# 调研文档：学术推理写作工作流——与当前框架的同构分析（P-040）

> **Feature**: 学术推理写作工作流的工程化管理（LGMM 场景驱动）
> **创建日期**: 2026-09-11
> **状态**: in-review（调研批，Step 1-2）
> **Spec 步骤**: Step 1-2（调研 + 三问懒加载门禁）
> **任务来源**: 用户指令「执行另一个与当前框架存在同构关系的调研任务 以学术推理写作为例 一般包含 调研 缺口分析 初步设想 模型方法构建 数据获取 初步结果 草稿撰写 模拟评审 反馈迭代 每一个步骤都会产生连锁式影响 且需要频繁进行审查 修改 需要控制版本 保持数学-算法实现-数据-结果-论文表达一致性 每一步改动都要自动产生下一步状态提醒 以用户学术仓库为例 D:\Article\Working paper\LGMM ... 同时需要记录研究日志 路线 变更历史 用户在学术推理中面临各种复杂的管理 验证 请结合用户场景 开源社区优秀案例进行分析」
> 参考先例: P-039 分布式 Agent 执行（同构框架调研批）、P-028 loop engineering、P-018 community-ecosystem
> **v1.1 补充调研（用户指令「补充调研 学术推理写作与当前框架开发中 有什么UI工具框架可以实时反馈工作流 状态 阶段 防止用户认知过载出现漂移 遗忘 / 学术推理中也包含ai工作流 也需要进行结果审计 决策链追溯 严格抑制幻觉 且每一个步骤可能包含微工作流 如何实现 / 学术写作中的连锁反应必须建立某种硬规则 类似图结构 状态机等模式 请仔细搜索开源社区 学术研究等信息 进行深度调研」）**: 新增 **§7 补充调研——UI 实时反馈与认知防过载**（AgentGUI / 认知负荷心理物理实证 / Msft AI brain fry / Racc 认知设计原则 / LLM observability / AutoGPT 三级粒度）、**§8 补充调研——AI 工作流审计·决策链追溯·幻觉抑制·微工作流嵌套**（COCO / AWorld Guard / 形式化护栏 AgentGuardian+ACM / W3C PROV / auditable-ai 谱系 / 幻觉抑制生成侧 / HAACS 层级 Petri 网）、**§9 补充调研——链条连锁反应硬规则（图/状态机）**——**13 条新 A**（A-15~A-27）+ **B5/B6/B7** + **C-4/C-5** + **H3/H4**；断言 **A 14→27 / B 4→7 / C 3→5 / H 2→4**（附录同步，参考文献顺延 **§10**）。
> **v1.2 补充调研（用户指令「本仓 doc-first + 每 feature 事件流独立 但是存在上下文问题 ai输出冗长且大量信息需要用户反馈 用户缺失存在认知过载 且用户在开发研究过程中需要经常注入外部信息 在主线开发研究过程中也需要fork形成支线探索 / UI 实时反馈 / 认知防过载 实现自动化追踪 任务看板等类似功能 需要仔细调研分析一下」）**: **织界线修正 C-5 前提**（per-feature 事件流独立 = **多流并存**非单流，+ fork 支线 + 长输出 + 频繁外部反馈 → 本仓认知过载**真实存在**，故不"免征"亦不"排除一切 UI 层"）——新增 **§10 补充调研四——任务看板与自动化追踪**（Magentic One Task/Progress Ledger 二账本 / Backlog.md + Markdown Task Board + Kanban.md markdown 原生看板 / git worktree + log graph fork 可视化）——**4 条新 A**（A-28~A-31）+ **B8** + **C-6** + **H5**；断言 **A 27→31 / B 7→8 / C 5→6 / H 4→5**；**裁定=C-6**（本仓认知过载缓解的正确形态 = **markdown-native 只读看板生成器**（stdlib，聚合 PROGRESS+sessions verdict 为单行认知块，按状态分组）+ git worktree/log graph 表达 fork——**零 GUI 服务器/零新依赖/AI 可写**；**仍按懒加载 gate**，仅登记概念，零代码改动，触发条件=用户明确要求落地 board 生成器）；参考文献顺延 **§11**。
> **v1.3 补充分析（用户指令「看板生成器具体设计是否能够实时反馈 自动抓取 自动状态更新 而不用依赖用户指令 请补充分析」）**: 明确回答 = **可以，且三条自动触发路径均已成熟**——① **事件驱动自动抓取**（改 PROGRESS/SOURCES 源头即触发；`watch-inbox.ps1` FileSystemWatcher 实作"文件变化→自动处理"模式、.NET FileSystemWatcher 为 Windows 本地零新依赖方案）；② **门禁钩子自动重生成**（do-knowledge-studio/*_skill `update-docs.mjs` + GitHub Actions push→自动更新生成节 + pre-commit 自动更新文档区、ProjectOdyssey badge 自动计数防 drift——本仓已有 pre-commit 四 hook/repo_stats 机械对账，**直接把 board 生成器并进 step-gate/pre-commit 即为"提交即刷板"，零新依赖**）；③ **终端实时渲染**（agent_pulse/cc-aio-mon = 轮询 temp(500ms 刷新 snapshots → 全屏 TUI progress bar，非阻塞不依赖用户指令 / Rich Live refresh_per_second=4 / minimal-tui rich+tqdm stdlib 主、省依赖）——纯 stdlib `watch -n` + 终帧重绘即可达同效（无需引入 rich/tqdm/Textual 重依赖，与零依赖 D6 一致）；**按 Clash 断言分层 A-32~A-34 + B9**，**裁定 C-7 = 看板可"被动由事件/hook 自动更新 + 可选主动终端轮询展示"，完全脱依赖用户指令**；三档自动强度（L0 门禁触发=提交自动刷 / L1 文件监听=源头改动即刷 / L2 终端轮询=常驻实时刷新）；懒加载 gate 保持，触发仍=用户要求落地 board 生成器；参考文献顺延 §12。
> **v1.4 补充调研（用户指令「回到P-40问题 学术推理还存在回溯的情况 也就是后面的步骤可能没有达到预期需要调整前面的步骤 模拟评审的意见可能需要对多个步骤进行调整 数据获取有困难可能需要再次启动调研 结果不理想可能需要重新进行缺口分析 请执行补充调研」）**: 新增 **§12 补充调研五——回溯与反馈回路（"后步证伪前步"的工程化）**——分四层取证：**补偿**（Saga 补偿事务 + pivot 不可回退点 + 幂等补偿）、**留痕**（durable execution append-only + replay / prospective vs retrospective provenance / DANTE「冻结合同 + 只恢复兼容工作」）、**回跳**（CSP 非时序回溯 backjumping·CBJ·CDCL：跳到冲突源而非退一步；thrashing 定义）、**重算**（内容寻址重跑判据 Snakemake / Nextflow / OxyMake + mtime 双向失效）；并按用户三场景分别取证（**返修轮次语义** major-vs-minor + 跨轮期望 / **ToolMaze 扰动 2×2** 与重试-重规划分流 / **HARKing-预注册-负结果** 规范）；**15 条新 A**（A-35~A-49）+ **B10/B11/B12** + **C-8/C-9** + **H6/H7**；断言 **A 34→49 / B 9→12 / C 7→9 / H 5→7**；**裁定 = C-8**（回溯可行且以既有机制承接——append-only / `fork` / 多轮 `vN` session / ADR `supersede` / M7 已备（B11），正确形态是**纪律**（非时序回跳到因果源 + 最小回改集 + 旧值留痕）而非引擎（Saga/DAG/状态机库违 D6 零依赖）；**仍止于调研**，懒加载 gate 保持，触发条件 = 出现一次「影响集失控」真例）+ **C-9**（收敛控制判据登记：轮次上限 + 进展判据，**仅纪律不落工具**）；参考文献顺延 **§13**。
> **v1.5 补充调研（用户指令「除了我举例的三个场景 是否可以进行盲区扫描 补充调研 针对学术推理写作场景」）**: 新增 **§13 补充调研六——盲区扫描（五轴系统性排查）**——按 P-015 先例（**多维轴 + 证据分级 + 环境维度**）排查六轴，**过程轴 / 证据轴显式声明为已覆盖并说明理由**（避免为凑数而制造盲区），其余**四轴均扫出真盲区**：**环境轴①**（外部世界变化使"当时正确"的前步过期——A-50 LSR 预设更新触发 + **三分类分流** / A-51 reference rot「**link rot vs content drift**」1/5~7/10 / A-52 撤稿传染 >63,000 且**撤稿后引用提及率 <5%** + 可机械化核验链）、**合规轴②**（A-53 AI 披露规范 + **政策效力被实证证伪**：70% 期刊有政策但 75k 篇中仅 76 篇(~0.1%)披露 / A-54 引用幻觉 18–69% 且**穿透 NeurIPS 同行评审** / A-55 重复发表·文本回收·香肠切片三现象（直击多期刊变体策略）/ A-56 会议**必填 checklist 缺则 desk reject**）、**时间轴③**（A-57 **scope freeze / scope lock 双层冻结** + "只有修错与补合规可直接进，其余进 parking lot"）、**人轴④**（A-58 escalation of commitment 双向风险（Staw 1976 / Arkes & Blumer 1985 [85% vs 10%] + **premature de-escalation**）/ A-59 **kill criteria 与 renegotiation trap**）；**10 条新 A**（A-50~A-59）+ **B13~B16** + **C-10~C-12** + **H8/H9**；断言 **A 49→59 / B 12→16 / C 9→12 / H 7→9**；**裁定 = C-10**（环境轴优先级最高——唯一一类"本仓完全无对应机制"的失效；采纳三分类分流 + 触发式重检候选，**懒加载 gate 保持**）+ **C-11**（**投稿前合规四检**登记为纪律：引用核验 / AI 披露 / 重叠声明 / 报告规范清单；**引用核验建议优先触发工具化**——0.1% × 18–69% × <5% 三者叠加下人工核验不可能可靠）+ **C-12**（**freeze 与 kill criteria 必须预先写定**，并显式防 renegotiation trap）；含**扫描结论表**（六轴 × 结论 × 本仓 Gap × 处置）；**零工具改动**；参考文献顺延 **§14**。
> **v1.6 补充调研（用户指令「环境轴 我的理解是 必须建立某种研究目标扫描机制 定期扫描预印本网站 搜索关联文献 防止目标缺口被填满 方法思路被抢发 是这个意思吗 或者目标期刊风向变化 审稿人taste变化 学术风向 技术潮流 数据开放等等层面」+ 两问裁答「全三层，一次做完」「设计成零依赖半自动形态」）**: 新增 **§14 补充调研七——目标竞争与评价漂移（环境轴 B/C 层细化）**——把环境轴拆为 **A 时效性失效（§13.2 已覆盖）/ B 抢先失效 / C 评价标准漂移 / 机会窗口** 四层，本轮补后三层：**B 层**（A-60 多重独立发现是常态：Hagstrom 1,718 人中 **46.2% 自认被抢先 1–2 次** / A-61 Hill & Stein 追踪 **1,630 场竞赛**实测首发 58 : 次发 42，而研究者主观预期 71:29 **严重高估** / A-62 **机构地位反转惩罚**——独立研究者须按最坏情形规划 / A-63 arXiv 时间戳即优先级声明（date-stamped priority claims）但过早公开**污染 novelty 判定** + 10k Monte-Carlo 论证"等 3–6 个月"实为"等 1–3 年" / A-64 **desk reject 首要过滤器就是 novelty（占 51%），且编辑会交叉比对本刊近期发表**）；**C 层**（A-65 NeurIPS 2014 双委员会实验 **25.9% 决策不一致 + accept precision 0.495** / A-66 **50% 评分方差源于主观性** + "善识别差论文、不善识别好论文"的不对称 / A-67 NeurIPS 2021 复现 **23.0% 不一致且不随规模改善** / A-68 风向可测：术语漂移·期刊专题·领军者转向，趋势可**提前 18 个月**检出）；**机会窗口**（A-69 NIH DMS Policy 强制的数据开放 / A-70 **同一政策消灭"数据护城河"**——机会与威胁同源 / A-71 技术潮流/危机把"快"变标准：bioRxiv **2 天** vs 传统 **125 天**）；**零依赖半自动形态**（A-72 告警/现状知悉是成熟领域——Scholar 三类告警·PubMed 保存检索·arXiv RSS·期刊 TOC，**本仓无需自建检索** / A-73 "人抓-工具记"先例 + 日/周/季三层节奏 ≙ C-7 三档强度）；**14 条新 A**（A-60~A-73）+ **B17~B19** + **C-13/C-14** + **H10/H11**；断言 **A 59→73 / B 16→19 / C 12→14 / H 9→11**；**裁定 = C-13**（B/C 两层为真盲区但**优先级低于 A 层**——A 层污染既有记录，B/C 层只浪费投入或判决不公；**零依赖半自动形态落地为「纪律 + 本地清单」**，不建抓取、不引依赖，触发=一次真例；懒加载 gate 保持）+ **C-14**（**抢先预警与止损正式耦合**：B 层预警即 kill criteria 所要求的前瞻性证据 → 形成完整判据链「**A-50 三分类 × B 层抢先预警 × A-59 kill criteria**」）；含 **四层对照表**；**零工具改动**；参考文献顺延 **§15**。
> **v1.7 补充调研（用户指令「补充扫描用户的论文仓库实例 里面有 lean4 形式化证明 逆向拆解文档 文档散乱管理不够规范 / 当前调研的是学术推理写作场景还有什么可以再补充调研的 系统性规范化用户的论文写作流程」）**: 新增 **§15 补充调研八——论文仓库实例扫描与流程规范化**（与前面七轮方法论不同：**先对 `D:\Article\Working paper\` 下 7 个论文仓做机械盘点（E1），再按症状检索社区标准**）——**实测读数** = **521 目录 / 4503 文件**（排除 `.lake`/`.git`）；**474 个编译产物**与源码混放（`.aux` 101 / `.log` 111 / `.out` 86 / `.toc` 54 / `.dvi` 32 / `.bbl` 29 / `.blg` 26 / `.fls` 18 / `.fdb_latexmk` 17）；残留 **40 压缩包 / 10 `.bak` / 34 `fix_*`·`debug*` 脚本**；**137 种 `.tex` 文件名**（含 `document.tex` 及状态词入名的 `*_v2_Final`·`*_v3_Corrected`·`*_v4_Reviewed`·`_v9_Rigorous`·`_v5_complete`）；**治理文档同名不同格式**（`CODE_WIKI.md` 6 + `Code_Wiki.md` 3 = **9**；决策 **3 名**；开发日志 **3 名**；spec **4 名**）；**版本目录命名 ≥5 种形态**；**Lean 双源漂移**（`LGMM 8.0/lean4/` 15 文件 vs `LGMM_Lean/LGMM/` 12 文件，**文件集不一致**）；`.lake/` 入库；`papers_achived` 错拼；**规范化程度极不均衡**（`LGMM 8.0` 接近 compendium，`Volsurface_SABR` 为裸 tex 堆）——**归因**到六层缺失（派生物分界 / 单一真值+版本外置 / 文档契约 / 证明制品单一归属 / 脚本生命周期 / 可复制骨架）；**五层社区标准对号**：**A-74 Research Compendium**（Marwick 2018 + The Turing Way：约定结构 / 数据-方法-产出分离 / 环境指定）+ **A-75 RO-Crate**（1.1 推荐级，`ro-crate-metadata.json`，just enough linked data）+ **A-76 Lean 项目硬约定**（`lean-toolchain` + `lakefile.toml` + `lake-manifest.json` + **`.lake` typically gitignored**；模块 root 只放 import；依赖钉 tag 不钉 main）+ **A-77 Lean blueprint**（`leanblueprint` → Verso；**LeanArchitect** arXiv:2601.22554 以注解内联消除「LaTeX 与 Lean 重复→漂移」；**BlueprintRepair** arXiv:2607.28110 类型化局部编辑成本最低 1.30× vs 2.06×）+ **A-78 LaTeX 卫生**（成文黑名单 + `outDir` 重定向 + `autoClean`；**陈旧 `.bbl` 会产生错误参考文献**）+ **A-79 命名共识**（ISO 8601「字母序=时序」；两分隔符规则；**「一旦 final 进了名字，就没有词留给下一个版本」**）+ **A-80 代价量化**（**73% 数据重复事件源于命名不一致** / **89% 每周浪费 ≥1h** / 日期格式不一致使检索慢 **34%**）+ **A-81 ACM 制品徽章**（Available/Evaluated/Validated 三类独立；**"such as Zenodo but not GitHub"**；版本标签范式 `R1-submission`/`camera-ready`/`AEC-*`）+ **A-82 Diátaxis**（四模式按**用户意图**划分；**硬规则=同一页面禁止混模式**，其价值被定位为"最大可读性收益来自这条硬规则本身"）；**9 条新 A**（A-74~A-82）+ **B20**（症状与本仓不变式**逐条对偶**：I-5/I-6↔派生物不入真值区、I-1↔一份真值、I-3↔名=身份版本=元数据、I-7↔同名必须同义、I-10↔证明制品单一归属、I-8↔脚本分层）+ **B21**（"逆向拆解文档"的正确形态=blueprint，人工文档只留 Explanation）+ **B22**（多版本发表/返修阶段语义应由 A-81 式**标签**承载）+ **C-15**（**分层落地而非一次重整**：先立"一页 `CONVENTIONS.md` + 三模板"**零工具零依赖**契约层，再逐仓迁移）+ **C-16**（规范化价值在**可机械检出**——四条判据中 ①②④ **与 project-console 三件套完全同构可复用**）+ **C-17**（**blueprint 为性价比最高的新增**——134 个 `.lean` 已有、依赖关系却只在人脑；**仍懒加载**，触发=决定做成可被第三方独立核查的制品）+ **H12/H13**；断言 **A 73→82 / B 19→22 / C 14→17 / H 11→13**；含**实测读数表**与**症状-不变式对偶表**；**零工具改动**；参考文献顺延 **§16**。
> **v1.8 补充调研（用户指令「先补调研共享层和辅助资产归属」；缘起 = v1.7 后的覆盖度审计发现两项真空白）**: 新增 **§16 补充调研九——共享层与辅助资产归属**。**方法论**：先做**覆盖度审计**（把 §15 六层根因逐条核对"已有覆盖 vs 真空白"，结论 = **六类中五类解法已在手**：4 类来自已调研社区标准、1 类来自本仓既有机制可直接外推，**仅两项真空白 + 1 项触发式**），再**先补一手实测（E1）后按症状检索**。**E1 增补读数**：**共享层（`Working paper/` 根 13 文件）实为"多用途杂层"** = ① 论文级共享资产（`CODE_WIKI.md` / `Academic Phrasebank Navigable PDF 2018.pdf` / 热点分析.pdf）② **归档快照**（`LGMM_0727.rar` / `MIDAS-Granger.rar`，**根目录无对应解压副本** → 根已被当"归档层"）③ **个人/职业内容**（`potemkin-village-notes-en.md`(+`.bak`) / `职场经历对话记录.md` / `草台班子复盘.md` / `草台班子观察笔记.md`(+`.bak`)）④ 跨项目脚本（`turnover_backtest.py` + png）；**实际项目数 ~17 个**（用户之初仅报 7 个）；**辅助资产总量** = `.pdf` **363** / `.csv` 404 / `.png` 199 / `.txt` **121** / `.json` **114** / `.docx` 18 / `.xlsx` **4** / `.canvas` **3**（**`论文参考资料/` = 与论文项目平级的独立"资料层"**）；**同名多处** = `files.zip` ×**10**（**与解压目录并存**）/ `.pytest_cache` ×**9** / `SKILL.md` ×**13**（含第三方 `.agents`/`.claude`/`.trae` 技能目录）/ **`document.tex`·`.pdf`·`.aux`·`.log`·`.synctex.gz` 各 ×6–7** / `CODE_WIKI.md` ×6 / **文献提取文本 4 种命名**（`barunik_extracted.txt` / `extracted_text.txt` / `temp_*.txt` / `_dl_ks_igmm.txt`）。**八条社区标准（A-83~A-90）**：**A-83** monorepo / polyrepo / **hybrid 三元**（Brousse, ACM *Programming '19*；Hybrid 两变体 **Poly-as-Mono** 与 **Mono-as-Poly**；该主题学术研究不足）+ **A-84** **monorepo vs polyrepo 是组织问题而非工程问题，且有可操作规模判据**（Meta 巨型 monorepo vs AWS 千仓 polyrepo 双向代价；"**Discoverability is terrible**" vs "**删一个函数可能有 200+ 跨团队引用**"；**判据 = 「Team size 1–50 且需要协调 + 共享数据模型/基础设施」→ monorepo**）+ **A-85** 共享层三种成文形态（group-handbook「**共享层首先是一份规范，而不是一个目录**」/ `research-template` 的 `00_admin`+`data_policy.md`+强制 `workspace.code-workspace` / 论文仓规范 README 必含 **Article Information + Reproducing Results** / Fred Hutch 实证「**与未来的自己及未来加入的成员协作**」）+ **A-86** **文献副本能否入仓取决于"版本"而非"是否被引用"**（**Preprint / AM / VoR** 三分；**多数出版商不允许自存档 VoR**；Cambridge Green OA 附 CC BY-NC-ND + embargo；SHERPA/RoMEO；**作者的自身复用权 ≠ 向他人分发权**）+ **A-87** **Zotero stored vs linked + 仓内只留引用键**（官方强推 stored；Better BibTeX 自动导出；「Zotero + 云盘」模式）+ **A-88** **codebook 是有一标准格式的一等制品且须"采集前创建"**（必含列 / **缺失值编码须超值域且分因** / 变量命名规范 / 多选拆 0-1 / **DDI-Codebook** 标准 / **随数据集一并提交**）+ **A-89** **PARA × Zettelkasten 双引擎须物理分离、功能双向链接**（执行引擎 vs 洞察引擎；失效模式被点名「**读得不够就先链接太多**」/「**有用的想法被困在文件夹里**」；47% 保存内容不再被打开）+ **A-90** **笔记仓化与隐私**（私有 Git 仓无容量上限但**并非端到端加密**；`.obsidian/workspace*.json` 与插件 `data.json` 须 ignore；community plugins 未必安全）。**B23**（用户现状精确对应 **`Mono-as-Poly`——有 monorepo 形态、无其机制**；A-84 判据指 monorepo 侧 → **不拆分、补机制**；并消解根 `CODE_WIKI.md` 的定位问题：作为顶层索引**定位合法、名不副实**）+ **B24**（**辅助资产归属"一次判定"表**：文献 PDF **移出仓** / 提取文本 = **派生物不入仓** / codebook **升为一等制品** / 笔记 **分离为独立 vault** / **个人职业内容物理隔离（优先级最高）** / 归档快照待裁）+ **B25**（**共享层正确形态 = "一份规范 + 一个索引 + 一个红线清单"** → `WORKSPACE.md` / `INDEX.md` / `data_policy.md`）+ **C-18**（两项空白已关闭，**不需新方法论亦不需外部机制**；与 v1.7 的 C-15 契约层**合并为同一批交付**；触发=用户指定首个迁移仓）+ **C-19**（**隐私隔离优先级最高——高于整洁、高于规范**：`Working paper/` 同时含可公开产出与绝不外传内容，整体打包即不可逆泄露，且私有仓非 E2E → `data_policy.md` 为**首件交付**）+ **C-20**（**辅助资产三层收敛**：**真值层 / 参考层 / 私域层**，**层间唯一连接是引用键而非文件复制** → 从根上消灭 `files.zip` ×10 与 `document.tex` ×6）+ **H14**（归档快照处置未裁决——**裁决前不得删除**）/ **H15**（363 PDF 版本构成未实测 → **默认按不可再分发保守处理**）；断言 **A 82→90 / B 22→25 / C 17→20 / H 13→15**；含**增补实测表**与**归属裁定表**；**零工具改动**；参考文献顺延 **§17**。
> **v1.9 补充调研（用户指令「单独调研一下是否可以执行分步走策略 先建立文件 工作流规范 命名 数据等论文写作学术推理规范 将此标准广播给其它项目执行清理 然后再建立后续学术推理工作流」）**: 新增 **§17 补充调研十——分步走策略的可行性**。**缘起**：用户把 v1.7/v1.8 的落地形态明确拆为"先立规范→广播清理→后建推理工作流"三步，追问是否可执行。**方法**：先做**依赖结构分析**（S1 契约层 / S2 清理层 / S3 工作流层之间的依赖方向），再**补充社区证据**（contract-first 契约先于管道 + strangler fig 增量迁移 vs big-bang）+ **A-91**（契约先于实现的社区共识：Martin Fowler 数据契约 / Thoughtworks contract-first / DMM 5.1 治理先于自动化）+ **A-92**（strangler fig / 增量迁移 vs 一次性重整：后者失败率被反复证实）+ **B26**（依赖结构推断：S3 依赖 S1 但不依赖 S2——工具建在契约上、不依赖"某仓已清理"；故"广播清理"应先以**单仓 pilot** 验 H12 最小充分集，再决定"一次性广播 vs 逐仓"）+ **C-21**（分步走可执行且与 C-15/C-19 同构：先立契约、后广播、再建工作流；但**广播≠统一重整**，须遵 C-15 逐仓 + C-16 可机械检出判据）+ **C-22**（"广播"的正确读法 = **标准唯一 × 执行逐仓**，且**首个广播对象应选最接近 compendium 的仓做 pilot** 以实测契约最小充分集，不跳过 H12/H13 两个动仓前门禁）+ **C-23**（推导到 v1.7 的 C-15 触发条件一致性：广播执行即 C-15 的"逐仓迁移"，故 C-15 触发=用户指定首个迁移仓与 C-22 的 pilot 选择是同一动作）；**H16**（"广播"的推进粒度未裁决：单仓 pilot 验证后应该"gap-fill 全量翻新"还是"strangler-fig 渐进替换 17 仓"——依赖 H12 实测结果，登记观察项）；断言 **A 90→92 / B 25→26 / C 20→23 / H 15→16**；**零工具改动**；参考文献顺延 **§18**。
> **v1.10 pilot 实测批（用户指令「基于 LGMM 8.0 升级任务卡」→「按这个方案来」）**: 新增 [PILOT_TASK_CARD.md](PILOT_TASK_CARD.md)（P-040 落地执行清单，type: template，v0.4），并在 **`D:\Article\Working paper\LGMM\LGMM 8.0` 只读跑全部迁移判据（零写入，守 H14）**。**实测矩阵** = 编译产物 26（live 20 + archive 6）/ 状态词 18（其中约 12 属第三方子仓 `data/co_pricing_zoo`，非本仓缺陷）/ **Lean 双源 hash**（16 专有 → 与 `LGMM_Lean/LGMM/` 同名 13，**12 内容一致 + 1 DIFF（`EWNLS.lean`）+ 3 仅本仓**）/ 根层同名 0 / **README 仍引 `MAPPING.md` vs MANIFEST 已归档（声明冲突）** / **MANIFEST 声明 lean=14 实测 16（声明漂移）** / 脚本分层已合规（`code/scripts/` 七子层）/ `data/CODEBOOK.md` 缺失 / `data/manual_llm/` 2 文件待归红线。**观察项状态更新**：**H12 由"未实测"→"部分实测"**（骨架层充分、**判据层不足**：最小充分集须含"可跑命令 + 排除第三方子仓 + hash 对比"）；**H13 由"未实测"→"数据齐备待裁决"**（真值源方向趋于 `lean4/`，**确认前不删任一份**）。**断言计数不变（92A+26B+23C+16H）**——本轮为既有 H12/H13 的状态更新与实测回填，无新增断言行；**零工具改动**；参考文献仍 **§18**。
> **v1.11 裁决证据落档批（用户指令「基于 LGMM 8.0 文件夹相对规范 请在此基础上升级」→「先做派生物清理」→「现将论文工作 裁决证据完整落档 挂起」）**: 新增 **§17 补充调研十——分步走策略、pilot 执行与裁决证据**（**补写 v1.9 横幅已声明但正文缺失的节**；参考文献顺延 **§18**）。**执行实录**：派生物清理三档 **T1 485 + T2 48 + T3 61 = 594 条目**（→ `_trash\2026-09-14-derived`，**911 文件 / 28,385,385 B**）；3 个非 TeX `.log` **fail-closed 挂起后单独处置**（脚本生成 / 输入法垃圾 / `tee` 捕获三类，**同名不同性质**）；五仓 **tracked-artifacts = 0** → 移动产生**零 git 变更**；`LGMM 8.0` 1 项 + `CDO_8.1` 5 项 tracked 删除经核为**先前遗留**（既不在工作区亦不在隔离区）。**裁决证据包** = 6 个多版本目录 / 22 个 `.tex` / 推荐真值 6 个（其中 2 项**信号矛盾**需人工指认）。**四条新增发现**：**孤儿派生物**（`AL model_old` 9 PDF vs 5 `.tex`，含名带拼写错误的 `…Mode-working paperl.pdf`）/ **版本入名的实证危害**（`SABR-v1` 560 行 > `SABR-v2` 288 行）/ **`.log` 须 fail-closed + allowlist** / **v1.7「`.lake/` 入库」记载证伪**（实测零追踪）——四条均定位为 **H12 最小充分集增补**，不新增编号断言。**挂起登记 G-01~G-13**（真值指认 / 命名规则 / T4 `.lake` / 承 H14-H16 / PILOT_TASK_CARD 自相矛盾待订正）。**§0 计数据实订正**：A 90→**92**、假设区 15→**16**（H16 补入）——修正跨文档计数漂移（CODE_WIKI 早已声明 92A+16H）；断言计数保持 **92A+26B+23C+16H**；**零工具改动**。
> **v1.12 引文二次核验批（用户指令「回到学术推理框架 先根据之前学术仓库情况 补充学术文件规范 写一份任务卡 交给学术仓库agent执行」；本批 = 「先落档」之 B 项）**: 对 P-040 自身的高风险引文做**独立二次核验**（时序独立于原取证轮）——**A-17 原引《The Agentic AI Oversight Problem》（署名微软 / UC Berkeley / 清华，含 POMDP 模型 + 监督准确率 92%/62%/17% + 注意容量 C≈3–5）**：arXiv 官方 API 精确短语检索 `all:"Agentic AI Oversight Problem"` **totalResults = 0**、Semantic Scholar / DBLP **零条目**、MSR 与会议页**无匹配**、两条具名细节（所谓通讯作者 **Sarah Sterman 实为 UIUC HCI 研究者**；术语"**AI brain fry**"另属 **BCG × UC Riverside**）**均可证伪** → **判定疑似虚构引文（形态 III）**。**处置 = 据实换源**：命题保留、**原引具体数字一律撤回**、**断言编号 A-17 保留 → 计数不变**（92A+26B+23C+16H），全文既有下游引用（§10.1 的 B8 引 / 附录 B 的 B5·B8 `basis`）**继续有效**。新增 **§18 补充调研十一——外部引文二次核验**（可复现检索式与入口清单 / 不可核验线索不作证据 / 三条同轴替代一手来源逐字 / 三条取证纪律收获），**参考文献顺延 §19**；同步改写 §7.3 标题与正文、§0 的 A-17 条目、§17.7 追加说明、§19 原条目划线存档并补替换来源。**零工具改动**。
> **v1.13 G-13 订正批（用户指令「先修复 G-13 矛盾」；Layer-0 文档批、零代码）**: 订正 §17.6 挂起登记 **G-13**——[PILOT_TASK_CARD.md](PILOT_TASK_CARD.md) §0「进入门槛」原写「`LGMM_Lean/` 为 mathlib 全量（7735 .lean）、非第二专有源」（该结论出自卡 v0.2，已被**卡自身 v0.3 行明文推翻**），与同文档 §2.3 / §2.8 的 hash 实测结论**自相矛盾**（同一文档内两处相反结论）。本批据 **v0.3 口径**改写 §0 该格（**双源真实存在**——`LGMM 8.0/lean4/` 16 专有与 `LGMM_Lean/LGMM/` 同名 13 = **12 内容一致 + 1 DIFF（`EWNLS.lean`）+ 3 仅本仓**；真值源暂记 `undecided`，**裁决前不删任一份**）+ 卡补变更记录 **v0.5** 行（含「性质 = 表述同步欠账，非新实测」定性）+ front-matter `version 0.4 → 0.5`。**性质与边界** = 表述同步欠账，**判据列与实测矩阵一字未动**；本文件断言编号与计数 **零改动**（92A + 26B + 23C + 16H）；§17.6 该行状态转「**已订正**」，其余 **G-01~G-12 仍挂**（其中 **G-12** 即承 **H13** 的双源真值指认，属内容判断，仍待用户裁决）。**零工具改动**。
> **v1.14 G-12 双源真值取证批（用户指令「继续处理 G-12 的双源真值指认」；Layer-0 文档批、零代码）**: 对 §17.6 **G-12** 做**只读取证**（`D:\Article` 侧**零写入**），新增 **§17.8 G-12 双源真值取证与指认建议**（十一项判据表 + 结论 + 三条派生发现 + 处置三档建议）。**结论 = 内容真值源为 `LGMM 8.0/lean4/`**——四路判据同向（文件集 ⊂ / 文本行 99.84% ⊂ / 声明集 34 ⊂ 43 且 B 零独有 / mtime 晚），且**由该仓自身 changelog 自证**（A 侧根模块头部「v8.1」+「v9.1 Changelog（2026-08-01）」明列实测到的 A 独有声明 5 个与 +2 公理）⇒ **该指认属机械可判，非内容判断**；G-12 状态由「数据齐备待裁决」改为「**证据齐备·机械可判，待用户追认 + 处置裁决**」。**三条派生发现** = **F-1** v9.1 证明集**当前不可构建**（A 有源无工程、B 有工程但根模块 import 面仅 13 且内容停 v5.0 时代 ⇒ 「No sorry placeholders remain」类声明无法用 `lake build` 复现）/ **F-2** v9.0/v9.1 全部改动**未提交**（内层仓 HEAD `e200be9` 落后工作区，`lean4/` 4 文件已改未提交，`EWNLS.lean` **+178 −1** ⇒ 一次干净克隆即丢失）/ **F-3** 朴素 `grep sorry` **假阳性 10 例**（全为 changelog 散文提及，剥注释后真实 0 —— 同族 = 本仓 P-061 M5 假阳性）。**边界** = `D:\Article` 侧零写入（未提交 / 未同步 / 未删除任何文件）；**不新增编号断言**（读数以 §17.8 实测表承载，口径保持 **92A + 26B + 23C + 16H**）。**零工具改动**。
> **v1.15 完成度评估与阻塞项分类批（P-071，用户指令「分析学术推理框架完成度」→「学术框架阻塞项分类调研先落档 然后按照建议顺序执行」；Layer-0 登记批、零代码）**: 新增 **§17.10 完成度评估与阻塞项分类**——分层完成度矩阵（S1 契约层 / S2 清理层 / S3 推理工作流）× 本轮实测发现（**F-1** 各仓 S1/S2 已就地落档（2026-10-02/03，4 仓各 **9 件**齐）/ **F-2** H13-H16 已于 2026-10-03 裁决 / **F-3** G-12 P0 已由提交 `79cbdc7` 满足（仓库级未提交面降为 0，**未造空提交**）/ **F-4** 本批写动作 = 工作区根三件套落盘（`data_policy.md` **4,241 B** + `WORKSPACE.md` **2,282 B** + `INDEX.md` **5,322 B**〔17 项目登记〕；UTF-8 无 BOM；**未 commit / 未 push**）/ **F-5** 两处与既有记录不符（`LGMM_Lean/LGMM` 实测存在 vs H13 记录「不存在」；**G-12 P1 未执行**，hash 对账 **DIFF/missing = 4**））+ 阻塞项三分类（可立即做 / 等裁决 / 等触发）+ 建议执行顺序（G-12 P1 → H13 记录复核）；**不新增或删除编号断言**（口径保持 **92A+26B+23C+16H**）；**本仓零工具改动**；学术仓侧仅根三件套写、**未 commit / 未 push**。
> **核心目的**: 确认"学术推理写作工作流"与本仓 Spec 驱动框架的**同构性**——把 LGMM 场景的痛点映射到本仓既有机制，识别社区可借鉴构件，判定是否需吸收/承接。

## 0. 断言统计表（必填，审计入口）

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 92 | A-1 用户步骤链 / A-2 LGMM 证据链痛点实证 / A-3 数学-实现断点 / A-4 SciTeX 交口控制 / A-5 交互 literate 编程（Quarto/knitr） / A-6 跨模型审稿 / A-7 PaperJury / A-8 Agentic_Paper 多臂 / A-9 eLabFTW ELN / A-10 auto-research 阶段门 / A-11 Lean4-Coq 一致性 / A-12 预注册-版本化（paper-template Zotero） / A-13 LGMM 已有机制盘点 / A-14 本仓同构机制盘点 / A-15 AgentGUI 观察+转向 / A-16 认知负荷心理物理实证 / A-17 并行监督容量上限与失效退化（v1.12 据实换源：原引疑似虚构，数字撤回，命题保留） / A-18 Racc 认知设计原则 / A-19 LLM observability 平台 / A-20 AutoGPT 三级事件粒度 / A-21 COCO 连续监督 / A-22 AWorld Guard 防幻觉 / A-23 形式化护栏（AgentGuardian CFG+ACM） / A-24 W3C PROV 溯源标准 / A-25 可审计 AI 谱系 / A-26 幻觉抑制生成侧 / A-27 层级状态机/嵌套子网 / A-28 Magentic One 二账本 / A-29 Backlog.md markdown 看板 / A-30 Markdown Task Board 零依赖板 / A-31 git worktree+log graph fork / A-32 FileSystemWatcher 事件驱动自动抓取 / A-33 hook+CI 门禁自动重生成 / A-34 终端实时轮询渲染（agent_pulse/Rich Live） / **A-35~A-49 回溯与反馈回路（v1.4）**（A-35 Saga 补偿事务 + pivot 不可回退点 + 幂等补偿 / A-36 durable execution = append-only + replay（非确定性副作用须移出可重放流）/ A-37 非时序回溯 backjumping·CBJ·CDCL + thrashing / A-38 内容寻址重跑判据（Snakemake·Nextflow·OxyMake）+ mtime 双向失效 / A-39 prospective-vs-retrospective provenance 二分 / A-40 R-LAM 四件套 + reproducibility firewall / A-41 DANTE 版本化合同 + 不可变尝试史 + 只恢复兼容工作 / A-42 ToolMaze 扰动 2×2 + 隐式语义失败 PRR −37% + 容错 scaling 慢 3.66× / A-43 BEAP-Agent DFS 多级回溯 + LATS/SWE-Search MCTS + 重规划步数上限与收敛检查 / A-44 闭环多轮规划「错误归因 + 定位补丁点 + 最小关键步骤回退」 / A-45 返修 major-vs-minor + 返原审 + MDPI 最多两轮大修 / A-46 跨轮审稿期望 R0-R3 + early tolerance is not forgiveness / A-47 HARKing 三型 + p-hacking + 3125 条分析路径 / A-48 预注册 + Registered Reports 的 in-principle acceptance / A-49 负结果规模（1/3~9/10）+ 82% vs 14% 分享落差 + negative≠useless） / **A-50~A-59 盲区扫描五轴（v1.5）**（A-50 living systematic review 预设更新触发 + **三分类分流** / A-51 reference rot 双重形态（**link rot vs content drift**）1/5~7/10 + 14.7% 不可检索 + 9–25% 误引 / A-52 撤稿传染 >63,000 + **撤稿后提及率 <5%** + **可机械化核验链**（citecheck / RWCheck / CiteGuard / retraction-watch-mcp）/ A-53 AI 披露规范（AI 不得署名 + 各社披露位置不一）+ **政策效力实证**（70% 有政策 vs 0.1% 披露）/ A-54 引用幻觉 **18–69%** + 穿透 NeurIPS 2025（53 篇含 ≥100 幻觉引用）/ A-55 重复发表·文本回收·香肠切片三现象 + 分节宽容度 + 处置梯度 / A-56 会议必填 checklist（**缺则 desk reject**，含统计显著性/算力/许可）/ A-57 **scope freeze + scope lock 双层冻结** + 冻结后仅修错与补合规 / A-58 escalation of commitment（Staw 1976 / Arkes & Blumer 1985 [85% vs 10%] / 损失厌恶）+ **premature de-escalation** / A-59 **kill criteria** + pre-mortem + **renegotiation trap** + kill matrix） / **A-60~A-73 环境轴 B/C 层细化（v1.6）**（A-60 多重独立发现是常态（Merton multiples / Hagstrom 1,718 人 **46.2%** 被抢先 1–2 次 / Gaston 203 人 38%+26%）/ A-61 抢先代价可量化且被高估（Hill & Stein **1,630 场**：首发 **58** : 次发 **42**；主观预期 **71:29**）/ A-62 机构地位反转惩罚（顶尖机构被抢时第二名反得多引）→ 独立研究者须按最坏情形规划 / A-63 预印本 = 时间戳优先级声明（date-stamped priority claims）但过早公开**污染 novelty 判定** + 10k Monte-Carlo「等 1–3 年」 / A-64 **desk reject 首要过滤器即 novelty（占 51%）** + 编辑交叉比对本刊近期发表 / A-65 NeurIPS 2014 双委员会实验（**25.9% 不一致 / accept precision 0.495**）/ A-66 **50% 评分方差源于主观性** + 「善识别差论文、不善识别好论文」不对称 / A-67 NeurIPS 2021 复现（**23.0% 不一致，不随规模改善**；spotlight 不一致 >50%）/ A-68 风向可测（术语漂移 / 期刊专题 / 领军者转向；趋势可提前 **18 个月** 检出）/ A-69 NIH DMS Policy（2023-01-25，**无 Plan 不予受理**，FAIR）/ A-70 数据开放**消灭数据护城河**（机会与威胁同源）/ A-71 技术潮流/危机把「快」变标准（bioRxiv **2 天** vs 传统 **125 天**；arXiv 月增 >15,000 篇）/ A-72 告警/现状知悉成熟（Scholar 三类告警 / PubMed 保存检索 / arXiv RSS / 期刊 TOC；**本仓无需自建检索**）/ A-73 「人抓-工具记」先例 + 日/周/季节奏 ≙ C-7 三档强度） / **A-74~A-82 论文仓实测扫描与流程规范化（v1.7）**（A-74 Research Compendium（Marwick 2018 + The Turing Way：约定结构 / 数据-方法-产出分离 / 环境指定）+ rrtools 模板 / A-75 RO-Crate 1.1（`ro-crate-metadata.json`；just enough linked data） / A-76 Lean 项目硬约定（`lean-toolchain`+`lakefile.toml`+`lake-manifest.json`+**`.lake` typically gitignored**；模块 root 只放 import；依赖钉 tag） / A-77 Lean blueprint（`leanblueprint`→Verso；**LeanArchitect** 内联注解消除 LaTeX↔Lean 重复；**BlueprintRepair** 类型化编辑 1.30× vs 2.06×） / A-78 LaTeX 卫生（成文黑名单 + `outDir`/`autoClean`；**陈旧 `.bbl` → 错误参考文献**） / A-79 命名共识（ISO 8601「字母序=时序」；两分隔符；**「final 进了名字就没有词留给下一个版本」**） / A-80 代价量化（**73% 数据重复源于命名** / **89% 每周浪费 ≥1h** / 检索慢 **34%**） / A-81 ACM 制品徽章（三类独立；**"Zenodo but not GitHub"**；`R1-submission`/`camera-ready`/`AEC-*` 标签范式） / A-82 Diátaxis（四模式按用户意图；**硬规则=禁止混模式**）） / **A-83~A-90 共享层与辅助资产归属（v1.8）**（A-83 monorepo/polyrepo/**hybrid 三元**（Brousse ACM *Programming '19*；Hybrid 两变体 **Poly-as-Mono** / **Mono-as-Poly**；该主题学术研究不足） / A-84 **monorepo vs polyrepo 是组织问题且有规模判据**（Meta 巨型 monorepo vs AWS 千仓 polyrepo 双向代价；15 仓迁 1 仓；**判据「Team size 1–50 且需协调 + 共享数据模型/基础设施 → monorepo」**） / A-85 共享层三成文形态（group-handbook「**共享层首先是一份规范而非目录**」/ `research-template` 的 `00_admin`+`data_policy.md`+强制 `workspace.code-workspace` / 论文仓 README 必含 **Article Information + Reproducing Results** / Fred Hutch「**与未来的自己及未来成员协作**」） / A-86 **文献 PDF 入仓取决于"版本"非"是否引用"**（Preprint/**AM**/**VoR** 三分；**多数出版商不许自存档 VoR**；Green OA 附 CC BY-NC-ND + embargo；**自身复用权 ≠ 分发权**；SHERPA/RoMEO） / A-87 **Zotero stored vs linked + 仓内只留引用键**（官方强推 stored；Better BibTeX 自动导出；「Zotero + 云盘」） / A-88 **codebook 是有标准格式的一等制品且须采集前创建**（必含列 / **缺失值编码须超值域且分因** / 变量命名规范 / 多选拆 0-1 / **DDI-Codebook** / **随数据集一并提交**） / A-89 **PARA × Zettelkasten 双引擎须物理分离、功能双向链接**（执行引擎 vs 洞察引擎；失效模式「**读得不够就先链接太多**」/「**想法被困在文件夹里**」；47% 保存内容不再打开） / **A-90** **笔记仓化与隐私**（私有 Git 仓无容量上限但**非端到端加密**；`.obsidian/workspace*.json` 与插件 `data.json` 须 ignore；community plugins 未必安全）） / **A-91~A-92 分步走策略可行性补充（v1.9）**（A-91 **契约先于实现的社区共识**（contract-first：Martin Fowler《Making Your Data Ready for Agentic AI》数据契约"schema is law"/ Thoughtworks-CLI + ODCS / Data Management Model 5.1 治理左移，Data Contracts 是"机器可读、可执行"的治理落点）/ A-92 **strangler fig / 增量迁移 vs 一次性重整**（Martin Fowler 绞杀榕模式 + VRIZE/多篇实战：big-bang 失败率反复被证实；"可回滚的渐进位移"优于"单一 cutover"；每个迁移步须独立可回滚）） |
| B 推断类 | 26 | B1 步骤链=非线性依赖图 / B2 状态提醒=宏写者序列的推进提示 / B3 一致性=多对象证据绑定 / B4 分步治理=spec 门禁的推广 / B5 认知防过载=状态压缩+主动微介入 / B6 硬规则=状态机+物证门+seq 记录 / B7 审计幻觉抑制=证据锚点化跨层校验 / B8 本仓多流=需聚合看板 / B9 自动刷新=事件/hook/轮询三路径 / **B10（v1.4）回溯语义=非时序回跳因果源+补偿式留痕+最小回改集** / **B11（v1.4）本仓回溯物理前提已全备，缺语义与收敛规则** / **B12（v1.4）计划变更版本化（防 HARKing 的工程形态）** / **B13（v1.5）"前步过期"三来源，v1.4 只覆盖内部证伪** / **B14（v1.5）仓外三层核验能力为零，却是唯一可完全机械化的一环** / **B15（v1.5）pivot 与 freeze 是同一概念的两个尺度** / **B16（v1.5）vN 轮次缺 kill criteria 即 renegotiation trap** / **B17（v1.6）B 层是"剥夺"非"过期"，无补偿动作（=外部先到达 pivot）** / **B18（v1.6）C 层噪声量级已固定 → 应降低单次判决的权重** / **B19（v1.6）零依赖半自动形态的最低充分三段式：人抓 → 工具记 → 三态差分** / **B20（v1.7）论文仓症状与本仓不变式逐条对偶（6 条：I-5/I-6↔派生物不入真值区 · I-1↔一份真值 · I-3↔名=身份版本=元数据 · I-7↔同名必须同义 · I-10↔证明制品单一归属 · I-8↔脚本分层）** / **B21（v1.7）"逆向拆解文档"的正确形态=blueprint（依赖与证明状态自动导出，人工文档只留 Explanation）** / **B22（v1.7）多版本发表/返修阶段语义应由标签承载而非文件名** / **B23（v1.8）用户现状=`Mono-as-Poly`（有 monorepo 形态无其机制）→ 不拆分、补机制** / **B24（v1.8）辅助资产归属"一次判定"表（PDF 移出/提取文本为派生物/codebook 升一等制品/笔记分离/个人内容物理隔离）** / **B25（v1.8）共享层正确形态="一份规范 + 一个索引 + 一个红线清单"而非"一个杂目录"** / **B26（v1.9）分步走依赖结构：S3（推理工作流）依赖 S1（契约层）、不依赖 S2（清理层）→ 广播清理应先单仓 pilot 实测 H12，再定一次性 vs 逐仓** |
| C 判断类 | 23 | C-1 同构成立 / C-2 分阶段吸收 / C-3 门禁判定（本期止于调研） / C-4 三新维度同构成立 / C-5 补充裁定（仍止于调研，零工具改动） / C-6 织界线修正（markdown 看板生成器方向，仍懒加载） / C-7 自动刷新可行（事件/hook/轮询，脱用户指令） / **C-8（v1.4）回溯可行且以既有机制承接（仍懒加载 gate）** / **C-9（v1.4）收敛控制判据登记（轮次上限 + 进展判据，仅纪律不落工具）** / **C-10（v1.5）环境轴优先级最高（唯一无机制覆盖的失效；三分类分流 + 触发式重检候选，仍懒加载）** / **C-11（v1.5）投稿前合规四检登记为纪律（引用核验优先触发工具化）** / **C-12（v1.5）freeze 与 kill criteria 必须预先写定，防 renegotiation trap** / **C-13（v1.6）B/C 两层为真盲区但优先级低于 A 层；零依赖半自动形态落地为「纪律 + 本地清单」** / **C-14（v1.6）抢先预警与止损耦合——形成「A-50 三分类 × B 层抢先预警 × A-59 kill criteria」判据链** / **C-15（v1.7）规范化分层落地（先立零工具零依赖契约层，再逐仓迁移）** / **C-16（v1.7）规范化价值在可机械检出（四条判据，其中 ①②④ 与 project-console 三件套同构可复用）** / **C-17（v1.7）blueprint 为性价比最高新增（仍懒加载，触发=做成可被第三方独立核查的制品）** / **C-18（v1.8）两项空白关闭，不需新方法论亦不需外部机制；与 C-15 合并为同一批"纪律 + 三文件"交付** / **C-19（v1.8）隐私隔离优先级最高（先划红线再谈规范；`data_policy.md` 为首件交付）** / **C-20（v1.8）辅助资产三层收敛（真值层/参考层/私域层；层间唯一连接是引用键而非文件复制）** / **C-21（v1.9）分步走可执行且与 C-15/C-19 同构（先立契约→再广播→后建工作流）；但广播≠统一重整，须逐仓 + 可机械检出** / **C-22（v1.9）"广播"=标准唯一 × 执行逐仓；首个广播对象应选最接近 compendium 的仓做 pilot 实测契约最小充分集，不跳过 H12/H13** / **C-23（v1.9）广播执行即 C-15 的"逐仓迁移"，两者触发一致（用户指定首个迁移仓 = pilot 选择）** |
| 假设区 | 16 | H1 步骤链是否需要 DAG 依赖映射 / H2 数学-实现上场时是否引入 Lean4 性价比未实测 / H3 本仓是否需要可视化/UI 展示层 / H4 链条上游依赖发现是否需要显式依赖元数据 / H5 看板生成时机（按需 vs 自动刷新）——v1.3 部分回答=三档自动强度（L0 门禁/L1 监听/L2 轮询）但各档开销未实测 / **H6（v1.4）回溯"影响集"（哪些前步须重做）如何确定：人工声明 vs 依赖图反向闭包（与 H1/H4 同源）未裁决** / **H7（v1.4）回溯轮次上限阈值未实测——MDPI「两轮大修」为期刊流程经验值，本仓 `vN` session 先例最多 v3，"几轮后应改判换方向"缺本地实证** / **H8（v1.5）环境轴重检的触发频率与成本未实测（LSR 为月度节奏，本仓无自动化）** / **H9（v1.5）仓外核验是否可引入外部数据源未裁决（Crossref/OpenAlex/Retraction Watch 违 D6；离线快照或"仅生成待核清单"的半自动形态是否足够未实测）** / **H10（v1.6）告警覆盖的召回率与延迟未实测（Scholar 索引滞后数天–数周；arXiv 分类告警对相邻领域是否有系统性漏报）** / **H11（v1.6）"重叠判定"的自动化边界未裁决（LLM 判"是否与我的缺口重叠"属 M7 关注的高幻觉点，与 A-54 同源；是否以"只做机械的关键词/分类差分、重叠判定全交人工"为上限）** / **H12（v1.7）规范化契约的"最小充分集"未实测（"一页契约 + 三模板"能否覆盖 7 仓全部差异，需真实迁移验证）** / **H13（v1.7）Lean 双源漂移中哪一份是真值未裁决（`LGMM 8.0/lean4/` 15 文件 vs `LGMM_Lean/LGMM/` 12 文件，文件集不一致；裁决前不得删除任一份）** / **H14（v1.8）`files.zip` ×10 与归档快照（`LGMM_0727.rar`/`MIDAS-Granger.rar`）的处置未裁决（留档 vs 冗余；**裁决前不得删除**）** / **H15（v1.8）363 个 PDF 的版本构成（VoR/AM/preprint）未实测（需 DOI 逐篇判定，多数仓无 git 无历史）→ 判定前默认按"不可再分发"保守处理** / **H16（v1.9）"广播"的推进粒度未裁决：单仓 pilot 验证后应"gap-fill 全量翻新"还是"strangler-fig 渐进替换 17 仓"——依赖 H12 实测结果，登记观察项** |

---

## 1. 调研目标

**核心问题**:
1. 学术推理写作工作流（调研→缺口→设想→模型→数据→初结果→草稿→模拟评审→反馈迭代）与本仓 Spec 驱动框架是否**同构**？同构点在哪？
2. LGMM 实证审计暴露的"数学-算法-数据-结果-论文表达一致性"问题，能否被本仓的"声明=重数 + 证据链 + 门禁"机制承接？
3. 社区开源案例中哪些是可直接借鉴构件，哪些需改造，哪些与本仓重叠应规避？
4. "每步改动自动产生下一步状态提醒"、"研究日志/路线/变更历史"的需求，社区如何实现，本仓的 spec_runner 事件流是否已覆盖？

## 2. 用户场景解剖（AGENT 即用户，LGMM 为锚点）

### 2.1 用户给出的九步学术推理写作链（A-1）

【A】A-1: 用户将学术推理写作分解为九步，每步间**连锁式影响**且需**频繁审查修改**、**控制版本**、保持**数学-算法-数据-结果-论文表达一致性**、每步改动**自动产生下一步状态提醒**，同时需记录**研究日志、路线、变更历史**：
> 调研 → 缺口分析 → 初步设想 → 模型方法构建 → 数据获取 → 初步结果 → 草稿撰写 → 模拟评审 → 反馈迭代

### 2.2 LGMM 证据链审计揭示的工程痛点实证（A-2 / A-3）

【A】A-2: **LGMM 8.0 证据链审计（2026-09-10）已定稿**，暴露实证管线的一致性断裂：论文数学（`eq:lgmm_obj` 横截面 GMM 因子溢价 λ̂ = (Ḡ'ŴḠ)⁻¹Ḡ'Ŵḡ，Σ_i 跨资产 + 工具变量 Z + HAC 权重）与主实证代码（`rolling_lgmm_*` 三副本，λ̂_jt = Σ_t w_t·r_jt / Σ_t w_t，**收益加权平均**）**估的不是同一个对象**。来源：[外部·证据链审计](file:///D:/Article/Working%20paper/LGMM/LGMM%208.0/docs/audit/2026-09-10-empirical-estimator-evidence-chain.md)
【A】A-3: **该断点的性质 = "类型差异"升级为"估计对象不同"**：设计文档 `<docs/spec/review_repair_m1_m8_design.md> §3.1 符号核对表与论文一致，但代码三副本未消费 `lgmm_core.lgmm_at_t0`（真正实现横截面矩条件的唯一版本）。数值铁证：探针 `lam[0,30]=0.004935` == Epanechnikov 加权平均==相等。→ **同一符号 λ̂ 在 论文/设计/代码 三层指代不同对象，恰是本仓最痛恨的"声明≠重数"。**

## 3. 社区开源案例调研

### 3.1 手稿版本控制与审稿反馈（SciTeX Writer / paper-template）（A-4）

【A】A-4: **SciTeX Writer** 提供模块化 LaTeX 手稿管理：`make archive`（时间戳+版本号归档）→ `make diff`（**latexdiff 高亮版本间改动**）→ revision 目录承载多轮审稿（subdirectories per round）。**paper-template**（GitHub Actions）每次 commit 自动编译 PDF + Pages 发布，解决"最新版本在哪"。→ 命中用户"控制版本 + 频繁审查修改"痛点，对应本仓 `git` + 版本化。

### 3.2 可执行论文 / 交互编程（Quarto / knitr / Jupyter）（A-5）

【A】A-5: **literate programming**（Knuth 1984）使"数据→代码→输出→手稿"单一来源：Quarto 成为主流，**改数据/代码自动重跑并传播到手稿**，消除"结果复制粘贴进论文"的断点。研究仅 8.5% 的 Jupyter 笔记可原样复现。→ **直接对应"数学-算法-数据-结果"一致性**：把结果内联到手稿，从根上防 A-3 式数字断章取义。

### 3.3 跨模型模拟评审 + 反馈迭代（ARIS / PaperJury / Agentic_Paper / AutoReviewLoop）（A-6/A-7/A-8）

【A】A-6: **ARIS（Auto research in sleep）核心 = 跨模型审稿**：Claude Code 执行，外部 LLM（Codex 等）评审，明确论证"单模型自审是 stochastic bandit（噪声可预测）→ adversarial bandit（审稿者探测执行者盲区）更难被 game"；两模型逼近 Nash 均衡是打破自我博弈的最小配置。持 `REVIEW_STATE.json`（round/status/score）+ `AUTO_REVIEW.md`（累计变化日志）。→ **与本仓 RULE-5 异基座第二会话高度同构**，且给出"2 个审稿者为何最优"的论据。
【A】A-7: **PaperJury**：CONF-venue 三模式（direct-edit / **review 对抗式法庭** / auto），review 引擎 = N 域 reviewer → contestability routing → 双向庭审 → 三方判决 → **clerk-converged 多轮循环**，**共识门控 + 作者签字**，issue 记入 **durable ledger**。auto 模式：drift-bounded 安全修复 + 风险项排队待人工。
【A】A-8: **Agentic_Paper**：12 个并行 reviewer agent（Methodology/Results/Citation Validator/Statcheck 等）+ 协调器综合裁决。arXiv 2511.10902：RQ-OpenReview 审稿模拟 + **Action:Objective[#] 可执行 to-do** 列表。→ 命中"模拟评审+反馈迭代"，比本仓现有人工异基座 pass 更结构化。

### 3.4 电子实验记录本 ELN（eLabFTW / OSF）（A-9）

【A】A-9: **eLabFTW**：审计防篡改（**数据不可删、改动带时间戳留痕**）+ 版本历史 + 锁定归档 + FAIR 元数据；解决"记录断档/文件分散/版本失控"三丢。OSF 提供预注册+项目全生命周期管理。→ 对应本仓 M7 证据账本（append-only）+ 事件流。

### 3.5 全生命周期阶段化研究（auto-research 8 phases / 4 gates）（A-10）

【A】A-10: **auto-research**（Claude Code 插件）：研究全生命周期 **8 phases / 4 user gates** 自动工作流（survey→idea→实验→draft），`LAB_NOTEBOOK.md` 作**单一 living document 时序"思考航海日志"**。→ 与本仓 SPEC_PROCESS 十步阶段化 + per-feature session + step-gate 高度同构。

### 3.6 数学-实现一致性：形式化验证（Lean4 / Coq）（A-11）

【A】A-11: 形式化验证（Lean4 Mathlib / Coq, LF-lean 类型同构验证 / Lean Workbook 57K 题）把"数学结论成立"变成**机器可校验**。但桥接成本高（数学被形式化 → 手动翻译易错 → 需求类型同构）。→ 对应本仓"数学表达一致性"痛点：Lean4 是**终极但最重**的解法；对本仓 M7（文档断言）+ A-3 式"实现对象"抽查而言，**替代方案 = 符号核对表 + 探针断言**（LGMM 已用数值探针）。

### 3.7 版本化文献（Zotero + Better BibTeX + Git 锚定）（A-12）

【A】A-12: Zotero+LaTeX+Git 模板用 **Git Submodule + 触发式导出 + git notes 元数据锚定**解耦 BBT 导出与 GUI，构建确定性文献版本控制。→ 命中"引用一致性"。

## 4. 同构性分析：学术写作链 ↔ 本仓 Spec 框架

### 4.1 九步链的本质 = 非线性依赖图，非线性流水线（B1）

【B】B1（见附录 B）: 用户"九步连锁影响"表明**上游改动向右游传播、下游发现反噬上游**——这是**依赖图**而非线性管道。本仓 SPEC_PROCESS 十步 + step-gate 的 STEP_SEQUENCE 是线性骨架，但**事件流（append-only + seq 单调）天然支持 fork/replay**。社区（auto-research 8 phases / PaperJury 多轮）也把链当作**可循环**而非一次性。→ 同构成立点为"**分步 + 门禁 + 可回溯**"。

### 4.2 "每步改动自动产生下一步状态提醒" = 推进提示（B2）

【B】B2（见附录 B）: 社区实现 = spec_runner 事件流 append-only 后，由**读取方**消费 seq 判定推进；auto-research 用 8 phases 明确 next gate；ARIS 用 REVIEW_STATE.json。本仓 spec_runner 已落 append-only + seq + replay/fork，**"自动提醒"= 一个读取 seq 并打印"下一步该做 Gate N"的轻壳**，机制零新增。→ **最大同构点：不欠账**。

### 4.3 "数学-算法-数据-结果-论文一致性" = 多对象证据绑定（B3）

【B】B3（见附录 B）: A-3 断点的根治 = 让 **λ̂ 在论文/设计/代码/结果四层绑定到同一对象标识**。社区三条路：(a) literate（Quarto 内联结果，A-5）；(b) Lean4 形式化（A-11）；(c) 符号核对表 + 数值探针（LGMM 已用）。→ 本仓对应 = "声明=重数" + verify-anchor + M7 证据分级 E1（可重放命令）。**LGMM 缺的是把这条绑定做成例行 guard**（审记建议"固化为例行 guard，M-12 引述"）。

### 4.4 分步治理 = spec 门禁的推广（B4）

【B】B4（见附录 B）: "模拟评审→反馈迭代" 社区用跨模型/multi-arm（A-6/7/8）；本仓用 RULE-5 异基座独立 pass。**两者同旨**：把"作者自评"替换为"独立评审者"。ARIS 的"两模型即最优"论据直接支持本仓 RULE-5。

### 4.5 LGMM 仓库已有机制盘点（A-13）

【A】A-13: LGMM 8.0 已在实践（非本仓）：`docs/spec/`（engineering_constraints_* 四份：research/design/implementation/checklist —— 直接对标本仓四件套）、`docs/audit/`（含 2026-09-10 证据链）、`memory/`、`roadmap/`、`lean4/`、`data_lineage_v8.1.md`、`MAPPING_v8.2.md`、`review_repair_m1_m8_*` 族、`SPEC_DRIVEN_DEVELOPMENT.md`。→ **用户已在用 spec-driven + 审计 + lineage + lean4 的组合，本仓框架是这套的自举/增强，非全新引入。**

### 4.6 本仓既有同构机制盘点（A-14）

【A】A-14: 本仓已具备承接学术写作链的全部机制：SPEC_PROCESS 十步 + spec_runner 事件流（append-only/seq/replay/fork）+ step-gate 三类规则 + verify-anchor 锚点核查 + **FWK-DECISION-RECORD 八字段**（决策记录）+ **M7 证据账本**（反幻觉 + 分级 E1-E5）+ RULE-5 异基座独立 pass + 三校验器（dc_validator/m7_stats/repo_stats）」+ PROGRESS（进度/路线）+ CODE_WIKI（变更历史/索引）。**研究日志=事件流，路线=PROGRESS/roadmap，变更历史=git+CODE_WIKI。**

## 5. 收敛裁定

【C】C-1（见附录 C）: **同构成立**。学术推理写作工作流与本仓 Spec 驱动框架共享同一组不变量：分步阶段化、每步一个决策/产物、门禁审查、证据绑定、可回溯、声明=重数。用户九步链 ↔ SPEC_PROCESS 十步；模拟评审↔异基座独立 pass；一致性↔视重数+证据链；状态提醒↔事件流 seq。**特色项（数学-实现一致性）是本仓的 feature 级应用，不改变框架同构性。**

【C】C-2（见附录 C）: **分阶段吸收该概念**（Layer-0 概念登记 + 分步采纳）：
- **立即候选（零新依赖）**：把"同符号跨层指代不同对象"的检查固化为**例行 guard**（对应 LGMM M-12/M-08）——符号核对表 + 数值探针断言，挂到本仓 step-gate/校验器同族。
- **候选（懒加载）**：literate 结果内联（Quarto）若在 LGMM 采用则与本仓 verify-anchor 重叠定位需对齐；跨模型模拟评审（含 ARIS "2 模型最优"论据）若在 LLM 端落地则复用 RULE-5。
- **否决/重（代价）项**：Lean4 全量形式化（A-11）在字数/工作量上不划算（本仓/实证文档层，非定理级），仅当"数学断言需机器级确证"时按用例进 ADR-0010 三问。

【C】C-3（见附录 C）: **本期止于调研（懒加载 gate）**，不实施工具改动。理由：Q1 属 Layer-0 概念登记 + 通过本仓既有机制承接，不新增 layer-1 组件；Q2 无明确激活触发（LGMM 一致性 guard 属外部仓库，非本仓 feature）；Q3 零工具副作用。**不重复造轮子**，不引入社区框架本体（SciTeX/Quarto/eLabFTW 均为外部重型平台，与本仓单写者+文档层的轻量定位冲突）。

【C】C-4（见附录 C，v1.1）: **三新维度同构成立**：① **UI/认知防过载**（§7）→ 本仓 doc-first + 每 feature 事件流独立（**v1.2 修正**：实为 per-feature **多流并存**非单流，过载真实存在；见 §10.1/C-6）；缓解=吸收"状态压缩 / 主动微介入 / 嗅探线索"为聚合**看板**展示原则，无需引入重型 UI 框架。② **AI 工作流审计/决策链追溯/幻觉抑制**（§8）→ = 本仓 M7（断言分级 E1-E5，同 COCO 集成分歧/AWorld 双角色/ACM 形式护栏同旨）+ RULE-5（异基座独立臂）+ decision 八字段（决策链，同 PROV）+ verify-anchor（证据锚点）；LGMM 证据链审计即其实证。③ **链条连锁反应硬规则**（§9）→ = 本仓 spec step-gate **状态机**（steps=状态 / gate=转移守卫 / seq=状态历史），与 AgentGuardian CFG / ACM security automaton / PROV-CONSTRAINTS 同一手法。
【C】C-5（见附录 C，v1.1）: **补充裁定——仍止于调研（懒加载 gate 保持，零工具改动）**：① 认知防过载 UI = **Layer-0 概念登记**（Racc 四原则 + AutoGPT 三级粒度）；**v1.2 修正**——本仓实为多流并存故过载真实，正确缓解 = markdown 看板生成器（§10/C-6），**不引入** AgentGUI/LangSmith/Langfuse 重型平台本体（仍成立）。② 幻觉抑制 = **复用既有**（RULE-5 + M7 + verify-anchor + C-2 已承诺的"同符号跨层对象绑定"例行 guard），不新增；③ 链条硬规则 = 明确"**状态机表达 + 每转移物证门 + seq 状态记录**"，无需新引擎。新样本零新增。
【C】C-6（见附录 C，v1.2）: **织界线修正——本仓认知过载真实，缓解形态 = markdown-native 只读看板生成器 + git worktree/log graph，仍懒加载**：per-feature 事件流独立 ≠ 单写者单流（每 feature 一条 + fork 派生 = **多流并存**），叠加 AI 长输出 + 频繁外部反馈 → 认知过载/漂移真实。最小治愈 = 一个 stdlib 只读 Board 生成器：扫描 PROGRESS.md（Task Ledger）+ spec/*/ 四文档 + sessions/ 事件流 verdict（Progress Ledger）→ 压缩每 feature 为**单行认知块**（pid+状态+下一步+阻塞），按 3 状态分组（进行中/待你审/阻塞），暴露"需要你/下一步"= 外部信息注入 + 主动微介入入口；fork 派生用 **git worktree + `git log --graph`** 原生表达（零新增）。**零 GUI 服务器、零新依赖、AI 可写 markdown**。按 ADR-0010 仍**止于调研（懒加载 gate）**：零代码改动，仅登记概念，触发条件 = 用户明确要求落地 board 生成器（见 §10.6/H5）。
【C】C-7（见附录 C，v1.3）: **看板可自动（事件/hook/轮询三路径），完全脱依赖用户指令**：① **自动抓取** = 事件驱动——源头文件（PROGRESS / `.jsonl` 事件流 / spec 四文档）一改即触发重新生成，无需手敲命令；② **自动状态更新** = 门禁钩子——并进本仓既有 pre-commit 四 hook / step-gate / repo_stats 机械对账，**提交即刷板**（"声明=重数"外推到看板自身，防 drift）；③ **实时反馈** = 终端轮询渲染（纯 stdlib `watch -n`+终帧重绘即可，无需 rich/tqdm/Textual 重依赖）或常驻 FileSystemWatcher。**三档自动强度**：L0 门禁触发（最弱，提交时刷）/ L1 文件监听（源头改动即刷，`watch-inbox.ps1` FileSystemWatcher 现成）/ L2 终端轮询（常驻实时刷新，agent_pulse 500ms 模式）。仍懒加载 gate，触发=用户要求落地。

## 7. 补充调研一：UI 实时反馈与认知防过载（Q1，v1.1）

### 7.1 AgentGUI：观察 + 转向长时 agent（A-15）

【A】A-15: **AgentGUI**（ETH Zürich，[arXiv:2607.26300](https://arxiv.org/abs/2607.26300)，本地开源 GUI）：统一展示多个并发长时 agent 的轨迹可视化，支持手动+自动**转向（steering）**、与开源/前沿框架集成。受控用户研究=从混乱 trace 定位关键要素**提速 38%（p=0.023）**；自动"漂移预防"特性使本地小模型任务完成率跨 0.8B–9B 阶梯**最多 +34pp**（每模型 N=50 次）。→ 命中"实时反馈 + 防漂移"双目标，且给出"agent 越弱、越需防漂移"的实证。

### 7.2 认知负荷的心理物理实证（A-16）

【A】A-16: 三条跨学科实证锚定"防认知过载"设计边界：① **Cowan ~4±1 chunk**——工作记忆真实容量（Miller 7±2 高估）；② Sophie Leroy **attention residue**——任务间切换残留占用认知，切换性能下降 **40–60%** 直到 15–30 分钟才消退；③ Norman Mackworth **vigilance decrement**——被动持续监视 15–20 分钟内显著衰退，且**自动化监视比手操更严重**；Pop et al. 2012：叠加次级交互小任务可**抵消**该衰退（主动微介入保全注意力）。

### 7.3 并行监督的容量上限与失效退化（A-17；v1.12 据实换源）

【A】A-17: 人的**并行监督容量有限**，超出容量后监督失效或退化；且长期使用 AI 系统本身会削弱监督所需的认知能力——构成"**多流并行才爆**"的过载机理。三条可核验一手来源（v1.12 二次核验换源）：

① **AI Agents Push Humans Out of the Loop**（Mitchell / Ghosh / Passi，[arXiv:2608.23642](https://arxiv.org/abs/2608.23642)，2026）逐字："Not only do current approaches to AI agent design impede effective human oversight, but the cognitive capacities required for it are also themselves degraded by extended use of AI systems."
② **Operating Imperfect AI: Reliability Drift and Human Congestion**（Wang & Rachev，[arXiv:2601.22295](https://arxiv.org/abs/2601.22295)，2026）逐字："human override capacity is scarce and congestible … we identify a critical 'Capacity Phase Transition' … beyond which no policy can maintain safety standards without causing structural system failure (infinite queues)."
③ **The Oversight Game**（Overman & Bayati，Stanford，[arXiv:2510.26752](https://arxiv.org/abs/2510.26752)，2025）逐字："passive loss of control … can arise … [from] the agent's decisions becoming too complex or numerous for humans to reliably oversee."

→ 启示：**长链（单流线性）不触发过载，多流并行才爆**——本仓单写者单流恰好避开。

> **v1.12 二次核验（据实换源，形态 III 处置）**：v1.1–v1.11 本条原引《The Agentic AI Oversight Problem》（署名"微软 / UC Berkeley / 清华"，含 **POMDP** 模型、注意容量 **C≈3–5 流**、监督准确率 **1 / 5 / 20 agent = 92% / 62% / 17%**、响应由 <10s 升至 >2min、NASA-TLX 主观负荷）——**该文献未获任何一手来源**：arXiv 官方 API 精确短语检索 `all:"Agentic AI Oversight Problem"` 返回 **totalResults = 0**；无 arXiv 编号、无 MSR 官方出版物页、无会议页、无 Semantic Scholar 或 DBLP 条目；两条具名细节均可证伪（所谓通讯作者 **Sarah Sterman 实为 UIUC HCI 研究者**，方向为 AI 写作工具；"**AI brain fry**" 的真实出处指向 BCG × UC Riverside 研究，与该"论文"无关联）；**唯一来源为论坛帖**（forum.gnoppix.org，疑 AI 生成、无任何文献链接）。判定 = **疑似虚构引文（形态 III）**，故**原引具体数字（92% / 62% / 17% 与 C≈3–5）一律撤回**；命题改由 ①②③ 三条可核验来源承载。**断言编号 A-17 与命题方向保留 → 计数不变**，全文既有引用（§10.1 B8 引、附录 B 的 B5/B8 `basis`）继续有效。检索式、入口清单与两条证伪的完整记录见 **§18**。

### 7.4 Racc 认知设计原则：状态压缩 + 嗅探线索 + 主动微介入（A-18）

【A】A-18: **Racc**（多 agent IDE）把上述研究合成可落地原则：每会话压缩为**单个认知块**（状态色+任务+进度+耗时）；按 3 类状态（正常/待审/阻塞）**分组削减 chunk 数**；用**信息嗅探线索**（错误计数 / stuck 徽章 / 距上次进展时长 / 微摘要）引导"信息觅食"；agent 周期性请求**轻量人工输入**维持主动监督。→ 设计体检：始终护住"工作记忆 ≤4 chunk + 主动微介入 + 线索"。

### 7.5 既有 LLM observability 平台（A-19）

【A】A-19: LangSmith / Langfuse / Arize Phoenix / MLflow 均以 **span trace 树 + agent 图可视化 + 逐轮 replay + 版本化评测**为基座（OpenTelemetry/OpenInference 统一 ingest）；核心洞察="**trace 是新的 log**"——单 LLM call 不是 agent，失败在 call **之间**（工具选择/重试/子 agent/未退出的环）。→ 这些是重型平台（SaaS 或 ClickHouse self-host），与本仓"单写者 + 纯文档 + 零依赖"定位冲突，纳入 C-5 懒加载排除。

### 7.6 AutoGPT 三级事件粒度 + DAG 布局（A-20）

【A】A-20: AutoGPT 实时进度可视化落点=**事件驱动 + 三级粒度**：L1 用户级（主干任务）/ L2 开发级（工具调用+状态变更）/ L3 调试级（LLM 输入输出），按角色切层**防信息过载**；用 **Dagre 有向无环图布局**排依赖，颜色编码（绿完成/蓝进行/红失败重试/灰跳过）。→ **粒度分层 = 多流混合时的"救生筏"**；本仓单流场景只需 L1。

## 8. 补充调研二：AI 工作流审计·决策链追溯·幻觉抑制·微工作流嵌套（Q2，v1.1）

### 8.1 错误级联与连续监督：COCO（A-21）

【A】A-21: **COCO**（BUPT，[arXiv:2508.13815](https://arxiv.org/abs/2508.13815)）用多点连续监督阻断多 agent **错误级联**（下游放大上游幻觉——正是本仓 A-3 LGMM 断点的泛化）：**Contextual Rollback**（按执行历史回滚，非盲目重试）、**Bidirectional Reflection Protocol**（防振荡控制环）、**Heterogeneous Cross-Validation**（用**集成分歧**识别偏差/幻觉——与本仓 RULE-5 异基座同构）；30× 参数削减仍达大模型性能 **95.1%**，平均提升 6.5%。

### 8.2 执行 + 守卫双角色防幻觉：AWorld（A-22）

【A】A-22: **AWorld**（[arXiv:2508.09889](https://arxiv.org/abs/2508.09889)，GAIA 开源第一）：Execution Agent 由 **Guard Agent** 运行时"动态驾驶"监管，用 **System Identification** 离线建档执行者固有弱点（性能指纹）→ Guard **profile-aware** 定向纠错；严格防幻觉护栏 = **明令禁止编造数据、关键信息缺失必须输出"cannot solve"终止**（拒答优于臆造）。→ 对应本仓 M7 断言分级 + 拒绝表演性自信。

### 8.3 形式化护栏：AgentGuardian 控制流图 + ACM 形式证明（A-23）

【A】A-23: 两条形式化硬护栏：① **AgentGuardian**（BGU，[arXiv:2601.10440](https://arxiv.org/abs/2601.10440)）从执行日志**学习控制流图 CFG**（合法工具的合法序列）+ 输入正则约束，运行时访问控制，实测**缓解幻觉驱动错误与编排级故障**；② ACM《Guardians of the Agents》（Erik Meijer，2025）：要求 agent 在授权执行前**生成安全性的形式证明**，把安全不变量表达为 **security automaton**（约束执行全程成立）——evals 只能证有不能证无，形式证明给出确定性保证。→ 与本仓"证据链 + 门禁先于放行"同旨。

### 8.4 决策链追溯标准：W3C PROV（A-24）

【A】A-24: **W3C PROV 家族**（PROV-DM/O/N/XML + **PROV-CONSTRAINTS**）是"决策/数据链可追溯"的互操作标准：Entity/Activity/Agent 三要素 + wasGeneratedBy/usedBy/wasAttributedTo/derivedFrom 关系；**PROV-CONSTRAINTS** 形式化**时序与因果约束**（编辑不能先于文档存在、因果不能反向），防止溯源记录自相矛盾。→ 本仓事件流（append-only）+ seq 即 PROV 的纯文档层实例。

### 8.5 可审计 AI 谱系：trace 质量决定归因（A-25）

【A】A-25: awesome-auditable-ai（201 条目）实证**可审计性取决于记录质量**：**TraceElephant**（ACL'26）显示完整执行 trace 把 step 级归因准确率 **17%→30%**（相对 +76%）；Who&When（ICML'25）最强归因法定位责任 agent **53.5%**、决定性错误步 **14.2%**；AgentAuditor（NeurIPS'25）、SpecBench（reward hacking 测量）量化"能力增长快于可靠性增长"。→ 直接支持本仓"每步恰一条决策 + 证据锚点 + status seq"的价值。

### 8.6 幻觉抑制的生成侧：grounding + 自验证引用（A-26）

【A】A-26: 幻觉抑制分三层：① **检索-grounding**（RAG 用 DPR/ColBERT 检索证据锚定生成；本仓 research-lookup 即此）；② **自验证-引用**（**VeriFact-CoT** [arXiv:2509.05741]：事实核验→反思→引用整合多级；多模态事实核验框架 [arXiv:2510.22751] 跨结构化库+网络+学术文献交叉核对，幻觉 **-67%**、领域专家 89% 满意）；③ **训练无关检测器集成**（token 熵 + 自一致性 + 证据覆盖 + 零样本 NLI 蕴含/矛盾）。→ 文本框引用锚定 = 本仓 M7 锚点的学术写作等价物。

### 8.7 每步内嵌微工作流 = 层级状态机/子网（A-27）

【A】A-27: 社区把"每步含微工作流"建为**层级形式结构**：① **HAACS**（[arXiv:2505.00018](https://arxiv.org/abs/2505.00018)）用**层级 Petri 网**形式化 agent 协作——MIMO 转移、子网并发执行、冲突消解，step=可再分的子网；② **NVIDIA Deep Researcher / artificial-agent-lab**：owner/orchestrator → planner/researcher/PI → PhD 逐层委派，每层一个 loop；③ **LangGraph StateGraph**：节点+边+state reducer+checkpointer+human-in-the-loop interrupt——**状态机作为图引擎硬骨架**。→ 与本仓 P-039 P-b 裁定呼应：层级用于探讨口，本仓 flat-feature 结构不引入内层 agent 递归（复利误差）。

## 9. 补充调研三：链条连锁反应硬规则（图/状态机）（Q3，v1.1）

### 9.1 诉求与本质

用户要求把"写作链条的连锁式影响"固化为**硬规则**（图结构/状态机/类 模式）而非口头纪律——每一步改动引发的上游/下游连锁修改必须**被机器强制、可追溯**（A-1 的"连锁式影响 + 频繁审查修改"）。

### 9.2 本仓已是状态机（B6 引）

【B】B6（见附录 B）: 本仓 spec 流程**本质上就是一个确定性状态机**：STEP_SEQUENCE=状态集，step-gate（schema 硬性-1 / evidence 非空 / 同符号核对）=状态转移守卫，事件流 seq=状态历史（append-only）。"连锁反应硬规则"落点=**每步产物标注"被下游消费的对象"**（B3 的跨层绑定）+ 转移合法性由 gate 机械裁决。→ 与 AgentGuardian CFG / ACM security automaton / PROV-CONSTRAINTS 同一手法，**无需新引擎**。

### 9.3 硬规则形态选型：状态机 vs 全量 DAG 依赖图

社区形态折中：**状态机（合法转移集）**比 **全量 DAG 依赖图**更贴合"门禁编排"——状态机声明哪些转移合法、谁必须被 gate；DAG 声明全部祖先。前者贪心、可叠加、逐点裁决，与本仓 gate 逐步骤机制一致；后者需显式依赖发现成本（→ H4）。

### 9.4 与既有裁定收敛

上述映射已并入 §5 C-4/C-5；三条红线（机械物证门先于语义门、seq 单调记录、跨层同符号绑定）与 P-039 P-c 的三条红线同族。

## 10. 补充调研四：任务看板与自动化追踪——本仓认知过载的真实落点（v1.2）

### 10.1 前提修正：per-feature 多流并存 = 真实过载（B8 引）

【B】B8（见附录 B）: 先前 C-4/C-5 以"doc-first + 每 feature 事件流独立 = 单写者单流，天然免征 attention residue/vigilance decrement"为据排除一切 UI 层——该前提被用户场景证伪：**per-feature 事件流独立恰恰意味着多流并存**（每 feature 一条独立流 + fork 派生支线），叠加 AI 输出冗长需逐条反馈 + 频繁外部信息注入 → 本仓认知过载/漂移**真实存在**（A-16/A-17 的过载机理直接适用）。故正确姿态不是"免征"也不是"引入重型 GUI 平台"，而是**在既有事件流之上加一层轻量聚合视图**（§10.5）。

### 10.2 Task Ledger / Progress Ledger 二账本：想做的事 vs 实际进度（A-28）

【A】A-28: **Magentic-One**（Microsoft，[arXiv:2411.04468](https://arxiv.org/abs/2411.04468)）确立二账本模式：**Task Ledger**（given facts / facts to look up / educated guesses / step-by-step plan = 想做的事）vs **Progress Ledger**（per-tick **五问判题**：is_request_satisfied / is_in_loop / is_progress_being_made / who_to_speak_to / what_to_say = 实际进度），**"账本即人工审查面"**；stall counter 把"继续或重规划"从判断转成**确定性门**（≤2 即 re-plan）。→ 本仓天然对应：**Task Ledger≈PROGRESS.md（待办/路线）+ spec 四文档（计划）**；**Progress Ledger≈事件流**（event:decision + step-gate verdict exit 0/1/2 = per-step 判题）——**二账本分离已在隐式存在，缺的是显式聚合读取**。

### 10.3 Markdown-native 任务看板：AI 可写 + 零后端（A-29 / A-30）

【A】A-29: **Backlog.md**（npm，AI-ready）：每个任务=仓库里一个普通 `.md` 任务文件（frontmatter+验收标准+DoD+milestone/deps），`backlog board` 终端看板 + `backlog board export` markdown 报告 + `backlog browser` 本地 web；**三审查检查点 = 审 spec → 审 plan → 审 code**，一任务 = 一上下文窗口 = 一 PR；核心动机="瓶颈不再是写代码，是你的注意力——AI 一小时产出比人类一天能读的还多，但你可以先读一屏任务规格+验收标准再让代码写一行"。→ 与本仓 **doc-first + one-feature-one-context** 高度同构，且全部输出 markdown（AI 与人两可读）。
【A】A-30: **Markdown Task Board**（ad-halfspace）：纯 **Python 标准库** web server（仅绑 127.0.0.1）+ 单 HTML，list/kanban 双视图、按状态/优先级/领域分组、**依赖自动阻塞**；**Kanban.md**（VSCode 扩展）把 `.kanban.md` 渲染成可交互板；**Nullboard** = 单个 HTML 文件零配置。→ 印证"**看板可零第三方依赖 + markdown 作单一事实源**"，与本仓 stdlib 约束兼容。

### 10.4 fork 支线探索：git worktree + log graph（A-31）

【A】A-31: **git worktree**（Git≥2.5）= 一仓多工作目录、共享历史、按分支隔离——是"主线开发中 fork 支线探索"的**原生载体**（OpenAI Codex 每线程自动建 worktree；spaarke 并行 Claude 会话 3-5 个 worktree + 顺序 merge 防冲突；冲突检测可早提示）；`git log --oneline --graph --decorate --all` **原生可视化分支 DAG**（`*` 提交 / `|/` 合并线）。→ 本仓"主线 + fork 支线"= **git branch/worktree + 事件流 fork/replay**，零新增工具，板只需标注分支派生与"diverge/merge 回主线"状态。

### 10.5 最小落地方案：只读看板生成器 + git 可视化（B8 落点）

综合 A-28~A-31，本仓"自动化追踪 / 任务看板"的最小形态 = **一个 stdlib 只读 Board 生成器**（可作 spec_runner `board` 子命令或独立脚本）：

- **输入**（全部既有，零新状态）：
  - `docs/PROGRESS.md`（Task Ledger：P-id + 状态词表 pending/in-progress/blocked/done + 验收标准）
  - `spec/*/` 四文档（feature 计划呈现）
  - `tools/spec_runner/sessions/*.jsonl` 事件流（Progress Ledger：event:decision + step-gate verdict exit 0/1/2）
  - `git log --graph`（fork/分支派生）
- **输出**：终端看板 + `docs/BOARD.md`（可提交、AI/人两可读）。每 **feature = 单行认知块**：`pid | 状态(色) | 当前 step/Next | 阻塞标记 | fork 派生标记`；按 **3 状态分组**（▶进行中 / ⚠待你审 / ✖阻塞）；顶部独立 "**需要你 / NEXT**" 队列 = 外部信息注入 + step-gate exit 2(soft)/blocked 的汇聚点（主动微介入入口）。
- **满足 Racc 认知设计四原则**（A-18）：单认知块（一行一 feature）、状态分组（3 桶）、嗅探线索（阻塞徽章/距离上次进展/色）、主动微介入（NEXT 队列）；对应用户三大痛点：长输出→压缩为一行；外部注入+反馈→NEXT 队列；fork 支线→git graph 标注。
- **零新增依赖**：纯 stdlib 读文件 + 重新排列 + 写 markdown/stdout；**无 GUI 服务器、无 watch 常驻进程**（按需生成；H5 挂自动 watch 之需未实测）。

### 10.6 收敛与触发条件（C-6 引）

- 结论 = C-6（§5）：改编织界线，给出方向，**仍止于调研（懒加载 gate）**——零代码改动，仅登记概念设计与社区案例。
- **触发条件（Q2）**：用户明确要求落地 board 生成器（或指定首用例），此时按 ADR-0010 走实施小流程。
- 与 P-039 P-c 的关联：看板 = 主控站"任务卡 + 状态聚合"的本地单机版（无集群）；与 PROGRESS/CODE_WIKI 视图层一致性由 repo_stats 机械对账（声明=重数外推）天然兜底。

## 11. 补充分析：看板能否不依赖用户指令自动实时更新（v1.3）

### 11.1 结论先行（B9 引）

【B】B9（见附录 B）: **能**。看板的"自动抓取 / 自动状态更新 / 实时反馈"是标准的一类**派生产物自动重生成**问题，社区已有三条成熟且与零依赖兼容的触发路径，本仓无需任何第三方依赖即可全部具备。看板 = "只读视图"，其唯一职责是从既有真值源（PROGRESS/事件流/spec 四文档/git）**被动重算**——因此**不存在"需用户主动唤醒"的固有理由**，只需选一个自动触发时机（B9/C-7：L0/L1/L2）。

### 11.2 路径一：事件驱动自动抓取（A-32）

【A】A-32: 文件变化→自动处理 = **FileSystemWatcher** 的标准用途（.NET 内置，Windows 本机零新依赖，NotifyFilter=FileName/LastWrite/DirectoryName，IncludeSubdirectories，事件 Created/Changed/Deleted/Renamed 触发 Action）；`watch-inbox.ps1` 完整实作"文件落盘→自动归纳→写每日笔记"模式。→ 本仓 = watch `docs/PROGRESS.md` + `spec/*/` + `tools/spec_runner/sessions/*.jsonl` 任何 one 变化即重跑板生成器，**源头改动即自动刷新**，无需任何用户指令。

### 11.3 路径二：门禁钩子自动重生成（A-33）

【A】A-33: **do-knowledge-studio** `update-docs.mjs`：静态分析 + 模板驱动 API-GIT 钩子/CI 自动更新文档"生成节"（`<!-- AUTO-START -->`/`<!-- AUTO-END -->` 栅栏，只改写生成区，保留人工内容；pre-commit + GitHub Actions），**零外部 LLM、确定性、~1-2s**；**ProjectOdyssey** 把 test-count badge 做成 pre-commit 自动计数防 drift。→ 本仓已有 pre-commit 四 hook + repo_stats 机械对账 + step-gate，**把板生成器并进同一 pre-commit/step-gate 即"提交即刷板"**，且 repo_stats 对账天然保证"看板声明 = 真值"（声明=重数外推）。

### 11.4 路径三：终端实时轮询渲染（A-34）

【A】A-34: **agent_pulse / cc-aio-mon**（Claude Code 终端监视器）：轮询 temp 目录 snapshots（约 500ms 刷新）→ 全屏 TUI progress bar/指标渲染，**非阻塞、不依赖用户指令**；**Rich Live** 自带 `refresh_per_second` 定时自动刷新 + 可 `screen=True` 切换备屏；**minimal-tui** 强调"rich+tqdm 主、stdlib 兜底"。→ 本仓最小形态 = 纯 stdlib：`watch -n 5 board_cmd`（每隔 5s 重渲染终帧）+ 可选的 Wi-Fi 行内状态条，**无需引入 rich/tqdm/Textual 重依赖**（与零依赖 D6 一致）。

### 11.5 三档自动强度与裁定（C-7 落地）

| 档 | 触发 | 实时性 | 依赖 | 本仓现状 |
|----|------|--------|------|---------|
| L0 | pre-commit/step-gate 门禁 | 提交时刻 | 零（既有 hook）| ✅ 已有四 hook + repo_stats |
| L1 | FileSystemWatcher 监听源头 | 次秒-秒级 | 零（.NET 内置）| 可选 |
| L2 | 终端轮询 `watch -n` 渲染 | 秒级常驻 | 零（stdlib）| 可选 |

- **L0 已零成本可办**（并进既有 hook）；**L1/L2 为增量可选档**，开销 H5 未实测（但均为 stdlib + 轻轮询，成本低）。
- 综合 = **C-7**（§5）：看板可由事件/hook 自动更新 + 可选终端轮询展示，**完全脱依赖用户指令**；仍懒加载 gate，触发=用户要求落地 board 生成器。
- **归属转移（2026-09-11，P-042 剥离）**: C-7 触发的落地物已由 [project-console](../project-console/RESEARCH.md) 承接——可视化层归**通用底座**独立 feature，P-041 [board-generator](../board-generator/DESIGN.md) 记为其**前身（L0 首落点）**；本节自此降格为**来源指针**（只记录 C-6/C-7 概念来源），不再拥有看板能力的归属。

## 12. 补充调研五：回溯与反馈回路——"后步证伪前步"的工程化（v1.4）

### 12.1 诉求与本质：线性 STEP_SEQUENCE 之外

**用户指出的三类回溯**（本轮调研起点）：

1. **模拟评审的意见可能需要对多个步骤进行调整**——评审发生在链**末端**（草稿之后），但其意见常要求改数据、改模型、改论证；
2. **数据获取有困难可能需要再次启动调研**——第 5 步受阻，**回退到第 1 步**；
3. **结果不理想可能需要重新进行缺口分析**——第 6 步的产出**证伪了第 2 步**的缺口判断。

**本质**：九步链在本仓的机械骨架是 `step-gate`（**正向五步各恰一条 + seq 单调**），而真实研究是**非线性依赖图上的逆向传播**——下游的失败信号必须能**往回跳**，且跳的落点不是"前一步"而是**真正被证伪的那一步**。这与 B1（§4.1「非线性依赖图而非线性管道」）同源，但 **B1 只指出"可回溯"，未规定回溯的语义**；本轮补足。

社区把这个问题分四层解决：**补偿**（怎么撤销）、**留痕**（怎么不篡改历史）、**回跳**（跳到哪）、**重算**（重做什么）。

### 12.2 通用工程模式（四层）

【A】A-35: **Saga 模式 = 长事务的补偿式回滚**：把长事务拆为一串**本地事务（local transaction）**，每个配一个**补偿事务（compensating transaction）**；任一步失败则**逆序执行**已成功步骤的补偿（Azure 架构中心 / Temporal / Cloudflare Workflows 均已产品化，Cloudflare 更进一步支持**在步骤旁声明式地定义补偿逻辑**）。三个关键概念：① **可补偿事务**（可撤销）；② **pivot transaction = 不可回退点**——过了 pivot，补偿不再适用，后续只能**重试至成功**；③ **可重试事务**（pivot 之后）必须**幂等**。原始文献 = Garcia-Molina & Salem (1987, ACM SIGMOD)。→ **工程含义：撤销不是"删除"，而是"执行一个语义相反的动作"**；且**必须显式标注"不可回退点"**（对本仓：**已验收的文档、已入库的 commit、已接受的 ADR 即 pivot**）。

【A】A-36: **durable execution = 追加日志 + 重放，而非快照回滚**：Temporal（Event History）/ Microsoft Durable Orchestrations / AWS Step Functions（Retry + Catch 的声明式错误处理）都以 **append-only 事件历史**记录每个决策与结果，崩溃后**重放历史重建状态**，从而**不必重做已完成的副作用**。**关键约束（MS Durable Orchestrations 明示）**：为使重放确定，**非确定性的模型调用与外部副作用必须移出可重放的编排控制流**，落入"recorded steps"（记录式步骤）；Temporal 侧的表述同旨（"log each step so a restarted run reaches the same point without redoing side effects"）。→ 与本仓 **事件流 append-only + I-2（禁 wall clock）+ 决策入流**逐条同构；这也是"**回溯不删历史**"的最强工业背书。

【A】A-37: **回溯应"跳出深度"而非"退一步"——非时序回溯（non-chronological backtracking）**：CSP/CP 求解从朴素**时序回溯**（chronological，逐层退）演进到 **backjumping / conflict-directed backjumping（CBJ）/ dynamic backtracking（DBT）**——失败时不退回上一层，而是**直接跳到与冲突相关的那次决策**（"退到最近一次真正导致该冲突的变量赋值"）；工业 SAT/CP 求解器（CDCL、Gurobi/CPLEX/Chuffed）进一步以**冲突导向子句学习（conflict clause / nogood）**记录"此组合必然失败"，使搜索**不再重复同类死胡同**。该文献族把"反复探索无用子树"命名为 **thrashing**（Lecoutre et al., *Artificial Intelligence* 173 (2009) 1592–1614 将其归为 look-back 方案，与 look-ahead 并列）。→ **本仓含义：一次评审意见要求的回改，应落到"被证伪的产物"所在的那一步，而不是机械退一步**；且"哪些组合已被证伪"应被记录下来（= 决策记录 + M7 账本）。

【A】A-38: **"该重做什么"应由内容决定，而非时间戳**：Snakemake 按输出记录 provenance，并在**代码 / 输入 / 参数 / 软件环境 / 修改时间**变化时决定是否重跑；Nextflow 对每任务计算 hash，`-resume` **要求缓存命中且输出仍保留**；OxyMake 以 **BLAKE3 内容寻址缓存键**（规则源码 + 输入内容 + 参数 + 环境 + 平台）**取代 mtime 代理**。OxyMake 明确点出 mtime 代理的**双向失效**：**phantom re-run**（git checkout / 目录复制 / 备份还原会改写 mtime 而内容未变 → 白白重跑）与 **missed re-run**（内容已变但时间戳更"新" → **静默复用陈旧结果**）；DANTE 亦记录 Snakemake/Nextflow 的同类取舍。→ **本仓含义：判断"回改后要重跑哪些步"，应基于"哪个产物/前提的**内容**变了"的显式依赖，而非"哪一步更晚"**。

【A】A-39: **prospective vs retrospective provenance 的二分**（Freire & Chirigati, *IEEE Data Eng. Bull.* 2018）：**prospective provenance = 实验的规格/计划**（步骤图、参数、期望产物），**retrospective provenance = 实际执行的记录**（真跑了什么、产出什么）。前者是"打算怎么做"，后者是"实际做了什么"；两者用途不同、**必须分别保全**。→ **本仓的对应极干净：四文档（RESEARCH/DESIGN/IMPLEMENTATION/CHECKLIST）+ `step` 序 = prospective；事件流 session（`seq`/`decision`/`ts`）= retrospective**。回溯时两者**须分别版本化**——**计划变更改文档版本号，执行变更追加事件流**。

【A】A-40: **R-LAM（arXiv:2601.09749，Reproducibility-Constrained Large Action Models）**：面向科学工作流的 LAM 框架 = **结构化 action schema** + **确定性执行策略** + **显式 provenance 追踪** + **replay / forking**；并把执行引擎定位为**"概率推理与确定性执行之间的 reproducibility firewall"**，支持 **failure-aware execution loop** 与**受控 workflow forking**，使"迭代实验"与"可复现"不再互斥。→ 与本仓 **step-gate（确定性门禁）+ append-only + `fork`** 逐条同构，且**明确给出"回溯 ≠ 破坏可复现"的架构条件**。

【A】A-41: **DANTE 内容寻址工作流（arXiv:2609.08695）**：15 阶段 DAG 的**版本化 workflow contract** 显式声明「阶段序 / 依赖 / 期望产物 / **verifier 命令** / 结果可见性 / **resumability**」；**durable state 把"不可变的尝试史（attempts + 产物 hash）"与"可替换的进度信息"分离**；恢复时**只恢复与"冻结合同"兼容的工作**（resumes only work compatible with the frozen contract）。→ **"冻结合同 + 只恢复兼容工作"正是本仓「不改历史 PROGRESS 行 / 已验收文档须版本化变更」的工程化表述**。

### 12.3 场景二：数据获取受阻——"重试"还是"重规划"？

【A】A-42: **ToolMaze（arXiv:2606.05806）——工具失败的动态重规划基准**：把工具扰动按 **2×2** 分类（**显式/隐式 × 瞬时/永久**）；实测 ① **隐式语义失败最致命**——**Perturbation Recovery Rate（PRR）下跌约 37%**，根因是模型**过度信任被污染的输出**（structurally valid but semantically corrupted）；② **复杂拓扑把 agent 困在徒劳的试错循环（futile trial-and-error loops）**；③ **容错能力随模型规模提升的速度比基础任务慢 3.66×** → **动态重规划是独立的、不能被 scale 或提示词替代的能力**。→ 对本仓：**"数据获取受阻"必须先判扰动类型**——**瞬时**（网络/端点/限流）→ **重试**；**永久**（数据不存在/采不到）→ **回跳重规划**；而**隐式污染（拿到了数据但语义不对）最危险**，恰是本仓 A-3（LGMM λ̂ 在论文/设计/代码三层指代不同对象）那类断点，须靠**数值探针 / 重数比对**而非"看起来像"来发现。

【A】A-43: **回溯式 agent 规划的结构化解法**：① **BEAP-Agent（arXiv:2601.21352）** 把 GUI 任务执行建模为 **DFS**，以 Planner / Executor / **Tracker** 三角色支持**长程、多级状态回溯**；② **LATS（ICML 2024）/ SWE-Search（ICLR 2025）** 用 **MCTS + 树搜索**替代线性执行——原文指出"现有基于 LLM 的软件 agent 常遵循线性顺序过程，**这妨碍了回溯与替代方案的探索**"，并以**混合价值函数**（数值 + 语言评估）实现"**在真正无望的分支上更早回溯**"（SWE-Search 在 SWE-bench 上相对提升 23%）；③ **共同工程纪律**：朴素重规划若无**步数上限与收敛检查**，会让 agent **无限加步而不产生实质进展**（replanning loop；另一份综述把失败模式归为 commitment bias / context drift / lack of exploration / replanning loops 四类）。→ **对本仓：回溯需要"预算"（轮次/步数上限）与"收敛判据"，否则退化为 thrashing。**

### 12.4 闭环纠错的落点：最小回改集

【A】A-44: **闭环多轮规划（Closed-Loop Multi-Round Planning via Self-Reflection and Error Correction）**：每轮后基于可观测反馈对中间状态做**一致性验证与约束满足检查**；检测到偏差即触发**反思模块做错误归因（error attribution）并定位"补丁点（patching points）"**；再由**纠错模块"最小化关键步骤"以恢复可行轨迹**（minimizes key steps to restore feasible trajectories），并配**轨迹对齐 / 失败类型分布**的诊断可视化。→ **"定位补丁点 + 最小回改集"是本轮对本仓最直接可用的原则**：回改范围应是**因果必要集**，而不是"从出错点往后的全部重做"。

### 12.5 场景一：模拟评审意见 → 多步调整

【A】A-45: **返修的语义分层**：**Minor revision** = 有界修复（澄清、补引文、收窄论断），**通常不再外审**（编辑直接裁决）；**Major revision（revise and resubmit）** = 需**补充分析 / 补数据 / 重构论证**，**几乎必然返还原审稿人二审**（MDPI 明示：要求大修或建议拒稿的审稿人**始终**会收到修订稿）。**轮次上限**：MDPI **通常最多两轮大修**，更多轮次需学术编辑推荐。另有独立事实：**返修不是从零开始**——审稿人已了解论文，修订稿**回到原审稿人**；配套纪律 = **逐条点对点回复（point-by-point response）+ 变更高亮**。→ **对本仓：P-020 起「新决策轮 = 独立 `vN` session」正是这条语义的物理化**（`specwf-p042-...v2/v3` 与 `specwf-p028-...v2/v3` 即两轮返修实证）；但**返修必须带"意见 → 改动锚点"的响应表**与**轮次上限意识**。

【A】A-46: **跨轮次的审稿期望不是恒定的**：Dwivedi et al.（*Journal of Global Marketing* 39(1):3–17, 2026）把审稿轮次刻画为 **R0 编辑初筛与契合度 → R1 发展潜力 → R2 响应性与方法可信度 → R3 润色与专业交付**，并给出关键判据：**"early tolerance is not forgiveness"**——早期轮次的容忍是**对提交物的条件性宽限（option value）**，**持续未消解的弱点会在后续轮次招致更硬的评判**。→ **对本仓：回溯轮次中"未消解项"必须显式登记并跨轮结转**，不能因"本轮通过"而消失；否则即 thrashing 的另一种形态——**反复进入却没有清偿**。

### 12.6 场景三：结果不理想 → 重做缺口分析

【A】A-47: **回溯本身不是问题，"回溯后改写历史叙事"才是**：**HARKing**（Hypothesizing After the Results are Known，Kerr 1998）= 把**事后假设当作事前假设**呈现；三型 = **CHARKing**（构造新假设冒充先验）/ **SHARKing**（隐去曾做出并失败的预测）/ **THARKing**（**明确标注为探索性** → 可接受）。连带失效模式 = **p-hacking**（反复选数据/选分析直到显著）与 **garden of forking paths / researcher degrees of freedom**（示例：5 个分析决策 × 各 5 种可辩护选择 = **3125 条分析路径**）。→ **对本仓：回溯改口径（如"重做缺口分析"）本身合法，但必须"旧口径留痕 + 新口径显式标注为事后"**——这与本仓「不改历史 PROGRESS 行」「ADR `supersede` 不编辑」是**同一纪律**。

【A】A-48: **预注册与 Registered Reports 的机制本质 = 给"计划"打时间戳，以区分确认性与探索性**：**预注册**（OSF / ClinicalTrials.gov / AsPredicted）在**观测数据之前**公开登记研究问题、假设、设计与分析计划；**Registered Reports** 更进一步——**Stage 1 先同行评审背景/设计/分析计划**，通过即获 **in-principle acceptance（原则性接收）**，随后**无论结果如何都发表**（Stage 2 只核验是否遵循注册方案）。二者**不禁止探索**：探索分析始终可做，**但必须明确标注为 exploratory**。收益被明确表述为：降低 HARKing / p-hacking、降低假发现率、消除发表偏倚与"文件抽屉问题"，并使"愿意做严谨研究的作者"获益（"the incentives for authors change from producing the most beautiful story to the most accurate one"）。→ **本仓含义：这为"回溯留痕"提供了科学规范层的正名**——回溯**不改写"我们原本打算做什么"的时间戳记录**。

【A】A-49: **负结果/失败路径的规模与处置**：行业实测——Microsoft/Bing 约 **1/3** 特征测试为正、**1/3** 为负；Google/Bing **10–20%** 实验产生统计显著正向；Airbnb **90–92%** 的 250 个搜索排序想法未改善指标；Booking.com **约 9/10** 测试无赢家（Kohavi："over two-thirds of ideas actually fail to move the metrics… Fail fast, pivot fast"）。学术侧：**82%** 研究者认同负结果应被分享，但**仅 14%** 实际发表（主因"太耗时" 53% / "负结果引用少" 26%）；**"negative data ≠ useless data"**——需区分**负/意外数据**与**无用数据**，前者应被结构化记录并共享（Emborg, *Brain Res Bull* 192:203–207, 2022）。→ **本仓含义：失败路径（被证伪的假设、不可得的数据）应作为一等产物入库**，而非被静默丢弃。

### 12.7 映射到本仓：物理前提已具备，缺"回溯语义"与"收敛规则"

【B】B10（见附录 B）: **回溯的正确语义 = "非时序回跳到被证伪的那一步（A-37）+ 补偿式留痕而非删除（A-35/A-36）+ 最小回改集（A-44）"**。这否定了两种直觉做法：① **顺序退一步**——thrashing 的源头（A-37）；② **删除重来**——破坏 append-only 与可复现（A-36/A-41）。**回溯跨度应由因果链决定，而非层数**；且**必须显式区分"不可回退点"（A-35 的 pivot）与"可重做区间"**。

【B】B11（见附录 B）: **本仓的"回溯物理前提"已全部具备，缺的是语义与规则**：✅ append-only 事件流（不可变历史）；✅ `fork`（从旧 `seq` 派生支线）；✅ **多轮独立 `vN` session（P-020 先例，`specwf-p042-...v2/v3`、`specwf-p028-...v2/v3` 已实证两轮返修）**；✅ ADR `supersede` 链（决策取代而非编辑）；✅ M7 证据账本（负结果可入账）。**缺口三项**：① **回溯事件无形式化记录**（从哪步回到哪步、跨度、影响集、被取代的产物版本）；② **无收敛/终止规则**（thrashing 与 replanning-loop 防护，A-42/A-43）；③ **"计划变更 vs 执行变更"未显式分离**（A-39 的 prospective/retrospective 二分未落位）。

【B】B12（见附录 B）: **本仓"重做缺口分析"的合规形态 = 计划变更版本化，而非就地改写**：既然 RESEARCH/DESIGN 属 prospective provenance（A-39），"回到第 2 步"在本仓应表现为**该文档版本号自增 + 新增"本轮回溯依据"节**（**旧结论保留在历史叙述中**）；"实际跑过什么"则追加到事件流。**"旧口径留痕 + 新口径标注事后"由此获得机械落点**（A-47/A-48），且**无需引入 Saga 引擎、状态机库或 DAG 引擎本体**。

**处置矩阵（三类场景 × 本仓动作；C-8 的落地形态）**

| 场景 | 触发性质 | 社区对应 | 本仓动作（零新机制） |
|---|---|---|---|
| 模拟评审 → 多步调整 | **计划内的"预期返修"**（非失败） | Major/Minor revision（A-45）+ 跨轮期望（A-46） | **新建 `vN` session** 承载本轮返修；**点对点响应**（意见 → 改动锚点）落 IMPLEMENTATION 版本变更节 + CHECKLIST 复跑节；**轮次上限意识**（MDPI 两轮先例）；**未消解项跨轮结转** |
| 数据获取受阻 → 重启调研 | 需先判 **瞬时 vs 永久**（A-42） | ToolMaze 2×2 + 重试/重规划分流（A-42/A-43） | **瞬时** → 同轮重试（不产生回溯）；**永久** → **回跳至 research 步**，在 RESEARCH 版本自增中登记"数据可得性被证伪"；**隐式污染**用数值探针 / 重数比对兜底（A-3 教训） |
| 结果不理想 → 重做缺口分析 | **计划被证伪**（认知更新，非执行错误） | HARKing 防护（A-47）+ 预注册留痕（A-48）+ 负结果一等公民（A-49） | RESEARCH **版本自增**并新增"缺口重估"节（**旧缺口判断保留**）；事件流追加新决策；**禁止就地改写旧结论**（= HARKing 的工程形态） |
| （横切）收敛控制 | thrashing / 无限重规划 | 步数上限 + 收敛检查（A-43）；thrashing（A-37） | **同一 (step, 产物) 的回改计数**与**轮次上限**作为登记项；**超限即升级人工裁决**，不自动续轮 |

### 12.8 裁定（C-8/C-9）与假设（H6/H7）

【C】C-8（见附录 C）: **回溯可行，且以既有机制承接；对照 ADR-0010 三问——Q1 主体为 Layer-0 概念登记（处置矩阵为纪律层），零新组件；Q2 无明确激活触发（当前各 feature 的返修已由 `vN` session 承接，未出现"影响集不可控"的实证痛例）；Q3 零副作用。故本轮仍止于调研（懒加载 gate 保持），不实施工具改动**。理由：① 本仓**不欠物理前提**（B11）；② 回溯的正确形态是**纪律**（非时序回跳到因果源 + 最小回改集 + 旧值留痕）而非**引擎**（Saga / DAG / 状态机库均为外部重型本体，违 D6 零依赖定位）；③ 唯一"可选增量"是**回溯事件的形式化记录**（B11 缺口①），但按懒加载 gate 登记为**触发式候选**，触发条件 = **出现一次"影响集失控"的真实案例**（例如：某次返修波及 3 个以上 feature，或两次返修互相覆盖）。

【C】C-9（见附录 C）: **收敛控制的判据确立（登记层，非实现层）**：采纳 A-43 的"步数上限 + 收敛检查"作为**回溯纪律的两条硬约束**——① **轮次上限**（先例：MDPI 两轮大修；**超限须人工裁决而非自动续轮**）；② **进展判据**（每轮回溯必须能指出"消解了哪条未消解项"，否则即为 thrashing）。两者**只登记为纪律**，不引入任何计数器/工具；若未来实施，其形态应是 **step-gate 的只读校验**（而非新写路径）。

- **[H6] 回溯的"影响集"（哪些前步必须重做）应如何确定？** 未裁决——可选路径：① **人工声明**（当前事实做法，零成本但依赖判断力）；② **依赖图反向闭包**（机械推导，需先有显式依赖元数据——与 H1/H4 同源，且 §4.1 全量 DAG 的性价比未实测）。本仓现状（PROGRESS 依据列 + 四文档间的 markdown 链接）**已具备弱依赖信号**，但**未验证其能否支撑自动闭包**。
- **[H7] 回溯轮次上限的合理阈值未实测**——MDPI 的"两轮大修"是**期刊编辑流程**的经验值，本仓 `vN` session 先例目前最多到 `v3`（P-042 / P-028）；"几轮之后应当改判为'换 feature / 换方向'而非继续返修"缺乏本地实证，登记为观察项。

## 13. 补充调研六：盲区扫描——五轴系统性排查（v1.5）

### 13.1 扫描方法

用户提问「除三个场景外是否还有盲区」。本节按本仓既有盲区扫描方法（P-015 先例：**多维轴 + 证据分级 + 环境维度**）对学术推理写作链做**系统性排查**，判据两条：① **该轴是否已有承接机制**（本 feature 前四轮 + 本仓既有机制）；② **若已有，是否覆盖该轴的核心失效模式**。扫描结果仅保留**同时满足"无机制覆盖"或"覆盖不完整"且"有实证痛例"**者，其余显式声明为**已排除**（避免为凑数而制造盲区）。

**轴与首轮判定**：**过程轴**（链上哪步失效）— v1.0 九步同构 + v1.4 回溯，**已覆盖**；**证据轴**（断言/溯源/审计）— v1.0 声明=重数 + v1.1 M7/PROV/审计 + `verify-anchor`，**已覆盖**；其余四轴进入取证。

### 13.2 环境轴（真盲区①）：外部世界变化使"当时正确"的前步过期

**关键区分**：v1.4 覆盖的是**内部证伪**（后步的产出证伪前步）；本节发现的是**外部过期**——前步在写下时**完全正确**，但随着外部世界变化而失效。**两者机理不同、处置也不同**（前者靠回溯纪律，后者靠触发式重检）。

【A】A-50: **证据的"时效性失效"是系统综述领域的既有问题，且有预设触发机制**：Cochrane 把「**signals for updating**」正式化为**须在 protocol 中预先规定**的条款；F1000Research 的 Living Systematic Review（LSR）指南规定**检索与筛查的频率、更新计划、以及何时启动新一轮同行评审都必须写入方法**；实操中检索结果只可能有**三种结局**——(1) 无新研究；(2) 有新研究但**不改变结论**；(3) 有新研究**改变结论**——**只有第三种才触发全量更新与再评审**。Cochrane 的更新提案决策框架还给出「不更新 → 至少两年后再评估」的显式分支。实证：Butler 等在 *J Clin Epidemiol* (2024) 报告一项运行两年的 Cochrane LSR——**30 次检索更新 + 3 次全量更新**，其结论是 LSR 应当「**被证明有理据、预先规划（含更新时机与终止触发）、及时发表**」。→ **对本仓：外部过期需要"预先写定的重检触发 + 三分类分流（无关 / 不改变 / 改变）"，而不是每次重跑**；且「**何时停止更新**」与「何时更新」同等重要。

【A】A-51: **reference rot 的双重形态：link rot（资源消失）与 content drift（同一 URL 内容变了）**：Klein 等（*PLoS ONE* 9(12):e115253, 2014，遍历 350 万+ 论文中 100 万+ 条 web 引用）给出**两个量级**——**1/5 的 STM 论文受 reference rot 影响**；**若只统计含 web 引用的论文，则高达 7/10**。其余实证：Ott（*JSLS* 2022）抽检 95 篇 / 2,424 条引用，**14.7% 因链接失效或指向错误文章而"不可检索"**，并明确指出**此前研究已发现 9–25% 的被引陈述被误引或断章取义**；另有汇总显示 URL 引用的可及率从 **87%（0–5 年）降至 38%（>10 年）**，永久失效比例从 2012 年的 **5% 升至 2025 年的 15%**。→ **"content drift" 这一形态对本仓尤其致命**：它意味着**引用锚点即使仍然可访问，也可能已不再支持当初的陈述**——这与本仓"**声明=重数**"的失效形态**完全同构**（锚点可达 ≠ 陈述成立）。

【A】A-52: **撤稿传染（retraction contagion）与可机械化的核验链**：Retraction Watch 数据库已收录 **超过 63,000 篇撤稿**（2023 一年即 >10,000 篇），现由 Crossref 合作维护；而**撤稿后的引用中，承认该文已撤稿的不足 5%**；COPE 指南进一步指出「**引用了已撤稿文献的系统综述本身可能需要更正**」。核验工具链已成型且**可机械化**：`citecheck`（对 `.bib`/`.ris`/CSL-JSON/`.docx` 逐条查 Crossref + OpenAlex 存在性 + 撤稿状态，**并有退出码 0/1/2 可接入 CI**）、`RWCheck`（本地 SQLite ingest Retraction Watch 数据集 + Pre-commit hook 形态）、`CiteGuard`（区分 retracted / corrected / expression of concern / hijacked-journal，**不做二值化**）、`retraction-watch-mcp`（整篇 PDF/DOCX/LaTeX 一次性筛查全部引用）；Zotero 亦已内置 Retraction Watch 比对。→ **这是本轮扫描中"风险最高 × 最可机械化"的一项**：环境轴的三类失效里，**只有引用层失效可以纯机械检出**。

### 13.3 合规轴（真盲区②）：AI 披露、引用幻觉、重复发表、报告规范

【A】A-53: **AI 使用披露已成硬性规范，但其效力被实证证伪**：ICMJE 与 COPE 自 2023 年起的通行规则是——**AI 不得列为作者**（作者须对科学性与原始数据承担完全责任），**允许辅助但必须声明**；**主流出版商在"披露位置"上并不统一**：Elsevier 要求**投稿系统与正文两处**，Nature Portfolio 要 Methods 或 Acknowledgments，Science 要 Methods 且**须点名具体工具**，IEEE **仅允许编辑用途且禁止 AI 生成原始图**。更关键的是**政策效力实证**：He & Bu（arXiv:2512.06705）分析 **5,114 种期刊 / 5,235,012 篇论文**发现——约 **70% 期刊已有 AI 政策（多为"要求披露"）**，但**有政策与无政策的期刊在 AI 使用增长上无显著差异**；对 164,579 篇全文的分析显示，2023 年后 75k 篇论文中**仅 76 篇（约 0.1%）显式披露了 AI 使用**——即**政策基本未能提升透明度**。→ **对本仓：若依赖"期刊政策会让人自律"，等于依赖一个已被证伪的机制**；合规必须做成**自己链上的检查项**。

【A】A-54: **AI 引用幻觉的规模足以穿透同行评审**：Editage 汇总的同行评审研究显示伪造引用率区间为 **18%–69%**（按模型、学科、提示设计而变）——GPT-4 众学科综述 414 条中 **18%** 伪造、心理健康领域 176 条中 **19.9%**、**6 项早期研究的合并值达 51%**；2026 年 GPTZero 对 **NeurIPS 2025 的 4,841 篇被接受论文**的审查发现 **53 篇含至少 100 条确认的幻觉引用**（每篇经 3–5 位专家评审仍未拦住）；香港大学报告的一篇已发表论文 **61 条引用中 20 条为 AI 伪造**。结构性原因被明确指出：**伪造引用与真实引用由完全相同的生成过程产生**，且典型伪造件会**使用真实作者名 + 真实期刊 + 指向无关论文的可解析 DOI**——因此"**问模型自己是否真实**"不构成检查（那是"第二次幻觉机会"）。→ **对本仓：引用核验必须是"出链到外部权威库"的机械动作，不能是自证**。

【A】A-55: **重复发表 / 文本回收 / 香肠切片三现象的定义与处置梯度（直击"多期刊变体"策略）**：COPE 给出三个**相邻但不同**的概念——**redundant/duplicate publication**（已发表的作品/数据/分析的全部或实质部分被再次发表而未透明声明）、**text recycling / 'self-plagiarism'**（自身既往文字在未透明引用的情况下再现）、**salami slicing**（把研究切成最小可发表单元以虚增产出，会**扭曲系统综述**并**降低每篇的影响力**）。**分节宽容度差异明确**：引言/背景的少量回收常难避免；**方法段**因描述同一技术本来写法有限，**较宽容**且**说明"该法已在别处描述"并引用即合规**；**结果段几乎总是不可接受**（若重复已发表数据，则按**重复发表**处理而非"简单文本回收"）。处置按重叠程度与位置分级：**更正 → expression of concern → 撤稿**（COPE **不认可"部分撤稿"**），**重叠须在投稿时声明并引用既有作品**；工具（相似度检测）**不能作为唯一判据**（存在语言差异导致的漏检实例，编辑须按内容与程度判断）。→ **对本仓：用户的"同一核心 → 不同期刊变体"策略正落在该红线区**；合规动作 = **投稿时显式声明重叠并引用既往版本**（而非寄望相似度工具放行）。

【A】A-56: **会议/期刊的"声明清单"制度 = 本仓"声明=重数"的同行，且已具强制力**：NeurIPS 2026 的 **Paper Checklist 为必填，缺失即 desk reject**（置于参考文献后、**不计入 9 页正文**），约 15–16 项覆盖**claims 与结果对齐 / limitations 专节 / 理论假设与完整证明 / 可复现性 / 代码与数据获取（含精确命令与环境） / 实验细节（数据划分、超参、选择方法） / 统计显著性（误差棒、种子数、计算方法） / 算力申报 / 伦理 / 广泛影响 / 既有资产的引用与许可声明**；ML Reproducibility Checklist（arXiv:2003.12206）为其前身；且**纯实证论文对理论项须显式填 N/A**（而非留空）。→ **"逐项显式回答 + 缺则拒稿"正是本仓"显式缺口（I-8）+ 声明=重数"的学术版**；差别在于本仓的清单是**自查派生**，而学术清单是**对手方门禁**。

### 13.4 时间轴（真盲区③）：冻结与例外处理

【A】A-57: **scope freeze / scope lock 双层冻结，且有"冻结后例外"的显式判据**：HP 大型跨国项目（COMPASS，~200 名贡献者 / 5 年 / 50+ 国家）的实证经验是**单层冻结不够**——先设 **scope freeze**（约发布前五个月停止新增），再设 **scope lock**（约四个月前连"需设计复核的需求"一并锁死），否则**后期加入的范围项无法完成而被迫丢弃**。冻结后的变更判据被明确为**四维评估**（业务 / 技术 / 测试 / 发布）并**当例外处理**：**只有"修正错误"与"补齐合规缺口"可直接进**，其余进 **parking lot（停放区，标为"post-... 产出"）**——"把'不'变成'尚未'"。配套三件：**变更控制**、**决策日志（Issue / Decision / Rationale + 日期 + 相对人）**、以及 **time-box（时间固定则范围可变，范围固定则时间可变，二者不可同时固定）**。→ **本仓含义：`pivot（不可回退点，A-35）` 是"单个决策"尺度的不可回退点，`freeze` 是"整条链"尺度的——本仓已有前者（ADR accepted / commit 入库），缺后者。**

### 13.5 人轴（真盲区④）：何时该止损，而非继续回溯

【A】A-58: **escalation of commitment 的双向风险**：Staw（1976，"Knee-Deep in the Big Muddy"）以 240 名受试者证明——**对初始决策负个人责任者，会向失败项目追加显著更多资源**（机制 = 自我辩护：承认该止损等于承认原决策错误），该效应已**在至少八项后续实验中被复现**，是组织行为学中最稳健的发现之一。Arkes & Blumer（1985）以"雷达盲飞飞机"场景给出量级：**在告知既往投入时 85% 选择继续注资，不告知时仅 10%**；票务现场实验亦显示**全价购票者出席率显著更高**（两组观看权完全相同）。深层机制 = **损失厌恶**（Kahneman & Tversky 1979：等额损失的权重约为收益的两倍）→ 止损被框定为"确定的损失"，继续则保留"不确定的希望"。**但反方向同样存在**：Heath & Petersen 的实验（受训 MBA）支持 **mental budgeting**，并指出**premature de-escalation（过早放弃）**——**在不该放弃时放弃**——因为过去失败不应机械地导致退出。→ **本仓含义：`vN` 轮次若只受"数量上限"约束，会同时存在两种错误——该停不停（escalation）与不该停而停（premature de-escalation）；判据必须是"前瞻性证据"而非"已投入多少"。**

【A】A-59: **kill criteria：把"放弃决策"移到唯一能理性做出的时刻**：核心机制 = **预先承诺的条件**（"a specific, pre-committed condition under which you will abandon a course of action"），因为**人在当下无法理性做出放弃决策**（情绪胁迫下）；配套三件：**事前验尸（pre-mortem）**（先想象失败）、**stop-loss**（借自金融的硬阈值）、以及必须防范的 **renegotiation trap（重新谈判陷阱）**——**每次条件触及时就顺势改判据**，使 kill criteria 形同虚设。工业界的对照物 = R&D **sunk cost kill matrix**（**只用前瞻性指标评分，把既往支出完全剔除**），并指出传统 stage-gate 之所以失效，是因为**评委会评估"过去里程碑完成度"而非"下一块钱的回报"**；另一个被点名的失效形态是 **zombie project**（达不到核心目标，却因制度惯性存活）。AI 侧的并行物 = **early stopping / circuit breaker**。→ **本仓含义：kill criteria 与 v1.4 的"轮次上限"互补——上限是数量约束，kill criteria 是条件约束；且必须先写定，否则退化为 renegotiation trap。**

### 13.6 映射到本仓与裁定

【B】B13（见附录 B）: **"前步过期"有三种来源，v1.4 只覆盖其中一种**：① **内部证伪**（后步产出证伪前步）——v1.4 已覆盖；② **外部世界变化**（新文献出现 / 数据源变更或消失 / 引用被撤稿 / 链接内容漂移，A-50~A-52）；③ **外部要求变化**（报告规范、AI 披露政策、期刊清单，A-53/A-56）。②③ **不是"当时写错了"，而是"现在过期了"**——因此**不能靠回溯纪律解决**，必须靠**预先写定的重检触发**（A-50 的三分类分流）+ **门禁化核验**（A-52/A-56）。

【B】B14（见附录 B）: **本仓对外部引用的核验能力目前为零，而这是唯一可完全机械化的一环**：`verify-anchor` 核验的是**仓内路径**（文件存在 + 章节标题 + 行号），**不覆盖仓外资源**；而环境轴要求的恰是**仓外三层核验**——**存在性**（DOI/bib 可解析）× **未变更**（A-51 的 content drift 二分）× **未撤稿**（A-52）。三者**均有现成工具与结构化数据（Crossref / OpenAlex / Retraction Watch 数据集）**，且 `citecheck` 已具 **CI 退出码语义**（0/1/2）——**与本仓 hook 语义天然对齐**。

【B】B15（见附录 B）: **`pivot`（A-35）与 `freeze`（A-57）是同一概念的两个尺度**：pivot = **单个决策**的不可回退点（过此不再补偿、只能重试）；freeze = **整条链**的不可回退点（过此只允许修错与补合规）。本仓已具备前者（ADR `accepted`、commit 入库、文档 `accepted`），**缺后者**；且 A-57 给出的"**只有修错与补合规可直接进，其余进 parking lot**"为后者提供了**现成的例外判据**。

【B】B16（见附录 B）: **`vN` 轮次若缺 kill criteria，正是 A-59 的 renegotiation trap**：v1.4 的 C-9 只给了"轮次上限"（**数量约束**），而 A-59 表明真正防住"该停不停"的是**条件约束**（预先写定的前瞻性阈值）；同时 A-58 提醒**反方向风险（过早放弃）**——故 kill criteria 必须与"**新证据是否改变结论**"（A-50 的三分类）绑定，而**不能与"已投入多少轮"绑定**。

**扫描结论表**

| 轴 | 扫描结论 | 本仓 Gap | 处置 |
|---|---|---|---|
| 过程轴 | 已覆盖（v1.0 九步同构 + v1.4 回溯） | — | 无需动作 |
| 证据轴 | 已覆盖（声明=重数 + M7 + PROV + `verify-anchor`） | **仅限仓内**（B14） | 见环境轴的"仓外三层核验" |
| **环境轴** | **真盲区①**（A-50/A-51/A-52） | **无任何承接机制**；"外部过期"与"内部证伪"未区分 | **C-10**（登记 + 触发式重检候选） |
| **合规轴** | **真盲区②**（A-53~A-56） | 无投稿前合规检查；多期刊变体策略正落在 A-55 红线区 | **C-11**（合规四检登记为纪律；引用核验优先触发） |
| **时间轴** | **真盲区③**（A-57） | 有 pivot（单决策），无 freeze（全链） | **C-12**（freeze + kill 判据须预先写定） |
| **人轴** | **真盲区④**（A-58/A-59） | 仅有"轮次上限"（数量约束），无条件判据 | **C-12**（同上；并防 renegotiation trap） |

【C】C-10（见附录 C）: **环境轴为真盲区，且优先级最高——它是唯一一类"本仓完全无对应机制"的失效**。理由：本仓的事件流 / 门禁 / 审计三件套全部回答"**我们做了什么**"，**不回答"外部世界是否已使既有结论过期"**；而 A-50 表明该问题在证据合成领域已被正式化为**预设触发条款**，A-51 表明其漏检率可达 **7/10**，A-52 表明其后果（引用已撤稿文献）**可能在发表多年后才被追认**。**裁定 = Layer-0 概念登记 + 触发式重检候选（懒加载 gate 保持）**：采纳 A-50 的**三分类分流**（无新证据 / 有新证据但不改变结论 / 有新证据且改变结论 → 仅第三种触发回溯）；触发条件 = **出现一次"外部过期"真实案例**（引用了已撤稿文献 / 依赖的数据源失效或改版 / 外部要求变化使既有产出不合规）。

【C】C-11（见附录 C）: **合规轴为真盲区，但性质与①不同——它不是"要不要造工具"，而是"要不要在链上插一道检查"**。用户的两项实际情形使其不可豁免：**多期刊变体发表策略**（A-55 的重复发表/香肠切片红线区）+ **LLM 辅助写作**（A-53 的披露义务 + A-54 的引用幻觉）。**裁定 = "投稿前合规四检"登记为纪律**（① **引用核验**：存在性 + 撤稿状态；② **AI 使用披露**（按目标期刊的实际位置要求，注意 Elsevier 需两处）；③ **重叠发表声明**（投稿时声明并引用既往版本）；④ **报告规范清单**（按目标 venue 的必填 checklist 逐项显式作答））。其中**引用核验建议优先触发工具化**：它是四检中**唯一可完全机械化**（B14）且**风险最高**的一项——**0.1% 的实际披露率（A-53）× 18–69% 的伪造率（A-54）× <5% 的撤稿提及率（A-52）三者叠加下，人工核验不可能可靠**。

【C】C-12（见附录 C）: **时间轴与人轴合并裁定：freeze 与 kill criteria 都必须"预先"写定**——两者共享同一原理（A-59）：**决策必须移到尚能理性做出的时刻**（前者在开始前冻结范围，后者在开始前写定放弃条件）。**本仓形态 = 在 feature 的 DESIGN/CHECKLIST 中预注册两类判据**：**freeze 判据**（哪些是 pivot、冻结后仅允许修错与补合规、其余进 parking lot）与 **kill 判据**（何种前瞻性证据出现即终止而非继续返修）；并**显式防 renegotiation trap**（条件触及时不得顺势改判据）。**"何时停止更新"与"何时更新"同等重要**（A-50 的"不更新 → 至少两年后再评估"即此意）。

- **[H8] 环境轴重检的触发频率与成本未实测**——A-50 的 LSR 以**月度检索**为节奏，本仓无任何自动化；"人工按批次重检"与"引入监听/定时"的成本收益未实测。
- **[H9] 仓外核验是否可引入外部数据源未裁决**——Crossref / OpenAlex / Retraction Watch 数据集均为外部依赖，**与本仓 D6 零依赖定位直接冲突**；替代形态（**离线快照 + 手动刷新**，或以"仅生成待核清单、由人工在浏览器完成核验"的**零依赖半自动形态**）是否足够，未实测。

## 14. 补充调研七：目标竞争与评价漂移（环境轴 B/C 层细化，v1.6）

### 14.1 缘起：把"环境轴"拆成三层

用户对 §13.2 提出细化：「必须建立研究**目标扫描**机制，定期扫描**预印本网站**、搜索关联文献，防止**目标缺口被填满、方法思路被抢发**——或者**目标期刊风向变化、审稿人 taste 变化、学术风向、技术潮流、数据开放**等层面」。据此把环境轴拆为三层，本轮补 **B/C 两层**（A 层已由 §13.2 覆盖）：

| 层 | 机理 | 处置形态 | 本轮 |
|---|---|---|---|
| **A 时效性失效** | 已有产出被外部变化**弄旧/弄错** | 重检触发 + 三分类分流 | §13.2 已覆盖 |
| **B 抢先失效** | **目标本身**被别人先做掉（novelty 被剥夺） | **早期预警 + 差异化重定位**（无可补偿动作） | **本 §14.2** |
| **C 评价标准漂移** | **游戏规则**变了（风向 / taste / 术语） | 噪声认知校正 + 术语时间序列 | **本 §14.3** |
| **机会窗口** | 数据开放 / 技术潮流**使原本不可行变可行** | 机会捕捉（与威胁同源） | **本 §14.4** |

### 14.2 B 层：抢先失效——"被先做掉"是常规职业风险，不是意外

【A】A-60: **多重独立发现（multiple discovery）是科学的常态而非例外**：Merton 把"多人独立做出相似发现"称为 **multiples**，并主张**多重发现而非唯一发现才是科学的普遍形态**（经典例：牛顿/莱布尼茨微积分、达尔文/华莱士演化论、门捷列夫/迈耶周期表）。实证：Hagstrom（1974）调查 **1,718 名美国学术研究者**——**46.2% 自认被抢先 1–2 次，另有 16.4% 认为被抢先 3 次以上**；Gaston（1971）调查 **203 名英国高能物理学家**——**38% 一次、26% 多次**。→ **对本仓：把"被抢先"当作可预期的常规风险来规划（而非偶发事故），是 B 层设计的前提。**

【A】A-61: **抢先的实际代价可量化，且被主观严重高估**：Hill & Stein 利用 **Protein Data Bank 的"embargo 先于论文"特性**，追踪 **1,630 场**结构解析竞赛（1999–2017）——**并列第二的论文仅比首发低 2.5% 的发表概率**，但**更可能落在低影响力期刊**；按 100 次引用份额计，**首发 58 / 次发 42**。而他们对 **915 名结构生物学家**的调查显示，研究者的**预期是 71:29**——即**"恐惧远超实际损失"**。→ **本仓含义：被抢先不等同于工作作废；但"次发趋向低影响力期刊"意味着对以期刊层级为目标的策略，损失是真实且需前置规划的。**

【A】A-62: **惩罚不是均匀的——机构地位会反转它**：同一研究发现，**当顶尖机构的团队被低知名度机构抢先时，第二名反而获得略多引用**；而**顶尖机构在"抢先方"位置时获取的引用份额更大**。→ **对本仓含义：独立研究者 / 单写者恰在"低知名度机构"这一侧，必须按最坏情形（无地位补偿）规划，不能按平均值预期。**

【A】A-63: **预印本是"优先级保险箱"，但过早公开会把 novelty 判定污染**：arXiv 提供**永久、带时间戳、可被引用且不可篡改的优先级声明**（Ginsparg 原话：arXiv postings are accepted as **date-stamped and citable priority claims**）；Mishkin 等（arXiv:2010.05365）以马尔可夫过程建模并以 **10k 次 Monte-Carlo** 模拟竞争水平与抢先概率，论证"等 3–6 个月再公开"实际是"**等 1–3 年且祈祷运气**"，并给出反面代价：**arXiv 公开版可能被会议审稿人以"缺乏新颖性"质疑**（且构成去匿名化）。据此给出的实务时序是：**会议投稿后 1–2 周、且确认 venue 匿名政策允许时发布；绝不在投稿同日发布**。→ **本仓含义：B 层的"防御"本身是有代价的取舍——早公开换优先级、牺牲匿名与新态度评价。**

【A】A-64: **"缺口被填满"最常见的机制不是别处抢先，而是目标期刊自己刚发过**：desk reject 占投稿的 **30%–70%**（高水平期刊 40%–60%，高度选择性期刊可达 60%–90%），而编辑筛选中 **"创新性不足（insufficient novelty）"在一项调查中占 desk reject 的 51%**；编辑的判据是"**这篇是否推进了对话**"，且明确会**交叉比对本刊近期发表以避免重复**（editors cross-reference recent publications in their journal to avoid redundancy）。→ **本仓含义：B 层的扫描对象必须包含"目标期刊近 12 个月的目录"，而不是只有预印本站点。**

### 14.3 C 层：评价标准漂移——量级已被实证固定为"结构性噪声"

【A】A-65: **同行评审的随机性有硬数字**：NeurIPS 2014 实验把约 10%（**170 篇**）投稿**随机分给两个独立程序委员会**双审，166 篇可判——**43/166 = 25.9% 的决策不一致**；**accept precision = 0.495**（≈"若独立重跑，约一半被接收的论文会被拒"）；reject precision = 0.175；agreed accept rate = 0.218。对照**纯随机基线**（inconsistency 37.5% / accept precision 25%）：**实际委员会优于随机，但远低于直觉**。

【A】A-66: **噪声的来源被定位为"主观性"，且揭示一个不对称**：Cortes & Lawrence 七年后重访该实验（arXiv:2109.09774）——**50% 的审稿人评分方差源于主观因素**；**被接收论文的评分与其后续引用量无相关**，而**被拒论文的评分与引用量却有相关** → 结论是「**评审流程善于识别差论文，却不善于识别好论文**」，并据此建议社区**减少对"顶会发表"作为个人质量代理的执念**。→ **本仓含义：单次"被拒"几乎不携带关于工作质量的信息；但"被打低分"携带信息。复评与返修的注意力应分配给后者。**

【A】A-67: **该结论在规模扩大一个数量级后依然稳定**：NeurIPS 2021 复现实验（**882 篇**重复送审）：**23.0% 决策不一致**（vs 随机基线 35.1%）；**spotlight 层的不一致尤其极端**（一个委员会推荐的 spotlight 有 **13/25 与 13/23** 被另一委员会拒，即**超过一半**）；程序主席结论 =「**没有证据表明决策过程随规模变大而变得更噪或更不噪**」。→ **评审噪声是结构性的，不能指望"领域成熟/规模变大"使其改善。**

【A】A-68: **风向与潮流是可测量的，且有可操作的信号**：hot topic dynamics 已有量化方法（Chumachenko, *PLoS ONE* 2025：以 NVI 距离构建年度概念网络 + MST 抽取趋势，发现**概念漂移集中在时间局部的 hub 上**、并非由共现频率驱动）；趋势探测框架报告可**在主流化前最多 18 个月检出**（precision > 0.89）。实务信号（跨文献一致指向）：**① 术语漂移**（某新词/新法在最近一年突然高频出现）；**② 期刊专题**（顶刊开始出专刊）；**③ 领军者转向**（领域内主要研究者更换方向）。→ **本仓含义：C 层可观测，但观测对象是"术语/主题的时间序列"，单次检索看不出漂移——这正是需要"定期 + 差分"的原因。**

### 14.4 机会窗口：数据开放与技术潮流是**双向**的

【A】A-69: **数据开放是政策强制的机会窗口**：NIH 的 **Data Management and Sharing Policy**（2023-01-25 生效）要求**提交 2 页 DMS Plan，无 Plan 不予受理**，共享**不晚于发表时**、最低保存 3 年，并明确采用 **FAIR** 原则；OSTP 2022 备忘录把公开访问要求推向全体联邦资助研究。政策自述的理由正是「**复用难以生成的数据（reuse hard-to-generate data）**、加速发现、支撑验证」。→ **机会面：原本需要数年采集的数据，可能已经现成。**

【A】A-70: **但同一政策也是竞争威胁**：数据开放**消灭"数据获取护城河"**——若一项工作的贡献点之一是"我拿到了这个数据"，开放后该贡献归零；且高价值数据集在**被你复用**的同时，也**被竞争对手同等复用**。→ **本仓含义：数据开放不是单边利好，而是"机会窗口开启 + 护城河消失"的同一事件；判断时必须同时问"我现在能做什么"和"我原本靠什么领先"。**

【A】A-71: **技术潮流/危机会把"快"变成标准，慢的一方直接出局**：COVID 期间预印本占英文 COVID 文献的比例一度接近 **40%**（后降至约 28%，因基数从 16,000+ 涨到 49,000+）；bioRxiv 上线约 **2 天**、medRxiv 约 **4 天**，对照传统期刊**平均约 125 天**；Europe PMC 于 **2020-07** 起索引 COVID 预印本全文。同期体量：arXiv 于 2026 年**累计超 300 万篇**、**每月新增 >15,000 篇**；天体物理单一子领域约 **70 篇/天**。→ **本仓含义：当领域进入"快"的均衡态，"等一轮完整审稿再公开"会直接失去对话窗口——这与 A-63 的预印本时序策略互为印证。**

### 14.5 零依赖半自动监视形态（用户指定约束）

用户明确要求监视机制**设计为零依赖半自动形态**。证据表明这是可行且成熟的：

【A】A-72: **"告警 / 现状知悉（current awareness）"是成熟领域，且必须不自建检索**：主流告警源包括 **Google Scholar 三类告警（关键词 / 作者 / 引文告警——"追随一篇锚定论文的被引，常是子领域开始移动的最早信号"）**、**PubMed 保存检索告警（MeSH 受控词使精度优于裸关键词）**、**arXiv / bioRxiv / medRxiv 的邮件或 RSS 告警（按分类 / 作者 / 关键词）**、期刊 **TOC 告警**、以及把 RSS 汇入阅读器。已知短板被明确记录：**Scholar 索引滞后数天至数周**（可靠但"很少是第一个看到"）、覆盖面不穷尽。→ **本仓约束天然满足：告警由外部平台完成，本仓不需要任何检索能力。**

【A】A-73: **"人负责抓、工具负责记"的形态已有先例，且节奏可分层**：`scholar-alert-reader-skill` 的做法是——**接收告警内容（Scholar Alert / RSS / BibTeX·RIS / 网页）→ 本地解析 + 去重 + 可解释打分 → Review Workspace 交互筛选 → 沉淀本地文献库（可选导出 Zotero/Obsidian）**，全程不自建抓取。配套节奏（跨来源一致）为三层：**每日快扫（daily literature check）→ 每周审读（weekly review）→ 每季战略评估（quarterly strategic assessment）**。→ **与本仓 C-7 的 L0/L1/L2 三档自动强度同构**，可直接映射为「**L0 提交时刷差分清单 / L1 收到告警时喂入 / L2 定期（月/季）整体重算**」。

### 14.6 映射到本仓与裁定

【B】B17（见附录 B）: **B 层不是"过期"而是"剥夺"，且没有补偿动作**——用 v1.4 的语言：**抢先 = 外部先到达 pivot（A-35 的不可回退点），不存在 compensating transaction**。因此它的处置形态与 A 层根本不同：A 层是"**重检 → 三分类 → 重跑**"（可更新），B 层只能是"**早期预警 → 差异化重定位 / 或终止（kill）**"。→ **结论：B 层需要一个"预警"面，而不是一个"更新"面。**

【B】B18（见附录 B）: **C 层的量级已被实证固定，其管理学含义是"降低单次判决的权重"**：25.9%（2014）与 23.0%（2021）的决策不一致率、0.495 的 accept precision、50% 的主观方差、以及"高分端与引用无相关／低分端有相关"的不对称 —— 合起来意味着：**"好却没中"几乎不携带信息，"被打低分"才携带信息**。故本仓的**复评资源应按此分配**（对低分做归因，对"高分被拒"不做过度归因），避免把评审噪声误读为自我诊断信号。

【B】B19（见附录 B）: **零依赖半自动形态的最低充分三段式**：**① 人负责"抓"**（订阅 Scholar 引文告警 / arXiv 分类 RSS / 目标期刊 TOC，用现成阅读器聚合）；**② 本仓负责"记"**（把抓到的条目落为**本地清单文件**，与既有缺口清单做**差分**）；**③ 差分产出三态**——「**新增疑似重叠**（可能被抢先）」/「**新增疑似过期**（A 层）」/「**无变化**」。**全程零外部依赖**（不调 arXiv/Crossref API、不引第三方库），且**与 A-73 的日/周/季节奏及 C-7 三档强度直接对齐**。

【C】C-13（见附录 C）: **B/C 两层均登记为真盲区，但优先级低于 A 层**。理由：**A 层是"产出已被污染"**（可能已把错误写进论文/已发表），后果直达记录完整性；**B 层的后果是"投入被浪费 / novelty 被剥夺"**，**C 层的后果是"判决不公"**——两者都**不污染既有真实记录**。**裁定 = 零依赖半自动形态落地为「纪律 + 本地清单」**（不建抓取、不引依赖、不新增脚本）；**触发条件 = 出现一次真实案例**（被抢先导致返工，或因 novelty 被 desk reject）。**懒加载 gate 保持**。

【C】C-14（见附录 C）: **"抢先预警"与"止损"的耦合正式确立**：B 层的预警输出应**直接喂给 v1.4 的 kill criteria（A-59）**——"该切口已被占用"正是 kill criteria 所要求的那类**前瞻性证据**（而非"已投入多少轮"的沉没量），同时避免 A-59 的 renegotiation trap。→ **本仓至此形成一条完整的判据链**：A-50 的**三分类**（是否改变结论）× B 层的**抢先预警**（切口是否仍空）× A-59 的 **kill criteria**（何时终止）。

- **[H10] 告警覆盖的召回率与延迟未实测**——Scholar 滞后数天至数周、覆盖面不穷尽；arXiv 分类告警是否对"相邻领域"存在系统性漏报，本仓无实测数据。
- **[H11] "重叠判定"的自动化边界未裁决**——由 LLM 判"这篇是否与我的缺口重叠"属 M7 关注的高幻觉点（与 A-54 同源：伪造与真实引用同源生成）；是否应以「**只做机械的关键词/分类差分，重叠判定全数交人工**」为上限，未实测。

## 15. 补充调研八：论文仓库实例扫描与流程规范化（v1.7）

### 15.1 方法：从"实测症状"出发，而非从文献推断

用户指令「补充扫描用户的论文仓库实例 里面有 lean4 形式化证明 逆向拆解文档 文档散乱管理不够规范 / 当前调研的是学术推理写作场景还有什么可以再补充调研的 系统性规范化用户的论文写作流程」。本节与前面七轮**方法论不同**：先对 `D:\Article\Working paper\` 下 7 个论文仓做**机械盘点（E1）**，再按症状检索社区对应标准，最后把症状归因到"缺哪一层"。**所有数字均为本机实测**（`os.walk`，排除 `.lake`/`.git`/`node_modules`/`__pycache__`）。

**实测读数（E1）**：

| 维度 | 读数 |
|---|---|
| 规模 | **521 目录 / 4503 文件** |
| **编译产物与源码混放** | `.aux` 101 / `.log` 111 / `.out` 86 / `.toc` 54 / `.dvi` 32 / `.bbl` 29 / `.blg` 26 / `.fls` 18 / `.fdb_latexmk` 17 = **474 个** |
| 残留物 | 压缩包 **40** / `.bak` **10** / `fix_*`·`debug*.py` **34** / `新建文本文档.txt` 1 |
| **`.tex` 源文件名** | **137 种**——含无语义的 `document.tex` / `document-A.tex` / `document2.1.tex`，以及**把状态词写进名字**的 `*_v2_Final` / `*_v3_Corrected` / `*_v4_Reviewed` / `_v9_Rigorous` / `_v5_complete` |
| **治理文档同名不同格式** | `CODE_WIKI.md` 6 + `Code_Wiki.md` 3（大小写两种）= **9**；`ARCHITECTURE.md` 6 + `engineering_architecture.md` 1；**决策 3 名**（`DECISIONS.md` 4 / `DECISION_RECORD.md` 1 / `key_decisions.md` 1）；**开发日志 3 名**（`DEVLOG.md` 2 / `DEVELOPMENT_LOG.md` 3 / `DEV_LOG.md` 2）；**spec 4 名**（`SPEC.md` 5 / `spec.md` 1 / `SPEC_PROCESS.md` 2 / `SPEC_GUIDE.md` 1） |
| **版本目录命名** | **≥5 种形态**：`CDO_8.1`（下划线）/ `LGMM 8.0`（空格）/ `MIDAS v2.0`（小写 v + 空格）/ `SABR_v1.0`（下划线 + v）/ `v2.0`（裸）/ `RMT3.0`（无分隔）；且 `Coupla` / `Fisher–Conduction Duality` / `Volsurface_Heston` **无版本目录** |
| **Lean 双源** | `LGMM 8.0/lean4/`（15 文件）与 `LGMM_Lean/LGMM/`（12 文件）**文件集不一致**（前有 `BahadurBoundary.lean`、后有 `AsymptoticNormality.lean`）→ **同项目两份证明源**；lean 目录名也不统一（`lean/` / `lean4/` / `JOLF/` / `LGMM_Lean/`） |
| `.lake/` 依赖树 | 在仓库内（mathlib 全量，数千文件） |
| 打包与解压并存 | `files.zip`（多处）/ `v3.1.rar` / `LGMM_0727.rar` / `CDO 5.0.rar` + `CDO_5.0.zip` + `papers_achived/CDO 5.0/` |
| 目录名错拼 | `papers_achived`（archive） |
| 一次性修补脚本堆积 | `Volsurface_SABR/SABR_v1.0/` 内 **23 个** `fix_*.py` / `debug*.py` |
| **规范化程度极不均衡** | `LGMM 8.0/` 最规范（`code/ data/ docs/ lean4/ memory/ paper/ roadmap/` + `MANIFEST.md` + `RESEARCH_LOG.md` + `RESEARCH_MAP.canvas`）；`Coupla/` 次之（`.github/` + `spec/templates/` + `pyproject.toml` + `LICENSE`）；`Volsurface_SABR/`、`算子传导/`、`Gold/`、`RMT/old/` 基本是裸 tex 堆 |
| 已有 PKM 痕迹 | `roadmap/.obsidian/`、`RESEARCH_MAP.canvas` |

**归因（症状 → 缺哪一层）**：① **474 编译产物 + 40 压缩包** → 缺「**派生物 vs 真值源**」的分界；② **137 个 `.tex` 名 + ≥5 种版本目录名 + 状态词入名** → 缺「**单一真值 + 版本外置**」；③ **治理文档 9 份同名不同格式** → 缺「**文档契约**」（同名 ≠ 同义，跨项目不可机读）；④ **Lean 双源漂移** → 缺「**证明制品的单一归属**」；⑤ **34 个 one-off 脚本** → 缺「**脚本生命周期分层**」；⑥ **规范化程度不均衡** → 缺「**可复制骨架**」（最规范的 `LGMM 8.0` 是偶然，不是模板）。

### 15.2 社区对应：五层标准（按症状对号）

【A】A-74: **Research Compendium**（Marwick, Boettiger & Mullen 2018；The Turing Way 专章）——**三条原则**：**① 文件按约定目录结构组织；② 数据、方法、产出明确分离；③ 计算环境被指定**。其"可读性"面向亦有成文约定（Nüst, Boettiger & Marwick《**How to Read a Research Compendium**》把 Keshav 的三遍读法扩展到 compendium，主张**作者应按读者的阅读路径组织**）；工具侧有 `rrtools`（**0. Git 管理目录 → 模板 → 环境隔离 → CI**，且明确"**不要把这些一次性设置函数存成项目里的脚本**"）。→ 正对症状 ①⑥。

【A】A-75: **RO-Crate**（RO-Crate 1.1，2020-10-30 发布，researchobject.org **Recommendation** 级）——**机器可读打包的最小充分条件**：一个目录 + 一个 **`ro-crate-metadata.json`**（JSON-LD + Schema.org），描述 **Data Entities**（文件/目录）与 **Contextual Entities**（人/机构/许可/时间）；核心设计哲学被明示为「**just enough linked data**」+ **对开发者友好**（假定受众是熟悉 JSON 的 Web 开发者，**不要求语义网背景**）。已有跨领域采用（**WorkflowHub / LDaCA / OME-OMERO / M@TE / HUN-REN ARP**），且可与 BagIt / ZIP / **git** 组合。→ 正对症状 ③（把"这个仓是什么"从自由文本变成**可机读的一等产物**），且**天然满足本仓零依赖定位**（纯 JSON 文件，无运行时）。

【A】A-76: **Lean 项目布局是硬约定，且官方明示 `.lake/` 应被忽略**：workspace 的标准布局 = `lean-toolchain`（钉住版本）+ `lakefile.toml` **（当前默认；`lakefile.lean` 仅在需计算配置时用）** + `lake-manifest.json`（依赖清单）+ **`.lake/`（"this folder is typically gitignored"，且可安全删除以强制全量重建）**；模块约定 = `Myproject.lean`（**root 文件通常只含 import 行**）+ `Myproject/`（其下即 `Myproject.Something`）；`lake new myproject math` 直接生成 mathlib + lint + CI 骨架；官方明确警告**依赖必须钉到 tag/commit 而非 `main`**（mathlib 与 Lean 版本锁步，漂移即海量报错）。→ 正对症状 ④ 与 `.lake` 入库问题。

【A】A-77: **Lean blueprint = 大型形式化的"地图"，且社区已解决"非形式化文档与形式化代码重复"这一根本问题**：blueprint 源于 Massot 的 `leanblueprint`（以 `\uses` / `\leanok` 宏从 LaTeX 生成依赖图），"**节点 = 形式化陈述，边 = 证明依赖**"；FLT（50+ 贡献者）与 sphere packing 级项目**必须有图**（下一代为 Verso Blueprint，且 blueprint 本身是**可类型检查的 Lean 文档**）。**LeanArchitect**（CMU / Trento，arXiv:2601.22554）明确点出既有工作流的**两个根本局限**：① **blueprint 信息在 LaTeX 与 Lean 之间重复** → 维护开销 + **漂移机会**；② 缺乏 AI 集成。其解法 = **把 blueprint 元数据以声明式注解内联进 Lean**，**自动推断依赖**（递归遍历声明中使用的常量）与**证明状态**（检查是否用 `sorry`），并**导出与 Lean 同步的 LaTeX**——设计目标是「**消除形式化与非形式化表示之间的重复**」。修复侧另有 **BlueprintRepair**（arXiv:2607.28110）：以**类型化局部编辑**（十个 schema 检查的操作，操作须**指名被编辑的节点**，故目标定理不可被偷换）修失败蓝图，实测**每解一状态成本最低**（源码 patch 为 1.30×，整模块重写为 2.06×）。→ **正对用户"逆向拆解文档"与 134 个 `.lean` 之间的同步问题**。

【A】A-78: **LaTeX 仓库卫生有成文黑名单与工具链**：需忽略的产物被逐项列出（`*.aux / *.log / *.out / *.toc / *.lof / *.lot / *.fls / *.fdb_latexmk / *.synctex.gz / *.bbl / *.bcf / *.blg / *.run.xml / *.dvi / *.xdv / *.nav / *.snm / *.vrb` 等）；VS Code + LaTeX Workshop 提供**源头拦截**（`latex-workshop.latex.outDir` 指向 `out/` + `autoClean.run: onBuilt`，官方 recipe 用 `latexmk`）；命令行侧 `latexmk -c` 清副产物、`-pvc` 热编译。**关键实证（不只是"难看"）**：`.olignore` 提案记录了**陈旧派生物导致的三类真实危害**——① **编译失败**（服务端写不出自己的 `thesis.aux`，因陈旧 aux 被"钉住"）② **产生错误 PDF**（Overleaf 用**陈旧 `.bbl`** 而非重新生成 → **参考文献错误**）③ 仓库噪声（协作者看到数十个二进制产物）。→ 正对症状 ①。

【A】A-79: **文件命名有跨标准共识，且"final"被明确指为谎言**：日期 **`YYYY-MM-DD`（ISO 8601）**——其决定性特征是"**字母序 = 时序**"，在任何文件浏览器/操作系统/语言环境下均成立（并须补零，否则 `2026-6-…` 会排在 `2026-10-…` 之后）；**连字符分隔词内、下划线分隔字段**（两分隔符规则）；小写 + 数字 + `-`/`_`/`.`；**禁用空格与 `< > : " / \ | ? *`**；数字补零；长度 < 70；**描述内容而非归档过程**。对"版本"的判据尤为锋利：**"一旦 `final` 进了名字，就没有词留给下一个版本"**——于是 `final 2` → `Version 6 FINAL` → `really final`，名字**不再说明状态**；另一类明确失效是**"文件名被当 changelog 用"**（"Clean and Tracked"、"Indemnity Sections"、"as of 13 Nov" 描述的是**编辑过程**，应进元数据不进名）。→ 正对症状 ②。

【A】A-80: **命名混乱的代价已被量化**：一项实验室数据完整性研究给出——**73% 的研究数据重复事件直接源于命名不一致或歧义**，且 **89% 的研究者每周至少浪费 1 小时**寻找文件；另一份对照表显示**日期格式不一致使检索慢 34%**；对 10,000 个真实文件名的分析发现 **73% 至少含一项"生产力杀手"模式**（其中 **41% 为不一致日期格式、34% 为模糊版本指示**）。→ 为症状 ② 提供**量化动机**（这不是审美问题）。

【A】A-81: **研究制品的归档与引用已成制度（ACM Artifact Review and Badging v1.1，2020-08-24，与 NISO RP-31-2021 对齐）**：三类**相互独立**的徽章——**Artifacts Available**（绿色，可被他人验证）/ **Artifacts Evaluated**（红色，Functional / Reusable）/ **Results Validated**（蓝色，Reproduced / Replicated）；**术语经 NISO 建议后互换**（**Reproducibility = 不同团队、同一装置、用作者的制品**；**Replicability = 不同团队、不同装置、独立制品**）。"Available" 清单的硬性要求：**公开存档 + 不可撤销的版本化 + 长期保存**——"**such as Zenodo but not GitHub**"，且 **"promises of future availability are not acceptable"**；须有允许比较与扩展的**许可**（CC-BY / MIT）与**引用论文的 README**。**Data-Availability Statement** 章节（置于参考文献前）要求**像引用文献一样引用制品**，且**不要用"always latest"的 DOI，要用对应版本的 DOI**（FigShare 用 `.v1` 后缀）。版本标签范式（OOPSLA 2025 实例）：**`-R1-submission` / `-R1-camera-ready` / `-AEC-submission` / `-AEC-revision` / `-AEC-final`**——**恰好把"投稿 / 返修 / 终稿"三态标准化为可机读标签**。→ 正对症状 ②（并与用户的多期刊变体策略直接相关）。

【A】A-82: **文档组织有成熟分类框架，且其核心价值被定位为"禁止混模式"**：Diátaxis（Procida；被 Python / Cloudflare / Canonical / Django / Gatsby 采用）按**用户意图**（而非受众角色）划分四模式——**Tutorial**（学习）/ **How-to**（任务）/ **Reference**（查阅）/ **Explanation**（理解），判别问句为"内容是**指导行动**还是**指导认知**"×"服务于**获取技能**还是**应用技能**"；**硬规则 = 同一页面禁止混模式**。迁移者实证（ADR 0004，agentic-harness）：**按受众分组**（`development/ operational/ design/ architecture/`）在实践中会让**每一页同时是 reference + how-to + explanation**，读者"**分不清自己正在读哪一种**"，且该页"**为哪一种都没优化**"；并指出**最大可读性收益来自这条硬规则本身，而非模式名**。→ 正对症状 ③（治理文档同名不同格式，本质是**同一名字下混了多种模式**）。

### 15.3 映射到本仓与用户仓库

【B】B20（见附录 B）: **论文仓的症状与本仓不变式逐条对偶**——本仓的六条不变式可**原样翻译**成论文仓纪律，故"规范化"不需要新方法论，**只需把既有不变式外推一层**：

| 论文仓实测症状 | 本仓对应不变式 | 论文仓应立纪律 |
|---|---|---|
| 474 编译产物与源码混放 | **I-5 纯派生 / I-6 不增真值** | **派生物不入真值区**（`outDir` 重定向 + gitignore + 清理） |
| 40 压缩包与解压目录并存 | **I-1 单写路径** | **一份真值**：压缩包只作分发包，不作第二真值 |
| 137 个 `.tex` 名 + 状态词入名 | **I-3 幂等 / 版本外置** | **名 = 身份，版本 = 元数据**（`final` 不入名，见 A-79） |
| 治理文档 9 份同名不同格式 | **I-7 词表对齐** | **同名必须同义**（文档契约：同名 = 同模板同字段） |
| Lean 双源漂移 | **I-10 语义同源** | **证明制品单一归属**（一处 Lean，其余降为指针） |
| 34 个 one-off 脚本 | **I-8 显式缺口** | **脚本分层**（`explore/` 与 `pipeline/` 分离，前者可删） |

【B】B21（见附录 B）: **用户仓里的"逆向拆解文档"就是"非形式化—形式化"的桥，而社区已给出它的正确形态 = blueprint**（A-77）：现状是 `CLAUDE_REASONING_ARCHITECTURE.md` / `PROOF_ANALYSIS.md`（RMT4/5 各一份）/ `LGMM8_Proofs_Analysis.md` / `verify_proofs.py` / `SABR_v6_完备性分析.md` **各自为政，与 134 个 `.lean` 之间靠人工同步**——**这正是 LeanArchitect 点名的"两份制品重复 → 维护开销与漂移"**。**正确形态**：让「**陈述 → 依赖 → 证明状态（是否含 `sorry`）**」从 Lean 侧**自动导出**（A-77），人工文档只保留 **Explanation**（为什么这么做、放弃了什么），**不重复 Reference**（做了什么）——这同时是 A-82 的"禁止混模式"在形式化场景的实例。

【B】B22（见附录 B）: **用户的多版本发表策略与返修轮次，社区已有标准化标签方案**（A-81 的 `R1-submission / camera-ready / AEC-submission / AEC-revision / AEC-final`）——即**"阶段语义"应由标签承载，而非由文件名自由发挥**。这可直接消解当前 `JOLF-2.0` / `JOLF_3_1_MVP` / `RMT-4.0` / `RMT-5.0` / `CDO_v9_Rigorous` 之间「**哪个对应哪一轮投稿**」**不可机读**的问题；并与 v1.4 的返修语义（A-45/A-46）、v1.5 的合规四检（C-11 之重叠声明）**天然衔接**。

### 15.4 裁定

【C】C-15（见附录 C）: **规范化应"分层落地"而非"一次重整"**。判据来自 E1 的**不均衡**（`LGMM 8.0` 已接近 compendium，而 `Volsurface_SABR` 是裸 tex 堆）——**统一重整会同时破坏已规范的部分、又无法一次改完未规范的部分**。**裁定 = 先立"契约层"，再逐仓迁移**：契约层 = **一页 `CONVENTIONS.md`（命名 + 目录骨架 + 派生物隔离 + 脚本分层）+ 三个模板文件（论文骨架 / Lean 骨架 / 治理文档骨架）**；**且契约层零工具、零依赖**（纯 markdown + 模板），符合 D6。触发条件 = 用户指定首个迁移仓。

【C】C-16（见附录 C）: **"规范化"的最大价值不在整洁，而在可机械检出**。A-80 的 73%/89%/34% 全部是**人在错**（找到错文件、用掉时间、对错版本）——而机器可以代替人做这类检查。**四条可立即机械化的判据**：① **编译产物零残留**（gitignore + `--check`）② **命名合规**（正则：日期 ISO、无空格/特殊字符、版本不入名）③ **同名文档同模板**（字段齐备性）④ **生成物可重生成**（compendium 的"可执行"要求）。**其中 ①②④ 与本仓 project-console 的"纯派生视图 + 门禁"完全同构**，**可复用同一套"生成器 + hook + 校验器"三件套形态**（这正是 P-047 已落地的架构），无需新范式。

【C】C-17（见附录 C）: **blueprint（A-77）是用户仓中"性价比最高的一项新增"**。理由：用户已投入 **134 个 `.lean`**（CDO 21 / JOL 10 / LGMM 62 / MIDAS 24 / Volsurface_Heston 17），但**证明依赖关系只存在于人脑与散落 md 中**；blueprint 把「**定理依赖图 + 证明完成度**」变成**可机械导出的产物**，社区有现成实现（`leanblueprint` / LeanArchitect），且**与本仓既有的"派生视图"哲学同构**。**但仍懒加载**：本轮**仅登记**，触发条件 = 用户决定把某个论文仓做成"**可被第三方独立核查**"的制品（即 A-81 的 **Artifacts Available** 门槛）——**规范化到"能被别人复现"的那一天，blueprint 与 compendium 就是同一件事的两面**。

- **[H12] 规范化契约的"最小充分集"未实测**——"一页契约 + 三模板"是否足以覆盖 7 个仓库的全部差异（尤其 `Coupla` 已有 `spec/templates/`、`LGMM 8.0` 已有 `MANIFEST.md` 的既成事实），需一次真实迁移验证后方可定稿。**v1.10 部分实测（2026-09-13，LGMM 8.0 只读扫描，零写入）**：以 [PILOT_TASK_CARD.md](PILOT_TASK_CARD.md)（type: template）对 pilot 仓跑全部迁移判据，得 **"骨架层充分、判据层不足"**——骨架已备（`MANIFEST.md` 双向溯源 + `.gitignore` LaTeX 段 + `code/scripts/` 七子层 + 根层同名 0），但"最小充分集"须**再含判据层三件**：① 判据须为**可跑命令**而非语义勾选（实测七项判据全部落为 PowerShell 命令后方可判对错）② 须**排除第三方子仓**（`data/co_pricing_zoo/` 的 `_v2` 文件约 12 个属依赖库，非本仓缺陷）③ 须 **hash 级对比**（仅凭文件名/目录名无法判"漂移"，见 H13）。→ **H12 由"未实测"改为"部分实测"**；全量迁移实测仍待 H16（广播粒度）裁决后执行。
- **[H13] Lean 双源漂移中哪一份是真值未裁决**——`LGMM 8.0/lean4/`（15 文件）与 `LGMM_Lean/LGMM/`（12 文件）**文件集不一致**，需逐文件 diff 后才能定"保留哪份、另一份降为指针"；**在裁决前不得删除任一份**（AGENTS.md 破坏性操作纪律）。**v1.10 实测修正（2026-09-13，只读 SHA256）**：读数修正为 `lean4/` = **16** 个 `.lean`（v1.7 记 15，实际 16）；`LGMM_Lean/LGMM/` 与其中 **13** 个同名，逐对哈希比对 = **12 内容一致** + **1 内容不同（`EWNLS.lean`）**；另有 **3 个仅在 `lean4/`**（`BahadurBoundary.lean` / `JointDistribution.lean` / `LGMM.lean`）。**澄清一处误判**：`LGMM_Lean/` 根含 mathlib 全量 **7735** 个 `.lean`（依赖库），**项目根是其 `LGMM/` 子目录**，故"双源"确为两个 LGMM 制品，而非"专有源 vs 依赖库"。→ **裁决方向收敛**：真值源取 `LGMM 8.0/lean4/`（16 完整）；12 一致者降为指针（内容等价）；`EWNLS.lean` **原记「需人工判定（两版语义不同）」已由 §17.8 收口**——实为 **A 超前而非分歧**（A ⊃ B：多 9 个声明 / 单文件 +2 公理 / 非空行仅 A 有 147 且 B 零独有）。**原记「裁决仍待用户确认，确认前不删任一份」继续有效**。**v1.14 补（P-066 §17.8）**：方向已由**机械判据**锁定（文件集 ⊂ / 文本行 99.84% ⊂ / 声明集 34 ⊂ 43 且 B 零独有 / mtime 晚，四路独立同向 + 该仓 changelog 自证）⇒ **H13 状态「数据齐备待裁决」→「证据齐备待追认」**。

## 16. 补充调研九：共享层与辅助资产归属（v1.8）

### 16.1 缘起与方法

v1.7 之后用户追问「真实仓库里面存在问题，解决方案是否已经调研过，是否还需要补充调研来解决」。据此做了一次**覆盖度审计**：把 §15 的六层根因逐条对地毯式核对"已有覆盖 vs 真空白"，结论是**六类中五类的解法已在手**（4 类来自已调研社区标准，1 类来自本仓既有机制可直接外推），**只有两项是真空白**——**⑨ 跨论文共享层**与 **⑧ 辅助资产归属**（另 1 项 ④b 为触发式）。**本轮补这两项**。方法沿用 v1.7：**先补一手实测（E1），再按症状检索**。

**E1 增补读数（本轮新增扫描）**：

| 组 | 读数 |
|---|---|
| **A 共享层**（`Working paper/` 根，**13 个文件**） | ① 论文级共享资产：`CODE_WIKI.md` / `Academic Phrasebank Navigable PDF 2018.pdf` / `2025-2026年数理金融计量领域学术热点全景分析（含规范引用）.pdf`；② **归档快照**：`LGMM_0727.rar` / `MIDAS-Granger.rar`（**根目录无对应解压副本** → 说明根已被当作"归档层"）；③ **个人/职业内容**：`potemkin-village-notes-en.md`(+`.bak`) / `职场经历对话记录.md` / `草台班子复盘.md` / `草台班子观察笔记.md`(+`.bak`)；④ 跨项目脚本：`turnover_backtest.py` + `turnover_low_decile_backtest.png` |
| **B 实际项目数** | **~17 个**（用户之初只报 7 个）：另含 `2025-2026研究进展` / `Time-Varying Functional Itô Avellaneda–Lipkin Model` / **`论文参考资料`** / `PhD` / `DL-KS-IGMM` / `Gold` / `RMT` / `Volsurface_SABR` / `算子传导` / `Agent_Multi` |
| **C 辅助资产总量** | `.pdf` **363** / `.csv` 404 / `.png` 199 / `.txt` **121** / `.json` **114** / `.docx` 18 / `.xlsx` **4** / `.canvas` **3**；分布极不均（LGMM：pdf 85 + csv 301；MIDAS：pdf 78；Agent_Multi：pdf 67；CDO：png 114）。**`论文参考资料/`（9 pdf + 2 md）是一个与论文项目平级的独立"资料层"** |
| **D 同名多处出现** | `files.zip` ×**10**（**且与解压目录并存**）；`.pytest_cache` ×**9**；`SKILL.md` ×**13**（含第三方 `co_pricing_zoo/.agents/`+`.claude/` 与 `CDO算子/.trae/skills/`）；**`document.tex` / `.pdf` / `.aux` / `.log` / `.synctex.gz` 各 ×6–7**（无语义名在多项目重复）；`CODE_WIKI.md` ×6；**文献提取文本 4 种命名**（`barunik_extracted.txt` / `extracted_text.txt` / `temp_*.txt`（MIDAS 4 个）/ `_dl_ks_igmm.txt`） |

**归因**：⑨ 共享层是**"多用途杂层"**（研究资产 + 归档快照 + 个人内容三类混放，且无红线）；⑧ 辅助资产（文献/字典/笔记）**无归属规则**，且**其中含绝不应外传的内容**。

### 16.2 共享层：社区对应

【A】A-83: **monorepo / polyrepo / hybrid 三元结构，且"混合形态"被承认为独立一类**（Brousse, *Programming '19*, ACM）：表格给出三类——**Multi-repositories**（polyrepo；Amazon / Netflix / Lyft）/ **Mono-repository**（Microsoft / Uber / Twitter / React / Google / Facebook / Angular / Babel / Kubernetes）/ **Hybrid** 两变体：**Poly-as-Mono**（Android / Chrome）与 **Mono-as-Poly**；该文并指出**该主题的学术研究不足**（大量材料是网上比较），结论是**选择属权衡比较**，而 monorepo「**encourages consistent and high-quality code**」。→ **用户现状精确落在 `Mono-as-Poly`**：一个物理目录承载多个独立项目与共享资产，**有 monorepo 的形态、无 monorepo 的机制**。

【A】A-84: **monorepo vs polyrepo 是组织问题而非工程问题，且有可操作的规模判据**：一份实战复盘（作者先后在 Meta 的巨型 monorepo 与 AWS 的千仓 polyrepo 工作，并把自己公司的 **15 个仓迁移为 1 个**）列出两侧代价——polyrepo：「**Discoverability is terrible**」（"同一基础设施模式被十几个团队各写一遍"）、跨切面改动需协调数十仓、共享库=**版本管理地狱**、重复代码累积；monorepo：克隆 GB 级、搜索慢、构建需分布式缓存、热点文件冲突频繁、"**删一个函数可能有 200+ 跨团队引用**"。**判据被明写**：「**Monorepo wins when: Team size is 1–50 engineers and everyone needs to coordinate; Services share data models, auth, and infrastructure**」。→ **用户是 1 人 + 17 个项目 + 确实共享的资产（bootstrap / phrasebank / 热点分析 / 6 份 `CODE_WIKI`）** → 判据**明确落在 monorepo 侧**；同时其**代价也已发生**（该仓已达数百 MB–GB 量级）。

【A】A-85: **"多论文共享层"在社区的三种成文形态**：① **研究组 handbook 模板**（`cct-datascience/group-handbook-template`）把最佳实践（compendium 结构 / 命名（**脚本编号等宽补零**、**日期 ISO 置首**、**避免空格与大小写**）/ 文件格式 / **共享存储位置**）写成**组级文档**——即「**共享层首先是一份规范，而不是一个目录**」；② **项目模板仓**（`ggszk-lab/research-template`，AI 友好）：`00_admin`（**`data_policy.md` 明文化 PII/敏感信息/公开范围** + `environment.md`）/ `00_context`（`context.md` 固定目标·范围·约束 + `decisions.md` 记录重大方针变更）/ `00_planning` / `01_data` / `02_work` / `03_results` / `04_docs` + `CLAUDE.md` + **强制经 `workspace.code-workspace` 打开**（否则 AI 工具历史按目录分裂）；③ **论文仓规范**（`les2feup/guidelines`）：`docs/ src/ tests/ data/ notebooks/ results/` + `LICENSE` + `.gitignore`，README **必含**「**Article Information**（标题/作者/会议/摘要/全文链接）」+ 「**Reproducing Results**」。另有**实验室级实证**（Chen, Toro-Moreno & Subramaniam, Fred Hutch）：用 GitHub 承载研究全生命周期三步 = **issues+project board 设计实验 / 版本控制记录实验与分析 / 容器化固定环境**，主张**项目一开始就采用**、并**提供可直接复制的模板仓**；其动机段落明确点出**"个体与未来的自己协作、与未来加入的实验室成员协作"**——正对应用户"逆向拆解文档给未来的自己看"。

### 16.3 辅助资产：三类归属

【A】A-86: **文献副本能否进仓，取决于"版本"而非"是否被引用"**：三类版本被区分——**Preprint**（投稿前）/ **Accepted Manuscript (AM)**（经同行评审但未排版）/ **Version of Record (VoR)**（正式发表版）；**多数出版商不允许自存档 VoR（即期刊排版后的 PDF）**，但常允许 preprint / AM；Cambridge Green OA 政策明示：**若 VoR 为 all rights reserved，则仅允许在非商业仓储共享 AM、且仅限 CC BY-NC-ND、并附 embargo**；Elsevier 的政策表区分"**作者自身可复用**"（含**纳入学位论文**、在自身新作中复用部分/图表）与"**可向他人分发**"——**前者不等于后者**；查权限的入口是 **SHERPA/RoMEO（现 Open Policy Finder）** 与"**保留你的出版协议原文**"。→ **对用户**：大量 PDF（`LGMM/LGMM 8.0/data/factor_papers/` 20 篇 + 各仓散落，共 363 个）**若属 VoR 则不可进任何公开仓**；且它们会污染 A-81 的 **Artifacts Available**（你宣称的"制品"里混着他人受版权保护的 VoR）。

【A】A-87: **文献管理的正确形态 = 外部参考管理器 + 仓内只留引用键与元数据**：Zotero 的 **stored files vs linked files** 二分（**stored** = 存进 Zotero data directory、由其托管并**自动按条目元数据重命名**、参与同步；**linked** = 只存路径、**不参与同步**、不能用于 group library），官方«**强烈推荐 stored files**»；配套生态 = **Better BibTeX**（citation key 管理 + **on item change 自动导出**，便于与 Obsidian/LaTeX 双向链接）+ **Attanger/ZotFile**（附件位置与云存储）；实践中广泛采用「**Zotero + 云盘**」（PDF 落云盘、**仓里只放 `.bib`**）。→ **对用户**：各仓 `references.bib`（`LGMM/paper/refs_v7.bib` 等）**已是正确形态**；缺的是**把 PDF 移出仓**、并让 citekey 成为唯一的跨层指针。

【A】A-88: **数据字典（codebook）是有标准格式的一等制品，且规范要求"在采集前创建"**：定义 = 描述数据集**变量及其组织方式**的结构化文档；**必含列** = 变量名 / 可读名 / 变量定义 / **数据类型** / 单位或范围或格式 / **类别编码与解码** / **派生变量的计算式与变量间关系** / **缺失值处理** / 备注；**缺失值编码规范** = 用**超出该变量可能值域**的值（如年龄用 999）、**不同缺失原因用不同码**（999=漏填 / 888=不适用 / 777=录入错误）；**变量命名规范** = 唯一、仅字母数字下划线、≤64 字符、可行时用 prefix-root-suffix；**多选问题必须拆为多个 0/1 变量**（且此类型**不存在缺失值**）；另有国际标准 **DDI-Codebook**（DDI Alliance，含 `codebook`/`codelist`/`conceptual variable` 等条目）与 FAIR Cookbook / OSF / Harvard 的实务指南；**建议在研究开始前而非事后编写，并随数据集变化更新**；**存档/投稿时须随数据集单独提交**（若无独立 codebook，则 README 中须含同等内容）。→ **对用户**：`LGMM/全因子目录索引表_AST与智能推断版.xlsx` 就是事实上的 codebook，**但它是 xlsx 且游离在项目根**——而规范要求**纯文本、与数据集同提交、列齐备**。

【A】A-89: **"笔记"应分离为两层，且各有被点名的失效模式**：PARA（Forte，按**可行动性**：Projects / Areas / Resources / Archives）× Zettelkasten（Luhmann，按**概念连接**：原子笔记 + 唯一标识 + 显式链接）被明确架构为**两个引擎**——**PARA = 执行引擎（Front Office，按可行动性组织、随项目起止频繁变化）**，**Zettelkasten = 洞察引擎（Research Library，稳定、永久、只增的原子思想网络）**；建议**物理分离、功能上以双向链接连接**（"**真正的解不是强行合并，而是架构成互补的两个引擎**"）。**两者失效模式被点名**：Zettelkasten =「**读得不够就先链接太多**」；PARA =「**有用的想法被困在文件夹里**」。相关实证：**47% 被保存的内容再也不会被打开**；而 Zettelkasten 的价值遵循 **Metcalfe 式"连接越多、系统价值越高"**。→ **对用户**：`PhD/`（申请类 11 份）、`草台班子*`、`potemkin-village-notes-en.md`、`职场经历对话记录.md` **属 Areas/Archive（长期责任与私域）而非 Projects**；`RESEARCH_MAP.canvas` / `roadmap/` 属 Zettelkasten 层——**它们与论文项目物理混层，正是 PARA 被点名的失效模式**。

【A】A-90: **笔记/知识库的仓化有成熟做法，且 `.obsidian` 有明确"该忽略什么"，同时存在硬性机密警告**：Git 方案（GitHub 私有仓）在重度笔记用户中成为首选——**免费 + 私有仓无容量上限（单文件 100 MB、仓建议 <5 GB）+ 自带版本管理 + 去中心化可迁移**，代价 = **必须处理冲突**；**Obsidian Git / Git Sync** 类插件自动 commit+push（默认 **10 分钟**间隔、`Pull on startup`），冲突以**并排 UI** 解决。**反复出现的 `.gitignore` 关键清单**：`.obsidian/workspace.json`、`workspace-mobile.json`、**插件 `data.json`**、`.trash/`——理由是「**`workspace.json` 因两端布局不同而频繁冲突**」。**机密性警告被明写**：**私有 GitHub 仓并非端到端加密**（与 Obsidian Sync 的 AES-256 E2E 不同），敏感数据须遵守机构政策；且 **community plugins 未必安全**。→ **对用户**：建议**笔记独立为单独 vault 仓**（A-83 的 polyrepo 侧）；至少在总仓中把 `.obsidian/workspace*.json` 与插件 `data.json` 列入忽略；**而"草台班子/职场经历"这类内容必须与任何可能公开的仓物理隔离**（A-85 的 `data_policy.md` 正是为此机制）。

### 16.4 映射到本仓

【B】B23（见附录 B）: **用户现状精确对应 A-83 的 `Mono-as-Poly`——有 monorepo 的形态、无 monorepo 的机制**（无一致性规范、无共享层契约、无忽略清单）；而 A-84 的判据（「**1–50 人且需要协调 + 共享数据模型/基础设施**」）**明确把结论指向 monorepo 侧**。→ **裁定方向 = 不拆分，而给这个既成 monorepo 补机制**。这同时消解 ⑨ 的"根 `CODE_WIKI.md` 定位"问题：**它作为 monorepo 顶层索引的定位是合法的，只是"名不副实"（与仓内另 6 份同名文档无法区分层级）**。

【B】B24（见附录 B）: **三类辅助资产的归属可"一次判定"，判据全部来自已调研标准**：

| 资产 | 归属裁定 | 依据 |
|---|---|---|
| **文献 PDF**（363 个，含 `data/factor_papers/` 20 篇） | **移出仓** → Zotero stored files + 云盘；仓内只留 `.bib` + DOI/citekey | A-86（VoR 不可再分发）+ A-87（stored vs linked） |
| **文献提取文本**（121 个 txt，**4 种命名**） | **派生物，不入仓**；如必须保留则统一为 `data/extracted/<citekey>.txt` 且声明可重生成 | A-87 + v1.7 的 **B20 ↔ I-5/I-6**（派生物不入真值区） |
| **数据字典**（4 个 xlsx，如 LGMM「全因子目录索引表」） | **升级为一等制品**：纯文本 `data/CODEBOOK.md`，补齐 A-88 的必含列 | A-88 |
| **笔记 / canvas / Obsidian**（3 canvas + `roadmap/` + `PhD/` 对话记录） | **物理分离为独立 vault 仓**（PARA 的 Areas/Archive 层） | A-89（双引擎物理分离）+ A-90（E2E 警告） |
| **个人 / 职业内容**（`草台班子复盘` / `草台班子观察笔记` / `职场经历对话记录` / `potemkin-village-notes-en`） | **必须与任何可公开仓物理隔离**（**优先级最高**） | A-90（私有仓非 E2E）+ A-85（`data_policy.md`） |
| **归档快照**（`LGMM_0727.rar` / `MIDAS-Granger.rar` / `files.zip` ×10） | 待裁决（见 **H14**）；**裁决前不得删除** | A-81（版本标签范式）+ 待裁 |

【B】B25（见附录 B）: **共享层的正确形态 = "一份规范 + 一个索引 + 一个红线清单"，而不是"一个杂目录"**（综合 A-83/A-84/A-85）：A-85 的 handbook 模板给出「**共享层首先是一份规范文档**」，A-84 给出「1 人 / 17 项目应走 monorepo」，故 `Working paper/` 根应从"杂层"收敛为**三个具名物**：① **`WORKSPACE.md`**——monorepo 顶层规范（命名 / 目录骨架 / 派生物隔离 / 脚本分层 / 资产归属），即 v1.7 **C-15 契约层的落点**；② **`INDEX.md`**——取代当前模糊的根 `CODE_WIKI.md`，登记 17 个项目的名称 / 状态 / 关联（A-89 的 **Index/structure note**）；③ **`data_policy.md`**——明确"哪些内容绝不外传"（A-85 的 `00_admin/data_policy.md`）。

### 16.5 裁定

【C】C-18（见附录 C）: **⑨ 与 ⑧ 两项空白已关闭，且结论是"不需要新方法论、不需要外部机制"**——共享层以 **monorepo 机制补全**（A-83/A-84 判据指向用户侧），辅助资产以 **B24 归属表**一次判定。**两项交付均为"纪律 + 三份文件"（`WORKSPACE.md` / `INDEX.md` / `data_policy.md`），零工具零依赖**，与 v1.7 的 **C-15 契约层合并为同一批**。**触发条件 = 用户指定首个迁移仓**（与 C-15 同）。

【C】C-19（见附录 C）: **隐私隔离的优先级被判定为最高——高于整洁、高于规范**。理由：`Working paper/` **同时**包含"可能要公开的研究产出"与"绝不外传的个人/职业内容"（`草台班子复盘.md` / `职场经历对话记录.md` / `potemkin-village-notes-en.md`），**一旦该目录被整体打包、上传或共享，泄露不可逆**；而 A-90 明示**私有仓并非端到端加密**。**裁定 = 先划红线，再谈规范**：`data_policy.md` 为**首件交付**，其余（命名 / 派生物 / 资产迁移）排其后。

【C】C-20（见附录 C）: **"辅助资产三层收敛"确立**（对应 A-89 的双引擎 + A-87 的存储二分）：**① 真值层**（必须入仓：论文 `.tex` / `.bib` / code / docs / **codebook**）→ **② 参考层**（不入仓、由外部工具托管：文献 PDF → Zotero + 云盘；仓内只留 DOI/citekey）→ **③ 私域层**（不入仓、物理分离：笔记 vault / 职业与个人内容 / 归档快照）。**三层之间唯一的连接是"引用键"（citekey / 相对指针），不是文件复制**——这同时从根上消灭 **`files.zip` ×10**（压缩包是"复制"的极端形态）与 **`document.tex` ×6**（无语义名的复制）。

- **[H14] `files.zip` ×10 与归档快照（`LGMM_0727.rar` / `MIDAS-Granger.rar`）的处置未裁决**——它们属"历史交付快照"（有留档价值）还是"冗余副本"（可删）？需**逐个人工判定**后才能定"归档层"规则；**裁决前不得删除**（AGENTS.md 破坏性操作纪律）。
- **[H15] 363 个 PDF 的版本构成（VoR / AM / preprint）未实测**——A-86 的判据依赖逐篇版本判定，而这**需要 DOI 查询**（且多数仓**无 git**、无历史可溯）。**逐篇判定完成前，默认按"不可再分发"处理（保守原则），不进入任何公开仓。**

## 17. 补充调研十——分步走策略、pilot 执行与裁决证据（v1.9 / v1.10 / v1.11 三批合并落地）

> **本节的由来（如实说明）**：v1.9 横幅声明「新增 §17 补充调研十」，但**该节正文此前从未写入**（文件内 §17 实为参考文献）——本批补写以兑现声明，并把参考文献顺延 **§18**（与 v1.9 横幅「参考文献顺延 §18」一致）。同时 §0 两处计数据实订正：A 90→**92**（内容早已列出 A-91/A-92）、假设区 15→**16**（H16 早已在横幅声明）。

### 17.1 分步走三步的依赖结构（v1.9，承 §16 的 C-15/C-18/C-19）

用户把落地形态拆为三步：**S1 契约层**（WORKSPACE.md / INDEX.md / data_policy.md）→ **S2 清理层**（广播至各仓执行清理）→ **S3 推理工作流层**。

**依赖结构裁定（B26）**：**S3 依赖 S1、但不依赖 S2**——推理工作流建在契约之上，不依赖"某仓已完成清理"。三条含义：

1. 前两阶段**互不阻塞**：S1 完成后 S3 即可动工，S2 可并行推进；
2. S2 的"广播"**≠ 统一重整**（C-21）——标准唯一、**执行逐仓**（C-22），须遵 C-15 逐仓迁移 + C-16 可机械检出判据；
3. 首个广播对象应选**最接近 compendium** 的仓做 pilot（C-22），以实测 H12 的契约最小充分集；**不跳过 H12/H13** 两个动仓前门禁。

社区证据：

【A】A-91: **契约先于实现、治理先于自动化（contract-first）**——Martin Fowler 数据契约「schema is law」/ Thoughtworks contract-first / DMM 5.1 治理左移；治理规则须"机器可读、可执行"方为落点。

【A】A-92: **strangler fig 增量迁移 vs big-bang 一次性重整**——后者失败率被反复证实；"可回滚的渐进位移"优于"单一 cutover"；**每个迁移步须独立可回滚**。

### 17.2 pilot 实测（v1.10，pilot 仓 = `LGMM\LGMM 8.0`）

只读跑全部迁移判据（零写入，守 H14）。**实测矩阵**：

| 判据 | 读数 | 结论 |
|---|---|---|
| 编译产物混放 | `paper/` 26（live 20 + archive 6） | 未通过 |
| 状态词入名 | 18（其中约 12 属第三方子仓 `data/co_pricing_zoo`） | 部分通过（须排除第三方） |
| Lean 单一真值 | `lean4/` **16** 专有 → 与 `LGMM_Lean/LGMM/` 同名 **13** = **12 内容一致 + 1 DIFF（`EWNLS.lean`）+ 3 仅本仓** | 双源漂移**真实存在** |
| 同名 + 声明 | 根层同名 0；**README 仍引 `MAPPING.md` 而 MANIFEST 已归档**；**MANIFEST 声明 lean=14 实测 16** | 声明冲突 + 声明漂移 |
| 脚本分层 | `code/` 根层游离 0；`code/scripts/` 七子层 | 通过 |
| 辅助资产 | `data/CODEBOOK.md` 缺失 | 待建 |

**观察项状态**：**H12**「未实测」→「**部分实测**」（**骨架层充分、判据层不足**）；**H13**「未实测」→「**数据齐备待裁决**」（真值源方向趋于 `lean4/`，**确认前不删任一份**）。

> **订正（v1.11 核实）**：pilot 早期曾把 `LGMM_Lean/` 判为"mathlib 全量（7735 `.lean`）、故双源不存在"——**该结论错误**。`LGMM_Lean/LGMM/` 是一个**真实项目根**，且与 `lean4/` 有 **13 个同名文件**。正确结论 = **双源漂移真实存在**（见上表 hash 对比）。

### 17.3 派生物清理执行实录（v1.11）

**范围与结果**（`D:\Article\Working paper\`，隔离而非删除）：

| 档 | 内容 | 条目 | 判据 |
|---|---|---:|---|
| T1 | LaTeX 中间产物（**排除 `.bbl`/`.dvi`**） | **485** 文件 | 扩展名 + `.log` 须过 TeX 内容签名 |
| T2 | `__pycache__` 39 + `.pytest_cache` 9 | **48** 目录 | — |
| T3 | `.bbl` 29 + `.dvi` 32 | **61** 文件 | 实测 git 追踪 = 0 |
| **合计** | → `D:\Article\_trash\2026-09-14-derived` | **594** 条目 / **911 文件 / 28,385,385 B** | — |

**non-TeX `.log` 的 fail-closed 处置**：111 个 `.log` 中 108 过 TeX 签名；3 个不过 → **先挂起、后单独处置**至 `D:\Article\_trash\2026-09-14-held-logs`：

| 文件 | 性质 | 判据 |
|---|---|---|
| `Coupla\results\sp100_run.log` | **脚本生成的运行日志 → 可重生成** | grep 命中 `moe_copula\experiments\run_sp100_experiments.py:46` 写该路径 |
| `CDO算子\CDO_8.1\lean\debug.log`（359 B） | **搜狗输入法垃圾，非项目产物** | 三行均为 `t_skinfilemap.cpp / SGRenderLog … sogouime` |
| `Agent_Multi\simulation_v3\results_full\run.log`（46 KB） | **一次性 `tee` 捕获，非代码写入** | `Agent_Multi` 内 grep `run.log` **0 命中**；内容为 PowerShell 回显 + 进度条 |

**git 影响核验**：五仓 **tracked-artifacts/caches = 0** → 移动产生**零 git 变更**。`git status` 报出 `LGMM 8.0` 1 项 + `CDO_8.1` 5 项 tracked 删除，经核**与本次无关**（既不在工作区、也不在隔离区，且扩展名 `.md`/`.png` 不在清理范围）→ **先前遗留的未提交删除**。

**归属核验**：594 条目全落自有 5 仓（`Working paper` 493 / `MIDAS-Granger` 46 / `LGMM 8.0` 35 / `CDO_8.1` 12 / `Coupla` 8），**无 vendored 第三方仓**。

### 17.4 A 类多版本目录裁决证据包

裁决判据四栏：**体积 / 行数 / 同名已编译 PDF / mtime**。6 目录 / 22 个 `.tex`，推荐真值 6 个：

| 目录 | `.tex` 数 | 推荐真值 | 依据 | 置信 |
|---|---:|---|---|---|
| `Joint Online Learning\v2.0` | 6 | `JOLF-2.0-academic-ctex-fixed.tex` | 最新（13:28）+ PDF + 最完整（630 行）；前 4 个 473 行系同族抖动（体积差 ≤8 B） | **需你裁定分支** |
| `MIDAS-Granger\temp` | 3 | **无**（整目录归档） | 三者全无编译 PDF + 目录名即 `temp`；正式产出为 `MIDAS v3.0\MIDAS_HM_GC_v3.tex` | 高 |
| `DL-KS-IGMM\DL-KS-IGMM_v1.0` | 3 | `document_improved.tex` | 体积/行数/mtime **三项单调递增**（29,899→30,114→34,525 B） | 高 |
| `Volsurface_SABR\SABR_v5.0` | 3 | — | **信号矛盾**：mtime 最新为 `SABR-v1`（23:16），体积/行数最大为 `sabr_wavelet_revised`（43,467 B / 625 行）；且 `SABR-v1`(560 行) > `SABR-v2`(288 行) | **需你指认** |
| `Agent_Multi\Agent_Multi_2.0` | 2 | `document_2.0.tex` | 2.7× 体积 + PDF + 晚 7 天 + 引 `references.bib` | 高 |
| `…Avellaneda–Lipkin Model\AL model_old` | 5 | `document-3.0.tex` | 最新最大（86,233 B / 1297 行）；目录已在 `old\` | 待确认 |

**B 类（结构正常，仅命名待归一，非版本问题）**：`LGMM 8.0\paper`（附录 + 主文）、`LGMM 8.0\data\enhanced_tables`（10 个 `table_*.tex`）、`MIDAS v3.0\estimation_output`（9 表）、`算子传导_1.0/_2.0`（疑似分章 A–E）。

**引用爆炸半径（改名须同步）**：`MIDAS-Granger\MIDAS v3.0\reconcile_numbers.py:24` **硬编码** `MIDAS_HM_GC_v3.tex`（功能性依赖）；`CDO_v9_Rigorous.tex` 被 4 个 `.py` 注释 + 多份 `.md`（`ARCHITECTURE.md`/`REVISION_WORKLOG.md`/`proof_breakdown_v9.md`）引用；`Fisher–Conduction Duality\{tasks,spec,plan}.md` 引 `paper_a_heston.tex`。**顺带发现 path drift**：`tasks.md:59` 写的路径 `Volsurface_Heston\Volsurface_Heston_v2.0\paper_a_heston.tex` 与实际位置 `Volsurface_Heston\paper\paper_a_heston.tex` **不符**。

### 17.5 本轮新增实测发现（四条，均为 H12 最小充分集的增补件）

1. **孤儿派生物**：`AL model_old` 有 **9 个 PDF 但只 5 个 `.tex`**——`Ito_AL_new_fixed.pdf`、`…Mode-working paperl.pdf`（**名带拼写错误 `l`**）、`UNIFIED THEOREM NUMBERING.pdf` 均**无同名源文件**。→ **最小充分集须增"孤儿检测"一件**。
2. **「版本入名」的实证危害**：`SABR-v1`(560 行) > `SABR-v2`(288 行)；`JOLF-2.0-fixed` 与 `JOLF-2.0.tex` **字节数完全相同（24,468）**却并存；`SABR_v5.0` 目录名与文件内 v1/v2 是**两套互相冲突的编号**。→ 版本号**不承载任何时序信息**，反制造"看起来有版本管理"的假象，为 **A-79**（"final 进了名字就没有词留给下一个版本"）提供**本仓实测证据**。
3. **`.log` 判据须 fail-closed + allowlist**：同为"运行日志"，`sp100_run.log` 可重生成（该清）、`run.log` 是 tee 捕获（含 provenance）、`debug.log` 是输入法垃圾（该删）——**仅靠扩展名或内容签名无法区分三者**。→ **最小充分集须增"日志白名单机制"一件**（有意保留的运行日志统一入 `logs/` 并纳入白名单，其余 `.log` 一律视为派生物）。
4. **v1.7 记载订正**：v1.7 记「`.lake/` 入库」，本轮实测 **`.lake` 与缓存零 git 追踪**（T1b 无输出）→ 该记载**证伪**。（有利面：移走不产生删除记录、无需改写历史。）

- **[H16] "广播"的推进粒度未裁决**——单仓 pilot 验证契约最小充分集（H12）后，应"gap-fill 全量翻新"还是"strangler-fig 渐进替换 17 仓"？依赖 H12 实测完成度（进展见 §17.3：pilot 判据已跑、执行实录已落档）；**登记观察项**，与 §17.6 **G-11** 同源。

### 17.6 挂起登记（承前挂起 + 本轮挂起）

**本轮"落档即挂起"**：裁决证据已完整落档，但**执行一律挂起**——真值指认与规范定稿均属内容判断，不由工具代裁。

| 编号 | 挂起项 | 阻塞原因 | 解锁条件 |
|---|---|---|---|
| **G-01** | `Joint Online Learning\v2.0` 真值指认（6 版） | 英文本 vs ctex 分支取舍属内容判断 | 用户指认 |
| **G-02** | `Volsurface_SABR\SABR_v5.0` 真值指认（3 版） | mtime 与体积信号**矛盾** | 用户指认 |
| **G-03** | `DL-KS-IGMM\DL-KS-IGMM_v1.0` 真值确认 | 推荐 `document_improved.tex` | 用户确认 |
| **G-04** | `Agent_Multi\Agent_Multi_2.0` 真值确认 | 推荐 `document_2.0.tex` | 用户确认 |
| **G-05** | `MIDAS-Granger\temp` 整目录归档 | 三者无 PDF，疑已被 `MIDAS v3.0` 取代 | 用户确认 |
| **G-06** | `AL model_old` 真值 + **4 个孤儿 PDF** | 目录已在 `old\`；孤儿 PDF 无源 | 用户确认 |
| **G-07** | 命名规则执行（含 `main.tex` 单入口约定） | 规则未写入 `WORKSPACE.md`；且 `reconcile_numbers.py` 硬编码 `.tex` 名，改名须同步 | 规则定稿 + 引用同步方案 |
| **G-08** | T4 `.lake\build`（自有 2 目录 / 依赖缓存 **7.02 GB**） | 清依赖缓存 → mathlib 需重下载或重编 | 用户按时间成本取舍 |
| **G-09** | 承 **H14** 归档快照（`LGMM_0727.rar` 2.4 GB / `MIDAS-Granger.rar`） | 留档 vs 冗余未判 | 逐个人工判定（**裁决前不得删除**） |
| **G-10** | 承 **H15** 363 个 PDF 版本构成（VoR/AM/preprint） | 需 DOI 逐篇判定 | 判定前默认**不可再分发** |
| **G-11** | 承 **H16** 广播推进粒度（gap-fill vs strangler-fig） | 依赖 H12 实测完成度 | pilot 全量判据跑完 |
| **G-12** | 承 **H13** Lean 双源真值（12 一致 + 1 DIFF `EWNLS.lean`） | 需判哪版是当前真理 | **证据齐备 · 机械可判（P-066 §17.8）**——**真值源 = `LGMM 8.0/lean4/`**（四路判据同向 + 该仓 changelog 自证）；**指认已追认**（由处置档位裁决蕴含）**· 动作未执行**（用户裁决档位 = **全部 P0 + P1 + P2**，可逐条执行清单见 **§17.9**；执行须再获显式指令）；**确认前不删任一份** |
| **G-13** | `PILOT_TASK_CARD.md` §0 与 §2.3 表述不一致 | §0 仍写「`LGMM_Lean/` 为 mathlib 全量（7735）、非第二专有源」，§2.3 已改 hash 对比 → **同文档自相矛盾** | **已订正（P-065，`PILOT_TASK_CARD` v0.4 → v0.5）**——§0 据 v0.3 实测口径改写为「双源真实存在（12 一致 + 1 DIFF + 3 仅本仓）+ 真值暂记 `undecided` + 裁决前不删任一份」；**判据与读数零改动**（性质 = 表述同步欠账） |

> **状态更新（P-071，2026-10-04）**：G-09 / G-10 / G-11 / G-12 的承项已由学术仓侧于 2026-10-03 裁决 / 满足（H14 / H15 / H16 / H13）；G-12 **P0 已满足、P1 未执行**——详见 §17.10。

**执行纪律（本轮固化）**：派生物清理**只隔离不删除**（move 至 `_trash` + 保相对路径 + 可原路回滚 + 计数守卫 + 内容签名 fail-closed），观察期无异常后再释放；此后**已由 §17.3 实测**：5 仓 tracked-artifacts = 0，故"隔离"不与版本控制冲突。

### 17.7 计数声明

本节为**实测回填 + 挂起登记**，**不新增编号断言**——方法论层面的三条增补件（孤儿检测 / 日志白名单 / 版本入名实证）均定性为 **H12 最小充分集的增补**与对 **A-79** 的本仓补证，非新断言。断言计数保持 **92A + 26B + 23C + 16H**；§0 两处陈旧计数（A 90→92、假设区 15→16）据实订正使与视图层声明一致。

> **v1.12 追加**：§18 二次核验使 **A-17 据实换源**（原引文判为疑似虚构、具体数字撤回，命题与编号保留）——**属证据替换而非新增/删除断言**，故 92A 口径不变；§0 与附录 A 的编号映射无需改动。

> **v1.13 追加**：**G-13 订正**（`PILOT_TASK_CARD.md` §0 与 §2.3/§2.8 表述同步，卡 v0.4 → v0.5）——**零新增/删除断言**（本文件断言口径不变：92A + 26B + 23C + 16H）；§17.6 挂起登记中 **G-13 状态转「已订正」**，其余 **G-01~G-12 仍挂**（皆为内容判断，等用户指认或实测完成）。

> **v1.14 追加**：**G-12 双源真值取证**（§17.8）——**零新增/删除断言**（口径不变：92A + 26B + 23C + 16H）；§17.6 中 **G-12 状态转「证据齐备·机械可判」**（真值源 = `LGMM 8.0/lean4/`），其余 **G-01~G-11 仍挂**。

> **v1.15 追加**：**完成度评估与阻塞项分类**（§17.10，P-071）——**零新增/删除断言**（口径不变：92A+26B+23C+16H）；§17.6 挂起项状态更新（G-09 / G-10 / G-11 / G-12）见 §17.10。

### 17.8 G-12 双源真值取证与指认建议（v1.14）

**缘起**：用户指令「继续处理 G-12 的双源真值指认」。G-12 原状 = 「数据齐备待裁决」、解锁条件「用户指认」。本轮对该项做**只读取证**（`D:\Article` 侧**零写入**），结论 = **该指认已由机械判据锁定，不再属"内容判断"**。

**取证对象**：`LGMM\LGMM 8.0\lean4\`（记 **A**）与 `LGMM\LGMM_Lean\LGMM\`（记 **B**）。

| # | 判据 | A = `lean4/` | B = `LGMM_Lean/LGMM/` | 指向 |
|---|---|---|---|---|
| 1 | `.lean` 文件集（排除 `.lake` 内部） | **16** | **13**（**全部**与 A 同名） | B ⊂ A，**B 零独有文件** |
| 2 | 同名对 SHA256 | — | 13 对 = **12 一致 + 1 DIFF**（`EWNLS.lean`） | 与 pilot 2026-09-13 读数**逐项一致** |
| 3 | `EWNLS.lean` 逐行包含率 | — | B 的 **629** 个非空行中 **628** 出现在 A（**99.84%**；唯一未命中 = `open …` 行的扩展形态）；A 另有 **147** 个非空行独有 | **A ⊃ B**（B 无独有文本） |
| 4 | 声明集（theorem / lemma / def / structure / instance / abbrev / axiom） | **43** | **34** | **仅 A 有 9 / 仅 B 有 0** |
| 5 | 总行数 | **902** | **725** | A 多 **177** 行 |
| 6 | `axiom` 重数（**剥块注释与行注释后精确重数**） | `EWNLS.lean` **8**；全树 **53** | `EWNLS.lean` **6** | 单文件 **+2** = 两条 Cauchy-Schwarz 公理 |
| 7 | mtime | **2026-08-01** | 2026-06-03 | A 晚 |
| 8 | 其余 12 文件 mtime | 与 B **逐文件相同**（2026-06-03 / 2026-05-31） | 同左 | B 为**拷贝**（时间戳被保留） |
| 9 | **仓内权威自证** | 根模块 `lean4/LGMM.lean` 头部「LGMM **v8.1**」+「**v9.1 Changelog（2026-08-01）**」明列实测到的 A 独有声明 **5 个**（`ewnlsHessian` / `ewnls_hessian_det_eq` / `nls_hessian_nonsingular` / 两条 Cauchy-Schwarz 公理）与公理总数 | 根模块 `LGMM_Lean/LGMM.lean` 头部「**LGMM 5.0** paper / 基于 `LGMM-5_0_final.tex`」，import **13** 模块 | **A 自证 v9.1；B 停在 v5.0 时代** |
| 10 | lake 工程三件套（A-76） | **无**（`lean-toolchain` / `lakefile.*` / `lake-manifest.json` **全缺**） | **有**——且为**全 `LGMM/` 树唯一**的 lake 工程（mathlib4 v4.20.0 缓存于其 `.lake/`） | **B 才是工程根** |
| 11 | git 覆盖 | 内层仓 `LGMM 8.0`：**471** 追踪文件、`lean4/` **16/16 已入库**（`a885468` 2026-07-17「pre-reorganization baseline」） | **零追踪**（属外层 `Working paper` 仓，该仓仅 **5** 个追踪文件、`LGMM/` 下 0 个） | 仅 A 受版本控制 |

**结论（指认）**：**内容真值源 = `LGMM 8.0/lean4/`**（工作区态 = v9.1）。判据 **1 / 3 / 4 / 9** 四路**独立同向**（文件集 ⊂、文本行 ⊂、声明集 ⊂、仓内自证版本号）；其中判据 9 由**该仓自己书写的 changelog** 命名了我们实测到的 A 独有声明与 +2 公理，判据 8 又解释了 12 个文件为何逐字节相同（拷贝保留时间戳）⇒ **非内容判断，属机械可判**。

**三条派生发现（比"选哪份"更重要）**

- **F-1 = v9.1 证明集当前不可构建**：「A 有源无工程、B 有工程无新源」——B 的根模块 `import` 面仅 **13**（**不含** v9.0 新增的 `JointDistribution` 与 `BahadurBoundary`）且其 `LGMM/` 停在 06-03 ⇒ `LGMM.lean` 头部自述的「**No `sorry` placeholders remain**」与「axiom 53」**当前无法用 `lake build` 机械复现**。这正是本仓 A-76 / B20「症状↔不变式对偶」的活样本。
- **F-2 = v9.0 / v9.1 全部改动未提交**：内层仓 HEAD `e200be9`（2026-07-23）落后于工作区；`git status` 显示 `lean4/` **4 文件已改未提交**（`BahadurBoundary.lean` / `EWNLS.lean` / `JointDistribution.lean` / `LGMM.lean`），其中 `EWNLS.lean` **+178 −1** ⇒ **一次干净克隆即丢失**。该风险**独立于、且高于**双源问题。**⚠️ 范围订正（P-066 执行期，写任务卡时跑全局 `git status` 暴露）**：本项初稿**只报 lean4 的 4 条**（当时用的是**范围限定**命令 `git status -- lean4/`），**低估了仓库整体未提交面**——实测全局 **61 条** = 24 修改 + **1 删除** + 36 未跟踪、**0 已暂存**，其中**非 lean4 共 57 条**（横跨 `paper/` 的 `.tex`/`.pdf`、`code/`、`data/`、`MANIFEST.md` / `README.md` / `RESEARCH_LOG.md`），并含一处**工作区删除**（`LGMM7_Proofs_Analysis.md`，状态 ` D`）；HEAD 之后**约 2.3 个月的产出全部未提交**（工作区最新文件 mtime = 2026-10-01）。⇒ **F-2 的性质由「4 文件级」升级为「仓库级」**；本仓处置仍以 lean4 的 4 条为**最小切口**（写进任务卡 §2.1），**其余 57 条不属该卡范围**、须另立任务卡由仓主裁决。
- **F-3 = 朴素 `grep sorry` 假阳性 10 例**：首轮以词边界全树计得 **10**，**全部**来自根模块 changelog 散文对该词的提及；**剥注释后真实 = 0**，与声明一致 ⇒ 再次实证「**朴素匹配 ≠ 语义重数**」（同族 = 本仓 P-061 的 `dc_validator` M5 假阳性）。**附带正向证据**：同批实测 `axiom` 全树 **53** 与声明**精确吻合** ⇒ 该仓的**可数声明可信**。

**处置建议（三档，按成本升序；均在 `D:\Article` 侧，属用户裁决面）**

| 档 | 动作 | 收益 | 前置 |
|---|---|---|---|
| **P0** | 提交 A 侧 4 个未提交文件（`lean4/` 的 v9.0 / v9.1 工作） | 消除 **F-2** 的丢失风险；**零改内容** | 无（建议最先做） |
| **P1** | 把 A 的 16 文件**单向同步**进 `LGMM_Lean/LGMM/`，并以 A 侧 `LGMM.lean` 替换 B 侧根模块（补 2 个 `import`） | 恢复可构建性 ⇒ 使「声明可复现」 | mathlib 缓存已在（无需重下） |
| **P2** | `LGMM_Lean/` 纳入版本控制或至少 README 标注；`.lake/` 按 A-76 ignore | **工程配置与源**（`lakefile.lean` / `lean-toolchain` / `lake-manifest.json` / 16 个源文件）获版本保护；**不含 `.lake` 本身**——按 A-76 该目录**应 ignore**，7 GB 依赖缓存靠 `lake exe cache get` 重建（**订正**：本条初稿写「7 GB 依赖缓存获版本保护」**不成立**） | 可与 P1 合并 |

**不推荐**：删任一份——B 是**唯一**承载构建配置者，A 侧无 lake 三件套；删 B 等于放弃可构建性（与 PILOT_TASK_CARD §2.3「DIFF = 0；唯一真值源 = `lean4/`」并不矛盾：该判据说的是**内容真值源**，不是**工程根**）。

**边界**：本轮**只读取证**，`D:\Article` 侧**零写入**（未提交 / 未同步 / 未删除任何文件）；**不新增编号断言**（读数以本节实测表承载，口径保持 **92A + 26B + 23C + 16H**）；**指认已追认**（由处置档位裁决蕴含，见 §17.9）**· 动作未执行**——处置动作按 P0 → P1 → P2 顺序另立批次（属学术仓侧写动作，不并入本仓批次）。

### 17.9 G-12 处置动作清单（三档 · 待执行）

**同批追加（v1.14）**：用户就 §17.8【处置建议】三档作出裁决 = **全部（P0 + P1 + P2）**。下表为**学术仓侧**可逐条执行的清单——**执行本体仍属学术仓侧写动作，不并入本仓批次**（与 §17.8 边界一致）；本仓**只出清单、不代执行**，执行须再获一次显式指令。

**前置 Ⅰ · 变量与备份（不可跳过）**（AGENTS.md 破坏性文件操作纪律：覆盖前必须备份）

```powershell
$A  = "D:\Article\Working paper\LGMM\LGMM 8.0"
$B  = "D:\Article\Working paper\LGMM\LGMM_Lean"
$BK = "D:\Article\_trash\$(Get-Date -Format 'yyyy-MM-dd-HHmm')-lgmm-lean-pre-sync"
New-Item -ItemType Directory -Force $BK | Out-Null
Copy-Item "$B\LGMM" "$BK\LGMM" -Recurse -Force
Copy-Item "$B\LGMM.lean","$B\lakefile.lean","$B\lean-toolchain","$B\lake-manifest.json" $BK -Force
```

通过门 = `$BK` 下存在 `LGMM\`（13 文件）与 4 个顶层文件。

**P0 · 提交 A 侧 4 个未提交文件**（消除 **F-2**）

```powershell
git -C $A add lean4/EWNLS.lean lean4/BahadurBoundary.lean lean4/JointDistribution.lean lean4/LGMM.lean
git -C $A commit -m "lean4: v9.0/v9.1 axiom-based formalization (P1-1 EW-NLS Hessian non-singularity)"
git -C $A status --short -- lean4/
```

通过门 = 第三条**输出为空**（`lean4/` 工作区干净）；`git -C $A log -1 --stat` 列出上述 4 文件。
回退 = `git -C $A reset --soft HEAD~1`（提交撤回，工作区内容保留）。
约束 = **不用 `git add -A`**（避免夹带未审内容）；**不 push**（推送属该仓自治，另裁）。

**P1 · A→B 单向同步 + 换根模块**（恢复可构建性）

映射口径（**结构性要点**）= A 的 `lean4/LGMM.lean` 是 **`LGMM` 模块根**（import `LGMM.*`），其余 15 个是 **`LGMM.*` 子模块** ⇒ 前者**替换** `$B\LGMM.lean`，后者**覆盖进** `$B\LGMM\`（不可把根模块放进 `LGMM\`，那样模块名会变成 `LGMM.LGMM`）。

```powershell
Get-ChildItem "$A\lean4" -File -Filter *.lean | Where-Object { $_.Name -ne 'LGMM.lean' } |
  ForEach-Object { Copy-Item $_.FullName "$B\LGMM\" -Force }
Copy-Item "$A\lean4\LGMM.lean" "$B\LGMM.lean" -Force
```

对账（**逐文件、不得抽样**）：

```powershell
$bad = @()
foreach ($f in (Get-ChildItem "$A\lean4" -File -Filter *.lean)) {
  $t = if ($f.Name -eq 'LGMM.lean') { "$B\LGMM.lean" } else { "$B\LGMM\$($f.Name)" }
  if ((Get-FileHash $f.FullName).Hash -ne (Get-FileHash $t).Hash) { $bad += $f.Name }
}
"DIFF = " + $bad.Count
(Select-String -Path "$B\LGMM.lean" -Pattern '^import LGMM\.').Count
```

构建（**F-1 的真正判据**）：

```powershell
Push-Location $B; lake build; $code = $LASTEXITCODE; Pop-Location; "lake build exit = $code"
```

通过门 = `DIFF = 0` / import 计数 **15** / `lake build` **exit 0**。
> **不表演纪律**：若本机无 `elan` / `lake` 或工具链未就绪，**如实标注「构建未执行」**——不得以「对账通过」冒充「可构建性已恢复」，那正是本节要检验的对象本身（同 PILOT_TASK_CARD §3 的判据纪律）。
回退 = `Copy-Item "$BK\LGMM" $B -Recurse -Force` + `Copy-Item "$BK\LGMM.lean" $B -Force`。

**P2 · `LGMM_Lean/` 纳入版本控制**

```powershell
if (-not (Test-Path "$B\.gitignore")) { Set-Content "$B\.gitignore" ".lake/`n*.olean`n*.ilean" -Encoding UTF8 }
git -C $B init
git -C $B add LGMM LGMM.lean lakefile.lean lean-toolchain lake-manifest.json .gitignore
git -C $B commit -m "chore: version-control LGMM Lean project (sources + lake config; .lake ignored)"
git -C $B status --short
```

通过门 = `git status --short` **输出为空**（`.lake/` 未被纳入）；`git -C $B ls-files` 计数 = 源 + 配置（**不含 `.lake` 内任何文件**）。
形态说明 = 与 `LGMM 8.0` 自身即**嵌套仓**的既成事实**同构**，且守 **A-76**（`.lake` 不入库）。
**等价替代（轻量形态）** = 仅新增 `$B\README.md`，标注「本目录为**构建工作副本**，内容真值源在 `LGMM 8.0\lean4\`」——收益仅可读性，**不产生版本保护**。
回退 = `Remove-Item "$B\.git" -Recurse -Force`（只撤版本控制，**不动任何文件**）。

**执行顺序**：P0 → P1 → P2（P0 亦可在 P1 后补做，但遗漏 P0 则 **F-2** 风险持续）。
**执行后回填**：① §17.8 结论段的「待追认」改为「**已追认**」；② 学术仓侧动作实录（做了什么 / 读数 / 未执行项如实标注）；③ 若 P1 的 `lake build` 成功 ⇒ **F-1 关闭**；若失败或未执行 ⇒ **F-1 维持开启**并附失败读数。

**落档（P-066 同批）**：本清单已**实例化为学术仓内的任务卡** `D:\Article\Working paper\LGMM\LGMM 8.0\TASK_CARD.md`（**12,021 B / UTF-8 无 BOM**）。写入方式 = 单引号 here-string + `WriteAllText`（规避 PowerShell 对反引号与 `$` 的展开）；**本仓 `Write` 工具受工作目录限制无法直达 `D:\`，故以 Shell 落盘**。卡片为**自足形态**（执行者无需外部仓上下文）：§0 前置三件（基线 / **备份** / 环境探测）→ §1 已完成的取证（读数表 + 指认结论 + 三条发现）→ §2 三档命令 + 通过门 + 回退点 → §3 **机读回填块**（JSON）+ `F1_closed` / `F2_closed` 判定口径 → §4 **九条红线** → §5 范围。**未纳入任何提交**——卡片 §2.1 明令 P0 **只提交 4 个 lean4 文件**，并禁止 `git add -A`。

**⚠️ 同批执行期发现（P-066）**：写卡时跑**全局** `git status` 暴露 **F-2 记载低估范围**——初稿用的是**范围限定**命令（`-- lean4/`），实际仓库整体未提交面 = **61 条**（非 lean4 **57 条**）⇒ 已就地订正 §17.8 F-2，并把该读数作为 **§0.1b 仓库级基线**写进卡片（含「不要扩大提交范围」的显式护栏）。**教训**：**范围限定命令的读数不等于全局读数**，报"未提交风险"时须**先声明作用域**或直接用全局读（同族 = P-064 的 P1-1「把眼估当机械重数」——同为**读数口径未声明**）。

### 17.10 完成度评估与阻塞项分类（P-071，2026-10-04 · Layer-0 · 零新增断言）

**缘起**：用户指令「分析学术推理框架完成度」→「学术框架阻塞项分类调研先落档，然后按建议顺序执行」。本批对该 feature 做**分层完成度评估 + 阻塞项三分类**，并回填本轮学术仓侧实测发现。**性质 = 评估 / 登记，不新增或删除编号断言**（口径保持 92A + 26B + 23C + 16H），读数一律来自机械扫描（声明 = 机械重数，R7）。

**完成度矩阵**（分层 × 制品维度）：

| 层 | 规范层（写定） | 实测层 | 执行层（学术仓落地） | 判定 |
|---|---|---|---|---|
| **S1 契约层** | 100%（规范 §1 尾 + 两执行卡 §1） | — | 各仓已落（**4 仓各 9 件**齐）+ **根级三件套 2026-10-04 落盘** | 补齐 |
| **S2 清理层** | 100%（六轴判据全成文） | **pilot 部分**（LGMM 8.0 只读矩阵 + 派生物隔离 **594 条目**） | 单仓 | 单点验证 |
| **S3 推理工作流** | 调研 100%、裁定为**纪律不落工具**（C-8 / C-9） | — | **0%（未建）** | 未建 |

**本轮实测发现（学术仓侧，2026-10-04，以只读为主）**：

- **F-1｜S1 / S2 已在各仓就地落档**（2026-10-02/03）：`LGMM 8.0` / `CDO_8.1` / `MIDAS-Granger` / `Volsurface_SABR` **四仓各 9 件**契约制品齐（RESULT_MAP / LINEAGE / RESEARCH_LOG / CONVENTIONS / WORKSPACE / INDEX / data_policy / MANIFEST / MANIFEST.sha256）。根级三件套原挂「回执 D2c 待裁决」（学术仓侧 agent 写入工具受各仓目录限制、无法写父目录，故降级落档于各仓内）——**本批已补齐**（见 F-4）。
- **F-2｜未决项已于 2026-10-03 裁决**（学术仓侧 `LGMM 8.0` 的 `data_policy.md §4`）：H13（`lean4/` 为唯一真值源）/ H14（归档快照原位仅登记）/ H15（`factor_papers` 31 个 PDF 判 **VoR**、不随仓发布）/ H16（**strangler-fig 渐进**）⇒ §17.6 中 **G-09 / G-10 / G-11 承项闭合**。
- **F-3｜G-12 P0 已满足**：`lean4/` 已在提交 `79cbdc7`（2026-10-03「freeze pre-audit uncommitted working tree as snapshot」）入库，`git status -- lean4/` **为空**；仓库级未提交面由 §17.8 的 **61 条降为 0**（整仓已冻结）⇒ **P0 无需动作；本批未造空提交**（守「不表演」纪律）。
- **F-4｜本批写动作（学术仓侧）**：工作区根三件套落盘——`data_policy.md`（**4,241 B**；原为 **0 字节空文件**，已备份至 `_trash\2026-10-04-s1-pre\`）/ `WORKSPACE.md`（**2,282 B**）/ `INDEX.md`（**5,322 B**，登记 **17 个项目** + 非项目显式登记）；均 **UTF-8 无 BOM**；**未 commit / 未 push**。⇒ **「回执 D2c 待裁决」关**。
- **F-5｜两处与既有记录不符（须复核）**：① 学术仓 `LGMM_Lean\LGMM\` **实测存在**（与 H13 记录「工作区内不可复现、目录不存在」**矛盾**）；② **G-12 P1 未执行**——`LGMM 8.0\lean4\` 对 `LGMM_Lean` 的 hash 对账 **DIFF/missing = 4**（`BahadurBoundary.lean`、`JointDistribution.lean` 缺失；`EWNLS.lean`、`LGMM.lean` 内容不同），而 **P1 通过门要求 DIFF = 0** ⇒ 「A 有源无工程、B 有工程无新源」的可构建性断裂**仍在**。

**阻塞项三分类**：

| 类别 | 项 | 状态 |
|---|---|---|
| **可立即做**（规范就绪、零新调研） | ① S1 根级三件套落盘（**本批已做**）② **G-12 P1**（A→B 同步 + `lake build`）③ H12 全量判据跑完 | 待指令 |
| **等裁决**（用户内容判断） | G-01 至 G-06 真值指认 / G-07 命名规则 / G-12 P1-P2 档位执行（部分已由 H13-H16 裁决覆盖） | 挂起 |
| **等触发**（懒加载 gate） | **S3 推理工作流本体**（**无触发条件定义 = 最大结构空白**）/ 回溯形式化记录（C-8）/ 环境轴重检工具化（C-10 / C-13）/ 引用核验工具化（C-11 / B14）/ blueprint（C-17）/ H2 Lean4 性价比 | 挂起 |

**建议执行顺序**：**G-12 P1**（恢复可构建性）→ **H13 记录复核订正**（F-5）→ 其余等裁决 / 等触发。

**边界**：本批 = **Layer-0 登记批**（**零代码 / 零工具改动 / 零新增 M7 样本 / 不新增或删除编号断言**，口径保持 **92A + 26B + 23C + 16H**）；本仓只做**登记**（RESEARCH / PROGRESS / CODE_WIKI / session 四处），不改任何校验器；学术仓侧写动作仅 = 根三件套落盘（F-4），**未 commit / 未 push**；H13-H16 的裁决记录在**学术仓侧**，不在本仓。

**执行追记（2026-10-04，同批，学术仓侧）**：按本批建议顺序执行两项——① **G-12 P1 已执行**：A → B 单向同步（`DIFF = 0` / `import = 15`；备份 `_trash\2026-10-04-lgmm-lean-pre-sync`）；**`lake build` 失败（exit 1）**——根因 = **Mathlib olean 缓存缺失**（`LGMM_Lean\.lake\build\lib\lean\Mathlib` 不存在，mathlib 源在未编译）⇒ **F-1 维持开启**（未以「对账通过」冒充「可构建性已恢复」）。② **H13 记录订正**：学术仓 `LGMM 8.0\data_policy.md` 新增 **§4.1 订正**（`LGMM_Lean\LGMM\` 实测存在；原「目录不存在」为当时读数），原行保留不改。⇒ **F-5 处理完毕**（不符处已在本仓 §17.10 与学术仓侧 §4.1 **双向登记**）。

## 18. 补充调研十一：外部引文二次核验（v1.12）

**缘起**：v1.1–v1.11 的 A-17 依赖一篇"微软 / UC Berkeley / 清华"论文（§7.3 原引）。本轮对该条做**独立二次核验**（时序独立于原取证轮，RULE-1 精神），目标是把"**看起来像文献**"与"**确有文献**"分开。**结论 = 原引疑似虚构，据实换源**。

### 18.1 核验方法（可复现检索式与入口）

| # | 入口 | 检索式 / 动作 | 读数 |
|---|---|---|---|
| 1 | arXiv 官方 API（`export.arxiv.org/api/query`） | `all:"Agentic AI Oversight Problem"`（精确短语） | **totalResults = 0** |
| 2 | arXiv 编号 / 题名检索 | 题名逐词组合 + 作者名组合 | 无匹配条目 |
| 3 | Semantic Scholar / DBLP | 题名检索 | **无条目** |
| 4 | MSR 官方出版物页 / 会议论文集页 | 站内题名检索 | **无匹配** |
| 5 | **具名细节反查** | ① 所谓通讯作者 Sarah Sterman；② 术语"AI brain fry" | ① 命中 **UIUC HCI 研究者**（方向为 AI 写作工具），与该"论文"无关联；② 真实出处指向 **BCG × UC Riverside** 研究，亦无关联 |
| 6 | 唯一来源追溯 | 反向查找首发链接 | 仅 **forum.gnoppix.org 论坛帖**（无任何文献链接，疑 AI 生成） |

**判定**：**疑似虚构引文（形态 III）**——一条同时具备"机构署名 + 建模方法（POMDP）+ 精确实测读数（92% / 62% / 17%）+ 主观量表（NASA-TLX）"四要素的"论文"，在任何一手索引中**零命中**，且两条具名细节**均可证伪**。

> **不可核验的线索不作证据**：核验轮另见 OpenReview 上《Scalable Oversight in Multi-Agent Systems》高度同轴，但作者栏署名非自然人，来源可信度存疑，**未纳入一手证据**；"AI brain fry" 的 HBR 出处**未取得可核验 URL**，故同样**不作 A 类证据**，仅记为"排除原引"的理由。

### 18.2 处置（据实换源，不新增/不删除断言）

| 项 | 处置 |
|---|---|
| **命题** | **保留**——"人的并行监督容量有限 ⟹ 多流并发监督失效/退化"由三条可核验来源共同支撑（§7.3 ①②③） |
| **具体数字** | **撤回**——92% / 62% / 17% 与 C≈3–5 流**不得再引用** |
| **断言编号** | **保留 A-17** → 92A 计数不变；§0 与附录 A 的编号映射无需改动 |
| **下游引用** | §10.1 的 B8 引、附录 B 的 B5 / B8 `basis` 字段**继续有效**（引用的是 A-17 的**编号与命题**，非其具体数字） |
| **参考文献** | §19 中该条**划删除线 + 标注已证伪**并存档备查；同处补三条替换来源 |

### 18.3 同轴替代一手证据（逐字）

- **①** Mitchell / Ghosh / Passi，*AI Agents Push Humans Out of the Loop*（[arXiv:2608.23642](https://arxiv.org/abs/2608.23642)，2026）：`Not only do current approaches to AI agent design impede effective human oversight, but the cognitive capacities required for it are also themselves degraded by extended use of AI systems.`
- **②** Wang & Rachev，*Operating Imperfect AI: Reliability Drift and Human Congestion*（[arXiv:2601.22295](https://arxiv.org/abs/2601.22295)，2026）：`human override capacity is scarce and congestible … we identify a critical 'Capacity Phase Transition' … beyond which no policy can maintain safety standards without causing structural system failure (infinite queues).`
- **③** Overman & Bayati，*The Oversight Game*（[arXiv:2510.26752](https://arxiv.org/abs/2510.26752)，Stanford，2025）：`passive loss of control … can arise … [from] the agent's decisions becoming too complex or numerous for humans to reliably oversee.`

**三条共同支撑的命题** = 监督容量是**稀缺且会拥塞**的资源；一旦并发决策数超出容量，监督会**相变式失效或被动退化**（而非缓慢劣化）。与本仓"per-feature 多流并存"场景（§10.1 / B8）同轴。

### 18.4 方法论收获（登记为取证纪律，不新增断言）

1. **"高保真引文形态"是幻觉的高危伪装**——机构署名 + 建模方法 + 精确百分比 + 量表名四要素齐备，却零一手来源。故**证据分级（E1-E5）须以"能否给出可解析标识符（DOI / arXiv 编号 / 稳定 URL）"为准，而非以"描述是否像论文"为准**。
2. **具名细节反查是低成本证伪手段**——一次作者身份核对 + 一次术语溯源即足以推翻整条。建议将"**至少一条具名细节须可反查**"纳入调研取证的常规动作。
3. **R7 机械对账不覆盖"引文真实性"**——§0 的 92A 计数正确、格式合规，仍可容纳一条虚构引文；**计数纪律与证据真实性是两个正交维度**（与 A-54 的"引用幻觉穿透同行评审"同族，M7 账本候选登记）。

## 19. 参考文献

- LGMM 证据链审计（用户仓库）：[外部·2026-09-10-empirical-estimator-evidence-chain.md](file:///D:/Article/Working%20paper/LGMM/LGMM%208.0/docs/audit/2026-09-10-empirical-estimator-evidence-chain.md)
- SciTeX Writer（模块化版本控制手稿 + latexdiff + revision 轮次）：https://github.com/scitex-ai/scitex-writer
- paper-template（GitHub Actions 自动编译 PDF）：https://github.com/specialpointcentral/paper-template
- Quarto（literate programming）：https://quarto.org ；knitr：https://yihui.org/knitr/
- reproducible analysis five pillars（literate 即五柱之一）：https://github.com/depaul-uni/depaul-open-science/blob/main/chapters/04-reproducible-analysis.md
- ARIS 跨模型审稿（adversarial bandit / REVIEW_STATE / AUTO_REVIEW）：https://github.com/LeoLin990405/Auto-claude-code-research-in-sleep
- PaperJury（对抗式法庭审稿 + durable ledger）：https://github.com/u7079256/paperjury
- Agentic_Paper（12 并行 reviewer agent）：https://github.com/albertogerli/Agentic_Paper
- Multimodal Peer Review Simulation（Action:Objective to-do，WWW'26）：https://arxiv.org/html/2511.10902v2
- auto-research（8 phases / 4 gates / LAB_NOTEBOOK.md）：https://github.com/0h-n0/auto-research
- eLabFTW（开源 ELN，审计防篡改）：https://github.com/elabftw/elabftw
- Open Science Framework（预注册）：https://osf.io
- Lie-algebra/Lean4 一致性 / lf-lean 类型同构验证：https://github.com/theorem-labs/lf-lean ；Lean Workbook：https://arxiv.org/html/2406.03847v3
- Zotero+LaTeX+Git 文献版本锚定：https://wenku.csdn.net/column/1dwf16jqotan
- Auto Review Loop（review-2-fix 循环 + MARK_ROUNDS）：https://lobehub.com/skills/comeonoliver-skillshub-auto-review-loop-llm
- AgentGUI（观察 + 转向长时 agent，38% 提速 / 防漂移 +34pp）：https://github.com/eth-medical-ai-lab/agent-gui ；arXiv：https://arxiv.org/abs/2607.26300
- ~~Msft/Berkeley/清华《The Agentic AI Oversight Problem》（AI brain fry / POMDP 监督容量 C≈3-5）~~ —— **v1.12 二次核验判定为疑似虚构引文（形态 III）：原引具体数字（92%/62%/17% 与 C≈3–5）一律撤回**；唯一来源（论坛帖，疑 AI 生成、无任何文献链接）存档备查：https://forum.gnoppix.org/t/study-warns-of-ai-brain-fry-as-workers-hit-cognitive-limits-overseeing-ai-agents/4876
- **（v1.12 替换 A-17 证据源）**：Mitchell / Ghosh / Passi《AI Agents Push Humans Out of the Loop》https://arxiv.org/abs/2608.23642 ；Wang & Rachev《Operating Imperfect AI: Reliability Drift and Human Congestion》https://arxiv.org/abs/2601.22295 ；Overman & Bayati《The Oversight Game》https://arxiv.org/abs/2510.26752 —— 逐字引文与核验记录见 §18
- Racc（多 agent IDE 认知设计研究，Cowan 4±1 / attention residue / info foraging / 主动微介入）：https://github.com/liu1700/racc/wiki/Cognitive-Design-Research
- Top LLM observability tools 2026（LangSmith / Langfuse / Arize Phoenix / MLflow，trace 是新的 log）：https://mlflow.org/articles/top-llm-observability-tools-in-2026-a-pro-guide/
- AutoGPT 实时进度可视化（三级事件粒度 + Dagre DAG 布局 + 颜色编码）：https://blog.csdn.net/weixin_35829279/article/details/155927006
- COCO（连续监督 / heterogeneous cross-validation / 30× 参数削减 95.1%）：https://arxiv.org/abs/2508.13815
- AWorld（Execution+Guard 双角色，System Identification 建档，防幻觉护栏）：https://arxiv.org/abs/2508.09889
- AgentGuardian（从日志学习 CFG 控制流图 + 输入约束，缓解幻觉驱动错误）：https://arxiv.org/abs/2601.10440
- ACM Guardians of the Agents（Erik Meijer，security automaton + 执行前形式证明）：https://cacm.acm.org/practice/guardians-of-the-agents/
- W3C PROV 家族（Entity/Activity/Agent + PROV-CONSTRAINTS 时序因果约束）：https://www.w3.org/TR/prov-overview/ ；PROV-O：https://www.w3.org/TR/prov-o/
- awesome-auditable-ai（201 条目；TraceElephant 17%→30% / Who&When / AgentAuditor）：https://github.com/yzhao062/awesome-auditable-ai/
- VeriFact-CoT（事实核验-反思-引用整合）：https://arxiv.org/abs/2509.05741 ；多模态事实核验（网络+文献交叉核对，-67% 幻觉）：https://arxiv.org/abs/2510.22751
- HAACS（层级 Petri 网形式化多 agent 协作，step=可再分子网）：https://arxiv.org/abs/2505.00018
- NVIDIA Deep Researcher（orchestrator-planner-researcher 层级 loop）与 artificial-agent-lab（PI+PhD investigators + knowledge_graph.jsonl）
- Magentic-One Task Ledger / Progress Ledger（Microsoft，二账本 + 五问判题 + stall counter）：https://arxiv.org/abs/2411.04468 ；模式解读：https://www.agentpatterns.ai/multi-agent/magentic-orchestration/
- Backlog.md（markdown 原生任务看板 + 终端 kanban + 三审查检查点，AI-ready）：https://www.npmjs.com/package/backlog.md ；https://github.com/MrLesk/Backlog.md
- Markdown Task Board（ad-halfspace，纯 Python stdlib + 单 HTML，依赖自动阻塞）：https://github.com/ad-halfspace/markdown-task-board
- Kanban.md（VSCode 扩展，`.kanban.md` 交互板）：https://marketplace.visualstudio.com/items?itemName=wguilherme.kanban-md ；Nullboard（单 HTML 零配置）：https://gitcode.com/GitHub_Trending/nu/nullboard
- git worktree 并行 agent 开发 + `git log --graph` fork 可视化：https://araisun.com/git-worktree-parallel-ai-codex/ ；https://github.com/spaarke-dev/spaarke/blob/master/docs/procedures/parallel-claude-sessions.md
- PowerShell FileSystemWatcher（.NET 内置，事件驱动自动抓取，零新依赖）：https://gist.github.com/mobzystems/d81b46733c1868ed916e0859d4929e2b ；https://gist.github.com/16892434/8677af78f247bfd5d3208df7ad838912 （watch-inbox.ps1）
- do-knowledge-studio 自动更新文档（`update-docs.mjs` + AUTO-START/AUTO-END 栅栏 + pre-commit/CI）：https://github.com/d-oit/do-knowledge-studio/issues/34
- ProjectOdyssey 自动计数 badge 防 drift（pre-commit）：https://github.com/HomericIntelligence/ProjectOdyssey/issues/3307
- agent_pulse（GitHub Copilot CLI 实时终端看板）：https://github.com/DUBSOpenHub/copilot-cli-agent-pulse ；cc-aio-mon（Claude Code 终端监视器，500ms 轮询）：https://github.com/iM3SK/cc-aio-mon
- Rich Live（`refresh_per_second` 自动刷新 + screen）：https://rich.readthedocs.io/en/latest/live.html ；minimal-tui（rich+tqdm stdlib 兜底）：https://www.skillmd.ai/skills/minimal-tui/

**v1.4 补充（回溯与反馈回路）**：

- Saga 模式（补偿事务 / pivot 不可回退点 / 可重试事务）：https://learn.microsoft.com/zh-cn/azure/architecture/patterns/saga ；Temporal Saga：https://docs.temporal.io/design-patterns/saga-pattern ；原始文献 Garcia-Molina & Salem (1987, SIGMOD)：https://dl.acm.org/doi/10.1145/38713.38742 ；Cloudflare Workflows 声明式补偿：https://media.aivoid.dev/pdfs/technical-case-studies_20260629153051.pdf
- durable execution（append-only 事件历史 + 重放；非确定性副作用须移出可重放控制流）：Temporal《Definitive Guide to Durable Execution》https://temporal.io/blog/what-is-durable-execution ；Temporal Event History https://docs.temporal.io/workflow-execution/event ；MS Durable Orchestrations https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-orchestrations ；AWS Step Functions 错误处理 https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html
- 非时序回溯 / backjumping / CBJ / 冲突导向学习 / thrashing：Lecoutre et al., *Artificial Intelligence* 173 (2009) 1592–1614 http://cse.unl.edu/~choueiry/Documents/Lecoutre-LastConflictAIJ-2009.pdf ；Russell & Norvig Ch.5 backjumping 讲义 http://courses.cs.umbc.edu/671/fall12/notes/06/06.ppt.pdf ；CDCL 与非时序回溯实践 https://github.com/github/gh-aw/discussions/40780
- 内容寻址重跑判据 + mtime 双向失效（phantom / missed re-run）：OxyMake https://arxiv.org/html/2606.20989v2 ；DANTE（content-addressed 15-stage DAG，含 Snakemake/Nextflow 对照）https://arxiv.org/html/2609.08695v1 ；数据版本化与溯源（DVC/DataLad）https://matforge.org/reproducibility-workflows-beyond-containers-data-versioning-and-provenance-tracking/
- prospective vs retrospective provenance：Freire & Chirigati, *IEEE DEBULL* 2018 http://sites.computer.org/debull/A18mar/p15.pdf
- R-LAM（reproducibility-constrained LAM：action schema + 确定性执行 + provenance + replay/forking + failure handling）https://arxiv.org/html/2601.09749v1
- ToolMaze（动态重规划基准：扰动 2×2 / 隐式语义失败 PRR −37% / futile trial-and-error / 容错 scaling 慢 3.66×）https://arxiv.org/html/2606.05806v1
- BEAP-Agent（DFS 建模 + 长程多级状态回溯）https://arxiv.org/html/2601.21352v1
- 回溯式规划综述（MCTS/LATS/SWE-Search + 四类失败模式 + replanning loop）https://zylos.ai/research/2026-05-15-ai-agent-planning-backtracking-adaptive-replanning/ ；Loop Engineering Codex（FR-1~FR-9 工程证据库：durable execution / saga / 幂等）https://github.com/brennhill/looprails/blob/main/codex-loops.md
- 闭环多轮规划（错误归因 + 定位补丁点 + 最小关键步骤回退）：https://ashpress.org/index.php/jcts/article/download/269/219/447
- 复查点/时间旅行（replay 与 fork 的工程实现参照）：LangGraph time-travel https://docs.langchain.com/oss/python/langgraph/use-time-travel ；Checkpointers https://docs.langchain.com/oss/python/langgraph/checkpointers
- 返修轮次语义（major/minor、返原审、轮次上限）：https://www.alfredscholar.com/blog/what-to-expect-from-peer-review ；MDPI 编辑流程（最多两轮大修）https://www.mdpi.com/editorial_process ；跨轮审稿期望 R0-R3 / "early tolerance is not forgiveness"：Dwivedi et al., *J. Global Marketing* 39(1):3–17 (2026) https://www.tandfonline.com/doi/full/10.1080/08911762.2026.2623400
- HARKing（三型 CHARKing/SHARKing/THARKing）+ researcher degrees of freedom：https://www.datacamp.com/blog/harking ；预注册与 Registered Reports（UKRN Primer）https://eprints.whiterose.ac.uk/169948/1/UKRN%20Primer%20-%20Pre-registration%20and%20Registered%20Reports.pdf ；COS Registered Reports（in-principle acceptance）https://www.cos.io/initiatives/registered-reports ；preregistration 与 garden of forking paths https://lrissman03.github.io/experimentology/011-prereg.html
- 负结果规模与处置（10–30% 成功率 / 82% vs 14% / negative ≠ useless）：https://github.com/weisberg/knowledge_base_public/wiki/03.-The-Role-of-Null-Results/101dae170ae78e38f5dd92f967af5e9f9ff1715c ；Emborg, *Brain Res Bull* 192:203–207 (2022) https://pmc.ncbi.nlm.nih.gov/articles/PMC9891652/

**v1.5 补充（盲区扫描五轴）**：

- living systematic review（预设更新触发 / 三分类结局 / 终止重评估）：Cochrane Handbook Ch.22「Prospective approaches to accumulating evidence」https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-22 ；Cochrane 更新提案决策框架 https://documentation.cochrane.org/emkb/editorial-manager-for-authors/new-and-returning-authors/update-an-existing-review/decision-frameworkfor-update-proposals ；F1000Research  Living Systematic Review 作者指南 https://f1000research.com/for-authors/article-guidelines/living-systematic-reviews ；Butler et al., *J Clin Epidemiol* 2024（30 次检索更新 + 3 次全量更新的实操复盘）https://pmc.ncbi.nlm.nih.gov/articles/PMC12018299/
- reference rot（link rot vs content drift）与其量级：Klein et al., *PLoS ONE* 9(12):e115253 (2014)「Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot」https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253 ；Ott, *JSLS* 26(1):e2021.00082 (2022)「Reference Hygiene and Death on the Internet」（95 篇 / 2,424 条引用，14.7% 不可检索；含 9–25% 误引的历史实证）https://pdfs.semanticscholar.org/2d13/643bd7a5f985e74740c9a7e0d56f14c470b6.pdf ；link rot 综述（各研究半衰期与永久失效比例）https://en.wikipedia.org/wiki/Link_rot
- 撤稿核验（Retraction Watch >63,000 条；撤稿后引用提及率 <5%）与工具链：Retraction Watch https://retractionwatch.com/ ；citecheck（Crossref/OpenAlex 存在性 + 撤稿状态，**CI 退出码 0/1/2**）https://github.com/tobiasosDev/citecheck ；RWCheck https://github.com/khan-lab/rwcheck ；CiteGuard（retracted/corrected/EoC/hijacked-journal 非二值化）https://github.com/lonexreb/cite-guard ；retraction-watch-mcp（整篇 PDF/DOCX/LaTeX 一次性筛查）https://github.com/handsomezr-netizen/retraction-watch-mcp
- AI 使用披露（AI 不得署名 + 各社披露位置差异）与**政策效力实证**：He & Bu, arXiv:2512.06705「Academic Journals' AI Policies Fail to Curb the Surge in AI-assisted Academic Writing」（5,114 期刊 / 523 万论文；70% 有政策；75k 篇仅 76 篇 ~0.1% 披露）https://arxiv.org/pdf/2512.06705v1 ；2026 期刊 AI 政策对照（Nature/Cell/Science/Elsevier/Wiley/IEEE/PLOS 的披露位置差异）https://manusights.com/blog/journal-ai-policies-2026
- AI 引用幻觉的规模与穿透力：Editage「What Are AI Hallucinations in Research」（伪造率 18%–69% 区间汇总表）https://www.editage.com/blog/what-are-ai-hallucinations-in-research-causes-examples-and-risks/ ；GPTZero 对 NeurIPS 2025 的审查报道（4,841 篇接受论文 / 53 篇含 ≥100 条幻觉引用；港大 61 条中 20 条伪造）https://manuscriptlab.com/blog/why-chatgpt-cant-pass-peer-review-and-why-you-still-need-a-human-editor/
- 重复发表 / 文本回收 / 香肠切片的定义与处置梯度：COPE 立场「Handling duplicated or redundant content (salami slicing)」https://publicationethics.org/guidance/cope-position/handling-duplicated-or-redundant-content-salami-slicing ；COPE/BMC Text recycling guidelines https://publicationethics.org/guidance/endorsed-guidance/text-recycling-guidelines-editors ；COPE 案例分析「Self-plagiarism and suspected salami publishing」https://publicationethics.org/news-opinion/self-plagiarism-and-suspected-salami-publishing
- 报告规范 / 可复现性清单（必填、缺则拒稿）：NeurIPS 2026 Paper Checklist（~15–16 项全清单与答法）https://www.typetex.app/templates/neurips/checklist ；ML Reproducibility Checklist（前身）https://arxiv.org/abs/2003.12206 ；NeurIPS 2026 格式说明（checklist 不计入 9 页）https://cn.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc.pdf
- scope freeze / scope lock 双层冻结与例外判据：HP COMPASS 大型项目实证（Kendrick & Blickle, PMI 2006）https://www.pmi.org/learning/library/catch-wave-information-technology-projects-8003 ；scope creep 与 feature freeze / MoSCoW 策略 https://whennotesfly.com/work-skills/project-management/scope-creep-explained ；学位论文的范围冻结与 parking lot + 决策日志（Issue/Decision/Rationale）https://completed.blog/negotiating-scope-for-a-manageable-completed-thesis-assignment/
- escalation of commitment / sunk cost / kill criteria：Buxton & Rivers（Staw 1976 与 Arkes & Blumer 1985 的综述与实验复现，「90% 完成也可被叫停」）http://na-businesspress.homestead.com/JAF/BuxtonM_Web14_5_.pdf ；kill criteria（预承诺 + 事前验尸 + stop-loss + **renegotiation trap**）https://www.howtothink.ai/learn/kill-criteria ；PMI「The critical point—the psychology of project termination」（sunk cost / self-justification / project completion / optimism bias 四因）https://www.pmi.org/learning/library/project-failure-optimism-business-benefit-investigated-5808 ；Heath & Petersen「Premature De-escalation in Response to Failed Investment」（**过早放弃**的反向风险）https://www.kellogg.northwestern.edu/faculty/petersen/htm/papers/chip.pdf

**v1.6 补充（环境轴 B/C 层细化 + 机会窗口 + 零依赖半自动形态）**：

- 多重独立发现（Merton "multiples"）与被抢先的职业风险量级：Garfield《Multiple Independent Discovery & Creativity in Science》（Hagstrom 1974 调查 **1,718 人**：46.2% 被抢先 1–2 次 + 16.4% ≥3 次；Gaston 1971 调查 **203 名**英国高能物理学家：38% 一次 + 26% 多次）https://garfield.library.upenn.edu/essays/v4p660y1979-80.pdf
- 被抢先的实际代价（可量化、且被主观高估）：Hill & Stein 基于 Protein Data Bank 追踪 **1,630 场竞赛**——首发 **58** : 次发 **42**（100 次引用份额）；次发仅低 2.5% 发表概率但趋向低影响力期刊；**915 名**结构生物学家预期为 **71:29**；机构地位反转惩罚——Callaway, *Nature* News https://media.nature.com/original/magazine-assets/d41586-019-03648-4/d41586-019-03648-4.pdf ；中文综述（*J. Political Economy* 发表；次发进十大刊可能性 −20%、当年成热门论文可能性 −24%）https://m.thepaper.cn/newsDetail_forward_30090230
- 预印本 = 时间戳优先级声明 + 时序策略与双刃：Ginsparg《Preprint Déjà Vu: an FAQ》（arXiv postings are accepted as **date-stamped and citable priority claims**）https://arxiv.org/pdf/1706.04188v1 ；Mishkin et al.《ArXiving Before Submission Helps Everyone》（**10k Monte-Carlo** 模拟抢先概率；"等 3–6 个月"实为"等 1–3 年"）https://arxiv.org/pdf/2010.05365 ；arXiv 使用策略（时间戳不可篡改 + 反面代价：被审稿人质疑 novelty + 去匿名化）https://blog.csdn.net/AladdinEdu/article/details/156982968 ；发布时间窗（投稿后 1–2 周、**绝不在投稿同日**）https://github.com/serre-ai/research/blob/main/docs/PUBLISHING.md ；预印本 DOI/时间戳 https://www.editage.us/blog/what-are-preprints/
- desk reject 与 novelty（首要过滤器 + 编辑交叉比对）：Zerfu, ECRlife（**30–70%** desk reject；**"lack of novelty" 占 51%**）https://ecrlife.org/why-desk-rejections-happen/amp/ ；六大原因与 40–60% / 60–90% 分档 https://m.sohu.com/a/1061333250_122917150/ ；Editage 投稿前清单 https://www.editage.com/insights/top-5-reasons-for-desk-rejection-and-simple-solutions-for-authors ；定义与耗时（2–14 天）https://www.donotedit.com/why-was-my-paper-desk-rejected-within-48-hours/ ；编辑交叉比对本刊近期发表 https://publearnhub.com/desk-rejection-explained/
- NeurIPS 2014 双委员会实验（原始读数）：Lawrence 讲义（170 篇双审 / **43/166 = 25.9% 不一致** / **accept precision 0.495** / reject precision 0.175 / agreed accept rate 0.218；随机基线 37.5% & 25%）https://inverseprobability.com/talks/lawrence-peer15/peer-review-and-the-nips-experiment.html
- NeurIPS 2014 重访（主观性定位 + 不对称）：Cortes & Lawrence, arXiv:2109.09774（**50% 评分方差源于主观因素**；被接收论文评分与引用**无相关**、被拒论文评分与引用**有相关** → 「善识别差论文、不善识别好论文」）https://arxiv.org/pdf/2109.09774 ；中文解读 https://m.leiphone.com/category/academic/w28F9tN681zoFE1E.html
- NeurIPS 2021 复现（规模扩大一个数量级后仍稳定）：官方博客（**882 篇**重复送审 / **23.0% 不一致** / spotlight **13/25 与 13/23** 被另一委员会拒 / 「没有证据表明随规模变大而更噪或更不噪」）https://blog.neurips.cc/2021/12/08/the-neurips-2021-consistency-experiment/ ；Lawrence 复访讲义 https://inverseprobability.com/slides/2024-05-22-the-neurips-experiment-iwcv.slides.html
- 风向/主题漂移的可测量性与信号：Chumachenko, *PLoS ONE* 20(7):e0327793 (2025)（NVI 距离 + MST；概念漂移集中于时间局部 hub）https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0327793 ；趋势提前检出框架（最多 **18 个月**、precision > 0.89）https://ijsret.com/wp-content/uploads/IJSRET_V11_issue4_285.pdf ；语义漂移分析（情报学报 2025）https://qbxb.istic.ac.cn/EN/10.3772/j.issn.1000-0135.2025.10.006 ；实务信号（术语漂移 / 期刊专题 / 领军者转向）https://www.wispaper.ai/en/faq/how-to-filter-citations-to-identify-trends
- 数据开放政策（机会 + 护城河消失同源）：NIH DMS Policy 总览（**2023-01-25 生效**；须提交 DMS Plan，否则不予受理）https://grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/policy-overview ；写作指南（FAIR；「reuse hard-to-generate data」）https://sharing.nih.gov/data-management-and-sharing-policy/planning-and-budgeting-for-data-management-and-sharing/writing-a-data-management-and-sharing-plan ；2026 新格式页 https://grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/writing-dms-plan ；RFI（OSTP 2022 备忘录）https://grants.nih.gov/grants/guide/notice-files/NOT-OD-23-091.html ；机构速览（2 页 Plan / 共享不晚于发表 / 最低保存 3 年）https://research.columbia.edu/sites/default/files/content/EVPR/October_2022_Town_Hall_Slides.pdf
- 技术潮流/危机把「快」变标准：COVID 预印本占比（一度近 **40%**）与转化率 https://www.medrxiv.org/content/10.1101/2020.09.04.20188771v3.full.pdf ；Europe PMC 预印本索引 https://pmc.ncbi.nlm.nih.gov/articles/PMC11426508/ ；bioRxiv **2 天** / medRxiv **4 天** vs 传统期刊 **~125 天** https://pmc.ncbi.nlm.nih.gov/articles/PMC7518906/ ；钟南山团队预印本案例 https://blog.sciencenet.cn/blog-3516770-1508133.html
- 告警 / 现状知悉（current awareness）与规模：Paper Digest 指南（**3.3M 篇/年**；arXiv 2026 累计超 **300 万**、月增 **>15,000**；天体物理子领域约 **70 篇/天**；Scholar 三类告警 / PubMed MeSH 检索告警 / arXiv·bioRxiv·medRxiv 邮件与 RSS / 期刊 TOC / RSS 阅读器）https://www.paperdigest.org/research-workflow/how-to-keep-up-with-latest-research.html ；Stanford 图书馆告警设置指南 https://ell-core.stanford.edu/ell_documentation/tools/paper_alerts/ ；Google Scholar 帮助（告警/排序/操作符）https://scholar.google.com/intl/es/scholar/help.html ；告警系统局限（覆盖不穷尽、时序不一致）https://pagecrawl.io/blog/academic-journal-paper-monitoring-alerts
- 「人抓-工具记」零依赖先例与节奏分层：scholar-alert-reader-skill（接收 Scholar Alert / RSS / BibTeX·RIS / 网页 → 本地解析 + 去重 + 可解释打分 → Review Workspace 交互筛选 → 本地文献库，可选导出 Zotero/Obsidian）https://github.com/RunningXinLiu/scholar-alert-reader-skill ；日/周/季三层工作流（daily literature check → weekly review → quarterly strategic assessment）https://pagecrawl.io/blog/academic-journal-paper-monitoring-alerts

**v1.7 补充（论文仓实测扫描与流程规范化）**：

- Research Compendium（三原则：约定目录结构 / 数据-方法-产出分离 / 环境指定）：Marwick, Boettiger & Mullen (2018) https://doi.org/10.7287/peerj.preprints.3192v2 ；The Turing Way「Research Compendia」专章（含 Basic / Executable 两档与 checklist）https://book.the-turing-way.org/reproducible-research/compendia/ ；NCEAS 课程「Reproducibility and Provenance」（compendium 定义 + 可复现四要素 + Trisovic 2022 仅 26% R 文件可直接运行）https://learning.nceas.ucsb.edu/2023-02-arctic/reproducibility-and-provenance.html ；Nüst, Boettiger & Marwick《How to Read a Research Compendium》（读者视角约定，扩展 Keshav 三遍读法）https://ar5iv.labs.arxiv.org/html/1806.09525 ；工具 `rrtools`（0. Git 管理目录 → 模板 → 环境隔离 → CI，并明示"不要把这些一次性设置函数存成项目里的脚本"）https://github.com/benmarwick/rrtools ；实例仓（`analysis/` + `renv/` + `Dockerfile` + `LICENSE` 分层）https://github.com/benmarwick/web-of-science-archaeology
- RO-Crate（机器可读打包的最小充分条件）：规范首页与结构（Metadata Document **MUST** 名为 `ro-crate-metadata.json`；Attached vs Detached）https://www.researchobject.org/ro-crate/specification/1.2/structure.html ；1.1 规范 PDF（2020-10-30 发布，Recommendation 级）https://zenodo.org/record/4031327/files/ro-crate-1.1.0.pdf ；Goble & Soiland-Reyes 导引（"just enough linked data" + 开发者友好 + RO-Crate Profiles）https://www.rd-alliance.org/wp-content/uploads/2024/05/2021-02-25-ro-crate-fdo-FINAL.pdf ；Dublin Core MSI 条目（采用者：WorkflowHub / LDaCA / OME-OMERO / M@TE / HUN-REN ARP）https://msi.dublincore.org/standards/ro-crate/ ；JSON-LD 附录（@context 与 @graph 最小示例）https://www.researchobject.org/ro-crate/specification/1.1/appendix/jsonld.html
- Lean 项目布局与 `.lake` 的官方立场：Lake Build System 教程（`lake new myproject math` 直接给 mathlib+lint+CI；workspace 布局；**"`.lake` … this folder is typically gitignored"**；**TOML 为当前默认**；依赖须钉 tag 而非 `main`）https://lean4.dev/language/projects/lake ；官方参考 21.1 Lake（workspace 典型布局逐项：`lean-toolchain` / `lakefile.toml|lean` / `lake-manifest.json` / `.lake/`）https://lean-lang.org/doc/reference/4.19.0-rc2/Build-Tools-and-Distribution/Lake/ ；leanprover「Lean projects」（"一个 Lean project 不只是你命名为 My Lean stuff 的文件夹"）https://leanprover-community.github.io/install/project.html
- Lean blueprint（大型形式化的"地图"）：**LeanArchitect**（arXiv:2601.22554；点明 既有工作流两根本局限 = ① blueprint 信息在 LaTeX 与 Lean 之间**重复** → 维护开销与**漂移** ② 缺乏 AI 集成；解法 = 注解内联 + **自动推断依赖**（递归遍历声明所用常量）与**证明状态**（检查 `sorry`）+ 导出同步 LaTeX）https://arxiv.org/pdf/2601.22554v1 ；**BlueprintRepair**（arXiv:2607.28110；类型化局部编辑十操作，操作须**指名被编辑节点**故目标定理不可偷换；每解一状态成本 patch 1.30× / rewrite 2.06×）https://arxiv.org/html/2607.28110v1 ；de Moura 2026 Paris（Verso Blueprint；FLT 50+ 贡献者与 sphere packing 级项目"需要有地图"）https://leodemoura.github.io/static/paris2026/ ；AI4Math 讲义（"blueprint as project memory"：链接人类证明计划 / Lean 声明 / 依赖图 / agent 任务队列）https://math-xmum.github.io/ai4math/week05/week05-notes.pdf ；**LeanMarathon**（arXiv:2606.05400，"blueprint as the system of record"，四契约化 agent）https://arxiv.org/html/2606.05400
- LaTeX 仓库卫生（成文黑名单 + 工具 + 真实危害）：官方/toptal gitignore 的 LaTeX 段（`*.aux|*.lof|*.lot|*.fls|*.toc|*.dvi|*.bbl|*.bcf|*.blg|*.run.xml|*.fdb_latexmk|*.synctex.gz…`）http://raw.githubusercontent.com/dcpetty/first/refs/heads/main/.gitignore ；三招整洁工作流（VS Code `latex-workshop.latex.outDir` → `out/` + `autoClean.run: onBuilt`；`clean-tex` 脚本；`.gitignore` 黑名单；`latexmk -pdf/-pvc`）https://ruizhou03.com/research/latex/latex-clean-workflow ；Git for LaTeX 完整指南（黑名单 + one sentence per line + 提交纪律 + 分支策略）https://www.thetapad.com/blog/latex-git-workflows-productivity ；**陈旧派生物的三类真实危害**（`.olignore` 提案：① 服务端写不出自己的 `thesis.aux` 致编译失败 ② 用**陈旧 `.bbl`** 致**参考文献错误** ③ 协作者看到数十个二进制产物；三层 ignore 设计）https://github.com/aloth/olcli/issues/19 ；跨平台 LaTeX 工作区套件（严格 gitignore 过滤 20+ 类残留 + build 引擎封装）https://github.com/autentisitet/latex-devenv
- 文件命名（跨标准共识 + 代价量化 + "final 是谎言"）：实验室命名指南（**73% 研究数据重复事件直接源于命名不一致/歧义**；**89% 研究者每周至少浪费 1 小时**找文件；"若一个文件无法仅从名字被确信识别，该名字已经失败"）https://www.verbalexperiment.com/blog/file-naming-conventions ；10,000 文件名分析（**73% 含至少一项"生产力杀手"模式**；41% 日期格式不一致 / 34% 版本指示模糊；不一致日期格式使检索慢 **34%**）https://www.renamer.ai/insights/10000-file-names-analysis-productivity-patterns ；ISO 8601 五规则与模板（**字母序=时序** 是唯一跨 OS/语言成立的格式；连字符分词 / 下划线分字段；禁用 `< > : " / \ | ? *` 与 Windows 保留名；<70 字符）https://filesdesk.app/blog/file-naming-conventions ；**"final 是谎言"四类失效**（① 日期会撒谎（复制/转发破坏修改时间）② "final" 一旦进名字就没有词留给下一个版本 ③ 首字母归属被破坏 ④ **文件名被当 changelog 用**（"Clean and Tracked"、"as of 13 Nov"））https://inn.law/en/perspectives/file-naming-convention/ ；咨询业版本控制（**单一主文件 + 明确所有权 + 显式版本标签 + 检入检出协议**；"FinalDeck / _v2 / _FINAL / _FINAL_v2" 不传达任何确定性的实证）https://poesius.com/blog/version-control-consulting-deliverables
- 研究制品归档与引用（制度已成型）：ACM《Artifact Review and Badging》v1.1（2020-08-24；三类**相互独立**徽章 Artifacts Available / Evaluated / Results Validated；术语经 NISO 建议后**互换**：Reproducibility = 不同团队 + 同装置 + **作者制品**，Replicability = 不同团队 + 不同装置 + 独立制品）https://www.acm.org/publications/policies/artifact-review-and-badging-current ；制品处理流程（**"such as Zenodo but not GitHub"**；**"promises of future availability are not acceptable"**；Data-Availability Statement 置于参考文献前；**不要用 "always latest" 的 DOI**，FigShare 用 `.v1`；**版本标签范式** `OOPSLA-2025-R1-submission / -camera-ready / -AEC-submission / -AEC-revision / -AEC-final`）https://www.conference-publishing.com/ProcedureArtifacts.html ；SOSP 2026 badges（三种徽章组合 + 每徽章 checklist：长存储 + 不可变 + CC-BY/MIT 许可 + 引用论文的 README）https://sysartifacts.github.io/sosp2026/badges ；FSE'25 教程（AE 历史与"制品缺陷是复现失败根因之一"）https://www.sosy-lab.org/research/prs/2025-06-26_FSE25-Tutorial-Artifacts_Dirk_Stefan.pdf ；ACM CCS 2025 CFP（"a scientific paper consists of a constellation of artifacts…"）https://www.sigsac.org/ccs/CCS2025/call-for-artifacts/
- 文档组织（按用户意图而非受众）：Diátaxis 官网（四模式：tutorials / how-to / reference / explanation；"文档本身应围绕这些需求的结构来组织"；采用者 Python / Cloudflare / Canonical / Django / Gatsby）https://diataxis.fr/ ；**受众分组失效的实证**（ADR 0004：按 `development/ operational/ design/ architecture/` 分组会使每页同时是 reference + how-to + explanation，"读者分不清自己在读哪一种"，且"为哪一种都没优化"；**最大可读性收益来自"禁止混模式"这条硬规则本身**）https://github.com/alexherrero/agentic-harness/wiki/0004-diataxis-documentation-spec/7e0c1ce4668ef36f81a75abaebc4f660e0bb079e ；四模式规则与反模式清单（含 tutorial/how-to/reference/explanation 各自的语言模式与 anti-patterns）https://github.com/grootgordon/docs/blob/main/DIATAXIS.md

**v1.8 补充（共享层与辅助资产归属）**：

- monorepo / polyrepo / hybrid 三元结构（含 **Poly-as-Mono** 与 **Mono-as-Poly** 两混合变体；该主题学术研究不足）：Brousse, *The Issue of Monorepo and Polyrepo In Large Enterprises*, Programming '19 (ACM) https://dl.acm.org/doi/pdf/10.1145/3328433.3328435
- monorepo vs polyrepo 的双向代价与**规模判据**（Meta 巨型 monorepo vs AWS 千仓；15 仓迁 1 仓；「**Monorepo wins when: Team size is 1-50 engineers and everyone needs to coordinate; Services share data models, auth, and infrastructure**」；polyrepo「Discoverability is terrible」）：Managing Monorepos at Scale — Lessons from Meta, AWS, and a 15-Repo Migration https://dev.to/logical_bytes/managing-monorepos-at-scale-lessons-from-meta-aws-and-a-15-repo-migration-o84 ；结构对照表 https://velog.io/@shjk0531/%EB%AA%A8%EB%85%B8%EB%A0%88%ED%8F%ACMonorepo-%EA%B5%AC%EC%A1%B0 ；前端工程化与 Monorepo https://blog.csdn.net/2402_88266590/article/details/162029088
- 研究组 handbook 模板（**"共享层首先是一份规范，而不是一个目录"**；compendium 结构 / 命名（编号等宽补零、日期 ISO 置首、避免空格与大小写）/ 文件格式 / 共享存储位置；README 最小三要素）：cct-datascience/group-handbook-template `research-best-practices.qmd` https://github.com/cct-datascience/group-handbook-template/blob/main/research-best-practices.qmd
- 项目模板仓（`00_admin/data_policy.md`（**PII / 敏感信息 / 公开范围**）+ `environment.md` / `00_context/context.md` + `decisions.md` / 强制经 `workspace.code-workspace` 打开以免 AI 历史分裂）：ggszk-lab/research-template https://github.com/ggszk-lab/research-template
- 论文仓结构规范（`docs/ src/ tests/ data/ notebooks/ results/` + LICENSE + `.gitignore`；README 必含 **Article Information**（标题/作者/会议/摘要/全文链接）+ **Reproducing Results**）：les2feup/guidelines https://github.com/les2feup/guidelines
- GitHub 作为实验室研究平台（Fred Hutch 实证三步：issues+project board 设计 / 版本控制记录 / 容器化环境；**"个体与未来的自己协作、与未来加入的成员协作"**；提供可直接复制的模板仓）：Chen, Toro-Moreno & Subramaniam https://pmc.ncbi.nlm.nih.gov/articles/PMC11844616/pdf/nihpp-2408.09344v2.pdf
- 数据管理与项目组织（`02_literature/`（论文·笔记·参考文献）/ `03_data/`（raw 只读 / processed / **metadata 含 codebook**）/ `04_analysis/` / `05_outputs/`；命名约定；3-2-1 备份；敏感数据）：Introduction to Data Management（Schweinberger）https://ladal.edu.au/tutorials/datamanage/datamanage.html
- **文献版本三分与自存档权限**：UBC cIRcle 作者指南（**Preprint / Post-print / Published** 三分；**多数出版商不允许自存档最终发表版**；SHERPA/RoMEO 查权限；保留出版协议原文）https://wiki.ubc.ca/images/archive/f/fe/20180213173701!CopyrightcIRcle_AuthorsGuide.pdf ；Can I share my published article（取决于协议 / 保留权利 / **版本** / 存放地 / embargo；**"The publisher PDF is not always the version you can share"**；Open Policy Finder）https://libraryhelp.mtroyal.ca/copyright/faq/212956 ；Elsevier 版权页（**作者自身复用权 ≠ 向他人分发权**）https://www.elsevier.com/en-in/about/policies-and-standards/copyright ；Cambridge Green OA（VoR 保留全部权利时，仅允许非商业仓储共享 **AM**、仅限 CC BY-NC-ND、附 6 个月 embargo；商业仓储与社交媒体禁止）https://www.cambridge.org/core/open-research/green-open-access-policy-for-journals
- Zotero 附件管理（**stored files vs linked files**；官方强推 stored；自动按元数据重命名；linked 不参与同步、不能用于 group library）：Zotero — Adding Files https://www.zotero.org/support/attaching_files ；最佳实践（Zotero + ZotFile + 云盘；`%a_%t_%y` 重命名）https://www.nrel.colostate.edu/set-up-best-reference-manager ；设置指南（**Better BibTeX** citation key + on item change 自动导出；Attanger 附件管理；与 Obsidian 双向链接）https://research-memex.org/docs/implementation/foundational-setup/zotero-setup-guide
- **codebook / 数据字典**：Amsterdam UMC 质量手册 Codebook v4.0（必含列：条目/编号/变量名/类型/可能值/编码含缺失值；**缺失值编码须超出值域**（9/999）且**不同缺失原因用不同码**；变量命名唯一、仅字母数字下划线、≤64 字符、prefix-root-suffix；**多选须拆为多个 0/1 变量**）https://aph-qualityhandbook.org/media/tthbhp21/codebook.pdf ；Codebook or data dictionary（必含列清单；**无独立 codebook 时 README 须含同等内容**；**随数据集一并提交**；缺失值编码建议 NA/999 并跨数据集统一）https://dataverse.lv/en/code-book/ ；Creating Data Dictionaries for Researchers（OSF / FAIR Cookbook / Harvard 来源；**"Create a data dictionary at the beginning of a project rather than retrospectively"**；核心组件表）https://github.com/javieraatenas-pixel/testOSC/wiki/4.4--Creating-Data-Dictionaries-for-Researchers ；DDI Alliance Glossary（`codebook` / `codelist` / `conceptual variable` 定义；**DDI-Codebook 标准**）https://ddialliance.org/glossary
- **PARA × Zettelkasten 双引擎**：The Unified Vault（**PARA = 执行引擎 / Front Office**（按可行动性、随项目起止变动）；**Zettelkasten = 洞察引擎 / Research Library**（稳定、永久、只增）；**"真正的解不是强行合并，而是架构成互补的两个引擎"**；物理分离 + 双向链接）https://garden.quintsmart.com/para-and-zettelkasten-combined ；Zettelkasten 完整指南（笔记类型表：fleeting / literature / permanent / index / project；**失效模式「Too much linking before enough reading」**；**47% 被保存的内容再也不会被打开**）https://www.atlasworkspace.ai/blog/zettelkasten-method-guide ；PARA vs Zettelkasten（索引机制差异：文件夹时间视野 vs 网络；**"One system is for finishing projects. The other is for generating ideas."**；PARA 失效模式 = 有用想法被困在文件夹）https://smartremotegigs.com/para-vs-zettelkasten/
- 笔记仓化与 `.obsidian` 忽略清单（`.obsidian/workspace.json`、`workspace-mobile.json`、插件 `data.json`、`.trash/`；Obsidian Git 10 分钟自动 commit+push + Pull on startup）：Obsidian 知识库多端共享方案对比与 Git 同步实战 https://www.cnblogs.com/michaelleelll/p/21653461/obsidian-knowledge-base-multi-device-git-sync ；协作同步 FAQ（**私有 GitHub 仓并非端到端加密**（对照 Obsidian Sync 的 AES-256 E2E）；community plugins 未必安全；git 冲突解决）https://pdf.benchchem.com/1174/how_to_sync_obsidian_across_multiple_devices_for_research_collaboration.pdf ；Git Sync 插件（每 vault 一个私有仓；保存即提交；冲突并排 UI）https://community.obsidian.md/plugins/git-obsi-sync
- 仓隐私卫生（密钥/个人文件/大文件/派生物的 `.gitignore` 实践）：appendix f git security（`.gitignore` = 第一道防线；GitHub push protection；**已提交的密钥必须轮换**）https://github.com/Community-Access/git-going-with-github/wiki/appendix-f-git-security ；Ignoring Files（生成物/依赖/密钥/IDE/OS 五类；`git rm --cached`；global gitignore）https://gitcheatsheet.dev/docs/getting-started/ignoring-files/ ；为什么 ignore（**隐私 / 无关 / 过大**三类理由；GitHub 100 MB 限制）https://github.com/learn-co-curriculum/dsc-gitignore

## 附录 A：A 类断言明细

- A-1 至 A-3：见 §2 各 `【A】` 行（用户场景）。A-4 至 A-12：见 §3 各 `【A】` 行（社区案例）。A-13/A-14：见 §4.5/§4.6。A-15 至 A-20：见 §7 各 `【A】` 行（v1.1 UI/认知防过载）。A-21 至 A-27：见 §8 各 `【A】` 行（v1.1 审计·决策链·幻觉抑制·微工作流）。A-28 至 A-31：见 §10 各 `【A】`/`【B】` 行（v1.2 任务看板·自动化追踪）。A-32 至 A-34：见 §11 各 `【A】` 行（v1.3 自动刷新三路径）。A-35 至 A-49：见 §12 各 `【A】` 行（**v1.4 回溯与反馈回路**——通用工程模式 A-35~A-41 / 扰动分流与重规划 A-42~A-43 / 闭环纠错最小回改集 A-44 / 返修语义 A-45~A-46 / 决策变更与负结果 A-47~A-49）。A-50 至 A-59：见 §13 各 `【A】` 行（**v1.5 盲区扫描五轴**——**环境轴** A-50~A-52（外部过期 / reference rot / 撤稿传染）/ **合规轴** A-53~A-56（AI 披露 / 引用幻觉 / 重复发表 / 报告规范清单）/ **时间轴** A-57（双层冻结）/ **人轴** A-58~A-59（escalation 双向风险 / kill criteria））。A-60 至 A-73：见 §14 各 `【A】` 行（**v1.6 环境轴 B/C 层细化**——**B 抢先失效** A-60~A-64（多重发现常态 / 代价量化 / 地位反转 / 预印本双刃 / desk reject novelty）/ **C 评价标准漂移** A-65~A-68（NeurIPS 2014·2021 双实验 / 主观方差 50% / 风向可测）/ **机会窗口** A-69~A-71（数据开放政策 / 护城河消失 / 快成为标准）/ **零依赖半自动监视** A-72~A-73（告警成熟领域 / 人抓-工具记 + 日周季节奏））。A-74 至 A-82：见 §15 各 `【A】` 行（**v1.7 论文仓实测扫描与流程规范化**——Compendium A-74 / RO-Crate A-75 / Lean 项目布局 A-76 / Lean blueprint A-77 / LaTeX 卫生 A-78 / 命名共识 A-79 / 代价量化 A-80 / ACM 制品徽章 A-81 / Diátaxis A-82）。A-83 至 A-90：见 §16 各 `【A】` 行（**v1.8 共享层与辅助资产归属**——monorepo/polyrepo/hybrid 三元 A-83 / 规模判据与双向代价 A-84 / 共享层三成文形态 A-85 / 文献版本三分与再分发权 A-86 / Zotero stored-vs-linked A-87 / codebook 一等制品 A-88 / PARA × Zettelkasten 双引擎 A-89 / 笔记仓化与隐私 A-90）。A-91 至 A-92：见 §17.1/§17.5（**v1.9 分步走策略可行性**——contract-first A-91 / strangler-fig 增量迁移 A-92）。

## 附录 B：B 类推断机读块

```json
[
  {"id": "B1", "inference": "用户九步学术推理写作链的本质是非线性依赖图而非线性管道——上游改动向右游传播、下游发现反噬上游（连锁式影响）；本仓 SPEC_PROCESS 十步 + step-gate 的 STEP_SEQUENCE 是线性骨架，但事件流 append-only + seq 单调天然支持 fork/replay，社区（auto-research 8 phases / PaperJury 多轮）也把链当可循环过程。同构成立点为『分步 + 门禁 + 可回溯』，故无新增机制要求", "basis": "A-1/A-10/A-7 + SPEC_RUNNER_DESIGN"},
  {"id": "B2", "inference": "『每步改动自动产生下一步状态提醒』的社区实现本质是读取方消费 append-only 事件流按 seq 判定推进（auto-research 用 8 phases 显式 next gate、ARIS 用 REVIEW_STATE.json）；本仓 spec_runner 已落 append-only + seq + replay/fork，自动提醒 = 一个读取 seq 并打印『下一步该做 Gate N』的轻壳，机制零新增，最大同构点是不欠账", "basis": "A-1/A-10/A-6 + SPEC_RUNNER_DESIGN"},
  {"id": "B3", "inference": "『数学-算法-数据-结果-论文表达一致性』的本质是多对象证据绑定——让 λ̂ 在论文/设计/代码/结果四层绑定同一对象标识；社区三条路（literate 内联结果 / Lean4 形式化 / 符号核对表+数值探针）中本仓对应 = 声明=重数 + verify-anchor + M7 证据分级 E1（可重放命令）。LGMM 缺的是把这条绑定做成例行 guard（对应其 M-12/M-08）", "basis": "A-2/A-3/A-5/A-11 + SPEC_PROCESS R7"},
  {"id": "B4", "inference": "『模拟评审→反馈迭代』社区用跨模型/multi-arm（ARIS adversarial bandit、PaperJury 对抗式法庭、Agentic_Paper 12 reviewer），本仓用 RULE-5 异基座独立 pass，两者同旨：把作者自评替换为独立评审者；ARIS『两模型逼近 Nash 即最优』论据直接支持本仓 RULE-5 异基座第二会话的价值", "basis": "A-6/A-7/A-8 + SPEC_PROCESS RULE-5"},
  {"id": "B5", "inference": "『防认知过载/漂移/遗忘』不是新机制而是一组展示与介入设计原则——社区共识（Cowan 4±1 / attention residue / vigilance decrement / Msft POMDP）都指向『多流并行才过载、单流线性不触发』（v1.2 修正：本仓 per-feature 事件流独立 = 多流并存，过载真实，见 B8/C-6）；需要吸收的只是『状态压缩成单个认知块 + 主动微介入确认 + 嗅探线索』三条展示原则（对应 verify-anchor 结果色 + step-gate 确认提示），落地为 markdown 聚合看板，而非引入 AgentGUI/LangSmith 重型平台", "basis": "A-15/A-16/A-17/A-18/A-19/A-20 + B2/B8"},
  {"id": "B6", "inference": "链条式连锁反应的硬规则 = 本仓已是确定性状态机：STEP_SEQUENCE=状态集、step-gate（schema 硬性/evidence 非空/同符号核对）=状态转移守卫、事件流 seq=状态历史，与 AgentGuardian CFG、ACM security automaton、PROV-CONSTRAINTS 同一手法；『连锁』落点 = 每步产物标注被下游消费的对象（B3 跨层绑定）+ gate 机械裁决转移合法性，无需引入 DAG 引擎或新状态机库", "basis": "A-23/A-24/A-14 + SPEC_PROCESS R7/gate"},
  {"id": "B7", "inference": "AI 工作流的结果审计/决策链追溯/严格抑制幻觉，在本仓 = 证据锚点化 + 跨层机械校验：M7（断言分级 E1-E5，同 COCO 集成分歧/AWorld 双角色），RULE-5（异基座独立臂，同 heterogeneous cross-validation），decision 八字段（决策链，同 PROV wasGeneratedBy/derivedFrom），verify-anchor（锚点核查）；社区（TraceElephant 17%→30%）实证『可审计性取决于记录质量』，直接支持本仓『每步恰一条决策 + 物证锚点』——幻觉抑制不是模型层补丁而是记录与门禁纪律", "basis": "A-21/A-22/A-23/A-24/A-25/A-26 + M7/RULE-5"},
  {"id": "B8", "inference": "本仓认知过载真实存在（C-4/C-5『单写者单流天然免征』前提被证伪）：per-feature 事件流独立 = 多流并存（每 feature 一条 + fork 派生），叠加 AI 长输出 + 频繁外部反馈；正确缓解形态 = 在既有事件流之上加一层轻量聚合视图——stdlib 只读看板生成器，扫描 PROGRESS(Task Ledger)+spec 四文档+sessions 事件流 verdict(Progress Ledger，Magentic-One 二账本已隐式存在) → 压缩每 feature 为单行认知块，按 3 状态分组 + NEXT 队列（外部注入/主动微介入入口）；fork 派生用 git worktree + git log --graph 原生表达；『声明=重数』由 repo_stats 机械对账兜底；零 GUI 服务器/零新依赖/AI 可写 markdown", "basis": "A-16/A-17/A-18/A-28/A-29/A-30/A-31 + C-6"},
  {"id": "B9", "inference": "看板『自动抓取/自动状态更新/实时反馈』本质是派生产物自动重生成问题——看板=只读视图，职责=从真值源被动重算，故无『需用户主动唤醒』固有理由；社区三路径（FileSystemWatcher 事件驱动 / hook+CI 门禁自动重生成 / 终端轮询渲染）均零第三方依赖可达成；本仓 L0 档已零成本（并进既有 pre-commit 四 hook + step-gate + repo_stats 对账，提交即刷板），L1/L2 为增量可选档（stdlib + 轻轮询）——完全脱依赖用户指令", "basis": "A-32/A-33/A-34 + C-7"},
  {"id": "B10", "inference": "回溯的正确语义 = 『非时序回跳到被证伪的那一步』+『补偿式留痕而非删除』+『最小回改集』；它否定两种直觉做法——顺序退一步（thrashing 的源头）与删除重来（破坏 append-only 与可复现）。回溯跨度应由因果链而非层数决定，且必须显式区分『不可回退点（pivot）』与『可重做区间』", "basis": "A-35/A-36/A-37/A-44 + B1（非线性依赖图）"},
  {"id": "B11", "inference": "本仓『回溯的物理前提』已全部具备：append-only 事件流（不可变历史）/ fork（旧 seq 派生支线）/ 多轮独立 vN session（P-020 先例，specwf-p042 与 specwf-p028 已实证两轮返修）/ ADR supersede 链（取代而非编辑）/ M7 账本（负结果可入账）。缺口仅三点语义与规则：① 回溯事件无形式化记录（跨度·影响集·被取代产物版本）② 无收敛/终止规则（thrashing 与 replanning-loop 防护）③ 计划变更与执行变更未显式分离（prospective/retrospective 二分未落位）", "basis": "A-36/A-39/A-41 + SPEC_RUNNER_DESIGN（append-only + fork）+ PROGRESS P-020 先例"},
  {"id": "B12", "inference": "本仓『重做缺口分析』的合规形态 = 计划变更版本化而非就地改写：RESEARCH/DESIGN 属 prospective provenance，故『回到第 N 步』应表现为该文档版本号自增 + 新增『本轮回溯依据』节（旧结论保留在历史叙述中），而『实际跑过什么』追加到事件流（retrospective）。由此『旧口径留痕 + 新口径显式标注为事后』获得机械落点，且无需引入 Saga 引擎、状态机库或 DAG 引擎本体", "basis": "A-39/A-47/A-48 + C-8"},
  {"id": "B13", "inference": "『前步过期』有三种来源，而 v1.4 只覆盖第一种：① 内部证伪（后步产出证伪前步，v1.4 已覆盖）；② 外部世界变化（新文献出现 / 数据源变更或消失 / 引用被撤稿 / 链接内容漂移）；③ 外部要求变化（报告规范、AI 披露政策、venue 必填清单）。②③ 不是『当时写错了』而是『现在过期了』——因此不能靠回溯纪律解决，须靠预先写定的重检触发（三分类分流）+ 门禁化核验", "basis": "A-50/A-51/A-52/A-53/A-56 + B1（非线性依赖图）"},
  {"id": "B14", "inference": "本仓对外部引用的核验能力目前为零，而这是环境轴中唯一可完全机械化的一环：verify-anchor 只核验仓内路径（文件存在 + 章节标题 + 行号），不覆盖仓外资源；环境轴要求的恰是仓外三层——存在性（DOI/bib 可解析）× 未变更（content drift 二分）× 未撤稿；三者均有现成结构化数据（Crossref / OpenAlex / Retraction Watch）与工具（citecheck 已具 CI 退出码 0/1/2），与本仓 hook 语义天然对齐", "basis": "A-51/A-52 + verify-anchor（P-025 三形态）+ B6"},
  {"id": "B15", "inference": "pivot（A-35）与 freeze（A-57）是同一概念的两个尺度：pivot = 单个决策的不可回退点（过此不再补偿、只能重试）；freeze = 整条链的不可回退点（过此只允许修错与补合规）。本仓已具备前者（ADR accepted / commit 入库 / 文档 accepted），缺后者；A-57 的『只有修错与补合规可直接进，其余进 parking lot』为其提供现成的例外判据", "basis": "A-35/A-57 + B12"},
  {"id": "B16", "inference": "vN 轮次若缺 kill criteria，正是 A-59 的 renegotiation trap：v1.4 的 C-9 只给了『轮次上限』（数量约束），而真正防住『该停不停』的是条件约束（预先写定的前瞻性阈值）；同时 A-58 提醒反方向风险（过早放弃）——故 kill criteria 必须与『新证据是否改变结论』（A-50 的三分类）绑定，而不能与『已投入多少轮』绑定", "basis": "A-58/A-59/A-50 + C-9"},
  {"id": "B17", "inference": "B 层（抢先失效）的本质不是『过期』而是『剥夺』，且不存在补偿动作——用 v1.4 的语言：抢先 = 外部先到达 pivot（A-35 的不可回退点），没有 compensating transaction 可执行。因此其处置形态与 A 层根本不同：A 层是『重检 → 三分类 → 重跑』（可更新），B 层只能是『早期预警 → 差异化重定位 / 或终止（kill）』。结论：B 层需要的是一个『预警面』，而不是一个『更新面』", "basis": "A-35/A-60/A-61/A-63 + B13"},
  {"id": "B18", "inference": "C 层（评价标准漂移）的量级已被实证固定为结构性噪声（NeurIPS 2014 25.9% / 2021 23.0% 决策不一致；accept precision 0.495；50% 评分方差源于主观性；且不随规模改善），其管理学含义是『降低单次判决的权重』——结合『高分端与引用无相关／低分端有相关』的不对称可得：『好却没中』几乎不携带信息，『被打低分』才携带信息。故本仓复评资源应按此分配（对低分做归因，对『高分被拒』不做过度归因）", "basis": "A-65/A-66/A-67"},
  {"id": "B19", "inference": "零依赖半自动监视形态的最低充分三段式 = ① 人负责『抓』（订阅 Google Scholar 引文/关键词告警、arXiv 分类 RSS、目标期刊 TOC，用现成阅读器聚合）② 本仓负责『记』（把抓到的条目落为本地清单文件，与既有缺口清单做差分）③ 差分产出三态（新增疑似重叠 / 新增疑似过期 / 无变化）。全程零外部依赖（不调 arXiv/Crossref API、不引第三方库），且与 A-73 的日/周/季节奏及本仓 C-7 三档自动强度直接对齐", "basis": "A-72/A-73/A-50/A-52 + B14 + C-7"},
  {"id": "B20", "inference": "论文仓实测症状与本仓不变式可逐条对偶，故『规范化』不需要新方法论，只需把既有不变式外推一层：① 474 编译产物与源码混放 ↔ I-5 纯派生 / I-6 不增真值（派生物不入真值区）② 40 压缩包与解压目录并存 ↔ I-1 单写路径（一份真值，压缩包只作分发包）③ 137 个 .tex 文件名与状态词入名 ↔ I-3 幂等 / 版本外置（名=身份，版本=元数据）④ 治理文档 9 份同名不同格式 ↔ I-7 词表对齐（同名必须同义）⑤ Lean 双源漂移 ↔ I-10 语义同源（证明制品单一归属）⑥ 34 个 one-off 脚本 ↔ I-8 显式缺口（脚本分层 explore/ · pipeline/）", "basis": "E1 实测（521 目录 / 4503 文件）+ A-74/A-76/A-78/A-79 + 本仓 I-1/I-3/I-5/I-6/I-7/I-8/I-10"},
  {"id": "B21", "inference": "用户仓中的『逆向拆解文档』本质是『非形式化—形式化』的桥，而社区已给出其正确形态 = blueprint：现状是多份 md/py（CLAUDE_REASONING_ARCHITECTURE / PROOF_ANALYSIS / LGMM8_Proofs_Analysis / verify_proofs / SABR_v6_完备性分析）各自为政、与 134 个 .lean 靠人工同步——正是 LeanArchitect 点名的『两份制品重复 → 维护开销与漂移』；正确形态是让『陈述 → 依赖 → 证明状态（是否含 sorry）』从 Lean 侧自动导出，人工文档只保留 Explanation（为什么）而不重复 Reference（做了什么）——这同时是 Diátaxis『禁止混模式』在形式化场景的实例", "basis": "A-77/A-82 + E1（.lean 分布：CDO 21 / JOL 10 / LGMM 62 / MIDAS 24 / Volsurface_Heston 17）"},
  {"id": "B22", "inference": "用户的多版本发表策略与返修轮次，社区已有标准化『标签』承载阶段语义（ACM/AEC 版本标签范式：R1-submission / R1-camera-ready / AEC-submission / AEC-revision / AEC-final），即阶段语义应由标签而非文件名自由发挥承载；这可消解当前 JOLF-2.0 / JOLF_3_1_MVP / RMT-4.0 / RMT-5.0 / CDO_v9_Rigorous 之间『哪个对应哪一轮投稿』不可机读的问题，并与 v1.4 返修语义、v1.5 合规四检（重叠声明）衔接", "basis": "A-81 + A-45/A-46 + C-11"},
  {"id": "B23", "inference": "用户现状精确对应 A-83 的 Mono-as-Poly——一个物理目录（Working paper/）承载 ~17 个独立项目 + 共享资产 + 归档快照 + 个人内容，具备 monorepo 的形态却不具备 monorepo 的机制（无一致性规范 / 无共享层契约 / 无忽略清单）；而 A-84 的判据（Team size 1–50 且需协调 + 共享数据模型与基础设施）明确把结论指向 monorepo 侧。裁定方向 = 不拆分，而给这个既成 monorepo 补机制。这同时消解『根 CODE_WIKI.md 定位』问题：它作为 monorepo 顶层索引的定位是合法的，只是名不副实（与仓内另 6 份同名文档无法区分层级）", "basis": "A-83/A-84/A-85 + E1 实测（Working paper 根 13 文件 / ~17 项目 / 6 份 CODE_WIKI）"},
  {"id": "B24", "inference": "三类辅助资产的归属可一次判定，判据全部来自已调研标准，无需新方法：① 文献 PDF（363 个）→ 移出仓，Zotero stored files + 云盘，仓内只留 .bib + DOI/citekey（A-86 VoR 不可再分发 + A-87 stored vs linked）② 文献提取文本（121 个 txt、4 种命名）→ 派生物不入仓；必须保留则统一 data/extracted/<citekey>.txt 并声明可重生成（A-87 + v1.7 B20 的 I-5/I-6）③ 数据字典（4 个 xlsx）→ 升级为一等制品纯文本 data/CODEBOOK.md 并补齐 A-88 必含列 ④ 笔记 / canvas / Obsidian（3 canvas + roadmap/ + PhD/ 对话记录）→ 物理分离为独立 vault 仓（A-89 双引擎物理分离 + A-90）⑤ 个人与职业内容 → 必须与任何可公开仓物理隔离（优先级最高；A-90 私有仓非 E2E）⑥ 归档快照（files.zip ×10 与 .rar）→ 待裁决（H14）", "basis": "A-86/A-87/A-88/A-89/A-90 + v1.7 B20 + E1 实测（PDF 363 / txt 121 / xlsx 4 / canvas 3 / files.zip ×10）"},
  {"id": "B25", "inference": "共享层的正确形态 = 『一份规范 + 一个索引 + 一个红线清单』，而不是『一个杂目录』：A-85 的 handbook 模板给出『共享层首先是一份规范文档』，A-84 给出『1 人 / 17 项目应走 monorepo』，故 Working paper/ 根应从杂层收敛为三个具名物——① WORKSPACE.md（monorepo 顶层规范：命名 / 目录骨架 / 派生物隔离 / 脚本分层 / 资产归属，即 v1.7 C-15 契约层的落点）② INDEX.md（取代当前模糊的根 CODE_WIKI.md，登记 17 个项目的名称 / 状态 / 关联；A-89 的 Index/structure note）③ data_policy.md（明确哪些内容绝不外传；A-85 的 00_admin/data_policy.md）", "basis": "A-83/A-84/A-85/A-89 + C-15/C-18/C-19/C-20"},
  {"id": "B26", "inference": "分步走三步的依赖结构是 S3（推理工作流）只依赖 S1（契约层）、不依赖 S2（清理层）——即『先立规范 → 广播清理 → 后建推理工作流』次序自洽：S3 落地不必等 S2 完成，S2 也不必阻断 S3；但 S2 的『广播』须按 C-22 细化 = 标准唯一 × 执行逐仓，先以最接近 compendium 的仓做 pilot 实测契约最小充分集（H12），再据 B20/C-16 的可机械检出判据决定全量翻新或逐仓渐进，避免一次性重整（A-92）破坏已规范化部分", "basis": "A-91/A-92 + C-21/C-22/C-23 + H12"}
]
```

## 附录 C：C 类判断与假设区

- C-1/C-2/C-3：见 §5。C-4/C-5：见 §5（v1.1，新增三同构维度 + 仍止于调研的补充裁定）。C-6：见 §5 + §10（v1.2，织界线修正——本仓多流并存过载真实，缓解=markdown 只读看板生成器 + git worktree/log graph，仍懒加载 gate）。C-7：见 §5 + §11（v1.3，看板可自动刷新——事件/hook/轮询三路径，脱用户指令）。**C-8：见 §12.7-§12.8**（v1.4，回溯可行且以既有机制承接——正确形态是**纪律**而非引擎，仍懒加载 gate，触发 = 一次「影响集失控」真例）。**C-9：见 §12.8**（v1.4，收敛控制判据登记——轮次上限 + 进展判据，仅纪律不落工具）。**C-10：见 §13.6**（v1.5 盲区扫描——环境轴优先级最高：唯一"本仓完全无对应机制"的失效；三分类分流 + 触发式重检候选，仍懒加载）。**C-11：见 §13.6**（v1.5 合规轴——**投稿前合规四检**登记为纪律：引用核验 / AI 披露 / 重叠声明 / 报告规范清单；**引用核验建议优先触发工具化**）。**C-12：见 §13.6**（v1.5 时间轴 + 人轴——freeze 与 kill criteria 必须**预先写定**，并防 renegotiation trap）。**C-13：见 §14.6**（v1.6 环境轴 B/C 层——B/C 为真盲区但**优先级低于 A 层**（A 层污染既有记录；B 层浪费投入、C 层判决不公）；**零依赖半自动形态落地为「纪律 + 本地清单」**，不建抓取、不引依赖，触发=一次真例；懒加载 gate 保持）。**C-14：见 §14.6**（v1.6——**抢先预警与止损正式耦合**：B 层预警即 kill criteria 所要求的前瞻性证据，形成判据链「**A-50 三分类 × B 层抢先预警 × A-59 kill criteria**」）。**C-15：见 §15.4**（v1.7 论文仓——**规范化分层落地**：先立"一页 `CONVENTIONS.md` + 三模板"**零工具零依赖**契约层，再逐仓迁移；触发=用户指定首个迁移仓）。**C-16：见 §15.4**（v1.7——规范化价值在**可机械检出**；四条判据中 ①②④ **与 project-console"生成器 + hook + 校验器"三件套完全同构可复用**）。**C-17：见 §15.4**（v1.7——**blueprint 为性价比最高的一项新增**；**仍懒加载**，触发=决定做成可被第三方独立核查的制品）。**C-18：见 §16.5**（v1.8 共享层与辅助资产——⑨/⑧ 两项空白已关闭，**不需新方法论亦不需外部机制**；与 C-15 合并为同一批**"纪律 + 三份文件"**交付；触发=用户指定首个迁移仓）。**C-19：见 §16.5**（v1.8——**隐私隔离优先级最高，高于整洁与规范**；`data_policy.md` 为**首件交付**）。**C-20：见 §16.5**（v1.8——**辅助资产三层收敛**：真值层 / 参考层 / 私域层，**层间唯一连接是引用键而非文件复制**）。
- [H1] 九步链是否需要显式 **DAG 依赖映射**（vs 现状线性 + 事件流跳相）未裁决——当前 spec_runner 用 STEP_SEQUENCE 线性 + --expect，若学术写作链确现分支合并，需评估是否有补充依赖表达的必要。
- [H2] **数学-实现一致性**是否引入 Lean4 形式化的性价比未实测——A-11 示 Lean4 为终极工具但成本高，LGMM 已用数值探针替代，需在真正的定理级断言场景做成本收益实测。
- [H3] 本仓是否需要引入任何**可视化/UI 展示层**？未实测（v1.2/v1.3 部分回答）——事件流 seq + doc 单读单位可能已满足"状态/阶段/下一步提醒"；v1.2 指向 markdown 只读看板生成器（§10.5）为最小形态，v1.3 确认其可自动刷新（§11），但**是否真的值得落地**（维护开销 vs 单写者低并发收益）仍未实测。
- [H4] 链条式连锁反应的**上游依赖发现**是否需要显式依赖元数据（全量 DAG）？未实测——§9.3 社区状态机路线主张"逐点 gate 裁决"（贪心增量），全量 DAG 需依赖推理/反向传播成本，本仓 topic 以 review 人工发现反噬切入（B1），显式自动依赖发现的性价比未实测。
- [H5] 看板生成器的**生成时机**：按需生成（手动/CI 触发）vs 上游 watch 自动重生成（改 PROGRESS/事件流即刷新）？**v1.3 部分回答** = 三档自动强度（L0 门禁触发 / L1 FileSystemWatcher 监听 / L2 终端轮询 `watch -n`），三者均零新依赖可行，但各档**常驻开销与实用性未实测**；默认建议 L0（提交即刷）+ L1 可选。
- **H6 / H7（v1.4 回溯，条目标记置于 §12.8 正文原位）**：① **H6 = 回溯「影响集」（哪些前步须重做）的确定方式**——人工声明（当前事实做法）vs 依赖图反向闭包（需显式依赖元数据，与 H1/H4 同源）；② **H7 = 回溯轮次上限阈值**——MDPI「两轮大修」为**期刊流程**经验值，本仓 `vN` 先例最多 `v3`（P-042 / P-028）。两条均**未实测**，登记为观察项。
- **H8 / H9（v1.5 盲区扫描，条目标记置于 §13.6 正文原位）**：① **H8 = 环境轴重检的触发频率与成本**（LSR 以月度检索为节奏，本仓无任何自动化；"人工按批次重检"与"引入监听/定时"的成本收益未实测）；② **H9 = 仓外核验是否可引入外部数据源**（Crossref / OpenAlex / Retraction Watch 数据集均为外部依赖，**与本仓 D6 零依赖定位直接冲突**；离线快照 + 手动刷新、或"仅生成待核清单由人工在浏览器完成"的零依赖半自动形态是否足够，未实测）。两条均**未实测**，登记为观察项。
- **H10 / H11（v1.6 环境轴 B/C 层，条目标记置于 §14.6 正文原位）**：① **H10 = 告警覆盖的召回率与延迟**（Google Scholar 索引滞后数天至数周、覆盖面不穷尽；arXiv 分类告警对"相邻领域"是否存在**系统性漏报**）；② **H11 = "重叠判定"的自动化边界**（由 LLM 判"这篇是否与我的缺口重叠"属 **M7 关注的高幻觉点**（与 A-54 同源：伪造与真实引用由同一生成过程产生）；是否应以「**只做机械的关键词/分类差分，重叠判定全数交人工**」为上限）。两条均**未实测**，登记为观察项。
- **H12 / H13（v1.7 论文仓实测扫描，条目标记置于 §15.4 正文原位；v1.10 状态更新亦见 §15.4）**：① **H12 = 规范化契约的"最小充分集"**（"一页契约 + 三模板"能否覆盖 7 个仓库的全部差异，尤其 `Coupla` 已有 `spec/templates/`、`LGMM 8.0` 已有 `MANIFEST.md` 的**既成事实**）——**v1.10 部分实测：骨架层充分、判据层不足，最小充分集须含"可跑命令 + 排除第三方子仓 + hash 对比"三件**；② **H13 = Lean 双源漂移中哪一份是真值**（`LGMM 8.0/lean4/` 15 文件 vs `LGMM_Lean/LGMM/` 12 文件，**文件集不一致**；需逐文件 diff 后裁决，**裁决前不得删除任一份**）——**v1.10 实测：`lean4/` 实为 16 / 同名 13 / 12 内容一致 / 1 DIFF（`EWNLS.lean`）/ 3 仅本仓；真值源方向趋于 `lean4/`，待用户确认**。H12 余全量迁移实测（挂 H16）、H13 余用户裁决，均**登记为观察项**。
- **H14 / H15（v1.8 共享层与辅助资产，条目标记置于 §16.5 正文原位）**：① **H14 = 归档快照的处置**（`files.zip` ×10 与 `LGMM_0727.rar` / `MIDAS-Granger.rar` 属"历史交付快照"（有留档价值）还是"冗余副本"（可删）？需**逐个人工判定**后才能定"归档层"规则；**裁决前不得删除**）；② **H15 = 363 个 PDF 的版本构成**（VoR / AM / preprint 三分未实测；判定依赖 DOI 查询，而多数仓**无 git、无历史可溯**）→ **逐篇判定完成前，默认按"不可再分发"保守处理，不进入任何公开仓**。两条均**未实测**，登记为观察项。

## 附录 D：与既有候选池的关系

- 本调研同构于 P-039（同属"把当前框架应用到另一个工作流"）；不新增候选 UID（无外部框架本体吸收，仅概念登记 + 复用，符合 ADR-0010 懒加载）。
- v1.1 补充三个新维度均映射本仓既有机制（M7/RULE-5/decision/verify-anchor/step-gate/事件流 seq），**零新依赖**；未引入 AgentGUI/LangSmith/Langfuse/AgentGuardian 等重型平台或运行时本体——与 C-5 裁定一致。
- v1.2 补充（任务看板/自动化追踪）：**候选形态 = markdown 只读看板生成器（Layer-0/1 概念，stdlib，可作 spec_runner `board` 子命令或独立脚本）**，从 Backlog.md/Magentic-One 二账本取模式但**不吸收框架本体**；fork 支线用 git worktree/log graph 原生能力。未落地（C-6 懒加载 gate），触发条件=用户明确要求。
- v1.3 补充（自动刷新）：三条自动触发路径（FileSystemWatcher 事件 / hook+CI 门禁 / 终端轮询渲染）均为**零新依赖**方案；L0（并进既有 pre-commit 四 hook）已零成本，L1/L2 为增量可选档——**完全脱依赖用户指令**（C-7/B9）；仍未落地，懒加载 gate 保持。
- **v1.4 补充（回溯与反馈回路）**：社区四层模式（**补偿 / 留痕 / 回跳 / 重算**）**全部映射到本仓既有机制**（append-only 事件流 / `fork` / 多轮 `vN` session / ADR `supersede` / M7 账本），**零新依赖、零新组件**；正确形态 = **纪律**（非时序回跳到因果源 + 最小回改集 + 旧值留痕，B10）而非**引擎**（Saga / DAG / 状态机库均为外部重型本体，违 D6 零依赖定位）；**回溯事件的形式化记录**（B11 缺口①）登记为**触发式候选**，触发 = 出现一次「影响集失控」真例（如某次返修波及 3+ feature，或两次返修互相覆盖）；**收敛控制**（轮次上限 + 进展判据，C-9）仅登记为纪律；懒加载 gate 保持。
- **v1.5 补充（盲区扫描五轴）**：排查六轴后**过程轴 / 证据轴显式判为已覆盖**（并说明理由，防为凑数而制造盲区）；**四轴为真盲区且均在既有机制边界之外**——**环境轴**（外部过期：本仓三件套只回答"我们做了什么"，不回答"外部世界是否已使结论过期"）、**合规轴**（投稿前合规：期刊政策效力已被实证证伪，不能外推给对手方自律）、**时间轴**（全链 freeze：本仓只有单决策 pivot）、**人轴**（kill criteria：本仓只有数量约束"轮次上限"）。四者**均未引入外部框架本体**：环境轴采纳 LSR 的**三分类分流**（概念）、合规轴列为**纪律四检**（引用核验 / AI 披露 / 重叠声明 / 报告规范清单）、时间轴与人轴合并为 **"freeze + kill 预先写定"**（预注册思想，与 v1.4 的 A-48 同源）；**唯一可工具化的候选 = 引用核验**（B14，且 `citecheck` 已具 CI 退出码语义），但其外部数据源依赖与 D6 冲突 → 登记 **H9**；懒加载 gate 保持。
- **v1.6 补充（环境轴 B/C 层 + 机会窗口）**：把环境轴细化为四层后，**B/C 两层同样落在既有机制边界之外，但性质与 A 层不同**——**A 层污染既有真实记录**（后果直达记录完整性），**B 层只浪费投入**（novelty 被剥夺）、**C 层只造成判决不公**；故 **C-13 判定其优先级低于 A 层**，且处置形态**不能复用 A 层的"重检触发"**（B 层无补偿动作，见 **B17**），只能是"**预警 + 差异化重定位 / kill**"。**零依赖半自动形态（用户指定约束）经 A-72/A-73 取证确认为成熟且零成本**：告警由外部平台完成，**本仓只做"记账 + 三态差分"**（**B19**），与既有 C-7 三档强度、A-73 的日/周/季节奏直接对齐；**唯一有争议的自动化边界 = "重叠判定"是否交 LLM**（登记 **H11**，与 A-54 同源的高幻觉点）。**机会窗口（数据开放 / 技术潮流）为双向**——同一政策**同时**开启机会与消灭护城河（A-70）；懒加载 gate 保持。
- **v1.7 补充（论文仓实测扫描与流程规范化）**：本轮**首次把调研对象从"文献"换成"用户自己的仓"**——E1 实测给出**可机械枚举的症状**（474 编译产物 / 40 压缩包 / 137 种 `.tex` 名 / 9 份同名不同格式的 `CODE_WIKI` / ≥5 种版本目录命名 / Lean 双源漂移），归因到**六层缺失**，并与社区五层标准（Compendium / RO-Crate / Lean 布局 / blueprint / LaTeX 卫生 / 命名 / 制品徽章 / Diátaxis）**逐条对号**。**关键结论 = B20**：这些症状与本仓不变式**逐条对偶**（I-5/I-6 · I-1 · I-3 · I-7 · I-10 · I-8）——**故"系统性规范化论文写作流程"不需要新方法论，只需要把已有不变式外推一层**；**C-16** 进一步指出其最大价值**不在整洁而在可机械检出**，且其中三条判据**与 project-console 的"生成器 + hook + 校验器"三件套完全同构**（可直接复用 P-043~P-047 已验证的架构）。**落地节奏 = C-15 分层**（先立零工具零依赖的"一页契约 + 三模板"，再逐仓迁移——因为 E1 显示规范化程度**极不均衡**，统一重整会同时破坏已规范的部分）；**C-17 登记 blueprint 为性价比最高新增**（134 个 `.lean` 已投入而依赖关系只在人脑）但**仍懒加载**。**H12/H13 两处必须在动仓前解决**：契约的最小充分集未实测；**Lean 双源哪份是真值未裁决 —— 裁决前不得删除任一份**。
- **v1.8 补充（共享层与辅助资产归属）**：本轮先做**覆盖度审计**（把 §15 六层根因逐条核对）——**六类中五类的解法已在手**（4 类来自已调研社区标准、1 类来自本仓既有机制可直接外推），**仅两项真空白**（⑨ 共享层 / ⑧ 辅助资产）+ 1 项触发式（④b）。**两项空白经本轮取证已关闭，且结论仍是"不需新方法论、不需外部机制"**：**⑨ 共享层**用 **monorepo 机制补全**（A-83 的 `Mono-as-Poly` 判定 + A-84 的规模判据「1–50 人且需协调 + 共享基础设施」均指向用户侧 → **不拆分、补机制**），**⑧ 辅助资产**用 **B24 归属表一次判定**（PDF 移出仓 / 提取文本为派生物 / codebook 升一等制品 / 笔记分离 / 个人内容隔离 / 归档待裁）。**交付形态 = 与 v1.7 的 C-15 契约层合并为同一批"纪律 + 三份文件"**（`WORKSPACE.md` / `INDEX.md` / `data_policy.md`），**零工具零依赖**。**优先级排序被本轮推翻了一次直觉**：不是"先整洁"，而是 **C-19 隐私隔离最高**——因为 `Working paper/` 同时含"可能要公开的研究产出"与"绝不外传的职业/个人内容"（`草台班子复盘.md` / `职场经历对话记录.md` / `potemkin-village-notes-en.md`），**整体打包即不可逆泄露**，而 A-90 明示**私有仓并非端到端加密**。**方法论级收获 = C-20 的三层收敛**（真值层 / 参考层 / 私域层，**层间唯一连接是引用键而非文件复制**）——这一条同时**从根上消灭** v1.7 实测的 **`files.zip` ×10**（压缩包是"复制"的极端形态）与 **`document.tex` ×6**（无语义名的复制），即**两类症状共享同一根因**。