"""Tests for src/lex_drl/results.py.

Uses synthetic fixture files written to a tmp_path, never the real
data/outputs/ tree.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from lex_drl.results import (
    load_all_discrepancies,
    node_type_table,
    tier_summary,
)


# ──────────────────────────────────────────────
# Synthetic-fixture helpers
# ──────────────────────────────────────────────

def _case_md(tier: str, role: str) -> str:
    return (
        "# X1 — placeholder\n\n"
        "## Metadata\n"
        f"- tier: {tier}\n"
        f"- role: {role}\n"
        "## Facts\nplaceholder\n## Question\nplaceholder\n"
    )


def _teacher_graph(case_id: str, n_facts: int = 2) -> dict:
    return {
        "case_id": case_id, "source": "reference",
        "model_name": "claude-opus", "agent_id": None,
        "facts": [{"fid": f"F{i+1}", "label": f"t fact {i+1}", "polarity": "present"}
                  for i in range(n_facts)],
        "issues": [], "rules": [], "applications": [],
        "conclusions": [], "obligations": [], "edges": [],
    }


def _student_graph(case_id: str, student: str, n_facts: int) -> dict:
    return {
        "case_id": case_id, "source": "agent",
        "model_name": "test-student", "agent_id": student,
        "facts": [{"fid": f"F{i+1}", "label": f"s fact {i+1}", "polarity": "present"}
                  for i in range(n_facts)],
        "issues": [], "rules": [], "applications": [],
        "conclusions": [], "obligations": [], "edges": [],
    }


def _discrepancy(case_id: str, student: str, v_miss: int, v_halluc: int, e_diff: int,
                 l_ged: float) -> dict:
    return {
        "case_id": case_id, "student_id": student,
        "v_miss": [{"teacher_id": f"F{i}", "node_type": "F", "label": "x", "weight": 1.0}
                   for i in range(v_miss)],
        "v_halluc": [{"student_id": f"F{i}", "node_type": "F", "label": "x",
                      "reason": "unaligned", "weight": 1.0} for i in range(v_halluc)],
        "e_diff": [{"teacher_eid": f"E{i}", "teacher_src": "F1", "teacher_dst": "F2",
                    "teacher_type": "supports", "kind": "missing", "weight": 1.0,
                    "student_src": "F1", "student_dst": "F2"} for i in range(e_diff)],
        "l_ged": l_ged,
        "node_type_breakdown": {k: {"v_miss": 0, "v_halluc": 0} for k in "FIRACO"},
    }


@pytest.fixture
def synth_tree(tmp_path: Path) -> dict[str, Path]:
    """Build a minimal tree mimicking the real one and return its paths."""
    cases_dir = tmp_path / "cases"
    graphs_dir = tmp_path / "graphs"
    disc_dir = tmp_path / "discrepancies"
    cases_dir.mkdir()
    graphs_dir.mkdir()
    disc_dir.mkdir()

    spec = [
        # (case_id, tier, role, teacher_n_facts, students[(name, n_facts, v_miss, v_halluc, e_diff, l_ged)])
        ("E1", "easy",   "training", 5, [("gpt5", 5, 0, 0, 0, 0.0), ("llama3_2b", 2, 3, 0, 0, 6.0)]),
        ("M1", "medium", "training", 5, [("gpt5", 4, 1, 0, 0, 2.0), ("llama3_2b", 2, 3, 1, 0, 8.0)]),
        ("H1", "hard",   "test",     5, [("gpt5", 3, 2, 1, 0, 6.0), ("llama3_2b", 1, 4, 2, 1, 14.0)]),
    ]

    for case_id, tier, role, teacher_n, students in spec:
        (cases_dir / f"{case_id}_synthetic.md").write_text(_case_md(tier, role))
        (graphs_dir / f"{case_id}_reference.json").write_text(
            json.dumps(_teacher_graph(case_id, teacher_n))
        )
        for student, n_facts, v_miss, v_halluc, e_diff, score in students:
            (graphs_dir / f"{case_id}_agent_{student}.json").write_text(
                json.dumps(_student_graph(case_id, student, n_facts))
            )
            (disc_dir / f"{case_id}_{student}.json").write_text(
                json.dumps(_discrepancy(case_id, student, v_miss, v_halluc, e_diff, score))
            )

    return {"cases": cases_dir, "graphs": graphs_dir, "results": disc_dir}


# ──────────────────────────────────────────────
# load_all_discrepancies
# ──────────────────────────────────────────────

def test_load_all_discrepancies_returns_one_row_per_pair(synth_tree):
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    assert len(df) == 6
    assert set(df["case_id"]) == {"E1", "M1", "H1"}
    assert set(df["student"]) == {"gpt5", "llama3_2b"}
    assert set(df.columns) >= {
        "case_id", "tier", "role", "student", "teacher_nodes", "student_nodes",
        "f", "i", "r", "a", "c", "o", "v_miss", "v_halluc", "e_diff", "l_ged",
    }


def test_load_all_discrepancies_pulls_tier_and_node_counts(synth_tree):
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    e1_gpt5 = df[(df["case_id"] == "E1") & (df["student"] == "gpt5")].iloc[0]
    assert e1_gpt5["tier"] == "easy"
    assert e1_gpt5["role"] == "training"
    assert e1_gpt5["teacher_nodes"] == 5
    assert e1_gpt5["student_nodes"] == 5  # 5 facts


def test_load_all_discrepancies_empty_dir_returns_empty_frame(tmp_path):
    df = load_all_discrepancies(
        results_dir=tmp_path / "does_not_exist",
        graphs_dir=tmp_path / "no_graphs",
        cases_dir=tmp_path / "no_cases",
    )
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# ──────────────────────────────────────────────
# node_type_table
# ──────────────────────────────────────────────

def test_node_type_table_has_uppercase_columns(synth_tree):
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    wide = node_type_table(df)
    assert list(wide.columns) == ["case_id", "student", "F", "I", "R", "A", "C", "O", "Total"]
    assert len(wide) == len(df)


def test_node_type_table_total_equals_sum_of_components(synth_tree):
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    wide = node_type_table(df)
    for _, row in wide.iterrows():
        assert row["Total"] == row["F"] + row["I"] + row["R"] + row["A"] + row["C"] + row["O"]


# ──────────────────────────────────────────────
# tier_summary
# ──────────────────────────────────────────────

def test_tier_summary_has_one_row_per_tier_student(synth_tree):
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    summary = tier_summary(df)
    assert len(summary) == 6  # 3 tiers × 2 students
    assert set(summary["tier"]) == {"easy", "medium", "hard"}
    assert set(summary["student"]) == {"gpt5", "llama3_2b"}


def test_tier_summary_means_match_inputs(synth_tree):
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    summary = tier_summary(df)
    # Each tier has exactly one case in the fixture, so means equal the single value.
    easy_gpt5 = summary[(summary["tier"] == "easy") & (summary["student"] == "gpt5")].iloc[0]
    assert easy_gpt5["l_ged"] == pytest.approx(0.0)
    hard_llama = summary[(summary["tier"] == "hard") & (summary["student"] == "llama3_2b")].iloc[0]
    assert hard_llama["l_ged"] == pytest.approx(14.0)


def test_tier_summary_lged_monotone_across_tiers(synth_tree):
    """Sanity check the spec asks for: L-GED rises Easy → Medium → Hard."""
    df = load_all_discrepancies(
        results_dir=synth_tree["results"],
        graphs_dir=synth_tree["graphs"],
        cases_dir=synth_tree["cases"],
    )
    summary = tier_summary(df)
    for student in ["gpt5", "llama3_2b"]:
        sub = summary[summary["student"] == student].set_index("tier")
        assert sub.loc["easy", "l_ged"] <= sub.loc["medium", "l_ged"] <= sub.loc["hard", "l_ged"]
