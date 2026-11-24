# Task: fold the appendices into the main text (Meta-Radiology research articles have no page limit)

The user wants no appendices and no supplementary material: everything in journal/sections/app_*.tex goes
into the numbered main sections. Same rules as brief.md: numbers only through macros (\cf..., \jn...),
no CI / p-values / "interval", positive contribution framing, no AI-writing tells, \cite only, plain
journal prose for a radiology readership, define terms at first use.

Target structure (keep all existing labels alive so every \ref resolves; drop "Appendix" wording):
2 Materials and methods
  2.1 Datasets, labels and cohorts      <- app_campaign "Labels, registration, and artifact" + app_repro "Cohort roles"
                                           + the fine-grained COCO selection rule (app_repro protocol amendments)
  2.2 Models and selected vision layers  <- app_campaign grid (Table cf-models) + app_repro "Consumed sites per family"
                                           and "consumed-token mask" (condense the per-family list into a compact
                                           paragraph or keep as a short itemized list)
  2.3 Reading and writing (existing) + projection/probe details from app_repro "Projection, lift, scaler, and probe"
  2.4 Label directions and controls (existing) + app_repro "Control constructions" + alternative directions
      and token weights (equations eq:displacement-lift, eq:token-weights)
  2.5 Questions and scoring             <- app_prompts (templates, score); move the notation table here or drop it
                                           if the key-terms table already covers it (keep symbols that are used)
  2.6 Ownership and direction specificity (existing; column selectivity eq:column-selectivity moves here)
  2.7 Decision rules, acceptance checks and analyses (existing + app_campaign "Acceptance decisions", "Coverage
      and cost", answer-direction fitting eq:answer-direction and whitened cosine eq:whitened-cos, semantic
      endpoints eq:endpoint-reference, crossed tower/reader eq:crossover, replay, common support)
  2.8 Registration and reproducibility (registration paragraph + protocol amendments, short)
3 Results: integrate the supporting results next to the result they support; each existing subsection gains
  its detail paragraphs and tables/figures from the appendix (controls and robustness -> 3.3; reader,
  crossed tower, replay, size/family, chest-trained towers -> 3.6; attributes -> 3.5; answer direction,
  semantic endpoints -> 3.7; difficulty/fine-grained -> 3.4; write structure figure and per-image examples
  -> 3.2; the independent Qwen2.5-VL-7B replication (app_seed_results, Table cf-seed) -> 3.2 where the
  Effusion case is reported). Avoid repeating a number already stated; merge rather than append.
Then remove the \appendix block and the app_* \input lines from journal/main.tex (delete the counterwithin
lines too), and delete the "Appendix" references everywhere. Keep figures/tables as floats near first
mention; full-width floats as figure*/table*. Tables must not overflow the column or page (use the
existing \fitwidth / \cftabsize), and nothing may overlap.

Compile with
`export PATH=/raid/home/CAMCA/hj880/tools/.TinyTeX/bin/x86_64-linux:$PATH; cd journal; TEXINPUTS=.:..//: BIBINPUTS=..: latexmk -pdf -interaction=nonstopmode main.tex`
and fix every undefined reference and every Overfull hbox > 1pt you introduce. Report the new section map.
