#!/usr/bin/env python3
"""Airframe theme releases: read the version from theme/CHANGELOG.md and guard changes.

    python3 scripts/theme_release.py version            # prints the newest tag, e.g. theme-v2
    python3 scripts/theme_release.py notes [tag]        # prints that entry (release notes)
    python3 scripts/theme_release.py check --base REF   # CI: a theme change needs a new entry

The changelog's newest `## theme-vN` heading is the release. When a published theme file
(THEME_FILES: the Airframe outputs generated from airframe/, and airframe-docs.css) differs from
REF, `check` requires the changelog to gain a heading with a higher N than REF's newest, so
every token change is recorded and tagged once.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = "theme/CHANGELOG.md"
THEME_FILES = ("theme/airframe.css", "theme/airframe-docs.css", "theme/airframe-components.css",
               "theme/airframe-icons.svg", "theme/airframe-tokens.json", "theme/airframe-tailwind.css",
               "theme/airframe.tokens.json", "theme/airframe-day.tokens.json")
HEADING = re.compile(r"^## (theme-v(\d+))\b", re.MULTILINE)


def versions(text: str) -> list[tuple[str, int]]:
    return [(m[1], int(m[2])) for m in HEADING.finditer(text)]


def newest(text: str) -> tuple[str, int] | None:
    found = versions(text)
    if not found:
        return None
    nums = [n for _, n in found]
    if nums != sorted(nums, reverse=True) or len(set(nums)) != len(nums):
        raise ValueError(f"{CHANGELOG}: versions must be unique and newest first, got {nums}")
    return found[0]


def notes(text: str, tag: str) -> str:
    m = re.search(rf"^## {re.escape(tag)}\b.*$", text, re.MULTILINE)
    if not m:
        raise ValueError(f"{CHANGELOG}: no entry for {tag}")
    rest = text[m.end():]
    nxt = HEADING.search(rest)
    return rest[: nxt.start() if nxt else None].strip() + "\n"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def show(ref: str, path: str) -> str:
    try:
        return git("show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return ""


def check(base: str, head_text: str, base_text: str, changed: list[str]) -> list[str]:
    """Problems with a change from base to head; empty when it is fine."""
    problems = []
    try:
        head_v = newest(head_text)
    except ValueError as exc:
        return [str(exc)]
    theme_changed = [f for f in changed if f in THEME_FILES]
    if head_v is None:
        problems.append(f"{CHANGELOG} has no '## theme-vN' entry")
    if theme_changed:
        base_v = newest(base_text) if base_text else None
        if head_v and base_v and head_v[1] <= base_v[1]:
            problems.append(
                f"{', '.join(theme_changed)} changed since {base} but {CHANGELOG} still ends at "
                f"{base_v[0]}; add a '## theme-v{base_v[1] + 1}' entry listing each token change")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("version")
    n = sub.add_parser("notes")
    n.add_argument("tag", nargs="?")
    c = sub.add_parser("check")
    c.add_argument("--base", required=True, help="git ref to compare against, e.g. origin/main")
    args = ap.parse_args(argv)

    text = (ROOT / CHANGELOG).read_text()
    if args.cmd == "version":
        v = newest(text)
        if not v:
            print(f"{CHANGELOG}: no theme-vN entry", file=sys.stderr)
            return 1
        print(v[0])
        return 0
    if args.cmd == "notes":
        tag = args.tag or (newest(text) or ("", 0))[0]
        sys.stdout.write(notes(text, tag))
        return 0
    merge_base = git("merge-base", args.base, "HEAD").strip()
    changed = git("diff", "--name-only", merge_base, "--").split()
    problems = check(args.base, text, show(merge_base, CHANGELOG), changed)
    for p in problems:
        print(f"theme: {p}", file=sys.stderr)
    if not problems:
        print(f"theme: ok ({newest(text)[0]})")  # type: ignore[index]
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
