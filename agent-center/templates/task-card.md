# Task Card — Origin Return Format

A card on a Kanban board (or in `reports/task-receipts/` fallback) carries the Origin Return anchors by default.

```md
# Task

## Origin
<where the request came from>

## Owner
<profile / person who is on the hook for the outcome>

## Assignee
<profile / person who actually does the work, if delegated>

## Goal
<one sentence>

## Status
DONE | BLOCKED | NEEDS_APPROVAL | STALE

## Artifact
<where the result will live>

## Return path
<where the final summary must land>

## Verification
- <what to check>
- <what to check>

## Allowed paths / data
- ...

## Forbidden paths / data
- ...

## Tools allowed
- ...

## Side-effect policy
- ...

## Output format
- ...

## Stop rules
- ...

## Dependencies
- ...

## Receipt path
`reports/task-receipts/<timestamp>-<slug>.md`
```

Rules:

- `origin` and `return_path` are mandatory for any non-trivial task.
- A task without `return_path` cannot transition to `DONE`.
- When status flips to `BLOCKED`, list exactly what is missing in the receipt.
- When status flips to `NEEDS_APPROVAL`, list the action, rollback and verification in the approval request, and stop until the owner responds.