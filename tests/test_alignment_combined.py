"""Tests for the combined citation+text rule aligner (LEX_DRL_RULE_ALIGN=combined).

Runs under the default TF-IDF text backend so no embedding model is loaded; the
combined logic (citation force-match, sibling-subsection discount, text fallback)
is backend-independent.
"""
from __future__ import annotations

import lex_drl.alignment as al
from lex_drl.alignment import align_rules
from lex_drl.schema import Authority, GraphSource, LegalReasoningGraph, Rule

THR = 0.10  # TF-IDF default threshold


def _graph(rules: list[Rule]) -> LegalReasoningGraph:
    return LegalReasoningGraph(
        case_id="T", source=GraphSource.REFERENCE, model_name="m", rules=rules
    )


def _rule(rid: str, citation: str, label: str) -> Rule:
    return Rule(rid=rid, citation=citation, label=label,
                authority=Authority.BINDING, jurisdiction="co")


def test_combined_exact_citation_matches_despite_different_text(monkeypatch):
    monkeypatch.setattr(al, "RULE_ALIGN_MODE", "combined")
    t = _graph([_rule("R1", "§6-1-1703(2)(a)", "risk management policy")])
    s = _graph([_rule("R1", "CO AIA Section 6-1-1703(2)(a)", "deployer obligations")])
    # citation tokens intersect -> forced match even though the labels differ
    assert align_rules(t, s, THR) == {"R1": "R1"}


def test_combined_blocks_sibling_subsection_merge(monkeypatch):
    monkeypatch.setattr(al, "RULE_ALIGN_MODE", "combined")
    # identical text, DIFFERENT subsection -> must NOT merge (the professor's concern)
    t = _graph([_rule("R1", "§6-1-1703(2)(a)", "deployer must implement a risk management policy")])
    s = _graph([_rule("R1", "§6-1-1703(2)(b)", "deployer must implement a risk management policy")])
    assert align_rules(t, s, THR) == {"R1": None}


def test_hybrid_default_WOULD_merge_siblings(monkeypatch):
    # Contrast: the default hybrid falls to text and merges the two subsections.
    monkeypatch.setattr(al, "RULE_ALIGN_MODE", "hybrid")
    t = _graph([_rule("R1", "§6-1-1703(2)(a)", "deployer must implement a risk management policy")])
    s = _graph([_rule("R1", "§6-1-1703(2)(b)", "deployer must implement a risk management policy")])
    assert align_rules(t, s, THR) == {"R1": "R1"}


def test_combined_text_fallback_when_no_citation(monkeypatch):
    monkeypatch.setattr(al, "RULE_ALIGN_MODE", "combined")
    # no section tokens on either side -> pure text similarity aligns them
    t = _graph([_rule("R1", "NIST AI RMF", "risk management framework guidance")])
    s = _graph([_rule("R1", "NIST AI RMF 1.0", "risk management framework guidance")])
    assert align_rules(t, s, THR) == {"R1": "R1"}


def test_combined_empty_student_rules_all_none(monkeypatch):
    monkeypatch.setattr(al, "RULE_ALIGN_MODE", "combined")
    t = _graph([_rule("R1", "§6-1-1703(2)(a)", "risk management policy")])
    assert align_rules(t, _graph([]), THR) == {"R1": None}
