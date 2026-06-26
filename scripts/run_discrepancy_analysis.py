"""Run the discrepancy scorer across every (case, student) pair.

For each of the 6 cases × 2 students, load the teacher and student graphs,
compute alignment + discrepancy, and write one report per pair to
``data/outputs/discrepancies/{case_id}_{student}.json``.

Also writes a summary CSV at ``results/discrepancy_summary.csv`` with one row
per (case, student) and columns:
``case_id, student, v_miss_count, v_halluc_count, e_diff_count,
v_misground_count, l_ged_score``.

Usage:
    poetry run python scripts/run_discrepancy_analysis.py
    poetry run python scripts/run_discrepancy_analysis.py --case E1
    poetry run python scripts/run_discrepancy_analysis.py --student gpt5
    poetry run python scripts/run_discrepancy_analysis.py --force   # overwrite
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.table import Table

from lex_drl.alignment import align_all
from lex_drl.discrepancy import (
    DiscrepancyReport,
    _default_validity_check,
    compute_discrepancies,
    make_statute_validity_check,
)
from lex_drl.schema import LegalReasoningGraph
from lex_drl.statute_index import load_statute_index, make_section_exists_fn

console = Console()

GRAPHS_DIR = Path("data/outputs/graphs")
DISCREPANCIES_DIR = Path("data/outputs/discrepancies")
RESULTS_DIR = Path("results")
SUMMARY_CSV = RESULTS_DIR / "discrepancy_summary.csv"

CASES = ["E1", "E2", "M1", "M2", "H1", "H2"]
STUDENTS = ["gpt5", "llama3_2b"]


def load_graph(path: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(path.read_text())


def out_path_for(case_id: str, student: str) -> Path:
    return DISCREPANCIES_DIR / f"{case_id}_{student}.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES, help="run on a single case")
    parser.add_argument("--student", choices=STUDENTS, help="run on a single student")
    parser.add_argument("--force", action="store_true",
                        help="overwrite existing reports (default: skip)")
    parser.add_argument("--graphs-dir", default=str(GRAPHS_DIR))
    parser.add_argument("--out-dir", default=str(DISCREPANCIES_DIR))
    parser.add_argument("--summary-csv", default=str(SUMMARY_CSV))
    args = parser.parse_args()

    graphs_dir = Path(args.graphs_dir)
    out_dir = Path(args.out_dir)
    summary_csv = Path(args.summary_csv)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_csv.parent.mkdir(parents=True, exist_ok=True)

    case_ids = [args.case] if args.case else CASES
    student_ids = [args.student] if args.student else STUDENTS

    # Statute-grounded validity check + misgrounding subtype, gated on a
    # provenance-confirmed index. make_section_exists_fn returns None when the
    # index is untrustworthy (e.g. DCWP rules MISSING / TX summary), in which
    # case we fall back to the default validity check and leave the subtype
    # unset — so an incomplete corpus never drives a false "fabricated" verdict.
    section_exists_fn = make_section_exists_fn(load_statute_index())
    if section_exists_fn is not None:
        validity_check = make_statute_validity_check(section_exists_fn)
        console.print("[green]statute index trustworthy[/green] — "
                      "statute-grounded v_halluc + misgrounding subtype ENABLED")
    else:
        validity_check = _default_validity_check
        console.print("[yellow]statute index untrustworthy or absent[/yellow] — "
                      "using default validity check; misgrounding subtype unset "
                      "(see data/statutes/index/PROVENANCE_AUDIT.md)")

    table = Table(title="Discrepancy summary")
    for col in ("Case", "Student", "v_miss", "v_halluc", "e_diff", "v_misg", "L-GED"):
        table.add_column(col, justify="right" if col != "Case" else "left")

    rows: list[dict[str, object]] = []
    errors: list[str] = []

    for case_id in case_ids:
        teacher_path = graphs_dir / f"{case_id}_reference.json"
        if not teacher_path.exists():
            errors.append(f"{case_id}: missing teacher graph at {teacher_path}")
            continue
        teacher = load_graph(teacher_path)

        for student in student_ids:
            student_path = graphs_dir / f"{case_id}_agent_{student}.json"
            if not student_path.exists():
                errors.append(f"{case_id}/{student}: missing {student_path}")
                continue

            target = out_dir / f"{case_id}_{student}.json"
            if target.exists() and not args.force:
                console.print(f"[yellow]skip[/yellow] {target.name} (use --force to overwrite)")
                report = DiscrepancyReport.model_validate_json(target.read_text())
            else:
                student_graph = load_graph(student_path)
                alignment = align_all(teacher, student_graph)
                report = compute_discrepancies(
                    teacher, student_graph, alignment,
                    validity_check=validity_check,
                    section_exists_fn=section_exists_fn,
                )
                target.write_text(report.model_dump_json(indent=2))
                console.print(f"[green]wrote[/green] {target}")

            row = {
                "case_id": case_id,
                "student": student,
                "v_miss_count": report.v_miss_count,
                "v_halluc_count": report.v_halluc_count,
                "e_diff_count": report.e_diff_count,
                "v_misground_count": report.v_misground_count,
                "l_ged_score": round(report.l_ged, 4),
            }
            rows.append(row)
            table.add_row(
                case_id, student,
                str(report.v_miss_count), str(report.v_halluc_count),
                str(report.e_diff_count), str(report.v_misground_count),
                f"{report.l_ged:.2f}",
            )

    # Write summary CSV.
    if rows:
        with summary_csv.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=[
                "case_id", "student", "v_miss_count", "v_halluc_count",
                "e_diff_count", "v_misground_count", "l_ged_score",
            ])
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        console.print(f"\n[bold]Summary CSV:[/bold] {summary_csv}")

    console.print(table)

    if errors:
        console.print("\n[red]Errors:[/red]")
        for e in errors:
            console.print(f"  • {e}")

    # Sanity sketch: ensure L-GED is non-negative & finite.
    bad = [r for r in rows if not (r["l_ged_score"] >= 0)]
    if bad:
        console.print(f"[red]Sanity check failed: {len(bad)} negative scores[/red]")
        sys.exit(2)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
