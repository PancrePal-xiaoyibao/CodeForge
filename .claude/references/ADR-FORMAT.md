# ADR Format Reference

Architecture Decision Records capture decisions that are **hard to reverse**, **surprising without context**, and **the result of a real trade-off**.

## When to Write an ADR

All three must be true:
1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, **skip the ADR**.

## File Location

```
docs/adr/NNNN-kebab-case-title.md
```

Number sequentially starting from `0001`.

## Template

```markdown
# ADR-NNNN: [Short Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

[What forces are at play? What problem are we solving? What constraints exist?
Keep it factual — this section explains WHY a decision was needed.]

## Decision

[What did we decide? State it clearly in one or two sentences.
Then explain the approach if needed.]

## Consequences

### Positive
- [Good thing that follows from this decision]
- [Another benefit]

### Negative
- [Trade-off we accepted]
- [Limitation this creates]

### Neutral
- [Something that changes but isn't clearly good or bad]
```

## Examples of Good ADR Titles

- `0001-use-event-sourcing-for-orders.md`
- `0002-postgres-for-write-model-redis-for-read.md`
- `0003-reject-graphql-in-favor-of-rest.md`
- `0004-monorepo-with-turborepo.md`

## Anti-patterns

- ADR for obvious choices ("use git for version control")
- ADR for easily reversible decisions ("use blue for the button")
- ADR without alternatives considered (if there's no trade-off, there's no decision)
- ADR as a spec (keep implementation details in code, not ADRs)
