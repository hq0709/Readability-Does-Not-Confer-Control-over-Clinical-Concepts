"""Generate the single-file source from main.tex, so it cannot drift from the sections it came from.

A flat file is what submission systems want. Maintained by hand beside the modular source it becomes a
second truth: the prose updates in one place and the tables in the other, and nothing says which the PDF
was built from. Generated, it is an artefact -- rebuilt by the refresh chain like a table or a figure.

What it inlines and what it does not follows the file it replaces. Sections and the generated
table_cf_*.tex are pasted in. math_commands, cf_colors and cf_numbers stay as \\input, which is the point:
cf_numbers carries every number the prose quotes, so a flat file that still reads it keeps its numbers
live instead of freezing them at the moment it was flattened.

    python scripts/flatten.py                 # writes main_revised.tex
    python scripts/flatten.py --check         # exits non-zero if the file on disk is stale
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEEP = ("math_commands", "tables/cf_colors", "tables/cf_numbers")
INPUT = re.compile(r"\\input\{([^}]+)\}")


def expand(text: str, depth: int = 0) -> str:
    if depth > 8:
        raise RuntimeError("input nesting deeper than eight; a file probably includes itself")

    def sub(m: re.Match) -> str:
        name = m.group(1)
        if name in KEEP:
            return m.group(0)
        p = ROOT / (name if name.endswith(".tex") else name + ".tex")
        if not p.exists():
            return m.group(0)
        return expand(p.read_text(), depth + 1)

    return INPUT.sub(sub, text)


ap = argparse.ArgumentParser()
ap.add_argument("--out", default="main_revised.tex")
ap.add_argument("--check", action="store_true", help="compare against the file on disk instead of writing")
a = ap.parse_args()

flat = expand((ROOT / "main.tex").read_text())
out = ROOT / a.out

if a.check:
    if not out.exists():
        print(f"{a.out} does not exist", file=sys.stderr)
        raise SystemExit(1)
    if out.read_text() != flat:
        print(f"{a.out} is stale: regenerate it with python scripts/flatten.py", file=sys.stderr)
        raise SystemExit(1)
    print(f"{a.out} matches main.tex and its sections")
else:
    out.write_text(flat)
    print(f"{a.out}: {len(flat)} characters from main.tex and its sections")
