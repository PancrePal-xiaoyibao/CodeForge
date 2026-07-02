---
name: dev-env-scan
description: 开发环境扫描与偏好配置 — 项目初始化时自动检测本地工具链、运行时、硬件能力，交互式收集开发者偏好，输出结构化 profile 供后续 skill 决策参考。
---

# Dev Env Scan

项目引导工程师角色。在新项目启动或首次协作时，快速建立对开发环境和开发者偏好的完整画像。

## Overview

- 自动检测 OS/Shell/语言运行时/包管理器/GPU/容器/IDE/VCS
- 交互式收集偏好（5-8 问）：主力语言、部署风格、测试哲学、CI 偏好等
- 双输出：`.dev-profile.json`（结构化）+ CLAUDE.md `## Developer Environment` 段落

## Workflow

1. **环境自动检测** — 执行跨平台命令序列，静默跳过不可用项
2. **偏好问卷** — 基于检测结果附推荐答案，用户可采纳或自定义
3. **输出生成** — JSON profile + CLAUDE.md 段落（替换或追加）
4. **增量更新** — 已有 profile 时只更新变化项

## Trigger

- 用户说"环境扫描"、"新项目"、"onboarding"、"dev scan"、"偏好设置"、"init project"

## Guardrails

- 能自动检测的绝不问用户
- 偏好无对错，只记录不评判
- 输出同时服务人类阅读和机器消费

## Output

- `.dev-profile.json` — JSON Schema: `dev-profile/v1`
- CLAUDE.md `## Developer Environment` 段落

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 新项目/onboarding 时主调度路由 |
| 输出供 | ai-spec | 技术栈决策参考 |
| 输出供 | code-debugger | 运行上下文预填 |
