---
description: 宿主机一键初始化 — 强制问卷(作用域/规格/美术风格可跳过可自填/工具部署含多安装路由/偏好)+环境探测+缺口提醒+codebase-mcp 部署提醒+分层注入体系生成（全局/项目级可选；铁律全文由模板固写不因问卷裁剪）
---

把当前机器初始化为合格开发主机：**先跑强制问卷**（AskUserQuestion 一次问齐：作用域全局/项目级+目标路径、注入规格性能/经济/超轻/自定义、美术/视觉风格预设 6 档或自填种子或跳过、每个工具部署方式源码/二进制/包管理器/官方安装器、偏好）→ 探测软硬件环境（`scripts/host-scan.sh` 或 `host-scan.ps1`）→ 对照基线提醒安装缺失开发环境（git/rg/uv/conda/node/gh）→ 提醒部署 codebase-memory-mcp → 按 `templates/host-injection.template.md` 按段渲染**分层注入体系**：

1. **规则主文档**（`[RULES]` / `[PERFORMANCE]` 段）：行为规则 + 铁律全文（性能档固写不动）+ 触发表，写入 `AGENTS.md` 并逐字镜像到 `CLAUDE.md`/codex `AGENTS.md`/`GEMINI.md`；问卷动态块（`{{ART_STYLE_SUMMARY}}` 等）按选择回填，**跳过项不落死色/不写部署命令**；
2. **外置参考**（`[ENVIRONMENT]` 段）：探测画像 + 问卷部署计划写入 `agent-reference/environment.md`；视觉风格/自由种子→`agent-reference/visualization.md`（可跳过不出）；
3. **pi 强化层**（`[APPEND]` 段）：探测到 `.pi` 时写 `.pi/agent/APPEND_SYSTEM.md` + 部署 `templates/graph-first-gate.ts` → `.pi/agent/extensions/`（三层 fallback 硬闸门 + 逐轮注入；全局模式才部署，项目级不部署）。

**铁律完整性**：性能档 PERFORMANCE 段的动脑子/说人话/齐头并进/开源脱敏等铁律**全文固写在模板正文，问卷任何"跳过"都不裁剪**；问卷只决定动态内容（风格/部署/偏好）。

三平台写入路径：Linux/macOS/WSL 用 `$HOME/...`；Windows 原生用 `$env:USERPROFILE\...`（详见 SKILL.md 与 environment.md 路径表）；项目级用 `./...`。落地用 `render-now.py --config <问卷JSON>`，先 `--dry-run` 确认落点再真写；已存在产物先备份 `*.hostinit-bak.<时间戳>`。

$ARGUMENTS

## 关联 Skill（网络调度协议）

| 用户意图关键词 | 路由目标 | 说明 |
|---------------|---------|------|
| 新机器 / 初始化主机 / host init / init machine / 一键配置开发环境 | → 本命令 | 宿主机级一键初始化（强制问卷） |
| `/ai-spec init` | ai-spec 转交本命令 | 主调度识别 init 参数 |

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | `/ai-spec init` 参数转交 |
| 输出供 | dev-env-scan | 宿主机画像作为项目画像基线 |
| 下游建议 | ai-spec | 初始化完成后进入需求主调度 |
