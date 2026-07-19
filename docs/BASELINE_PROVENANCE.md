# Baseline provenance & the pinned generation (Phase 3, Task 1)

## The mismatch

The Phase-2 k-ablation reported Llama baselines (E2 = 110.5, M2 = 138.5) that did
**not** match the frozen snapshot values (E2 = 109.5, M2 = 132.0). Every GPT-5
baseline matched exactly.

## Root cause — cloud-vs-local extraction (not just a cache rename)

The two Llama baselines came from **different extraction stacks**, both at
temperature 0 (documented non-determinism is real):

| Artifact | Extraction stack | `model_name` recorded |
|---|---|---|
| Snapshot Llama graphs (Phase 2) | **cloud** — OpenRouter free route (Venice) | `meta-llama/llama-3.2-3b-instruct:free` |
| Ablation Llama baselines (`data/outputs/graphs_local/`) | **local** — HF transformers, unsloth mirror, MPS, fp16, greedy | `unsloth/Llama-3.2-3B-Instruct` |

GPT-5 matched because it was never re-extracted (cloud only, one generation). The
cache-namespace rename (`agent_qwen3_4b` → `agent_llama3_2b`) is a *contributing*
factor — it invalidated the Llama cache and is why a fresh (local) extraction was
run — but the substantive difference is cloud (Venice) vs local (unsloth/MPS)
serving of the same weights, which produce different greedy decodes.

The patched Llama runs were also **local**, so the local generation is the one
consistent with the patched graphs.

## Resolution — pin the local generation

1. Extracted E1/M1/H1 Llama **locally** (unsloth mirror, MPS) so all 6 Llama graphs
   are one generation (E2/M2/H2 already local from Phase 2).
2. Copied all 6 `graphs_local/*_agent_llama3_2b.json` into `data/outputs/graphs/`
   (replacing the cloud Llama graphs). Teacher (Claude) and GPT-5 graphs unchanged.
3. Regenerated **all** snapshot discrepancy JSONs + `discrepancy_summary.csv` for
   **both** backends (tfidf_v1, embedding_v1) from the pinned graphs, so snapshots,
   mining inputs, and ablation baselines are one consistent generation.

**Guard:** `scripts/run_k_ablation.py` now asserts, per cell, that the ablation
baseline L-GED equals the frozen snapshot value (`abs(diff) < 1e-6`), failing loudly
on any reintroduced drift. Verified: the guarded dirty run passes 6/6.

## Pinned generation (canonical going forward)

- **Teacher:** Claude Opus 4.6 (cloud, with statutes) — unchanged, out of scope.
- **GPT-5:** cloud (OpenAI) — unchanged.
- **Llama-3.2-3B:** **local** — HF transformers, `unsloth/Llama-3.2-3B-Instruct`
  (bit-identical to the gated Meta release), MPS, fp16, greedy/deterministic.

## Knock-on: ranking re-verification (see docs/ALIGNMENT_METHODS.md)

Regenerating the Llama snapshots changes the numbers behind the methods claim that
embedding recovers the GPT-5 < Llama capability ranking. After regeneration:

- **Embedding: 6/6 — HOLDS** (GPT-5 < Llama on every case). The headline is intact.
- **TF-IDF: 2/6 → 0/6.** The embedding-vs-TF-IDF contrast is now *cleaner* (TF-IDF
  inverts on all six), not weaker.

Flagged to Prof. Rao: the embedding 6/6 result survives the re-pin; the TF-IDF
comparison shifted from 2/6 to 0/6.
