# Table folders

Each `table-NN/` folder holds `displayed-source.tex`, the exact numbered table environment included by current `main.tex`; `source.txt` names its canonical TeX file. These preserve displayed values and markup, not the full-precision campaign inputs. Refresh with `python scripts/export_displayed_figure_data.py`. Table 2 additionally has `displayed-counts.csv`; Table 27 has `displayed-macros.json`.

| Number | Subject | Folder |
| --- | --- | --- |
| 1 | Main campaign result | [table-01](table-01/README.md) |
| 2 | Steering reference × verdict | [table-02](table-02/README.md) |
| 3 | Model inventory | [table-03](table-03/README.md) |
| 4 | Concept prevalence | [table-04](table-04/README.md) |
| 5 | Module coverage | [table-05](table-05/README.md) |
| 6–8 | Ownership: NIH, CheXpert, COCO | [table-06](table-06/README.md), [table-07](table-07/README.md), [table-08](table-08/README.md) |
| 9 | Controls | [table-09](table-09/README.md) |
| 10 | Evidence ledger | [table-10](table-10/README.md) |
| 11 | Geometry | [table-11](table-11/README.md) |
| 12 | Scale and numerics | [table-12](table-12/README.md) |
| 13 | Probe refits | [table-13](table-13/README.md) |
| 14 | Same-write pairs | [table-14](table-14/README.md) |
| 15 | Alternative directions | [table-15](table-15/README.md) |
| 16 | Answer directions | [table-16](table-16/README.md) |
| 17–18 | Attributes and stratification | [table-17](table-17/README.md), [table-18](table-18/README.md) |
| 19–20 | Validation | [table-19](table-19/README.md), [table-20](table-20/README.md) |
| 21 | Tower swap | [table-21](table-21/README.md) |
| 22 | Semantic endpoints | [table-22](table-22/README.md) |
| 23 | Fine-grained objects | [table-23](table-23/README.md) |
| 24–25 | Seed and mass | [table-24](table-24/README.md), [table-25](table-25/README.md) |
| 26 | Notation | [table-26](table-26/README.md) |
| 27 | Cohort roles | [table-27](table-27/README.md) |
| 28 | Protocol amendments | [table-28](table-28/README.md) |

Tables 26 and 28 are notation/protocol text, not experimental numeric plots. Their TeX is the complete relevant source. Table 25's formatted inputs are committed in `tables/table_encoding_mass.tex` and `tables/table_mass_confirmation.tex`. The other appendix tables' campaign summaries, manifest and robustness JSONs are now available in [our code repository's released `runs/` bundle](https://github.com/wy-coliney/reading-is-not-writing-code/tree/main/runs), except licensed CheXpert cohort/label manifests. Each table folder names the specific source.
