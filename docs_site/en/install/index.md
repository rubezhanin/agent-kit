# Install

> This page mirrors `docs/GITHUB_INSTALL.en.md`. The Russian version is [here](https://github.com/rubezhanin/agent-kit/blob/main/docs/install/index.md).

## Quick start

```bash
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent

# Linux / macOS:
sh ./install.sh

# Windows PowerShell:
.\install.ps1

# Cross-platform (recommended):
python scripts/setup_kit.py --dry-run
python scripts/setup_kit.py
```

## If Hermes Agent is not installed

The installer checks for `hermes` and `hermes-agent` and runs an install command only after explicit confirmation.

```bash
export HERMES_KIT_HERMES_INSTALL_COMMAND="<OFFICIAL_INSTALL_COMMAND>"
python scripts/setup_kit.py --install-hermes
```

…or pass the flag directly:

```bash
python scripts/setup_kit.py --install-hermes --hermes-install-command "<OFFICIAL_INSTALL_COMMAND>"
```

## Configuration via `.env`

```bash
cp .env.example .env
$EDITOR .env
```

The installer reads both `.env` and CLI flags. CLI flags take precedence.

| Variable | Purpose |
| --- | --- |
| `HERMES_KIT_WORKSPACE` | Target workspace path. |
| `HERMES_KIT_HERMES_HOME` | Hermes home directory. |
| `HERMES_KIT_MAIN_PROFILE` | Main profile name (default `main-operator`). |
| `HERMES_KIT_YES` | Auto-confirm safe defaults. |
| `HERMES_KIT_DRY_RUN` | Force dry-run mode. |
| `HERMES_KIT_HERMES_INSTALL_COMMAND` | Command to install Hermes if missing. |
| `HERMES_KIT_INSTALL_HERMES` | Allow running the install command non-interactively. |
| `HERMES_KIT_DEFAULT_PROFILES` | Comma-separated override of default profiles. |
| `HERMES_KIT_INCLUDE_DISABLED` | Offer disabled-by-default profiles. |
| `HERMES_KIT_SAFETY_LEVEL` | `strict`, `balanced`, or `permissive`. |
| `HERMES_KIT_LOCK_OUTSIDE_WORKSPACE` | Refuse to write outside the chosen workspace. |
| `HERMES_KIT_REFUSE_SHELL_FROM_ENV` | Defence-in-depth: refuse shell commands sourced from env. |

## What the installer does

- reads `kit-manifest.json`;
- discovers profiles from `agent-center/profiles/*.profile.json`;
- prepares or uses the `agent-center` workspace;
- records selected profiles in `.hermes-kit/selected-profiles.json`;
- writes an install receipt to `reports/task-receipts/`;
- leaves optional integrations disabled unless selected.

## What it does not do by default

- does not request secrets in chat;
- does not edit production config blindly;
- does not enable Telegram watcher;
- does not join Telegram channels;
- does not assume Kanban / Curator availability.

## Continue

| Guide | Purpose |
| --- | --- |
| [One-file installer](one-file.md) | Hand a clean Hermes agent the dialog flow. |
| [Adding profiles](adding-profiles.md) | Drop a JSON, get a new specialist. |
| [Architecture](../architecture/index.md) | End-to-end architecture. |
| [Changelog](../reference/changelog.md) | What changed between versions. |