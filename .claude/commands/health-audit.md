---
description: 变更前技术债基线 — build/test/lint 状态 + 债务登记表 + before/during/after 分类
---

对当前仓库执行证据驱动的项目健康审计：跑仓库自身检查命令 → 扫描 build/test/lint/依赖/安全/热点 → 每条发现附证据 → 分类 BEFORE/DURING/AFTER_CHANGE → 输出债务登记表与变更影响图。不执行修复。

$ARGUMENTS

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 本命令 | project-health-audit | 变更前技术债基线 — build/test/lint 状态 + 债务登记表 + before/during/after 分类 |
| 前置 | intent-grill / prd / ai-spec | 契约准备 |
