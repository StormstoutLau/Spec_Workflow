#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Spec_Runner — 薄壳 spec 工作流 runner（P-009 方案 B，DESIGN v1.0 D1-D7）。

零框架依赖（Python stdlib only，D6）。事件流 = 唯一 state（L1 append-only JSONL）。
门禁 = 流程门禁执行器（D3：subprocess 执行 + exit 透传，verdict 纯机械映射）。
端点 = 运行时注入 + 就绪门控（D5：预检不可达即 exit 1，不发起主调用）。
adapter 开放结构（D4：NativeHTTPAdapter 默认，DshSDKAdapter 为实测后候选）。

命令面（D7）：run / gate / status / replay / fork（search = grep，零代码）。
用法示例见 README.md；selftest：python spec_runner.py selftest。
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.2.0"
ROOT = Path(__file__).resolve().parent

# ---- 事件行 schema（DESIGN §3 十字段，写入端单点把守） ----
SOURCES = ("system", "user", "assistant", "tool", "gate")
EVENTS = ("session_start", "prompt", "llm_request", "llm_response", "tool",
          "gate", "decision", "endpoint_unreachable", "session_end")
LLM_EVENTS = ("llm_request", "llm_response")  # model/provider 必填非空
SID_RE = re.compile(r"^[a-z0-9-]{1,64}$")
GATE_STDOUT_TAIL = 2000
EXIT_USAGE, EXIT_GATE_MISSING, EXIT_ENDPOINT = 2, 3, 1
# P-022 懒加载门控：会话目录注入 + git 快照 opt-in（ADR-0010 Q3 借懒加载原则）
SESSIONS_ENV = "SR_SESSIONS_DIR"
GIT_AUTOCOMMIT_ENV = "SR_GIT_AUTOCOMMIT"


def sessions_dir() -> Path:
    """会话目录：env SR_SESSIONS_DIR 可注入（selftest 用），默认 <repo>/sessions。"""
    return Path(os.environ.get(SESSIONS_ENV, ROOT / "sessions"))


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# ---- 模块 1：事件流写入器（L1/L2/L3/L7——唯一写路径，无 rewrite 代码路径） ----
class EventWriter:
    def __init__(self, base: Path):
        self.base = base

    def path(self, sid: str) -> Path:
        return self.base / f"{sid}.jsonl"

    def _validate(self, sid, source, event, model, provider, gate):
        if not SID_RE.match(sid or ""):
            raise ValueError(f"bad session id: {sid!r}")
        if source not in SOURCES:
            raise ValueError(f"bad source: {source!r}")
        if event not in EVENTS:
            raise ValueError(f"bad event: {event!r}")
        if event in LLM_EVENTS and not (model and provider):
            raise ValueError(f"{event} requires non-empty model/provider")
        if event == "gate" and not gate:
            raise ValueError("gate event requires gate payload")

    def next_seq(self, sid: str) -> int:
        p = self.path(sid)
        if not p.exists():
            return 1
        last = 0
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last = json.loads(line).get("seq", 0)
        return last + 1

    def append(self, sid, source, event, input_=None, output=None,
               gate=None, model=None, provider=None):
        """append-only 写入：校验 → 取 seq → 单行 write + flush。"""
        self._validate(sid, source, event, model, provider, gate)
        row = {"ts": now_iso(), "seq": self.next_seq(sid), "session": sid,
               "source": source, "model": model, "provider": provider,
               "event": event, "input": input_, "output": output, "gate": gate}
        p = self.path(sid)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:  # 唯一写路径：mode="a"
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
        return row

    def read(self, sid):
        p = self.path(sid)
        if not p.exists():
            return []
        rows = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows


# ---- 模块 6：git 持久化薄封装（P-022 A+B 修复——opt-in 默认关 + 精确 sid 文件 + 会话目录所在 git 根） ----
def _git_root() -> Path | None:
    """会话目录所在 git 根（P-022 F1 修复：从 sessions_dir 而非 ROOT 派生，隔离天然成立）。"""
    try:
        p = subprocess.run(["git", "-C", str(sessions_dir()), "rev-parse",
                            "--show-toplevel"], capture_output=True, text=True,
                           timeout=30)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    out = p.stdout.strip()
    return Path(out) if out else None


def git_snapshot(sid: str, message: str):
    """gate/run 后事件流持久化快照（P-022 A+B）。

    - A 门控：`SR_GIT_AUTOCOMMIT != "1"` 即早退——未激活零副作用（借 ADR-0010 Q3）
    - B 范围：只 add 本次实际写入的 `<sid>.jsonl`（相对会话目录所在 git 根）；
      会话目录不在 git 仓内 → 静默跳过（注释与行为一致）
    - commit 带 `--no-verify`：透明持久化快照不被仓级 pre-commit 三校验器的中间态打断
    """
    if os.environ.get(GIT_AUTOCOMMIT_ENV) != "1":
        return
    try:
        root = _git_root()
        if root is None:
            return  # 非 git 环境——事件流文件本身已是持久化
        target = sessions_dir() / f"{sid}.jsonl"
        rel = target.resolve().relative_to(root.resolve())  # 越界即 ValueError → 跳过
        add = subprocess.run(["git", "add", "--", str(rel)], cwd=root,
                             capture_output=True, timeout=30)
        if add.returncode != 0:
            return
        subprocess.run(["git", "commit", "-m", message, "--quiet", "--no-verify"],
                       cwd=root, capture_output=True, timeout=30)
    except Exception:
        pass


# ---- 模块 2：gate 执行器（D3——verdict = exit code 机械映射，无 LLM 判断） ----
def cmd_gate(args) -> int:
    w = EventWriter(sessions_dir())
    proc = subprocess.run(args.cmd, shell=True, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          cwd=args.cwd or None)
    stdout_tail = (proc.stdout or "")[-GATE_STDOUT_TAIL:]
    verdict = "pass" if proc.returncode == 0 else "fail"
    w.append(args.session, "gate", "gate",
             input_={"cmd": args.cmd, "cwd": args.cwd},
             output={"stdout_tail": stdout_tail, "exit": proc.returncode},
             gate={"name": args.name, "cmd": args.cmd, "exit": proc.returncode,
                   "verdict": verdict, "stdout_tail": stdout_tail})
    git_snapshot(args.session, f"gate:{args.name}:{verdict} (session {args.session})")
    print(f"gate[{args.name}] verdict={verdict} exit={proc.returncode}")
    return proc.returncode  # 透传（可嵌套 pre-commit/CI）


def gate_passed(w: EventWriter, sid: str, name: str) -> bool:
    """派生视图查询：流中是否存在该 gate 的 pass 事件（D3 前置检查）。"""
    return any(r.get("gate", {}) and r["gate"].get("name") == name
               and r["gate"].get("verdict") == "pass" for r in w.read(sid))


# ---- 模块 2b：step-gate 决策产物管线校验（P-020，CER §3.5——只读校验，三类规则分级 exit） ----
STEP_SEQUENCE = ("research", "design", "implement", "verify", "finalize")
DREQ = ("category", "scenario", "reasoning", "outcome", "confidence")
ANCHOR_RE = re.compile(
    r"^(https?://\S+|"
    r"(?:spec|adr|docs|tools|scripts)/"
    r"[A-Za-z0-9_./\-]*(?:\.(?:md|py|jsonl))?"
    r"(?:#[L]\d+|L\d+|\s*§[0-9.]+)?)$")


def cmd_gate_step(args) -> int:
    """校验 session 内 decision 事件链——只读不写流。

    三类规则（DESIGN §6.2）：
      - 硬性-1 schema：八字段必填 + metadata.step_id/step_seq + evidence 非空
      - 硬性-2 秩序：step_id ∈ 序表、step_seq = 序表位、每步恰一条、--expect 覆盖时全链一致
      - 软性-3 锚点：evidence[].anchor 形态可解析（正则）
    exit 0 / 1（硬性）/ 2（软性存疑）。
    """
    w = EventWriter(sessions_dir())
    decisions = [r for r in w.read(args.session) if r.get("event") == "decision"]
    if not decisions:
        print(f"step-gate[{args.session}]: 无 decision 事件（决策记录纪律未执行）")
        return 1
    expect = tuple(args.expect) if args.expect else None
    hard, soft, seen = [], [], {}
    for r in decisions:
        inp = r.get("input") if isinstance(r.get("input"), dict) else {}
        md = inp.get("metadata") if isinstance(inp.get("metadata"), dict) else {}
        missing = [k for k in DREQ if k not in inp]
        if not md.get("step_id") or md.get("step_seq") is None:
            missing.append("metadata.step_id/step_seq")
        if not (isinstance(md.get("evidence"), list) and md["evidence"]):
            missing.append("metadata.evidence 非空")
        if missing:
            hard.append(f"seq{r.get('seq')} 缺字段: {missing}")
            continue
        sid_, sseq = md["step_id"], md["step_seq"]
        if sid_ not in STEP_SEQUENCE or sseq != STEP_SEQUENCE.index(sid_) + 1:
            hard.append(f"seq{r.get('seq')} step 位错 (step_id={sid_!r}, step_seq={sseq})")
        if sid_ in seen:
            hard.append(f"seq{r.get('seq')} step_id 重复 {sid_!r}（已见于 seq{seen[sid_]}）")
        seen[sid_] = r.get("seq")
        for ev in md["evidence"]:
            anchor = ev.get("anchor") if isinstance(ev, dict) else str(ev)
            if anchor and not ANCHOR_RE.match(anchor):
                soft.append(f"seq{r.get('seq')} 锚点形态存疑 {str(anchor)[:50]!r}")
    got = list(seen)
    if expect:
        if len(got) != len(expect) or got != list(expect):
            hard.append(f"期望链 {list(expect)} ≠ 已登记 {got}")
    else:
        print(f"step-gate[{args.session}]: 已登记 {len(got)}/{len(STEP_SEQUENCE)} 步 ({got})"
              + ("（未声明 --expect 完整性）" if len(got) < len(STEP_SEQUENCE) else ""))
    for m in hard:
        print(f"  [HARD] {m}")
    for m in soft:
        print(f"  [SOFT] {m}")
    if hard:
        print(f"step-gate[{args.session}]: hard={len(hard)} soft={len(soft)} → exit 1")
        return 1
    if soft:
        print(f"step-gate[{args.session}]: soft={len(soft)} → exit 2（人工复核）")
        return 2
    print(f"step-gate[{args.session}]: 决策链一致 pass → exit 0")
    return 0


# ---- 模块 3：adapter 接口 + NativeHTTP（D4/D5——stdlib urllib，预检门控 + 重试） ----
class LLMAdapter:
    """协议面（D4 开放结构单点）：chat / endpoint_ready。"""

    def chat(self, messages, **params):
        raise NotImplementedError

    def endpoint_ready(self) -> bool:
        raise NotImplementedError


class NativeHTTPAdapter(LLMAdapter):
    def __init__(self, endpoint, model, provider, timeout=60):
        self.endpoint = endpoint.rstrip("/")
        self.model, self.provider, self.timeout = model, provider, timeout

    def endpoint_ready(self) -> bool:
        try:
            req = urllib.request.Request(self.endpoint + "/v1/models")
            urllib.request.urlopen(req, timeout=3)
            return True
        except Exception:
            return False

    def chat(self, messages, **params):
        payload = json.dumps({"model": self.model, "messages": messages,
                              **params}).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint + "/v1/chat/completions", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        last_err = None
        for attempt in range(3):  # 超时重试 2 次
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except Exception as e:  # noqa: BLE001——薄壳统一异常面
                last_err = e
                if attempt < 2:
                    time.sleep(1)
        raise last_err


def make_adapter(args):
    endpoint = args.endpoint or os.environ.get("SR_ENDPOINT")
    model = args.model or os.environ.get("SR_MODEL")
    provider = args.provider or os.environ.get("SR_PROVIDER")
    missing = [n for n, v in (("endpoint", endpoint), ("model", model),
                              ("provider", provider)) if not v]
    if missing:
        print(f"run: missing {missing} (--flag 或 SR_* env 注入)", file=sys.stderr)
        sys.exit(EXIT_USAGE)
    return NativeHTTPAdapter(endpoint, model, provider)


# ---- 模块 4：run 命令（L2 装配后请求入流 / L6 新 sid 强制 / D5 门控） ----
def cmd_run(args) -> int:
    sid = args.session
    if not SID_RE.match(sid or ""):
        print(f"run: bad session id {sid!r} (^[a-z0-9-]+$ <=64)", file=sys.stderr)
        return EXIT_USAGE
    w = EventWriter(sessions_dir())
    exists = w.path(sid).exists()
    if exists and not args.resume:  # L6：RULE-1 物理化——同 sid 复用必须显式 --resume
        print(f"run: session {sid} exists (resume with --resume)", file=sys.stderr)
        return EXIT_USAGE
    for g in (args.require_gate or []):  # D3 前置检查：审查 gate 未过实施不可启动
        if not gate_passed(w, sid, g):
            print(f"run: required gate '{g}' not passed in {sid}", file=sys.stderr)
            return EXIT_GATE_MISSING
    adapter = make_adapter(args)
    if not exists:
        w.append(sid, "system", "session_start",
                 input_={"task": args.task, "model": adapter.model,
                         "provider": adapter.provider, "endpoint": adapter.endpoint})
    if not adapter.endpoint_ready():  # D5：预检不可达即 exit 1，不发起主调用
        w.append(sid, "tool", "endpoint_unreachable",
                 input_={"endpoint": adapter.endpoint, "checked_at": now_iso()})
        print(f"run: endpoint unreachable: {adapter.endpoint}", file=sys.stderr)
        return EXIT_ENDPOINT
    prompt_text = args.prompt
    if args.prompt_file:
        prompt_text = Path(args.prompt_file).read_text(encoding="utf-8")
    if not prompt_text:
        print("run: --prompt or --prompt-file required", file=sys.stderr)
        return EXIT_USAGE
    messages = [{"role": "user", "content": prompt_text}]
    w.append(sid, "user", "prompt", input_={"messages": messages})
    w.append(sid, "assistant", "llm_request",  # L2：记录装配后实际请求
             input_={"messages": messages, "params": {}},
             model=adapter.model, provider=adapter.provider)
    resp = adapter.chat(messages)
    w.append(sid, "assistant", "llm_response", output=resp,
             model=adapter.model, provider=adapter.provider)
    w.append(sid, "system", "session_end", output={"status": "done"})
    try:
        text = resp["choices"][0]["message"]["content"]
    except Exception:
        text = json.dumps(resp, ensure_ascii=False)
    print(text)
    git_snapshot(sid, f"run:{sid} (session appended)")
    return 0


# ---- 模块 5：status / replay / fork 派生件（L1 状态=派生 / L4 共享流） ----
def cmd_status(args) -> int:
    w = EventWriter(sessions_dir())
    sids = [args.session] if args.session else sorted(
        p.stem for p in sessions_dir().glob("*.jsonl"))
    for sid in sids:
        rows = w.read(sid)
        if not rows:
            continue
        gates = {r["gate"]["name"]: r for r in rows if r.get("gate")}
        print(f"session: {sid}  seq_max: {rows[-1]['seq']}  "
              f"last_event: {rows[-1]['event']}")
        for name, r in gates.items():
            print(f"  gate[{name}]: {r['gate']['verdict']} "
                  f"(seq {r['seq']}, exit {r['gate']['exit']})")
    return 0


def cmd_replay(args) -> int:
    """重放校验：seq 从 1 单调 + 每行可解析 + llm_request 装配载荷完整（ADD 复现）。"""
    w = EventWriter(sessions_dir())
    rows = w.read(args.session)
    errors = []
    for i, r in enumerate(rows, 1):
        if r.get("seq") != i:
            errors.append(f"seq {r.get('seq')} != expected {i}")
        if r.get("session") != args.session:
            errors.append(f"seq {i}: session mismatch")
        if r.get("event") == "llm_request":
            msgs = (r.get("input") or {}).get("messages")
            if not (isinstance(msgs, list) and msgs):
                errors.append(f"seq {i}: llm_request input.messages empty")
    if errors:
        for e in errors:
            print(f"replay: {e}", file=sys.stderr)
        return 1
    print(f"replay: {len(rows)} rows OK (seq monotonic, schema parseable)")
    return 0


def cmd_fork(args) -> int:
    w = EventWriter(sessions_dir())
    src = w.read(args.session)
    if not src:
        print(f"fork: source session empty/missing: {args.session}", file=sys.stderr)
        return EXIT_USAGE
    if w.path(args.new).exists():
        print(f"fork: target session exists: {args.new}", file=sys.stderr)
        return EXIT_USAGE
    kept = [r for r in src if r["seq"] <= args.seq_from]
    if not kept:
        print(f"fork: no rows with seq <= {args.seq_from}", file=sys.stderr)
        return EXIT_USAGE
    p = w.path(args.new)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:  # L4：fork = 从事件 i 复制出新流
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"fork: {args.new} <- {args.session} (seq 1..{kept[-1]['seq']}, "
          f"{len(kept)} rows)")
    return 0


# ---- CLI 入口（模块 7 的一半；selftest 为另一半） ----
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="spec_runner",
        description="薄壳 spec 工作流 runner（P-009 方案 B）")
    p.add_argument("--version", action="version", version=VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="装配 prompt → LLM → 事件入流")
    r.add_argument("--task", required=True)
    r.add_argument("--session", required=True)
    r.add_argument("--prompt")
    r.add_argument("--prompt-file")
    r.add_argument("--resume", action="store_true")
    r.add_argument("--require-gate", action="append", default=[],
                   help="启动前须已在流中 pass 的 gate 名（可多次）")
    for flag in ("endpoint", "model", "provider"):
        r.add_argument(f"--{flag}")
    r.set_defaults(func=cmd_run)
    g = sub.add_parser("gate", help="流程门禁执行器（exit 透传）")
    g.add_argument("--name", required=True)
    g.add_argument("--cmd", required=True)
    g.add_argument("--session", required=True)
    g.add_argument("--cwd", help="命令工作目录")
    g.set_defaults(func=cmd_gate)
    s = sub.add_parser("status", help="派生视图：gate 通过态 / seq / 末事件")
    s.add_argument("--session")
    s.set_defaults(func=cmd_status)
    v = sub.add_parser("replay", help="重放校验（seq 单调 + 行可解析）")
    v.add_argument("--session", required=True)
    v.set_defaults(func=cmd_replay)
    f = sub.add_parser("fork", help="复制前 N seq 行至新流（L4）")
    f.add_argument("--session", required=True)
    f.add_argument("--seq", type=int, required=True, dest="seq_from")
    f.add_argument("--new", required=True)
    f.set_defaults(func=cmd_fork)
    sg = sub.add_parser("step-gate", help="决策产物管线校验（P-020：schema/evidence/step 序，只读）")
    sg.add_argument("--session", required=True)
    sg.add_argument("--expect", nargs="*", default=None,
                    help="期望完整链 step_id 列表（缺省 = 仅校验已登记链内部一致性）")
    sg.set_defaults(func=cmd_gate_step)
    st = sub.add_parser("selftest", help="内置自测（stdlib mock server）")
    st.set_defaults(func=lambda a: run_selftest())
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


# ---- selftest（R7 同构：计数自增机械计数，不硬编码——样本⑨ 教训） ----
def _mock_server(port):
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, obj, code=200):
            body = json.dumps(obj).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self._json({"data": []} if self.path == "/v1/models" else {})

        def do_POST(self):
            self._json({"choices": [{"message": {"role": "assistant",
                                                 "content": "mock-ok"}}]}
                       if self.path == "/v1/chat/completions" else {})

    srv = HTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def run_selftest() -> int:
    import shutil
    import tempfile

    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f" — {detail}" if detail else ""))

    tmp = Path(tempfile.mkdtemp(prefix="sr_selftest_"))
    # P-022 修正：子进程 env 显式剥离 SR_GIT_AUTOCOMMIT——父环境即使已导也不泄漏
    # （审查 §1.4：L467 env=dict(os.environ,...) 整体拷贝是绕过点）
    env = {k: v for k, v in os.environ.items() if k != GIT_AUTOCOMMIT_ENV}
    env[SESSIONS_ENV] = str(tmp)
    me = str(Path(__file__).resolve())

    def run_cli(*argv):
        return subprocess.run([sys.executable, me, *argv],
                              capture_output=True, text=True, env=env)

    print(f"selftest tmp dir: {tmp}")
    try:
        # F1-F5: gate 写入 + seq 单调 + exit 透传（pass/fail 两臂）+ schema
        p0 = run_cli("gate", "--name", "always-pass", "--session", "st-001",
                     "--cmd", "echo ok")
        check("F1 gate pass exit 透传", p0.returncode == 0)
        p5 = run_cli("gate", "--name", "always-fail", "--session", "st-001",
                     "--cmd", "exit 5")
        check("F2 gate fail exit 透传(=5)", p5.returncode == 5)
        w = EventWriter(tmp)
        rows = w.read("st-001")
        check("F3 事件流落盘可解析", len(rows) == 2)
        check("F4 seq 从 1 单调", [r["seq"] for r in rows] == [1, 2])
        check("F5 gate 事件 schema（name/exit/verdict）",
              all(r["gate"]["name"] and isinstance(r["gate"]["exit"], int)
                  and r["gate"]["verdict"] in ("pass", "fail") for r in rows))

        # F6/F7: schema 拒绝（写入端单点把守）——进程内直调
        for bad in (("bad-source", "tool", None),
                    ("st-x", "system", "no-such-event")):
            try:
                EventWriter(tmp).append(bad[0], bad[1], bad[2])
                check(f"F6 schema 拒绝 {bad}", False)
            except ValueError:
                check(f"F6 schema 拒绝 {bad}", True)
        try:
            EventWriter(tmp).append("st-x", "assistant", "llm_request",
                                    model=None, provider="p")
            check("F7 LLM 事件缺 model 拒绝", False)
        except ValueError:
            check("F7 LLM 事件缺 model 拒绝", True)

        # F8: replay 一致性
        pr = run_cli("replay", "--session", "st-001")
        check("F8 replay exit 0", pr.returncode == 0)

        # F9/F10: fork 复制前 1 行
        pf = run_cli("fork", "--session", "st-001", "--seq", "1",
                     "--new", "st-001f")
        check("F9 fork exit 0", pf.returncode == 0)
        check("F10 fork 内容 = 前 1 行",
              [r["seq"] for r in w.read("st-001f")] == [1])

        # F11: L6 拒绝对已存在 sid 无 --resume 的 run
        p_dup = run_cli("run", "--task", "t", "--session", "st-001",
                        "--prompt", "x", "--endpoint", "http://127.0.0.1:1",
                        "--model", "m", "--provider", "p")
        check("F11 L6 同 sid 无 --resume 拒绝(exit 2)", p_dup.returncode == 2)

        # F12/F13: 端点不可达 → exit 1 + endpoint_unreachable 事件（新 sid）
        p_ep = run_cli("run", "--task", "t", "--session", "st-ep",
                       "--prompt", "x", "--endpoint", "http://127.0.0.1:1",
                       "--model", "m", "--provider", "p")
        check("F12 端点不可达 exit 1", p_ep.returncode == 1)
        check("F13 endpoint_unreachable 入流",
              any(r["event"] == "endpoint_unreachable" for r in w.read("st-ep")))

        # F14-F16: gate 建流 → run --resume 同流续写（require-gate 同流前置通过）
        port, srv = 18742, None
        try:
            p_gate = run_cli("gate", "--name", "pre-gate", "--session",
                             "st-run", "--cmd", "echo ok")
            check("F14a 前置 gate 建流", p_gate.returncode == 0)
            srv = _mock_server(port)
            p_run = run_cli("run", "--task", "demo", "--session", "st-run",
                            "--resume", "--prompt", "hello",
                            "--require-gate", "pre-gate",
                            "--endpoint", f"http://127.0.0.1:{port}",
                            "--model", "mock-model", "--provider", "mock")
            check("F14 run 全链路 exit 0（require-gate 同流前置通过）",
                  p_run.returncode == 0, p_run.stderr.strip()[:120])
            rows_run = w.read("st-run")
            evs = [r["event"] for r in rows_run]
            check("F15 事件序列完整（gate 建流 + resume 续写）",
                  evs == ["gate", "prompt", "llm_request", "llm_response",
                          "session_end"], str(evs))
            check("F16 L2 装配后请求入流",
                  len(rows_run) >= 3 and
                  rows_run[-3]["input"]["messages"][0]["content"] == "hello")
        finally:
            if srv:
                srv.shutdown()

        # F17: require-gate 未过 → exit 3
        p_rg = run_cli("run", "--task", "t", "--session", "st-rg",
                       "--prompt", "x", "--require-gate", "never-passed",
                       "--endpoint", f"http://127.0.0.1:{port}",
                       "--model", "m", "--provider", "p")
        check("F17 require-gate 未过 exit 3", p_rg.returncode == 3)

        # F18: status 派生视图
        p_st = run_cli("status", "--session", "st-001")
        check("F18 status exit 0 且含 gate 态",
              p_st.returncode == 0 and "gate[always-pass]: pass" in p_st.stdout
              and "gate[always-fail]: fail" in p_st.stdout)

        # F19: replay 对坏 seq 流拒绝（手工构造 seq 跳跃流）
        bad_sid = "st-badseq"
        base_row = {"ts": now_iso(), "session": bad_sid, "source": "system",
                    "model": None, "provider": None, "input": None,
                    "output": None, "gate": None}
        r1 = dict(base_row, seq=1, event="session_start")
        r5 = dict(base_row, seq=5, event="session_end")
        (tmp / f"{bad_sid}.jsonl").write_text(
            json.dumps(r1, ensure_ascii=False) + "\n"
            + json.dumps(r5, ensure_ascii=False) + "\n", encoding="utf-8")
        p_rp = run_cli("replay", "--session", bad_sid)
        check("F19 replay 坏 seq exit 1", p_rp.returncode == 1)

        # F20-F23: step-gate 决策产物管线（P-020，CER §3.5）
        p_sg0 = run_cli("step-gate", "--session", "st-nod")
        check("F20 空流无 decision → exit 1", p_sg0.returncode == 1)
        w_sg = EventWriter(tmp)
        for i, st in enumerate(["research", "design"], 1):
            w_sg.append("st-ok", "assistant", "decision", input_={
                "category": "feature-design", "scenario": "s", "reasoning": "r",
                "outcome": "o", "confidence": 0.9,
                "metadata": {"step_id": st, "step_seq": i,
                             "evidence": [{"grade": "E1", "anchor": "spec/step-gate/DESIGN.md §4"}]}})
        p_sg_ok = run_cli("step-gate", "--session", "st-ok",
                          "--expect", "research", "design")
        check("F21 完整链 --expect 一致 → exit 0", p_sg_ok.returncode == 0, p_sg_ok.stdout[-80:])
        w_sg.append("st-miss", "assistant", "decision", input_={
            "category": "feature-design", "scenario": "s",
            "metadata": {"step_id": "research", "step_seq": 1,
                         "evidence": [{"grade": "E1", "anchor": "spec/x.md"}]}})
        p_sg_miss = run_cli("step-gate", "--session", "st-miss")
        check("F22 缺 reasoning/outcome/confidence → exit 1", p_sg_miss.returncode == 1)
        w_sg.append("st-soft", "assistant", "decision", input_={
            "category": "c", "scenario": "s", "reasoning": "r", "outcome": "o",
            "confidence": 0.9, "metadata": {"step_id": "research", "step_seq": 1,
            "evidence": [{"grade": "E1", "anchor": "not a valid anchor !!"}]}})
        p_sg_soft = run_cli("step-gate", "--session", "st-soft")
        check("F23 锚点形态存疑 → exit 2", p_sg_soft.returncode == 2)
        w_sg.append("st-badd", "assistant", "decision", input_={
            "category": "c", "scenario": "s", "reasoning": "r", "outcome": "o",
            "confidence": 0.9, "metadata": {"step_id": "XXX", "step_seq": 9,
            "evidence": [{"grade": "E1", "anchor": "spec/x.md"}]}})
        p_sg_badd = run_cli("step-gate", "--session", "st-badd")
        check("F24 step_id 非法 → exit 1", p_sg_badd.returncode == 1)

        # F25-F26: git_snapshot 懒加载门控 + 精确范围（P-022 A+B，临时 git 仓实证）
        git_tmp = Path(tempfile.mkdtemp(prefix="sr_gittest_"))
        sdir = git_tmp / "sessions"
        sdir.mkdir()
        (sdir / "real-001.jsonl").write_text("a\n", encoding="utf-8")
        (sdir / "real-002.jsonl").write_text("b\n", encoding="utf-8")
        for c in (["init", "-q"], ["config", "user.email", "t@t"],
                  ["config", "user.name", "t"]):
            subprocess.run(["git", *c], cwd=git_tmp, capture_output=True)
        sv, ac = os.environ.get(SESSIONS_ENV), os.environ.get(GIT_AUTOCOMMIT_ENV)
        os.environ[SESSIONS_ENV] = str(sdir)
        os.environ.pop(GIT_AUTOCOMMIT_ENV, None)
        git_snapshot("real-001", "m1")  # 默认关 → 零提交
        cnt0 = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=git_tmp,
                              capture_output=True, text=True)
        check("F25 git_snapshot 默认关零提交", cnt0.returncode != 0)
        os.environ[GIT_AUTOCOMMIT_ENV] = "1"
        git_snapshot("real-001", "m1")  # 显式激活 → 只提交 real-001
        os.environ.pop(GIT_AUTOCOMMIT_ENV, None)
        cnt1 = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=git_tmp,
                              capture_output=True, text=True)
        files_p = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"],
                                 cwd=git_tmp, capture_output=True, text=True)
        files = [l for l in files_p.stdout.splitlines() if l.strip()]
        msg_p = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=git_tmp,
                               capture_output=True, text=True)
        check("F26 git_snapshot 精确提交单文件+消息一致",
              cnt1.returncode == 0 and cnt1.stdout.strip() == "1"
              and files == ["sessions/real-001.jsonl"]
              and msg_p.stdout.strip() == "m1")
        if sv is not None:
            os.environ[SESSIONS_ENV] = sv
        else:
            os.environ.pop(SESSIONS_ENV, None)
        shutil.rmtree(git_tmp, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    passed = sum(1 for r in results if r)
    total = len(results)  # 机械计数（R7 同构，样本⑨ 教训）
    print(f"selftest: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
