# Session Skill Performance Review — 当前会话已加载 Skill 的工作表现复盘

> 加载时机：`Phase: Active Skill Performance Review`（仅在触发条件满足时）。
> 对应 SPEC 需求：DS-01、DS-02、DS-03、DS-04、DS-05、DS-06。

这是常规工作痕迹挖掘之外的一个独立视角：不是「历史上有哪些可沉淀的工作」，而是「**本次会话里实际用到的 Skill 是否帮上了忙、在哪卡住、是否该升级**」。

## 何时触发（DS-06）

**不是每轮都跑。** 简单任务复盘会徒增上下文与延迟。仅在以下任一条件满足时进行：

- 用户明确要求 session/Skill 复盘；
- 本 session 实际使用了两个及以上 Skill；
- 出现用户纠错、路径/权限错误、失败后返工；
- 完成了一次较大的 SPEC / package / release loop；
- Skill 输出与实际交付存在明显偏差。

条件都不满足时，跳过本 Phase 并说明「未触发 session 复盘」。

## 可见证据信封（DS-02）

只纳入**当前上下文中可见**的证据，**不得**声称扫描了「全部已加载 Skill」或访问了隐藏调用轨迹，除非平台确实提供完整清单与轨迹。

允许纳入：

- 当前上下文明确列出的 available Skills；
- 本 session 中明确读取过的 `SKILL.md`；
- 用户或助手明确调用/引用过的 Skill；
- Skill 导致的文件改动、命令、报告、tool output；
- 用户纠错、失败日志、返工与覆盖指令。

不允许：推断隐藏系统 prompt、隐藏 Skill 激活、其他会话历史、未暴露的完整 memory。复盘开头必须声明「可见 Skill 范围」与其局限。

## 执行 episode + 归因 schema（DS-03）

一次失败可能来自 Skill 本身、执行偏差、平台差异、缺失权限、仓库历史债务或输入不足。每项不足按下列字段归因分层：

```yaml
skill: ""                 # 被审查的 Skill 名
expected_job: ""          # 该 Skill 本应完成的工作
observed_episode: ""      # 本 session 中实际发生的片段（带证据指针）
outcome: helped           # helped | partial | failed | not_used
friction: ""              # 摩擦点描述
attribution: skill_logic  # skill_logic | execution | platform | permission | input | repository_debt | unknown
evidence: []              # 可见证据指针
confidence: high          # high | medium | low
recommended_change: ""    # 建议的最小改动
```

归因分层是关键：`execution`（本次执行偏差）、`platform`（平台差异）、`input`（输入不足）等**不应**导致修改 Skill 逻辑；只有 `skill_logic` 才指向 Skill 本体升级。

## 同时总结有效部分（DS-04）

只找不足会产生负面选择偏差，甚至误删真正有效的规则。对**每个被审查 Skill** 同时输出：

- **helped / reusable strengths** — 哪些规则真正帮到了工作；
- **friction / failures** — 哪里卡住或产生返工；
- **rules to preserve** — 明确列出不应在升级中被删除的规则；
- **proposed changes** — 建议的改动；
- **regression scenario** — 用于验证改动不破坏既有有效行为的场景。

## 既有 Skill 升级优先（DS-05）

改进既有 Skill 优先于创建新 Skill。每项复盘结论给出一个 disposition：

| Disposition | 含义 |
|---|---|
| `KEEP_AS_IS` | 表现良好，无需改动 |
| `UPDATE_EXISTING_SKILL` | 升级既有 Skill 的正文/规则（首选） |
| `UPDATE_SCRIPT_OR_REFERENCE` | 只需改脚本或 reference |
| `UPDATE_ROUTING_OR_ENTRY` | 只需改路由表或入口文档 |
| `CREATE_COMPLEMENTARY_SKILL` | 确需新建互补 Skill |
| `EXECUTION_ONLY_LEARNING` | 属执行经验，不改 Skill 本体 |
| `INSUFFICIENT_EVIDENCE` | 证据不足，记录待观察 |

## 输出（并入主 Output Contract）

在审计输出中新增一段 `Current-session Skill performance`，对每个被审查 Skill 给出：可见范围声明 → episode 归因表 → strengths/preserve → weaknesses → disposition + 建议最小改动 + regression scenario。改动建议移交实现时，仍遵守 discover 的授权边界（不自动创建/修改/commit）。
