<!--
Meeting deck — renders as slides with Marp/pandoc (slides split on '---'),
and reads fine as a plain document. Plain-language summary for Prof. Rao.
-->

# L-DRL: Teaching a Small AI to Reason About US AI Law
### Project summary & results — for the meeting with Prof. Rao

**In one line:** we're trying to make a weak AI reason about US AI law more like a strong "teacher" AI, *and prove it with numbers* — then we stress-tested whether the improvement is real.

Work spans 4 git branches (all pushed; `master` untouched). Flow of this deck: **goal → approaches → Phase 1 → Phase 2 → Phase 3 → what's next.**

---

## 1. The goal

- A **teacher** (Claude) writes the "correct" legal analysis for each case.
- Two **students** attempt the same case:
  - **GPT-5** — frontier, strong.
  - **Llama-3.2-3B** — small, weak (the one we want to improve).
- Each analysis becomes a **structured graph** (Facts → Issues → Rules → Application → Conclusion → Obligations). We **score how far each student is from the teacher** with a metric called **L-GED** — *lower = closer = better*.
- Then we mine reusable **"policy patches"** (legal reasoning tips) from training cases and inject them into the students on new test cases.

**Research question:** *do the patches actually make the weak student reason more like the teacher?*

---

## 2. The setup — how the pipeline works

```
Case  →  Teacher (Claude, given the statutes)   →  "correct" graph
Case  →  Student (GPT-5 / Llama, no statutes)    →  student graph
                        │
              align nodes + score  →  L-GED  (distance from teacher)
                        │
  mine patches from TRAINING cases → retrieve top-k → inject → re-score TEST cases
```

- **6 cases** — 3 difficulty tiers × 3 jurisdictions: E1/E2 (easy, NYC), M1/M2 (medium, CO), H1/H2 (hard, multi-state).
- **Train on E1/M1/H1, test on E2/M2/H2** — strict, no leakage.

---

## 3. Approaches we explored — models & scoring

**Models & serving** (getting the small model to run was a real fight):

| Approach | Outcome |
|---|---|
| Small model labeled "Qwen3-4B" | ❌ mislabel — was actually Llama; renamed repo-wide |
| Llama via OpenRouter **free** (Venice) | ⚠️ works but heavily rate-limited |
| Llama via OpenRouter **paid** (Cloudflare) | ❌ broken — returns empty responses |
| **Llama local on the Mac GPU (HuggingFace/MPS)** | ✅ **adopted** — free, deterministic, reproducible |

**Scoring & alignment:**

| Approach | Outcome |
|---|---|
| Citation-first rule matching (`§20-871` ≡ `Section 20-871`) | ✅ adopted |
| TF-IDF alignment (word overlap) | ⚠️ ablation only — ranks models *backwards* |
| **Sentence-embedding alignment** (meaning) | ✅ **primary** — ranks correctly |

---

## 4. Approaches we explored — patches & data validity

**The patches:**

| Approach | Outcome |
|---|---|
| Family A (missing rule/obligation) + Family B (misgrounding) | ✅ both built |
| Deterministic template text vs **LLM-polished ("InsightWriter")** | ✅ templates used · ⏸ LLM-polish **deferred** |
| BM25 retrieval + train→test leakage filter | ✅ how we pick top-k, safely |
| Budget ablation **k ∈ {1, 3, 5}** | ✅ completed |
| Store variants: **dirty** (all) / **clean** (verified-only) / clean+jurisdiction-filter | ✅ all three run |

**Data validity (Phase 3):** build the statute index from **official PDFs, not the AI-summary `.txt` files**; a **citation classifier** (verified/fabricated/unverified); a **trust gate**; a **variance study**. All ✅.

---

## 5. Phase 1 — Foundation & measurement

**What we did:** built the full scoring pipeline + the patch infrastructure (patch store with BM25 retrieval, statute index, misgrounding detector), and **fixed the alignment**.

**Result — the measuring tool works ✅ (our solid, publishable win):**

| Alignment method | Ranks GPT-5 better than Llama on… |
|---|---|
| TF-IDF (word overlap) | **0 of 6 cases** — backwards every time |
| **Sentence embeddings** | **6 of 6 cases** — correct every time ✅ |

Word-matching mistakes GPT-5's rephrasing for "hallucinations." Embeddings fix it completely. *Tests: 42 → 66, all passing.*

---

## 6. Phase 2 — Patch injection

**What we did:** mined **79 patches** from the training cases, injected the top-k as a "policy notes" block before each test case, re-extracted, and ran the **k-ablation**.

**Result — looked promising:** L-GED change (**negative = patches helped**):

| Student | k=1 | k=3 | k=5 |
|---|--:|--:|--:|
| **Llama-3B** (weak) | −2.83 | **−4.17** ✅ | +0.67 |
| **GPT-5** (frontier) | +8.33 | +5.83 | +2.50 |

**The story we told:** *"patches help the weak student (best at k=3); the strong one doesn't need them."* Biggest single win: **Llama on H2 at k=3 = −16.5.** This matched the hypothesis — so we scrutinized it in Phase 3.

---

## 7. Phase 3 — Data-validity cleanup

**What we did:** audited the data, found contamination, **quarantined it**, pinned one consistent model generation, and **re-ran cleanly**.

**Result — the Phase-2 win did NOT hold up ⚠️ (the important finding):**

| Student, k=3 | Phase 2 (dirty) | Phase 3 (clean) |
|---|--:|--:|
| **Llama-3B** | **−4.17** (helped) | **+4.00** (hurt) |
| Big H2 win | **−16.5** | **−4.5** |

**Two reasons it collapsed:**
- **Contamination:** the teacher was fed AI-summarized statutes that **invented a fake NYC §20-875**; the teacher graphs cite it (E1/E2/H1), and 2 patches told students to cite it. Removing them (1 of 85 patches is "fabricated") erased most of the "benefit."
- **Noise > effect:** the same GPT-5 run varies **±9.5 points** run-to-run — bigger than the effects (±6). *On clean data, the patch effect is within noise.*

---

## 8. What we're going to try now

**Fix the data (root cause)**
- Decide on **teacher re-extraction** — the teacher graphs carry the fake §20-875; re-running from the *real* statutes removes it at the source (but resets baselines). **Your call.**
- Source the **NYC DCWP rules** + the **real TX HB-149** text (the TX PDF we were given is the wrong file) → completes the statute corpus → turns the citation-verification check fully **on**.

**Make the experiment stronger**
- **Scale up** — only 3 test cases, 1 run each; add more cases + repeats so effects can beat the noise.
- Turn on the **InsightWriter** (LLM-polished patches) — the most likely way to produce a *real* effect.
- Re-calibrate the embedding threshold across all cases (currently tuned on E1 only).

**Write it up**
- Consolidate branches → paper (target **JURIX 2026**, fallback ICAIL 2026 workshop). Honest framing: *the metric is sound (6/6); the intervention shows no effect beyond noise at this scale.*

---

## Appendix — the exact numbers

**Model ranking (GPT-5 should score lower/better), 6 cases:** TF-IDF **0/6** · Embedding **6/6**.

**k-ablation — mean L-GED change (negative = patches help), across E2/M2/H2:**

| | dirty k1 | dirty k3 | dirty k5 | clean k1 | clean k3 | clean k5 |
|---|--:|--:|--:|--:|--:|--:|
| Llama-3B | −2.83 | **−4.17** | +0.67 | −1.50 | **+4.00** | −1.83 |
| GPT-5 | +8.33 | +5.83 | +2.50 | +6.50 | +6.17 | −6.17 |

**Llama / H2 / k3:** dirty −16.5 → clean −4.5 (edge-driven, not rule-recovery).
**Variance (3 repeats):** GPT-5/M2/k3 range **9.5**; Llama/H2/k3 range **0.0** (deterministic).
**Patch store:** 85 = **50 verified / 34 unverified / 1 fabricated** (§20-875).
**Contamination sensitivity:** removing the fake rule = **−4.0 L-GED for both students** (symmetric — doesn't bias the comparison).

**Files:** `results/{k_ablation_dirty,k_ablation_clean,variance}.csv`, `results/{PHASE2_RESULTS,DELTA_AUDIT}.md`, `docs/{ALIGNMENT_METHODS,BASELINE_PROVENANCE}.md`, `data/statutes/index/PROVENANCE_AUDIT.md`.
