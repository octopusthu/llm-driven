#!/usr/bin/env python3
"""Collect open frictions from every vault under the given roots.

A vault is a directory holding AGENTS.md, index.md and log.md. Frictions live in
its revisions.md, one block per record. A record is closed by appending a line
with the same id, so the last line for an id wins.

Usage:
    revisions.py <root> [<root> ...]      print open records
    revisions.py --all <root> [...]       print every record, with its status
"""

import re
import sys
from pathlib import Path

HEADING = re.compile(r"^##\s+(R-\d+)\s*\|\s*([a-z-]+)\s*\|\s*(.*?)\s*$")
CASE = re.compile(r"^\s*-\s*Case:\s*(.+?)\s*$")
VAULT_FILES = ("AGENTS.md", "index.md", "log.md")


def is_vault(path):
    return all((path / name).is_file() for name in VAULT_FILES)


def read_records(revisions):
    """Return {id: (status, tail, case)} keeping the last state of each id."""
    records = {}
    current = None
    for line in revisions.read_text(encoding="utf-8").splitlines():
        heading = HEADING.match(line)
        if heading:
            rid, status, tail = heading.groups()
            records[rid] = [status, tail, records.get(rid, ["", "", ""])[2]]
            current = rid
            continue
        case = CASE.match(line)
        if case and current:
            records[current][2] = case.group(1)
    return records


def main(argv):
    show_all = "--all" in argv
    roots = [a for a in argv if not a.startswith("-")]
    if not roots:
        print(__doc__.strip())
        return 2

    found = []
    for root in roots:
        base = Path(root).expanduser()
        if not base.is_dir():
            print(f"not a directory: {base}")
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_dir() or ".git" in path.parts:
                continue
            if is_vault(path):
                found.append(path)

    if not found:
        print("no vault found under: " + ", ".join(roots))
        return 0

    total = 0
    for vault in found:
        revisions = vault / "revisions.md"
        if not revisions.is_file():
            continue
        records = read_records(revisions)
        rows = [(rid, *v) for rid, v in records.items() if show_all or v[0] == "open"]
        if not rows:
            continue
        print(f"\n{vault}")
        for rid, status, tail, case in sorted(rows):
            print(f"  {rid}  {status:<9} {tail}")
            if case:
                print(f"          case: {case}")
        total += len(rows)

    print(f"\n{total} record(s) across {len(found)} vault(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
