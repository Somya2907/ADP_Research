# Phase 2 (patch injection) — results

Δ = patched − baseline L-GED (**negative = patches help**); n=1 sample per cell (temperature-0; see variance below). Baselines are the Task-1 pinned generation.

## Store: `clean`

| Student | k | E2 Δ (pct) | M2 Δ (pct) | H2 Δ (pct) | mean Δ |
|---|---|---|---|---|---|
| GPT-5 (frontier) | 1 | -10.0 (-11%) | +16.5 (+17%) | +13.0 (+10%) | **+6.50** |
| GPT-5 (frontier) | 3 | +7.0 (+8%) | +6.5 (+7%) | +5.0 (+4%) | **+6.17** |
| GPT-5 (frontier) | 5 | +0.0 (+0%) | +4.0 (+4%) | -22.5 (-18%) | **-6.17** |
| Llama-3B (weak) | 1 | +10.5 (+10%) | -4.0 (-3%) | -11.0 (-7%) | **-1.50** |
| Llama-3B (weak) | 3 | +10.5 (+10%) | +6.0 (+4%) | -4.5 (-3%) | **+4.00** |
| Llama-3B (weak) | 5 | +2.0 (+2%) | +4.0 (+3%) | -11.5 (-7%) | **-1.83** |

## Store: `clean_jfilter`

| Student | k | E2 Δ (pct) | M2 Δ (pct) | H2 Δ (pct) | mean Δ |
|---|---|---|---|---|---|
| GPT-5 (frontier) | 1 | -10.0 (-11%) | +16.5 (+17%) | +13.0 (+10%) | **+6.50** |
| GPT-5 (frontier) | 3 | +2.5 (+3%) | +6.5 (+7%) | +5.0 (+4%) | **+4.67** |
| GPT-5 (frontier) | 5 | +2.5 (+3%) | +4.0 (+4%) | -22.5 (-18%) | **-5.33** |
| Llama-3B (weak) | 1 | +10.5 (+10%) | -4.0 (-3%) | -11.0 (-7%) | **-1.50** |
| Llama-3B (weak) | 3 | +12.0 (+11%) | +6.0 (+4%) | -4.5 (-3%) | **+4.50** |
| Llama-3B (weak) | 5 | +12.0 (+11%) | +4.0 (+3%) | -11.5 (-7%) | **+1.50** |

## Reading the result

- **Weak student (Llama-3B):** best at k=5 (mean Δ -1.83). But means hide sign flips — check the per-case columns above; individual cases can be positive even at the best k.
- **Frontier student (GPT-5): patches DEGRADE it** at every k (means all positive; worst k=1 mean +6.50). worst single cell M2 k1: +16.5 This is harm, not neutrality.

## Variance (Task 5)

- `gpt5/M2/k3`: 120.0, 119.5, 110.5 (range **9.5**)
- `llama3_2b/H2/k3`: 158.0, 158.0, 158.0 (range **0.0**)

Plus two zero-cost baseline resamples from the cloud→local re-pin (Llama E2 +1.0, M2 +6.5). Interpretation: effects larger than the observed run-to-run range are credible; a +6.5 resample means single-digit means should not be over-read.

## Clean vs dirty (contamination comparison)

`k_ablation_dirty.csv` is the pre-quarantine store (all 85 patches incl. the fabricated §20-875). Comparing mean Δ at k=3:

| Student | dirty k3 | clean k3 |
|---|---|---|
| GPT-5 (frontier) | +5.83 | +6.17 |
| Llama-3B (weak) | -4.17 | +4.00 |

The delta between them is how much of the apparent Phase-2 effect was fabrication-driven.

## Optional analyses

- **S1 (patch interference):** GPT-5's per-cell harm does **not** track off-jurisdiction patch share — the largest swings (M2/k1 +16.5, H2/k5 −22.5) occur at 0% off-jurisdiction, and the jurisdiction pre-filter (`clean_jfilter`) barely moves GPT-5. So "retrieval precision matters more for the stronger student" is not supported here; the swings are within-jurisdiction edge disruption (see `DELTA_AUDIT.md`).
- **S3 (contamination sensitivity):** each contaminated case (E1/E2/H1) has one fabricated teacher rule (§20-875); excluding it drops L-GED by a uniform **−4.0** for *both* students. The fabrication adds ~4 spurious points per case but is symmetric, so it does not bias the GPT-5-vs-Llama comparison.
- **S2 (family ablation): deferred** — needs fresh injections, and with the clean-store effects already inside the noise band it would compare two small noisy sub-effects.

## Bottom line

The metric is sound (embedding recovers the GPT-5 < Llama ranking 6/6; see `docs/ALIGNMENT_METHODS.md`). But on the clean, verified-only store the patch-injection effect is **within run-to-run noise** (GPT-5 range 9.5 > its effect sizes; Llama deterministic but tiny and sign-flipping). Phase 2's "patches help the weak student at k=3" (−4.17) does **not survive** quarantine (clean k=3 = +4.00; the H2 −16.5 collapses to −4.5, edge-driven not rule-recovery). The Phase-2 headline was substantially contamination + noise — which Phase 3 was designed to detect.
