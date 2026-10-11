"""Per-cell decision data for the new designs, taken through the paper's own inclusion rule.

Every table and figure of the paper selects blocks with cf_inclusion; this uses the same call, so the
450 cells here are the 450 cells the paper grades. Per cell it records the own write's effect, the
strongest competing write's effect, the random-family reference the write must clear, and the three
grades. Nothing is recomputed: O_q = W_qq - max_other_clinical is the definition the manifest writes.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import cf_inclusion as ci                      # noqa: E402
import export_campaign_plot_data as E          # noqa: E402

OUT = Path(__file__).resolve().parent / "data"


def main():
    all_blocks, included = E.blocks_from(ci.RUNS)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for (mk, ds), block in sorted(included.items()):
        s = block["summary"]
        core = s["core"]["per_question"]
        cal = s.get("calibration") or {}          # keyed by concept, not by "per_question"
        for c, v in core.items():
            k = cal.get(c, {})
            k = k if isinstance(k, dict) else {}
            rows.append({
                "checkpoint": mk, "dataset": ds, "concept": c,
                "W_qq": v.get("W_qq"),
                "max_other": v.get("max_other_clinical"),
                "O_q": v.get("O_q"),
                "argmax_other": v.get("argmax_other"),
                "random_p95": v.get("random_p95"),
                "rank_in_random_family": v.get("rank_in_random_family"),
                "steering_reference": bool(v.get("steering_reference")),
                "owned": ci.owned(v),
                "selectivity": k.get("selectivity"),
                "answer_auroc": k.get("answer_auroc"),
                "readable": ci.readable(k) if k else None,
                "answer_capable": ci.answer_capable(k) if k else None,
            })
    p = OUT / "cells.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    # The readable count of the paper is taken over every probe-graded block, not only the included
    # ones (cf_inclusion: a probe-graded block contributes readability even when CORE is incomplete),
    # so the three grades do not share a denominator. The funnel panel needs the paper's own numbers.
    grades = []
    for ds in ("nih", "chexpert", "coco"):
        read = [ci.readable(v) for (mk, d), b in all_blocks.items()
                if d == ds and "CALIBRATION" in b["run"].get("completed_modules", [])
                for v in b["summary"].get("calibration", {}).values() if isinstance(v, dict)]
        ans = [ci.answer_capable(b["summary"].get("calibration", {}).get(c, {}))
               for (mk, d), b in included.items() if d == ds
               for c in b["summary"]["core"]["per_question"]]
        own = [ci.owned(v) for (mk, d), b in included.items() if d == ds
               for v in b["summary"]["core"]["per_question"].values()]
        for grade, flags in (("readable", read), ("answerable", ans), ("owned", own)):
            grades.append({"dataset": ds, "grade": grade,
                           "numerator": int(sum(flags)), "denominator": len(flags)})
    gp = OUT / "grades.csv"
    with gp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(grades[0])); w.writeheader(); w.writerows(grades)
    print(f"{gp}: {len(grades)} rows")

    n_owned = sum(r["owned"] for r in rows)
    print(f"{p}: {len(rows)} cells, {n_owned} owned")
    for ds in ("nih", "chexpert", "coco"):
        g = [r for r in rows if r["dataset"] == ds]
        print(f"   {ds:9s} {len(g):3d} cells  owned {sum(r['owned'] for r in g):3d}"
              f"  readable {sum(bool(r['readable']) for r in g):3d}"
              f"  answerable {sum(bool(r['answer_capable']) for r in g):3d}")


if __name__ == "__main__":
    main()
