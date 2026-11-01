"""Iterative learning with checklist patches: at which round does the student stop improving?

Same question and round structure as lex_drl.loop (Phase 5), with the patch
format that worked (lex_drl.checklist): k checklist items mined from training
cases, picked by case similarity + how often they were missed.

Round 0 is the unpatched baseline. Each later round:

1. **Generate** — every training and test case is answered with its top-k
   checklist items in the prompt.
2. **Score** — L-GED against the teacher. Test cases are scored only; nothing
   about them reaches the store.
3. **Efficacy (training only)** — for each item shown to a training case: did it
   match a real teacher node of that case (*useful*), and did the student write
   that node (*resolved*)?
4. **Update the store**
   * *re-mine*: what the patched training students still miss becomes new items;
   * *re-rank*: ``priority = 2 × resolved / given − 1`` — an item that closes its
     gap rises, one that is shown but does not help (irrelevant, or ignored)
     falls; untested items stay at 0;
   * *swap wording*: an item that was useful at least twice and never resolved
     is shown with another training case's wording (at most ``max_swaps``).
     Deterministic, no LLM: in Stage B, Claude-written notes did worse.
5. **Stop** when the prompts stop changing (fixpoint), when neither the test nor
   the training curve has improved by more than epsilon for ``patience`` rounds
   (plateau), or at ``max_rounds``.

With priorities at 0, round 1 is exactly the single-pass checklist method.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Callable, Iterable, Optional

from .cases import Case
from .checklist import (
    Cluster, Embed, match_pairs, missed_items, rank, render_checklist, teacher_targets,
)
from .loop import CaseRound, empty_graph, score
from .schema import LegalReasoningGraph

# (case, notes_block, round) -> the student's graph, or None if unparseable
StudentFn = Callable[[Case, str, int], Optional[LegalReasoningGraph]]


@dataclass
class ChecklistLoopConfig:
    k: int = 10
    max_rounds: int = 5
    support_weight: float = 0.5
    priority_alpha: float = 0.25     # weight of the learned priority in the ranking
    max_swaps: int = 2
    epsilon_frac: float = 0.01       # plateau threshold, share of the round-0 mean
    patience: int = 2


@dataclass
class ChecklistRound:
    round: int
    clusters: int                    # items in the store used for this round
    new_clusters: int                # added from this round's training answers
    swapped: int                     # wordings swapped after this round
    given_train: int                 # item showings to training cases
    useful_train: int
    resolved_train: int
    mean_lged_train: float
    mean_lged_test: float
    ro_recovery_train: float
    ro_recovery_test: float
    unparsed: int
    by_tier: dict = field(default_factory=dict)


@dataclass
class ChecklistLoopResult:
    config: dict
    rounds: list[ChecklistRound]
    cases: list[CaseRound]
    stop_reason: str
    best_round: int                  # round with the best mean test L-GED
    best_round_train: int
    epsilon: float
    stores: dict[int, list[dict]] = field(default_factory=dict)


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def cluster_record(c: Cluster) -> dict:
    rep = c.representative()
    return {"key": c.key, "kind": c.kind, "jurisdiction": c.jurisdiction,
            "support": c.support, "given": c.given, "useful": c.useful,
            "resolved": c.resolved, "priority": round(c.priority, 3), "swaps": c.swaps,
            "shown": {"citation": rep.citation, "label": rep.label, "from": rep.source_case},
            "items": [asdict(i) | {"sections": sorted(i.sections)} for i in c.items]}


def merge_items(clusters: list[Cluster], new: Iterable) -> int:
    """Add newly missed items; returns how many clusters are new."""
    by_key = {(c.kind, c.sections): c for c in clusters}
    added = 0
    for it in new:
        c = by_key.get((it.kind, it.sections))
        if c is None:
            c = Cluster(kind=it.kind, sections=it.sections, jurisdiction=it.jurisdiction)
            clusters.append(c)
            by_key[(it.kind, it.sections)] = c
            added += 1
        if not any(i.source_case == it.source_case and i.label == it.label for i in c.items):
            c.items.append(it)
    return added


def update_priorities(clusters: list[Cluster]) -> None:
    for c in clusters:
        c.priority = (2 * c.resolved / c.given - 1) if c.given else 0.0


def swap_failing(clusters: list[Cluster], max_swaps: int) -> int:
    """Show a different training case's wording for items that keep failing."""
    n = 0
    for c in clusters:
        if c.useful >= 2 and c.resolved == 0 and c.swaps < max_swaps:
            current = c.representative()
            others = [j for j, it in enumerate(c.items) if it.label != current.label]
            if others:
                c.rep = max(others, key=lambda j: (c.items[j].weight, -len(c.items[j].label)))
                c.swaps += 1
                n += 1
    return n


def run_checklist_loop(
    train: list[Case],
    test: list[Case],
    teachers: dict[str, LegalReasoningGraph],
    student: StudentFn,
    embed: Embed,
    cfg: ChecklistLoopConfig = ChecklistLoopConfig(),
    *,
    index=None,
    party_names: Iterable[str] = (),
    on_round: Optional[Callable[[ChecklistRound, list[CaseRound], list[dict]], None]] = None,
) -> ChecklistLoopResult:
    for c in test:
        if c.role == "training":
            raise ValueError(f"{c.case_id} is a training case but was passed as test")
    names = list(party_names)
    targets = {c.case_id: teacher_targets(teachers[c.case_id], index=index) for c in train}
    clusters: list[Cluster] = []
    rounds: list[ChecklistRound] = []
    all_cases: list[CaseRound] = []
    stores: dict[int, list[dict]] = {}
    prev_notes: Optional[dict] = None
    best = best_train = math.inf
    best_round = best_round_train = stale = stale_train = 0
    epsilon = epsilon_train = 0.0
    stop_reason = "max_rounds"

    for t in range(cfg.max_rounds + 1):
        given = {c.case_id: (rank(clusters, c, "combined", embed=embed,
                                  support_weight=cfg.support_weight,
                                  priority_alpha=cfg.priority_alpha)[:cfg.k] if t > 0 else [])
                 for c in train + test}
        notes = {cid: render_checklist(cs) for cid, cs in given.items()}
        if t >= 1 and notes == prev_notes:
            stop_reason = "fixpoint"          # same prompts as last round → same answers
            break
        prev_notes = notes
        stores[t] = [cluster_record(c) for c in clusters]

        rows: list[CaseRound] = []
        observed = []
        for case in train + test:
            teacher = teachers[case.case_id]
            graph = student(case, notes[case.case_id], t)
            parsed = graph is not None
            report, al = score(teacher, graph if parsed else empty_graph(case.case_id))
            ro_rec = (sum(v is not None for v in al.rule_map.values())
                      + sum(v is not None for v in al.obligation_map.values()))
            rows.append(CaseRound(
                round=t, case_id=case.case_id, split=case.role, tier=case.tier, parsed=parsed,
                l_ged=report.l_ged, v_miss=len(report.v_miss), v_halluc=len(report.v_halluc),
                e_diff=len(report.e_diff), v_misground=len(report.v_misground),
                ro_total=len(teacher.rules) + len(teacher.obligations), ro_recovered=ro_rec,
                retrieved=[c.key for c in given[case.case_id]],
            ))
            if case.role == "training" and parsed:
                observed.append((case, report, al))

        # efficacy on training cases
        g_n = u_n = r_n = 0
        for case, _report, al in observed:
            shown = given[case.case_id]
            if not shown:
                continue
            for c in shown:
                c.given += 1
            g_n += len(shown)
            for c, gap in match_pairs(shown, targets[case.case_id], embed=embed):
                c.useful += 1
                u_n += 1
                m = al.obligation_map if gap.teacher_id.startswith("O") else al.rule_map
                if m.get(gap.teacher_id) is not None:
                    c.resolved += 1
                    r_n += 1

        # re-mine what the (patched) training students still miss
        new_items = []
        for case, report, _al in observed:
            new_items += missed_items(case, report, teachers[case.case_id], index=index,
                                      party_names=names)
        n_new = merge_items(clusters, new_items)
        n_swap = swap_failing(clusters, cfg.max_swaps) if t > 0 else 0
        update_priorities(clusters)

        def _rows(split, tier=None):
            return [r for r in rows if r.split == split and (tier is None or r.tier == tier)]

        def _rec(rs):
            tot = sum(r.ro_total for r in rs)
            return sum(r.ro_recovered for r in rs) / tot if tot else 0.0

        by_tier = {f"{s}/{tier}": round(_mean([r.l_ged for r in _rows(s, tier)]), 2)
                   for s in ("training", "test") for tier in sorted({r.tier for r in rows})
                   if _rows(s, tier)}
        summary = ChecklistRound(
            round=t, clusters=len(stores[t]), new_clusters=n_new, swapped=n_swap,
            given_train=g_n, useful_train=u_n, resolved_train=r_n,
            mean_lged_train=round(_mean([r.l_ged for r in _rows("training")]), 2),
            mean_lged_test=round(_mean([r.l_ged for r in _rows("test")]), 2),
            ro_recovery_train=round(_rec(_rows("training")), 4),
            ro_recovery_test=round(_rec(_rows("test")), 4),
            unparsed=sum(1 for r in rows if not r.parsed), by_tier=by_tier,
        )
        rounds.append(summary)
        all_cases.extend(rows)
        if on_round is not None:
            on_round(summary, rows, stores[t])

        m = summary.mean_lged_test if test else summary.mean_lged_train
        m_train = summary.mean_lged_train
        if t == 0:
            epsilon, epsilon_train = cfg.epsilon_frac * m, cfg.epsilon_frac * m_train
            best, best_train = m, m_train
            continue
        if m < best - epsilon:
            best, best_round, stale = m, t, 0
        else:
            stale += 1
        if m_train < best_train - epsilon_train:
            best_train, best_round_train, stale_train = m_train, t, 0
        else:
            stale_train += 1
        if stale >= cfg.patience and stale_train >= cfg.patience:
            stop_reason = "plateau"
            break

    return ChecklistLoopResult(config=asdict(cfg), rounds=rounds, cases=all_cases,
                               stop_reason=stop_reason, best_round=best_round,
                               best_round_train=best_round_train,
                               epsilon=round(epsilon, 3), stores=stores)


__all__ = ["ChecklistLoopConfig", "ChecklistRound", "ChecklistLoopResult", "run_checklist_loop",
           "merge_items", "update_priorities", "swap_failing", "cluster_record"]
