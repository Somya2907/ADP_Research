# Checklist patches, k=10 — confirmation on all 15 test cases

Method fixed before this run: checklist items mined from the 15 training cases only,
ranked by similarity to the case + how often training students missed them, 10 items,
checklist wording, loop guard on. Llama-3.2-3B, greedy. Change = L-GED with the
checklist minus L-GED with no notes, same case (negative = closer to the teacher).

| Cases | n | Mean change (95% CI) | % of baseline | Improved | Paired t | Wilcoxon |
|---|--:|--:|--:|--:|--:|--:|
| All test cases | 15 | −14.6 (−19.8 to −9.4) | −11% | 12/15 | p = 0.0001 | p = 0.002 |
| Never used for tuning | 9 | −15.8 (−23.6 to −8.1) | −12% | 7/9 | p = 0.006 | p = 0.02 |
| Easy | 5 | −17.8 (−27.7 to −7.9) | −16% | 4/5 | p = 0.04 | p = 0.13 |
| Medium | 5 | −15.1 (−17.0 to −12.7) | −12% | 5/5 | p = 0.0003 | p = 0.06 |
| Hard | 5 | −11.0 (−21.5 to −0.6) | −7% | 3/5 | p = 0.14 | p = 0.31 |

Against the Phase 5 method (BM25 patches, k=3, loop round 1) on the same 15 cases:
Phase 5 averaged −0.5 (6/15 improved); the checklist is 14.1 points better
(paired t p = 0.001, Wilcoxon p = 0.008).

Per case: E2 −15.5, E7 −30.0, E8 −13.0, E9 −31.5, E10 +1.0, M2 −16.0, M7 −16.0,
M8 −15.0, M9 −10.5, M10 −18.0, H2 −22.5, H7 −5.0, H8 −28.5, H9 +0.5, H10 +0.5.

Rules per answer 3.2 → 8.6; nodes 20 → 26. Of the 78 items that matched a real gap,
the student wrote 49 (63%). The loop guard cut 2 answers (E2, E8), both of which still
improved. No answer failed to parse.

Caveats: one student model; one teacher (with known fabricated citations); 15 synthetic
cases; the placebo control was run on 6 of the 15 only; 6 of the 15 cases were used
while designing the method (the 9 untuned cases give the same result).
