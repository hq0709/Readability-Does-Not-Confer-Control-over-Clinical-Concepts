# Revision diff (2026-09-27)

This directory freezes one revision cycle of the manuscript: the draft was revised as a single flattened file,
reviewed as an annotated diff against the flattened original, and then ported back into `main.tex`,
`sections/`, and `tables/`.

- `main_flat.tex`, `main_flat.pdf`: the baseline, `main.tex` at commit `39e0672` flattened into one file.
  Only `math_commands`, `tables/cf_colors`, and `tables/cf_numbers` remain as inputs.
- `main_revised.tex`, `main_revised.pdf`: the revised draft at commit `627e605`.
- `main_diff.tex`, `main_diff.pdf`: `latexdiff` from the baseline to the revised draft, with 53 boxed notes
  (in Chinese) that give the reason for each change. Tags: 写作 (writing), 公式 (notation), 术语 (terminology),
  精简 (condensing), 表注 (captions), 退回 agent (reverted edits by another agent), 全局 (global);
  the prefix 第四轮 marks changes from the last round.

The cycle covers three rounds of changes:

1. Writing and notation: every symbol defined at first use, symbol clashes resolved ($S_d\to\kappa_d$,
   $P_{q,d}\to F_{q,d}$, bootstrap $s_j\to\tau_j$), the lift equation simplified, terminology unified
   (consumed block, pilot study, the Effusion case, answerable).
2. Condensing: main text from about 7,900 to 5,300 words, results regrouped into seven subsections, details
   moved to Appendix A.10; every table wrapped in `\fitwidth` without a font-size switch.
3. Introduction merged and shortened against the abstract, contributions restated as full sentences, ledger
   text condensed, long captions shortened, and stale legends updated (Table 1, Coverage, the per-image figure).

When the draft was ported, one change was made outside this diff: the three chest-trained vision towers in Appendix A.2 gained citations (XraySigLIP to CheXagent, EVA-CLIP, and BiomedCLIP with LLaVA-Rad), with two new entries in `refs.bib`.

The PDFs are the frozen record. The `.tex` files input `math_commands` and `tables/cf_numbers` from the
repository root, so recompiling them later picks up the repository's current macros; compile from the root
with XeLaTeX (the diff needs `ctex` with the `fandol` fonts for the notes).
