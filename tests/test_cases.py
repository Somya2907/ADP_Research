"""The case corpus must stay a balanced 30-case benchmark.

Guards the contract the patch loop depends on: at least ten cases per tier,
a 5/5 train/test split in each tier, complete metadata, and unique parties
(so the train→test leakage guard can work from the ``parties`` field).
"""
from __future__ import annotations

from collections import Counter

import pytest

from lex_drl.cases import CASES_DIR, TIERS, case_census, cases_by_role, load_all_cases

# Whole-file word counts (metadata + facts + question), per tier.
WORD_BANDS = {"easy": (280, 460), "medium": (360, 560), "hard": (520, 820)}
KNOWN_JURISDICTIONS = {"NYC", "CO", "TX"}


@pytest.fixture(scope="module")
def cases():
    return load_all_cases()


def test_at_least_ten_cases_per_tier(cases):
    per_tier = Counter(c.tier for c in cases)
    for tier in TIERS:
        assert per_tier[tier] >= 10, f"{tier}: only {per_tier[tier]} cases"


def test_five_train_five_test_per_tier():
    census = case_census()
    for tier in TIERS:
        assert census[tier].get("training", 0) == 5, (tier, census[tier])
        assert census[tier].get("test", 0) == 5, (tier, census[tier])


def test_original_six_keep_their_roles(cases):
    roles = {c.case_id: c.role for c in cases}
    for cid in ("E1", "M1", "H1"):
        assert roles[cid] == "training"
    for cid in ("E2", "M2", "H2"):
        assert roles[cid] == "test"


def test_metadata_is_complete(cases):
    for c in cases:
        assert c.tier in TIERS, c.case_id
        assert c.role in ("training", "test"), c.case_id
        assert c.case_id[0] == {"easy": "E", "medium": "M", "hard": "H"}[c.tier], c.case_id
        assert c.jurisdiction_tags and set(c.jurisdiction_tags) <= KNOWN_JURISDICTIONS, c.case_id
        assert c.doctrinal_area, c.case_id
        assert c.facts.strip() and c.question.strip(), c.case_id
        assert c.parties, f"{c.case_id}: no parties (leakage guard needs them)"


def test_ids_are_unique_and_ordered(cases):
    ids = [c.case_id for c in cases]
    assert len(ids) == len(set(ids))
    assert ids[:3] == ["E1", "E2", "E3"]          # numeric, not lexical, order
    assert "E10" in ids and ids.index("E10") > ids.index("E9")


def test_no_party_is_shared_between_cases(cases):
    seen: dict[str, str] = {}
    for c in cases:
        for p in c.parties:
            key = p.lower()
            assert key not in seen, f"party {p!r} in both {seen.get(key)} and {c.case_id}"
            seen[key] = c.case_id


def test_parties_actually_appear_in_the_facts(cases):
    for c in cases:
        for p in c.parties:
            assert p.lower() in c.facts.lower(), f"{c.case_id}: party {p!r} not in facts"


def test_word_counts_fit_the_tier(cases):
    for c in cases:
        path = next(CASES_DIR.glob(f"{c.case_id}_*.md"))
        n = len(path.read_text(encoding="utf-8").split())
        lo, hi = WORD_BANDS[c.tier]
        assert lo <= n <= hi, f"{c.case_id} ({c.tier}): {n} words, expected {lo}-{hi}"


def test_cases_by_role_partitions_the_corpus(cases):
    train, test = cases_by_role("training"), cases_by_role("test")
    assert len(train) == 15 and len(test) == 15
    assert {c.case_id for c in train}.isdisjoint({c.case_id for c in test})
    assert len(train) + len(test) == len(cases)
