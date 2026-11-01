"""Iterative patch loop: at which round does the weak student stop learning?

Round 0 is the unpatched baseline. Each later round injects the top-k patches,
scores every case against the teacher, then updates the patch store from what
the *patched* student still gets wrong on the training cases (re-mine, rewrite
failing patches, reprioritise). Test cases are scored every round but never
feed the store. See src/lex_drl/loop.py for the round structure.

    poetry run python scripts/run_patch_loop.py                       # full loop
    poetry run python scripts/run_patch_loop.py --no-rewrite          # no Claude rewrites
    poetry run python scripts/run_patch_loop.py --rounds 1 --cases E1 E2   # smoke test

The student is Llama-3.2-3B run locally with greedy decoding, so a re-run
reproduces the same graphs and finished rounds are served from the cache.

Outputs:
    data/outputs/loop/{run}/round_{t}/   student graphs and raw answers
    results/loop/{run}/                  rounds.csv, summary.csv, store_round_{t}.json,
                                         retrieval_log.json, curve.html, LOOP_RESULTS.md
    results/loop/teacher_contamination.csv
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

# The scorer reads these at import time, and its code default (tfidf) is the
# backend that ranks the models backwards. Set them before importing lex_drl.
REQUIRED_ENV = {
    "LEX_DRL_SIMILARITY": "embedding",
    "LEX_DRL_RULE_ALIGN": "combined",
    "SMALL_MODEL_BACKEND": "local",
}
for _k, _v in REQUIRED_ENV.items():
    os.environ.setdefault(_k, _v)
os.environ.setdefault("SMALL_MODEL_LOCAL_REPO", "unsloth/Llama-3.2-3B-Instruct")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

# Loaded up front so a long run cannot lose its chart to a missing package at the end.
import plotly.graph_objects as go  # noqa: E402

import lex_drl.alignment as alignment_module  # noqa: E402
from lex_drl.cases import load_all_cases  # noqa: E402
from lex_drl.clients import get_agent_client  # noqa: E402
from lex_drl.discrepancy import DiscrepancyReport  # noqa: E402
from lex_drl.extraction import _parse_response  # noqa: E402
from lex_drl.injection import build_patched_system, training_party_names  # noqa: E402
from lex_drl.loop import LoopConfig, LoopResult, plateau_round, run_loop  # noqa: E402
from lex_drl.schema import GraphSource, LegalReasoningGraph  # noqa: E402
from lex_drl.statute_index import load_statute_index  # noqa: E402

STUDENT = "llama3_2b"
GRAPHS = Path("data/outputs/graphs")
SNAPSHOT = Path("data/snapshots/embedding_combined_v1/discrepancies")
ORIGINAL_SIX = ["E1", "E2", "M1", "M2", "H1", "H2"]


def _check_env() -> None:
    for k, v in REQUIRED_ENV.items():
        if os.environ.get(k, "").lower() != v:
            raise SystemExit(f"{k} must be '{v}' for this experiment (got {os.environ.get(k)!r})")
    if alignment_module.SIMILARITY_METHOD != "embedding" or alignment_module.RULE_ALIGN_MODE != "combined":
        raise SystemExit("scorer is not embedding + combined; refusing to run")


def _write_contamination(teachers: dict[str, LegalReasoningGraph], index, out: Path) -> int:
    """Per case: teacher rules whose citation the statute index classifies as fabricated."""
    rows, total = [], 0
    for cid, g in teachers.items():
        fab = [r.citation for r in g.rules
               if index is not None and index.classify_citation(r.citation) == "fabricated"]
        total += len(fab)
        rows.append({"case": cid, "teacher_rules": len(g.rules),
                     "fabricated_citations": len(fab), "which": "; ".join(fab)})
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    return total


def _make_student(run_dir: Path, n_cases: int):
    client = get_agent_client(STUDENT)
    timings: list[float] = []
    state = {"done": 0}

    def student(case, notes: str, t: int):
        rdir = run_dir / f"round_{t}"
        rdir.mkdir(parents=True, exist_ok=True)
        system = build_patched_system(case, notes)
        t0 = time.time()
        # Same call shape as the Phase 2-4 baselines, so round 0 of the original
        # six cases is served from the same cache entries.
        resp = client.generate(system=system, user="Begin your analysis now.")
        dt = time.time() - t0
        if dt > 2.0:                     # a real generation, not a cache hit
            timings.append(dt)
        state["done"] += 1
        (rdir / f"{case.case_id}_raw.txt").write_text(resp.text, encoding="utf-8")
        try:
            graph = _parse_response(resp.text, case_id=case.case_id, source=GraphSource.AGENT,
                                    model=resp.model, agent_id=STUDENT)
        except Exception as e:
            print(f"    [unparsed] round {t} {case.case_id}: {str(e)[:90]}")
            return None
        (rdir / f"{case.case_id}_agent_{STUDENT}.json").write_text(
            graph.model_dump_json(indent=2), encoding="utf-8")
        avg = sum(timings) / len(timings) if timings else 0.0
        print(f"    round {t} {case.case_id:>4}  {dt:6.1f}s"
              + (f"  (avg {avg:.0f}s/case, ~{avg * n_cases / 60:.0f} min per uncached round)"
                 if timings else "  (cached)"), flush=True)
        return graph

    return student


def _guard_round_zero(rows, no_guard: bool) -> None:
    """Round 0 of the original six must reproduce the pinned Phase-4 baselines."""
    drift = []
    for r in rows:
        snap = SNAPSHOT / f"{r.case_id}_{STUDENT}.json"
        if r.case_id in ORIGINAL_SIX and snap.exists():
            pinned = DiscrepancyReport.model_validate_json(snap.read_text()).l_ged
            if abs(pinned - r.l_ged) > 1e-6:
                drift.append(f"{r.case_id}: loop {r.l_ged} vs pinned {pinned}")
    if drift:
        msg = "round-0 baseline differs from embedding_combined_v1: " + "; ".join(drift)
        if no_guard:
            print(f"  [warning] {msg}")
        else:
            raise SystemExit(msg + "\n(re-run with --no-guard to continue anyway)")
    else:
        print("  round-0 baselines match the pinned Phase-4 values for the original six.")


def _write_outputs(res: LoopResult, out: Path, run: str, contaminated: int,
                   n_train: int, n_test: int) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with (out / "rounds.csv").open("w", newline="") as f:
        cols = [k for k in asdict(res.cases[0]) if k != "retrieved"] + ["retrieved"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for c in res.cases:
            d = asdict(c); d["retrieved"] = " ".join(c.retrieved)
            w.writerow(d)
    with (out / "summary.csv").open("w", newline="") as f:
        cols = [k for k in asdict(res.rounds[0]) if k != "by_tier"]
        tiers = sorted({k for r in res.rounds for k in r.by_tier})
        w = csv.DictWriter(f, fieldnames=cols + tiers)
        w.writeheader()
        for r in res.rounds:
            d = asdict(r); bt = d.pop("by_tier")
            w.writerow(d | {t: bt.get(t, "") for t in tiers})
    (out / "retrieval_log.json").write_text(json.dumps(
        [{"round": c.round, "case": c.case_id, "split": c.split, "retrieved": c.retrieved}
         for c in res.cases if c.round > 0], indent=2))

    r0 = res.rounds[0]
    train_best = plateau_round([r.mean_lged_train for r in res.rounds], res.epsilon)
    reason = {"plateau": "neither the test nor the training curve was still improving",
              "fixpoint": "the prompts stopped changing (store reached a fixed point)",
              "max_rounds": "the round limit was reached"}[res.stop_reason]
    L = [f"# Iterative patch loop — run `{run}`", "",
         f"Student: Llama-3.2-3B (local, greedy). {n_train} training cases, {n_test} held-out "
         f"test cases. k = {res.config['k']} patches per prompt. "
         f"Rewrites: {'on' if res.config['rewrite'] else 'off'}.", "",
         "L-GED is distance from the teacher's graph: lower is better.", "",
         "## Result", "",
         f"- **Held-out (test) cases stop improving at round {res.best_round}.** "
         f"Mean test L-GED: {r0.mean_lged_test} at round 0 → "
         f"{res.rounds[res.best_round].mean_lged_test} at round {res.best_round} "
         f"({res.rounds[res.best_round].mean_lged_test - r0.mean_lged_test:+.2f}).",
         f"- Training cases are best at round {train_best}: {r0.mean_lged_train} → "
         f"{res.rounds[train_best].mean_lged_train} "
         f"({res.rounds[train_best].mean_lged_train - r0.mean_lged_train:+.2f}).",
         f"- The loop ran {len(res.rounds) - 1} patched round(s) and stopped because {reason}.",
         f"- A gain counts only if it exceeds {res.epsilon} L-GED points "
         f"(1% of the round-0 test mean).",
         "- Patches are mined only from this student's own gaps on the training cases, "
         "so the store differs from the Phase 2–4 store (which also used GPT-5's gaps).",
         "- Retrieval: BM25 over patch keywords with function words removed from the case "
         "text, one patch per legal duty, and only patches from the case's own "
         "jurisdictions. Round 1 uses no loop evidence, so it is the single-pass method.", "",
         "## Per round", "",
         "| Round | Store | New | Rewritten | Train L-GED | Test L-GED | Test Δ vs r0 "
         "| Train R+O recovered | Test R+O recovered | Unparsed |",
         "|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in res.rounds:
        L.append(f"| {r.round} | {r.store_size} | {r.new_patches} | {r.rewritten} "
                 f"| {r.mean_lged_train} | {r.mean_lged_test} "
                 f"| {r.mean_lged_test - r0.mean_lged_test:+.2f} "
                 f"| {r.ro_recovery_train:.1%} | {r.ro_recovery_test:.1%} | {r.unparsed} |")
    tiers = sorted({k for r in res.rounds for k in r.by_tier if k.startswith("test/")})
    if tiers:
        L += ["", "## Test L-GED by tier", "",
              "| Round | " + " | ".join(t.split("/")[1] for t in tiers) + " |",
              "|--:|" + "--:|" * len(tiers)]
        for r in res.rounds:
            L.append(f"| {r.round} | " + " | ".join(str(r.by_tier.get(t, "")) for t in tiers) + " |")
    L += ["", "Columns: *Store* = patches available that round; *New* = patches mined from "
          "that round's training graphs; *Rewritten* = failing patches rewritten after that "
          "round; *R+O recovered* = share of the teacher's Rules and Obligations present in "
          "the student's graph.", "",
          "## Caveats", "",
          f"- Teacher graphs were extracted from statute summaries known to contain errors; "
          f"{contaminated} teacher rule citation(s) across these cases are classified as "
          f"fabricated (see `results/loop/teacher_contamination.csv`).",
          "- 24 of the 30 cases are synthetic and have not been reviewed by a legal expert.",
          "- One student and a fixed budget of k patches: the plateau round is specific "
          "to this model and this k.", ""]
    (out / "LOOP_RESULTS.md").write_text("\n".join(L), encoding="utf-8")

    try:
        xs = [r.round for r in res.rounds]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=[r.mean_lged_test for r in res.rounds],
                                 mode="lines+markers", name="test (held out)"))
        fig.add_trace(go.Scatter(x=xs, y=[r.mean_lged_train for r in res.rounds],
                                 mode="lines+markers", name="training"))
        for t in tiers:
            fig.add_trace(go.Scatter(x=xs, y=[r.by_tier.get(t) for r in res.rounds],
                                     mode="lines", line={"dash": "dot"}, name=t))
        fig.add_vline(x=res.best_round, line_dash="dash",
                      annotation_text=f"test stops improving (round {res.best_round})")
        fig.update_layout(title=f"Patch loop '{run}': mean L-GED per round (lower is better)",
                          xaxis_title="round (0 = no patches)", yaxis_title="mean L-GED",
                          xaxis={"dtick": 1})
        fig.write_html(out / "curve.html", include_plotlyjs="cdn")
    except Exception as e:  # the chart is a convenience; never fail the run on it
        print(f"  [warning] could not write curve.html: {e}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", default=None, help="run name (default: full | no_rewrite)")
    ap.add_argument("--k", type=int, default=3, help="patches per prompt")
    ap.add_argument("--rounds", type=int, default=8, help="maximum patched rounds")
    ap.add_argument("--no-rewrite", action="store_true",
                    help="re-mine and reprioritise only; no Claude rewrites")
    ap.add_argument("--cases", nargs="+", default=None, help="restrict to these case ids")
    ap.add_argument("--allowed", default="verified,unverified",
                    help="patch verification statuses eligible for injection")
    ap.add_argument("--patience", type=int, default=2)
    ap.add_argument("--no-guard", action="store_true",
                    help="continue even if round 0 differs from the pinned baselines")
    args = ap.parse_args()
    _check_env()

    run = args.run or ("no_rewrite" if args.no_rewrite else "full")
    cases = load_all_cases()
    if args.cases:
        cases = [c for c in cases if c.case_id in set(args.cases)]
    missing = [c.case_id for c in cases if not (GRAPHS / f"{c.case_id}_reference.json").exists()]
    if missing:
        raise SystemExit(f"no teacher graph for: {missing} — run scripts/run_extraction.py "
                         f"--teacher --skip-existing first")
    teachers = {c.case_id: LegalReasoningGraph.model_validate_json(
        (GRAPHS / f"{c.case_id}_reference.json").read_text()) for c in cases}
    train = [c for c in cases if c.role == "training"]
    test = [c for c in cases if c.role == "test"]

    index = load_statute_index()
    out = Path("results/loop") / run
    contaminated = _write_contamination(teachers, index, Path("results/loop/teacher_contamination.csv"))

    cfg = LoopConfig(k=args.k, max_rounds=args.rounds, rewrite=not args.no_rewrite,
                     allowed=frozenset(s.strip() for s in args.allowed.split(",") if s.strip()),
                     patience=args.patience)
    writer = None
    if cfg.rewrite:
        from lex_drl.patch_generator import InsightWriter
        writer = InsightWriter()

    print(f"Patch loop '{run}': {len(train)} training + {len(test)} test cases, k={cfg.k}, "
          f"up to {cfg.max_rounds} rounds, rewrites {'on' if cfg.rewrite else 'off'}, "
          f"allowed={sorted(cfg.allowed)}")
    print(f"  scorer: {alignment_module.SIMILARITY_METHOD} + {alignment_module.RULE_ALIGN_MODE}; "
          f"fabricated teacher citations in these cases: {contaminated}")

    def on_round(summary, rows, store_used):
        out.mkdir(parents=True, exist_ok=True)
        (out / f"store_round_{summary.round}.json").write_text(
            json.dumps(store_used, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  ── round {summary.round}: train {summary.mean_lged_train}  "
              f"test {summary.mean_lged_test}  store {summary.store_size}  "
              f"new {summary.new_patches}  rewritten {summary.rewritten}  "
              f"unparsed {summary.unparsed}", flush=True)
        if summary.round == 0:
            _guard_round_zero(rows, args.no_guard)

    res = run_loop(train, test, teachers,
                   _make_student(Path("data/outputs/loop") / run, len(cases)), cfg,
                   index=index, writer=writer, party_names=training_party_names(),
                   on_round=on_round)
    _write_outputs(res, out, run, contaminated, len(train), len(test))
    print(f"\nStopped: {res.stop_reason}. Test cases stop improving at round {res.best_round}.")
    print(f"Results → {out}/LOOP_RESULTS.md")


if __name__ == "__main__":
    main()
