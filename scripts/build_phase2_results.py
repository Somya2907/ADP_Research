"""Task 6 — honest reporting: regenerate results/PHASE2_RESULTS.md from the clean run.

Per-case tables FIRST, means underneath, GPT-5 stated as harm, a pct_delta column,
n per cell, within-mean sign flips, the variance range (Task 5), and the
clean-vs-dirty (contamination) comparison. Reads:
  results/k_ablation_clean.csv   (store = clean [, clean_jfilter])
  results/k_ablation_dirty.csv   (store = dirty — contamination comparison)
  results/variance.csv           (optional; cell,run,l_ged)

    poetry run python scripts/build_phase2_results.py
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

RESULTS = Path("results")
CASES = ["E2", "M2", "H2"]
KS = [1, 3, 5]
STUDENTS = ["gpt5", "llama3_2b"]
LABEL = {"gpt5": "GPT-5 (frontier)", "llama3_2b": "Llama-3B (weak)"}


def _read(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open())) if path.exists() else []


def _rows_by(rows, store):
    d: dict[tuple, dict] = {}
    for r in rows:
        if r["store"] == store:
            d[(r["student"], int(r["k"]), r["case"])] = r
    return d


def _mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def main() -> None:
    clean = _read(RESULTS / "k_ablation_clean.csv")
    dirty = _read(RESULTS / "k_ablation_dirty.csv")
    variance = _read(RESULTS / "variance.csv")
    stores = [s for s in ("clean", "clean_jfilter") if any(r["store"] == s for r in clean)]

    L = ["# Phase 2 (patch injection) — results", "",
         "Δ = patched − baseline L-GED (**negative = patches help**); n=1 sample per cell "
         "(temperature-0; see variance below). Baselines are the Task-1 pinned generation.", ""]

    for store in stores:
        by = _rows_by(clean, store)
        L.append(f"## Store: `{store}`")
        L.append("")
        # ── per-case table FIRST ──
        L.append("| Student | k | " + " | ".join(f"{c} Δ (pct)" for c in CASES) + " | mean Δ |")
        L.append("|---|---|" + "---|" * (len(CASES) + 1))
        for student in STUDENTS:
            for k in KS:
                cells = []
                deltas = []
                for c in CASES:
                    r = by.get((student, k, c))
                    if r:
                        d = float(r["delta"]); deltas.append(d)
                        cells.append(f"{d:+.1f} ({float(r['pct_delta']):+.0f}%)")
                    else:
                        cells.append("—")
                mean = f"**{_mean(deltas):+.2f}**" if deltas else "—"
                L.append(f"| {LABEL[student]} | {k} | " + " | ".join(cells) + f" | {mean} |")
        L.append("")

    # ── narrative ──
    L.append("## Reading the result")
    L.append("")
    by_clean = _rows_by(clean, "clean")
    def cell_mean(student, k):
        ds = [float(by_clean[(student, k, c)]["delta"]) for c in CASES if (student, k, c) in by_clean]
        return _mean(ds)
    # best k for llama, worst for gpt5
    llama_means = {k: cell_mean("llama3_2b", k) for k in KS}
    gpt_means = {k: cell_mean("gpt5", k) for k in KS}
    if llama_means:
        bk = min(llama_means, key=llama_means.get)
        L.append(f"- **Weak student (Llama-3B):** best at k={bk} (mean Δ {llama_means[bk]:+.2f}). "
                 "But means hide sign flips — check the per-case columns above; individual cases "
                 "can be positive even at the best k.")
    if gpt_means:
        worst = max(gpt_means.items(), key=lambda kv: kv[1])
        # worst single GPT-5 cell
        worst_cell = max(((student, k, c) for (student, k, c) in by_clean if student == "gpt5"),
                         key=lambda key: float(by_clean[key]["delta"]), default=None)
        wc = (f" worst single cell {worst_cell[2]} k{worst_cell[1]}: "
              f"{float(by_clean[worst_cell]['delta']):+.1f}") if worst_cell else ""
        L.append(f"- **Frontier student (GPT-5): patches DEGRADE it** at every k "
                 f"(means all positive; worst k={worst[0]} mean {worst[1]:+.2f}).{wc} "
                 "This is harm, not neutrality.")
    L.append("")

    # ── variance ──
    if variance:
        L.append("## Variance (Task 5)")
        L.append("")
        cells = defaultdict(list)
        for r in variance:
            cells[r["cell"]].append(float(r["l_ged"]))
        for cell, vals in cells.items():
            rng = max(vals) - min(vals)
            L.append(f"- `{cell}`: {', '.join(f'{v:.1f}' for v in vals)} "
                     f"(range **{rng:.1f}**)")
        L.append("")
        L.append("Plus two zero-cost baseline resamples from the cloud→local re-pin "
                 "(Llama E2 +1.0, M2 +6.5). Interpretation: effects larger than the observed "
                 "run-to-run range are credible; a +6.5 resample means single-digit means "
                 "should not be over-read.")
        L.append("")

    # ── clean vs dirty ──
    if dirty:
        L.append("## Clean vs dirty (contamination comparison)")
        L.append("")
        L.append("`k_ablation_dirty.csv` is the pre-quarantine store (all 85 patches incl. "
                 "the fabricated §20-875). Comparing mean Δ at k=3:")
        L.append("")
        L.append("| Student | dirty k3 | clean k3 |")
        L.append("|---|---|---|")
        bd = _rows_by(dirty, "dirty")
        for student in STUDENTS:
            dm = _mean([float(bd[(student, 3, c)]["delta"]) for c in CASES if (student, 3, c) in bd])
            cm = _mean([float(by_clean[(student, 3, c)]["delta"]) for c in CASES if (student, 3, c) in by_clean])
            L.append(f"| {LABEL[student]} | {dm:+.2f} | {cm:+.2f} |")
        L.append("")
        L.append("The delta between them is how much of the apparent Phase-2 effect was "
                 "fabrication-driven.")
        L.append("")

    # ── optional analyses (S1, S3; S2 deferred) ──
    L.append("## Optional analyses")
    L.append("")
    L.append("- **S1 (patch interference):** GPT-5's per-cell harm does **not** track "
             "off-jurisdiction patch share — the largest swings (M2/k1 +16.5, H2/k5 −22.5) "
             "occur at 0% off-jurisdiction, and the jurisdiction pre-filter (`clean_jfilter`) "
             "barely moves GPT-5. So \"retrieval precision matters more for the stronger "
             "student\" is not supported here; the swings are within-jurisdiction edge "
             "disruption (see `DELTA_AUDIT.md`).")
    L.append("- **S3 (contamination sensitivity):** each contaminated case (E1/E2/H1) has "
             "one fabricated teacher rule (§20-875); excluding it drops L-GED by a uniform "
             "**−4.0** for *both* students. The fabrication adds ~4 spurious points per case "
             "but is symmetric, so it does not bias the GPT-5-vs-Llama comparison.")
    L.append("- **S2 (family ablation): deferred** — needs fresh injections, and with the "
             "clean-store effects already inside the noise band it would compare two small "
             "noisy sub-effects.")
    L.append("")
    L.append("## Bottom line")
    L.append("")
    L.append("The metric is sound (embedding recovers the GPT-5 < Llama ranking 6/6; see "
             "`docs/ALIGNMENT_METHODS.md`). But on the clean, verified-only store the "
             "patch-injection effect is **within run-to-run noise** (GPT-5 range 9.5 > its "
             "effect sizes; Llama deterministic but tiny and sign-flipping). Phase 2's "
             "\"patches help the weak student at k=3\" (−4.17) does **not survive** "
             "quarantine (clean k=3 = +4.00; the H2 −16.5 collapses to −4.5, edge-driven not "
             "rule-recovery). The Phase-2 headline was substantially contamination + noise — "
             "which Phase 3 was designed to detect.")
    L.append("")

    out = RESULTS / "PHASE2_RESULTS.md"
    out.write_text("\n".join(L))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
