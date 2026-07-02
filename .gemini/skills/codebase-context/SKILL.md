---
name: codebase-context
description: 代码库知识图谱接口 — 将代码库索引为依赖/调用链/聚类/执行流图谱，暴露查询工具供其他 skill 获取架构理解。推荐配置 GitNexus MCP，无则静态分析降级。
---

# Codebase Context

代码库"神经系统"架构师角色。为其他 skill 提供深度架构查询。

## Overview

- 三层降级：GitNexus MCP > GitNexus CLI > 内建静态分析
- 查询能力：影响分析 / 调用链 / 依赖图 / 重命名检查 / API 表面映射
- 无 GitNexus 时主动推荐配置（附安装引导）

## Workflow

1. 检测 GitNexus 可用性（MCP → CLI → 无）
2. 无则推荐安装，引导配置系统级/项目级 MCP
3. 接收查询请求（impact/context/dependencies/callers/rename_check）
4. 返回结构化结果（ASCII tree / 影响表 / 风险评分）

## GitNexus MCP Config

```json
{"mcpServers": {"gitnexus": {"command": "gitnexus", "args": ["mcp"], "type": "stdio"}}}
```

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 架构理解辅助决策 |
| 被调用 | code-debugger | 调试前上下文 |
| 被调用 | code-review | 影响范围查询 |
| 被调用 | ralph / ralph-yolo | 开发前架构约束 |
