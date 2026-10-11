# Candidate figures — QA notes

Produced with the nature-figure skill. Nothing in `figures/` was changed; every candidate is written
to `rebuild/candidates/output/`, and the originals under `rebuild/scripts/` are untouched.

## Contract

```
Core conclusion:      A direction that reads a clinical concept does not write it: the concept's own
                      write moves its own answer less than a competing write does, while the same
                      procedure on natural objects writes cleanly.
Results question:     Does readability confer control?
Archetype:            quantitative grid (Fig. 2, 4, 6) / asymmetric hero (Fig. 2 candidates B, D, E)
Target:               ACL Rolling Review, two columns, A4
Backend:              Python (matplotlib) -- saved preference, and the existing figure code is Python
Final size:           spanning float 455.24 pt = 6.323 in; column 219.09 pt = 3.043 in
Statistics:           n = 450 scored cells (150 per dataset, 25 checkpoints x 6 concepts);
                      centre = median over checkpoints; no interval is drawn, because the grade is a
                      count over the whole grid rather than an estimate of one
Source data:          rebuild/candidates/data/cells.csv and grades.csv, written by export_cells.py
                      through cf_inclusion -- the same block-inclusion rule every table uses
```

## The size invariant was broken

`figstyle.py` authors every figure at 5.5 in and records the invariant that it is included at
`\textwidth` so nothing is rescaled. The ACL text width is 6.323 in, so each figure was being
enlarged by 1.1496 and every 7 pt label printed at 8.0 pt. Each candidate is authored at the real
width: for the scripts that place panels in absolute inches, `make_resized.py` scales every inch
constant by that same factor, so the composition is unchanged and the type returns to its intended
size.

## Data integrity

- All 450 cells are used. No cell is dropped, downsampled or filtered.
- The grade counts reproduce the paper exactly: readable 135/121/118, answerable 143/114/121,
  owned 16/28/117. Readable is counted over every probe-graded block and the other two over included
  blocks, as `cf_inclusion` specifies, so the three grades do not share a denominator.
- `fig4-C` first used x-limits of (-0.33, 0.78), which clipped a point in 18 of the 450 cells off the
  strip. The limits now hold the full data range.
- `fig2-C` drops the nine per-bar counts: at 1.4 in per panel they collide, and they are in Table 1.
  That is the only candidate that shows less than its siblings.

## Gates

| Gate | Result |
|---|---|
| `validate_figure.py` source preflight | PASS on all seven candidate scripts |
| `audit_pdf_text.py`, 5 pt glyph floor | PASS on all sixteen; minimum 5.25 pt |
| `audit_panel_alignment.py`, 1.5 pt | ALIGNED on all sixteen |
| `audit_figure_collisions.py` | see the exemptions below |
| `rebuild/scripts/qa.py` (the project's own) | PASS on all sixteen |

A real glyph-floor violation was found and fixed: the ladder legend reads `largest $O_q$ at the
largest size`, and a mathtext subscript sets at 0.7 of its base, so a 7 pt legend put that `q` at
4.9 pt. The legend is 7.5 pt in the candidates, which puts it at 5.25 pt.

## Collision findings: what was fixed and what is exempt

**Fixed.** `fig5-A` has 65 text-stroke findings because the ceiling hatch runs under the cell values;
the render confirms it, with lines through `.75`, `.76`, `.61` and `.48`. `fig5-B` outlines each
value in the opposite of its own colour -- white behind a dark value, ink behind a white one, since
a white halo around white text turns `.75` into a blob -- which drops the count to 13 and leaves the
digits legible over the hatching.

**Exempt, verified by eye at 400-600 dpi.** The remaining findings are axis-aligned bounding-box
artifacts, not overlaps:

| Finding | Why it is not a collision |
|---|---|
| `text-text` between neighbouring 45-degree tick labels | A rotated label's axis-aligned box is much larger than its glyphs. `Mass`/`Nodule` report 100% box overlap; at 600 dpi the glyphs are clearly apart. The project's own `qa.py` skips parallel rotated labels for this reason. |
| `text-stroke` on a label beside a heat map | The hatch and cell-edge paths have boxes spanning the whole axes, so a row label outside the axes is reported as crossed by them. |
| `text-stroke` on `0.75` in `fig3-A` | The crossing path is the shaded row's border, whose box spans the row. The value sits inside the band. |
| `text-stroke` on `share above the line` in `fig2-D` | The crossing path is the identity diagonal, whose box is the whole panel. The text is in the empty upper-left. |

## Alignment exemptions, with reasons

| Candidate | Check | Reason |
|---|---|---|
| `fig4-B-paired` | horizontal-gutter | The gap between the two checkpoint pairs is deliberately wider than the gap inside a pair, so the contrast reads as two pairs rather than four panels. |
| `fig6-A`, `fig6-B` | panel-width | Panel (c) carries two model sizes against three in (a) and (b); at equal width its points sit on both edges with an empty middle and it reads as the narrowest. The original gives it about ten per cent more. |
| `fig2-E-units` | column | The unit grid is drawn with equal aspect so its 450 squares stay square, so its axes box is set by the aspect ratio and cannot share an edge with a free panel. |

## Evidence-architecture findings behind the new designs

1. **Figures 4, 7 and A1 are three encodings of `W_{q,d}`.** Figure 7 draws the mean over checkpoints
   of `max(W,0)` as flow; Figure A1 draws the cell-wise median as a heat map; A1's caption says
   Figure 7 reads the same matrices. `fig7A1-M` merges them; keeping one is the alternative.
2. **The 2x3 matrix grid pairs different checkpoints in the same column.** The export has both
   datasets for `q25-7` and `lingshu-32` only, so the middle column puts Qwen2.5-VL-72B (chest) above
   Qwen3-VL-32B (COCO). `fig4-B` and `fig4-C` make the comparison exact.
3. **Figure 2 is a 2x2 of equal panels** whose first panel carries the result. `fig2-B`, `fig2-D` and
   `fig2-E` give it the hero position.
4. **Figure 6's three panels run to 0.6, 0.2 and 0.3**, so a line that looks steep in (b) is a sixth
   of the rise it would be in (a). `fig6-B` puts them on one scale.

## What was chosen and installed

| Paper figure | Candidate | Placement |
|---|---|---|
| Figure 2 | `fig2-E-units` — the 450 cells as a unit grid, the margin as a raincloud, the dose curve | main text |
| Figure 3 | `fig3-A-example` — unchanged design, re-authored at the real width | main text |
| Figure 4 (was 6) | `fig6-D-portrait-shared` — portrait panels, key in its own slot, one y scale | appendix |
| Figure 5 | `figA3-rank` — the rank curve that was Figure 2(d), now a single-column figure | appendix |
| Figure 6 (was 5) | `fig5-B-halo` — values outlined so they read over the ceiling hatch | appendix |
| Figure 7 (was 4) | `fig4-A-six` — unchanged design, re-authored at the real width | appendix |
| Figure 8 (was 7 + A1) | `fig7A1-M-merged` — the flow and the median matrix in one figure | appendix |

`figA1_write_structure.pdf` is gone: its content is panels (d)--(f) of the merged figure, which carries
both `\label{fig:write-flow}` and `\label{fig:cf-w-structure}` so every existing reference resolves.

Section 5 cited the rank curve as Figure 2(d). Candidate E has no fourth panel, so the curve moved to
the appendix rather than being dropped, and the citation points there.
