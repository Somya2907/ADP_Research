# L-DRL: Legal Differential Reasoning Learning for US AI Law

Applying [Differential Reasoning Learning](https://arxiv.org/abs/...) (Liu et al., 2026) to
legal compliance reasoning under the **Colorado AI Act (SB 24-205)** and **NYC Local Law 144**,
using a novel **F-I-R-A-C-O** (Facts–Issues–Rules–Application–Conclusion–Obligations) typed
reasoning graph.

## Research Overview

This project implements Legal DRL (L-DRL), which:
1. Represents legal reasoning as typed DAGs (F-I-R-A-C-O nodes + typed edges)
2. Compares agent reasoning (G_agent) against teacher reasoning (G_ref)
3. Mines discrepancies into reusable natural-language patches (L-DR-KB)
4. Retrieves relevant patches at inference time to close reasoning gaps

**Target venue:** JURIX 2026 (Toulouse, December 2026), with ICAIL 2026 workshop as fallback.

## Quickstart

Four commands from a fresh clone to a first extraction:

```bash
git clone <your-private-repo-url> && cd l-drl-us-ai-law
cp .env.example .env             # then fill in API keys (see Detailed Setup)
make setup                       # poetry install + create output dirs
make check                       # verify env, schema, and the three model providers
make extract-teacher             # produce the 6 reference (teacher) graphs
```

Then `make breakdown` for a per-graph node-type table, or
`poetry run streamlit run scripts/view_graph.py` to inspect graphs interactively.

Full list of `make` targets: `make help`.

## Detailed Setup

```bash
# 1. Clone and install
git clone <your-private-repo-url>
cd l-drl-us-ai-law
poetry install

# 2. Configure API keys
cp .env.example .env
# Edit .env with your Anthropic, OpenAI, and OpenRouter keys.
# Also set TEACHER_MODEL, AGENT_MODEL, SMALL_MODEL.

# 3. Populate statute texts (see data/statutes/README.md)
# Download CO AIA, NYC LL 144, and optionally TX TRAIGA

# 4. Verify environment (Python, venv, env vars, dirs, schema, API pings)
poetry run python scripts/check_setup.py

# 5. Run schema tests
poetry run pytest

# 6. Day 1 smoke test (single case E1)
poetry run python scripts/smoke_test_e1.py

# 7. Day 2 wide run (all 6 cases × 3 models)
poetry run python scripts/run_extraction.py
```

## Sprint Cases (5-Day Walking Skeleton)

| ID | Title | Jurisdiction | Tier | Role | Key Test |
|----|-------|-------------|------|------|----------|
| E1 | ResumeRank NYC | NYC | Easy | Training | AEDT bias audit + notice violations |
| E2 | PromoteAI NYC | NYC | Easy | Test | Notice timing/content; patch transfer from E1 |
| M1 | LoanScore Denver | CO | Medium | Training | Deployer obligations, rubber-stamp human review |
| M2 | TenantRank Boulder | CO | Medium | Test | Small-deployer exception trap (own-data condition) |
| H1 | PeopleScore Multi-State | NYC+CO+TX | Hard | Training | Multi-jurisdictional scoping, authority confusion |
| H2 | AutoApprove Lending | CO | Hard | Test | Substantial-factor ambiguity, authority hierarchy |

## Alignment & Discrepancy Scoring

Each student graph is scored against the teacher graph with **L-GED** (legal-weighted
graph edit distance: `v_miss` + `v_halluc` + `e_diff`, lower = closer to teacher).
The one tunable step is **node alignment** — matching student nodes to teacher nodes.
Rules align by citation token first; everything else falls back to a text-similarity
backend selected at runtime by the `LEX_DRL_SIMILARITY` environment variable:

| `LEX_DRL_SIMILARITY` | Backend | Threshold |
|---|---|---|
| `tfidf` *(default)* | n-gram (1,2) TF-IDF cosine | 0.10 |
| `embedding` | `BAAI/bge-small-en-v1.5` sentence-embedding cosine | 0.55 |

```bash
# Default (TF-IDF)
poetry run python scripts/run_discrepancy_analysis.py --force

# Embedding backend
LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_discrepancy_analysis.py --force
```

The embedding model name is overridable via `LEX_DRL_EMBEDDING_MODEL`. The backend
falls back to TF-IDF if `sentence-transformers` is unavailable.

**Why two backends.** TF-IDF is brittle to paraphrase: it mislabels the frontier
model's reworded nodes as hallucinations, which inverts the model ranking on the
medium/hard cases. The embedding backend ranks GPT-5 below the 3B model (the expected
ordering, since L-GED is distance-from-teacher) on **6/6** cases vs **2/6** for TF-IDF.
Full comparison: [`docs/ALIGNMENT_METHODS.md`](docs/ALIGNMENT_METHODS.md) (auto-generated
from the snapshots). **Caveat:** the 0.55 embedding threshold is calibrated on E1 only.

**Snapshot layout.** Each backend's scored output is frozen for reproducibility:

```
data/snapshots/
├── tfidf_v1/
│   ├── discrepancies/       # {case}_{student}.json — per-pair reports
│   └── results/
│       └── discrepancy_summary.csv
└── embedding_v1/            # same layout, embedding backend
```

Graphs are frozen; the two snapshots score the *same* graphs with different backends.
Regenerate the comparison doc with `poetry run python scripts/build_alignment_doc.py`.

## Project Structure

```
src/lex_drl/
├── schema.py          # F-I-R-A-C-O pydantic schema (foundational)
├── clients.py         # Anthropic + OpenAI SDK wrappers with caching
├── cache.py           # Disk-backed response cache (saves API costs)
├── cases.py           # Case file loader
├── alignment.py       # Node alignment (tfidf | embedding backend)
├── discrepancy.py     # v_miss / v_halluc / e_diff + L-GED scoring
├── results.py         # Aggregate discrepancy reports → DataFrames
└── extraction.py      # Case → graph pipeline

configs/
├── prompts/           # Teacher and agent prompt templates
└── models.yaml        # Model configurations (3 tiers)

data/
├── cases/             # 6 sprint case markdown files
├── statutes/          # Authoritative text (gitignored)
└── outputs/           # Run artifacts (gitignored)

scripts/
├── smoke_test_e1.py   # Day 1: single-case validation
└── run_extraction.py  # Day 2: all-case extraction
```

## Sprint Timeline

| Day | Focus | Gate |
|-----|-------|------|
| 1 | Setup + smoke test E1 | Schema validates; both models produce JSON |
| 2 | All 6 cases; hand-inspect teacher graphs | 12 graph files; teacher quality confirmed |
| 3 | Hand-diff training cases (E1, M1, H1); generate 3 patches | 3 discrepancy reports + 3 patches |
| 4 | Inject patches into test cases (E2, M2, H2); with/without comparison | 6 agent outputs (3 pairs) |
| 5 | Manual rubric scoring; walking skeleton report | Results table + narrative |

## Key References

- Liu, J. et al. (2026). *Closing Reasoning Gaps in Clinical Agents with Differential Reasoning Learning.*
- Guha, N. et al. (2023). *LEGALBENCH.* 162 legal reasoning tasks.
- Fei, Z. et al. (2023). *LawBench.* Chinese legal benchmarking.
- Shi, Y. et al. (2026). *PLAWBENCH.* Rubric-based legal evaluation.
- Jiang, C. & Yang, X. (2023). *Legal Syllogism Prompting.*
- Trautmann, D. et al. (2022). *Legal Prompt Engineering for Multilingual LJP.*
- Kong, A. et al. (2024). *Better Zero-Shot Reasoning with Role-Play Prompting.*
