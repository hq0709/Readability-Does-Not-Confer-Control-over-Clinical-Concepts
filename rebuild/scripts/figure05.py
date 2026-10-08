"""Figure 5 (fig4_write_matrices) redrawn from data/plot/figures/figure-05/write-matrices-full.csv.

Changes against the original, per review:
  cells       larger panels (the original left ~0.9 in unused on the right)
  numbers     short form (.19 / -.07) so neighbouring values no longer run together; threshold |v| >= 0.05 unchanged
  owned mark  no diagonal outlines and no bold values; an owned cell carries a small folded-corner triangle at its
              top-right (the original dot sat on the numbers)
  axes        x-axis title "written direction d" added; colour bar label shortened, round ticks, owned key beside it
  colour      project diverging map (style.DIVERGING): terracotta = positive, dusty blue = negative, lighter than the original
Values are read from the CSV unchanged.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import style
import qa
from style import fs, plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Polygon, Rectangle

DATA = style.FIGDATA / "figure-05"
PICKS = [("q25-7", "nih"), ("q25-72", "nih"), ("lingshu-32", "nih"), ("q25-7", "coco"), ("q3-32", "coco"), ("lingshu-32", "coco")]
NAMES = {"q25-7": "Qwen2.5-VL-7B", "q25-72": "Qwen2.5-VL-72B", "lingshu-32": "Lingshu 32B", "q3-32": "Qwen3-VL-32B"}
DS_SHORT = {"nih": "NIH", "coco": "COCO"}

CMAP = style.DIVERGING      # project diverging map (warm = positive, cool = negative)
GAP = 1.2                  # white gap between cells (pt)
ANNOT_MIN, ANNOT_SIZE = 0.05, 6.5
EAR = 0.26                 # owned mark: corner triangle, as a fraction of the cell side
EAR_INSET = 0.9            # pt, keeps the triangle inside the white gap


def lum(rgba):
    r, g, b = rgba[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def short(v):
    s = f"{abs(v):.2f}".lstrip("0")
    return ("−" if v < 0 else "") + s


def rect(fw, fh, x, y, w, h):
    return (x / fw, y / fh, w / fw, h / fh)


def draw_matrix(ax, concepts, W, owned, norm, cell_pt, ylabels):
    n = len(concepts)
    ax.pcolormesh(np.arange(n + 1), np.arange(n + 1), W, cmap=CMAP, norm=norm, edgecolors="white", linewidth=GAP, zorder=2)
    ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect("equal"); ax.grid(False); ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    lab = [style.SHORT_CONCEPT.get(c, c) for c in concepts]
    ax.set_xticks(np.arange(n) + 0.5); ax.set_yticks(np.arange(n) + 0.5)
    ax.set_xticklabels(lab, rotation=45, ha="right", rotation_mode="anchor", fontsize=7.5)
    ax.set_yticklabels(lab if ylabels else [""] * n, fontsize=7.5)
    e = EAR_INSET / cell_pt
    for i, c in enumerate(concepts):
        if c in owned:     # small folded-corner triangle at the top-right of the owned diagonal cell
            ax.add_patch(Polygon([(i + 1 - e - EAR, i + e), (i + 1 - e, i + e), (i + 1 - e, i + e + EAR)], closed=True,
                                 facecolor=fs.CHARCOAL, edgecolor="none", zorder=5))
        for j in range(n):
            v = W[i, j]
            if abs(v) < ANNOT_MIN:
                continue
            col = "white" if lum(CMAP(norm(v))) < 0.5 else fs.INK
            ax.text(j + 0.5, i + 0.5, short(v), ha="center", va="center", fontsize=ANNOT_SIZE, color=col, zorder=6)


class OwnedKey:
    pass


class HandlerOwned(HandlerBase):
    """Legend key: a pale cell with the owned corner triangle."""
    def create_artists(self, legend, orig, x0, y0, width, height, fontsize, trans):
        s = 1.15 * fontsize                     # a cell about one text line tall, centred on the label
        x0, y0 = x0 + (width - s) / 2, y0 + (height - s) / 2 + 0.12 * fontsize
        cell = Rectangle((x0, y0), s, s, facecolor=style.DIV_POS[0],
                         edgecolor="none", transform=trans)
        k = EAR * s
        ear = Polygon([(x0 + s - k, y0 + s), (x0 + s, y0 + s), (x0 + s, y0 + s - k)], closed=True,
                      facecolor=fs.CHARCOAL, edgecolor="none", transform=trans)
        return [cell, ear]


def main():
    fs.use_house_style()
    df = pd.read_csv(DATA / "write-matrices-full.csv")
    vlim = 0.9                                            # the original's symmetric limit (max |W| = 0.87, rounded up)
    norm = TwoSlopeNorm(vmin=-vlim, vcenter=0.0, vmax=vlim)
    FW = fs.WIDTH
    P, gap, x0 = 1.30, 0.22, 0.66                         # panel side, column gap, left margin (inches)
    title_h, xt_h, xl_h, row_gap, bar_h = 0.22, 0.36, 0.16, 0.10, 0.62
    FH = 2 * (title_h + P + xt_h + xl_h) + row_gap + bar_h
    rows_y = [FH - title_h - P, bar_h + xl_h + xt_h]
    f = plt.figure(figsize=(FW, FH))
    cell_pt = P * 72 / 6
    for k, (mk, ds) in enumerate(PICKS):
        g = df[(df.checkpoint_key == mk) & (df.dataset == ds)]
        concepts = list(dict.fromkeys(g.question))
        W = g.pivot(index="question", columns="written_direction", values="value").loc[concepts, concepts].to_numpy()
        owned = set(g[g.owned_diagonal].question)
        r, c = divmod(k, 3)
        ax = f.add_axes(rect(FW, FH, x0 + c * (P + gap), rows_y[r], P, P), label=f"m{k}")
        draw_matrix(ax, concepts, W, owned, norm, cell_pt, ylabels=(c == 0))
        ax.set_title(f"({'abcdef'[k]})  {NAMES[mk]}, {DS_SHORT[ds]}", fontsize=8.5, pad=4)
        if c == 0:
            ax.set_ylabel("question $q$", fontsize=8, labelpad=3)
        if c == 1:
            ax.set_xlabel("written direction $d$", fontsize=8, labelpad=2)
    # colour bar (left) and outline key (right) on one line
    cax = f.add_axes(rect(FW, FH, 0.95, 0.40, 2.3, 0.08), label="cbar")
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
    cb = f.colorbar(sm, cax=cax, orientation="horizontal")
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=2, width=0.5)
    cb.set_ticks([-0.8, -0.4, 0, 0.4, 0.8]); cb.set_ticklabels(["−0.8", "−0.4", "0", "0.4", "0.8"])
    cb.set_label(r"$W_{q,d}$: change in $P(\mathrm{yes}\mid q)$ under the write of $d$", fontsize=7.5, labelpad=2)
    f.legend(handles=[OwnedKey()], labels=["owned concept"], handler_map={OwnedKey: HandlerOwned()},
             loc="center left", bbox_to_anchor=(3.55 / FW, 0.44 / FH), fontsize=7.5, frameon=False,
             handlelength=1.3, handleheight=0.7, handletextpad=0.5)
    qa.run(f, "figure-05")
    d = style.save(f, 5, "fig4_write_matrices")
    plt.close(f)
    print("wrote", d, f"(FH = {FH:.2f} in)")


if __name__ == "__main__":
    main()
