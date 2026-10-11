"""New designs for the overview figure. Different encodings, not a re-layout of the present one.

The present Figure 2 is bars + scatter + dose curve + cumulative rank. Two of those -- the cumulative
rank of the own direction among its 119 rivals, and the per-model landscape -- state the same thing
the ownership grade already states, in another encoding. These candidates replace the set with three
panels that each do a different job, and give the decisive one the hero position.

  D  decision plane: every cell as own-write effect against its strongest rival, the diagonal as the
     ownership boundary; then the grade funnel; then the dose response.
  E  unit grid: the 450 cells themselves, one square each, coloured by the highest grade reached;
     then the margin distribution as a raincloud; then the dose response.

Both read the per-cell export written by export_cells.py through the paper's own inclusion rule.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

import aclsize
from aclsize import fs
import style
import qa
import figure02 as F

DATA = __import__("pathlib").Path(__file__).resolve().parent / "data"
DATASETS = ("nih", "chexpert", "coco")
COL, MK, LAB = fs.DATASET_COLOR, fs.DATASET_MARKER, fs.DATASET_LABEL
SHORT = {"nih": "NIH", "chexpert": "CheXpert", "coco": "COCO"}
LIN = 0.05                      # symlog linear zone: below the effect floor the paper calls meaningful


def _symlog(ax):
    """Both axes on the same symmetric log, so the ownership boundary stays the 45 degree diagonal."""
    for setter in (ax.set_xscale, ax.set_yscale):
        setter("symlog", linthresh=LIN, linscale=0.45)
    t = [-0.5, -0.1, 0, 0.1, 0.5]
    lab = ["−.5", "−.1", "0", ".1", ".5"]
    ax.set_xticks(t); ax.set_xticklabels(lab); ax.set_yticks(t); ax.set_yticklabels(lab)
    ax.set_xlim(-0.95, 0.95); ax.set_ylim(-0.95, 0.95)


def decision_plane(ax, d, legend_in_panel=True):
    """Hero: one point per scored cell. Above the diagonal the concept's own write moves its own
    answer more than any rival write; below it, a rival moves it more."""
    lo, hi = -0.95, 0.95
    ax.add_patch(Polygon([(lo, lo), (hi, lo), (hi, hi)], closed=True, facecolor="#F2EFEA",
                         edgecolor="none", zorder=0))                     # a rival wins
    ax.plot([lo, hi], [lo, hi], color=fs.MUTED, lw=0.8, ls="-", zorder=2)
    ax.axhline(0, color=fs.CHANCE, lw=0.6, ls=":", zorder=1)
    ax.axvline(0, color=fs.CHANCE, lw=0.6, ls=":", zorder=1)
    for ds in DATASETS:
        g = d[d.dataset == ds]
        ax.plot(g.max_other, g.W_qq, ls="none", marker=MK[ds], ms=3.8, mfc=COL[ds],
                mec="white", mew=0.45, alpha=0.82, zorder=4 if ds == "coco" else 3)
    _symlog(ax)
    ax.text(0.03, 0.965, "the concept's own write wins", transform=ax.transAxes, ha="left", va="top",
            fontsize=7, color=fs.MUTED, style="italic")
    ax.text(0.97, 0.035, "a rival write wins", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7, color=fs.MUTED, style="italic")
    ax.set_xlabel("strongest rival write, change in $P(\\mathrm{yes})$")
    ax.set_ylabel("own write, change in $P(\\mathrm{yes})$")
    if legend_in_panel:
        share = {ds: (d[d.dataset == ds].W_qq > d[d.dataset == ds].max_other).mean() for ds in DATASETS}
        ax.text(0.045, 0.875, "share above the line", transform=ax.transAxes, ha="left",
                va="center", fontsize=7, color=fs.MUTED)
        for k, ds in enumerate(("coco", "chexpert", "nih")):
            y = 0.805 - k * 0.072
            ax.plot(0.062, y + 0.004, transform=ax.transAxes, marker=MK[ds], ms=4.6, mfc=COL[ds],
                    mec="white", mew=0.5, clip_on=False)
            ax.text(0.105, y, f"{SHORT[ds]}  {100 * share[ds]:.0f}%", transform=ax.transAxes,
                    ha="left", va="center", fontsize=7, color=fs.INK)
    fs.panel_title(ax, "a", "every cell against its strongest rival")


def funnel(ax, g):
    """The three grades as one line per dataset: reading and answering hold, ownership falls away."""
    grades = ("readable", "answerable", "owned")
    x = np.arange(3)
    for ds in DATASETS:
        v = [int(g[(g.dataset == ds) & (g.grade == q)].numerator.iloc[0]) for q in grades]
        ax.plot(x, v, color=COL[ds], lw=1.6, marker=MK[ds], ms=5, mec="white", mew=0.7, zorder=3)
        ax.annotate(f"{v[-1]}", (x[-1], v[-1]), xytext=(4, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=7, color=COL[ds], zorder=5)
    ax.set_xticks(x, ["read", "answer", "own"])
    ax.set_xlim(-0.25, 2.55); ax.set_ylim(0, 158)
    ax.set_yticks([0, 50, 100, 150])
    ax.set_ylabel("cells (of 150)")
    ax.tick_params(axis="x", length=0)
    fs.panel_title(ax, "b", "where the grade is lost")


def raincloud(ax, d):
    """The signed margin over the best rival, as a distribution per dataset: the boundary is zero."""
    ax.axvline(0, color=fs.MUTED, lw=0.8, zorder=2)
    rng = np.random.default_rng(0)
    for k, ds in enumerate(("coco", "chexpert", "nih")):
        v = d[d.dataset == ds].O_q.to_numpy()
        kde = np.histogram(np.clip(v, -0.6, 0.9), bins=34, range=(-0.6, 0.9), density=True)
        edges = kde[1][:-1] + np.diff(kde[1]) / 2
        h = 0.34 * kde[0] / kde[0].max()
        ax.fill_between(edges, k + 0.08, k + 0.08 + h, color=COL[ds], alpha=0.55, lw=0, zorder=3)
        ax.plot(np.clip(v, -0.6, 0.9), k - 0.13 + rng.uniform(-0.055, 0.055, v.size), ls="none",
                marker="o", ms=1.9, mfc=COL[ds], mec="none", alpha=0.75, zorder=4)
        ax.plot(np.median(v), k - 0.13, marker="|", ms=8, color=fs.INK, mew=1.1, zorder=6)
    ax.set_yticks(range(3), [SHORT[ds] for ds in ("coco", "chexpert", "nih")])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.45, 2.55); ax.set_xlim(-0.62, 0.92)
    ax.set_xlabel("margin over the best rival, $O_q$")
    fs.panel_title(ax, "b", "how far from the boundary")


def unit_grid(ax, d):
    """The 450 cells themselves: one square per cell, darkest where the write also owns the concept."""
    tiers = [("owned", "#A9503F"), ("answerable", "#DCC6B4"), ("readable", "#EFE7DD"), ("none", "#F4F1EC")]
    order = {t: i for i, (t, _) in enumerate(tiers)}
    cols, rows_n = 15, 10
    for b, ds in enumerate(DATASETS):
        g = d[d.dataset == ds].copy()
        g["tier"] = np.where(g.owned, "owned",
                     np.where(g.answer_capable.fillna(False), "answerable",
                     np.where(g.readable.fillna(False), "readable", "none")))
        g = g.sort_values("tier", key=lambda s: s.map(order))
        x0 = b * (cols + 3)
        for i, t in enumerate(g.tier.to_numpy()):
            c, r = divmod(i, rows_n)
            ax.add_patch(plt.Rectangle((x0 + c + 0.08, r + 0.08), 0.84, 0.84,
                                       facecolor=dict(tiers)[t], edgecolor="none"))
        n_own = int((g.tier == "owned").sum())
        ax.text(x0 + cols / 2, -0.9, f"{SHORT[ds]}\n{n_own} owned", ha="center", va="top",
                fontsize=7.5, color=fs.INK, linespacing=1.25)
    # the key is drawn in data coordinates: with aspect("equal") the axes box is taller than the
    # squares, so a legend anchored to the axes lands on the first row of the grid
    top = rows_n + 2.9
    ax.set_xlim(-0.5, 3 * (cols + 3) - 2.5); ax.set_ylim(-3.6, top)
    ax.set_aspect("equal"); ax.axis("off")
    kx = 0.0
    for name, col in [("owned", tiers[0][1]), ("answerable", tiers[1][1]),
                      ("readable only", tiers[2][1]), ("neither", tiers[3][1])]:
        ax.add_patch(plt.Rectangle((kx, top - 1.75), 0.9, 0.9, facecolor=col, edgecolor="none"))
        ax.text(kx + 1.25, top - 1.30, name, ha="left", va="center", fontsize=7, color=fs.INK)
        kx += 1.25 + 0.42 * len(name) + 1.5
    ax.set_title("(a)  450 scored cells, one square each", fontsize=9, pad=6)


def _load():
    return pd.read_csv(DATA / "cells.csv"), pd.read_csv(DATA / "grades.csv")


def cand_D():
    d, g = _load()
    aclsize.use()
    f = plt.figure(figsize=(fs.WIDTH, 3.85), layout="constrained")
    f.get_layout_engine().set(w_pad=0.05, h_pad=0.05, wspace=0.06, hspace=0.10)
    gs = f.add_gridspec(2, 2, width_ratios=[1.52, 1.0])
    ax_a = f.add_subplot(gs[:, 0]); ax_b = f.add_subplot(gs[0, 1]); ax_c = f.add_subplot(gs[1, 1])
    decision_plane(ax_a, d)
    funnel(ax_b, g)
    F.panel_c(ax_c)
    ax_c.set_title("(c)  dose response", fontsize=9, pad=5)
    ax_c.set_xlabel(r"steering strength $\alpha$"); ax_c.set_ylabel("ownership $O$")
    qa.run(f, "fig2-D")
    aclsize.save(f, "fig2-D-decision"); plt.close(f)


def cand_E():
    d, g = _load()
    aclsize.use()
    f = plt.figure(figsize=(fs.WIDTH, 4.15), layout="constrained")
    f.get_layout_engine().set(w_pad=0.05, h_pad=0.05, wspace=0.08, hspace=0.16)
    gs = f.add_gridspec(2, 2, height_ratios=[1.0, 1.05])
    ax_a = f.add_subplot(gs[0, :]); ax_b = f.add_subplot(gs[1, 0]); ax_c = f.add_subplot(gs[1, 1])
    unit_grid(ax_a, d)
    raincloud(ax_b, d)
    F.panel_c(ax_c)
    ax_c.set_title("(c)  dose response", fontsize=9, pad=5)
    ax_c.set_xlabel(r"steering strength $\alpha$"); ax_c.set_ylabel("ownership $O$")
    qa.run(f, "fig2-E")
    aclsize.save(f, "fig2-E-units",
                 exemptions=[{"panels": ["a"], "checks": ["column"],
                              "reason": "the unit grid is drawn with equal aspect so that its 450 "
                                        "squares stay square; its axes box is therefore set by the "
                                        "aspect ratio and cannot share an edge with a free panel"}])
    plt.close(f)


if __name__ == "__main__":
    cand_D(); cand_E()
