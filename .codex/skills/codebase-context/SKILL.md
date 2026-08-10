---
name: codebase-context
description: 代码库知识图谱接口 — 将代码库索引为依赖/调用链/聚类/执行流图谱，暴露查询工具供其他 skill 获取架构理解。优先使用 codebase-memory MCP 图谱（search_graph / trace_path / query_graph / get_architecture），无 MCP 时降级 GitNexus，再降级静态分析。触发词：探索代码库、理解架构、谁调用了 X、X 调用了什么、调用链、影响分析、依赖分析、死代码、高扇出、重构候选、Cypher 查询、跨服务调用。
---

# Codebase Context — 代码库"神经系统"架构师

为其他 skill 提供深度架构查询。图谱工具一次返回精确结构结果（~500 tokens），大范围 grep 同样问题要 ~80K tokens。

## 三层降级

1. **codebase-memory MCP 图谱**（首选）— 已部署 codebase-memory-mcp 时使用，`mcp__codebase-memory-mcp__*` 工具可用
2. **GitNexus MCP/CLI** — 无 codebase-memory 时使用，`gitnexus mcp`
3. **内建静态分析** — 两者皆无时使用，并主动推荐配置

## 安装 codebase-memory MCP（首选路径）

```bash
# 1. 安装（任意其一）
npm install -g codebase-memory-mcp        # npm 版
pip install codebase-memory-mcp           # PyPI 版
# 或从源码: git clone https://github.com/PancrePal-xiaoyibao/codebase-memory-mcp

# 2. 配置 MCP（~/.claude/settings.json 或项目 .mcp.json）
# {"mcpServers": {"codebase-memory-mcp": {"command": "codebase-memory-mcp", "type": "stdio"}}}

# 3. 索引项目（首次使用必做）
codebase-memory-mcp cli list_projects                        # 查已索引项目
codebase-memory-mcp cli index_repository --repo-path . --mode full   # 建索引
```

## GitNexus 降级配置

```json
{"mcpServers": {"gitnexus": {"command": "gitnexus", "args": ["mcp"], "type": "stdio"}}}
```

## 决策矩阵

| 问题 | 调用 |
|------|------|
| 谁调用了 X？ | `trace_path(direction="inbound")` |
| X 调用了什么？ | `trace_path(direction="outbound")` |
| 完整调用上下文 | `trace_path(direction="both")` |
| 按名字/语义找函数 | `search_graph(query="...")` 或 `name_pattern=".*Regex.*"` |
| 自然语言发现 | `search_graph(query="update settings")`（BM25+camelCase 拆分） |
| 跨语言/词汇桥接 | `search_graph(semantic_query=["send","publish"])`（数组！） |
| 架构总览/模块聚类 | `get_architecture`（含 Leiden clusters） |
| 死代码 | `search_graph(max_degree=0, exclude_entry_points=true)` |
| 高扇出/扇入 | `search_graph(min_degree=10)` |
| 跨服务/多跳/聚合 | `query_graph` + Cypher |
| 纯文本/配置搜索 | `search_code` 或 Grep |
| 复杂度/性能热点 | `query_graph` 查 `transitive_loop_depth`/`linear_scan_in_loop` 等属性 |

## 探索工作流

1. CLI `list_projects` — 确认项目已索引；未索引则 `index_repository(repo_path, mode="full")`
2. `get_graph_schema` — 了解节点/边类型
3. `search_graph` — 定位符号（拿到 qualified_name）
4. `get_code_snippet(qualified_name=...)` — 读源码

## 追踪工作流

1. `search_graph(name_pattern=".*FuncName.*")` — 先拿精确名
2. `trace_path(function_name="...", direction="both", depth=3)` — 追踪
3. 跨服务影响：`trace_path(mode="cross_service")`

## 边类型

CALLS, HTTP_CALLS, ASYNC_CALLS, IMPORTS, DEFINES, DEFINES_METHOD,
HANDLES, IMPLEMENTS, OVERRIDE, USAGE, FILE_CHANGES_WITH,
CONTAINS_FILE, CONTAINS_FOLDER, CONTAINS_PACKAGE,
CROSS_HTTP_CALLS, CROSS_ASYNC_CALLS, CROSS_CHANNEL（跨仓库）

## Cypher 示例（query_graph）

```
MATCH (a)-[r:HTTP_CALLS]->(b) RETURN a.name, b.name, r.url_path LIMIT 20
MATCH (f:Function) WHERE f.name =~ '.*Handler.*' RETURN f.qualified_name, f.file_path
MATCH (f:Function) WHERE f.transitive_loop_depth >= 3 OR f.linear_scan_in_loop >= 1
RETURN f.qualified_name, f.transitive_loop_depth ORDER BY f.transitive_loop_depth DESC
```

## 注意事项（Gotchas）

1. `trace_path` 需要精确函数名 — 先 `search_graph` 找到再追。
2. `search_graph` 默认 limit=200，看响应里的 `total`/`has_more`，截断时用 `offset` 分页。
3. `search_code` 默认只回 10 条且无 offset — 用 `path_filter`/`file_pattern` 收窄或调大 `limit`。
4. `query_graph` 有 100k 行硬顶且无 offset — 宽查询在 Cypher 里自己加 `LIMIT`。
5. `direction="outbound"` 会漏跨服务调用方 — 用 `direction="both"`。
6. `semantic_query` 必须是**关键词数组**，不是单个字符串。
7. 文本/配置/非代码文件（YAML、Markdown、日志）不适用图谱 — 用 Grep/Glob/Read。

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 架构理解辅助决策 |
| 被调用 | code-debugger | 调试前上下文 |
| 被调用 | code-review | 影响范围查询 |
| 被调用 | goal-driven-development | 变更影响与证据 |
| 被调用 | ralph / ralph-yolo | 开发前架构约束 |
