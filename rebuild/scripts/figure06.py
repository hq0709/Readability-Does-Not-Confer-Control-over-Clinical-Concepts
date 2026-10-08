"""Figure 6 (fig5_same_write) redrawn from data/plot/figures/figure-06/ownership-full.csv.

Same treatment as Figure 5 (see figure05.py):
  colour      project diverging map (style.DIVERGING), shared scale +-0.9 as Figure 5 (max |O| = 0.83 rounded up)
  numbers     short form (.16 / -.83), |O| >= 0.05, never bold
  owned mark  the dot is replaced by the small top-right corner triangle
  ceiling     hatching kept (it marks cells whose clean answer sits at a ceiling) but lighter and finer, so the values
              under it stay readable; explained in the key instead of the colour-bar label
  axes        colour-bar label shortened, round ticks; x-axis title "concept q"
Rows: Gemma 3 4B / 12B / 27B, a spacer, MedGemma 4B / 27B (same probes and write vectors within each family).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import style
import qa
import figure05 as f5
from style import fs, plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Polygon, Rectangle

DATA = style.FIGDATA / "figure-06"
DATASETS = ("nih", "chexpert", "coco")
FAM = [("gemma3-4", "Gemma 3 4B"), ("gemma3-12", "Gemma 3 12B"), ("gemma3-27", "Gemma 3 27B"),
       ("medgemma-4", "MedGemma 4B"), ("medgemma-27", "MedGemma 27B")]
FAM_GAP = 0.32                                  # extra white gap (cell units) between the Gemma 3 and MedGemma rows
YE = np.array([0, 1, 2, 3, 3 + FAM_GAP, 4 + FAM_GAP, 5 + FAM_GAP]); REAL = [0, 1, 2, 4, 5]   # row 3 is the spacer
HATCH, HATCH_COL, HATCH_LW = "///", "#B5AFA6", 0.45
CMAP = style.DIVERGING


class CeilingKey:
    pass


class HandlerCeiling(HandlerBase):
    """Legend key: a pale cell with the ceiling hatching."""
    def create_artists(self, legend, orig, x0, y0, width, height, fontsize, trans):
        s = 1.15 * fontsize
        x0, y0 = x0 + (width - s) / 2, y0 + (height - s) / 2 + 0.12 * fontsize
        return [Rectangle((x0, y0), s, s, facecolor=style.DIV_MID, edgecolor="none", transform=trans),
                Rectangle((x0, y0), s, s, fill=False, hatch=HATCH, edgecolor=HATCH_COL, lw=0, transform=trans)]


def main():
    fs.use_house_style()
    plt.rcParams["hatch.linewidth"] = HATCH_LW
    df = pd.read_csv(DATA / "ownership-full.csv")
    norm = TwoSlopeNorm(vmin=-0.9, vcenter=0.0, vmax=0.9)
    FW = fs.WIDTH; P = 1.36; gap = 0.20; x0 = 0.98; Ph = P * YE[-1] / 6
    FH = 0.22 + Ph + 0.36 + 0.16 + 0.62
    f = plt.figure(figsize=(FW, FH))
    cell_pt = P * 72 / 6
    e = f5.EAR_INSET / cell_pt
    g_in = (f5.GAP / 2) / cell_pt                 # half the white cell gap, in cell units
    for k, ds in enumerate(DATASETS):
        g = df[df.dataset == ds]
        concepts = list(dict.fromkeys(g.concept))
        ax = f.add_axes(f5.rect(FW, FH, x0 + k * (P + gap), FH - 0.22 - Ph, P, Ph), label=f"h{k}")
        M6 = np.full((6, len(concepts)), np.nan)
        for i, (mk, _) in zip(REAL, FAM):
            M6[i] = g[g.checkpoint_key == mk].set_index("concept").loc[concepts, "ownership"].to_numpy()
        ax.pcolormesh(np.arange(len(concepts) + 1), YE, np.ma.masked_invalid(M6), cmap=CMAP, norm=norm,
                      edgecolors="white", linewidth=f5.GAP, zorder=2)
        ax.set_xlim(0, len(concepts)); ax.set_ylim(YE[-1], 0); ax.set_aspect("equal")
        ax.grid(False); ax.tick_params(length=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_xticks(np.arange(len(concepts)) + 0.5)
        ax.set_xticklabels([style.SHORT_CONCEPT.get(c, c) for c in concepts], rotation=45, ha="right",
                           rotation_mode="anchor", fontsize=7.5)
        ax.set_yticks([(YE[i] + YE[i + 1]) / 2 for i in REAL])
        ax.set_yticklabels([lab for _, lab in FAM] if k == 0 else [""] * len(FAM), fontsize=7.5)
        for i, (mk, _) in zip(REAL, FAM):
            rows = g[g.checkpoint_key == mk].set_index("concept")
            y0, y1 = YE[i], YE[i + 1]
            for j, c in enumerate(concepts):
                v, own, ceil = rows.loc[c, "ownership"], bool(rows.loc[c, "owned"]), bool(rows.loc[c, "ceiling"])
                if ceil:
                    # inset by half the white gap so the hatching stays inside the coloured cell
                    ax.add_patch(Rectangle((j + g_in, y0 + g_in), 1 - 2 * g_in, y1 - y0 - 2 * g_in, fill=False, hatch=HATCH,
                                           edgecolor=HATCH_COL, lw=0, zorder=3))
                if own:
                    ax.add_patch(Polygon([(j + 1 - e - f5.EAR, y0 + e), (j + 1 - e, y0 + e), (j + 1 - e, y0 + e + f5.EAR)],
                                         closed=True, facecolor=fs.CHARCOAL, edgecolor="none", zorder=5))
                if abs(v) >= f5.ANNOT_MIN:
                    col = "white" if f5.lum(CMAP(norm(v))) < 0.5 else fs.INK
                    ax.text(j + 0.5, (y0 + y1) / 2, f5.short(v), ha="center", va="center", fontsize=f5.ANNOT_SIZE, color=col,
                            zorder=6)
        ax.set_title(f"({'abc'[k]})  {fs.DATASET_LABEL[ds]}", fontsize=8.5, pad=4)
        if k == 1:
            ax.set_xlabel("concept $q$", fontsize=8, labelpad=2)
    cax = f.add_axes(f5.rect(FW, FH, 0.95, 0.40, 2.3, 0.08), label="cbar")
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
    cb = f.colorbar(sm, cax=cax, orientation="horizontal")
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=2, width=0.5)
    cb.set_ticks([-0.8, -0.4, 0, 0.4, 0.8]); cb.set_ticklabels(["−0.8", "−0.4", "0", "0.4", "0.8"])
    cb.set_label(r"ownership $O_q$ of the shared write vector, by reader", fontsize=7.5, labelpad=2)
    f.legend(handles=[f5.OwnedKey(), CeilingKey()], labels=["owned concept", "clean answer at a ceiling"],
             handler_map={f5.OwnedKey: f5.HandlerOwned(), CeilingKey: HandlerCeiling()},
             loc="center left", bbox_to_anchor=(3.55 / FW, 0.44 / FH), fontsize=7.5, frameon=False,
             handlelength=1.3, handleheight=0.7, handletextpad=0.5, labelspacing=0.6)
    qa.run(f, "figure-06")
    d = style.save(f, 6, "fig5_same_write")
    plt.close(f)
    print("wrote", d, f"(FH = {FH:.2f} in)")


if __name__ == "__main__":
    main()
