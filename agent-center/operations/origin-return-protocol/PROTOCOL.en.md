# Origin Return Protocol — reference (English)

> Canonical English reference for the operation. The skill wrapper lives at `agent-center/skills/operations/origin-return-protocol/SKILL.md`. The Russian original lives next to this file as `PROTOCOL.ru.md`.

The first rule for an agent: **return the result to where it was requested**.

If you are just starting to assemble an agent, do not start with a big architecture. Not with a team of ten roles. Not with memory. Not with a Kanban. Not with a pretty diagram.

Start by checking one boring thing: does the agent return the result to where it was requested?

In real work, that is exactly where everything breaks.

## Why this matters at all

One agent is still easy to keep in your head. You wrote to it in Telegram, it replied there. Done.

Add at least one more layer and confusion starts:

- the agent creates a file;
- the agent starts a long task;
- the agent hands work to another agent;
- the agent runs through cron;
- the agent parks a task in Kanban;
- the agent drafts, another agent reviews;
- the agent writes "done" but attaches nothing.

Now the human who asked is sitting there, lost:

- where is the result;
- who is responding now;
- what was checked;
- why the agent is silent;
- whether it is ready to use.

For the human, the task is not done. It is lost.

## Main rule

A task is closed only when the result returns to the origin point.

Not when the model finished answering. Not when a file was created. Not when a card became `done`. Not when another agent wrote something in its own window.

It is closed when the human receives a clear summary:

```text
what was done
where the result lives
what was verified
what remains blocked
```

If that is missing, the task is not closed.

## The five things a task must carry

| Field | Simple question |
| --- | --- |
| `origin` | Where did the task come from? |
| `owner` | Who is on the hook for the outcome? |
| `artifact` | Where is the result? |
| `status` | What is the status now? |
| `return_path` | Where does the final answer go? |

That's the entire first layer. Until these five anchors exist, the agent may be doing work, but the system is already blind.

## Mini template

```yaml
origin:
owner:
request:
artifact:
status:
return_path:
verification:
final_message:
```

## Statuses without a zoo

Four statuses are enough.

| Status | Use when |
| --- | --- |
| `DONE` | Result is ready, verified, and returned to where it was requested. |
| `BLOCKED` | Agent cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required: send, publish, delete, pay, change a live system. |
| `STALE` | Task stalled or went stale; needs a re-check. |

The most common error is to set `DONE` when the agent only finished locally. That status must not be counted as `DONE`. It is just a trace somewhere in the system.

## What the agent must return at the end

```text
Status: DONE
Outcome: what was done
Artifact: where the result lives
Verification: what was verified
Returned to: where the summary was returned
Blocked: what remains unresolved, if anything
```

A bad reply:

```text
Done.
```

Why it is bad: it is unclear what is done, where it lives, and whether it can be trusted.

## When the agent must stop

The agent must not silently do external-effect actions. It must return `NEEDS_APPROVAL` for:

- sending a message on behalf of a human;
- publishing a post;
- deleting or overwriting user data;
- changing a live service setting;
- spending money;
- using secrets, tokens, cookies or OAuth;
- writing to a client, partner or external human;
- accepting legal, financial or medical final decisions without a human.

This is also part of the return path. The human must understand not only where the result lives, but also where the agent stopped.

## Quick self-test

Ask the agent:

```text
Create file test-result.md with one line: ORIGIN_RETURN_OK.
Use Origin Return Protocol.
Return status, path, verification, and final message.
```

Good reply:

```text
Status: DONE
Artifact: ./test-result.md
Verification: file created, line ORIGIN_RETURN_OK verified
Returned to: current chat
Blocked: none
```

Bad reply:

```text
Did it.
```

If the agent replies the second way, it is too early to give it long chains, other agents, or background tasks. First teach it to close the loop.

## Why this is the first layer

Memory is needed.
Kanban is needed.
Agent roles are needed.
Verification is needed.

But if the result does not return to the origin point, all of that just breeds noise. There are more places where work can be lost.

So the first layer is this simple:

```text
request -> owner -> work -> result -> verification -> return
```

Get this right first. Only then add Kanban, memory, roles, verification, handoff and a proper agent team.

## Short formula

```text
No origin     -> the agent does not know where the task came from.
No owner      -> no one answers for the outcome.
No artifact   -> the result cannot be found.
No verification -> the result cannot be trusted.
No return_path -> the task is not finished.
```

This is where the agent operating loop should start.