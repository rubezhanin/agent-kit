# Receipt — Origin Return Format

Save this file under `agent-center/reports/task-receipts/<timestamp>-<short-slug>.md` after every task closes.

```md
# Receipt

## Date: <YYYY-MM-DD HH:MM>
## Origin: <where the request came from>
## Owner: <who is on the hook>
## Assignee: <who actually did the work, if delegated>
## Request: <what was asked, in one or two sentences>
## Artifact: <path to the result>
## Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
## Returned to: <where the summary was returned>
## Verification:
- <what was checked>
- <what was checked>

## Outcome
- <what was done>

## Blocked
- <what remains unresolved, if anything>

## Artifacts
- <path-1>
- <path-2>

## Next step
- <what should happen next, if anything>

## Source ledger (when applicable)
- <source path> — <claim>
```

If `status` is anything other than `DONE`, the task is not closed. The receipt still goes into `reports/task-receipts/` because the operator and owner need to see what was tried.

This template is the audit trail of the **Origin Return Protocol**.
