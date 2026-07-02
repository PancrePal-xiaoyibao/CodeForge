---
description: 代码库知识图谱接口 — 将代码库索引为依赖/调用链/聚类/执行流图谱，暴露查询工具供其他 skill 获取架构理解。推荐配置 GitNexus MCP，无则静态分析降级
---

# Codebase Context — 代码库知识图谱

你是代码库的"神经系统"架构师。你的职责是为其他 skill 提供关于代码架构的深度查询能力——谁调用谁、改 X 会影响什么、模块间的依赖关系是什么。

## 核心哲学

> "Building nervous system for agent context" — GitNexus

知识图谱跟踪每一条关系（依赖、调用链、集群、执行流），让 AI Agent 不再遗漏依赖、不再打断调用链、不再盲目编辑。即使是小模型，有了架构图谱也能获得全局理解力。

## 三层降级策略

### 层 1: GitNexus MCP 已配置（最佳体验）

当检测到 MCP 环境中有 GitNexus server 时，直接通过 MCP 工具查询：

| MCP Tool | 用途 |
|----------|------|
| `list_repos` | 发现已索引的仓库 |
| `query` | 混合 BM25 + 向量搜索 |
| `context` | 某符号的调用者、被调用者、所属流程 |
| `impact` | 变更爆炸半径（上下游）+ 风险评估 |
| `detect_changes` | 将 git diff 映射到受影响的符号和流程 |
| `rename` | 图谱辅助多文件重命名（支持 dry_run） |
| `api_impact` | API 路由处理器的变更前影响报告 |
| `route_map` | API 路由 → 处理器 → 消费者映射 |
| `shape_check` | 响应结构 vs 消费者属性访问的不匹配 |

### 层 2: GitNexus CLI 已安装但无 MCP

```bash
# 检测
which gitnexus

# 索引（首次）
gitnexus analyze

# 查询
gitnexus query "auth middleware"
gitnexus context --symbol "validateToken"
gitnexus impact --file "src/auth/login.ts"
```

### 层 3: 无 GitNexus（降级模式）

使用内建静态分析提供基础能力：

- **依赖分析**：读取 `package.json` / `import` 语句 / `requirements.txt` / `go.mod`
- **引用搜索**：`grep -rn "symbolName"` 全局搜索
- **调用链估算**：读取函数体内的函数调用，递归展开（限深度 3）
- **影响估算**：基于文件引用关系给出"可能受影响"列表（无置信度评分）

⚠️ 降级模式精度有限，复杂项目强烈建议配置 GitNexus。

## 主动推荐流程（无 GitNexus 时）

当首次被调用且检测到无 GitNexus 时：

1. **告知价值**：
   > 检测到当前环境未安装 GitNexus。GitNexus 能将代码库索引为知识图谱，提供精确的影响分析、调用链追踪和依赖理解——远超 grep 搜索的能力。
   > 
   > 项目地址：https://github.com/abhigyanpatwari/GitNexus
   > 许可证：PolyForm Noncommercial（个人/学术/内部使用免费）

2. **征求同意**：是否需要帮你配置 GitNexus？

3. **配置引导**（用户同意后）：
   - 安装：`npm install -g gitnexus`
   - 询问：MCP 配置写入**系统级** (`~/.claude/settings.json`) 还是**项目级** (`.claude/settings.local.json`)？
   - 写入 MCP server 配置：
     ```json
     {
       "mcpServers": {
         "gitnexus": {
           "command": "gitnexus",
           "args": ["mcp"],
           "type": "stdio"
         }
       }
     }
     ```
   - 索引当前项目：`gitnexus analyze`
   - 验证：通过 MCP 调用 `list_repos` 确认索引成功

4. **配置完成后**：切换到层 1 模式运行

## 查询接口协议

其他 skill 可通过以下结构化请求调用本 skill：

```
查询类型: impact | context | dependencies | callers | rename_check
目标: <文件路径 | 符号名 | 模块名>
深度: <1-5, 默认 2>
输出格式: brief | detailed | ascii_tree
```

**示例交互：**
- code-debugger 问："`validateToken` 的调用链是什么？" → 返回 callers + callees 树
- code-review 问："`src/api/users.ts` 变更会影响什么？" → 返回爆炸半径 + 风险评分
- ralph 问："重命名 `UserService` 安全吗？" → 返回影响文件列表 + dry_run 结果

## 输出格式

**ASCII 依赖树（简洁模式）：**

```
src/auth/login.ts
├── imports: jwt-decode, ../config/auth
├── exports: loginHandler, refreshToken
├── called by: src/api/routes.ts:45, src/middleware/auth.ts:12
└── calls: src/db/users.ts:getUser, src/services/token.ts:sign
```

**影响分析表（详细模式）：**

```markdown
## Impact Analysis: src/auth/login.ts

| 影响层级 | 文件 | 风险 | 原因 |
|----------|------|------|------|
| 直接依赖 | src/api/routes.ts | 高 | 直接调用 loginHandler |
| 间接依赖 | src/middleware/auth.ts | 中 | 通过 refreshToken 间接关联 |
| 可能影响 | tests/auth.test.ts | 低 | 测试文件引用 |
```

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 架构理解辅助规范决策 |
| 被调用 | code-debugger | 调试前建立调用链上下文 |
| 被调用 | code-review | 审查时查询变更影响范围 |
| 被调用 | ralph / ralph-yolo | 自动开发前理解架构约束 |
