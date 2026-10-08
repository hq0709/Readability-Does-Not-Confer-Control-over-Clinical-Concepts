# Figure 7 — statistics & data traceability

Source data: `reading-is-not-writing/data/plot/figures/figure-07/ownership-full.csv` (54 values = 9 checkpoints × 6 concepts). Script: `rebuild/scripts/figure07.py`.

| Panel | Ladder | Dataset | Sizes | Owned cells per size | Thick line (largest O at the largest size) |
|---|---|---|---|---|---|
| a | Qwen2.5-VL | NIH | 3B, 7B, 32B, 72B | 0, 0, 1, 3 | Atelectasis (0.54 at 72B) |
| b | Qwen3-VL | NIH | 4B, 8B, 32B | 0, 0, 1 | Nodule (0.17 at 32B) |
| c | Lingshu | CheXpert | 7B, 32B | 3, 5 | Edema (0.11 at 32B) |

- Each point: ownership O<sub>q</sub> of one concept in one checkpoint (α = +0.25, 600 test rows); no averaging.
- Filled marker = owned (`owned` = True), open = not owned. Colour and marker are fixed per concept across panels (project concept palette).
- x axis: model size on a log2 scale; equal panel widths, each spanning its own sizes plus 12% padding, so the distance per doubling differs between panels.
- y axis: each panel has its own range (a: −0.6 to 0.6; b: −0.3 to 0.2; c: −0.1 to 0.3), so heights are not comparable across panels; the dashed line marks O = 0 in each.
- Suggested caption update: "…The concept with the largest ownership at the largest size is drawn as a thick solid line (Atelectasis, Nodule, Edema), the other concepts dashed; filled markers are owned cells. Each panel has its own y range." (replaces "…drawn bold…; ringed markers are owned cells.")
