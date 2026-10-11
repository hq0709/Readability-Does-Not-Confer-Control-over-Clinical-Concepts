"""Candidate: the write flow and the median write matrix as one figure.

Figure 7 and Figure A1 display the same quantity. Figure 7 draws the mean over checkpoints of
max(W_{q,d}, 0) as flow; Figure A1 draws the cell-wise median of W_{q,d} as a heat map; A1's own
caption says Figure 7 reads the same matrices as flow. Two figures, one aggregate, two encodings.

This candidate puts them in one figure: the flow states the share that lands on the named question,
the matrix underneath says which cells that share comes from. The appendix then carries one figure
fewer. The alternative is to keep only one of the two, for which the separate candidates
fig7-A-flow and figA1-A-median are the rendered versions.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt

import aclsize
from aclsize import fs
import style
import qa

import figure03 as FLOW
import figure05 as F5
import figure08 as MED

K = aclsize.K
DATASETS = ("nih", "chexpert", "coco")


def median_panel(f, FW, FH, x, y, P, ds, df, norm, letter, ylabels, xlabel):
    g = df[df.dataset == ds]
    concepts = list(dict.fromkeys(g.question)); n = len(concepts)
    W = g.pivot(index="question", columns="written_direction", values="value").loc[concepts, concepts].to_numpy()
    ax = f.add_axes(F5.rect(FW, FH, x, y, P, P), label=f"med{letter}")
    ax.pcolormesh(np.arange(n + 1), np.arange(n + 1), W, cmap=MED.CMAP, norm=norm,
                  edgecolors="white", linewidth=F5.GAP, zorder=2)
    ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect("equal"); ax.grid(False); ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    lab = [style.SHORT_CONCEPT.get(c, c) for c in concepts]
    ax.set_xticks(np.arange(n) + 0.5); ax.set_yticks(np.arange(n) + 0.5)
    ax.set_xticklabels(lab, rotation=45, ha="right", rotation_mode="anchor", fontsize=7)
    ax.set_yticklabels(lab if ylabels else [""] * n, fontsize=7)
    for i in range(n):
        for j in range(n):
            v = W[i, j]
            col = "white" if F5.lum(MED.CMAP(norm(v))) < 0.5 else fs.INK
            ax.text(j + 0.5, i + 0.5, MED.short0(v), ha="center", va="center",
                    fontsize=F5.ANNOT_SIZE, color=col, zorder=6)
    ax.set_title(f"({letter})  median $W_{{q,d}}$", fontsize=8, pad=4)
    if ylabels:
        ax.set_ylabel("question $q$", fontsize=8, labelpad=3)
    if xlabel:
        ax.set_xlabel("written direction $d$", fontsize=8, labelpad=2)
    return ax


def main():
    aclsize.use()
    fs.use_house_style()                       # the flow draws no axes; the axis overrides do not apply to it
    FW = fs.WIDTH
    flow_h, mat_P, mat_gap, mat_x0 = 2.20 * K, 1.25 * K, 0.45 * K, 0.60 * K
    note_h, mat_title, mat_xt, mat_xl, bar_h = 0.34, 0.26, 0.42, 0.20, 0.62
    FH = 0.44 + flow_h + note_h + mat_title + mat_P + mat_xt + mat_xl + bar_h
    f = plt.figure(figsize=(FW, FH))

    # (a)-(c): the flow, at the top
    FLOW.flow_panels(f, FW, FH, y0=FH - 0.30 - flow_h, PH=flow_h, PW=1.72 * K, xl=0.10 * K, letters="abc")
    f.text(0.5, (FH - 0.30 - flow_h - 0.22) / FH,
           "colored: the write lands on the question it names;   gray: it lands on another question",
           ha="center", va="center", fontsize=7, color=fs.INK)

    # (d)-(f): the same aggregate as a matrix, underneath
    df = pd.read_csv(MED.DATA / "median-write-matrices-full.csv")
    norm = TwoSlopeNorm(vmin=-MED.VLIM, vcenter=0.0, vmax=MED.VLIM)
    y = bar_h + mat_xl + mat_xt
    for k, ds in enumerate(DATASETS):
        median_panel(f, FW, FH, mat_x0 + k * (mat_P + mat_gap), y, mat_P, ds, df, norm,
                     "def"[k], ylabels=(k == 0), xlabel=(k == 1))

    cax = f.add_axes(F5.rect(FW, FH, 1.55 * K, 0.40 * K, 2.4 * K, 0.08 * K), label="cbar")
    cb = f.colorbar(plt.cm.ScalarMappable(cmap=MED.CMAP, norm=norm), cax=cax, orientation="horizontal")
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=2, width=0.5)
    cb.set_ticks([-0.4, -0.2, 0, 0.2, 0.4]); cb.set_ticklabels(["−0.4", "−0.2", "0", "0.2", "0.4"])
    cb.set_label(r"median $W_{q,d}$ over checkpoints", fontsize=7.5, labelpad=2)

    qa.run(f, "fig7A1-merge")
    aclsize.save(f, "fig7A1-M-merged",
                 rows=[["flow0", "flow1", "flow2"], ["medd", "mede", "medf"]],
                 exclude=("cbar",))
    plt.close(f)


if __name__ == "__main__":
    main()
