# Checklist loop — `checklist_t4` (rounds 0–3)

Llama-3.2-3B student, 15 training + 15 test cases, k=10 checklist items per prompt. Each round after the first re-ranks items by how often they were written on the training cases, adds newly missed items and swaps the wording of items that keep failing. Test cases are scored only. Scores re-computed from the saved answers with the current parser.

| Round | Train L-GED | Test L-GED | Test change vs round 0 (95% CI) | Test cases improved | Wilcoxon p | Test R/O recovered | Rules per answer (test) | Unparsed (train/test) |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0 | 141.60 | 133.63 | — | — | — | 17.8% | 3.1 | 0/0 |
| 1 | 129.97 | 115.17 | -18.5 (-22.6 to -14.2) | 15/15 | 0.0007 | 40.2% | 8.6 | 0/0 |
| 2 | 131.37 | 122.27 | -11.4 (-16.0 to -6.6) | 14/15 | 0.0018 | 31.4% | 6.7 | 1/0 |
| 3 | 126.23 | 118.43 | -15.2 (-20.7 to -9.2) | 14/15 | 0.0029 | 38.4% | 8.8 | 0/0 |

## By tier (test mean L-GED)

| Round | Easy | Medium | Hard |
|--:|--:|--:|--:|
| 0 | 114.2 | 123.5 | 163.2 |
| 1 | 95.7 | 102.7 | 147.1 |
| 2 | 101.3 | 113.9 | 151.6 |
| 3 | 94.6 | 111.8 | 148.9 |

## When does learning stop?

- Best test round: **1** (mean 115.17; ε = 1.34, 1% of the round-0 mean).
- Round 2 vs round 1 on the test cases: +7.1 (Wilcoxon p = 0.017).
- Round 3 vs round 1 on the test cases: +3.3 (Wilcoxon p = 0.256).
- Training cases: 141.6 → 130.0 → 131.4 → 126.2.
