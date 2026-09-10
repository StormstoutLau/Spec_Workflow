# 验收清单：board-generator / 任务看板生成器（L0 门禁钩子落地）

---
id: board-generator-CHECKLIST
type: design
version: 1.0
status: accepting
date: 2026-09-11
depends: [board-generator-IMPLEMENTATION, board-generator-DESIGN]
upstream: null
---

> **Feature**: board-generator / 任务看板生成器（P-041 实施批验收）
> **创建日期**: 2026-09-11
> **状态**: accepting（自查全绿；独立 pass 待触发——RULE-1 时序独立 / RULE-5 异基座）
> **Spec 步骤**: Step 7
> **验收对象**: [DESIGN.md](./DESIGN.md) v1.0 + [IMPLEMENTATION.md](./IMPLEMENTATION.md) v1.0

---

## 1. 交付物核对

| # | 交付物 | 存在 | 备注 |
|---|-------|------|------|
| 1 | `scripts/board_gen.py` | ✅ | stdlib only |
| 2 | `docs/BOARD.md` | ✅ | 纯派生产物（首生成 P 行 40 / session 16 / feature 31） |
| 3 | pre-commit 第五 hook `board-gen` | ✅ | `--stage`（生成 + git add） |
| 4 | `specwf-p041-20260911.jsonl` | ✅ | 五步 decision 链（research→finalize） |
| 5 | PROGRESS P-041 行 | ✅ | 状态 done |
| 6 | CODE_WIKI 同步 | ✅ | 版本头 / 目录树 / §9 索引 / stats 块 / 仓库性质行 |

## 2. 不变式验收（DESIGN §8）

| 不变式 | 验收方法 | 结果 |
|-------|---------|------|
| I-1 单写路径（仅写 `docs/BOARD.md`） | selftest S11：除 BOARD.md 外全仓文件字节零变化 | ✅ |
| I-2 确定性（禁 wall clock） | selftest S8 双跑字节一致 + S5 基准取源最大 ts | ✅ |
| I-3 幂等（内容未变不写盘） | selftest S7（首写 True / 二次 False）+ 端到端二次运行「无变化」 | ✅ |
| I-4 零依赖（stdlib only） | import 清单复核（无第三方） | ✅ |
| I-5 纯派生（覆盖无需备份） | 产物含「请勿手改」标注；100% 可重生成 | ✅ |
| I-6 不增真值 | 生成器对源全只读；改板不影响 PROGRESS/sessions/spec | ✅ |

## 3. 三校验器回归（R7 声明=重数）

| 校验器 | 命令 | 结果 |
|-------|------|------|
| DC 契约 | `python scripts/dc_validator.py` | 0 违规（含新增三件套 front-matter / 链接可解析） |
| M7 统计 | `python scripts/m7_stats.py` | 0 违规（本批零新增样本） |
| 视图层枚举 | `python scripts/repo_stats.py` | 0 违规（stats 块 declared + PT-8 同步到位） |

> 追加：`board_gen --selftest` 11/11 PASS；`board_gen --check` exit 0（板与源一致）。

## 4. 端到端「提交即刷板」验收（本批核心目标）

| 步骤 | 期望 | 实测 |
|------|------|------|
| 1. 真实源变更（PROGRESS 加 P-041 + 新 session） | 板内容应变化 | P 行 40→41 / session 16→17 ✅ |
| 2. 经 pre-commit 通道跑 hook | hook Passed | `Task board generator ... Passed` ✅ |
| 3. 板被重生成 | `docs/BOARD.md` 更新 | 基准行更新 + P-041 行出现 ✅ |
| 4. 板被**暂存**（提交将包含） | `git status` 显示已暂存 | `A  docs/BOARD.md` ✅ |
| 5. 幂等（二次） | 零变化、零扰动 | 「无变化」+ `--check` 一致 ✅ |

**结论：核心目标达成** —— 提交时自动刷板并暂存，**完全脱依赖用户指令**（RESEARCH C-7 / B9 落地验证）。

## 5. 残余风险与未覆盖项

| 项 | 说明 | 状态 |
|----|------|------|
| `--no-verify` 旁路 | 本地 hook = 诚实护栏非绝对强制（同仓内既有四 hook 边界，见 hook-surface RESEARCH） | 已知（不新引入） |
| H5 常驻开销 | L1（监听）/ L2（轮询）两档未实施故未实测 | 未实测（保留） |
| 板内容语义 | 板仅机械投影状态，不含推断；「阻塞原因」为状态直译非归因 | 设计内（§2.3 职责外） |
| 自动依赖发现 | 板不推断上游依赖（H4 未实测） | 不适用本批 |

## 6. 验收结论

**有条件通过（accepting）**：9 项交付/不变式全部实测通过；三校验器全绿；「提交即刷板」端到端达成。待 **独立 pass**（RULE-1 时序独立 + RULE-5 异基座）后转 accepted。

---

**验收签字**: 自查（`dc_validator` / `m7_stats` / `repo_stats` / `board_gen --selftest` 全绿）· 独立 pass 待触发
