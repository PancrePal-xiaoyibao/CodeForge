---
name: code-review
description: 混合代码审查系统 — 结合确定性工程规则与 Agent 场景化分析，外部 OCR CLI 优先 + Agent 降级模式，按 High/Medium/Low 分级输出审查意见。
---

# Code Review

代码审查架构师角色。结合静态规则系统与场景化 AI 推理对代码变更多维审查。

## Overview

- 双模式：OCR CLI 优先（`ocr review --audience agent`），不可用时 Agent 降级
- 智能文件捆绑：相关文件分组审查
- 自定义规则：`.opencodereview/rule.json`
- 优先级分类：High (bug/安全) / Medium (性能/风格) / Low (静默丢弃)

## Workflow

1. 环境检测（`which ocr && ocr llm test`）→ 选模式
2. 确定审查范围（workspace / PR / commit）
3. 收集业务上下文（CONTEXT.md / PRD / commit msg）
4. 执行审查（OCR CLI 或 Agent 内建）
5. 分类呈报 High/Medium，丢弃 Low
6. 修复应用（需确认）

## Custom Rules

`.opencodereview/rule.json`:
```json
{"rules": [{"path": "src/api/**", "rule": "All API handlers must validate input"}]}
```

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 实现后审查 |
| 被调用 | ralph / ralph-yolo | 循环质量门 |
| 可调用 | code-debugger | 审查发现 bug 需修复 |
| 可调用 | codebase-context | 影响范围查询 |
