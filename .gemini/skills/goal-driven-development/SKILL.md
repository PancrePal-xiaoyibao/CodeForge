---
name: goal-driven-development
description: 批准后 SPEC 的证据化执行引擎 — 将已批准的工程 SPEC 转化为持久的、带证据的目标循环，逐里程碑实现、跑确定性检查、执行 spec-aware 审查，并在独立的 commit / push 授权门处停止。在 intent / 项目健康 / PRD / SPEC 批准后使用；不适用于模糊需求、未批准 spec、一次性解释、或未经明确授权的自动 commit/push。
---

# Goal-Driven Development

## Overview

在 `SPEC_APPROVED` 后担任默认编码执行器。一次推进一个可验证的里程碑，持久化状态与证据，把实现、审查、commit、push、结果反馈视为显式状态转移，防止"口头完成"。

## Input Contract

要求或解析以下输入：

- 仓库入口文档与当前 Git 状态；
- `CHANGE.md`、已批准 `PRD.md`、已批准 `SPEC.md`、`TRACEABILITY.md`；
- 修改既有系统时的项目健康/技术债基线（见 project-health-audit）；
- 验收标准、确定性检查命令、里程碑依赖、审批边界。

若关键输入缺失，在改动代码前停下，路由到 `intent-grill` / `project-health-audit` / `prd` / `ai-spec`。

## Goal 适配器

1. 若运行时存在原生 goal API，使用它：从已批准 SPEC 设定具体目标，保留平台完成/阻塞语义。
2. 否则创建或更新 `tasks/<change-id>/goal-state.yaml`，字段包含目标、里程碑、当前状态、证据、阻塞、授权。
3. 当 API 不可用时，绝不谎称调用了 `/goal` / `create_goal` 或等效接口。
4. 不因上下文/时间/预算紧张而关闭 goal；仅在验收达成时关闭，仅在运行时真实阻塞规则下标记 blocked。

最小适配器 schema：

```yaml
change_id: CHG-000
spec_version: 1
state: GOAL_ACTIVE
objective: ""
milestones: []
current_milestone: ""
evidence: []
blockers: []
authorization:
  commit: false
  push: false
```

## Workflow

### Phase 1: 初始化或恢复

1. 读取仓库入口文档、变更工件、goal 状态、Git 状态与既有证据。
2. 拒绝过期或被取代的 SPEC 版本。
3. 将 SPEC 转为依赖排序的里程碑，每个里程碑足够小，可在一轮 实现/检查/审查 内完成。
4. 将每条验收标准映射到至少一个里程碑与验证方法。
5. 仅当依赖关系与工作树归属已理解时，才进入 `GOAL_ACTIVE`。

### Phase 2: 执行一个里程碑

1. 选择依赖已满足的最高优先级未完成里程碑。
2. 编辑前声明目标文件、验收标准、检查项、风险与回滚方案。
3. 实现最小一致变更；保留用户无关工作。
4. 按变更类型运行仓库原生的 lint / type / unit / integration / build / security 或手工检查。
5. 在 `evidence/` 下记录简洁命令、退出码与工件指针；绝不只用叙述宣称成功。

**🧹 测试产物卫生铁律（每次测试/Checkfix 前后必须执行）** — 测试是开发闭环里最容易"拉屎"的环节。任何测试/验证/Checkfix 前后必须执行 T0–T3：

- **T0 · 测试前检查** — 跑测试前，先扫工作区是否有**上轮测试遗留**：未被 .gitignore 覆盖的 test artifact、跑测生成的临时 db/缓存/截图/导出、fixture 残留、`__pycache__`。发现即通报用户清单后再启动本轮测试，避免新旧残留混淆。**只扫测试产物类遗留，绝不碰别人的在途代码改动**。
- **T1 · 测试后清扫** — 测试结束后检查本轮"拉屎"：测试运行残留、临时输出、调试快照、未被 .gitignore 覆盖的生成物。通报清单后清理。
- **T2 · 严格区分三类，误删运行数据 = 事故**

  | 类别 | 判定 | 处置 |
  |------|------|------|
  | **测试产物** | 测试框架临时输出、fixture 残留、跑测临时 db/缓存/截图/mock 数据、`__pycache__`、被 .gitignore 覆盖的生成物 | 通报后**自动删** |
  | **运行数据** | 项目实际运行产生的 DB 记录、日志、用户上传、缓存里的真实数据、生产/热开发正在用的状态 | **绝不删**，哪怕看起来像临时文件 |
  | **模糊/无法确认** | 既不像明确测试产物，也无法确认是运行数据；或属于别人在途改动 | **逐项问用户**，不擅自处置 |

- **T3 · 代码层老鼠屎清扫** — 测试通过后，清理代码层残留：`print`/`console.log`/调试输出、`debugger`/breakpoint 语句、注释掉的测试代码块、临时 TODO/FIXME、硬编码测试数据/魔法数字、未清理的 mock 注入、被注释掉的旧实现。这些"老鼠屎"在热开发与生产 debug 时会误导排查，必须随测试闭环一并清掉。
- **删除安全网**：批量删除用 `/bin/rm -f` 或 `command rm -f`（绕 `rm -i` 别名）；删除前通报清单与分类；运行数据一律不动；模糊项问；删除范围仅限本轮自己产生的测试产物，不卷入他人改动。

### Phase 3: 合规强制与审查

1. 进入 `CHECKING`，将 diff 对照 SPEC、可追溯性、验收标准、项目规则与债务约束。
2. 进入 `REVIEWING`，调用或遵循 `code-review`。
3. 若 `FAIL`，进入 `FIX_REQUIRED`，在范围内修复并重跑检查与审查。
4. 若 `PASS_WITH_DEBT`，将已接受发现项记录进债务登记表，附 owner/reason/follow-up。
5. 仅当存在确定性证据与审查结论时，才标记里程碑完成。

### Phase 4: 交付门

1. 全部里程碑通过后，更新 `TRACEABILITY.md`、`goal-state.yaml`、计划文档与可复用的仓库经验。
2. 进入 `COMMIT_READY`，报告确切 diff 与证据。
3. 仅在 commit 授权显式时 commit；随后进入 `COMMITTED` 并记录 commit hash。
4. 仅在 push 授权单独显式时 push；随后进入 `PUSHED` 并记录 remote/ref。
5. 编辑/测试/运行 goal/commit 的授权不视为 push 授权。

### Phase 5: 结果与延续

1. 将已交付、已停止或部分验收的工作路由到 `iteration-manager`。
2. 将残差分类为 bug / debt / PRD amendment / SPEC amendment / new change。
3. 仅对同一已批准 SPEC 下范围内未完成里程碑继续既有 goal；否则新建 change/version。
4. 仅当验收、可追溯性、审查与所需交付状态全部满足时完成。

## 完成规则

绝不把模型输出的 `COMPLETE` 字符串当证据。完成必须满足：

- 所有必需里程碑完成；
- 所有验收标准映射到通过的证据；
- 审查结论 `PASS` 或已批准 `PASS_WITH_DEBT`；
- 无 Critical/High 发现项；
- 可追溯性与 goal 状态已更新；
- Git/交付状态准确报告；
- 结果审查已执行或显式推迟。

## Output Contract

每轮报告：

1. change/spec 与当前状态；
2. 推进的里程碑与受影响文件；
3. 检查与证据；
4. 审查结论/发现项；
5. 阻塞或债务；
6. 下一状态转移与所需授权。

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 前置 | intent-grill / project-health-audit / prd / ai-spec | 准备已批准的变更契约 |
| 调用 | codebase-context / code-debugger / code-review | 上下文、修复与质量门 |
| 回转 | iteration-manager | 结果与下一轮路由 |
| 兼容替代 | ralph / ralph-yolo | 仅兼容；非默认执行器 |
