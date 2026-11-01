# Stage A — what the existing outputs say (run `full`)

## Training cases (n=15), mean round-0 L-GED 139.3

| Where the L-GED comes from | Mean | Share |
|---|--:|--:|
| Missing Rules + Obligations (what patches target) | 79.7 | 57% |
| Missing Facts, Issues, Applications, Conclusions | 53.1 | 38% |
| Hallucinated nodes + edge differences | 6.4 | 5% |

| Best case: the student adds its heaviest missing R/O nodes | L-GED drop | Share |
|---|--:|--:|
| 3 nodes (k=3) | −12.0 | 9% |
| 10 nodes | −39.4 | 28% |
| all of them | −79.7 | 57% |

Size: teacher 72 nodes / 18 rules; student 20 nodes / 3.5 rules; 23 missing R/O per case.

## Test cases (n=15), mean round-0 L-GED 133.5

| Where the L-GED comes from | Mean | Share |
|---|--:|--:|
| Missing Rules + Obligations (what patches target) | 73.7 | 55% |
| Missing Facts, Issues, Applications, Conclusions | 51.8 | 39% |
| Hallucinated nodes + edge differences | 8.0 | 6% |

| Best case: the student adds its heaviest missing R/O nodes | L-GED drop | Share |
|---|--:|--:|
| 3 nodes (k=3) | −12.0 | 9% |
| 10 nodes | −39.4 | 30% |
| all of them | −73.7 | 55% |

Size: teacher 69 nodes / 16 rules; student 20 nodes / 3.2 rules; 22 missing R/O per case.

## Teacher errors

12 of 30 teacher graphs cite a section the statute index marks as fabricated (12 rules). Removing them (and the obligations and edges hanging off them) changes the round-0 L-GED of those cases by -4.8 on average (range -6.5 to -4.0).
The list for the legal reviewer is in `teacher_suspect_nodes.csv`.

## Retrieval audit (round-1 injections)

| Question | Train | Test |
|---|--:|--:|
| Patch is in the case's jurisdiction | 45/45 (100%) | 45/45 (100%) |
| Teacher cites the same section somewhere in the case | 17/45 (38%) | 17/45 (38%) |
| Teacher uses this exact authority (what efficacy is scored on) | 12/45 (27%) | 11/45 (24%) |
| …and the student was missing it (useful patch) | 12/45 (27%) | 8/45 (18%) |
| Student cites the injected section | 16/45 (36%) | 17/45 (38%) |
| Gap closed, of the useful patches | 4/12 | 2/8 |

90 injections in total. Precision@k = share that were useful patches.

## Same section, different spelling

The final store (store_round_2) holds 241 patches. Merging citations that name the same section in a different format leaves 147 (39% were duplicates); they cover 21 distinct sections.
