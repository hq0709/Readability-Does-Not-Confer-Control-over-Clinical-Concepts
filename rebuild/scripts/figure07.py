"""Figure 7 (fig6_ladders) redrawn from data/plot/figures/figure-07/ownership-full.csv.

Changes against the original, per review:
  colour      project concept palette (style.CONCEPT_COLOR), no extra tinting of the non-emphasised series
  markers     fixed per concept across all panels (the original assigned them in panel order)
  owned       filled marker = owned, open marker = not owned (replaces the barely visible ring)
  lines       the concept with the largest O at the largest size: thick solid; the others: thinner dashed, full colour;
              legend lists concepts by colour + marker only and explains the two line styles once
  axes        left/bottom spines only, no grid, zero line kept; y label without the "(ringed: owned)" aside;
              each panel has its own y range (b and c span far less than a), tick labels on every panel
  layout      one frameless legend below the panels (3 rows x 4 columns) instead of three framed legends inside the panels; (c) ~10% wider
              for visual balance, 1 pt outer padding, each x range = its size span plus 12% padding (log2), so points reach close to the panel edges
Values are read from the CSV unchanged.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import style
import qa
from style import fs, plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

DATA = style.FIGDATA / "figure-07"
LADDERS = [("Qwen2.5-VL, NIH", [("q25-3", "3B"), ("q25-7", "7B"), ("q25-32", "32B"), ("q25-72", "72B")], "nih"),
           ("Qwen3-VL, NIH", [("q3-4", "4B"), ("q3-8", "8B"), ("q3-32", "32B")], "nih"),
           ("Lingshu, CheXpert", [("lingshu-7", "7B"), ("lingshu-32", "32B")], "chexpert")]
MARKER = {"Effusion": "o", "Atelectasis": "s", "Pneumothorax": "^", "Cardiomegaly": "D", "Mass": "v", "Nodule": "P",
          "Consolidation": "X", "Edema": "h"}
ORDER = ["Effusion", "Atelectasis", "Pneumothorax", "Cardiomegaly", "Mass", "Nodule", "Consolidation", "Edema"]
PAD_FRAC = 0.12                 # x padding on each side, as a fraction of the panel's log2 size span
LW, LW_EMPH, MS = 1.15, 2.2, 4.4
DASH = (0, (3.2, 1.8))          # other concepts: thin dashed, slightly faded, so the emphasised series leads
ALPHA_BG = 1.0                  # no fading (user: colours should read deeper); dashes alone set them back


def fit_y(ax, v):
    """Per-panel y range: the data rounded out to the tick step (0.3 for a wide ladder, 0.1 otherwise), zero included."""
    step = 0.3 if v.max() - v.min() > 0.6 else 0.1
    lo = min(np.floor(v.min() / step - 1e-9) * step, 0.0); hi = max(np.ceil(v.max() / step + 1e-9) * step, 0.0)
    pad = 0.04 * (hi - lo)                                   # room for the markers at the extremes
    ax.set_ylim(lo - pad, hi + pad); ax.set_yticks(np.round(np.arange(lo, hi + step / 2, step), 2))
    # short tick labels (.3 / -.3 / 0), as in the heat maps: narrower label columns leave the panels more width
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "0" if abs(v) < 1e-9 else
                                               ("\u2212" if v < 0 else "") + f"{abs(v):.1f}".lstrip("0")))


def main():
    style.use()
    df = pd.read_csv(DATA / "ownership-full.csv")
    f = plt.figure(figsize=(fs.WIDTH, 2.95), layout="constrained")   # legend below; panels a little wider than tall
    # equal panels read unequal: (c) has only two sizes (points at both edges, empty middle) and ends at the figure's
    # right edge, so it looks narrowest. It gets ~10% more width.
    gs = f.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.1])
    f.get_layout_engine().set(w_pad=1 / 72)                 # 1 pt side padding: the figure fills the text width
    axes = [f.add_subplot(gs[0])]
    axes += [f.add_subplot(gs[k]) for k in (1, 2)]          # own y range per panel (see fit_y)
    emphs = []
    for k, (ax, (title, sizes, ds)) in enumerate(zip(axes, LADDERS)):
        g = df[df.dataset == ds]
        keys = [m for m, _ in sizes]
        xs = g.drop_duplicates("checkpoint_key").set_index("checkpoint_key").loc[keys, "size_b"].to_numpy(float)
        concepts = list(dict.fromkeys(g.concept))
        last = g[g.checkpoint_key == keys[-1]].set_index("concept").ownership
        emph = last.idxmax()                              # largest ownership at the largest size
        emphs.append(emph)
        ax.axhline(0, color=fs.CHANCE, ls="--", lw=0.7, zorder=1)
        for c in sorted(concepts, key=lambda c: c == emph):   # emphasised series drawn last (on top)
            rows = g[g.concept == c].set_index("checkpoint_key").loc[keys]
            col = style.CONCEPT_COLOR[c]; e = c == emph
            ax.plot(xs, rows.ownership, color=col, lw=LW_EMPH if e else LW, ls="-" if e else DASH,
                    alpha=1 if e else ALPHA_BG, zorder=4 if e else 3, solid_capstyle="round")
            for x, y, o in zip(xs, rows.ownership, rows.owned):
                ax.plot(x, y, marker=MARKER[c], ms=MS + (1.0 if e else 0), mec=col, mew=1.1,
                        mfc=col if o else "white", ls="none", alpha=1 if e else ALPHA_BG, zorder=6 if e else 5)
        ax.set_xscale("log", base=2)
        pad = PAD_FRAC * np.log2(xs[-1] / xs[0])
        ax.set_xlim(xs[0] / 2 ** pad, xs[-1] * 2 ** pad)
        ax.set_xticks(xs, [l for _, l in sizes]); ax.xaxis.set_minor_locator(plt.NullLocator())
        ax.set_title(f"({'abc'[k]})  {title}", fontsize=8.5, pad=5)
        ax.set_xlabel("model size", fontsize=8.5)
        fit_y(ax, g[g.checkpoint_key.isin(keys)].ownership)
    axes[0].set_ylabel("ownership $O_q$", fontsize=8.5)

    grey = fs.MUTED
    # legend under the panels, 3 rows x 4 columns: two rows of concepts (colour + marker only), one row of encodings.
    # matplotlib fills legends column by column, so the handles are listed column-major.
    conc = [Line2D([], [], ls="none", marker=MARKER[c], ms=MS + 0.5, mfc=style.CONCEPT_COLOR[c],
                   mec=style.CONCEPT_COLOR[c], label=c) for c in ORDER]
    enc = [Line2D([], [], ls="none", marker="o", ms=MS, mfc=grey, mec=grey, label="owned"),
           Line2D([], [], ls="none", marker="o", ms=MS, mfc="white", mec=grey, mew=0.9, label="not owned"),
           Line2D([], [], color=grey, lw=LW_EMPH, label="largest $O_q$ at the largest size"),
           Line2D([], [], color=grey, lw=LW, ls=DASH, label="other concepts")]
    rows = [conc[:4], conc[4:], enc]
    handles = [rows[r][c] for c in range(4) for r in range(3)]
    f.legend(handles=handles, loc="outside lower center", ncol=4, fontsize=7, frameon=False, handlelength=1.8,
             handletextpad=0.5, labelspacing=0.35, columnspacing=1.6, borderpad=0.1)
    qa.run(f, "figure-07")
    d = style.save(f, 7, "fig6_ladders")
    plt.close(f)
    print("wrote", d, "emphasised:", emphs)


if __name__ == "__main__":
    main()
