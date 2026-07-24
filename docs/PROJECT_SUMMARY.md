<!--
Meeting deck — renders as slides with Marp/pandoc (slides split on '---'),
and reads fine as a plain document. Plain-language summary for Prof. Rao.
-->

# L-DRL: Teaching a Small AI to Reason About US AI Law
### Project summary & results — for the meeting with Prof. Rao

**In one line:** we're trying to make a weak AI reason about US AI law more like a strong "teacher" AI, *and prove it with numbers* — then we stress-tested whether the improvement is real.

Work spans 4 git branches (all pushed; `master` untouched). This deck covers the whole arc, every approach we tried, the results, and what's left.

---

## 1. The goal, in plain English

- A **teacher** (Claude) writes the "correct" legal analysis for each case.
- Two **students** try the same case:
  - **GPT-5** — frontier, strong.
  - **Llama-3.2-3B** — small, weak (the one we want to improve).
- We turn each analysis into a **structured graph** (Facts → Issues → Rules → Application → Conclusion → Obligations) and **score how far each student is from the teacher**. This score is **L-GED** — *lower = closer = better*.
- Then we mine reusable **"policy patches"** (legal reasoning tips) from training cases and inject them into the students on new test cases, to see if they get closer to the teacher.

**The research question:** do the patches actually help the weak student?

---

## 2. How the pipeline works

```
Case  →  Teacher (Claude, with the statutes)      →  "correct" graph
Case  →  Student (GPT-5 / Llama, no statutes)      →  student graph
                          │
                 align nodes + score  →  L-GED (distance from teacher)
                          │
   mine patches from training cases → retrieve top-k → inject → re-score
```

- **6 cases**, 3 difficulty tiers × 3 jurisdictions: E1/E2 (easy, NYC), M1/M2 (medium, CO), H1/H2 (hard, multi-state).
- **Train on E1/M1/H1, test on E2/M2/H2** (strict — no leakage).

---

## 3. The journey — 5 stages across branches

| Stage | Branch | What happened |
|---|---|---|
| **0. Base pipeline** | `master` | Built extraction + the L-GED scorer + tooling (Streamlit viewer, reports). |
| **1. Infra prep** | `phase1-patch-phase-prep` | Patch store, statute index + provenance audit, misgrounding detector. |
| **2. Patch injection** | `phase2-patch-injection` / `patch-phase-complete` | Mined + injected patches; ran the k-ablation. **First "positive" result.** |
| **3. Data-validity cleanup** | `phase3-data-validity` | Found the positive result was contaminated; cleaned it up and re-ran. **Result collapsed.** |

Test count grew as we went: **42 → 66 → 83 tests, all passing.**

---

## 4. Result #1 — The measuring tool works ✅ (the solid win)

The way we **align** graph nodes decides whether the score is trustworthy. We tried two:

| Alignment method | Ranks GPT-5 better than Llama on… |
|---|---|
| **TF-IDF** (word overlap) | **0 of 6 cases** — gets it *backwards* every time |
| **Sentence embeddings** (meaning) | **6 of 6 cases** — correct every time ✅ |

- Word-matching (TF-IDF) mistakes GPT-5's rephrasing for "hallucinations," so it wrongly ranks the frontier model as worse.
- Switching to embeddings fixes it completely. **This is a genuine, defensible methods contribution** — and it holds up.

---

## 5. Result #2 — Phase 2 looked promising

We injected patches and measured the L-GED change (**negative = patches helped**):

| Student | k=1 | k=3 | k=5 |
|---|--:|--:|--:|
| **Llama-3B** (weak) | −2.83 | **−4.17** ✅ | +0.67 |
| **GPT-5** (frontier) | +8.33 | +5.83 | +2.50 |

**The story we told:** *"Patches help the weak student (best at k=3), and the strong student doesn't need them."* This matched the hypothesis nicely.

Biggest single win: **Llama on case H2 at k=3 = −16.5** (a big improvement).

---

## 6. Result #3 — Phase 3: it did **not** hold up ⚠️ (the important finding)

When we removed the **bad patches** (see next slide) and re-ran cleanly:

| Student, k=3 | Phase 2 (dirty) | Phase 3 (clean) |
|---|--:|--:|
| **Llama-3B** | **−4.17** (helped) | **+4.00** (hurt) |
| The big H2 win | **−16.5** | **−4.5** |

- The "patches help the weak student at k=3" result **flips**.
- The −16.5 headline **collapses to −4.5**, and what's left comes from edge cleanup, **not** the model recovering the right legal rules.
- GPT-5 is **harmed at every k** (not neutral).

---

## 7. Why it collapsed — Reason A: contamination

- The statute text files given to the teacher were **AI-written summaries, not the real law**.
- They **invented a NYC section §20-875 that doesn't exist** (real NYC LL 144 stops at §20-874).
- The **teacher graphs themselves cite this fake §20-875** on cases E1, E2, H1.
- So two of our patches told students to cite a **fake law** — and "recovering" it looked like an improvement.

We built a **citation classifier** that labels every patch: **50 verified / 34 unverified / 1 fabricated** (out of 85). Quarantining the fabricated one removed most of the Phase-2 "benefit."

---

## 8. Why it collapsed — Reason B: noise is bigger than the effect

We ran the **same** experiment 3 times:

| Cell | Run-to-run spread |
|---|--:|
| **GPT-5** / M2 / k3 | **9.5 points** (120.0, 119.5, 110.5) |
| **Llama** / H2 / k3 | **0.0 points** (158, 158, 158 — perfectly repeatable) |

- GPT-5 (cloud) wobbles **±9.5 points** run to run — **larger than the effects we're measuring (±6)**. So its results are indistinguishable from random.
- Local Llama is **deterministic** (0 wobble), so its numbers are exact — but the effect is **tiny and flips sign** case to case.

**Bottom line: on clean data, the patch effect is within noise.**

---

## 9. Everything we tried — (a) Models & serving

| Approach | Outcome |
|---|---|
| Small model "Qwen3-4B" label | ❌ mislabel — was actually Llama; renamed repo-wide |
| Llama via OpenRouter **free** (Venice) | ⚠️ works but heavily rate-limited (429s) |
| Llama via OpenRouter **paid** (Cloudflare) | ❌ broken — returns empty responses |
| **Llama local via HuggingFace on Mac GPU (MPS)** | ✅ **adopted** — free, deterministic, reproducible |
| Teacher non-streaming | ❌ hit 10-min API limit on hard cases |
| **Teacher streaming (Claude Opus)** | ✅ adopted |

*Lesson: getting the small model to run reliably was a real fight; local was the answer.*

---

## 10. Everything we tried — (b) Scoring & alignment

| Approach | Outcome |
|---|---|
| Citation-first rule matching (`§20-871` ≡ `Section 20-871`) | ✅ adopted (high-confidence first pass) |
| TF-IDF alignment (threshold 0.1) | ⚠️ kept only as an ablation — ranks backwards |
| **Sentence-embedding alignment** (bge-small, 0.55) | ✅ **primary** — 6/6 correct |
| Threshold calibration on E1 | ⚠️ works but tuned on one case (see "to-do") |
| Greedy node-matching + graph-edit-distance (L-GED) | ✅ the metric itself |
| Misgrounding detector (right rule, wrong section) | ✅ built; kept as a flag (teacher is contaminated) |

---

## 11. Everything we tried — (c) The patches

| Approach | Outcome |
|---|---|
| Family A: missing rule / missing obligation | ✅ bulk of the store |
| Family B: misgrounding | ✅ built (semantics caveated — teacher contamination) |
| Deterministic patch text (templates) | ✅ used (fully reproducible) |
| **InsightWriter** (LLM polishes patch text) | ⏸ **deferred** — likely lever to make patches better |
| BM25 retrieval + keyword triggers | ✅ how we pick top-k |
| Train→test leakage filter (drop patches naming a training party) | ✅ safety firewall |
| **k ∈ {1, 3, 5}** budget ablation | ✅ completed |
| Store: **dirty** (all) vs **clean** (verified-only) vs **clean+jurisdiction-filter** | ✅ all three run; clean is the honest one |

---

## 12. Everything we tried — (d) Data validity (Phase 3)

| Approach | Outcome |
|---|---|
| Build statute index from `.txt` files | ❌ rejected — all 4 are AI summaries with errors |
| **Build index from official PDFs** (`pdftotext`) | ✅ CO + NYC verified; DCWP & TX missing |
| Trust gate (don't use an incomplete index for verdicts) | ✅ conservative by design |
| **Citation classifier** (verified / fabricated / unverified) | ✅ quarantines the fake §20-875 |
| Baseline pinning + guard (cloud vs local mismatch) | ✅ one consistent generation, asserted |
| Variance study (repeat runs) | ✅ showed effects are within noise |
| S1 (does off-jurisdiction share explain GPT-5 harm?) | ✅ **no** |
| S3 (how much does the fake rule distort the score?) | ✅ **±4.0/case, symmetric** — doesn't bias the comparison |
| S2 (patch-family ablation) | ⏸ deferred (effects already within noise) |

---

## 13. What we learned (the honest position)

1. **The metric is sound.** Embedding alignment recovers the correct model ranking 6/6. This survives everything and is publishable.
2. **The Phase-2 "patches help the weak student" headline was mostly an artifact** — a mix of (a) patches built on a fabricated law section, and (b) run-to-run noise larger than the effect.
3. **The data had a hidden problem:** the teacher itself was fed AI-summarized statutes and cites a fake section. That's an upstream contamination we caught and isolated.
4. This is a **more honest and more interesting** paper than "our method works": *a cautionary, well-instrumented negative result about knowledge injection at small scale, on a metric we can defend.*

---

## 14. What's yet to be done

**Data / correctness**
- [ ] Source the **NYC DCWP rules** + the **real TX HB-149** statute (the provided TX PDF is the wrong file — a House Journal).
- [ ] Complete the statute corpus → make the index **trustworthy** → turn on the citation-verification check + real-vs-fake misgrounding subtype.
- [ ] Re-calibrate the embedding threshold across all cases (currently tuned on E1 only).

**Experiment strength**
- [ ] **Scale up** — only 3 test cases and 1 sample per cell; the noise finding demands more cases + repeats.
- [ ] Enable the **InsightWriter** (LLM-polished patches) — the most likely way to get a real effect.

**Writeup**
- [ ] Consolidate branches and write the paper (target: JURIX 2026 / ICAIL 2026 workshop).

---

## 15. Decisions for you, Prof. Rao

1. **Re-extract the teacher?** The teacher graphs carry the fabricated §20-875 (E1/E2/H1). Re-extracting from the *real* statutes would remove the contamination at the source — but resets every baseline. We deliberately **did not** touch it, pending your call.
2. **What does the paper claim?** Recommended honest framing: *"The L-GED metric with embedding alignment reliably ranks models; the patch intervention shows no effect distinguishable from noise at this corpus scale."*
3. **Invest in scale-up + InsightWriter** before claiming any intervention effect?
4. **Priority order** for the remaining to-do list?

---

## Appendix — the exact numbers

**Model ranking (GPT-5 should score lower/better than Llama), 6 cases:**
- TF-IDF: **0/6** correct · Embedding: **6/6** correct.

**k-ablation — mean L-GED change (negative = patches help), across E2/M2/H2:**

| | dirty k1 | dirty k3 | dirty k5 | clean k1 | clean k3 | clean k5 |
|---|--:|--:|--:|--:|--:|--:|
| Llama-3B | −2.83 | **−4.17** | +0.67 | −1.50 | **+4.00** | −1.83 |
| GPT-5 | +8.33 | +5.83 | +2.50 | +6.50 | +6.17 | −6.17 |

**Llama / H2 / k3:** dirty −16.5 → clean −4.5 (edge-driven, not rule-recovery).

**Variance (3 repeats):** GPT-5/M2/k3 range **9.5**; Llama/H2/k3 range **0.0** (deterministic).

**Patch store:** 85 total = **50 verified / 34 unverified / 1 fabricated** (§20-875).

**Contamination sensitivity (S3):** removing the fake §20-875 rule = **−4.0 L-GED for both students** (symmetric, doesn't bias the comparison).

**Files:** `results/{k_ablation_dirty,k_ablation_clean,variance}.csv`, `results/{PHASE2_RESULTS,DELTA_AUDIT}.md`, `docs/{ALIGNMENT_METHODS,BASELINE_PROVENANCE}.md`, `data/statutes/index/PROVENANCE_AUDIT.md`.
