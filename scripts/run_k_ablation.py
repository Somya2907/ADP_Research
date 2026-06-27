"""Task 6 — k-ablation table: mean L-GED drop per (student, k) for k in {1,3,5}.

Baseline is fixed per (student, case); only the patched graph varies with k.
Baseline source is per-student (parity): GPT-5 from the cloud embedding snapshot,
Llama from the locally-extracted baseline (data/outputs/graphs_local). Patched
graphs are the k-tagged outputs from run_patch_injection.

Run under the alignment backend the baselines were scored with (embedding):
    LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_k_ablation.py
"""
from __future__ import annotations

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

CASES = ["E2", "M2", "H2"]
KS = [1, 3, 5]
GRAPHS = Path("data/outputs/graphs")
# Per-student baseline source (kept on the same stack as that student's patched runs).
BASELINE = {
    "gpt5": ("snapshot", "embedding_v1"),
    "llama3_2b": ("local", "data/outputs/graphs_local"),
}


def _load(p: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(p.read_text())


def _lged(teacher, graph) -> float:
    return compute_discrepancies(teacher, graph, align_all(teacher, graph)).l_ged


def _baseline_lged(teacher, student: str, case: str) -> float | None:
    mode, loc = BASELINE[student]
    if mode == "snapshot":
        p = Path("data/snapshots") / loc / "discrepancies" / f"{case}_{student}.json"
        if not p.exists():
            return None
        return DiscrepancyReport.model_validate_json(p.read_text()).l_ged
    p = Path(loc) / f"{case}_agent_{student}.json"
    return _lged(teacher, _load(p)) if p.exists() else None


def main() -> None:
    console.print(f"[bold]k-ablation[/bold] (alignment={alignment_module.SIMILARITY_METHOD}, "
                  f"threshold={alignment_module.DEFAULT_THRESHOLD})")

    teachers = {c: _load(GRAPHS / f"{c}_reference.json") for c in CASES}
    # baseline per (student, case) — computed once, reused across k
    base = {}
    for student in BASELINE:
        for c in CASES:
            base[(student, c)] = _baseline_lged(teachers[c], student, c)

    rows: list[dict] = []
    per_case_rows: list[dict] = []
    for student in BASELINE:
        for k in KS:
            deltas, present = [], 0
            for c in CASES:
                b = base[(student, c)]
                pp = GRAPHS / f"{c}_agent_{student}_patched_k{k}.json"
                if b is None or not pp.exists():
                    continue
                patched = _lged(teachers[c], _load(pp))
                d = patched - b
                deltas.append(d); present += 1
                per_case_rows.append({"student": student, "k": k, "case": c,
                                      "baseline": round(b, 1), "patched": round(patched, 1),
                                      "delta": round(d, 1)})
            if deltas:
                mean_d = sum(deltas) / len(deltas)
                rows.append({"student": student, "k": k, "cases": present,
                             "mean_delta": round(mean_d, 2),
                             "improved": sum(1 for d in deltas if d < 0)})

    # ── Table ──
    table = Table(title="k-ablation — mean L-GED drop (patched − baseline; negative = better)")
    for col in ("Student", "k", "cases", "mean Δ L-GED", "# improved"):
        table.add_column(col, justify="right" if col != "Student" else "left")
    for student in BASELINE:
        srows = [r for r in rows if r["student"] == student]
        best = min(srows, key=lambda r: r["mean_delta"], default=None) if srows else None
        for r in srows:
            star = " ★" if best and r["k"] == best["k"] else ""
            mark = "green" if r["mean_delta"] < 0 else ("red" if r["mean_delta"] > 0 else "white")
            table.add_row(r["student"], str(r["k"]), str(r["cases"]),
                          f"[{mark}]{r['mean_delta']:+.2f}{star}[/{mark}]", str(r["improved"]))
    console.print(table)

    for student in BASELINE:
        srows = [r for r in rows if r["student"] == student]
        if srows:
            best = min(srows, key=lambda r: r["mean_delta"])
            console.print(f"  best k for [bold]{student}[/bold]: "
                          f"k={best['k']} (mean Δ {best['mean_delta']:+.2f})")

    out = Path("results") / "k_ablation.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["student", "k", "case", "baseline", "patched", "delta"])
        w.writeheader(); w.writerows(per_case_rows)
    console.print(f"\n[bold]Per-case CSV:[/bold] {out}")


if __name__ == "__main__":
    main()
