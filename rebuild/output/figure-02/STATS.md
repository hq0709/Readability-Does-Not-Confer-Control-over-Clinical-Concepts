# Figure 2 — statistics & data traceability

Source data: `data/plot/figures/figure-02/`. Script: `rebuild/scripts/figure02.py`.

| Panel | What is plotted | n | Centre | Spread / interval | Source file |
|---|---|---|---|---|---|
| a | Number of concept cells passing each grade, per dataset | 150 cells per dataset and grade | count | none: every cell of the grid is counted, so the bar is the quantity rather than an estimate of one | `panel-a-bars-full.csv` |
| b | One marker per block (checkpoint × dataset): mean selectivity *S* over the block's concepts vs. mean ownership *O* over its concepts | 75 blocks (25 per dataset) | mean over concepts | none | `panel-b-points-full.csv` |
| c | Ownership *O* at each write dose α, across blocks | 25 blocks each for NIH and COCO (CheXpert has no dose sweep) | median over blocks | interquartile range (shaded) | `panel-c-plotted-summary.csv` |
| d | Empirical CDF of the rank of each concept's own write among 120 directions (own + 119 random); rank 1 = largest effect | 150 cells per dataset | — | — | `panel-d-ranks.csv` |

Definitions (from `sections/3_framework.tex`):
- *S* (readability) = probe AUROC − mean AUROC of 20 random-label control probes.
- *O* (ownership) = W<sub>q,q</sub> − max<sub>d≠q</sub> W<sub>q,d</sub>, in units of change in P(yes). A cell is owned when the write clears the random and sham reference and *O* > 0; the grade is read from these effects, not from an interval on them.
- α = write strength as a fraction of each token's own norm; the paper's main dose is α = +0.25 (dotted line in c).

Display notes:
- (c) y axis is clipped to [−0.2, 0.2] on request. All medians and the NIH band are inside; the COCO IQR band exceeds the top at α = +0.1 (q75 = 0.22), +0.25 (0.34) and +0.5 (0.56).
- (d) x axis is log-scaled. The marker at the start of each curve is its value at rank 1; the "ranked 1st" key lists these shares (COCO 71%, CheXpert 11%, NIH 3% — 107/150, 16/150, 5/150 cells), replacing the original three in-plot sentences.
- Suggested caption addition: "(c) median and interquartile range over 25 blocks; the dotted line marks α = +0.25, the dose at which every grade in the paper is scored; the COCO band is clipped at 0.2."
