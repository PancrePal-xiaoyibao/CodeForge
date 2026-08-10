# Skill opportunity scoring rubric

Score each dimension from 0 to 5. Keep raw scores visible.

| Dimension | Weight | A score of 5 means |
|---|---:|---|
| Recurrence | 15 | Repeated across periods, projects, or users with credible evidence |
| Process stability | 15 | Core steps and decision points are stable despite variable inputs |
| Reusable context | 10 | The same schemas, policies, examples, or domain rules are repeatedly reconstructed |
| Friction and time | 15 | The workflow consumes material effort, coordination, or attention |
| Error or omission cost | 15 | Missed steps cause meaningful rework, loss, delay, or control failure |
| Verifiability | 15 | Outputs have observable acceptance criteria or deterministic checks |
| Tool and resource leverage | 10 | Scripts, references, templates, or integrations materially improve execution |
| Strategic leverage | 5 | Packaging improves delegation, scale, consistency, or decision speed |

Calculate `weighted_score = sum(score / 5 * weight)`, yielding 0-100.

## Interpretation

- `75-100`: strong `BUILD_SKILL` candidate if no red flag applies.
- `60-74`: prototype or `PILOT_AS_SOP`; validate with more episodes.
- `40-59`: prefer a checklist, template, saved prompt, or small script.
- `<40`: keep ad hoc unless risk controls independently justify standardization.

## Red-flag caps

- Cap at 59 when fewer than two credible episodes support recurrence.
- Cap at 59 when the output cannot be evaluated and no review gate can be defined.
- Cap at 49 when the core method changes on almost every instance.
- Mark `AUTOMATE_DIFFERENTLY` when the task is deterministic data movement with negligible reasoning.
- Mark `KEEP_AD_HOC` when value comes primarily from unconstrained originality or one-off negotiation.
- Do not recommend autonomous execution for regulated advice, trading, payments, filings, publication claims, or production changes without explicit review and controls.

## Simpler-alternative test

Before recommending a skill, ask whether the dominant need is better served by:

1. a one-page checklist for human execution;
2. a reusable document or spreadsheet template;
3. a saved prompt with little domain context;
4. a deterministic script or scheduled integration;
5. a policy/reference document;
6. an update to an existing skill.

A new skill should win because it combines reusable reasoning, workflow, context, resources, and validation—not because it is fashionable.
