"""Render the full-sweep results as a single self-contained HTML report.

Sections:
  - Header: run timestamp + git SHA (if available)
  - Per-case discrepancy table (from results.load_all_discrepancies)
  - Wide-format node-type table (from results.node_type_table)
  - Tier × student averaged metrics (from results.tier_summary)
  - One bar chart per case: teacher vs student node counts
  - Grouped bar chart: L-GED by tier × student
  - Links to each per-case discrepancy report

Usage:
    poetry run python scripts/build_report.py
    poetry run python scripts/build_report.py --out results/report.html
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as html_lib
import subprocess
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pandas as pd
import plotly.express as px
import plotly.io as pio

from lex_drl.results import load_all_discrepancies, node_type_table, tier_summary

REPORT_OUT = Path("results/report.html")
DISCREPANCIES_DIR = Path("data/outputs/discrepancies")

TIER_ORDER = {"easy": 0, "medium": 1, "hard": 2, "": 3}


def git_sha() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=4)
        if r.returncode == 0:
            return r.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return "unknown"


def fig_html(fig) -> str:
    return pio.to_html(fig, include_plotlyjs="cdn", full_html=False,
                       config={"displaylogo": False})


def styled_table(df: pd.DataFrame, table_id: str) -> str:
    if df.empty:
        return f"<p><em>No data ({table_id}).</em></p>"
    return df.to_html(index=False, classes=f"results-table {table_id}",
                      table_id=table_id, border=0, float_format=lambda x: f"{x:.2f}")


def chart_node_counts(df: pd.DataFrame) -> str:
    """One stacked bar chart per case: teacher vs each student's total nodes."""
    if df.empty:
        return ""
    plot_df = df.melt(
        id_vars=["case_id", "student"],
        value_vars=["teacher_nodes", "student_nodes"],
        var_name="graph", value_name="nodes",
    )
    # Deduplicate teacher rows so each (case, "teacher_nodes") appears once.
    teacher_rows = plot_df[plot_df["graph"] == "teacher_nodes"] \
        .drop_duplicates(subset=["case_id"])
    teacher_rows = teacher_rows.assign(label="teacher")
    student_rows = plot_df[plot_df["graph"] == "student_nodes"].assign(
        label=lambda d: d["student"],
    )
    plot_df = pd.concat([teacher_rows, student_rows], ignore_index=True)
    plot_df["case_sort"] = plot_df["case_id"]
    fig = px.bar(
        plot_df, x="case_id", y="nodes", color="label", barmode="group",
        title="Node count: teacher vs student, per case",
        labels={"case_id": "Case", "nodes": "Total nodes", "label": "Graph"},
    )
    fig.update_layout(margin=dict(l=40, r=20, t=50, b=40), height=400)
    return fig_html(fig)


def chart_lged_by_tier(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    summary = tier_summary(df).copy()
    summary["tier_order"] = summary["tier"].map(TIER_ORDER).fillna(99)
    summary = summary.sort_values(["tier_order", "student"])
    fig = px.bar(
        summary, x="tier", y="l_ged", color="student", barmode="group",
        title="Mean L-GED by tier × student",
        labels={"tier": "Tier", "l_ged": "Mean L-GED", "student": "Student"},
    )
    fig.update_layout(margin=dict(l=40, r=20, t=50, b=40), height=400)
    return fig_html(fig)


def per_case_links(case_ids: Iterable[str], students: Iterable[str]) -> str:
    rows: list[str] = ["<ul class='link-list'>"]
    for case_id in sorted(set(case_ids)):
        for student in sorted(set(students)):
            href = (DISCREPANCIES_DIR / f"{case_id}_{student}.json").as_posix()
            rows.append(
                f"<li><a href='{html_lib.escape(href)}'>"
                f"{html_lib.escape(case_id)} · {html_lib.escape(student)}</a></li>"
            )
    rows.append("</ul>")
    return "\n".join(rows)


CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       max-width: 1100px; margin: 2em auto; padding: 0 1em; color: #222; }
h1 { border-bottom: 2px solid #2E86C1; padding-bottom: 0.3em; }
h2 { margin-top: 2em; color: #2E86C1; }
.meta { color: #666; font-size: 0.9em; margin-bottom: 1.5em; }
.results-table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em; }
.results-table th { background: #2E86C1; color: white; text-align: left;
                    padding: 0.5em 0.75em; }
.results-table td { padding: 0.4em 0.75em; border-bottom: 1px solid #eee; }
.results-table tr:nth-child(even) { background: #fafafa; }
.link-list { columns: 3; -webkit-columns: 3; -moz-columns: 3;
             font-family: monospace; font-size: 0.9em; }
.link-list li { break-inside: avoid; margin-bottom: 0.2em; }
.chart-wrap { margin: 1em 0; }
"""


def build_html(df: pd.DataFrame) -> str:
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    sha = git_sha()
    case_ids = df["case_id"].tolist() if not df.empty else []
    students = df["student"].tolist() if not df.empty else []

    # Sort the main table by tier → case → student for readable display.
    if not df.empty:
        df_sorted = df.copy()
        df_sorted["tier_order"] = df_sorted["tier"].map(TIER_ORDER).fillna(99)
        df_sorted = df_sorted.sort_values(["tier_order", "case_id", "student"]) \
                             .drop(columns=["tier_order"])
    else:
        df_sorted = df

    nodes_chart = chart_node_counts(df)
    lged_chart = chart_lged_by_tier(df)

    parts = [
        "<!DOCTYPE html><html><head>",
        "<meta charset='utf-8'>",
        "<title>L-DRL — sweep report</title>",
        f"<style>{CSS}</style>",
        "</head><body>",
        "<h1>L-DRL — sweep report</h1>",
        f"<div class='meta'>Generated {html_lib.escape(timestamp)} · git {html_lib.escape(sha)}</div>",
        "<h2>Discrepancy summary</h2>",
        styled_table(df_sorted, "discrepancy-summary"),
        "<h2>Node-type breakdown (student graphs)</h2>",
        styled_table(node_type_table(df), "node-type-breakdown"),
        "<h2>Tier × student averages</h2>",
        styled_table(tier_summary(df), "tier-summary"),
        "<h2>Node counts per case</h2>",
        f"<div class='chart-wrap'>{nodes_chart}</div>",
        "<h2>L-GED by tier × student</h2>",
        f"<div class='chart-wrap'>{lged_chart}</div>",
        "<h2>Per-case discrepancy reports</h2>",
        per_case_links(case_ids, students),
        "</body></html>",
    ]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="data/outputs/discrepancies")
    parser.add_argument("--graphs-dir", default="data/outputs/graphs")
    parser.add_argument("--cases-dir", default="data/cases")
    parser.add_argument("--out", default=str(REPORT_OUT))
    args = parser.parse_args()

    df = load_all_discrepancies(
        results_dir=Path(args.results_dir),
        graphs_dir=Path(args.graphs_dir),
        cases_dir=Path(args.cases_dir),
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_html(df), encoding="utf-8")
    print(f"Report written: {out_path}  ({len(df)} rows)")


if __name__ == "__main__":
    main()
