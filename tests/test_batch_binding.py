#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次绑定门禁集成测试（P-130 / U-1 O3 Phase 1）。

真实 `spec_runner.py` + 临时 git 仓；零写入真实仓；stdlib only。
覆盖 DESIGN §3.5 的 12 类模式 / 故障注入 + git 错误 fail-closed。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STEP_ENFORCE = REPO_ROOT / "scripts" / "step_enforce.py"
SPEC_MAP = REPO_ROOT / "scripts" / "spec_map.py"
RUNNER = REPO_ROOT / "tools" / "spec_runner" / "spec_runner.py"

STEPS = ("research", "design", "implement", "verify", "finalize")

INITIAL_PROGRESS = """# PROGRESS

| P | 事项 | 依据 | 状态 | 优先 | 说明 |
|---|---|---|---|---|---|
| P-001 | demo | [spec/demo/](../spec/demo/) | done | 中 | - |
| P-002 | other | [spec/other/](../spec/other/) | done | 中 | - |
"""

INITIAL_WIKI = """# WIKI

## 9. 文档索引

| 文件 | 定位 |
|---|---|
| [spec/demo/](./spec/demo/) | P-001 demo |
| [spec/other/](./spec/other/) | P-002 other |

## 10. 统计
"""


class BatchBindingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="p130_batch_"))
        self.root = self.tmp / "repo"
        (self.root / "scripts").mkdir(parents=True)
        (self.root / "docs").mkdir(parents=True)
        (self.root / "spec" / "demo").mkdir(parents=True)
        (self.root / "spec" / "other").mkdir(parents=True)
        (self.root / "tools" / "spec_runner" / "sessions").mkdir(parents=True)
        shutil.copy2(STEP_ENFORCE, self.root / "scripts" / "step_enforce.py")
        shutil.copy2(SPEC_MAP, self.root / "scripts" / "spec_map.py")
        shutil.copy2(RUNNER, self.root / "tools" / "spec_runner" / "spec_runner.py")
        self._write("docs/PROGRESS.md", INITIAL_PROGRESS)
        self._write("CODE_WIKI.md", INITIAL_WIKI)
        self._write("spec/demo/RESEARCH.md", "# Demo\n\ncontent\n")
        self._write("spec/other/RESEARCH.md", "# Other\n\ncontent\n")
        self._git("init", "-q")
        self._git("config", "user.email", "t@example.com")
        self._git("config", "user.name", "tester")
        self._git("add", ".")
        self._git("commit", "-q", "-m", "init")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------ helpers

    def _write(self, rel: str, text: str):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")

    def _git(self, *args):
        return subprocess.run(["git", *args], cwd=str(self.root),
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=True)

    def _stage(self, *rels):
        self._git("add", "--", *rels)

    def _commit(self, msg="step"):
        self._git("add", "-A")
        self._git("commit", "-q", "-m", msg)

    def _append_p_row(self, pid="P-130", status="done", links=("demo",)):
        text = (self.root / "docs" / "PROGRESS.md").read_text(encoding="utf-8")
        cell = " ".join(f"[spec/{f}/](../spec/{f}/)" for f in links) or "-"
        row = f"| {pid} | demo batch | run | {status} | 高 | {cell} |\n"
        self._write("docs/PROGRESS.md", text + row)

    def _pin_wiki(self, pid: str):
        """维护模式的 feature→P 映射优先取 CODE_WIKI §9，须同步改写。"""
        self._write("CODE_WIKI.md", INITIAL_WIKI.replace("P-001 demo", f"{pid} demo"))

    def _session(self, sid="specwf-p130-20261026", n=5,
                 anchor="spec/demo/RESEARCH.md"):
        rows = []
        for i, step in enumerate(STEPS[:n], 1):
            md = {"step_id": step, "step_seq": i,
                  "evidence": [{"grade": "E1", "anchor": anchor}]}
            if step == "finalize":
                md["upstream_impact"] = "none"
            rows.append({
                "ts": "2026-10-26T00:00:%02d+08:00" % i,
                "seq": i, "session": sid, "source": "assistant",
                "model": None, "provider": None, "event": "decision",
                "input": {"category": "feature", "scenario": "s",
                          "reasoning": "r", "outcome": "o",
                          "confidence": 0.9, "metadata": md},
                "output": None, "gate": None,
            })
        rel = f"tools/spec_runner/sessions/{sid}.jsonl"
        self._write(rel, "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
        return rel

    def _run(self, files, base=None, branch=None):
        cmd = [sys.executable, str(self.root / "scripts" / "step_enforce.py")]
        if base:
            cmd += ["--base", base]
        if branch:
            cmd += ["--branch", branch]
        cmd += list(files)
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(cmd, cwd=str(self.root), env=env,
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace")

    def _assert_pass(self, r, mode):
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertIn(f"mode={mode}", r.stdout)

    def _assert_fail(self, r, needle=""):
        self.assertEqual(r.returncode, 1, r.stderr + r.stdout)
        if needle:
            self.assertIn(needle, r.stderr)

    # ------------------------------------------------------------ cases

    def test_batch_pass(self):
        self._append_p_row()
        rel = self._session()
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        self._assert_pass(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md", rel]), "batch")

    def test_all_files_mode_ignores_unchanged(self):
        """pre-commit --all-files：全量 argv 退化为实际变更集（DESIGN §3.3 步 2a）。"""
        self._append_p_row()
        rel = self._session()
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        all_files = ["docs/PROGRESS.md", "spec/demo/RESEARCH.md",
                     "spec/other/RESEARCH.md", rel]
        self._assert_pass(self._run(all_files), "batch")
        # 求交不得放行真实改动：other 实际变更后同一 argv 必须失败
        self._write("spec/other/RESEARCH.md", "# Other\n\nchanged\n")
        self._stage("spec/other/RESEARCH.md")
        self._assert_fail(self._run(all_files), "未被声明 P 覆盖")

    def test_partial_argv_uses_git_change_set(self):
        """pre-commit 分块：单次 argv 只含四文档子集，仍应按整批变更判定。"""
        self._append_p_row()
        rel = self._session()
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        # 模拟 pre-commit 一个 chunk：只传文档，不含 PROGRESS / session
        self._assert_pass(self._run(["spec/demo/RESEARCH.md"]), "batch")

    def test_batch_one_step_fails(self):
        self._append_p_row()
        rel = self._session(n=1)
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        self._assert_fail(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md", rel]), "无 5/5")

    def test_zero_step_session_fails(self):
        """0/5：无 decision 的 session 内部不合法，必须判红。"""
        self._append_p_row()
        rel = self._session(n=0)
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        self._assert_fail(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md", rel]), "内部不一致")

    def test_four_step_session_fails(self):
        """4/5：内部合法但缺 finalize，必须判红。"""
        self._append_p_row()
        rel = self._session(n=4)
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        self._assert_fail(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md", rel]), "无 5/5")

    def test_maintenance_boundary_128_legacy_partial_passes(self):
        """U-2 边界 129：P-128 维护模式只验内部合法，不要求 5/5。"""
        self._append_p_row(pid="P-128", links=("demo",))
        self._pin_wiki("P-128")
        self._session("specwf-p128-20261025", n=1)
        self._commit("legacy batch")
        self._write("spec/demo/RESEARCH.md", "# Demo\n\ncontent   \n")
        self._stage("spec/demo/RESEARCH.md")
        self._assert_pass(self._run(["spec/demo/RESEARCH.md"]), "maintenance")

    def test_maintenance_boundary_129_requires_complete(self):
        """U-2 边界 129：P-129 维护模式必须 5/5（边界含 129）。"""
        self._append_p_row(pid="P-129", links=("demo",))
        self._pin_wiki("P-129")
        self._session("specwf-p129-20261025", n=1)
        self._commit("boundary batch")
        self._write("spec/demo/RESEARCH.md", "# Demo\n\ncontent   \n")
        self._stage("spec/demo/RESEARCH.md")
        self._assert_fail(self._run(["spec/demo/RESEARCH.md"]), "无 5/5")

    def test_legacy_declaration_with_docs_still_requires_complete(self):
        """边界只作用于维护/登记：P<129 的显式声明带文档改动仍须 5/5。"""
        self._append_p_row(pid="P-128", links=("demo",))
        rel = self._session("specwf-p128-20261025", n=1)
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        self._assert_fail(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md", rel]), "无 5/5")

    def test_no_declaration_fails(self):
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nsemantic change\n")
        self._stage("spec/demo/RESEARCH.md")
        self._assert_fail(self._run(["spec/demo/RESEARCH.md"]), "缺少批次声明")

    def test_session_mode_pass(self):
        self._append_p_row()
        base = self._session("specwf-p130-20261025")
        self._commit("base batch")
        rel = self._session("specwf-p130-20261027")
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("spec/demo/RESEARCH.md", rel)
        self._assert_pass(self._run(["spec/demo/RESEARCH.md", rel]), "session")

    def test_branch_mode_pass(self):
        self._append_p_row()
        self._session("specwf-p130-20261025")
        self._commit("base batch")
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("spec/demo/RESEARCH.md")
        self._assert_pass(self._run(["spec/demo/RESEARCH.md"],
                                    branch="docs/p130-demo"), "branch")

    def test_maintenance_whitespace_pass(self):
        self._write("spec/demo/RESEARCH.md", "# Demo\n\ncontent   \n")
        self._stage("spec/demo/RESEARCH.md")
        self._assert_pass(self._run(["spec/demo/RESEARCH.md"]), "maintenance")

    def test_multi_feature_batch_pass(self):
        self._append_p_row(links=("demo", "other"))
        rel = self._session()
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._write("spec/other/RESEARCH.md", "# Other\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md",
                    "spec/other/RESEARCH.md", rel)
        self._assert_pass(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md",
                                     "spec/other/RESEARCH.md", rel]), "batch")

    def test_new_p_row_no_links_fails(self):
        self._append_p_row(links=())
        rel = self._session()
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", rel)
        self._assert_fail(self._run(["docs/PROGRESS.md",
                                     "spec/demo/RESEARCH.md", rel]),
                          "未声明任何 spec")

    def test_no_filename_sort_trap(self):
        self._append_p_row()
        v9 = self._session("specwf-p130-20261026v9", n=1)
        v10 = self._session("specwf-p130-20261026v10", n=5)
        self._write("spec/demo/RESEARCH.md", "# Demo\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/demo/RESEARCH.md", v9, v10)
        r = self._run(["docs/PROGRESS.md", "spec/demo/RESEARCH.md", v9, v10])
        self._assert_pass(r, "batch")
        self.assertIn("v10", r.stdout)
        self.assertNotIn("v9", r.stdout.split("sessions=")[1].split(" ")[0])

    def test_feature_not_covered_fails(self):
        self._append_p_row(links=("demo",))
        rel = self._session()
        self._write("spec/other/RESEARCH.md", "# Other\n\nchanged\n")
        self._stage("docs/PROGRESS.md", "spec/other/RESEARCH.md", rel)
        self._assert_fail(self._run(["docs/PROGRESS.md",
                                     "spec/other/RESEARCH.md", rel]),
                          "未被声明 P 覆盖")

    def test_session_progress_passes(self):
        self._append_p_row()
        self._commit("base batch")
        rel = self._session("specwf-p130-20261027", n=1)
        self._stage(rel)
        self._assert_pass(self._run([rel]), "session-progress")

    def test_batch_registration_passes(self):
        self._append_p_row(status="pending")
        self._stage("docs/PROGRESS.md")
        self._assert_pass(self._run(["docs/PROGRESS.md"]), "batch-registration")

    def test_git_error_returns_2(self):
        root = Path(tempfile.mkdtemp(prefix="p130_nogit_"))
        try:
            (root / "scripts").mkdir()
            (root / "docs").mkdir()
            shutil.copy2(STEP_ENFORCE, root / "scripts" / "step_enforce.py")
            shutil.copy2(SPEC_MAP, root / "scripts" / "spec_map.py")
            (root / "docs" / "PROGRESS.md").write_text(INITIAL_PROGRESS, encoding="utf-8")
            r = subprocess.run([sys.executable, str(root / "scripts" / "step_enforce.py"),
                                "docs/PROGRESS.md"], cwd=str(root),
                               capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            self.assertEqual(r.returncode, 2, r.stderr + r.stdout)
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
