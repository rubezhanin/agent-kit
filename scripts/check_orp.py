#!/usr/bin/env python3
"""Origin Return Protocol (ORP) validator.

Verifies that any Markdown file under ``agent-center/reports/`` follows the
Origin Return Protocol:

    * has a ``Status:`` line (``DONE`` | ``BLOCKED`` | ``NEEDS_APPROVAL`` | ``STALE``);
    * has an ``Artifact:`` line (path to the result);
    * has a ``Returned to:`` line.

It also verifies that the five anchors (``origin``, ``owner``, ``artifact``,
``status``, ``return_path``) appear in every task-card under
``agent-center/reports/task-receipts/``.

Used by ``.github/workflows/ci.yml`` and locally before tagging a release.

Usage:
    python scripts/check_orp.py [--strict] [--path ROOT]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATUS_VALUES = {"DONE", "BLOCKED", "NEEDS_APPROVAL", "STALE"}
REQUIRED_RECEIPT_HEADINGS = (
    "Status:",
    "Artifact:",
    "Returned to:",
    "Origin:",
    "Owner:",
)
REQUIRED_CARD_HEADINGS = (
    "Status:",
    "Artifact:",
    "Return path:",
    "Origin:",
    "Owner:",
)


def fail(rel: str, line: int | None, reason: str) -> str:
    where = f"{rel}:{line}" if line else rel
    return f"::error file={where}::ORP fail: {reason}"


def check_file(path: Path, headings: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    rel = str(path.relative_to(ROOT))
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Required headings
    line_index = {h.strip(":").lower(): None for h in headings}
    for i, line in enumerate(lines, start=1):
        normalized = line.strip().lower().rstrip(":") + ":"
        for h in headings:
            if normalized == h.strip().lower():
                line_index[h.strip(":").lower()] = i
    for h, idx in line_index.items():
        if idx is None:
            errors.append(fail(rel, None, f"missing heading: `{h}:`"))

    # Validate Status value
    if line_index.get("status") is not None:
        status_line = lines[line_index["status"] - 1]
        m = re.search(r"Status:\s*([A-Z_]+)", status_line)
        if m and m.group(1) not in STATUS_VALUES:
            errors.append(
                fail(
                    rel,
                    line_index["status"],
                    f"Status must be one of {sorted(STATUS_VALUES)}, got `{m.group(1)}`",
                )
            )

    return errors


def iter_receipts(root: Path):
    receipts_dir = root / "agent-center" / "reports" / "task-receipts"
    if not receipts_dir.exists():
        return
    for p in sorted(receipts_dir.glob("*.md")):
        yield p


def iter_cards(root: Path):
    """Task cards live next to the main operator in a Kanban board
    (which we don't ship), as well as the contract blueprint under
    ``agent-center/kanban/``. We only lint the actual card files,
    not the contract.
    """
    cards_dir = root / "agent-center" / "kanban"
    if not cards_dir.exists():
        return
    for p in sorted(cards_dir.rglob("*.md")):
        # Skip the contract and README; they are documentation, not cards.
        if p.name in {"board-contract.md", "README.md"}:
            continue
        # Skip anything that is not labelled like a card.
        if "-card" not in p.name and "task-" not in p.name and not p.name.endswith("-task.md"):
            continue
        yield p


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--path", default=str(ROOT), help="Repo root to scan")
    args = parser.parse_args()

    root = Path(args.path).resolve()

    errors: list[str] = []

    if not (root / "agent-center" / "reports").exists():
        # No reports yet (fresh repo) — nothing to validate.
        print("OK: no reports found yet (fresh repo)")
        return 0

    for receipt in iter_receipts(root):
        errors.extend(check_file(receipt, REQUIRED_RECEIPT_HEADINGS))

    for card in iter_cards(root):
        errors.extend(check_file(card, REQUIRED_CARD_HEADINGS))

    if errors:
        for e in errors:
            print(e, flush=True)
        print(f"\nFAILED: {len(errors)} ORP issues.", file=sys.stderr)
        return 1

    print("OK: Origin Return Protocol — all checked receipts / cards conform.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())