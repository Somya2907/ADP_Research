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

```bash
# 1. Clone and install
git clone <your-private-repo-url>
cd l-drl-us-ai-law
poetry install

# 2. Configure API keys
cp .env.example .env
# Edit .env with your Anthropic and OpenAI keys

# 3. Populate statute texts (see data/statutes/README.md)
# Download CO AIA, NYC LL 144, and optionally TX TRAIGA

# 4. Run schema tests
poetry run pytest

# 5. Day 1 smoke test (single case E1)
poetry run python scripts/smoke_test_e1.py

# 6. Day 2 wide run (all 6 cases)
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

## Project Structure

```
src/lex_drl/
├── schema.py          # F-I-R-A-C-O pydantic schema (foundational)
├── clients.py         # Anthropic + OpenAI SDK wrappers with caching
├── cache.py           # Disk-backed response cache (saves API costs)
├── cases.py           # Case file loader
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
