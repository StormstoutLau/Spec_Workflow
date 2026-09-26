#!/usr/bin/env python3
"""ARC 快照漂移核查（ADR-0006 §D J-3 的本仓实例，2026-09-26）。

职责：
  - 比对 `adr/*.md`（权威源）与 `tools/arc/data/.arc/decisions/*.md`（ARC 导入时点快照）
    的版本行，使本仓派生物的漂移**机械可见**（J-3 泛化：由「跨仓下游副本」扩为「任意副本」）。
  - 只读零副作用；**零 ARC 二进制依赖**（纯文本比对），**不接三校验器**（守 P-035 D6）。

语义：`.arc` 是**导入时点快照（不追平）**——本命令不修复漂移，只如实报告。
  exit 0 = 8/8 一致；exit 1 = 检出漂移；exit 2 = 结构性异常（副本缺失/多余）。

零依赖 stdlib only。用法：
  python tools/arc/arc_drift_check.py
"""
import os
import re
import sys

ARC_DIR = os.path.dirname(os.path.abspath(__file__))
RECROOT = os.path.dirname(os.path.dirname(ARC_DIR))   # tools/arc → 仓根
ADR_DIR = os.path.join(RECROOT, "adr")
SNAP_DIR = os.path.join(ARC_DIR, "data", ".arc", "decisions")

# 权威源前置块与 ARC 快照嵌入块皆以 `id: ADR-XXXX` + 紧随其后的 `version:` 标识；
# 位置不固定（本仓 ADR 存在「标题在前」与「front-matter 在前」两种布局）→ 按 id 锚点后搜 version。
ID_RE = re.compile(r"^id:\s*(ADR-\d{4})\s*$", re.MULTILINE)
VER_RE = re.compile(r"^version:\s*(\S+)\s*$", re.MULTILINE)


def read_version(path: str):
    """返回 (adr_id, version)；id 锚点后首个 version 行。缺失返回 (None, None)。"""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = ID_RE.search(text)
    if not m:
        return None, None
    v = VER_RE.search(text, m.end())
    return m.group(1), (v.group(1) if v else None)


def collect(directory: str, pattern) -> dict:
    out = {}
    if not os.path.isdir(directory):
        return out
    for name in os.listdir(directory):
        if not pattern.search(name):
            continue
        aid, ver = read_version(os.path.join(directory, name))
        if aid:
            out[aid] = (ver, name)
    return out


def main() -> int:
    src = collect(ADR_DIR, re.compile(r"ADR-\d{4}.*\.md$"))
    snap = collect(SNAP_DIR, re.compile(r"D-\d{3}.*\.md$"))
    if not src or not snap:
        print(f"[arc_drift] 结构性异常：权威源 {len(src)} 份 / 快照 {len(snap)} 份", file=sys.stderr)
        return 2

    keys = sorted(set(src) | set(snap))
    drift, missing = [], []
    print(f"{'ADR':<9} {'权威源':<9} {'快照':<9} 状态")
    print("-" * 44)
    for k in keys:
        s = src.get(k)
        c = snap.get(k)
        if s is None:
            print(f"{k:<9} {'—':<9} {c[0] or '—':<9} 快照多余")
            missing.append(k)
            continue
        if c is None:
            print(f"{k:<9} {s[0] or '—':<9} {'—':<9} 快照缺失")
            missing.append(k)
            continue
        ok = s[0] == c[0]
        print(f"{k:<9} {s[0] or '—':<9} {c[0] or '—':<9} {'一致' if ok else '漂移'}")
        if not ok:
            drift.append(k)

    if missing:
        print(f"\n[arc_drift] 结构性异常 {len(missing)} 项："
              f"{', '.join(missing)}（快照集与权威源集不一致）", file=sys.stderr)
        return 2
    if drift:
        print(f"\n[arc_drift] 检出漂移 {len(drift)}/{len(keys)}：{', '.join(drift)}")
        print("[arc_drift] `.arc` 为导入时点快照（不追平）；如需追平，"
              "按 ADR-0006 §F R-3 ③ 全量重建（**不可增量 import**）。", file=sys.stderr)
        return 1
    print(f"\n[arc_drift] 8/8 一致（快照与权威源同版本）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
