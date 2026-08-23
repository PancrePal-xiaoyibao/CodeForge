# 证据与报告目录约定

## `.debug/` 布局

```
.debug/
├── SECURITY_AUDIT_REPORT.md     # 总报告（唯一交付物，人读）
├── raw/                         # 分面子报告 + 中间数据
│   ├── cve-scan.md              # 依赖 CVE 比对
│   ├── static-frontend-xss.md   # frontend 静态
│   ├── static-backend-injection.md
│   ├── static-agent-sandbox.md
│   ├── dynamic-pentest-public.md
│   └── findings-confirmed.md   # 手动维护的确认清单（F-NN 单行汇总）
└── evidence/                    # 原始证据，一个动作一个文件
    ├── search/                 # SSRF / search-gateway MCP 测试
    │   ├── mcp-init-*.txt
    │   ├── mcp-tools-list.txt
    │   ├── mcp-ssrf-*.txt      # 每个 SSRF 目标一个
    │   └── mcp-*-noauth.txt
    └── local/                  # 内网链路自测
        ├── get_health.txt
        ├── get_ready.txt
        └── internal_metrics.txt
```

## 证据文件命名

- `mcp-{phase}-{detail}.txt`：MCP 协议测试（init/tools/call）
- `mcp-ssrf-{target}.txt`：SSRF 目标（backend-3001 / mongodb / localhost / self / 8083 / metadata）
- `mcp-{phase}-noauth.txt`：无鉴权测试
- `get_{path}.txt` / `post_{path}.txt`：HTTP 探测，path 用下划线
- `auth_*.txt`：认证相关（sktest / events / signin_enum）
- `billing_*` / `webhook_*` / `staff_*` / `attachments_*` / `cors_*`：业务面

## 总报告结构

```markdown
# Security Audit Report — <项目/域名>
## 执行摘要（范围/方法/发现计数/最高级别/一句话结论）
## 审计范围与方法
## 发现总表（表格：ID/标题/级别/类别/状态）
## CRITICAL 详述（每条：证据+failure_scenario+可达性+修复提示）
## HIGH / MEDIUM / LOW / INFO 详述
## 攻击面拓扑图
## 修复优先级建议
## 附录：已核查面（含无发现项）
```

## 命名规范

- 发现 ID：`F-01` 起递增，跨级别连续编号（不复用）。
- 证据文件路径在总报告里用相对路径引用（`.debug/evidence/search/mcp-ssrf-backend-3001.txt`）。
- 子报告与总报告的发现 ID 必须一致——`findings-confirmed.md` 是 ID 的权威清单。
