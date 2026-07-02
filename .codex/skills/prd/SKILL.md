---
name: prd
description: "Generate a Product Requirements Document (PRD) for a new feature. Use when planning a feature, starting a new project, or when asked to create a PRD."
---

# PRD Generator

## Overview

Create detailed Product Requirements Documents that are clear, actionable, and suitable for implementation with the Ralph autonomous agent system.

## Workflow

1. Receive a feature description from the user
2. Ask 3-5 essential clarifying questions (with lettered options)
3. Generate a structured PRD based on answers
4. Save to `tasks/prd-[feature-name].md`

## Output Contract

- A complete PRD markdown file saved to `tasks/`
- Structured sections: Overview, User Stories, Technical Requirements, Acceptance Criteria
- Do NOT start implementing — only produce the document

## Resources

| File | Purpose | When |
|------|---------|------|
| tasks/ | PRD output directory | Always |

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 可调用 | ralph / ralph-yolo | PRD 完成后进入自动实现 |
| 被调用 | ai-spec | 主调度分诊需要 PRD 文档 |
