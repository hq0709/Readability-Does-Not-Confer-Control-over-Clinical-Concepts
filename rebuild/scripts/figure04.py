"""Figure 4 (fig3_example) redrawn from data/plot/figures/figure-04/all-bars-full.csv.

Changes against the original, per review:
  colours      by dataset as in Figure 2: concept write = dataset colour, competing write = its light tint, clean grey
  frame/grid   box frame kept, grid removed; one dashed guide at P(yes) = 0.5 (yes and no equally likely)
  subtitles    shortened to the finding
  numbers      the right-hand "0.02 -> 0.56 / 0.75" string is replaced by values written at the tips of the concept and
               competing bars in the highlighted row; the freed margin widens the bar panels
  legend       no frame (project rule); a fourth entry explains the highlighted row
  highlight    written concept's row: bold question name, band under the name; image captions state the concept is absent
Everything else follows scripts/plot_paper_figures.py::fig3_example.
The two photos are the ones embedded in the committed figures/fig3_example.pdf (extracted to rebuild/assets/figure-04/).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from PIL import Image

import style
import qa
from style import fs, plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.legend_handler import HandlerTuple
from matplotlib.patches import Rectangle

DATA = style.FIGDATA / "figure-04"
ASSETS = style.ROOT / "rebuild/assets/figure-04"
BAND = "#ECE8E2"                  # warm light grey: the written concept's row
def tint(c, w=0.5):
    return to_hex([x + (1 - x) * w for x in to_rgb(c)])


# colours follow the dataset, as in Figure 2 (NIH terracotta, COCO blue): the concept write in the dataset colour, the
# competing write in a light tint of it, the clean input in neutral grey
EX_COL = {ds: {"clean": "#9d9a95", "concept": fs.DATASET_COLOR[ds], "competitor": tint(fs.DATASET_COLOR[ds])}
          for ds in ("nih", "coco")}

EXAMPLES = [("nih", ASSETS / "0_I1.png", "NIH ChestX-ray14\nlabel: no finding (no effusion)",
             "(a)  chest radiograph: the Nodule write beats the Effusion write"),
            ("coco", ASSETS / "1_I2.png", "COCO val2017\nno dog in the image",
             "(b)  natural image: only the dog write moves the dog answer")]


def rect(fw, fh, x, y, w, h):
    return (x / fw, y / fh, w / fw, h / fh)


def main():
    fs.use_house_style()
    df = pd.read_csv(DATA / "all-bars-full.csv")
    FW, FH = fs.WIDTH, 3.66          # +0.13 in for the two-row legend
    f = plt.figure(figsize=(FW, FH))
    img_w, img_x = 1.02, 0.12; bar_x, bar_w = 1.96, 3.22; ax_h = 1.15
    row_y = [2.28, 0.76]; title_y = [3.49, 1.96]
    for r, (ds, path, desc, claim) in enumerate(EXAMPLES):
        g = df[df.dataset == ds]
        target, comp = g.target.iloc[0], g.competitor.iloc[0]
        concepts = list(dict.fromkeys(g.question))
        P = g.pivot(index="question", columns="condition", values="p_yes").loc[concepts]
        im = Image.open(path).convert("RGB"); iw, ih = im.size
        h_img = min(ax_h, img_w * ih / iw); w_img = h_img * iw / ih
        axi = f.add_axes(rect(FW, FH, img_x + (img_w - w_img) / 2, row_y[r] + ax_h - h_img, w_img, h_img), label=f"img{r}")
        axi.imshow(im, interpolation="lanczos"); axi.set_xticks([]); axi.set_yticks([]); axi.grid(False)
        for sp in axi.spines.values():
            sp.set_edgecolor("#8a8a8a"); sp.set_linewidth(0.6)
        f.text((img_x + img_w / 2) / FW, (row_y[r] + ax_h - h_img - 0.06) / FH, desc, ha="center", va="top", fontsize=7, color=fs.MUTED, linespacing=1.15)
        ax = f.add_axes(rect(FW, FH, bar_x, row_y[r], bar_w, ax_h), label=f"bars{r}")
        y = np.arange(len(concepts)); h = 0.27
        cols = {"clean": "clean", "concept": "concept_write", "competitor": "competitor_write"}
        vals = [P[cols[k]].to_numpy() for k in ("clean", "concept", "competitor")]
        for k, (v, key) in enumerate(zip(vals, ("clean", "concept", "competitor"))):
            ax.barh(y + (k - 1) * h, v, h, color=EX_COL[ds][key], edgecolor="none", zorder=3)
        jt = concepts.index(target)
        ax.set_yticks(y); ax.set_yticklabels(concepts, fontsize=7.5); ax.set_ylim(len(concepts) - 0.5, -0.5)
        # the written concept's question (absent from the image): bold tick label, band running under the label too
        ax.get_yticklabels()[jt].set_fontweight("bold")
        f.canvas.draw()
        lab = ax.get_yticklabels()[jt].get_window_extent(f.canvas.get_renderer()).transformed(ax.transAxes.inverted())
        x0 = lab.x0 - 0.015
        ax.add_patch(Rectangle((x0, jt - 0.47), 1 - x0, 0.94, transform=ax.get_yaxis_transform(), color=BAND,
                               zorder=0, clip_on=False))
        ax.set_xlim(0, 1); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.tick_params(axis="x", labelsize=7); ax.grid(False)
        ax.axvline(0.5, color=fs.CHANCE, ls="--", lw=0.7, zorder=1)          # yes and no equally likely
        if r == 1:
            ax.set_xlabel(r"$P(\mathrm{yes})$ to each question at $\alpha=+0.25$, Qwen2.5-VL-7B", fontsize=7.5)
        # values at the bar tips of the highlighted row: the concept label is nudged up (beside the near-zero clean bar),
        # the competitor label down (towards the gap under the row), so neither sits on another bar
        for k, key, dy in ((1, "concept", 1.6), (2, "competitor", -1.6)):
            v = vals[k][jt]
            ax.annotate(f"{v:.2f}", (v, jt + (k - 1) * h), xytext=(2.5, dy), textcoords="offset points", ha="left", va="center",
                        fontsize=6.8, color=fs.INK, annotation_clip=False, zorder=6)
        f.text(img_x / FW, title_y[r] / FH, claim, ha="left", va="bottom", fontsize=8.5, color=fs.INK)
    pair = lambda key: tuple(Rectangle((0, 0), 1, 1, color=EX_COL[ds][key]) for ds in ("nih", "coco"))
    handles = [Rectangle((0, 0), 1, 1, color=EX_COL["nih"]["clean"]), pair("concept"), pair("competitor"),
               Rectangle((0, 0), 1, 1, facecolor=BAND, edgecolor="#cfc9c1", lw=0.5)]
    labels = ["clean (no write)", "concept write (Effusion in a, dog in b)",
              "strongest competing write (Nodule in a, bottle in b)", "written concept, absent from the image"]
    f.legend(handles=handles, labels=labels, handler_map={tuple: HandlerTuple(ndivide=None, pad=0)}, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2, fontsize=6.8, frameon=False,
             handlelength=1.4, handleheight=0.8, columnspacing=2.0, handletextpad=0.5, borderpad=0.45, labelspacing=0.35)
    qa.run(f, "figure-04")
    d = style.save(f, 4, "fig3_example")
    plt.close(f)
    print("wrote", d)


if __name__ == "__main__":
    main()
