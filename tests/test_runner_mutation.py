#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-139（P1-1 / U-3）：四类变异体 guard proof。

判据（RESEARCH §7.3 / DESIGN §13.4）：**每个变异体必须使至少一个集成用例变红**。
实现 = 把被测脚本复制到 temp 仓后**就地改字**（唯一命中，源码漂移即测试红），
再对同一探针比较「原版 exit」与「变异版 exit」——不相等即证明集成面可感知该缺陷。

四类（与 §7.3 逐条对应）：
  M1 删除完整链检查            （runner `step-gate`）
  M2 改回旧 PID 绑定（静态最新 P）（`step_enforce` 批次声明）
  M3 吞掉 gate 硬失败           （runner `step-gate` 硬性分支）
  M4 破坏 verify-anchor 路径解析（runner `_check_anchor` 调用）
"""
from __future__ import annotations

import shutil
import unittest

from tests.harness import (PROGRESS_ONE, STEPS, git, make_repo, run_cli,
                           write, write_session)

RUNNER_REL = "tools/spec_runner/spec_runner.py"
ENFORCE_REL = "scripts/step_enforce.py"

M1 = (RUNNER_REL,
      "        if len(got) != len(expect) or got != list(expect):",
      "        if False:  # MUTANT M1")
M2 = (ENFORCE_REL,
      "    declared = spec_map.changed_pids(old_progress, new_progress) if progress_changed else []",
      "    declared = [max(rows, key=_pid_num)] if rows else []  # MUTANT M2")
M3 = (RUNNER_REL,
      '    if hard:\n        print(f"step-gate[{args.session}]: hard=',
      '    if False:  # MUTANT M3\n        print(f"step-gate[{args.session}]: hard=')
M4 = (RUNNER_REL,
      "            res = _check_anchor(path, kind, loc)",
      "            res = None  # MUTANT M4")


class MutationGuardTest(unittest.TestCase):
    def _repo_with(self, mutate, **kw):
        tmp, root = make_repo("p139_mut_", mutate=mutate, **kw)
        self.addCleanup(shutil.rmtree, tmp, True)
        return root

    def _plain_repo(self, **kw):
        tmp, root = make_repo("p139_mut_", **kw)
        self.addCleanup(shutil.rmtree, tmp, True)
        return root

    def assertEqualsDifferent(self, original, mutated):
        self.assertNotEqual(original, mutated,
                            f"变异体未被感知：原版 exit {original} == 变异版 exit {mutated}")

    # ---------------------------------------------------------------- M1

    def test_m1_delete_complete_chain_check(self):
        def probe(root):
            write_session(root, "specwf-p910-20261026", n=4)
            return run_cli(root, RUNNER_REL, "step-gate", "--session",
                           "specwf-p910-20261026", "--expect", *STEPS).returncode
        original = probe(self._plain_repo())
        mutated = probe(self._repo_with(M1))
        self.assertEqual(original, 1)
        self.assertEqualsDifferent(original, mutated)

    # ---------------------------------------------------------------- M2

    def test_m2_revert_to_static_latest_pid(self):
        def probe(root):
            rel = write_session(root, "specwf-p001-20261026")
            # 先提交 session：否则它作为未跟踪变更被 `_local_changed` 视作 mode=session（P-130 设计）
            git(root, "add", rel)
            git(root, "commit", "-q", "-m", "session")
            text = (root / "docs" / "PROGRESS.md").read_text(encoding="utf-8")
            write(root, "docs/PROGRESS.md",
                  text.replace("| P-001 | demo |", "| P-001 | demo edited |", 1))
            write(root, "spec/demo/RESEARCH.md", "# 1. Demo\n\nchanged\n")
            git(root, "add", "docs/PROGRESS.md", "spec/demo/RESEARCH.md")
            return run_cli(root, ENFORCE_REL).returncode
        original = probe(self._plain_repo(progress=PROGRESS_ONE))
        mutated = probe(self._repo_with(M2, progress=PROGRESS_ONE))
        self.assertEqual(original, 1, "正确行为：仅改描述 + 四文档变更 ⇒ 缺批次声明必须红")
        self.assertEqualsDifferent(original, mutated)

    # ---------------------------------------------------------------- M3

    def test_m3_swallow_gate_hard_failure(self):
        def probe(root):
            write_session(root, "specwf-p911-20261026", n=4)
            return run_cli(root, RUNNER_REL, "step-gate", "--session",
                           "specwf-p911-20261026", "--expect", *STEPS).returncode
        original = probe(self._plain_repo())
        mutated = probe(self._repo_with(M3))
        self.assertEqual(original, 1)
        self.assertEqualsDifferent(original, mutated)

    # ---------------------------------------------------------------- M4

    def test_m4_break_anchor_path_resolution(self):
        def probe(root):
            write_session(root, "specwf-p912-20261026",
                          anchor="spec/demo/MISSING.md §1")
            return run_cli(root, RUNNER_REL, "verify-anchor", "--session",
                           "specwf-p912-20261026").returncode
        original = probe(self._plain_repo())
        mutated = probe(self._repo_with(M4))
        self.assertEqual(original, 1)
        self.assertEqualsDifferent(original, mutated)


if __name__ == "__main__":
    unittest.main(verbosity=2)
