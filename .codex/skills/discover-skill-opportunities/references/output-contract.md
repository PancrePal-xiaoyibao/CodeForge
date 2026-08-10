# Audit and candidate templates

## Consequential finding

```markdown
### Finding: <decision-relevant pattern>
- Status: observed | strongly supported | plausible | speculative
- Evidence: <artifact pointers and recurrence>
- Hidden leverage or risk: <why this matters>
- Decisions affected: <allocation, sequencing, control, delegation, tooling>
- Alternative explanation: <credible competing interpretation>
- Reversible next action: <small test>
```

## Cluster summary

```markdown
| Cluster | Episodes/evidence | Stable core | Main friction | Score | Disposition |
|---|---|---|---|---:|---|
```

Avoid false precision. Use ranges or qualitative recurrence when the corpus is sampled.

## Skill candidate specification

```markdown
### <rank>. <kebab-case-name>

**Job and value**
- User job:
- Evidence:
- Expected leverage:
- Why a skill beats simpler alternatives:

**Trigger contract**
- Trigger when:
- Positive examples:
- Do not trigger when:
- Negative examples:

**Inputs and prerequisites**
- Required:
- Optional:
- Missing-input behavior:

**Workflow**
1. ...

**Output contract and validation**
- Deliverables:
- Acceptance criteria:
- Human review gates:
- Failure/degraded modes:

**Reusable contents**
- SKILL.md:
- references/:
- scripts/:
- assets/:
- tool or connector dependencies:

**Risks and controls**
- Data/privacy:
- Domain risk:
- Scope boundary:

**Pilot plan**
- Test episodes:
- Success metrics:
- Stop/revise criteria:
```

## Portfolio recommendation

Rank the requested number of candidates, normally three. Favor a portfolio that covers distinct high-value jobs unless adjacent skills share resources and should deliberately form a parent-child package. Name overlaps with existing skills and recommend extension rather than duplication.
