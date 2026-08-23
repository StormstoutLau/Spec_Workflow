# DEV-LOG-007: promptfoo M7 对比臂声明式评测——调研 → spec 四件套 → pf_m7_eval.py 落地 → Review 轮拦截修复 → 样本㉔ 登记

> **日期**: 2026-08-23
> **会话**: Claude GLM-5.3（主控站）
> **涉及**: spec/promptfoo-m7-eval/（RESEARCH/DESIGN/IMPLEMENTATION/CHECKLIST + promptfooconfig.yaml）/ scripts/pf_m7_eval.py / CODE_WIKI.md（v1.8：§2.1 树 + §4.7 + §9 索引 + §10 stats 块 declared 11/7/4）/ docs/M7_EVIDENCE_LOG.md / docs/PROGRESS.md / README.md / README.en.md / docs/assets/readme/evidence.svg / .gitignore（新建）
> **状态**: CHECKLIST v1.1 accepting（35/35 有条件通过；缺端点实评，方案 Z 门控——不假造；RULE-1 独立 pass 待触发，同 P-014 收口先例）

---

## 做了什么（时序）

1. **Step 1-2 RESEARCH**（5A+1B+4C+2H）：promptfoo 声明式评测能力面查证（YAML 测试矩阵 / provider 变量注入 / 断言库 / CLI JSON 输出）+ 本仓适配点（M7 对比臂样本来源 = provider.label 机械区分 base-model/cross-model；LG H5 假设 = 异基座审查臂可发现同基座盲区，触发条件样本≥10 已满足）。关键发现：LM Studio env 三件套重定向可绕过 promptfoo 沙箱 SQLite 写入（RESEARCH A4）；端点不可达时方案 Z = 门控阻断而非假造基线。
2. **Step 3-4 DESIGN**：双 provider 臂矩阵（base-model/cross-model）+ run/record/selftest 三子命令契约 + EvalRecord/EvalSummary dataclass + 不变式 I-1~I-6（I-4 机械解析不经 LLM 转述 / I-6 双臂门控）+ 方案 Z 范围声明（首轮评测端点就绪触发）。
3. **Step 5-9 IMPLEMENTATION + TDD**：`scripts/pf_m7_eval.py` 275 行（PM1-PM5），selftest 13 断言 / 6 fixture（F1-F6：解析/门控/兜底/异常路径，不依赖外部端点）+ `promptfooconfig.yaml` 双臂矩阵模板。
4. **Review 轮（用户指令「review上一轮工作」，2026-08-23）**：dc_validator 全量首跑（55 文件）+ repo_stats 首跑 + 逐行代码审查，捕获 **P1×2 + P2×3 + P3×3**：
   - P1×2：RESEARCH 附录 A/H 标记形态违规（`**A1**` 粗体 ≠ 行首【A】契约、`**H1**` ≠ `[H1]` 方括号契约，M4 重数 0 ≠ 声明）——上轮验收只单文件验了 CHECKLIST，新增 4 文件未逐个过契约致逃逸；
   - P2×3：config 缺异基座臂 provider（DESIGN §4.2 双臂只落一臂）/ promptfoo 未安装 FileNotFoundError 兜底未实施 / 顶层 try/except 兜底未实施；
   - P3×3：env_prefix 死参数 / tempfile 未用 import / record 旗标 --input ≠ DESIGN 的 --results。
   全部修复 + 活靶复验（F6 + 目录当 --results → exit 2 实测）。P2×2 兜底补齐后 DESIGN §7 全四行错误处理活靶实测通过。
5. **裁决与入账**：Review 轮 8 项发现入 **M7 样本㉔**（形态 II=0——格式契约违规非形态 II，同⑭⑮ 处置不入 §2 分桶；㉓ 已被 P-014 独立 pass 批占用，编号顺延）；hits 块 `m7_stats.py --write` 重生成（samples 23→24 / form2_total 62 不变）。
6. **Step 10 收束批**：CHECKLIST v1.1 accepting + IMPLEMENTATION v1.1（status in-review 待独立 pass）+ PROGRESS P-010 done（主动队列清空）+ CODE_WIKI v1.8（§2.1 树 + §4.7 工具入册 + §9 索引 + §10 declared 11 目录/7 dev-log/4 scripts）+ 门面三件刷新（README×2 + evidence.svg 23→24）+ 本 DEV-LOG + `.gitignore` 新建（.promptfoo/ 沙箱 + __pycache__）。

## 决策依据

### ① 方案 Z（门控不假造）

三机 LM Studio 端点实测不可达（沙箱环境）。处置 = run 子命令双臂 TCP 预检，任一臂不可达即 `[P1] 端点不可达` + exit 1，不调 promptfoo、不生成占位 results——「首轮评测入 M7」验收项如实标记为端点就绪触发。与 RESEARCH A5 一致：假造基线 = 污染 M7 对比臂数据。

### ② 机械解析（I-4）

record 子命令直取 results.json 的 provider.label / gradingResult.pass / latencyMs / cost 字段，不经 LLM 转述——M7 登记草案生成与三校验器同构（声明 = 机械重数）。登记纪律：草案仅打印不入账，人工核对后追加（LLM 产出不直写账本）。

### ③ 评测运行器与三校验器分工（非 hook）

pf_m7_eval 不进 pre-commit：dc_validator/m7_stats/repo_stats 是提交瞬间看护（确定性输入、秒级），pf_m7_eval 是外部依赖运行器（promptfoo CLI + LLM 端点 + 分钟级）——触发条件与作用域均不同，hook 化会阻断提交流。CODE_WIKI §4.7 明确此分工。

## 遇到的问题

- **上轮验收逃逸模式（P1×2 根因）**：验收时 dc_validator 只单文件跑了 CHECKLIST，RESEARCH/DESIGN/IMPLEMENTATION/config 四个新增文件未逐个过契约——「新文件全量首跑」应成为实施轮标准动作（同⑨⑫⑮ 工具拦截性质，如实标注入 M7 样本㉔）。
- **设计-实施偏差（P2×3 根因）**：DESIGN §4.2 双 provider 与 §7 全四行错误处理在设计文档中均无歧义，纯实施侧漏落——逐行 code review（非仅 selftest 绿即过）仍不可替代；selftest 13 断言是设计后补的契约面，设计文档自身才是完整契约源。
- **repo_stats verify 误当子命令**：`repo_stats.py verify` 会把 verify 解析为文件参数跳过全量对账——正确用法是无参数裸跑（P-014 收口批同款坑，复现确认）。
- **样本编号占用冲突**：入账时㉓ 已被 P-014 独立 pass 批登记，Review 轮样本顺延为㉔——入账前先读账本末行（不凭记忆续号，形态 II 风格错误的 LLM 变体）。

## 下一步

- RULE-1 独立 pass（真异基座优先，DeepSeek V4 Pro 先例）：四件套 + 脚本复核 → IMPLEMENTATION in-review → verified / CHECKLIST accepting → accepted。
- 端点就绪触发首轮评测（run 双臂实评 → record 机械解析 → M7 登记 → LG H5 假设实测：异基座审查臂 vs 同基座盲区）。
