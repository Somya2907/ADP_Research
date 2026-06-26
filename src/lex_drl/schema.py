"""F-I-R-A-C-O legal reasoning graph schema.

Both G_ref (teacher) and G_agent (student) conform to this schema,
enabling structural comparison via Legal-Weighted Graph Edit Distance (L-GED).

Node types: F (Facts), I (Issues), R (Rules), A (Application),
            C (Conclusion), O (Obligations)
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
    BINDING = "binding"
    PERSUASIVE = "persuasive"
    ADVISORY = "advisory"
    OVERRULED = "overruled"


class ApplicationResult(str, Enum):
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    REQUIRES_FACT = "requires-fact"
    PARTIAL = "partial"


class ConclusionDetermination(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non-compliant"
    CONDITIONAL = "conditional"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ObligationStatus(str, Enum):
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    SAFE_HARBOR = "safe-harbor"


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
    citation: str
    label: str
    authority: Authority = Authority.BINDING
    jurisdiction: str
    effective_as_of: Optional[str] = None


class Application(BaseModel):
    aid: str = Field(pattern=r"^A\d+$")
    rule_ref: str
    fact_refs: list[str]
    issue_ref: str
    result: ApplicationResult
    reasoning: str


class Conclusion(BaseModel):
    cid: str = Field(pattern=r"^C\d+$")
    determination: ConclusionDetermination
    confidence: Confidence = Confidence.MEDIUM
    support_refs: list[str]


class Obligation(BaseModel):
    oid: str = Field(pattern=r"^O\d+$")
    label: str
    required_by: str
    status: ObligationStatus
    jurisdiction: str
    deadline: Optional[str] = None


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
    model_name: str

    # agent_id identifies WHICH student model produced this graph.
    # None for reference graphs.
    # Values: "gpt5", "llama3_2b" (or any future student key).
    # Used to name output files as {case_id}_agent_{agent_id}.json
    agent_id: Optional[str] = None

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
                    f"Edge {edge.eid} src '{edge.src}' references nonexistent node. "
                    f"Valid IDs: {sorted(all_ids)}"
                )
            if edge.dst not in all_ids:
                raise ValueError(
                    f"Edge {edge.eid} dst '{edge.dst}' references nonexistent node. "
                    f"Valid IDs: {sorted(all_ids)}"
                )
        return edges

    def node_count(self) -> int:
        return (
            len(self.facts) + len(self.issues) + len(self.rules)
            + len(self.applications) + len(self.conclusions)
            + len(self.obligations)
        )

    def node_summary(self) -> str:
        return (
            f"F={len(self.facts)} I={len(self.issues)} R={len(self.rules)} "
            f"A={len(self.applications)} C={len(self.conclusions)} "
            f"O={len(self.obligations)} E={len(self.edges)}"
        )

    def save_path(self, output_dir: str = "data/outputs/graphs") -> str:
        """Canonical file path for this graph."""
        from pathlib import Path
        base = Path(output_dir)
        if self.source == GraphSource.REFERENCE:
            fname = f"{self.case_id}_reference.json"
        elif self.agent_id:
            fname = f"{self.case_id}_agent_{self.agent_id}.json"
        else:
            fname = f"{self.case_id}_agent.json"
        return str(base / fname)
