---
id: adr0006-pointer-RESEARCH
type: design
version: 1.0
status: in-review
date: 2026-08-16
depends: [ADR-0006, FWK-ASSERTION, DIS-007, cpp-hub-gap-analysis]
upstream: null
---

# ADR-0006 决策 3 跨仓库指针动作——执行前调研文档 v1.0 (2026-08-16)

> **任务**: 展开"Cpp_Hub 侧两文件加迁移指针"这一遗留跨仓库动作的完整分析，定义可验收的执行方案
> **性质**: 待办事项 P-001 的设计文档（登记于 docs/PROGRESS.md）
> **审计状态**: `自查（单视角）`

## 0. 断言统计表

| 级别 | 条数 | 说明 |
|------|------|------|
| A 事实类 | 8 | 本地路径 + 引文锚定（v1.1 修正：原计 7 漏数 §3 L61-L62 两条治理载体断言，机械枚举 `【A】` 行标 = 8） |
| B 推断类 | 2 | B1-B2，登记于附录 B |
| C 判断类 | 3 | 执行选项与推荐 |
| 假设区 | 2 | H1-H2 |

---

## 1. 动作定义（ADR-0006 决策 3 原文）

【A】(源: f:/Spec_Workflow/adr/ADR-0006-assertion-framework-dual-copy-authority.md 决策 3; 引文: "**指针封堵**：Cpp_Hub 侧两文件头部各加一行'权威源已迁移至 Spec_Workflow 仓库'（G3 档 2 标注的反向操作）")

**对象**:

| # | 文件 | 插入位置 | 指针性质 |
|---|------|---------|---------|
| P1 | f:/Cpp_Hub/docs/ASSERTION_EVIDENCE_FRAMEWORK.md（v1.1, 304 行） | L3 版本行之后 | 副本冻结于 v1.1；权威源 = Spec_Workflow 仓库 v1.2+；新演进经权威仓库回流 |
| P2 | f:/Cpp_Hub/docs/discoveries/007_hallucination_audit_asymmetric_evidence.md（v1.1, 88 行） | L4 版本行之后 | 同上 |

## 2. 为什么必须做——失效声明与分叉实证

【A】源侧 007 头部仍声称已失效的同步关系：
(源: f:/Cpp_Hub/docs/discoveries/007_...md L4; 引文: "**版本**: v1.1 (2026-08-16; 公共承载 = docs/ASSERTION_EVIDENCE_FRAMEWORK.md v1.1, 两者同步维护)")
——ADR-0006 生效后"同步对"已迁至本仓库（v1.2），此句成为**主动撒谎的文档**。

【A】源侧框架 §9 同样声称内部同步：
(源: f:/Cpp_Hub/docs/ASSERTION_EVIDENCE_FRAMEWORK.md L303-304; 引文: "两者以编号互引, 版本同步维护 (当前均 v1.1)")

【A】消费侧已锚定过期版本号——pilot 报告头部引用框架 v1.1：
(源: f:/Cpp_Hub/docs/research/ADR019_REVIEW_PILOT.md L5-6; 引文: "> **上游**: [PHASE7C_RESEARCH.md](./PHASE7C_RESEARCH.md) v1.1 (已经 3 agent 126 条全量审计) / [ASSERTION_EVIDENCE_FRAMEWORK.md](../ASSERTION_EVIDENCE_FRAMEWORK.md) v1.1")

【A】Cpp_Hub 是持续演化的活项目（流程文档同日双版本）：
(源: DEVELOPMENT_WORKFLOW.md L3-4; 引文: "> **版本**: 1.1 / > **日期**: 2026-08-16 (v1.1: 新增阶段 0 调研证据审计 + R1-R4 门禁…; v1.0 2026-07-29)")

【A】ADR-0006 已预注册本动作失效时的退化结局：
(源: ADR-0006 失效条件; 引文: "Cpp_Hub 侧拒绝/遗漏指针且持续迭代 → 降级为'声明式权威'（单方维护，接受滞后）")

【B1】**分叉已在发生**（见附录 B）：pilot 提出的 STEP_GAP 分型只存在于 Cpp_Hub 侧提案，权威源 v1.2 无此内容——双谱系的第一个具体分歧点已经出现，指针延迟越久，"哪边是真的"越难回答。

## 3. 治理性约束——为什么不顺手改掉

【A】Cpp_Hub 有自己的工程治理载体：git 仓库 + CI（f:/Cpp_Hub/.github/workflows/ci.yml，Glob 实证）+ 开发日志（docs/DEVELOPMENT_LOG.md，1500+ 行）。
【A】Cpp_Hub 仓库根**无 AGENTS.md / CLAUDE.md 类会话指令文件**（本会话早前 f:/ LS 快照：根目录仅 README/BUILD_PLAN/PROJECT_PLAN/TRACEABILITY_REPORT 四个 md）——指针无现成指令层落点，只能落文档头部 + 该项目 dev-log。
【C】越权判断：Spec_Workflow 会话直接改动乃至提交另一仓库，绕过其提交规范与进行中工作状态（working tree 是否干净未验证，见 H1）。指针的技术写入成本 O(1)，治理成本才是主体。

## 4. 执行选项（C 类）

| 选项 | 内容 | 代价/风险 |
|------|------|----------|
| O1 本会话直改并提交 | 直接编辑 P1/P2 并在 Cpp_Hub 仓库 commit | 越权；working tree 状态未验证；指令层仍缺 |
| O2 携带式交办 | 产出指针文本 + 交办卡，用户转交 Cpp_Hub 现场会话执行 | 依赖转交——正是 ADR-0006 失效条件"回流频度不足"警惕的模式 |
| **O3 两段式（推荐）** | 本会话写入两行指针（**仅工作区，不 commit**）+ 交办卡；现场会话复核、提交、登记其 dev-log | 现场困惑可用交办卡消除；治理链完整 |

**推荐理由**（C 类 rationale）: O3 把"机械部分"（两行文本，无歧义）与"治理部分"（提交、登记、指令层）分离——前者立即消除失效声明，后者留给有权限的现场。若用户明确授权本会话代表其执行 Cpp_Hub 侧提交（同一所有者），O1 降级为可行，但仍建议同步登记 DEVELOPMENT_LOG。

## 5. 指针文本（P1/P2 通用，可直接粘贴）

```markdown
> **⚠️ 权威源已迁移**: 本文件为历史副本，冻结于 v1.1。权威版本 = Spec_Workflow 仓库
> (github.com/StormstoutLau/Spec_Workflow) docs/ASSERTION_EVIDENCE_FRAMEWORK.md v1.2+。
> 本项目新发现/改进经 Discovery 或 ADR 流程回流权威仓库（ADR-0006），勿在此副本上继续演化。
```

（P2 版本将首行文件名换为 007 对应路径；两处"同步维护"句保留原文不动——历史声明由指针覆盖解释，不篡改历史。）

## 6. 验收标准（P-001 完成定义）

- [ ] P1/P2 头部指针存在（grep "权威源已迁移" 于两文件各 1 命中，E1）
- [ ] Cpp_Hub 侧提交完成（该仓库 git log 可溯，E1）
- [ ] Cpp_Hub DEVELOPMENT_LOG 登记本次变更（E1）
- [ ] 本仓库 ADR-0006 修订历史追记"决策 3 已执行"（E1）
- [ ] pilot 头部 v1.1 引用是否随动 → 记开放项（引用是历史快照，可不改；由现场会话裁量）

## 7. 关联与升级路径

- 本动作是 P3-10（消费方通知机制）的**首个试点实例**；其做成形态将模板化进 ADR-0007 职责边界节（doc-contract PLAN §8-4）。
- 回流通道（ADR-0006 决策 4）的首次真实使用 = STEP_GAP 分型回流（差距分析报告 §5-1）——与指针动作同属"跨仓库协议"的第一批两个事务。

## 附录 B: 断言登记表（机器可读）

```assertions
[
  {
    "id": "B1",
    "conclusion": "双谱系首个具体分歧点已出现: STEP_GAP 分型仅存在于 Cpp_Hub pilot 提案, 权威源 v1.2 无此内容, 且消费侧文档锚定 v1.1",
    "op": "existence",
    "claimed_chain": [
      {"step": 1, "text": "pilot §5.1-3 提出两态分型并建议框架采纳", "source": "ADR019_REVIEW_PILOT §5.1"},
      {"step": 2, "text": "权威源 v1.2 为本会话逐行 Write, 无分型表述", "source": "框架 v1.2 全文"},
      {"step": 3, "text": "pilot 头部上游引用锚定 v1.1", "source": "pilot L5-6"}
    ],
    "sources": [
      {"label": "pilot §5.1", "path": "f:/Cpp_Hub/docs/research/ADR019_REVIEW_PILOT.md", "url": null, "quote": "建议框架 v1.2 将 STEP_GAP 细分为 'gap-closed' (无需仲裁) 与 'gap-open' (需仲裁) 两态"},
      {"label": "pilot L5", "path": "f:/Cpp_Hub/docs/research/ADR019_REVIEW_PILOT.md", "url": null, "quote": "[ASSERTION_EVIDENCE_FRAMEWORK.md](../ASSERTION_EVIDENCE_FRAMEWORK.md) v1.1"}
    ],
    "probe": {"type": "existence", "files": ["f:/Spec_Workflow/docs/ASSERTION_EVIDENCE_FRAMEWORK.md"], "params": {"symbols": ["gap-closed", "gap-open"], "claim": "absent", "candidates": [{"name": "权威源", "path": "f:/Spec_Workflow/docs"}]}}
  },
  {
    "id": "B2",
    "conclusion": "指针无现成指令层落点: Cpp_Hub 仓库根不存在 AGENTS.md/CLAUDE.md 类会话指令文件, 指针只能落文档头部 + dev-log 登记",
    "op": "existence",
    "claimed_chain": [
      {"step": 1, "text": "本会话 f:/ LS 快照显示 Cpp_Hub 根目录 md 仅 4 份 (README/BUILD_PLAN/PROJECT_PLAN/TRACEABILITY_REPORT)", "source": "f:/ LS 快照"},
      {"step": 2, "text": "无 AGENTS.md/CLAUDE.md → 会话启动加载层无指针载体", "source": "同上"}
    ],
    "sources": [
      {"label": "f:/ LS", "path": "f:/Cpp_Hub", "url": null, "quote": "根目录: README.md, BUILD_PLAN.md, CMakeLists.txt, LICENSE, PROJECT_PLAN.md, TRACEABILITY_REPORT.md"}
    ],
    "probe": {"type": "existence", "files": ["f:/Cpp_Hub"], "params": {"symbols": ["AGENTS.md", "CLAUDE.md"], "claim": "absent", "candidates": [{"name": "Cpp_Hub 根", "path": "f:/Cpp_Hub"}]}}
  }
]
```

## 附录 C: 假设区

- [H1] Cpp_Hub working tree 当前是否干净未验证（含未提交演进的 git status 未知）— 查证路径: `git -C f:/Cpp_Hub status` 后再决定 O1/O3
- [H2] Cpp_Hub 会话的指令加载机制（若存在仓库外机制如全局 CLAUDE 配置）未经取证 — 查证路径: 询问用户该项目会话如何加载项目约定

---

**Review 签字**: _________ 日期: _________
