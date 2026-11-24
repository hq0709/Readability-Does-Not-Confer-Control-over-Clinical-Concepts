# ARR reviews of the ACL version (Submission 4295)

## Reviewer oKEU (Soundness 3, Overall 3 Findings)
W1. Ownership (Eq. 4) is row-wise: whether question q is moved most by its own direction. It does not show that steering the target leaves other concepts unaffected; a direction could pass ownership while strongly changing several unrelated answers. Column selectivity is low for chest (App. A.10). Clarify ownership vs intervention specificity; consider combining row-wise ownership with column-wise selectivity.
W2. Medical vs natural comparison may be confounded by task difficulty / answerability. Table 15: matched difference shrinks to -0.066 controlling clean-answer AUROC and -0.024 also matching selectivity. High-AUROC stratum has only 37 chest cells, all CheXpert Plus. Wants discussion and, if feasible, difficulty-controlled evaluations with better overlap.
W3. Answer-fitted directions (5.6) achieving higher ownership is not surprising (they are fitted to the outputs); they align less with clinical labels (Table 13). Higher ownership does not imply clinically meaningful concepts. Distinguish output controllability from semantic correctness.
Comment: no accessible code repository link; provide one.

## Reviewer N3dN (Soundness 3, Overall 3 Findings)
1. Ownership does not mean the direction controls only that concept (off-target effects).
2. Cross-domain bias: chest findings correlated and visually similar; COCO objects easier to distinguish. Only six concepts per dataset, sensitivity to competitor choice. Suggest analysing concept correlation and competitor selection, or visually similar natural-image concepts.
3. Component attribution: shared-tower results attributed to downstream components, but connector vs language model not separated.
4. Value of ownership: 244/300 chest directions already fail random/sham; competitor comparison adds only 12 failures. Clarify the added value of competitor-aware evaluation.

## Reviewer bZHf (Soundness 2, Overall 1.5)
- Hard to follow; dense sentences; ad hoc terminology (cell, block, grid, campaign, write, reader, competitor, sham, consumed site) used before definition; main text full of implementation details; motivation for design choices missing; protocol and decision rules relegated to appendix; medical terms unexplained (for an NLP venue).
- Motivation "Used together, they assume that a concept decodable along a direction can also be controlled along it" cites no work making the assumption; prior work (Ravichander 2021; Arad 2025) already shows decodable info need not be used, so the finding is expected and novelty reduced.
- Ownership mostly captures writes with no effect: 244/300 do not exceed random/sham; only 12/300 show the competitor phenomenon.
- Ownership margin is per question, so it measures whether question q is moved most by its own direction, not whether direction d is specific to concept d. Hence "the effusion direction is thus not specific to effusion" is incorrect.
- Design choices not motivated; claims "for any open-weight VLM" and "decodability is not enough for control" are overstated given six binary concepts on two chest datasets.
- Figure 1 unclear; Figure 2 hard to follow ("Hatched: excluded"); Table 2 caption hard to follow and table overloaded; related work reads as a list; conclusion has implementation details ("up to bf16 precision").
