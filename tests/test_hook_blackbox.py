#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""外置黑盒回归：spec_map 纯函数契约 + FEATURE_RE 命名契约（P-111 / P-130）。

P-130 变更：CLI 批次绑定行为已迁移到 `test_batch_binding.py`（需要真实 git 仓 +
真实 spec_runner）。本文件只保留无 git 依赖的纯函数与命名契约，以及 1 个
`spec_map` 变异 guard proof（防「全绿但规则没生效」）。
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STEP_ENFORCE = REPO_ROOT / "scripts" / "step_enforce.py"
SPEC_MAP = REPO_ROOT / "scripts" / "spec_map.py"

PROGRESS = """# PROGRESS
| P-001 | old | [spec/old/](../spec/old/) |
| P-020 | live | [spec/live/](../spec/live/) |
| P-021 | other | [spec/other/](../spec/other/) |
| P-023 | dup | [spec/dup/](../spec/dup/) |
"""

WIKI = """# WIKI
## 9. 文档索引
| 文件 | 定位 |
|---|---|
| [spec/dup/](./spec/dup/) | P-020 主索引（优先） |
## 10. 统计
"""


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod          # dataclass 需要模块已在 sys.modules 中
    spec.loader.exec_module(mod)
    return mod


class SpecMapContractTest(unittest.TestCase):
    def test_priority_and_fallback(self):
        m = _load(SPEC_MAP, "spec_map_contract")
        merged = m.build_pid_map(PROGRESS, WIKI)
        self.assertEqual(merged["dup"], "P-020")
        self.assertEqual(merged["live"], "P-020")
        self.assertNotIn("ghost", merged)

    def test_missing_wiki_degrades_to_progress(self):
        m = _load(SPEC_MAP, "spec_map_degrade")
        self.assertEqual(m.build_pid_map(PROGRESS, "")["dup"], "P-023")

    def test_historical_boundary_fail_closed(self):
        m = _load(SPEC_MAP, "spec_map_boundary")
        self.assertTrue(m.is_historical_exempt("P-019"))
        self.assertFalse(m.is_historical_exempt("P-020"))
        self.assertFalse(m.is_historical_exempt("P-9"))
        self.assertFalse(m.is_historical_exempt(""))

    def test_parse_progress_rows(self):
        m = _load(SPEC_MAP, "spec_map_rows")
        rows = m.parse_progress_rows(
            "| P-130 | demo | run | **done** | 高 | [spec/demo/](../spec/demo/) |")
        self.assertEqual(rows["P-130"]["status"], "done")
        self.assertEqual(rows["P-130"]["features"], ("demo",))

    def test_changed_pids_new_row_and_status(self):
        m = _load(SPEC_MAP, "spec_map_changed")
        old = "| P-130 | demo | run | pending | 高 | [spec/demo/](../spec/demo/) |"
        new = old.replace("pending", "done")
        self.assertEqual(m.changed_pids(old, new), ["P-130"])
        self.assertEqual(m.changed_pids("", old), ["P-130"])

    def test_changed_pids_ignores_description_only(self):
        m = _load(SPEC_MAP, "spec_map_desc")
        old = "| P-130 | old text | run | done | 高 | [spec/demo/](../spec/demo/) |"
        new = "| P-130 | new text | run | done | 高 | [spec/demo/](../spec/demo/) |"
        self.assertEqual(m.changed_pids(old, new), [])

    def test_feature_regex_prefix(self):
        m = _load(STEP_ENFORCE, "step_enforce_regex")
        self.assertTrue(m.FEATURE_RE.match("spec/legacy/COMMUNITY_ECOSYSTEM_RESEARCH.md"))
        self.assertTrue(m.FEATURE_RE.match("spec/demo/DESIGN.md"))
        self.assertFalse(m.FEATURE_RE.match("spec/demo/PLAN.md"))

    def test_guard_wiki_priority(self):
        tmp = Path(tempfile.mkdtemp(prefix="p130_guard_"))
        try:
            p = tmp / "spec_map.py"
            shutil.copy2(SPEC_MAP, p)
            text = p.read_text(encoding="utf-8")
            old = "merged.update(wiki_pid_map(wiki_text))"
            self.assertEqual(text.count(old), 1)
            p.write_text(text.replace(old, "pass", 1), encoding="utf-8", newline="")
            m = _load(p, "spec_map_guard")
            self.assertEqual(m.build_pid_map(PROGRESS, WIKI)["dup"], "P-023")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
