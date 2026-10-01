# Figure 6 — same-write reader heatmaps

Current assets: [PDF](../../../../figures/fig5_same_write.pdf) · [PNG](../../../../figures/fig5_same_write.png).

`ownership-displayed.csv` contains all 90 plotted cells (five readers × three datasets × six concepts), extracted from the three tables in `tables/table_cf_own.tex`. Values are rounded to two decimals; `owned_mark` and `verdict_mark` preserve the table's formatting decisions.

`ownership-full.csv` adds all 90 full-precision `O` values, owned marks and ceiling/hatch flags from the released per-block summaries and `runs/robustness/pairs.json`. Source: `scripts/plot_paper_figures.py::fig5_same_write`.
