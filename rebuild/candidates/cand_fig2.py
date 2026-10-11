"""Figure 2 candidates: the overview panel at the real ACL width.

The four panels already carry four different inferential roles -- establish the three grades (a),
stratify by checkpoint (b), stress the write with steering strength (c), and compare the own
direction against its 119 competitors (d). What the present layout does not do is rank them: a 2x2
grid of equal panels states that the four are equally important, when (a) is the result and the
other three defend it.

  A  the same 2x2, re-authored at 6.32 in so the page no longer enlarges it
  B  hero: (a) tall on the left, the three defences smaller at the right
  C  one row of four: the shortest version, for the page budget
"""
from __future__ import annotations

import aclsize
from aclsize import fs, style   # noqa: F401
import qa
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

import figure02 as F

DATASETS = F.DATASETS
COL, MK, LAB = fs.DATASET_COLOR, fs.DATASET_MARKER, fs.DATASET_LABEL


def compact(ax_b, ax_c, ax_d, short=False):
    """Shorter titles and axis labels for the narrow panels of the hero and row layouts.

    The long forms were written for a 2.6 in panel. What they spell out -- that the dose curve is a
    median over models, that the steering strength is a fraction of the token norm -- belongs in the
    caption once, not in an axis label that then collides with its own tick.
    """
    ax_b.set_title("(b)  per-model landscape", fontsize=9, pad=5)
    ax_c.set_title("(c)  dose response", fontsize=9, pad=5)
    ax_d.set_title("(d)  rank of own direction", fontsize=9, pad=5)
    if short:
        ax_b.set_title("(b)  landscape", fontsize=9, pad=5)
        ax_d.set_title("(d)  own-direction rank", fontsize=9, pad=5)
    ax_c.set_xlabel(r"steering strength $\alpha$")
    ax_c.set_ylabel("ownership $O$")
    ax_d.set_xlabel("rank of own direction")


def legend(f, fontsize=7.5):
    handles = [Line2D([], [], marker=MK[d], ms=6, color=COL[d], ls="none", mec="white", label=LAB[d])
               for d in DATASETS]
    f.legend(handles=handles, loc="outside lower center", ncol=3, fontsize=fontsize,
             columnspacing=1.8, handletextpad=0.3)


def cand_A():
    """Same composition, authored at the real width; height scaled with it so the panels keep their shape."""
    aclsize.use()
    f, axes = plt.subplots(2, 2, figsize=(fs.WIDTH, 4.3 * aclsize.K), layout="constrained")
    f.get_layout_engine().set(w_pad=0.06, h_pad=0.06, wspace=0.08, hspace=0.08)
    F.panel_a(axes[0, 0]); F.panel_b(axes[0, 1]); F.panel_c(axes[1, 0]); F.panel_d(axes[1, 1])
    legend(f)
    qa.run(f, "fig2-A")
    aclsize.save(f, "fig2-A-grid"); plt.close(f)


def cand_B():
    """Hero: the grade counts get the tall left panel; the three defending panels sit at the right."""
    aclsize.use()
    f = plt.figure(figsize=(fs.WIDTH, 4.1), layout="constrained")
    f.get_layout_engine().set(w_pad=0.06, h_pad=0.06, wspace=0.09, hspace=0.10)
    gs = f.add_gridspec(2, 3, width_ratios=[1.35, 1.0, 1.0])
    ax_a = f.add_subplot(gs[:, 0])
    ax_b = f.add_subplot(gs[0, 1]); ax_c = f.add_subplot(gs[0, 2])
    ax_d = f.add_subplot(gs[1, 1:])
    F.panel_a(ax_a); F.panel_b(ax_b); F.panel_c(ax_c); F.panel_d(ax_d)
    compact(ax_b, ax_c, ax_d)
    legend(f)
    qa.run(f, "fig2-B")
    aclsize.save(f, "fig2-B-hero"); plt.close(f)


def cand_C():
    """One row: establish, stratify, stress, compare -- read left to right, shortest on the page."""
    aclsize.use()
    # explicit equal widths rather than constrained layout: the engine gives each panel the slot its
    # own tick labels need, so the four plot areas end up different widths and the gutters between
    # them are not uniform -- which is what the alignment gate measures.
    f, axes = plt.subplots(1, 4, figsize=(fs.WIDTH, 2.35))
    f.subplots_adjust(left=0.072, right=0.972, bottom=0.30, top=0.88, wspace=0.42)
    F.panel_a(axes[0]); F.panel_b(axes[1]); F.panel_c(axes[2]); F.panel_d(axes[3])
    compact(axes[1], axes[2], axes[3], short=True)
    # the in-panel key of (d) is placed for a 2.6 in panel; at 1.2 in it runs off the figure
    for t in axes[3].texts:
        x, y = t.get_position()
        t.set_position((x - 0.30, y))
    for ln in axes[3].lines:
        if ln.get_transform() is axes[3].transAxes and ln.get_linestyle() == "None":
            ln.set_xdata([v - 0.30 for v in ln.get_xdata()])
    # nine bars in a 1.4 in panel cannot also carry nine count labels: they collide, and the counts
    # are already in Table 1. The row layout keeps the shape of the comparison and drops the numbers.
    for t in list(axes[0].texts):
        t.remove()
    axes[0].set_title("(a)  cells per grade", fontsize=9, pad=5)
    axes[0].set_xticks(range(3), ("read", "answer", "own"))
    axes[0].set_xlabel("grade")
    axes[2].set_xticks([-0.5, 0, 0.5])
    axes[3].set_xticks([1, 10, 120]); axes[3].set_xticklabels(["1", "10", "120"])
    legend(f, fontsize=7)
    qa.run(f, "fig2-C")
    aclsize.save(f, "fig2-C-row"); plt.close(f)


if __name__ == "__main__":
    cand_A(); cand_B(); cand_C()
