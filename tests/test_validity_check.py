"""Tests for make_statute_validity_check — statute-grounded v_halluc refinement.

A fake section_exists_fn (only §20-870 is "real") stands in for the index, so
these tests are hermetic and don't depend on the corpus.
"""
from __future__ import annotations

from lex_drl.alignment import AlignmentReport
from lex_drl.discrepancy import (
    compute_discrepancies,
    make_statute_validity_check,
)
from lex_drl.schema import Fact, GraphSource, LegalReasoningGraph, Rule

# Only §20-870 counts as a real section for these tests.
_fake_exists = lambda citation: "20-870" in citation


def _rule(rid: str, citation: str) -> Rule:
    return Rule(rid=rid, citation=citation, label="x", jurisdiction="NYC")


def test_rule_with_fabricated_citation_is_flagged():
    check = make_statute_validity_check(_fake_exists)
    flag, reason = check(_rule("R1", "§20-875"))  # cites a section that isn't real
    assert flag is True and reason == "fabricated_citation"


def test_rule_with_real_citation_is_not_flagged():
    check = make_statute_validity_check(_fake_exists)
    flag, reason = check(_rule("R1", "NYC Admin. Code §20-870"))  # real section
    assert flag is False and reason == "cites_real_section"


def test_uncited_rule_falls_back_to_default():
    check = make_statute_validity_check(_fake_exists)
    flag, reason = check(_rule("R1", ""))  # no citation tokens to judge
    assert flag is True and reason == "unaligned"


def test_non_rule_node_behavior_unchanged():
    check = make_statute_validity_check(_fake_exists)
    flag, reason = check(Fact(fid="F1", label="some fact"))
    assert flag is True and reason == "unaligned"


def test_compute_discrepancies_default_flags_all_unaligned_rules():
    teacher = LegalReasoningGraph(case_id="E1", source=GraphSource.REFERENCE, model_name="t")
    student = LegalReasoningGraph(
        case_id="E1", source=GraphSource.AGENT, model_name="s", agent_id="gpt5",
        rules=[_rule("R1", "§20-875"), _rule("R2", "NYC Admin. Code §20-870")],
    )
    align = AlignmentReport(case_id="E1")  # nothing aligned → both rules unaligned
    base = compute_discrepancies(teacher, student, align)
    assert base.v_halluc_count == 2  # default flags every unaligned node


def test_compute_discrepancies_statute_check_spares_real_citation():
    teacher = LegalReasoningGraph(case_id="E1", source=GraphSource.REFERENCE, model_name="t")
    student = LegalReasoningGraph(
        case_id="E1", source=GraphSource.AGENT, model_name="s", agent_id="gpt5",
        rules=[_rule("R1", "§20-875"), _rule("R2", "NYC Admin. Code §20-870")],
    )
    align = AlignmentReport(case_id="E1")
    check = make_statute_validity_check(_fake_exists)
    grounded = compute_discrepancies(teacher, student, align, validity_check=check)
    # Only the fabricated-citation rule remains a hallucination.
    assert grounded.v_halluc_count == 1
    assert grounded.v_halluc[0].student_id == "R1"
