"""Day 2 wide run: teacher + agent on all 6 cases.

Usage:
    poetry run python scripts/run_extraction.py

Runs all 6 cases through both teacher and agent, saving graphs and raw
responses. Cached responses are reused automatically — clear .cache/ to
force fresh calls.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from rich import print as rprint
from rich.table import Table

from lex_drl.cases import load_all_cases
from lex_drl.extraction import extract_agent_graph, extract_teacher_graph, save_graph

load_dotenv()


def main():
    cases = load_all_cases()
    rprint(f"[bold]Loaded {len(cases)} cases[/bold]\n")

    results = Table(title="Extraction Results")
    results.add_column("Case", style="bold")
    results.add_column("Tier")
    results.add_column("Role")
    results.add_column("Teacher", justify="center")
    results.add_column("Agent", justify="center")
    results.add_column("Δ Nodes", justify="center")

    for case in cases:
        teacher_ok, agent_ok = False, False
        t_nodes, a_nodes = 0, 0

        # Teacher
        try:
            g_ref = extract_teacher_graph(case)
            save_graph(g_ref)
            teacher_ok = True
            t_nodes = g_ref.node_count()
        except Exception as e:
            rprint(f"[red]{case.case_id} teacher FAIL: {e}[/red]")

        # Agent
        try:
            g_agent = extract_agent_graph(case)
            save_graph(g_agent)
            agent_ok = True
            a_nodes = g_agent.node_count()
        except Exception as e:
            rprint(f"[red]{case.case_id} agent FAIL: {e}[/red]")

        t_status = f"[green]✓ {t_nodes}[/green]" if teacher_ok else "[red]✗[/red]"
        a_status = f"[green]✓ {a_nodes}[/green]" if agent_ok else "[red]✗[/red]"
        delta = ""
        if teacher_ok and agent_ok:
            d = t_nodes - a_nodes
            if d > 0:
                delta = f"[yellow]-{d}[/yellow]"
            elif d < 0:
                delta = f"[yellow]+{abs(d)}[/yellow]"
            else:
                delta = "[dim]0[/dim]"

        results.add_row(case.case_id, case.tier, case.role, t_status, a_status, delta)

    rprint(results)
    rprint("\n[green bold]All extractions complete.[/green bold]")
    rprint("Next: hand-inspect data/outputs/graphs/ and data/outputs/analysis/")


if __name__ == "__main__":
    main()
