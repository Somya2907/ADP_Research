"""Compute structural discrepancies between a teacher and a student graph.

Four discrepancy types are reported:

* ``v_miss``       — nodes in the teacher graph with no student-side alignment.
* ``v_halluc``     — student nodes that don't align to any teacher node and fail
  a pluggable validity check. The default validity check flags every unaligned
  student node as a candidate.
* ``e_diff``       — edges whose aligned ``(src, dst)`` pair exists in the
  teacher graph but is absent in the student graph or carries a different
  edge type.
* ``v_misground``  — (NEW) an *aligned* Rule pair whose citations conflict:
  the student grounded the right proposition in the wrong (or fabricated)
  statutory section. This is the Magesh pattern and is, by construction,
  invisible to the other three categories — both endpoints are aligned, so it
  is neither a miss nor a hallucination nor an edge difference.

The aggregate L-GED (Legal-weighted Graph Edit Distance) score weighs each
discrepancy by node-type weight × authority multiplier (the latter applies to
Rule nodes only). ``v_misground`` is reported as a diagnostic and is **not**
folded into L-GED unless ``include_misground_in_lged=True`` (kept off by default
so existing snapshot scores stay comparable).
"""
from __future__ import annotations

from typing import Callable, Optional

from pydantic import BaseModel, Field

from .alignment import AlignmentReport, citations_match, extract_citation_tokens
from .schema import Authority, EdgeType, LegalReasoningGraph, Rule

# Per-node-type weights for L-GED scoring (per onboarding spec).
NODE_TYPE_WEIGHTS: dict[str, float] = {
    "F": 1.0, "I": 1.5, "R": 2.0,
    "A": 2.5, "C": 1.5, "O": 2.5,
}

# Authority-hierarchy multiplier — applies to Rule nodes only.
AUTHORITY_MULTIPLIERS: dict[Authority, float] = {
    Authority.BINDING: 2.0,
    Authority.PERSUASIVE: 1.0,
    Authority.ADVISORY: 0.75,
    Authority.OVERRULED: 0.5,
}


# ──────────────────────────────────────────────
# Report models
# ──────────────────────────────────────────────

class MissingNode(BaseModel):
    teacher_id: str
    node_type: str
    label: str
    weight: float


class HallucinatedNode(BaseModel):
    student_id: str
    node_type: str
    label: str
    reason: str = "unaligned"
    weight: float


class EdgeDiff(BaseModel):
    teacher_eid: str
    teacher_src: str
    teacher_dst: str
    teacher_type: str
    student_src: Optional[str]
    student_dst: Optional[str]
    student_type: Optional[str] = None
    kind: str  # "missing" | "type_mismatch"
    weight: float


class Misgrounding(BaseModel):
    """An aligned Rule pair whose citations conflict (the Magesh pattern).

    Detection is index-independent: a misgrounding is flagged purely from the
    citation conflict between an aligned teacher/student rule pair. The statute
    index only sets ``student_section_exists`` (the real-but-wrong vs fabricated
    subtype), which is ``None`` until a provenance-confirmed index is supplied.
    """

    teacher_id: str
    student_id: str
    teacher_citation: str
    student_citation: str
    proposition: str
    student_section_exists: Optional[bool] = None
    weight: float


class DiscrepancyReport(BaseModel):
    case_id: str
    student_id: Optional[str] = None
    v_miss: list[MissingNode] = Field(default_factory=list)
    v_halluc: list[HallucinatedNode] = Field(default_factory=list)
    e_diff: list[EdgeDiff] = Field(default_factory=list)
    v_misground: list[Misgrounding] = Field(default_factory=list)
    l_ged: float = 0.0
    node_type_breakdown: dict[str, dict[str, int]] = Field(default_factory=dict)

    @property
    def v_miss_count(self) -> int:
        return len(self.v_miss)

    @property
    def v_halluc_count(self) -> int:
        return len(self.v_halluc)

    @property
    def e_diff_count(self) -> int:
        return len(self.e_diff)

    @property
    def v_misground_count(self) -> int:
        return len(self.v_misground)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _node_type_of(node_id: str) -> str:
    return node_id[:1].upper() if node_id else "?"


def _index_nodes(graph: LegalReasoningGraph) -> dict[str, BaseModel]:
    """Map node-id → pydantic node model across all six node lists."""
    idx: dict[str, BaseModel] = {}
    for f in graph.facts: idx[f.fid] = f
    for i in graph.issues: idx[i.iid] = i
    for r in graph.rules: idx[r.rid] = r
    for a in graph.applications: idx[a.aid] = a
    for c in graph.conclusions: idx[c.cid] = c
    for o in graph.obligations: idx[o.oid] = o
    return idx


def _label_of(node: BaseModel) -> str:
    for attr in ("label", "reasoning", "determination", "citation"):
        if hasattr(node, attr):
            val = getattr(node, attr)
            if hasattr(val, "value"):
                return str(val.value)
            if val:
                return str(val)
    return ""


def _node_weight(node: BaseModel) -> float:
    """Weight of a node = node-type weight × authority multiplier (rules only)."""
    nid = (
        getattr(node, "fid", None) or getattr(node, "iid", None)
        or getattr(node, "rid", None) or getattr(node, "aid", None)
        or getattr(node, "cid", None) or getattr(node, "oid", None)
        or ""
    )
    base = NODE_TYPE_WEIGHTS.get(_node_type_of(nid), 1.0)
    authority = getattr(node, "authority", None)
    if isinstance(authority, Authority):
        return base * AUTHORITY_MULTIPLIERS.get(authority, 1.0)
    return base


def _edge_weight(src_node: Optional[BaseModel], dst_node: Optional[BaseModel]) -> float:
    """Edge weight = max of its endpoints' node weights (sensible default)."""
    weights = [_node_weight(n) for n in (src_node, dst_node) if n is not None]
    return max(weights) if weights else 1.0


# Default validity check: flag every unaligned student node as candidate halluc.
def _default_validity_check(node: BaseModel) -> tuple[bool, str]:
    return True, "unaligned"


def make_statute_validity_check(
    section_exists_fn: Callable[[str], bool],
) -> Callable[[BaseModel], tuple[bool, str]]:
    """Build a statute-grounded ``validity_check`` for ``compute_discrepancies``.

    Refines hallucination detection for unaligned student **Rule** nodes only:

    * Rule citing section token(s), none of which are a real section →
      ``(True, "fabricated_citation")`` — a grounded-but-invented rule.
    * Rule citing a real section → ``(False, "cites_real_section")`` — a real
      rule the teacher simply omitted; not a hallucination.
    * Uncited Rule, or any non-Rule node → ``(True, "unaligned")`` — the statute
      index can't speak to it, so behaviour is unchanged (matches the default).

    Gate this behind a provenance-confirmed index: build it from
    ``make_section_exists_fn(load_statute_index())`` and fall back to
    ``_default_validity_check`` when that returns ``None`` (untrustworthy index).
    """
    def check(node: BaseModel) -> tuple[bool, str]:
        if isinstance(node, Rule):
            tokens = extract_citation_tokens(node.citation)
            if tokens:
                if section_exists_fn(node.citation):
                    return False, "cites_real_section"
                return True, "fabricated_citation"
        return True, "unaligned"

    return check


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────

def compute_discrepancies(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    alignment: AlignmentReport,
    validity_check: Callable[[BaseModel], tuple[bool, str]] = _default_validity_check,
    *,
    section_exists_fn: Optional[Callable[[str], bool]] = None,
    include_misground_in_lged: bool = False,
) -> DiscrepancyReport:
    """Compute v_miss / v_halluc / e_diff / v_misground and the L-GED score.

    ``validity_check`` is a pluggable callable applied to each unaligned student
    node; if it returns ``(True, reason)`` the node is recorded as v_halluc.

    ``section_exists_fn`` is an optional callable ``citation -> bool`` from the
    statute index; when supplied, misgroundings record whether the student's
    section is real-but-wrong (True) or fabricated (False). When ``None`` (no
    provenance-confirmed index yet), ``student_section_exists`` is left ``None``.

    ``include_misground_in_lged`` folds misgrounding weights into L-GED. Default
    off, so this addition does not change existing snapshot scores.
    """
    t_index = _index_nodes(teacher)
    s_index = _index_nodes(student)
    aligned_student_ids = {sid for sid in (
        list(alignment.fact_map.values()) + list(alignment.issue_map.values())
        + list(alignment.rule_map.values()) + list(alignment.application_map.values())
        + list(alignment.conclusion_map.values()) + list(alignment.obligation_map.values())
    ) if sid is not None}

    teacher_to_student: dict[str, Optional[str]] = {}
    for m in alignment.all_maps().values():
        teacher_to_student.update(m)

    # ── v_miss ──
    v_miss: list[MissingNode] = []
    for tid, sid in teacher_to_student.items():
        if sid is None:
            node = t_index.get(tid)
            if node is None:
                continue
            v_miss.append(MissingNode(
                teacher_id=tid,
                node_type=_node_type_of(tid),
                label=_label_of(node),
                weight=_node_weight(node),
            ))

    # ── v_halluc ──
    v_halluc: list[HallucinatedNode] = []
    for sid, node in s_index.items():
        if sid in aligned_student_ids:
            continue
        flag, reason = validity_check(node)
        if not flag:
            continue
        v_halluc.append(HallucinatedNode(
            student_id=sid,
            node_type=_node_type_of(sid),
            label=_label_of(node),
            reason=reason,
            weight=_node_weight(node),
        ))

    # ── e_diff ──
    student_edge_index: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for e in student.edges:
        student_edge_index.setdefault((e.src, e.dst), []).append((e.eid, e.type.value))

    e_diff: list[EdgeDiff] = []
    for edge in teacher.edges:
        mapped_src = teacher_to_student.get(edge.src)
        mapped_dst = teacher_to_student.get(edge.dst)
        if mapped_src is None or mapped_dst is None:
            continue
        student_candidates = student_edge_index.get((mapped_src, mapped_dst), [])
        if not student_candidates:
            e_diff.append(EdgeDiff(
                teacher_eid=edge.eid, teacher_src=edge.src, teacher_dst=edge.dst,
                teacher_type=edge.type.value, student_src=mapped_src,
                student_dst=mapped_dst, student_type=None, kind="missing",
                weight=_edge_weight(t_index.get(edge.src), t_index.get(edge.dst)),
            ))
            continue
        if not any(stype == edge.type.value for _, stype in student_candidates):
            e_diff.append(EdgeDiff(
                teacher_eid=edge.eid, teacher_src=edge.src, teacher_dst=edge.dst,
                teacher_type=edge.type.value, student_src=mapped_src,
                student_dst=mapped_dst, student_type=student_candidates[0][1],
                kind="type_mismatch",
                weight=_edge_weight(t_index.get(edge.src), t_index.get(edge.dst)),
            ))

    # ── v_misground (NEW) ──
    # For each aligned Rule pair, flag a misgrounding iff the student cites a
    # (non-empty) section that shares no canonical token with the teacher's
    # citation — i.e. the pair aligned by *text* despite conflicting citations.
    # This is deliberately recomputed from citations_match rather than read from
    # AlignmentMatch.method, which is hardcoded to "citation" for all rules.
    v_misground: list[Misgrounding] = []
    for tid, sid in alignment.rule_map.items():
        if sid is None:
            continue
        t_rule = t_index.get(tid)
        s_rule = s_index.get(sid)
        if not isinstance(t_rule, Rule) or not isinstance(s_rule, Rule):
            continue
        s_tokens = extract_citation_tokens(s_rule.citation)
        if not s_tokens:
            continue  # uncited student rule — a different defect, not a misgrounding
        if citations_match(t_rule.citation, s_rule.citation):
            continue  # citations agree → correctly grounded
        exists: Optional[bool] = None
        if section_exists_fn is not None:
            exists = section_exists_fn(s_rule.citation)
        v_misground.append(Misgrounding(
            teacher_id=tid,
            student_id=sid,
            teacher_citation=t_rule.citation,
            student_citation=s_rule.citation,
            proposition=t_rule.label,
            student_section_exists=exists,
            weight=_node_weight(t_rule),
        ))

    # ── Breakdown ──
    breakdown: dict[str, dict[str, int]] = {
        k: {"v_miss": 0, "v_halluc": 0} for k in "FIRACO"
    }
    for m in v_miss:
        breakdown.setdefault(m.node_type, {"v_miss": 0, "v_halluc": 0})["v_miss"] += 1
    for h in v_halluc:
        breakdown.setdefault(h.node_type, {"v_miss": 0, "v_halluc": 0})["v_halluc"] += 1

    score = (
        sum(m.weight for m in v_miss)
        + sum(h.weight for h in v_halluc)
        + sum(e.weight for e in e_diff)
    )
    if include_misground_in_lged:
        score += sum(mg.weight for mg in v_misground)

    return DiscrepancyReport(
        case_id=teacher.case_id,
        student_id=student.agent_id,
        v_miss=v_miss,
        v_halluc=v_halluc,
        e_diff=e_diff,
        v_misground=v_misground,
        l_ged=score,
        node_type_breakdown=breakdown,
    )


def l_ged(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    alignment: AlignmentReport,
    validity_check: Callable[[BaseModel], tuple[bool, str]] = _default_validity_check,
    **kwargs,
) -> float:
    """Legal-weighted Graph Edit Distance, as a single number."""
    return compute_discrepancies(
        teacher, student, alignment, validity_check, **kwargs
    ).l_ged


__all__ = [
    "AUTHORITY_MULTIPLIERS",
    "DiscrepancyReport",
    "EdgeDiff",
    "HallucinatedNode",
    "Misgrounding",
    "MissingNode",
    "NODE_TYPE_WEIGHTS",
    "compute_discrepancies",
    "l_ged",
    "make_statute_validity_check",
]
