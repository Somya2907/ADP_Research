"""Rebuild a checklist-loop run's results from its saved answers.

Used when a run was stopped before it wrote its own summary, and to re-score
every round with the current parser (so a parser fix applies to all rounds
alike). Reads data/outputs/loop/{run}/round_{t}/ and writes
results/loop/{run}/: rounds.csv, summary.csv, LOOP_RESULTS.md, curve.html.

    poetry run python scripts/summarize_checklist_loop.py --run checklist_t4 --rounds 0 1 2 3
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
from pathlib import Path
from statistics import mean

os.environ.setdefault("LEX_DRL_SIMILARITY", "embedding")
os.environ.setdefault("LEX_DRL_RULE_ALIGN", "combined")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import plotly.graph_objects as go  # noqa: E402
from scipy import stats  # noqa: E402

from lex_drl.cases import load_all_cases  # noqa: E402
from lex_drl.extraction import _parse_response  # noqa: E402
from lex_drl.loop import empty_graph, score  # noqa: E402
from lex_drl.schema import GraphSource, LegalReasoningGraph  # noqa: E402

GRAPHS = Path("data/outputs/graphs")
NODE_LISTS = ("facts", "issues", "rules", "applications", "conclusions", "obligations")


def _ci(xs, n=10000, seed=0):
    rng = random.Random(seed)
    ms = sorted(mean(rng.choices(xs, k=len(xs))) for _ in range(n))
    return ms[int(0.025 * n)], ms[int(0.975 * n) - 1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="checklist_t4")
    ap.add_argument("--rounds", nargs="+", type=int, default=[0, 1, 2, 3])
    ap.add_argument("--epsilon-frac", type=float, default=0.01)
    args = ap.parse_args()
    data, out = Path("data/outputs/loop") / args.run, Path("results/loop") / args.run
    cases = load_all_cases()

    rows = []
    for t in args.rounds:
        for c in cases:
            raw = data / f"round_{t}" / f"{c.case_id}_raw.txt"
            if not raw.exists():
                raise SystemExit(f"missing {raw}: round {t} is incomplete")
            teacher = LegalReasoningGraph.model_validate_json(
                (GRAPHS / f"{c.case_id}_reference.json").read_text())
            try:
                g = _parse_response(raw.read_text(), case_id=c.case_id, source=GraphSource.AGENT,
                                    model="student", agent_id="llama3_2b")
                parsed = True
            except Exception:
                g, parsed = empty_graph(c.case_id), False
            rep, al = score(teacher, g)
            rows.append({
                "round": t, "case": c.case_id, "split": c.role, "tier": c.tier, "parsed": parsed,
                "l_ged": rep.l_ged,
                "ro_total": len(teacher.rules) + len(teacher.obligations),
                "ro_recovered": sum(v is not None for v in al.rule_map.values())
                + sum(v is not None for v in al.obligation_map.values()),
                "rules": len(g.rules), "nodes": sum(len(getattr(g, f)) for f in NODE_LISTS),
            })
    out.mkdir(parents=True, exist_ok=True)
    with (out / "rounds.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    def sel(t, split=None, tier=None):
        return [r for r in rows if r["round"] == t and (split is None or r["split"] == split)
                and (tier is None or r["tier"] == tier)]

    def lged(t, split, tier=None):
        return {r["case"]: r["l_ged"] for r in sel(t, split, tier)}

    summary = []
    for t in args.rounds:
        s = {"round": t}
        for split in ("training", "test"):
            rs = sel(t, split)
            s[f"mean_{split}"] = round(mean(r["l_ged"] for r in rs), 2)
            s[f"ro_recovery_{split}"] = round(sum(r["ro_recovered"] for r in rs)
                                             / sum(r["ro_total"] for r in rs), 4)
            s[f"unparsed_{split}"] = sum(1 for r in rs if not r["parsed"])
            s[f"rules_{split}"] = round(mean(r["rules"] for r in rs), 1)
        for tier in ("easy", "medium", "hard"):
            s[f"test_{tier}"] = round(mean(r["l_ged"] for r in sel(t, "test", tier)), 2)
        summary.append(s)
    with (out / "summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]))
        w.writeheader(); w.writerows(summary)

    # paired comparisons on the test cases
    base, first = lged(args.rounds[0], "test"), lged(1, "test") if 1 in args.rounds else None
    comp = []
    for t in args.rounds[1:]:
        cur = lged(t, "test")
        d0 = [cur[c] - base[c] for c in base]
        lo, hi = _ci(d0)
        entry = {"round": t, "vs_base": mean(d0), "ci": (lo, hi),
                 "improved": sum(x < 0 for x in d0), "n": len(d0),
                 "p_t": stats.ttest_1samp(d0, 0).pvalue, "p_w": stats.wilcoxon(d0).pvalue}
        if first is not None and t != 1:
            d1 = [cur[c] - first[c] for c in first]
            entry |= {"vs_r1": mean(d1), "p_r1": stats.wilcoxon(d1).pvalue if any(d1) else 1.0}
        comp.append(entry)

    eps = args.epsilon_frac * summary[0]["mean_test"]
    best = min(summary, key=lambda s: s["mean_test"])
    lines = [f"# Checklist loop — `{args.run}` (rounds {args.rounds[0]}–{args.rounds[-1]})", "",
             "Llama-3.2-3B student, 15 training + 15 test cases, k=10 checklist items per prompt. "
             "Each round after the first re-ranks items by how often they were written on the "
             "training cases, adds newly missed items and swaps the wording of items that keep "
             "failing. Test cases are scored only. Scores re-computed from the saved answers "
             "with the current parser.", "",
             "| Round | Train L-GED | Test L-GED | Test change vs round 0 (95% CI) | Test cases improved | "
             "Wilcoxon p | Test R/O recovered | Rules per answer (test) | Unparsed (train/test) |",
             "|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for s in summary:
        c = next((x for x in comp if x["round"] == s["round"]), None)
        lines.append(
            f"| {s['round']} | {s['mean_training']:.2f} | {s['mean_test']:.2f} | "
            + (f"{c['vs_base']:+.1f} ({c['ci'][0]:+.1f} to {c['ci'][1]:+.1f}) | "
               f"{c['improved']}/{c['n']} | {c['p_w']:.4f}" if c else "— | — | —")
            + f" | {100 * s['ro_recovery_test']:.1f}% | {s['rules_test']} | "
              f"{s['unparsed_training']}/{s['unparsed_test']} |")
    lines += ["", "## By tier (test mean L-GED)", "", "| Round | Easy | Medium | Hard |", "|--:|--:|--:|--:|"]
    for s in summary:
        lines.append(f"| {s['round']} | {s['test_easy']:.1f} | {s['test_medium']:.1f} | {s['test_hard']:.1f} |")
    later = [x for x in comp if "vs_r1" in x]
    lines += ["", "## When does learning stop?", "",
              f"- Best test round: **{best['round']}** (mean {best['mean_test']:.2f}; ε = {eps:.2f}, "
              "1% of the round-0 mean)."]
    for x in later:
        lines.append(f"- Round {x['round']} vs round 1 on the test cases: {x['vs_r1']:+.1f} "
                     f"(Wilcoxon p = {x['p_r1']:.3f}).")
    tr = [s["mean_training"] for s in summary]
    lines.append(f"- Training cases: {' → '.join(f'{v:.1f}' for v in tr)}.")
    (out / "LOOP_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    fig = go.Figure()
    xs = [s["round"] for s in summary]
    fig.add_trace(go.Scatter(x=xs, y=[s["mean_training"] for s in summary], mode="lines+markers",
                             name="training (15)"))
    fig.add_trace(go.Scatter(x=xs, y=[s["mean_test"] for s in summary], mode="lines+markers",
                             name="test (15)"))
    fig.update_layout(title=f"Checklist loop: mean L-GED per round (lower is better)",
                      xaxis_title="round (0 = no notes)", yaxis_title="mean L-GED",
                      template="plotly_white")
    fig.write_html(out / "curve.html", include_plotlyjs="cdn")
    print(f"\n→ {out}/LOOP_RESULTS.md")


if __name__ == "__main__":
    main()
