"""Tests for the patch diagnostics (src/lex_drl/diagnostics.py). No model, no API."""
from __future__ import annotations

import pytest

from lex_drl.cases import Case
from lex_drl.diagnostics import (
    canonical_citation, collapse_counts, directive_notes, lged_components,
    oracle_selection, placebo_patches, ro_ceiling, taken_up, teacher_without,
)
from lex_drl.loop import score
from lex_drl.patch_generator import dedup_merge, generate_patches
from lex_drl.patch_store import Patch
from lex_drl.schema import (
    Edge, Fact, GraphSource, LegalReasoningGraph, Obligation, Rule,
)

AUDIT = "NYC LL 144 §20-871(a)(1)"
NOTICE = "NYC LL 144 §20-872"
FAKE = "NYC LL 144 §20-875"


class _Index:
    """Stand-in statute index: §20-875 does not exist."""

    def classify_citation(self, citation):
        return "fabricated" if "20-875" in citation else "verified"


def _case(role="test", tags=("NYC",)):
    return Case(case_id="X1", title="X1", facts="An NYC employer used a screening tool.",
                question="Assess compliance.", jurisdiction_tags=list(tags), tier="easy",
                role=role, parties=["Acme"])


def _teacher():
    return LegalReasoningGraph(
        case_id="X1", source=GraphSource.REFERENCE, model_name="teacher",
        facts=[Fact(fid="F1", label="Tool used without an audit")],
        rules=[
            Rule(rid="R1", citation=AUDIT, label="Bias audit within one year of use",
                 jurisdiction="NYC"),
            Rule(rid="R2", citation=NOTICE, label="Notice ten business days before use",
                 jurisdiction="NYC"),
            Rule(rid="R3", citation=FAKE, label="Penalties for repeat violations",
                 jurisdiction="NYC"),
        ],
        obligations=[
            Obligation(oid="O1", label="Commission an independent bias audit",
                       required_by="R1", status="mandatory", jurisdiction="NYC"),
            Obligation(oid="O2", label="Pay the escalating penalty", required_by="R3",
                       status="mandatory", jurisdiction="NYC"),
        ],
        edges=[Edge(eid="E1", src="R1", dst="O1", type="triggers"),
               Edge(eid="E2", src="R3", dst="O2", type="triggers")],
    )


def _empty_student():
    return LegalReasoningGraph(case_id="X1", source=GraphSource.AGENT, model_name="s",
                               agent_id="s", facts=[Fact(fid="F1", label="Tool used without an audit")])


def _patch(pid, cite, juris, family="missing_rule"):
    return Patch(patch_id=pid, patch_family=family, trigger_keywords=[juris],
                 controlling_authority=cite, prevention_step=f"Apply {cite}.",
                 node_types_addressed=["R"], source_cases=["T1"], jurisdiction=juris)


# ── citations ──

@pytest.mark.parametrize("cite,want", [
    ("CO AIA § 6-1-1703(3)(a)", {"colorado:6-1-1703"}),
    ("Colorado AIA SB 24-205 Section 6-1-1703", {"colorado:6-1-1703"}),
    ("NYC LL 144 §20-871(a)(1); DCWP Rules §5-301(a)", {"nyc:20-871", "nyc:5-301"}),
    ("TRAIGA §551.001(1)", {"texas:551.001"}),
    ("no citation here", set()),
])
def test_canonical_citation(cite, want):
    assert canonical_citation(cite) == want


def test_dedup_canonical_merges_formats_but_default_does_not():
    ps = [_patch("a", "CO AIA § 6-1-1703(2)", "colorado"),
          _patch("b", "Colorado AIA Section 6-1-1703", "colorado")]
    assert len(dedup_merge(ps)) == 2                       # unchanged default
    merged = dedup_merge(ps, canonical=True)
    assert len(merged) == 1 and merged[0].patch_id == "a"
    assert collapse_counts(ps) == {"patches": 2, "distinct_exact": 2,
                                   "distinct_canonical": 1, "distinct_sections": 1}


# ── ceiling and teacher errors ──

def test_ceiling_counts_heaviest_rule_and_obligation_nodes():
    report, _ = score(_teacher(), _empty_student())
    comp = lged_components(report)
    ceil = ro_ceiling(report, ns=(1, None))
    weights = sorted((m.weight for m in report.v_miss if m.node_type in "RO"), reverse=True)
    assert ceil["1"] == weights[0]
    assert ceil["all"] == pytest.approx(comp["miss_R"] + comp["miss_O"])


def test_teacher_without_drops_rule_its_obligations_and_edges():
    clean = teacher_without(_teacher(), ["R3"])
    assert [r.rid for r in clean.rules] == ["R1", "R2"]
    assert [o.oid for o in clean.obligations] == ["O1"]
    assert [e.eid for e in clean.edges] == ["E1"]
    assert teacher_without(_teacher(), []) is not None


# ── oracle ──

def test_oracle_uses_only_this_cases_gaps_and_skips_fabricated():
    teacher, student = _teacher(), _empty_student()
    report, _ = score(teacher, student)
    sel = oracle_selection(_case(), report, teacher, student, None, index=_Index())
    nodes = [nid for _, nid in sel]
    assert "R3" not in nodes and "O2" not in nodes        # fabricated §20-875 left out
    assert set(nodes) <= {m.teacher_id for m in report.v_miss}
    assert all("20-875" not in p.controlling_authority for p, _ in sel)
    assert len(oracle_selection(_case(), report, teacher, student, 1, index=_Index())) == 1


def test_oracle_leaves_the_real_miner_guard_in_place():
    teacher, student = _teacher(), _empty_student()
    report, _ = score(teacher, student)
    case = _case(role="test")
    oracle_selection(case, report, teacher, student, 2)
    assert case.role == "test"
    with pytest.raises(ValueError):
        generate_patches(report, teacher, student, case)


def test_directive_names_the_same_nodes_as_the_oracle():
    teacher, student = _teacher(), _empty_student()
    report, _ = score(teacher, student)
    sel = oracle_selection(_case(), report, teacher, student, None, index=_Index())
    text = directive_notes([nid for _, nid in sel], teacher)
    assert text.startswith("REQUIRED ELEMENTS")
    assert text.count("\n") - 1 == len(sel)
    for _, nid in sel:
        node = next(n for n in teacher.rules + teacher.obligations
                    if getattr(n, "rid", None) == nid or getattr(n, "oid", None) == nid)
        assert node.label in text
    assert directive_notes([], teacher) == ""


# ── placebo and uptake ──

def test_placebo_never_touches_the_case_and_prefers_other_jurisdictions():
    store = [
        _patch("in1", "NYC LL 144 §20-871(b)", "nyc"),              # same section as R1
        _patch("in2", "DCWP Rules §5-303", "nyc"),                  # unrelated NYC section
        _patch("co1", "CO AIA §6-1-1703", "colorado"),
        _patch("co2", "CO AIA §6-1-1704", "colorado"),
        _patch("tx1", "TRAIGA §551.101", "texas"),
    ]
    picked = placebo_patches(_case(), _teacher(), store, k=3)
    ids = {p.patch_id for p in picked}
    assert "in1" not in ids
    assert ids == {"co1", "co2", "tx1"}
    assert placebo_patches(_case(), _teacher(), store, k=3) == picked   # seeded
    assert {p.patch_id for p in placebo_patches(_case(), _teacher(), store, k=4)} \
        == {"co1", "co2", "tx1", "in2"}


def test_taken_up_matches_section_whatever_the_format():
    student = _empty_student().model_copy(update={"rules": [
        Rule(rid="R1", citation="Section 20-871", label="audit", jurisdiction="NYC")]})
    assert taken_up(_patch("a", AUDIT, "nyc"), student)
    assert not taken_up(_patch("b", NOTICE, "nyc"), student)
