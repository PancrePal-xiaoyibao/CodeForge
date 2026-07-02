# 🇨🇳 国内 API 供应商配置指南

> 让国内开发者用 **Claude Code** + **国产大模型 API** 完成 CodeForge 全流程开发喵～ (๑•̀ㅂ•́) ✧

**适用对象**：国内开发者、被 Anthropic 官方 API 访问受限的用户、希望用国产模型降本增效的团队。

**核心原理**：Claude Code 支持通过 `ANTHROPIC_BASE_URL` 环境变量把请求指向兼容 Anthropic API 协议的第三方供应商。国内主流大模型（智谱 GLM、DeepSeek、Kimi、小米 MiMo 等）都提供了 Anthropic 兼容端点，配一下环境变量就能用。

---

## 📋 前置准备

1. **安装 Claude Code**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. **注册 API Key**（选一家或多家）：见下方各供应商小节的申请链接。
3. **打开一个终端**（PowerShell / CMD / Git Bash / macOS Terminal / Linux Bash）。

---

## 🎯 快速选型

| 供应商 | 主打模型 | 上下文 | 特点 | 推荐场景 |
|--------|---------|--------|------|---------|
| **智谱 GLM** | glm-5.2[1m] / glm-5.1 | 1M | 当前国产最强 Coding 模型（对标 Claude Sonnet 4.6） | 大型项目 / Agent 编程首选 |
| **DeepSeek** | deepseek-v4-pro / flash | 1M | 极致性价比、代码能力顶级 | 大批量代码生成、Ralph 循环 |
| **Kimi K2.7-Code** | kimi-k2.7-code | 256K | 开源 1T MoE，30% 更少思考 token，$0.95/$4/M | 长循环 Agent 编程 |
| **小米 MiMo** | mimo-v2.5-pro[1m] / v2.5[1m] | 1M | 小米生态整合，1M 上下文 | 端云一体开发 |
| **硅基流动** | 多家聚合 | 视模型 | 一个 Key 通多家 | 试模型、切换成本低 |
| **中转 Claude** | claude-opus-4-6 / sonnet-4-6 | 1M | 原厂能力 | 品质优先、预算充足 |

> 💡 **建议**：先用 **DeepSeek** 或 **智谱 GLM** 起步（性价比高、注册便捷），熟悉 CodeForge 工作流后再按项目切换。

---

## 🔧 配置模板

**📌 通用规则**：Claude Code 读四个核心环境变量：
- `ANTHROPIC_BASE_URL` — 供应商端点
- `ANTHROPIC_AUTH_TOKEN` — 你的 API Key
- `ANTHROPIC_MODEL` — 主力模型（复杂任务）
- `ANTHROPIC_SMALL_FAST_MODEL` — 快速小模型（简单任务、摘要等）

配完启动：`claude --permission-mode bypassPermissions`（bypass 模式跳过多数确认，适合 CodeForge 已内置人在回路约束的场景；对细粒度控制敏感的团队可以去掉该 flag）。

---

### 1️⃣ DeepSeek（推荐新人首选：性价比极高）

**申请 Key**：<https://platform.deepseek.com/>

**Linux / macOS (bash / zsh)**：
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=your-API-key
export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-v4-flash[1m]
claude --permission-mode bypassPermissions
```

**Windows PowerShell**：
```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="your-API-key"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_SMALL_FAST_MODEL="deepseek-v4-flash[1m]"
claude --permission-mode bypassPermissions
```

**Windows CMD**：
```cmd
set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
set ANTHROPIC_AUTH_TOKEN=your-API-key
set ANTHROPIC_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_SMALL_FAST_MODEL=deepseek-v4-flash[1m]
claude --permission-mode bypassPermissions
```

---

### 2️⃣ 智谱 GLM（国产旗舰 · Coding 能力最强 · 1M 上下文）

**申请 Key**：
- 🇨🇳 境内入口：<https://open.bigmodel.cn/>（bigmodel MaaS 平台，支持 GLM Coding Plan 订阅）
- 🌏 海外入口：<https://z.ai/>（z.ai 是智谱海外站，包含 Coding Plan 页 `https://z.ai/subscribe`）

**最新旗舰模型**：`glm-5.2[1m]`（1M 上下文，Coding 能力对标 Claude Sonnet 4.6，是当前国产最强 coding 模型喵～）。
辅助快速模型：`glm-5.1`（可用于低延迟摘要 / 快问快答）。

**⚠️ 重要**：要真正启用 GLM 5.2 的 **1M 上下文**，模型名必须带 `[1m]` 后缀，同时设置 `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`，否则 Claude Code 会用默认压缩窗口，等于白开长上下文喵。

#### 方式 A · 环境变量（Codespace / 临时会话推荐）

**Linux / macOS / Codespace**：
```bash
export ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
export ANTHROPIC_AUTH_TOKEN=your-API-key
export ANTHROPIC_MODEL="glm-5.2[1m]"
export ANTHROPIC_SMALL_FAST_MODEL=glm-5.1
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000
export API_TIMEOUT_MS=3000000
claude --permission-mode bypassPermissions
```

**Windows PowerShell**：
```powershell
$env:ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="your-API-key"
$env:ANTHROPIC_MODEL="glm-5.2[1m]"
$env:ANTHROPIC_SMALL_FAST_MODEL="glm-5.1"
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1000000"
$env:API_TIMEOUT_MS="3000000"
claude --permission-mode bypassPermissions
```

**Windows CMD**：
```cmd
set ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
set ANTHROPIC_AUTH_TOKEN=your-API-key
set ANTHROPIC_MODEL=glm-5.2[1m]
set ANTHROPIC_SMALL_FAST_MODEL=glm-5.1
set CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000
set API_TIMEOUT_MS=3000000
claude --permission-mode bypassPermissions
```

#### 方式 B · `~/.claude/settings.json`（Claude Code 官方推荐 · 持久生效）

编辑 `~/.claude/settings.json`（不存在就新建），加入：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-API-key",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-5.1",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.2[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.2[1m]"
  }
}
```

保存后重开 `claude` 即可生效。在 Claude Code 里输 `/status` 可以看到实际调用的是 GLM。想切换推理力度用 `/effort`。

> 📌 **官方文档**：<https://docs.z.ai/devpack/tool/claude>（含最新模型清单、切换指南、GLM Coding Plan 计费说明）。
>
> 💡 **境内 vs 海外端点**：`api.z.ai/api/anthropic` 是当前官方文档主推端点，境内境外都能访问；老的 `open.bigmodel.cn/api/anthropic` 端点仍可用，但新特性（如 5.2、1M 上下文的 mapping）以 z.ai 文档为准。境内用户如果 z.ai 访问慢，可以试用 bigmodel 端点。


---

### 3️⃣ Kimi K2.7-Code（Moonshot · 开源 1T MoE Coding 模型）

**申请 Key**：
- 🇨🇳 境内入口：<https://kimi.com/>（Kimi Code 平台，Coding 专用 Key）
- 官方文档：<https://platform.kimi.ai/docs/guide/agent-support>

**最新旗舰模型**：`kimi-k2.7-code`（2026-06-12 发布，1T 总参数 / 32B 激活的 MoE Coding 模型，**256K 上下文**，思考 token 比 K2.6 减少约 30%，在 MCP Mark Verified 上得分 81.1，超过 Claude Opus 4.8 的 76.4）。

**⚠️ 端点变更**：老的 `api.moonshot.cn/anthropic` 端点在 Kimi Code 平台的 `sk-kimi-` Key 下会返回 401，请使用新端点 **`https://api.kimi.com/coding/`**。上下文窗口 256K（262144），需要匹配 `CLAUDE_CODE_AUTO_COMPACT_WINDOW=262144`。

**Linux / macOS / Codespace**：
```bash
export ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
export ANTHROPIC_AUTH_TOKEN=your-kimi-API-key
export ANTHROPIC_MODEL=kimi-k2.7-code
export ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2.7-code
export ANTHROPIC_DEFAULT_SONNET_MODEL=kimi-k2.7-code
export ANTHROPIC_DEFAULT_HAIKU_MODEL=kimi-k2.7-code
export CLAUDE_CODE_SUBAGENT_MODEL=kimi-k2.7-code
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=262144
export ENABLE_TOOL_SEARCH=false
claude --permission-mode bypassPermissions
```

**Windows PowerShell**：
```powershell
$env:ANTHROPIC_BASE_URL="https://api.kimi.com/coding/"
$env:ANTHROPIC_AUTH_TOKEN="your-kimi-API-key"
$env:ANTHROPIC_MODEL="kimi-k2.7-code"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k2.7-code"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k2.7-code"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k2.7-code"
$env:CLAUDE_CODE_SUBAGENT_MODEL="kimi-k2.7-code"
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="262144"
$env:ENABLE_TOOL_SEARCH="false"
claude --permission-mode bypassPermissions
```

**Windows CMD**：
```cmd
set ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
set ANTHROPIC_AUTH_TOKEN=your-kimi-API-key
set ANTHROPIC_MODEL=kimi-k2.7-code
set ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2.7-code
set ANTHROPIC_DEFAULT_SONNET_MODEL=kimi-k2.7-code
set ANTHROPIC_DEFAULT_HAIKU_MODEL=kimi-k2.7-code
set CLAUDE_CODE_SUBAGENT_MODEL=kimi-k2.7-code
set CLAUDE_CODE_AUTO_COMPACT_WINDOW=262144
set ENABLE_TOOL_SEARCH=false
claude --permission-mode bypassPermissions
```

> 📌 **官方 Anthropic 兼容说明**：<https://platform.kimi.ai/docs/guide/agent-support>
>
> 💡 K2.7-Code 上下文是 **256K 而不是 1M**，但通过 30% 更低的思考 token + $0.95/$4.00 per M tokens 的极低单价，在长循环 Agent 任务里性价比依然突出。

---

### 4️⃣ 小米 MiMo v2.5 · 1M 上下文（Xiaomi）

**申请 Key**：见小米开放平台文档。

**最新模型**：`mimo-v2.5-pro[1m]` / `mimo-v2.5[1m]`（**1M 上下文**，模型名带 `[1m]` 后缀才能真正启用长上下文）。

**⚠️ 重要**：和 GLM 一样，1M 上下文需要 `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`。

**Linux / macOS / Codespace**：
```bash
export ANTHROPIC_BASE_URL=https://token-plan-cn.xiaomimimo.com/anthropic
export ANTHROPIC_AUTH_TOKEN=your-API-key
export ANTHROPIC_MODEL="mimo-v2.5-pro[1m]"
export ANTHROPIC_SMALL_FAST_MODEL="mimo-v2.5[1m]"
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000
claude --permission-mode bypassPermissions
```

**Windows PowerShell**：
```powershell
$env:ANTHROPIC_BASE_URL="https://token-plan-cn.xiaomimimo.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="your-API-key"
$env:ANTHROPIC_MODEL="mimo-v2.5-pro[1m]"
$env:ANTHROPIC_SMALL_FAST_MODEL="mimo-v2.5[1m]"
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1000000"
claude --permission-mode bypassPermissions
```

**Windows CMD**：
```cmd
set ANTHROPIC_BASE_URL=https://token-plan-cn.xiaomimimo.com/anthropic
set ANTHROPIC_AUTH_TOKEN=your-API-key
set ANTHROPIC_MODEL=mimo-v2.5-pro[1m]
set ANTHROPIC_SMALL_FAST_MODEL=mimo-v2.5[1m]
set CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000
claude --permission-mode bypassPermissions
```

---

### 5️⃣ 硅基流动（SiliconFlow · 多模型聚合）

**申请 Key**：<https://cloud.siliconflow.cn/>

硅基流动提供一键脚本自动完成配置，支持在多家开源大模型间切换：

```bash
bash -c "$(curl -fsSL https://static01.siliconflow.cn/cdn/assets/claude_code_with_siliconcloud_install_0716.sh)"
```

运行后按提示：
1. 粘贴你的 SiliconCloud API Key
2. 用方向键选要在 Claude Code 中使用的模型

**目前支持的非思考模型**（更多模型陆续接入）：
- `Pro/moonshotai/Kimi-K2-Instruct`
- `moonshotai/Kimi-K2-Instruct`
- `Pro/deepseek-ai/DeepSeek-V3`
- `deepseek-ai/DeepSeek-V3`
- `moonshotai/Kimi-Dev-72B`
- `baidu/ERNIE-4.5-300B-A47B`

**官方文档**：<https://docs.siliconflow.cn/cn/usercases/use-siliconcloud-in-ClaudeCode>

---

### 6️⃣ 中转 Claude（第三方 Anthropic 中转，用原生 Claude 能力）

> ⚠️ **风险提示**：中转服务的合规性、日志留存、Key 泄露风险差异很大。请选择长期口碑良好、有明确 SLA 的服务商，并且**不要把生产密钥、生产数据发给未经审计的中转**。

**Linux / macOS**：
```bash
export ANTHROPIC_BASE_URL=https://api.xxxxx.com     # 换成你的中转地址
export ANTHROPIC_AUTH_TOKEN=your-API-key
export ANTHROPIC_MODEL=claude-opus-4-6[1m]
export ANTHROPIC_SMALL_FAST_MODEL=claude-sonnet-4-6[1m]
claude --permission-mode bypassPermissions
```

**Windows PowerShell**：
```powershell
$env:ANTHROPIC_BASE_URL="https://api.xxxxx.com"
$env:ANTHROPIC_AUTH_TOKEN="your-API-key"
$env:ANTHROPIC_MODEL="claude-opus-4-6[1m]"
$env:ANTHROPIC_SMALL_FAST_MODEL="claude-sonnet-4-6[1m]"
claude --permission-mode bypassPermissions
```

**Windows CMD**：
```cmd
set ANTHROPIC_BASE_URL=https://api.xxxxx.com
set ANTHROPIC_AUTH_TOKEN=your-API-key
set ANTHROPIC_MODEL=claude-opus-4-6[1m]
set ANTHROPIC_SMALL_FAST_MODEL=claude-sonnet-4-6[1m]
claude --permission-mode bypassPermissions
```

---

## 💡 持久化配置技巧

上面的命令**每次开终端都要重跑**。想一次配好长期用：

### Linux / macOS — 写进 `~/.bashrc` / `~/.zshrc`

```bash
# ============ CodeForge · DeepSeek ============
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=your-API-key
export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-v4-flash[1m]
```

然后 `source ~/.bashrc` 或重开终端。

### Windows PowerShell — 写进 `$PROFILE`

打开 PowerShell 执行：
```powershell
notepad $PROFILE
```

（若文件不存在，先跑 `New-Item -Path $PROFILE -Type File -Force`）

在文件里加：
```powershell
# ============ CodeForge · GLM ============
$env:ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="your-API-key"
$env:ANTHROPIC_MODEL="glm-5.2[1m]"
$env:ANTHROPIC_SMALL_FAST_MODEL="glm-5.1"
$env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1000000"
```

保存后重开 PowerShell 生效。

### Windows CMD — 用系统环境变量

`Win + R` → `sysdm.cpl` → 高级 → 环境变量 → 新建 4 个用户变量（不推荐；PowerShell 或 WSL 是更好的路径）。

---

## 🔀 一键切换供应商（推荐方案）

写个 shell 函数或 PowerShell 函数，一秒切换：

### Linux / macOS — 加到 `~/.bashrc` / `~/.zshrc`

```bash
cf-deepseek() {
  export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
  export ANTHROPIC_AUTH_TOKEN=$DEEPSEEK_KEY
  export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
  export ANTHROPIC_SMALL_FAST_MODEL=deepseek-v4-flash[1m]
  echo "✅ Claude Code switched to DeepSeek"
}
cf-glm() {
  export ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
  export ANTHROPIC_AUTH_TOKEN=$GLM_KEY
  export ANTHROPIC_MODEL="glm-5.2[1m]"
  export ANTHROPIC_SMALL_FAST_MODEL=glm-5.1
  export CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000
  echo "✅ Claude Code switched to GLM 5.2 (1M ctx)"
}
cf-kimi() {
  export ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
  export ANTHROPIC_AUTH_TOKEN=$KIMI_KEY
  export ANTHROPIC_MODEL=kimi-k2.7-code
  export ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2.7-code
  export ANTHROPIC_DEFAULT_SONNET_MODEL=kimi-k2.7-code
  export ANTHROPIC_DEFAULT_HAIKU_MODEL=kimi-k2.7-code
  export CLAUDE_CODE_AUTO_COMPACT_WINDOW=262144
  export ENABLE_TOOL_SEARCH=false
  echo "✅ Claude Code switched to Kimi K2.7-Code (256K ctx)"
}
cf-mimo() {
  export ANTHROPIC_BASE_URL=https://token-plan-cn.xiaomimimo.com/anthropic
  export ANTHROPIC_AUTH_TOKEN=$MIMO_KEY
  export ANTHROPIC_MODEL="mimo-v2.5-pro[1m]"
  export ANTHROPIC_SMALL_FAST_MODEL="mimo-v2.5[1m]"
  export CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000
  echo "✅ Claude Code switched to Xiaomi MiMo v2.5 (1M ctx)"
}
```

再把 `DEEPSEEK_KEY` / `GLM_KEY` / `KIMI_KEY` / `MIMO_KEY` 放到 `~/.bashrc` 或专门的 `~/.secrets.env` 里（**记得 chmod 600 并加入 .gitignore**）。

用起来：`cf-deepseek && claude` 或 `cf-glm && claude`。

### PowerShell — 加到 `$PROFILE`

```powershell
function cf-deepseek {
  $env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
  $env:ANTHROPIC_AUTH_TOKEN=$env:DEEPSEEK_KEY
  $env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
  $env:ANTHROPIC_SMALL_FAST_MODEL="deepseek-v4-flash[1m]"
  Write-Host "✅ Claude Code switched to DeepSeek" -ForegroundColor Green
}
function cf-glm {
  $env:ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
  $env:ANTHROPIC_AUTH_TOKEN=$env:GLM_KEY
  $env:ANTHROPIC_MODEL="glm-5.2[1m]"
  $env:ANTHROPIC_SMALL_FAST_MODEL="glm-5.1"
  $env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1000000"
  Write-Host "✅ Claude Code switched to GLM 5.2 (1M ctx)" -ForegroundColor Green
}
function cf-kimi {
  $env:ANTHROPIC_BASE_URL="https://api.kimi.com/coding/"
  $env:ANTHROPIC_AUTH_TOKEN=$env:KIMI_KEY
  $env:ANTHROPIC_MODEL="kimi-k2.7-code"
  $env:ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k2.7-code"
  $env:ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k2.7-code"
  $env:ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k2.7-code"
  $env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="262144"
  $env:ENABLE_TOOL_SEARCH="false"
  Write-Host "✅ Claude Code switched to Kimi K2.7-Code (256K ctx)" -ForegroundColor Green
}
function cf-mimo {
  $env:ANTHROPIC_BASE_URL="https://token-plan-cn.xiaomimimo.com/anthropic"
  $env:ANTHROPIC_AUTH_TOKEN=$env:MIMO_KEY
  $env:ANTHROPIC_MODEL="mimo-v2.5-pro[1m]"
  $env:ANTHROPIC_SMALL_FAST_MODEL="mimo-v2.5[1m]"
  $env:CLAUDE_CODE_AUTO_COMPACT_WINDOW="1000000"
  Write-Host "✅ Claude Code switched to Xiaomi MiMo v2.5 (1M ctx)" -ForegroundColor Green
}
```

用起来：`cf-deepseek; claude`。

---

## ✅ 配置成功验证

```bash
# 环境变量已生效
echo $ANTHROPIC_BASE_URL       # Linux/macOS/Git Bash
$env:ANTHROPIC_BASE_URL        # PowerShell

# 启动 Claude Code
claude --permission-mode bypassPermissions

# 在 Claude Code 里输入
> /model
# 应该显示当前使用的模型名（如 deepseek-v4-pro[1m]）

# 试一个简单命令
> /ai-spec 帮我起一个 hello world 项目
# 有响应说明配置成功喵～
```

---

## ⚠️ 常见问题

### Q1: 环境变量设了但 Claude Code 不生效？
**A**: 检查环境变量是否**在启动 claude 的同一个 shell 会话里**设置。**关键**：设完变量后再启动 `claude`，而不是相反顺序。PowerShell 用户注意变量作用域（`$env:` 是当前进程级）。

### Q2: 报 `401 Unauthorized`？
**A**: API Key 错了 / 过期了 / 没充值。到对应平台控制台重新生成 Key，注意粘贴时不要有多余空格或换行。

### Q3: 报 `model not found`？
**A**: 供应商的模型名可能更新过，去对应文档查最新的模型 ID。或者尝试去掉 `[1m]` 上下文后缀。

### Q4: 想用 CodeForge 的 skill 但不确定国产模型能否驱动？
**A**: CodeForge 的所有 skill 是 **prompt 层配置**，与底层模型解耦。任何 Claude API 兼容供应商都能跑。**实测**：DeepSeek-V4-Pro、GLM-5.2[1m]、Kimi-K2.7-Code、小米 MiMo v2.5-pro[1m] 都能顺畅跑 `/ai-spec` `/deep-research` `/api-first` 全流程。

### Q5: `--permission-mode bypassPermissions` 是啥？安全吗？
**A**: Claude Code 的一个启动 flag，跳过多数交互确认。**CodeForge 内部的 skill 已内置人在回路约束**（commit/push 前必须人工授权），所以 bypass 对 CodeForge 工作流影响不大。若你在通用场景需要更严格的每步确认，去掉该 flag 用默认交互模式即可。

### Q6: 我在 GitHub Codespace 里用可以吗？
**A**: 完全可以喵～ 在 Codespace 终端里 `export` 环境变量后启动 `claude`。国内供应商在 Codespace（境外）访问速度也很不错。

### Q7: 团队协作时怎么共享配置？
**A**: **不要把 API Key 提交到 git**。推荐做法：
1. 把切换函数（不含 Key）加到项目的 `docs/env-switch.sh` 或 `docs/env-switch.ps1`
2. Key 放到每人自己的 `~/.secrets.env`（记得 `.gitignore` 加白）
3. 或用团队级密钥管理（Doppler、1Password CLI、GitHub Codespace Secrets 等）

---

## 🌏 国内网络优化

- **DNS**：国内 API 端点建议用 `223.5.5.5`（阿里）或 `119.29.29.29`（腾讯）
- **Codespace 用户**：Codespace 在 Azure 境外区，访问国内 API 速度取决于跨境线路，一般 100–300ms 可接受
- **本地 Windows**：无需魔法，国产 API 本地直连即可
- **本地 macOS/Linux**：同上

---

## 💰 成本参考（2026-07 · 大约值）

| 供应商 | 输入 | 输出 | 备注 |
|--------|------|------|------|
| DeepSeek V4 Pro | ~¥1/M tokens | ~¥8/M tokens | 极致性价比，Ralph 循环首选 |
| GLM-5.2[1m] (Coding Plan) | 起步 ~¥20/月 订阅 | 起步 ~¥20/月 订阅 | 1M 上下文，性价比之王 |
| Kimi K2.7-Code | ~$0.95/M tokens | ~$4.00/M tokens | 开源，256K 上下文，思考 token 少 30% |
| 小米 MiMo v2.5 | 视订阅计划 | 视订阅计划 | 1M 上下文，小米生态 |
| Claude Opus 4 (中转) | ~¥20/M tokens | ~¥100/M tokens | 顶级质量 |

> 数据随时会变，请以各家官网最新价格为准。

---

## 🧭 与 CodeForge 工作流的配合

**读完这份指南后，回到主流程**：

1. 装好 Claude Code：`npm i -g @anthropic-ai/claude-code`
2. 按本指南配好国内供应商环境变量
3. 启动：`claude --permission-mode bypassPermissions`
4. 在 Claude Code 会话里贴 **[CodeForge 一句话部署 prompt](../README.md#step-4--一句话部署-codeforge-到-agent-环境)**
5. 然后按 [新手完整工作流](../README.md#-新手开发者-15-分钟第一次贡献) 接社区 issue → Agent 完成闭环

**祝主人和社区其他开发者们都能用起国产 API + CodeForge 高效贡献开源喵～** (´｡• ᵕ •｡`) ♡

---

## 📞 反馈与贡献

- 发现新的兼容供应商 / 模型 → 欢迎提 PR 补充到本文档
- 配置踩坑 → 到 [CodeForge Issues](https://github.com/PancrePal-xiaoyibao/CodeForge/issues) 反馈
- 相关话题：`docs`, `chinese-providers`, `claude-code-config`
