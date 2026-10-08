# Figure 5 — statistics & data traceability

Source data: `reading-is-not-writing/data/plot/figures/figure-05/write-matrices-full.csv` (216 cells = 6 matrices × 6 × 6). Script: `rebuild/scripts/figure05.py`.

| Panel | Checkpoint | Dataset | max \|W\| | Owned concepts (corner mark) |
|---|---|---|---|---|
| a | Qwen2.5-VL-7B | NIH | 0.53 | none |
| b | Qwen2.5-VL-72B | NIH | 0.53 | Atelectasis, Cardiomegaly, Mass |
| c | Lingshu 32B | NIH | 0.20 | Pneumothorax, Cardiomegaly |
| d | Qwen2.5-VL-7B | COCO | 0.87 | all six |
| e | Qwen3-VL-32B | COCO | 0.24 | all six |
| f | Lingshu 32B | COCO | 0.55 | all six |

- Cell value W<sub>q,d</sub>: paired mean change in P(yes) of question *q* (row) under the write of direction *d* (column), at α = +0.25, over the 600 test rows of the block.
- Shared symmetric colour scale ±0.9 (max \|W\| = 0.87 rounded up, as in the original). Terracotta = positive, dusty blue = negative (project diverging map `style.DIVERGING`).
- Values printed for \|W\| ≥ 0.05, in short form (.19 = +0.19, −.07 = −0.07).
- Corner triangle: owned concept (`owned_diagonal` = True: the write clears the random and sham reference and moves the concept's own answer further than any competitor does).
- Suggested caption update: "…The small corner mark flags owned concepts." (replaces "The diagonal is outlined and owned concepts carry a dot.")
