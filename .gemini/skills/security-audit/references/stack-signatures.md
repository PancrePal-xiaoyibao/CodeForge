# 技术栈识别与攻击面签名

> 配合 SKILL.md Phase 2 使用。识别项目技术栈后，启用对应的审计面与检查项。

## 技术栈指纹识别

```bash
# 框架/语言
rg -l "next|nuxt|vite" package.json      # 前端框架
rg -l "fastify|express|hono|koa"          # 后端框架
rg -l "bun|deno" package.json             # 运行时
rg -l "mongoose|prisma|drizzle|sequelize" # ORM
rg -l "redis|ioredis|bun:redis"           # 缓存
rg -l "clerk|auth0|supabase|nextauth"     # 认证服务
rg -l "e2b|firecracker|sandbox"           # 代码沙箱
rg -l "@modelcontextprotocol|mcp"         # MCP 服务
```

## 认证服务签名

| 服务 | 审计重点 |
|---|---|
| Clerk | JWT 本地验签（test/prod 分支）、authorizedParties、sk_test/pk_test 同实例泄漏、session 校验、webhook 签名 |
| Auth0 | audience 校验、issuer 校验、jwks 缓存、RS256 vs HS256 |
| NextAuth | session strategy（jwt/database）、CSRF token、回调 URL 白名单 |
| 自研 JWT | 算法混淆（none/HS256↔RS256）、密钥强度、过期校验、签名验证是否可绕过 |

## 数据库签名

| 存储 | 注入面 |
|---|---|
| MongoDB (mongoose) | NoSQL operator（$where/$expr/$function）、查询拼接、IDOR（缺 ownerId 过滤） |
| SQL (prisma/drizzle) | 原生查询拼接、ORDER BY 注入、LIKE 通配符 |
| Redis | Lua 脚本注入、KEY 命令注入、SSRF（可控 URL redis） |

## 代码沙箱签名

| 沙箱 | 审计重点 |
|---|---|
| E2B | 沙箱间隔离、网络出口、文件系统边界、环境变量泄漏到沙箱 |
| Firecracker | rootfs 配置、网络命名空间、CPU/内存限制 |
| VM2/isolated-vm | escape CVE、原型链逃逸 |
| child_process | shell 注入（拼接 vs spawn）、命令白名单 |

## 外部调用面（SSRF/注入）

| 面 | 识别 |
|---|---|
| fetch(用户URL) | `rg -n "fetch\(" src/` —— 每个 fetch 看参数来源，有无 scheme/内网过滤 |
| HTTP 代理/网关 | 是否有 auth 中间件、apiKeys 是否空数组后门 |
| AI API | prompt 注入、key 泄漏、response 注入下游 |
| 文件上传 | 路径穿越、MIME 校验、存储 URL 签名越权 |

## 公网暴露面识别

```bash
# 生产部署配置
rg -n "0\.0\.0\.0|127\.0\.0\.1|localhost" docker-compose*.yml Dockerfile
rg -n "NODE_ENV\s*=" .env* docker-compose*.yml
# nginx/反代
rg -n "proxy_pass|server_name" nginx.conf
# 端口暴露
rg -n "ports:|expose:" docker-compose*.yml
```

**关键判断**：服务绑 `127.0.0.1` → 仅内网可达（降级公网漏洞）；绑 `0.0.0.0` → 公网可达。生产 `NODE_ENV=production` 是否启用更严校验分支。
