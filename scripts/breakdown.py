"""Node-type breakdown diagnostic.

Walks data/outputs/graphs/ and prints per-graph counts of F/I/R/A/C/O nodes
and edges, plus per-case teacher-vs-student deltas. Useful for spotting
catastrophically short student extractions before running the discrepancy
scorer.

Usage:
    poetry run python scripts/breakdown.py
    poetry run python scripts/breakdown.py --graphs-dir data/outputs/graphs
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.table import Table

NODE_FIELDS = ["facts", "issues", "rules", "applications", "conclusions", "obligations"]
NODE_LABELS = ["F", "I", "R", "A", "C", "O"]


def counts(graph: dict) -> dict[str, int]:
    out = {label: len(graph.get(field, [])) for label, field in zip(NODE_LABELS, NODE_FIELDS)}
    out["E"] = len(graph.get("edges", []))
    out["total"] = sum(out[k] for k in NODE_LABELS)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graphs-dir", default="data/outputs/graphs")
    args = parser.parse_args()

    console = Console()
    gdir = Path(args.graphs_dir)
    if not gdir.is_dir():
        console.print(f"[red]No such directory: {gdir}[/red]")
        sys.exit(1)

    by_case: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    for path in sorted(gdir.glob("*.json")):
        try:
            graph = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            console.print(f"[red]{path.name}: invalid JSON ({e})[/red]")
            continue
        case_id = graph.get("case_id", path.stem)
        source = graph.get("source", "?")
        agent_id = graph.get("agent_id")
        label = "reference" if source == "reference" else f"agent_{agent_id or '?'}"
        by_case[case_id][label] = counts(graph)

    table = Table(title="F-I-R-A-C-O node-type breakdown", show_lines=True)
    table.add_column("Case", style="bold")
    table.add_column("Graph")
    for h in NODE_LABELS:
        table.add_column(h, justify="right")
    table.add_column("E", justify="right")
    table.add_column("Total", justify="right")

    for case_id in sorted(by_case):
        for label in sorted(by_case[case_id]):
            c = by_case[case_id][label]
            row = [case_id, label] + [str(c[k]) for k in NODE_LABELS] + [str(c["E"]), str(c["total"])]
            table.add_row(*row)

    console.print(table)


if __name__ == "__main__":
    main()
