#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-139（P1-1 / U-3）：真实 `spec_runner` 集成回归。

覆盖（DESIGN §13.3）：
  - `step-gate` 四态：完整链 pass / 缺步硬红 / 无显式声明 exit 2 / legacy 内部一致；
  - `verify-anchor` 两态：真实锚点 / 文件缺失硬红（+ `--detail` 逐锚点）；
  - `fork` 前缀复制（写路径只在 temp 仓）；
  - `anchor-audit`（J2⊆J1 守门）/ `backflow-audit`（零待处理）；
  - **门禁面 parity guard**：本地 hook 触发面含 runner、CI 跑同一 `unittest discover`；
  - **CI 逐提交面 guard（P-140）**：`rev-list --reverse` 逐提交 + 执行器取提交自身版本
    （`--base` 能力探测）+ 合并提交跳过，且不再出现 `BASE...HEAD` 单次 diff 形态。
  - **evil merge 检测（P-144 / U-11）**：`--check-merge` 四态——冲突解决写入两父皆无的内容
    ⇒ exit 1；干净合并 / 受判路径等于第一父 / 非合并提交 ⇒ exit 0（不产生并集假红）。

纪律：真实 runner + 临时仓 + `SR_SESSIONS_DIR` / `SR_REWORK_REGISTRY` 注入；零写入真实仓。
"""
from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

from tests.harness import (REPO_ROOT, STEPS, git, make_repo, run_cli, write,
                           write_session)

RUNNER_REL = "tools/spec_runner/spec_runner.py"
STEP_ENFORCE_REL = "scripts/step_enforce.py"


def _commit(root: Path, msg: str) -> str:
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", msg)
    return git(root, "rev-parse", "HEAD").stdout.strip()


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

    def test_ci_per_commit_walk(self):
        """P-140：CI step-enforce 须逐提交遍历（回归 `BASE...HEAD` 单次 diff）。"""
        ci = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("git rev-list --reverse", ci,
                      "CI 未逐提交遍历 ⇒ 整条分支被塞进单一变更集（P-127 类结构性假红）")
        self.assertIn("git checkout -q -f", ci,
                      "CI 未 checkout 到各提交 ⇒ 判定用的工作树内容与提交不一致")
        self.assertIn("""grep -q 'add_argument("--base"'""", ci,
                      "CI 未按提交自身版本分派执行器 ⇒ 拿新规则追溯判处历史内容")
        self.assertIn('echo "step-enforce: skip merge commit', ci,
                      "CI 未跳过合并提交 ⇒ 其 diff = 父提交并集，重新引入单次 diff 假红")
        self.assertNotIn('"$BASE"...HEAD', ci,
                         "CI 仍存在 `BASE...HEAD` 单次 diff 形态（P-127 假红成因）")
        self.assertIn("--check-merge", ci,
                      "CI 未接 evil merge 检测 ⇒ 合并提交中两父皆无的内容永久逃逸（U-11）")

    # ----------------------------------------------- evil merge（P-144 / U-11）

    def test_evil_merge_detected(self):
        """冲突解决写入两父皆无的语义内容 ⇒ --check-merge exit 1（U-11 逃逸口）。"""
        rel = "spec/demo/RESEARCH.md"
        base = git(self.root, "rev-parse", "HEAD").stdout.strip()
        mainb = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        write(self.root, rel, "# 1. Demo\n\nline main\n")
        _commit(self.root, "main side")
        git(self.root, "checkout", "-q", "-b", "feat", base)
        write(self.root, rel, "# 1. Demo\n\nline feat\n")
        _commit(self.root, "branch side")
        with self.assertRaises(subprocess.CalledProcessError):
            git(self.root, "merge", mainb, "-m", "auto merge")
        write(self.root, rel, "# 1. Demo\n\nline evil\n")   # 两父皆无
        merge = _commit(self.root, "merge with evil resolution")
        r = run_cli(self.root, STEP_ENFORCE_REL, "--check-merge", merge)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("evil merge 内容（两父皆无）", r.stderr)
        self.assertIn(rel, r.stderr)

    def test_clean_merge_passes(self):
        """两侧改不同文件（无冲突）⇒ 合并结果等于某一父 ⇒ 不判。"""
        base = git(self.root, "rev-parse", "HEAD").stdout.strip()
        mainb = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        write(self.root, "spec/demo/RESEARCH.md", "# 1. Demo\n\nmain side\n")
        _commit(self.root, "main side")
        git(self.root, "checkout", "-q", "-b", "feat", base)
        write(self.root, "spec/other/RESEARCH.md", "# 1. Other\n\nfeat side\n")
        _commit(self.root, "branch side")
        git(self.root, "merge", mainb, "-q", "-m", "clean merge")
        sha = git(self.root, "rev-parse", "HEAD").stdout.strip()
        r = run_cli(self.root, STEP_ENFORCE_REL, "--check-merge", sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("无 evil 内容", r.stdout)

    def test_merge_equals_first_parent_passes(self):
        """main 侧只改非受判文件 ⇒ 受判路径上合并结果 = 第一父 ⇒ 不判。"""
        base = git(self.root, "rev-parse", "HEAD").stdout.strip()
        mainb = git(self.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        write(self.root, "docs/rework-graph.json", '{"graph_version": "1.1"}\n')
        _commit(self.root, "main side (non-judged path)")
        git(self.root, "checkout", "-q", "-b", "feat", base)
        write(self.root, "spec/demo/RESEARCH.md", "# 1. Demo\n\nfeat side\n")
        _commit(self.root, "branch side")
        git(self.root, "merge", mainb, "-q", "-m", "clean merge")
        sha = git(self.root, "rev-parse", "HEAD").stdout.strip()
        r = run_cli(self.root, STEP_ENFORCE_REL, "--check-merge", sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("0 个受判路径", r.stdout)

    def test_check_merge_non_merge_commit_is_noop(self):
        """非合并提交 ⇒ 直接放行（该面由逐提交循环负责）。"""
        sha = git(self.root, "rev-parse", "HEAD").stdout.strip()
        r = run_cli(self.root, STEP_ENFORCE_REL, "--check-merge", sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("非合并提交", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
