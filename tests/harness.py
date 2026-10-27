#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-139（P1-1）共享夹具：临时仓 + 真实脚本副本 + 环境注入。

口径（DESIGN §13.2）：
  - 每个用例独立 temp 仓，**零写入真实仓**；
  - 注入 `SR_SESSIONS_DIR` / `SR_REWORK_REGISTRY`（runner 既有先例，P-022 / P-069）；
  - 只复制被测脚本本体（runner / step_enforce / spec_map），不复制整仓；
  - 变异体测试把脚本复制到 temp 后**就地改字**，真实仓脚本永不被改。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPO_ROOT / "tools" / "spec_runner" / "spec_runner.py"
STEP_ENFORCE = REPO_ROOT / "scripts" / "step_enforce.py"
SPEC_MAP = REPO_ROOT / "scripts" / "spec_map.py"

STEPS = ("research", "design", "implement", "verify", "finalize")

PROGRESS = """# PROGRESS

| P | 事项 | 依据 | 状态 | 优先 | 说明 |
|---|---|---|---|---|---|
| P-001 | demo | [spec/demo/](../spec/demo/) | done | 中 | - |
| P-002 | other | [spec/other/](../spec/other/) | done | 中 | - |
"""

PROGRESS_ONE = """# PROGRESS

| P | 事项 | 依据 | 状态 | 优先 | 说明 |
|---|---|---|---|---|---|
| P-001 | demo | [spec/demo/](../spec/demo/) | done | 中 | - |
"""

WIKI = """# WIKI

## 9. 文档索引

| 文件 | 定位 |
|---|---|
| [spec/demo/](./spec/demo/) | P-001 demo |
| [spec/other/](./spec/other/) | P-002 other |
"""

REGISTRY = """{
  "graph_version": "1.0",
  "trigger_kinds": ["upstream_overturned", "review_rejection"],
  "provenance_prefixes": ["commit"],
  "forks": [],
  "non_rework": []
}
"""


def make_repo(prefix: str = "p139_", progress: str | None = None,
              mutate: tuple[str, str, str] | None = None):
    """建 temp 仓并返回 (tmp_dir, repo_root)。

    mutate = (相对脚本路径, 原字面量, 替换字面量)：**只改 temp 副本**，且要求原字面量
    恰好出现 1 次（否则抛断言错误 —— 变异体与源码漂移必须显式失败）。
    """
    tmp = Path(tempfile.mkdtemp(prefix=prefix))
    root = tmp / "repo"
    for d in ("scripts", "docs", "spec/demo", "spec/other",
              "tools/spec_runner/sessions"):
        (root / d).mkdir(parents=True, exist_ok=True)
    shutil.copy2(STEP_ENFORCE, root / "scripts" / "step_enforce.py")
    shutil.copy2(SPEC_MAP, root / "scripts" / "spec_map.py")
    shutil.copy2(RUNNER, root / "tools" / "spec_runner" / "spec_runner.py")
    write(root, "docs/PROGRESS.md", progress or PROGRESS)
    write(root, "CODE_WIKI.md", WIKI)
    write(root, "docs/rework-graph.json", REGISTRY)
    write(root, "spec/demo/RESEARCH.md", "# 1. Demo\n\ncontent\n")
    write(root, "spec/other/RESEARCH.md", "# 1. Other\n\ncontent\n")
    if mutate is not None:
        rel, needle, repl = mutate
        p = root / rel
        text = p.read_text(encoding="utf-8")
        assert text.count(needle) == 1, f"变异点须唯一: {rel} {needle[:40]!r} 出现 {text.count(needle)} 次"
        p.write_text(text.replace(needle, repl, 1), encoding="utf-8", newline="")
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "tester")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "init")
    return tmp, root


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def git(root: Path, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=True)


def env_for(root: Path) -> dict:
    """显式注入两个 env：会话目录 + 返工图真值源，均指向 temp 仓内。"""
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["SR_SESSIONS_DIR"] = str(root / "tools" / "spec_runner" / "sessions")
    env["SR_REWORK_REGISTRY"] = str(root / "docs" / "rework-graph.json")
    env.pop("SR_GIT_AUTOCOMMIT", None)
    return env


def run_cli(root: Path, rel_script: str, *args):
    cmd = [sys.executable, str(root / rel_script), *args]
    return subprocess.run(cmd, cwd=str(root), env=env_for(root), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def decision_row(sid: str, seq: int, step: str, step_seq: int,
                 anchor: str = "spec/demo/RESEARCH.md §1") -> dict:
    md = {"step_id": step, "step_seq": step_seq,
          "evidence": [{"grade": "E1", "anchor": anchor}]}
    if step == "finalize":
        md["upstream_impact"] = "none"
    return {
        "ts": "2026-10-26T00:00:%02d+08:00" % (seq % 60),
        "seq": seq, "session": sid, "source": "assistant",
        "model": None, "provider": None, "event": "decision",
        "input": {"category": step, "scenario": "s", "reasoning": "r",
                  "outcome": "o", "confidence": 0.9, "metadata": md},
        "output": None, "gate": None,
    }


def write_session(root: Path, sid: str, n: int = 5,
                  anchor: str = "spec/demo/RESEARCH.md §1") -> str:
    """写入 n 步 decision 链（seq 1..n）；返回相对路径。"""
    rows = [decision_row(sid, i, s, i, anchor) for i, s in enumerate(STEPS[:n], 1)]
    rel = f"tools/spec_runner/sessions/{sid}.jsonl"
    write(root, rel, "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    return rel
