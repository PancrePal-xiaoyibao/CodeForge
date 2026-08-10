# Evidence, provenance, and privacy

## Source inventory

Record each source as `source_id`, type, accessible range, owner, sensitivity, completeness, and location. Prefer stable artifact pointers such as file paths, ticket IDs, dates, or conversation identifiers over long quotations.

Possible sources include conversation exports, task trackers, commit history, code review, meeting notes, SOPs, spreadsheets, reports, calendars, support tickets, experiment logs, and user-provided memory summaries. Availability is platform-specific; never imply access that was not demonstrated.

## Evidence levels

- `Direct`: an artifact shows the task, decision, output, or validation.
- `Corroborated`: two or more independent artifacts support the pattern.
- `Inferred`: the pattern is a reasonable explanation but is not directly recorded.
- `Unknown`: evidence is insufficient or contradictory.

Attach at least one pointer to every cluster and two independent pointers for a consequential hidden finding when possible.

## Sampling large corpora

Use full review when feasible. Otherwise declare one method:

- time-stratified sample across early, middle, and recent periods;
- source-stratified sample across conversations, tickets, files, and reports;
- event-focused sample around launches, closes, submissions, incidents, or decisions;
- random or systematic interval sample.

Check the proposed top clusters against a second sample before final ranking. State that counts are sample estimates rather than corpus totals.

## Data minimization

- Request only the evidence needed to identify workflow structure.
- Replace names, account numbers, credentials, client identifiers, unpublished results, and health details with neutral tokens.
- Do not reproduce secrets in the audit. If encountered, report the category and location without exposing the value.
- Keep personal evaluation out of scope. Analyze process behavior, not identity or character.
- Respect retention, access-control, contractual, and regulatory constraints supplied by the user or workspace.

## Conflict handling

When evidence conflicts, show both signals, prefer newer or directly observed artifacts only with justification, and lower confidence. Do not merge workflows merely because their surface language is similar.
