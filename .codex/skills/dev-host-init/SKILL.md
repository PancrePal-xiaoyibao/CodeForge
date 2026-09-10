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
| 外置参考 | `environment.md` + `tooling.md` | `agent-reference/` 目录（全局或项目级） | B 层机器探测画像：硬件/代理/环境速查/三平台路径表/个人偏好；图谱工具指南：CLI 速查/场景映射/三层 fallback 状态机/反例/决策树；均触发式读取 |
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
0'. **齐头并进铁律（与动脑子同权，防顾头不顾腚）** — 任何改动必须**同时照顾系统的所有相关层面**，绝对禁止"只改一端"而忽略其余。前后端项目：改后端必须让前端体现变动（或明确告知"为什么前端没动"）；多端/5 头项目（KAIROS 等：前端/MCP 端/内置 agent-skill 端/外置 agent-skill 端/后端）：**任何 CHG→开发→测试→commit/push 全链路须五端齐头并进**，缺一不可。交付前自问"每个受影响层面我都同步了吗？没同步的有理由吗？"答不出则停下补齐；只改一端就标 CHG 完成 = 违规。**本 skill 生成规则主文档时须在第一节呈现此铁律（第 1.1 节），pi 平台 APPEND_SYSTEM 摘要同样强化**。
0''. **说人话铁律（与动脑子同权，防黑话/谢绝术语）** — 一切对用户/其他 Agent 的输出**必须说人话**：先结论，再必要依据。禁止堆术语/黑话/缩写（MCP/CHG 之类首次必解释）、禁止把"结论+一张表"当交付、禁止用语气词/颜文字掩盖不清晰表达；复杂逻辑用举例+类比，不用术语堆叠。**本 skill 生成规则主文档时须在第一节呈现此铁律（第 1.2 节），pi 平台 APPEND_SYSTEM 摘要同样强化**。
1. **探测优先**：能自动检测的绝不问用户，减少打扰
2. **提醒不擅动**：安装开发环境、部署 MCP 均需用户确认后才执行；未确认只记录为 environment.md 的 TODO
3. **不留裸占位**：探测不到的 `{{占位符}}` 必须填明确兜底文案（如「未检测到，如需请手填」）
4. **不覆盖**：目标产物已存在时先备份 `*.hostinit-bak.<时间戳>` 再写入；增量模式按「分层增量」规则处理（见 Phase 6）

## 工作流（6 Phase + Phase 0 强制问卷）

### Phase 0: 强制完整问卷（先于一切探测/渲染/写入）

> 用户点名要渲染**全量 / 性能档 / 完整注入**时，**铁律全文是否完整不取决于问卷——性能档的 PERFORMANCE 段本就把动脑子/说人话/齐头并进/开源脱敏等铁律全文一次性固死在模板正文里（模板升级改的是铁律内容，不因问卷裁剪）**。问卷只决定"往模板里填什么动态内容"，绝不裁剪铁律本身。

**任何一次 init（含 `/ai-spec init`）都必须跑完整问卷**，即使只差想跳过某一项也要显式选"跳过"。用 **AskUserQuestion 一次问齐**以下 5 组（每组附"可选/可跳过/可自填"）：不探测、不渲染、不写入。

**Q1 作用域（先问）**
1. **作用域**：全局（写入 `$HOME`/`%USERPROFILE%`，本机所有项目共享）还是**项目级**（只写这个仓库，可入库）？
2. **项目路径**：若项目级 → **目标目录是不是当前工作目录（cwd）？** 不是的话给绝对路径。先 `--dry-run` 回显"将写入路径清单"确认后真写。
3. 项目级附加：git 管理的仓库说明产物会进 `git status`，是否 `gitignore` 或直接入库；项目级**不部署** pi 强化层。

**Q2 注入规格**（Phase 4 的反向合并）：性能（全量）默认 / 经济（分层）/ 超轻 / 自定义。性能全量时 PERFORMANCE 段铁律全文固写、不受问卷影响；经济/超轻只写 RULES 段（行为规则+触发表，参考外置）。

**Q3 美术/视觉风格（可跳过、可自填，绝不写死不替他域套用）**

诉诸描述性风格而非唯一领域；**不默认等于"单细胞暖粉/冷紫"**。预设 6 档 + 可跳过 + 可自填：

| 档位 | 语义 | 参数 |
|---|---|---|
| 工程冷静 · 深海蓝灰 | 低饱和蓝灰+冷强调，克制专业 | `engineering-calm` |
| 科研学术 · 暖纸古蓝 | 米白纸底+古蓝/暗红，克制数据色谱 | `academic-muted` |
| 温暖人文 · 焦糖暖橙 | 奶油底+焦糖/珊瑚，人文感强 | `warm-human` |
| 暗黑高级 · 墨黑鎏金 | 近黑底+金/青极光，NV 高级感 | `dark-premium` |
| 自然生态 · 苔绿雾松 | 苔绿+陶土/雾蓝，天然透气 | `nature-fresh` |
| 艺术活力 · 钴蓝朱红 | 高饱和钴蓝+朱红，年轻张力 | `art-vivid` |

- **可跳过**：`art_skip=true` → 注入正文给"未在 init 问卷选择（命中视觉任务按 visualization.md 现场确立）"，不落死色。
- **可自填**：给一段争议性描述（"前端 Vue 仪表盘，深色科技感"…）→ 用 `tools-catalog.auto_palette` 的哈希→色相族 + CBDR 对比逻辑生成**初始提案**写入 visualization.md，用户可后续手调。**自填≠自动落库当最终答案**：先给提案、确认后写。
- 生成：`visualization.md`（风格+主/强调/背景/正文+语义渐变）+ 注入正文 `ART_STYLE_SUMMARY` 一段。

**Q4 工具部署偏好（可跳过；覆盖"源码/二进制/包管理器/官方安装器"全部路由）**

对每个工具问**采用哪种安装方式**并给出一键命令（含真实下载源，查证于官方与 `E:/Development/codebase-memory-mcp/DEPLOYMENT.zh-CN.md`）：

| 工具 | 可选项（示例） |
|---|---|
| codebase-memory-mcp | 官方安装脚本(二进制/推荐) / 源码编译 / npm i -g / uv tool |
| pi（@earendil-works/pi-coding-agent） | npm i -g（推荐）/ 官方安装器 / 源码 |
| gh / GitHub CLI | winget / apt / 官网 MSI / 源码 go build |
| rg / ripgrep | winget / apt / 官网二进制 |
| uv | winget / 官方安装器（irm/curl） |
| node | 官方 LTS / nvm-windows / 官网 tarball |
| gh login 快速免密 | `gh auth login`（凭据存本机，免密做远端） |

已装工具选项显示"已装✓"；未装按选择渲染到 `environment.md` 的**开发工具部署计划**节。**每项都可跳过**：跳过=不动该工具、不写部署命令。

**Q5 部署/配置偏好（可跳过）**：部署风格（本地/远程跳板/容器）、测试哲学、代码风格、CI/CD、Monorepo/Polyrepo、风险偏好（"源码优先可控 / 二进制快速 / 包管理器整洁"）。未填一律**不替用户默认某一种**，注入只保留"默认偏好模板"占位。

> 问卷产出统一作为 `──config questionnaire.json` 传给 render-now.py；**任何"可跳过"项 == 不注入该动态块**（铁律正文不受影响）。判断辅佐（可不问即推断，但推断结果要在报告说明）：用户说"这台机器/新机器/开箱即用"→全局；"这个项目/这个仓库/给 repo 加规则"或 cwd 即仓库→项目级；两者都要→先全局再项目级，分两次渲染。

### Phase 1: 宿主机环境探测

执行本 skill 的探测脚本（跨平台，静默跳过不可用项，输出 JSON）：

- Linux / macOS（含 WSL/Git Bash）：`bash <skill目录>/scripts/host-scan.sh`
- Windows 原生：`powershell -NoProfile -File <skill目录>/scripts/host-scan.ps1`

> ⚠️ Windows 原生（含 Git Bash）**优先用 `host-scan.ps1`**：Git Bash 里没有系统 `lscpu`/`free`/`nproc`，`.sh` 会输出空 JSON 导致硬件/代理全落空。`fill-placeholders.py` 已按 `os.name` 分派（Win→ps1，POSIX→sh），新脚本请沿用同一分派逻辑。

脚本无法覆盖的平台差异项，用等价命令手动补测。探测维度：

```
OS & Shell     → 名称/版本/架构/默认 shell（os.name 决定三平台路径表取哪列）
硬件           → CPU 型号+核心数 / 内存 / GPU(nvidia-smi|rocm|无) / 磁盘挂载点+可用空间
语言运行时     → node / python / rust / go / java / dotnet / R（版本）
包管理器       → npm / pnpm / yarn / uv / conda / cargo / pip / brew
环境管理       → conda env list / uv python list（环境名清单）
网络代理       → env 代理变量 + 常见本地端口试探(1080/7890/7897/8118/8888…)
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

### Phase 4: 注入规格（问卷 Q2 已定；此处保留分档事实表供 render-now 决策）

| 档位 | 产物 | token 消耗（模型起始上下文） | 适用对象 |
|---|---|---|---|
| **性能（全量，默认）** | `PERFORMANCE` 段 → AGENTS.md + 各 agent 镜像全量正文（**铁律全文固写，不因问卷裁剪** + 环境/偏好画像驻留，~10KB/会话） | 高 | 不差钱、要铁律遵守密度与首次质量；**默认档** |
| **经济（分层）** | `RULES` 段 → AGENTS.md + 镜像（行为规则 + 触发表，~2KB/会话）；环境/偏好/工具外置 `agent-reference/` 触发式读取 | 低 | 少数轻量任务，token 敏感 |
| **超轻** | `RULES` 段 → 仅 AGENTS.md（极简行为规则 + 触发表），不生成 agent 镜像 | 极低 | 简单/短任务、token 极敏感 |
| **自定义** | 用户勾选内联内容（铁律全文 / 环境 / 偏好 / 配色 / 网络…） | 按勾选 | 需要精确裁剪 |

分档对照如实告知：性能档把「环境 + 偏好 + 铁律」写入起始上下文 → 模型无需先查参考即可遵守，token 成本高；经济/超轻档省 token，但环境/偏好需命中任务读参考，遵守密度受触发准确性影响。超轻档只有一份 AGENTS.md，跨平台行为不完全一致。

> 分档只决定「铁律正文用量（PERFORMANCE vs RULES）与参考常驻与否」，**不裁剪任何铁律原文**。生成位置由问卷 Q1 决定：全局写 `$HOME` 四镜像 + pi 强化层；项目级写 `./AGENTS.md` + `./CLAUDE.md` + `./GEMINI.md` + `./agent-reference/`，不部署 pi 全局件。

### Phase 5: 渲染分层注入体系（问卷已定动态内容；铁律全文由模板固写）

读取 `templates/host-injection.template.md`，先按段标记切分（四个段标记只以下方「=====」分隔注释行形式出现，按行首 `<!-- ===== [段名]` 匹配：RULES / PERFORMANCE / ENVIRONMENT / TOOLING / APPEND），逐段渲染：

| 占位符 | 渲染来源 | 可跳过（跳过时） |
|---|---|---|
| `{{LANG_HEADER}}` `{{OS_NAME}}` `{{MIRROR_LIST}}` `{{REFERENCE_DIR}}` `{{DEV_ROOT}}` `{{CODEBASE_MCP_DOCS}}` `{{CPU}}` `{{RAM}}` `{{GPU}}` `{{STORAGE}}` `{{HW_NOTES}}` `{{ENV_TABLE}}` | Phase 1 探测 + 作用域（全局/项目级） | —（探测驱动，无跳过） |
| `{{ART_STYLE_SUMMARY}}` | **Q3 美术问卷**：风格预设 / 自填种子（auto_palette）/ 跳过 | 跳过/未选 → 不落死色，正文写"命中视觉任务按 visualization.md 现场确立" |
| `{{PREFERENCES_SUMMARY}}` | Phase 4/0 偏好问卷摘要 | 可跳过 → 走默认偏好模板占位 |
| `install_picks` 部署计划 | **Q4 工具部署偏好** → `environment.md`「开发工具部署计划」 | 整项跳过 → 不写任何部署命令 |
| `visualization.md` | Q3 风格选择 / 自填种子生成 | 跳过 → 不生成 visualization.md |

> **铁律完整性（用户重点）**：性能档的 `PERFORMANCE` 段（动脑子/说人话/齐头并进/开源脱敏/codebase 图谱/多 Agent/测试卫生/踩坑/网络拓扑）**全文固写在模板正文，1:1 复用历史全量注入，不因问卷任何"跳过"而裁剪**。模板升级改的就是铁律内容本身，不是问卷选项。渲染命令以 `render-now.py --config questionnaire.json` 为准（问卷落 `questionnaire.json`）。

渲染与写入顺序：

1. **[性能档] 无脑铁律模式**：写 `AGENTS.md`（PERFORMANCE 段全量正文 + 问卷动态占位回填），再逐字复制到各 agent 镜像（CLAUDE.md / codex AGENTS.md / GEMINI.md，按 Phase 1 探测结果）+ 写 `agent-reference/preferences.md`（问卷全量 + 默认模板）
2. **RULES 段（经济/超轻档）** → 写通用 `AGENTS.md`，再逐字复制到各 agent 镜像（同上）
3. **ENVIRONMENT 段** → `agent-reference/environment.md`（探测画像 + Q4 部署计划）
4. **TOOLING 段** → `agent-reference/tooling.md`（图谱工具指南：CLI 速查/场景映射表/三层 fallback 状态机/反例/决策树，含 `{{DEV_ROOT}}` 与 `{{CODEBASE_MCP_DOCS}}` 渲染）；工具名一律按「功能」写参考名，并注明以当前实际部署 schema 为准
4'. **Q3 视觉** → 选中风格/自填种子时生成 `agent-reference/visualization.md`（泵基调 + 主/强调/背景/正文 + 语义渐变），并在注入正文回填 `{{ART_STYLE_SUMMARY}}`；跳过则不生成、正文写"未在问卷选择"
5. **APPEND 段** → 探测到 pi（`~/.pi` 或 `%USERPROFILE%\.pi`）时写 `.pi/agent/APPEND_SYSTEM.md`；同时把 `templates/graph-first-gate.ts` 复制到 `.pi/agent/extensions/`（已存在且 md5 不同时提示用户 diff 决定）；提示 `pi` 重启或 `/reload` 生效（**项目级不部署**）
6. **全产物检查**：每个写出的文件不允许残留任何 `{{`；镜像间 cmp 逐字一致（已确认 4 镜像 md5 相同）；network.md / type-map.md 等用户自建参考不生成、触发表自洽

### Phase 6: 写入 + 报告（含备份与分层增量）

1. 目标文件已存在 → 备份为 `<原名>.hostinit-bak.<YYYYmmddHHMMSS>` 再写入
2. 按三平台路径表写入（Linux/macOS/WSL 用 `$HOME/...`；Windows 原生用 `$env:USERPROFILE\...`；项目模式用 `./...`）
3. 输出报告：环境画像摘要 / **问卷选择回显（作用域/规格/美术/部署/偏好，含跳过项）** / 缺口清单（已装✓ 未装⚠）/ 各层产物写入位置 / pi 强化层部署状态 / 下一步建议

## 分层增量更新规则（产物已存在时）

- **规则主文档（AGENTS.md 及镜像）**：不覆盖用户本地修改；模板升级时提示 diff 由用户决定；镜像间不一致时以用户确认的版本为准重新对齐
- **environment.md**：整体覆写为最新探测结果（探测型数据无历史包袱）；用户手改的「个人开发偏好」小节保留
- **APPEND_SYSTEM.md / graph-first-gate.ts**：md5 与模板一致则跳过；不一致提示 diff 由用户决定
- **用户自建参考（network.md / visualization.md 等）与项目专属区**：绝不触碰

## 输出契约

- 分层注入体系一套：规则主文档 1-N 份镜像（逐字一致、无裸 `{{}}`）+ `agent-reference/environment.md` 与 `agent-reference/tooling.md` 各 1 份 + 性能档额外 `AGENTS.md` 全量正文 + `agent-reference/preferences.md`（问卷全量回报）+ pi 强化层（条件部署）
- 环境探测 JSON（可存 `~/.dev-host-profile.json` 供 dev-env-scan / code-debugger 复用）
- 缺口清单 + 安装状态 + 规格档位记录 + 下一步建议（跑 deploy 脚本装 skills、`/dev-env-scan` 建项目画像、`/ai-spec` 开始需求）

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | `/ai-spec init` 参数转交 |
| 输出供 | dev-env-scan | 宿主机画像作为项目画像基线 |
| 输出供 | code-debugger | 运行上下文预填（OS/硬件/代理） |
| 下游建议 | ai-spec | 初始化完成后进入需求主调度 |
