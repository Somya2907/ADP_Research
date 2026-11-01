"""Iterative patch learning: how many rounds until the weak student stops improving?

The original method is single-pass (mine patches once, inject, score). This
module repeats it. Round 0 is the unpatched baseline. Each later round:

1. **Generate** — every training and test case is answered with the top-k
   patches from the current store in the prompt.
2. **Score** — L-GED against the teacher for every case. Test cases are scored
   only; nothing about them ever reaches the store.
3. **Efficacy (training only)** — for each patch that was injected, did the gap
   it targets close in that case this round?
4. **Update the store**
   * *re-mine*: diff the patched student against the teacher and add patches
     for errors that were not in the store yet;
   * *rewrite*: a patch that has been injected and has never closed its gap is
     rewritten by Claude (bounded, guard-railed);
   * *reprioritise*: a patch that closed its gap when injected is boosted in
     retrieval, one that was injected and failed is demoted, and an untested
     patch is left alone (an additive term on the BM25 score; see
     ``PatchStore.retrieve``). Because untested patches are neutral, round 1 is
     exactly the single-pass method and serves as the control.
5. **Stop** when the prompts stop changing (fixpoint), when neither the test
   curve nor the training curve has improved by more than epsilon for
   ``patience`` rounds (plateau), or at ``max_rounds``. Waiting for both curves
   means the run also shows where the training cases level off.

The student has no memory between rounds: everything it "learns" is carried by
the store. With a fixed budget of k patches per prompt, learning means the store
finding out which k patches work, so the curve is expected to rise and flatten.

Everything here is deterministic given a deterministic student, and takes the
student as a function, so it is testable without a model.
"""
from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from typing import Callable, Iterable, Optional

from .alignment import AlignmentReport, align_all, extract_citation_tokens
from .cases import Case
from .discrepancy import DiscrepancyReport, compute_discrepancies
from .injection import filter_leaks, render_notes_block
from .patch_generator import _canon_jurisdiction, dedup_merge, generate_patches
from .patch_store import Patch, PatchStore
from .schema import GraphSource, LegalReasoningGraph, Rule

# (case, notes_block, round) -> the student's graph, or None if its answer
# could not be parsed into a graph.
StudentFn = Callable[[Case, str, int], Optional[LegalReasoningGraph]]


# Function words removed from the case text before BM25 scoring (see
# PatchStore.retrieve). Deliberately short and closed-class: no legal terms.
STOPWORDS = frozenset("""
a an the of to in on for and or nor but is are was were be been being as at by with
from that this these those it its their they them there which who whom whose what
when where if than then so such not no any all each per into under over about after
before between during through against only also both either neither can could may
might must shall should will would do does did done has have had having other more
most some own same very
""".split())


@dataclass
class LoopConfig:
    k: int = 3                       # patches per prompt (fixed budget)
    max_rounds: int = 8              # last round index (round 0 is the baseline)
    allowed: frozenset = frozenset({"verified", "unverified"})  # fabricated excluded
    diversify: bool = True           # at most one patch per legal duty
    jurisdiction_gate: bool = True   # only patches from the case's own jurisdictions
    priority_alpha: float = 0.5      # strength of the retrieval boost
    rewrite: bool = True             # let the writer rewrite failing patches
    max_rewrites: int = 2            # per patch
    epsilon_frac: float = 0.01       # plateau threshold as a share of round-0 mean test L-GED
    patience: int = 2                # rounds without improvement before stopping


@dataclass
class CaseRound:
    round: int
    case_id: str
    split: str                       # "training" | "test"
    tier: str
    parsed: bool                     # False → scored as an empty graph
    l_ged: float
    v_miss: int
    v_halluc: int
    e_diff: int
    v_misground: int
    ro_total: int                    # teacher Rules + Obligations
    ro_recovered: int                # of those, aligned in the student graph
    retrieved: list[str] = field(default_factory=list)   # "patch_id@version"


@dataclass
class RoundSummary:
    round: int
    store_size: int                  # patches in the store used for this round
    dropped_for_party_names: int     # held back by the leakage guard
    new_patches: int                 # added from this round's training graphs
    rewritten: int                   # rewritten after this round
    rewrites_rejected: int           # rewrites discarded by a guardrail
    mean_lged_train: float
    mean_lged_test: float
    ro_recovery_train: float         # share of teacher Rules+Obligations recovered
    ro_recovery_test: float
    unparsed: int
    by_tier: dict = field(default_factory=dict)   # {"test/easy": mean L-GED, ...}


@dataclass
class LoopResult:
    config: dict
    rounds: list[RoundSummary]
    cases: list[CaseRound]
    stop_reason: str                 # "plateau" | "fixpoint" | "max_rounds"
    best_round: int                  # round with the best mean test L-GED
    epsilon: float
    stores: dict[int, list[dict]] = field(default_factory=dict)  # round -> store used


# ──────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────

def empty_graph(case_id: str) -> LegalReasoningGraph:
    """What an unparseable answer is scored as: it recovers nothing."""
    return LegalReasoningGraph(case_id=case_id, source=GraphSource.AGENT,
                               model_name="unparsed", agent_id=None)


def score(teacher: LegalReasoningGraph, student: LegalReasoningGraph,
          ) -> tuple[DiscrepancyReport, AlignmentReport]:
    alignment = align_all(teacher, student)
    return compute_discrepancies(teacher, student, alignment), alignment


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


# ──────────────────────────────────────────────
# Efficacy — did an injected patch close its gap?
# ──────────────────────────────────────────────

def _tokens(citation: str) -> set[str]:
    return extract_citation_tokens(citation) or {(citation or "").strip().lower()}


def patch_targets(patch: Patch, teacher: LegalReasoningGraph) -> list[str]:
    """Teacher node ids this patch is about, within one case's teacher graph.

    Rule patches (missing_rule, misgrounding) target the teacher Rules that
    cite the patch's authority. Obligation patches target the Obligations
    required by such a Rule. A patch about an authority the teacher never
    used in this case has no targets here and is neither helped nor blamed.
    """
    want = _tokens(patch.controlling_authority)
    rule_ids = [r.rid for r in teacher.rules if _tokens(r.citation) & want]
    if patch.patch_family != "missing_obligation":
        return rule_ids
    rules = {r.rid: r for r in teacher.rules}
    targets = []
    for o in teacher.obligations:
        req = rules.get(o.required_by)
        cite = req.citation if isinstance(req, Rule) else o.required_by
        if _tokens(cite) & want:
            targets.append(o.oid)
    return targets


def patch_outcome(patch: Patch, teacher: LegalReasoningGraph,
                  report: DiscrepancyReport, alignment: AlignmentReport) -> tuple[int, int]:
    """(targets, closed) for one injected patch in one training case."""
    targets = patch_targets(patch, teacher)
    if not targets:
        return 0, 0
    if patch.patch_family == "missing_obligation":
        closed = sum(1 for t in targets if alignment.obligation_map.get(t) is not None)
    elif patch.patch_family == "misgrounding":
        still_wrong = {m.teacher_id for m in report.v_misground}
        closed = sum(1 for t in targets
                     if alignment.rule_map.get(t) is not None and t not in still_wrong)
    else:  # missing_rule
        closed = sum(1 for t in targets if alignment.rule_map.get(t) is not None)
    return len(targets), closed


# ──────────────────────────────────────────────
# Store update
# ──────────────────────────────────────────────

def merge_mined(store: PatchStore, candidates: Iterable[Patch], round_idx: int) -> int:
    """Add newly mined patches; widen the evidence on ones already stored.

    Returns how many patches were new. ``source_cases`` of an existing patch
    grows to every training case in which its error has been seen — that count
    is the "how common is this error" term of the priority.
    """
    new = 0
    for cand in dedup_merge(candidates):
        cur = store.get(cand.patch_id)
        if cur is None:
            cand.round_added = round_idx
            store.add(cand)
            new += 1
            continue
        cur.source_cases = sorted(set(cur.source_cases) | set(cand.source_cases))
        seen = set(cur.trigger_keywords)
        extra = [k for k in cand.trigger_keywords if k not in seen]
        if extra:
            cur.trigger_keywords = (cur.trigger_keywords + extra)[:12]
            store.add(cur)  # keywords changed → rebuild the BM25 index
    return new


def update_priorities(store: PatchStore) -> None:
    """priority = 2 × (share of targeted gaps the patch closed) − 1, in [-1, 1].

    +1 for a patch that closed every gap it was injected against, −1 for one
    that closed none, 0 for a patch with no evidence yet. Only evidence the loop
    has gathered moves a patch, so before any injection every priority is 0 and
    retrieval is plain BM25.
    """
    for p in store.all():
        p.priority = (2.0 * p.n_resolved / p.n_injected - 1.0) if p.n_injected else 0.0


_SECTION_LIKE = re.compile(r"\d[\d.\-]*\d(?:\([^()\s]+\))*")


def _section_bases(text: str) -> set[str]:
    """Base section numbers written in ``text`` (e.g. "6-1-1703", "551.051").

    Only tokens with a hyphen or dot count, so plain numbers and years do not.
    """
    out = set()
    for tok in _SECTION_LIKE.findall(text or ""):
        base = tok.split("(")[0].strip(".-")
        if ("-" in base or "." in base) and sum(ch.isdigit() for ch in base) >= 3:
            out.add(base.lower())
    return out


def rewrite_is_acceptable(patch: Patch, new_text: str, party_names: Iterable[str]) -> bool:
    """Guardrails on a rewritten patch. Any failure discards the rewrite."""
    text = (new_text or "").strip()
    if not text or text == patch.prevention_step.strip() or len(text) > 700:
        return False
    low = text.lower()
    if any(name.lower() in low for name in party_names):
        return False                                  # must stay party-free
    allowed = (_section_bases(patch.controlling_authority)
               | _section_bases(patch.prevention_step)
               | _section_bases(patch.contraindication))
    return _section_bases(text) <= allowed            # no new statutory sections


_FAILURE_NOTE = {
    "missing_rule": "After reading the note, the model's analysis still contained "
                    "no rule grounded in the controlling authority.",
    "missing_obligation": "After reading the note, the model's analysis still listed "
                          "no obligation arising under the controlling authority.",
    "misgrounding": "After reading the note, the model still attached this proposition "
                    "to a different citation instead of the controlling authority.",
}


def rewrite_failing(store: PatchStore, writer, cfg: LoopConfig,
                    party_names: Iterable[str]) -> tuple[int, int]:
    """Rewrite patches that were injected and never closed a gap.

    Returns (rewritten, rejected). A rewritten patch starts over as untested
    (its counters reset) so the new wording gets a fair trial.
    """
    rewritten = rejected = 0
    names = list(party_names)
    for p in store.all():
        failing = p.n_injected > 0 and p.n_resolved == 0
        if not failing or p.n_rewrite_attempts >= cfg.max_rewrites:
            continue
        fields = {
            "patch_family": p.patch_family,
            "controlling_authority": p.controlling_authority,
            "jurisdiction": p.jurisdiction,
            "contraindication": p.contraindication,
        }
        new_text = writer.rewrite_failed(fields, p.prevention_step,
                                         _FAILURE_NOTE[p.patch_family])
        p.n_rewrite_attempts += 1          # an attempt counts, accepted or not
        if rewrite_is_acceptable(p, new_text, names):
            p.history.append(p.prevention_step)
            p.prevention_step = new_text.strip()
            p.version += 1
            p.n_injected = p.n_resolved = 0   # new wording starts untested
            rewritten += 1
        else:
            rejected += 1                  # text and record unchanged
    return rewritten, rejected


# ──────────────────────────────────────────────
# The loop
# ──────────────────────────────────────────────

def _retrieve(store: PatchStore, case: Case, cfg: LoopConfig) -> list[Patch]:
    query = f"{case.facts}\n{case.question}"
    kw = dict(k=cfg.k, allowed=cfg.allowed, diversify=cfg.diversify,
              priority_alpha=cfg.priority_alpha, stopwords=STOPWORDS)
    if cfg.jurisdiction_gate:
        juris = {_canon_jurisdiction(t) for t in case.jurisdiction_tags}
        if juris:
            # A patch about another jurisdiction's law is never injected. If the
            # case's own jurisdictions have nothing relevant, it gets fewer notes.
            return store.retrieve(query, jurisdictions=juris, **kw)
    return store.retrieve(query, **kw)


def run_loop(
    train: list[Case],
    test: list[Case],
    teachers: dict[str, LegalReasoningGraph],
    student: StudentFn,
    cfg: LoopConfig = LoopConfig(),
    *,
    index=None,
    writer=None,
    party_names: Iterable[str] = (),
    on_round: Optional[Callable[[RoundSummary, list[CaseRound], list[dict]], None]] = None,
) -> LoopResult:
    """Run the loop until it stops. See the module docstring for the round structure.

    ``index`` is the optional StatuteIndex used to classify mined patches.
    ``writer`` needs a ``rewrite_failed(fields, current, failure)`` method; it is
    only called when ``cfg.rewrite`` is true. ``party_names`` feeds the leakage
    guard and the rewrite guardrail.
    """
    for c in test:
        if c.role == "training":
            raise ValueError(f"{c.case_id} is a training case but was passed as test")
    names = list(party_names)
    store = PatchStore()
    rounds: list[RoundSummary] = []
    all_cases: list[CaseRound] = []
    stores: dict[int, list[dict]] = {}
    prev_sig: Optional[dict] = None
    best, best_round, stale, epsilon = math.inf, 0, 0, 0.0
    best_train, stale_train, epsilon_train = math.inf, 0, 0.0
    stop_reason = "max_rounds"

    for t in range(cfg.max_rounds + 1):
        usable, dropped = filter_leaks(store, names)
        retrieved = {c.case_id: (_retrieve(usable, c, cfg) if t > 0 else [])
                     for c in train + test}
        sig = {cid: tuple((p.patch_id, p.version) for p in ps)
               for cid, ps in retrieved.items()}
        if t >= 1 and sig == prev_sig:
            stop_reason = "fixpoint"   # same prompts as last round → same answers
            break
        prev_sig = sig
        store_used = [p.model_dump() for p in store.all()]
        stores[t] = store_used

        rows: list[CaseRound] = []
        observed = []   # parsed training cases: (case, graph, report, alignment)
        for case in train + test:
            teacher = teachers[case.case_id]
            graph = student(case, render_notes_block(retrieved[case.case_id]), t)
            parsed = graph is not None
            report, alignment = score(teacher, graph if parsed else empty_graph(case.case_id))
            ro_total = len(teacher.rules) + len(teacher.obligations)
            ro_rec = (sum(1 for v in alignment.rule_map.values() if v is not None)
                      + sum(1 for v in alignment.obligation_map.values() if v is not None))
            rows.append(CaseRound(
                round=t, case_id=case.case_id, split=case.role, tier=case.tier,
                parsed=parsed, l_ged=report.l_ged, v_miss=len(report.v_miss),
                v_halluc=len(report.v_halluc), e_diff=len(report.e_diff),
                v_misground=len(report.v_misground), ro_total=ro_total, ro_recovered=ro_rec,
                retrieved=[f"{p.patch_id}@{p.version}" for p in retrieved[case.case_id]],
            ))
            if case.role == "training" and parsed:
                observed.append((case, graph, report, alignment))

        # efficacy of what was injected (training cases only)
        for case, _graph, report, alignment in observed:
            for patch in retrieved[case.case_id]:
                n, closed = patch_outcome(patch, teachers[case.case_id], report, alignment)
                patch.n_injected += n
                patch.n_resolved += closed

        # re-mine from the (patched) training graphs
        candidates: list[Patch] = []
        for case, graph, report, _alignment in observed:
            candidates += generate_patches(report, teachers[case.case_id], graph, case,
                                           insight=None, index=index)
        n_new = merge_mined(store, candidates, t)

        n_rw = n_rej = 0
        if cfg.rewrite and writer is not None:
            n_rw, n_rej = rewrite_failing(store, writer, cfg, names)
        update_priorities(store)

        def _rows(split, tier=None):
            return [r for r in rows if r.split == split and (tier is None or r.tier == tier)]

        def _recovery(rs):
            tot = sum(r.ro_total for r in rs)
            return sum(r.ro_recovered for r in rs) / tot if tot else 0.0

        by_tier = {}
        for split in ("training", "test"):
            for tier in sorted({r.tier for r in rows}):
                rs = _rows(split, tier)
                if rs:
                    by_tier[f"{split}/{tier}"] = round(_mean([r.l_ged for r in rs]), 2)
        summary = RoundSummary(
            round=t, store_size=len(store_used), dropped_for_party_names=len(dropped),
            new_patches=n_new, rewritten=n_rw, rewrites_rejected=n_rej,
            mean_lged_train=round(_mean([r.l_ged for r in _rows("training")]), 2),
            mean_lged_test=round(_mean([r.l_ged for r in _rows("test")]), 2),
            ro_recovery_train=round(_recovery(_rows("training")), 4),
            ro_recovery_test=round(_recovery(_rows("test")), 4),
            unparsed=sum(1 for r in rows if not r.parsed), by_tier=by_tier,
        )
        rounds.append(summary)
        all_cases.extend(rows)
        if on_round is not None:
            on_round(summary, rows, store_used)

        # plateau: have both curves stopped improving? ``best_round`` tracks the
        # held-out curve; the training curve only delays the stop.
        m = summary.mean_lged_test if test else summary.mean_lged_train
        m_train = summary.mean_lged_train
        if t == 0:
            epsilon, epsilon_train = cfg.epsilon_frac * m, cfg.epsilon_frac * m_train
            best, best_round, best_train = m, 0, m_train
        else:
            if m < best - epsilon:
                best, best_round, stale = m, t, 0
            else:
                stale += 1
            if m_train < best_train - epsilon_train:
                best_train, stale_train = m_train, 0
            else:
                stale_train += 1
            if stale >= cfg.patience and stale_train >= cfg.patience:
                stop_reason = "plateau"
                break

    return LoopResult(config=asdict(cfg) | {"allowed": sorted(cfg.allowed)},
                      rounds=rounds, cases=all_cases, stop_reason=stop_reason,
                      best_round=best_round, epsilon=round(epsilon, 3), stores=stores)


def plateau_round(means: list[float], epsilon: float) -> int:
    """Round with the best value, where 'better' means lower by more than epsilon."""
    best, best_round = math.inf, 0
    for t, m in enumerate(means):
        if t == 0 or m < best - epsilon:
            best, best_round = m, t
    return best_round


__all__ = [
    "STOPWORDS", "LoopConfig", "CaseRound", "RoundSummary", "LoopResult", "StudentFn",
    "run_loop", "score", "empty_graph", "patch_targets", "patch_outcome",
    "merge_mined", "update_priorities", "rewrite_failing", "rewrite_is_acceptable",
    "plateau_round",
]
