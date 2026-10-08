# Figure 4 — statistics & data traceability

Source data: `reading-is-not-writing/data/plot/figures/figure-04/all-bars-full.csv` (36 bars = 2 images × 6 questions × 3 conditions). Photos: extracted from the committed `figures/fig3_example.pdf` (102 px thumbnails, as in the current paper). Script: `rebuild/scripts/figure04.py`.

| Panel | Image (row_id) | Checkpoint | Highlighted question | Competitor | clean → concept write / competing write |
|---|---|---|---|---|---|
| a | NIH `00005446_000` | Qwen2.5-VL-7B, α = +0.25 | Effusion | Nodule | 0.02 → 0.56 / 0.75 |
| b | COCO `000000028449` | Qwen2.5-VL-7B, α = +0.25 | dog | bottle | 0.00 → 1.00 / 0.01 |

- Each bar is a single P(yes) = σ(ℓ<sub>yes</sub> − ℓ<sub>no</sub>) for one image, template IY, fit seed 0; no averaging, no interval.
- "Strongest competing write" = the other concept direction that raises the highlighted answer most (fixed by the source data).
- Dashed line: P(yes) = 0.5, where yes and no are equally likely.
- Values printed at the bar tips are the concept and competing writes of the highlighted row (they replace the original "0.02 → 0.56 / 0.75" string).
- Highlighted row (bold name, grey band): the question about the written concept, which is absent from the image (NIH label "No Finding"; COCO image has no dog). A "yes" there is produced by the write, not by the image. Explained in the legend's fourth entry.
- Suggested caption addition: "Grey band: the written concept, absent from the image; values at the bar tips give its two write answers. Dashed line: P(yes) = 0.5."
