"""Tests for patch_store: Patch model, BM25 retrieval, JSON round-trip."""
from __future__ import annotations

from lex_drl.patch_store import Patch, PatchStore


def _patch(pid, kws, authority, family="missing_rule"):
    return Patch(
        patch_id=pid, patch_family=family, trigger_keywords=kws,
        controlling_authority=authority, prevention_step="do the thing",
        node_types_addressed=["R"], source_cases=["E1"], jurisdiction="nyc",
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
