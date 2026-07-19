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
import re
from pathlib import Path
from typing import Optional

from .alignment import extract_citation_tokens

DEFAULT_INDEX_PATH = Path("data/statutes/index/statute_index.json")

# Verdict severity for the "worst-of" rule across a multi-citation authority.
_VERDICT_RANK = {"verified": 0, "unverified": 1, "fabricated": 2}


def _clean_token(token: str) -> str:
    """Strip trailing junk from a citation token.

    ``extract_citation_tokens`` can emit truncated tokens like
    ``6-1-1703(2)(a)-(`` (from malformed controlling-authority strings). Trailing
    chars that aren't a digit, letter, or closing paren are noise.
    """
    return re.sub(r"[^0-9a-z)]+$", "", token)


def _strip_one_paren(token: str) -> Optional[str]:
    """Remove the last balanced ``(...)`` group, or return None if there is none."""
    if not token.endswith(")"):
        return None
    depth = 0
    for i in range(len(token) - 1, -1, -1):
        if token[i] == ")":
            depth += 1
        elif token[i] == "(":
            depth -= 1
            if depth == 0:
                return token[:i]
    return None


def _ancestors(token: str) -> list[str]:
    """``token`` plus every ancestor obtained by stripping trailing ``(...)`` groups.

    ``20-871(a)(1)`` -> ``["20-871(a)(1)", "20-871(a)", "20-871"]``. Also adds the
    bare section number (everything before the first ``(``) so range/compound
    citations like ``6-1-1703(2)(a)-(g)`` still resolve to their real base
    section (``6-1-1703``) rather than being mis-flagged fabricated.
    """
    out = [token]
    cur = token
    while True:
        parent = _strip_one_paren(cur)
        if parent is None or parent == cur:
            break
        out.append(parent)
        cur = parent
    base = cur.split("(")[0].rstrip("-.")  # robust base for ranges/compounds
    if base and base not in out:
        out.append(base)
    return out


def _base_section(token: str) -> str:
    """Strip ALL trailing ``(...)`` subdivisions -> the base section number."""
    return _ancestors(token)[-1]


class StatuteIndex:
    """Known-good section tokens + provenance, with citation classification."""

    def __init__(
        self,
        sections: set[str],
        provenance: dict[str, str] | None = None,
        *,
        section_lists: dict[str, list[str]] | None = None,
        family_prefixes: dict[str, str] | None = None,
    ):
        self._sections = sections
        self.provenance = provenance or {}
        self._section_lists = section_lists or {}
        # statute_key -> section-number prefix of that verbatim family
        # (e.g. {"co_aia": "6-1-17", "nyc_ll144": "20-87"}). A citation whose base
        # section matches one of these prefixes can be verified or fabricated;
        # a citation matching none is unverifiable (DCWP 5-3xx, TX 551.x).
        self._family_prefixes = family_prefixes or {}

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

    # ── citation verification (NOT gated on trustworthy) ──────────────
    def _classify_token(self, token: str) -> str:
        token = _clean_token(token)
        if not token:
            return "unverified"
        base = _base_section(token)
        in_family = any(base.startswith(pref) for pref in self._family_prefixes.values())
        if not in_family:
            return "unverified"  # outside every verbatim family (DCWP, TX)
        # Ancestor rule: verified if the token or any ancestor is a known section.
        if any(a in self._sections for a in _ancestors(token)):
            return "verified"
        return "fabricated"  # base is in a verbatim family's range but not in its list

    def classify_citation(self, citation: str) -> str:
        """Classify an authority string as verified / fabricated / unverified.

        A multi-citation authority ("§20-871(a); DCWP §5-301") takes the WORST of
        its tokens (fabricated > unverified > verified). Unlike ``section_exists``,
        this is *not* gated on ``trustworthy`` — it reports what the verbatim
        section lists can and cannot confirm. Empty/uncited -> "unverified".
        """
        tokens = extract_citation_tokens(citation)
        if not tokens:
            return "unverified"
        return max((self._classify_token(t) for t in tokens),
                   key=lambda v: _VERDICT_RANK[v])

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
    section_lists = data.get("sections", {})
    tokens: set[str] = set()
    for section_list in section_lists.values():
        tokens |= {t for s in section_list for t in extract_citation_tokens(f"§{s}")}
        tokens |= set(section_list)  # also accept raw tokens as listed
    return StatuteIndex(
        tokens,
        provenance=data.get("provenance", {}),
        section_lists=section_lists,
        family_prefixes=data.get("family_prefixes", {}),
    )


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
