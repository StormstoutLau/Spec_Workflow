---
id: arc-rollout-IMPLEMENTATION
type: design
version: 1.0
status: verified
date: 2026-09-09
depends: [arc-rollout-DESIGN, arc-rollout-RESEARCH]
upstream: null
---

# 实施文档：ARC 升级落地（吃狗粮模式，P-035）

> **Feature**: ARC（kegesch/arc 0.8.0）决策图谱升级
> **创建日期**: 2026-09-09
> **状态**: verified（已验证）
> **Spec 步骤**: Step 5-7（实施 + 验收）

## 1. 交付物清单

| 文件 | 职责 | 状态 |
|------|------|------|
| `tools/arc/arc_wrap.py` | 命令白名单封装器（D2 落地） | ✅ 实测 |
| `tools/arc/arc_prelink.py` | ADR 预链接脚本（D4 落地） | ✅ 实测 |
| `tools/arc/arc.exe` | ARC 0.8.0 Windows 二进制（gitignore） | ✅ sha256 校验 |
| `tools/arc/arc.sha256.md` | 版本快照固化（D3 落地） | ✅ 与官方一致 |
| `tools/arc/README.md` | 用法 + D7 停滞观察项登记（D1 文件布局交付） | ✅ 新增 |
| `tools/arc/data/.arc/` | 8 ADR 决策图谱（git 提交） | ✅ 8 实体 7 关系 |
| `spec/arc-rollout/` 四件套 | RESEARCH/DESIGN/IMPLEMENTATION/CHECKLIST | ✅ |
| `.gitignore` | arc.exe/node_modules/npm_tmp 排除 | ✅ |

## 2. 二进制获取与版本固化（D1/D3）

- **途径**: npm registry 可达（`npm install @kegesch/arc@0.8.0`），GitHub 直连超时——npm 分发含分平台二进制 `@kegesch/arc-win32-x64/arc.exe`（98,961,920 字节）
- **sha256**: `8f4b3089b17c1bafbeedcb3f5ef1b7f3d4a94c9a8c3b57acf763e26649df682a` = 官方 release v0.8.0 资产 sha256 **逐字节一致**（RESEARCH A-19/A-22 登记值复核）
- **分发链等价**: npm optionalDependencies → 同一官方发布产物
- **版本事实源**: `arc.sha256.md`（不信 `arc --version`，复测输出 0.1.0）

## 3. 命令白名单实测（D2）

封装器 `arc_wrap.py`：白名单命令透传，非白名单 exit 2。实测：

| 命令 | 结果 | 说明 |
|------|------|------|
| `init` | ✅ exit 0 | 落 data/.arc（10 目录 + arc.yaml） |
| `add` | ✅ | D-001~D-008 已导入 |
| `list --format json` | ✅ | 8 实体完整（id/title/type/status） |
| `check` | ✅ | 8 实体 7 关系健康报告（orphan 语义见 §6） |
| `next` | ✅ | 分类输出（orphan decisions） |
| `context D-001` | ✅ | 实体 + 关系闭包 |
| `trace D-008 --format json` | ✅ | **递归 2 跳 +**（D-008→D-004→D-003） |
| `impact D-004 --format json` | ✅ | 直接/间接影响者 |
| `link D-R --type driven_by` | ✅ | decision→requirement 方向实测合法 |
| `link D-D --type depends_on` | ✅ | decision→decision 方向实测合法 |
| `import adr/` | ✅ | 8 文件导入成功（D-001~D-008 中文保真） |
| `skill`（白名单外） | ⛔ exit 2 拦截 | 崩溃面规避（P-031 A-7 复测：13940 行 stack trace） |
| `bogus`（白名单外） | ⛔ exit 2 拦截 | 未知命令拦截 |

**白名单**: `init add list show trace impact check next context import link validate status graph`

## 4. 预链接脚本实测（D4）

`arc_prelink.py`：解析 ADR frontmatter depends → ARC depends_on 边。

- **ADR id → D-id 映射**: 动态解析（`list --format json` + 标题 ADR-NNNN 前缀匹配）
- **方向映射（实测校准，关键发现）**:
  - `link --help` 展示合法边 = `driven_by | enables | supersedes | derived_from | conflicts_with`
  - **运行时按实体类型动态校验**：decision → decision 仅 `enables | supersedes | depends_on`（`driven_by` 报错——实测捕获）
  - 本仓 ADR 簇（decision-only）→ 依赖链用 `depends_on` 边
- **实测结果**: 8 ADR → 依赖簇 **7 条 depends_on 边**全部链接成功：
  `D-002→D-001`（0005→0004）/ `D-003→D-002`（0006→0005）/ `D-004→D-003`（0007→0006）/ `D-006→D-004`（0009→0007）/ `D-007→D-004`（0010→0007）/ `D-008→D-004`+`D-008→D-007`（0011→0007,0010）

## 5. 图价值验证（D5 验收）

| 验收项 | 结果 | 实测 |
|--------|------|------|
| trace 递归 | ✅ | D-008 树含 ≥2 跳（D-008→D-004→D-003→...） |
| impact 影响面 | ✅ | D-004 直接影响 D-006/D-007/D-008 |
| check 健康报告 | ✅ | 8 实体 7 关系 / 0 断链 |
| 孤儿率 | 结构性 | decision-only 图全 orphan（无 requirement 层）——语义说明见 §6 |

## 6. 实测发现与处置（归 M7 候选）

1. **link 合法边按实体类型动态决定**（--help ≠ 运行时）：decision→decision 仅 `enables/supersedes/depends_on`——预链接脚本已用 depends_on 校准；登记为 ARC 文档盲区 + 预链接脚本契约
2. **orphan_decision 语义**：check 对无 requirement backing 的 decision 全标 orphan——本仓 ADR 簇是 decision-only 图（无 requirement 层），孤儿率为结构性事实非缺陷；图上价值 = 依赖链 trace/impact 递归（**已验证可用**）；如需消 orphan 需建 requirement 层（超出本批范围，登记候选）
3. **npm 分发链可用性**：GitHub 直连超时 → npm 途径成功且 sha256 与官方一致——两条路均验证

## 7. 零工具改动确认（D6）

- pre-commit hook：**零改动**（未新增 hook）
- 校验器（dc/m7/repo）：**零改动**
- spec_runner：**零改动**
- 仅新增 `tools/arc/` 目录 + `.gitignore` 3 行

## 8. 三通道校验（提交前）

- dc_validator / m7_stats / repo_stats → 见 CHECKLIST §2

**Review 签字**: _________ 日期: _________