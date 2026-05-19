"""Aggregate per-case discrepancy reports into DataFrame views.

Loads every file under ``data/outputs/discrepancies/`` and merges in case
metadata (tier, role) plus per-graph node counts from the original
extractions. Produces three DataFrame shapes the HTML report renders:

* :func:`load_all_discrepancies` — one row per (case, student) with every metric.
* :func:`node_type_table` — wide-format F/I/R/A/C/O breakdown per row.
* :func:`tier_summary` — averages across cases within a tier × student.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_RESULTS_DIR = Path("data/outputs/discrepancies")
DEFAULT_GRAPHS_DIR = Path("data/outputs/graphs")
DEFAULT_CASES_DIR = Path("data/cases")

NODE_FIELDS = ["facts", "issues", "rules", "applications", "conclusions", "obligations"]
NODE_LABELS = ["f", "i", "r", "a", "c", "o"]


# ──────────────────────────────────────────────
# Metadata helpers
# ──────────────────────────────────────────────

def _read_case_metadata(cases_dir: Path) -> dict[str, dict[str, str]]:
    """Best-effort parse of ``data/cases/*.md`` for tier and role fields."""
    out: dict[str, dict[str, str]] = {}
    if not cases_dir.is_dir():
        return out
    for path in cases_dir.glob("*.md"):
        case_id = path.name.split("_")[0]
        tier = role = ""
        in_meta = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                in_meta = line[3:].strip().lower() == "metadata"
                continue
            if in_meta and ":" in line:
                key, _, val = line.partition(":")
                key = key.strip().lstrip("-").strip().lower()
                val = val.strip().strip("`").strip('"')
                if key == "tier":
                    tier = val
                elif key == "role":
                    role = val
        out[case_id] = {"tier": tier, "role": role}
    return out


def _read_graph_counts(graphs_dir: Path) -> dict[tuple[str, str], dict[str, int]]:
    """Map (case_id, student) → {f,i,r,a,c,o,teacher_nodes,student_nodes}."""
    out: dict[tuple[str, str], dict[str, int]] = {}
    if not graphs_dir.is_dir():
        return out
    # Collect teacher counts by case.
    teacher_nodes: dict[str, int] = {}
    for path in graphs_dir.glob("*_reference.json"):
        try:
            g = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        teacher_nodes[g.get("case_id", path.stem)] = sum(len(g.get(f, [])) for f in NODE_FIELDS)

    for path in graphs_dir.glob("*_agent_*.json"):
        try:
            g = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        case_id = g.get("case_id") or path.stem.split("_agent_")[0]
        student = g.get("agent_id") or path.stem.split("_agent_")[-1]
        counts = {label: len(g.get(field, []))
                  for label, field in zip(NODE_LABELS, NODE_FIELDS)}
        counts["student_nodes"] = sum(counts[k] for k in NODE_LABELS)
        counts["teacher_nodes"] = teacher_nodes.get(case_id, 0)
        out[(case_id, student)] = counts
    return out


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────

def load_all_discrepancies(
    results_dir: Path = DEFAULT_RESULTS_DIR,
    graphs_dir: Path = DEFAULT_GRAPHS_DIR,
    cases_dir: Path = DEFAULT_CASES_DIR,
) -> pd.DataFrame:
    """Load every ``{case_id}_{student}.json`` and return a single DataFrame.

    Columns: ``case_id, tier, role, student, teacher_nodes, student_nodes,
    f, i, r, a, c, o, v_miss, v_halluc, e_diff, l_ged``.
    """
    results_dir = Path(results_dir)
    if not results_dir.is_dir():
        return pd.DataFrame(columns=[
            "case_id", "tier", "role", "student", "teacher_nodes", "student_nodes",
            "f", "i", "r", "a", "c", "o", "v_miss", "v_halluc", "e_diff", "l_ged",
        ])

    case_meta = _read_case_metadata(Path(cases_dir))
    graph_counts = _read_graph_counts(Path(graphs_dir))

    rows: list[dict[str, Any]] = []
    for path in sorted(results_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        case_id = data.get("case_id")
        student = data.get("student_id") or path.stem.split("_", 1)[-1]
        if not case_id:
            # fallback: parse "E1_gpt5" → "E1"
            case_id = path.stem.split("_", 1)[0]
            student = path.stem.split("_", 1)[-1]

        gc = graph_counts.get((case_id, student), {})
        row = {
            "case_id": case_id,
            "tier": case_meta.get(case_id, {}).get("tier", ""),
            "role": case_meta.get(case_id, {}).get("role", ""),
            "student": student,
            "teacher_nodes": gc.get("teacher_nodes", 0),
            "student_nodes": gc.get("student_nodes", 0),
            "f": gc.get("f", 0), "i": gc.get("i", 0), "r": gc.get("r", 0),
            "a": gc.get("a", 0), "c": gc.get("c", 0), "o": gc.get("o", 0),
            "v_miss": len(data.get("v_miss", [])),
            "v_halluc": len(data.get("v_halluc", [])),
            "e_diff": len(data.get("e_diff", [])),
            "l_ged": float(data.get("l_ged", 0.0)),
        }
        rows.append(row)

    return pd.DataFrame(rows, columns=[
        "case_id", "tier", "role", "student", "teacher_nodes", "student_nodes",
        "f", "i", "r", "a", "c", "o", "v_miss", "v_halluc", "e_diff", "l_ged",
    ])


def node_type_table(df: pd.DataFrame) -> pd.DataFrame:
    """Wide-format F/I/R/A/C/O breakdown — one row per (case, student)."""
    if df.empty:
        return df.copy()
    cols = ["case_id", "student", "f", "i", "r", "a", "c", "o", "student_nodes"]
    return df[cols].rename(columns={
        "f": "F", "i": "I", "r": "R", "a": "A", "c": "C", "o": "O",
        "student_nodes": "Total",
    })


def tier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (tier, student) with mean metrics across the tier's cases."""
    if df.empty:
        return df.copy()
    grouped = df.groupby(["tier", "student"], dropna=False).agg(
        cases=("case_id", "nunique"),
        teacher_nodes=("teacher_nodes", "mean"),
        student_nodes=("student_nodes", "mean"),
        v_miss=("v_miss", "mean"),
        v_halluc=("v_halluc", "mean"),
        e_diff=("e_diff", "mean"),
        l_ged=("l_ged", "mean"),
    ).reset_index()
    for col in ["teacher_nodes", "student_nodes", "v_miss", "v_halluc", "e_diff", "l_ged"]:
        grouped[col] = grouped[col].round(2)
    return grouped


__all__ = [
    "DEFAULT_CASES_DIR",
    "DEFAULT_GRAPHS_DIR",
    "DEFAULT_RESULTS_DIR",
    "load_all_discrepancies",
    "node_type_table",
    "tier_summary",
]
