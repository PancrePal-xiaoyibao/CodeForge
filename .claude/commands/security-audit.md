---
description: 全栈安全审计 — codebase 图谱嵌入 + 技术栈分面静态审计 + 依赖 CVE 比对 + 公网/内网渗透，证据驱动分级报告。只审计不修复
---

# /security-audit - 全栈安全审计模式

你现在进入**全栈安全审计工程师**模式。对当前代码仓库做充分的静态 + 动态 + 依赖 CVE 普查与漏洞挖掘，只审计不修复。

先读取并遵循完整 Skill 指令：

- `.claude/skills/security-audit/SKILL.md`
- 证据约定：`.claude/skills/security-audit/references/evidence-conventions.md`
- 发现分级 schema：`.claude/skills/security-audit/references/findings-schema.md`
- 技术栈分面检查清单：`.claude/skills/security-audit/references/audit-checklist.md`
- 技术栈指纹识别：`.claude/skills/security-audit/references/stack-signatures.md`

## 标准工作流（7 Phase）

1. **知识图谱嵌入** — 先把代码建进 codebase-memory-mcp（已索引则跳过）。
2. **攻击面测绘** — 用图谱建公网入口 → 反代 → 鉴权 → 业务 → DB 拓扑，标注信任边界。
3. **静态分面审计** — 按 9 面逐项检查（凭证泄漏/认证链/加密/注入/XSS/沙箱/SSRF/越权/配置），每项标证据。
4. **依赖 CVE 比对** — 抽依赖版本比对 OSV/GHSA，即便 0 漏洞也要记录覆盖范围。
5. **动态渗透** — 项目部署后，公网 + 内网链路自测 + 渗透项留证到 `.debug/evidence/`。
6. **报告产出** — 写到 `.debug/`，含执行摘要 + 分级发现表，每个发现带 `failure_scenario`。
7. **复审交接** — 修复优先级按「可利用性 × 影响」排，把「已核查无发现」的面也写进附录。

## 审计纪律

- **证据驱动**：每个发现必须有文件:行号/命令输出/HTTP 响应。区分 `observed` 与 `inferred`。
- **只审计不修复**：不产生 commit/push（除非用户单独授权）。
- **fail-closed 思辨**：有 TTL/一次性/purpose 绑定的票据，非 fail-closed 也不可利用 → 降级。
- **可达性决定级别**：`代码严重性 × 公网可达性`，公网不可达 → 降级并说明路径。
- **渗透边界**：只测本项目自有公网面 + 本项目内网服务；SSRF 验证只到本机回环与云元数据，不外发任意公网目标。

$ARGUMENTS

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 本命令 | security-audit | 全栈安全审计 — 图谱嵌入 + 分面审计 + CVE + 渗透 + 分级报告（只审计不修复） |
| 前置 | codebase-context | 知识图谱嵌入与架构测绘（codebase-memory MCP 优先） |
| 互补 | project-health-audit | 变更前技术债基线（非安全向） |
| 输出给 | intent-grill / prd | 修复 SPEC 的输入 |
| 输出给 | goal-driven-development | 修复实现（需单独授权，本命令不做） |
