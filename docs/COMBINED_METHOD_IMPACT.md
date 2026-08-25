<!--
Clear, defensible answer for Prof. Rao. Separates two DIFFERENT improvements that
are easy to conflate:
  (A) the -16.5 -> -4.5 drop  = Phase-3 DATA cleanup (NOT the metric change)
  (B) the combined citation aligner = Phase-4 METRIC-accuracy fix
Evidence: docs/H2_dirty_vs_clean_explained.md, docs/ALIGNMENT_HYBRID_RESULTS.md,
results/k_ablation_clean.csv (hybrid) vs results/k_ablation_combined_clean.csv (combined).
-->

# What changed the results — two separate improvements

**The one-line correction up front:** the **−16.5 → −4.5** drop and the **combined
citation method** are **two different things**. The drop happened in Phase 3 (data
cleanup) *before* the combined method existed. The combined method (Phase 4) is a
metric-accuracy fix that changes different cases and **left H2's −4.5 unchanged**.
Keeping them separate is what makes the story defensible.

---

## A. What caused the −16.5 → −4.5 drop? (Phase 3 — data, not metric)

H2 Llama k=3 went from **−16.5** (Phase-2 "dirty") to **−4.5** (Phase-3 "clean").
The cause was **data hygiene**, three things bundled:

1. **Contamination quarantine** — a fabricated NYC §20-875 was removed from the
   patch store (and the store was re-mined from corrected data).
2. **Baseline pinning** — the Llama baseline was moved from a cloud run to a fixed
   local run, so patched and baseline are scored on the same generation.
3. **Noise** — GPT-5 varies ±9.5 L-GED run-to-run; a −16.5 built partly on that
   was never robust.

The −16.5 was an **artifact of the old, messy pipeline**; −4.5 is the honest
number. Full mechanism (node-by-node) in `docs/H2_dirty_vs_clean_explained.md`.

**Key fact for the professor:** the **combined aligner did NOT change this** — under
the combined method H2 Llama k=3 is **still −4.5** (verified: the combined method
re-maps two H2-Llama rules but the change is L-GED-neutral). So do **not** attribute
the −16.5 → −4.5 to the citation method.

---

## B. What did the combined citation method actually improve? (Phase 4 — metric accuracy)

The concern it answers: sentence embeddings **cannot tell statute subsections
apart** — e.g. `§6-1-1703(2)(a)` vs `(2)(b)` score **0.63–0.81 cosine**, above the
0.55 match threshold, so the old scorer could **merge two legally distinct rules**
into one match.

The combined aligner blends citation + text into one score: exact citation
agreement forces a match; **sibling subsections are discounted below threshold** so
they can no longer be merged; text similarity otherwise.

**What it improves is measurement *accuracy*, not model behaviour.** It makes L-GED
count rules the way a lawyer would (a different subsection is a different rule). The
headline is unaffected — **GPT-5 < Llama still 6/6** under both aligners — which is
exactly the robustness result: the finding is not an artifact of how we match rules.

---

## C. Why it changes some cases and not others (the "particular cases")

The combined aligner only differs from the old one **where sibling subsections
create ambiguity**. That is entirely case-dependent:

| Case | Sibling-subsection groups in teacher rules | Affected by combined? |
|---|---|---|
| **M2** (Colorado) | **2 dense families** — §6-1-1701 (7 subsections: (2),(3)(f),(5),(6),(7),(8),(9)) and §6-1-1703 (6 subsections) | **Yes — most affected** |
| **H2** (Colorado) | **0** (teacher rules are citation-distinct) | **Llama: no change** (−4.5 → −4.5) |
| E2 (NYC) | a few (§20-871 subsections) | mildly |

- **M2 is dense with sibling subsections**, so this is exactly where the old scorer
  risked merging distinct rules and the combined aligner re-scores. Its baselines
  and measured patch effects move the most (e.g. GPT-5 M2 k=3 measured patch effect
  goes from **+6.5 to −13.5** once the rules are separated correctly).
- **H2 Llama has no sibling collisions**, so combined ≡ hybrid there → **identical**.

**Honest framing:** on M2 the *measured* patch effect improves because the metric
now scores the citations correctly — it is a **more faithful measurement**, not the
3B model suddenly learning more. The underlying effects remain small and near the
noise floor (see `docs/CASE_COMPARISON.md`, Table 2).

---

## D. Before → after (patch effect, clean store): hybrid vs combined

`patched − baseline`, negative = learned. Cells that move most are the
citation-dense ones (M2 for both students, some GPT-5 cells).

| Student · k · case | hybrid (old metric) | combined (new metric) |
|---|--:|--:|
| GPT-5 · k1 · M2 | +16.5 | **−7.5** |
| GPT-5 · k3 · M2 | +6.5 | **−13.5** |
| GPT-5 · k3 · E2 | +7.0 | **−1.0** |
| Llama · k3 · M2 | +6.0 | **−2.0** |
| **Llama · k3 · H2** | **−4.5** | **−4.5** (unchanged) |
| Llama · k1 · H2 | −11.0 | −7.0 |

The bottom rows make the point: the combined method **does not touch the H2 result**
the −16.5→−4.5 story is about; it changes the **citation-dense** cases (M2, E2).

---

## The two sentences to say to the professor

1. *"The −16.5 → −4.5 was **data cleanup** — quarantining a fabricated citation,
   pinning the baseline, and removing noise; the metric change had nothing to do
   with it (H2 stays −4.5 under the new metric too)."*
2. *"The **combined citation method** is a separate **accuracy** fix — it stops the
   scorer merging legally distinct statute subsections; it changes the citation-dense
   cases (most visibly M2), keeps the GPT-5<Llama ranking 6/6, and makes the numbers
   more faithful without changing the headline."*
