#!/usr/bin/env python3
"""P-010 promptfoo 对比臂评测助手：运行封装 + 结果解析 + M7 样本登记草案。

子命令:
  run      注入 env → promptfoo eval（端点就绪预检门控）
  record   解析 results.json → M7 §1 样本行草案（供人工确认归类后追加）
  selftest 内嵌自测（零真实端点调用）

设计依据: PROMPTFOO_M7_EVAL_DESIGN.md（方案 Z：基础设施先行，端点就绪触发）
哲学: 登记 = 机械解析（I-4），异构于生成端（I-5），默认只读（I-1）。
"""

import argparse
import json
import os
import socket
import subprocess
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTFOO_DIR = os.path.join(ROOT, ".promptfoo")  # 存储重定向目标（沙箱绕过）


# ---------------------------------------------------------------- 数据结构（DESIGN §6）
@dataclass(frozen=True)
class EvalRecord:
    provider_label: str
    success: bool
    pass_: bool
    findings_count: int
    metadata: dict
    latency_ms: float
    cost: float


@dataclass(frozen=True)
class EvalSummary:
    successes: int
    failures: int
    errors: int
    total_tests: int


# ---------------------------------------------------------------- PM2 运行封装
def endpoint_reachable(host: str, port: int, timeout: float = 1.5) -> bool:
    """只读 TCP 预检（I-1 / 只读不变式）。"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def parse_endpoint(endpoint: str) -> tuple[str, int]:
    """从 http://host:port 提取 (host, port)。仅支持 http(s):// 形态。"""
    part = endpoint.split("://", 1)[-1]  # 去掉协议前缀
    host_port = part.split("/", 1)[0]    # 去掉路径
    if ":" in host_port:
        host, _, port = host_port.rpartition(":")
        return host, int(port)
    return host_port, 80


def call_promptfoo(cmd: list[str], env: dict) -> subprocess.CompletedProcess | None:
    """调 promptfoo CLI；未安装时提示安装命令并返回 None（DESIGN §7 错误处理）。"""
    try:
        return subprocess.run(cmd, env=env, cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError:
        print("[P1] 未找到 promptfoo CLI——请先 npm install -g promptfoo（DESIGN §7 错误处理）")
        return None


def run_eval(config: str, endpoint: str, model: str, api_key: str, output: str,
             endpoint2: str = "", model2: str = "") -> int:
    """注入 env + 双臂 provider 变量 → 调 promptfoo eval（子进程）。双臂端点均门控（I-6）。返回子进程退出码。"""
    for ep in (endpoint, endpoint2):
        if ep and not endpoint_reachable(*parse_endpoint(ep)):
            print(f"[P1] 端点不可达: {ep}——请启动 LM Studio 服务或换 --endpoint/--endpoint2（PROMPTFOO_M7_EVAL_DESIGN 方案 Z 运行门控）")
            return 1
    for d in ("", "cache", "logs"):
        os.makedirs(os.path.join(PROMPTFOO_DIR, d), exist_ok=True)
    cmd = [
        "promptfoo", "eval",
        "-c", config,
        "--output", output,
        "--no-share",
    ]
    env = dict(os.environ)
    env.update({
        "PROMPTFOO_CONFIG_DIR": PROMPTFOO_DIR,
        "PROMPTFOO_CACHE_PATH": os.path.join(PROMPTFOO_DIR, "cache"),
        "PROMPTFOO_LOG_DIR": os.path.join(PROMPTFOO_DIR, "logs"),
        "endpoint": endpoint,
        "model": model,
        "apiKey": api_key,
    })
    if endpoint2:
        env.update({"endpoint2": endpoint2, "model2": model2 or "cross-model"})
    print(f"[run] promptfoo eval -c {config} --output {output}")
    r = call_promptfoo(cmd, env)
    if r is None:
        return 1
    for line in r.stdout.splitlines():
        print(line)
    if r.stderr:
        for line in r.stderr.splitlines():
            print(line, file=sys.stderr)
    return r.returncode


# ---------------------------------------------------------------- PM3 结果解析
def parse_results(results: dict) -> tuple[list[EvalRecord], EvalSummary]:
    """机械解析 results.json → EvalRecord 列表 + 顶层 Summary（I-4：字段来自 JSON，不经 LLM）。"""
    rc = results.get("results", {})
    stats = rc.get("stats", {})
    summary = EvalSummary(
        successes=stats.get("successes", 0),
        failures=stats.get("failures", 0),
        errors=stats.get("errors", 0),
        total_tests=len(rc.get("results", [])),
    )
    records = []
    for item in rc.get("results", []):
        grading = item.get("gradingResult", {})
        provider = (item.get("provider", {}) or {}).get("label", "?")
        metadata = item.get("testCase", {}).get("metadata", {}) or {}
        records.append(EvalRecord(
            provider_label=provider,
            success=bool(item.get("success")),
            pass_=bool(grading.get("pass")),
            findings_count=0,  # 由语义归并（DESIGN §4.4），机械暂不推断
            metadata=metadata,
            latency_ms=float(item.get("latencyMs", 0) or 0),
            cost=float(item.get("cost", 0) or 0),
        ))
    return records, summary


# ---------------------------------------------------------------- PM4 M7 登记草案
def to_m7_sample_row(rec: EvalRecord, num: int, date: str, source: str) -> str:
    """EvalRecord → M7 §1 样本行草案（DESIGN §4.4；语义归类留人工）。"""
    status = "PASS" if rec.pass_ else "FAIL"
    return (f"| {num} | {date} | promptfoo 评测 | {rec.provider_label}（{status}）"
            f" | 待人工归并发现（results.json 机械字段） | 0 | {source} |")


# ---------------------------------------------------------------- record 输出
def cmd_record(results_path: str, date: str) -> int:
    """parse results.json → 打印 M7 §1 样本行草案（Step 9 补全的 CLI 出口）。"""
    try:
        with open(results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"[P1] 找不到 results.json: {results_path}")
        return 2
    except json.JSONDecodeError as e:
        print(f"[P1] results.json 解析失败: {e}")
        return 2
    records, summary = parse_results(results)
    if not records:
        print("[P2] results.json 无记录（可能是门控未通过或空评测）")
        return 1
    print(f"# total_tests={summary.total_tests} successes={summary.successes} "
          f"failures={summary.failures} errors={summary.errors}")
    for i, rec in enumerate(records, start=1):
        print(to_m7_sample_row(rec, i, date, "spec/promptfoo-m7-eval"))
    return 0


# ---------------------------------------------------------------- PM5 selftest
def run_selftest() -> int:
    expect_count = 0
    fails = []

    def expect(cond: bool, msg: str) -> None:
        nonlocal expect_count
        expect_count += 1
        if not cond:
            fails.append(msg)

    # F1 解析: 合法 results.json 子集 → EvalSummary/EvalRecord 精确值
    stub = {
        "results": {
            "stats": {"successes": 1, "failures": 1, "errors": 0},
            "results": [
                {"gradingResult": {"pass": True}, "provider": {"label": "base-model"},
                 "success": True, "latencyMs": 12.5, "cost": 0.1,
                 "testCase": {"metadata": {"报告": "X"}}},
                {"gradingResult": {"pass": False}, "provider": {"label": "cross-model"},
                 "success": False, "latencyMs": 8, "cost": 0.2,
                 "testCase": {"metadata": {}}},
            ],
        }
    }
    records, summary = parse_results(stub)
    expect(summary.total_tests == 2, "F1 total_tests=2")
    expect(summary.successes == 1 and summary.failures == 1, "F1 stats 精确")
    expect(records[0].provider_label == "base-model", "F1 provider label 解析")
    expect(records[0].pass_ is True and records[0].latency_ms == 12.5, "F1 逐字段")
    expect(records[1].pass_ is False, "F1 第二记录 PASS/FAIL")

    # F2 解析: 异常缺失字段（stats 缺）→ 零值兜底不崩
    rec2, sum2 = parse_results({"results": {}})
    expect(sum2.total_tests == 0 and sum2.successes == 0, "F2 缺字段兜底")
    expect(len(rec2) == 0, "F2 无记录")

    # F3 端点预检: 已知不可达端口 → False（只读，不抛）
    expect(endpoint_reachable("127.0.0.255", 1, timeout=0.2) is False, "F3 端点不可达=False")

    # F4 端点解析
    h, p = parse_endpoint("http://192.168.1.11:1234")
    expect(h == "192.168.1.11" and p == 1234, "F4 端点解析 host:port")
    h2, p2 = parse_endpoint("http://10.0.0.1")
    expect(h2 == "10.0.0.1" and p2 == 80, "F4 无端口默认 80")

    # F5 M7 登记草案（provider/状态）
    row = to_m7_sample_row(records[0], 24, "2026-08-23", "spec/promptfoo-m7-eval")
    expect("base-model（PASS）" in row, "F5 草案含 provider+状态")
    expect(row.startswith("| 24 | 2026-08-23 |"), "F5 草案列序")

    # F6 promptfoo 未安装兜底: 不存在的命令 → None（FileNotFoundError 被捕获，不崩栈）
    r6 = call_promptfoo(["no_such_cmd_pf_probe_xyz"], dict(os.environ))
    expect(r6 is None, "F6 未安装兜底=None")

    if fails:
        print("selftest: %d/%d FAILED" % (len(fails), expect_count))
        for f in fails:
            print("  - %s" % f)
        return 1
    print("selftest: %d/%d PASS" % (expect_count, expect_count))
    return 0


# ---------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pf_m7_eval", description="promptfoo M7 对比臂评测助手")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="运行评测（双臂端点就绪门控）")
    p_run.add_argument("--config", default=os.path.join("spec", "promptfoo-m7-eval", "promptfooconfig.yaml"))
    p_run.add_argument("--endpoint", default="http://192.168.1.11:1234",
                       help="同基座臂端点（工作站 A）")
    p_run.add_argument("--endpoint2", default="http://192.168.1.15:1234",
                       help="异基座臂端点（工作站 B）")
    p_run.add_argument("--model", default="base-model")
    p_run.add_argument("--model2", default="cross-model")
    p_run.add_argument("--api-key", default="lm-studio")  # LM Studio 免鉴权，占位
    p_run.add_argument("--output", default=os.path.join(PROMPTFOO_DIR, "results.json"))

    sub.add_parser("selftest", help="内嵌自测（零真实端点）")

    p_record = sub.add_parser("record", help="解析 results.json → M7 样本行草案")
    p_record.add_argument("--results", default=os.path.join(PROMPTFOO_DIR, "results.json"),
                          help="promptfoo 输出 JSON 路径")
    p_record.add_argument("--date", default="2026-08-23", help="样本登记日期（YYYY-MM-DD）")

    args, _ = parser.parse_known_args(argv)
    if args.cmd == "selftest":
        return run_selftest()
    if args.cmd == "run":
        return run_eval(args.config, args.endpoint, args.model, args.api_key, args.output,
                        endpoint2=args.endpoint2, model2=args.model2)
    if args.cmd == "record":
        return cmd_record(args.results, args.date)
    parser.print_help()
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # 顶层兜底（DESIGN §7 未知异常 → exit 2）
        print(f"[P2] 未预期异常: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)