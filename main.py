#!/usr/bin/env python3
"""The Worst Pizza Topping.

Writes one funny line pitching a terrible pizza topping to
/output/entry.txt (the path the make.fun program/v1 harness grades).

The line pitches wet cardboard as a pizza topping: it opens like a
new-product announcement, then the punchline turns the topping into
the box the pizza came in — the topping is literally the packaging,
which is why it tastes exactly like it.
"""

import argparse
import os
import sys

# The pitch, kept as one line of plain text.
PITCH = ("New pizza topping: wet cardboard — it tastes exactly like the "
         "box it came in, because it is the box it came in.")

DEFAULT_OUTPUT = "/output/entry.txt"


def build_pitch() -> str:
    """Return the single topping pitch line."""
    return PITCH


def parse_args(argv=None):
    """Command-line options for local runs and debugging."""
    parser = argparse.ArgumentParser(
        description="Write the worst-pizza-topping pitch to entry.txt.")
    parser.add_argument(
        "--output", default=None,
        help="where to write the pitch (default: $ENTRY_OUTPUT or "
             "/output/entry.txt)")
    parser.add_argument(
        "--print", action="store_true",
        help="also print the pitch to stdout instead of only writing it")
    return parser.parse_args(argv)


def check_pitch(pitch: str) -> list:
    """Return a list of gate problems; empty means the pitch is valid.

    Mirrors the competition gate: 1-200 UTF-8 characters, not only
    whitespace, a single line of plain text.
    """
    problems = []
    if not pitch.strip():
        problems.append("pitch is empty or only whitespace")
    if not (1 <= len(pitch.encode("utf-8")) <= 200):
        problems.append(
            f"pitch is {len(pitch.encode('utf-8'))} bytes, outside 1-200")
    if "\n" in pitch.strip():
        problems.append("pitch must be a single line")
    return problems


def main(argv=None) -> int:
    args = parse_args(argv)
    pitch = build_pitch()

    problems = check_pitch(pitch)
    if problems:
        for problem in problems:
            print(f"gate check failed: {problem}", file=sys.stderr)
        return 1

    if args.print:
        print(pitch)

    output = args.output or os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(pitch + "\n")

    # Read the file back and verify it holds exactly the pitch.
    with open(output, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != pitch + "\n":
        print("read-back check failed: file does not match the pitch",
              file=sys.stderr)
        return 1
    readback_problems = check_pitch(written.strip())
    if readback_problems:
        for problem in readback_problems:
            print(f"read-back gate check failed: {problem}", file=sys.stderr)
        return 1

    print(f"wrote {len(pitch.split())}-word pitch to {output} "
          f"({len(pitch)} chars, read-back verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
