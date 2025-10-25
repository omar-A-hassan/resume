#!/usr/bin/env python3
"""Refresh the README's "Last updated" line with today's UTC date."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys


_LAST_UPDATED_PATTERN = re.compile(r"^last updated:\s*\d{4}-\d{2}-\d{2}\s*$", re.IGNORECASE)


def _current_utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _normalize_line(line: str, date_str: str) -> str:
    newline = "\n" if line.endswith("\n") else ""
    return f"Last updated: {date_str}{newline}"


def update_readme(path: Path, *, date_str: str) -> bool:
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines(keepends=True)

    updated_lines: list[str] = []
    replaced = False

    for line in lines:
        if _LAST_UPDATED_PATTERN.match(line.strip()):
            updated_lines.append(_normalize_line(line, date_str))
            replaced = True
        else:
            updated_lines.append(line)

    if not replaced:
        if updated_lines:
            if not updated_lines[-1].endswith("\n"):
                updated_lines[-1] += "\n"
        updated_lines.append(f"Last updated: {date_str}\n")

    new_content = "".join(updated_lines)

    if new_content != original:
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        default="README.md",
        help="Path to the README file to update.",
    )
    parser.add_argument(
        "--print-date",
        action="store_true",
        help="Print the date that was applied to stdout.",
    )

    args = parser.parse_args(argv)
    readme_path = Path(args.target)
    if not readme_path.exists():
        parser.error(f"README file not found: {readme_path}")

    date_str = _current_utc_date()
    update_readme(readme_path, date_str=date_str)

    if args.print_date:
        print(date_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())
