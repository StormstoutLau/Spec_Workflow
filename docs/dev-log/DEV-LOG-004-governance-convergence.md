# DEV-LOG-004: 治理收束轮——遗留任务调研 → M7 样本⑩ 补登 → ADR-0009 首次重审 → P-009~P-011 登记 → CODE_WIKI v1.5

> **日期**: 2026-08-19
> **会话**: Claude GLM-5.3（主控站）
> **涉及**: docs/M7_EVIDENCE_LOG.md / adr/ADR-0009-discoveries-log-mechanism.md / docs/discoveries/README.md / docs/007_hallucination_audit_asymmetric_evidence.md / spec/langgraph-upgrade/LANGGRAPH_UPGRADE_RESEARCH.md / docs/PROGRESS.md / CODE_WIKI.md
> **状态**: 收敛完成（六项收束全落盘 + dry-run 自查追加 M7 样本⑪；机械 dry-run 因 RunCommand/bash_exec 双通道故障未执行——降级人工 Grep 枚举复验，捕获本轮自身 4 处产出错误并修复；提交推送待环境恢复，见 §遇到的问题）

---

## 做了什么（时序）

1. **遗留任务全仓调研**：扫描全部 .md 的待办/开放项/候选/TODO 标注（findstr 中文匹配失效 → Python UTF-8 正则扫描兜底），产出遗留清单——M7 未入账计数错误（LANGGRAPH）、ADR-0009 重审到期、P-006 决策待闭合、三个未登记任务候选（薄壳 runner / promptfoo / M7 机读块）、CODE_WIKI 滞后。
2. **M7 样本⑩ 补登**：LANGGRAPH v1.0 A=14→11（虚报 +3）从"自称候选⑦"裁决实登为样本⑩（存量补登）；分桶表新增 LANGGRAPH 行（计数桶），合计 15→16；追加队列由 ⑨ 改⑪。
3. **ADR-0009 失效条件首次重审**：触发事实 = DIS-008（2026-08-17）后连续 5 个 feature（P-003~P-007）无新增且无状态迁移，超阈值 3；结论 = 机制保留不降级、无新增计数自本轮重置。重审记录表新增于"验证"节，修订历史 v1.2 追加一行。
4. **DIS-007 追记 DR-6**（v1.3）：dc_validator.py selftest 硬编码 12/12 实调 13 的工具自身计数错——命题扩展至"人写校验工具"；discoveries README 同步追记 + 首次重审纪律注。
5. **LANGGRAPH L26 标注收束**：计数修正记录改写——"已入账 M7 样本⑩（存量补登——写作时自称候选⑦，惟 ⑦ 已被 precommit-dc-validator 复验占用）"；自引用观察（`grep -c` 自身命中 +1）明确为附随观察不单列。PROGRESS P-006 开放项同步闭合。
6. **PROGRESS 登记滚动**：P-009（薄壳纯 Python runner，方案 B 独立仓库）/ P-010（promptfoo M7 对比臂声明式评测，触发条件样本数 ≥10 已满足）/ P-011（M7 ```hits 机读块 + 登记脚本化）三项 pending 登记；"已完成"表滚动纳入治理收束轮与 P-007 Step 5-7。
7. **CODE_WIKI v1.5 同步**：版本头/覆盖对象（含工具层）/解决的问题表新增契约拦截行/目录结构（scripts/ + 六 feature 目录）/§4.4 dc_validator 专节/依赖表/§6.4 提交契约拦截注/历史教训案例库新增形态 II 计数复发案/文档索引与 ADR-0009 状态刷新。
8. **dry-run 复验（降级）+ 本轮自查捕获 → M7 样本⑪**：RunCommand 与 bash_exec 双通道故障 → dc_validator 未能机械执行，降级为 Grep 全仓枚举 + Read 逐行对账的人工机械复验。复验捕获**本收束轮自身产出的 4 处错误**：① CODE_WIKI v1.5 称"五 feature 目录"（机械枚举 = 6：adr0006-pointer/cpp-hub-absorption/doc-contract/cpp-hub-gap-analysis/langgraph-upgrade/precommit-dc-validator，P2）；② 本 DEV-LOG 初稿复制同错（P3）；③ PROGRESS P-010 触发条件写"M7 样本 16"——16 为形态 II 处数，样本数实为 10/11 混轴（P3，触发结论两轴下均成立）；④ 本 DEV-LOG 初稿状态行未跑先称"dry-run 复验 exit 0"——无证据断言（P2，非形态 II，RULE-6 取证纪律违例）。四处全部修复；形态 II ×3 入账 **M7 样本⑪**（分桶 16→19，计数桶 6→9），追加队列顺延 ⑫（P-008）。
9. **本 DEV-LOG 定稿 + 提交推送**（提交推送因环境故障挂起，恢复后执行——见 §遇到的问题）。

## 决策依据

### ① 样本⑩ 编号裁决（存量补登不挤占已入账编号）

LANGGRAPH v1.1 写作时自称"候选⑦"，但 ⑦⑧⑨ 此后已被 precommit-dc-validator 复验/实施期自查/P-007 实施轮依次占用——写作时点的编号预期被后续登记事实挤出。裁决 = 按实际入账时点顺延为⑩，原"候选⑦"自称以治理收束轮注记形式保留在 L26（不篡改历史文本，只追加裁决说明）。原则：**账本编号以入账事实为准，不以写作意图为准**——与 R7"计数以机械重数为准"同构。

### ② ADR-0009 重审结论"机制保留"的三点依据

零新增 ≠ 机制失效：① DIS-008 后 5 feature 零新增是**登记纪律的设计结果**（每轮审查如实登记，无可登才不登）；② 机制活性有实证——DR-6（工具自身计数错）正是经 DIS-007 追记通道登记的，机制在真实事故上运转过；③ 僵尸账本判据（M7 L5：连续两轮无追加）与 discoveries 零新增是两个独立观测面，后者不触发前者。无新增计数自本轮重置，下轮重审阈值重新起算。

### ③ 自引用观察不单列样本

`grep -c '【A】'` 命令行自身贡献 +1 是**工具盲区观察**而非文档错误事件——没有载体文档含错（LANGGRAPH v1.1 的 15 是修正后正确值）。单列会稀释"形态 II = 文档事实与机械重数不符"的定义。处理 = 作样本⑩附随观察入账，与 DR-6 同族（均指向"机械工具自身亦有盲区"）但不占样本行。

### ④ 样本⑪ 登记：收束轮自查自身产出（本轮最重要的方法论事件）

登记计数错误的治理收束轮，其自身产出（CODE_WIKI v1.5 / DEV-LOG-004 初稿 / PROGRESS P-010）含 3 处计数错 + 1 处无证据断言——**规律②"防幻觉机制自身不设防"至今最强实例**：样本⑨ 证明校验器自身会错，样本⑪ 证明连"正在登记计数错误"的轮次自身也会错，元断言逃逸不认语境。三裁决：(a) 超前断言（未跑先称 exit 0）**不计形态 II**——形态 II 定义 = 精确-looking 低语义载荷字段错误，无证据断言属 RULE-6 取证纪律违例，单列为发现但入不同桶（防概念稀释，同 ③ 逻辑）；(b) DEV-LOG 复制错**独立计数**——不同载体、grep 可独立命中，按分桶"载体 × 字段"矩阵口径各占一行；(c) 静默修复不可接受——本仓库的存在理由即"错误必须入账"，收束轮自查捕获自身错误并入账，是方法论自洽性的实测（登记纪律 vs 形式表演的分水岭）。拦截层归属：dc_validator M5 只覆盖 §0 统计表，prose 计数（版本注/触发条件）靠全仓 grep 枚举对账兜底——三层拦截（工具/prose grep/审查轮）缺一不可的又一实证。

## 遇到的问题

- **RunCommand 工具不可用**（icube.shellExec 报错，与 DEV-LOG-003 同日同状，本日全程未恢复）
- **bash_exec 中途失联**（前半段可用——git status/log 探测成功；后半段 MCP server "tool is not found"，子代理对照测试证实 research-tools 服务器运行时未连接，english-search/paper-search 正常）→ **机械 dry-run 与 git 提交推送均未能执行**
- **降级方案**：dry-run 复验改人工机械复验（Grep 全仓枚举 + Read 逐行对账，覆盖改动文件的 front-matter/链接/计数三类契约点）——该降级复验捕获样本⑪ 的 4 处错误；git 提交推送挂起
- **恢复后待执行**（提交前机械 dry-run 必须 exit 0）：`python -S -E scripts/dc_validator.py` + `python -S -E scripts/dc_validator.py --selftest`，然后 git add 8 文件（CODE_WIKI.md / adr/ADR-0009 / docs/007 / docs/M7_EVIDENCE_LOG / docs/PROGRESS / docs/discoveries/README / spec/langgraph-upgrade/LANGGRAPH / docs/dev-log/DEV-LOG-004）+ commit + push
- **findstr 中文模式匹配失效**（GBK 控制台编码）→ Python `open(encoding='utf-8')` + 正则全仓扫描兜底
- **Glob/LS 工具间歇超时** → Grep（ripgrep 内核）与 Read 通道稳定，以二者为主

## 下一步

- **提交推送（环境恢复后立即执行）**：上节"恢复后待执行"三项——机械 dry-run exit 0 为提交前置门禁（本 DEV-LOG 降级复验不替代 pre-commit 语义）
- **P-008**（首项）：P-007 产出独立 pass（RULE-1 时序独立；真异基座优先；含 Step 10 ADD 独立审计）→ 通过后 IMPLEMENTATION → verified、CHECKLIST → accepted，M7 追加候选⑫
- **P-010**（触发已满足）：promptfooconfig.yaml + 首轮声明式对比评测入 M7
- **P-009/P-011**：按各自触发条件推进（自动化需求出现 / 学习回路独立议题）
