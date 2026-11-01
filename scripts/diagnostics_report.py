"""Summarise the diagnostic arms into results/diagnostics/REPORT.md + dose.html.

Every number is a paired difference against the same case's unpatched answer
(negative = closer to the teacher). The placebo arm is the noise floor: an arm
only counts as an effect if it beats placebo. Every answer has been through the
loop guard, so an answer that started repeating itself is scored on what it
wrote before the loop.

    poetry run python scripts/diagnostics_report.py
"""
from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean

OUT = Path("results/diagnostics")
PHASE5_ROUNDS = Path("results/loop/full/rounds.csv")
ARMS = [  # (arm, label, kind)
    ("placebo", "Placebo: 3 irrelevant real patches", "control"),
    ("phase5_k3", "Phase 5 method: BM25 patches, k=3 (loop round 1)", "method"),
    ("checklist_k5", "**Checklist from training cases, k=5**", "method"),
    ("checklist_k10", "**Checklist from training cases, k=10**", "method"),
    ("oracle_k3", "Oracle, k=3, advice wording", "upper bound"),
    ("oracle_k10", "Oracle, k=10, advice wording", "upper bound"),
    ("oracle_all", "Oracle, all missing R/O, advice wording", "upper bound"),
    ("directive_k10", "Oracle, k=10, checklist wording", "upper bound"),
    ("llm_k10", "Oracle, k=10, text written by Claude", "upper bound"),
]


def _load(arm: str) -> list[dict]:
    p = OUT / f"{arm}.csv"
    if not p.exists():
        return []
    rows = list(csv.DictReader(p.open()))
    for r in rows:
        for k, v in r.items():
            if k == "looped":
                r[k] = v == "True"
            elif k not in ("arm", "case", "tier", "parsed"):
                r[k] = float(v)
    return rows


def _phase5(cases: set[str]) -> list[dict]:
    """Round 1 vs round 0 of the Phase 5 loop on the same cases."""
    if not PHASE5_ROUNDS.exists():
        return []
    rows = list(csv.DictReader(PHASE5_ROUNDS.open()))
    r0 = {r["case_id"]: r for r in rows if r["round"] == "0"}
    out = []
    for r in rows:
        if r["round"] == "1" and r["case_id"] in cases:
            b = r0[r["case_id"]]
            out.append({"case": r["case_id"], "tier": r["tier"], "notes": 3.0, "looped": False,
                        "base_l_ged": float(b["l_ged"]), "l_ged": float(r["l_ged"]),
                        "delta": round(float(r["l_ged"]) - float(b["l_ged"]), 2),
                        "targets": 0.0, "targets_closed": 0.0, "rules": None, "base_rules": None,
                        "nodes": None, "base_nodes": None})
    return out


def _ci(xs: list[float], n_boot: int = 5000, seed: int = 0) -> tuple[float, float]:
    """95% bootstrap interval of the mean."""
    if len(xs) < 2:
        return (xs[0], xs[0]) if xs else (0.0, 0.0)
    rng = random.Random(seed)
    means = sorted(mean(rng.choices(xs, k=len(xs))) for _ in range(n_boot))
    return means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1]


def _avg(rs, key):
    vals = [r[key] for r in rs if r.get(key) is not None]
    return mean(vals) if vals else None


def main() -> None:
    data = {arm: _load(arm) for arm, _, _ in ARMS if arm != "phase5_k3"}
    subset = {r["case"] for rs in data.values() for r in rs}
    data["phase5_k3"] = _phase5(subset)
    data = {a: data[a] for a, _, _ in ARMS if data.get(a)}
    if not data:
        raise SystemExit(f"no arm results in {OUT}")
    labels = {a: lab for a, lab, _ in ARMS}
    kinds = {a: kd for a, _, kd in ARMS}

    lines = ["# Patch diagnostics — 6 test cases (E2, E8, M2, M9, H2, H10)", "",
             "Each number compares the same case with and without the notes; negative L-GED "
             "change = closer to the teacher. **Upper bound** arms are built from the test "
             "case's own teacher graph, so they show the most patches could do and are not a "
             "method result. **Method** arms use only the training cases.", "",
             "All answers went through the loop guard: an answer that started repeating "
             "itself is scored on what it wrote before the loop (\"loops cut\").", "",
             "| Arm | Kind | Cases | Notes | Loops cut | L-GED change (95% CI) | % of baseline | "
             "Targeted nodes recovered | Rules per answer | Nodes per answer |",
             "|---|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    summary = {}
    for arm, rs in data.items():
        d = [r["delta"] for r in rs]
        lo, hi = _ci(d)
        base = mean(r["base_l_ged"] for r in rs)
        tgt, closed = sum(r["targets"] for r in rs), sum(r["targets_closed"] for r in rs)
        loops = sum(1 for r in rs if r.get("looped"))
        summary[arm] = {"delta": mean(d), "lo": lo, "hi": hi, "pct": 100 * mean(d) / base,
                        "notes": mean(r["notes"] for r in rs), "n": len(rs), "loops": loops,
                        "recovered": closed / tgt if tgt else None, "tgt": tgt, "closed": closed}
        rules = (f"{_avg(rs, 'base_rules'):.1f} → {_avg(rs, 'rules'):.1f}"
                 if _avg(rs, "rules") is not None else "–")
        nodes = (f"{_avg(rs, 'base_nodes'):.0f} → {_avg(rs, 'nodes'):.0f}"
                 if _avg(rs, "nodes") is not None else "–")
        lines.append(
            f"| {labels[arm]} | {kinds[arm]} | {len(rs)} | {summary[arm]['notes']:.0f} | {loops} | "
            f"{mean(d):+.1f} ({lo:+.1f} to {hi:+.1f}) | {summary[arm]['pct']:+.0f}% | "
            + (f"{closed:.0f}/{tgt:.0f} ({100 * closed / tgt:.0f}%)" if tgt else "–")
            + f" | {rules} | {nodes} |")

    cases = sorted(subset, key=lambda c: ("EMH".index(c[0]), int(c[1:])))
    lines += ["", "## Per case (L-GED change)", "",
              "| Case | Baseline | " + " | ".join(data) + " |",
              "|---|--:|" + "--:|" * len(data)]
    for c in cases:
        base = next(r["base_l_ged"] for rs in data.values() for r in rs if r["case"] == c)
        cells = []
        for rs in data.values():
            r = next((r for r in rs if r["case"] == c), None)
            cells.append((f"{r['delta']:+.1f}" + (" (loop cut)" if r.get("looped") else "")) if r else "")
        lines.append(f"| {c} | {base:.1f} | " + " | ".join(cells) + " |")

    lines += ["", "## Reading", ""]
    floor = summary.get("placebo")

    def beats(arm):
        return floor is not None and summary[arm]["hi"] < floor["lo"]

    if floor:
        lines.append(f"- **Noise floor.** Irrelevant notes: {floor['delta']:+.1f} "
                     f"({floor['lo']:+.1f} to {floor['hi']:+.1f}).")
    for arm in ("phase5_k3", "checklist_k5", "checklist_k10"):
        if arm in summary:
            s = summary[arm]
            rec = (f", {s['closed']:.0f} of the {s['tgt']:.0f} useful items written into the answer"
                   if s["tgt"] else "")
            lines.append(f"- **{labels[arm].strip('*')}**: {s['delta']:+.1f} "
                         f"({s['lo']:+.1f} to {s['hi']:+.1f}){rec}; "
                         + ("beats the placebo." if beats(arm) else "not distinguishable from placebo."))
    if "directive_k10" in summary and "oracle_k10" in summary:
        a, b = summary["directive_k10"], summary["oracle_k10"]
        lines.append(f"- **Wording (upper bound).** Same 10 nodes as a checklist: {a['delta']:+.1f}, "
                     f"{100 * a['recovered']:.0f}% recovered; as advice: {b['delta']:+.1f}, "
                     f"{100 * b['recovered']:.0f}% recovered.")
    if "llm_k10" in summary and "oracle_k10" in summary:
        a, b = summary["llm_k10"], summary["oracle_k10"]
        lines.append(f"- **LLM-written patches (upper bound).** Claude's text: {a['delta']:+.1f}, "
                     f"{100 * a['recovered']:.0f}% recovered, vs the template's {b['delta']:+.1f}, "
                     f"{100 * b['recovered']:.0f}%. Claude's notes are about twice as long.")
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    # dose curve: L-GED change against number of notes, by wording
    import plotly.graph_objects as go
    fig = go.Figure()
    series = [("Oracle, advice wording", ["oracle_k3", "oracle_k10", "oracle_all"]),
              ("Oracle, checklist wording", ["directive_k10"]),
              ("Checklist from training cases", ["checklist_k5", "checklist_k10"]),
              ("Phase 5 BM25 patches", ["phase5_k3"])]
    for name, arms in series:
        pts = [(summary[a]["notes"], summary[a]["delta"], summary[a]["lo"], summary[a]["hi"])
               for a in arms if a in summary]
        if not pts:
            continue
        xs = [0.0] + [p[0] for p in pts]
        ys = [0.0] + [p[1] for p in pts]
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines+markers", name=name,
            error_y=dict(type="data", symmetric=False,
                         array=[0.0] + [p[3] - p[1] for p in pts],
                         arrayminus=[0.0] + [p[1] - p[2] for p in pts])))
    if floor:
        fig.add_hrect(y0=floor["lo"], y1=floor["hi"], fillcolor="grey", opacity=0.2,
                      line_width=0, annotation_text="placebo 95% CI")
    fig.update_layout(title="L-GED change vs number of notes (6 test cases)",
                      xaxis_title="notes in the prompt (mean)",
                      yaxis_title="L-GED change vs no notes (lower is better)",
                      template="plotly_white")
    fig.write_html(OUT / "dose.html", include_plotlyjs="cdn")
    print(f"\n→ {OUT}/REPORT.md")


if __name__ == "__main__":
    main()
