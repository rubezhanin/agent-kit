# Origin Return Protocol — kit integration

> Mirrors `agent-center/wiki/origin-return-protocol.md`. Russian: see the locale switcher.

The first rule of the kit:

> A task is closed only when the result returns to the place where it was requested.

A reply that ends with "Done." is not a closure — it is invisible to the owner. The kit bakes the protocol into the contract, the templates and the skills.

## Five anchors every task carries

| Anchor | Question |
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
| `BLOCKED` | Agent cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required (send, publish, delete, pay, change a live system, use a secret). |
| `STALE` | Task stalled or went stale; needs a re-check. |

## Final answer shape

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: what was done
Artifact: path to the result
Verification: what was checked
Returned to: where the summary was returned
Blocked: what remains unresolved
```

A reply that ends with `Done.` alone is not a closure — it is invisible.

## How the kit enforces it

| Layer | Where it lands |
| --- | --- |
| Skill wrapper | `agent-center/skills/operations/origin-return-protocol/SKILL.md` |
| Reference text | `agent-center/operations/origin-return-protocol/PROTOCOL.en.md` |
| Profile default | `main-operator.profile.json` (and every active profile) loads the skill |
| Operating contract | `agent-center/AGENTS.md` — first rule block |
| System prompt | `agent-center/prompts/main-agent-system.md` |
| Final-answer shape | `agent-center/prompts/final-report.md` |
| Templates | `agent-center/templates/task-card.md` + `agent-center/templates/receipt.md` |
| Wiki page | `agent-center/wiki/origin-return-protocol.md` |

## Self-test for the operator

Before responding to the owner, answer four questions:

```text
Where is the result?
What was verified?
Where did the result land?
What is still blocked?
```

If any answer is empty, the task is not closed.

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

For the original protocol text — the full Russian write-up with the reasoning behind each status — see [`agent-center/operations/origin-return-protocol/PROTOCOL.en.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/operations/origin-return-protocol/PROTOCOL.en.md) in this repository.