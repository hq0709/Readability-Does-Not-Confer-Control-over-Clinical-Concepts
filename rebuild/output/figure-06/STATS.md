# Figure 6 — statistics & data traceability

Source data: `reading-is-not-writing/data/plot/figures/figure-06/ownership-full.csv` (90 cells = 5 readers × 3 datasets × 6 concepts). Script: `rebuild/scripts/figure06.py`.

- Cell value: ownership O<sub>q</sub> = W<sub>q,q</sub> − max<sub>d≠q</sub> W<sub>q,d</sub> of each reader, for the write vector shared within its family (Gemma 3 4B/12B/27B share one set of probes and write vectors; MedGemma 4B/27B another).
- Shared symmetric colour scale ±0.9, the same as Figure 5 (max \|O\| here = 0.83). Terracotta = positive, dusty blue = negative (`style.DIVERGING`).
- Values printed for \|O\| ≥ 0.05, short form (.16 = +0.16, −.83 = −0.83).
- Corner triangle: owned cell (`owned`): NIH 1, CheXpert 3, COCO 27.
- Light hatching: clean answer at a ceiling (`ceiling`, from `runs/robustness/pairs.json`): NIH 12, CheXpert 11, COCO 23.
- Suggested caption update: "…Corner marks flag owned cells and hatching marks ceiling cells." (replaces "Dots mark owned cells…")
