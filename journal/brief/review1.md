# Review of draft 1 (fix all; same rules as brief.md: macros only, no CI/p-values, positive framing, no AI tells)

Factual / content
1. Abstract omits the headline result. Add: owned in \cfChestOwnedPct% of chest pairs vs \cfCocoOwnedPct% of COCO pairs, then owned-and-specific \jnTwoWayChestPct% vs \jnTwoWayCocoPct%. Add one clause that checkpoints sharing a vision tower differ in ownership. Keep <=250 words; keep Background/Methods/Results/Conclusions. Make the Conclusions sentence direct (no "helps establish").
2. Results 3.x reader section: replace "Tower swaps also changed margins in the crossed experiment" with the specific numbers: on NIH, swapping the reader changed O_q by \cfSwapReaderNihOMin on average against \cfSwapTowerNihOMin for swapping the tower (W_qq: \cfSwapReaderNihMin vs \cfSwapTowerNihMin); on COCO the tower effect was larger (\cfSwapTowerCocoOMin vs \cfSwapReaderCocoOMin). No chest cell was owned under any of the four combinations (\cfSwapChestOwned of \cfSwapChestCells) against \cfSwapCocoOwned of \cfSwapCocoCells COCO cells.
3. Methods 2.1: add cohort sizes (20,000 training, 400 calibration, 600 test rows per dataset; numbers as in ../sections/4_setup.tex) and the scale (\cfBlocks blocks, \cfCells cells, about 30 million scored answers). In 2.4 state that the random reference uses 119 random unit directions.
4. Methods 2.5: replace the displayed equation for a in {0.80, 0.85} by inline text.
5. Results "Owned directions ranked near the top among the random vectors": give the rank range (owned writes rank 1-6 among their own and the 119 random writes, as in ../sections/5_results.tex).

Framing
6. Introduction: end with a short paragraph that states what the study shows and why the evaluation is needed, positively and concretely: chest findings are readable and answerable as often as COCO objects but owned far less often (macros); random and sham references alone would certify \jnRefChest chest directions, half of which fail the labeled comparisons; the gap holds at comparable answer difficulty and for non-clinical attributes; the components downstream of the vision tower decide ownership. Three to five sentences, no bullet list.
7. Discussion: open with the principal finding in one direct sentence with numbers. Remove hedges ("relatively few", "indicate that ... reflect more than", "part of the difference"). Add a paragraph positioning the result against prior work: Ravichander et al. and Arad et al. showed that decoded information need not be used, and Haufe et al./Marks and Tegmark showed classifier normals are not the patterns that steer; RAW adds a test of specificity against labeled competitors and shows at the scale of 25 checkpoints that on chest radiographs this specificity is mostly absent while on natural images it is present. Then implications for radiology AI auditing (report the write matrix; pair any clinical intervention with competitor and off-target checks and a natural-image control). Keep the final scope paragraph to two or three neutral sentences.
8. Conclusions: four direct sentences; no hedging; no implementation details.

Template
9. Revert journal/cas-common.sty to the unmodified class file (copy from /raid/home/CAMCA/hj880/meta_radiology/template/els-cas-templates/cas-common.sty). Journals expect the stock class. Remove the empty `[orcid=]` option from \author in main.tex instead, and accept or work around the keyword box warning in main.tex only.

Recompile and report what changed.
