# Artifact Templates

> Mirrors `agent-center/templates/artifacts/README.md` for the docs site.

The Origin Return Protocol requires that every task leaves an **artifact** — a file the owner can open. These templates pre-fill the five anchors so the operator does not rebuild them from scratch.

## Templates

| Template | When |
| --- | --- |
| **Note** | Short reference, one observation. |
| **Report** | Long analytical artifact with sources. |
| **Brief** | One-page summary for a stakeholder. |
| **Summary** | TL;DR of a completed task. |
| **Hypothesis** | Working assumption with falsification plan. |

Each template lives at `agent-center/templates/artifacts/<name>.md`. Copy, fill, save, and carry the path back through `return_path`.

## Origin Return block (top of every template)

```yaml
origin:
owner:
artifact: ./<this-file>.md
status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
return_path:
verification:
```

A template without `status:` or `return_path:` is a draft, not an artifact. CI validator `scripts/check_orp.py` will fail the build.

## Status vocabulary

Only four statuses are recognised at the operator layer:

| Status | When |
| --- | --- |
| `DONE` | Result is ready, verified, and returned through `return_path`. |
| `BLOCKED` | Operator cannot continue without a file, access, decision or context. |
| `NEEDS_APPROVAL` | External effect required. |
| `STALE` | Task stalled or went stale; needs a re-check. |

## Self-test

```text
Create file test-result.md using templates/artifacts/summary.md.
Use Origin Return Protocol.
Return Status, Artifact, Verification, Returned to.
```

A correct reply includes all five anchors and the final-answer shape.

## Read more

| Document | Purpose |
| --- | --- |
| [`agent-center/templates/artifacts/README.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/templates/artifacts/README.md) | Index of artifact templates. |
| [`agent-center/operations/origin-return-protocol/PROTOCOL.en.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/operations/origin-return-protocol/PROTOCOL.en.md) | Full Origin Return Protocol. |
| [`agent-center/skills/operations/origin-return-protocol/SKILL.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/skills/operations/origin-return-protocol/SKILL.md) | Skill wrapper. |
| [`scripts/check_orp.py`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/scripts/check_orp.py) | CI validator. |