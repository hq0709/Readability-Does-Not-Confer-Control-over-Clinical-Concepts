"""A new design for the write figure: the comparison itself, per concept, over every checkpoint.

The present figure is six heat maps of W_{q,d} for three hand-picked checkpoints per dataset. A heat
map shows the whole matrix, but the claim needs only two of its numbers per concept: what the own
write did, and what the best rival write did. Reading that comparison off a 6x6 grid is work the
figure can do instead.

  C  dumbbells: per concept, the median own write and the median best rival across every checkpoint,
     joined, with the per-checkpoint values behind them. 25 checkpoints, not 3.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import aclsize
from aclsize import fs
import style
import qa

DATA = __import__("pathlib").Path(__file__).resolve().parent / "data"
DATASETS = ("nih", "chexpert", "coco")
TITLE = {"nih": "NIH ChestX-ray14", "chexpert": "CheXpert Plus", "coco": "COCO (control)"}
OWN_WINS, RIVAL_WINS = "#A9503F", "#44709F"          # the project diverging ends


def panel(ax, d, ds, letter, ylabels):
    g = d[d.dataset == ds]
    concepts = list(dict.fromkeys(g.concept))
    med = g.groupby("concept")[["W_qq", "max_other"]].median().loc[concepts]
    rng = np.random.default_rng(1)
    ax.axvline(0, color=fs.CHANCE, lw=0.7, ls=":", zorder=1)
    for i, c in enumerate(concepts):
        rows = g[g.concept == c]
        jit = rng.uniform(-0.12, 0.12, len(rows))
        ax.plot(rows.max_other, i + 0.22 + jit, ls="none", marker="o", ms=2.0,
                mfc=RIVAL_WINS, mec="none", alpha=0.30, zorder=2)
        ax.plot(rows.W_qq, i - 0.22 + jit, ls="none", marker="o", ms=2.0,
                mfc=OWN_WINS, mec="none", alpha=0.30, zorder=2)
        a, b = float(med.loc[c, "max_other"]), float(med.loc[c, "W_qq"])
        win = b > a
        ax.plot([a, b], [i, i], color=OWN_WINS if win else RIVAL_WINS, lw=1.9,
                solid_capstyle="round", zorder=4, alpha=0.85)
        ax.plot(a, i, marker="o", ms=5.0, mfc="white", mec=RIVAL_WINS, mew=1.4, zorder=5)
        ax.plot(b, i, marker="o", ms=5.0, mfc=OWN_WINS, mec="white", mew=0.8, zorder=6)
    ax.set_yticks(range(len(concepts)),
                  [style.SHORT_CONCEPT.get(c, c) for c in concepts] if ylabels else [""] * len(concepts))
    ax.set_ylim(len(concepts) - 0.5, -0.65)
    ax.tick_params(axis="y", length=0)
    # the limits hold every point: at (-0.33, 0.78) eighteen of the 450 cells had a value outside
    # the axes and were silently clipped off the strip
    ax.set_xlim(-0.72, 0.96); ax.set_xticks([-0.5, -0.25, 0, 0.25, 0.5, 0.75])
    ax.set_xticklabels(["−.5", "−.25", "0", ".25", ".5", ".75"])
    # the count belongs in the title: under the panel it lands on the shared axis label, and inside
    # the axes it lands on the strip
    n_win = int((med.W_qq > med.max_other).sum())
    ax.set_title(f"({letter})  {TITLE[ds]}\n{n_win} of {len(concepts)} own writes win",
                 fontsize=9, pad=4, linespacing=1.35)


def main():
    d = pd.read_csv(DATA / "cells.csv")
    aclsize.use()
    f, axes = plt.subplots(1, 3, figsize=(fs.WIDTH, 2.60), layout="constrained")
    f.get_layout_engine().set(w_pad=0.05, h_pad=0.05, wspace=0.05)
    for k, ds in enumerate(DATASETS):
        panel(axes[k], d, ds, "abc"[k], ylabels=True)
    axes[1].set_xlabel(r"change in $P(\mathrm{yes})$ at $\alpha=+0.25$, median over 25 checkpoints")
    faint = lambda c: Line2D([], [], ls="none", marker="o", ms=2.8, mfc=c, mec="none", alpha=0.45)
    handles = [Line2D([], [], ls="none", marker="o", ms=5, mfc=OWN_WINS, mec="white", mew=0.8,
                      label="median own write"),
               Line2D([], [], ls="none", marker="o", ms=5, mfc="white", mec=RIVAL_WINS, mew=1.4,
                      label="median strongest rival"),
               (faint(OWN_WINS), faint(RIVAL_WINS))]
    labels = ["median own write", "median strongest rival", "one checkpoint"]
    from matplotlib.legend_handler import HandlerTuple
    f.legend(handles=handles, labels=labels, handler_map={tuple: HandlerTuple(ndivide=None, pad=0.6)},
             loc="outside lower center", ncol=3, fontsize=7.5, columnspacing=2.0, handletextpad=0.5)
    qa.run(f, "fig4-C")
    aclsize.save(f, "fig4-C-dumbbell"); plt.close(f)


if __name__ == "__main__":
    main()
