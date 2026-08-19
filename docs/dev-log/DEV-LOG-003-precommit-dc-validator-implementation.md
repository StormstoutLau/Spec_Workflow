# DEV-LOG-003: precommit-dc-validator Step 5-7——实施落地 → dry-run 迭代 → 存量违规修复 → CHECKLIST 验收

> **日期**: 2026-08-19
> **会话**: Claude GLM-5.3（主控站）
> **涉及**: spec/precommit-dc-validator/（IMPLEMENTATION v1.1 + CHECKLIST v1.0）/ scripts/dc_validator.py / .pre-commit-config.yaml / adr/ADR-0004~0005 / spec/adr0006-pointer/ / docs/M7_EVIDENCE_LOG.md / docs/PROGRESS.md
> **状态**: CHECKLIST 有条件通过（自查 50+4 项全绿，机械证据 E1 可重放；RULE-1 独立 pass 挂 P-008）

---

## 做了什么（时序）

1. **Step 5 IMPLEMENTATION.md 编写**：以实施期三项机械取证开篇（E1 可重放）——① DC 契约范围实测（24 契约文件 = 14 首行式 + 10 标题后式，9 轻契约无 front-matter）；② §0 计数预跑（4 份调研文档对账，捕获 ADR0006 A=7 实为 8）；③ 断链预扫（真断链 2 / 引文内 3 / 模板占位 6）。YAML 解析选型落定 stdlib 手写（hermes venv 353s site 延迟实证 + 三值形态全覆盖 + `language: system` 不继承 pre-commit 环境）。
2. **Step 6 脚本 + hook 落地**：`scripts/dc_validator.py`（M1-M5 五模块 + CheckResult/Summary + TYPE_VOCAB 常量 + `--selftest` 13 fixture）+ `.pre-commit-config.yaml`（repo: local / language: system / files: `\.md$`）。pre-commit 4.6.2 装于 Python 3.12。
3. **dry-run 迭代清障**：首跑 5 处误报——README/CODE_WIKI/dev-log 的**装饰性 `---` 分隔线**被误判为 front-matter 围栏 → `parse_frontmatter` 加"开围栏后首个非空行必须为 `key: value` 形态"规则，误报清零，selftest F10 回归覆盖。剩余 3 处真违规定位修复（DR-5）。
4. **DR-5 存量违规修复**：ADR0006_POINTER_RESEARCH §0 A 计数 7→8（修正注附机械枚举口径）+ ADR-0004/0005 L21 断链 `../../SPEC_PROCESS.md` → `../SPEC_PROCESS.md`（findstr 定位 + Edit 修复）。
5. **DR-6 工具自身缺陷修复**：selftest 复验发现汇总打印"12/12 PASS"而实际输出 13 行 PASS——13 个 `expect()` 实调 vs 硬编码手填计数。修复 = `total[0] += 1` 自增机械计数（R7 同构应用于工具自身），实测 13/13。
6. **Step 7 CHECKLIST.md 编写 + 验收**：50 项 + Iron Law 4 盲区自查全过；验收决定 = **有条件通过**（条件 = RULE-1 独立 pass，与 IMPLEMENTATION v1.1"待独立 pass"状态同轴，不冒充 accepted）。
7. **登记收束**：M7 样本⑨入账（形态 II ×2：ADR0006 计数漏计 + selftest 硬编码；分桶 13→15，规律锚点补双实证）；PROGRESS P-007 → done + P-008（独立 pass）新登记；本 DEV-LOG。

## 决策依据

### ① 装饰性分隔线判定规则（M2 检测窗口收窄）

仅凭"前 10 行内 `---` 围栏"判定 front-matter 会把 README 式装饰分隔线误判入契约范围（首跑 5 误报）。收窄规则 = 开围栏后**首个非空行必须为 `key: value` 形态**，否则整体判非 front-matter。规则来源不是猜测——是 dry-run 实测误报的修复，且 F10 fixture 固化为回归测试。与 DIS-007 教训同构：规则必须由机械实例驱动，而非先验设计。

### ② DR-6：预注册风险的精确命中（本日最重要的发现）

[DESIGN §10.2](../../spec/precommit-dc-validator/DESIGN.md) 风险 1 预注册："校验器自身含计数/分类错误（形态 II 于'反幻觉工具'本身复发）"——v1.0 selftest **精确兑现**：打印 13 行 PASS 汇总却称 12/12，硬编码手填计数。三层意义：(a) 规律②"防幻觉机制自身不设防"的最极端实例——元断言逃逸到审查臂自身，即便该机制本身就是计数校验器；(b) 预注册风险不是纸面仪式——设计期声明的失效模式真实发生，证明 §10.2 风险表有效；(c) 修复方式 = R7 同构（计数由调用自增，不手填），原则从"管文档"外溢到"管工具"。M7 样本⑨双实证登记。

### ③ 环境隔离策略（python -S -E + Python 3.12 主验）

hermes venv Python 3.11 的 site 初始化延迟 353s（计时取证），`-S -E` 绕过后 PyYAML 不可用——两项事实共同锁定零依赖 + `-S -E` 运行形态。pre-commit hook 的 `language: system` entry 在系统 PATH 执行、不继承 pre-commit 安装环境，故选型不能依赖"装 pre-commit 的 Python"（IMPLEMENTATION §2.1 决策 3）。

## 遇到的问题

- **RunCommand 工具不可用**（icube.shellExec 报错）→ 全部 shell 操作走 mcp_research-tools `bash_exec`（cmd 环境）
- **Glob/LS/Grep 工具在本环境不稳定**（超时 / UTF-8 流错误）→ `dir /s /b` / `findstr /n` 兜底，输出重定向 `.tmp_*.txt` 再 Read
- **bash_exec 频发 REQUEST_TIMEOUT 但命令实际完成**（输出文件完整落盘）→ 以文件内容为完成判据，不重跑已成功的命令；MCP 层超时 ≠ 命令失败
- **GBK 控制台编码**（✅ 等字符 UnicodeEncodeError / 中文乱码）→ `io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` 包装或输出重定向文件
- .tmp_*.txt 临时文件随提交前清理

## 下一步

- **P-008**：P-007 产出独立 pass（RULE-1 时序独立，真异基座优先；含 Step 10 ADD 独立审计）→ 通过后 IMPLEMENTATION → verified、CHECKLIST → accepted
- **DR-2**（挂起）：C 类计数对账待 FWK-ASSERTION 统一 C 类标记格式
- **DR-1**（候选）：front-matter 检测窗口契约显式化（PLAN DC1 注记，另行裁决）
- Linux 实机 dry-run（工作站 A/B，可选非阻塞）
- 开放项待用户裁决：LANGGRAPH v1.1 A 计数自引用是否补登记 M7 样本⑩
