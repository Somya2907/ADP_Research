"""Mine reusable patches from the training-case discrepancy snapshots.

Task 4 mining driver (Phase 2). Assembles
``(report, teacher_graph, student_graph, case)`` tuples for the training cases
(E1/M1/H1) × both students from a discrepancy snapshot + the frozen graphs,
runs ``patch_generator.generate_all`` (deterministic; ``insight=None``), and
saves the deduped patch store to ``data/patches/patches.json``.

Deterministic-only this phase — no API calls. The default snapshot is
``embedding_v1`` (the primary alignment backend; see docs/ALIGNMENT_METHODS.md).

Usage:
    poetry run python scripts/run_patch_mining.py
    poetry run python scripts/run_patch_mining.py --snapshot tfidf_v1
    poetry run python scripts/run_patch_mining.py --out data/patches/patches.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.table import Table

from lex_drl.cases import load_all_cases
from lex_drl.discrepancy import DiscrepancyReport
from lex_drl.patch_generator import generate_all
from lex_drl.patch_store import PatchStore
from lex_drl.schema import LegalReasoningGraph

console = Console()

TRAINING = ["E1", "M1", "H1"]          # train-only: patches mined here, injected on test cases
STUDENTS = ["gpt5", "llama3_2b"]
GRAPHS_DIR = Path("data/outputs/graphs")
SNAPSHOTS_DIR = Path("data/snapshots")
DEFAULT_OUT = Path("data/patches/patches.json")


def _load_graph(path: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(path.read_text())


def _load_report(path: Path) -> DiscrepancyReport:
    return DiscrepancyReport.model_validate_json(path.read_text())


def main() -> None:
    ap = argparse.ArgumentParser(description="Mine patches from training discrepancies")
    ap.add_argument("--snapshot", default="embedding_v1",
                    help="snapshot under data/snapshots/ to mine (default: embedding_v1)")
    ap.add_argument("--graphs-dir", default=str(GRAPHS_DIR))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    disc_dir = SNAPSHOTS_DIR / args.snapshot / "discrepancies"
    graphs_dir = Path(args.graphs_dir)
    out_path = Path(args.out)
    if not disc_dir.is_dir():
        console.print(f"[red]No discrepancy snapshot at {disc_dir}[/red]")
        raise SystemExit(1)

    cases_by_id = {c.case_id: c for c in load_all_cases()}

    # Assemble (report, teacher, student, case) tuples — training cases × students.
    tuples = []
    skipped: list[str] = []
    for case_id in TRAINING:
        case = cases_by_id.get(case_id)
        if case is None:
            skipped.append(f"{case_id}: case file missing")
            continue
        if case.role != "training":   # defensive — generator enforces this too
            skipped.append(f"{case_id}: role={case.role!r} (not training)")
            continue
        teacher_path = graphs_dir / f"{case_id}_reference.json"
        if not teacher_path.exists():
            skipped.append(f"{case_id}: teacher graph missing")
            continue
        teacher = _load_graph(teacher_path)
        for student in STUDENTS:
            report_path = disc_dir / f"{case_id}_{student}.json"
            student_path = graphs_dir / f"{case_id}_agent_{student}.json"
            if not report_path.exists() or not student_path.exists():
                skipped.append(f"{case_id}/{student}: report or graph missing")
                continue
            tuples.append((
                _load_report(report_path), teacher,
                _load_graph(student_path), case,
            ))

    console.print(f"[bold]Mining {len(tuples)} (case, student) reports "
                  f"from snapshot '{args.snapshot}'[/bold] (insight=None, deterministic)")

    patches = generate_all(tuples, insight=None)

    store = PatchStore()
    store.populate_from_candidates(patches)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    store.save(out_path)

    # ── Summary ──
    by_family: dict[str, int] = {}
    for p in store.all():
        by_family[p.patch_family] = by_family.get(p.patch_family, 0) + 1

    table = Table(title=f"Mined patches → {out_path}")
    for col in ("patch_id", "family", "authority", "juris", "src_cases", "#kw"):
        table.add_column(col, overflow="fold")
    for p in sorted(store.all(), key=lambda x: (x.patch_family, x.controlling_authority)):
        table.add_row(
            p.patch_id, p.patch_family, p.controlling_authority[:42],
            p.jurisdiction, ",".join(p.source_cases), str(len(p.trigger_keywords)),
        )
    console.print(table)
    console.print(f"\n[green bold]{len(store)} patches[/green bold] "
                  f"({', '.join(f'{k}={v}' for k, v in sorted(by_family.items()))}) "
                  f"→ {out_path}")
    if skipped:
        console.print("\n[yellow]Skipped:[/yellow]")
        for s in skipped:
            console.print(f"  • {s}")


if __name__ == "__main__":
    main()
