"""k-ablation table: mean L-GED drop per (student, k) for k in {1,3,5}.

Baseline is fixed per (student, case); only the patched graph varies with k.
Baseline source is per-student (parity): GPT-5 from the embedding snapshot, Llama
recomputed from the pinned local baseline (data/outputs/graphs_local). Patched
graphs are the k-tagged outputs from run_patch_injection, per store variant.

Guard: each cell's baseline L-GED must equal the frozen snapshot value (Task 1
pins one generation). Drift fails loudly.

Phase-4 re-pin: baselines are now the COMBINED rule aligner
(embedding_combined_v1). Run with LEX_DRL_RULE_ALIGN unset (combined is the
default) or explicitly =combined. The pre-Phase-4 baselines (embedding_v1,
LEX_DRL_RULE_ALIGN=hybrid) are preserved and still guardable via --snapshot.

Run under the alignment backend the baselines were scored with (embedding):
    LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_k_ablation.py \\
        --variants clean --out results/k_ablation_combined_clean.csv
    # reproduce the pre-Phase-4 (hybrid) baselines instead:
    LEX_DRL_SIMILARITY=embedding LEX_DRL_RULE_ALIGN=hybrid \\
        poetry run python scripts/run_k_ablation.py --snapshot embedding_v1 \\
        --variants clean --out results/k_ablation_clean.csv
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

CASES = ["E2", "M2", "H2"]
KS = [1, 3, 5]
GRAPHS = Path("data/outputs/graphs")
# Per-student baseline source (kept on the same stack as that student's patched runs).
BASELINE = {
    "gpt5": ("snapshot", "embedding_combined_v1"),
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
        return DiscrepancyReport.model_validate_json(p.read_text()).l_ged if p.exists() else None
    p = Path(loc) / f"{case}_agent_{student}.json"
    return _lged(teacher, _load(p)) if p.exists() else None


def _snapshot_lged(student: str, case: str, snapshot: str) -> float | None:
    p = Path("data/snapshots") / snapshot / "discrepancies" / f"{case}_{student}.json"
    return DiscrepancyReport.model_validate_json(p.read_text()).l_ged if p.exists() else None


def _patched_path(case: str, student: str, variant: str, k: int) -> Path:
    suffix = f"_patched_k{k}" if variant == "dirty" else f"_patched_{variant}_k{k}"
    return GRAPHS / f"{case}_agent_{student}{suffix}.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", nargs="+", default=["dirty"],
                    help="store variants: dirty | clean | clean_jfilter")
    ap.add_argument("--out", default="results/k_ablation.csv")
    ap.add_argument("--snapshot", default="embedding_combined_v1",
                    help="baseline snapshot for the guard (Phase-4 re-pin; "
                         "use embedding_v1 with LEX_DRL_RULE_ALIGN=hybrid for the old baselines)")
    ap.add_argument("--no-guard", action="store_true",
                    help="skip the baseline==snapshot assertion (e.g. before Task-1 pinning)")
    args = ap.parse_args()

    console.print(f"[bold]k-ablation[/bold] (alignment={alignment_module.SIMILARITY_METHOD}, "
                  f"threshold={alignment_module.DEFAULT_THRESHOLD}, variants={args.variants})")

    teachers = {c: _load(GRAPHS / f"{c}_reference.json") for c in CASES}

    # baseline per (student, case) — computed once, GUARDED against the snapshot.
    base: dict[tuple[str, str], float | None] = {}
    for student in BASELINE:
        for c in CASES:
            b = _baseline_lged(teachers[c], student, c)
            if b is not None and not args.no_guard:
                snap = _snapshot_lged(student, c, args.snapshot)
                assert snap is not None and abs(b - snap) < 1e-6, (
                    f"BASELINE DRIFT {student}/{c}: ablation={b} vs snapshot={snap} "
                    f"(pin one generation — see docs/BASELINE_PROVENANCE.md)"
                )
            base[(student, c)] = b

    per_case_rows: list[dict] = []
    agg: list[dict] = []
    for variant in args.variants:
        for student in BASELINE:
            for k in KS:
                deltas, present = [], 0
                for c in CASES:
                    b = base[(student, c)]
                    pp = _patched_path(c, student, variant, k)
                    if b is None or not pp.exists():
                        continue
                    patched = _lged(teachers[c], _load(pp))
                    d = patched - b
                    deltas.append(d); present += 1
                    per_case_rows.append({
                        "store": variant, "student": student, "k": k, "case": c,
                        "baseline": round(b, 1), "patched": round(patched, 1),
                        "delta": round(d, 1),
                        "pct_delta": round(100.0 * d / b, 1) if b else 0.0,
                    })
                if deltas:
                    agg.append({"store": variant, "student": student, "k": k,
                                "cases": present, "mean_delta": round(sum(deltas) / len(deltas), 2),
                                "improved": sum(1 for d in deltas if d < 0)})

    # ── Table ──
    table = Table(title="k-ablation — mean L-GED drop (patched − baseline; negative = better)")
    for col in ("store", "Student", "k", "cases", "mean Δ L-GED", "# improved"):
        table.add_column(col, justify="right" if col not in ("store", "Student") else "left")
    for variant in args.variants:
        for student in BASELINE:
            srows = [r for r in agg if r["store"] == variant and r["student"] == student]
            best = min(srows, key=lambda r: r["mean_delta"], default=None) if srows else None
            for r in srows:
                star = " ★" if best and r["k"] == best["k"] else ""
                mark = "green" if r["mean_delta"] < 0 else ("red" if r["mean_delta"] > 0 else "white")
                table.add_row(variant, student, str(r["k"]), str(r["cases"]),
                              f"[{mark}]{r['mean_delta']:+.2f}{star}[/{mark}]", str(r["improved"]))
    console.print(table)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["store", "student", "k", "case",
                                           "baseline", "patched", "delta", "pct_delta"])
        w.writeheader(); w.writerows(per_case_rows)
    console.print(f"\n[bold]Per-case CSV:[/bold] {out} ({len(per_case_rows)} rows)")


if __name__ == "__main__":
    main()
