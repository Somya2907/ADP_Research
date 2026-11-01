"""Iterative loop with checklist patches: at which round does the student stop improving?

Round 0 is the unpatched baseline (the same answers as the Phase 5 loop). Each
later round gives every case its top-k checklist items, scores all cases, and
updates the item store from the training cases only (re-mine, re-rank by
efficacy, swap the wording of items that keep failing). See
src/lex_drl/checklist_loop.py.

    poetry run python scripts/run_checklist_loop.py                # k=10, up to 5 rounds
    poetry run python scripts/run_checklist_loop.py --rounds 1 --cases E1 E2   # smoke test
    poetry run python scripts/run_checklist_loop.py --backend remote          # on the Colab T4

``--backend remote`` sends generation to notebooks/colab_t4_server.ipynb (set
SMALL_MODEL_REMOTE_URL / SMALL_MODEL_REMOTE_KEY in .env); the run is then named
``checklist_t4`` and its round 0 is that GPU's own baseline.

Llama-3.2-3B, local, greedy, with the loop guard and repair. Answers are cached,
so a stopped run resumes where it left off.

Outputs:
    data/outputs/loop/{run}/round_{t}/   student graphs and raw answers
    results/loop/{run}/                  rounds.csv, summary.csv, store_round_{t}.json,
                                         curve.html, LOOP_RESULTS.md
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

for _k, _v in {"LEX_DRL_SIMILARITY": "embedding", "LEX_DRL_RULE_ALIGN": "combined",
               "SMALL_MODEL_BACKEND": "local", "LEX_DRL_LOOP_GUARD": "1",
               "LEX_DRL_MAX_GEN_SECONDS": "2400"}.items():
    os.environ.setdefault(_k, _v)
os.environ.setdefault("SMALL_MODEL_LOCAL_REPO", "unsloth/Llama-3.2-3B-Instruct")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

import plotly.graph_objects as go  # noqa: E402  (loaded early: a long run must not lose its chart)

import lex_drl.alignment as alignment_module  # noqa: E402
from lex_drl.cases import load_all_cases  # noqa: E402
from lex_drl.checklist_loop import ChecklistLoopConfig, run_checklist_loop  # noqa: E402
from lex_drl.clients import get_agent_client  # noqa: E402
from lex_drl.extraction import _parse_response  # noqa: E402
from lex_drl.injection import build_patched_system, training_party_names  # noqa: E402
from lex_drl.repair import generate_with_repair  # noqa: E402
from lex_drl.schema import GraphSource, LegalReasoningGraph  # noqa: E402
from lex_drl.statute_index import load_statute_index  # noqa: E402

STUDENT = "llama3_2b"
GRAPHS = Path("data/outputs/graphs")
PHASE5_ROUNDS = Path("results/loop/full/rounds.csv")


def _embed(texts):
    return alignment_module._get_embed_model().encode(texts, normalize_embeddings=True,
                                                      show_progress_bar=False)


def _make_student(run_dir: Path, n_cases: int):
    client = get_agent_client(STUDENT)
    timings: list[float] = []

    def student(case, notes: str, t: int):
        rdir = run_dir / f"round_{t}"
        rdir.mkdir(parents=True, exist_ok=True)
        (rdir / f"{case.case_id}_notes.txt").write_text(notes, encoding="utf-8")
        t0 = time.time()
        rep = generate_with_repair(client, system=build_patched_system(case, notes),
                                   user="Begin your analysis now.")
        dt = time.time() - t0
        if dt > 2.0:
            timings.append(dt)
        (rdir / f"{case.case_id}_raw.txt").write_text(rep.text, encoding="utf-8")
        tag = (f"  [loop repaired ×{rep.repairs}]" if rep.looped else "") + \
              ("  [empty JSON resumed]" if rep.empty_json else "")
        try:
            graph = _parse_response(rep.text, case_id=case.case_id, source=GraphSource.AGENT,
                                    model=client.model, agent_id=STUDENT)
        except Exception as e:
            print(f"    [unparsed] round {t} {case.case_id}: {str(e)[:90]}")
            return None
        (rdir / f"{case.case_id}_agent_{STUDENT}.json").write_text(
            graph.model_dump_json(indent=2), encoding="utf-8")
        avg = sum(timings) / len(timings) if timings else 0.0
        print(f"    round {t} {case.case_id:>4}  {dt:6.1f}s{tag}"
              + (f"  (avg {avg:.0f}s/case, ~{avg * n_cases / 60:.0f} min per uncached round)"
                 if timings else "  (cached)"), flush=True)
        return graph

    return student


def _guard_round_zero(rows) -> None:
    """Round 0 must reproduce the Phase 5 baseline exactly (same prompts, same cache)."""
    if not PHASE5_ROUNDS.exists():
        return
    pinned = {r["case_id"]: float(r["l_ged"]) for r in csv.DictReader(PHASE5_ROUNDS.open())
              if r["round"] == "0"}
    drift = [f"{r.case_id}: {r.l_ged} vs {pinned[r.case_id]}" for r in rows
             if r.case_id in pinned and abs(pinned[r.case_id] - r.l_ged) > 1e-6]
    if drift:
        raise SystemExit("round 0 differs from the Phase 5 baseline: " + "; ".join(drift))


def _write_outputs(res, out: Path, run: str, n_train: int, n_test: int) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with (out / "rounds.csv").open("w", newline="") as f:
        rows = [asdict(c) | {"retrieved": ";".join(c.retrieved)} for c in res.cases]
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    with (out / "summary.csv").open("w", newline="") as f:
        rows = [asdict(r) | {"by_tier": json.dumps(r.by_tier)} for r in res.rounds]
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    fig = go.Figure()
    xs = [r.round for r in res.rounds]
    fig.add_trace(go.Scatter(x=xs, y=[r.mean_lged_train for r in res.rounds],
                             mode="lines+markers", name=f"training ({n_train})"))
    fig.add_trace(go.Scatter(x=xs, y=[r.mean_lged_test for r in res.rounds],
                             mode="lines+markers", name=f"test ({n_test})"))
    fig.update_layout(title=f"Checklist loop '{run}': mean L-GED per round (lower is better)",
                      xaxis_title="round (0 = no notes)", yaxis_title="mean L-GED",
                      template="plotly_white")
    fig.write_html(out / "curve.html", include_plotlyjs="cdn")

    r0 = res.rounds[0]
    lines = [f"# Checklist loop — `{run}`", "",
             f"Llama-3.2-3B student, {n_train} training + {n_test} test cases, "
             f"k={res.config['k']} checklist items, up to {res.config['max_rounds']} rounds. "
             f"Stopped: **{res.stop_reason}**. Plateau threshold ε = {res.epsilon} "
             f"(1% of the round-0 test mean).", "",
             "| Round | Items in store | Train L-GED | Test L-GED | Test change vs round 0 | "
             "Train R/O recovered | Test R/O recovered | Items shown to training → useful → written | "
             "New items | Wordings swapped |",
             "|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in res.rounds:
        lines.append(
            f"| {r.round} | {r.clusters} | {r.mean_lged_train:.2f} | {r.mean_lged_test:.2f} | "
            f"{r.mean_lged_test - r0.mean_lged_test:+.2f} | {100 * r.ro_recovery_train:.1f}% | "
            f"{100 * r.ro_recovery_test:.1f}% | "
            + (f"{r.given_train} → {r.useful_train} → {r.resolved_train}" if r.round else "–")
            + f" | {r.new_clusters} | {r.swapped} |")
    tiers = sorted({k for r in res.rounds for k in r.by_tier})
    lines += ["", "## By tier (mean L-GED)", "",
              "| Round | " + " | ".join(tiers) + " |", "|--:|" + "--:|" * len(tiers)]
    for r in res.rounds:
        lines.append(f"| {r.round} | " + " | ".join(f"{r.by_tier.get(t, float('nan')):.1f}"
                                                   for t in tiers) + " |")
    lines += ["", "## When does learning stop?", "",
              f"- Test cases: best at round **{res.best_round}** "
              f"(no later round improved the mean by more than ε).",
              f"- Training cases: best at round **{res.best_round_train}**.",
              f"- Stop reason: {res.stop_reason}."]
    (out / "LOOP_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--backend", choices=["local", "remote"], default="local")
    ap.add_argument("--run", default=None, help="default: checklist (local) / checklist_t4 (remote)")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--patience", type=int, default=2)
    ap.add_argument("--cases", nargs="+", default=None)
    args = ap.parse_args()
    os.environ["SMALL_MODEL_BACKEND"] = args.backend
    args.run = args.run or ("checklist" if args.backend == "local" else "checklist_t4")
    if alignment_module.SIMILARITY_METHOD != "embedding" or alignment_module.RULE_ALIGN_MODE != "combined":
        raise SystemExit("scorer must be embedding + combined")

    cases = load_all_cases()
    if args.cases:
        cases = [c for c in cases if c.case_id in set(args.cases)]
    teachers = {c.case_id: LegalReasoningGraph.model_validate_json(
        (GRAPHS / f"{c.case_id}_reference.json").read_text()) for c in cases}
    train = [c for c in cases if c.role == "training"]
    test = [c for c in cases if c.role == "test"]
    cfg = ChecklistLoopConfig(k=args.k, max_rounds=args.rounds, patience=args.patience)
    out = Path("results/loop") / args.run
    print(f"Checklist loop '{args.run}' ({args.backend}): {len(train)} training + "
          f"{len(test)} test cases, k={cfg.k}, up to {cfg.max_rounds} rounds", flush=True)

    def on_round(summary, rows, store):
        out.mkdir(parents=True, exist_ok=True)
        (out / f"store_round_{summary.round}.json").write_text(
            json.dumps(store, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  ── round {summary.round}: train {summary.mean_lged_train}  "
              f"test {summary.mean_lged_test}  items {summary.clusters}  "
              f"new {summary.new_clusters}  swapped {summary.swapped}  "
              f"shown/useful/written {summary.given_train}/{summary.useful_train}/"
              f"{summary.resolved_train}  unparsed {summary.unparsed}", flush=True)
        if summary.round == 0 and args.backend == "local":
            _guard_round_zero(rows)        # another GPU's baseline is its own

    res = run_checklist_loop(train, test, teachers,
                             _make_student(Path("data/outputs/loop") / args.run, len(cases)),
                             _embed, cfg, index=load_statute_index(),
                             party_names=training_party_names(), on_round=on_round)
    _write_outputs(res, out, args.run, len(train), len(test))
    print(f"\nStopped: {res.stop_reason}. Test best at round {res.best_round}, "
          f"training best at round {res.best_round_train}.")
    print(f"Results → {out}/LOOP_RESULTS.md")


if __name__ == "__main__":
    main()
