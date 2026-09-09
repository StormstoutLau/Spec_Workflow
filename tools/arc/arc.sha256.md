# ARC 0.8.0 二进制版本快照（P-035 版本固化，D3）

- **包**: @kegesch/arc 0.8.0（npm 分发）→ 分平台二进制 @kegesch/arc-win32-x64
- **获取途径**: `npm install @kegesch/arc@0.8.0`（2026-09-09，registry.npmjs.org 可达）
- **文件**: `tools/arc/arc.exe`（98,961,920 字节）
- **sha256**: `8f4b3089b17c1bafbeedcb3f5ef1b7f3d4a94c9a8c3b57acf763e26649df682a`
- **比对**: 与官方 GitHub release v0.8.0 资产 `arc-win32-x64.exe` sha256 **一致**（RESEARCH A-19/A-22 登记值）→ 分发链等价
- **版本事实源**: 本 sha256 表 + tag v0.8.0（**不信 `arc --version`**，P-031 A-5 实测失配 0.1.0）
- **升级策略**: 升级须改本表 + 三校验器重跑 + diff 命令比对新旧行为；90 天无新 release → 评估 P-033 C-5 退路

## 实测命令面（白名单验证，2026-09-09）

见 [IMPLEMENTATION v1.0](../../spec/arc-rollout/IMPLEMENTATION.md) §3（白名单实测清单）。