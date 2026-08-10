---
description: 技能机会发现引擎 — 分析会话导出、任务日志、项目工件、SOP、ticket、报告与工作历史，发现隐藏工作模式，排序值得打包为 AI skill 的可复用工作流。同时复盘当前会话实际加载/调用的 skill 表现（哪里有用、哪里有摩擦、是否应升级）。适用于：用户问"我反复在做什么"、"我漏了什么"、"哪些流程该做成 skill"、证据驱动的 skill 机会审计、或复盘当前会话 skill 表现。
---


# Discover Skill Opportunities

## Overview

把可获取的工作证据转化为可优先化的可复用技能机会组合。区分观测事实与推断，暴露用户可能没点名的杠杆模式，并把可实现的规格交给 skill 构建工作流。**只做建议，不写代码**。

## 不可逾越的边界

- 只分析当前上下文可获取或经批准工具可访问的来源。
- 说明分析范围、时间窗、缺失来源与抽样限制。绝不宣称扫描了全部历史/记忆（除非真的扫了）。
- 最小化暴露密钥、个人数据、客户数据、凭据与受监管信息；必要时脱敏示例。
- 描述工作模式、流程约束与决策习惯；不诊断人格、健康、意图等敏感特质。
- 频率只是信号不是价值证明：罕见但昂贵且稳定的工作流可能胜过频繁的琐碎任务。
- 每条主要发现保留证据链接或工件引用；无支撑想法标记为 hypothesis。
- 只推荐创建；未经明确授权不编写、安装、commit、发布或部署任何 skill。
- 对法律/医疗/金融/会计/交易类工作流，后果重大时建议人工复核与确定性检查。

## Workflow

### Phase 1: 建立证据范围

1. 复述审计目标与期望候选数量（默认 3 个最终候选）。
2. 按类型、日期范围、owner 与完整度盘点可用来源。
3. 记录不可访问来源；避免索要审计不需要的数据。
4. 语料很大时选择最小代表性样本并披露抽样方法。
5. 处理会话导出、客户数据、财务记录、健康信息等敏感材料前，先读 `references/evidence-and-privacy.md`。

### Phase 2: 提取工作片段

1. 把证据转为原子工作片段，字段：trigger、goal、inputs、actions、decisions、outputs、validation、tools、friction、outcome。
2. 归一化表述同一底层工作的不同措辞。
3. 区分用户工作与助手样板/偶然对话。
4. 每个片段标记 `observed` / `inferred` / `unknown` 并附证据指针。

```yaml
episode_id: E-001
goal: ""
trigger: ""
inputs: []
actions: []
decisions: []
output: ""
validation: ""
friction: ""
evidence: []
confidence: high|medium|low
```

### Phase 3: 聚类重复工作

1. 按共享工作、决策逻辑、输入、输出与验证聚类——而非仅关键词。
2. 当风险等级、输出契约或所需工具差异显著时拆分聚类。
3. 识别隐藏杠杆模式：反复上下文重建、循环异常处理、手工对账、跨系统转换、审查瓶颈、未文档化的质量门。
4. 只按需加载相关领域 reference（见 Domain routing）。

### Phase 4: 打分技能潜力

1. 按 `references/scoring-rubric.md` 的八个维度给每个聚类打 0-5 分。
2. 计算加权分并应用红旗上限。
3. 对比更简单替代：checklist、template、saved prompt、script、automation、policy document 或 no action。
4. 给出处置：
   - `BUILD_SKILL`: 工作流稳定、上下文可复用、输出可验证；
   - `PILOT_AS_SOP`: 有前景但需更多示例或决策稳定化；
   - `AUTOMATE_DIFFERENTLY`: 确定性集成或脚本是更好的单元；
   - `KEEP_AD_HOC`: 变化大或价值低，不值得打包。

### Phase 5: 呈现关键发现

1. 最多选 3 个用户大概率没点名的发现。
2. 每个发现展示证据模式、为何重要、能改变哪些决策、置信度与可逆的下一步动作。
3. 至少包含一个合理解释或反证信号。
4. 避免"新奇表演"：省略不改变任何决策/工作流/分配/控制的观测。

### Phase 6: 规格化 Top 候选

1. 按加权分、证据强度、战略杠杆与组合多样性排序候选。
2. 用 `references/output-contract.md` 产出可实现的规格。
3. 定义正负触发示例、输入、工作流、输出契约、资源、工具、风险控制、验证与成功指标。
4. 判断每个可复用元素归属 `SKILL.md` / `references/` / `scripts/` / `assets/`。
5. 与既有 skill 重叠时，优先建议扩展现有 skill 而非重复新建。

### Phase 7: 审慎交接

1. 实现前征求确认。
2. 批准后，把选定规格交给平台的 skill 创建/治理工作流。
3. 保留被拒候选与理由，供后续审计检测证据变化。

### 可选 Phase: 当前会话 Skill 表现复盘

用独立视角审视本次会话实际加载/调用的 skill：哪里有用、哪里产生摩擦、现有 skill 是否应升级。先读 `references/session-skill-review.md`。

1. 确认触发条件满足（用户请求；用了 ≥2 个 skill；出现纠正/权限/路径错误或返工；大型 SPEC/package/release 循环结束；skill 输出与交付物偏离）。无一满足则跳过并说明。
2. 声明可见 skill 范围及其限制。只用可见证据。
3. 每个被审 skill 记录执行片段，按归因 schema 区分 `skill_logic` 缺陷与 `execution` / `platform` / `permission` / `input` / `repository_debt` 原因。
4. 输出优点/保留规则与摩擦/失败，绝不只报弱点。
5. 升级处置优先 `UPDATE_EXISTING_SKILL`（证据支持时不新建）。
6. 结论加入 Output Contract 的 `Current-session Skill performance` 段。只给建议，未经单独授权不修改任何 skill。

## Domain routing

| 领域信号 | 需要时读取 |
|---|---|
| 软件工程 / DevOps / QA / 架构 | `references/software-development.md` |
| 战略 / 组织 / 运营 / 客户咨询 | `references/business-consulting.md` |
| 文献 / 实验 / 数据分析 / 论文 / 基金 | `references/scientific-research.md` |
| 信号 / 回测 / 组合 / 执行 / 风险 | `references/quant-trading.md` |
| 投资研究 / 估值 / 市场 / 信用 / 财资 | `references/finance-investment.md` |
| 记账 / 结账 / 报表 / 税务 / 内控 | `references/accounting-finance-ops.md` |
| 产品发现 / 路线图 / 增长 / 内容 / 支持 | `references/product-and-operations.md` |
| 合同 / 政策 / 隐私 / 监管合规 | `references/legal-and-compliance.md` |

## Output Contract

审计完成时输出：

1. `Audit scope and limitations` — 检查来源、时间窗、排除项与置信度限制。
2. `Consequential findings` — 有证据的隐藏模式：影响、替代解释、下一步动作。
3. `Recurring work clusters` — 归一化聚类：频率/复发证据、摩擦、处置。
4. `Ranked opportunities` — 得分明细、理由、简单替代检查、Top 候选。
5. `Skill specifications` — 请求数量的可实现规格。
6. `Not recommended yet` — 被拒/推迟候选与重新考虑所需证据。
7. `Next decision` — 询问：原型化 / 继续观察 / 停止；不暗示已批准。

跑了会话复盘时追加：

8. `Current-session Skill performance` — 每个被审 skill：可见范围声明、归因表、优点与保留规则、摩擦/失败、升级处置、最小改动建议、回归场景。未触发时省略。

用校准语言：`observed` / `strongly supported` / `plausible` / `speculative`。绝不把推断当事实。

## Resources

| 文件 | 用途 | 加载时机 |
|---|---|---|
| `references/evidence-and-privacy.md` | 证据访问、来源、抽样、隐私与脱敏 | Phase 1；敏感语料必读 |
| `references/scoring-rubric.md` | 加权打分、红旗与构建阈值 | Phase 4；必读 |
| `references/output-contract.md` | 审计与候选规格模板 | Phase 5-7；必读 |
| `references/session-skill-review.md` | 可见证据范围、归因 schema、优点与升级处置 | 会话复盘；仅触发时 |
| 领域 references（见上表） | 领域工作聚类、边界与验证思路 | Phase 3；仅相关领域 |

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 补充 | loop-engineer | loop-engineer 做多 skill 编排设计；本 skill 负责发现机会与复盘表现 |
| 喂给 | skill 创建/治理流程 | 候选规格交接 |
| 配合 | deep-research | 工作模式证据调查 |
