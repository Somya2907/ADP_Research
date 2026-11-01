# C1 — choosing checklist items without looking at the answer

Items: 222 missed teacher Rules/Obligations from 15 training cases, grouped into 50 clusters (same kind of node + same statute section). Test cases: 15; their mean missing R/O weight is 72.1.

An item is **useful** if it is the same kind of node as a missing teacher node in the test case, cites the same section and has a similar label (embedding similarity ≥ 0.5). **Fillable weight** is the L-GED those useful items would remove if the student wrote them correctly.

| Method | k | Useful items per case | Precision | Fillable L-GED per case | Useful (section match only) |
|---|--:|--:|--:|--:|--:|
| bm25 | 3 | 1.1 | 36% | 3.4 | 1.1 |
| support | 3 | 1.7 | 58% | 6.9 | 1.9 |
| similarity | 3 | 1.7 | 58% | 4.9 | 1.7 |
| combined | 3 | 1.9 | 62% | 6.6 | 1.9 |
| store_best | 3 | 2.4 | 100% | 9.5 | 2.4 |
| bm25 | 5 | 1.5 | 31% | 4.8 | 1.5 |
| support | 5 | 3.1 | 61% | 11.6 | 3.3 |
| similarity | 5 | 2.6 | 52% | 7.9 | 2.6 |
| combined | 5 | 3.3 | 65% | 12.1 | 3.4 |
| store_best | 5 | 3.9 | 100% | 15.1 | 3.9 |
| bm25 | 10 | 3.3 | 33% | 10.4 | 3.3 |
| support | 10 | 4.9 | 49% | 17.8 | 5.1 |
| similarity | 10 | 5.0 | 50% | 16.4 | 5.1 |
| combined | 10 | 5.2 | 52% | 18.5 | 5.5 |
| store_best | 10 | 6.7 | 100% | 24.1 | 6.7 |

## Tier transfer (k=10, section+label match)

Fillable L-GED per test case when items come only from one tier's training cases.

| Items from ↓ / test tier → | easy | medium | hard |
|---|--:|--:|--:|
| easy | 14.7 (best 16.8) | 21.3 (best 23.8) | 14.2 (best 21.8) |
| medium | 12.6 (best 12.6) | 20.2 (best 20.2) | 14.4 (best 20.6) |
| hard | 14.4 (best 18.6) | 27.0 (best 28.9) | 18.5 (best 23.1) |
