"""Write MANIFEST.sha256 from the files the build actually read.

A manifest typed by hand drifts from the paper beside it, and silently: the one this replaces listed
iclr2027_conference.sty, fig1_framework.pdf and B_answer_encoding.tex, none of which are in this
repository, so twenty-one of its forty-four entries pointed at nothing and `sha256sum -c` failed on every
one of them. It also omitted preprint.sty, which sets the layout, the float parameters and the title block.

latexmk records every file it opened in main.fls. Taking the manifest from there means it lists what the
build consumed rather than what someone remembered, and a file that stops being read drops out by itself.

    latexmk -pdf main.tex && python scripts/make_manifest.py
    sha256sum -c MANIFEST.sha256
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLS = ROOT / "main.fls"
# read by the build but written by it, or not source: these are products, not inputs
SKIP_SUFFIX = (".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".pdf.gz", ".bbl", ".blg", ".toc")
# refs.bib is read by bibtex, which does not write to main.fls; the .sty files vendored beside the paper
# are listed whether or not this build happened to read them, since they are part of what is shipped
EXTRA = ("LICENSE", "REPRODUCE.md", "README.md", "main_revised.tex", "refs.bib",
         "fancyhdr.sty", "natbib.sty", "preprint.sty")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


if not FLS.exists():
    sys.exit("main.fls not found: build the paper once with latexmk -pdf main.tex first")

seen: set[Path] = set()
for line in FLS.read_text().splitlines():
    if not line.startswith("INPUT "):
        continue
    p = Path(line[6:].strip())
    p = p if p.is_absolute() else ROOT / p
    try:
        rel = p.resolve().relative_to(ROOT)          # only files inside the repository
    except ValueError:
        continue                                      # the TeX distribution's own files
    if rel.suffix in SKIP_SUFFIX or not p.exists():
        continue
    seen.add(rel)

for name in EXTRA:                                    # shipped, not read by the build
    if (ROOT / name).exists():
        seen.add(Path(name))

lines = [f"{sha(ROOT / rel)}  {rel}" for rel in sorted(seen, key=str)]
(ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(f"MANIFEST.sha256: {len(lines)} files")
