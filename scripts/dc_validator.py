#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DC 契约校验器（DC1-DC4 + R7）——契约的机器可读定义。

权威源：spec/doc-contract/PLAN.md §1 DC1-DC4 (v1.6) + adr/ADR-0007 D4/D5
       + docs/ASSERTION_EVIDENCE_FRAMEWORK.md v1.4 R7。
词表常量逐字符复制自 spec/precommit-dc-validator/DESIGN.md §6.3（I-4 单一真值源）。

不变式（DESIGN §8）：I-1 只读 / I-2 确定性 / I-3 零新规则 / I-4 单一真值源 / I-5 异构于生成端。
退出码：0 全部通过 / 1 发现契约违规 / 2 工具自身错误。

用法：
  python scripts/dc_validator.py                     # 全仓全检查（默认 --check-all）
  python scripts/dc_validator.py file1.md file2.md   # 指定文件（pre-commit staged 语义）
  python scripts/dc_validator.py --check-namespace   # 单项组合
  python scripts/dc_validator.py --selftest          # 内嵌自测（fixture 见 IMPLEMENTATION §8.1）
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass

# --- 仓库根（脚本位于 <root>/scripts/，与 cwd 无关，I-2） ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- DC2 词表（DESIGN §6.3；权威源 PLAN v1.6 §1 DC2 + ADR-0007 D4/D5） ---
TYPE_VOCAB = {
    "adr":              {"proposed", "accepted", "superseded", "deferred"},
    "discovery":        {"open", "resolved", "toolized"},
    "process-spec":     {"active", "deprecated"},
    "framework":        {"active", "deprecated"},
    "template":         {"draft", "in-review", "verified"},
    "design":           {"draft", "in-review", "verified"},  # 一般设计文档（id 不以 -CHECKLIST 结尾）
}
# 副轴（PLAN v1.6 DC2 消歧）：id 以 "-CHECKLIST" 结尾的 design 文档用 CHECKLIST 词表
CHECKLIST_STATUS_VOCAB = {"pending", "accepting", "accepted"}

SEVEN_FIELDS = ("id", "type", "version", "status", "date", "depends", "upstream")
FM_WINDOW = 10                          # DR-1：front-matter 围栏检测窗口（前 N 行）
TIER_PREFIXES = ("源项目·", "外部·", "本地工具·")   # DC3 档 2-4 标注前缀
QUOTE_MARKERS = ("引文:", '"quote":')             # M5：引文行（源仓库路径空间）
TEMPLATE_DIR = os.path.join("spec", "templates")  # DR-3：模板占位链接排除

UNPARSABLE = "UNPARSABLE"  # front-matter 存在但结构不可解析的哨兵


@dataclass(frozen=True)
class CheckResult:
    check_id: str      # "dc1" | "dc2" | "dc4" | "r7" | "dc3"
    file: str          # 相对路径
    severity: str      # "P1" | "P2" | "P3" | ""（空 = skip，非违规）
    message: str
    line: int | None = None


class Summary:
    """DESIGN §6.2：violations = severity 非空的结果。"""

    def __init__(self, results):
        self.results = list(results)

    @property
    def violations(self):
        return [r for r in self.results if r.severity]

    @property
    def passed(self):
        return not self.violations


# ---------------------------------------------------------------- M2 frontmatter

def parse_frontmatter(text):
    """返回 (fm_dict, close_line) / (None, None) 无 front-matter / (UNPARSABLE, None) 结构错误。

    检测窗口 = 前 FM_WINDOW 行（DR-1：覆盖首行式与标题后式两种实测形态）。
    值形态：单行 key: value / 流式数组 [a, b] / null / 裸标量（IMPLEMENTATION §2.1）。
    """
    lines = text.splitlines()
    open_idx = None
    for i, ln in enumerate(lines[:FM_WINDOW]):
        if ln.strip() == "---":
            open_idx = i
            break
    if open_idx is None:
        return None, None
    fm = {}
    kv_count = 0
    for j in range(open_idx + 1, len(lines)):
        ln = lines[j]
        if ln.strip() == "---":
            if kv_count == 0:
                return None, None  # 装饰性分隔线（README/CODE_WIKI 场景），非 front-matter
            return fm, j
        if not ln.strip():
            continue
        m = re.match(r"^([A-Za-z_-]+):\s?(.*)$", ln)
        if not m:
            if kv_count == 0:
                return None, None  # 开围栏后首个非空行非 key: value → 非 front-matter
            return UNPARSABLE, None  # 围栏内出现无 key: 结构的行
        fm[m.group(1)] = m.group(2).strip()
        kv_count += 1
    return (UNPARSABLE, None) if kv_count else (None, None)  # 未闭合


def check_frontmatter(file, text):
    """M2：DC1 七字段 + DC2 词表（design 二档判定 = id 后缀 -CHECKLIST）。"""
    fm, _ = parse_frontmatter(text)
    if fm == UNPARSABLE:
        return [CheckResult("dc1", file, "P1", "front-matter 非合法 YAML: 围栏内存在无 key: value 结构的行")]
    if fm is None:
        return [CheckResult("dc1", file, "", "不在 DC 契约范围（无 front-matter）")]
    results = []
    for k in SEVEN_FIELDS:
        if k not in fm:
            results.append(CheckResult("dc1", file, "P1", "DC1 缺失字段: %s" % k))
    t, s = fm.get("type"), fm.get("status")
    if t is not None and t not in TYPE_VOCAB:
        results.append(CheckResult("dc2", file, "P1",
                                   "DC2 非法 type: %r（允许: %s）" % (t, "/".join(sorted(TYPE_VOCAB)))))
    elif t is not None and s is not None:
        vocab = (CHECKLIST_STATUS_VOCAB
                 if t == "design" and fm.get("id", "").endswith("-CHECKLIST")
                 else TYPE_VOCAB.get(t, set()))
        if s not in vocab:
            results.append(CheckResult("dc2", file, "P1",
                                       "DC2 非法 status: %r（type %s 允许: %s）" % (s, t, "/".join(sorted(vocab)))))
    return results


# ---------------------------------------------------------------- M3 namespace

def check_namespace(files, root=ROOT):
    """M3：DC4 id 全仓唯一（输入必须为全仓 .md 集，非 staged-only）。重复方全部报告。"""
    seen = {}
    for f in files:
        full = os.path.normpath(os.path.join(root, f))
        try:
            with open(full, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        fm, _ = parse_frontmatter(text)
        if isinstance(fm, dict) and "id" in fm:
            seen.setdefault(fm["id"], []).append(f)
    results = []
    for doc_id, paths in sorted(seen.items()):
        if len(paths) > 1:
            for p in paths:
                results.append(CheckResult("dc4", p, "P1", "DC4 重复 id %r: %s" % (doc_id, paths)))
    return results


# ---------------------------------------------------------------- M4 counting

RE_STAT_ROW = {
    "A": re.compile(r"^\|\s*A\s*事实类\s*\|\s*(\d+)"),
    "B": re.compile(r"^\|\s*B\s*推断类\s*\|\s*(\d+)"),
    "H": re.compile(r"^\|\s*假设区\s*\|\s*(\d+)"),
}
RE_A_MARK = re.compile(r"(?:^|\|\s*)【A】", re.M)   # 行首 + 表格单元格内（IMPLEMENTATION §3.4）
RE_B_ID = re.compile(r'"id":\s*"B\d+"')             # 附录 B 机读登记
RE_H_ITEM = re.compile(r"\[H\d+\]")                 # 附录 C 假设区条目
RE_STAT_SECTION = re.compile(r"^##\s*0[\.、]?\s*断言统计表", re.M)
# C 类首版不对账（DR-2：标记格式无统一契约——原生文档行首标记 vs 吸收文档语义计数）


def check_counting(file, text):
    """M4：R7——§0 统计表声明计数 = 机械重数（A/B/H 三类）。"""
    if not RE_STAT_SECTION.search(text):
        return []
    declared = {}
    for ln in text.splitlines():
        s = ln.strip()
        for k, rx in RE_STAT_ROW.items():
            m = rx.match(s)
            if m:
                declared[k] = int(m.group(1))
    actual = {
        "A": len(RE_A_MARK.findall(text)),
        "B": len(RE_B_ID.findall(text)),
        "H": len(RE_H_ITEM.findall(text)),
    }
    results = []
    for k in ("A", "B", "H"):
        if k in declared and declared[k] != actual[k]:
            results.append(CheckResult("r7", file, "P1",
                                       "§0 %s 类声明 %d 实为 %d" % (k, declared[k], actual[k])))
    return results


# ---------------------------------------------------------------- M5 linkcheck

RE_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def check_links(file, text, root=ROOT):
    """M5：DC3 档 1——仓库内相对链接可解析。

    排除上下文（DR-3）：fenced code block / 引文行（引文: 或 "quote":）/ spec/templates/。
    档 2-4 标注（链接文本前缀 源项目·/外部·/本地工具·）不跨仓解析。
    """
    if file.replace("\\", "/").startswith(TEMPLATE_DIR.replace("\\", "/")):
        return []
    results = []
    in_fence = False
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if any(mk in ln for mk in QUOTE_MARKERS):
            continue
        for m in RE_MD_LINK.finditer(ln):
            label, tgt = m.group(1).strip(), m.group(2).strip()
            if tgt.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if label.startswith(TIER_PREFIXES):
                continue
            p = tgt.split("#")[0].strip()
            if not p:
                continue
            base = os.path.dirname(os.path.normpath(os.path.join(root, file)))
            if not os.path.exists(os.path.normpath(os.path.join(base, p))):
                results.append(CheckResult("dc3", file, "P2", "档 1 相对链接不可解析: %s" % tgt, i))
    return results


# ---------------------------------------------------------------- M1 CLI

def gather_md_files(root=ROOT):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            if fn.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), root))
    return sorted(out)


def _read(full):
    with open(full, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def run_checks(files, checks, root=ROOT):
    """逐文件检查（M2/M4/M5）+ 强制全仓 namespace（M3）。返回 list[CheckResult]。"""
    results = []
    for f in files:
        full = os.path.normpath(os.path.join(root, f))
        try:
            text = _read(full)
        except OSError as e:
            results.append(CheckResult("dc1", f, "P2", "文件不可读: %s" % e))
            continue
        if "frontmatter" in checks:
            results += check_frontmatter(f, text)
        if "counting" in checks:
            results += check_counting(f, text)
        if "links" in checks:
            results += check_links(f, text, root)
    if "namespace" in checks:
        results += check_namespace(gather_md_files(root), root)
    return results


ALL_CHECKS = ("frontmatter", "namespace", "counting", "links")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="dc_validator", description="DC 契约校验器（DC1-DC4 + R7）")
    ap.add_argument("--check-all", action="store_true", help="全部检查（默认）")
    ap.add_argument("--check-frontmatter", action="store_true", help="DC1 七字段 + DC2 词表")
    ap.add_argument("--check-namespace", action="store_true", help="DC4 id 全仓唯一")
    ap.add_argument("--check-counting", action="store_true", help="R7 计数 = 机械重数")
    ap.add_argument("--check-links", action="store_true", help="DC3 档 1 相对链接")
    ap.add_argument("--selftest", action="store_true", help="内嵌自测（IMPLEMENTATION §8.1）")
    ap.add_argument("files", nargs="*", help="目标 .md（缺省 = 全仓；pre-commit 传入 staged 列表）")
    args = ap.parse_args(argv)
    if args.selftest:
        return run_selftest()

    selected = {c for c in ALL_CHECKS if getattr(args, "check_" + c)}
    if args.check_all or not selected:
        selected = set(ALL_CHECKS)

    try:
        files = args.files if args.files else gather_md_files()
        results = run_checks(files, selected)
    except Exception as e:  # 工具自身错误 ≠ 校验通过（DESIGN §3.4 补注）
        sys.stderr.write("[tool-error] %s: %s\n" % (type(e).__name__, e))
        return 2

    summary = Summary(results)
    for r in summary.results:
        tag = "[%s]" % r.severity if r.severity else "[skip]"
        loc = " (L%d)" % r.line if r.line else ""
        print("%s %s: %s%s" % (tag, r.file, r.message, loc))
    if summary.passed:
        print("DC 契约校验通过：%d 文件，%d 结果，0 违规" % (len(files), len(summary.results)))
        return 0
    print("DC 契约校验失败：%d 违规（P1=%d P2=%d）" % (
        len(summary.violations),
        sum(1 for r in summary.violations if r.severity == "P1"),
        sum(1 for r in summary.violations if r.severity == "P2")))
    return 1


# ---------------------------------------------------------------- selftest

FM_OK = ("---\nid: selftest-ok-RESEARCH\ntype: design\nversion: 1.0\n"
         "status: draft\ndate: 2026-08-19\ndepends: [x]\nupstream: null\n---\n\n# t\n")


def run_selftest():
    """十三 fixture（IMPLEMENTATION §8.1 F1-F10，含 F3b/F3c/F8b 分支），tempfile 构造于系统临时目录（I-1 不触工作树）。"""
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="dcv_selftest_")
    fails = []
    total = [0]  # 机械计数（R7 同构：计数由 expect 调用自增，不手填）

    def expect(cond, msg):
        total[0] += 1
        print("  %s %s" % ("PASS" if cond else "FAIL", msg))
        if not cond:
            fails.append(msg)

    def w(name, content):
        p = os.path.join(tmp, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        return os.path.relpath(p, tmp)

    try:
        # F1 七字段缺失 depends
        f1 = w("f1.md", FM_OK.replace("depends: [x]\n", ""))
        r = check_frontmatter(f1, _read(os.path.join(tmp, f1)))
        expect(any(x.severity == "P1" and "depends" in x.message for x in r), "F1 DC1 缺字段报 P1")

        # F2 围栏内结构错误
        f2 = w("f2.md", "---\nid: x\nbroken line no colon\n---\n")
        r = check_frontmatter(f2, _read(os.path.join(tmp, f2)))
        expect(any(x.severity == "P1" and "非合法 YAML" in x.message for x in r), "F2 yaml-unparsable 报 P1")

        # F3 status 词表非法
        f3 = w("f3.md", FM_OK.replace("status: draft", "status: bogus"))
        r = check_frontmatter(f3, _read(os.path.join(tmp, f3)))
        expect(any(x.severity == "P1" and "非法 status" in x.message for x in r), "F3 DC2 词表报 P1")

        # F3b CHECKLIST 副轴：id 尾缀 -CHECKLIST 时 pending 合法、draft 非法
        f3b = w("f3b.md", FM_OK.replace("id: selftest-ok-RESEARCH", "id: x-CHECKLIST")
                .replace("status: draft", "status: pending"))
        r = check_frontmatter(f3b, _read(os.path.join(tmp, f3b)))
        expect(not any("status" in x.message for x in r), "F3b CHECKLIST 词表 pending 合法")
        f3c = w("f3c.md", FM_OK.replace("id: selftest-ok-RESEARCH", "id: x-CHECKLIST"))
        r = check_frontmatter(f3c, _read(os.path.join(tmp, f3c)))
        expect(any("非法 status" in x.message for x in r), "F3c CHECKLIST 词表 draft 非法")

        # F4 §0 计数差
        f4 = w("f4.md", FM_OK + "\n## 0. 断言统计表\n\n| 级别 | 条数 |\n|---|---|\n| A 事实类 | 3 |\n\n【A】x\n【A】y\n")
        r = check_counting(f4, _read(os.path.join(tmp, f4)))
        expect(any(x.severity == "P1" and "声明 3 实为 2" in x.message for x in r), "F4 R7 计数差报 P1")

        # F5 无 front-matter → skip
        f5 = w("f5.md", "# plain doc\n")
        r = check_frontmatter(f5, _read(os.path.join(tmp, f5)))
        expect(len(r) == 1 and r[0].severity == "" and "不在 DC 契约范围" in r[0].message, "F5 范围外 [skip]")

        # F6 id 重复（双方各报）
        w("f6a.md", FM_OK.replace("id: selftest-ok-RESEARCH", "id: dup-id"))
        w("f6b.md", FM_OK.replace("id: selftest-ok-RESEARCH", "id: dup-id"))
        r = check_namespace(["f6a.md", "f6b.md"], root=tmp)
        expect(len(r) == 2 and all(x.severity == "P1" for x in r), "F6 DC4 重复双方各报 P1")

        # F7 不可读文件 → P2 不崩溃
        r = run_checks(["no_such_file.md"], {"frontmatter"}, root=tmp)
        expect(any(x.severity == "P2" and "不可读" in x.message for x in r), "F7 不可读文件报 P2")

        # F8 断链 / 档 2 标注 / 引文行三分流
        w("f8_target.md", FM_OK)
        f8 = w("f8.md", FM_OK + "\n[missing](./nope.md)\n[源项目·p](../anywhere.md)\n"
                             "> 引文: [q](./also-missing.md)\n[ok](./f8_target.md)\n")
        r = check_links(f8, _read(os.path.join(tmp, f8)), root=tmp)
        expect(len(r) == 1 and r[0].severity == "P2" and "nope.md" in r[0].message, "F8 仅真断链报 P2")

        # F8b templates 排除
        f8b = w(os.path.join("spec", "templates", "f8b.md"), FM_OK + "\n[t](./nope.md)\n")
        r = check_links(f8b, _read(os.path.join(tmp, f8b)), root=tmp)
        expect(len(r) == 0, "F8b templates 占位链接排除")

        # F9 合规文件零误报（含 §0 对账一致）
        f9 = w("f9.md", FM_OK + "\n## 0. 断言统计表\n\n| 级别 | 条数 |\n|---|---|\n| A 事实类 | 1 |\n\n【A】one\n")
        text = _read(os.path.join(tmp, f9))
        r = check_frontmatter(f9, text) + check_counting(f9, text) + check_links(f9, text, root=tmp)
        expect(not any(x.severity for x in r), "F9 合规文件零违规")

        # F10 无 front-matter 但含装饰性 --- 分隔线（dry-run 首跑 5 误报回归）
        f10 = w("f10.md", "# 标题\n\n---\n\n正文段落，非 key: value。\n")
        r = check_frontmatter(f10, _read(os.path.join(tmp, f10)))
        expect(len(r) == 1 and r[0].severity == "" and "不在 DC 契约范围" in r[0].message,
               "F10 装饰性 --- 分隔线判为范围外 [skip]")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if fails:
        print("selftest: %d/%d FAILED" % (len(fails), total[0]))
        return 1
    print("selftest: %d/%d PASS" % (total[0], total[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
