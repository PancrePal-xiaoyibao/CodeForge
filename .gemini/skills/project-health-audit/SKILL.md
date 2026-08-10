---
name: project-health-audit
description: 证据驱动的项目健康与技术债基线扫描 — 在 PRD / SPEC / 重构 / 迁移 / 大型功能开发之前使用。检查 build/test/lint 状态、架构热点、依赖与安全风险、mock/stub/TODO、文档漂移、迁移与近期变更热点，并把债务分类为 BEFORE_CHANGE / DURING_CHANGE / AFTER_CHANGE。不执行未被单独授权的修复。
---

# Project Health Audit

## Overview

确定既有系统条件是否会阻塞、约束或应伴随目标变更一起处理。产出可复现的基线，而非泛泛的代码质量意见。

## Workflow

1. 读取仓库规则、变更意图、架构/上下文工件、Git 状态、CI 配置、清单、测试、迁移与近期历史。
2. 发现仓库自己的检查命令；按审计范围运行安全的只读或常规校验检查。
3. 检查 build/test/lint/type 状态、flaky/skipped 测试、依赖/安全信号、模块耦合、变更热点、TODO/FIXME/stub/mock、迁移、配置漂移、可观测性与文档漂移。
4. 为每条发现项附上 file/command/commit/report/log 证据。区分观测失败与推断风险。
5. 对严重度、可能性、变更相关性、修复成本与置信度打分。
6. 将修复时机分类为 `BEFORE_CHANGE` / `DURING_CHANGE` / `AFTER_CHANGE` / `ACCEPTED`。
7. 当项目有变更工作区时，写 `tasks/<change-id>/HEALTH.md` 与结构化债务登记表。

## Debt schema

```yaml
debt_id: TD-001
title: ""
severity: critical|high|medium|low
evidence: []
affected_modules: []
blocks_change: false
timing: BEFORE_CHANGE|DURING_CHANGE|AFTER_CHANGE|ACCEPTED
remediation: ""
owner: ""
confidence: high|medium|low
status: open
```

## Guardrails

- 不把旧代码等同于债务；要求影响与证据。
- 审计期间不运行破坏性迁移、升级、部署或大规模 autofix。
- 不隐藏失败的检查；区分环境失败与产品失败。
- 避免通用阈值；优先仓库策略与变更相关风险。
- 把实现发现项路由到已批准的 goal/SPEC，而不是静默扩大范围。

## Output Contract

产出：

1. 审计范围、环境、命令与限制；
2. build/test/lint/type/security/docs/migrations 基线状态；
3. 带证据与置信度的优先级债务登记表；
4. 变更影响图与阻塞性债务；
5. before/during/after 修复建议；
6. 输入到 PRD/SPEC 的内容与显式非发现项。

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 使用 | codebase-context | 架构与影响证据 |
| 喂给 | intent-grill / prd / ai-spec | 变更约束与债务决策 |
| 喂给 | goal-driven-development | 必要前置条件与债务控制 |
| 接收 | iteration-manager | 已交付工作的推迟发现项 |
