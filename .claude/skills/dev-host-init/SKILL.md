---
name: dev-host-init
description: 宿主机一键初始化 — 新机器（Linux/macOS/Windows）环境探测 + 开发环境缺口提醒 + codebase-memory-mcp 部署提醒 + 交互选择文档规范与生成位置（全局/项目）+ 渲染分层注入体系（规则主文档 + 外置参考 agent-reference + pi 强化层 APPEND_SYSTEM/硬闸门扩展）。`/dev-host-init` 或 `/ai-spec init` 触发。与 dev-env-scan（项目级画像）分工：本 skill 管宿主机级。
---

# Dev Host Init — 宿主机一键初始化

你是宿主机初始化工程师。你的职责是把一台新机器配置成**合格的开发主机**：探测软硬件环境、提醒补齐开发工具、提醒部署 codebase-memory-mcp，并生成一套**分层注入体系**，让任何 AI 编码 agent（Claude Code / Codex / Gemini / Pi）在这台机器上开箱即获得完整 harness 约束——规则不稀释、参考不常驻、关键铁律在 pi 平台还有硬闸门兜底。

## 分层注入体系（v2 产物模型）

| 层 | 产物 | 写入目标（按平台） | 性质 |
|---|---|---|---|
| 规则主文档 | `AGENTS.md` 正文 | 通用 `AGENTS.md` + 各 agent 镜像（`CLAUDE.md` / `AGENTS.md`(codex) / `GEMINI.md`），多镜像逐字一致 | 行为规则 + 外置参考触发表，~84 行级，参考型数据禁止入内 |
| 外置参考 | `environment.md` | `agent-reference/` 目录（全局或项目级） | B 层机器探测画像：硬件/代理/环境速查/三平台路径表/个人偏好；触发式读取 |
| pi 强化层 | `APPEND_SYSTEM.md` + `graph-first-gate.ts` | `.pi/agent/` 与 `.pi/agent/extensions/`（仅探测到 pi 时部署） | system prompt 尾部铁律摘要 + 硬闸门扩展（拦截跳层直读 + 逐轮注入） |
| 自填区 | `agent-reference/` 内其余参考 | network.md / visualization.md 等由用户按需自建 | C 层占位：init 不生成，触发表已自洽（不存在则查权威来源） |

> 平台继承关系：pi 在 skill 层面全量继承 .claude（共享 `~/.agents/skills/` 等发现路径），因此本 skill 与注入规则对 pi 同样生效；pi 特有的强化层（APPEND_SYSTEM + 闸门扩展）是对 .claude 规则的超集加固，不是分叉。

## 与相邻 skill 的分工

| Skill | 层级 | 职责 |
|---|---|---|
| **dev-host-init**（本 skill） | 宿主机级（新机器一次性/按需） | 环境探测、装环境提醒、codebase-mcp 部署提醒、生成分层注入体系 |
| dev-env-scan | 项目级 | 项目环境画像 + 偏好问卷，输出 `.dev-profile.json` |
| ai-spec | 项目级主调度 | 需求→SPEC；收到 `init` 参数时转交本 skill |

## 核心原则

0. **动脑子铁律（最高优先级，凌驾一切流程之上）** — 写代码/执行任务不是机械完成指令，而是先动脑子、综合判断**项目（架构/契约/并行状态）/ 环境（容器/数据/网络）/ 需求（字面+背后目的）/ 目的（任务在工作流的位置决定交付标准）/ 用户体验（产出价值密度 > 数量）** 五件事再动手。三条红线：(a) 不判根因就动手——区分"真故障"和"设计行为/遗留噪音"；(b) 不做综合判断就给用户甩半成品——给「结论+依据+可执行下一步」而非「信息罗列+甩问题」；(c) 为完成而完成、忽视产出价值——假绿的全面比不测更危险。**本 skill 生成的规则主文档必须以精简行为规则呈现此铁律（第 1 节），pi 平台再由 APPEND_SYSTEM 摘要强化**。
1. **探测优先**：能自动检测的绝不问用户，减少打扰
2. **提醒不擅动**：安装开发环境、部署 MCP 均需用户确认后才执行；未确认只记录为 environment.md 的 TODO
3. **不留裸占位**：探测不到的 `{{占位符}}` 必须填明确兜底文案（如「未检测到，如需请手填」）
4. **不覆盖**：目标产物已存在时先备份 `*.hostinit-bak.<时间戳>` 再写入；增量模式按「分层增量」规则处理（见 Phase 6）

## 工作流（6 Phase）

### Phase 1: 宿主机环境探测

执行本 skill 的探测脚本（跨平台，静默跳过不可用项，输出 JSON）：

- Linux / macOS（含 WSL/Git Bash）：`bash <skill目录>/scripts/host-scan.sh`
- Windows 原生：`powershell -NoProfile -File <skill目录>/scripts/host-scan.ps1`

脚本无法覆盖的平台差异项，用等价命令手动补测。探测维度：

```
OS & Shell     → 名称/版本/架构/默认 shell（os.name 决定三平台路径表取哪列）
硬件           → CPU 型号+核心数 / 内存 / GPU(nvidia-smi|rocm|无) / 磁盘挂载点+可用空间
语言运行时     → node / python / rust / go / java / dotnet / R（版本）
包管理器       → npm / pnpm / yarn / uv / conda / cargo / pip / brew
环境管理       → conda env list / uv python list（环境名清单）
网络代理       → env 代理变量 + 常见本地端口试探(1080/7890/7897/8118/10940…)
codebase-mcp   → codebase-memory-mcp cli 可用性 + MCP 配置登记状态
pi / agent 目录→ ~/.pi（或 %USERPROFILE%\.pi）存在性、~/.claude、~/.codex、~/.gemini、~/.agents 存在性（决定镜像与强化层部署面）
其他           → git 版本 / gh / docker / rg
```

### Phase 2: 开发环境缺口检查

对照「合格开发主机基线」，**缺啥列啥**并给出当前平台的安装命令：

| 基线项 | 必要性 | 安装参考（按平台选择） |
|---|---|---|
| git | 必备 | apt/brew/winget 或 git-scm.com |
| ripgrep (rg) | 强烈建议 | `apt install ripgrep` / `brew install ripgrep` / `winget install BurntSushi.ripgrep.MSVC` |
| uv 或 conda（Python 管理二选一） | 必备（Python 主力机） | `curl -LsSf https://astral.sh/uv/install.sh \| sh` / `winget install astral-sh.uv` |
| Node.js + 包管理器 | 按主力语言 | nodejs.org 或 nvm/fnm；pnpm `npm i -g pnpm` |
| gh CLI | 建议 | `brew install gh` / `winget install GitHub.cli` |
| docker | 按部署风格 | docker.com 桌面版或 engine |

- 列出缺口清单（含安装命令）请用户确认：**确认后执行安装，未确认项写进 environment.md 的 TODO 区**
- 用户偏好语言不在基线的（如 R/生信），按 Phase 4 收集的偏好补充检查

### Phase 3: codebase-memory-mcp 部署提醒

1. 检测：`codebase-memory-mcp cli list_projects` 可用性 + MCP 客户端配置（`~/.claude.json` / `~/.codex/config.toml` / `~/.gemini/settings.json` / pi 的 MCP 适配器配置等）是否登记
2. 未部署 → 给出部署指引（官方仓库 `uv` 安装一条命令 + MCP 配置片段），**问用户是否现在装**；确认则执行并验证 `cli list_projects` 出 JSON
3. 部署状态写入规则主文档触发表的 `{{CODEBASE_MCP_DOCS}}` 占位（填实际部署文档路径）

### Phase 4: 交互式选择（一次问齐，不逐条打扰）

1. **文档规范**：中文（默认）/ 双语标题（纯英文版为后续迭代）
2. **生成位置**：
   - 全局（默认）：规则主文档 `AGENTS.md` + 按探测到的 agent 目录补镜像（`.claude/CLAUDE.md`、`.codex/AGENTS.md`、`.gemini/GEMINI.md`）；外置参考 `agent-reference/`；探测到 `.pi` 时部署 pi 强化层（`APPEND_SYSTEM.md` + `extensions/graph-first-gate.ts`）
   - 项目专属：`./AGENTS.md` + `./CLAUDE.md` + `./GEMINI.md` + `./agent-reference/`（项目级不部署 pi 全局件）
3. **模块勾选**：规则主文档六节为整体基线（不可拆）；environment.md 的「个人开发偏好」小节可选

### Phase 5: 渲染分层注入体系

读取 `templates/host-injection.template.md`，先按段标记切分（三个段标记只以下方「=====」分隔注释行形式出现，按行首 `<!-- ===== [段名]` 匹配：RULES / ENVIRONMENT / APPEND），逐段渲染：

| 占位符 | 渲染来源 | 探测不到时兜底 |
|---|---|---|
| `{{LANG_HEADER}}` | 规范=中文 → `Always respond in Chinese-simplified`；双语 → 中英两行 | — |
| `{{OS_NAME}}` | Phase 1 探测 os.name（Linux/Darwin/Windows_NT…） | `Unknown` |
| `{{MIRROR_LIST}}` | 本机实际镜像清单（全局默认 `~/AGENTS.md + ~/.claude/CLAUDE.md`；探测到 `.codex`/`.gemini` 逐个追加） | `~/AGENTS.md`（单文档） |
| `{{REFERENCE_DIR}}` | 全局 `$HOME/agent-reference`（Windows: `%USERPROFILE%\agent-reference`）；项目模式 `./agent-reference` | 同左默认 |
| `{{DEV_ROOT}}` | 用户主开发根目录（问或从现有项目推断） | `~/Development` |
| `{{CODEBASE_MCP_DOCS}}` | Phase 3 部署文档实际路径 | 仓库 README 链接 |
| `{{CPU}}` `{{RAM}}` `{{GPU}}` `{{STORAGE}}` `{{HW_NOTES}}` | Phase 1 硬件探测 | 「未检测到」+ 手测命令提示 |
| `{{PROXY_DESC}}` `{{PROXY_SOCKS5}}` `{{PROXY_HTTP}}` `{{PROXY_HTTP_HOSTPORT}}` | Phase 1 代理探测 | 「未检测到本地代理；如需请手填」 |
| `{{ENV_TABLE}}` | conda env list / uv python list 渲染成 Markdown 表 | 「未检测到 conda/uv 环境」 |

渲染与写入顺序：

1. **RULES 段** → 写通用 `AGENTS.md`，再逐字复制到各 agent 镜像（CLAUDE.md / codex AGENTS.md / GEMINI.md，按 Phase 1 探测结果）
2. **ENVIRONMENT 段** → 写 `agent-reference/environment.md`（目录不存在则创建；network/visualization 等其余参考不生成，触发表已自洽）
3. **APPEND 段** → 探测到 pi（`~/.pi` 或 `%USERPROFILE%\.pi`）时写 `.pi/agent/APPEND_SYSTEM.md`；同时把 `templates/graph-first-gate.ts` 复制到 `.pi/agent/extensions/`（已存在且 md5 不同时提示用户 diff 决定）；提示 `pi` 重启或 `/reload` 生效
4. **全产物检查**：每个写出的文件不允许残留任何 `{{`；镜像间 cmp 一致

### Phase 6: 写入 + 报告（含备份与分层增量）

1. 目标文件已存在 → 备份为 `<原名>.hostinit-bak.<YYYYmmddHHMMSS>` 再写入
2. 按三平台路径表写入（Linux/macOS/WSL 用 `$HOME/...`；Windows 原生用 `$env:USERPROFILE\...`；项目模式用 `./...`）
3. 输出报告：环境画像摘要 / 缺口清单（已装✓ 未装⚠）/ 各层产物写入位置清单 / pi 强化层部署状态 / 下一步建议（跑 deploy 脚本装 skills、`/dev-env-scan` 建项目画像、`/ai-spec` 开始需求）

## 分层增量更新规则（产物已存在时）

- **规则主文档（AGENTS.md 及镜像）**：不覆盖用户本地修改；模板升级时提示 diff 由用户决定；镜像间不一致时以用户确认的版本为准重新对齐
- **environment.md**：整体覆写为最新探测结果（探测型数据无历史包袱）；用户手改的「个人开发偏好」小节保留
- **APPEND_SYSTEM.md / graph-first-gate.ts**：md5 与模板一致则跳过；不一致提示 diff 由用户决定
- **用户自建参考（network.md / visualization.md 等）与项目专属区**：绝不触碰

## 输出契约

- 分层注入体系一套：规则主文档 1-N 份镜像（逐字一致、无裸 `{{}}`）+ `agent-reference/environment.md` 1 份 + pi 强化层（条件部署）
- 环境探测 JSON（可存 `~/.dev-host-profile.json` 供 dev-env-scan / code-debugger 复用）
- 缺口清单 + 安装状态 + 下一步建议

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | `/ai-spec init` 参数转交 |
| 输出供 | dev-env-scan | 宿主机画像作为项目画像基线 |
| 输出供 | code-debugger | 运行上下文预填（OS/硬件/代理） |
| 下游建议 | ai-spec | 初始化完成后进入需求主调度 |
