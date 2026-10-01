"""Collect committed, displayed figure values without reading campaign runs.

These exports are not substitutes for the full-precision cf-transfer summaries.
The source notes in data/plot/ describe the coverage of each panel.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "plot" / "figures"
TABLE_OUT = ROOT / "data" / "plot" / "tables"


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def copy_json(source: str, target: str) -> None:
    destination = OUT / target
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / source, destination)


def seed_bars() -> None:
    macros = json.loads((ROOT / "tables" / "cf_numbers.json").read_text(encoding="utf-8"))["macros"]
    names = {
        "Effusion": "cfSeedWEff",
        "Atelectasis": "cfSeedWAtel",
        "Pneumothorax": "cfSeedWPneu",
        "Cardiomegaly": "cfSeedWCard",
        "Mass": "cfSeedWMass",
        "Nodule": "cfSeedWNodule",
    }
    write_csv(
        OUT / "figure-01" / "panel-c-bars-displayed.csv",
        ["written_direction", "W_effusion_displayed"],
        [{"written_direction": name, "W_effusion_displayed": macros[key]} for name, key in names.items()],
    )
    write_csv(
        OUT / "figure-01" / "panel-c-references-displayed.csv",
        ["reference", "value_displayed"],
        [{"reference": name, "value_displayed": macros[key]} for name, key in (
            ("random_p95", "cfSeedEffRandP"), ("abs_sham", "cfSeedEffSham"),
            ("ownership", "cfSeedEffO"), ("ownership_low", "cfSeedEffOLo"),
            ("ownership_high", "cfSeedEffOHi"),
        )],
    )


def overview_bars() -> None:
    counts = json.loads((ROOT / "figures" / "fig2_counts.json").read_text(encoding="utf-8"))
    rows = []
    for dataset, grades in counts.items():
        for grade, (numerator, denominator) in grades.items():
            rows.append({"dataset": dataset, "grade": grade, "numerator": numerator,
                         "denominator": denominator, "fraction": numerator / denominator})
    assert len(rows) == 9
    write_csv(OUT / "figure-02" / "panel-a-bars.csv",
              ["dataset", "grade", "numerator", "denominator", "fraction"], rows)
    copy_json("figures/fig2_dose_blocks.json", "figure-02/panel-c-block-counts.json")


def overview_landscape() -> None:
    """Extract the 75 displayed, two-decimal Read/Own points from Table 1."""
    source = (ROOT / "tables" / "table_cf_main.tex").read_text(encoding="utf-8")
    rows = []
    inside = False
    for line in source.splitlines():
        if line == r"\midrule":
            inside = True
            continue
        if not inside or line.startswith(r"\textbf{All cells}"):
            if line.startswith(r"\textbf{All cells}"):
                break
            continue
        parts = line.split(" & ")
        if len(parts) != 13 or not line.endswith(r"\\"):
            continue
        for dataset, start in (("nih", 1), ("chexpert", 4), ("coco", 7)):
            read = re.search(r"[+-]?\d+\.\d+", parts[start])
            own = re.search(r"[+-]?\d+\.\d+", parts[start + 2])
            if not read or not own:
                raise ValueError(f"missing displayed Read/Own point: {parts[0]} {dataset}")
            rows.append({"checkpoint": parts[0], "dataset": dataset,
                         "read_displayed": read.group(), "ownership_displayed": own.group()})
    assert len(rows) == 75, len(rows)
    write_csv(OUT / "figure-02" / "panel-b-points-displayed.csv",
              ["checkpoint", "dataset", "read_displayed", "ownership_displayed"], rows)


def ownership_table() -> list[dict]:
    source = (ROOT / "tables" / "table_cf_own.tex").read_text(encoding="utf-8")
    dataset_names = {"NIH ChestX-ray14": "nih", "CheXpert Plus": "chexpert", "COCO": "coco"}
    rows = []
    for section in source.split(r"\begin{table}")[1:]:
        title = re.search(r"Ownership of every concept, ([^.]+)\.", section)
        if not title:
            continue
        dataset = dataset_names[title.group(1)]
        header = next(line for line in section.splitlines() if line.startswith("Checkpoint &"))
        concepts = re.findall(r"\\multicolumn\{1\}\{c\}\{([^}]+)\}", header)
        assert len(concepts) == 6
        for line in section.splitlines():
            cells = line.split(" & ")
            if len(cells) != 7 or not line.endswith(r"\\") or line.startswith("Checkpoint"):
                continue
            if cells[0].startswith("\\"):
                continue
            for concept, cell in zip(concepts, cells[1:]):
                value = re.search(r"[+-]\d+\.\d+", cell)
                if not value:
                    raise ValueError(f"missing displayed ownership: {dataset} {cells[0]} {concept}")
                rows.append({"dataset": dataset, "checkpoint": cells[0], "concept": concept,
                             "ownership_displayed": value.group(), "owned_mark": r"\textbf{" in cell,
                             "verdict_mark": "stronger_competitor" if r"\dagger" in cell
                             else "unresolved" if r"\ddagger" in cell else ""})
    assert len(rows) == 450, len(rows)
    return rows


def reader_heatmap_and_ladders() -> None:
    rows = ownership_table()
    fields = ["dataset", "checkpoint", "concept", "ownership_displayed", "owned_mark", "verdict_mark"]
    reader_models = {"Gemma 3 4B", "Gemma 3 12B", "Gemma 3 27B", "MedGemma 4B", "MedGemma 27B"}
    reader = [r for r in rows if r["checkpoint"] in reader_models]
    assert len(reader) == 90, len(reader)
    write_csv(OUT / "figure-06" / "ownership-displayed.csv", fields, reader)
    ladders = {
        "nih": {"Qwen2.5-VL-3B", "Qwen2.5-VL-7B", "Qwen2.5-VL-32B", "Qwen2.5-VL-72B",
                "Qwen3-VL-4B", "Qwen3-VL-8B", "Qwen3-VL-32B"},
        "chexpert": {"Lingshu 7B", "Lingshu 32B"},
    }
    ladder = [r for r in rows if r["checkpoint"] in ladders.get(r["dataset"], set())]
    assert len(ladder) == 54, len(ladder)
    write_csv(OUT / "figure-07" / "ownership-displayed.csv", fields, ladder)


def tables() -> None:
    """Preserve the exact displayed source of each compiled table separately."""
    sources = [
        "table_cf_main", "table_cf_contingency", "table_cf_models", "table_cf_prevalence",
        "table_cf_coverage", "table_cf_own", "table_cf_own", "table_cf_own",
        "table_cf_controls", "table_cf_ledger", "table_cf_geometry", "table_cf_scale",
        "table_cf_refit", "table_cf_pairs", "table_cf_altdir", "table_cf_ansdir",
        "table_cf_attr", "table_cf_attr_strat", "table_cf_validation", "table_cf_valid",
        "table_cf_towerswap", "table_cf_semend", "table_cf_fgobj", "table_cf_seed",
        "table_seed_mass", "sections/app_prompts", "sections/app_repro", "sections/app_repro",
    ]
    assert len(sources) == 28
    upstream = {
        1: "runs/<model>/<dataset>/summary.json and run.json (75 blocks)",
        2: "runs/manifest.csv",
        3: "per-block summary.json, run.json, template eligibility and preflight; checkpoint metadata",
        4: "runs/_manifests/{nih,coco}/{cohort,labels}.csv; CheXpert source manifests licensed; generator provenance not located",
        5: "runs/manifest.csv",
        6: "per-block summary.json (NIH)",
        7: "per-block summary.json (CheXpert)",
        8: "per-block summary.json (COCO)",
        9: "per-block summary.json",
        10: "per-block summary.json and run.json; runs/robustness/{refit,scale}.json",
        11: "runs/robustness/geometry.json",
        12: "runs/robustness/{scale,round2}.json",
        13: "runs/robustness/refit.json",
        14: "runs/robustness/pairs.json",
        15: "core/altdir/tokenw/extcomp summaries and runs/robustness/round2.json",
        16: "per-block summary.json and runs/robustness/{validation,round2}.json",
        17: "runs/robustness/round2.json (attr)",
        18: "runs/robustness/round2.json (stratified)",
        19: "runs/robustness/validation.json",
        20: "runs/robustness/{round2,validfit}.json",
        21: "towerswap summary.json and run.json",
        22: "semend summary.json and run.json; runs/robustness/round2.json",
        23: "fgobj summary.json and run.json; runs/robustness/round2.json",
        24: "Qwen2.5-VL-7B NIH summary.json and run.json",
        25: "tables/{table_encoding_mass,table_mass_confirmation}.tex (committed formatted source)",
        26: "none; hand-authored notation table",
        27: "tables/cf_numbers.json (committed displayed macros); NIH/COCO manifests in runs/_manifests, CheXpert manifests licensed",
        28: "protocol amendments in code repository docs/external-replication/protocol.json",
    }
    for number, stem in enumerate(sources, 1):
        path = ROOT / (f"{stem}.tex" if stem.startswith("sections/") else f"tables/{stem}.tex")
        source = path.read_text(encoding="utf-8")
        if number in (6, 7, 8):
            source = re.findall(r"\\begin\{table\}.*?\\end\{table\}", source, re.S)[number - 6]
        elif number == 26:
            source = re.search(r"\\begin\{table\}.*?\\end\{table\}", source, re.S).group()
        elif number in (27, 28):
            source = re.findall(r"\\begin\{table\}.*?\\end\{table\}", source, re.S)[number - 27]
        directory = TABLE_OUT / f"table-{number:02d}"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "displayed-source.tex").write_text(source + ("" if source.endswith("\n") else "\n"), encoding="utf-8")
        (directory / "source.txt").write_text(path.relative_to(ROOT).as_posix() + "\n", encoding="utf-8")
        status = ("complete as protocol/notation text" if number in (26, 28)
                  else "displayed values included; CheXpert source manifests remain licensed" if number in (4, 27)
                  else "displayed formatted values included; released campaign inputs are in the code repository")
        (directory / "README.md").write_text(
            f"# Table {number}\n\n"
            f"Source: `{path.relative_to(ROOT).as_posix()}`. "
            "`displayed-source.tex` is the exact table environment used in the compiled manuscript.\n\n"
            f"Status: {status}.\n\n"
            f"Campaign source in the code repository: {upstream[number]}. "
            "See `GUIDE.md` and `REPRODUCING.md` there for the released-data boundary.\n",
            encoding="utf-8",
        )

    contingency = (TABLE_OUT / "table-02" / "displayed-source.tex").read_text(encoding="utf-8")
    rows = []
    group = ""
    for line in contingency.splitlines():
        match = re.fullmatch(r"(.*?) & (met|not met) & (\d+) & (\d+) & (\d+) & (\d+) \\\\ ?", line)
        if match:
            if match.group(1).strip():
                group = match.group(1).strip()
            a, b, c, total = map(int, match.groups()[2:])
            assert a + b + c == total
            rows.append({"cells": group, "steering_reference": match.group(2),
                         "advantage": a, "stronger_competitor": b, "unresolved": c, "total": total})
    assert len(rows) == 6
    write_csv(TABLE_OUT / "table-02" / "displayed-counts.csv",
              ["cells", "steering_reference", "advantage", "stronger_competitor", "unresolved", "total"], rows)

    macros = json.loads((ROOT / "tables" / "cf_numbers.json").read_text(encoding="utf-8"))["macros"]
    roles = (TABLE_OUT / "table-27" / "displayed-source.tex").read_text(encoding="utf-8")
    keys = sorted(set(re.findall(r"\\(cf[A-Za-z0-9]+)\{\}", roles)))
    assert keys and all(key in macros for key in keys)
    (TABLE_OUT / "table-27" / "displayed-macros.json").write_text(
        json.dumps({key: macros[key] for key in keys}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    seed_bars()
    overview_bars()
    overview_landscape()
    reader_heatmap_and_ladders()
    copy_json("figures/fig3_example.json", "figure-04/reported-values.json")
    copy_json("figures/figA1_own_share.json", "figure-03/flow-marginals.json")
    tables()


if __name__ == "__main__":
    main()
