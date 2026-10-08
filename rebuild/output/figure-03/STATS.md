# Figure 3 — statistics & data traceability

Source data: `reading-is-not-writing/data/plot/figures/figure-03/positive-flow-full.csv` (108 links = 3 datasets × 6 questions × 6 written directions). Script: `rebuild/scripts/figure03.py`.

| Element | What is plotted | n | Source column |
|---|---|---|---|
| Band from write *d* to question *q* | width ∝ P<sub>q,d</sub> = mean over checkpoints of max(W<sub>q,d</sub>, 0) | 25 checkpoints per dataset | `value` (`question`, `written_direction`) |
| Left bar (write *d*) | Σ<sub>q</sub> P<sub>q,d</sub> (out-flow) | — | derived from `value` |
| Right bar (question *q*) | Σ<sub>d</sub> P<sub>q,d</sub> (in-flow) | — | derived from `value` |
| Own-question share | Σ<sub>d</sub> P<sub>d,d</sub> / Σ<sub>q,d</sub> P<sub>q,d</sub> | — | NIH 24%, CheXpert 22%, COCO 79% (matches `flow-marginals.json`) |

Change against the original: colours only (project concept palette in `rebuild/scripts/style.py`). Geometry, band order, labels and footnote are unchanged.
