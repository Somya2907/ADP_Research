"""Task 4 — delta audit: which nodes moved between baseline and patched, and why.

For each (case, student, k, variant) cell, recompute the baseline and patched
DiscrepancyReports and report:
  * teacher Rules newly matched ("recovered": in baseline v_miss, not in patched)
    with citation + classify_citation verdict;
  * L-GED component deltas (v_miss / v_halluc / e_diff weight) — which node type
    drives the change;
  * patched misgroundings (teacher→student citation) with verdicts;
  * a HEURISTIC patch→node attribution (keyword overlap; labelled heuristic).

    LEX_DRL_SIMILARITY=embedding poetry run python scripts/audit_delta.py \\
        --cells llama3_2b/H2/3 gpt5/M2/1 gpt5/M2/3 gpt5/M2/5 --variant clean
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from lex_drl.alignment import align_all
from lex_drl.discrepancy import compute_discrepancies
from lex_drl.schema import LegalReasoningGraph
from lex_drl.statute_index import load_statute_index

GRAPHS = Path("data/outputs/graphs")
BASELINE_DIR = {"gpt5": GRAPHS, "llama3_2b": Path("data/outputs/graphs_local")}
RETRIEVAL_LOG = Path("results/retrieval_log.json")
IDX = load_statute_index()
_WORD = re.compile(r"[a-z0-9]+")


def _load(p: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(p.read_text())


def _report(teacher, graph):
    return compute_discrepancies(teacher, graph, align_all(teacher, graph))


def _weight_by_type(items, get_type):
    out: dict[str, float] = {}
    for it in items:
        out[get_type(it)] = out.get(get_type(it), 0.0) + it.weight
    return out


def _patched_path(case, student, variant, k):
    suffix = f"_patched_k{k}" if variant == "dirty" else f"_patched_{variant}_k{k}"
    return GRAPHS / f"{case}_agent_{student}{suffix}.json"


def _retrieved_for(case, student, k, variant):
    if not RETRIEVAL_LOG.exists():
        return []
    for e in json.loads(RETRIEVAL_LOG.read_text()):
        if (e["case"], e["student"], e["k"], e["variant"]) == (case, student, k, variant):
            return e["retrieved"]
    return []


def audit_cell(case: str, student: str, k: int, variant: str) -> list[str]:
    teacher = _load(GRAPHS / f"{case}_reference.json")
    base_g = _load(BASELINE_DIR[student] / f"{case}_agent_{student}.json")
    pp = _patched_path(case, student, variant, k)
    if not pp.exists():
        return [f"### {student}/{case}/k{k} ({variant})", "", "_patched graph missing._", ""]
    patched_g = _load(pp)
    b, p = _report(teacher, base_g), _report(teacher, patched_g)
    rule_cite = {r.rid: r.citation for r in teacher.rules}

    b_missed = {mn.teacher_id for mn in b.v_miss if mn.teacher_id.startswith("R")}
    p_missed = {mn.teacher_id for mn in p.v_miss if mn.teacher_id.startswith("R")}
    recovered = sorted(b_missed - p_missed)
    newly_missed = sorted(p_missed - b_missed)

    retrieved = _retrieved_for(case, student, k, variant)
    kw_by_patch = {}
    if retrieved:
        pj = {x["patch_id"]: x for x in retrieved}
        allp = {x["patch_id"] for x in retrieved}
        # keyword sets from patches.json for attribution
        store = {x["patch_id"]: x for x in json.loads(Path("data/patches/patches.json").read_text())}
        for pid in allp:
            kw_by_patch[pid] = set(store.get(pid, {}).get("trigger_keywords", []))

    L = [f"### {student}/{case}/k{k} ({variant})", ""]
    L.append(f"- baseline L-GED **{b.l_ged:.1f}** → patched **{p.l_ged:.1f}** "
             f"(Δ **{p.l_ged - b.l_ged:+.1f}**)")
    # component deltas
    bt = _weight_by_type(b.v_miss, lambda x: x.node_type)
    ptt = _weight_by_type(p.v_miss, lambda x: x.node_type)
    dmiss = round(sum(ptt.values()) - sum(bt.values()), 1)
    dhall = round(sum(h.weight for h in p.v_halluc) - sum(h.weight for h in b.v_halluc), 1)
    dedge = round(sum(e.weight for e in p.e_diff) - sum(e.weight for e in b.e_diff), 1)
    comps = {"v_miss": dmiss, "v_halluc": dhall, "e_diff": dedge}
    driver = max(comps, key=lambda c: abs(comps[c]))
    L.append(f"- component Δ (weight): v_miss {dmiss:+.1f}, v_halluc {dhall:+.1f}, "
             f"e_diff {dedge:+.1f} → **driver: {driver}**")
    L.append(f"- counts: v_miss {b.v_miss_count}→{p.v_miss_count}, "
             f"v_halluc {b.v_halluc_count}→{p.v_halluc_count}, "
             f"e_diff {b.e_diff_count}→{p.e_diff_count}, "
             f"v_misground {b.v_misground_count}→{p.v_misground_count}")
    L.append("")

    if recovered:
        L.append(f"**Recovered teacher rules ({len(recovered)})** "
                 f"(in baseline v_miss, matched after patching):")
        for rid in recovered:
            cite = rule_cite.get(rid, "?")
            verdict = IDX.classify_citation(cite) if IDX else "?"
            # heuristic attribution
            rtoks = set(_WORD.findall((cite + " ").lower()))
            attr = [pid for pid, kws in kw_by_patch.items()
                    if rtoks & {t for kw in kws for t in _WORD.findall(kw.lower())}]
            L.append(f"- **{rid}** `{cite}` → *{verdict}*"
                     + (f"  [heuristic: {', '.join(attr)}]" if attr else ""))
        L.append("")
    if newly_missed:
        L.append(f"**Newly missed** (matched in baseline, missed after patching): "
                 f"{', '.join(newly_missed)}")
        L.append("")
    if p.v_misground:
        L.append("**Patched misgroundings** (teacher→student citation, verdict of student cite):")
        for mg in p.v_misground:
            sv = IDX.classify_citation(mg.student_citation) if IDX else "?"
            L.append(f"- {mg.teacher_id}→{mg.student_id}: "
                     f"`{mg.teacher_citation}` vs `{mg.student_citation}` (student *{sv}*)")
        L.append("")
    return L


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", nargs="+", required=True,
                    help="cells as student/case/k, e.g. llama3_2b/H2/3 gpt5/M2/1")
    ap.add_argument("--variant", default="clean")
    ap.add_argument("--out", default="results/DELTA_AUDIT.md")
    args = ap.parse_args()

    lines = ["# Delta audit — what moved and why", "",
             f"Variant: `{args.variant}`. Heuristic attribution is keyword-overlap only "
             "(labelled heuristic; not authoritative).", ""]
    for cell in args.cells:
        student, case, k = cell.split("/")
        lines += audit_cell(case, student, int(k), args.variant)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print(f"wrote {out}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
