"""The rank of each concept's own direction, as its own appendix figure.

Candidate E for Figure 2 carries three panels and no rank curve, but Section 5 cites the rank of the
own direction among the 120 compared effects. The evidence moves rather than disappears: one
single-column panel in the appendix, drawn by the same code that drew it as Figure 2(d).
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import aclsize
from aclsize import fs
import qa
import figure02 as F


def main():
    aclsize.use(aclsize.COLUMN)                     # one column of the two-column page
    f = plt.figure(figsize=(fs.WIDTH, 2.45))
    f.subplots_adjust(left=0.185, right=0.955, bottom=0.30, top=0.95)
    ax = f.add_subplot(111, label="a")
    F.panel_d(ax)
    ax.set_title("")                                 # a one-panel figure needs no panel title
    ax.set_xlabel("rank of own direction (1 = strongest of 120)", fontsize=8)
    # the panel already carries a key of the three share-at-rank-1 figures; naming the datasets there
    # is shorter than a second legend, which in one column lands on the axis label
    SHORT = {"coco": "COCO", "chexpert": "CheXpert", "nih": "NIH"}
    pcts = [t for t in ax.texts if t.get_text().endswith("%")]
    for t, ds in zip(pcts, ("coco", "chexpert", "nih")):
        t.set_text(f"{SHORT[ds]}  {t.get_text()}")
    for t in ax.texts:                                   # make room for the longer labels
        x, y = t.get_position(); t.set_position((x - 0.30, y))
    for ln in ax.lines:
        if ln.get_transform() is ax.transAxes and ln.get_linestyle() == "None":
            ln.set_xdata([v - 0.30 for v in ln.get_xdata()])
    qa.run(f, "figA3-rank")
    aclsize.save(f, "figA3-rank")
    plt.close(f)


if __name__ == "__main__":
    main()
