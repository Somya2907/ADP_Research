"""F-I-R-A-C-O legal reasoning graph schema.

This is the typed representation of a legal reasoning trace.
Both G_ref (teacher) and G_agent (agent) conform to this schema,
enabling structural comparison via Legal-Weighted Graph Edit Distance (L-GED).

Node types:
  F (Facts)        — Material facts including jurisdictional anchors
  I (Issues)       — Legal questions raised by the facts
  R (Rules)        — Statutory provisions, regulations, framework controls
  A (Application)  — Element-by-element subsumption / analogical reasoning
  C (Conclusion)   — Compliance determinations
  O (Obligations)  — Required remedial actions (novel to L-DRL; no DRL analogue)

Edge types encode legal reasoning relations: supports, contradicts,
applies-to, triggers, satisfies-element, fails-element, preempts, distinguishes.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class Polarity(str, Enum):
    PRESENT = "present"
    DISPUTED = "disputed"
    ABSENT = "absent"
    UNKNOWN = "unknown"


class IssueStatus(str, Enum):
    DISPOSITIVE = "dispositive"
    COLLATERAL = "collateral"
    WAIVED = "waived"


class Authority(str, Enum):
    BINDING = "binding"           # controlling statute or regulation in jurisdiction
    PERSUASIVE = "persuasive"     # out-of-jurisdiction or secondary authority
    ADVISORY = "advisory"         # framework or guidance (NIST AI RMF, ISO)
    OVERRULED = "overruled"       # superseded or contradicted authority


class ApplicationResult(str, Enum):
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    REQUIRES_FACT = "requires-fact"   # element requires fact not in the record
    PARTIAL = "partial"               # partially satisfied


class ConclusionDetermination(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non-compliant"
    CONDITIONAL = "conditional"       # compliant if condition X is met


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ObligationStatus(str, Enum):
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    SAFE_HARBOR = "safe-harbor"       # optional but provides affirmative defense


class EdgeType(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    APPLIES_TO = "applies-to"
    TRIGGERS = "triggers"
    SATISFIES_ELEMENT = "satisfies-element"
    FAILS_ELEMENT = "fails-element"
    PREEMPTS = "preempts"
    DISTINGUISHES = "distinguishes"


class GraphSource(str, Enum):
    AGENT = "agent"
    REFERENCE = "reference"


# ──────────────────────────────────────────────
# Node models
# ──────────────────────────────────────────────

class Fact(BaseModel):
    fid: str = Field(pattern=r"^F\d+$")
    label: str
    polarity: Polarity = Polarity.PRESENT
    support_quote: Optional[str] = None


class Issue(BaseModel):
    iid: str = Field(pattern=r"^I\d+$")
    label: str
    status: IssueStatus = IssueStatus.DISPOSITIVE


class Rule(BaseModel):
    rid: str = Field(pattern=r"^R\d+$")
    citation: str                             # e.g., "Colo. Rev. Stat. §6-1-1703(3)"
    label: str
    authority: Authority = Authority.BINDING
    jurisdiction: str                         # "CO", "NYC", "TX", "US-federal"
    effective_as_of: Optional[str] = None     # ISO date; None if in force indefinitely


class Application(BaseModel):
    aid: str = Field(pattern=r"^A\d+$")
    rule_ref: str                             # rid of the R node being applied
    fact_refs: list[str]                      # fids of F nodes in the subsumption
    issue_ref: str                            # iid of the I node
    result: ApplicationResult
    reasoning: str


class Conclusion(BaseModel):
    cid: str = Field(pattern=r"^C\d+$")
    determination: ConclusionDetermination
    confidence: Confidence = Confidence.MEDIUM
    support_refs: list[str]                   # Application aids that support this


class Obligation(BaseModel):
    oid: str = Field(pattern=r"^O\d+$")
    label: str                                # e.g., "Complete annual impact assessment"
    required_by: str                          # rid of triggering rule
    status: ObligationStatus
    jurisdiction: str
    deadline: Optional[str] = None            # ISO date or descriptive


class Edge(BaseModel):
    eid: str = Field(pattern=r"^E\d+$")
    src: str
    dst: str
    type: EdgeType
    justification: Optional[str] = None


# ──────────────────────────────────────────────
# Top-level graph
# ──────────────────────────────────────────────

class LegalReasoningGraph(BaseModel):
    """Complete F-I-R-A-C-O reasoning graph for a single case."""

    case_id: str
    source: GraphSource
    model_name: str                           # e.g., "claude-opus-4-6"

    facts: list[Fact] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
    rules: list[Rule] = Field(default_factory=list)
    applications: list[Application] = Field(default_factory=list)
    conclusions: list[Conclusion] = Field(default_factory=list)
    obligations: list[Obligation] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)

    @field_validator("edges")
    @classmethod
    def validate_edge_refs(cls, edges: list[Edge], info) -> list[Edge]:
        """Ensure every edge src/dst references an existing node ID."""
        data = info.data
        all_ids: set[str] = set()
        id_fields = {
            "facts": "fid", "issues": "iid", "rules": "rid",
            "applications": "aid", "conclusions": "cid", "obligations": "oid",
        }
        for list_name, id_field in id_fields.items():
            for node in data.get(list_name, []):
                if isinstance(node, BaseModel):
                    all_ids.add(getattr(node, id_field))
                elif isinstance(node, dict):
                    all_ids.add(node[id_field])

        for edge in edges:
            if edge.src not in all_ids:
                raise ValueError(
                    f"Edge {edge.eid} src '{edge.src}' references "
                    f"nonexistent node. Valid IDs: {sorted(all_ids)}"
                )
            if edge.dst not in all_ids:
                raise ValueError(
                    f"Edge {edge.eid} dst '{edge.dst}' references "
                    f"nonexistent node. Valid IDs: {sorted(all_ids)}"
                )
        return edges

    def node_count(self) -> int:
        """Total number of nodes across all types."""
        return (
            len(self.facts) + len(self.issues) + len(self.rules)
            + len(self.applications) + len(self.conclusions)
            + len(self.obligations)
        )

    def node_summary(self) -> str:
        """Human-readable node count string."""
        return (
            f"F={len(self.facts)} I={len(self.issues)} R={len(self.rules)} "
            f"A={len(self.applications)} C={len(self.conclusions)} "
            f"O={len(self.obligations)} E={len(self.edges)}"
        )
