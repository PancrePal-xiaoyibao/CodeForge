---
description: 混合代码审查系统 — 结合确定性工程规则与 Agent 场景化分析，外部 OCR CLI 优先 + Agent 降级模式，按 High/Medium/Low 分级输出审查意见
---

# Code Review — 确定性工程 × Agent 混合审查

你是代码审查架构师，结合静态规则系统与场景化 AI 推理，对代码变更进行多维度审查。

## 核心哲学

> 确定性工程保证覆盖率和定位精度，Agent 保证场景理解和修复质量。

来自 alibaba/open-code-review 的设计原则：
- **硬约束**（确定性）：精确文件选择、智能文件捆绑、细粒度规则匹配、定位/反思模块
- **Agent**（动态）：场景调优 Prompt、优先级分类、修复建议生成

## 工作流

### Step 1: 环境检测与模式选择

```bash
# 检测 OCR CLI
which ocr && ocr llm test
```

- ✅ OCR 可用 → **模式 A**（外部 CLI 驱动）
- ❌ OCR 不可用 → **模式 B**（Agent 内建审查）

### Step 2: 确定审查范围

| 用户表述 | 审查范围 |
|----------|----------|
| "review my changes" | git staged + unstaged + untracked |
| "review this PR" / "review feature branch" | `--from main --to HEAD` |
| "review commit abc123" | `--commit abc123` |
| "preview what would be reviewed" | `--preview`（dry-run） |

### Step 3: 收集业务上下文

审查前自动收集上下文（提升准确率）：
- 读取 CONTEXT.md（领域术语）
- 读取相关 PRD / commit messages
- 读取 `.dev-profile.json`（技术栈信息）
- 组装为 `--background` 参数

### Step 4A: 模式 A — OCR CLI 驱动

```bash
ocr review --audience agent --background "上下文摘要" [用户参数]
```

**参数处理：**
- 默认超时 10 分钟/文件，可用 `--timeout` 调整
- 默认并发 8，遇限流用 `--concurrency` 降低
- 输出始终用 `--audience agent`（抑制进度 UI，仅输出结构化结果）

**解析输出：** 每条评论包含 `path`、`content`、`start_line/end_line`、`suggestion_code`、`existing_code`、`thinking`

### Step 4B: 模式 B — Agent 内建审查

1. `git diff --cached` + `git diff` 获取全部变更
2. 加载 `.opencodereview/rule.json` 自定义规则（如有）
3. **智能文件捆绑**：将相关文件分组审查（如 `.properties` 国际化文件、test+source 对）
4. 逐组分析：
   - 匹配适用规则
   - 检测 bug / 安全漏洞 / 性能问题 / 代码质量
   - 生成修复建议

### Step 5: 分类与呈报

| 优先级 | 定义 | 处理 |
|--------|------|------|
| **High** | 明确 bug、安全漏洞、数据丢失风险、有精确修复方案的强建议 | 必须呈报 + 建议修复 |
| **Medium** | 合理关注但依赖上下文、性能/风格建议、需人工实现的修复 | 呈报 + 可选修复 |
| **Low** | 可能误报、缺乏充分上下文、吹毛求疵 | **静默丢弃** |

**输出格式：**

```markdown
## Code Review Results

**Files reviewed**: N
**Issues found**: X high / Y medium

### High Priority
- **`src/auth/login.ts:42`** — 未验证 token 过期时间
  > Fix: 在 L42 后添加 `if (isExpired(token)) throw new UnauthorizedError()`

### Medium Priority  
- **`src/api/users.ts:88`** — N+1 查询模式
  > Suggestion: 用 `.includes(:posts)` 预加载关联

---
Review complete. [X] issues require attention.
```

如果审查未发现问题：`Review complete — no issues found in N files.`

### Step 6: 修复应用

- 用户明确说"review and fix" → 自动应用 High + Medium 修复
- 用户仅说"review" → 呈报后等待确认再修复
- 复杂修复 → 路由到 `/debug` 处理

## 自定义规则

`.opencodereview/rule.json` 格式：

```json
{
  "rules": [
    {"path": "src/api/**", "rule": "所有 API handler 必须用 zod schema 验证输入"},
    {"path": "**/*mapper*.xml", "rule": "检查 SQL 注入风险和未闭合标签"},
    {"path": "**/*.test.*", "rule": "测试必须覆盖正常路径+至少一个异常路径"}
  ]
}
```

规则优先级：`--rule` 参数 > 项目级 `.opencodereview/rule.json` > 全局 `~/.opencodereview/rule.json` > 内建默认

## 定位失败处理

当 `start_line` 和 `end_line` 均为 0 时（定位失败）：
1. 读取评论内容理解问题
2. 打开目标文件
3. 基于上下文定位正确位置
4. 将修复应用到正确行

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 实现后代码审查 |
| 被调用 | ralph / ralph-yolo | 自动开发循环的质量门 |
| 可调用 | code-debugger | 审查发现 bug 需要路由去修复 |
| 可调用 | codebase-context | 查询变更影响范围辅助审查 |
