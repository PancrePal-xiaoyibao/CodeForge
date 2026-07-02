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
| New repository / first agent run | `dev-env-scan` → `ai-spec` | Environment profile + project workflow |
| Vague requirement | `intent-grill` → `ai-spec` | Clarified spec |
| External info / tech selection / literature | `deep-research` → `ai-spec` | Structured research + citations |
| Product feature from scratch | `prd` → `ai-spec` → `api-first-modular` | PRD + implementation plan |
| Full-stack feature | `ai-spec` → `api-first-modular` → `code-review` | API-first implementation + review |
| Bug or regression | `codebase-context` → `code-debugger` | Impact map + targeted fix |
| UI visual issue | `debug-ui` → `ux-experience-audit` | Visual polish + workflow check |
| UX issue across layers | `ux-experience-audit` → `code-debugger` or `api-first-modular` | Cross-layer diagnosis |
| Autonomous implementation | `prd` or `ai-spec` → `ralph` / `ralph-yolo` | Story loop execution |
| Package / multi-skill system | `loop-engineer` → `ai-spec` | Skill network design |
| CI/CD or release | `gh-actions-architect` / `nodejs-npm-auto-release` | Workflow or release automation |

Every development task follows `Archive → Develop → Test → Update plan → commit/push only with explicit authorization`.

---

## 📚 Included Skills (`.gemini/skills/`)

- **ai-spec** — Full-stack architect & AI instruction optimizer. Translates natural-language requirements into production-ready specs and "god prompts".
- **deep-research** — Multi-agent parallel research engine for tech selection, literature, and competitor scans; supports citation management and lightweight quantitative validation.
- **dev-env-scan** — Detects local toolchain (OS, languages, package managers, GPU, containers) and interactively collects developer preferences.
- **intent-grill** — Alignment interrogator, one-question-at-a-time. Maintains CONTEXT.md (domain glossary + relationships + ambiguities).
- **api-first-modular** — Enforces three-layer separation (Frontend / BFF / Backend API packages) and the 5-step backend loop.
- **code-debugger** — Context-first debugging. Maintains `.debug/` documentation.
- **debug-ui** — Top-tier UI visual design & implementation. Bridges "make it pop" aesthetic intent with Tailwind/CSS engineering.
- **code-review** — Hybrid code review (OCR CLI × Agent). Structured High/Medium/Low classification.
- **codebase-context** — Knowledge-graph queries (impact analysis, call chains, dependency graphs, rename safety) via GitNexus MCP/CLI with static-analysis fallback.
- **prd** — Interactive PRD generator with clarifying-question loop.
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

---

## 🚀 How to Use

1. Ensure Gemini CLI is installed.
2. Navigate to this project root (or run `deploy/deploy.sh` / `deploy/deploy.ps1` to install globally).
3. Trigger a skill by describing your intent:
   - *"I need to design a user-auth feature"* → activates `ai-spec` / `prd`
   - *"Debug this failing endpoint"* → activates `code-debugger`
   - *"Make the dashboard feel modern and Swiss"* → activates `debug-ui`
   - *"Find the latest best-practice for edge-runtime auth in 2026"* → activates `deep-research`
