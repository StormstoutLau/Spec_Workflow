# 实施文档：下游符合性（ADR-0006 决策 5/6 落地）

---
id: downstream-compliance-IMPLEMENTATION
type: design
version: 1.0
status: draft
date: 2026-09-26
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
| J-4 | since 2026-08-17 | 回流 0 条 / 窗口内总提交 **39** 条 | — 窗口内 0 次（未满窗不判负） |

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
