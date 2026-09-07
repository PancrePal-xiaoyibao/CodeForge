# CLAUDE.md — CodeForge Full-Stack AI Dev Engine (Claude Code)

CodeForge is a community-driven **full-stack AI development engine**. This repository ships a pre-installed skill suite that turns a blank Claude Code environment into a **requirement → spec → API-First implementation → debug → UX → CI/CD → release** cockpit.

Every skill lives in `.claude/`, `.codex/`, and `.gemini/` mirrors so **any** of the three AI coding platforms can drive the workflow.

---

## 🎯 主调度入口

| 命令 | 何时使用 |
|------|---------|
| `/ai-spec` | **默认主调度**。任何新需求先走这里，自动分诊到规范/调试/UI/研究等分支 |
| `/deep-research` | 需要外部信息（技术选型、文献、竞品、SDK 变化）时的深度调研引擎 |
| `/dev-env-scan` | 首次进入项目 / 新机器 onboarding — 输出环境画像 + 偏好档案 |

**Repo Init 规约**：`/ai-spec` 首次运行必须读取 / 补齐 `AGENTS.md` `CLAUDE.md` `GEMINI.md`，提取项目哲学、环境、测试命令、开发者偏好、编码约定、计划文档、审批边界。

---

## 🗺️ 技能网络路由

| 场景 | 推荐路径 | 结果 |
|------|----------|------|
| 新机器 / 宿主机 onboarding | `/dev-host-init` → `/dev-env-scan` → `/ai-spec` | 一键初始化 + 分层注入体系 + 环境画像 |
| 新仓库 / 首次运行 Agent | `/dev-env-scan` → `/ai-spec` | 环境画像 + 项目工作流 |
| 需求模糊 | `/intent-grill` → `/ai-spec` | 对齐后的技术规范 |
| 需要外部信息 / 技术选型 / 文献调研 | `/deep-research` → `/ai-spec` | 结构化调研报告 + 引用 |
| 变更前健康基线（重构/迁移/大型功能） | `/health-audit` → `/prd` / `/ai-spec` | 技术债登记表 + 变更影响图 |
| 从 0 到 1 产品功能 | `/prd` → `/ai-spec` → `/api-first` | PRD + 规格 + API 包实现计划 |
| 全栈功能开发（已批准 SPEC 执行） | `/goal-driven` → `/api-first` → `/code-review` | 里程碑证据化执行 + 提交授权门 |
| Bug / 回归 | `/codebase-context` → `/debug` | 先判定归属层，再定点修复和验证 |
| UI 视觉 / 渲染问题 | `/debug-ui` → `/ux-experience-audit` | 视觉修复 + 用户路径验证 |
| 功能可用但体验不通 | `/ux-experience-audit` → `/debug` 或 `/api-first` | 跨层体验诊断和修复 |
| 大批量自动实现 | `/prd` 或 `/ai-spec` → `/ralph` / `/ralph-yolo` | User Story 循环实现 |
| 交付后迭代管理 | `/iteration` | 残差分类 BUG/DEBT/PRD_AMENDMENT/SPEC_AMENDMENT + 下一 Gate |
| 多 skill 系统 / 包设计 | `/loop-engineer` → `/ai-spec` | Gap 分析 + 编排层 |
| skill 机会发现 / 会话复盘 | `/discover-skill` | 挖掘可打包 skill 的工作模式 |
| 项目开发规范初始化 | `/sam-init` | PDCO 循环工作流（CLAUDE.md/PROGRESS-LOG/TASKS/self.opt） |
| 计算生物学干实验 | `/ai4s-lab` | SPEC 驱动 + OODA + Gate（W1-W4 强制记录） |
| 研究方法论沉淀 | `/extract-framework` | 从深度研究文档反向提取可复用框架 |
| 全栈安全审计 | `/security-audit` | `.debug/` 证据驱动分级报告（只审计不修复） |
| CI/CD / 发布 | `/gh-actions` / `/nodejs-npm-auto-release` | 工作流或 npm 发布闭环 |

---

## 📚 Available Commands

| Command | Purpose |
|---------|---------|
| `/ai-spec` | 主调度 — 需求分诊 + 技术规范生成 |
| `/deep-research` | 多 agent 并行深度调研（技术选型、文献、竞品） |
| `/dev-env-scan` | 开发环境扫描 + 偏好配置（输出 `.dev-profile.json` + CLAUDE.md 段落） |
| `/dev-host-init` | 宿主机一键初始化 — 环境探测+缺口提醒+codebase-mcp 部署提醒+分层注入体系生成（规则主文档+agent-reference 外置参考+pi 强化层 APPEND_SYSTEM/硬闸门扩展；pi 在 skill 层全量继承 .claude）（全局/项目，`/ai-spec init` 可触发） |
| `/intent-grill` | 需求追问对齐 — 逐分支追问至共识，维护 CONTEXT.md |
| `/api-first` | Activate the API-First modular development framework |
| `/debug` | Context-first code debugging (maintains `.debug/` records) |
| `/debug-ui` | Frontend UI debugging specialist |
| `/ux-experience-audit` | Cross-layer UX audit and fix loop |
| `/prd` | Generate structured PRD documents |
| `/code-review` | 混合代码审查（OCR CLI 优先 + Agent 降级，High/Medium/Low 分级） |
| `/codebase-context` | 代码库知识图谱查询（codebase-memory MCP 图谱优先 + GitNexus/静态分析降级） |
| `/health-audit` | 变更前项目健康与技术债基线审计 |
| `/goal-driven` | 批准后 SPEC 的证据化执行（里程碑循环 + 提交授权门） |
| `/iteration` | 交付后迭代管理（残差分类 + 下一 Gate） |
| `/discover-skill` | 技能机会发现 + 会话 skill 表现复盘 |
| `/sam-init` | PDCO 循环开发工作流初始化 |
| `/ai4s-lab` | AI4S 端到端干实验自动化研究引擎 |
| `/extract-framework` | 研究方法论反向提取 |
| `/security-audit` | 全栈安全审计（图谱嵌入 + 分面审计 + CVE + 渗透 + 分级报告，只审计不修复） |
| `/ralph` | Autonomous dev loop driven by PRD (manual cycle count) |
| `/ralph-yolo` | Ralph fully autonomous mode (unattended) |
| `/loop-engineer` | 多 skill 联动 package 设计与开发 |
| `/nodejs-npm-auto-release` | Node.js/npm 自动发布 |
| `/gh-actions` | GitHub Actions CI/CD workflow 生成器（多生态、多平台多架构构建） |

---

## 🔒 Core Development Rules

0. **Think before act（最高优先级，凌驾一切流程之上）** — 写代码/执行任务不是机械完成指令，而是先动脑子、综合判断**项目（架构/契约/并行状态）、环境（容器/数据/网络）、需求（字面+背后目的）、目的（任务在工作流的位置决定交付标准）、用户体验（产出价值密度 > 数量）** 五件事再动手。三条红线：(a) 不判根因就动手——很多"问题"是预期行为/遗留噪音，区分"真故障"和"设计行为"再决定动不动；(b) 不做综合判断就给主人甩半成品——该自己基于事实下判断的别让主人下，给「结论+依据+可执行下一步」而非「信息罗列+甩问题」，让主人做选择题不做问答题；(c) 为完成而完成、忽视产出价值——假绿的全面比不测更危险，宁可少而准不要多而假。判定速查：动手前能一句话说清"为什么这么做、不这么做怎样、对谁有何影响"？

1. **API-First (mandatory)** — Frontend/backend work follows three-layer separation (Frontend / BFF / Backend API packages). Every backend feature must complete the 5-step loop: **Implement → Checkfix → Encapsulate → Expose API → Document API**.
2. **Layer-scoped debugging** — Always identify the bug's owning layer (backend / frontend / BFF / contract mismatch) before making any fix. Never patch one layer to work around another layer's bug.
3. **Cross-layer task decomposition** — Requirements spanning multiple layers must be split into ordered sub-tasks along API boundaries — backend first → API docs → frontend consumption → integration verification.
4. **Repo Init + task loop** — Every development task follows `Archive → Develop → Test → Update plan → commit/push only with explicit authorization`. Never auto-commit without user confirmation.
5. **Research before opinion** — For technology selection, external SDKs, latest specs, or unfamiliar domains, run `/deep-research` first; do not answer from stale memory.
6. **Test artifact hygiene** — 测试产物卫生铁律。每次测试/验证/Checkfix 前后必须遵守 T0 测试前检查 → T1 测试后清扫 → T2 区分测试产物与运行数据（运行数据绝不删）→ T3 代码层老鼠屎清扫。完整规则见 `code-debugger` T0–T3。

---

## 🛠️ Configuration

- Permission allowlist: `.claude/settings.local.json`
- Ralph loop config: `.claude/ralph-config.json`
- PRD template: `.claude/templates/prd.json.example`
- Deep-research playbooks & scripts: `.claude/skills/deep-research/`

---

## 🌐 Three-Mirror Contract

CodeForge synchronizes every skill across three platforms:

| Platform | Skill root | Command root |
|----------|-----------|--------------|
| Claude Code | `.claude/skills/` | `.claude/commands/` |
| Codex CLI | `.codex/skills/` | (skills auto-trigger via description) |
| Gemini CLI | `.gemini/skills/` | (skills auto-trigger via description) |

Any skill change **must** update all three mirrors — this is enforced by review.

> 📖 **用其他 agent（Antigravity / OpenClaw / Hermes / WorkBuddy 等）？** 多 Agent 分类部署规则（🅰️ A 类直接 merge / 🅱️ B 类中立桥接）见 [`docs/agent-deployment-guide.md`](./docs/agent-deployment-guide.md)。
