# Kanban Board Contract

Kanban is the durable execution layer.

Do not assume Kanban exists. First verify live Hermes commands.

Expected discovery:

```bash
hermes --version
hermes kanban --help
hermes dashboard --help
hermes profile list
```

If Kanban is unavailable, use a temporary report/task-log fallback and recommend upgrade. Do not fake Kanban with prompt-only state.

## Task Card Fields

- title;
- goal;
- status;
- assignee;
- priority;
- dependencies;
- workspace;
- allowed paths/data;
- forbidden paths/data;
- side-effect policy;
- expected output;
- verification;
- receipt path;
- blocker/approval needed.

## Statuses

| Status | Meaning |
| --- | --- |
| triage | Captured, not yet shaped. |
| todo | Understood but not ready. |
| ready | Ready to run. |
| running | Agent is working. |
| blocked | Needs data, access or approval. |
| review | Result needs check. |
| done | Completed and verified. |
| archived | No longer active. |

