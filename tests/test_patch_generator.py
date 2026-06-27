"""Tests for patch_generator: families, selection, keywords, dedup, determinism."""
from __future__ import annotations

import pytest

from lex_drl.cases import Case
from lex_drl.discrepancy import DiscrepancyReport, MissingNode, Misgrounding
from lex_drl.patch_generator import generate_patches, dedup_merge, generate_all
from lex_drl.schema import (
    Authority, GraphSource, LegalReasoningGraph, Obligation, ObligationStatus, Rule,
)


def _case(cid="E1", role="training", juris=("NYC",)):
    return Case(case_id=cid, title="t", facts="f", question="q",
                jurisdiction_tags=list(juris), tier="easy", role=role)


def _teacher(rules=None, obligations=None, edges=None):
    return LegalReasoningGraph(
        case_id="E1", source=GraphSource.REFERENCE, model_name="opus",
        rules=rules or [], obligations=obligations or [], edges=edges or [],
    )


def _student():
    return LegalReasoningGraph(case_id="E1", source=GraphSource.AGENT,
                              model_name="gpt5", agent_id="gpt5")


def _report(v_miss=None, v_misground=None):
    return DiscrepancyReport(case_id="E1", student_id="gpt5",
                             v_miss=v_miss or [], v_misground=v_misground or [])


def test_train_guard_rejects_test_case():
    with pytest.raises(ValueError):
        generate_patches(_report(), _teacher(), _student(), _case(role="test"))


def test_missing_binding_rule_makes_patch():
    rule = Rule(rid="R7", citation="NYC §20-875", label="penalties for AEDT misuse",
                authority=Authority.BINDING, jurisdiction="NYC")
    teacher = _teacher(rules=[rule])
    report = _report(v_miss=[MissingNode(teacher_id="R7", node_type="R",
                                         label=rule.label, weight=4.0)])
    patches = generate_patches(report, teacher, _student(), _case())
    assert len(patches) == 1
    p = patches[0]
    assert p.patch_family == "missing_rule" and p.node_types_addressed == ["R"]
    assert "20-875" in p.controlling_authority and p.jurisdiction == "nyc"
    assert "penalties" in p.trigger_keywords  # lexicon concept
    assert "greenleaf" not in " ".join(p.trigger_keywords).lower()  # no party leak


def test_advisory_rule_and_fact_are_filtered():
    rule = Rule(rid="R9", citation="NIST RMF", label="risk framework",
                authority=Authority.ADVISORY, jurisdiction="US")
    teacher = _teacher(rules=[rule])
    report = _report(v_miss=[
        MissingNode(teacher_id="R9", node_type="R", label="risk framework", weight=1.5),
        MissingNode(teacher_id="F3", node_type="F", label="some fact", weight=1.0),
    ])
    assert generate_patches(report, teacher, _student(), _case()) == []


def test_missing_obligation_resolves_authority_and_deadline():
    rule = Rule(rid="R2", citation="NYC §20-871", label="audit duty",
                authority=Authority.BINDING, jurisdiction="NYC")
    obl = Obligation(oid="O1", label="commission a new bias audit", required_by="R2",
                     status=ObligationStatus.MANDATORY, jurisdiction="NYC",
                     deadline="before further use")
    teacher = _teacher(rules=[rule], obligations=[obl])
    report = _report(v_miss=[MissingNode(teacher_id="O1", node_type="O",
                                         label=obl.label, weight=2.5)])
    p = generate_patches(report, teacher, _student(), _case())[0]
    assert p.patch_family == "missing_obligation"
    assert "20-871" in p.controlling_authority           # resolved via required_by
    assert "before further use" in p.prevention_step     # deadline rendered


def test_future_effective_date_contraindication():
    rule = Rule(rid="R8", citation="CO §6-1-1703", label="deployer duty",
                authority=Authority.BINDING, jurisdiction="Colorado",
                effective_as_of="2026-06-30")
    teacher = _teacher(rules=[rule])
    report = _report(v_miss=[MissingNode(teacher_id="R8", node_type="R",
                                         label="deployer duty", weight=4.0)])
    p = generate_patches(report, teacher, _student(), _case(juris=("CO",)))[0]
    assert "not yet enforceable" in p.contraindication.lower()


def test_misgrounding_family():
    rule = Rule(rid="R1", citation="NYC §20-870", label="AEDT definition",
                authority=Authority.BINDING, jurisdiction="NYC")
    teacher = _teacher(rules=[rule])
    mg = Misgrounding(teacher_id="R1", student_id="R1", teacher_citation="NYC §20-870",
                      student_citation="§20-871", proposition="AEDT definition",
                      student_section_exists=False, weight=4.0)
    p = generate_patches(_report(v_misground=[mg]), teacher, _student(), _case())[0]
    assert p.patch_family == "misgrounding"
    assert "20-870" in p.controlling_authority and "20-871" in p.prevention_step


def test_dedup_merges_same_authority_across_cases():
    rule = Rule(rid="R8", citation="CO §6-1-1703(2)(b)", label="impact assessment",
                authority=Authority.BINDING, jurisdiction="Colorado")
    t = _teacher(rules=[rule])
    m1 = generate_patches(
        _report(v_miss=[MissingNode(teacher_id="R8", node_type="R", label=rule.label, weight=4.0)]),
        t, _student(), _case(cid="M1"))
    h1 = generate_patches(
        _report(v_miss=[MissingNode(teacher_id="R8", node_type="R", label=rule.label, weight=4.0)]),
        t, _student(), _case(cid="H1"))
    merged = dedup_merge(m1 + h1)
    assert len(merged) == 1
    assert merged[0].source_cases == ["H1", "M1"]


def test_determinism_with_no_insight():
    rule = Rule(rid="R7", citation="NYC §20-875", label="penalties",
                authority=Authority.BINDING, jurisdiction="NYC")
    teacher = _teacher(rules=[rule])
    report = _report(v_miss=[MissingNode(teacher_id="R7", node_type="R",
                                         label="penalties", weight=4.0)])
    a = generate_patches(report, teacher, _student(), _case(), insight=None)
    b = generate_patches(report, teacher, _student(), _case(), insight=None)
    assert [p.model_dump() for p in a] == [p.model_dump() for p in b]
