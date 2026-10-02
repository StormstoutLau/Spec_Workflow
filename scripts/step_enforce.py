#!/usr/bin/env python
"""step-enforce hook 入口（P-024，ADR-0011 出路 A——批次级流程强制）。

pre-commit 传入匹配文件（files: ^spec/<feature>/([A-Z0-9_]+_)?(四文档).md$——含非标准前缀命名），
本脚本：① 提取 feature 名 → ② 经共享模块 `spec_map` 映射 P 编号（`CODE_WIKI §9` 行标注优先 →
`PROGRESS` 行内链接兜底，C-16）→ ③ 调用 spec_runner step-enforce。
只读零副作用（P-022 教训：不创建/修改/提交任何文件）。
exit 0 = 全部应走批次决策流就绪；1 = 任一缺失（阻断）；2 = 映射缺位（提示，不阻断）。
历史豁免（P-027 盲区修复，2026-09-09）：P-020 前批次（决策流纪律建立前）不追溯强制。
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # 共享纯函数模块（同目录）
import spec_map   # noqa: E402  （C-16/I-10：feature ↔ P 映射的唯一实现）

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "docs" / "PROGRESS.md"
WIKI = ROOT / "CODE_WIKI.md"
RUNNER = ROOT / "tools" / "spec_runner" / "spec_runner.py"

# P-003 命名约定前遗留的前缀命名（COMMUNITY_ECOSYSTEM_RESEARCH.md / STEP_GATE_CHECKLIST.md 等）纳入扫描；
# 模板（*_TEMPLATE.md）/ PLAN / *_AUDIT.md 非管线交付物，不触发。
FEATURE_RE = re.compile(r"^spec/([a-z0-9-]+)/(?:[A-Z0-9_]+_)?(?:RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST(?:_FUNC)?)\.md$")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def build_feature_pid_map():
    """feature → P-0xx 映射（C-16：**唯一实现** = `spec_map`，本处与 console_gen 复用同一纯函数）。

    语义（RESEARCH v1.3 §7.10 C-16 ①）= `CODE_WIKI §9` 行标注**优先** → `PROGRESS` P 行内
    首个 `spec/<feature>/` 链接**兜底** → 缺位不入表（调用方 exit 2 提示）。
    旧语义（只认 PROGRESS 行内链接）会被「引用上游依据」的 P 行劫持（A-33，4 个 feature 受害），
    且两处实现同错、一致性对账抓不住 → 故收敛为单一来源（I-10 语义同源）。
    """
    return spec_map.build_pid_map(_read(PROGRESS), _read(WIKI))


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
        # P-020 前历史批次豁免（P-027 盲区修复）：决策流纪律 P-020 起建立，
        # 早于 P-020 的 feature（遗留前缀命名为主）无 specwf session，不追溯强制。
        # P-068（I-10 / B25 / B26）：边界改为**单点定义**（`spec_map.is_historical_exempt`），
        # 与 `console_gen` 的派生态豁免面共用同一判据（原为本地字面量 `< 20`）。
        if spec_map.is_historical_exempt(pid):
            print(f"step-enforce: {feat} ({pid}) 为 P-020 前历史批次 → 豁免（不追溯强制）")
            continue
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
