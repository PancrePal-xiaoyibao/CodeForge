---
description: 宿主机一键初始化 — 环境探测+缺口提醒+codebase-mcp 部署提醒+分层注入体系生成（规则主文档+外置参考+pi 强化层；全局/项目可选）
---

把当前机器初始化为合格开发主机：探测软硬件环境（`scripts/host-scan.sh` 或 `host-scan.ps1`）→ 对照基线提醒安装缺失开发环境（git/rg/uv/conda/node/gh）→ 提醒部署 codebase-memory-mcp → 交互选择文档规范与生成位置（全局 `AGENTS.md` + agent 镜像 / 项目 `./AGENTS.md` 等）→ 按 `templates/host-injection.template.md` 按段渲染**分层注入体系**：

1. **规则主文档**（`[RULES]` 段）：行为规则 + 外置参考触发表，写入 `AGENTS.md` 并逐字镜像到 `CLAUDE.md`(claude) / `AGENTS.md`(codex) / `GEMINI.md`(gemini)；
2. **外置参考**（`[ENVIRONMENT]` 段）：本机探测画像写入 `agent-reference/environment.md`（硬件/代理/环境速查/三平台路径表），触发式读取不常驻注入；
3. **pi 强化层**（`[APPEND]` 段）：探测到 `.pi` 时写 `.pi/agent/APPEND_SYSTEM.md`（system prompt 尾部铁律摘要）+ 部署 `templates/graph-first-gate.ts` → `.pi/agent/extensions/`（三层 fallback 硬闸门 + 逐轮注入；pi 在 skill 层全量继承 .claude，此层为超集加固）。

三平台写入路径：Linux/macOS/WSL 用 `$HOME/...`；Windows 原生用 `$env:USERPROFILE\...`（详见 SKILL.md 与 environment.md 路径表）→ 备份后写入，已有产物按「分层增量」规则处理。

$ARGUMENTS

## 关联 Skill（网络调度协议）

| 用户意图关键词 | 路由目标 | 说明 |
|---------------|---------|------|
| 新机器 / 初始化主机 / host init / init machine / 一键配置开发环境 | → 本命令 | 宿主机级一键初始化 |
| `/ai-spec init` | ai-spec 转交本命令 | 主调度识别 init 参数 |

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | `/ai-spec init` 参数转交 |
| 输出供 | dev-env-scan | 宿主机画像作为项目画像基线 |
| 下游建议 | ai-spec | 初始化完成后进入需求主调度 |
