# DEV-LOG-028: `dc_validator` M5 假阳性根因定位 + M7 §4 轻量候选登记

> **日期**: 2026-10-01（回补）
> **会话**: `specwf-p061-20261001.jsonl`（`tools/spec_runner/sessions/`，五步链 research → design → implement → verify → finalize）
> **涉及**: `docs/M7_EVIDENCE_LOG.md`（§4 待办挂钩新增候选③）/ `docs/PROGRESS.md`（P-061）/ `CODE_WIKI.md`（banner v1.107 → v1.108）/ `scripts/dc_validator.py`（**只读排查，未改**）；零代码
> **状态**: done（**回补说明**: 本份为 2026-10-01 统一回补批产出的事后叙事，非当时记录；事实源 = PROGRESS 行 + 对应 feature 四文档 + session 事件流 + CODE_WIKI banner 对应段；源中未出现的内容一律不写，无法确认处标「未核」）
> **源指针**: [PROGRESS P-061](../PROGRESS.md)、[M7 §4 待办挂钩](../M7_EVIDENCE_LOG.md)、[dc_validator](../../scripts/dc_validator.py)、[repo-stats DESIGN](../../spec/repo-stats/REPO_STATS_DESIGN.md)、[session 事件流](../../tools/spec_runner/sessions/specwf-p061-20261001.jsonl)

## 做了什么（时序）

1. **research 步（源码级排查 E1）**：定位 `check_links`（M5）的 `RE_MD_LINK` 为**朴素匹配**（不做 markdown 语义解析），**排除面仅三处**——围栏代码块 / 引文行 / `spec/templates/` ⇒ **行内反引号代码跨度不在其列**（属**未考虑**，非 by-design）；且 target **无形态过滤**（不要求含 `/` 或扩展名）⇒ 凡正文写出**右方括号紧跟左圆括号**的相邻字面量，即被拆为 label / target 且 resolve 不成立 ⇒ 报 **P2** ⇒ **pre-commit 阻断提交**（P-060 首跑被拦 3 条）。
2. **核实同族先例**：`repo-stats` DESIGN L186 记 **2026-08-22** P-014 起草期同一撞车（示意列改述）⇒ **同类复现 2 例 / 40 天**，两次均以改述规避、**均未登记**（隐性纪律）。机械探针：当前全仓潜在位点 **0**（本批已清零）。
3. **design 步**：定载体 = **`docs/M7_EVIDENCE_LOG.md` §4「待办挂钩」候选池**（用户裁决「M7 §4 轻量候选」），与既有两条候选同形；预登记修法否决项。
4. **implement 步**：M7 §4 新增**轻量候选**一条（来源 / 机制三要素 / ADR-0010 三问 / 预登记最小落地形态 / 本轮不做 / 登记理由）；PROGRESS 新增 P-061 行（V1a：先 `pending` 后回填 `done`）；`CODE_WIKI` banner v1.108 + `declared.progress_tasks` 60 → **61**（PT-11 两处）；补 session。**文本内避开完整「右方括号紧跟左圆括号」字面量**（分解为文字表述，避开 M5 误判）。
5. **verify 步**：三校验器全绿（`dc_validator` 尤其新增文本不再触发 M5；`m7_stats` hits 不变，§4 属 prose）；`console_gen` 与源一致；门禁链全 exit 0；零代码声明核对成立。

## 决策依据

### ① 为何登记「轻量候选」而非完整七段式观察项

**机制已定型**（源码级三要素明确、非未知待观察）⇒ 不需完整七段式观察项，登记为**轻量候选**（固化触发条件、缓存评估结论）即可。

### ② ADR-0010 三问

- **Q1 分层 = 双档**：方向 A「表述弱纪律」= **Layer-0**；方向 B「M5 增行内代码跨度排除」= **Layer-1**。
- **Q2 激活条件 = 触发驱动**：阈值 = 同类复现 **≥1 例**（已达 2 例）**或** 用户裁决。
- **Q3 未激活副作用 = 0**。

### ③ 预登记否决：方向 B′「target 形态过滤」

方向 B′（target 须含 `/` 或扩展名）**显式否决**——机械探针实测会**误伤 2 处真实链接**（`README.md` / `README.en.md` 的 `LICENSE` 目标：既无 `/` 又无 `.`，且真实存在）。

### ④ 边界：不改 `dc_validator`、不改 `AGENTS.md`

本批**只登记、不实施**任何工具改动（守 Layer-0；是否实施 A / B 待用户裁决）。

## 遇到的问题

- **根因的「未考虑」定性**：排除行内代码跨度**非 by-design**（IMPLEMENTATION 实施要点亦只列三处排除），已如实登记，避免被误读为有意取舍。
- **登记文本自身须规避触发形态**：候选条目的正文亦**不得**写出相邻形态，故以文字表述替代（否则新文本会自触发 M5）。

## 下一步

- 候选触发已在（同类 2 例）⇒ 是否实施**方向 A**（表述弱纪律，落 `AGENTS.md`）或**方向 B**（`check_links` 增行内代码跨度排除）须用户裁决。
- 当前全仓潜在位点 **0** ⇒ 无存量压力。
- 唯一真阻塞仍为 U-6；唯一硬期限仍为 ADR-0006 失效条件③（2026-11-15）。