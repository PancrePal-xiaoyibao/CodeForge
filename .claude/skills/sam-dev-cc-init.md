---
description: PDCO 循环开发工作流初始化工具。当用户输入 sam-init、pdco、init-pdco 或需要建立项目开发规范时使用。为 AI 辅助编程项目快速建立 CLAUDE.md、PROGRESS-LOG.md、任务管理、经验沉淀机制和智能评估系统。适合任何需要系统化开发流程、质量管理和激励机制的项目。
---


# Sam Dev CC Init — PDCO 开发工作流初始化

为任何新项目快速建立完整的 AI 辅助开发规范。

## 核心哲学

```
Context Window = RAM (易失，有限)
Filesystem = Disk (持久，无限)

→ 重要信息必须写入文件！
```

## 触发条件

用户输入以下任一内容时激活：
- `sam-init` / `pdco` / `init-pdco` / `pdca` / `init-pdca`
- `初始化pdco` / `建立开发规范` / `pdco workflow`

## 初始化操作指令

### Step 1: 确认信息
1. 确认当前工作目录
2. 获取项目名称：从目录名或询问用户
3. 获取当前日期：`date +%Y-%m-%d`

### Step 2: 检查现有文件
检查以下文件是否已存在：
- `CLAUDE.md`
- `PROGRESS-LOG.md`
- `tasks/TASKS.md`
- `self.opt`

如果存在，提示用户并询问是否覆盖或跳过。

### Step 3: 生成文件（自包含模板，无需外部资源）

目标文件结构：
```
project-root/
├── CLAUDE.md           # AI上下文指南（含PDCO流程、5问重启、最佳实践）
├── PROGRESS-LOG.md     # 进度日志（倒序追加）
├── self.opt            # 经验沉淀（错误模式、最佳实践）
└── tasks/
    └── TASKS.md        # 任务管理（当前Sprint、待办池、已完成）
```

每个文件按下方「模板内容参考」生成，替换变量：
- `{{PROJECT_NAME}}` → 实际项目名称
- `{{DATE}}` → 当前日期（YYYY-MM-DD）

### Step 4: 输出结果
显示创建的文件清单（创建/跳过）、文件说明、下一步建议、常用命令提示。


## PDCO 开发循环（CHECKFIX 零错误部署）

```
┌──────────────────────────────────────────────────────────────────┐
│          PDCO 开发循环（CHECKFIX 零错误部署）                    │
├──────────────────────────────────────────────────────────────────┤
│  1. PLAN   → 读取 tasks/TASKS.md，查看并领取任务                │
│  2. DO     → 代码修改 + 执行 CHECKFIX 检查清单（必须）          │
│  3. CHECK  → 验证 CHECKFIX 全部通过 + 测试/集成验证             │
│  4. OPT    → 更新 PROGRESS-LOG.md + 更新任务 + self.opt 沉淀    │
│                                                                  │
│  🔴 核心原则：所有代码修改必须 CHECKFIX 零错误提交/部署         │
│     (跳过 CHECKFIX 代价：500-1000+ tokens 修复成本)             │
│                                                                  │
│  🧹 CHECK/测试 前后必须遵守测试产物卫生铁律                      │
│     (T0 测试前检查 / T1 测试后清扫 / T2 区分测试产物vs运行数据 │
│      / T3 代码层老鼠屎清扫，详见 code-debugger T0-T3)           │
└──────────────────────────────────────────────────────────────────┘
```

### 文件对应关系

| 阶段 | 文件 | 用途 | 更新方式 |
|------|------|------|----------|
| PLAN | `tasks/TASKS.md` | 任务列表与状态管理 | 手动编辑 |
| DO | 代码目录 | 实现 + **CHECKFIX 检查** | 编码 |
| CHECK | `.checkfix/` + 测试 | **验证 CHECKFIX** + 测试 | 命令 |
| OPT | `PROGRESS-LOG.md` + `self.opt` | 进度日志 + 经验沉淀 | 手动编辑 |


## 会话恢复（5-Question Reboot Test）

在长时间会话后、上下文重置后或新的一天开始时执行：

| 问题 | 答案来源 |
|------|----------|
| Where am I? | 当前阶段在 `tasks/TASKS.md` |
| Where am I going? | 剩余任务列表 |
| What's the goal? | `tasks/TASKS.md` 中的项目目标 |
| What have I learned? | `self.opt` 中的经验沉淀 |
| What have I done? | `PROGRESS-LOG.md` 中的记录 |


## 开发循环（PDCO）

**PLAN**
1. 读取 `tasks/TASKS.md`，选择优先级最高的 TODO 任务，更新为 `IN_PROGRESS`

**DO**
1. 实现代码（遵循 2-Action Rule）
2. 编写/运行单元测试
3. 遇到错误 → 记录到 `self.opt`

**CHECK**
1. 运行测试验证（如 `pytest`）
2. 端到端验证（如 API 测试）
3. 代码质量检查（可选）

**ACT**
1. 在 `PROGRESS-LOG.md` **顶部（倒序）**追加今日完成
2. 更新 `tasks/TASKS.md` 任务状态为 `DONE`，填写实际耗时

**OPT（Agent 自优化）**
1. **判断偏差值不值得永久记录？**
   - ❌ 一般性错误（语法、拼写）→ 不记录
   - ⚠️ 一次性领域错误 → 记录在 PROGRESS-LOG.md 即可
   - ✅ 关键偏差（>3次尝试/反直觉/会再犯）→ 记录到 `self.opt`
2. **提取关键偏差模式（CDP）**：偏差描述 → 根因 → 解决策略 → 预防触发器
3. **提炼核心解决策略（CRS）**：是否跨项目可复用？是否是方法论而非具体命令？

**→ 返回 PLAN，领取下一个任务（带着进化后的认知）**


## 关键规则

1. **倒序追加原则**：`PROGRESS-LOG.md` 永远在最上面写新内容。
2. **2-Action Rule**：每进行 2 个 view/browser/search 操作后，立即将关键发现写入文本文件。
3. **Read Before Decide**：做重大决策前，重新阅读 `tasks/TASKS.md` 和 `PROGRESS-LOG.md`。
4. **Agent 自优化原则**：只记录花 >3 次尝试才解决的、解决策略反直觉或跨领域迁移的、大概率会再犯的、导致显著时间浪费（>20分钟）的认知偏差。
5. **Never Repeat Failures**：`if action_failed: next_action != same_action`

## 3-Strike Error Protocol

```
ATTEMPT 1: 诊断与修复 → 仔细阅读错误 → 识别根因 → 针对性修复
ATTEMPT 2: 替代方法 → 同样错误？换方法/换工具/换库 → 绝不重复相同失败操作
ATTEMPT 3: 重新思考 → 质疑假设 → 搜索解决方案 → 考虑更新计划
AFTER 3 FAILURES: 升级给用户 → 解释尝试过的方法 → 分享具体错误 → 请求指导
```


## 模板内容参考

### CLAUDE.md 包含
- 快速开始与常用命令
- PDCO 循环流程图
- 文件对应关系表
- 5-Question Reboot Test
- 开发循环详细流程
- 关键规则（倒序追加、2-Action Rule 等）
- 3-Strike Error Protocol
- Read vs Write 决策矩阵

### PROGRESS-LOG.md 包含
- 用途说明（倒序追加）
- 记录规范
- 错误记录格式
- 测试记录格式
- 初始条目：项目初始化

### tasks/TASKS.md 包含
- 项目目标
- 当前 Sprint 表格
- 待办池
- 已完成归档
- 关键决策表
- 错误日志
- 风险与阻塞

### self.opt 包含（Agent 自优化日志）
- 项目信息 + 快速命令备忘
- 关键偏差模式（CDP）：偏差→根因→解决策略→预防触发器
- 核心解决策略库（CRS）：可复用的方法论级策略
- 认知盲区档案（CBS）：AI 容易「看不见」的场景
- 效率法则（Laws）：经过验证的效率提升法则
- 假设验证记录：做过的假设及其验证结果
- 记录决策树：帮助 AI 判断「什么值得记录」


## Token 动态预算管理

| 预算等级 | 说明 |
|---|---|
| 🔴 严格 (3k) | 返工多、质量差 |
| 🟡 标准 (8k) | 默认起始级别 |
| 🟢 宽松 (15k) | 连续 3 次高质量 |
| 🔵 信任 (∞) | 连续 5 次高质量（需汇报数据） |

**自动调整规则**：3×A 级 → 升级；1×C/D 级 → 降级并进入冷静期 3 次；周度复盘更新 self.opt 效率趋势。

## 奖惩机制

**奖励**：CHECKFIX 一次通过 +10 · 零缺陷交付 +15 · self.opt 经验分享 +3/条 · Token 预估精准 +5
**惩罚**：跳过 CHECKFIX -50 · 生产 bug -30/个 · 不记录经验 -10 · Token 预估严重偏离 -10
**兑现**：101+ 分 → 快速通道/任务优先；<50 分 → 强制质量培训/二级审查


## 更新机制

- 已有项目不受影响（保持独立）
- 新项目自动使用最新模板
- 如需同步更新旧项目：手动复制模板内容

## 最佳实践提示

1. **倒序追加**：PROGRESS-LOG.md 永远在最上面写新内容
2. **原子提交**：一个任务一个 commit，便于回滚
3. **及时记录**：踩坑后立即写 self.opt，不要等
4. **简洁原则**：日志只写要点，不写流水账
5. **AI友好**：CLAUDE.md 是给 AI 看的，写清楚上下文
6. **定期恢复**：使用 5-Question Reboot Test 恢复上下文

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 前置 | dev-env-scan | 扫描技术栈后初始化 PDCO 规范 |
| 配合 | ai-spec | Repo Init 补齐入口文档 |
| 配合 | code-review | 质量门（对应 CHECKFIX） |
