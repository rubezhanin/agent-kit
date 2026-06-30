#!/usr/bin/env python3
"""Manifest-driven installer for Hermes Agent Architecture Kit.

This script is intentionally conservative:
- it discovers Hermes but does not assume a package manager;
- it runs a Hermes install command only if supplied by the user/env/manifest;
- it installs the kit workspace and writes receipts;
- it auto-discovers profiles from agent-center/profiles/*.profile.json.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ask(question: str, default: bool = False, yes: bool = False) -> bool:
    if yes:
        return True
    suffix = " [Y/n] " if default else " [y/N] "
    ans = input(question + suffix).strip().lower()
    if not ans:
        return default
    return ans in {"y", "yes", "д", "да"}


def run(cmd: str, dry_run: bool) -> int:
    print(f"RUN: {cmd}")
    if dry_run:
        return 0
    return subprocess.call(cmd, shell=True)


def which_any(commands: list[str]) -> str | None:
    for command in commands:
        found = shutil.which(command)
        if found:
            return found
    return None


def copy_tree(src: Path, dst: Path, dry_run: bool) -> None:
    print(f"COPY: {src} -> {dst}")
    if dry_run:
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)


def discover_profiles(profile_dir: Path) -> list[dict]:
    profiles = []
    for path in sorted(profile_dir.glob("*.profile.json")):
        data = load_json(path)
        data["_source_file"] = str(path)
        profiles.append(data)
    return profiles


def select_profiles(
    profiles: list[dict],
    defaults: list[str],
    yes: bool,
    include_disabled: bool,
    dry_run: bool = False,
) -> list[dict]:
    selected = []
    defaults_set = set(defaults)
    for profile in profiles:
        name = profile.get("name")
        default_enabled = bool(profile.get("default_enabled", name in defaults_set))
        disabled = bool(profile.get("disabled_by_default", False))
        if disabled and not include_disabled:
            print(f"SKIP default-disabled profile: {name}")
            continue
        # In dry-run mode we never block on interactive prompts; we honour
        # the profile's `default_enabled` flag instead. This makes the installer
        # usable in CI / previews without `--yes`.
        if dry_run:
            if default_enabled:
                selected.append(profile)
            else:
                print(f"DRY-RUN SKIP non-default profile: {name}")
            continue
        if yes or ask(f"Enable profile '{name}'?", default=default_enabled, yes=False):
            selected.append(profile)
    return selected


def write_receipt(path: Path, receipt: dict, dry_run: bool) -> None:
    print(f"RECEIPT: {path}")
    if dry_run:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Hermes Agent Architecture Kit.")
    parser.add_argument("--yes", action="store_true", help="Non-interactive yes for safe default actions.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    parser.add_argument("--workspace", help="Target workspace. Defaults to kit/agent-center in place.")
    parser.add_argument("--hermes-home", help="Hermes home directory, if known.")
    parser.add_argument("--main-profile", default=None, help="Main Hermes profile name.")
    parser.add_argument("--hermes-install-command", help="Command to install Hermes Agent if not found.")
    parser.add_argument("--install-hermes", action="store_true", help="Allow Hermes install command if Hermes is missing.")
    parser.add_argument("--include-disabled", action="store_true", help="Allow selection of disabled-by-default profiles.")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    kit_root = script_path.parents[1]
    manifest_path = kit_root / "kit-manifest.json"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    manifest = load_json(manifest_path)
    agent_center = kit_root / manifest["agent_center"]
    profile_dir = kit_root / manifest["profile_registry"]
    if not agent_center.exists():
        print(f"ERROR: agent-center not found: {agent_center}", file=sys.stderr)
        return 2

    hermes_command = which_any(manifest["hermes"]["candidate_commands"])
    install_command = (
        args.hermes_install_command
        or os.environ.get("HERMES_KIT_HERMES_INSTALL_COMMAND")
        or manifest["hermes"].get("install_command")
    )

    if hermes_command:
        print(f"Hermes command found: {hermes_command}")
    else:
        print("Hermes command not found.")
        if install_command and (args.install_hermes or ask("Run configured Hermes install command?", default=False, yes=args.yes)):
            code = run(install_command, args.dry_run)
            if code != 0:
                print("ERROR: Hermes install command failed.", file=sys.stderr)
                return code
            hermes_command = which_any(manifest["hermes"]["candidate_commands"])
        else:
            print("No Hermes install command was run. Provide --hermes-install-command or HERMES_KIT_HERMES_INSTALL_COMMAND.")

    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else agent_center.resolve()
    hermes_home = Path(args.hermes_home).expanduser().resolve() if args.hermes_home else None
    main_profile = args.main_profile or manifest.get("default_main_profile", "main-operator")

    profiles = discover_profiles(profile_dir)
    selected = select_profiles(
        profiles,
        manifest.get("default_profiles", []),
        yes=args.yes,
        include_disabled=args.include_disabled,
        dry_run=args.dry_run,
    )

    if workspace != agent_center.resolve():
        copy_tree(agent_center, workspace, args.dry_run)
    else:
        print(f"Using in-place workspace: {workspace}")

    install_state_dir = workspace / ".hermes-kit"
    selected_path = install_state_dir / "selected-profiles.json"
    receipt_dir = workspace / "reports" / "task-receipts"
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    receipt_path = receipt_dir / f"hermes-kit-install-{timestamp}.json"

    selected_payload = {
        "main_profile": main_profile,
        "profiles": selected,
    }
    if not args.dry_run:
        install_state_dir.mkdir(parents=True, exist_ok=True)
        selected_path.write_text(json.dumps(selected_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(f"WOULD WRITE: {selected_path}")

    if hermes_home:
        profile_pkg_dir = hermes_home / "profiles" / main_profile / "hermes-kit"
        print(f"Hermes profile package target: {profile_pkg_dir}")
        if not args.dry_run:
            profile_pkg_dir.mkdir(parents=True, exist_ok=True)
            (profile_pkg_dir / "workspace.txt").write_text(str(workspace) + "\n", encoding="utf-8")
            (profile_pkg_dir / "selected-profiles.json").write_text(
                json.dumps(selected_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    receipt = {
        "kit": manifest["name"],
        "version": manifest["version"],
        "timestamp": timestamp,
        "kit_root": str(kit_root),
        "workspace": str(workspace),
        "hermes_command": hermes_command,
        "hermes_home": str(hermes_home) if hermes_home else None,
        "main_profile": main_profile,
        "selected_profiles": [p.get("name") for p in selected],
        "profile_count": len(selected),
        "dry_run": args.dry_run,
        "next_steps": [
            "Open ONE_FILE_HERMES_KIT_INSTALLER.md in a clean Hermes agent for guided setup.",
            "Run smoke tests from agent-center/templates/smoke-tests.md.",
            "Enable Telegram watcher only after separate approval."
        ],
    }
    write_receipt(receipt_path, receipt, args.dry_run)

    print("\nDone.")
    print(f"Workspace: {workspace}")
    print(f"Selected profiles: {', '.join(receipt['selected_profiles'])}")
    print(f"Receipt: {receipt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
