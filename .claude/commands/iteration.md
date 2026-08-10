---
description: 交付后迭代管理 — 残差分类 BUG/DEBT/PRD_AMENDMENT/SPEC_AMENDMENT/NEW_CHANGE + 下一 Gate
---

分析刚结束的交付：比较预期 vs 观测结果 → 分类每条残差（BUG/DEBT/PRD_AMENDMENT/SPEC_AMENDMENT/NEW_CHANGE/NO_ACTION）→ 保留已批准历史 → 输出下一变更 ID、优先级、下一 Gate 与路由。

$ARGUMENTS

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 本命令 | iteration-manager | 交付后迭代管理 — 残差分类 BUG/DEBT/PRD_AMENDMENT/SPEC_AMENDMENT/NEW_CHANGE + 下一 Gate |
| 前置 | intent-grill / prd / ai-spec | 契约准备 |
