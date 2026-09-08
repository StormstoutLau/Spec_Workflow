#!/usr/bin/env python
"""step-enforce hook 入口（P-024，ADR-0011 出路 A——批次级流程强制）。

pre-commit 传入匹配文件（files: ^spec/<feature>/(RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST*).md$），
本脚本：① 提取 feature 名 → ② 读 PROGRESS.md 映射 P 编号 → ③ 调用 spec_runner step-enforce。
只读零副作用（P-022 教训：不创建/修改/提交任何文件）。
exit 0 = 全部应走批次决策流就绪；1 = 任一缺失（阻断）；2 = 映射缺位（提示，不阻断）。
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "docs" / "PROGRESS.md"
RUNNER = ROOT / "tools" / "spec_runner" / "spec_runner.py"

P_ROW_RE = re.compile(r"^\|\s*(P-\d{3})\s*\|.*?spec/([a-z0-9-]+)/")
FEATURE_RE = re.compile(r"^spec/([a-z0-9-]+)/(RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST(?:_FUNC)?)\.md$")


def build_feature_pid_map():
    """PROGRESS.md → {feature: P-0xx} 映射（行内 spec/<feature>/ 链接定位）。"""
    if not PROGRESS.exists():
        return {}
    mapping = {}
    for line in PROGRESS.read_text(encoding="utf-8").splitlines():
        m = P_ROW_RE.search(line)
        if m:
            mapping[m.group(2)] = m.group(1)
    return mapping


def main(argv) -> int:
    files = [a for a in argv if a.startswith("spec/")]
    features = sorted({m.group(1) for f in files
                       for m in [FEATURE_RE.match(f)] if m})
    if not features:
        return 0
    mapping = build_feature_pid_map()
    fails = []
    for feat in features:
        pid = mapping.get(feat)
        if not pid:
            print(f"step-enforce: {feat} 无对应 P 行（PROGRESS 映射缺位）→ exit 2 提示")
            return 2
        r = subprocess.run([sys.executable, str(RUNNER), "step-enforce",
                            "--pid", pid], capture_output=True, text=True)
        if r.stdout:
            print(r.stdout, end="")
        if r.stderr:
            print(r.stderr, end="", file=sys.stderr)
        if r.returncode != 0:
            fails.append((feat, pid, r.returncode))
    if fails:
        for feat, pid, code in fails:
            print(f"step-enforce: {feat} ({pid}) 校验未过 → exit {code}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
