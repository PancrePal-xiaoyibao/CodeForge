---
description: 宿主机一键初始化 — 环境探测+缺口提醒+codebase-mcp 部署提醒+注入文档生成（全局/项目可选）
---

把当前机器初始化为合格开发主机：探测软硬件环境（`scripts/host-scan.sh` 或 `host-scan.ps1`）→ 对照基线提醒安装缺失开发环境（git/rg/uv/conda/node/gh）→ 提醒部署 codebase-memory-mcp → 交互选择文档规范与生成位置（全局 `~/.claude/CLAUDE.md` + `~/AGENTS.md` / 项目 `./CLAUDE.md` + `./AGENTS.md`）→ 按 `templates/host-injection.template.md` 渲染三层注入文档（A 通用开发铁律 + B 本机探测填充 + C 留空占位）→ 备份后写入。

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
