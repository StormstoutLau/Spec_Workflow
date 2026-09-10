#!/usr/bin/env python3
"""P-038 DeepEval 评测臂助手：增强端评测运行 + 结果解析 + M7 样本登记草案。

子命令:
  selftest  内嵌自测（零真实端点、零 deepeval 依赖，expect 自增机械计数）
  eval      跑单个评测用例集（注入端点+模型，FaithfulnessMetric / GEval 评判
            LLM 输出相对上下文的事实忠实性，输出 0-1 分数 + reason）
  record    把 eval 输出 JSON → M7 §1 样本行草案（供人工确认归类后追加）

设计依据: spec/deepeval-arm/DEEPEVAL_M7_EVAL_DESIGN.md（方案：基础设施先行 + 端点就绪触发）
哲学对齐（I-6/R4）:
  - 评测横 / 生成端，不接验证端机械门禁（DeepEval 臂与 pf_m7_eval.py 正交，互补不强求）。
  - reason 即证据锚点如实输出（EVAL 的 judge 判断过程可审计 → 可登记为证据锚点）。
  - 端点不可达门控不假造（I-6）：TCP 探测不可达 → exit 1，不调 judge。
  - deepeval 库检测：不可用 → 打印安装提示，不裸崩。
"""

import argparse
import importlib
import json
import os
import socket
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- 内向默认测例（吃狗粮 FIR 用例）
# 两测例如实构造于 CER 语料：context = 一段"断言+取证"结构语句片段，
# oral 忠实用例（output 忠实重述）与负例（output 引入来源外信息），供 verify judge 是否区分。

CER_CONTEXT_FAITHFUL = (
    "DeepEval 是 Python 原生 pytest 评测框架，15.6k 星（2026-05 快照），"
    "研究背书指标含 faithfulness / answer relevancy / contextual precision 等，"
    "llm-as-a-judge + agent 追踪。【来源：scrolltest 评测综述】"
)
CER_CONTEXT_HALLU = (
    "DeepEval 臂候选作为 M7 评测矩阵（P-010 交付）第二臂：LLM-as-judge 指标（faithfulness 等）"
    "补 promptfoo 的 llm-rubric 缺失位点；Python 原生产物可直接嵌入校验器生态。"
    "首轮评测（端点就绪）后再行裁决。"
)

DEFAULT_CASES = [
    {
        "name": "faithful-01",
        "kind": "忠实用例",
        "input": "只依据下列来源对 DeepEval 作定位描述，不得添加来源之外的信息。",
        "output": "DeepEval 是 Python 原生的 pytest 评测框架；据 2026 年 5 月快照其 Star 数约 15.6k；"
                  "提供 faithfulness、answer relevancy、contextual precision 等研究背书的评测指标；"
                  "并采用 llm-as-a-judge 与 agent 追踪。",
        "context": [CER_CONTEXT_FAITHFUL],
        "expected_faithful": True,
    },
    {
        "name": "hallu-01",
        "kind": "引入来源外信息用例",
        "input": "只依据下列来源对 DeepEval 臂候选作定位描述，不得添加来源之外的信息。",
        "output": "DeepEval 作为 M7 评测矩阵（P-010 交付）的第二臂，用于补充 promptfoo 在 llm-rubric 上的缺失位点；"
                  "它拥有超过 200 个开箱即用的评测指标，并且其 Cloud 平台会自动记录每一次评测并生成可视化报告。",
        "context": [CER_CONTEXT_HALLU],
        "expected_faithful": False,
    },
]


# ---------------------------------------------------------------- 数据结构
@dataclass(frozen=True)
class MetricRec:
    name: str
    kind: str
    faithful_score: float
    faithful_reason: str
    geval_score: float | None
    geval_reason: str | None
    expected_faithful: bool
    faithful_passed: bool


@dataclass(frozen=True)
class EvalSummary:
    total: int
    faithful_passed: int
    detected_hallu: int   # 负例中被 Faithfulness 正确判低分（score < 0.7）的个数


# ---------------------------------------------------------------- 基础设施
def endpoint_reachable(host: str, port: int, timeout: float = 1.5) -> bool:
    """只读 TCP 预检（I-6 / 门控不假造）。"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def parse_endpoint(endpoint: str) -> tuple[str, int]:
    """从 http://host:port 提取 (host, port)。仅支持 http(s):// 形态。"""
    part = endpoint.split("://", 1)[-1]
    host_port = part.split("/", 1)[0]
    if ":" in host_port:
        host, _, port = host_port.rpartition(":")
        return host, int(port)
    return host_port, 80


def deepeval_available() -> bool:
    """检测 deepeval 库是否可导入（未装时返回 False，由调用方给安装提示）。"""
    try:
        importlib.import_module("deepeval")
        return True
    except ImportError:
        return False


def get_deepeval_api(endpoint: str, model: str, api_key: str):
    """延迟导入 deepeval 组件并注入端点（OpenAIModel base_url）。返回组件命名空间 dict。

    组件形态以 deepeval v4.2.2 为准；import 失败或签名不匹配时抛 RuntimeError（由 cmd_eval 兜成 exit 2）。
    """
    try:
        from deepeval.metrics import FaithfulnessMetric, GEval
        from deepeval.metrics.g_eval.utils import Rubric
        from deepeval.models import OpenAIModel
        from deepeval.test_case import LLMTestCase, LLMTestCaseParams
    except ImportError as e:  # pragma: no cover —— 由 availability 检测前置，双保险
        raise RuntimeError("deepeval 导入失败: %s" % e)
    try:
        llm = OpenAIModel(model=model, base_url=endpoint, api_key=api_key)
    except Exception as e:  # pragma: no cover
        raise RuntimeError("OpenAIModel 注入失败: %s" % e)
    return {"FaithfulnessMetric": FaithfulnessMetric,
            "GEval": GEval, "LLMTestCase": LLMTestCase,
            "LLMTestCaseParams": LLMTestCaseParams, "llm": llm}


def _measure_faithfulness(api, test_case) -> tuple[float, str, bool]:
    metric = api["FaithfulnessMetric"](threshold=0.7, strict_mode=True, async_mode=False,
                                       model=api["llm"])
    metric.measure(test_case)
    return metric.score, metric.reason, bool(getattr(metric, "success", False))


def _measure_geval(api, test_case) -> tuple[float, str]:
    metric = api["GEval"](
        name="事实忠实性（Faithfulness-style 判据）",
        criteria=("输出各句必须能从给定上下文中找到依据；引入上下文不存在的事实或数字视为不忠实。"),
        evaluation_steps=["逐句核对输出是否能在 context 中定位依据",
                          "若任何句子引入 context 外事实则判不忠实"],
        evaluation_params=[api["LLMTestCaseParams"].ACTUAL_OUTPUT,
                           api["LLMTestCaseParams"].RETRIEVAL_CONTEXT],
        threshold=0.7,
        strict_mode=True,
        async_mode=False,
        model=api["llm"],
    )
    metric.measure(test_case)
    return metric.score, metric.reason


# ---------------------------------------------------------------- eval
def make_test_cases(api, cases) -> list:
    """dict 用例 → deepeval LLMTestCase 列表（字段透传，machine 判定留 judge）。"""
    out = []
    for c in cases:
        out.append(api["LLMTestCase"](
            input=str(c.get("input", "")),
            actual_output=str(c.get("output", "")),
            retrieval_context=list(c.get("context", [])),
        ))
    return out


def run_eval(endpoint: str, model: str, api_key: str, cases: list | None = None,
             out_path: str | None = None) -> int:
    """门控端点 + 依赖 → 对每用例跑 FaithfulnessMetric(+GEval) → 输出 JSON。返回退出码。"""
    cases = cases if cases is not None else DEFAULT_CASES
    host, port = parse_endpoint(endpoint)
    if not endpoint_reachable(host, port):
        print("[P1] 端点不可达: %s——请启动 LM Studio 服务或换 --endpoint（I-6 门控不假造）" % endpoint)
        return 1
    if not deepeval_available():
        print("[P1] 未找到 deepeval 库——请先 `pip install deepeval`（或用本仓临时 venv）后重试（不可用时如实登记，不假造评测）")
        return 1
    try:
        api = get_deepeval_api(endpoint, model, api_key)
    except RuntimeError as e:
        print("[P2] deepeval API 初始化失败: %s" % e)
        return 2

    tcs = make_test_cases(api, cases)
    results = []
    faithful_passed = 0
    detected_hallu = 0
    for c, tc in zip(cases, tcs):
        try:
            fs, fr, ok = _measure_faithfulness(api, tc)
        except Exception as e:  # judge 网络/模型失败 → 如实登记，不假造
            print("[P2] Faithfulness 评测失败（%s）: %s" % (c["name"], e))
            fs, fr = 0.0, "评测失败（未产出 score）"
            ok = False
        gs, gr = (None, None)
        try:
            gs, gr = _measure_geval(api, tc)
        except Exception as e:  # GEval 失败不阻断 Faithfulness 主信号，如实标注
            print("[P2] GEval 评测失败（%s）: %s" % (c["name"], e))
        faithful_passed += 1 if ok and fs >= 0.7 else 0
        if (not c["expected_faithful"]) and fs < 0.7:
            detected_hallu += 1
        results.append(MetricRec(
            name=c["name"], kind=c["kind"],
            faithful_score=round(float(fs), 4), faithful_reason=fr,
            geval_score=round(float(gs), 4) if gs is not None else None, geval_reason=gr,
            expected_faithful=c["expected_faithful"], faithful_passed=ok and fs >= 0.7,
        ))
    summary = EvalSummary(len(results), faithful_passed, detected_hallu)

    payload = {
        "endpoint": endpoint, "model": model,
        "summary": {"total": summary.total, "faithful_passed": summary.faithful_passed,
                    "detected_hallu": summary.detected_hallu},
        "cases": [
            {"name": r.name, "kind": r.kind,
             "faithfulness_score": r.faithful_score, "faithfulness_reason": r.faithful_reason,
             "geval_score": r.geval_score, "geval_reason": r.geval_reason,
             "expected_faithful": r.expected_faithful, "faithful_passed": r.faithful_passed}
            for r in results],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if out_path:
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("[eval] 已写出: %s" % out_path)
    print(text)
    return 0


# ---------------------------------------------------------------- record
def to_m7_sample_row(status: str, model: str, num: int, date: str, source: str,
                     reason_snip: str) -> str:
    """生成 M7 §1 样本行草案（发现/形态II 留人工补全，reason 作证据锚点碎片）。"""
    return (f"| {num} | {date} | deepeval 评测（{model}） | DeepEval 臂（{status}）"
            f" | 待人工归并（faithfulness_score/reason 见评测 JSON） | 0 | {source} |"
            f" reason:`{reason_snip}`")


def cmd_record(results_path: str, date: str) -> int:
    """读 eval 输出 JSON → 打印 M7 §1 样本行草案（Step 9 补全出口）。"""
    try:
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[P1] 找不到 eval 结果 JSON: %s" % results_path)
        return 2
    except json.JSONDecodeError as e:
        print("[P1] eval 结果 JSON 解析失败: %s" % e)
        return 2
    cases = data.get("cases", [])
    if not cases:
        print("[P2] eval 结果无用例（可能门控未通过或空评测）")
        return 1
    model = data.get("model", "?")
    print("# total=%d faithful_passed=%d detected_hallu=%d"
          % (data["summary"]["total"], data["summary"]["faithful_passed"],
             data["summary"]["detected_hallu"]))
    for i, c in enumerate(cases, start=1):
        status = "PASS" if c.get("faithful_passed") else "FAIL"
        snip = (c.get("faithfulness_reason") or "")[:60]
        print(to_m7_sample_row(status, model, i, date, "spec/deepeval-arm", snip))
    return 0


# ---------------------------------------------------------------- selftest
def run_selftest() -> int:
    expect_count = 0
    fails = []

    def expect(cond: bool, msg: str) -> None:
        nonlocal expect_count
        expect_count += 1
        if not cond:
            fails.append(msg)

    # F1 端点解析
    h, p = parse_endpoint("http://127.0.0.1:1234/v1")
    expect(h == "127.0.0.1" and p == 1234, "F1 端点解析 host:port")
    h2, p2 = parse_endpoint("http://localhost")
    expect(h2 == "localhost" and p2 == 80, "F1 无端口默认 80")

    # F2 端点不可达预检（只读，不抛，不假造）
    expect(endpoint_reachable("127.0.0.255", 1, timeout=0.2) is False, "F2 端点不可达=False")

    # F3 deepeval 未安装检测（在系统空间（多半未装）返回 bool，不抛栈）
    importlib.invalidate_caches()
    expect(isinstance(deepeval_available(), bool), "F3 deepeval_available 返回 bool")

    # F4 默认测例结构：两类用例 + expected_faithful 相反
    expect(len(DEFAULT_CASES) == 2, "F4 默认两测例")
    expect(DEFAULT_CASES[0]["expected_faithful"] is True, "F4 忠实用例标记")
    expect(DEFAULT_CASES[1]["expected_faithful"] is False, "F4 引入来源外信息用例标记")
    expect(isinstance(DEFAULT_CASES[0]["context"], list) and len(DEFAULT_CASES[0]["context"]) == 1,
           "F4 context 结构")

    # F5 M7 登记草案（状态/model 透传 + reason 证据锚点碎片）
    row = to_m7_sample_row("PASS", "qwen2.5-7b-instruct", 34, "2026-09-10", "spec/deepeval-arm",
                           "no contradictions present")
    expect("deepeval 评测（qwen2.5-7b-instruct）" in row, "F5 草案含 model")
    expect(row.startswith("| 34 | 2026-09-10 |"), "F5 草案列序")
    expect("reason:`no contradictions present`" in row, "F5 reason 证据锚点碎片")

    # F6 门控：端点不可达时 run_eval 返回 1 且不触碰 deepeval
    rc = run_eval("http://127.0.0.255:1", "x", "k")
    expect(rc == 1, "F6 不可达门控 exit 1")

    if fails:
        print("selftest: %d/%d FAILED" % (len(fails), expect_count))
        for f in fails:
            print("  - %s" % f)
        return 1
    print("selftest: %d/%d PASS" % (expect_count, expect_count))
    return 0


# ---------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="deepeval_m7_eval", description="DeepEval M7 评测臂助手")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("selftest", help="内嵌自测（零真实端点 / 零 deepeval 依赖）")

    p_eval = sub.add_parser("eval", help="跑单套评测用例（FaithfulnessMetric + GEval）")
    p_eval.add_argument("--endpoint", default="http://127.0.0.1:1234/v1", help="OpenAI 兼容端点 base_url")
    p_eval.add_argument("--model", default="qwen2.5-7b-instruct", help="目标模型（注意 A-6：规避 qwen3.8-27b-uncensored 空输出）")
    p_eval.add_argument("--api-key", default="lm-studio")
    p_eval.add_argument("--cases", default=None, help="评测用例 JSON 路径（缺省 = 内置吃狗粮两测例）")
    p_eval.add_argument("--output", default=None, help="eval 结果 JSON 写出路径")

    p_record = sub.add_parser("record", help="解析 eval 结果 JSON → M7 样本行草案")
    p_record.add_argument("--results", required=True, help="eval 结果 JSON 路径")
    p_record.add_argument("--date", default="2026-09-10")

    args, _ = parser.parse_known_args(argv)
    if args.cmd == "selftest":
        return run_selftest()
    if args.cmd == "eval":
        cases = None
        if args.cases:
            try:
                with open(args.cases, "r", encoding="utf-8") as f:
                    cases = json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                print("[P1] 读取 --cases 失败: %s" % e)
                return 2
        return run_eval(args.endpoint, args.model, args.api_key, cases, args.output)
    if args.cmd == "record":
        return cmd_record(args.results, args.date)
    parser.print_help()
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # 顶层兜底（未知异常 → exit 2）
        print("[P2] 未预期异常: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)