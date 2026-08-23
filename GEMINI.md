# GEMINI.md — CodeForge Full-Stack AI Dev Engine (Gemini CLI)

CodeForge is a community-driven **full-stack AI development engine**. This scaffold ships a pre-installed Gemini skill suite that turns a blank Gemini CLI environment into a **requirement → spec → API-First implementation → debug → UX → CI/CD → release** cockpit.

---

## 🎯 Lead Skill

Use `ai-spec` as the lead skill when unsure. For any first-run project work, `ai-spec` must perform **Repo Init**: read or create `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`, capture project philosophy, environment, tests, developer preferences, encoding rules, plan docs, and approval boundaries.

For external information tasks (tech selection, literature, competitor scans), invoke `deep-research` before spec generation.

---

## 🗺️ Skill Routing Network

| Scenario | Route | Output |
|----------|-------|--------|
| New machine / host onboarding | `dev-host-init` → `dev-env-scan` → `ai-spec` | Host bootstrap + injection doc + environment profile |
| New repository / first agent run | `dev-env-scan` → `ai-spec` | Environment profile + project workflow |
| Vague requirement | `intent-grill` → `ai-spec` | Clarified spec |
| External info / tech selection / literature | `deep-research` → `ai-spec` | Structured research + citations |
| Pre-change health baseline | `project-health-audit` → `prd` / `ai-spec` | Debt register + change-impact map |
| Product feature from scratch | `prd` → `ai-spec` → `api-first-modular` | PRD + implementation plan |
| Full-stack feature | `ai-spec` → `api-first-modular` → `code-review` | API-first implementation + review |
| Approved-SPEC execution | `goal-driven-development` → `api-first-modular` → `code-review` | Evidence milestone loop + authorization gates |
| Bug or regression | `codebase-context` → `code-debugger` | Impact map + targeted fix |
| UI visual issue | `debug-ui` → `ux-experience-audit` | Visual polish + workflow check |
| UX issue across layers | `ux-experience-audit` → `code-debugger` or `api-first-modular` | Cross-layer diagnosis |
| Autonomous implementation | `prd` or `ai-spec` → `ralph` / `ralph-yolo` | Story loop execution |
| Post-delivery iteration | `iteration-manager` | Residual classification + next Gate |
| Package / multi-skill system | `loop-engineer` → `ai-spec` | Skill network design |
| Skill opportunity mining | `discover-skill-opportunities` | Skill candidates + session review |
| Project workflow bootstrap | `sam-dev-cc-init` | PDCO loop files |
| Computational dry-lab research | `ai4s-dry-lab` | SPEC-driven OODA loop (W1-W4) |
| Methodology extraction | `extract-research-framework` | Reusable research framework templates |
| Full-stack security audit | `security-audit` | Evidence-graded findings under `.debug/` (audit-only, no fixes) |
| CI/CD or release | `gh-actions-architect` / `nodejs-npm-auto-release` | Workflow or release automation |

Every development task follows `Archive → Develop → Test → Update plan → commit/push only with explicit authorization`.

---

## 📚 Included Skills (`.gemini/skills/`)

- **ai-spec** — Full-stack architect & AI instruction optimizer. Translates natural-language requirements into production-ready specs and "god prompts".
- **deep-research** — Multi-agent parallel research engine for tech selection, literature, and competitor scans; supports citation management and lightweight quantitative validation.
- **dev-env-scan** — Detects local toolchain (OS, languages, package managers, GPU, containers) and interactively collects developer preferences.
- **dev-host-init** — One-command host bootstrap for a new machine: cross-platform environment probe, dev-tool gap checklist, codebase-memory-mcp deployment guidance, and a generated global/project injection doc (universal dev rules + machine-detected facts). Reachable via `/ai-spec init`.
- **intent-grill** — Alignment interrogator, one-question-at-a-time. Maintains CONTEXT.md (domain glossary + relationships + ambiguities).
- **api-first-modular** — Enforces three-layer separation (Frontend / BFF / Backend API packages) and the 5-step backend loop.
- **code-debugger** — Context-first debugging. Maintains `.debug/` documentation.
- **debug-ui** — Top-tier UI visual design & implementation. Bridges "make it pop" aesthetic intent with Tailwind/CSS engineering.
- **code-review** — Hybrid code review (OCR CLI × Agent). Structured High/Medium/Low classification.
- **codebase-context** — Knowledge-graph queries (impact analysis, call chains, dependency graphs, rename safety). codebase-memory MCP first (search_graph/trace_path/query_graph/Cypher), GitNexus/static-analysis fallback.
- **prd** — Interactive PRD generator with clarifying-question loop.
- **project-health-audit** — Pre-change evidence-backed health/debt baseline (HEALTH.md + debt register).
- **goal-driven-development** — Approved-SPEC execution engine: milestone loop, deterministic checks, spec-aware review, commit/push authorization gates.
- **iteration-manager** — Post-delivery residual classification (BUG/DEBT/PRD_AMENDMENT/SPEC_AMENDMENT/NEW_CHANGE) and next-Gate routing.
- **discover-skill-opportunities** — Skill opportunity mining from work evidence + session skill performance review.
- **sam-dev-cc-init** — PDCO loop development workflow initialization (CLAUDE.md/PROGRESS-LOG.md/TASKS.md/self.opt).
- **ai4s-dry-lab** — End-to-end AI4S dry-lab research engine: SPEC-driven, OODA loop, Gate control, W1-W4 mandatory records.
- **extract-research-framework** — Reverse-extract reusable research methodology frameworks from deep-research documents.
- **security-audit** — Full-stack security audit: codebase graph embed + stack-surface static audit + dependency CVE + public/internal pentest, evidence-graded report (audit-only, no fixes).
- **ralph** / **ralph-yolo** — Autonomous PRD execution loops.
- **ux-experience-audit** — User-journey-driven UX scanning and cross-layer fix loop.
- **loop-engineer** — Multi-skill package design: asset audit, gap analysis, orchestration layer.
- **gh-actions-architect** — GitHub Actions workflow generator (multi-ecosystem, multi-arch builds, releases).
- **nodejs-npm-auto-release** — Node.js/npm auto-release with version bump, changelog, publish.

---

## 🔒 Core Rules

- **API-First** — Backend features encapsulated as API packages; frontend consumes only.
- **Layer-scoped debugging** — Identify owning layer first, no cross-layer patches.
- **Research before opinion** — Tech selection or unfamiliar domain → `deep-research` first.
- **Repo Init + task loop** — `Archive → Develop → Test → Update plan → commit/push only with explicit authorization`.
- **Test artifact hygiene** — 测试产物卫生铁律。每次测试/验证/Checkfix 前后必须遵守 T0 测试前检查 → T1 测试后清扫 → T2 区分测试产物与运行数据（运行数据绝不删）→ T3 代码层老鼠屎清扫。完整规则见 `code-debugger` T0–T3。
- **Multi-agent deployment** — Installing CodeForge skills into other agents (Antigravity / OpenClaw / Hermes / WorkBuddy) follows the A/B classification in [`docs/agent-deployment-guide.md`](./docs/agent-deployment-guide.md).

---

## 🚀 How to Use

1. Ensure Gemini CLI is installed.
2. Navigate to this project root (or run `deploy/deploy.sh` / `deploy/deploy.ps1` to install globally).
3. Trigger a skill by describing your intent:
   - *"I need to design a user-auth feature"* → activates `ai-spec` / `prd`
   - *"Debug this failing endpoint"* → activates `code-debugger`
   - *"Make the dashboard feel modern and Swiss"* → activates `debug-ui`
   - *"Find the latest best-practice for edge-runtime auth in 2026"* → activates `deep-research`
