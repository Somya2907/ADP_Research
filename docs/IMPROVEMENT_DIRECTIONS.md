<!--
Research directions to improve the intervention — literature-grounded.
Companion to PROJECT_SUMMARY.md. For the meeting with Prof. Rao.
-->

# How to Improve the Results — Research Directions

**The Phase-3 finding (effect within noise) tells us two separate things**, and each has a fix:

1. **The measurement is too noisy to see a small effect** — and most of that noise is *avoidable methodology*, not real signal. **Fixing this is cheap and comes first.**
2. **In-context patching has a low ceiling for a 3B model** — so the real gains come from *stronger interventions*, culminating in *actually learning from the teacher* (which is what "Differential Reasoning Learning" always implied).

Below: a staged roadmap (cheapest/highest-leverage first), each grounded in specific papers.

---

## Tier 0 — Make an effect *detectable* (do this first; cheap; non-negotiable)

Our reported ±9.5 run-to-run noise **exceeds** the ±6 effect. Multiple angles say most of that noise is fixable:

| Move | What & why | Papers |
|---|---|---|
| **Freeze the teacher graph** | Compute each teacher reference **once**, cache it, score every run against the fixed file. We're measuring the *student's* change against a fixed target — re-rolling the teacher manufactures variance. Kills the biggest variance term. | — |
| **Control decoding non-determinism** | Even "temp-0" LLMs wobble due to batch-size-dependent float reduction order. Pin batch=1, fixed seed; verify the local 3B is bit-identical across repeats. | *Defeating Nondeterminism in LLM Inference* (Thinking Machines, 2025); *The Good, Bad & Greedy* (Song 2024) |
| **Report the 3 L-GED components separately** | The aggregate sign-flips because "help on missed-nodes" cancels "harm on edges." Splitting missed / hallucinated / edge-cost **reveals** where patches help vs. harm (the frontier-model edge-harm is invisible in the total). | *deep-significance* (Ulmer 2022) |
| **Paired bootstrap over graph *elements*** | Treat each missed node / wrong edge as a resampling unit → a real 95% CI + p-value from n=3 cases. Turns "3 sign-flipping numbers" into "reduces L-GED by X [CI a,b]." | *Hitchhiker's Guide to Testing Significance in NLP* (Dror 2018); Berg-Kirkpatrick 2012 |
| **Self-consistency (K samples/cell)** | Sample the student K=5×, keep nodes/edges appearing in ≥3 samples (prunes hallucinations), report the spread as the true noise floor. Adds power without new cases. | *Self-Consistency* (Wang 2022); *Universal Self-Consistency* (Chen 2023) |

**Outcome:** either the existing ±6 effect becomes significant, or we get an **honest, well-powered null** — both are publishable; the current n=3 anecdote is not.

---

## Tier 1 — Fix retrieval & injection (cheap; removes *harm*)

| Move                                              | What & why                                                                                                                                                                                                     | Papers                                                     |
| ---------------------------------------------------| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------|
| **Jurisdiction gating + contamination blocklist** | Never inject a CO patch into an NYC case; hard-exclude the fabricated §20-875. Deterministic; kills the off-jurisdiction sign-flips.                                                                           | (RRF) Cormack 2009                                         |
| **Hybrid dense + BM25 retrieval**                 | Embed the patch's *instruction* (not just keywords), fuse with BM25 (RRF). Matches by meaning on a tiny corpus.                                                                                                | Contriever (Izacard 2022); HyDE (Gao 2022)                 |
| **Conditional / asymmetric injection**            | **Only inject a patch if the draft graph doesn't already contain that node.** A strong model that already cited the authority gets nothing → **stops patches disrupting the frontier model** (our GPT-5 harm). | Self-RAG (Asai 2023); Self-Refine (Madaan 2023)            |
| **Reason-then-schema**                            | Let the 3B reason in free text first, *then* extract into the FIRACO JSON. Forcing reasoning directly into rigid schema hurts weak models most ("format tax"). Raises the baseline, lowers the noise floor.    | *Let Me Speak Freely?* (Tam 2024); Outlines (Willard 2023) |

---

## Tier 2 — Fix the patches themselves (medium; the real ceiling-raiser)

The core disease: **we generate patches but never check they help before shipping them.** The fix everyone converged on:

- **Reflective patch generation + a held-out L-GED acceptance gate.** Turn on the (currently dormant) InsightWriter to abstract each training mistake into a *general principle* (not a rigid template); then **keep a patch only if it lowers L-GED on the *other* training cases** (leave-one-case-out). Discard harmful ones. *(LEAP — Zhang 2024; Reflexion — Shinn 2023; ExpeL — Zhao 2023.)*
- **Citation-decoupled structural recipes.** Abstract patches to *structure* ("emit a bias-audit Obligation grounded in the controlling local statute; assert a section only if independently verified") and **drop the specific section token** → the fabricated §20-875 can't propagate. *(ExpeL; Distilling Step-by-Step — Hsieh 2023.)*
- **Tool-grounded verification (not vibes).** After the draft, verify only Rule/citation nodes with a **deterministic citation checker**; revise only failing nodes. Critical caveat from the literature: **ungrounded self-correction does not work** — feedback must be external. *(Chain-of-Verification — Dhuliawala 2023; CRITIC — Gou 2023; "LLMs Cannot Self-Correct Reasoning Yet" — Huang 2024.)*
- **Optimize the notes-block text against L-GED** with a reflective prompt-optimizer (few rollouts, fits one Mac). *(GEPA — Agrawal 2025; OPRO — Yang 2023; TextGrad — Yuksekgonul 2024; DSPy/MIPROv2 — Khattab 2023.)*

---

## Tier 3 — Actually *learn* from the teacher (the "DRL" headline; higher ceiling)

L-GED **is a reward** — so stop only prompting and start training the 3B (LoRA, fits/near-fits the Mac):

| Move | What & why | Papers |
|---|---|---|
| **Rejection-sampling fine-tuning (workhorse)** | Sample K=64–256 graphs from the 3B, score each with L-GED, SFT on the best. Converts 3 cases into **hundreds of scored rollouts** (also fixes power!). Directly optimizes what we measure. | STaR (Zelikman 2022); RFT (Yuan 2023); ReST (Gulcehre 2023) |
| **Sequence-level distillation (init)** | SFT the 3B to reproduce the teacher's clean FIRACO graphs → fixes schema/citation-style errors (a big slice of L-GED). Then on-policy correct its own mistakes. | Seq-KD (Kim 2016); GKD (Agarwal 2024) |
| **DPO on L-GED-ranked pairs** | Turn L-GED gaps into (better, worse) pairs; a **margin filter ignores within-noise pairs** — robust to the jitter that sinks the current effect. | DPO (Rafailov 2023); RSO (Liu 2023) |
| **GRPO with L-GED as a verifiable reward** | The literal realization of "L-GED is a reward." Decompose the reward (node-recall, hallucination penalty, edge-F1, citation-correctness); KL-anchor to prevent gaming. *Ceiling / framing experiment.* | DeepSeekMath/GRPO (Shao 2024); Tülu 3 RLVR (Lambert 2024) |

---

## The prerequisite that unlocks Tiers 2–3

- **Teacher-driven data augmentation.** Have Claude synthesize **~15–40 more CO/NYC/TX cases + teacher graphs.** This is the single enabler: it gives statistical power, fixes the CO-jurisdiction skew, and provides training data for fine-tuning. Teacher graphs are **cacheable and reused** across every future experiment.
- **Multi-teacher consensus ground truth.** Build each reference from ≥2 strong models; a node enters ground truth only if corroborated. This **automatically quarantines the fabricated §20-875** (a single-source hallucination) — attacking the contamination without a manual re-extraction.

---

## Recommended sequence (what I'd actually do)

1. **Tier 0** — freeze teacher + determinism + component reporting + paired bootstrap + self-consistency. *(days; may already flip the verdict)*
2. **Tier 1** — jurisdiction gating + conditional injection + reason-then-schema. *(days; removes harm)*
3. **Data augmentation** — Claude synthesizes 15–40 cases + consensus teacher graphs. *(the unlock)*
4. **Tier 2** — reflective patches + acceptance gate + citation-decoupled recipes.
5. **Tier 3** — rejection-sampling FT as the workhorse; DPO for sharpness; GRPO as the paper's "DRL" ceiling experiment.

## The strategic reframe for the paper

> *Phase 3's null isn't a dead end — it's the finding that (a) the metric needs de-noising (mostly free) and (b) in-context patching under-delivers for small models, motivating a shift to **reward-driven learning** where L-GED is the training signal.* That arc — a defensible metric + an honest negative for prompting + a learning method that uses the metric as a reward — is a stronger, more novel paper than "our patches work."

---

### Papers cited (all real; arXiv IDs where useful)
Nondeterminism: Thinking Machines 2025 · Song 2024 (2407.10457). Significance/power: Dror 2018 (P18-1128) · Card 2020 · Reimers & Gurevych 2018 (1803.09578) · Ulmer 2022 (deep-significance). Self-consistency: Wang 2022 (2203.11171) · Chen 2023 (2311.17311). Retrieval: Cormack 2009 (RRF) · Izacard 2022 (Contriever) · Gao 2022 (HyDE, 2212.10496) · Asai 2023 (Self-RAG). Verification: Dhuliawala 2023 (CoVe, 2309.11495) · Gou 2023 (CRITIC, 2305.11738) · Huang 2024 (2310.01798) · Tam 2024 (format tax, 2408.02442). Patch gen: Zhang 2024 (LEAP, 2402.05403) · Shinn 2023 (Reflexion) · Zhao 2023 (ExpeL, 2308.10144) · Agrawal 2025 (GEPA, 2507.19457) · Yang 2023 (OPRO, 2309.03409) · Yuksekgonul 2024 (TextGrad, 2406.07496) · Khattab 2023 (DSPy, 2310.03714) · Hsieh 2023 (Distilling Step-by-Step, 2305.02301). Training/RL: Zelikman 2022 (STaR) · Yuan 2023 (RFT) · Gulcehre 2023 (ReST) · Kim 2016 (Seq-KD) · Agarwal 2024 (GKD) · Rafailov 2023 (DPO) · Shao 2024 (GRPO/DeepSeekMath) · Lambert 2024 (Tülu 3).
