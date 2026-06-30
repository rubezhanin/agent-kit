# Operating Contract

## Origin Return Protocol

Every task — short or long — carries the five anchors:

- `origin` — where the request came from;
- `owner` — who is on the hook for the outcome;
- `artifact` — where the result lives;
- `status` — `DONE` / `BLOCKED` / `NEEDS_APPROVAL` / `STALE`;
- `return_path` — where the final answer lands.

A task is closed only when the result reaches `return_path`. The system default reply shape is documented in [`agent-center/prompts/final-report.md`](../prompts/final-report.md); receipts are emitted per [`agent-center/templates/receipt.md`](../templates/receipt.md).

Full protocol text is kept at `agent-center/operations/origin-return-protocol/PROTOCOL.en.md`.

## Non-Destructive Default

The system starts read-only.

Writes, external calls, account actions, publishing, sending, payment, deletion, production changes and secrets require explicit approval.

## Approval Request Must Include

- exact action;
- reason;
- target path/account/system;
- expected effect;
- rollback path;
- verification plan.

Approval requests are answered by the owner, never silently fulfilled.

## Evidence Standard

The phrase "done" is not evidence.

Evidence is:

- changed file path;
- diff or artifact;
- command/check result;
- source ledger;
- receipt (per the Origin Return format);
- human approval record.

## Context Discipline

- Keep root instructions short.
- Put long details into `references/` and skill source files.
- Read only relevant sections.
- Use Kanban/reports instead of carrying long task history in chat.

