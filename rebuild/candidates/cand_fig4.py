"""Figure 4 candidates: the write matrices at the real ACL width.

The figure's claim is a contrast: on COCO the own direction lights the diagonal, on chest it does not.
A two-row grid states that contrast column by column, so a column should hold one checkpoint on both
datasets. In the present grid the middle column does not: Qwen2.5-VL-72B (chest) sits above
Qwen3-VL-32B (COCO), and only the first and third columns are the same checkpoint twice. The export
has both datasets for exactly two checkpoints.

  A  the same six matrices, re-authored at 6.32 in; the cells grow with the canvas
  B  the two checkpoints measured on both datasets, paired column by column, at larger cell size
"""
from __future__ import annotations

import pandas as pd
from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt

import aclsize
from aclsize import fs
import qa
import figure05 as F

K = aclsize.K
VLIM = 0.9                                     # the original symmetric limit, kept so colours are comparable


def _matrix(ax, g, concepts, norm, cell_pt, ylabels):
    W = g.pivot(index="question", columns="written_direction", values="value").loc[concepts, concepts].to_numpy()
    owned = set(g[g.owned_diagonal].question)
    F.draw_matrix(ax, concepts, W, owned, norm, cell_pt, ylabels=ylabels)


def _colorbar(f, FW, FH, x, y, w, h, legend_x, legend_y):
    norm = TwoSlopeNorm(vmin=-VLIM, vcenter=0.0, vmax=VLIM)
    cax = f.add_axes(F.rect(FW, FH, x, y, w, h), label="cbar")
    cb = f.colorbar(plt.cm.ScalarMappable(cmap=F.CMAP, norm=norm), cax=cax, orientation="horizontal")
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=2, width=0.5)
    cb.set_ticks([-0.8, -0.4, 0, 0.4, 0.8]); cb.set_ticklabels(["−0.8", "−0.4", "0", "0.4", "0.8"])
    cb.set_label(r"$W_{q,d}$: change in $P(\mathrm{yes}\mid q)$ under the write of $d$", fontsize=7.5, labelpad=2)
    f.legend(handles=[F.OwnedKey()], labels=["owned concept"], handler_map={F.OwnedKey: F.HandlerOwned()},
             loc="center left", bbox_to_anchor=(legend_x / FW, legend_y / FH), fontsize=7.5, frameon=False,
             handlelength=1.3, handleheight=0.7, handletextpad=0.5)
    return norm


def cand_A():
    """Same six matrices and same composition, every inch of the layout scaled to the real width."""
    aclsize.use()
    df = pd.read_csv(F.DATA / "write-matrices-full.csv")
    FW = fs.WIDTH
    P, gap, x0 = 1.30 * K, 0.22 * K, 0.66 * K
    title_h, xt_h, xl_h, row_gap, bar_h = (v * K for v in (0.22, 0.36, 0.16, 0.10, 0.62))
    FH = 2 * (title_h + P + xt_h + xl_h) + row_gap + bar_h
    rows_y = [FH - title_h - P, bar_h + xl_h + xt_h]
    f = plt.figure(figsize=(FW, FH))
    norm = TwoSlopeNorm(vmin=-VLIM, vcenter=0.0, vmax=VLIM)
    cell_pt = P * 72 / 6
    for k, (mk, ds) in enumerate(F.PICKS):
        g = df[(df.checkpoint_key == mk) & (df.dataset == ds)]
        concepts = list(dict.fromkeys(g.question))
        r, c = divmod(k, 3)
        ax = f.add_axes(F.rect(FW, FH, x0 + c * (P + gap), rows_y[r], P, P), label=f"m{k}")
        _matrix(ax, g, concepts, norm, cell_pt, ylabels=(c == 0))
        ax.set_title(f"({'abcdef'[k]})  {F.NAMES[mk]}, {F.DS_SHORT[ds]}", fontsize=8.5, pad=4)
        if c == 0:
            ax.set_ylabel("question $q$", fontsize=8, labelpad=3)
        if c == 1:
            ax.set_xlabel("written direction $d$", fontsize=8, labelpad=2)
    _colorbar(f, FW, FH, 0.95 * K, 0.40 * K, 2.3 * K, 0.08 * K, 3.55 * K, 0.44 * K)
    qa.run(f, "fig4-A")
    aclsize.save(f, "fig4-A-six", rows=[["m0", "m1", "m2"], ["m3", "m4", "m5"]],
                 cols=[["m0", "m3"], ["m1", "m4"], ["m2", "m5"]], exclude=("cbar",))
    plt.close(f)


def cand_B():
    """Paired and adjacent: the same checkpoint on chest then COCO, so the contrast is one glance wide.

    A 2x2 square grid of these matrices is 6.7 in tall at the ACL width, two thirds of a page. One row
    of four is 3 in and puts each pair side by side, which is the comparison the figure is making.
    """
    aclsize.use()
    df = pd.read_csv(F.DATA / "write-matrices-full.csv")
    pairs = ["q25-7", "lingshu-32"]                     # the checkpoints the export carries on both datasets
    order = [(mk, ds) for mk in pairs for ds in ("nih", "coco")]
    FW = fs.WIDTH
    P, gap, pair_gap, x0 = 1.24, 0.16, 0.42, 0.62
    # measured from the render: the rotated tick labels take 0.46 in below the panel and the axis title
    # another 0.18, so the bar sits 0.10 under that rather than under a nominal row gap.
    title_h, xt_h, xl_h, row_gap, bar_h = 0.26, 0.46, 0.18, 0.10, 0.58
    FH = title_h + P + xt_h + xl_h + row_gap + bar_h
    y = FH - title_h - P
    f = plt.figure(figsize=(FW, FH))
    norm = TwoSlopeNorm(vmin=-VLIM, vcenter=0.0, vmax=VLIM)
    cell_pt = P * 72 / 6
    x = x0
    for k, (mk, ds) in enumerate(order):
        g = df[(df.checkpoint_key == mk) & (df.dataset == ds)]
        concepts = list(dict.fromkeys(g.question))
        ax = f.add_axes(F.rect(FW, FH, x, y, P, P), label=f"p{k}")
        _matrix(ax, g, concepts, norm, cell_pt, ylabels=(k == 0))
        ax.set_title(f"({'abcd'[k]})  {F.NAMES[mk]}, {F.DS_SHORT[ds]}", fontsize=8, pad=4)
        if k == 0:
            ax.set_ylabel("question $q$", fontsize=8, labelpad=3)
        if k == 1:
            ax.set_xlabel("written direction $d$", fontsize=8, labelpad=2)
        x += P + (pair_gap if k % 2 == 1 else gap)      # wider gap between the two checkpoint pairs
    _colorbar(f, FW, FH, 1.30, 0.38, 2.5, 0.09, 4.20, 0.42)
    qa.run(f, "fig4-B")
    aclsize.save(f, "fig4-B-paired", rows=[["p0", "p1", "p2", "p3"]], exclude=("cbar",),
                 exemptions=[{"panels": ["p0", "p1", "p2", "p3"], "checks": ["horizontal-gutter"],
                              "reason": "the gap between the two checkpoint pairs is deliberately "
                                        "wider than the gap inside a pair, so that the chest/COCO "
                                        "contrast reads as two pairs and not as four panels"}])
    plt.close(f)


if __name__ == "__main__":
    cand_A(); cand_B()
