# 实施文档：下游符合性（ADR-0006 决策 5/6 落地）

---
id: downstream-compliance-IMPLEMENTATION
type: design
version: 1.1
status: draft
date: 2026-09-29
depends: [downstream-compliance-DESIGN, downstream-compliance-RESEARCH]
upstream: null
---

> **Feature**: 下游符合性（P-049）
> **创建日期**: 2026-09-26
> **状态**: 草稿
> **Spec 步骤**: Step 5-6
> **基于设计**: [DESIGN.md](./DESIGN.md)

---

## 1. 交付物

| # | 交付物 | 类型 | 说明 |
|---|--------|------|------|
| D1 | `scripts/downstream_compliance.py` | 新增 | J-1~J-4 可复算检查器 + 判定表骨架生成器（stdlib only，**无 hook 注册**） |
| D2 | `scripts/dc_validator.py` | 修改 | **单点化修复**：`.arc` 排除抽为 `EXCLUDE_DIRS` + `is_excluded()`，遍历与显式传参共用同一判定；selftest 增 F11（十三 → 十四 fixture） |
| D3 | `spec/downstream-compliance/` 四件套 | 新增 | 本目录（RESEARCH / DESIGN / IMPLEMENTATION / CHECKLIST） |
| D4 | `adr/ADR-0006-...md` | 修改 | 决策 5/6 proposed → **accepted**；新增 §B2 重审 #2；§F 收口；修订历史 |
| D5 | `docs/adr/README.md` | 修改 | ADR-0006 行状态同步（v1.1 定稿 + 落地） |

## 2. 实现要点

### 2.1 `check_consumer()`：J-1 两事实同函数内一次判定（I-1）

```python
for cp in c["copies"]:
    text = _read(full)
    has_ptr = POINTER_MARK in text                     # 事实一：指针存在
    rc, out = _git(root, "ls-files", "--", cp["path"])
    tracked = bool(out.strip())                        # 事实二：是否入库
    # 两事实在同一分支内合成判定 → 不构成「另一处 grep」
```

⇒ 直接消除重审 #1 的错误形态（把「grep 命中」当作 J-1 的全部）。

### 2.2 `is_excluded()` 单点化（D2）

```python
EXCLUDE_DIRS = (".git", "__pycache__", ".arc")

def is_excluded(rel):
    parts = str(rel).replace("\\", "/").split("/")
    return any(p in EXCLUDE_DIRS for p in parts[:-1])   # 末段为文件名，不参与
```

`gather_md_files()` 的 `os.walk` 剪枝与 `main()` 的显式传参过滤**共用本函数**——修掉「排除只在遍历生效」的语义分叉。

### 2.3 `emit_table()`：只写 stdout（I-2 / I-5）

按 `CONSUMERS` 逐副本生成三列骨架行（`上游版本（upstream + version）` 列自动填入权威源当前版本），**不写任何文件**。

## 3. 实测

### 3.1 首轮全量（`python scripts/downstream_compliance.py`，2026-09-26）

| 判据 | 对象 | 读数 | 判定 |
|---|---|---|---|
| J-1 | `docs/ASSERTION_EVIDENCE_FRAMEWORK.md` | 指针命中 + 已入库 | ✓ |
| J-1 | `docs/discoveries/007_...md` | 指针命中但**未入库** | ✗ |
| J-2 | `origin/main...HEAD` | `ahead=0 behind=0` | ✓ 已同步 |
| J-3 | AEF 副本 | 冻结 **1.1** / 权威 **1.4.2** | — 无判定表（待消费仓落盘） |
| J-3 | DIS-007 副本 | 冻结 **1.1** / 权威 **1.3** | — 无判定表（待消费仓落盘） |
| 决策5 | `docs/COMPLIANCE_TABLE.md` | 判定表缺失 | — 待消费仓落盘 |
| J-4 | since 2026-08-17（**裸日期**） | 回流 0 条 / 窗口内总提交 **39** 条〔**读数存疑**——裸日期漂移 + `--grep` 缺 `-E` 致标记恒 0，见 **§3.4**〕 | — 窗口内 0 次（未满窗不判负） |

**exit = 1**（唯一阻塞项 = J-1 未入库）。三态语义首轮即验：本批另有 exit 0（`--emit-table`）实测见 §3.2；exit 2 由「消费仓不可达」分支承担（设计 §7，未在本机触发）。

### 3.2 `--emit-table`（exit 0）

输出三列骨架，其中「上游版本」列自动填 `upstream=Spec_Workflow version=1.4.2` / `version=1.3`（与 §3.1 J-3 读数同源，保证**表与判据不脱钩**）。

### 3.3 单点化修复验证（D2）

| 场景 | 修复前 | 修复后 |
|---|---|---|
| 显式传入 `.arc` 文件（`D-008-...md`） | **18 违规**（P1=2 P2=16） | **0 文件，0 违规**（exit 0） |
| `pre-commit run --all-files`（dc-validator） | **Failed**（8 份副本累计 **47** 误判：P1=8 / P2=39） | **Passed** |
| selftest | 13 fixture / 13 断言 | **十四 fixture / 16 断言，16/16 PASS**（新增 F11/F11b/F11c） |
| 全量（无参） | 115 文件 0 违规 | 115 文件 0 违规（回归不变） |

### 3.4 J-4 判据缺陷修复（2026-09-29，P-056）

**触发** = P-056 复核批（ADR-0006 重审 #3）独立 pass 检出 J-4 读数异常 → 逐层复算定位。**两处实现缺陷（E2 实测）**：

| 编号 | 缺陷 | 机制 | 处置 |
|---|---|---|---|
| **DR-4** | **窗口起点用裸日期** | `--since=2026-08-17` 的时刻被 git `approxidate` 以**当前时钟补齐** ⇒ 截止点随执行时刻漂移：同一冻结仓（`HEAD=62891ea` 2026-08-23、全 history 116 commits、窗口内**无新提交**）实测 **09-26 上午 39 / 09-29 22:10 36 / 09-29 23:0x 35**。反证：`--since="2026-08-17 00:00:00 +0800"` = **40**、`… 12:00:00 +0800` = **39**、`… 2026-08-16 00:00:00 +0800` = 48 ⇒ 时刻确被补齐而非固定 | `CONSUMERS["reflux_since"]` 改**含时区的完整时刻** `"2026-08-17 00:00:00 +0800"`（DESIGN §4.2 同步约束） |
| **DR-5** | **`--grep` 缺 `-E`** | BRE 下竖线是**字面量**而非交替 ⇒ 三词交替模式（回流 / absorb / absorption）**恒不匹配**，回流标记**结构性假阴性**（原代码 `"✓" if hits` 的分支从未执行） | 命令补 `-E`（`--extended-regexp`）；读数改报**原始标记数**并注明「判读归人」 |

**同轮加固**：计数由 `len(stdout.splitlines())` 改为 **`git rev-list --count`**（取 git 权威整数——字符串切分对空行 / 分页器 / 解码差异无防护，非「声明 = 重数」所需形态）。

**修复后权威读数**（2026-09-29 复跑 `python scripts/downstream_compliance.py`）：

| 判据 | 对象 | 读数 | 判定 |
|---|---|---|---|
| J-4 | `since 2026-08-17 00:00:00 +0800` | 回流标记 **1** 条 / 窗口内总提交 **40** 条 | — 窗口内有标记 **1** 条（**判读归人**） |

> **判据语义不变**：标记 1 条 = `96edc5c`（**指针提交自身**，其 subject 含「回流经 Discovery/ADR 流程」）⇒ **有效回流 = 0**，与 [RESEARCH §3.4](./RESEARCH.md) A-5 结论一致；工具只报**原始标记数**、**不代判**「有效回流」（守 「不代裁定」边界，§5）。**连带订正** = §3.1 的「39」与 [ADR-0006 §B3](../../adr/ADR-0006-assertion-framework-dual-copy-authority.md) 的「35」均系裸日期漂移产物，权威值为 **40**。

## 4. 实施期发现

| 编号 | 发现 | 处置 |
|------|------|------|
| **DR-1** | 首版 `main()` 以 `if all_struct: return 2` 先判，会把 `blocking` 列表**掩盖**（结构性提示压住了明确的不满足项） | 调整判定序：**blocking 优先 → exit 1**，structural 次之 → exit 2（明确失败优先于不可判定） |
| **DR-2** | J-3 初版在判定表缺失时把版本差异记为 `✗ 差异未记录` 并计入 blocking——属**双重归因**：无表则「是否已记录」本就无从判定，报「未记录」是伪结论 | 改为 `— 无判定表（待消费仓落盘）`（不 block）+ 表缺失归 `structural`。**这是「缺失不得冒充失败」的实例** |
| **DR-3** | J-3 首次给出权威源版本读数，暴露 **AEF 1.4.2 / DIS-007 1.3 vs 副本冻结 1.1** 的差异量此前**无任何记录** | 读数入 RESEARCH §3.3；差异的正确处置归消费仓（决策 5），本仓只报不断 |

## 5. 边界与未做

- **不碰 `.pre-commit-config.yaml`**：本脚本不进 hook（守 ADR-0006 §D 定位 + DESIGN §6.2 否决理由）；
- **不写消费仓**：含判定表（I-5）；`--emit-table` 只写 stdout；
- **不代裁定**：J-3 只报「有差异 / 已记录 / 未记录」，**不判**该差异是否可接受；
- **未做**：J-5（结构化差异，仅版本号外的内容比对）登记为 H1；跨机路径可移植性未处理（不可达即 exit 2）。

---

**Review 签字**: _________ 日期: _________
