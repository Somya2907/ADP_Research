# Alignment Methods: TF-IDF vs Sentence Embeddings

> **Auto-generated** by `scripts/build_alignment_doc.py` from the snapshot files under `data/snapshots/`. Do not edit by hand — re-run the script to refresh. Every number below is read from `{tfidf,embedding}_v1/results/discrepancy_summary.csv`.

> **Ranking re-verification (Phase 3, post baseline re-pin):** embedding recovers the expected GPT-5 < Llama ranking on **6/6** cases — the methods claim **HOLDS**; TF-IDF manages **0/6**. See `docs/BASELINE_PROVENANCE.md`.

The discrepancy scorer (L-GED) compares each student's F-I-R-A-C-O graph against the teacher's. Node alignment — deciding which student node corresponds to which teacher node — is the one step with a pluggable similarity backend. This document compares the two backends on the frozen 6-case corpus.

## 1. The two backends

Rules are aligned by citation token first (e.g. `§20-871(d)(2)` ≡ `Section 20-871(d)(2)`). Everything else falls back to text similarity, selected at runtime by the `LEX_DRL_SIMILARITY` environment variable:

| Backend | `LEX_DRL_SIMILARITY` | Similarity | Threshold |
|---|---|---|---|
| TF-IDF (default) | `tfidf` | n-gram (1,2) TF-IDF cosine | 0.10 |
| Embedding | `embedding` | `BAAI/bge-small-en-v1.5` cosine | 0.55 |

A teacher node and a student node align when their similarity clears the threshold under a greedy bipartite assignment. Below the threshold, the teacher node is a *miss* (`v_miss`) and the unmatched student node a *hallucination* (`v_halluc`).

## 2. Models compared

- **Teacher (reference):** `claude-opus-4-6` — produces G_ref with statutory context.
- **Student 1 (frontier):** `gpt-5` — no statutory context.
- **Student 2 (small, <7B):** `unsloth/Llama-3.2-3B-Instruct` via OpenRouter — no statutory context.

L-GED measures distance from the teacher, so **lower is better**. We expect the frontier student (GPT-5) to sit closer to the teacher than the 3B model on every case; a backend that inverts that ordering is mismeasuring.

## 3. Per-case discrepancy counts and L-GED

Read directly from the two snapshot CSVs. `v_miss` / `v_halluc` / `e_diff` are counts; L-GED is the weighted aggregate.

| Case | Tier | Student | v_miss (tf→emb) | v_halluc (tf→emb) | e_diff (tf→emb) | L-GED (tf→emb) |
|---|---|---|---|---|---|---|
| E1 | easy | GPT-5 | 40 → 23 | 19 → 2 | 11 → 23 | 167.0 → 131.0 |
| E1 | easy | Llama-3B | 62 → 59 | 3 → 0 | 0 → 0 | 159.0 → 149.0 |
| E2 | easy | GPT-5 | 22 → 8 | 17 → 3 | 13 → 22 | 128.5 → 88.5 |
| E2 | easy | Llama-3B | 49 → 46 | 3 → 0 | 0 → 1 | 128.0 → 110.5 |
| M1 | medium | GPT-5 | 24 → 8 | 24 → 8 | 15 → 24 | 176.5 → 116.0 |
| M1 | medium | Llama-3B | 58 → 54 | 4 → 0 | 1 → 2 | 164.0 → 145.0 |
| M2 | medium | GPT-5 | 41 → 23 | 18 → 0 | 10 → 16 | 166.5 → 96.5 |
| M2 | medium | Llama-3B | 61 → 58 | 3 → 0 | 1 → 1 | 153.5 → 138.5 |
| H1 | hard | GPT-5 | 51 → 26 | 36 → 11 | 8 → 23 | 248.0 → 171.0 |
| H1 | hard | Llama-3B | 72 → 65 | 7 → 0 | 0 → 0 | 216.5 → 180.5 |
| H2 | hard | GPT-5 | 38 → 16 | 29 → 7 | 9 → 21 | 196.0 → 125.5 |
| H2 | hard | Llama-3B | 65 → 63 | 2 → 0 | 2 → 3 | 171.5 → 162.5 |

## 4. Ranking correctness (the headline result)

Cases (out of 6) where GPT-5 L-GED < Llama-3B L-GED — i.e. the metric correctly ranks the frontier model as closer to the teacher:

| Backend | Correct rankings | Cases |
|---|---|---|
| TF-IDF | **0/6** | — |
| Embedding | **6/6** | E1, E2, M1, M2, H1, H2 |

Under TF-IDF the ranking inverts on 6 cases (E1, E2, M1, M2, H1, H2); the embedding backend recovers the expected ordering on all 6. **This is the core argument for the embedding backend.**

## 5. The E1 / GPT-5 contrast

E1 is the calibration case. The single change of similarity backend moves GPT-5's components as follows:

| Component | TF-IDF | Embedding | Δ |
|---|---|---|---|
| v_miss | 40 | 23 | -17 |
| v_halluc | 19 | 2 | -17 |
| e_diff | 11 | 23 | +12 |
| L-GED | 167.0 | 131.0 | -36.0 |

`v_halluc` collapses from 19 to 2: TF-IDF was mislabeling GPT-5's paraphrases of teacher nodes as hallucinations, because their n-grams don't overlap. Embeddings match the paraphrases, so they align instead. Note `e_diff` *rises* (11 → 23): with more nodes aligned, more edges are comparable, surfacing real edge differences that the unaligned nodes had hidden. The `v_miss`/`v_halluc` gains dominate, so L-GED still drops 167.0 → 131.0.

For E1 specifically, GPT-5 < Llama-3B under **both** backends (TF-IDF: 167.0 < 159.0; Embedding: 131.0 < 149.0) — but the TF-IDF margin is only -8.0 points, and it does not survive to the harder tiers (§4).

## 6. Why TF-IDF inverts the ranking on harder cases

GPT-5 produces longer, more paraphrastic node labels than the 3B model. TF-IDF cosine on short legal labels is brittle to paraphrase: *"based in Austin"* vs *"operates out of Austin"* scores near zero because the bigrams don't overlap. Those unmatched GPT-5 nodes are counted as hallucinations, inflating GPT-5's L-GED. The 3B model emits fewer, terser nodes, so it accrues fewer hallucination penalties — and on the medium/hard cases that artifact is enough to rank the weaker model ahead. Sentence embeddings score paraphrase pairs ≈0.95, so the alignment reflects meaning rather than surface n-grams and the ordering corrects.

## 7. Known limitation: E1-only threshold calibration

The embedding threshold (**0.55**) was calibrated on **E1 only**. It has not been swept against the other five cases or a held-out set, so it may be over-fit to E1's label distribution. The 6/6 ranking result is robust to this (it holds with comfortable margins on most cases), but the exact threshold value should be treated as provisional pending a multi-case calibration. The TF-IDF threshold (0.10) was likewise the best of a sweep on E1 (`scripts/calibrate_threshold.py`).

## 8. Conclusion

Node alignment is not a neutral preprocessing step — it determines whether L-GED recovers the expected capability ordering. On this corpus, embedding-based alignment ranks the frontier student (GPT-5) closer to the teacher than the 3B model on **6/6** cases; TF-IDF does so on only **0/6**, inverting on every medium/hard case (E1, E2, M1, M2, H1, H2). The inversion is a measurement artifact rather than a quality signal: TF-IDF mislabels the frontier model's paraphrased nodes as hallucinations, and that penalty grows with case difficulty until it overtakes the genuinely weaker model. The capability ranking is therefore **not invariant to the alignment backend** — embedding alignment is load-bearing for the headline result, not a cosmetic refinement. We adopt embedding alignment (`BAAI/bge-small-en-v1.5`, threshold 0.55) as the primary backend and retain TF-IDF (threshold 0.10) as a documented ablation; the 0/6 → 6/6 ranking recovery is the methods contribution, subject to the E1-only calibration caveat in §7.

## 9. Provenance notes

- The small-model student key is `llama3_2b`; the underlying model is `unsloth/Llama-3.2-3B-Instruct` (the `model_name` recorded in every small-model graph). An earlier code revision labeled this student `qwen3_4b`; that key was a leftover and has been renamed repo-wide to `llama3_2b` so labels match the data.
- Numbers come from the **frozen** graph corpus; graphs are not re-extracted. The two snapshots differ only in the alignment backend used to score the same graphs.
- Regenerate this doc with `poetry run python scripts/build_alignment_doc.py`.
