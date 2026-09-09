# tools/arc —— ARC 决策图谱薄壳工具链（P-035）

ARC（kegesch/arc 0.8.0）决策图谱的**生成端辅助查询工具**（D6：不接 pre-commit/校验器，验证端仍由三校验器把守）。

## 组成

| 文件 | 职责 |
|------|------|
| `arc_wrap.py` | 命令白名单封装器（D2：skill/init-agent 崩溃面拦截 exit 2；版本事实源护栏） |
| `arc_prelink.py` | ADR 预链接脚本（D4：frontmatter depends → depends_on 边，ADR id→D-xxx 动态映射） |
| `arc.sha256.md` | 版本快照固化（D3：0.8.0 sha256，不信 `arc --version`） |
| `data/.arc/` | 8 ADR 决策图谱（git 提交；8 实体 7 depends_on 边） |
| `arc.exe` | ARC 0.8.0 Windows 二进制（gitignore，94.4MB，见 arc.sha256.md 获取） |

## 用法

```bash
python tools/arc/arc_wrap.py check            # 8 实体 7 关系健康报告
python tools/arc/arc_wrap.py trace D-008      # 依赖链递归（≥2 跳）
python tools/arc/arc_wrap.py impact D-004     # 影响面
python tools/arc/arc_prelink.py --dry-run     # ADR 依赖簇链接建议
python tools/arc/arc_prelink.py --execute     # 执行 arc link（经白名单）
```

## 铁律

- 所有 ARC 调用必须经 `arc_wrap.py`（白名单门，未知命令 exit 2）
- 不信 `arc --version`（0.1.0 失配，见 arc.sha256.md）
- 零依赖 stdlib only；ARC 二进制为外部工具非依赖

## 停滞观察项（D7）

**90 天无新 release（截至 2026-09-09）→ 评估 P-033 C-5 退路**：adr-explorer 只读看板 + ARC 受限使用 / 自研薄查询壳。触发时同步登记 PROGRESS。