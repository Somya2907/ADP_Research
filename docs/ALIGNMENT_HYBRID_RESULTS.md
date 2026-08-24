<!--
Answers Prof. Rao's concern: "you moved to sentence embeddings, but citations carry
meaning embeddings can't distinguish — you should use a hybrid and show results."
Reproduce: LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_alignment_hybrid_ablation.py
-->

# Hybrid rule alignment — does the citation concern change the results?

**The concern (Prof. Rao):** we switched node matching to sentence embeddings, but statute
citations (e.g. `§6-1-1703(2)(a)` vs `(2)(b)`) look almost identical to an embedding yet are
legally distinct. Rule matching should be a **hybrid** of citation + text, and we should show
results under it.

**Two-part answer:** (1) the concern is **empirically correct** — embeddings cannot separate
sibling subsections; (2) we are **already citation-first for rules**, and when we run the full
hybrid ablation the **headline ranking is robust (6/6) under every variant**, so the concern
sharpens the method but does **not** overturn the result.

---

## 1. The concern is real — embeddings can't tell subsections apart

Cosine similarity on the rule text of genuinely different provisions (same base section,
different subsection) — all **above** the 0.55 match threshold, so embeddings alone would
**merge** them:

| Rule A | Rule B | Cosine | Verdict |
|---|---|--:|---|
| `§20-871(a)(1); §5-301(a)` | `§20-871(d)(2)` | 0.805 | would merge |
| `§20-871(a)(1); §5-301(a)` | `§20-871(a)(2), §20-873; §5-303` | 0.787 | would merge |
| `§20-872; §5-304(a)-(c)` | `§5-304(d)` | 0.747 | would merge |
| `§6-1-1703(2)(a)-(g)` | `§6-1-1703(6)` | 0.631 | would merge |
| `§20-871(a)` | `§20-871(b)` | 0.633 | would merge |

So yes — on their own, embeddings would treat these distinct duties as the same node. The
citation tokens are the only reliable signal that keeps them apart.

## 2. We are already citation-first for rules (not pure embeddings)

`align_rules` (in `src/lex_drl/alignment.py`) is a **hybrid today**:

1. **Citation match first** — normalize citation tokens on both sides; align if they intersect
   (method-independent, no embeddings involved).
2. **Embedding fallback** — only rules with no citation match fall through to embedding cosine.

All other node types (facts/issues/application/conclusions/obligations) have no citations, so
embeddings are the right tool there. The "6/6 embedding" numbers already run through this
citation-first rule path.

## 3. Results under every rule-alignment mode (all 6 cases, both students)

Holding non-rule nodes on embeddings and swapping only the rule aligner:

| Rule mode | GPT-5 < Llama | Σ L-GED | Σ misgroundings* |
|---|:--:|--:|--:|
| **embedding_only** (the non-hybrid) | **6/6** | 1614.5 | 56 |
| **citation_only** (no text fallback) | 5/6 | 2002.0 | 0 |
| **hybrid** (current: citation-first + fallback) | **6/6** | 1614.5 | 51 |
| **hybrid_combined** (citation match + sibling-subsection discount) | **6/6** | 1622.5 | 51 |

*misgroundings = aligned rule pairs whose citations conflict — i.e. embeddings pairing rules
that cite different sections. Tracked as a diagnostic; **not** folded into L-GED by default.

**What this says:**
- **The ranking is robust.** Embedding-only, the current hybrid, and a stronger hybrid all give
  **6/6**. The GPT-5 < Llama result is driven by the huge coverage gap (Llama omits 60+ teacher
  nodes), which dwarfs subsection-level citation nuance. The professor's concern does **not**
  threaten the headline.
- **Pure citation matching is worse (5/6, Σ L-GED +388).** Students rarely cite *identically* to
  the teacher (the teacher writes compound cites like `§20-871(a)(1); §5-301(a)`; the student
  writes `§20-871(a)`), so citation-only leaves most rules unmatched and inflates "missed nodes."
  This is exactly why a text signal is needed — citations alone are too brittle.

## 4. The real, honest gap (worth telling the professor)

The current hybrid is *nominally* citation-first, but the **citation step only fires for ~5% of
teacher rules** (14% of the rules that get matched at all). Reason: exact citation-token matching
requires the same subsection, and the teacher's compound citations rarely token-match the
student's shorter ones. So in practice, **rule matching is mostly embedding-driven anyway** — which
is the kernel of truth in the professor's concern.

Embeddings consequently pair **~51–56 rule pairs with conflicting citations** across the 6 cases.
Those are surfaced as `v_misground` (a separate channel) and are **kept out of the L-GED total by
default**, so they don't corrupt the headline — but for *per-rule* precision they matter.

## 5. Recommendation

- **Report all three modes as a robustness check** in the paper (this table *is* "results through
  the hybrid"): the GPT-5 < Llama ranking holds 6/6 under embedding-only, hybrid, and
  hybrid_combined — so the finding is not an artifact of the similarity backend.
- **Adopt `hybrid_combined` as the default rule aligner** (citation agreement forces a match;
  sibling subsections are discounted so embeddings can't merge `(2)(a)` with `(2)(b)`; text
  embedding otherwise). It keeps 6/6, barely moves L-GED (+8 over 12 datapoints), and closes the
  theoretical hole. *(Deferred as a default change because it shifts every pinned snapshot; safe
  to flip once we re-pin.)*
- **Longer term:** a base-section citation tier (match on `20-871` even when subsections differ,
  then use the subsection as a tie-breaker/misgrounding signal) would raise the 5% citation-fire
  rate without merging siblings — the best of both.

*Reproduce all numbers: `LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_alignment_hybrid_ablation.py`.*
