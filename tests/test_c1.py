"""Tests for the loop guard and checklist patches (C1). No model, no API."""
from __future__ import annotations

import numpy as np
import pytest

from lex_drl.cases import Case
from lex_drl.checklist import (
    HEADER, Cluster, Gap, Item, cluster, coverage, match_gaps, missed_items, rank,
    render_checklist,
)
from lex_drl.discrepancy import DiscrepancyReport, MissingNode
from lex_drl.loopguard import LoopGuard, loop_start, truncate_loop
from lex_drl.schema import GraphSource, LegalReasoningGraph, Obligation, Rule

# ── loop guard ──

RULE = ('    {{"rid": "R{n}", "citation": "NYC LL 144 §20-873", "label": "NYC Local Law 144 '
        'Section 20-873", "authority": "binding", "jurisdiction": "NYC"}},\n')


def test_guard_cuts_before_the_third_identical_node():
    head = "=== JSON GRAPH ===\n{\n  \"rules\": [\n"
    text = head + "".join(RULE.format(n=i) for i in range(1, 8))
    cut, looped = truncate_loop(text)
    assert looped
    assert cut == head + RULE.format(n=1) + RULE.format(n=2)


def test_guard_ignores_prose_brackets_and_distinct_nodes():
    prose = "- **Authority**: Binding statute, effective January 1, 2026.\n" * 5
    brackets = "    ],\n    {\n" * 10
    distinct = "".join(
        f'    {{"rid": "R{i}", "citation": "§20-87{i}", "label": "rule number {i} about audits"}},\n'
        for i in range(1, 9))
    text = prose + brackets + distinct
    assert truncate_loop(text) == (text, False)


def test_guard_caps_one_node_type_but_not_edges():
    many = "".join(f'{{"rid": "R{i}", "citation": "§20-{900 + i}", "label": "invented section {i}"}}\n'
                   for i in range(1, 40))
    assert loop_start(many) is not None
    assert many[:loop_start(many)].count('"rid"') == 30
    edges = "".join(f'{{"eid": "E{i}", "src": "R{i}", "dst": "O{i}", "type": "triggers"}}\n'
                    for i in range(1, 60))
    assert loop_start(edges) is None


def test_guard_judges_complete_lines_only():
    partial = RULE.format(n=1) + RULE.format(n=2) + RULE.format(n=3).rstrip("\n")
    assert loop_start(partial) is None


class _Tok:
    """Character-level fake tokenizer: one id per character."""

    def decode(self, ids, **_):
        return "".join(chr(int(i)) for i in ids)


def test_stopping_criterion_agrees_with_truncation():
    prompt = "PROMPT"
    text = "".join(RULE.format(n=i) for i in range(1, 6))
    ids = [ord(ch) for ch in prompt + text]
    guard = LoopGuard(_Tok(), prompt_len=len(prompt))
    stop_at = next(t for t in range(len(prompt) + 1, len(ids) + 1)
                   if guard(np.array([ids[:t]]), None))
    generated = "".join(chr(i) for i in ids[len(prompt):stop_at])
    cut, _ = truncate_loop(text)
    assert generated.startswith(cut) and generated[len(cut):].count("\n") == 1


# ── checklist ──

def _case(cid="T1", role="training", tags=("CO",)):
    return Case(case_id=cid, title=cid, facts="A Colorado lender used an AI underwriting model.",
                question="Assess compliance.", jurisdiction_tags=list(tags), tier="medium",
                role=role, parties=["Acme"])


def _teacher():
    return LegalReasoningGraph(
        case_id="T1", source=GraphSource.REFERENCE, model_name="teacher",
        rules=[Rule(rid="R1", citation="CO AIA §6-1-1703(3)(a)", label="Impact assessment before deployment",
                    jurisdiction="Colorado"),
               Rule(rid="R2", citation="NYC LL 144 §20-875", label="Penalties", jurisdiction="NYC"),
               Rule(rid="R3", citation="CO AIA §6-1-1704", label="Acme must notify the AG",
                    jurisdiction="Colorado")],
        obligations=[Obligation(oid="O1", label="Complete an impact assessment", required_by="R1",
                                status="mandatory", jurisdiction="Colorado", deadline="2026-06-30")],
    )


def _report():
    return DiscrepancyReport(case_id="T1", l_ged=0.0, v_miss=[
        MissingNode(teacher_id="R1", node_type="R", label="", weight=4.0),
        MissingNode(teacher_id="R2", node_type="R", label="", weight=4.0),
        MissingNode(teacher_id="R3", node_type="R", label="", weight=4.0),
        MissingNode(teacher_id="O1", node_type="O", label="", weight=2.5),
    ])


class _Index:
    def classify_citation(self, c):
        return "fabricated" if "20-875" in c else "verified"


def test_items_skip_fabricated_and_party_labels_and_refuse_test_cases():
    items = missed_items(_case(), _report(), _teacher(), index=_Index(), party_names=["Acme"])
    assert [(i.kind, i.citation) for i in items] == [
        ("R", "CO AIA §6-1-1703(3)(a)"), ("O", "CO AIA §6-1-1703(3)(a)")]
    assert items[1].deadline == "2026-06-30" and items[1].status == "mandatory"
    with pytest.raises(ValueError):
        missed_items(_case(role="test"), _report(), _teacher())


def _item(kind, cite, label, case, w=4.0, juris="colorado"):
    from lex_drl.patch_generator import canonical_citation
    return Item(kind=kind, citation=cite, jurisdiction=juris, label=label, weight=w,
                sections=canonical_citation(cite, juris), source_case=case)


def test_clusters_merge_formats_and_count_support():
    cs = cluster([_item("R", "CO AIA §6-1-1703(3)", "Impact assessment", "T1"),
                  _item("R", "Colorado AIA Section 6-1-1703", "Impact assessment yearly", "T2"),
                  _item("O", "CO AIA §6-1-1703", "Complete assessment", "T1", w=2.5),
                  _item("R", "NYC LL 144 §20-871", "Bias audit", "T3", juris="nyc")])
    by = {c.key: c for c in cs}
    assert by["R|colorado:6-1-1703"].support == 2
    assert by["R|colorado:6-1-1703"].representative().label == "Impact assessment"
    ranked = rank(cs, _case(role="test"), "support")
    assert [c.key for c in ranked] == ["R|colorado:6-1-1703", "O|colorado:6-1-1703"]   # NYC gated out


def _fake_embed(texts):
    """Bag-of-words vectors, L2-normalised."""
    vocab = sorted({w for t in texts for w in t.lower().split()})
    m = np.array([[t.lower().split().count(w) for w in vocab] for t in texts], dtype=float)
    return m / np.linalg.norm(m, axis=1, keepdims=True)


def test_match_gaps_needs_kind_section_and_similar_label():
    c_rule = Cluster("R", frozenset({"colorado:6-1-1703"}), "colorado",
                     [_item("R", "CO AIA §6-1-1703", "impact assessment before deployment", "T1")])
    gaps = [Gap("R7", "R", "impact assessment before deployment annually", 4.0, frozenset({"colorado:6-1-1703"})),
            Gap("O2", "O", "impact assessment before deployment", 2.5, frozenset({"colorado:6-1-1703"})),
            Gap("R9", "R", "consumer appeal rights", 4.0, frozenset({"colorado:6-1-1703"}))]
    assert [g.teacher_id for g in match_gaps([c_rule], gaps, embed=_fake_embed)] == ["R7"]
    loose = match_gaps([c_rule], gaps)                  # section + kind only: heaviest R
    assert loose[0].kind == "R"
    assert coverage([c_rule], gaps, 1, embed=_fake_embed)["weight"] == 4.0


def test_render_checklist_lines():
    cs = cluster([_item("R", "CO AIA §6-1-1703", "Impact assessment", "T1"),
                  _item("O", "CO AIA §6-1-1704", "Notify the AG", "T1", w=2.5)])
    cs[1].items[0].status, cs[1].items[0].deadline = "mandatory", "2026-06-30"
    text = render_checklist(cs)
    assert text.startswith(HEADER)
    assert '1. A Rule node with citation "CO AIA §6-1-1703" (colorado, binding): Impact assessment.' in text
    assert "2. An Obligation node (mandatory, required by CO AIA §6-1-1704): Notify the AG. Deadline: 2026-06-30." in text
    assert render_checklist([]) == ""


# ── repair: resume a looping answer at the next JSON section ──

from lex_drl.repair import generate_with_repair, resume_prefix  # noqa: E402


def _looping_answer():
    head = 'Analysis.\n=== JSON GRAPH ===\n{\n  "facts": [\n    {"fid": "F1", "label": "fact one about the tool"}\n  ],\n  "rules": [\n'
    return head + "".join(RULE.format(n=i) for i in range(1, 9)), head


def test_resume_prefix_closes_the_looping_list_and_opens_the_next():
    text, head = _looping_answer()
    cut, _ = truncate_loop(text)
    prefix = resume_prefix(cut)
    assert prefix.startswith(head + RULE.format(n=1) + RULE.format(n=2).rstrip().rstrip(","))
    assert prefix.endswith('\n  ],\n  "applications": [\n')
    assert resume_prefix('=== JSON GRAPH ===\n{"edges": [\n {"eid": "E1", "src": "R1"},\n') is None


class _FakeClient:
    model = "fake"

    def __init__(self, first, continuations):
        self.first, self.conts, self.prefixes = first, list(continuations), []

    def generate(self, system, user):
        return type("R", (), {"text": self.first})()

    def continue_from(self, system, user, prefix):
        self.prefixes.append(prefix)
        return type("R", (), {"text": self.conts.pop(0)})()


def test_repair_leaves_clean_answers_alone_and_resumes_loops():
    clean = _FakeClient("no loop here", [])
    r = generate_with_repair(clean, "s", "u")
    assert (r.text, r.looped, r.repairs) == ("no loop here", False, 0)

    text, _ = _looping_answer()
    rest = '    {"aid": "A1", "rule_ref": "R1", "reasoning": "applies"}\n  ]\n}\n'
    c = _FakeClient(text, [rest])
    r = generate_with_repair(c, "s", "u")
    assert r.looped and r.repairs == 1 and not r.still_looped
    assert r.text == c.prefixes[0] + rest
    assert r.text.count('"rid"') == 2


def test_repair_gives_up_after_the_limit():
    text, _ = _looping_answer()
    again = "".join(RULE.format(n=i) for i in range(20, 26))     # loops again every time
    c = _FakeClient(text, [again] * 5)
    r = generate_with_repair(c, "s", "u", max_repairs=2)
    assert r.still_looped and r.repairs == 2 and len(c.prefixes) == 2


def test_answer_that_stops_at_the_marker_is_resumed_with_a_brace():
    from lex_drl.repair import stopped_at_marker

    text = "PART 1 analysis.\n\n=== JSON GRAPH ===\n"
    assert stopped_at_marker(text) and not stopped_at_marker(text + "{}")
    assert not stopped_at_marker("no marker here")
    rest = '  "facts": [\n    {"fid": "F1", "label": "a fact"}\n  ]\n}\n'
    c = _FakeClient(text, [rest])
    r = generate_with_repair(c, "s", "u")
    assert r.empty_json and not r.looped
    assert c.prefixes == ["PART 1 analysis.\n\n=== JSON GRAPH ===\n{\n"]
    assert r.text == c.prefixes[0] + rest
