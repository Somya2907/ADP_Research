# Patch diagnostics — 6 test cases (E2, E8, M2, M9, H2, H10)

Each number compares the same case with and without the notes; negative L-GED change = closer to the teacher. **Upper bound** arms are built from the test case's own teacher graph, so they show the most patches could do and are not a method result. **Method** arms use only the training cases.

All answers went through the loop guard: an answer that started repeating itself is scored on what it wrote before the loop ("loops cut").

| Arm | Kind | Cases | Notes | Loops cut | L-GED change (95% CI) | % of baseline | Targeted nodes recovered | Rules per answer | Nodes per answer |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Placebo: 3 irrelevant real patches | control | 6 | 3 | 0 | +2.8 (-4.4 to +8.8) | +2% | – | 3.5 → 3.0 | 16 → 18 |
| Phase 5 method: BM25 patches, k=3 (loop round 1) | method | 6 | 3 | 0 | -4.8 (-13.2 to +3.2) | -4% | – | – | – |
| **Checklist from training cases, k=5** | method | 6 | 5 | 1 | -3.2 (-12.5 to +9.8) | -2% | 11/19 (58%) | 3.5 → 5.2 | 16 → 18 |
| **Checklist from training cases, k=10** | method | 6 | 10 | 2 | -12.8 (-17.9 to -6.8) | -10% | 22/32 (69%) | 3.5 → 7.7 | 16 → 26 |
| Oracle, k=3, advice wording | upper bound | 6 | 3 | 0 | -1.4 (-6.7 to +4.7) | -1% | 8/18 (44%) | 3.5 → 3.3 | 16 → 20 |
| Oracle, k=10, advice wording | upper bound | 6 | 10 | 1 | -5.3 (-19.6 to +7.2) | -4% | 27/60 (45%) | 3.5 → 5.3 | 16 → 23 |
| Oracle, all missing R/O, advice wording | upper bound | 4 | 16 | 1 | +9.1 (-8.4 to +23.8) | +8% | 19/65 (29%) | 3.5 → 9.2 | 14 → 22 |
| Oracle, k=10, checklist wording | upper bound | 6 | 10 | 1 | -9.0 (-23.8 to +12.4) | -7% | 43/60 (72%) | 3.5 → 7.5 | 16 → 25 |
| Oracle, k=10, text written by Claude | upper bound | 6 | 10 | 0 | -3.8 (-13.5 to +4.8) | -3% | 22/60 (37%) | 3.5 → 4.0 | 16 → 20 |

## Per case (L-GED change)

| Case | Baseline | placebo | phase5_k3 | checklist_k5 | checklist_k10 | oracle_k3 | oracle_k10 | oracle_all | directive_k10 | llm_k10 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| E2 | 110.5 | +12.0 | -5.5 | -15.0 (loop cut) | -15.5 (loop cut) | -1.5 | -7.0 (loop cut) | +29.0 (loop cut) | -13.5 | +11.0 |
| E8 | 99.5 | +11.0 | +11.5 | +1.0 | -13.0 (loop cut) | +11.5 | +16.0 | +16.0 | -8.5 | -4.0 |
| M2 | 138.5 | +0.0 | +0.0 | -8.0 | -16.0 | -8.0 | -14.0 | -16.5 | -29.5 | +6.5 |
| M9 | 126.5 | -13.0 | -4.0 | +27.0 | -10.5 | -5.5 | +6.5 | +8.0 | -25.0 | -7.0 |
| H2 | 162.5 | +1.5 | -9.0 | -14.5 | -22.5 | -8.5 | -37.5 |  | -19.5 | -25.5 |
| H10 | 166.5 | +5.0 | -22.0 | -9.5 | +0.5 | +3.5 | +4.0 |  | +42.0 (loop cut) | -4.0 |

## Reading

- **Noise floor.** Irrelevant notes: +2.8 (-4.4 to +8.8).
- **Phase 5 method: BM25 patches, k=3 (loop round 1)**: -4.8 (-13.2 to +3.2); not distinguishable from placebo.
- **Checklist from training cases, k=5**: -3.2 (-12.5 to +9.8), 11 of the 19 useful items written into the answer; not distinguishable from placebo.
- **Checklist from training cases, k=10**: -12.8 (-17.9 to -6.8), 22 of the 32 useful items written into the answer; beats the placebo.
- **Wording (upper bound).** Same 10 nodes as a checklist: -9.0, 72% recovered; as advice: -5.3, 45% recovered.
- **LLM-written patches (upper bound).** Claude's text: -3.8, 37% recovered, vs the template's -5.3, 45%. Claude's notes are about twice as long.
