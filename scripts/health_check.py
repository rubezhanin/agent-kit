#!/usr/bin/env python3
"""Kit health check.

Runs a set of structural checks on the kit:

1. Required files exist (manifest, README, LICENSE, AGENTS.md, ...).
2. Profile manifests parse and required fields are present.
3. ``.env`` is not tracked by git and ``.env.example`` is.
4. The installer dry-run path completes without errors.
5. There are no Cyrillic characters in the canonical English files.
6. Origin Return Protocol is wired (skill, references, system prompt).

Used by ``.github/workflows/ci.yml`` as a pre-release gate and locally by
maintainers with ``python scripts/health_check.py``.

Exit code ``0`` on success, ``1`` on any failure.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kit-manifest.json"


def ok(msg: str) -> None:
    print(f"OK   {msg}")


def fail(msg: str) -> None:
    print(f"FAIL {msg}")


def has_cyrillic(text: str) -> bool:
    return any("а" <= ch <= "я" or "А" <= ch <= "Я" or ch in "ёЁ" for ch in text)


def check_required_files() -> list[str]:
    required = [
        "README.md",
        "README.ru.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        ".env.example",
        ".gitignore",
        "kit-manifest.json",
        "mkdocs.yml",
        "agent-center/AGENTS.md",
        "agent-center/skills/operations/origin-return-protocol/SKILL.md",
        "agent-center/operations/origin-return-protocol/PROTOCOL.en.md",
        "agent-center/operations/origin-return-protocol/PROTOCOL.ru.md",
        "agent-center/templates/task-card.md",
        "agent-center/templates/receipt.md",
        "scripts/setup_kit.py",
        "scripts/check_orp.py",
        "scripts/check_release.py",
        "scripts/check_locale_sanity.py",
    ]
    errs: list[str] = []
    for rel in required:
        if not (ROOT / rel).exists():
            errs.append(f"missing artifact: {rel}")
    return errs


def check_profiles() -> list[str]:
    errs: list[str] = []
    profiles_dir = ROOT / "agent-center" / "profiles"
    if not profiles_dir.exists():
        errs.append(f"missing profiles dir: {profiles_dir}")
        return errs
    required_fields = {"name", "title", "type", "default_enabled", "description"}
    for p in sorted(profiles_dir.glob("*.profile.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            errs.append(f"{p.relative_to(ROOT)}: invalid JSON: {e}")
            continue
        missing = required_fields - set(data.keys())
        if missing:
            errs.append(f"{p.relative_to(ROOT)}: missing fields: {sorted(missing)}")
    return errs


def check_env_not_tracked() -> list[str]:
    errs: list[str] = []
    try:
        out = subprocess.run(
            ["git", "ls-files", ".env"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # No git on this host — skip; CI will catch this.
        return errs
    if out.returncode != 0:
        # Not a git repo or git errored — skip.
        return errs
    if out.stdout.strip():
        errs.append(f".env is tracked by git: {out.stdout.strip()}")
    out2 = subprocess.run(
        ["git", "ls-files", ".env.example"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if out2.returncode == 0 and not out2.stdout.strip():
        errs.append(".env.example is NOT tracked — it must be in the repo")
    return errs


def check_installer_dry_run() -> list[str]:
    proc = subprocess.run(
        [sys.executable, "scripts/setup_kit.py", "--dry-run", "--include-disabled"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"installer dry-run failed (rc={proc.returncode}): {proc.stderr.strip()[:400]}"]
    return []


def check_locale_sanity() -> list[str]:
    errs: list[str] = []
    canonical = [
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "LICENSE",
        ".env.example",
        "agent-center/AGENTS.md",
        "agent-center/skills/README.md",
        "agent-center/wiki/security-checklist.md",
        "agent-center/wiki/context-management.md",
        "agent-center/wiki/local-embedding.md",
        "agent-center/wiki/origin-return-protocol.md",
    ]
    for rel in canonical:
        p = ROOT / rel
        if not p.exists():
            continue
        if has_cyrillic(p.read_text(encoding="utf-8")):
            errs.append(f"{rel}: cyrillic character found in English file")
    # Files where Cyrillic is intentional (RU nav translations in mkdocs
    # i18n block, the locale-sanity script itself, etc.).
    if has_cyrillic((ROOT / "mkdocs.yml").read_text(encoding="utf-8")):
        # mkdocs.yml holds the i18n nav_translations block by design.
        pass
    return errs


def check_orp_wiring() -> list[str]:
    errs: list[str] = []

    # Skill is referenced from main-operator profile
    p = json.loads((ROOT / "agent-center" / "profiles" / "main-operator.profile.json").read_text(encoding="utf-8"))
    skills = p.get("skills", [])
    if "origin-return-protocol" not in skills:
        errs.append("main-operator profile does not list origin-return-protocol")

    # Reference text exists
    if not (ROOT / "agent-center" / "operations" / "origin-return-protocol" / "PROTOCOL.en.md").exists():
        errs.append("PROTOCOL.en.md missing")
    if not (ROOT / "agent-center" / "operations" / "origin-return-protocol" / "PROTOCOL.ru.md").exists():
        errs.append("PROTOCOL.ru.md missing")

    # System prompt references the protocol
    p = (ROOT / "agent-center" / "prompts" / "main-agent-system.md").read_text(encoding="utf-8")
    if "Origin Return Protocol" not in p:
        errs.append("main-agent-system.md does not mention Origin Return Protocol")

    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip",
        choices=["installer", "git", "locale", "orp", "profiles", "files"],
        action="append",
        default=[],
        help="Skip a specific check (repeatable)",
    )
    args = parser.parse_args()

    checks = [
        ("required files", lambda: check_required_files()),
        ("profiles parse", lambda: check_profiles()),
        (".env hygiene", lambda: check_env_not_tracked()),
        ("installer dry-run", lambda: check_installer_dry_run()),
        ("locale sanity", lambda: check_locale_sanity()),
        ("orp wiring", lambda: check_orp_wiring()),
    ]

    failures: list[str] = []
    for name, fn in checks:
        if name.startswith(tuple(args.skip)):
            print(f"--   skipping {name}")
            continue
        try:
            errs = fn()
        except Exception as e:
            errs = [f"{name}: exception: {e}"]
        if errs:
            for e in errs:
                fail(f"[{name}] {e}")
            failures.extend(f"[{name}] " + e for e in errs)
        else:
            ok(name)

    print()
    if failures:
        print(f"HEALTH CHECK FAILED ({len(failures)} issue(s))", file=sys.stderr)
        return 1
    print("HEALTH CHECK OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())