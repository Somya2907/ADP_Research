# Handoff — L-DRL for US AI law (state as of 2026-10-31)

Context for a coding assistant picking up this project. It summarises a long working session: what the project is, the user's working rules, how to run things, what was built and found, what is half-done, and the traps that cost time.

Repo: `/Users/somayajain/Research-Anand_rao/l-drl-us-ai-law`, branch `phase5-iterative-loop`. Phase 5/6 code, cases, result summaries, and the Prof. Philipp review materials are included in the 1 November 2026 publication update. Raw model outputs, execution logs, caches, secrets, and the reference paper PDF remain local.

---

## 1. The project in one paragraph

A research project for **Prof. Anand Rao** (the user is his student; a legal expert, **Prof. Philipp**, reviews legal content). It adapts Liu et al., KDD 2026 ("discrepancy-driven" reasoning patches; PDF in the parent folder) to US AI law: NYC Local Law 144, the Colorado AI Act, Texas TRAIGA.

- A **teacher** (Claude Opus 4.6, given statute text) writes a FIRACO reasoning graph per case: Facts, Issues, Rules, Applications, Conclusions, Obligations, plus edges.
- A **student** (Llama-3.2-3B-Instruct, no statutes) writes the same kind of graph.
- **L-GED** (legal-weighted graph edit distance) measures how far the student's graph is from the teacher's. Lower is better.
- **Patches** mined from the student's training-case mistakes are injected into its prompt, to see whether the weak student improves on unseen test cases.

## 2. The user's working rules (follow these)

- **Never add a `Co-Authored-By: Claude` trailer** to commits in this repo. The user removed Claude as a contributor. This is also stored in auto-memory.
- **Commit only when the user asks.** The user authorised the 1 November 2026 publication update; future commits still require a request.
- Refer to people as **"Prof. Rao"** and **"Prof. Philipp"**.
- **Human-facing docs:** plain English and to the point. No `file:line` references in docs written for people.
- Report results honestly: confidence intervals and paired tests, a placebo or noise floor, and caveats. Don't oversell.
- The user often asks just "updates?". Answer with a short status from logs. Don't poll background jobs in a loop.
- The user's Mac is an **M4 with 16 GB RAM**. Running the student locally makes it slow and swap-heavy, so they prefer generation on the **Colab T4** (see §4).

## 3. Environment

- **Python:** an in-project venv `.venv` (`poetry.toml` sets `virtualenvs.in-project = true`; an earlier venv in `~/Library/Caches` got wiped).
  - Run everything with `.venv/bin/python`.
  - Tests: `.venv/bin/python -m pytest -q` gives **160 passed**.
- **The scorer must use the embedding backend.** The code default (`tfidf`) ranks the models backwards. Every script sets these with `setdefault`:
  - `LEX_DRL_SIMILARITY=embedding` (model BAAI/bge-small-en-v1.5, threshold 0.55)
  - `LEX_DRL_RULE_ALIGN=combined`
- **Student generation:** greedy (deterministic), up to 4096 new tokens. Other environment variables:

  | Variable | Meaning |
  |---|---|
  | `SMALL_MODEL_BACKEND` | `local` (HF transformers on Apple MPS, fp16), `remote` (Colab T4 server), or unset (OpenRouter, unusable: see §9) |
  | `SMALL_MODEL_LOCAL_REPO` | `unsloth/Llama-3.2-3B-Instruct` (ungated copy of the Meta weights) |
  | `SMALL_MODEL_REMOTE_URL`, `SMALL_MODEL_REMOTE_KEY` | printed by the Colab notebook; kept in `.env` |
  | `SMALL_MODEL_REMOTE_TAG` | suffix on the remote model name (default `colab-t4`) so remote cache entries never mix with local ones |
  | `LEX_DRL_LOOP_GUARD=1` | stop a generation that has started looping (see §6) |
  | `LEX_DRL_MAX_GEN_SECONDS` | per-answer time cap (the loop script sets 2400) |

- **Cache:** `.cache/llm` (diskcache), keyed on namespace, model name, system prompt, user prompt and call kwargs.
  - Stopping criteria and environment variables are deliberately **not** part of the key.
  - Re-running anything replays finished answers instantly, so a stopped run resumes where it stopped.
  - Namespaces: `agent_llama3_2b` (whole answers) and `agent_llama3_2b_continue` (repair continuations).
- **`.env` holds secrets:** Anthropic key, OpenRouter key, HF token, and the remote URL/key. Never print, publish or commit it.

## 4. Running the student on the Colab T4 (the preferred backend)

The notebook `notebooks/colab_t4_server.ipynb` does everything needed:
- loads `unsloth/Llama-3.2-3B-Instruct` in fp16 on CUDA;
- holds a verbatim copy of `src/lex_drl/loopguard.py`;
- runs a FastAPI job server (`POST /submit`, `GET /result/{id}`, `GET /health`, header `X-API-Key`);
- exposes it through a Cloudflare quick tunnel.

Quick tunnels drop responses slower than about 100 s, which is why the API is submit-then-poll. The user opens the notebook through the Colab extension in their editor (Antigravity), picks a T4 runtime and runs all cells.

- **Setup:** the second-to-last cell prints `SMALL_MODEL_REMOTE_URL=…` and `SMALL_MODEL_REMOTE_KEY=…`. The user pastes them into `.env`.
- **The last cell** is an endless keep-alive loop by design. When work is finished, tell the user to stop it **and terminate the runtime**, so the free GPU quota isn't burned.
- **Free Colab disconnects** after a few hours or when idle.
  - `RemoteSmallModelClient` handles this. If the server stops answering, it waits, prints "server unreachable — restart …", re-reads `.env`, and resubmits the job once the URL or key changes.
  - So: restart the notebook, update `.env`, and the run continues.
- **Speed:** about 1 minute per unpatched answer and about 2–2.5 minutes per checklist answer, so about 45–80 minutes per 30-case round.
- **T4 answers are not bit-identical to the Mac's.** They diverge partway through an answer. Never mix local and remote results in one comparison: each backend has its own round-0 baseline.

## 5. Data and split

- **Cases:** 30 synthetic cases in `data/cases/`: E1–E10 (easy), M1–M10 (medium), H1–H10 (hard).
  - Each file has metadata including `- parties:` (used by the leak guard).
  - `MANIFEST.md` is generated by `scripts/build_case_manifest.py`.
  - The cases haven't been reviewed by a legal expert yet.
- **Split (5 training / 5 test per tier):**
  - Training: E1, E3–E6, M1, M3–M6, H1, H3–H6
  - Test: E2, E7–E10, M2, M7–M10, H2, H7–H10
  - Test cases are never mined. `generate_patches` and `checklist.missed_items` raise on non-training cases.
- **Teacher graphs:** `data/outputs/graphs/{case}_reference.json`, 30 of them. The original six (E1/E2/M1/M2/H1/H2) are frozen.
  - **12 of 30 cite NYC §20-875, which does not exist.** That costs about 5 L-GED per affected case.
  - The list for expert review is `results/diagnostics/teacher_suspect_nodes.csv`.
  - Fabricated citations are excluded from everything patches and checklists teach.

## 6. Code map

### Modules in `src/lex_drl/`

New in this phase, or heavily changed:

| Module | What it does |
|---|---|
| `injection.py` | Prompt notes rendering (`render_notes_block`, `build_patched_system`), training-party leak guard |
| `loop.py` | Phase 5 iterative *patch* loop (BM25 top-k, re-mine, Claude rewrite, priority); also `score`, `patch_targets`, `patch_outcome`, `empty_graph` |
| `diagnostics.py` | Ceiling, teacher-without-fabricated, oracle patch selection, directive (checklist) notes, placebo notes, uptake |
| `checklist.py` | **The method that works.** Items = teacher R/O nodes missed on training cases; clusters by kind and canonical section; `rank` (support / similarity / combined, plus learned priority); `match_pairs` / `match_gaps` / `coverage`; `render_checklist` |
| `checklist_loop.py` | Iterative loop with checklist patches: re-mine, efficacy-based priority, wording swap, plateau / fixpoint stop |
| `loopguard.py` | Detects a looping answer: one JSON node line (ID removed) seen 3 times, or more than 30 lines of one node type (edges exempt). `truncate_loop` and a transformers `LoopGuard` stopping criterion give identical cuts under greedy decoding |
| `repair.py` | `generate_with_repair`: if the answer stopped at the `=== JSON GRAPH ===` marker with no JSON, resume with `{`; if it looped, cut it and resume at the next JSON section (`],` plus `"<next>": [`). Adds no content; at most 3 repairs; untouched answers are returned as-is |

Also changed:
- **`clients.py`:**
  - `LocalSmallModelClient.continue_from`
  - `_add_time_cap`
  - `RemoteSmallModelClient` (submit/poll, `.env` reload)
  - the factory picks local / remote / OpenRouter
- **`extraction.py`:** the sanitizer now maps or fills, instead of rejecting the graph:
  - invalid issue status → `dispositive`
  - invalid fact polarity → `present`
  - dangling edges → dropped
  - missing application `reasoning` / `fact_refs` → filled with defaults
  - missing or unknown edge `type` → `supports`
- **`patch_generator.py`:** `canonical_citation()` (e.g. `colorado:6-1-1703`, whatever the citation format), `dedup_merge(canonical=False)`, and `InsightWriter.rewrite_failed`.
- **`patch_store.py`:** Phase 5 bookkeeping fields and the `priority_alpha` / `stopwords` options on `retrieve`. Defaults keep Phase 2–4 behaviour.
- **`cases.py`:** `parties`, tiers, `cases_by_role`, `case_census`.

### Scripts in `scripts/`

| Script | Use |
|---|---|
| `run_patch_loop.py` | Phase 5 BM25 patch loop (`--run`, `--k`, `--rounds`, `--no-rewrite`, …) |
| `analyze_patch_diagnostics.py` | Stage A (no model): ceiling, teacher sensitivity, retrieval audit, citation collapse |
| `run_patch_diagnostics.py` | One prompt arm on test cases, paired against a baseline round-0 folder |
| `diagnostics_report.py` | Summarises the arms into `results/diagnostics/REPORT.md` and `dose.html` |
| `evaluate_checklist_retrieval.py` | Offline (no model) comparison of item rankers, plus tier transfer |
| `run_checklist_loop.py` | Checklist loop (`--backend local\|remote`, `--run`, `--k 10`, `--rounds 5`, `--patience 2`) |
| `summarize_checklist_loop.py` | Rebuilds a loop's results (tables, tests, curve) from saved answers with the current parser |

`run_patch_diagnostics.py` details:
- arms: `placebo`, `oracle_k3`, `oracle_k10`, `oracle_all`, `directive_k10`, `llm_k10`, `checklist_k5`, `checklist_k10`
- options: `--cases <ids>|test`, `--name`, `--backend`, `--base-run`; remote outputs get a `_t4` suffix

Tests: `test_cases`, `test_loop`, `test_diagnostics`, `test_c1` (loop guard, repair, checklist), `test_checklist_loop`, `test_extraction_sanitizer`, plus one added to `test_patch_store`. All use fake students and embeddings, with no model and no API.

## 7. What was found

### Phase 5: the original patch loop failed (Mac)

BM25 top-3 patches, re-mined each round with Claude rewrites (`results/loop/full`):

| | Round 0 | Round 1 | Round 2 |
|---|--:|--:|--:|
| Training mean L-GED | 139.27 | 142.97 | 143.03 |
| Test mean L-GED | 133.47 | 132.97 | 132.87 |

So test moved about −0.6, which is noise, and the loop plateaued at round 0. The `no_rewrite` run was similar. This is written up in `docs/PROJECT_SUMMARY.md` §8.

### Phase 6: diagnosis and the checklist method

This phase is **not yet in PROJECT_SUMMARY.md**.

**Stage A, no model runs** (`results/diagnostics/STAGE_A.md`):
- Only **27% (training) / 18% (test)** of injected patches targeted something the case was actually missing.
- Even perfect k=3 patches cap the gain at **9%** of L-GED.
- **39%** of L-GED comes from missing F/I/A/C nodes, which patches never targeted.
- **39%** of stored patches duplicate a section in another citation format (241 patches cover only 21 sections).

**Stage B, oracle arms on 6 test cases** (E2, E8, M2, M9, H2, H10; Mac). Oracle = the case's own missing nodes, an upper bound only. Results are in `results/diagnostics/REPORT.md`:

| Arm | L-GED change | Given nodes written |
|---|--:|--:|
| Placebo (3 irrelevant notes) | +2.8 | – |
| Oracle k=3, advice wording | −1.4 | 44% |
| Oracle k=10, advice wording | −5.3 | 45% |
| Oracle, all missing R/O | +9.1 | 29% |
| **Oracle k=10, checklist wording** | about −9 to −19 (depending on one looped answer) | 72–86% |
| Oracle k=10, Claude-written | −3.8 | 37% |

So the **checklist wording matters most**, k=10 beats k=3, all nodes is too many, and LLM-written patches are worse than templates.

**C1, the checklist method:**
- Items come from training cases only: 222 items in 50 clusters.
- Each case gets the top 10, ranked by label similarity to the case text plus how many training cases missed the item (support).
- Offline, precision@10 is 52% vs BM25's 33%, and fillable L-GED is 18.5 vs 10.4 (`results/c1/RETRIEVAL.md`).
- Items from hard training cases transfer best to medium and hard test cases.

**Mac 15-case confirmation** (k=10 checklist, `results/diagnostics/CONFIRM15.md`):
- −14.6 overall: 12/15 improved, t-test p = 0.0001, Wilcoxon p = 0.002.
- −15.8 on the 9 cases never used for tuning.

**Colab T4 (final numbers, `results/loop/checklist_t4/LOOP_RESULTS.md`):**

| Round | Training L-GED | Test L-GED | Test change vs round 0 | Test cases improved |
|--:|--:|--:|--:|--:|
| 0 (baseline) | 141.60 | 133.63 | – | – |
| **1** | 129.97 | **115.17** | **−18.5 (CI −22.6 to −14.1)**, Wilcoxon p = 0.0007 | 15/15 |
| 2 | 131.37 | 122.27 | −11.4 | 14/15 |
| 3 | 126.23 | 118.43 | −15.2 | 14/15 |

- **Placebo on all 15 test cases** (`results/diagnostics/placebo_all15_t4.csv`): −1.3 (7/15 improved, p = 0.66).
- **Checklist minus placebo:** −17.2 (CI −22.5 to −11.5), better in 14/15 cases (t-test p = 0.00004, Wilcoxon p = 0.001).
- **Learning stops after round 1.**
  - Round 2 vs round 1: +7.1 (Wilcoxon p = 0.017).
  - Round 3 vs round 1: +3.3 (p = 0.26).
  - Training keeps improving, so the later updates overfit.
  - The user agreed to stop the loop after round 3. A partial `round_4` folder exists under `data/outputs/loop/checklist_t4/`: ignore it.
- **Coverage:** test R/O recovered goes from 17.8% to 40.2% in round 1, and rules per answer from 3.1 to 8.6.
- **By tier (test means, round 0 → round 1):** easy 114.2 → 95.7, medium 123.5 → 102.7, hard 163.2 → 147.1.

The Mac checklist loop (run `checklist`) completed only rounds 0–1 (training 123.77, test 118.77) before the switch to the T4.

**Loop repair:**
- Repairing the looped answers barely changes the scores (±2.5 per answer, 0.1 on the 15-case mean), but it makes every graph complete.
- The cut versions are kept in `results/diagnostics/before_repair/`.

### The brief for Prof. Rao

A Claude Docs document, **"Patch learning for a small student model: results"**: https://claude.ai/artifact/EcmQY3EXj9LWbiuJGBfoFR

It has 8 sections, including a learning-curve chart and answers to the questions from the last meeting. It's private until the user shares it from the page's Share menu.

## 8. Open tasks

1. **Publication update (1 November 2026):** the user authorised committing and pushing Phase 5/6 on `phase5-iterative-loop`, without a Claude co-author trailer. Include result tables, reports, curves, and patch-store snapshots; leave execution logs and raw `data/outputs/` artifacts local. `docs/PROF_PHILIPP_REVIEW.md` and its Word copy link all 30 cases to readable teacher FIRACO pages under `docs/review/firaco/`. Those pages preserve source text and node IDs and record source hashes; they are unverified model outputs, not corrected references.
2. **Add a Phase 6 section to `docs/PROJECT_SUMMARY.md`.** Write it in plain English, with no file:line references. Also update §9 "What we're going to try now".
3. **Next experiments** (from the meeting and the brief):
   - A **reasoning or chain-of-thought student** (e.g. Qwen3-4B with thinking) and a **larger student** (Llama-3.1-8B), with the same k=10 checklist.
     - On the T4: change `REPO` in the notebook, set `SMALL_MODEL_LOCAL_REPO` locally to the same repo (the remote model name is built from it), and use a new `--run` name.
     - Each new student needs its own round 0.
   - **More training cases**, especially hard multi-state ones, to raise the ceiling. Training items cover only about a third of what test cases miss.
   - **Network analysis** of the FIRACO graphs (centrality, path length). This was raised in the meeting and hasn't been started.
4. **Expert review** by Prof. Philipp: the 30 cases, and the suspect teacher rules (§20-875).
5. Not done, and low priority: the oracle all-nodes arm on H2/H10 (it hit the Mac's memory limit), and the oracle H10 checklist-wording repair.

## 9. Traps that cost time (read before running anything)

- **The local backend on this Mac:**
  - Long prompts make PyTorch's MPS memory balloon to 14–16 GB, and single answers can take hours.
  - The Mac also sleeps overnight and pauses runs: wrap long local runs in `caffeinate -i`.
  - Prefer the T4.
- **Paid APIs are not available.**
  - OpenRouter: both keys are free-tier with $0 credit, and Llama-3.2-3B has no free route there.
  - HF Inference Providers: the token has no credits (402). Only Featherless serves this model there anyway.
- **Three ways the 3B student fails to produce a graph**, in addition to loops:
  - it stops right after the JSON marker (repaired);
  - it writes prose with no marker and no JSON (rare; scored as an empty graph);
  - small schema slips (handled by the sanitizer).

  An unparseable answer is scored as an empty graph, which inflates L-GED, so check `unparsed` counts in every summary.
- **Stale parsers:** a long run keeps the parser it started with. After a sanitizer fix, re-score from saved answers with `summarize_checklist_loop.py`, or by re-running the cached arm, before reporting.
- **The `_guard_round_zero` check** in the loop scripts compares local round 0 with the pinned Phase 5 baseline. It is skipped for the remote backend.
- **`data/outputs/loop/checklist/`** (Mac) and **`checklist_t4/`** (T4) are different backends. Don't compare across them.
- **Background jobs** started by a previous assistant session die when that session ends. Check `ps` and restart. Everything is cached, so a restart replays finished work in seconds.

## 10. Reproducing the headline results (T4)

These commands run from the repo, after the Colab notebook is up and `.env` holds its URL and key:

```bash
# checklist loop (round 0 baseline + rounds until the stop rule)
caffeinate -i .venv/bin/python scripts/run_checklist_loop.py --backend remote          # → data/outputs/loop/checklist_t4, results/loop/checklist_t4
# placebo on all 15 test cases, against the T4's own baseline
.venv/bin/python scripts/run_patch_diagnostics.py --arm placebo --cases test --backend remote \
    --base-run data/outputs/loop/checklist_t4/round_0 --name placebo_all15
# rebuild the loop tables, tests and curve from saved answers (current parser)
.venv/bin/python scripts/summarize_checklist_loop.py --run checklist_t4 --rounds 0 1 2 3
# offline retrieval comparison (no model)
.venv/bin/python scripts/evaluate_checklist_retrieval.py
.venv/bin/python -m pytest -q
```

With the cache in place, all of these replay without calling the model.
