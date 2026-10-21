#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""外置黑盒回归：step_enforce 包装层 + spec_map 契约（P-111 B1）。

范围（净增量，不复制已有 6 套内嵌 selftest）：
- step_enforce CLI：feature 识别 / 映射查表 / 历史豁免 / 多 feature 聚合 / exit 0·1·2
- spec_map 纯函数：§9 优先 / PROGRESS 兜底 / 缺位不入表 / 历史边界 fail-closed
- guard proof ×3：故意变更加载副本，断言对应测试必红（防「全绿但规则没生效」）

不变式：全部在 tempfile 镜像仓运行，零写入真实仓；仅 stdlib；不接 pre-commit hook。
"""
from __future__ import annotations

import importlib.util
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

STUB_RUNNER = '''# -*- coding: utf-8 -*-
import os, sys
args = sys.argv[1:]
pid = args[args.index("--pid") + 1] if "--pid" in args else ""
log = os.environ.get("STUB_LOG")
if log:
    with open(log, "a", encoding="utf-8") as fh:
        fh.write(pid + "\\n")
fail = {p for p in os.environ.get("STUB_FAIL_PIDS", "").split(",") if p}
sys.exit(1 if pid in fail else 0)
'''

DEFAULT_PROGRESS = """# PROGRESS
| P-001 | old | [spec/old/](spec/old/) |
| P-020 | live | [spec/live/](spec/live/) |
| P-021 | other | [spec/other/](spec/other/) |
| P-022 | legacy | [spec/legacy/](spec/legacy/) |
| P-023 | dup | [spec/dup/](spec/dup/) |
"""

DEFAULT_WIKI = """# WIKI
## 9. 文档索引
| 文件 | 定位 |
|---|---|
| [spec/dup/](./spec/dup/) | P-020 主索引（优先） |
## 10. 统计
"""


class HookBlackBoxTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="p111_blackbox_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _repo(self, name="repo", progress=DEFAULT_PROGRESS, wiki=DEFAULT_WIKI,
              mutate_enforce=None, mutate_map=None):
        root = self.tmp / name
        (root / "scripts").mkdir(parents=True)
        (root / "tools" / "spec_runner").mkdir(parents=True)
        (root / "docs").mkdir(parents=True)
        shutil.copy2(STEP_ENFORCE, root / "scripts" / "step_enforce.py")
        shutil.copy2(SPEC_MAP, root / "scripts" / "spec_map.py")
        (root / "tools" / "spec_runner" / "spec_runner.py").write_text(
            STUB_RUNNER, encoding="utf-8", newline="\n")
        (root / "docs" / "PROGRESS.md").write_text(progress, encoding="utf-8", newline="\n")
        (root / "CODE_WIKI.md").write_text(wiki, encoding="utf-8", newline="\n")
        for rel, mutation in (("scripts/step_enforce.py", mutate_enforce),
                              ("scripts/spec_map.py", mutate_map)):
            if not mutation:
                continue
            p = root / rel
            text = p.read_text(encoding="utf-8")
            old, new = mutation
            self.assertEqual(text.count(old), 1, "guard mutation anchor 不唯一: %s" % old)
            p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")
        return root

    def _run(self, root, args, fail_pids=""):
        log = root / "stub.log"
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["STUB_FAIL_PIDS"] = fail_pids
        env["STUB_LOG"] = str(log)
        r = subprocess.run([sys.executable, str(root / "scripts" / "step_enforce.py")] + args,
                           cwd=str(root), env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        return r, log

    # ------------------------------------------------------------ step_enforce CLI

    def test_no_feature_arg_returns_0(self):
        r, log = self._run(self._repo(), ["docs/PROGRESS.md"])
        self.assertEqual(r.returncode, 0)
        self.assertFalse(log.exists())

    def test_unmapped_feature_returns_2(self):
        r, _ = self._run(self._repo(), ["spec/ghost/RESEARCH.md"])
        self.assertEqual(r.returncode, 2)
        self.assertIn("映射缺位", r.stdout)

    def test_historical_exempt_skips_runner(self):
        r, log = self._run(self._repo(), ["spec/old/RESEARCH.md"], fail_pids="P-001")
        self.assertEqual(r.returncode, 0)
        self.assertIn("豁免", r.stdout)
        self.assertFalse(log.exists())

    def test_post_p020_success_returns_0(self):
        r, log = self._run(self._repo(), ["spec/live/RESEARCH.md"])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(log.read_text(encoding="utf-8").strip(), "P-020")

    def test_post_p020_failure_returns_1(self):
        r, _ = self._run(self._repo(), ["spec/live/RESEARCH.md"], fail_pids="P-020")
        self.assertEqual(r.returncode, 1)
        self.assertIn("校验未过", r.stdout)

    def test_multi_feature_aggregates_failure(self):
        r, log = self._run(self._repo(),
                           ["spec/live/RESEARCH.md", "spec/other/RESEARCH.md"],
                           fail_pids="P-021")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(sorted(log.read_text(encoding="utf-8").split()), ["P-020", "P-021"])

    def test_prefixed_four_doc_name_is_recognized(self):
        # P-027 回归锚点：遗留前缀命名的四文档必须进入门禁，不得静默绕过
        r, log = self._run(self._repo(), ["spec/legacy/COMMUNITY_ECOSYSTEM_RESEARCH.md"])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(log.read_text(encoding="utf-8").strip(), "P-022")

    def test_non_four_doc_is_ignored(self):
        r, log = self._run(self._repo(), ["spec/live/PLAN.md"])
        self.assertEqual(r.returncode, 0)
        self.assertFalse(log.exists())

    def test_wiki_section9_priority_over_progress(self):
        # C-16：PROGRESS 把 dup 指向 P-023，§9 标注 P-020 ⇒ 应按 P-020 执行
        r, _ = self._run(self._repo(), ["spec/dup/RESEARCH.md"], fail_pids="P-020")
        self.assertEqual(r.returncode, 1)

    # ------------------------------------------------------------ spec_map 契约

    def _load_spec_map(self, root):
        spec = importlib.util.spec_from_file_location(
            "spec_map_%d" % id(root), str(root / "scripts" / "spec_map.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_spec_map_priority_and_fallback(self):
        root = self._repo()
        m = self._load_spec_map(root)
        merged = m.build_pid_map((root / "docs" / "PROGRESS.md").read_text(encoding="utf-8"),
                                 (root / "CODE_WIKI.md").read_text(encoding="utf-8"))
        self.assertEqual(merged["dup"], "P-020")
        self.assertEqual(merged["live"], "P-020")
        self.assertNotIn("ghost", merged)

    def test_spec_map_missing_wiki_degrades_to_progress(self):
        root = self._repo()
        m = self._load_spec_map(root)
        merged = m.build_pid_map((root / "docs" / "PROGRESS.md").read_text(encoding="utf-8"), "")
        self.assertEqual(merged["dup"], "P-023")

    def test_historical_boundary_fail_closed(self):
        root = self._repo()
        m = self._load_spec_map(root)
        self.assertTrue(m.is_historical_exempt("P-019"))
        self.assertFalse(m.is_historical_exempt("P-020"))
        self.assertFalse(m.is_historical_exempt("P-9"))
        self.assertFalse(m.is_historical_exempt(""))

    # ------------------------------------------------------------ guard proof ×3

    def test_guard_feature_regex_prefix(self):
        root = self._repo("mut_regex", mutate_enforce=("(?:[A-Z0-9_]+_)?", ""))
        r, log = self._run(root, ["spec/legacy/COMMUNITY_ECOSYSTEM_RESEARCH.md"])
        # 变异体不再识别前缀命名 ⇒ 正例失效（不调用 runner）
        self.assertEqual(r.returncode, 0)
        self.assertFalse(log.exists())

    def test_guard_wiki_priority(self):
        root = self._repo("mut_map",
                          mutate_map=("merged.update(wiki_pid_map(wiki_text))", "pass"))
        r, _ = self._run(root, ["spec/dup/RESEARCH.md"], fail_pids="P-020")
        # 变异体丢掉 §9 优先 ⇒ 按 PROGRESS 的 P-023 成功，失败注入不生效
        self.assertEqual(r.returncode, 0)

    def test_guard_failure_aggregation(self):
        root = self._repo("mut_fail", mutate_enforce=("if r.returncode != 0:", "if False:"))
        r, _ = self._run(root, ["spec/live/RESEARCH.md"], fail_pids="P-020")
        # 变异体吞掉失败 ⇒ 原失败用例失效
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
