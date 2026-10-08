"""Rendered-output QA (academic-figure-skill Pass 3, automated part) for a live matplotlib figure.

  VV-1  text/text overlaps and text over the legend
  VV-2  text clipped by the figure edge
  VV-3  font size floor (>= 5 pt at print size; the figure is authored at print size)
  CL-2  figure size (fixed paper width, 5.5 in)
Call run(fig, name) after drawing and before closing; it prints a report and returns the list of problems.
"""
from __future__ import annotations

from itertools import combinations

from matplotlib.legend import Legend
from matplotlib.text import Text

MIN_PT = 5.0
WIDTH_IN = 5.5


def _texts(fig):
    # tick labels of axes switched off with set_axis_off() stay "visible" as artists but are never drawn
    hidden = {id(t) for ax in fig.axes if not ax.axison
              for t in ax.get_xticklabels() + ax.get_yticklabels() + [ax.xaxis.label, ax.yaxis.label]}
    return [t for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip() and id(t) not in hidden]


def run(fig, name):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    legends = [l for l in fig.findobj(Legend)]
    legend_texts = {id(t) for l in legends for t in l.get_texts()}
    texts = [t for t in _texts(fig) if id(t) not in legend_texts]
    problems = []

    w_in = fig.get_figwidth()
    if abs(w_in - WIDTH_IN) > 0.01:
        problems.append(f"CL-2 width {w_in:.2f} in (expected {WIDTH_IN})")

    for t in texts + [t for l in legends for t in l.get_texts()]:
        if t.get_fontsize() < MIN_PT:
            problems.append(f"VV-3 '{t.get_text()[:30]}' is {t.get_fontsize():.1f} pt")

    boxes = [(t, t.get_window_extent(r)) for t in texts]
    for t, b in boxes:
        if b.x0 < -0.5 or b.y0 < -0.5 or b.x1 > W + 0.5 or b.y1 > H + 0.5:
            problems.append(f"VV-2 clipped: '{t.get_text()[:40]}'")
    for (t1, b1), (t2, b2) in combinations(boxes, 2):
        # parallel rotated labels (e.g. 45-degree tick labels) have overlapping axis-aligned boxes but not glyphs
        if t1.get_rotation() == t2.get_rotation() and t1.get_rotation() % 180 != 0:
            continue
        # pieces of one multi-colour label abut edge to edge; count only a real intersection (> 1 px each way)
        ix = min(b1.x1, b2.x1) - max(b1.x0, b2.x0); iy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
        if ix > 1 and iy > 1:
            problems.append(f"VV-1 overlap: '{t1.get_text()[:25]}' / '{t2.get_text()[:25]}'")
    for l in legends:
        lb = l.get_window_extent(r)
        for t, b in boxes:
            if lb.overlaps(b):
                problems.append(f"VV-1 legend overlaps '{t.get_text()[:25]}'")

    status = "PASS" if not problems else f"{len(problems)} issue(s)"
    print(f"[QA] {name}: {status}")
    for p in problems:
        print("   -", p)
    return problems
