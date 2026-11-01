"""Tests for the checklist loop (src/lex_drl/checklist_loop.py). Fake student, fake embedding."""
from __future__ import annotations

import re

import numpy as np

from lex_drl.cases import Case
from lex_drl.checklist import Cluster, Item, cluster, missed_items, rank, render_checklist
from lex_drl.checklist_loop import (
    ChecklistLoopConfig, merge_items, run_checklist_loop, swap_failing, update_priorities,
)
from lex_drl.loop import score
from lex_drl.schema import Fact, GraphSource, LegalReasoningGraph, Obligation, Rule

AUDIT = ("NYC LL 144 §20-871(a)(1)", "Bias audit required within one year of use")
NOTICE = ("NYC LL 144 §20-872", "Candidate notice ten business days before use")
DUTY = "Commission a new independent bias audit"


def _case(cid, role):
    return Case(case_id=cid, title=cid, facts="An NYC employer used a hiring tool without an audit.",
                question="Assess compliance.", jurisdiction_tags=["NYC"], tier="easy", role=role,
                parties=["Acme"])


def _teacher(cid):
    return LegalReasoningGraph(
        case_id=cid, source=GraphSource.REFERENCE, model_name="t",
        facts=[Fact(fid="F1", label="Tool used without an audit")],
        rules=[Rule(rid="R1", citation=AUDIT[0], label=AUDIT[1], jurisdiction="NYC"),
               Rule(rid="R2", citation=NOTICE[0], label=NOTICE[1], jurisdiction="NYC")],
        obligations=[Obligation(oid="O1", label=DUTY, required_by="R1", status="mandatory",
                                jurisdiction="NYC")],
    )


def _graph(cid, rules=(), duty=False):
    return LegalReasoningGraph(
        case_id=cid, source=GraphSource.AGENT, model_name="s", agent_id="s",
        facts=[Fact(fid="F1", label="Tool used without an audit")],
        rules=[Rule(rid=f"R{i + 1}", citation=c, label=l, jurisdiction="NYC")
               for i, (c, l) in enumerate(rules)],
        obligations=[Obligation(oid="O1", label=DUTY, required_by="R1", status="mandatory",
                                jurisdiction="NYC")] if duty else [])


def obedient(case, notes, _t):
    """Writes every Rule the checklist names."""
    rules = re.findall(r'citation "([^"]+)" \([^)]*\): ([^\n]+)\.', notes)
    return _graph(case.case_id, rules, duty="Obligation node" in notes)


def deaf(case, _notes, _t):
    return _graph(case.case_id)


def embed(texts):
    vocab = sorted({w for t in texts for w in t.lower().split()})
    m = np.array([[t.lower().split().count(w) for w in vocab] for t in texts], dtype=float)
    return m / np.linalg.norm(m, axis=1, keepdims=True)


def _run(student, rounds=3):
    train = [_case("T1", "training"), _case("T2", "training")]
    test = [_case("X1", "test")]
    teachers = {c.case_id: _teacher(c.case_id) for c in train + test}
    return run_checklist_loop(train, test, teachers, student, embed,
                              ChecklistLoopConfig(k=3, max_rounds=rounds, patience=1))


def test_obedient_student_learns_then_stops():
    res = _run(obedient)
    r0, r1 = res.rounds[0], res.rounds[1]
    assert r1.mean_lged_test < r0.mean_lged_test and r1.mean_lged_train < r0.mean_lged_train
    assert r1.resolved_train > 0
    assert res.best_round == 1
    assert res.stop_reason in ("fixpoint", "plateau")


def test_deaf_student_never_improves_and_items_are_demoted():
    res = _run(deaf, rounds=2)
    assert all(r.mean_lged_test == res.rounds[0].mean_lged_test for r in res.rounds)
    assert res.best_round == 0 and res.stop_reason == "plateau"
    last = res.stores[max(res.stores)]
    assert last and all(c["priority"] < 0 for c in last if c["given"])


def test_round_one_is_the_single_pass_checklist():
    train = [_case("T1", "training"), _case("T2", "training")]
    teachers = {c.case_id: _teacher(c.case_id) for c in train + [_case("X1", "test")]}
    items = []
    for c in train:
        rep, _ = score(teachers[c.case_id], deaf(c, "", 0))
        items += missed_items(c, rep, teachers[c.case_id])
    expected = render_checklist(rank(cluster(items), _case("X1", "test"), "combined", embed=embed)[:3])
    seen = {}

    def spy(case, notes, t):
        seen[(case.case_id, t)] = notes
        return deaf(case, notes, t)

    train2 = [_case("T1", "training"), _case("T2", "training")]
    run_checklist_loop(train2, [_case("X1", "test")], teachers, spy, embed,
                       ChecklistLoopConfig(k=3, max_rounds=1))
    assert seen[("X1", 0)] == "" and seen[("X1", 1)] == expected


def test_priorities_swaps_and_merging():
    it = lambda case, label, w=4.0: Item("R", "NYC §20-871", "nyc", label, w,
                                         frozenset({"nyc:20-871"}), case)
    cs = [Cluster("R", frozenset({"nyc:20-871"}), "nyc", [it("T1", "audit A"), it("T2", "audit B", 2.0)])]
    assert merge_items(cs, [it("T1", "audit A"), it("T3", "audit C")]) == 0
    assert len(cs[0].items) == 3 and cs[0].support == 3
    cs[0].given, cs[0].useful, cs[0].resolved = 4, 3, 0
    update_priorities(cs)
    assert cs[0].priority == -1.0
    assert cs[0].representative().label == "audit A"
    assert swap_failing(cs, max_swaps=1) == 1 and cs[0].representative().label != "audit A"
    assert swap_failing(cs, max_swaps=1) == 0          # limit reached
