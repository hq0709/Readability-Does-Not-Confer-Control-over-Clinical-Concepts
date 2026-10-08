"""Figure 2 (fig2_overview) redrawn from the exported plot data in data/plot/figures/figure-02/.

Changes against the original, per review:
  (a) y axis in counts (0-150) instead of fractions; bar labels show the count only; axis stops at 150.
      The grade is read from the measurement now, so the bars carry no interval.
  (b) y axis extended to 1.0; the two in-plot cluster notes are removed (the legend identifies the datasets).
  (c) y axis clipped to [-0.2, 0.2]; in-plot notes removed; the main dose (0.25) is a dotted line + bold tick.
  (d) three in-plot sentences replaced by rank-1 markers and a small 'ranked 1st' key; plain rank tick labels.
Style: rebuild/scripts/style.py (house fonts and palette + Nature-style axes). QA: rebuild/scripts/qa.py.
Numbers are read from the CSVs unchanged; nothing is recomputed beyond scaling (a) fractions by 150.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import style
import qa
from style import fs, plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, NullLocator

DATA = style.FIGDATA / "figure-02"
DATASETS = ("nih", "chexpert", "coco")
COL, MK, LAB = fs.DATASET_COLOR, fs.DATASET_MARKER, fs.DATASET_LABEL
GRADES = ("readable", "answerable", "owned")


def zero_line(ax):
    ax.axhline(0, color=fs.CHANCE, ls="--", lw=0.7, zorder=1)


def panel_a(ax):
    df = pd.read_csv(DATA / "panel-a-bars-full.csv").set_index(["dataset", "grade"])
    w = 0.26
    for k, ds in enumerate(DATASETS):
        for gi, g in enumerate(GRADES):
            r = df.loc[(ds, g)]
            n = int(r.numerator)
            x = gi + (k - 1) * w
            ax.bar(x, n, w - 0.03, color=COL[ds], edgecolor="none", zorder=3)
            # every cell of the grid is in the bar, so the count is the quantity, not an estimate of one
            ax.annotate(f"{n}", (x, n), xytext=(0, 1.5), textcoords="offset points",
                        ha="center", va="bottom", fontsize=7, color=fs.INK, zorder=6)
    ax.set_xticks(range(3), GRADES); ax.tick_params(axis="x", length=0)
    # headroom above the tallest bar for its label: under the direct grade the answerable count reaches 143
    # of 150, and a label at the bar top otherwise sits in the panel title
    ax.set_ylim(0, 168); ax.set_yticks(range(0, 151, 30))
    ax.set_ylabel("concept cells (of 150)")
    ax.set_xlabel("grade")
    fs.panel_title(ax, "a", "cells passing each grade")


def panel_b(ax):
    df = pd.read_csv(DATA / "panel-b-points-full.csv")
    zero_line(ax)
    for ds in DATASETS:
        d = df[df.dataset == ds]
        ax.plot(d.read, d.ownership, marker=MK[ds], color=COL[ds], ls="none", ms=5.5, mec="white", mew=0.7, zorder=3)
    ax.set_xlim(0, 0.3); ax.set_ylim(-0.5, 1.0)
    ax.set_xticks([0, 0.1, 0.2, 0.3]); ax.set_yticks([-0.5, 0, 0.5, 1.0])
    ax.set_xlabel("mean readability $S$")
    ax.set_ylabel("mean ownership $O$")
    fs.panel_title(ax, "b", "readability vs. ownership per model")


def panel_c(ax):
    df = pd.read_csv(DATA / "panel-c-plotted-summary.csv")
    zero_line(ax)
    # the paper's main write dose; every other panel and table is graded here
    ax.axvline(0.25, color=fs.CHARCOAL, lw=0.7, ls=":", zorder=1)
    for ds in ("nih", "coco"):
        d = df[df.dataset == ds].sort_values("alpha")
        ax.fill_between(d.alpha, d.q25, d.q75, color=COL[ds], alpha=0.18, lw=0, zorder=2)
        ax.plot(d.alpha, d["median"], marker=MK[ds], color=COL[ds], lw=1.5, ms=5, mec="white", zorder=4)
    ax.set_xticks([-0.5, -0.25, 0, 0.25, 0.5]); ax.set_xlim(-0.55, 0.55)
    ax.get_xticklabels()[3].set_fontweight("bold")      # 0.25: the dose marked by the dotted line
    ax.set_ylim(-0.2, 0.2); ax.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
    ax.set_xlabel(r"write dose $\alpha$ (fraction of token norm)")
    ax.set_ylabel("ownership $O$ (median over models)")
    fs.panel_title(ax, "c", "ownership vs. write dose")


def panel_d(ax):
    df = pd.read_csv(DATA / "panel-d-ranks.csv")
    xs = np.arange(1, 121); shares = {}
    for ds in DATASETS:
        r = df[df.dataset == ds]["rank"].to_numpy()
        ax.step(xs, [(r <= x).mean() for x in xs], where="post", color=COL[ds], lw=1.5)
        shares[ds] = (r == 1).mean()
        # mark where each curve starts: its height at rank 1 is the share of cells whose own direction ranks first
        ax.plot(1, shares[ds], marker=MK[ds], color=COL[ds], ms=5, mec="white", mew=0.7, zorder=5)
    # compact key in the empty bottom-right corner (below the chest curves), instead of three sentences
    x0, y0, dy = 0.78, 0.33, 0.085
    ax.text(x0, y0, "ranked 1st", transform=ax.transAxes, ha="left", va="center", fontsize=7, color=fs.INK)
    for k, ds in enumerate(("coco", "chexpert", "nih")):
        y = y0 - (k + 1) * dy
        ax.plot(x0 + 0.02, y, transform=ax.transAxes, marker=MK[ds], color=COL[ds], ms=5, mec="white", mew=0.7)
        ax.text(x0 + 0.06, y, f"{100 * shares[ds]:.0f}%", transform=ax.transAxes, ha="left", va="center",
                fontsize=7, color=fs.INK)
    ax.set_xscale("log"); ax.set_xlim(0.88, 120); ax.set_ylim(0, 1.0)
    ticks = [1, 2, 5, 10, 20, 50, 120]
    ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels([str(t) for t in ticks])
    ax.set_xlabel("rank of own direction (1 = strongest of 120)")
    ax.set_ylabel("cumulative fraction of cells")
    fs.panel_title(ax, "d", "rank of each concept's own direction")


def main():
    style.use()
    f, axes = plt.subplots(2, 2, figsize=(fs.WIDTH, 4.3), layout="constrained")
    f.get_layout_engine().set(w_pad=0.06, h_pad=0.06, wspace=0.08, hspace=0.08)
    panel_a(axes[0, 0]); panel_b(axes[0, 1]); panel_c(axes[1, 0]); panel_d(axes[1, 1])
    handles = [Line2D([], [], marker=MK[d], ms=6, color=COL[d], ls="none", mec="white", label=LAB[d]) for d in DATASETS]
    f.legend(handles=handles, loc="outside lower center", ncol=3, fontsize=7.5, columnspacing=1.8, handletextpad=0.3)
    qa.run(f, "figure-02")
    d = style.save(f, 2, "fig2_overview")
    plt.close(f)
    print("wrote", d)


if __name__ == "__main__":
    main()
