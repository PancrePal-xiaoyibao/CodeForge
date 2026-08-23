# 发现分级与 Schema

## 严重性分级

| 级别 | 含义 | 处置时限（建议） |
|---|---|---|
| CRITICAL | 直接可被公网利用，导致数据泄漏/越权/RCE | 立即 |
| HIGH | 公网可利用但有门槛，或内网链路致命 | 本周 |
| MEDIUM | 需组合利用，或公网可达性受限 | 本迭代 |
| LOW | 防御纵深缺失/非 fail-closed 但实际难利用 | 计划修复 |
| INFO | 安全观察项/已核查无发现/环境事实 | 知悉 |

> **降级原则**：代码缺陷的级别 = `代码严重性 × 公网可达性`。一个真实的后门若公网不可达（如 backend 仅绑 127.0.0.1），降级一档并说明可达路径。

## 单条发现 Schema

```yaml
finding_id: F-01
title: ""
severity: CRITICAL|HIGH|MEDIUM|LOW|INFO
category: 凭证泄漏|认证|加密|注入|XSS|沙箱|SSRF|越权|配置|依赖
status: observed|inferred|confirmed
evidence:
  - type: file|command|http
    ref: "backend/.env:7"
    snippet: "MASTER_KEY=0123456789abcdef…"
failure_scenario: "攻击者获得 MASTER_KEY（dev 默认值），调用 decryptSecret 解密所有 MinerU 加密 URL，越权读取任意用户上传文档"
reachability: "公网经 frontend 反代 → backend（生产绑 127.0.0.1:3001，仅内网可达）"
remediation_hint: "生产强制随机 MASTER_KEY，轮换已泄漏值"
confidence: high|medium|low
```

## 不可写入报告的内容

- 未带证据的推测（标 `inferred` 并列待验证项，不混入 confirmed 总表）
- 把环境失败（DNS 不解析、容器未起）写成漏洞
- 完整密钥值进总报告正文（只留前 8 位 + `…`）
