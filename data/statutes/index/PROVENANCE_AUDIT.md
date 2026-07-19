# Statute corpus — provenance audit

Audit of `data/statutes/` to determine which sources are trustworthy for the
statute-section index (which backs the `v_halluc` validity check and the
misgrounding `student_section_exists` subtype). Method: read each `.txt` study
aid; extract section tokens from each authoritative `.pdf` with `pdftotext`;
compare. Conducted 2026-06.

## Headline

**All four `.txt` files in `data/statutes/` are AI-assisted study aids, not
verbatim statute text, and each contains errors that would corrupt a
section-existence index.** The index is therefore built only from the
authoritative source PDFs (CO AIA, NYC LL144). Because two needed sources are
unavailable (NYC DCWP Final Rules, TX HB 149 enrolled text), the index's
`trustworthy` flag is **False** and the gate (`make_section_exists_fn`) keeps it
from driving hard verdicts until the corpus is completed.

## Per-source findings

### CO AIA — `2024a_205_signed-act.pdf` → **verbatim** ✓
- The 26-page PDF is the enacted SB 24-205. `pdftotext` confirms sections
  **6-1-1701 through 6-1-1707** are all present (incl. 6-1-1705 ×2, 6-1-1707 ×3).
- `co_aia_sb24_205.txt` is a partial study aid: it **omits 6-1-1705 and
  6-1-1707** and inserts interpretive `NOTE:` blocks and an editorial "NIST AI
  RMF NOTE" with cross-framework commentary. Building the index from it would
  falsely report 1705/1707 as nonexistent. → index built from the PDF.

### NYC LL144 — `Legislation Text.pdf` → **verbatim** ✓ (statute-only)
- The 4-page PDF (Int. 1894-A) is the enacted Local Law 144. Real sections:
  **§20-870** (Definitions), **§20-871** (Requirements; subdivisions a, b),
  **§20-872** (Penalties; a–d), **§20-873** (Enforcement), **§20-874**
  (Construction). **There is no §20-875.**
- `nyc_ll144_statute.txt` **fabricates a §20-875**, **mislabels** §20-873 as
  "Public Disclosure" and §20-874 as "Applicability" (they are Enforcement and
  Construction), and **invents a §20-871(d)** ("new bias audit after retraining")
  that is not a subdivision in the enacted text.
- This **corrects the earlier `statute_index.fixture.json`**, which stopped NYC
  at 20-872 and missed 20-873/874.
- Marked `statute-only`: the LL144 statute is verbatim, but NYC citations also
  reference the DCWP Final Rules (6 RCNY §5-3xx), a separate source (below).

### NYC DCWP Final Rules — **MISSING**
- 6 RCNY §5-300 et seq. is not in the corpus as authoritative text. The teacher
  and students cite §5-300/5-301/5-302/5-303. `nyc_ll144_dcwp_rules.txt` is an
  unverified study aid, not an authoritative DCWP extract, so it is not used.
- Consequence: a real section like **§5-301 resolves to "does not exist"** under
  the current index — which is exactly why the trust gate must block it.

### TX TRAIGA — `89RDAY81FINAL.pdf` → **WRONG-FILE**; `.txt` → **summary**
- The PDF is a **House Journal** (floor proceedings / roll call for the 81st day
  of the 89th Legislature), **not** the HB 149 enrolled statute. First lines:
  "HOUSE JOURNAL … PROCEEDINGS … The house met at 11 a.m. … roll of the house
  was called".
- `tx_traiga_hb149.txt` is an **AI-generated summary** with a "NOTE ON
  LEGISLATIVE HISTORY" preamble, inline interpretive `NOTE:` blocks comparing
  TRAIGA to *other states'* laws, a "KEY COMPLIANCE NOTES FOR EMPLOYERS" section,
  and a "COMPARISON WITH OTHER STATE LAWS" section — none of which appear in
  verbatim statute. Its section list (551.001/051/101/102/201/301) is
  non-contiguous and almost certainly omits real sections.
- Neither source is usable for section existence.

## Why this matters for the metric

`student_section_exists` (real-but-wrong vs fabricated misgrounding) and the
`v_halluc` validity check both depend on a trustworthy "does this section exist?"
oracle. An index built from an incomplete or summarized source produces **false
"fabricated" verdicts** for sections that are real but absent from the source
(e.g. §5-301). The gate is deliberately conservative: with any source flagged,
`make_section_exists_fn` returns `None`, so `compute_discrepancies` runs with
`section_exists_fn=None` and the subtype stays unset rather than wrong.

Separately, this audit shows the **teacher's statute context itself contained
AI-introduced errors** (fabricated §20-875, mislabeled §20-873/874, invented
§20-871(d), omitted CO §1705/1707), which is why Task 3c saw teacher rules citing
sections like §20-875. This is a data-quality caveat for any analysis that treats
the teacher graph as ground truth.

## Blast radius (where the contamination spread)

The root cause is the `.txt` study aids, but the errors did **not** stay there —
the teacher consumed the `.txt` files (not the PDFs) at extraction time, so the
**frozen teacher reference graphs carry the fabrications**:

- **Fabricated NYC §20-875** appears in the teacher graphs for **E1, E2, and H1**
  (`grep 20-875 data/outputs/graphs/{E1,E2,H1}_reference.json`).
- The teacher also uses the study-aid's **mislabeled §20-873** (the real §20-873 is
  Enforcement; the `.txt` labels it "Public Disclosure").

Consequences: (a) two mined patches instructed students to cite §20-875 — now
classified `fabricated` and quarantined from verified retrieval; (b) on NYC rules
L-GED can *reward* reproducing the fabrication; (c) some `v_misground` flags mark a
student that was right against a teacher that was wrong.

**Teacher re-extraction is deferred pending Prof. Rao's decision** (it would reset
every baseline). The `v_misground` semantics are intentionally left unchanged for
the same reason — we flag counts, not silently "fix" them. Until then, the
citation-verification classifier + verified-only retrieval keep the fabrication out
of the patch pipeline, and `docs/BASELINE_PROVENANCE.md` + the Task-4 delta audit
record which recovered rules rest on unverifiable authorities.

## To make the index trustworthy

1. Source the **NYC DCWP Final Rules** (6 RCNY §5-300 et seq.) and the **HB 149
   enrolled** TRAIGA text (not the House Journal). Confirm verbatim, not summaries.
2. Extract section tokens (`pdftotext` + the `extract_citation_tokens` regex).
3. Add them under `sections`; flip `nyc_dcwp_rules` and `tx_traiga` provenance to
   `verbatim` and `nyc_ll144` to `verbatim` once the DCWP gap is filled.
4. `trustworthy` becomes True; `make_section_exists_fn` returns a live function;
   re-run discrepancy analysis to backfill `student_section_exists` and enable the
   `v_halluc` validity check (Task 3b).
