#!/usr/bin/env python3
"""Manifest-driven installer for Hermes Agent Architecture Kit.

This script is intentionally conservative:
- it discovers Hermes but does not assume a package manager;
- it runs a Hermes install command only if supplied by the user/env/manifest;
- it installs the kit workspace and writes receipts;
- it auto-discovers profiles from agent-center/profiles/*.profile.json;
- it supports non-interactive (default), fully interactive (``--interactive``)
  and dry-run (``--dry-run``) modes;
- on failure it produces actionable hints instead of an opaque traceback.
"""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Errors with friendly hints
# ---------------------------------------------------------------------------


class KitError(RuntimeError):
    """User-facing error with a remediation hint."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message)
        self.hint = hint

    def format(self) -> str:
        if self.hint:
            return f"{self.args[0]}\n  hint: {self.hint}"
        return str(self.args[0])


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise KitError(
            f"file not found: {path}",
            hint="run the installer from the kit root, or check that the repo was cloned completely.",
        ) from e
    except json.JSONDecodeError as e:
        raise KitError(
            f"invalid JSON in {path}: {e}",
            hint="fix the JSON syntax (a trailing comma is a common cause) and re-run.",
        ) from e


def safe_print(*args, **kwargs) -> None:
    print(*args, **kwargs, flush=True)


def ask(question: str, default: bool = False, yes: bool = False) -> bool:
    if yes:
        return True
    suffix = " [Y/n] " if default else " [y/N] "
    try:
        ans = input(question + suffix).strip().lower()
    except EOFError as e:
        raise KitError("interactive prompt failed: stdin closed", hint="pass --yes for non-interactive mode") from e
    if not ans:
        return default
    return ans in {"y", "yes", "д", "да"}


def ask_text(question: str, default: str | None = None, allow_empty: bool = False) -> str:
    suffix = f" [{default}] " if default else ""
    while True:
        try:
            ans = input(question + suffix).strip()
        except EOFError as e:
            raise KitError("interactive prompt failed: stdin closed") from e
        if not ans and default is not None:
            return default
        if not ans and not allow_empty:
            continue
        return ans


def ask_secret(question: str, env_name: str | None = None) -> str:
    """Prompt for a secret value with masking.

    Falls back to the env variable if non-interactive input is unavailable.
    """
    try:
        return getpass.getpass(question + " ").strip()
    except (EOFError, KeyboardInterrupt):
        if env_name and os.environ.get(env_name):
            return os.environ[env_name].strip()
        raise KitError(
            f"could not read secret: {question}",
            hint=f"set the matching env var ({env_name}) and re-run, or pass --yes plus the env.",
        )


def run(cmd: str, dry_run: bool) -> int:
    safe_print(f"RUN: {cmd}")
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
    safe_print(f"COPY: {src} -> {dst}")
    if dry_run:
        return
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
    except PermissionError as e:
        raise KitError(
            f"cannot copy {src} -> {dst}: permission denied",
            hint="check that the destination is writable. On POSIX, sudo / chmod. On Windows, run as admin or pick another folder.",
        ) from e
    except OSError as e:
        raise KitError(
            f"copy failed: {e}",
            hint="verify the destination path exists, the source path is not empty, and disk space is sufficient.",
        ) from e


def discover_profiles(profile_dir: Path) -> list[dict]:
    if not profile_dir.exists():
        raise KitError(
            f"profile directory missing: {profile_dir}",
            hint="clone the repo again or check that agent-center/profiles/*.profile.json files exist.",
        )
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
    interactive: bool = False,
) -> list[dict]:
    selected = []
    defaults_set = set(defaults)
    safe_print(f"Discovered {len(profiles)} profile(s).")

    if interactive and not yes:
        safe_print("\nAvailable profiles:")
        for i, p in enumerate(profiles, start=1):
            tag = "default" if p.get("default_enabled") else (
                "DISABLED" if p.get("disabled_by_default") else "opt-in"
            )
            safe_print(f"  {i:>2}. {p.get('name'):<28} [{tag}]  {p.get('title')}")
        safe_print("\nEnter the numbers of profiles to enable, comma-separated.")
        safe_print("Press Enter to accept the defaults.")
        raw = ask_text("Profiles []", default="")
        if raw.strip():
            choices = {n.strip() for n in raw.split(",") if n.strip()}
            for i, p in enumerate(profiles, start=1):
                if str(i) in choices:
                    selected.append(p)
            return selected

    for profile in profiles:
        name = profile.get("name")
        default_enabled = bool(profile.get("default_enabled", name in defaults_set))
        disabled = bool(profile.get("disabled_by_default", False))
        if disabled and not include_disabled:
            safe_print(f"SKIP default-disabled profile: {name}")
            continue
        if dry_run:
            if default_enabled:
                selected.append(profile)
            else:
                safe_print(f"DRY-RUN SKIP non-default profile: {name}")
            continue
        if yes or ask(f"Enable profile '{name}'?", default=default_enabled, yes=False):
            selected.append(profile)
    return selected


def write_receipt(path: Path, receipt: dict, dry_run: bool) -> None:
    safe_print(f"RECEIPT: {path}")
    if dry_run:
        safe_print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise KitError(
            f"cannot create receipt directory {path.parent}: {e}",
            hint="check write permissions on the workspace.",
        ) from e
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Interactive flow
# ---------------------------------------------------------------------------


def interactive_flow(manifest: dict, agent_center: Path) -> dict:
    """Drives a small interactive session and returns the resolved config.

    Returns dict with keys:
      workspace, main_profile, hermes_home, install_hermes, hermes_install_cmd,
      selected_profiles, language.
    """
    safe_print("\n=== Hermes Kit installer (interactive) ===\n")

    language = ask_text(
        "Output language [en/ru]",
        default=manifest.get("default_language", "en"),
    ).strip().lower() or "en"
    if language not in {"en", "ru"}:
        safe_print(f"  unknown language `{language}`, falling back to `en`")
        language = "en"

    safe_print("\n[1/5] Workspace")
    default_workspace = str(agent_center.resolve())
    workspace = ask_text(
        "Workspace path (Enter for in-place agent-center)",
        default=default_workspace,
    )
    workspace = Path(workspace).expanduser().resolve()

    safe_print("\n[2/5] Main profile")
    main_profile = ask_text(
        "Main profile name",
        default=manifest.get("default_main_profile", "main-operator"),
    )

    safe_print("\n[3/5] Hermes home (optional, press Enter to skip)")
    hermes_home_raw = ask_text("HERMES_HOME directory (leave empty to skip)", default="")
    hermes_home = Path(hermes_home_raw).expanduser().resolve() if hermes_home_raw else None

    safe_print("\n[4/5] Install Hermes if missing? (y/N)")
    install_hermes = ask("Allow installer to run a Hermes install command?", default=False, yes=False)
    hermes_install_cmd = ""
    if install_hermes:
        hermes_install_cmd = ask_text(
            "Hermes install command (leave empty to use env HERMES_KIT_HERMES_INSTALL_COMMAND)",
            default=os.environ.get("HERMES_KIT_HERMES_INSTALL_COMMAND", ""),
        )

    safe_print("\n[5/5] Profiles")
    profile_dir = ROOT / manifest["profile_registry"]
    profiles = discover_profiles(profile_dir)
    selected = select_profiles(
        profiles,
        manifest.get("default_profiles", []),
        yes=False,
        include_disabled=False,
        dry_run=False,
        interactive=True,
    )
    if not selected:
        safe_print("No profiles selected — kit will install only the workspace skeleton.")

    safe_print("\n--- Dry-run preview ---")
    safe_print(json.dumps(
        {
            "language": language,
            "workspace": str(workspace),
            "main_profile": main_profile,
            "hermes_home": str(hermes_home) if hermes_home else None,
            "install_hermes": install_hermes,
            "hermes_install_command": hermes_install_cmd or "(none)",
            "selected_profiles": [p.get("name") for p in selected],
        },
        ensure_ascii=False,
        indent=2,
    ))
    safe_print("---")
    if not ask("Apply these choices and write files? [y/N]", default=False, yes=False):
        raise KitError("aborted by user", hint="re-run with different choices or pass --yes to accept the preview blindly.")

    return {
        "language": language,
        "workspace": workspace,
        "main_profile": main_profile,
        "hermes_home": hermes_home,
        "install_hermes": install_hermes,
        "hermes_install_cmd": hermes_install_cmd,
        "selected_profiles": selected,
    }


# ---------------------------------------------------------------------------
# Secret prompts (.env helper)
# ---------------------------------------------------------------------------


def prompt_env_secrets(env_path: Path) -> dict:
    """Prompt for the main optional secrets with masking. Returns a dict.

    Never overwrites an existing ``.env``; merge instead.
    """
    safe_print("\nOptional: populate secrets for the kit. Press Enter to skip any value.")
    env_path.parent.mkdir(parents=True, exist_ok=True)
    existing: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            existing[k.strip()] = v.strip()

    new_values: dict[str, str] = dict(existing)
    fields = [
        ("HERMES_TELEGRAM_PHONE", "Telegram watcher phone (E.164, e.g. +10000000000)", False),
        ("HERMES_TELEGRAM_API_ID", "Telegram API ID (digits)", False),
        ("HERMES_TELEGRAM_API_HASH", "Telegram API hash (string)", True),
        ("HERMES_TELEGRAM_BOT_TOKEN", "Telegram Bot API token (optional)", True),
    ]
    for key, prompt, is_secret in fields:
        existing_value = existing.get(key, "")
        suffix = f" [current: {'set' if existing_value else 'empty'}] " if existing_value else " "
        if is_secret:
            value = ask_secret(prompt + suffix, env_name=key)
        else:
            value = ask_text(prompt + suffix, default=existing_value)
        if value:
            new_values[key] = value

    lines = []
    for k, v in new_values.items():
        if v == "":
            continue
        lines.append(f"{k}={v}")
    try:
        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as e:
        raise KitError(
            f"cannot write .env at {env_path}: {e}",
            hint="check write permissions on the workspace, or pick a different path with --workspace.",
        ) from e
    safe_print(f"Wrote {len(new_values)} value(s) to .env")
    return new_values


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Hermes Agent Architecture Kit.")
    parser.add_argument("--yes", action="store_true", help="Non-interactive yes for safe default actions.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    parser.add_argument("--interactive", action="store_true", help="Drive an interactive install flow.")
    parser.add_argument("--populate-env", action="store_true", help="After install, prompt for optional secrets (Telegram, etc.) into .env.")
    parser.add_argument("--workspace", help="Target workspace. Defaults to kit/agent-center in place.")
    parser.add_argument("--hermes-home", help="Hermes home directory, if known.")
    parser.add_argument("--main-profile", default=None, help="Main Hermes profile name.")
    parser.add_argument("--hermes-install-command", help="Command to install Hermes Agent if not found.")
    parser.add_argument("--install-hermes", action="store_true", help="Allow Hermes install command if Hermes is missing.")
    parser.add_argument("--include-disabled", action="store_true", help="Allow selection of disabled-by-default profiles.")
    parser.add_argument("--language", default=None, help="Output language: en or ru.")
    args = parser.parse_args()

    try:
        return _run(args)
    except KitError as e:
        safe_print(f"\nERROR: {e.format()}", file=sys.stderr)
        return 1


def _run(args: argparse.Namespace) -> int:
    manifest_path = ROOT / "kit-manifest.json"
    if not manifest_path.exists():
        raise KitError(f"manifest not found: {manifest_path}", hint="run the installer from the kit root directory.")
    manifest = load_json(manifest_path)
    agent_center = ROOT / manifest["agent_center"]
    profile_dir = ROOT / manifest["profile_registry"]

    interactive = bool(args.interactive) and not args.yes

    if interactive:
        chosen = interactive_flow(manifest, agent_center)
        workspace = chosen["workspace"]
        hermes_home = chosen["hermes_home"]
        main_profile = chosen["main_profile"]
        install_hermes = chosen["install_hermes"]
        hermes_install_cmd = chosen["hermes_install_cmd"] or (
            args.hermes_install_command
            or os.environ.get("HERMES_KIT_HERMES_INSTALL_COMMAND")
            or manifest["hermes"].get("install_command")
        )
        profiles = chosen["selected_profiles"]
        args.dry_run = False
        args.yes = False
    else:
        if not agent_center.exists():
            raise KitError(
                f"agent-center not found: {agent_center}",
                hint="verify the repo was cloned completely; the kit cannot install without an agent-center tree.",
            )

        hermes_command = which_any(manifest["hermes"]["candidate_commands"])
        install_command = (
            args.hermes_install_command
            or os.environ.get("HERMES_KIT_HERMES_INSTALL_COMMAND")
            or manifest["hermes"].get("install_command")
        )

        if hermes_command:
            safe_print(f"Hermes command found: {hermes_command}")
        else:
            safe_print("Hermes command not found.")
            if install_command and (args.install_hermes or ask("Run configured Hermes install command?", default=False, yes=args.yes)):
                code = run(install_command, args.dry_run)
                if code != 0:
                    raise KitError(
                        f"Hermes install command failed (exit {code})",
                        hint="run the install command manually, then re-run this installer.",
                    )
                hermes_command = which_any(manifest["hermes"]["candidate_commands"])
            else:
                safe_print("No Hermes install command was run. Provide --hermes-install-command or HERMES_KIT_HERMES_INSTALL_COMMAND.")

        try:
            workspace = Path(args.workspace).expanduser().resolve() if args.workspace else agent_center.resolve()
        except OSError as e:
            raise KitError(
                f"cannot resolve workspace path: {e}",
                hint="use --workspace PATH to pick a different workspace.",
            ) from e
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
        profiles = selected
        install_hermes = args.install_hermes
        hermes_install_cmd = install_command

    safe_print(f"\nWorkspace: {workspace}")
    safe_print(f"Main profile: {main_profile}")
    safe_print(f"Profiles to enable: {[p.get('name') for p in profiles]}")

    if workspace != agent_center.resolve():
        copy_tree(agent_center, workspace, args.dry_run)
    else:
        safe_print(f"Using in-place workspace: {workspace}")

    install_state_dir = workspace / ".hermes-kit"
    selected_path = install_state_dir / "selected-profiles.json"
    receipt_dir = workspace / "reports" / "task-receipts"
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    receipt_path = receipt_dir / f"hermes-kit-install-{timestamp}.json"

    selected_payload = {
        "main_profile": main_profile,
        "profiles": profiles,
    }
    if not args.dry_run:
        install_state_dir.mkdir(parents=True, exist_ok=True)
        try:
            selected_path.write_text(
                json.dumps(selected_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as e:
            raise KitError(
                f"cannot write {selected_path}: {e}",
                hint="check write permissions on the workspace, or pick a different path.",
            ) from e
    else:
        safe_print(f"WOULD WRITE: {selected_path}")

    if hermes_home:
        try:
            profile_pkg_dir = hermes_home / "profiles" / main_profile / "hermes-kit"
            safe_print(f"Hermes profile package target: {profile_pkg_dir}")
            if not args.dry_run:
                profile_pkg_dir.mkdir(parents=True, exist_ok=True)
                (profile_pkg_dir / "workspace.txt").write_text(str(workspace) + "\n", encoding="utf-8")
                (profile_pkg_dir / "selected-profiles.json").write_text(
                    json.dumps(selected_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
        except OSError as e:
            raise KitError(
                f"cannot write to {hermes_home / 'profiles' / main_profile / 'hermes-kit'}: {e}",
                hint="verify write permissions on HERMES_HOME. The kit never overwrites existing profiles.",
            ) from e

    receipt = {
        "kit": manifest["name"],
        "version": manifest["version"],
        "timestamp": timestamp,
        "kit_root": str(ROOT),
        "workspace": str(workspace),
        "hermes_command": which_any(manifest["hermes"]["candidate_commands"]),
        "hermes_home": str(hermes_home) if hermes_home else None,
        "main_profile": main_profile,
        "selected_profiles": [p.get("name") for p in profiles],
        "profile_count": len(profiles),
        "dry_run": args.dry_run,
        "interactive": interactive,
        "next_steps": [
            "Open ONE_FILE_HERMES_KIT_INSTALLER.md in a clean Hermes agent for guided setup.",
            "Run smoke tests from agent-center/templates/smoke-tests.md.",
            "If you enabled Telegram watcher, approve exact channel handles BEFORE the watcher joins anything.",
            "Read agent-center/operations/origin-return-protocol/PROTOCOL.en.md — every receipt follows this protocol.",
        ],
    }
    write_receipt(receipt_path, receipt, args.dry_run)

    if args.populate_env and not args.dry_run:
        try:
            prompt_env_secrets(workspace / ".env")
        except KitError:
            raise

    safe_print("\nDone.")
    safe_print(f"Workspace: {workspace}")
    safe_print(f"Selected profiles: {', '.join(receipt['selected_profiles'])}")
    safe_print(f"Receipt: {receipt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())