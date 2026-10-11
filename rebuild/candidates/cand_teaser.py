"""Figure 1 (fig0_teaser): the RAW grades over the whole grid, chest radiographs against natural images.

Complements Figure 3 (fig3_example), which shows single images; this figure carries the grid-wide rates that the
old Figure 2(a) carried. Thumbnails are the appendix examples (figA2_examples), not the Figure 3 images.
Numbers: data/plot/figures/figure-02/panel-a-bars-full.csv; the best-answered stratum is the Section 5.3 count.
Run from rebuild/candidates/; writes output/teaser/ and installs figures/fig0_teaser.{pdf,png}.
"""
import shutil
import sys
from pathlib import Path
P = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(P / "rebuild/scripts"))
import pandas as pd
import style
from style import fs, plt
from PIL import Image

style.use()
grades = pd.read_csv(P / "data/plot/figures/figure-02/panel-a-bars-full.csv")
def rate(dsets, g):
    t = grades[(grades.dataset.isin(dsets)) & (grades.grade == g)]
    return 100 * t.numerator.sum() / t.denominator.sum(), int(t.denominator.sum())
OK, NO, TRACK, HAIR = style.SLOT["green"], style.SLOT["red"], "#ECE8E2", "#D6D1C9"
SYM = dict(family="DejaVu Sans", fontweight="bold")
IMG = P / "rebuild/assets/teaser"
# best-answered stratum (clean-answer AUROC >= 0.90), as printed in Section 5.3
TOP = {"chest": (12, 37), "coco": (145, 162)}
EX = [dict(key="chest", sets=["nih", "chexpert"], col=style.DATASET_COLOR["nih"], title="Chest radiographs",
           sub="NIH, CheXpert", imgs=["figA2_I1.png", "figA2_I3.png", "figA2_I6.png"]),
      dict(key="coco", sets=["coco"], col=style.DATASET_COLOR["coco"], title="Natural images",
           sub="COCO", imgs=["figA2_I7.png", "figA2_I8.png", "figA2_I10.png"])]

W, GUT, IG = 3.043, 0.17, 0.03            # ACL column width
PW = (W - GUT) / 2
TH = (PW - 2 * IG) / 3                    # thumbnail edge
TITLE, PIPE, TOPB = 0.16, 0.31, 0.25
H = TITLE + TH + 0.06 + PIPE + 0.03 + TOPB
f = plt.figure(figsize=(W, H))
X = lambda v: v / W
Y = lambda v: v / H
f.add_artist(plt.Line2D([X(W / 2)] * 2, [Y(0.02), Y(H - 0.02)], transform=f.transFigure, color=HAIR, lw=0.6))

def square(path):
    im = Image.open(path).convert("RGB"); w, h = im.size; s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))

for p, e in enumerate(EX):
    x0 = p * (PW + GUT)
    n = rate(e["sets"], "owned")[1]
    f.text(X(x0), Y(H - 0.005), e["title"], ha="left", va="top", fontsize=7.4, fontweight="bold", color=e["col"])
    yi = H - TITLE - TH
    for k, name in enumerate(e["imgs"]):
        ax = f.add_axes([X(x0 + k * (TH + IG)), Y(yi), X(TH), Y(TH)]); ax.imshow(square(IMG / name)); ax.set_axis_off()
    # read -> answer -> write, rates over the grid
    yp = yi - 0.06 - PIPE
    sw = PW / 3
    for i, (name, g) in enumerate([("read", "readable"), ("answer", "answerable"), ("write", "owned")]):
        v = rate(e["sets"], g)[0]; ok = v > 50
        c = OK if ok else NO
        cx = x0 + sw * (i + 0.5)
        f.text(X(cx), Y(yp + PIPE - 0.01), name, ha="center", va="top", fontsize=6.6, color=fs.INK,
               fontweight="bold" if name == "write" else "normal")
        f.text(X(cx - 0.035), Y(yp + 0.085), "✓" if ok else "✗", ha="right", va="center", fontsize=9.5, color=c, **SYM)
        f.text(X(cx - 0.02), Y(yp + 0.08), f"{v:.0f}%", ha="left", va="center", fontsize=6.8,
               color=c if name == "write" else fs.INK, fontweight="bold" if name == "write" else "normal")
        if i < 2:
            f.text(X(x0 + sw * (i + 1)), Y(yp + 0.085), "›", ha="center", va="center", fontsize=9, color=fs.MUTED)
    # owned among the cells the model answers best
    o, nt = TOP[e["key"]]; v = o / nt
    f.text(X(x0), Y(TOPB - 0.005), "owned, best-answered cells", ha="left", va="top", fontsize=6, color=fs.MUTED)
    ax = f.add_axes([X(x0), Y(0.0), X(PW - 0.27), Y(0.13)])
    ax.barh(0, 1, height=1, color=TRACK); ax.barh(0, v, height=1, color=e["col"])
    ax.set_xlim(0, 1); ax.set_ylim(-0.5, 0.5); ax.set_axis_off()
    f.text(X(x0 + PW), Y(0.065), f"{100 * v:.0f}%", ha="right", va="center", fontsize=6.8, fontweight="bold", color=e["col"])
out = P / "rebuild/candidates/output/teaser"; out.mkdir(parents=True, exist_ok=True)
for ext in ("pdf", "png"):
    f.savefig(out / f"fig0_teaser.{ext}", **({"dpi": 300} if ext == "png" else {}))
    shutil.copy(out / f"fig0_teaser.{ext}", P / "figures" / f"fig0_teaser.{ext}")
print("wrote figures/fig0_teaser.pdf", f"({W} x {H:.2f} in)")
