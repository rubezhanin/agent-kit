# GitHub Install Guide

## Quick Start

```bash
git clone <YOUR_REPO_URL> hermes-agent-architecture-kit
cd hermes-agent-architecture-kit/kit
python scripts/setup_kit.py
```

Windows PowerShell:

```powershell
.\install.ps1
```

macOS/Linux:

```bash
sh ./install.sh
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
- does not assume Kanban/Curator availability.

