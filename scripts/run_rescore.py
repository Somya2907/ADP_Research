"""Task 6: re-score patched student graphs and tabulate before/after L-GED.

For each test case (E2/M2/H2) and student, compute the discrepancy of the
*patched* graph against the teacher using the SAME pipeline as the baseline
(align_all + compute_discrepancies), then compare to the baseline (unpatched)
L-GED from the snapshot. Lower L-GED = closer to teacher = better; a negative
delta means the patch helped.

Run under the alignment backend the baseline was scored with (embedding):
    LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_rescore.py
    LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_rescore.py --k 3

Patched graphs are read from data/outputs/graphs/{case}_agent_{student}_patched[_k{k}].json
(the _k suffix is used when the k-ablation has tagged outputs; falls back to the
untagged name otherwise). Baselines come from data/snapshots/{snapshot}/.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.table import Table

import lex_drl.alignment as alignment_module
from lex_drl.alignment import align_all
from lex_drl.discrepancy import DiscrepancyReport, compute_discrepancies
from lex_drl.schema import LegalReasoningGraph

console = Console()

TEST_CASES = ["E2", "M2", "H2"]
GRAPHS_DIR = Path("data/outputs/graphs")
RESULTS_DIR = Path("results")


def _load_graph(p: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(p.read_text())


def _patched_path(case: str, student: str, k: int | None) -> Path | None:
    """Prefer the k-tagged name; fall back to the untagged one."""
    if k is not None:
        tagged = GRAPHS_DIR / f"{case}_agent_{student}_patched_k{k}.json"
        if tagged.exists():
            return tagged
    untagged = GRAPHS_DIR / f"{case}_agent_{student}_patched.json"
    return untagged if untagged.exists() else None


def _baseline_lged(snapshot: str, case: str, student: str) -> dict | None:
    path = Path("data/snapshots") / snapshot / "discrepancies" / f"{case}_{student}.json"
    if not path.exists():
        return None
    r = DiscrepancyReport.model_validate_json(path.read_text())
    return {"v_miss": r.v_miss_count, "v_halluc": r.v_halluc_count,
            "e_diff": r.e_diff_count, "l_ged": r.l_ged}


def _baseline_from_graph(teacher, graphs_dir: Path, case: str, student: str) -> dict | None:
    """Compute baseline discrepancy fresh from an unpatched graph (same pipeline
    as the patched scoring) — for clean local-baseline vs local-patched parity."""
    path = graphs_dir / f"{case}_agent_{student}.json"
    if not path.exists():
        return None
    g = _load_graph(path)
    r = compute_discrepancies(teacher, g, align_all(teacher, g))
    return {"v_miss": r.v_miss_count, "v_halluc": r.v_halluc_count,
            "e_diff": r.e_diff_count, "l_ged": r.l_ged}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--students", nargs="+", default=["gpt5", "llama3_2b"])
    ap.add_argument("--cases", nargs="+", default=TEST_CASES)
    ap.add_argument("--k", type=int, default=None, help="k used for injection (for k-tagged graphs)")
    ap.add_argument("--snapshot", default="embedding_v1", help="baseline snapshot dir")
    ap.add_argument("--baseline-graphs-dir", default=None,
                    help="compute baseline fresh from unpatched graphs here (e.g. "
                         "data/outputs/graphs_local) instead of reading the snapshot — "
                         "use for local-baseline vs local-patched parity")
    args = ap.parse_args()

    baseline_src = args.baseline_graphs_dir or f"snapshot:{args.snapshot}"
    console.print(f"[bold]Re-scoring patched graphs[/bold] "
                  f"(alignment={alignment_module.SIMILARITY_METHOD}, "
                  f"threshold={alignment_module.DEFAULT_THRESHOLD}, baseline={baseline_src})")

    table = Table(title=f"Before → after L-GED (patched, k={args.k or 'untagged'})")
    for col in ("Case", "Student", "baseline L-GED", "patched L-GED", "Δ", "% drop"):
        table.add_column(col, justify="right" if col not in ("Case", "Student") else "left")

    rows: list[dict] = []
    missing: list[str] = []
    for case_id in args.cases:
        teacher_path = GRAPHS_DIR / f"{case_id}_reference.json"
        if not teacher_path.exists():
            missing.append(f"{case_id}: teacher graph"); continue
        teacher = _load_graph(teacher_path)
        for student in args.students:
            patched_path = _patched_path(case_id, student, args.k)
            if args.baseline_graphs_dir:
                base = _baseline_from_graph(teacher, Path(args.baseline_graphs_dir), case_id, student)
            else:
                base = _baseline_lged(args.snapshot, case_id, student)
            if patched_path is None:
                missing.append(f"{case_id}/{student}: patched graph"); continue
            if base is None:
                missing.append(f"{case_id}/{student}: baseline"); continue

            patched_graph = _load_graph(patched_path)
            alignment = align_all(teacher, patched_graph)
            rep = compute_discrepancies(teacher, patched_graph, alignment)
            delta = rep.l_ged - base["l_ged"]
            pct = (delta / base["l_ged"] * 100.0) if base["l_ged"] else 0.0
            color = "green" if delta < 0 else ("red" if delta > 0 else "white")
            table.add_row(
                case_id, student, f"{base['l_ged']:.1f}", f"{rep.l_ged:.1f}",
                f"[{color}]{delta:+.1f}[/{color}]", f"[{color}]{pct:+.1f}%[/{color}]",
            )
            rows.append({
                "case_id": case_id, "student": student, "k": args.k or "",
                "baseline_l_ged": base["l_ged"], "patched_l_ged": rep.l_ged,
                "delta_l_ged": round(delta, 2), "pct_drop": round(pct, 1),
                "baseline_v_miss": base["v_miss"], "patched_v_miss": rep.v_miss_count,
                "baseline_v_halluc": base["v_halluc"], "patched_v_halluc": rep.v_halluc_count,
                "baseline_e_diff": base["e_diff"], "patched_e_diff": rep.e_diff_count,
            })

    console.print(table)
    if rows:
        improved = sum(1 for r in rows if r["delta_l_ged"] < 0)
        mean_delta = sum(r["delta_l_ged"] for r in rows) / len(rows)
        console.print(f"\n[bold]{improved}/{len(rows)}[/bold] patched runs improved "
                      f"(lower L-GED); mean Δ = [bold]{mean_delta:+.1f}[/bold]")
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        out = RESULTS_DIR / (f"rescore_k{args.k}.csv" if args.k else "rescore.csv")
        with out.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        console.print(f"[bold]CSV:[/bold] {out}")
    if missing:
        console.print("\n[yellow]Missing (skipped):[/yellow]")
        for m in missing:
            console.print(f"  • {m}")


if __name__ == "__main__":
    main()
