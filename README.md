# Readability Does Not Confer Control over Clinical Concepts

A linear probe reads a clinical concept from a vision-language model's visual representation at the block
its language model consumes. That readability promises a handle: write the direction back, change the
answer. We test the promise by writing every competing clinical direction at the same locus, dose and
patients, and asking whether the concept's own direction moves its own answer more than any other does.

Across 25 checkpoints from twelve families on NIH ChestX-ray14, CheXpert Plus and COCO — 75 blocks, 450
scored concept cells — clinical concepts are readable and answerable in most cells and **owned in 13%**.
The same procedure owns **75%** of natural-object cells, and the gap survives matching the two pools on
the model's own answer ability. A direction fitted to the model's own answers is a handle in the same
representation, nearly orthogonal to the probe direction.

Reading a concept is not writing it.

## This repository

| | |
|---|---|
| `main.tex`, `sections/` | the paper — the source of truth |
| `main_revised.tex` | the same document as one file, **generated** by `scripts/flatten.py` |
| `tables/`, `figures/` | generated from the campaign; `tables/cf_numbers.tex` holds every number the prose quotes |
| `data/plot/` | the numbers behind each figure and table, exported per artefact |
| `scripts/` | the generators, the consistency check, and the manifest and flatten tools |
| `MANIFEST.sha256` | checksums of everything the build reads — `sha256sum -c MANIFEST.sha256` |
| `REPRODUCE.md` | how to rebuild the PDF, the numbers and the figures |

No number is typed into the prose. Every one is a macro generated from the campaign manifest, and
`scripts/check_numbers.py` fails the build when the prose, the tables and the macros disagree.

## The campaign

The code that produced the results, and the slice of results that rebuilds this paper, is a separate
repository:

**https://github.com/hq0709/reading-is-not-writing-code**

Start from its `GUIDE.md`.

## Licence

The paper text and figures are under CC BY 4.0 (`LICENSE`). The style files vendored beside them are
redistributed under their own terms. CheXpert Plus is not redistributed here; see **Boundaries** in
`REPRODUCE.md`.
