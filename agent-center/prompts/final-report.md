# Final Report Format (Origin Return Protocol)

> Canonical English version. Russian localization: [`agent-center/prompts/final-report.ru.md`](agent-center/prompts/final-report.ru.md).

Use this after every task. The format is enforced by the **Origin Return Protocol**: a task is closed only when the result reaches `return_path`.

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: what was done
Artifact: path to the result
Verification: what was checked
Returned to: where the summary was returned (chat / file / channel)
Blocked: what remains unresolved, if anything
```

## Rules

- Do not claim `DONE` if the result did not reach `return_path`.
- Mention if verification was not run.
- Do not expose raw internal approval / tool blocks.
- A reply that ends with "Done." is invisible — it is not a closure.

## Anchor reminder

Every task carries five anchors:

| Anchor | Source |
| --- | --- |
| `origin` | Where the request came from. |
| `owner` | Who is on the hook for the outcome. |
| `artifact` | Where the result lives. |
| `status` | `DONE` / `BLOCKED` / `NEEDS_APPROVAL` / `STALE`. |
| `return_path` | Where the final answer must land. |

See [`../operations/origin-return-protocol/PROTOCOL.en.md`](../operations/origin-return-protocol/PROTOCOL.en.md).