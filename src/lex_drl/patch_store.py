"""JSON-backed patch store with BM25 retrieval over trigger keywords.

The store holds :class:`Patch` objects mined by ``patch_generator`` from the
training cases and retrieves the top-k most relevant patches for a new case at
inference time. Retrieval is lexical (BM25 over ``trigger_keywords``), matching
the clinical DRL design (Liu et al. 2026, Phase 4).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, Literal, Optional

from pydantic import BaseModel, Field

PatchFamily = Literal["missing_rule", "missing_obligation", "misgrounding"]
Verification = Literal["verified", "unverified", "fabricated"]

_TOKEN = re.compile(r"[A-Za-z0-9][\w\-§().]*")


def _tokenize(text: str) -> list[str]:
    """Lowercase word/citation tokenizer shared by indexing and querying."""
    return [t.lower() for t in _TOKEN.findall(text or "")]


class Patch(BaseModel):
    """A reusable, rule-level correction mined from a training discrepancy."""

    patch_id: str
    patch_family: PatchFamily
    trigger_keywords: list[str] = Field(default_factory=list)
    controlling_authority: str
    prevention_step: str
    contraindication: str = ""
    node_types_addressed: list[str] = Field(default_factory=list)
    source_cases: list[str] = Field(default_factory=list)
    jurisdiction: str = ""
    # Set at mining time from StatuteIndex.classify_citation(controlling_authority).
    # "unverified" when no index was supplied at mining time (back-compat default).
    verification: Verification = "unverified"

    def index_text(self) -> str:
        """The text BM25 indexes for this patch."""
        return " ".join(self.trigger_keywords)


class PatchStore:
    """In-memory store with JSON persistence and BM25 retrieval."""

    def __init__(self) -> None:
        self._patches: dict[str, Patch] = {}
        self._bm25 = None  # lazily (re)built
        self._corpus_ids: list[str] = []

    # ── mutation ──────────────────────────────────────────────
    def add(self, patch: Patch) -> None:
        """Insert or replace a patch by ``patch_id`` (idempotent upsert)."""
        self._patches[patch.patch_id] = patch
        self._bm25 = None  # invalidate index

    def populate_from_candidates(self, candidates: Iterable[Patch]) -> int:
        """Bulk upsert generator output. Returns the new store size."""
        for p in candidates:
            self.add(p)
        return len(self._patches)

    # ── access ────────────────────────────────────────────────
    def __len__(self) -> int:
        return len(self._patches)

    def all(self) -> list[Patch]:
        return list(self._patches.values())

    def get(self, patch_id: str) -> Optional[Patch]:
        return self._patches.get(patch_id)

    # ── retrieval ─────────────────────────────────────────────
    def _ensure_index(self) -> None:
        if self._bm25 is not None:
            return
        from rank_bm25 import BM25Okapi

        self._corpus_ids = list(self._patches.keys())
        tokenized = [_tokenize(self._patches[pid].index_text()) for pid in self._corpus_ids]
        # BM25Okapi requires a non-empty corpus; guard the empty case.
        self._bm25 = BM25Okapi(tokenized) if tokenized else None

    def retrieve(
        self,
        query: str,
        k: int = 3,
        allowed: "set[str] | frozenset[str]" = frozenset({"verified"}),
        jurisdictions: "set[str] | None" = None,
    ) -> list[Patch]:
        """Return the top-k patches most relevant to ``query`` (raw case text).

        Ranks by BM25 but gates on actual token overlap. The overlap gate matters
        because the store is small: in a tiny corpus BM25's IDF collapses to zero
        for terms appearing in ~half the patches, so a pure ``score > 0`` filter
        would discard valid matches. Patches with no keyword overlap are dropped,
        so an off-topic query returns fewer than k (or zero) rather than noise.

        ``allowed`` restricts retrieval to patches with those ``verification``
        statuses (default: verified-only). ``jurisdictions`` (canonical, e.g.
        {"nyc"}), when given, restricts to those patch jurisdictions. Both filters
        apply *before* ranking, so a quarantined/off-jurisdiction patch is never
        returned even when it is the top BM25 hit.
        """
        self._ensure_index()
        if not self._corpus_ids:
            return []
        q_tokens = _tokenize(query)
        q_set = set(q_tokens)
        scores = (self._bm25.get_scores(q_tokens) if self._bm25 is not None
                  else [0.0] * len(self._corpus_ids))
        scored: list[tuple[str, float, int]] = []
        for pid, bm in zip(self._corpus_ids, scores):
            patch = self._patches[pid]
            if patch.verification not in allowed:
                continue  # quarantine filter (before ranking)
            if jurisdictions is not None and patch.jurisdiction not in jurisdictions:
                continue  # jurisdiction pre-filter
            kw_tokens = set(_tokenize(patch.index_text()))
            overlap = len(q_set & kw_tokens)
            if overlap == 0:
                continue
            scored.append((pid, float(bm), overlap))
        scored.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return [self._patches[pid] for pid, _, _ in scored[:k]]

    # ── persistence ───────────────────────────────────────────
    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [p.model_dump() for p in self._patches.values()]
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def load(self, path: str | Path) -> "PatchStore":
        path = Path(path)
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            for item in raw:
                patch = Patch.model_validate(item)
                self._patches[patch.patch_id] = patch
            self._bm25 = None
        return self

    @classmethod
    def from_file(cls, path: str | Path) -> "PatchStore":
        return cls().load(path)


__all__ = ["Patch", "PatchStore", "PatchFamily"]
