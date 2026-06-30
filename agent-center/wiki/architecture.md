# Agent System Architecture

## Layers

| Layer | Role |
| --- | --- |
| Human owner | Sets goals, approvals, privacy and final business decisions. |
| Gateway / CLI | Entry points. Must batch inputs and avoid leaking internal tool state. |
| Main operator | Triage, routing, Kanban, final answer and quality gate. |
| Specialist skills/profiles | Narrow tasks with bounded outputs. |
| Kanban | Durable execution for long tasks and multi-agent handoff. |
| Wiki | Canonical structured knowledge. |
| References | Long source documents and imported kits. |
| Reports | Receipts, audits, incidents and evidence. |
| Memory index | Read-only search over sources. Not canonical truth. |
| Maintenance | Health, skill hygiene, token diagnostics and stale task review. |

## Design Principles

1. One operator owns routing.
2. Specialists are invoked only when they reduce risk.
3. Long tasks live in Kanban, not in chat memory.
4. Wiki and reports beat memory.
5. Retrieval is search, not truth.
6. External actions need approval.
7. Every non-trivial run leaves a receipt.

