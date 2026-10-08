#!/usr/bin/env bash
# Redraw the seven rebuilt figures and install them in figures/.
#
# Order matters. The scripts read data/plot/figures/, which export_campaign_plot_data.py writes from the
# campaign, so the export has to run first or the figures will be drawn from the previous grading. The two
# figures not rebuilt here -- fig1_framework, a schematic, and figA2_examples, which reads licensed CheXpert
# manifests -- stay with plot_main_figures.py and plot_paper_figures.py.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUNS="${CF_RUNS:-/rodata/azradonc_dev/m253405/cf-transfer/runs}"
cd "$ROOT"

echo "== export the plot data from $RUNS"
python scripts/export_campaign_plot_data.py --runs "$RUNS" > /dev/null

echo "== redraw"
cd rebuild/scripts
for f in figure02 figure03 figure04 figure05 figure06 figure07 figure08; do
  python "$f.py" || { echo "   FAILED $f"; exit 1; }
done

echo "== install into figures/"
cd "$ROOT"
for f in rebuild/output/figure-0*/*.pdf; do
  cp "$f" "figures/$(basename "$f")"
  echo "   $(basename "$f")"
done
