"""Day 1 smoke test: run teacher + agent on Case E1 only.

Usage:
    poetry run python scripts/smoke_test_e1.py

Expected outcome:
  - Teacher (Claude Opus 4.6) produces G_ref with ~8-12 nodes
  - Agent (GPT-5) produces G_agent with ~6-10 nodes
  - Both pass schema validation
  - JSON files saved to data/outputs/graphs/
  - Raw text responses saved to data/outputs/analysis/
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel

from lex_drl.cache import cache_stats
from lex_drl.cases import load_case
from lex_drl.extraction import extract_agent_graph, extract_teacher_graph, save_graph

load_dotenv()


def main():
    case = load_case("E1")
    rprint(Panel(
        f"[bold]{case.case_id}[/bold] — {case.title}\n"
        f"Jurisdiction: {case.jurisdiction_tags}\n"
        f"Tier: {case.tier} | Role: {case.role}",
        title="Sprint Case",
    ))

    # ── Teacher ──
    rprint("\n[cyan bold]Running TEACHER (Claude Opus 4.6)...[/cyan bold]")
    try:
        g_ref = extract_teacher_graph(case)
        path = save_graph(g_ref)
        rprint(f"  [green]✓ Schema valid[/green]")
        rprint(f"  Nodes: {g_ref.node_summary()}")
        rprint(f"  Saved: {path}")
    except Exception as e:
        rprint(f"  [red]✗ FAILED: {e}[/red]")
        rprint("  Fix the teacher prompt and re-run.")
        return

    # ── Agent ──
    rprint("\n[magenta bold]Running AGENT (GPT-5)...[/magenta bold]")
    try:
        g_agent = extract_agent_graph(case)
        path = save_graph(g_agent)
        rprint(f"  [green]✓ Schema valid[/green]")
        rprint(f"  Nodes: {g_agent.node_summary()}")
        rprint(f"  Saved: {path}")
    except Exception as e:
        rprint(f"  [red]✗ FAILED: {e}[/red]")
        rprint("  Fix the agent prompt and re-run.")
        return

    # ── Quick diff ──
    rprint("\n[bold]Quick Comparison:[/bold]")
    rprint(f"  Teacher total nodes: {g_ref.node_count()}")
    rprint(f"  Agent total nodes:   {g_agent.node_count()}")
    delta = g_ref.node_count() - g_agent.node_count()
    if delta > 0:
        rprint(f"  [yellow]Agent has {delta} fewer nodes — potential discrepancies[/yellow]")
    elif delta < 0:
        rprint(f"  [yellow]Agent has {abs(delta)} MORE nodes — possible hallucinations[/yellow]")
    else:
        rprint(f"  [dim]Same node count — check content alignment manually[/dim]")

    rprint(f"\n  Teacher obligations: {len(g_ref.obligations)}")
    rprint(f"  Agent obligations:   {len(g_agent.obligations)}")
    o_delta = len(g_ref.obligations) - len(g_agent.obligations)
    if o_delta > 0:
        rprint(f"  [yellow]Agent missed {o_delta} obligation(s) — O-node gap[/yellow]")

    stats = cache_stats()
    rprint(f"\n[dim]Cache: {stats['entries']} entries[/dim]")
    rprint("\n[green bold]Smoke test complete.[/green bold] "
           "Inspect data/outputs/ for full results.")


if __name__ == "__main__":
    main()
