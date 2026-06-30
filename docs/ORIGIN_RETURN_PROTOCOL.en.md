# Origin Return Protocol (kit integration)

> Canonical English version. Russian localization: [`agent-center/wiki/origin-return-protocol.ru.md`](../agent-center/wiki/origin-return-protocol.ru.md).

Mirror of `agent-center/wiki/origin-return-protocol.md` for the docs site.

## What the protocol is

The first rule of an agent operating loop:

> A task is closed only when the result returns to the place where it was requested.

A reply that ends with "Done." is not a closure — it is invisible to the owner.

## Five anchors

| Anchor | Question |
| --- | --- |
| `origin` | Where did the request come from? |
| `owner` | Who is on the hook for the outcome? |
| `artifact` | Where is the result? |
| `status` | What is the status now? |
| `return_path` | Where does the final answer go? |

## Four statuses

| Status | When |
| --- | --- |
| `DONE` | Result is ready, verified, and returned through `return_path`. |
| `BLOCKED` | Cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required. |
| `STALE` | Task stalled; needs a re-check. |

## Final answer shape

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: what was done
Artifact: path to the result
Verification: what was checked
Returned to: where the summary was returned
Blocked: what remains unresolved
```

## Where the kit enforces it

- Skill: `agent-center/skills/operations/origin-return-protocol/SKILL.md`.
- Reference: `agent-center/operations/origin-return-protocol/PROTOCOL.en.md`.
- Loaded by: every active profile (including `main-operator`).
- Operating contract: `agent-center/AGENTS.md` — first rule block.
- Templates: `agent-center/templates/task-card.md` and `agent-center/templates/receipt.md`.

## Quick self-test

Ask the agent:

```text
Create file test-result.md with one line: ORIGIN_RETURN_OK.
Use Origin Return Protocol.
Return status, path, verification, and final message.
```

A correct reply includes all five anchors and the final-answer shape above. A reply that reads "Did it." is a fail.

## Read more

| Document | Purpose |
| --- | --- |
| [`agent-center/operations/origin-return-protocol/PROTOCOL.en.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/operations/origin-return-protocol/PROTOCOL.en.md) | Full English reference. |
| [`agent-center/skills/operations/origin-return-protocol/SKILL.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/skills/operations/origin-return-protocol/SKILL.md) | Skill wrapper. |
| [`agent-center/templates/task-card.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/templates/task-card.md) | Task-card template. |
| [`agent-center/templates/receipt.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/templates/receipt.md) | Receipt template. |
| [`agent-center/AGENTS.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/AGENTS.md) | Operator contract. |