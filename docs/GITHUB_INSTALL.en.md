# GitHub Install Guide

> English version (canonical). For the Russian translation, see [`docs/GITHUB_INSTALL.ru.md`](docs/GITHUB_INSTALL.ru.md).

## Quick Start

```bash
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent
sh ./install.sh        # POSIX
python scripts/setup_kit.py   # cross-platform
```

Windows PowerShell:

```powershell
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent
.\install.ps1
```

## If Hermes Agent Is Not Installed

The installer checks for:

```text
hermes
hermes-agent
```

Because different Hermes distributions may use different install methods, the kit does not hardcode a fake universal install command.

Use one of these:

```bash
python scripts/setup_kit.py --install-hermes --hermes-install-command "<OFFICIAL_INSTALL_COMMAND>"
```

or:

```bash
export HERMES_KIT_HERMES_INSTALL_COMMAND="<OFFICIAL_INSTALL_COMMAND>"
python scripts/setup_kit.py --install-hermes
```

PowerShell:

```powershell
$env:HERMES_KIT_HERMES_INSTALL_COMMAND="<OFFICIAL_INSTALL_COMMAND>"
.\install.ps1 -Yes
```

The script asks before running the command unless `--yes` / `-Yes` is used.

## Dry Run

```bash
python scripts/setup_kit.py --dry-run
```

PowerShell:

```powershell
.\install.ps1 -DryRun
```

## Install To Another Workspace

```bash
python scripts/setup_kit.py --workspace ~/AgentCenter
```

## With Known Hermes Home

```bash
python scripts/setup_kit.py --hermes-home ~/.hermes --main-profile main-operator
```

The installer writes a small `hermes-kit` package pointer under:

```text
<HERMES_HOME>/profiles/<main-profile>/hermes-kit/
```

It does not overwrite unknown Hermes runtime config.

## Configuration via `.env`

All non-flag knobs can be set in `.env` (template: `.env.example`). CLI flags override env values.

```bash
cp .env.example .env
$EDITOR .env
```

Useful variables:

| Variable | Purpose |
| --- | --- |
| `HERMES_KIT_WORKSPACE` | Target workspace path. |
| `HERMES_KIT_HERMES_HOME` | Hermes home directory. |
| `HERMES_KIT_MAIN_PROFILE` | Main profile name (default `main-operator`). |
| `HERMES_KIT_YES` | Auto-confirm safe defaults (`true` / `false`). |
| `HERMES_KIT_DRY_RUN` | Force dry-run mode (`true` / `false`). |
| `HERMES_KIT_HERMES_INSTALL_COMMAND` | Command to install Hermes if missing. |
| `HERMES_KIT_INSTALL_HERMES` | Allow running the install command non-interactively. |
| `HERMES_KIT_DEFAULT_PROFILES` | Comma-separated override of default profiles. |
| `HERMES_KIT_INCLUDE_DISABLED` | Offer disabled-by-default profiles. |
| `HERMES_KIT_SAFETY_LEVEL` | `strict`, `balanced`, or `permissive`. |
| `HERMES_KIT_LOCK_OUTSIDE_WORKSPACE` | Refuse to write outside the chosen workspace. |
| `HERMES_KIT_REFUSE_SHELL_FROM_ENV` | Defence-in-depth: refuse shell commands sourced from env. |

## What The Installer Does

- reads `kit-manifest.json`;
- discovers profiles from `agent-center/profiles/*.profile.json`;
- prepares/uses the `agent-center` workspace;
- records selected profiles in `.hermes-kit/selected-profiles.json`;
- writes an install receipt to `reports/task-receipts/`;
- leaves optional integrations disabled unless selected.

## What It Does Not Do By Default

- does not request secrets in chat;
- does not edit production config blindly;
- does not enable Telegram watcher;
- does not join Telegram channels;
- does not assume Kanban / Curator availability.