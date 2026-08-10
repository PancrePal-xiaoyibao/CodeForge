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
| CI/CD / 发布 | `/gh-actions` / `/nodejs-npm-auto-release` | 工作流或 npm 发布闭环 |

---

## 📚 Available Commands

| Command | Purpose |
|---------|---------|
| `/ai-spec` | 主调度 — 需求分诊 + 技术规范生成 |
| `/deep-research` | 多 agent 并行深度调研（技术选型、文献、竞品） |
| `/dev-env-scan` | 开发环境扫描 + 偏好配置（输出 `.dev-profile.json` + CLAUDE.md 段落） |
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
| `/ralph` | Autonomous dev loop driven by PRD (manual cycle count) |
| `/ralph-yolo` | Ralph fully autonomous mode (unattended) |
| `/loop-engineer` | 多 skill 联动 package 设计与开发 |
| `/nodejs-npm-auto-release` | Node.js/npm 自动发布 |
| `/gh-actions` | GitHub Actions CI/CD workflow 生成器（多生态、多平台多架构构建） |

---

## 🔒 Core Development Rules

1. **API-First (mandatory)** — Frontend/backend work follows three-layer separation (Frontend / BFF / Backend API packages). Every backend feature must complete the 5-step loop: **Implement → Checkfix → Encapsulate → Expose API → Document API**.
2. **Layer-scoped debugging** — Always identify the bug's owning layer (backend / frontend / BFF / contract mismatch) before making any fix. Never patch one layer to work around another layer's bug.
3. **Cross-layer task decomposition** — Requirements spanning multiple layers must be split into ordered sub-tasks along API boundaries — backend first → API docs → frontend consumption → integration verification.
4. **Repo Init + task loop** — Every development task follows `Archive → Develop → Test → Update plan → commit/push only with explicit authorization`. Never auto-commit without user confirmation.
5. **Research before opinion** — For technology selection, external SDKs, latest specs, or unfamiliar domains, run `/deep-research` first; do not answer from stale memory.

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
