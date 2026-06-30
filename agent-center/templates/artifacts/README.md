# Artifacts Index

> Origin-Return-aligned artifact templates. Copy the one you need, fill the Origin Return block at the top, and use it as the result of a task.

The Origin Return Protocol requires that every task leave an artifact. These templates pre-fill the five anchors (`origin` / `owner` / `artifact` / `status` / `return_path`) and the final-answer shape so the agent does not have to rebuild the contract from scratch.

## Templates

| Template | When | File |
| --- | --- | --- |
| Note | Short reference / one observation. | [`note.md`](note.md) |
| Report | Long analytical artifact with sources. | [`report.md`](report.md) |
| Brief | One-page summary for a stakeholder. | [`brief.md`](brief.md) |
| Summary | TL;DR of a completed task. | [`summary.md`](summary.md) |
| Hypothesis | Working assumption with falsification plan. | [`hypothesis.md`](hypothesis.md) |

## How to use

1. Copy the template you need (`templates/artifacts/<name>.md`).
2. Fill in the Origin Return block at the top: `origin`, `owner`, `artifact`, `status`, `return_path`.
3. Replace the section bodies with the actual content.
4. Save the file under the task's working directory or under `agent-center/reports/task-receipts/`.
5. Carry the path through `return_path` — the chat / channel where the owner waits.

## Status vocabulary

Only four statuses are recognised on the operator layer:

| Status | When |
| --- | --- |
| `DONE` | Result is ready, verified, and returned through `return_path`. |
| `BLOCKED` | Operator cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required. |
| `STALE` | Task stalled; needs a re-check. |

A template without `status:` or `return_path:` is a draft, not an artifact. The CI validator `scripts/check_orp.py` will fail the build.

## References in this repo

- `agent-center/operations/origin-return-protocol/PROTOCOL.en.md`
- `agent-center/skills/operations/origin-return-protocol/SKILL.md`
- `agent-center/templates/receipt.md`
- `agent-center/templates/task-card.md`
