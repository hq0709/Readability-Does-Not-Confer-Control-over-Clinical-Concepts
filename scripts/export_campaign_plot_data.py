"""Export plotted values from the released campaign summary bundle, without drawing figures.

Usage: python scripts/export_campaign_plot_data.py --runs ../reading-is-not-writing-code/runs
The selected inputs are the same packaged statistics read by plot_paper_figures.py.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "plot" / "figures"
DATASETS = ("nih", "chexpert", "coco")
MATRIX_PICKS = (("q25-7", "nih"), ("q25-72", "nih"), ("lingshu-32", "nih"),
                ("q25-7", "coco"), ("q3-32", "coco"), ("lingshu-32", "coco"))
READERS = ("gemma3-4", "gemma3-12", "gemma3-27", "medgemma-4", "medgemma-27")
LADDERS = (("q25-3", "nih", 3), ("q25-7", "nih", 7), ("q25-32", "nih", 32),
           ("q25-72", "nih", 72), ("q3-4", "nih", 4), ("q3-8", "nih", 8),
           ("q3-32", "nih", 32), ("lingshu-7", "chexpert", 7), ("lingshu-32", "chexpert", 32))


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def blocks_from(runs: Path) -> tuple[dict, dict]:
    all_blocks = {}
    for file in sorted(runs.glob("*/*/run.json")):
        run = read_json(file)
        key = (run.get("model_key", file.parent.parent.name), run.get("dataset_id", file.parent.name))
        all_blocks[key] = {"run": run, "summary": read_json(file.parent / "summary.json")}
    included = {key: block for key, block in all_blocks.items()
                if {"CORE", "CALIBRATION"}.issubset(block["run"].get("completed_modules", []))}
    assert len(included) == 75, f"expected 75 included blocks, got {len(included)}"
    return all_blocks, included


def concepts_and_matrix(summary: dict) -> tuple[list[str], np.ndarray]:
    concepts = list(summary["core"]["per_question"])
    matrix = np.array([[summary["core"]["W"][q].get(f"concept:{d}", np.nan)
                        for d in concepts] for q in concepts], dtype=float)
    return concepts, matrix


def matrix_rows(dataset: str, concepts: list[str], matrix: np.ndarray, **fields) -> list[dict]:
    return [{**fields, "dataset": dataset, "question": q, "written_direction": d, "value": float(matrix[i, j])}
            for i, q in enumerate(concepts) for j, d in enumerate(concepts)]


def ownership_rows(included: dict, pairs: dict) -> None:
    ceiling = {(c["model"], c["dataset"], c["concept"]) for c in pairs["task2_ceiling"]["cells"] if c.get("ceiling")}
    common = lambda mk, ds, c: {
        "checkpoint_key": mk, "dataset": ds, "concept": c,
        "ownership": included[(mk, ds)]["summary"]["core"]["per_question"][c]["O_q"],
        "owned": bool(included[(mk, ds)]["summary"]["core"]["per_question"][c].get("steering_reference")
                      and included[(mk, ds)]["summary"]["core"]["per_question"][c].get("verdict") == "fixed_family_advantage"),
    }
    reader = [{**common(mk, ds, c), "ceiling": (mk, ds, c) in ceiling}
              for ds in DATASETS for mk in READERS
              for c in included[(mk, ds)]["summary"]["core"]["per_question"]]
    assert len(reader) == 90
    write_csv(OUT / "figure-06" / "ownership-full.csv",
              ["checkpoint_key", "dataset", "concept", "ownership", "owned", "ceiling"], reader)
    ladder = [{**common(mk, ds, c), "size_b": size}
              for mk, ds, size in LADDERS
              for c in included[(mk, ds)]["summary"]["core"]["per_question"]]
    assert len(ladder) == 54
    write_csv(OUT / "figure-07" / "ownership-full.csv",
              ["checkpoint_key", "dataset", "concept", "ownership", "owned", "size_b"], ladder)


def overview(all_blocks: dict, included: dict, runs: Path) -> None:
    points, counts, ranks = [], [], []
    for ds in DATASETS:
        read = [bool(v.get("readable")) for (mk, d), block in all_blocks.items()
                if d == ds and "CALIBRATION" in block["run"].get("completed_modules", [])
                for v in block["summary"].get("calibration", {}).values() if isinstance(v, dict)]
        ans = [bool(block["summary"].get("calibration", {}).get(c, {}).get("answer_capable"))
               for (mk, d), block in included.items() if d == ds
               for c in block["summary"]["core"]["per_question"]]
        own = [bool(v.get("steering_reference") and v.get("verdict") == "fixed_family_advantage")
               for (mk, d), block in included.items() if d == ds
               for v in block["summary"]["core"]["per_question"].values()]
        for grade, flags in (("readable", read), ("answerable", ans), ("owned", own)):
            flags = np.asarray(flags, dtype=float)
            draws = np.random.default_rng(0).choice(flags, size=(2000, len(flags)), replace=True).mean(axis=1)
            counts.append({"dataset": ds, "grade": grade, "numerator": int(flags.sum()),
                           "denominator": len(flags), "fraction": float(flags.mean()),
                           "ci_low": float(np.percentile(draws, 2.5)), "ci_high": float(np.percentile(draws, 97.5))})
        for (mk, d), block in included.items():
            if d != ds:
                continue
            summary = block["summary"]
            core = summary["core"]["per_question"]
            cal = summary.get("calibration", {})
            sel = [cal[c]["selectivity"] for c in core if isinstance(cal.get(c), dict) and "selectivity" in cal[c]]
            own_values = [v["O_q"] for v in core.values() if v.get("O_q") is not None]
            points.append({"checkpoint_key": mk, "dataset": ds, "read": float(np.nanmean(sel)),
                           "ownership": float(np.nanmean(own_values))})
            ranks += [{"checkpoint_key": mk, "dataset": ds, "concept": c, "rank": v["rank_in_random_family"]}
                      for c, v in core.items() if v.get("rank_in_random_family")]
    assert len(points) == 75 and len(counts) == 9
    displayed = read_json(ROOT / "figures" / "fig2_counts.json")
    assert all([r["numerator"], r["denominator"]] == displayed[r["dataset"]][r["grade"]] for r in counts)
    write_csv(OUT / "figure-02" / "panel-a-bars-full.csv",
              ["dataset", "grade", "numerator", "denominator", "fraction", "ci_low", "ci_high"], counts)
    write_csv(OUT / "figure-02" / "panel-b-points-full.csv", ["checkpoint_key", "dataset", "read", "ownership"], points)
    write_csv(OUT / "figure-02" / "panel-d-ranks.csv", ["checkpoint_key", "dataset", "concept", "rank"], ranks)
    curves = read_json(runs / "figures" / "dose_curves.json")
    write_json(OUT / "figure-02" / "panel-c-block-curves.json", curves)
    summary_rows = []
    for ds in ("nih", "coco"):
        series = [v for key, v in curves.items() if key.endswith("/" + ds) and v]
        alphas = sorted({float(alpha) for row in series for alpha in row})
        values = np.array([[row.get(str(alpha), np.nan) for alpha in alphas] for row in series])
        for i, alpha in enumerate(alphas):
            summary_rows.append({"dataset": ds, "alpha": alpha, "blocks": len(series),
                                 "median": float(np.nanmedian(values[:, i])),
                                 "q25": float(np.nanpercentile(values[:, i], 25)),
                                 "q75": float(np.nanpercentile(values[:, i], 75))})
    write_csv(OUT / "figure-02" / "panel-c-plotted-summary.csv",
              ["dataset", "alpha", "blocks", "median", "q25", "q75"], summary_rows)


def examples(runs: Path, included: dict) -> None:
    import pyarrow.parquet as pq

    picks = (("q25-7", "nih", "00005446_000", "Effusion", "Nodule"),
             ("q25-7", "coco", "000000028449", "dog", "bottle"))
    rows = []
    for mk, ds, row_id, target, competitor in picks:
        concepts = list(included[(mk, ds)]["summary"]["core"]["per_question"])
        table = pq.read_table(runs / mk / ds / "outcomes" / "CORE.parquet",
                              columns=["row_id", "concept", "template_id", "fit_seed", "direction_id", "direction_kind", "p_present", "sample_status"])
        df = table.to_pandas()
        df = df[(df.row_id == row_id) & (df.sample_status == "OK") & (df.template_id == "IY") & (df.fit_seed == 0)]
        for question in concepts:
            for condition, direction in (("clean", "baseline"), ("concept_write", f"concept:{target}"),
                                         ("competitor_write", f"concept:{competitor}")):
                values = df[(df.concept == question) & (df.direction_id == direction)].p_present.tolist()
                assert len(values) == 1, (mk, ds, row_id, question, direction, len(values))
                rows.append({"checkpoint_key": mk, "dataset": ds, "row_id": row_id, "target": target,
                             "competitor": competitor, "question": question, "condition": condition,
                             "p_yes": float(values[0])})
    assert len(rows) == 36
    write_csv(OUT / "figure-04" / "all-bars-full.csv",
              ["checkpoint_key", "dataset", "row_id", "target", "competitor", "question", "condition", "p_yes"], rows)


def matrices(included: dict) -> None:
    selected = []
    for mk, ds in MATRIX_PICKS:
        summary = included[(mk, ds)]["summary"]
        concepts, matrix = concepts_and_matrix(summary)
        owned = {c for c, v in summary["core"]["per_question"].items()
                 if v.get("steering_reference") and v.get("verdict") == "fixed_family_advantage"}
        selected += [{**row, "owned_diagonal": row["question"] == row["written_direction"] and row["question"] in owned}
                     for row in matrix_rows(ds, concepts, matrix, checkpoint_key=mk)]
    assert len(selected) == 216
    write_csv(OUT / "figure-05" / "write-matrices-full.csv",
              ["checkpoint_key", "dataset", "question", "written_direction", "value", "owned_diagonal"], selected)
    flow, median = [], []
    for ds in DATASETS:
        cohort = [(mk, block["summary"]) for (mk, d), block in included.items() if d == ds]
        concepts = list(cohort[0][1]["core"]["per_question"])
        matrices = np.stack([concepts_and_matrix(summary)[1] for _, summary in cohort])
        flow += matrix_rows(ds, concepts, np.nanmean(np.maximum(matrices, 0), axis=0), checkpoints=len(cohort))
        median += matrix_rows(ds, concepts, np.nanmedian(matrices, axis=0), checkpoints=len(cohort))
    assert len(flow) == len(median) == 108
    write_csv(OUT / "figure-03" / "positive-flow-full.csv",
              ["dataset", "checkpoints", "question", "written_direction", "value"], flow)
    write_csv(OUT / "figure-08" / "median-write-matrices-full.csv",
              ["dataset", "checkpoints", "question", "written_direction", "value"], median)
    displayed = read_json(ROOT / "figures" / "figA1_own_share.json")
    for ds in DATASETS:
        rows = [row for row in flow if row["dataset"] == ds]
        assert np.isclose(sum(row["value"] for row in rows), displayed[ds]["total"])
        assert np.isclose(sum(row["value"] for row in rows if row["question"] == row["written_direction"]),
                          displayed[ds]["diag"])


def verify_example_annotations() -> None:
    reported = read_json(ROOT / "figures" / "fig3_example.json")
    with (OUT / "figure-04" / "all-bars-full.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for ds, annotation in reported.items():
        values = {(row["question"], row["condition"]): float(row["p_yes"])
                  for row in rows if row["dataset"] == ds}
        target = annotation["question"]
        assert np.isclose(values[target, "clean"], annotation["clean"])
        assert np.isclose(values[target, "concept_write"], annotation["concept_write"])
        assert np.isclose(values[target, "competitor_write"], annotation["competitor_write"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True, help="released code repository runs/ directory")
    args = parser.parse_args()
    runs = args.runs.resolve()
    assert (runs / "manifest.csv").is_file() and (runs / "figures" / "dose_curves.json").is_file()
    all_blocks, included = blocks_from(runs)
    overview(all_blocks, included, runs)
    examples(runs, included)
    verify_example_annotations()
    matrices(included)
    ownership_rows(included, read_json(runs / "robustness" / "pairs.json"))
    print("Exported full-precision plotted values for compiled Figures 2-8")


if __name__ == "__main__":
    main()
