"""Tests for src/lex_drl/discrepancy.py.

Covers the four required scenarios from the onboarding spec:
  1. Identical graphs → zero discrepancies, L-GED = 0
  2. Missing rule node → v_miss = 1, L-GED = rule's weighted cost
  3. Extra hallucinated rule → v_halluc = 1
  4. Same nodes, rewired edges → e_diff > 0
(Citation-variant alignment is tested in test_alignment.py.)
"""
from __future__ import annotations

import pytest

from lex_drl.alignment import align_all
from lex_drl.discrepancy import (
    AUTHORITY_MULTIPLIERS,
    NODE_TYPE_WEIGHTS,
    compute_discrepancies,
    l_ged,
)
from lex_drl.schema import (
    Authority,
    Edge,
    EdgeType,
    Fact,
    GraphSource,
    Issue,
    IssueStatus,
    LegalReasoningGraph,
    Rule,
)


# ──────────────────────────────────────────────
# Builders
# ──────────────────────────────────────────────

def _graph(case_id="T1", source=GraphSource.REFERENCE, model="m", agent_id=None,
           facts=(), issues=(), rules=(), edges=()):
    return LegalReasoningGraph(
        case_id=case_id,
        source=source,
        model_name=model,
        agent_id=agent_id,
        facts=list(facts),
        issues=list(issues),
        rules=list(rules),
        edges=list(edges),
    )


def _baseline_graph(*, with_extra_rule=False, with_extra_edge=False, source=GraphSource.REFERENCE):
    facts = [
        Fact(fid="F1", label="HireFlow is based in Austin Texas"),
        Fact(fid="F2", label="ResumeRank is an automated employment decision tool"),
    ]
    issues = [Issue(iid="I1", label="does the AEDT audit obligation apply",
                    status=IssueStatus.DISPOSITIVE)]
    rules = [Rule(rid="R1", citation="§ 20-871(d)(2)", label="annual bias audit",
                  authority=Authority.BINDING, jurisdiction="NYC")]
    if with_extra_rule:
        rules.append(Rule(
            rid="R2", citation="§ 99-99-9",
            label="phantom reporting requirement that does not exist",
            authority=Authority.BINDING, jurisdiction="ZZ",
        ))
    edges = [
        Edge(eid="E1", src="F1", dst="I1", type=EdgeType.TRIGGERS),
        Edge(eid="E2", src="R1", dst="I1", type=EdgeType.APPLIES_TO),
    ]
    if with_extra_edge:
        edges.append(Edge(eid="E3", src="F2", dst="I1", type=EdgeType.TRIGGERS))
    return _graph(facts=facts, issues=issues, rules=rules, edges=edges, source=source)


# ──────────────────────────────────────────────
# 1. Identical graphs → zero discrepancies
# ──────────────────────────────────────────────

def test_identical_graphs_produce_zero_discrepancies_and_zero_lged():
    teacher = _baseline_graph()
    student = _baseline_graph(source=GraphSource.AGENT)
    student.agent_id = "test_student"
    alignment = align_all(teacher, student)
    report = compute_discrepancies(teacher, student, alignment)

    assert report.v_miss == []
    assert report.v_halluc == []
    assert report.e_diff == []
    assert report.l_ged == pytest.approx(0.0)
    assert report.student_id == "test_student"


# ──────────────────────────────────────────────
# 2. Missing rule → v_miss = 1, L-GED = R-weight × binding-multiplier
# ──────────────────────────────────────────────

def test_missing_rule_node_produces_one_v_miss_and_correct_lged():
    teacher = _baseline_graph()
    student = _graph(
        case_id="T1", source=GraphSource.AGENT, agent_id="test_student",
        facts=teacher.facts, issues=teacher.issues,
        rules=[],  # drop the rule
        edges=[Edge(eid="E1", src="F1", dst="I1", type=EdgeType.TRIGGERS)],
    )
    alignment = align_all(teacher, student)
    report = compute_discrepancies(teacher, student, alignment)

    assert report.v_miss_count == 1
    assert report.v_miss[0].teacher_id == "R1"
    assert report.v_miss[0].node_type == "R"

    expected_rule_weight = NODE_TYPE_WEIGHTS["R"] * AUTHORITY_MULTIPLIERS[Authority.BINDING]
    # We also lose the R1→I1 edge in v_miss-edge accounting? No: e_diff only fires when
    # both endpoints align. R1 is unaligned so the edge is implicitly accounted for via v_miss.
    # The R1 node weight alone should dominate the L-GED contribution.
    assert report.l_ged == pytest.approx(expected_rule_weight)


# ──────────────────────────────────────────────
# 3. Extra hallucinated rule → v_halluc = 1
# ──────────────────────────────────────────────

def test_extra_rule_in_student_produces_one_v_halluc():
    teacher = _baseline_graph()
    student = _baseline_graph(with_extra_rule=True, source=GraphSource.AGENT)
    student.agent_id = "test_student"
    alignment = align_all(teacher, student)
    report = compute_discrepancies(teacher, student, alignment)

    assert report.v_miss == []
    assert report.v_halluc_count == 1
    assert report.v_halluc[0].student_id == "R2"
    assert report.v_halluc[0].node_type == "R"
    # The extra rule contributes its weight to L-GED.
    expected = NODE_TYPE_WEIGHTS["R"] * AUTHORITY_MULTIPLIERS[Authority.BINDING]
    assert report.l_ged == pytest.approx(expected)


# ──────────────────────────────────────────────
# 4. Same nodes, rewired edges → e_diff > 0
# ──────────────────────────────────────────────

def test_same_nodes_rewired_edges_produces_edge_diff():
    teacher = _baseline_graph()
    # Student keeps the same node set but flips an edge type.
    student = _graph(
        case_id="T1", source=GraphSource.AGENT, agent_id="test_student",
        facts=teacher.facts, issues=teacher.issues, rules=teacher.rules,
        edges=[
            Edge(eid="E1", src="F1", dst="I1", type=EdgeType.SUPPORTS),  # was TRIGGERS
            Edge(eid="E2", src="R1", dst="I1", type=EdgeType.APPLIES_TO),
        ],
    )
    alignment = align_all(teacher, student)
    report = compute_discrepancies(teacher, student, alignment)

    assert report.v_miss == []
    assert report.v_halluc == []
    assert report.e_diff_count == 1
    diff = report.e_diff[0]
    assert diff.teacher_type == "triggers"
    assert diff.student_type == "supports"
    assert diff.kind == "type_mismatch"
    assert report.l_ged > 0
    assert l_ged(teacher, student, alignment) == report.l_ged


def test_missing_edge_with_aligned_endpoints_produces_edge_diff():
    teacher = _baseline_graph()
    student = _graph(
        case_id="T1", source=GraphSource.AGENT, agent_id="test_student",
        facts=teacher.facts, issues=teacher.issues, rules=teacher.rules,
        edges=[Edge(eid="E1", src="F1", dst="I1", type=EdgeType.TRIGGERS)],
        # Dropped R1→I1
    )
    alignment = align_all(teacher, student)
    report = compute_discrepancies(teacher, student, alignment)

    assert report.v_miss == []
    assert report.e_diff_count == 1
    assert report.e_diff[0].kind == "missing"


# ──────────────────────────────────────────────
# Sanity: L-GED is non-negative & finite across all cases above.
# ──────────────────────────────────────────────

def test_lged_is_non_negative_and_finite():
    teacher = _baseline_graph()
    for student in [
        _baseline_graph(source=GraphSource.AGENT),
        _baseline_graph(with_extra_rule=True, source=GraphSource.AGENT),
        _baseline_graph(with_extra_edge=True, source=GraphSource.AGENT),
    ]:
        student.agent_id = "test_student"
        alignment = align_all(teacher, student)
        score = l_ged(teacher, student, alignment)
        assert score >= 0
        assert score < float("inf")
