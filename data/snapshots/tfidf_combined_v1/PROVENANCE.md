# Snapshot: tfidf_combined_v1

Discrepancy snapshot with the **combined** rule aligner on the **TF-IDF** text
backend — the control cell that shows the combined hybrid does **not** rescue
TF-IDF.

- Text similarity: n-gram (1,2) TF-IDF cosine, threshold 0.10.
- Rule alignment: `LEX_DRL_RULE_ALIGN=combined` (see
  `src/lex_drl/alignment.py::_align_rules_combined`).

Result: **GPT-5 < Llama 0/6**, Σ L-GED 2143.0 — same 0/6 as the default-hybrid
`tfidf_v1` (Σ 2075.0). Fixing the rule aligner does not help TF-IDF, because the
ranking failure is driven by paraphrase mismatch on the *non-rule* nodes
(facts/issues/application), which only embeddings resolve. Confirms the citation
concern is orthogonal to (and does not overturn) the Phase-1 embedding result.

Regenerate:
```
LEX_DRL_SIMILARITY=tfidf LEX_DRL_RULE_ALIGN=combined \
  poetry run python scripts/run_discrepancy_analysis.py --force \
  --out-dir data/snapshots/tfidf_combined_v1/discrepancies \
  --summary-csv data/snapshots/tfidf_combined_v1/results/discrepancy_summary.csv
```

**Do not delete `tfidf_v1` / `embedding_v1`** — those are the snapshots the paper
cites. This directory is additive.
