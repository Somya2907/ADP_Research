<!--
Cross-case L-GED comparison. Two DIFFERENT measurements kept separate on purpose:
  (1) student separation = Llama - GPT5  (which student is closer to the teacher)
  (2) patch effect       = patched - baseline  (did a patch help the student learn)
Canonical combined baselines (embedding_combined_v1) + results/k_ablation_combined_clean.csv.
-->

# Cross-case comparison — L-GED across the six cases

Two numbers are easy to confuse because both are subtractions. They mean opposite things, so we keep them in **separate tables**.

- **Student separation** = `Llama L-GED − GPT-5 L-GED`. Which student is closer to the teacher. **Positive is good** (GPT-5 closer). *No patches involved.*
- **Patch effect** = `patched L-GED − baseline L-GED`. Did a patch move the student toward the teacher. **Negative is good** (learned).

---

## Table 1 — Student separation (baseline, no patches)

How far each student sits from the teacher, per case. Raw L-GED grows with case size, so a **per-node** column is included for a size-fair comparison.

| Case | Tier | Teacher size | GPT-5 | Llama | Separation (Llama−GPT5) | GPT-5 /node | Llama /node |
|---|---|--:|--:|--:|--:|--:|--:|
| E1 | Easy | 71 | 135.0 | 149.0 | +14.0 | 1.90 | 2.10 |
| E2 | Easy | 60 | 88.5 | 110.5 | +22.0 | 1.48 | 1.84 |
| M1 | Medium | 73 | 120.0 | 141.0 | +21.0 | 1.64 | 1.93 |
| M2 | Medium | 70 | 108.5 | 138.5 | +30.0 | 1.55 | 1.98 |
| H1 | Hard | 88 | 167.0 | 184.5 | +17.5 | 1.90 | 2.10 |
| H2 | Hard | 77 | 117.5 | 162.5 | +45.0 | 1.53 | 2.11 |
| **mean** | | 73 | **122.8** | **147.7** | **+24.9** | **1.67** | **2.01** |

- **GPT-5 is closer to the teacher on all 6 cases** (separation positive 6/6). Positive is the *correct, desired* sign here — a negative would mean the weak model beat the frontier model.
- **Raw L-GED is dominated by case size** (correlation with teacher size: GPT-5 0.91, Llama 0.98). Compare *within a case* or *per node*, never raw across cases.
- **Per node the students separate cleanly and flatly:** Llama ≈ **2.0**, GPT-5 ≈ **1.67** distance per teacher node, roughly constant across difficulty.

---

## Table 2 — Patch effect (did the student learn?)

`patched − baseline` on the clean, verified-only store under the canonical combined aligner. **Negative = learned** (bold).

| Student | k | E2 | M2 | H2 | mean |
|---|---|--:|--:|--:|--:|
| **Llama** | 1 | +10.5 | **−4.0** | **−7.0** | −0.2 |
| **Llama** | 3 | +10.5 | **−2.0** | **−4.5** | +1.3 |
| **Llama** | 5 | +2.0 | 0.0 | **−11.5** | **−3.2** |
| **GPT-5** | 1 | **−6.0** | **−7.5** | +21.0 | +2.5 |
| **GPT-5** | 3 | **−1.0** | **−13.5** | +9.0 | **−1.8** |
| **GPT-5** | 5 | 0.0 | +4.0 | **−6.5** | **−0.8** |

- Llama **learns on M2 and H2 at every k** (all negative); it is hurt only on E2.
- The learning is **real but modest** and sign-flips across cases — consistent with the effect sitting near the run-to-run noise floor (the honest Phase-3/4 finding).
- **This is the number to read for "did the patches help,"** not the separation in Table 1.

---

*Both tables regenerate from `data/snapshots/embedding_combined_v1/` and
`results/k_ablation_combined_clean.csv`. Student separation is a baseline property;
patch effect is the intervention signal — do not conflate them.*
