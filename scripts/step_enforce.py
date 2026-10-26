#!/usr/bin/env python
"""批次绑定门禁入口（P-130 / U-1 O3 Phase 1）。

目标：回答「本次变更属于哪个批次，且该批次的 session 是否完整」，而不是
「这个 feature 曾经关联过哪个 P」。模式优先级（DESIGN §3.4）：

  1. batch      = 本提交新增 / 变更 P 行；
  2. session    = 本提交变更 session；
  3. branch     = 分支名 pNNN + P 行存在；
  4. maintenance= 仅 whitespace-only 文档改动；
  5. 其余语义性四文档改动 → 失败。

只读零副作用。exit 0 = 通过；1 = 违规；2 = git / 映射错误（fail-closed）。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # 共享纯函数模块（同目录）
import spec_map   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "docs" / "PROGRESS.md"
WIKI = ROOT / "CODE_WIKI.md"
RUNNER = ROOT / "tools" / "spec_runner" / "spec_runner.py"
SESSIONS = ROOT / "tools" / "spec_runner" / "sessions"

FEATURE_RE = re.compile(
    r"^spec/([a-z0-9-]+)/(?:[A-Z0-9_]+_)?"
    r"(?:RESEARCH|DESIGN|IMPLEMENTATION|CHECKLIST(?:_FUNC)?)\.md$")
SESSION_RE = re.compile(
    r"^tools/spec_runner/sessions/(specwf-p(\d{3})-[a-z0-9-]+)\.jsonl$")
BRANCH_RE = re.compile(r"(?:^|[/_-])p(\d{3})(?:$|[/_-])", re.I)
STEP_SEQUENCE = ("research", "design", "implement", "verify", "finalize")
BATCH_BINDING_MIN_P = 129


@dataclass
class Decision:
    mode: str = ""
    pids: list[str] = field(default_factory=list)
    sessions: list[str] = field(default_factory=list)
    features: set[str] = field(default_factory=set)
    source: str = ""
    errors: list[str] = field(default_factory=list)


def _norm(path: str) -> str:
    """路径归一化：反斜杠 → 斜杠；绝对路径 → 仓内相对路径。"""
    p = (path or "").replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    q = Path(p)
    if q.is_absolute():
        try:
            p = q.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return ""
    return p


def _git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=str(ROOT), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _read_progress(ref: str) -> str:
    """ref ∈ HEAD / INDEX / WORKTREE / <base-sha>。失败抛 RuntimeError（fail-closed）。"""
    if ref == "WORKTREE":
        try:
            return PROGRESS.read_text(encoding="utf-8")
        except OSError as e:
            raise RuntimeError(f"读 PROGRESS 失败: {e}") from e
    spec = ":docs/PROGRESS.md" if ref == "INDEX" else f"{ref}:docs/PROGRESS.md"
    r = _git(["show", spec])
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip() or f"git show {spec} 失败")
    return r.stdout


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _branch() -> str:
    r = _git(["branch", "--show-current"])
    return (r.stdout or "").strip()


def _branch_pid(branch: str) -> str | None:
    m = BRANCH_RE.search(branch or "")
    return f"P-{m.group(1)}" if m else None


def _pid_num(pid: str) -> int:
    m = re.search(r"P-(\d{3})", pid or "")
    return int(m.group(1)) if m else -1


def _sessions_for_pid(pid: str) -> list[str]:
    key = pid.lower().replace("-", "")
    return sorted(p.stem for p in SESSIONS.glob(f"specwf-{key}-*.jsonl"))


def _run_gate(sid: str, expect: tuple[str, ...] | None = None) -> int:
    cmd = [sys.executable, str(RUNNER), "step-gate", "--session", sid]
    if expect:
        cmd += ["--expect", *expect]
    else:
        cmd += ["--legacy"]          # 内部一致性检查 = 显式 legacy（P-132）
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode


def _check_sessions(sids: list[str], require_complete: bool) -> tuple[list[str], list[str]]:
    """内部合法性对所有 session 强制；完整性只要求「至少一个 5/5」。"""
    complete, errors = [], []
    for sid in sids:
        internal = _run_gate(sid)
        if internal != 0:
            errors.append(f"session {sid} 内部不一致（step-gate exit {internal}）")
            continue
        if require_complete and _run_gate(sid, STEP_SEQUENCE) == 0:
            complete.append(sid)
    if require_complete and not complete:
        errors.append("无 5/5 完整 session")
    return complete, errors


def _local_changed() -> set[str] | None:
    """本地模式的实际变更集：暂存 ∪ 工作树（DESIGN §3.3 步 2a）。

    背景：`pre-commit run --all-files` 会把**全量**匹配文件作为 argv 传入，
    若直接按 argv 判「变更」，每次 P 行变更都会把 66 份四文档误判为改动。
    提交时 pre-commit 只传暂存文件，故求交**不削弱**门禁；git 失败返回 None（fail-closed）。
    """
    changed: set[str] = set()
    for args in (["diff", "--cached", "--name-only"],
                 ["diff", "--name-only"],
                 ["ls-files", "--others", "--exclude-standard"]):
        r = _git(args)
        if r.returncode != 0:
            return None
        changed.update(x.strip().replace("\\", "/")
                       for x in (r.stdout or "").splitlines() if x.strip())
    return changed


def _whitespace_only(docs: list[str], base: str | None) -> bool:
    """维护模式判据：仅空白 / 行尾差异。git 失败按非维护处理（fail-closed）。"""
    if not docs:
        return False
    args = (["diff", f"{base}...HEAD"] if base else ["diff", "--cached"])
    args += ["-w", "--ignore-blank-lines", "--"] + docs
    r = _git(args)
    if r.returncode != 0:
        return False
    return not (r.stdout or "").strip()


def _resolve_declared(d: Decision, docs_features: set[str], rows: dict) -> None:
    allowed: set[str] = set()
    for pid in d.pids:
        row = rows.get(pid)
        if not row:
            d.errors.append(f"{pid} 不在 PROGRESS")
            continue
        if not row["features"]:
            d.errors.append(f"{pid} 未声明任何 spec/<feature>/ 链接")
            continue
        allowed.update(row["features"])
    if d.errors:
        return
    missing = sorted(docs_features - allowed)
    if missing:
        d.errors.append("变更 feature 未被声明 P 覆盖: " + ", ".join(missing))
        return
    d.features = allowed
    for pid in d.pids:
        sids = _sessions_for_pid(pid)
        if not sids:
            d.errors.append(f"{pid} 无 session")
            continue
        complete, errs = _check_sessions(sids, require_complete=True)
        d.errors += errs
        d.sessions += complete


def _resolve_maintenance(d: Decision, docs_features: set[str], new_progress: str) -> None:
    mapping = spec_map.build_pid_map(new_progress, _read_text(WIKI))
    d.features = set(docs_features)
    pids: set[str] = set()
    for feat in sorted(docs_features):
        pid = mapping.get(feat)
        if not pid:
            d.errors.append(f"feature {feat} 无 feature→P 映射")
            continue
        pids.add(pid)
        sids = _sessions_for_pid(pid)
        if _pid_num(pid) >= BATCH_BINDING_MIN_P:
            if not sids:
                d.errors.append(f"{pid} 无 session（维护模式要求完整链）")
                continue
            complete, errs = _check_sessions(sids, require_complete=True)
            d.errors += errs
            d.sessions += complete
        elif sids:
            _, errs = _check_sessions(sids, require_complete=False)
            d.errors += errs
    d.pids = sorted(pids)


def resolve(changed_docs: list[str], changed_sessions: list[tuple[str, str]],
            progress_changed: bool, old_progress: str, new_progress: str,
            branch: str, whitespace_only: bool) -> Decision:
    docs_features = {m.group(1) for f in changed_docs
                     for m in [FEATURE_RE.match(f)] if m}
    rows = spec_map.parse_progress_rows(new_progress)
    declared = spec_map.changed_pids(old_progress, new_progress) if progress_changed else []
    d = Decision()

    if docs_features:
        if declared:
            d.mode, d.pids, d.source = "batch", declared, "P-row"
        elif changed_sessions:
            d.mode = "session"
            d.pids = sorted({pid for _, pid in changed_sessions})
            d.source = "session"
        else:
            bp = _branch_pid(branch)
            if bp and bp in rows:
                d.mode, d.pids, d.source = "branch", [bp], "branch"
            elif whitespace_only:
                d.mode, d.source = "maintenance", "whitespace"
            else:
                d.errors.append(
                    "语义性四文档改动缺少批次声明（新 P 行 / 变更 session / 分支名）")
                return d
        if d.mode == "maintenance":
            _resolve_maintenance(d, docs_features, new_progress)
        else:
            _resolve_declared(d, docs_features, rows)
        return d

    if changed_sessions:
        d.mode, d.source = "session-progress", "session"
        d.pids = sorted({pid for _, pid in changed_sessions})
        d.sessions = [sid for sid, _ in changed_sessions]
        _, errs = _check_sessions(d.sessions, require_complete=False)
        d.errors += errs
        return d

    if progress_changed and declared:
        d.mode, d.source = "batch-registration", "P-row"
        d.pids = declared
        for pid in declared:
            row = rows.get(pid)
            if not row:
                d.errors.append(f"{pid} 不在 PROGRESS")
            elif _pid_num(pid) >= BATCH_BINDING_MIN_P and not row["features"]:
                d.errors.append(f"{pid} 未声明任何 spec/<feature>/ 链接")
        return d

    d.mode = "nothing"
    return d


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="step_enforce")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--base", help="CI 模式：旧 PROGRESS 的 git ref")
    ap.add_argument("--branch", help="CI 模式：分支名（默认读当前分支）")
    args = ap.parse_args(argv)

    files = [_norm(f) for f in args.files]
    if not args.base:
        changed = _local_changed()
        if changed is None:
            print("step-enforce: git error: 无法计算本地变更集", file=sys.stderr)
            return 2
        # 本地模式以 git 实际变更集为准：pre-commit 会按块传参（单次 argv 可能只是
        # 四文档子集），若信 argv 会把「同一次提交的声明」分块误判（DESIGN §3.3 步 2）。
        files = [f for f in changed
                 if FEATURE_RE.match(f) or SESSION_RE.match(f)
                 or f == "docs/PROGRESS.md"]
    docs = [f for f in files if FEATURE_RE.match(f)]
    sessions = []
    for f in files:
        m = SESSION_RE.match(f)
        if m:
            sessions.append((m.group(1), f"P-{m.group(2)}"))
    progress_changed = "docs/PROGRESS.md" in files
    if not docs and not sessions and not progress_changed:
        return 0

    try:
        old = _read_progress(args.base) if args.base else _read_progress("HEAD")
        new = _read_progress("WORKTREE") if args.base else _read_progress("INDEX")
    except RuntimeError as e:
        print(f"step-enforce: git error: {e}", file=sys.stderr)
        return 2

    branch = args.branch or _branch()
    d = resolve(docs, sessions, progress_changed, old, new, branch,
                _whitespace_only(docs, args.base))
    if d.errors:
        for e in d.errors:
            print(f"step-enforce: {e}", file=sys.stderr)
        print(f"step-enforce: mode={d.mode} pid={','.join(d.pids) or '-'} -> exit 1",
              file=sys.stderr)
        return 1
    print(f"step-enforce: mode={d.mode} pid={','.join(d.pids) or '-'} "
          f"sessions={','.join(d.sessions) or '-'} "
          f"features={','.join(sorted(d.features)) or '-'} source={d.source}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
