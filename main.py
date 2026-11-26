#!/usr/bin/env python3
"""Pitch the worst pizza topping ever invented.

Running this script drops a single joke line about a pizza topping
into the file the make.fun grader reads, /output/entry.txt. The joke
sells wet cardboard as the newest topping: the twist is that the
topping tastes exactly like the delivery box, because it *is* the
delivery box. Before writing anything the script measures the line
against the contest's limits, and after writing it reads the file
back to make sure nothing got mangled on the way to disk.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

LINE = (
    "New pizza topping: wet cardboard — it tastes exactly like the box "
    "it came in, because it is the box it came in."
)

FALLBACK_PATH = Path("/output/entry.txt")
MAX_CHARS = 200


def gate_ok(text: str) -> str | None:
    """Check `text` against the contest limits.

    Returns a short description of the first problem found, or None
    when the line is good to go.
    """
    stripped = text.strip()
    if not stripped:
        return "line is blank"
    if len(text.encode("utf-8")) > MAX_CHARS:
        return f"line is {len(text.encode('utf-8'))} bytes, over the {MAX_CHARS} limit"
    if "\n" in stripped or "\r" in stripped:
        return "line must fit on one line"
    return None


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the worst-pizza-topping pitch to entry.txt.")
    parser.add_argument("--output", metavar="PATH",
                        help="destination file (overrides $ENTRY_OUTPUT)")
    parser.add_argument("--print", action="store_true",
                        help="echo the pitch to stdout as well")
    return parser.parse_args()


def run() -> int:
    args = parse_cli()

    problem = gate_ok(LINE)
    if problem is not None:
        print(f"gate failed: {problem}", file=sys.stderr)
        return 1

    if args.print:
        print(LINE)

    target = Path(args.output) if args.output else Path(
        os.environ.get("ENTRY_OUTPUT", FALLBACK_PATH))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(LINE + "\n", encoding="utf-8")

    saved = target.read_text(encoding="utf-8")
    if saved != LINE + "\n":
        print("verification failed: file content differs from the pitch",
              file=sys.stderr)
        return 1
    problem = gate_ok(saved.strip())
    if problem is not None:
        print(f"verification failed: {problem}", file=sys.stderr)
        return 1

    print(f"done: {len(LINE)}-char pitch written to {target} and verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
