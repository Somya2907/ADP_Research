"""Task 5 — variance: repeat two decision cells with cache-salt; report L-GED range.

Two cells: gpt5/M2/k3 (cloud — real temperature-0 provider non-determinism) and
llama3_2b/H2/k3 (local — greedy/deterministic, expected ~0 run-to-run range). Each
repeat salts the cache key via run_tag (does NOT delete cache.db). GPT-5 runs first
so its variance is captured even if the local cell stalls on MPS.

    LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_variance.py [--reps 3]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv

from lex_drl.alignment import align_all
from lex_drl.discrepancy import compute_discrepancies
from lex_drl.clients import get_agent_client
from lex_drl.cases import load_case
from lex_drl.extraction import _parse_response
from lex_drl.patch_store import PatchStore
from lex_drl.schema import GraphSource, LegalReasoningGraph

# reuse the injection prompt builders + leakage guard
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_patch_injection import build_patched_system, filter_leaks, render_notes_block

load_dotenv()

GRAPHS = Path("data/outputs/graphs")
BASELINE_DIR = {"gpt5": GRAPHS, "llama3_2b": Path("data/outputs/graphs_local")}
# (student, case, k) — GPT-5 first (safe/fast); Llama second (local).
CELLS = [("gpt5", "M2", 3), ("llama3_2b", "H2", 3)]


def _load(p: Path) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json(p.read_text())


def _lged(teacher, graph) -> float:
    return compute_discrepancies(teacher, graph, align_all(teacher, graph)).l_ged


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--out", default="results/variance.csv")
    args = ap.parse_args()

    store = filter_leaks(PatchStore.from_file("data/patches/patches.json"))[0]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    def _flush(rows):
        with out.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["cell", "run", "l_ged", "delta"])
            w.writeheader(); w.writerows(rows)

    rows: list[dict] = []
    for student, case_id, k in CELLS:
        case = load_case(case_id)
        teacher = _load(GRAPHS / f"{case_id}_reference.json")
        base = _lged(teacher, _load(BASELINE_DIR[student] / f"{case_id}_agent_{student}.json"))
        patches = store.retrieve(f"{case.facts}\n{case.question}", k=k, allowed={"verified"})
        system = build_patched_system(case, render_notes_block(patches))
        client = get_agent_client(student)
        print(f"\n[{student}/{case_id}/k{k}] baseline={base:.1f}", flush=True)
        for rep in range(1, args.reps + 1):
            try:
                resp = client.generate(system=system, user="Begin your analysis now.",
                                       run_tag=f"var{rep}")
                g = _parse_response(resp.text, case_id=case_id, source=GraphSource.AGENT,
                                    model=resp.model, agent_id=student)
                lged = _lged(teacher, g)
                rows.append({"cell": f"{student}/{case_id}/k{k}", "run": rep,
                             "l_ged": round(lged, 2), "delta": round(lged - base, 2)})
                print(f"  run {rep}: L-GED={lged:.1f} (Δ {lged - base:+.1f})", flush=True)
            except Exception as e:
                print(f"  run {rep} FAILED: {type(e).__name__}: {str(e)[:120]}", flush=True)
        _flush(rows)  # persist after each cell so GPT-5 survives a local stall

    # summary
    print(f"\n → {out}")
    from collections import defaultdict
    by = defaultdict(list)
    for r in rows:
        by[r["cell"]].append(r["l_ged"])
    for cell, vals in by.items():
        print(f"  {cell}: {vals}  range={max(vals) - min(vals):.1f}")


if __name__ == "__main__":
    main()
