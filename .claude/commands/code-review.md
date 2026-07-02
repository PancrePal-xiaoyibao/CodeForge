---
description: 混合代码审查 — OCR CLI 优先 + Agent 降级，按 High/Medium/Low 分级输出
---

对当前代码变更执行混合审查：优先使用 OCR CLI（如已安装），否则 Agent 内建审查。按 High/Medium/Low 分级输出审查意见并提供修复建议。

$ARGUMENTS

## 关联 Skill（网络调度协议）

| 用户意图关键词 | 路由目标 | 说明 |
|---------------|---------|------|
| 代码审查 / code review / review PR / 变更审查 | → 本命令 | 混合代码审查 |

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 实现后审查 |
| 被调用 | ralph | 循环质量门 |
| 可调用 | code-debugger | bug 修复 |
| 可调用 | codebase-context | 影响范围查询 |
