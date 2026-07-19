#!/usr/bin/env python3
"""Bump the version in pyproject.toml.

Usage:
    python scripts/bump_version.py [patch|minor|major]

Defaults to `patch` (0.2.0 -> 0.2.1). Prints the new version to stdout.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"
VERSION_RE = re.compile(r'^(version\s*=\s*)"(\d+)\.(\d+)\.(\d+)"', re.MULTILINE)


def bump(kind: str) -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    m = VERSION_RE.search(text)
    if not m:
        raise SystemExit('could not find version = "x.y.z" in pyproject.toml')
    prefix, major, minor, patch = m.group(1), *map(int, m.group(2, 3, 4))
    if kind == "major":
        major, minor, patch = major + 1, 0, 0
    elif kind == "minor":
        minor, patch = minor + 1, 0
    else:  # patch
        patch += 1
    new = f'{prefix}"{major}.{minor}.{patch}"'
    PYPROJECT.write_text(VERSION_RE.sub(new, text, count=1), encoding="utf-8")
    return f"{major}.{minor}.{patch}"


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "patch"
    if kind not in {"patch", "minor", "major"}:
        raise SystemExit(f"unknown bump kind: {kind}")
    print(bump(kind))
