"""Compute structural discrepancies between a teacher and a student graph.

Three discrepancy types are reported:

* ``v_miss``   — nodes in the teacher graph with no student-side alignment.
* ``v_halluc`` — student nodes that don't align to any teacher node and fail
  a pluggable validity check. The default validity check flags every
  unaligned student node as a candidate.
* ``e_diff``   — edges whose aligned ``(src, dst)`` pair exists in the
  teacher graph but is absent in the student graph or carries a different
  edge type.

The aggregate L-GED (Legal-weighted Graph Edit Distance) score weighs each
discrepancy by node-type weight × authority multiplier (the latter applies
to Rule nodes only).
"""
from __future__ import annotations

from typing import Callable, Optional

from pydantic import BaseModel, Field

from .alignment import AlignmentReport
from .schema import Authority, EdgeType, LegalReasoningGraph

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


class DiscrepancyReport(BaseModel):
    case_id: str
    student_id: Optional[str] = None
    v_miss: list[MissingNode] = Field(default_factory=list)
    v_halluc: list[HallucinatedNode] = Field(default_factory=list)
    e_diff: list[EdgeDiff] = Field(default_factory=list)
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
    """Edge weight = max of its endpoints' node weights (sensible default).

    Using the heavier endpoint means a teacher rule wired into a teacher
    conclusion contributes more than a fact-to-issue edge.
    """
    weights = [_node_weight(n) for n in (src_node, dst_node) if n is not None]
    return max(weights) if weights else 1.0


# Default validity check: flag every unaligned student node as candidate halluc.
def _default_validity_check(node: BaseModel) -> tuple[bool, str]:
    return True, "unaligned"


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────

def compute_discrepancies(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    alignment: AlignmentReport,
    validity_check: Callable[[BaseModel], tuple[bool, str]] = _default_validity_check,
) -> DiscrepancyReport:
    """Compute v_miss / v_halluc / e_diff and the aggregate L-GED score.

    ``validity_check`` is a pluggable callable applied to each unaligned
    student node; if it returns ``(True, reason)`` the node is recorded as a
    v_halluc. The default flags every unaligned student node.
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
            # Endpoint unaligned: covered by v_miss; don't double-count here.
            continue
        student_candidates = student_edge_index.get((mapped_src, mapped_dst), [])
        if not student_candidates:
            e_diff.append(EdgeDiff(
                teacher_eid=edge.eid,
                teacher_src=edge.src,
                teacher_dst=edge.dst,
                teacher_type=edge.type.value,
                student_src=mapped_src,
                student_dst=mapped_dst,
                student_type=None,
                kind="missing",
                weight=_edge_weight(t_index.get(edge.src), t_index.get(edge.dst)),
            ))
            continue
        if not any(stype == edge.type.value for _, stype in student_candidates):
            e_diff.append(EdgeDiff(
                teacher_eid=edge.eid,
                teacher_src=edge.src,
                teacher_dst=edge.dst,
                teacher_type=edge.type.value,
                student_src=mapped_src,
                student_dst=mapped_dst,
                student_type=student_candidates[0][1],
                kind="type_mismatch",
                weight=_edge_weight(t_index.get(edge.src), t_index.get(edge.dst)),
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

    return DiscrepancyReport(
        case_id=teacher.case_id,
        student_id=student.agent_id,
        v_miss=v_miss,
        v_halluc=v_halluc,
        e_diff=e_diff,
        l_ged=score,
        node_type_breakdown=breakdown,
    )


def l_ged(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    alignment: AlignmentReport,
    validity_check: Callable[[BaseModel], tuple[bool, str]] = _default_validity_check,
) -> float:
    """Legal-weighted Graph Edit Distance, as a single number.

    Sum over all discrepancies of: node_type_weight × authority_multiplier.
    The multiplier applies only to Rule nodes; defaults to 1.0 elsewhere.
    """
    return compute_discrepancies(teacher, student, alignment, validity_check).l_ged


__all__ = [
    "AUTHORITY_MULTIPLIERS",
    "DiscrepancyReport",
    "EdgeDiff",
    "HallucinatedNode",
    "MissingNode",
    "NODE_TYPE_WEIGHTS",
    "compute_discrepancies",
    "l_ged",
]
