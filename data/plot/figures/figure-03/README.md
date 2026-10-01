# Figure 3 — positive write-flow

Current assets: [PDF](../../../../figures/fig7_write_flow.pdf) · [PNG](../../../../figures/fig7_write_flow.png).

`flow-marginals.json` copies `figures/figA1_own_share.json`: three datasets' total, diagonal, own-share, in-flow and out-flow. These marginals do **not** determine the 36 individual links in each dataset's 6×6 positive-flow matrix.

`positive-flow-full.csv` contains all 108 links of the three full-precision `Pm[q,d]` matrices, derived with the same mean-over-checkpoints rule from released per-block `summary.json`. Source: `scripts/plot_paper_figures.py::fig7_write_flow`.
