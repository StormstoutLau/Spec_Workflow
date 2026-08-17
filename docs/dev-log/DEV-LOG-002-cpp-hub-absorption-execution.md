# DEV-LOG-002: cpp-hub-absorption 全链路——差距分析审计 → 吸收设计 → ADR 三连 → Tier1/Tier2 落地 → CHECKLIST

> **日期**: 2026-08-17
> **会话**: Claude GLM-5.3（主控站）
> **涉及**: spec/cpp-hub-absorption/ / adr/ADR-0007~0009 / SPEC_PROCESS v1.4 / 框架 v1.3 / M7_EVIDENCE_LOG / docs/discoveries/
> **状态**: CHECKLIST 验收通过（39/40，1 P3 属 P-003 范围）；4 commits 已推送（12c79a4..b7a7f58）

---

## 做了什么（时序）

1. **吸收设计 Step 4 Review（独立 pass）**：全锚点 E1 重验，发现 2 P2 + 6 P3——P2-1 机制 #7 逃脱三层处置（"计数闭合假象"，形态 II 新变体）/ P2-2 M7 载体三方冲突。P2 修正批清零（设计 v1.1）。
2. **ADR-0007 起草 → 决策分析 → 外部取证 → 定版**：五决策（D1 M7 账本载体 / D2 DC1-DC4 / D3 登记补全 / D4 design 入词表 / D5 英文 token）。D2 外部证据经 MCP 检索（arXiv ×2 + StackExchange + K8s 提案）+ 页面级 grep 复核 4/4，决策阈值从"回流常态化"下调为"≥ 第三次回流即正期望"。用户整批确认 → accepted v1.1（DC token 占用 grep 闭合后定版）。
3. **ADR-0008 起草 → 定版**：scope 自设计 v1.0 的"D4 单决策"修正为"D4+D6 双决策"（Step 4 Review 缺口 B：D6 决策记录悬空）。决策分析含内部 E1 实证五例 + arXiv 2603.03406 佐证（review 有效性随规格丰富度 4x 放大）。
4. **Tier1 执行**：框架 v1.2→v1.3（STEP_GAP 两态分型）。设计预估 3 处修改，实际全量枚举 **10 位点**（S4 教训预判成立）；**DIS-008 事件**——同文件多 Edit 并行执行致 6 处静默回滚，grep 终验拦截、串行重放修复。M7_EVIDENCE_LOG 新建（ADR-0007 D1 首次消费）。
5. **Tier2 执行**：SPEC_PROCESS v1.3→v1.4（门禁块 a-d / Step 8 +2 项 / D5 集成点 ×2，吸取 DIS-008 教训全程串行编辑）；ADR-0009 + docs/discoveries/README（DIS-007 映射 + DIS-008 首登）。
6. **4 commits 提交推送**（设计 §9.2 切分：adr 定版 / spec v1.1 / tier1 / tier2）。
7. **CHECKLIST 验收**：v1.4 新规则（双向引用/断言延续）首次自举执行——双向引用 6 命中闭环；B2 gap 判 **STEP_GAP_CLOSED**（本仓首个 CLOSED 实例，闭合证据 = 框架 v1.3 grep 5 处）。验收 39/40。

## 决策依据

### ① ADR 外部证据的双层复核纪律

MCP 检索返回体（API 级）≠ 页面级复核。ADR-0007 D2 四条证据先登记为"检索级 A 类"，独立 pass 页面抓取 + grep 逐字比对后升级"页面级复核 A 类"（4/4；E3 顺带升级元数据 ICSE'2023）。反爬拦截（SE 页面）如实登记不掩盖——证据等级的诚实标注优先于证据数量。

### ② 形态 II 第四桶："映射闭合"

GAP_ANALYSIS 计数错（12A→16A）是"数错"；本次 P2-1 是"计数对但映射漏"——3+3+5=11 的表面闭合掩盖 #7 逃逸。拦截手段同为 E1 机械枚举（逐项映射表），已入 M7 分桶（载体 × 字段类型第 7 列）。

### ③ DIS-008（open）：同文件并行 Edit 静默回滚

工具层失效：多个 Edit 并行写同一文件时，后发写入以陈旧快照覆盖先发编辑（6/10 位点回滚，无任何报错）。拦截层 = 事后 grep 终验，非工具自护。操作缓解已内化为本日志后续纪律：**同文件编辑严格串行；破坏性/批量编辑后必 grep 终验**。与形态 II 规律三同构（机械枚举才是可靠拦截层）。

### ④ Step 2 门禁自举核验

本 feature 是 v1.4 门禁生效后首个走完 Step 7-10 的 feature，其自身文档过 (a)-(d) 四条：(a) P2 修正入修订历史 / (b) B2 CLOSED / (c) D2 证据双源 / (d) H2 以能力边界携带。门禁不是空转的仪式——本 feature 恰有 2 P2 被 Step 4 独立 pass 抓获，证明检查链有效。

## 遇到的问题

- PowerShell 无 heredoc（`<<'EOF'` 解析失败）→ 改多 `-m` 参数提交，无损失
- 并行 Edit 竞态（DIS-008，见上）
- `search_semantic` 两轮空返回 + web 镜像四次超时 → arXiv/WebSearch/StackExchange API 多通道兜底，检索失败如实登记

## 下一步

- P-003（doc-contract Step A-G，含 G→DC 替换——关闭本 feature 唯一遗留 P3）
- P-001（Cpp_Hub 侧迁移指针，跨仓库现场动作）
- P-004（异基座 S1 复验 → M7 样本 ⑥）
- P-005 剩余半项："§0 计数改脚本生成"规则入 ADR-0007 修订候选
