# 贡献指南 (CONTRIBUTING.md)

> **CodeForge** 是一个"社区开发引擎"——不仅欢迎你**改进脚手架本身**，更希望你**用它去开发别的开源项目**。这份文档教你怎么做喵～ φ(≧ω≦*)♪

**版本**: 1.0.0 · **License**: [BSL 1.1](./LICENSE) → 转 Apache 2.0 (2030-07-02) + [ETHICS.md](./ETHICS.md)

---

## 🌟 三条贡献路径

CodeForge 的贡献路径有点特别 —— 它同时是**被贡献的项目**和**用来贡献的工具**。

| 路径 | 说明 | 难度 |
|------|------|------|
| 🎯 **Path A — 用 CodeForge 贡献社区项目** | 接社区 issue / project 任务，用 CodeForge 让 Agent 完成开发 → PR | ⭐⭐ |
| 🐛 **Path B — 改进 CodeForge 本身** | 报 issue、优化 skill、加新 skill | ⭐ ~ ⭐⭐⭐ |
| 🤖 **Path C — Agent 自我优化** | 让正在用的 Agent 自己给 CodeForge 提 PR | ⭐⭐⭐ |

---

## 🎯 Path A — 用 CodeForge 贡献社区项目（推荐新人首选）

这是 CodeForge 存在的**核心价值**——让 AI Agent 帮社区消化 issue 与 project 任务。

### Step 1 · 部署 CodeForge 到 Codespace

**（如果你还没做过，先看主 README 的 [🚀 5 分钟上手](./README.md#-5-分钟上手) 章节。）**

三平台任选其一：

```bash
# 首次进入 Codespace 后（postCreateCommand 已自动跑）
claude    # 或 codex / gemini
```

### Step 2 · 挑一个 issue

访问社区 GitHub Projects，选一个标签为 `good first issue` / `help wanted` / `needs-agent` 的任务。

**📌 官方 Projects 面板**: https://github.com/orgs/PancrePal-xiaoyibao/projects

**当前热门开源项目 & 可挑 issue** 举例：

| 项目 | 领域 | 典型 issue |
|------|------|------------|
| [`osintel-pancrepal`](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal) | 胰腺癌开源情报 | [#3 生产版本发布](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal/issues/3) · [#6 时效性搜索](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal/issues/6) · [#7 非专业友好化](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal/issues/7) · [#8 视频整合](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal/issues/8) · [#9 胰腺中心信息库](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal/issues/9) · [#10 Mock audit](https://github.com/PancrePal-xiaoyibao/osintel-pancrepal/issues/10) |
| [`openpancan`](https://github.com/PancrePal-xiaoyibao/openpancan) | 胰腺癌数据库集成 | [Phase 1 COSMIC](https://github.com/PancrePal-xiaoyibao/openpancan/issues/6) · [Phase 2 TCGA-PAAD](https://github.com/PancrePal-xiaoyibao/openpancan/issues/7) · [Phase 3 OncoKB](https://github.com/PancrePal-xiaoyibao/openpancan/issues/8) · [Phase 4 STRING](https://github.com/PancrePal-xiaoyibao/openpancan/issues/9) · [Phase 5 GTEx](https://github.com/PancrePal-xiaoyibao/openpancan/issues/10) · [Phase 6 HPO](https://github.com/PancrePal-xiaoyibao/openpancan/issues/11) · [Phase 7 ClinicalTrials.gov](https://github.com/PancrePal-xiaoyibao/openpancan/issues/12) · [Phase 8 DGIdb](https://github.com/PancrePal-xiaoyibao/openpancan/issues/13) · [Phase 9 测试与文档](https://github.com/PancrePal-xiaoyibao/openpancan/issues/14) |
| [`VitaForge`](https://github.com/PancrePal-xiaoyibao/VitaForge) | AI4S 医学干实验引擎 | [#1 Rapid+Deep 双模式](https://github.com/PancrePal-xiaoyibao/VitaForge/issues/1) |
| [`.github`](https://github.com/PancrePal-xiaoyibao/.github) | 社区总览 & 跨项目 | [#5 小胰宝官网重构](https://github.com/PancrePal-xiaoyibao/.github/issues/5) · [#8 Agent 项目工程化](https://github.com/PancrePal-xiaoyibao/.github/issues/8) · [#9 四类子任务分工](https://github.com/PancrePal-xiaoyibao/.github/issues/9) · [#10 多场景测试](https://github.com/PancrePal-xiaoyibao/.github/issues/10) · [#11 AI4S 引擎融合](https://github.com/PancrePal-xiaoyibao/.github/issues/11) · [#12 knows-MCP QA](https://github.com/PancrePal-xiaoyibao/.github/issues/12) · [#13 Frontend UI/UX](https://github.com/PancrePal-xiaoyibao/.github/issues/13) · [#14 Agent 自我迭代](https://github.com/PancrePal-xiaoyibao/.github/issues/14) |

### Step 3 · 认领 issue

**认领方式：**

1. 在 issue 下评论：`我想接手这个任务，会用 CodeForge Agent 开发`。
2. 等维护者 assign 你（一般 24h 内）。避免撞车。
3. 或者用 GH CLI 一键操作：

```bash
gh issue comment <issue-url> --body "我想接手，会用 CodeForge Agent 开发。预计 X 天内提交 PR。"
```

### Step 4 · Fork + Clone 目标项目

```bash
# 在 Codespace 里（gh CLI 已装好）
gh auth login                                      # 首次登录 GitHub
gh repo fork PancrePal-xiaoyibao/openpancan --clone
cd openpancan

# 建特性分支（命名规范见下文）
git checkout -b feat/phase1-cosmic-integration
```

### Step 5 · 让 Agent 读 issue，生成开发计划

打开 CodeForge 的主入口（Claude / Codex / Gemini 都行）：

```
/ai-spec  帮我接下这个 issue：https://github.com/PancrePal-xiaoyibao/openpancan/issues/6
请：
1. 读一遍 issue 的完整内容与讨论。
2. 先跑 /dev-env-scan，扫这个 Fork 的技术栈。
3. 如果 issue 涉及外部数据源 / API / 领域知识，先 /deep-research 补齐上下文。
4. 用 /prd 生成结构化 PRD，落到 docs/prd/<issue-id>.md。
5. 输出实现计划：分成 3-5 个 user story，标注 API-First 拆分点。
6. 计划确认前不写代码。
```

### Step 6 · Agent 循环开发

计划确认后：

```
按刚才的计划开始实现。全程遵守 API-First：
- 每个 user story 走 /api-first
- 出现 bug 走 /codebase-context → /debug
- 前端相关走 /debug-ui / /ux-experience-audit
- 每完成一个 story 跑 /code-review

**重要**：不要 commit / push，我要人工 review。
```

**建议节奏喵～** (๑•̀ㅂ•́) 每个 story 完成后手动 review + 让 Agent 跑 `/code-review`，然后你自己再看一遍再合并到分支。

**大批量任务**（如 openpancan 有 9 个 Phase）可以：

```
/ralph-yolo  用 Ralph YOLO 模式循环实现刚才 PRD 里的所有 story。
每 story 完成后停下等我 review，通过再进下一个。
```

### Step 7 · 提交 PR

```bash
# 手动 review 通过后，让 Agent 帮你写 commit message
# （或者你自己写 conventional commit）
git add .
git commit -m "$(cat <<'EOF'
feat(phase1): integrate COSMIC CGC gene database

- Add COSMIC data fetcher with retry & rate limiting
- Expose /api/genes/cosmic endpoint
- Add integration tests for 5 known driver genes
- Docs: openapi.yaml updated

Closes #6

🤖 Generated with CodeForge (deep-research + ai-spec + api-first)
Co-Authored-By: Claude Code <noreply@anthropic.com>
EOF
)"
git push origin feat/phase1-cosmic-integration
```

用 GH CLI 一键开 PR：

```bash
gh pr create \
  --title "feat(phase1): integrate COSMIC CGC gene database" \
  --body "$(cat <<'EOF'
## 改动类型
- [x] ✨ 新功能

## Closes
Closes #6

## 改动说明
按 Phase 1 计划集成 COSMIC CGC 基因库，包含数据抓取、缓存、暴露 API、测试。

## AI 辅助披露
本 PR 使用 CodeForge 生成，主要 skill：
- `/deep-research` — 调研 COSMIC API 与 licensing
- `/ai-spec` + `/prd` — 生成 PRD 与实现规范
- `/api-first` — 按 API-First 拆分实现
- `/code-review` — 提交前审查

## 本地验证
- [x] 单元测试通过
- [x] 集成测试通过（5 个已知驱动基因）
- [x] `/code-review` 无 High 级问题

## Checklist
- [x] 遵循 API-First 分层
- [x] 更新 openapi.yaml
- [x] 添加/更新测试
- [x] AI 辅助已披露
EOF
)"
```

### Step 8 · 响应 review

维护者 review 时可能提问：

```
/debug  维护者说这里 <粘贴 review 评论> 有问题，帮我定位 + 修改。
```

修完 push 到同一分支即可，PR 会自动更新。

---

### 🧠 什么样的 issue 特别适合 Agent 干？

✅ **适合 Agent**：
- 明确的 API 集成任务（如 openpancan 的各 Phase）
- 数据源升级、字段变更、批处理
- 单元测试覆盖率提升
- 文档批量更新、README 修订
- 简单 UI 优化（有明确设计参考）
- 明确的重构任务（rename、抽公共函数）

⚠️ **需要人类主导，Agent 只做辅助**：
- 架构级决策（选新框架、重写核心模块）
- 涉及用户信任、隐私、支付的关键路径
- 需要新的产品判断（"这个功能应不应该做"）
- 高安全性代码（认证、加密、注入防御）

❌ **不适合 Agent 单独干**（人工必须主导）：
- 变更 License、CoC、组织治理
- 涉及生产密钥、数据库 schema 迁移
- 涉及未成年人 / 医疗 / 支付的合规变更

---

## 🐛 Path B — 改进 CodeForge 本身

### B.1 报 Issue

- **Bug** → 在 [CodeForge Issues](https://github.com/PancrePal-xiaoyibao/CodeForge/issues) 提交，标签 `bug`
- **新 skill 建议** → 标签 `enhancement`
- **文档 / typo** → 标签 `docs`

### B.2 优化现有 Skill / 新增 Skill

Fork → 特性分支 → 修改**三镜像**（`.claude/`、`.codex/`、`.gemini/`）→ PR。

**分支命名：**

| 类型 | 前缀 | 示例 |
|------|------|------|
| Bug | `fix/` | `fix/ai-spec-repo-init-missing` |
| 新功能 / 新 skill | `feat/` | `feat/skill-security-audit` |
| 文档 | `docs/` | `docs/readme-quickstart` |
| 重构 | `refactor/` | `refactor/route-table-cleanup` |

**优化 skill 的检查清单：**

- [ ] **三镜像同步** — `.claude/` + `.codex/` + `.gemini/` 三个版本同时修改（**最严格的规则**）
- [ ] **frontmatter 完整** — `name` + `description`，description 说明触发条件
- [ ] **关联 Skill 段** — 若改动影响 skill 间路由，更新相关 skill 关联段并保证双向一致
- [ ] **无死链** — `scripts/` `references/` 引用路径真实存在
- [ ] **入口文档同步** — `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` 三个入口的路由表 / 命令列表都要更
- [ ] **本地验证** — 在至少一个平台实际跑一遍该 skill

### B.3 新增 Skill 的标准结构

```
1. 写 Codex 源（真源）
   .codex/skills/<your-skill>/
   ├── SKILL.md          # frontmatter (name/description) + Overview/Workflow/Output Contract
   ├── agents/openai.yaml # display_name / short_description / default_prompt
   ├── scripts/          # 可选：.py/.ps1/.sh
   └── references/       # 可选：静态文档

2. 同步 Gemini 镜像
   .gemini/skills/<your-skill>/SKILL.md  (frontmatter: name + description)

3. 同步 Claude 镜像
   .claude/skills/<your-skill>.md 或 .claude/skills/<your-skill>/SKILL.md
   .claude/commands/<your-skill>.md      # slash command 入口

4. 更新入口文档
   CLAUDE.md / AGENTS.md / GEMINI.md 里的技能矩阵和路由表

5. 更新 README 的技能矩阵
```

---

## 🤖 Path C — Agent 自我优化闭环（最酷的玩法）

**场景**：你用 `/ai-spec` 时发现它没有按 API-First 拆分子任务。直接对 Agent 说：

```
/ai-spec 刚才没有按 API-First 拆分子任务，直接给了一坨代码。请：
1. 打开 .claude/skills/ai-spec.md 及三镜像，在 workflow 里强化：
   凡是涉及前后端的需求，必须先拆 backend API package → API doc → frontend 调用。
2. 同步改 .codex/skills/ai-spec/ 与 .gemini/skills/ai-spec/。
3. fork PancrePal-xiaoyibao/CodeForge，建分支 fix/ai-spec-enforce-api-first。
4. commit + gh pr create，PR 描述写清：现象、根因、三镜像 diff。
```

**一个 prompt，Agent 自动完成：改 skill → 三镜像同步 → fork → 分支 → commit → PR**。

---

## 🔀 Pull Request 通用规范

### Commit 信息

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat(scope): 新功能
fix(scope): bug 修复
docs(scope): 文档
refactor(scope): 重构（不改行为）
test(scope): 测试
chore(scope): 构建、CI、脚手架
```

**Scope 示例**：`ai-spec`、`deep-research`、`deploy`、`docs`、`api-first` 等。

### AI 辅助披露

**必填**：如果这次 PR 大部分工作是 AI 生成的，请在 PR 描述里写清楚使用了哪些 skill / Agent。示例：

```markdown
## AI 辅助披露
本 PR 使用 CodeForge 生成，主要 skill：
- `/deep-research` — 调研上游 API 变化
- `/ai-spec` — 生成实现规范
- `/api-first` — 后端封装
- `/code-review` — 提交前审查

人类审阅点：架构决策、安全边界、user-facing 文案。
```

### Review 标准

维护者会重点检查：
1. ✅ CodeForge 三镜像一致性（Path B/C）
2. ✅ ETHICS.md 合规（所有 Path）
3. ✅ AI 辅助披露完整（所有 Path）
4. ✅ description 触发条件清晰
5. ✅ 无死链、无格式错误
6. ✅ 与主入口文档的路由表一致

---

## 🤝 行为准则

- **友善** — 尊重所有贡献者，无论背景与水平。
- **透明** — AI 辅助生成的改动请在 PR 中披露。
- **人类主导** — Agent 是副驾驶，`commit` / `push` / `发布` 前必须人类明确授权（[ETHICS.md 第 3 节](./ETHICS.md#3-强制使用要求)）。
- **合规** — 遵守 [ETHICS.md](./ETHICS.md) 与所在地法律。

---

## 💬 沟通

- **Bug / 功能建议**: [GitHub Issues](https://github.com/PancrePal-xiaoyibao/CodeForge/issues)
- **社区总入口**: [PancrePal-xiaoyibao Projects](https://github.com/orgs/PancrePal-xiaoyibao/projects)
- **安全 / 伦理举报**: 见 [ETHICS.md 第 7 节](./ETHICS.md#7-举报与反馈)
- **大改动讨论**: 先开 Issue 讨论，再动手

---

*CodeForge 的进步，来自每一个像你这样：既写代码又教 Agent 写代码的贡献者喵～* (´｡• ᵕ •｡`) ♡
