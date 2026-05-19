"""End-to-end experiment sweep: extraction + discrepancy scoring + summary.

For each case × student in the experiment matrix:

  1. Run teacher extraction (cache hit if already done; skipped if reference
     graph file already exists on disk and ``--force`` was not passed).
  2. Run baseline student extraction (same skip rule).
  3. Compute alignment + discrepancy report vs the teacher.
  4. Save the discrepancy JSON and (after all rows) a CSV summary.

Resume-from-checkpoint: any file the script would produce that already
exists is left untouched unless ``--force`` is passed. The cached LLM
responses provide a second layer of resume-from-checkpoint at the API
level (see ``src/lex_drl/cache.py``).

Usage:
    poetry run python scripts/run_full_sweep.py
    poetry run python scripts/run_full_sweep.py --force
    poetry run python scripts/run_full_sweep.py --case E1 --student gpt5
    poetry run python scripts/run_full_sweep.py --no-extract     # use existing graphs
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from lex_drl.alignment import align_all
from lex_drl.cases import load_case
from lex_drl.discrepancy import DiscrepancyReport, compute_discrepancies
from lex_drl.extraction import extract_agent_graph, extract_teacher_graph, save_graph
from lex_drl.schema import LegalReasoningGraph

load_dotenv()
console = Console()

CASES = ["E1", "E2", "M1", "M2", "H1", "H2"]
STUDENTS = ["gpt5", "qwen3_4b"]

GRAPHS_DIR = Path("data/outputs/graphs")
DISCREPANCIES_DIR = Path("data/outputs/discrepancies")
RESULTS_DIR = Path("results")
SUMMARY_CSV = RESULTS_DIR / "sweep_summary.csv"


def graph_path(case_id: str, kind: str) -> Path:
    """``kind`` is 'reference' or one of the student IDs."""
    if kind == "reference":
        return GRAPHS_DIR / f"{case_id}_reference.json"
    return GRAPHS_DIR / f"{case_id}_agent_{kind}.json"


def discrepancy_path(case_id: str, student: str) -> Path:
    return DISCREPANCIES_DIR / f"{case_id}_{student}.json"


def load_or_extract_teacher(case_id: str, no_extract: bool, force: bool) -> LegalReasoningGraph:
    path = graph_path(case_id, "reference")
    if path.exists() and not force:
        return LegalReasoningGraph.model_validate_json(path.read_text())
    if no_extract:
        raise FileNotFoundError(f"--no-extract set but missing {path}")
    case = load_case(case_id)
    graph = extract_teacher_graph(case)
    save_graph(graph)
    return graph


def load_or_extract_student(case_id: str, student: str, no_extract: bool, force: bool) -> LegalReasoningGraph:
    path = graph_path(case_id, student)
    if path.exists() and not force:
        return LegalReasoningGraph.model_validate_json(path.read_text())
    if no_extract:
        raise FileNotFoundError(f"--no-extract set but missing {path}")
    case = load_case(case_id)
    graph = extract_agent_graph(case, model_key=student)
    save_graph(graph)
    return graph


def load_or_compute_discrepancy(
    teacher: LegalReasoningGraph,
    student_graph: LegalReasoningGraph,
    case_id: str,
    student: str,
    force: bool,
) -> DiscrepancyReport:
    path = discrepancy_path(case_id, student)
    if path.exists() and not force:
        return DiscrepancyReport.model_validate_json(path.read_text())
    alignment = align_all(teacher, student_graph)
    report = compute_discrepancies(teacher, student_graph, alignment)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report.model_dump_json(indent=2))
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES, help="single case")
    parser.add_argument("--student", choices=STUDENTS, help="single student")
    parser.add_argument("--force", action="store_true",
                        help="overwrite all artifacts (graphs + discrepancies)")
    parser.add_argument("--no-extract", action="store_true",
                        help="never call models; use existing graph files only")
    parser.add_argument("--summary-csv", default=str(SUMMARY_CSV))
    args = parser.parse_args()

    cases = [args.case] if args.case else CASES
    students = [args.student] if args.student else STUDENTS
    total_steps = len(cases) * (1 + len(students))

    rows: list[dict[str, object]] = []
    errors: list[str] = []
    start = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Sweep", total=total_steps)

        for case_id in cases:
            try:
                teacher = load_or_extract_teacher(case_id, args.no_extract, args.force)
                progress.update(task, advance=1, description=f"{case_id} teacher")
            except Exception as e:
                errors.append(f"{case_id} teacher: {e}")
                progress.update(task, advance=1 + len(students),
                                description=f"{case_id} skipped")
                continue

            for student in students:
                try:
                    student_graph = load_or_extract_student(case_id, student,
                                                            args.no_extract, args.force)
                    report = load_or_compute_discrepancy(
                        teacher, student_graph, case_id, student, args.force,
                    )
                    rows.append({
                        "case_id": case_id,
                        "student": student,
                        "teacher_nodes": teacher.node_count(),
                        "student_nodes": student_graph.node_count(),
                        "v_miss_count": report.v_miss_count,
                        "v_halluc_count": report.v_halluc_count,
                        "e_diff_count": report.e_diff_count,
                        "l_ged_score": round(report.l_ged, 4),
                    })
                except Exception as e:
                    errors.append(f"{case_id}/{student}: {e}")
                progress.update(task, advance=1,
                                description=f"{case_id} · {student}")

    # Write summary CSV.
    Path(args.summary_csv).parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(args.summary_csv, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        console.print(f"\n[bold]Summary CSV:[/bold] {args.summary_csv}")

    # Final table.
    table = Table(title="Sweep summary")
    for col in ("Case", "Student", "T-nodes", "S-nodes", "v_miss", "v_halluc",
                "e_diff", "L-GED"):
        table.add_column(col, justify="right" if col != "Case" else "left")
    for r in rows:
        table.add_row(
            str(r["case_id"]), str(r["student"]),
            str(r["teacher_nodes"]), str(r["student_nodes"]),
            str(r["v_miss_count"]), str(r["v_halluc_count"]),
            str(r["e_diff_count"]), f"{r['l_ged_score']:.2f}",
        )
    console.print(table)
    console.print(f"\nElapsed: {time.time() - start:.1f}s")

    if errors:
        console.print("[red]Errors:[/red]")
        for e in errors:
            console.print(f"  • {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
