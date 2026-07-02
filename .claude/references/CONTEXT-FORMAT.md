# CONTEXT.md Format Reference

This file defines the canonical format for `CONTEXT.md` — the shared domain language document maintained by the `/intent-grill` skill.

## Purpose

CONTEXT.md is a **glossary and nothing else**. It captures the precise meanings of domain terms so that AI agents and developers share the same vocabulary. It is NOT a spec, a scratchpad, or an implementation guide.

## Structure

```markdown
# [Project Name] Context

## Language

**[Term]**:
[One clear sentence defining this term in the project's domain.]
_Avoid_: [terms that are easily confused with this one]

**[Another Term]**:
[Definition.]
_Avoid_: [confusable terms]

## Relationships

- A **[Term A]** contains many **[Term B]**
- A **[Term C]** can only apply to a **[Term A]** in state `pending`

## Flagged Ambiguities

- "[word]" is used in code to mean both X and Y — needs resolution
- "[word]" means different things in module A vs module B
```

## Rules

1. **One term per entry** — don't bundle related terms
2. **Definition is domain-level** — no implementation details (no "stored in column X")
3. **_Avoid_ is mandatory** — every term must list at least one confusable alternative
4. **Relationships are structural** — "A has many B", not "A calls B.save()"
5. **Flagged Ambiguities are temporary** — resolve them during grilling, then promote to Language
6. **Update inline** — don't batch; capture terms the moment they're clarified
7. **Keep it short** — if CONTEXT.md exceeds 2 pages, the domain model needs refactoring

## Multi-Context Repos

If a repo has multiple bounded contexts, use a `CONTEXT-MAP.md` at root:

```markdown
# Context Map

| Context | Path | Description |
|---------|------|-------------|
| Ordering | src/ordering/CONTEXT.md | Order lifecycle and fulfillment |
| Billing | src/billing/CONTEXT.md | Payment processing and invoicing |

## Cross-Context Terms

- **Customer** in Ordering = **Payer** in Billing (same entity, different roles)
```

Each bounded context gets its own `CONTEXT.md` in its directory.
