"""Mine reusable patches from training-case discrepancy reports.

Two families:

* **Family A** — missing Rules / Obligations (from ``report.v_miss``). The
  teacher established a controlling authority the student dropped.
* **Family B** — misgroundings (from ``report.v_misground``). The student
  grounded the right proposition in the wrong statutory section.

Each candidate carries a deterministic ``prevention_step`` (always computed,
serving as fallback and as the LLM's grounding draft). If an :class:`InsightWriter`
is supplied, a cached Claude-Opus call rewrites that draft into tighter prose;
otherwise the deterministic draft is used verbatim (fully reproducible).

Mining is **train-only**: ``generate_patches`` raises on a non-training case.
Patches are rule/authority-level, never case-outcome-level — that abstraction is
the train→test leakage firewall.
"""
from __future__ import annotations

import hashlib
import os
from datetime import date
from typing import Callable, Iterable, Optional

from .alignment import extract_citation_tokens
from .cases import Case
from .discrepancy import DiscrepancyReport, MissingNode, Misgrounding
from .patch_store import Patch
from .schema import Authority, LegalReasoningGraph, Obligation, ObligationStatus, Rule

# Operative date for the study (matches configs/prompts/agent_firaco.txt).
OPERATIVE_DATE = date(2026, 4, 16)

# ── D4 selection floor ─────────────────────────────────────────
INCLUDED_RULE_AUTHORITIES = {Authority.BINDING, Authority.PERSUASIVE}
INCLUDED_OBLIGATION_STATUSES = {ObligationStatus.MANDATORY, ObligationStatus.RECOMMENDED}

# ── D5 concept lexicon (seed; extend as the corpus grows) ──────
LEGAL_LEXICON: set[str] = {
    "bias audit", "independent auditor", "retraining", "substantial modification",
    "impact assessment", "high-risk", "deployer", "developer",
    "consequential decision", "algorithmic discrimination", "notice",
    "disclosure", "penalties", "safe harbor", "small deployer", "aedt",
    "consumer", "documentation", "appeal", "data correction", "reasonable care",
    "effective date", "annual review", "risk management",
    # Extensions from reading the E1/M1/H1 rules (recurring statutory vocabulary
    # across CO AIA / NYC LL144 / TX TRAIGA; never party-specific):
    "promotion", "screening", "selection rate", "impact ratio", "preemption",
    "private right of action", "rebuttable presumption", "distribution date",
    "intentional discrimination", "civil penalty", "risk management policy",
    "candidate notice",
}

_JURIS_CANON = {"nyc": "nyc", "new york": "nyc", "colorado": "colorado",
                "co": "colorado", "texas": "texas", "tx": "texas"}


# ──────────────────────────────────────────────
# Optional hybrid prose writer
# ──────────────────────────────────────────────

class InsightWriter:
    """Cached one-shot Claude-Opus rewrite of a patch's prevention step.

    Mirrors ``TeacherClient``'s cached pattern (namespace ``patch_insight``) so
    prose is frozen in ``cache.db`` and the mining run is reproducible.
    """

    _SYSTEM = (
        "You are a US AI-law expert writing a single reusable reasoning note. "
        "Given a structured patch, rewrite the draft into 2-3 tight sentences: "
        "the error to avoid, the controlling authority, and the one-line prevention. "
        "Stay rule-level and generalizable. Name NO parties or case-specific facts. "
        "Do not exceed ~200 tokens. Return only the note text."
    )

    def __init__(self, model: str | None = None):
        from anthropic import Anthropic  # lazy: tests need not install it
        self.client = Anthropic()
        self.model = model or os.environ.get("TEACHER_MODEL", "claude-opus-4-6")

    def rewrite(self, fields: dict, draft: str) -> str:
        user = (
            f"FAMILY: {fields['patch_family']}\n"
            f"CONTROLLING AUTHORITY: {fields['controlling_authority']}\n"
            f"JURISDICTION: {fields['jurisdiction']}\n"
            f"PROPOSITION: {fields['proposition']}\n"
            f"CONTRAINDICATION: {fields.get('contraindication', '')}\n"
            f"DRAFT: {draft}\n"
        )
        resp = self.generate(system=self._SYSTEM, user=user)
        text = getattr(resp, "text", None)
        return (text or draft).strip()

    # cached_call imported lazily to avoid a hard import at module load
    def generate(self, system: str, user: str, max_tokens: int = 400,
                 temperature: float = 0.0):
        from .cache import cached_call

        @cached_call(namespace="patch_insight")
        def _call(self, system: str, user: str, **kw):
            from .clients import LLMResponse
            msg = self.client.messages.create(
                model=self.model, max_tokens=max_tokens, temperature=temperature,
                system=system, messages=[{"role": "user", "content": user}],
            )
            text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
            return LLMResponse(text=text, model=self.model,
                               input_tokens=msg.usage.input_tokens,
                               output_tokens=msg.usage.output_tokens)

        return _call(self, system=system, user=user)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _canon_jurisdiction(raw: str) -> str:
    return _JURIS_CANON.get((raw or "").strip().lower(), (raw or "").strip().lower())


def _concept_terms(label: str) -> list[str]:
    low = (label or "").lower()
    hits = [term for term in LEGAL_LEXICON if term in low]
    hits.sort(key=lambda t: low.index(t))
    return hits


def _trigger_keywords(citation: str, label: str, jurisdiction: str, case: Case) -> list[str]:
    kws: list[str] = []
    kws += sorted(extract_citation_tokens(citation))
    j = _canon_jurisdiction(jurisdiction)
    if j:
        kws.append(j)
    kws += _concept_terms(label)
    # NB: we intentionally do NOT add case.jurisdiction_tags — in a multi-
    # jurisdiction case those would tag a single-jurisdiction rule's patch with
    # sibling jurisdictions (e.g. a TX rule tagged "nyc"), hurting BM25 precision.
    # The rule's own jurisdiction (above) is the authoritative signal.
    seen, out = set(), []
    for k in kws:
        if k and k not in seen:
            seen.add(k); out.append(k)
    return out[:12]


def _future_effective_clause(effective_as_of: Optional[str]) -> str:
    if not effective_as_of:
        return ""
    try:
        eff = date.fromisoformat(effective_as_of[:10])
    except (ValueError, TypeError):
        return ""
    if eff > OPERATIVE_DATE:
        return f"Not yet enforceable as of the operative date (effective {effective_as_of})."
    return ""


def _contraindication_rule(rule: Rule, teacher: LegalReasoningGraph) -> str:
    parts: list[str] = []
    j = _canon_jurisdiction(rule.jurisdiction)
    if j:
        parts.append(f"Applies only in {j.upper()}; not triggered for matters outside it.")
    fut = _future_effective_clause(rule.effective_as_of)
    if fut:
        parts.append(fut)
    # Linked exceptions: teacher rules that contradict/distinguish/preempt this one.
    exception_targets = {
        e.dst for e in teacher.edges
        if e.src == rule.rid and e.type.value in {"contradicts", "distinguishes", "preempts"}
    }
    for r in teacher.rules:
        if r.rid in exception_targets:
            parts.append(f"Subject to: {r.label}.")
    return " ".join(parts)


def _patch_id(family: str, citation: str, node_types: list[str]) -> str:
    tokens = sorted(extract_citation_tokens(citation)) or [citation.strip().lower()]
    raw = f"{family}|{tokens}|{sorted(node_types)}"
    return "p_" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def _prevention_step(family: str, fields: dict, insight: Optional[InsightWriter]) -> str:
    if family == "missing_rule":
        concept = fields["keywords"][0] if fields["keywords"] else "this matter"
        draft = (f"When a matter involves {concept}, apply {fields['controlling_authority']} "
                 f"({fields['jurisdiction']}, {fields['authority_level']}): {fields['proposition']}.")
    elif family == "missing_obligation":
        concept = fields["keywords"][0] if fields["keywords"] else "this matter"
        deadline = f" (deadline: {fields['deadline']})" if fields.get("deadline") else ""
        draft = (f"Where {concept} applies, {fields['controlling_authority']} imposes a "
                 f"{fields['status']} obligation: {fields['proposition']}{deadline}.")
    else:  # misgrounding
        draft = (f"Ground the proposition \"{fields['proposition']}\" in "
                 f"{fields['controlling_authority']}, not {fields['wrong_cite']}.")
    if insight is None:
        return draft
    return insight.rewrite({**fields, "patch_family": family}, draft)


# ──────────────────────────────────────────────
# Family miners
# ──────────────────────────────────────────────

def _selected(node: MissingNode, teacher_index: dict) -> bool:
    real = teacher_index.get(node.teacher_id)
    if isinstance(real, Rule):
        return real.authority in INCLUDED_RULE_AUTHORITIES
    if isinstance(real, Obligation):
        return real.status in INCLUDED_OBLIGATION_STATUSES
    return False


def _mine_missing(node: MissingNode, teacher: LegalReasoningGraph, case: Case,
                  teacher_index: dict, insight: Optional[InsightWriter]) -> Optional[Patch]:
    real = teacher_index.get(node.teacher_id)
    if isinstance(real, Rule):
        citation, jurisdiction, proposition = real.citation, real.jurisdiction, real.label
        keywords = _trigger_keywords(citation, proposition, jurisdiction, case)
        fields = {
            "controlling_authority": citation, "jurisdiction": _canon_jurisdiction(jurisdiction),
            "authority_level": real.authority.value, "proposition": proposition,
            "keywords": keywords, "contraindication": _contraindication_rule(real, teacher),
        }
        prevention = _prevention_step("missing_rule", fields, insight)
        return Patch(
            patch_id=_patch_id("missing_rule", citation, ["R"]),
            patch_family="missing_rule", trigger_keywords=keywords,
            controlling_authority=citation, prevention_step=prevention,
            contraindication=fields["contraindication"], node_types_addressed=["R"],
            source_cases=[case.case_id], jurisdiction=_canon_jurisdiction(jurisdiction),
        )
    if isinstance(real, Obligation):
        # Resolve controlling authority through required_by → rule citation.
        req_rule = teacher_index.get(real.required_by)
        citation = req_rule.citation if isinstance(req_rule, Rule) else real.required_by
        jurisdiction = real.jurisdiction
        keywords = _trigger_keywords(citation, real.label, jurisdiction, case)
        fields = {
            "controlling_authority": citation, "jurisdiction": _canon_jurisdiction(jurisdiction),
            "proposition": real.label, "status": real.status.value,
            "deadline": real.deadline, "keywords": keywords,
            "contraindication": (_contraindication_rule(req_rule, teacher)
                                 if isinstance(req_rule, Rule) else ""),
        }
        prevention = _prevention_step("missing_obligation", fields, insight)
        return Patch(
            patch_id=_patch_id("missing_obligation", citation, ["O"]),
            patch_family="missing_obligation", trigger_keywords=keywords,
            controlling_authority=citation, prevention_step=prevention,
            contraindication=fields["contraindication"], node_types_addressed=["O"],
            source_cases=[case.case_id], jurisdiction=_canon_jurisdiction(jurisdiction),
        )
    return None


def _mine_misground(m: Misgrounding, teacher: LegalReasoningGraph, case: Case,
                    teacher_index: dict, insight: Optional[InsightWriter]) -> Patch:
    real = teacher_index.get(m.teacher_id)
    jurisdiction = real.jurisdiction if isinstance(real, Rule) else ""
    keywords = _trigger_keywords(m.teacher_citation, m.proposition, jurisdiction, case)
    contra = _contraindication_rule(real, teacher) if isinstance(real, Rule) else ""
    fields = {
        "controlling_authority": m.teacher_citation, "wrong_cite": m.student_citation,
        "proposition": m.proposition, "jurisdiction": _canon_jurisdiction(jurisdiction),
        "keywords": keywords, "contraindication": contra,
    }
    prevention = _prevention_step("misgrounding", fields, insight)
    return Patch(
        patch_id=_patch_id("misgrounding", m.teacher_citation, ["R"]),
        patch_family="misgrounding", trigger_keywords=keywords,
        controlling_authority=m.teacher_citation, prevention_step=prevention,
        contraindication=contra, node_types_addressed=["R"],
        source_cases=[case.case_id], jurisdiction=_canon_jurisdiction(jurisdiction),
    )


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────

def generate_patches(
    report: DiscrepancyReport,
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    case: Case,
    *,
    insight: Optional[InsightWriter] = None,
) -> list[Patch]:
    """Mine raw patch candidates from one training-case report (train-only)."""
    if case.role != "training":
        raise ValueError(
            f"patch mining is train-only; {case.case_id} has role={case.role!r}"
        )
    t_index: dict[str, object] = {}
    for r in teacher.rules: t_index[r.rid] = r
    for o in teacher.obligations: t_index[o.oid] = o

    patches: list[Patch] = []
    for node in report.v_miss:
        if _selected(node, t_index):
            p = _mine_missing(node, teacher, case, t_index, insight)
            if p is not None:
                patches.append(p)
    for m in report.v_misground:
        patches.append(_mine_misground(m, teacher, case, t_index, insight))
    return patches


def dedup_merge(patches: Iterable[Patch]) -> list[Patch]:
    """D3: merge patches that describe the same authority + family + node types.

    source_cases and trigger_keywords are unioned; the textual fields are taken
    from the first contributor (deterministic), avoiding a second LLM call.
    """
    buckets: dict[tuple, Patch] = {}
    for p in patches:
        key = (p.patch_family,
               frozenset(extract_citation_tokens(p.controlling_authority)
                         or {p.controlling_authority.strip().lower()}),
               tuple(sorted(p.node_types_addressed)))
        if key not in buckets:
            buckets[key] = p.model_copy(deep=True)
        else:
            cur = buckets[key]
            cur.source_cases = sorted(set(cur.source_cases) | set(p.source_cases))
            seen = set(cur.trigger_keywords)
            cur.trigger_keywords += [k for k in p.trigger_keywords if k not in seen]
    return list(buckets.values())


def generate_all(
    cases: list[tuple[DiscrepancyReport, LegalReasoningGraph, LegalReasoningGraph, Case]],
    *,
    insight: Optional[InsightWriter] = None,
) -> list[Patch]:
    """Mine + dedup across multiple training cases.

    ``cases`` is a list of (report, teacher_graph, student_graph, case) tuples,
    assembled by the caller from the snapshot + graphs dirs (training cases only).
    """
    raw: list[Patch] = []
    for report, teacher, student, case in cases:
        raw += generate_patches(report, teacher, student, case, insight=insight)
    return dedup_merge(raw)


__all__ = [
    "InsightWriter", "Patch", "generate_patches", "dedup_merge", "generate_all",
    "LEGAL_LEXICON", "OPERATIVE_DATE",
]
