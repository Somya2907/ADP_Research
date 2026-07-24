<!--
Meeting deck — renders as slides with Marp/pandoc (slides split on '---'),
and reads fine as a plain document. Plain-language summary for Prof. Rao.
-->

# L-DRL: Teaching a Small AI to Reason About US AI Law
### Project summary & results — for the meeting with Prof. Rao

**In one line:** we're trying to make a weak AI reason about US AI law more like a strong "teacher" AI, *and prove it with numbers* — then we stress-tested whether the improvement is real.

Flow: **goal → methodology → Phase 1 → Phase 2 → Phase 3 → what's next.** (Work spans 4 git branches, all pushed; `master` untouched.)

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

| Student | k=1 | k=3 | k=5 |
|---|--:|--:|--:|
| **Llama-3B** (weak) | −2.83 | **−4.17** ✅ | +0.67 |
| **GPT-5** (frontier) | +8.33 | +5.83 | +2.50 |

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

## 7. What we're going to try now

**Fix the data (root cause)**
- Decide on **teacher re-extraction** — the teacher graphs carry the fake §20-875; re-running from the *real* statutes removes it at the source (but resets baselines). **Your call.**
- Source the **NYC DCWP rules** + the **real TX HB-149** text (the TX PDF we were given is the wrong file) → completes the statute corpus → turns the citation check fully **on**.

**Make the experiment stronger**
- **Scale up** — only 3 test cases, 1 run each; add more cases + repeats so a real effect can beat the noise.
- Turn on the **"InsightWriter"** (LLM-polished patch text) — the most likely way to get a *real* effect.

**Write it up**
- Consolidate branches → paper (target **JURIX 2026**). Honest framing: *the metric is sound (6/6); the intervention shows no effect beyond noise at this scale.*

---

## Appendix A — the exact numbers

**Model ranking (GPT-5 should score lower/better), 6 cases:** word-overlap **0/6** · meaning **6/6**.

**k-ablation — mean L-GED change (negative = patches help), across E2/M2/H2:**

| | dirty k1 | dirty k3 | dirty k5 | clean k1 | clean k3 | clean k5 |
|---|--:|--:|--:|--:|--:|--:|
| Llama-3B | −2.83 | **−4.17** | +0.67 | −1.50 | **+4.00** | −1.83 |
| GPT-5 | +8.33 | +5.83 | +2.50 | +6.50 | +6.17 | −6.17 |

**Llama / H2 / k3:** dirty −16.5 → clean −4.5 (edge-driven, not rule-recovery).
**Variance (3 repeats):** GPT-5/M2/k3 range **9.5**; Llama/H2/k3 range **0.0** (deterministic).
**Patch store:** 85 = **50 verified / 34 unverified / 1 fabricated** (§20-875).

---

## Appendix B — engineering choices we made (if asked)

| Question | What we did / found |
|---|---|
| Which small model? | "Qwen" label was wrong — it was **Llama-3.2-3B** all along; renamed. |
| How is Llama served? | Cloud failed (free route rate-limited, paid route broken) → **run it locally on the Mac GPU** — free, deterministic, reproducible. |
| Statute source? | The `.txt` files are **AI summaries with errors** → index built from **official PDFs**; a **trust gate** blocks the incomplete index from making false calls. |
| Patch quality control | Citation **classifier** (verified/fabricated/unverified) + verified-only retrieval quarantines bad patches. |

**Deferred (on purpose):** teacher re-extraction, full statute corpus, InsightWriter, patch-family ablation — all pending the meeting's direction.
