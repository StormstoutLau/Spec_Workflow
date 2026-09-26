#!/usr/bin/env python3
"""下游符合性检查器（ADR-0006 决策 5/6 落地，P-049）。

职责：
  - 把 ADR-0006 §D 的 J-1~J-4 判据从「纪律 + 手记」变成**可复算命令**（机械 exit code）。
  - 决策 5 的「符合性判定表」只提供**三列格式 + 骨架生成器**（`--emit-table`）；
    **判定表本体归各消费仓**，本仓不代填、不代判。

判据（ADR-0006 §D，J-3 已泛化为「任意副本」）：
  J-1  指针存在**且已入库**      工作区 grep + `git ls-files`
  J-2  提交**已推送**            `git rev-list --left-right --count origin/<b>...HEAD` = 0 0
  J-3  版本行一致性              副本冻结版本 vs 权威源当前版本；差异须在判定表**有记录**
  J-4  回流频度                  窗口内 `git log --grep` 回流标记 ≥1

零第三方依赖（stdlib + 本机 git）；**不接三校验器**（ADR-0006 §D「纪律 + 可复算命令」定位）。

exit 0 = 全部满足；1 = 有阻塞项（未记录差异 / 指针缺失）；2 = 结构性异常（消费仓不可达/非 git 仓）。

用法：
  python scripts/downstream_compliance.py                 # 全量 J-1~J-4
  python scripts/downstream_compliance.py --emit-table    # 输出判定表三列骨架（供消费仓落盘）
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 本仓根（权威源侧）

# ── 消费仓登记（新增消费仓 = 加一条；登记面极小、可审）──────────────────
CONSUMERS = [
    {
        "name": "Cpp_Hub",
        "root": r"F:\Cpp_Hub",
        "branch": "main",
        "table": "docs/COMPLIANCE_TABLE.md",      # 判定表（归消费仓；本仓只读）
        "copies": [
            {"path": "docs/ASSERTION_EVIDENCE_FRAMEWORK.md",
             "authority": "docs/ASSERTION_EVIDENCE_FRAMEWORK.md"},
            {"path": "docs/discoveries/007_hallucination_audit_asymmetric_evidence.md",
             "authority": "docs/007_hallucination_audit_asymmetric_evidence.md"},
        ],
        "reflux_since": "2026-08-17",             # 决策 4 回流通道首次批量使用日
        "reflux_pattern": "回流|absorb|absorption",
    },
]

POINTER_MARK = "权威源已迁移"
RE_FROZEN = re.compile(r"冻结于\s*v?([0-9][0-9.]*)")
RE_VERSION = re.compile(r"^(?:version|版本):\s*v?([0-9][0-9.]*)\s*$", re.MULTILINE)


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def _git(root, *args):
    """返回 (rc, stdout)。git 不可用/非仓 → rc!=0。"""
    try:
        p = subprocess.run(["git", "-C", root, *args],
                           capture_output=True, text=True)
        return p.returncode, p.stdout
    except OSError:
        return 127, ""


def _frozen_version(text, max_lines=12):
    """副本冻结版本：优先指针行内「冻结于 vX.Y」，缺则取头部 version/版本 行。"""
    for ln in text.splitlines()[:max_lines]:
        if POINTER_MARK in ln:
            m = RE_FROZEN.search(ln)
            if m:
                return m.group(1)
    m = RE_VERSION.search("\n".join(text.splitlines()[:max_lines]))
    return m.group(1) if m else None


def _authority_version(rel):
    text = _read(os.path.join(ROOT, rel))
    if text is None:
        return None
    m = RE_VERSION.search("\n".join(text.splitlines()[:40]))
    return m.group(1) if m else None


def check_consumer(c):
    """返回 (rows, blocking, structural)。rows = [(判据, 对象, 读数, 判定)]。"""
    name, root = c["name"], c["root"]
    rows, blocking, structural = [], [], []
    if not os.path.isdir(root):
        return rows, blocking, ["消费仓不可达: %s" % root]

    table_text = _read(os.path.join(root, c["table"]))
    has_table = table_text is not None

    # ── J-1 指针存在且已入库 ──────────────────────────────────────────
    for cp in c["copies"]:
        full = os.path.join(root, cp["path"])
        text = _read(full)
        if text is None:
            rows.append(("J-1", cp["path"], "工作区不存在", "✗ 缺失"))
            blocking.append("J-1 %s: 副本不存在" % cp["path"])
            continue
        has_ptr = POINTER_MARK in text
        rc, out = _git(root, "ls-files", "--", cp["path"])
        tracked = bool(out.strip())
        if has_ptr and tracked:
            rows.append(("J-1", cp["path"], "指针命中 + 已入库", "✓"))
        elif has_ptr and not tracked:
            rows.append(("J-1", cp["path"], "指针命中但**未入库**（仅本地生效）", "✗ 未入库"))
            blocking.append("J-1 %s: 指针未入库" % cp["path"])
        else:
            rows.append(("J-1", cp["path"], "无指针", "✗ 无指针"))
            blocking.append("J-1 %s: 无指针" % cp["path"])

    # ── J-2 提交已推送 ────────────────────────────────────────────────
    rc, out = _git(root, "rev-list", "--left-right", "--count",
                   "origin/%s...HEAD" % c["branch"])
    if rc != 0:
        structural.append("J-2 %s: 无法比对 origin/%s（无 remote 或未 fetch）" % (name, c["branch"]))
    else:
        ahead, behind = (out.split() + ["?", "?"])[:2]
        ok = (ahead == "0" and behind == "0")
        rows.append(("J-2", "origin/%s...HEAD" % c["branch"],
                     "ahead=%s behind=%s" % (ahead, behind), "✓ 已同步" if ok else "✗ 未同步"))
        if not ok:
            blocking.append("J-2 %s: 与 origin/%s 不同步（ahead=%s）" % (name, c["branch"], ahead))

    # ── J-3 版本行一致性（差异须在判定表有记录）──────────────────────
    for cp in c["copies"]:
        text = _read(os.path.join(root, cp["path"]))
        if text is None:
            continue
        fz, au = _frozen_version(text), _authority_version(cp["authority"])
        if fz is None or au is None:
            rows.append(("J-3", cp["path"], "冻结=%s 权威=%s（解析不全）" % (fz, au), "? 无法判定"))
            structural.append("J-3 %s: 版本行解析不全" % cp["path"])
            continue
        same = (fz == au)
        if same:
            rows.append(("J-3", cp["path"], "冻结=%s 权威=%s" % (fz, au), "✓ 一致"))
        elif not has_table:
            rows.append(("J-3", cp["path"], "冻结=%s 权威=%s" % (fz, au), "— 无判定表（待消费仓落盘）"))
        else:
            recorded = os.path.basename(cp["path"]) in (table_text or "")
            rows.append(("J-3", cp["path"], "冻结=%s 权威=%s" % (fz, au),
                         "✓ 差异已记录" if recorded else "✗ 差异未记录"))
            if not recorded:
                blocking.append("J-3 %s: 版本差异(%s≠%s)且判定表未记录" % (cp["path"], fz, au))

    if not has_table:
        rows.append(("决策5", c["table"], "判定表缺失", "— 待消费仓落盘"))
        structural.append("%s: 判定表未落盘（%s）——用 --emit-table 生成骨架交现场填"
                          % (name, c["table"]))

    # ── J-4 回流频度 ──────────────────────────────────────────────────
    rc, out = _git(root, "log", "--since=%s" % c["reflux_since"],
                   "--oneline", "--grep=%s" % c["reflux_pattern"], "-i")
    total_rc, total = _git(root, "log", "--since=%s" % c["reflux_since"], "--oneline")
    if rc != 0:
        structural.append("J-4 %s: git log 失败" % name)
    else:
        hits = [l for l in out.splitlines() if l.strip()]
        rows.append(("J-4", "since %s" % c["reflux_since"],
                     "回流提交 %d 条 / 窗口内总提交 %d 条" % (len(hits), len(total.splitlines())),
                     "✓" if hits else "— 窗口内 0 次（未满窗不判负）"))
    return rows, blocking, structural


def emit_table():
    print("# 符合性判定表（ADR-0006 决策 5，三列格式）\n")
    print("> 本表**归消费仓持有**；`Spec_Workflow` 只提供格式与骨架。填表即声明「已采信/已偏差」，")
    print("> 差异项必须落在此表 C-2 列，否则 J-3 判为「差异未记录」。\n")
    for c in CONSUMERS:
        print("## %s\n" % c["name"])
        print("| 上游版本（upstream + version） | 本仓采信或偏差项 | 裁定依据与日期 |")
        print("|---|---|---|")
        for cp in c["copies"]:
            au = _authority_version(cp["authority"]) or "?"
            print("| `%s` upstream=Spec_Workflow version=%s | （待填：采信 / 偏差说明） | （待填：依据 + 日期） |"
                  % (cp["path"], au))
        print()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="downstream_compliance",
                                 description="下游符合性检查（ADR-0006 J-1~J-4）")
    ap.add_argument("--emit-table", action="store_true", help="输出判定表三列骨架")
    args = ap.parse_args(list(sys.argv[1:] if argv is None else argv))

    if args.emit_table:
        emit_table()
        return 0

    all_rows, all_blocking, all_struct = [], [], []
    for c in CONSUMERS:
        rows, blocking, structural = check_consumer(c)
        all_rows += [("%s" % c["name"],) + r for r in rows]
        all_blocking += blocking
        all_struct += structural

    print("下游符合性检查（J-1~J-4，ADR-0006 §D）")
    print("=" * 72)
    for name, j, obj, reading, verdict in all_rows:
        print("  [%s] %-10s %-52s %s" % (j, name, obj[:52], verdict))
        print("        %s" % reading)
    if all_blocking:
        print("\n[阻塞项] exit 1")
        for b in all_blocking:
            print("  - %s" % b)
        return 1
    if all_struct:
        print("\n[结构性提示] exit 2")
        for s in all_struct:
            print("  - %s" % s)
        return 2
    print("\n全部判据满足（J-1~J-4）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
