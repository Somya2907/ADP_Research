"""Full extraction: teacher + all student models on all 6 cases.

Usage:
    poetry run python scripts/run_extraction.py            # all models
    poetry run python scripts/run_extraction.py --teacher  # teacher only
    poetry run python scripts/run_extraction.py --agents   # agents only (gpt5 + qwen3_4b)
    poetry run python scripts/run_extraction.py --gpt5     # GPT-5 agent only
    poetry run python scripts/run_extraction.py --qwen     # Qwen3-4B agent only

Output files:
    data/outputs/graphs/{case_id}_reference.json
    data/outputs/graphs/{case_id}_agent_gpt5.json
    data/outputs/graphs/{case_id}_agent_qwen3_4b.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from rich import print as rprint
from rich.table import Table

from lex_drl.cases import load_all_cases
from lex_drl.extraction import extract_teacher_graph, extract_agent_graph, save_graph

load_dotenv()

AGENT_MODELS = ["gpt5", "qwen3_4b"]


def main():
    parser = argparse.ArgumentParser(description="Extract F-I-R-A-C-O graphs")
    parser.add_argument("--teacher", action="store_true", help="Teacher only")
    parser.add_argument("--agents",  action="store_true", help="All agents only")
    parser.add_argument("--gpt5",    action="store_true", help="GPT-5 agent only")
    parser.add_argument("--qwen",    action="store_true", help="Qwen3-4B agent only")
    args = parser.parse_args()

    run_teacher = not (args.agents or args.gpt5 or args.qwen)
    run_gpt5    = not args.teacher and (args.gpt5 or args.agents or
                  not any([args.teacher, args.agents, args.gpt5, args.qwen]))
    run_qwen    = not args.teacher and (args.qwen or args.agents or
                  not any([args.teacher, args.agents, args.gpt5, args.qwen]))
    if args.gpt5:
        run_gpt5, run_qwen, run_teacher = True, False, False
    if args.qwen:
        run_gpt5, run_qwen, run_teacher = False, True, False
    if args.teacher:
        run_gpt5, run_qwen, run_teacher = False, False, True

    cases = load_all_cases()
    rprint(f"[bold]Loaded {len(cases)} cases[/bold]")
    rprint(f"Running: teacher={run_teacher} gpt5={run_gpt5} qwen3_4b={run_qwen}\n")

    results = Table(title="Extraction Results")
    results.add_column("Case", style="bold")
    results.add_column("Tier")
    results.add_column("Role")
    if run_teacher:
        results.add_column("Teacher", justify="center")
    if run_gpt5:
        results.add_column("GPT-5", justify="center")
    if run_qwen:
        results.add_column("Qwen3-4B", justify="center")

    for case in cases:
        row = [case.case_id, case.tier, case.role]

        if run_teacher:
            try:
                g = extract_teacher_graph(case)
                save_graph(g)
                row.append(f"[green]✓ {g.node_count()}[/green]")
            except Exception as e:
                row.append(f"[red]✗[/red]")
                rprint(f"[red]{case.case_id} teacher FAIL: {e}[/red]")

        if run_gpt5:
            try:
                g = extract_agent_graph(case, model_key="gpt5")
                save_graph(g)
                row.append(f"[green]✓ {g.node_count()}[/green]")
            except Exception as e:
                row.append(f"[red]✗[/red]")
                rprint(f"[red]{case.case_id} gpt5 FAIL: {e}[/red]")

        if run_qwen:
            try:
                g = extract_agent_graph(case, model_key="qwen3_4b")
                save_graph(g)
                row.append(f"[green]✓ {g.node_count()}[/green]")
            except Exception as e:
                row.append(f"[red]✗[/red]")
                rprint(f"[red]{case.case_id} qwen3_4b FAIL: {e}[/red]")

        results.add_row(*row)

    rprint(results)
    rprint("\n[green bold]Extraction complete.[/green bold]")
    rprint("Files saved to data/outputs/graphs/")


if __name__ == "__main__":
    main()
