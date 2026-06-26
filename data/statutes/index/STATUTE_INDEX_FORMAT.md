# Statute section index — format & provenance

`statute_index.json` answers one question per citation: **does this statutory
section actually exist?** It backs the `v_halluc` validity check (a rule citing
no real section is a hallucination) and the misgrounding subtype flag
(`student_section_exists`: real-but-wrong vs fabricated).

## Format

```json
{
  "provenance": { "<statute_key>": "verbatim | statute-only | summary | MISSING | WRONG-FILE | unconfirmed" },
  "sections":   { "<statute_key>": ["6-1-1701(2)", "6-1-1703(2)(a)", ...] }
}
```

- **`sections`** maps each statute to the canonical section tokens it contains.
  Tokens should be in the same shape `alignment.extract_citation_tokens` emits
  (e.g. `6-1-1703(2)(a)`, `20-871(b)`), so the index and the citations being
  checked tokenize identically. `load_statute_index` re-tokenizes each entry, so
  listing either `§6-1-1701` or `6-1-1701` works.
- **`provenance`** records, per statute, whether the source text is trustworthy.

## The provenance gate (why this matters)

`StatuteIndex.trustworthy` is **False** if any source is `MISSING`, `WRONG-FILE`,
`statute-only`, `summary`, or `unconfirmed`. `make_section_exists_fn(index)`
returns `None` for an untrustworthy index, so `compute_discrepancies` is called
with `section_exists_fn=None` and the misgrounding subtype stays unset. This is
deliberate: a "section does not exist" verdict from an incomplete index is a
false hallucination flag.

Current corpus state (independently audited against `data/statutes/*.pdf` —
section tokens extracted with `pdftotext`; see `PROVENANCE_AUDIT.md`):

| statute | authoritative source | status | sections |
|---|---|---|---|
| CO AIA | `2024a_205_signed-act.pdf` (26pp) | **verbatim** ✓ | 6-1-1701..1707 (all 7 confirmed in PDF, incl. 1705, 1707) |
| NYC LL144 | `Legislation Text.pdf` (4pp, Int. 1894-A) | statute-only | 20-870, 871, 872, 873, 874 (**no 20-875**) |
| NYC DCWP rules | — | **MISSING** | teacher cites 6 RCNY §5-300..5-303 |
| TX TRAIGA | `89RDAY81FINAL.pdf` | **WRONG-FILE / summary** | House Journal, not the statute |

**Important — the `.txt` files in `data/statutes/` are AI-assisted study aids, not
verbatim statute, and are NOT used to build the index.** Independent audit found:
the CO `.txt` omits real sections 6-1-1705/1707; the NYC `.txt` fabricates a
§20-875 and mislabels §20-873/874 (and invents §20-871(d)); the TX `.txt` is a
summary with cross-state commentary. The index is built only from the authoritative
PDFs (CO, NYC LL144). This **corrects** the earlier fixture, which stopped NYC at
20-872 and missed 20-873/874.

`statute_index.json` encodes this state: CO and the NYC LL144 statute are populated
from their verbatim PDFs; the provenance block marks NYC DCWP rules MISSING, NYC
LL144 statute-only (its citation space also needs the DCWP rules), and TX as a
summary — so `trustworthy` is False and the gate keeps the index from driving hard
verdicts until the DCWP rules and the real HB 149 enrolled text are sourced.

## To make the index trustworthy

1. Source the NYC DCWP Final Rules text (6 RCNY §5-300 et seq.) and the actual
   **HB 149 enrolled** TRAIGA text (not the House Journal). Confirm CO/NYC/TX are
   verbatim, not AI summaries.
2. Extract section tokens from each (the `pdf` skill / pdfplumber; the citation
   regex in `alignment.py` already knows the section-number shape).
3. Add them under `sections`, flip each `provenance` entry to `verbatim`.
4. `trustworthy` becomes True; `make_section_exists_fn` returns a live function;
   re-run discrepancy analysis to backfill `student_section_exists` and enable
   the `v_halluc` validity check.
