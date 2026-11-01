"""Sanitizer cases found in the patch-loop runs.

Three patched Llama answers were rejected outright for one dangling edge or an
invalid issue status. A graph with such a slip is still an answer and should
be scored as one.
"""
from __future__ import annotations

from lex_drl.extraction import _sanitize_raw_graph
from lex_drl.schema import LegalReasoningGraph


def _raw() -> dict:
    return {
        "case_id": "T", "source": "agent", "model_name": "m", "agent_id": "x",
        "facts": [{"fid": "F1", "label": "f", "polarity": "present"}],
        "issues": [{"iid": "I1", "label": "i", "status": "dispositive"}],
        "rules": [{"rid": "R1", "citation": "§1", "label": "r", "jurisdiction": "NYC"}],
        "applications": [], "conclusions": [], "obligations": [],
        "edges": [{"eid": "E1", "src": "F1", "dst": "I1", "type": "triggers"}],
    }


def test_a_dangling_edge_is_dropped_and_the_graph_survives():
    raw = _raw()
    raw["edges"].append({"eid": "E2", "src": "I1", "dst": "C2", "type": "supports"})  # no C2
    out = _sanitize_raw_graph(raw, "T", "agent_x")
    assert [e["eid"] for e in out["edges"]] == ["E1"]
    graph = LegalReasoningGraph.model_validate(out)
    assert len(graph.edges) == 1 and graph.node_count() == 3


def test_an_invalid_issue_status_is_mapped_to_a_default():
    raw = _raw()
    raw["issues"][0]["status"] = "violated"
    out = _sanitize_raw_graph(raw, "T", "agent_x")
    assert out["issues"][0]["status"] == "dispositive"
    LegalReasoningGraph.model_validate(out)


def test_an_invalid_fact_polarity_is_mapped_to_a_default():
    raw = _raw()
    raw["facts"][0]["polarity"] = "confirmed"
    out = _sanitize_raw_graph(raw, "T", "agent_x")
    assert out["facts"][0]["polarity"] == "present"


def test_a_valid_graph_is_left_exactly_as_it_was():
    raw = _raw()
    before = repr(raw)
    assert repr(_sanitize_raw_graph(raw, "T", "agent_x")) == before


def test_application_missing_reasoning_is_filled_not_rejected():
    from lex_drl.extraction import _sanitize_raw_graph

    raw = {"applications": [{"aid": "A1", "rule_ref": "R1", "issue_ref": "I1", "result": "violated"}]}
    out = _sanitize_raw_graph(raw, "X1", "agent")
    assert out["applications"][0]["reasoning"] == "" and out["applications"][0]["fact_refs"] == []


def test_edge_missing_type_gets_the_default():
    from lex_drl.extraction import _sanitize_raw_graph

    raw = {"facts": [{"fid": "F1", "label": "x"}], "issues": [{"iid": "I1", "label": "y"}],
           "edges": [{"eid": "E1", "src": "F1", "dst": "I1"}]}
    assert _sanitize_raw_graph(raw, "X1", "agent")["edges"][0]["type"] == "supports"
