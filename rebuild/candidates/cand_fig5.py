"""Figure 5 candidates: the shared-write reader heat maps at the real ACL width.

The ceiling mark is a hatch over the whole cell, and on COCO most cells are both coloured and
hatched, so the value sits on the hatch strokes: .75, .76, .61 and .48 all have lines through the
digits. The collision audit flags it and the render confirms it -- this one is not a bounding-box
artifact of rotated labels.

  A  the present encoding, re-authored at 6.32 in
  B  the same, with a thin white halo behind every value so a digit reads over the hatching
"""
from __future__ import annotations

import matplotlib.patheffects as pe

import aclsize
import style

import figure06_acl as F

def halo_values(fig):
    """Outline the in-cell values so a digit reads over the hatching.

    The halo has to follow the text. A dark value on a pale cell wants a white outline; a white value
    on a dark cell wants an ink one -- white on white turns .75 into a blob. The value colour is
    already chosen from cell luminance, so reading it back gives the right halo for free.
    """
    n = 0
    for ax in fig.axes:
        for t in ax.texts:
            white = str(t.get_color()).lower() in ("white", "#ffffff", "w")
            t.set_path_effects([pe.withStroke(linewidth=1.5, foreground="#3a3a3a" if white else "white")])
            t.set_zorder(7)
            n += 1
    return n


def render(name, halo):
    aclsize.use()

    def save(fig, _no, _stem):
        if halo:
            print(f"   halo on {halo_values(fig)} in-cell values")
        return aclsize.save(fig, name, rows=[["h0", "h1", "h2"]], exclude=("cbar",))

    style.save = save
    F.main()


if __name__ == "__main__":
    render("fig5-A-reader", halo=False)
    render("fig5-B-halo", halo=True)
