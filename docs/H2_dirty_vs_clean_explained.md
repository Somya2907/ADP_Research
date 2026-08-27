<!--
Explainer for Prof. Rao: why H2's patched L-GED moved from -16.5 (dirty) to -4.5 (clean),
and why it was NOT the fabricated NYC §20-875 patch. Plain language + the exact node-level
evidence. Companion to docs/H2_TRACE_SLIDES.md and docs/REASONING_TRACES.md.
-->

# Why H2's patch result changed from −16.5 to −4.5

**The question:** In Phase 3 we quarantined a fabricated NYC §20-875 patch. But if §20-875 was never used for H2 (a *Colorado* case), why did H2's patched result change at all? Shouldn't the dirty and clean outputs be identical?

**Short answer:** They differ because Phase 3 changed **more than just §20-875**. We didn't only delete one bad patch — we **rebuilt the entire patch library from scratch**. So Llama got a *different set of patches* in the clean run than in the dirty run, and a different cheat-sheet produces a different answer. The −16.5 was never a solid result; it depended on the old library, and it didn't reproduce once we rebuilt everything honestly.

---

## 1. Phase 3 was three changes bundled together, not one

When we "cleaned up," we did three things at once:

1. **Re-pinned the baselines** — ran Llama locally (Mac) instead of in the cloud.
2. **Rebuilt the entire patch library** ("re-mining") from the corrected data.
3. **Kept only verified patches** at retrieval time.

The one that answers this question is **#2 — the full library rebuild.**

## 2. The "cheat-sheet" intuition

Think of the retrieved patches as a **cheat-sheet** handed to Llama before it answers a case.

| Run | Cheat-sheet Llama received |
|---|---|
| **Dirty** (Phase 2) | the **old** library |
| **Clean** (Phase 3) | a **freshly rebuilt** library |

Neither cheat-sheet contained §20-875 for H2 — but the two cheat-sheets were **still different** (different patches, different wording). Give a model a different cheat-sheet and it writes a different answer → it matches different teacher rules → it gets a different score. That is the entire reason 146.0 became 158.0.

## 3. The proof it was NOT §20-875 (and not even the "verified-only" filter)

- **§20-875 is NYC-only.** H2 is a **Colorado** case, so that patch can never be retrieved for it. It appears in **zero** H2 outputs (dirty or clean).
- With **today's rebuilt library**, retrieving "all patches" vs "verified-only" for H2 returns the **exact same 3 patches**. So the verified-only filter, by itself, **changes nothing for H2**.
- Therefore the only reason the old dirty output differs is that it was produced with the **old library, before the rebuild** — not because a bad patch was removed.

---

## 4. The exact size of the change (node-level evidence)

Both patched outputs were scored against the same teacher and the same baseline (162.5). Breaking the L-GED into its parts:

| | Missing-node cost (`v_miss`) | Edge cost (`e_diff`) | L-GED | Δ vs baseline |
|---|--:|--:|--:|--:|
| Baseline (no patch) | 155.5 | 7.0 | 162.5 | — |
| **Dirty k=3** | 144.5 | 1.5 | 146.0 | **−16.5** |
| **Clean k=3** | 156.5 | 1.5 | 158.0 | **−4.5** |

- The **edge fix is identical** in both (7.0 → 1.5 = −5.5).
- **The entire 12-point gap (−16.5 vs −4.5) is in node recovery** — *which* teacher nodes each answer happened to match.

**What the dirty answer matched that the clean one missed (26.0 pts):** the Colorado deployer **consumer-duty** rules —

| Teacher node | Weight | Meaning |
|---|--:|---|
| R10 | 4.0 | Publish website statement on high-risk AI |
| R11 | 4.0 | Pre-decision consumer notice |
| R12 | 4.0 | Data-correction opportunity |
| R13 | 4.0 | Appeal of adverse decisions |
| O4 | 2.5 | Website-statement obligation |
| A1 | 2.5 | AutoApprove is a machine-based system |
| F9–F13 | 1.0 ×5 | Facts: Helix has not issued notices/correction/appeal |

**What the clean answer matched that the dirty one missed (14.0 pts):** the "substantial factor" framing —

| Teacher node | Weight | Meaning |
|---|--:|---|
| R3 | 4.0 | High-risk AI system definition |
| R4 | 4.0 | "Substantial factor" definition |
| A4 | 2.5 | Stage-2 substantial-factor analysis |
| O10 | 2.5 | FinLogic public use-case inventory |
| F7 | 1.0 | Morrison-memo fact |

**Net: 26.0 − 14.0 = 12.0 points to the dirty answer**, which is exactly 156.5 − 144.5. Add the identical −5.5 edge fix to each → **−16.5 vs −4.5**.

So the difference is not rule *quality*. The dirty answer, steered by the old library, enumerated the **consumer-facing duties** (notice → correction → appeal → website) — which happen to be **four separate high-weight rules** in the teacher's graph. The clean answer, steered by the rebuilt library, leaned on the **"substantial factor" framing** — only **two** high-weight rules. The 3B model wrote 5 rules one way and 3 the other, and which teacher rules those grazed swung the score 12 points.

---

## 5. The honest takeaway

The dirty-vs-clean comparison was **not** a controlled "removed one bad patch" experiment. It was **"we rebuilt everything, and the −16.5 didn't come back — it came back as −4.5."**

The −16.5 was **never a robust result**: it depended on the exact old cheat-sheet, and on which cluster of teacher rules the weak model happened to land on. Rebuild the library honestly and the big win evaporates — which is precisely what Phase 3 was designed to expose. The fabricated §20-875 patch was a **symptom** of the messy data; the score movement came from **rebuilding the patch library**, not from that single patch.

*Reproduce: retrieval reconstruction over `data/patches/patches.json`; component breakdown via `compute_discrepancies` (embedding alignment) on `data/outputs/graphs/H2_agent_llama3_2b_patched_{k3,clean_k3}.json` vs `H2_reference.json`.*
