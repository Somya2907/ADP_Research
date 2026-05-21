"""Calibrate the TF-IDF alignment threshold for legal text.

Sweeps threshold values on E1 (ground-truth calibration case) and reports
which threshold satisfies all three calibration criteria:
  1. v_miss ≈ 18–22 for E1/gpt5
  2. v_halluc < 10 for E1/gpt5
  3. gpt5 L-GED < llama L-GED (the model ranking should be correct)

Ground truth from manual analysis: E1/gpt5 should have ~20 v_miss.

Usage:
    poetry run python scripts/calibrate_threshold.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.table import Table

import lex_drl.alignment as alignment_module
from lex_drl.discrepancy import compute_discrepancies
from lex_drl.alignment import align_all
from lex_drl.schema import LegalReasoningGraph

console = Console()

GRAPHS_DIR = Path("data/outputs/graphs")
CASE_ID = "E1"
THRESHOLDS = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
CALIBRATION_TARGETS = {
    "v_miss_min": 18,
    "v_miss_max": 22,
    "v_halluc_max": 10,
}


def load_graph(path: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(path.read_text())


def run_calibration():
    console.print(f"\n[bold cyan]Calibrating TF-IDF threshold on {CASE_ID}[/bold cyan]\n")

    teacher = load_graph(GRAPHS_DIR / f"{CASE_ID}_reference.json")
    gpt5_graph = load_graph(GRAPHS_DIR / f"{CASE_ID}_agent_gpt5.json")
    llama_graph = load_graph(GRAPHS_DIR / f"{CASE_ID}_agent_qwen3_4b.json")

    table = Table(title="Threshold calibration sweep")
    table.add_column("Threshold", justify="right")
    table.add_column("GPT-5 v_miss", justify="right")
    table.add_column("GPT-5 v_halluc", justify="right")
    table.add_column("GPT-5 L-GED", justify="right")
    table.add_column("Llama L-GED", justify="right")
    table.add_column("GPT > Llama?", justify="center")
    table.add_column("Calibration match", justify="center")

    results = []
    for threshold in THRESHOLDS:
        # Temporarily override the threshold.
        orig_threshold = alignment_module.DEFAULT_THRESHOLD
        alignment_module.DEFAULT_THRESHOLD = threshold

        try:
            # Align and score both students.
            gpt5_alignment = align_all(teacher, gpt5_graph, threshold=threshold)
            gpt5_report = compute_discrepancies(teacher, gpt5_graph, gpt5_alignment)

            llama_alignment = align_all(teacher, llama_graph, threshold=threshold)
            llama_report = compute_discrepancies(teacher, llama_graph, llama_alignment)

            gpt5_vmiss = gpt5_report.v_miss_count
            gpt5_vhalluc = gpt5_report.v_halluc_count
            gpt5_lged = gpt5_report.l_ged
            llama_lged = llama_report.l_ged

            # Check calibration criteria.
            vmiss_ok = CALIBRATION_TARGETS["v_miss_min"] <= gpt5_vmiss <= CALIBRATION_TARGETS["v_miss_max"]
            vhalluc_ok = gpt5_vhalluc < CALIBRATION_TARGETS["v_halluc_max"]
            ranking_ok = gpt5_lged < llama_lged
            all_ok = vmiss_ok and vhalluc_ok and ranking_ok

            gpt_gt_llama = "✗" if gpt5_lged < llama_lged else "✓"
            calib_marker = "[green]✓[/green]" if all_ok else "[red]✗[/red]"

            table.add_row(
                f"{threshold:.2f}",
                str(gpt5_vmiss),
                str(gpt5_vhalluc),
                f"{gpt5_lged:.1f}",
                f"{llama_lged:.1f}",
                gpt_gt_llama,
                calib_marker,
            )

            results.append({
                "threshold": threshold,
                "gpt5_vmiss": gpt5_vmiss,
                "gpt5_vhalluc": gpt5_vhalluc,
                "gpt5_lged": gpt5_lged,
                "llama_lged": llama_lged,
                "vmiss_ok": vmiss_ok,
                "vhalluc_ok": vhalluc_ok,
                "ranking_ok": ranking_ok,
                "all_ok": all_ok,
            })

        finally:
            # Restore original threshold.
            alignment_module.DEFAULT_THRESHOLD = orig_threshold

    console.print(table)

    # Recommendation.
    console.print("\n[bold]Calibration criteria:[/bold]")
    console.print(f"  • v_miss ∈ [{CALIBRATION_TARGETS['v_miss_min']}, {CALIBRATION_TARGETS['v_miss_max']}]")
    console.print(f"  • v_halluc < {CALIBRATION_TARGETS['v_halluc_max']}")
    console.print("  • GPT-5 L-GED < Llama L-GED (✗ in table = better)")

    passing = [r for r in results if r["all_ok"]]
    if passing:
        best = passing[0]
        console.print(f"\n[bold green]✓ Recommendation: threshold = {best['threshold']:.2f}[/bold green]")
        console.print(f"  v_miss={best['gpt5_vmiss']}, v_halluc={best['gpt5_vhalluc']}, "
                      f"GPT-5 L-GED={best['gpt5_lged']:.1f} vs Llama={best['llama_lged']:.1f}")
    else:
        console.print("\n[yellow]⚠ No threshold fully satisfies all criteria.[/yellow]")
        console.print("   Closest match:")
        # Sort by (vmiss_ok, vhalluc_ok, ranking_ok, then by how close v_miss is).
        best = max(results, key=lambda r: (r["vmiss_ok"], r["vhalluc_ok"], r["ranking_ok"]))
        console.print(f"  threshold = {best['threshold']:.2f} (v_miss={best['gpt5_vmiss']}, "
                      f"v_halluc={best['gpt5_vhalluc']}, GPT={best['gpt5_lged']:.1f} vs Llama={best['llama_lged']:.1f})")


if __name__ == "__main__":
    run_calibration()
