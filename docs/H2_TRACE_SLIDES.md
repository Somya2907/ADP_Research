<!--
Slide deck (paste-ready) — Case H2 reasoning traces, phase by phase.
Each block = one slide: TITLE, a one-line takeaway, table(s)/trace, bullets.
H2 chosen because it shows the largest L-GED movement of any case across all three phases.
Numbers: embedding alignment; snapshots + results/k_ablation_{dirty,clean}.csv.
Full untruncated traces: docs/REASONING_TRACES.md.
-->

# Case H2 — reasoning traces, phase by phase (paste into the deck)

**Why H2?** Of all six cases, H2 shows the **largest L-GED movement** at every phase — the biggest metric correction (Phase 1), the biggest apparent patch win (Phase 2), and the biggest collapse of that win (Phase 3). It's the clearest single case to *see* what each phase did.

**The case:** "AutoApprove" — a two-stage AI lending system (Stage 1 fully automated, Stage 2 human-reviewed). Question: is it a **high-risk AI system under the Colorado AI Act**, is the vendor a deployer or developer, and what must they fix by June 30 2026?

FIRACO = **F**acts → **I**ssues → **R**ules → **A**pplication → **C**onclusion → **O**bligations. L-GED = distance from the teacher (**lower = better**).

---

## Slide 1 — The three analyses (the baseline traces)

**Title:** H2 — teacher vs. students, before any intervention

**Takeaway:** The weak student collapses a 77-node analysis into 14 nodes — one issue, one step.

| | Teacher (Claude) | GPT-5 (frontier) | Llama-3B (weak) |
|---|---|---|---|
| **Total nodes** | 77 | 68 | **14** |
| **Issues** | 7 | 5 | **1** |
| **Rules** | 20 (Colorado AIA subsections) | 10 (CO Act, section-level) | 3 |
| **Application steps** | 16 | 14 | **1** |
| **Obligations** | 10 | 14 | **1** |
| **L-GED** (embedding) | — (reference) | **125.5** | **162.5** |

- **Teacher** frames the full analysis: Stage-1 vs Stage-2 high-risk, deployer-vs-developer, the GC-memo/Morrison-memo authority conflict, a June-2026 compliance-gap inventory.
- **GPT-5** tracks that spine (5 of 7 issues) but more compactly.
- **Llama** frames **one** issue and grounds its lead rule in **NYC law — on a Colorado case**.

---

## Slide 2 — What each model actually wrote (trace excerpt)

**Title:** H2 — the reasoning, side by side

**Takeaway:** GPT-5 reasons in parallel to the teacher; Llama writes a stub and cites the wrong jurisdiction.

| | Issues framed | Lead rules cited |
|---|---|---|
| **Teacher** | I1 Stage-1 high-risk? · I2 Stage-2 high-risk / "substantial factor"? · I3 memo conflict vs statute · I4 deployer or developer? · I5 gap inventory by 6/30/26 · (+2) | `§6-1-1701(7)` high-risk def · `§6-1-1703(2)(b)` impact assessment · `§6-1-1703` consumer notice … (20 total) |
| **GPT-5** | I1 high-risk Stage 1 & 2? · I2 resolve memo conflict · I3 deployer or developer? · I4 CO compliance by 6/30/26 · I5 FinLogic duties | `§6-1-1704` deployer duties · `§6-1-1707` NIST safe harbor · `§24-4-103` APA (memos non-binding) … (10) |
| **Llama** | I1 Is AutoApprove "high-risk" under the CO AI Act? | `NYC LL 144 §20-871` ✗ wrong statute · `CO §6-1-1703` · `NIST AI 100-1` |

- Llama's single application step: *"AutoApprove's automated decisions may be 'substantial factors' in consequential decisions"* — correct direction, but no deployer/developer analysis, no obligations beyond one.
- **Its L-GED (162.5) is almost all *missing* nodes (63), not wrong ones (0 hallucinations).** It doesn't err; it omits.

---

## Slide 3 — Phase 1: the measurement (before → after)

**Title:** Phase 1 — fixing the metric flipped H2's ranking

**Takeaway:** Word-overlap scoring ranked the *frontier* model as worse on H2; meaning-based scoring fixed it.

| H2 L-GED | GPT-5 | Llama-3B | Ranking |
|---|---|---|---|
| **Word overlap (TF-IDF)** | 196.0 | 171.5 | ✗ GPT-5 scored *worse* |
| **Meaning (embeddings)** | **125.5** | **162.5** | ✓ GPT-5 correctly better |

- Under TF-IDF, GPT-5's **29 "hallucinations"** were mostly *paraphrases* of the teacher it failed to match on words — inflating its score above Llama's.
- Embeddings recognize the paraphrases as the same nodes → hallucinations drop 29 → 7, and the ranking corrects.
- **This is the project's solid, publishable win:** across all 6 cases, embedding ranks GPT-5 < Llama **6/6**; TF-IDF **0/6**. H2 is the most dramatic flip.

---

## Slide 4 — Phase 2: patch injection (before → after)

**Title:** Phase 2 — patches looked like they *rescued* Llama on H2

**Takeaway:** Injecting the top-3 mined patches dropped Llama's H2 L-GED by 16.5 — the biggest single win in the study.

| Llama H2 | L-GED | Δ |
|---|---|---|
| No-patch baseline | 162.5 | — |
| **+ top-3 patches (k=3, dirty store)** | **146.0** | **−16.5** ✅ |

**What changed in the trace — rules cited:**

| Baseline (3 rules) | + patches (5 rules) |
|---|---|
| `NYC §20-871` ✗ · `CO §6-1-1703` · `NIST 100-1` | `CO §6-1-1703(2)(a)` · `CO §6-1-1703(2)(b)` · `CO §6-1-1703(2)(c)` · `NYC §20-871` · `NYC §20-872` |

- The patches injected **three correct Colorado deployer-duty subsections** the student had never cited → looked like genuine rule recovery.
- The hypothesis seemed confirmed: *"patches help the weak student, best at k=3."* So we pressure-tested it.

---

## Slide 5 — Phase 3: data-validity cleanup (before → after)

**Title:** Phase 3 — most of the H2 "win" was contamination, not learning

**Takeaway:** On the clean, verified-only store the −16.5 shrinks to −4.5, and the same patches *hurt* GPT-5.

| Llama H2, k=3 | Phase 2 (dirty) | Phase 3 (clean) |
|---|---|---|
| L-GED | 146.0 | 158.0 |
| **Δ vs baseline** | **−16.5** | **−4.5** |
| GPT-5 H2, k=3 (Δ) | −11.0 | **+5.0** (hurt) |

**What changed in the trace — rules cited:**

| Phase 2 dirty (5 rules) | Phase 3 clean (3 rules) |
|---|---|
| CO §6-1-1703(2)(a/b/c) + NYC §20-871 + §20-872 | `CO §6-1-1703(2)(a)` · `NYC §20-871` · `NIST RMF 1.0` |

- **Two causes of the collapse:** (1) the extra CO subsections came from patches mined off a **contaminated store** and weren't verified, so quarantine removed them; (2) the teacher graph itself carries a **fabricated `§20-875`**, and GPT-5's variance is ±9.5 — bigger than a 4.5 effect.
- The clean patch still does one real thing: it **fixes Llama's lead-rule grounding** from `NYC §20-871` → `CO §6-1-1703(2)(a)`. But it does **not** add coverage — still 1 issue.
- **Honest read:** on clean data the patch effect is **within noise**. Phase 3 was built to catch exactly this.

---

## Slide 6 — H2 across all three phases (the whole story)

**Title:** H2 — one case, three phases

**Takeaway:** A sound metric, an apparent win, and an honest correction — all visible in one case.

| Phase | What it did to H2 | The number |
|---|---|---|
| **Phase 1 — Measurement** | Fixed the ranking (TF-IDF had GPT-5 worse) | GPT-5 196→**125.5**; ranking ✗→✓ |
| **Phase 2 — Patch injection** | Top-3 patches, Llama k=3 | **−16.5** (looked like recovery) |
| **Phase 3 — Cleanup** | Quarantine + pinned baseline, Llama k=3 | **−4.5** (win mostly contamination) |

- The **metric is trustworthy** (H2 ranking corrected, 6/6 overall).
- The **intervention's headline did not survive** honest data hygiene: the recovery was largely fabricated CO subsections + run-to-run noise.
- **Next:** the ceiling of in-context patching for a 3B is low — the reasoning trace still collapses to one issue. The path to real gains is **learning from the teacher** using L-GED as a reward (see `IMPROVEMENT_DIRECTIONS.md`).

---

*Full untruncated H2 traces (every node, complete text): `docs/REASONING_TRACES.md`. Interactive: the "Reasoning traces" page in `scripts/view_graph.py` (pick H2). Numbers regenerate via `scripts/build_traces_doc.py` and `scripts/run_k_ablation.py`.*
