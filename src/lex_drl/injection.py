"""Turn retrieved patches into prompt text, and keep training parties out of it.

Shared by the single-pass injection script (``scripts/run_patch_injection.py``)
and the iterative loop (``lex_drl.loop``).
"""
from __future__ import annotations

from typing import Iterable, Optional

from .extraction import PROMPT_DIR
from .patch_store import Patch, PatchStore

# Train→test leakage guard. Patch text is copied from the teacher's node labels,
# so a few patches embed training-case party or product names. Injecting those
# into a test prompt would be train→test contamination, so any patch whose text
# names a training-case party is dropped before retrieval.
#
# This fixed list covers the original three training cases (E1/M1/H1) and is the
# default so the Phase 2–4 scripts behave exactly as before. The loop passes the
# ``parties`` declared in every training case file instead (``training_party_names``).
TRAIN_PARTY_NAMES = [
    "HireFlow", "Greenleaf", "ResumeRank", "TalentMetrics",   # E1
    "LoanScore", "Denver",                                    # M1
    "PeopleScore",                                            # H1
]


def training_party_names() -> list[str]:
    """Every party named in the metadata of a training case."""
    from .cases import cases_by_role

    names: list[str] = []
    for case in cases_by_role("training"):
        names.extend(case.parties)
    return sorted(set(names))


def has_party_leak(patch: Patch, party_names: Optional[Iterable[str]] = None) -> bool:
    names = TRAIN_PARTY_NAMES if party_names is None else party_names
    text = f"{patch.prevention_step} {patch.contraindication}".lower()
    return any(name.lower() in text for name in names)


def filter_leaks(
    store: PatchStore, party_names: Optional[Iterable[str]] = None,
) -> tuple[PatchStore, list[Patch]]:
    """Return (clean_store, dropped) — patches naming a training-case party removed."""
    names = list(TRAIN_PARTY_NAMES if party_names is None else party_names)
    clean, dropped = PatchStore(), []
    for p in store.all():
        (dropped.append(p) if has_party_leak(p, names) else clean.add(p))
    return clean, dropped


def render_notes_block(patches: list[Patch]) -> str:
    """Render retrieved patches as a compact POLICY REASONING NOTES block."""
    if not patches:
        return ""
    lines = ["POLICY REASONING NOTES (apply only where the facts trigger them):"]
    for i, p in enumerate(patches, 1):
        note = f"{i}. {p.prevention_step}"
        if p.contraindication:
            note += f" [Caveat: {p.contraindication}]"
        lines.append(note)
    lines.append("")  # trailing blank line before CASE
    return "\n".join(lines)


def build_patched_system(case, notes_block: str) -> str:
    template = (PROMPT_DIR / "agent_firaco.txt").read_text(encoding="utf-8")
    system = (
        template
        .replace("<<CASE_FACTS>>", case.facts)
        .replace("<<CASE_QUESTION>>", case.question)
    )
    if notes_block:
        # Insert before the CASE section so the persona/intro stays first.
        system = system.replace("CASE:", notes_block + "\nCASE:", 1)
    return system


__all__ = [
    "TRAIN_PARTY_NAMES", "training_party_names", "has_party_leak", "filter_leaks",
    "render_notes_block", "build_patched_system",
]
