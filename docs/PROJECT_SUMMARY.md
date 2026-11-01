<!--
Meeting deck — renders as slides with Marp/pandoc (slides split on '---'),
and reads fine as a plain document. Plain-language summary for Prof. Rao.
-->

# L-DRL: Teaching a Small AI to Reason About US AI Law
### Project summary & results — for the meeting with Prof. Rao

**In one line:** we're trying to make a weak AI reason about US AI law more like a strong "teacher" AI, *and prove it with numbers* — then we stress-tested whether the improvement is real.

Flow: **goal → methodology → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → what's next.** (Work spans Phases 1–5 across git branches; `master` untouched.)

---

## 1. The goal

- A **teacher** (Claude) writes the "correct" legal analysis for each case.
- Two **students** attempt the same case:
  - **GPT-5** — frontier, strong.
  - **Llama-3.2-3B** — small, weak (the one we want to improve).
- We measure **how far each student is from the teacher**, then try to **close that gap** by giving the weak student reusable "reasoning tips" (patches).

**Research question:** *do the patches actually make the weak student reason more like the teacher?*

---

## 2. Methodology — how we *measure* reasoning

**Step 1: turn each legal analysis into a structured graph** (F-I-R-A-C-O):
> **F**acts → **I**ssues → **R**ules → **A**pplication → **C**onclusion → **O**bligations, connected by typed edges (e.g. "rule *applies to* fact").

**Step 2: compare the student's graph to the teacher's** by matching up nodes and counting what's wrong:
- **missed** teacher nodes, **hallucinated** student nodes, **wrong connections**.
- Weighted by legal importance (a wrong *binding rule* costs more than a missed *fact*) → one score: **L-GED** — *lower = closer to teacher = better*.

**Key choice:** we match nodes by **meaning (sentence embeddings)**, not word overlap — so a student rephrasing the teacher isn't wrongly punished. *(This is what makes the metric trustworthy — see Phase 1.)*

---

## 3. Methodology — how we *intervene* (the patches)

**Mine (from training cases E1/M1/H1):** wherever a student missed or mis-cited a rule the teacher had, record a reusable **patch** — the controlling authority, a short "do this" tip, and trigger keywords.

**Inject (on test cases E2/M2/H2):**
1. Retrieve the **top-k** most relevant patches (BM25 keyword search).
2. Prepend them as a **"POLICY REASONING NOTES"** block before the case.
3. Re-run the student and re-score vs. its own no-patch baseline.

**Ablate:** try **k = 1, 3, 5** patches to find the best dose.
**Discipline:** strict train/test split (patches from E1/M1/H1 only), plus a leakage filter so no training-case names leak into test prompts.

---

## 4. Phase 1 — Foundation & measurement

**What we did:** built the full scoring pipeline + the patch infrastructure (patch store, statute index, misgrounding detector), and **got the measurement right**.

**Result — the measuring tool works ✅ (our solid, publishable win):**

| Node-matching method | Ranks GPT-5 better than Llama on… |
|---|---|
| Word overlap (TF-IDF) | **0 of 6 cases** — backwards every time |
| **Meaning (embeddings)** | **6 of 6 cases** — correct every time ✅ |

Word-matching mistook GPT-5's rephrasing for "hallucinations" and ranked the frontier model as *worse*. Matching by meaning fixes it completely. *(Tests: 42 → 66, all passing.)*

---

## 5. Phase 2 — Patch injection

**What we did:** mined **79 patches** from the training cases, injected the top-k, re-ran the students, and did the **k-ablation**.

**Result — looked promising:** L-GED change (**negative = patches helped**):

| Student              | k=1   | k=3         | k=5   |
| ----------------------| ------:| ------------:| ------:|
| **Llama-3B** (weak)  | −2.83 | **−4.17** ✅ | +0.67 |
| **GPT-5** (frontier) | +8.33 | +5.83       | +2.50 |

**The story:** *"patches help the weak student (best at k=3); the strong one doesn't need them."* Biggest single win: **Llama on H2 at k=3 = −16.5.**
It matched the hypothesis — so we pressure-tested it in Phase 3.

---

## 6. Phase 3 — Data-validity cleanup

**What we did:** audited the data, found **contamination**, quarantined it, pinned one consistent model run, and **re-ran cleanly**.

**Result — the Phase-2 win did NOT survive ⚠️ (the key finding):**

| Student, k=3 | Phase 2 (dirty) | Phase 3 (clean) |
|---|--:|--:|
| **Llama-3B** | **−4.17** (helped) | **+4.00** (hurt) |
| Big H2 win | **−16.5** | **−4.5** |

**Two reasons it collapsed:**
- **Contamination:** the teacher was fed AI-summarized statutes that **invented a fake NYC §20-875**. The teacher graphs cite it (E1/E2/H1), and 2 patches told students to cite it. Quarantining them (1 of 85 patches is "fabricated") erased most of the "benefit."
- **Noise > effect:** the *same* GPT-5 run varies **±9.5 points** run-to-run — bigger than the effects (±6). **On clean data, the patch effect is within noise.**

---

## 7. Phase 4 — fixing the metric, then fixing retrieval ("diverse + combined")

**What we did:** two independent fixes, at two different stages of the pipeline, that turned out to stack.

**Fix 1 — the combined aligner (fixes how we *score*).**Our concern: sentence embeddings can't tell adjacent statute subsections apart. Checked directly — he was right:

| Rule A | Rule B | Cosine similarity | Above the 0.55 match threshold? |
|---|---|--:|---|
| `§6-1-1703(2)(a)-(g)` | `§6-1-1703(6)` | 0.631 | yes — would wrongly merge |
| `§20-871(a)` | `§20-871(b)` | 0.633 | yes — would wrongly merge |

Fix: citation-token match forces a match; **sibling subsections are explicitly discounted below threshold** so they can't be merged; text similarity only where there's no citation. This changes *scoring only*, not what the student writes. Headline check: GPT-5 < Llama still **6/6** under it — an accuracy fix, not a result-mover on its own.

**Fix 2 — duty-diversified retrieval (fixes what we *inject*).** The Phase-3 k-curve was non-monotonic (k=3 *worse* than k=1) — a mining error can't produce that shape, so we pulled the actual retrieval log. At k=3, BM25 was handing the student **three near-duplicate patches on the same subsection**:

| | standard retrieval (k=3) | duty-diversified retrieval (k=3) |
|---|---|---|
| H2 patches retrieved | `(2)(a)`, `(2)(a)`, `(2)(a)(III)` — same duty ×3 | `(2)(a)`, `(2)(d)`, `(2)(f)` — three duties |

**Proof it landed in the graph, not just the score:** baseline Llama on H2 cites only a bare `§6-1-1703`, no subsection. After diversified injection its own graph cites `(2)(a)`, `(2)(d)`, `(2)(f)` — matching teacher rules **R10** (website statement) and **R12** (data correction), binding duties the baseline never touched.

**Result — both stacked** (Llama, k=3, clean verified store; negative = patches helped):

| Case | old retrieval + old aligner | + combined aligner only | + diversified retrieval only | **+ both** |
|---|--:|--:|--:|--:|
| E2 (NYC) | +10.5 (hurt) | +10.5 | +6.5 | **−1.5** |
| M2 (CO) | +6.0 | −2.0 | +3.5 | **−0.5** |
| H2 (CO) | −4.5 | −4.5 *(no sibling subsections — unchanged)* | −25.5 | **−25.5** |
| **mean** | **+4.0 (net hurt)** | +1.3 | −5.2 | **−9.2 (net help)** |

**Why this beats Phase 2's −16.5 rather than repeating its mistake:** every link is now traceable — retrieval log → real patch text → the student's own graph citations → matched teacher rule — all on the clean, contamination-quarantined store. H2 reaches **−25.5**, bigger than the old, contaminated −16.5, for a defensible reason this time: real binding duties recovered (R10, R12, R13, R19), not one lucky patch's wording.

---

## 8. Phase 5 — 30 cases, and a loop to find where learning stops

**What we did:** grew the benchmark from 6 to **30 cases** (10 easy / 10 medium / 10 hard; 15 for mining patches, 15 held out), then ran the patch method as a **loop**: inject top-3 patches, score, update the patches from what the patched student still gets wrong (re-mine, rewrite failing patches with Claude, promote patches that worked), repeat until the curve is flat.

**Result — the weak student does not improve at any round ⚠️**

Llama-3.2-3B, mean L-GED (lower = closer to teacher). Round 0 = no patches; round 1 = the Phase-4 single-pass method.

| Round | Training (15) | Held-out test (15) | Test change vs round 0 |
|--:|--:|--:|--:|
| 0 | 139.27 | 133.47 | — |
| 1 | 142.97 | 132.97 | −0.50 (95% CI ±4.8) |
| 2 | 143.03 | 132.87 | −0.60 (95% CI ±2.6) |

The loop stopped after round 2 because neither curve was improving. Without Claude rewrites the picture is the same (test +0.70 at round 2).

**What this says about Phase 4.** The Phase-4 gain (mean −9.2) was measured on three test cases. On those same three it is still negative here (E2 −5.5, M2 0.0, H2 −9.0), but across all 15 held-out cases it averages to zero: 6 improve, 8 get worse, 1 is unchanged. Injecting three notes moves a single case by about ±8 L-GED points in either direction, so a 3-case mean can land far from zero by chance. **The Phase-4 number does not generalise.**

**Why the student does not learn (what the graphs show):**
- **It writes about 3 rules per answer whatever we inject.** The teacher writes 17. Rules per answer: 3.4 → 3.1 → 2.8 across rounds.
- **It does read the notes.** Of the 48 patches injected in round 1 whose section number could be parsed, the student cited the same section exactly for 42% and the same base section for 69%. The injected rules *replace* rules it would otherwise have written; they do not add to them.
- **Net coverage falls.** The share of the teacher's rules and duties it recovers drops on training cases (19.5% → 16.6% → 14.5%) and is flat on test (18.1% → 16.8% → 17.3%).
- **The loop has little to learn from.** Of 45 patches injected into training cases in round 1, only 14 targeted a gap the scorer could link to that case's teacher graph, and 5 closed. The teacher writes the same section in several formats across cases, so evidence about a patch is split across near-duplicates.

**A first run was discarded.** It injected one Texas patch into 29 of 30 cases, because retrieval matched the word "of" in the keyword "private right of action". Retrieval now drops function words and only uses patches from the case's own jurisdictions. That run is kept under `results/loop/v1_unfiltered_retrieval/` for the record.

**Caveats:** teacher graphs still come from the statute summaries (12 fabricated citations across the 30 cases); the 24 new cases are synthetic and unreviewed; one student, k = 3. Full tables: `results/loop/full/LOOP_RESULTS.md`.

---

## 9. What we're going to try now

**Fix the data (root cause) — still open**
- **Statute corpus is not complete.** The `.txt` files the teacher reads are AI study aids, not verbatim law: the NYC file contains the fake §20-875, the Texas file is a summary, and the Texas PDF is a House Journal rather than HB 149 (see `data/statutes/index/PROVENANCE_AUDIT.md`). Sourcing the real **NYC DCWP rules** and **TX HB-149** text turns the citation check fully on.
- **Teacher re-extraction** — 13 of the 30 teacher graphs now cite the fake §20-875; re-running from verbatim statutes removes it at the source. **Your call.**

**Address what Phase 5 found**
- **The student's output is the bottleneck, not the patches.** It produces about 20 nodes where the teacher produces about 70. Options to test: let it reason in free text first and extract the graph afterwards; ask for one F-I-R-A-C-O section per call; or use a larger weak model.
- **Normalise citations** so one statutory section is one patch. This would cut the 219-patch store and give the loop usable evidence.
- **Have the 24 new cases reviewed** by a legal expert before any result on them is published.

**Write it up**
- Target **JURIX 2026**. Honest framing: *the metric is sound (6/6, robust to the citation concern); on a 30-case benchmark, in-context patching does not move a 3B student, and iterating does not change that.*

---

## Appendix A — the exact numbers

**Model ranking (GPT-5 should score lower/better), 6 cases:** word-overlap **0/6** · meaning **6/6**.

**k-ablation — mean L-GED change (negative = patches help), across E2/M2/H2:**

| | dirty k1 | dirty k3 | dirty k5 | clean k1 | clean k3 | clean k5 |
|---|--:|--:|--:|--:|--:|--:|
| Llama-3B | −2.83 | **−4.17** | +0.67 | −1.50 | **+4.00** | −1.83 |
| GPT-5 | +8.33 | +5.83 | +2.50 | +6.50 | +6.17 | −6.17 |

**Llama / H2 / k3:** dirty −16.5 → clean −4.5 (edge-driven, not rule-recovery) → **−25.5 with diverse + combined** (rule-recovery, on the clean store).
**Variance (3 repeats):** GPT-5/M2/k3 range **9.5**; Llama/H2/k3 range **0.0** (deterministic).
**Patch store:** 85 = **50 verified / 34 unverified / 1 fabricated** (§20-875).

**Phase 4 — diverse + combined, Llama k=3, clean store (mean across E2/M2/H2, negative = patches help):**

| | standard retrieval | duty-diversified retrieval |
|---|--:|--:|
| hybrid (old) aligner | +4.0 | −5.2 |
| combined aligner | +1.3 | **−9.2** |

Sibling-subsection collision example that motivated the combined aligner: `§6-1-1703(2)(a)-(g)` vs `§6-1-1703(6)` scores **0.631 cosine** — above the 0.55 match threshold, so embeddings alone would wrongly merge them.

---

## Appendix B — engineering choices we made (if asked)

| Question              | What we did / found                                                                                                                                           |
| -----------------------| ---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Which small model?    | "Qwen" label was wrong — it was **Llama-3.2-3B** all along; renamed.                                                                                          |
| How is Llama served?  | Cloud failed (free route rate-limited, paid route broken) → **run it locally on the Mac GPU** — free, deterministic, reproducible.                            |
| Statute source?       | The `.txt` files are **AI summaries with errors** → index built from **official PDFs**; a **trust gate** blocks the incomplete index from making false calls. |
| Patch quality control | Citation **classifier** (verified/fabricated/unverified) + verified-only retrieval quarantines bad patches.                                                   |
| Rule scoring accuracy | Embeddings alone merge sibling statute subsections (0.63 cosine, above threshold) → **combined aligner**: citation match forces agreement, siblings explicitly discounted. Headline ranking unchanged (6/6).|
| Retrieval redundancy  | BM25 at k=3 returned near-duplicate patches on the same subsection → **duty-diversified retrieval**: at most one patch per citation-subsection key, freeing slots for other duties.|

**Deferred (on purpose):** teacher re-extraction, full statute corpus, InsightWriter, patch-family ablation, noise-reduction (frozen teacher graph, decoding determinism) — all pending the meeting's direction.
