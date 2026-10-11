"""One PDF holding every candidate at its true size on the page, for choosing between them.

Each page is A4 with the ACL text column marked, the candidate placed at the width it would occupy
in the paper, and a header naming it and what it changes. Nothing is rescaled: what the page shows
is what the compiled paper shows. Built in matplotlib from the rendered PNG previews, so the figures
themselves remain the Python exports and this is only an assembly.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import aclsize

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
A4 = (8.27, 11.69)
SPAN = aclsize.SPAN

# name, heading, what it is
SHEET = [
    ("fig6-C-portrait", "Figure 6 — candidate C: portrait panels, key at the right",
     "RESHAPED. The three rows of legend under the panels took the bottom third and left each ladder "
     "1.3 in of height against 2.1 in of width. The key moves into a fourth slot, the panels take the "
     "whole height and turn portrait, and the figure is 2.72 in instead of 3.39 in. One y scale per panel."),
    ("fig6-D-portrait-shared", "Figure 6 — candidate D: portrait panels, one y scale",
     "RESHAPED, and all three ladders on one scale. The panels are wider because (b) and (c) no longer "
     "carry their own y ticks, and the comparison across panels becomes honest: the chest effects really "
     "are a fraction of the Qwen2.5-VL rise."),
    ("fig6-A-perpanel", "Figure 6 — candidate A: the present shape, for reference",
     "What it looks like now, re-authored at the real width: legend below, panels wide and short."),
]


def page(pdf, name, heading, blurb):
    png = OUT / name / f"{name}.png"
    pdf_path = OUT / name / f"{name}.pdf"
    if not png.exists():
        print(f"   missing {name}"); return
    import pymupdf
    r = pymupdf.open(pdf_path)[0].rect
    w_in, h_in = r.width / 72, r.height / 72

    f = plt.figure(figsize=A4)
    f.text(0.07, 0.962, heading, fontsize=13, weight="bold", color="#222222", va="top")
    f.text(0.07, 0.935, blurb, fontsize=8.5, color="#555555", va="top", wrap=True)
    f.text(0.07, 0.885, f"{name}.pdf    {w_in:.2f} x {h_in:.2f} in    "
                        f"({w_in * 72:.0f} x {h_in * 72:.0f} pt)    shown at true size",
           fontsize=7.5, color="#888888", va="top", family="monospace")

    # place at true size, top-aligned under the header
    left = (A4[0] - SPAN) / 2
    top = 0.86 * A4[1]
    scale = 1.0
    if h_in > top - 0.6:
        scale = (top - 0.6) / h_in
    w, h = w_in * scale, h_in * scale
    ax = f.add_axes([(A4[0] - w) / 2 / A4[0], (top - h) / A4[1], w / A4[0], h / A4[1]])
    ax.imshow(mpimg.imread(png)); ax.axis("off")
    if scale < 1.0:
        f.text(0.5, (top - h) / A4[1] - 0.018, f"reduced to {100 * scale:.0f}% to fit the sheet",
               ha="center", fontsize=7, color="#aa6655")
    # the ACL text column, for judging the width
    for x in (left / A4[0], (left + SPAN) / A4[0]):
        f.add_artist(plt.Line2D([x, x], [0.05, 0.875], color="#cfc9c1", lw=0.6, ls=(0, (4, 4))))
    f.text(left / A4[0], 0.042, "ACL text width 455 pt", fontsize=6.5, color="#aaaaaa")
    pdf.savefig(f); plt.close(f)


def main():
    out = HERE / "FIG6_OPTIONS.pdf"
    with PdfPages(out) as pdf:
        for name, heading, blurb in SHEET:
            page(pdf, name, heading, blurb)
    print(f"wrote {out}  ({len(SHEET)} pages)")


if __name__ == "__main__":
    main()
