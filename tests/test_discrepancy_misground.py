"""Tests for the v_misground detector in discrepancy.compute_discrepancies."""
from __future__ import annotations

from lex_drl.alignment import AlignmentReport
from lex_drl.discrepancy import compute_discrepancies
from lex_drl.schema import GraphSource, LegalReasoningGraph, Rule


def _graph(source: GraphSource, rules: list[Rule], agent_id=None) -> LegalReasoningGraph:
    return LegalReasoningGraph(
        case_id="E1", source=source, model_name="test", agent_id=agent_id, rules=rules,
    )


def _rule(rid: str, citation: str, label: str) -> Rule:
    return Rule(rid=rid, citation=citation, label=label, jurisdiction="NYC")


def _align(rule_map: dict) -> AlignmentReport:
    return AlignmentReport(case_id="E1", rule_map=rule_map)


def test_text_aligned_conflicting_citation_is_misgrounding():
    # Teacher AEDT-definition §20-870 aligned (by text) to student citing §20-871.
    teacher = _graph(GraphSource.REFERENCE, [_rule("R1", "§20-870", "AEDT definition")])
    student = _graph(GraphSource.AGENT, [_rule("R1", "§20-871", "AEDT definition")], agent_id="gpt5")
    report = compute_discrepancies(teacher, student, _align({"R1": "R1"}))
    assert report.v_misground_count == 1
    mg = report.v_misground[0]
    assert mg.teacher_citation == "§20-870" and mg.student_citation == "§20-871"
    assert mg.student_section_exists is None  # no index supplied


def test_citation_aligned_pair_is_not_misgrounding():
    teacher = _graph(GraphSource.REFERENCE, [_rule("R1", "§20-870", "AEDT definition")])
    student = _graph(GraphSource.AGENT, [_rule("R1", "NYC §20-870", "AEDT def")], agent_id="gpt5")
    report = compute_discrepancies(teacher, student, _align({"R1": "R1"}))
    assert report.v_misground_count == 0


def test_uncited_student_rule_is_skipped():
    teacher = _graph(GraphSource.REFERENCE, [_rule("R1", "§20-870", "AEDT definition")])
    student = _graph(GraphSource.AGENT, [_rule("R1", "", "AEDT definition")], agent_id="gpt5")
    report = compute_discrepancies(teacher, student, _align({"R1": "R1"}))
    assert report.v_misground_count == 0


def test_section_exists_fn_sets_subtype():
    teacher = _graph(GraphSource.REFERENCE, [_rule("R1", "§20-870", "AEDT definition")])
    student = _graph(GraphSource.AGENT, [_rule("R1", "§20-871", "AEDT definition")], agent_id="gpt5")
    real_sections = {"20-870", "20-871"}  # both real → real-but-wrong
    fn = lambda c: bool({t.strip("§") for t in c.replace("§", " §").split() if t.strip("§")} & real_sections) or "20-871" in c
    report = compute_discrepancies(teacher, student, _align({"R1": "R1"}), section_exists_fn=lambda c: "20-871" in c)
    assert report.v_misground[0].student_section_exists is True
    report2 = compute_discrepancies(teacher, student, _align({"R1": "R1"}), section_exists_fn=lambda c: False)
    assert report2.v_misground[0].student_section_exists is False


def test_misground_not_in_lged_by_default():
    teacher = _graph(GraphSource.REFERENCE, [_rule("R1", "§20-870", "AEDT definition")])
    student = _graph(GraphSource.AGENT, [_rule("R1", "§20-871", "AEDT definition")], agent_id="gpt5")
    base = compute_discrepancies(teacher, student, _align({"R1": "R1"}))
    folded = compute_discrepancies(teacher, student, _align({"R1": "R1"}), include_misground_in_lged=True)
    assert folded.l_ged > base.l_ged  # weight added only when requested


def test_e1_oracle_pairs_flag_as_misgroundings():
    """E1 oracle fixture: each (wrong, correct) pair on the same proposition
    must be flagged. Validates detector logic (not the frozen snapshot)."""
    pairs = [("§20-871", "§20-870"), ("§20-872(a)", "§20-871"),
             ("§20-874", "§20-875"), ("§6-1-1704", "§6-1-1703")]
    t_rules, s_rules, rmap = [], [], {}
    for i, (wrong, correct) in enumerate(pairs, 1):
        rid = f"R{i}"
        t_rules.append(_rule(rid, correct, f"proposition {i}"))
        s_rules.append(_rule(rid, wrong, f"proposition {i}"))
        rmap[rid] = rid
    teacher = _graph(GraphSource.REFERENCE, t_rules)
    student = _graph(GraphSource.AGENT, s_rules, agent_id="gpt5")
    report = compute_discrepancies(teacher, student, _align(rmap))
    assert report.v_misground_count == 4
