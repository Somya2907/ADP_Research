# Snapshot: embedding_combined_v1

Discrepancy snapshot generated with the **combined** rule aligner on the
**embedding** text backend — the answer to Prof. Rao's citation-hybrid concern.

- Text similarity: `BAAI/bge-small-en-v1.5` cosine, threshold 0.55.
- Rule alignment: `LEX_DRL_RULE_ALIGN=combined` — exact citation agreement forces
  a match; sibling subsections (e.g. §6-1-1703(2)(a) vs (2)(b)) are discounted
  below threshold so embeddings cannot merge legally distinct rules; text
  otherwise. See `src/lex_drl/alignment.py::_align_rules_combined`.

Result: **GPT-5 < Llama 6/6**, Σ L-GED 1622.5 (vs the default-hybrid
`embedding_v1`: 6/6, Σ 1614.5 — the ranking is unchanged, confirming the finding
is not an artifact of the similarity backend).

Regenerate:
```
LEX_DRL_SIMILARITY=embedding LEX_DRL_RULE_ALIGN=combined \
  poetry run python scripts/run_discrepancy_analysis.py --force \
  --out-dir data/snapshots/embedding_combined_v1/discrepancies \
  --summary-csv data/snapshots/embedding_combined_v1/results/discrepancy_summary.csv
```

**Do not delete `tfidf_v1` / `embedding_v1`** — those are the Phase-1/3 snapshots
the paper cites. This directory is additive.
