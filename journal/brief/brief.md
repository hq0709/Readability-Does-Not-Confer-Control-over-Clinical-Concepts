# Brief: port the ACL paper to a Meta-Radiology research article

You are drafting the journal version of the paper "Rethinking Concept-Level Control in Medical
Vision-Language Models". Work ONLY inside `journal/` of the repository at
/raid/home/CAMCA/hj880/meta_radiology/paper. Never edit files outside `journal/`
(the ACL source in `sections/`, `tables/`, `main.tex` stays untouched; read it freely).

## Source of truth
The ACL version is `../main.tex` + `../sections/*.tex` + `../tables/*.tex`. Every number in the prose
is a LaTeX macro from `../tables/cf_numbers.tex` (prefix `\cf...`) or, for the new journal analyses,
from `journal/journal_numbers.tex` (prefix `\jn...`). Never type a number that a macro carries; never
invent a number. If you need a number that has no macro, leave `\textcolor{red}{[NUMBER?]}` and list it
in your final message.

## Target journal: Meta-Radiology (KeAi/Elsevier), research article
- Audience: radiologists, medical physicists, medical-imaging AI researchers. They know chest findings
  (effusion, atelectasis …) but NOT interpretability jargon. Define every technical term at first use in
  plain words (probe, steering, direction, write, reader, competitor, sham, cell, block). Prefer
  plain terms: "checkpoint–concept pair (cell)" defined once; avoid "campaign", "grid", "consumed site"
  in the main text (say "evaluation", "set of models", "the visual tokens passed to the language model").
- Required section order (already wired in journal/main.tex):
  1 Introduction (fold the old Background/Related Work into it as positioning, not a list)
  2 Materials and methods
  3 Results
  4 Discussion (principal findings, implications for radiology AI auditing, a SHORT neutral scope
    paragraph — no long limitation list)
  5 Conclusions (no implementation details)
  then declarations (file 6_declarations.tex).
- Abstract: structured, <=250 words, headings Background:, Methods:, Results:, Conclusions:
  (write as `\textbf{Background:} ...` paragraphs). No citations in the abstract. Write it to
  `journal/sections/abstract.tex`.
- Citations: superscript numbered style. Use ONLY `\cite{key}` (natbib super). NEVER `\citep`, `\citet`,
  `\citealp`. When an author name is needed write it: `Ravichander et al.\cite{ravichander2021probing}`.
  Only cite keys present in `../refs.bib` (two new keys are available: `li2023iti` — Inference-Time
  Intervention, shifts activations along probe directions to steer truthfulness; `vonrutte2024guide` —
  steers LLMs along linear-probe concept directions). Use these to support the sentence that steering
  practice uses probe directions as steering vectors.
- Figures/tables: two-column CAS class. Full-width floats are `figure*`/`table*`. Keep the existing
  figure files and table inputs (`\input{tables/...}` resolves to ../tables). Captions must be
  self-contained and short: a bold title sentence, then what is plotted. Remove internal markers that
  confuse readers (e.g. explain or drop "Hatched: excluded").

## Style rules (from the authors; mandatory)
1. Positive contribution framing: tell the contribution story, argue the evaluation is necessary, and
   show the results prove it. No self-undermining sentences; no repeated disclaimers.
2. NO confidence intervals anywhere (no "95% CI", no "[lo, hi]" intervals, no "interval" wording, no
   p-values). Where spread is needed, use a standard deviation (`\jn...Sd` macros are bootstrap SDs over
   checkpoints). Interquartile ranges in existing tables may stay.
3. No AI-writing tells: no aphoristic paragraph closers ("X is a property of Y"), no "not X but Y"
   contrast chains, no forced triads, no em-dash chains, no "Notably/Crucially/Importantly", no bold
   inline labels in prose. Plain, direct, journal prose. American spelling.
4. No v1/v2 or "pilot version" talk; one method, RAW.
5. Scope claims precisely: findings are established for chest radiographs (NIH ChestX-ray14, CheXpert
   Plus) with COCO as natural-image control; RAW "applies to open-weight VLMs whose activations can be
   accessed". Do not write "any open-weight VLM" or unqualified "decodability is not enough for control".

## How to use the reviews (`journal/brief/reviews.md`)
Reviews are input, not orders. Revise where the point is right for a radiology journal:
- R-ownership-vs-specificity (oKEU W1, N3dN 1, bZHf "per-question"): ownership O_q is a ROW criterion
  (is question q moved most by its own direction). Add a COLUMN criterion: column margin
  C_d = W_{d,d} - max_{q != d} |W_{q,d}| (the write moves its own answer more than any other answer, in
  either direction). A cell is "specific" when the steering reference is met and C_d > 0, and
  "owned and specific" when it is owned and C_d > 0. Results (macros in journal_numbers.tex):
  chest owned and specific \jnTwoWayChest/300 (\jnTwoWayChestPct%) vs COCO \jnTwoWayCoco/150
  (\jnTwoWayCocoPct%); NIH \jnTwoWayNih, CheXpert \jnTwoWayChex (each of 150).
  Of the chest owned cells, \jnOwnedNotColChest of 44 (\cfChestOwned) move some other answer at least as
  much as their own (COCO \jnOwnedNotColCoco of 117). Among directions with steering reference met
  (\jnRefChest chest, \jnRefCoco COCO), off-target movement summed over the other five questions is a
  median \jnOffTargetChest times the own effect on chest vs \jnOffTargetCoco on COCO. Median column
  selectivity kappa (Eq. in appendix) \jnKappaMedChest chest vs \jnKappaMedCoco COCO.
  Define both criteria in Methods (new subsection, with an equation for C_d) and report in Results.
  Fix the intro sentence: the Effusion example shows that the Effusion ANSWER is not owned by its
  direction (another finding's direction moves it more), not that "the effusion direction is not
  specific to effusion".
- R-added-value (N3dN 4, bZHf): new Results subsection "What the competitor comparison adds". A
  standard steering evaluation (random + sham references only) would certify \jnRefChest of 300 chest
  directions (\cfChestRefMet). Requiring the row comparison removes \jnRefLostChest; adding the column
  comparison removes \jnOwnedNotColChest more, leaving \jnTwoWayChest: \jnRefNotTwoWayChest of the
  \jnRefChest certified chest directions (\jnRefNotTwoWayChestPct%) are not concept-specific, against
  \jnRefNotTwoWayCoco of \jnRefCoco on COCO (\jnRefNotTwoWayCocoPct%). So the competitor-aware
  evaluation halves the set of chest directions a standard evaluation would certify, while leaving
  natural-image directions almost untouched. Also keep that most chest writes fail the reference
  itself (\cfChestRefBelow of 300) — present this as a finding about chest radiographs (small own
  writes), not as a weakness of the criterion.
- R-competitor-set (N3dN 2): competitor-subset sensitivity. Grading against every subset of k of the 5
  competitors and averaging: expected chest owned count \jnSubOneChest (k=1), \jnSubTwoChest (k=2),
  \jnSubThreeChest (k=3), \jnSubFourChest (k=4), vs 44 with all five; COCO stays at 117 for every k.
  So even a single randomly chosen competitor leaves chest ownership far below COCO; the result does
  not hinge on which competitors are chosen. Combine with existing geometry result: the strongest
  competitor matches the most similar direction or most co-occurring label only at chance
  (Table geometry, existing text in ../sections/5_results.tex controls paragraph).
- R-difficulty (oKEU W2, N3dN 2): keep the stratified top-bin comparison (12/37 vs 145/162,
  difference \jnTopDiff, bootstrap SD \jnTopDiffSd — replace the old CI). Add a common-support
  analysis with better overlap: all cells with clean-answer AUROC >= 0.80, pooling easy and
  fine-grained COCO objects: chest \jnCsEightyChestOwned/\jnCsEightyChestN (\jnCsEightyChestPct%,
  including \jnCsEightyNihN NIH cells, \jnCsEightyNihOwned owned) vs natural
  \jnCsEightyNatOwned/\jnCsEightyNatN (\jnCsEightyNatPct%); adjusted for clean-answer AUROC and probe
  selectivity with a logistic model, the chest-minus-natural difference in ownership probability is
  \jnCsEightyAdj (bootstrap SD over checkpoints \jnCsEightyAdjSd); at AUROC >= 0.85 it is
  \jnCsEightyFiveAdj (SD \jnCsEightyFiveAdjSd). Also lean on the within-radiograph control: non-clinical
  attributes (projection, sex, age) of the same radiographs are read at least as well and owned at the
  same low rate (existing macros cfAttr*, cfStratAttrTop*), which a pure-difficulty account does not
  predict. Report the matched estimator values in the appendix as before but without CIs.
- R-component (N3dN 3): say precisely what the shared-tower, crossed tower/reader swap
  (appendix "Crossed tower and reader") and connector-site writes show: the deficit follows the reader
  (connector + language model). Writing at the connector output, which bypasses the connector and is
  read by the language model alone, keeps the chest/COCO sign pattern (median connector-site O_q
  -0.013 NIH, -0.009 CheXpert, +0.003 COCO; Table controls in ../tables/table_cf_controls.tex, IQR
  allowed). Attribute to "the components downstream of the vision tower"; the language model alone
  reproduces the pattern at the connector site. Do not claim a clean connector-vs-LM split beyond this.
- R-answer-direction (oKEU W3): reframe 'answer direction' results as OUTPUT controllability: it is
  fitted to the model's answers, so its higher ownership is expected by construction; the informative
  result is the geometry — on chest radiographs it is nearly orthogonal to the label direction while on
  COCO they align — and its weak agreement with report labels (AUROC vs label) shows the model answers
  along a signal the clinical label does not mark. State clearly it is a handle on the model's answer,
  not a clinically validated concept.
- R-motivation (bZHf): cite li2023iti, vonrutte2024guide, zou2023representation, turner2023steering,
  panickssery2024caa, kim2018tcav as practice that takes a probe/concept direction as the steering
  vector. Position against Ravichander et al. (decodable info need not be used) and Arad et al.
  (detecting vs controlling features): those show that decoding does not guarantee USE; RAW tests a
  different, stronger property, SPECIFICITY against labeled competitors, and measures it at scale in
  medical VLMs. Explain why random/sham references cannot detect this (they carry no label).
- R-clarity (bZHf): move the decision rules into Methods (Table of grades stays); define terms on first
  use; add a short "Key terms" table (term → plain definition) in Methods. Motivate design choices in
  one clause each (why the selected vision layer: it is where both reading and writing act on what the
  language model receives; why norm-scaled alpha: comparability across models; why six concepts:
  datasets' most frequent findings with enough positives; why yes/no: a scalar answer at one position).
- Code availability: code at https://github.com/hq0709/reading-is-not-writing-code (public).

## Files to write (journal/sections/)
- `abstract.tex` (plain text body only, structured, <=250 words)
- `1_introduction.tex`, `2_methods.tex`, `3_results.tex`, `4_discussion.tex`, `5_conclusions.tex`,
  `6_declarations.tex` (unnumbered sections via `\section*`: CRediT authorship contribution statement,
  Ethics statement, Declaration of competing interest, Funding, Data and code availability,
  Declaration of generative AI and AI-assisted technologies in the writing process. For facts the
  authors must supply (CRediT roles, funding, competing interests, AI-use wording) write a standard
  sentence and wrap the uncertain part in `\textcolor{red}{[...]}` so the authors confirm it.)
- Keep labels used by the appendix (`sec:...`, `eq:...`, `tab:...`, `fig:...`) so cross-references
  resolve; the appendix files in journal/sections/app_*.tex reference e.g. eq:lift, eq:selectivity,
  eq:margin, eq:intervention, sec:robust-geometry, sec:coco, sec:attributes, fig:write-matrices,
  fig:rank, fig:readers, fig:ladders, tab:grades, tab:cf-main …  grep them and keep every label alive.
- Figures and tables: reuse all figures and tables the ACL main text uses (teaser, framework,
  overview, example, write matrices, readers, ladders, rank, and the tables). Add ONE new compact table
  `tab:specificity` (table, single column) in Results: rows NIH / CheXpert / chest total / COCO;
  columns: reference met, owned (row), specific (column), owned and specific. Use the \jn macros
  (\jnRefNih, \cfNih..., etc.; owned counts NIH 16, CheXpert 28 are \cfChestOwned split — use
  existing macros if available, else compute: owned = \jnRef - \jnRefLost per dataset; write it as
  macros only).
- Length: no hard limit; aim for a main text similar to the ACL version plus the new analyses,
  without implementation detail that belongs in the appendix.

When done, compile from journal/:
`export PATH=/raid/home/CAMCA/hj880/tools/.TinyTeX/bin/x86_64-linux:$PATH; TEXINPUTS=.:..//: BIBINPUTS=..: latexmk -pdf -interaction=nonstopmode main.tex`
and fix every undefined reference/citation/macro you introduced. Final message: list of files written,
any red placeholders, and every number you could not express with a macro.
