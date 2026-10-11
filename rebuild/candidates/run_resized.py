"""Render the ACL-width copies as candidates, with their comparable panel groups declared.

The alignment gate infers rows and columns from a gridspec. These figures place panels with
add_axes, so the groups are named here: the gate reports an add_axes layout as not auditable, and
not auditable is not the same as aligned.
"""
from __future__ import annotations

import aclsize
import style

SPEC = {
    # module          candidate name     rows of panels meant to line up            axes to exclude
    "figure03_acl": ("fig7-A-flow",      [["flow0", "flow1", "flow2"]],             ()),
    "figure04_acl": ("fig3-A-example",   [],                                        ("img0", "img1")),
    "figure06_acl": ("fig5-A-reader",    [["h0", "h1", "h2"]],                      ("cbar",)),
    "figure08_acl": ("figA1-A-median",   [["med0", "med1", "med2"]],                ("cbar",)),
}

# the two example rows are stacked, so they are a column group, not a row group
COLS = {"figure04_acl": [["bars0", "bars1"]]}

for mod, (out, rows, exclude) in SPEC.items():
    aclsize.use()
    m = __import__(mod)
    style.save = (lambda fig, _n, _s, _o=out, _r=rows, _e=exclude, _c=COLS.get(mod):
                  aclsize.save(fig, _o, rows=_r, cols=_c, exclude=_e))
    m.main()
