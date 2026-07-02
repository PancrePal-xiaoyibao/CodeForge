# CodeForge 伦理与负责任使用条款 (ETHICS.md)

> 本文件是 [LICENSE](./LICENSE) 的强制性补充条款。违反本文件任何条款，将立即且自动终止 LICENSE 授予的全部许可。

**版本**: 1.0.0 · **生效日期**: 2026-07-02

---

## 0. 适用声明

CodeForge 是面向**软件开发者与开源社区**的 AI 辅助开发脚手架，不是"自主开发系统"、不是"审计-免责机器"、不是替代人类工程判断的工具。

- CodeForge 所有 skill 的输出（技术规范、代码、评审意见、CI 配置、投放决策等）均为**辅助参考**，必须经过**具备相应工程能力**的开发者独立审阅后方可用于任何正式产品/服务。
- 使用者对其使用 CodeForge 产生的全部代码、部署、决策后果承担全部法律责任。
- 涉及生产环境、支付、隐私、健康、安全的场景中，使用者必须**优先遵守**所在地适用的法律法规与行业规范。本文件不构成法律建议。

---

## 1. 核心原则

| 原则 | 内涵 |
|------|------|
| **人类主导 (Human-in-the-Loop)** | AI Agent 是副驾驶，不是决策者。commit、push、发布、变更生产系统前须人类明确授权 |
| **开源正直 (Open-Source Integrity)** | 遵守上游 License、正确署名、不隐匿 AI 辅助来源 |
| **透明可审计 (Transparency)** | AI 生成的代码、PR、Issue 回复须可披露、可追溯 |
| **最小权限 (Least Privilege)** | 授予 Agent 的令牌/权限最小化；不共享包含长期机密的会话 |
| **社区尊重 (Community Respect)** | 对 issue 提出者、维护者、其他贡献者保持基本尊重 |

---

## 2. 严格禁止的用途（红线）

以下用途**在任何情况下均不被许可**：

### 2.1 恶意代码与网络攻击
- 生成或部署**恶意软件、勒索软件、蠕虫、后门、rootkit、间谍软件**。
- 生成用于**未授权入侵、拒绝服务攻击、大规模钓鱼、凭证窃取**的代码或基础设施。
- 使用 CodeForge 的 Agent 循环批量**扫描-利用**第三方系统的漏洞。

### 2.2 供应链与信任滥用
- 向上游开源项目提交**恶意 PR**（隐藏后门、依赖投毒、typo-squatting、诱导性代码）。
- 冒用他人身份/账号提交贡献；伪造 commit signatures 或 CI 状态。
- 在 CodeForge 输出的代码中**混入未披露的商业追踪、遥测或数据外传**。

### 2.3 学术与工程不端
- 将 AI 生成的代码/文档**冒充为完全人工产出**并提交至强制披露 AI 使用的场景（如学位论文、期刊、企业审计）。
- **数据/结果造假**、性能测试作弊、伪造 benchmark、隐匿失败样本。

### 2.4 侵犯权利与歧视
- 生成或部署基于种族、性别、宗教、地域、健康状况等的**歧视性算法**。
- 未获同意即处理、传输、销售**个人身份信息 (PII)** 或**受保护健康信息 (PHI)**。
- 违反 GDPR / CCPA / 《个人信息保护法》/ HIPAA 等适用数据保护法规的处理行为。

### 2.5 武器与高危双用途
- 设计、优化、指导**武器系统、化学/生物/核/放射性武器**相关代码或数据管线。
- 规避出口管制、制裁清单、双用途技术管控要求。

### 2.6 其他
- 任何违反所在地法律的用途。
- 任何意在**逃避伦理审查**或**规避监管**的用途。
- 任何将 CodeForge 用于**规模化制造虚假信息、深度伪造 (deepfake) 内容**的行为。

---

## 3. 强制使用要求

使用 CodeForge 时，使用者**必须**：

1. **授权明确** — Agent 执行 `git commit` / `git push` / 修改数据库 / 部署生产系统 / 发布 npm 包 / 发送外部消息前，必须获得人类明确授权（本仓库的 skill 已默认内置该约束）。
2. **权限最小化** — 分配给 Agent 的 GitHub token、npm token、云厂商密钥、生产凭证应最小化 scope，并按项目周期轮换。
3. **代码审阅** — AI 生成的代码进入主分支前须由人类 review。禁止在无人 review 的情况下将 AI 代码合并到 `main` / `master` / `release/*`。
4. **AI 披露** — 在 PR、Issue 回复、学术产出中如实披露 CodeForge / 相关 Agent 的辅助角色。
5. **上游 License 合规** — 使用 CodeForge 修改其他开源项目时，遵守目标项目的 License 与 CLA 要求。
6. **数据合规** — 处理用户数据、日志、备份时遵守适用法规；不将真实生产数据未经脱敏送入公开 API。

---

## 4. AI 系统的已知局限

使用者应知晓，CodeForge 基于大语言模型，存在以下固有局限：

- **可能产生幻觉** — 生成的代码可能引用不存在的 API、包版本、CLI flag；`deep-research` 已内置引用验证，但仍需人工核查。
- **安全漏洞盲区** — 生成的代码可能包含 SQL 注入、XSS、SSRF、路径穿越等常见漏洞；上线前必须做 `code-review` + 人工安全审阅。
- **知识时效性** — 模型训练数据有截止日期，最新 API / SDK / 规范请通过 `deep-research` 实时补充。
- **依赖偏差** — 可能默认选用作者训练数据中"看起来主流"但已被弃用的库或写法。
- **不构成法律/工程终审** — 任何输出不得替代法律、合规、架构、安全的人类专业判断。

---

## 5. 参考框架

- [The Twelve-Factor App](https://12factor.net/) — 云原生开发原则
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Web 应用安全
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM 应用安全
- [ACM Code of Ethics](https://www.acm.org/code-of-ethics) — 计算机专业伦理
- [EU AI Act](https://artificialintelligenceact.eu/) — 欧盟 AI 法案
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — AI 风险管理

---

## 6. 违规后果

任何违反本文件第 2 节（红线）或第 3 节（强制要求）的行为：

1. **立即终止许可** — LICENSE 授予的全部许可自动终止，使用者须立即停止使用并销毁全部副本。
2. **维护方权利** — CodeForge 维护方保留公开声明、要求停止侵权、追究法律责任的权利。
3. **不免责** — 本条款的任何宽限或未执行，不构成对未来违规的默许。

---

## 7. 举报与反馈

发现本仓库被用于上述禁止用途，或发现某 skill 存在安全/伦理风险（例如某 skill 的输出引导了危险的代码模式），请：

1. 在 [GitHub Issues](https://github.com/PancrePal-xiaoyibao/CodeForge/issues) 提交报告（涉及敏感信息请脱敏）。
2. 严重违规（如恶意软件、供应链攻击）请同时向所在地监管机构与相关平台（GitHub Security、npm Security）举报。
3. 欢迎通过 Pull Request 完善 ETHICS.md 与各 skill 的安全约束 —— **让伦理条款随社区一起进化**。

---

*CodeForge 相信：让 AI Agent 高效工作的前提，是让人类始终握着方向盘喵～* (..•˘_˘•..)
