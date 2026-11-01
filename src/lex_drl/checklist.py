"""Checklist patches: what the student keeps missing, given back as required nodes.

Stage B showed the 3B student uses the right content when it is worded as a
checklist ("your graph must contain a Rule node citing X …": 86% of the given
nodes recovered) and mostly ignores the same content worded as advice. This
module builds that checklist from **training** cases only, so it can be used on
unseen cases.

* An **item** is one teacher Rule or Obligation the unpatched student missed in
  a training case (fabricated citations and labels naming a training party are
  left out).
* Items about the same kind of node and the same statute section are one
  **cluster**. A cluster's **support** is how many training cases missed it —
  the "how often does this gap occur" part of a patch's goodness.
* ``rank`` orders clusters for a new case. ``coverage`` scores a ranking against
  a test case's real gaps (teacher used only for evaluation), so rankers can be
  compared without generating anything.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

from .cases import Case
from .discrepancy import DiscrepancyReport, MissingNode
from .patch_generator import _canon_jurisdiction, canonical_citation
from .schema import LegalReasoningGraph, Obligation, Rule


@dataclass
class Item:
    kind: str                        # "R" | "O"
    citation: str
    jurisdiction: str                # canonical: nyc | colorado | texas
    label: str
    weight: float
    sections: frozenset[str]
    source_case: str
    status: str = ""                 # obligations
    deadline: Optional[str] = None
    authority: str = ""              # rules


@dataclass
class Cluster:
    kind: str
    sections: frozenset[str]
    jurisdiction: str
    items: list[Item] = field(default_factory=list)
    # ── iterative-loop bookkeeping; defaults leave ranking and wording unchanged ──
    given: int = 0            # times shown to a training case
    useful: int = 0           # … where it matched a real teacher node of that case
    resolved: int = 0         # … and the student wrote that node
    priority: float = 0.0     # in [-1, 1]; 0 = untested
    rep: Optional[int] = None  # index of the item whose wording is shown (None = heaviest)
    swaps: int = 0            # times the wording was swapped after failing

    @property
    def support(self) -> int:
        return len({i.source_case for i in self.items})

    @property
    def key(self) -> str:
        return f"{self.kind}|{'+'.join(sorted(self.sections))}"

    def representative(self) -> Item:
        """The item whose wording is shown: the pinned one, else the heaviest
        (ties go to the shortest label, the most generic wording)."""
        if self.rep is not None:
            return self.items[self.rep]
        return min(self.items, key=lambda i: (-i.weight, len(i.label)))


def _label_has_party(text: str, party_names: Iterable[str]) -> bool:
    low = text.lower()
    return any(n.lower() in low for n in party_names)


def missed_items(case: Case, report: DiscrepancyReport, teacher: LegalReasoningGraph,
                 *, index=None, party_names: Iterable[str] = ()) -> list[Item]:
    """The teacher Rules/Obligations this (training) case's student answer missed."""
    if case.role != "training":
        raise ValueError(f"checklist items are mined from training cases only, not {case.case_id}")
    rules = {r.rid: r for r in teacher.rules}
    obligations = {o.oid: o for o in teacher.obligations}
    names = list(party_names)
    out = []
    for m in report.v_miss:
        node = rules.get(m.teacher_id) or obligations.get(m.teacher_id)
        if isinstance(node, Rule):
            cite, juris = node.citation, node.jurisdiction
        elif isinstance(node, Obligation):
            req = rules.get(node.required_by)
            cite = req.citation if isinstance(req, Rule) else node.required_by
            juris = node.jurisdiction
        else:
            continue
        if index is not None and index.classify_citation(cite) == "fabricated":
            continue
        if _label_has_party(node.label, names):
            continue
        sections = canonical_citation(cite, juris)
        if not sections:
            continue
        out.append(Item(
            kind=m.node_type, citation=cite, jurisdiction=_canon_jurisdiction(juris),
            label=node.label, weight=m.weight, sections=sections, source_case=case.case_id,
            status=node.status.value if isinstance(node, Obligation) else "",
            deadline=node.deadline if isinstance(node, Obligation) else None,
            authority=node.authority.value if isinstance(node, Rule) else "",
        ))
    return out


def cluster(items: Iterable[Item]) -> list[Cluster]:
    groups: dict[tuple, Cluster] = {}
    for it in items:
        key = (it.kind, it.sections)
        if key not in groups:
            groups[key] = Cluster(kind=it.kind, sections=it.sections, jurisdiction=it.jurisdiction)
        groups[key].items.append(it)
    return list(groups.values())


# ──────────────────────────────────────────────
# Ranking
# ──────────────────────────────────────────────

Embed = Callable[[list[str]], "object"]   # texts -> L2-normalised matrix (rows)


def _eligible(clusters: list[Cluster], case: Case) -> list[Cluster]:
    juris = {_canon_jurisdiction(t) for t in case.jurisdiction_tags}
    return [c for c in clusters if c.jurisdiction in juris]


def rank(clusters: list[Cluster], case: Case, method: str, *, embed: Optional[Embed] = None,
         support_weight: float = 0.5, priority_alpha: float = 0.0) -> list[Cluster]:
    """Clusters in the case's jurisdictions, best first.

    ``support``    most often missed in training first (weight breaks ties)
    ``similarity`` closest label to the case text first (needs ``embed``)
    ``combined``   similarity + support_weight × support / max support
                   + priority_alpha × priority (learned by the iterative loop)
    """
    pool = _eligible(clusters, case)
    if not pool:
        return []
    max_sup = max(c.support for c in pool)
    sup = {c.key: c.support / max_sup for c in pool}
    if method == "support":
        return sorted(pool, key=lambda c: (-c.support, -c.representative().weight, c.key))
    if embed is None:
        raise ValueError(f"ranking method {method!r} needs an embedding function")
    texts = [f"{case.facts}\n{case.question}"] + [c.representative().label for c in pool]
    m = embed(texts)
    sims = (m[1:] @ m[0]).tolist()
    sim = {c.key: s for c, s in zip(pool, sims)}
    if method == "similarity":
        return sorted(pool, key=lambda c: (-sim[c.key], c.key))
    if method == "combined":
        return sorted(pool, key=lambda c: (-(sim[c.key] + support_weight * sup[c.key]
                                              + priority_alpha * c.priority), c.key))
    raise ValueError(f"unknown ranking method {method!r}")


# ──────────────────────────────────────────────
# Offline evaluation against a test case's real gaps
# ──────────────────────────────────────────────

@dataclass
class Gap:
    teacher_id: str
    kind: str
    label: str
    weight: float
    sections: frozenset[str]


def test_gaps(report: DiscrepancyReport, teacher: LegalReasoningGraph, *, index=None) -> list[Gap]:
    """Missing teacher R/O nodes of a test case (evaluation only)."""
    rules = {r.rid: r for r in teacher.rules}
    obligations = {o.oid: o for o in teacher.obligations}
    out = []
    for m in report.v_miss:
        node = rules.get(m.teacher_id) or obligations.get(m.teacher_id)
        if isinstance(node, Rule):
            cite, juris = node.citation, node.jurisdiction
        elif isinstance(node, Obligation):
            req = rules.get(node.required_by)
            cite = req.citation if isinstance(req, Rule) else node.required_by
            juris = node.jurisdiction
        else:
            continue
        if index is not None and index.classify_citation(cite) == "fabricated":
            continue
        out.append(Gap(m.teacher_id, m.node_type, node.label, m.weight,
                       canonical_citation(cite, juris)))
    return out


def match_gaps(given: list[Cluster], gaps: list[Gap], *, embed: Optional[Embed] = None,
               min_sim: float = 0.5) -> list[Gap]:
    """The gaps the given clusters fill, one gap per cluster at most."""
    return [g for _, g in match_pairs(given, gaps, embed=embed, min_sim=min_sim)]


def match_pairs(given: list[Cluster], gaps: list[Gap], *, embed: Optional[Embed] = None,
                min_sim: float = 0.5) -> list[tuple[Cluster, Gap]]:
    """(cluster, gap it fills) pairs.

    A cluster fills a gap if it is the same kind of node, shares a statute
    section and (with ``embed``) its label is at least ``min_sim`` similar.
    Each gap is filled at most once, by the first cluster that covers it.
    """
    if not given or not gaps:
        return []
    sim = None
    if embed is not None:
        m = embed([c.representative().label for c in given] + [g.label for g in gaps])
        sim = (m[:len(given)] @ m[len(given):].T)
    filled: list[Gap] = []
    pairs: list[tuple[Cluster, Gap]] = []
    for i, c in enumerate(given):
        best = None
        for j, g in enumerate(gaps):
            if g in filled or g.kind != c.kind or not (g.sections & c.sections):
                continue
            if sim is not None and sim[i, j] < min_sim:
                continue
            if best is None or g.weight > gaps[best].weight:
                best = j
        if best is not None:
            filled.append(gaps[best])
            pairs.append((c, gaps[best]))
    return pairs


def teacher_targets(teacher: LegalReasoningGraph, *, index=None) -> list[Gap]:
    """Every (non-fabricated) teacher Rule/Obligation of a case, as gaps to match against."""
    from .discrepancy import _node_weight

    nodes = [(r.rid, "R", r) for r in teacher.rules] + [(o.oid, "O", o) for o in teacher.obligations]
    fake = DiscrepancyReport(case_id=teacher.case_id, l_ged=0.0, v_miss=[
        MissingNode(teacher_id=nid, node_type=kind, label=n.label, weight=_node_weight(n))
        for nid, kind, n in nodes])
    return test_gaps(fake, teacher, index=index)


def coverage(ranked: list[Cluster], gaps: list[Gap], k: int, *, embed: Optional[Embed] = None,
             min_sim: float = 0.5) -> dict[str, float]:
    """How much of the test case's gap the top-k clusters could fill."""
    top = ranked[:k]
    filled = match_gaps(top, gaps, embed=embed, min_sim=min_sim)
    return {"useful": len(filled), "given": len(top), "weight": sum(g.weight for g in filled),
            "gap_weight": sum(g.weight for g in gaps)}


# ──────────────────────────────────────────────
# Rendering
# ──────────────────────────────────────────────

HEADER = ("REQUIRED ELEMENTS — check each against the facts. For every one that the "
          "facts trigger, your JSON graph must contain it, with an Application node that "
          "applies it to the facts:")


def render_checklist(clusters: list[Cluster]) -> str:
    """The same wording as the Stage B checklist arm, from training-case items.

    The header asks the student to check each element against the facts,
    because unlike the oracle arm these items may not all apply to the case.
    """
    lines = []
    for c in clusters:
        it = c.representative()
        i = len(lines) + 1
        if it.kind == "R":
            lines.append(f"{i}. A Rule node with citation \"{it.citation}\" "
                         f"({it.jurisdiction}, {it.authority or 'binding'}): {it.label}.")
        else:
            deadline = f" Deadline: {it.deadline}." if it.deadline else ""
            lines.append(f"{i}. An Obligation node ({it.status or 'mandatory'}, required by "
                         f"{it.citation}): {it.label}.{deadline}")
    if not lines:
        return ""
    return "\n".join([HEADER, *lines, ""])


__all__ = [
    "Item", "Cluster", "Gap", "missed_items", "cluster", "rank", "test_gaps",
    "match_gaps", "match_pairs", "teacher_targets", "coverage", "render_checklist", "HEADER",
]
