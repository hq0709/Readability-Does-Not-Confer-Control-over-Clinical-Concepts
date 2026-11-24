# Round 4: clinical-implications Discussion + plain-language rewrite (Methods first)

Same rules as brief.md: numbers only through existing macros (\cf..., \jn...), never invent a number,
no CI / p-values, \cite only with keys in refs.bib, positive contribution framing, no AI-writing tells
(no aphoristic closers, no "not X but Y" chains, no forced triads, no em-dash chains, no "Notably").
Keep every \label alive. Files: journal/sections/*.tex only (plus meta_radiology.tex abstract if needed).
Compile from the repository root: `latexmk -pdf -interaction=nonstopmode meta_radiology.tex`
(PATH=/raid/home/CAMCA/hj880/tools/.TinyTeX/bin/x86_64-linux:$PATH). No undefined refs, no new Overfull.

## A. Discussion: a new, substantial subsection on clinical implications (the author wants this bold)
Structure Discussion as subsections:
4.1 Principal findings (keep, tighten).
4.2 Clinical implications (NEW, ~600-800 words, the centre of the Discussion). Argue strongly, but every
    claim must follow from the results; state the scope of each claim through its wording, not through
    disclaimers. Points to develop, each with the supporting result (macros):
  - Concept-level explanations of medical VLMs can name the wrong finding. A probe that reads
    "effusion" and a steering effect on the effusion answer look like evidence that the model used
    effusion; on chest radiographs the nodule direction moves the effusion answer more (Effusion case,
    \cfSeedWEff vs \cfSeedWNodule). An explanation built this way would hand the radiologist evidence for
    the wrong finding. Misattributed evidence is worse than no evidence: it invites automation bias, it
    can make a wrong answer look justified, and it can make a right answer look justified for the wrong
    reason.
  - Concept-level correction is unsafe. Editing a model to suppress a false-positive finding (e.g.
    effusion) along its probe direction also moves other findings' answers: among chest directions that
    pass standard controls, off-target movement summed over the other answers is a median
    \jnOffTargetChest times the intended effect (COCO \jnOffTargetCoco). A fix for one finding silently
    changes the report for others.
  - Standard checks give false assurance. Random and sham controls certified \jnRefChest chest
    directions; half failed the labeled comparisons. Audits, model cards and regulatory documentation that
    rely on probe accuracy, answer accuracy, or random-direction controls would pass these models.
  - Medical fine-tuning and chest-specific vision towers do not resolve it: chest-trained towers read the
    findings best (\cfSpecTowerProbeAuroc vs \cfSpecRestProbeAuroc) yet own \cfSpecTowerOwned of
    \cfSpecTowerN chest cells; medical checkpoints (MedGemma, Lingshu, LLaVA-Med, CheXagent,
    HuatuoGPT-Vision, LLaVA-Rad) show the same deficit as general ones. Scale helps only in some families.
  - Closed commercial models: their internal concept explanations cannot be checked at all, because
    activation access is needed; every checkpoint whose internals could be tested, general or medical,
    3B to 72B, largely failed. Until a model's concept-level control is demonstrated, its concept-level
    explanations and edits should not be treated as diagnostic evidence. Phrase as a strong
    recommendation; do NOT claim we measured commercial models.
  - Consequences for clinical use: VLM answers about chest findings should not be accepted as diagnostic
    evidence on the strength of decodability or explanation; for deployment, require RAW-style
    certification per finding (write matrix, competitor and off-target checks, natural-image control),
    keep the radiologist as the decision maker, and treat finding-level edits as untested changes to the
    whole report.
4.3 Why the label direction fails on radiographs (short): reader downstream of the tower; answer
    direction nearly orthogonal; non-clinical attributes owned at the same low rate, pointing to a signal
    shared across findings rather than finding-specific evidence.
4.4 Recommendations for evaluating medical VLMs (short numbered or compact paragraph).
4.5 Scope (2-3 neutral sentences, keep as is).
Update the abstract Conclusions sentence and the Conclusions section to carry the clinical message
(still <=250 words abstract).

## B. Plain-language rewrite, Methods first
Goal: a radiologist with basic statistics can follow Methods on first reading.
- Open Methods with a short overview paragraph (5-6 sentences) that walks through RAW in plain words:
  read the finding with a probe, ask the model, add the finding's direction to the image features,
  compare with the other findings' directions and with random/shuffled controls, grade.
- One idea per sentence; short sentences; active voice; explain each symbol right where it appears;
  define a term before using it; prefer words over symbols where the symbol is used once.
- Move engineering detail (per-family token masks, PCG64 seeds, preflight checks A-G, batch effects,
  float precision, token-weight variants, displacement lift) into compact, clearly titled subsubsections
  at the END of Methods ("2.x Implementation details"), so the main flow reads cleanly. Shorten them;
  keep only what is needed to reproduce.
- Results: same treatment, lighter. Lead each subsection with its one-sentence finding, then the
  numbers. Split long number-laden sentences. Do not remove results that support the thesis.
- Keep all tables and figures, all macros, all labels.

Report: the new section map, word counts before/after for Methods and Discussion, and anything you
could not express with macros.
