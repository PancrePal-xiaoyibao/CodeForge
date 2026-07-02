---
name: ralph-yolo
description: "YOLO模式 - 直接使用Claude Code子Agent实现PRD，不依赖Amp CLI。顺序执行每个用户故事，前台跟踪进度。"
---

# Ralph YOLO - Autonomous Agent Loop (No Amp Required)

## Overview

Ralph YOLO 是 Ralph 的轻量版本，直接使用 Claude Code 的 Task tool 管理子 agent 完成任务，无需依赖 Amp CLI。

## Workflow

1. 读取 PRD 文件（从 `tasks/prd-*.md`）
2. 解析用户故事列表
3. 对每个用户故事，创建子 agent 执行实现
4. 前台实时跟踪进度
5. 每个故事完成后运行验证

## Output Contract

- 所有用户故事实现完毕
- 每个故事通过基本验证
- 进度实时可见

## Resources

| File | Purpose | When |
|------|---------|------|
| tasks/prd-*.md | PRD input | Phase 1 |

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 可调用 | code-debugger | YOLO 执行中遇到错误 |
| 可调用 | nodejs-npm-auto-release | 全部故事完成后发布 |
| 被调用 | ai-spec | 主调度路由到自动开发(YOLO) |
| 被调用 | prd | PRD 完成后启动 YOLO |
| 被调用 | api-first | API 设计完成进入 YOLO 实现 |
