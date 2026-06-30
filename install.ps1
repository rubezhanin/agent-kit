param(
  [switch]$Yes,
  [switch]$DryRun,
  [string]$HermesHome,
  [string]$Workspace,
  [string]$HermesInstallCommand
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Setup = Join-Path $ScriptDir "scripts\setup_kit.py"

$ArgsList = @()
if ($Yes) { $ArgsList += "--yes" }
if ($DryRun) { $ArgsList += "--dry-run" }
if ($HermesHome) { $ArgsList += @("--hermes-home", $HermesHome) }
if ($Workspace) { $ArgsList += @("--workspace", $Workspace) }
if ($HermesInstallCommand) { $ArgsList += @("--hermes-install-command", $HermesInstallCommand) }

python $Setup @ArgsList

