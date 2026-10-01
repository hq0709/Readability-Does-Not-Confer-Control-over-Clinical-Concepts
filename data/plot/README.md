# Manuscript figure and table data

This directory tracks the figures and tables included by the **current compiled `main.tex`**, not older seed-study plots. Figure folders `figure-01/` through `figure-09/` follow the final PDF's displayed numbers; each folder points to its existing PDF/PNG and contains the available plotted values. `python scripts/export_displayed_figure_data.py` refreshes printed table values; `python scripts/export_campaign_plot_data.py --runs ../reading-is-not-writing-code/runs` exports full-precision figure values from the released campaign bundle. Neither script runs experiments or redraws the PDF.

The plotting script retains older source stems. Final Figure 3 is `fig7_write_flow`, Figure 4 is `fig3_example`, Figure 5 is `fig4_write_matrices`, Figure 6 is `fig5_same_write`, Figure 7 is `fig6_ladders`, Figure 8 is `figA1_write_structure`, and Figure 9 is `figA2_examples`.

`displayed` means the number printed in the manuscript, at the paper's chosen precision; these values are sufficient when recreating the displayed table or chart labels. `full` is an optional higher-precision export from the packaged campaign records in [our code repository](https://github.com/wy-coliney/reading-is-not-writing-code/tree/main/runs). Do not change a published value merely because an unrounded source value is available. The public bundle follows the [source working guide](https://github.com/hq0709/reading-is-not-writing-code/blob/main/GUIDE.md) and its [data boundary](https://github.com/hq0709/reading-is-not-writing-code/blob/main/REPRODUCING.md).

These full-precision exports were generated from our code commit `a65e334` (incorporating the public bundle at `7f41232`). Regenerate them after changing that campaign source rather than editing plotted numbers by hand.

| Artifact | Local plot/table data | Use for this task |
| --- | --- | --- |
| [Figure 1](figures/figure-01/README.md) | displayed inset bars and reference lines | diagram and image in existing PDF/PNG |
| [Figure 2](figures/figure-02/README.md) | counts/intervals, 75 points, dose curves/IQR, rank cells | four numeric panels covered |
| [Figure 3](figures/figure-03/README.md) | three 6×6 positive-flow matrices and marginals | numeric panels covered |
| [Figure 4](figures/figure-04/README.md) | 36 bar probabilities, two selected-image IDs | both photos in existing PDF/PNG |
| [Figure 5](figures/figure-05/README.md) | six 6×6 write matrices and marks | 216 cells covered |
| [Figure 6](figures/figure-06/README.md) | same-write ownership and ceiling flags | 90 cells covered |
| [Figure 7](figures/figure-07/README.md) | model-scale ownership values and marks | 54 values covered |
| [Figure 8](figures/figure-08/README.md) | three median 6×6 write matrices | 108 cells covered |
| [Figure 9](figures/figure-09/README.md) | ten qualitative examples | existing PDF/PNG; no numeric remake requested |
| [Table 1](tables/table-01/README.md), [Table 2](tables/table-02/README.md) | displayed table source; Table 2 counts CSV | displayed values covered |
| [Appendix Tables 3–28](tables/README.md) | one folder per table, displayed TeX; Table 27 macros | displayed values covered |

The existing Figure PDFs (including embedded photos) and PNGs are committed and already used or previewable from `main.tex`; separately locating photo files is not required for this materials handoff. [Source-asset note](MISSING_INPUTS.md) distinguishes that optional future work from the data needed here.
