# Figure 4 — two per-image examples

Current assets: [PDF](../../../../figures/fig3_example.pdf) · [PNG](../../../../figures/fig3_example.png). The PDF embeds the two images; their source pixel files are not separately required for this handoff.

`reported-values.json` copies `figures/fig3_example.json`: both selected row IDs, questions and annotated probabilities. `all-bars-full.csv` contains all 36 plotted bars (two examples × six questions × three conditions) from the released sliced `CORE.parquet` records. The committed `figures/fig3_example.pdf` already embeds both example images and is included by `main.tex`; no separate photo files are needed for the current edits.

Source: `scripts/plot_paper_figures.py::fig3_example` and the code repository's `runs/q25-7/{nih,coco}/outcomes/CORE.parquet`.
