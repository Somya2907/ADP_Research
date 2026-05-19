"""Verify the F-I-R-A-C-O schema enforces what we intend.

Run with: poetry run pytest
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from lex_drl.schema import (
    Application,
    ApplicationResult,
    Authority,
    Conclusion,
    ConclusionDetermination,
    Confidence,
    Edge,
    EdgeType,
    Fact,
    GraphSource,
    Issue,
    IssueStatus,
    LegalReasoningGraph,
    Obligation,
    ObligationStatus,
    Polarity,
    Rule,
)


# ── Minimal valid graph ──

def test_minimal_valid_graph():
    g = LegalReasoningGraph(
        case_id="E1",
        source=GraphSource.REFERENCE,
        model_name="claude-opus-4-6",
    )
    assert g.case_id == "E1"
    assert g.facts == []
    assert g.node_count() == 0
    assert "F=0" in g.node_summary()


# ── Node ID pattern enforcement ──

def test_fact_id_must_match_pattern():
    with pytest.raises(ValidationError, match="fid"):
        Fact(fid="fact-1", label="something")


def test_fact_id_valid():
    f = Fact(fid="F1", label="Company is in NYC")
    assert f.fid == "F1"
    assert f.polarity == Polarity.PRESENT


def test_issue_id_must_match_pattern():
    with pytest.raises(ValidationError, match="iid"):
        Issue(iid="issue_1", label="x")


def test_rule_id_must_match_pattern():
    with pytest.raises(ValidationError, match="rid"):
        Rule(rid="rule-A", citation="x", label="x", jurisdiction="CO")


def test_application_id_must_match_pattern():
    with pytest.raises(ValidationError, match="aid"):
        Application(
            aid="app1", rule_ref="R1", fact_refs=["F1"],
            issue_ref="I1", result=ApplicationResult.SATISFIED, reasoning="x",
        )


def test_conclusion_id_must_match_pattern():
    with pytest.raises(ValidationError, match="cid"):
        Conclusion(
            cid="conclusion", determination=ConclusionDetermination.COMPLIANT,
            support_refs=["A1"],
        )


def test_obligation_id_must_match_pattern():
    with pytest.raises(ValidationError, match="oid"):
        Obligation(
            oid="ob-1", label="x", required_by="R1",
            status=ObligationStatus.MANDATORY, jurisdiction="CO",
        )


def test_edge_id_must_match_pattern():
    with pytest.raises(ValidationError, match="eid"):
        Edge(eid="edge-1", src="F1", dst="I1", type=EdgeType.TRIGGERS)


# ── Edge reference validation ──

def test_edge_refs_must_exist():
    """Edges that reference nonexistent node IDs should fail validation."""
    with pytest.raises(ValidationError, match="nonexistent"):
        LegalReasoningGraph(
            case_id="E1",
            source=GraphSource.REFERENCE,
            model_name="test",
            facts=[Fact(fid="F1", label="x")],
            edges=[Edge(eid="E1", src="F1", dst="F99", type=EdgeType.SUPPORTS)],
        )


def test_edge_refs_valid_when_nodes_exist():
    """Edges referencing real node IDs should pass."""
    g = LegalReasoningGraph(
        case_id="E1",
        source=GraphSource.REFERENCE,
        model_name="test",
        facts=[Fact(fid="F1", label="Company in NYC")],
        issues=[Issue(iid="I1", label="Does LL 144 apply?")],
        edges=[Edge(eid="E1", src="F1", dst="I1", type=EdgeType.TRIGGERS)],
    )
    assert len(g.edges) == 1


# ── Rule fields ──

def test_rule_effective_date_optional():
    r = Rule(
        rid="R1", citation="Colo. Rev. Stat. §6-1-1703",
        label="Deployer obligations", jurisdiction="CO",
        effective_as_of="2026-06-30",
    )
    assert r.effective_as_of == "2026-06-30"
    assert r.authority == Authority.BINDING


def test_rule_advisory_authority():
    r = Rule(
        rid="R2", citation="NIST AI RMF 1.0",
        label="Map function", jurisdiction="US-federal",
        authority=Authority.ADVISORY,
    )
    assert r.authority == Authority.ADVISORY


# ── Full graph round-trip ──

def test_full_graph_round_trip():
    """Build a small but complete graph and verify serialization."""
    g = LegalReasoningGraph(
        case_id="E1",
        source=GraphSource.AGENT,
        model_name="gpt-5",
        facts=[
            Fact(fid="F1", label="Greenleaf uses ResumeRank in NYC"),
            Fact(fid="F2", label="No bias audit posted"),
        ],
        issues=[
            Issue(iid="I1", label="Is ResumeRank an AEDT under LL 144?"),
        ],
        rules=[
            Rule(rid="R1", citation="NYC LL 144 §20-871",
                 label="Bias audit requirement", jurisdiction="NYC"),
        ],
        applications=[
            Application(aid="A1", rule_ref="R1", fact_refs=["F1", "F2"],
                       issue_ref="I1", result=ApplicationResult.VIOLATED,
                       reasoning="No audit within 1 year"),
        ],
        conclusions=[
            Conclusion(cid="C1", determination=ConclusionDetermination.NON_COMPLIANT,
                      confidence=Confidence.HIGH, support_refs=["A1"]),
        ],
        obligations=[
            Obligation(oid="O1", label="Commission independent bias audit",
                      required_by="R1", status=ObligationStatus.MANDATORY,
                      jurisdiction="NYC"),
        ],
        edges=[
            Edge(eid="E1", src="F1", dst="I1", type=EdgeType.TRIGGERS),
            Edge(eid="E2", src="R1", dst="A1", type=EdgeType.APPLIES_TO),
            Edge(eid="E3", src="F2", dst="A1", type=EdgeType.SUPPORTS),
            Edge(eid="E4", src="A1", dst="C1", type=EdgeType.FAILS_ELEMENT),
            Edge(eid="E5", src="R1", dst="O1", type=EdgeType.TRIGGERS),
        ],
    )

    # Serialize and deserialize
    json_str = g.model_dump_json(indent=2)
    g2 = LegalReasoningGraph.model_validate_json(json_str)
    assert g2.case_id == "E1"
    assert g2.node_count() == 7  # 2F + 1I + 1R + 1A + 1C + 1O (edges excluded)
    assert len(g2.edges) == 5
    assert g2.source == GraphSource.AGENT


# ── Node count and summary ──

def test_node_count_excludes_edges():
    g = LegalReasoningGraph(
        case_id="X1", source=GraphSource.REFERENCE, model_name="test",
        facts=[Fact(fid="F1", label="x")],
        edges=[Edge(eid="E1", src="F1", dst="F1", type=EdgeType.SUPPORTS)],
    )
    assert g.node_count() == 1  # edges don't count as nodes
