#!/usr/bin/env python3
"""Create a new profile manifest and SKILL.md skeleton for the kit."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9а-яё]+", "-", value, flags=re.I)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Create profile and skill skeleton.")
    parser.add_argument("name", help="Profile name or title.")
    parser.add_argument("--title", help="Human-readable title.")
    parser.add_argument("--description", default="TODO: describe this agent profile.")
    parser.add_argument("--type", default="specialist")
    parser.add_argument("--group", default="specialists", choices=["operations", "specialists", "optional"])
    parser.add_argument("--default-enabled", action="store_true")
    parser.add_argument("--kit-root", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    kit_root = Path(args.kit_root).resolve() if args.kit_root else script_path.parents[1]
    slug = slugify(args.name)
    title = args.title or args.name.strip()

    profile_path = kit_root / "agent-center" / "profiles" / f"{slug}.profile.json"
    skill_dir = kit_root / "agent-center" / "skills" / args.group / slug
    skill_path = skill_dir / "SKILL.md"

    if not args.force:
        for path in [profile_path, skill_path]:
            if path.exists():
                raise SystemExit(f"Refusing to overwrite existing file: {path}")

    profile = {
        "name": slug,
        "title": title,
        "type": args.type,
        "default_enabled": bool(args.default_enabled),
        "description": args.description,
        "skills": [slug],
        "approval_required_for": [],
        "forbidden_by_default": [],
        "outputs": [],
    }

    profile_path.parent.mkdir(parents=True, exist_ok=True)
    skill_dir.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    skill_path.write_text(
        "\n".join([
            "---",
            f"name: {slug}",
            f"description: {args.description}",
            "---",
            "",
            f"# {title}",
            "",
            "## When To Use",
            "",
            "Use this skill when the task matches this profile's purpose.",
            "",
            "## Workflow",
            "",
            "1. Clarify the task.",
            "2. Check sources of truth.",
            "3. Produce bounded output.",
            "4. Verify.",
            "5. Return a receipt.",
            "",
            "## Stop Rules",
            "",
            "Stop before secrets, accounts, production, destructive changes or external side effects.",
            "",
        ]),
        encoding="utf-8",
    )

    print(f"Created profile: {profile_path}")
    print(f"Created skill: {skill_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

