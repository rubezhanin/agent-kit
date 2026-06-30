---
hide:
  - navigation
---

# Hermes Agent Architecture Kit

A manifest-driven, opinionated starter kit for setting up a [Hermes Agent](https://github.com) workspace with profiles, skills, wiki, memory, optional Kanban, and a read-only Telegram channel intelligence layer.

> [!IMPORTANT]
> This kit does **not** include the Hermes Agent runtime. Install Hermes separately (or pass `--hermes-install-command`), then point this kit at the workspace.

<div class="grid cards" markdown>

- :material-rocket-launch: __Quick start__
    Clone, run the installer, get a working Hermes main profile in under five minutes.
    [:octicons-arrow-right-24: Install now](install/index.md)

- :material-shield-lock: __Safety first__
    Read-only defaults, secrets stay in `.env`, Telegram watcher disabled out of the box.
    [:octicons-arrow-right-24: Security stance](architecture/index.md#safety)

- :material-source-branch: __Manifest-driven__
    Adding a profile is "drop a JSON file" — no code change.
    [:octicons-arrow-right-24: Architecture](architecture/index.md)

- :material-translate: __English + Russian__
    Canonical English; Russian localization next to every page.
    [:octicons-arrow-right-24: Русская версия](../ru/index.md)

</div>

## What you get

The installer boots a Hermes-aware workspace that contains:

- a `main-operator` profile that owns intake, routing, the final answer, and the quality gate;
- a vetted specialist team (`researcher`, `technical-engineer`, `business-analyst`, `methodologist`, `marketer`, `designer`, `legal-ops`, `economist`);
- an `agent-center/` workspace with `wiki/`, `references/`, `reports/`, `templates/`, `kanban/`, `prompts/`, `skills/`, `integrations/`;
- conservative optional integrations (Telegram channel intelligence, brand carousel generator) that stay disabled until you opt in;
- install receipts under `reports/task-receipts/`.

## Where to start

| You want to … | Read |
| --- | --- |
| Install from a fresh clone | [Install guide](install/index.md) |
| Hand a clean Hermes agent the dialog flow | [One-file installer](install/one-file.md) |
| Add a new profile | [Adding profiles](install/adding-profiles.md) |
| Understand the architecture | [Architecture](architecture/index.md) |
| See the *why* behind the kit | [Architecture review](architecture/architecture-review.md) |
| Audit a Telegram channel watcher | [Telegram channel intelligence](integrations/telegram-channel-intelligence.md) |
| Run a brand carousel workflow | [Carousel creator](integrations/carousel-creator.md) |
| See who owns what skill | [Agent × skill matrix](reference/skill-matrix.md) |
| See what got moved where from `source/` | [Source selection](reference/source-selection.md) |
| Upgrade from a previous version | [Changelog](reference/changelog.md) |