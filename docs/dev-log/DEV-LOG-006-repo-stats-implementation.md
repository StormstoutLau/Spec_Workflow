# DEV-LOG-006: repo_stats 全流程——DIS-010 深度调研 → spec 四件套 → repo_stats.py 落地 → stats 块集成 → 样本㉑ 登记

> **日期**: 2026-08-22
> **会话**: Claude GLM-5.3（主控站）
> **涉及**: spec/repo-stats/（RESEARCH/DESIGN/IMPLEMENTATION/CHECKLIST）/ scripts/repo_stats.py / CODE_WIKI.md（§2.1 树 + §9 索引 + §10 stats 块）/ .pre-commit-config.yaml / docs/M7_EVIDENCE_LOG.md / docs/discoveries/README.md / README.md / README.en.md / docs/assets/readme/evidence.svg / docs/PROGRESS.md
> **状态**: CHECKLIST 有条件通过（自查全绿，机械证据 E1 可重放；RULE-1 独立 pass 待触发，验收决定同 P-007/P-011 先例）

---

## 做了什么（时序）

1. **Step 1-2 RESEARCH（取证轮 + 撰写轮，样本⑱⑲⑳ 三连击）**：CODE_WIKI §9 全区 / README 双语 / evidence.svg / DIS-010 条目 vs LS/PROGRESS/discoveries/dev-log/各文档 front-matter 机械枚举逐行对账——捕获视图层成片陈旧（五类漂移并存）、⑰⑱ 修正轮残留批（手算中间值 27 四载体复制）、⑲轮「修完即绿」8 位点实际未写入（修正的声明与执行分离）。DIS-010 从 open 调研升级为工具化处置需求：**视图层（CODE_WIKI/README/SVG）累计 33 处占形态 II 总量 62%，手工修正对成片漂移无效，区域级机械对账是唯一终结路径**。
2. **Step 3-4 DESIGN**：stats 机读声明块契约（carriers/patterns/declared/view_layer_samples/doc_registry/facade_baseline/suppress 七节）+ 模式库 21 条数据驱动（正则/真值绑定/作用域/捕获组登记在数据非代码）+ 载体两级（living 阻断 P2 / facade 时点快照 P3 非阻断）+ 七通道真值枚举（T1 文件系统/T3 hooks/T4 PROGRESS/T5 hits 块/T6 DIS/T7 派生）+ 三路对账（rs-decl P1 / rs-pattern / rs-list P2）+ 不变式 I-1~I-7。
3. **Step 5-8 IMPLEMENTATION/CHECKLIST**：解析契约正则化 + 19+4 fixture 矩阵 + stdlib API 下限表 + LOC 预估口径显式（~650 含 selftest）。
4. **Step 9 TDD 实现**：`scripts/repo_stats.py` 1276 行（RS1-RS5）。selftest 首跑捕获 DR-D~G 四项实现期发现（分桶行守卫逻辑反转 / fixture 载体名不匹配 / F7 语义与契约不符 / F9 树字符错误），修正后 23/23 PASS。
5. **集成-起草**：CODE_WIKI §10 stats 块人工起草（模式库全仓试扫定稿）→ **verify 首跑捕获 10 项 P2：7 项真实漂移（§9 缺 repo-stats 索引行 + 三处版本号停旧值（⑲发现③遗留批）+ §2.1 树缺条目 + P-013 停旧值 + 双 hook 停旧值）+ 3 项工具侧误报**（2 处 PT-4 误命中行号/版本片段 + 1 处 doc_registry label 子串定位误命中叙事行）。
6. **集成-修正（双通道）**：工具侧——PT-4 加负向后顾 `(?<!L)(?<![.\d])` + doc_registry 行定位改链接形态（`](./path)` / `](./dir/)`）+ **F20 TDD 先红后绿**（复现 label 子串误命中 → 修复 → 23/23）；文档侧——活靶 7 处修正 + CODE_WIKI v1.7 入册（§2.1 树/§6.4/§9 索引区/stats 块）→ **verify exit 0（「修完即绿」由模式扫描对账确认——修正轮产出自身在扫描面，区别于⑲轮仅声明）**。
7. **集成-hook**：`.pre-commit-config.yaml` 第三 hook repo-stats（files 作用域 = SCOPE_RE 镜像）。三校验器连带损伤终验全绿（dc_validator 49 文件 0 违规 / m7_stats 1 P3 预期 / selftest 23/23）。
8. **Step 10 收口**：M7 样本㉑ 登记（7 P2 + 形态 II 7 处=版本号×3+计数×4，新工作流第三次实战：手工加行 → `m7_stats.py --write` → verify）→ hits 块 samples 20→21 / form2_total 53→60 / from_samples 47→54；DIS-010 → toolized（九度实证/七入载体/40 处占 66% + 处置落地注）；本 DEV-LOG；门面三件刷新（README 双语 + evidence.svg 21/60）。

## 决策依据

### ① 对账器非再生成器（与 m7_stats --write 相反）

prose 不可机械重建（模式命中位点分散在叙述性文字中，重建=改写全文）。故 repo_stats 只报偏差、永不代改，维护工作流 = 「真值源前进 → 人工同步视图 prose **与** stats 块声明 → verify 至全绿 → commit」。这一分工使两工具构成互补：M7 表内统计可再生成（结构规整），视图层 prose 只可对账（语义载体）。

### ② 模式库数据驱动（数据非代码）

正则/真值绑定/作用域/捕获组全部登记在 CODE_WIKI §10 stats 块，repo_stats.py 只含通用执行引擎——新模式零代码改动（加一条 JSON 即入扫描面）。配套试扫否决记录（PT-3 DIS 范围对账：T6 真值口径 min/max 与 prose 序列声明语义不同轴，登记必产误报）——**否决记录入块**，防后人重蹈。

### ③ 载体两级 + 门面快照基准

living（CODE_WIKI/discoveries）实时对账阻断 P2；facade（README 双语/evidence.svg）「时点快照 + 真值指针」——baseline 值 ≠ 当前真值仅报 P3 滞后提示（快照豁免前提 = 写入值为当时真值，⑲轮手算中间值 27 不受豁免保护的教训入 DESIGN）。README/SVG 不追实时同步是设计决定：门面层数字是营销快照，真值指针已指向 M7 账本。

### ④ SVG 特殊通道 + doc_registry 链接形态定位

SVG 不跑 prose 模式（图形布局无稳定锚）——只做 baseline 值的 `>N<` 文本节点包含性检查；doc_registry 行定位用链接 token 而非 label 子串（「002（cpp-hub-absorption）」叙事行含 label 子串但不含链接——F20 实证）。两条均为首跑误报的语义甄别产物：**误报修复必须 fixture 化（F20 TDD），不能只改当次输入**。

### ⑤ 历史叙事用负向后顾而非 suppress 白名单

PT-4（行号引用「L4 feature 目录」/版本片段「v1.5 feature 目录」）与 PT-8（述史「扩为双 hook」）的排除用负向后顾断言——suppress 是文件粒度白名单，会误杀同文件其余真实位点；能改措辞不进白名单（§6 L561 历史叙事改写为「P-011 扩为双 hook、P-014 扩为三 hook」）。

## 遇到的问题

- LOC 预估 650 → 实际 1276（超估 92%）：即便在 P-008（422 vs ~100）/m7_stats（828 vs ~300）双教训后、预估口径已显式含 selftest，仍漏计 stats 块 schema 校验七节逐条 P1 报文 + facade 双通道（prose 基准 + SVG 包含性）+ suppress 后补契约三块——**DESIGN 后补契约项须同步回填 LOC 预估**，已入 IMPL §10。
- 首跑 10 项中 3 项误报：模式设计阶段对「计数声明」与「引用/述史形态」的语义边界估计不足——负向后顾排除清单（L 前缀行号 / `.`前缀版本号 / 「扩为」述史）是首跑实证后才补的。教训：**模式库定稿前须全仓试扫 + 语义甄别，正则精确性靠活靶校准**。
- declared.hooks 声明值 2 与实际 3 不符（第三 hook 入册后忘了同步声明）——rs-decl 通道 P1 当场拦截，对账器自身的声明也是视图（元递归的又一实例，好在同轮被自身看护）。
- 样本㉑ 发现列写法约束（m7_stats 解析契约）：前导数紧跟 P 标记即视为 P 标记本身（`7 P2` → lead=None、ptok 计 7）；形态 II 列须前导整数；prose 避免非意图的「数字+P1/P2/P3」连写。

## 收口批独立审查追记（2026-08-22）

收口批独立 review（RULE-1 时序独立满足——新会话与收口轮分离；RULE-5 同基座降级标注；[REPO_STATS_AUDIT.md](../../spec/repo-stats/REPO_STATS_AUDIT.md)）对账收口批数字链条，捕获一处边界外停旧：

- **发现（P3）**：[PROGRESS](../PROGRESS.md) P-014 依据列「八度实证」计数词停旧——行内 40 处/66%/㉑ 收口时点值均已推进，独「八度」停在立项时点（行内已并列「立项时点 33 处/62%」却漏推计数词本身）。位于 repo_stats 机械对账边界外：「N 度实证」无 PT 模式锚定（模式库 21 条全部锚定短语形态，无一匹配「度」），verify 四通道全绿零拦截——**pattern 覆盖是枚举性而非穷举性，工具化当日即现库外复发**。
- **裁决与登记**：入账裁决 A（新样本㉒）——形态 II 计数复发 ∧ 轮次分离（产出轮 = 收口轮，捕获轮 = 用户指令 review）∧ 新机制变体三条件全中；B（并入㉑）被 ㉑ 合并成立条件逐项取反否决（review 臂捕获不可写入工具捕获样本，污染 M7 对比臂分组变量），C（仅修正）造成 ⑰-㉑ 同 feature 逐轮全入账的口径分裂。㉒ = **repo_stats 落地后首个「工具边界外 review 臂捕获」数据点**，与样本⑯（工具化前边界外）构成前后对照——评估 P-014 效果的唯一持续观测方式，喂 pattern_lib_version 2 候选议程。
- **八步执行**（同日）：PROGRESS 八度→九度 → M7 ㉒ 入账（合计 60→61，hits 块 --write 重生成 samples 21→22）→ repo_stats verify 首跑 9 P2 + 6 P3 活靶全枚举（living 停旧值族 + facade 快照滞后，与审计级联预测吻合——首跑即活靶再次实证）→ 修正后 exit 0（P3 提示 0，门面三件同日刷新 22/61）。错误未流入版本历史（P-014 未 commit，提交前拦截）。
- **教训**：级联修正须「计数词本体」与「计数词修饰的数值」同批推进——数值并列了时点标注反而制造「已推进」错觉，掩护计数词停旧；机械对账覆盖 = 模式锚定枚举，边界外位点（无锚定短语的计数词）仍靠 review 臂 + 独立审查兜底，与 DIS-010 既有结论（机械枚举是可靠拦截层，但有覆盖边界）一致。

## 下一步

- 独立 pass（RULE-1 时序独立，真异基座优先）：审查对象 = repo-stats 四件套 + repo_stats.py + stats 块（挂后续会话，触发条件同 P-007/P-011 先例；PROGRESS 后续行动登记）
- 门面快照滞后属 P3 非阻断预期态：下次真值前进（新样本/新 feature）时同步 facade_baseline 与 README/SVG 数字
- PT-3 否决的 DIS 范围对账、evidence.svg 复发规律数大数节点（TRUTH_KEYS 封闭枚举无绑定键）为已知未覆盖，低频位点人工同步兜底——pattern_lib_version 2 候选
