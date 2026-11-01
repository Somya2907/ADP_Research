# Iterative patch loop — run `full`

Student: Llama-3.2-3B (local, greedy). 15 training cases, 15 held-out test cases. k = 3 patches per prompt. Rewrites: on.

L-GED is distance from the teacher's graph: lower is better.

## Result

- **Held-out (test) cases stop improving at round 0.** Mean test L-GED: 133.47 at round 0 → 133.47 at round 0 (+0.00).
- Training cases are best at round 0: 139.27 → 139.27 (+0.00).
- The loop ran 2 patched round(s) and stopped because neither the test nor the training curve was still improving.
- A gain counts only if it exceeds 1.335 L-GED points (1% of the round-0 test mean).
- Patches are mined only from this student's own gaps on the training cases, so the store differs from the Phase 2–4 store (which also used GPT-5's gaps).

## Per round

| Round | Store | New | Rewritten | Train L-GED | Test L-GED | Test Δ vs r0 | Train R+O recovered | Test R+O recovered | Unparsed |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 0 | 219 | 0 | 139.27 | 133.47 | +0.00 | 19.5% | 18.1% | 0 |
| 1 | 219 | 21 | 5 | 149.5 | 133.8 | +0.33 | 17.2% | 16.3% | 0 |
| 2 | 240 | 8 | 4 | 143.5 | 135.4 | +1.93 | 17.2% | 15.3% | 0 |

## Test L-GED by tier

| Round | easy | hard | medium |
|--:|--:|--:|--:|
| 0 | 112.4 | 166.5 | 121.5 |
| 1 | 111.4 | 167.5 | 122.5 |
| 2 | 115.6 | 166.5 | 124.1 |

Columns: *Store* = patches available that round; *New* = patches mined from that round's training graphs; *Rewritten* = failing patches rewritten after that round; *R+O recovered* = share of the teacher's Rules and Obligations present in the student's graph.

## Caveats

- Teacher graphs were extracted from statute summaries known to contain errors; 12 teacher rule citation(s) across these cases are classified as fabricated (see `results/loop/teacher_contamination.csv`).
- 24 of the 30 cases are synthetic and have not been reviewed by a legal expert.
- One student and a fixed budget of k patches: the plateau round is specific to this model and this k.
