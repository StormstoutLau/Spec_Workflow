#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-139（P1-1 / U-3）：真实 `spec_runner` 集成回归。

覆盖（DESIGN §13.3）：
  - `step-gate` 四态：完整链 pass / 缺步硬红 / 无显式声明 exit 2 / legacy 内部一致；
  - `verify-anchor` 两态：真实锚点 / 文件缺失硬红（+ `--detail` 逐锚点）；
  - `fork` 前缀复制（写路径只在 temp 仓）；
  - `anchor-audit`（J2⊆J1 守门）/ `backflow-audit`（零待处理）；
  - **门禁面 parity guard**：本地 hook 触发面含 runner、CI 跑同一 `unittest discover`。

纪律：真实 runner + 临时仓 + `SR_SESSIONS_DIR` / `SR_REWORK_REGISTRY` 注入；零写入真实仓。
"""
from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from tests.harness import REPO_ROOT, STEPS, make_repo, run_cli, write_session

RUNNER_REL = "tools/spec_runner/spec_runner.py"


class RunnerIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp, self.root = make_repo("p139_it_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---------------------------------------------------------- step-gate

    def test_step_gate_complete_chain_pass(self):
        write_session(self.root, "specwf-p900-20261026")
        r = run_cli(self.root, RUNNER_REL, "step-gate", "--session",
                    "specwf-p900-20261026", "--expect", *STEPS)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("决策链一致 pass", r.stdout)

    def test_step_gate_missing_step_hard_fail(self):
        write_session(self.root, "specwf-p901-20261026", n=4)
        r = run_cli(self.root, RUNNER_REL, "step-gate", "--session",
                    "specwf-p901-20261026", "--expect", *STEPS)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("[HARD]", r.stdout)

    def test_step_gate_requires_explicit_declaration(self):
        write_session(self.root, "specwf-p902-20261026")
        r = run_cli(self.root, RUNNER_REL, "step-gate", "--session",
                    "specwf-p902-20261026")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("--expect", r.stdout)

    def test_step_gate_legacy_internal_consistency(self):
        write_session(self.root, "specwf-p903-20261026", n=4)
        r = run_cli(self.root, RUNNER_REL, "step-gate", "--session",
                    "specwf-p903-20261026", "--legacy")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("mode=legacy", r.stdout)

    # ------------------------------------------------------- verify-anchor

    def test_verify_anchor_real_pass(self):
        write_session(self.root, "specwf-p904-20261026")
        r = run_cli(self.root, RUNNER_REL, "verify-anchor", "--session",
                    "specwf-p904-20261026", "--detail")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("锚点 5 真实", r.stdout)
        self.assertIn("[DETAIL]", r.stdout)

    def test_verify_anchor_missing_file_hard_fail(self):
        write_session(self.root, "specwf-p905-20261026",
                      anchor="spec/demo/MISSING.md §1")
        r = run_cli(self.root, RUNNER_REL, "verify-anchor", "--session",
                    "specwf-p905-20261026")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("文件不存在", r.stdout)

    # --------------------------------------------------------------- fork

    def test_fork_copies_prefix_rows(self):
        write_session(self.root, "specwf-p906-20261026")
        r = run_cli(self.root, RUNNER_REL, "fork", "--session",
                    "specwf-p906-20261026", "--seq", "3", "--new",
                    "specwf-p906-20261026v2")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        new = self.root / "tools" / "spec_runner" / "sessions" / "specwf-p906-20261026v2.jsonl"
        self.assertTrue(new.is_file())
        self.assertEqual(len(new.read_text(encoding="utf-8").splitlines()), 3)

    # ------------------------------------------------- audit (read-only)

    def test_anchor_audit_invariant_holds(self):
        write_session(self.root, "specwf-p907-20261026")
        r = run_cli(self.root, RUNNER_REL, "anchor-audit")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_backflow_audit_zero_pending(self):
        write_session(self.root, "specwf-p908-20261026")
        r = run_cli(self.root, RUNNER_REL, "backflow-audit")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # -------------------------------------------- gate surface parity guard

    def test_gate_surface_parity(self):
        """本地 hook 触发面须含 runner；CI 须跑同一 `unittest discover`（同判定面）。"""
        hook = (REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        idx = hook.index("- id: blackbox-tests")
        block = hook[idx:].replace("\\", "")   # YAML 正则转义不影响语义判定
        self.assertIn("tools/spec_runner/spec_runner", block,
                      "blackbox-tests 触发面未覆盖 spec_runner.py（改 runner 将不触发本地门禁）")
        ci = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("python -m unittest discover -s tests", ci,
                      "CI 未跑与本地同一 unittest discover ⇒ 同一变异体判定面不一致")


if __name__ == "__main__":
    unittest.main(verbosity=2)
