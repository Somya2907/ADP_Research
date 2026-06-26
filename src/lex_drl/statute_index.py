"""Statute-section index: which statutory sections actually exist.

Used by (a) the ``v_halluc`` validity check — a student Rule citing no real
section is a hallucination — and (b) the misgrounding subtype flag
(``student_section_exists``: real-but-wrong vs fabricated).

IMPORTANT — provenance gate
---------------------------
The index is only as trustworthy as its source text. Two known issues in the
current corpus (confirmed by inspection of ``data/statutes/*.pdf``):

* The TX file (``89RDAY81FINAL.pdf``) is a House *Journal* (floor proceedings /
  roll call), NOT the HB 149 enrolled statute. A TX index built from it is
  unreliable.
* The NYC file (``Legislation Text.pdf``) is the 4-page Local Law 144 statute
  only; it omits the DCWP Final Rules (6 RCNY §5-300 et seq.) that the teacher
  graph cites. Sections like §5-301 would be wrongly flagged "does not exist".

Until the corpus is corrected and confirmed verbatim, callers should treat a
"section does not exist" verdict as *advisory*, and ``compute_discrepancies``
should be called with ``section_exists_fn=None`` (leaving the misgrounding
subtype unset) rather than trusting a partial index.

Index file format (``data/statutes/index/statute_index.json``)
--------------------------------------------------------------
A JSON object mapping a statute key to the canonical section tokens it contains,
plus a ``provenance`` block recording source + verbatim confirmation::

    {
      "provenance": {"co_aia": "verbatim", "nyc_ll144": "statute-only",
                     "nyc_dcwp_rules": "MISSING", "tx_traiga": "WRONG-FILE"},
      "sections": {
        "co_aia":   ["6-1-1701", "6-1-1701(2)", "6-1-1703(2)(a)", ...],
        "nyc_ll144": ["20-870", "20-871", "20-871(a)", "20-872", ...]
      }
    }

Tokens are produced by ``alignment.extract_citation_tokens`` so the index and
the citations being checked tokenize identically.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .alignment import extract_citation_tokens

DEFAULT_INDEX_PATH = Path("data/statutes/index/statute_index.json")


class StatuteIndex:
    """A set of known-good section tokens, with provenance metadata."""

    def __init__(self, sections: set[str], provenance: dict[str, str] | None = None):
        self._sections = sections
        self.provenance = provenance or {}

    @property
    def trustworthy(self) -> bool:
        """True only if every declared source is verbatim/complete.

        If any source is MISSING / WRONG-FILE / statute-only / summary, the
        index should not drive hard "does not exist" verdicts.
        """
        bad = {"MISSING", "WRONG-FILE", "statute-only", "summary", "unconfirmed"}
        return bool(self.provenance) and not (set(self.provenance.values()) & bad)

    def section_exists(self, citation: str) -> bool:
        """True iff any canonical token in ``citation`` is a known section."""
        return bool(extract_citation_tokens(citation) & self._sections)

    def __len__(self) -> int:
        return len(self._sections)


def load_statute_index(path: str | Path = DEFAULT_INDEX_PATH) -> Optional[StatuteIndex]:
    """Load the statute index, or return ``None`` if it isn't present yet.

    Returning ``None`` (rather than raising) lets the pipeline run before the
    corpus/provenance work is done: callers pass ``section_exists_fn=None`` and
    misgrounding detection still works (it is index-independent), leaving only
    the real-but-wrong vs fabricated subtype unset.
    """
    path = Path(path)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    tokens: set[str] = set()
    for section_list in data.get("sections", {}).values():
        tokens |= {t for s in section_list for t in extract_citation_tokens(f"§{s}")}
        tokens |= set(section_list)  # also accept raw tokens as listed
    return StatuteIndex(tokens, provenance=data.get("provenance", {}))


def make_section_exists_fn(index: Optional[StatuteIndex], *, require_trustworthy: bool = True):
    """Return a ``citation -> bool`` callable, or ``None`` if unsafe to use.

    When ``require_trustworthy`` and the index provenance is incomplete, returns
    ``None`` so callers fall back to ``section_exists_fn=None``.
    """
    if index is None:
        return None
    if require_trustworthy and not index.trustworthy:
        return None
    return index.section_exists


__all__ = ["StatuteIndex", "load_statute_index", "make_section_exists_fn", "DEFAULT_INDEX_PATH"]
