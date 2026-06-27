"""Case-specific mining tests (Task 4d).

Hermetic — tiny in-memory graphs, no network, no data files. Locks in the
LEGAL_LEXICON extension and a couple of case-grounded behaviours used by the
run_patch_mining driver.
"""
from __future__ import annotations

from lex_drl.cases import Case
from lex_drl.discrepancy import DiscrepancyReport, MissingNode
from lex_drl.patch_generator import LEGAL_LEXICON, generate_patches
from lex_drl.schema import Authority, GraphSource, LegalReasoningGraph, Rule


def _case(cid="M1", role="training", juris=("CO",)):
    return Case(case_id=cid, title="t", facts="f", question="q",
                jurisdiction_tags=list(juris), tier="medium", role=role)


def _teacher(rules):
    return LegalReasoningGraph(case_id="M1", source=GraphSource.REFERENCE,
                               model_name="opus", rules=rules)


def _student():
    return LegalReasoningGraph(case_id="M1", source=GraphSource.AGENT,
                               model_name="llama3_2b", agent_id="llama3_2b")


def _report(v_miss):
    return DiscrepancyReport(case_id="M1", student_id="llama3_2b", v_miss=v_miss)


def test_extended_lexicon_terms_present():
    # Sanity: the Task 4c additions are actually in the lexicon.
    for term in ["selection rate", "impact ratio", "preemption", "promotion"]:
        assert term in LEGAL_LEXICON


def test_new_lexicon_term_flows_into_keywords():
    # A rule whose label uses an *extended* concept term should surface it as a
    # trigger keyword (drives BM25 retrieval in run_patch_injection).
    rule = Rule(rid="R3", citation="NYC LL 144 §20-871(b)",
                label="bias audit must report selection rate and impact ratio per category",
                authority=Authority.BINDING, jurisdiction="NYC")
    report = _report([MissingNode(teacher_id="R3", node_type="R", label=rule.label, weight=2.0)])
    patches = generate_patches(report, _teacher([rule]), _student(), _case(juris=("NYC",)))
    kws = patches[0].trigger_keywords
    assert "selection rate" in kws and "impact ratio" in kws


def test_co_deployer_rule_mines_colorado_jurisdiction():
    rule = Rule(rid="R1", citation="Colo. Rev. Stat. §6-1-1703",
                label="deployer must use reasonable care and complete an impact assessment",
                authority=Authority.BINDING, jurisdiction="CO")
    report = _report([MissingNode(teacher_id="R1", node_type="R", label=rule.label, weight=2.5)])
    p = generate_patches(report, _teacher([rule]), _student(), _case())[0]
    assert p.jurisdiction == "colorado"
    assert "6-1-1703" in p.controlling_authority
    assert "deployer" in p.trigger_keywords and "impact assessment" in p.trigger_keywords
