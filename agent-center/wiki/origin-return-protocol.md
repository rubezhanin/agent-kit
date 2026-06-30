# Origin Return Protocol (kit integration)

> Canonical English version. The original Russian protocol text lives at `agent-center/operations/origin-return-protocol/PROTOCOL.ru.md`. The English reference lives next to it at `PROTOCOL.en.md`. The skill wrapper is at `agent-center/skills/operations/origin-return-protocol/SKILL.md`.

This page explains how the protocol is wired into the kit. For the full text of the protocol itself, see `agent-center/operations/origin-return-protocol/PROTOCOL.en.md`.

## What the protocol is

The first rule of an agent operating loop:

> A task is closed only when the result returns to the place where it was requested.

A reply that ends with "Done." is not a closure — it is invisible to the owner. The protocol replaces that with five anchors and four statuses.

## Five anchors every task carries

| Anchor | Simple question |
| --- | --- |
| `origin` | Where did the request come from? |
| `owner` | Who is on the hook for the outcome? |
| `artifact` | Where is the result? |
| `status` | What is the status now? |
| `return_path` | Where does the final answer go? |

## Four statuses — no zoo

| Status | When |
| --- | --- |
| `DONE` | Result is ready, verified, and returned through `return_path`. |
| `BLOCKED` | The agent cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required (send, publish, delete, pay, change a live system). |
| `STALE` | Task stalled or went stale; needs a re-check. |

## How the kit enforces it

| Layer | Where it lands |
| --- | --- |
| Skill | `agent-center/skills/operations/origin-return-protocol/SKILL.md` |
| Reference text | `agent-center/operations/origin-return-protocol/PROTOCOL.en.md` + `PROTOCOL.ru.md` |
| Profile default | `main-operator.profile.json` and every active profile load the skill |
| Operating contract | `agent-center/AGENTS.md` and `AGENTS.ru.md` — first rule block |
| System prompt | `agent-center/prompts/main-agent-system.md` and `prompts/final-report.md` |
| Templates | `agent-center/templates/task-card.md` and `agent-center/templates/receipt.md` |
| Wiki | `agent-center/wiki/operating-contract.md` references the protocol |
| Docs | This page; mirrored in `docs/ORIGIN_RETURN_PROTOCOL.en.md` |

## Final answer shape

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: what was done
Artifact: path to the result
Verification: what was checked
Returned to: where the summary was returned
Blocked: what remains unresolved, if anything
```

## Quick self-test

Ask the agent:

```text
Create file test-result.md with one line: ORIGIN_RETURN_OK.
Use Origin Return Protocol.
Return status, path, verification, and final message.
```

A correct reply includes the five anchors and the final-answer shape above. A reply that reads "Did it." is a fail.

## For a single agent

The agent must always carry:

```text
origin: <chat, file, channel>
owner: <current agent or person>
artifact: <file path or message>
status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
return_path: <where the summary must land>
verification: <what was checked>
```

## For a team of agents

The owner of the task is one agent (usually the main operator). Specialists return receipts; the owner carries the receipt through `return_path`. The owner is responsible for visibility, not the worker.

## Read more

| Document | Purpose |
| --- | --- |
| [`agent-center/operations/origin-return-protocol/PROTOCOL.en.md`](../agent-center/operations/origin-return-protocol/PROTOCOL.en.md) | Full English reference. |
| [`agent-center/skills/operations/origin-return-protocol/SKILL.md`](../agent-center/skills/operations/origin-return-protocol/SKILL.md) | Skill wrapper, in-context loading. |
| [`agent-center/templates/task-card.md`](../agent-center/templates/task-card.md) | Task-card template with the anchors. |
| [`agent-center/templates/receipt.md`](../agent-center/templates/receipt.md) | Receipt template. |
| [`agent-center/AGENTS.md`](../agent-center/AGENTS.md) | Operator contract. |