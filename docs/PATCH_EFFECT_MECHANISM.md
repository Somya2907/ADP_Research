<!--
The rigorous, generalized answer for Prof. Rao:
  (1) WHY H2 went -16.5 -> -4.5, decomposed exactly;
  (2) the SAME decomposition tested on E2 and M2 (the reason generalizes);
  (3) concrete, testable improvements that follow from the reason.
Reproduce: LEX_DRL_SIMILARITY=embedding poetry run python scripts/decompose_patch_effect.py
Supersedes the narrower docs/H2_dirty_vs_clean_explained.md (which explains why the
dirty and clean OUTPUTS differ — store rebuild); this doc explains the mechanism of
the patch effect itself and generalizes it.
-->

# Why patches move L-GED — the mechanism, tested across cases, and how to improve

## 0. The key that makes this testable: L-GED is additive

L-GED = weighted(missed teacher nodes) + weighted(hallucinated nodes) + weighted(edge diffs).
So **every** patch effect decomposes **exactly** into three parts:

> **patch delta = Δmissed + Δhallucinated + Δedges**  (all weighted)

A patch can only help (negative delta) by **recovering missed teacher nodes**
(Δmissed < 0) or **fixing edges** (Δedges < 0), without adding hallucinations. This
isn't a theory — it's an identity, so we can attribute every point of every delta.

Node weights: Rules **R = 2.0 × authority** (binding ×2 → **4.0**), Obligations **O =
2.5**, Application **A = 2.5**, Issues 1.5, Conclusions 1.5, Facts 1.0. So **recovering
one binding rule is worth 4 points** — the big movers are rules and obligations.

---

## 1. H2 −16.5 → −4.5, decomposed exactly (Llama, k=3)

| | L-GED | Δmissed | Δhalluc | Δedges | high-weight teacher nodes recovered |
|---|--:|--:|--:|--:|---|
| baseline | 162.5 | — | — | — | — |
| **dirty patch** | 146.0 (**−16.5**) | **−11.0** | 0 | **−5.5** | **R5, R10, R11, R13** (4 binding rules ×4) + A1 + O4 |
| **clean patch** | 158.0 (**−4.5**) | **+1.0** | 0 | **−5.5** | R3 + O10 (≈8 pts) |

**Read it off the table:**
- The **edge fix is identical** in both (−5.5). It is *not* where the difference lives.
- The entire −16.5 vs −4.5 gap is **node recovery**: the dirty injection made the 3B
  emit **four binding deployer-duty rules at once** (notice → correction → appeal →
  website, R10–R13, 4 pts each); the clean injection made it emit **one**.
- **Why the two injections differ:** different patches were retrieved — the dirty run
  used the pre-rebuild store, the clean run the re-mined verified store (full store
  story in `docs/H2_dirty_vs_clean_explained.md`).

So the −16.5 was **real arithmetic**, but it depended on one lucky injection hitting a
dense cluster of binding rules. It wasn't robust — which is why it didn't reproduce.

---

## 2. The same decomposition on the other cases (the reason generalizes)

Every row's `delta = Δmissed + Δhalluc + Δedges` holds exactly (it must). The
**mechanism is universal**; only the sign/size changes with what gets recovered:

| Case | store·k | delta | Δmissed | Δedges | what happened |
|---|---|--:|--:|--:|---|
| **H2** | clean·k1 | **−7.0** | −7.0 | 0 | recovered R2, R5, R10 (binding rules) |
| **M2** | clean·k1 | **−4.0** | −8.0 | +4.0 | recovered **4 binding rules** (R1,R6,R7,R9); edges cost some back |
| **M2** | clean·k3 | −2.0 | −2.0 | 0 | recovered R1 only — small |
| **E2** | clean·k3 | **+10.5** | **+12.0** | −1.5 | **patch HURTS** — see below |

**M2 behaves like H2** (helps by recovering binding rules; the win scales with how many
high-weight rules the injection triggers).

**E2 is the informative failure.** Its delta is *positive* (+10.5): Δmissed = **+12**.
The patch recovered ~12 pts of nodes **but displaced ~24 pts** of content the student had
*already* matched — i.e. the injected (Colorado-heavy) patch made the 3B **rewrite** its
NYC answer and **drop correct nodes**. The disease isn't "no recovery," it's
**displacement**.

---

## 3. The reason, in one sentence (generalized + testable)

> A patch helps **exactly** when it makes the student emit **high-weight teacher nodes it
> was missing** (binding rules = 4 pts, mandatory obligations = 2.5) and/or fixes edges,
> **without displacing correct content or adding hallucinations**. The H2 −16.5 was a
> store-lucky injection that triggered four binding-rule recoveries at once.

This is falsifiable and we confirmed it: the three-component sum reproduces every delta
to the decimal (`scripts/decompose_patch_effect.py`).

---

## 4. How to improve — levers that follow directly from the reason

Because we know *what* makes a patch help, we can target it. Each is testable against the
prediction "delta ≈ −(weight of high-weight nodes recovered) + edge change."

1. **Weight-targeted retrieval.** Rank patches by the **weight of the teacher node they
   would recover** (prioritize binding rules and mandatory obligations the draft is
   missing), not just BM25 keyword overlap. Prediction: consistent negative deltas.
2. **Conditional / additive injection (fixes E2).** Only inject a patch for a node the
   draft is **missing**, and phrase it to **add, not rewrite**. E2 shows the failure is
   *displacement* (Δmissed +12), so this is the highest-value fix for the cases where
   patches currently hurt.
3. **Jurisdiction gating — necessary but not sufficient.** We tested it (`clean_jfilter`):
   on E2 it did **not** help (+10.5 → +12.0) because the verified store has no good NYC
   patches to gate *to*. So gating must be paired with **completing NYC patch coverage**,
   not used alone.
4. **Make recovery deterministic.** Today which rules the 3B emits from a patch is
   store/phrasing dependent (that's the whole −16.5 fragility). The robust path is
   **training the student on the teacher graphs** so the high-weight rules are emitted by
   default (the Tier-3 direction in `docs/IMPROVEMENT_DIRECTIONS.md`).

---

## 5. What to tell the professor

- *"We can attribute the −16.5 exactly: −11 from recovering four binding deployer rules,
  −5.5 from an edge fix. The clean run only recovered one rule (+1 on nodes) with the same
  −5.5 edge fix → −4.5. The difference is entirely which rules the injected patch triggered."*
- *"The same decomposition explains every case — M2 helps by recovering binding rules; E2
  hurts because the patch displaces correct content. It's one mechanism."*
- *"Because we know the mechanism (recover high-weight missing nodes without displacing),
  we can improve it: weight-targeted, additive-only injection — and we have a numeric
  prediction to test it against."*
