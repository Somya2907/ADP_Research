<!--
Copy-paste slide content for the meeting deck — reasoning traces behind the L-GED scores.
5 slides. Each block = one slide: TITLE, a one-line takeaway, a table, and bullets.
Source: data/outputs/graphs/*.json under embedding alignment (regenerate via scripts/build_traces_doc.py).
Longer prose version: docs/REASONING_TRACES.md.
-->

# Reasoning-trace slides (paste into the deck)

Each analysis is a graph: **F**acts → **I**ssues → **R**ules → **A**pplication → **C**onclusion → **O**bligations.
The teacher (Claude) writes the reference; each student attempts the **same** case; L-GED counts what the student **missed / invented / mis-connected** (lower = closer to teacher).

---

## Slide 1 — The weak student *collapses* the analysis

**Title:** What the students actually produce (graph size)

**Takeaway (one line):** The weak model doesn't reason wrong — it barely reasons at all. That gap *is* the L-GED.

| Case | Teacher (Claude) | GPT-5 (frontier) | Llama-3B (weak) |
|---|---|---|---|
| **E2** (easy, NYC) | 60 nodes — 9 issues, 12 steps, 8 obligations | 55 nodes — 8 / 12 / 9 | **14 nodes — 1 / 1 / 1** |
| **H2** (hard, multi-state) | 77 nodes — 7 issues, 16 steps, 10 obligations | 68 nodes — 5 / 14 / 14 | **14 nodes — 1 / 1 / 1** |

- Llama collapses every case to **1 issue, 1 application step, 1 conclusion, 1 obligation**.
- GPT-5 stays within ~10–20% of the teacher's size on both cases.
- Format for each cell above: *total nodes — issues / application-steps / obligations*.

---

## Slide 2 — Case E2 (easy): the same case, three analyses

**Title:** NYC hospital promotion tool — LL 144 bias-audit compliance

**Takeaway:** GPT-5 tracks the teacher's reasoning (rephrased); Llama frames one issue and wanders off-jurisdiction.

| | Teacher | GPT-5 | Llama-3B |
|---|---|---|---|
| **Issues** | 9 (AEDT? audit timely? auditor independent? notice content? notice timing? …) | 8 (same spine) | **1** ("does it comply with LL 144?") |
| **Rules** | 14 — all NYC LL 144 / DCWP | 10 — NYC + CO + TX + NIST | 4 — NYC §20-871, **NIST, Colorado, Texas** |
| **Application** | 12 steps | 12 steps | **1 step** |
| **Obligations** | 8 (new audit, revise notice, 10-day timing, disclosure…) | 9 (closely track teacher) | **1** (generic "provide notice") |
| **L-GED** | — (reference) | 88.5 | **110.5** |

- **Llama's failure = omission, not error:** L-GED = 46 *missed* teacher nodes, **0 hallucinations**.
- On an **NYC-only** fact pattern, Llama cites **Colorado and Texas** statutes — the retrieval-precision problem patches were meant to fix.

---

## Slide 3 — Case H2 (hard): the gap widens

**Title:** Multi-jurisdiction lending model — Colorado AI Act high-risk analysis

**Takeaway:** On the hard case the teacher builds 77 nodes; Llama still writes 14 — and grounds its lead rule in the *wrong state's* law.

| | Teacher | GPT-5 | Llama-3B |
|---|---|---|---|
| **Issues** | 7 (Stage-1 high-risk? Stage-2? deployer vs developer? memo conflict? …) | 5 (same spine) | **1** |
| **Rules** | 20 — Colorado AIA subsections | 10 — CO AIA (section-level) | 3 — **NYC LL 144**, CO §6-1-1703, NIST |
| **Application** | 16 steps | 14 steps | **1 step** |
| **Conclusions** | 6 | 4 | 1 |
| **L-GED** | — (reference) | 125.5 | **162.5** |

- Llama's **63 missed nodes** = the whole analysis: the deployer/developer distinction, the two-stage high-risk test, the impact-assessment and consumer-notice obligations.
- Its lead rule cites **NYC Local Law 144 on a Colorado case** — right idea, wrong statute.
- GPT-5's "errors" are mostly **sub-section drift** (cites §6-1-1702 where the teacher pinpoints §6-1-1701(7)) — the proposition is correct.

---

## Slide 4 — The "ground truth" is sometimes wrong (visible in a trace)

**Title:** You can see the data contamination in a single line

**Takeaway:** In E2, L-GED penalizes GPT-5 for being *more correct than the teacher*.

| Node | Citation | Reality |
|---|---|---|
| Teacher R7 (penalties) | `§20-875` | **fabricated** — no such section exists in LL 144 |
| GPT-5 R7 (penalties) | `§20-872` | **the real** enforcement/penalties section |
| L-GED verdict | GPT-5 "misgrounded" | ✗ scored against the correct answer |

- Root cause: the teacher was fed **AI-summarized statutes** that invented `§20-875`; it appears in the teacher graphs for E1/E2/H1.
- This is the **Phase-3 finding made concrete** — why we quarantined the fabricated patches and flagged teacher re-extraction.
- Reassurance: the metric itself is sound (embedding recovers the GPT-5 < Llama ranking **6 / 6**); the issue is the *reference data*, not the scoring.

---

## Slide 5 — What a *patch* actually does

**Title:** The intervention nudges grounding, not coverage (Llama · H2 · k=3)

**Takeaway:** Patches fix *what little the model writes* — they can't make a 3B model write the rest.

| | No-patch baseline | + top-3 verified patches |
|---|---|---|
| Graph size | 14 nodes | 13 nodes |
| **L-GED** | 162.5 | **158.0**  (−4.5) |
| Lead rule | `NYC LL 144 §20-871` ✗ wrong | `CO AIA §6-1-1703(2)(a)` ✓ **corrected** |
| Issues framed | 1 | **still 1** |
| Missed nodes | 63 | 64 (unchanged) |

- The −4.5 gain is **corrected grounding + one trimmed edge**, *not* recovered coverage.
- The student still frames **1 of 7 issues** — the ceiling of in-context prompting for a small model.
- This motivates the next step: **learn from the teacher** (use L-GED as a training reward), not just prompt. → see `IMPROVEMENT_DIRECTIONS.md`.

---

*Full prose traces (more detail per node): `docs/REASONING_TRACES.md`. Regenerate all numbers: `LEX_DRL_SIMILARITY=embedding poetry run python scripts/build_traces_doc.py`.*
