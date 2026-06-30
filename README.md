# Hermes Agent Architecture Kit

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](CHANGELOG.md)
[![CI](https://github.com/your-org/hermes-agent-architecture-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/hermes-agent-architecture-kit/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-success)](https://your-org.github.io/hermes-agent-architecture-kit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![Hermes Kit](https://img.shields.io/badge/hermes--kit-0.3.0-indigo)](https://github.com/your-org/hermes-agent-architecture-kit)

A manifest-driven, opinionated starter kit for setting up a [Hermes Agent](https://github.com) workspace with profiles, skills, wiki, memory, optional Kanban, and a read-only Telegram channel intelligence layer.

It ships with a conservative installer that **discovers** profiles from `agent-center/profiles/*.profile.json`, **never** asks for secrets in chat, and **never** edits your existing Hermes runtime config without your explicit approval.

> [!IMPORTANT]
> This kit does **not** include the Hermes Agent runtime. Install Hermes separately (or pass `--hermes-install-command`), then point this kit at the workspace.

---

## Table of Contents

- [Why this kit?](#why-this-kit)
- [Quick start](#quick-start)
- [Repository layout](#repository-layout)
- [What gets installed](#what-gets-installed)
- [Profiles and skills](#profiles-and-skills)
- [Optional: Telegram channel intelligence](#optional-telegram-channel-intelligence)
- [Configuration](#configuration)
- [Localization](#localization)
- [Safety defaults](#safety-defaults)
- [Adding new profiles](#adding-new-profiles)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Why this kit?

Most Hermes setups start from scratch in chat: you assemble a prompt, write a few skills, glue them to a Kanban, and hope nothing collides. This kit provides a **boring, conservative default**:

- A pre-vetted team of agents (`main-operator`, `researcher`, `technical-engineer`, `business-analyst`, `methodologist`, `marketer`, `designer`, `legal-ops`, `economist`).
- A clear separation between *source of truth* (`wiki/`, `references/`, `owner-context/`) and *transient state* (`reports/`, Kanban).
- A manifest that the installer reads at runtime, so adding a profile is "drop a file" instead of "edit code".
- Hard safety rails: write-by-default is read-only, secrets never go in chat, integrations like Telegram watcher stay disabled until you flip them on.

## Quick start

### Linux / macOS

```bash
git clone <YOUR_REPO_URL> hermes-agent-architecture-kit
cd hermes-agent-architecture-kit
sh ./install.sh
```

### Windows (PowerShell)

```powershell
git clone <YOUR_REPO_URL> hermes-agent-architecture-kit
cd hermes-agent-architecture-kit
.\install.ps1
```

### Cross-platform (Python, the recommended entry point)

```bash
python scripts/setup_kit.py --dry-run   # inspect the plan
python scripts/setup_kit.py             # run it
```

Useful flags:

| Flag | Description |
| --- | --- |
| `--dry-run` | Print every action without writing anything. |
| `--yes` | Auto-accept safe defaults (still asks before external side effects). |
| `--workspace PATH` | Install into a custom workspace instead of in-place. |
| `--hermes-home PATH` | Tell the installer where Hermes lives (e.g. `~/.hermes`). |
| `--main-profile NAME` | Override the main profile (default `main-operator`). |
| `--install-hermes` | Allow running the configured Hermes install command. |
| `--hermes-install-command "..."` | Command used when Hermes CLI is missing. |
| `--include-disabled` | Also offer profiles disabled by default (e.g. Telegram watcher). |

See [`GITHUB_INSTALL.md`](GITHUB_INSTALL.md) for the full reference and [`docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md) for the guided dialog flow.

## Repository layout

```
hermes-agent-architecture-kit/
├── README.md                        # this file (English, primary)
├── README.ru.md                     # Russian localization
├── LICENSE                          # MIT
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .env.example                     # template for local configuration
├── .gitignore
├── GITHUB_INSTALL.md                # EN installer reference
├── docs/                            # localized long-form docs
│   ├── GITHUB_INSTALL.ru.md
│   ├── ONE_FILE_HERMES_KIT_INSTALLER.en.md
│   ├── ONE_FILE_HERMES_KIT_INSTALLER.ru.md
│   ├── ADDING_PROFILES.en.md
│   ├── ADDING_PROFILES.ru.md
│   ├── AGENT_SKILL_MATRIX.en.md
│   ├── AGENT_SKILL_MATRIX.ru.md
│   ├── ARCHITECTURE_REVIEW.en.md
│   ├── ARCHITECTURE_REVIEW.ru.md
│   ├── IMPLEMENTATION_PLAN.en.md
│   ├── IMPLEMENTATION_PLAN.ru.md
│   ├── SOURCE_SELECTION.en.md
│   └── SOURCE_SELECTION.ru.md
├── kit-manifest.json                # machine-readable manifest
├── install.ps1                      # Windows entry point
├── install.sh                       # POSIX entry point
├── scripts/
│   ├── setup_kit.py                 # canonical installer
│   └── create_profile_skeleton.py   # helper for new profiles
├── agent-center/                    # the workspace that gets installed
│   ├── AGENTS.md                    # main operator contract (EN)
│   ├── AGENTS.ru.md                 # Russian localization
│   ├── config/                      # profile/team blueprints
│   ├── profiles/                    # one JSON per profile
│   ├── skills/                      # operations / specialists / optional
│   ├── wiki/                        # canonical source of truth
│   ├── prompts/                     # system prompts
│   ├── templates/                   # receipt / task / smoke-test forms
│   ├── kanban/                      # Kanban contract
│   ├── owner-context/               # private owner notes
│   ├── references/                  # long-form sources
│   ├── reports/                     # receipts / audits / health
│   └── integrations/
│       └── telegram-channel-intelligence/
└── source/                          # original MD-packs (reference only)
```

## What gets installed

The installer:

1. Reads `kit-manifest.json`.
2. Auto-discovers profiles from `agent-center/profiles/*.profile.json` — adding a new profile is just dropping a file, no installer code change required.
3. Optionally prepares the `agent-center` workspace at a target path.
4. Records selected profiles in `.hermes-kit/selected-profiles.json`.
5. Writes a timestamped install receipt to `reports/task-receipts/`.
6. Leaves all optional integrations disabled unless you select them.

It does **not**:

- Request secrets, tokens, or session files in chat.
- Edit existing production Hermes config blindly.
- Enable the Telegram watcher without a separate approval.
- Assume Kanban / Curator commands exist before checking them.

## Profiles and skills

Default active profiles:

- `main-operator` — triage, routing, Kanban, quality gate, final user answer.
- `researcher` — public-source research, source ledger, Telegram channel candidate discovery.
- `technical-engineer` — setup, diagnostics, bounded local implementation.
- `business-analyst` — process map, automation audit, pilot design.
- `methodologist` — guides, courses, knowledge packaging.
- `marketer` — audience, offer, content strategy, safe experiments.
- `designer` — visual brief, prompt pack, visual QA.
- `legal-ops` — contract / claim / privacy / AI-vendor risk triage.
- `economist` — ROI, pricing, subscription and budget review.

Disabled by default (must be opted in explicitly):

- `psychological-support` — supportive, non-clinical conversation.
- `telegram-channel-watcher` — read-only watcher for approved channels.
- `carousel-creator` — optional wrap of the `chatgpt-carousel-agent-kit` pack for brand carousels / GPT image prompts. See `agent-center/integrations/carousel-creator/README.md`.

## The first layer — Origin Return Protocol

Every active profile loads the [`origin-return-protocol`](agent-center/skills/operations/origin-return-protocol/SKILL.md) skill so the operating loop keeps the five anchors (`origin` / `owner` / `artifact` / `status` / `return_path`) and never marks a task `DONE` until the result reaches `return_path`. Full text of the protocol is kept in `agent-center/operations/origin-return-protocol/PROTOCOL.en.md` (English) and `PROTOCOL.ru.md` (Russian original). See also the docs site under `Architecture → Origin Return Protocol`.

## Documentation site

A bilingual MkDocs Material site is built from `docs_site/`. Build locally with:

```bash
pip install -r requirements-docs.txt
mkdocs build      # → site/
mkdocs serve      # http://127.0.0.1:8000
```

The site is published to GitHub Pages by `.github/workflows/docs.yml` on every push to `main` and on tagged releases. Visit `https://<org>.github.io/hermes-agent-architecture-kit/` after the first deploy.

See [`docs/AGENT_SKILL_MATRIX.en.md`](docs/AGENT_SKILL_MATRIX.en.md) and `agent-center/skills/README.md` for the full skill matrix.

## Optional: Telegram channel intelligence

Disabled by default. To enable:

1. Decide what you want (researcher finds candidates → owner approves exact handles → dedicated watcher account monitors in read-only mode).
2. Fill the Telegram section of `.env` (`HERMES_TELEGRAM_*`).
3. Run the installer with `--include-disabled` and explicitly enable the `telegram-channel-watcher` profile.
4. Approve exact channel handles **before** any watcher joins anything.

See `agent-center/integrations/telegram-channel-intelligence/README.md` for the policy and `agent-center/config/watcher-policy.yaml` for the limits.

The kit does not promise "no ban". Telegram automation carries inherent risk; treat it as a dedicated, conservative watcher.

## Configuration

All knobs live in `.env`. Start from `.env.example`:

```bash
cp .env.example .env
$EDITOR .env
```

The installer reads both `.env` (if present) and explicit CLI flags. CLI flags take precedence. See `.env.example` for the full list of variables.

## Localization

- `README.md` — English (primary).
- `README.ru.md` — Russian.
- Long-form docs live in `docs/` with `.en.md` / `.ru.md` suffixes.
- Source-of-truth pages (`agent-center/AGENTS.md`, `wiki/`, `prompts/`) ship in English with `.ru.md` siblings where helpful.

If you spot a translation issue, please open a PR — the English version is canonical, the Russian version is provided for convenience.

## Safety defaults

- Default mode is **read-only**. Writes, external calls, account actions, payments, and deletions require explicit approval.
- Secrets are never requested in chat. They go in `.env` or in a local secret manager.
- The Telegram watcher never uses the owner's main account.
- The installer refuses to write outside the chosen workspace when `HERMES_KIT_LOCK_OUTSIDE_WORKSPACE=true`.
- `.gitignore` excludes `.env`, session files, raw Telegram caches, and all receipt/audit output by default.

## Adding new profiles

Drop two files into the kit:

```text
agent-center/profiles/<profile-name>.profile.json
agent-center/skills/<group>/<profile-name>/SKILL.md
```

The installer auto-discovers them on the next run. See [`docs/ADDING_PROFILES.en.md`](docs/ADDING_PROFILES.en.md) for the schema and an example.

## Documentation

| Topic | English | Russian |
| --- | --- | --- |
| End-to-end architecture | [`docs/ARCHITECTURE.en.md`](docs/ARCHITECTURE.en.md) | [`docs/ARCHITECTURE.ru.md`](docs/ARCHITECTURE.ru.md) |
| Install reference | [`GITHUB_INSTALL.md`](GITHUB_INSTALL.md) | [`docs/GITHUB_INSTALL.ru.md`](docs/GITHUB_INSTALL.ru.md) |
| One-file installer dialog | [`docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md) | [`docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md) |
| Adding profiles | [`docs/ADDING_PROFILES.en.md`](docs/ADDING_PROFILES.en.md) | [`docs/ADDING_PROFILES.ru.md`](docs/ADDING_PROFILES.ru.md) |
| Agent × skill matrix | [`docs/AGENT_SKILL_MATRIX.en.md`](docs/AGENT_SKILL_MATRIX.en.md) | [`docs/AGENT_SKILL_MATRIX.ru.md`](docs/AGENT_SKILL_MATRIX.ru.md) |
| Architecture review | [`docs/ARCHITECTURE_REVIEW.en.md`](docs/ARCHITECTURE_REVIEW.en.md) | [`docs/ARCHITECTURE_REVIEW.ru.md`](docs/ARCHITECTURE_REVIEW.ru.md) |
| Implementation plan | [`docs/IMPLEMENTATION_PLAN.en.md`](docs/IMPLEMENTATION_PLAN.en.md) | [`docs/IMPLEMENTATION_PLAN.ru.md`](docs/IMPLEMENTATION_PLAN.ru.md) |
| Source selection log | [`docs/SOURCE_SELECTION.en.md`](docs/SOURCE_SELECTION.en.md) | [`docs/SOURCE_SELECTION.ru.md`](docs/SOURCE_SELECTION.ru.md) |

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Keep PRs small, focus on one profile / skill / doc per change, and always run `python scripts/setup_kit.py --dry-run` before sending a PR.

## License

[MIT](LICENSE). See `LICENSE` for the full text.