"""The rank of each concept's own direction, as its own single-column appendix figure.

Candidate E for Figure 2 carries three panels and no rank curve, but Section 5 cites the rank of the
own direction among the 120 compared effects, so the curve moves here rather than being dropped.

The curves are the same step construction and the same exported ranks as the panel they came from.
The key is not: reusing the four-panel version's in-panel key and shifting it left left the markers
behind their labels. The three curves are furthest apart at rank 1 -- 71, 11 and 3 per cent -- which
is exactly where a direct label belongs, so there is no key at all.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator

import aclsize
from aclsize import fs
import qa
import figure02 as F

DATASETS = ("coco", "chexpert", "nih")
SHORT = {"coco": "COCO", "chexpert": "CheXpert", "nih": "NIH"}
# where to hang each label: the rank it is anchored at, the offset in points, and the corner it takes.
# The two chest curves run close together everywhere, so one label goes into the empty band above them
# and the other into the empty corner below; COCO sits in the band over its own curve.
LABEL = {"coco":     (4,  (0, 7),   "left",  "bottom"),
         "chexpert": (26, (-2, 7),  "right", "bottom"),
         "nih":      (14, (6, -8),  "left",  "top")}


def main():
    aclsize.use(aclsize.COLUMN)                      # one column of the two-column page
    df = pd.read_csv(F.DATA / "panel-d-ranks.csv")
    f = plt.figure(figsize=(fs.WIDTH, 2.30))
    f.subplots_adjust(left=0.175, right=0.965, bottom=0.235, top=0.97)
    ax = f.add_subplot(111, label="a")
    xs = np.arange(1, 121)
    for ds in DATASETS:
        r = df[df.dataset == ds]["rank"].to_numpy()
        share = (r <= xs[:, None]).mean(axis=1)
        ax.step(xs, share, where="post", color=fs.DATASET_COLOR[ds], lw=1.5, zorder=3)
        first = (r == 1).mean()
        ax.plot(1, first, marker=fs.DATASET_MARKER[ds], color=fs.DATASET_COLOR[ds], ms=5,
                mec="white", mew=0.7, zorder=5)
        at, off, ha, va = LABEL[ds]
        ax.annotate(f"{SHORT[ds]}  {100 * first:.0f}%", (at, share[at - 1]), xytext=off,
                    textcoords="offset points", ha=ha, va=va, fontsize=7.5,
                    color=fs.DATASET_COLOR[ds], zorder=6)
    ax.set_xscale("log"); ax.set_xlim(0.9, 125); ax.set_ylim(0, 1.0)
    ticks = [1, 2, 5, 10, 20, 50, 120]
    ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels([str(t) for t in ticks])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("rank of own direction (1 = strongest of 120)", fontsize=8)
    ax.set_ylabel("cumulative fraction of cells", fontsize=8)
    qa.run(f, "figA3-rank")
    aclsize.save(f, "figA3-rank")
    plt.close(f)


if __name__ == "__main__":
    main()
