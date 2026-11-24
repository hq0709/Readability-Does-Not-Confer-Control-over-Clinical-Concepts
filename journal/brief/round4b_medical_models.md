# Round 4b (author instruction): aim the clinical message at medical models

The author wants the clinical-implications text to say directly that medical VLMs and VLMs fine-tuned on
medical data are not reliable for concept-level clinical use. Drop the closed/commercial-model point
entirely (we did not test commercial models; do not mention them).

State it plainly, with the evidence attached:
- The medically fine-tuned checkpoints in the study (MedGemma 4B/27B, Lingshu 7B/32B, LLaVA-Med,
  HuatuoGPT-Vision-7B) and the checkpoints with chest-trained vision towers (CheXagent-2-3B, CheXagent-8B,
  LLaVA-Rad-7B) show the same deficit as general-purpose models: they read and answer chest findings,
  but their finding directions rarely own the answer (macros: \cfSpecTowerOwned of \cfSpecTowerN chest
  cells for chest-trained towers; \cfSpecMedOwned of \cfSpecMedN for medically tuned; \cfSpecGenOwned of
  \cfSpecGenN for general; chest-trained towers read best, \cfSpecTowerProbeAuroc vs
  \cfSpecRestProbeAuroc). Use the macros that exist in tables/cf_numbers.tex; check each before use.
- Therefore medical fine-tuning, chest-specific pretraining, and higher probe or answer accuracy do not
  make a model's finding-level evidence trustworthy. Such models should not be used as sources of
  diagnostic evidence, explanation, or finding-level correction in clinical practice until their
  concept-level control is shown per finding.
- Say what goes wrong in practice: wrong evidence shown to the radiologist, automation bias, unsafe
  edits that change other findings, audits that pass on standard controls.
Keep it assertive (the author asked for a bold Discussion) and keep every claim tied to a result. Apply to
Discussion 4.2, the abstract Conclusions, the Conclusions section, and the Highlights if one fits
(journal/Highlights.txt; <=85 characters per line). Compile from the repository root and report.

Accuracy note (checked against tables/cf_numbers.tex): chest-trained towers own 7 of 36 chest cells,
medically tuned checkpoints 16 of 72, general checkpoints 21 of 192. Medical groups are somewhat higher than
general ones, so do NOT write "the same as general models". Write that medical fine-tuning and chest
pretraining leave ownership far below the \cfCocoOwnedPct% reached on natural images (and below one in four
chest cells), i.e. they do not close the gap.
