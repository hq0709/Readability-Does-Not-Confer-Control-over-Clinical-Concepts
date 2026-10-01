# Figure 2 — overview, landscape, dose, rank

Current assets: [PDF](../../../../figures/fig2_overview.pdf) · [PNG](../../../../figures/fig2_overview.png).

- Panel a: `panel-a-bars-full.csv` has all 9 exact integer counts and the plotted bootstrap confidence intervals. `panel-a-bars.csv` preserves the earlier count-only extraction.
- Panel b: `panel-b-points-full.csv` has all 75 full-precision Read/Own coordinates. `panel-b-points-displayed.csv` retains the paper's rounded values.
- Panel c: `panel-c-block-curves.json` contains the released per-block dose cache; `panel-c-plotted-summary.csv` contains the median and IQR actually plotted. `panel-c-block-counts.json` records cohort sizes.
- Panel d: `panel-d-ranks.csv` lists every plotted concept-cell rank; the ECDF is the cumulative fraction at ranks 1–120.

Source: `scripts/plot_paper_figures.py::fig2_overview`; full-precision inputs from the code repository's released `runs/` bundle. The numeric panels can be redrawn without raw outcome shards.
