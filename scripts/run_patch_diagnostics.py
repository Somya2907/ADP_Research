"""Stage B diagnostics: one prompt variant ("arm") on a small set of test cases.

Every arm is compared with the unpatched round-0 answer of the same case, so
the result is a paired difference. The arms separate the three explanations
for why patches barely help (see src/lex_drl/diagnostics.py):

    placebo        3 real patches that have nothing to do with the case — how much
                   does any extra text move the score? (noise floor)
    oracle_k3      the case's own 3 heaviest missing Rule/Obligation nodes as
                   template patches — if the patch is exactly right, is it used?
    oracle_k10     same, 10 patches — does passing more help?
    oracle_all     same, every missing R/O — the most patches could do
    directive_k10  oracle_k10 content worded as a checklist of required nodes
    llm_k10        oracle_k10 content with the patch text written by Claude
    checklist_k5   C1: 5 checklist items mined from the training cases only, picked
                   by case similarity + how often they were missed (a real method)
    checklist_k10  same, 10 items

Oracle arms read the test case's own teacher graph: they are upper bounds,
never a method result. Checklist arms use the teacher only to score.

Every answer goes through the loop guard and repair (src/lex_drl/repair.py): an
answer that starts repeating itself is cut where the loop begins and resumed at
the next JSON section. ``looped`` marks those answers, ``repairs`` counts the
continuations, ``still_looped`` marks answers given up on after the last one.

    poetry run python scripts/run_patch_diagnostics.py --arm placebo
    poetry run python scripts/run_patch_diagnostics.py --arm oracle_k10 --cases E2
    poetry run python scripts/run_patch_diagnostics.py --all      # every arm in turn
    poetry run python scripts/run_patch_diagnostics.py --arm placebo --cases test \
        --backend remote --base-run data/outputs/loop/checklist_t4/round_0   # on the Colab T4

With ``--backend remote`` outputs get a ``_t4`` suffix and the baseline answers
come from ``--base-run`` (that GPU's own unpatched answers).

Outputs: data/outputs/diagnostics/{arm}/ (notes, raw answers, graphs) and
results/diagnostics/{arm}.csv. Answers are cached, so a re-run is instant.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

for _k, _v in {"LEX_DRL_SIMILARITY": "embedding", "LEX_DRL_RULE_ALIGN": "combined",
               "SMALL_MODEL_BACKEND": "local", "LEX_DRL_LOOP_GUARD": "1"}.items():
    os.environ.setdefault(_k, _v)
os.environ.setdefault("SMALL_MODEL_LOCAL_REPO", "unsloth/Llama-3.2-3B-Instruct")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

import lex_drl.alignment as alignment_module  # noqa: E402
from lex_drl.cases import load_all_cases  # noqa: E402
from lex_drl.checklist import (  # noqa: E402
    cluster, match_gaps, missed_items, rank, render_checklist, test_gaps,
)
from lex_drl.clients import get_agent_client  # noqa: E402
from lex_drl.diagnostics import (  # noqa: E402
    SUBSET, directive_notes, oracle_selection, placebo_patches, taken_up,
)
from lex_drl.extraction import _parse_response  # noqa: E402
from lex_drl.injection import build_patched_system, filter_leaks, render_notes_block, training_party_names  # noqa: E402
from lex_drl.loop import empty_graph, patch_outcome, score  # noqa: E402
from lex_drl.repair import generate_with_repair  # noqa: E402
from lex_drl.patch_store import Patch, PatchStore  # noqa: E402
from lex_drl.schema import GraphSource, LegalReasoningGraph  # noqa: E402
from lex_drl.statute_index import load_statute_index  # noqa: E402

STUDENT = "llama3_2b"
GRAPHS = Path("data/outputs/graphs")
BASE_RUN = Path("data/outputs/loop/full/round_0")       # cached unpatched answers
PLACEBO_STORE = Path("results/loop/full/store_round_1.json")
OUT_DATA = Path("data/outputs/diagnostics")
OUT = Path("results/diagnostics")
ARMS = ["placebo", "oracle_k10", "directive_k10", "oracle_k3", "oracle_all", "llm_k10",
        "checklist_k10", "checklist_k5"]
CHECKLIST = {}          # filled in main(): training clusters + embedding function
NODE_LISTS = ("facts", "issues", "rules", "applications", "conclusions", "obligations")


def _load_graph(path: Path, cid: str) -> LegalReasoningGraph:
    if not path.exists():
        return empty_graph(cid)
    return LegalReasoningGraph.model_validate_json(path.read_text())


def _embed(texts):
    return alignment_module._get_embed_model().encode(texts, normalize_embeddings=True,
                                                      show_progress_bar=False)


def _build_checklist(index) -> list:
    """Clusters of what the unpatched student missed on the training cases."""
    items = []
    for c in load_all_cases():
        if c.role != "training":
            continue
        teacher = LegalReasoningGraph.model_validate_json(
            (GRAPHS / f"{c.case_id}_reference.json").read_text())
        student = _load_graph(BASE_RUN / f"{c.case_id}_agent_{STUDENT}.json", c.case_id)
        report, _ = score(teacher, student)
        items += missed_items(c, report, teacher, index=index, party_names=training_party_names())
    return cluster(items)


def _notes(arm: str, case, teacher, base_report, base_graph, index, placebo_store, writer):
    """(patches, teacher node ids they target, notes text, number of notes) for one arm and case."""
    if arm == "placebo":
        ps = placebo_patches(case, teacher, placebo_store, k=3)
        return ps, [], render_notes_block(ps), len(ps)
    if arm.startswith("checklist"):
        k = int(arm.split("_k")[1])
        given = rank(CHECKLIST["clusters"], case, "combined", embed=_embed)[:k]
        # the teacher is used only to see which items were useful, never to pick them
        filled = match_gaps(given, test_gaps(base_report, teacher, index=index), embed=_embed)
        return [], [g.teacher_id for g in filled], render_checklist(given), len(given)
    k = {"k3": 3, "k10": 10, "all": None}[arm.split("_")[1]]
    sel = oracle_selection(case, base_report, teacher, base_graph, k, index=index,
                           insight=writer if arm.startswith("llm") else None)
    ps, nodes = [p for p, _ in sel], [nid for _, nid in sel]
    if arm.startswith("directive"):
        return ps, nodes, directive_notes(nodes, teacher), len(ps)
    return ps, nodes, render_notes_block(ps), len(ps)


def run_arm(arm: str, cases, teachers, client, index, placebo_store, writer,
            name: str | None = None) -> list[dict]:
    name = name or arm
    odir = OUT_DATA / name
    odir.mkdir(parents=True, exist_ok=True)
    rows = []
    for case in cases:
        teacher = teachers[case.case_id]
        base_graph = _load_graph(BASE_RUN / f"{case.case_id}_agent_{STUDENT}.json", case.case_id)
        base_report, base_al = score(teacher, base_graph)
        patches, nodes, notes, n_notes = _notes(arm, case, teacher, base_report, base_graph, index,
                                placebo_store, writer)
        (odir / f"{case.case_id}_notes.txt").write_text(notes, encoding="utf-8")

        t0 = time.time()
        rep = generate_with_repair(client, system=build_patched_system(case, notes),
                                   user="Begin your analysis now.")
        dt = time.time() - t0
        (odir / f"{case.case_id}_raw.txt").write_text(rep.text, encoding="utf-8")
        looped = rep.looped
        try:
            graph = _parse_response(rep.text, case_id=case.case_id, source=GraphSource.AGENT,
                                    model=client.model, agent_id=STUDENT)
            (odir / f"{case.case_id}_agent_{STUDENT}.json").write_text(
                graph.model_dump_json(indent=2), encoding="utf-8")
            parsed = True
        except Exception as e:
            print(f"    [unparsed] {arm} {case.case_id}: {str(e)[:90]}")
            graph, parsed = empty_graph(case.case_id), False
        report, al = score(teacher, graph)

        def _ro(a):
            return (sum(v is not None for v in a.rule_map.values())
                    + sum(v is not None for v in a.obligation_map.values()))

        # oracle/checklist arms: was each targeted node recovered? placebo: did any patch close a gap?
        if nodes:
            targets = len(nodes)
            closed = sum(al.teacher_to_student(nid) is not None for nid in nodes)
        else:
            targets = closed = 0
            for p in patches:
                n, c = patch_outcome(p, teacher, report, al)
                targets += n
                closed += c
        rows.append({
            "arm": arm, "case": case.case_id, "tier": case.tier, "parsed": parsed,
            "notes": n_notes, "notes_words": len(notes.split()), "looped": looped,
            "repairs": rep.repairs, "still_looped": rep.still_looped, "empty_json": rep.empty_json,
            "base_l_ged": base_report.l_ged, "l_ged": report.l_ged,
            "delta": round(report.l_ged - base_report.l_ged, 2),
            "ro_total": len(teacher.rules) + len(teacher.obligations),
            "base_ro_recovered": _ro(base_al), "ro_recovered": _ro(al),
            "targets": targets, "targets_closed": closed,
            "taken_up": sum(taken_up(p, graph) for p in patches),
            "base_rules": len(base_graph.rules), "rules": len(graph.rules),
            "base_nodes": sum(len(getattr(base_graph, f)) for f in NODE_LISTS),
            "nodes": sum(len(getattr(graph, f)) for f in NODE_LISTS),
            "base_halluc": len(base_report.v_halluc), "halluc": len(report.v_halluc),
            "base_misground": len(base_report.v_misground), "misground": len(report.v_misground),
            "seconds": round(dt, 1),
        })
        r = rows[-1]
        print(f"  {arm:>13} {case.case_id:>4}  L-GED {r['base_l_ged']:6.1f} → {r['l_ged']:6.1f} "
              f"({r['delta']:+6.1f})  rules {r['base_rules']}→{r['rules']}  "
              f"closed {closed}/{targets}  {dt:5.0f}s", flush=True)
        _write(name, rows)              # after every case, so a stopped run keeps its rows
    return rows


def _write(arm: str, rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / f"{arm}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--arm", choices=ARMS)
    ap.add_argument("--all", action="store_true", help="run every arm in turn")
    ap.add_argument("--cases", nargs="+", default=SUBSET,
                    help="test case ids, or 'test' for all of them")
    ap.add_argument("--backend", choices=["local", "remote"], default="local")
    ap.add_argument("--base-run", default=None,
                    help="folder of unpatched answers to compare against (default: the local round 0)")
    ap.add_argument("--name", default=None,
                    help="output name (default: the arm), e.g. checklist_k10_all15")
    args = ap.parse_args()
    if not args.arm and not args.all:
        ap.error("give --arm or --all")
    global BASE_RUN
    os.environ["SMALL_MODEL_BACKEND"] = args.backend
    if args.base_run:
        BASE_RUN = Path(args.base_run)
    elif args.backend == "remote":
        ap.error("--backend remote needs --base-run (that GPU's own unpatched answers)")
    suffix = "_t4" if args.backend == "remote" else ""
    if alignment_module.SIMILARITY_METHOD != "embedding" or alignment_module.RULE_ALIGN_MODE != "combined":
        raise SystemExit("scorer must be embedding + combined")

    by_id = {c.case_id: c for c in load_all_cases()}
    cases = ([c for c in by_id.values() if c.role == "test"] if args.cases == ["test"]
             else [by_id[c] for c in args.cases])
    if any(c.role != "test" for c in cases):
        raise SystemExit("diagnostic arms run on test cases only")
    teachers = {c.case_id: LegalReasoningGraph.model_validate_json(
        (GRAPHS / f"{c.case_id}_reference.json").read_text()) for c in cases}
    index = load_statute_index()
    store = PatchStore()
    for p in json.loads(PLACEBO_STORE.read_text()):
        store.add(Patch.model_validate(p))
    placebo_store, _ = filter_leaks(store, training_party_names())

    arms = ARMS if args.all else [args.arm]
    if any(a.startswith("checklist") for a in arms):
        CHECKLIST["clusters"] = _build_checklist(index)
    writer = None
    if any(a.startswith("llm") for a in arms):
        from lex_drl.patch_generator import InsightWriter
        writer = InsightWriter()
    client = get_agent_client(STUDENT)
    for arm in arms:
        print(f"── {arm} on {', '.join(c.case_id for c in cases)}", flush=True)
        name = (args.name if not args.all and args.name else arm) + suffix
        run_arm(arm, cases, teachers, client, index, placebo_store.all(), writer, name=name)
    print(f"\n→ {OUT}/  (summarise with scripts/diagnostics_report.py)")


if __name__ == "__main__":
    main()
