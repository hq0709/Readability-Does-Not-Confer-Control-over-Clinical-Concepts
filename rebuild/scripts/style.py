"""Shared style for every rebuilt figure.

Base: the paper's house style (reading-is-not-writing/scripts/figstyle.py) -- serif type, Morandi dataset palette,
markers, sizes -- kept unchanged so rebuilt figures stay consistent with the rest of the paper.
Overrides from academic-figure-skill (Nature-style): left/bottom spines only (AP-3), 0.6 pt spines and ticks (CL-5),
outward ticks (CL-6), no background grid (VI-3), frameless legends,
Panel titles keep the house "(a)  title" form (fs.panel_title) -- do not move them. PDF with embedded Type 42 fonts plus a 300 dpi PNG preview (CL-4, AP-5).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # the paper repository: rebuild/ lives inside it
REPO = ROOT
FIGDATA = REPO / "data/plot/figures"
OUTROOT = ROOT / "rebuild/output"

sys.path.insert(0, str(REPO / "scripts"))
import figstyle as fs                                   # noqa: E402  (also selects the Agg backend)
import matplotlib.pyplot as plt                         # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

OVERRIDES = {
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.6, "axes.edgecolor": "#444444",
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.minor.width": 0.5, "ytick.minor.width": 0.5,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "xtick.direction": "out", "ytick.direction": "out",
    "axes.grid": False,
    "legend.frameon": False,
}


# Dataset colours: warmer, higher-chroma replacement for the house Morandi trio (which reads grey/faded), softened to
# sit with Figure 1 and the table shading (tables/cf_colors.tex). Project-wide: every rebuilt figure uses these.
# Validated with the dataviz palette checker (lightness band, CVD and normal-vision separation, all pairs).
DATASET_COLOR = {"nih": "#BF6254", "chexpert": "#D7AB56", "coco": "#5282B3"}   # soft terracotta / ochre / dusty blue
fs.DATASET_COLOR.update(DATASET_COLOR)   # mutate in place: every figure script shares this dict

# Concept colours: eight slots at the same softened level, replacing the house slots one for one (ROSE, SAGE, HAZE, OAT,
# LILAC, SLATE, MUSTARD, TERRACOTTA). Red, blue and ochre share their hues with the dataset colours.
# Deepened one step on Figure 7 (user: the concept colours read too light): OKLCH lightness -0.07 and chroma +0.015 per
# slot (half for the already dark slate and teal; pink only -0.03 so it stays apart from teal under CVD).
# Validated per figure panel on the adjacent concept order (NIH, CheXpert, COCO): CVD dE >= 8.8, normal dE >= 15.5.
# Dataset colours (DATASET_COLOR) are unchanged, so the concept red/blue/ochre are now a shade deeper than them.
SLOT = {"red": "#AE473A", "green": "#639F79", "blue": "#346DA5", "ochre": "#C59429",
        "lavender": "#866BB7", "slate": "#3B6674", "teal": "#01736A", "pink": "#D27488"}
CONCEPT_COLOR = {"Effusion": SLOT["red"], "Atelectasis": SLOT["green"], "Pneumothorax": SLOT["blue"], "Cardiomegaly": SLOT["ochre"],
                 "Mass": SLOT["lavender"], "Nodule": SLOT["slate"], "Consolidation": SLOT["teal"], "Edema": SLOT["pink"],
                 "person": SLOT["red"], "dog": SLOT["green"], "car": SLOT["blue"], "chair": SLOT["ochre"],
                 "bottle": SLOT["lavender"], "bicycle": SLOT["teal"]}
# Diverging map for every heat map (decided on Figure 5): intuitive direction, warm terracotta = positive / high, cool
# dusty blue = negative / low, warm off-white at zero (the table's neutral family). The ramps pass through the project
# colours one step before their darkest end, so extremes are a shade deeper than the categorical colours.
DIV_MID = "#F4F1EC"
DIV_POS = ["#EDD0C9", "#DA9C8F", "#C66F5F", "#A9503F"]   # light -> dark (terracotta)
DIV_NEG = ["#D2DEEC", "#A0BAD9", "#6D95C2", "#44709F"]   # light -> dark (dusty blue)
DIVERGING = LinearSegmentedColormap.from_list("project_div", DIV_NEG[::-1] + [DIV_MID] + DIV_POS, N=256)

SHORT_CONCEPT = {"Effusion": "Effus.", "Atelectasis": "Atel.", "Pneumothorax": "Pneu.", "Cardiomegaly": "Card.",
                 "Mass": "Mass", "Nodule": "Nodule", "Consolidation": "Cons.", "Edema": "Edema"}


def use():
    fs.use_house_style()
    plt.rcParams.update(OVERRIDES)


def outdir(fig_no: int) -> Path:
    d = OUTROOT / f"figure-{fig_no:02d}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save(fig, fig_no: int, stem: str):
    d = outdir(fig_no)
    fig.savefig(d / f"{stem}.pdf")
    fig.savefig(d / f"{stem}.png", dpi=300)
    return d
