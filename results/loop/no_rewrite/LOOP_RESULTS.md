# Iterative patch loop — run `no_rewrite`

Student: Llama-3.2-3B (local, greedy). 15 training cases, 15 held-out test cases. k = 3 patches per prompt. Rewrites: off.

L-GED is distance from the teacher's graph: lower is better.

## Result

- **Held-out (test) cases stop improving at round 0.** Mean test L-GED: 133.47 at round 0 → 133.47 at round 0 (+0.00).
- Training cases are best at round 0: 139.27 → 139.27 (+0.00).
- The loop ran 2 patched round(s) and stopped because neither the test nor the training curve was still improving.
- A gain counts only if it exceeds 1.335 L-GED points (1% of the round-0 test mean).
- Patches are mined only from this student's own gaps on the training cases, so the store differs from the Phase 2–4 store (which also used GPT-5's gaps).
- Retrieval: BM25 over patch keywords with function words removed from the case text, one patch per legal duty, and only patches from the case's own jurisdictions. Round 1 uses no loop evidence, so it is the single-pass method.

## Per round

| Round | Store | New | Rewritten | Train L-GED | Test L-GED | Test Δ vs r0 | Train R+O recovered | Test R+O recovered | Unparsed |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 0 | 219 | 0 | 139.27 | 133.47 | +0.00 | 19.5% | 18.1% | 0 |
| 1 | 219 | 22 | 0 | 142.97 | 132.97 | -0.50 | 16.6% | 16.8% | 0 |
| 2 | 241 | 6 | 0 | 141.93 | 134.17 | +0.70 | 15.6% | 15.3% | 0 |

## Test L-GED by tier

| Round | easy | hard | medium |
|--:|--:|--:|--:|
| 0 | 112.4 | 166.5 | 121.5 |
| 1 | 114.6 | 161.6 | 122.7 |
| 2 | 118.1 | 163.2 | 121.2 |

Columns: *Store* = patches available that round; *New* = patches mined from that round's training graphs; *Rewritten* = failing patches rewritten after that round; *R+O recovered* = share of the teacher's Rules and Obligations present in the student's graph.

## Caveats

- Teacher graphs were extracted from statute summaries known to contain errors; 12 teacher rule citation(s) across these cases are classified as fabricated (see `results/loop/teacher_contamination.csv`).
- 24 of the 30 cases are synthetic and have not been reviewed by a legal expert.
- One student and a fixed budget of k patches: the plateau round is specific to this model and this k.
