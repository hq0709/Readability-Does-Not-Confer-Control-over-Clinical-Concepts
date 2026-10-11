"""Final-size geometry for the ACL two-column page, and a candidate writer.

The house style authors every figure at 5.5 in and states the invariant that it is included at
\\textwidth so nothing is rescaled. That invariant held for a one-column 11 pt layout. It does not
hold now: the ACL text width is 455.24 pt = 6.32 in and the column width 219.09 pt = 3.04 in, so a
5.5 in figure placed in a spanning float is enlarged by 1.149 and every 7 pt label prints at 8.0 pt.
Authoring at the real width restores the invariant and gives the data the extra inch instead of
giving it to the type.

Candidates are written under rebuild/candidates/output/. Nothing in figures/ is touched.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))          # the house style and the figure modules

import style                                               # noqa: E402
from style import fs                                       # noqa: E402

SPAN_PT, COL_PT = 455.24411, 219.08614                     # measured from the compiled ACL document
SPAN, COLUMN = SPAN_PT / 72.0, COL_PT / 72.0               # 6.323 in, 3.043 in
AUTHORED = 5.5                                             # the width the existing figures were drawn at
K = SPAN / AUTHORED                                        # 1.1496

OUT = HERE / "output"
SKILL = Path("/rodata/azradonc_dev/m253405/fake_home/.claude/skills/nature-figure/scripts")
sys.path.insert(0, str(SKILL))


def use(width: float = SPAN):
    """House style, with the figure width set to the real one and the QA width check moved with it."""
    style.use()
    fs.WIDTH = width
    import qa
    qa.WIDTH_IN = width
    return width


def _axes_by_label(fig, labels):
    by = {}
    for ax in fig.axes:
        by.setdefault(str(ax.get_label() or ""), ax)
    return [by[l] for l in labels if l in by]


def save(fig, name: str, rows=None, cols=None, exclude=(), exemptions=()):
    """Write the candidate, after measuring the rendered plot-area geometry.

    `rows` and `cols` name the panels that are meant to line up, by the axes label the drawing code
    gave them. The gate cannot infer them for a figure laid out with add_axes rather than a gridspec,
    and an uninferred layout counts as not auditable, not as aligned. `exclude` drops colour bars and
    image insets, which are not comparable panels. `exemptions` records an intentional difference
    with its reason; the gate requires the reason, not just the flag.
    """
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    verdict = "NOT AUDITABLE"
    try:
        from audit_panel_alignment import require_matplotlib_panel_alignment, PanelAlignmentError
        kw = {}
        # row_groups/column_groups are panel ids, and an id defaults to the axes label the drawing
        # code set, so the label lists go through unchanged. exclude_axes does take axes objects.
        if rows:
            kw["row_groups"] = [list(r) for r in rows]
        if cols:
            kw["column_groups"] = [list(c) for c in cols]
        if exclude:
            kw["exclude_axes"] = _axes_by_label(fig, exclude)
        if exemptions:
            kw["exemptions"] = list(exemptions)
        try:
            require_matplotlib_panel_alignment(
                fig, json_out=str(d / f"{name}.alignment.json"),
                tolerance_pt=1.5, gutter_tolerance_pt=1.5, strict=False, **kw)
            verdict = "ALIGNED"
        except PanelAlignmentError as e:
            verdict = "FIX: " + str(e).strip().splitlines()[-1][:95]
    except Exception as e:                                   # the gate must not stop a candidate render
        verdict = f"NOT AUDITABLE ({type(e).__name__}: {e})"[:110]
    fig.savefig(d / f"{name}.pdf")
    fig.savefig(d / f"{name}.png", dpi=300)
    print(f"wrote {d}/{name}.pdf  ({fig.get_figwidth():.3f} x {fig.get_figheight():.3f} in)  "
          f"alignment: {verdict}")
    return d
