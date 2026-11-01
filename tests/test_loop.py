"""Tests for the iterative patch loop (src/lex_drl/loop.py).

No model and no API: the student is a function that reads the injected notes
and decides which rules to write, so each test states exactly how the
"student" responds to patches.
"""
from __future__ import annotations

import pytest

from lex_drl import loop
from lex_drl.cases import Case
from lex_drl.loop import (
    LoopConfig, empty_graph, merge_mined, patch_outcome, patch_targets,
    plateau_round, rewrite_is_acceptable, run_loop, score, update_priorities,
)
from lex_drl.patch_store import Patch, PatchStore
from lex_drl.schema import (
    Application, Conclusion, Fact, GraphSource, Issue, LegalReasoningGraph,
    Obligation, Rule,
)

AUDIT = "NYC LL 144 §20-871(a)(1)"
NOTICE = "NYC LL 144 §20-872"
AUDIT_LABEL = "Bias audit required no more than one year before use of the tool"
NOTICE_LABEL = "Candidate notice required at least ten business days before use"
DUTY_LABEL = "Commission a new bias audit from an independent auditor"

FACTS = ("The employer in NYC used a screening tool without a bias audit and "
         "gave candidates no notice before use.")


def _case(cid: str, role: str) -> Case:
    return Case(case_id=cid, title=cid, facts=FACTS, question="Assess compliance.",
                jurisdiction_tags=["NYC"], tier="easy", role=role, parties=["Acme"])


def _teacher(cid: str) -> LegalReasoningGraph:
    return LegalReasoningGraph(
        case_id=cid, source=GraphSource.REFERENCE, model_name="teacher",
        facts=[Fact(fid="F1", label="Tool used without an audit")],
        issues=[Issue(iid="I1", label="Was a bias audit required?")],
        rules=[
            Rule(rid="R1", citation=AUDIT, label=AUDIT_LABEL, jurisdiction="NYC"),
            Rule(rid="R2", citation=NOTICE, label=NOTICE_LABEL, jurisdiction="NYC"),
        ],
        applications=[Application(aid="A1", rule_ref="R1", fact_refs=["F1"], issue_ref="I1",
                                  result="violated", reasoning="No audit was performed.")],
        conclusions=[Conclusion(cid="C1", determination="non-compliant", support_refs=["A1"])],
        obligations=[Obligation(oid="O1", label=DUTY_LABEL, required_by="R1",
                                status="mandatory", jurisdiction="NYC")],
    )


def _student_graph(cid: str, *, audit=False, notice=False, duty=False,
                   wrong_audit_cite=False) -> LegalReasoningGraph:
    rules, obligations = [], []
    if audit:
        cite = "NYC Admin. Code §20-999" if wrong_audit_cite else AUDIT
        rules.append(Rule(rid="R1", citation=cite, label=AUDIT_LABEL, jurisdiction="NYC"))
    if notice:
        rules.append(Rule(rid=f"R{len(rules) + 1}", citation=NOTICE, label=NOTICE_LABEL,
                          jurisdiction="NYC"))
    if duty:
        obligations.append(Obligation(oid="O1", label=DUTY_LABEL, required_by="R1",
                                      status="mandatory", jurisdiction="NYC"))
    return LegalReasoningGraph(
        case_id=cid, source=GraphSource.AGENT, model_name="fake", agent_id="fake",
        facts=[Fact(fid="F1", label="Tool used without an audit")],
        rules=rules, obligations=obligations,
    )


def obedient_student(case, notes, _round):
    """Writes exactly the rules and duties the notes mention."""
    return _student_graph(case.case_id,
                          audit="20-871(a)(1)" in notes and "apply" in notes,
                          notice="20-872" in notes,
                          duty="imposes a mandatory obligation" in notes)


def deaf_student(case, _notes, _round):
    """Ignores every note."""
    return _student_graph(case.case_id)


@pytest.fixture
def corpus():
    train = [_case("T1", "training"), _case("T2", "training")]
    test = [_case("X1", "test")]
    teachers = {c.case_id: _teacher(c.case_id) for c in train + test}
    return train, test, teachers


# ── round mechanics ──────────────────────────────────────────

def test_round_zero_is_the_unpatched_baseline(corpus):
    train, test, teachers = corpus
    seen = []

    def student(case, notes, t):
        seen.append((t, case.case_id, notes))
        return deaf_student(case, notes, t)

    run_loop(train, test, teachers, student, LoopConfig(k=1, max_rounds=1))
    assert all(notes == "" for t, _cid, notes in seen if t == 0)
    assert any(notes for t, _cid, notes in seen if t == 1)   # round 1 is patched


def test_an_obedient_student_improves_then_reaches_a_fixpoint(corpus):
    train, test, teachers = corpus
    res = run_loop(train, test, teachers, obedient_student, LoopConfig(k=3, max_rounds=6))
    r0, last = res.rounds[0], res.rounds[-1]
    assert last.mean_lged_test < r0.mean_lged_test          # held-out cases improved
    assert last.mean_lged_train < r0.mean_lged_train
    assert last.ro_recovery_test == 1.0                     # every rule and duty recovered
    assert res.stop_reason in ("fixpoint", "plateau")
    assert res.best_round >= 1
    assert len(res.rounds) < 6                              # it stopped on its own


def test_a_student_that_ignores_notes_plateaus_at_round_zero(corpus):
    train, test, teachers = corpus
    res = run_loop(train, test, teachers, deaf_student,
                   LoopConfig(k=1, max_rounds=6, patience=2, rewrite=False))
    assert res.best_round == 0
    assert res.stop_reason in ("plateau", "fixpoint")
    assert {r.mean_lged_test for r in res.rounds} == {res.rounds[0].mean_lged_test}


def test_first_round_store_holds_one_patch_per_missed_rule_and_duty(corpus):
    train, test, teachers = corpus
    res = run_loop(train, test, teachers, deaf_student, LoopConfig(k=1, max_rounds=1))
    assert res.stores[0] == []                               # round 0 has no store
    families = sorted(p["patch_family"] for p in res.stores[1])
    assert families == ["missing_obligation", "missing_rule", "missing_rule"]
    # merged across the two training cases, so each records both as evidence
    assert all(p["source_cases"] == ["T1", "T2"] for p in res.stores[1])


# ── train/test separation ────────────────────────────────────

def test_test_cases_never_reach_the_miner(corpus, monkeypatch):
    train, test, teachers = corpus
    mined = []
    real = loop.generate_patches

    def spy(report, teacher, student, case, **kw):
        mined.append(case.case_id)
        return real(report, teacher, student, case, **kw)

    monkeypatch.setattr(loop, "generate_patches", spy)
    run_loop(train, test, teachers, deaf_student, LoopConfig(k=1, max_rounds=2))
    assert mined and set(mined) == {"T1", "T2"}


def test_a_training_case_cannot_be_passed_as_test(corpus):
    train, _test, teachers = corpus
    with pytest.raises(ValueError, match="training case"):
        run_loop(train, [train[0]], teachers, deaf_student)


def test_efficacy_is_recorded_from_training_cases_only(corpus):
    """With no training cases nothing is mined, so nothing is ever injected."""
    _train, test, teachers = corpus
    res = run_loop([], test, teachers, obedient_student, LoopConfig(k=3, max_rounds=3))
    assert res.stop_reason == "fixpoint"
    assert all(r.retrieved == [] for r in res.cases)


# ── efficacy ─────────────────────────────────────────────────

def test_patch_targets_and_outcome_for_each_family():
    teacher = _teacher("T1")
    rule_patch = Patch(patch_id="p1", patch_family="missing_rule",
                       controlling_authority=AUDIT, prevention_step="x")
    duty_patch = Patch(patch_id="p2", patch_family="missing_obligation",
                       controlling_authority=AUDIT, prevention_step="x")
    other = Patch(patch_id="p3", patch_family="missing_rule",
                  controlling_authority="CO AIA §6-1-1703(2)(a)", prevention_step="x")
    assert patch_targets(rule_patch, teacher) == ["R1"]
    assert patch_targets(duty_patch, teacher) == ["O1"]
    assert patch_targets(other, teacher) == []               # authority not in this case

    report, alignment = score(teacher, _student_graph("T1", audit=True))
    assert patch_outcome(rule_patch, teacher, report, alignment) == (1, 1)
    assert patch_outcome(duty_patch, teacher, report, alignment) == (1, 0)
    assert patch_outcome(other, teacher, report, alignment) == (0, 0)


def test_misgrounding_patch_is_resolved_only_when_the_citation_is_fixed():
    teacher = _teacher("T1")
    patch = Patch(patch_id="p1", patch_family="misgrounding",
                  controlling_authority=AUDIT, prevention_step="x")
    wrong = score(teacher, _student_graph("T1", audit=True, wrong_audit_cite=True))
    right = score(teacher, _student_graph("T1", audit=True))
    assert patch_outcome(patch, teacher, *wrong) == (1, 0)
    assert patch_outcome(patch, teacher, *right) == (1, 1)


# ── store update ─────────────────────────────────────────────

def test_merge_mined_adds_new_and_widens_existing():
    store = PatchStore()
    a = Patch(patch_id="pa", patch_family="missing_rule", controlling_authority=AUDIT,
              prevention_step="x", source_cases=["T1"], trigger_keywords=["nyc"])
    assert merge_mined(store, [a], round_idx=0) == 1
    again = a.model_copy(update={"source_cases": ["T2"], "trigger_keywords": ["nyc", "audit"]})
    assert merge_mined(store, [again], round_idx=3) == 0
    got = store.get("pa")
    assert got.source_cases == ["T1", "T2"]
    assert got.trigger_keywords == ["nyc", "audit"]
    assert got.round_added == 0                               # first sighting is kept


def test_priority_is_plus_one_proven_zero_untested_minus_one_failed():
    store = PatchStore()
    for pid, inj, res in (("proven", 4, 4), ("half", 4, 2), ("untested", 0, 0), ("failed", 4, 0)):
        store.add(Patch(patch_id=pid, patch_family="missing_rule", controlling_authority=AUDIT,
                        prevention_step="x", source_cases=["T1", "T2"],
                        n_injected=inj, n_resolved=res))
    update_priorities(store)
    pr = {p.patch_id: p.priority for p in store.all()}
    assert pr == {"proven": 1.0, "half": 0.0, "untested": 0.0, "failed": -1.0}


def test_round_one_is_plain_retrieval_because_nothing_is_tested_yet(corpus):
    """Round 1 must be the single-pass method: every priority is still zero."""
    train, test, teachers = corpus
    res = run_loop(train, test, teachers, deaf_student, LoopConfig(k=1, max_rounds=1))
    assert res.stores[1] and all(p["priority"] == 0.0 for p in res.stores[1])


def test_a_failed_patch_is_demoted_below_an_untested_one():
    store = PatchStore()
    for pid, auth, inj in (("failed", AUDIT, 3), ("untested", NOTICE, 0)):
        store.add(Patch(patch_id=pid, patch_family="missing_rule", controlling_authority=auth,
                        prevention_step="x", trigger_keywords=["nyc", "audit"],
                        verification="verified", n_injected=inj, n_resolved=0))
    update_priorities(store)
    assert store.retrieve("nyc audit", k=1)[0].patch_id == "untested"


def test_priority_changes_which_patch_is_retrieved():
    def build(priority_on: str) -> PatchStore:
        store = PatchStore()
        for pid, auth in (("pa", AUDIT), ("pb", NOTICE)):
            store.add(Patch(patch_id=pid, patch_family="missing_rule",
                            controlling_authority=auth, prevention_step="x",
                            trigger_keywords=["nyc", "audit"], verification="verified",
                            priority=1.0 if pid == priority_on else 0.0))
        return store

    assert build("pa").retrieve("nyc audit", k=1)[0].patch_id == "pa"
    assert build("pb").retrieve("nyc audit", k=1)[0].patch_id == "pb"


# ── rewrites ─────────────────────────────────────────────────

class _Writer:
    """Fake rewriter. ``text`` may use {authority}, filled per patch."""

    def __init__(self, text: str):
        self.text, self.calls = text, 0

    def rewrite_failed(self, fields, current, failure):
        self.calls += 1
        return self.text.format(authority=fields["controlling_authority"])


def needs_emphasis(case, notes, _round):
    """Only follows a note that says MUST."""
    return _student_graph(case.case_id, audit="MUST" in notes and "20-871(a)(1)" in notes,
                          notice="MUST" in notes and "20-872" in notes)


def test_a_failing_patch_is_rewritten_and_then_works(corpus):
    train, test, teachers = corpus
    writer = _Writer("When a tool screens candidates in NYC you MUST cite {authority} as a rule.")
    res = run_loop(train, test, teachers, needs_emphasis, LoopConfig(k=3, max_rounds=6),
                   writer=writer)
    assert writer.calls >= 1
    assert sum(r.rewritten for r in res.rounds) >= 1
    assert res.rounds[-1].mean_lged_test < res.rounds[0].mean_lged_test
    final = res.stores[max(res.stores)]
    rewritten = [p for p in final if p["version"] > 1]
    assert rewritten and all(p["history"] for p in rewritten)      # old text is kept


def test_rewrites_are_off_when_disabled(corpus):
    train, test, teachers = corpus
    writer = _Writer("you MUST cite {authority}")
    res = run_loop(train, test, teachers, needs_emphasis,
                   LoopConfig(k=3, max_rounds=3, rewrite=False), writer=writer)
    assert writer.calls == 0
    assert sum(r.rewritten for r in res.rounds) == 0


def test_rewrite_attempts_are_capped(corpus):
    train, test, teachers = corpus
    writer = _Writer("Cite {authority} as a rule in the analysis.")  # never says MUST
    res = run_loop(train, test, teachers, needs_emphasis,
                   LoopConfig(k=3, max_rounds=8, max_rewrites=1, patience=5), writer=writer)
    final = res.stores[max(res.stores)]
    assert max(p["n_rewrite_attempts"] for p in final) <= 1


def test_rewrite_guardrails():
    patch = Patch(patch_id="p", patch_family="missing_rule", controlling_authority=AUDIT,
                  prevention_step="When a matter involves 20-871(a)(1), apply it.")
    parties = ["Greenleaf", "ResumeRank"]
    ok = "Before an employer uses a screening tool, cite §20-871(a)(1): a bias audit is required."
    assert rewrite_is_acceptable(patch, ok, parties)
    assert not rewrite_is_acceptable(patch, "", parties)
    assert not rewrite_is_acceptable(patch, patch.prevention_step, parties)          # unchanged
    assert not rewrite_is_acceptable(patch, ok + " As Greenleaf did.", parties)      # names a party
    assert not rewrite_is_acceptable(patch, ok + " See also §20-875.", parties)      # new section
    assert not rewrite_is_acceptable(patch, "x" * 701, parties)                      # too long


def test_a_rejected_rewrite_leaves_the_patch_untouched(corpus):
    train, test, teachers = corpus
    writer = _Writer("Acme should have cited {authority}.")        # names a party → rejected
    res = run_loop(train, test, teachers, deaf_student, LoopConfig(k=3, max_rounds=3),
                   writer=writer, party_names=["Acme"])
    assert sum(r.rewritten for r in res.rounds) == 0
    assert sum(r.rewrites_rejected for r in res.rounds) >= 1
    final = res.stores[max(res.stores)]
    assert all(p["version"] == 1 and not p["history"] for p in final)


# ── leakage guard, unparsed answers, stop rule ───────────────

def test_patches_naming_a_training_party_are_never_injected(corpus):
    train, test, teachers = corpus
    for t in teachers.values():                       # teacher wording names the party
        t.rules[0].label = "Acme must obtain a bias audit within one year"
    res = run_loop(train, test, teachers, deaf_student, LoopConfig(k=3, max_rounds=1),
                   party_names=["Acme"])
    assert res.rounds[1].dropped_for_party_names >= 1
    leaked = {p["patch_id"] for p in res.stores[1] if "Acme" in p["prevention_step"]}
    injected = {r.split("@")[0] for c in res.cases for r in c.retrieved}
    assert leaked and not (leaked & injected)


def test_an_unparseable_answer_is_scored_as_an_empty_graph(corpus):
    train, test, teachers = corpus

    def flaky(case, notes, t):
        return None if case.case_id == "X1" else deaf_student(case, notes, t)

    res = run_loop(train, test, teachers, flaky, LoopConfig(k=1, max_rounds=0))
    row = next(r for r in res.cases if r.case_id == "X1")
    expected, _ = score(teachers["X1"], empty_graph("X1"))
    assert not row.parsed and row.l_ged == expected.l_ged
    assert res.rounds[0].unparsed == 1


def test_plateau_round_ignores_gains_smaller_than_epsilon():
    assert plateau_round([100.0, 90.0, 89.5, 89.4], epsilon=1.0) == 1
    assert plateau_round([100.0, 100.2, 99.9], epsilon=1.0) == 0
    assert plateau_round([100.0, 95.0, 97.0, 80.0], epsilon=1.0) == 3


# ── retrieval hygiene ────────────────────────────────────────

def _one_patch_store(jurisdiction: str, keywords: list[str]) -> PatchStore:
    store = PatchStore()
    store.add(Patch(patch_id="p", patch_family="missing_rule", controlling_authority="§551.301(a)",
                    prevention_step="x", trigger_keywords=keywords, jurisdiction=jurisdiction,
                    verification="verified"))
    return store


def test_a_patch_from_another_jurisdiction_is_not_injected():
    case = _case("T1", "training")                         # an NYC-only case
    texas = _one_patch_store("texas", ["nyc", "audit"])    # keywords match, law does not
    assert loop._retrieve(texas, case, LoopConfig()) == []
    assert len(loop._retrieve(texas, case, LoopConfig(jurisdiction_gate=False))) == 1
    nyc = _one_patch_store("nyc", ["nyc", "audit"])
    assert len(loop._retrieve(nyc, case, LoopConfig())) == 1


def test_a_patch_is_not_retrieved_on_a_function_word_alone():
    """ "private right of action" must not match a case just because it says "of"."""
    case = _case("T1", "training")
    assert " of " not in case.facts
    case.facts += " The employer disclosed none of this."
    store = _one_patch_store("nyc", ["private right of action"])
    assert loop._retrieve(store, case, LoopConfig()) == []
    plain = store.retrieve(f"{case.facts}\n{case.question}", k=3)   # no stop-word list
    assert len(plain) == 1                                   # the old behaviour, for contrast
