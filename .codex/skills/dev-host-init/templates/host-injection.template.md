<!-- dev-host-init injection template v1
     三层结构：A 通用开发铁律（固定文本）/ B 机器环境画像（{{占位符}}探测填充）/ C 个人项目专属区（留空自填）
     渲染规则：探测不到的占位符必须填明确兜底文案，禁止留裸 {{}}；已存在注入文档时只增量更新 B 层段落。 -->
{{LANG_HEADER}}
## Codebase 索引优先（codebase-memory-mcp）

**任何新 session 进入项目开发前，先查 codebase 是否已索引，未索引则建索引（full 模式）。** 代码探索优先用 codebase-memory-mcp 工具（`search_graph` / `trace_path` / `get_code_snippet` / `query_graph` / `get_architecture`），文本/配置/非代码文件才用 grep/glob/read。

```bash
# 1. 查已索引项目（后续查询的 project 参数用返回的 name 字段）
codebase-memory-mcp cli list_projects

# 2. 未索引则建（--mode: full=全量+相似/语义边 / moderate / fast；--persistence true 生成团队共享 .codebase-memory/graph.db.zst）
codebase-memory-mcp cli index_repository --repo-path {{DEV_ROOT}}/<项目> --mode full

# 3. 查询（推荐 stdin 写法，对所有工具通用）
echo '{"project":"项目名","name_pattern":".*Handler.*","label":"Function"}' | codebase-memory-mcp cli search_graph
echo '{"project":"项目名","function_name":"Search","direction":"both"}' | codebase-memory-mcp cli trace_path
echo '{"project":"项目名","query":"MATCH (f:Function) RETURN f.name LIMIT 5"}' | codebase-memory-mcp cli query_graph
```

> 部署/细节见 `{{CODEBASE_MCP_DOCS}}`（cli 不在 PATH 时按文档激活，或直接用 MCP 工具 `mcp__codebase-memory-mcp__*`）。

> **核心原则**：codebase-memory-mcp 的知识图谱已经是代码关系的结构化完整视图。查询图谱替代逐文件阅读，每少一次 `read` 调用就是约 **99% 的 token 节省**。
>
> **先问图谱，再无细节，最后才读文件。**

---

## 一、场景 → 工具映射（必选路径）

| 你想知道 / 你要做的事 | 调用的 MCP 工具 | 说明 |
|---|---|---|
| 这个项目整体结构？语言、包、入口、路由 | `get_architecture()` | 一次调用，给你全景 |
| 这个函数/类被谁调用了？ | `trace_call_path(name, direction="inbound")` | 入向调用链，depth 可达多层 |
| 这个函数调用了谁？ | `trace_call_path(name, direction="outbound")` | 出向调用链 |
| 找名字带 X 的函数/类/方法 | `search_graph(name_pattern=".*X.*", label=["Function","Class"])` | 支持 regex 匹配 |
| 两类代码之间的关系（继承/实现/调用） | `query_graph("MATCH (a)-[:INHERITS\|IMPLEMENTS\|CALLS]->(b) WHERE a.name = 'X'")` | 类 Cypher 语法 |
| 源码里搜关键词 | `search_code(query="TODO\|FIXME")` | 图谱增强的 grep |
| 只记得功能不记得名字 | 先用 `search_graph(name_pattern)`，必要时 `semantic_query` | 语义搜索兜底 |
| 看某个函数/类的具体代码 | `get_code_snippet(name)` | 仅拿该 symbol 的几行，不加载整个文件 |
| 改了代码，影响范围？ | `detect_changes()` | git diff → 风险映射 |
| 检查文件/路径有没有被索引 | `check_index_coverage(path)` | 先查后读，避免读未索引文件 |
| 列出目录结构 | `list_directory(path)` | 替代 `ls` |
| 获取索引统计（节点、边、标签） | `get_graph_schema()` | 了解项目规模 |

---

## 二、强制执行顺序（3 级阶梯）

```
Level 1 — 图谱查询（必须优先）
   调用：trace_call_path / search_graph / query_graph / get_architecture
   不满足 ↓

Level 2 — 精准代码片段（仅当 Level 1 不够）
   调用：get_code_snippet(name) 获取 symbol 级代码
   不满足 ↓

Level 3 — 逐文件阅读（final fallback）
   先 check_index_coverage(path) 确认已索引
   然后 list_directory(path) 定位
   最后 read(path) 读具体文件
```

### 🔒 硬约束

- **不允许**直接从 Level 1 跳到 Level 3
- **不允许**在任何能调用 Level 1/2 工具的场合直接 `ls` 或 `read`
- 当 trace / search 返回空结果时，**先检查参数是否正确**（函数名拼写、label 类型、过滤条件），而不是立即 fallback 到读文件

---

## 三、常见反例（禁止的行为 🚫）

| ❌ 别这样做 | ✅ 应该这样做 |
|---|---|
| `read src/handler/order.ts` 逐行读文件 | `trace_call_path("processOrder", direction="inbound")` |
| `ls src/services/` 然后挨个读 | `get_architecture()` 获取全貌 |
| `grep -r "validate" src/` | `search_code(query="validate")` |
| 用 `read` 看函数实现 | `get_code_snippet("validateOrder")` |
| 手动追踪调用链 `read fileA → read fileB → ...` | `trace_call_path("main", direction="outbound", depth=5)` |
| 搜不到就说"没找到这个文件"然后放弃 | 先用 `search_graph` 确认 symbol 是否存在，或用 `search_code` 搜索关键词 |

---

## 四、注意事项

1. **`trace_call_path` 和 `search_graph` 返回空时**：先检查参数（函数名拼写、label 类型、方向），不是直接跳过图谱去读文件
2. **`get_code_snippet`**：只返回 symbol 本体代码，不包含上下文；如果需要看实现细节，先 snippet 再 `read` 指定行号范围
3. **`query_graph`**：是最灵活的底层查询工具，任何图谱层面找关系的问题都可以用它
4. **不确定 symbol 名称**：先用 `search_graph(name_pattern=".*")` 搜到准确名字
5. **同时涉及多个文件的改动**：用 `detect_changes()` 定位影响范围，再针对重点 symbol 用 `trace_call_path`
6. **未索引的文件**：如果 `check_index_coverage` 说未索引，需要先索引项目，不要直接读取大段源码

---

## 五、快速决策树

```
┌─ 我想了解代码关系 ──────────────────────┐
│                                           │
│  1. 项目全景？          → get_architecture │
│  2. 调用链？（谁调了/调了谁）→ trace_call_path │
│  3. 找函数/类？         → search_graph    │
│  4. 搜关键词？           → search_code     │
│  5. 关系查询？（继承/调用等）→ query_graph  │
│  6. 看具体实现？         → 先 Level 1-2    │
│                         再 get_code_snippet│
│                         最后 read (行级)   │
└───────────────────────────────────────────┘
```

## 宿主机硬件环境

- **CPU**: {{CPU}}
- **RAM**: {{RAM}}
- **GPU**: {{GPU}}
- **存储**: {{STORAGE}}
- **注意**: {{HW_NOTES}}

## 网络代理

{{PROXY_DESC}}

- **SOCKS5**: `{{PROXY_SOCKS5}}`
- **HTTP**: `{{PROXY_HTTP}}`

配置方式:
```bash
git config --global http.proxy http://{{PROXY_HTTP_HOSTPORT}}
git config --global https.proxy http://{{PROXY_HTTP_HOSTPORT}}
```

## 环境速查

{{ENV_TABLE}}

## 个人开发偏好

- **Python**: 优先 `uv venv` 管理虚拟环境，不用 conda（除非特定环境已存在）
- **前端/Office/文档**: JS/Node + TypeScript，包括 PPTX/DOCX 等办公文档生成
- **应用开发**: Rust 或 Go，追求优雅和性能
- **原则**: 新项目 Python 用 uv，已有 conda 环境直接复用，不重复造轮子

## 多 Agent 并行开发协作机制（本机常态）

本机同一仓库经常有 **2-3 个 agent（Claude Code / Codex / OpenCode / Kimi 等）并行开发**，是常态而非异常。下列规则保证多 agent 不互相踩踏。

### 动手前：感知并行状态（每次开发第一步）

```bash
cd <项目绝对路径>
git status -sb                    # 工作区改动 + 与 origin 领先/落后
git log --oneline -6               # 最近 commit，识别其他 agent 提交
git rev-parse HEAD origin/main     # 本地是否已 push
```

工作区有大量**自己不认识**的未提交改动 = 另一个 agent 正在写。**先告诉用户当前并行状况，再决定动不动手**，不自作主张。

### 识别在途改动归属（不要默认是"残留垃圾"去清理）

| 判断依据 | 方法 |
|---|---|
| 时间戳 | `ls -lt --time-style=+%H:%M:%S <files>`，与自己的会话时间对照 |
| 内容连续性 | `git diff <file>` 看是否连贯方案，还是残缺断片 |
| commit 历史 | `git log --oneline -1 -- <file>` 看该文件最近被谁 commit |
| 是否在 HEAD 基础上扩展 | `git show HEAD:<file>` 对比工作区差量，是扩展还是覆盖 |

### 协作铁律

1. ❌ **绝不 `git add .` / `git add -A`** —— 会把别的 agent 在途改动卷进自己 commit。**显式列每个文件**：`git add src/a.py tests/test_a.py`。
2. ❌ **不动别人的未提交改动** —— 不修改、不格式化、不"帮忙"提交、不删除别人工作区里看起来有问题/未完成的代码（那是别人的思考中间态）。
3. ❌ **不叠加自己的内容到别人在改的文件** —— 若某文件正被别的 agent 改（工作区有未提交 diff），即使自己也要改同文件，**先等对方 commit/push 再动**，避免 merge 冲突。
4. ✅ **尊重已改部分** —— 重叠/冲突时尊重已经修改的部分，**不覆盖、不回退**，先暂停自己的相关改动，等另一 agent 落地后再在其基础上优化。
5. ✅ **只 commit 自己职责范围的文件** —— push 前确认 `git diff --cached --name-only` 只含自己的改动，不含 .bak / secrets / 别人的在途文件 / 运行时噪音。
6. ✅ **小步独立 commit** —— 一个逻辑单元一个 commit，message 说清干了什么，让其他 agent 看 log 能接上。
7. ✅ **自己的改动尽早 push** —— 减少工作区堆积，工作区越干净对其他 agent 越友好。

### commit/push 是独立 Gate

commit 和 push 是需确认的动作（非自动）。但用户明示「该推送推送」后，对**已验证通过、纯属自己职责范围**的改动可直接 commit/push，不必逐次请示；遇到边界（涉及别人在途文件、生产环境、明文密钥）才停下来请示。

### 运行时噪音文件

容器/守护进程/运行时自动写的状态快照（如 workspace shared/state、`*.json.tmpl`、`cache/live/*`）时间戳频繁更新。**通常不主动 commit**（除非是配置结构变更）；若要提交，单独一个 commit，不和业务代码混。

## 测试产物卫生铁律（Test Artifact Hygiene）

测试是开发闭环里最容易"拉屎"的环节。执行任何测试/验证/Checkfix 前后，必须遵守：

**T0 · 测试前检查（Pre-test Sweep）** — 进入项目跑测试前，先扫工作区是否有**上轮测试遗留**：未被 .gitignore 覆盖的 test artifact、跑测生成的临时 db/缓存/截图/导出、fixture 残留、`__pycache__`。发现即通报用户清单后再启动本轮测试，避免新旧残留混淆。**只扫测试产物类遗留，绝不碰别人的在途代码改动**（见协作铁律）。

**T1 · 测试后清扫（Post-test Cleanup）** — 测试结束后进入项目内部检查本轮"拉屎"：测试运行残留、临时输出、调试快照、未被 .gitignore 覆盖的生成物。通报清单后清理。

**T2 · 严格区分三类，误删运行数据 = 事故**

| 类别 | 判定 | 处置 |
|------|------|------|
| **测试产物**（test artifact） | 测试框架临时输出、fixture 残留、跑测临时 db/缓存/截图/mock 数据、`__pycache__`、被 .gitignore 覆盖的生成物 | 通报后**自动删** |
| **运行数据**（runtime data） | 项目实际运行产生的 DB 记录、日志、用户上传、缓存里的真实数据、生产/热开发正在用的状态 | **绝不删**，哪怕看起来像临时文件 |
| **模糊/无法确认** | 既不像明确测试产物，也无法确认是运行数据；或属于别人在途改动 | **逐项问用户**，不擅自处置 |

**T3 · 代码层老鼠屎清扫（Code-level Turd Sweep）** — 测试通过后，清理代码层残留：`print`/`console.log`/调试输出、`debugger`/breakpoint 语句、注释掉的测试代码块、临时 TODO/FIXME、硬编码测试数据/魔法数字、未清理的 mock 注入、被注释掉的旧实现。这些"老鼠屎"在热开发与生产 debug 时会误导排查，必须随测试闭环一并清掉。

**删除安全网**：批量删除用 `/bin/rm -f` 或 `command rm -f`（绕 `rm -i` 别名）；删除前通报清单与分类；运行数据一律不动；模糊项问；删除范围仅限本轮自己产生的测试产物，不卷入他人改动。

## 开发审美铁律（Aesthetic Discipline）

双轨目标：**下限兜底**（任何产出物不出丑）+ **上限激发**（最大化模型审美潜能）。

### 下限 · 三禁（无条件遵守，违反即返工）

1. ❌ **禁默认色与彩虹色**：全项目统一低饱和色板——类别 ≤8 离散色，数值渐变 sequential，正负对比 diverging。
2. ❌ **禁堆装饰**：删掉一切不承载信息的元素（多余网格线 / 边框 / 阴影 / 3D / 渐变背景）；留白优先于填充。
3. ❌ **禁风格漂移**：同一作品内字体、线宽、间距、图例必须统一；动手前先定视觉系统，再画第一笔。

### 上限 · 激发（以设计师而非规则执行者自居）

- 规则只兜底，优雅靠主动判断：每次产出后自问「还能更克制吗？层级还能更清晰吗？删掉什么会更高级？」——最好的作品是删无可删。
- 建立并沿用一套自己的视觉系统（色板 + 字体 + 线宽 + 间距），让所有产出呈现同一位作者的手笔。
- 不确定时向公认的高级感范式对齐（瑞士平面 / 杂志级排版 / 顶级产品官网），而不是向「能用」对齐。

## 踩坑记录（避免重复犯错）

- **rm -i 别名**：部分 shell 把 `rm` 别名成 `rm -i`（每次删文件都问确认）。批量删除用 `/bin/rm -f` 或 `command rm -f`
- **工具默认工作目录**：agent 的 Bash 工具默认 cwd 通常是用户主目录（不是项目目录）。用相对路径会解析错误，**一律用绝对路径**
- **管道掩盖退出码**：`cmd | tail` 会用 tail 的 exit code 覆盖 cmd 的。验证命令成败用 `cmd > /tmp/out.log 2>&1; echo "EXIT=$?"; tail -20 /tmp/out.log`
- **vendor 源码不完整**：从 GitHub 下载的 vendor 目录可能缺文件（如 Cython .pyx）。编译失败时改用 PyPI 包
- **setuptools-scm 无 .git**：vendor 源码无 .git 目录时 setuptools-scm 推断版本失败。设 `SETUPTOOLS_SCM_PRETEND_VERSION=x.y.z` 环境变量

<!-- 踩坑持续追加于此：每条一行「**坑名**：现象 → 解法」 -->

---

## 个人项目专属区（按需自填）

<!-- 本区块不参与通用模板：配色方案、网络拓扑、业务专属规则等，由本机用户按项目自行补充。
     建议形态：项目配色板（含取色来源与约束）、服务拓扑图（入口/端口/证书）、领域术语表。 -->
