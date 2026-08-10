# Software development opportunity patterns

## High-value recurring clusters

| Cluster | Evidence signals | Likely reusable contents | Validation |
|---|---|---|---|
| Repository onboarding and context reconstruction | Repeated architecture scans, conventions rediscovered, same setup questions | architecture map, search workflow, project conventions | required paths and commands resolve |
| Issue reproduction and debugging | Similar log collection, environment checks, hypothesis loops | diagnostic decision tree, log parsers, repro template | failing test or repro becomes deterministic |
| Code review and release gates | Repeated review criteria, missed checks, release checklists | review rubric, CI scripts, release template | tests, lint, security and artifact checks pass |
| Cross-platform configuration synchronization | Equivalent files drift across platforms | mapping reference, sync script, diff guard | mirrors and entry docs agree |
| Migration and dependency upgrades | Same compatibility research and staged rollout | migration playbook, codemods, rollback checklist | tests and compatibility matrix pass |
| Incident response and postmortems | Recurring triage, timelines, action tracking | severity rubric, evidence collector, postmortem template | timeline and actions are complete |

## Good skill boundaries

Package reasoning plus repository-specific conventions, tool commands, and quality gates. Split by materially different stacks or deployment risks. Prefer a script alone for deterministic formatting or file copying; prefer CI configuration for checks that must always run.

## Candidate evidence

Look for repeated shell commands, copied review comments, recurring missing context, nearly identical tickets, release regressions, or manual comparisons across files. Distinguish maintenance of a single repository from a reusable multi-project workflow.

## Risk controls

Require explicit authorization for destructive commands, production changes, releases, commits, pushes, credential operations, and external messages. Preserve user changes and define rollback or degraded behavior.
