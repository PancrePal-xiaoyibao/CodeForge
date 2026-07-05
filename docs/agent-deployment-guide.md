# 🤖 CodeForge 多 Agent 分类部署指南

> **看到一堆 AI agent 不知道 CodeForge 该装到哪？先判断你的 agent 属于哪一类，再选部署路径。** φ(≧ω≦*)♪

**适用对象**：想用 CodeForge 但不确定自己的 agent（Claude Code / Codex / Gemini / Antigravity / OpenClaw / Hermes / WorkBuddy / 未来的新 agent）该走哪条部署路径的开发者。

**核心承诺**：
- ✅ **A 类 agent**（有官方 skill 目录约定）→ deploy 脚本一键 merge，零额外配置
- ✅ **B 类 agent**（无官方 skill 目录约定）→ 走 `~/.agents/skills` 中立桥接层 + MCP / prompt 投喂
- ✅ 任何**未来新增**的 agent，都能用 §2 的 5 问 Checklist 自动归位

---

## 1. 为什么分两类（分类哲学）

CodeForge 的本质是 **16 个 prompt 层 skill + 三镜像目录结构**。这些 skill 要"装进"agent，前提是 **agent 得有一个 skill 加载入口**。

但现实是：不是所有 agent 都有这个入口。

- **Claude Code / Codex / Gemini** 这类"专业 coding agent"出厂就带官方 skill 目录约定（`~/.claude/skills/`、`~/.codex/skills/`、`~/.gemini/skills/`），CodeForge 直接把文件 merge 进去就行。
- **OpenClaw / Hermes / WorkBuddy** 这类"通用智能体"要么是社区开源项目（skill 目录约定不稳定），要么是 SaaS（根本没有本地目录），CodeForge 没法直接 merge，得**绕一层桥接**。

所以 CodeForge 的 deploy 脚本（[`deploy/deploy.sh`](../deploy/deploy.sh) / [`deploy/deploy.ps1`](../deploy/deploy.ps1)）早就埋好了**两层架构**：

```
┌─────────────────────────────────────────────────────────┐
│  A 类 merge（直接进 agent 官方目录）                       │
│    ~/.claude/skills + commands + agents                  │
│    ~/.codex/skills                                       │
│    ~/.gemini/skills                                      │
├─────────────────────────────────────────────────────────┤
│  B 类桥接（写一份到中立目录，通用 agent 自取）              │
│    ~/.agents/skills   ← deploy 第 85/78 行自动写入        │
└─────────────────────────────────────────────────────────┘
```

> **一句话判定**：你的 agent **官方文档里**有没有写明"skill 放在 `~/.<agent>/skills/`（或等价目录）"？有 → A 类；没有 → B 类。

---

## 2. 分类判定 Checklist（客观 5 问）

拿任何一个 agent，依次回答下面 5 个问题。**全"是" → 🅰️ A 类**；**任意一个"否" → 🅱️ B 类**。

| # | 判定问题 | 是 / 否 |
|---|---------|---------|
| Q1 | 该 agent 有**官方维护**的 skill / plugin / rules 加载目录约定吗？（不是社区 hack，是官方文档写明的） | ☐ |
| Q2 | 这个目录约定是**稳定**的（不是 alpha/实验性，版本间不轻易变）？ | ☐ |
| Q3 | CodeForge 的纯 Markdown skill 文件**能被原样识别**（不需要转译成 agent 私有格式）？ | ☐ |
| Q4 | 该 agent **本地运行**（有可写的本地配置目录，不是纯 SaaS 网页）？ | ☐ |
| Q5 | 社区已有**共识案例**证明这个目录约定可用（不是孤例）？ | ☐ |

**判定结果**：
- 5/5 全是 → 🅰️ **A 类 · Skill-Native 专业 Agent**（走 §4，deploy 直接 merge）
- 4/5 及以下 → 🅱️ **B 类 · 通用智能体**（走 §5，中立桥接 + MCP/prompt 投喂）
  - Q4 = 否（纯 SaaS） → 🅱️**B2 SaaS 类**（WorkBuddy）
  - Q4 = 是（本地 CLI/IDE） → 🅱️**B1 本地类**（OpenClaw、Hermes）

---

## 3. 部署总览矩阵

| Agent | 厂商 | 类别 | 判定依据 | Skill 目录 | 接入方式 | 自动部署 | 验证命令 |
|-------|------|------|---------|-----------|---------|---------|---------|
| **Claude Code** ⭐ | Anthropic | 🅰️ A | 官方 `~/.claude/skills` + `commands` | `~/.claude/` | deploy 直接 merge | ✅ 已支持 | `ls ~/.claude/commands/ai-spec.md` |
| **Codex CLI** | OpenAI | 🅰️ A | 官方 `~/.codex/skills` | `~/.codex/` | deploy 直接 merge | ✅ 已支持 | `ls ~/.codex/skills/ai-spec/SKILL.md` |
| **Gemini CLI** | Google | 🅰️ A | 官方 `~/.gemini/skills` | `~/.gemini/` | deploy 直接 merge | ✅ 已支持 | `ls ~/.gemini/skills/ai-spec/SKILL.md` |
| **Antigravity** | Google | 🅰️ A | 官方 setup file / AGENTS.md 约定 | 项目级 AGENTS.md | 手动 cp / 符号链接 | 🔧 已知 gap | 见 §4.4 |
| **OpenClaw** | OSS 社区 | 🅱️ B1 | 无官方 skill 目录约定 | — | `~/.agents/skills` 桥接 + MCP | ✅ 桥接层已写 | 见 §5.2.1 |
| **Hermes Agent** (hermas) | Nous Research | 🅱️ B1 | 自学习 `/learn`，非标准目录 | — | `~/.agents/skills` 桥接 + `/learn` 投喂 | ✅ 桥接层已写 | 见 §5.2.2 |
| **WorkBuddy** | 腾讯 | 🅱️ B2 | SaaS 网页端，无本地目录 | — | MCP + prompt 注入 | ⚙️ 网页端配置 | 见 §5.3.1 |

**图例**：✅ 已支持并验证 · 🔧 已知 gap（部分支持） · ⚙️ 需手动网页配置 · ⭐ 项目原生推荐首选

> 💡 想加新 agent？跳到 **[§8 新增 Agent 归位指南](#8-新增-agent-归位指南扩展性)**。

---

## ⚡ 快速复制：分流版一句话部署提示词

> 不想读完整步骤？直接把对应提示词贴进 Agent 会话即可。详细原理见 [§4](#4-🅰️-a-类--专业-agent-部署详解) / [§5](#5-🅱️-b-类--通用智能体接入方案)。**本节提示词与 [README Step 4](../README.md#step-4--一句话部署-codeforge-到-agent-环境) 逐字一致**。

### 🅰️ A 类（Claude Code / Codex / Gemini / Antigravity）

```text
请把 https://github.com/PancrePal-xiaoyibao/CodeForge 部署到当前用户的本机 Agent 环境。

要求：
1. 确认本机有 git 和可用 shell；如果缺依赖，先明确说明缺什么。
2. 克隆仓库到合适的本地目录；如果目录已存在且是 Git 仓库，先 git pull --ff-only。
3. 进入 CodeForge 仓库根目录后按系统执行：
   - Windows PowerShell: powershell -ExecutionPolicy Bypass -File .\deploy\deploy.ps1 -Yes
   - macOS / Linux Bash: chmod +x ./deploy/deploy.sh && ./deploy/deploy.sh --yes
4. 部署完成后确认存在下列之一：
   ~/.claude/commands/ai-spec.md
   ~/.codex/skills/ai-spec/
   ~/.gemini/skills/ai-spec/
5. 报告：部署路径、备份情况、下一步启动哪个 CLI。
```

### 🅱️ B 类（OpenClaw / Hermes / WorkBuddy）—— 走 `~/.agents/skills` 桥接层

把 `[你的 agent 名]` 换成 OpenClaw / Hermes / WorkBuddy：

```text
请把 https://github.com/PancrePal-xiaoyibao/CodeForge 部署到当前用户的本机 Agent 环境（B 类通用智能体路径）。

背景：我用的是 [你的 agent 名]，属于无官方 skill 目录约定的通用智能体（B 类），需要走 ~/.agents/skills 中立桥接层接入 CodeForge。

要求：
1. 确认本机有 git 和可用 shell；如果缺依赖，先明确说明缺什么。
2. 克隆仓库到合适的本地目录；如果目录已存在且是 Git 仓库，先 git pull --ff-only。
3. 进入 CodeForge 仓库根目录后按系统执行 deploy 脚本：
   - Windows PowerShell: powershell -ExecutionPolicy Bypass -File .\deploy\deploy.ps1 -Yes
   - macOS / Linux Bash: chmod +x ./deploy/deploy.sh && ./deploy/deploy.sh --yes
4. 部署完成后确认中立桥接层就位：
   ~/.agents/skills/ai-spec/SKILL.md
5. 根据我的 agent 类型激活桥接：
   - OpenClaw：配置 agent 读取 ~/.agents/skills/，或用 filesystem MCP 暴露该目录
   - Hermes (hermas)：对核心 skill 逐个跑 /learn（如 /learn ~/.agents/skills/ai-spec/SKILL.md）
   - WorkBuddy：在网页端配 MCP 指向 ~/.agents/skills/，或贴能力注入 prompt
6. 报告：部署路径、桥接层就位情况、agent 特定激活步骤是否完成、下一步。
```

> 💡 提示词里的 `[你的 agent 名]` 是占位符，贴之前先替换成你实际用的 agent。B 类 agent 的激活差异（步骤 5）会在 [§5](#5-🅱️-b-类--通用智能体接入方案) 详细展开。

---

## 4. 🅰️ A 类 · 专业 Agent 部署详解

A 类 agent 的部署**完全一致**：跑一次 deploy 脚本，skill 自动 merge 到 agent 官方目录。区别只在"用哪个 CLI 启动"和"如何配 API Key"。

### 4.1 Claude Code（Anthropic）⭐ 项目原生推荐

**为什么推荐**：CodeForge 三镜像契约以 Claude Code 的 `commands/` + `skills/` 为最完整入口，16 个 slash command（`/ai-spec`、`/deep-research` 等）原生可用。

**安装 CLI**：

```bash
# Linux / macOS / Codespace
npm install -g @anthropic-ai/claude-code

# Windows PowerShell / CMD
npm install -g @anthropic-ai/claude-code
```

**部署 CodeForge skill**（任选一种，二选一即可）：

```bash
# 方式 A · 跑仓库自带 deploy 脚本（推荐，自动备份重名文件）
git clone https://github.com/PancrePal-xiaoyibao/CodeForge.git
cd CodeForge
# Linux / macOS / Codespace
./deploy/deploy.sh --yes
# Windows PowerShell
.\deploy\deploy.ps1 -Yes
```

```bash
# 方式 B · Codespace 零配置（.devcontainer 已自动跑 deploy）
# 直接在 Codespace 终端敲 claude 即可
```

**配 API Key**：
- 🌏 海外：`claude` 首次运行按提示登录 Anthropic 账号
- 🇨🇳 国内：用国产大模型（GLM-5.2[1m] / DeepSeek / Kimi / 小米 MiMo）→ 完整配置见 **[docs/cn-api-providers.md](./cn-api-providers.md)**

**启动 + 验证**：

```bash
claude --permission-mode bypassPermissions
# 在 Claude Code 会话里输入：
> /ai-spec
# 有响应 = 部署成功喵～
```

**验证命令**（deploy 后立即检查）：

```bash
# Linux / macOS / Codespace
ls ~/.claude/commands/ai-spec.md && echo "✅ Claude Code skill 已就位"

# Windows PowerShell
Test-Path "$env:USERPROFILE\.claude\commands\ai-spec.md"
```

---

### 4.2 Codex CLI（OpenAI）

**安装 CLI**：

```bash
npm install -g @openai/codex
```

**部署 CodeForge skill**：同 §4.1 的 deploy 脚本（脚本会同时 merge `.codex/skills`）。

**配 API Key**：

```bash
# Linux / macOS / Codespace
export OPENAI_API_KEY=your-key

# Windows PowerShell
$env:OPENAI_API_KEY="your-key"

# Windows CMD
set OPENAI_API_KEY=your-key
```

**启动 + 验证**：

```bash
codex
# Codex 按 skill 的 description 自动触发，无需 slash command
# 描述一个需求，如"帮我设计一个用户认证功能"→ 自动激活 ai-spec
```

**验证命令**：

```bash
# Linux / macOS / Codespace
ls ~/.codex/skills/ai-spec/SKILL.md && echo "✅ Codex skill 已就位"

# Windows PowerShell
Test-Path "$env:USERPROFILE\.codex\skills\ai-spec\SKILL.md"
```

---

### 4.3 Gemini CLI（Google）

**安装 CLI**：

```bash
npm install -g @google/gemini-cli
```

**部署 CodeForge skill**：同 §4.1 的 deploy 脚本（脚本会同时 merge `.gemini/skills`）。

**配 API Key**：

```bash
# Linux / macOS / Codespace
export GEMINI_API_KEY=your-key
# 或用 Google 账号登录：首次运行 gemini 按提示

# Windows PowerShell
$env:GEMINI_API_KEY="your-key"
```

**启动 + 验证**：

```bash
gemini
# 同 Codex，按 skill description 自动触发
```

**验证命令**：

```bash
# Linux / macOS / Codespace
ls ~/.gemini/skills/ai-spec/SKILL.md && echo "✅ Gemini skill 已就位"

# Windows PowerShell
Test-Path "$env:USERPROFILE\.gemini\skills\ai-spec\SKILL.md"
```

---

### 4.4 Antigravity（Google）🔧 已知 gap

> **⚠️ 状态说明**：Antigravity 是 Google 的 agentic IDE（基于 Gemini），有项目级 setup file / `AGENTS.md` 约定，符合 A 类判定。但 **CodeForge 的 deploy 脚本目前未覆盖 Antigravity 的 skill 目录**，需要手动桥接。自动 merge 待 [Path B PR](../CONTRIBUTING.md) 增强。

**判定为 A 类的依据**：
- Q1 ✅ 有官方 agent rules / setup file 约定
- Q2 ✅ 约定稳定（基于项目根 `AGENTS.md` + IDE 内 rules）
- Q3 ✅ 能识别 Markdown
- Q4 ✅ 本地 IDE
- Q5 ✅ 社区共识（superpowers 等 skill 生态已支持）

**手动部署步骤**（在 Antigravity 打开你的项目后）：

1. **确保项目根有 `AGENTS.md`**（CodeForge 已自带，[见根目录](../AGENTS.md)）。Antigravity 会自动读取它作为 agent 行为约束。

2. **把 CodeForge skill 引入项目**（任选一种）：

   ```bash
   # 方式 A · 符号链接（推荐，skill 更新自动同步）
   # Linux / macOS
   ln -s ~/.codex/skills ./.antigravity/skills
   # Windows PowerShell（需管理员权限或开发者模式）
   New-Item -ItemType SymbolicLink -Path .\.antigravity\skills -Target $env:USERPROFILE\.codex\skills

   # 方式 B · 直接复制（不自动同步）
   cp -r ~/.codex/skills ./.antigravity/skills   # Linux/macOS
   Copy-Item -Recurse $env:USERPROFILE\.codex\skills .\.antigravity\skills   # PowerShell
   ```

   > 💡 具体 skill 目录路径以 **Antigravity 官方文档**最新版为准。上面是社区验证可用的方案。

3. **在 Antigravity 里验证**：打开一个对话，描述"帮我做技术选型调研"，看是否触发 deep-research skill。

**待增强（⏳ TODO）**：在 `deploy/deploy.sh` / `deploy.ps1` 增加 `merge_codeforge_dir ".codex/skills" ".antigravity/skills"` 分支，实现自动部署。欢迎按 [CONTRIBUTING.md §Path B](../CONTRIBUTING.md) 提 PR。

---

## 5. 🅱️ B 类 · 通用智能体接入方案

### 5.1 桥接层原理：`~/.agents/skills` 中立目录

B 类 agent 没有官方 skill 目录约定，但 CodeForge 不能因此让它们用不上 skill。解决方案是 deploy 脚本早就写好的**中立桥接目录**：

```bash
# deploy/deploy.sh 第 85 行 / deploy.ps1 第 78 行
merge_codeforge_dir ".codex/skills" ".agents/skills"
```

这行代码把 CodeForge 的全套 skill 镜像一份到 `~/.agents/skills/`：

```
~/.agents/skills/
├── ai-spec/SKILL.md
├── api-first-modular/SKILL.md
├── code-debugger/SKILL.md
├── code-review/SKILL.md
├── deep-research/SKILL.md
├── dev-env-scan/SKILL.md
├── ...（16 个 skill 全套）
```

**为什么用 `.agents/`**：这个目录名**中立**，不属于任何一家厂商，是社区约定的"通用 agent skill 仓库"。任何 agent 只要愿意读这个目录，就能拿到 CodeForge 全套能力。

**B 类接入的通用三步**：
1. 跑 deploy 脚本（桥接目录自动写入）
2. 配置你的 agent 读取 `~/.agents/skills/`（或用 MCP / prompt 投喂）
3. 验证 skill 能被识别

**验证桥接层就位**：

```bash
# Linux / macOS / Codespace
ls ~/.agents/skills/ai-spec/SKILL.md && echo "✅ 中立桥接层已就位"

# Windows PowerShell
Test-Path "$env:USERPROFILE\.agents\skills\ai-spec\SKILL.md"
```

---

### 5.2 B1 本地 CLI 类

#### 5.2.1 OpenClaw（开源 Claude Code 替代）

**项目简介**：OpenClaw 是社区维护的开源 agentic CLI，定位为 Claude Code 的开源替代，可运行 Anthropic Opus 等模型。**具体安装与 skill 目录约定以 [OpenClaw 官方仓库](https://github.com/topics/openclaw) 最新文档为准。**

**接入三步**：

1. **跑 CodeForge deploy**（桥接目录自动写入）：

   ```bash
   git clone https://github.com/PancrePal-xiaoyibao/CodeForge.git
   cd CodeForge && ./deploy/deploy.sh --yes   # 或 .\deploy\deploy.ps1 -Yes
   ```

2. **让 OpenClaw 读取中立目录**（按 OpenClaw 配置机制二选一）：

   - **方式 A · 配置文件指向**：在 OpenClaw 的配置里把 skill 路径指向 `~/.agents/skills/`（具体配置项查 OpenClaw 文档）。
   - **方式 B · MCP 桥接**：用 [filesystem MCP server](https://github.com/topics/model-context-protocol) 把 `~/.agents/skills/` 暴露给 OpenClaw，让它能 `read` 这些 SKILL.md。

3. **验证**：在 OpenClaw 会话里描述"帮我跑一次 ai-spec 需求审计"，看是否激活 ai-spec skill。

**验证命令**：

```bash
# 桥接层就位检查
ls ~/.agents/skills/ | head   # 应看到 16 个 skill 目录
# OpenClaw 能否读取，取决于步骤 2 的配置是否生效
```

> 💡 **推荐**：B1 类 agent 优先用 **MCP filesystem 桥接**，比改 agent 私有配置更通用、更稳定。

---

#### 5.2.2 Hermes Agent（hermas · Nous Research）

**项目简介**：Hermes Agent 是 Nous Research 的**自学习 AI agent**（GitHub: [`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent)），内置学习循环，能用 `/learn` 命令把文档转成持久知识。社区常简称为 "hermas"。

> 💡 **拼写说明**：`hermas` 是社区口语拼写，正式名是 **Hermes Agent**。本文档统一写作 `Hermes Agent (hermas)`。

**接入三步**：

1. **跑 CodeForge deploy**（桥接目录自动写入）：

   ```bash
   git clone https://github.com/PancrePal-xiaoyibao/CodeForge.git
   cd CodeForge && ./deploy/deploy.sh --yes
   ```

2. **用 Hermes 的 `/learn` 投喂 CodeForge skill**（Hermes 的特色玩法）：

   ```text
   # 在 Hermes 会话里
   /learn ~/.agents/skills/ai-spec/SKILL.md
   /learn ~/.agents/skills/deep-research/SKILL.md
   /learn ~/.agents/skills/api-first-modular/SKILL.md
   # ...（或批量 learn 整个目录）
   ```

   Hermes 会把这些 skill 内化为它的持久能力，**之后即使删掉原文件，能力也保留**——这是 Hermes 区别于其他 agent 的核心优势。

3. **验证**：投喂后，描述"帮我做一个 API-First 的用户认证功能"，看 Hermes 是否按 CodeForge 的 API-First 流程拆解任务。

**验证命令**：

```bash
# 桥接层就位
ls ~/.agents/skills/ai-spec/SKILL.md
# Hermes 学习效果在会话内验证（/learn 后无报错即成功）
```

> 💡 **Hermes 模型无关**：支持 OpenRouter / OpenAI / Anthropic / Nous Portal / 本地模型，配好任一 provider 即可。

---

### 5.3 B2 SaaS 类

#### 5.3.1 WorkBuddy（腾讯）

**项目简介**：WorkBuddy 是腾讯的**多智能体工作空间**（SaaS 网页端），自动化文档、研究、电子表格，定位为"AI 员工"。**纯网页端，无本地 skill 目录**，因此 B2 类接入方式与前两类本质不同。

**接入方式（网页端配置，⚙️ 手动）**：

1. **deploy 脚本依然要跑**（虽然 WorkBuddy 读不到本地目录，但为你**本地备用**的其他 agent 准备好桥接层）：

   ```bash
   cd CodeForge && ./deploy/deploy.sh --yes
   ```

2. **在 WorkBuddy 网页端接入 CodeForge 能力**（二选一或组合）：

   - **方式 A · MCP 接入**（若 WorkBuddy 支持 MCP）：在 WorkBuddy 的 MCP 配置里加一个 filesystem server，指向你本地的 `~/.agents/skills/` 目录，让 WorkBuddy 的 agent 能读取 CodeForge skill。模板见 [`deploy/mcp-config.template.json`](../deploy/mcp-config.template.json)。
   - **方式 B · Prompt 注入**：在 WorkBuddy 新建对话时，把下面这段精简版"能力注入 prompt"贴进去：

     ```text
     你已接入 CodeForge 工作流。遇到以下场景请按对应流程：
     - 新需求 → 先做需求审计（核心功能/非功能需求/技术挑战），再拆 API-First 子任务
     - 外部信息/技术选型 → 先调研，保留引用，不凭记忆作答
     - Bug → 先判定归属层（后端/前端/BFF/契约），再定点修复
     - 代码变更后 → 跑 lint/typecheck/test 三件套
     - commit/push → 必须等我明确授权，绝不自主推送
     完整 16 个 skill 规范见 ~/.agents/skills/ 各 SKILL.md。
     ```

3. **验证**：在 WorkBuddy 里描述一个开发需求，看 agent 是否按 CodeForge 的 API-First / 人在回路约束行动。

> ⚠️ **ETHICS 边界**：WorkBuddy 这类 SaaS 接入时，**不要把生产密钥、真实用户数据传给网页端**。CodeForge 的 skill 是 prompt 层配置，传 prompt 本身安全；传数据要谨慎。详见 [ETHICS.md](../ETHICS.md)。

---

## 6. 混合编排：一个人同时用多个 agent

实际开发中你可能**同时开多个 agent**（比如 Claude Code 主力 + Hermes 辅助学习 + WorkBuddy 做文档）。CodeForge 的设计天然支持这种混合用法：

### 6.1 推荐组合

| 场景 | 推荐组合 | 理由 |
|------|---------|------|
| 主力开发 | Claude Code ⭐ 单开 | 三镜像最完整，16 个 slash command 原生可用 |
| 长循环批量实现 | Codex / Gemini + Claude Code | 不同模型互补，避免单点过载 |
| 沉淀团队知识 | Claude Code + Hermes | Claude 干活，Hermes `/learn` 把成果内化为持久能力 |
| 文档/研究自动化 | Claude Code + WorkBuddy | 代码用 Claude，文档自动化用 WorkBuddy |

### 6.2 共享桥接层

所有 B 类 agent **共享同一个 `~/.agents/skills/` 目录**，所以你只需跑一次 deploy，所有 B 类 agent 都能读到。**A 类和 B 类可以并存**：deploy 脚本会同时写 A 类官方目录 + B 类中立目录，互不干扰。

### 6.3 切换不丢失

每个 agent 的 skill 都是**独立副本**（deploy 是 `cp -r` 不是符号链接），所以：
- 卸载某个 agent 不影响其他 agent 的 skill
- CodeForge 升级后重跑 deploy，重名文件自动备份（`*.codeforge-bak.<TIMESTAMP>`）

---

## 7. 故障排查 FAQ

### Q1: 跑完 deploy，但 agent 里 `/ai-spec` 没反应？

**A**：分类排查：
- **A 类**：检查 agent 官方目录是否真有文件（用 §4 各节的"验证命令"）。Windows 用户注意 `$env:USERPROFILE` vs `$HOME`。
- **B 类**：检查 `~/.agents/skills/` 是否就位（§5.1 验证命令），再确认你的 agent 是否真的配了读取该目录 / MCP / `/learn`。

### Q2: deploy 报"重名文件已备份"是怎么回事？

**A**：正常现象。deploy 用 `merge_codeforge_dir`，遇到同名文件会自动备份为 `*.codeforge-bak.<TIMESTAMP>` 再覆盖。你之前的配置没丢，在备份文件里。想恢复就把备份 rename 回去。

### Q3: 我用的 agent 不在矩阵里，怎么判断 A 还是 B？

**A**：跑 §2 的 5 问 Checklist。5/5 全是 → A 类；否则 B 类。判定完按 §4 或 §5 对应方案接入，并欢迎按 §8 提 PR 把它补进矩阵。

### Q4: WorkBuddy（SaaS）能像 Claude Code 一样用全部 16 个 skill 吗？

**A**：**不能完全等同**。SaaS 类靠 MCP / prompt 注入，skill 是"软接入"，不像 A 类那样原生 slash command。复杂 skill（如 `/ralph` 自主循环）在 SaaS 上可能降级为 prompt 引导。需要完整能力请用 A 类。

### Q5: Antigravity 为什么是 🔧 而不是 ✅？

**A**：因为 deploy 脚本还没覆盖 Antigravity 的 skill 目录（ADR-004：本次不改脚本）。Antigravity 本身符合 A 类判定，只是自动 merge 待 Path B PR 增强。现在手动 cp 或符号链接即可用（§4.4）。

### Q6: Hermes 的 `/learn` 和直接读 skill 目录有什么区别？

**A**：`/learn` 是 Hermes 特色——把文档**内化为持久知识**，删原文件能力也在；直接读目录是"现读现用"，文件没了能力就没了。两者可组合：先 `/learn` 核心 skill，再保留目录做参考。

### Q7: 国内网络，B 类 agent 接入有特殊注意吗？

**A**：B 类 agent 多为开源/海外服务。国内用户注意：
- OpenClaw / Hermes 本地运行 → 配国产模型 API（参考 [cn-api-providers.md](./cn-api-providers.md)）
- WorkBuddy 是腾讯产品 → 国内访问无障碍，但注意 ETHICS 的数据边界

---

## 8. 新增 Agent 归位指南（扩展性）

发现了一个矩阵里没有的新 agent？按下面流程归位，并欢迎提 PR。

### 8.1 归位三步

1. **跑 §2 的 5 问 Checklist**，判定 A / B（B 再分 B1 / B2）。
2. **按对应类别试接入**（A 类试 deploy merge，B 类试桥接 + MCP）。
3. **验证可用后**，按下面 PR 模板补进矩阵。

### 8.2 PR 模板

```
标题：docs(agent-deployment): add <agent-name> to deployment matrix

改动：
1. docs/agent-deployment-guide.md §3 矩阵新增一行 + §4 或 §5 新增一节
2. README.md "多 Agent 分类部署"章节矩阵同步新增（C1 一致性约束）
3. 若该 agent 触发了新接入方式，更新 §5 桥接层说明

判定依据（贴 §2 Checklist 5 问答案）：
- Q1: ...
- Q2: ...
- ...

验证证据：
- [ ] 跑过 deploy，桥接/官方目录就位
- [ ] agent 实测能激活至少 1 个 skill
- [ ] 截图/日志
```

提交前必读 [CONTRIBUTING.md §Path B](../CONTRIBUTING.md)，遵守三镜像同步 + AI 辅助披露 + ETHICS。

### 8.3 已知待增强（⏳ TODO）

| 项 | 状态 | 说明 |
|----|------|------|
| Antigravity 自动 merge | ⏳ | deploy 脚本加 `.antigravity/skills` 分支 |
| 更多 A 类 agent（Trae / Windsurf / Cursor Agent 等） | ⏳ | 跑 §2 Checklist 后按 §8.2 提 PR |
| B 类 MCP 桥接标准化模板 | ⏳ | 沉淀一份通用 filesystem MCP 配置 |

---

## 9. 三镜像与本文档的关系

**本文档是 `docs/` 下的单一文档**，**不需要三镜像**（与 [`docs/cn-api-providers.md`](./cn-api-providers.md) 同范式）。但以下两处需要保持同步：

| 同步点 | 文件 | 同步内容 |
|--------|------|---------|
| ① README 分类门户 | [`README.md`](../README.md) "多 Agent 分类部署"章节 | 矩阵表内容必须与本文 §3 **逐字一致** |
| ② 三入口指针 | [`CLAUDE.md`](../CLAUDE.md) / [`AGENTS.md`](../AGENTS.md) / [`GEMINI.md`](../GEMINI.md) | 各保留一行指向本文档的链接 |

**改本文档时的检查清单**：
- [ ] §3 矩阵改动后，同步改 README 矩阵（C1 约束）
- [ ] 新增 agent 后，三入口文档的指针仍有效
- [ ] 所有内部链接无死链
- [ ] 遵守 [ETHICS.md](../ETHICS.md)（B2 SaaS 类不得建议绕过人工审批）

---

<div align="center">

**不管你的 agent 是哪一类，CodeForge 都有路可走喵～** (´｡• ᵕ •｡`) ♡

_判断不准？回到 [§2 Checklist](#2-分类判定-checklist客观-5-问) 重新走一遍。_

</div>
