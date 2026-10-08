"""Figure 8 (figA1_write_structure) redrawn from data/plot/figures/figure-08/median-write-matrices-full.csv.

Same treatment as Figures 5 and 6 (see figure05.py):
  colour      project diverging map (style.DIVERGING); the figure keeps its own symmetric limit +-0.5 (max |median W|
              = 0.45 rounded up, as in the original), round ticks
  numbers     short form (.36 / -.01); unlike Figure 5 every cell stays annotated, because the chest medians all lie
              within +-0.05 and a 0.05 threshold would blank two of the three panels; |v| < 0.005 prints "0"
  diagonal    no outline
  axes        x-axis title "written direction d" on the middle panel; colour-bar label shortened
Titles keep the original two-line form, second line shortened ("over 25" -> ", 25") so neighbours do not touch. Values are read from the CSV unchanged.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import style
import qa
import figure05 as f5
from style import fs, plt
from matplotlib.colors import TwoSlopeNorm

DATA = style.FIGDATA / "figure-08"
DATASETS = ("nih", "chexpert", "coco")
CMAP = style.DIVERGING
VLIM = 0.5


def short0(v):
    return "0" if abs(v) < 0.005 else f5.short(v)


def main():
    fs.use_house_style()
    df = pd.read_csv(DATA / "median-write-matrices-full.csv")
    norm = TwoSlopeNorm(vmin=-VLIM, vcenter=0.0, vmax=VLIM)
    FW = fs.WIDTH
    P, gap, x0 = 1.25, 0.45, 0.60
    title_h, xt_h, xl_h, bar_h = 0.40, 0.36, 0.16, 0.62
    FH = title_h + P + xt_h + xl_h + bar_h
    y0 = bar_h + xl_h + xt_h
    f = plt.figure(figsize=(FW, FH))
    for k, ds in enumerate(DATASETS):
        g = df[df.dataset == ds]
        concepts = list(dict.fromkeys(g.question)); n = len(concepts)
        W = g.pivot(index="question", columns="written_direction", values="value").loc[concepts, concepts].to_numpy()
        ax = f.add_axes(f5.rect(FW, FH, x0 + k * (P + gap), y0, P, P), label=f"med{k}")
        ax.pcolormesh(np.arange(n + 1), np.arange(n + 1), W, cmap=CMAP, norm=norm, edgecolors="white", linewidth=f5.GAP, zorder=2)
        ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect("equal"); ax.grid(False); ax.tick_params(length=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        lab = [style.SHORT_CONCEPT.get(c, c) for c in concepts]
        ax.set_xticks(np.arange(n) + 0.5); ax.set_yticks(np.arange(n) + 0.5)
        ax.set_xticklabels(lab, rotation=45, ha="right", rotation_mode="anchor", fontsize=7.5)
        ax.set_yticklabels(lab, fontsize=7.5)
        for i in range(n):
            for j in range(n):
                v = W[i, j]
                col = "white" if f5.lum(CMAP(norm(v))) < 0.5 else fs.INK
                ax.text(j + 0.5, i + 0.5, short0(v), ha="center", va="center", fontsize=f5.ANNOT_SIZE, color=col, zorder=6)
        n_ck = int(g.checkpoints.iloc[0])
        ax.set_title(f"({'abc'[k]})  {fs.DATASET_LABEL[ds].replace(' (control)', '')}\nmedian $W_{{q,d}}$, {n_ck} checkpoints",
                     fontsize=8, pad=4, linespacing=1.2)
        if k == 0:
            ax.set_ylabel("question $q$", fontsize=8, labelpad=3)
        if k == 1:
            ax.set_xlabel("written direction $d$", fontsize=8, labelpad=2)
    cax = f.add_axes(f5.rect(FW, FH, 1.55, 0.40, 2.4, 0.08), label="cbar")
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
    cb = f.colorbar(sm, cax=cax, orientation="horizontal")
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=2, width=0.5)
    cb.set_ticks([-0.4, -0.2, 0, 0.2, 0.4]); cb.set_ticklabels(["−0.4", "−0.2", "0", "0.2", "0.4"])
    cb.set_label(r"median $W_{q,d}$: change in $P(\mathrm{yes}\mid q)$ under the write of $d$", fontsize=7.5, labelpad=2)
    qa.run(f, "figure-08")
    d = style.save(f, 8, "figA1_write_structure")
    plt.close(f)
    print("wrote", d, f"(FH = {FH:.2f} in)")


if __name__ == "__main__":
    main()
