"""Tests for statute_index: loading, section_exists, and the provenance gate.

Unit tests use synthetic tmp index files. One integration test checks the real
data/statutes/index/statute_index.json if present.
"""
from __future__ import annotations

import json
from pathlib import Path

from lex_drl.statute_index import (
    DEFAULT_INDEX_PATH,
    StatuteIndex,
    load_statute_index,
    make_section_exists_fn,
)


def _write_index(path: Path, provenance: dict, sections: dict,
                 family_prefixes: dict | None = None) -> None:
    payload = {"provenance": provenance, "sections": sections}
    if family_prefixes is not None:
        payload["family_prefixes"] = family_prefixes
    path.write_text(json.dumps(payload))


def _corpus_index(tmp_path: Path):
    """An index mirroring the real corpus for classify_citation tests."""
    p = tmp_path / "idx.json"
    _write_index(
        p,
        {"co_aia": "verbatim", "nyc_ll144": "statute-only"},
        {
            "co_aia": ["6-1-1701", "6-1-1702", "6-1-1703", "6-1-1703(2)(a)",
                       "6-1-1704", "6-1-1705", "6-1-1706", "6-1-1707"],
            "nyc_ll144": ["20-870", "20-871", "20-871(a)", "20-871(b)",
                          "20-872", "20-872(a)", "20-873", "20-874"],
        },
        family_prefixes={"co_aia": "6-1-17", "nyc_ll144": "20-87"},
    )
    return load_statute_index(p)


def test_classify_ancestor_rule_subsubdivision_is_verified(tmp_path):
    """The ancestor rule: a real sub-subdivision resolves via its parent section."""
    idx = _corpus_index(tmp_path)
    assert idx.classify_citation("§20-871(a)(1)") == "verified"   # ancestor 20-871(a)
    assert idx.classify_citation("§6-1-1703(2)(a)") == "verified"


def test_classify_fabricated_real_and_unverified(tmp_path):
    idx = _corpus_index(tmp_path)
    assert idx.classify_citation("NYC LL 144 §20-875") == "fabricated"  # in 20-87, not in list
    assert idx.classify_citation("§20-872(a)") == "verified"
    assert idx.classify_citation("§5-301") == "unverified"              # DCWP, no family
    assert idx.classify_citation("Texas TRAIGA §551.201") == "unverified"


def test_classify_multi_citation_is_worst_of(tmp_path):
    idx = _corpus_index(tmp_path)
    assert idx.classify_citation("§20-871(a)(1); DCWP §5-301(a)") == "unverified"
    assert idx.classify_citation("§20-875; §5-301") == "fabricated"


def test_classify_handles_truncated_authority_and_empty(tmp_path):
    idx = _corpus_index(tmp_path)
    assert idx.classify_citation("CO AIA §6-1-1703(2)(a)-(") == "verified"
    assert idx.classify_citation("") == "unverified"


def test_classify_range_citations_resolve_to_base_section(tmp_path):
    """Range/compound citations must resolve to their real base section, not
    be mis-flagged fabricated (regression: 6-1-1703(2)(a)-(g))."""
    idx = _corpus_index(tmp_path)
    assert idx.classify_citation("CO AIA §6-1-1703(2)(a)-(g)") == "verified"
    assert idx.classify_citation("Colorado AIA Section 6-1-1702(2)-(3)") == "verified"
    assert idx.classify_citation("§6-1-1703(2)(f)-(g)") == "verified"


def test_load_missing_file_returns_none(tmp_path):
    assert load_statute_index(tmp_path / "nope.json") is None


def test_section_exists_real_vs_fabricated(tmp_path):
    p = tmp_path / "idx.json"
    _write_index(p, {"co_aia": "verbatim"}, {"co_aia": ["6-1-1705", "6-1-1707"]})
    idx = load_statute_index(p)
    # Real sections (with the § prefix that real citations carry) resolve True.
    assert idx.section_exists("Colo. Rev. Stat. §6-1-1705") is True
    assert idx.section_exists("§6-1-1707") is True
    # A section not in the index is False (fabricated / unknown).
    assert idx.section_exists("§6-1-1799") is False


def test_trustworthy_true_only_when_all_verbatim(tmp_path):
    p = tmp_path / "idx.json"
    _write_index(p, {"co_aia": "verbatim", "nyc_ll144": "verbatim"}, {"co_aia": ["6-1-1701"]})
    assert load_statute_index(p).trustworthy is True


def test_trustworthy_false_when_any_source_flagged(tmp_path):
    p = tmp_path / "idx.json"
    _write_index(
        p,
        {"co_aia": "verbatim", "nyc_dcwp_rules": "MISSING", "tx_traiga": "summary"},
        {"co_aia": ["6-1-1701"]},
    )
    assert load_statute_index(p).trustworthy is False


def test_gate_blocks_untrustworthy_index(tmp_path):
    p = tmp_path / "idx.json"
    _write_index(p, {"co_aia": "verbatim", "nyc_dcwp_rules": "MISSING"}, {"co_aia": ["6-1-1701"]})
    idx = load_statute_index(p)
    # Default require_trustworthy: an incomplete corpus must NOT drive verdicts.
    assert make_section_exists_fn(idx) is None
    # But the data is still queryable when the caller opts out of the gate.
    fn = make_section_exists_fn(idx, require_trustworthy=False)
    assert callable(fn) and fn("§6-1-1701") is True


def test_gate_returns_callable_for_trustworthy_index(tmp_path):
    p = tmp_path / "idx.json"
    _write_index(p, {"co_aia": "verbatim"}, {"co_aia": ["6-1-1701"]})
    fn = make_section_exists_fn(load_statute_index(p))
    assert callable(fn) and fn("§6-1-1701") is True


def test_real_index_is_loadable_and_gated():
    """The shipped index loads, knows the PDF-verified sections, rejects the
    .txt-fabricated §20-875, and is correctly gated (DCWP missing / TX summary)."""
    if not DEFAULT_INDEX_PATH.exists():
        return  # skip silently if corpus not present
    idx = load_statute_index()
    assert idx is not None
    assert idx.section_exists("NYC Admin. Code §20-873") is True   # real (fixture missed it)
    assert idx.section_exists("NYC Admin. Code §20-875") is False  # .txt fabrication
    assert idx.section_exists("Colo. Rev. Stat. §6-1-1705") is True  # .txt omitted it
    assert idx.trustworthy is False        # DCWP MISSING + TX summary
    assert make_section_exists_fn(idx) is None
