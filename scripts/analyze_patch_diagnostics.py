"""Stage A diagnostics: what the Phase 5 outputs already say about the patches.

No model is run. Reads the cached student graphs and patch stores of a loop run
and writes, under results/diagnostics/:

    ceiling.csv              per case: L-GED split by component, and the drop if
                             the student added its 3 / 10 / all heaviest missing
                             Rule/Obligation nodes
    teacher_sensitivity.csv  per case: L-GED with the teacher's fabricated
                             citations removed (teacher error, not student error)
    teacher_suspect_nodes.csv teacher rules to hand to the legal reviewer
    retrieval_audit.csv      per round-1 injection: in jurisdiction? was its target
                             actually missing? did the student cite it? did the gap close?
    citation_collapse.csv    how many store patches are the same section written differently
    STAGE_A.md               the summary

    poetry run python scripts/analyze_patch_diagnostics.py [--run full]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from statistics import mean, median

os.environ.setdefault("LEX_DRL_SIMILARITY", "embedding")
os.environ.setdefault("LEX_DRL_RULE_ALIGN", "combined")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import lex_drl.alignment as alignment_module  # noqa: E402
from lex_drl.cases import load_all_cases  # noqa: E402
from lex_drl.diagnostics import (  # noqa: E402
    canonical_citation, collapse_counts, fabricated_rule_ids, lged_components, missing_targets,
    ro_ceiling, taken_up, teacher_without,
)
from lex_drl.loop import empty_graph, patch_outcome, patch_targets, score  # noqa: E402
from lex_drl.patch_generator import _canon_jurisdiction  # noqa: E402
from lex_drl.patch_store import Patch  # noqa: E402
from lex_drl.schema import LegalReasoningGraph  # noqa: E402
from lex_drl.statute_index import load_statute_index  # noqa: E402

STUDENT = "llama3_2b"
GRAPHS = Path("data/outputs/graphs")
OUT = Path("results/diagnostics")


def _student(run: str, t: int, cid: str) -> LegalReasoningGraph:
    p = Path("data/outputs/loop") / run / f"round_{t}" / f"{cid}_agent_{STUDENT}.json"
    if not p.exists():
        return empty_graph(cid)
    return LegalReasoningGraph.model_validate_json(p.read_text())


def _write(name: str, rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _pct(a: float, b: float) -> str:
    return f"{100 * a / b:.0f}%" if b else "–"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="full")
    args = ap.parse_args()
    if alignment_module.SIMILARITY_METHOD != "embedding" or alignment_module.RULE_ALIGN_MODE != "combined":
        raise SystemExit("scorer must be embedding + combined")

    cases = load_all_cases()
    teachers = {c.case_id: LegalReasoningGraph.model_validate_json(
        (GRAPHS / f"{c.case_id}_reference.json").read_text()) for c in cases}
    index = load_statute_index()
    res = Path("results/loop") / args.run

    # ── 1. ceiling + 2. teacher sensitivity (round 0) ──
    ceil_rows, sens_rows, suspect_rows = [], [], []
    r0 = {}
    for c in cases:
        teacher, student = teachers[c.case_id], _student(args.run, 0, c.case_id)
        report, alignment = score(teacher, student)
        r0[c.case_id] = (report, alignment)
        comp = lged_components(report)
        ceil = ro_ceiling(report)
        ceil_rows.append({
            "case": c.case_id, "split": c.role, "tier": c.tier, "l_ged": report.l_ged,
            **{k: round(v, 2) for k, v in comp.items()},
            "missing_ro": sum(1 for m in report.v_miss if m.node_type in ("R", "O")),
            "teacher_nodes": sum(len(getattr(teacher, f)) for f in
                                 ("facts", "issues", "rules", "applications", "conclusions", "obligations")),
            "student_nodes": sum(len(getattr(student, f)) for f in
                                 ("facts", "issues", "rules", "applications", "conclusions", "obligations")),
            "teacher_rules": len(teacher.rules), "student_rules": len(student.rules),
            "gain_ro_top3": ceil["3"], "gain_ro_top10": ceil["10"], "gain_ro_all": ceil["all"],
        })
        fab = fabricated_rule_ids(teacher, index)
        clean = teacher_without(teacher, fab)
        clean_report, _ = score(clean, student) if fab else (report, None)
        sens_rows.append({
            "case": c.case_id, "split": c.role, "tier": c.tier,
            "fabricated_rules": len(fab),
            "dropped_obligations": len(teacher.obligations) - len(clean.obligations),
            "l_ged": report.l_ged, "l_ged_clean_teacher": clean_report.l_ged,
            "delta": round(clean_report.l_ged - report.l_ged, 2),
        })
        by_id = {r.rid: r for r in teacher.rules}
        for rid in fab:
            suspect_rows.append({"case": c.case_id, "rule": rid, "citation": by_id[rid].citation,
                                 "label": by_id[rid].label})
    _write("ceiling.csv", ceil_rows)
    _write("teacher_sensitivity.csv", sens_rows)
    if suspect_rows:
        _write("teacher_suspect_nodes.csv", suspect_rows)

    # ── 3. retrieval audit (round 1 injections) ──
    log = json.loads((res / "retrieval_log.json").read_text())
    store1 = {p["patch_id"]: Patch.model_validate(p)
              for p in json.loads((res / "store_round_1.json").read_text())}
    by_case = {c.case_id: c for c in cases}
    audit = []
    for entry in log:
        if entry["round"] != 1:
            continue
        c = by_case[entry["case"]]
        teacher = teachers[c.case_id]
        student1 = _student(args.run, 1, c.case_id)
        rep1, al1 = score(teacher, student1)
        _rep0, al0 = r0[c.case_id]
        juris = {_canon_jurisdiction(t) for t in c.jurisdiction_tags}
        teacher_secs = set()
        for r in teacher.rules:
            teacher_secs |= canonical_citation(r.citation, r.jurisdiction)
        for rank, ref in enumerate(entry["retrieved"], 1):
            p = store1[ref.split("@")[0]]
            targets = patch_targets(p, teacher)
            gaps = missing_targets(p, teacher, al0)
            n, closed = patch_outcome(p, teacher, rep1, al1)
            audit.append({
                "case": c.case_id, "split": c.role, "tier": c.tier, "rank": rank,
                "patch": p.patch_id, "family": p.patch_family, "authority": p.controlling_authority,
                "in_jurisdiction": p.jurisdiction in juris,
                "teacher_cites_section": bool(
                    canonical_citation(p.controlling_authority, p.jurisdiction) & teacher_secs),
                "teacher_uses_it": bool(targets), "was_missing": bool(gaps),
                "taken_up": taken_up(p, student1), "closed": closed, "targets": n,
            })
    _write("retrieval_audit.csv", audit)

    # ── 4. citation fragmentation ──
    collapse = []
    for f in sorted(res.glob("store_round_*.json"), key=lambda p: int(p.stem.split("_")[-1])):
        ps = [Patch.model_validate(p) for p in json.loads(f.read_text())]
        if ps:
            collapse.append({"store": f.stem, **collapse_counts(ps)})
    if collapse:
        _write("citation_collapse.csv", collapse)

    # ── summary ──
    lines = [f"# Stage A — what the existing outputs say (run `{args.run}`)", ""]
    for split in ("training", "test"):
        rs = [r for r in ceil_rows if r["split"] == split]
        lg = mean(r["l_ged"] for r in rs)
        ro_miss = mean(r["miss_R"] + r["miss_O"] for r in rs)
        other = mean(r["miss_F"] + r["miss_I"] + r["miss_A"] + r["miss_C"] for r in rs)
        rest = mean(r["halluc"] + r["edges"] for r in rs)
        lines += [
            f"## {split.title()} cases (n={len(rs)}), mean round-0 L-GED {lg:.1f}", "",
            "| Where the L-GED comes from | Mean | Share |", "|---|--:|--:|",
            f"| Missing Rules + Obligations (what patches target) | {ro_miss:.1f} | {_pct(ro_miss, lg)} |",
            f"| Missing Facts, Issues, Applications, Conclusions | {other:.1f} | {_pct(other, lg)} |",
            f"| Hallucinated nodes + edge differences | {rest:.1f} | {_pct(rest, lg)} |", "",
            "| Best case: the student adds its heaviest missing R/O nodes | L-GED drop | Share |",
            "|---|--:|--:|",
        ]
        for key, label in (("gain_ro_top3", "3 nodes (k=3)"), ("gain_ro_top10", "10 nodes"),
                           ("gain_ro_all", "all of them")):
            g = mean(r[key] for r in rs)
            lines.append(f"| {label} | −{g:.1f} | {_pct(g, lg)} |")
        lines += ["", f"Size: teacher {mean(r['teacher_nodes'] for r in rs):.0f} nodes / "
                  f"{mean(r['teacher_rules'] for r in rs):.0f} rules; student "
                  f"{mean(r['student_nodes'] for r in rs):.0f} nodes / "
                  f"{mean(r['student_rules'] for r in rs):.1f} rules; "
                  f"{mean(r['missing_ro'] for r in rs):.0f} missing R/O per case.", ""]

    contaminated = [r for r in sens_rows if r["fabricated_rules"]]
    lines += ["## Teacher errors", "",
              f"{len(contaminated)} of {len(sens_rows)} teacher graphs cite a section the statute "
              f"index marks as fabricated ({sum(r['fabricated_rules'] for r in sens_rows)} rules). "
              "Removing them (and the obligations and edges hanging off them) changes the "
              "round-0 L-GED of those cases by "
              + (f"{mean(r['delta'] for r in contaminated):+.1f} on average "
                 f"(range {min(r['delta'] for r in contaminated):+.1f} to "
                 f"{max(r['delta'] for r in contaminated):+.1f})."
                 if contaminated else "nothing."),
              "The list for the legal reviewer is in `teacher_suspect_nodes.csv`.", ""]

    if audit:
        n = len(audit)
        lines += ["## Retrieval audit (round-1 injections)", "",
                  "| Question | Train | Test |", "|---|--:|--:|"]
        for label, key in (("Patch is in the case's jurisdiction", "in_jurisdiction"),
                           ("Teacher cites the same section somewhere in the case", "teacher_cites_section"),
                           ("Teacher uses this exact authority (what efficacy is scored on)", "teacher_uses_it"),
                           ("…and the student was missing it (useful patch)", "was_missing"),
                           ("Student cites the injected section", "taken_up")):
            cells = []
            for split in ("training", "test"):
                rs = [a for a in audit if a["split"] == split]
                cells.append(f"{sum(1 for a in rs if a[key])}/{len(rs)} ({_pct(sum(1 for a in rs if a[key]), len(rs))})")
            lines.append(f"| {label} | {cells[0]} | {cells[1]} |")
        useful = [a for a in audit if a["was_missing"]]
        lines += [f"| Gap closed, of the useful patches | "
                  + " | ".join(
                      f"{sum(1 for a in useful if a['split'] == s and a['closed'])}"
                      f"/{sum(1 for a in useful if a['split'] == s)}"
                      for s in ("training", "test")) + " |", "",
                  f"{n} injections in total. Precision@k = share that were useful patches.", ""]

    if collapse:
        last = collapse[-1]
        lines += ["## Same section, different spelling", "",
                  f"The final store ({last['store']}) holds {last['patches']} patches. "
                  f"Merging citations that name the same section in a different format leaves "
                  f"{last['distinct_canonical']} ({_pct(last['patches'] - last['distinct_canonical'], last['patches'])} "
                  f"were duplicates); they cover {last['distinct_sections']} distinct sections.", ""]

    (OUT / "STAGE_A.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n→ {OUT}/")


if __name__ == "__main__":
    main()
