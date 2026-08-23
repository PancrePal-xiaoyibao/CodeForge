---
name: security-audit
description: 全栈安全审计 — 对任意代码仓库做充分的静态+动态+依赖CVE 普查与漏洞挖掘。先 codebase 知识图谱嵌入，再按技术栈分面审计，然后公网测绘与渗透，在 .debug/ 输出证据驱动分级报告。只审计不修复
---

# Security Audit — 全栈安全审计

## 定位

本 skill 是 **通用全栈安全审计流程**，适用于任何有公网暴露面或处理敏感数据的代码仓库。它从一轮真实全栈审计（含 19 项发现、3 CRITICAL）沉淀工作流、要点和坑，做成可复用的审计骨架。原始案例仓库与域名已脱敏。

**核心原则**：
- **证据驱动**：每个发现必须有文件:行号、命令输出或 HTTP 响应作为证据。区分 `observed`（实测确认）与 `inferred`（推理待验），不混入总表。
- **图谱优先**：先用 codebase-memory-mcp 知识图谱建全景，再下钻。图谱是代码关系的结构化完整视图，查图谱替代逐文件阅读，省 ~99% token。
- **只审计不修复**：把问题查清楚是第一位。不产生 commit/push（除非用户单独授权）。
- **fail-closed 思辨**：见一个"非 fail-closed"分支时，必须验证它是否真在攻击路径上——有一次性消费/TTL/purpose 绑定的票据，非 fail-closed 也不可利用，应如实降级而非夸大。
- **可达性决定级别**：代码缺陷的级别 = `代码严重性 × 公网可达性`。一个真实后门若公网不可达（如仅绑 127.0.0.1），降级一档并说明路径。

## 非协商边界

- 渗透边界：只测本项目自有公网面与本项目内网服务。不打第三方基础设施（Clerk/MongoDB Atlas/E2B 等）。SSRF 验证只到本机回环与云元数据地址（169.254.169.254），不外发任意公网目标。
- 区分环境失败与产品缺陷：`curl` DNS 不解析（exit 6）是环境/部署事实不是漏洞；`401` 是鉴权正常。不要把正常拦截写成发现。
- 密钥脱敏：报告正文引用密钥值只留前 8 位 + `…`，完整值仅在证据文件留存（证据文件若入 git 需用户确认）。
- 无证据不写入报告：未带证据的推测标 `inferred` 并列待验证项，不混入 confirmed 总表。

## 工作流（7 Phase）

### Phase 1 — codebase 知识图谱嵌入

审计前**必须**先把代码建进 codebase-memory-mcp 知识图谱。

```bash
codebase-memory-mcp cli list_projects                              # 查是否已索引
codebase-memory-mcp cli index_repository --repo-path <repo> --mode full  # 未索引则建
```

多子项目单仓库可作为一个 project 索引。首轮典型规模：9k+ nodes / 22k+ edges。

### Phase 2 — 技术栈识别与攻击面测绘

先用图谱建立全景，再据技术栈识别该启用的审计面（见 `references/stack-signatures.md`）：

| 要知道 | 调用 |
|---|---|
| 整体结构/包/入口/路由 | `get_architecture(aspects=["all"])` |
| 某函数被谁调用 | `trace_path(function_name, direction="inbound")` |
| 找鉴权/加密相关 symbol | `search_graph(name_pattern=".*(auth\|crypto\|secret\|key).*", label=["Function","Class"])` |
| 认证中间件实现 | `get_code_snippet("authenticateSession")` |
| 跨服务调用链 | `trace_path(name, mode="cross_service")` |

产出一张**攻击面拓扑图**：公网入口 → 反代 → 应用路由 → 鉴权层 → 业务 → DB/外部服务，标注每跳的信任边界。

### Phase 3 — 静态审计（按技术栈分面）

按 `references/audit-checklist.md` 逐面检查。核心 9 面（按技术栈启用）：

1. **凭证与密钥泄漏**：`.env` 入 git？硬编码 secret？公网 pk 与 secret 同实例？第三方 key？
2. **认证与鉴权链**：JWT 验签是否严格？session 校验 fail-closed？role 守卫？票据防重放？
3. **加密与密钥管理**：派生算法？AES mode 与 IV？legacy 回退弱化？生产校验拒绝默认值？
4. **注入面**：DB 查询拼接？NoSQL operator？模板注入？AI prompt 注入？
5. **XSS**：markdown 渲染禁 raw HTML？CSP script-src？dangerouslySetInnerHTML？
6. **沙箱逃逸**：代码执行边界？文件系统/网络访问？沙箱间隔离？
7. **SSRF**：所有 `fetch(用户可控URL)` 路径？scheme/内网/元数据过滤？
8. **越权（IDOR）**：按 ownerId 过滤还是只校验登录？admin 端点仅 admin？
9. **配置与部署**：端口绑定（公网 vs 127.0.0.1）？NODE_ENV 分支？CORS？CSP？

每面用图谱定位 symbol → `get_code_snippet` 看实现 → 标注证据。

### Phase 4 — 依赖 CVE 比对

抽取依赖版本（各 `package.json` + lockfile）→ 比对 OSV/GHSA 漏洞库。即便 0 漏洞也要记录比对过程与覆盖范围，作为"已核查"证据，不能跳过。

### Phase 5 — 动态渗透（公网 + 内网链路）

**前置**：项目须先部署起来。部署后先做内部链路自测（curl healthz/ready/OpenAPI），再公网测试。

公网面测绘：
- 抓首页 → 看是否被认证拦截重定向（正常，非发现）
- 从 chunk 抓 API 域名（注意区分：chunk 里的域名可能是认证库的 fallback base，**不是后端 API 域名**——别误判）
- 确认 backend 是否有独立公网域名，还是只经 frontend 反代

渗透项（每项留存证据到 `.debug/evidence/`）：
- 认证绕过：无 token / 伪造 token / 跨 user 串用
- 越权：普通用户打 admin 端点、IDOR
- SSRF：fetch provider 抓本机 healthz / backend / DB HTTP 探活 / 云元数据
- 票据重放：一次性票据二次消费、跨 session 串用
- CORS / webhook 签名 / presign URL 越权

### Phase 6 — 报告产出

输出到 `.debug/`，结构见 `references/evidence-conventions.md`。发现分级与 schema 见 `references/findings-schema.md`：CRITICAL / HIGH / MEDIUM / LOW / INFO。

### Phase 7 — 复审与交接

- 总报告首段放**执行摘要**：范围、方法、发现计数与最高级别、一句话结论。
- 每个发现给 `failure_scenario`（具体输入/状态 → 错误输出/被攻陷）。
- 修复优先级建议按"可利用性 × 影响"排，不按编号。
- 把"已核查但无发现"的面也写进附录（如 CVE 0 漏洞），证明覆盖完整。

## 审计纪律

- **先问图谱，再无细节，最后才读文件**。`trace`/`search` 返回空时，先检查参数（函数名拼写、label、方向），不要立即跳到逐文件读。
- **环境失败 ≠ 漏洞**。DNS 不解析、容器未起是部署事实，如实记录为环境事实而非发现。
- **可达性约束级别**。每个发现标注 reachability：公网可达 / 仅内网 / 需特定权限。
- **避免夸大**。非 fail-closed 但有 TTL/一次性/purpose 绑定的，实际不可利用 → 降级。代码缺陷但公网不可达 → 降级并说明。

## 相关技能

| 关系 | Skill | 场景 |
|---|---|---|
| 前置 | codebase-context | 知识图谱嵌入与架构测绘 |
| 互补 | project-health-audit | 技术债基线（非安全向） |
| 输出给 | intent-grill / prd | 修复 SPEC 的输入 |
| 输出给 | goal-driven-development | 修复实现（需单独授权，本 skill 不做） |

## 关联 Skill（CodeForge 网络调度协议）

| 关系 | Skill | 场景 |
|---|---|---|
| 前置 | codebase-context | 知识图谱嵌入与架构测绘（codebase-memory MCP 优先） |
| 互补 | project-health-audit | 变更前技术债基线（非安全向） |
| 输出给 | intent-grill | 修复需求澄清 |
| 输出给 | prd | 修复 PRD 输入 |
| 输出给 | goal-driven-development | 修复实现（需单独授权，本 skill 只审计不修复） |
