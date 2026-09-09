#!/usr/bin/env python3
"""ARC 命令白名单封装器（P-035，吃狗粮实施）——规避矩阵 D2 落地。

职责：
  - 白名单门：仅放行实测可用主命令链（RESEARCH A-8 实测 + 本批复测）
  - 排除缺陷命令面：skill / init-agent（Windows 崩溃，P-031 A-7 复测）
  - 版本事实源护栏：不信 `arc --version`（失配 0.1.0 vs 0.8.0，P-031 A-5）
    用法 `arc_wrap.py version` 返回固化 sha256 登记文档性输出（exit 0），
    不调 ARC 二进制自身版本命令。

零依赖 stdlib only。用法：
  python tools/arc/arc_wrap.py <cmd> [args...]
  python tools/arc/arc_wrap.py version   # 输出版本事实源指针
  python tools/arc/arc_wrap.py whitelist # 输出白名单
"""
import os
import subprocess
import sys

# ── 白名单（实测可用主命令链；增补须过实测 + 本文件 + DESIGN 追记）──
WHITELIST = {
    "init", "add", "list", "show", "trace", "impact", "check",
    "next", "context", "import", "link", "validate", "status", "graph",
}

BLOCKED_BY_DESIGN = {
    # skill / init-agent = Windows 构建路径崩溃面（P-031 A-7 + 本批复测）
    "skill", "init-agent",
    # 写操作面窄或未实测（0.x 阶段保持白名单前置）
    "edit", "remove", "rename", "promote", "invalidate", "obsoleted",
    "unlink", "query", "diff", "related",
}

ARC_DIR = os.path.dirname(os.path.abspath(__file__))
ARC_EXE = os.path.join(ARC_DIR, "arc.exe")
SHA256_DOC = os.path.join(ARC_DIR, "arc.sha256.md")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(f"用法: python {os.path.basename(__file__)} <cmd> [args...]", file=sys.stderr)
        return 2

    cmd = args[0]
    if cmd == "version":
        print("ARC 版本事实源 = tools/arc/arc.sha256.md（固化 0.8.0 sha256: 8f4b3089...）")
        print("不信 `arc --version`（0.1.0 失配，P-031 A-5）。")
        return 0
    if cmd == "whitelist":
        print("白名单: " + " ".join(sorted(WHITELIST)))
        print("设计排除: " + " ".join(sorted(BLOCKED_BY_DESIGN)))
        return 0

    if cmd not in WHITELIST:
        print(f"[arc_wrap] 命令 '{cmd}' 不在白名单（exit 2）。"
              f"允许: {sorted(WHITELIST)}", file=sys.stderr)
        return 2

    if not os.path.exists(ARC_EXE):
        print(f"[arc_wrap] 缺少二进制: {ARC_EXE}（见 arc.sha256.md 获取）", file=sys.stderr)
        return 2

    # 装配 .arc 数据目录上下文：arc_wrap 始终在 tools/arc/data 下运行（init 落 data）
    data_dir = os.path.join(ARC_DIR, "data")
    env = os.environ.copy()
    os.makedirs(data_dir, exist_ok=True)
    cwd = data_dir

    proc = subprocess.run(
        [ARC_EXE, *args], cwd=cwd, env=env,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())