#!/usr/bin/env python3
"""Locale sanity check.

Verifies that English-facing files (under ``docs_site/en/``, the canonical
English doc tree, and the English GitHub-rooted Markdown) do not contain
Cyrillic characters that have leaked in from Russian-only sources.

The Russian localization lives under ``docs_site/ru/`` and the Russian
language pairs (``*.ru.md``) — those are intentionally allowed to contain
Cyrillic.

Usage:
    python scripts/check_locale_sanity.py [--strict]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files / directories where Cyrillic is expected.
RUSSIAN_OK = {
    "README.ru.md",
    "AGENTS.ru.md",
    "README.ru.md",
}

# Whitelist of files that should *not* contain Cyrillic (English canonical).
# Paths are relative to ROOT.
ENGLISH_CANONICAL_PATHS = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    ".env.example",
    "agent-center/AGENTS.md",
    "agent-center/skills/README.md",
    "agent-center/wiki/architecture.md",
    "agent-center/wiki/operating-contract.md",
    "agent-center/wiki/memory-policy.md",
    "agent-center/wiki/team-roster.md",
    "agent-center/wiki/security-checklist.md",
    "agent-center/wiki/context-management.md",
    "agent-center/wiki/local-embedding.md",
    "agent-center/templates/smoke-tests.md",
    "agent-center/prompts/main-agent-system.md",
    "agent-center/prompts/delegation.md",
    "agent-center/prompts/final-report.md",
    "agent-center/config/gateway-telegram.yaml",
    "agent-center/config/profiles.yaml",
    "agent-center/config/cron-jobs.yaml",
    "agent-center/config/hermes-target-profile.yaml",
    "agent-center/integrations/telegram-channel-intelligence/README.md",
    "agent-center/integrations/carousel-creator/README.md",
]

# Files that intentionally contain Cyrillic by design (and are validated by
# separate process: the Russian localisation must stay in sync).
EXEMPT_FROM_LOCALE_CHECK = {
    # Files where Cyrillic is required (RU localisation pairs, the locale-sanity
    # script itself, and tooling that holds RU nav translations inline).
    "scripts/check_locale_sanity.py",
    # mkdocs.yml holds nav translations for the RU locale; the EN site itself
    # does not embed Cyrillic, only the language toggle and the translator
    # titles. We exempt the entire file rather than try to line-by-line skip.
    "mkdocs.yml",
}

# Lines under these files that mention RU are allowed (e.g. cross-links in
# the English home page that read "Russian version").
EXEMPT_LINE_FRAGMENTS = (
    "Русская версия",
    "Русский",
    "Russian version",
    "Главная",
    "Установка",
    "Архитектура",
    "Справочник",
    "Интеграции",
    "История версий",
    "nav_translations",
    "name: Русский",
    "default: true",  # mkdocs i18n default language flag
)


def has_cyrillic(text: str) -> bool:
    return any("а" <= ch <= "я" or "А" <= ch <= "Я" or ch in "ёЁ" for ch in text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    errors: list[tuple[str, int, str]] = []

    def check_file(rel: str) -> None:
        if rel in EXEMPT_FROM_LOCALE_CHECK:
            return
        path = ROOT / rel
        if not path.exists():
            return
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not has_cyrillic(line):
                continue
            if any(frag in line for frag in EXEMPT_LINE_FRAGMENTS):
                continue
            errors.append((rel, lineno, line.strip()[:120]))

    # 1) Strict check: ENGLISH_CANONICAL_PATHS must not contain Cyrillic.
    for rel in ENGLISH_CANONICAL_PATHS:
        check_file(rel)

    # 2) Heuristic check: scan every *.md under docs_site/en/ for Cyrillic.
    en_dir = ROOT / "docs_site" / "en"
    if en_dir.exists():
        for p in en_dir.rglob("*.md"):
            check_file(str(p.relative_to(ROOT)))

    if errors:
        for rel, lineno, line in errors:
            print(f"::error file={rel}:{lineno}::cyrillic in EN file: {line}", flush=True)
        print(f"\nFAILED: {len(errors)} cyrillic occurrences in English files.", file=sys.stderr)
        return 1

    print("Locale sanity: no cyrillic in English canonical files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())