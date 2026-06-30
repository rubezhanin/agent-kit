---
name: origin-return-protocol
description: Use on every task before it leaves the operator's hands — file creation, long runs, cron, Kanban delegation, subagent handoff. Forces the operator to keep five anchors (origin / owner / artifact / status / return_path) and never close a task as DONE until the result reached return_path.
---

# Origin Return Protocol

> The first layer of agent operations. Mirrors `agent-center/operations/origin-return-protocol/PROTOCOL.en.md` for in-context loading.

A task is closed only when the result reached the place where it was requested. Not when the model finished answering. Not when a file was created. Not when a card moved to `done`. Not when another agent wrote something in its own window.

When `return_path` has not been hit, the task is **lost** from the owner's point of view.

## Five anchors every task must carry

| Anchor | Simple question |
| --- | --- |
| `origin` | Where did the request come from? |
| `owner` | Who is on the hook for the outcome? |
| `artifact` | Where is the result? |
| `status` | What is the current state? |
| `return_path` | Where should the final answer land? |

If any of these is empty, the agent itself does not know where the task lives.

## Status (no zoo)

Use only four statuses:

| Status | When |
| --- | --- |
| `DONE` | Result is ready, verified, and delivered back through `return_path`. |
| `BLOCKED` | Agent cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required (send, publish, delete, pay, change a live system, use a secret). |
| `STALE` | Task stalled or went stale; needs a re-check. |

Marking `DONE` while the agent only finished locally is the most common error. That is not `DONE`; that is a track somewhere inside the system.

## Final answer shape

```text
Status:
Outcome:
Artifact:
Verification:
Returned to:
Blocked:
```

A reply that reads just "Done." is not a closure — it is invisible.

## Block conditions (also part of the return path)

Stop and return `NEEDS_APPROVAL` when the task asks for:

- sending a message on behalf of a human;
- publishing a post;
- deleting or overwriting user data;
- changing a live service setting;
- spending money;
- using secrets, tokens, cookies or OAuth;
- writing to a client, partner, or external human;
- a legal, financial or medical final decision without a human.

When `BLOCKED`, write what is missing in the `Blocked:` line of the final answer.

## When to load this skill

- whenever a task creates a file;
- whenever a task starts a long-running operation;
- whenever work goes into cron, Kanban, background, or another agent;
- whenever a specialist returns a receipt to the main operator;
- before the operator says "Done." to the owner.

## Mini template

```yaml
origin:
owner:
assignee:
request:
artifact:
status:
return_path:
verification:
final_message:
```

## Worked example

```yaml
origin: Telegram DM with the owner
owner: main-operator
assignee: researcher
request: short MD note on the first layer of agent operations
artifact: ./ORIGIN_RETURN_PROTOCOL.md
verification: file created, text reviewed, no private data inside
return_path: original Telegram DM
status: DONE
final_message: file attached below
```

## Self-test for the operator

Before responding to the owner, answer four questions:

```text
Where is the result?
What was verified?
Where did the result land?
What is still blocked?
```

If the operator cannot answer, the task is not closed.

## References in this repo

- [`agent-center/operations/origin-return-protocol/PROTOCOL.en.md`](../../operations/origin-return-protocol/PROTOCOL.en.md) — full English reference.
- [`agent-center/operations/origin-return-protocol/PROTOCOL.ru.md`](../../operations/origin-return-protocol/PROTOCOL.ru.md) — original Russian text.
- [`agent-center/templates/task-card.md`](../../templates/task-card.md) — Kanban / receipt template using these anchors.
- [`agent-center/prompts/final-report.md`](../../prompts/final-report.md) — final-answer format.
- [`agent-center/AGENTS.md`](../../AGENTS.md) — operating contract (Stop rules, return path).
