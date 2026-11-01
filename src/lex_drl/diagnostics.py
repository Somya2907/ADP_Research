"""Diagnostics: why do patches barely move the small model?

Three explanations are mixed together in the Phase 5 result:

* **content** — the patch does not carry what the student is missing;
* **delivery** — the right patch is not retrieved, or the student ignores it;
* **capacity** — a 3B model writing JSON cannot add many nodes, whatever it is told.

This module holds the pieces that pull them apart: the L-GED ceiling patches
could reach, a teacher graph with its fabricated citations removed, a retrieval
audit, and the notes for the diagnostic arms (placebo, oracle, directive,
LLM-written). Oracle notes are mined from a test case's *own* teacher gaps, so
they are an upper bound and never a method result.
"""
from __future__ import annotations

import dataclasses
import random
from typing import Iterable, Optional

from .alignment import AlignmentReport, extract_citation_tokens
from .cases import Case
from .discrepancy import DiscrepancyReport
from .loop import patch_targets
from .patch_generator import (
    _canon_jurisdiction, base_section, canonical_citation, dedup_merge, generate_patches,
)
from .patch_store import Patch
from .schema import LegalReasoningGraph

# The six test cases the diagnostic arms run on: the original E2/M2/H2 plus, per
# tier, the other test case closest to that tier's median round-0 L-GED.
SUBSET = ["E2", "E8", "M2", "M9", "H2", "H10"]


# ──────────────────────────────────────────────
# Citation normalisation
# ──────────────────────────────────────────────

def collapse_counts(patches: Iterable[Patch]) -> dict[str, int]:
    """How many distinct patches the store has under each notion of 'same patch'."""
    patches = list(patches)
    exact = {(p.patch_family, frozenset(extract_citation_tokens(p.controlling_authority)
                                        or {p.controlling_authority.strip().lower()}))
             for p in patches}
    canon = {(p.patch_family, canonical_citation(p.controlling_authority, p.jurisdiction)
              or frozenset({p.controlling_authority.strip().lower()}))
             for p in patches}
    sections = set()
    for p in patches:
        sections |= canonical_citation(p.controlling_authority, p.jurisdiction)
    return {"patches": len(patches), "distinct_exact": len(exact),
            "distinct_canonical": len(canon), "distinct_sections": len(sections)}


# ──────────────────────────────────────────────
# Ceiling: what could patches buy at best?
# ──────────────────────────────────────────────

def lged_components(report: DiscrepancyReport) -> dict[str, float]:
    """L-GED split into missing nodes by type, hallucinations and edges."""
    out = {f"miss_{t}": 0.0 for t in "FIRACO"}
    for m in report.v_miss:
        out[f"miss_{m.node_type}"] = out.get(f"miss_{m.node_type}", 0.0) + m.weight
    out["halluc"] = sum(h.weight for h in report.v_halluc)
    out["edges"] = sum(e.weight for e in report.e_diff)
    return out


def ro_ceiling(report: DiscrepancyReport, ns: Iterable[Optional[int]] = (3, 10, None),
               ) -> dict[str, float]:
    """L-GED drop if the student added its n heaviest missing Rule/Obligation nodes.

    ``None`` means all of them. Edges are ignored, so this is the node-only gain.
    """
    weights = sorted((m.weight for m in report.v_miss if m.node_type in ("R", "O")),
                     reverse=True)
    return {("all" if n is None else str(n)): sum(weights if n is None else weights[:n])
            for n in ns}


# ──────────────────────────────────────────────
# Teacher errors
# ──────────────────────────────────────────────

def fabricated_rule_ids(teacher: LegalReasoningGraph, index) -> list[str]:
    if index is None:
        return []
    return [r.rid for r in teacher.rules if index.classify_citation(r.citation) == "fabricated"]


def teacher_without(teacher: LegalReasoningGraph, rule_ids: Iterable[str]) -> LegalReasoningGraph:
    """The teacher graph minus the given rules, the obligations they require,
    and every edge touching a removed node."""
    drop_r = set(rule_ids)
    if not drop_r:
        return teacher
    drop_o = {o.oid for o in teacher.obligations if o.required_by in drop_r}
    gone = drop_r | drop_o
    return teacher.model_copy(update={
        "rules": [r for r in teacher.rules if r.rid not in drop_r],
        "obligations": [o for o in teacher.obligations if o.oid not in drop_o],
        "edges": [e for e in teacher.edges if e.src not in gone and e.dst not in gone],
    })


# ──────────────────────────────────────────────
# Uptake: did the student cite what it was given?
# ──────────────────────────────────────────────

def student_sections(student: LegalReasoningGraph) -> set[str]:
    keys: set[str] = set()
    for r in student.rules:
        keys |= canonical_citation(r.citation, r.jurisdiction)
    return keys


def taken_up(patch: Patch, student: LegalReasoningGraph) -> bool:
    """True if the student cites any section the patch is about."""
    return bool(canonical_citation(patch.controlling_authority, patch.jurisdiction)
                & student_sections(student))


def missing_targets(patch: Patch, teacher: LegalReasoningGraph,
                    alignment: AlignmentReport) -> list[str]:
    """Teacher nodes this patch is about that the student did NOT have."""
    out = []
    for t in patch_targets(patch, teacher):
        m = alignment.obligation_map if t.startswith("O") else alignment.rule_map
        if m.get(t) is None:
            out.append(t)
    return out


# ──────────────────────────────────────────────
# Notes for the diagnostic arms
# ──────────────────────────────────────────────

def as_training(case: Case) -> Case:
    """A copy the miner accepts. Only for oracle notes, which are never a result."""
    return dataclasses.replace(case, role="training")


def oracle_selection(case: Case, report: DiscrepancyReport, teacher: LegalReasoningGraph,
                     student: LegalReasoningGraph, k: Optional[int], *, index=None,
                     insight=None) -> list[tuple[Patch, str]]:
    """(patch, teacher node id) for this case's own missing Rule/Obligation nodes.

    Nodes are taken heaviest first and mined one at a time, so every patch has
    exactly one source node; a node whose patch would repeat one already chosen
    is skipped. Fabricated teacher citations are left out (teacher errors, not
    knowledge the student lacks). ``k=None`` takes all of them. With an
    ``insight`` writer the patch text is Claude-written instead of the template.
    """
    ro = sorted((m for m in report.v_miss if m.node_type in ("R", "O")),
                key=lambda m: -m.weight)
    picked: list[tuple[Patch, str]] = []
    seen: set[str] = set()
    for node in ro:
        one = report.model_copy(update={"v_miss": [node], "v_misground": []})
        mined = generate_patches(one, teacher, student, as_training(case),
                                 insight=insight, index=index)
        if not mined or mined[0].patch_id in seen or mined[0].verification == "fabricated":
            continue
        seen.add(mined[0].patch_id)
        picked.append((mined[0], node.teacher_id))
        if k is not None and len(picked) == k:
            break
    return picked


def oracle_patches(case: Case, report: DiscrepancyReport, teacher: LegalReasoningGraph,
                   student: LegalReasoningGraph, k: Optional[int], *, index=None,
                   insight=None) -> list[Patch]:
    """The patches of ``oracle_selection``."""
    return [p for p, _ in oracle_selection(case, report, teacher, student, k,
                                           index=index, insight=insight)]


def directive_notes(node_ids: list[str], teacher: LegalReasoningGraph) -> str:
    """Teacher nodes worded as a checklist the answer must contain.

    Given the node ids from ``oracle_selection`` this carries the same content
    as the oracle patches, phrased as requirements instead of advice.
    """
    rules = {r.rid: r for r in teacher.rules}
    obligations = {o.oid: o for o in teacher.obligations}
    lines = []
    for nid in node_ids:
        i = len(lines) + 1
        if nid in rules:
            node = rules[nid]
            lines.append(f"{i}. A Rule node with citation \"{node.citation}\" "
                         f"({_canon_jurisdiction(node.jurisdiction)}, "
                         f"{node.authority.value}): {node.label}.")
        elif nid in obligations:
            node = obligations[nid]
            req = rules.get(node.required_by)
            cite = req.citation if req else node.required_by
            deadline = f" Deadline: {node.deadline}." if node.deadline else ""
            lines.append(f"{i}. An Obligation node ({node.status.value}, required by "
                         f"{cite}): {node.label}.{deadline}")
    if not lines:
        return ""
    head = ("REQUIRED ELEMENTS — your JSON graph must contain each of these, each "
            "with an Application node that applies it to the facts:")
    return "\n".join([head, *lines, ""])


def placebo_patches(case: Case, teacher: LegalReasoningGraph, store: Iterable[Patch],
                    k: int = 3, seed: int = 0) -> list[Patch]:
    """k real store patches that have nothing to do with this case.

    A patch qualifies if it targets no node of this case's teacher graph and
    shares no section with it. Off-jurisdiction patches are preferred; the
    choice is seeded so a re-run picks the same notes.
    """
    case_sections = set()
    for r in teacher.rules:
        case_sections |= canonical_citation(r.citation, r.jurisdiction)
    juris = {_canon_jurisdiction(t) for t in case.jurisdiction_tags}
    pool = [p for p in store
            if p.verification != "fabricated"
            and not patch_targets(p, teacher)
            and not (canonical_citation(p.controlling_authority, p.jurisdiction) & case_sections)]
    off = [p for p in pool if p.jurisdiction not in juris]
    rng = random.Random(f"{seed}:{case.case_id}")
    picked: list[Patch] = []
    seen: set[frozenset] = set()
    for group in (off, [p for p in pool if p not in off]):
        group = sorted(group, key=lambda p: p.patch_id)
        rng.shuffle(group)
        for p in group:
            key = canonical_citation(p.controlling_authority, p.jurisdiction)
            if key in seen:
                continue
            seen.add(key)
            picked.append(p)
            if len(picked) == k:
                return picked
    return picked


__all__ = [
    "SUBSET", "base_section", "canonical_citation", "collapse_counts",
    "lged_components", "ro_ceiling", "fabricated_rule_ids", "teacher_without",
    "student_sections", "taken_up", "missing_targets", "as_training",
    "oracle_selection", "oracle_patches", "directive_notes", "placebo_patches",
]
