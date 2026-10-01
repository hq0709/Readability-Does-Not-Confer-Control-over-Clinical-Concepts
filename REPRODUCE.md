# Reproducing this paper

## The PDF

```bash
SOURCE_DATE_EPOCH=1788439147 FORCE_SOURCE_DATE=1 tectonic -X compile main.tex --keep-logs
```

Pinning the date makes the build byte-reproducible: without it the PDF carries a timestamp and two
correct builds differ. `latexmk -pdf main.tex` works too and is what the figures and tables were checked
against; it just does not give you the same bytes twice.

`main_revised.tex` is the same document as one file, for submission systems that want one. It is
**generated**, not maintained:

```bash
python scripts/flatten.py            # rewrite it from main.tex and sections/
python scripts/flatten.py --check    # non-zero if it is stale
```

It inlines the sections and the generated tables and keeps `\input{tables/cf_numbers}`, so the numbers it
quotes stay live rather than freezing at the moment it was flattened.

## The manifest

```bash
latexmk -pdf main.tex                # writes main.fls
python scripts/make_manifest.py      # MANIFEST.sha256 from the files the build read
sha256sum -c MANIFEST.sha256
```

The manifest is taken from `main.fls`, which records every file the build opened, plus the bibliography
and the style files that ship beside the paper. It is not typed by hand, because the previous one was and
it had drifted: twenty-one of its forty-four entries named files from a different paper, and it omitted
`preprint.sty`, which sets the layout, the float parameters and the title block.

## What the paper measures

| | |
|---|---|
| checkpoints | 25, across twelve families, 3B to 72B |
| datasets | NIH ChestX-ray14, CheXpert Plus, COCO as a natural-image control |
| blocks | 75 (checkpoint × dataset) |
| scored concept cells | 450 — 300 chest, 150 COCO |
| headline | clinical concepts owned in 13% of chest cells, 75% of COCO cells |

Every number in the prose is a macro from `tables/cf_numbers.tex`, and every macro is generated from the
campaign manifest. No number is typed into the text.

## Regenerating the numbers, tables and figures

The campaign code and the results it produced are a separate repository:

**https://github.com/hq0709/reading-is-not-writing-code**

It carries the runners, the protocol and the adapters, and under `runs/` the part of the campaign that
rebuilds this paper: the packaged per-block records, the robustness analyses, the figure caches, and the
per-sample rows the two qualitative figures read. Its `GUIDE.md` covers the whole chain; the short form is

```bash
export CF_RUNS=/path/to/code-repo/runs
bash /path/to/code-repo/scripts/mayo/refresh_numbers.sh
```

which repackages the blocks, re-analyses the stale ones, rebuilds the manifest, the robustness analyses,
the tables, the macros and the figures, compiles, and finishes with `check_numbers.py`. **That last step
is the gate: if it does not print `ALL CONSISTENT`, the PDF disagrees with itself somewhere.** It compares
the prose, the tables and the macros against the manifest — three paths to the same number.

Note what it does not prove. The three paths agreeing means they agree; it once agreed over a manifest
missing five blocks. When a count looks wrong, check the block count before trusting the check.

## Boundaries

**CheXpert Plus** travels under a use agreement. Every CheXpert grade this paper reports is in the code
repository; the cohort and label manifests and the images are not, and cannot be redistributed here.
Figure A2 is the one figure that reads them.

**The raw campaign** — per-sample outcome shards and activations, 75 GB — is in neither repository. It is
needed only to re-derive a grade from raw rows or to refit a probe from activations.

**Checkpoints** are public Hugging Face releases, each pinned to a commit in the code repository's
`docs/external-replication/protocol.json`. Nothing here mirrors them.
