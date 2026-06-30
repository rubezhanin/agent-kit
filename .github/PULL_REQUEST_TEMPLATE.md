---
name: Pull request
about: Open a PR against hermes-agent
title: ""
labels: ""
assignees: ""
---

## What

<!-- One paragraph summary. -->

## Why

<!-- The user problem or capability gap this PR closes. -->

## How

<!-- The minimum context a reviewer needs to validate the change. -->

## Risk and safety

- Touches installer logic: yes / no
- Touches safety policy or stop rules: yes / no
- Requires `.env` changes: yes / no
- Affects optional integrations (Telegram watcher / Kanban / Curator): yes / no

## Validation

- [ ] `python scripts/setup_kit.py --dry-run` runs clean
- [ ] I updated `CHANGELOG.md` under `[Unreleased]`
- [ ] I updated both `.en.md` and `.ru.md` siblings where applicable
- [ ] I did not commit `.env`, session files, or secrets

## Linked issues

<!-- Closes #... / Related to #... -->