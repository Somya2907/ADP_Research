"""Node-level alignment between a teacher graph and a student graph.

Two-stage matching:

1. Rules use **citation-based** matching first: when both rules cite the same
   statutory section (after normalising "§ 20-871(d)(2)" vs "Section
   20-871(d)(2)" to a canonical form), they are aligned with high confidence.
2. Everything else (facts, issues, applications, conclusions, obligations) and
   any rules left unaligned after step 1 fall back to text similarity. Two
   backends are available, selected by ``LEX_DRL_SIMILARITY``:

   * ``tfidf`` (default) — n-gram TF-IDF cosine, threshold tuned to 0.10.
   * ``embedding`` — sentence-transformers cosine via
     ``BAAI/bge-small-en-v1.5``, threshold tuned to 0.55. Survives legal
     paraphrases that TF-IDF misses.

The output is an :class:`AlignmentReport` consumed by
:mod:`lex_drl.discrepancy`.
"""
from __future__ import annotations

import os
import re
from typing import Callable, Iterable, Optional

from pydantic import BaseModel, Field

from .schema import (
    Application,
    Conclusion,
    Fact,
    Issue,
    LegalReasoningGraph,
    Obligation,
    Rule,
)

SIMILARITY_METHOD = os.environ.get("LEX_DRL_SIMILARITY", "tfidf").lower()
EMBEDDING_MODEL_NAME = os.environ.get(
    "LEX_DRL_EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"
)
DEFAULT_THRESHOLD = 0.55 if SIMILARITY_METHOD == "embedding" else 0.10

_EMBED_MODEL = None  # lazy-loaded SentenceTransformer instance


def _get_embed_model():
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        from sentence_transformers import SentenceTransformer
        _EMBED_MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _EMBED_MODEL


# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────

class AlignmentMatch(BaseModel):
    """One teacher → student node alignment decision."""

    teacher_id: str
    student_id: Optional[str]
    similarity: float
    method: str  # "citation" | "tfidf" | "none"


class AlignmentReport(BaseModel):
    """Per-case alignment between a teacher and a student graph."""

    case_id: str
    fact_map: dict[str, Optional[str]] = Field(default_factory=dict)
    issue_map: dict[str, Optional[str]] = Field(default_factory=dict)
    rule_map: dict[str, Optional[str]] = Field(default_factory=dict)
    application_map: dict[str, Optional[str]] = Field(default_factory=dict)
    conclusion_map: dict[str, Optional[str]] = Field(default_factory=dict)
    obligation_map: dict[str, Optional[str]] = Field(default_factory=dict)
    confidence: float = 0.0
    unaligned_teacher: list[str] = Field(default_factory=list)
    unaligned_student: list[str] = Field(default_factory=list)
    per_type_counts: dict[str, dict[str, int]] = Field(default_factory=dict)
    matches: list[AlignmentMatch] = Field(default_factory=list)

    def all_maps(self) -> dict[str, dict[str, Optional[str]]]:
        return {
            "fact": self.fact_map, "issue": self.issue_map,
            "rule": self.rule_map, "application": self.application_map,
            "conclusion": self.conclusion_map, "obligation": self.obligation_map,
        }

    def teacher_to_student(self, teacher_id: str) -> Optional[str]:
        """Return the student node id aligned to ``teacher_id``, or None."""
        for m in self.all_maps().values():
            if teacher_id in m:
                return m[teacher_id]
        return None


# ──────────────────────────────────────────────
# Citation normalisation
# ──────────────────────────────────────────────

_SECTION_TOKEN = re.compile(
    r"(?:§|sec(?:tion|\.)?)\s*([0-9A-Za-z][\w\-.()]*)",
    flags=re.IGNORECASE,
)


def extract_citation_tokens(citation: str) -> set[str]:
    """Extract a canonical set of statute tokens from a citation string.

    "§20-871(d)(2)" and "Section 20-871(d)(2)" both yield {"20-871(d)(2)"}.
    Returns an empty set if no recognisable token is present.
    """
    if not citation:
        return set()
    tokens: set[str] = set()
    for match in _SECTION_TOKEN.finditer(citation):
        raw = match.group(1).strip().rstrip(".,;:")
        if raw:
            tokens.add(raw.lower())
    return tokens


def citations_match(a: str, b: str) -> bool:
    """True iff the two citations share at least one normalised section token."""
    return bool(extract_citation_tokens(a) & extract_citation_tokens(b))


# ──────────────────────────────────────────────
# TF-IDF helper
# ──────────────────────────────────────────────

def _embedding_cosine_matrix(teacher_texts: list[str], student_texts: list[str]):
    """Return cosine-similarity matrix using a sentence-transformer model.

    Texts are encoded with L2-normalised embeddings so cosine reduces to a
    matrix multiply. Falls back to TF-IDF if sentence-transformers is missing.
    """
    if not teacher_texts or not student_texts:
        return [[0.0] * len(student_texts) for _ in teacher_texts]
    try:
        model = _get_embed_model()
        t_emb = model.encode(teacher_texts, normalize_embeddings=True, show_progress_bar=False)
        s_emb = model.encode(student_texts, normalize_embeddings=True, show_progress_bar=False)
        return (t_emb @ s_emb.T).tolist()
    except (ImportError, OSError):
        return _cosine_matrix(teacher_texts, student_texts)


def _cosine_matrix(teacher_texts: list[str], student_texts: list[str]):
    """Return a (len(teacher) × len(student)) cosine-similarity matrix.

    Falls back gracefully if scikit-learn isn't available or the corpus has
    only stop words — in that case every entry is 1.0 if the strings are
    identical (case-insensitive) and 0.0 otherwise.
    """
    if not teacher_texts or not student_texts:
        return [[0.0] * len(student_texts) for _ in teacher_texts]
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vec = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
        matrix = vec.fit_transform(teacher_texts + student_texts)
        t = matrix[: len(teacher_texts)]
        s = matrix[len(teacher_texts):]
        return cosine_similarity(t, s).tolist()
    except (ImportError, ValueError):
        # Degenerate corpus (all stop words) or sklearn missing → exact match.
        out = []
        for tt in teacher_texts:
            row = []
            for st in student_texts:
                row.append(1.0 if tt.strip().lower() == st.strip().lower() and tt.strip() else 0.0)
            out.append(row)
        return out


def _greedy_assign(
    teacher_ids: list[str],
    student_ids: list[str],
    sim: list[list[float]],
    threshold: float,
) -> list[tuple[str, Optional[str], float]]:
    """Greedy bipartite max-similarity assignment under a threshold.

    Picks the highest cosine each round, locks the row and column, repeats.
    Each student id can be matched to at most one teacher id.
    """
    if not teacher_ids:
        return []
    if not student_ids:
        return [(tid, None, 0.0) for tid in teacher_ids]

    used_student: set[int] = set()
    used_teacher: set[int] = set()
    results: dict[str, tuple[Optional[str], float]] = {}

    while len(used_teacher) < len(teacher_ids) and len(used_student) < len(student_ids):
        best = (-1.0, -1, -1)
        for i in range(len(teacher_ids)):
            if i in used_teacher:
                continue
            for j in range(len(student_ids)):
                if j in used_student:
                    continue
                if sim[i][j] > best[0]:
                    best = (sim[i][j], i, j)
        score, i, j = best
        if i < 0 or score < threshold:
            break
        results[teacher_ids[i]] = (student_ids[j], score)
        used_teacher.add(i)
        used_student.add(j)

    out: list[tuple[str, Optional[str], float]] = []
    for tid in teacher_ids:
        sid_score = results.get(tid)
        if sid_score is None:
            out.append((tid, None, 0.0))
        else:
            out.append((tid, sid_score[0], sid_score[1]))
    return out


def _align_by_text(
    teacher_nodes: Iterable[BaseModel],
    student_nodes: Iterable[BaseModel],
    id_attr: str,
    text_fn: Callable[[BaseModel], str],
    threshold: float = DEFAULT_THRESHOLD,
) -> tuple[dict[str, Optional[str]], list[AlignmentMatch]]:
    """TF-IDF cosine alignment with greedy assignment.

    Returns ``(map, matches)`` where ``map`` is teacher_id → student_id|None
    and ``matches`` records the similarity and method per teacher node.
    """
    teacher_list = list(teacher_nodes)
    student_list = list(student_nodes)

    t_ids = [getattr(n, id_attr) for n in teacher_list]
    s_ids = [getattr(n, id_attr) for n in student_list]
    t_text = [text_fn(n) or "" for n in teacher_list]
    s_text = [text_fn(n) or "" for n in student_list]

    if SIMILARITY_METHOD == "embedding":
        sim = _embedding_cosine_matrix(t_text, s_text)
    else:
        sim = _cosine_matrix(t_text, s_text)
    assignments = _greedy_assign(t_ids, s_ids, sim, threshold)

    mapping: dict[str, Optional[str]] = {}
    matches: list[AlignmentMatch] = []
    for tid, sid, score in assignments:
        mapping[tid] = sid
        matches.append(AlignmentMatch(
            teacher_id=tid,
            student_id=sid,
            similarity=float(score),
            method=SIMILARITY_METHOD if sid is not None else "none",
        ))
    return mapping, matches


# ──────────────────────────────────────────────
# Public per-type functions
# ──────────────────────────────────────────────

def align_facts(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Optional[str]]:
    """Map each teacher fact id to the best student fact id (or None).

    Uses TF-IDF cosine similarity on the ``label`` field with a configurable
    threshold (default 0.4).
    """
    mapping, _ = _align_by_text(
        teacher.facts, student.facts, "fid",
        lambda f: f.label, threshold=threshold,
    )
    return mapping


def align_issues(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Optional[str]]:
    """Map each teacher issue id to the best student issue id (or None)."""
    mapping, _ = _align_by_text(
        teacher.issues, student.issues, "iid",
        lambda i: i.label, threshold=threshold,
    )
    return mapping


def align_rules(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Optional[str]]:
    """Map each teacher rule id to the best student rule id (or None).

    Citation tokens are normalised and matched first (e.g. "§20-871(d)(2)" ≡
    "Section 20-871(d)(2)"). Rules with no citation match fall back to label
    TF-IDF.
    """
    mapping: dict[str, Optional[str]] = {}
    used_student: set[str] = set()

    # Step 1 — citation match.
    for t_rule in teacher.rules:
        t_tokens = extract_citation_tokens(t_rule.citation)
        match_id: Optional[str] = None
        if t_tokens:
            for s_rule in student.rules:
                if s_rule.rid in used_student:
                    continue
                if extract_citation_tokens(s_rule.citation) & t_tokens:
                    match_id = s_rule.rid
                    used_student.add(match_id)
                    break
        if match_id is not None:
            mapping[t_rule.rid] = match_id

    # Step 2 — TF-IDF on unmatched rules.
    remaining_teacher = [r for r in teacher.rules if r.rid not in mapping]
    remaining_student = [r for r in student.rules if r.rid not in used_student]
    if remaining_teacher:
        text_mapping, _ = _align_by_text(
            remaining_teacher, remaining_student, "rid",
            lambda r: f"{r.label} {r.citation}",
            threshold=threshold,
        )
        mapping.update(text_mapping)

    return mapping


def align_applications(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Optional[str]]:
    mapping, _ = _align_by_text(
        teacher.applications, student.applications, "aid",
        lambda a: a.reasoning, threshold=threshold,
    )
    return mapping


def align_conclusions(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Optional[str]]:
    mapping, _ = _align_by_text(
        teacher.conclusions, student.conclusions, "cid",
        lambda c: f"{c.determination.value} {' '.join(c.support_refs)}",
        threshold=threshold,
    )
    return mapping


def align_obligations(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Optional[str]]:
    mapping, _ = _align_by_text(
        teacher.obligations, student.obligations, "oid",
        lambda o: f"{o.label} {o.required_by}",
        threshold=threshold,
    )
    return mapping


# ──────────────────────────────────────────────
# Combined entry point
# ──────────────────────────────────────────────

def _matches_for(
    teacher_ids: list[str],
    mapping: dict[str, Optional[str]],
    method_default: str,
) -> list[AlignmentMatch]:
    out: list[AlignmentMatch] = []
    for tid in teacher_ids:
        sid = mapping.get(tid)
        out.append(AlignmentMatch(
            teacher_id=tid,
            student_id=sid,
            similarity=1.0 if sid else 0.0,
            method=method_default if sid else "none",
        ))
    return out


def align_all(
    teacher: LegalReasoningGraph,
    student: LegalReasoningGraph,
    threshold: float = DEFAULT_THRESHOLD,
) -> AlignmentReport:
    """Align every node type and return a single :class:`AlignmentReport`.

    The ``confidence`` field is the fraction of teacher nodes that received
    a student match across all node types (1.0 means full coverage).
    ``unaligned_teacher`` lists teacher node ids with no match, and
    ``unaligned_student`` lists student node ids no teacher node mapped to.
    """
    fact_map = align_facts(teacher, student, threshold)
    issue_map = align_issues(teacher, student, threshold)
    rule_map = align_rules(teacher, student, threshold)
    app_map = align_applications(teacher, student, threshold)
    conc_map = align_conclusions(teacher, student, threshold)
    obl_map = align_obligations(teacher, student, threshold)

    all_maps = {
        "fact": fact_map, "issue": issue_map, "rule": rule_map,
        "application": app_map, "conclusion": conc_map, "obligation": obl_map,
    }

    per_type_counts: dict[str, dict[str, int]] = {}
    aligned_total = 0
    teacher_total = 0
    aligned_student_ids: set[str] = set()
    unaligned_teacher: list[str] = []

    for label, mapping in all_maps.items():
        n_teacher = len(mapping)
        n_aligned = sum(1 for v in mapping.values() if v is not None)
        per_type_counts[label] = {
            "teacher": n_teacher,
            "aligned": n_aligned,
            "unaligned": n_teacher - n_aligned,
        }
        aligned_total += n_aligned
        teacher_total += n_teacher
        for tid, sid in mapping.items():
            if sid is None:
                unaligned_teacher.append(tid)
            else:
                aligned_student_ids.add(sid)

    confidence = (aligned_total / teacher_total) if teacher_total else 1.0

    student_ids = {n.fid for n in student.facts}
    student_ids |= {n.iid for n in student.issues}
    student_ids |= {n.rid for n in student.rules}
    student_ids |= {n.aid for n in student.applications}
    student_ids |= {n.cid for n in student.conclusions}
    student_ids |= {n.oid for n in student.obligations}
    unaligned_student = sorted(student_ids - aligned_student_ids)

    matches: list[AlignmentMatch] = []
    matches += _matches_for([f.fid for f in teacher.facts], fact_map, SIMILARITY_METHOD)
    matches += _matches_for([i.iid for i in teacher.issues], issue_map, SIMILARITY_METHOD)
    matches += _matches_for([r.rid for r in teacher.rules], rule_map, "citation")
    matches += _matches_for([a.aid for a in teacher.applications], app_map, SIMILARITY_METHOD)
    matches += _matches_for([c.cid for c in teacher.conclusions], conc_map, SIMILARITY_METHOD)
    matches += _matches_for([o.oid for o in teacher.obligations], obl_map, SIMILARITY_METHOD)

    return AlignmentReport(
        case_id=teacher.case_id,
        fact_map=fact_map,
        issue_map=issue_map,
        rule_map=rule_map,
        application_map=app_map,
        conclusion_map=conc_map,
        obligation_map=obl_map,
        confidence=confidence,
        unaligned_teacher=sorted(unaligned_teacher),
        unaligned_student=unaligned_student,
        per_type_counts=per_type_counts,
        matches=matches,
    )


__all__ = [
    "AlignmentMatch",
    "AlignmentReport",
    "DEFAULT_THRESHOLD",
    "align_all",
    "align_applications",
    "align_conclusions",
    "align_facts",
    "align_issues",
    "align_obligations",
    "align_rules",
    "citations_match",
    "extract_citation_tokens",
]
