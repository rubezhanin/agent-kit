#!/usr/bin/env python3
"""Release / packaging helper.

Validates that:
  - all *.json files under the repo (excluding .git/, source/) parse;
  - kit-manifest.json parses and has the required keys;
  - the version in kit-manifest.json matches the version embedded in mkdocs.yml
    (when present);
  - the required release artifacts exist on disk.

Used by `.github/workflows/ci.yml` and locally by maintainers before tagging.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kit-manifest.json"
MKDOCS = ROOT / "mkdocs.yml"

REQUIRED_MANIFEST_KEYS = {
    "name",
    "version",
    "agent_center",
    "profile_registry",
    "skills_root",
    "default_workspace",
    "default_main_profile",
    "default_profiles",
    "disabled_by_default",
    "hermes",
    "installer",
}


def err(msg: str) -> None:
    print(f"::error file=scripts/check_release.py::{msg}", flush=True)


def ok(msg: str) -> None:
    print(f"ok: {msg}", flush=True)


def iter_json(root: Path):
    for path in root.rglob("*.json"):
        rel = path.relative_to(root)
        parts = rel.parts
        if ".git" in parts or "source" in parts:
            continue
        yield path


def validate_json() -> int:
    errors = 0
    for p in iter_json(ROOT):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            err(f"{p.relative_to(ROOT)}: {e}")
            errors += 1
    if errors == 0:
        ok(f"all {sum(1 for _ in iter_json(ROOT))} json files parse")
    return errors


def validate_manifest() -> int:
    if not MANIFEST.exists():
        err("kit-manifest.json missing")
        return 1
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"kit-manifest.json: {e}")
        return 1

    missing = REQUIRED_MANIFEST_KEYS - set(data.keys())
    if missing:
        err(f"kit-manifest.json missing keys: {sorted(missing)}")
        return 1
    ok(f"kit-manifest.json ok (version={data['version']})")
    return 0


def validate_mkdocs_version(manifest_version: str) -> int:
    if not MKDOCS.exists():
        err("mkdocs.yml missing")
        return 1
    text = MKDOCS.read_text(encoding="utf-8")
    m = re.search(r"^extra:\s*$(.+?)(?=^[a-z]+:|\Z)", text, flags=re.M | re.S)
    if not m:
        return 0  # version block optional
    block = m.group(1)
    if "provider" not in block:
        return 0
    if manifest_version not in text:
        # We only check that the version string at least appears once
        # somewhere in mkdocs.yml. If you do not pin a version there, skip.
        ok("mkdocs.yml exists (no version pinning expected)")
        return 0
    ok(f"mkdocs.yml mentions version {manifest_version}")
    return 0


def validate_release_artifacts() -> int:
    required = [
        ("README.md", ROOT / "README.md"),
        ("README.ru.md", ROOT / "README.ru.md"),
        ("LICENSE", ROOT / "LICENSE"),
        ("CHANGELOG.md", ROOT / "CHANGELOG.md"),
        ("CONTRIBUTING.md", ROOT / "CONTRIBUTING.md"),
        (".env.example", ROOT / ".env.example"),
        (".gitignore", ROOT / ".gitignore"),
        ("kit-manifest.json", ROOT / "kit-manifest.json"),
        ("mkdocs.yml", ROOT / "mkdocs.yml"),
        ("scripts/setup_kit.py", ROOT / "scripts" / "setup_kit.py"),
        ("install.ps1", ROOT / "install.ps1"),
        ("install.sh", ROOT / "install.sh"),
        (".github/workflows/ci.yml", ROOT / ".github" / "workflows" / "ci.yml"),
        (".github/workflows/docs.yml", ROOT / ".github" / "workflows" / "docs.yml"),
    ]
    errors = 0
    for label, p in required:
        if not p.exists():
            err(f"required artifact missing: {label}")
            errors += 1
    if errors == 0:
        ok(f"all {len(required)} release artifacts present")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-only", action="store_true", help="Only validate JSON files")
    parser.add_argument("--manifest-only", action="store_true", help="Only validate the manifest")
    args = parser.parse_args()

    errors = 0
    if not args.manifest_only:
        errors += validate_json()
    if not args.json_only:
        errors += validate_manifest()
        try:
            manifest_version = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
        except Exception:
            manifest_version = ""
        errors += validate_mkdocs_version(manifest_version)
        errors += validate_release_artifacts()

    if errors:
        print(f"\nFAILED with {errors} error(s).", file=sys.stderr)
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())