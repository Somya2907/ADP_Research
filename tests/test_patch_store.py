"""Tests for patch_store: Patch model, BM25 retrieval, JSON round-trip."""
from __future__ import annotations

from lex_drl.patch_store import Patch, PatchStore


def _patch(pid, kws, authority, family="missing_rule", verification="verified"):
    return Patch(
        patch_id=pid, patch_family=family, trigger_keywords=kws,
        controlling_authority=authority, prevention_step="do the thing",
        node_types_addressed=["R"], source_cases=["E1"], jurisdiction="nyc",
        verification=verification,
    )


def test_roundtrip(tmp_path):
    store = PatchStore()
    store.add(_patch("p1", ["bias audit", "retraining", "nyc"], "§20-871"))
    store.add(_patch("p2", ["impact assessment", "deployer", "colorado"], "§6-1-1703"))
    path = tmp_path / "patches.json"
    store.save(path)
    loaded = PatchStore.from_file(path)
    assert len(loaded) == 2
    assert loaded.get("p1").controlling_authority == "§20-871"


def test_bm25_ranks_relevant_first():
    store = PatchStore()
    store.add(_patch("p1", ["bias", "audit", "retraining", "nyc", "aedt"], "§20-871"))
    store.add(_patch("p2", ["impact", "assessment", "deployer", "colorado"], "§6-1-1703"))
    hits = store.retrieve("company retrained its AEDT and never ran a new bias audit in NYC", k=2)
    assert hits and hits[0].patch_id == "p1"


def test_offtopic_query_returns_nothing():
    store = PatchStore()
    store.add(_patch("p1", ["bias", "audit", "nyc"], "§20-871"))
    assert store.retrieve("xylophone marmalade quantum", k=3) == []


def test_populate_is_idempotent():
    store = PatchStore()
    p = _patch("p1", ["bias", "audit"], "§20-871")
    store.populate_from_candidates([p, p, p])
    assert len(store) == 1


def test_empty_store_retrieve_is_safe():
    assert PatchStore().retrieve("anything", k=3) == []


def test_retrieve_filters_non_verified_before_ranking():
    """A non-verified patch is never returned under the default allowed set,
    even when it is the top BM25 hit."""
    store = PatchStore()
    # p_fab is the strongest lexical match but is fabricated → must be excluded.
    store.add(_patch("p_fab", ["bias", "audit", "retraining", "nyc", "aedt"],
                     "§20-875", verification="fabricated"))
    store.add(_patch("p_ok", ["bias", "audit", "nyc"], "§20-871",
                     verification="verified"))
    hits = store.retrieve("retrained AEDT with no new bias audit in NYC", k=3)
    ids = {h.patch_id for h in hits}
    assert "p_fab" not in ids and "p_ok" in ids
    # Opening the gate lets it back in.
    hits_all = store.retrieve("retrained AEDT with no new bias audit in NYC", k=3,
                              allowed={"verified", "unverified", "fabricated"})
    assert {h.patch_id for h in hits_all} == {"p_fab", "p_ok"}


def test_diversify_surfaces_a_crowded_out_duty():
    """Duty-diversified retrieval surfaces a distinct-duty patch that the standard
    top-k crowds out with near-duplicates for the same subsection."""
    store = PatchStore()
    # three strong matches for the SAME duty (2)(a), one for a different duty (2)(d)
    store.add(_patch("a1", ["deployer", "risk", "management", "colorado"], "CO AIA §6-1-1703(2)(a)"))
    store.add(_patch("a2", ["deployer", "risk", "management", "colorado"], "CO AIA §6-1-1703(2)(a)"))
    store.add(_patch("a3", ["deployer", "risk", "management", "colorado"], "CO AIA §6-1-1703(2)(a)(iii)"))
    store.add(_patch("d1", ["deployer", "risk", "management", "colorado"], "CO AIA §6-1-1703(2)(d)"))
    q = "colorado deployer risk management"
    standard = [p.patch_id for p in store.retrieve(q, k=3, diversify=False)]
    diverse = [p.patch_id for p in store.retrieve(q, k=3, diversify=True)]
    # standard fills all 3 slots with the (2)(a) family; diverse pulls in (2)(d).
    assert "d1" not in standard, f"standard unexpectedly diverse: {standard}"
    assert "d1" in diverse, f"diverse should surface the distinct (2)(d) duty: {diverse}"
    # the two distinct duties come before any repeat (backfill only after)
    from lex_drl.patch_store import _duty_key
    first_two = [_duty_key(store.get(pid).controlling_authority) for pid in diverse[:2]]
    assert len(set(first_two)) == 2, f"first two picks share a duty: {first_two}"


def test_diversify_backfills_when_few_duties():
    """If fewer than k distinct duties clear the gate, diversify backfills to k."""
    store = PatchStore()
    store.add(_patch("a1", ["risk", "management", "colorado"], "CO AIA §6-1-1703(2)(a)"))
    store.add(_patch("a2", ["risk", "management", "colorado"], "CO AIA §6-1-1703(2)(a)"))
    hits = store.retrieve("colorado risk management", k=2, diversify=True)
    assert len(hits) == 2  # only one duty, but backfilled to k
