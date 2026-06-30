# Agent × Skill Matrix (English)

> Canonical English version. Russian localization: [`docs/AGENT_SKILL_MATRIX.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/docs/AGENT_SKILL_MATRIX.ru.md).

This is where to look when you need to know which agents / profiles ship with which skills.

Primary sources:

- `agent-center/config/profiles.yaml` — profile map and roles.
- `agent-center/wiki/team-roster.md` — human-readable list of roles.
- `agent-center/skills/**/SKILL.md` — actual skill wrappers.

## Matrix

| Agent / profile | Status | Skills | Purpose |
| --- | --- | --- | --- |
| `main-operator` | active | `agent-creator`, `profile-factory`, `origin-return-protocol`, `wiki-memory`, `kanban-operator`, `gateway-ux`, `skill-hygiene-audit`, `hermes-token-drain-diagnostic`, `telegram-channel-intelligence` | Intake, routing, install, memory, Kanban, diagnostics, controlled Telegram intelligence, and the Origin Return Protocol anchors. |
| `profile-factory` | active operations | `profile-factory`, `agent-creator`, `origin-return-protocol` | Creates new profiles and skills from owner descriptions through intake, dry-run, approval and smoke tests; never invents `DONE` until the result reached `return_path`. |
| `researcher` | active | `researcher`, `telegram-channel-intelligence`, `origin-return-protocol` | Public-source research, weak signals, channel candidate discovery. Returns through the Origin Return summary. |
| `technical-engineer` | active | `technical-engineer`, `wiki-memory`, `hermes-token-drain-diagnostic`, `origin-return-protocol` | Setup, diagnostics, bounded local changes, smoke tests, receipts. |
| `business-analyst` | active | `business-analyst`, `researcher` (support), `origin-return-protocol` | Process map, automation audit, pilot design, implementation handoff. |
| `methodologist` | active | `methodologist`, `wiki-memory`, `origin-return-protocol` | Guides, courses, instructions, agent-ready documents. |
| `marketer` | active | `marketer`, `researcher`, `legal-ops` (review), `origin-return-protocol` | Audience, offers, proof bank, safe marketing experiments. |
| `designer` | active | `designer`, `marketer` (input), `origin-return-protocol` | Visual brief, style pack, prompt pack, visual OTK. |
| `legal-ops` | active risk-review | `legal-ops`, `origin-return-protocol` | Contracts, claims, privacy / data, vendor terms, contractual and AI-risk flags. |
| `economist` | active risk-review | `economist`, `origin-return-protocol` | ROI, pricing, subscriptions, paid pilot economics, budget review. |
| `agent-creator` | on-demand | `agent-creator`, `origin-return-protocol` | Designs new profiles, helper agents and skills through dry-run / change packet. |
| `psychological-support` | disabled by default | `psychological-support`, `origin-return-protocol` | Separate, guarded support profile, enabled only on explicit opt-in. |
| `userbot / watcher` | disabled by default | `telegram-channel-intelligence`, `origin-return-protocol` | Read-only Telegram channel watcher via TDLib / Telethon after separate approval. |
| `carousel-creator` | disabled by default | `carousel-creator`, `origin-return-protocol` | Brand intake → SMM brief → carousel workflow → visual design → GPT image prompts → OTK. Wraps the upstream `chatgpt-carousel-agent-kit` pack from `source/`. |

> Every active profile loads the `origin-return-protocol` skill so receipts and final answers are formed against the five anchors.

## Where to look in the filesystem

```text
kit/
  AGENT_SKILL_MATRIX.md
  agent-center/
    profiles/
    config/
      profiles.yaml
    wiki/
      team-roster.md
      security-checklist.md
      context-management.md
      local-embedding.md
    operations/
      origin-return-protocol/
        PROTOCOL.en.md
        PROTOCOL.ru.md
    skills/
      operations/
      specialists/
      optional/
```

## Rule for adding a new skill

1. Create `agent-center/skills/<group>/<skill-name>/SKILL.md`.
2. Add the skill to `agent-center/config/profiles.yaml`.
3. Add a row to `agent-center/wiki/team-roster.md` if the skill changes an agent's role.
4. Update this matrix.
5. Run a smoke / negative smoke test.

Profiles auto-discovered by the installer live here:

```text
agent-center/profiles/*.profile.json
```