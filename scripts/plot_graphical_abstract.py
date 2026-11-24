"""Graphical abstract for the Meta-Radiology submission (journal/graphical_abstract.{pdf,tiff}).

Left: the write matrix of one checkpoint (Qwen2.5-VL-7B) on NIH ChestX-ray14 and on COCO; each row is a
question, each column the concept direction written, colour the mean change in P(yes).
Right: share of cells passing each RAW grade, chest radiographs vs COCO, from the paper's macros.
Size: 13.28 x 5.31 in at 300 dpi (>= 1328 x 531 px required).
"""
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
macros = {}
for f in (ROOT / "tables/cf_numbers.tex", ROOT / "journal/journal_numbers.tex"):
    for k, v in re.findall(r"\\renewcommand\{\\(\w+)\}\{([^}]*)\}", f.read_text()):
        macros[k] = v
chest = [float(macros["cfChestReadablePct"]), float(macros["cfChestAnswerablePct"]),
         float(macros["cfChestOwnedPct"]), float(macros["jnTwoWayChestPct"])]
coco = [100 * 118 / 150, float(macros["cfCocoAnswerablePct"]), float(macros["cfCocoOwnedPct"]),
        float(macros["jnTwoWayCocoPct"])]
assert macros["cfCocoReadable"] == "118"

W = pd.read_csv(ROOT / "data/plot/figures/figure-05/write-matrices-full.csv")
CH, NAT, INK, MUTE = "#b5523b", "#8c8c8c", "#2b2b2b", "#6b6b6b"
plt.rcParams.update({"font.family": "serif", "font.serif": ["STIXGeneral", "Nimbus Roman", "DejaVu Serif"], "mathtext.fontset": "stix", "font.size": 13})

fig = plt.figure(figsize=(13.28, 5.31), dpi=300)
fig.patch.set_facecolor("white")
fig.text(0.02, 0.93, "A finding the model can decode is rarely controlled by its own direction",
         fontsize=19, fontweight="bold", color=INK)

for i, (ds, title, short) in enumerate((("nih", "Chest radiograph (NIH)", ["Eff", "Atel", "Ptx", "Card", "Mass", "Nod"]),
                                        ("coco", "Natural image (COCO)", ["person", "dog", "car", "chair", "bottle", "bike"]))):
    d = W[(W.checkpoint_key == "q25-7") & (W.dataset == ds)]
    order = list(dict.fromkeys(d.question))
    M = d.pivot(index="question", columns="written_direction", values="value").loc[order, order].values
    ax = fig.add_axes([0.065 + i * 0.29, 0.20, 0.52 * 5.31 / 13.28, 0.52])
    vmax = np.abs(M).max()
    ax.imshow(M, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    for k in range(6):
        ax.add_patch(plt.Rectangle((k - .5, k - .5), 1, 1, fill=False, ec=INK, lw=1.4))
    ax.set_xticks(range(6), short, rotation=90, fontsize=10)
    ax.set_yticks(range(6), short, fontsize=10)
    ax.tick_params(length=0)
    ax.set_title(title, fontsize=13, color=CH if ds == "nih" else MUTE, pad=6)
    ax.set_xlabel("direction written", fontsize=10.5, color=MUTE)
    if i == 0:
        ax.set_ylabel("question answered", fontsize=10.5, color=MUTE)
fig.text(0.065, 0.025, "Write matrices of Qwen2.5-VL-7B; boxed diagonal = the concept's own direction",
         fontsize=10.5, color=MUTE)

ax = fig.add_axes([0.70, 0.13, 0.27, 0.64])
labels = ["Readable", "Answerable", "Owned", "Owned and\nspecific"]
y = np.arange(4)[::-1]
h = 0.36
ax.barh(y + h / 2, chest, h, color=CH)
ax.barh(y - h / 2, coco, h, color=NAT)
for yy, a, b in zip(y, chest, coco):
    ax.text(a + 1.5, yy + h / 2, f"{a:.0f}%", va="center", fontsize=13, color=CH, fontweight="bold")
    ax.text(b + 1.5, yy - h / 2, f"{b:.0f}%", va="center", fontsize=13, color=NAT, fontweight="bold")
ax.set_yticks(y, labels, fontsize=13)
ax.set_xlim(0, 108)
ax.set_xticks([])
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.text(0, 4.05 - 0.6, "", fontsize=1)
fig.text(0.70, 0.82, "Chest radiographs", color=CH, fontsize=13.5, fontweight="bold")
fig.text(0.865, 0.82, "COCO objects", color=NAT, fontsize=13.5, fontweight="bold")
fig.text(0.615, 0.025, "Share of model-concept pairs passing each grade, 25 VLMs (3B-72B)",
         fontsize=10.5, color=MUTE)

out = ROOT / "journal/graphical_abstract"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=150)
fig.savefig(out.with_suffix(".tiff"), dpi=300, pil_kwargs={"compression": "tiff_lzw"})
print(out)
