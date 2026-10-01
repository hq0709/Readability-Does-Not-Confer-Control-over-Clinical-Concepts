# Revision diff (2026-09-28)

This directory freezes one revision cycle of the manuscript: the draft was revised as a single flattened file,
reviewed as an annotated diff against the flattened original, and then ported back into `main.tex`,
`sections/`, and `tables/`.

- `main_flat.tex`, `main_flat.pdf`: the baseline, `main.tex` at commit `7d6838a` flattened into one file.
- `main_revised.tex`, `main_revised.pdf`: the revised draft.
- `main_diff.tex`, `main_diff.pdf`: `latexdiff` from the baseline to the revised draft, with boxed notes
  (in Chinese) that give the reason for each change against the baseline. Deleted tables appear in red frames;
  tables whose content changed are followed by their earlier version in an orange frame.

The cycle changes the appendix only, apart from the removal of run-record phrases:

1. Tables: eleven bookkeeping and multi-panel tables are removed, five are cut to a single panel, and the
   remaining result tables sit in the subsections that discuss them; every table spans the text width. The
   revision column of the checkpoint table is removed.
2. Appendix A is regrouped by topic (controls and robustness, the reader, non-clinical attributes, the answer
   direction, difficulty); definitions are written as equations; each per-concept ownership table in A.5 has
   its own description.
3. The pilot protocol refers to the main-text equations instead of restating them, and the max-$T$ construction
   is defined once, in the bootstrap appendix.
4. Run records (protocol identifier, code and library versions, pinned revisions) are removed from the text.

The PDFs are the frozen record. The `.tex` files input `math_commands` and `tables/cf_numbers` from the
repository root, so recompiling them later picks up the repository's current macros; compile from the root
with XeLaTeX (the diff needs `ctex` with the `fandol` fonts for the notes).
