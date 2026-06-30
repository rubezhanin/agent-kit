# Context Management

> Canonical English version. The reference pack with deeper detail lives at `source/core/context-management-guide.md`.

Long sessions are where Hermes-style agents break down — not because the model gets tired, but because the context window fills up. This page gives the kit's stance on context hygiene.

## The problem in one diagram

```text
┌───────────────────────────────────────────────────┐
│            LEVEL 1 — PREVENTION                   │
│   Don't load what you don't need.                 │
│   - Light system prompt (pointers, not bodies)    │
│   - Subagents for heavy work                      │
│   - Capped reads (offset / limit)                 │
│   - No full dumps of cron lists, logs, configs    │
└─────────────────────┬─────────────────────────────┘
                      ▼
┌─────────────────────┴─────────────────────────────┐
│            LEVEL 2 — MONITORING                   │
│   Know how full the window is.                    │
│   - Per-turn status checks                        │
│   - Auto context check cron (every 30 min)        │
│   - Thresholds: 60% → 70% → 75% → 80%            │
└─────────────────────┬─────────────────────────────┘
                      ▼
┌─────────────────────┴─────────────────────────────┐
│            LEVEL 3 — GRACEFUL SAVE                │
│   When full — save and bounce.                    │
│   - Handoff file (save game)                      │
│   - Session diary                                 │
│   - Fresh /new, with memory reattached            │
└───────────────────────────────────────────────────┘
```

## What the kit already does for you

| Source of bloat | Mitigation in this kit |
| --- | --- |
| Heavy `AGENTS.md` | `agent-center/AGENTS.md` is intentionally short. Long details live in `wiki/` and `references/`. |
| All skills in every prompt | Skills are loaded only when a trigger matches; source-pack files in `source/` are not loaded by default. |
| Unbounded cron lists | `agent-center/config/cron-jobs.yaml` keeps jobs small and read-only. |
| Random file reads | `agent-center/AGENTS.md` directs the operator to read only relevant sections. |
| Skill metadata | The `skill-hygiene-audit` skill flags oversized skills and stale descriptions. |

## Thresholds

| Context % | Action |
| --- | --- |
| `< 60%` | Normal operation. |
| `60–70%` | Push heavy work into specialists / Kanban; coordinator only routes. |
| `70–75%` | STOP. Write a handoff note + session diary. Warn the user. |
| `75–80%` | Recommend `/new` with memory reattached. |
| `> 80%` | STOP. Force handoff. Do not continue the current thread. |

## Handoff format

A handoff note should be small enough to live in `agent-center/reports/task-receipts/<timestamp>-handoff.md`:

```md
# Handoff

## Goal
- ...

## State so far
- ...

## Next concrete step
- ...

## Open questions
- ...
```

## Subagent pattern

Use subagents or specialists whenever a task would consume more than one tool call's worth of context:

- Reading a file with `> 100` lines.
- Research with `> 3` search calls.
- Multi-file analysis.
- Content generation (posts, docs, briefings).

The main session then receives a short receipt, not the whole transcript.

## What the kit does NOT do

- It does not chunk context automatically — the agent and the operator must read thresholds and act.
- It does not silently compact — compaction is a logged operation.
- It does not pretend that bigger windows fix the underlying hygiene problem. Bigger windows buy time, not safety.

## References in this repo

- `source/core/context-management-guide.md` — full upstream guide.
- `agent-center/AGENTS.md` — operating contract and source-of-truth layering.
- `agent-center/skills/operations/skill-hygiene-audit/SKILL.md` — weekly context hygiene.
- `agent-center/skills/operations/hermes-token-drain-diagnostic/SKILL.md` — token drain diagnostic.