# Figure 8 — statistics & data traceability

Source data: `reading-is-not-writing/data/plot/figures/figure-08/median-write-matrices-full.csv` (108 cells = 3 datasets × 6 × 6). Script: `rebuild/scripts/figure08.py`.

| Panel | Dataset | Checkpoints | max \|median W\| |
|---|---|---|---|
| a | NIH ChestX-ray14 | 25 | 0.05 (Card. diagonal) |
| b | CheXpert Plus | 25 | 0.04 (Effus. diagonal) |
| c | COCO | 25 | 0.45 (chair diagonal) |

- Cell value: cell-wise median over the dataset's completed checkpoints of W<sub>q,d</sub> (mean change in P(yes) of question *q* under the write of direction *d*, α = +0.25).
- Colour scale ±0.5 (max 0.45 rounded up, as in the original); terracotta = positive, dusty blue = negative (`style.DIVERGING`). Note: Figures 5 and 6 use ±0.9, so colours are not comparable across figures; the colour bar states the range.
- Every cell is annotated (short form: .36 = +0.36, −.01 = −0.01; |v| < 0.005 shown as 0), since the chest medians all lie within ±0.05.
- Caption unchanged except "The diagonal is outlined" does not appear in this figure's caption, so no update is needed.
