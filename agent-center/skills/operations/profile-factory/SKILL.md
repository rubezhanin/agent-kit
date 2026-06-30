---
name: profile-factory
description: Use when the owner describes a new agent/profile they want. Creates a profile manifest, skill skeleton, routing rules, safety policy and smoke tests through guided questions, dry-run, approval and receipt.
---

# Profile Factory

Use this skill when the user says:

- "create an agent for ...";
- "add a profile ...";
- "I need an agent with skills ...";
- "make a specialist / helper-agent from this description";
- "add a role to the kit".

## Core Rule

Do not create a live profile from a vague idea.

Work in this sequence:

```text
description -> intake -> role card -> skill map -> safety policy -> dry-run change packet -> approval -> files -> smoke tests -> receipt
```

## Intake

Ask only what is needed:

1. What repeated work should this agent reduce?
2. What should it produce?
3. What sources may it trust?
4. What tools does it need?
5. What must it never do?
6. What actions require approval?
7. Should it be active by default or optional?
8. What harmless smoke test proves it works?

## Output Files

For a new profile named `<slug>`:

```text
agent-center/profiles/<slug>.profile.json
agent-center/skills/<group>/<slug>/SKILL.md
agent-center/templates/profile-factory/<slug>-smoke-test.md
```

Update if needed:

```text
AGENT_SKILL_MATRIX.md
agent-center/skills/README.md
agent-center/wiki/team-roster.md
```

## Profile Manifest Contract

Use JSON, not YAML, for machine-readable profile auto-discovery:

```json
{
  "name": "profile-slug",
  "title": "Human Title",
  "type": "specialist",
  "default_enabled": false,
  "description": "What this profile does.",
  "skills": ["profile-slug"],
  "approval_required_for": [],
  "forbidden_by_default": [],
  "outputs": []
}
```

## Safety Defaults

If unsure:

- `default_enabled: false`;
- no external side effects;
- read-only first;
- no account access;
- no production;
- no secrets in chat;
- owner approval before enabling.

## Stop Rules

Stop and ask for clarification if:

- no repeated use case exists;
- sources of truth are unknown;
- forbidden actions are not named;
- the profile would need money/account/production access;
- no smoke test can be defined.

