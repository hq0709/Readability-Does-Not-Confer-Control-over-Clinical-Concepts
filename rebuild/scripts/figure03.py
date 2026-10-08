"""Figure 3 (fig7_write_flow) redrawn from data/plot/figures/figure-03/positive-flow-full.csv.

Only change against the original: colours. Concept bands and write-side bars use style.CONCEPT_COLOR (the project's
softened palette); everything else -- geometry, band ordering, labels, titles, footnote -- follows
scripts/plot_paper_figures.py::flow_panels / fig7_write_flow line for line.
P[q, d] = mean over checkpoints of max(W_qd, 0) is read from the CSV, not recomputed.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import style
import qa
from style import fs, plt
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MPath

DATA = style.FIGDATA / "figure-03"
DATASETS = ("nih", "chexpert", "coco")
OFF_GREY = "#c9c6c0"          # bands that land on another question (unchanged: warm neutral)


def rect(fw, fh, x, y, w, h):
    return (x / fw, y / fh, w / fw, h / fh)


def repel(ys, step, lo, hi, iters=200):
    ys = np.array(ys, float); order = np.argsort(ys); y = ys[order].copy()
    for _ in range(iters):
        moved = False
        for a in range(len(y) - 1):
            gap = y[a + 1] - y[a]
            if gap < step - 1e-9:
                d = (step - gap) / 2; y[a] -= d; y[a + 1] += d; moved = True
        y = np.clip(y, lo, hi)
        if not moved:
            break
    out = np.empty_like(y); out[order] = y
    return out


def load(ds, df):
    g = df[df.dataset == ds]
    concepts = list(dict.fromkeys(g.question))
    Pm = g.pivot(index="question", columns="written_direction", values="value").loc[concepts, concepts].to_numpy()
    return concepts, Pm


def flow_panels(f, FW, FH, y0, PH, PW, xl, letters):
    df = pd.read_csv(DATA / "positive-flow-full.csv")
    BAR_W_IN, GAP_FRAC = 0.05, 0.04
    pgap = (FW - 2 * xl - 3 * PW) / 2
    for k, ds in enumerate(DATASETS):
        concepts, Pm = load(ds, df); n = len(concepts)
        total = float(Pm.sum()); own_share = float(np.trace(Pm) / total)
        ax = f.add_axes(rect(FW, FH, xl + k * (PW + pgap), y0, PW, PH), label=f"flow{k}")
        ax.set_xlim(-0.45, 1.45); ax.set_ylim(-0.11, 1.09); ax.set_axis_off(); ax.grid(False)
        bar_w = BAR_W_IN / (PW / 1.9)
        usable = 1.0 - GAP_FRAC * (n - 1)
        out_h = {c: usable * Pm[:, j_].sum() / total for j_, c in enumerate(concepts)}
        in_h = {c: usable * Pm[i_, :].sum() / total for i_, c in enumerate(concepts)}
        left, right, yt = {}, {}, 1.0
        for c in concepts:
            left[c] = (yt - out_h[c], yt); yt = yt - out_h[c] - GAP_FRAC
        yt = 1.0
        for c in concepts:
            right[c] = (yt - in_h[c], yt); yt = yt - in_h[c] - GAP_FRAC
        lcur = {c: left[c][1] for c in concepts}; rcur = {c: right[c][1] for c in concepts}
        bands = []
        for j_, d in enumerate(concepts):
            for i_, q in enumerate(concepts):
                w = usable * Pm[i_, j_] / total
                if w <= 0:
                    continue
                yl1, yl0 = lcur[d], lcur[d] - w; lcur[d] = yl0
                bands.append((d, q, yl0, yl1))
        rb = {}
        for j_, d in enumerate(concepts):
            for i_, q in enumerate(concepts):
                w = usable * Pm[i_, j_] / total
                if w <= 0:
                    continue
                yr1, yr0 = rcur[q], rcur[q] - w; rcur[q] = yr0
                rb[(d, q)] = (yr0, yr1)
        for d, q, yl0, yl1 in bands:
            yr0, yr1 = rb[(d, q)]
            verts = [(0, yl1), (0.5, yl1), (0.5, yr1), (1, yr1), (1, yr0), (0.5, yr0), (0.5, yl0), (0, yl0), (0, yl1)]
            codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
            own = d == q
            ax.add_patch(PathPatch(MPath(verts, codes), facecolor=style.CONCEPT_COLOR[d] if own else OFF_GREY, edgecolor="none",
                                   alpha=0.9 if own else 0.75, zorder=3 if own else 2))
        for c in concepts:
            ax.add_patch(Rectangle((-bar_w, left[c][0]), bar_w, left[c][1] - left[c][0], facecolor=style.CONCEPT_COLOR[c], edgecolor="none", zorder=4))
            ax.add_patch(Rectangle((1, right[c][0]), bar_w, right[c][1] - right[c][0], facecolor=fs.CHARCOAL, edgecolor="none", zorder=4))
        step = 9.0 / (PH * 72 / 1.11)
        for side, spans, x, ha in (("L", left, -bar_w - 0.05, "right"), ("R", right, 1 + bar_w + 0.05, "left")):
            cs = list(concepts); ys = [(spans[c][0] + spans[c][1]) / 2 for c in cs]
            ly = repel(ys, step, 0.0, 1.0)
            for c, y_, y_lab in zip(cs, ys, ly):
                ax.text(x, y_lab, style.SHORT_CONCEPT.get(c, c), ha=ha, va="center", fontsize=7, color=fs.INK)
        ax.text(0.5, -0.075, f"own-question share of the write: {100 * own_share:.0f}%", ha="center", va="center", fontsize=7.5, color=fs.INK)
        ax.text(-bar_w / 2, 1.025, "write $d$", ha="center", va="bottom", fontsize=7, color=fs.MUTED)
        ax.text(1 + bar_w / 2, 1.025, "question $q$", ha="center", va="bottom", fontsize=7, color=fs.MUTED)
        ax.set_title(f"({letters[k]})  {fs.DATASET_LABEL[ds].replace(' (control)', '')}\nwhere the write goes", fontsize=8, pad=3, linespacing=1.2)


def main():
    fs.use_house_style()          # no axes are drawn here, so the Nature-style axis overrides do not apply
    FW, FH = fs.WIDTH, 3.30
    f = plt.figure(figsize=(FW, FH))
    flow_panels(f, FW, FH, y0=0.44, PH=2.20, PW=1.72, xl=0.10, letters="abc")
    f.text(0.5, 0.17 / FH, "coloured: the write lands on the question it names;   grey: it lands on another question",
           ha="center", va="center", fontsize=7, color=fs.INK)
    qa.run(f, "figure-03")
    d = style.save(f, 3, "fig7_write_flow")
    plt.close(f)
    print("wrote", d)


if __name__ == "__main__":
    main()
