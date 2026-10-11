"""Figure 6 candidates: the size ladders at the real ACL width.

The three panels sit side by side and invite a comparison the axes do not support: (a) runs to 0.6,
(b) to 0.2, (c) to 0.3, so a line that looks steep in (b) is a sixth of the rise it would be in (a).
The caption states that the scales differ, which is honest but asks the reader to rescale by eye.

  A  one scale per panel, as now, re-authored at 6.32 in
  B  one scale for all three, so the panels are comparable and the chest effects stay visibly small
"""
from __future__ import annotations

import numpy as np
from matplotlib.ticker import FuncFormatter

import aclsize
import style
import qa  # noqa: F401

import figure07_acl as F


def shared_y(ax, _v):
    """One range for every panel: the union of the three ladders, rounded out to the 0.3 tick step."""
    lo, hi, step = -0.6, 0.6, 0.3
    pad = 0.04 * (hi - lo)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_yticks(np.round(np.arange(lo, hi + step / 2, step), 2))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "0" if abs(v) < 1e-9 else
                                               ("−" if v < 0 else "") + f"{abs(v):.1f}".lstrip("0")))


def render(name, fit):
    aclsize.use()
    F.fit_y = fit
    style.save = lambda fig, _no, _stem: aclsize.save(
        fig, name,
        exemptions=[{"panels": ["c"], "checks": ["panel-width"],
                     "reason": "panel (c) carries two model sizes against three in (a) and (b): at "
                               "equal width its points sit on both edges with an empty middle and it "
                               "reads as the narrowest, so it is given about ten per cent more"}])
    F.main()


if __name__ == "__main__":
    import figure07 as ORIG
    render("fig6-A-perpanel", ORIG.fit_y)
    render("fig6-B-shared", shared_y)
