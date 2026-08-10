# AGENTS.md — CodeForge Full-Stack AI Dev Engine (Codex / OpenAI Agents)

CodeForge is a community-driven **full-stack AI development engine**. This repository ships a pre-installed Codex skill suite that turns a blank Codex CLI environment into a **requirement → spec → API-First implementation → debug → UX → CI/CD → release** cockpit.

---

## 🎯 Lead Skill

Use `ai-spec` as the **default lead skill** for any unclear, architectural, cross-layer, or executable-instruction task. For external-information tasks (tech selection / literature / competitor scans), use `deep-research` first.

On first run in a new project, `ai-spec` must execute **Repo Init**: read or create `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`, extract project philosophy, environment, testing commands, developer preferences, encoding rules, plan docs, and approval boundaries.

---

## 📚 Available Skills

| Skill | Trigger Scenarios | Path |
|-------|-------------------|------|
| `ai-spec` | Natural-language requirements → precise technical spec translation | `.codex/skills/ai-spec/` |
| `deep-research` | External information gathering, tech selection, literature, competitor scans | `.codex/skills/deep-research/` |
| `dev-env-scan` | New project environment scan, preferences, onboarding | `.codex/skills/dev-env-scan/` |
| `intent-grill` | Requirement disambiguation, CONTEXT.md maintenance | `.codex/skills/intent-grill/` |
| `project-health-audit` | Pre-change health/debt baseline for refactoring, migration, major features | `.codex/skills/project-health-audit/` |
| `prd` | Generate structured PRD documents | `.codex/skills/prd/` |
| `goal-driven-development` | Approved-SPEC execution, milestone loop, commit/push authorization gates | `.codex/skills/goal-driven-development/` |
| `iteration-manager` | Post-delivery residual classification and next iteration routing | `.codex/skills/iteration-manager/` |
| `api-first-modular` | Frontend/backend development, cross-layer decomposition, API design | `.codex/skills/api-first-modular/` |
| `code-debugger` | Bug fixing, performance tuning, incremental development | `.codex/skills/code-debugger/` |
| `debug-ui` | Frontend UI debugging — styling, interaction, rendering | `.codex/skills/debug-ui/` |
| `code-review` | Code review (OCR CLI first, Agent fallback), High/Medium/Low classification | `.codex/skills/code-review/` |
| `codebase-context` | Codebase knowledge-graph queries (codebase-memory MCP first, GitNexus/static fallback) | `.codex/skills/codebase-context/` |
| `ralph` | Autonomous development loop driven by PRD | `.codex/skills/ralph/` |
| `ralph-yolo` | Ralph lightweight mode — sub-agents directly, no Amp CLI required | `.codex/skills/ralph-yolo/` |
| `ux-experience-audit` | User-journey UX scanning, prioritization & fix loop | `.codex/skills/ux-experience-audit/` |
| `loop-engineer` | Multi-skill package design — audit, gap analysis, orchestration layer | `.codex/skills/loop-engineer/` |
| `discover-skill-opportunities` | Skill opportunity mining from work evidence, session skill performance review | `.codex/skills/discover-skill-opportunities/` |
| `sam-dev-cc-init` | PDCO loop development workflow initialization (CLAUDE.md/PROGRESS-LOG/TASKS/self.opt) | `.codex/skills/sam-dev-cc-init/` |
| `ai4s-dry-lab` | End-to-end AI4S dry-lab engine — SPEC-driven, OODA loop, Gate control (W1-W4) | `.codex/skills/ai4s-dry-lab/` |
| `extract-research-framework` | Reverse-extract reusable research methodology frameworks from deep-research docs | `.codex/skills/extract-research-framework/` |
| `nodejs-npm-auto-release` | Node.js / npm auto-release | `.codex/skills/nodejs-npm-auto-release/` |
| `gh-actions-architect` | GitHub Actions CI/CD workflow (multi-ecosystem, multi-arch) | `.codex/skills/gh-actions-architect/` |

---

## 🗺️ Skill Routing Network

| Scenario | Route | Output |
|----------|-------|--------|
| New repository / first agent run | `dev-env-scan` → `ai-spec` | Environment profile + initialized project workflow |
| Vague requirement | `intent-grill` → `ai-spec` | Clarified intent + technical spec |
| External info / tech selection / literature | `deep-research` → `ai-spec` | Structured research + citations |
| Pre-change health baseline | `project-health-audit` → `prd` / `ai-spec` | Debt register + change-impact map |
| Product feature from scratch | `prd` → `ai-spec` → `api-first-modular` | PRD + implementation plan + API packages |
| Full-stack feature | `ai-spec` → `api-first-modular` → `code-review` | Backend-first, docs, frontend integration, review |
| Approved-SPEC execution | `goal-driven-development` → `api-first-modular` → `code-review` | Evidence-backed milestone loop + authorization gates |
| Bug or regression | `codebase-context` → `code-debugger` → targeted tests | Owning layer identified before edits |
| UI rendering / visual issue | `debug-ui` → `ux-experience-audit` when workflow impact | Visual fix + user journey verification |
| UX "works but feels broken" | `ux-experience-audit` → `api-first-modular` or `code-debugger` | Cross-layer diagnosis and fix plan |
| Large autonomous build | `prd` or `ai-spec` → `ralph` / `ralph-yolo` | Story-by-story implementation loop |
| Post-delivery iteration | `iteration-manager` | Residual classification + next Gate routing |
| Package or skill system design | `loop-engineer` → `ai-spec` as needed | Gap analysis + multi-skill orchestration |
| Skill opportunity mining | `discover-skill-opportunities` | Evidence-based skill candidates + session review |
| Project workflow bootstrap | `sam-dev-cc-init` | PDCO loop files (CLAUDE.md/PROGRESS-LOG/TASKS/self.opt) |
| Computational dry-lab research | `ai4s-dry-lab` | SPEC-driven OODA loop with W1-W4 enforcement |
| Methodology extraction | `extract-research-framework` | Reusable research framework templates |
| CI/CD or release | `gh-actions-architect` / `nodejs-npm-auto-release` | Validated workflow or npm release path |

---

## 🔒 Core Rules

- **API-First** — Every backend feature must be encapsulated as an independent API package (Implement → Checkfix → Encapsulate → Expose API → Document API). Frontend consumes APIs per documentation only — no business logic in the frontend.
- **Layer-scoped debugging** — Identify the bug's owning layer before making changes. Never apply cross-layer workarounds.
- **Ordered cross-layer execution** — Backend first → API docs → frontend consumption → integration verification.
- **Research before opinion** — Tech selection or unfamiliar domains → `deep-research` first, do not answer from stale memory.
- **Repo Init + task loop** — `Archive → Develop → Test → Update plan → commit/push only with explicit authorization`.
- **Multi-agent deployment** — Installing CodeForge skills into other agents (Antigravity / OpenClaw / Hermes / WorkBuddy) follows the A/B classification in [`docs/agent-deployment-guide.md`](./docs/agent-deployment-guide.md).
