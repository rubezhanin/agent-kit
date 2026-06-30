---
name: Profile proposal
about: Propose a new specialist profile to ship with the kit
title: "[profile] "
labels: profile-proposal
assignees: ""
---

## Slug and role

- Slug (lowercase, kebab-case): `...`
- Title: `...`
- Type: `specialist | risk_review | optional_disabled | operations`

## What it does

<!-- 2–4 sentences: input, transformation, output. -->

## Trigger

<!-- When does this profile get invoked? What kind of user request triggers it? -->

## Output

<!-- What artifact does it return? Receipt? Source ledger? Risk register? -->

## Skills

<!-- Existing skills it depends on (group/name). New skills proposed? -->

## Safety gates

<!-- What does it never do? What always needs owner approval? -->

## Sources of truth

<!-- Which wiki pages, references, or owner-context files does it read? -->

## Opt-in or default?

<!-- Should the installer enable this profile by default, or only after explicit opt-in? -->

## Checklist

- [ ] I will provide `agent-center/profiles/<slug>.profile.json` in the PR
- [ ] I will provide `agent-center/skills/<group>/<slug>/SKILL.md` in the PR
- [ ] I will provide at least one smoke test under `agent-center/templates/`
- [ ] I will update `docs/AGENT_SKILL_MATRIX.en.md` and `docs/AGENT_SKILL_MATRIX.ru.md`
- [ ] I will update `CHANGELOG.md` under `[Unreleased]`