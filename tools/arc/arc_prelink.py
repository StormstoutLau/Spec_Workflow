#!/usr/bin/env python3
"""ARC ADR 预链接脚本（P-035，吃狗粮实施）——规避矩阵 D4 落地。

职责：
  - 扫描本仓 adr/*.md 的 frontmatter（id/depends/status/取代元数据）
  - 将 ADR 依赖簇映射为 ARC 实体间链接建议（decision → decision 用 driven_by）
  - 输出 `arc link <from> <to> --type <edge>` 命令序列 + dry-run 统计
  - 方向映射（实测校准，P-031 A-9 + 本批复测）：
      ADR 之间：D-xxx ──driven_by──▶ D-yyy（yyy 在 xxx 的 depends 中）
      （0.8.0 link 合法边类型: driven_by | enables | supersedes | derived_from | conflicts_with）

零依赖 stdlib only。
用法：
  python tools/arc/arc_prelink.py --dry-run   # 只输出建议，不改库
  python tools/arc/arc_prelink.py --execute   # 执行 arc link（经 arc_wrap 白名单）
"""
import argparse
import os
import re
import subprocess
import sys

ARC_DIR = os.path.dirname(os.path.abspath(__file__))
RECROOT = os.path.dirname(os.path.dirname(ARC_DIR))   # tools/arc → 仓根
ADR_DIR = os.path.join(RECROOT, "adr")
WRAP = os.path.join(ARC_DIR, "arc_wrap.py")

FM_ID_RE = re.compile(r"^id:\s*(\S+)", re.MULTILINE)
FM_DEPENDS_RE = re.compile(r"^depends:\s*\[([^\]]*)\]", re.MULTILINE)
FM_STATUS_RE = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
SUPERSEDE_RE = re.compile(r"\| 取代 \| (.+) \|", re.MULTILINE)

# ADR 编号 → ARC decision 实体 ID 映射（import 后由 ARC 分配 D-xxx）
# 策略：预链接脚本按 ADR-id → D-xxx 依赖 cmd 输出的映射表；当前：ADR id 直接作 key
# 实测映射见 IMPLEMENTATION §4（arc import 单文件后 list 分配序号）


def parse_frontmatter(path: str):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fid = FM_ID_RE.search(text)
    depends = FM_DEPENDS_RE.search(text)
    status = FM_STATUS_RE.search(text)
    supersede = SUPERSEDE_RE.search(text)
    return {
        "file": os.path.basename(path),
        "id": fid.group(1) if fid else None,
        "depends": [d.strip().strip('"') for d in depends.group(1).split(",")] if depends else [],
        "status": status.group(1) if status else None,
        "supersedes": supersede.group(1).strip() if supersede else None,
    }


def collect_adrs() -> dict:
    import glob
    adrs = {}
    for path in glob.glob(os.path.join(ADR_DIR, "*.md")):
        rec = parse_frontmatter(path)
        if rec["id"]:
            adrs[rec["id"]] = rec
    return adrs


def resolve_d_map() -> dict:
    """动态建 ADR id → D-xxx 映射：arc list --format json + 标题 ADR-NNNN 前缀。"""
    proc = subprocess.run([sys.executable, WRAP, "list", "--format", "json"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print("[arc_prelink] list --format json 失败", file=sys.stderr)
        return {}
    import json
    try:
        ents = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}
    d_map = {}
    for e in ents:
        eid = e.get("id", "")
        title = e.get("title", "")
        m = re.match(r"(ADR-\d{4})", title)
        if m:
            d_map[m.group(1)] = eid
    return d_map


def build_links(adrs: dict) -> list:
    """依赖簇 → (from_id, to_id) 链接建议（实测校准，P-035 实施批）：
    本仓 ADR frontmatter `depends` = ADR 依赖的其它 ADR。
    方向映射（实测）：ADR-B 依赖 ADR-A ⇒ link D(B) ──depends_on──▶ D(A)。
    实测发现：link 合法边按源-目标实体类型动态决定——
      decision → decision: 仅 enables | supersedes | depends_on（--help 展示集 ≠ 运行时校验集）
      decision → requirement: driven_by ✓（P-031 + 本批复测校准）
    """
    links = []
    d_map = resolve_d_map()
    for aid, rec in adrs.items():
        for dep in rec.get("depends", []):
            if dep in adrs and dep in d_map and aid in d_map:
                links.append((d_map[aid], d_map[dep], "depends_on"))
    return sorted(set(links))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只输出建议链接，不执行")
    ap.add_argument("--execute", action="store_true", help="执行 arc link（经白名单封装）")
    args = ap.parse_args()

    adrs = collect_adrs()
    links = build_links(adrs)
    # 去重
    links = sorted(set(links))

    print(f"[arc_prelink] 扫描 ADR: {len(adrs)} 个，依赖簇链接建议: {len(links)} 条")
    ok = 0
    for fid, dep, etype in links:
        cmd = ["link", fid, dep, "--type", etype]
        line = f"  {fid} ──{etype}──▶ {dep}"
        if args.dry_run or not args.execute:
            print("  [dry] " + line)
            ok += 1
            continue
        proc = subprocess.run([sys.executable, WRAP, *cmd],
                              capture_output=True, text=True)
        if proc.returncode == 0:
            ok += 1
            print("  [ok] " + line)
        else:
            print(f"  [ERR {proc.returncode}] " + line)
            if proc.stderr:
                sys.stderr.write(proc.stderr)

    print(f"[arc_prelink] 完成: 建议 {len(links)} / 成功 {ok}")
    return 0 if ok == len(links) else 1


if __name__ == "__main__":
    sys.exit(main())