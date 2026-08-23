# 安全审计检查清单（8 分面）

> 配合 SKILL.md Phase 3 使用。每面给"查什么 / 怎么查 / 证据 / 典型发现模板"。

## 面 1：凭证与密钥泄漏

**查什么**：`.env*` 文件是否入 git；硬编码 secret；公网 pk 与 secret 是否同实例；第三方 key 泄漏。

**怎么查**：
```bash
# 历史泄漏：查 .env 是否被提交过
git log --all --oneline -- backend/.env frontend/.env.local
git log --all --diff-filter=A --name-only --oneline -- '*.env*'
# 当前硬编码
rg -n "sk_test_|sk_live_|pk_test_|pk_live_|MASTER_KEY\s*=" --type-add 'cfg:*.{env,local,json,ts,js}' -t cfg
# Clerk 实例一致
rg -n "clerk\.accounts\.dev" 
```

**证据**：`git log` 输出、含 secret 的文件:行号、Clerk 实例域名。

**典型发现**：`backend/.env` 真实密钥已推 private repo（CRITICAL）；MASTER_KEY 用 dev 默认值（CRITICAL）。

## 面 2：认证与鉴权链

**查什么**：Clerk JWT 本地验签是否严格；session 校验是否 fail-closed；admin role 守卫；SSE 票据防重放/越权。

**怎么查**：
```
search_graph(name_pattern=".*authenticat.*", label="Function")
get_code_snippet("requireClerkSession")
get_code_snippet("requireAdmin")
get_code_snippet("consumeSseTicket")
trace_path("consumeSseTicket", direction="inbound")
```

**证据**：鉴权函数源码行号、票据校验逻辑、无 token/伪造 token 的 HTTP 响应。

**典型发现**：SSE 票据 threadId 校验非 fail-closed（但票据一次性+TTL+purpose 绑定 → 实际不可利用 → 降级 LOW）。

## 面 3：加密与密钥管理

**查什么**：MASTER_KEY 派生算法；AES mode；IV 复用；legacy 回退是否弱化；生产校验是否拒绝默认值。

**怎么查**：
```
get_code_snippet("encryptSecret")
get_code_snippet("decryptSecret")
get_code_snippet("assertProductionSecrets")
rg -n "HKDF|createCipher|createDecipher|legacy|fallback" backend/src/lib/crypto.ts backend/src/config/env.ts
```

**证据**：crypto.ts 行号、env.ts 生产校验行号。

**典型发现**：HKDF-SHA256 派生 AES-256-GCM（正确）；legacy SHA-256 回退存在但仅旧数据；dev 跳过生产校验。

## 面 4：注入面

**查什么**：MongoDB 查询是否拼接用户输入；NoSQL operator（$where/$expr）；模板注入；AI prompt 注入。

**怎么查**：
```
search_graph(query="mongo find query where")
rg -n "\$where|\$expr|\$function" backend/src
rg -n "collection\.find\(|collection\.aggregate\(" backend/src  # 看参数来源
```

**证据**：查询构造行号、用户输入到查询的 data_flow。

## 面 5：XSS

**查什么**：react-markdown 是否禁用 raw HTML；CSP script-src；dangerouslySetInnerHTML。

**怎么查**：
```bash
rg -n "dangerouslySetInnerHTML|rehype-raw|allowDangerousHtml" frontend/
cat frontend/next.config.ts  # CSP
```

**证据**：CSP 头、markdown 渲染配置。

**典型发现**：CSP 含 'unsafe-inline' 'unsafe-eval'（MEDIUM，可被 XSS 利用但非直接漏洞）。

## 面 6：沙箱逃逸

**查什么**：E2B 沙箱边界；Agent 代码执行权限；文件系统/网络访问；沙箱间隔离。

**怎么查**：
```
search_graph(query="e2b sandbox execute code")
rg -n "E2B|Sandbox|codeInterpreter|runCode" backend/src
trace_path("runAgent", direction="outbound", mode="cross_service")
```

**证据**：沙箱配置、执行函数源码。

## 面 7：SSRF

**查什么**：所有 `fetch(用户可控URL)` 路径；是否有 scheme/内网/元数据过滤。

**怎么查**：
```bash
rg -n "fetch\(" search-gateway/src backend/src  # 找所有 fetch
# 重点：search-gateway fetchFallback + mcp/handler 的 fetch
```

**动态验证**（证据存 `.debug/evidence/search/`）：
```bash
# MCP initialize
curl -s -X POST http://<gateway>/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",...}' > mcp-init.txt
# tools/list 看有无 extract
# tools/call extract 抓本机回环
curl -s -X POST http://<gateway>/mcp -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"extract","arguments":{"url":"http://localhost:3001/"}}...}' > mcp-ssrf-backend-3001.txt
curl ... "url":"http://localhost:8083/" > mcp-ssrf-8083.txt   # 若 8083 在跑
curl ... "url":"http://169.254.169.254/" > mcp-ssrf-metadata.txt  # 云元数据
```

**证据**：`evidence/search/mcp-ssrf-*.txt`（抓到本机 healthz/backend health/OpenAPI/MongoDB HTTP 探活即 SSRF 成立）。

**已知坑**：两个搜索服务要区分（见 SKILL.md "已知坑"）。

## 面 8：越权（IDOR）

**查什么**：用户态能否访问他人资源（按 userId 过滤还是只校验登录）；admin 端点是否仅 admin。

**怎么查**：
```
search_graph(query="admin route user id filter")
rg -n "requireAdmin|isAdmin|role.*admin" backend/src
# 动态：普通 token 打 admin 端点
curl -s -H "Authorization: Bearer <user_token>" http://<api>/api/admin/users
```

**证据**：admin 守卫行号、越权 HTTP 响应。
