"""Figure 6, reshaped: the panels were wide and short because the legend took the bottom third.

Three rows of legend under the panels left each ladder about 1.3 in of height against 2.1 in of
width, so a ladder with three or four sizes was stretched flat and the figure read as one long
strip. Moving the key into a fourth slot at the right gives the panels the whole height, and they
turn portrait, which is the shape a ladder wants.

  C  portrait panels, key at the right, one y scale per panel
  D  the same, with one y scale across all three, so the panels can be compared
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

import aclsize
from aclsize import fs
import style
import qa
import figure07 as F

SHARED_LO, SHARED_HI, SHARED_STEP = -0.6, 0.6, 0.3


def fit_shared(ax, _v):
    pad = 0.04 * (SHARED_HI - SHARED_LO)
    ax.set_ylim(SHARED_LO - pad, SHARED_HI + pad)
    ax.set_yticks(np.round(np.arange(SHARED_LO, SHARED_HI + SHARED_STEP / 2, SHARED_STEP), 2))
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda v, _: "0" if abs(v) < 1e-9 else ("−" if v < 0 else "") + f"{abs(v):.1f}".lstrip("0")))


def ladder(ax, df, title, sizes, ds, letter, fit, yticklabels=True):
    g = df[df.dataset == ds]
    keys = [m for m, _ in sizes]
    xs = g.drop_duplicates("checkpoint_key").set_index("checkpoint_key").loc[keys, "size_b"].to_numpy(float)
    concepts = list(dict.fromkeys(g.concept))
    emph = g[g.checkpoint_key == keys[-1]].set_index("concept").ownership.idxmax()
    ax.axhline(0, color=fs.CHANCE, ls="--", lw=0.7, zorder=1)
    for c in sorted(concepts, key=lambda c: c == emph):      # the emphasised series is drawn last
        rows = g[g.concept == c].set_index("checkpoint_key").loc[keys]
        col = style.CONCEPT_COLOR[c]; e = c == emph
        ax.plot(xs, rows.ownership, color=col, lw=F.LW_EMPH if e else F.LW, ls="-" if e else F.DASH,
                zorder=4 if e else 3, solid_capstyle="round")
        for x, y, o in zip(xs, rows.ownership, rows.owned):
            ax.plot(x, y, marker=F.MARKER[c], ms=F.MS + (0.9 if e else 0), mec=col, mew=1.1,
                    mfc=col if o else "white", ls="none", zorder=6 if e else 5)
    ax.set_xscale("log", base=2)
    pad = F.PAD_FRAC * np.log2(xs[-1] / xs[0])
    ax.set_xlim(xs[0] / 2 ** pad, xs[-1] * 2 ** pad)
    ax.set_xticks(xs, [l for _, l in sizes]); ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.set_title(f"({letter})  {title}", fontsize=8.5, pad=5)
    fit(ax, g[g.checkpoint_key.isin(keys)].ownership)
    if not yticklabels:
        ax.set_yticklabels([])
    return emph


def key_panel(ax):
    """A legend in its own slot: twelve entries in one column, which the bottom strip needed three rows for."""
    ax.axis("off")
    grey = fs.MUTED
    conc = [Line2D([], [], ls="none", marker=F.MARKER[c], ms=F.MS + 0.5, mfc=style.CONCEPT_COLOR[c],
                   mec=style.CONCEPT_COLOR[c], label=c) for c in F.ORDER]
    enc = [Line2D([], [], ls="none", marker="o", ms=F.MS, mfc=grey, mec=grey, label="owned"),
           Line2D([], [], ls="none", marker="o", ms=F.MS, mfc="white", mec=grey, mew=0.9, label="not owned"),
           Line2D([], [], color=grey, lw=F.LW_EMPH, label="largest $O_q$"),
           Line2D([], [], color=grey, lw=F.LW, ls=F.DASH, label="other concepts")]
    leg = ax.legend(handles=conc + enc, loc="center left", bbox_to_anchor=(-0.06, 0.52),
                    fontsize=7.5, frameon=False, handlelength=1.9, handletextpad=0.55,
                    labelspacing=0.52, borderpad=0.0)
    # the thick-line entry wraps onto two lines; the caller sets the text once the legend exists
    return leg, leg.get_texts()[-2]


def build(name, fit, shared_axis):
    """Explicit equal panel widths rather than constrained layout.

    The engine gives each panel the slot its own y-tick labels need, so the three plot areas end up
    different widths and the gutters between them are not uniform, which is what the alignment gate
    measures. Placing them by hand makes the three ladders directly comparable in width as well.
    """
    df = pd.read_csv(F.DATA / "ownership-full.csv")
    aclsize.use()
    FW, FH = fs.WIDTH, 2.72
    left, bottom, top_pad = 0.52, 0.62, 0.30
    gutter = 0.12 if shared_axis else 0.34          # room for the y-tick labels of (b) and (c)
    key_w, key_gap = 1.30, 0.10
    W = (FW - left - 2 * gutter - key_gap - key_w) / 3
    H = FH - bottom - top_pad
    f = plt.figure(figsize=(FW, FH))
    axes = []
    for k, (title, sizes, ds) in enumerate(F.LADDERS):
        ax = f.add_axes([(left + k * (W + gutter)) / FW, bottom / FH, W / FW, H / FH], label="abc"[k])
        ladder(ax, df, title, sizes, ds, "abc"[k], fit, yticklabels=not (shared_axis and k > 0))
        ax.set_xlabel("model size", fontsize=8.5)
        axes.append(ax)
    axes[0].set_ylabel("ownership $O_q$", fontsize=8.5)
    kax = f.add_axes([(FW - key_w) / FW, bottom / FH, key_w / FW, H / FH], label="key")
    leg, t = key_panel(kax)
    t.set_text("largest $O_q$ at the\nlargest size")
    qa.run(f, name)
    aclsize.save(f, name, rows=[["a", "b", "c"]], exclude=("key",))
    plt.close(f)


if __name__ == "__main__":
    build("fig6-C-portrait", F.fit_y, shared_axis=False)
    build("fig6-D-portrait-shared", fit_shared, shared_axis=True)
